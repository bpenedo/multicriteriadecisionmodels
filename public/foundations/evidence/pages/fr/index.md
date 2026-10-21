---
title: MCDM Studio — Decisão MultiCritère
---

<div style="text-align:center;">

🌐 [Português](/) · [English](/en) · [Español](/es) · **Français** · [Deutsch](/de) · [中文](/zh) · [한국어](/ko) · [हिन्दी](/hi) · [עברית](/he) · [Русский](/ru) · [Svenska](/sv) · [Suomi](/fi)

<div style="text-align:center;margin:1.2rem 0 1.6rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="200" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.5rem;font-size:1.05rem;">ProfBru © 2026</div>
</div>

_MCDM Studio — Modelos MultiCritère de Decisão · Autor: **ProfBru - Bruno Penedo** © 2026 — TOUS DROITS RÉSERVÉS · profbruanbima@gmail.com_

</div>

<!--
  ÍNDICE LEVE, DE PROPÓSITO.
  Só consultas AGREGADAS (uma linha por caso). As tabelas detalhadas — ranking por
  método (3.744 linhas), Matrice de décision (3.514), distribuição (4.230), Robustesse por
  método (4.160) — vivem nas páginas de caso, onde estão filtradas por `id_caso`.
  Carregá-las todas aqui somava ~16 mil linhas e travava o navegador.
-->

```sql casos
select *, '/casos/' || id_caso as link from mcdm.casos
```
```sql bcg_geral
select * from mcdm.bcg_resumo
```
```sql totais
select
  (select count(*) from mcdm.casos)                                 as casos,
  (select count(*) from mcdm.consenso)                              as alternativas,
  (select count(*) from mcdm.casos where classificacao = 'ROBUSTO') as robustos,
  (select count(*) from mcdm.casos where classificacao = 'FRÁGIL')  as frageis
```
```sql alavancas
select * from mcdm.dematel_alavancas
```
```sql resumo_dominio
select dominio, count(*) as casos, avg(prob_vitoria) as confianca_media
from mcdm.casos group by dominio order by casos desc
```

# 🎯 Décision Multicritère — dix écoles, un verdict avec intervalle de confiance

> **Le tableur ne se trompe pas dans le calcul. Il se trompe de question.** Trier par prix élit le moins cher. Trier par note d'expert élit le plus cher. Filtrer sur « répond à toutes les exigences » vide généralement la liste. Aucune des trois ne répond à la question posée : *parmi des alternatives qui se contredisent, laquelle choisir — et avec quelle confiance ?*

Ce tableau de bord exécute **dix méthodes multicritères** sur chaque cas, tire le gagnant du **consensus de Borda** entre elles, puis **perturbe les poids 2 000 fois** pour répondre à la seule question que le comité pose vraiment : *et si nous avions donné un poids un peu différent ?*

<BigValue data={totais} value=casos title="Cas de décision" fmt=num0/>
<BigValue data={totais} value=alternativas title="Alternatives évaluées" fmt=num0/>
<BigValue data={totais} value=robustos title="Verdicts ROBUSTES" fmt=num0/>
<BigValue data={totais} value=frageis title="Verdicts FRAGILES" fmt=num0/>

## 📋 Cas de décision

> Cliquez sur n'importe quel cas pour ouvrir le **rapport complet** : diagramme cause-effet du DEMATEL, carte des dix écoles, noyau de l'ELECTRE, double normalisation du TOPSIS, consensus de Borda, robustesse sur 2 000 univers, matrice BCG et la matrice de décision.

<DataTable data={casos} rows=all rowShading=true link=link>
  <Column id=nome title="Cas"/>
  <Column id=dominio title="Domaine"/>
  <Column id=n_alternativas title="Alternatives" fmt=num0/>
  <Column id=vencedor_rotulo title="🏆 Gagnant"/>
  <Column id=prob_vitoria title="Confiance (%)" fmt=num1 contentType=colorscale/>
  <Column id=classificacao title="Verdict"/>
</DataTable>

> **Comment lire le Verdict.** `ROBUSTE` (≥ 90 %) = le choix ne dépend pas du calibrage fin des poids ; il peut aller au comité. `PROBABLE` (60–90 %) = il tient dans la plupart des scénarios, mais le second est compétitif. `FRAGILE` (sous 60 %) = **la 1re place est un artefact des poids** — le système le dit au lieu d'exhiber un trophée.

<BarChart data={resumo_dominio} x=dominio y=casos title="Cas par domaine d'application" yAxisTitle="Casos"/>

## 🧮 DEMATEL — la cause racine de chaque décision

> La question que presque personne ne pose avant d'attribuer des poids : **les critères sont-ils indépendants ?** Ils ne le sont presque jamais. La consommation d'énergie *cause* l'autonomie ; le blindage *cause* le poids, qui *cause* une perte de mobilité. Additionner les deux comme indépendants compte deux fois la même chose.
>
> Le **DEMATEL** (Gabus & Fontela, Battelle) construit la matrice de relation totale `T = X(I−X)⁻¹` — qui somme les influences directes **et indirectes** de toute longueur de chemin — et sépare : `R+C` = importance dans le système ; `R−C > 0` = **CAUSE** (levier : agissez ici) et `R−C < 0` = **EFFET** (thermomètre : résultat de ce qui a déjà été fait).
>
> La colonne **Cause racine** ci-dessous est le critère de plus grand `R−C` de chaque cas : c'est là qu'une intervention déplace le système entier.

<DataTable data={alavancas} rows=all rowShading=true>
  <Column id=nome title="Cas"/>
  <Column id=n_criterios title="Critères" fmt=num0/>
  <Column id=n_causas title="Causes" fmt=num0 contentType=colorscale/>
  <Column id=causa_raiz title="🔧 Cause racine (plus grand R−C)"/>
  <Column id=criterio_maior_peso title="Critère de plus grand poids"/>
  <Column id=maior_peso_pct title="Poids (%)" fmt=num1/>
</DataTable>

<BarChart data={alavancas} x=nome y={['n_causas','n_criterios']} type=grouped title="Critères qui sont CAUSE dans chaque cas (leviers sur le total)" yAxisTitle="Critérios" swapXY=true/>

> **Ouvrez un cas** pour voir le diagramme cause-effet complet, le tableau avec `R` et `C` séparés et la **matrice de relation totale** avec les liens un à un.

## 🎲 Matrice BCG — carte des opportunités par catégorie

> Au-delà de *laquelle choisir*, chaque catégorie a un **profil d'opportunité** : combien d'alternatives sont ⭐ Étoile (investir), 🐄 Vache (récolter), ❓ Dilemme (évaluer le gain) et 🐕 Poids mort (abandonner). Une catégorie faite uniquement de dilemmes est un marché cher ; une pleine de vaches est un marché mûr, où l'argent décide peu.

<DataTable data={bcg_geral} rows=all rowShading=true>
  <Column id=nome title="Catégorie"/>
  <Column id=estrelas title="⭐" fmt=num0 contentType=colorscale/>
  <Column id=vacas title="🐄" fmt=num0 contentType=colorscale/>
  <Column id=interrogacoes title="❓" fmt=num0 contentType=colorscale/>
  <Column id=abacaxis title="🐕" fmt=num0 contentType=colorscale/>
  <Column id=total title="Total" fmt=num0/>
  <Column id=quadrante_do_vencedor title="Quadrant de la 1re place"/>
</DataTable>

## ⚖️ Les dix écoles de décision

> Chaque méthode est une **théorie différente de ce que « meilleur » signifie**, et c'est pourquoi nous les exécutons toutes : quand dix écoles indépendantes élisent le même gagnant, le choix n'est pas un artefact d'une méthode. Quand elles divergent, la divergence indique où se trouve le vrai compromis.

| Método | Escola | O que assume | Quando é a ferramenta certa |
|---|---|---|---|
| **AHP-TOPSIS 2n** | Distância à solução ideal | Compensação total entre Critères | Critères quantitativos, decisor único |
| **ELECTRE I** | Surclassement | Incomparabilidade é permitida | Triagem: eliminar o que é dominado |
| **ELECTRE II** | Surclassement | Limiares forte e fraco | Ordenação completa com veto |
| **PROMETHEE II** | Surclassement | Preferência gradual (6 funções) | Quando "um pouco melhor" não é "melhor" |
| **MAUT** | Utilidade | Independência aditiva + Aversion au risque | Decisão sob incerteza |
| **MCDA-C** | Construtivista | Níveis Neutro/Bom ancorados | Diagnóstico absoluto, não só ranking |
| **VIKOR** | Compromisso | Utilidade do grupo × arrependimento máximo | Quando compensar é inaceitável |
| **TODIM** | Teoria dos Prospectos | Perda dói mais que ganho equivalente | Decisor avesso a perda (todos são) |
| **SAPEVO-M** | Ordinal multidecisor | Julgamento ordinal de vários decisores | Comitê que não concorda entre si |

## 🎯 Robustesse — l'intervalle de confiance de la décision elle-même

> **Le problème.** Toute méthode MCDM renvoie un gagnant avec une confiance implicite de 100 %. Mais les poids ne sont jamais exacts — ce sont des estimations de préférence. Si deux points de pourcentage dans le poids d'un critère échangent la 1re et la 2e place, le « gagnant » est un artefact du calibrage, non un fait de l'ensemble. Personne ne le rapporte. **C'est là que les décisions meurent en comité.**
>
> **La solution.** Nous perturbons les poids avec `w' ~ Dirichlet(κ·w)` et reclassons 2 000 fois. La Dirichlet est le choix naturel : son support est exactement le simplexe (poids positifs de somme 1) et elle satisfait `E[w'] = w` — nous perturbons **sans biaiser**. Avec κ = 200, un poids de 13 % oscille de ±2,4 pts.
>
> Le verdict cesse d'être *« le Modèle C est le meilleur »* et devient **« le Modèle C gagne dans 96 % des univers de préférence plausibles »**.

**Ouvrez un cas du tableau ci-dessus** pour voir le diagramme cause-effet, la carte des dix écoles, la matrice BCG et la distribution complète des positions sur les 2 000 univers.

---

<div style="text-align:center;margin-top:2rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="120" style="display:inline-block;opacity:0.9;"/>
  <div style="font-weight:700;margin-top:0.4rem;">ProfBru © 2026</div>
  <div style="margin-top:0.5rem;font-style:italic;font-size:0.9rem;color:#64748b;">
    MCDM Studio — Modelos MultiCritère de Decisão<br/>
    Autor: <strong>ProfBru - Bruno Penedo</strong> © 2026 — TOUS DROITS RÉSERVÉS<br/>
    profbruanbima@gmail.com
  </div>
</div>
