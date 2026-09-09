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
from nucleo import (METODOS, RI, ahp_topsis_2n, borda, dematel, electre_i, maut,
                    mcda_c, orientar, pesos_ahp, preparar, promethee_ii, ranks)

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
    secao("5. Dominância estrita — TODOS os 9 métodos devem eleger a alternativa dominante")
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
    ok = True
    for _ in range(100):
        w = rng.dirichlet(np.full(7, 25.0))
        rapido = prep.pontuar(w)
        for nome, lento in (("ELECTRE II", electre_ii(X, w, dirs)[0]),
                            ("VIKOR", vikor(X, w, dirs)[0]),
                            ("TODIM", todim(X, w, dirs)[0]),
                            ("SAPEVO-M", sapevo_m_de_matriz(X, dirs, w)),
                            ("ELECTRE I", electre_i(X, w, dirs)[0]),
                            ("PROMETHEE II", promethee_ii(X, w, dirs)),
                            ("MAUT", maut(X, w, dirs)),
                            ("MCDA-C", mcda_c(X, w, dirs)),
                            ("AHP-TOPSIS 2n", ahp_topsis_2n(X, w, dirs)[2])):
            if not np.array_equal(ranks(rapido[nome]), ranks(lento)):
                ok = False
    checar(ok, "100 universos × 9 métodos: rankings idênticos nos dois caminhos")


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


def main():
    print("=" * 78)
    print(" SUÍTE DE VERIFICAÇÃO MATEMÁTICA — Passada 1 da tripla-checagem")
    print(" MCDM Studio · ProfBru - Bruno Penedo © 2026")
    print("=" * 78)

    for teste in (teste_ahp_consistente, teste_ahp_reprova, teste_ahp_muitos_criterios,
                  teste_dematel, teste_dominancia, teste_topsis, teste_borda,
                  teste_orientar, teste_vikor, teste_todim, teste_electre_ii,
                  teste_sapevo, teste_copeland, teste_hibrido, teste_equivalencia,
                  teste_entradas_invalidas):
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
