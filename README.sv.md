<!--
MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
-->

<div align="center">

# 🎯 MCDM Studio — Multikriteriella beslutsmodeller

<img src="docs/logo_capa.png" alt="ProfBru" width="320"/>

**ProfBru © 2026**

### Sluta välja med kalkylblad. Börja besluta med bevis.

**Nio beslutsskolor. En vinnare. Och — för första gången — sannolikheten att den vinnaren är rätt.**

[![MCDM](https://img.shields.io/badge/MCDM_metoder-9-2563eb?style=for-the-badge)](#-de-nio-beslutsskolorna--och-varför-nio)
[![Engines](https://img.shields.io/badge/Motorer-Python_+_Rust-c2410c?style=for-the-badge)](#-två-oberoende-motorer-korskontrollen)
[![i18n](https://img.shields.io/badge/Språk-12-16a34a?style=for-the-badge)](#-12-språk--sdl-trados-översättningsminne)
[![Robustez](https://img.shields.io/badge/Simulerade_universum-2.000-8f3d56?style=for-the-badge)](#-frågan-ingen-besvarar-tänk-om-vikterna-är-fel)

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Rust](https://img.shields.io/badge/Rust-1.96-000000?logo=rust&logoColor=white)](https://www.rust-lang.org)
[![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?logo=numpy&logoColor=white)](https://numpy.org)
[![Numba](https://img.shields.io/badge/Numba-JIT-00A3E0?logo=numba&logoColor=white)](https://numba.pydata.org)
[![Evidence](https://img.shields.io/badge/Evidence.dev-Dashboard-f4b548)](https://evidence.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/Licens-Proprietär-red)](#-licens-och-upphovsrätt)

🌐 [Português](README.md) · [English](README.en.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [中文](README.zh.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [עברית](README.he.md) · [Русский](README.ru.md) · **Svenska** · [Suomi](README.fi.md)

</div>

---

## 💀 Smärtan: du har redan förlorat pengar på grund av ett kalkylblad

Tänk på det senaste dyra beslut du fattade. Att köpa bilen. Att välja leverantören. Att godkänna projektet. Att bestämma den bärbara dator som 200 personer ska använda i fyra år.

**Du öppnade ett kalkylblad. Alternativen i raderna, attributen i kolumnerna. Och sedan gjorde du en av dessa tre saker:**

| Vad du gjorde | Vad som faktiskt hände |
|---|---|
| 🔻 **Sorterade efter priskolumnen** | Du valde det billigaste. Till det behövde du inget kalkylblad. |
| 🔺 **Sorterade efter expertbetyget** | Du valde det dyraste. Till det behövde du inte heller något. |
| 🔍 **Filtrerade på ”uppfyller alla krav”** | Listan blev tom. Så du mjukade upp ett krav. Vilket? **Det som var i vägen.** |

> [!WARNING]
> **Alla tre operationerna har samma brist: ingen av dem besvarar frågan du ställde.**
> Frågan var *”vilket ska jag välja bland alternativ som motsäger varandra?”* — och att sortera efter en kolumn är per definition att besluta utifrån **ett** kriterium. De andra sju använde du aldrig. De fanns där bara för att du skulle känna dig tryggare.

Och så finns problemet som ingen ser: **du summerade sådant som redan var summerat.** Du gav 20 % till ”energiförbrukning” och 25 % till ”räckvidd” — men förbrukningen *orsakar* räckvidden. Du räknade samma sak två gånger och kallade det analys.

### Ögonblicket då beslutet dör

Det sker på mötet. Du presenterar rankningen. Någon i kommittén frågar:

> *Och om räckvidden vore värd 30 % i stället för 25 %?*

Och du vet inte. **Ingen vet.** För kalkylbladet returnerar **ett** tal, med en underförstådd säkerhet på 100 % som det omöjligt kan ha. Du kommer tillbaka med läxan gjord, justerar vikterna och upptäcker att tvåan blir etta med **två procentenheters** skillnad.

Den ”vinnaren” var aldrig någon vinnare. Den var en **artefakt av din kalibrering** — och du var nära att skriva under.

---

## 💊 Lösningen: nio skolor, en konsensus och ett konfidensintervall

**MCDM Studio kör **nio etablerade multikriteriella metoder** på samma problem, härleder vinnaren ur **konsensus** mellan dem, och gör sedan det enda som verkligen betyder något:**

> ### 🎲 Den stör vikterna **2 000 gånger** och räknar i hur många universum vinnaren fortsätter att vinna.

Utlåtandet upphör att vara ett tal och blir en **mening som överlever kommittén**:

<div align="center">

| ❌ Vad kalkylbladet säger | ✅ Vad MCDM Studio säger |
|---|---|
| ”Modell C är bäst.” | **”Modell C vinner i 96 % av de rimliga preferensuniversumen. Utlåtande ROBUST: valet beror inte på finjustering av vikterna.”** |
| *(inget svar)* | **”Modell A vinner i 51 %. Utlåtande BRÄCKLIGT: förstaplatsen är en artefakt av vikterna. Besluta inte enbart utifrån rankningen.”** |

</div>

**Lägg märke till det andra fallet. Ett hederligt system måste kunna säga *”lita inte på mig här”*. Det är skillnaden mellan beslutsstöd och en generator av efterhandsmotiveringar för det beslut du redan ville fatta.**

---

## 🖼️ Se det fungera

### 1. Vem är orsak och vem är verkan — före all viktning

<div align="center"><img src="docs/telas/caca_multifuncao/dematel_causa_efeito.png" alt="DEMATEL" width="820"/></div>

**Smärtan detta löser:** du sätter vikter under antagandet att kriterierna är oberoende. **Det är de nästan aldrig.** Energiförbrukning *orsakar* räckvidd. Pansar *orsakar* vikt, som *orsakar* förlorad rörlighet. Att addera dem som oberoende är dubbelräkning.

**DEMATEL** bygger totalrelationsmatrisen `T = X(I−X)⁻¹` — som summerar direkt **och indirekt** påverkan av godtycklig väglängd — och skiljer det du kan **dra i** (orsaker, ovanför linjen) från det som bara **mäter resultatet** (verkningar, nedanför). Vikterna kommer därifrån: från systempåverkan, inte från magkänsla.

> I fallet ovan är **teknologiöverföring** och **radarsignatur** ORSAKER: att röra dem rör hela systemet. **Flottans tillgänglighet** är en VERKAN — en termometer, inte en hävstång. En upphandling som poängsätter tillgänglighet och bortser från teknologiöverföring mäter febern och struntar i infektionen.

### 2. Nio skolor på samma problem

<div align="center"><img src="docs/telas/veiculo_eletrico/mapa_metodos.png" alt="Métodos" width="900"/></div>

**Smärtan detta löser:** varje MCDM-metod bär en inbyggd teori om vad ”bättre” betyder — och den ändrar vinnaren. Att välja en metod och presentera resultatet är att välja resultatet.

Vi kör alla nio. När de är eniga är valet **ingen metodartefakt**. När de skiljer sig åt **är avvikelsen fyndet**.

> Ovan: **laddhybriden** är etta i sju metoder men **sexa i ELECTRE I**. Det är inte brus — det är information. ELECTRE I tillåter *veto*: den säger att hybriden har en nackdel som är allvarlig nog i något kriterium för att sållas bort, hur bra den än är i övrigt. **Det är precis den frågan du vill ta till kommittén.**

### 3. Konfidensintervallet för själva beslutet

<div align="center"><img src="docs/telas/portfolio_startup/robustez.png" alt="Robustez" width="820"/></div>

**Smärtan detta löser:** kommitténs fråga — *”och om vikten vore en annan?”*. Besvarad **innan** någon hinner ställa den.

Vi stör vikterna med `w' ~ Dirichlet(κ·w)` och rankar om 2 000 gånger. Dirichlet är det naturliga valet: dess stöd är exakt simplexet (positiva vikter med summan 1) och den uppfyller `E[w'] = w` — vi stör alltså **utan att snedvrida**.

### 4. Där din intuition har fel

<div align="center"><img src="docs/telas/blindado/pesos_dematel_ahp.png" alt="DEMATEL x AHP" width="820"/></div>

**Smärtan detta löser:** du tror att du vet vad som är viktigt. Två viktfamiljer prövar det.

**AHP** (Saaty) frågar parvis hur mycket viktigare ett kriterium är än ett annat. **DEMATEL** mäter systempåverkan. **Där de skiljer sig åt finns andra ordningens effekt som du underskattade** — och diagrammet markerar den största avvikelsen i rött.

### 5. Var varje alternativ hamnar, över 2 000 scenarier

<div align="center"><img src="docs/telas/estacao_trabalho/distribuicao_posicoes.png" alt="Distribuição" width="820"/></div>

En helt grön stapel är en placering som **inte beror på vikterna**. En spräcklig stapel är en omstridd placering. Du ser på ett ögonkast var rankningen är fakta och var den är åsikt.

---

## 🎯 Vad det är till för — det skräddarsydda valet

Motorn är **domänoberoende**: enheten är *beslutsfallet* (alternativ × kriterier), utan inbyggd verksamhetssemantik. Att byta domän är att byta data, inte kod.

<div align="center">

| Domän | Beslutet | Den specifika smärtan |
|---|---|---|
| 📱 **Elektronik** | Telefon, laptop, utrustning | Den billigaste har sämst kamera; den med bäst kamera har sämst batteri. ”Bäst” finns inte — det finns **bäst för din användning**. |
| 🚗 **Elbilar** | Fordonsflotta eller privat bruk | Räckvidd, laddning, servicenät och andrahandsvärde drar åt motsatta håll. Och det avgörande kriteriet (**verklig räckvidd**, inte katalogens) är svårast att mäta. |
| 🎖️ **Försvar** | Stridsflygplan, pansarfordon, drönare, logistikbas | 30 års livscykel, oåterkallelig, under offentlig granskning. **Styckpriset är mindre än en tredjedel av totalkostnaden.** Teknologiöverföring och timkostnad avgör tre decenniers budget. |
| 🏢 **Företag** | Leverantör, ERP, outsourcing, expansion | En kommitté som inte är överens med sig själv. **SAPEVO-M** byggdes just för detta: den aggregerar ordinala bedömningar från **flera beslutsfattare** utan att kräva förhandskonsensus. |
| 🚀 **Startups** | Projektportfölj, kapitalallokering | Den som beslutar efter förväntad avkastning väljer alltid den mest riskfyllda satsningen — **väntevärdet bortser från svansen**. Här är risk ett **kriterium**, inte en fotnot på bild 14. |
| 💻 **IT** | Standardisering av utrustningsparken | Beslutet multipliceras med 200 och varar i 4 år. Batteritid och garanti på plats är värda mer, i total ägandekostnad, än två poäng i ett syntetiskt benchmark. |

</div>

### Färdiga fall att köra

```bash
python3 pipeline.py --listar
```

| Fall | Domän | Alternativ | Kriterier |
|---|---|---|---|
| `smartphone` | konsument | 6 | 8 |
| `veiculo_eletrico` | fordon | 7 | 8 |
| `caca_multifuncao` | försvar | 6 | 9 |
| `blindado` | försvar | 5 | 8 |
| `portfolio_startup` | företag | 7 | 9 |
| `estacao_trabalho` | IT | 6 | 8 |

> [!NOTE]
> Fallens matriser är **illustrativa** — offentliga och rimliga storleksordningar för att demonstrera metoden. Det som **inte** är illustrativt är **modelleringen**: kriterier, riktningar, DEMATEL:s kausalmatris och Saaty-matrisen. Där ligger värdet. **Byt ut siffrorna mot din offert, din upphandling eller ditt labbtest** — motorn är densamma; datan är din.

---

## ⚡ Installation

### Snabbaste vägen (Python)

```bash
git clone <url> multicriteriadecisionmodels
cd multicriteriadecisionmodels/public/foundations/pipeline
pip install -r requirements.txt
python3 pipeline.py
```

Klart. Alla sex fallen körs, med fullständig rapport.

<details>
<summary><b>Detaljerade förutsättningar</b></summary>

| Komponent | Lägsta version | Obligatorisk? | Till vad |
|---|---|---|---|
| Python | 3.10 | ✅ | referensmotor |
| NumPy | 2.0 | ✅ | algebran för alla metoder |
| numba | 0.60 | ⚠️ | JIT för kärnorna — utan den samma resultat, bara långsammare |
| SciPy | 1.10 | ✅ | hjälpstatistik |
| matplotlib | 3.7 | ✅ | de 5 vyerna per fall |
| Rust / cargo | 1.75 | ⭕ | motor för korskontroll |
| Node.js | 18 | ⭕ | Evidence-instrumentpanel |
| screen | — | ⭕ | körning i bakgrunden |

</details>

### Fullständig kedja

```bash
./run_all.sh                    # tester → pipeline → vyer → i18n → Rust → avstämning
./run_all.sh --rapido           # hoppar över Rust och i18n
./run_all.sh --caso smartphone  # ett enda fall
./run_all.sh --background       # kör i screen (återanslut: screen -r mcdm)
```

### Rust-motor — binär utan runtime

```bash
cd public/foundations/rust/mcdm_core
cargo test --release
cargo build --release

./target/release/mcdm --exemplo > problema.mcdm
./target/release/mcdm problema.mcdm
./target/release/mcdm problema.mcdm --json
```

### Instrumentpanel

```bash
cd public/foundations/evidence
npm install
npm run dev               # http://localhost:3000
```

<details>
<summary><b>Avancerade kommandon</b></summary>

```bash
python3 pipeline.py caca_multifuncao --workers 8 --iter 5000
python3 testes_nucleo.py
python3 exportar_rust.py
python3 gerar_i18n.py --tudo
python3 gerar_i18n.py --verificar
python3 gerar_graficos.py --workers 6
```

| Variabel | Standard | Effekt |
|---|---|---|
| `MCDM_WORKERS` | auto | processer i `ProcessPoolExecutor` |
| `MCDM_NUMBA` | `1` | JIT på; `0` för felsökning i ren NumPy |
| `MCDM_SEED` | `42` | reproducerbarhet |
| `ROBUSTEZ_ITER` | `2000` | preferensuniversum |
| `ROBUSTEZ_KAPPA` | `200` | Dirichlets koncentration (högre = vikterna ligger närmare ursprunget) |
| `MAUT_AVERSAO` | `2.0` | riskaversion (r > 0 = konkav) |
| `PROMETHEE_TIPO` | `linear` | preferensfunktion (6 tillgängliga) |

</details>

---

## ⚖️ De nio beslutsskolorna — och varför nio

> [!IMPORTANT]
> **Varje metod är en annan teori om vad ”bättre” betyder.** Att bara använda en är att välja svaret tillsammans med frågan. Vi kör alla nio eftersom **samstämmighet mellan oberoende teorier** är det starkaste belägg ett beslutsproblem tillåter.

<div align="center">

| Metod | Skola | Vad den antar | När den är **rätt** verktyg | Ursprung |
|---|---|---|---|---|
| **AHP-TOPSIS 2n** | avstånd till idealet | full kompensation | kvantitativa kriterier, en enda beslutsfattare | Saaty (1980); Hwang & Yoon (1981) |
| **ELECTRE I** | överklassificering | ojämförbarhet tillåts | **gallring**: rensa bort det dominerade | Roy (1968) |
| **ELECTRE II** | överklassificering | stark och svag tröskel | fullständig ordning **med veto** | Roy & Bertier (1971) |
| **PROMETHEE II** | överklassificering | gradvis preferens (6 funktioner) | när ”lite bättre” ≠ ”bättre” | Brans & Vincke (1985) |
| **MAUT** | nytta | additiv oberoende + riskaversion | beslut under osäkerhet | Keeney & Raiffa (1976) |
| **MCDA-C** | konstruktivistisk | förankrade nivåer Neutral/Bra | **absolut diagnos**, inte bara rankning | Ensslin, Montibeller & Noronha (2001) |
| **VIKOR** | kompromiss | gruppnytta × maximal ånger | när **kompensation är oacceptabel** | Opricovic (1979); Opricovic & Tzeng (2002-07) |
| **TODIM** | prospektteori | en förlust svider mer än en likvärdig vinst gläder | förlustavert beslutsfattare — **det är alla** | Gomes & Lima (1992); Kahneman & Tversky (1979) |
| **SAPEVO-M** | ordinal, flera beslutsfattare | ordinal bedömning från flera beslutsfattare | **kommitté som inte är överens** | Gomes et al. (1997); Teixeira, Santos & Gomes (2019) |

</div>

<details>
<summary><b>Varför dessa tre förtjänar särskild uppmärksamhet</b></summary>

### VIKOR — när kompensation är oacceptabel
VIKOR beräknar **två** mått: `S` (gruppnytta — viktad summa, som **accepterar** att en usel prestation vägs upp av flera bra) och `R` (maximal individuell ånger — minimax, som **avvisar** kompensation).

Ett pansarfordon med utmärkt rörlighet och usel skyddsnivå får ett optimalt `S` och ett katastrofalt `R`. Den viktade summan skulle välja det; VIKOR flaggar. Och när `S` och `R` går isär rapporterar villkoren **C1** (godtagbart försprång) och **C2** (godtagbar stabilitet) uttryckligen att beslutet har en blind fläck.

### TODIM — förlusten svider mer än vinsten
Bygger på Kahneman och Tverskys **prospektteori**: att förlora 10 poäng räckvidd svider mer än att vinna 10 gläder. Den klassiska viktade summan bortser från denna asymmetri och behandlar vinst och förlust som symmetriska — **vilket ingen mänsklig beslutsfattare gör.** Faktorn `θ` kalibrerar hur mycket: `θ < 1` förstärker förlustaversionen.

### SAPEVO-M — kommittén som inte är överens
Alla andra metoder kräver en viktvektor. **Varifrån kommer den när fem beslutsfattare tycker olika?** SAPEVO-M löser det vid källan: varje beslutsfattare uttrycker **ordinal** preferens (”räckvidd är mycket viktigare än pris”, på en sjugradig skala), och metoden aggregerar **utan att kräva en förhandsordning i konsensus**. Så uttrycker sig en kommitté i verkligheten — ingen säger ”räckvidd är värd 0,237”.

</details>

### Konsensusmotorn

```
DEMATEL ──► vikter efter påverkan ──► 9 metoder ──► Borda-konsensus ──► vinnare
                                                    │
                        2 000 Dirichlet-universum ─────────────────┘
                                    ▼
                     utlåtande: ROBUSTO / PROVÁVEL / FRÁGIL
```

| Utlåtande | Konfidens | Vad man ska göra |
|---|---|---|
| 🟢 **ROBUST** | ≥ 90% | Valet beror inte på finjustering. **Det kan tas till kommittén.** |
| 🟡 **SANNOLIKT** | 60–90% | Det håller i de flesta scenarier, men tvåan är konkurrenskraftig. **Jämför båda.** |
| 🔴 **BRÄCKLIGT** | < 60% | Förstaplatsen är en **artefakt av vikterna**. Besluta inte enbart utifrån rankningen: gå tillbaka till beslutsfattaren och omkalibrera. |

---

## 🔬 Två oberoende motorer: korskontrollen

> [!TIP]
> **Varför implementera om allt i Rust?** För att ”koden kör” inte är något belägg för att **matematiken** stämmer.

Ett transkriptionsfel i en formel upprepas sällan **identiskt** i två språk med oberoende linjär algebra. Python-motorn använder NumPy/LAPACK; Rust-motorn implementerar Gausselimination med partiell pivotering och potensmetoden **för hand, utan en enda extern beroende**.

```bash
python3 exportar_rust.py
```
```
✅ smartphone           8 identiska metoder · vinnare=C     (Δ ≤ 4.7e-11)
✅ veiculo_eletrico     8 identiska metoder · vinnare=EV6   (Δ ≤ 4.1e-11)
✅ caca_multifuncao     8 identiska metoder · vinnare=C3    (Δ ≤ 4.5e-11)
✅ blindado             8 identiska metoder · vinnare=B3    (Δ ≤ 4.6e-11)
✅ portfolio_startup    8 identiska metoder · vinnare=P3    (Δ ≤ 4.9e-11)
✅ estacao_trabalho     8 identiska metoder · vinnare=W5    (Δ ≤ 5.0e-11)
```

**Bonus: Rust-binären behöver varken Python, NumPy, numba eller virtuell miljö. Några få MB som kör på server, i container eller på inbyggd maskin — vilket spelar roll när motorn följer med ett system ut i fält.**

---

## 🚀 Prestanda: 26× snabbare, samma svar

Robusthetsanalysen kör 2 000 universum × 9 metoder. Den naiva implementationen tog **42 sekunder** per fall.

<div align="center">

| Steg | Tid | Snabbare |
|---|---|---|
| JIT-kärnor per universum | 42,33 s | — |
| **Förkompilering till tensorer** | 2,41 s | **17,6×** |
| `ranks` under JIT + tillstånd per process | **1,63 s** | **26,0×** |

</div>

> **Den optimering som gav mest var varken parallellism eller JIT.** Det var insikten att fyra av de nio metoderna är **linjära i viktvektorn** — vilket gör det möjligt att förberäkna tensorer och reducera varje universum till en matris-vektor-produkt. **Algebra före infrastruktur.**

Och resultatet är **bit för bit identiskt** med den långsamma vägen — 100 universum × 9 metoder verifieras vid varje körning av sviten. En optimering som ändrar resultatet är en defekt, inte en vinst.

<details>
<summary><b>Projektets körpolicy</b></summary>

| Regel | Tillämpning |
|---|---|
| **Parallellism** | `ProcessPoolExecutor` för CPU-bundet arbete; aldrig trådar (GIL serialiserar) |
| **Tröskel** | Seriellt eller parallellt avgörs av **arbetsmängden** (`n_iter · m² · k`), inte av antalet poster — att parallellisera ett litet problem är **långsammare** än att lösa det |
| **JIT** | `numba` med `cache=True` på O(m²k)-kärnor; faller tillbaka på ren NumPy om den saknas |
| **Bakgrund** | `screen`, aldrig `nohup` — tillåter återanslutning och interaktion |
| **Reproducerbarhet** | Fast partitionering, oberoende av antalet processer: samma frö → identiskt resultat med 1 eller 32 processer |

</details>

---

## 🌐 12 språk — SDL Trados översättningsminne

Detta är ingen maskinöversättning av en README. Det är en **lokaliseringspipeline** med översättningsminne enligt standarden **SDL Trados Studio**.

```
translation.memory.md          ← kanonisk källa, versionshanterad i git
   │  --tm
   ▼
strings.<locale>.json          ← konsumerad artefakt
   │  --paginas
   ▼
12 instrumentpanelssidor + 12 README-filer
   │  --tmx
   ▼
translation.memory.tmx         ← kan importeras i SDL Trados Studio
```

| Post | Siffror |
|---|---|
| Lokaler | **12** (pt-BR · en · es · fr · de · zh · ko · hi · **he RTL** · ru · sv · fi) |
| Översättningsenheter | 56 |
| Termpostar (MultiTerm) | 22 |
| Segment i TMX | **948** |
| Teckenkodning | UTF-8 · LF · NFC |

```bash
python3 gerar_i18n.py --verificar
```

Kvalitetskontrollen speglar Trados **Verify**: terminologisk konsekvens, bevarade placeables, segmenttäckning, strikt teckenkodning och orörda icke-översättbara element — med en regel som skiljer sig åt per skriftsystem (tekniska förkortningar förblir latinska på alla språk; egennamn **translittereras** där skriften inte är latinsk).

---

## 📁 Vad som finns inuti

```
multicriteriadecisionmodels/
├── README.md (+11)                     skyltfönster på 12 språk
├── docs/                               logotyp och vyer för README-filerna
│
└── public/foundations/
    ├── pipeline/                       PYTHON-MOTOR (referens)
    │   ├── nucleo.py                   DEMATEL · ELECTRE I/II · PROMETHEE II
    │   │                               MAUT · MCDA-C · AHP · TOPSIS 2N
    │   ├── metodos_br.py               SAPEVO-M · VIKOR · TODIM · Copeland
    │   ├── robustez.py                 Dirichlet + ProcessPoolExecutor
    │   ├── pipeline.py                 orkestrerare
    │   ├── gerar_graficos.py           5 vyer per fall
    │   ├── gerar_i18n.py               TM → strängar → sidor → TMX
    │   ├── testes_nucleo.py            16 matematiska kontroller
    │   ├── exportar_rust.py            avstämning mellan motorer
    │   ├── casos/catalogo.py           6 fall + validering
    │   └── run_all.sh                  kedja (screen)
    │
    ├── rust/mcdm_core/                 RUST-MOTOR (verifiering + distribution)
    │   └── src/lib.rs                  alla metoder, noll beroenden
    │
    └── evidence/                       INSTRUMENTPANEL (Evidence.dev)
        ├── sources/mcdm/               11 SQL-frågor
        └── pages/                      12 språkrutter
```

---

## 🧠 Grundvalar

Projektet vilar på granskad litteratur, inte på intuition. Integrationsarkitekturen följer **John (2025)**, *”Integration of DEMATEL with Other MCDM Methods for Comprehensive Techno-Economic Analysis”*: DEMATEL blottlägger den kausala strukturen och härleder **vikter efter påverkan**, som sedan matar rankningsmetoderna — i stället för godtyckligt satta vikter.

Metoderna från den **brasilianska skolan för multikriteriellt beslutsstöd** (SAPEVO-M, TODIM-FSE, ELECTRE II, VIKOR, ordinala metoder) följer arbeten från **IME**, **UFF**, **CASNAV**, **AMAN** och **FURB** — inklusive verkliga tillämpningar på **utvärdering av drönare för sjökrigföring**, **klassificering av en brigads logistikbas** och **rankning av korvetter för brasilianska flottan**.

> [!NOTE]
> **Upphovsrätten till metoderna tillhör helt och hållet deras skapare,** namngivna var för sig i sidhuvudena i `nucleo.py` och `metodos_br.py`. Projektet bidrar med implementationen, integrationen och konsensusmotorn — **inte metoderna**.

---

## ❓ Frågor du kommer att ställa

<details>
<summary><b>Jag använder redan en viktad beslutsmatris. Är det inte samma sak?</b></summary>

Nej, av tre skäl. **(1)** En viktad matris är **en** metod (viktad summa) med en inbyggd teori: full kompensation. Den förutsätter att en usel prestation i ett kriterium kan vägas upp på annat håll — vilket är falskt inom säkerhet, pansarskydd och regelefterlevnad. **(2)** Den förutsätter oberoende kriterier, och du summerar nästan alltid sådant som redan är summerat. **(3)** Den returnerar ett tal utan konfidensintervall och överlever därför inte kommitténs första fråga.
</details>

<details>
<summary><b>Hur väljer jag vikterna?</b></summary>

Du väljer dem inte — **tre vägar härleder dem**. **DEMATEL** utvinner dem ur den kausala struktur du deklarerar (vem påverkar vem). **AHP** utvinner dem ur parvisa jämförelser, med en konsistenskontroll som **underkänner** motsägelsefulla bedömningar. **SAPEVO-M** utvinner dem ur ordinala bedömningar från flera beslutsfattare. Och därefter frågar robusthetsanalysen hur mycket resultatet fortfarande **beror** på dem.
</details>

<details>
<summary><b>Och om mitt problem har 200 alternativ?</b></summary>

Det kör. Parallellismtröskeln känner av storleksordningen och fördelar på processer. Uppmätt: 60 alternativ × 12 kriterier × 2 000 universum på 3,8 s med 4 processer. Över ungefär 700 alternativ överskrider preferenstensorn den konfigurerade minnesgränsen, och motorn varnar i stället för att hänga sig.
</details>

<details>
<summary><b>Metoderna var oense. Vad gör jag nu?</b></summary>

**Det är produkten, inte problemet.** Avvikelsen säger att ditt beslut är känsligt för vald skola — och namnger vilken. Om ELECTRE nedgraderar den som alla andra väljer finns det ett kriterium där det alternativet är illa nog för veto. Ta **det** till kommittén, inte rankningen.
</details>

<details>
<summary><b>Kan jag använda mina egna data?</b></summary>

Det är precis vad det är till för. Ett fall är en deklarativ struktur i `casos/catalogo.py`: kriterier (med riktning och enhet), alternativ, beslutsmatris, DEMATEL:s kausalmatris och Saaty-matrisen. Valideraren avvisar ett felaktigt fall **före** varje beräkning — inkonsekventa dimensioner, fel diagonal, icke-reciprok Saaty-matris, ett konstant kriterium som inte skiljer något åt.
</details>

---

## 📜 Licens och upphovsrätt

<div align="center">

<img src="docs/logo_capa.png" alt="ProfBru" width="180"/>

**ProfBru © 2026**

**MCDM Studio — Multikriteriella beslutsmodeller**
Författare: **ProfBru - Bruno Penedo** © 2026 — **ALLA RÄTTIGHETER FÖRBEHÅLLNA**
📧 profbruanbima@gmail.com

</div>

**Proprietärt** projekt. Detta arkiv medger ingen licens att använda, kopiera, ändra, distribuera eller skapa bearbetningar. Kommersiell, akademisk eller institutionell användning kräver skriftligt tillstånd från upphovspersonen.

**Tredjepartsattribution:** de multikriteriella metoderna är skapade av sina respektive upphovspersoner — Saaty, Roy, Bertier, Brans, Vincke, Keeney, Raiffa, Ensslin, Montibeller, Noronha, Gabus, Fontela, Opricovic, Tzeng, Hwang, Yoon, Kahneman, Tversky, Borda, Copeland, Gomes, Lima, Santos, Teixeira, Moreira, Rangel, Neves, Hein, Kroenke, Keunecke och Gomes Júnior — namngivna var för sig i källkoden.
