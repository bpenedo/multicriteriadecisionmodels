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

# Casos derivados da base de conhecimento, com a referência que DEVE acompanhá-los.
# Isto não é decoração: os critérios vieram do texto destes autores, e a atribuição
# viaja junto com a tabela em todos os 12 idiomas.
FONTES_KB = {
    "acoes_b3": "COSTA, L. S. *Uma metodologia para a pré-seleção de ações utilizando o "
                "método multicritério TOPSIS*; *AHP–TOPSIS Methodology for Stock Portfolio "
                "Investments*, Risks 10(4):4, 2022",
    "fundos_imobiliarios": "SANTOS, V. V. *TCC*, Engenharia da Computação, UFPE",
    "fintech": "*A Fuzzy Multicriteria Group Decision Making Approach for Evaluating and "
               "Selecting Fintech Projects*",
    "avaliacao_imoveis": "DUARTE, D. C. O. *Análise multicritério e geoestatística aplicadas "
                         "na avaliação de imóveis*; MARQUES, J. P. M.",
    "ordens_servico": "*Priorização de ordens de serviço: o AHP integrado ao PROMETHEE*. "
                      "Revista Produção Online, v.22, n.2, 2022",
    "cloud_providers": "SOLOMON. *Ranking of Cloud Service Providers Using a Dynamic TOPSIS "
                       "Model*. The George Washington University",
    "venture_capital": "BEIM, G.; LÉVESQUE, M.; DHOCHAK, M. et al. (2019); AFFUL-DADZIE, E. "
                       "et al.; MILKOVA/ANDREICHIKOV (IJAHP)",
    "instrutores": "*Modelagem matemática com os métodos AHP e TOPSIS para ordenação de "
                   "instrutores em uma escola da FAB*. LIV SBPO, 2022",
    "cripto_portfolio": "ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. *Cryptocurrency "
                        "Portfolio Selection — A Multicriteria Approach*. Mathematics, "
                        "9(14):1677, 2021 — **pesos AHP do artigo**",
    "portfolio_crise": "COSTA, I. P. A.; MAÊDA, S. M. N.; TEIXEIRA, L. F. H. S. B.; GOMES, "
                       "C. F. S.; SANTOS, M. *Finanças em períodos de crise: aplicação do "
                       "método SAPEVO-M*. Pesquisa Operacional para o Desenvolvimento, "
                       "v.13, e13004, 2021 — **matriz de decisão do artigo**",
    "cenarios_va": "LI, S.; ZHOU, R.; HUANG, H. *Multidimensional Evaluation of Autonomous "
                   "Driving Test Scenarios Based on AHP-EWM-TOPSIS Models*. Automotive "
                   "Innovation, 2025",
    "impressora_3d_energia": "OLIVEIRA, V. A. R. et al. *Multicriteria Analysis for 3D "
                             "Printer Selection*. 23rd LACCEI, Cidade do México, 2025 — UNESP",
    "impressoras_juridico": "OLIVEIRA, N. C.; OLIVEIRA, P. F. C.; GOMES, C. F. S.; SANTOS, M. "
                            "*Aplicação do método AHP TOPSIS 2N: estudo de caso no departamento "
                            "jurídico da Secretaria Municipal de Saúde de Duque de Caxias*, 2019",
    "fundos_hedge": "SILVA, F. P.; RIBEIRO, C. O. *Análise comparativa de fundos de hedge "
                    "brasileiros utilizando DEA e bootstrap*. XII SIMPEP, Bauru-SP, 2005 — USP",
    "modelos_previsao": "SHAH, S. *Comparison of Stochastic Forecasting Models*. Johns Hopkins "
                        "University — o artigo compara os modelos; a modelagem multicritério é deste projeto",
    "policultivo_rj": "*AGTech PoliCultivo 4.0 — Otimização de Portfólio de Cultivos (RJ)*, "
                      "relatório técnico, 03/08/2026, seção 14 — **matriz e pesos do relatório**",
}

# Blocos consumidos SÓ pelas tabelas dinâmicas. Precisam ser declarados aqui, senão
# `verificar()` os acusa de órfãos (não aparecem no template) e a cobertura deixa de
# ser checada justamente nos blocos que ninguém vê ao ler o template. Ver bugs.md #BUG-034.
CHAVES_DINAMICAS = (tuple(DOMINIO_BLOCO.values()) + tuple(VEREDITO_BLOCO.values())
                    + ("th_caso", "th_dominio", "th_alternativas", "th_criterios",
                       "th_veredito", "th_fonte"))


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
              f"{t('th_criterios')} | {t('th_veredito')} |",
              "|--:|---|---|--:|--:|---|"]
    for i, (id_caso, caso) in enumerate(catalogo.items(), 1):
        marca = " 📚" if id_caso in FONTES_KB else ""
        cls, prob = vereditos.get(id_caso, (None, None))
        vd = f"{t(VEREDITO_BLOCO[cls])} {prob:.0f}%" if cls in VEREDITO_BLOCO else "—"
        linhas.append(f"| {i} | `{id_caso}`{marca} | {t(DOMINIO_BLOCO[caso['dominio']])} | "
                      f"{len(caso['alternativas'])} | {len(caso['criterios'])} | {vd} |")
    return "\n".join(linhas)


def tabela_casos_kb(codigo, blocos):
    """Tabela dos casos derivados da literatura, com referência e autoria."""
    catalogo, _ = _catalogo_e_vereditos()

    def t(chave):
        return blocos.get(chave, {}).get(codigo, chave)

    linhas = [f"| {t('th_caso')} | {t('th_dominio')} | {t('th_fonte')} |", "|---|---|---|"]
    for id_caso, fonte in FONTES_KB.items():
        caso = catalogo.get(id_caso)
        if caso is None:
            continue
        linhas.append(f"| `{id_caso}` | {t(DOMINIO_BLOCO[caso['dominio']])} | {fonte} |")
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
