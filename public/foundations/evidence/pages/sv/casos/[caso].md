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

🌐 [Português](/casos/{params.caso}) · [English](/en/casos/{params.caso}) · [Español](/es/casos/{params.caso}) · [Français](/fr/casos/{params.caso}) · [Deutsch](/de/casos/{params.caso}) · [中文](/zh/casos/{params.caso}) · [한국어](/ko/casos/{params.caso}) · [हिन्दी](/hi/casos/{params.caso}) · [עברית](/he/casos/{params.caso}) · [Русский](/ru/casos/{params.caso}) · **Svenska** · [Suomi](/fi/casos/{params.caso})

# {caso[0].nome}

> **{caso[0].descricao}**
>
> _Modellerad beslutsfattare: {caso[0].decisor} · Område: {caso[0].dominio}_

<BigValue data={caso} value=vencedor_rotulo title="🏆 Konsensusvinnare"/>
<BigValue data={caso} value=prob_vitoria title="Vinner i (% av universum)" fmt=num1/>
<BigValue data={caso} value=classificacao title="Utlåtande"/>
<BigValue data={caso} value=n_alternativas title="Alternativ" fmt=num0/>
<BigValue data={caso} value=n_metodos title="Metoder som rangordnar" fmt=num0/>
<BigValue data={caso} value=n_modelos title="Tillämpade modeller" fmt=num0/>

---

## 🧮 DEMATEL — vilka kriterier är orsak och vilka är verkan

> Antes de qualquer peso: **os Kriteriums não são independentes**. O DEMATEL monta a matriz de relação total `T = X(I−X)⁻¹` — somando influência direta **e indireta** de qualquer comprimento de caminho — e separa o que você pode **puxar** (CAUSA) do que apenas **mede o resultado** (EFEITO). Os pesos saem daí, por influência sistêmica.

<img src="/mc/{params.caso}/dematel_orsak_verkan.png" alt="Diagrama orsak-verkan DEMATEL" style="width:100%;border-radius:8px;"/>

<DataTable data={dematel_c} rows=all rowShading=true>
  <Column id=rotulo title="Kriterium"/>
  <Column id=unidade title="Enhet"/>
  <Column id=direcao title="Riktning"/>
  <Column id=influencia_exercida title="R (utövat inflytande)" fmt=num3/>
  <Column id=influencia_recebida title="C (mottaget inflytande)" fmt=num3/>
  <Column id=prominencia title="Framträdande (R+C)" fmt=num3 contentType=colorscale/>
  <Column id=relacao title="Relation (R−C)" fmt=num3 contentType=colorscale/>
  <Column id=papel title="Roll"/>
  <Column id=peso title="Härledd vikt" fmt=pct2/>
</DataTable>

<BarChart data={dematel_c} x=rotulo y=relacao title="DEMATEL orsak–verkan-diagram (R−C): över noll = ORSAK" yAxisTitle="R − C" sort=false>
  <ReferenceLine y=0 color=info label="fronteira causa / efeito"/>
</BarChart>

### Matriz de relação total — quem influencia quem

> A tabela acima resume cada Kriterium em dois números. **Esta matriz mostra as ligações uma a uma**: `T = X(I − X)⁻¹` soma os caminhos diretos **e indiretos** de qualquer comprimento, e por isso revela influências que o especialista nunca declarou diretamente — A influencia B, B influencia C, logo A influencia C, e a matriz total contabiliza isso.
>
> Só aparecem as arestas **acima do limiar α** (a média de T). Abaixo dele, a intensidade é indistinguível de ruído de arredondamento, e um diagrama que desenhasse todas as ligações não informaria nada — toda matriz densa parece igualmente conectada.

<DataTable data={relacao_c} rows=12 rowShading=true>
  <Column id=origem_rotulo title="Källa (påverkar)"/>
  <Column id=origem_papel title="Källans roll"/>
  <Column id=destino_rotulo title="Mål (påverkas)"/>
  <Column id=destino_papel title="Målets roll"/>
  <Column id=intensidade title="Intensitet tᵢⱼ" fmt=num4 contentType=colorscale/>
</DataTable>

<BarChart data={relacao_c} x=origem_rotulo y=intensidade series=destino_rotulo type=stacked title="Totalt inflytande från varje kriterium, uppdelat per mål" yAxisTitle="Intensidade acumulada" swapXY=true/>

### Quatro famílias de peso sobre o mesmo problema

> O **AHP** pergunta, par a par, quanto um Kriterium importa mais que outro. O **DEMATEL** mede influência sistêmica. **Onde divergem está o verkan de segunda ordem subestimado.**
>
> O **AHP Fuzzy** (Buckley, 1985) recebe o mesmo julgamento do AHP, mas não descarta a imprecisão: quem disse "5" quis dizer algo entre 4 e 6, e essa faixa é carregada até o fim. As colunas `l` e `u` são os limites do número triangular de cada peso.
>
> O **BWM** (Rezaei, 2015) resolve um problema operacional, não teórico: a matriz de Saaty com 9 Kriteriums exige 36 comparações e **ninguém a preenche com atenção até o fim**. O BWM pede apenas o melhor e o pior Kriterium e deriva o resto — 2n−3 comparações. A coluna `BWM CR` diz se o julgamento resultante é consistente.

<img src="/mc/{params.caso}/pesos_dematel_ahp.png" alt="DEMATEL, AHP e AHP Fuzzy" style="width:100%;border-radius:8px;"/>

<DataTable data={pesos_c} rows=all rowShading=true>
  <Column id=rotulo title="Kriterium"/>
  <Column id=papel title="Roll"/>
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

## ⚖️ Tio beslutsskolor på samma problem

> [!IMPORTANT] **Tolv modeller tillämpas på detta fall, och tio ingår i detta diagram.** **BWM** ger kriterievikter (se tabellen över de fyra familjerna ovan) och **DRSA** ger regler (eget avsnitt längre ned) — ingen av dem ger en placering för ett alternativ, och därför beräknas **Borda-konsensus och robusthet över dessa tio**. Att räkna alla tolv här skulle antyda att konsensus sammanväger det den inte sammanväger.

> Varje metod är en **egen teori om vad ”bäst” betyder**. När de tio är eniga är valet ingen metodartefakt. **När de skiljer sig åt är avvikelsen fyndet** — och den pekar oftast ut exakt var den verkliga avvägningen ligger.
>
> **Fuzzy TOPSIS** (Chen, 2000) förtjänar egen läsning: det är inte ”AHP-TOPSIS med brus”. Utöver de triangulära talen byter den normalisering (linjär i stället för vektoriell) och ideallösning (absolut i stället för relativ). Att avvika från AHP-TOPSIS 2n är det **förväntade** beteendet, och det mäter hur mycket rangordningen beror på dessa val.

<img src="/mc/{params.caso}/mapa_metodos.png" alt="Placering por escola de decisão" style="width:100%;border-radius:8px;"/>

<BarChart data={metodos_c} x=rotulo y=rank_ series=metodo type=grouped title="Placering per beslutsskola (1:a = bäst)" yAxisTitle="Posição" swapXY=true/>

### ELECTRE I — kärnan (kernel)

> Före rangordning: **sålla bort**. Kärnan är den mängd som inget annat alternativ överklassar. En kärna med ett enda element avgör beslutet; en alltför stor kärna visar att kriterierna inte skiljer — och problemet ligger i modelleringen, inte i beräkningen.

<DataTable data={nucleo_c} rows=12 rowShading=true>
  <Column id=rotulo title="Alternativ"/>
  <Column id=no_nucleo title="I kärnan?" fmt=boolean/>
  <Column id=domina title="Överklassar" fmt=num0/>
  <Column id=dominada title="Överklassas av" fmt=num0/>
</DataTable>

### AHP-TOPSIS 2N — den dubbla normaliseringen

> TOPSIS är **känslig för vald normalisering**. Vi kör båda (vektoriell och min-max) och redovisar samstämmigheten: kolumnen **Robust?** är metodologisk hederlighet.

<DataTable data={topsis_c} rows=12 rowShading=true>
  <Column id=rank_final title="#"/>
  <Column id=rotulo title="Alternativ"/>
  <Column id=ci_vector title="Ci vektoriell" fmt=num4/>
  <Column id=ci_minmax title="Ci min-max" fmt=num4/>
  <Column id=ci_final title="Ci slutlig" fmt=num4 contentType=colorscale/>
  <Column id=concordante title="Robust?" fmt=boolean/>
</DataTable>

---

## 🤝 Borda-konsensus

<DataTable data={consenso_c} rows=all rowShading=true>
  <Column id=rank_final title="#" contentType=colorscale/>
  <Column id=rotulo title="Alternativ"/>
  <Column id=borda title="Borda-poäng" fmt=num0/>
  <Column id=rank_medio title="Genomsnittlig placering" fmt=num2/>
  <Column id=unanime title="Enhälligt?" fmt=boolean/>
  <Column id=prob_vitoria title="Vinner i (%)" fmt=num1 contentType=colorscale/>
  <Column id=rank_p95 title="Sämsta fall (p95)" fmt=num0/>
</DataTable>

---

## 🎯 Robusthet — beslutets eget konfidensintervall

> **Problemet.** Vikter är aldrig exakta — de är preferensskattningar. Om två procentenheter byter plats ett och två är ”vinnaren” en artefakt av kalibreringen.
>
> **Lösningen.** Vi stör med `w' ~ Dirichlet(κ·w)` och rangordnar om **2 000 gånger**. Dirichlet har sitt stöd exakt på simplexet och uppfyller `E[w'] = w` — vi stör **utan att snedvrida**.

<BigValue data={robustez_top} value=rotulo title="Ledare vid störda vikter"/>
<BigValue data={robustez_top} value=prob_vitoria title="Vinner i (%)" fmt=num1/>
<BigValue data={robustez_top} value=rank_p95 title="Sämsta rimliga placering" fmt=num0/>

<img src="/mc/{params.caso}/Robusthet.png" alt="Robusthet sob pesos perturbados" style="width:100%;border-radius:8px;"/>

<DataTable data={robustez_c} rows=15 rowShading=true>
  <Column id=rotulo title="Alternativ"/>
  <Column id=prob_vitoria title="Vinner konsensus (%)" fmt=num1 contentType=colorscale/>
  <Column id=prob_top3 title="Top-3 (%)" fmt=num1/>
  <Column id=rank_medio title="Typisk placering" fmt=num2/>
  <Column id=rank_p05 title="Bästa fall (p05)" fmt=num0/>
  <Column id=rank_p95 title="Sämsta fall (p95)" fmt=num0/>
</DataTable>

### Fullständig fördelning av placeringar

> En helt grön stapel är en placering som **inte beror på vikterna**. En fläckig stapel är en omstridd placering.

<img src="/mc/{params.caso}/distribuicao_posicoes.png" alt="Distribuição das posições" style="width:100%;border-radius:8px;"/>

---

## 🎲 Matriz BCG — que ITPO de aposta é cada Alternativ

> O consenso responde **qual escolher**. A BCG responde **que tipo de aposta cada uma é** — pergunta diferente, e igualmente decisiva na hora de assinar.
>
> Dois eixos, ambos derivados dos **mesmos pesos do DEMATEL** que alimentam os dez métodos (renormalizados por grupo, de modo que a BCG é um segundo corte da mesma modelagem, não uma segunda modelagem):
>
> - **Attraktivitet** (Y) — desempenho ponderado nos Kriteriums de **nytta** - **Kostnadsläge** (X) — quanto entrega por unidade de **sacrifício**
>
> Os cortes são as **medianas** de cada eixo, não o ponto médio: mediana divide o conjunto em duas metades reais, enquanto 0,5 deixaria quadrantes vazios num conjunto assimétrico — e quadrante vazio não informa nada.

<BigValue data={bcg_res_c} value=estrelas title="⭐ Stjärnor" fmt=num0/>
<BigValue data={bcg_res_c} value=vacas title="🐄 Kassakor" fmt=num0/>
<BigValue data={bcg_res_c} value=interrogacoes title="❓ Frågetecken" fmt=num0/>
<BigValue data={bcg_res_c} value=abacaxis title="🐕 Hundar" fmt=num0/>

<img src="/mc/{params.caso}/matriz_bcg.png" alt="Matriz BCG" style="width:100%;border-radius:8px;"/>

| Kvadrant | Leitura de decisão |
|---|---|
| ⭐ **Estrela** | Alta atratividade **e** boa posição de kostnad — a aposta natural: investir e padronizar. |
| 🐄 **Vaca leiteira** | Entrega o essencial pelo **menor sacrifício**. É a escolha de quem tem orçamento apertado. |
| ❓ **Interrogação** | Desempenho alto a **preço alto**. Só se justifica se o prêmio for necessário. |
| 🐕 **Abacaxi** | Nem entrega, nem é barata. **Descartar.** |

> **O cruzamento é onde mora o achado.** Um 2º colocado que é 🐄 Vaca costuma ser a escolha real de quem tem restrição orçamentária; um 2º colocado ❓ Interrogação só compensa se você precisa do prêmio de desempenho que ele cobra.

<DataTable data={bcg_c} rows=15 rowShading=true>
  <Column id=rank_consenso title="#" contentType=colorscale/>
  <Column id=rotulo title="Alternativ"/>
  <Column id=quadrante_rotulo title="Kvadrant"/>
  <Column id=atratividade title="Attraktivitet" fmt=num3 contentType=colorscale/>
  <Column id=posicao title="Kostnadsläge" fmt=num3 contentType=colorscale/>
  <Column id=acao title="Vad som bör göras"/>
</DataTable>

---

## 📏 DRSA — regeln som förklarar tidigare beslut

> De övriga elva modellerna kräver **deklarerade** preferenser: vikter, jämförelser, trösklar. **DRSA** (Greco, Matarazzo & Słowiński) går motsatt väg — den tar beslut som redan fattats och ger den **regel** som förklarar dem, i klarspråk, för den som inte vet vad vektoriell normalisering är. Det är den enda familjen här som lär av historik i stället för att kräva att någon kan uttala vad hen föredrar.

<div class="grid grid-cols-3 gap-4">
<BigValue data={drsa_q} value=gamma title="γ — approximationens kvalitet" fmt=pct1/>
<BigValue data={drsa_q} value=n_regras title="Inducerade regler" fmt=num0/>
<BigValue data={drsa_q} value=n_violacoes title="Par som bryter mot dominans" fmt=num0/>
</div>

<DataTable data={drsa_r} rows=all rowShading=true>
  <Column id=n_regra title="#"/>
  <Column id=texto title="Regel"/>
  <Column id=cobertura title="Täcker" fmt=num0/>
  <Column id=certeza title="Säkerhet" fmt=pct0/>
</DataTable>

> [!NOTE] **γ = 100 %** betyder att dominansrelationen klassificerar alla alternativ utan tvetydighet: historiken är sammanhängande och reglerna beskriver den helt. **γ < 100 %** är diagnos, inte defekt — det säger att det finns par där det dominerade alternativet föredrogs, och kolumnen *Par som bryter mot dominans* räknar hur många. Då har det tidigare beslutet undantag, och att veta det är värt mer än en ren rangordning.

---

## 📐 Beslutsmatris

> Os dados de entrada. **Substitua pela sua cotação, seu edital ou seu ensaio** — o motor é o mesmo; os dados é que são seus.

<DataTable data={matriz_c} rows=25 rowShading=true search=true>
  <Column id=alternativa_rotulo title="Alternativ"/>
  <Column id=criterio_rotulo title="Kriterium"/>
  <Column id=direcao title="Riktning"/>
  <Column id=valor title="Värde" fmt=num2/>
  <Column id=unidade title="Enhet"/>
</DataTable>

<LinkButton url='/sv'>← Voltar ao índice de casos</LinkButton>

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
