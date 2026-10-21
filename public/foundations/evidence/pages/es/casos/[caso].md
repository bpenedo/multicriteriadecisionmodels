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

🌐 [Português](/casos/{params.caso}) · [English](/en/casos/{params.caso}) · **Español** · [Français](/fr/casos/{params.caso}) · [Deutsch](/de/casos/{params.caso}) · [中文](/zh/casos/{params.caso}) · [한국어](/ko/casos/{params.caso}) · [हिन्दी](/hi/casos/{params.caso}) · [עברית](/he/casos/{params.caso}) · [Русский](/ru/casos/{params.caso}) · [Svenska](/sv/casos/{params.caso}) · [Suomi](/fi/casos/{params.caso})

# {caso[0].nome}

> **{caso[0].descricao}**
>
> _Decisor modelado: {caso[0].decisor} · Dominio: {caso[0].dominio}_

<BigValue data={caso} value=vencedor_rotulo title="🏆 Ganador del consenso"/>
<BigValue data={caso} value=prob_vitoria title="Gana en (% de los universos)" fmt=num1/>
<BigValue data={caso} value=classificacao title="Veredicto"/>
<BigValue data={caso} value=n_alternativas title="Alternativas" fmt=num0/>
<BigValue data={caso} value=n_metodos title="Métodos que ordenan" fmt=num0/>
<BigValue data={caso} value=n_modelos title="Modelos aplicados" fmt=num0/>

---

## 🧮 DEMATEL — qué criterios son causa y cuáles efecto

> Antes de qualquer peso: **os Criterios não são independentes**. O DEMATEL monta a matriz de relação total `T = X(I−X)⁻¹` — somando influência direta **e indireta** de qualquer comprimento de caminho — e separa o que você pode **puxar** (CAUSA) do que apenas **mede o resultado** (EFEITO). Os pesos saem daí, por influência sistêmica.

<img src="/mc/{params.caso}/dematel_causa_efecto.png" alt="Diagrama causa-efecto DEMATEL" style="width:100%;border-radius:8px;"/>

<DataTable data={dematel_c} rows=all rowShading=true>
  <Column id=rotulo title="Criterio"/>
  <Column id=unidade title="Unidad"/>
  <Column id=direcao title="Dirección"/>
  <Column id=influencia_exercida title="R (influencia ejercida)" fmt=num3/>
  <Column id=influencia_recebida title="C (influencia recibida)" fmt=num3/>
  <Column id=prominencia title="Prominencia (R+C)" fmt=num3 contentType=colorscale/>
  <Column id=relacao title="Relación (R−C)" fmt=num3 contentType=colorscale/>
  <Column id=papel title="Rol"/>
  <Column id=peso title="Peso derivado" fmt=pct2/>
</DataTable>

<BarChart data={dematel_c} x=rotulo y=relacao title="Diagrama causa–efecto DEMATEL (R−C): por encima de cero = CAUSA" yAxisTitle="R − C" sort=false>
  <ReferenceLine y=0 color=info label="fronteira causa / efeito"/>
</BarChart>

### Matriz de relação total — quem influencia quem

> A tabela acima resume cada Criterio em dois números. **Esta matriz mostra as ligações uma a uma**: `T = X(I − X)⁻¹` soma os caminhos diretos **e indiretos** de qualquer comprimento, e por isso revela influências que o especialista nunca declarou diretamente — A influencia B, B influencia C, logo A influencia C, e a matriz total contabiliza isso.
>
> Só aparecem as arestas **acima do limiar α** (a média de T). Abaixo dele, a intensidade é indistinguível de ruído de arredondamento, e um diagrama que desenhasse todas as ligações não informaria nada — toda matriz densa parece igualmente conectada.

<DataTable data={relacao_c} rows=12 rowShading=true>
  <Column id=origem_rotulo title="Origen (influye)"/>
  <Column id=origem_papel title="Papel del origen"/>
  <Column id=destino_rotulo title="Destino (es influido)"/>
  <Column id=destino_papel title="Papel del destino"/>
  <Column id=intensidade title="Intensidad tᵢⱼ" fmt=num4 contentType=colorscale/>
</DataTable>

<BarChart data={relacao_c} x=origem_rotulo y=intensidade series=destino_rotulo type=stacked title="Influencia total ejercida por cada criterio, desglosada por destino" yAxisTitle="Intensidade acumulada" swapXY=true/>

### Quatro famílias de peso sobre o mesmo problema

> O **AHP** pergunta, par a par, quanto um Criterio importa mais que outro. O **DEMATEL** mede influência sistêmica. **Onde divergem está o efecto de segunda ordem subestimado.**
>
> O **AHP Fuzzy** (Buckley, 1985) recebe o mesmo julgamento do AHP, mas não descarta a imprecisão: quem disse "5" quis dizer algo entre 4 e 6, e essa faixa é carregada até o fim. As colunas `l` e `u` são os limites do número triangular de cada peso.
>
> O **BWM** (Rezaei, 2015) resolve um problema operacional, não teórico: a matriz de Saaty com 9 Criterios exige 36 comparações e **ninguém a preenche com atenção até o fim**. O BWM pede apenas o melhor e o pior Criterio e deriva o resto — 2n−3 comparações. A coluna `BWM CR` diz se o julgamento resultante é consistente.

<img src="/mc/{params.caso}/pesos_dematel_ahp.png" alt="DEMATEL, AHP e AHP Fuzzy" style="width:100%;border-radius:8px;"/>

<DataTable data={pesos_c} rows=all rowShading=true>
  <Column id=rotulo title="Criterio"/>
  <Column id=papel title="Rol"/>
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

> [!NOTE] O AHP Fuzzy **achata os extremos** em relação ao AHP crisp: a média geométrica com incerteza puxa os pesos para o centro. Um Criterio que o AHP coloca em 50% costuma cair, e um que ele deixa em 0,4% costuma subir. Isso não é correção de erro, é o que acontece quando se admite que o julgamento tinha uma faixa. Se a ORDEM dos pesos muda entre os dois, a prioridade declarada não sobrevive à imprecisão do próprio decisor, e isso é informação para o comitê.

---

## ⚖️ Diez escuelas de decisión sobre el mismo problema

> [!IMPORTANT] **Son doce modelos aplicados a este caso, y diez entran en este gráfico.** El **BWM** devuelve pesos de criterio (véase la tabla de las cuatro familias, arriba) y el **DRSA** devuelve reglas (sección propia, más adelante) — ninguno de los dos produce posición de alternativa, y por eso el **consenso de Borda y la robustez se calculan sobre estos diez**. Contar los doce aquí haría parecer que el consenso agrega lo que no agrega.

> Cada método es una **teoría distinta sobre lo que significa «mejor»**. Cuando las diez coinciden, la elección no es artefacto del método. **Cuando divergen, la divergencia es el hallazgo** — y suele señalar exactamente dónde está el trade-off real.
>
> El **TOPSIS Fuzzy** (Chen, 2000) merece lectura aparte: no es «el AHP-TOPSIS con ruido». Además de los números triangulares, cambia la normalización (lineal en vez de vectorial) y la solución ideal (absoluta en vez de relativa). Divergir del AHP-TOPSIS 2n es el comportamiento **esperado**, y mide cuánto depende el ranking de esas elecciones.

<img src="/mc/{params.caso}/mapa_metodos.png" alt="Posición por escola de decisão" style="width:100%;border-radius:8px;"/>

<BarChart data={metodos_c} x=rotulo y=rank_ series=metodo type=grouped title="Posición por escuela de decisión (1º = mejor)" yAxisTitle="Posição" swapXY=true/>

### ELECTRE I — el Núcleo

> Antes de ordenar, **elimine**: el núcleo es el conjunto que ninguna otra alternativa sobreclasifica. Un núcleo unitario cierra la decisión; un núcleo demasiado grande indica que los criterios no están discriminando — y el problema es de modelado, no de cálculo.

<DataTable data={nucleo_c} rows=12 rowShading=true>
  <Column id=rotulo title="Alternativa"/>
  <Column id=no_nucleo title="¿En el núcleo?" fmt=boolean/>
  <Column id=domina title="Sobreclasifica" fmt=num0/>
  <Column id=dominada title="Es sobreclasificada por" fmt=num0/>
</DataTable>

### AHP-TOPSIS 2N — la doble normalización

> El TOPSIS es **sensible a la normalización elegida**. Ejecutamos las dos (vectorial y min-max) y reportamos la concordancia: la columna **¿¿Robusto?** es honestidad metodológica.

<DataTable data={topsis_c} rows=12 rowShading=true>
  <Column id=rank_final title="#"/>
  <Column id=rotulo title="Alternativa"/>
  <Column id=ci_vector title="Ci vectorial" fmt=num4/>
  <Column id=ci_minmax title="Ci mín-máx" fmt=num4/>
  <Column id=ci_final title="Ci final" fmt=num4 contentType=colorscale/>
  <Column id=concordante title="¿Robusto?" fmt=boolean/>
</DataTable>

---

## 🤝 Consenso de Borda

<DataTable data={consenso_c} rows=all rowShading=true>
  <Column id=rank_final title="#" contentType=colorscale/>
  <Column id=rotulo title="Alternativa"/>
  <Column id=borda title="Puntos de Borda" fmt=num0/>
  <Column id=rank_medio title="Posición media" fmt=num2/>
  <Column id=unanime title="¿Unánime?" fmt=boolean/>
  <Column id=prob_vitoria title="Gana en (%)" fmt=num1 contentType=colorscale/>
  <Column id=rank_p95 title="Peor caso (p95)" fmt=num0/>
</DataTable>

---

## 🎯 Robustez — el intervalo de confianza de la propia decisión

> **El problema.** Los pesos nunca son exactos — son estimaciones de preferencia. Si dos puntos porcentuales intercambian el 1.º con el 2.º, el «ganador» es artefacto de la calibración.
>
> **La solución.** Perturbamos con `w' ~ Dirichlet(κ·w)` y reordenamos **2.000 veces**. La Dirichlet tiene soporte exactamente en el simplex y satisface `E[w'] = w` — perturbamos **sin sesgar**.

<BigValue data={robustez_top} value=rotulo title="Líder con pesos perturbados"/>
<BigValue data={robustez_top} value=prob_vitoria title="Gana en (%)" fmt=num1/>
<BigValue data={robustez_top} value=rank_p95 title="Peor posición plausible" fmt=num0/>

<img src="/mc/{params.caso}/robustez.png" alt="Robustez sob pesos perturbados" style="width:100%;border-radius:8px;"/>

<DataTable data={robustez_c} rows=15 rowShading=true>
  <Column id=rotulo title="Alternativa"/>
  <Column id=prob_vitoria title="Gana el consenso (%)" fmt=num1 contentType=colorscale/>
  <Column id=prob_top3 title="Top-3 (%)" fmt=num1/>
  <Column id=rank_medio title="Posición típica" fmt=num2/>
  <Column id=rank_p05 title="Mejor caso (p05)" fmt=num0/>
  <Column id=rank_p95 title="Peor caso (p95)" fmt=num0/>
</DataTable>

### Distribución completa de las posiciones

> Una barra enteramente verde es una posición que **no depende de los pesos**. Una barra manchada es posición en disputa.

<img src="/mc/{params.caso}/distribuicao_posicoes.png" alt="Distribuição das posições" style="width:100%;border-radius:8px;"/>

---

## 🎲 Matriz BCG — que TIPO de aposta é cada alternativa

> O consenso responde **qual escolher**. A BCG responde **que tipo de aposta cada uma é** — pergunta diferente, e igualmente decisiva na hora de assinar.
>
> Dois eixos, ambos derivados dos **mesmos pesos do DEMATEL** que alimentam os dez métodos (renormalizados por grupo, de modo que a BCG é um segundo corte da mesma modelagem, não uma segunda modelagem):
>
> - **Atractivo** (Y) — desempenho ponderado nos Criterios de **beneficio** - **Posición de costo** (X) — quanto entrega por unidade de **sacrifício**
>
> Os cortes são as **medianas** de cada eixo, não o ponto médio: mediana divide o conjunto em duas metades reais, enquanto 0,5 deixaria quadrantes vazios num conjunto assimétrico — e quadrante vazio não informa nada.

<BigValue data={bcg_res_c} value=estrelas title="⭐ Estrellas" fmt=num0/>
<BigValue data={bcg_res_c} value=vacas title="🐄 Vacas lecheras" fmt=num0/>
<BigValue data={bcg_res_c} value=interrogacoes title="❓ Interrogantes" fmt=num0/>
<BigValue data={bcg_res_c} value=abacaxis title="🐕 Perros" fmt=num0/>

<img src="/mc/{params.caso}/matriz_bcg.png" alt="Matriz BCG" style="width:100%;border-radius:8px;"/>

| Cuadrante | Leitura de decisão |
|---|---|
| ⭐ **Estrela** | Alta atratividade **e** boa posição de costo — a aposta natural: investir e padronizar. |
| 🐄 **Vaca leiteira** | Entrega o essencial pelo **menor sacrifício**. É a escolha de quem tem orçamento apertado. |
| ❓ **Interrogação** | Desempenho alto a **preço alto**. Só se justifica se o prêmio for necessário. |
| 🐕 **Abacaxi** | Nem entrega, nem é barata. **Descartar.** |

> **O cruzamento é onde mora o achado.** Um 2º colocado que é 🐄 Vaca costuma ser a escolha real de quem tem restrição orçamentária; um 2º colocado ❓ Interrogação só compensa se você precisa do prêmio de desempenho que ele cobra.

<DataTable data={bcg_c} rows=15 rowShading=true>
  <Column id=rank_consenso title="#" contentType=colorscale/>
  <Column id=rotulo title="Alternativa"/>
  <Column id=quadrante_rotulo title="Cuadrante"/>
  <Column id=atratividade title="Atractivo" fmt=num3 contentType=colorscale/>
  <Column id=posicao title="Posición de costo" fmt=num3 contentType=colorscale/>
  <Column id=acao title="Qué hacer"/>
</DataTable>

---

## 📏 DRSA — la regla que explica las decisiones pasadas

> Los otros once modelos piden preferencias **declaradas**: pesos, comparaciones, umbrales. El **DRSA** (Greco, Matarazzo & Słowiński) hace el camino inverso — recibe las decisiones ya tomadas y devuelve la **regla** que las explica, en lenguaje llano, para quien no sabe qué es una normalización vectorial. Es la única familia aquí que aprende del historial en vez de exigir que alguien sepa declarar lo que prefiere.

<div class="grid grid-cols-3 gap-4">
<BigValue data={drsa_q} value=gamma title="γ — calidad de la aproximación" fmt=pct1/>
<BigValue data={drsa_q} value=n_regras title="Reglas inducidas" fmt=num0/>
<BigValue data={drsa_q} value=n_violacoes title="Pares que violan la dominancia" fmt=num0/>
</div>

<DataTable data={drsa_r} rows=all rowShading=true>
  <Column id=n_regra title="#"/>
  <Column id=texto title="Regla"/>
  <Column id=cobertura title="Cubre" fmt=num0/>
  <Column id=certeza title="Certeza" fmt=pct0/>
</DataTable>

> [!NOTE] **γ = 100%** significa que la relación de dominancia clasifica todas las alternativas sin ambigüedad: el historial es coherente y las reglas lo describen enteramente. **γ < 100%** es diagnóstico, no defecto — dice que existen pares en los que la alternativa dominada fue preferida, y la columna *Pares que violan la dominancia* cuenta cuántos. En ese caso la decisión pasada tiene excepciones, y saberlo vale más que un ranking limpio.

---

## 📐 Matriz de decisión

> Os dados de entrada. **Substitua pela sua cotação, seu edital ou seu ensaio** — o motor é o mesmo; os dados é que são seus.

<DataTable data={matriz_c} rows=25 rowShading=true search=true>
  <Column id=alternativa_rotulo title="Alternativa"/>
  <Column id=criterio_rotulo title="Criterio"/>
  <Column id=direcao title="Dirección"/>
  <Column id=valor title="Valor" fmt=num2/>
  <Column id=unidade title="Unidad"/>
</DataTable>

<LinkButton url='/es'>← Voltar ao índice de casos</LinkButton>

---

<div style="text-align:center;margin-top:2rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="120" style="display:inline-block;opacity:0.9;"/>
  <div style="font-weight:700;margin-top:0.4rem;">ProfBru © 2026</div>
  <div style="margin-top:0.5rem;font-style:italic;font-size:0.9rem;color:#64748b;">
    MCDM Studio — Modelos MultiCriterio de Decisão<br/>
    Autor: <strong>ProfBru - Bruno Penedo</strong> © 2026 — TODOS LOS DERECHOS RESERVADOS<br/>
    profbruanbima@gmail.com
  </div>
</div>
