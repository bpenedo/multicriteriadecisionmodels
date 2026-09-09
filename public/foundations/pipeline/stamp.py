"""
STAMP de autoria — carimbo único, multilíngue (linguagens de programação).

Fonte canônica: _private/foundations/stamp.md
Este módulo é a ÚNICA definição do carimbo no código. Todo arquivo do projeto
importa daqui (ou usa `python3 stamp.py <linguagem>`) em vez de repetir texto —
assim uma correção de autoria se propaga sem varredura manual.

Uso:
    python3 stamp.py bash | md | python | fsharp | rust | ruby | zig | sql | js | c
    python3 stamp.py --todos          # imprime todas as variantes

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import sys

PROJETO = "MCDM Studio — Modelos Multicritério de Decisão"
AUTOR = "ProfBru - Bruno Penedo"
ANO = "2026"
DIREITOS = "TODOS OS DIREITOS RESERVADOS"
EMAIL = "profbruanbima@gmail.com"

# Linhas puras do carimbo, sem sintaxe de comentário.
LINHAS = (
    PROJETO,
    f"Autor: {AUTOR} © {ANO} - {DIREITOS}",
    f"E-mail: {EMAIL}",
)

# Sintaxe de comentário por linguagem: (prefixo_linha, abertura_bloco, fechamento_bloco)
SINTAXE = {
    "bash":   ("# ", None, None),
    "python": ("# ", None, None),
    "ruby":   ("# ", None, None),
    "yaml":   ("# ", None, None),
    "r":      ("# ", None, None),
    "julia":  ("# ", None, None),
    "sql":    ("-- ", None, None),
    "haskell": ("-- ", None, None),
    "lua":    ("-- ", None, None),
    "fsharp": ("// ", "(*", "*)"),
    "rust":   ("// ", None, None),
    "zig":    ("// ", None, None),
    "js":     ("// ", "/*", "*/"),
    "ts":     ("// ", "/*", "*/"),
    "go":     ("// ", None, None),
    "c":      ("// ", "/*", "*/"),
    "java":   ("// ", "/*", "*/"),
    "md":     (None, "<!--", "-->"),
    "html":   (None, "<!--", "-->"),
    "tex":    ("% ", None, None),
}

ALIASES = {
    "sh": "bash", "py": "python", "rb": "ruby", "fs": "fsharp", "f#": "fsharp",
    "rs": "rust", "markdown": "md", "javascript": "js", "typescript": "ts",
    "yml": "yaml", "latex": "tex", "cpp": "c", "c++": "c",
}


def carimbo(linguagem: str = "python", bloco: bool = False) -> str:
    """Devolve o carimbo formatado como comentário da linguagem pedida.

    bloco=True usa a sintaxe de comentário de bloco quando a linguagem tiver uma
    (útil em F#, JS e C, onde o bloco é a convenção de cabeçalho de arquivo).
    """
    chave = ALIASES.get(linguagem.lower(), linguagem.lower())
    if chave not in SINTAXE:
        raise ValueError(
            f"linguagem desconhecida: {linguagem!r}. "
            f"Disponíveis: {', '.join(sorted(SINTAXE))}"
        )
    prefixo, abre, fecha = SINTAXE[chave]

    # Markdown/HTML só têm comentário de bloco — força o modo bloco.
    if prefixo is None or (bloco and abre):
        corpo = "\n".join(LINHAS)
        return f"{abre}\n{corpo}\n{fecha}"
    return "\n".join(prefixo + linha for linha in LINHAS)


def markdown_visivel() -> str:
    """Carimbo VISÍVEL para rodapé de README (não é comentário)."""
    return (
        f"**{PROJETO}**  \n"
        f"Autor: **{AUTOR}** © {ANO} — {DIREITOS}  \n"
        f"E-mail: {EMAIL}"
    )


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        print("Linguagens:", ", ".join(sorted(SINTAXE)))
        return 0
    if args[0] == "--todos":
        for chave in sorted(SINTAXE):
            print(f"----- {chave} -----")
            print(carimbo(chave))
            print()
        return 0
    try:
        print(carimbo(args[0], bloco="--bloco" in args))
    except ValueError as erro:
        print(f"❌ {erro}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
