"""
Catálogo de casos de decisão do MCDM Studio.

Reúne os casos DEMONSTRATIVOS (`catalogo.py`, 6 casos de modelagem) e os
ESTUDOS DE CASO de produtos (`produtos.py`, 9 casos, 282 alternativas).

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
from casos.catalogo import CATALOGO as _BASE, validar          # noqa: F401
from casos.produtos import CATALOGO_PRODUTOS as _PRODUTOS      # noqa: F401
from casos.producao import CATALOGO_PRODUCAO as _PRODUCAO      # noqa: F401
from casos.estudos_kb import CATALOGO_ESTUDOS_KB as _ESTUDOS    # noqa: F401

# Um caso de `produtos.py` com o mesmo id sobrepõe o demonstrativo — nenhum
# colide hoje, e a ordem deixa explícita a precedência caso venha a colidir.
CATALOGO = {**_BASE, **_PRODUTOS, **_PRODUCAO, **_ESTUDOS}


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
