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

🌐 [Português](/casos/{params.caso}) · [English](/en/casos/{params.caso}) · [Español](/es/casos/{params.caso}) · [Français](/fr/casos/{params.caso}) · [Deutsch](/de/casos/{params.caso}) · **中文** · [한국어](/ko/casos/{params.caso}) · [हिन्दी](/hi/casos/{params.caso}) · [עברית](/he/casos/{params.caso}) · [Русский](/ru/casos/{params.caso}) · [Svenska](/sv/casos/{params.caso}) · [Suomi](/fi/casos/{params.caso})

# {caso[0].nome}

> **{caso[0].descricao}**
>
> _所建模的决策者：{caso[0].decisor} · 领域：{caso[0].dominio}_

<BigValue data={caso} value=vencedor_rotulo title="🏆 共识优胜方案"/>
<BigValue data={caso} value=prob_vitoria title="在（%的宇宙中）获胜" fmt=num1/>
<BigValue data={caso} value=classificacao title="结论"/>
<BigValue data={caso} value=n_alternativas title="备选方案" fmt=num0/>
<BigValue data={caso} value=n_metodos title="产生排序的方法" fmt=num0/>
<BigValue data={caso} value=n_modelos title="已应用模型" fmt=num0/>

---

## 🧮 DEMATEL — 哪些准则是原因，哪些是结果

> Antes de qualquer peso: **os 准则s não são independentes**. O DEMATEL monta a matriz de relação total `T = X(I−X)⁻¹` — somando influência direta **e indireta** de qualquer comprimento de caminho — e separa o que você pode **puxar** (CAUSA) do que apenas **mede o resultado** (EFEITO). Os pesos saem daí, por influência sistêmica.

<img src="/mc/{params.caso}/dematel_原因_结果.png" alt="Diagrama 原因-结果 DEMATEL" style="width:100%;border-radius:8px;"/>

<DataTable data={dematel_c} rows=all rowShading=true>
  <Column id=rotulo title="准则"/>
  <Column id=unidade title="单位"/>
  <Column id=direcao title="方向"/>
  <Column id=influencia_exercida title="R（施加的影响）" fmt=num3/>
  <Column id=influencia_recebida title="C（受到的影响）" fmt=num3/>
  <Column id=prominencia title="显著度（R+C）" fmt=num3 contentType=colorscale/>
  <Column id=relacao title="关系（R−C）" fmt=num3 contentType=colorscale/>
  <Column id=papel title="角色"/>
  <Column id=peso title="导出权重" fmt=pct2/>
</DataTable>

<BarChart data={dematel_c} x=rotulo y=relacao title="DEMATEL 因果图 (R−C)：零以上为原因" yAxisTitle="R − C" sort=false>
  <ReferenceLine y=0 color=info label="fronteira causa / efeito"/>
</BarChart>

### Matriz de relação total — quem influencia quem

> A tabela acima resume cada 准则 em dois números. **Esta matriz mostra as ligações uma a uma**: `T = X(I − X)⁻¹` soma os caminhos diretos **e indiretos** de qualquer comprimento, e por isso revela influências que o especialista nunca declarou diretamente — A influencia B, B influencia C, logo A influencia C, e a matriz total contabiliza isso.
>
> Só aparecem as arestas **acima do limiar α** (a média de T). Abaixo dele, a intensidade é indistinguível de ruído de arredondamento, e um diagrama que desenhasse todas as ligações não informaria nada — toda matriz densa parece igualmente conectada.

<DataTable data={relacao_c} rows=12 rowShading=true>
  <Column id=origem_rotulo title="来源（施加影响）"/>
  <Column id=origem_papel title="来源的角色"/>
  <Column id=destino_rotulo title="目标（被影响）"/>
  <Column id=destino_papel title="目标的角色"/>
  <Column id=intensidade title="强度 tᵢⱼ" fmt=num4 contentType=colorscale/>
</DataTable>

<BarChart data={relacao_c} x=origem_rotulo y=intensidade series=destino_rotulo type=stacked title="各准则施加的总影响，按目标分解" yAxisTitle="Intensidade acumulada" swapXY=true/>

### Quatro famílias de peso sobre o mesmo problema

> O **AHP** pergunta, par a par, quanto um 准则 importa mais que outro. O **DEMATEL** mede influência sistêmica. **Onde divergem está o 结果 de segunda ordem subestimado.**
>
> O **AHP Fuzzy** (Buckley, 1985) recebe o mesmo julgamento do AHP, mas não descarta a imprecisão: quem disse "5" quis dizer algo entre 4 e 6, e essa faixa é carregada até o fim. As colunas `l` e `u` são os limites do número triangular de cada peso.
>
> O **BWM** (Rezaei, 2015) resolve um problema operacional, não teórico: a matriz de Saaty com 9 准则s exige 36 comparações e **ninguém a preenche com atenção até o fim**. O BWM pede apenas o melhor e o pior 准则 e deriva o resto — 2n−3 comparações. A coluna `BWM CR` diz se o julgamento resultante é consistente.

<img src="/mc/{params.caso}/pesos_dematel_ahp.png" alt="DEMATEL, AHP e AHP Fuzzy" style="width:100%;border-radius:8px;"/>

<DataTable data={pesos_c} rows=all rowShading=true>
  <Column id=rotulo title="准则"/>
  <Column id=papel title="角色"/>
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

> [!NOTE] O AHP Fuzzy **achata os extremos** em relação ao AHP crisp: a média geométrica com incerteza puxa os pesos para o centro. Um 准则 que o AHP coloca em 50% costuma cair, e um que ele deixa em 0,4% costuma subir. Isso não é correção de erro, é o que acontece quando se admite que o julgamento tinha uma faixa. Se a ORDEM dos pesos muda entre os dois, a prioridade declarada não sobrevive à imprecisão do próprio decisor, e isso é informação para o comitê.

---

## ⚖️ 同一个问题上的十大决策学派

> [!IMPORTANT] **本案例应用了十二个模型，其中十个进入此图。** **BWM** 给出的是准则权重（见上方四个权重族的表格），**DRSA** 给出的是规则（下方有独立章节）——两者都不产生备选方案的名次，因此**博尔达共识与稳健性分析是在这十个之上计算的**。在此处把十二个都算进来，会让人误以为共识汇总了它并未汇总的东西。

> 每种方法都是**关于“更好”含义的不同理论**。当这十种一致时，该选择不是方法的产物。**当它们分歧时，分歧本身就是发现**——而且通常恰好指出真正的权衡在哪里。
>
> **模糊 TOPSIS**（Chen, 2000）值得单独一读：它不是“加了噪声的 AHP-TOPSIS”。除三角模糊数之外，它还更换了标准化方式（线性而非向量）与理想解（绝对而非相对）。与 AHP-TOPSIS 2n 产生分歧是**预期**行为，它度量的是排序对这些选择的依赖程度。

<img src="/mc/{params.caso}/mapa_metodos.png" alt="排名 por escola de decisão" style="width:100%;border-radius:8px;"/>

<BarChart data={metodos_c} x=rotulo y=rank_ series=metodo type=grouped title="各决策学派下的排名（第1名最佳）" yAxisTitle="Posição" swapXY=true/>

### ELECTRE I — 核（kernel）

> 排序之前先**淘汰**：核是没有任何其他备选能够超越的集合。单元素的核直接了结决策；核过大则说明准则没有区分力——问题出在建模，而不在计算。

<DataTable data={nucleo_c} rows=12 rowShading=true>
  <Column id=rotulo title="备选方案"/>
  <Column id=no_nucleo title="在核内？" fmt=boolean/>
  <Column id=domina title="超越" fmt=num0/>
  <Column id=dominada title="被超越于" fmt=num0/>
</DataTable>

### AHP-TOPSIS 2N — 双重标准化

> TOPSIS **对所选的标准化方式敏感**。我们两种都跑（向量与极差），并报告二者的一致性：**稳健？**这一列是方法论上的诚实。

<DataTable data={topsis_c} rows=12 rowShading=true>
  <Column id=rank_final title="#"/>
  <Column id=rotulo title="备选方案"/>
  <Column id=ci_vector title="Ci 向量" fmt=num4/>
  <Column id=ci_minmax title="Ci 极差" fmt=num4/>
  <Column id=ci_final title="Ci 最终" fmt=num4 contentType=colorscale/>
  <Column id=concordante title="是否稳健？" fmt=boolean/>
</DataTable>

---

## 🤝 波达共识

<DataTable data={consenso_c} rows=all rowShading=true>
  <Column id=rank_final title="#" contentType=colorscale/>
  <Column id=rotulo title="备选方案"/>
  <Column id=borda title="博尔达得分" fmt=num0/>
  <Column id=rank_medio title="平均排名" fmt=num2/>
  <Column id=unanime title="是否一致？" fmt=boolean/>
  <Column id=prob_vitoria title="获胜比例（%）" fmt=num1 contentType=colorscale/>
  <Column id=rank_p95 title="最差情形 (p95)" fmt=num0/>
</DataTable>

---

## 🎯 稳健性 — 决策自身的置信区间

> **问题所在。** 权重从不精确——它们是偏好的估计。如果两个百分点就让第一与第二互换，那么这个“优胜方案”是校准的产物。
>
> **解法。** 我们以 `w' ~ Dirichlet(κ·w)` 扰动并重新排序 **2000 次**。狄利克雷分布的支撑集恰好是单纯形，且满足 `E[w'] = w`——我们在扰动时**不引入偏倚**。

<BigValue data={robustez_top} value=rotulo title="扰动权重下的领先者"/>
<BigValue data={robustez_top} value=prob_vitoria title="获胜比例（%）" fmt=num1/>
<BigValue data={robustez_top} value=rank_p95 title="最差的合理名次" fmt=num0/>

<img src="/mc/{params.caso}/稳健性.png" alt="稳健性 sob pesos perturbados" style="width:100%;border-radius:8px;"/>

<DataTable data={robustez_c} rows=15 rowShading=true>
  <Column id=rotulo title="备选方案"/>
  <Column id=prob_vitoria title="赢得共识（%）" fmt=num1 contentType=colorscale/>
  <Column id=prob_top3 title="Top-3 (%)" fmt=num1/>
  <Column id=rank_medio title="典型排名" fmt=num2/>
  <Column id=rank_p05 title="最佳情形 (p05)" fmt=num0/>
  <Column id=rank_p95 title="最差情形 (p95)" fmt=num0/>
</DataTable>

### 名次的完整分布

> 整条全绿的条形表示该名次**不依赖于权重**。有杂色的条形则是存在争议的名次。

<img src="/mc/{params.caso}/distribuicao_posicoes.png" alt="Distribuição das posições" style="width:100%;border-radius:8px;"/>

---

## 🎲 Matriz BCG — que 信息技术PO de aposta é cada 备选方案

> O consenso responde **qual escolher**. A BCG responde **que tipo de aposta cada uma é** — pergunta diferente, e igualmente decisiva na hora de assinar.
>
> Dois eixos, ambos derivados dos **mesmos pesos do DEMATEL** que alimentam os dez métodos (renormalizados por grupo, de modo que a BCG é um segundo corte da mesma modelagem, não uma segunda modelagem):
>
> - **吸引力** (Y) — desempenho ponderado nos 准则s de **效益** - **成本位置** (X) — quanto entrega por unidade de **sacrifício**
>
> Os cortes são as **medianas** de cada eixo, não o ponto médio: mediana divide o conjunto em duas metades reais, enquanto 0,5 deixaria quadrantes vazios num conjunto assimétrico — e quadrante vazio não informa nada.

<BigValue data={bcg_res_c} value=estrelas title="⭐ 明星" fmt=num0/>
<BigValue data={bcg_res_c} value=vacas title="🐄 金牛" fmt=num0/>
<BigValue data={bcg_res_c} value=interrogacoes title="❓ 问号" fmt=num0/>
<BigValue data={bcg_res_c} value=abacaxis title="🐕 瘦狗" fmt=num0/>

<img src="/mc/{params.caso}/matriz_bcg.png" alt="Matriz BCG" style="width:100%;border-radius:8px;"/>

| 象限 | Leitura de decisão |
|---|---|
| ⭐ **Estrela** | Alta atratividade **e** boa posição de 成本 — a aposta natural: investir e padronizar. |
| 🐄 **Vaca leiteira** | Entrega o essencial pelo **menor sacrifício**. É a escolha de quem tem orçamento apertado. |
| ❓ **Interrogação** | Desempenho alto a **preço alto**. Só se justifica se o prêmio for necessário. |
| 🐕 **Abacaxi** | Nem entrega, nem é barata. **Descartar.** |

> **O cruzamento é onde mora o achado.** Um 2º colocado que é 🐄 Vaca costuma ser a escolha real de quem tem restrição orçamentária; um 2º colocado ❓ Interrogação só compensa se você precisa do prêmio de desempenho que ele cobra.

<DataTable data={bcg_c} rows=15 rowShading=true>
  <Column id=rank_consenso title="#" contentType=colorscale/>
  <Column id=rotulo title="备选方案"/>
  <Column id=quadrante_rotulo title="象限"/>
  <Column id=atratividade title="吸引力" fmt=num3 contentType=colorscale/>
  <Column id=posicao title="成本位置" fmt=num3 contentType=colorscale/>
  <Column id=acao title="该怎么做"/>
</DataTable>

---

## 📏 DRSA — 解释过往决策的规则

> 其余十一个模型要求**事先声明**偏好：权重、比较、阈值。**DRSA**（Greco、Matarazzo 与 Słowiński）反其道而行——它接收已经做出的决策，并返回解释这些决策的**规则**，用平实的语言写成，面向不知道什么是向量标准化的人。它是这里唯一一个从历史中学习、而不要求有人说得出自己偏好什么的家族。

<div class="grid grid-cols-3 gap-4">
<BigValue data={drsa_q} value=gamma title="γ — 近似质量" fmt=pct1/>
<BigValue data={drsa_q} value=n_regras title="归纳出的规则" fmt=num0/>
<BigValue data={drsa_q} value=n_violacoes title="违反占优关系的对" fmt=num0/>
</div>

<DataTable data={drsa_r} rows=all rowShading=true>
  <Column id=n_regra title="#"/>
  <Column id=texto title="规则"/>
  <Column id=cobertura title="覆盖" fmt=num0/>
  <Column id=certeza title="确定度" fmt=pct0/>
</DataTable>

> [!NOTE] **γ = 100%** 表示占优关系毫无歧义地对所有备选作了分类：历史是自洽的，规则完整地描述了它。**γ < 100%** 是诊断而非缺陷——它说明存在若干对，其中被占优的备选反而被选中，而*违反占优关系的对数*一列给出了具体数量。此时过往决策存在例外，知道这一点比一个干净的排序更有价值。

---

## 📐 决策矩阵

> Os dados de entrada. **Substitua pela sua cotação, seu edital ou seu ensaio** — o motor é o mesmo; os dados é que são seus.

<DataTable data={matriz_c} rows=25 rowShading=true search=true>
  <Column id=alternativa_rotulo title="备选方案"/>
  <Column id=criterio_rotulo title="准则"/>
  <Column id=direcao title="方向"/>
  <Column id=valor title="数值" fmt=num2/>
  <Column id=unidade title="单位"/>
</DataTable>

<LinkButton url='/zh'>← Voltar ao índice de casos</LinkButton>

---

<div style="text-align:center;margin-top:2rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="120" style="display:inline-block;opacity:0.9;"/>
  <div style="font-weight:700;margin-top:0.4rem;">ProfBru © 2026</div>
  <div style="margin-top:0.5rem;font-style:italic;font-size:0.9rem;color:#64748b;">
    MCDM Studio — Modelos Multi准则 de Decisão<br/>
    Autor: <strong>ProfBru - Bruno Penedo</strong> © 2026 — 保留所有权利<br/>
    profbruanbima@gmail.com
  </div>
</div>
