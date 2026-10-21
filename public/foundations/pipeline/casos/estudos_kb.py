"""
Estudos de caso derivados do acervo `kb/Artigos e Teses/Novos2/`.

═══════════════════════════════════════════════════════════════════════════════
 PROCEDÊNCIA — cada caso abaixo reproduz a ESTRUTURA DE DECISÃO (critérios,
 direções, relações causais) de um trabalho específico do acervo. A autoria dos
 estudos é dos autores citados; deste projeto é a implementação e a integração
 ao motor de dez métodos.
═══════════════════════════════════════════════════════════════════════════════

⚠️  Os VALORES das matrizes são ILUSTRATIVOS — ordens de grandeza plausíveis de
mercado, arredondadas, para demonstrar o método. Os trabalhos originais usam dados
de períodos específicos (2015-2023) que não reproduzo aqui. O que é fiel é a
MODELAGEM: quais critérios entram, em que direção, e como se influenciam.

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import numpy as np

from casos.catalogo import _saaty

# ===========================================================================
# 1. PRÉ-SELEÇÃO DE AÇÕES — TOPSIS
# Fonte: COSTA, Leandro Santos da. "Uma metodologia para a pré-seleção de ações
#        utilizando o método multicritério TOPSIS" [114755_0.pdf]
#        (UERJ) [114755_0.pdf]
#        + VÁSQUEZ, J. A.; ESCOBAR, J. W.; MANOTAS, D. F. "AHP–TOPSIS
#          Methodology for Stock Portfolio Investments" (Risks, v.10, n.1,
#          art.4, 2022; Universidad del Valle)
#          doi:10.3390/risks10010004 [risks-10-00004.pdf]
# Critérios do trabalho: Liquidez Geral · Dividend Yield · Volatilidade ·
#                        Governança Corporativa · 1/(P/L) · P/VPA · ROE
# ===========================================================================
ACOES = {
    "id_caso": "acoes_b3",
    "nome": "Pré-seleção de ações para carteira",
    "dominio": "financeiro",
    "decisor": "Gestor de carteira / investidor pessoa física",
    "descricao": (
        "20 ações, 7 critérios — a modelagem de Costa (TOPSIS) somada à de Risks "
        "(AHP–TOPSIS). O erro clássico é ranquear por Dividend Yield: o DY alto "
        "costuma ser sintoma de cotação em queda, não de generosidade. E "
        "**volatilidade e governança**, que o trabalho original inclui, são "
        "justamente os critérios que a planilha de indicadores ignora."),
    "criterios": [
        ("liquidez",    "Liquidez geral",         "benefit", "índice"),
        ("dy",          "Dividend Yield",         "benefit", "%"),
        ("volatilidade", "Volatilidade",          "cost",    "% a.a."),
        ("governanca",  "Governança corporativa", "benefit", "0-10"),
        ("inv_pl",      "1/(P/L)",                "benefit", "índice"),
        ("pvpa",        "P/VPA",                  "cost",    "índice"),
        ("roe",         "ROE",                    "benefit", "%"),
    ],
    "alternativas": [
        ("A01", "Banco de varejo"), ("A02", "Mineradora"), ("A03", "Siderúrgica"),
        ("A04", "Energia elétrica"), ("A05", "Saneamento"), ("A06", "Petróleo e gás"),
        ("A07", "Varejo alimentar"), ("A08", "Varejo vestuário"), ("A09", "Telecom"),
        ("A10", "Seguradora"), ("A11", "Papel e celulose"), ("A12", "Frigorífico"),
        ("A13", "Construtora"), ("A14", "Shopping centers"), ("A15", "Bolsa/serviços fin."),
        ("A16", "Bebidas"), ("A17", "Química/petroquímica"), ("A18", "Transporte/logística"),
        ("A19", "Saúde"), ("A20", "Tecnologia"),
    ],
    "matriz": np.array([
        # liquidez  DY   volat  gov  1/PL  P/VPA  ROE
        [ 1.35,  8.2, 26.0, 9.0, 0.145, 1.10, 18.5],  # banco
        [ 1.85, 11.4, 38.0, 8.0, 0.180, 1.45, 24.0],  # mineradora
        [ 1.62,  7.8, 41.0, 7.5, 0.120, 0.85, 12.5],  # siderúrgica
        [ 1.20,  9.6, 19.0, 9.5, 0.110, 1.60, 15.0],  # energia
        [ 1.45,  5.4, 22.0, 8.5, 0.095, 1.25,  13.2],  # saneamento
        [ 1.55, 14.8, 34.0, 7.0, 0.210, 1.05, 26.5],  # petróleo
        [ 1.10,  3.2, 28.0, 8.0, 0.055, 2.40,  9.8],  # varejo alimentar
        [ 0.95,  2.1, 45.0, 7.0, 0.030, 2.90,  6.5],  # varejo vestuário
        [ 1.28,  6.8, 24.0, 8.5, 0.085, 1.35, 11.0],  # telecom
        [ 1.72,  7.2, 21.0, 9.2, 0.130, 1.55, 19.8],  # seguradora
        [ 1.48,  6.4, 33.0, 8.2, 0.105, 1.15, 14.0],  # papel e celulose
        [ 1.15,  4.6, 36.0, 6.5, 0.140, 0.95, 16.2],  # frigorífico
        [ 0.88,  2.8, 48.0, 6.8, 0.060, 0.75,  8.4],  # construtora
        [ 1.32,  8.8, 27.0, 8.8, 0.090, 1.20, 12.8],  # shoppings
        [ 2.10,  5.8, 25.0, 9.6, 0.075, 3.10, 22.0],  # bolsa
        [ 1.40,  4.2, 20.0, 9.0, 0.065, 2.70, 17.5],  # bebidas
        [ 1.25,  5.0, 39.0, 7.2, 0.115, 1.00, 10.6],  # química
        [ 1.05,  3.6, 31.0, 7.8, 0.070, 1.70,  9.2],  # transporte
        [ 1.18,  1.8, 35.0, 8.4, 0.045, 2.20,  7.6],  # saúde
        [ 1.60,  0.9, 52.0, 8.6, 0.025, 4.50, 11.4],  # tecnologia
    ], dtype=float),
    # Volatilidade e governança são CAUSAS: ditam o risco percebido e, por ele,
    # o múltiplo que o mercado aceita pagar (P/VPA) e o DY implícito.
    "dematel": np.array([
        #     liq  DY  vol gov 1/PL PVPA ROE
        [0, 1, 1, 1, 2, 2, 2],   # liquidez
        [1, 0, 1, 0, 2, 3, 1],   # DY
        [2, 3, 0, 2, 3, 3, 1],   # volatilidade -> CAUSA de múltiplo e DY
        [2, 2, 3, 0, 2, 3, 2],   # governança -> CAUSA de risco percebido
        [1, 2, 1, 0, 0, 3, 2],   # 1/(P/L)
        [1, 2, 1, 0, 2, 0, 1],   # P/VPA
        [2, 2, 1, 1, 3, 3, 0],   # ROE -> dita múltiplos
    ], dtype=float),
    "ahp": _saaty([3, 1, 0, 2, 4, 6, 5]),   # volatilidade > DY > governança > liquidez > ...
}

# ===========================================================================
# 2. FUNDOS IMOBILIÁRIOS
# Fonte: SANTOS, Victor Vianna dos. "Avaliação do método Random Forest para
#        auxílio à seleção de fundos de investimento imobiliário listados na
#        Bolsa de Valores". Trabalho de Graduação, Engenharia da Computação,
#        CIn/UFPE, set. 2023. Orient.: ALMEIDA FILHO, Adiel Teixeira de.
#        [Fundo Imobiliário TCC Victor Vianna dos Santos.pdf]
# Critérios do trabalho: Dividend Yield · P/VP · Vacância física · Vacância
#        financeira · Liquidez · Cap rate · Nº de ativos · Patrimônio líquido
# ===========================================================================
FII = {
    "id_caso": "fundos_imobiliarios",
    "nome": "Seleção de fundos imobiliários (FII)",
    "dominio": "financeiro",
    "decisor": "Investidor em renda passiva imobiliária",
    "descricao": (
        "18 fundos, 8 critérios. O trabalho de origem mostra por que ranquear FII "
        "por Dividend Yield engana: **vacância** é a causa raiz — um fundo com "
        "imóveis desocupados paga bem hoje com receita não recorrente e quebra o "
        "rendimento adiante. E P/VP abaixo de 1 tanto pode ser desconto quanto "
        "aviso do mercado sobre a carteira."),
    "criterios": [
        ("dy",          "Dividend Yield",        "benefit", "% a.a."),
        ("pvp",         "P/VP",                  "cost",    "índice"),
        ("vacancia",    "Vacância física",       "cost",    "%"),
        ("vac_fin",     "Vacância financeira",   "cost",    "%"),
        ("liquidez",    "Liquidez diária",       "benefit", "R$ mil"),
        ("cap_rate",    "Cap rate",              "benefit", "%"),
        ("n_ativos",    "Diversificação",        "benefit", "imóveis"),
        ("patrimonio",  "Patrimônio líquido",    "benefit", "R$ mi"),
    ],
    "alternativas": [
        ("F01", "Lajes corporativas AAA"), ("F02", "Lajes corporativas B"),
        ("F03", "Galpões logísticos"), ("F04", "Shopping centers"),
        ("F05", "Agências bancárias"), ("F06", "Educacional"),
        ("F07", "Hospitalar"), ("F08", "Papel (CRI) high grade"),
        ("F09", "Papel (CRI) high yield"), ("F10", "Fundo de fundos"),
        ("F11", "Residencial para renda"), ("F12", "Varejo de rua"),
        ("F13", "Hotelaria"), ("F14", "Data centers"),
        ("F15", "Desenvolvimento"), ("F16", "Híbrido"),
        ("F17", "Renda urbana"), ("F18", "Agro (Fiagro imobiliário)"),
    ],
    "matriz": np.array([
        #  DY   P/VP  vac  vacF  liq   cap  ativos  PL
        [ 8.2, 0.88,  9.0, 11.0, 2400,  7.8, 12,  2800],  # lajes AAA
        [ 9.6, 0.72, 22.0, 26.0,  680,  9.2,  8,   740],  # lajes B
        [ 9.1, 0.94,  4.0,  5.0, 3100,  8.4, 24,  4200],  # logística
        [ 8.8, 0.91,  6.5,  8.0, 2900,  8.0, 14,  3600],  # shoppings
        [ 9.4, 0.83, 12.0, 14.0,  520,  9.0, 62,   890],  # agências
        [10.2, 0.78, 15.0, 17.0,  310,  9.8,  9,   420],  # educacional
        [ 8.6, 0.96,  3.0,  4.0,  760,  8.2,  6,  1100],  # hospitalar
        [11.4, 1.01,  0.0,  0.0, 4200, 11.0,  0,  5400],  # CRI high grade
        [14.8, 0.97,  0.0,  0.0, 1900, 14.2,  0,  1600],  # CRI high yield
        [ 9.8, 0.89,  0.0,  0.0, 2200,  9.4,  0,  2100],  # FoF
        [ 7.4, 0.92, 11.0, 12.0,  430,  7.0, 18,   560],  # residencial
        [ 9.0, 0.81, 17.0, 19.0,  290,  8.8, 34,   380],  # varejo de rua
        [ 6.8, 0.68, 28.0, 33.0,  180,  6.4,  5,   240],  # hotelaria
        [ 8.4, 1.08,  2.0,  2.5, 1400,  7.6,  4,  1900],  # data centers
        [ 5.2, 0.86, 35.0, 40.0,  210,  5.0,  3,   320],  # desenvolvimento
        [ 9.3, 0.90,  8.0,  9.5, 1700,  8.6, 20,  2300],  # híbrido
        [ 9.7, 0.85, 10.0, 11.5,  940,  9.1, 28,  1200],  # renda urbana
        [10.6, 0.93,  5.0,  6.0,  610, 10.0,  7,   680],  # Fiagro
    ], dtype=float),
    # Vacância é a CAUSA RAIZ: derruba receita, logo DY futuro e cap rate,
    # e o mercado a precifica no P/VP.
    "dematel": np.array([
        #     DY  PVP vac vacF liq cap ativos PL
        [0, 3, 0, 0, 1, 2, 0, 0],   # DY
        [1, 0, 0, 0, 2, 1, 0, 1],   # P/VP
        [3, 3, 0, 4, 1, 3, 1, 1],   # vacância -> CAUSA RAIZ
        [3, 3, 2, 0, 1, 3, 0, 1],   # vacância financeira
        [1, 2, 0, 0, 0, 0, 0, 2],   # liquidez
        [3, 2, 1, 1, 1, 0, 0, 1],   # cap rate
        [1, 1, 3, 3, 1, 1, 0, 2],   # diversificação -> dilui vacância
        [1, 1, 0, 0, 3, 0, 2, 0],   # patrimônio -> liquidez
    ], dtype=float),
    "ahp": _saaty([1, 3, 0, 2, 5, 4, 6, 7]),   # vacância > DY > vacF > P/VP > ...
}

# ===========================================================================
# 3. SELEÇÃO DE FINTECH
# Fonte: WIBOWO, S.; GRANDHI, L.; GRANDHI, S.; WELLS, M. "A Fuzzy
#        Multicriteria Group Decision Making Approach for Evaluating and
#        Selecting Fintech Projects" (Mathematics, v.10, n.2, art.225, 2022;
#        CQUniversity) doi:10.3390/math10020225
#        [A fuzzy multicriteria group decision making...pdf, Fintech.pdf]
# ===========================================================================
FINTECH = {
    "id_caso": "fintech",
    "nome": "Avaliação e seleção de projetos de Fintech",
    "dominio": "financeiro",
    "decisor": "Comitê de inovação de instituição financeira (decisão em grupo)",
    "descricao": (
        "16 projetos de fintech, 8 critérios. O trabalho original usa decisão em "
        "GRUPO com números difusos — porque um comitê de banco não converge para um "
        "número, converge para uma faixa. Aqui o SAPEVO-M cumpre esse papel: agrega "
        "julgamento ordinal de vários decisores sem exigir consenso prévio.\n\n"
        "O critério que decide não é retorno: é **conformidade regulatória**. Uma "
        "fintech excelente que o regulador barra vale zero."),
    "criterios": [
        ("roi",         "Retorno esperado",        "benefit", "%"),
        ("investimento", "Investimento inicial",   "cost",    "R$ mi"),
        ("time_market", "Tempo até o mercado",     "cost",    "meses"),
        ("regulatorio", "Conformidade regulatória", "benefit", "0-10"),
        ("escalabilidade", "Escalabilidade",       "benefit", "0-10"),
        ("risco_tec",   "Risco tecnológico",       "cost",    "0-10"),
        ("sinergia",    "Sinergia com o negócio",  "benefit", "0-10"),
        ("seguranca",   "Segurança e privacidade", "benefit", "0-10"),
    ],
    "alternativas": [
        ("P01", "Pagamentos instantâneos"), ("P02", "Carteira digital"),
        ("P03", "Crédito com score alternativo"), ("P04", "Open finance / agregador"),
        ("P05", "Investimentos automatizados"), ("P06", "Seguros paramétricos"),
        ("P07", "Antifraude com IA"), ("P08", "Banking as a Service"),
        ("P09", "Crédito consignado digital"), ("P10", "Câmbio e remessas"),
        ("P11", "Tokenização de recebíveis"), ("P12", "Cripto/custódia"),
        ("P13", "Conta para PMEs"), ("P14", "Marketplace de crédito"),
        ("P15", "Cobrança inteligente"), ("P16", "Identidade digital / KYC"),
    ],
    "matriz": np.array([
        # ROI  invest  TTM  regul escal risco siner seg
        [ 28,  12.0,  10, 9.5, 9.2, 3.5, 9.0, 9.0],  # pagamentos instantâneos
        [ 24,   8.0,   8, 9.0, 9.0, 3.0, 8.6, 8.8],  # carteira digital
        [ 42,  15.0,  14, 6.5, 8.4, 6.5, 8.0, 7.5],  # score alternativo
        [ 31,  18.0,  16, 8.5, 8.8, 5.5, 9.2, 8.6],  # open finance
        [ 26,   9.0,  11, 8.8, 8.2, 4.0, 8.4, 8.4],  # investimentos automatizados
        [ 35,  11.0,  15, 6.0, 7.4, 6.8, 6.5, 7.8],  # seguros paramétricos
        [ 33,  14.0,  12, 9.2, 8.6, 5.0, 9.4, 9.6],  # antifraude IA
        [ 38,  26.0,  22, 7.5, 9.5, 6.2, 8.2, 8.2],  # BaaS
        [ 22,   6.0,   7, 9.4, 7.0, 2.5, 8.8, 8.5],  # consignado digital
        [ 29,  10.0,  13, 7.0, 8.0, 4.5, 7.2, 8.0],  # câmbio
        [ 46,  20.0,  20, 5.5, 8.8, 7.5, 7.0, 7.2],  # tokenização
        [ 58,  16.0,  18, 3.5, 9.0, 8.5, 5.0, 6.4],  # cripto/custódia
        [ 25,   7.5,   9, 9.0, 8.4, 3.2, 8.6, 8.6],  # conta PME
        [ 34,  13.0,  15, 7.2, 8.6, 5.8, 7.6, 7.6],  # marketplace de crédito
        [ 19,   4.5,   6, 9.2, 6.8, 2.2, 8.0, 8.2],  # cobrança inteligente
        [ 27,  11.5,  12, 9.6, 8.0, 4.2, 9.0, 9.8],  # identidade / KYC
    ], dtype=float),
    # Regulatório é a CAUSA: dita prazo, risco e até o investimento necessário.
    "dematel": np.array([
        #     ROI inv TTM reg esc risco sin seg
        [0, 2, 1, 1, 2, 1, 2, 0],   # ROI
        [2, 0, 3, 1, 2, 2, 1, 1],   # investimento
        [2, 2, 0, 1, 1, 2, 1, 0],   # time to market
        [3, 3, 4, 0, 2, 3, 2, 3],   # regulatório -> CAUSA RAIZ
        [3, 2, 1, 1, 0, 2, 2, 1],   # escalabilidade
        [2, 3, 3, 1, 2, 0, 1, 3],   # risco tecnológico
        [2, 1, 1, 1, 2, 1, 0, 1],   # sinergia
        [1, 2, 2, 3, 1, 2, 1, 0],   # segurança -> conformidade
    ], dtype=float),
    "ahp": _saaty([3, 5, 6, 0, 4, 7, 2, 1]),   # regulatório > segurança > sinergia > ROI > ...
}

# ===========================================================================
# 4. AVALIAÇÃO DE IMÓVEIS
# Fontes (pasta "Avaliação de Imóveis"):
#   DUARTE, D. C. O. "Análise multicritério e geoestatística aplicadas na
#     avaliação em massa de imóveis urbanos"
#   "Modelos e técnicas de tomada de decisão em análise multicritério —
#     aplicações em avaliação de imóveis" (Paulo Fábio ...)
#   "Métodos multicritério de auxílio à decisão aplicados a avaliação..."
#     (Relatórios de Pesquisa em Engenharia de Produção, v.8, n.4)
#   MARQUES, J. P. M. "As formas de avaliar imóvel em leilão judicial"
# ===========================================================================
IMOVEIS = {
    "id_caso": "avaliacao_imoveis",
    "nome": "Avaliação e escolha de imóvel urbano",
    "dominio": "imobiliario",
    "decisor": "Comprador / avaliador em avaliação em massa",
    "descricao": (
        "16 imóveis, 8 critérios. A avaliação tradicional regride preço contra área "
        "e conclui pouco. Os trabalhos de origem mostram que **localização** é a "
        "causa que move todo o resto — infraestrutura, valorização e até o padrão "
        "construtivo que o entorno comporta. Área é efeito, não alavanca."),
    "criterios": [
        ("preco",       "Preço",                  "cost",    "R$ mil"),
        ("area",        "Área útil",              "benefit", "m²"),
        ("localizacao", "Localização",            "benefit", "0-10"),
        ("infra",       "Infraestrutura urbana",  "benefit", "0-10"),
        ("idade",       "Idade do imóvel",        "cost",    "anos"),
        ("padrao",      "Padrão construtivo",     "benefit", "0-10"),
        ("valorizacao", "Valorização projetada",  "benefit", "% a.a."),
        ("condominio",  "Custo de condomínio",    "cost",    "R$/mês"),
    ],
    "alternativas": [
        ("I01", "Apto 2q centro"), ("I02", "Apto 3q centro"),
        ("I03", "Apto 2q bairro nobre"), ("I04", "Apto 3q bairro nobre"),
        ("I05", "Apto 2q periferia"), ("I06", "Casa térrea bairro médio"),
        ("I07", "Casa sobrado bairro nobre"), ("I08", "Cobertura centro"),
        ("I09", "Kitnet centro"), ("I10", "Apto 4q alto padrão"),
        ("I11", "Casa condomínio fechado"), ("I12", "Apto 1q investidor"),
        ("I13", "Loja térrea comercial"), ("I14", "Sala comercial"),
        ("I15", "Terreno urbano"), ("I16", "Imóvel em leilão judicial"),
    ],
    "matriz": np.array([
        # preço  área  loc  infra idade padrão valoriz  cond
        [  420,  62,  8.0, 8.5, 18, 7.0,  6.5,  680],  # apto 2q centro
        [  610,  88,  8.0, 8.5, 15, 7.5,  6.8,  820],  # apto 3q centro
        [  580,  68,  9.2, 9.0, 10, 8.5,  8.0,  920],  # apto 2q nobre
        [  850,  96,  9.2, 9.0,  8, 8.8,  8.2, 1150],  # apto 3q nobre
        [  230,  58,  5.5, 6.0, 22, 5.5,  4.5,  380],  # apto 2q periferia
        [  390, 120,  6.8, 7.0, 25, 6.0,  5.5,    0],  # casa térrea
        [  980, 210,  9.0, 8.8, 12, 8.6,  7.8,  620],  # sobrado nobre
        [ 1250, 180,  8.2, 8.5, 14, 9.0,  7.0, 1480],  # cobertura centro
        [  180,  32,  7.8, 8.4, 20, 6.0,  5.8,  460],  # kitnet
        [ 1650, 240,  9.5, 9.2,  6, 9.4,  8.5, 1900],  # 4q alto padrão
        [ 1100, 260,  8.4, 7.6,  9, 8.8,  8.8,  980],  # condomínio fechado
        [  260,  38,  8.6, 8.8, 16, 6.8,  7.2,  520],  # 1q investidor
        [  720,  95,  8.8, 8.2, 28, 6.5,  6.0,  340],  # loja térrea
        [  340,  46,  8.4, 8.6, 13, 7.4,  6.4,  590],  # sala comercial
        [  450, 300,  7.2, 6.4,  0, 1.0,  9.2,    0],  # terreno
        [  290,  84,  7.6, 7.8, 24, 6.2,  7.5,  700],  # leilão judicial
    ], dtype=float),
    # Localização é a CAUSA RAIZ: puxa infraestrutura, valorização, padrão e preço.
    "dematel": np.array([
        #     pre area loc inf idade pad val cond
        [0, 2, 1, 1, 1, 2, 2, 2],   # preço
        [3, 0, 0, 0, 0, 1, 1, 3],   # área -> condomínio
        [4, 1, 0, 4, 0, 3, 4, 2],   # localização -> CAUSA RAIZ
        [3, 0, 2, 0, 0, 1, 3, 1],   # infraestrutura
        [3, 0, 0, 0, 0, 3, 2, 1],   # idade -> padrão e valorização
        [3, 1, 1, 1, 1, 0, 2, 2],   # padrão construtivo
        [3, 0, 1, 1, 0, 1, 0, 0],   # valorização
        [2, 0, 0, 0, 0, 1, 1, 0],   # condomínio
    ], dtype=float),
    "ahp": _saaty([1, 4, 0, 3, 6, 5, 2, 7]),   # localização > preço > valorização > infra > ...
}

# ===========================================================================
# 5. PRIORIZAÇÃO DE ORDENS DE SERVIÇO — AHP integrado ao PROMETHEE
# Fonte: ALENCAR, L. G. de; TAVARES, F. R. M.; MENDONÇA, F. J. S. de F.;
#        DUARTE, A. K. G. (URCA). "Priorização de ordens de serviço aplicando
#        métodos de tomada de decisão: o AHP integrado ao PROMETHEE". RPO,
#        v.22, n.2, p.2763-2784, 2022. [4637-Texto do Artigo...pdf]
# ===========================================================================
ORDENS_SERVICO = {
    "id_caso": "ordens_servico",
    "nome": "Priorização de ordens de serviço de manutenção",
    "dominio": "operacoes",
    "decisor": "Planejador de manutenção (PCM)",
    "descricao": (
        "18 ordens de serviço na fila, 8 critérios. A prática comum é atender por "
        "ordem de chegada — o que faz a OS mais antiga passar à frente da que vai "
        "parar a linha de produção. O trabalho de origem integra AHP e PROMETHEE "
        "justamente porque **tempo de fila e criticidade são critérios distintos** "
        "e frequentemente opostos."),
    "criterios": [
        ("criticidade", "Criticidade do ativo",     "benefit", "0-10"),
        ("tempo_fila",  "Tempo em aberto",          "benefit", "dias"),
        ("custo",       "Custo da intervenção",     "cost",    "R$ mil"),
        ("parada",      "Risco de parada de linha", "benefit", "0-10"),
        ("seguranca",   "Risco de segurança",       "benefit", "0-10"),
        ("duracao",     "Duração do serviço",       "cost",    "h"),
        ("recursos",    "Disponibilidade de peça",  "benefit", "0-10"),
        ("legal",       "Exigência legal/normativa", "benefit", "0-10"),
    ],
    "alternativas": [
        ("OS01", "Vazamento em prensa hidráulica"), ("OS02", "Troca de rolamento crítico"),
        ("OS03", "Calibração de balança fiscal"), ("OS04", "Reparo de esteira principal"),
        ("OS05", "Iluminação de galpão"), ("OS06", "Painel elétrico com sobreaquecimento"),
        ("OS07", "Compressor de ar principal"), ("OS08", "Manutenção de empilhadeira"),
        ("OS09", "Sensor de temperatura da estufa"), ("OS10", "Pintura de sinalização de piso"),
        ("OS11", "Sistema de combate a incêndio"), ("OS12", "Bomba de água de processo"),
        ("OS13", "Ar-condicionado administrativo"), ("OS14", "Ponte rolante"),
        ("OS15", "Caldeira — inspeção NR-13"), ("OS16", "Portão automático de doca"),
        ("OS17", "Exaustor de cabine de pintura"), ("OS18", "Nobreak da sala de servidores"),
    ],
    "matriz": np.array([
        # crit  fila custo parada seg  dur  peça legal
        [ 9.0,  12,  8.5, 9.2, 8.0,  6, 8.0, 5.0],  # prensa hidráulica
        [ 9.5,   4, 12.0, 9.6, 7.0,  8, 6.5, 4.0],  # rolamento crítico
        [ 6.0,  38,  2.0, 2.0, 3.0,  3, 9.0, 9.8],  # balança fiscal
        [ 9.2,   8, 18.0, 9.8, 6.5, 14, 5.5, 4.5],  # esteira principal
        [ 2.5,  62,  3.0, 1.0, 4.5,  4, 9.5, 3.0],  # iluminação
        [ 8.5,   6,  9.0, 8.4, 9.6,  5, 7.5, 8.5],  # painel elétrico
        [ 9.4,   3, 22.0, 9.4, 7.5, 16, 4.5, 5.0],  # compressor
        [ 5.5,  26,  6.0, 4.5, 6.0,  7, 8.0, 6.0],  # empilhadeira
        [ 7.0,  15,  1.5, 6.8, 5.0,  2, 9.2, 4.0],  # sensor da estufa
        [ 1.5,  88,  1.0, 0.5, 5.5,  6, 9.8, 6.5],  # sinalização de piso
        [ 8.0,  20,  7.5, 3.0, 9.9,  9, 7.0, 9.9],  # combate a incêndio
        [ 8.8,   5, 11.0, 9.0, 6.0, 10, 6.0, 4.2],  # bomba de processo
        [ 2.0,  45,  4.5, 0.5, 3.5,  5, 8.8, 2.5],  # ar-condicionado adm.
        [ 8.6,  11, 26.0, 8.6, 9.2, 20, 4.0, 8.0],  # ponte rolante
        [ 7.5,  30, 16.0, 5.0, 9.8, 24, 5.0, 9.9],  # caldeira NR-13
        [ 4.0,  34,  3.5, 3.5, 5.0,  4, 8.5, 3.5],  # portão de doca
        [ 6.5,  18,  5.5, 4.0, 8.8,  6, 7.8, 8.8],  # exaustor de pintura
        [ 8.2,   9, 14.0, 7.0, 4.0,  6, 6.8, 5.5],  # nobreak
    ], dtype=float),
    # Criticidade e segurança são CAUSAS; tempo de fila é EFEITO de má priorização.
    "dematel": np.array([
        #     crit fila custo par seg dur peça legal
        [0, 1, 3, 4, 3, 2, 1, 2],   # criticidade -> CAUSA
        [1, 0, 1, 1, 1, 0, 1, 1],   # tempo de fila -> EFEITO
        [1, 2, 0, 1, 0, 2, 2, 0],   # custo
        [3, 2, 3, 0, 2, 2, 1, 1],   # risco de parada
        [3, 2, 2, 2, 0, 1, 1, 4],   # segurança -> CAUSA de exigência legal
        [1, 2, 3, 2, 1, 0, 2, 0],   # duração
        [1, 3, 2, 2, 1, 3, 0, 0],   # disponibilidade de peça
        [2, 2, 2, 1, 3, 1, 1, 0],   # exigência legal
    ], dtype=float),
    "ahp": _saaty([1, 6, 5, 2, 0, 7, 4, 3]),   # segurança > criticidade > parada > legal > ...
}

# ===========================================================================
# 6. PROVEDORES DE NUVEM — Dynamic TOPSIS
# Fonte: SOLOMON, Tomas. "Ranking of Cloud Service Providers Using a Dynamic
#        TOPSIS Model for Provisioning of Enterprise IT Infrastructure in the
#        Cloud". Praxis (Doctor of Engineering), The George Washington
#        University, 2017. [@SAAS Solomon_gwu_0075A_13791.pdf]
# ===========================================================================
CLOUD = {
    "id_caso": "cloud_providers",
    "nome": "Seleção de provedor de nuvem corporativa",
    "dominio": "ti",
    "decisor": "Arquitetura corporativa / CIO (contrato plurianual)",
    "descricao": (
        "14 configurações de provedor, 8 critérios. O trabalho de origem usa TOPSIS "
        "**dinâmico** porque desempenho e disponibilidade de nuvem variam ao longo "
        "do contrato — o ranking de hoje não vale amanhã. E o critério que aprisiona "
        "a empresa não aparece na fatura: **portabilidade**. Migrar depois custa mais "
        "que toda a economia que motivou a escolha."),
    "criterios": [
        ("custo",         "Custo mensal",             "cost",    "US$ mil"),
        ("disponib",      "Disponibilidade (SLA)",    "benefit", "%"),
        ("desempenho",    "Desempenho",               "benefit", "0-100"),
        ("latencia",      "Latência para o Brasil",   "cost",    "ms"),
        ("seguranca",     "Segurança e certificações", "benefit", "0-10"),
        ("conformidade",  "Conformidade LGPD",        "benefit", "0-10"),
        ("suporte",       "Suporte e SLA de resposta", "benefit", "0-10"),
        ("portabilidade", "Portabilidade (sem lock-in)", "benefit", "0-10"),
    ],
    "alternativas": [
        ("C01", "Hyperscaler A — região BR"), ("C02", "Hyperscaler A — região US"),
        ("C03", "Hyperscaler B — região BR"), ("C04", "Hyperscaler B — região US"),
        ("C05", "Hyperscaler C — região BR"), ("C06", "Provedor nacional tier III"),
        ("C07", "Provedor nacional tier IV"), ("C08", "Nuvem privada gerenciada"),
        ("C09", "Colocation + hardware próprio"), ("C10", "Nuvem híbrida"),
        ("C11", "Provedor regional LATAM"), ("C12", "Bare metal dedicado"),
        ("C13", "Kubernetes gerenciado neutro"), ("C14", "On-premises modernizado"),
    ],
    "matriz": np.array([
        # custo  SLA   desemp lat  seg  LGPD  sup  portab
        [ 48.0, 99.99, 94,  12, 9.6, 9.4, 9.0, 5.5],  # hyperscaler A BR
        [ 38.0, 99.99, 96, 140, 9.6, 6.5, 9.0, 5.5],  # hyperscaler A US
        [ 46.0, 99.95, 92,  14, 9.4, 9.2, 8.8, 5.8],  # hyperscaler B BR
        [ 36.0, 99.95, 95, 135, 9.4, 6.2, 8.8, 5.8],  # hyperscaler B US
        [ 44.0, 99.95, 90,  16, 9.2, 9.0, 8.5, 6.0],  # hyperscaler C BR
        [ 29.0, 99.90, 78,  10, 8.0, 9.6, 8.0, 8.5],  # nacional tier III
        [ 37.0, 99.98, 85,   9, 8.8, 9.8, 8.6, 8.2],  # nacional tier IV
        [ 55.0, 99.95, 88,  11, 9.0, 9.5, 9.2, 7.5],  # nuvem privada gerenciada
        [ 42.0, 99.80, 82,   8, 8.4, 9.6, 6.5, 9.6],  # colocation
        [ 51.0, 99.96, 90,  13, 9.2, 9.4, 8.4, 8.8],  # híbrida
        [ 31.0, 99.85, 76,  28, 7.6, 8.2, 7.4, 8.0],  # regional LATAM
        [ 39.0, 99.90, 93,   9, 8.6, 9.5, 7.0, 9.4],  # bare metal
        [ 43.0, 99.95, 89,  15, 9.0, 9.0, 8.0, 9.8],  # k8s neutro
        [ 62.0, 99.70, 80,   5, 8.8, 9.9, 5.5, 9.9],  # on-premises
    ], dtype=float),
    # Conformidade e portabilidade são as CAUSAS estratégicas: ditam onde os
    # dados podem residir e quanto custa sair depois.
    "dematel": np.array([
        #     custo SLA des lat seg LGPD sup port
        [0, 2, 2, 1, 2, 1, 2, 1],   # custo
        [2, 0, 2, 1, 1, 1, 2, 0],   # SLA
        [3, 2, 0, 2, 0, 0, 1, 1],   # desempenho
        [1, 1, 3, 0, 0, 2, 0, 0],   # latência
        [2, 2, 1, 0, 0, 3, 2, 1],   # segurança -> conformidade
        [2, 1, 0, 3, 2, 0, 1, 3],   # conformidade -> região e portabilidade
        [2, 3, 1, 0, 1, 1, 0, 1],   # suporte
        [3, 1, 1, 1, 1, 2, 1, 0],   # portabilidade -> custo de saída
    ], dtype=float),
    "ahp": _saaty([2, 3, 6, 7, 1, 0, 5, 4]),   # LGPD > segurança > custo > SLA > ...
}

# ===========================================================================
# 7. SELEÇÃO DE STARTUPS PARA VENTURE CAPITAL
# Fontes (pasta "Startup" e "Startup/Novos"):
#   BEIM, G.; LÉVESQUE, M. "Selecting projects for venture capital funding:
#     a multiple criteria decision approach" [beim-and-levesque-vc...pdf]
#   "Multi criteria decision making for assisting business angels in
#     investments" (Technological and Economic Development) [angels.pdf]
#   DHOCHAK, M.; DOLIYA, P. "Valuation of a startup: moving towards strategic
#     approaches" (J. Multi-Criteria Decision Analysis, 2019)
#     doi:10.1002/mcda.1703 [dhochak2019.pdf]
#   AFFUL-DADZIE, E.; AFFUL-DADZIE, A.; OPLATKOVÁ, Z. K. "Assessing commercial
#     viability of technology start-up businesses in a government venture
#     capital under intuitionistic fuzzy environment" (Int. J. Fuzzy Syst.,
#     2016) doi:10.1007/s40815-016-0141-9 [afful-dadzie2016.pdf]
#   MILKOVA/ANDREICHIKOV, "Venture capitalists decision making: applying ANP"
#     (IJAHP) [egray...511-Article...pdf]
# ===========================================================================
VENTURE_CAPITAL = {
    "id_caso": "venture_capital",
    "nome": "Seleção de startups para aporte de venture capital",
    "dominio": "corporativo",
    "decisor": "Comitê de investimento de fundo de VC",
    "descricao": (
        "16 startups, 8 critérios consolidados da literatura de VC (Beim & Lévesque; "
        "Dhochak et al.; Afful-Dadzie et al.). A convergência dos trabalhos é clara "
        "e contraintuitiva para quem vem de finanças: **o time pesa mais que o "
        "produto**. Um time excepcional corrige um produto médio; o inverso não "
        "acontece. Tração é evidência, não promessa — e por isso entra como critério "
        "separado do tamanho de mercado."),
    "criterios": [
        ("time",        "Qualidade do time",        "benefit", "0-10"),
        ("mercado",     "Tamanho de mercado (TAM)", "benefit", "R$ bi"),
        ("tracao",      "Tração comprovada",        "benefit", "0-10"),
        ("valuation",   "Valuation pedido",         "cost",    "R$ mi"),
        ("queima",      "Taxa de queima mensal",    "cost",    "R$ mil"),
        ("defensavel",  "Barreira de entrada",      "benefit", "0-10"),
        ("escalab",     "Escalabilidade do modelo", "benefit", "0-10"),
        ("saida",       "Perspectiva de saída",     "benefit", "0-10"),
    ],
    "alternativas": [
        ("S01", "SaaS B2B vertical"), ("S02", "Marketplace de serviços"),
        ("S03", "Fintech de crédito"), ("S04", "Healthtech diagnóstica"),
        ("S05", "Agtech de sensoriamento"), ("S06", "Edtech corporativa"),
        ("S07", "Logtech de última milha"), ("S08", "Retailtech de estoque"),
        ("S09", "IA aplicada a jurídico"), ("S10", "Hardware conectado (IoT)"),
        ("S11", "Insurtech"), ("S12", "Proptech de locação"),
        ("S13", "Foodtech D2C"), ("S14", "Climatech de créditos"),
        ("S15", "Cybersecurity"), ("S16", "Govtech"),
    ],
    "matriz": np.array([
        # time  TAM  tração valuat queima defens escal saída
        [ 9.2,  8.5, 8.6,  42,  380, 8.0, 9.2, 8.6],  # SaaS B2B
        [ 7.8, 22.0, 7.4,  68,  920, 5.5, 8.8, 7.8],  # marketplace
        [ 8.6, 45.0, 8.0,  95,  740, 6.5, 9.0, 8.8],  # fintech crédito
        [ 9.0, 18.0, 6.4,  56,  610, 8.8, 7.6, 8.0],  # healthtech
        [ 8.2, 12.0, 7.0,  34,  290, 7.5, 7.8, 7.0],  # agtech
        [ 7.4,  9.5, 6.8,  28,  240, 5.0, 8.4, 6.5],  # edtech
        [ 8.0, 16.0, 8.2,  48,  830, 5.8, 8.0, 7.4],  # logtech
        [ 7.6, 14.0, 7.2,  38,  460, 6.0, 8.2, 7.2],  # retailtech
        [ 9.4,  6.5, 7.8,  52,  320, 9.0, 9.4, 8.4],  # IA jurídico
        [ 8.4,  7.0, 5.5,  44, 1050, 8.6, 5.8, 6.4],  # hardware IoT
        [ 8.0, 28.0, 6.6,  62,  580, 6.8, 8.6, 8.2],  # insurtech
        [ 7.2, 20.0, 6.0,  40,  520, 4.5, 8.0, 6.8],  # proptech
        [ 6.8, 11.0, 7.6,  30,  680, 3.5, 6.5, 5.5],  # foodtech
        [ 8.8, 35.0, 4.8,  70,  410, 8.4, 8.8, 7.6],  # climatech
        [ 9.6, 24.0, 8.4,  88,  560, 9.4, 9.0, 9.2],  # cybersecurity
        [ 7.0,  5.0, 6.2,  22,  180, 7.0, 6.0, 5.0],  # govtech
    ], dtype=float),
    # Time é a CAUSA RAIZ na literatura de VC: dita tração, execução e a saída.
    "dematel": np.array([
        #     time TAM trac val queima def esc saída
        [0, 0, 4, 3, 3, 3, 3, 3],   # time -> CAUSA RAIZ
        [1, 0, 2, 3, 1, 1, 2, 3],   # mercado
        [1, 1, 0, 4, 2, 1, 2, 3],   # tração -> dita valuation
        [0, 1, 1, 0, 2, 0, 1, 2],   # valuation
        [1, 0, 2, 2, 0, 0, 1, 1],   # queima
        [1, 1, 2, 2, 1, 0, 2, 2],   # defensabilidade
        [1, 2, 2, 2, 2, 1, 0, 2],   # escalabilidade
        [0, 1, 1, 2, 0, 1, 1, 0],   # saída -> EFEITO
    ], dtype=float),
    "ahp": _saaty([0, 3, 1, 5, 6, 4, 2, 7]),   # time > tração > escalab. > mercado > ...
}

# ===========================================================================
# 8. ORDENAÇÃO DE INSTRUTORES — AHP e TOPSIS
# Fonte: SILVA, C. E. J. da (ITA/UNIFESP); SALLES-NETO, L. L. de (UNIFESP);
#        SANTOS, M. dos (IME). "Modelagem matemática com os métodos AHP e
#        TOPSIS para ordenação de instrutores em uma escola da FAB".
#        LIV SBPO, Juiz de Fora, MG, 2022.
#        [ModelagemmatemticacomosmtodosAHPeTOPSIS...pdf]
# ===========================================================================
INSTRUTORES = {
    "id_caso": "instrutores",
    "nome": "Ordenação de instrutores de escola de formação",
    "dominio": "corporativo",
    "decisor": "Coordenação de ensino (designação de turmas e promoção)",
    "descricao": (
        "15 instrutores, 8 critérios. O trabalho de origem, aplicado numa escola da "
        "FAB, resolve um problema que toda instituição de ensino tem e quase nenhuma "
        "modela: a designação por antiguidade ignora avaliação discente, e a "
        "designação só por avaliação discente premia quem é popular. Nenhum dos dois "
        "critérios sozinho sustenta a decisão."),
    "criterios": [
        ("aval_discente", "Avaliação discente",     "benefit", "0-10"),
        ("titulacao",     "Titulação acadêmica",    "benefit", "0-10"),
        ("experiencia",   "Experiência docente",    "benefit", "anos"),
        ("exp_operacional", "Experiência operacional", "benefit", "anos"),
        ("producao",      "Produção técnica",       "benefit", "itens"),
        ("carga",         "Carga horária atual",    "cost",    "h/sem"),
        ("disponib",      "Disponibilidade",        "benefit", "0-10"),
        ("capacitacao",   "Capacitação continuada", "benefit", "h/ano"),
    ],
    "alternativas": [
        ("D01", "Instrutor sênior — doutorado"), ("D02", "Instrutor sênior — mestrado"),
        ("D03", "Instrutor pleno — mestrado"), ("D04", "Instrutor pleno — especialização"),
        ("D05", "Instrutor júnior — especialização"), ("D06", "Instrutor operacional sênior"),
        ("D07", "Instrutor operacional pleno"), ("D08", "Instrutor convidado — doutorado"),
        ("D09", "Instrutor de simulador"), ("D10", "Instrutor de idiomas"),
        ("D11", "Instrutor técnico de manutenção"), ("D12", "Instrutor de gestão"),
        ("D13", "Instrutor recém-formado"), ("D14", "Instrutor com pesquisa ativa"),
        ("D15", "Instrutor com dupla função"),
    ],
    "matriz": np.array([
        # aval titul exp expOp prod carga disp capac
        [ 9.2, 10.0, 18,  8,  24, 16, 7.0, 120],  # sênior doutorado
        [ 8.8,  8.0, 15,  6,  12, 18, 7.5,  80],  # sênior mestrado
        [ 8.4,  8.0,  9,  5,   8, 20, 8.0,  90],  # pleno mestrado
        [ 8.0,  6.0, 10,  7,   4, 22, 8.2,  60],  # pleno especialização
        [ 7.6,  6.0,  4,  3,   2, 24, 9.0,  70],  # júnior
        [ 8.6,  5.0, 12, 20,   6, 14, 6.5,  50],  # operacional sênior
        [ 8.2,  5.0,  7, 12,   3, 20, 7.8,  55],  # operacional pleno
        [ 9.0, 10.0,  6,  4,  32,  6, 4.0, 140],  # convidado doutorado
        [ 8.8,  6.0, 11,  9,   5, 26, 8.4,  65],  # simulador
        [ 9.4,  7.0, 14,  0,   7, 18, 8.6,  85],  # idiomas
        [ 8.0,  4.0, 13, 16,   2, 22, 7.2,  45],  # técnico de manutenção
        [ 8.6,  8.0,  8,  6,  10, 16, 7.6,  95],  # gestão
        [ 7.2,  6.0,  1,  2,   1, 28, 9.6,  75],  # recém-formado
        [ 8.4, 10.0, 10,  4,  38, 12, 6.0, 130],  # pesquisa ativa
        [ 7.8,  7.0, 12, 10,   6, 32, 5.0,  60],  # dupla função
    ], dtype=float),
    # Titulação e capacitação são CAUSAS: sustentam produção e avaliação.
    "dematel": np.array([
        #     aval tit exp expOp prod carga disp cap
        [0, 0, 1, 0, 1, 1, 1, 1],   # avaliação discente -> EFEITO
        [3, 0, 1, 0, 4, 2, 0, 3],   # titulação -> CAUSA
        [3, 1, 0, 1, 2, 2, 1, 1],   # experiência docente
        [2, 0, 1, 0, 1, 1, 1, 0],   # experiência operacional
        [2, 2, 1, 0, 0, 2, 1, 2],   # produção técnica
        [1, 0, 0, 0, 2, 0, 4, 2],   # carga horária -> CAUSA de indisponibilidade
        [1, 0, 0, 0, 1, 1, 0, 1],   # disponibilidade
        [3, 3, 1, 1, 3, 2, 1, 0],   # capacitação -> CAUSA
    ], dtype=float),
    "ahp": _saaty([0, 2, 3, 5, 4, 7, 6, 1]),   # avaliação > capacitação > titulação > ...
}

CATALOGO_ESTUDOS_KB = {c["id_caso"]: c for c in (
    ACOES, FII, FINTECH, IMOVEIS, ORDENS_SERVICO, CLOUD, VENTURE_CAPITAL, INSTRUTORES)}

if __name__ == "__main__":
    from casos.catalogo import validar
    n_alt = n_cel = 0
    for c in CATALOGO_ESTUDOS_KB.values():
        validar(c)
        a, k = len(c["alternativas"]), len(c["criterios"])
        n_alt += a; n_cel += a * k
        print(f"✅ {c['id_caso']:<22} {c['dominio']:<14} {a:>3} alt × {k} crit")
    print(f"\n{len(CATALOGO_ESTUDOS_KB)} casos · {n_alt} alternativas · {n_cel} células")
