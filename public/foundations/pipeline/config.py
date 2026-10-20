"""
Configuração central do MCDM Studio.

Lê variáveis de ambiente (.env opcional) e expõe caminhos, parâmetros dos métodos
e a política de PARALELISMO do projeto (ProcessPoolExecutor + numba), conforme
_private/foundations/foundations.md.

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import os
from pathlib import Path

# Carrega .env se python-dotenv estiver disponível (opcional, sem quebrar se faltar).
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except Exception:
    pass

PIPELINE_DIR = Path(__file__).resolve().parent
FOUNDATIONS_DIR = PIPELINE_DIR.parent
PROJETO_DIR = FOUNDATIONS_DIR.parent.parent      # raiz do repositório
QUERIES_DIR = PIPELINE_DIR / "queries"
CASOS_DIR = PIPELINE_DIR / "casos"
EVIDENCE_DIR = FOUNDATIONS_DIR / "evidence"
STATIC_DIR = EVIDENCE_DIR / "static" / "mc"
TELAS_DIR = PROJETO_DIR / "_private" / "foundations" / "telas"

# Banco SQLite — compartilhado com o Evidence (fonte `mcdm`).
DB_PATH = os.environ.get("MCDM_DB_PATH", str(EVIDENCE_DIR / "sources" / "mcdm" / "mcdm.db"))

# Encoding único do projeto. TODA leitura/escrita de texto passa por aqui.
# (Ver bugs.md #BUG-004: leitura sem encoding explícito quebra em locale não-UTF-8.)
ENCODING = os.environ.get("MCDM_ENCODING", "utf-8")

# --- Métodos MCDM ----------------------------------------------------------
# ELECTRE I — limiares de concordância e discordância (Roy, 1968).
ELECTRE_C = float(os.environ.get("ELECTRE_C", "0.65"))   # concordância mínima
ELECTRE_D = float(os.environ.get("ELECTRE_D", "0.35"))   # discordância máxima

# PROMETHEE II — função de preferência default (Brans & Vincke, 1985).
PROMETHEE_TIPO = os.environ.get("PROMETHEE_TIPO", "linear")
PROMETHEE_Q = float(os.environ.get("PROMETHEE_Q", "0.10"))  # quantil p/ limiar de indiferença q
PROMETHEE_P = float(os.environ.get("PROMETHEE_P", "0.90"))  # quantil p/ limiar de preferência p

# MAUT — coeficiente de aversão a risco r (Keeney & Raiffa, 1976).
# r > 0 => utilidade côncava => aversão a risco. r = 0 => linear (neutro).
MAUT_AVERSAO = float(os.environ.get("MAUT_AVERSAO", "2.0"))

# MCDA-C — âncoras Neutro/Bom nos quantis observados (Ensslin et al., 2001).
MCDAC_NEUTRO = float(os.environ.get("MCDAC_NEUTRO", "0.25"))
MCDAC_BOM = float(os.environ.get("MCDAC_BOM", "0.75"))

# AHP — limite de consistência de Saaty.
AHP_CR_LIMITE = float(os.environ.get("AHP_CR_LIMITE", "0.10"))

# --- extensões fuzzy -------------------------------------------------------
# Banda PROPORCIONAL aplicada à matriz de decisão crisp para obter TFNs:
#   x → (x·(1−α), x, x·(1+α)).
# α = 0 NÃO devolve o TOPSIS clássico: Chen também troca a normalização (linear em
# vez de vetorial) e os ideais (absolutos em vez de relativos). Ver fuzzy.py.
# 10% é incerteza de medição plausível para preço de catálogo, nota 0-10 e
# especificação de ficha técnica — e está DECLARADA no relatório de cada caso,
# porque é hipótese nossa e não dado do caso.
FUZZY_ALPHA = float(os.environ.get("FUZZY_ALPHA", "0.10"))

# Espalhamento GEOMÉTRICO dos julgamentos: a_ij → (a_ij/g, a_ij, a_ij·g).
# g = 1,5 significa "quem disse 5 quis dizer entre 3,3 e 7,5". g = 1 desliga o
# espalhamento e reduz o AHP Fuzzy ao AHP crisp.
#
# Geométrico e não aditivo porque as matrizes deste projeto são razões em
# progressão geométrica e excedem a escala de Saaty [1/9, 9] em 35 dos 38 casos;
# o espalhamento aditivo com recorte corrompia o valor modal. Ver fuzzy.py.
FUZZY_FATOR_SAATY = float(os.environ.get("FUZZY_FATOR_SAATY", "1.5"))

# --- Robustez (perturbação de Dirichlet nos pesos) --------------------------
# w' ~ Dirichlet(κ·w). E[w'] = w; Var(w_i) = w_i(1-w_i)/(κ+1).
ROBUSTEZ_ITER = int(os.environ.get("ROBUSTEZ_ITER", "2000"))    # universos de preferência
ROBUSTEZ_KAPPA = float(os.environ.get("ROBUSTEZ_KAPPA", "200"))  # concentração
SEED = int(os.environ.get("MCDM_SEED", "42"))                    # reprodutibilidade

# --- Paralelismo e aceleração ----------------------------------------------
# Política do projeto: SEMPRE ProcessPoolExecutor para trabalho CPU-bound.
# 0 = detecta automaticamente (os.cpu_count()).
N_WORKERS = int(os.environ.get("MCDM_WORKERS", "0")) or (os.cpu_count() or 4)

# Trabalho mínimo para valer a pena pagar fork + pickle do ProcessPoolExecutor.
# Medido em unidades de (n_iter × n_alternativas² × n_criterios) — o custo real de
# um universo de preferência cresce com m², não com n_iter isoladamente. Abaixo
# deste limiar o executor SERIAL é mais rápido: com o caminho pré-compilado,
# 2.000 universos de 8×6 levam 1,8 s em série e 2,0 s em 4 processos, porque o
# fork custa mais que o cálculo. Ver bugs.md #BUG-008.
LIMIAR_TRABALHO_PARALELO = int(os.environ.get("MCDM_LIMIAR_TRABALHO", "1500000"))

# numba: JIT dos kernels numéricos quentes (ELECTRE/PROMETHEE são O(m²k)).
# Desligue com MCDM_NUMBA=0 para depurar em Python puro.
USAR_NUMBA = os.environ.get("MCDM_NUMBA", "1") not in ("0", "false", "False")

# Cython: usado apenas se o módulo compilado existir (build opcional, ver setup.py).
USAR_CYTHON = os.environ.get("MCDM_CYTHON", "1") not in ("0", "false", "False")

# --- Apresentação ----------------------------------------------------------
IDIOMA_PADRAO = os.environ.get("MCDM_IDIOMA", "pt")
IDIOMAS = ("pt", "en", "es", "fr", "de", "zh", "ko", "hi", "he", "ru", "sv", "fi")
DPI_FIGURAS = int(os.environ.get("MCDM_DPI", "150"))


def resumo() -> str:
    """Linha única com a configuração ativa — impressa no início de cada pipeline."""
    aceleracao = []
    if USAR_NUMBA:
        aceleracao.append("numba")
    if USAR_CYTHON:
        aceleracao.append("cython")
    return (
        f"⚙️  banco={Path(DB_PATH).name} · workers={N_WORKERS} · "
        f"aceleração={'+'.join(aceleracao) or 'nenhuma'} · "
        f"robustez={ROBUSTEZ_ITER:,} universos (κ={ROBUSTEZ_KAPPA:g}) · seed={SEED}"
    )


if __name__ == "__main__":
    print(resumo())
    print(f"   DB_PATH   = {DB_PATH}")
    print(f"   ENCODING  = {ENCODING}")
    print(f"   IDIOMAS   = {', '.join(IDIOMAS)} ({len(IDIOMAS)} idiomas)")
