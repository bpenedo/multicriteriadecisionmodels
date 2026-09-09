"""
Estudos de caso de PRODUTOS — 9 domínios, ~312 alternativas.

⚠️  NATUREZA DOS DADOS — leia antes de usar
--------------------------------------------
As matrizes abaixo são ILUSTRATIVAS. Os valores são ordens de grandeza públicas e
plausíveis para 2025-2026, deliberadamente arredondadas, e servem para DEMONSTRAR O
MÉTODO — não como ficha técnica. Especificações de produto mudam por versão, mercado,
configuração e ano-modelo; nenhum número aqui foi verificado contra o fabricante.

Para uma decisão real, substitua a matriz pelos números da SUA cotação, do SEU edital
ou do SEU ensaio — o motor é o mesmo, os dados é que são seus.

O que NÃO é ilustrativo: a MODELAGEM. Os critérios, suas direções (benefício/custo),
a matriz causal do DEMATEL e a matriz de Saaty representam a estrutura real de cada
decisão, e é nelas que mora o valor do método.

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import numpy as np

from casos.catalogo import _saaty

# ===========================================================================
# 1. CARROS ELÉTRICOS E HÍBRIDOS (2025/2026+) — 38 alternativas
# ===========================================================================
_EV_ALT = [
    ("byd_seal", "BYD Seal"), ("porsche_taycan", "Porsche Taycan"),
    ("tesla_m3", "Tesla Model 3"), ("amg_gt", "Mercedes AMG GT 2026"),
    ("haval_h8gt", "Haval H8 GT"), ("cybertruck", "Tesla Cybertruck"),
    ("cybercab", "Tesla Cybercab"), ("xiaomi_su7", "Xiaomi SU7"),
    ("byd_dolphin", "BYD Dolphin"), ("byd_yuan", "BYD Yuan Plus"),
    ("tesla_my", "Tesla Model Y"), ("tesla_ms", "Tesla Model S"),
    ("macan_ev", "Porsche Macan EV"), ("volvo_ex30", "Volvo EX30"),
    ("volvo_xc40", "Volvo XC40 Recharge"), ("audi_etrongt", "Audi e-tron GT"),
    ("bmw_i4", "BMW i4"), ("bmw_ix", "BMW iX"),
    ("blazer_ev", "Chevrolet Blazer EV"), ("mach_e", "Ford Mustang Mach-E"),
    ("ioniq5", "Hyundai Ioniq 5"), ("kia_ev6", "Kia EV6"),
    ("ariya", "Nissan Ariya"), ("vw_id4", "Volkswagen ID.4"),
    ("ora03", "GWM Ora 03"), ("megane_et", "Renault Megane E-Tech"),
    ("e208", "Peugeot e-208"), ("fiat_500e", "Fiat 500e"),
    ("prologue", "Honda Prologue"), ("rivian_r1t", "Rivian R1T"),
    ("lucid_air", "Lucid Air"), ("polestar2", "Polestar 2"),
    ("lexus_rz", "Lexus RZ"), ("eqe", "Mercedes-Benz EQE"),
    ("eletre", "Lotus Eletre"), ("zeekr001", "Zeekr 001"),
    ("lyriq", "Cadillac Lyriq"), ("nevera", "Rimac Nevera"),
]
_EV_CRIT = [
    ("preco",      "Preço",                 "cost",    "R$ mil"),
    ("autonomia",  "Autonomia real",        "benefit", "km"),
    ("potencia",   "Potência",              "benefit", "cv"),
    ("recarga",    "Recarga 10-80%",        "cost",    "min"),
    ("consumo",    "Consumo",               "cost",    "kWh/100km"),
    ("malas",      "Porta-malas",           "benefit", "L"),
    ("seguranca",  "Segurança (NCAP)",      "benefit", "pts"),
    ("rede",       "Rede de assistência",   "benefit", "0-10"),
    ("revenda",    "Retenção de valor 3a",  "benefit", "%"),
]
_EV_X = np.array([
    # preço  auton  pot  rec  cons malas seg rede rev
    [ 300,  520,  530,  26, 16.8, 400, 89, 6.5, 52],  # BYD Seal
    [ 780,  480,  680,  18, 20.5, 407, 92, 8.0, 58],  # Porsche Taycan
    [ 280,  510,  394,  25, 14.5, 594, 93, 8.5, 62],  # Tesla Model 3
    [1100,  400,  816,  22, 24.0, 321, 88, 7.5, 55],  # AMG GT
    [ 240,  420,  340,  30, 17.5, 480, 85, 5.5, 44],  # Haval H8 GT
    [ 620,  480,  845,  28, 26.0, 1897, 82, 7.0, 50],  # Cybertruck
    [ 180,  400,  250,  30, 15.0, 350, 84, 7.0, 45],  # Cybercab
    [ 260,  560,  673,  20, 15.8, 517, 90, 5.0, 48],  # Xiaomi SU7
    [ 150,  340,  204,  32, 13.2, 345, 84, 6.5, 46],  # BYD Dolphin
    [ 210,  380,  204,  30, 15.5, 440, 86, 6.5, 47],  # BYD Yuan Plus
    [ 320,  480,  384,  27, 16.2, 854, 91, 8.5, 60],  # Tesla Model Y
    [ 600,  600,  680,  20, 17.0, 793, 92, 8.5, 57],  # Tesla Model S
    [ 560,  550,  639,  21, 18.5, 540, 91, 8.0, 61],  # Porsche Macan EV
    [ 230,  380,  272,  28, 15.0, 318, 90, 7.5, 53],  # Volvo EX30
    [ 320,  400,  408,  33, 18.8, 452, 93, 7.5, 51],  # Volvo XC40
    [ 720,  480,  598,  19, 19.5, 405, 90, 7.5, 56],  # Audi e-tron GT
    [ 400,  490,  340,  31, 16.0, 470, 91, 8.0, 54],  # BMW i4
    [ 620,  560,  523,  25, 19.8, 500, 92, 8.0, 55],  # BMW iX
    [ 350,  450,  340,  30, 19.0, 705, 87, 6.5, 44],  # Blazer EV
    [ 340,  440,  346,  32, 18.2, 470, 90, 7.0, 46],  # Mach-E
    [ 330,  460,  325,  18, 17.0, 527, 92, 7.5, 55],  # Ioniq 5
    [ 340,  470,  325,  18, 16.5, 480, 91, 7.5, 54],  # Kia EV6
    [ 300,  400,  394,  35, 18.0, 466, 90, 7.0, 45],  # Ariya
    [ 290,  420,  299,  30, 17.2, 543, 91, 7.5, 48],  # VW ID.4
    [ 160,  310,  171,  38, 14.0, 228, 82, 5.0, 40],  # Ora 03
    [ 240,  390,  218,  30, 15.4, 440, 89, 7.0, 47],  # Megane E-Tech
    [ 200,  330,  156,  30, 14.8, 311, 87, 7.0, 45],  # e-208
    [ 190,  300,  118,  35, 14.2, 185, 86, 7.0, 49],  # Fiat 500e
    [ 310,  450,  288,  32, 18.5, 700, 88, 7.5, 44],  # Honda Prologue
    [ 480,  510,  665,  30, 22.0, 1130, 89, 6.0, 52],  # Rivian R1T
    [ 700,  700,  819,  20, 15.0, 456, 91, 6.0, 50],  # Lucid Air
    [ 290,  440,  408,  33, 17.5, 405, 92, 7.0, 49],  # Polestar 2
    [ 360,  380,  313,  30, 18.0, 522, 91, 7.5, 52],  # Lexus RZ
    [ 560,  550,  292,  32, 17.8, 430, 92, 8.0, 53],  # Mercedes EQE
    [ 750,  480,  918,  20, 21.5, 688, 88, 5.5, 46],  # Lotus Eletre
    [ 350,  580,  544,  22, 17.0, 539, 89, 5.5, 45],  # Zeekr 001
    [ 420,  490,  528,  31, 19.2, 793, 90, 6.5, 47],  # Cadillac Lyriq
    [12000, 490, 1914,  19, 25.0, 300, 85, 4.0, 65],  # Rimac Nevera
], dtype=float)
# Consumo é a CAUSA técnica: dita autonomia e recarga. Potência causa consumo.
# Preço e revenda são efeitos de mercado.
_EV_DEMATEL = np.array([
    #      pre aut pot rec con mal seg red rev
    [0, 3, 3, 1, 1, 2, 3, 3, 3],   # preço
    [2, 0, 1, 3, 2, 1, 0, 1, 3],   # autonomia
    [3, 3, 0, 2, 4, 1, 1, 1, 2],   # potência -> consumo
    [1, 2, 0, 0, 1, 0, 0, 2, 2],   # recarga
    [2, 4, 1, 3, 0, 1, 0, 0, 2],   # consumo -> CAUSA RAIZ
    [1, 1, 0, 0, 1, 0, 1, 0, 1],   # porta-malas
    [2, 0, 1, 0, 1, 1, 0, 1, 2],   # segurança
    [1, 0, 0, 1, 0, 0, 1, 0, 3],   # rede -> revenda
    [1, 0, 0, 0, 0, 0, 0, 0, 0],   # revenda -> EFEITO puro
], dtype=float)
CARROS_ELETRICOS = {
    "id_caso": "carros_eletricos",
    "nome": "Carros elétricos e híbridos (2025/2026+)",
    "dominio": "automotivo",
    "decisor": "Comprador/gestor de frota com meta de descarbonização",
    "descricao": (
        "38 veículos, 9 critérios que se contradizem. O mais rápido é o que mais "
        "consome; o de maior autonomia raramente é o de recarga mais rápida; e a "
        "rede de assistência — que decide o custo dos próximos cinco anos — não "
        "aparece em nenhuma comparação de revista."),
    "criterios": _EV_CRIT, "alternativas": _EV_ALT, "matriz": _EV_X,
    "dematel": _EV_DEMATEL,
    "ahp": _saaty([1, 0, 6, 4, 3, 7, 2, 5, 8]),   # autonomia > preço > segurança > ...
}

# ===========================================================================
# 2. SMARTPHONES (2025/2026) — 38 alternativas
# ===========================================================================
_SP_ALT = [
    ("s26_ultra", "Samsung Galaxy S26 Ultra"), ("iph17_pro", "Apple iPhone 17 Pro"),
    ("xiaomi16p", "Xiaomi 16 Pro"), ("edge60u", "Motorola Edge 60 Ultra"),
    ("pixel10", "Google Pixel 10"), ("realme_gt6", "Realme GT 6"),
    ("honor_m7", "Honor Magic 7"), ("rog9", "Asus ROG Phone 9"),
    ("op13", "OnePlus 13"), ("xperia1v7", "Sony Xperia 1 VII"),
    ("vivo_x100p", "Vivo X100 Pro"), ("oppo_fx8", "Oppo Find X8"),
    ("nothing3", "Nothing Phone (3)"), ("phantom_v", "Tecno Phantom V"),
    ("infinix40", "Infinix Zero 40"), ("zte_axon60", "ZTE Axon 60"),
    ("redmagic10", "Nubia RedMagic 10"), ("meizu21", "Meizu 21"),
    ("fairphone5", "Fairphone 5"), ("htc_u24p", "HTC U24 Pro"),
    ("aquos_r9", "Sharp Aquos R9"), ("poco_f7p", "Poco F7 Pro"),
    ("redmi_n15", "Redmi Note 15"), ("zfold8", "Samsung Galaxy Z Fold 8"),
    ("razr60", "Motorola Razr 60"), ("mate70", "Huawei Mate 70"),
    ("nokia_g60", "Nokia G60"), ("legion_ph", "Lenovo Legion Phone"),
    ("tcl50xl", "TCL 50 XL"), ("bv9300", "Blackview BV9300"),
    ("s25", "Samsung Galaxy S25"), ("iph17", "Apple iPhone 17"),
    ("xiaomi16", "Xiaomi 16"), ("moto_g85", "Motorola Moto G85"),
    ("htc_one", "HTC One (linha)"), ("realme13p", "Realme 13 Pro"),
    ("honor200", "Honor 200"), ("pixel10a", "Google Pixel 10a"),
]
_SP_CRIT = [
    ("preco",     "Preço",                "cost",    "R$"),
    ("bateria",   "Bateria",              "benefit", "mAh"),
    ("camera",    "Câmera",               "benefit", "pts"),
    ("cpu",       "Desempenho",           "benefit", "mil pts"),
    ("tela",      "Qualidade de tela",    "benefit", "0-10"),
    ("peso",      "Peso",                 "cost",    "g"),
    ("suporte",   "Anos de atualização",  "benefit", "anos"),
    ("armazen",   "Armazenamento",        "benefit", "GB"),
    ("carga",     "Potência de carga",    "benefit", "W"),
]
_SP_X = np.array([
    # preço  bat  cam   cpu  tela peso sup arm carga
    [ 9800, 5000, 154, 2900, 9.8, 218,  7, 512, 45],  # S26 Ultra
    [10500, 4700, 158, 2750, 9.7, 206,  7, 256, 35],  # iPhone 17 Pro
    [ 7200, 6100, 152, 2850, 9.6, 213,  5, 512, 120],  # Xiaomi 16 Pro
    [ 5500, 5000, 140, 1980, 9.2, 197,  4, 512, 125],  # Edge 60 Ultra
    [ 6800, 5060, 156, 1850, 9.4, 207,  7, 256, 45],  # Pixel 10
    [ 3200, 5500, 128, 1720, 8.8, 199,  3, 256, 120],  # Realme GT 6
    [ 6200, 5850, 148, 2700, 9.5, 202,  5, 512, 100],  # Honor Magic 7
    [ 8500, 5800, 130, 2950, 9.3, 227,  4, 512, 65],  # ROG Phone 9
    [ 6500, 6000, 145, 2880, 9.5, 210,  5, 512, 100],  # OnePlus 13
    [ 8900, 5000, 150, 2100, 9.6, 192,  4, 256, 30],  # Xperia 1 VII
    [ 6900, 5400, 155, 2200, 9.5, 221,  4, 512, 100],  # Vivo X100 Pro
    [ 6600, 5630, 151, 2350, 9.4, 193,  5, 256, 80],  # Oppo Find X8
    [ 4800, 5000, 132, 1650, 9.0, 197,  5, 256, 45],  # Nothing Phone 3
    [ 5200, 5000, 126, 1450, 8.9, 209,  3, 256, 45],  # Tecno Phantom V
    [ 2200, 5000, 118, 1100, 8.4, 195,  2, 256, 45],  # Infinix Zero 40
    [ 3900, 5100, 130, 1600, 8.9, 198,  3, 256, 80],  # ZTE Axon 60
    [ 6800, 6500, 128, 2900, 9.2, 229,  3, 512, 80],  # RedMagic 10
    [ 3500, 5000, 124, 1750, 8.8, 190,  3, 256, 80],  # Meizu 21
    [ 4500, 4200, 108, 820, 7.8, 212,  8, 256, 30],  # Fairphone 5
    [ 3800, 4600, 120, 1250, 8.6, 195,  3, 256, 60],  # HTC U24 Pro
    [ 6500, 5000, 142, 1800, 9.3, 197,  4, 256, 45],  # Aquos R9
    [ 3400, 6000, 126, 2100, 9.0, 206,  4, 256, 90],  # Poco F7 Pro
    [ 1900, 5500, 112, 980, 8.2, 191,  3, 256, 45],  # Redmi Note 15
    [15500, 4600, 145, 2800, 9.6, 239,  7, 512, 45],  # Z Fold 8
    [ 8200, 4200, 130, 1700, 9.1, 189,  4, 256, 45],  # Razr 60
    [ 8800, 5300, 157, 2400, 9.5, 214,  4, 512, 88],  # Mate 70
    [ 1800, 4500, 104, 620, 7.6, 190,  3, 128, 20],  # Nokia G60
    [ 5900, 5500, 122, 2600, 9.1, 235,  3, 512, 68],  # Legion Phone
    [ 1500, 5010, 100, 560, 7.4, 205,  2, 128, 18],  # TCL 50 XL
    [ 2400, 15080, 96, 700, 7.2, 425,  2, 256, 33],  # Blackview BV9300
    [ 6900, 4900, 146, 2450, 9.5, 196,  7, 256, 45],  # S25
    [ 7800, 4400, 148, 2500, 9.4, 199,  7, 128, 30],  # iPhone 17
    [ 5400, 5800, 144, 2600, 9.4, 205,  5, 256, 90],  # Xiaomi 16
    [ 2100, 5000, 110, 780, 8.0, 186,  3, 256, 30],  # Moto G85
    [ 2900, 4400, 114, 950, 8.3, 188,  2, 128, 25],  # HTC One
    [ 2600, 5200, 122, 1350, 8.7, 192,  3, 256, 80],  # Realme 13 Pro
    [ 3600, 5200, 136, 1500, 9.0, 187,  4, 256, 100],  # Honor 200
    [ 3900, 4500, 138, 1200, 8.9, 190,  7, 128, 30],  # Pixel 10a
], dtype=float)
# Desempenho e tela CAUSAM consumo de bateria; preço limita tudo.
_SP_DEMATEL = np.array([
    #      pre bat cam cpu tela pes sup arm car
    [0, 3, 4, 4, 3, 1, 3, 3, 2],   # preço
    [0, 0, 0, 1, 0, 3, 0, 0, 2],   # bateria -> peso
    [1, 1, 0, 2, 0, 1, 0, 2, 0],   # câmera
    [1, 4, 2, 0, 0, 1, 1, 1, 1],   # cpu -> CAUSA de consumo
    [1, 3, 0, 1, 0, 2, 0, 0, 0],   # tela -> consome bateria
    [0, 0, 0, 0, 0, 0, 0, 0, 0],   # peso -> EFEITO puro
    [1, 0, 0, 1, 0, 0, 0, 0, 0],   # suporte
    [1, 0, 1, 1, 0, 1, 0, 0, 0],   # armazenamento
    [1, 2, 0, 0, 0, 1, 0, 0, 0],   # carga
], dtype=float)
SMARTPHONES_2026 = {
    "id_caso": "smartphones_2026",
    "nome": "Smartphones (2025/2026)",
    "dominio": "consumo",
    "decisor": "Comprador pessoa física / gestor de frota de dispositivos",
    "descricao": (
        "38 aparelhos, 9 critérios em conflito direto. O de melhor câmera não é o de "
        "melhor bateria; o mais potente é o mais pesado; e o critério que decide o "
        "custo real — anos de atualização — é o que ninguém compara na loja."),
    "criterios": _SP_CRIT, "alternativas": _SP_ALT, "matriz": _SP_X,
    "dematel": _SP_DEMATEL,
    "ahp": _saaty([0, 3, 2, 4, 5, 8, 1, 6, 7]),   # preço > suporte > câmera > bateria > ...
}

# ===========================================================================
# 3. TABLETS — 34 alternativas
# ===========================================================================
_TB_ALT = [
    ("ipad_pro_m4", "iPad Pro M4"), ("ipad_air_m2", "iPad Air M2"),
    ("ipad_mini7", "iPad Mini 7"), ("tab_s10u", "Galaxy Tab S10 Ultra"),
    ("tab_s9fe", "Galaxy Tab S9 FE"), ("xiaomi_pad7p", "Xiaomi Pad 7 Pro"),
    ("lenovo_p12", "Lenovo Tab P12"), ("yoga_tab13", "Lenovo Yoga Tab 13"),
    ("oneplus_pad2", "OnePlus Pad 2"), ("pixel_tablet", "Google Pixel Tablet"),
    ("fire_hd10", "Amazon Fire HD 10"), ("matepad_pro", "Huawei MatePad Pro"),
    ("oppo_pad2", "Oppo Pad 2"), ("vivo_pad3", "Vivo Pad 3"),
    ("surface_p11", "Microsoft Surface Pro 11"), ("honor_pad9", "Honor Pad 9"),
    ("realme_pad2", "Realme Pad 2"), ("nokia_t21", "Nokia T21"),
    ("bv_tab18", "Blackview Tab 18"), ("chuwi_hipadx", "Chuwi HiPad X"),
    ("teclast_t60", "Teclast T60"), ("alldocube50", "Alldocube iPlay 50"),
    ("htc_a103", "HTC A103"), ("doogee_t30p", "Doogee T30 Pro"),
    ("acer_endt1", "Acer Enduro T1"), ("zenbook_fold", "Asus Zenbook Fold"),
    ("toughbook", "Panasonic Toughbook"), ("tcl_nxt14", "TCL NxtPaper 14"),
    ("x1_fold", "Lenovo ThinkPad X1 Fold"), ("fusion5_10", "Fusion5 10"),
    ("tab_s10p", "Galaxy Tab S10+"), ("ipad_10", "iPad 10ª geração"),
    ("xiaomi_pad7", "Xiaomi Pad 7"), ("lenovo_m11", "Lenovo Tab M11"),
]
_TB_CRIT = [
    ("preco",   "Preço",               "cost",    "R$"),
    ("tela",    "Tamanho de tela",     "benefit", "pol"),
    ("cpu",     "Desempenho",          "benefit", "mil pts"),
    ("bateria", "Autonomia",           "benefit", "h"),
    ("peso",    "Peso",                "cost",    "g"),
    ("armazen", "Armazenamento",       "benefit", "GB"),
    ("caneta",  "Suporte a caneta",    "benefit", "0-10"),
    ("suporte", "Anos de atualização", "benefit", "anos"),
]
_TB_X = np.array([
    # preço  tela  cpu  bat  peso arm caneta sup
    [14000, 13.0, 2600, 10.0, 582, 512, 10, 6],  # iPad Pro M4
    [ 7500, 13.0, 1850,  9.5, 617, 256,  9, 6],  # iPad Air M2
    [ 5200,  8.3, 1650, 10.0, 293, 128,  9, 6],  # iPad Mini 7
    [12500, 14.6, 2100,  9.0, 723, 512, 10, 7],  # Tab S10 Ultra
    [ 3800, 10.9,  620, 11.0, 523, 128,  8, 4],  # Tab S9 FE
    [ 4200, 11.2, 1550,  9.5, 500, 256,  8, 3],  # Xiaomi Pad 7 Pro
    [ 3600, 12.7,  580, 10.0, 615, 128,  7, 3],  # Lenovo Tab P12
    [ 3900, 13.0,  520,  9.0, 830, 128,  6, 2],  # Yoga Tab 13
    [ 4500, 12.1, 1720,  9.5, 584, 256,  8, 4],  # OnePlus Pad 2
    [ 3500, 10.9,  680, 11.0, 493, 128,  5, 5],  # Pixel Tablet
    [ 1200, 10.1,  280, 12.0, 434,  64,  3, 3],  # Fire HD 10
    [ 6800, 12.2, 1400, 10.0, 508, 256,  9, 3],  # MatePad Pro
    [ 3200, 11.6,  980, 10.5, 552, 128,  7, 3],  # Oppo Pad 2
    [ 3100, 12.1, 1050, 10.0, 570, 128,  7, 3],  # Vivo Pad 3
    [11500, 13.0, 1900, 10.0, 895, 512,  9, 8],  # Surface Pro 11
    [ 2400, 12.1,  560, 11.0, 555, 128,  6, 3],  # Honor Pad 9
    [ 1600, 11.5,  340, 10.0, 520,  64,  4, 2],  # Realme Pad 2
    [ 1500, 10.4,  260,  9.0, 466,  64,  3, 3],  # Nokia T21
    [ 1300, 12.0,  310, 11.0, 620, 128,  4, 2],  # Blackview Tab 18
    [ 1400, 10.5,  290, 10.0, 540,  64,  3, 2],  # Chuwi HiPad X
    [ 1500, 12.0,  330, 10.0, 590, 128,  4, 2],  # Teclast T60
    [ 1100, 10.4,  250, 10.0, 510,  64,  3, 2],  # Alldocube iPlay 50
    [ 1200, 10.1,  240,  9.5, 500,  64,  3, 2],  # HTC A103
    [ 1600, 11.0,  350, 12.0, 640, 256,  4, 2],  # Doogee T30 Pro
    [ 3400, 10.1,  420, 13.0, 700, 128,  5, 4],  # Acer Enduro T1
    [16000, 17.3, 1600,  8.0, 1100, 512, 7, 6],  # Zenbook Fold
    [15000, 10.1,  700, 14.0, 1200, 256, 6, 8],  # Toughbook
    [ 2900, 14.0,  480, 11.0, 700, 256,  6, 3],  # TCL NxtPaper 14
    [18000, 16.3, 1750,  9.0, 1280, 512, 8, 7],  # ThinkPad X1 Fold
    [  900, 10.1,  220,  9.0, 480,  64,  2, 1],  # Fusion5 10
    [ 9500, 12.4, 2050, 10.0, 571, 256, 10, 7],  # Tab S10+
    [ 3300, 10.9,  980, 10.0, 477,  64,  6, 5],  # iPad 10
    [ 3000, 11.0, 1200, 10.5, 500, 128,  7, 3],  # Xiaomi Pad 7
    [ 1400, 11.0,  380, 10.0, 520, 128,  5, 3],  # Lenovo Tab M11
], dtype=float)
_TB_DEMATEL = np.array([
    #      pre tela cpu bat pes arm can sup
    [0, 3, 4, 2, 2, 3, 3, 3],   # preço
    [2, 0, 1, 2, 4, 0, 2, 0],   # tela -> peso e bateria
    [3, 1, 0, 3, 1, 1, 1, 1],   # cpu -> consome bateria
    [1, 0, 0, 0, 2, 0, 0, 0],   # bateria -> peso
    [0, 0, 0, 0, 0, 0, 0, 0],   # peso -> EFEITO
    [1, 0, 1, 0, 0, 0, 0, 0],   # armazenamento
    [2, 1, 1, 0, 0, 0, 0, 1],   # caneta
    [1, 0, 1, 0, 0, 0, 0, 0],   # suporte
], dtype=float)
TABLETS = {
    "id_caso": "tablets",
    "nome": "Tablets",
    "dominio": "consumo",
    "decisor": "Comprador para produtividade, estudo ou uso em campo",
    "descricao": (
        "34 tablets, 8 critérios. Tela maior custa peso e bateria; desempenho custa "
        "bateria; e o critério que define a vida útil real — anos de atualização — "
        "varia de 1 a 8 anos entre modelos de preço parecido."),
    "criterios": _TB_CRIT, "alternativas": _TB_ALT, "matriz": _TB_X,
    "dematel": _TB_DEMATEL,
    "ahp": _saaty([0, 3, 2, 4, 6, 5, 7, 1]),   # preço > suporte > cpu > tela > ...
}

# ===========================================================================
# 4. SMARTWATCHES E WEARABLES — 31 alternativas
# ===========================================================================
_SW_ALT = [
    ("huawei_gt7", "Huawei Watch GT 7"), ("aw_s11", "Apple Watch Series 11"),
    ("aw_ultra3", "Apple Watch Ultra 3"), ("gw8_ultra", "Galaxy Watch 8 Ultra"),
    ("gt7_pro", "Huawei Watch GT 7 Pro"), ("fenix8", "Garmin Fenix 8"),
    ("fr965", "Garmin Forerunner 965"), ("trex3", "Amazfit T-Rex 3"),
    ("gtr4", "Amazfit GTR 4"), ("fitbit_s3", "Fitbit Sense 3"),
    ("pixel_w3", "Google Pixel Watch 3"), ("op_watch2", "OnePlus Watch 2"),
    ("xiaomi_s4", "Xiaomi Watch S4"), ("ticwatch_p5", "TicWatch Pro 5"),
    ("polar_v3", "Polar Vantage V3"), ("suunto_race", "Suunto Race"),
    ("gshock_h2000", "Casio G-Shock GBD-H2000"), ("coros_pace3", "Coros Pace 3"),
    ("scanwatch2", "Withings ScanWatch 2"), ("citizen_cz", "Citizen CZ Smart"),
    ("fossil_g6", "Fossil Gen 6"), ("mk_gen6", "Michael Kors Gen 6"),
    ("venu3", "Garmin Venu 3"), ("watch_fit3", "Huawei Watch Fit 3"),
    ("redmi_w5", "Redmi Watch 5"), ("galaxy_fit3", "Samsung Galaxy Fit 3"),
    ("bip5", "Amazfit Bip 5"), ("oura4", "Oura Ring Gen 4"),
    ("ultrahuman", "Ultrahuman Ring Air"), ("galaxy_ring", "Samsung Galaxy Ring"),
    ("charge6", "Fitbit Charge 6"),
]
_SW_CRIT = [
    ("preco",      "Preço",                "cost",    "R$"),
    ("autonomia",  "Autonomia",            "benefit", "dias"),
    ("sensores",   "Conjunto de sensores", "benefit", "0-10"),
    ("gps",        "Precisão de GPS",      "benefit", "0-10"),
    ("resistencia", "Resistência à água",  "benefit", "ATM"),
    ("peso",       "Peso",                 "cost",    "g"),
    ("tela",       "Qualidade de tela",    "benefit", "0-10"),
    ("ecossistema", "Ecossistema/apps",    "benefit", "0-10"),
]
_SW_X = np.array([
    # preço  aut sens gps atm peso tela eco
    [ 2200, 14,  8.5, 8.0,  5, 48, 9.0, 7.0],  # Huawei GT 7
    [ 4800,  1.5, 9.5, 9.0,  5, 39, 9.6, 9.8],  # AW Series 11
    [ 7900,  3,  9.6, 9.5, 10, 61, 9.5, 9.8],  # AW Ultra 3
    [ 5200,  3,  9.4, 9.0, 10, 60, 9.4, 9.2],  # GW8 Ultra
    [ 3100, 14,  8.8, 8.5,  5, 53, 9.1, 7.0],  # GT 7 Pro
    [ 8500, 16,  9.5, 9.8, 10, 79, 9.0, 8.0],  # Fenix 8
    [ 5400, 15,  9.0, 9.7,  5, 53, 8.9, 8.0],  # Forerunner 965
    [ 2400, 20,  8.4, 8.6, 10, 68, 8.7, 6.5],  # T-Rex 3
    [ 1500, 14,  8.0, 8.0,  5, 34, 8.6, 6.5],  # GTR 4
    [ 2600,  6,  9.2, 7.5,  5, 40, 8.8, 8.5],  # Fitbit Sense 3
    [ 3200,  1.5, 9.0, 8.5,  5, 31, 9.2, 9.0],  # Pixel Watch 3
    [ 1900, 10,  8.2, 8.2,  5, 49, 8.8, 7.5],  # OnePlus Watch 2
    [ 1300, 15,  8.0, 8.0,  5, 44, 8.9, 6.8],  # Xiaomi Watch S4
    [ 2100,  3,  8.6, 8.4,  5, 44, 8.9, 8.8],  # TicWatch Pro 5
    [ 4900, 12,  9.1, 9.4, 10, 57, 8.5, 7.0],  # Polar Vantage V3
    [ 3600, 12,  8.8, 9.3, 10, 69, 8.6, 6.8],  # Suunto Race
    [ 1800, 60,  7.0, 7.5, 20, 63, 6.5, 5.0],  # G-Shock GBD-H2000
    [ 1400, 24,  8.2, 9.0,  5, 30, 8.0, 6.0],  # Coros Pace 3
    [ 2700, 30,  8.6, 6.5,  5, 34, 7.2, 7.5],  # ScanWatch 2
    [ 2300,  2,  7.4, 7.0,  3, 52, 8.4, 7.0],  # Citizen CZ Smart
    [ 1600,  1.5, 7.0, 6.8,  3, 43, 8.2, 7.2],  # Fossil Gen 6
    [ 1900,  1.5, 7.0, 6.8,  3, 45, 8.2, 7.2],  # MK Gen 6
    [ 3400, 14,  9.0, 9.2,  5, 47, 9.0, 8.0],  # Venu 3
    [  900, 10,  7.6, 7.8,  5, 26, 8.5, 6.5],  # Watch Fit 3
    [  600, 18,  7.0, 7.0,  5, 32, 8.3, 5.5],  # Redmi Watch 5
    [  450, 13,  6.8, 6.0,  5, 19, 7.8, 7.0],  # Galaxy Fit 3
    [  400, 10,  6.5, 6.5,  5, 26, 7.6, 5.5],  # Amazfit Bip 5
    [ 2500,  7,  9.3, 4.0, 10,  4, 1.0, 8.0],  # Oura Ring Gen 4
    [ 2100,  6,  9.0, 4.0, 10,  3, 1.0, 7.0],  # Ultrahuman Ring Air
    [ 2400,  7,  9.1, 4.0, 10,  3, 1.0, 8.5],  # Galaxy Ring
    [  900,  7,  8.4, 7.2,  5, 30, 7.9, 8.0],  # Fitbit Charge 6
], dtype=float)
# Tela e GPS CAUSAM consumo (autonomia); sensores encarecem e pesam.
_SW_DEMATEL = np.array([
    #      pre aut sen gps atm pes tel eco
    [0, 2, 4, 3, 2, 1, 3, 3],   # preço
    [1, 0, 0, 0, 0, 2, 0, 0],   # autonomia -> peso (bateria maior)
    [3, 3, 0, 1, 1, 2, 0, 2],   # sensores -> consomem bateria
    [2, 4, 1, 0, 0, 1, 0, 1],   # GPS -> CAUSA RAIZ de consumo
    [2, 0, 0, 0, 0, 3, 0, 0],   # resistência -> peso
    [0, 0, 0, 0, 0, 0, 0, 0],   # peso -> EFEITO puro
    [3, 4, 0, 0, 0, 1, 0, 1],   # tela -> maior CAUSA de consumo
    [2, 0, 1, 1, 0, 0, 1, 0],   # ecossistema
], dtype=float)
SMARTWATCHES = {
    "id_caso": "smartwatches",
    "nome": "Smartwatches e wearables",
    "dominio": "consumo",
    "decisor": "Usuário de esporte/saúde ou comprador corporativo de wearables",
    "descricao": (
        "31 dispositivos, 8 critérios, e o trade-off mais brutal da categoria: tela "
        "boa e GPS preciso destroem autonomia. Um relógio de 1,5 dia e outro de 60 "
        "dias concorrem na mesma prateleira — e os anéis inteligentes vencem em "
        "sensores enquanto perdem em tela por não terem nenhuma."),
    "criterios": _SW_CRIT, "alternativas": _SW_ALT, "matriz": _SW_X,
    "dematel": _SW_DEMATEL,
    "ahp": _saaty([0, 1, 2, 4, 6, 7, 5, 3]),   # preço > autonomia > sensores > eco > ...
}

# ===========================================================================
# 5. NOTEBOOKS E COMPUTADORES — 32 alternativas
# ===========================================================================
_NB_ALT = [
    ("mbp_m4", "MacBook Pro M4"), ("mba_m3", "MacBook Air M3"),
    ("dell_xps13", "Dell XPS 13"), ("dell_insp15", "Dell Inspiron 15"),
    ("hp_spectre", "HP Spectre x360"), ("hp_pavilion", "HP Pavilion"),
    ("x1_carbon", "ThinkPad X1 Carbon"), ("ideapad3", "Lenovo IdeaPad 3"),
    ("zenbook14", "Asus Zenbook 14"), ("rog_g14", "Asus ROG Zephyrus G14"),
    ("predator_h", "Acer Predator Helios"), ("aspire5", "Acer Aspire 5"),
    ("gbook4u", "Samsung Galaxy Book4 Ultra"), ("lg_gram17", "LG Gram 17"),
    ("msi_raider", "MSI Raider"), ("razer_b16", "Razer Blade 16"),
    ("surface_l7", "Surface Laptop 7"), ("alienware_m16", "Alienware m16"),
    ("legion_p5", "Lenovo Legion Pro 5"), ("imac_m3", "Apple iMac M3"),
    ("mac_studio", "Mac Studio"), ("optiplex", "Dell OptiPlex"),
    ("elitebook", "HP EliteBook"), ("vivobook", "Asus Vivobook"),
    ("m70q", "ThinkCentre M70q"), ("aorus", "Gigabyte Aorus"),
    ("yoga_slim7", "Lenovo Yoga Slim 7"), ("vaio_fe15", "VAIO FE15"),
    ("chromebook_p", "Chromebook Plus"), ("toughbook55", "Panasonic Toughbook 55"),
    ("macbook", "MacBook (base)"), ("dell_22gb", "Dell 22 GB RAM"),
]
_NB_CRIT = [
    ("preco",     "Preço",              "cost",    "R$"),
    ("cpu",       "Desempenho multicore", "benefit", "pts"),
    ("gpu",       "Desempenho gráfico", "benefit", "pts"),
    ("ram",       "Memória",            "benefit", "GB"),
    ("autonomia", "Autonomia",          "benefit", "h"),
    ("peso",      "Peso",               "cost",    "kg"),
    ("tela",      "Qualidade de tela",  "benefit", "0-10"),
    ("armazen",   "Armazenamento",      "benefit", "GB"),
]
_NB_X = np.array([
    # preço   cpu    gpu   ram aut  peso tela arm
    [22000, 22500, 16800, 24, 18.0, 1.6, 9.7, 1024],  # MacBook Pro M4
    [12500, 14200,  8500, 16, 18.0, 1.2, 9.2,  512],  # MacBook Air M3
    [13500, 15800,  6200, 16, 12.0, 1.2, 9.4,  512],  # Dell XPS 13
    [ 4200,  7800,  2100, 16,  7.0, 1.9, 7.6,  512],  # Inspiron 15
    [11000, 14500,  5800, 16, 13.0, 1.4, 9.3,  512],  # Spectre x360
    [ 4500,  8200,  2400, 16,  8.0, 1.8, 7.8,  512],  # Pavilion
    [15000, 15200,  5900, 32, 15.0, 1.1, 9.1, 1024],  # X1 Carbon
    [ 3200,  6400,  1800,  8,  7.5, 1.9, 7.2,  256],  # IdeaPad 3
    [ 8500, 13800,  5200, 16, 14.0, 1.3, 9.2,  512],  # Zenbook 14
    [16500, 19200, 21500, 32, 10.0, 1.5, 9.4, 1024],  # ROG Zephyrus G14
    [14000, 18500, 24000, 32,  6.0, 2.6, 9.0, 1024],  # Predator Helios
    [ 3800,  7200,  2000, 16,  8.5, 1.8, 7.5,  512],  # Aspire 5
    [17000, 18800, 19500, 32, 13.0, 1.6, 9.6, 1024],  # Galaxy Book4 Ultra
    [12000, 13200,  4800, 16, 17.0, 1.4, 8.8, 1024],  # LG Gram 17
    [19000, 20500, 26000, 32,  5.5, 2.9, 9.2, 2048],  # MSI Raider
    [24000, 21000, 25000, 32,  7.0, 2.2, 9.6, 1024],  # Razer Blade 16
    [11500, 14800,  5500, 16, 16.0, 1.4, 9.3,  512],  # Surface Laptop 7
    [18000, 19800, 23000, 32,  6.5, 2.7, 9.1, 1024],  # Alienware m16
    [12500, 17500, 20000, 32,  8.0, 2.5, 8.9, 1024],  # Legion Pro 5
    [14000, 14000,  9500, 16,  0.1, 4.4, 9.5,  512],  # iMac M3 (desktop)
    [21000, 24500, 22000, 32,  0.1, 2.7, 1.0, 1024],  # Mac Studio (sem tela)
    [ 5500,  9500,  2200, 16,  0.1, 4.0, 1.0,  512],  # OptiPlex (sem tela)
    [ 9800, 12500,  4200, 16, 14.0, 1.4, 8.6,  512],  # EliteBook
    [ 4800,  9800,  3200, 16,  9.0, 1.7, 8.0,  512],  # Vivobook
    [ 4200,  8800,  2000, 16,  0.1, 1.3, 1.0,  512],  # ThinkCentre M70q
    [13000, 17000, 18500, 32,  7.0, 2.4, 8.8, 1024],  # Gigabyte Aorus
    [ 7500, 12000,  4500, 16, 15.0, 1.3, 9.0,  512],  # Yoga Slim 7
    [ 3500,  6800,  1700,  8,  8.0, 1.7, 7.0,  256],  # VAIO FE15
    [ 2800,  5200,  1500,  8, 12.0, 1.4, 7.4,  128],  # Chromebook Plus
    [21000, 11500,  3500, 32, 16.0, 2.1, 7.5, 1024],  # Toughbook 55
    [ 9500, 12800,  7200, 16, 17.0, 1.3, 9.0,  256],  # MacBook (base)
    [ 5200,  9200,  2600, 22,  8.0, 1.9, 7.9,  512],  # Dell 22 GB
], dtype=float)
# GPU é a CAUSA RAIZ: dita consumo (autonomia), calor e peso.
_NB_DEMATEL = np.array([
    #      pre cpu gpu ram aut pes tel arm
    [0, 4, 4, 3, 1, 1, 3, 3],   # preço
    [3, 0, 1, 1, 3, 2, 0, 0],   # cpu -> consome bateria
    [4, 1, 0, 1, 4, 3, 1, 0],   # gpu -> CAUSA RAIZ
    [2, 1, 0, 0, 1, 1, 0, 0],   # ram
    [1, 0, 0, 0, 0, 2, 0, 0],   # autonomia -> peso (bateria)
    [1, 0, 0, 0, 1, 0, 0, 0],   # peso
    [3, 0, 1, 0, 2, 1, 0, 0],   # tela -> consome bateria
    [2, 0, 0, 0, 0, 0, 0, 0],   # armazenamento
], dtype=float)
NOTEBOOKS = {
    "id_caso": "notebooks",
    "nome": "Notebooks e computadores",
    "dominio": "ti",
    "decisor": "Coordenação de TI ou profissional que decide sua ferramenta de trabalho",
    "descricao": (
        "32 máquinas, 8 critérios. A GPU é a causa raiz de tudo o que incomoda: "
        "consumo, calor, peso e preço. E desktops entram na mesma comparação com "
        "autonomia ~0 e sem tela — o que testa se o método sabe lidar com "
        "alternativas estruturalmente diferentes."),
    "criterios": _NB_CRIT, "alternativas": _NB_ALT, "matriz": _NB_X,
    "dematel": _NB_DEMATEL,
    "ahp": _saaty([0, 2, 5, 3, 1, 6, 4, 7]),   # preço > autonomia > cpu > ram > ...
}

# ===========================================================================
# 6. TRATORES E MAQUINÁRIO AGRÍCOLA PESADO — 35 alternativas
# ===========================================================================
_AG_ALT = [
    ("massey", "Massey Ferguson"), ("john_deere", "John Deere"),
    ("caterpillar", "Caterpillar"), ("tatu", "Tatu Marchesan"), ("case", "Case IH"),
    ("new_holland", "New Holland"), ("valtra", "Valtra"), ("kubota", "Kubota"),
    ("claas", "Claas"), ("fendt", "Fendt"), ("jcb", "JCB"), ("yanmar", "Yanmar"),
    ("ls_tractor", "LS Tractor"), ("mahindra", "Mahindra"), ("deutz", "Deutz-Fahr"),
    ("stara", "Stara"), ("jacto", "Jacto"), ("baldan", "Baldan"), ("budny", "Budny"),
    ("agrale", "Agrale"), ("montana", "Montana"), ("solis", "Solis"),
    ("landini", "Landini"), ("mccormick", "McCormick"), ("challenger", "Challenger"),
    ("versatile", "Versatile"), ("zoomlion", "Zoomlion"), ("lovol", "Lovol"),
    ("iseki", "Iseki"), ("same", "SAME"), ("hurlimann", "Hürlimann"),
    ("zetor", "Zetor"), ("rostselmash", "Rostselmash"), ("gomselmash", "Gomselmash"),
    ("valmet", "Valtra (linha pesada)"),
]
_AG_CRIT = [
    ("preco",       "Preço",                   "cost",    "R$ mil"),
    ("potencia",    "Potência",                "benefit", "cv"),
    ("consumo",     "Consumo de combustível",  "cost",    "L/h"),
    ("capacidade",  "Capacidade operacional",  "benefit", "0-10"),
    ("rede",        "Rede de assistência BR",  "benefit", "0-10"),
    ("manutencao",  "Custo de manutenção",     "cost",    "R$ mil/ano"),
    ("tecnologia",  "Tecnologia embarcada",    "benefit", "0-10"),
    ("nacionaliz",  "Índice de nacionalização", "benefit", "%"),
]
_AG_X = np.array([
    # preço pot  cons cap rede manut tec nac
    [ 620, 180, 18.0, 8.0, 9.5,  42, 7.5, 62],  # Massey Ferguson
    [ 890, 260, 22.0, 9.5, 9.8,  55, 9.5, 48],  # John Deere
    [1250, 420, 34.0, 9.8, 9.0,  78, 9.2, 22],  # Caterpillar
    [ 180,  90,  9.0, 6.0, 8.5,  18, 5.0, 92],  # Tatu Marchesan
    [ 780, 240, 21.0, 9.0, 9.2,  52, 9.0, 45],  # Case IH
    [ 720, 230, 20.5, 8.8, 9.3,  48, 8.6, 52],  # New Holland
    [ 680, 210, 19.0, 8.5, 9.4,  45, 8.4, 68],  # Valtra
    [ 420, 140, 13.0, 7.5, 7.0,  32, 8.0, 15],  # Kubota
    [ 950, 300, 24.0, 9.4, 7.5,  62, 9.4, 12],  # Claas
    [1150, 380, 26.0, 9.7, 7.0,  70, 9.8, 10],  # Fendt
    [ 640, 200, 19.5, 8.0, 7.2,  46, 8.2, 14],  # JCB
    [ 380, 120, 11.5, 7.0, 6.5,  28, 7.6, 12],  # Yanmar
    [ 320, 110, 12.0, 6.8, 6.0,  26, 6.5, 10],  # LS Tractor
    [ 340, 115, 12.5, 6.9, 6.2,  25, 6.2, 18],  # Mahindra
    [ 700, 220, 20.0, 8.6, 6.8,  50, 8.8, 12],  # Deutz-Fahr
    [ 560, 170, 16.0, 8.2, 9.0,  36, 8.5, 88],  # Stara
    [ 480, 150, 14.0, 8.4, 9.6,  30, 8.8, 95],  # Jacto
    [ 210,  95,  9.5, 6.2, 9.0,  19, 5.2, 96],  # Baldan
    [ 240, 100, 10.0, 6.4, 8.2,  20, 5.5, 90],  # Budny
    [ 400, 130, 13.5, 7.2, 8.8,  29, 6.8, 82],  # Agrale
    [ 290, 105, 11.0, 6.6, 8.0,  23, 6.0, 78],  # Montana
    [ 260, 100, 11.5, 6.5, 5.5,  22, 5.8,  8],  # Solis
    [ 590, 190, 18.5, 8.1, 6.4,  42, 8.0, 11],  # Landini
    [ 610, 195, 18.8, 8.2, 6.3,  43, 8.1, 11],  # McCormick
    [1080, 350, 28.0, 9.5, 7.8,  66, 9.0, 18],  # Challenger
    [1180, 400, 32.0, 9.6, 6.5,  74, 8.6, 10],  # Versatile
    [ 450, 160, 16.5, 7.6, 5.0,  34, 7.4,  6],  # Zoomlion
    [ 360, 130, 14.0, 7.0, 4.8,  27, 6.6,  6],  # Lovol
    [ 330, 115, 12.0, 6.8, 5.2,  25, 7.0,  8],  # Iseki
    [ 660, 205, 19.2, 8.3, 6.0,  47, 8.3, 10],  # SAME
    [ 650, 200, 19.0, 8.2, 5.8,  46, 8.2, 10],  # Hürlimann
    [ 370, 125, 13.0, 7.1, 5.6,  28, 6.4, 12],  # Zetor
    [ 820, 280, 26.0, 9.0, 4.5,  58, 7.8,  5],  # Rostselmash
    [ 700, 250, 25.0, 8.6, 4.2,  54, 7.2,  5],  # Gomselmash
    [ 760, 240, 21.5, 8.9, 9.4,  50, 8.9, 70],  # Valtra pesada
], dtype=float)
# Potência é a CAUSA: dita consumo, manutenção e preço. Nacionalização
# reduz manutenção no longo prazo. Rede é a alavanca de disponibilidade.
_AG_DEMATEL = np.array([
    #      pre pot con cap red man tec nac
    [0, 2, 1, 2, 1, 2, 3, 2],   # preço
    [4, 0, 4, 3, 0, 3, 1, 0],   # potência -> CAUSA RAIZ
    [2, 1, 0, 1, 0, 2, 0, 0],   # consumo
    [3, 2, 2, 0, 1, 2, 2, 0],   # capacidade
    [2, 0, 0, 2, 0, 3, 1, 3],   # rede -> manutenção
    [2, 0, 1, 1, 1, 0, 0, 0],   # manutenção
    [3, 1, 2, 3, 1, 2, 0, 0],   # tecnologia
    [3, 0, 0, 0, 2, 3, 0, 0],   # nacionalização -> baixa manutenção
], dtype=float)
MAQUINARIO_AGRICOLA = {
    "id_caso": "maquinario_agricola",
    "nome": "Tratores e maquinário agrícola pesado",
    "dominio": "agronegocio",
    "decisor": "Produtor rural / gestor de frota agrícola (ciclo de 10-15 anos)",
    "descricao": (
        "35 marcas de tratores, colheitadeiras, pivôs e pulverizadores. Aqui o preço "
        "de compra é a menor parte da conta: consumo de combustível, custo de "
        "manutenção e — sobretudo — **rede de assistência** decidem se a máquina para "
        "no meio da safra. Nacionalização não é patriotismo: é peça disponível."),
    "criterios": _AG_CRIT, "alternativas": _AG_ALT, "matriz": _AG_X,
    "dematel": _AG_DEMATEL,
    "ahp": _saaty([2, 4, 3, 5, 0, 1, 6, 7]),   # rede > manutenção > preço > consumo > ...
}

# ===========================================================================
# 7. COMPUTADORES DE PLACA ÚNICA (SBCs) E IoT — 33 alternativas
# ===========================================================================
_SBC_ALT = [
    ("rpi5", "Raspberry Pi 5"), ("rock64", "Rock64"), ("lattepanda", "LattePanda"),
    ("rpi_zero2w", "Raspberry Pi Zero 2 W"), ("opi5plus", "Orange Pi 5 Plus"),
    ("bpi_m5", "Banana Pi M5"), ("rockpi4", "RockPi 4"),
    ("tinker2", "ASUS Tinker Board 2"), ("odroid_n2", "Odroid N2+"),
    ("bbb", "BeagleBone Black"), ("jetson_nano", "Nvidia Jetson Nano"),
    ("khadas_vim4", "Khadas VIM4"), ("pine64", "Pine64"),
    ("radxa_rock5b", "Radxa Rock 5B"), ("le_potato", "Libre Le Potato"),
    ("omega2", "Onion Omega2"), ("arduino_r4", "Arduino Uno R4"),
    ("esp32", "ESP32 Wroom"), ("teensy41", "Teensy 4.1"),
    ("particle_boron", "Particle Boron"), ("xiao", "Seeed Studio Xiao"),
    ("up_board", "Up Board"), ("milkv_duo", "Milk-V Duo"),
    ("mangopi", "MangoPi MQ Dual"), ("vocore2", "VoCore2"),
    ("nanopi_r4s", "NanoPi R4S"), ("friendlyelec_cm3", "FriendlyElec CM3"),
    ("clockworkpi", "ClockworkPi"), ("microbit2", "BBC Micro:bit V2"),
    ("rp2040", "Waveshare RP2040"), ("m5stack", "M5Stack Core2"),
    ("pyboard", "Pyboard"), ("rpi4", "Raspberry Pi 4"),
]
_SBC_CRIT = [
    ("preco",        "Preço",                 "cost",    "US$"),
    ("cpu",          "Desempenho de CPU",     "benefit", "pts"),
    ("ram",          "Memória",               "benefit", "GB"),
    ("gpio",         "Pinos de GPIO",         "benefit", "n"),
    ("consumo",      "Consumo",               "cost",    "W"),
    ("comunidade",   "Comunidade e docs",     "benefit", "0-10"),
    ("io",           "Conectividade e I/O",   "benefit", "0-10"),
    ("disponib",     "Disponibilidade",       "benefit", "0-10"),
]
_SBC_X = np.array([
    # preço  cpu   ram  gpio cons com  io  disp
    [  80, 1250,  8.0, 40,  7.5, 10.0, 9.0, 9.0],  # Raspberry Pi 5
    [  45,  480,  4.0, 40,  4.5,  6.0, 7.0, 5.5],  # Rock64
    [ 140,  620,  4.0, 20,  8.0,  6.5, 8.5, 6.0],  # LattePanda
    [  15,  210,  0.5, 40,  1.2,  9.5, 5.0, 7.5],  # Pi Zero 2 W
    [ 150, 1580, 16.0, 40,  9.0,  7.0, 9.5, 7.0],  # Orange Pi 5 Plus
    [  55,  420,  4.0, 40,  4.0,  6.5, 7.0, 6.5],  # Banana Pi M5
    [  75,  560,  4.0, 40,  5.0,  6.8, 7.5, 6.0],  # RockPi 4
    [ 130,  680,  4.0, 40,  6.0,  6.2, 8.0, 6.5],  # Tinker Board 2
    [ 110,  790,  4.0, 40,  6.5,  7.5, 8.0, 7.0],  # Odroid N2+
    [  60,  180,  0.5, 92,  2.5,  7.8, 7.0, 7.0],  # BeagleBone Black
    [ 160,  520,  4.0, 40, 10.0,  8.5, 8.0, 5.0],  # Jetson Nano
    [ 200, 1180,  8.0, 40,  8.5,  6.0, 9.0, 6.0],  # Khadas VIM4
    [  35,  320,  2.0, 40,  3.5,  6.5, 6.5, 6.0],  # Pine64
    [ 190, 1620, 16.0, 40,  9.5,  6.8, 9.5, 6.5],  # Radxa Rock 5B
    [  35,  280,  2.0, 40,  3.0,  6.0, 6.0, 7.0],  # Le Potato
    [  25,   90,  0.1, 18,  1.0,  5.5, 6.5, 5.5],  # Onion Omega2
    [  28,   45,  0.03, 14, 0.5,  9.8, 5.5, 9.5],  # Arduino Uno R4
    [   6,   60,  0.05, 34, 0.4,  9.6, 7.0, 9.8],  # ESP32 Wroom
    [  32,  120,  0.06, 42, 0.6,  8.0, 7.5, 8.0],  # Teensy 4.1
    [  45,   70,  0.03, 20,  0.8, 6.5, 8.5, 6.0],  # Particle Boron
    [  10,   55,  0.04, 14,  0.3, 8.2, 6.0, 8.5],  # Seeed Xiao
    [ 120,  640,  4.0, 40,  7.0,  6.0, 8.0, 5.5],  # Up Board
    [   9,  150,  0.06, 26, 0.9,  5.8, 6.0, 7.0],  # Milk-V Duo
    [  12,  170,  0.5, 40,  1.5,  5.2, 6.0, 6.0],  # MangoPi MQ Dual
    [  18,   80,  0.06, 20, 0.9,  4.8, 6.5, 5.0],  # VoCore2
    [  55,  520,  4.0, 26,  5.0,  6.5, 8.5, 6.5],  # NanoPi R4S
    [  70,  600,  4.0, 40,  5.5,  6.0, 8.0, 6.0],  # FriendlyElec CM3
    [ 140,  380,  1.0, 40,  4.0,  5.5, 7.0, 4.5],  # ClockworkPi
    [  20,   40,  0.02, 25, 0.3,  9.4, 6.0, 9.2],  # Micro:bit V2
    [   8,   85,  0.03, 30, 0.4,  8.0, 6.5, 9.0],  # Waveshare RP2040
    [  45,   95,  0.04, 16,  1.0, 7.5, 8.0, 7.5],  # M5Stack Core2
    [  40,   70,  0.03, 29, 0.5,  6.5, 6.5, 6.0],  # Pyboard
    [  60,  720,  8.0, 40,  6.0,  9.8, 8.5, 8.5],  # Raspberry Pi 4
], dtype=float)
# CPU e RAM CAUSAM consumo; comunidade CAUSA disponibilidade percebida e I/O útil.
_SBC_DEMATEL = np.array([
    #      pre cpu ram gpio con com io  dis
    [0, 3, 3, 1, 1, 2, 2, 3],   # preço
    [3, 0, 2, 0, 4, 1, 1, 1],   # cpu -> CAUSA RAIZ de consumo
    [3, 1, 0, 0, 2, 0, 0, 1],   # ram
    [1, 0, 0, 0, 0, 1, 3, 0],   # gpio -> I/O
    [1, 0, 0, 0, 0, 0, 0, 1],   # consumo
    [1, 0, 0, 1, 0, 0, 3, 4],   # comunidade -> CAUSA de disponibilidade
    [2, 1, 1, 2, 1, 2, 0, 1],   # I/O
    [2, 0, 0, 0, 0, 1, 0, 0],   # disponibilidade -> EFEITO
], dtype=float)
SBC_IOT = {
    "id_caso": "sbc_iot",
    "nome": "Computadores de placa única (SBCs) e IoT",
    "dominio": "ti",
    "decisor": "Engenheiro de sistemas embarcados / maker / integrador de IoT",
    "descricao": (
        "33 placas, de microcontroladores de US$ 6 a SBCs de US$ 200. O critério que "
        "mais determina o sucesso do projeto não está na ficha técnica: é **comunidade "
        "e documentação**. Uma placa 30% mais rápida com metade da documentação custa "
        "semanas de desenvolvimento — e é isso que o DEMATEL revela aqui."),
    "criterios": _SBC_CRIT, "alternativas": _SBC_ALT, "matriz": _SBC_X,
    "dematel": _SBC_DEMATEL,
    "ahp": _saaty([0, 3, 4, 6, 5, 1, 2, 7]),   # preço > comunidade > I/O > cpu > ...
}

# ===========================================================================
# 8. HARDWARE DE MINERAÇÃO (ASICs) — 31 alternativas
# ===========================================================================
# ⚠️  Hashrate normalizado para índice 0-100 (algoritmos diferentes não são
#     diretamente comparáveis: TH/s de SHA-256 ≠ GH/s de Ethash ≠ MH/s de kHeavyHash).
_MIN_ALT = [
    ("antminer_s21", "Antminer S21"), ("antminer_t21", "Antminer T21"),
    ("antminer_l7", "Antminer L7"), ("antminer_k7", "Antminer K7"),
    ("antminer_e11", "Antminer E11"), ("wm_m60s", "Whatsminer M60S"),
    ("wm_m50", "Whatsminer M50"), ("wm_m30s", "Whatsminer M30S+"),
    ("avalon1346", "AvalonMiner 1346"), ("avalon1246", "AvalonMiner 1246"),
    ("gs_albox", "Goldshell AL Box"), ("gs_kabox", "Goldshell KA Box"),
    ("gs_ck6", "Goldshell CK6"), ("inno_a11", "Innosilicon A11"),
    ("inno_a10p", "Innosilicon A10 Pro"), ("iceriver_ks3", "IceRiver KS3"),
    ("iceriver_ks0", "IceRiver KS0"), ("jasminer_x16q", "Jasminer X16-Q"),
    ("jasminer_x4", "Jasminer X4"), ("antminer_d9", "Antminer D9"),
    ("antminer_z15", "Antminer Z15"), ("strongu_u1", "StrongU STU-U1"),
    ("wm_m53", "MicroBT Whatsminer M53"), ("avalon1446", "Canaan Avalon 1446"),
    ("ipollo_v1", "iPollo V1"), ("ipollo_g1", "iPollo G1"),
    ("baikal_giantn", "Baikal Giant N"), ("obelisk_sc1", "Obelisk SC1"),
    ("dayun_z1", "Dayun Zig Z1"), ("pinidea_rr200", "Pinidea RR-200"),
    ("antminer_s19", "Antminer S19 (base)"),
]
_MIN_CRIT = [
    ("preco",      "Preço",                  "cost",    "US$"),
    ("hashrate",   "Hashrate (índice)",      "benefit", "0-100"),
    ("consumo",    "Consumo",                "cost",    "W"),
    ("eficiencia", "Eficiência energética",  "cost",    "J/TH norm."),
    ("ruido",      "Ruído",                  "cost",    "dB"),
    ("disponib",   "Disponibilidade",        "benefit", "0-10"),
    ("roi",        "Perspectiva de ROI",     "benefit", "0-10"),
    ("suporte",    "Suporte e garantia",     "benefit", "0-10"),
]
_MIN_X = np.array([
    # preço  hash cons  efic ruido disp roi sup
    [ 4200, 95.0, 3500, 17.5, 75, 8.5, 8.0, 8.0],  # Antminer S21
    [ 2800, 78.0, 3610, 19.0, 75, 8.0, 7.2, 8.0],  # Antminer T21
    [ 6500, 62.0, 3425, 21.0, 76, 6.5, 7.5, 7.8],  # Antminer L7
    [ 1900, 45.0, 3080, 32.0, 75, 6.0, 6.0, 7.5],  # Antminer K7
    [ 3200, 55.0, 2550, 26.0, 72, 5.5, 5.8, 7.5],  # Antminer E11
    [ 4500, 92.0, 3441, 18.5, 75, 7.5, 7.8, 7.5],  # Whatsminer M60S
    [ 2200, 70.0, 3306, 24.0, 75, 8.0, 6.8, 7.2],  # Whatsminer M50
    [ 1400, 58.0, 3400, 31.0, 76, 8.5, 5.8, 7.0],  # Whatsminer M30S+
    [ 3100, 82.0, 3300, 21.0, 75, 7.0, 7.0, 7.0],  # AvalonMiner 1346
    [ 1500, 60.0, 3420, 30.0, 76, 7.5, 5.9, 6.8],  # AvalonMiner 1246
    [  900, 32.0,  790, 34.0, 55, 6.5, 5.5, 6.5],  # Goldshell AL Box
    [  850, 30.0,  700, 36.0, 55, 6.5, 5.4, 6.5],  # Goldshell KA Box
    [ 1200, 38.0, 3300, 42.0, 72, 6.0, 5.2, 6.5],  # Goldshell CK6
    [ 2400, 52.0, 2500, 29.0, 75, 5.5, 5.6, 6.0],  # Innosilicon A11
    [ 1100, 40.0, 1300, 33.0, 70, 5.0, 5.0, 5.8],  # Innosilicon A10 Pro
    [ 8500, 88.0, 3400, 20.0, 75, 6.0, 7.0, 6.5],  # IceRiver KS3
    [  600, 22.0,  100, 28.0, 45, 7.5, 5.5, 6.5],  # IceRiver KS0
    [ 4800, 66.0, 1900, 22.0, 65, 5.5, 6.5, 6.2],  # Jasminer X16-Q
    [ 1300, 35.0,  240, 25.0, 50, 6.0, 5.6, 6.0],  # Jasminer X4
    [ 1600, 48.0, 2839, 33.0, 75, 6.5, 5.8, 7.5],  # Antminer D9
    [ 2900, 42.0, 1510, 38.0, 72, 4.5, 5.0, 7.0],  # Antminer Z15
    [  700, 25.0, 2200, 48.0, 76, 3.5, 4.2, 4.5],  # StrongU STU-U1
    [ 3800, 85.0, 3276, 20.5, 75, 7.0, 7.4, 7.5],  # Whatsminer M53
    [ 3600, 86.0, 3200, 20.0, 75, 7.2, 7.5, 7.0],  # Canaan Avalon 1446
    [ 1800, 44.0, 3000, 36.0, 74, 5.0, 5.2, 5.5],  # iPollo V1
    [  950, 28.0, 1500, 40.0, 68, 5.0, 4.8, 5.5],  # iPollo G1
    [  800, 24.0, 1800, 46.0, 72, 3.8, 4.0, 4.2],  # Baikal Giant N
    [  650, 20.0, 1200, 50.0, 70, 3.0, 3.6, 3.8],  # Obelisk SC1
    [  600, 18.0, 1200, 52.0, 72, 3.2, 3.5, 4.0],  # Dayun Zig Z1
    [  550, 16.0, 1000, 55.0, 70, 3.0, 3.2, 3.5],  # Pinidea RR-200
    [ 1100, 54.0, 3250, 32.5, 75, 9.0, 5.5, 7.8],  # Antminer S19
], dtype=float)
# Consumo e eficiência são a CAUSA econômica: ditam o ROI. Ruído é efeito do consumo.
_MIN_DEMATEL = np.array([
    #      pre has con efi rui dis roi sup
    [0, 2, 1, 1, 0, 2, 4, 1],   # preço -> dita ROI
    [3, 0, 3, 2, 2, 1, 3, 0],   # hashrate
    [2, 1, 0, 3, 4, 0, 4, 0],   # consumo -> CAUSA de ruído e ROI
    [2, 1, 3, 0, 2, 0, 4, 0],   # eficiência -> CAUSA RAIZ do ROI
    [0, 0, 0, 0, 0, 0, 1, 0],   # ruído -> EFEITO
    [2, 0, 0, 0, 0, 0, 2, 2],   # disponibilidade
    [1, 0, 0, 0, 0, 1, 0, 0],   # ROI -> EFEITO final
    [1, 0, 0, 0, 0, 2, 2, 0],   # suporte
], dtype=float)
MINERACAO = {
    "id_caso": "mineracao_asic",
    "nome": "Hardware de mineração (ASICs)",
    "dominio": "infraestrutura",
    "decisor": "Operador de datacenter de mineração",
    "descricao": (
        "31 equipamentos. O erro clássico é comparar por hashrate — que só faz sentido "
        "dentro do mesmo algoritmo. O que decide a operação é **eficiência energética "
        "(J/TH)**, porque a energia é o custo recorrente que consome a margem. Ruído "
        "não é conforto: é o que define se a instalação pode existir onde você quer.\n\n"
        "⚠️ Hashrate normalizado em índice 0-100 — SHA-256, Scrypt, kHeavyHash e Ethash "
        "não são diretamente comparáveis."),
    "criterios": _MIN_CRIT, "alternativas": _MIN_ALT, "matriz": _MIN_X,
    "dematel": _MIN_DEMATEL,
    "ahp": _saaty([1, 3, 2, 0, 6, 5, 4, 7]),   # eficiência > preço > consumo > hashrate > ...
}

# ===========================================================================
# 9. MINI PCs — 10 alternativas
# ===========================================================================
_MPC_ALT = [
    ("rpi4", "Raspberry Pi 4"), ("rock64", "Rock64"), ("lattepanda", "LattePanda"),
    ("nuc_intel", "NUC Intel"), ("lenovo_i5", "Lenovo MiniPC i5 7ª ger."),
    ("mac_mini_m4", "Mac Mini M4"), ("khadas_vim4", "Khadas VIM 4"),
    ("beelink_ser5", "Beelink SER5 (Ryzen 5 5560U)"),
    ("gmktec_nucbox", "GMKtec NUCBOX (Ryzen 7 7840HS)"),
    ("geekom_a5", "Geekom A5 (Ryzen 5 6600H)"),
]
_MPC_CRIT = [
    ("preco",      "Preço",                "cost",    "R$"),
    ("cpu",        "Desempenho multicore", "benefit", "pts"),
    ("ram",        "Memória",              "benefit", "GB"),
    ("armazen",    "Armazenamento",        "benefit", "GB"),
    ("consumo",    "Consumo",              "cost",    "W"),
    ("tamanho",    "Volume",               "cost",    "L"),
    ("conectiv",   "Conectividade",        "benefit", "0-10"),
    ("expansao",   "Expansibilidade",      "benefit", "0-10"),
]
_MPC_X = np.array([
    # preço   cpu   ram  arm  cons tam conect expan
    [  600,   720,  8,   64,   6.0, 0.10, 7.0, 4.0],  # Raspberry Pi 4
    [  450,   480,  4,   32,   4.5, 0.09, 6.0, 3.5],  # Rock64
    [  900,   620,  4,   64,   8.0, 0.12, 7.5, 4.5],  # LattePanda
    [ 3200,  9800, 16,  512,  28.0, 0.65, 9.0, 8.0],  # NUC Intel
    [ 1400,  5200, 16,  256,  25.0, 1.00, 7.5, 7.0],  # Lenovo i5 7ª
    [ 5500, 16800, 16,  256,  22.0, 0.36, 9.2, 3.0],  # Mac Mini M4
    [ 1800, 11800,  8,  128,   9.0, 0.14, 8.5, 5.0],  # Khadas VIM 4
    [ 2100,  9600, 16,  500,  32.0, 0.60, 8.8, 8.5],  # Beelink SER5
    [ 3900, 17500, 32, 1024,  54.0, 0.72, 9.5, 8.8],  # GMKtec NUCBOX
    [ 2600, 12200, 16,  512,  45.0, 0.68, 9.0, 8.2],  # Geekom A5
], dtype=float)
# CPU é a CAUSA: dita consumo, que dita tamanho (dissipação).
_MPC_DEMATEL = np.array([
    #      pre cpu ram arm con tam con exp
    [0, 4, 3, 3, 1, 1, 3, 3],   # preço
    [4, 0, 2, 1, 4, 3, 1, 1],   # cpu -> CAUSA RAIZ
    [3, 1, 0, 0, 2, 1, 0, 1],   # ram
    [2, 0, 0, 0, 1, 1, 0, 1],   # armazenamento
    [1, 0, 0, 0, 0, 3, 0, 0],   # consumo -> tamanho (dissipação)
    [1, 0, 1, 1, 0, 0, 2, 3],   # tamanho -> limita expansão
    [2, 0, 0, 0, 1, 1, 0, 2],   # conectividade
    [2, 0, 1, 1, 0, 1, 1, 0],   # expansibilidade
], dtype=float)
MINIPCS = {
    "id_caso": "minipcs",
    "nome": "Mini PCs",
    "dominio": "ti",
    "decisor": "Comprador de estação compacta, homelab ou thin client",
    "descricao": (
        "10 máquinas que vão de um Raspberry Pi de R$ 600 a um GMKtec de R$ 3.900 — "
        "uma faixa de 6,5× em preço e 24× em desempenho. O trade-off central: a CPU "
        "que entrega desempenho é a mesma que exige dissipação, e dissipação é volume. "
        "Quem escolhe pelo menor tamanho está escolhendo o teto de desempenho."),
    "criterios": _MPC_CRIT, "alternativas": _MPC_ALT, "matriz": _MPC_X,
    "dematel": _MPC_DEMATEL,
    "ahp": _saaty([0, 1, 3, 5, 4, 6, 2, 7]),   # preço > cpu > conectividade > ram > ...
}

# ===========================================================================
CATALOGO_PRODUTOS = {c["id_caso"]: c for c in (
    CARROS_ELETRICOS, SMARTPHONES_2026, TABLETS, SMARTWATCHES, NOTEBOOKS,
    MAQUINARIO_AGRICOLA, SBC_IOT, MINERACAO, MINIPCS)}

if __name__ == "__main__":
    from casos.catalogo import validar
    print(f"{'ID':<22} {'DOMÍNIO':<16} {'ALT':>4} {'CRIT':>5}  NOME")
    print("-" * 100)
    n_alt = n_cel = 0
    for c in CATALOGO_PRODUTOS.values():
        validar(c)
        a, k = len(c["alternativas"]), len(c["criterios"])
        n_alt += a
        n_cel += a * k
        print(f"{c['id_caso']:<22} {c['dominio']:<16} {a:>4} {k:>5}  {c['nome']}")
    print(f"\n✅ {len(CATALOGO_PRODUTOS)} casos válidos · {n_alt} alternativas · "
          f"{n_cel} células de decisão")
