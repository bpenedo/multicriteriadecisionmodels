<!--
MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
-->

<div align="center">

# 🎯 MCDM Studio — Multikriterielle Entscheidungsmodelle

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="820"/>

**ProfBru © 2026**

### Hören Sie auf, mit einer Tabelle zu wählen. Fangen Sie an, mit Beweis zu entscheiden.

**Neun Entscheidungsschulen. Ein Sieger. Und — zum ersten Mal — die Wahrscheinlichkeit, dass dieser Sieger richtig ist.**

[![MCDM](https://img.shields.io/badge/MCDM_Methoden-10-2563eb?style=for-the-badge)](#-die-zehn-entscheidungsschulen--und-warum-zehn)
[![Engines](https://img.shields.io/badge/Engines-Python_+_Rust-c2410c?style=for-the-badge)](#-zwei-unabhängige-engines-die-kreuzprüfung)
[![i18n](https://img.shields.io/badge/Sprachen-12-16a34a?style=for-the-badge)](#-12-sprachen--sdl-trados-translation-memory)
[![Robustez](https://img.shields.io/badge/Simulierte_Universen-2.000-8f3d56?style=for-the-badge)](#-die-frage-die-niemand-beantwortet-was-wenn-die-gewichte-falsch-sind)

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Rust](https://img.shields.io/badge/Rust-1.96-000000?logo=rust&logoColor=white)](https://www.rust-lang.org)
[![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?logo=numpy&logoColor=white)](https://numpy.org)
[![Numba](https://img.shields.io/badge/Numba-JIT-00A3E0?logo=numba&logoColor=white)](https://numba.pydata.org)
[![Evidence](https://img.shields.io/badge/Evidence.dev-Dashboard-f4b548)](https://evidence.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/Lizenz-Proprietär-red)](#-lizenz-und-urheberschaft)

🌐 [Português](README.md) · [English](README.en.md) · [Español](README.es.md) · [Français](README.fr.md) · **Deutsch** · [中文](README.zh.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [עברית](README.he.md) · [Русский](README.ru.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md)

</div>

---

## 💀 Der Schmerz: Sie haben wegen einer Tabelle bereits Geld verloren

Denken Sie an die letzte teure Entscheidung, die Sie getroffen haben. Das Auto kaufen. Den Lieferanten wählen. Das Projekt genehmigen. Den Laptop festlegen, den 200 Menschen vier Jahre lang benutzen werden.

**Sie haben eine Tabelle geöffnet. Optionen in Zeilen, Attribute in Spalten. Und dann haben Sie eines dieser drei Dinge getan:**

| Was Sie getan haben | Was tatsächlich passiert ist |
|---|---|
| 🔻 **Nach der Preisspalte sortiert** | Sie haben das Billigste gewählt. Dafür brauchten Sie keine Tabelle. |
| 🔺 **Nach der Expertennote sortiert** | Sie haben das Teuerste gewählt. Auch dafür brauchten Sie keine. |
| 🔍 **Nach „erfüllt alle Anforderungen“ gefiltert** | Die Liste blieb leer. Also haben Sie eine Anforderung gelockert. Welche? **Die, die im Weg stand.** |

> [!WARNING]
> **Alle drei Operationen haben denselben Fehler: keine beantwortet die Frage, die Sie gestellt haben.**
> Die Frage lautete *„Welche unter Optionen wählen, die einander widersprechen?“* — und nach einer Spalte zu sortieren heißt per Definition, nach **einem** Kriterium zu entscheiden. Die anderen sieben haben Sie nicht benutzt. Sie waren nur da, damit Sie sich besser fühlen.

Und da ist das Problem, das niemand sieht: **Sie haben addiert, was bereits addiert war.** Sie gaben „Energieverbrauch“ 20 % und „Reichweite“ 25 % — aber der Verbrauch *verursacht* die Reichweite. Sie haben dasselbe zweimal gezählt und es Analyse genannt.

### Der Moment, in dem die Entscheidung stirbt

Es passiert im Meeting. Sie präsentieren das Ranking. Jemand aus dem Gremium fragt:

> *Und wenn die Reichweite 30 % statt 25 % wert wäre?*

Und Sie wissen es nicht. **Niemand weiß es.** Denn die Tabelle liefert **eine** Zahl mit einer impliziten Konfidenz von 100 %, die sie unmöglich haben kann. Sie kommen mit Hausaufgaben zurück, verändern die Gewichte und stellen fest, dass der Zweite mit **zwei Prozentpunkten** Unterschied zum Ersten wird.

Dieser „Sieger“ war nie ein Sieger. Er war ein **Artefakt Ihrer Kalibrierung** — und Sie hätten beinahe unterschrieben.

---

## 💊 Die Lösung: zehn Schulen, ein Konsens und ein Konfidenzintervall

**MCDM Studio führt **neun etablierte multikriterielle Methoden** auf demselben Problem aus, zieht den Sieger aus dem **Konsens** zwischen ihnen und tut dann das Einzige, worauf es wirklich ankommt:**

> ### 🎲 Es stört die Gewichte **2.000-mal** und zählt, in wie vielen Universen der Sieger weiterhin gewinnt.

Das Urteil ist keine Zahl mehr, sondern ein **Satz, der das Gremium überlebt**:

<div align="center">

| ❌ Was die Tabelle sagt | ✅ Was MCDM Studio sagt |
|---|---|
| „Modell C ist das beste.“ | **„Modell C gewinnt in 96 % der plausiblen Präferenzuniversen. Urteil ROBUST: die Wahl hängt nicht von der Feinjustierung der Gewichte ab.“** |
| *(keine Antwort)* | **„Modell A gewinnt in 51 %. Urteil FRAGIL: der erste Platz ist ein Artefakt der Gewichte. Entscheiden Sie nicht allein nach dem Ranking.“** |

</div>

**Beachten Sie den zweiten Fall. Ein ehrliches System muss sagen können *„vertraue mir hier nicht“*. Das ist der Unterschied zwischen Entscheidungsunterstützung und einem Generator für die Rechtfertigung der Entscheidung, die Sie ohnehin treffen wollten.**

---

## 🖼️ Sehen Sie es in Aktion

### 1. Wer Ursache und wer Wirkung ist — vor jeder Gewichtung

<div align="center"><img src="docs/telas/caca_multifuncao/dematel_causa_efeito.png" alt="DEMATEL" width="820"/></div>

**Der Schmerz, den das löst:** Sie vergeben Gewichte unter der Annahme, die Kriterien seien unabhängig. **Das sind sie fast nie.** Energieverbrauch *verursacht* Reichweite. Panzerung *verursacht* Gewicht, das *verursacht* Mobilitätsverlust. Sie als unabhängig zu addieren heißt doppelt zu zählen.

**DEMATEL** bildet die Gesamtrelationsmatrix `T = X(I−X)⁻¹` — die direkte **und indirekte** Einflüsse jeder Pfadlänge summiert — und trennt, woran Sie **ziehen** können (Ursachen, oberhalb der Linie), von dem, was nur das **Ergebnis misst** (Wirkungen, darunter). Die Gewichte entstehen daraus: aus systemischem Einfluss, nicht aus dem Bauch.

> Im obigen Fall sind **Technologietransfer** und **Radarsignatur** URSACHEN: an ihnen zu drehen bewegt das ganze System. **Flottenverfügbarkeit** ist eine WIRKUNG — ein Thermometer, kein Hebel. Eine Ausschreibung, die Verfügbarkeit bewertet und ToT ignoriert, misst das Fieber und ignoriert die Infektion.

### 2. Zehn Schulen auf demselben Problem

<div align="center"><img src="docs/telas/veiculo_eletrico/mapa_metodos.png" alt="Métodos" width="900"/></div>

**Der Schmerz, den das löst:** jede MCDM-Methode trägt eine eingebaute Theorie darüber, was „am besten“ bedeutet — und sie verändert den Sieger. Eine Methode zu wählen und das Ergebnis zu präsentieren heißt, das Ergebnis zu wählen.

Wir führen alle neun aus. Stimmen sie überein, ist die Wahl **kein Methodenartefakt**. Weichen sie ab, **ist die Abweichung der Befund**.

> Oben: der **Plug-in-Hybrid** ist in sieben Methoden Erster, aber **Sechster in ELECTRE I**. Das ist kein Rauschen — das ist Information. ELECTRE I erlaubt das *Veto*: es sagt, der Hybrid habe bei einem Kriterium einen so schweren Nachteil, dass er ausscheidet, so gut er sonst auch sei. **Genau diese Frage wollen Sie ins Gremium tragen.**

### 3. Das Konfidenzintervall der Entscheidung selbst

<div align="center"><img src="docs/telas/portfolio_startup/robustez.png" alt="Robustez" width="820"/></div>

**Der Schmerz, den das löst:** die Frage des Gremiums — *„und wenn das Gewicht anders wäre?“*. Beantwortet, **bevor** sie jemand stellt.

Wir stören die Gewichte mit `w' ~ Dirichlet(κ·w)` und ranken 2.000-mal neu. Die Dirichlet ist die natürliche Wahl: ihr Träger ist genau das Simplex (positive Gewichte mit Summe 1) und sie erfüllt `E[w'] = w` — wir stören **ohne zu verzerren**.

### 4. Wo Ihre Intuition falsch liegt

<div align="center"><img src="docs/telas/blindado/pesos_dematel_ahp.png" alt="DEMATEL x AHP" width="820"/></div>

**Der Schmerz, den das löst:** Sie glauben zu wissen, was wichtig ist. Zwei Gewichtsfamilien stellen das auf die Probe.

Der **AHP** (Saaty) fragt paarweise, wie viel wichtiger ein Kriterium als ein anderes ist. **DEMATEL** misst systemischen Einfluss. **Wo sie abweichen, liegt der Effekt zweiter Ordnung, den Sie unterschätzt haben** — und das Diagramm markiert die größte Abweichung rot.

### 5. Wo jede Alternative landet, über 2.000 Szenarien

<div align="center"><img src="docs/telas/estacao_trabalho/distribuicao_posicoes.png" alt="Distribuição" width="820"/></div>

Ein durchgehend grüner Balken ist eine Platzierung, die **nicht von den Gewichten abhängt**. Ein gesprenkelter Balken ist eine umkämpfte Platzierung. Sie sehen auf einen Blick, wo das Ranking Tatsache und wo es Meinung ist.

---

## 🎯 Wofür es gut ist — die maßgeschneiderte Wahl

Die Engine ist **domänenagnostisch**: die Einheit ist der *Entscheidungsfall* (Alternativen × Kriterien), ohne eingebaute Geschäftssemantik. Die Domäne zu wechseln heißt Daten zu wechseln, nicht Code.

<div align="center">

| Domäne | Die Entscheidung | Der spezifische Schmerz |
|---|---|---|
| 📱 **Elektronik** | Handy, Laptop, Ausrüstung | Das Billigste hat die schlechteste Kamera; das mit der besten Kamera den schlechtesten Akku. „Das Beste“ gibt es nicht — es gibt **das Beste für Ihren Einsatz**. |
| 🚗 **Elektroautos** | Flotte oder Privatnutzung | Reichweite, Ladezeit, Servicenetz und Wiederverkauf ziehen in entgegengesetzte Richtungen. Und das entscheidende Kriterium (**reale Reichweite**, nicht die aus dem Katalog) ist das am schwersten messbare. |
| 🎖️ **Verteidigung** | Kampfjets, Panzer, Drohnen, Logistikbasis | 30 Jahre Lebenszyklus, unumkehrbar, unter öffentlicher Beobachtung. **Der Stückpreis macht weniger als ein Drittel der Gesamtkosten aus.** Technologietransfer und Stundenkosten entscheiden über drei Jahrzehnte Budget. |
| 🏢 **Unternehmen** | Lieferant, ERP, Outsourcing, Expansion | Ein Gremium, das sich mit sich selbst nicht einig ist. **SAPEVO-M** wurde genau dafür gebaut: es aggregiert das ordinale Urteil **mehrerer Entscheidungsträger**, ohne vorherigen Konsens zu verlangen. |
| 🚀 **Start-ups** | Projektportfolio, Kapitalallokation | Wer nach Erwartungswert entscheidet, wählt stets die riskanteste Wette — **der Erwartungswert ignoriert den Rand der Verteilung**. Hier ist Risiko ein **Kriterium**, keine Fußnote auf Folie 14. |
| 💻 **IT** | Standardisierung des Gerätebestands | Die Entscheidung multipliziert sich mit 200 und hält 4 Jahre. Akkulaufzeit und Vor-Ort-Garantie sind in den Gesamtbetriebskosten mehr wert als zwei Punkte im synthetischen Benchmark. |

</div>

### Sofort ausführbare Fälle

```bash
python3 pipeline.py --listar
```

| # | Fall | Domäne | Alternativen | Kriterien | Urteil | Autorschaft / Quelle |
|--:|---|---|--:|--:|---|---|
| 1 | `smartphone` | Konsum | 6 | 8 | WAHRSCHEINLICH 63% | Eigene Modellierung |
| 2 | `veiculo_eletrico` | Automobil | 7 | 8 | ROBUST 99% | Eigene Modellierung |
| 3 | `caca_multifuncao` | Verteidigung | 6 | 9 | ROBUST 100% | Eigene Modellierung |
| 4 | `blindado` | Verteidigung | 5 | 8 | ROBUST 93% | Eigene Modellierung |
| 5 | `portfolio_startup` | Unternehmen | 7 | 9 | ROBUST 96% | Eigene Modellierung |
| 6 | `estacao_trabalho` | IT | 6 | 8 | ROBUST 98% | Eigene Modellierung |
| 7 | `carros_eletricos` | Automobil | 38 | 9 | ROBUST 96% | Eigene Modellierung |
| 8 | `smartphones_2026` | Konsum | 38 | 9 | WAHRSCHEINLICH 73% | Eigene Modellierung |
| 9 | `tablets` | Konsum | 34 | 8 | WAHRSCHEINLICH 67% | Eigene Modellierung |
| 10 | `smartwatches` | Konsum | 31 | 8 | WAHRSCHEINLICH 84% | Eigene Modellierung |
| 11 | `notebooks` | IT | 32 | 8 | WAHRSCHEINLICH 83% | Eigene Modellierung |
| 12 | `maquinario_agricola` | Agrarwirtschaft | 35 | 8 | ROBUST 100% | Eigene Modellierung |
| 13 | `sbc_iot` | IT | 33 | 8 | ROBUST 100% | Eigene Modellierung |
| 14 | `mineracao_asic` | Infrastruktur | 31 | 8 | FRAGIL 50% | Eigene Modellierung |
| 15 | `minipcs` | IT | 10 | 8 | ROBUST 91% | Eigene Modellierung |
| 16 | `impressoras_3d_miniaturas` | Fertigung | 30 | 9 | FRAGIL 48% | Eigene Modellierung |
| 17 | `impressoras_3d_producao` | Fertigung | 30 | 9 | FRAGIL 58% | Eigene Modellierung |
| 18 | `plotters_formato` | Fertigung | 24 | 9 | ROBUST 96% | Eigene Modellierung |
| 19 | `impressoras_3d_miniaturas_triadas` | Fertigung | 13 | 9 | ROBUST 100% | Eigene Modellierung |
| 20 | `acoes_b3` 📚 | Finanzen | 20 | 7 | FRAGIL 39% | COSTA, L. S. da · VÁSQUEZ, J. A.; ESCOBAR, J. W.; MANOTAS, D. F. · [DOI](https://doi.org/10.3390/risks10010004) |
| 21 | `fundos_imobiliarios` 📚 | Finanzen | 18 | 8 | WAHRSCHEINLICH 85% | SANTOS, V. V. dos (orient. ALMEIDA FILHO, A. T. de) |
| 22 | `fintech` 📚 | Finanzen | 16 | 8 | WAHRSCHEINLICH 67% | WIBOWO, S.; GRANDHI, L.; GRANDHI, S.; WELLS, M. · [DOI](https://doi.org/10.3390/math10020225) |
| 23 | `avaliacao_imoveis` 📚 | Immobilien | 16 | 8 | ROBUST 94% | DUARTE, D. C. de O. · MARQUES, J. P. M. |
| 24 | `ordens_servico` 📚 | Betrieb | 18 | 8 | ROBUST 97% | ALENCAR, L. G. de; TAVARES, F. R. M.; MENDONÇA, F. J. S. de F.; DUARTE, A. K. G. |
| 25 | `cloud_providers` 📚 | IT | 14 | 8 | ROBUST 100% | SOLOMON, T. |
| 26 | `venture_capital` 📚 | Unternehmen | 16 | 8 | ROBUST 96% | BEIM, G.; LÉVESQUE, M. · DHOCHAK, M.; DOLIYA, P. · AFFUL-DADZIE, E.; AFFUL-DADZIE, A.; OPLATKOVÁ, Z. K. · [DOI](https://doi.org/10.1002/mcda.1703) |
| 27 | `instrutores` 📚 | Unternehmen | 15 | 8 | ROBUST 100% | SILVA, C. E. J. da; SALLES-NETO, L. L. de; SANTOS, M. dos |
| 28 | `cripto_portfolio` 📚 | Finanzen | 9 | 7 | ROBUST 100% | ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. · [DOI](https://doi.org/10.3390/math9141677) |
| 29 | `portfolio_crise` 📚 | Finanzen | 8 | 4 | WAHRSCHEINLICH 77% | COSTA, I. P. de A.; MAÊDA, S. M. do N.; TEIXEIRA, L. F. H. de S. de B.; GOMES, C. F. S.; SANTOS, M. dos |
| 30 | `cenarios_va` 📚 | Automobil | 16 | 9 | WAHRSCHEINLICH 73% | LI, S.; ZHOU, R.; HUANG, H. · [DOI](https://doi.org/10.1007/s42154-024-00344-6) |
| 31 | `impressora_3d_energia` 📚 | Fertigung | 12 | 7 | WAHRSCHEINLICH 69% | OLIVEIRA, V. A. R. de; ALVARADO SILVA, C. A.; OLIVEIRA, G. C. R. de; TAJIMA, F. M.; FARIA NETO, A. dos R.; SALOMON, V. A. P.; GUIDI, E. S. · [DOI](https://doi.org/10.18687/LACCEI2025.1.1.1193) |
| 32 | `impressoras_juridico` 📚 | Betrieb | 12 | 4 | ROBUST 100% | OLIVEIRA, N. C.; OLIVEIRA, P. F. C. de; GOMES, C. F. S.; SANTOS, M. dos |
| 33 | `fundos_hedge` 📚 | Finanzen | 20 | 8 | ROBUST 94% | SILVA, F. P. da; RIBEIRO, C. de O. |
| 34 | `modelos_previsao` 📚 | IT | 7 | 8 | ROBUST 95% | SHAH, S. |
| 35 | `policultivo_rj` 📚 | Agrarwirtschaft | 8 | 8 | WAHRSCHEINLICH 86% | PENEDO, B. |
| 36 | `parafusadeiras_domesticas` 📚 | Konsum | 14 | 8 | WAHRSCHEINLICH 70% | COMPROU AVALIOU (canal) · [vídeo](https://youtu.be/pgdqVYEjZtk) |
| 37 | `parafusadeiras_profissionais` 📚 | Fertigung | 12 | 8 | ROBUST 100% | FERRAMENTAS EM AÇÃO — ASSIS PIRES (canal) · [vídeo](https://youtube.com/shorts/9SIs3agoZKc) |
| 38 | `crowdfunding_startups` 📚 | Unternehmen | 16 | 9 | ROBUST 93% | SKARE, M.; GAVUROVA, B.; POLISHCHUK, V. · [DOI](https://doi.org/10.1016/j.jbusres.2023.113719) |

> [!NOTE]
> Die Fallmatrizen sind **illustrativ** — öffentliche, plausible Größenordnungen zur Demonstration der Methode. **Nicht** illustrativ ist die **Modellierung**: Kriterien, Richtungen, DEMATEL-Kausalmatrix und Saaty-Matrix. Dort liegt der Wert. **Ersetzen Sie die Zahlen durch Ihr Angebot, Ihre Ausschreibung oder Ihre Laborprüfung** — die Engine bleibt dieselbe; die Daten sind Ihre.

> [!TIP]
> Das **Urteil** misst, in wie vielen der 2.000 simulierten Präferenzuniversen der Sieger Sieger bleibt, wobei die Gewichte per Dirichlet (κ=200) gestört werden. **ROBUST** ≥ 90 %: Die Wahl hängt nicht von der Kalibrierung ab. **WAHRSCHEINLICH** 60–89 %: Der Zweite ist konkurrenzfähig, vergleichen Sie beide. **FRAGIL** < 60 %: Der erste Platz ist ein Artefakt der Gewichte — und das ist ein legitimer Befund, kein Fehler. Es bedeutet, dass die Daten nicht entscheiden und die Entscheidung zum Menschen zurückkehrt.

### 📚 Aus der Fachliteratur abgeleitete Fallstudien

> [!IMPORTANT]
> Bei den Fällen in der folgenden Tabelle stammen **Kriterien und Kausalstruktur aus den aufgeführten Arbeiten** — begutachtete Aufsätze, Abschlussarbeiten, Konferenzbände und technische Berichte. Die Kriterien sind nicht erfunden: Sie stammen aus dem Quelltext, und die Urheberschaft ist hier und im Kopf des jeweiligen Moduls festgehalten. Die **Zahlenmatrizen** sind eigene Instanziierungen — es wurden keine Daten aus den Originalarbeiten übernommen. Wo ein indexierter DOI vorliegt, führt der Link zur Arbeit; andernfalls genügt die vollständige Textangabe, um sie zu finden.

| Fall | Domäne | Autoren | Quellenangabe |
|---|---|---|---|
| `acoes_b3` | Finanzen | COSTA, L. S. da · VÁSQUEZ, J. A.; ESCOBAR, J. W.; MANOTAS, D. F. | *Uma metodologia para a pré-seleção de ações utilizando o método multicritério TOPSIS* (COSTA, UERJ) · *AHP–TOPSIS Methodology for Stock Portfolio Investments*, Risks, v.10, n.1, 4, 2022 (Universidad del Valle) · [DOI](https://doi.org/10.3390/risks10010004) |
| `fundos_imobiliarios` | Finanzen | SANTOS, V. V. dos (orient. ALMEIDA FILHO, A. T. de) | *Avaliação do método Random Forest para auxílio à seleção de fundos de investimento imobiliário listados na Bolsa de Valores*. Trabalho de Graduação, Engenharia da Computação, CIn/UFPE, set. 2023 |
| `fintech` | Finanzen | WIBOWO, S.; GRANDHI, L.; GRANDHI, S.; WELLS, M. | *A Fuzzy Multicriteria Group Decision Making Approach for Evaluating and Selecting Fintech Projects*. Mathematics, v.10, n.2, 225, 2022 — CQUniversity, Austrália · [DOI](https://doi.org/10.3390/math10020225) |
| `avaliacao_imoveis` | Immobilien | DUARTE, D. C. de O. · MARQUES, J. P. M. | *Análise multicritério e geoestatística aplicadas na avaliação em massa de imóveis urbanos*. Tese, UFV, 2019 · *As formas de avaliar imóvel em leilão judicial*. Universidade São Judas Tadeu, 2023 |
| `ordens_servico` | Betrieb | ALENCAR, L. G. de; TAVARES, F. R. M.; MENDONÇA, F. J. S. de F.; DUARTE, A. K. G. | *Priorização de ordens de serviço aplicando métodos de tomada de decisão: o AHP integrado ao PROMETHEE*. Revista Produção Online, v.22, n.2, p.2763-2784, 2022 — URCA, Ceará |
| `cloud_providers` | IT | SOLOMON, T. | *Ranking of Cloud Service Providers Using a Dynamic TOPSIS Model for Provisioning of Enterprise IT Infrastructure in the Cloud*. Praxis (Doctor of Engineering), The George Washington University, 2017 |
| `venture_capital` | Unternehmen | BEIM, G.; LÉVESQUE, M. · DHOCHAK, M.; DOLIYA, P. · AFFUL-DADZIE, E.; AFFUL-DADZIE, A.; OPLATKOVÁ, Z. K. | *Selecting projects for venture capital funding: a multiple criteria decision approach* (Case Western Reserve University) · *Valuation of a startup: moving towards strategic approaches*, J. Multi-Criteria Decision Analysis, 2019 · *Assessing commercial viability of technology start-up businesses in a government venture capital under intuitionistic fuzzy environment*, Int. J. Fuzzy Systems, 2016 · [DOI](https://doi.org/10.1002/mcda.1703) · [DOI](https://doi.org/10.1007/s40815-016-0141-9) |
| `instrutores` | Unternehmen | SILVA, C. E. J. da; SALLES-NETO, L. L. de; SANTOS, M. dos | *Modelagem matemática com os métodos AHP e TOPSIS para ordenação de instrutores em uma escola da FAB*. LIV SBPO, Juiz de Fora, 2022 — ITA / UNIFESP / IME |
| `cripto_portfolio` | Finanzen | ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. | *Cryptocurrency Portfolio Selection — A Multicriteria Approach*. Mathematics, v.9, n.14, 1677, 2021 — University of Split, Croácia — **pesos AHP do artigo** · [DOI](https://doi.org/10.3390/math9141677) |
| `portfolio_crise` | Finanzen | COSTA, I. P. de A.; MAÊDA, S. M. do N.; TEIXEIRA, L. F. H. de S. de B.; GOMES, C. F. S.; SANTOS, M. dos | *Finanças em períodos de crise: aplicação do método SAPEVO-M para composição de portfólios de investimentos*. Pesquisa Operacional para o Desenvolvimento, v.13, e13004, 2021 — UFF / CASNAV / IME — **matriz de decisão do artigo** |
| `cenarios_va` | Automobil | LI, S.; ZHOU, R.; HUANG, H. | *Multidimensional Evaluation of Autonomous Driving Test Scenarios Based on AHP-EWM-TOPSIS Models*. Automotive Innovation, 2025 · [DOI](https://doi.org/10.1007/s42154-024-00344-6) |
| `impressora_3d_energia` | Fertigung | OLIVEIRA, V. A. R. de; ALVARADO SILVA, C. A.; OLIVEIRA, G. C. R. de; TAJIMA, F. M.; FARIA NETO, A. dos R.; SALOMON, V. A. P.; GUIDI, E. S. | *Multicriteria Analysis for 3D Printer Selection*. 23rd LACCEI International Multi-Conference, Cidade do México, 2025 — UNESP / Universidad César Vallejo · [DOI](https://doi.org/10.18687/LACCEI2025.1.1.1193) |
| `impressoras_juridico` | Betrieb | OLIVEIRA, N. C.; OLIVEIRA, P. F. C. de; GOMES, C. F. S.; SANTOS, M. dos | *Aplicação do método AHP TOPSIS 2N como apoio à tomada de decisão: estudo de caso no departamento jurídico da Secretaria Municipal de Saúde de Duque de Caxias* — UNIGRANRIO / UFF / IME |
| `fundos_hedge` | Finanzen | SILVA, F. P. da; RIBEIRO, C. de O. | *Análise comparativa de fundos de hedge brasileiros utilizando DEA e bootstrap*. XII SIMPEP, Bauru-SP, 2005 — Escola Politécnica da USP |
| `modelos_previsao` | IT | SHAH, S. | *Comparison of Stochastic Forecasting Models*. Stochastic Differential Equations Course Project, Johns Hopkins University — o artigo compara os modelos; a modelagem multicritério sobre eles é deste projeto |
| `policultivo_rj` | Agrarwirtschaft | PENEDO, B. | *AGTech PoliCultivo 4.0 — Otimização de Portfólio de Cultivos em Ambiente Controlado (RJ)*. Relatório técnico, 03/08/2026, seção 14 — **matriz e pesos do relatório** |
| `parafusadeiras_domesticas` | Konsum | COMPROU AVALIOU (canal) | *As 5 Melhores Parafusadeira De 2025*, 14/05/2024 — especificações extraídas da narração · [vídeo](https://youtu.be/pgdqVYEjZtk) |
| `parafusadeiras_profissionais` | Fertigung | FERRAMENTAS EM AÇÃO — ASSIS PIRES (canal) | *As Melhores Parafusadeiras Do Mundo*, 04/01/2024 — modelos e baterias lidos dos quadros do vídeo · [vídeo](https://youtube.com/shorts/9SIs3agoZKc) |
| `crowdfunding_startups` | Unternehmen | SKARE, M.; GAVUROVA, B.; POLISHCHUK, V. | *A decision-making support model for financing start-up projects by venture capital funds on a crowdfunding platform*. Journal of Business Research, v.158, 113719, 2023 — **critérios e escalas do artigo** · [DOI](https://doi.org/10.1016/j.jbusres.2023.113719) |

---

## ⚡ Installation

### Schnellster Weg (Python)

```bash
git clone <url> multicriteriadecisionmodels
cd multicriteriadecisionmodels/public/foundations/pipeline
pip install -r requirements.txt
python3 pipeline.py
```

Fertig. Alle sechs Fälle laufen, mit vollständigem Bericht.

<details>
<summary><b>Detaillierte Voraussetzungen</b></summary>

| Komponente | Mindestversion | Pflicht? | Wofür |
|---|---|---|---|
| Python | 3.10 | ✅ | Referenz-Engine |
| NumPy | 2.0 | ✅ | Algebra aller Methoden |
| numba | 0.60 | ⚠️ | JIT der Kernel — ohne ihn gleiches Ergebnis, langsamer |
| SciPy | 1.10 | ✅ | Hilfsstatistik |
| matplotlib | 3.7 | ✅ | die 5 Ansichten pro Fall |
| Rust / cargo | 1.75 | ⭕ | Kreuzprüfungs-Engine |
| Node.js | 18 | ⭕ | Evidence-Dashboard |
| screen | — | ⭕ | Ausführung im Hintergrund |

</details>

### Vollständige Pipeline

```bash
./run_all.sh                    # Tests → Pipeline → Ansichten → i18n → Rust → Abgleich
./run_all.sh --rapido           # überspringt Rust und i18n
./run_all.sh --caso smartphone  # nur ein Fall
./run_all.sh --background       # läuft in screen (wieder anhängen: screen -r mcdm)
```

### Rust-Engine — Binary ohne Runtime

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
<summary><b>Erweiterte Befehle</b></summary>

```bash
python3 pipeline.py caca_multifuncao --workers 8 --iter 5000
python3 testes_nucleo.py
python3 exportar_rust.py
python3 gerar_i18n.py --tudo
python3 gerar_i18n.py --verificar
python3 gerar_graficos.py --workers 6
```

| Variable | Standard | Wirkung |
|---|---|---|
| `MCDM_WORKERS` | auto | Prozesse des `ProcessPoolExecutor` |
| `MCDM_NUMBA` | `1` | JIT an; `0` zum Debuggen in reinem NumPy |
| `MCDM_SEED` | `42` | Reproduzierbarkeit |
| `ROBUSTEZ_ITER` | `2000` | Präferenzuniversen |
| `ROBUSTEZ_KAPPA` | `200` | Konzentration der Dirichlet (höher = Gewichte bleiben näher) |
| `MAUT_AVERSAO` | `2.0` | Risikoaversion (r > 0 = konkav) |
| `PROMETHEE_TIPO` | `linear` | Präferenzfunktion (6 verfügbar) |

</details>

---

## ⚖️ Die zehn Entscheidungsschulen — und warum zehn

> [!IMPORTANT]
> **Jede Methode ist eine andere Theorie darüber, was „am besten“ bedeutet.** Nur eine zu verwenden heißt, die Antwort zusammen mit der Frage zu wählen. Wir führen alle zehn aus, weil **Übereinstimmung zwischen unabhängigen Theorien** der stärkste Beleg ist, den ein Entscheidungsproblem zulässt.

<div align="center">

| Methode | Schule | Was sie annimmt | Wann sie **das** richtige Werkzeug ist | Ursprung |
|---|---|---|---|---|
| **AHP-TOPSIS 2n** | Distanz zum Ideal | vollständige Kompensation | quantitative Kriterien, einzelner Entscheider | Saaty (1980); Hwang & Yoon (1981) |
| **ELECTRE I** | Outranking | Unvergleichbarkeit ist erlaubt | **Vorauswahl**: das Dominierte ausscheiden | Roy (1968) |
| **ELECTRE II** | Outranking | starke und schwache Schwellen | vollständige Rangfolge **mit Veto** | Roy & Bertier (1971) |
| **PROMETHEE II** | Outranking | graduelle Präferenz (6 Funktionen) | wenn „etwas besser“ ≠ „besser“ | Brans & Vincke (1985) |
| **MAUT** | Nutzen | additive Unabhängigkeit + Risikoaversion | Entscheidung unter Unsicherheit | Keeney & Raiffa (1976) |
| **MCDA-C** | konstruktivistisch | verankerte Neutral-/Gut-Niveaus | **absolute Diagnose**, nicht nur Ranking | Ensslin, Montibeller & Noronha (2001) |
| **VIKOR** | Kompromiss | Gruppennutzen × maximales Bedauern | wenn **Kompensation inakzeptabel ist** | Opricovic (1979); Opricovic & Tzeng (2002-07) |
| **TODIM** | Prospect Theory | ein Verlust schmerzt mehr als ein gleich großer Gewinn erfreut | verlustaverser Entscheider — **das sind alle** | Gomes & Lima (1992); Kahneman & Tversky (1979) |
| **SAPEVO-M** | ordinal, mehrere Entscheider | ordinales Urteil mehrerer Entscheider | **Gremium, das sich nicht einig ist** | Gomes et al. (1997); Teixeira, Santos & Gomes (2019) |
| **TOPSIS Fuzzy** | Fuzzy | dass die Angabe eine SPANNE ist, kein Punkt | die Messung unscharf ist und Sie wissen wollen, ob die Rangliste das übersteht | Zadeh (1965); Chen (2000) |

</div>

> [!NOTE]
> Das **Fuzzy-TOPSIS** ist nicht AHP-TOPSIS mit Rauschen: Neben den Dreiecksnummern tauscht es die Normalisierung (linear statt vektoriell) und die Ideallösung (absolut statt relativ). **Vom AHP-TOPSIS 2n abzuweichen ist das erwartete Verhalten** und misst, wie stark die Rangliste von diesen Entscheidungen abhängt. Das **Fuzzy-AHP** (Buckley) tritt als dritte Gewichtsquelle neben DEMATEL und AHP: Es erhält dasselbe paarweise Urteil, trägt die Unschärfe aber bis zum Ende — bei gleichmäßiger Streuung stimmt der Zentralwert mit dem des AHP überein, und was es hinzufügt, ist die **Spanne**, die beantwortet, ob die Prioritätenfolge die Unschärfe des Entscheiders selbst übersteht.

<details>
<summary><b>Warum diese drei besondere Aufmerksamkeit verdienen</b></summary>

### VIKOR — wenn Kompensation inakzeptabel ist
VIKOR berechnet **zwei** Maße: `S` (Gruppennutzen — gewichtete Summe, die **akzeptiert**, dass eine miserable Leistung durch mehrere gute ausgeglichen wird) und `R` (maximales individuelles Bedauern — Minimax, das Kompensation **ablehnt**).

Ein Panzer mit exzellenter Mobilität und miserablem Schutz hat ein optimales `S` und ein katastrophales `R`. Die gewichtete Summe würde ihn wählen; VIKOR schlägt Alarm. Und wenn `S` und `R` sich widersprechen, melden die Bedingungen **C1** (akzeptabler Vorteil) und **C2** (akzeptable Stabilität) ausdrücklich, dass die Entscheidung einen blinden Fleck hat.

### TODIM — der Verlust schmerzt mehr als der Gewinn
Basierend auf der **Prospect Theory** von Kahneman & Tversky: 10 Punkte Reichweite zu verlieren schmerzt mehr, als 10 zu gewinnen erfreut. Die klassische gewichtete Summe ignoriert diese Asymmetrie und behandelt Gewinn und Verlust als symmetrisch — **was kein menschlicher Entscheider tut.** Der Faktor `θ` kalibriert das Ausmaß: `θ < 1` verstärkt die Verlustaversion.

### SAPEVO-M — das Gremium, das sich nicht einig ist
Alle anderen Methoden verlangen einen Gewichtsvektor. **Woher kommt er, wenn fünf Entscheider unterschiedlicher Meinung sind?** SAPEVO-M löst das an der Quelle: jeder Entscheider äußert eine **ordinale** Präferenz („Reichweite ist viel wichtiger als Preis“, auf einer Sieben-Punkte-Skala), und die Methode aggregiert **ohne eine vorherige Konsensordnung zu verlangen**. So spricht ein Gremium tatsächlich — niemand sagt „Reichweite ist 0,237 wert“.

</details>

### Die Konsens-Engine

```
DEMATEL ──► Gewichte nach Einfluss ──► 10 Methoden ──► Borda-Konsens ──► Sieger
                                                    │
                        2.000 Dirichlet-Universen ─────────────────┘
                                    ▼
                     Urteil: ROBUSTO / PROVÁVEL / FRÁGIL
```

| Urteil | Konfidenz | Was zu tun ist |
|---|---|---|
| 🟢 **ROBUST** | ≥ 90% | Die Wahl hängt nicht von der Feinjustierung ab. **Sie können sie ins Gremium tragen.** |
| 🟡 **WAHRSCHEINLICH** | 60–90% | Sie hält in den meisten Szenarien, aber der Zweite ist konkurrenzfähig. **Vergleichen Sie beide.** |
| 🔴 **FRAGIL** | < 60% | Der erste Platz ist ein **Artefakt der Gewichte**. Entscheiden Sie nicht allein nach dem Ranking: gehen Sie zum Entscheidungsträger zurück und kalibrieren Sie neu. |

---

## 🔬 Zwei unabhängige Engines: die Kreuzprüfung

> [!TIP]
> **Warum alles noch einmal in Rust implementieren?** Weil „der Code läuft“ kein Beleg dafür ist, dass die **Mathematik** stimmt.

Ein Formel-Übertragungsfehler wiederholt sich selten **identisch** in zwei Sprachen mit unabhängiger linearer Algebra. Die Python-Engine nutzt NumPy/LAPACK; die Rust-Engine implementiert Gauß-Elimination mit Teilpivotisierung und die Potenzmethode **von Hand, ohne jede externe Abhängigkeit**.

```bash
python3 exportar_rust.py
```
```
✅ smartphone           8 identische Methoden · Sieger=C     (Δ ≤ 4.7e-11)
✅ veiculo_eletrico     8 identische Methoden · Sieger=EV6   (Δ ≤ 4.1e-11)
✅ caca_multifuncao     8 identische Methoden · Sieger=C3    (Δ ≤ 4.5e-11)
✅ blindado             8 identische Methoden · Sieger=B3    (Δ ≤ 4.6e-11)
✅ portfolio_startup    8 identische Methoden · Sieger=P3    (Δ ≤ 4.9e-11)
✅ estacao_trabalho     8 identische Methoden · Sieger=W5    (Δ ≤ 5.0e-11)
```

**Bonus: das Rust-Binary braucht kein Python, kein NumPy, kein numba und keine virtuelle Umgebung. Wenige MB, die auf Server, Container oder eingebetteter Maschine laufen — was zählt, wenn die Engine ein System im Feld begleitet.**

---

## 🚀 Performance: 26× schneller, dieselbe Antwort

Die Robustheitsanalyse führt 2.000 Universen × 10 Methoden aus. Die naive Implementierung brauchte **42 Sekunden** pro Fall.

<div align="center">

| Stufe | Zeit | Beschleunigung |
|---|---|---|
| JIT-Kernel pro Universum | 42,33 s | — |
| **Vorkompilierung in Tensoren** | 2,41 s | **17,6×** |
| `ranks` unter JIT + Zustand pro Prozess | **1,63 s** | **26,0×** |

</div>

> **Die Optimierung mit dem größten Ertrag war weder Parallelität noch JIT.** Es war die Erkenntnis, dass vier der neun Methoden **linear im Gewichtsvektor** sind — was erlaubt, Tensoren vorzuberechnen und jedes Universum auf ein Matrix-Vektor-Produkt zu reduzieren. **Algebra vor Infrastruktur.**

Und das Ergebnis ist **bitgenau identisch** mit dem langsamen Pfad — 100 Universen × 10 Methoden bei jedem Suite-Lauf geprüft. Eine Optimierung, die das Ergebnis verändert, ist ein Fehler, kein Gewinn.

<details>
<summary><b>Ausführungsrichtlinie des Projekts</b></summary>

| Regel | Anwendung |
|---|---|
| **Parallelität** | `ProcessPoolExecutor` für CPU-gebundene Arbeit; niemals Threads (der GIL serialisiert) |
| **Schwelle** | Seriell oder parallel wird nach der **Arbeit** entschieden (`n_iter · m² · k`), nicht nach der Anzahl der Elemente — ein kleines Problem zu parallelisieren ist **langsamer**, als es zu lösen |
| **JIT** | `numba` mit `cache=True` auf O(m²k)-Kernels; degradiert zu reinem NumPy, falls nicht vorhanden |
| **Hintergrund** | `screen`, niemals `nohup` — erlaubt Wiederanhängen und Interaktion |
| **Reproduzierbarkeit** | Feste, von der Prozessanzahl unabhängige Partitionierung: gleicher Seed → identisches Ergebnis mit 1 oder 32 Prozessen |

</details>

---

## 🌐 12 Sprachen — SDL Trados Translation Memory

Das ist keine maschinelle Übersetzung eines README. Es ist eine **Lokalisierungspipeline** mit Translation Memory im Standard **SDL Trados Studio**.

```
translation.memory.md          ← kanonische Quelle, in git versioniert
   │  --tm
   ▼
strings.<locale>.json          ← konsumiertes Artefakt
   │  --paginas
   ▼
12 Dashboard-Seiten + 12 READMEs
   │  --tmx
   ▼
translation.memory.tmx         ← in SDL Trados Studio importierbar
```

| Element | Zahlen |
|---|---|
| Locales | **12** (pt-BR · en · es · fr · de · zh · ko · hi · **he RTL** · ru · sv · fi) |
| Übersetzungseinheiten | 56 |
| Glossarbegriffe (MultiTerm) | 22 |
| Segmente im TMX | **948** |
| Kodierung | UTF-8 · LF · NFC |

```bash
python3 gerar_i18n.py --verificar
```

Die QA bildet Trados **Verify** nach: terminologische Konsistenz, erhaltene Placeables, Segmentabdeckung, strikte Kodierung und unangetastete Nicht-Übersetzbare — mit einer nach Schriftsystem differenzierten Regel (technische Kürzel bleiben in jeder Sprache lateinisch; Eigennamen werden **transliteriert**, wo die Schrift nicht lateinisch ist).

---

## 📁 Was drin ist

```
multicriteriadecisionmodels/
├── README.md (+11)                     Schaufenster in 12 Sprachen
├── docs/                               Logo und README-Ansichten
│
└── public/foundations/
    ├── pipeline/                       PYTHON-ENGINE (Referenz)
    │   ├── nucleo.py                   DEMATEL · ELECTRE I/II · PROMETHEE II
    │   │                               MAUT · MCDA-C · AHP · TOPSIS 2N
    │   ├── metodos_br.py               SAPEVO-M · VIKOR · TODIM · Copeland
    │   ├── robustez.py                 Dirichlet + ProcessPoolExecutor
    │   ├── pipeline.py                 Orchestrator
    │   ├── gerar_graficos.py           5 Ansichten pro Fall
    │   ├── gerar_i18n.py               TM → Strings → Seiten → TMX
    │   ├── testes_nucleo.py            16 mathematische Prüfungen
    │   ├── exportar_rust.py            Abgleich zwischen Engines
    │   ├── casos/catalogo.py           6 Fälle + Validierung
    │   └── run_all.sh                  Pipeline (screen)
    │
    ├── rust/mcdm_core/                 RUST-ENGINE (Verifikation + Verteilung)
    │   └── src/lib.rs                  alle Methoden, null Abhängigkeiten
    │
    └── evidence/                       DASHBOARD (Evidence.dev)
        ├── sources/mcdm/               11 SQL-Abfragen
        └── pages/                      12 Sprachrouten
```

---

## 🧠 Fundierung

Das Projekt baut auf begutachteter Literatur auf, nicht auf Intuition. Die Integrationsarchitektur folgt **John (2025)**, *„Integration of DEMATEL with Other MCDM Methods for Comprehensive Techno-Economic Analysis“*: DEMATEL legt die Kausalstruktur offen und leitet **Gewichte nach Einfluss** ab, die dann die Ranking-Methoden speisen — statt willkürlich gesetzter Gewichte.

Die Methoden der **brasilianischen Schule der multikriteriellen Entscheidungsunterstützung** (SAPEVO-M, TODIM-FSE, ELECTRE II, VIKOR, ordinale Methoden) folgen den Arbeiten von **IME**, **UFF**, **CASNAV**, **AMAN** und **FURB** — einschließlich realer Anwendungen auf die **Bewertung von Drohnen für die Seekriegführung**, die **Klassifizierung einer Brigade-Logistikbasis** und die **Rangfolge von Korvetten für die brasilianische Marine**.

> [!NOTE]
> **Die Urheberschaft der Methoden liegt vollständig bei ihren Schöpfern,** einzeln genannt in den Kopfzeilen von `nucleo.py` und `metodos_br.py`. Dieses Projekt steuert die Implementierung, die Integration und die Konsens-Engine bei — **nicht die Methoden**.

---

## ❓ Fragen, die Sie stellen werden

<details>
<summary><b>Ich nutze bereits eine gewichtete Entscheidungsmatrix. Ist das nicht dasselbe?</b></summary>

Nein, aus drei Gründen. **(1)** Eine gewichtete Matrix ist **eine** Methode (gewichtete Summe) mit eingebauter Theorie: vollständige Kompensation. Sie unterstellt, eine miserable Leistung bei einem Kriterium lasse sich anderswo ausgleichen — was bei Sicherheit, Panzerschutz und regulatorischer Konformität falsch ist. **(2)** Sie unterstellt unabhängige Kriterien, und Sie addieren fast immer, was bereits addiert ist. **(3)** Sie liefert eine Zahl ohne Konfidenzintervall und überlebt daher die erste Frage des Gremiums nicht.
</details>

<details>
<summary><b>Wie wähle ich die Gewichte?</b></summary>

Sie wählen sie nicht — **drei Wege leiten sie ab**. **DEMATEL** gewinnt sie aus der von Ihnen erklärten Kausalstruktur (wer wen beeinflusst). Der **AHP** gewinnt sie aus paarweisen Vergleichen, mit einer Konsistenzprüfung, die widersprüchliches Urteil **zurückweist**. **SAPEVO-M** gewinnt sie aus dem ordinalen Urteil mehrerer Entscheider. Und danach fragt die Robustheitsanalyse, wie stark das Ergebnis noch von ihnen **abhängt**.
</details>

<details>
<summary><b>Und wenn mein Problem 200 Alternativen hat?</b></summary>

Es läuft. Die Parallelitätsschwelle erkennt das Regime und verteilt auf Prozesse. Gemessen: 60 Alternativen × 12 Kriterien × 2.000 Universen in 3,8 s mit 4 Prozessen. Oberhalb von rund 700 Alternativen überschreitet der Präferenztensor das konfigurierte Speicherlimit, und die Engine warnt, statt hängen zu bleiben.
</details>

<details>
<summary><b>Die Methoden waren uneins. Und jetzt?</b></summary>

**Das ist das Produkt, nicht das Problem.** Die Abweichung sagt Ihnen, dass Ihre Entscheidung von der gewählten Schule abhängt — und benennt welche. Wenn ELECTRE denjenigen abwertet, den alle anderen wählen, gibt es ein Kriterium, bei dem diese Alternative schwerwiegend genug für ein Veto ist. Tragen Sie **das** ins Gremium, nicht das Ranking.
</details>

<details>
<summary><b>Kann ich meine eigenen Daten verwenden?</b></summary>

Dafür ist es da. Ein Fall ist eine deklarative Struktur in `casos/catalogo.py`: Kriterien (mit Richtung und Einheit), Alternativen, Entscheidungsmatrix, DEMATEL-Kausalmatrix und Saaty-Matrix. Der Validator weist einen fehlerhaften Fall **vor** jeder Berechnung zurück — inkohärente Dimensionen, falsche Diagonale, nicht-reziproke Saaty-Matrix, konstantes Kriterium, das nichts unterscheidet.
</details>

---

## 📜 Lizenz und Urheberschaft

<div align="center">

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="420"/>

**ProfBru © 2026**

**MCDM Studio — Multikriterielle Entscheidungsmodelle**
Autor: **ProfBru - Bruno Penedo** © 2026 — **ALLE RECHTE VORBEHALTEN**
📧 profbruanbima@gmail.com

</div>

**Proprietäres** Projekt. Dieses Repository gewährt keine Lizenz zur Nutzung, Vervielfältigung, Änderung, Verbreitung oder Erstellung abgeleiteter Werke. Kommerzielle, akademische oder institutionelle Nutzung erfordert die schriftliche Genehmigung des Autors.

**Zuschreibung Dritter:** die multikriteriellen Methoden stammen von ihren jeweiligen Schöpfern — Saaty, Roy, Bertier, Brans, Vincke, Keeney, Raiffa, Ensslin, Montibeller, Noronha, Gabus, Fontela, Opricovic, Tzeng, Hwang, Yoon, Kahneman, Tversky, Borda, Copeland, Gomes, Lima, Santos, Teixeira, Moreira, Rangel, Neves, Hein, Kroenke, Keunecke und Gomes Júnior — einzeln im Quellcode genannt.
