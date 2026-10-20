"""
Gerador dos READMEs nos 12 idiomas, a partir de um TEMPLATE com blocos.

POR QUE TEMPLATE E NÃO TRADUÇÃO DIRETA
--------------------------------------
Traduzir 12 arquivos à mão garante que eles divergem: alguém corrige um exemplo em
português e os outros 11 ficam desatualizados em silêncio. Pior, uma tradução por
substituição de termos deixa frases pela metade — foi exatamente o #BUG-017.

Aqui a estrutura (títulos, tabelas, badges, blocos de código, caminhos de imagem) vive
em UM template. Só a prosa é bloco traduzível, identificado por chave. Um bloco sem
tradução é ERRO DE GERAÇÃO, não um trecho que sai em português sem ninguém notar:
a cobertura é verificada por construção, e o gerador se recusa a escrever um README
incompleto.

Uso:
    python3 gerar_readmes.py              # gera os 12
    python3 gerar_readmes.py --verificar  # só checa cobertura
    python3 gerar_readmes.py --idioma en

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import argparse
import json
import re
import sys
from pathlib import Path

from config import ENCODING, PIPELINE_DIR, PROJETO_DIR

BLOCOS_JSON = PROJETO_DIR / "_private" / "foundations" / "translation" / "readme.blocos.json"
TEMPLATE = PROJETO_DIR / "_private" / "foundations" / "translation" / "readme.template.md"

IDIOMAS = [
    ("pt", "Português", "README.md", "ltr"),
    ("en", "English", "README.en.md", "ltr"),
    ("es", "Español", "README.es.md", "ltr"),
    ("fr", "Français", "README.fr.md", "ltr"),
    ("de", "Deutsch", "README.de.md", "ltr"),
    ("zh", "中文", "README.zh.md", "ltr"),
    ("ko", "한국어", "README.ko.md", "ltr"),
    ("hi", "हिन्दी", "README.hi.md", "ltr"),
    ("he", "עברית", "README.he.md", "rtl"),
    ("ru", "Русский", "README.ru.md", "ltr"),
    ("sv", "Svenska", "README.sv.md", "ltr"),
    ("fi", "Suomi", "README.fi.md", "ltr"),
]

PADRAO_BLOCO = re.compile(r"\{\{([a-z0-9_.]+)\}\}")

# ---------------------------------------------------------------------------
# Tabelas dinâmicas de estudos de caso
# ---------------------------------------------------------------------------
# Por que geradas e não escritas no template: a tabela de casos é a parte do README
# que ENVELHECE — todo caso novo a torna mentirosa, em 12 idiomas de uma vez, e sem
# nenhum sinal de que ficou desatualizada. Antes ela era colada no template a cada
# rodada, e a cada rodada alguém tinha de lembrar. Agora ela é derivada do CATALOGO
# e do banco na hora da geração: se o catálogo cresce, os 12 READMEs crescem juntos.
#
# Os placeholders são MAIÚSCULOS de propósito — PADRAO_BLOCO só casa minúsculas, então
# não competem com os blocos traduzíveis e são substituídos depois deles, como {{SELETOR}}.

# Domínio do caso -> chave do bloco traduzível que o nomeia.
DOMINIO_BLOCO = {
    "consumo": "dm_consumo", "automotivo": "dm_automotivo", "defesa": "dm_defesa",
    "corporativo": "dm_corporativo", "ti": "dm_ti", "financeiro": "dm_financeiro",
    "imobiliario": "dm_imobiliario", "operacoes": "dm_operacoes",
    "manufatura": "dm_manufatura", "agronegocio": "dm_agronegocio",
    "infraestrutura": "dm_infraestrutura",
}

# Classificação de robustez -> chave do bloco traduzível.
VEREDITO_BLOCO = {
    "ROBUSTO": "vd_robusto", "PROVÁVEL": "vd_provavel", "FRÁGIL": "vd_fragil",
}

# Casos derivados de fonte externa: AUTORIA e LINK verificáveis.
#
# A autoria foi lida da FOLHA DE ROSTO de cada trabalho em
# _private/foundations/kb/Artigos e Teses — não de memória nem de busca. `links`
# só recebe DOI/URL que resolveu de fato (CrossRef, ou o endereço do vídeo).
# Trabalho sem DOI indexado — TCC, tese, anais de congresso nacional, relatório
# técnico — fica com a referência textual completa e `links` vazio. Um DOI
# inventado que leva a outro artigo é pior que link nenhum: atribui a terceiros
# um trabalho que não é deles.
#
# `autores` é quem ASSINA o trabalho de origem, não quem implementou o caso aqui.
FONTES_KB = {
    "acoes_b3": {
        "autores": "COSTA, L. S. da · VÁSQUEZ, J. A.; ESCOBAR, J. W.; MANOTAS, D. F.",
        "ref": "*Uma metodologia para a pré-seleção de ações utilizando o método "
               "multicritério TOPSIS* (COSTA, UERJ) · *AHP–TOPSIS Methodology for Stock "
               "Portfolio Investments*, Risks, v.10, n.1, 4, 2022 (Universidad del Valle)",
        "links": ["https://doi.org/10.3390/risks10010004"]},
    "fundos_imobiliarios": {
        "autores": "SANTOS, V. V. dos (orient. ALMEIDA FILHO, A. T. de)",
        "ref": "*Avaliação do método Random Forest para auxílio à seleção de fundos de "
               "investimento imobiliário listados na Bolsa de Valores*. Trabalho de "
               "Graduação, Engenharia da Computação, CIn/UFPE, set. 2023",
        "links": []},
    "fintech": {
        "autores": "WIBOWO, S.; GRANDHI, L.; GRANDHI, S.; WELLS, M.",
        "ref": "*A Fuzzy Multicriteria Group Decision Making Approach for Evaluating and "
               "Selecting Fintech Projects*. Mathematics, v.10, n.2, 225, 2022 — "
               "CQUniversity, Austrália",
        "links": ["https://doi.org/10.3390/math10020225"]},
    "avaliacao_imoveis": {
        "autores": "DUARTE, D. C. de O. · MARQUES, J. P. M.",
        "ref": "*Análise multicritério e geoestatística aplicadas na avaliação em massa de "
               "imóveis urbanos*. Tese, UFV, 2019 · *As formas de avaliar imóvel em leilão "
               "judicial*. Universidade São Judas Tadeu, 2023",
        "links": []},
    "ordens_servico": {
        "autores": "ALENCAR, L. G. de; TAVARES, F. R. M.; "
                   "MENDONÇA, F. J. S. de F.; DUARTE, A. K. G.",
        "ref": "*Priorização de ordens de serviço aplicando métodos de tomada de decisão: "
               "o AHP integrado ao PROMETHEE*. Revista Produção Online, v.22, n.2, "
               "p.2763-2784, 2022 — URCA, Ceará",
        "links": []},
    "cloud_providers": {
        "autores": "SOLOMON, T.",
        "ref": "*Ranking of Cloud Service Providers Using a Dynamic TOPSIS Model for "
               "Provisioning of Enterprise IT Infrastructure in the Cloud*. Praxis "
               "(Doctor of Engineering), The George Washington University, 2017",
        "links": []},
    "venture_capital": {
        "autores": "BEIM, G.; LÉVESQUE, M. · DHOCHAK, M.; DOLIYA, P. · "
                   "AFFUL-DADZIE, E.; AFFUL-DADZIE, A.; OPLATKOVÁ, Z. K.",
        "ref": "*Selecting projects for venture capital funding: a multiple criteria "
               "decision approach* (Case Western Reserve University) · *Valuation of a "
               "startup: moving towards strategic approaches*, J. Multi-Criteria Decision "
               "Analysis, 2019 · *Assessing commercial viability of technology start-up "
               "businesses in a government venture capital under intuitionistic fuzzy "
               "environment*, Int. J. Fuzzy Systems, 2016",
        "links": ["https://doi.org/10.1002/mcda.1703",
                  "https://doi.org/10.1007/s40815-016-0141-9"]},
    "instrutores": {
        "autores": "SILVA, C. E. J. da; SALLES-NETO, L. L. de; SANTOS, M. dos",
        "ref": "*Modelagem matemática com os métodos AHP e TOPSIS para ordenação de "
               "instrutores em uma escola da FAB*. LIV SBPO, Juiz de Fora, 2022 — "
               "ITA / UNIFESP / IME",
        "links": []},
    "cripto_portfolio": {
        "autores": "ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T.",
        "ref": "*Cryptocurrency Portfolio Selection — A Multicriteria Approach*. "
               "Mathematics, v.9, n.14, 1677, 2021 — University of Split, Croácia — "
               "**pesos AHP do artigo**",
        "links": ["https://doi.org/10.3390/math9141677"]},
    "portfolio_crise": {
        "autores": "COSTA, I. P. de A.; MAÊDA, S. M. do N.; "
                   "TEIXEIRA, L. F. H. de S. de B.; GOMES, C. F. S.; SANTOS, M. dos",
        "ref": "*Finanças em períodos de crise: aplicação do método SAPEVO-M para "
               "composição de portfólios de investimentos*. Pesquisa Operacional para o "
               "Desenvolvimento, v.13, e13004, 2021 — UFF / CASNAV / IME — "
               "**matriz de decisão do artigo**",
        "links": []},
    "cenarios_va": {
        "autores": "LI, S.; ZHOU, R.; HUANG, H.",
        "ref": "*Multidimensional Evaluation of Autonomous Driving Test Scenarios Based on "
               "AHP-EWM-TOPSIS Models*. Automotive Innovation, 2025",
        "links": ["https://doi.org/10.1007/s42154-024-00344-6"]},
    "impressora_3d_energia": {
        "autores": "OLIVEIRA, V. A. R. de; ALVARADO SILVA, C. A.; OLIVEIRA, G. C. R. de; "
                   "TAJIMA, F. M.; FARIA NETO, A. dos R.; SALOMON, V. A. P.; GUIDI, E. S.",
        "ref": "*Multicriteria Analysis for 3D Printer Selection*. 23rd LACCEI "
               "International Multi-Conference, Cidade do México, 2025 — "
               "UNESP / Universidad César Vallejo",
        "links": ["https://doi.org/10.18687/LACCEI2025.1.1.1193"]},
    "impressoras_juridico": {
        "autores": "OLIVEIRA, N. C.; OLIVEIRA, P. F. C. de; GOMES, C. F. S.; SANTOS, M. dos",
        "ref": "*Aplicação do método AHP TOPSIS 2N como apoio à tomada de decisão: estudo "
               "de caso no departamento jurídico da Secretaria Municipal de Saúde de Duque "
               "de Caxias* — UNIGRANRIO / UFF / IME",
        "links": []},
    "fundos_hedge": {
        "autores": "SILVA, F. P. da; RIBEIRO, C. de O.",
        "ref": "*Análise comparativa de fundos de hedge brasileiros utilizando DEA e "
               "bootstrap*. XII SIMPEP, Bauru-SP, 2005 — Escola Politécnica da USP",
        "links": []},
    "modelos_previsao": {
        "autores": "SHAH, S.",
        "ref": "*Comparison of Stochastic Forecasting Models*. Stochastic Differential "
               "Equations Course Project, Johns Hopkins University — o artigo compara os "
               "modelos; a modelagem multicritério sobre eles é deste projeto",
        "links": []},
    "policultivo_rj": {
        "autores": "PENEDO, B.",
        "ref": "*AGTech PoliCultivo 4.0 — Otimização de Portfólio de Cultivos em Ambiente "
               "Controlado (RJ)*. Relatório técnico, 03/08/2026, seção 14 — "
               "**matriz e pesos do relatório**",
        "links": []},
    "parafusadeiras_domesticas": {
        "autores": "COMPROU AVALIOU (canal)",
        "ref": "*As 5 Melhores Parafusadeira De 2025*, 14/05/2024 — especificações "
               "extraídas da narração",
        "links": ["https://youtu.be/pgdqVYEjZtk"]},
    "parafusadeiras_profissionais": {
        "autores": "FERRAMENTAS EM AÇÃO — ASSIS PIRES (canal)",
        "ref": "*As Melhores Parafusadeiras Do Mundo*, 04/01/2024 — modelos e baterias "
               "lidos dos quadros do vídeo",
        "links": ["https://youtube.com/shorts/9SIs3agoZKc"]},
    "crowdfunding_startups": {
        "autores": "SKARE, M.; GAVUROVA, B.; POLISHCHUK, V.",
        "ref": "*A decision-making support model for financing start-up projects by venture "
               "capital funds on a crowdfunding platform*. Journal of Business Research, "
               "v.158, 113719, 2023 — **critérios e escalas do artigo**",
        "links": ["https://doi.org/10.1016/j.jbusres.2023.113719"]},
}


def _rotulo_link(url):
    return "vídeo" if "youtu" in url else "DOI"


def referencia_curta(id_caso, bloco_autoral):
    """Célula de autoria da tabela de casos: autores + link, ou 'modelagem autoral'.

    O link entra como rótulo curto ("DOI", "vídeo") e não como URL crua: uma URL
    de 60 caracteres numa célula estoura a largura da tabela em 12 idiomas, e o
    README é lido tanto no GitHub quanto no terminal. Quando o trabalho tem mais
    de um DOI, só o primeiro vem para cá; a lista completa fica na tabela de
    estudos derivados da literatura, logo abaixo.
    """
    f = FONTES_KB.get(id_caso)
    if not f:
        return bloco_autoral
    if not f["links"]:
        return f["autores"]
    url = f["links"][0]
    return f"{f['autores']} · [{_rotulo_link(url)}]({url})"


# Blocos consumidos SÓ pelas tabelas dinâmicas. Precisam ser declarados aqui, senão
# `verificar()` os acusa de órfãos (não aparecem no template) e a cobertura deixa de
# ser checada justamente nos blocos que ninguém vê ao ler o template. Ver bugs.md #BUG-034.
CHAVES_DINAMICAS = (tuple(DOMINIO_BLOCO.values()) + tuple(VEREDITO_BLOCO.values())
                    + ("th_caso", "th_dominio", "th_alternativas", "th_criterios",
                       "th_veredito", "th_fonte", "th_autoria", "th_autores",
                       "autoria_propria"))


def _catalogo_e_vereditos():
    """Catálogo de casos + veredito de cada um. O veredito é opcional: um caso recém
    cadastrado e ainda não executado entra na tabela sem coluna de robustez, em vez
    de derrubar a geração do README."""
    sys.path.insert(0, str(PIPELINE_DIR))
    from casos import CATALOGO
    vereditos = {}
    try:
        from db import get_conn
        conn = get_conn()
        vereditos = {r[0]: (r[1], r[2]) for r in conn.execute(
            "SELECT id_caso, classificacao, prob_vitoria FROM veredito")}
        conn.close()
    except Exception:
        pass                       # sem banco, a tabela sai sem veredito — e diz isso
    return CATALOGO, vereditos


def tabela_casos(codigo, blocos):
    """Tabela com TODOS os casos do catálogo, no idioma pedido."""
    catalogo, vereditos = _catalogo_e_vereditos()

    def t(chave):
        return blocos.get(chave, {}).get(codigo, chave)

    linhas = [f"| # | {t('th_caso')} | {t('th_dominio')} | {t('th_alternativas')} | "
              f"{t('th_criterios')} | {t('th_veredito')} | {t('th_autoria')} |",
              "|--:|---|---|--:|--:|---|---|"]
    for i, (id_caso, caso) in enumerate(catalogo.items(), 1):
        marca = " 📚" if id_caso in FONTES_KB else ""
        cls, prob = vereditos.get(id_caso, (None, None))
        vd = f"{t(VEREDITO_BLOCO[cls])} {prob:.0f}%" if cls in VEREDITO_BLOCO else "—"
        linhas.append(f"| {i} | `{id_caso}`{marca} | {t(DOMINIO_BLOCO[caso['dominio']])} | "
                      f"{len(caso['alternativas'])} | {len(caso['criterios'])} | {vd} | "
                      f"{referencia_curta(id_caso, t('autoria_propria'))} |")
    return "\n".join(linhas)


def tabela_casos_kb(codigo, blocos):
    """Tabela dos casos derivados da literatura, com referência e autoria."""
    catalogo, _ = _catalogo_e_vereditos()

    def t(chave):
        return blocos.get(chave, {}).get(codigo, chave)

    linhas = [f"| {t('th_caso')} | {t('th_dominio')} | {t('th_autores')} | {t('th_fonte')} |",
              "|---|---|---|---|"]
    for id_caso, f in FONTES_KB.items():
        caso = catalogo.get(id_caso)
        if caso is None:
            continue
        ref = f["ref"]
        if f["links"]:
            ref += " · " + " · ".join(f"[{_rotulo_link(u)}]({u})" for u in f["links"])
        linhas.append(f"| `{id_caso}` | {t(DOMINIO_BLOCO[caso['dominio']])} | "
                      f"{f['autores']} | {ref} |")
    return "\n".join(linhas)



def seletor_idiomas(codigo_atual):
    """Linha de seleção: idioma atual em negrito, os demais como link relativo."""
    itens = []
    for cod, nome, arquivo, _ in IDIOMAS:
        itens.append(f"**{nome}**" if cod == codigo_atual else f"[{nome}]({arquivo})")
    return "🌐 " + " · ".join(itens)


def carregar():
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"template não encontrado: {TEMPLATE}")
    if not BLOCOS_JSON.exists():
        raise FileNotFoundError(f"blocos não encontrados: {BLOCOS_JSON}")
    return (TEMPLATE.read_text(encoding=ENCODING),
            json.loads(BLOCOS_JSON.read_text(encoding=ENCODING)))


def chaves_do_template(template):
    """Todas as chaves {{...}} usadas, na ordem de aparição, sem repetição."""
    vistas, ordem = set(), []
    for m in PADRAO_BLOCO.finditer(template):
        if m.group(1) not in vistas:
            vistas.add(m.group(1))
            ordem.append(m.group(1))
    return ordem


def verificar(template, blocos):
    """Confere que todo bloco do template existe em todo idioma. Devolve problemas."""
    chaves = chaves_do_template(template) + [
        k for k in CHAVES_DINAMICAS if k not in chaves_do_template(template)]
    problemas = []
    for cod, nome, _arq, _d in IDIOMAS:
        se_falta = [k for k in chaves if not blocos.get(k, {}).get(cod, "").strip()]
        if se_falta:
            problemas.append(
                f"[{cod}] {len(se_falta)}/{len(chaves)} bloco(s) sem tradução: "
                f"{', '.join(se_falta[:5])}{' ...' if len(se_falta) > 5 else ''}")
    orfaos = [k for k in blocos if k not in chaves]
    if orfaos:
        problemas.append(f"blocos definidos e não usados no template: {', '.join(orfaos[:5])}")
    return chaves, problemas


def gerar(codigo, template, blocos):
    """Materializa o README de um idioma. Falha se algum bloco estiver ausente."""
    faltando = []

    def _sub(m):
        chave = m.group(1)
        valor = blocos.get(chave, {}).get(codigo, "")
        if not valor.strip():
            faltando.append(chave)
            return f"⟪FALTA:{chave}⟫"
        return valor

    texto = PADRAO_BLOCO.sub(_sub, template)
    if faltando:
        raise ValueError(
            f"README '{codigo}' incompleto: {len(faltando)} bloco(s) sem tradução "
            f"({', '.join(sorted(set(faltando))[:5])}). Nada foi escrito.")

    texto = texto.replace("{{SELETOR}}", seletor_idiomas(codigo))
    texto = texto.replace("{{TABELA_CASOS}}", tabela_casos(codigo, blocos))
    texto = texto.replace("{{TABELA_CASOS_KB}}", tabela_casos_kb(codigo, blocos))
    return texto


def main():
    ap = argparse.ArgumentParser(description="Gera os READMEs nos 12 idiomas.")
    ap.add_argument("--verificar", action="store_true", help="só checa cobertura")
    ap.add_argument("--idioma", help="gera apenas este idioma")
    args = ap.parse_args()

    template, blocos = carregar()
    chaves, problemas = verificar(template, blocos)

    print(f"Template: {len(chaves)} blocos · {len(IDIOMAS)} idiomas "
          f"= {len(chaves) * len(IDIOMAS)} segmentos")
    if problemas:
        print(f"\n⚠️  {len(problemas)} problema(s) de cobertura:")
        for p in problemas:
            print(f"   • {p}")
        if args.verificar:
            return 1
    else:
        print("✅ cobertura completa: todo bloco traduzido em todo idioma.")
    if args.verificar:
        return 0

    alvos = [i for i in IDIOMAS if not args.idioma or i[0] == args.idioma]
    escritos = 0
    for cod, nome, arquivo, _direcao in alvos:
        try:
            texto = gerar(cod, template, blocos)
        except ValueError as erro:
            print(f"❌ {arquivo}: {erro}")
            continue
        destino = PROJETO_DIR / arquivo
        destino.write_text(texto, encoding=ENCODING)
        print(f"  📄 {arquivo:<16} {nome:<12} {len(texto.splitlines()):>4} linhas")
        escritos += 1
    print(f"\n✅ {escritos}/{len(alvos)} READMEs gerados.")
    return 0 if escritos == len(alvos) else 1


if __name__ == "__main__":
    sys.exit(main())
