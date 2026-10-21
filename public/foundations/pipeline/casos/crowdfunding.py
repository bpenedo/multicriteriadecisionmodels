"""
Estudo de caso: financiamento de startups por fundos de venture capital em
plataforma de crowdfunding.

═══════════════════════════════════════════════════════════════════════════════
 FONTE — SKARE, Marinko; GAVUROVA, Beata; POLISHCHUK, Volodymyr.
 "A decision-making support model for financing start-up projects by venture
 capital funds on a crowdfunding platform".
 Journal of Business Research, v. 158, 113719, 2023. Elsevier.
 Juraj Dobrila University of Pula · University of Economics and Human Sciences
 in Warsaw · Tomas Bata University in Zlin · Uzhhorod National University.
 [Ultimos/A_decision_making_support_model_for_financing_start_up_projects.pdf]
═══════════════════════════════════════════════════════════════════════════════

O QUE É FIEL AO ARTIGO. Os critérios e suas ESCALAS DE PONTUAÇÃO são os do
trabalho de origem, seção 4:

  · KS1..KS9 — avaliação da ideia inovadora, cada um com sua escala discreta
    (KS1: 5/8/15/25 pontos; KS2: 10/15/18/20; KS3: 10/15/20/25; KS4: 5/15/20/25;
     KS5: 5/15/20/25; KS6: 5/10/15/20; KS7: 5/7/10/15/20; KS8: 8/15/20;
     KS9: 10/15/25)
  · KH1..KH8 — competência do time, escala contínua [a;b]
  · MR — risco de implementação, variáveis linguísticas com grau de confiança

Nove critérios foram consolidados a partir desses três blocos: KS4 entrou junto
de KS2 (ambos medem atratividade de mercado) e KS8+KS9 viraram um só (proteção
jurídica e de PI), porque dezessete rótulos tornam o diagrama DEMATEL ilegível
(lição do #BUG-021). Os oito critérios de time do artigo entram agregados em
"competência do time", como o próprio artigo faz no passo 3 do modelo híbrido.

O QUE É NOSSO. A matriz de avaliação — dezesseis projetos numa plataforma de
crowdfunding — é instanciação própria, pontuada DENTRO das escalas do artigo.
O trabalho de origem valida o modelo num único projeto real, não publicado.

DIFERENÇA DE MÉTODO, declarada. O artigo resolve por lógica fuzzy (funções de
pertinência S-spline, convoluções pessimista/média/otimista, defuzzificação e
interpretação linguística). Aqui o mesmo problema passa pelos DEZ MÉTODOS deste
projeto, com pesos do DEMATEL. Não é reprodução do algoritmo: é o mesmo problema
de decisão submetido a outras escolas — e a convergência (ou não) é o achado.

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import numpy as np

from casos.catalogo import _saaty

CROWDFUNDING_STARTUPS = {
    "id_caso": "crowdfunding_startups",
    "nome": "Financiamento de startups em plataforma de crowdfunding",
    "dominio": "corporativo",
    "decisor": "Fundo de venture capital em plataforma de crowd-investment",
    "descricao": (
        "Dezesseis projetos numa plataforma de crowdfunding, avaliados pelos critérios e "
        "escalas do modelo de origem. O problema que o artigo ataca não é escolher o melhor "
        "projeto — é **impedir que a avaliação enviesada dos especialistas da plataforma "
        "decida sozinha** onde o fundo põe dinheiro. Daí a estrutura em três blocos: a ideia "
        "(KS1–KS9), o time (KH1–KH8) e o risco de implementação. A tese central, que o "
        "DEMATEL confirma por via causal: **competência do time e maturidade da ideia são "
        "causas; risco é efeito**. Fundo que tenta reduzir risco olhando para o risco está "
        "olhando o termômetro."),
    "criterios": [
        ("maturidade",  "Maturidade da ideia (KS1)",       "benefit", "pts 5-25"),
        ("mercado",     "Atratividade de mercado (KS2/KS4)", "benefit", "pts 15-45"),
        ("impacto",     "Relevância e impacto (KS3)",      "benefit", "pts 10-25"),
        ("competicao",  "Posição competitiva (KS5)",       "benefit", "pts 5-25"),
        ("parcerias",   "Parceiro estratégico (KS6)",      "benefit", "pts 5-20"),
        ("capital_setor", "Capital captado no setor (KS7)", "benefit", "pts 5-20"),
        ("juridico_pi", "Proteção jurídica e de PI (KS8/KS9)", "benefit", "pts 18-45"),
        ("time",        "Competência do time (KH1–KH8)",   "benefit", "0-10"),
        ("risco",       "Risco de implementação (MR)",     "cost",    "0-10"),
    ],
    "alternativas": [
        ("C01", "Healthtech de diagnóstico por imagem"),
        ("C02", "Marketplace B2B de insumos"),
        ("C03", "Fintech de crédito para MEI"),
        ("C04", "Agtech de irrigação inteligente"),
        ("C05", "Edtech de formação técnica"),
        ("C06", "Climatech de captura de carbono"),
        ("C07", "Foodtech de proteína alternativa"),
        ("C08", "Logtech de roteirização"),
        ("C09", "Biotech de terapia celular"),
        ("C10", "SaaS de conformidade regulatória"),
        ("C11", "Hardware de sensoriamento industrial"),
        ("C12", "Insurtech paramétrica"),
        ("C13", "Plataforma de energia distribuída"),
        ("C14", "Cybersecurity para OT industrial"),
        ("C15", "Proptech de gestão predial"),
        ("C16", "Mobilidade elétrica urbana"),
    ],
    # Pontuações dentro das escalas do artigo.
    "matriz": np.array([
        # matur. mercado impacto compet. parc. capital jurid+PI time risco
        [ 25.0, 40.0, 25.0, 20.0, 15.0, 15.0, 40.0, 8.6, 4.2],  # healthtech imagem
        [ 15.0, 35.0, 15.0, 15.0, 10.0, 10.0, 23.0, 7.4, 3.5],  # marketplace B2B
        [ 25.0, 45.0, 15.0, 15.0, 20.0, 20.0, 45.0, 8.8, 5.0],  # fintech MEI
        [ 15.0, 33.0, 20.0, 25.0, 15.0, 10.0, 30.0, 8.0, 4.6],  # agtech irrigação
        [ 25.0, 25.0, 15.0, 15.0, 10.0,  7.0, 23.0, 7.2, 2.8],  # edtech
        [  8.0, 38.0, 20.0, 20.0, 20.0, 15.0, 35.0, 8.4, 7.5],  # climatech
        [ 15.0, 30.0, 20.0, 15.0, 10.0, 10.0, 30.0, 6.8, 6.4],  # foodtech
        [ 25.0, 35.0, 15.0, 15.0, 15.0, 10.0, 23.0, 7.8, 3.2],  # logtech
        [  5.0, 40.0, 25.0, 25.0, 15.0, 20.0, 45.0, 9.2, 8.8],  # biotech celular
        [ 25.0, 30.0, 15.0, 20.0, 15.0,  7.0, 45.0, 8.2, 2.5],  # SaaS conformidade
        [ 15.0, 28.0, 15.0, 25.0, 10.0,  7.0, 35.0, 7.6, 6.0],  # hardware industrial
        [  8.0, 38.0, 20.0, 20.0, 15.0, 15.0, 40.0, 7.0, 5.8],  # insurtech paramétrica
        [ 15.0, 40.0, 20.0, 15.0, 20.0, 15.0, 35.0, 8.0, 6.2],  # energia distribuída
        [ 25.0, 35.0, 20.0, 25.0, 15.0, 15.0, 40.0, 9.4, 3.8],  # cybersecurity OT
        [ 25.0, 25.0, 10.0, 15.0, 10.0,  5.0, 23.0, 6.5, 3.0],  # proptech
        [  8.0, 43.0, 20.0, 15.0, 20.0, 20.0, 30.0, 7.4, 7.0],  # mobilidade elétrica
    ], dtype=float),
    # Estrutura causal do modelo de origem: TIME e MATURIDADE são as causas
    # raiz — governam a execução e, por ela, o risco. RISCO é o maior efeito:
    # é o que o fundo mede, não o que o fundo controla.
    "dematel": np.array([
        #    mat merc imp comp parc cap jur time risco
        [0, 2, 1, 2, 2, 2, 2, 1, 4],   # maturidade -> CAUSA
        [1, 0, 2, 3, 2, 3, 1, 0, 2],   # mercado
        [0, 3, 0, 1, 2, 2, 1, 0, 1],   # impacto
        [1, 2, 1, 0, 1, 2, 2, 0, 2],   # posição competitiva
        [1, 2, 0, 2, 0, 2, 1, 1, 2],   # parcerias
        [1, 3, 1, 2, 2, 0, 1, 0, 2],   # capital do setor
        [1, 1, 0, 3, 1, 1, 0, 0, 3],   # jurídico e PI
        [4, 2, 1, 2, 3, 2, 2, 0, 4],   # time -> CAUSA RAIZ
        [1, 1, 0, 1, 1, 1, 1, 0, 0],   # risco -> MAIOR EFEITO
    ], dtype=float),
    # Prioridade declarada do fundo: time > maturidade > risco > mercado > ...
    "ahp": _saaty([1, 3, 7, 5, 6, 8, 4, 0, 2]),
}

CATALOGO_CROWDFUNDING = {CROWDFUNDING_STARTUPS["id_caso"]: CROWDFUNDING_STARTUPS}

if __name__ == "__main__":
    from casos.catalogo import validar
    for c in CATALOGO_CROWDFUNDING.values():
        validar(c)
        a, k = len(c["alternativas"]), len(c["criterios"])
        print(f"✅ {c['id_caso']:<26} {c['dominio']:<12} {a:>3} alt × {k} crit")
