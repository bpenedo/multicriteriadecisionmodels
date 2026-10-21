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

🌐 [Português](/casos/{params.caso}) · [English](/en/casos/{params.caso}) · [Español](/es/casos/{params.caso}) · [Français](/fr/casos/{params.caso}) · [Deutsch](/de/casos/{params.caso}) · [中文](/zh/casos/{params.caso}) · **한국어** · [हिन्दी](/hi/casos/{params.caso}) · [עברית](/he/casos/{params.caso}) · [Русский](/ru/casos/{params.caso}) · [Svenska](/sv/casos/{params.caso}) · [Suomi](/fi/casos/{params.caso})

# {caso[0].nome}

> **{caso[0].descricao}**
>
> _모델링된 의사결정자: {caso[0].decisor} · 영역: {caso[0].dominio}_

<BigValue data={caso} value=vencedor_rotulo title="🏆 합의 선정안"/>
<BigValue data={caso} value=prob_vitoria title="승리 비율 (전체 세계 중 %)" fmt=num1/>
<BigValue data={caso} value=classificacao title="판정"/>
<BigValue data={caso} value=n_alternativas title="대안" fmt=num0/>
<BigValue data={caso} value=n_metodos title="순위를 내는 방법" fmt=num0/>
<BigValue data={caso} value=n_modelos title="적용된 모델" fmt=num0/>

---

## 🧮 DEMATEL — 무엇이 원인이고 무엇이 결과인가

> Antes de qualquer peso: **os 기준s não são independentes**. O DEMATEL monta a matriz de relação total `T = X(I−X)⁻¹` — somando influência direta **e indireta** de qualquer comprimento de caminho — e separa o que você pode **puxar** (CAUSA) do que apenas **mede o resultado** (EFEITO). Os pesos saem daí, por influência sistêmica.

<img src="/mc/{params.caso}/dematel_원인_결과.png" alt="Diagrama 원인-결과 DEMATEL" style="width:100%;border-radius:8px;"/>

<DataTable data={dematel_c} rows=all rowShading=true>
  <Column id=rotulo title="기준"/>
  <Column id=unidade title="단위"/>
  <Column id=direcao title="방향"/>
  <Column id=influencia_exercida title="R (행사한 영향)" fmt=num3/>
  <Column id=influencia_recebida title="C (받은 영향)" fmt=num3/>
  <Column id=prominencia title="현저성 (R+C)" fmt=num3 contentType=colorscale/>
  <Column id=relacao title="관계 (R−C)" fmt=num3 contentType=colorscale/>
  <Column id=papel title="역할"/>
  <Column id=peso title="도출 가중치" fmt=pct2/>
</DataTable>

<BarChart data={dematel_c} x=rotulo y=relacao title="DEMATEL 인과 다이어그램 (R−C): 0 위는 원인" yAxisTitle="R − C" sort=false>
  <ReferenceLine y=0 color=info label="fronteira causa / efeito"/>
</BarChart>

### Matriz de relação total — quem influencia quem

> A tabela acima resume cada 기준 em dois números. **Esta matriz mostra as ligações uma a uma**: `T = X(I − X)⁻¹` soma os caminhos diretos **e indiretos** de qualquer comprimento, e por isso revela influências que o especialista nunca declarou diretamente — A influencia B, B influencia C, logo A influencia C, e a matriz total contabiliza isso.
>
> Só aparecem as arestas **acima do limiar α** (a média de T). Abaixo dele, a intensidade é indistinguível de ruído de arredondamento, e um diagrama que desenhasse todas as ligações não informaria nada — toda matriz densa parece igualmente conectada.

<DataTable data={relacao_c} rows=12 rowShading=true>
  <Column id=origem_rotulo title="원천 (영향을 줌)"/>
  <Column id=origem_papel title="원천의 역할"/>
  <Column id=destino_rotulo title="대상 (영향을 받음)"/>
  <Column id=destino_papel title="대상의 역할"/>
  <Column id=intensidade title="강도 tᵢⱼ" fmt=num4 contentType=colorscale/>
</DataTable>

<BarChart data={relacao_c} x=origem_rotulo y=intensidade series=destino_rotulo type=stacked title="각 기준이 행사한 총영향, 대상별 분해" yAxisTitle="Intensidade acumulada" swapXY=true/>

### Quatro famílias de peso sobre o mesmo problema

> O **AHP** pergunta, par a par, quanto um 기준 importa mais que outro. O **DEMATEL** mede influência sistêmica. **Onde divergem está o 결과 de segunda ordem subestimado.**
>
> O **AHP Fuzzy** (Buckley, 1985) recebe o mesmo julgamento do AHP, mas não descarta a imprecisão: quem disse "5" quis dizer algo entre 4 e 6, e essa faixa é carregada até o fim. As colunas `l` e `u` são os limites do número triangular de cada peso.
>
> O **BWM** (Rezaei, 2015) resolve um problema operacional, não teórico: a matriz de Saaty com 9 기준s exige 36 comparações e **ninguém a preenche com atenção até o fim**. O BWM pede apenas o melhor e o pior 기준 e deriva o resto — 2n−3 comparações. A coluna `BWM CR` diz se o julgamento resultante é consistente.

<img src="/mc/{params.caso}/pesos_dematel_ahp.png" alt="DEMATEL, AHP e AHP Fuzzy" style="width:100%;border-radius:8px;"/>

<DataTable data={pesos_c} rows=all rowShading=true>
  <Column id=rotulo title="기준"/>
  <Column id=papel title="역할"/>
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

> [!NOTE] O AHP Fuzzy **achata os extremos** em relação ao AHP crisp: a média geométrica com incerteza puxa os pesos para o centro. Um 기준 que o AHP coloca em 50% costuma cair, e um que ele deixa em 0,4% costuma subir. Isso não é correção de erro, é o que acontece quando se admite que o julgamento tinha uma faixa. Se a ORDEM dos pesos muda entre os dois, a prioridade declarada não sobrevive à imprecisão do próprio decisor, e isso é informação para o comitê.

---

## ⚖️ 같은 문제를 보는 열 개의 의사결정 학파

> [!IMPORTANT] **이 사례에는 열두 개 모델이 적용되었고, 그중 열 개가 이 그래프에 들어갑니다.** **BWM**은 기준 가중치를 돌려주고(위의 네 가지 가중치 계열 표 참조), **DRSA**는 규칙을 돌려줍니다(아래 별도 섹션). 둘 다 대안의 순위를 만들지 않으며, 그래서 **보르다 합의와 견고성 분석은 이 열 개 위에서 계산됩니다**. 여기서 열둘을 모두 세면 합의가 집계하지 않는 것까지 집계한다는 인상을 줍니다.

> 각 방법은 **“더 좋다”가 무엇인지에 대한 서로 다른 이론**입니다. 열 가지가 일치하면 그 선택은 방법의 산물이 아닙니다. **갈릴 때는 그 갈림 자체가 발견**이며, 대개 진짜 트레이드오프가 어디인지를 정확히 가리킵니다.
>
> **퍼지 TOPSIS**(Chen, 2000)는 따로 읽을 가치가 있습니다. 이것은 “잡음을 넣은 AHP-TOPSIS”가 아닙니다. 삼각퍼지수 외에도 정규화(벡터 대신 선형)와 이상해(상대 대신 절대)를 바꿉니다. AHP-TOPSIS 2n과 갈리는 것은 **예상된** 동작이며, 순위가 그 선택들에 얼마나 의존하는지를 재는 척도입니다.

<img src="/mc/{params.caso}/mapa_metodos.png" alt="순위 por escola de decisão" style="width:100%;border-radius:8px;"/>

<BarChart data={metodos_c} x=rotulo y=rank_ series=metodo type=grouped title="의사결정 학파별 순위 (1위 = 최고)" yAxisTitle="Posição" swapXY=true/>

### ELECTRE I — 핵(kernel)

> 순위를 매기기 전에 **걸러내십시오**. 핵은 다른 어떤 대안도 능가하지 못하는 집합입니다. 원소가 하나인 핵은 결정을 끝내고, 지나치게 큰 핵은 기준이 변별하지 못한다는 뜻입니다 — 문제는 계산이 아니라 모델링에 있습니다.

<DataTable data={nucleo_c} rows=12 rowShading=true>
  <Column id=rotulo title="대안"/>
  <Column id=no_nucleo title="핵에 속하는가?" fmt=boolean/>
  <Column id=domina title="우월함" fmt=num0/>
  <Column id=dominada title="에게 우월당함" fmt=num0/>
</DataTable>

### AHP-TOPSIS 2N — 이중 정규화

> TOPSIS는 **선택한 정규화 방식에 민감합니다**. 우리는 두 가지(벡터와 min-max)를 모두 돌리고 그 일치도를 보고합니다. **견고한가?** 열은 방법론적 정직함입니다.

<DataTable data={topsis_c} rows=12 rowShading=true>
  <Column id=rank_final title="#"/>
  <Column id=rotulo title="대안"/>
  <Column id=ci_vector title="Ci 벡터" fmt=num4/>
  <Column id=ci_minmax title="Ci 최소-최대" fmt=num4/>
  <Column id=ci_final title="Ci 최종" fmt=num4 contentType=colorscale/>
  <Column id=concordante title="견고한가?" fmt=boolean/>
</DataTable>

---

## 🤝 보르다 합의

<DataTable data={consenso_c} rows=all rowShading=true>
  <Column id=rank_final title="#" contentType=colorscale/>
  <Column id=rotulo title="대안"/>
  <Column id=borda title="보르다 점수" fmt=num0/>
  <Column id=rank_medio title="평균 순위" fmt=num2/>
  <Column id=unanime title="만장일치?" fmt=boolean/>
  <Column id=prob_vitoria title="승리 비율 (%)" fmt=num1 contentType=colorscale/>
  <Column id=rank_p95 title="최악 (p95)" fmt=num0/>
</DataTable>

---

## 🎯 견고성 — 결정 그 자체의 신뢰구간

> **문제.** 가중치는 결코 정확하지 않습니다 — 선호의 추정치입니다. 2퍼센트포인트가 1위와 2위를 뒤바꾼다면 그 “승자”는 보정의 산물입니다.
>
> **해법.** `w' ~ Dirichlet(κ·w)`로 교란하고 **2,000번** 다시 순위를 매깁니다. 디리클레의 지지집합은 정확히 단체이고 `E[w'] = w`를 만족합니다 — **편향 없이** 교란합니다.

<BigValue data={robustez_top} value=rotulo title="교란된 가중치에서의 선두"/>
<BigValue data={robustez_top} value=prob_vitoria title="승리 비율 (%)" fmt=num1/>
<BigValue data={robustez_top} value=rank_p95 title="가장 나쁜 타당한 순위" fmt=num0/>

<img src="/mc/{params.caso}/견고성.png" alt="견고성 sob pesos perturbados" style="width:100%;border-radius:8px;"/>

<DataTable data={robustez_c} rows=15 rowShading=true>
  <Column id=rotulo title="대안"/>
  <Column id=prob_vitoria title="합의에서 승리 (%)" fmt=num1 contentType=colorscale/>
  <Column id=prob_top3 title="Top-3 (%)" fmt=num1/>
  <Column id=rank_medio title="전형적 순위" fmt=num2/>
  <Column id=rank_p05 title="최선 (p05)" fmt=num0/>
  <Column id=rank_p95 title="최악 (p95)" fmt=num0/>
</DataTable>

### 순위의 전체 분포

> 전부 녹색인 막대는 **가중치에 의존하지 않는** 순위입니다. 얼룩진 막대는 다툼이 있는 순위입니다.

<img src="/mc/{params.caso}/distribuicao_posicoes.png" alt="Distribuição das posições" style="width:100%;border-radius:8px;"/>

---

## 🎲 Matriz BCG — que ITPO de aposta é cada 대안

> O consenso responde **qual escolher**. A BCG responde **que tipo de aposta cada uma é** — pergunta diferente, e igualmente decisiva na hora de assinar.
>
> Dois eixos, ambos derivados dos **mesmos pesos do DEMATEL** que alimentam os dez métodos (renormalizados por grupo, de modo que a BCG é um segundo corte da mesma modelagem, não uma segunda modelagem):
>
> - **매력도** (Y) — desempenho ponderado nos 기준s de **편익** - **비용 위치** (X) — quanto entrega por unidade de **sacrifício**
>
> Os cortes são as **medianas** de cada eixo, não o ponto médio: mediana divide o conjunto em duas metades reais, enquanto 0,5 deixaria quadrantes vazios num conjunto assimétrico — e quadrante vazio não informa nada.

<BigValue data={bcg_res_c} value=estrelas title="⭐ 스타" fmt=num0/>
<BigValue data={bcg_res_c} value=vacas title="🐄 캐시카우" fmt=num0/>
<BigValue data={bcg_res_c} value=interrogacoes title="❓ 물음표" fmt=num0/>
<BigValue data={bcg_res_c} value=abacaxis title="🐕 개" fmt=num0/>

<img src="/mc/{params.caso}/matriz_bcg.png" alt="Matriz BCG" style="width:100%;border-radius:8px;"/>

| 사분면 | Leitura de decisão |
|---|---|
| ⭐ **Estrela** | Alta atratividade **e** boa posição de 비용 — a aposta natural: investir e padronizar. |
| 🐄 **Vaca leiteira** | Entrega o essencial pelo **menor sacrifício**. É a escolha de quem tem orçamento apertado. |
| ❓ **Interrogação** | Desempenho alto a **preço alto**. Só se justifica se o prêmio for necessário. |
| 🐕 **Abacaxi** | Nem entrega, nem é barata. **Descartar.** |

> **O cruzamento é onde mora o achado.** Um 2º colocado que é 🐄 Vaca costuma ser a escolha real de quem tem restrição orçamentária; um 2º colocado ❓ Interrogação só compensa se você precisa do prêmio de desempenho que ele cobra.

<DataTable data={bcg_c} rows=15 rowShading=true>
  <Column id=rank_consenso title="#" contentType=colorscale/>
  <Column id=rotulo title="대안"/>
  <Column id=quadrante_rotulo title="사분면"/>
  <Column id=atratividade title="매력도" fmt=num3 contentType=colorscale/>
  <Column id=posicao title="비용 위치" fmt=num3 contentType=colorscale/>
  <Column id=acao title="무엇을 할 것인가"/>
</DataTable>

---

## 📏 DRSA — 과거의 결정을 설명하는 규칙

> 나머지 열한 모델은 **선언된** 선호를 요구합니다. 가중치, 비교, 임계값 말입니다. **DRSA**(Greco, Matarazzo & Słowiński)는 반대로 갑니다 — 이미 내려진 결정을 받아 그것을 설명하는 **규칙**을, 벡터 정규화가 무엇인지 모르는 사람도 읽을 수 있는 말로 돌려줍니다. 여기서 누군가 자기 선호를 말할 수 있기를 요구하는 대신 이력에서 배우는 유일한 계열입니다.

<div class="grid grid-cols-3 gap-4">
<BigValue data={drsa_q} value=gamma title="γ — 근사의 품질" fmt=pct1/>
<BigValue data={drsa_q} value=n_regras title="귀납된 규칙" fmt=num0/>
<BigValue data={drsa_q} value=n_violacoes title="우월 관계를 위반한 쌍" fmt=num0/>
</div>

<DataTable data={drsa_r} rows=all rowShading=true>
  <Column id=n_regra title="#"/>
  <Column id=texto title="규칙"/>
  <Column id=cobertura title="포괄" fmt=num0/>
  <Column id=certeza title="확실도" fmt=pct0/>
</DataTable>

> [!NOTE] **γ = 100%**는 우월 관계가 모든 대안을 모호함 없이 분류한다는 뜻입니다. 이력이 일관되며 규칙이 그것을 온전히 기술합니다. **γ < 100%**는 결함이 아니라 진단입니다 — 열등한 대안이 선택된 쌍이 존재한다는 뜻이고, *우월 관계를 위반한 쌍* 열이 그 수를 셉니다. 그 경우 과거의 결정에 예외가 있다는 뜻이며, 그것을 아는 편이 깔끔한 순위보다 값집니다.

---

## 📐 의사결정 행렬

> Os dados de entrada. **Substitua pela sua cotação, seu edital ou seu ensaio** — o motor é o mesmo; os dados é que são seus.

<DataTable data={matriz_c} rows=25 rowShading=true search=true>
  <Column id=alternativa_rotulo title="대안"/>
  <Column id=criterio_rotulo title="기준"/>
  <Column id=direcao title="방향"/>
  <Column id=valor title="값" fmt=num2/>
  <Column id=unidade title="단위"/>
</DataTable>

<LinkButton url='/ko'>← Voltar ao índice de casos</LinkButton>

---

<div style="text-align:center;margin-top:2rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="120" style="display:inline-block;opacity:0.9;"/>
  <div style="font-weight:700;margin-top:0.4rem;">ProfBru © 2026</div>
  <div style="margin-top:0.5rem;font-style:italic;font-size:0.9rem;color:#64748b;">
    MCDM Studio — Modelos Multi기준 de Decisão<br/>
    Autor: <strong>ProfBru - Bruno Penedo</strong> © 2026 — 모든 권리 보유<br/>
    profbruanbima@gmail.com
  </div>
</div>
