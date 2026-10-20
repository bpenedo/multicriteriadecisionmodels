"""
Núcleo numérico dos métodos MCDM — kernels puros, sem I/O e sem banco.

Por que este módulo existe separado de `mcdm.py`:
  1. São FUNÇÕES PURAS (matriz entra, vetor sai). Isso as torna testáveis à mão
     e reutilizáveis fora do pipeline (notebook, API, outro projeto).
  2. São o alvo do JIT do numba e do ProcessPoolExecutor. Kernels sem estado e
     sem conexão de banco podem ser serializados para processos-filho; funções
     que carregam um `sqlite3.Connection` não podem.

ORIGEM DAS EQUAÇÕES
-------------------
  • DEMATEL      — Gabus & Fontela (Battelle Memorial Institute, 1972-73).
  • ELECTRE I    — Roy, B. (1968): concordância/discordância e núcleo (kernel).
  • PROMETHEE II — Brans & Vincke (1985): 6 funções de preferência, fluxo líquido φ.
  • MAUT         — Keeney & Raiffa (1976): utilidade aditiva com aversão a risco.
  • MCDA-C       — Ensslin, Montibeller & Noronha (2001): função de valor ancorada
                   em níveis Neutro (0) e Bom (100).
  • AHP          — Saaty (1980): autovetor principal + razão de consistência.
  • TOPSIS       — Hwang & Yoon (1981); variante 2N (dupla normalização).
  • Borda        — Borda (1781), consenso entre ordenações.

ARQUITETURA DE INTEGRAÇÃO
-------------------------
Segue John, J. (2025), "Integration of DEMATEL with Other MCDM Methods for
Comprehensive Techno-Economic Analysis" (_private/foundations/kb/): o DEMATEL
revela a estrutura causal entre critérios e deriva PESOS POR INFLUÊNCIA, que
então alimentam os métodos de ranqueamento — em vez de pesos arbitrados.

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import numpy as np

from config import (FUZZY_ALPHA, AHP_CR_LIMITE, ELECTRE_C, ELECTRE_D, MAUT_AVERSAO,
                    MCDAC_BOM, MCDAC_NEUTRO, PROMETHEE_P, PROMETHEE_Q,
                    PROMETHEE_TIPO, USAR_NUMBA)

# --- JIT opcional -----------------------------------------------------------
# Os kernels de ELECTRE e PROMETHEE são O(m²k) com laços aninhados: é exatamente
# o padrão em que o numba paga. Se o numba faltar, `njit` vira identidade e o
# código roda em NumPy puro — mesma resposta, mais devagar.
try:
    if not USAR_NUMBA:
        raise ImportError("numba desabilitado por configuração (MCDM_NUMBA=0)")
    from numba import njit
    NUMBA_ATIVO = True
except ImportError:                                    # pragma: no cover
    NUMBA_ATIVO = False

    def njit(*args, **kwargs):                         # noqa: D103
        def _decorador(funcao):
            return funcao
        return _decorador(args[0]) if args and callable(args[0]) else _decorador


# ---------------------------------------------------------------------------
# Normalização — a direção do critério é embutida aqui, uma vez só.
# ---------------------------------------------------------------------------
def orientar(X, direcoes):
    """Normaliza para [0,1] embutindo a direção: na saída, MAIOR é SEMPRE MELHOR.

    Critério de benefício: (x - min) / (max - min).
    Critério de custo:     (max - x) / (max - min).
    Coluna constante vira 0.5 — indiferença. (Zerar, como fazia o framework de
    origem, embute um viés: uma coluna constante passaria a "punir" toda
    alternativa no MAUT, cuja utilidade é ancorada em 0.)
    """
    X = np.asarray(X, dtype=np.float64)
    G = np.empty_like(X)
    for j in range(X.shape[1]):
        col = X[:, j]
        lo, hi = col.min(), col.max()
        if hi <= lo:
            G[:, j] = 0.5
        elif direcoes[j] == "benefit":
            G[:, j] = (col - lo) / (hi - lo)
        else:
            G[:, j] = (hi - col) / (hi - lo)
    return G


def _normalizar_pesos(w, n_criterios):
    """Valida e normaliza o vetor de pesos para somar 1."""
    w = np.asarray(w, dtype=np.float64).ravel()
    if w.size != n_criterios:
        raise ValueError(f"pesos: esperados {n_criterios}, recebidos {w.size}")
    if np.any(w < 0):
        raise ValueError("pesos negativos não fazem sentido em MCDM")
    total = w.sum()
    if total <= 0:
        raise ValueError("soma dos pesos é zero")
    return w / total


# ---------------------------------------------------------------------------
# DEMATEL — Gabus & Fontela (Battelle).
# ---------------------------------------------------------------------------
def dematel(Z):
    """Matriz de relação direta Z -> (R, C, proeminência, relação, pesos, T, limiar).

    Passos:
      1. Normaliza por s = max(maior soma de linha, maior soma de coluna) -> X.
      2. Matriz de relação TOTAL  T = X(I - X)⁻¹  (soma da série de Neumann ΣXᵏ:
         captura influência DIRETA e INDIRETA, de qualquer comprimento de caminho).
      3. R = somas das linhas (influência exercida); C = somas das colunas (recebida).
      4. Proeminência = R + C (importância no sistema); Relação = R − C
         (> 0 = CAUSA, alavanca; < 0 = EFEITO, termômetro).
      5. Peso_i = sqrt((R+C)_i² + (R−C)_i²), normalizado para somar 1.
      6. Limiar α = média de T: define quais arestas entram no diagrama de influência.
    """
    Z = np.asarray(Z, dtype=np.float64)
    if Z.ndim != 2 or Z.shape[0] != Z.shape[1]:
        raise ValueError(f"DEMATEL exige matriz quadrada, recebida {Z.shape}")

    s = max(Z.sum(axis=1).max(), Z.sum(axis=0).max())
    if s <= 0:
        raise ValueError("matriz DEMATEL é toda zero: nenhuma influência declarada")
    X = Z / s
    n = X.shape[0]

    # (I - X) é inversível porque o raio espectral de X é < 1 por construção da
    # normalização; ainda assim usamos solve em vez de inv — mais estável e mais
    # rápido do que formar a inversa explicitamente.
    T = np.linalg.solve(np.eye(n) - X.T, X.T).T

    R, C = T.sum(axis=1), T.sum(axis=0)
    prominencia, relacao = R + C, R - C
    pesos = np.sqrt(prominencia ** 2 + relacao ** 2)
    pesos = pesos / pesos.sum()
    return R, C, prominencia, relacao, pesos, T, float(T.mean())


# ---------------------------------------------------------------------------
# ELECTRE I — Roy (1968).
# ---------------------------------------------------------------------------
@njit(cache=True, fastmath=True)
def _electre_kernel(G, w, c_limiar, d_limiar):
    """Concordância/discordância par a par. G já orientado (maior = melhor).

    C(a,b) = soma dos pesos dos critérios em que a é ao menos tão bom quanto b.
    D(a,b) = maior desvantagem de a frente a b (G ∈ [0,1], logo já é a amplitude).
    a sobreclassifica b  <=>  C(a,b) >= c_limiar  E  D(a,b) <= d_limiar.
    """
    m, k = G.shape
    S = np.zeros((m, m), dtype=np.bool_)
    for a in range(m):
        for b in range(m):
            if a == b:
                continue
            conc = 0.0
            disc = 0.0
            for j in range(k):
                if G[a, j] >= G[b, j]:
                    conc += w[j]
                else:
                    d = G[b, j] - G[a, j]
                    if d > disc:
                        disc = d
            if conc >= c_limiar and disc <= d_limiar:
                S[a, b] = True
    return S


def electre_i(X, w, direcoes, c_limiar=ELECTRE_C, d_limiar=ELECTRE_D):
    """Devolve (score, nucleo, S).

    score  = grau de sobreclassificação líquido (quantas domina − por quantas é dominada).
    nucleo = alternativas não dominadas por ninguém (kernel de Roy).
    S      = matriz booleana de sobreclassificação.

    Nota sobre a discordância: G já está normalizado em [0,1] pela `orientar`, então
    a amplitude de cada critério é 1 por construção e a divisão por `np.ptp` que o
    framework de origem fazia era um no-op — removida (ver bugs.md #BUG-006).
    """
    G = orientar(X, direcoes)
    w = _normalizar_pesos(w, G.shape[1])
    S = _electre_kernel(G, w, float(c_limiar), float(d_limiar))

    domina = S.sum(axis=1)
    dominada = S.sum(axis=0)
    score = (domina - dominada).astype(np.float64)
    nucleo = [i for i in range(G.shape[0]) if dominada[i] == 0]
    return score, nucleo, S


# ---------------------------------------------------------------------------
# PROMETHEE II — Brans & Vincke (1985).
# ---------------------------------------------------------------------------
# Códigos das 6 funções de preferência generalizadas (numba não aceita str).
TIPO_PREFERENCIA = {"usual": 0, "u-shape": 1, "v-shape": 2,
                    "level": 3, "linear": 4, "gaussian": 5}


@njit(cache=True, fastmath=True)
def _preferencia(d, tipo, q, p, s):
    """Grau de preferência para um desvio d = g(a) − g(b), já orientado."""
    if d <= 0.0:
        return 0.0
    if tipo == 0:                      # usual: qualquer diferença conta
        return 1.0
    if tipo == 1:                      # u-shape: só acima do limiar de indiferença
        return 1.0 if d > q else 0.0
    if tipo == 2:                      # v-shape: linear até p
        return d / p if d < p else 1.0
    if tipo == 3:                      # level: degrau em meio-passo
        if d <= q:
            return 0.0
        return 0.5 if d <= p else 1.0
    if tipo == 4:                      # linear: v-shape com zona de indiferença
        if d <= q:
            return 0.0
        if d >= p:
            return 1.0
        return (d - q) / (p - q)
    if tipo == 5:                      # gaussiana: sem descontinuidade
        return 1.0 - np.exp(-(d * d) / (2.0 * s * s))
    return 0.0


@njit(cache=True, fastmath=True)
def _promethee_kernel(G, w, tipo, qs, ps, ss):
    """Índice de preferência agregado Π(a,b) e fluxos φ⁺, φ⁻."""
    m, k = G.shape
    phi_mais = np.zeros(m)
    phi_menos = np.zeros(m)
    for a in range(m):
        for b in range(m):
            if a == b:
                continue
            pi_ab = 0.0
            for j in range(k):
                pi_ab += w[j] * _preferencia(G[a, j] - G[b, j], tipo, qs[j], ps[j], ss[j])
            phi_mais[a] += pi_ab
            phi_menos[b] += pi_ab
    if m > 1:
        phi_mais /= (m - 1)
        phi_menos /= (m - 1)
    return phi_mais, phi_menos


def promethee_ii(X, w, direcoes, tipo=PROMETHEE_TIPO):
    """Fluxo líquido φ = φ⁺ − φ⁻ (pré-ordem COMPLETA, sem incomparabilidades).

    Limiares q (indiferença) e p (preferência estrita) são tirados dos quantis 10%
    e 90% dos desvios |d| observados EM CADA CRITÉRIO — prática usual quando não há
    limiares elicitados com o decisor. Quando p colapsa em q (critério quase
    constante), abrimos uma folga mínima para não dividir por zero.
    """
    G = orientar(X, direcoes)
    m, k = G.shape
    w = _normalizar_pesos(w, k)
    if tipo not in TIPO_PREFERENCIA:
        raise ValueError(
            f"função de preferência desconhecida: {tipo!r}. "
            f"Use uma de: {', '.join(TIPO_PREFERENCIA)}")

    qs, ps, ss = np.empty(k), np.empty(k), np.empty(k)
    fora_diag = ~np.eye(m, dtype=bool)
    for j in range(k):
        d = np.abs(G[:, j][:, None] - G[:, j][None, :])[fora_diag]
        q = float(np.quantile(d, PROMETHEE_Q)) if d.size else 0.0
        p = float(np.quantile(d, PROMETHEE_P)) if d.size else 1.0
        if p <= q:
            p = q + 1e-9
        qs[j], ps[j] = q, p
        ss[j] = max(float(d.std()) if d.size else 0.5, 1e-9)   # σ da gaussiana

    phi_mais, phi_menos = _promethee_kernel(
        G, w, TIPO_PREFERENCIA[tipo], qs, ps, ss)
    return phi_mais - phi_menos


# ---------------------------------------------------------------------------
# MAUT — Keeney & Raiffa (1976).
# ---------------------------------------------------------------------------
def maut(X, w, direcoes, aversao=MAUT_AVERSAO):
    """Utilidade aditiva U(a) = Σ wⱼ·uⱼ(a) com utilidade exponencial.

    u(z) = (1 − e^{−r·z}) / (1 − e^{−r}),  z ∈ [0,1] já orientado ao benefício.
    r > 0 => côncava => AVERSÃO A RISCO (ganho marginal decrescente: os primeiros
    pontos de desempenho valem mais que os últimos). r = 0 => linear (neutro).
    Válida sob independência aditiva em preferência/utilidade entre os critérios.
    """
    G = orientar(X, direcoes)
    w = _normalizar_pesos(w, G.shape[1])
    r = float(aversao)
    if abs(r) < 1e-12:
        U = G
    else:
        U = (1.0 - np.exp(-r * G)) / (1.0 - np.exp(-r))
    return U @ w


# ---------------------------------------------------------------------------
# MCDA-C — Ensslin, Montibeller & Noronha (2001).
# ---------------------------------------------------------------------------
def mcda_c(X, w, direcoes, q_neutro=MCDAC_NEUTRO, q_bom=MCDAC_BOM):
    """Função de valor ancorada: V = 0 no nível NEUTRO, V = 100 no nível BOM.

    Na ausência de descritores construídos com o decisor (fase de estruturação do
    MCDA-C), ancoramos nos quartis observados: Neutro = Q1 e Bom = Q3 (invertidos
    nos critérios de custo). A função é linear por partes e EXTRAPOLA fora das
    âncoras — é isso que produz as faixas de diagnóstico do método:

        V < 0        -> COMPROMETEDOR (abaixo do nível neutro: inaceitável)
        0 ≤ V ≤ 100  -> COMPETITIVO   (dentro do mercado)
        V > 100      -> EXCELÊNCIA    (acima do nível bom)

    É a única saída do sistema com significado ABSOLUTO — as demais são relativas
    ao conjunto de alternativas comparadas.
    """
    X = np.asarray(X, dtype=np.float64)
    w = _normalizar_pesos(w, X.shape[1])
    V = np.zeros_like(X)
    for j in range(X.shape[1]):
        col = X[:, j]
        if direcoes[j] == "benefit":
            neutro, bom = np.quantile(col, q_neutro), np.quantile(col, q_bom)
        else:
            neutro, bom = np.quantile(col, 1 - q_neutro), np.quantile(col, 1 - q_bom)
        span = bom - neutro
        V[:, j] = 100.0 * (col - neutro) / span if span != 0 else 0.0
    return V @ w


# ---------------------------------------------------------------------------
# AHP — Saaty (1980).
# ---------------------------------------------------------------------------
# Índice Aleatório de Saaty. Estendido até n = 15 (Saaty, 1980, e extensões de
# Alonso & Lamata, 2006) — o framework de origem parava em n = 8 e devolvia CR = 0
# em silêncio acima disso, o que faz um julgamento INCONSISTENTE passar como
# perfeito. Ver bugs.md #BUG-001.
RI = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
      9: 1.45, 10: 1.49, 11: 1.51, 12: 1.48, 13: 1.56, 14: 1.57, 15: 1.59}


def pesos_ahp(A):
    """Autovetor principal -> pesos; devolve (pesos, CR, lambda_max).

    O autovetor principal é o do autovalor de MAIOR MÓDULO (Perron-Frobenius), não
    o de maior parte real: para matrizes recíprocas fortemente inconsistentes os
    autovalores saem complexos e as duas escolhas divergem. Ver bugs.md #BUG-002.

    CR = (λmax − n) / ((n − 1) · RI(n)).  CR < 0,10 => julgamentos aceitáveis.
    """
    A = np.asarray(A, dtype=np.float64)
    n = A.shape[0]
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError(f"AHP exige matriz quadrada, recebida {A.shape}")
    if np.any(A <= 0):
        raise ValueError("matriz de Saaty deve ser positiva (escala 1/9..9)")

    autovalores, autovetores = np.linalg.eig(A)
    k = int(np.argmax(np.abs(autovalores)))            # Perron-Frobenius
    w = np.abs(autovetores[:, k].real)
    w = w / w.sum()
    lmax = float(autovalores[k].real)

    if n <= 2:
        cr = 0.0                                       # sempre consistente por construção
    elif n in RI and RI[n] > 0:
        cr = ((lmax - n) / (n - 1)) / RI[n]
    else:
        # Acima da tabela: aproximação de Alonso & Lamata (2006), RI ≈ 0.00149·n + 1.3454.
        # Melhor uma estimativa declarada do que um zero silencioso.
        cr = ((lmax - n) / (n - 1)) / (0.00149 * n + 1.3454)
    return w, float(cr), lmax


def ahp_consistente(cr, limite=AHP_CR_LIMITE) -> bool:
    """CR abaixo do limite de Saaty (0,10) => julgamentos par a par aceitáveis."""
    return cr < limite


# ---------------------------------------------------------------------------
# TOPSIS — Hwang & Yoon (1981), variante 2N (dupla normalização).
# ---------------------------------------------------------------------------
def topsis(X, w, direcoes, modo="vector"):
    """Coeficiente de proximidade Ci ∈ [0,1] para uma normalização.

    modo='vector' — normalização vetorial/Euclidiana: rᵢⱼ = xᵢⱼ / √(Σᵢ xᵢⱼ²).
    modo='minmax' — normalização linear com direção embutida.

    Ci = d⁻ / (d⁺ + d⁻). Ci → 1 = perto da solução ideal positiva.
    """
    X = np.asarray(X, dtype=np.float64)
    w = _normalizar_pesos(w, X.shape[1])

    if modo == "vector":
        norma = np.sqrt((X ** 2).sum(axis=0))
        R = X / np.where(norma == 0, 1.0, norma)
        V = R * w
        ideal_pos = np.array([V[:, j].max() if direcoes[j] == "benefit" else V[:, j].min()
                              for j in range(V.shape[1])])
        ideal_neg = np.array([V[:, j].min() if direcoes[j] == "benefit" else V[:, j].max()
                              for j in range(V.shape[1])])
    elif modo == "minmax":
        V = orientar(X, direcoes) * w                  # direção já embutida
        ideal_pos, ideal_neg = V.max(axis=0), V.min(axis=0)
    else:
        raise ValueError(f"modo de normalização desconhecido: {modo!r}")

    d_pos = np.sqrt(((V - ideal_pos) ** 2).sum(axis=1))
    d_neg = np.sqrt(((V - ideal_neg) ** 2).sum(axis=1))
    soma = d_pos + d_neg
    return d_neg / np.where(soma == 0, 1.0, soma)


def ahp_topsis_2n(X, w, direcoes):
    """AHP-TOPSIS 2N: devolve (ci_vector, ci_minmax, ci_final).

    A dupla normalização é o coração do "2N": TOPSIS é sensível à normalização
    escolhida, e um ranking que muda conforme a normalização é um ranking que não
    se deve levar ao comitê. Rodar as duas e comparar transforma essa fragilidade
    em INFORMAÇÃO — a coluna "concordante" do relatório.
    """
    ci_v = topsis(X, w, direcoes, "vector")
    ci_m = topsis(X, w, direcoes, "minmax")
    return ci_v, ci_m, (ci_v + ci_m) / 2.0


# ---------------------------------------------------------------------------
# Ranking e consenso.
# ---------------------------------------------------------------------------
@njit(cache=True)
def _ranks_kernel(score):
    """argsort decrescente estável + atribuição de posições, em um só passe."""
    n = score.size
    ordem = np.argsort(-score, kind="mergesort")     # mergesort = estável
    rk = np.empty(n, dtype=np.int64)
    for pos in range(n):
        rk[ordem[pos]] = pos + 1
    return rk


def ranks(score):
    """Posição 1 = melhor (maior score). Empates recebem posições distintas e estáveis.

    Chamado uma vez por método mais uma pelo consenso, a cada universo de preferência
    (hoje `len(METODOS) + 1`), sobre vetores de poucas dezenas de elementos: é o regime
    em que o overhead de despacho do NumPy supera a conta em si, e o JIT do numba paga.
    """
    return _ranks_kernel(np.ascontiguousarray(score, dtype=np.float64))


def borda(matriz_ranks, n_alternativas):
    """Contagem de Borda: cada método dá (n − posição) pontos. Maior soma vence."""
    M = np.asarray(matriz_ranks, dtype=np.float64)     # (n_metodos, n_alternativas)
    return (n_alternativas - M).sum(axis=0).astype(np.int64)


def pontuar_todos(X, w, direcoes):
    """Score de TODOS os métodos para um vetor de pesos. Maior = melhor, sempre.

    É o CAMINHO LENTO: chama cada método direto, sem o pré-cômputo de
    `ProblemaPreparado`. A robustez usa `prep.pontuar()`; esta função existe para
    duas situações em que o caminho rápido não serve — a suíte, que compara os dois
    para provar que a otimização não mudou resultado, e o caso grande demais para o
    tensor de preferência, para onde o `MemoryError` de `ProblemaPreparado` aponta.

    Por isso ela **tem de cobrir `METODOS` inteiro**: um caminho de fuga que devolve
    menos métodos que o normal entrega uma análise incompleta a quem já está num
    cenário degradado — e sem erro nenhum (#BUG-049).

    Pura: recebe arrays, devolve dict de arrays, não toca em banco nem em disco.
    """
    from fuzzy import fuzzy_topsis_de_crisp
    from metodos_br import electre_ii, sapevo_m_de_matriz, todim, vikor
    _, _, ci_final = ahp_topsis_2n(X, w, direcoes)
    pontos = {
        "ELECTRE I":     electre_i(X, w, direcoes)[0],
        "ELECTRE II":    electre_ii(X, w, direcoes)[0],
        "PROMETHEE II":  promethee_ii(X, w, direcoes),
        "MAUT":          maut(X, w, direcoes),
        "MCDA-C":        mcda_c(X, w, direcoes),
        "AHP-TOPSIS 2n": ci_final,
        "VIKOR":         vikor(X, w, direcoes)[0],
        "TODIM":         todim(X, w, direcoes)[0],
        "SAPEVO-M":      sapevo_m_de_matriz(X, direcoes, w),
        "TOPSIS Fuzzy":  fuzzy_topsis_de_crisp(X, w, direcoes),
    }
    faltando = set(METODOS) - set(pontos)
    if faltando:                      # método novo em METODOS sem par aqui
        raise RuntimeError(f"pontuar_todos não cobre {sorted(faltando)}")
    return pontos


# Dez escolas de decisão: cinco da literatura clássica internacional, quatro da
# escola brasileira de AMD (ver metodos_br.py) e uma da família fuzzy (ver fuzzy.py).
#
# O TOPSIS Fuzzy NÃO é "o TOPSIS com ruído": além dos números triangulares, ele
# troca a normalização (linear em vez de vetorial) e a solução ideal (absoluta em
# vez de relativa). Divergir do AHP-TOPSIS 2n é o comportamento esperado — e é
# informação sobre a sensibilidade do caso, não defeito.
METODOS = ("ELECTRE I", "ELECTRE II", "PROMETHEE II", "MAUT", "MCDA-C",
           "AHP-TOPSIS 2n", "VIKOR", "TODIM", "SAPEVO-M", "TOPSIS Fuzzy")
CONSENSO = "CONSENSO (Borda)"


if __name__ == "__main__":
    print(f"Núcleo MCDM · numba {'ATIVO' if NUMBA_ATIVO else 'inativo (NumPy puro)'}")
    print(f"Métodos: {', '.join(METODOS)}")
    print(f"Funções de preferência PROMETHEE: {', '.join(TIPO_PREFERENCIA)}")
    print(f"Índice Aleatório de Saaty tabelado até n = {max(RI)}")


# ===========================================================================
# CAMINHO RÁPIDO — pré-compilação do problema (performance tuning)
# ===========================================================================
# OBSERVAÇÃO QUE MUDA TUDO: na análise de robustez, X e as direções são FIXOS;
# só o vetor de pesos w varia entre os 2.000 universos. E os métodos são
# LINEARES em w:
#
#   ELECTRE I    C(a,b) = Σⱼ wⱼ·1[Gₐⱼ ≥ G_bⱼ]      → C = tensordot(w, MASC)
#                D(a,b) não depende de w             → constante
#   PROMETHEE II Π(a,b) = Σⱼ wⱼ·Pⱼ(a,b)             → Π = tensordot(w, PREF)
#   MAUT         U(a)   = Σⱼ wⱼ·uⱼ(a)               → U = MAT_MAUT @ w
#   MCDA-C       V(a)   = Σⱼ wⱼ·vⱼ(a)               → V = MAT_MCDAC @ w
#   TOPSIS       V = R·w com R constante nas duas normalizações
#
# Logo TODO o trabalho O(m²k) — normalizar, calcular quantis, avaliar as funções
# de preferência — pode sair do laço e ser feito UMA vez. O que sobra por universo
# é álgebra linear em cima de tensores já prontos.
#
# Medido em 8 alternativas × 6 critérios × 2.000 universos: 42,3 s → 0,35 s.

# Acima disto o tensor de preferência (k × m × m) fica grande demais para valer a
# pena materializar; o caminho lento (kernel numba) volta a ser preferível.
LIMITE_TENSOR_MB = 512


class ProblemaPreparado:
    """Tudo que NÃO depende dos pesos, calculado uma vez só.

    Depois disso, `pontuar(w)` custa um punhado de produtos matriz-vetor em vez de
    reprocessar a matriz de decisão inteira. É a estrutura que o ProcessPoolExecutor
    envia ao processo-filho: um único pickle de arrays contíguos, e nenhum trabalho
    redundante do outro lado.
    """

    __slots__ = ("X", "direcoes", "G", "m", "k", "masc_conc", "disc",
                 "pref", "mat_maut", "mat_mcdac", "r_vector", "sinal_vector",
                 "c_limiar", "d_limiar", "conc_pesada", "mat_sapevo", "dif",
                 "r_fuzzy")

    def __init__(self, X, direcoes, tipo_preferencia=PROMETHEE_TIPO,
                 aversao=MAUT_AVERSAO, q_neutro=MCDAC_NEUTRO, q_bom=MCDAC_BOM,
                 c_limiar=ELECTRE_C, d_limiar=ELECTRE_D):
        self.X = np.ascontiguousarray(X, dtype=np.float64)
        self.direcoes = list(direcoes)
        self.G = orientar(self.X, self.direcoes)
        self.m, self.k = self.G.shape
        self.c_limiar, self.d_limiar = float(c_limiar), float(d_limiar)

        bytes_tensor = self.k * self.m * self.m * 8
        if bytes_tensor > LIMITE_TENSOR_MB * 1024 ** 2:
            raise MemoryError(
                f"tensor de preferência exigiria {bytes_tensor/1024**3:.1f} GB "
                f"({self.m} alternativas × {self.k} critérios). "
                f"Use o caminho lento (pontuar_todos) ou aumente LIMITE_TENSOR_MB.")

        # --- ELECTRE I: máscara de concordância e matriz de discordância -----
        # d[j,a,b] = Gᵦⱼ − Gₐⱼ, a desvantagem de a frente a b no critério j.
        d = self.G.T[:, None, :] - self.G.T[:, :, None]      # (k, m, m)
        self.masc_conc = (d <= 0)                            # a é ao menos tão bom quanto b
        self.disc = np.maximum(d, 0.0).max(axis=0)           # (m, m) — independe de w

        # --- PROMETHEE II: tensor das preferências ---------------------------
        if tipo_preferencia not in TIPO_PREFERENCIA:
            raise ValueError(f"função de preferência desconhecida: {tipo_preferencia!r}")
        cod = TIPO_PREFERENCIA[tipo_preferencia]
        dif = np.ascontiguousarray(-d)                       # dif[j,a,b] = Gₐⱼ − Gᵦⱼ
        fora = ~np.eye(self.m, dtype=bool)
        self.pref = np.empty_like(dif)
        for j in range(self.k):
            absd = np.abs(dif[j])[fora]
            q = float(np.quantile(absd, PROMETHEE_Q)) if absd.size else 0.0
            p = float(np.quantile(absd, PROMETHEE_P)) if absd.size else 1.0
            if p <= q:
                p = q + 1e-9
            s = max(float(absd.std()) if absd.size else 0.5, 1e-9)
            self.pref[j] = _preferencia_vetorial(dif[j], cod, q, p, s)
        for j in range(self.k):
            np.fill_diagonal(self.pref[j], 0.0)

        # --- MAUT: utilidade exponencial já aplicada -------------------------
        r = float(aversao)
        self.mat_maut = (self.G if abs(r) < 1e-12
                         else (1.0 - np.exp(-r * self.G)) / (1.0 - np.exp(-r)))

        # --- MCDA-C: função de valor ancorada em Neutro/Bom ------------------
        V = np.zeros_like(self.X)
        for j in range(self.k):
            col = self.X[:, j]
            if self.direcoes[j] == "benefit":
                neutro, bom = np.quantile(col, q_neutro), np.quantile(col, q_bom)
            else:
                neutro, bom = np.quantile(col, 1 - q_neutro), np.quantile(col, 1 - q_bom)
            span = bom - neutro
            V[:, j] = 100.0 * (col - neutro) / span if span != 0 else 0.0
        self.mat_mcdac = V

        # --- TOPSIS: normalização vetorial (a min-max já é G) ----------------
        norma = np.sqrt((self.X ** 2).sum(axis=0))
        self.r_vector = self.X / np.where(norma == 0, 1.0, norma)
        self.sinal_vector = np.array(
            [1.0 if dd == "benefit" else -1.0 for dd in self.direcoes])

        # --- TOPSIS Fuzzy: a normalização de Chen não depende de w -----------
        # Fuzzificar e normalizar é O(mk) e constante entre universos; só a
        # ponderação ṽ = r̃ ⊗ w̃ muda. Fica aqui pelo mesmo motivo de todo o resto
        # desta classe: 2.000 universos não podem refazer o que não muda.
        from fuzzy import fuzzificar_matriz, normalizar_fuzzy_chen
        self.r_fuzzy = normalizar_fuzzy_chen(
            fuzzificar_matriz(self.X, FUZZY_ALPHA), self.direcoes)   # (m, k, 3)

        # --- TODIM: as diferenças por critério não dependem de w -------------
        self.dif = dif                                       # (k, m, m)

        # --- SAPEVO-M adaptado: a matriz de avaliação é constante ------------
        # (só os pesos mudam entre universos, e eles multiplicam por fora)
        from metodos_br import _normalizar_sapevo
        mat = np.zeros((self.m, self.k))
        for j in range(self.k):
            graus = np.clip(np.round(dif[j] * 3.0), -3, 3)
            np.fill_diagonal(graus, 0.0)
            mat[:, j] = _normalizar_sapevo(graus.sum(axis=1))
        self.mat_sapevo = mat

    # -- métodos individuais, todos O(m²) ou O(mk) por chamada ---------------
    def electre(self, w):
        C = np.tensordot(w, self.masc_conc, axes=(0, 0))     # (m, m)
        S = (C >= self.c_limiar) & (self.disc <= self.d_limiar)
        np.fill_diagonal(S, False)
        return (S.sum(axis=1) - S.sum(axis=0)).astype(np.float64)

    def promethee(self, w):
        PI = np.tensordot(w, self.pref, axes=(0, 0))         # (m, m)
        denom = self.m - 1 if self.m > 1 else 1
        return (PI.sum(axis=1) - PI.sum(axis=0)) / denom

    def maut(self, w):
        return self.mat_maut @ w

    def mcdac(self, w):
        return self.mat_mcdac @ w

    def topsis_2n(self, w):
        cis = []
        for R, embutido in ((self.r_vector, False), (self.G, True)):
            V = R * w
            if embutido:                                     # min-max: maior já é melhor
                ip, ineg = V.max(axis=0), V.min(axis=0)
            else:                                            # vetorial: respeita a direção
                alto, baixo = V.max(axis=0), V.min(axis=0)
                ip = np.where(self.sinal_vector > 0, alto, baixo)
                ineg = np.where(self.sinal_vector > 0, baixo, alto)
            d_pos = np.sqrt(((V - ip) ** 2).sum(axis=1))
            d_neg = np.sqrt(((V - ineg) ** 2).sum(axis=1))
            soma = d_pos + d_neg
            cis.append(d_neg / np.where(soma == 0, 1.0, soma))
        return (cis[0] + cis[1]) / 2.0

    def electre_ii(self, w, c_forte=0.75, c_fraca=0.60, d_forte=0.25, d_fraca=0.40):
        """ELECTRE II — Roy & Bertier (1971). Pré-ordem completa por destilação."""
        from metodos_br import _destilar_relacao
        C = np.tensordot(w, self.masc_conc, axes=(0, 0))
        forte = (C >= c_forte) & (self.disc <= d_forte)
        fraca = (C >= c_fraca) & (self.disc <= d_fraca)
        np.fill_diagonal(forte, False)
        np.fill_diagonal(fraca, False)
        desc = _destilar_relacao(forte, self.m, True)
        asc = _destilar_relacao(fraca, self.m, False)
        return -((desc + (asc.max() + 1 - asc)) / 2.0)

    def vikor(self, w, v=0.5):
        """VIKOR — Opricovic. Devolve −Q (maior = melhor, para compor no consenso)."""
        pen = w * (1.0 - self.G)
        S, R = pen.sum(axis=1), pen.max(axis=1)
        ds = (S.max() - S.min()) or 1.0
        dr = (R.max() - R.min()) or 1.0
        Q = v * (S - S.min()) / ds + (1.0 - v) * (R - R.min()) / dr
        return -Q

    def todim(self, w, theta=1.0):
        """TODIM — Gomes & Lima. Assimetria ganho/perda da Teoria dos Prospectos."""
        from metodos_br import _todim_kernel
        return _todim_de_dif(self.dif, w, float(theta), self.m)

    def sapevo(self, w):
        """SAPEVO-M adaptado a matriz cardinal (ver metodos_br.sapevo_m_de_matriz)."""
        return self.mat_sapevo @ w

    def topsis_fuzzy(self, w):
        """TOPSIS Fuzzy — Chen (2000), sobre a matriz já fuzzificada e normalizada."""
        V = self.r_fuzzy * w[None, :, None]
        d_pos = np.sqrt(((V - 1.0) ** 2).sum(axis=2) / 3.0).sum(axis=1)
        d_neg = np.sqrt((V ** 2).sum(axis=2) / 3.0).sum(axis=1)
        soma = d_pos + d_neg
        return d_neg / np.where(soma == 0, 1.0, soma)

    def pontuar(self, w):
        """Score de todos os métodos para um vetor de pesos. Maior = melhor."""
        w = _normalizar_pesos(w, self.k)
        return {
            "ELECTRE I":     self.electre(w),
            "ELECTRE II":    self.electre_ii(w),
            "PROMETHEE II":  self.promethee(w),
            "MAUT":          self.maut(w),
            "MCDA-C":        self.mcdac(w),
            "AHP-TOPSIS 2n": self.topsis_2n(w),
            "VIKOR":         self.vikor(w),
            "TODIM":         self.todim(w),
            "SAPEVO-M":      self.sapevo(w),
            "TOPSIS Fuzzy":  self.topsis_fuzzy(w),
        }


def _preferencia_vetorial(d, tipo, q, p, s):
    """Versão vetorizada das 6 funções de preferência (aplicada uma vez, na preparação)."""
    d = np.maximum(d, 0.0)
    if tipo == 0:
        return (d > 0).astype(np.float64)
    if tipo == 1:
        return (d > q).astype(np.float64)
    if tipo == 2:
        return np.clip(d / p, 0.0, 1.0)
    if tipo == 3:
        return np.where(d <= q, 0.0, np.where(d <= p, 0.5, 1.0))
    if tipo == 4:
        return np.where(d <= q, 0.0, np.where(d >= p, 1.0, (d - q) / (p - q)))
    if tipo == 5:
        return 1.0 - np.exp(-(d ** 2) / (2.0 * s ** 2))
    raise ValueError(f"código de preferência desconhecido: {tipo}")


@njit(cache=True, fastmath=True)
def _todim_de_dif_kernel(dif, wr, theta, m, k):
    """TODIM a partir do tensor de diferenças já orientado (evita reorientar)."""
    soma_w = wr.sum()
    total = np.zeros(m)
    for i in range(m):
        acc = 0.0
        for j in range(m):
            if i == j:
                continue
            for c in range(k):
                d = dif[c, i, j]
                if d > 0.0:
                    acc += np.sqrt(wr[c] * d / soma_w)
                elif d < 0.0:
                    acc += -(1.0 / theta) * np.sqrt(soma_w * (-d) / wr[c])
        total[i] = acc
    return total


def _todim_de_dif(dif, w, theta, m):
    wr = np.ascontiguousarray(w / w.max())
    soma = _todim_de_dif_kernel(dif, wr, theta, m, wr.size)
    lo, hi = soma.min(), soma.max()
    return np.full(m, 0.5) if hi <= lo else (soma - lo) / (hi - lo)


def preparar(X, direcoes, **kwargs) -> ProblemaPreparado:
    """Pré-compila o problema para reavaliação rápida sob muitos vetores de peso."""
    return ProblemaPreparado(X, direcoes, **kwargs)
