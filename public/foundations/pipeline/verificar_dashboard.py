"""
Verificação do dashboard mais próxima do navegador que o `curl`.

POR QUE ESTE ARQUIVO EXISTE
---------------------------
`curl` retornando 200 NÃO prova que a página funciona. Numa SPA, o servidor entrega o
shell com sucesso e o erro acontece depois, no cliente: módulo que não compilou
(#BUG-027), volume de dados que trava o navegador (#BUG-028), coluna referenciada por
um `<Column id=...>` que não existe no schema servido.

Três defeitos seguidos deste projeto passaram por `curl` com 200 e log limpo, e foram
encontrados pelo usuário abrindo o navegador. Isto aqui não substitui a inspeção humana
— nada substitui —, mas fecha a parte verificável por máquina:

  1. o servidor responde em todas as rotas;
  2. nenhum erro de compilação no log do Vite;
  3. toda coluna citada por um `<Column id=...>` EXISTE no schema servido ao cliente;
  4. nenhuma consulta devolve conjunto vazio;
  5. o volume por página está abaixo do limiar que trava o navegador.

Uso:  python3 verificar_dashboard.py [--porta 3010]

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import argparse
import json
import os
import re
from datetime import datetime
import sqlite3
import subprocess
import sys
from pathlib import Path

from config import ENCODING, EVIDENCE_DIR

# Acima disto o navegador começa a engasgar — medido no #BUG-028, em que o índice
# carregava ~16 mil linhas e a página não abria.
LIMIAR_LINHAS_POR_PAGINA = 3000
# Mesmo caminho que evidence/subir_servidor.sh grava. Antes era "/tmp/evidence.log"
# fixo, enquanto o servidor passou a gravar em outro lugar — e o passo [2] seguiu
# lendo um log de uma subida ANTIGA e aprovando "0 erros". Ver bugs.md #BUG-036.
LOG_VITE = Path(os.environ.get("MCDM_EVIDENCE_LOG",
                               str(Path(os.environ.get("TMPDIR", "/tmp")) / "mcdm_evidence.log")))
SESSAO_SCREEN = "mcdm_evidence"

PROBLEMAS = []


def falhar(msg):
    PROBLEMAS.append(msg)
    print(f"  ❌ {msg}")


def ok(msg):
    print(f"  ✅ {msg}")


def _http(url, tempo=120):
    r = subprocess.run(["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}",
                        "--max-time", str(tempo), url],
                       capture_output=True, text=True)
    return r.stdout.strip()


def verificar_rotas(porta):
    print("\n[1] Rotas respondem")
    conn = sqlite3.connect(EVIDENCE_DIR / "sources" / "mcdm" / "mcdm.db")
    casos = [r[0] for r in conn.execute("SELECT id_caso FROM caso ORDER BY id_caso")]
    conn.close()

    rotas = ["", "en", "es", "fr", "de", "zh", "ko", "hi", "he", "ru", "sv", "fi"]
    ruins = [r for r in rotas if _http(f"http://localhost:{porta}/{r}") != "200"]
    (ok if not ruins else falhar)(
        f"{len(rotas) - len(ruins)}/{len(rotas)} rotas de idioma"
        + (f" — falharam: {', '.join(ruins)}" if ruins else ""))

    ruins = [c for c in casos if _http(f"http://localhost:{porta}/casos/{c}") != "200"]
    (ok if not ruins else falhar)(
        f"{len(casos) - len(ruins)}/{len(casos)} páginas de caso"
        + (f" — falharam: {', '.join(ruins)}" if ruins else ""))


def verificar_compilacao():
    print("\n[2] Compilação sem erro (log do Vite)")
    if not LOG_VITE.exists():
        falhar(f"log não encontrado: {LOG_VITE}")
        return
    # O log tem de ser DESTA subida. subir_servidor.sh recria o arquivo a cada início,
    # então um log mais antigo que a sessão screen do servidor é resto de outra
    # execução — e "0 erros" nele não diz nada sobre o servidor que está no ar.
    ls = subprocess.run(["screen", "-ls"], capture_output=True, text=True).stdout
    m = re.search(rf"\d+\.{SESSAO_SCREEN}\s+\((\d\d/\d\d/\d{{4}} \d\d:\d\d:\d\d [AP]M)\)", ls)
    if not m:
        falhar(f"sessão screen '{SESSAO_SCREEN}' não encontrada — suba com evidence/subir_servidor.sh")
        return
    inicio = datetime.strptime(m.group(1), "%m/%d/%Y %I:%M:%S %p").timestamp()
    if LOG_VITE.stat().st_mtime + 5 < inicio:
        falhar(f"log {LOG_VITE} é anterior à sessão do servidor — é de outra execução")
        return
    texto = LOG_VITE.read_text(encoding=ENCODING, errors="replace")
    # Log sem nenhuma linha do servidor não prova ausência de erro — prova ausência de log.
    if not re.search(r"localhost:\d+|ready in|Evaluated sources", texto):
        falhar(f"log {LOG_VITE} não contém saída do servidor — '0 erros' seria vazio")
        return
    padrao = re.compile(r"Internal server error|Pre-transform error|Expected valid tag",
                        re.I)
    achados = padrao.findall(texto)
    (ok if not achados else falhar)(
        f"{len(achados)} erro(s) de compilação no log")


def _schemas():
    """{nome_da_consulta: [colunas]} do que é efetivamente servido ao cliente."""
    base = EVIDENCE_DIR / ".evidence" / "template" / "static" / "data"
    saida = {}
    for f in base.rglob("*.schema.json"):
        try:
            saida[f.parent.name] = [c["name"] for c in
                                    json.loads(f.read_text(encoding=ENCODING))]
        except Exception:
            continue
    return saida


def verificar_colunas():
    """Toda coluna citada num <Column id=...> tem de existir no schema servido.

    É o erro que produz tabela em branco sem mensagem: o componente pede uma coluna
    que o parquet não tem, e simplesmente não desenha.
    """
    print("\n[3] Colunas referenciadas existem no schema servido")
    schemas = _schemas()
    if not schemas:
        falhar("nenhum schema encontrado — rode `npx evidence sources`")
        return
    ok(f"{len(schemas)} consultas com schema publicado")

    for pagina in (EVIDENCE_DIR / "pages").rglob("*.md"):
        texto = pagina.read_text(encoding=ENCODING)
        # {consulta} usado como data= ... e os <Column id=...> que vêm logo depois
        for bloco in re.finditer(
                r"<DataTable\s+data=\{(\w+)\}(.*?)</DataTable>", texto, re.S):
            consulta, corpo = bloco.group(1), bloco.group(2)
            # nome da consulta no markdown -> nome da fonte no SQL
            fonte = re.search(rf"```sql {consulta}\s*\n(.*?)```", texto, re.S)
            if not fonte:
                continue
            m = re.search(r"from\s+mcdm\.(\w+)", fonte.group(1), re.I)
            if not m or m.group(1) not in schemas:
                continue
            disponiveis = set(schemas[m.group(1)])
            pedidas = set(re.findall(r"<Column\s+id=(\w+)", corpo))
            faltando = pedidas - disponiveis
            if faltando:
                falhar(f"{pagina.name} · {consulta} → coluna(s) inexistente(s): "
                       f"{', '.join(sorted(faltando))}")


def verificar_volume():
    print("\n[4] Volume por página abaixo do limiar")
    conn = sqlite3.connect(EVIDENCE_DIR / "sources" / "mcdm" / "mcdm.db")
    for pagina in (EVIDENCE_DIR / "pages").rglob("*.md"):
        texto = pagina.read_text(encoding=ENCODING)
        total = 0
        for corpo in re.findall(r"```sql \w+\s*\n(.*?)```", texto, re.S):
            if "${params" in corpo:      # filtrada por caso — não soma no índice
                continue
            m = re.search(r"from\s+mcdm\.(\w+)", corpo, re.I)
            if not m:
                continue
            arquivo = EVIDENCE_DIR / "sources" / "mcdm" / f"{m.group(1)}.sql"
            if not arquivo.exists():
                continue
            try:
                sql = arquivo.read_text(encoding=ENCODING).rstrip().rstrip(";")
                total += len(conn.execute(sql).fetchall())
            except Exception:
                continue
        if total > LIMIAR_LINHAS_POR_PAGINA:
            falhar(f"{pagina.relative_to(EVIDENCE_DIR)} carrega {total:,} linhas "
                   f"(limiar {LIMIAR_LINHAS_POR_PAGINA:,}) — ver #BUG-028")
    conn.close()
    if not any("carrega" in p for p in PROBLEMAS):
        ok(f"nenhuma página acima de {LIMIAR_LINHAS_POR_PAGINA:,} linhas")


def verificar_consultas_vazias():
    print("\n[5] Nenhuma consulta devolve conjunto vazio")
    conn = sqlite3.connect(EVIDENCE_DIR / "sources" / "mcdm" / "mcdm.db")
    vazias = []
    for arquivo in sorted((EVIDENCE_DIR / "sources" / "mcdm").glob("*.sql")):
        try:
            sql = arquivo.read_text(encoding=ENCODING).rstrip().rstrip(";")
            if not conn.execute(sql).fetchall():
                vazias.append(arquivo.stem)
        except Exception as erro:
            falhar(f"{arquivo.name}: {erro}")
    conn.close()
    (ok if not vazias else falhar)(
        "todas as consultas devolvem dados" if not vazias
        else f"consulta(s) vazia(s): {', '.join(vazias)}")


def main():
    ap = argparse.ArgumentParser(description="Verifica o dashboard além do HTTP 200.")
    ap.add_argument("--porta", type=int, default=3010)
    args = ap.parse_args()

    print("=" * 78)
    print(" VERIFICAÇÃO DO DASHBOARD — o que o `curl 200` não prova")
    print("=" * 78)
    verificar_rotas(args.porta)
    verificar_compilacao()
    verificar_colunas()
    verificar_volume()
    verificar_consultas_vazias()

    print("\n" + "=" * 78)
    if PROBLEMAS:
        print(f" ❌ {len(PROBLEMAS)} problema(s)")
        print("=" * 78)
        return 1
    print(" ✅ TUDO OK — mas isto NÃO substitui abrir no navegador.")
    print("    Os #BUG-026, #BUG-027 e #BUG-028 foram encontrados por uma pessoa")
    print("    olhando a tela, não por verificação automatizada.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
