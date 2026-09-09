"""
Orquestrador do pipeline MCDM: caso -> DEMATEL -> 5 métodos -> consenso -> robustez.

FLUXO
-----
    1. carrega o caso (matriz de decisão, matriz causal, matriz de Saaty)
    2. DEMATEL      -> estrutura causa/efeito + PESOS POR INFLUÊNCIA
    3. AHP          -> pesos por julgamento par a par + razão de consistência
    4. 5 métodos    -> ELECTRE I · PROMETHEE II · MAUT · MCDA-C · AHP-TOPSIS 2n
    5. Borda        -> consenso entre as escolas de decisão
    6. Dirichlet    -> robustez: em quantos universos de preferência o líder vence
    7. veredito     -> ROBUSTO / PROVÁVEL / FRÁGIL

Por que os pesos vêm do DEMATEL e não do AHP: o AHP pergunta ao decisor o quanto um
critério importa mais que outro, e o decisor responde olhando cada par isoladamente —
ignorando que "consumo" já está DENTRO de "autonomia". O DEMATEL mede a influência
sistêmica e devolve pesos que não contam a mesma coisa duas vezes. O AHP continua no
pipeline como CONTRAPONTO: se as duas famílias de peso elegem o mesmo vencedor, a
escolha é sólida; se divergem, a divergência é o achado.

Uso:
    python3 pipeline.py                    # todos os casos
    python3 pipeline.py smartphone         # um caso
    python3 pipeline.py --listar
    python3 pipeline.py --workers 8

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import argparse
import sys
import time

import numpy as np

from casos import CATALOGO, obter
from casos.catalogo import validar
from config import N_WORKERS, ROBUSTEZ_ITER, ROBUSTEZ_KAPPA, SEED, resumo
from db import carregar_caso, get_conn, init_schema
from nucleo import (CONSENSO, METODOS, ahp_consistente, ahp_topsis_2n, borda,
                    dematel, electre_i, pesos_ahp, preparar, ranks)
from robustez import (DESCRICAO_VEREDITO, classificar, distribuicao_consenso,
                      resumir, simular)


# ---------------------------------------------------------------------------
# Carga do caso no banco
# ---------------------------------------------------------------------------
def semear(conn, caso):
    """Grava a ESTRUTURA do caso (entrada) no banco. Idempotente."""
    validar(caso)
    id_caso = caso["id_caso"]
    cur = conn.cursor()

    # Limpa apenas este caso — outros casos no mesmo banco não são tocados.
    for tabela in ("avaliacao", "dematel_entrada", "ahp_entrada",
                   "alternativa", "criterio", "caso"):
        cur.execute(f"DELETE FROM {tabela} WHERE id_caso = ?", (id_caso,))

    cur.execute(
        "INSERT INTO caso (id_caso, nome, dominio, descricao, decisor) VALUES (?,?,?,?,?)",
        (id_caso, caso["nome"], caso["dominio"], caso["descricao"], caso["decisor"]))

    for i, (chave, rotulo) in enumerate(caso["alternativas"]):
        cur.execute(
            "INSERT INTO alternativa (id_caso, alternativa, rotulo, ordem) VALUES (?,?,?,?)",
            (id_caso, chave, rotulo, i))
    for j, (chave, rotulo, direcao, unidade) in enumerate(caso["criterios"]):
        cur.execute(
            "INSERT INTO criterio (id_caso, criterio, rotulo, direcao, unidade, ordem) "
            "VALUES (?,?,?,?,?,?)", (id_caso, chave, rotulo, direcao, unidade, j))

    chaves_alt = [a for a, _ in caso["alternativas"]]
    chaves_crit = [c for c, _, _, _ in caso["criterios"]]
    cur.executemany(
        "INSERT INTO avaliacao (id_caso, alternativa, criterio, valor) VALUES (?,?,?,?)",
        [(id_caso, chaves_alt[i], chaves_crit[j], float(caso["matriz"][i, j]))
         for i in range(len(chaves_alt)) for j in range(len(chaves_crit))])
    cur.executemany(
        "INSERT INTO dematel_entrada (id_caso, origem, destino, intensidade) VALUES (?,?,?,?)",
        [(id_caso, chaves_crit[i], chaves_crit[j], float(caso["dematel"][i, j]))
         for i in range(len(chaves_crit)) for j in range(len(chaves_crit))])
    cur.executemany(
        "INSERT INTO ahp_entrada (id_caso, linha, coluna, valor) VALUES (?,?,?,?)",
        [(id_caso, chaves_crit[i], chaves_crit[j], float(caso["ahp"][i, j]))
         for i in range(len(chaves_crit)) for j in range(len(chaves_crit))])
    conn.commit()


# ---------------------------------------------------------------------------
# Execução dos métodos
# ---------------------------------------------------------------------------
def executar(conn, id_caso, n_workers=N_WORKERS, n_iter=ROBUSTEZ_ITER, verboso=True):
    """Roda o pipeline completo de um caso e grava todos os resultados."""
    caso = obter(id_caso)
    alternativas, criterios, rotulos, direcoes, X = carregar_caso(conn, id_caso)
    rotulo_alt = dict(caso["alternativas"])
    cur = conn.cursor()
    n_alt = len(alternativas)

    for tabela in ("dematel_criterio", "dematel_relacao", "ahp_peso", "decisao_topsis",
                   "decisao_mcdm", "electre_nucleo", "decisao_consenso",
                   "mcdm_robustez", "mcdm_robustez_dist", "veredito"):
        cur.execute(f"DELETE FROM {tabela} WHERE id_caso = ?", (id_caso,))

    # --- 1) DEMATEL: estrutura causal + pesos por influência -----------------
    R, C, prom, rel, pesos, T, limiar = dematel(caso["dematel"])
    cur.executemany(
        "INSERT INTO dematel_criterio (id_caso, criterio, rotulo, r, c, prominencia, "
        "relacao, papel, peso) VALUES (?,?,?,?,?,?,?,?,?)",
        [(id_caso, criterios[i], rotulos[i], float(R[i]), float(C[i]), float(prom[i]),
          float(rel[i]), "causa" if rel[i] > 0 else "efeito", float(pesos[i]))
         for i in range(len(criterios))])
    cur.executemany(
        "INSERT INTO dematel_relacao (id_caso, origem, destino, intensidade, acima_limiar) "
        "VALUES (?,?,?,?,?)",
        [(id_caso, criterios[i], criterios[j], float(T[i, j]), int(T[i, j] > limiar))
         for i in range(len(criterios)) for j in range(len(criterios))])

    # --- 2) AHP: pesos por julgamento par a par (contraponto ao DEMATEL) -----
    w_ahp, cr, lmax = pesos_ahp(caso["ahp"])
    consistente = ahp_consistente(cr)
    cur.executemany(
        "INSERT INTO ahp_peso (id_caso, criterio, peso, cr, consistente) VALUES (?,?,?,?,?)",
        [(id_caso, criterios[j], float(w_ahp[j]), float(cr), int(consistente))
         for j in range(len(criterios))])

    # --- 3) Cinco métodos, todos com os pesos do DEMATEL ---------------------
    prep = preparar(X, direcoes)
    scores = prep.pontuar(pesos)
    posicoes = {m: ranks(s) for m, s in scores.items()}

    cur.executemany(
        "INSERT INTO decisao_mcdm (id_caso, alternativa, metodo, score, rank_) VALUES (?,?,?,?,?)",
        [(id_caso, alternativas[i], m, round(float(scores[m][i]), 6), int(posicoes[m][i]))
         for m in METODOS for i in range(n_alt)])

    # ELECTRE I: além do score, o NÚCLEO (quem não é dominado por ninguém).
    _, nucleo, S = electre_i(X, pesos, direcoes)
    cur.executemany(
        "INSERT INTO electre_nucleo (id_caso, alternativa, no_nucleo, domina, dominada) "
        "VALUES (?,?,?,?,?)",
        [(id_caso, alternativas[i], int(i in nucleo),
          int(S[i].sum()), int(S[:, i].sum())) for i in range(n_alt)])

    # AHP-TOPSIS 2n: as duas normalizações separadas (a coluna "concordante").
    ci_v, ci_m, ci_f = ahp_topsis_2n(X, pesos, direcoes)
    rk_v, rk_m, rk_f = ranks(ci_v), ranks(ci_m), ranks(ci_f)
    cur.executemany(
        "INSERT INTO decisao_topsis (id_caso, alternativa, ci_vector, ci_minmax, ci_final, "
        "rank_final, rank_vector, rank_minmax, concordante) VALUES (?,?,?,?,?,?,?,?,?)",
        [(id_caso, alternativas[i], round(float(ci_v[i]), 6), round(float(ci_m[i]), 6),
          round(float(ci_f[i]), 6), int(rk_f[i]), int(rk_v[i]), int(rk_m[i]),
          int(rk_v[i] == rk_m[i])) for i in range(n_alt)])

    # --- 4) Consenso de Borda ------------------------------------------------
    matriz_rk = np.array([posicoes[m] for m in METODOS], dtype=float)
    rank_medio = matriz_rk.mean(axis=0)
    pontos = borda(matriz_rk, n_alt)
    rank_final = ranks(pontos)
    unanime = (matriz_rk == matriz_rk[0]).all(axis=0)
    cur.executemany(
        "INSERT INTO decisao_consenso (id_caso, alternativa, rank_medio, borda, rank_final, "
        "unanime) VALUES (?,?,?,?,?,?)",
        [(id_caso, alternativas[i], round(float(rank_medio[i]), 3), int(pontos[i]),
          int(rank_final[i]), int(unanime[i])) for i in range(n_alt)])

    # --- 5) Robustez sob perturbação de Dirichlet ---------------------------
    t0 = time.perf_counter()
    pos_sim = simular(X, direcoes, pesos, n_iter=n_iter, n_workers=n_workers)
    dt = time.perf_counter() - t0

    linhas_rob = resumir(pos_sim, alternativas)
    cur.executemany(
        "INSERT INTO mcdm_robustez (id_caso, alternativa, metodo, prob_vitoria, prob_top3, "
        "rank_medio, rank_p05, rank_p95) VALUES (?,?,?,?,?,?,?,?)",
        [(id_caso, r["alternativa"], r["metodo"], r["prob_vitoria"], r["prob_top3"],
          r["rank_medio"], r["rank_p05"], r["rank_p95"]) for r in linhas_rob])
    cur.executemany(
        "INSERT INTO mcdm_robustez_dist (id_caso, alternativa, posicao, frequencia, pct) "
        "VALUES (?,?,?,?,?)",
        [(id_caso, r["alternativa"], r["posicao"], r["frequencia"], r["pct"])
         for r in distribuicao_consenso(pos_sim, alternativas)])

    # --- 6) Veredito ---------------------------------------------------------
    prob = {r["alternativa"]: r["prob_vitoria"]
            for r in linhas_rob if r["metodo"] == CONSENSO}
    ordem = sorted(alternativas, key=lambda a: -prob[a])
    vencedor, vice = ordem[0], (ordem[1] if len(ordem) > 1 else None)
    classe = classificar(prob[vencedor])
    cur.execute(
        "INSERT INTO veredito (id_caso, vencedor, prob_vitoria, classificacao, vice, "
        "prob_vice, n_metodos, n_alternativas, unanimidade) VALUES (?,?,?,?,?,?,?,?,?)",
        (id_caso, vencedor, prob[vencedor], classe, vice,
         prob[vice] if vice else None, len(METODOS), n_alt,
         float(unanime.mean() * 100)))
    conn.commit()

    if verboso:
        _relatorio(caso, alternativas, rotulo_alt, rotulos, criterios, pesos, w_ahp,
                   cr, consistente, rel, prom, limiar, posicoes, rank_final, nucleo,
                   prob, vencedor, vice, classe, unanime, dt, n_iter, X, direcoes)
    return {"vencedor": vencedor, "prob": prob[vencedor], "classe": classe,
            "segundos": dt}


# ---------------------------------------------------------------------------
# Relatório em texto (saída padrão do projeto: português-Brasil)
# ---------------------------------------------------------------------------
def _relatorio(caso, alternativas, rotulo_alt, rotulos, criterios, pesos, w_ahp, cr,
               consistente, rel, prom, limiar, posicoes, rank_final, nucleo, prob,
               vencedor, vice, classe, unanime, dt, n_iter, X, direcoes):
    largura = 100
    print("\n" + "═" * largura)
    print(f" {caso['nome'].upper()}")
    print(f" domínio: {caso['dominio']} · decisor: {caso['decisor']}")
    print("═" * largura)

    print(f"\n▸ DEMATEL — estrutura causal dos critérios (limiar α = {limiar:.4f})")
    print(f"  {'CRITÉRIO':<26} {'R+C':>8} {'R−C':>8}  {'PAPEL':<7} {'PESO':>8}")
    for i in np.argsort(-prom):
        papel = "CAUSA" if rel[i] > 0 else "efeito"
        print(f"  {rotulos[i]:<26} {prom[i]:8.3f} {rel[i]:+8.3f}  {papel:<7} {pesos[i]*100:7.2f}%")
    causas = [rotulos[i] for i in range(len(rotulos)) if rel[i] > 0]
    print(f"  ↳ alavancas (aja aqui): {', '.join(causas) or '(nenhuma)'}")

    print(f"\n▸ AHP — contraponto por julgamento par a par")
    print(f"  CR = {cr:.4f} " + ("✅ consistente (< 0,10)" if consistente
                                 else "⚠️  INCONSISTENTE — revise os julgamentos"))
    div = max(range(len(criterios)), key=lambda j: abs(w_ahp[j] - pesos[j]))
    print(f"  maior divergência DEMATEL×AHP: {rotulos[div]} "
          f"({pesos[div]*100:.1f}% vs {w_ahp[div]*100:.1f}%)")

    print(f"\n▸ RANKING POR ESCOLA DE DECISÃO ({len(METODOS)} métodos, {len(alternativas)} alternativas)")
    cab = f"  {'ALTERNATIVA':<32}" + "".join(f"{m:>16}" for m in METODOS) + f"{'CONSENSO':>11}"
    print(cab)
    print("  " + "─" * (len(cab) - 2))
    for i in np.argsort(rank_final):
        linha = f"  {rotulo_alt.get(alternativas[i], alternativas[i]):<32}"
        for m in METODOS:
            linha += f"{str(posicoes[m][i]) + 'º':>16}"
        marca = " ✓" if unanime[i] else ""
        print(linha + f"{str(rank_final[i]) + 'º':>11}{marca}")
    print(f"  ↳ ELECTRE I — núcleo (não dominadas): "
          f"{', '.join(rotulo_alt.get(alternativas[i], alternativas[i]) for i in nucleo) or '(vazio)'}")
    print(f"  ↳ unanimidade entre métodos: {int(unanime.sum())}/{len(alternativas)} alternativas")

    print(f"\n▸ ROBUSTEZ — {n_iter:,} universos de preferência, κ={ROBUSTEZ_KAPPA:g} ({dt:.2f}s)")
    dp = np.sqrt(0.13 * 0.87 / (ROBUSTEZ_KAPPA + 1)) * 100
    print(f"  perturbação w' ~ Dirichlet(κ·w) — desvio de ±{dp:.2f} p.p. num peso de 13%")
    for a in sorted(alternativas, key=lambda a: -prob[a]):
        if prob[a] < 0.05:
            continue
        barra = "█" * int(prob[a] / 2)
        print(f"  {rotulo_alt.get(a, a):<32} {prob[a]:5.1f}%  {barra}")

    print(f"\n{'─' * largura}")
    print(f" 🏆 VENCEDOR: {rotulo_alt.get(vencedor, vencedor)}")
    print(f"    vence em {prob[vencedor]:.1f}% dos universos de preferência plausíveis")
    print(f"    veredito {classe} — {DESCRICAO_VEREDITO[classe]}")
    if vice and prob[vice] >= 5:
        print(f"    vice: {rotulo_alt.get(vice, vice)} ({prob[vice]:.1f}%)")
    print("─" * largura)


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Pipeline de decisão multicritério (MCDM Studio).")
    ap.add_argument("casos", nargs="*", help="ids de caso (vazio = todos)")
    ap.add_argument("--listar", action="store_true", help="lista os casos disponíveis")
    ap.add_argument("--workers", type=int, default=N_WORKERS, help="processos paralelos")
    ap.add_argument("--iter", type=int, default=ROBUSTEZ_ITER, help="universos de preferência")
    ap.add_argument("--silencioso", action="store_true", help="só o resumo final")
    args = ap.parse_args()

    if args.listar:
        print(f"{'ID':<20} {'DOMÍNIO':<12} {'ALT':>4} {'CRIT':>5}  NOME")
        print("-" * 100)
        from casos import listar
        for id_caso, nome, dominio, n_a, n_c in listar():
            print(f"{id_caso:<20} {dominio:<12} {n_a:>4} {n_c:>5}  {nome}")
        return 0

    alvos = args.casos or list(CATALOGO)
    desconhecidos = [c for c in alvos if c not in CATALOGO]
    if desconhecidos:
        print(f"❌ caso(s) desconhecido(s): {', '.join(desconhecidos)}", file=sys.stderr)
        print(f"   disponíveis: {', '.join(CATALOGO)}", file=sys.stderr)
        return 1

    print(resumo())
    init_schema(silencioso=True)
    conn = get_conn()
    resultados = {}
    try:
        for id_caso in alvos:
            semear(conn, obter(id_caso))
            resultados[id_caso] = executar(
                conn, id_caso, n_workers=args.workers, n_iter=args.iter,
                verboso=not args.silencioso)
    finally:
        conn.close()

    print(f"\n{'═' * 100}")
    print(f" RESUMO — {len(resultados)} caso(s)")
    print(f"{'═' * 100}")
    print(f" {'CASO':<20} {'VENCEDOR':<34} {'CONFIANÇA':>10} {'VEREDITO':>10} {'TEMPO':>8}")
    for id_caso, r in resultados.items():
        rotulo = dict(obter(id_caso)["alternativas"]).get(r["vencedor"], r["vencedor"])
        print(f" {id_caso:<20} {rotulo:<34} {r['prob']:9.1f}% {r['classe']:>10} {r['segundos']:7.2f}s")
    fragil = [c for c, r in resultados.items() if r["classe"] == "FRÁGIL"]
    if fragil:
        print(f"\n ⚠️  {len(fragil)} caso(s) com veredito FRÁGIL: {', '.join(fragil)}")
        print("    O 1º lugar ali é artefato dos pesos — leve ao decisor antes de decidir.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
