"""
Catálogo de casos de decisão — os problemas que o motor resolve.

⚠️  NATUREZA DOS DADOS
---------------------
As matrizes de decisão abaixo são ILUSTRATIVAS e servem para demonstrar o método,
não como fonte de especificação técnica. Os valores são ordens de grandeza públicas
e plausíveis para 2025-2026, deliberadamente arredondadas; as alternativas de defesa
usam apenas dados de catálogo de fabricante amplamente divulgados. Para uma decisão
real, substitua a matriz pelos números da sua cotação, do seu edital ou do seu
laboratório de ensaio — o motor é o mesmo, os dados é que são seus.

O que NÃO é ilustrativo: a estrutura. Os critérios, as direções (benefício/custo),
a matriz causal do DEMATEL e a matriz de Saaty do AHP são a modelagem de fato do
problema, e é nelas que mora o valor do método.

ESTRUTURA DE UM CASO
--------------------
    id_caso      identificador curto, usado nas rotas do dashboard
    nome         título legível
    dominio      consumo | automotivo | defesa | corporativo | ti
    descricao    a DOR que o caso resolve (vai para o README e o dashboard)
    decisor      de quem é a preferência modelada (muda os pesos, muda o vencedor)
    criterios    [(chave, rótulo, direção, unidade), ...]
    alternativas [(chave, rótulo), ...]
    matriz       linhas = alternativas, colunas = critérios, na ordem declarada
    dematel      matriz de influência entre critérios (0..4), quadrada em `criterios`
    ahp          matriz de Saaty par a par entre critérios (1/9..9)

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import numpy as np


def _saaty(ordem_importancia, escala=2.0):
    """Gera uma matriz de Saaty CONSISTENTE a partir de uma ordem de importância.

    a_ij = p_i / p_j com p decaindo geometricamente. Por construção CR = 0: serve
    como ponto de partida honesto quando não houve elicitação par a par com o
    decisor — e o relatório diz exatamente isso, em vez de fingir um julgamento
    que ninguém fez. Substitua pela matriz real quando houver workshop de decisão.
    """
    n = len(ordem_importancia)
    p = np.array([escala ** (n - 1 - i) for i in range(n)], dtype=float)
    ordem = np.argsort(ordem_importancia)          # posição 0 = mais importante
    pesos = np.empty(n)
    pesos[ordem] = p
    return pesos[:, None] / pesos[None, :]


# ===========================================================================
# 1. CONSUMO — escolha de smartphone
# ===========================================================================
SMARTPHONE = {
    "id_caso": "smartphone",
    "nome": "Escolha de smartphone corporativo",
    "dominio": "consumo",
    "decisor": "Comprador pessoa física / gestor de frota de dispositivos",
    "descricao": (
        "Seis aparelhos, oito critérios que se contradizem: o mais barato tem a pior "
        "câmera, o de melhor câmera tem a pior bateria, e o de melhor bateria pesa "
        "mais. Uma planilha ordenada por preço elege o mais barato; ordenada por nota "
        "de review elege o mais caro. Nenhuma das duas é a resposta."),
    "criterios": [
        ("preco",      "Preço",              "cost",    "R$"),
        ("bateria",    "Bateria",            "benefit", "mAh"),
        ("camera",     "Câmera (DxOMark)",   "benefit", "pts"),
        ("desempenho", "Desempenho (CPU)",   "benefit", "pts"),
        ("tela",       "Qualidade de tela",  "benefit", "0-10"),
        ("peso",       "Peso",               "cost",    "g"),
        ("suporte",    "Anos de atualização", "benefit", "anos"),
        ("reparo",     "Custo de reparo",    "cost",    "R$"),
    ],
    "alternativas": [
        ("A", "Flagship importado"), ("B", "Flagship nacional"),
        ("C", "Intermediário premium"), ("D", "Intermediário"),
        ("E", "Robusto / uso em campo"), ("F", "Entrada corporativa"),
    ],
    "matriz": np.array([
        # preço  bateria camera cpu   tela  peso  suporte reparo
        [ 9200,   4400,  148,  2180,   9.5,  221,   7,    3400],   # A
        [ 6800,   5000,  140,  1890,   9.0,  209,   5,    2100],   # B
        [ 3900,   5000,  128,  1420,   8.2,  195,   4,    1250],   # C
        [ 2400,   5200,  116,  1050,   7.4,  188,   3,     820],   # D
        [ 4600,   6500,  108,  1180,   7.0,  268,   4,     990],   # E
        [ 1500,   4500,   96,   760,   6.5,  190,   2,     540],   # F
    ], dtype=float),
    # Influência: preço e custo de reparo são CAUSAS (restringem tudo o mais);
    # desempenho puxa bateria e peso; tela puxa bateria.
    "dematel": np.array([
        #        preco bat cam cpu tela peso sup rep
        [0, 3, 4, 4, 3, 1, 3, 2],   # preco   -> limita todo o resto
        [0, 0, 0, 1, 0, 3, 0, 0],   # bateria -> mais mAh, mais peso
        [0, 1, 0, 2, 0, 1, 0, 1],   # camera
        [0, 3, 2, 0, 0, 1, 1, 1],   # desempenho -> consome bateria
        [0, 3, 0, 1, 0, 2, 0, 2],   # tela -> consome bateria, encarece reparo
        [0, 0, 0, 0, 0, 0, 0, 0],   # peso  -> efeito puro
        [1, 0, 0, 1, 0, 0, 0, 1],   # suporte
        [2, 0, 0, 0, 1, 0, 1, 0],   # reparo
    ], dtype=float),
    "ahp": _saaty([0, 2, 3, 4, 5, 7, 1, 6]),   # preço > suporte > bateria > câmera > ...
}

# ===========================================================================
# 2. AUTOMOTIVO — carro elétrico
# ===========================================================================
VEICULO_ELETRICO = {
    "id_caso": "veiculo_eletrico",
    "nome": "Aquisição de veículo elétrico (frota e uso pessoal)",
    "dominio": "automotivo",
    "decisor": "Gestor de frota corporativa com meta de descarbonização",
    "descricao": (
        "O carro elétrico é o caso-escola do problema multicritério: autonomia, preço, "
        "tempo de recarga, rede de assistência e valor de revenda puxam para lados "
        "opostos, e o critério que decide (autonomia real, não a de catálogo) é "
        "justamente o mais difícil de medir. Comparar por preço é como escolher "
        "avião por preço de passagem sem olhar o destino."),
    "criterios": [
        ("preco",      "Preço de aquisição",   "cost",    "R$ mil"),
        ("autonomia",  "Autonomia real",       "benefit", "km"),
        ("recarga",    "Tempo de recarga 10-80%", "cost", "min"),
        ("consumo",    "Consumo energético",   "cost",    "kWh/100km"),
        ("rede",       "Rede de assistência",  "benefit", "0-10"),
        ("revenda",    "Retenção de valor 3a", "benefit", "%"),
        ("porta_malas", "Porta-malas",         "benefit", "L"),
        ("seguranca",  "Segurança (NCAP)",     "benefit", "pts"),
    ],
    "alternativas": [
        ("EV1", "SUV elétrico premium"), ("EV2", "Sedã elétrico executivo"),
        ("EV3", "Hatch elétrico urbano"), ("EV4", "SUV elétrico chinês"),
        ("EV5", "Picape elétrica"), ("EV6", "Híbrido plug-in"),
        ("EV7", "Compacto elétrico de entrada"),
    ],
    "matriz": np.array([
        # preço autonomia recarga consumo rede revenda malas ncap
        [ 480,   520,   22,  18.5,  8.5,  61,  520,  92],   # EV1
        [ 350,   480,   28,  16.2,  8.0,  58,  460,  90],   # EV2
        [ 240,   330,   35,  14.0,  7.5,  52,  350,  86],   # EV3
        [ 210,   400,   30,  15.8,  6.0,  44,  430,  88],   # EV4
        [ 520,   380,   40,  24.0,  7.0,  63,  900,  85],   # EV5
        [ 290,   680,   45,  12.5,  9.0,  66,  400,  89],   # EV6 (autonomia combinada)
        [ 150,   250,   50,  13.2,  5.5,  40,  290,  78],   # EV7
    ], dtype=float),
    # Autonomia e consumo são CAUSAS técnicas; revenda e preço são efeitos de mercado.
    "dematel": np.array([
        #      preco auto rec cons rede rev malas seg
        [0, 3, 2, 1, 2, 3, 2, 3],   # preco
        [2, 0, 3, 3, 1, 3, 1, 0],   # autonomia -> dita recarga, consumo, revenda
        [1, 2, 0, 1, 2, 2, 0, 0],   # recarga
        [2, 4, 2, 0, 0, 2, 1, 0],   # consumo -> causa raiz da autonomia
        [1, 0, 2, 0, 0, 3, 0, 1],   # rede
        [1, 0, 0, 0, 1, 0, 0, 0],   # revenda -> efeito
        [1, 1, 0, 2, 0, 1, 0, 1],   # porta-malas
        [2, 1, 0, 1, 1, 2, 0, 0],   # segurança
    ], dtype=float),
    "ahp": _saaty([1, 0, 4, 3, 5, 2, 7, 6]),   # autonomia > preço > revenda > consumo > ...
}

# ===========================================================================
# 3. DEFESA — aeronave de caça multifunção
# ===========================================================================
CACA_MULTIFUNCAO = {
    "id_caso": "caca_multifuncao",
    "nome": "Aquisição de aeronave de caça multifunção",
    "dominio": "defesa",
    "decisor": "Comissão de avaliação de força aérea (decisão de Estado, 30 anos)",
    "descricao": (
        "Compra de ciclo de vida de 30 anos, irreversível, sob escrutínio público e "
        "geopolítico. O preço unitário responde por menos de um terço do custo total; "
        "transferência de tecnologia e custo por hora de voo decidem o orçamento das "
        "próximas três décadas. É o caso em que uma planilha de preços não apenas "
        "falha — ela induz o erro caro."),
    "criterios": [
        ("preco_unit",  "Preço unitário",          "cost",    "US$ mi"),
        ("custo_hora",  "Custo por hora de voo",   "cost",    "US$ mil"),
        ("raio",        "Raio de combate",         "benefit", "km"),
        ("carga",       "Carga bélica",            "benefit", "t"),
        ("sensores",    "Aviônica e sensores",     "benefit", "0-10"),
        ("furtividade", "Assinatura radar",        "benefit", "0-10"),
        ("tot",         "Transferência de tecnologia", "benefit", "%"),
        ("disponib",    "Disponibilidade de frota", "benefit", "%"),
        ("interop",     "Interoperabilidade OTAN", "benefit", "0-10"),
    ],
    "alternativas": [
        ("C1", "Caça 5ª geração furtivo"), ("C2", "Caça 4.5ª geração europeu"),
        ("C3", "Caça 4.5ª geração nórdico"), ("C4", "Caça 4.5ª geração oriental"),
        ("C5", "Caça naval embarcado"), ("C6", "Caça leve de baixo custo"),
    ],
    "matriz": np.array([
        # preço  h.voo  raio carga sens furt  ToT  disp interop
        [  95,   42,  1100,  8.2,  9.8,  9.5,  15,  72,  9.5],   # C1
        [  85,   28,  1400,  9.0,  8.8,  6.0,  55,  84,  9.0],   # C2
        [  70,   14,  1300,  7.2,  8.5,  6.5,  85,  88,  8.5],   # C3
        [  55,   22,  1500,  8.0,  7.5,  5.5,  70,  76,  4.0],   # C4
        [ 110,   38,   900,  8.8,  9.0,  6.8,  20,  70,  9.2],   # C5
        [  32,    9,   700,  3.6,  6.5,  4.0,  60,  90,  6.5],   # C6
    ], dtype=float),
    # ToT e custo/hora são as CAUSAS estruturais: ditam disponibilidade e orçamento.
    "dematel": np.array([
        #     preco hora raio carga sens furt ToT disp inter
        [0, 2, 1, 1, 2, 2, 2, 1, 1],   # preço unitário
        [3, 0, 1, 0, 1, 1, 2, 4, 0],   # custo/hora -> dita disponibilidade
        [2, 2, 0, 2, 1, 0, 0, 1, 0],   # raio
        [2, 2, 2, 0, 1, 2, 0, 1, 1],   # carga
        [3, 2, 1, 1, 0, 3, 2, 2, 3],   # sensores
        [4, 3, 1, 2, 2, 0, 3, 2, 1],   # furtividade -> encarece tudo
        [2, 3, 0, 0, 2, 1, 0, 4, 2],   # ToT -> causa raiz de soberania logística
        [1, 1, 0, 0, 0, 0, 0, 0, 0],   # disponibilidade -> efeito
        [1, 1, 0, 1, 2, 0, 1, 1, 0],   # interoperabilidade
    ], dtype=float),
    "ahp": _saaty([4, 2, 5, 6, 3, 7, 0, 1, 8]),   # ToT > disponibilidade > custo/hora > ...
}

# ===========================================================================
# 4. DEFESA — viatura blindada de combate
# ===========================================================================
BLINDADO = {
    "id_caso": "blindado",
    "nome": "Aquisição de viatura blindada de combate",
    "dominio": "defesa",
    "decisor": "Comissão de material bélico do Exército",
    "descricao": (
        "O triângulo clássico do blindado — proteção, mobilidade e poder de fogo — é "
        "matematicamente insolúvel: cada tonelada de blindagem compra sobrevivência e "
        "vende mobilidade, e nenhuma soma ponderada ingênua captura isso. Some "
        "nacionalização e pressão logística de manutenção em campanha, e você tem o "
        "problema multicritério em estado puro."),
    "criterios": [
        ("preco",        "Preço unitário",       "cost",    "R$ mi"),
        ("protecao",     "Nível de proteção",    "benefit", "STANAG"),
        ("mobilidade",   "Mobilidade",           "benefit", "km/h"),
        ("autonomia",    "Autonomia",            "benefit", "km"),
        ("fogo",         "Poder de fogo",        "benefit", "0-10"),
        ("peso",         "Peso de combate",      "cost",    "t"),
        ("manutencao",   "Custo de manutenção",  "cost",    "R$ mil/ano"),
        ("nacionaliz",   "Índice de nacionalização", "benefit", "%"),
    ],
    "alternativas": [
        ("B1", "Carro de combate pesado"), ("B2", "Blindado de rodas 8x8"),
        ("B3", "Blindado de rodas 6x6 nacional"), ("B4", "Viatura leve multiuso"),
        ("B5", "Blindado de esteiras médio"),
    ],
    "matriz": np.array([
        # preço prot mobil auton fogo peso manut nacion
        [ 42,   6,   68,   450,  9.5,  62,  980,  12],   # B1
        [ 18,   4,   100,  800,  7.0,  28,  420,  35],   # B2
        [ 11,   3,   105,  750,  5.5,  20,  260,  78],   # B3
        [  4,   2,   120,  600,  3.0,   9,  120,  85],   # B4
        [ 26,   5,   70,   500,  8.0,  45,  700,  22],   # B5
    ], dtype=float),
    "dematel": np.array([
        #     preco prot mob auton fogo peso manut nac
        [0, 2, 1, 1, 2, 1, 2, 2],   # preço
        [3, 0, 3, 2, 1, 4, 3, 1],   # proteção -> pesa, logo tira mobilidade
        [1, 0, 0, 2, 0, 1, 2, 0],   # mobilidade
        [1, 0, 2, 0, 0, 2, 1, 0],   # autonomia
        [3, 1, 2, 1, 0, 3, 2, 1],   # poder de fogo
        [3, 1, 4, 3, 1, 0, 3, 0],   # peso -> causa raiz da mobilidade
        [2, 0, 1, 1, 0, 0, 0, 2],   # manutenção
        [2, 1, 0, 0, 1, 0, 3, 0],   # nacionalização -> baixa manutenção no longo prazo
    ], dtype=float),
    "ahp": _saaty([3, 0, 2, 5, 1, 6, 4, 7]),   # proteção > fogo > mobilidade > preço > ...
}

# ===========================================================================
# 5. CORPORATIVO — priorização de portfólio de projetos / startups
# ===========================================================================
PORTFOLIO_STARTUP = {
    "id_caso": "portfolio_startup",
    "nome": "Priorização de portfólio de projetos e startups",
    "dominio": "corporativo",
    "decisor": "Comitê de investimento / board de aceleradora",
    "descricao": (
        "Sete iniciativas competindo pelo mesmo capital e pelo mesmo time. O comitê "
        "que decide por retorno esperado sempre elege a aposta mais arriscada, porque "
        "valor esperado ignora a cauda. Aqui o risco entra como CRITÉRIO — "
        "probabilidade de perda e pior cenário plausível — e não como nota de rodapé "
        "do slide 14."),
    "criterios": [
        ("vpl",        "VPL esperado",           "benefit", "R$ mil"),
        ("tir",        "TIR",                    "benefit", "%"),
        ("payback",    "Payback descontado",     "cost",    "meses"),
        ("prob_perda", "P(VPL < 0)",             "cost",    "%"),
        ("var5",       "VaR 5% (pior caso)",     "benefit", "R$ mil"),
        ("tam",        "Tamanho de mercado",     "benefit", "0-10"),
        ("time",       "Maturidade do time",     "benefit", "0-10"),
        ("esforco",    "Esforço de engenharia",  "cost",    "pessoa-mês"),
        ("estrategia", "Aderência estratégica",  "benefit", "0-10"),
    ],
    "alternativas": [
        ("P1", "Plataforma SaaS B2B"), ("P2", "Marketplace vertical"),
        ("P3", "Produto de IA aplicada"), ("P4", "Expansão internacional"),
        ("P5", "Automação interna"), ("P6", "Hardware conectado"),
        ("P7", "Serviço de dados por assinatura"),
    ],
    "matriz": np.array([
        # vpl    tir  payb p_perda  var5   tam time esforço estrat
        [ 4200,  38,  22,   18,     -380,  8.5, 8.0,  96,  9.0],   # P1
        [ 6800,  52,  31,   34,    -2100,  9.2, 6.5, 168,  7.5],   # P2
        [ 5100,  61,  17,   27,     -900,  9.5, 7.0,  72,  9.5],   # P3
        [ 9500,  44,  40,   41,    -4200,  8.8, 5.5, 240,  6.0],   # P4
        [ 1800,  29,  11,    7,      210,  5.0, 9.0,  36,  8.0],   # P5
        [ 3400,  33,  36,   38,    -1800,  7.0, 6.0, 200,  5.5],   # P6
        [ 2900,  46,  15,   12,      -90,  7.8, 8.5,  54,  8.8],   # P7
    ], dtype=float),
    "dematel": np.array([
        #     vpl tir payb pperda var5 tam time esf estrat
        [0, 3, 2, 2, 3, 0, 0, 0, 1],   # vpl
        [3, 0, 3, 2, 2, 0, 0, 0, 0],   # tir
        [2, 3, 0, 2, 1, 0, 0, 2, 0],   # payback
        [3, 3, 2, 0, 4, 0, 0, 0, 0],   # P(perda) -> dita o VaR
        [3, 2, 1, 3, 0, 0, 0, 0, 0],   # VaR
        [3, 3, 2, 2, 2, 0, 0, 1, 2],   # tamanho de mercado -> CAUSA de tudo
        [2, 2, 3, 3, 2, 0, 0, 3, 1],   # time -> CAUSA: executa ou não
        [2, 2, 3, 2, 2, 0, 0, 0, 0],   # esforço
        [2, 1, 1, 1, 1, 2, 2, 1, 0],   # aderência estratégica
    ], dtype=float),
    "ahp": _saaty([0, 3, 5, 2, 4, 6, 1, 8, 7]),   # vpl > time > p_perda > tir > var5 > ...
}

# ===========================================================================
# 6. TI — estação de trabalho de engenharia
# ===========================================================================
ESTACAO_TRABALHO = {
    "id_caso": "estacao_trabalho",
    "nome": "Padronização de estação de trabalho de engenharia",
    "dominio": "ti",
    "decisor": "Coordenação de infraestrutura de TI (compra de 200 unidades)",
    "descricao": (
        "Decisão que se multiplica por 200 e dura quatro anos. O erro de escolher "
        "pela ficha técnica é ignorar que autonomia e garantia on-site valem mais, no "
        "custo total de posse, do que dois pontos de benchmark sintético que ninguém "
        "vai sentir."),
    "criterios": [
        ("preco",     "Preço unitário",        "cost",    "R$"),
        ("cpu",       "Desempenho multicore",  "benefit", "pts"),
        ("gpu",       "Desempenho gráfico",    "benefit", "pts"),
        ("ram",       "Memória",               "benefit", "GB"),
        ("autonomia", "Autonomia de bateria",  "benefit", "h"),
        ("peso",      "Peso",                  "cost",    "kg"),
        ("garantia",  "Garantia on-site",      "benefit", "anos"),
        ("ruido",     "Ruído sob carga",       "cost",    "dB"),
    ],
    "alternativas": [
        ("W1", "Workstation móvel topo"), ("W2", "Notebook profissional 14\""),
        ("W3", "Ultrabook executivo"), ("W4", "Notebook corporativo padrão"),
        ("W5", "Desktop compacto + monitor"), ("W6", "Notebook gamer reaproveitado"),
    ],
    "matriz": np.array([
        # preço  cpu   gpu   ram  auton peso garantia ruído
        [ 21000, 24800, 18500,  64,  5.5, 2.3,  3,  48],   # W1
        [ 12500, 17200,  6400,  32,  9.0, 1.4,  3,  41],   # W2
        [  9800, 12600,  3100,  16, 12.0, 1.1,  2,  36],   # W3
        [  6200,  9400,  2200,  16,  8.0, 1.6,  1,  43],   # W4
        [  8900, 21000, 12000,  32, 24.0, 6.5,  3,  39],   # W5 (autonomia = nobreak)
        [ 11000, 19500, 16800,  32,  4.0, 2.7,  1,  53],   # W6
    ], dtype=float),
    "dematel": np.array([
        #     preco cpu gpu ram auton peso gar ruido
        [0, 3, 3, 3, 1, 1, 3, 1],   # preço
        [3, 0, 1, 1, 3, 2, 0, 4],   # cpu -> consome bateria e faz ruído
        [3, 1, 0, 1, 4, 3, 0, 4],   # gpu -> causa raiz de calor/ruído/autonomia
        [2, 1, 0, 0, 1, 1, 0, 0],   # ram
        [1, 0, 0, 0, 0, 2, 0, 0],   # autonomia -> efeito
        [1, 0, 0, 0, 1, 0, 0, 1],   # peso
        [2, 0, 0, 0, 0, 0, 0, 0],   # garantia
        [0, 0, 0, 0, 0, 0, 0, 0],   # ruído -> efeito puro
    ], dtype=float),
    "ahp": _saaty([0, 2, 5, 4, 1, 6, 3, 7]),   # preço > autonomia > cpu > garantia > ...
}


CATALOGO = {c["id_caso"]: c for c in (
    SMARTPHONE, VEICULO_ELETRICO, CACA_MULTIFUNCAO,
    BLINDADO, PORTFOLIO_STARTUP, ESTACAO_TRABALHO)}


def listar():
    """(id_caso, nome, domínio, nº alternativas, nº critérios) de cada caso."""
    return [(c["id_caso"], c["nome"], c["dominio"],
             len(c["alternativas"]), len(c["criterios"]))
            for c in CATALOGO.values()]


def obter(id_caso):
    if id_caso not in CATALOGO:
        raise KeyError(f"caso desconhecido: {id_caso!r}. "
                       f"Disponíveis: {', '.join(CATALOGO)}")
    return CATALOGO[id_caso]


def validar(caso):
    """Confere que as matrizes do caso são consistentes entre si.

    Um caso mal formado produz um ranking que PARECE certo — números saem, gráficos
    desenham — e está errado em silêncio. Por isso a validação é dura e roda antes
    de qualquer carga no banco.
    """
    id_caso = caso["id_caso"]
    n_alt, n_crit = len(caso["alternativas"]), len(caso["criterios"])
    erros = []

    if caso["matriz"].shape != (n_alt, n_crit):
        erros.append(f"matriz {caso['matriz'].shape} != esperado ({n_alt}, {n_crit})")
    if caso["dematel"].shape != (n_crit, n_crit):
        erros.append(f"dematel {caso['dematel'].shape} != ({n_crit}, {n_crit})")
    if caso["ahp"].shape != (n_crit, n_crit):
        erros.append(f"ahp {caso['ahp'].shape} != ({n_crit}, {n_crit})")
    if not np.allclose(np.diag(caso["dematel"]), 0):
        erros.append("diagonal do DEMATEL deve ser zero (critério não influencia a si mesmo)")
    if not np.allclose(np.diag(caso["ahp"]), 1):
        erros.append("diagonal do AHP deve ser 1")
    if not np.allclose(caso["ahp"] * caso["ahp"].T, 1):
        erros.append("matriz do AHP deve ser recíproca: a_ij · a_ji = 1")
    if not np.isfinite(caso["matriz"]).all():
        erros.append("matriz de decisão tem NaN ou infinito")
    direcoes = {d for _, _, d, _ in caso["criterios"]}
    if not direcoes <= {"benefit", "cost"}:
        erros.append(f"direções inválidas: {direcoes - {'benefit', 'cost'}}")
    for j, (chave, _, _, _) in enumerate(caso["criterios"]):
        if np.ptp(caso["matriz"][:, j]) == 0:
            erros.append(f"critério {chave!r} é constante — não discrimina nada, remova-o")

    if erros:
        raise ValueError(f"caso {id_caso!r} inválido:\n  - " + "\n  - ".join(erros))
    return True


if __name__ == "__main__":
    print(f"{'ID':<20} {'DOMÍNIO':<12} {'ALT':>4} {'CRIT':>5}  NOME")
    print("-" * 100)
    for id_caso, nome, dominio, n_a, n_c in listar():
        validar(CATALOGO[id_caso])
        print(f"{id_caso:<20} {dominio:<12} {n_a:>4} {n_c:>5}  {nome}")
    print(f"\n✅ {len(CATALOGO)} casos válidos "
          f"({sum(len(c['alternativas']) for c in CATALOGO.values())} alternativas, "
          f"{sum(len(c['criterios']) for c in CATALOGO.values())} critérios no total)")
