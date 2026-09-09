<!--
MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
-->

<div align="center">

# 🎯 MCDM Studio — Monikriteeriset päätösmallit

<img src="docs/logo_capa.png" alt="ProfBru" width="320"/>

**ProfBru © 2026**

### Lopeta valitseminen taulukkolaskennalla. Ala päättää todisteiden pohjalta.

**Yhdeksän päätöksenteon koulukuntaa. Yksi voittaja. Ja — ensimmäistä kertaa — todennäköisyys sille, että voittaja on oikea.**

[![MCDM](https://img.shields.io/badge/MCDM_menetelmät-9-2563eb?style=for-the-badge)](#-yhdeksän-päätöksenteon-koulukuntaa--ja-miksi-yhdeksän)
[![Engines](https://img.shields.io/badge/Moottorit-Python_+_Rust-c2410c?style=for-the-badge)](#-kaksi-riippumatonta-moottoria-ristiintarkistus)
[![i18n](https://img.shields.io/badge/Kielet-12-16a34a?style=for-the-badge)](#-12-kieltä--sdl-trados-käännösmuisti)
[![Robustez](https://img.shields.io/badge/Simuloidut_universumit-2.000-8f3d56?style=for-the-badge)](#-kysymys-johon-kukaan-ei-vastaa-entä-jos-painot-ovat-väärin)

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Rust](https://img.shields.io/badge/Rust-1.96-000000?logo=rust&logoColor=white)](https://www.rust-lang.org)
[![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?logo=numpy&logoColor=white)](https://numpy.org)
[![Numba](https://img.shields.io/badge/Numba-JIT-00A3E0?logo=numba&logoColor=white)](https://numba.pydata.org)
[![Evidence](https://img.shields.io/badge/Evidence.dev-Dashboard-f4b548)](https://evidence.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/Lisenssi-Omisteinen-red)](#-lisenssi-ja-tekijyys)

🌐 [Português](README.md) · [English](README.en.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [中文](README.zh.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [עברית](README.he.md) · [Русский](README.ru.md) · [Svenska](README.sv.md) · **Suomi**

</div>

---

## 💀 Kipu: olet jo menettänyt rahaa taulukkolaskennan takia

Ajattele viimeisintä kallista päätöstäsi. Auton ostaminen. Toimittajan valinta. Projektin hyväksyminen. Sen kannettavan tietokoneen valinta, jota 200 ihmistä käyttää neljä vuotta.

**Avasit taulukon. Vaihtoehdot riveille, ominaisuudet sarakkeisiin. Ja sitten teit yhden näistä kolmesta:**

| Mitä teit | Mitä todella tapahtui |
|---|---|
| 🔻 **Lajittelit hintasarakkeen mukaan** | Valitsit halvimman. Siihen et olisi tarvinnut taulukkoa. |
| 🔺 **Lajittelit asiantuntija-arvion mukaan** | Valitsit kalleimman. Siihenkään et olisi tarvinnut sitä. |
| 🔍 **Suodatit ehdolla ”täyttää kaikki vaatimukset”** | Lista tyhjeni. Niinpä löysensit yhtä vaatimusta. Mitä? **Sitä, joka oli tiellä.** |

> [!WARNING]
> **Kaikissa kolmessa toimenpiteessä on sama vika: yksikään ei vastaa esittämääsi kysymykseen.**
> Kysymys oli *”mikä valita keskenään ristiriitaisista vaihtoehdoista?”* — ja sarakkeen mukaan lajittelu on määritelmän mukaan päättämistä **yhden** kriteerin perusteella. Niitä muita seitsemää et käyttänyt lainkaan. Ne olivat siellä vain rauhoittamassa mieltäsi.

Ja on se ongelma, jota kukaan ei näe: **lasket yhteen sen, mikä oli jo laskettu yhteen.** Annoit ”energiankulutukselle” 20 % ja ”toimintamatkalle” 25 % — mutta kulutus *aiheuttaa* toimintamatkan. Laskit saman asian kahdesti ja kutsuit sitä analyysiksi.

### Hetki, jolloin päätös kuolee

Se tapahtuu kokouksessa. Esität järjestyksen. Joku komiteasta kysyy:

> *Entä jos toimintamatka olisi 30 % eikä 25 %?*

Etkä tiedä. **Kukaan ei tiedä.** Sillä taulukko palauttaa **yhden** luvun, mukanaan sadan prosentin oletettu varmuus, jota sillä ei voi olla. Palaat kotiläksyt tehtyäsi, säädät painoja ja huomaat, että kakkonen nousee ykköseksi **kahden prosenttiyksikön** erolla.

Se ”voittaja” ei koskaan ollut voittaja. Se oli **kalibrointisi artefakti** — ja olit vähällä allekirjoittaa sen.

---

## 💊 Ratkaisu: yhdeksän koulukuntaa, yksi konsensus ja luottamusväli

**MCDM Studio ajaa **yhdeksän vakiintunutta monikriteerimenetelmää** samaan ongelmaan, johtaa voittajan niiden välisestä **konsensuksesta** ja tekee sitten sen ainoan asian, jolla on todella väliä:**

> ### 🎲 Se häiritsee painoja **2 000 kertaa** ja laskee, kuinka monessa universumissa voittaja yhä voittaa.

Tuomio lakkaa olemasta luku ja muuttuu **lauseeksi, joka kestää komitean**:

<div align="center">

| ❌ Mitä taulukko sanoo | ✅ Mitä MCDM Studio sanoo |
|---|---|
| ”Malli C on paras.” | **”Malli C voittaa 96 %:ssa uskottavista preferenssiuniversumeista. Tuomio ROBUSTI: valinta ei riipu painojen hienosäädöstä.”** |
| *(ei vastausta)* | **”Malli A voittaa 51 %:ssa. Tuomio HAURAS: ensimmäinen sija on painojen artefakti. Älä päätä pelkän järjestyksen perusteella.”** |

</div>

**Huomaa jälkimmäinen tapaus. Rehellisen järjestelmän on kyettävä sanomaan *”älä luota minuun tässä”*. Siinä on ero päätöksenteon tuen ja sen perustelugeneraattorin välillä, jonka päätöksen halusit tehdä joka tapauksessa.**

---

## 🖼️ Katso se toiminnassa

### 1. Kuka on syy ja kuka seuraus — ennen mitään painotusta

<div align="center"><img src="docs/telas/caca_multifuncao/dematel_causa_efeito.png" alt="DEMATEL" width="820"/></div>

**Kipu, jonka tämä poistaa:** annat painoja olettaen, että kriteerit ovat riippumattomia. **Ne eivät lähes koskaan ole.** Energiankulutus *aiheuttaa* toimintamatkan. Panssarointi *aiheuttaa* massan, joka *aiheuttaa* liikkuvuuden menetyksen. Niiden summaaminen riippumattomina on kaksinkertaista laskentaa.

**DEMATEL** muodostaa kokonaisrelaatiomatriisin `T = X(I−X)⁻¹` — joka summaa suorat **ja epäsuorat** vaikutukset minkä tahansa polun pituudelta — ja erottaa sen, mistä voi **vetää** (syyt, viivan yläpuolella), siitä, mikä vain **mittaa tulosta** (seuraukset, alapuolella). Painot syntyvät siitä: systeemisestä vaikutuksesta, ei mutu-tuntumasta.

> Yllä olevassa tapauksessa **teknologiansiirto** ja **tutkasignatuuri** ovat SYITÄ: niihin koskeminen liikuttaa koko järjestelmää. **Kaluston käytettävyys** on SEURAUS — lämpömittari, ei vipu. Tarjouspyyntö, joka pisteyttää käytettävyyden ja sivuuttaa teknologiansiirron, mittaa kuumetta ja jättää infektion huomiotta.

### 2. Yhdeksän koulukuntaa samaan ongelmaan

<div align="center"><img src="docs/telas/veiculo_eletrico/mapa_metodos.png" alt="Métodos" width="900"/></div>

**Kipu, jonka tämä poistaa:** jokaiseen MCDM-menetelmään on sisäänrakennettu teoria siitä, mitä ”parempi” tarkoittaa — ja se vaihtaa voittajan. Menetelmän valitseminen ja tuloksen esittäminen on tuloksen valitsemista.

Ajamme kaikki yhdeksän. Kun ne ovat yhtä mieltä, valinta **ei ole menetelmän artefakti**. Kun ne eroavat, **ero itsessään on löydös**.

> Yllä: **lataushybridi** on ensimmäinen seitsemässä menetelmässä mutta **kuudes ELECTRE I:ssä**. Se ei ole kohinaa — se on informaatiota. ELECTRE I sallii *veton*: se kertoo, että hybridillä on jossakin kriteerissä riittävän vakava haitta karsiutuakseen, olipa se muuten miten hyvä tahansa. **Juuri sen kysymyksen haluat viedä komitealle.**

### 3. Itse päätöksen luottamusväli

<div align="center"><img src="docs/telas/portfolio_startup/robustez.png" alt="Robustez" width="820"/></div>

**Kipu, jonka tämä poistaa:** komitean kysymys — *”entä jos paino olisi toinen?”*. Vastattu **ennen** kuin kukaan ehtii kysyä.

Häiritsemme painoja muodossa `w' ~ Dirichlet(κ·w)` ja järjestämme uudelleen 2 000 kertaa. Dirichlet on luonteva valinta: sen kantaja on täsmälleen simpleksi (positiiviset painot, summa 1) ja se toteuttaa `E[w'] = w` — häiritsemme siis **vinouttamatta**.

### 4. Missä intuitiosi on väärässä

<div align="center"><img src="docs/telas/blindado/pesos_dematel_ahp.png" alt="DEMATEL x AHP" width="820"/></div>

**Kipu, jonka tämä poistaa:** luulet tietäväsi, mikä on tärkeää. Kaksi painoperhettä koettelee sitä.

**AHP** (Saaty) kysyy pareittain, kuinka paljon tärkeämpi yksi kriteeri on toista. **DEMATEL** mittaa systeemistä vaikutusta. **Siellä missä ne eroavat, on se toisen kertaluvun vaikutus, jonka aliarvioit** — ja kuvaaja merkitsee suurimman eron punaisella.

### 5. Mihin kukin vaihtoehto päätyy 2 000 skenaariossa

<div align="center"><img src="docs/telas/estacao_trabalho/distribuicao_posicoes.png" alt="Distribuição" width="820"/></div>

Kokonaan vihreä palkki on sija, joka **ei riipu painoista**. Kirjava palkki on kiistelty sija. Näet yhdellä silmäyksellä, missä järjestys on tosiasia ja missä mielipide.

---

## 🎯 Mihin tämä on — räätälöity valinta

Moottori on **toimialariippumaton**: yksikkö on *päätöstapaus* (vaihtoehdot × kriteerit), ilman sisäänrakennettua liiketoimintasemantiikkaa. Toimialan vaihtaminen on datan vaihtamista, ei koodin.

<div align="center">

| Toimiala | Päätös | Erityinen kipu |
|---|---|---|
| 📱 **Elektroniikka** | Puhelin, kannettava, laitteisto | Halvimmassa on huonoin kamera; parhaassa kamerassa on huonoin akku. ”Parasta” ei ole olemassa — on **paras sinun käyttöösi**. |
| 🚗 **Sähköautot** | Kalusto tai henkilökohtainen käyttö | Toimintamatka, lataus, huoltoverkosto ja jälleenmyyntiarvo vetävät eri suuntiin. Ja ratkaiseva kriteeri (**todellinen toimintamatka**, ei esitteen luku) on vaikeimmin mitattava. |
| 🎖️ **Puolustus** | Hävittäjät, panssariajoneuvot, droonit, logistiikkatukikohta | 30 vuoden elinkaari, peruuttamaton, julkisen tarkastelun alla. **Yksikköhinta on alle kolmasosa kokonaiskustannuksista.** Teknologiansiirto ja lentotuntikustannus ratkaisevat kolmen vuosikymmenen budjetin. |
| 🏢 **Yritys** | Toimittaja, ERP, ulkoistus, laajentuminen | Komitea, joka ei ole yksimielinen itsensä kanssa. **SAPEVO-M** rakennettiin juuri tähän: se yhdistää **useiden päätöksentekijöiden** järjestysasteikolliset arviot vaatimatta ennakkokonsensusta. |
| 🚀 **Startupit** | Projektisalkku, pääoman kohdentaminen | Odotusarvon perusteella päättävä valitsee aina riskialtteimman vedon — **odotusarvo sivuuttaa hännän**. Täällä riski on **kriteeri**, ei alaviite dian 14 laidassa. |
| 💻 **IT** | Laitekannan standardointi | Päätös kertautuu 200:lla ja kestää 4 vuotta. Akunkesto ja on-site-takuu ovat kokonaiskustannuksissa arvokkaampia kuin kaksi pistettä synteettisessä vertailuluvussa. |

</div>

### Valmiit ajettavat tapaukset

```bash
python3 pipeline.py --listar
```

| Tapaus | Toimiala | Vaihtoehdot | Kriteerit |
|---|---|---|---|
| `smartphone` | kuluttaja | 6 | 8 |
| `veiculo_eletrico` | autoala | 7 | 8 |
| `caca_multifuncao` | puolustus | 6 | 9 |
| `blindado` | puolustus | 5 | 8 |
| `portfolio_startup` | yritys | 7 | 9 |
| `estacao_trabalho` | IT | 6 | 8 |

> [!NOTE]
> Tapausten matriisit ovat **havainnollistavia** — julkisia ja uskottavia suuruusluokkia menetelmän esittelyyn. **Ei-havainnollistavaa** on **mallinnus**: kriteerit, suunnat, DEMATELin kausaalimatriisi ja Saatyn matriisi. Siinä on arvo. **Korvaa luvut omalla tarjouksellasi, omalla tarjouspyynnölläsi tai omalla laboratoriotestilläsi** — moottori on sama; data on sinun.

---

## ⚡ Asennus

### Nopein reitti (Python)

```bash
git clone <url> multicriteriadecisionmodels
cd multicriteriadecisionmodels/public/foundations/pipeline
pip install -r requirements.txt
python3 pipeline.py
```

Valmis. Kaikki kuusi tapausta ajetaan, täydellisen raportin kera.

<details>
<summary><b>Yksityiskohtaiset esivaatimukset</b></summary>

| Komponentti | Vähimmäisversio | Pakollinen? | Mihin |
|---|---|---|---|
| Python | 3.10 | ✅ | referenssimoottori |
| NumPy | 2.0 | ✅ | kaikkien menetelmien algebra |
| numba | 0.60 | ⚠️ | ytimien JIT — ilman sitä sama tulos, vain hitaammin |
| SciPy | 1.10 | ✅ | aputilastot |
| matplotlib | 3.7 | ✅ | 5 näkymää tapausta kohden |
| Rust / cargo | 1.75 | ⭕ | ristiintarkistusmoottori |
| Node.js | 18 | ⭕ | Evidence-koontinäyttö |
| screen | — | ⭕ | taustasuoritus |

</details>

### Täysi putki

```bash
./run_all.sh                    # testit → putki → näkymät → i18n → Rust → täsmäytys
./run_all.sh --rapido           # ohittaa Rustin ja i18n:n
./run_all.sh --caso smartphone  # yksi tapaus
./run_all.sh --background       # ajaa screenissä (liity uudelleen: screen -r mcdm)
```

### Rust-moottori — binääri ilman ajoympäristöä

```bash
cd public/foundations/rust/mcdm_core
cargo test --release
cargo build --release

./target/release/mcdm --exemplo > problema.mcdm
./target/release/mcdm problema.mcdm
./target/release/mcdm problema.mcdm --json
```

### Koontinäyttö

```bash
cd public/foundations/evidence
npm install
npm run dev               # http://localhost:3000
```

<details>
<summary><b>Edistyneet komennot</b></summary>

```bash
python3 pipeline.py caca_multifuncao --workers 8 --iter 5000
python3 testes_nucleo.py
python3 exportar_rust.py
python3 gerar_i18n.py --tudo
python3 gerar_i18n.py --verificar
python3 gerar_graficos.py --workers 6
```

| Muuttuja | Oletus | Vaikutus |
|---|---|---|
| `MCDM_WORKERS` | auto | `ProcessPoolExecutor`-prosessit |
| `MCDM_NUMBA` | `1` | JIT päällä; `0` virheenjäljitykseen puhtaalla NumPyllä |
| `MCDM_SEED` | `42` | toistettavuus |
| `ROBUSTEZ_ITER` | `2000` | preferenssiuniversumit |
| `ROBUSTEZ_KAPPA` | `200` | Dirichlet-keskittymä (suurempi = painot lähempänä alkuperäisiä) |
| `MAUT_AVERSAO` | `2.0` | riskinkarttaminen (r > 0 = konkaavi) |
| `PROMETHEE_TIPO` | `linear` | preferenssifunktio (6 saatavilla) |

</details>

---

## ⚖️ Yhdeksän päätöksenteon koulukuntaa — ja miksi yhdeksän

> [!IMPORTANT]
> **Jokainen menetelmä on eri teoria siitä, mitä ”parempi” tarkoittaa.** Vain yhden käyttäminen on vastauksen valitsemista yhdessä kysymyksen kanssa. Ajamme kaikki yhdeksän, koska **riippumattomien teorioiden yksimielisyys** on vahvin todiste, jonka päätösongelma sallii.

<div align="center">

| Menetelmä | Koulukunta | Mitä olettaa | Milloin se on **oikea** työkalu | Alkuperä |
|---|---|---|---|---|
| **AHP-TOPSIS 2n** | etäisyys ideaaliin | täysi kompensaatio | määrälliset kriteerit, yksi päättäjä | Saaty (1980); Hwang & Yoon (1981) |
| **ELECTRE I** | ylivertaisuus | vertailukelvottomuus sallitaan | **karsinta**: poista dominoidut | Roy (1968) |
| **ELECTRE II** | ylivertaisuus | vahva ja heikko kynnys | täydellinen järjestys **veto-oikeudella** | Roy & Bertier (1971) |
| **PROMETHEE II** | ylivertaisuus | asteittainen preferenssi (6 funktiota) | kun ”hieman parempi” ≠ ”parempi” | Brans & Vincke (1985) |
| **MAUT** | hyöty | additiivinen riippumattomuus + riskinkarttaminen | päätös epävarmuuden vallitessa | Keeney & Raiffa (1976) |
| **MCDA-C** | konstruktivistinen | ankkuroidut Neutraali/Hyvä-tasot | **absoluuttinen diagnoosi**, ei pelkkä järjestys | Ensslin, Montibeller & Noronha (2001) |
| **VIKOR** | kompromissi | ryhmän hyöty × suurin kaduttavuus | kun **kompensaatio on kelvoton** | Opricovic (1979); Opricovic & Tzeng (2002-07) |
| **TODIM** | prospektiteoria | tappio sattuu enemmän kuin vastaava voitto ilahduttaa | tappiota karttava päättäjä — **niitä ovat kaikki** | Gomes & Lima (1992); Kahneman & Tversky (1979) |
| **SAPEVO-M** | järjestysasteikollinen, monta päättäjää | useiden päättäjien järjestysasteikollinen arvio | **komitea, joka ei ole yksimielinen** | Gomes et al. (1997); Teixeira, Santos & Gomes (2019) |

</div>

<details>
<summary><b>Miksi nämä kolme ansaitsevat erityishuomion</b></summary>

### VIKOR — kun kompensaatio on kelvoton
VIKOR laskee **kaksi** mittaa: `S` (ryhmän hyöty — painotettu summa, joka **hyväksyy** että surkea suoritus kuittautuu useilla hyvillä) ja `R` (suurin yksilöllinen kaduttavuus — minimax, joka kompensaation **hylkää**).

Panssariajoneuvolla, jolla on erinomainen liikkuvuus ja surkea suoja, on optimaalinen `S` ja kammottava `R`. Painotettu summa valitsisi sen; VIKOR nostaa lipun. Ja kun `S` ja `R` ovat eri mieltä, ehdot **C1** (hyväksyttävä etu) ja **C2** (hyväksyttävä vakaus) raportoivat nimenomaisesti, että päätöksessä on katvealue.

### TODIM — tappio sattuu enemmän kuin voitto
Perustuu Kahnemanin ja Tverskyn **prospektiteoriaan**: 10 pisteen menetys toimintamatkassa sattuu enemmän kuin 10 pisteen saaminen ilahduttaa. Klassinen painotettu summa sivuuttaa tämän epäsymmetrian ja kohtelee voittoa ja tappiota symmetrisinä — **mitä yksikään inhimillinen päättäjä ei tee.** Kerroin `θ` kalibroi voimakkuuden: `θ < 1` vahvistaa tappion karttamista.

### SAPEVO-M — komitea, joka ei ole yksimielinen
Kaikki muut menetelmät vaativat painovektorin. **Mistä se tulee, kun viisi päättäjää on eri mieltä?** SAPEVO-M ratkaisee tämän lähteellä: kukin päättäjä ilmaisee **järjestysasteikollisen** preferenssin (”toimintamatka on paljon tärkeämpi kuin hinta”, seitsemänportaisella asteikolla), ja menetelmä yhdistää ne **vaatimatta ennakkoon sovittua konsensusjärjestystä**. Näin komitea todella puhuu — kukaan ei sano ”toimintamatka on arvoltaan 0,237”.

</details>

### Konsensusmoottori

```
DEMATEL ──► painot vaikutuksen mukaan ──► 9 menetelmää ──► Bordan konsensus ──► voittaja
                                                    │
                        2 000 Dirichlet-universumia ─────────────────┘
                                    ▼
                     tuomio: ROBUSTO / PROVÁVEL / FRÁGIL
```

| Tuomio | Luottamus | Mitä tehdä |
|---|---|---|
| 🟢 **ROBUSTI** | ≥ 90% | Valinta ei riipu hienosäädöstä. **Sen voi viedä komitealle.** |
| 🟡 **TODENNÄKÖINEN** | 60–90% | Se pitää useimmissa skenaarioissa, mutta kakkonen on kilpailukykyinen. **Vertaa molempia.** |
| 🔴 **HAURAS** | < 60% | Ensimmäinen sija on **painojen artefakti**. Älä päätä pelkän järjestyksen perusteella: palaa päättäjän luo ja kalibroi uudelleen. |

---

## 🔬 Kaksi riippumatonta moottoria: ristiintarkistus

> [!TIP]
> **Miksi toteuttaa kaikki uudelleen Rustilla?** Koska ”koodi toimii” ei ole todiste siitä, että **matematiikka** on oikein.

Kaavan kirjausvirhe toistuu harvoin **täsmälleen samanlaisena** kahdella kielellä, joiden lineaarialgebra on riippumaton. Python-moottori käyttää NumPy/LAPACKia; Rust-moottori toteuttaa Gaussin eliminoinnin osittaisella tukiluvun valinnalla ja potenssimenetelmän **käsin, ilman ainuttakaan ulkoista riippuvuutta**.

```bash
python3 exportar_rust.py
```
```
✅ smartphone           8 menetelmää identtisiä · voittaja=C     (Δ ≤ 4.7e-11)
✅ veiculo_eletrico     8 menetelmää identtisiä · voittaja=EV6   (Δ ≤ 4.1e-11)
✅ caca_multifuncao     8 menetelmää identtisiä · voittaja=C3    (Δ ≤ 4.5e-11)
✅ blindado             8 menetelmää identtisiä · voittaja=B3    (Δ ≤ 4.6e-11)
✅ portfolio_startup    8 menetelmää identtisiä · voittaja=P3    (Δ ≤ 4.9e-11)
✅ estacao_trabalho     8 menetelmää identtisiä · voittaja=W5    (Δ ≤ 5.0e-11)
```

**Bonus: Rust-binääri ei tarvitse Pythonia, NumPyta, numbaa eikä virtuaaliympäristöä. Muutama megatavu, joka toimii palvelimella, kontissa tai sulautetussa laitteessa — millä on väliä, kun moottori lähtee järjestelmän mukana kentälle.**

---

## 🚀 Suorituskyky: 26× nopeampi, sama vastaus

Robustiusanalyysi ajaa 2 000 universumia × 9 menetelmää. Naiivi toteutus vei **42 sekuntia** tapausta kohden.

<div align="center">

| Vaihe | Aika | Nopeutus |
|---|---|---|
| JIT-ytimet universumia kohden | 42,33 s | — |
| **Esikäännös tensoreiksi** | 2,41 s | **17,6×** |
| `ranks` JITin alla + tila prosessia kohden | **1,63 s** | **26,0×** |

</div>

> **Eniten tuottanut optimointi ei ollut rinnakkaisuus eikä JIT.** Se oli oivallus, että neljä yhdeksästä menetelmästä on **lineaarisia painovektorin suhteen** — mikä sallii tensorien esilaskennan ja kunkin universumin typistämisen yhdeksi matriisi-vektori-tuloksi. **Algebra ennen infrastruktuuria.**

Ja tulos on **bitilleen identtinen** hitaan reitin kanssa — 100 universumia × 9 menetelmää tarkistetaan jokaisella testisarjan ajolla. Optimointi, joka muuttaa tulosta, on vika eikä hyöty.

<details>
<summary><b>Projektin suorituskäytäntö</b></summary>

| Sääntö | Soveltaminen |
|---|---|
| **Rinnakkaisuus** | `ProcessPoolExecutor` prosessoriin sidottuun työhön; ei koskaan säikeitä (GIL sarjallistaa) |
| **Kynnys** | Sarjallinen vai rinnakkainen ratkaistaan **työmäärän** (`n_iter · m² · k`) perusteella, ei alkioiden lukumäärän — pienen ongelman rinnakkaistaminen on **hitaampaa** kuin sen ratkaiseminen |
| **JIT** | `numba` ja `cache=True` O(m²k)-ytimissä; puuttuessaan putoaa puhtaaseen NumPyhyn |
| **Taustasuoritus** | `screen`, ei koskaan `nohup` — mahdollistaa uudelleenliittymisen ja vuorovaikutuksen |
| **Toistettavuus** | Kiinteä, prosessimäärästä riippumaton osiointi: sama siemen → identtinen tulos yhdellä tai 32 prosessilla |

</details>

---

## 🌐 12 kieltä — SDL Trados -käännösmuisti

Tämä ei ole READMEn konekääntämistä. Tämä on **lokalisointiputki**, jossa on käännösmuisti **SDL Trados Studio** -standardin mukaisesti.

```
translation.memory.md          ← kanoninen lähde, versioitu gitissä
   │  --tm
   ▼
strings.<locale>.json          ← kulutettu artefakti
   │  --paginas
   ▼
12 koontinäytön sivua + 12 README-tiedostoa
   │  --tmx
   ▼
translation.memory.tmx         ← tuotavissa SDL Trados Studioon
```

| Kohde | Luvut |
|---|---|
| Kielialueet | **12** (pt-BR · en · es · fr · de · zh · ko · hi · **he RTL** · ru · sv · fi) |
| Käännösyksiköt | 56 |
| Sanastotermit (MultiTerm) | 22 |
| Segmenttejä TMX:ssä | **948** |
| Merkistökoodaus | UTF-8 · LF · NFC |

```bash
python3 gerar_i18n.py --verificar
```

Laadunvarmistus jäljittelee Tradosin **Verify**-toimintoa: termistön johdonmukaisuus, säilyneet placeable-elementit, segmenttien kattavuus, tiukka merkistökoodaus ja koskemattomat ei-käännettävät — säännöllä, joka eroaa kirjoitusjärjestelmän mukaan (tekniset lyhenteet pysyvät latinalaisina kaikilla kielillä; erisnimet **translitteroidaan** siellä, missä kirjoitus ei ole latinalaista).

---

## 📁 Mitä sisältä löytyy

```
multicriteriadecisionmodels/
├── README.md (+11)                     näyteikkuna 12 kielellä
├── docs/                               logo ja READMEjen näkymät
│
└── public/foundations/
    ├── pipeline/                       PYTHON-MOOTTORI (referenssi)
    │   ├── nucleo.py                   DEMATEL · ELECTRE I/II · PROMETHEE II
    │   │                               MAUT · MCDA-C · AHP · TOPSIS 2N
    │   ├── metodos_br.py               SAPEVO-M · VIKOR · TODIM · Copeland
    │   ├── robustez.py                 Dirichlet + ProcessPoolExecutor
    │   ├── pipeline.py                 orkestroija
    │   ├── gerar_graficos.py           5 näkymää tapausta kohden
    │   ├── gerar_i18n.py               TM → merkkijonot → sivut → TMX
    │   ├── testes_nucleo.py            16 matemaattista tarkistusta
    │   ├── exportar_rust.py            moottoreiden välinen täsmäytys
    │   ├── casos/catalogo.py           6 tapausta + validointi
    │   └── run_all.sh                  putki (screen)
    │
    ├── rust/mcdm_core/                 RUST-MOOTTORI (varmennus + jakelu)
    │   └── src/lib.rs                  kaikki menetelmät, nolla riippuvuutta
    │
    └── evidence/                       KOONTINÄYTTÖ (Evidence.dev)
        ├── sources/mcdm/               11 SQL-kyselyä
        └── pages/                      12 kielireittiä
```

---

## 🧠 Perusta

Projekti nojaa vertaisarvioituun kirjallisuuteen, ei intuitioon. Integraatioarkkitehtuuri seuraa lähdettä **John (2025)**, *”Integration of DEMATEL with Other MCDM Methods for Comprehensive Techno-Economic Analysis”*: DEMATEL paljastaa kausaalirakenteen ja johtaa **vaikutukseen perustuvat painot**, jotka syöttävät järjestämismenetelmiä — mielivaltaisesti asetettujen painojen sijaan.

**Brasilialaisen monikriteerisen päätöstuen koulukunnan** menetelmät (SAPEVO-M, TODIM-FSE, ELECTRE II, VIKOR, järjestysasteikolliset menetelmät) seuraavat laitosten **IME**, **UFF**, **CASNAV**, **AMAN** ja **FURB** töitä — mukaan lukien todelliset sovellukset **droonien arviointiin merisodankäynnissä**, **prikaatin logistiikkatukikohdan luokitteluun** ja **korvettien järjestämiseen Brasilian laivastolle**.

> [!NOTE]
> **Menetelmien tekijyys kuuluu kokonaan niiden luojille,** jotka on mainittu erikseen tiedostojen `nucleo.py` ja `metodos_br.py` otsikoissa. Projektin panos on toteutus, integraatio ja konsensusmoottori — **eivät menetelmät**.

---

## ❓ Kysymykset, jotka tulet esittämään

<details>
<summary><b>Käytän jo painotettua päätösmatriisia. Eikö tämä ole sama asia?</b></summary>

Ei, kolmesta syystä. **(1)** Painotettu matriisi on **yksi** menetelmä (painotettu summa), jossa on sisäänrakennettu teoria: täysi kompensaatio. Se olettaa, että surkea suoritus yhdessä kriteerissä voidaan kuitata muualla — mikä ei päde turvallisuudessa, panssarisuojassa eikä sääntelynmukaisuudessa. **(2)** Se olettaa kriteerit riippumattomiksi, ja lähes aina lasket yhteen jo yhteen laskettua. **(3)** Se palauttaa luvun ilman luottamusväliä, eikä siksi kestä komitean ensimmäistä kysymystä.
</details>

<details>
<summary><b>Miten valitsen painot?</b></summary>

Et valitse niitä — **kolme reittiä johtaa ne**. **DEMATEL** poimii ne ilmoittamastasi kausaalirakenteesta (kuka vaikuttaa keneen). **AHP** poimii ne pareittaisista vertailuista, ja johdonmukaisuustarkistus **hylkää** ristiriitaisen arvion. **SAPEVO-M** poimii ne useiden päättäjien järjestysasteikollisista arvioista. Ja sen jälkeen robustiusanalyysi kysyy, kuinka paljon tulos yhä **riippuu** niistä.
</details>

<details>
<summary><b>Entä jos ongelmassani on 200 vaihtoehtoa?</b></summary>

Se toimii. Rinnakkaisuuskynnys tunnistaa mittakaavan ja jakaa työn prosesseille. Mitattu: 60 vaihtoehtoa × 12 kriteeriä × 2 000 universumia 3,8 sekunnissa neljällä prosessilla. Noin 700 vaihtoehdon jälkeen preferenssitensori ylittää määritetyn muistirajan, ja moottori varoittaa sen sijaan että jumittuisi.
</details>

<details>
<summary><b>Menetelmät olivat eri mieltä. Mitä nyt?</b></summary>

**Se on tuote, ei ongelma.** Ero kertoo, että päätöksesi on herkkä valitulle koulukunnalle — ja nimeää minkä. Jos ELECTRE pudottaa sen, jonka kaikki muut valitsevat, on olemassa kriteeri, jolla kyseinen vaihtoehto on riittävän huono vetoon. Vie komitealle **se**, älä järjestystä.
</details>

<details>
<summary><b>Voinko käyttää omia tietojani?</b></summary>

Juuri sitä varten tämä on. Tapaus on deklaratiivinen rakenne tiedostossa `casos/catalogo.py`: kriteerit (suunnan ja yksikön kera), vaihtoehdot, päätösmatriisi, DEMATELin kausaalimatriisi ja Saatyn matriisi. Validoija hylkää virheellisen tapauksen **ennen** mitään laskentaa — epäjohdonmukaiset ulottuvuudet, väärä lävistäjä, ei-resiprookkinen Saatyn matriisi, vakio kriteeri joka ei erottele mitään.
</details>

---

## 📜 Lisenssi ja tekijyys

<div align="center">

<img src="docs/logo_capa.png" alt="ProfBru" width="180"/>

**ProfBru © 2026**

**MCDM Studio — Monikriteeriset päätösmallit**
Tekijä: **ProfBru - Bruno Penedo** © 2026 — **KAIKKI OIKEUDET PIDÄTETÄÄN**
📧 profbruanbima@gmail.com

</div>

**Omisteinen** projekti. Tämä tietovarasto ei myönnä lisenssiä käyttöön, kopiointiin, muokkaamiseen, levittämiseen tai johdannaisteosten luomiseen. Kaupallinen, akateeminen tai institutionaalinen käyttö edellyttää tekijän kirjallista lupaa.

**Kolmansien osapuolten attribuutio:** monikriteerimenetelmät ovat tekijöidensä työtä — Saaty, Roy, Bertier, Brans, Vincke, Keeney, Raiffa, Ensslin, Montibeller, Noronha, Gabus, Fontela, Opricovic, Tzeng, Hwang, Yoon, Kahneman, Tversky, Borda, Copeland, Gomes, Lima, Santos, Teixeira, Moreira, Rangel, Neves, Hein, Kroenke, Keunecke ja Gomes Júnior — jotka on mainittu erikseen lähdekoodissa.
