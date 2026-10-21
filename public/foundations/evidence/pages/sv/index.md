---
title: MCDM Studio — Decisão MultiKriterium
---

<div style="text-align:center;">

🌐 [Português](/) · [English](/en) · [Español](/es) · [Français](/fr) · [Deutsch](/de) · [中文](/zh) · [한국어](/ko) · [हिन्दी](/hi) · [עברית](/he) · [Русский](/ru) · **Svenska** · [Suomi](/fi)

<div style="text-align:center;margin:1.2rem 0 1.6rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="200" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.5rem;font-size:1.05rem;">ProfBru © 2026</div>
</div>

_MCDM Studio — Modelos MultiKriterium de Decisão · Autor: **ProfBru - Bruno Penedo** © 2026 — ALLA RÄTITGHETER FÖRBEHÅLLNA · profbruanbima@gmail.com_

</div>

<!--
  ÍNDICE LEVE, DE PROPÓSITO.
  Só consultas AGREGADAS (uma linha por caso). As tabelas detalhadas — ranking por
  método (3.744 linhas), Beslutsmatris (3.514), distribuição (4.230), Robusthet por
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

# 🎯 Multikriteriellt beslut — tio skolor, ett utlåtande med konfidensintervall

> **Kalkylbladet räknar inte fel. Det ställer fel fråga.** Sortera på pris utser det billigaste. Sortera på expertbetyg utser det dyraste. Filtrera på "uppfyller alla krav" tömmer oftast listan. Ingen av de tre svarar på frågan som ställdes: *bland alternativ som motsäger varandra, vilket ska man välja — och med vilken tillförlitlighet?*

Den här panelen kör **tio multikriteriella metoder** på varje fall, härleder vinnaren ur **Borda-konsensus** mellan dem och **stör sedan vikterna 2 000 gånger** för att besvara den enda fråga kommittén egentligen ställer: *vad om vi hade satt en något annan vikt?*

<BigValue data={totais} value=casos title="Beslutsfall" fmt=num0/>
<BigValue data={totais} value=alternativas title="Bedömda alternativ" fmt=num0/>
<BigValue data={totais} value=robustos title="ROBUSTA utlåtanden" fmt=num0/>
<BigValue data={totais} value=frageis title="BRÄCKLIGA utlåtanden" fmt=num0/>

## 📋 Beslutsfall

> Klicka på vilket fall som helst för att öppna den **fullständiga rapporten**: DEMATEL:s orsak-verkan-diagram, kartan över de tio skolorna, ELECTRE:s kärna, TOPSIS dubbla normalisering, Borda-konsensus, robusthet över 2 000 universum, BCG-matris och beslutsmatrisen.

<DataTable data={casos} rows=all rowShading=true link=link>
  <Column id=nome title="Fall"/>
  <Column id=dominio title="Domän"/>
  <Column id=n_alternativas title="Alternativ" fmt=num0/>
  <Column id=vencedor_rotulo title="🏆 Vinnare"/>
  <Column id=prob_vitoria title="Konfidens (%)" fmt=num1 contentType=colorscale/>
  <Column id=classificacao title="Utlåtande"/>
</DataTable>

> **Så läser du Utlåtandet.** `ROBUST` (≥ 90 %) = valet beror inte på finkalibrering av vikterna; det kan gå till kommittén. `SANNOLIK` (60–90 %) = det håller i de flesta scenarier, men tvåan är konkurrenskraftig. `BRÄCKLIG` (under 60 %) = **förstaplatsen är en artefakt av vikterna** — systemet säger det i stället för att visa en trofé.

<BarChart data={resumo_dominio} x=dominio y=casos title="Fall per tillämpningsområde" yAxisTitle="Casos"/>

## 🧮 DEMATEL — grundorsaken till varje beslut

> Frågan som nästan ingen ställer innan vikter sätts: **är kriterierna oberoende?** De är nästan aldrig det. Energiförbrukning *orsakar* räckvidd; bepansring *orsakar* vikt, som *orsakar* förlorad rörlighet. Att addera båda som oberoende räknar samma sak två gånger.
>
> **DEMATEL** (Gabus & Fontela, Battelle) bygger totalrelationsmatrisen `T = X(I−X)⁻¹` — som summerar direkta **och indirekta** influenser av vilken väglängd som helst — och separerar: `R+C` = betydelse i systemet; `R−C > 0` = **ORSAK** (spak: agera här) och `R−C < 0` = **VERKAN** (termometer: resultatet av det som redan gjorts).
>
> Kolumnen **Grundorsak** nedan är kriteriet med högst `R−C` i varje fall: där flyttar en insats hela systemet.

<DataTable data={alavancas} rows=all rowShading=true>
  <Column id=nome title="Fall"/>
  <Column id=n_criterios title="Kriterier" fmt=num0/>
  <Column id=n_causas title="Orsaker" fmt=num0 contentType=colorscale/>
  <Column id=causa_raiz title="🔧 Grundorsak (högsta R−C)"/>
  <Column id=criterio_maior_peso title="Kriteriet med högst vikt"/>
  <Column id=maior_peso_pct title="Vikt (%)" fmt=num1/>
</DataTable>

<BarChart data={alavancas} x=nome y={['n_causas','n_criterios']} type=grouped title="Kriterier som är ORSAK i varje fall (spakar mot totalen)" yAxisTitle="Critérios" swapXY=true/>

> **Öppna ett fall** för att se hela orsak-verkan-diagrammet, tabellen med `R` och `C` separerade och **totalrelationsmatrisen** med kopplingarna en för en.

## 🎲 BCG-matris — karta över möjligheter per kategori

> Utöver *vilken man ska välja* har varje kategori en **möjlighetsprofil**: hur många alternativ som är ⭐ Stjärna (investera), 🐄 Kassako (skörda), ❓ Frågetecken (väga vinsten) och 🐕 Hund (lägga ned). En kategori med bara frågetecken är en dyr marknad; en full av kassakor är en mogen marknad, där pengar avgör lite.

<DataTable data={bcg_geral} rows=all rowShading=true>
  <Column id=nome title="Kategori"/>
  <Column id=estrelas title="⭐" fmt=num0 contentType=colorscale/>
  <Column id=vacas title="🐄" fmt=num0 contentType=colorscale/>
  <Column id=interrogacoes title="❓" fmt=num0 contentType=colorscale/>
  <Column id=abacaxis title="🐕" fmt=num0 contentType=colorscale/>
  <Column id=total title="Totalt" fmt=num0/>
  <Column id=quadrante_do_vencedor title="Kvadrant för förstaplatsen"/>
</DataTable>

## ⚖️ De tio beslutsskolorna

> Varje metod är en **egen teori om vad "bäst" betyder**, och därför kör vi alla: när tio oberoende skolor utser samma vinnare är valet ingen artefakt av en metod. När de skiljer sig åt pekar avvikelsen ut var den verkliga avvägningen ligger.

| Método | Escola | O que assume | Quando é a ferramenta certa |
|---|---|---|---|
| **AHP-TOPSIS 2n** | Distância à solução ideal | Compensação total entre Kriteriums | Kriterier quantitativos, decisor único |
| **ELECTRE I** | Överklassificering | Incomparabilidade é permitida | Triagem: eliminar o que é dominado |
| **ELECTRE II** | Överklassificering | Limiares forte e fraco | Ordenação completa com veto |
| **PROMETHEE II** | Överklassificering | Preferência gradual (6 funções) | Quando "um pouco melhor" não é "melhor" |
| **MAUT** | Utilidade | Independência aditiva + Riskaversion | Decisão sob incerteza |
| **MCDA-C** | Construtivista | Níveis Neutro/Bom ancorados | Diagnóstico absoluto, não só ranking |
| **VIKOR** | Compromisso | Utilidade do grupo × arrependimento máximo | Quando compensar é inaceitável |
| **TODIM** | Teoria dos Prospectos | Perda dói mais que ganho equivalente | Decisor avesso a perda (todos são) |
| **SAPEVO-M** | Ordinal multidecisor | Julgamento ordinal de vários decisores | Comitê que não concorda entre si |

## 🎯 Robusthet — konfidensintervall för själva beslutet

> **Problemet.** Varje MCDM-metod ger en vinnare med implicit tillförlitlighet på 100 %. Men vikter är aldrig exakta — de är preferensskattningar. Om två procentenheter i ett kriteriums vikt byter plats ett och två är "vinnaren" en artefakt av kalibreringen, inte ett faktum om mängden. Ingen rapporterar det. **Det är där besluten dör i kommittén.**
>
> **Lösningen.** Vi stör vikterna med `w' ~ Dirichlet(κ·w)` och rangordnar om 2 000 gånger. Dirichlet är det naturliga valet: dess stöd är exakt simplexet (positiva vikter som summerar till 1) och den uppfyller `E[w'] = w` — vi stör **utan att snedvrida**. Med κ = 200 svänger en vikt på 13 % ±2,4 p.e.
>
> Utlåtandet är inte längre *"Modell C är bäst"* utan **"Modell C vinner i 96 % av de rimliga preferensuniversumen"**.

**Öppna ett fall ur tabellen ovan** för att se orsak-verkan-diagrammet, kartan över de tio skolorna, BCG-matrisen och den fullständiga fördelningen av placeringar över de 2 000 universumen.

---

<div style="text-align:center;margin-top:2rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="120" style="display:inline-block;opacity:0.9;"/>
  <div style="font-weight:700;margin-top:0.4rem;">ProfBru © 2026</div>
  <div style="margin-top:0.5rem;font-style:italic;font-size:0.9rem;color:#64748b;">
    MCDM Studio — Modelos MultiKriterium de Decisão<br/>
    Autor: <strong>ProfBru - Bruno Penedo</strong> © 2026 — ALLA RÄTITGHETER FÖRBEHÅLLNA<br/>
    profbruanbima@gmail.com
  </div>
</div>
