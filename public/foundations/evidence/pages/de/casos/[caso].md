---
title: "{params.caso}"
---

```sql caso
select * from mcdm.casos where id_caso = '${params.caso}'
```
```sql dematel_c
select * from mcdm.dematel where id_caso = '${params.caso}' order by prominencia desc
```
```sql relacao_c
-- Arestas do diagrama de influência: só as que superam o limiar α (média de T).
select * from mcdm.dematel_relacao
where id_caso = '${params.caso}' and acima_limiar = 1
order by intensidade desc limit 20
```
```sql relacao_todas_c
select * from mcdm.dematel_relacao where id_caso = '${params.caso}'
order by intensidade desc
```
```sql pesos_c
select * from mcdm.pesos_comparados where id_caso = '${params.caso}'
```
```sql consenso_c
select * from mcdm.consenso where id_caso = '${params.caso}'
order by rank_final limit 20
```
```sql robustez_c
select * from mcdm.robustez where id_caso = '${params.caso}'
order by prob_vitoria desc limit 20
```
```sql robustez_top
select * from mcdm.robustez where id_caso = '${params.caso}' order by prob_vitoria desc limit 1
```
```sql metodos_c
-- Apenas as 10 primeiras do consenso × 10 métodos = 100 linhas. Trazer as 38
-- alternativas daria 342 e o gráfico agrupado ficaria ilegível de qualquer forma.
select r.* from mcdm.ranking_metodos r
join mcdm.consenso c on c.id_caso = r.id_caso and c.alternativa = r.alternativa
where r.id_caso = '${params.caso}' and c.rank_final <= 10
```
```sql topsis_c
select * from mcdm.topsis where id_caso = '${params.caso}' order by rank_final limit 15
```
```sql nucleo_c
select * from mcdm.electre_nucleo where id_caso = '${params.caso}'
order by no_nucleo desc, domina desc limit 15
```
```sql matriz_c
-- Matriz de decisão das 10 primeiras colocadas. A tabela tem busca; para ver todas
-- as alternativas de um caso grande, consulte o banco diretamente.
select m.* from mcdm.matriz_decisao m
join mcdm.consenso c on c.id_caso = m.id_caso and c.alternativa = m.alternativa
where m.id_caso = '${params.caso}' and c.rank_final <= 10
```
```sql dist_c
select d.* from mcdm.distribuicao d
join mcdm.consenso c on c.id_caso = d.id_caso and c.alternativa = d.alternativa
where d.id_caso = '${params.caso}' and c.rank_final <= 10
```
```sql bcg_c
select * from mcdm.bcg where id_caso = '${params.caso}' order by rank_consenso limit 20
```
```sql bcg_res_c
select * from mcdm.bcg_resumo where id_caso = '${params.caso}'
```

```sql drsa_q
select * from mcdm.drsa_qualidade where id_caso = '${params.caso}'
```

```sql drsa_r
select * from mcdm.drsa_regras where id_caso = '${params.caso}'
```

<div style="text-align:center;margin:1rem 0 1.4rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="150" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.45rem;">ProfBru © 2026</div>
</div>

🌐 [Português](/casos/{params.caso}) · [English](/en/casos/{params.caso}) · [Español](/es/casos/{params.caso}) · [Français](/fr/casos/{params.caso}) · **Deutsch** · [中文](/zh/casos/{params.caso}) · [한국어](/ko/casos/{params.caso}) · [हिन्दी](/hi/casos/{params.caso}) · [עברית](/he/casos/{params.caso}) · [Русский](/ru/casos/{params.caso}) · [Svenska](/sv/casos/{params.caso}) · [Suomi](/fi/casos/{params.caso})

# {caso[0].nome}

> **{caso[0].descricao}**
>
> _Modellierter Entscheider: {caso[0].decisor} · Bereich: {caso[0].dominio}_

<BigValue data={caso} value=vencedor_rotulo title="🏆 Sieger des Konsenses"/>
<BigValue data={caso} value=prob_vitoria title="Gewinnt in (% der Universen)" fmt=num1/>
<BigValue data={caso} value=classificacao title="Urteil"/>
<BigValue data={caso} value=n_alternativas title="Alternativen" fmt=num0/>
<BigValue data={caso} value=n_metodos title="Methoden mit Rangfolge" fmt=num0/>
<BigValue data={caso} value=n_modelos title="Angewandte Modelle" fmt=num0/>

---

## 🧮 DEMATEL — welche Kriterien Ursache und welche Wirkung sind

> Antes de qualquer peso: **os Kriteriums não são independentes**. O DEMATEL monta a matriz de relação total `T = X(I−X)⁻¹` — somando influência direta **e indireta** de qualquer comprimento de caminho — e separa o que você pode **puxar** (CAUSA) do que apenas **mede o resultado** (EFEITO). Os pesos saem daí, por influência sistêmica.

<img src="/mc/{params.caso}/dematel_Ursache_Wirkung.png" alt="Diagrama Ursache-Wirkung DEMATEL" style="width:100%;border-radius:8px;"/>

<DataTable data={dematel_c} rows=all rowShading=true>
  <Column id=rotulo title="Kriterium"/>
  <Column id=unidade title="Einheit"/>
  <Column id=direcao title="Richtung"/>
  <Column id=influencia_exercida title="R (ausgeübter Einfluss)" fmt=num3/>
  <Column id=influencia_recebida title="C (empfangener Einfluss)" fmt=num3/>
  <Column id=prominencia title="Prominenz (R+C)" fmt=num3 contentType=colorscale/>
  <Column id=relacao title="Relation (R−C)" fmt=num3 contentType=colorscale/>
  <Column id=papel title="Rolle"/>
  <Column id=peso title="Abgeleitetes Gewicht" fmt=pct2/>
</DataTable>

<BarChart data={dematel_c} x=rotulo y=relacao title="DEMATEL Ursache-Wirkungs-Diagramm (R−C): über null = URSACHE" yAxisTitle="R − C" sort=false>
  <ReferenceLine y=0 color=info label="fronteira causa / efeito"/>
</BarChart>

### Matriz de relação total — quem influencia quem

> A tabela acima resume cada Kriterium em dois números. **Esta matriz mostra as ligações uma a uma**: `T = X(I − X)⁻¹` soma os caminhos diretos **e indiretos** de qualquer comprimento, e por isso revela influências que o especialista nunca declarou diretamente — A influencia B, B influencia C, logo A influencia C, e a matriz total contabiliza isso.
>
> Só aparecem as arestas **acima do limiar α** (a média de T). Abaixo dele, a intensidade é indistinguível de ruído de arredondamento, e um diagrama que desenhasse todas as ligações não informaria nada — toda matriz densa parece igualmente conectada.

<DataTable data={relacao_c} rows=12 rowShading=true>
  <Column id=origem_rotulo title="Quelle (beeinflusst)"/>
  <Column id=origem_papel title="Rolle der Quelle"/>
  <Column id=destino_rotulo title="Ziel (wird beeinflusst)"/>
  <Column id=destino_papel title="Rolle des Ziels"/>
  <Column id=intensidade title="Intensität tᵢⱼ" fmt=num4 contentType=colorscale/>
</DataTable>

<BarChart data={relacao_c} x=origem_rotulo y=intensidade series=destino_rotulo type=stacked title="Gesamteinfluss je Kriterium, aufgeschlüsselt nach Ziel" yAxisTitle="Intensidade acumulada" swapXY=true/>

### Quatro famílias de peso sobre o mesmo problema

> O **AHP** pergunta, par a par, quanto um Kriterium importa mais que outro. O **DEMATEL** mede influência sistêmica. **Onde divergem está o Wirkung de segunda ordem subestimado.**
>
> O **AHP Fuzzy** (Buckley, 1985) recebe o mesmo julgamento do AHP, mas não descarta a imprecisão: quem disse "5" quis dizer algo entre 4 e 6, e essa faixa é carregada até o fim. As colunas `l` e `u` são os limites do número triangular de cada peso.
>
> O **BWM** (Rezaei, 2015) resolve um problema operacional, não teórico: a matriz de Saaty com 9 Kriteriums exige 36 comparações e **ninguém a preenche com atenção até o fim**. O BWM pede apenas o melhor e o pior Kriterium e deriva o resto — 2n−3 comparações. A coluna `BWM CR` diz se o julgamento resultante é consistente.

<img src="/mc/{params.caso}/pesos_dematel_ahp.png" alt="DEMATEL, AHP e AHP Fuzzy" style="width:100%;border-radius:8px;"/>

<DataTable data={pesos_c} rows=all rowShading=true>
  <Column id=rotulo title="Kriterium"/>
  <Column id=papel title="Rolle"/>
  <Column id=peso_dematel title="DEMATEL" fmt=pct2/>
  <Column id=peso_ahp title="AHP" fmt=pct2/>
  <Column id=peso_ahp_fuzzy title="AHP Fuzzy" fmt=pct2/>
  <Column id=fuzzy_l title="l" fmt=pct2/>
  <Column id=fuzzy_u title="u" fmt=pct2/>
  <Column id=peso_bwm title="BWM" fmt=pct2/>
  <Column id=divergencia title="DEMATEL - AHP" fmt=pct2 contentType=colorscale/>
  <Column id=cr title="AHP CR" fmt=num4/>
  <Column id=bwm_cr title="BWM CR" fmt=num4/>
</DataTable>

> [!NOTE] O AHP Fuzzy **achata os extremos** em relação ao AHP crisp: a média geométrica com incerteza puxa os pesos para o centro. Um Kriterium que o AHP coloca em 50% costuma cair, e um que ele deixa em 0,4% costuma subir. Isso não é correção de erro, é o que acontece quando se admite que o julgamento tinha uma faixa. Se a ORDEM dos pesos muda entre os dois, a prioridade declarada não sobrevive à imprecisão do próprio decisor, e isso é informação para o comitê.

---

## ⚖️ Zehn Entscheidungsschulen zum selben Problem

> [!IMPORTANT] **Zwölf Modelle werden auf diesen Fall angewandt, und zehn gehen in dieses Diagramm ein.** **BWM** liefert Kriteriengewichte (siehe Tabelle der vier Familien oben) und **DRSA** liefert Regeln (eigener Abschnitt weiter unten) — keines von beiden erzeugt eine Position für eine Alternative, und deshalb werden **Borda-Konsens und Robustheit über diese zehn berechnet**. Hier alle zwölf zu zählen würde nahelegen, der Konsens aggregiere, was er nicht aggregiert.

> Jede Methode ist eine **andere Theorie darüber, was „besser“ bedeutet**. Stimmen die zehn überein, ist die Wahl kein Methodenartefakt. **Weichen sie ab, ist die Abweichung der Befund** — und sie zeigt meist genau, wo der echte Zielkonflikt liegt.
>
> **Fuzzy-TOPSIS** (Chen, 2000) verdient eine eigene Lesung: es ist nicht „AHP-TOPSIS mit Rauschen“. Neben den Dreieckszahlen tauscht es die Normalisierung (linear statt vektoriell) und die Ideallösung (absolut statt relativ). Vom AHP-TOPSIS 2n abzuweichen ist das **erwartete** Verhalten und misst, wie stark das Ranking von diesen Entscheidungen abhängt.

<img src="/mc/{params.caso}/mapa_metodos.png" alt="Platzierung por escola de decisão" style="width:100%;border-radius:8px;"/>

<BarChart data={metodos_c} x=rotulo y=rank_ series=metodo type=grouped title="Platzierung nach Entscheidungsschule (1. = beste)" yAxisTitle="Posição" swapXY=true/>

### ELECTRE I — der Kern (Kernel)

> Vor dem Ranking **aussortieren**: Der Kern ist die Menge, die keine andere Alternative überflügelt. Ein einelementiger Kern beendet die Entscheidung; ein zu großer Kern zeigt, dass die Kriterien nicht trennen — und das Problem liegt in der Modellierung, nicht in der Rechnung.

<DataTable data={nucleo_c} rows=12 rowShading=true>
  <Column id=rotulo title="Alternative"/>
  <Column id=no_nucleo title="Im Kern?" fmt=boolean/>
  <Column id=domina title="Überflügelt" fmt=num0/>
  <Column id=dominada title="Wird überflügelt von" fmt=num0/>
</DataTable>

### AHP-TOPSIS 2N — die doppelte Normalisierung

> TOPSIS ist **empfindlich gegenüber der gewählten Normalisierung**. Wir führen beide aus (vektoriell und Min-Max) und berichten die Übereinstimmung: Die Spalte **Robust?** ist methodische Ehrlichkeit.

<DataTable data={topsis_c} rows=12 rowShading=true>
  <Column id=rank_final title="#"/>
  <Column id=rotulo title="Alternative"/>
  <Column id=ci_vector title="Ci vektoriell" fmt=num4/>
  <Column id=ci_minmax title="Ci Min-Max" fmt=num4/>
  <Column id=ci_final title="Ci final" fmt=num4 contentType=colorscale/>
  <Column id=concordante title="Robust?" fmt=boolean/>
</DataTable>

---

## 🤝 Borda-Konsens

<DataTable data={consenso_c} rows=all rowShading=true>
  <Column id=rank_final title="#" contentType=colorscale/>
  <Column id=rotulo title="Alternative"/>
  <Column id=borda title="Borda-Punkte" fmt=num0/>
  <Column id=rank_medio title="Durchschnittsplatz" fmt=num2/>
  <Column id=unanime title="Einstimmig?" fmt=boolean/>
  <Column id=prob_vitoria title="Gewinnt in (%)" fmt=num1 contentType=colorscale/>
  <Column id=rank_p95 title="Schlechtester Fall (p95)" fmt=num0/>
</DataTable>

---

## 🎯 Robustheit — das Konfidenzintervall der Entscheidung selbst

> **Das Problem.** Gewichte sind nie exakt — sie sind Präferenzschätzungen. Wenn zwei Prozentpunkte den ersten und zweiten Platz tauschen, ist der „Sieger“ ein Artefakt der Kalibrierung.
>
> **Die Lösung.** Wir stören mit `w' ~ Dirichlet(κ·w)` und ranken **2.000 Mal** neu. Die Dirichlet hat ihren Träger genau auf dem Simplex und erfüllt `E[w'] = w` — wir stören **ohne zu verzerren**.

<BigValue data={robustez_top} value=rotulo title="Führender bei gestörten Gewichten"/>
<BigValue data={robustez_top} value=prob_vitoria title="Gewinnt in (%)" fmt=num1/>
<BigValue data={robustez_top} value=rank_p95 title="Schlechtestmögliche Position" fmt=num0/>

<img src="/mc/{params.caso}/Robustheit.png" alt="Robustheit sob pesos perturbados" style="width:100%;border-radius:8px;"/>

<DataTable data={robustez_c} rows=15 rowShading=true>
  <Column id=rotulo title="Alternative"/>
  <Column id=prob_vitoria title="Gewinnt den Konsens (%)" fmt=num1 contentType=colorscale/>
  <Column id=prob_top3 title="Top-3 (%)" fmt=num1/>
  <Column id=rank_medio title="Typische Platzierung" fmt=num2/>
  <Column id=rank_p05 title="Bester Fall (p05)" fmt=num0/>
  <Column id=rank_p95 title="Schlechtester Fall (p95)" fmt=num0/>
</DataTable>

### Vollständige Verteilung der Positionen

> Ein durchgehend grüner Balken ist eine Position, die **nicht von den Gewichten abhängt**. Ein gefleckter Balken ist eine umstrittene Position.

<img src="/mc/{params.caso}/distribuicao_posicoes.png" alt="Distribuição das posições" style="width:100%;border-radius:8px;"/>

---

## 🎲 Matriz BCG — que ITPO de aposta é cada Alternative

> O consenso responde **qual escolher**. A BCG responde **que tipo de aposta cada uma é** — pergunta diferente, e igualmente decisiva na hora de assinar.
>
> Dois eixos, ambos derivados dos **mesmos pesos do DEMATEL** que alimentam os dez métodos (renormalizados por grupo, de modo que a BCG é um segundo corte da mesma modelagem, não uma segunda modelagem):
>
> - **Attraktivität** (Y) — desempenho ponderado nos Kriteriums de **Nutzen** - **Kostenposition** (X) — quanto entrega por unidade de **sacrifício**
>
> Os cortes são as **medianas** de cada eixo, não o ponto médio: mediana divide o conjunto em duas metades reais, enquanto 0,5 deixaria quadrantes vazios num conjunto assimétrico — e quadrante vazio não informa nada.

<BigValue data={bcg_res_c} value=estrelas title="⭐ Sterne" fmt=num0/>
<BigValue data={bcg_res_c} value=vacas title="🐄 Melkkühe" fmt=num0/>
<BigValue data={bcg_res_c} value=interrogacoes title="❓ Fragezeichen" fmt=num0/>
<BigValue data={bcg_res_c} value=abacaxis title="🐕 Arme Hunde" fmt=num0/>

<img src="/mc/{params.caso}/matriz_bcg.png" alt="Matriz BCG" style="width:100%;border-radius:8px;"/>

| Quadrant | Leitura de decisão |
|---|---|
| ⭐ **Estrela** | Alta atratividade **e** boa posição de Kosten — a aposta natural: investir e padronizar. |
| 🐄 **Vaca leiteira** | Entrega o essencial pelo **menor sacrifício**. É a escolha de quem tem orçamento apertado. |
| ❓ **Interrogação** | Desempenho alto a **preço alto**. Só se justifica se o prêmio for necessário. |
| 🐕 **Abacaxi** | Nem entrega, nem é barata. **Descartar.** |

> **O cruzamento é onde mora o achado.** Um 2º colocado que é 🐄 Vaca costuma ser a escolha real de quem tem restrição orçamentária; um 2º colocado ❓ Interrogação só compensa se você precisa do prêmio de desempenho que ele cobra.

<DataTable data={bcg_c} rows=15 rowShading=true>
  <Column id=rank_consenso title="#" contentType=colorscale/>
  <Column id=rotulo title="Alternative"/>
  <Column id=quadrante_rotulo title="Quadrant"/>
  <Column id=atratividade title="Attraktivität" fmt=num3 contentType=colorscale/>
  <Column id=posicao title="Kostenposition" fmt=num3 contentType=colorscale/>
  <Column id=acao title="Was zu tun ist"/>
</DataTable>

---

## 📏 DRSA — die Regel, die frühere Entscheidungen erklärt

> Die anderen elf Modelle verlangen **erklärte** Präferenzen: Gewichte, Vergleiche, Schwellen. **DRSA** (Greco, Matarazzo & Słowiński) geht den umgekehrten Weg — es nimmt bereits getroffene Entscheidungen und liefert die **Regel**, die sie erklärt, in klarer Sprache, für jemanden, der nicht weiß, was vektorielle Normalisierung ist. Es ist die einzige Familie hier, die aus der Historie lernt, statt zu verlangen, dass jemand seine Präferenz erklären kann.

<div class="grid grid-cols-3 gap-4">
<BigValue data={drsa_q} value=gamma title="γ — Güte der Approximation" fmt=pct1/>
<BigValue data={drsa_q} value=n_regras title="Induzierte Regeln" fmt=num0/>
<BigValue data={drsa_q} value=n_violacoes title="Paare, die die Dominanz verletzen" fmt=num0/>
</div>

<DataTable data={drsa_r} rows=all rowShading=true>
  <Column id=n_regra title="#"/>
  <Column id=texto title="Regel"/>
  <Column id=cobertura title="Deckt ab" fmt=num0/>
  <Column id=certeza title="Sicherheit" fmt=pct0/>
</DataTable>

> [!NOTE] **γ = 100 %** bedeutet, dass die Dominanzrelation alle Alternativen eindeutig klassifiziert: Die Historie ist kohärent und die Regeln beschreiben sie vollständig. **γ < 100 %** ist Diagnose, kein Defekt — es besagt, dass es Paare gibt, in denen die dominierte Alternative vorgezogen wurde, und die Spalte *Paare, die die Dominanz verletzen* zählt sie. Dann hat die frühere Entscheidung Ausnahmen, und das zu wissen ist mehr wert als ein sauberes Ranking.

---

## 📐 Entscheidungsmatrix

> Os dados de entrada. **Substitua pela sua cotação, seu edital ou seu ensaio** — o motor é o mesmo; os dados é que são seus.

<DataTable data={matriz_c} rows=25 rowShading=true search=true>
  <Column id=alternativa_rotulo title="Alternative"/>
  <Column id=criterio_rotulo title="Kriterium"/>
  <Column id=direcao title="Richtung"/>
  <Column id=valor title="Wert" fmt=num2/>
  <Column id=unidade title="Einheit"/>
</DataTable>

<LinkButton url='/de'>← Voltar ao índice de casos</LinkButton>

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
