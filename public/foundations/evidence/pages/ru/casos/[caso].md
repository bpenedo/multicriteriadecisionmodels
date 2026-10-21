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

🌐 [Português](/casos/{params.caso}) · [English](/en/casos/{params.caso}) · [Español](/es/casos/{params.caso}) · [Français](/fr/casos/{params.caso}) · [Deutsch](/de/casos/{params.caso}) · [中文](/zh/casos/{params.caso}) · [한국어](/ko/casos/{params.caso}) · [हिन्दी](/hi/casos/{params.caso}) · [עברית](/he/casos/{params.caso}) · **Русский** · [Svenska](/sv/casos/{params.caso}) · [Suomi](/fi/casos/{params.caso})

# {caso[0].nome}

> **{caso[0].descricao}**
>
> _Моделируемый ЛПР: {caso[0].decisor} · Область: {caso[0].dominio}_

<BigValue data={caso} value=vencedor_rotulo title="🏆 Победитель консенсуса"/>
<BigValue data={caso} value=prob_vitoria title="Побеждает в (% вселенных)" fmt=num1/>
<BigValue data={caso} value=classificacao title="Вердикт"/>
<BigValue data={caso} value=n_alternativas title="Альтернативы" fmt=num0/>
<BigValue data={caso} value=n_metodos title="Методы, дающие упорядочение" fmt=num0/>
<BigValue data={caso} value=n_modelos title="Применённые модели" fmt=num0/>

---

## 🧮 DEMATEL — какие критерии причины, а какие следствия

> Antes de qualquer peso: **os Критерийs não são independentes**. O DEMATEL monta a matriz de relação total `T = X(I−X)⁻¹` — somando influência direta **e indireta** de qualquer comprimento de caminho — e separa o que você pode **puxar** (CAUSA) do que apenas **mede o resultado** (EFEITO). Os pesos saem daí, por influência sistêmica.

<img src="/mc/{params.caso}/dematel_причина_следствие.png" alt="Diagrama причина-следствие DEMATEL" style="width:100%;border-radius:8px;"/>

<DataTable data={dematel_c} rows=all rowShading=true>
  <Column id=rotulo title="Критерий"/>
  <Column id=unidade title="Единица"/>
  <Column id=direcao title="Направление"/>
  <Column id=influencia_exercida title="R (оказанное влияние)" fmt=num3/>
  <Column id=influencia_recebida title="C (полученное влияние)" fmt=num3/>
  <Column id=prominencia title="Выраженность (R+C)" fmt=num3 contentType=colorscale/>
  <Column id=relacao title="Отношение (R−C)" fmt=num3 contentType=colorscale/>
  <Column id=papel title="Роль"/>
  <Column id=peso title="Производный вес" fmt=pct2/>
</DataTable>

<BarChart data={dematel_c} x=rotulo y=relacao title="Диаграмма причин-следствий DEMATEL (R−C): выше нуля — ПРИЧИНА" yAxisTitle="R − C" sort=false>
  <ReferenceLine y=0 color=info label="fronteira causa / efeito"/>
</BarChart>

### Matriz de relação total — quem influencia quem

> A tabela acima resume cada Критерий em dois números. **Esta matriz mostra as ligações uma a uma**: `T = X(I − X)⁻¹` soma os caminhos diretos **e indiretos** de qualquer comprimento, e por isso revela influências que o especialista nunca declarou diretamente — A influencia B, B influencia C, logo A influencia C, e a matriz total contabiliza isso.
>
> Só aparecem as arestas **acima do limiar α** (a média de T). Abaixo dele, a intensidade é indistinguível de ruído de arredondamento, e um diagrama que desenhasse todas as ligações não informaria nada — toda matriz densa parece igualmente conectada.

<DataTable data={relacao_c} rows=12 rowShading=true>
  <Column id=origem_rotulo title="Источник (влияет)"/>
  <Column id=origem_papel title="Роль источника"/>
  <Column id=destino_rotulo title="Цель (испытывает влияние)"/>
  <Column id=destino_papel title="Роль цели"/>
  <Column id=intensidade title="Интенсивность tᵢⱼ" fmt=num4 contentType=colorscale/>
</DataTable>

<BarChart data={relacao_c} x=origem_rotulo y=intensidade series=destino_rotulo type=stacked title="Полное влияние каждого критерия в разбивке по цели" yAxisTitle="Intensidade acumulada" swapXY=true/>

### Quatro famílias de peso sobre o mesmo problema

> O **AHP** pergunta, par a par, quanto um Критерий importa mais que outro. O **DEMATEL** mede influência sistêmica. **Onde divergem está o следствие de segunda ordem subestimado.**
>
> O **AHP Fuzzy** (Buckley, 1985) recebe o mesmo julgamento do AHP, mas não descarta a imprecisão: quem disse "5" quis dizer algo entre 4 e 6, e essa faixa é carregada até o fim. As colunas `l` e `u` são os limites do número triangular de cada peso.
>
> O **BWM** (Rezaei, 2015) resolve um problema operacional, não teórico: a matriz de Saaty com 9 Критерийs exige 36 comparações e **ninguém a preenche com atenção até o fim**. O BWM pede apenas o melhor e o pior Критерий e deriva o resto — 2n−3 comparações. A coluna `BWM CR` diz se o julgamento resultante é consistente.

<img src="/mc/{params.caso}/pesos_dematel_ahp.png" alt="DEMATEL, AHP e AHP Fuzzy" style="width:100%;border-radius:8px;"/>

<DataTable data={pesos_c} rows=all rowShading=true>
  <Column id=rotulo title="Критерий"/>
  <Column id=papel title="Роль"/>
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

> [!NOTE] O AHP Fuzzy **achata os extremos** em relação ao AHP crisp: a média geométrica com incerteza puxa os pesos para o centro. Um Критерий que o AHP coloca em 50% costuma cair, e um que ele deixa em 0,4% costuma subir. Isso não é correção de erro, é o que acontece quando se admite que o julgamento tinha uma faixa. Se a ORDEM dos pesos muda entre os dois, a prioridade declarada não sobrevive à imprecisão do próprio decisor, e isso é informação para o comitê.

---

## ⚖️ Десять школ принятия решений по одной и той же задаче

> [!IMPORTANT] **К этому кейсу применены двенадцать моделей, и десять входят в этот график.** **BWM** возвращает веса критериев (см. таблицу четырёх семейств выше), а **DRSA** возвращает правила (отдельный раздел ниже) — ни одна из них не даёт позиции альтернативы, и поэтому **консенсус Борда и анализ робастности считаются по этим десяти**. Считать здесь все двенадцать значило бы внушить, будто консенсус агрегирует то, чего он не агрегирует.

> Каждый метод — это **иная теория о том, что значит «лучше»**. Когда десять совпадают, выбор не является артефактом метода. **Когда они расходятся, расхождение и есть находка** — и оно обычно указывает ровно туда, где лежит настоящий компромисс.
>
> **Нечёткий TOPSIS** (Chen, 2000) заслуживает отдельного чтения: это не «AHP-TOPSIS с шумом». Помимо треугольных чисел он меняет нормализацию (линейная вместо векторной) и идеальное решение (абсолютное вместо относительного). Расхождение с AHP-TOPSIS 2n — **ожидаемое** поведение, и оно измеряет, насколько ранжирование зависит от этих выборов.

<img src="/mc/{params.caso}/mapa_metodos.png" alt="Место por escola de decisão" style="width:100%;border-radius:8px;"/>

<BarChart data={metodos_c} x=rotulo y=rank_ series=metodo type=grouped title="Место по школе принятия решений (1-е — лучшее)" yAxisTitle="Posição" swapXY=true/>

### ELECTRE I — ядро (kernel)

> Прежде чем ранжировать — **отсеките**: ядро есть множество, которое не превосходит ни одна другая альтернатива. Ядро из одного элемента закрывает решение; слишком большое ядро говорит, что критерии не различают — и проблема в моделировании, а не в расчёте.

<DataTable data={nucleo_c} rows=12 rowShading=true>
  <Column id=rotulo title="Альтернатива"/>
  <Column id=no_nucleo title="В ядре?" fmt=boolean/>
  <Column id=domina title="Превосходит" fmt=num0/>
  <Column id=dominada title="Уступает по превосходству" fmt=num0/>
</DataTable>

### AHP-TOPSIS 2N — двойная нормализация

> TOPSIS **чувствителен к выбранной нормализации**. Мы выполняем обе (векторную и минимакс) и сообщаем согласие: столбец **Робастно?** — это методологическая честность.

<DataTable data={topsis_c} rows=12 rowShading=true>
  <Column id=rank_final title="#"/>
  <Column id=rotulo title="Альтернатива"/>
  <Column id=ci_vector title="Ci векторный" fmt=num4/>
  <Column id=ci_minmax title="Ci минимакс" fmt=num4/>
  <Column id=ci_final title="Ci итоговый" fmt=num4 contentType=colorscale/>
  <Column id=concordante title="Робастно?" fmt=boolean/>
</DataTable>

---

## 🤝 Консенсус Борда

<DataTable data={consenso_c} rows=all rowShading=true>
  <Column id=rank_final title="#" contentType=colorscale/>
  <Column id=rotulo title="Альтернатива"/>
  <Column id=borda title="Очки Борда" fmt=num0/>
  <Column id=rank_medio title="Среднее место" fmt=num2/>
  <Column id=unanime title="Единогласно?" fmt=boolean/>
  <Column id=prob_vitoria title="Побеждает в (%)" fmt=num1 contentType=colorscale/>
  <Column id=rank_p95 title="Худший случай (p95)" fmt=num0/>
</DataTable>

---

## 🎯 Робастность — доверительный интервал самого решения

> **Проблема.** Веса никогда не точны — это оценки предпочтений. Если два процентных пункта меняют местами первое и второе место, «победитель» — артефакт калибровки.
>
> **Решение.** Мы возмущаем как `w' ~ Dirichlet(κ·w)` и переранжируем **2 000 раз**. Носитель Дирихле — в точности симплекс, и она удовлетворяет `E[w'] = w` — мы возмущаем **без смещения**.

<BigValue data={robustez_top} value=rotulo title="Лидер при возмущённых весах"/>
<BigValue data={robustez_top} value=prob_vitoria title="Побеждает в (%)" fmt=num1/>
<BigValue data={robustez_top} value=rank_p95 title="Худшая правдоподобная позиция" fmt=num0/>

<img src="/mc/{params.caso}/Робастность.png" alt="Робастность sob pesos perturbados" style="width:100%;border-radius:8px;"/>

<DataTable data={robustez_c} rows=15 rowShading=true>
  <Column id=rotulo title="Альтернатива"/>
  <Column id=prob_vitoria title="Побеждает в консенсусе (%)" fmt=num1 contentType=colorscale/>
  <Column id=prob_top3 title="Top-3 (%)" fmt=num1/>
  <Column id=rank_medio title="Типичное место" fmt=num2/>
  <Column id=rank_p05 title="Лучший случай (p05)" fmt=num0/>
  <Column id=rank_p95 title="Худший случай (p95)" fmt=num0/>
</DataTable>

### Полное распределение мест

> Сплошь зелёная полоса — место, которое **не зависит от весов**. Пёстрая полоса — место, за которое идёт спор.

<img src="/mc/{params.caso}/distribuicao_posicoes.png" alt="Distribuição das posições" style="width:100%;border-radius:8px;"/>

---

## 🎲 Matriz BCG — que ИТPO de aposta é cada Альтернатива

> O consenso responde **qual escolher**. A BCG responde **que tipo de aposta cada uma é** — pergunta diferente, e igualmente decisiva na hora de assinar.
>
> Dois eixos, ambos derivados dos **mesmos pesos do DEMATEL** que alimentam os dez métodos (renormalizados por grupo, de modo que a BCG é um segundo corte da mesma modelagem, não uma segunda modelagem):
>
> - **Привлекательность** (Y) — desempenho ponderado nos Критерийs de **выгода** - **Позиция по стоимости** (X) — quanto entrega por unidade de **sacrifício**
>
> Os cortes são as **medianas** de cada eixo, não o ponto médio: mediana divide o conjunto em duas metades reais, enquanto 0,5 deixaria quadrantes vazios num conjunto assimétrico — e quadrante vazio não informa nada.

<BigValue data={bcg_res_c} value=estrelas title="⭐ Звёзды" fmt=num0/>
<BigValue data={bcg_res_c} value=vacas title="🐄 Дойные коровы" fmt=num0/>
<BigValue data={bcg_res_c} value=interrogacoes title="❓ Знаки вопроса" fmt=num0/>
<BigValue data={bcg_res_c} value=abacaxis title="🐕 Собаки" fmt=num0/>

<img src="/mc/{params.caso}/matriz_bcg.png" alt="Matriz BCG" style="width:100%;border-radius:8px;"/>

| Квадрант | Leitura de decisão |
|---|---|
| ⭐ **Estrela** | Alta atratividade **e** boa posição de затраты — a aposta natural: investir e padronizar. |
| 🐄 **Vaca leiteira** | Entrega o essencial pelo **menor sacrifício**. É a escolha de quem tem orçamento apertado. |
| ❓ **Interrogação** | Desempenho alto a **preço alto**. Só se justifica se o prêmio for necessário. |
| 🐕 **Abacaxi** | Nem entrega, nem é barata. **Descartar.** |

> **O cruzamento é onde mora o achado.** Um 2º colocado que é 🐄 Vaca costuma ser a escolha real de quem tem restrição orçamentária; um 2º colocado ❓ Interrogação só compensa se você precisa do prêmio de desempenho que ele cobra.

<DataTable data={bcg_c} rows=15 rowShading=true>
  <Column id=rank_consenso title="#" contentType=colorscale/>
  <Column id=rotulo title="Альтернатива"/>
  <Column id=quadrante_rotulo title="Квадрант"/>
  <Column id=atratividade title="Привлекательность" fmt=num3 contentType=colorscale/>
  <Column id=posicao title="Позиция по стоимости" fmt=num3 contentType=colorscale/>
  <Column id=acao title="Что делать"/>
</DataTable>

---

## 📏 DRSA — правило, объясняющее прошлые решения

> Остальные одиннадцать моделей требуют **объявленных** предпочтений: весов, сравнений, порогов. **DRSA** (Greco, Matarazzo и Słowiński) идёт обратным путём — он берёт уже принятые решения и возвращает **правило**, которое их объясняет, обычными словами, для того, кто не знает, что такое векторная нормализация. Это единственное здесь семейство, которое учится на истории вместо того, чтобы требовать от кого-то умения объявить свои предпочтения.

<div class="grid grid-cols-3 gap-4">
<BigValue data={drsa_q} value=gamma title="γ — качество аппроксимации" fmt=pct1/>
<BigValue data={drsa_q} value=n_regras title="Выведенные правила" fmt=num0/>
<BigValue data={drsa_q} value=n_violacoes title="Пары, нарушающие доминирование" fmt=num0/>
</div>

<DataTable data={drsa_r} rows=all rowShading=true>
  <Column id=n_regra title="#"/>
  <Column id=texto title="Правило"/>
  <Column id=cobertura title="Покрывает" fmt=num0/>
  <Column id=certeza title="Достоверность" fmt=pct0/>
</DataTable>

> [!NOTE] **γ = 100%** означает, что отношение доминирования классифицирует все альтернативы без неоднозначности: история согласованна, и правила описывают её целиком. **γ < 100%** — это диагноз, а не дефект: он говорит, что есть пары, в которых предпочли доминируемую альтернативу, а столбец *Пары, нарушающие доминирование* считает, сколько их. В таком случае у прошлого решения есть исключения, и знать об этом ценнее, чем иметь чистое ранжирование.

---

## 📐 Матрица решений

> Os dados de entrada. **Substitua pela sua cotação, seu edital ou seu ensaio** — o motor é o mesmo; os dados é que são seus.

<DataTable data={matriz_c} rows=25 rowShading=true search=true>
  <Column id=alternativa_rotulo title="Альтернатива"/>
  <Column id=criterio_rotulo title="Критерий"/>
  <Column id=direcao title="Направление"/>
  <Column id=valor title="Значение" fmt=num2/>
  <Column id=unidade title="Единица"/>
</DataTable>

<LinkButton url='/ru'>← Voltar ao índice de casos</LinkButton>

---

<div style="text-align:center;margin-top:2rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="120" style="display:inline-block;opacity:0.9;"/>
  <div style="font-weight:700;margin-top:0.4rem;">ProfBru © 2026</div>
  <div style="margin-top:0.5rem;font-style:italic;font-size:0.9rem;color:#64748b;">
    MCDM Studio — Modelos MultiКритерий de Decisão<br/>
    Autor: <strong>ProfBru - Bruno Penedo</strong> © 2026 — ВСЕ ПРАВА ЗАЩИЩЕНЫ<br/>
    profbruanbima@gmail.com
  </div>
</div>
