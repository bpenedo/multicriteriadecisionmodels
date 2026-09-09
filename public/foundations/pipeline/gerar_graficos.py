"""
Gráficos da decisão multicritério — as cinco telas que sustentam o veredito.

  1. dematel_causa_efeito — proeminência (R+C) × relação (R−C). Acima da linha
     y=0 estão as CAUSAS (alavancas: aja aqui); abaixo, os EFEITOS (termômetros).
     O tamanho do círculo é o peso derivado por influência.
  2. mapa_metodos        — matriz alternativas × métodos com a posição de cada uma.
     Divergência entre escolas de decisão é INFORMAÇÃO, não ruído.
  3. robustez            — em quantos universos de preferência cada alternativa vence.
  4. distribuicao        — histograma completo das posições do consenso.
  5. pesos_dematel_ahp   — DEMATEL (influência sistêmica) × AHP (julgamento par a par).
     Onde as duas famílias de peso divergem é onde a decisão merece um humano.

Saída: evidence/static/mc/<caso>/*.png  e cópia em _private/foundations/telas/<caso>/

Uso:  python3 gerar_graficos.py [caso ...] [--workers N]

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import argparse
import shutil
from concurrent.futures import ProcessPoolExecutor

import matplotlib
matplotlib.use("Agg")                      # backend sem display: roda em servidor/screen
import matplotlib.pyplot as plt
import numpy as np

from casos import CATALOGO
from config import DPI_FIGURAS, N_WORKERS, STATIC_DIR, TELAS_DIR
from db import get_conn

CAUSA, EFEITO = "#c0392b", "#1f77b4"
# Mínimo de barras nos gráficos de robustez/distribuição — abaixo disso a figura
# fica curta demais para ser lida; acima, vira parede de zeros (bugs.md #BUG-021).
MIN_BARRAS_ROBUSTEZ = 15
COR_DEMATEL, COR_AHP = "#236aa4", "#f4b548"
plt.rcParams.update({"font.size": 10, "axes.titlesize": 12, "figure.autolayout": False})


def _encurtar(texto, limite=26):
    """Encurta preservando palavras inteiras, com reticências.

    O corte cru por `texto[:26]` produzia rótulos mutilados — "Instrutor convidado — dout",
    "Instrutor operacional sêni" — em que o leitor não distingue a alternativa truncada de
    outra com o mesmo prefixo. Cortar na fronteira da palavra e marcar a omissão com "…"
    diz ao leitor que há texto além, e o rótulo continua identificando a alternativa.
    """
    texto = texto.strip()
    if len(texto) <= limite:
        return texto
    corte = texto[:limite - 1]
    espaco = corte.rfind(" ")
    if espaco >= limite * 0.55:            # só vale se não amputar quase tudo
        corte = corte[:espaco]
    return corte.rstrip(" —-·,;:") + "…"


def _encurtar_lote(textos, limite=26, teto=44):
    """Encurta um conjunto de rótulos SEM torná-los ambíguos entre si.

    Encurtar cada rótulo isoladamente cria um defeito pior do que o que resolve: numa
    lista com "Instrutor sênior — doutorado" e "Instrutor sênior — mestrado", o corte na
    fronteira da palavra devolve "Instrutor sênior…" para os DOIS. O gráfico fica limpo e
    mentiroso — dois rótulos idênticos apontando para pontos diferentes, e o leitor sem
    como saber qual é qual. Rótulo mutilado ainda identifica; rótulo ambíguo, não.

    Aqui o limite é do CONJUNTO: enquanto houver colisão, ele sobe (de 4 em 4 caracteres)
    até desambiguar ou bater no teto. Quem não colide fica curto; só os rótulos que
    disputam prefixo pagam o preço da largura extra. Ver bugs.md #BUG-032.
    """
    textos = list(textos)
    for lim in range(limite, teto + 1, 4):
        curtos = [_encurtar(t, lim) for t in textos]
        # Ambíguo = mesmo rótulo curto para textos originais diferentes.
        por_curto = {}
        for original, curto in zip(textos, curtos):
            por_curto.setdefault(curto, set()).add(original)
        if all(len(v) == 1 for v in por_curto.values()):
            return curtos
    return textos            # desistimos de encurtar antes de desistir de distinguir


def _anotar_sem_colisao(ax, fig, pontos, candidatos=None, folga=3.0):
    """Posiciona rótulos com linha de chamada, sem corte nem sobreposição.

    `pontos` é uma sequência de (x, y, texto, cor). Para cada ponto, testa offsets
    candidatos, MEDE o retângulo real do rótulo com o renderer e escolhe o de menor
    custo — `choques × 1000 + transbordo` —, de modo que sobreposição pesa sempre
    mais que encostar na borda.

    Devolve `(choques_restantes, anotações)`. `choques_restantes > 0` significa que NÃO
    havia posição livre para algum rótulo e o algoritmo aceitou o menos ruim — o chamador
    deve então **reduzir o número de rótulos**, porque nenhuma busca resolve o caso em que
    o espaço simplesmente não comporta o conjunto (ver `_anotar_o_que_couber`).

    Existe como função compartilhada porque o mesmo defeito apareceu duas vezes em
    gráficos diferentes: primeiro no diagrama do DEMATEL (#BUG-013), depois na matriz
    BCG (#BUG-025). Nas duas, corrigir o corte na borda produziu sobreposição, e
    corrigir a sobreposição produziu rótulo duplicado. Resolver por distância entre
    centros não funciona: rótulos têm larguras muito diferentes.
    """
    if candidatos is None:
        # Anéis concêntricos: 8 direções × 4 raios = 32 posições candidatas.
        #
        # Doze candidatos bastavam para pontos espalhados, mas não para uma região
        # DENSA — nos carros elétricos, oito rótulos disputavam o mesmo canto superior
        # direito, TODOS os candidatos colidiam, e a função de custo aceitava "o menos
        # ruim", que ainda sobrepunha. Com raios maiores existe sempre uma saída para
        # fora do aglomerado. Ver bugs.md #BUG-026.
        import math
        candidatos = []
        for raio in (26, 46, 70, 96):
            for graus in (90, 45, 135, 0, 180, 315, 225, 270):
                rad = math.radians(graus)
                candidatos.append((round(raio * 1.7 * math.cos(rad)),
                                   round(raio * math.sin(rad))))
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    area = ax.get_window_extent(renderer)
    postos = []

    def _colide(a, b):
        return not (a.x1 + folga < b.x0 or b.x1 + folga < a.x0 or
                    a.y1 + folga < b.y0 or b.y1 + folga < a.y0)

    xs = [p[0] for p in pontos]
    meio = (max(xs) + min(xs)) / 2 if xs else 0
    choques_restantes, desenhados = 0, []
    for xi, yi, texto, cor_i in pontos:
        # Ponto na metade direita prefere rótulo à esquerda, e vice-versa.
        ordem = sorted(candidatos, key=lambda c: c[0] * (1 if xi > meio else -1))
        melhor, melhor_custo, melhor_fora = None, None, 0.0
        for dx, dy in ordem:
            ann = ax.annotate(texto, (xi, yi), xytext=(dx, dy),
                              textcoords="offset points", ha="center", va="center",
                              fontsize=8.5, fontweight="bold", color=cor_i, zorder=6,
                              bbox=dict(boxstyle="round,pad=0.26", fc="white",
                                        ec=cor_i, lw=0.9, alpha=0.96),
                              arrowprops=dict(arrowstyle="-", color=cor_i, lw=0.9,
                                              shrinkA=0, shrinkB=4))
            caixa = ann.get_window_extent(renderer)
            fora = max(0.0, area.x0 - caixa.x0) + max(0.0, caixa.x1 - area.x1) \
                 + max(0.0, area.y0 - caixa.y0) + max(0.0, caixa.y1 - area.y1)
            # Sobreposição (×1000) domina transbordo; a distância do ponto entra
            # como desempate leve, para não afastar o rótulo mais que o necessário.
            distancia = (dx * dx + dy * dy) ** 0.5
            custo = (sum(1 for c in postos if _colide(caixa, c)) * 1000
                     + fora * 10 + distancia * 0.05)
            if melhor_custo is None or custo < melhor_custo:
                melhor_fora = fora
            if custo == 0:
                melhor_fora = 0.0
                # Remove o melhor parcial ANTES de aceitar este, senão a anotação
                # descartada continua desenhada (rótulo duplicado, #BUG-013c).
                if melhor is not None and melhor is not ann:
                    melhor.remove()
                melhor = ann
                break
            if melhor_custo is None or custo < melhor_custo:
                if melhor is not None:
                    melhor.remove()
                melhor, melhor_custo = ann, custo
            else:
                ann.remove()
        if melhor is not None:
            postos.append(melhor.get_window_extent(renderer))
            desenhados.append(melhor)
            if (melhor_custo is not None and melhor_custo >= 1000) or melhor_fora > 0.5:
                choques_restantes += 1
    return choques_restantes, desenhados


def _anotar_o_que_couber(ax, fig, pontos, minimo=3):
    """Rotula o máximo de pontos que cabe SEM sobreposição, reduzindo se preciso.

    Em regiões densas — oito primeiras colocadas amontoadas no mesmo canto — não existe
    disposição sem choque, por maior que seja o espaço de busca. Insistir produz rótulos
    sobrepostos, que informam MENOS que rótulos a menos: um rótulo ilegível esconde dois.

    Tenta com todos, e vai cortando o último (a pior colocada, já que `pontos` chega
    ordenado por posição no consenso) até que nenhum rótulo colida. Devolve quantos
    foram efetivamente rotulados. Ver bugs.md #BUG-026.
    """
    for n in range(len(pontos), minimo - 1, -1):
        for ann in list(ax.texts):
            ann.remove()
        choques, _ = _anotar_sem_colisao(ax, fig, pontos[:n])
        if choques == 0:
            return n
    return minimo


def _salvar(fig, destino):
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino, dpi=DPI_FIGURAS, bbox_inches="tight",
                pad_inches=0.35, facecolor="white")
    plt.close(fig)
    return destino


# ---------------------------------------------------------------------------
def diagrama_causa_efeito(conn, id_caso, destino):
    linhas = conn.execute(
        "SELECT rotulo, prominencia, relacao, papel, peso FROM dematel_criterio "
        "WHERE id_caso = ? ORDER BY prominencia DESC", (id_caso,)).fetchall()
    if not linhas:
        return None
    x = np.array([r["prominencia"] for r in linhas])
    y = np.array([r["relacao"] for r in linhas])
    pesos = np.array([r["peso"] for r in linhas])
    cores = [CAUSA if r["papel"] == "causa" else EFEITO for r in linhas]

    fig, ax = plt.subplots(figsize=(9.6, 6.0))
    ax.axhline(0, color="black", lw=1.1, zorder=2)
    ax.scatter(x, y, s=pesos * 3600, c=cores, alpha=0.85,
               edgecolors="white", linewidths=1.4, zorder=3)

    # Rótulos SEMPRE fora do círculo, com linha de chamada.
    #
    # A MOLDURA VEM PRIMEIRO. Antes, os rótulos eram posicionados e medidos e só
    # depois `set_xlim`/`set_ylim` eram aplicados — ou seja, cada caixa era testada
    # contra uma área de eixos que ainda ia mudar, e a medição inteira era descartada
    # em silêncio. O rótulo do critério mais à direita saía cortado pela borda
    # ("...mprovada 14.2%") mesmo com o algoritmo de anticolisão funcionando: ele
    # acertava o alvo errado. Ver bugs.md #BUG-029.
    #
    # E usamos `_anotar_sem_colisao` em vez de uma cópia local: este gráfico manteve
    # sua própria versão com 12 candidatos por engano, enquanto a função compartilhada
    # — extraída no #BUG-025 justamente para acabar com a duplicação — já testava 32.
    # O DEMATEL nunca foi migrado. Ver bugs.md #BUG-030.
    faixa = max(abs(y).max(), 0.1) * 1.45
    margem = (x.max() - x.min()) * 0.30 or 0.5
    rotulos = [(xi, yi, f"{r['rotulo']}  {r['peso']*100:.1f}%", cores[i])
               for i, (r, xi, yi) in enumerate(zip(linhas, x, y))]

    # Nenhum critério pode ser omitido — num diagrama causal, um critério sem rótulo
    # é um critério que o decisor não vê. Então, em vez de reduzir a quantidade de
    # rótulos (o que a matriz BCG faz), ALARGAMOS a moldura até todos caberem.
    for _ in range(7):
        ax.set_ylim(-faixa, faixa)
        ax.set_xlim(x.min() - margem, x.max() + margem)
        for ann in list(ax.texts):
            ann.remove()
        pendencias, _ = _anotar_sem_colisao(ax, fig, rotulos)
        if pendencias == 0:
            break
        margem *= 1.30
        faixa *= 1.18

    # Faixas de fundo pintadas com o xlim JÁ definitivo: pintar sobre um limite que
    # ainda vai mudar desalinha o preenchimento. Ver bugs.md #BUG-010.
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    ax.fill_between(xlim, 0, ylim[1], color=CAUSA, alpha=0.05, zorder=0)
    ax.fill_between(xlim, ylim[0], 0, color=EFEITO, alpha=0.05, zorder=0)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    ax.text(0.985, 0.965, "CAUSAS — alavancas: aja aqui", transform=ax.transAxes,
            ha="right", fontsize=10, fontweight="bold", color=CAUSA)
    ax.text(0.985, 0.03, "EFEITOS — termômetros: resultado do que já foi decidido",
            transform=ax.transAxes, ha="right", fontsize=10, fontweight="bold", color=EFEITO)
    ax.set_xlabel("Proeminência  R + C  (importância no sistema)", fontsize=10.5)
    ax.set_ylabel("Relação  R − C  (causa ↑ / efeito ↓)", fontsize=10.5)
    nome = conn.execute("SELECT nome FROM caso WHERE id_caso = ?", (id_caso,)).fetchone()["nome"]
    ax.set_title(f"DEMATEL — estrutura causal dos critérios\n{nome}", fontweight="bold")
    ax.grid(alpha=0.25, linestyle=":")
    ax.set_axisbelow(True)
    return _salvar(fig, destino / "dematel_causa_efeito.png")


def mapa_metodos(conn, id_caso, destino):
    linhas = conn.execute(
        "SELECT m.alternativa, m.metodo, m.rank_, a.rotulo FROM decisao_mcdm m "
        "JOIN alternativa a ON a.id_caso = m.id_caso AND a.alternativa = m.alternativa "
        "WHERE m.id_caso = ?", (id_caso,)).fetchall()
    if not linhas:
        return None
    consenso = {r["alternativa"]: r["rank_final"] for r in conn.execute(
        "SELECT alternativa, rank_final FROM decisao_consenso WHERE id_caso = ?", (id_caso,))}
    rotulos = {r["alternativa"]: r["rotulo"] for r in linhas}

    metodos = sorted({r["metodo"] for r in linhas})
    alts = sorted(consenso, key=lambda a: consenso[a])
    M = np.full((len(alts), len(metodos) + 1), np.nan)
    for r in linhas:
        M[alts.index(r["alternativa"]), metodos.index(r["metodo"])] = r["rank_"]
    for a, pos in consenso.items():
        M[alts.index(a), -1] = pos

    cols = metodos + ["CONSENSO\n(Borda)"]
    fig, ax = plt.subplots(figsize=(1.6 * len(cols) + 3.6, 0.56 * len(alts) + 2.6))
    im = ax.imshow(M, cmap="RdYlGn_r", aspect="auto", vmin=1, vmax=len(alts))
    for i in range(len(alts)):
        for j in range(len(cols)):
            ax.text(j, i, f"{int(M[i, j])}º", ha="center", va="center", fontsize=10,
                    fontweight="bold" if j == len(cols) - 1 else "normal", color="black")
    ax.axvline(len(metodos) - 0.5, color="black", lw=2.2)
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, fontsize=9)
    ax.set_yticks(range(len(alts)))
    ax.set_yticklabels([rotulos.get(a, a) for a in alts], fontsize=9.5)
    ax.set_title("Posição por escola de decisão\n"
                 "verde = melhor · divergência entre métodos é informação, não ruído",
                 fontweight="bold")
    fig.colorbar(im, ax=ax, shrink=0.85, label="Posição (1º = melhor)")
    return _salvar(fig, destino / "mapa_metodos.png")


def grafico_robustez(conn, id_caso, destino):
    linhas = conn.execute(
        "SELECT r.alternativa, r.prob_vitoria, r.rank_p05, r.rank_p95, a.rotulo "
        "FROM mcdm_robustez r JOIN alternativa a "
        "  ON a.id_caso = r.id_caso AND a.alternativa = r.alternativa "
        "WHERE r.id_caso = ? AND r.metodo = 'CONSENSO (Borda)' "
        "ORDER BY r.prob_vitoria DESC", (id_caso,)).fetchall()
    if not linhas:
        return None
    ver = conn.execute("SELECT * FROM veredito WHERE id_caso = ?", (id_caso,)).fetchone()

    # Em casos grandes (30+ alternativas) a maioria vence em 0% dos universos, e
    # plotar todas produz uma figura altíssima onde 90% das barras são vazias —
    # ilegível justamente onde a decisão é mais difícil. Mostramos as que têm
    # chance real, mais uma margem de contexto, e declaramos quantas ficaram fora.
    # Ver bugs.md #BUG-021.
    com_chance = sum(1 for r in linhas if r["prob_vitoria"] >= 0.05)
    limite = max(com_chance + 3, MIN_BARRAS_ROBUSTEZ)
    omitidas = max(0, len(linhas) - limite)
    linhas = linhas[:limite]

    rot = [r["rotulo"] for r in linhas]
    prob = np.array([r["prob_vitoria"] for r in linhas])
    cor_classe = {"ROBUSTO": "#16a34a", "PROVÁVEL": "#f4b548", "FRÁGIL": "#dc2626"}
    cores = [cor_classe.get(ver["classificacao"], "#236aa4") if i == 0 else "#8dacbf"
             for i in range(len(rot))]

    fig, ax = plt.subplots(figsize=(9.6, 0.62 * len(rot) + 2.8))
    barras = ax.barh(range(len(rot)), prob, color=cores, edgecolor="white", height=0.68)
    for i, (b, p) in enumerate(zip(barras, prob)):
        if p >= 0.05:
            ax.text(b.get_width() + 1.2, b.get_y() + b.get_height() / 2,
                    f"{p:.1f}%", va="center", fontsize=9.5,
                    fontweight="bold" if i == 0 else "normal")
    ax.set_yticks(range(len(rot)))
    ax.set_yticklabels(rot, fontsize=9.5)
    ax.invert_yaxis()
    ax.set_xlim(0, max(105, prob.max() * 1.18))
    ax.set_xlabel("% dos universos de preferência em que vence o consenso", fontsize=10.5)
    ax.axvline(90, color="#16a34a", ls="--", lw=1, alpha=0.6)
    ax.axvline(60, color="#f4b548", ls="--", lw=1, alpha=0.6)
    ax.text(90, -0.75, "ROBUSTO ≥90%", color="#16a34a", fontsize=8.5, ha="center")
    ax.text(60, -0.75, "PROVÁVEL ≥60%", color="#d19a00", fontsize=8.5, ha="center")
    subtitulo = (f"veredito: {ver['classificacao']} "
                 f"({ver['prob_vitoria']:.1f}% para o 1º lugar)")
    if omitidas:
        subtitulo += f" · {omitidas} alternativas com 0% omitidas"
    ax.set_title(f"Robustez da decisão — {ver['n_alternativas']} alternativas, "
                 f"perturbação de Dirichlet nos pesos\n{subtitulo}", fontweight="bold")
    ax.grid(axis="x", alpha=0.25, linestyle=":")
    ax.set_axisbelow(True)
    return _salvar(fig, destino / "robustez.png")


def distribuicao_posicoes(conn, id_caso, destino):
    linhas = conn.execute(
        "SELECT d.alternativa, d.posicao, d.pct, a.rotulo FROM mcdm_robustez_dist d "
        "JOIN alternativa a ON a.id_caso = d.id_caso AND a.alternativa = d.alternativa "
        "WHERE d.id_caso = ?", (id_caso,)).fetchall()
    if not linhas:
        return None
    ordem = [r["alternativa"] for r in conn.execute(
        "SELECT alternativa FROM decisao_consenso WHERE id_caso = ? ORDER BY rank_final",
        (id_caso,))]
    rotulos = {r["alternativa"]: r["rotulo"] for r in linhas}
    # Mesma razão do gráfico de robustez: em caso grande, mostrar as primeiras
    # colocadas é o que informa; o resto vira uma parede de barras vermelhas.
    total_alt = len(ordem)
    ordem = ordem[:MIN_BARRAS_ROBUSTEZ]
    n = len(ordem)
    M = np.zeros((n, total_alt))
    for r in linhas:
        if r["alternativa"] in ordem:
            M[ordem.index(r["alternativa"]), r["posicao"] - 1] = r["pct"]

    fig, ax = plt.subplots(figsize=(9.6, 0.62 * n + 2.6))
    cores = plt.cm.RdYlGn_r(np.linspace(0.08, 0.92, total_alt))
    esquerda = np.zeros(n)
    for pos in range(total_alt):
        ax.barh(range(n), M[:, pos], left=esquerda, color=cores[pos],
                edgecolor="white", height=0.7, label=f"{pos+1}º")
        for i in range(n):
            if M[i, pos] >= 7:
                ax.text(esquerda[i] + M[i, pos] / 2, i, f"{M[i, pos]:.0f}%",
                        ha="center", va="center", fontsize=8.5, color="black")
        esquerda += M[:, pos]
    ax.set_yticks(range(n))
    ax.set_yticklabels([rotulos.get(a, a) for a in ordem], fontsize=9.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("% dos universos de preferência", fontsize=10.5)
    titulo = "Distribuição das posições no consenso"
    if total_alt > n:
        titulo += f" — {n} primeiras de {total_alt}"
    ax.set_title(f"{titulo}\n"
                 "uma barra inteiramente verde = posição que não depende dos pesos",
                 fontweight="bold")
    # Legenda só das posições que aparecem de fato — 38 entradas seriam ilegíveis.
    manipuladores, etiquetas = ax.get_legend_handles_labels()
    visiveis = [(h, e) for h, e, p in zip(manipuladores, etiquetas, range(total_alt))
                if M[:, p].max() >= 1.0][:12]
    if visiveis:
        ax.legend(*zip(*visiveis), title="Posição", bbox_to_anchor=(1.01, 1),
                  loc="upper left", fontsize=9)
    return _salvar(fig, destino / "distribuicao_posicoes.png")


def pesos_dematel_ahp(conn, id_caso, destino):
    linhas = conn.execute(
        "SELECT d.rotulo, d.peso AS p_dematel, h.peso AS p_ahp, h.cr, d.papel "
        "FROM dematel_criterio d JOIN ahp_peso h "
        "  ON h.id_caso = d.id_caso AND h.criterio = d.criterio "
        "WHERE d.id_caso = ? ORDER BY d.peso DESC", (id_caso,)).fetchall()
    if not linhas:
        return None
    rot = [r["rotulo"] for r in linhas]
    pd_ = np.array([r["p_dematel"] for r in linhas]) * 100
    pa = np.array([r["p_ahp"] for r in linhas]) * 100
    cr = linhas[0]["cr"]
    y = np.arange(len(rot))

    fig, ax = plt.subplots(figsize=(9.6, 0.66 * len(rot) + 2.8))
    ax.barh(y - 0.2, pd_, height=0.38, color=COR_DEMATEL, label="DEMATEL (influência sistêmica)")
    ax.barh(y + 0.2, pa, height=0.38, color=COR_AHP, label="AHP (julgamento par a par)")
    for i in range(len(rot)):
        ax.text(pd_[i] + 0.6, y[i] - 0.2, f"{pd_[i]:.1f}%", va="center", fontsize=8.5)
        ax.text(pa[i] + 0.6, y[i] + 0.2, f"{pa[i]:.1f}%", va="center", fontsize=8.5)
    div = int(np.argmax(np.abs(pd_ - pa)))
    ax.axhspan(div - 0.45, div + 0.45, color="#dc2626", alpha=0.08, zorder=0)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{r} {'▲' if l['papel']=='causa' else '▼'}"
                        for r, l in zip(rot, linhas)], fontsize=9.5)
    ax.invert_yaxis()
    ax.set_xlabel("Peso do critério (%)", fontsize=10.5)
    ax.set_title("Duas famílias de peso sobre o mesmo problema\n"
                 f"maior divergência: {rot[div]} "
                 f"({pd_[div]:.1f}% × {pa[div]:.1f}%) · AHP CR = {cr:.4f}"
                 + ("" if cr < 0.10 else "  ⚠️ INCONSISTENTE"), fontweight="bold")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(axis="x", alpha=0.25, linestyle=":")
    ax.set_axisbelow(True)
    return _salvar(fig, destino / "pesos_dematel_ahp.png")


def matriz_bcg(conn, id_caso, destino):
    """Matriz BCG: atratividade (Y) × posição de custo (X), 4 quadrantes.

    O tamanho do ponto é inversamente proporcional à posição no consenso — as
    primeiras colocadas aparecem maiores, de modo que o gráfico responde às duas
    perguntas ao mesmo tempo: *qual escolher* (tamanho) e *que tipo de aposta é*
    (quadrante).
    """
    linhas = conn.execute(
        "SELECT b.alternativa, b.atratividade, b.posicao, b.quadrante, b.rank_consenso, "
        "       b.corte_atratividade, b.corte_posicao, a.rotulo "
        "FROM bcg_quadrante b JOIN alternativa a "
        "  ON a.id_caso = b.id_caso AND a.alternativa = b.alternativa "
        "WHERE b.id_caso = ? ORDER BY b.rank_consenso", (id_caso,)).fetchall()
    if not linhas:
        return None
    nome = conn.execute("SELECT nome FROM caso WHERE id_caso = ?", (id_caso,)).fetchone()["nome"]

    cor = {"ESTRELA": "#16a34a", "VACA": "#2563eb",
           "INTERROGACAO": "#f4b548", "ABACAXI": "#dc2626"}
    emoji = {"ESTRELA": "ESTRELA", "VACA": "VACA LEITEIRA",
             "INTERROGACAO": "INTERROGAÇÃO", "ABACAXI": "ABACAXI"}
    x = np.array([r["posicao"] for r in linhas])
    y = np.array([r["atratividade"] for r in linhas])
    cx, cy = linhas[0]["corte_posicao"], linhas[0]["corte_atratividade"]
    n = len(linhas)
    tam = np.array([420 * (1 - 0.75 * ((r["rank_consenso"] or n) - 1) / max(n - 1, 1))
                    for r in linhas]) + 60

    fig, ax = plt.subplots(figsize=(11.0, 8.2))

    # A MOLDURA VEM ANTES DO FUNDO. Os quadrantes eram pintados com as constantes
    # -0.05 e 1.05 — que presumiam onde os eixos iriam parar — e só depois
    # `set_xlim`/`set_ylim` definiam os limites de verdade, calculados a partir da
    # amplitude dos dados. Quando a amplitude empurrava os limites além de ±0.05,
    # sobravam FAIXAS BRANCAS nas bordas, e o gráfico passava a insinuar uma região
    # "fora de quadrante" que não existe: na matriz BCG todo ponto está em algum
    # quadrante, por construção. Terceira ocorrência da mesma causa raiz (#BUG-010,
    # #BUG-029). Ver bugs.md #BUG-031.
    amp_x = max(x.max() - x.min(), 1e-6)
    amp_y = max(y.max() - y.min(), 1e-6)
    ax.set_xlim(min(x.min(), cx) - amp_x * 0.22, max(x.max(), cx) + amp_x * 0.22)
    ax.set_ylim(min(y.min(), cy) - amp_y * 0.10, max(y.max(), cy) + amp_y * 0.14)
    lx0, lx1 = ax.get_xlim()
    ly0, ly1 = ax.get_ylim()

    # Fundo dos quadrantes, agora nos limites REAIS do eixo.
    ax.axvspan(cx, lx1, ymin=0, ymax=1, color="#f8fafc", zorder=0)
    for (xa, xb, ya, yb, q) in ((cx, lx1, cy, ly1, "ESTRELA"),
                                (cx, lx1, ly0, cy, "VACA"),
                                (lx0, cx, cy, ly1, "INTERROGACAO"),
                                (lx0, cx, ly0, cy, "ABACAXI")):
        ax.add_patch(plt.Rectangle((xa, ya), xb - xa, yb - ya,
                                   color=cor[q], alpha=0.06, zorder=0))
    ax.axvline(cx, color="black", lw=1.2, ls="--", alpha=0.7, zorder=1)
    ax.axhline(cy, color="black", lw=1.2, ls="--", alpha=0.7, zorder=1)
    # `add_patch` pode reativar o autoscale e reabrir os limites — refixamos.
    ax.set_xlim(lx0, lx1)
    ax.set_ylim(ly0, ly1)

    for r, xi, yi, ti in zip(linhas, x, y, tam):
        ax.scatter(xi, yi, s=ti, c=cor[r["quadrante"]], alpha=0.80,
                   edgecolors="white", linewidths=1.3, zorder=3)
    # Rotula só as 8 primeiras do consenso — rotular 38 pontos é ilegível
    # (mesma razão do #BUG-021).
    # Margem PROPORCIONAL à amplitude de cada eixo, não fixa: com dados concentrados
    # (amplitude 0,1) uma folga de 0,06 é enorme, e com dados espalhados (amplitude 1,0)
    # é insuficiente para caber um rótulo de 26 caracteres. Ver bugs.md #BUG-013a/#BUG-025.
    x0, x1, y0, y1 = lx0, lx1, ly0, ly1
    for (px, py, ha, va, q) in ((x1, y1, "right", "top", "ESTRELA"),
                                (x1, y0, "right", "bottom", "VACA"),
                                (x0, y1, "left", "top", "INTERROGACAO"),
                                (x0, y0, "left", "bottom", "ABACAXI")):
        ax.text(px, py, emoji[q], ha=ha, va=va, fontsize=11, fontweight="bold",
                color=cor[q], alpha=0.85)

    ax.set_xlabel("Posição de custo  →  entrega mais por unidade de sacrifício", fontsize=10.5)
    ax.set_ylabel("Atratividade  →  desempenho nos critérios de benefício", fontsize=10.5)
    ax.set_title(f"Matriz BCG — {nome}\n"
                 "tamanho do ponto = posição no consenso (maior = melhor colocada)",
                 fontweight="bold")
    ax.grid(alpha=0.22, linestyle=":")
    ax.set_axisbelow(True)

    # Rotula as primeiras colocadas — no MÁXIMO 8 (38 seriam ilegíveis, #BUG-021) e no
    # máximo o que couber sem sobreposição, que em região densa costuma ser menos.
    primeiros = list(zip(linhas, x, y))[:8]
    nomes = _encurtar_lote(r["rotulo"] for r, _, _ in primeiros)
    rotulados = _anotar_o_que_couber(ax, fig, [
        (xi, yi, f"{r['rank_consenso']}º {nome}", cor[r["quadrante"]])
        for (r, xi, yi), nome in zip(primeiros, nomes)])
    if rotulados < len(linhas):
        ax.text(0.5, -0.105, f"rotuladas as {rotulados} primeiras colocadas de "
                             f"{len(linhas)} — as demais estão no gráfico sem rótulo",
                transform=ax.transAxes, ha="center", fontsize=8.5,
                color="#475569", style="italic")
    return _salvar(fig, destino / "matriz_bcg.png")


GERADORES = (diagrama_causa_efeito, mapa_metodos, grafico_robustez,
             distribuicao_posicoes, pesos_dematel_ahp, matriz_bcg)


def gerar_caso(id_caso):
    """Gera as 5 telas de um caso. Uma conexão por processo — SQLite não gosta
    de compartilhar conexão entre processos, e cada worker abre a sua."""
    conn = get_conn()
    destino = STATIC_DIR / id_caso
    try:
        feitos = [g(conn, id_caso, destino) for g in GERADORES]
    finally:
        conn.close()
    feitos = [f for f in feitos if f]

    # Espelha em _private/foundations/telas/ para uso nos READMEs.
    espelho = TELAS_DIR / id_caso
    espelho.mkdir(parents=True, exist_ok=True)
    for f in feitos:
        shutil.copy2(f, espelho / f.name)
    return id_caso, [f.name for f in feitos]


def main():
    ap = argparse.ArgumentParser(description="Gera as telas do MCDM Studio.")
    ap.add_argument("casos", nargs="*", help="ids de caso (vazio = todos)")
    ap.add_argument("--workers", type=int, default=N_WORKERS)
    args = ap.parse_args()
    alvos = args.casos or list(CATALOGO)

    # Cada caso é independente: paralelismo trivial por processo.
    if args.workers > 1 and len(alvos) > 1:
        with ProcessPoolExecutor(max_workers=min(args.workers, len(alvos))) as ex:
            resultados = list(ex.map(gerar_caso, alvos))
    else:
        resultados = [gerar_caso(c) for c in alvos]

    total = 0
    for id_caso, nomes in resultados:
        print(f"  🖼️  {id_caso}: {len(nomes)} telas → static/mc/{id_caso}/")
        total += len(nomes)
    print(f"\n✅ {total} gráficos gerados em {len(resultados)} caso(s).")
    print(f"   dashboard: {STATIC_DIR}")
    print(f"   READMEs:   {TELAS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
