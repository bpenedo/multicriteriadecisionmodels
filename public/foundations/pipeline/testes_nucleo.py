"""
Suíte de verificação matemática — Passada 1 da tripla-checagem.

Não é teste de unidade no sentido usual (não verifica se a função foi chamada): verifica
PROPRIEDADES MATEMÁTICAS que os métodos precisam satisfazer, contra casos cuja resposta
é conhecida analiticamente.

Princípio que organiza a suíte: **todo verificador precisa de um teste que prove que ele
REPROVA**. Testar só o caso bom foi o que deixou passar o #BUG-001, em que o cálculo de
consistência do AHP aprovava qualquer julgamento a partir de 9 critérios.

Uso:  python3 testes_nucleo.py

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import sys

import numpy as np

from metodos_br import (borda_ordinal, copeland, electre_ii, promethee_sapevo_m1,
                        sapevo_m_de_matriz, sapevo_m_pesos, todim, vikor)
from bwm import bwm_de_pesos, comparacoes, pesos_bwm
from drsa import (discretizar_classes, induzir_regras, qualidade_aproximacao,
                  texto_regra)
from fuzzy import (fuzzificar_matriz, fuzzificar_saaty, fuzzy_ahp_pesos,
                   fuzzy_topsis_de_crisp, indice_fuzziness,
                   normalizar_fuzzy_chen, validar_tfn)
from nucleo import (METODOS, RI, ahp_topsis_2n, borda, dematel, electre_i, maut,
                    mcda_c, orientar, pesos_ahp, pontuar_todos, preparar,
                    promethee_ii, ranks, topsis)

FALHAS = []


def checar(condicao, descricao):
    if condicao:
        print(f"    ✅ {descricao}")
    else:
        print(f"    ❌ {descricao}")
        FALHAS.append(descricao)
    return condicao


def secao(titulo):
    print(f"\n[{titulo}]")


def problema_dominante():
    """alt0 é a melhor nos DOIS critérios: dominância estrita, resposta conhecida."""
    X = np.array([[10.0, 1.0], [8.0, 3.0], [6.0, 5.0]])
    return X, ["benefit", "cost"], np.array([0.5, 0.5])


# ---------------------------------------------------------------------------
def teste_ahp_consistente():
    secao("1. AHP — recupera pesos de matriz consistente por construção")
    p = np.array([0.5, 0.25, 0.15, 0.10])
    A = p[:, None] / p[None, :]                    # a_ij = p_i/p_j  =>  CR = 0
    w, cr, lmax = pesos_ahp(A)
    checar(np.allclose(w, p, atol=1e-9), f"pesos exatos recuperados {np.round(w, 4)}")
    checar(abs(lmax - 4) < 1e-9, f"λmax = {lmax:.9f} (deve ser n = 4)")
    checar(cr < 1e-9, f"CR = {cr:.2e} (deve ser ~0)")


def teste_ahp_reprova():
    secao("2. AHP — REPROVA ciclo de preferência (o verificador tem que reprovar)")
    B = np.array([[1, 9, 1/9], [1/9, 1, 9], [9, 1/9, 1]], float)   # A≫B≫C≫A
    _, cr, _ = pesos_ahp(B)
    checar(cr > 0.10, f"CR = {cr:.4f} > 0,10 — julgamento rejeitado")


def teste_ahp_muitos_criterios():
    secao("3. AHP — regressão do #BUG-001: n > 8 não pode devolver CR = 0")
    q = np.random.default_rng(0).uniform(1, 5, 10)
    C = q[:, None] / q[None, :]
    C[0, 1] *= 7                                    # injeta 1 julgamento absurdo
    C[1, 0] = 1 / C[0, 1]
    _, cr, _ = pesos_ahp(C)
    checar(max(RI) >= 15, f"Índice Aleatório tabelado até n = {max(RI)}")
    checar(cr > 0, f"CR = {cr:.4f} > 0 com n = 10 (antes era zero silencioso)")


def teste_dematel():
    secao("4. DEMATEL — pesos somam 1 e papéis batem com a matriz de entrada")
    Z = np.array([[0, 3, 3, 0], [0, 0, 2, 0], [0, 0, 0, 0], [3, 3, 3, 0]], float)
    _R, _C, _prom, rel, pesos, _T, _lim = dematel(Z)
    checar(abs(pesos.sum() - 1) < 1e-12, f"Σpesos = {pesos.sum():.12f}")
    checar(rel[3] > 0, "critério 4 (influencia todos) classificado como CAUSA")
    checar(rel[2] < 0, "critério 3 (não influencia ninguém) classificado como EFEITO")


def teste_dominancia():
    secao(f"5. Dominância estrita — TODOS os {len(METODOS)} métodos devem eleger a alternativa dominante")
    X, dirs, w = problema_dominante()
    prep = preparar(X, dirs)
    scores = prep.pontuar(w)
    checar(len(scores) == len(METODOS), f"{len(scores)} métodos no consenso")
    for metodo in METODOS:
        rk = ranks(scores[metodo])
        checar(rk[0] == 1 and rk[2] == 3,
               f"{metodo:<15} ranks={list(rk)} (dominante em 1º, pior em último)")


def teste_topsis():
    secao("6. TOPSIS 2N — Ci ∈ [0,1] nas duas normalizações")
    X, dirs, w = problema_dominante()
    ci_v, ci_m, ci_f = ahp_topsis_2n(X, w, dirs)
    checar((ci_f >= 0).all() and (ci_f <= 1).all(), f"Ci final ∈ [0,1]: {np.round(ci_f, 4)}")
    checar(np.array_equal(ranks(ci_v), ranks(ci_m)),
           "as duas normalizações concordam na ordem (caso dominante)")


def teste_borda():
    secao("7. Borda — preserva unanimidade")
    M = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
    checar(list(ranks(borda(M, 3))) == [1, 2, 3], "3 métodos unânimes → mesma ordenação")


def teste_orientar():
    secao("8. orientar() — direção do custo e coluna constante (#BUG-019)")
    Xc = np.array([[1.0, 5.0], [3.0, 5.0], [5.0, 5.0]])
    G = orientar(Xc, ["cost", "benefit"])
    checar(np.allclose(G[:, 0], [1, 0.5, 0]), f"custo invertido: {G[:, 0]}")
    checar(np.allclose(G[:, 1], 0.5), f"coluna constante → 0,5 (indiferença), não zero: {G[:, 1]}")


# --- escola brasileira ------------------------------------------------------
def teste_vikor():
    secao("9. VIKOR — Q(melhor) = 0 e condições C1/C2 avaliadas")
    X, dirs, w = problema_dominante()
    score, S, R, Q, diag = vikor(X, w, dirs)
    checar(abs(Q.min()) < 1e-12 and Q.argmin() == 0, f"Q = {np.round(Q, 4)}, mínimo na dominante")
    checar(diag["c1_vantagem_aceitavel"] and diag["c2_estabilidade_aceitavel"],
           f"C1 e C2 satisfeitas — {diag['situacao']}")
    checar(ranks(score)[0] == 1, "dominante em 1º (score = −Q)")


def teste_todim():
    secao("10. TODIM — ξ ∈ [0,1] com máx = 1 e mín = 0, em todo θ")
    X, dirs, w = problema_dominante()
    for theta in (0.5, 1.0, 2.5):
        xi, _ = todim(X, w, dirs, theta=theta)
        checar(abs(xi.max() - 1) < 1e-12 and abs(xi.min()) < 1e-12 and ranks(xi)[0] == 1,
               f"θ = {theta:<4} ξ = {np.round(xi, 4)}")
    try:
        todim(X, w, dirs, theta=0.0)
        checar(False, "θ = 0 deveria ser rejeitado")
    except ValueError:
        checar(True, "θ ≤ 0 rejeitado com erro explícito")


def teste_electre_ii():
    secao("11. ELECTRE II — pré-ordem completa por dupla destilação")
    X, dirs, w = problema_dominante()
    score, desc, asc, forte, fraca = electre_ii(X, w, dirs)
    checar(ranks(score)[0] == 1, f"ranks = {list(ranks(score))}")
    checar(len(set(desc)) > 1, f"destilação descendente separa níveis: {list(desc)}")


def teste_sapevo():
    secao("12. SAPEVO-M — Σpesos = 1, nenhum peso nulo, ordem preservada")
    D1 = np.array([[0, 1, 2, 3], [-1, 0, 1, 2], [-2, -1, 0, 1], [-3, -2, -1, 0]], float)
    D2 = np.array([[0, 2, 2, 3], [-2, 0, 1, 1], [-2, -1, 0, 2], [-3, -1, -2, 0]], float)
    D3 = np.array([[0, 0, 1, 2], [0, 0, 1, 3], [-1, -1, 0, 1], [-2, -3, -1, 0]], float)
    p = sapevo_m_pesos([D1, D2, D3])
    checar(abs(p.sum() - 1) < 1e-12, f"Σpesos = {p.sum():.12f}")
    checar((p > 0).all(), f"nenhum peso nulo (menor = {p.min():.6f} = 1% do superior)")
    checar(p[0] > p[1] > p[2] > p[3], f"ordem de importância preservada: {np.round(p, 4)}")


def teste_copeland():
    secao("13. Copeland — empata em ciclo de Condorcet, onde Borda arbitra")
    M = np.array([[1, 2, 3], [3, 1, 2], [2, 3, 1]])         # ciclo de maioria perfeito
    c, b = copeland(M), borda_ordinal(M)
    checar((c == 0).all(), f"Copeland empata tudo em 0: {c}")
    checar(len(set(b)) == 1, f"Borda também empata neste ciclo simétrico: {b}")


def teste_hibrido():
    secao("14. PROMETHEE-SAPEVO-M1 — pesos ordinais alimentam o fluxo φ")
    D = np.array([[0, 1, 2, 3], [-1, 0, 1, 2], [-2, -1, 0, 1], [-3, -2, -1, 0]], float)
    X = np.array([[10., 1., 5., 2.], [8., 3., 7., 4.], [6., 5., 9., 1.], [9., 2., 6., 3.]])
    phi, pesos = promethee_sapevo_m1(X, ["benefit", "cost", "benefit", "cost"], [D])
    checar(abs(pesos.sum() - 1) < 1e-12, f"pesos SAPEVO-M somam 1: {np.round(pesos, 4)}")
    checar(np.isfinite(phi).all(), f"fluxo líquido finito: {np.round(phi, 4)}")


def teste_equivalencia():
    secao("15. Caminho rápido ≡ métodos diretos (a otimização não mudou resultado)")
    rng = np.random.default_rng(11)
    X = rng.uniform(1, 100, (9, 7))
    dirs = ["benefit" if i % 3 else "cost" for i in range(7)]
    prep = preparar(X, dirs)
    ok, cobertura = True, set()
    for _ in range(100):
        w = rng.dirichlet(np.full(7, 25.0))
        rapido = prep.pontuar(w)
        # Confrontar com pontuar_todos em vez de listar os métodos à mão: a lista
        # manual ficou 9/10 quando o TOPSIS Fuzzy entrou, e um método não comparado
        # não acusa divergência nenhuma (#BUG-049).
        lento = pontuar_todos(X, w, dirs)
        cobertura |= set(lento)
        for nome in METODOS:
            if not np.array_equal(ranks(rapido[nome]), ranks(lento[nome])):
                ok = False
    checar(ok, f"100 universos × {len(METODOS)} métodos: rankings idênticos nos dois caminhos")
    checar(cobertura == set(METODOS),
           f"os dois caminhos cobrem METODOS inteiro ({len(METODOS)} métodos)")


def teste_entradas_invalidas():
    secao("16. Entradas inválidas falham ALTO (nunca silenciosamente)")
    X, dirs, _ = problema_dominante()
    casos = [
        ("pesos negativos", lambda: maut(X, [-1.0, 2.0], dirs)),
        ("soma de pesos zero", lambda: maut(X, [0.0, 0.0], dirs)),
        ("nº de pesos errado", lambda: maut(X, [1.0], dirs)),
        ("DEMATEL não quadrado", lambda: dematel(np.ones((2, 3)))),
        ("DEMATEL todo zero", lambda: dematel(np.zeros((3, 3)))),
        ("AHP com zero", lambda: pesos_ahp(np.zeros((3, 3)))),
        ("preferência inexistente", lambda: promethee_ii(X, [0.5, 0.5], dirs, tipo="inexistente")),
    ]
    for descricao, fn in casos:
        try:
            fn()
            checar(False, f"{descricao} — deveria ter falhado")
        except (ValueError, np.linalg.LinAlgError):
            checar(True, f"{descricao} — rejeitado com erro explícito")


def teste_fuzzy_ahp():
    secao("17. AHP Fuzzy (Buckley 1985) — degenerescência, modal e reciprocidade")
    A = np.array([[1, 2, 4], [0.5, 1, 2], [0.25, 0.5, 1]], float)
    w_crisp, _cr, _l = pesos_ahp(A)

    # fator = 1 não espalha nada: tem de devolver exatamente o AHP crisp.
    w_f1, W1 = fuzzy_ahp_pesos(fuzzificar_saaty(A, 1.0))
    checar(np.allclose(w_crisp, w_f1, atol=1e-12),
           f"fator=1 reproduz o AHP crisp (Δ = {np.abs(w_crisp - w_f1).max():.1e})")
    checar(abs(indice_fuzziness(W1)) < 1e-9, "Φ = 0 quando não há espalhamento")

    # O defeito do #BUG-043: razão fora da escala de Saaty perdia o valor modal.
    F = fuzzificar_saaty(np.array([[1.0, 128.0], [1 / 128, 1.0]]), 1.5)
    checar(abs(F[0, 1, 1] - 128.0) < 1e-9,
           f"razão 128 (fora de [1/9,9]) mantém o modal → {F[0, 1, 1]:.1f}")
    checar(F[0, 1, 0] < F[0, 1, 1] < F[0, 1, 2], "TFN ordenado (l < m < u)")
    checar(abs(F[0, 1, 0] * F[1, 0, 2] - 1) < 1e-12
           and abs(F[0, 1, 1] * F[1, 0, 1] - 1) < 1e-12,
           "reciprocidade fuzzy exata (l·u' = m·m' = 1)")

    w_f, W_f = fuzzy_ahp_pesos(fuzzificar_saaty(A, 1.5))
    checar(abs(w_f.sum() - 1) < 1e-12 and (w_f > 0).all(),
           "pesos fuzzy somam 1 e nenhum é zerado")
    checar(np.array_equal(np.argsort(-w_crisp), np.argsort(-w_f)),
           "ordem de importância do AHP é preservada")
    checar(indice_fuzziness(W_f) > 0, "Φ > 0 quando há espalhamento declarado")


def teste_fuzzy_topsis():
    secao("18. TOPSIS Fuzzy (Chen 2000) — não é o TOPSIS do projeto com ruído")
    X = np.array([[25., 40., 4.2], [15., 35., 3.5], [5., 40., 8.8], [25., 30., 2.5]])
    dirs = ["benefit", "benefit", "cost"]
    w = np.array([0.5, 0.3, 0.2])

    def topsis_chen_crisp(X, w, dirs):
        """TOPSIS com as DUAS outras escolhas de Chen: normalização linear e
        ideais absolutos. É nisto que o fuzzy degenera quando alpha = 0."""
        X = np.asarray(X, float); w = np.asarray(w, float) / np.sum(w)
        R = np.empty_like(X)
        for j, d in enumerate(dirs):
            col = X[:, j]
            R[:, j] = col / col.max() if d == "benefit" else col.min() / col
        V = R * w
        dp = np.sqrt((V - 1.0) ** 2).sum(axis=1)
        dn = np.sqrt(V ** 2).sum(axis=1)
        return dn / (dp + dn)

    cc0 = fuzzy_topsis_de_crisp(X, w, dirs, alpha=0.0)
    checar(np.allclose(cc0, topsis_chen_crisp(X, w, dirs), atol=1e-12),
           "alpha=0 degenera em TOPSIS linear com ideais absolutos")
    # E NÃO no topsis() vetorial — confundir os dois levaria a "consertar" o certo.
    checar(not np.allclose(cc0, topsis(X, w, dirs), atol=1e-6),
           "alpha=0 NÃO reproduz o topsis() vetorial — diferença de método (#BUG-040)")

    Xd, dirs_d, w_d = problema_dominante()
    cc_dom = fuzzy_topsis_de_crisp(Xd, w_d, dirs_d)
    checar(ranks(cc_dom)[0] == 1, "alternativa dominante é 1ª também no TOPSIS Fuzzy")
    checar(((cc_dom >= 0) & (cc_dom <= 1)).all(), "CC permanece em [0,1]")

    # custo com zero não pode virar infinito
    Xz = np.array([[10., -5.], [20., 3.], [30., 0.]])
    R = normalizar_fuzzy_chen(fuzzificar_matriz(Xz, 0.10), ["benefit", "cost"])
    checar(R.shape == (3, 2, 3) and np.isfinite(R).all(),
           "normalização de Chen é finita com custo zero e valor negativo")

    prep = preparar(X, dirs)
    checar(np.allclose(prep.topsis_fuzzy(w / w.sum()),
                       fuzzy_topsis_de_crisp(X, w, dirs), atol=1e-12),
           "caminho rápido idêntico ao lento")
    checar(len(METODOS) == 10 and "TOPSIS Fuzzy" in METODOS,
           f"METODOS traz as dez escolas ({len(METODOS)})")
    checar(set(prep.pontuar(w).keys()) == set(METODOS),
           "pontuar() devolve exatamente o que METODOS declara")


def teste_fuzzy_entradas_invalidas():
    secao("19. Fuzzy — entrada inválida falha ALTO, nunca em silêncio")
    A = np.array([[1, 2], [0.5, 1]], float)
    X = np.array([[25., 40.], [15., 35.]])
    casos = [
        ("TFN invertido (l > u)", lambda: validar_tfn(np.array([[3.0, 2.0, 1.0]]))),
        ("fator < 1", lambda: fuzzificar_saaty(A, 0.5)),
        ("alpha negativo", lambda: fuzzificar_matriz(X, -0.1)),
        ("Saaty com zero", lambda: fuzzificar_saaty(np.zeros((2, 2)))),
        ("direção inválida", lambda: fuzzy_topsis_de_crisp(X, [0.5, 0.5], ["xpto", "benefit"])),
        ("pesos a menos", lambda: fuzzy_topsis_de_crisp(X, [1.0], ["benefit", "cost"])),
        ("pesos somando zero", lambda: fuzzy_topsis_de_crisp(X, [0.0, 0.0], ["benefit", "cost"])),
    ]
    for nome, fn in casos:
        try:
            fn()
            checar(False, f"{nome} — NÃO levantou erro (falha silenciosa!)")
        except (ValueError, TypeError, IndexError):
            checar(True, f"{nome} — rejeitado com erro explícito")


def teste_bwm():
    secao("20. BWM (Rezaei 2015/2016) — menos comparações, mesmo julgamento")
    # Exemplo publicado no artigo de 2015 (§4): escolha de carro.
    # Melhor = Price (1), Pior = Style (4).
    a_bo = [2., 1., 4., 3., 8.]
    a_ow = [4., 8., 2., 3., 1.]
    w, ksi, cr, ok = pesos_bwm(1, 4, a_bo, a_ow)
    checar(abs(w.sum() - 1) < 1e-12, f"Σw = {w.sum():.12f}")
    checar(int(np.argmax(w)) == 1 and int(np.argmin(w)) == 4,
           "o eleito MELHOR recebe o maior peso e o PIOR o menor")
    checar(cr < 0.10 and ok, f"julgamento do artigo é consistente (CR = {cr:.4f})")

    # Julgamento perfeitamente coerente: ξᴸ = 0 e os pesos são recuperados.
    wr = np.array([0.5, 0.25, 0.15, 0.10])
    m_i, p_i, bo, ow = bwm_de_pesos(wr)
    w2, k2, cr2, _ = pesos_bwm(m_i, p_i, bo, ow)
    checar(k2 < 1e-9, f"coerência perfeita devolve ξᴸ ≈ 0 ({k2:.2e})")
    checar(np.allclose(w2, wr, atol=1e-9),
           f"e recupera os pesos de referência (Δ = {np.abs(w2-wr).max():.1e})")

    # O argumento do método, em número.
    for n, esperado in [(4, 5), (6, 9), (9, 15), (12, 21)]:
        c = comparacoes(n)
        checar(c["BWM"] == esperado and c["AHP"] == n * (n - 1) // 2,
               f"n={n}: BWM {c['BWM']} × AHP {c['AHP']} comparações")

    # Entrada estruturalmente incoerente tem de falhar ALTO.
    casos = [
        ("a_BO[melhor] ≠ 1", lambda: pesos_bwm(0, 2, [2., 3., 9.], [9., 3., 1.])),
        ("a_OW[pior] ≠ 1", lambda: pesos_bwm(0, 2, [1., 3., 9.], [9., 3., 2.])),
        ("a_BW divergente entre BO e OW",
         lambda: pesos_bwm(0, 2, [1., 3., 9.], [7., 3., 1.])),
        ("melhor == pior", lambda: pesos_bwm(1, 1, [1., 1., 1.], [1., 1., 1.])),
        ("julgamento não positivo", lambda: pesos_bwm(0, 2, [1., 0., 9.], [9., 3., 1.])),
    ]
    for nome, fn in casos:
        try:
            fn()
            checar(False, f"{nome} — NÃO levantou erro (falha silenciosa!)")
        except (ValueError, TypeError, IndexError):
            checar(True, f"{nome} — rejeitado com erro explícito")


def teste_drsa():
    secao("21. DRSA (Greco, Matarazzo & Słowiński) — regras e princípio de dominância")
    X = np.array([[9., 9.], [7., 8.], [5., 5.], [3., 4.], [1., 1.]])
    dirs = ["benefit", "benefit"]
    cls = np.array([3, 3, 2, 1, 1])
    G = orientar(X, dirs)

    gamma, ambiguas, violacoes = qualidade_aproximacao(G, cls)
    checar(abs(gamma - 1.0) < 1e-12, f"classificação coerente devolve γ = {gamma:.3f}")
    checar(ambiguas.sum() == 0 and not violacoes, "nenhuma ambiguidade nem violação")

    regras = induzir_regras(X, dirs, cls, ["nota", "preco"])
    checar(len(regras) > 0, f"{len(regras)} regra(s) induzida(s)")
    checar(all(r["certeza"] == 1.0 for r in regras),
           "só regras CERTAS (da aproximação inferior)")
    # Toda regra tem de ser verdadeira nos dados que diz cobrir.
    ok_sup = all(all(cls[i] >= r["classe_min"] for i in r["suporte"]) for r in regras)
    checar(ok_sup, "nenhuma regra cobre objeto abaixo da classe que afirma")
    # Limiar sai de valor OBSERVADO, não de ponto médio inventado.
    observados = {float(v) for col in range(X.shape[1]) for v in X[:, col]}
    checar(all(v in observados for r in regras for _rot, _d, v in r["condicoes"]),
           "todo limiar corresponde a um valor que existe nos dados")
    # Minimalidade: nenhuma regra é subsumida por outra da mesma classe.
    subsumida = any(i != j and r["classe_min"] == q["classe_min"]
                    and set(r["suporte"]) <= set(q["suporte"])
                    for i, r in enumerate(regras) for j, q in enumerate(regras))
    checar(not subsumida, "conjunto de regras é minimal (nenhuma subsumida)")

    # Violação do princípio de dominância: a 1 domina a 0 e foi classificada PIOR.
    Xv = np.array([[5., 5.], [9., 9.], [1., 1.]])
    gv, ambv, violv = qualidade_aproximacao(orientar(Xv, dirs), np.array([3, 2, 1]))
    checar(gv < 1.0, f"γ < 1 denuncia inconsistência nos dados (γ = {gv:.3f})")
    checar((1, 0) in violv, "o par que viola a dominância é identificado")

    # Discretização por quantil sobrevive a outlier.
    classes_out = discretizar_classes(np.array([1., 2., 3., 4., 100.]), 3)
    checar(len(set(classes_out)) == 3, "quantis mantêm as 3 classes povoadas com outlier")

    # Critério de CUSTO precisa sair com ≤ na frase, não ≥.
    Xc = np.array([[10., 1.], [20., 2.], [30., 3.]])
    rc = induzir_regras(Xc, ["cost", "benefit"], np.array([3, 2, 1]), ["preco", "nota"])
    tem_custo = [c for r in rc for c in r["condicoes"] if c[0] == "preco"]
    checar(all(d == "cost" for _r, d, _v in tem_custo) if tem_custo else True,
           "condição sobre critério de custo é marcada como custo")
    checar(all("≤" in texto_regra(r) or "preco" not in texto_regra(r) for r in rc),
           "e aparece como ≤ na frase legível")


def main():
    print("=" * 78)
    print(" SUÍTE DE VERIFICAÇÃO MATEMÁTICA — Passada 1 da tripla-checagem")
    print(" MCDM Studio · ProfBru - Bruno Penedo © 2026")
    print("=" * 78)

    for teste in (teste_ahp_consistente, teste_ahp_reprova, teste_ahp_muitos_criterios,
                  teste_dematel, teste_dominancia, teste_topsis, teste_borda,
                  teste_orientar, teste_vikor, teste_todim, teste_electre_ii,
                  teste_sapevo, teste_copeland, teste_hibrido, teste_equivalencia,
                  teste_entradas_invalidas,
                  teste_fuzzy_ahp, teste_fuzzy_topsis, teste_fuzzy_entradas_invalidas,
                  teste_bwm, teste_drsa):
        teste()

    print("\n" + "=" * 78)
    if FALHAS:
        print(f" ❌ {len(FALHAS)} VERIFICAÇÃO(ÕES) FALHARAM — publicação BLOQUEADA")
        for f in FALHAS:
            print(f"    • {f}")
        print("=" * 78)
        return 1
    print(" ✅ TODAS AS VERIFICAÇÕES PASSARAM — Passada 1 aprovada")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
