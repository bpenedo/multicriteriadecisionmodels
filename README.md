<!--
MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
-->

<div align="center">

# 🎯 MCDM Studio — Modelos Multicritério de Decisão

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="820"/>

**ProfBru © 2026**

### Pare de escolher com planilha. Comece a decidir com prova.

**Nove escolas de decisão. Um vencedor. E — pela primeira vez — a probabilidade de esse vencedor estar certo.**

[![MCDM](https://img.shields.io/badge/Métodos_MCDM-9-2563eb?style=for-the-badge)](#-as-nove-escolas-de-decisão-e-por-que-nove)
[![Engines](https://img.shields.io/badge/Motores-Python_+_Rust-c2410c?style=for-the-badge)](#-dois-motores-independentes-a-prova-cruzada)
[![i18n](https://img.shields.io/badge/Idiomas-12-16a34a?style=for-the-badge)](#-12-idiomas--memória-de-tradução-sdl-trados)
[![Robustez](https://img.shields.io/badge/Universos_simulados-2.000-8f3d56?style=for-the-badge)](#-a-pergunta-que-ninguém-responde-e-se-os-pesos-estiverem-errados)

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Rust](https://img.shields.io/badge/Rust-1.96-000000?logo=rust&logoColor=white)](https://www.rust-lang.org)
[![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?logo=numpy&logoColor=white)](https://numpy.org)
[![Numba](https://img.shields.io/badge/Numba-JIT-00A3E0?logo=numba&logoColor=white)](https://numba.pydata.org)
[![Evidence](https://img.shields.io/badge/Evidence.dev-Dashboard-f4b548)](https://evidence.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/Licença-Proprietária-red)](#-licença-e-autoria)

🌐 **Português** · [English](README.en.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [中文](README.zh.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [עברית](README.he.md) · [Русский](README.ru.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md)

</div>

---

## 💀 A dor: você já perdeu dinheiro por causa de uma planilha

Pense na última decisão cara que você tomou. Comprar o carro. Escolher o fornecedor. Aprovar o projeto. Definir o notebook que 200 pessoas vão usar por quatro anos.

**Você abriu uma planilha. Colocou as opções nas linhas, os atributos nas colunas. E aí fez uma destas três coisas:**

| O que você fez | O que aconteceu de verdade |
|---|---|
| 🔻 **Ordenou pela coluna do preço** | Elegeu o mais barato. Você não precisava de uma planilha para isso. |
| 🔺 **Ordenou pela nota do especialista** | Elegeu o mais caro. Também não precisava. |
| 🔍 **Filtrou por "atende a todos os requisitos"** | A lista ficou vazia. Aí você afrouxou um requisito. Qual? **O que estava atrapalhando.** |

> [!WARNING]
> **As três operações têm o mesmo defeito: nenhuma delas responde à pergunta que você fez.**
> A pergunta era *"entre opções que se contradizem, qual escolher?"* — e ordenar por uma coluna é, por definição, decidir por **um** critério. Você não usou os outros sete. Eles estavam ali só para você se sentir melhor.

E tem o problema que ninguém vê: **você somou coisas que já estavam somadas.** Deu peso 20% para "consumo energético" e 25% para "autonomia" — mas consumo *causa* autonomia. Você contou a mesma coisa duas vezes e chamou isso de análise.

### O momento em que a decisão morre

É na reunião. Você apresenta o ranking. Alguém do comitê pergunta:

> *E se a autonomia valesse 30% em vez de 25%?*

E você não sabe. **Ninguém sabe.** Porque a planilha devolve **um** número, com uma confiança implícita de 100% que ela não tem como ter. Você volta com a lição de casa, mexe nos pesos, e descobre que o segundo colocado vira primeiro com **dois pontos percentuais** de diferença.

Aquele "vencedor" nunca foi um vencedor. Era um **artefato da sua calibração** — e você quase assinou embaixo.

---

## 💊 A solução: nove escolas, um consenso, e um intervalo de confiança

**MCDM Studio roda **nove métodos multicritério** consagrados sobre o mesmo problema, tira o vencedor do **consenso** entre eles, e então faz a única coisa que realmente importa:**

> ### 🎲 Perturba os pesos **2.000 vezes** e conta em quantos universos o vencedor continua vencendo.

O veredito deixa de ser um número e passa a ser uma **frase que sobrevive ao comitê**:

<div align="center">

| ❌ O que a planilha diz | ✅ O que o MCDM Studio diz |
|---|---|
| "O Modelo C é o melhor." | **"O Modelo C vence em 96% dos universos de preferência plausíveis. Veredito ROBUSTO: a escolha não depende da calibração fina dos pesos."** |
| *(sem resposta)* | **"O Modelo A vence em 51%. Veredito FRÁGIL: o 1º lugar é artefato dos pesos. Não decida só pelo ranking."** |

</div>

**Repare no segundo caso. Um sistema honesto tem que ser capaz de dizer *"não confie em mim aqui"*. É essa a diferença entre apoio à decisão e um gerador de justificativa para a decisão que você já queria tomar.**

---

## 🖼️ Veja funcionando

### 1. Quem é causa e quem é efeito — antes de qualquer peso

<div align="center"><img src="docs/telas/caca_multifuncao/dematel_causa_efeito.png" alt="DEMATEL" width="820"/></div>

**A dor que isso resolve:** você atribui pesos supondo que os critérios são independentes. **Quase nunca são.** Consumo energético *causa* autonomia. Blindagem *causa* peso, que *causa* perda de mobilidade. Somá-los como independentes é contar duas vezes.

O **DEMATEL** monta a matriz de relação total `T = X(I−X)⁻¹` — que soma influências diretas **e indiretas**, de qualquer comprimento de caminho — e separa o que você pode **puxar** (causas, acima da linha) do que apenas **mede o resultado** (efeitos, abaixo). Os pesos saem daí: por influência sistêmica, não por chute.

> No caso acima, **Transferência de Tecnologia** e **Assinatura Radar** são CAUSAS: mexer nelas move o sistema inteiro. **Disponibilidade de frota** é EFEITO — é termômetro, não alavanca. Um edital que pontua disponibilidade e ignora ToT está medindo febre e ignorando a infecção.

### 2. Nove escolas sobre o mesmo problema

<div align="center"><img src="docs/telas/veiculo_eletrico/mapa_metodos.png" alt="Métodos" width="900"/></div>

**A dor que isso resolve:** todo método MCDM tem uma teoria embutida sobre o que significa "melhor" — e ela muda o vencedor. Escolher um método e apresentar o resultado é escolher o resultado.

Rodamos os nove. Quando concordam, a escolha **não é artefato de método**. Quando divergem, **a divergência é o achado**.

> Acima: o **Híbrido plug-in** é 1º em sete métodos, mas **6º no ELECTRE I**. Não é ruído — é informação. O ELECTRE I permite *veto*: ele diz que o híbrido tem uma desvantagem grave o bastante em algum critério para ser eliminado, por melhor que seja no resto. **Essa é exatamente a pergunta que você quer levar ao comitê.**

### 3. O intervalo de confiança da própria decisão

<div align="center"><img src="docs/telas/portfolio_startup/robustez.png" alt="Robustez" width="820"/></div>

**A dor que isso resolve:** a pergunta do comitê — *"e se o peso fosse outro?"*. Respondida **antes** de alguém perguntar.

Perturbamos os pesos com `w' ~ Dirichlet(κ·w)` e reranqueamos 2.000 vezes. A Dirichlet é a escolha natural: seu suporte é exatamente o simplex (pesos positivos que somam 1) e ela satisfaz `E[w'] = w` — perturbamos **sem enviesar**.

### 4. Onde sua intuição está errada

<div align="center"><img src="docs/telas/blindado/pesos_dematel_ahp.png" alt="DEMATEL x AHP" width="820"/></div>

**A dor que isso resolve:** você acha que sabe o que é importante. Duas famílias de peso testam isso.

O **AHP** (Saaty) pergunta, par a par, quanto um critério importa mais que outro. O **DEMATEL** mede influência sistêmica. **Quando divergem, ali está o efeito de segunda ordem que você subestimou** — e o gráfico marca a maior divergência em vermelho.

### 5. Onde cada alternativa termina, em 2.000 cenários

<div align="center"><img src="docs/telas/estacao_trabalho/distribuicao_posicoes.png" alt="Distribuição" width="820"/></div>

Uma barra inteiramente verde é uma posição que **não depende dos pesos**. Uma barra manchada é uma posição em disputa. Você vê, de relance, onde o ranking é fato e onde é opinião.

---

## 🎯 Para que serve — a escolha sob medida

O motor é **agnóstico de domínio**: a unidade é o *caso de decisão* (alternativas × critérios), sem semântica de negócio embutida. Trocar de domínio é trocar dados, não código.

<div align="center">

| Domínio | A decisão | A dor específica |
|---|---|---|
| 📱 **Eletrônicos** | Celular, notebook, equipamento | O mais barato tem a pior câmera; o de melhor câmera tem a pior bateria. Não existe "o melhor" — existe **o melhor para o seu uso**. |
| 🚗 **Carros elétricos** | Frota ou uso pessoal | Autonomia, recarga, rede de assistência e revenda puxam para lados opostos. E o critério que decide (**autonomia real**, não a de catálogo) é o mais difícil de medir. |
| 🎖️ **Defesa** | Caças, blindados, drones, base logística | Ciclo de vida de 30 anos, irreversível, sob escrutínio público. **Preço unitário é menos de 1/3 do custo total.** Transferência de tecnologia e custo/hora decidem o orçamento de três décadas. |
| 🏢 **Corporativo** | Fornecedor, ERP, terceirização, expansão | Comitê que não concorda entre si. O **SAPEVO-M** foi feito exatamente para isso: agrega julgamento ordinal de **vários decisores** sem exigir consenso prévio. |
| 🚀 **Startups** | Portfólio de projetos, alocação de capital | Quem decide por retorno esperado sempre elege a aposta mais arriscada — **valor esperado ignora a cauda**. Aqui risco é **critério**, não nota de rodapé do slide 14. |
| 💻 **TI** | Padronização de parque | A decisão se multiplica por 200 e dura 4 anos. Autonomia e garantia on-site valem mais, no custo total de posse, que dois pontos de benchmark sintético. |

</div>

### Casos prontos para rodar

```bash
python3 pipeline.py --listar
```

| # | Caso | Domínio | Alternativas | Critérios | Veredito |
|--:|---|---|--:|--:|---|
| 1 | `smartphone` | consumo | 6 | 8 | PROVÁVEL 85% |
| 2 | `veiculo_eletrico` | automotivo | 7 | 8 | ROBUSTO 96% |
| 3 | `caca_multifuncao` | defesa | 6 | 9 | ROBUSTO 100% |
| 4 | `blindado` | defesa | 5 | 8 | ROBUSTO 90% |
| 5 | `portfolio_startup` | corporativo | 7 | 9 | ROBUSTO 97% |
| 6 | `estacao_trabalho` | TI | 6 | 8 | ROBUSTO 98% |
| 7 | `carros_eletricos` | automotivo | 38 | 9 | ROBUSTO 99% |
| 8 | `smartphones_2026` | consumo | 38 | 9 | PROVÁVEL 65% |
| 9 | `tablets` | consumo | 34 | 8 | PROVÁVEL 62% |
| 10 | `smartwatches` | consumo | 31 | 8 | PROVÁVEL 79% |
| 11 | `notebooks` | TI | 32 | 8 | PROVÁVEL 76% |
| 12 | `maquinario_agricola` | agronegócio | 35 | 8 | ROBUSTO 100% |
| 13 | `sbc_iot` | TI | 33 | 8 | ROBUSTO 100% |
| 14 | `mineracao_asic` | infraestrutura | 31 | 8 | FRÁGIL 51% |
| 15 | `minipcs` | TI | 10 | 8 | ROBUSTO 96% |
| 16 | `impressoras_3d_miniaturas` | manufatura | 30 | 9 | FRÁGIL 35% |
| 17 | `impressoras_3d_producao` | manufatura | 30 | 9 | FRÁGIL 45% |
| 18 | `plotters_formato` | manufatura | 24 | 9 | PROVÁVEL 86% |
| 19 | `impressoras_3d_miniaturas_triadas` | manufatura | 13 | 9 | ROBUSTO 100% |
| 20 | `acoes_b3` 📚 | financeiro | 20 | 7 | FRÁGIL 52% |
| 21 | `fundos_imobiliarios` 📚 | financeiro | 18 | 8 | PROVÁVEL 61% |
| 22 | `fintech` 📚 | financeiro | 16 | 8 | PROVÁVEL 78% |
| 23 | `avaliacao_imoveis` 📚 | imobiliário | 16 | 8 | ROBUSTO 96% |
| 24 | `ordens_servico` 📚 | operações | 18 | 8 | ROBUSTO 92% |
| 25 | `cloud_providers` 📚 | TI | 14 | 8 | ROBUSTO 100% |
| 26 | `venture_capital` 📚 | corporativo | 16 | 8 | ROBUSTO 97% |
| 27 | `instrutores` 📚 | corporativo | 15 | 8 | ROBUSTO 100% |
| 28 | `cripto_portfolio` 📚 | financeiro | 9 | 7 | ROBUSTO 100% |
| 29 | `portfolio_crise` 📚 | financeiro | 8 | 4 | PROVÁVEL 71% |
| 30 | `cenarios_va` 📚 | automotivo | 16 | 9 | PROVÁVEL 75% |
| 31 | `impressora_3d_energia` 📚 | manufatura | 12 | 7 | PROVÁVEL 80% |
| 32 | `impressoras_juridico` 📚 | operações | 12 | 4 | ROBUSTO 100% |
| 33 | `fundos_hedge` 📚 | financeiro | 20 | 8 | ROBUSTO 98% |
| 34 | `modelos_previsao` 📚 | TI | 7 | 8 | PROVÁVEL 74% |
| 35 | `policultivo_rj` 📚 | agronegócio | 8 | 8 | ROBUSTO 100% |
| 36 | `parafusadeiras_domesticas` 📚 | consumo | 14 | 8 | PROVÁVEL 86% |
| 37 | `parafusadeiras_profissionais` 📚 | manufatura | 12 | 8 | ROBUSTO 100% |

> [!NOTE]
> As matrizes dos casos são **ilustrativas** — ordens de grandeza públicas e plausíveis, para demonstrar o método. O que **não** é ilustrativo é a **modelagem**: critérios, direções, matriz causal do DEMATEL e matriz de Saaty. É nela que mora o valor. **Substitua os números pela sua cotação, seu edital ou seu ensaio de laboratório** — o motor é o mesmo; os dados é que são seus.

> [!TIP]
> O **veredito** mede em quantos dos 2.000 universos de preferência simulados o vencedor continua vencendo, perturbando os pesos por Dirichlet (κ=200). **ROBUSTO** ≥ 90%: a escolha não depende da calibragem. **PROVÁVEL** 60–89%: o vice é competitivo, compare os dois. **FRÁGIL** < 60%: o 1º lugar é artefato dos pesos — e isso é um achado legítimo, não uma falha. Significa que os dados não decidem, e a decisão volta para o humano.

### 📚 Estudos de caso derivados da literatura

> [!IMPORTANT]
> Oito dos casos têm os **critérios e a estrutura causal extraídos de artigos e teses revisados** — ações, fundos imobiliários, fintechs, avaliação de imóveis, ordens de serviço, provedores de nuvem, venture capital e ordenação de instrutores. Os critérios não foram inventados: vieram do texto de origem, e a autoria de cada trabalho está preservada no cabeçalho do módulo correspondente. As **matrizes numéricas** são instanciações próprias — nenhum dado dos trabalhos originais foi reproduzido.

| Caso | Domínio | Referência e autoria |
|---|---|---|
| `acoes_b3` | financeiro | COSTA, L. S. *Uma metodologia para a pré-seleção de ações utilizando o método multicritério TOPSIS*; *AHP–TOPSIS Methodology for Stock Portfolio Investments*, Risks 10(4):4, 2022 |
| `fundos_imobiliarios` | financeiro | SANTOS, V. V. *TCC*, Engenharia da Computação, UFPE |
| `fintech` | financeiro | *A Fuzzy Multicriteria Group Decision Making Approach for Evaluating and Selecting Fintech Projects* |
| `avaliacao_imoveis` | imobiliário | DUARTE, D. C. O. *Análise multicritério e geoestatística aplicadas na avaliação de imóveis*; MARQUES, J. P. M. |
| `ordens_servico` | operações | *Priorização de ordens de serviço: o AHP integrado ao PROMETHEE*. Revista Produção Online, v.22, n.2, 2022 |
| `cloud_providers` | TI | SOLOMON. *Ranking of Cloud Service Providers Using a Dynamic TOPSIS Model*. The George Washington University |
| `venture_capital` | corporativo | BEIM, G.; LÉVESQUE, M.; DHOCHAK, M. et al. (2019); AFFUL-DADZIE, E. et al.; MILKOVA/ANDREICHIKOV (IJAHP) |
| `instrutores` | corporativo | *Modelagem matemática com os métodos AHP e TOPSIS para ordenação de instrutores em uma escola da FAB*. LIV SBPO, 2022 |
| `cripto_portfolio` | financeiro | ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. *Cryptocurrency Portfolio Selection — A Multicriteria Approach*. Mathematics, 9(14):1677, 2021 — **pesos AHP do artigo** |
| `portfolio_crise` | financeiro | COSTA, I. P. A.; MAÊDA, S. M. N.; TEIXEIRA, L. F. H. S. B.; GOMES, C. F. S.; SANTOS, M. *Finanças em períodos de crise: aplicação do método SAPEVO-M*. Pesquisa Operacional para o Desenvolvimento, v.13, e13004, 2021 — **matriz de decisão do artigo** |
| `cenarios_va` | automotivo | LI, S.; ZHOU, R.; HUANG, H. *Multidimensional Evaluation of Autonomous Driving Test Scenarios Based on AHP-EWM-TOPSIS Models*. Automotive Innovation, 2025 |
| `impressora_3d_energia` | manufatura | OLIVEIRA, V. A. R. et al. *Multicriteria Analysis for 3D Printer Selection*. 23rd LACCEI, Cidade do México, 2025 — UNESP |
| `impressoras_juridico` | operações | OLIVEIRA, N. C.; OLIVEIRA, P. F. C.; GOMES, C. F. S.; SANTOS, M. *Aplicação do método AHP TOPSIS 2N: estudo de caso no departamento jurídico da Secretaria Municipal de Saúde de Duque de Caxias*, 2019 |
| `fundos_hedge` | financeiro | SILVA, F. P.; RIBEIRO, C. O. *Análise comparativa de fundos de hedge brasileiros utilizando DEA e bootstrap*. XII SIMPEP, Bauru-SP, 2005 — USP |
| `modelos_previsao` | TI | SHAH, S. *Comparison of Stochastic Forecasting Models*. Johns Hopkins University — o artigo compara os modelos; a modelagem multicritério é deste projeto |
| `policultivo_rj` | agronegócio | *AGTech PoliCultivo 4.0 — Otimização de Portfólio de Cultivos (RJ)*, relatório técnico, 03/08/2026, seção 14 — **matriz e pesos do relatório** |
| `parafusadeiras_domesticas` | consumo | COMPROU AVALIOU (canal). *As 5 Melhores Parafusadeira De 2025! // Tem Boa e Barata, 20V, De Impacto e Outras*, 14/05/2024 — especificações extraídas da narração |
| `parafusadeiras_profissionais` | manufatura | FERRAMENTAS EM AÇÃO — ASSIS PIRES (canal). *As Melhores Parafusadeiras Do Mundo*, 04/01/2024 — modelos e baterias lidos dos quadros do vídeo |

---

## ⚡ Instalação

### Caminho mais rápido (Python)

```bash
git clone <url> multicriteriadecisionmodels
cd multicriteriadecisionmodels/public/foundations/pipeline
pip install -r requirements.txt
python3 pipeline.py
```

Pronto. Os seis casos rodam, com relatório completo em português.

<details>
<summary><b>Pré-requisitos detalhados</b></summary>

| Componente | Versão mínima | Obrigatório? | Para quê |
|---|---|---|---|
| Python | 3.10 | ✅ | motor de referência |
| NumPy | 2.0 | ✅ | álgebra de todos os métodos |
| numba | 0.60 | ⚠️ | JIT dos kernels — sem ele roda igual, mais devagar |
| SciPy | 1.10 | ✅ | estatística auxiliar |
| matplotlib | 3.7 | ✅ | as 5 telas por caso |
| Rust / cargo | 1.75 | ⭕ | motor de verificação cruzada |
| Node.js | 18 | ⭕ | dashboard Evidence |
| screen | — | ⭕ | execução em background |

</details>

### Esteira completa

```bash
./run_all.sh                    # testes → pipeline → telas → i18n → Rust → conferência
./run_all.sh --rapido           # pula Rust e i18n
./run_all.sh --caso smartphone  # um caso só
./run_all.sh --background       # roda em screen (reatar: screen -r mcdm)
```

### Motor Rust — binário sem runtime

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
<summary><b>Comandos avançados</b></summary>

```bash
python3 pipeline.py caca_multifuncao --workers 8 --iter 5000
python3 testes_nucleo.py
python3 exportar_rust.py
python3 gerar_i18n.py --tudo
python3 gerar_i18n.py --verificar
python3 gerar_graficos.py --workers 6
```

| Variável | Padrão | Efeito |
|---|---|---|
| `MCDM_WORKERS` | auto | processos do `ProcessPoolExecutor` |
| `MCDM_NUMBA` | `1` | JIT ligado; `0` para depurar em NumPy puro |
| `MCDM_SEED` | `42` | reprodutibilidade |
| `ROBUSTEZ_ITER` | `2000` | universos de preferência |
| `ROBUSTEZ_KAPPA` | `200` | concentração da Dirichlet (maior = pesos mais fiéis) |
| `MAUT_AVERSAO` | `2.0` | aversão a risco (r > 0 = côncava) |
| `PROMETHEE_TIPO` | `linear` | função de preferência (6 disponíveis) |

</details>

---

## ⚖️ As nove escolas de decisão — e por que nove

> [!IMPORTANT]
> **Cada método é uma teoria diferente sobre o que significa "melhor".** Usar um só é escolher a resposta junto com a pergunta. Rodamos os nove porque a **concordância entre teorias independentes** é a evidência mais forte que um problema de decisão admite.

<div align="center">

| Método | Escola | O que assume | Quando é **a** ferramenta certa | Origem |
|---|---|---|---|---|
| **AHP-TOPSIS 2n** | distância ao ideal | compensação total | critérios quantitativos, decisor único | Saaty (1980); Hwang & Yoon (1981) |
| **ELECTRE I** | sobreclassificação | incomparabilidade é permitida | **triagem**: eliminar o dominado | Roy (1968) |
| **ELECTRE II** | sobreclassificação | limiares forte e fraco | ordenação completa **com veto** | Roy & Bertier (1971) |
| **PROMETHEE II** | sobreclassificação | preferência gradual (6 funções) | quando "um pouco melhor" ≠ "melhor" | Brans & Vincke (1985) |
| **MAUT** | utilidade | independência aditiva + aversão a risco | decisão sob incerteza | Keeney & Raiffa (1976) |
| **MCDA-C** | construtivista | níveis Neutro/Bom ancorados | **diagnóstico absoluto**, não só ranking | Ensslin, Montibeller & Noronha (2001) |
| **VIKOR** | compromisso | utilidade do grupo × arrependimento máximo | quando **compensar é inaceitável** | Opricovic (1979); Opricovic & Tzeng (2002-07) |
| **TODIM** | Teoria dos Prospectos | perda dói mais que ganho equivalente | decisor avesso a perda — **todos são** | Gomes & Lima (1992); Kahneman & Tversky (1979) |
| **SAPEVO-M** | ordinal multidecisor | julgamento ordinal de vários decisores | **comitê que não concorda entre si** | Gomes et al. (1997); Teixeira, Santos & Gomes (2019) |

</div>

<details>
<summary><b>Por que estes três merecem atenção especial</b></summary>

### VIKOR — quando compensar é inaceitável
O VIKOR calcula **duas** medidas: `S` (utilidade do grupo — soma ponderada, **aceita** que um desempenho péssimo seja compensado por vários bons) e `R` (arrependimento individual máximo — minimax, **recusa** compensação).

Um blindado com mobilidade excelente e proteção péssima tem `S` ótimo e `R` terrível. A soma ponderada o elegeria; o VIKOR sinaliza. E quando `S` e `R` discordam, as condições **C1** (vantagem aceitável) e **C2** (estabilidade aceitável) reportam explicitamente que a decisão tem um ponto cego.

### TODIM — a perda dói mais que o ganho
Baseado na **Teoria dos Prospectos** de Kahneman & Tversky: perder 10 pontos de autonomia dói mais do que ganhar 10 agrada. A soma ponderada clássica ignora essa assimetria e trata ganho e perda como simétricos — **o que nenhum decisor humano faz.** O fator `θ` calibra quanto: `θ < 1` amplifica a aversão à perda.

### SAPEVO-M — o comitê que não concorda
Todos os outros métodos exigem um vetor de pesos. **De onde ele vem quando há cinco decisores com opiniões diferentes?** O SAPEVO-M resolve na origem: cada decisor expressa preferência **ordinal** ("autonomia é muito mais importante que preço", numa escala de sete pontos), e o método agrega **sem exigir pré-ordem de consenso**. É como um comitê realmente se expressa — ninguém diz "autonomia vale 0,237".

</details>

### O motor de consenso

```
DEMATEL ──► pesos por influência ──► 9 métodos ──► consenso de Borda ──► vencedor
                                                    │
                        2.000 universos de Dirichlet ─────────────────┘
                                    ▼
                     veredito: ROBUSTO / PROVÁVEL / FRÁGIL
```

| Veredito | Confiança | O que fazer |
|---|---|---|
| 🟢 **ROBUSTO** | ≥ 90% | A escolha não depende da calibração fina. **Pode levar ao comitê.** |
| 🟡 **PROVÁVEL** | 60–90% | Se sustenta na maioria dos cenários, mas o vice é competitivo. **Compare os dois.** |
| 🔴 **FRÁGIL** | < 60% | O 1º lugar é **artefato dos pesos**. Não decida só pelo ranking: volte ao decisor e recalibre. |

---

## 🔬 Dois motores independentes: a prova cruzada

> [!TIP]
> **Por que reimplementar tudo em Rust?** Porque "o código roda" não é evidência de que a **matemática** está certa.

Um erro de transcrição de fórmula raramente se repete **idêntico** em duas linguagens com álgebra linear independente. O motor Python usa NumPy/LAPACK; o motor Rust implementa eliminação gaussiana com pivotamento parcial e método das potências **à mão, sem dependência externa alguma**.

```bash
python3 exportar_rust.py
```
```
✅ smartphone           8 métodos idênticos · vencedor=C     (Δ ≤ 4.7e-11)
✅ veiculo_eletrico     8 métodos idênticos · vencedor=EV6   (Δ ≤ 4.1e-11)
✅ caca_multifuncao     8 métodos idênticos · vencedor=C3    (Δ ≤ 4.5e-11)
✅ blindado             8 métodos idênticos · vencedor=B3    (Δ ≤ 4.6e-11)
✅ portfolio_startup    8 métodos idênticos · vencedor=P3    (Δ ≤ 4.9e-11)
✅ estacao_trabalho     8 métodos idênticos · vencedor=W5    (Δ ≤ 5.0e-11)
```

**Bônus: o binário Rust não precisa de Python, NumPy, numba nem ambiente virtual. Poucos MB que rodam em servidor, contêiner ou máquina embarcada — o que importa quando o motor acompanha um sistema em campo.**

---

## 🚀 Performance: 26× mais rápido, mesma resposta

A análise de robustez roda 2.000 universos × 9 métodos. A implementação ingênua levava **42 segundos** por caso.

<div align="center">

| Etapa | Tempo | Ganho |
|---|---|---|
| Kernels JIT por universo | 42,33 s | — |
| **Pré-compilação em tensores** | 2,41 s | **17,6×** |
| `ranks` sob JIT + estado por processo | **1,63 s** | **26,0×** |

</div>

> **A otimização que mais rendeu não foi paralelismo nem JIT.** Foi perceber que quatro dos nove métodos são **lineares no vetor de pesos** — o que permite pré-computar tensores e reduzir cada universo a um produto matriz-vetor. **Álgebra antes de infraestrutura.**

E o resultado é **bit a bit idêntico** ao caminho lento — 100 universos × 9 métodos verificados a cada execução da suíte. Otimização que muda resultado é bug, não ganho.

<details>
<summary><b>Política de execução do projeto</b></summary>

| Regra | Aplicação |
|---|---|
| **Paralelismo** | `ProcessPoolExecutor` para CPU-bound; nunca threads (o GIL serializa) |
| **Limiar** | Serial × paralelo decidido pelo **trabalho** (`n_iter · m² · k`), não pela contagem de itens — paralelizar problema pequeno é **mais lento** que resolvê-lo |
| **JIT** | `numba` com `cache=True` nos kernels O(m²k); degrada para NumPy puro se ausente |
| **Background** | `screen`, nunca `nohup` — permite reatar e interagir |
| **Reprodutibilidade** | Partição fixa e independente do nº de processos: mesma semente → resultado idêntico com 1 ou 32 processos |

</details>

---

## 🌐 12 idiomas — memória de tradução SDL Trados

Não é tradução automática de README. É um **pipeline de localização** com memória de tradução no padrão **SDL Trados Studio**.

```
translation.memory.md          ← fonte canônica, versionada em git
   │  --tm
   ▼
strings.<locale>.json          ← artefato consumido
   │  --paginas
   ▼
12 páginas do dashboard + 12 READMEs
   │  --tmx
   ▼
translation.memory.tmx         ← importável no SDL Trados Studio
```

| Item | Números |
|---|---|
| Locales | **12** (pt-BR · en · es · fr · de · zh · ko · hi · **he RTL** · ru · sv · fi) |
| Unidades de tradução | 56 |
| Termos de glossário (MultiTerm) | 22 |
| Segmentos no TMX | **948** |
| Encoding | UTF-8 · LF · NFC |

```bash
python3 gerar_i18n.py --verificar
```

O QA replica o **Verify** do Trados: consistência terminológica, placeables preservados, cobertura de segmento, encoding estrito e não-traduzíveis intactos — com regra diferenciada por sistema de escrita (siglas técnicas permanecem latinas em qualquer idioma; nomes próprios são **transliterados** onde a escrita não é latina).

---

## 📁 O que tem dentro

```
multicriteriadecisionmodels/
├── README.md (+11)                     vitrine em 12 idiomas
├── docs/                               logo e telas dos READMEs
│
└── public/foundations/
    ├── pipeline/                       MOTOR PYTHON (referência)
    │   ├── nucleo.py                   DEMATEL · ELECTRE I/II · PROMETHEE II
    │   │                               MAUT · MCDA-C · AHP · TOPSIS 2N
    │   ├── metodos_br.py               SAPEVO-M · VIKOR · TODIM · Copeland
    │   ├── robustez.py                 Dirichlet + ProcessPoolExecutor
    │   ├── pipeline.py                 orquestrador
    │   ├── gerar_graficos.py           5 telas por caso
    │   ├── gerar_i18n.py               TM → strings → páginas → TMX
    │   ├── testes_nucleo.py            16 verificações matemáticas
    │   ├── exportar_rust.py            conferência entre motores
    │   ├── casos/catalogo.py           6 casos + validação
    │   └── run_all.sh                  esteira (screen)
    │
    ├── rust/mcdm_core/                 MOTOR RUST (verificação + distribuição)
    │   └── src/lib.rs                  todos os métodos, zero dependências
    │
    └── evidence/                       DASHBOARD (Evidence.dev)
        ├── sources/mcdm/               11 consultas SQL
        └── pages/                      12 rotas de idioma
```

---

## 🧠 Fundamentação

O projeto é construído sobre literatura revisada, não sobre intuição. A arquitetura de integração segue **John (2025)**, *"Integration of DEMATEL with Other MCDM Methods for Comprehensive Techno-Economic Analysis"*: o DEMATEL revela a estrutura causal e deriva **pesos por influência**, que então alimentam os métodos de ranqueamento — em vez de pesos arbitrados.

Os métodos da **escola brasileira de Apoio Multicritério à Decisão** (SAPEVO-M, TODIM-FSE, ELECTRE II, VIKOR, métodos ordinais) seguem os trabalhos do **IME**, **UFF**, **CASNAV**, **AMAN** e **FURB** — incluindo aplicações reais em **avaliação de drones para guerra naval**, **classificação de base logística de brigada** e **ordenação de corvetas para a Marinha do Brasil**.

> [!NOTE]
> **A autoria dos métodos é integralmente de seus criadores,** creditados individualmente nos cabeçalhos de `nucleo.py` e `metodos_br.py`. Deste projeto são a implementação, a integração e o motor de consenso — **não os métodos**.

---

## ❓ Perguntas que você vai fazer

<details>
<summary><b>Já uso uma matriz de decisão ponderada. Não é a mesma coisa?</b></summary>

Não, por três razões. **(1)** Uma matriz ponderada é **um** método (soma ponderada), com uma teoria embutida: compensação total. Ela assume que desempenho péssimo num critério pode ser compensado por bom desempenho em outros — o que é falso em segurança, em proteção blindada e em conformidade regulatória. **(2)** Ela assume critérios independentes, e você quase sempre soma coisas que já estão somadas. **(3)** Ela devolve um número sem intervalo de confiança, e por isso não sobrevive à primeira pergunta do comitê.
</details>

<details>
<summary><b>Como escolho os pesos?</b></summary>

Você não escolhe — **três caminhos os derivam**. O **DEMATEL** os extrai da estrutura causal que você declara (quem influencia quem). O **AHP** os extrai de comparações par a par, com verificação de consistência que **reprova** julgamento contraditório. O **SAPEVO-M** os extrai de julgamento ordinal de vários decisores. E depois disso a análise de robustez pergunta o quanto o resultado ainda **depende** deles.
</details>

<details>
<summary><b>E se meu problema tiver 200 alternativas?</b></summary>

Roda. O limiar de paralelismo detecta o regime e distribui em processos. Medido: 60 alternativas × 12 critérios × 2.000 universos em 3,8 s com 4 processos. Acima de ~700 alternativas o tensor de preferência estoura o limite de memória configurado e o motor avisa, em vez de travar.
</details>

<details>
<summary><b>Os métodos discordaram. E agora?</b></summary>

**Isso é o produto, não o problema.** A divergência diz que sua decisão é sensível à escola adotada — e nomeia qual. Se o ELECTRE rebaixa quem todos os outros elegem, existe um critério em que essa alternativa é grave o bastante para veto. Leve **isso** ao comitê, não o ranking.
</details>

<details>
<summary><b>Posso usar meus próprios dados?</b></summary>

É para isso que serve. Um caso é uma estrutura declarativa em `casos/catalogo.py`: critérios (com direção e unidade), alternativas, matriz de decisão, matriz causal do DEMATEL e matriz de Saaty. O validador recusa caso mal formado **antes** de qualquer cálculo — dimensões incoerentes, diagonal errada, matriz de Saaty não recíproca, critério constante que não discrimina nada.
</details>

---

## 📜 Licença e autoria

<div align="center">

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="420"/>

**ProfBru © 2026**

**MCDM Studio — Modelos Multicritério de Decisão**
Autor: **ProfBru - Bruno Penedo** © 2026 — **TODOS OS DIREITOS RESERVADOS**
📧 profbruanbima@gmail.com

</div>

Projeto **proprietário**. Não há licença de uso, cópia, modificação, distribuição ou obra derivada concedida por este repositório. Uso comercial, acadêmico ou institucional requer autorização escrita do autor.

**Atribuição de terceiros:** os métodos multicritério são de autoria de seus respectivos criadores — Saaty, Roy, Bertier, Brans, Vincke, Keeney, Raiffa, Ensslin, Montibeller, Noronha, Gabus, Fontela, Opricovic, Tzeng, Hwang, Yoon, Kahneman, Tversky, Borda, Copeland, Gomes, Lima, Santos, Teixeira, Moreira, Rangel, Neves, Hein, Kroenke, Keunecke e Gomes Júnior — creditados individualmente no código-fonte.
