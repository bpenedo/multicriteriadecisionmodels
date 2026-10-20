<!--
MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
-->

<div align="center">

# 🎯 MCDM Studio — Multi-Criteria Decision Models

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="820"/>

**ProfBru © 2026**

### Stop choosing with a spreadsheet. Start deciding with proof.

**Ten schools of decision. One winner. And — for the first time — the probability that this winner is right.**

[![MCDM](https://img.shields.io/badge/MCDM_Methods-10-2563eb?style=for-the-badge)](#-the-ten-schools-of-decision--and-why-ten)
[![Engines](https://img.shields.io/badge/Engines-Python_+_Rust-c2410c?style=for-the-badge)](#-two-independent-engines-the-cross-check)
[![i18n](https://img.shields.io/badge/Languages-12-16a34a?style=for-the-badge)](#-12-languages--sdl-trados-translation-memory)
[![Robustez](https://img.shields.io/badge/Simulated_universes-2.000-8f3d56?style=for-the-badge)](#-the-question-nobody-answers-what-if-the-weights-are-wrong)

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Rust](https://img.shields.io/badge/Rust-1.96-000000?logo=rust&logoColor=white)](https://www.rust-lang.org)
[![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?logo=numpy&logoColor=white)](https://numpy.org)
[![Numba](https://img.shields.io/badge/Numba-JIT-00A3E0?logo=numba&logoColor=white)](https://numba.pydata.org)
[![Evidence](https://img.shields.io/badge/Evidence.dev-Dashboard-f4b548)](https://evidence.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-Proprietary-red)](#-license-and-authorship)

🌐 [Português](README.md) · **English** · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [中文](README.zh.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [עברית](README.he.md) · [Русский](README.ru.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md)

</div>

---

## 💀 The pain: you have already lost money because of a spreadsheet

Think of the last expensive decision you made. Buying the car. Choosing the supplier. Approving the project. Picking the laptop 200 people will use for four years.

**You opened a spreadsheet. Options in rows, attributes in columns. And then you did one of these three things:**

| What you did | What actually happened |
|---|---|
| 🔻 **Sorted by the price column** | You picked the cheapest. You did not need a spreadsheet for that. |
| 🔺 **Sorted by the expert score** | You picked the most expensive. You did not need one for that either. |
| 🔍 **Filtered by "meets all requirements"** | The list came back empty. So you relaxed one requirement. Which one? **The one that was in the way.** |

> [!WARNING]
> **All three operations share the same flaw: none of them answers the question you asked.**
> The question was *"among options that contradict each other, which one do I choose?"* — and sorting by a column is, by definition, deciding by **one** criterion. You never used the other seven. They were there to make you feel better.

And there is the problem nobody sees: **you added up things that were already added up.** You gave 20% to "energy consumption" and 25% to "range" — but consumption *causes* range. You counted the same thing twice and called it analysis.

### The moment the decision dies

It happens in the meeting. You present the ranking. Someone on the committee asks:

> *What if range were worth 30% instead of 25%?*

And you do not know. **Nobody does.** Because the spreadsheet returns **one** number, with an implicit 100% confidence it has no way of having. You go back, adjust the weights, and find that second place becomes first with **two percentage points** of difference.

That "winner" was never a winner. It was an **artefact of your calibration** — and you almost signed off on it.

---

## 💊 The solution: ten schools, one consensus, and a confidence interval

**MCDM Studio runs **nine established multi-criteria methods** on the same problem, draws the winner from the **consensus** among them, and then does the one thing that actually matters:**

> ### 🎲 It perturbs the weights **2,000 times** and counts in how many universes the winner keeps winning.

The verdict stops being a number and becomes a **sentence that survives the committee**:

<div align="center">

| ❌ What the spreadsheet says | ✅ What MCDM Studio says |
|---|---|
| "Model C is the best." | **"Model C wins in 96% of plausible preference universes. Verdict ROBUST: the choice does not depend on fine-tuning the weights."** |
| *(no answer)* | **"Model A wins in 51%. Verdict FRAGILE: first place is an artefact of the weights. Do not decide on the ranking alone."** |

</div>

**Look at the second case. An honest system has to be able to say *"do not trust me here"*. That is the difference between decision support and a generator of justification for the decision you already wanted to make.**

---

## 🖼️ See it working

### 1. Which criteria are causes and which are effects — before any weighting

<div align="center"><img src="docs/telas/caca_multifuncao/dematel_causa_efeito.png" alt="DEMATEL" width="820"/></div>

**The pain this solves:** you assign weights assuming criteria are independent. **They almost never are.** Energy consumption *causes* range. Armour *causes* weight, which *causes* loss of mobility. Adding them as independent is double counting.

**DEMATEL** builds the total relation matrix `T = X(I−X)⁻¹` — summing direct **and indirect** influence of any path length — and separates what you can **pull** (causes, above the line) from what merely **measures the result** (effects, below). The weights come from there: by systemic influence, not by guesswork.

> In the case above, **Technology Transfer** and **Radar Signature** are CAUSES: moving them moves the whole system. **Fleet availability** is an EFFECT — a thermometer, not a lever. A tender that scores availability and ignores ToT is measuring the fever and ignoring the infection.

### 2. Ten schools on the same problem

<div align="center"><img src="docs/telas/veiculo_eletrico/mapa_metodos.png" alt="Métodos" width="900"/></div>

**The pain this solves:** every MCDM method carries an embedded theory of what "best" means — and it changes the winner. Choosing one method and presenting the result is choosing the result.

We run all nine. When they agree, the choice is **not a method artefact**. When they diverge, **the divergence is the finding**.

> Above: the **plug-in hybrid** is 1st in seven methods but **6th in ELECTRE I**. That is not noise — it is information. ELECTRE I allows *veto*: it says the hybrid has a disadvantage severe enough in some criterion to be eliminated, however good it is elsewhere. **That is exactly the question you want to take to the committee.**

### 3. A confidence interval on the decision itself

<div align="center"><img src="docs/telas/portfolio_startup/robustez.png" alt="Robustez" width="820"/></div>

**The pain this solves:** the committee's question — *"what if the weight were different?"*. Answered **before** anyone asks.

We perturb the weights with `w' ~ Dirichlet(κ·w)` and re-rank 2,000 times. The Dirichlet is the natural choice: its support is exactly the simplex (positive weights summing to 1) and it satisfies `E[w'] = w` — we perturb **without bias**.

### 4. Where your intuition is wrong

<div align="center"><img src="docs/telas/blindado/pesos_dematel_ahp.png" alt="DEMATEL x AHP" width="820"/></div>

**The pain this solves:** you think you know what matters. Two families of weights put that to the test.

**AHP** (Saaty) asks, pairwise, how much more one criterion matters than another. **DEMATEL** measures systemic influence. **Where they diverge is the second-order effect you underestimated** — and the chart marks the largest divergence in red.

### 5. Where each alternative ends up, across 2,000 scenarios

<div align="center"><img src="docs/telas/estacao_trabalho/distribuicao_posicoes.png" alt="Distribuição" width="820"/></div>

A fully green bar is a position that **does not depend on the weights**. A mottled bar is a contested position. You see at a glance where the ranking is fact and where it is opinion.

---

## 🎯 What it is for — the tailored choice

The engine is **domain-agnostic**: the unit is the *decision case* (alternatives × criteria), with no business semantics baked in. Changing domain means changing data, not code.

<div align="center">

| Domain | The decision | The specific pain |
|---|---|---|
| 📱 **Electronics** | Phone, laptop, equipment | The cheapest has the worst camera; the best camera has the worst battery. There is no "best" — there is **the best for your use**. |
| 🚗 **Electric vehicles** | Fleet or personal use | Range, charging, service network and resale pull in opposite directions. And the deciding criterion (**real range**, not the catalogue figure) is the hardest to measure. |
| 🎖️ **Defence** | Fighters, armoured vehicles, drones, logistics base | A 30-year life cycle, irreversible, under public scrutiny. **Unit price is less than 1/3 of total cost.** Technology transfer and cost per hour decide three decades of budget. |
| 🏢 **Corporate** | Supplier, ERP, outsourcing, expansion | A committee that does not agree with itself. **SAPEVO-M** was built exactly for this: it aggregates ordinal judgement from **several decision makers** without requiring prior consensus. |
| 🚀 **Startups** | Project portfolio, capital allocation | Deciding by expected return always elects the riskiest bet — **expected value ignores the tail**. Here risk is a **criterion**, not a footnote on slide 14. |
| 💻 **IT** | Fleet standardisation | The decision multiplies by 200 and lasts 4 years. Battery life and on-site warranty are worth more, in total cost of ownership, than two points of synthetic benchmark. |

</div>

### Cases ready to run

```bash
python3 pipeline.py --listar
```

| # | Case | Domain | Alternatives | Criteria | Verdict | Authorship / source |
|--:|---|---|--:|--:|---|---|
| 1 | `smartphone` | consumer | 6 | 8 | LIKELY 63% | Original modelling |
| 2 | `veiculo_eletrico` | automotive | 7 | 8 | ROBUST 99% | Original modelling |
| 3 | `caca_multifuncao` | defence | 6 | 9 | ROBUST 100% | Original modelling |
| 4 | `blindado` | defence | 5 | 8 | ROBUST 93% | Original modelling |
| 5 | `portfolio_startup` | corporate | 7 | 9 | ROBUST 96% | Original modelling |
| 6 | `estacao_trabalho` | IT | 6 | 8 | ROBUST 98% | Original modelling |
| 7 | `carros_eletricos` | automotive | 38 | 9 | ROBUST 96% | Original modelling |
| 8 | `smartphones_2026` | consumer | 38 | 9 | LIKELY 73% | Original modelling |
| 9 | `tablets` | consumer | 34 | 8 | LIKELY 67% | Original modelling |
| 10 | `smartwatches` | consumer | 31 | 8 | LIKELY 84% | Original modelling |
| 11 | `notebooks` | IT | 32 | 8 | LIKELY 83% | Original modelling |
| 12 | `maquinario_agricola` | agribusiness | 35 | 8 | ROBUST 100% | Original modelling |
| 13 | `sbc_iot` | IT | 33 | 8 | ROBUST 100% | Original modelling |
| 14 | `mineracao_asic` | infrastructure | 31 | 8 | FRAGILE 50% | Original modelling |
| 15 | `minipcs` | IT | 10 | 8 | ROBUST 91% | Original modelling |
| 16 | `impressoras_3d_miniaturas` | manufacturing | 30 | 9 | FRAGILE 48% | Original modelling |
| 17 | `impressoras_3d_producao` | manufacturing | 30 | 9 | FRAGILE 58% | Original modelling |
| 18 | `plotters_formato` | manufacturing | 24 | 9 | ROBUST 96% | Original modelling |
| 19 | `impressoras_3d_miniaturas_triadas` | manufacturing | 13 | 9 | ROBUST 100% | Original modelling |
| 20 | `acoes_b3` 📚 | finance | 20 | 7 | FRAGILE 39% | COSTA, L. S. da · VÁSQUEZ, J. A.; ESCOBAR, J. W.; MANOTAS, D. F. · [DOI](https://doi.org/10.3390/risks10010004) |
| 21 | `fundos_imobiliarios` 📚 | finance | 18 | 8 | LIKELY 85% | SANTOS, V. V. dos (orient. ALMEIDA FILHO, A. T. de) |
| 22 | `fintech` 📚 | finance | 16 | 8 | LIKELY 67% | WIBOWO, S.; GRANDHI, L.; GRANDHI, S.; WELLS, M. · [DOI](https://doi.org/10.3390/math10020225) |
| 23 | `avaliacao_imoveis` 📚 | real estate | 16 | 8 | ROBUST 94% | DUARTE, D. C. de O. · MARQUES, J. P. M. |
| 24 | `ordens_servico` 📚 | operations | 18 | 8 | ROBUST 97% | ALENCAR, L. G. de; TAVARES, F. R. M.; MENDONÇA, F. J. S. de F.; DUARTE, A. K. G. |
| 25 | `cloud_providers` 📚 | IT | 14 | 8 | ROBUST 100% | SOLOMON, T. |
| 26 | `venture_capital` 📚 | corporate | 16 | 8 | ROBUST 96% | BEIM, G.; LÉVESQUE, M. · DHOCHAK, M.; DOLIYA, P. · AFFUL-DADZIE, E.; AFFUL-DADZIE, A.; OPLATKOVÁ, Z. K. · [DOI](https://doi.org/10.1002/mcda.1703) |
| 27 | `instrutores` 📚 | corporate | 15 | 8 | ROBUST 100% | SILVA, C. E. J. da; SALLES-NETO, L. L. de; SANTOS, M. dos |
| 28 | `cripto_portfolio` 📚 | finance | 9 | 7 | ROBUST 100% | ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. · [DOI](https://doi.org/10.3390/math9141677) |
| 29 | `portfolio_crise` 📚 | finance | 8 | 4 | LIKELY 77% | COSTA, I. P. de A.; MAÊDA, S. M. do N.; TEIXEIRA, L. F. H. de S. de B.; GOMES, C. F. S.; SANTOS, M. dos |
| 30 | `cenarios_va` 📚 | automotive | 16 | 9 | LIKELY 73% | LI, S.; ZHOU, R.; HUANG, H. · [DOI](https://doi.org/10.1007/s42154-024-00344-6) |
| 31 | `impressora_3d_energia` 📚 | manufacturing | 12 | 7 | LIKELY 69% | OLIVEIRA, V. A. R. de; ALVARADO SILVA, C. A.; OLIVEIRA, G. C. R. de; TAJIMA, F. M.; FARIA NETO, A. dos R.; SALOMON, V. A. P.; GUIDI, E. S. · [DOI](https://doi.org/10.18687/LACCEI2025.1.1.1193) |
| 32 | `impressoras_juridico` 📚 | operations | 12 | 4 | ROBUST 100% | OLIVEIRA, N. C.; OLIVEIRA, P. F. C. de; GOMES, C. F. S.; SANTOS, M. dos |
| 33 | `fundos_hedge` 📚 | finance | 20 | 8 | ROBUST 94% | SILVA, F. P. da; RIBEIRO, C. de O. |
| 34 | `modelos_previsao` 📚 | IT | 7 | 8 | ROBUST 95% | SHAH, S. |
| 35 | `policultivo_rj` 📚 | agribusiness | 8 | 8 | LIKELY 86% | PENEDO, B. |
| 36 | `parafusadeiras_domesticas` 📚 | consumer | 14 | 8 | LIKELY 70% | COMPROU AVALIOU (canal) · [vídeo](https://youtu.be/pgdqVYEjZtk) |
| 37 | `parafusadeiras_profissionais` 📚 | manufacturing | 12 | 8 | ROBUST 100% | FERRAMENTAS EM AÇÃO — ASSIS PIRES (canal) · [vídeo](https://youtube.com/shorts/9SIs3agoZKc) |
| 38 | `crowdfunding_startups` 📚 | corporate | 16 | 9 | ROBUST 93% | SKARE, M.; GAVUROVA, B.; POLISHCHUK, V. · [DOI](https://doi.org/10.1016/j.jbusres.2023.113719) |

> [!NOTE]
> The case matrices are **illustrative** — public, plausible orders of magnitude to demonstrate the method. What is **not** illustrative is the **modelling**: criteria, directions, the DEMATEL causal matrix and the Saaty matrix. That is where the value lives. **Replace the numbers with your quotation, your tender or your lab test** — the engine is the same; the data is yours.

> [!TIP]
> The **verdict** measures in how many of the 2,000 simulated preference universes the winner keeps winning, perturbing the weights by Dirichlet (κ=200). **ROBUST** ≥ 90%: the choice does not depend on calibration. **LIKELY** 60–89%: the runner-up is competitive, compare both. **FRAGILE** < 60%: first place is an artefact of the weights — and that is a legitimate finding, not a failure. It means the data does not decide, and the decision goes back to the human.

### 📚 Case studies derived from the literature

> [!IMPORTANT]
> The cases in the table below have their **criteria and causal structure taken from the works listed** — peer-reviewed papers, theses, conference proceedings and technical reports. The criteria were not invented: they come from the source text, and authorship is preserved here and in the header of the corresponding module. The **numerical matrices** are our own instantiations — no data from the original works was reproduced. Where an indexed DOI exists, the link points to the work; where it does not, the full textual reference is enough to find it.

| Case | Domain | Authors | Reference |
|---|---|---|---|
| `acoes_b3` | finance | COSTA, L. S. da · VÁSQUEZ, J. A.; ESCOBAR, J. W.; MANOTAS, D. F. | *Uma metodologia para a pré-seleção de ações utilizando o método multicritério TOPSIS* (COSTA, UERJ) · *AHP–TOPSIS Methodology for Stock Portfolio Investments*, Risks, v.10, n.1, 4, 2022 (Universidad del Valle) · [DOI](https://doi.org/10.3390/risks10010004) |
| `fundos_imobiliarios` | finance | SANTOS, V. V. dos (orient. ALMEIDA FILHO, A. T. de) | *Avaliação do método Random Forest para auxílio à seleção de fundos de investimento imobiliário listados na Bolsa de Valores*. Trabalho de Graduação, Engenharia da Computação, CIn/UFPE, set. 2023 |
| `fintech` | finance | WIBOWO, S.; GRANDHI, L.; GRANDHI, S.; WELLS, M. | *A Fuzzy Multicriteria Group Decision Making Approach for Evaluating and Selecting Fintech Projects*. Mathematics, v.10, n.2, 225, 2022 — CQUniversity, Austrália · [DOI](https://doi.org/10.3390/math10020225) |
| `avaliacao_imoveis` | real estate | DUARTE, D. C. de O. · MARQUES, J. P. M. | *Análise multicritério e geoestatística aplicadas na avaliação em massa de imóveis urbanos*. Tese, UFV, 2019 · *As formas de avaliar imóvel em leilão judicial*. Universidade São Judas Tadeu, 2023 |
| `ordens_servico` | operations | ALENCAR, L. G. de; TAVARES, F. R. M.; MENDONÇA, F. J. S. de F.; DUARTE, A. K. G. | *Priorização de ordens de serviço aplicando métodos de tomada de decisão: o AHP integrado ao PROMETHEE*. Revista Produção Online, v.22, n.2, p.2763-2784, 2022 — URCA, Ceará |
| `cloud_providers` | IT | SOLOMON, T. | *Ranking of Cloud Service Providers Using a Dynamic TOPSIS Model for Provisioning of Enterprise IT Infrastructure in the Cloud*. Praxis (Doctor of Engineering), The George Washington University, 2017 |
| `venture_capital` | corporate | BEIM, G.; LÉVESQUE, M. · DHOCHAK, M.; DOLIYA, P. · AFFUL-DADZIE, E.; AFFUL-DADZIE, A.; OPLATKOVÁ, Z. K. | *Selecting projects for venture capital funding: a multiple criteria decision approach* (Case Western Reserve University) · *Valuation of a startup: moving towards strategic approaches*, J. Multi-Criteria Decision Analysis, 2019 · *Assessing commercial viability of technology start-up businesses in a government venture capital under intuitionistic fuzzy environment*, Int. J. Fuzzy Systems, 2016 · [DOI](https://doi.org/10.1002/mcda.1703) · [DOI](https://doi.org/10.1007/s40815-016-0141-9) |
| `instrutores` | corporate | SILVA, C. E. J. da; SALLES-NETO, L. L. de; SANTOS, M. dos | *Modelagem matemática com os métodos AHP e TOPSIS para ordenação de instrutores em uma escola da FAB*. LIV SBPO, Juiz de Fora, 2022 — ITA / UNIFESP / IME |
| `cripto_portfolio` | finance | ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. | *Cryptocurrency Portfolio Selection — A Multicriteria Approach*. Mathematics, v.9, n.14, 1677, 2021 — University of Split, Croácia — **pesos AHP do artigo** · [DOI](https://doi.org/10.3390/math9141677) |
| `portfolio_crise` | finance | COSTA, I. P. de A.; MAÊDA, S. M. do N.; TEIXEIRA, L. F. H. de S. de B.; GOMES, C. F. S.; SANTOS, M. dos | *Finanças em períodos de crise: aplicação do método SAPEVO-M para composição de portfólios de investimentos*. Pesquisa Operacional para o Desenvolvimento, v.13, e13004, 2021 — UFF / CASNAV / IME — **matriz de decisão do artigo** |
| `cenarios_va` | automotive | LI, S.; ZHOU, R.; HUANG, H. | *Multidimensional Evaluation of Autonomous Driving Test Scenarios Based on AHP-EWM-TOPSIS Models*. Automotive Innovation, 2025 · [DOI](https://doi.org/10.1007/s42154-024-00344-6) |
| `impressora_3d_energia` | manufacturing | OLIVEIRA, V. A. R. de; ALVARADO SILVA, C. A.; OLIVEIRA, G. C. R. de; TAJIMA, F. M.; FARIA NETO, A. dos R.; SALOMON, V. A. P.; GUIDI, E. S. | *Multicriteria Analysis for 3D Printer Selection*. 23rd LACCEI International Multi-Conference, Cidade do México, 2025 — UNESP / Universidad César Vallejo · [DOI](https://doi.org/10.18687/LACCEI2025.1.1.1193) |
| `impressoras_juridico` | operations | OLIVEIRA, N. C.; OLIVEIRA, P. F. C. de; GOMES, C. F. S.; SANTOS, M. dos | *Aplicação do método AHP TOPSIS 2N como apoio à tomada de decisão: estudo de caso no departamento jurídico da Secretaria Municipal de Saúde de Duque de Caxias* — UNIGRANRIO / UFF / IME |
| `fundos_hedge` | finance | SILVA, F. P. da; RIBEIRO, C. de O. | *Análise comparativa de fundos de hedge brasileiros utilizando DEA e bootstrap*. XII SIMPEP, Bauru-SP, 2005 — Escola Politécnica da USP |
| `modelos_previsao` | IT | SHAH, S. | *Comparison of Stochastic Forecasting Models*. Stochastic Differential Equations Course Project, Johns Hopkins University — o artigo compara os modelos; a modelagem multicritério sobre eles é deste projeto |
| `policultivo_rj` | agribusiness | PENEDO, B. | *AGTech PoliCultivo 4.0 — Otimização de Portfólio de Cultivos em Ambiente Controlado (RJ)*. Relatório técnico, 03/08/2026, seção 14 — **matriz e pesos do relatório** |
| `parafusadeiras_domesticas` | consumer | COMPROU AVALIOU (canal) | *As 5 Melhores Parafusadeira De 2025*, 14/05/2024 — especificações extraídas da narração · [vídeo](https://youtu.be/pgdqVYEjZtk) |
| `parafusadeiras_profissionais` | manufacturing | FERRAMENTAS EM AÇÃO — ASSIS PIRES (canal) | *As Melhores Parafusadeiras Do Mundo*, 04/01/2024 — modelos e baterias lidos dos quadros do vídeo · [vídeo](https://youtube.com/shorts/9SIs3agoZKc) |
| `crowdfunding_startups` | corporate | SKARE, M.; GAVUROVA, B.; POLISHCHUK, V. | *A decision-making support model for financing start-up projects by venture capital funds on a crowdfunding platform*. Journal of Business Research, v.158, 113719, 2023 — **critérios e escalas do artigo** · [DOI](https://doi.org/10.1016/j.jbusres.2023.113719) |

---

## ⚡ Installation

### Fastest path (Python)

```bash
git clone <url> multicriteriadecisionmodels
cd multicriteriadecisionmodels/public/foundations/pipeline
pip install -r requirements.txt
python3 pipeline.py
```

Done. All six cases run, with a full report.

<details>
<summary><b>Detailed prerequisites</b></summary>

| Component | Minimum version | Required? | What for |
|---|---|---|---|
| Python | 3.10 | ✅ | reference engine |
| NumPy | 2.0 | ✅ | algebra for every method |
| numba | 0.60 | ⚠️ | kernel JIT — without it, same result, slower |
| SciPy | 1.10 | ✅ | auxiliary statistics |
| matplotlib | 3.7 | ✅ | the 5 screens per case |
| Rust / cargo | 1.75 | ⭕ | cross-check engine |
| Node.js | 18 | ⭕ | Evidence dashboard |
| screen | — | ⭕ | background execution |

</details>

### Full pipeline

```bash
./run_all.sh                    # tests → pipeline → screens → i18n → Rust → cross-check
./run_all.sh --rapido           # skips Rust and i18n
./run_all.sh --caso smartphone  # a single case
./run_all.sh --background       # runs in screen (reattach: screen -r mcdm)
```

### Rust engine — binary with no runtime

```bash
cd public/foundations/rust/mcdm_core
cargo test --release
cargo build --release

./target/release/mcdm --exemplo > problema.mcdm
./target/release/mcdm problema.mcdm
./target/release/mcdm problema.mcdm --json
```

### Dashboard

```bash
cd public/foundations/evidence
npm install
npm run dev               # http://localhost:3000
```

<details>
<summary><b>Advanced commands</b></summary>

```bash
python3 pipeline.py caca_multifuncao --workers 8 --iter 5000
python3 testes_nucleo.py
python3 exportar_rust.py
python3 gerar_i18n.py --tudo
python3 gerar_i18n.py --verificar
python3 gerar_graficos.py --workers 6
```

| Variable | Default | Effect |
|---|---|---|
| `MCDM_WORKERS` | auto | `ProcessPoolExecutor` processes |
| `MCDM_NUMBA` | `1` | JIT on; `0` to debug in pure NumPy |
| `MCDM_SEED` | `42` | reproducibility |
| `ROBUSTEZ_ITER` | `2000` | preference universes |
| `ROBUSTEZ_KAPPA` | `200` | Dirichlet concentration (higher = weights stay closer) |
| `MAUT_AVERSAO` | `2.0` | risk aversion (r > 0 = concave) |
| `PROMETHEE_TIPO` | `linear` | preference function (6 available) |

</details>

---

## ⚖️ The ten schools of decision — and why ten

> [!IMPORTANT]
> **Each method is a different theory of what "best" means.** Using only one is choosing the answer along with the question. We run all ten because **agreement among independent theories** is the strongest evidence a decision problem admits.

<div align="center">

| Method | School | What it assumes | When it is **the** right tool | Origin |
|---|---|---|---|---|
| **AHP-TOPSIS 2n** | distance to ideal | full compensation | quantitative criteria, single decision maker | Saaty (1980); Hwang & Yoon (1981) |
| **ELECTRE I** | outranking | incomparability is allowed | **screening**: eliminate the dominated | Roy (1968) |
| **ELECTRE II** | outranking | strong and weak thresholds | complete ranking **with veto** | Roy & Bertier (1971) |
| **PROMETHEE II** | outranking | gradual preference (6 functions) | when "a bit better" ≠ "better" | Brans & Vincke (1985) |
| **MAUT** | utility | additive independence + risk aversion | decision under uncertainty | Keeney & Raiffa (1976) |
| **MCDA-C** | constructivist | anchored Neutral/Good levels | **absolute diagnosis**, not just a ranking | Ensslin, Montibeller & Noronha (2001) |
| **VIKOR** | compromise | group utility × maximum regret | when **compensation is unacceptable** | Opricovic (1979); Opricovic & Tzeng (2002-07) |
| **TODIM** | Prospect Theory | a loss hurts more than an equivalent gain | loss-averse decision maker — **everyone is** | Gomes & Lima (1992); Kahneman & Tversky (1979) |
| **SAPEVO-M** | ordinal multi-decision-maker | ordinal judgement from several decision makers | **a committee that does not agree with itself** | Gomes et al. (1997); Teixeira, Santos & Gomes (2019) |
| **TOPSIS Fuzzy** | Fuzzy | that data has a RANGE, not a point | measurement is imprecise and you want to know whether the ranking survives it | Zadeh (1965); Chen (2000) |

</div>

> [!NOTE]
> **Fuzzy TOPSIS** is not AHP-TOPSIS with noise: besides triangular numbers, it swaps the normalization (linear instead of vector) and the ideal solution (absolute instead of relative). **Diverging from AHP-TOPSIS 2n is the expected behaviour**, and it measures how much the ranking depends on those choices. **Fuzzy AHP** (Buckley) joins as a third source of weights, alongside DEMATEL and AHP: it takes the same pairwise judgement but carries the imprecision to the end — with uniform spread the central value matches AHP's, and what it adds is the **range**, which answers whether the priority order survives the decision maker's own imprecision.

<details>
<summary><b>Why these three deserve special attention</b></summary>

### VIKOR — when compensation is unacceptable
VIKOR computes **two** measures: `S` (group utility — weighted sum, which **accepts** that one terrible score be offset by several good ones) and `R` (maximum individual regret — minimax, which **refuses** compensation).

An armoured vehicle with excellent mobility and terrible protection has a great `S` and an awful `R`. The weighted sum would elect it; VIKOR flags it. And when `S` and `R` disagree, conditions **C1** (acceptable advantage) and **C2** (acceptable stability) explicitly report that the decision has a blind spot.

### TODIM — a loss hurts more than a gain
Based on Kahneman & Tversky's **Prospect Theory**: losing 10 points of range hurts more than gaining 10 pleases. The classic weighted sum ignores this asymmetry and treats gain and loss as symmetric — **which no human decision maker does.** The `θ` factor calibrates how much: `θ < 1` amplifies loss aversion.

### SAPEVO-M — the committee that does not agree
Every other method requires a weight vector. **Where does it come from when five decision makers disagree?** SAPEVO-M solves it at the source: each decision maker expresses **ordinal** preference ("range is much more important than price", on a seven-point scale), and the method aggregates **without requiring a prior consensus ordering**. That is how a committee actually speaks — nobody says "range is worth 0.237".

</details>

### The consensus engine

```
DEMATEL ──► weights by influence ──► 10 methods ──► Borda consensus ──► winner
                                                    │
                        2,000 Dirichlet universes ─────────────────┘
                                    ▼
                     verdict: ROBUSTO / PROVÁVEL / FRÁGIL
```

| Verdict | Confidence | What to do |
|---|---|---|
| 🟢 **ROBUST** | ≥ 90% | The choice does not depend on fine calibration. **You can take it to the committee.** |
| 🟡 **LIKELY** | 60–90% | It holds in most scenarios, but the runner-up is competitive. **Compare both.** |
| 🔴 **FRAGILE** | < 60% | First place is an **artefact of the weights**. Do not decide on the ranking alone: go back to the decision maker and recalibrate. |

---

## 🔬 Two independent engines: the cross-check

> [!TIP]
> **Why reimplement everything in Rust?** Because "the code runs" is not evidence that the **mathematics** is right.

A formula transcription error rarely repeats **identically** in two languages with independent linear algebra. The Python engine uses NumPy/LAPACK; the Rust engine implements Gaussian elimination with partial pivoting and the power method **by hand, with no external dependency whatsoever**.

```bash
python3 exportar_rust.py
```
```
✅ smartphone           8 identical methods · winner=C     (Δ ≤ 4.7e-11)
✅ veiculo_eletrico     8 identical methods · winner=EV6   (Δ ≤ 4.1e-11)
✅ caca_multifuncao     8 identical methods · winner=C3    (Δ ≤ 4.5e-11)
✅ blindado             8 identical methods · winner=B3    (Δ ≤ 4.6e-11)
✅ portfolio_startup    8 identical methods · winner=P3    (Δ ≤ 4.9e-11)
✅ estacao_trabalho     8 identical methods · winner=W5    (Δ ≤ 5.0e-11)
```

**Bonus: the Rust binary needs no Python, no NumPy, no numba and no virtual environment. A few MB that run on a server, a container or an embedded machine — which matters when the engine ships with a system in the field.**

---

## 🚀 Performance: 26× faster, same answer

The robustness analysis runs 2,000 universes × 10 methods. The naive implementation took **42 seconds** per case.

<div align="center">

| Stage | Time | Speed-up |
|---|---|---|
| JIT kernels per universe | 42,33 s | — |
| **Pre-compilation into tensors** | 2,41 s | **17,6×** |
| `ranks` under JIT + per-process state | **1,63 s** | **26,0×** |

</div>

> **The optimisation that paid most was neither parallelism nor JIT.** It was realising that four of the nine methods are **linear in the weight vector** — which allows pre-computing tensors and reducing each universe to a matrix-vector product. **Algebra before infrastructure.**

And the result is **bit-for-bit identical** to the slow path — 100 universes × 10 methods verified on every suite run. An optimisation that changes the result is a bug, not a gain.

<details>
<summary><b>Project execution policy</b></summary>

| Rule | Application |
|---|---|
| **Parallelism** | `ProcessPoolExecutor` for CPU-bound work; never threads (the GIL serialises) |
| **Threshold** | Serial vs. parallel decided by **work** (`n_iter · m² · k`), not item count — parallelising a small problem is **slower** than solving it |
| **JIT** | `numba` with `cache=True` on O(m²k) kernels; degrades to pure NumPy if absent |
| **Background** | `screen`, never `nohup` — allows reattaching and interacting |
| **Reproducibility** | Fixed partitioning, independent of process count: same seed → identical result with 1 or 32 processes |

</details>

---

## 🌐 12 languages — SDL Trados translation memory

This is not machine-translating a README. It is a **localisation pipeline** with a translation memory in the **SDL Trados Studio** standard.

```
translation.memory.md          ← canonical source, versioned in git
   │  --tm
   ▼
strings.<locale>.json          ← consumed artefact
   │  --paginas
   ▼
12 dashboard pages + 12 READMEs
   │  --tmx
   ▼
translation.memory.tmx         ← importable into SDL Trados Studio
```

| Item | Numbers |
|---|---|
| Locales | **12** (pt-BR · en · es · fr · de · zh · ko · hi · **he RTL** · ru · sv · fi) |
| Translation units | 56 |
| Glossary terms (MultiTerm) | 22 |
| Segments in the TMX | **948** |
| Encoding | UTF-8 · LF · NFC |

```bash
python3 gerar_i18n.py --verificar
```

The QA mirrors Trados **Verify**: terminological consistency, preserved placeables, segment coverage, strict encoding and untouched non-translatables — with a rule that differs by writing system (technical acronyms stay Latin in every language; proper names are **transliterated** where the script is not Latin).

---

## 📁 What is inside

```
multicriteriadecisionmodels/
├── README.md (+11)                     showcase in 12 languages
├── docs/                               logo and README screens
│
└── public/foundations/
    ├── pipeline/                       PYTHON ENGINE (reference)
    │   ├── nucleo.py                   DEMATEL · ELECTRE I/II · PROMETHEE II
    │   │                               MAUT · MCDA-C · AHP · TOPSIS 2N
    │   ├── metodos_br.py               SAPEVO-M · VIKOR · TODIM · Copeland
    │   ├── robustez.py                 Dirichlet + ProcessPoolExecutor
    │   ├── pipeline.py                 orchestrator
    │   ├── gerar_graficos.py           5 screens per case
    │   ├── gerar_i18n.py               TM → strings → pages → TMX
    │   ├── testes_nucleo.py            16 mathematical checks
    │   ├── exportar_rust.py            cross-engine check
    │   ├── casos/catalogo.py           6 cases + validation
    │   └── run_all.sh                  pipeline (screen)
    │
    ├── rust/mcdm_core/                 RUST ENGINE (verification + distribution)
    │   └── src/lib.rs                  every method, zero dependencies
    │
    └── evidence/                       DASHBOARD (Evidence.dev)
        ├── sources/mcdm/               11 SQL queries
        └── pages/                      12 language routes
```

---

## 🧠 Foundations

The project is built on reviewed literature, not intuition. The integration architecture follows **John (2025)**, *"Integration of DEMATEL with Other MCDM Methods for Comprehensive Techno-Economic Analysis"*: DEMATEL reveals the causal structure and derives **weights by influence**, which then feed the ranking methods — instead of arbitrated weights.

The methods of the **Brazilian school of Multi-Criteria Decision Aid** (SAPEVO-M, TODIM-FSE, ELECTRE II, VIKOR, ordinal methods) follow the work of **IME**, **UFF**, **CASNAV**, **AMAN** and **FURB** — including real applications in **evaluating drones for naval warfare**, **classifying a brigade logistics base** and **ranking corvettes for the Brazilian Navy**.

> [!NOTE]
> **Authorship of the methods belongs entirely to their creators,** credited individually in the headers of `nucleo.py` and `metodos_br.py`. This project contributes the implementation, the integration and the consensus engine — **not the methods**.

---

## ❓ Questions you are going to ask

<details>
<summary><b>I already use a weighted decision matrix. Isn't that the same thing?</b></summary>

No, for three reasons. **(1)** A weighted matrix is **one** method (weighted sum) with an embedded theory: full compensation. It assumes a terrible score on one criterion can be offset by good scores elsewhere — which is false in safety, in armour protection and in regulatory compliance. **(2)** It assumes independent criteria, and you almost always add up things that are already added up. **(3)** It returns a number with no confidence interval, and so it does not survive the committee's first question.
</details>

<details>
<summary><b>How do I choose the weights?</b></summary>

You do not choose them — **three paths derive them**. **DEMATEL** extracts them from the causal structure you declare (who influences whom). **AHP** extracts them from pairwise comparisons, with a consistency check that **rejects** contradictory judgement. **SAPEVO-M** extracts them from the ordinal judgement of several decision makers. And after that, the robustness analysis asks how much the result still **depends** on them.
</details>

<details>
<summary><b>What if my problem has 200 alternatives?</b></summary>

It runs. The parallelism threshold detects the regime and distributes across processes. Measured: 60 alternatives × 12 criteria × 2,000 universes in 3.8 s with 4 processes. Above roughly 700 alternatives the preference tensor exceeds the configured memory limit and the engine warns you, instead of hanging.
</details>

<details>
<summary><b>The methods disagreed. Now what?</b></summary>

**That is the product, not the problem.** The divergence tells you your decision is sensitive to the school adopted — and names which one. If ELECTRE demotes what everyone else elects, there is a criterion on which that alternative is bad enough to warrant a veto. Take **that** to the committee, not the ranking.
</details>

<details>
<summary><b>Can I use my own data?</b></summary>

That is what it is for. A case is a declarative structure in `casos/catalogo.py`: criteria (with direction and unit), alternatives, decision matrix, DEMATEL causal matrix and Saaty matrix. The validator rejects a malformed case **before** any computation — incoherent dimensions, wrong diagonal, non-reciprocal Saaty matrix, a constant criterion that discriminates nothing.
</details>

---

## 📜 License and authorship

<div align="center">

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="420"/>

**ProfBru © 2026**

**MCDM Studio — Multi-Criteria Decision Models**
Author: **ProfBru - Bruno Penedo** © 2026 — **ALL RIGHTS RESERVED**
📧 profbruanbima@gmail.com

</div>

**Proprietary** project. No license to use, copy, modify, distribute or create derivative works is granted by this repository. Commercial, academic or institutional use requires written authorisation from the author.

**Third-party attribution:** the multi-criteria methods are authored by their respective creators — Saaty, Roy, Bertier, Brans, Vincke, Keeney, Raiffa, Ensslin, Montibeller, Noronha, Gabus, Fontela, Opricovic, Tzeng, Hwang, Yoon, Kahneman, Tversky, Borda, Copeland, Gomes, Lima, Santos, Teixeira, Moreira, Rangel, Neves, Hein, Kroenke, Keunecke and Gomes Júnior — credited individually in the source code.
