"""
Robustez do ranking multicritério — perturbação de Dirichlet nos pesos.

O PROBLEMA
----------
Todo método MCDM devolve um vencedor com uma confiança implícita de 100%. Mas os
pesos dos critérios nunca são exatos — são estimativas de preferência. Se um
deslocamento de 2 pontos percentuais no peso de "autonomia" troca o 1º com o 2º
colocado, o "vencedor" é um artefato da calibração, não um fato do conjunto de
alternativas. Ninguém reporta isso; e é exatamente onde as decisões morrem no comitê.

A SOLUÇÃO
---------
Perturbamos os pesos e reranqueamos N vezes:

    w' ~ Dirichlet(κ · w)

A Dirichlet é a escolha natural: seu suporte é exatamente o simplex (pesos positivos
que somam 1), e ela satisfaz E[w'] = w — perturbamos SEM enviesar. O κ (concentração)
controla a dispersão: κ→∞ devolve os pesos originais; κ pequeno espalha.
Var(w'ᵢ) = wᵢ(1−wᵢ)/(κ+1), então κ=200 dá ≈ ±2,4 p.p. num peso de 13%.

O veredito deixa de ser "o Modelo C é o melhor" e passa a ser
"o Modelo C vence em 78% dos universos de preferência plausíveis" — um intervalo
de confiança sobre a PRÓPRIA DECISÃO. É o que separa uma recomendação defensável
de um palpite com verniz matemático.

PARALELISMO
-----------
Cada universo de preferência é independente dos demais: é paralelismo trivial e
CPU-bound puro. Conforme a política do projeto (foundations.md), usamos
ProcessPoolExecutor — não threads, que o GIL serializaria. O trabalho é dividido em
BLOCOS contíguos de iterações por worker: cada processo recebe (X, direções, w0,
semente, faixa) e devolve as matrizes de posição já agregadas, de modo que o custo
de pickle não engula o ganho.

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from config import (LIMIAR_TRABALHO_PARALELO, N_WORKERS, ROBUSTEZ_ITER,
                    ROBUSTEZ_KAPPA, SEED)
from nucleo import CONSENSO, METODOS, borda, preparar, ranks


# Problema pré-compilado, UM por processo. É preenchido pelo `initializer` do pool
# (ou diretamente pelo pai, no caminho serial). Preparar por BLOCO custava 16
# reconstruções do tensor de preferência — 19% do tempo total gasto recalculando
# exatamente os mesmos quantis. Ver bugs.md #BUG-012.
_PREP = None


def _preparar_processo(X, direcoes):
    """Inicializador do pool: pré-compila o problema uma vez por processo."""
    global _PREP
    _PREP = preparar(X, direcoes)


def _bloco(args):
    """Roda uma faixa de universos de preferência. Executado no processo-filho.

    Recebe e devolve apenas arrays NumPy e tipos primitivos — nada de conexão de
    banco, nada de closure. É o que torna a função serializável para o pool. O
    problema pré-compilado vem do estado do processo (`_PREP`), montado uma única
    vez pelo inicializador: o tensor de preferência é maior que a matriz de decisão,
    então é mais barato reconstruí-lo por processo do que enviá-lo por pickle a
    cada bloco.
    """
    w0, semente, n_iter, n_alt = args
    prep = _PREP
    if prep is None:                       # salvaguarda: processo sem inicializador
        raise RuntimeError("_PREP não inicializado — chame _preparar_processo antes")
    rng = np.random.default_rng(semente)
    chaves = METODOS + (CONSENSO,)
    posicoes = {m: np.empty((n_iter, n_alt), dtype=np.int64) for m in chaves}

    alpha = ROBUSTEZ_KAPPA * np.asarray(w0, dtype=np.float64)
    # Sorteia os pesos de uma vez: uma chamada vetorizada em vez de n_iter chamadas.
    W = rng.dirichlet(alpha, size=n_iter)
    matriz_rk = np.empty((len(METODOS), n_alt), dtype=np.int64)
    for i in range(n_iter):
        scores = prep.pontuar(W[i])
        for linha, metodo in enumerate(METODOS):
            rk = ranks(scores[metodo])
            posicoes[metodo][i] = rk
            matriz_rk[linha] = rk
        posicoes[CONSENSO][i] = ranks(borda(matriz_rk, n_alt))
    return posicoes


# Número FIXO de blocos lógicos. Deliberadamente independente de n_workers: se as
# sementes fossem derivadas por worker, mudar o nº de processos mudaria os fluxos
# aleatórios e o mesmo SEED devolveria probabilidades diferentes (medido: 74,7% em
# série contra 74,4% em 4 processos). Com blocos fixos, o executor apenas distribui
# um particionamento que já é determinístico. Ver bugs.md #BUG-011.
N_BLOCOS = 16


def _particionar(n_iter, semente_base, n_blocos=N_BLOCOS):
    """Divide n_iter em blocos contíguos determinísticos, com sementes distintas.

    Sementes derivadas de uma SeedSequence dão fluxos independentes E reprodutíveis:
    o mesmo SEED devolve exatamente o mesmo resultado com 1 ou com 32 processos —
    propriedade que nem `default_rng(seed + i)` nem o spawn por worker garantem.
    """
    n_blocos = max(1, min(n_blocos, n_iter))
    sementes = np.random.SeedSequence(semente_base).spawn(n_blocos)
    base, resto = divmod(n_iter, n_blocos)
    blocos, usado = [], 0
    for k in range(n_blocos):
        tamanho = base + (1 if k < resto else 0)
        if tamanho:
            blocos.append((sementes[k], tamanho))
            usado += tamanho
    assert usado == n_iter, f"particionamento perdeu iterações: {usado} != {n_iter}"
    return blocos


def simular(X, direcoes, w0, n_iter=ROBUSTEZ_ITER, n_workers=N_WORKERS, semente=SEED):
    """Reranqueia n_iter vezes com pesos perturbados.

    Devolve dict {método -> matriz (n_iter, n_alternativas) de posições}.
    Abaixo de LIMIAR_TRABALHO_PARALELO unidades de trabalho roda em série.
    """
    X = np.ascontiguousarray(X, dtype=np.float64)
    w0 = np.asarray(w0, dtype=np.float64)
    chaves = METODOS + (CONSENSO,)

    # Decide serial × paralelo pelo TRABALHO estimado, não pelo nº de iterações:
    # o custo de um universo cresce com m²·k. Paralelizar um problema pequeno é
    # mais lento que resolvê-lo (fork + pickle > cálculo).
    m, k = X.shape
    trabalho = n_iter * m * m * k
    # O particionamento é SEMPRE o mesmo; só muda quem executa cada bloco. É isso
    # que faz serial e paralelo devolverem resultados bit a bit idênticos.
    tarefas = [(w0, sem, tam, m)
               for sem, tam in _particionar(n_iter, semente)]

    if trabalho < LIMIAR_TRABALHO_PARALELO or n_workers <= 1:
        _preparar_processo(X, direcoes)                    # uma vez, neste processo
        parciais = [_bloco(t) for t in tarefas]
    else:
        with ProcessPoolExecutor(max_workers=min(n_workers, len(tarefas)),
                                 initializer=_preparar_processo,
                                 initargs=(X, direcoes)) as executor:
            parciais = list(executor.map(_bloco, tarefas))

    # Concatena na ORDEM das tarefas — preserva a reprodutibilidade.
    return {met: np.concatenate([p[met] for p in parciais], axis=0) for met in chaves}


def resumir(posicoes, alternativas):
    """Agrega as posições simuladas em estatísticas por (alternativa, método)."""
    linhas = []
    for metodo, M in posicoes.items():
        n_iter = M.shape[0]
        for j, alt in enumerate(alternativas):
            col = M[:, j]
            linhas.append({
                "alternativa": alt,
                "metodo": metodo,
                "prob_vitoria": float((col == 1).mean() * 100),
                "prob_top3": float((col <= 3).mean() * 100),
                "rank_medio": float(col.mean()),
                "rank_p05": float(np.percentile(col, 5)),
                "rank_p95": float(np.percentile(col, 95)),
                "n_iter": n_iter,
            })
    return linhas


def distribuicao_consenso(posicoes, alternativas):
    """Histograma completo das posições no consenso — alimenta o gráfico do dashboard."""
    C = posicoes[CONSENSO]
    n_iter, n_alt = C.shape
    linhas = []
    for j, alt in enumerate(alternativas):
        for pos in range(1, n_alt + 1):
            freq = int((C[:, j] == pos).sum())
            if freq:
                linhas.append({"alternativa": alt, "posicao": pos,
                               "frequencia": freq, "pct": freq / n_iter * 100})
    return linhas


def classificar(prob_lider: float) -> str:
    """Traduz a probabilidade de vitória do líder em veredito para o comitê.

    Os cortes são deliberadamente conservadores: abaixo de 60% o primeiro lugar
    é ruído de calibração, e o relatório PRECISA dizer isso em vez de exibir um
    troféu. É a diferença entre um sistema de apoio à decisão e um gerador de
    justificativa para a decisão que já se queria tomar.
    """
    if prob_lider >= 90:
        return "ROBUSTO"
    if prob_lider >= 60:
        return "PROVÁVEL"
    return "FRÁGIL"


DESCRICAO_VEREDITO = {
    "ROBUSTO":  "a escolha NÃO depende da calibração fina dos pesos — pode levar ao comitê.",
    "PROVÁVEL": "a escolha se sustenta na maioria dos cenários, mas o vice é competitivo — compare os dois.",
    "FRÁGIL":   "o 1º lugar é ARTEFATO DOS PESOS. Não decida só pelo ranking: volte ao decisor e recalibre os critérios.",
}


if __name__ == "__main__":
    import time
    rng = np.random.default_rng(7)
    X = rng.uniform(1, 100, (8, 6))
    direcoes = ["benefit", "benefit", "cost", "benefit", "cost", "benefit"]
    w0 = np.full(6, 1 / 6)
    alternativas = [f"Alt {chr(65+i)}" for i in range(8)]

    print(f"Regime PEQUENO (8 alternativas × 6 critérios) — o serial deve vencer:")
    for workers in (1, N_WORKERS):
        t0 = time.perf_counter()
        pos = simular(X, direcoes, w0, n_iter=2000, n_workers=workers)
        dt = time.perf_counter() - t0
        lider = max(resumir(pos, alternativas),
                    key=lambda r: (r["metodo"] == CONSENSO, r["prob_vitoria"]))
        print(f"  workers={workers:2d} · {dt:6.2f}s · líder={lider['alternativa']} "
              f"({lider['prob_vitoria']:.1f}%) · {classificar(lider['prob_vitoria'])}")

    print(f"\nRegime GRANDE (60 alternativas × 12 critérios) — o pool deve vencer:")
    Xg = rng.uniform(1, 100, (60, 12))
    dg = ["benefit" if i % 3 else "cost" for i in range(12)]
    wg = np.full(12, 1 / 12)
    altg = [f"Alt {i:02d}" for i in range(60)]
    for workers in (1, N_WORKERS):
        t0 = time.perf_counter()
        pos = simular(Xg, dg, wg, n_iter=2000, n_workers=workers)
        dt = time.perf_counter() - t0
        lider = max(resumir(pos, altg),
                    key=lambda r: (r["metodo"] == CONSENSO, r["prob_vitoria"]))
        print(f"  workers={workers:2d} · {dt:6.2f}s · líder={lider['alternativa']} "
              f"({lider['prob_vitoria']:.1f}%) · {classificar(lider['prob_vitoria'])}")
