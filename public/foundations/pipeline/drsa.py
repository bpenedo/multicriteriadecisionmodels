"""
DRSA — Dominance-based Rough Set Approach (Greco, Matarazzo & Słowiński).

═══════════════════════════════════════════════════════════════════════════════
 O QUE ELE FAZ DE DIFERENTE DE TODO O RESTO DESTE PROJETO
═══════════════════════════════════════════════════════════════════════════════
Os dez métodos de ranqueamento exigem que o decisor DECLARE preferências antes:
pesos, limiares, funções de preferência, aversão a risco. O DRSA inverte: recebe
DECISÕES JÁ TOMADAS — exemplos classificados — e deduz as regras que as explicam.

O que ele devolve não é um score, é uma frase:

    SE maturidade ≥ 15 E time ≥ 8,2  ENTÃO classe ≥ ALTA   (cobre 7, certeza 100%)

Isso muda a conversa no comitê. Um ranking diz *quem* ganhou; uma regra diz *por
quê*, numa forma que alguém pode contestar com um contraexemplo.

E há um diagnóstico que nenhum outro método do projeto dá: a **qualidade da
aproximação γ**. Se γ < 1, existem pares de alternativas em que uma domina a outra
em todos os critérios e mesmo assim foi classificada igual ou pior. Isso é
**inconsistência nos próprios dados** — ou falta um critério que o decisor usou e
não declarou, ou a classificação tem erro. Nenhum método compensatório acusa isso:
eles calculam um score e seguem.

═══════════════════════════════════════════════════════════════════════════════
 COMO ESTE PROJETO O USA — declarado
═══════════════════════════════════════════════════════════════════════════════
O DRSA pede exemplos de decisões passadas. Aqui não há histórico de decisões do
comitê: o que existe é o CONSENSO DE BORDA já calculado. Então o usamos como
camada de EXPLICAÇÃO — discretizamos o consenso em classes ordenadas e induzimos
as regras que o reproduzem.

Isso responde "que condições nos critérios levam uma alternativa ao topo?" — e
**não** "o que o comitê decidiria". Com histórico real de decisões, passe as
classes observadas em `classes` e o método vira o que de fato é: aprendizado a
partir do que foi decidido.

REFERÊNCIAS
    GRECO, S.; MATARAZZO, B.; SŁOWIŃSKI, R. "Rough approximation of a preference
        relation by dominance relations". EJOR, 117(1):63-83, 1999.
    GRECO, S.; MATARAZZO, B.; SŁOWIŃSKI, R. "Rough sets theory for multicriteria
        decision analysis". EJOR, 129(1):1-47, 2001.
    GRECO, S.; MATARAZZO, B.; SŁOWIŃSKI, R.; STEFANOWSKI, J. "An algorithm for
        induction of decision rules consistent with the dominance principle"
        (DOMLEM). RSCTC 2000, LNCS 2005, p. 304-313.

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import numpy as np

from nucleo import orientar


def discretizar_classes(score, n_classes=3):
    """Score contínuo → classes ORDENADAS 1..n_classes (1 = pior, n = melhor).

    Corta por quantis, não por amplitude: com um outlier, o corte por amplitude
    põe quase tudo numa classe só e as regras induzidas ficam triviais
    ("se nada, então classe 1"). O corte por quantil mantém as classes povoadas.

    Empates na fronteira ficam na classe SUPERIOR — escolha declarada: na dúvida,
    a alternativa recebe o benefício, e a regra que a cobre fica mais exigente,
    não mais frouxa.
    """
    score = np.asarray(score, dtype=np.float64).ravel()
    if score.size == 0:
        raise ValueError("score vazio")
    if n_classes < 2:
        raise ValueError(f"n_classes deve ser ≥ 2, recebido {n_classes}")
    cortes = np.quantile(score, np.linspace(0, 1, n_classes + 1)[1:-1])
    return np.searchsorted(cortes, score, side="right") + 1


def dominancia(G):
    """Matriz booleana D onde D[a, b] = "a domina b em TODOS os critérios".

    `G` já vem de `orientar`: tudo em [0,1] com maior = melhor. A dominância é
    sobre os critérios ORIENTADOS — sem isso, um critério de custo inverteria o
    sentido e a dominância diria o oposto do que significa.
    """
    G = np.asarray(G, dtype=np.float64)
    if G.ndim != 2:
        raise ValueError(f"G deve ser 2-D, recebida {G.shape}")
    return (G[:, None, :] >= G[None, :, :] - 1e-12).all(axis=2)


def aproximacoes(G, classes, t):
    """Aproximações inferior e superior da união ascendente Cl≥t.

    Devolve `(inferior, superior, fronteira)` como máscaras booleanas.

        P̲(Cl≥t) = { x : D⁺(x) ⊆ Cl≥t }   — quem tem CERTEZA de pertencer:
                                             tudo que domina x também é ≥ t
        P̄(Cl≥t) = { x : D⁻(x) ∩ Cl≥t ≠ ∅ } — quem POSSIVELMENTE pertence:
                                             x domina alguém que é ≥ t

    A fronteira P̄ − P̲ é a parte ambígua, e seu tamanho é o diagnóstico: contém
    exatamente as alternativas envolvidas em violação do princípio de dominância.
    """
    D = dominancia(G)
    classes = np.asarray(classes).ravel()
    m = len(classes)
    if D.shape != (m, m):
        raise ValueError(f"classes ({m}) não batem com G ({D.shape[0]} alternativas)")
    pertence = classes >= t
    inferior = np.zeros(m, dtype=bool)
    superior = np.zeros(m, dtype=bool)
    for x in range(m):
        dom_x = D[:, x]                      # quem domina x (inclui o próprio x)
        por_x = D[x, :]                      # quem x domina
        inferior[x] = bool(np.all(pertence[dom_x]))
        superior[x] = bool(np.any(pertence[por_x]))
    return inferior, superior, superior & ~inferior


def qualidade_aproximacao(G, classes):
    """γ — fração das alternativas que NÃO estão em nenhuma fronteira.

    γ = 1 significa que a classificação respeita integralmente o princípio de
    dominância: nunca uma alternativa pior em tudo foi classificada melhor.

    γ < 1 é um achado sobre os DADOS, não sobre o método. Devolve também os pares
    que violam, porque "γ = 0,87" não aciona ninguém — "a alternativa 12 domina a
    5 em todos os critérios e ficou numa classe inferior" aciona.
    """
    classes = np.asarray(classes).ravel()
    m = len(classes)
    ambiguas = np.zeros(m, dtype=bool)
    for t in range(int(classes.min()) + 1, int(classes.max()) + 1):
        _inf, _sup, fron = aproximacoes(G, classes, t)
        ambiguas |= fron
    D = dominancia(G)
    violacoes = [(a, b) for a in range(m) for b in range(m)
                 if a != b and D[a, b] and not D[b, a] and classes[a] < classes[b]]
    gamma = float((~ambiguas).sum() / m) if m else 1.0
    return gamma, ambiguas, violacoes


def induzir_regras(X, direcoes, classes, rotulos=None, min_cobertura=1):
    """Regras certas "SE … ENTÃO classe ≥ t", a partir da aproximação INFERIOR.

    Estratégia (DOMLEM simplificado): para cada união ascendente Cl≥t, parte-se
    do objeto da aproximação inferior e procura-se o menor conjunto de condições
    `f_j(x) ≥ v_j` que cobre objetos de Cl≥t **sem cobrir nenhum objeto fora**.

    Só induzimos regras CERTAS (da aproximação inferior). Regras possíveis, da
    aproximação superior, descrevem o que *pode* acontecer — num sistema de apoio
    à decisão elas seriam lidas como recomendação, e não são.

    Os limiares saem dos VALORES OBSERVADOS, nunca de pontos médios inventados:
    uma regra "preço ≥ 2.437,50" não corresponde a nenhuma alternativa real e não
    pode ser verificada contra os dados.
    """
    X = np.asarray(X, dtype=np.float64)
    classes = np.asarray(classes).ravel()
    m, k = X.shape
    if len(classes) != m:
        raise ValueError(f"classes ({len(classes)}) ≠ alternativas ({m})")
    if len(direcoes) != k:
        raise ValueError(f"direções ({len(direcoes)}) ≠ critérios ({k})")
    if rotulos is None:
        rotulos = [f"c{j}" for j in range(k)]
    G = orientar(X, direcoes)

    regras = []
    for t in range(int(classes.min()) + 1, int(classes.max()) + 1):
        inferior, _sup, _fr = aproximacoes(G, classes, t)
        alvo = classes >= t
        restantes = set(np.flatnonzero(inferior))
        while restantes:
            # Semente = o objeto MAIS FRACO ainda não coberto, não o mais forte.
            # Partindo do mais forte, a primeira regra sai restritíssima ("nota ≥ 9")
            # e as seguintes, mais frouxas, acabam cobrindo-a — o conjunto fica
            # redundante. Começando pelo mais fraco, a regra nasce no limiar mais
            # baixo que ainda é puro, e já cobre todos os melhores de uma vez.
            semente = min(restantes, key=lambda i: G[i].sum())
            cond, usados = {}, set()
            cobertos = np.ones(m, dtype=bool)
            # Adiciona a condição que mais exclui objeto FORA do alvo, até a
            # cobertura ficar pura. Guloso, como o DOMLEM.
            while (cobertos & ~alvo).any() and len(usados) < k:
                melhor_j, melhor_falsos = None, None
                for j in range(k):
                    if j in usados:
                        continue
                    novo = cobertos & (G[:, j] >= G[semente, j] - 1e-12)
                    falsos = int((novo & ~alvo).sum())
                    if not novo[semente]:
                        continue
                    if melhor_falsos is None or falsos < melhor_falsos:
                        melhor_j, melhor_falsos = j, falsos
                if melhor_j is None:
                    break
                usados.add(melhor_j)
                cond[melhor_j] = float(X[semente, melhor_j])
                cobertos = cobertos & (G[:, melhor_j] >= G[semente, melhor_j] - 1e-12)
            if not cond or (cobertos & ~alvo).any():
                restantes.discard(semente)
                continue
            n_cob = int(cobertos.sum())
            if n_cob >= min_cobertura:
                regras.append({
                    "classe_min": int(t),
                    "condicoes": [(rotulos[j], direcoes[j], v) for j, v in cond.items()],
                    "cobertura": n_cob,
                    "suporte": [int(i) for i in np.flatnonzero(cobertos)],
                    "certeza": 1.0,
                })
            restantes -= set(np.flatnonzero(cobertos))
    return _remover_subsumidas(regras)


def _remover_subsumidas(regras):
    """Descarta regra cujo suporte já está contido no de outra da MESMA classe.

    Mesmo partindo do objeto mais fraco, critérios diferentes podem gerar duas
    regras em que uma cobre tudo o que a outra cobre. Regra redundante não está
    errada — está sobrando, e um conjunto de regras que o comitê não consegue ler
    inteiro não cumpre a função do DRSA, que é justamente ser legível.
    """
    mantidas = []
    for r in sorted(regras, key=lambda x: (-x["cobertura"], len(x["condicoes"]))):
        sup = set(r["suporte"])
        if any(r["classe_min"] == m["classe_min"] and sup <= set(m["suporte"])
               for m in mantidas):
            continue
        mantidas.append(r)
    return sorted(mantidas, key=lambda x: (-x["classe_min"], -x["cobertura"]))


def texto_regra(regra, nomes_alt=None):
    """Regra → frase em português, legível por quem não conhece o método."""
    partes = [f"{rot} {'≥' if d == 'benefit' else '≤'} {v:g}"
              for rot, d, v in regra["condicoes"]]
    frase = ("SE " + " E ".join(partes) +
             f" ENTÃO classe ≥ {regra['classe_min']}")
    return f"{frase}  (cobre {regra['cobertura']}, certeza {regra['certeza']:.0%})"


if __name__ == "__main__":
    print("DRSA — Dominance-based Rough Set Approach")
    print("  Greco, Matarazzo & Słowiński (1999, 2001); DOMLEM (2000)")
    print("  Aprende REGRAS a partir de decisões classificadas,")
    print("  em vez de exigir pesos e limiares declarados antes.")
