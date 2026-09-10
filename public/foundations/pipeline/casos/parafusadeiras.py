"""
Estudos de caso da categoria PARAFUSADEIRA ELÉTRICA.

═══════════════════════════════════════════════════════════════════════════════
 PROCEDÊNCIA — os dois casos derivam da análise de vídeos feita com a skill
 `watch` (transcrição por Whisper + leitura de quadros). A autoria dos vídeos é
 dos canais citados; deste projeto é a modelagem multicritério.

   [V1] "As 5 Melhores Parafusadeira De 2025! // Tem Boa e Barata, 20V,
        De Impacto e Outras." — canal Comprou Avaliou, 14/05/2024, 6min33s.
        https://youtu.be/pgdqVYEjZtk
        Especificações extraídas da narração (torque, RPM, tensão, posições de
        torque, autonomia, faixa de preço declarada no vídeo).

   [V2] "As Melhores Parafusadeiras Do Mundo" — canal Ferramentas Em Ação -
        Assis Pires, 04/01/2024, 15s. https://youtube.com/shorts/9SIs3agoZKc
        Comparativo visual de plataformas profissionais; os modelos e as
        baterias foram lidos dos quadros (o áudio é trilha musical).
═══════════════════════════════════════════════════════════════════════════════

POR QUE DOIS CASOS E NÃO UM. Os vídeos tratam de mercados diferentes, e juntá-los
produziria um ranking sem sentido: no doméstico o preço domina e a plataforma de
bateria é irrelevante; no profissional o preço da ferramenta é ruído diante do
custo de trocar de ecossistema. É a lição das impressoras 3D deste projeto —
mesma categoria, finalidades distintas, critérios distintos.

Os modelos citados nos vídeos estão marcados com [V1] / [V2] nos comentários.
Os demais são comparáveis do mesmo segmento, acrescentados para dar discriminação
ao método — cinco alternativas não exercitam discordância entre os nove métodos.

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import numpy as np

from casos.catalogo import _saaty

# ===========================================================================
# 1. PARAFUSADEIRAS DOMÉSTICAS E SEMIPROFISSIONAIS  [V1]
# ===========================================================================
PARAFUSADEIRAS_DOMESTICAS = {
    "id_caso": "parafusadeiras_domesticas",
    "nome": "Parafusadeira doméstica e semiprofissional",
    "dominio": "consumo",
    "decisor": "Comprador doméstico / marceneiro autônomo",
    "descricao": (
        "Catorze parafusadeiras, entre elas as cinco do guia de compra analisado. O vídeo "
        "ordena por 'custo-benefício' e coroa a Bosch GSR 12V — e o método mostra por quê, "
        "contra a intuição: a DeWalt de impacto tem **quatro vezes mais torque** (65 Nm "
        "contra 15) e custa quase três vezes mais, mas o trabalho doméstico raramente "
        "exige 65 Nm. O critério que decide não é torque nem preço isolados: é **autonomia "
        "por carga** — 600 parafusamentos significam não interromper a montagem no meio."),
    "criterios": [
        ("preco",      "Preço médio de mercado",       "cost",    "R$"),
        ("torque",     "Torque máximo",                "benefit", "Nm"),
        ("tensao",     "Tensão da bateria",            "benefit", "V"),
        ("rpm",        "Rotação máxima",               "benefit", "rpm"),
        ("posicoes",   "Posições de torque",           "benefit", "níveis"),
        ("autonomia",  "Autonomia por carga",          "benefit", "parafusos"),
        ("funcoes",    "Funções (parafusar/furar/impacto)", "benefit", "1-3"),
        ("peso",       "Peso da ferramenta",           "cost",    "kg"),
    ],
    "alternativas": [
        ("D01", "Bosch GSR 12V-15"),            # [V1] 1º lugar
        ("D02", "DeWalt DCD777 20V brushless"),  # [V1] 2º lugar
        ("D03", "Black+Decker BCD70 20V"),       # [V1] 3º lugar
        ("D04", "Wunder PFV 12V"),               # [V1] 4º lugar
        ("D05", "WAP BPF 12V"),                  # [V1] 5º lugar
        ("D06", "Makita DF333D 12V"),
        ("D07", "Bosch GSB 18V-50 com impacto"),
        ("D08", "Vonder PAV 1210"),
        ("D09", "Tramontina PRO 12V"),
        ("D10", "Einhell TE-CD 18V"),
        ("D11", "Stanley SCD20 20V"),
        ("D12", "Black+Decker LD12 12V"),
        ("D13", "Mondial FPM-01 (com fio)"),
        ("D14", "DeWalt DCD701 12V XR brushless"),
    ],
    "matriz": np.array([
        # preço torque tensão  rpm  posições autonomia funções peso
        [  480,  15.0, 12,  1300, 20,  600, 2, 0.95],  # [V1] Bosch GSR 12V-15
        [ 1341,  65.0, 20,  1750, 15,  420, 3, 1.60],  # [V1] DeWalt DCD777
        [  710,  45.0, 20,  1400, 11,  380, 2, 1.35],  # [V1] Black+Decker BCD70
        [  444,  25.0, 12,  1100, 18,  260, 3, 1.10],  # [V1] Wunder PFV
        [  216,  12.0, 12,   740, 19,  180, 2, 0.90],  # [V1] WAP BPF
        [  620,  30.0, 12,  1700, 21,  520, 2, 0.98],  # Makita DF333D
        [ 1180,  55.0, 18,  1900, 20,  480, 3, 1.70],  # Bosch GSB 18V-50
        [  260,  14.0, 12,   800, 18,  200, 2, 1.05],  # Vonder PAV 1210
        [  330,  18.0, 12,   900, 18,  240, 2, 1.00],  # Tramontina PRO
        [  390,  22.0, 18,  1250, 21,  300, 3, 1.45],  # Einhell TE-CD
        [  560,  35.0, 20,  1500, 11,  340, 2, 1.30],  # Stanley SCD20
        [  240,  10.0, 12,   650, 11,  150, 1, 0.85],  # B+D LD12
        [  180,  20.0,  0,  2500,  1,  999, 2, 1.25],  # Mondial com fio
        [  980,  40.0, 12,  1650, 15,  650, 2, 1.05],  # DeWalt DCD701 XR
    ], dtype=float),
    # Tensão é a CAUSA estrutural: dita torque, rotação e, por eles, o preço.
    # Autonomia é o critério que a ficha técnica esconde e o uso revela.
    "dematel": np.array([
        #  preço torq tens rpm  pos auton func peso
        [0, 1, 1, 1, 1, 1, 1, 0],   # preço -> EFEITO
        [3, 0, 1, 2, 2, 2, 2, 3],   # torque
        [3, 4, 0, 3, 1, 3, 3, 4],   # tensão -> CAUSA RAIZ
        [2, 2, 1, 0, 1, 2, 1, 1],   # rotação
        [2, 2, 0, 1, 0, 1, 1, 0],   # posições de torque
        [2, 1, 2, 1, 0, 0, 1, 2],   # autonomia
        [3, 2, 2, 1, 1, 1, 0, 2],   # funções
        [2, 1, 1, 1, 0, 1, 1, 0],   # peso
    ], dtype=float),
    # Uso doméstico: preço manda, autonomia em seguida, torque depois.
    "ahp": _saaty([0, 3, 5, 4, 6, 1, 2, 7]),
}

# ===========================================================================
# 2. PARAFUSADEIRAS PROFISSIONAIS — plataformas de bateria  [V2]
# ===========================================================================
PARAFUSADEIRAS_PROFISSIONAIS = {
    "id_caso": "parafusadeiras_profissionais",
    "nome": "Parafusadeira profissional — plataforma de bateria",
    "dominio": "manufatura",
    "decisor": "Construtora / marcenaria com equipe (compra de plataforma)",
    "descricao": (
        "Doze ferramentas de topo de linha, entre elas as cinco do comparativo analisado "
        "(DeWalt POWERSTACK e FLEXVOLT XR, Bosch ProCORE 18V, FLEX 24V). Aqui a decisão "
        "muda de natureza: ninguém compra uma parafusadeira profissional isolada — compra "
        "**um ecossistema de bateria**, e a partir daí toda ferramenta seguinte fica presa "
        "à plataforma. O preço da ferramenta é ruído diante do custo de trocar de sistema. "
        "Por isso amplitude do ecossistema e disponibilidade de assistência entram como "
        "critérios, e por isso o vencedor aqui não é o mesmo do uso doméstico."),
    "criterios": [
        ("preco_kit",   "Preço do kit (2 baterias)",   "cost",    "R$"),
        ("torque",      "Torque máximo",               "benefit", "Nm"),
        ("tensao",      "Tensão da plataforma",        "benefit", "V"),
        ("capacidade",  "Capacidade da bateria",       "benefit", "Ah"),
        ("ecossistema", "Ferramentas na plataforma",   "benefit", "un"),
        ("assistencia", "Rede de assistência no Brasil", "benefit", "0-10"),
        ("durabilidade", "Durabilidade em obra",       "benefit", "0-10"),
        ("peso",        "Peso com bateria",            "cost",    "kg"),
    ],
    "alternativas": [
        ("R01", "DeWalt DCD999 FLEXVOLT XR 60V"),   # [V2]
        ("R02", "DeWalt DCD800 POWERSTACK 20V"),    # [V2]
        ("R03", "Bosch GSB 18V-150 C ProCORE"),     # [V2]
        ("R04", "Bosch GSR 18V-90 C ProCORE"),      # [V2]
        ("R05", "FLEX FX1271 24V"),                 # [V2]
        ("R06", "Makita XPH14 18V LXT"),
        ("R07", "Makita GPH01 40V XGT"),
        ("R08", "Milwaukee M18 FUEL 2904"),
        ("R09", "Milwaukee M12 FUEL 3404"),
        ("R10", "Metabo SB 18 LTX BL Q I"),
        ("R11", "Hilti SF 6H-22 Nuron"),
        ("R12", "Ryobi ONE+ HP PBLDD01"),
    ],
    "matriz": np.array([
        # preço  torque tensão  Ah  ecoss. assist. durab. peso
        [ 3980,  125.0, 60,  9.0, 300, 8.5, 9.4, 2.60],  # [V2] DeWalt FLEXVOLT
        [ 2450,   90.0, 20,  5.0, 300, 8.5, 9.0, 1.75],  # [V2] DeWalt POWERSTACK
        [ 3650,  150.0, 18,  8.0, 280, 9.2, 9.2, 2.40],  # [V2] Bosch GSB 18V-150
        [ 2890,   90.0, 18,  8.0, 280, 9.2, 9.0, 1.95],  # [V2] Bosch GSR 18V-90
        [ 3200,  105.0, 24,  3.5,  60, 4.0, 9.6, 2.20],  # [V2] FLEX 24V
        [ 2380,   80.0, 18,  5.0, 320, 9.6, 8.8, 1.90],  # Makita XPH14 LXT
        [ 4150,  140.0, 40,  4.0, 130, 8.8, 9.5, 2.75],  # Makita XGT 40V
        [ 3450,  135.0, 18,  6.0, 290, 6.5, 9.6, 2.30],  # Milwaukee M18 FUEL
        [ 2100,   65.0, 12,  5.0, 130, 6.5, 8.6, 1.30],  # Milwaukee M12 FUEL
        [ 2950,  120.0, 18,  5.5, 190, 7.0, 9.2, 2.35],  # Metabo SB 18 LTX
        [ 5600,  160.0, 22,  8.0, 210, 9.8, 9.8, 2.50],  # Hilti Nuron
        [ 1180,   60.0, 18,  4.0, 260, 7.5, 6.5, 1.85],  # Ryobi ONE+ HP
    ], dtype=float),
    # Ecossistema é a CAUSA RAIZ: dita a assistência que o comprador terá, a
    # disponibilidade de bateria e, por elas, o custo real ao longo dos anos.
    # Preço do kit é o efeito mais visível e o menos decisivo.
    "dematel": np.array([
        #  preço torq tens  Ah  ecos assist durab peso
        [0, 1, 1, 1, 1, 1, 1, 0],   # preço do kit -> EFEITO
        [3, 0, 2, 1, 1, 0, 2, 3],   # torque
        [3, 4, 0, 2, 2, 1, 2, 3],   # tensão da plataforma
        [3, 2, 2, 0, 1, 1, 1, 4],   # capacidade da bateria
        [3, 1, 3, 3, 0, 4, 2, 1],   # ecossistema -> CAUSA RAIZ
        [2, 0, 1, 2, 2, 0, 2, 0],   # assistência
        [3, 2, 1, 1, 1, 2, 0, 2],   # durabilidade
        [1, 1, 1, 2, 0, 0, 1, 0],   # peso
    ], dtype=float),
    # Uso profissional: ecossistema e assistência acima de preço.
    "ahp": _saaty([4, 2, 6, 5, 0, 1, 3, 7]),
}

CATALOGO_PARAFUSADEIRAS = {c["id_caso"]: c for c in (
    PARAFUSADEIRAS_DOMESTICAS, PARAFUSADEIRAS_PROFISSIONAIS)}

if __name__ == "__main__":
    from casos.catalogo import validar
    for c in CATALOGO_PARAFUSADEIRAS.values():
        validar(c)
        a, k = len(c["alternativas"]), len(c["criterios"])
        print(f"✅ {c['id_caso']:<30} {c['dominio']:<12} {a:>3} alt × {k} crit")
