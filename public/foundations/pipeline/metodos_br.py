"""
Escola brasileira de Apoio Multicritério à Decisão (AMD) — SAPEVO-M, TODIM,
VIKOR, ELECTRE II e métodos ordinais.

═══════════════════════════════════════════════════════════════════════════════
 PROCEDÊNCIA — este módulo implementa métodos descritos nos trabalhos reunidos
 em  _private/foundations/kb/Artigos e Teses/Novos/.  A autoria dos MÉTODOS e
 das APLICAÇÕES é integralmente dos autores citados abaixo; deste projeto é
 apenas a implementação em Python/Rust e a integração ao motor de consenso.
═══════════════════════════════════════════════════════════════════════════════

SAPEVO-M — Simple Aggregation of Preferences Expressed by Ordinal Vectors,
            Multi Decision Makers
    Método original SAPEVO: GOMES, L. F. A. M. et al. (1997).
    Versão multidecisor e implementação computacional de referência:
      TEIXEIRA, Luiz Frederico Horácio de Souza de Barros; SANTOS, Marcos dos;
      GOMES, Carlos Francisco Simões. "Proposta e implementação em Python do
      método Simple Aggregation of Preferences Expressed by Ordinal Vectors –
      Multi Decision Makers: uma ferramenta web simples e intuitiva para Apoio à
      Decisão Multicritério". In: SIMPÓSIO DE PESQUISA OPERACIONAL E LOGÍSTICA
      DA MARINHA (SPOLM), 19., 2019, Rio de Janeiro. Anais. Rio de Janeiro:
      Centro de Análises de Sistemas Navais (CASNAV), 2019.   [arquivo 168.pdf]
    Aplicação em seleção de equipamentos:
      SANTOS, Marcos dos; OLIVEIRA, Nathália Campos de; OLIVEIRA, Pamela
      Ferreira Carvalho de; GOMES, Carlos Francisco Simões. "Aplicação do Método
      Multicritério SAPEVO-M na seleção de equipamentos: estudo de caso em uma
      panificadora do RJ". SPOLM, 19., 2019.                    [arquivo 053.pdf]
    Aplicação em seleção de lâmpada:
      ALVES, Camila Guimarães Monteiro de Freitas et al. "Seleção de uma lâmpada
      de filamento em uma empresa de iluminação decorativa: uma aplicação do
      método multicritério SAPEVO-M".                           [arquivo 186.pdf]

PROMETHEE-SAPEVO-M1 — modelagem híbrida
      MOREIRA, Miguel Ângelo Lellis; SANTOS, Marcos dos; GOMES, Carlos Francisco
      Simões. "Proposta de Modelagem Híbrida PROMETHEE-SAPEVO-M1: avaliação
      multicritério de drones para emprego na guerra naval". Instituto Militar de
      Engenharia (IME).                                         [arquivo 163.pdf]

TODIM — Tomada de Decisão Interativa Multicritério (Teoria dos Prospectos)
      Método: GOMES, L. F. A. M.; LIMA, M. M. P. P. (1992); GOMES (2004).
      Função de valor: KAHNEMAN, D.; TVERSKY, A. (1979).
      Extensão TODIM-FSE e aplicação militar conforme:
      SILVA, Cleidinei Augusto da; RANGEL, Luís Alberto Duncan; NEVES, Tiago
      Araújo. "Utilização do método multicritério TODIM-FSE para classificação de
      base logística de brigada". Academia Militar das Agulhas Negras (AMAN) /
      EEIMVR-UFF.                                            [arquivo 126482.pdf]

VIKOR — ViseKriterijumska Optimizacija i Kompromisno Resenje
      Método: OPRICOVIC, S. (1979); DUCKSTEIN; OPRICOVIC (1980);
              OPRICOVIC; TZENG (2002; 2004; 2007).
      Aplicação e formulação seguida aqui:
      KEUNECKE, Leandro; HEIN, Nelson; KROENKE, Adriana. "Avaliação de insumos
      têxteis – uma análise multicritério por meio do método VIKOR". FURB.
                                                             [arquivo 140621.pdf]

ELECTRE II e MÉTODOS ORDINAIS (Borda, Copeland)
      GOMES JÚNIOR, Silvio Figueiredo. "Método multicritério ELECTRE II na
      avaliação de pilotos no campeonato de Fórmula 1". SPOLM 2008,
      ISSN 2175-6295, Universidade Federal Fluminense.        [arquivo 016_0.pdf]
      GOMES JÚNIOR, Silvio Figueiredo. "Análise dos resultados dos desfiles de
      carnaval do Rio de Janeiro com emprego dos métodos ordinais multicritério".
      SPOLM 2008, Faculdade Redentor.                       [arquivo 053_1.pdf]

TOPSIS (aplicação ambiental de referência)
      DEGENHART, Larissa; ROSA, Fabricia Silva da et al. "Ranking de evidenciação
      dos impactos ambientais das empresas brasileiras listadas no IBrX-100 da
      BM&FBOVESPA – uma análise usando o método multicritério TOPSIS". FURB/UFSC.
                                                             [arquivo 139769.pdf]

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import numpy as np

from config import USAR_NUMBA
from nucleo import _normalizar_pesos, njit, orientar, ranks

# ---------------------------------------------------------------------------
# SAPEVO-M — Gomes et al. (1997); Teixeira, Santos & Gomes (SPOLM, 2019).
# ---------------------------------------------------------------------------
# Escala ordinal de SETE pontos (Tabela 1 de Teixeira, Santos & Gomes, 2019):
#   -3  <<<   absolutamente menos importante
#   -2  <<    muito menos importante
#   -1  <     menos importante
#    0  =     tão importante quanto
#   +1  >     mais importante
#   +2  >>    muito mais importante
#   +3  >>>   absolutamente mais importante
ESCALA_SAPEVO = (-3, -2, -1, 0, 1, 2, 3)

# Substituto do peso nulo após a normalização: 1% do valor imediatamente
# superior. Está no método, não é escolha nossa — "não faz sentido que um
# determinado critério possua peso nulo" (Teixeira, Santos & Gomes, 2019).
FRACAO_PESO_MINIMO = 0.01


def _vetor_sapevo(M):
    """Matriz de comparações ordinais -> vetor de preferências (soma das linhas).

    M[i, j] ∈ {-3..3} é o julgamento "i comparado a j" de UM decisor.
    Vᵢ = Σⱼ M[i, j]: quanto a opção i acumula de preferência sobre as demais.
    """
    M = np.asarray(M, dtype=np.float64)
    if M.ndim != 2 or M.shape[0] != M.shape[1]:
        raise ValueError(f"SAPEVO-M exige matriz quadrada, recebida {M.shape}")
    return M.sum(axis=1)


def _normalizar_sapevo(v):
    """Normalização min-max do método, com o tratamento do peso nulo.

    ʋ = (aᵢ − min a) / (max a − min a), seguido da substituição do zero por 1%
    do menor valor positivo — exatamente como especificado por Teixeira, Santos
    & Gomes (2019). Sem essa substituição, um critério que o decisor apenas
    julgou "o menos importante" seria ELIMINADO do modelo (peso zero anula a
    coluna inteira), e não foi isso que ele disse.
    """
    v = np.asarray(v, dtype=np.float64)
    lo, hi = v.min(), v.max()
    vn = np.full_like(v, 0.5) if hi <= lo else (v - lo) / (hi - lo)
    positivos = vn[vn > 0]
    if positivos.size:
        vn[vn <= 0] = positivos.min() * FRACAO_PESO_MINIMO
    else:
        vn[:] = 1.0 / vn.size
    return vn


def sapevo_m_pesos(matrizes_decisores):
    """Pesos dos critérios a partir dos julgamentos ordinais de VÁRIOS decisores.

    matrizes_decisores: iterável de matrizes (n_criterios × n_criterios) na escala
    de sete pontos, uma por decisor.

    A agregação multidecisor é o que distingue o SAPEVO-M do SAPEVO original:
    somam-se os vetores de preferência dos decisores ANTES de normalizar, de modo
    que nenhum decisor precisa concordar previamente com os demais sobre a ordem
    dos critérios — não há exigência de pré-ordem de consenso.
    """
    matrizes = [np.asarray(M, dtype=np.float64) for M in matrizes_decisores]
    if not matrizes:
        raise ValueError("SAPEVO-M: nenhum decisor informado")
    n = matrizes[0].shape[0]
    if any(M.shape != (n, n) for M in matrizes):
        raise ValueError("SAPEVO-M: todos os decisores devem julgar os mesmos critérios")
    v_total = np.sum([_vetor_sapevo(M) for M in matrizes], axis=0)
    pesos = _normalizar_sapevo(v_total)
    return pesos / pesos.sum()


def sapevo_m(matrizes_criterios, matrizes_alternativas):
    """SAPEVO-M completo: devolve (score, pesos).

    matrizes_criterios:   lista (por decisor) de matrizes n_crit × n_crit.
    matrizes_alternativas: dict {índice_do_critério: lista (por decisor) de
                           matrizes n_alt × n_alt}, comparando alternativas
                           À LUZ daquele critério.

    Resultado = V (pesos dos critérios) · M (matriz de avaliação das
    alternativas), ordenado em ordem decrescente — Teixeira, Santos & Gomes (2019).
    """
    pesos = sapevo_m_pesos(matrizes_criterios)
    n_crit = pesos.size
    n_alt = np.asarray(next(iter(matrizes_alternativas.values()))[0]).shape[0]

    M = np.zeros((n_alt, n_crit))
    for j in range(n_crit):
        if j not in matrizes_alternativas:
            raise ValueError(f"SAPEVO-M: faltam julgamentos de alternativas no critério {j}")
        v = np.sum([_vetor_sapevo(Mk) for Mk in matrizes_alternativas[j]], axis=0)
        M[:, j] = _normalizar_sapevo(v)
    return M @ pesos, pesos


def sapevo_m_de_matriz(X, direcoes, pesos=None):
    """Adaptação do SAPEVO-M a uma matriz de decisão CARDINAL já existente.

    O SAPEVO-M nasceu para julgamentos ORDINAIS (o decisor diz "A é muito melhor
    que B"), mas o motor deste projeto parte de matrizes cardinais (autonomia em
    km, preço em reais). A ponte: derivamos as comparações par a par do sinal e da
    magnitude relativa dos desempenhos observados, discretizando na escala de sete
    pontos do método.

    ⚠️  Isto é uma ADAPTAÇÃO deste projeto, não o método como publicado. Quando
    houver julgamento ordinal real de decisores, use `sapevo_m` — é a forma fiel.
    """
    G = orientar(X, direcoes)                       # [0,1], maior = melhor
    n_alt, n_crit = G.shape
    M = np.zeros((n_alt, n_crit))
    for j in range(n_crit):
        d = G[:, j][:, None] - G[:, j][None, :]     # diferença par a par
        # Discretiza em {-3..3}: limiares em 1/6, 3/6, 5/6 da amplitude [-1,1].
        graus = np.clip(np.round(d * 3.0), -3, 3)
        np.fill_diagonal(graus, 0.0)
        M[:, j] = _normalizar_sapevo(graus.sum(axis=1))
    if pesos is None:
        pesos = np.full(n_crit, 1.0 / n_crit)
    return M @ _normalizar_pesos(pesos, n_crit)


# ---------------------------------------------------------------------------
# VIKOR — Opricovic (1979); Opricovic & Tzeng (2002, 2004, 2007).
# Formulação conforme Keunecke, Hein & Kroenke (FURB) [140621.pdf].
# ---------------------------------------------------------------------------
def vikor(X, w, direcoes, v=0.5):
    """Solução de compromisso VIKOR. Devolve (score, S, R, Q, diagnostico).

    Passo 1 — melhor e pior valor de cada critério: f*ᵢ e f⁻ᵢ.
    Passo 2 — S (utilidade do GRUPO, soma ponderada) e R (arrependimento
              INDIVIDUAL máximo, minimax):
                  Sⱼ = Σᵢ wᵢ (f*ᵢ − fᵢⱼ) / (f*ᵢ − f⁻ᵢ)
                  Rⱼ = maxᵢ [ wᵢ (f*ᵢ − fᵢⱼ) / (f*ᵢ − f⁻ᵢ) ]
    Passo 3 — índice de compromisso, com v = peso de estratégia (padrão 0,5):
                  Qⱼ = v(Sⱼ−S*)/(S⁻−S*) + (1−v)(Rⱼ−R*)/(R⁻−R*)
              MENOR Q é melhor. Devolvemos `score = −Q` para manter a convenção
              do motor (maior = melhor) e permitir o consenso de Borda.
    Passo 4 — as duas condições de aceitação da solução de compromisso:
              C1 (vantagem aceitável):    Q(a²) − Q(a¹) ≥ 1/(m−1)
              C2 (estabilidade aceitável): a¹ também é o melhor em S ou em R.

    A distinção entre S e R é o que o VIKOR traz e a soma ponderada não tem: S
    aceita que um desempenho péssimo seja compensado por vários bons; R recusa.
    Quando os dois discordam, a decisão tem um ponto cego — e C1/C2 dizem isso.
    """
    G = orientar(X, direcoes)                       # f* = 1 e f⁻ = 0 por construção
    m, k = G.shape
    w = _normalizar_pesos(w, k)

    penalidade = w * (1.0 - G)                      # wᵢ(f*ᵢ − fᵢⱼ)/(f*ᵢ − f⁻ᵢ)
    S = penalidade.sum(axis=1)
    R = penalidade.max(axis=1)

    S_min, S_max = S.min(), S.max()
    R_min, R_max = R.min(), R.max()
    ds = (S_max - S_min) or 1.0
    dr = (R_max - R_min) or 1.0
    Q = v * (S - S_min) / ds + (1.0 - v) * (R - R_min) / dr

    ordem = np.argsort(Q)                           # menor Q primeiro
    melhor, segundo = ordem[0], (ordem[1] if m > 1 else ordem[0])
    dq = 1.0 / (m - 1) if m > 1 else 0.0
    c1 = bool(Q[segundo] - Q[melhor] >= dq)         # vantagem aceitável
    c2 = bool(melhor == int(np.argmin(S)) or melhor == int(np.argmin(R)))

    if c1 and c2:
        conjunto, situacao = [int(melhor)], "compromisso único"
    elif not c2:
        # Sem estabilidade: a¹ e a² são um conjunto de compromisso.
        conjunto, situacao = [int(melhor), int(segundo)], "compromisso instável (C2 falha)"
    else:
        # Sem vantagem: todas as alternativas dentro da folga dq empatam.
        conjunto = [int(i) for i in ordem if Q[i] - Q[melhor] < dq]
        situacao = "vantagem insuficiente (C1 falha)"

    diagnostico = {"c1_vantagem_aceitavel": c1, "c2_estabilidade_aceitavel": c2,
                   "dq": float(dq), "conjunto_compromisso": conjunto,
                   "situacao": situacao, "v": float(v)}
    return -Q, S, R, Q, diagnostico


# ---------------------------------------------------------------------------
# TODIM — Gomes & Lima (1992); Gomes (2004). Teoria dos Prospectos de
# Kahneman & Tversky (1979). Conforme Silva, Rangel & Neves [126482.pdf].
# ---------------------------------------------------------------------------
@njit(cache=True, fastmath=True)
def _todim_kernel(G, wr, theta):
    """Matriz de dominância δ(i,j) = Σ_c Φ_c(i,j).

    Φ_c(i,j) =  √( w_rc · d / Σw_rc )                se d > 0  (GANHO)
                0                                     se d = 0
               −(1/θ)·√( (Σw_rc) · (−d) / w_rc )      se d < 0  (PERDA)

    onde d = P_ic − P_jc e w_rc = w_c / w_r é a taxa de substituição em relação ao
    critério de referência r (o de maior peso). θ é o fator de atenuação de perdas:
    θ pequeno amplifica a aversão à perda, reproduzindo a assimetria da função de
    valor da Teoria dos Prospectos — a perda dói mais do que o ganho equivalente
    agrada. É exatamente essa assimetria que a soma ponderada clássica ignora.
    """
    m, k = G.shape
    soma_w = wr.sum()
    delta = np.zeros((m, m))
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
            total = 0.0
            for c in range(k):
                d = G[i, c] - G[j, c]
                if d > 0.0:
                    total += np.sqrt(wr[c] * d / soma_w)
                elif d < 0.0:
                    total += -(1.0 / theta) * np.sqrt(soma_w * (-d) / wr[c])
            delta[i, j] = total
    return delta


def todim(X, w, direcoes, theta=1.0):
    """Devolve (score ξ ∈ [0,1], matriz de dominância δ).

    ξᵢ = (Σⱼδ(i,j) − min) / (max − min): por construção a melhor alternativa vale
    exatamente 1 e a pior exatamente 0 — Gomes (2004), Eq. (5).

    theta (θ) é o fator de atenuação de perdas:
      θ = 1   aversão à perda padrão da formulação;
      θ < 1   amplifica a perda (decisor mais conservador);
      θ > 1   atenua a perda (decisor mais tolerante ao risco).
    """
    G = orientar(X, direcoes)
    m, k = G.shape
    w = _normalizar_pesos(w, k)
    if theta <= 0:
        raise ValueError("TODIM: o fator de atenuação θ deve ser positivo")

    wr = w / w.max()                                # taxa de substituição w_c / w_r
    delta = _todim_kernel(np.ascontiguousarray(G), np.ascontiguousarray(wr), float(theta))

    soma = delta.sum(axis=1)
    lo, hi = soma.min(), soma.max()
    xi = np.full(m, 0.5) if hi <= lo else (soma - lo) / (hi - lo)
    return xi, delta


# ---------------------------------------------------------------------------
# ELECTRE II — Roy & Bertier (1971).
# Conforme Gomes Júnior, SPOLM 2008 [016_0.pdf].
# ---------------------------------------------------------------------------
@njit(cache=True, fastmath=True)
def _concordancia_discordancia(G, w):
    """Índices C(a,b) e D(a,b) par a par. G orientado, w normalizado."""
    m, k = G.shape
    C = np.zeros((m, m))
    D = np.zeros((m, m))
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
            C[a, b] = conc
            D[a, b] = disc
    return C, D


def _destilar_relacao(relacao, m, descendente):
    """Destilação do ELECTRE II: extrai níveis sucessivos da relação.

    descendente=True retira quem não é sobreclassificado por ninguém (os melhores
    saem primeiro); False retira quem não sobreclassifica ninguém (os piores).
    Um ciclo de preferência (ninguém livre) corta o nível inteiro de uma vez —
    é o tratamento clássico, e o alternativo seria travar em laço infinito.
    """
    posicao = np.zeros(m, dtype=np.int64)
    restantes = list(range(m))
    nivel = 1
    while restantes:
        sub = relacao[np.ix_(restantes, restantes)]
        livres = [restantes[i] for i in range(len(restantes))
                  if (not sub[:, i].any() if descendente else not sub[i, :].any())]
        if not livres:
            livres = list(restantes)
        for i in livres:
            posicao[i] = nivel
        restantes = [i for i in restantes if i not in livres]
        nivel += 1
    return posicao


def electre_ii(X, w, direcoes, c_forte=0.75, c_fraca=0.60,
               d_forte=0.25, d_fraca=0.40):
    """ELECTRE II — sobreclassificação FORTE e FRACA, com destilação.

    Diferença essencial para o ELECTRE I: o I devolve um núcleo (quem não é
    dominado), o II devolve uma ORDENAÇÃO COMPLETA. Para isso usa dois pares de
    limiares — um exigente e um tolerante — e produz duas relações:

        forte: C(a,b) ≥ c_forte  e  D(a,b) ≤ d_forte
        fraca: C(a,b) ≥ c_fraca  e  D(a,b) ≤ d_fraca

    A ordenação sai de duas DESTILAÇÕES:
      • descendente: retira iterativamente quem não é fortemente sobreclassificado
        por ninguém (os melhores saem primeiro);
      • ascendente:  retira quem não sobreclassifica ninguém (os piores saem primeiro).
    A posição final é a média das duas — o procedimento clássico que evita o viés
    de olhar o problema por uma ponta só.

    Devolve (score, rank_descendente, rank_ascendente, forte, fraca).
    """
    if not (c_fraca <= c_forte and d_forte <= d_fraca):
        raise ValueError("ELECTRE II: exige c_fraca ≤ c_forte e d_forte ≤ d_fraca")
    G = orientar(X, direcoes)
    m, k = G.shape
    w = _normalizar_pesos(w, k)
    C, D = _concordancia_discordancia(np.ascontiguousarray(G), np.ascontiguousarray(w))

    forte = (C >= c_forte) & (D <= d_forte)
    fraca = (C >= c_fraca) & (D <= d_fraca)
    np.fill_diagonal(forte, False)
    np.fill_diagonal(fraca, False)

    desc = _destilar_relacao(forte, m, True)
    asc = _destilar_relacao(fraca, m, False)
    # asc conta do pior para o melhor: inverte para virar posição "1 = melhor".
    asc_invertida = asc.max() + 1 - asc
    media = (desc + asc_invertida) / 2.0
    return -media, desc, asc_invertida, forte, fraca


# ---------------------------------------------------------------------------
# MÉTODOS ORDINAIS — Borda (1781) e Copeland (1951).
# Conforme Gomes Júnior, SPOLM 2008 [053_1.pdf].
# ---------------------------------------------------------------------------
def borda_ordinal(matriz_ranks):
    """Contagem de Borda: pontos = (n − posição), somados sobre os julgadores."""
    M = np.asarray(matriz_ranks, dtype=np.float64)
    n = M.shape[1]
    return (n - M).sum(axis=0)


def copeland(matriz_ranks):
    """Copeland: vitórias menos derrotas em confrontos DIRETOS, dois a dois.

    Diferença para Borda: Borda soma posições e por isso é sensível a quão longe
    ficou o adversário; Copeland só olha quem ganhou de quem. Quando os dois
    discordam, existe um ciclo de maioria (paradoxo de Condorcet) escondido nos
    dados — e essa discordância é o achado, não um defeito do cálculo.
    """
    M = np.asarray(matriz_ranks, dtype=np.int64)   # (n_julgadores, n_alternativas)
    n = M.shape[1]
    score = np.zeros(n)
    for a in range(n):
        for b in range(n):
            if a == b:
                continue
            vitorias = int((M[:, a] < M[:, b]).sum())     # posição menor = melhor
            derrotas = int((M[:, a] > M[:, b]).sum())
            if vitorias > derrotas:
                score[a] += 1
            elif vitorias < derrotas:
                score[a] -= 1
    return score


# ---------------------------------------------------------------------------
# PROMETHEE-SAPEVO-M1 — modelagem híbrida.
# Moreira, Santos & Gomes (IME) [163.pdf].
# ---------------------------------------------------------------------------
def promethee_sapevo_m1(X, direcoes, matrizes_criterios, tipo="linear"):
    """Híbrido: pesos ordinais do SAPEVO-M alimentando o fluxo do PROMETHEE.

    A ideia da modelagem híbrida de Moreira, Santos & Gomes é usar cada método
    onde ele é forte: o SAPEVO-M elicita os pesos a partir de julgamento ORDINAL
    de múltiplos decisores (que é como um comitê realmente se expressa — "a
    autonomia importa mais que o preço", não "a autonomia vale 0,237"), e o
    PROMETHEE II ranqueia as alternativas com esses pesos, aproveitando suas
    funções de preferência e os limiares de indiferença.

    Devolve (fluxo_liquido_phi, pesos_sapevo).
    """
    from nucleo import promethee_ii
    pesos = sapevo_m_pesos(matrizes_criterios)
    if pesos.size != X.shape[1]:
        raise ValueError(
            f"PROMETHEE-SAPEVO-M1: {pesos.size} critérios julgados, "
            f"{X.shape[1]} colunas na matriz de decisão")
    return promethee_ii(X, pesos, direcoes, tipo=tipo), pesos


METODOS_BR = ("SAPEVO-M", "VIKOR", "TODIM", "ELECTRE II", "Copeland")


if __name__ == "__main__":
    print("Escola brasileira de AMD — métodos implementados:")
    for m in METODOS_BR:
        print(f"  • {m}")
    print("\nProcedência: _private/foundations/kb/Artigos e Teses/Novos/")
    print("Autoria dos métodos e aplicações: ver cabeçalho deste arquivo.")
