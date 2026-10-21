---
title: MCDM Studio — Decisão Multi准则
---

<div style="text-align:center;">

🌐 [Português](/) · [English](/en) · [Español](/es) · [Français](/fr) · [Deutsch](/de) · **中文** · [한국어](/ko) · [हिन्दी](/hi) · [עברית](/he) · [Русский](/ru) · [Svenska](/sv) · [Suomi](/fi)

<div style="text-align:center;margin:1.2rem 0 1.6rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="200" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.5rem;font-size:1.05rem;">ProfBru © 2026</div>
</div>

_MCDM Studio — Modelos Multi准则 de Decisão · Autor: **ProfBru - Bruno Penedo** © 2026 — 保留所有权利 · profbruanbima@gmail.com_

</div>

<!--
  ÍNDICE LEVE, DE PROPÓSITO.
  Só consultas AGREGADAS (uma linha por caso). As tabelas detalhadas — ranking por
  método (3.744 linhas), 决策矩阵 (3.514), distribuição (4.230), 稳健性 por
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

# 🎯 多准则决策 — 十大学派，一个带置信区间的结论

> **电子表格算得没错，错的是它问的问题。** 按价格排序选出最便宜的。按专家评分排序选出最贵的。按“满足全部要求”筛选往往把清单清空。这三种都没有回答真正被提出的问题：*在互相矛盾的备选之间，该选哪一个——又有多大的确信？*

本面板对每个案例运行**十种多准则方法**，从它们之间的**博尔达共识**中得出优胜方案，然后**对权重扰动 2000 次**，以回答委员会真正会问的那一个问题：*如果当初给的权重略有不同呢？*

<BigValue data={totais} value=casos title="决策案例" fmt=num0/>
<BigValue data={totais} value=alternativas title="已评估备选" fmt=num0/>
<BigValue data={totais} value=robustos title="稳健结论" fmt=num0/>
<BigValue data={totais} value=frageis title="脆弱结论" fmt=num0/>

## 📋 决策案例

> 点击任意案例即可打开**完整报告**：DEMATEL 因果图、十大学派对照图、ELECTRE 核、TOPSIS 双重标准化、博尔达共识、2000 个宇宙下的稳健性、BCG 矩阵以及决策矩阵。

<DataTable data={casos} rows=all rowShading=true link=link>
  <Column id=nome title="案例"/>
  <Column id=dominio title="领域"/>
  <Column id=n_alternativas title="备选方案" fmt=num0/>
  <Column id=vencedor_rotulo title="🏆 优胜方案"/>
  <Column id=prob_vitoria title="置信度 (%)" fmt=num1 contentType=colorscale/>
  <Column id=classificacao title="结论"/>
</DataTable>

> **如何读结论。** `稳健`（≥ 90%）= 该选择不依赖权重的精细校准，可以提交委员会。`可能`（60–90%）= 在多数情形下成立，但第二名颇具竞争力。`脆弱`（低于 60%）= **第一名是权重的产物**——系统会这么说，而不是摆出一座奖杯。

<BarChart data={resumo_dominio} x=dominio y=casos title="按应用领域划分的案例" yAxisTitle="Casos"/>

## 🧮 DEMATEL — 每个决策的根本原因

> 分配权重之前几乎没人问的问题：**各准则彼此独立吗？** 几乎从来都不独立。能耗*导致*续航；装甲*导致*重量，而重量*导致*机动性下降。把两者当作独立相加，等于把同一件事算了两遍。
>
> **DEMATEL**（Gabus 与 Fontela，Battelle）构造总关系矩阵 `T = X(I−X)⁻¹`——它把任意路径长度的直接**与间接**影响都求和——并作区分：`R+C` = 在系统中的重要性；`R−C > 0` = **原因**（杠杆：从此处着手），`R−C < 0` = **结果**（温度计：已做之事的产物）。
>
> 下方的**根本原因**一列，是每个案例中 `R−C` 最大的准则：正是在那里，一次干预能带动整个系统。

<DataTable data={alavancas} rows=all rowShading=true>
  <Column id=nome title="案例"/>
  <Column id=n_criterios title="准则" fmt=num0/>
  <Column id=n_causas title="原因" fmt=num0 contentType=colorscale/>
  <Column id=causa_raiz title="🔧 根本原因（R−C 最大）"/>
  <Column id=criterio_maior_peso title="权重最大的准则"/>
  <Column id=maior_peso_pct title="权重（%）" fmt=num1/>
</DataTable>

<BarChart data={alavancas} x=nome y={['n_causas','n_criterios']} type=grouped title="在各案例中属于原因的准则（相对总数的杠杆）" yAxisTitle="Critérios" swapXY=true/>

> **打开一个案例**，即可看到完整的因果图、`R` 与 `C` 分列的表格，以及逐条列出连接的**总关系矩阵**。

## 🎲 BCG 矩阵 — 按类别绘制的机会地图

> 除了*选哪一个*之外，每个类别还有一份**机会画像**：有多少备选是 ⭐ 明星（投入）、🐄 金牛（收获）、❓ 问号（权衡赌注）与 🐕 瘦狗（放弃）。只有问号的类别是昂贵的市场；满是金牛的类别是成熟市场，钱在其中起的作用很小。

<DataTable data={bcg_geral} rows=all rowShading=true>
  <Column id=nome title="类别"/>
  <Column id=estrelas title="⭐" fmt=num0 contentType=colorscale/>
  <Column id=vacas title="🐄" fmt=num0 contentType=colorscale/>
  <Column id=interrogacoes title="❓" fmt=num0 contentType=colorscale/>
  <Column id=abacaxis title="🐕" fmt=num0 contentType=colorscale/>
  <Column id=total title="合计" fmt=num0/>
  <Column id=quadrante_do_vencedor title="第一名所在象限"/>
</DataTable>

## ⚖️ 十大决策学派

> 每种方法都是**关于“更好”含义的不同理论**，所以我们全部运行：当十个独立学派选出同一个优胜方案时，这个选择就不是某一方法的产物。当它们分歧时，分歧恰好指出真正的权衡在哪里。

| Método | Escola | O que assume | Quando é a ferramenta certa |
|---|---|---|---|
| **AHP-TOPSIS 2n** | Distância à solução ideal | Compensação total entre 准则s | 准则 quantitativos, decisor único |
| **ELECTRE I** | 级别高于关系 | Incomparabilidade é permitida | Triagem: eliminar o que é dominado |
| **ELECTRE II** | 级别高于关系 | Limiares forte e fraco | Ordenação completa com veto |
| **PROMETHEE II** | 级别高于关系 | Preferência gradual (6 funções) | Quando "um pouco melhor" não é "melhor" |
| **MAUT** | Utilidade | Independência aditiva + 风险厌恶 | Decisão sob incerteza |
| **MCDA-C** | Construtivista | Níveis Neutro/Bom ancorados | Diagnóstico absoluto, não só ranking |
| **VIKOR** | Compromisso | Utilidade do grupo × arrependimento máximo | Quando compensar é inaceitável |
| **TODIM** | Teoria dos Prospectos | Perda dói mais que ganho equivalente | Decisor avesso a perda (todos são) |
| **SAPEVO-M** | Ordinal multidecisor | Julgamento ordinal de vários decisores | Comitê que não concorda entre si |

## 🎯 稳健性 — 决策本身的置信区间

> **问题所在。** 任何 MCDM 方法都会给出一个隐含 100% 确信度的优胜方案。但权重从不精确——它们是偏好的估计。如果某个准则的权重变动两个百分点就让第一与第二互换，那么这个“优胜方案”是校准的产物，而非这组备选的事实。没有人报告这一点。**决策正是死在委员会这一步。**
>
> **解法。** 我们以 `w' ~ Dirichlet(κ·w)` 扰动权重并重新排序 2000 次。狄利克雷分布是自然的选择：它的支撑集恰好是单纯形（和为 1 的正权重），且满足 `E[w'] = w`——我们在扰动时**不引入偏倚**。取 κ = 200 时，13% 的权重波动约 ±2.4 个百分点。
>
> 结论不再是*“C 方案最好”*，而成为**“在 96% 的合理偏好宇宙中，C 方案胜出”**。

**打开上表中的一个案例**，即可看到因果图、十大学派对照图、BCG 矩阵，以及 2000 个宇宙中各名次的完整分布。

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
