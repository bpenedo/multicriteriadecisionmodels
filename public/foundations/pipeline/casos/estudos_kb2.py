"""
Estudos de caso derivados de `kb/Artigos e Teses/Novos2/` e
`kb/Artigos e Teses/Outros e Criptoativos/` — segunda leva.

═══════════════════════════════════════════════════════════════════════════════
 PROCEDÊNCIA — cada caso reproduz a ESTRUTURA DE DECISÃO (critérios, direções,
 relações causais) de um trabalho específico do acervo. A autoria dos estudos é
 dos autores citados; deste projeto é a implementação e a integração ao motor.
═══════════════════════════════════════════════════════════════════════════════

SOBRE OS NÚMEROS — e a diferença em relação ao módulo `estudos_kb.py`:

    · `portfolio_crise` REPRODUZ a matriz de decisão publicada por Costa et al.
      (2021), Tabela 1 — são dados factuais de mercado coletados pelos autores em
      14/07/2020, citados com atribuição integral. Replicar o estudo é o ponto.
    · `cripto_portfolio` REPRODUZ os pesos AHP publicados por Aljinović et al.
      (2021), Tabela 3 (elicitados com doze especialistas, inconsistência 0,02).
      A matriz de avaliação é instanciação própria, com ordens de grandeza do
      período estudado (jan/2017–fev/2020).
    · Nos demais, a matriz é instanciação própria; o que é fiel é a MODELAGEM.

Cada caso declara isso na sua descrição. Onde o dado é do autor, está dito.

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import numpy as np

from casos.catalogo import _saaty


def _saaty_de_pesos(pesos):
    """Matriz de Saaty a partir de um vetor de pesos JÁ CONHECIDO: a_ij = w_i / w_j.

    Existe para os casos em que o trabalho de origem PUBLICA os pesos elicitados.
    Reconstruir a matriz par a par a partir deles devolve exatamente aqueles pesos
    no autovetor principal, com CR = 0 por construção — o que é honesto: a
    inconsistência era dos especialistas do estudo, não nossa, e inventar uma
    perturbação para simulá-la seria fabricar dado que não temos.

    O alternativo — `_saaty(ordem)` — só preserva a ORDEM de importância e descarta
    a magnitude. Quando o artigo dá 0,321 contra 0,035, a magnitude é o achado.
    """
    w = np.asarray(pesos, dtype=float)
    if w.ndim != 1 or (w <= 0).any():
        raise ValueError("pesos devem ser um vetor positivo")
    w = w / w.sum()
    return w[:, None] / w[None, :]


# ===========================================================================
# 1. PORTFÓLIO DE CRIPTOATIVOS — PROMETHEE II
# Fonte: ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. "Cryptocurrency Portfolio
#        Selection — A Multicriteria Approach". Mathematics, 9(14):1677, 2021.
#        Faculty of Economics, Business and Tourism, University of Split.
#        [Cryptocurrency_Portfolio_Selection-A_Multicriteria.pdf]
# Critérios e PESOS AHP reproduzidos da Tabela 3 do artigo (12 especialistas,
# inconsistência 0,02). Alternativas: as nove criptomoedas do estudo.
# ===========================================================================
CRIPTO = {
    "id_caso": "cripto_portfolio",
    "nome": "Seleção de portfólio de criptoativos",
    "dominio": "financeiro",
    "decisor": "Gestor de carteira / investidor em ativos digitais",
    "descricao": (
        "As nove criptomoedas do estudo de origem, avaliadas pelos sete critérios que "
        "os autores defendem contra a prática dominante de reduzir cripto a **retorno e "
        "risco**. O achado que sustenta o artigo está nos pesos: doze especialistas "
        "colocaram **32,1% em VaR** — mais que no retorno esperado (20,8%) — e apenas "
        "3,5% em atratividade. Somados, os três critérios de perda (VaR, CVaR, desvio) "
        "pesam **64,5%**. Quem compra cripto olhando rentabilidade está usando um quinto "
        "do modelo. Os pesos AHP aqui são os publicados na Tabela 3, não estimados."),
    "criterios": [
        ("retorno",     "Retorno diário médio",        "benefit", "%"),
        ("desvio",      "Desvio padrão",               "cost",    "%"),
        ("var",         "Value-at-Risk (95%)",         "cost",    "%"),
        ("cvar",        "Conditional VaR (95%)",       "cost",    "%"),
        ("volume",      "Volume médio negociado",      "benefit", "US$ mi/dia"),
        ("mcap",        "Capitalização de mercado",    "benefit", "US$ bi"),
        ("atratividade", "Atratividade (menções)",     "benefit", "mil/dia"),
    ],
    "alternativas": [
        ("BTC", "Bitcoin"), ("ETH", "Ethereum"), ("XRP", "Ripple"),
        ("LTC", "Litecoin"), ("ETC", "Ethereum Classic"), ("XMR", "Monero"),
        ("DASH", "Dash"), ("NEO", "Neo"), ("XLM", "Stellar"),
    ],
    "matriz": np.array([
        # retorno desvio  VaR   CVaR   volume  mcap  atrat.
        [ 0.252,  4.18,  6.30,  9.40, 18500.0, 165.0, 42.0],  # Bitcoin
        [ 0.238,  5.46,  8.35, 12.10,  8200.0,  48.0, 21.0],  # Ethereum
        [ 0.196,  6.72, 10.10, 15.30,  2100.0,  16.5,  9.4],  # Ripple
        [ 0.214,  6.05,  9.20, 13.60,  3400.0,   4.8,  7.2],  # Litecoin
        [ 0.168,  6.94, 10.60, 15.90,   980.0,   1.4,  2.6],  # Ethereum Classic
        [ 0.205,  5.88,  8.90, 13.20,   310.0,   1.6,  3.1],  # Monero
        [ 0.152,  6.41,  9.80, 14.70,   240.0,   1.1,  1.8],  # Dash
        [ 0.221,  7.85, 11.90, 17.80,   620.0,   1.9,  4.5],  # Neo
        [ 0.183,  7.12, 10.90, 16.40,   410.0,   1.7,  3.8],  # Stellar
    ], dtype=float),
    # Estrutura causal: capitalização e volume são as CAUSAS estruturais — governam
    # liquidez e, por ela, a magnitude das perdas de cauda. Atratividade é EFEITO:
    # o interesse segue o preço, não o contrário.
    "dematel": np.array([
        #    ret desv VaR CVaR vol mcap atr
        [0, 2, 2, 2, 1, 1, 2],   # retorno
        [2, 0, 4, 4, 1, 0, 1],   # desvio -> dita VaR e CVaR
        [1, 3, 0, 4, 1, 0, 1],   # VaR
        [1, 3, 4, 0, 1, 0, 1],   # CVaR
        [2, 3, 3, 3, 0, 3, 2],   # volume -> CAUSA (liquidez amortece a cauda)
        [2, 3, 3, 3, 4, 0, 3],   # capitalização -> CAUSA RAIZ
        [2, 2, 1, 1, 3, 2, 0],   # atratividade -> EFEITO do preço
    ], dtype=float),
    # Pesos EXATOS do artigo (Tabela 3): μ .208 · σ .141 · VaR .321 · CVaR .183
    #                                    · MVlm .057 · MMC .055 · MoT .035
    "ahp": _saaty_de_pesos([0.208, 0.141, 0.321, 0.183, 0.057, 0.055, 0.035]),
}

# ===========================================================================
# 2. PORTFÓLIO EM PERÍODO DE CRISE — SAPEVO-M
# Fonte: COSTA, I. P. A.; MAÊDA, S. M. N.; TEIXEIRA, L. F. H. S. B.;
#        GOMES, C. F. S.; SANTOS, M. "Finanças em períodos de crise: aplicação do
#        método SAPEVO-M para composição de portfólios de investimentos".
#        Pesquisa Operacional para o Desenvolvimento, v.13, e13004, p.1-17, 2021.
#        UFF · CASNAV · IME.
#        [FINANÇAS EM PERÍODOS DE CRISE_....pdf]
# ⚠️  A MATRIZ ABAIXO É A TABELA 1 DO ARTIGO — dados de mercado coletados pelos
#     autores em 14/07/2020 junto a corretora, reproduzidos com atribuição.
# ===========================================================================
PORTFOLIO_CRISE = {
    "id_caso": "portfolio_crise",
    "nome": "Composição de portfólio em período de crise",
    "dominio": "financeiro",
    "decisor": "Investidor pessoa física (doze decisores, perfis distintos)",
    "descricao": (
        "Os oito investimentos de renda fixa e variável analisados pelos autores em "
        "plena crise da COVID-19, com **os dados publicados no artigo** (Tabela 1, "
        "coletados em 14/07/2020). O caso existe para mostrar o que a crise faz com a "
        "fronteira risco-retorno: o Tesouro Selic rende 0,40% em doze meses e o fundo "
        "de ações 12,80% — trinta e duas vezes mais — mas com volatilidade de 29,77% "
        "contra 4%. Nenhum critério isolado decide; e o método existe porque **liquidez "
        "e rentabilidade se opõem** justamente quando o investidor mais precisa das duas."),
    "criterios": [
        ("rentabilidade", "Rentabilidade (12 meses)",  "benefit", "%"),
        ("volatilidade",  "Volatilidade (12 meses)",   "cost",    "%"),
        ("risco",         "Risco declarado",           "cost",    "1-5"),
        ("liquidez",      "Prazo de resgate",          "cost",    "dias"),
    ],
    "alternativas": [
        ("TS",   "Tesouro Selic"), ("CDB", "CDB prefixado"), ("LCA", "LCA"),
        ("DEB",  "Debêntures (IPCA+5%)"), ("FMM", "Fundos multimercado"),
        ("FII",  "Fundos imobiliários"), ("FCB", "Fundo cambial (dólar)"),
        ("FAC",  "Fundo de ações"),
    ],
    # Tabela 1 de Costa et al. (2021). Risco: Muito Baixo=1 ... Muito Alto=5.
    # Liquidez: D+n em dias; "Vencimento" tratado como 365 (carência até o termo).
    "matriz": np.array([
        # rentab.  volat.  risco  liquidez
        [ 0.40,  4.00, 2, 1],      # Tesouro Selic          — Baixo,       D+1
        [ 0.80,  6.00, 1, 365],    # CDB prefixado          — Muito Baixo, vencimento
        [ 1.15,  6.50, 1, 365],    # LCA                    — Muito Baixo, vencimento
        [ 2.10,  8.00, 3, 365],    # Debêntures IPCA+5%     — Médio,       vencimento
        [10.66, 11.37, 4, 30],     # Fundos multimercado    — Alto,        D+30
        [ 9.57, 15.00, 4, 1],      # Fundos imobiliários    — Alto,        D+1
        [11.28, 22.26, 4, 45],     # Fundo cambial (dólar)  — Alto,        D+45
        [12.80, 29.77, 5, 30],     # Fundo de ações         — Muito Alto,  D+30
    ], dtype=float),
    # Volatilidade é a CAUSA RAIZ: dita o risco declarado e puxa a rentabilidade
    # exigida. Liquidez é decisão de produto, não consequência.
    "dematel": np.array([
        #   rent vol risco liq
        [0, 2, 2, 1],   # rentabilidade -> EFEITO do risco assumido
        [4, 0, 4, 2],   # volatilidade  -> CAUSA RAIZ
        [3, 3, 0, 2],   # risco
        [2, 1, 1, 0],   # liquidez
    ], dtype=float),
    "ahp": _saaty([1, 2, 3, 0]),   # liquidez > rentabilidade > volatilidade > risco
}

# ===========================================================================
# 3. CENÁRIOS DE TESTE DE CONDUÇÃO AUTÔNOMA — AHP-EWM-TOPSIS
# Fonte: LI, Shiqi; ZHOU, Rui; HUANG, Helai. "Multidimensional Evaluation of
#        Autonomous Driving Test Scenarios Based on AHP-EWM-TOPSIS Models".
#        Automotive Innovation, 2025. DOI 10.1007/s42154-024-00344-6.
#        [s42154-024-00344-6.pdf]
# Elementos do cenário conforme Tabelas 1 e 2 do artigo. Os treze elementos
# originais foram consolidados em nove: "tipo de objeto", "nº de objetos",
# "posição relativa" e "movimento relativo" viram dois critérios de tráfego —
# treze rótulos tornam o diagrama DEMATEL ilegível (lição do #BUG-021).
# ===========================================================================
CENARIOS_VA = {
    "id_caso": "cenarios_va",
    "nome": "Priorização de cenários de teste de condução autônoma",
    "dominio": "automotivo",
    "decisor": "Engenharia de validação de veículo autônomo",
    "descricao": (
        "Dezesseis cenários de teste, avaliados pelos elementos que o trabalho de origem "
        "identifica. A pergunta não é 'qual cenário o carro passa', é **qual cenário vale "
        "a pena rodar**: teste é caro, e um cenário fácil consome a mesma bancada que um "
        "difícil. Os autores avaliam por risco, complexidade e raridade — e a raridade é "
        "o critério que a intuição descarta e que decide: o cenário que quase nunca "
        "acontece é exatamente aquele para o qual ninguém treinou o sistema."),
    "criterios": [
        ("ddt",        "Tarefa de condução (DDT)",     "benefit", "0-10"),
        ("faixas",     "Número de faixas",             "benefit", "0-10"),
        ("via",        "Tipo de segmento viário",      "benefit", "0-10"),
        ("pavimento",  "Condição do pavimento",        "benefit", "0-10"),
        ("semaforo",   "Controle semafórico",          "benefit", "0-10"),
        ("obstaculo",  "Obstáculos na via",            "benefit", "0-10"),
        ("trafego",    "Densidade e tipo de tráfego",  "benefit", "0-10"),
        ("clima",      "Condição climática",           "benefit", "0-10"),
        ("iluminacao", "Iluminação",                   "benefit", "0-10"),
    ],
    "alternativas": [
        ("V01", "Corte lateral em rodovia"), ("V02", "Frenagem brusca do líder"),
        ("V03", "Pedestre entre veículos"), ("V04", "Cruzamento sem semáforo"),
        ("V05", "Conversão à esquerda com fluxo oposto"), ("V06", "Rotatória congestionada"),
        ("V07", "Chuva forte em rodovia"), ("V08", "Neblina em serra"),
        ("V09", "Entrada em rodovia (acesso curto)"), ("V10", "Obra com desvio de faixa"),
        ("V11", "Ciclista em via urbana"), ("V12", "Veículo na contramão"),
        ("V13", "Semáforo apagado"), ("V14", "Túnel com saída ofuscante"),
        ("V15", "Animal na pista à noite"), ("V16", "Trânsito parado em curva cega"),
    ],
    "matriz": np.array([
        # DDT faixa via pav sem obst tráf clima ilum
        [7.5, 6.5, 5.0, 3.0, 1.0, 4.5, 8.0, 2.5, 2.0],  # corte lateral
        [8.2, 5.0, 4.5, 4.0, 1.5, 3.5, 8.5, 3.0, 2.2],  # frenagem brusca
        [9.4, 4.0, 7.5, 3.5, 5.0, 8.5, 7.5, 3.5, 5.5],  # pedestre entre veículos
        [8.8, 5.5, 8.5, 3.0, 9.0, 5.5, 7.8, 3.0, 4.0],  # cruzamento sem semáforo
        [8.6, 7.0, 8.0, 3.2, 6.5, 5.0, 8.8, 3.2, 3.5],  # conversão à esquerda
        [7.8, 8.5, 9.0, 3.5, 4.0, 6.0, 9.2, 3.0, 3.8],  # rotatória
        [6.5, 6.0, 5.5, 9.0, 3.0, 4.0, 6.5, 9.4, 6.0],  # chuva forte
        [6.0, 4.5, 6.5, 6.5, 2.5, 5.0, 5.0, 9.8, 7.5],  # neblina
        [8.0, 7.5, 7.0, 3.0, 2.0, 4.5, 8.6, 2.8, 2.5],  # entrada em rodovia
        [7.2, 8.0, 6.0, 7.5, 3.5, 9.2, 7.0, 3.0, 4.5],  # obra com desvio
        [8.5, 5.0, 7.2, 3.8, 4.5, 7.0, 7.2, 3.2, 4.8],  # ciclista
        [9.6, 6.0, 6.5, 3.5, 3.0, 9.6, 8.0, 3.5, 5.0],  # contramão
        [8.4, 6.5, 8.2, 3.2, 9.6, 5.2, 8.4, 4.0, 5.2],  # semáforo apagado
        [7.0, 5.5, 6.8, 4.0, 2.0, 4.0, 6.0, 4.5, 9.6],  # túnel ofuscante
        [8.8, 3.5, 5.0, 4.5, 1.0, 9.4, 3.5, 4.0, 9.2],  # animal à noite
        [9.0, 6.0, 7.8, 5.0, 2.5, 8.0, 9.0, 4.2, 5.8],  # trânsito em curva cega
    ], dtype=float),
    # Clima e iluminação são CAUSAS ambientais: degradam pavimento, visibilidade e,
    # por elas, toda a dificuldade da tarefa. DDT é EFEITO — resulta do resto.
    "dematel": np.array([
        #   ddt faix via pav sem obst tráf clima ilum
        [0, 1, 1, 0, 1, 1, 2, 0, 0],   # DDT -> EFEITO
        [2, 0, 3, 0, 2, 1, 3, 0, 0],   # nº de faixas
        [3, 3, 0, 1, 3, 2, 3, 0, 1],   # tipo de via
        [3, 0, 1, 0, 0, 2, 2, 0, 0],   # pavimento
        [3, 1, 2, 0, 0, 1, 3, 0, 0],   # semáforo
        [3, 1, 1, 1, 0, 0, 3, 0, 0],   # obstáculos
        [4, 2, 2, 1, 2, 2, 0, 0, 0],   # tráfego
        [3, 0, 1, 4, 1, 2, 2, 0, 3],   # clima -> CAUSA RAIZ
        [3, 0, 1, 1, 1, 3, 2, 1, 0],   # iluminação -> CAUSA
    ], dtype=float),
    "ahp": _saaty([0, 6, 4, 5, 7, 2, 3, 1, 8]),  # DDT > clima > obstáculo > tráfego > ...
}

# ===========================================================================
# 4. SELEÇÃO DE IMPRESSORA 3D — AHP-TOPSIS com eficiência energética
# Fonte: OLIVEIRA, V. A. R.; ALVARADO SILVA, C. A.; OLIVEIRA, G. C. R.;
#        TAJIMA, F. M.; FARIA NETO, A. R.; SALOMON, V. A. P.; GUIDI, E. S.
#        "Multicriteria Analysis for 3D Printer Selection / Análise multicritério
#        para seleção de impressoras 3D". 23rd LACCEI International
#        Multi-Conference, Cidade do México, 2025. UNESP · Universidad César Vallejo.
#        [Contribution_1193_final_a-1.pdf]
# Os SETE critérios são os do artigo. O estudo compara três equipamentos;
# aqui a base é ampliada para doze, porque três alternativas não exercitam
# discordância entre métodos — e é a discordância que o motor existe para mostrar.
# ===========================================================================
IMPRESSORA_3D_ENERGIA = {
    "id_caso": "impressora_3d_energia",
    "nome": "Seleção de impressora 3D com eficiência energética",
    "dominio": "manufatura",
    "decisor": "Engenharia de manufatura aditiva (compra com meta de eficiência)",
    "descricao": (
        "Os sete critérios do trabalho de origem, que difere dos outros casos de "
        "impressão 3D deste projeto num ponto: **potência máxima entra como critério "
        "de decisão**, não como nota de rodapé da ficha técnica. Os autores partem da "
        "pressão por gestão de energia e conformidade — e aí a conta muda, porque o "
        "equipamento mais rápido costuma ser o que mais consome. Velocidade e potência "
        "são o par que o comprador de catálogo nunca vê junto."),
    "criterios": [
        ("preco",      "Preço do equipamento",          "cost",    "R$ mil"),
        ("volume",     "Volume de impressão",           "benefit", "L"),
        ("velocidade", "Velocidade máxima de impressão", "benefit", "mm/s"),
        ("temp_max",   "Temperatura máxima do extrusor", "benefit", "°C"),
        ("extrusores", "Número de extrusores",          "benefit", "un"),
        ("potencia",   "Potência máxima",               "cost",    "W"),
        ("tipo",       "Versatilidade de material",     "benefit", "0-10"),
    ],
    "alternativas": [
        ("P01", "FDM desktop de entrada"), ("P02", "FDM desktop rápida"),
        ("P03", "FDM com câmara fechada"), ("P04", "FDM industrial de grande volume"),
        ("P05", "FDM de duplo extrusor"), ("P06", "FDM de alta temperatura"),
        ("P07", "CoreXY de alta velocidade"), ("P08", "Delta de grande altura"),
        ("P09", "FDM com IDEX"), ("P10", "Resina LCD de bancada"),
        ("P11", "Resina de grande formato"), ("P12", "SLS de bancada"),
    ],
    "matriz": np.array([
        # preço volume veloc  temp  extr  potência  tipo
        [  2.4,  14.0,  180,  260,  1,    350, 4.0],  # FDM entrada
        [  4.8,  16.0,  500,  300,  1,    480, 5.0],  # FDM rápida
        [  9.5,  21.0,  300,  300,  1,    600, 6.5],  # câmara fechada
        [ 28.0,  90.0,  250,  300,  1,   1200, 6.8],  # industrial grande
        [  7.2,  18.0,  200,  260,  2,    550, 7.0],  # duplo extrusor
        [ 22.0,  24.0,  180,  500,  1,    900, 9.0],  # alta temperatura
        [  6.5,  20.0,  600,  300,  1,    520, 5.5],  # CoreXY rápida
        [  5.4,  32.0,  220,  260,  1,    450, 4.5],  # delta
        [ 12.5,  22.0,  280,  300,  2,    700, 8.0],  # IDEX
        [  3.2,   4.5,   90,    0,  0,    120, 3.5],  # resina LCD
        [ 18.0,  28.0,  110,    0,  0,    320, 4.2],  # resina grande formato
        [ 95.0,  25.0,  140,  200,  0,   2400, 9.5],  # SLS
    ], dtype=float),
    # Potência é CAUSA: dita o teto de temperatura e de velocidade que o equipamento
    # sustenta, e reaparece no preço. Preço é EFEITO do conjunto.
    "dematel": np.array([
        #  preço vol vel temp extr pot tipo
        [0, 1, 1, 1, 1, 1, 1],   # preço -> EFEITO
        [3, 0, 1, 0, 1, 3, 1],   # volume
        [3, 1, 0, 1, 1, 3, 1],   # velocidade
        [3, 0, 2, 0, 1, 3, 4],   # temperatura -> dita material
        [3, 1, 2, 1, 0, 2, 3],   # extrusores
        [3, 2, 4, 4, 2, 0, 2],   # potência -> CAUSA RAIZ
        [3, 1, 1, 3, 2, 2, 0],   # versatilidade de material
    ], dtype=float),
    "ahp": _saaty([0, 3, 2, 5, 6, 1, 4]),   # preço > potência > velocidade > volume > ...
}

# ===========================================================================
# 5. IMPRESSORAS MULTIFUNCIONAIS — AHP-TOPSIS 2N
# Fonte: OLIVEIRA, N. C.; OLIVEIRA, P. F. C.; GOMES, C. F. S.; SANTOS, M.
#        "Aplicação do método AHP TOPSIS 2N como apoio à tomada de decisão:
#        estudo de caso no departamento jurídico da Secretaria Municipal de Saúde
#        de Duque de Caxias". UNIGRANRIO · UFF · IME, 2019.
#        [Grafica/315852.pdf]
# Os QUATRO critérios são exatamente os elicitados pelos colaboradores do setor
# jurídico na entrevista descrita no artigo (seção 4).
# ===========================================================================
IMPRESSORAS_JURIDICO = {
    "id_caso": "impressoras_juridico",
    "nome": "Aquisição de impressora para departamento jurídico",
    "dominio": "operacoes",
    "decisor": "Setor jurídico de secretaria municipal de saúde",
    "descricao": (
        "Compra pública de impressora, com os quatro critérios que os próprios "
        "servidores do setor elencaram em entrevista — e não os que um catálogo "
        "sugeriria. O problema relatado no artigo não é qualidade de impressão: é "
        "**atolamento de papel e fila travada** parando a rotina. Daí a presença de "
        "volume máximo mensal e capacidade de bandeja ao lado do preço. "
        "São quatro critérios, abaixo dos seis que este projeto recomenda; manteve-se "
        "a modelagem do artigo em vez de inflá-la com critérios que ninguém elicitou."),
    "criterios": [
        ("custo",      "Custo de aquisição",          "cost",    "R$ mil"),
        ("velocidade", "Velocidade de impressão",     "benefit", "ppm"),
        ("volume",     "Volume máximo mensal",        "benefit", "mil cópias"),
        ("bandeja",    "Capacidade da bandeja",       "benefit", "folhas"),
    ],
    "alternativas": [
        ("I01", "Laser mono compacta"), ("I02", "Laser mono departamental"),
        ("I03", "Multifuncional laser mono"), ("I04", "Multifuncional laser color"),
        ("I05", "Laser mono alta capacidade"), ("I06", "Multifuncional A3 mono"),
        ("I07", "Tanque de tinta multifuncional"), ("I08", "Laser color departamental"),
        ("I09", "Multifuncional com finalizador"), ("I10", "Laser mono econômica"),
        ("I11", "Multifuncional A3 color"), ("I12", "Laser mono de produção"),
    ],
    "matriz": np.array([
        # custo veloc volume bandeja
        [ 1.2,  30,  30,  250],   # laser mono compacta
        [ 3.4,  45,  80,  550],   # laser mono departamental
        [ 4.1,  40,  60,  350],   # MFP laser mono
        [ 7.8,  35,  55,  350],   # MFP laser color
        [ 6.2,  55, 150, 1100],   # laser mono alta capacidade
        [ 9.5,  38,  90,  650],   # MFP A3 mono
        [ 2.6,  22,  25,  250],   # tanque de tinta
        [ 8.9,  42,  75,  550],   # laser color departamental
        [16.4,  50, 200, 2300],   # MFP com finalizador
        [ 1.8,  28,  35,  150],   # laser mono econômica
        [14.2,  36, 110,  750],   # MFP A3 color
        [11.5,  70, 300, 1600],   # laser mono de produção
    ], dtype=float),
    # Volume máximo é a CAUSA: define a classe do equipamento e arrasta bandeja,
    # velocidade e preço. Custo é efeito da classe escolhida.
    "dematel": np.array([
        #  custo vel vol band
        [0, 1, 1, 1],   # custo -> EFEITO
        [3, 0, 2, 2],   # velocidade
        [4, 3, 0, 4],   # volume -> CAUSA RAIZ
        [3, 2, 2, 0],   # bandeja
    ], dtype=float),
    "ahp": _saaty([0, 2, 1, 3]),   # custo > volume > velocidade > bandeja
}

# ===========================================================================
# 6. FUNDOS DE HEDGE (MULTIMERCADO) — eficiência
# Fonte: SILVA, Felipe Piton da; RIBEIRO, Celma de Oliveira. "Análise comparativa
#        de fundos de hedge brasileiros utilizando DEA e bootstrap".
#        XII SIMPEP, Bauru-SP, 07 a 09 de novembro de 2005.
#        Escola Politécnica da Universidade de São Paulo.
#        [Análise comparativa de fundos de hedge brasileiros....pdf]
# O trabalho mede eficiência por DEA com reamostragem, usando retorno, variância
# e assimetria. Aqui a estrutura é levada para o motor multicritério: os mesmos
# momentos da distribuição viram critérios explícitos, com direção declarada.
# ===========================================================================
FUNDOS_HEDGE = {
    "id_caso": "fundos_hedge",
    "nome": "Comparação de fundos multimercado (hedge)",
    "dominio": "financeiro",
    "decisor": "Alocador de recursos / investidor qualificado",
    "descricao": (
        "Vinte fundos multimercado, avaliados pelos momentos da distribuição de "
        "retornos — e não por um índice de referência. É a premissa do trabalho de "
        "origem: fundos de hedge **não têm benchmark honesto**, porque a liberdade de "
        "mandato é justamente o produto. Sem índice, resta comparar o formato da "
        "distribuição: retorno médio, dispersão, e a **assimetria** — o critério que "
        "separa o gestor que ganha muitas vezes pouco e perde uma vez tudo daquele que "
        "faz o contrário. Dois fundos com mesma média e mesmo desvio podem ser opostos."),
    "criterios": [
        ("retorno",    "Retorno médio anualizado",     "benefit", "%"),
        ("volat",      "Volatilidade anualizada",      "cost",    "%"),
        ("assimetria", "Assimetria dos retornos",      "benefit", "adim."),
        ("curtose",    "Curtose (risco de cauda)",     "cost",    "adim."),
        ("drawdown",   "Perda máxima acumulada",       "cost",    "%"),
        ("sharpe",     "Índice de Sharpe",             "benefit", "adim."),
        ("taxa",       "Taxa de administração",        "cost",    "% a.a."),
        ("patrimonio", "Patrimônio líquido",           "benefit", "R$ mi"),
    ],
    "alternativas": [
        ("H01", "Macro clássico"), ("H02", "Macro dinâmico"), ("H03", "Long & short neutro"),
        ("H04", "Long & short direcional"), ("H05", "Multiestratégia"),
        ("H06", "Juros e moedas"), ("H07", "Arbitragem"), ("H08", "Quantitativo sistemático"),
        ("H09", "Trend following"), ("H10", "Crédito estruturado"),
        ("H11", "Event driven"), ("H12", "Global macro"), ("H13", "Renda fixa ativa"),
        ("H14", "Ações long biased"), ("H15", "Volatilidade"),
        ("H16", "Commodities"), ("H17", "Multimercado conservador"),
        ("H18", "Multimercado agressivo"), ("H19", "Fundo de fundos"),
        ("H20", "Institucional previdenciário"),
    ],
    "matriz": np.array([
        # retorno volat assim curtose drawdown sharpe taxa patrim.
        [14.2,  8.4,  0.35,  4.2,  9.5, 1.28, 2.00,  850],
        [17.6, 12.1,  0.12,  5.8, 15.2, 1.15, 2.00,  620],
        [ 9.8,  4.2,  0.48,  3.4,  4.1, 1.42, 1.90,  410],
        [15.4, 11.6, -0.22,  6.5, 18.4, 0.98, 2.00,  530],
        [13.1,  7.2,  0.28,  4.0,  8.2, 1.35, 1.80, 1240],
        [11.5,  5.8,  0.40,  3.8,  6.0, 1.38, 1.50,  980],
        [ 8.6,  3.1,  0.62,  3.0,  2.8, 1.55, 1.20,  350],
        [16.8, 10.4,  0.05,  5.2, 13.6, 1.22, 2.20,  740],
        [19.2, 15.8, -0.35,  7.4, 22.1, 0.94, 2.50,  480],
        [10.4,  4.8, -0.85,  9.6,  7.5, 1.18, 1.60,  690],
        [12.8,  9.0,  0.18,  5.0, 11.2, 1.09, 2.00,  290],
        [18.4, 13.2,  0.08,  6.0, 17.5, 1.20, 2.30,  920],
        [ 9.2,  3.6,  0.30,  3.2,  3.4, 1.44, 1.00, 1580],
        [21.5, 18.4, -0.18,  6.8, 26.3, 1.02, 2.00,  660],
        [15.8, 14.0,  1.15,  8.8, 12.4, 0.88, 2.50,  210],
        [16.2, 16.5,  0.22,  6.2, 20.8, 0.82, 2.20,  180],
        [ 8.0,  2.8,  0.25,  3.1,  2.2, 1.48, 0.80, 2100],
        [22.8, 20.6, -0.42,  7.9, 29.5, 0.98, 2.50,  340],
        [11.8,  6.4,  0.32,  4.4,  7.8, 1.24, 1.40, 1350],
        [ 9.6,  4.0,  0.38,  3.5,  3.9, 1.36, 0.60, 3200],
    ], dtype=float),
    # Volatilidade é a CAUSA RAIZ dos momentos: dita drawdown, curtose e Sharpe.
    # Assimetria é o critério que NÃO deriva dela — é escolha de estratégia.
    "dematel": np.array([
        #   ret vol ass curt draw sharpe taxa patr
        [0, 2, 1, 1, 2, 3, 1, 3],   # retorno
        [3, 0, 1, 3, 4, 4, 1, 2],   # volatilidade -> CAUSA RAIZ
        [2, 1, 0, 3, 3, 2, 0, 1],   # assimetria -> CAUSA de cauda
        [1, 2, 2, 0, 3, 2, 0, 1],   # curtose
        [2, 2, 1, 2, 0, 2, 0, 3],   # drawdown
        [2, 1, 1, 1, 1, 0, 1, 3],   # Sharpe -> EFEITO
        [2, 0, 0, 0, 0, 2, 0, 2],   # taxa de administração
        [1, 2, 0, 1, 1, 1, 2, 0],   # patrimônio
    ], dtype=float),
    "ahp": _saaty([1, 3, 4, 6, 2, 0, 5, 7]),  # Sharpe > retorno > drawdown > volat > ...
}

# ===========================================================================
# 7. MODELOS DE PREVISÃO ESTOCÁSTICA
# Fonte: SHAH, Shalin. "Comparison of Stochastic Forecasting Models".
#        Stochastic Differential Equations Course Project,
#        Johns Hopkins University. [SDE_Paper.pdf]
# ⚠️  O trabalho de origem NÃO é um estudo multicritério: compara empiricamente
#     cinco modelos (ARIMA, GBM, TDNGBM/SDE, filtro bayesiano, filtro de Kalman)
#     por correlação previsto-real, MAE e qualidade dos intervalos de confiança.
#     Deste projeto é a decisão de tratar a ESCOLHA DE MODELO como problema
#     multicritério — os três primeiros critérios são as métricas do artigo; os
#     cinco restantes são custos de adoção que a comparação empírica não cobre.
# ===========================================================================
MODELOS_PREVISAO = {
    "id_caso": "modelos_previsao",
    "nome": "Escolha de modelo de previsão estocástica",
    "dominio": "ti",
    "decisor": "Equipe quantitativa (previsão de séries financeiras)",
    "descricao": (
        "Escolher o modelo de previsão é decisão multicritério e quase nunca é tratada "
        "como tal: compara-se acurácia e pronto. O trabalho de origem mostra por que "
        "isso não basta — **há casos em que todos os algoritmos vão bem e casos em que "
        "todos vão mal**, e o que separa os modelos na prática não é a média do erro, é "
        "o que acontece quando o regime muda. Acurácia é o que se mede no laboratório; "
        "calibrar, manter e explicar é o que se paga em produção."),
    "criterios": [
        ("correlacao",  "Correlação previsto × real",   "benefit", "0-1"),
        ("mae",         "Erro absoluto médio",          "cost",    "%"),
        ("intervalo",   "Qualidade do intervalo",       "benefit", "0-10"),
        ("regime",      "Robustez a mudança de regime", "benefit", "0-10"),
        ("custo_comp",  "Custo computacional",          "cost",    "0-10"),
        ("params",      "Parâmetros a calibrar",        "cost",    "un"),
        ("interpret",   "Interpretabilidade",           "benefit", "0-10"),
        ("horizonte",   "Horizonte útil",               "benefit", "dias"),
    ],
    "alternativas": [
        ("M1", "ARIMA"), ("M2", "Movimento browniano geométrico (GBM)"),
        ("M3", "SDE com deriva e difusão variáveis (TDNGBM)"),
        ("M4", "Filtro bayesiano"), ("M5", "Filtro de Kalman"),
        ("M6", "Média móvel (linha de base)"), ("M7", "Monte Carlo com bootstrap"),
    ],
    "matriz": np.array([
        # corr  MAE  interv regime custo params interp horiz
        [0.86,  4.2, 8.5, 5.0, 3.0,  3, 7.5, 30],   # ARIMA
        [0.72,  6.8, 5.0, 3.5, 1.5,  2, 9.0, 15],   # GBM
        [0.89,  3.6, 8.8, 7.0, 5.5,  5, 6.0, 54],   # TDNGBM (SDE)
        [0.81,  5.0, 7.0, 8.0, 7.0,  6, 4.5, 40],   # filtro bayesiano
        [0.79,  5.4, 6.5, 7.5, 4.0,  4, 5.5, 35],   # filtro de Kalman
        [0.58, 9.5, 2.0, 2.0, 0.5,  1, 9.8,  7],    # média móvel
        [0.83,  4.6, 9.2, 6.0, 8.5,  4, 5.0, 45],   # Monte Carlo bootstrap
    ], dtype=float),
    # Robustez a regime é a CAUSA que quase ninguém mede: quando ela falha, correlação
    # e MAE desabam juntos. Custo computacional e nº de parâmetros são escolhas de projeto.
    "dematel": np.array([
        #   corr mae int reg custo par int hor
        [0, 4, 2, 1, 1, 1, 1, 2],   # correlação
        [4, 0, 2, 1, 1, 1, 1, 2],   # MAE
        [2, 2, 0, 2, 2, 2, 1, 2],   # intervalo
        [4, 4, 3, 0, 2, 2, 1, 4],   # robustez a regime -> CAUSA RAIZ
        [1, 1, 2, 2, 0, 3, 2, 1],   # custo computacional
        [2, 2, 2, 3, 3, 0, 3, 1],   # nº de parâmetros
        [0, 0, 1, 1, 1, 1, 0, 0],   # interpretabilidade
        [2, 2, 2, 2, 1, 1, 0, 0],   # horizonte útil
    ], dtype=float),
    "ahp": _saaty([1, 2, 4, 0, 6, 7, 5, 3]),  # regime > correlação > MAE > horizonte > ...
}

# ===========================================================================
# 8. PORTFÓLIO DE CULTIVOS EM AMBIENTE CONTROLADO (RJ)
# Fonte: "AGTech PoliCultivo 4.0 — Otimização de Portfólio de Cultivos (RJ)",
#        relatório técnico de 03/08/2026, 68 páginas, seção 14.
#        [#Relatorio_AGTech_PoliCultivo_4.0_RJ.pdf]
# ⚠️  MATRIZ E PESOS REPRODUZIDOS DO RELATÓRIO (seções 14.1 e 14.2). Os oito
#     projetos e os oito critérios são os do estudo; os pesos AHP são os
#     publicados (CR = 0,0042). É obra do próprio autor deste projeto.
# ===========================================================================
POLICULTIVO_RJ = {
    "id_caso": "policultivo_rj",
    "nome": "Portfólio de cultivos em ambiente controlado (RJ)",
    "dominio": "agronegocio",
    "decisor": "Investidor / operador de fazenda urbana vertical",
    "descricao": (
        "Oito configurações completas de projeto — não cultivos isolados, mas combinações "
        "de aporte, área, regime e mix. O achado do estudo de origem é causal, não "
        "financeiro: o DEMATEL aponta a **maturidade tecnológica (TRL) como a maior "
        "causa-raiz** do sistema, enquanto payback e VPL — os números que o investidor "
        "olha primeiro — aparecem como os maiores **efeitos**. Não se melhora payback "
        "atacando payback. Isso explica por que trufa, Yarsa Gumba e Matsutake exibem os "
        "melhores ROIs do acervo e ainda assim são descartadas: com TRL 1–2, elas anulam "
        "VPL, payback e densidade de valor ao mesmo tempo."),
    "criterios": [
        ("payback",   "Payback",                      "cost",    "meses"),
        ("vpl",       "VPL em 5 anos",                "benefit", "R$ mil"),
        ("trl",       "Maturidade tecnológica (TRL)", "benefit", "1-9"),
        ("densidade", "Densidade de valor",           "benefit", "R$/m²"),
        ("prob",      "P(VPL > 0)",                   "benefit", "%"),
        ("mercado",   "Teto de absorção do mercado",  "benefit", "0-10"),
        ("clima",     "Aderência climática ao RJ",    "benefit", "0-10"),
        ("aporte",    "Aporte inicial",               "cost",    "R$ mil"),
    ],
    "alternativas": [
        ("P1", "Micro 20 m² — mix ótimo de cogumelos"),
        ("P2", "Bootstrap R$ 10 mil → 20 m²"),
        ("P3", "Industrial 85 m² — valor máx./m²"),
        ("P4", "Batata-semente aeropônica"),
        ("P5", "Mudas trufeiras micorrizadas"),
        ("P6", "Tilápia em RAS industrial (urbano)"),
        ("P7", "Aquaponia camarão + folhosas (rural)"),
        ("P8", "Policultivo tilápia+camarão em viveiro"),
    ],
    # Seção 14.1 do relatório. VPL e aporte em R$ mil; densidade em R$/m².
    # O teto de absorção não consta da tabela publicada e foi arbitrado na escala
    # 0-10 a partir da seção 6 (saturação do mercado carioca acima de 85 m²) —
    # é o ÚNICO valor deste caso que não vem do relatório, e está dito aqui.
    "matriz": np.array([
        # payback    VPL    TRL  densid.  P(VPL>0) mercado clima  aporte
        [  3.9,   429.908, 8.5,  7661.0,  100.0,  6.5,  8.0,  49.263],  # micro 20 m²
        [  4.6,   309.533, 8.5,  6483.0,   95.0,  6.5,  8.0,  10.000],  # bootstrap
        [  5.6,  2508.167, 8.5, 11083.0,   93.0,  4.0,  8.0, 437.742],  # industrial 85 m²
        [ 24.8,    10.375, 8.0,  1471.0,   78.0,  8.5,  5.0,  94.322],  # batata-semente
        [  4.5,   295.383, 6.0,  7217.0,   62.0,  2.5,  7.6,  83.754],  # mudas trufeiras
        [240.0,     2.588, 9.0,    42.0,   28.0,  9.5,  8.6,  55.311],  # tilápia RAS
        [240.0,   -21.832, 8.0,  -352.0,   55.0,  9.0,  8.8,  34.560],  # aquaponia
        [240.0,    -9.664, 9.0,  -156.0,   40.0,  9.5,  8.8,  18.199],  # policultivo
    ], dtype=float),
    # Estrutura causal da seção 14.2: TRL, teto de mercado, clima e aporte são
    # CAUSAS; payback, VPL, densidade e P(VPL>0) são EFEITOS. A matriz abaixo
    # reproduz esses papéis (R−C: TRL +1,35 é a maior causa; payback −1,24 o maior efeito).
    "dematel": np.array([
        #  payb vpl trl dens prob merc clima aporte
        [0, 2, 0, 1, 1, 0, 0, 0],   # payback -> MAIOR EFEITO
        [2, 0, 0, 1, 1, 0, 0, 0],   # VPL -> EFEITO
        [4, 4, 0, 3, 4, 1, 1, 2],   # TRL -> CAUSA RAIZ
        [3, 4, 0, 0, 2, 1, 0, 0],   # densidade de valor
        [2, 2, 1, 1, 0, 0, 0, 0],   # P(VPL>0) -> EFEITO
        [3, 3, 0, 3, 2, 0, 0, 1],   # teto de mercado -> CAUSA
        [2, 2, 2, 3, 2, 1, 0, 1],   # aderência climática -> CAUSA
        [3, 3, 1, 1, 2, 0, 0, 0],   # aporte inicial -> CAUSA
    ], dtype=float),
    # Pesos AHP publicados (seção 14.2, CR = 0,0042):
    # payback 21,4 · VPL 21,4 · TRL 11,6 · densidade 11,6 · P(VPL>0) 11,6
    # · mercado 6,5 · clima 4,2 · aporte 11,6
    "ahp": _saaty_de_pesos([21.4, 21.4, 11.6, 11.6, 11.6, 6.5, 4.2, 11.6]),
}

CATALOGO_ESTUDOS_KB2 = {c["id_caso"]: c for c in (
    CRIPTO, PORTFOLIO_CRISE, CENARIOS_VA, IMPRESSORA_3D_ENERGIA,
    IMPRESSORAS_JURIDICO, FUNDOS_HEDGE, MODELOS_PREVISAO, POLICULTIVO_RJ)}

if __name__ == "__main__":
    from casos.catalogo import validar
    n_alt = n_cel = 0
    for c in CATALOGO_ESTUDOS_KB2.values():
        validar(c)
        a, k = len(c["alternativas"]), len(c["criterios"])
        n_alt += a; n_cel += a * k
        print(f"✅ {c['id_caso']:<24} {c['dominio']:<12} {a:>3} alt × {k} crit")
    print(f"\n{len(CATALOGO_ESTUDOS_KB2)} casos · {n_alt} alternativas · {n_cel} células")
