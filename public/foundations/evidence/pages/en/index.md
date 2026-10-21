---
title: MCDM Studio — Decisão MultiCriterion
---

<div style="text-align:center;">

🌐 [Português](/) · **English** · [Español](/es/) · [Français](/fr/) · [Deutsch](/de/) · [中文](/zh/) · [한국어](/ko/) · [हिन्दी](/hi/) · [עברית](/he/) · [Русский](/ru/) · [Svenska](/sv/) · [Suomi](/fi/)

<div style="text-align:center;margin:1.2rem 0 1.6rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="200" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.5rem;font-size:1.05rem;">ProfBru © 2026</div>
</div>

_MCDM Studio — Modelos MultiCriterion de Decisão · Autor: **ProfBru - Bruno Penedo** © 2026 — ALL RIGHTS RESERVED · profbruanbima@gmail.com_

</div>

<!--
  ÍNDICE LEVE, DE PROPÓSITO.
  Só consultas AGREGADAS (uma linha por caso). As tabelas detalhadas — ranking por
  método (3.744 linhas), Decision matrix (3.514), distribuição (4.230), Robustness por
  método (4.160) — vivem nas páginas de caso, onde estão filtradas por `id_caso`.
  Carregá-las todas aqui somava ~16 mil linhas e travava o navegador.
-->

```sql casos
select *, '/en/casos/' || id_caso as link from mcdm.casos
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

# 🎯 Multi-Criteria Decision — ten schools, one verdict with a confidence interval

> **The spreadsheet does not get the arithmetic wrong. It gets the question wrong.** Sorting by price elects the cheapest. Sorting by expert score elects the most expensive. Filtering by "meets all requirements" usually empties the list. None of the three answers the question that was asked: *among alternatives that contradict each other, which to choose — and with what confidence?*

This dashboard runs **ten multi-criteria methods** on every case, draws the winner from the **Borda consensus** among them, and then **perturbs the weights 2,000 times** to answer the one question the committee really asks: *what if we had set a slightly different weight?*

<BigValue data={totais} value=casos title="Decision cases" fmt=num0/>
<BigValue data={totais} value=alternativas title="Alternatives assessed" fmt=num0/>
<BigValue data={totais} value=robustos title="ROBUST verdicts" fmt=num0/>
<BigValue data={totais} value=frageis title="FRAGILE verdicts" fmt=num0/>

## 📋 Decision cases

> Click any case to open the **full report**: DEMATEL cause-effect diagram, map of the ten schools, the ELECTRE core, the TOPSIS double normalization, Borda consensus, robustness across 2,000 universes, BCG matrix and the decision matrix.

<DataTable data={casos} rows=all rowShading=true link=link>
  <Column id=nome title="Case"/>
  <Column id=dominio title="Domain"/>
  <Column id=n_alternativas title="Alternatives" fmt=num0/>
  <Column id=vencedor_rotulo title="🏆 Winner"/>
  <Column id=prob_vitoria title="Confidence (%)" fmt=num1 contentType=colorscale/>
  <Column id=classificacao title="Verdict"/>
</DataTable>

> **How to read the Verdict.** `ROBUST` (≥ 90%) = the choice does not depend on fine calibration of the weights; it can go to the committee. `LIKELY` (60–90%) = it holds in most scenarios, but the runner-up is competitive. `FRAGILE` (below 60%) = **first place is an artefact of the weights** — the system says so instead of displaying a trophy.

<BarChart data={resumo_dominio} x=dominio y=casos title="Cases by application domain" yAxisTitle="Casos"/>

## 🧮 DEMATEL — the root cause of every decision

> The question almost nobody asks before assigning weights: **are the criteria independent?** They almost never are. Energy consumption *causes* range; armour *causes* weight, which *causes* loss of mobility. Adding the two as independent counts the same thing twice.
>
> **DEMATEL** (Gabus & Fontela, Battelle) builds the total relation matrix `T = X(I−X)⁻¹` — which sums direct **and indirect** influences of any path length — and separates: `R+C` = importance in the system; `R−C > 0` = **CAUSE** (lever: act here) and `R−C < 0` = **EFFECT** (thermometer: the result of what has already been done).
>
> The **Root cause** column below is the criterion with the highest `R−C` in each case: it is there that one intervention moves the whole system.

<DataTable data={alavancas} rows=all rowShading=true>
  <Column id=nome title="Case"/>
  <Column id=n_criterios title="Criteria" fmt=num0/>
  <Column id=n_causas title="Causes" fmt=num0 contentType=colorscale/>
  <Column id=causa_raiz title="🔧 Root cause (highest R−C)"/>
  <Column id=criterio_maior_peso title="Highest-weight criterion"/>
  <Column id=maior_peso_pct title="Weight (%)" fmt=num1/>
</DataTable>

<BarChart data={alavancas} x=nome y={['n_causas','n_criterios']} type=grouped title="Criteria that are a CAUSE in each case (levers against the total)" yAxisTitle="Critérios" swapXY=true/>

> **Open a case** to see the full cause-effect diagram, the table with `R` and `C` separated, and the **total relation matrix** with the links one by one.

## 🎲 BCG matrix — a map of opportunity by category

> Beyond *which one to pick*, each category has an **opportunity profile**: how many alternatives are ⭐ Star (invest), 🐄 Cow (harvest), ❓ Question mark (weigh the prize) and 🐕 Dog (drop). A category made only of question marks is an expensive market; one full of cows is a mature market, where money decides little.

<DataTable data={bcg_geral} rows=all rowShading=true>
  <Column id=nome title="Category"/>
  <Column id=estrelas title="⭐" fmt=num0 contentType=colorscale/>
  <Column id=vacas title="🐄" fmt=num0 contentType=colorscale/>
  <Column id=interrogacoes title="❓" fmt=num0 contentType=colorscale/>
  <Column id=abacaxis title="🐕" fmt=num0 contentType=colorscale/>
  <Column id=total title="Total" fmt=num0/>
  <Column id=quadrante_do_vencedor title="Quadrant of the 1st place"/>
</DataTable>

## ⚖️ The ten schools of decision

> Each method is a **different theory of what "best" means**, and that is why we run them all: when ten independent schools elect the same winner, the choice is not an artefact of one method. When they diverge, the divergence points to where the real trade-off is.

| Método | Escola | O que assume | Quando é a ferramenta certa |
|---|---|---|---|
| **AHP-TOPSIS 2n** | Distância à solução ideal | Compensação total entre Criterions | Criteria quantitativos, decisor único |
| **ELECTRE I** | Outranksção | Incomparabilidade é permitida | Triagem: eliminar o que é dominado |
| **ELECTRE II** | Outranksção | Limiares forte e fraco | Ordenação completa com veto |
| **PROMETHEE II** | Outranksção | Preferência gradual (6 funções) | Quando "um pouco melhor" não é "melhor" |
| **MAUT** | Utilidade | Independência aditiva + Risk aversion | Decisão sob incerteza |
| **MCDA-C** | Construtivista | Níveis Neutro/Bom ancorados | Diagnóstico absoluto, não só ranking |
| **VIKOR** | Compromisso | Utilidade do grupo × arrependimento máximo | Quando compensar é inaceitável |
| **TODIM** | Teoria dos Prospectos | Perda dói mais que ganho equivalente | Decisor avesso a perda (todos são) |
| **SAPEVO-M** | Ordinal multidecisor | Julgamento ordinal de vários decisores | Comitê que não concorda entre si |

## 🎯 Robustness — the confidence interval of the decision itself

> **The problem.** Every MCDM method returns a winner with an implicit confidence of 100%. But weights are never exact — they are preference estimates. If two percentage points in one criterion's weight swap first and second place, the "winner" is an artefact of the calibration, not a fact about the set. Nobody reports this. **It is where decisions die in committee.**
>
> **The solution.** We perturb the weights with `w' ~ Dirichlet(κ·w)` and re-rank 2,000 times. The Dirichlet is the natural choice: its support is exactly the simplex (positive weights summing to 1) and it satisfies `E[w'] = w` — we perturb **without biasing**. With κ = 200, a weight of 13% swings ±2.4 p.p.
>
> The verdict stops being *"Model C is the best"* and becomes **"Model C wins in 96% of plausible preference universes"**.

**Open a case from the table above** to see the cause-effect diagram, the map of the ten schools, the BCG matrix and the full distribution of positions across the 2,000 universes.

---

<div style="text-align:center;margin-top:2rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="120" style="display:inline-block;opacity:0.9;"/>
  <div style="font-weight:700;margin-top:0.4rem;">ProfBru © 2026</div>
  <div style="margin-top:0.5rem;font-style:italic;font-size:0.9rem;color:#64748b;">
    MCDM Studio — Modelos MultiCriterion de Decisão<br/>
    Autor: <strong>ProfBru - Bruno Penedo</strong> © 2026 — ALL RIGHTS RESERVED<br/>
    profbruanbima@gmail.com
  </div>
</div>
