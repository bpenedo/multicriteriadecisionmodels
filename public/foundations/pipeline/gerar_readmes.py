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

from config import ENCODING, PROJETO_DIR

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
    chaves = chaves_do_template(template)
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
