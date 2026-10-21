---
title: "{params.caso}"
---

```sql caso
select * from mcdm.casos where id_caso = '${params.caso}'
```
```sql dematel_c
select * from mcdm.dematel where id_caso = '${params.caso}' order by prominencia desc
```
```sql relacao_c
-- Arestas do diagrama de influência: só as que superam o limiar α (média de T).
select * from mcdm.dematel_relacao
where id_caso = '${params.caso}' and acima_limiar = 1
order by intensidade desc limit 20
```
```sql relacao_todas_c
select * from mcdm.dematel_relacao where id_caso = '${params.caso}'
order by intensidade desc
```
```sql pesos_c
select * from mcdm.pesos_comparados where id_caso = '${params.caso}'
```
```sql consenso_c
select * from mcdm.consenso where id_caso = '${params.caso}'
order by rank_final limit 20
```
```sql robustez_c
select * from mcdm.robustez where id_caso = '${params.caso}'
order by prob_vitoria desc limit 20
```
```sql robustez_top
select * from mcdm.robustez where id_caso = '${params.caso}' order by prob_vitoria desc limit 1
```
```sql metodos_c
-- Apenas as 10 primeiras do consenso × 10 métodos = 100 linhas. Trazer as 38
-- alternativas daria 342 e o gráfico agrupado ficaria ilegível de qualquer forma.
select r.* from mcdm.ranking_metodos r
join mcdm.consenso c on c.id_caso = r.id_caso and c.alternativa = r.alternativa
where r.id_caso = '${params.caso}' and c.rank_final <= 10
```
```sql topsis_c
select * from mcdm.topsis where id_caso = '${params.caso}' order by rank_final limit 15
```
```sql nucleo_c
select * from mcdm.electre_nucleo where id_caso = '${params.caso}'
order by no_nucleo desc, domina desc limit 15
```
```sql matriz_c
-- Matriz de decisão das 10 primeiras colocadas. A tabela tem busca; para ver todas
-- as alternativas de um caso grande, consulte o banco diretamente.
select m.* from mcdm.matriz_decisao m
join mcdm.consenso c on c.id_caso = m.id_caso and c.alternativa = m.alternativa
where m.id_caso = '${params.caso}' and c.rank_final <= 10
```
```sql dist_c
select d.* from mcdm.distribuicao d
join mcdm.consenso c on c.id_caso = d.id_caso and c.alternativa = d.alternativa
where d.id_caso = '${params.caso}' and c.rank_final <= 10
```
```sql bcg_c
select * from mcdm.bcg where id_caso = '${params.caso}' order by rank_consenso limit 20
```
```sql bcg_res_c
select * from mcdm.bcg_resumo where id_caso = '${params.caso}'
```

```sql drsa_q
select * from mcdm.drsa_qualidade where id_caso = '${params.caso}'
```

```sql drsa_r
select * from mcdm.drsa_regras where id_caso = '${params.caso}'
```

<div style="text-align:center;margin:1rem 0 1.4rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="150" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.45rem;">ProfBru © 2026</div>
</div>

🌐 [Português](/casos/{params.caso}) · **English** · [Español](/es/casos/{params.caso}) · [Français](/fr/casos/{params.caso}) · [Deutsch](/de/casos/{params.caso}) · [中文](/zh/casos/{params.caso}) · [한국어](/ko/casos/{params.caso}) · [हिन्दी](/hi/casos/{params.caso}) · [עברית](/he/casos/{params.caso}) · [Русский](/ru/casos/{params.caso}) · [Svenska](/sv/casos/{params.caso}) · [Suomi](/fi/casos/{params.caso})

# {caso[0].nome}

> **{caso[0].descricao}**
>
> _Decision maker modelled: {caso[0].decisor} · Domain: {caso[0].dominio}_

<BigValue data={caso} value=vencedor_rotulo title="🏆 Winner of the consensus"/>
<BigValue data={caso} value=prob_vitoria title="Wins in (% of universes)" fmt=num1/>
<BigValue data={caso} value=classificacao title="Verdict"/>
<BigValue data={caso} value=n_alternativas title="Alternatives" fmt=num0/>
<BigValue data={caso} value=n_metodos title="Methods that rank" fmt=num0/>
<BigValue data={caso} value=n_modelos title="Models applied" fmt=num0/>

---

## 🧮 DEMATEL — which criteria are causes and which are effects

> Antes de qualquer peso: **os Criterions não são independentes**. O DEMATEL monta a matriz de relação total `T = X(I−X)⁻¹` — somando influência direta **e indireta** de qualquer comprimento de caminho — e separa o que você pode **puxar** (CAUSA) do que apenas **mede o resultado** (EFEITO). Os pesos saem daí, por influência sistêmica.

<img src="/mc/{params.caso}/dematel_cause_effect.png" alt="Diagrama cause-effect DEMATEL" style="width:100%;border-radius:8px;"/>

<DataTable data={dematel_c} rows=all rowShading=true>
  <Column id=rotulo title="Criterion"/>
  <Column id=unidade title="Unit"/>
  <Column id=direcao title="Direction"/>
  <Column id=influencia_exercida title="R (influence exerted)" fmt=num3/>
  <Column id=influencia_recebida title="C (influence received)" fmt=num3/>
  <Column id=prominencia title="Prominence (R+C)" fmt=num3 contentType=colorscale/>
  <Column id=relacao title="Relation (R−C)" fmt=num3 contentType=colorscale/>
  <Column id=papel title="Role"/>
  <Column id=peso title="Derived weight" fmt=pct2/>
</DataTable>

<BarChart data={dematel_c} x=rotulo y=relacao title="DEMATEL cause–effect diagram (R−C): above zero = CAUSE" yAxisTitle="R − C" sort=false>
  <ReferenceLine y=0 color=info label="fronteira causa / efeito"/>
</BarChart>

### Matriz de relação total — quem influencia quem

> A tabela acima resume cada Criterion em dois números. **Esta matriz mostra as ligações uma a uma**: `T = X(I − X)⁻¹` soma os caminhos diretos **e indiretos** de qualquer comprimento, e por isso revela influências que o especialista nunca declarou diretamente — A influencia B, B influencia C, logo A influencia C, e a matriz total contabiliza isso.
>
> Só aparecem as arestas **acima do limiar α** (a média de T). Abaixo dele, a intensidade é indistinguível de ruído de arredondamento, e um diagrama que desenhasse todas as ligações não informaria nada — toda matriz densa parece igualmente conectada.

<DataTable data={relacao_c} rows=12 rowShading=true>
  <Column id=origem_rotulo title="Source (influences)"/>
  <Column id=origem_papel title="Role of the source"/>
  <Column id=destino_rotulo title="Target (is influenced)"/>
  <Column id=destino_papel title="Role of the target"/>
  <Column id=intensidade title="Intensity tᵢⱼ" fmt=num4 contentType=colorscale/>
</DataTable>

<BarChart data={relacao_c} x=origem_rotulo y=intensidade series=destino_rotulo type=stacked title="Total influence exerted by each criterion, broken down by target" yAxisTitle="Intensidade acumulada" swapXY=true/>

### Quatro famílias de peso sobre o mesmo problema

> O **AHP** pergunta, par a par, quanto um Criterion importa mais que outro. O **DEMATEL** mede influência sistêmica. **Onde divergem está o effect de segunda ordem subestimado.**
>
> O **AHP Fuzzy** (Buckley, 1985) recebe o mesmo julgamento do AHP, mas não descarta a imprecisão: quem disse "5" quis dizer algo entre 4 e 6, e essa faixa é carregada até o fim. As colunas `l` e `u` são os limites do número triangular de cada peso.
>
> O **BWM** (Rezaei, 2015) resolve um problema operacional, não teórico: a matriz de Saaty com 9 Criterions exige 36 comparações e **ninguém a preenche com atenção até o fim**. O BWM pede apenas o melhor e o pior Criterion e deriva o resto — 2n−3 comparações. A coluna `BWM CR` diz se o julgamento resultante é consistente.

<img src="/mc/{params.caso}/pesos_dematel_ahp.png" alt="DEMATEL, AHP e AHP Fuzzy" style="width:100%;border-radius:8px;"/>

<DataTable data={pesos_c} rows=all rowShading=true>
  <Column id=rotulo title="Criterion"/>
  <Column id=papel title="Role"/>
  <Column id=peso_dematel title="DEMATEL" fmt=pct2/>
  <Column id=peso_ahp title="AHP" fmt=pct2/>
  <Column id=peso_ahp_fuzzy title="AHP Fuzzy" fmt=pct2/>
  <Column id=fuzzy_l title="l" fmt=pct2/>
  <Column id=fuzzy_u title="u" fmt=pct2/>
  <Column id=peso_bwm title="BWM" fmt=pct2/>
  <Column id=divergencia title="DEMATEL - AHP" fmt=pct2 contentType=colorscale/>
  <Column id=cr title="AHP CR" fmt=num4/>
  <Column id=bwm_cr title="BWM CR" fmt=num4/>
</DataTable>

> [!NOTE] O AHP Fuzzy **achata os extremos** em relação ao AHP crisp: a média geométrica com incerteza puxa os pesos para o centro. Um Criterion que o AHP coloca em 50% costuma cair, e um que ele deixa em 0,4% costuma subir. Isso não é correção de erro, é o que acontece quando se admite que o julgamento tinha uma faixa. Se a ORDEM dos pesos muda entre os dois, a prioridade declarada não sobrevive à imprecisão do próprio decisor, e isso é informação para o comitê.

---

## ⚖️ Ten schools of decision on the same problem

> [!IMPORTANT] **Twelve models are applied to this case, and ten enter this chart.** **BWM** returns criterion weights (see the table of the four families, above) and **DRSA** returns rules (its own section, further down) — neither produces a position for an alternative, and that is why the **Borda consensus and the robustness analysis are computed over these ten**. Counting all twelve here would suggest the consensus aggregates what it does not.

> Each method is a **different theory of what “best” means**. When the ten agree, the choice is not an artefact of method. **When they diverge, the divergence is the finding** — and it usually points exactly to where the real trade-off lies.
>
> **Fuzzy TOPSIS** (Chen, 2000) deserves separate reading: it is not “AHP-TOPSIS with noise”. Besides the triangular numbers, it swaps the normalization (linear instead of vectorial) and the ideal solution (absolute instead of relative). Diverging from AHP-TOPSIS 2n is the **expected** behaviour, and it measures how much the ranking depends on those choices.

<img src="/mc/{params.caso}/mapa_metodos.png" alt="Position por escola de decisão" style="width:100%;border-radius:8px;"/>

<BarChart data={metodos_c} x=rotulo y=rank_ series=metodo type=grouped title="Position by school of decision (1st = best)" yAxisTitle="Posição" swapXY=true/>

### ELECTRE I — the kernel

> Before ranking, **eliminate**: the kernel is the set that no other alternative outranks. A single-element kernel settles the decision; a kernel that is too large means the criteria are not discriminating — and the problem is one of modelling, not of calculation.

<DataTable data={nucleo_c} rows=12 rowShading=true>
  <Column id=rotulo title="Alternative"/>
  <Column id=no_nucleo title="In the kernel?" fmt=boolean/>
  <Column id=domina title="Outranks" fmt=num0/>
  <Column id=dominada title="Is outranked by" fmt=num0/>
</DataTable>

### AHP-TOPSIS 2N — the double normalization

> TOPSIS is **sensitive to the chosen normalization**. We run both (vectorial and min-max) and report the agreement: the **Robust?** column is methodological honesty.

<DataTable data={topsis_c} rows=12 rowShading=true>
  <Column id=rank_final title="#"/>
  <Column id=rotulo title="Alternative"/>
  <Column id=ci_vector title="Ci vectorial" fmt=num4/>
  <Column id=ci_minmax title="Ci min-max" fmt=num4/>
  <Column id=ci_final title="Ci final" fmt=num4 contentType=colorscale/>
  <Column id=concordante title="Robust?" fmt=boolean/>
</DataTable>

---

## 🤝 Borda consensus

<DataTable data={consenso_c} rows=all rowShading=true>
  <Column id=rank_final title="#" contentType=colorscale/>
  <Column id=rotulo title="Alternative"/>
  <Column id=borda title="Borda points" fmt=num0/>
  <Column id=rank_medio title="Average position" fmt=num2/>
  <Column id=unanime title="Unanimous?" fmt=boolean/>
  <Column id=prob_vitoria title="Wins in (%)" fmt=num1 contentType=colorscale/>
  <Column id=rank_p95 title="Worst case (p95)" fmt=num0/>
</DataTable>

---

## 🎯 Robustness — the confidence interval of the decision itself

> **The problem.** Weights are never exact — they are preference estimates. If two percentage points swap first and second place, the “winner” is an artefact of the calibration.
>
> **The solution.** We perturb with `w' ~ Dirichlet(κ·w)` and re-rank **2,000 times**. The Dirichlet has support exactly on the simplex and satisfies `E[w'] = w` — we perturb **without biasing**.

<BigValue data={robustez_top} value=rotulo title="Leader under perturbed weights"/>
<BigValue data={robustez_top} value=prob_vitoria title="Wins in (%)" fmt=num1/>
<BigValue data={robustez_top} value=rank_p95 title="Worst plausible position" fmt=num0/>

<img src="/mc/{params.caso}/Robustness.png" alt="Robustness sob pesos perturbados" style="width:100%;border-radius:8px;"/>

<DataTable data={robustez_c} rows=15 rowShading=true>
  <Column id=rotulo title="Alternative"/>
  <Column id=prob_vitoria title="Wins the consensus (%)" fmt=num1 contentType=colorscale/>
  <Column id=prob_top3 title="Top-3 (%)" fmt=num1/>
  <Column id=rank_medio title="Typical position" fmt=num2/>
  <Column id=rank_p05 title="Best case (p05)" fmt=num0/>
  <Column id=rank_p95 title="Worst case (p95)" fmt=num0/>
</DataTable>

### Full distribution of positions

> A fully green bar is a position that **does not depend on the weights**. A mottled bar is a position under dispute.

<img src="/mc/{params.caso}/distribuicao_posicoes.png" alt="Distribuição das posições" style="width:100%;border-radius:8px;"/>

---

## 🎲 Matriz BCG — que ITPO de aposta é cada Alternative

> O consenso responde **qual escolher**. A BCG responde **que tipo de aposta cada uma é** — pergunta diferente, e igualmente decisiva na hora de assinar.
>
> Dois eixos, ambos derivados dos **mesmos pesos do DEMATEL** que alimentam os dez métodos (renormalizados por grupo, de modo que a BCG é um segundo corte da mesma modelagem, não uma segunda modelagem):
>
> - **Attractiveness** (Y) — desempenho ponderado nos Criterions de **benefit** - **Cost position** (X) — quanto entrega por unidade de **sacrifício**
>
> Os cortes são as **medianas** de cada eixo, não o ponto médio: mediana divide o conjunto em duas metades reais, enquanto 0,5 deixaria quadrantes vazios num conjunto assimétrico — e quadrante vazio não informa nada.

<BigValue data={bcg_res_c} value=estrelas title="⭐ Stars" fmt=num0/>
<BigValue data={bcg_res_c} value=vacas title="🐄 Cash cows" fmt=num0/>
<BigValue data={bcg_res_c} value=interrogacoes title="❓ Question marks" fmt=num0/>
<BigValue data={bcg_res_c} value=abacaxis title="🐕 Dogs" fmt=num0/>

<img src="/mc/{params.caso}/matriz_bcg.png" alt="Matriz BCG" style="width:100%;border-radius:8px;"/>

| Quadrant | Leitura de decisão |
|---|---|
| ⭐ **Estrela** | Alta atratividade **e** boa posição de cost — a aposta natural: investir e padronizar. |
| 🐄 **Vaca leiteira** | Entrega o essencial pelo **menor sacrifício**. É a escolha de quem tem orçamento apertado. |
| ❓ **Interrogação** | Desempenho alto a **preço alto**. Só se justifica se o prêmio for necessário. |
| 🐕 **Abacaxi** | Nem entrega, nem é barata. **Descartar.** |

> **O cruzamento é onde mora o achado.** Um 2º colocado que é 🐄 Vaca costuma ser a escolha real de quem tem restrição orçamentária; um 2º colocado ❓ Interrogação só compensa se você precisa do prêmio de desempenho que ele cobra.

<DataTable data={bcg_c} rows=15 rowShading=true>
  <Column id=rank_consenso title="#" contentType=colorscale/>
  <Column id=rotulo title="Alternative"/>
  <Column id=quadrante_rotulo title="Quadrant"/>
  <Column id=atratividade title="Attractiveness" fmt=num3 contentType=colorscale/>
  <Column id=posicao title="Cost position" fmt=num3 contentType=colorscale/>
  <Column id=acao title="What to do"/>
</DataTable>

---

## 📏 DRSA — the rule that explains past decisions

> The other eleven models ask for **declared** preferences: weights, comparisons, thresholds. **DRSA** (Greco, Matarazzo & Słowiński) goes the other way — it takes decisions already made and returns the **rule** that explains them, in plain language, for someone who does not know what vectorial normalization is. It is the only family here that learns from history instead of requiring someone to state what they prefer.

<div class="grid grid-cols-3 gap-4">
<BigValue data={drsa_q} value=gamma title="γ — quality of the approximation" fmt=pct1/>
<BigValue data={drsa_q} value=n_regras title="Rules induced" fmt=num0/>
<BigValue data={drsa_q} value=n_violacoes title="Pairs violating dominance" fmt=num0/>
</div>

<DataTable data={drsa_r} rows=all rowShading=true>
  <Column id=n_regra title="#"/>
  <Column id=texto title="Rule"/>
  <Column id=cobertura title="Covers" fmt=num0/>
  <Column id=certeza title="Certainty" fmt=pct0/>
</DataTable>

> [!NOTE] **γ = 100%** means the dominance relation classifies every alternative without ambiguity: the history is coherent and the rules describe it entirely. **γ < 100%** is diagnostic, not a defect — it says there are pairs in which the dominated alternative was preferred, and the *Pairs violating dominance* column counts how many. In that case the past decision has exceptions, and knowing it is worth more than a clean ranking.

---

## 📐 Decision matrix

> Os dados de entrada. **Substitua pela sua cotação, seu edital ou seu ensaio** — o motor é o mesmo; os dados é que são seus.

<DataTable data={matriz_c} rows=25 rowShading=true search=true>
  <Column id=alternativa_rotulo title="Alternative"/>
  <Column id=criterio_rotulo title="Criterion"/>
  <Column id=direcao title="Direction"/>
  <Column id=valor title="Value" fmt=num2/>
  <Column id=unidade title="Unit"/>
</DataTable>

<LinkButton url='/en'>← Voltar ao índice de casos</LinkButton>

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
