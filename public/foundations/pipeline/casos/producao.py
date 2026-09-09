"""
Estudos de caso de EQUIPAMENTOS DE PRODUÇÃO — impressão 3D e grande formato.

⚠️  NATUREZA DOS DADOS
---------------------
ILUSTRATIVOS. Ordens de grandeza plausíveis para o mercado brasileiro em 2025-2026,
arredondadas, para DEMONSTRAR O MÉTODO. Preços de equipamento variam por câmbio,
importador, configuração e lote; nenhum valor aqui foi cotado.

As fontes de comparação citadas na solicitação (YouTube, Eletro Review, Mundo Plotter,
Multivisi, Promobit) NÃO foram consultadas — não tenho acesso a elas. Os números abaixo
são modelagem, não levantamento. Para decidir de fato, substitua pela sua cotação.

O que NÃO é ilustrativo: a modelagem. Critérios, direções, matriz causal e matriz de
Saaty representam a estrutura real de cada decisão.

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import numpy as np

from casos.catalogo import _saaty

# ===========================================================================
# IMPRESSORAS 3D — 30 modelos (resina MSLA + FDM)
# ===========================================================================
# A matriz é ÚNICA; o que muda entre os dois casos é a MATRIZ CAUSAL do DEMATEL,
# porque a estrutura de influência depende do contexto operacional:
#   • vendendo miniaturas, o DETALHE é a causa raiz (dita preço percebido e valor);
#   • produzindo peças em volume, a VELOCIDADE e a CONFIABILIDADE é que ditam
#     o custo por peça e a viabilidade da operação.
# Mesmas alternativas, mesmos números, contextos diferentes — e é exatamente por
# isso que o mesmo conjunto pode ter dois vencedores legítimos.
_3D_ALT = [
    # --- Resina MSLA ---
    ("saturn4_ultra", "Elegoo Saturn 4 Ultra"), ("saturn4_16k", "Elegoo Saturn 4 Ultra 16K"),
    ("mars5_ultra", "Elegoo Mars 5 Ultra"), ("mars5", "Elegoo Mars 5"),
    ("photon_m7max", "Anycubic Photon Mono M7 Max"), ("photon_m7pro", "Anycubic Photon Mono M7 Pro"),
    ("photon_m4ultra", "Anycubic Photon Mono 4 Ultra"), ("halot_r6", "Creality Halot-R6"),
    ("halot_mage_pro", "Creality Halot Mage Pro"), ("sonic_mighty14k", "Phrozen Sonic Mighty 14K"),
    ("sonic_mini8ks", "Phrozen Sonic Mini 8K S"), ("gktwo", "Uniformation GKtwo"),
    ("jupiter2", "Elegoo Jupiter 2"), ("photon_m5s_pro", "Anycubic Photon M5s Pro"),
    # --- FDM ---
    ("bambu_p1s", "Bambu Lab P1S"), ("bambu_a1combo", "Bambu Lab A1 Combo"),
    ("bambu_x1c", "Bambu Lab X1-Carbon"), ("bambu_a1mini", "Bambu Lab A1 mini"),
    ("k1_max", "Creality K1 Max"), ("k2_plus_combo", "Creality K2 Plus Combo"),
    ("k1c", "Creality K1C"), ("ender3_v3", "Creality Ender-3 V3"),
    ("ender3_v3se", "Creality Ender-3 V3 SE"), ("prusa_mk4s", "Prusa MK4S"),
    ("prusa_core1", "Prusa Core One"), ("kobra3_combo", "Anycubic Kobra 3 Combo"),
    ("neptune4plus", "Elegoo Neptune 4 Plus"), ("centauri_carbon", "Elegoo Centauri Carbon"),
    ("sovol_sv08", "Sovol SV08"), ("qidi_q1pro", "QIDI Q1 Pro"),
]
_3D_CRIT = [
    ("preco",        "Preço",                    "cost",    "R$"),
    ("detalhe",      "Detalhe e acabamento",     "benefit", "0-10"),
    ("volume",       "Volume de construção",     "benefit", "L"),
    ("velocidade",   "Velocidade de produção",   "benefit", "0-10"),
    ("pos_proc",     "Esforço de pós-processo",  "cost",    "0-10"),
    ("custo_mat",    "Custo de material",        "cost",    "R$/kg-L"),
    ("automacao",    "Automação",                "benefit", "0-10"),
    ("confiab",      "Confiabilidade",           "benefit", "0-10"),
    ("suporte_br",   "Insumos e suporte no BR",  "benefit", "0-10"),
]
_3D_X = np.array([
    # preço  det  vol  vel  pos  mat  aut  conf sup
    [ 4200, 9.6,  6.6, 8.5, 8.5, 260, 7.5, 8.5, 8.0],  # Saturn 4 Ultra
    [ 5400, 9.8,  6.6, 8.3, 8.5, 260, 7.5, 8.4, 7.5],  # Saturn 4 Ultra 16K
    [ 2600, 9.4,  2.3, 8.0, 8.5, 260, 7.0, 8.3, 8.0],  # Mars 5 Ultra
    [ 1900, 9.0,  2.3, 7.0, 8.5, 260, 5.5, 8.0, 8.0],  # Mars 5
    [ 8500, 9.5, 14.5, 8.2, 9.0, 250, 7.8, 8.0, 7.0],  # Photon Mono M7 Max
    [ 5200, 9.6,  6.2, 8.4, 8.8, 250, 7.6, 8.1, 7.0],  # Photon Mono M7 Pro
    [ 2900, 9.2,  2.6, 8.0, 8.8, 250, 6.5, 7.9, 7.0],  # Photon Mono 4 Ultra
    [ 2400, 8.6,  2.0, 6.5, 8.5, 270, 5.0, 7.2, 8.5],  # Halot-R6
    [ 3600, 9.1,  4.5, 7.6, 8.5, 270, 6.4, 7.6, 8.5],  # Halot Mage Pro
    [ 6800, 9.7,  7.8, 8.0, 8.8, 280, 7.0, 8.2, 5.5],  # Sonic Mighty 14K
    [ 3100, 9.5,  1.6, 7.4, 8.8, 280, 6.0, 8.0, 5.5],  # Sonic Mini 8K S
    [ 7200, 9.3, 10.5, 7.2, 9.2, 300, 7.4, 7.8, 4.5],  # Uniformation GKtwo
    [ 9800, 9.4, 19.0, 7.0, 9.4, 260, 7.2, 7.6, 7.0],  # Jupiter 2
    [ 4600, 9.5,  4.8, 8.6, 8.8, 250, 7.2, 8.0, 7.0],  # Photon M5s Pro
    [ 9500, 7.4, 15.6, 9.2, 2.0, 120, 9.0, 9.5, 8.0],  # Bambu Lab P1S
    [ 7200, 7.2, 16.4, 8.6, 2.2, 120, 9.4, 9.0, 8.0],  # Bambu Lab A1 Combo
    [14500, 7.8, 15.6, 9.4, 2.0, 120, 9.8, 9.6, 8.0],  # Bambu Lab X1-Carbon
    [ 3900, 6.8,  3.4, 8.0, 2.2, 120, 9.0, 8.8, 8.0],  # Bambu Lab A1 mini
    [ 8800, 7.0, 32.8, 9.0, 2.0, 110, 8.2, 8.4, 9.0],  # Creality K1 Max
    [11500, 7.4, 46.7, 9.1, 2.2, 110, 9.0, 8.6, 9.0],  # Creality K2 Plus Combo
    [ 6200, 7.0, 10.9, 8.8, 2.0, 110, 8.0, 8.5, 9.0],  # Creality K1C
    [ 2200, 6.6,  8.6, 7.6, 2.0, 100, 6.5, 7.8, 9.5],  # Ender-3 V3
    [ 1400, 6.2,  8.6, 6.8, 2.0, 100, 5.5, 7.4, 9.5],  # Ender-3 V3 SE
    [11000, 8.0, 12.6, 8.2, 2.0, 130, 8.6, 9.7, 5.0],  # Prusa MK4S
    [13500, 8.2, 13.4, 8.8, 2.0, 130, 9.0, 9.8, 5.0],  # Prusa Core One
    [ 4400, 6.8, 11.0, 8.2, 2.2, 105, 8.8, 8.0, 8.0],  # Kobra 3 Combo
    [ 3200, 6.6, 20.6, 7.8, 2.0, 105, 7.0, 7.8, 8.0],  # Neptune 4 Plus
    [ 4800, 7.2, 10.9, 8.9, 2.0, 105, 8.4, 8.4, 8.0],  # Centauri Carbon
    [ 5600, 7.0, 22.6, 9.0, 2.2, 105, 7.6, 8.0, 6.5],  # Sovol SV08
    [ 6600, 7.4, 12.6, 8.8, 2.0, 115, 8.5, 8.8, 6.0],  # QIDI Q1 Pro
], dtype=float)

# --- Contexto A: VENDA DE MINIATURAS -----------------------------------------
# Aqui o detalhe é a causa raiz: ele define o preço de venda da peça, justifica
# o pós-processamento e puxa o custo de material. Volume e velocidade são efeitos.
_3D_DEMATEL_MINI = np.array([
    #      pre det vol vel pos mat aut con sup
    [0, 2, 2, 2, 0, 1, 3, 2, 1],   # preço
    [4, 0, 1, 2, 4, 3, 1, 1, 0],   # detalhe -> CAUSA RAIZ
    [3, 0, 0, 2, 1, 3, 1, 1, 0],   # volume
    [2, 1, 1, 0, 0, 1, 1, 2, 0],   # velocidade
    [1, 0, 0, 2, 0, 2, 1, 0, 1],   # pós-processo
    [1, 0, 0, 0, 0, 0, 0, 0, 2],   # custo de material
    [3, 1, 0, 3, 3, 1, 0, 3, 0],   # automação
    [2, 1, 0, 2, 0, 1, 0, 0, 1],   # confiabilidade
    [2, 0, 0, 1, 1, 3, 0, 2, 0],   # suporte BR -> insumo disponível
], dtype=float)
IMPRESSORAS_3D_MINIATURAS = {
    "id_caso": "impressoras_3d_miniaturas",
    "nome": "Impressoras 3D — venda de miniaturas e peças decorativas",
    "dominio": "manufatura",
    "decisor": "Quem vende miniaturas, bustos e presépios com acabamento premium",
    "descricao": (
        "30 impressoras, resina MSLA e FDM na mesma matriz. A tese corrente é que "
        "resina vence para detalhe — e é isso que o método vai testar, não assumir. "
        "O trade-off central: resina entrega acabamento que justifica preço de venda, "
        "e cobra por isso em pós-processamento (limpeza, cura, resíduo) e custo de "
        "material 2 a 2,6× o do filamento."),
    "criterios": _3D_CRIT, "alternativas": _3D_ALT, "matriz": _3D_X,
    "dematel": _3D_DEMATEL_MINI,
    "ahp": _saaty([2, 0, 6, 5, 4, 3, 7, 8, 1]),   # detalhe > suporte > preço > material > ...
}

# --- Contexto B: PRODUÇÃO EM VOLUME ------------------------------------------
# Aqui a causa raiz muda: velocidade e confiabilidade ditam o custo por peça e a
# viabilidade da operação. Detalhe vira um requisito mínimo, não a alavanca.
_3D_DEMATEL_PROD = np.array([
    #      pre det vol vel pos mat aut con sup
    [0, 2, 3, 2, 0, 1, 3, 2, 1],   # preço
    [2, 0, 0, 1, 3, 2, 0, 0, 0],   # detalhe -> agora é EFEITO/requisito
    [3, 0, 0, 3, 1, 3, 1, 2, 0],   # volume -> dita ciclo e material
    [3, 1, 2, 0, 1, 2, 2, 3, 0],   # velocidade -> CAUSA RAIZ do custo por peça
    [1, 0, 0, 3, 0, 1, 1, 1, 1],   # pós-processo -> trava a linha
    [2, 0, 1, 1, 0, 0, 0, 1, 2],   # custo de material
    [3, 0, 1, 4, 3, 1, 0, 4, 0],   # automação -> CAUSA de velocidade e confiabilidade
    [3, 0, 1, 3, 1, 2, 0, 0, 2],   # confiabilidade -> CAUSA de produtividade real
    [2, 0, 0, 2, 1, 3, 0, 3, 0],   # suporte BR -> peça e insumo = máquina parada ou não
], dtype=float)
IMPRESSORAS_3D_PRODUCAO = {
    "id_caso": "impressoras_3d_producao",
    "nome": "Impressoras 3D — produção de peças funcionais em volume",
    "dominio": "manufatura",
    "decisor": "Quem fabrica peças grandes, resistentes e em série",
    "descricao": (
        "As MESMAS 30 impressoras, mesma matriz de decisão — e uma matriz causal "
        "diferente, porque o contexto operacional mudou. Em produção, velocidade, "
        "automação e confiabilidade deixam de ser conveniência e passam a ditar o "
        "custo por peça; o detalhe vira requisito mínimo, não alavanca. Se o vencedor "
        "mudar em relação ao caso de miniaturas, a mudança É o resultado."),
    "criterios": _3D_CRIT, "alternativas": _3D_ALT, "matriz": _3D_X,
    "dematel": _3D_DEMATEL_PROD,
    "ahp": _saaty([2, 7, 3, 0, 5, 4, 6, 1, 8]),   # velocidade > confiabilidade > preço > volume > ...
}

# ===========================================================================
# PLOTTERS DE GRANDE FORMATO — 24 configurações
# ===========================================================================
_PL_ALT = [
    ("xuli_x6_3204", "Xuli X6-3204 (i3200)"), ("xuli_x6_2000", "Xuli X6-2000 (DX5)"),
    ("xuli_uv_roll", "Xuli UV Roll (i3200)"),
    ("mimaki_jv330", "Mimaki JV330-160"), ("mimaki_cjv200", "Mimaki CJV200-160"),
    ("mimaki_ujv100", "Mimaki UJV100-160 (UV)"), ("mimaki_jv100", "Mimaki JV100-160"),
    ("roland_vg3", "Roland TrueVIS VG3-640"), ("roland_sg3", "Roland TrueVIS SG3-540"),
    ("roland_lec2", "Roland VersaUV LEC2-330"),
    ("impri_i3200_4", "Imprimiprinter i3200 4 cabeças"),
    ("impri_dx5_2", "Imprimiprinter DX5 2 cabeças"),
    ("hgr_uv_hibrida", "HGR UV Híbrida (i3200)"), ("hgr_uv_flatbed", "HGR UV Flatbed"),
    ("visutec_vt1800", "Visutec VT-1800 (DX5)"), ("visutec_vt3200", "Visutec VT-3200 (i3200)"),
    ("epson_s60600", "Epson SureColor S60600"), ("epson_s80600", "Epson SureColor S80600"),
    ("hp_latex335", "HP Latex 335"), ("hp_latex700", "HP Latex 700"),
    ("mutoh_vj1638", "Mutoh ValueJet 1638"), ("allwin_i3200", "Allwin i3200"),
    ("konica_512i", "Konica 512i"), ("witcolor_u9000", "Wit-Color Ultra 9000"),
]
_PL_CRIT = [
    ("preco",       "Preço",                     "cost",    "R$ mil"),
    ("largura",     "Largura de impressão",      "benefit", "m"),
    ("velocidade",  "Produtividade",             "benefit", "m²/h"),
    ("qualidade",   "Qualidade de imagem",       "benefit", "0-10"),
    ("suporte_br",  "Assistência técnica no BR", "benefit", "0-10"),
    ("custo_peca",  "Custo de peças e cabeças",  "cost",    "0-10"),
    ("vida_cabeca", "Durabilidade da cabeça",    "benefit", "0-10"),
    ("versatil",    "Versatilidade de substrato", "benefit", "0-10"),
    ("consumo",     "Consumo de tinta",          "cost",    "0-10"),
]
_PL_X = np.array([
    # preço larg  vel  qual sup  peça vida vers cons
    [  95,  3.20,  85, 7.8, 8.5, 4.0, 7.5, 7.0, 5.5],  # Xuli X6-3204 (i3200)
    [  62,  2.00,  35, 7.2, 8.5, 5.0, 6.5, 6.5, 6.0],  # Xuli X6-2000 (DX5)
    [ 180,  3.20,  55, 8.4, 8.0, 5.5, 7.8, 9.2, 5.0],  # Xuli UV Roll (i3200)
    [ 320,  1.61,  30, 9.4, 9.0, 7.5, 8.8, 8.0, 4.0],  # Mimaki JV330-160
    [ 410,  1.61,  26, 9.5, 9.0, 8.0, 8.8, 8.6, 4.2],  # Mimaki CJV200-160
    [ 520,  1.61,  22, 9.6, 8.8, 8.5, 9.0, 9.4, 3.8],  # Mimaki UJV100-160
    [ 210,  1.61,  24, 9.0, 9.0, 7.0, 8.5, 7.6, 4.5],  # Mimaki JV100-160
    [ 480,  1.62,  32, 9.6, 9.2, 8.5, 9.2, 8.4, 4.0],  # Roland TrueVIS VG3-640
    [ 290,  1.37,  25, 9.3, 9.2, 7.8, 9.0, 8.0, 4.2],  # Roland TrueVIS SG3-540
    [ 390,  0.76,  14, 9.7, 9.0, 8.2, 9.0, 9.6, 3.5],  # Roland VersaUV LEC2-330
    [ 130,  3.20, 110, 7.6, 7.5, 4.5, 7.0, 7.0, 5.8],  # Imprimiprinter i3200 ×4
    [  70,  3.20,  40, 7.0, 7.5, 5.2, 6.2, 6.5, 6.2],  # Imprimiprinter DX5 ×2
    [ 240,  2.50,  48, 8.6, 7.8, 6.0, 7.6, 9.5, 4.8],  # HGR UV Híbrida
    [ 330,  2.50,  38, 8.8, 7.6, 6.5, 7.8, 9.6, 4.6],  # HGR UV Flatbed
    [  58,  1.80,  32, 7.0, 8.2, 5.0, 6.4, 6.4, 6.0],  # Visutec VT-1800 (DX5)
    [  88,  3.20,  80, 7.7, 8.2, 4.2, 7.4, 7.0, 5.6],  # Visutec VT-3200 (i3200)
    [ 270,  1.62,  35, 9.2, 8.6, 7.2, 8.6, 7.8, 4.4],  # Epson S60600
    [ 350,  1.62,  30, 9.5, 8.6, 7.6, 8.8, 8.2, 4.2],  # Epson S80600
    [ 230,  1.63,  23, 8.8, 8.4, 6.8, 8.0, 8.8, 5.2],  # HP Latex 335
    [ 420,  1.63,  36, 9.3, 8.4, 7.4, 8.6, 9.0, 5.0],  # HP Latex 700
    [ 190,  1.62,  28, 8.6, 7.8, 6.4, 8.2, 7.4, 4.8],  # Mutoh ValueJet 1638
    [  78,  3.20,  75, 7.4, 6.5, 4.0, 7.0, 6.8, 5.8],  # Allwin i3200
    [ 110,  3.20,  95, 7.0, 6.8, 5.5, 7.8, 6.6, 6.5],  # Konica 512i
    [  92,  3.20,  70, 7.2, 6.2, 4.4, 6.8, 6.6, 6.0],  # Wit-Color Ultra 9000
], dtype=float)
# Cabeça (durabilidade) e suporte são as CAUSAS econômicas: ditam custo de peça e
# tempo de máquina parada. Qualidade e velocidade competem pelo mesmo passe.
_PL_DEMATEL = np.array([
    #      pre lar vel qua sup peç vid ver con
    [0, 3, 3, 3, 2, 2, 3, 3, 1],   # preço
    [3, 0, 3, 0, 1, 2, 1, 1, 2],   # largura
    [2, 1, 0, 3, 0, 2, 2, 0, 2],   # velocidade -> troca com qualidade
    [3, 0, 3, 0, 1, 2, 1, 1, 3],   # qualidade -> mais passes, mais tinta
    [2, 0, 1, 1, 0, 4, 2, 1, 0],   # suporte BR -> CAUSA de custo de peça
    [2, 0, 1, 0, 1, 0, 2, 0, 0],   # custo de peça
    [3, 0, 2, 2, 1, 4, 0, 1, 1],   # durabilidade da cabeça -> CAUSA RAIZ
    [3, 1, 1, 1, 1, 2, 1, 0, 2],   # versatilidade
    [1, 0, 0, 0, 0, 0, 0, 0, 0],   # consumo -> EFEITO
], dtype=float)
PLOTTERS = {
    "id_caso": "plotters_formato",
    "nome": "Plotters de impressão em grande formato",
    "dominio": "manufatura",
    "decisor": "Dono de gráfica / comunicação visual (custo-benefício e suporte no BR)",
    "descricao": (
        "24 configurações de plotter, com cabeças i3200, DX5, DX6 e equivalentes. "
        "O erro clássico é comparar por preço de máquina: quem decide a operação é a "
        "**durabilidade da cabeça** cruzada com **assistência técnica no Brasil** — "
        "juntas elas determinam custo de peça e, sobretudo, quantos dias a máquina "
        "fica parada. Uma cabeça i3200 barata sem assistência local custa mais que "
        "uma DX6 cara com técnico na cidade.\n\n"
        "⚠️ As fontes citadas na solicitação (Eletro Review, Mundo Plotter, Multivisi, "
        "Promobit, YouTube) NÃO foram consultadas — estes dados são modelagem, não "
        "levantamento de mercado."),
    "criterios": _PL_CRIT, "alternativas": _PL_ALT, "matriz": _PL_X,
    "dematel": _PL_DEMATEL,
    "ahp": _saaty([2, 6, 4, 3, 0, 5, 1, 7, 8]),   # suporte > durabilidade > preço > qualidade > ...
}

CATALOGO_PRODUCAO = {c["id_caso"]: c for c in (
    IMPRESSORAS_3D_MINIATURAS, IMPRESSORAS_3D_PRODUCAO, PLOTTERS)}

if __name__ == "__main__":
    from casos.catalogo import validar
    for c in CATALOGO_PRODUCAO.values():
        validar(c)
        print(f"✅ {c['id_caso']:<28} {len(c['alternativas']):>3} alternativas × "
              f"{len(c['criterios'])} critérios")


# ===========================================================================
# IMPRESSORAS 3D — MINIATURAS, COM TRIAGEM DE ADMISSIBILIDADE
# ===========================================================================
# POR QUE ESTE CASO EXISTE
# ------------------------
# Rodar as 30 impressoras juntas no caso `impressoras_3d_miniaturas` produziu um
# resultado que merece ser lido com atenção: ELECTRE I e ELECTRE II elegem a
# Elegoo Saturn 4 Ultra em 1º, enquanto os SEIS métodos compensatórios a colocam
# entre 12º e 16º. Não é ruído — é a divergência de escola fazendo seu trabalho.
#
# O motivo está no perfil orientado (0 = pior, 1 = melhor do conjunto):
#     detalhe .......... Saturn 0,94   ×   Bambu A1 0,28
#     pós-processo ..... Saturn 0,12   ×   Bambu A1 0,97
#     custo material ... Saturn 0,20   ×   Bambu A1 0,90
#
# Métodos compensatórios (MAUT, PROMETHEE, TOPSIS, MCDA-C, TODIM, SAPEVO-M)
# "compram" o déficit de detalhe da FDM com pós-processo fácil e filamento barato.
# O ELECTRE, que admite VETO, recusa a troca: nenhum consumível barato transforma
# uma peça de detalhe 0,28 numa miniatura vendável.
#
# O ELECTRE está certo, e o defeito era da MODELAGEM: para quem vende miniatura,
# detalhe não é critério compensável — é REQUISITO DE ADMISSIBILIDADE. Misturar as
# duas coisas na mesma matriz é o erro que Lima Jr. (2018) separa em duas
# problemáticas distintas: triagem (P.α) ANTES de ordenação (P.γ).
#
# Este caso aplica a triagem: só entram máquinas com detalhe ≥ 9,0 — o piso para
# uma peça decorativa com valor de venda premium. Depois disso, sim, os critérios
# restantes são legitimamente compensáveis entre si.
_LIMIAR_DETALHE_MINIATURA = 9.0
_idx_det = [k for k, _, _, _ in _3D_CRIT].index("detalhe")
_aptas = [i for i in range(len(_3D_ALT)) if _3D_X[i, _idx_det] >= _LIMIAR_DETALHE_MINIATURA]

IMPRESSORAS_3D_MINIATURAS_TRIADAS = {
    "id_caso": "impressoras_3d_miniaturas_triadas",
    "nome": "Impressoras 3D — miniaturas, após triagem de admissibilidade",
    "dominio": "manufatura",
    "decisor": "Quem vende miniaturas com acabamento premium (detalhe ≥ 9,0 é eliminatório)",
    "descricao": (
        f"As mesmas 30 impressoras, agora com **triagem antes da ordenação**: só "
        f"disputam as {len(_aptas)} que atingem detalhe ≥ {_LIMIAR_DETALHE_MINIATURA:.0f}, "
        "o piso para uma peça decorativa vendável como premium.\n\n"
        "Sem essa triagem, os métodos compensatórios trocavam o detalhe — que é a "
        "razão de existir do produto — por filamento barato e pós-processo fácil, e "
        "elegiam uma FDM para fazer miniatura. Com ela, a disputa passa a ser entre "
        "máquinas que efetivamente entregam a peça, e os critérios restantes (preço, "
        "volume, velocidade, custo de material, suporte) voltam a ser legitimamente "
        "compensáveis entre si.\n\n"
        "É a problemática de ESCOLHA (P.α) precedendo a de ORDENAÇÃO (P.γ), "
        "conforme Lima Jr. (2018)."),
    "criterios": _3D_CRIT,
    "alternativas": [_3D_ALT[i] for i in _aptas],
    "matriz": _3D_X[_aptas, :],
    "dematel": _3D_DEMATEL_MINI,
    "ahp": _saaty([2, 0, 6, 5, 4, 3, 7, 8, 1]),
}
CATALOGO_PRODUCAO["impressoras_3d_miniaturas_triadas"] = IMPRESSORAS_3D_MINIATURAS_TRIADAS
