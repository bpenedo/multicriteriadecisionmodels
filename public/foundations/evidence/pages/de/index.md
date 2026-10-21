---
title: MCDM Studio — Decisão MultiKriterium
---

<div style="text-align:center;">

🌐 [Português](/) · [English](/en/) · [Español](/es/) · [Français](/fr/) · **Deutsch** · [中文](/zh/) · [한국어](/ko/) · [हिन्दी](/hi/) · [עברית](/he/) · [Русский](/ru/) · [Svenska](/sv/) · [Suomi](/fi/)

<div style="text-align:center;margin:1.2rem 0 1.6rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="200" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.5rem;font-size:1.05rem;">ProfBru © 2026</div>
</div>

_MCDM Studio — Modelos MultiKriterium de Decisão · Autor: **ProfBru - Bruno Penedo** © 2026 — ALLE RECHTE VORBEHALTEN · profbruanbima@gmail.com_

</div>

<!--
  ÍNDICE LEVE, DE PROPÓSITO.
  Só consultas AGREGADAS (uma linha por caso). As tabelas detalhadas — ranking por
  método (3.744 linhas), Entscheidungsmatrix (3.514), distribuição (4.230), Robustheit por
  método (4.160) — vivem nas páginas de caso, onde estão filtradas por `id_caso`.
  Carregá-las todas aqui somava ~16 mil linhas e travava o navegador.
-->

```sql casos
select *, '/de/casos/' || id_caso as link from mcdm.casos
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

# 🎯 Multikriterielle Entscheidung — zehn Schulen, ein Urteil mit Konfidenzintervall

> **Die Tabellenkalkulation verrechnet sich nicht. Sie verfehlt die Frage.** Nach Preis sortieren wählt das Billigste. Nach Expertennote sortieren wählt das Teuerste. Nach "erfüllt alle Anforderungen" filtern leert meist die Liste. Keine der drei beantwortet die gestellte Frage: *unter Alternativen, die sich widersprechen, welche wählen — und mit welcher Zuverlässigkeit?*

Dieses Dashboard führt **zehn multikriterielle Methoden** auf jeden Fall aus, zieht den Sieger aus dem **Borda-Konsens** zwischen ihnen und **stört dann die Gewichte 2.000 Mal**, um die einzige Frage zu beantworten, die das Gremium wirklich stellt: *und wenn wir ein etwas anderes Gewicht gesetzt hätten?*

<BigValue data={totais} value=casos title="Entscheidungsfälle" fmt=num0/>
<BigValue data={totais} value=alternativas title="Bewertete Alternativen" fmt=num0/>
<BigValue data={totais} value=robustos title="ROBUSTE Urteile" fmt=num0/>
<BigValue data={totais} value=frageis title="FRAGILE Urteile" fmt=num0/>

## 📋 Entscheidungsfälle

> Klicken Sie auf einen Fall, um den **vollständigen Bericht** zu öffnen: DEMATEL-Ursache-Wirkungs-Diagramm, Karte der zehn Schulen, ELECTRE-Kern, doppelte TOPSIS-Normalisierung, Borda-Konsens, Robustheit über 2.000 Universen, BCG-Matrix und die Entscheidungsmatrix.

<DataTable data={casos} rows=all rowShading=true link=link>
  <Column id=nome title="Fall"/>
  <Column id=dominio title="Domäne"/>
  <Column id=n_alternativas title="Alternativen" fmt=num0/>
  <Column id=vencedor_rotulo title="🏆 Sieger"/>
  <Column id=prob_vitoria title="Konfidenz (%)" fmt=num1 contentType=colorscale/>
  <Column id=classificacao title="Urteil"/>
</DataTable>

> **Das Urteil lesen.** `ROBUST` (≥ 90 %) = die Wahl hängt nicht von der Feinkalibrierung der Gewichte ab; sie kann ins Gremium. `WAHRSCHEINLICH` (60–90 %) = sie hält in den meisten Szenarien, aber der Zweite ist konkurrenzfähig. `FRAGIL` (unter 60 %) = **der erste Platz ist ein Artefakt der Gewichte** — das System sagt es, statt einen Pokal zu zeigen.

<BarChart data={resumo_dominio} x=dominio y=casos title="Fälle nach Anwendungsbereich" yAxisTitle="Casos"/>

## 🧮 DEMATEL — die Grundursache jeder Entscheidung

> Die Frage, die fast niemand stellt, bevor er Gewichte vergibt: **sind die Kriterien unabhängig?** Fast nie. Energieverbrauch *verursacht* Reichweite; Panzerung *verursacht* Gewicht, das *verursacht* Mobilitätsverlust. Beide als unabhängig zu addieren zählt dasselbe zweimal.
>
> **DEMATEL** (Gabus & Fontela, Battelle) baut die Gesamtrelationsmatrix `T = X(I−X)⁻¹` — die direkte **und indirekte** Einflüsse jeder Pfadlänge summiert — und trennt: `R+C` = Bedeutung im System; `R−C > 0` = **URSACHE** (Hebel: hier ansetzen) und `R−C < 0` = **WIRKUNG** (Thermometer: Ergebnis des schon Getanen).
>
> Die Spalte **Grundursache** unten ist das Kriterium mit dem höchsten `R−C` je Fall: dort bewegt ein Eingriff das ganze System.

<DataTable data={alavancas} rows=all rowShading=true>
  <Column id=nome title="Fall"/>
  <Column id=n_criterios title="Kriterien" fmt=num0/>
  <Column id=n_causas title="Ursachen" fmt=num0 contentType=colorscale/>
  <Column id=causa_raiz title="🔧 Grundursache (höchstes R−C)"/>
  <Column id=criterio_maior_peso title="Kriterium mit höchstem Gewicht"/>
  <Column id=maior_peso_pct title="Gewicht (%)" fmt=num1/>
</DataTable>

<BarChart data={alavancas} x=nome y={['n_causas','n_criterios']} type=grouped title="Kriterien, die in jedem Fall URSACHE sind (Hebel gegen die Gesamtzahl)" yAxisTitle="Critérios" swapXY=true/>

> **Öffnen Sie einen Fall**, um das vollständige Ursache-Wirkungs-Diagramm, die Tabelle mit getrennten `R` und `C` und die **Gesamtrelationsmatrix** mit den Verbindungen einzeln zu sehen.

## 🎲 BCG-Matrix — Chancenkarte je Kategorie

> Über *welche zu wählen* hinaus hat jede Kategorie ein **Chancenprofil**: wie viele Alternativen ⭐ Star (investieren), 🐄 Kuh (ernten), ❓ Fragezeichen (den Preis abwägen) und 🐕 Armer Hund (fallen lassen) sind. Eine Kategorie nur aus Fragezeichen ist ein teurer Markt; eine voller Kühe ein reifer Markt, in dem Geld wenig entscheidet.

<DataTable data={bcg_geral} rows=all rowShading=true>
  <Column id=nome title="Kategorie"/>
  <Column id=estrelas title="⭐" fmt=num0 contentType=colorscale/>
  <Column id=vacas title="🐄" fmt=num0 contentType=colorscale/>
  <Column id=interrogacoes title="❓" fmt=num0 contentType=colorscale/>
  <Column id=abacaxis title="🐕" fmt=num0 contentType=colorscale/>
  <Column id=total title="Gesamt" fmt=num0/>
  <Column id=quadrante_do_vencedor title="Quadrant des 1. Platzes"/>
</DataTable>

## ⚖️ Die zehn Entscheidungsschulen

> Jede Methode ist eine **andere Theorie darüber, was „besser" bedeutet**, und darum führen wir alle aus: wählen zehn unabhängige Schulen denselben Sieger, ist die Wahl kein Artefakt einer Methode. Weichen sie ab, zeigt die Abweichung, wo der echte Zielkonflikt liegt.

| Método | Escola | O que assume | Quando é a ferramenta certa |
|---|---|---|---|
| **AHP-TOPSIS 2n** | Distância à solução ideal | Compensação total entre Kriteriums | Kriterien quantitativos, decisor único |
| **ELECTRE I** | Überflügeltção | Incomparabilidade é permitida | Triagem: eliminar o que é dominado |
| **ELECTRE II** | Überflügeltção | Limiares forte e fraco | Ordenação completa com veto |
| **PROMETHEE II** | Überflügeltção | Preferência gradual (6 funções) | Quando "um pouco melhor" não é "melhor" |
| **MAUT** | Utilidade | Independência aditiva + Risikoaversion | Decisão sob incerteza |
| **MCDA-C** | Construtivista | Níveis Neutro/Bom ancorados | Diagnóstico absoluto, não só ranking |
| **VIKOR** | Compromisso | Utilidade do grupo × arrependimento máximo | Quando compensar é inaceitável |
| **TODIM** | Teoria dos Prospectos | Perda dói mais que ganho equivalente | Decisor avesso a perda (todos são) |
| **SAPEVO-M** | Ordinal multidecisor | Julgamento ordinal de vários decisores | Comitê que não concorda entre si |

## 🎯 Robustheit — das Konfidenzintervall der Entscheidung selbst

> **Das Problem.** Jede MCDM-Methode liefert einen Sieger mit impliziter Zuverlässigkeit von 100 %. Aber Gewichte sind nie exakt — sie sind Präferenzschätzungen. Wenn zwei Prozentpunkte im Gewicht eines Kriteriums den ersten und zweiten Platz tauschen, ist der "Sieger" ein Artefakt der Kalibrierung, keine Tatsache über die Menge. Niemand berichtet das. **Dort sterben Entscheidungen im Gremium.**
>
> **Die Lösung.** Wir störn die Gewichte mit `w' ~ Dirichlet(κ·w)` und ranken 2.000 Mal neu. Die Dirichlet ist die natürliche Wahl: ihr Träger ist genau der Simplex (positive Gewichte mit Summe 1) und sie erfüllt `E[w'] = w` — wir störn **ohne zu verzerren**. Mit κ = 200 schwankt ein Gewicht von 13 % um ±2,4 Pp.
>
> Das Urteil ist nicht mehr *"Modell C ist das beste"*, sondern **"Modell C gewinnt in 96 % der plausiblen Präferenzuniversen"**.

**Öffnen Sie einen Fall aus der Tabelle oben**, um das Ursache-Wirkungs-Diagramm, die Karte der zehn Schulen, die BCG-Matrix und die vollständige Verteilung der Positionen über die 2.000 Universen zu sehen.

---

<div style="text-align:center;margin-top:2rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="120" style="display:inline-block;opacity:0.9;"/>
  <div style="font-weight:700;margin-top:0.4rem;">ProfBru © 2026</div>
  <div style="margin-top:0.5rem;font-style:italic;font-size:0.9rem;color:#64748b;">
    MCDM Studio — Modelos MultiKriterium de Decisão<br/>
    Autor: <strong>ProfBru - Bruno Penedo</strong> © 2026 — ALLE RECHTE VORBEHALTEN<br/>
    profbruanbima@gmail.com
  </div>
</div>
