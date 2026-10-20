"""
Extensões fuzzy: AHP Fuzzy (Buckley) e TOPSIS Fuzzy (Chen).

═══════════════════════════════════════════════════════════════════════════════
 POR QUE FUZZY — e o que ele NÃO resolve
═══════════════════════════════════════════════════════════════════════════════
O AHP clássico exige que o decisor diga "o critério A é exatamente 5 vezes mais
importante que B". Ninguém sabe isso. O que o decisor sabe é "A é bem mais
importante que B" — uma faixa, não um ponto. A extensão fuzzy carrega essa faixa
pelo cálculo inteiro, em vez de descartá-la na primeira linha.

O que fuzzy NÃO faz: inventar informação. Um número fuzzy construído a partir de
um crisp tem exatamente a informação do crisp mais uma hipótese de espalhamento
declarada. Por isso, aqui, **o espalhamento é sempre explícito e auditável**.

⚠️  CUIDADO COM UMA EQUIVALÊNCIA QUE NÃO EXISTE. `alpha=0` NÃO reduz o TOPSIS
Fuzzy ao `topsis()` deste projeto. Com alpha=0 o TFN degenera, sim, mas sobram
as outras DUAS escolhas de Chen, que são independentes da fuzzificação:

    | escolha        | `topsis()` (Hwang & Yoon)     | `fuzzy_topsis()` (Chen)   |
    |----------------|-------------------------------|---------------------------|
    | normalização   | vetorial (÷ norma euclidiana) | linear (÷ max da coluna)  |
    | solução ideal  | RELATIVA (max/min da matriz)  | ABSOLUTA ((1,1,1)/(0,0,0))|

Medido numa matriz 4×3: Δ máximo de 0,59 no CC e **inversão do 1º com o 2º lugar**.
O que `alpha=0` reproduz, com Δ = 0, é um TOPSIS de normalização linear e ideais
absolutos — ambos verificados em `testes_nucleo.py`. A divergência entre os dois
TOPSIS é metodológica e informativa; tratá-la como erro levaria a "consertar" o
que está certo. Ver bugs.md #BUG-040.

`fuzzy_ahp_pesos` com `delta=0`, esse sim, reproduz `pesos_ahp` (Δ ~ 1e-16): a
média geométrica de Buckley degenera exatamente no autovetor de uma matriz
consistente.

REFERÊNCIAS
    ZADEH, L. A. "Fuzzy sets". Information and Control, 8(3):338-353, 1965.
    VAN LAARHOVEN, P.; PEDRYCZ, W. "A fuzzy extension of Saaty's priority
        theory". Fuzzy Sets and Systems, 11(1-3):229-241, 1983.
    BUCKLEY, J. J. "Fuzzy hierarchical analysis". Fuzzy Sets and Systems,
        17(3):233-247, 1985.  ← método de pesos usado aqui
    CHEN, C.-T. "Extensions of the TOPSIS for group decision-making under fuzzy
        environment". Fuzzy Sets and Systems, 114(1):1-9, 2000.  ← TOPSIS fuzzy
    CHANG, D.-Y. "Applications of the extent analysis method on fuzzy AHP".
        European Journal of Operational Research, 95(3):649-655, 1996.
        (NÃO usado — ver a nota em `fuzzy_ahp_pesos`.)

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import numpy as np

from config import FUZZY_ALPHA, FUZZY_FATOR_SAATY

# Número triangular fuzzy (TFN): (l, m, u) com l ≤ m ≤ u.
# Guardamos sempre como array (..., 3) na última dimensão — assim toda a álgebra
# é vetorizada e o NumPy cuida do broadcast.
L, M, U = 0, 1, 2


# ---------------------------------------------------------------------------
# Construção e validação
# ---------------------------------------------------------------------------
def validar_tfn(T, nome="TFN"):
    """Confere l ≤ m ≤ u. Um TFN invertido produz distância negativa e um ranking
    que PARECE certo — por isso a checagem é dura e vem antes de qualquer conta."""
    T = np.asarray(T, dtype=np.float64)
    if T.shape[-1] != 3:
        raise ValueError(f"{nome}: última dimensão deve ser 3 (l, m, u), recebida {T.shape}")
    if not np.isfinite(T).all():
        raise ValueError(f"{nome}: contém NaN ou infinito")
    ruins = (T[..., L] > T[..., M] + 1e-12) | (T[..., M] > T[..., U] + 1e-12)
    if ruins.any():
        i = np.argwhere(ruins)[0]
        raise ValueError(f"{nome}: exige l ≤ m ≤ u; violado em {tuple(i)} = {T[tuple(i)]}")
    return T


def fuzzificar_matriz(X, alpha=FUZZY_ALPHA):
    """Matriz de decisão crisp → TFN com banda PROPORCIONAL de ±alpha.

        x  →  (x·(1−α),  x,  x·(1+α))

    A banda é proporcional, não absoluta, porque a incerteza de um preço de R$ 2.500
    não é a mesma de uma nota 0-10. Um α absoluto trataria as duas igual e daria peso
    desproporcional ao critério de menor escala.

    ⚠️  ESTA É UMA HIPÓTESE DECLARADA, não um dado. As matrizes deste projeto são
    crisp; a banda representa incerteza de medição de ±α e está registrada no
    relatório de cada caso. Com α=0 o TFN degenera no crisp e o TOPSIS Fuzzy
    reproduz o TOPSIS clássico — propriedade verificada em `testes_nucleo.py`.

    Para valores NEGATIVOS, (1−α)·x > (1+α)·x, e os extremos trocam de lado; por
    isso ordenamos no fim. Sem isso, um VPL negativo geraria TFN invertido.
    """
    X = np.asarray(X, dtype=np.float64)
    a = float(alpha)
    if a < 0:
        raise ValueError(f"alpha deve ser ≥ 0, recebido {a}")
    tri = np.stack([X * (1.0 - a), X, X * (1.0 + a)], axis=-1)
    tri.sort(axis=-1)                       # garante l ≤ m ≤ u também em negativos
    return tri


def fuzzificar_saaty(A, fator=FUZZY_FATOR_SAATY):
    """Matriz de razões crisp → julgamentos TFN, com espalhamento GEOMÉTRICO.

        a_ij  →  (a_ij / g,  a_ij,  a_ij · g)        g = fator ≥ 1
        a_ji  →  (1/u_ij,    1/m_ij, 1/l_ij)         recíproco EXATO

    POR QUE GEOMÉTRICO E NÃO ABSOLUTO. A literatura clássica (van Laarhoven &
    Pedrycz) fuzzifica com δ aditivo — "5" vira (4, 5, 6) — porque pressupõe a
    escala de Saaty, limitada a [1/9, 9]. As matrizes deste projeto NÃO estão
    nessa escala: `casos.catalogo._saaty` gera razões por progressão geométrica,
    e com 9 critérios a_ij chega a 2⁸ = 256. Em 35 dos 38 casos há razão fora de
    [1/9, 9].

    O espalhamento aditivo com recorte, que foi a primeira versão disto, produzia
    um defeito grave e silencioso: para a = 128, l = clip(127) = 9 e u = clip(129)
    = 9, e a ordenação devolvia o TFN (9, 9, 128) — **o valor modal deixava de ser
    128 e virava 9**. O julgamento do decisor era substituído por outro, sem aviso,
    e o peso resultante era o de um critério muito menos importante. Ver bugs.md
    #BUG-043.

    O espalhamento geométrico não tem esse problema: é invariante de escala (a
    amplitude relativa é g − 1/g para qualquer a), preserva o modal por construção
    e mantém a reciprocidade exata. `fator = 1` devolve o TFN degenerado (a, a, a)
    e reduz o AHP Fuzzy ao AHP crisp — propriedade verificada em `testes_nucleo.py`.

    Interpretação de `fator = 1.5`: "quando o decisor disse que A vale 5 vezes B,
    ele quis dizer algo entre 3,3 e 7,5 vezes".

    ⚠️  CONSEQUÊNCIA QUE PRECISA SER DITA: com `fator` ESCALAR (o mesmo espalhamento
    em todos os julgamentos), o peso central do AHP Fuzzy é **idêntico ao do AHP** e
    **invariante em g**. Não é defeito — é álgebra:

        l_i = (∏_j a_ij/g)^(1/n) = m_i/g   ⟹   w̃_i ∝ (m_i/g², m_i, m_i·g²)
        centroide normalizado = m_i / Σm   (o fator se cancela)

    Verificado para g ∈ {1; 1,2; 1,5; 3} e também em matriz inconsistente (CR=1,15).

    Ou seja: com espalhamento uniforme, o fuzzy NÃO acrescenta informação ao valor
    central — acrescenta a FAIXA (l, u), que responde outra pergunta: a ordem dos
    pesos sobrevive à imprecisão declarada? Vender o centroide como "terceira fonte
    de peso" seria vender um número que já se tinha.

    O centroide só se desloca quando o espalhamento VARIA entre julgamentos — que é
    o caso real: o decisor tem mais certeza sobre uns pares que sobre outros. Para
    isso, passe `fator` como MATRIZ n×n (g_ij ≥ 1, simétrica em significado), e o
    AHP Fuzzy passa a ser uma fonte de peso genuinamente distinta.
    """
    A = np.asarray(A, dtype=np.float64)
    n = A.shape[0]
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError(f"matriz de Saaty deve ser quadrada, recebida {A.shape}")
    if (A <= 0).any():
        raise ValueError("matriz de Saaty não pode ter zero ou negativo")

    G = np.asarray(fator, dtype=np.float64)
    if G.ndim == 0:
        G = np.full((n, n), float(G))
    elif G.shape != (n, n):
        raise ValueError(f"fator como matriz deve ser ({n}, {n}), recebida {G.shape}")
    if (G < 1.0).any():
        raise ValueError("todo fator deve ser ≥ 1 (1 = sem espalhamento naquele julgamento)")

    F = np.empty((n, n, 3))
    for i in range(n):
        F[i, i] = (1.0, 1.0, 1.0)
        for j in range(i + 1, n):
            m, g = float(A[i, j]), float(G[i, j])
            F[i, j] = (m / g, m, m * g)
            F[j, i] = (1.0 / (m * g), 1.0 / m, g / m)      # recíproco exato
    return validar_tfn(F, "matriz de Saaty fuzzy")


# ---------------------------------------------------------------------------
# AHP Fuzzy — Buckley (1985)
# ---------------------------------------------------------------------------
def fuzzy_ahp_pesos(A_fuzzy, desfuzzificar=True):
    """Pesos por média geométrica fuzzy (Buckley, 1985).

        r̃ᵢ = (∏ⱼ ãᵢⱼ)^(1/n)                 média geométrica da linha i
        w̃ᵢ = r̃ᵢ ⊗ (r̃₁ ⊕ … ⊕ r̃ₙ)⁻¹          normalização fuzzy
        wᵢ  = (l + m + u)/3                   centroide, se desfuzzificar

    Devolve `(w_crisp, W_fuzzy)`; com `desfuzzificar=False`, só `W_fuzzy`.

    POR QUE BUCKLEY E NÃO CHANG (extent analysis). O método de Chang (1996) é o
    mais citado, e tem um defeito conhecido e grave: o grau de possibilidade pode
    atribuir **peso ZERO** a um critério que o decisor julgou relevante — o critério
    simplesmente desaparece do modelo, sem aviso. Num sistema de apoio à decisão
    isso é inaceitável: some informação que o decisor forneceu. A média geométrica
    de Buckley sempre devolve peso positivo e preserva a ordem dos julgamentos.
    (A crítica está em Wang, Luo & Hua, EJOR 186(2):735-747, 2008.)

    A normalização usa o inverso do TFN da soma: (l,m,u)⁻¹ = (1/u, 1/m, 1/l) — por
    isso o l de w̃ᵢ divide pelo u da soma, e não pelo l. Trocar isso dá pesos
    plausíveis e errados, com o espalhamento invertido.
    """
    F = validar_tfn(A_fuzzy, "A_fuzzy")
    n = F.shape[0]
    if F.shape[:2] != (n, n):
        raise ValueError(f"A_fuzzy deve ser (n, n, 3), recebida {F.shape}")
    if (F <= 0).any():
        raise ValueError("julgamentos fuzzy devem ser estritamente positivos")

    # Média geométrica por linha, em log para não estourar com n grande.
    r = np.exp(np.log(F).mean(axis=1))                   # (n, 3)
    soma = r.sum(axis=0)                                 # (3,) = (Σl, Σm, Σu)
    inv_soma = np.array([1.0 / soma[U], 1.0 / soma[M], 1.0 / soma[L]])
    W = r * inv_soma                                     # (n, 3)
    W = validar_tfn(W, "pesos fuzzy")
    if not desfuzzificar:
        return W
    w = W.mean(axis=1)                                   # centroide (l+m+u)/3
    s = w.sum()
    if s <= 0:
        raise ValueError("pesos fuzzy somaram zero após desfuzzificação")
    return w / s, W


def indice_fuzziness(W):
    """Quanto o espalhamento dos pesos pesa, em relação ao valor central.

        Φ = Σᵢ (uᵢ − lᵢ) / Σᵢ mᵢ

    É o número que diz se valeu a pena rodar fuzzy: Φ próximo de 0 significa que o
    julgamento é praticamente crisp e os dois AHP vão concordar. Φ alto significa
    que a ordem dos pesos é sensível à imprecisão declarada — e aí a divergência
    entre AHP e AHP Fuzzy é o achado, não o ruído.
    """
    W = validar_tfn(W, "pesos fuzzy")
    den = W[..., M].sum()
    return float((W[..., U] - W[..., L]).sum() / den) if den else 0.0


# ---------------------------------------------------------------------------
# TOPSIS Fuzzy — Chen (2000)
# ---------------------------------------------------------------------------
def normalizar_fuzzy_chen(X_fuzzy, direcoes):
    """Passo 1 do TOPSIS Fuzzy, isolado por NÃO depender dos pesos.

        benefício: r̃ᵢⱼ = (lᵢⱼ/u⁺ⱼ, mᵢⱼ/u⁺ⱼ, uᵢⱼ/u⁺ⱼ)      u⁺ⱼ = max uᵢⱼ
        custo:     r̃ᵢⱼ = (l⁻ⱼ/uᵢⱼ, l⁻ⱼ/mᵢⱼ, l⁻ⱼ/lᵢⱼ)      l⁻ⱼ = min lᵢⱼ

    No custo os extremos TROCAM de lado — o maior u vira o menor l —, por isso o l
    do resultado divide pelo u da entrada. Normalizar componente a componente sem a
    troca produz um TFN invertido (l > u) que continua "parecendo" um TFN e envenena
    a distância vertex em silêncio. `validar_tfn` existe para pegar exatamente isso.

    Vive separada de `fuzzy_topsis` para que `ProblemaPreparado` a chame uma única
    vez e os 2.000 universos de robustez só refaçam a ponderação.
    """
    F = validar_tfn(X_fuzzy, "X_fuzzy").copy()
    k = F.shape[1]
    if len(direcoes) != k:
        raise ValueError(f"direções: esperadas {k}, recebidas {len(direcoes)}")

    # TRANSLAÇÃO DAS COLUNAS NÃO-POSITIVAS — e por que ela é inevitável aqui.
    #
    # A normalização de Chen é MULTIPLICATIVA (divide por max ou por cada valor) e
    # só é definida para dados estritamente positivos. Com l⁻ ≤ 0 num critério de
    # custo, l⁻/uᵢⱼ e l⁻/lᵢⱼ invertem a ordem dos vértices e produzem um TFN com
    # l > u — que `validar_tfn` rejeita, mas que antes dessa guarda envenenaria a
    # distância vertex em silêncio.
    #
    # Dados reais têm zero e negativo: VPL negativo, vacância 0%, assimetria
    # negativa — 13 colunas nos 38 casos deste projeto. A saída é deslocar a coluna
    # para o domínio positivo antes de formar as razões.
    #
    # ⚠️  O QUE A TRANSLAÇÃO CUSTA, declarado: ela preserva a ORDEM e as diferenças,
    # mas NÃO as razões — e Chen é um método de razões. Numa coluna transladada, o
    # resultado depende do deslocamento escolhido. Usamos o menor que serve: 1% da
    # amplitude da coluna acima de zero. Quem precisar de invariância exata de razão
    # deve reescalar o critério na modelagem, não aqui. Ver bugs.md #BUG-044.
    deslocamentos = np.zeros(k)
    for j in range(k):
        lo = F[:, j, L].min()
        if lo <= 0:
            amp = F[:, j, U].max() - lo
            eps = (amp * 0.01) if amp > 0 else 1.0
            deslocamentos[j] = -lo + eps
            F[:, j, :] += deslocamentos[j]

    R = np.empty_like(F)
    for j in range(k):
        col = F[:, j, :]
        if direcoes[j] == "benefit":
            upos = col[:, U].max()
            R[:, j, :] = col / (upos if upos != 0 else 1.0)
        elif direcoes[j] == "cost":
            lneg = col[:, L].min()
            denom = np.where(col == 0, np.inf, col)      # 1/0 → 0, nunca infinito
            R[:, j, L] = lneg / denom[:, U]
            R[:, j, M] = lneg / denom[:, M]
            R[:, j, U] = lneg / denom[:, L]
        else:
            raise ValueError(f"direção inválida em {j}: {direcoes[j]!r}")
    return validar_tfn(R, "matriz normalizada")


def colunas_transladadas(X_fuzzy, direcoes):
    """Índices das colunas que a normalização precisa deslocar (têm valor ≤ 0).

    Existe para o relatório poder DIZER quais critérios foram transladados: numa
    coluna deslocada, o TOPSIS Fuzzy deixa de ser invariante de razão, e isso tem
    de aparecer para quem lê o ranking.
    """
    F = validar_tfn(X_fuzzy, "X_fuzzy")
    return [j for j in range(F.shape[1]) if F[:, j, L].min() <= 0]


def fuzzy_topsis(X_fuzzy, w, direcoes, w_fuzzy=None):
    """TOPSIS Fuzzy de Chen (2000). Devolve a proximidade CCᵢ ∈ [0,1], maior = melhor.

    Passos, exatamente como no artigo:

    1. NORMALIZAÇÃO LINEAR, preservando o triângulo e o intervalo [0,1]:
         benefício: r̃ᵢⱼ = (lᵢⱼ/u⁺ⱼ, mᵢⱼ/u⁺ⱼ, uᵢⱼ/u⁺ⱼ)      com u⁺ⱼ = max uᵢⱼ
         custo:     r̃ᵢⱼ = (l⁻ⱼ/uᵢⱼ, l⁻ⱼ/mᵢⱼ, l⁻ⱼ/lᵢⱼ)      com l⁻ⱼ = min lᵢⱼ
       No custo os extremos TROCAM de lado (o maior u vira o menor l), e é por isso
       que a divisão usa u no numerador do l. Fazer componente a componente sem a
       troca gera TFN invertido — erro que passa despercebido porque o número
       continua "parecendo" um TFN.
    2. PONDERAÇÃO: ṽᵢⱼ = r̃ᵢⱼ ⊗ w̃ⱼ.
    3. IDEAIS: FPIS = (1,1,1) e FNIS = (0,0,0) por critério — válidos porque o passo
       1 já pôs tudo em [0,1] com o sentido unificado.
    4. DISTÂNCIA VERTEX entre TFNs:
         d(ã,b̃) = √[ ((l_a−l_b)² + (m_a−m_b)² + (u_a−u_b)²) / 3 ]
    5. CC ᵢ = dᵢ⁻ / (dᵢ⁺ + dᵢ⁻).

    `w_fuzzy` (n_crit × 3) usa pesos fuzzy de verdade — é o encaixe natural com o
    AHP Fuzzy. Sem ele, `w` crisp é promovido a TFN degenerado (w, w, w), e o
    resultado é o TOPSIS Fuzzy com pesos pontuais.
    """
    F = validar_tfn(X_fuzzy, "X_fuzzy")
    m, k = F.shape[0], F.shape[1]
    if len(direcoes) != k:
        raise ValueError(f"direções: esperadas {k}, recebidas {len(direcoes)}")

    if w_fuzzy is not None:
        W = validar_tfn(np.asarray(w_fuzzy, dtype=np.float64), "w_fuzzy")
        if W.shape != (k, 3):
            raise ValueError(f"w_fuzzy deve ser ({k}, 3), recebida {W.shape}")
    else:
        wc = np.asarray(w, dtype=np.float64).ravel()
        if wc.size != k:
            raise ValueError(f"pesos: esperados {k}, recebidos {wc.size}")
        if (wc < 0).any():
            raise ValueError("pesos negativos")
        if wc.sum() <= 0:
            raise ValueError("soma dos pesos é zero")
        wc = wc / wc.sum()
        W = np.repeat(wc[:, None], 3, axis=1)            # TFN degenerado (w,w,w)

    R = normalizar_fuzzy_chen(F, direcoes)
    V = R * W[None, :, :]                                # (m, k, 3)
    d_pos = np.sqrt(((V - 1.0) ** 2).sum(axis=2) / 3.0).sum(axis=1)
    d_neg = np.sqrt((V ** 2).sum(axis=2) / 3.0).sum(axis=1)
    soma = d_pos + d_neg
    return d_neg / np.where(soma == 0, 1.0, soma)


def fuzzy_topsis_de_crisp(X, w, direcoes, alpha=FUZZY_ALPHA, w_fuzzy=None):
    """Atalho: fuzzifica a matriz crisp com banda ±alpha e roda o TOPSIS Fuzzy."""
    return fuzzy_topsis(fuzzificar_matriz(X, alpha), w, direcoes, w_fuzzy=w_fuzzy)


if __name__ == "__main__":
    print("Extensões fuzzy — AHP Fuzzy (Buckley 1985) · TOPSIS Fuzzy (Chen 2000)")
    print(f"  banda padrão da matriz de decisão : ±{FUZZY_ALPHA:.0%}")
    print(f"  fator geométrico dos julgamentos  : ×/÷ {FUZZY_FATOR_SAATY}")
