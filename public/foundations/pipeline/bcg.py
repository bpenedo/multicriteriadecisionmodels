"""
Matriz BCG — ranqueamento por quadrante das oportunidades de cada categoria.

⚠️  PROCEDÊNCIA
--------------
O framework de referência (Framework_VPL_ProjetosIA) **cita** a BCG na documentação
(`foundations/admtools/ferramentas_administrativas.md`) e no texto do dashboard, mas
**não a implementa** — `gerar_admtools.py` traz SWOT, PESTELC, 5W4H, Pareto, GUT e
Radar, e nenhuma função BCG. Esta implementação é original deste projeto, seguindo a
metodologia clássica.

Método: Boston Consulting Group (Bruce Henderson, 1970).

O QUE A BCG ACRESCENTA AO MOTOR MCDM
------------------------------------
O consenso MCDM devolve uma ORDENAÇÃO: 1º, 2º, 3º. Isso responde "qual escolher",
mas não responde "que tipo de aposta é cada uma". Duas alternativas em 2º e 3º lugar
podem ser coisas completamente diferentes: uma barata e competente (colher agora),
outra cara e excepcional (investir para dominar).

A BCG responde a essa segunda pergunta cruzando dois eixos:

    ATRATIVIDADE (eixo Y, "crescimento do mercado")
        → o desempenho da alternativa nos critérios de BENEFÍCIO
    POSIÇÃO COMPETITIVA (eixo X, "participação relativa")
        → a vantagem da alternativa nos critérios de CUSTO, isto é, sua
          eficiência: quanto entrega por unidade de sacrifício

Os quatro quadrantes, na leitura de decisão de compra/investimento:

    ⭐ ESTRELA          alta atratividade + boa posição de custo
                        → a aposta natural; investir e padronizar
    🐄 VACA LEITEIRA    baixa atratividade + boa posição de custo
                        → colher: entrega o essencial pelo menor sacrifício
    ❓ INTERROGAÇÃO     alta atratividade + má posição de custo
                        → decisão de investimento: vale o prêmio pago?
    🐕 ABACAXI          baixa atratividade + má posição de custo
                        → descartar; nem entrega, nem é barata

O cruzamento com o ranking MCDM é onde mora o achado: um 2º colocado que é VACA
LEITEIRA costuma ser a escolha real de quem tem orçamento apertado, enquanto um 2º
colocado INTERROGAÇÃO só se justifica se o prêmio de desempenho for necessário.

Uso:  python3 bcg.py [caso ...]

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import argparse
import sys

import numpy as np

from casos import CATALOGO, obter
from config import ENCODING  # noqa: F401  (mantém a política de encoding explícita)
from db import carregar_caso, get_conn, init_schema
from nucleo import dematel, orientar

# Rótulos e cores dos quadrantes (mesma paleta do dashboard).
QUADRANTES = {
    "ESTRELA":      ("⭐", "#16a34a", "investir e padronizar"),
    "VACA":         ("🐄", "#2563eb", "colher — melhor entrega por unidade de sacrifício"),
    "INTERROGACAO": ("❓", "#f4b548", "decisão de investimento: o prêmio se justifica?"),
    "ABACAXI":      ("🐕", "#dc2626", "descartar — nem entrega, nem é barata"),
}


def classificar_quadrante(atratividade, posicao, corte_a, corte_p):
    """Quadrante BCG de uma alternativa, dados os cortes dos dois eixos."""
    alta_a = atratividade >= corte_a
    boa_p = posicao >= corte_p
    if alta_a and boa_p:
        return "ESTRELA"
    if alta_a and not boa_p:
        return "INTERROGACAO"
    if not alta_a and boa_p:
        return "VACA"
    return "ABACAXI"


def calcular(X, direcoes, pesos, corte="mediana"):
    """Eixos da BCG a partir da matriz de decisão e dos pesos do DEMATEL.

    Devolve (atratividade, posicao, corte_a, corte_p, quadrantes).

    ATRATIVIDADE = média ponderada do desempenho nos critérios de BENEFÍCIO.
    POSIÇÃO      = média ponderada do desempenho nos critérios de CUSTO (já
                   orientados, de modo que "maior" significa "mais barato/leve/
                   rápido de manter" — ou seja, melhor posição de custo).

    Os dois eixos usam os MESMOS pesos derivados do DEMATEL que alimentam os nove
    métodos, cada um renormalizado dentro do seu grupo. Isso é o que mantém a BCG
    coerente com o ranking: não é uma segunda modelagem, é um segundo corte da
    mesma modelagem.

    O corte dos eixos é a MEDIANA de cada um (não o ponto médio 0,5): a mediana
    divide o conjunto em duas metades reais, enquanto 0,5 pode deixar um quadrante
    vazio quando o conjunto é assimétrico — e quadrante vazio não informa nada.
    """
    G = orientar(X, direcoes)
    pesos = np.asarray(pesos, dtype=np.float64)
    beneficio = np.array([d == "benefit" for d in direcoes])
    custo = ~beneficio

    if not beneficio.any() or not custo.any():
        raise ValueError(
            "BCG exige critérios de benefício E de custo: os dois eixos saem "
            f"desses grupos (benefício={int(beneficio.sum())}, custo={int(custo.sum())})")

    w_b = pesos[beneficio] / pesos[beneficio].sum()
    w_c = pesos[custo] / pesos[custo].sum()
    atratividade = G[:, beneficio] @ w_b
    posicao = G[:, custo] @ w_c

    if corte == "mediana":
        corte_a, corte_p = float(np.median(atratividade)), float(np.median(posicao))
    elif corte == "media":
        corte_a, corte_p = float(atratividade.mean()), float(posicao.mean())
    elif corte == "central":
        corte_a = corte_p = 0.5
    else:
        raise ValueError(f"corte desconhecido: {corte!r} (use mediana|media|central)")

    quadrantes = [classificar_quadrante(a, p, corte_a, corte_p)
                  for a, p in zip(atratividade, posicao)]
    return atratividade, posicao, corte_a, corte_p, quadrantes


def processar(conn, id_caso, verboso=True):
    """Calcula a BCG de um caso e grava em `bcg_quadrante`."""
    caso = obter(id_caso)
    alternativas, criterios, rotulos, direcoes, X = carregar_caso(conn, id_caso)
    rotulo_alt = dict(caso["alternativas"])
    *_, pesos, _T, _lim = dematel(caso["dematel"])

    atr, pos, corte_a, corte_p, quad = calcular(X, direcoes, pesos)

    # Posição no consenso MCDM, para o cruzamento ranking × quadrante.
    rank = {r["alternativa"]: r["rank_final"] for r in conn.execute(
        "SELECT alternativa, rank_final FROM decisao_consenso WHERE id_caso = ?", (id_caso,))}

    cur = conn.cursor()
    cur.execute("DELETE FROM bcg_quadrante WHERE id_caso = ?", (id_caso,))
    cur.executemany(
        "INSERT INTO bcg_quadrante (id_caso, alternativa, atratividade, posicao, "
        "quadrante, corte_atratividade, corte_posicao, rank_consenso) VALUES (?,?,?,?,?,?,?,?)",
        [(id_caso, alternativas[i], float(atr[i]), float(pos[i]), quad[i],
          corte_a, corte_p, rank.get(alternativas[i]))
         for i in range(len(alternativas))])
    conn.commit()

    if verboso:
        print(f"\n{'═' * 92}")
        print(f" MATRIZ BCG — {caso['nome']}")
        print(f" cortes: atratividade ≥ {corte_a:.3f} · posição de custo ≥ {corte_p:.3f} (medianas)")
        print(f"{'═' * 92}")
        contagem = {q: quad.count(q) for q in QUADRANTES}
        print("  " + " · ".join(f"{QUADRANTES[q][0]} {q.title()}: {n}"
                                for q, n in contagem.items()))
        for q in ("ESTRELA", "VACA", "INTERROGACAO", "ABACAXI"):
            membros = [i for i in range(len(alternativas)) if quad[i] == q]
            if not membros:
                continue
            emoji, _cor, acao = QUADRANTES[q]
            print(f"\n  {emoji} {q.title()} — {acao}")
            membros.sort(key=lambda i: -(atr[i] + pos[i]))
            for i in membros[:8]:
                r = rank.get(alternativas[i])
                print(f"     {rotulo_alt.get(alternativas[i], alternativas[i])[:38]:<38} "
                      f"atrat={atr[i]:.3f}  custo={pos[i]:.3f}  "
                      f"{'consenso ' + str(r) + 'º' if r else ''}")
            if len(membros) > 8:
                print(f"     ... e mais {len(membros) - 8}")

        # O achado: o 1º do consenso caiu em que quadrante?
        vencedor = min(rank, key=rank.get) if rank else None
        if vencedor:
            iv = alternativas.index(vencedor)
            emoji, _c, acao = QUADRANTES[quad[iv]]
            print(f"\n  ▸ O 1º do consenso ({rotulo_alt.get(vencedor, vencedor)}) é "
                  f"{emoji} {quad[iv].title()} — {acao}")
            vacas = [i for i in range(len(alternativas))
                     if quad[i] == "VACA" and rank.get(alternativas[i], 99) <= 5]
            if vacas and quad[iv] != "VACA":
                melhor = min(vacas, key=lambda i: rank.get(alternativas[i], 99))
                print(f"    Alternativa de orçamento: "
                      f"{rotulo_alt.get(alternativas[melhor], alternativas[melhor])} "
                      f"(🐄 Vaca leiteira, {rank[alternativas[melhor]]}º no consenso) — "
                      f"entrega mais por unidade de sacrifício.")
    return {q: quad.count(q) for q in QUADRANTES}


def main():
    ap = argparse.ArgumentParser(description="Matriz BCG por categoria (MCDM Studio).")
    ap.add_argument("casos", nargs="*", help="ids de caso (vazio = todos)")
    ap.add_argument("--silencioso", action="store_true")
    args = ap.parse_args()

    init_schema(silencioso=True)
    conn = get_conn()
    alvos = args.casos or list(CATALOGO)
    desconhecidos = [c for c in alvos if c not in CATALOGO]
    if desconhecidos:
        print(f"❌ caso(s) desconhecido(s): {', '.join(desconhecidos)}", file=sys.stderr)
        return 1

    resumo = {}
    try:
        for id_caso in alvos:
            try:
                resumo[id_caso] = processar(conn, id_caso, verboso=not args.silencioso)
            except ValueError as erro:
                print(f"⚠️  {id_caso}: {erro}")
    finally:
        conn.close()

    print(f"\n{'═' * 92}")
    print(f" RESUMO BCG — {len(resumo)} caso(s)")
    print(f"{'═' * 92}")
    print(f" {'CASO':<36} {'⭐':>4} {'🐄':>4} {'❓':>4} {'🐕':>4}")
    for id_caso, c in resumo.items():
        print(f" {id_caso:<36} {c['ESTRELA']:>4} {c['VACA']:>4} "
              f"{c['INTERROGACAO']:>4} {c['ABACAXI']:>4}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
