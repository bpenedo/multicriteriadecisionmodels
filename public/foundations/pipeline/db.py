"""
Camada de acesso ao banco: conexão, schema e carga da matriz de decisão.

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import sqlite3
from pathlib import Path

import numpy as np

from config import DB_PATH, ENCODING, PIPELINE_DIR


def get_conn() -> sqlite3.Connection:
    """Conexão com row_factory=Row e chaves estrangeiras ativas."""
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    # NÃO usar journal_mode = WAL aqui.
    #
    # WAL cria os arquivos auxiliares `<banco>-wal` e `<banco>-shm`, que surgem e
    # somem conforme as transações. O FSWatcher do Evidence observa o diretório de
    # sources e tenta copiar cada arquivo que aparece; quando chega no `-shm` ele
    # já foi removido, e o `lstatSync` lança ENOENT que **derruba o servidor**:
    #
    #     Error: ENOENT: no such file or directory, lstat 'sources/mcdm/mcdm.db-shm'
    #         at FSWatcher.syncFile (@evidence-dev/evidence/cli.js:82:7)
    #
    # O ganho do WAL aqui seria leitura concorrente durante a escrita — que na
    # prática não ocorre: o pipeline roda até o fim, e só depois o dashboard lê.
    # Trocamos um benefício que não usamos por um servidor que fica de pé.
    # Ver bugs.md #BUG-024.
    conn.execute("PRAGMA journal_mode = DELETE")
    return conn


def init_schema(silencioso: bool = False) -> None:
    """Executa schema.sql (idempotente)."""
    schema_sql = (PIPELINE_DIR / "schema.sql").read_text(encoding=ENCODING)
    conn = get_conn()
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()
    if not silencioso:
        print(f"✅ Schema inicializado em: {DB_PATH}")


def ler_sql(nome: str) -> str:
    """Lê um .sql de queries/ SEMPRE com encoding explícito (ver bugs.md #BUG-004)."""
    return (PIPELINE_DIR / "queries" / nome).read_text(encoding=ENCODING)


def carregar_caso(conn: sqlite3.Connection, id_caso: str):
    """Monta a matriz de decisão de um caso.

    Devolve (alternativas, criterios, rotulos, direcoes, X) onde X tem shape
    (n_alternativas, n_criterios), na ORDEM DECLARADA em `alternativa.ordem` e
    `criterio.ordem`. A ordem explícita é o que garante que a matriz do DEMATEL,
    a matriz do AHP e a matriz de decisão falem do mesmo critério na mesma posição
    (ver bugs.md #BUG-005: ordem implícita de dicionário causava desalinhamento).
    """
    alternativas = [r["alternativa"] for r in conn.execute(
        "SELECT alternativa FROM alternativa WHERE id_caso = ? ORDER BY ordem, alternativa",
        (id_caso,))]
    linhas_crit = conn.execute(
        "SELECT criterio, rotulo, direcao FROM criterio WHERE id_caso = ? ORDER BY ordem, criterio",
        (id_caso,)).fetchall()

    if not alternativas or not linhas_crit:
        raise ValueError(f"caso {id_caso!r} não tem alternativas ou critérios cadastrados")

    criterios = [r["criterio"] for r in linhas_crit]
    rotulos = [r["rotulo"] or r["criterio"] for r in linhas_crit]
    direcoes = [r["direcao"] for r in linhas_crit]

    idx_alt = {a: i for i, a in enumerate(alternativas)}
    idx_crit = {c: j for j, c in enumerate(criterios)}

    X = np.full((len(alternativas), len(criterios)), np.nan)
    for r in conn.execute(
            "SELECT alternativa, criterio, valor FROM avaliacao WHERE id_caso = ?", (id_caso,)):
        i, j = idx_alt.get(r["alternativa"]), idx_crit.get(r["criterio"])
        if i is not None and j is not None:
            X[i, j] = r["valor"]

    # Falha ALTO e cedo: uma célula ausente vira NaN e contamina todo o ranking em
    # silêncio (min/max/quantis viram NaN). Melhor quebrar aqui e dizer onde.
    if np.isnan(X).any():
        faltando = [(alternativas[i], criterios[j])
                    for i, j in zip(*np.where(np.isnan(X)))]
        raise ValueError(
            f"caso {id_caso!r}: matriz de decisão incompleta, "
            f"{len(faltando)} célula(s) sem valor: {faltando[:5]}"
            + (" ..." if len(faltando) > 5 else ""))

    return alternativas, criterios, rotulos, direcoes, X


def carregar_matriz_quadrada(conn, id_caso: str, tabela: str, criterios: list) -> np.ndarray:
    """Lê dematel_entrada ou ahp_entrada como matriz densa na ordem de `criterios`.

    Ausências viram 0 no DEMATEL (nenhuma influência) e 1 no AHP (indiferença),
    que são os elementos neutros de cada escala.
    """
    if tabela == "dematel_entrada":
        col_o, col_d, neutro = "origem", "destino", 0.0
    elif tabela == "ahp_entrada":
        col_o, col_d, neutro = "linha", "coluna", 1.0
    else:
        raise ValueError(f"tabela desconhecida: {tabela!r}")

    n = len(criterios)
    idx = {c: i for i, c in enumerate(criterios)}
    M = np.full((n, n), neutro)
    if tabela == "dematel_entrada":
        np.fill_diagonal(M, 0.0)
    else:
        np.fill_diagonal(M, 1.0)

    for r in conn.execute(
            f"SELECT {col_o} AS o, {col_d} AS d, valor_col FROM ("
            f"  SELECT {col_o}, {col_d}, "
            f"         {'intensidade' if tabela == 'dematel_entrada' else 'valor'} AS valor_col "
            f"  FROM {tabela} WHERE id_caso = ?)", (id_caso,)):
        i, j = idx.get(r["o"]), idx.get(r["d"])
        if i is not None and j is not None:
            M[i, j] = r["valor_col"]
    return M


if __name__ == "__main__":
    init_schema()
