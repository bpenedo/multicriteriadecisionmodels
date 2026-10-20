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
-- Apenas as 10 primeiras do consenso × 9 métodos = 90 linhas. Trazer as 38
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

<div style="text-align:center;margin:1rem 0 1.4rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="150" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.45rem;">ProfBru © 2026</div>
</div>

# {caso[0].nome}

> **{caso[0].descricao}**
>
> _Decisor modelado: {caso[0].decisor} · Domínio: {caso[0].dominio}_

<BigValue data={caso} value=vencedor_rotulo title="🏆 Vencedor do consenso"/>
<BigValue data={caso} value=prob_vitoria title="Vence em (% dos universos)" fmt=num1/>
<BigValue data={caso} value=classificacao title="Veredito"/>
<BigValue data={caso} value=n_alternativas title="Alternativas" fmt=num0/>
<BigValue data={caso} value=n_metodos title="Métodos" fmt=num0/>

---

## 🧮 DEMATEL — quem é causa e quem é efeito

> Antes de qualquer peso: **os critérios não são independentes**. O DEMATEL monta a matriz
> de relação total `T = X(I−X)⁻¹` — somando influência direta **e indireta** de qualquer
> comprimento de caminho — e separa o que você pode **puxar** (CAUSA) do que apenas
> **mede o resultado** (EFEITO). Os pesos saem daí, por influência sistêmica.

<img src="/mc/{params.caso}/dematel_causa_efeito.png" alt="Diagrama causa-efeito DEMATEL" style="width:100%;border-radius:8px;"/>

<DataTable data={dematel_c} rows=all rowShading=true>
  <Column id=rotulo title="Critério"/>
  <Column id=unidade title="Unidade"/>
  <Column id=direcao title="Direção"/>
  <Column id=influencia_exercida title="R (influência exercida)" fmt=num3/>
  <Column id=influencia_recebida title="C (influência recebida)" fmt=num3/>
  <Column id=prominencia title="Proeminência (R+C)" fmt=num3 contentType=colorscale/>
  <Column id=relacao title="Relação (R−C)" fmt=num3 contentType=colorscale/>
  <Column id=papel title="Papel"/>
  <Column id=peso title="Peso derivado" fmt=pct2/>
</DataTable>

<BarChart data={dematel_c} x=rotulo y=relacao title="Diagrama causa–efeito do DEMATEL (R−C): acima de zero = CAUSA" yAxisTitle="R − C" sort=false>
  <ReferenceLine y=0 color=info label="fronteira causa / efeito"/>
</BarChart>

### Matriz de relação total — quem influencia quem

> A tabela acima resume cada critério em dois números. **Esta matriz mostra as ligações
> uma a uma**: `T = X(I − X)⁻¹` soma os caminhos diretos **e indiretos** de qualquer
> comprimento, e por isso revela influências que o especialista nunca declarou
> diretamente — A influencia B, B influencia C, logo A influencia C, e a matriz total
> contabiliza isso.
>
> Só aparecem as arestas **acima do limiar α** (a média de T). Abaixo dele, a intensidade
> é indistinguível de ruído de arredondamento, e um diagrama que desenhasse todas as
> ligações não informaria nada — toda matriz densa parece igualmente conectada.

<DataTable data={relacao_c} rows=12 rowShading=true>
  <Column id=origem_rotulo title="Origem (influencia)"/>
  <Column id=origem_papel title="Papel da origem"/>
  <Column id=destino_rotulo title="Destino (é influenciado)"/>
  <Column id=destino_papel title="Papel do destino"/>
  <Column id=intensidade title="Intensidade tᵢⱼ" fmt=num4 contentType=colorscale/>
</DataTable>

<BarChart data={relacao_c} x=origem_rotulo y=intensidade series=destino_rotulo type=stacked title="Influência total exercida por cada critério, decomposta por destino" yAxisTitle="Intensidade acumulada" swapXY=true/>

### Três famílias de peso sobre o mesmo problema

> O **AHP** pergunta, par a par, quanto um critério importa mais que outro. O **DEMATEL**
> mede influência sistêmica. **Onde divergem está o efeito de segunda ordem subestimado.**
>
> O **AHP Fuzzy** (Buckley, 1985) recebe o mesmo julgamento do AHP, mas não descarta a
> imprecisão: quem disse "5" quis dizer algo entre 4 e 6, e essa faixa é carregada até o
> fim. As colunas `l` e `u` são os limites do número triangular de cada peso.

<img src="/mc/{params.caso}/pesos_dematel_ahp.png" alt="DEMATEL, AHP e AHP Fuzzy" style="width:100%;border-radius:8px;"/>

<DataTable data={pesos_c} rows=all rowShading=true>
  <Column id=rotulo title="Critério"/>
  <Column id=papel title="Papel"/>
  <Column id=peso_dematel title="DEMATEL" fmt=pct2/>
  <Column id=peso_ahp title="AHP" fmt=pct2/>
  <Column id=peso_ahp_fuzzy title="AHP Fuzzy" fmt=pct2/>
  <Column id=fuzzy_l title="l" fmt=pct2/>
  <Column id=fuzzy_u title="u" fmt=pct2/>
  <Column id=divergencia title="DEMATEL - AHP" fmt=pct2 contentType=colorscale/>
  <Column id=cr title="AHP CR" fmt=num4/>
</DataTable>

> [!NOTE]
> O AHP Fuzzy **achata os extremos** em relacao ao AHP crisp: a media geometrica com
> incerteza puxa os pesos para o centro. Um criterio que o AHP coloca em 50% costuma cair,
> e um que ele deixa em 0,4% costuma subir. Isso nao e correcao de erro, e o que acontece
> quando se admite que o julgamento tinha uma faixa. Se a ORDEM dos pesos muda entre os
> dois, a prioridade declarada nao sobrevive a imprecisao do proprio decisor, e isso e
> informacao para o comite.

---

## ⚖️ Dez escolas de decisão sobre o mesmo problema

> Cada método é uma **teoria diferente sobre o que significa "melhor"**. Quando as dez
> concordam, a escolha não é artefato de método. **Quando divergem, a divergência é o achado** —
> e costuma apontar exatamente onde está o trade-off real.
>
> O **TOPSIS Fuzzy** (Chen, 2000) merece leitura à parte: ele não é "o AHP-TOPSIS com ruído".
> Além dos números triangulares, troca a normalização (linear em vez de vetorial) e a solução
> ideal (absoluta em vez de relativa). Divergir do AHP-TOPSIS 2n é o comportamento **esperado**,
> e mede o quanto o ranking depende dessas escolhas.

<img src="/mc/{params.caso}/mapa_metodos.png" alt="Posição por escola de decisão" style="width:100%;border-radius:8px;"/>

<BarChart data={metodos_c} x=rotulo y=rank_ series=metodo type=grouped title="Posição por escola de decisão (1º = melhor)" yAxisTitle="Posição" swapXY=true/>

### ELECTRE I — o núcleo (kernel)

> Antes de ranquear, **elimine**: o núcleo é o conjunto que nenhuma outra alternativa
> sobreclassifica. Núcleo unitário encerra a decisão; núcleo grande demais indica que os
> critérios não estão discriminando — e o problema é de modelagem, não de cálculo.

<DataTable data={nucleo_c} rows=12 rowShading=true>
  <Column id=rotulo title="Alternativa"/>
  <Column id=no_nucleo title="No núcleo?" fmt=boolean/>
  <Column id=domina title="Sobreclassifica" fmt=num0/>
  <Column id=dominada title="É sobreclassificada por" fmt=num0/>
</DataTable>

### AHP-TOPSIS 2N — a dupla normalização

> O TOPSIS é **sensível à normalização escolhida**. Rodamos as duas (vetorial e min-max)
> e reportamos a concordância: a coluna **Robusto?** é honestidade metodológica.

<DataTable data={topsis_c} rows=12 rowShading=true>
  <Column id=rank_final title="#"/>
  <Column id=rotulo title="Alternativa"/>
  <Column id=ci_vector title="Ci vetorial" fmt=num4/>
  <Column id=ci_minmax title="Ci min-max" fmt=num4/>
  <Column id=ci_final title="Ci final" fmt=num4 contentType=colorscale/>
  <Column id=concordante title="Robusto?" fmt=boolean/>
</DataTable>

---

## 🤝 Consenso de Borda

<DataTable data={consenso_c} rows=all rowShading=true>
  <Column id=rank_final title="#" contentType=colorscale/>
  <Column id=rotulo title="Alternativa"/>
  <Column id=borda title="Pontos de Borda" fmt=num0/>
  <Column id=rank_medio title="Posição média" fmt=num2/>
  <Column id=unanime title="Unânime?" fmt=boolean/>
  <Column id=prob_vitoria title="Vence em (%)" fmt=num1 contentType=colorscale/>
  <Column id=rank_p95 title="Pior caso (p95)" fmt=num0/>
</DataTable>

---

## 🎯 Robustez — o intervalo de confiança da própria decisão

> **O problema.** Os pesos nunca são exatos — são estimativas de preferência. Se dois pontos
> percentuais trocam o 1º com o 2º colocado, o "vencedor" é artefato da calibração.
>
> **A solução.** Perturbamos com `w' ~ Dirichlet(κ·w)` e reranqueamos **2.000 vezes**. A
> Dirichlet tem suporte exatamente no simplex e satisfaz `E[w'] = w` — perturbamos **sem enviesar**.

<BigValue data={robustez_top} value=rotulo title="Líder sob pesos perturbados"/>
<BigValue data={robustez_top} value=prob_vitoria title="Vence em (%)" fmt=num1/>
<BigValue data={robustez_top} value=rank_p95 title="Pior posição plausível" fmt=num0/>

<img src="/mc/{params.caso}/robustez.png" alt="Robustez sob pesos perturbados" style="width:100%;border-radius:8px;"/>

<DataTable data={robustez_c} rows=15 rowShading=true>
  <Column id=rotulo title="Alternativa"/>
  <Column id=prob_vitoria title="Vence o consenso (%)" fmt=num1 contentType=colorscale/>
  <Column id=prob_top3 title="Top-3 (%)" fmt=num1/>
  <Column id=rank_medio title="Posição típica" fmt=num2/>
  <Column id=rank_p05 title="Melhor caso (p05)" fmt=num0/>
  <Column id=rank_p95 title="Pior caso (p95)" fmt=num0/>
</DataTable>

### Distribuição completa das posições

> Uma barra inteiramente verde é uma posição que **não depende dos pesos**. Uma barra
> manchada é posição em disputa.

<img src="/mc/{params.caso}/distribuicao_posicoes.png" alt="Distribuição das posições" style="width:100%;border-radius:8px;"/>

---

## 🎲 Matriz BCG — que TIPO de aposta é cada alternativa

> O consenso responde **qual escolher**. A BCG responde **que tipo de aposta cada uma é** —
> pergunta diferente, e igualmente decisiva na hora de assinar.
>
> Dois eixos, ambos derivados dos **mesmos pesos do DEMATEL** que alimentam os nove métodos
> (renormalizados por grupo, de modo que a BCG é um segundo corte da mesma modelagem, não
> uma segunda modelagem):
>
> - **Atratividade** (Y) — desempenho ponderado nos critérios de **benefício**
> - **Posição de custo** (X) — quanto entrega por unidade de **sacrifício**
>
> Os cortes são as **medianas** de cada eixo, não o ponto médio: mediana divide o conjunto
> em duas metades reais, enquanto 0,5 deixaria quadrantes vazios num conjunto assimétrico —
> e quadrante vazio não informa nada.

<BigValue data={bcg_res_c} value=estrelas title="⭐ Estrelas" fmt=num0/>
<BigValue data={bcg_res_c} value=vacas title="🐄 Vacas leiteiras" fmt=num0/>
<BigValue data={bcg_res_c} value=interrogacoes title="❓ Interrogações" fmt=num0/>
<BigValue data={bcg_res_c} value=abacaxis title="🐕 Abacaxis" fmt=num0/>

<img src="/mc/{params.caso}/matriz_bcg.png" alt="Matriz BCG" style="width:100%;border-radius:8px;"/>

| Quadrante | Leitura de decisão |
|---|---|
| ⭐ **Estrela** | Alta atratividade **e** boa posição de custo — a aposta natural: investir e padronizar. |
| 🐄 **Vaca leiteira** | Entrega o essencial pelo **menor sacrifício**. É a escolha de quem tem orçamento apertado. |
| ❓ **Interrogação** | Desempenho alto a **preço alto**. Só se justifica se o prêmio for necessário. |
| 🐕 **Abacaxi** | Nem entrega, nem é barata. **Descartar.** |

> **O cruzamento é onde mora o achado.** Um 2º colocado que é 🐄 Vaca costuma ser a escolha
> real de quem tem restrição orçamentária; um 2º colocado ❓ Interrogação só compensa se você
> precisa do prêmio de desempenho que ele cobra.

<DataTable data={bcg_c} rows=15 rowShading=true>
  <Column id=rank_consenso title="#" contentType=colorscale/>
  <Column id=rotulo title="Alternativa"/>
  <Column id=quadrante_rotulo title="Quadrante"/>
  <Column id=atratividade title="Atratividade" fmt=num3 contentType=colorscale/>
  <Column id=posicao title="Posição de custo" fmt=num3 contentType=colorscale/>
  <Column id=acao title="O que fazer"/>
</DataTable>

---

## 📐 Matriz de decisão

> Os dados de entrada. **Substitua pela sua cotação, seu edital ou seu ensaio** — o motor é
> o mesmo; os dados é que são seus.

<DataTable data={matriz_c} rows=25 rowShading=true search=true>
  <Column id=alternativa_rotulo title="Alternativa"/>
  <Column id=criterio_rotulo title="Critério"/>
  <Column id=direcao title="Direção"/>
  <Column id=valor title="Valor" fmt=num2/>
  <Column id=unidade title="Unidade"/>
</DataTable>

<LinkButton url='/'>← Voltar ao índice de casos</LinkButton>

---

<div style="text-align:center;margin-top:2rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="120" style="display:inline-block;opacity:0.9;"/>
  <div style="font-weight:700;margin-top:0.4rem;">ProfBru © 2026</div>
  <div style="margin-top:0.5rem;font-style:italic;font-size:0.9rem;color:#64748b;">
    MCDM Studio — Modelos Multicritério de Decisão<br/>
    Autor: <strong>ProfBru - Bruno Penedo</strong> © 2026 — TODOS OS DIREITOS RESERVADOS<br/>
    profbruanbima@gmail.com
  </div>
</div>
