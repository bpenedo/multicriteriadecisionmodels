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

🌐 [Português](/casos/{params.caso}) · [English](/en/casos/{params.caso}) · [Español](/es/casos/{params.caso}) · [Français](/fr/casos/{params.caso}) · [Deutsch](/de/casos/{params.caso}) · [中文](/zh/casos/{params.caso}) · [한국어](/ko/casos/{params.caso}) · [हिन्दी](/hi/casos/{params.caso}) · [עברית](/he/casos/{params.caso}) · [Русский](/ru/casos/{params.caso}) · [Svenska](/sv/casos/{params.caso}) · **Suomi**

# {caso[0].nome}

> **{caso[0].descricao}**
>
> _Mallinnettu päättäjä: {caso[0].decisor} · Alue: {caso[0].dominio}_

<BigValue data={caso} value=vencedor_rotulo title="🏆 Konsensuksen voittaja"/>
<BigValue data={caso} value=prob_vitoria title="Voittaa (% universumeista)" fmt=num1/>
<BigValue data={caso} value=classificacao title="Tuomio"/>
<BigValue data={caso} value=n_alternativas title="Vaihtoehdot" fmt=num0/>
<BigValue data={caso} value=n_metodos title="Järjestävät menetelmät" fmt=num0/>
<BigValue data={caso} value=n_modelos title="Sovelletut mallit" fmt=num0/>

---

## 🧮 DEMATEL — mitkä kriteerit ovat syitä ja mitkä seurauksia

> Antes de qualquer peso: **os Kriteeris não são independentes**. O DEMATEL monta a matriz de relação total `T = X(I−X)⁻¹` — somando influência direta **e indireta** de qualquer comprimento de caminho — e separa o que você pode **puxar** (CAUSA) do que apenas **mede o resultado** (EFEITO). Os pesos saem daí, por influência sistêmica.

<img src="/mc/{params.caso}/dematel_syy_seuraus.png" alt="Diagrama syy-seuraus DEMATEL" style="width:100%;border-radius:8px;"/>

<DataTable data={dematel_c} rows=all rowShading=true>
  <Column id=rotulo title="Kriteeri"/>
  <Column id=unidade title="Yksikkö"/>
  <Column id=direcao title="Suunta"/>
  <Column id=influencia_exercida title="R (annettu vaikutus)" fmt=num3/>
  <Column id=influencia_recebida title="C (saatu vaikutus)" fmt=num3/>
  <Column id=prominencia title="Näkyvyys (R+C)" fmt=num3 contentType=colorscale/>
  <Column id=relacao title="Suhde (R−C)" fmt=num3 contentType=colorscale/>
  <Column id=papel title="Rooli"/>
  <Column id=peso title="Johdettu paino" fmt=pct2/>
</DataTable>

<BarChart data={dematel_c} x=rotulo y=relacao title="DEMATEL syy–seuraus-kaavio (R−C): nollan yläpuolella = SYY" yAxisTitle="R − C" sort=false>
  <ReferenceLine y=0 color=info label="fronteira causa / efeito"/>
</BarChart>

### Matriz de relação total — quem influencia quem

> A tabela acima resume cada Kriteeri em dois números. **Esta matriz mostra as ligações uma a uma**: `T = X(I − X)⁻¹` soma os caminhos diretos **e indiretos** de qualquer comprimento, e por isso revela influências que o especialista nunca declarou diretamente — A influencia B, B influencia C, logo A influencia C, e a matriz total contabiliza isso.
>
> Só aparecem as arestas **acima do limiar α** (a média de T). Abaixo dele, a intensidade é indistinguível de ruído de arredondamento, e um diagrama que desenhasse todas as ligações não informaria nada — toda matriz densa parece igualmente conectada.

<DataTable data={relacao_c} rows=12 rowShading=true>
  <Column id=origem_rotulo title="Lähde (vaikuttaa)"/>
  <Column id=origem_papel title="Lähteen rooli"/>
  <Column id=destino_rotulo title="Kohde (saa vaikutusta)"/>
  <Column id=destino_papel title="Kohteen rooli"/>
  <Column id=intensidade title="Voimakkuus tᵢⱼ" fmt=num4 contentType=colorscale/>
</DataTable>

<BarChart data={relacao_c} x=origem_rotulo y=intensidade series=destino_rotulo type=stacked title="Kunkin kriteerin kokonaisvaikutus kohteittain eriteltynä" yAxisTitle="Intensidade acumulada" swapXY=true/>

### Quatro famílias de peso sobre o mesmo problema

> O **AHP** pergunta, par a par, quanto um Kriteeri importa mais que outro. O **DEMATEL** mede influência sistêmica. **Onde divergem está o seuraus de segunda ordem subestimado.**
>
> O **AHP Fuzzy** (Buckley, 1985) recebe o mesmo julgamento do AHP, mas não descarta a imprecisão: quem disse "5" quis dizer algo entre 4 e 6, e essa faixa é carregada até o fim. As colunas `l` e `u` são os limites do número triangular de cada peso.
>
> O **BWM** (Rezaei, 2015) resolve um problema operacional, não teórico: a matriz de Saaty com 9 Kriteeris exige 36 comparações e **ninguém a preenche com atenção até o fim**. O BWM pede apenas o melhor e o pior Kriteeri e deriva o resto — 2n−3 comparações. A coluna `BWM CR` diz se o julgamento resultante é consistente.

<img src="/mc/{params.caso}/pesos_dematel_ahp.png" alt="DEMATEL, AHP e AHP Fuzzy" style="width:100%;border-radius:8px;"/>

<DataTable data={pesos_c} rows=all rowShading=true>
  <Column id=rotulo title="Kriteeri"/>
  <Column id=papel title="Rooli"/>
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

> [!NOTE] O AHP Fuzzy **achata os extremos** em relação ao AHP crisp: a média geométrica com incerteza puxa os pesos para o centro. Um Kriteeri que o AHP coloca em 50% costuma cair, e um que ele deixa em 0,4% costuma subir. Isso não é correção de erro, é o que acontece quando se admite que o julgamento tinha uma faixa. Se a ORDEM dos pesos muda entre os dois, a prioridade declarada não sobrevive à imprecisão do próprio decisor, e isso é informação para o comitê.

---

## ⚖️ Kymmenen päätöksenteon koulukuntaa samaan ongelmaan

> [!IMPORTANT] **Tähän tapaukseen sovelletaan kahtatoista mallia, ja kymmenen on mukana tässä kuvaajassa.** **BWM** tuottaa kriteeripainoja (ks. neljän perheen taulukko yllä) ja **DRSA** tuottaa sääntöjä (oma osionsa alempana) — kumpikaan ei tuota vaihtoehdon sijoitusta, ja siksi **Borda-konsensus ja robustius lasketaan näiden kymmenen yli**. Kaikkien kahdentoista laskeminen tässä antaisi ymmärtää, että konsensus yhdistää sen, mitä se ei yhdistä.

> Jokainen menetelmä on **eri teoria siitä, mitä ”parempi” tarkoittaa**. Kun kymmenen ovat yhtä mieltä, valinta ei ole menetelmän artefakti. **Kun ne eroavat, ero itsessään on löydös** — ja se osoittaa yleensä täsmälleen, missä todellinen kompromissi on.
>
> **Sumea TOPSIS** (Chen, 2000) ansaitsee oman lukunsa: se ei ole ”AHP-TOPSIS kohinalla”. Kolmiolukujen lisäksi se vaihtaa normalisoinnin (lineaarinen vektorimuotoisen sijaan) ja ideaaliratkaisun (absoluuttinen suhteellisen sijaan). Poikkeaminen AHP-TOPSIS 2n:stä on **odotettua** käytöstä, ja se mittaa, kuinka paljon järjestys riippuu näistä valinnoista.

<img src="/mc/{params.caso}/mapa_metodos.png" alt="Sija por escola de decisão" style="width:100%;border-radius:8px;"/>

<BarChart data={metodos_c} x=rotulo y=rank_ series=metodo type=grouped title="Sijoitus päätöskoulukunnittain (1. = paras)" yAxisTitle="Posição" swapXY=true/>

### ELECTRE I — ydin (kernel)

> Ennen järjestämistä: **karsi**. Ydin on se joukko, jota mikään muu vaihtoehto ei ylitä. Yhden alkion ydin ratkaisee päätöksen; liian suuri ydin kertoo, etteivät kriteerit erottele — ja ongelma on mallinnuksessa, ei laskennassa.

<DataTable data={nucleo_c} rows=12 rowShading=true>
  <Column id=rotulo title="Vaihtoehto"/>
  <Column id=no_nucleo title="Ytimessä?" fmt=boolean/>
  <Column id=domina title="Ylittää" fmt=num0/>
  <Column id=dominada title="Jää alle" fmt=num0/>
</DataTable>

### AHP-TOPSIS 2N — kaksoisnormalisointi

> TOPSIS on **herkkä valitulle normalisoinnille**. Ajamme molemmat (vektorimuotoisen ja min-max) ja raportoimme yhtäpitävyyden: sarake **Robusti?** on menetelmällistä rehellisyyttä.

<DataTable data={topsis_c} rows=12 rowShading=true>
  <Column id=rank_final title="#"/>
  <Column id=rotulo title="Vaihtoehto"/>
  <Column id=ci_vector title="Ci vektori" fmt=num4/>
  <Column id=ci_minmax title="Ci min-max" fmt=num4/>
  <Column id=ci_final title="Ci lopullinen" fmt=num4 contentType=colorscale/>
  <Column id=concordante title="Robusti?" fmt=boolean/>
</DataTable>

---

## 🤝 Bordan konsensus

<DataTable data={consenso_c} rows=all rowShading=true>
  <Column id=rank_final title="#" contentType=colorscale/>
  <Column id=rotulo title="Vaihtoehto"/>
  <Column id=borda title="Borda-pisteet" fmt=num0/>
  <Column id=rank_medio title="Keskimääräinen sija" fmt=num2/>
  <Column id=unanime title="Yksimielinen?" fmt=boolean/>
  <Column id=prob_vitoria title="Voittaa (%)" fmt=num1 contentType=colorscale/>
  <Column id=rank_p95 title="Huonoin tapaus (p95)" fmt=num0/>
</DataTable>

---

## 🎯 Robustius — itse päätöksen luottamusväli

> **Ongelma.** Painot eivät ole koskaan tarkkoja — ne ovat preferenssiarvioita. Jos kaksi prosenttiyksikköä vaihtaa ykkösen ja kakkosen, ”voittaja” on kalibroinnin artefakti.
>
> **Ratkaisu.** Häiritsemme `w' ~ Dirichlet(κ·w)` ja järjestämme uudelleen **2 000 kertaa**. Dirichlet'n kantaja on täsmälleen simpleksi ja se toteuttaa `E[w'] = w` — häiritsemme **harhauttamatta**.

<BigValue data={robustez_top} value=rotulo title="Johtaja häirityillä painoilla"/>
<BigValue data={robustez_top} value=prob_vitoria title="Voittaa (%)" fmt=num1/>
<BigValue data={robustez_top} value=rank_p95 title="Huonoin uskottava sijoitus" fmt=num0/>

<img src="/mc/{params.caso}/Robustius.png" alt="Robustius sob pesos perturbados" style="width:100%;border-radius:8px;"/>

<DataTable data={robustez_c} rows=15 rowShading=true>
  <Column id=rotulo title="Vaihtoehto"/>
  <Column id=prob_vitoria title="Voittaa konsensuksen (%)" fmt=num1 contentType=colorscale/>
  <Column id=prob_top3 title="Top-3 (%)" fmt=num1/>
  <Column id=rank_medio title="Tyypillinen sija" fmt=num2/>
  <Column id=rank_p05 title="Paras tapaus (p05)" fmt=num0/>
  <Column id=rank_p95 title="Huonoin tapaus (p95)" fmt=num0/>
</DataTable>

### Sijoitusten täysi jakauma

> Kauttaaltaan vihreä palkki on sijoitus, joka **ei riipu painoista**. Laikukas palkki on kiistanalainen sijoitus.

<img src="/mc/{params.caso}/distribuicao_posicoes.png" alt="Distribuição das posições" style="width:100%;border-radius:8px;"/>

---

## 🎲 Matriz BCG — que ITPO de aposta é cada Vaihtoehto

> O consenso responde **qual escolher**. A BCG responde **que tipo de aposta cada uma é** — pergunta diferente, e igualmente decisiva na hora de assinar.
>
> Dois eixos, ambos derivados dos **mesmos pesos do DEMATEL** que alimentam os dez métodos (renormalizados por grupo, de modo que a BCG é um segundo corte da mesma modelagem, não uma segunda modelagem):
>
> - **Houkuttelevuus** (Y) — desempenho ponderado nos Kriteeris de **hyöty** - **Kustannusasema** (X) — quanto entrega por unidade de **sacrifício**
>
> Os cortes são as **medianas** de cada eixo, não o ponto médio: mediana divide o conjunto em duas metades reais, enquanto 0,5 deixaria quadrantes vazios num conjunto assimétrico — e quadrante vazio não informa nada.

<BigValue data={bcg_res_c} value=estrelas title="⭐ Tähdet" fmt=num0/>
<BigValue data={bcg_res_c} value=vacas title="🐄 Lypsylehmät" fmt=num0/>
<BigValue data={bcg_res_c} value=interrogacoes title="❓ Kysymysmerkit" fmt=num0/>
<BigValue data={bcg_res_c} value=abacaxis title="🐕 Koirat" fmt=num0/>

<img src="/mc/{params.caso}/matriz_bcg.png" alt="Matriz BCG" style="width:100%;border-radius:8px;"/>

| Neljännes | Leitura de decisão |
|---|---|
| ⭐ **Estrela** | Alta atratividade **e** boa posição de kustannus — a aposta natural: investir e padronizar. |
| 🐄 **Vaca leiteira** | Entrega o essencial pelo **menor sacrifício**. É a escolha de quem tem orçamento apertado. |
| ❓ **Interrogação** | Desempenho alto a **preço alto**. Só se justifica se o prêmio for necessário. |
| 🐕 **Abacaxi** | Nem entrega, nem é barata. **Descartar.** |

> **O cruzamento é onde mora o achado.** Um 2º colocado que é 🐄 Vaca costuma ser a escolha real de quem tem restrição orçamentária; um 2º colocado ❓ Interrogação só compensa se você precisa do prêmio de desempenho que ele cobra.

<DataTable data={bcg_c} rows=15 rowShading=true>
  <Column id=rank_consenso title="#" contentType=colorscale/>
  <Column id=rotulo title="Vaihtoehto"/>
  <Column id=quadrante_rotulo title="Neljännes"/>
  <Column id=atratividade title="Houkuttelevuus" fmt=num3 contentType=colorscale/>
  <Column id=posicao title="Kustannusasema" fmt=num3 contentType=colorscale/>
  <Column id=acao title="Mitä tehdä"/>
</DataTable>

---

## 📏 DRSA — sääntö, joka selittää menneet päätökset

> Muut yksitoista mallia pyytävät **ilmoitettuja** preferenssejä: painoja, vertailuja, kynnyksiä. **DRSA** (Greco, Matarazzo & Słowiński) kulkee päinvastaiseen suuntaan — se ottaa jo tehdyt päätökset ja palauttaa **säännön**, joka ne selittää, selkokielellä, sellaiselle joka ei tiedä mitä vektorimuotoinen normalisointi on. Se on täällä ainoa perhe, joka oppii historiasta sen sijaan että vaatisi jonkun osaavan ilmaista mitä suosii.

<div class="grid grid-cols-3 gap-4">
<BigValue data={drsa_q} value=gamma title="γ — approksimaation laatu" fmt=pct1/>
<BigValue data={drsa_q} value=n_regras title="Indusoidut säännöt" fmt=num0/>
<BigValue data={drsa_q} value=n_violacoes title="Dominanssia rikkovat parit" fmt=num0/>
</div>

<DataTable data={drsa_r} rows=all rowShading=true>
  <Column id=n_regra title="#"/>
  <Column id=texto title="Sääntö"/>
  <Column id=cobertura title="Kattaa" fmt=num0/>
  <Column id=certeza title="Varmuus" fmt=pct0/>
</DataTable>

> [!NOTE] **γ = 100 %** tarkoittaa, että dominanssirelaatio luokittelee kaikki vaihtoehdot yksiselitteisesti: historia on johdonmukainen ja säännöt kuvaavat sen kokonaan. **γ < 100 %** on diagnoosi eikä vika — se kertoo, että on pareja joissa dominoitua vaihtoehtoa suosittiin, ja sarake *Dominanssia rikkovat parit* laskee montako. Silloin menneessä päätöksessä on poikkeuksia, ja sen tietäminen on arvokkaampaa kuin siisti järjestys.

---

## 📐 Päätösmatriisi

> Os dados de entrada. **Substitua pela sua cotação, seu edital ou seu ensaio** — o motor é o mesmo; os dados é que são seus.

<DataTable data={matriz_c} rows=25 rowShading=true search=true>
  <Column id=alternativa_rotulo title="Vaihtoehto"/>
  <Column id=criterio_rotulo title="Kriteeri"/>
  <Column id=direcao title="Suunta"/>
  <Column id=valor title="Arvo" fmt=num2/>
  <Column id=unidade title="Yksikkö"/>
</DataTable>

<LinkButton url='/fi'>← Voltar ao índice de casos</LinkButton>

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
