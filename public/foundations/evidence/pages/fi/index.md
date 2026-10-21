---
title: MCDM Studio — Decisão MultiKriteeri
---

<div style="text-align:center;">

🌐 [Português](/) · [English](/en/) · [Español](/es/) · [Français](/fr/) · [Deutsch](/de/) · [中文](/zh/) · [한국어](/ko/) · [हिन्दी](/hi/) · [עברית](/he/) · [Русский](/ru/) · [Svenska](/sv/) · **Suomi**

<div style="text-align:center;margin:1.2rem 0 1.6rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="200" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.5rem;font-size:1.05rem;">ProfBru © 2026</div>
</div>

_MCDM Studio — Modelos MultiKriteeri de Decisão · Autor: **ProfBru - Bruno Penedo** © 2026 — KAIKKI OIKEUDET PIDÄTETÄÄN · profbruanbima@gmail.com_

</div>

<!--
  ÍNDICE LEVE, DE PROPÓSITO.
  Só consultas AGREGADAS (uma linha por caso). As tabelas detalhadas — ranking por
  método (3.744 linhas), Päätösmatriisi (3.514), distribuição (4.230), Robustius por
  método (4.160) — vivem nas páginas de caso, onde estão filtradas por `id_caso`.
  Carregá-las todas aqui somava ~16 mil linhas e travava o navegador.
-->

```sql casos
select *, '/fi/casos/' || id_caso as link from mcdm.casos
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

# 🎯 Monikriteerinen päätös — kymmenen koulukuntaa, yksi tuomio luottamusvälillä

> **Taulukkolaskenta ei laske väärin. Se kysyy väärin.** Hinnan mukaan järjestäminen valitsee halvimman. Asiantuntija-arvion mukaan järjestäminen valitsee kalleimman. Suodatus "täyttää kaikki vaatimukset" tyhjentää listan yleensä. Mikään näistä kolmesta ei vastaa esitettyyn kysymykseen: *keskenään ristiriitaisista vaihtoehdoista, mikä valita — ja millä varmuudella?*

Tämä näkymä ajaa **kymmenen monikriteerimenetelmää** jokaiseen tapaukseen, johtaa voittajan niiden **Borda-konsensuksesta** ja **häiritsee sitten painoja 2 000 kertaa** vastatakseen siihen ainoaan kysymykseen, jonka toimikunta todella esittää: *entä jos olisimme antaneet hieman eri painon?*

<BigValue data={totais} value=casos title="Päätöstapaukset" fmt=num0/>
<BigValue data={totais} value=alternativas title="Arvioidut vaihtoehdot" fmt=num0/>
<BigValue data={totais} value=robustos title="ROBUSTIT tuomiot" fmt=num0/>
<BigValue data={totais} value=frageis title="HAURAAT tuomiot" fmt=num0/>

## 📋 Päätöstapaukset

> Napsauta mitä tahansa tapausta avatakseen **täyden raportin**: DEMATELin syy-vaikutuskaavio, kymmenen koulukunnan kartta, ELECTREn ydin, TOPSISin kaksoisnormalisointi, Borda-konsensus, robustius 2 000 universumissa, BCG-matriisi ja päätösmatriisi.

<DataTable data={casos} rows=all rowShading=true link=link>
  <Column id=nome title="Tapaus"/>
  <Column id=dominio title="Toimiala"/>
  <Column id=n_alternativas title="Vaihtoehdot" fmt=num0/>
  <Column id=vencedor_rotulo title="🏆 Voittaja"/>
  <Column id=prob_vitoria title="Luottamus (%)" fmt=num1 contentType=colorscale/>
  <Column id=classificacao title="Tuomio"/>
</DataTable>

> **Näin luet Tuomion.** `ROBUSIT` (≥ 90 %) = valinta ei riipu painojen hienosäädöstä; se voi mennä toimikuntaan. `TODENNÄKÖINEN` (60–90 %) = se pitää useimmissa skenaarioissa, mutta kakkonen on kilpailukykyinen. `HAURAS` (alle 60 %) = **ykköstila on painojen artefakti** — järjestelmä sanoo sen sen sijaan että näyttäisi palkintoa.

<BarChart data={resumo_dominio} x=dominio y=casos title="Tapaukset sovellusalueen mukaan" yAxisTitle="Casos"/>

## 🧮 DEMATEL — jokaisen päätöksen perussyy

> Kysymys, jota lähes kukaan ei esitä ennen painojen antamista: **ovatko kriteerit riippumattomia?** Lähes koskaan eivät ole. Energiankulutus *aiheuttaa* toimintamatkan; panssarointi *aiheuttaa* painon, joka *aiheuttaa* liikkuvuuden menetyksen. Näiden laskeminen yhteen riippumattomina laskee saman asian kaksi kertaa.
>
> **DEMATEL** (Gabus & Fontela, Battelle) rakentaa kokonaisrelaatiomatriisin `T = X(I−X)⁻¹` — joka summaa suorat **ja epäsuorat** vaikutukset mistä tahansa polun pituudesta — ja erottelee: `R+C` = tärkeys järjestelmässä; `R−C > 0` = **SYY** (vipu: toimi tässä) ja `R−C < 0` = **VAIKUTUS** (lämpömittari: jo tehdyn tulos).
>
> Alla oleva **Perussyy**-sarake on kunkin tapauksen suurimman `R−C`:n kriteeri: siinä yksi toimenpide liikuttaa koko järjestelmää.

<DataTable data={alavancas} rows=all rowShading=true>
  <Column id=nome title="Tapaus"/>
  <Column id=n_criterios title="Kriteerit" fmt=num0/>
  <Column id=n_causas title="Syyt" fmt=num0 contentType=colorscale/>
  <Column id=causa_raiz title="🔧 Perussyy (suurin R−C)"/>
  <Column id=criterio_maior_peso title="Suurimman painon kriteeri"/>
  <Column id=maior_peso_pct title="Paino (%)" fmt=num1/>
</DataTable>

<BarChart data={alavancas} x=nome y={['n_causas','n_criterios']} type=grouped title="Kriteerit, jotka ovat SYY kussakin tapauksessa (vivut suhteessa kokonaismäärään)" yAxisTitle="Critérios" swapXY=true/>

> **Avaa tapaus** nähdäksesi täyden syy-vaikutuskaavion, taulukon erillisillä `R`:llä ja `C`:llä sekä **kokonaisrelaatiomatriisin** yhteyksineen yksitellen.

## 🎲 BCG-matriisi — mahdollisuuksien kartta luokittain

> Sen lisäksi, *minkä valita*, jokaisella luokalla on **mahdollisuusprofiili**: montako vaihtoehtoa on ⭐ Tähti (sijoita), 🐄 Lehmä (korjaa sato), ❓ Kysymysmerkki (punnitse palkinto) ja 🐕 Koira (luovu). Pelkistä kysymysmerkeistä koostuva luokka on kallis markkina; lehmiä täynnä oleva on kypsä markkina, jossa raha ratkaisee vähän.

<DataTable data={bcg_geral} rows=all rowShading=true>
  <Column id=nome title="Luokka"/>
  <Column id=estrelas title="⭐" fmt=num0 contentType=colorscale/>
  <Column id=vacas title="🐄" fmt=num0 contentType=colorscale/>
  <Column id=interrogacoes title="❓" fmt=num0 contentType=colorscale/>
  <Column id=abacaxis title="🐕" fmt=num0 contentType=colorscale/>
  <Column id=total title="Yhteensä" fmt=num0/>
  <Column id=quadrante_do_vencedor title="Ensimmäisen sijan neljännes"/>
</DataTable>

## ⚖️ Kymmenen päätöksenteon koulukuntaa

> Jokainen menetelmä on **eri teoria siitä, mitä "parempi" tarkoittaa**, ja siksi ajamme ne kaikki: kun kymmenen riippumatonta koulukuntaa valitsee saman voittajan, valinta ei ole yhden menetelmän artefakti. Kun ne eroavat, ero osoittaa, missä todellinen kompromissi on.

| Método | Escola | O que assume | Quando é a ferramenta certa |
|---|---|---|---|
| **AHP-TOPSIS 2n** | Distância à solução ideal | Compensação total entre Kriteeris | Kriteerit quantitativos, decisor único |
| **ELECTRE I** | Ylittääção | Incomparabilidade é permitida | Triagem: eliminar o que é dominado |
| **ELECTRE II** | Ylittääção | Limiares forte e fraco | Ordenação completa com veto |
| **PROMETHEE II** | Ylittääção | Preferência gradual (6 funções) | Quando "um pouco melhor" não é "melhor" |
| **MAUT** | Utilidade | Independência aditiva + Riskinkarttaminen | Decisão sob incerteza |
| **MCDA-C** | Construtivista | Níveis Neutro/Bom ancorados | Diagnóstico absoluto, não só ranking |
| **VIKOR** | Compromisso | Utilidade do grupo × arrependimento máximo | Quando compensar é inaceitável |
| **TODIM** | Teoria dos Prospectos | Perda dói mais que ganho equivalente | Decisor avesso a perda (todos são) |
| **SAPEVO-M** | Ordinal multidecisor | Julgamento ordinal de vários decisores | Comitê que não concorda entre si |

## 🎯 Robustius — itse päätöksen luottamusväli

> **Ongelma.** Jokainen MCDM-menetelmä palauttaa voittajan, jonka implisiittinen varmuus on 100 %. Mutta painot eivät ole koskaan tarkkoja — ne ovat preferenssiarvioita. Jos kaksi prosenttiyksikköä yhden kriteerin painossa vaihtaa ykkösen ja kakkosen, "voittaja" on kalibroinnin artefakti eikä joukkoa koskeva tosiasia. Kukaan ei raportoi tätä. **Siinä päätökset kuolevat toimikunnassa.**
>
> **Ratkaisu.** Häiritsemme painoja `w' ~ Dirichlet(κ·w)` ja järjestämme uudelleen 2 000 kertaa. Dirichlet on luonnollinen valinta: sen kantaja on täsmälleen simpleksi (positiiviset painot, summa 1) ja se toteuttaa `E[w'] = w` — häiritsemme **harhauttamatta**. Kun κ = 200, 13 %:n paino heilahtelee ±2,4 %-yks.
>
> Tuomio ei ole enää *"Malli C on paras"* vaan **"Malli C voittaa 96 %:ssa uskottavista preferenssiuniversumeista"**.

**Avaa tapaus yllä olevasta taulukosta** nähdäksesi syy-vaikutuskaavion, kymmenen koulukunnan kartan, BCG-matriisin ja sijoitusten täyden jakauman 2 000 universumissa.

---

<div style="text-align:center;margin-top:2rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="120" style="display:inline-block;opacity:0.9;"/>
  <div style="font-weight:700;margin-top:0.4rem;">ProfBru © 2026</div>
  <div style="margin-top:0.5rem;font-style:italic;font-size:0.9rem;color:#64748b;">
    MCDM Studio — Modelos MultiKriteeri de Decisão<br/>
    Autor: <strong>ProfBru - Bruno Penedo</strong> © 2026 — KAIKKI OIKEUDET PIDÄTETÄÄN<br/>
    profbruanbima@gmail.com
  </div>
</div>
