<!--
MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
-->

<div align="center">

# 🎯 MCDM Studio — 다기준 의사결정 모델

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="820"/>

**ProfBru © 2026**

### 스프레드시트로 고르는 일을 멈추십시오. 증거로 결정하십시오.

**아홉 개의 의사결정 학파. 하나의 선정안. 그리고 — 처음으로 — 그 선정안이 옳을 확률.**

[![MCDM](https://img.shields.io/badge/MCDM_방법-9-2563eb?style=for-the-badge)](#-아홉-개의-의사결정-학파--그리고-왜-아홉인가)
[![Engines](https://img.shields.io/badge/엔진-Python_+_Rust-c2410c?style=for-the-badge)](#-두-개의-독립-엔진-교차-검증)
[![i18n](https://img.shields.io/badge/언어-12-16a34a?style=for-the-badge)](#-12개-언어--sdl-trados-번역-메모리)
[![Robustez](https://img.shields.io/badge/시뮬레이션_세계-2.000-8f3d56?style=for-the-badge)](#-아무도-답하지-않는-질문-가중치가-틀렸다면)

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Rust](https://img.shields.io/badge/Rust-1.96-000000?logo=rust&logoColor=white)](https://www.rust-lang.org)
[![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?logo=numpy&logoColor=white)](https://numpy.org)
[![Numba](https://img.shields.io/badge/Numba-JIT-00A3E0?logo=numba&logoColor=white)](https://numba.pydata.org)
[![Evidence](https://img.shields.io/badge/Evidence.dev-Dashboard-f4b548)](https://evidence.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/라이선스-독점-red)](#-라이선스와-저작권)

🌐 [Português](README.md) · [English](README.en.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [中文](README.zh.md) · **한국어** · [हिन्दी](README.hi.md) · [עברית](README.he.md) · [Русский](README.ru.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md)

</div>

---

## 💀 고통: 당신은 이미 스프레드시트 때문에 돈을 잃었다

마지막으로 내린 값비싼 결정을 떠올려 보십시오. 자동차 구매. 공급업체 선정. 프로젝트 승인. 200명이 4년 동안 쓸 노트북 확정.

**당신은 스프레드시트를 열었습니다. 행에는 선택지, 열에는 속성. 그리고 다음 세 가지 중 하나를 했습니다:**

| 당신이 한 일 | 실제로 벌어진 일 |
|---|---|
| 🔻 **가격 열로 정렬했다** | 가장 싼 것을 골랐습니다. 그러려고 스프레드시트가 필요하지는 않았습니다. |
| 🔺 **전문가 점수로 정렬했다** | 가장 비싼 것을 골랐습니다. 그것 역시 필요 없었습니다. |
| 🔍 **“모든 요구사항 충족”으로 필터링했다** | 목록이 비었습니다. 그래서 요구사항 하나를 완화했습니다. 어느 것을? **걸림돌이 되던 그것을.** |

> [!WARNING]
> **세 가지 조작 모두 같은 결함을 지닙니다: 어느 것도 당신이 던진 질문에 답하지 않습니다.**
> 질문은 *“서로 모순되는 선택지들 가운데 무엇을 고를 것인가?”*였습니다 — 그런데 한 열로 정렬하는 것은 정의상 **하나의** 기준으로 결정하는 일입니다. 나머지 일곱 개는 쓰지 않았습니다. 그것들은 당신의 마음을 편하게 하려고 거기 있었을 뿐입니다.

그리고 아무도 보지 못하는 문제가 있습니다: **당신은 이미 더해진 것을 또 더했습니다.** “에너지 소비”에 20%, “주행거리”에 25%를 주었지만 — 소비가 주행거리를 *유발*합니다. 같은 것을 두 번 세고 그것을 분석이라 불렀습니다.

### 의사결정이 죽는 순간

회의에서 벌어집니다. 당신이 순위를 발표합니다. 위원회의 누군가가 묻습니다:

> *주행거리가 25%가 아니라 30%라면요?*

그리고 당신은 모릅니다. **아무도 모릅니다.** 스프레드시트는 가질 수 없는 100%의 암묵적 신뢰도를 달고 **하나의** 숫자를 돌려주기 때문입니다. 숙제를 하고 돌아와 가중치를 조정하면, 2위가 **2퍼센트포인트** 차이로 1위가 되는 것을 발견합니다.

그 “선정안”은 애초에 선정안이 아니었습니다. 그것은 **당신 보정의 산물**이었고 — 당신은 하마터면 서명할 뻔했습니다.

---

## 💊 해법: 아홉 학파, 하나의 합의, 그리고 신뢰구간

**MCDM Studio는 같은 문제에 대해 **정립된 아홉 가지 다기준 방법**을 실행하고, 그 사이의 **합의**로부터 선정안을 도출한 뒤, 정말 중요한 단 한 가지를 수행합니다:**

> ### 🎲 가중치를 **2,000번** 교란하고, 몇 개의 세계에서 그 선정안이 계속 이기는지 셉니다.

판정은 더 이상 숫자가 아니라 **위원회에서 살아남는 문장**이 됩니다:

<div align="center">

| ❌ 스프레드시트가 말하는 것 | ✅ MCDM Studio가 말하는 것 |
|---|---|
| “모델 C가 최고입니다.” | **“모델 C는 타당한 선호 세계의 96%에서 승리합니다. 판정 견고: 이 선택은 가중치의 미세 보정에 의존하지 않습니다.”** |
| *(답 없음)* | **“모델 A는 51%에서 승리합니다. 판정 취약: 1위는 가중치의 산물입니다. 순위만으로 결정하지 마십시오.”** |

</div>

**두 번째 경우를 보십시오. 정직한 시스템은 *“여기서는 나를 믿지 마시오”*라고 말할 수 있어야 합니다. 그것이 의사결정 지원과, 이미 내리고 싶었던 결정을 정당화해 주는 생성기 사이의 차이입니다.**

---

## 🖼️ 작동하는 모습 보기

### 1. 무엇이 원인이고 무엇이 결과인가 — 가중치를 주기 전에

<div align="center"><img src="docs/telas/caca_multifuncao/dematel_causa_efeito.png" alt="DEMATEL" width="820"/></div>

**이것이 해결하는 고통:** 당신은 기준들이 독립이라고 가정하고 가중치를 부여합니다. **거의 결코 독립이 아닙니다.** 에너지 소비가 주행거리를 *유발*합니다. 장갑이 중량을 *유발*하고, 중량이 기동성 저하를 *유발*합니다. 이를 독립인 양 더하는 것은 이중 계산입니다.

**DEMATEL**은 총관계행렬 `T = X(I−X)⁻¹`을 구성합니다 — 이는 경로 길이에 상관없이 직접 **및 간접** 영향을 합산합니다 — 그리고 당신이 **당길 수 있는 것**(원인, 선 위)과 단지 **결과를 측정하는 것**(결과, 선 아래)을 분리합니다. 가중치는 여기서 나옵니다: 감이 아니라 시스템적 영향으로부터.

> 위 사례에서 **기술이전**과 **레이더 반사면적**은 원인입니다: 이들을 움직이면 시스템 전체가 움직입니다. **함대 가동률**은 결과입니다 — 지렛대가 아니라 온도계입니다. 가동률에 점수를 매기면서 기술이전을 무시하는 입찰공고는 열을 재면서 감염을 무시하는 것입니다.

### 2. 같은 문제에 대한 아홉 학파

<div align="center"><img src="docs/telas/veiculo_eletrico/mapa_metodos.png" alt="Métodos" width="900"/></div>

**이것이 해결하는 고통:** 모든 MCDM 방법에는 “더 낫다”가 무엇을 뜻하는지에 관한 이론이 내장되어 있으며 — 그것이 선정안을 바꿉니다. 방법 하나를 고르고 결과를 제시하는 것은 결과를 고르는 일입니다.

우리는 아홉 가지를 모두 실행합니다. 일치할 때 그 선택은 **방법의 산물이 아닙니다**. 갈릴 때는 **그 갈림 자체가 발견**입니다.

> 위: **플러그인 하이브리드**는 일곱 방법에서 1위지만 **ELECTRE I에서는 6위**입니다. 잡음이 아니라 정보입니다. ELECTRE I은 *거부권*을 허용합니다: 다른 면이 아무리 좋아도, 어떤 기준에서 탈락시킬 만큼 심각한 열위가 있다고 말하는 것입니다. **바로 그것이 위원회에 가져가고 싶은 질문입니다.**

### 3. 의사결정 자체의 신뢰구간

<div align="center"><img src="docs/telas/portfolio_startup/robustez.png" alt="Robustez" width="820"/></div>

**이것이 해결하는 고통:** 위원회의 질문 — *“가중치가 달랐다면?”*. 누군가 묻기 **전에** 이미 답해 둡니다.

`w' ~ Dirichlet(κ·w)`로 가중치를 교란하고 2,000번 재순위화합니다. 디리클레는 자연스러운 선택입니다: 그 지지집합이 정확히 심플렉스(합이 1인 양의 가중치)이며 `E[w'] = w`를 만족합니다 — 즉 **편향 없이** 교란합니다.

### 4. 당신의 직관이 틀린 지점

<div align="center"><img src="docs/telas/blindado/pesos_dematel_ahp.png" alt="DEMATEL x AHP" width="820"/></div>

**이것이 해결하는 고통:** 당신은 무엇이 중요한지 안다고 생각합니다. 두 가지 가중치 계열이 그것을 시험합니다.

**AHP**(Saaty)는 쌍대비교로 한 기준이 다른 기준보다 얼마나 더 중요한지 묻습니다. **DEMATEL**은 시스템적 영향을 측정합니다. **둘이 갈리는 지점이 바로 당신이 과소평가한 2차 효과입니다** — 그래프는 가장 큰 괴리를 빨간색으로 표시합니다.

### 5. 2,000개 시나리오에서 각 대안이 도달하는 자리

<div align="center"><img src="docs/telas/estacao_trabalho/distribuicao_posicoes.png" alt="Distribuição" width="820"/></div>

전부 초록인 막대는 **가중치에 의존하지 않는** 순위입니다. 얼룩진 막대는 다투는 순위입니다. 순위 중 어디가 사실이고 어디가 의견인지 한눈에 보입니다.

---

## 🎯 어디에 쓰는가 — 맞춤형 선택

엔진은 **도메인에 독립적**입니다: 단위는 *의사결정 사례*(대안 × 기준)이며 업무 의미가 내장되어 있지 않습니다. 도메인을 바꾸는 것은 데이터를 바꾸는 일이지 코드를 바꾸는 일이 아닙니다.

<div align="center">

| 영역 | 결정 대상 | 구체적 고통 |
|---|---|---|
| 📱 **전자제품** | 휴대폰, 노트북, 장비 | 가장 싼 것이 카메라가 가장 나쁘고, 카메라가 가장 좋은 것이 배터리가 가장 나쁩니다. “최고”는 없습니다 — **당신의 용도에 최고인 것**이 있을 뿐입니다. |
| 🚗 **전기차** | 차량 운용 또는 개인 사용 | 주행거리, 충전, 서비스망, 잔존가치가 서로 반대 방향으로 당깁니다. 그리고 결정적 기준(**카탈로그 수치가 아닌 실주행거리**)이 가장 측정하기 어렵습니다. |
| 🎖️ **국방** | 전투기, 장갑차, 드론, 병참기지 | 30년 수명주기, 되돌릴 수 없고, 공적 감시 아래 놓입니다. **단가는 총비용의 3분의 1도 되지 않습니다.** 기술이전과 시간당 비용이 30년치 예산을 결정합니다. |
| 🏢 **기업** | 공급업체, ERP, 외주, 확장 | 스스로 합의하지 못하는 위원회. **SAPEVO-M**은 바로 이를 위해 만들어졌습니다: 사전 합의를 요구하지 않고 **여러 의사결정자**의 서수적 판단을 집계합니다. |
| 🚀 **스타트업** | 프로젝트 포트폴리오, 자본 배분 | 기대수익으로 결정하면 언제나 가장 위험한 베팅이 선택됩니다 — **기댓값은 꼬리를 무시합니다**. 여기서 위험은 **기준**이지, 14번 슬라이드의 각주가 아닙니다. |
| 💻 **IT** | 장비 표준화 | 이 결정은 200배로 곱해지고 4년간 지속됩니다. 총소유비용 관점에서 배터리 지속시간과 방문 보증은 합성 벤치마크 2점보다 가치가 큽니다. |

</div>

### 바로 실행 가능한 사례

```bash
python3 pipeline.py --listar
```

| # | 사례 | 영역 | 대안 | 기준 | 판정 |
|--:|---|---|--:|--:|---|
| 1 | `smartphone` | 소비재 | 6 | 8 | 유력 85% |
| 2 | `veiculo_eletrico` | 자동차 | 7 | 8 | 견고 96% |
| 3 | `caca_multifuncao` | 국방 | 6 | 9 | 견고 100% |
| 4 | `blindado` | 국방 | 5 | 8 | 견고 90% |
| 5 | `portfolio_startup` | 기업 | 7 | 9 | 견고 97% |
| 6 | `estacao_trabalho` | IT | 6 | 8 | 견고 98% |
| 7 | `carros_eletricos` | 자동차 | 38 | 9 | 견고 99% |
| 8 | `smartphones_2026` | 소비재 | 38 | 9 | 유력 65% |
| 9 | `tablets` | 소비재 | 34 | 8 | 유력 62% |
| 10 | `smartwatches` | 소비재 | 31 | 8 | 유력 79% |
| 11 | `notebooks` | IT | 32 | 8 | 유력 76% |
| 12 | `maquinario_agricola` | 농업 | 35 | 8 | 견고 100% |
| 13 | `sbc_iot` | IT | 33 | 8 | 견고 100% |
| 14 | `mineracao_asic` | 인프라 | 31 | 8 | 취약 51% |
| 15 | `minipcs` | IT | 10 | 8 | 견고 96% |
| 16 | `impressoras_3d_miniaturas` | 제조 | 30 | 9 | 취약 35% |
| 17 | `impressoras_3d_producao` | 제조 | 30 | 9 | 취약 45% |
| 18 | `plotters_formato` | 제조 | 24 | 9 | 유력 86% |
| 19 | `impressoras_3d_miniaturas_triadas` | 제조 | 13 | 9 | 견고 100% |
| 20 | `acoes_b3` 📚 | 금융 | 20 | 7 | 취약 52% |
| 21 | `fundos_imobiliarios` 📚 | 금융 | 18 | 8 | 유력 61% |
| 22 | `fintech` 📚 | 금융 | 16 | 8 | 유력 78% |
| 23 | `avaliacao_imoveis` 📚 | 부동산 | 16 | 8 | 견고 96% |
| 24 | `ordens_servico` 📚 | 운영 | 18 | 8 | 견고 92% |
| 25 | `cloud_providers` 📚 | IT | 14 | 8 | 견고 100% |
| 26 | `venture_capital` 📚 | 기업 | 16 | 8 | 견고 97% |
| 27 | `instrutores` 📚 | 기업 | 15 | 8 | 견고 100% |
| 28 | `cripto_portfolio` 📚 | 금융 | 9 | 7 | 견고 100% |
| 29 | `portfolio_crise` 📚 | 금융 | 8 | 4 | 유력 71% |
| 30 | `cenarios_va` 📚 | 자동차 | 16 | 9 | 유력 75% |
| 31 | `impressora_3d_energia` 📚 | 제조 | 12 | 7 | 유력 80% |
| 32 | `impressoras_juridico` 📚 | 운영 | 12 | 4 | 견고 100% |
| 33 | `fundos_hedge` 📚 | 금융 | 20 | 8 | 견고 98% |
| 34 | `modelos_previsao` 📚 | IT | 7 | 8 | 유력 74% |
| 35 | `policultivo_rj` 📚 | 농업 | 8 | 8 | 견고 100% |

> [!NOTE]
> 사례 행렬은 **예시**입니다 — 방법을 보여 주기 위한 공개적이고 타당한 크기 수준입니다. **예시가 아닌 것**은 **모델링**입니다: 기준, 방향, DEMATEL 인과행렬, Saaty 행렬. 가치는 거기에 있습니다. **숫자를 당신의 견적서, 입찰공고, 실험 결과로 바꾸십시오** — 엔진은 같고, 데이터는 당신의 것입니다.

> [!TIP]
> **판정**은 가중치를 디리클레(κ=200)로 교란한 2,000개의 모의 선호 세계 중 몇 곳에서 우승자가 계속 이기는지를 측정합니다. **견고** ≥ 90%: 선택이 보정에 의존하지 않습니다. **유력** 60–89%: 차점자가 경쟁력이 있으니 둘을 비교하십시오. **취약** < 60%: 1위는 가중치가 만든 산물입니다 — 이는 실패가 아니라 정당한 발견입니다. 데이터가 결정하지 못하므로 결정이 사람에게 돌아간다는 뜻입니다.

### 📚 문헌에서 도출한 사례 연구

> [!IMPORTANT]
> 여덟 개 사례는 **기준과 인과 구조를 동료 심사 논문 및 학위논문에서 가져왔습니다** — 주식, 부동산 펀드, 핀테크, 부동산 감정, 정비 작업지시, 클라우드 사업자, 벤처 캐피털, 강사 순위. 기준은 지어낸 것이 아니라 원문에서 온 것이며, 각 연구의 저작자 정보는 해당 모듈 헤더에 보존되어 있습니다. **수치 행렬**은 자체 구성으로, 원 논문의 데이터는 재현하지 않았습니다.

| 사례 | 영역 | 출처 및 저작자 |
|---|---|---|
| `acoes_b3` | 금융 | COSTA, L. S. *Uma metodologia para a pré-seleção de ações utilizando o método multicritério TOPSIS*; *AHP–TOPSIS Methodology for Stock Portfolio Investments*, Risks 10(4):4, 2022 |
| `fundos_imobiliarios` | 금융 | SANTOS, V. V. *TCC*, Engenharia da Computação, UFPE |
| `fintech` | 금융 | *A Fuzzy Multicriteria Group Decision Making Approach for Evaluating and Selecting Fintech Projects* |
| `avaliacao_imoveis` | 부동산 | DUARTE, D. C. O. *Análise multicritério e geoestatística aplicadas na avaliação de imóveis*; MARQUES, J. P. M. |
| `ordens_servico` | 운영 | *Priorização de ordens de serviço: o AHP integrado ao PROMETHEE*. Revista Produção Online, v.22, n.2, 2022 |
| `cloud_providers` | IT | SOLOMON. *Ranking of Cloud Service Providers Using a Dynamic TOPSIS Model*. The George Washington University |
| `venture_capital` | 기업 | BEIM, G.; LÉVESQUE, M.; DHOCHAK, M. et al. (2019); AFFUL-DADZIE, E. et al.; MILKOVA/ANDREICHIKOV (IJAHP) |
| `instrutores` | 기업 | *Modelagem matemática com os métodos AHP e TOPSIS para ordenação de instrutores em uma escola da FAB*. LIV SBPO, 2022 |
| `cripto_portfolio` | 금융 | ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. *Cryptocurrency Portfolio Selection — A Multicriteria Approach*. Mathematics, 9(14):1677, 2021 — **pesos AHP do artigo** |
| `portfolio_crise` | 금융 | COSTA, I. P. A.; MAÊDA, S. M. N.; TEIXEIRA, L. F. H. S. B.; GOMES, C. F. S.; SANTOS, M. *Finanças em períodos de crise: aplicação do método SAPEVO-M*. Pesquisa Operacional para o Desenvolvimento, v.13, e13004, 2021 — **matriz de decisão do artigo** |
| `cenarios_va` | 자동차 | LI, S.; ZHOU, R.; HUANG, H. *Multidimensional Evaluation of Autonomous Driving Test Scenarios Based on AHP-EWM-TOPSIS Models*. Automotive Innovation, 2025 |
| `impressora_3d_energia` | 제조 | OLIVEIRA, V. A. R. et al. *Multicriteria Analysis for 3D Printer Selection*. 23rd LACCEI, Cidade do México, 2025 — UNESP |
| `impressoras_juridico` | 운영 | OLIVEIRA, N. C.; OLIVEIRA, P. F. C.; GOMES, C. F. S.; SANTOS, M. *Aplicação do método AHP TOPSIS 2N: estudo de caso no departamento jurídico da Secretaria Municipal de Saúde de Duque de Caxias*, 2019 |
| `fundos_hedge` | 금융 | SILVA, F. P.; RIBEIRO, C. O. *Análise comparativa de fundos de hedge brasileiros utilizando DEA e bootstrap*. XII SIMPEP, Bauru-SP, 2005 — USP |
| `modelos_previsao` | IT | SHAH, S. *Comparison of Stochastic Forecasting Models*. Johns Hopkins University — o artigo compara os modelos; a modelagem multicritério é deste projeto |
| `policultivo_rj` | 농업 | *AGTech PoliCultivo 4.0 — Otimização de Portfólio de Cultivos (RJ)*, relatório técnico, 03/08/2026, seção 14 — **matriz e pesos do relatório** |

---

## ⚡ 설치

### 가장 빠른 경로 (Python)

```bash
git clone <url> multicriteriadecisionmodels
cd multicriteriadecisionmodels/public/foundations/pipeline
pip install -r requirements.txt
python3 pipeline.py
```

끝입니다. 여섯 사례가 모두 실행되며 완전한 보고서가 나옵니다.

<details>
<summary><b>상세 사전 요구사항</b></summary>

| 구성요소 | 최소 버전 | 필수? | 용도 |
|---|---|---|---|
| Python | 3.10 | ✅ | 기준 엔진 |
| NumPy | 2.0 | ✅ | 모든 방법의 대수 연산 |
| numba | 0.60 | ⚠️ | 커널 JIT — 없어도 결과는 같고 더 느릴 뿐 |
| SciPy | 1.10 | ✅ | 보조 통계 |
| matplotlib | 3.7 | ✅ | 사례당 5개 화면 |
| Rust / cargo | 1.75 | ⭕ | 교차 검증 엔진 |
| Node.js | 18 | ⭕ | Evidence 대시보드 |
| screen | — | ⭕ | 백그라운드 실행 |

</details>

### 전체 파이프라인

```bash
./run_all.sh                    # 테스트 → 파이프라인 → 화면 → i18n → Rust → 대조
./run_all.sh --rapido           # Rust와 i18n 건너뜀
./run_all.sh --caso smartphone  # 단일 사례
./run_all.sh --background       # screen에서 실행 (재접속: screen -r mcdm)
```

### Rust 엔진 — 런타임 없는 바이너리

```bash
cd public/foundations/rust/mcdm_core
cargo test --release
cargo build --release

./target/release/mcdm --exemplo > problema.mcdm
./target/release/mcdm problema.mcdm
./target/release/mcdm problema.mcdm --json
```

### 대시보드

```bash
cd public/foundations/evidence
npm install
npm run dev               # http://localhost:3000
```

<details>
<summary><b>고급 명령</b></summary>

```bash
python3 pipeline.py caca_multifuncao --workers 8 --iter 5000
python3 testes_nucleo.py
python3 exportar_rust.py
python3 gerar_i18n.py --tudo
python3 gerar_i18n.py --verificar
python3 gerar_graficos.py --workers 6
```

| 변수 | 기본값 | 효과 |
|---|---|---|
| `MCDM_WORKERS` | auto | `ProcessPoolExecutor` 프로세스 수 |
| `MCDM_NUMBA` | `1` | JIT 켬; `0`이면 순수 NumPy로 디버깅 |
| `MCDM_SEED` | `42` | 재현성 |
| `ROBUSTEZ_ITER` | `2000` | 선호 세계 수 |
| `ROBUSTEZ_KAPPA` | `200` | 디리클레 집중도 (클수록 가중치가 원래 값에 가까움) |
| `MAUT_AVERSAO` | `2.0` | 위험 회피 (r > 0이면 오목) |
| `PROMETHEE_TIPO` | `linear` | 선호 함수 (6종) |

</details>

---

## ⚖️ 아홉 개의 의사결정 학파 — 그리고 왜 아홉인가

> [!IMPORTANT]
> **각 방법은 “더 낫다”가 무엇을 뜻하는지에 관한 서로 다른 이론입니다.** 하나만 쓰는 것은 질문과 함께 답을 고르는 일입니다. 아홉 가지를 모두 실행하는 이유는 **독립적인 이론들 사이의 일치**야말로 의사결정 문제가 허용하는 가장 강한 증거이기 때문입니다.

<div align="center">

| 방법 | 학파 | 전제 | **바로 이** 도구가 맞는 때 | 출처 |
|---|---|---|---|---|
| **AHP-TOPSIS 2n** | 이상해까지의 거리 | 완전 보상 | 정량 기준, 단일 의사결정자 | Saaty (1980); Hwang & Yoon (1981) |
| **ELECTRE I** | 우위관계 | 비교불가능 허용 | **선별**: 지배당한 것을 제거 | Roy (1968) |
| **ELECTRE II** | 우위관계 | 강·약 임계값 | **거부권이 있는** 완전 순위 | Roy & Bertier (1971) |
| **PROMETHEE II** | 우위관계 | 점진적 선호 (6개 함수) | “조금 더 낫다” ≠ “더 낫다”일 때 | Brans & Vincke (1985) |
| **MAUT** | 효용 | 가법적 독립 + 위험 회피 | 불확실성 하의 의사결정 | Keeney & Raiffa (1976) |
| **MCDA-C** | 구성주의 | 고정된 중립/양호 수준 | 순위가 아닌 **절대적 진단** | Ensslin, Montibeller & Noronha (2001) |
| **VIKOR** | 절충 | 집단 효용 × 최대 후회 | **보상이 용납되지 않을** 때 | Opricovic (1979); Opricovic & Tzeng (2002-07) |
| **TODIM** | 전망이론 | 손실이 같은 크기의 이득보다 더 아프다 | 손실 회피적 의사결정자 — **모두가 그렇다** | Gomes & Lima (1992); Kahneman & Tversky (1979) |
| **SAPEVO-M** | 다의사결정자 서수법 | 여러 의사결정자의 서수적 판단 | **스스로 합의하지 못하는 위원회** | Gomes et al. (1997); Teixeira, Santos & Gomes (2019) |

</div>

<details>
<summary><b>이 셋이 특별한 주목을 받는 이유</b></summary>

### VIKOR — 보상이 용납되지 않을 때
VIKOR는 **두 가지** 척도를 계산합니다: `S`(집단 효용 — 가중합으로, 형편없는 성능 하나가 여러 좋은 성능으로 상쇄되는 것을 **허용**)와 `R`(최대 개별 후회 — 미니맥스로, 보상을 **거부**).

기동성은 뛰어나고 방호력은 형편없는 장갑차는 `S`가 훌륭하고 `R`이 끔찍합니다. 가중합은 그것을 선택하지만 VIKOR는 경고합니다. 그리고 `S`와 `R`이 어긋날 때, 조건 **C1**(수용 가능한 우위)과 **C2**(수용 가능한 안정성)가 그 결정에 사각지대가 있음을 명시적으로 알립니다.

### TODIM — 손실이 이득보다 더 아프다
Kahneman과 Tversky의 **전망이론**에 기반합니다: 주행거리 10점을 잃는 아픔이 10점을 얻는 기쁨보다 큽니다. 고전적 가중합은 이 비대칭을 무시하고 이득과 손실을 대칭으로 취급합니다 — **어떤 인간 의사결정자도 그렇게 하지 않습니다.** 계수 `θ`가 그 정도를 조절합니다: `θ < 1`은 손실 회피를 증폭합니다.

### SAPEVO-M — 합의하지 못하는 위원회
다른 모든 방법은 가중치 벡터를 요구합니다. **의견이 다른 다섯 명의 의사결정자가 있을 때 그것은 어디서 오는가?** SAPEVO-M은 근원에서 해결합니다: 각 의사결정자가 **서수적** 선호를 표현하고(“주행거리가 가격보다 훨씬 중요하다”, 7점 척도), 방법은 **사전 합의 순서를 요구하지 않고** 집계합니다. 위원회는 실제로 그렇게 말합니다 — 아무도 “주행거리는 0.237의 가치”라고 말하지 않습니다.

</details>

### 합의 엔진

```
DEMATEL ──► 영향력 기반 가중치 ──► 9개 방법 ──► 보르다 합의 ──► 선정안
                                                    │
                        2,000개 디리클레 세계 ─────────────────┘
                                    ▼
                     판정: ROBUSTO / PROVÁVEL / FRÁGIL
```

| 판정 | 신뢰도 | 해야 할 일 |
|---|---|---|
| 🟢 **견고** | ≥ 90% | 이 선택은 미세 보정에 의존하지 않습니다. **위원회에 상정할 수 있습니다.** |
| 🟡 **유력** | 60–90% | 대부분의 시나리오에서 유지되지만 2위가 경쟁력 있습니다. **둘을 비교하십시오.** |
| 🔴 **취약** | < 60% | 1위는 **가중치의 산물**입니다. 순위만으로 결정하지 말고 의사결정자에게 돌아가 재보정하십시오. |

---

## 🔬 두 개의 독립 엔진: 교차 검증

> [!TIP]
> **왜 전부 Rust로 다시 구현하는가?** “코드가 돌아간다”는 것이 **수학**이 옳다는 증거는 아니기 때문입니다.

수식 전사 오류가 선형대수가 독립적인 두 언어에서 **똑같이** 반복되는 일은 드뭅니다. Python 엔진은 NumPy/LAPACK을 사용하고, Rust 엔진은 부분 피벗팅 가우스 소거법과 거듭제곱법을 **외부 의존성 없이 직접** 구현합니다.

```bash
python3 exportar_rust.py
```
```
✅ smartphone           8 개 방법 동일 · 선정안=C     (Δ ≤ 4.7e-11)
✅ veiculo_eletrico     8 개 방법 동일 · 선정안=EV6   (Δ ≤ 4.1e-11)
✅ caca_multifuncao     8 개 방법 동일 · 선정안=C3    (Δ ≤ 4.5e-11)
✅ blindado             8 개 방법 동일 · 선정안=B3    (Δ ≤ 4.6e-11)
✅ portfolio_startup    8 개 방법 동일 · 선정안=P3    (Δ ≤ 4.9e-11)
✅ estacao_trabalho     8 개 방법 동일 · 선정안=W5    (Δ ≤ 5.0e-11)
```

**덤: Rust 바이너리는 Python도, NumPy도, numba도, 가상환경도 필요 없습니다. 서버·컨테이너·임베디드 장비에서 도는 수 MB — 엔진이 현장 시스템과 함께 배포될 때 중요한 점입니다.**

---

## 🚀 성능: 26배 빠르게, 같은 답

견고성 분석은 2,000개 세계 × 9개 방법을 실행합니다. 소박한 구현은 사례당 **42초**가 걸렸습니다.

<div align="center">

| 단계 | 시간 | 속도 향상 |
|---|---|---|
| 세계마다 JIT 커널 | 42,33 s | — |
| **텐서로 사전 컴파일** | 2,41 s | **17,6×** |
| `ranks` JIT + 프로세스별 상태 | **1,63 s** | **26,0×** |

</div>

> **가장 큰 이득을 준 최적화는 병렬화도 JIT도 아니었습니다.** 아홉 방법 중 넷이 **가중치 벡터에 대해 선형**임을 알아챈 것이었습니다 — 덕분에 텐서를 미리 계산해 각 세계를 행렬-벡터 곱 하나로 줄일 수 있었습니다. **인프라보다 대수가 먼저입니다.**

그리고 결과는 느린 경로와 **비트 단위로 동일**합니다 — 스위트를 실행할 때마다 100개 세계 × 9개 방법을 검증합니다. 결과를 바꾸는 최적화는 이득이 아니라 결함입니다.

<details>
<summary><b>프로젝트 실행 정책</b></summary>

| 규칙 | 적용 |
|---|---|
| **병렬화** | CPU 바운드 작업에는 `ProcessPoolExecutor`; 스레드는 절대 사용하지 않음 (GIL이 직렬화) |
| **임계값** | 직렬/병렬은 항목 수가 아니라 **작업량**(`n_iter · m² · k`)으로 결정 — 작은 문제를 병렬화하는 것은 그냥 푸는 것보다 **느림** |
| **JIT** | O(m²k) 커널에 `cache=True`를 준 `numba`; 없으면 순수 NumPy로 격하 |
| **백그라운드** | `nohup`이 아니라 `screen` — 재접속과 상호작용이 가능 |
| **재현성** | 프로세스 수와 무관한 고정 분할: 같은 시드 → 1개든 32개든 동일한 결과 |

</details>

---

## 🌐 12개 언어 — SDL Trados 번역 메모리

README를 기계 번역하는 것이 아닙니다. **SDL Trados Studio** 표준의 번역 메모리를 갖춘 **현지화 파이프라인**입니다.

```
translation.memory.md          ← 정본 소스, git으로 버전 관리
   │  --tm
   ▼
strings.<locale>.json          ← 소비되는 산출물
   │  --paginas
   ▼
대시보드 12개 페이지 + README 12개
   │  --tmx
   ▼
translation.memory.tmx         ← SDL Trados Studio로 가져오기 가능
```

| 항목 | 수치 |
|---|---|
| 로케일 | **12** (pt-BR · en · es · fr · de · zh · ko · hi · **he RTL** · ru · sv · fi) |
| 번역 단위 | 56 |
| 용어집 항목 (MultiTerm) | 22 |
| TMX 내 세그먼트 | **948** |
| 인코딩 | UTF-8 · LF · NFC |

```bash
python3 gerar_i18n.py --verificar
```

QA는 Trados의 **Verify**를 재현합니다: 용어 일관성, 플레이서블 보존, 세그먼트 커버리지, 엄격한 인코딩, 비번역 요소 보존 — 문자 체계에 따라 규칙을 달리합니다(기술 약어는 어떤 언어에서도 라틴 문자를 유지하고, 고유명사는 비라틴 문자권에서 **음역**).

---

## 📁 내부 구성

```
multicriteriadecisionmodels/
├── README.md (+11)                     12개 언어 쇼케이스
├── docs/                               로고와 README용 화면
│
└── public/foundations/
    ├── pipeline/                       PYTHON 엔진 (기준 구현)
    │   ├── nucleo.py                   DEMATEL · ELECTRE I/II · PROMETHEE II
    │   │                               MAUT · MCDA-C · AHP · TOPSIS 2N
    │   ├── metodos_br.py               SAPEVO-M · VIKOR · TODIM · Copeland
    │   ├── robustez.py                 디리클레 + ProcessPoolExecutor
    │   ├── pipeline.py                 오케스트레이터
    │   ├── gerar_graficos.py           사례당 5개 화면
    │   ├── gerar_i18n.py               TM → 문자열 → 페이지 → TMX
    │   ├── testes_nucleo.py            16개 수학적 검증
    │   ├── exportar_rust.py            엔진 간 대조
    │   ├── casos/catalogo.py           6개 사례 + 검증
    │   └── run_all.sh                  파이프라인 (screen)
    │
    ├── rust/mcdm_core/                 RUST 엔진 (검증 + 배포)
    │   └── src/lib.rs                  모든 방법, 의존성 제로
    │
    └── evidence/                       대시보드 (Evidence.dev)
        ├── sources/mcdm/               11개 SQL 쿼리
        └── pages/                      12개 언어 라우트
```

---

## 🧠 이론적 근거

이 프로젝트는 직관이 아니라 심사된 문헌 위에 세워졌습니다. 통합 아키텍처는 **John (2025)**의 *“Integration of DEMATEL with Other MCDM Methods for Comprehensive Techno-Economic Analysis”*를 따릅니다: DEMATEL이 인과 구조를 드러내고 **영향력 기반 가중치**를 도출하여 순위화 방법들에 공급합니다 — 임의로 정한 가중치 대신에.

**브라질 다기준 의사결정 지원 학파**의 방법들(SAPEVO-M, TODIM-FSE, ELECTRE II, VIKOR, 서수적 방법)은 **IME**, **UFF**, **CASNAV**, **AMAN**, **FURB**의 연구를 따릅니다 — **해상전 드론 평가**, **여단 병참기지 분류**, **브라질 해군 초계함 순위화** 같은 실제 응용을 포함합니다.

> [!NOTE]
> **방법들의 저작권은 전적으로 그 창시자들에게 있으며,** `nucleo.py`와 `metodos_br.py`의 헤더에 개별적으로 명시되어 있습니다. 이 프로젝트가 기여하는 것은 구현, 통합, 합의 엔진이며 — **방법 자체가 아닙니다**.

---

## ❓ 당신이 하게 될 질문들

<details>
<summary><b>이미 가중 의사결정 행렬을 쓰고 있습니다. 같은 것 아닌가요?</b></summary>

아닙니다, 세 가지 이유에서. **(1)** 가중 행렬은 완전 보상이라는 이론이 내장된 **하나의** 방법(가중합)입니다. 어떤 기준에서의 형편없는 성능이 다른 곳에서 상쇄될 수 있다고 전제하는데 — 안전성, 장갑 방호, 규제 준수에서는 거짓입니다. **(2)** 기준이 독립이라 전제하지만, 당신은 거의 언제나 이미 더해진 것을 또 더합니다. **(3)** 신뢰구간 없는 숫자를 돌려주므로 위원회의 첫 질문을 넘기지 못합니다.
</details>

<details>
<summary><b>가중치는 어떻게 고르나요?</b></summary>

고르지 않습니다 — **세 경로가 그것을 도출합니다**. **DEMATEL**은 당신이 선언한 인과 구조(누가 누구에게 영향을 주는가)에서 추출합니다. **AHP**는 쌍대비교에서 추출하며, 일관성 검사가 모순된 판단을 **기각**합니다. **SAPEVO-M**은 여러 의사결정자의 서수적 판단에서 추출합니다. 그다음 견고성 분석이 결과가 아직 그것들에 얼마나 **의존**하는지 묻습니다.
</details>

<details>
<summary><b>제 문제에 대안이 200개라면요?</b></summary>

돌아갑니다. 병렬화 임계값이 규모를 감지해 프로세스에 분배합니다. 측정치: 대안 60개 × 기준 12개 × 세계 2,000개를 4프로세스에서 3.8초. 대안이 약 700개를 넘으면 선호 텐서가 설정된 메모리 한도를 초과하며, 엔진은 멈추는 대신 경고합니다.
</details>

<details>
<summary><b>방법들이 서로 다른 결론을 냈습니다. 이제 어떻게 하죠?</b></summary>

**그것이 산출물이지 문제가 아닙니다.** 갈림은 당신의 결정이 채택한 학파에 민감하다는 뜻이며, 어떤 학파인지도 알려 줍니다. 다른 모두가 선택한 대안을 ELECTRE가 강등한다면, 그 대안이 거부권을 부를 만큼 나쁜 기준이 존재하는 것입니다. 순위가 아니라 **그것**을 위원회에 가져가십시오.
</details>

<details>
<summary><b>제 데이터를 쓸 수 있나요?</b></summary>

그러라고 있는 것입니다. 사례는 `casos/catalogo.py`의 선언적 구조입니다: 기준(방향과 단위 포함), 대안, 의사결정 행렬, DEMATEL 인과행렬, Saaty 행렬. 검증기는 **어떤 계산보다 먼저** 잘못된 사례를 거부합니다 — 차원 불일치, 잘못된 대각선, 비상반 Saaty 행렬, 아무것도 구분하지 못하는 상수 기준.
</details>

---

## 📜 라이선스와 저작권

<div align="center">

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="420"/>

**ProfBru © 2026**

**MCDM Studio — 다기준 의사결정 모델**
저자: **ProfBru - Bruno Penedo** © 2026 — **모든 권리 보유**
📧 profbruanbima@gmail.com

</div>

**독점** 프로젝트입니다. 본 저장소는 사용·복제·수정·배포 또는 2차적 저작물 작성에 대한 어떠한 라이선스도 부여하지 않습니다. 상업적·학술적·기관적 사용에는 저자의 서면 허가가 필요합니다.

**제3자 귀속:** 다기준 방법들은 각 창시자의 저작입니다 — Saaty, Roy, Bertier, Brans, Vincke, Keeney, Raiffa, Ensslin, Montibeller, Noronha, Gabus, Fontela, Opricovic, Tzeng, Hwang, Yoon, Kahneman, Tversky, Borda, Copeland, Gomes, Lima, Santos, Teixeira, Moreira, Rangel, Neves, Hein, Kroenke, Keunecke, Gomes Júnior — 소스 코드에 개별적으로 명시되어 있습니다.
