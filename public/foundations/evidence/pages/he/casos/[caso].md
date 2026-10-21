---
dir: rtl
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

🌐 [Português](/casos/{params.caso}) · [English](/en/casos/{params.caso}) · [Español](/es/casos/{params.caso}) · [Français](/fr/casos/{params.caso}) · [Deutsch](/de/casos/{params.caso}) · [中文](/zh/casos/{params.caso}) · [한국어](/ko/casos/{params.caso}) · [हिन्दी](/hi/casos/{params.caso}) · **עברית** · [Русский](/ru/casos/{params.caso}) · [Svenska](/sv/casos/{params.caso}) · [Suomi](/fi/casos/{params.caso})

# {caso[0].nome}

> **{caso[0].descricao}**
>
> _מקבל ההחלטות הממודל: {caso[0].decisor} · תחום: {caso[0].dominio}_

<BigValue data={caso} value=vencedor_rotulo title="🏆 המנצח בקונצנזוס"/>
<BigValue data={caso} value=prob_vitoria title="מנצח ב-(% מהיקומים)" fmt=num1/>
<BigValue data={caso} value=classificacao title="פסק"/>
<BigValue data={caso} value=n_alternativas title="חלופות" fmt=num0/>
<BigValue data={caso} value=n_metodos title="שיטות שמדרגות" fmt=num0/>
<BigValue data={caso} value=n_modelos title="מודלים שיושמו" fmt=num0/>

---

## 🧮 DEMATEL — מי סיבה ומי תוצאה

> Antes de qualquer peso: **os קריטריוןs não são independentes**. O DEMATEL monta a matriz de relação total `T = X(I−X)⁻¹` — somando influência direta **e indireta** de qualquer comprimento de caminho — e separa o que você pode **puxar** (CAUSA) do que apenas **mede o resultado** (EFEITO). Os pesos saem daí, por influência sistêmica.

<img src="/mc/{params.caso}/dematel_סיבה_תוצאה.png" alt="Diagrama סיבה-תוצאה DEMATEL" style="width:100%;border-radius:8px;"/>

<DataTable data={dematel_c} rows=all rowShading=true>
  <Column id=rotulo title="קריטריון"/>
  <Column id=unidade title="יחידה"/>
  <Column id=direcao title="כיוון"/>
  <Column id=influencia_exercida title="R (השפעה שהופעלה)" fmt=num3/>
  <Column id=influencia_recebida title="C (השפעה שהתקבלה)" fmt=num3/>
  <Column id=prominencia title="בולטות (R+C)" fmt=num3 contentType=colorscale/>
  <Column id=relacao title="יחס (R−C)" fmt=num3 contentType=colorscale/>
  <Column id=papel title="תפקיד"/>
  <Column id=peso title="משקל נגזר" fmt=pct2/>
</DataTable>

<BarChart data={dematel_c} x=rotulo y=relacao title="תרשים סיבה–תוצאה של DEMATEL (R−C): מעל אפס = סיבה" yAxisTitle="R − C" sort=false>
  <ReferenceLine y=0 color=info label="fronteira causa / efeito"/>
</BarChart>

### Matriz de relação total — quem influencia quem

> A tabela acima resume cada קריטריון em dois números. **Esta matriz mostra as ligações uma a uma**: `T = X(I − X)⁻¹` soma os caminhos diretos **e indiretos** de qualquer comprimento, e por isso revela influências que o especialista nunca declarou diretamente — A influencia B, B influencia C, logo A influencia C, e a matriz total contabiliza isso.
>
> Só aparecem as arestas **acima do limiar α** (a média de T). Abaixo dele, a intensidade é indistinguível de ruído de arredondamento, e um diagrama que desenhasse todas as ligações não informaria nada — toda matriz densa parece igualmente conectada.

<DataTable data={relacao_c} rows=12 rowShading=true>
  <Column id=origem_rotulo title="מקור (משפיע)"/>
  <Column id=origem_papel title="תפקיד המקור"/>
  <Column id=destino_rotulo title="יעד (מושפע)"/>
  <Column id=destino_papel title="תפקיד היעד"/>
  <Column id=intensidade title="עוצמה tᵢⱼ" fmt=num4 contentType=colorscale/>
</DataTable>

<BarChart data={relacao_c} x=origem_rotulo y=intensidade series=destino_rotulo type=stacked title="ההשפעה הכוללת של כל קריטריון, בפילוח לפי יעד" yAxisTitle="Intensidade acumulada" swapXY=true/>

### Quatro famílias de peso sobre o mesmo problema

> O **AHP** pergunta, par a par, quanto um קריטריון importa mais que outro. O **DEMATEL** mede influência sistêmica. **Onde divergem está o תוצאה de segunda ordem subestimado.**
>
> O **AHP Fuzzy** (Buckley, 1985) recebe o mesmo julgamento do AHP, mas não descarta a imprecisão: quem disse "5" quis dizer algo entre 4 e 6, e essa faixa é carregada até o fim. As colunas `l` e `u` são os limites do número triangular de cada peso.
>
> O **BWM** (Rezaei, 2015) resolve um problema operacional, não teórico: a matriz de Saaty com 9 קריטריוןs exige 36 comparações e **ninguém a preenche com atenção até o fim**. O BWM pede apenas o melhor e o pior קריטריון e deriva o resto — 2n−3 comparações. A coluna `BWM CR` diz se o julgamento resultante é consistente.

<img src="/mc/{params.caso}/pesos_dematel_ahp.png" alt="DEMATEL, AHP e AHP Fuzzy" style="width:100%;border-radius:8px;"/>

<DataTable data={pesos_c} rows=all rowShading=true>
  <Column id=rotulo title="קריטריון"/>
  <Column id=papel title="תפקיד"/>
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

> [!NOTE] O AHP Fuzzy **achata os extremos** em relação ao AHP crisp: a média geométrica com incerteza puxa os pesos para o centro. Um קריטריון que o AHP coloca em 50% costuma cair, e um que ele deixa em 0,4% costuma subir. Isso não é correção de erro, é o que acontece quando se admite que o julgamento tinha uma faixa. Se a ORDEM dos pesos muda entre os dois, a prioridade declarada não sobrevive à imprecisão do próprio decisor, e isso é informação para o comitê.

---

## ⚖️ עשר אסכולות החלטה על אותה בעיה

> [!IMPORTANT] **שנים עשר מודלים מיושמים על מקרה זה, ועשרה נכנסים לתרשים הזה.** ה-**BWM** מחזיר משקלי קריטריון (ראו טבלת ארבע המשפחות למעלה) וה-**DRSA** מחזיר כללים (סעיף משלו, בהמשך) — אף אחד מהם אינו מפיק מיקום של חלופה, ולכן **קונצנזוס בורדה וניתוח החוסן מחושבים על פני העשרה האלה**. לספור כאן את כל השנים עשר היה יוצר רושם שהקונצנזוס מצרף את מה שאינו מצרף.

> כל שיטה היא **תיאוריה אחרת לשאלה מה פירוש “טוב יותר”**. כשהעשר מסכימות, הבחירה אינה תוצר של שיטה. **כשהן חלוקות, המחלוקת היא הממצא** — והיא מצביעה בדרך כלל בדיוק על מקומו של חילוף התמורות האמיתי.
>
> ה-**TOPSIS הפאזי** (Chen, 2000) ראוי לקריאה נפרדת: הוא אינו “ה-AHP-TOPSIS עם רעש”. מלבד המספרים המשולשים, הוא מחליף את הנרמול (ליניארי במקום וקטורי) ואת הפתרון האידיאלי (מוחלט במקום יחסי). סטייה מה-AHP-TOPSIS 2n היא ההתנהגות ה**צפויה**, והיא מודדת עד כמה הדירוג תלוי בבחירות הללו.

<img src="/mc/{params.caso}/mapa_metodos.png" alt="מיקום por escola de decisão" style="width:100%;border-radius:8px;"/>

<BarChart data={metodos_c} x=rotulo y=rank_ series=metodo type=grouped title="מיקום לפי אסכולת החלטה (1 = הטוב ביותר)" yAxisTitle="Posição" swapXY=true/>

### ELECTRE I — הגרעין (kernel)

> לפני הדירוג — **סננו**: הגרעין הוא הקבוצה שאף חלופה אחרת אינה מדרגת מעליה. גרעין בן איבר אחד סוגר את ההחלטה; גרעין גדול מדי מלמד שהקריטריונים אינם מבחינים — והבעיה היא בעיית מידול, לא בעיית חישוב.

<DataTable data={nucleo_c} rows=12 rowShading=true>
  <Column id=rotulo title="חלופה"/>
  <Column id=no_nucleo title="בגרעין?" fmt=boolean/>
  <Column id=domina title="מדרג מעל" fmt=num0/>
  <Column id=dominada title="מדורג מתחת ל-" fmt=num0/>
</DataTable>

### AHP-TOPSIS 2N — הנרמול הכפול

> ה-TOPSIS **רגיש לנרמול הנבחר**. אנו מריצים את שניהם (וקטורי ומינימום-מקסימום) ומדווחים על ההתאמה: העמודה **חסין?** היא יושר מתודולוגי.

<DataTable data={topsis_c} rows=12 rowShading=true>
  <Column id=rank_final title="#"/>
  <Column id=rotulo title="חלופה"/>
  <Column id=ci_vector title="Ci וקטורי" fmt=num4/>
  <Column id=ci_minmax title="Ci מינימום-מקסימום" fmt=num4/>
  <Column id=ci_final title="Ci סופי" fmt=num4 contentType=colorscale/>
  <Column id=concordante title="חסין?" fmt=boolean/>
</DataTable>

---

## 🤝 קונצנזוס בורדה

<DataTable data={consenso_c} rows=all rowShading=true>
  <Column id=rank_final title="#" contentType=colorscale/>
  <Column id=rotulo title="חלופה"/>
  <Column id=borda title="נקודות בורדה" fmt=num0/>
  <Column id=rank_medio title="מיקום ממוצע" fmt=num2/>
  <Column id=unanime title="פה אחד?" fmt=boolean/>
  <Column id=prob_vitoria title="מנצח ב-(%)" fmt=num1 contentType=colorscale/>
  <Column id=rank_p95 title="מקרה גרוע (p95)" fmt=num0/>
</DataTable>

---

## 🎯 חוסן — רווח בר-הסמך של ההחלטה עצמה

> **הבעיה.** המשקלים לעולם אינם מדויקים — הם אומדני העדפה. אם שתי נקודות אחוז מחליפות בין המקום הראשון לשני, ה“מנצח” הוא תוצר של הכיול.
>
> **הפתרון.** אנו מטרידים ב-`w' ~ Dirichlet(κ·w)` ומדרגים מחדש **2,000 פעמים**. לדיריכלה תומך בדיוק על הסימפלקס והיא מקיימת `E[w'] = w` — אנו מטרידים **בלי להטות**.

<BigValue data={robustez_top} value=rotulo title="מוביל תחת משקלים מוטרדים"/>
<BigValue data={robustez_top} value=prob_vitoria title="מנצח ב-(%)" fmt=num1/>
<BigValue data={robustez_top} value=rank_p95 title="המיקום הסביר הגרוע ביותר" fmt=num0/>

<img src="/mc/{params.caso}/חוסן.png" alt="חוסן sob pesos perturbados" style="width:100%;border-radius:8px;"/>

<DataTable data={robustez_c} rows=15 rowShading=true>
  <Column id=rotulo title="חלופה"/>
  <Column id=prob_vitoria title="מנצח בקונצנזוס (%)" fmt=num1 contentType=colorscale/>
  <Column id=prob_top3 title="Top-3 (%)" fmt=num1/>
  <Column id=rank_medio title="מיקום טיפוסי" fmt=num2/>
  <Column id=rank_p05 title="מקרה טוב (p05)" fmt=num0/>
  <Column id=rank_p95 title="מקרה גרוע (p95)" fmt=num0/>
</DataTable>

### ההתפלגות המלאה של המיקומים

> עמודה ירוקה לחלוטין היא מיקום ש**אינו תלוי במשקלים**. עמודה מנומרת היא מיקום שנתון במחלוקת.

<img src="/mc/{params.caso}/distribuicao_posicoes.png" alt="Distribuição das posições" style="width:100%;border-radius:8px;"/>

---

## 🎲 Matriz BCG — que מערכות מידעPO de aposta é cada חלופה

> O consenso responde **qual escolher**. A BCG responde **que tipo de aposta cada uma é** — pergunta diferente, e igualmente decisiva na hora de assinar.
>
> Dois eixos, ambos derivados dos **mesmos pesos do DEMATEL** que alimentam os dez métodos (renormalizados por grupo, de modo que a BCG é um segundo corte da mesma modelagem, não uma segunda modelagem):
>
> - **אטרקטיביות** (Y) — desempenho ponderado nos קריטריוןs de **תועלת** - **מיקום עלות** (X) — quanto entrega por unidade de **sacrifício**
>
> Os cortes são as **medianas** de cada eixo, não o ponto médio: mediana divide o conjunto em duas metades reais, enquanto 0,5 deixaria quadrantes vazios num conjunto assimétrico — e quadrante vazio não informa nada.

<BigValue data={bcg_res_c} value=estrelas title="⭐ כוכבים" fmt=num0/>
<BigValue data={bcg_res_c} value=vacas title="🐄 פרות מזומנים" fmt=num0/>
<BigValue data={bcg_res_c} value=interrogacoes title="❓ סימני שאלה" fmt=num0/>
<BigValue data={bcg_res_c} value=abacaxis title="🐕 כלבים" fmt=num0/>

<img src="/mc/{params.caso}/matriz_bcg.png" alt="Matriz BCG" style="width:100%;border-radius:8px;"/>

| רביע | Leitura de decisão |
|---|---|
| ⭐ **Estrela** | Alta atratividade **e** boa posição de עלות — a aposta natural: investir e padronizar. |
| 🐄 **Vaca leiteira** | Entrega o essencial pelo **menor sacrifício**. É a escolha de quem tem orçamento apertado. |
| ❓ **Interrogação** | Desempenho alto a **preço alto**. Só se justifica se o prêmio for necessário. |
| 🐕 **Abacaxi** | Nem entrega, nem é barata. **Descartar.** |

> **O cruzamento é onde mora o achado.** Um 2º colocado que é 🐄 Vaca costuma ser a escolha real de quem tem restrição orçamentária; um 2º colocado ❓ Interrogação só compensa se você precisa do prêmio de desempenho que ele cobra.

<DataTable data={bcg_c} rows=15 rowShading=true>
  <Column id=rank_consenso title="#" contentType=colorscale/>
  <Column id=rotulo title="חלופה"/>
  <Column id=quadrante_rotulo title="רביע"/>
  <Column id=atratividade title="אטרקטיביות" fmt=num3 contentType=colorscale/>
  <Column id=posicao title="מיקום עלות" fmt=num3 contentType=colorscale/>
  <Column id=acao title="מה לעשות"/>
</DataTable>

---

## 📏 DRSA — הכלל שמסביר את החלטות העבר

> אחד עשר המודלים האחרים מבקשים העדפות **מוצהרות**: משקלים, השוואות, ספים. ה-**DRSA** (Greco, Matarazzo ו-Słowiński) הולך בכיוון ההפוך — הוא מקבל החלטות שכבר התקבלו ומחזיר את ה**כלל** שמסביר אותן, בשפה פשוטה, למי שאינו יודע מהו נרמול וקטורי. זו המשפחה היחידה כאן שלומדת מהיסטוריה במקום לדרוש שמישהו יידע להצהיר מה הוא מעדיף.

<div class="grid grid-cols-3 gap-4">
<BigValue data={drsa_q} value=gamma title="γ — איכות הקירוב" fmt=pct1/>
<BigValue data={drsa_q} value=n_regras title="כללים שהוסקו" fmt=num0/>
<BigValue data={drsa_q} value=n_violacoes title="זוגות המפרים את יחס השליטה" fmt=num0/>
</div>

<DataTable data={drsa_r} rows=all rowShading=true>
  <Column id=n_regra title="#"/>
  <Column id=texto title="כלל"/>
  <Column id=cobertura title="מכסה" fmt=num0/>
  <Column id=certeza title="ודאות" fmt=pct0/>
</DataTable>

> [!NOTE] **γ = 100%** פירושו שיחס השליטה מסווג את כל החלופות ללא עמימות: ההיסטוריה עקבית והכללים מתארים אותה במלואה. **γ < 100%** הוא אבחנה ולא פגם — הוא אומר שקיימים זוגות שבהם החלופה הנשלטת הועדפה, והעמודה *זוגות המפרים את יחס השליטה* סופרת כמה. במקרה כזה להחלטת העבר יש חריגים, ולדעת זאת שווה יותר מדירוג נקי.

---

## 📐 מטריצת החלטה

> Os dados de entrada. **Substitua pela sua cotação, seu edital ou seu ensaio** — o motor é o mesmo; os dados é que são seus.

<DataTable data={matriz_c} rows=25 rowShading=true search=true>
  <Column id=alternativa_rotulo title="חלופה"/>
  <Column id=criterio_rotulo title="קריטריון"/>
  <Column id=direcao title="כיוון"/>
  <Column id=valor title="ערך" fmt=num2/>
  <Column id=unidade title="יחידה"/>
</DataTable>

<LinkButton url='/he'>← Voltar ao índice de casos</LinkButton>

---

<div style="text-align:center;margin-top:2rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="120" style="display:inline-block;opacity:0.9;"/>
  <div style="font-weight:700;margin-top:0.4rem;">ProfBru © 2026</div>
  <div style="margin-top:0.5rem;font-style:italic;font-size:0.9rem;color:#64748b;">
    MCDM Studio — Modelos Multiקריטריון de Decisão<br/>
    Autor: <strong>ProfBru - Bruno Penedo</strong> © 2026 — כל הזכויות שמורות<br/>
    profbruanbima@gmail.com
  </div>
</div>
