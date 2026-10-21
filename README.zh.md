<!--
MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
-->

<div align="center">

# 🎯 MCDM Studio — 多准则决策模型

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="820"/>

**ProfBru © 2026**

### 别再用电子表格做选择。开始用证据做决策。

**十二大决策学派。一个优胜方案。而且——这是第一次——附带该方案正确的概率。**

[![MCDM](https://img.shields.io/badge/MCDM方法-12-2563eb?style=for-the-badge)](#-十二大决策学派以及为何是十二个)
[![Engines](https://img.shields.io/badge/引擎-Python_+_Rust-c2410c?style=for-the-badge)](#-两个独立引擎交叉验证)
[![i18n](https://img.shields.io/badge/语言-12-16a34a?style=for-the-badge)](#-12种语言国际市场标准翻译记忆库)
[![Robustez](https://img.shields.io/badge/模拟宇宙-2.000-8f3d56?style=for-the-badge)](#共识引擎)

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Rust](https://img.shields.io/badge/Rust-1.96-000000?logo=rust&logoColor=white)](https://www.rust-lang.org)
[![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?logo=numpy&logoColor=white)](https://numpy.org)
[![Numba](https://img.shields.io/badge/Numba-JIT-00A3E0?logo=numba&logoColor=white)](https://numba.pydata.org)
[![Evidence](https://img.shields.io/badge/Evidence.dev-Dashboard-f4b548)](https://evidence.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/许可-专有-red)](#-许可与著作权)

🌐 [Português](README.md) · [English](README.en.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · **中文** · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [עברית](README.he.md) · [Русский](README.ru.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md)

</div>

---

## 💀 痛点：你已经因为一张电子表格亏过钱

回想你最近做过的一次昂贵决策。买车。选供应商。批项目。定下200个人要用四年的笔记本电脑。

**你打开了一张电子表格。选项放在行，属性放在列。然后你做了下面三件事之一：**

| 你做了什么 | 实际发生了什么 |
|---|---|
| 🔻 **按价格列排序** | 你选了最便宜的。为此你根本不需要电子表格。 |
| 🔺 **按专家评分排序** | 你选了最贵的。为此你同样不需要。 |
| 🔍 **按“满足全部要求”筛选** | 列表变成了空的。于是你放宽了一条要求。哪一条？**碍事的那条。** |

> [!WARNING]
> **这三种操作有着同一个缺陷：没有一种回答了你提出的问题。**
> 问题是*“在彼此矛盾的选项之间，该选哪一个？”*——而按某一列排序，按定义就是依据**一个**准则做决定。另外七个你根本没用上。它们摆在那里只是为了让你安心。

还有一个没人看见的问题：**你把已经加过的东西又加了一遍。**你给“能耗”20%的权重，给“续航”25%——但能耗*导致*续航。你把同一件事算了两次，还称之为分析。

### 决策死亡的那一刻

就发生在会议上。你展示排名。委员会里有人问：

> *如果续航占30%而不是25%呢？*

而你不知道。**没人知道。**因为电子表格只返回**一个**数字，带着它根本不可能拥有的100%隐含置信度。你回去做功课，调整权重，然后发现第二名以**两个百分点**的差距变成了第一名。

那个“优胜方案”从来就不是优胜方案。它是**你的校准所产生的假象**——而你差点就签了字。

---

## 💊 解法：十二大学派、一个共识，外加一个置信区间

**MCDM Studio 在同一个问题上运行**十二种成熟的多准则模型**，从其中产生排序的十种之间的**共识**中得出优胜方案，然后做那件真正重要的事：**

> ### 🎲 它把权重扰动**2000次**，统计在多少个宇宙里优胜方案依然获胜。

结论不再是一个数字，而成为一句**能在委员会上站得住脚的话**：

<div align="center">

| ❌ 电子表格说什么 | ✅ MCDM Studio 说什么 |
|---|---|
| “C方案最好。” | **“C方案在96%的合理偏好宇宙中获胜。结论为稳健：该选择不依赖权重的精细校准。”** |
| *（没有答案）* | **“A方案在51%中获胜。结论为脆弱：第一名是权重的产物。不要仅凭排名做决定。”** |

</div>

**请注意第二种情况。一个诚实的系统必须能够说出*“在这里别信我”*。这正是决策支持与“为你早已想做的决定生成理由”之间的区别。**

---

## 🖼️ 看它如何运作

### 1. 谁是原因、谁是结果——在赋任何权重之前

<div align="center"><img src="docs/telas/caca_multifuncao/dematel_causa_efeito.png" alt="DEMATEL" width="820"/></div>

**它解决的痛点：** 你赋权重时假定各准则相互独立。**它们几乎从来都不独立。**能耗*导致*续航。装甲*导致*重量，重量*导致*机动性下降。把它们当作独立项相加，就是重复计算。

**DEMATEL** 构建总关系矩阵 `T = X(I−X)⁻¹`——它累加任意路径长度的直接**与间接**影响——并区分你能**拉动**的（原因，位于零线之上）与仅仅**度量结果**的（结果，位于零线之下）。权重由此而来：源自系统性影响，而非拍脑袋。

> 在上图中，**技术转让**与**雷达特征**是原因：动它们就会牵动整个系统。**机队可用率**是结果——它是温度计，不是杠杆。一份为可用率打分却忽略技术转让的招标书，是在量体温而无视感染。

### 2. 十大学派面对同一个问题

<div align="center"><img src="docs/telas/veiculo_eletrico/mapa_metodos.png" alt="Métodos" width="900"/></div>

**它解决的痛点：** 每种MCDM方法都内嵌着一套关于“更好”意味着什么的理论——而它会改变优胜方案。选定一种方法再呈现结果，就等于选定了结果。

我们把十种全部跑一遍。当它们一致时，该选择**不是方法的产物**。当它们分歧时，**分歧本身就是发现**。

> 上图：**插电式混动**在七种方法中排第一，却在**ELECTRE I 中排第六**。这不是噪声，而是信息。ELECTRE I 允许*否决*：它指出该混动车在某个准则上的劣势严重到足以被淘汰，无论其他方面多好。**这正是你要带到委员会上的问题。**

### 3. 决策本身的置信区间

<div align="center"><img src="docs/telas/portfolio_startup/robustez.png" alt="Robustez" width="820"/></div>

**它解决的痛点：** 委员会的那个问题——*“如果权重不一样呢？”*。**在**有人提问**之前**就已作答。

我们用 `w' ~ Dirichlet(κ·w)` 扰动权重并重新排序2000次。狄利克雷分布是自然之选：其支撑集恰好是单纯形（和为1的正权重），且满足 `E[w'] = w`——我们**在不引入偏差的前提下**进行扰动。

### 4. 你的直觉错在哪里

<div align="center"><img src="docs/telas/blindado/pesos_dematel_ahp.png" alt="DEMATEL, AHP, AHP Fuzzy e BWM" width="820"/></div>

**它解决的痛点：** 你以为自己知道什么重要。两族权重会检验这一点。

**AHP**（Saaty）成对询问一个准则比另一个重要多少。**DEMATEL** 度量系统性影响。**二者分歧之处，正是你低估的二阶效应**——图中用红色标出最大分歧。

### 5. 在2000个情景中，每个方案最终落在哪里

<div align="center"><img src="docs/telas/estacao_trabalho/distribuicao_posicoes.png" alt="Distribuição" width="820"/></div>

整条全绿的条形代表一个**不依赖权重**的位次。斑驳的条形代表一个有争议的位次。你一眼就能看出排名中哪部分是事实、哪部分是意见。

---

## 🎯 它用来做什么——量身定制的选择

该引擎**与领域无关**：其单位是*决策案例*（备选方案 × 准则），不内嵌任何业务语义。更换领域就是更换数据，而不是更换代码。

<div align="center">

| 领域 | 决策内容 | 具体痛点 |
|---|---|---|
| 📱 **电子产品** | 手机、笔记本、设备 | 最便宜的相机最差；相机最好的电池最差。不存在“最好的”——只存在**最适合你使用场景的**。 |
| 🚗 **电动汽车** | 车队或个人使用 | 续航、充电、服务网络与保值率朝相反方向拉扯。而真正起决定作用的准则（**真实续航**，而非厂商标称值）恰恰最难测量。 |
| 🎖️ **国防** | 战斗机、装甲车、无人机、后勤基地 | 30年生命周期，不可逆，且处于公众监督之下。**单价不足总成本的三分之一。**技术转让与每小时使用成本决定着未来三十年的预算。 |
| 🏢 **企业** | 供应商、ERP、外包、扩张 | 一个内部无法达成一致的委员会。**SAPEVO-M** 正是为此而生：它汇总**多位决策者**的序数判断，而不要求事先达成共识。 |
| 🚀 **初创企业** | 项目组合、资本配置 | 按期望收益决策的人总会选中风险最高的那一注——**期望值忽略了尾部**。在这里，风险是**准则**，而不是第14页幻灯片的脚注。 |
| 💻 **信息技术** | 设备标准化 | 这个决策要乘以200，并持续4年。就总拥有成本而言，续航与上门保修的价值高于两分合成跑分。 |

</div>

### 可直接运行的案例

```bash
python3 pipeline.py --listar
```

| # | 案例 | 领域 | 备选方案 | 准则 | 结论 | 作者 / 来源 |
|--:|---|---|--:|--:|---|---|
| 1 | `smartphone` | 消费 | 6 | 8 | 可能 63% | 自建模型 |
| 2 | `veiculo_eletrico` | 汽车 | 7 | 8 | 稳健 99% | 自建模型 |
| 3 | `caca_multifuncao` | 国防 | 6 | 9 | 稳健 100% | 自建模型 |
| 4 | `blindado` | 国防 | 5 | 8 | 稳健 93% | 自建模型 |
| 5 | `portfolio_startup` | 企业 | 7 | 9 | 稳健 96% | 自建模型 |
| 6 | `estacao_trabalho` | 信息技术 | 6 | 8 | 稳健 98% | 自建模型 |
| 7 | `carros_eletricos` | 汽车 | 38 | 9 | 稳健 96% | 自建模型 |
| 8 | `smartphones_2026` | 消费 | 38 | 9 | 可能 73% | 自建模型 |
| 9 | `tablets` | 消费 | 34 | 8 | 可能 67% | 自建模型 |
| 10 | `smartwatches` | 消费 | 31 | 8 | 可能 84% | 自建模型 |
| 11 | `notebooks` | 信息技术 | 32 | 8 | 可能 83% | 自建模型 |
| 12 | `maquinario_agricola` | 农业 | 35 | 8 | 稳健 100% | 自建模型 |
| 13 | `sbc_iot` | 信息技术 | 33 | 8 | 稳健 100% | 自建模型 |
| 14 | `mineracao_asic` | 基础设施 | 31 | 8 | 脆弱 50% | 自建模型 |
| 15 | `minipcs` | 信息技术 | 10 | 8 | 稳健 91% | 自建模型 |
| 16 | `impressoras_3d_miniaturas` | 制造 | 30 | 9 | 脆弱 48% | 自建模型 |
| 17 | `impressoras_3d_producao` | 制造 | 30 | 9 | 脆弱 58% | 自建模型 |
| 18 | `plotters_formato` | 制造 | 24 | 9 | 稳健 96% | 自建模型 |
| 19 | `impressoras_3d_miniaturas_triadas` | 制造 | 13 | 9 | 稳健 100% | 自建模型 |
| 20 | `acoes_b3` 📚 | 金融 | 20 | 7 | 脆弱 39% | COSTA, L. S. da · VÁSQUEZ, J. A.; ESCOBAR, J. W.; MANOTAS, D. F. · [DOI](https://doi.org/10.3390/risks10010004) |
| 21 | `fundos_imobiliarios` 📚 | 金融 | 18 | 8 | 可能 85% | SANTOS, V. V. dos (orient. ALMEIDA FILHO, A. T. de) |
| 22 | `fintech` 📚 | 金融 | 16 | 8 | 可能 67% | WIBOWO, S.; GRANDHI, L.; GRANDHI, S.; WELLS, M. · [DOI](https://doi.org/10.3390/math10020225) |
| 23 | `avaliacao_imoveis` 📚 | 房地产 | 16 | 8 | 稳健 94% | DUARTE, D. C. de O. · MARQUES, J. P. M. |
| 24 | `ordens_servico` 📚 | 运营 | 18 | 8 | 稳健 97% | ALENCAR, L. G. de; TAVARES, F. R. M.; MENDONÇA, F. J. S. de F.; DUARTE, A. K. G. |
| 25 | `cloud_providers` 📚 | 信息技术 | 14 | 8 | 稳健 100% | SOLOMON, T. |
| 26 | `venture_capital` 📚 | 企业 | 16 | 8 | 稳健 96% | BEIM, G.; LÉVESQUE, M. · DHOCHAK, M.; DOLIYA, P. · AFFUL-DADZIE, E.; AFFUL-DADZIE, A.; OPLATKOVÁ, Z. K. · [DOI](https://doi.org/10.1002/mcda.1703) |
| 27 | `instrutores` 📚 | 企业 | 15 | 8 | 稳健 100% | SILVA, C. E. J. da; SALLES-NETO, L. L. de; SANTOS, M. dos |
| 28 | `cripto_portfolio` 📚 | 金融 | 9 | 7 | 稳健 100% | ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. · [DOI](https://doi.org/10.3390/math9141677) |
| 29 | `portfolio_crise` 📚 | 金融 | 8 | 4 | 可能 77% | COSTA, I. P. de A.; MAÊDA, S. M. do N.; TEIXEIRA, L. F. H. de S. de B.; GOMES, C. F. S.; SANTOS, M. dos |
| 30 | `cenarios_va` 📚 | 汽车 | 16 | 9 | 可能 73% | LI, S.; ZHOU, R.; HUANG, H. · [DOI](https://doi.org/10.1007/s42154-024-00344-6) |
| 31 | `impressora_3d_energia` 📚 | 制造 | 12 | 7 | 可能 69% | OLIVEIRA, V. A. R. de; ALVARADO SILVA, C. A.; OLIVEIRA, G. C. R. de; TAJIMA, F. M.; FARIA NETO, A. dos R.; SALOMON, V. A. P.; GUIDI, E. S. · [DOI](https://doi.org/10.18687/LACCEI2025.1.1.1193) |
| 32 | `impressoras_juridico` 📚 | 运营 | 12 | 4 | 稳健 100% | OLIVEIRA, N. C.; OLIVEIRA, P. F. C. de; GOMES, C. F. S.; SANTOS, M. dos |
| 33 | `fundos_hedge` 📚 | 金融 | 20 | 8 | 稳健 94% | SILVA, F. P. da; RIBEIRO, C. de O. |
| 34 | `modelos_previsao` 📚 | 信息技术 | 7 | 8 | 稳健 95% | SHAH, S. |
| 35 | `policultivo_rj` 📚 | 农业 | 8 | 8 | 可能 86% | PENEDO, B. |
| 36 | `parafusadeiras_domesticas` 📚 | 消费 | 14 | 8 | 可能 70% | COMPROU AVALIOU (canal) · [vídeo](https://youtu.be/pgdqVYEjZtk) |
| 37 | `parafusadeiras_profissionais` 📚 | 制造 | 12 | 8 | 稳健 100% | FERRAMENTAS EM AÇÃO — ASSIS PIRES (canal) · [vídeo](https://youtube.com/shorts/9SIs3agoZKc) |
| 38 | `crowdfunding_startups` 📚 | 企业 | 16 | 9 | 稳健 93% | SKARE, M.; GAVUROVA, B.; POLISHCHUK, V. · [DOI](https://doi.org/10.1016/j.jbusres.2023.113719) |

> [!NOTE]
> 案例矩阵是**示意性的**——采用公开且合理的数量级，用于演示方法。**并非**示意性的是**建模本身**：准则、方向、DEMATEL因果矩阵与Saaty矩阵。价值正在于此。**请把数字替换成你的报价、你的招标书或你的实验室测试结果**——引擎不变，数据是你的。

> [!TIP]
> **结论**衡量在 2000 个模拟偏好世界中优胜者仍然获胜的比例，权重按 Dirichlet(κ=200) 扰动。**稳健** ≥ 90%：结果不依赖于权重校准。**可能** 60–89%：亚军具有竞争力，请比较两者。**脆弱** < 60%：第一名只是权重造成的假象——这是一项正当的发现，而非失败。它意味着数据无法定夺，决策回到人手中。

### 📚 源自文献的案例研究

> [!IMPORTANT]
> 下表各案例的**准则与因果结构取自所列文献**——同行评审论文、学位论文、会议论文集与技术报告。准则并非杜撰：它们出自原文，著作权信息保留在此处及对应模块的文件头中。**数值矩阵**为我们自行构造——未复制原作中的任何数据。凡有收录 DOI 者，链接直达原文；无 DOI 者，完整的文字著录足以查找。

| 案例 | 领域 | 作者 | 参考文献 |
|---|---|---|---|
| `acoes_b3` | 金融 | COSTA, L. S. da · VÁSQUEZ, J. A.; ESCOBAR, J. W.; MANOTAS, D. F. | *Uma metodologia para a pré-seleção de ações utilizando o método multicritério TOPSIS* (COSTA, UERJ) · *AHP–TOPSIS Methodology for Stock Portfolio Investments*, Risks, v.10, n.1, 4, 2022 (Universidad del Valle) · [DOI](https://doi.org/10.3390/risks10010004) |
| `fundos_imobiliarios` | 金融 | SANTOS, V. V. dos (orient. ALMEIDA FILHO, A. T. de) | *Avaliação do método Random Forest para auxílio à seleção de fundos de investimento imobiliário listados na Bolsa de Valores*. Trabalho de Graduação, Engenharia da Computação, CIn/UFPE, set. 2023 |
| `fintech` | 金融 | WIBOWO, S.; GRANDHI, L.; GRANDHI, S.; WELLS, M. | *A Fuzzy Multicriteria Group Decision Making Approach for Evaluating and Selecting Fintech Projects*. Mathematics, v.10, n.2, 225, 2022 — CQUniversity, Austrália · [DOI](https://doi.org/10.3390/math10020225) |
| `avaliacao_imoveis` | 房地产 | DUARTE, D. C. de O. · MARQUES, J. P. M. | *Análise multicritério e geoestatística aplicadas na avaliação em massa de imóveis urbanos*. Tese, UFV, 2019 · *As formas de avaliar imóvel em leilão judicial*. Universidade São Judas Tadeu, 2023 |
| `ordens_servico` | 运营 | ALENCAR, L. G. de; TAVARES, F. R. M.; MENDONÇA, F. J. S. de F.; DUARTE, A. K. G. | *Priorização de ordens de serviço aplicando métodos de tomada de decisão: o AHP integrado ao PROMETHEE*. Revista Produção Online, v.22, n.2, p.2763-2784, 2022 — URCA, Ceará |
| `cloud_providers` | 信息技术 | SOLOMON, T. | *Ranking of Cloud Service Providers Using a Dynamic TOPSIS Model for Provisioning of Enterprise IT Infrastructure in the Cloud*. Praxis (Doctor of Engineering), The George Washington University, 2017 |
| `venture_capital` | 企业 | BEIM, G.; LÉVESQUE, M. · DHOCHAK, M.; DOLIYA, P. · AFFUL-DADZIE, E.; AFFUL-DADZIE, A.; OPLATKOVÁ, Z. K. | *Selecting projects for venture capital funding: a multiple criteria decision approach* (Case Western Reserve University) · *Valuation of a startup: moving towards strategic approaches*, J. Multi-Criteria Decision Analysis, 2019 · *Assessing commercial viability of technology start-up businesses in a government venture capital under intuitionistic fuzzy environment*, Int. J. Fuzzy Systems, 2016 · [DOI](https://doi.org/10.1002/mcda.1703) · [DOI](https://doi.org/10.1007/s40815-016-0141-9) |
| `instrutores` | 企业 | SILVA, C. E. J. da; SALLES-NETO, L. L. de; SANTOS, M. dos | *Modelagem matemática com os métodos AHP e TOPSIS para ordenação de instrutores em uma escola da FAB*. LIV SBPO, Juiz de Fora, 2022 — ITA / UNIFESP / IME |
| `cripto_portfolio` | 金融 | ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. | *Cryptocurrency Portfolio Selection — A Multicriteria Approach*. Mathematics, v.9, n.14, 1677, 2021 — University of Split, Croácia — **pesos AHP do artigo** · [DOI](https://doi.org/10.3390/math9141677) |
| `portfolio_crise` | 金融 | COSTA, I. P. de A.; MAÊDA, S. M. do N.; TEIXEIRA, L. F. H. de S. de B.; GOMES, C. F. S.; SANTOS, M. dos | *Finanças em períodos de crise: aplicação do método SAPEVO-M para composição de portfólios de investimentos*. Pesquisa Operacional para o Desenvolvimento, v.13, e13004, 2021 — UFF / CASNAV / IME — **matriz de decisão do artigo** |
| `cenarios_va` | 汽车 | LI, S.; ZHOU, R.; HUANG, H. | *Multidimensional Evaluation of Autonomous Driving Test Scenarios Based on AHP-EWM-TOPSIS Models*. Automotive Innovation, 2025 · [DOI](https://doi.org/10.1007/s42154-024-00344-6) |
| `impressora_3d_energia` | 制造 | OLIVEIRA, V. A. R. de; ALVARADO SILVA, C. A.; OLIVEIRA, G. C. R. de; TAJIMA, F. M.; FARIA NETO, A. dos R.; SALOMON, V. A. P.; GUIDI, E. S. | *Multicriteria Analysis for 3D Printer Selection*. 23rd LACCEI International Multi-Conference, Cidade do México, 2025 — UNESP / Universidad César Vallejo · [DOI](https://doi.org/10.18687/LACCEI2025.1.1.1193) |
| `impressoras_juridico` | 运营 | OLIVEIRA, N. C.; OLIVEIRA, P. F. C. de; GOMES, C. F. S.; SANTOS, M. dos | *Aplicação do método AHP TOPSIS 2N como apoio à tomada de decisão: estudo de caso no departamento jurídico da Secretaria Municipal de Saúde de Duque de Caxias* — UNIGRANRIO / UFF / IME |
| `fundos_hedge` | 金融 | SILVA, F. P. da; RIBEIRO, C. de O. | *Análise comparativa de fundos de hedge brasileiros utilizando DEA e bootstrap*. XII SIMPEP, Bauru-SP, 2005 — Escola Politécnica da USP |
| `modelos_previsao` | 信息技术 | SHAH, S. | *Comparison of Stochastic Forecasting Models*. Stochastic Differential Equations Course Project, Johns Hopkins University — o artigo compara os modelos; a modelagem multicritério sobre eles é deste projeto |
| `policultivo_rj` | 农业 | PENEDO, B. | *AGTech PoliCultivo 4.0 — Otimização de Portfólio de Cultivos em Ambiente Controlado (RJ)*. Relatório técnico, 03/08/2026, seção 14 — **matriz e pesos do relatório** |
| `parafusadeiras_domesticas` | 消费 | COMPROU AVALIOU (canal) | *As 5 Melhores Parafusadeira De 2025*, 14/05/2024 — especificações extraídas da narração · [vídeo](https://youtu.be/pgdqVYEjZtk) |
| `parafusadeiras_profissionais` | 制造 | FERRAMENTAS EM AÇÃO — ASSIS PIRES (canal) | *As Melhores Parafusadeiras Do Mundo*, 04/01/2024 — modelos e baterias lidos dos quadros do vídeo · [vídeo](https://youtube.com/shorts/9SIs3agoZKc) |
| `crowdfunding_startups` | 企业 | SKARE, M.; GAVUROVA, B.; POLISHCHUK, V. | *A decision-making support model for financing start-up projects by venture capital funds on a crowdfunding platform*. Journal of Business Research, v.158, 113719, 2023 — **critérios e escalas do artigo** · [DOI](https://doi.org/10.1016/j.jbusres.2023.113719) |

---

## ⚡ 安装

### 最快路径（Python）

```bash
git clone <url> multicriteriadecisionmodels
cd multicriteriadecisionmodels/public/foundations/pipeline
pip install -r requirements.txt
python3 pipeline.py
```

完成。六个案例全部运行，并给出完整报告。

<details>
<summary><b>详细前置条件</b></summary>

| 组件 | 最低版本 | 是否必需 | 用途 |
|---|---|---|---|
| Python | 3.10 | ✅ | 参考引擎 |
| NumPy | 2.0 | ✅ | 所有方法的代数运算 |
| numba | 0.60 | ⚠️ | 内核JIT——没有它结果相同，只是更慢 |
| SciPy | 1.10 | ✅ | 辅助统计 |
| matplotlib | 3.7 | ✅ | 每个案例的5张图 |
| Rust / cargo | 1.75 | ⭕ | 交叉验证引擎 |
| Node.js | 18 | ⭕ | Evidence 仪表板 |
| screen | — | ⭕ | 后台执行 |

</details>

### 完整流水线

```bash
./run_all.sh                    # 测试 → 流水线 → 图表 → i18n → Rust → 核对
./run_all.sh --rapido           # 跳过 Rust 与 i18n
./run_all.sh --caso smartphone  # 仅一个案例
./run_all.sh --background       # 在 screen 中运行（重新接入：screen -r mcdm）
```

### Rust 引擎——无需运行时的二进制文件

```bash
cd public/foundations/rust/mcdm_core
cargo test --release
cargo build --release

./target/release/mcdm --exemplo > problema.mcdm
./target/release/mcdm problema.mcdm
./target/release/mcdm problema.mcdm --json
```

### 仪表板

```bash
cd public/foundations/evidence
npm install
npm run dev               # http://localhost:3000
```

<details>
<summary><b>高级命令</b></summary>

```bash
python3 pipeline.py caca_multifuncao --workers 8 --iter 5000
python3 testes_nucleo.py
python3 exportar_rust.py
python3 gerar_i18n.py --tudo
python3 gerar_i18n.py --verificar
python3 gerar_graficos.py --workers 6
```

| 变量 | 默认值 | 作用 |
|---|---|---|
| `MCDM_WORKERS` | auto | `ProcessPoolExecutor` 的进程数 |
| `MCDM_NUMBA` | `1` | 启用JIT；设为 `0` 可在纯 NumPy 下调试 |
| `MCDM_SEED` | `42` | 可复现性 |
| `ROBUSTEZ_ITER` | `2000` | 偏好宇宙数 |
| `ROBUSTEZ_KAPPA` | `200` | 狄利克雷集中度（越大权重越贴近原值） |
| `MAUT_AVERSAO` | `2.0` | 风险厌恶（r > 0 为凹函数） |
| `PROMETHEE_TIPO` | `linear` | 偏好函数（共6种） |

</details>

---

## ⚖️ 十二大决策学派——以及为何是十二个

> [!IMPORTANT]
> **每种方法都是关于“更好”意味着什么的不同理论。** 只用一种，等于在选定问题的同时选定了答案。我们把它们全部运行，因为**独立理论之间的一致**是决策问题所能提供的最强证据。

<div align="center">

| 方法 | 学派 | 其假设 | 何时它是**恰当**的工具 | 出处 |
|---|---|---|---|---|
| **AHP-TOPSIS 2n** | 到理想解的距离 | 完全补偿 | 定量准则、单一决策者 | Saaty (1980); Hwang & Yoon (1981) |
| **ELECTRE I** | 级别高于关系 | 允许不可比 | **初筛**：剔除被支配者 | Roy (1968) |
| **ELECTRE II** | 级别高于关系 | 强弱双阈值 | **带否决权的**完全排序 | Roy & Bertier (1971) |
| **PROMETHEE II** | 级别高于关系 | 渐进偏好（6种函数） | 当“好一点”≠“更好”时 | Brans & Vincke (1985) |
| **MAUT** | 效用 | 可加独立性 + 风险厌恶 | 不确定条件下的决策 | Keeney & Raiffa (1976) |
| **MCDA-C** | 建构主义 | 锚定的中性/良好水平 | **绝对诊断**，不只是排名 | Ensslin, Montibeller & Noronha (2001) |
| **VIKOR** | 折中 | 群体效用 × 最大后悔 | 当**补偿不可接受**时 | Opricovic (1979); Opricovic & Tzeng (2002-07) |
| **TODIM** | 前景理论 | 损失之痛大于等量收益之喜 | 厌恶损失的决策者——**人人如此** | Gomes & Lima (1992); Kahneman & Tversky (1979) |
| **SAPEVO-M** | 多决策者序数法 | 多位决策者的序数判断 | **内部无法达成一致的委员会** | Gomes et al. (1997); Teixeira, Santos & Gomes (2019) |
| **TOPSIS Fuzzy** | 模糊 | 数据是一个**区间**，而非一个点 | 测量不精确，而你想知道排名是否经得起这种不确定 | Zadeh (1965); Chen (2000) |
| **BWM** | 权重来源 | 决策者能指出最佳与最差准则 | **萨蒂矩阵填不完**：2n−3 次比较，而非 n(n−1)/2 | Rezaei (2015; 2016) |
| **DRSA** | 规则归纳 | 存在过往决策，且它们尊重占优关系 | 没人能给出权重，但**有历史决策**——而答案必须是**可读的规则** | Greco, Matarazzo & Słowiński (1999; 2001) |

</div>

> [!NOTE]
> **模糊 TOPSIS** 不是「加了噪声的 AHP-TOPSIS」：除三角模糊数外，它还更换了归一化方式（线性而非向量）与理想解（绝对而非相对）。**与 AHP-TOPSIS 2n 产生分歧是预期行为**，它衡量排名对这些选择的依赖程度。**模糊 AHP**（Buckley）作为第三种权重来源，与 DEMATEL、AHP 并列：它接受同样的两两判断，但把不确定性一路带到最后——在均匀展幅下中心值与 AHP 一致，它新增的是**区间**，用以回答优先次序能否经得起决策者自身的不确定。

> [!IMPORTANT]
> **BWM 与 DRSA 的位置与其余十个不同。** BWM 是**权重来源**——AHP 与 DEMATEL 的替代——DRSA 则从过往决策中**归纳规则**。两者都不产生自己的排名，因此**博尔达共识与稳健性分析仍在十个排序方法之上计算**。

<details>
<summary><b>为何这三种值得特别关注</b></summary>

### VIKOR — 当补偿不可接受时
VIKOR 计算**两个**度量：`S`（群体效用——加权和，**接受**某项极差表现被多项良好表现抵消）与 `R`（最大个体后悔——极小化极大，**拒绝**补偿）。

一辆机动性极佳而防护极差的装甲车，`S` 很优、`R` 很糟。加权和会选中它；VIKOR 会发出警示。当 `S` 与 `R` 不一致时，条件 **C1**（可接受优势）与 **C2**（可接受稳定性）会明确报告该决策存在盲区。

### TODIM — 损失之痛大于收益之喜
基于 Kahneman 与 Tversky 的**前景理论**：失去10点续航所带来的痛苦，大于获得10点所带来的愉悦。经典加权和忽略这种不对称性，把收益与损失同等对待——**而没有任何人类决策者会这样做。**因子 `θ` 用于校准强度：`θ < 1` 会放大损失厌恶。

### SAPEVO-M — 无法达成一致的委员会
其他所有方法都需要一个权重向量。**当五位决策者意见不同时，它从哪里来？**SAPEVO-M 从源头解决：每位决策者表达**序数**偏好（“续航比价格重要得多”，采用七点量表），方法在**不要求事先达成共识排序**的情况下进行汇总。委员会实际就是这样表达的——没有人会说“续航值0.237”。

</details>

### 共识引擎

```
DEMATEL · AHP · AHP Fuzzy · BWM ──► 按影响力得出的权重 ──► 10种方法 ──► 波达共识 ──► 优胜方案
                                                                        │
                                        2000个狄利克雷宇宙 ───────────────────┘
                                                    ▼
                                 结论: ROBUSTO / PROVÁVEL / FRÁGIL

DRSA ──────────────────────────────► 由过往决策归纳出的可读规则
```

| 结论 | 置信度 | 应当怎么做 |
|---|---|---|
| 🟢 **稳健** | ≥ 90% | 该选择不依赖精细校准。**可以提交委员会。** |
| 🟡 **可能** | 60–90% | 在多数情景下成立，但第二名颇具竞争力。**请比较两者。** |
| 🔴 **脆弱** | < 60% | 第一名是**权重的产物**。不要仅凭排名做决定：回到决策者那里重新校准。 |

---

## 🔬 两个独立引擎：交叉验证

> [!TIP]
> **为什么要用 Rust 重新实现一遍？** 因为“代码能跑”并不能证明**数学**是对的。

公式转录错误极少会在两种线性代数彼此独立的语言中**完全一致地**重复出现。Python 引擎使用 NumPy/LAPACK；Rust 引擎则**手写实现**带部分主元的高斯消元与幂法，**不依赖任何外部库**。

```bash
python3 exportar_rust.py
```
```
✅ smartphone           8 种方法完全一致 · 优胜方案=C     (Δ ≤ 4.7e-11)
✅ veiculo_eletrico     8 种方法完全一致 · 优胜方案=EV6   (Δ ≤ 4.1e-11)
✅ caca_multifuncao     8 种方法完全一致 · 优胜方案=C3    (Δ ≤ 4.5e-11)
✅ blindado             8 种方法完全一致 · 优胜方案=B3    (Δ ≤ 4.6e-11)
✅ portfolio_startup    8 种方法完全一致 · 优胜方案=P3    (Δ ≤ 4.9e-11)
✅ estacao_trabalho     8 种方法完全一致 · 优胜方案=W5    (Δ ≤ 5.0e-11)
```

**额外收获：Rust 二进制文件不需要 Python、NumPy、numba，也不需要虚拟环境。仅几MB，可在服务器、容器或嵌入式设备上运行——当引擎要随系统部署到现场时，这一点至关重要。**

---

## 🚀 性能：快26倍，结果不变

稳健性分析要运行2000个宇宙 × 10种方法。朴素实现每个案例耗时**42秒**。

<div align="center">

| 阶段 | 耗时 | 加速比 |
|---|---|---|
| 逐宇宙的JIT内核 | 42,33 s | — |
| **预编译为张量** | 2,41 s | **17,6×** |
| `ranks` 加JIT + 按进程持有状态 | **1,63 s** | **26,0×** |

</div>

> **收益最大的优化既不是并行，也不是JIT。** 而是意识到十种方法中有四种**对权重向量是线性的**——这使得可以预先计算张量，把每个宇宙化简为一次矩阵-向量乘法。**代数优先于基础设施。**

而且结果与慢速路径**逐位完全一致**——每次运行测试套件都会验证100个宇宙 × 10种方法。改变结果的优化是缺陷，不是收益。

<details>
<summary><b>项目执行策略</b></summary>

| 规则 | 应用 |
|---|---|
| **并行** | CPU密集型工作使用 `ProcessPoolExecutor`；绝不使用线程（GIL会串行化） |
| **阈值** | 串行还是并行由**工作量**（`n_iter · m² · k`）决定，而非元素个数——把小问题并行化比直接求解**更慢** |
| **JIT** | 在 O(m²k) 内核上使用带 `cache=True` 的 `numba`；缺失时降级为纯 NumPy |
| **后台** | 使用 `screen`，绝不用 `nohup`——可重新接入并交互 |
| **可复现性** | 固定且与进程数无关的分区：相同种子 → 无论1个还是32个进程结果都相同 |

</details>

---

## 🌐 12种语言——国际市场标准翻译记忆库

这不是对 README 做机器翻译，而是一条采用国际市场标准翻译记忆库的**本地化流水线**。

```
translation.memory.md          ← 规范来源，纳入 git 版本管理
   │  --tm
   ▼
strings.<locale>.json          ← 被消费的产物
   │  --paginas
   ▼
12个仪表板页面 + 12份 README
   │  --tmx
   ▼
translation.memory.tmx         ← 可导入 SDL Trados Studio
```

| 项目 | 数量 |
|---|---|
| 语言区域 | **12** (pt-BR · en · es · fr · de · zh · ko · hi · **he RTL** · ru · sv · fi) |
| 翻译单元 | 56 |
| 术语库条目（MultiTerm） | 22 |
| TMX 中的片段数 | **948** |
| 编码 | UTF-8 · LF · NFC |

```bash
python3 gerar_i18n.py --verificar
```

质检复刻了 Trados 的 **Verify**：术语一致性、占位符保留、片段覆盖率、严格编码以及不可译内容完好——并按书写系统区别对待（技术缩写在任何语言中都保持拉丁字母；在非拉丁文字中，专有名词则采用**音译**）。

---

## 📁 内部结构

```
multicriteriadecisionmodels/
├── README.md (+11)                     12种语言的展示页
├── docs/                               README 用的标识与截图
│
└── public/foundations/
    ├── pipeline/                       PYTHON 引擎（参考实现）
    │   ├── nucleo.py                   DEMATEL · ELECTRE I/II · PROMETHEE II
    │   │                               MAUT · MCDA-C · AHP · TOPSIS 2N
    │   ├── metodos_br.py               SAPEVO-M · VIKOR · TODIM · Copeland
    │   ├── fuzzy.py                    AHP Fuzzy · TOPSIS Fuzzy
    │   ├── bwm.py                      BWM (Rezaei)
    │   ├── drsa.py                     DRSA (Greco · Matarazzo · Słowiński)
    │   ├── robustez.py                 狄利克雷 + ProcessPoolExecutor
    │   ├── pipeline.py                 编排器
    │   ├── gerar_graficos.py           每个案例6张图
    │   ├── gerar_i18n.py               TM → 字符串 → 页面 → TMX
    │   ├── testes_nucleo.py            99项数学检验
    │   ├── exportar_rust.py            引擎间核对
    │   ├── casos/                     38个案例 + 校验
    │   └── run_all.sh                  流水线（screen）
    │
    ├── rust/mcdm_core/                 RUST 引擎（验证 + 分发）
    │   └── src/lib.rs                  全部方法，零依赖
    │
    └── evidence/                       仪表板（Evidence.dev）
        ├── sources/mcdm/               11条SQL查询
        └── pages/                      12条语言路由
```

---

## 🧠 理论依据

本项目建立在经过评审的文献之上，而非直觉。集成架构遵循 **John (2025)** 的 *“Integration of DEMATEL with Other MCDM Methods for Comprehensive Techno-Economic Analysis”*：由 DEMATEL 揭示因果结构并导出**按影响力确定的权重**，再供各排序方法使用——而不是人为指定权重。

**巴西多准则决策支持学派**的方法（SAPEVO-M、TODIM-FSE、ELECTRE II、VIKOR、序数方法）遵循 **IME**、**UFF**、**CASNAV**、**AMAN** 与 **FURB** 的研究成果——其中包括**海战无人机评估**、**旅级后勤基地分类**以及**巴西海军护卫舰排序**等真实应用。

> [!NOTE]
> **这些方法的著作权完全属于其创造者，** 已在 `nucleo.py` 与 `metodos_br.py` 的文件头中逐一署名。本项目贡献的是实现、集成与共识引擎——**而非方法本身**。

---

## ❓ 你将会提出的问题

<details>
<summary><b>我已经在用加权决策矩阵了。这不是一回事吗？</b></summary>

不是，理由有三。**(1)** 加权矩阵只是**一种**方法（加权和），内嵌着一套理论：完全补偿。它假定某个准则上的极差表现可以被别处的良好表现抵消——这在安全性、装甲防护与合规性上并不成立。**(2)** 它假定准则相互独立，而你几乎总是在把已经加过的东西再加一遍。**(3)** 它给出一个没有置信区间的数字，因此撑不过委员会的第一个问题。
</details>

<details>
<summary><b>我该如何选择权重？</b></summary>

你不必选——**有五条路径推导出它们**。**DEMATEL** 从你声明的因果结构（谁影响谁）中提取；**AHP** 从两两比较中提取，并以一致性检验**否决**自相矛盾的判断；**模糊 AHP** 做同样的事，但承认每个判断是一个区间而非一个点；**BWM** 只问最佳与最差准则——2n−3 次比较而非 n(n−1)/2，因此在 AHP 填不动的地方它仍可填；**SAPEVO-M** 从多位决策者的序数判断中提取。之后，稳健性分析再问：结果究竟还有多**依赖**它们。
</details>

<details>
<summary><b>如果我的问题有200个备选方案怎么办？</b></summary>

能跑。并行阈值会识别当前规模并把任务分配到各进程。实测：60个方案 × 12个准则 × 2000个宇宙，4进程下耗时3.8秒。超过约700个方案后，偏好张量会超出配置的内存上限，引擎会发出警告，而不是卡死。
</details>

<details>
<summary><b>各方法出现了分歧。现在怎么办？</b></summary>

**这正是产出，而不是问题。**分歧说明你的决策对所采用的学派敏感——并指明是哪一个。如果 ELECTRE 把其他方法一致选中的方案降级，那就存在某个准则，使该方案严重到足以被否决。把**这件事**带到委员会上，而不是那份排名。
</details>

<details>
<summary><b>我可以使用自己的数据吗？</b></summary>

这正是它的用途。一个案例就是 `casos/catalogo.py` 中的一段声明式结构：准则（含方向与单位）、备选方案、决策矩阵、DEMATEL 因果矩阵与 Saaty 矩阵。校验器会在**任何计算之前**拒绝格式错误的案例——维度不一致、对角线错误、Saaty 矩阵不互反、常数准则毫无区分度等。
</details>

---

## 📜 许可与著作权

<div align="center">

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="420"/>

**ProfBru © 2026**

**MCDM Studio — 多准则决策模型**
作者: **ProfBru - Bruno Penedo** © 2026 — **保留所有权利**
📧 profbruanbima@gmail.com

</div>

**专有**项目。本仓库不授予任何使用、复制、修改、分发或创作衍生作品的许可。商业、学术或机构用途须取得作者的书面授权。

**第三方署名:** 各多准则方法归其各自创造者所有——Saaty、Roy、Bertier、Brans、Vincke、Keeney、Raiffa、Ensslin、Montibeller、Noronha、Gabus、Fontela、Opricovic、Tzeng、Hwang、Yoon、Kahneman、Tversky、Borda、Copeland、Gomes、Lima、Santos、Teixeira、Moreira、Rangel、Neves、Hein、Kroenke、Keunecke 与 Gomes Júnior——已在源代码中逐一署名。
