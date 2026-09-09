"""
Pipeline de internacionalização: Translation Memory -> strings -> páginas -> TMX.

A fonte canônica é _private/foundations/translation/translation.memory.md, no padrão
SDL Trados Studio. Este módulo apenas a LÊ e materializa os artefatos; nenhuma string
traduzida é definida aqui. É o que garante que corrigir uma tradução seja uma edição
em um lugar só, e não uma caçada por 12 arquivos.

Uso:
    python3 gerar_i18n.py --tm          # extrai a TM -> translation/strings.<locale>.json
    python3 gerar_i18n.py --paginas     # gera evidence/pages/<lang>/index.md (12 idiomas)
    python3 gerar_i18n.py --tmx         # exporta translation.memory.tmx (importável no Trados)
    python3 gerar_i18n.py --verificar   # QA: o "Verify" do Trados
    python3 gerar_i18n.py --tudo

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

from config import ENCODING, EVIDENCE_DIR, PROJETO_DIR

TM_DIR = PROJETO_DIR / "_private" / "foundations" / "translation"
TM_MD = TM_DIR / "translation.memory.md"
TMX = TM_DIR / "translation.memory.tmx"

# locale -> (código curto de rota, nome nativo, direção)
LOCALES = {
    "pt-BR": ("pt", "Português", "ltr"),
    "en-US": ("en", "English", "ltr"),
    "es-ES": ("es", "Español", "ltr"),
    "fr-FR": ("fr", "Français", "ltr"),
    "de-DE": ("de", "Deutsch", "ltr"),
    "zh-CN": ("zh", "中文", "ltr"),
    "ko-KR": ("ko", "한국어", "ltr"),
    "hi-IN": ("hi", "हिन्दी", "ltr"),
    "he-IL": ("he", "עברית", "rtl"),
    "ru-RU": ("ru", "Русский", "ltr"),
    "sv-SE": ("sv", "Svenska", "ltr"),
    "fi-FI": ("fi", "Suomi", "ltr"),
}
ORIGEM = "pt-BR"

# Placeables — duas classes, com regras de QA DIFERENTES.
#
# SIGLAS: identificadores técnicos e de marca. Permanecem em caracteres latinos em
# TODOS os locales, inclusive nos de escrita não-latina — é assim que a literatura
# de MCDA os grafa em chinês, coreano, híndi, hebraico e russo.
SIGLAS_TECNICAS = [
    "AHP-TOPSIS 2n", "ELECTRE I", "ELECTRE II", "PROMETHEE II", "MAUT", "MCDA-C",
    "DEMATEL", "VIKOR", "TODIM", "SAPEVO-M", "AHP", "TOPSIS", "MCDM", "MCDA",
    "R+C", "R−C", "p05", "p95",
]

# NOMES PRÓPRIOS: em locales de escrita latina permanecem idênticos; em zh/ko/hi/he/ru
# a convenção editorial é TRANSLITERAR (Borda -> 波达 / 보르다 / बोर्डा / בורדה / Борда).
# Exigir a forma latina ali produziria um texto que nenhum leitor nativo escreveria —
# por isso o QA não os cobra nesses locales.
NOMES_PROPRIOS = ["Borda", "Dirichlet", "Saaty"]

# Locales cujo sistema de escrita não é latino.
ESCRITA_NAO_LATINA = {"zh-CN", "ko-KR", "hi-IN", "he-IL", "ru-RU"}

NAO_TRADUZIVEIS = SIGLAS_TECNICAS + NOMES_PROPRIOS


# ---------------------------------------------------------------------------
def _tabelas_markdown(texto):
    """Extrai toda tabela do Markdown como (cabecalho, linhas de células)."""
    tabelas = []
    atual, cabecalho = None, None
    for linha in texto.splitlines():
        crua = linha.strip()
        if crua.startswith("|") and crua.endswith("|"):
            celulas = [c.strip() for c in crua.strip("|").split("|")]
            if cabecalho is None:
                cabecalho, atual = celulas, []
            elif set("".join(celulas)) <= set("-: "):
                continue                                  # linha separadora
            else:
                atual.append(celulas)
        else:
            if cabecalho and atual:
                tabelas.append((cabecalho, atual))
            cabecalho, atual = None, None
    if cabecalho and atual:
        tabelas.append((cabecalho, atual))
    return tabelas


def carregar_tm():
    """Lê a TM em Markdown e devolve (glossario, direitos, unidades).

    glossario: {termo_pt: {locale: traducao}}
    direitos:  {locale: frase}
    unidades:  {tuid: texto_pt}
    """
    if not TM_MD.exists():
        raise FileNotFoundError(f"Translation Memory não encontrada: {TM_MD}")
    texto = TM_MD.read_text(encoding=ENCODING)
    tabelas = _tabelas_markdown(texto)

    glossario, direitos, unidades = {}, {}, {}
    alvos_segmento = {loc: {} for loc in LOCALES}     # {locale: {tuid: target}}
    locale_corrente = None

    # A seção 5b traz uma tabela por locale, precedida de um cabeçalho "### xx-YY".
    # Percorremos o texto para saber a que locale cada tabela |tuid|target| pertence.
    ordem_secoes = []
    for linha in texto.splitlines():
        cru = linha.strip()
        if cru.startswith("### ") and cru[4:9] in LOCALES:
            ordem_secoes.append(cru[4:9])
        elif cru.startswith("|") and "tuid" in cru and "target" in cru:
            locale_corrente = ordem_secoes[-1] if ordem_secoes else None
            if locale_corrente:
                ordem_secoes.append(f"__marcado__{locale_corrente}")

    for cabecalho, linhas in tabelas:
        c0 = cabecalho[0].strip()
        # --- glossário: primeira coluna 'pt-BR', demais são locales ----------
        if c0 == "pt-BR" and len(cabecalho) > 1 and cabecalho[1] in LOCALES:
            for celulas in linhas:
                if len(celulas) != len(cabecalho):
                    continue
                termo = celulas[0]
                alvo = glossario.setdefault(termo, {ORIGEM: termo})
                for col, valor in zip(cabecalho[1:], celulas[1:]):
                    alvo[col] = valor
        # --- frase de direitos ------------------------------------------------
        elif c0 == "Locale" and "DIREITOS" in cabecalho[-1].upper():
            for celulas in linhas:
                loc = celulas[0].strip("`")
                if loc in LOCALES:
                    direitos[loc] = celulas[1]
        # --- unidades de tradução --------------------------------------------
        elif c0 == "tuid" and len(cabecalho) >= 2 and cabecalho[1] == "target":
            # tabela da seção 5b — pertence ao locale do último cabeçalho "###".
            pass          # tratada abaixo, com o locale correto
        elif c0 == "tuid":
            for celulas in linhas:
                if len(celulas) >= 2:
                    unidades[celulas[0].strip("`")] = celulas[1]

    # --- seção 5b: uma tabela por locale ------------------------------------
    locale_atual = None
    dentro = False
    for linha in texto.splitlines():
        cru = linha.strip()
        if cru.startswith("### ") and cru[4:9] in LOCALES:
            locale_atual, dentro = cru[4:9], False
        elif cru.startswith("|") and cru.endswith("|"):
            celulas = [c.strip() for c in cru.strip("|").split("|")]
            if celulas[:2] == ["tuid", "target"]:
                dentro = True
            elif dentro and locale_atual and len(celulas) >= 2:
                if set("".join(celulas)) <= set("-: "):
                    continue
                alvos_segmento[locale_atual][celulas[0].strip("`")] = \
                    celulas[1].replace("\\|", "|")
        elif cru.startswith("#"):
            dentro = False

    if not glossario or not direitos or not unidades:
        raise ValueError(
            f"TM incompleta: {len(glossario)} termos, {len(direitos)} frases de "
            f"direitos, {len(unidades)} unidades. Confira as tabelas de "
            f"{TM_MD.name} (seções 3, 4 e 5).")
    return glossario, direitos, unidades, alvos_segmento


def traduzir_unidade(texto_pt, locale, glossario, alvos_locale=None, tuid=None):
    """Traduz uma TU aplicando o glossário, do termo mais longo para o mais curto.

    Substituir do maior para o menor evita que 'Critério' quebre 'Peso do critério'.
    Sem correspondência no glossário, o segmento fica em pt-BR — e o QA (--verificar)
    reporta, em vez de deixar passar como se estivesse traduzido.
    """
    if locale == ORIGEM:
        return texto_pt
    # 1) target de segmento aprovado (seção 5b) — sempre tem prioridade.
    if alvos_locale and tuid and alvos_locale.get(tuid):
        return alvos_locale[tuid]
    # 2) fallback: substituição terminológica pelo glossário (seção 3).
    resultado = texto_pt
    for termo in sorted(glossario, key=len, reverse=True):
        alvo = glossario[termo].get(locale)
        if not alvo or alvo == termo:
            continue
        padrao = re.compile(re.escape(termo), re.IGNORECASE)

        def _sub(m, alvo=alvo):
            orig = m.group(0)
            return alvo.capitalize() if orig[:1].isupper() and alvo[:1].islower() else alvo

        resultado = padrao.sub(_sub, resultado)
    return resultado


# ---------------------------------------------------------------------------
def gerar_strings():
    """Materializa translation/strings.<locale>.json a partir da TM."""
    glossario, direitos, unidades, alvos = carregar_tm()
    TM_DIR.mkdir(parents=True, exist_ok=True)
    gerados = []
    for locale, (curto, nome, direcao) in LOCALES.items():
        dados = {
            "_locale": locale,
            "_codigo": curto,
            "_idioma": nome,
            "_direcao": direcao,
            "_origem": ORIGEM,
            "_gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "_fonte": "translation.memory.md",
            "direitos": direitos.get(locale, direitos[ORIGEM]),
            "strings": {tuid: traduzir_unidade(txt, locale, glossario,
                                              alvos.get(locale), tuid)
                        for tuid, txt in unidades.items()},
            "glossario": {t: v.get(locale, t) for t, v in glossario.items()},
        }
        destino = TM_DIR / f"strings.{curto}.json"
        destino.write_text(
            json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding=ENCODING)
        gerados.append(destino)
    print(f"✅ {len(gerados)} arquivos de strings em {TM_DIR}")
    print(f"   {len(unidades)} unidades de tradução · {len(glossario)} termos de glossário")
    return gerados


# ---------------------------------------------------------------------------
def gerar_tmx():
    """Exporta a TM em TMX 1.4b — importável no SDL Trados Studio (.tmx -> .sdltm)."""
    glossario, direitos, unidades, alvos = carregar_tm()
    agora = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    partes = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<tmx version="1.4">',
              '  <header creationtool="MCDM Studio i18n Pipeline"',
              '          creationtoolversion="1.0.0"',
              '          segtype="sentence"',
              '          o-tmf="MCDM-TM"',
              '          adminlang="pt-BR"',
              '          srclang="pt-BR"',
              '          datatype="plaintext"',
              f'          creationdate="{agora}"',
              '          creationid="ProfBru - Bruno Penedo">',
              '    <prop type="x-project">multicriteriadecisionmodels</prop>',
              '    <prop type="x-domain">MCDA / Apoio Multicritério à Decisão</prop>',
              '    <prop type="x-copyright">ProfBru - Bruno Penedo © 2026 - '
              'TODOS OS DIREITOS RESERVADOS</prop>',
              '  </header>', '  <body>']

    def _tu(tuid, textos, tipo):
        linhas = [f'    <tu tuid="{escape(tuid)}" datatype="plaintext" '
                  f'creationdate="{agora}">',
                  f'      <prop type="x-type">{tipo}</prop>']
        for loc, txt in textos.items():
            linhas.append(f'      <tuv xml:lang="{loc}"><seg>{escape(txt)}</seg></tuv>')
        linhas.append("    </tu>")
        return linhas

    for tuid, txt in unidades.items():
        partes += _tu(tuid, {loc: traduzir_unidade(txt, loc, glossario, alvos.get(loc), tuid)
                             for loc in LOCALES}, "interface")
    for i, (termo, alvos) in enumerate(glossario.items(), 1):
        partes += _tu(f"term.{i:03d}", {loc: alvos.get(loc, termo) for loc in LOCALES},
                      "glossario")
    partes += _tu("rod.direitos.frase",
                  {loc: direitos.get(loc, direitos[ORIGEM]) for loc in LOCALES}, "copyright")
    partes += ["  </body>", "</tmx>", ""]

    TMX.write_text("\n".join(partes), encoding=ENCODING)
    n_tu = len(unidades) + len(glossario) + 1
    print(f"✅ TMX 1.4b exportado: {TMX}")
    print(f"   {n_tu} unidades de tradução × {len(LOCALES)} locales "
          f"= {n_tu * len(LOCALES):,} segmentos")
    return TMX


# ---------------------------------------------------------------------------
def _seletor_idiomas(atual_curto):
    """Linha de seleção de idioma: o idioma atual em negrito, os demais como link."""
    itens = []
    for _loc, (curto, nome, _d) in LOCALES.items():
        if curto == atual_curto:
            itens.append(f"**{nome}**")
        else:
            itens.append(f"[{nome}](/{'' if curto == 'pt' else curto})")
    return "🌐 " + " · ".join(itens)


def gerar_paginas():
    """Gera evidence/pages/<lang>/index.md nos 12 idiomas a partir do index.md em pt."""
    base = EVIDENCE_DIR / "pages" / "index.md"
    if not base.exists():
        raise FileNotFoundError(f"página base não encontrada: {base}")
    glossario, direitos, unidades, alvos = carregar_tm()
    texto_base = base.read_text(encoding=ENCODING)

    # Blocos ```sql ... ``` e tags de componente NÃO são traduzidos: protege-os
    # antes de qualquer substituição e restaura depois. É o mesmo princípio dos
    # placeables do Trados — o que é código não entra na memória de tradução.
    def _proteger(texto):
        guardados = []

        def _guardar(m):
            guardados.append(m.group(0))
            return f"\x00{len(guardados)-1}\x00"

        protegido = re.sub(r"```.*?```", _guardar, texto, flags=re.S)
        protegido = re.sub(r"<[A-Z][^>]*>", _guardar, protegido)
        return protegido, guardados

    def _restaurar(texto, guardados):
        return re.sub(r"\x00(\d+)\x00", lambda m: guardados[int(m.group(1))], texto)

    gerados = []
    for locale, (curto, nome, direcao) in LOCALES.items():
        protegido, guardados = _proteger(texto_base)
        traduzido = protegido if locale == ORIGEM else traduzir_unidade(
            protegido, locale, glossario)
        traduzido = _restaurar(traduzido, guardados)

        # Troca o seletor de idiomas pela versão desta página.
        traduzido = re.sub(r"^🌐 .*$", _seletor_idiomas(curto), traduzido,
                           count=1, flags=re.M)
        # Frase de direitos localizada.
        traduzido = traduzido.replace("TODOS OS DIREITOS RESERVADOS",
                                      direitos.get(locale, direitos[ORIGEM]))
        if direcao == "rtl":
            traduzido = traduzido.replace(
                "---\ntitle:", '---\ndir: rtl\ntitle:', 1)

        destino = (EVIDENCE_DIR / "pages" / "index.md" if curto == "pt"
                   else EVIDENCE_DIR / "pages" / curto / "index.md")
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(traduzido, encoding=ENCODING)
        gerados.append(destino)
    print(f"✅ {len(gerados)} páginas do dashboard em {EVIDENCE_DIR / 'pages'}")
    return gerados


# ---------------------------------------------------------------------------
def verificar():
    """QA equivalente ao Verify do Trados. Devolve a lista de problemas."""
    glossario, direitos, unidades, alvos = carregar_tm()
    problemas = []

    # 1. cobertura de locales no glossário e nos direitos
    for locale in LOCALES:
        faltando = [t for t, v in glossario.items() if not v.get(locale)]
        if faltando:
            problemas.append(
                f"[{locale}] {len(faltando)} termo(s) sem tradução no glossário: "
                f"{', '.join(faltando[:3])}{' ...' if len(faltando) > 3 else ''}")
        if locale not in direitos:
            problemas.append(f"[{locale}] frase de direitos ausente (seção 4 da TM)")

    # 2. não-traduzíveis preservados
    for locale in LOCALES:
        if locale == ORIGEM:
            continue
        # Siglas técnicas: cobradas em todo locale.
        # Nomes próprios: cobrados apenas onde a escrita é latina (ver acima).
        exigidos = SIGLAS_TECNICAS + (
            [] if locale in ESCRITA_NAO_LATINA else NOMES_PROPRIOS)
        for tuid, txt in unidades.items():
            alvo = traduzir_unidade(txt, locale, glossario, alvos.get(locale), tuid)
            for nt in exigidos:
                if nt in txt and nt not in alvo:
                    problemas.append(f"[{locale}] {tuid}: não-traduzível {nt!r} perdido")

    # 3. placeables: mesma contagem de crases e chaves
    for locale in LOCALES:
        for tuid, txt in unidades.items():
            alvo = traduzir_unidade(txt, locale, glossario, alvos.get(locale), tuid)
            for simbolo in ("`", "{", "}"):
                if txt.count(simbolo) != alvo.count(simbolo):
                    problemas.append(
                        f"[{locale}] {tuid}: contagem de {simbolo!r} mudou "
                        f"({txt.count(simbolo)} -> {alvo.count(simbolo)})")

    # 4. encoding e normalização NFC
    for arquivo in [TM_MD] + sorted(TM_DIR.glob("strings.*.json")):
        try:
            conteudo = arquivo.read_text(encoding="utf-8")
        except UnicodeDecodeError as erro:
            problemas.append(f"{arquivo.name}: não é UTF-8 válido ({erro})")
            continue
        if unicodedata.normalize("NFC", conteudo) != conteudo:
            problemas.append(f"{arquivo.name}: não está normalizado em NFC")
        if conteudo.startswith("﻿"):
            problemas.append(f"{arquivo.name}: contém BOM (deve ser UTF-8 sem BOM)")
        if "\r\n" in conteudo:
            problemas.append(f"{arquivo.name}: contém CRLF (deve ser LF)")

    # 5. cobertura de targets de segmento (seção 5b da TM)
    for locale in LOCALES:
        if locale == ORIGEM:
            continue
        sem_alvo = [t for t in unidades if not alvos.get(locale, {}).get(t)]
        if sem_alvo:
            problemas.append(
                f"[{locale}] {len(sem_alvo)} tuid(s) sem target de segmento "
                f"(caem no glossário): {', '.join(sem_alvo[:3])}"
                f"{' ...' if len(sem_alvo) > 3 else ''}")

    # 6. segmentos vazios
    for tuid, txt in unidades.items():
        if not txt.strip():
            problemas.append(f"{tuid}: segmento de origem vazio")

    print("QA de tradução — equivalente ao Verify do SDL Trados Studio")
    print("=" * 74)
    print(f"  locales           : {len(LOCALES)}")
    print(f"  unidades (TU)     : {len(unidades)}")
    print(f"  termos glossário  : {len(glossario)}")
    print(f"  segmentos totais  : {(len(unidades) + len(glossario)) * len(LOCALES):,}")
    print("=" * 74)
    if problemas:
        print(f"⚠️  {len(problemas)} problema(s):")
        for p in problemas[:30]:
            print(f"   • {p}")
        if len(problemas) > 30:
            print(f"   ... e mais {len(problemas) - 30}")
    else:
        print("✅ nenhum problema: consistência, placeables, encoding e cobertura OK.")
    return problemas


def main():
    ap = argparse.ArgumentParser(description="Pipeline i18n do MCDM Studio (TM -> artefatos).")
    ap.add_argument("--tm", action="store_true", help="gera strings.<locale>.json")
    ap.add_argument("--paginas", action="store_true", help="gera as páginas do dashboard")
    ap.add_argument("--tmx", action="store_true", help="exporta TMX para o Trados")
    ap.add_argument("--verificar", action="store_true", help="QA das traduções")
    ap.add_argument("--tudo", action="store_true", help="tudo acima, em ordem")
    args = ap.parse_args()
    if not any(vars(args).values()):
        ap.print_help()
        return 0

    if args.tudo or args.tm:
        gerar_strings()
    if args.tudo or args.tmx:
        gerar_tmx()
    if args.tudo or args.paginas:
        gerar_paginas()
    if args.tudo or args.verificar:
        return 1 if verificar() else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
