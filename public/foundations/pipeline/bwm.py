"""
BWM — Best-Worst Method (Rezaei, 2015; forma linear em Rezaei, 2016).

═══════════════════════════════════════════════════════════════════════════════
 O PROBLEMA QUE ELE RESOLVE — e que o AHP não resolve
═══════════════════════════════════════════════════════════════════════════════
O AHP pede n(n−1)/2 comparações par a par. Com 9 critérios são **36 julgamentos**.
Ninguém preenche 36 comparações com atenção constante, e a matriz que volta do
workshop costuma ter consistência ruim — não porque o decisor não sabe o que quer,
mas porque a tarefa é longa demais.

O BWM pede **2n−3**: para 9 critérios, **15**. O decisor escolhe o MELHOR e o PIOR
critério e compara só esses dois contra os demais. Duas perguntas que ele responde
bem ("qual é o mais importante?", "qual é o menos?") substituem 21 comparações que
ele responderia mal.

    n       AHP n(n−1)/2      BWM 2n−3      redução
    4             6               5           17%
    6            15               9           40%
    9            36              15           58%
   12            66              21           68%

E há um ganho de qualidade junto: comparar tudo contra duas âncoras elimina os
ciclos de preferência que a comparação livre produz.

REFERÊNCIAS
    REZAEI, J. "Best-worst multi-criteria decision-making method".
        Omega, 53:49-57, 2015.
    REZAEI, J. "Best-worst multi-criteria decision-making method: Some properties
        and a linear model". Omega, 64:126-130, 2016.  ← modelo linear usado aqui
    LIANG, F.; BRUNELLI, M.; REZAEI, J. "Consistency issues in the best worst
        method: Measurements and thresholds". Omega, 96:102175, 2020.

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import numpy as np

# Índice de consistência de Rezaei (2015), tabela 1: valor máximo de ξ em função
# de a_BW. É o denominador da razão de consistência.
CI_BWM = {1: 0.00, 2: 0.44, 3: 1.00, 4: 1.63, 5: 2.30,
          6: 3.00, 7: 3.73, 8: 4.47, 9: 5.23}

# Acima de CR = 0,10 o julgamento é tratado como inconsistente — mesmo limiar do
# AHP, por coerência com o resto do projeto.
BWM_CR_LIMITE = 0.10


def _ci(a_bw):
    """Índice de consistência para a_BW, interpolado fora dos inteiros tabelados.

    a_BW é o julgamento "quanto o melhor supera o pior" e é, por construção, o
    maior valor da escala usada. Fora de 1..9 extrapolamos linearmente em vez de
    devolver 0 — devolver 0 faria o CR virar divisão por zero ou, pior,
    silenciosamente 0, que é o veredito de 'perfeitamente consistente'.
    """
    a = float(a_bw)
    if a <= 1:
        return 0.0
    if a in CI_BWM:
        return CI_BWM[a]
    lo = int(np.floor(a))
    if lo >= 9:
        return CI_BWM[9] + (a - 9) * (CI_BWM[9] - CI_BWM[8])
    frac = a - lo
    return CI_BWM[lo] + frac * (CI_BWM[lo + 1] - CI_BWM[lo])


def validar_bwm(melhor, pior, a_bo, a_ow, n):
    """Confere a coerência estrutural dos dois vetores antes de resolver.

    Os três erros que a validação pega, e que produziriam pesos plausíveis e
    errados se passassem:
      · a_BO[melhor] ≠ 1 — o melhor critério comparado consigo mesmo;
      · a_OW[pior] ≠ 1 — idem para o pior;
      · a_BO[pior] ≠ a_OW[melhor] — o mesmo julgamento "melhor contra pior"
        aparece nos DOIS vetores e tem de ser o mesmo número. É a única
        redundância do método, e é ela que faz 2n−2 virar 2n−3.
    """
    a_bo = np.asarray(a_bo, dtype=np.float64).ravel()
    a_ow = np.asarray(a_ow, dtype=np.float64).ravel()
    if a_bo.size != n or a_ow.size != n:
        raise ValueError(f"vetores BO/OW devem ter {n} entradas, "
                         f"recebidas {a_bo.size} e {a_ow.size}")
    if not (0 <= melhor < n and 0 <= pior < n):
        raise ValueError(f"índices melhor={melhor} e pior={pior} fora de 0..{n-1}")
    if melhor == pior and n > 1:
        raise ValueError("o melhor e o pior critério não podem ser o mesmo")
    if (a_bo <= 0).any() or (a_ow <= 0).any():
        raise ValueError("julgamentos do BWM devem ser estritamente positivos")
    if abs(a_bo[melhor] - 1.0) > 1e-9:
        raise ValueError(f"a_BO[melhor] deve ser 1, recebido {a_bo[melhor]}")
    if abs(a_ow[pior] - 1.0) > 1e-9:
        raise ValueError(f"a_OW[pior] deve ser 1, recebido {a_ow[pior]}")
    if abs(a_bo[pior] - a_ow[melhor]) > 1e-9:
        raise ValueError(
            f"a_BW inconsistente entre os vetores: a_BO[pior]={a_bo[pior]} "
            f"≠ a_OW[melhor]={a_ow[melhor]} — é o MESMO julgamento")
    return a_bo, a_ow


def pesos_bwm(melhor, pior, a_bo, a_ow):
    """Pesos pelo modelo LINEAR do BWM. Devolve (w, ksi, cr, consistente).

    Modelo (Rezaei, 2016):

        min  ξᴸ
        s.a. |w_B − a_Bj · w_j| ≤ ξᴸ      para todo j
             |w_j − a_jW · w_W| ≤ ξᴸ      para todo j
             Σ w_j = 1,  w_j ≥ 0

    POR QUE O LINEAR E NÃO O ORIGINAL. O modelo de 2015 minimiza
    max|w_B/w_j − a_Bj|, que é não-linear e pode ter **múltiplas soluções ótimas**
    — o decisor recebe um intervalo de pesos, não um vetor. O linear de 2016 tem
    solução única e o mesmo significado. Para apoio à decisão, um vetor que o
    comitê possa auditar vale mais que um intervalo que ninguém sabe usar.

    ξᴸ* é lido diretamente como indicador de consistência: 0 = julgamento
    perfeitamente coerente; quanto maior, mais os dois vetores se contradizem.
    """
    a_bo = np.asarray(a_bo, dtype=np.float64).ravel()
    n = a_bo.size
    a_bo, a_ow = validar_bwm(melhor, pior, a_bo, a_ow, n)

    try:
        from scipy.optimize import linprog
    except ImportError as erro:                               # pragma: no cover
        raise ImportError(
            "o BWM resolve um programa linear e precisa de scipy.optimize.linprog. "
            "Instale com `pip install scipy`. É a única dependência além do NumPy, "
            "e só o BWM a usa."
        ) from erro

    # Variáveis: [w_0 … w_{n-1}, ξ].  Objetivo: minimizar ξ.
    c = np.zeros(n + 1)
    c[n] = 1.0
    A_ub, b_ub = [], []
    for j in range(n):
        if j != melhor:
            # w_B − a_Bj·w_j − ξ ≤ 0   e   −w_B + a_Bj·w_j − ξ ≤ 0
            lin = np.zeros(n + 1); lin[melhor] = 1.0; lin[j] -= a_bo[j]; lin[n] = -1.0
            A_ub.append(lin.copy()); b_ub.append(0.0)
            A_ub.append(-lin + np.eye(n + 1)[n] * -2.0); b_ub.append(0.0)
        if j != pior:
            # w_j − a_jW·w_W − ξ ≤ 0   e   −w_j + a_jW·w_W − ξ ≤ 0
            lin = np.zeros(n + 1); lin[j] = 1.0; lin[pior] -= a_ow[j]; lin[n] = -1.0
            A_ub.append(lin.copy()); b_ub.append(0.0)
            A_ub.append(-lin + np.eye(n + 1)[n] * -2.0); b_ub.append(0.0)

    A_eq = np.zeros((1, n + 1)); A_eq[0, :n] = 1.0
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  A_eq=A_eq, b_eq=np.array([1.0]),
                  bounds=[(0.0, None)] * n + [(0.0, None)], method="highs")
    if not res.success:
        raise RuntimeError(f"BWM: o programa linear não convergiu — {res.message}")

    w = np.asarray(res.x[:n], dtype=np.float64)
    w = w / w.sum()
    ksi = float(res.x[n])
    ci = _ci(a_bo[pior])
    cr = float(ksi / ci) if ci > 0 else 0.0
    return w, ksi, cr, bool(cr <= BWM_CR_LIMITE)


def bwm_de_pesos(w_referencia, escala_max=9.0):
    """Deriva os vetores BO e OW a partir de um vetor de pesos já conhecido.

    Serve para COMPARAR o BWM com as outras fontes sobre o mesmo julgamento: a
    partir dos pesos de referência montamos as razões que um decisor coerente
    teria declarado, e rodamos o BWM sobre elas.

    ⚠️  Isto NÃO é o BWM como se usa na prática. O método existe para colher
    julgamento humano; aqui o julgamento é derivado de pesos que já existiam, e o
    resultado só responde: *se o decisor fosse perfeitamente coerente com estes
    pesos, o BWM os recuperaria?* Com elicitação real, passe `melhor`, `pior`,
    `a_bo` e `a_ow` direto para `pesos_bwm`. Esta função está aqui para o
    relatório poder confrontar as fontes, e diz isso no texto que gera.

    As razões são recortadas em [1, escala_max]: a escala do BWM é 1..9 como a de
    Saaty, e uma razão de 256 (que as matrizes geradas deste projeto produzem)
    não é um julgamento que alguém faça.
    """
    w = np.asarray(w_referencia, dtype=np.float64).ravel()
    if w.size < 2:
        raise ValueError("BWM exige ao menos 2 critérios")
    if (w <= 0).any():
        raise ValueError("pesos de referência devem ser positivos")
    melhor, pior = int(np.argmax(w)), int(np.argmin(w))
    a_bo = np.clip(w[melhor] / w, 1.0, escala_max)
    a_ow = np.clip(w / w[pior], 1.0, escala_max)
    a_bo[melhor] = 1.0
    a_ow[pior] = 1.0
    # A redundância a_BW tem de bater nos dois vetores; o recorte pode separá-los.
    a_bw = min(float(np.clip(w[melhor] / w[pior], 1.0, escala_max)), escala_max)
    a_bo[pior] = a_bw
    a_ow[melhor] = a_bw
    return melhor, pior, a_bo, a_ow


def comparacoes(n):
    """Quantas comparações cada método pede para n critérios — o argumento do BWM."""
    return {"AHP": n * (n - 1) // 2, "BWM": max(2 * n - 3, 1)}


if __name__ == "__main__":
    print("BWM — Best-Worst Method (Rezaei, 2015/2016)")
    print(f"  {'critérios':>10} {'AHP':>8} {'BWM':>8} {'redução':>9}")
    for n in (4, 6, 9, 12, 15):
        c = comparacoes(n)
        print(f"  {n:>10} {c['AHP']:>8} {c['BWM']:>8} "
              f"{1 - c['BWM'] / c['AHP']:>8.0%}")
