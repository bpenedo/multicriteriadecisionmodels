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

🌐 [Português](/casos/{params.caso}) · [English](/en/casos/{params.caso}) · [Español](/es/casos/{params.caso}) · [Français](/fr/casos/{params.caso}) · [Deutsch](/de/casos/{params.caso}) · [中文](/zh/casos/{params.caso}) · [한국어](/ko/casos/{params.caso}) · **हिन्दी** · [עברית](/he/casos/{params.caso}) · [Русский](/ru/casos/{params.caso}) · [Svenska](/sv/casos/{params.caso}) · [Suomi](/fi/casos/{params.caso})

# {caso[0].nome}

> **{caso[0].descricao}**
>
> _प्रतिरूपित निर्णयकर्ता: {caso[0].decisor} · क्षेत्र: {caso[0].dominio}_

<BigValue data={caso} value=vencedor_rotulo title="🏆 सहमति का विजेता"/>
<BigValue data={caso} value=prob_vitoria title="जीत (% ब्रह्मांडों में)" fmt=num1/>
<BigValue data={caso} value=classificacao title="निर्णय"/>
<BigValue data={caso} value=n_alternativas title="विकल्प" fmt=num0/>
<BigValue data={caso} value=n_metodos title="क्रम देने वाली विधियाँ" fmt=num0/>
<BigValue data={caso} value=n_modelos title="लागू मॉडल" fmt=num0/>

---

## 🧮 DEMATEL — कौन कारण है और कौन प्रभाव

> Antes de qualquer peso: **os मानदंडs não são independentes**. O DEMATEL monta a matriz de relação total `T = X(I−X)⁻¹` — somando influência direta **e indireta** de qualquer comprimento de caminho — e separa o que você pode **puxar** (CAUSA) do que apenas **mede o resultado** (EFEITO). Os pesos saem daí, por influência sistêmica.

<img src="/mc/{params.caso}/dematel_कारण_प्रभाव.png" alt="Diagrama कारण-प्रभाव DEMATEL" style="width:100%;border-radius:8px;"/>

<DataTable data={dematel_c} rows=all rowShading=true>
  <Column id=rotulo title="मानदंड"/>
  <Column id=unidade title="इकाई"/>
  <Column id=direcao title="दिशा"/>
  <Column id=influencia_exercida title="R (डाला गया प्रभाव)" fmt=num3/>
  <Column id=influencia_recebida title="C (प्राप्त प्रभाव)" fmt=num3/>
  <Column id=prominencia title="प्रमुखता (R+C)" fmt=num3 contentType=colorscale/>
  <Column id=relacao title="संबंध (R−C)" fmt=num3 contentType=colorscale/>
  <Column id=papel title="भूमिका"/>
  <Column id=peso title="व्युत्पन्न भार" fmt=pct2/>
</DataTable>

<BarChart data={dematel_c} x=rotulo y=relacao title="DEMATEL कारण–प्रभाव आरेख (R−C): शून्य के ऊपर = कारण" yAxisTitle="R − C" sort=false>
  <ReferenceLine y=0 color=info label="fronteira causa / efeito"/>
</BarChart>

### Matriz de relação total — quem influencia quem

> A tabela acima resume cada मानदंड em dois números. **Esta matriz mostra as ligações uma a uma**: `T = X(I − X)⁻¹` soma os caminhos diretos **e indiretos** de qualquer comprimento, e por isso revela influências que o especialista nunca declarou diretamente — A influencia B, B influencia C, logo A influencia C, e a matriz total contabiliza isso.
>
> Só aparecem as arestas **acima do limiar α** (a média de T). Abaixo dele, a intensidade é indistinguível de ruído de arredondamento, e um diagrama que desenhasse todas as ligações não informaria nada — toda matriz densa parece igualmente conectada.

<DataTable data={relacao_c} rows=12 rowShading=true>
  <Column id=origem_rotulo title="स्रोत (प्रभाव डालता है)"/>
  <Column id=origem_papel title="स्रोत की भूमिका"/>
  <Column id=destino_rotulo title="गंतव्य (प्रभावित होता है)"/>
  <Column id=destino_papel title="गंतव्य की भूमिका"/>
  <Column id=intensidade title="तीव्रता tᵢⱼ" fmt=num4 contentType=colorscale/>
</DataTable>

<BarChart data={relacao_c} x=origem_rotulo y=intensidade series=destino_rotulo type=stacked title="प्रत्येक मानदंड द्वारा डाला गया कुल प्रभाव, गंतव्य के अनुसार विभाजित" yAxisTitle="Intensidade acumulada" swapXY=true/>

### Quatro famílias de peso sobre o mesmo problema

> O **AHP** pergunta, par a par, quanto um मानदंड importa mais que outro. O **DEMATEL** mede influência sistêmica. **Onde divergem está o प्रभाव de segunda ordem subestimado.**
>
> O **AHP Fuzzy** (Buckley, 1985) recebe o mesmo julgamento do AHP, mas não descarta a imprecisão: quem disse "5" quis dizer algo entre 4 e 6, e essa faixa é carregada até o fim. As colunas `l` e `u` são os limites do número triangular de cada peso.
>
> O **BWM** (Rezaei, 2015) resolve um problema operacional, não teórico: a matriz de Saaty com 9 मानदंडs exige 36 comparações e **ninguém a preenche com atenção até o fim**. O BWM pede apenas o melhor e o pior मानदंड e deriva o resto — 2n−3 comparações. A coluna `BWM CR` diz se o julgamento resultante é consistente.

<img src="/mc/{params.caso}/pesos_dematel_ahp.png" alt="DEMATEL, AHP e AHP Fuzzy" style="width:100%;border-radius:8px;"/>

<DataTable data={pesos_c} rows=all rowShading=true>
  <Column id=rotulo title="मानदंड"/>
  <Column id=papel title="भूमिका"/>
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

> [!NOTE] O AHP Fuzzy **achata os extremos** em relação ao AHP crisp: a média geométrica com incerteza puxa os pesos para o centro. Um मानदंड que o AHP coloca em 50% costuma cair, e um que ele deixa em 0,4% costuma subir. Isso não é correção de erro, é o que acontece quando se admite que o julgamento tinha uma faixa. Se a ORDEM dos pesos muda entre os dois, a prioridade declarada não sobrevive à imprecisão do próprio decisor, e isso é informação para o comitê.

---

## ⚖️ एक ही समस्या पर निर्णय की दस विचारधाराएँ

> [!IMPORTANT] **इस प्रकरण पर बारह मॉडल लागू हैं, और दस इस ग्राफ़ में आते हैं।** **BWM** मानदंड-भार देता है (ऊपर चार भार-परिवारों की तालिका देखें) और **DRSA** नियम देता है (आगे अपना अनुभाग) — दोनों में से कोई विकल्प की स्थिति नहीं बनाता, और इसीलिए **बोर्डा सहमति तथा मजबूती विश्लेषण इन्हीं दस पर गणना किए जाते हैं**। यहाँ बारहों को गिनना यह आभास देगा कि सहमति वह भी जोड़ती है जो वह नहीं जोड़ती।

> प्रत्येक विधि **इस बात का भिन्न सिद्धांत है कि “बेहतर” का अर्थ क्या है**। जब दसों सहमत होती हैं, चयन विधि की कृति नहीं होता। **जब वे भिन्न होती हैं, वह भिन्नता ही खोज है** — और प्रायः ठीक वहीं संकेत करती है जहाँ असली समझौता है।
>
> **फ़ज़ी TOPSIS** (Chen, 2000) अलग से पढ़ने योग्य है: यह “शोर मिलाया हुआ AHP-TOPSIS” नहीं है। त्रिकोणीय संख्याओं के अतिरिक्त यह सामान्यीकरण (सदिश के स्थान पर रैखिक) और आदर्श हल (सापेक्ष के स्थान पर निरपेक्ष) भी बदल देता है। AHP-TOPSIS 2n से भिन्न होना **अपेक्षित** व्यवहार है, और यह मापता है कि क्रम इन चुनावों पर कितना निर्भर है।

<img src="/mc/{params.caso}/mapa_metodos.png" alt="स्थान por escola de decisão" style="width:100%;border-radius:8px;"/>

<BarChart data={metodos_c} x=rotulo y=rank_ series=metodo type=grouped title="निर्णय विचारधारा अनुसार स्थान (1 = सर्वोत्तम)" yAxisTitle="Posição" swapXY=true/>

### ELECTRE I — नाभिक (kernel)

> क्रम देने से पहले **छाँटें**: नाभिक वह समुच्चय है जिसे कोई अन्य विकल्प पराभूत नहीं करता। एकल-अवयव नाभिक निर्णय समाप्त कर देता है; अत्यधिक बड़ा नाभिक बताता है कि मानदंड विभेद नहीं कर रहे — और समस्या प्रतिरूपण की है, गणना की नहीं।

<DataTable data={nucleo_c} rows=12 rowShading=true>
  <Column id=rotulo title="विकल्प"/>
  <Column id=no_nucleo title="नाभिक में?" fmt=boolean/>
  <Column id=domina title="पराभूत करता है" fmt=num0/>
  <Column id=dominada title="इससे पराभूत होता है" fmt=num0/>
</DataTable>

### AHP-TOPSIS 2N — दोहरा सामान्यीकरण

> TOPSIS **चुने गए सामान्यीकरण के प्रति संवेदनशील** है। हम दोनों चलाते हैं (सदिश और मिन-मैक्स) और सहमति बताते हैं: **मजबूत?** स्तंभ पद्धतिगत ईमानदारी है।

<DataTable data={topsis_c} rows=12 rowShading=true>
  <Column id=rank_final title="#"/>
  <Column id=rotulo title="विकल्प"/>
  <Column id=ci_vector title="Ci सदिश" fmt=num4/>
  <Column id=ci_minmax title="Ci मिन-मैक्स" fmt=num4/>
  <Column id=ci_final title="Ci अंतिम" fmt=num4 contentType=colorscale/>
  <Column id=concordante title="मजबूत?" fmt=boolean/>
</DataTable>

---

## 🤝 बोर्डा सर्वसम्मति

<DataTable data={consenso_c} rows=all rowShading=true>
  <Column id=rank_final title="#" contentType=colorscale/>
  <Column id=rotulo title="विकल्प"/>
  <Column id=borda title="बोर्डा अंक" fmt=num0/>
  <Column id=rank_medio title="औसत स्थान" fmt=num2/>
  <Column id=unanime title="सर्वसम्मत?" fmt=boolean/>
  <Column id=prob_vitoria title="जीत (%)" fmt=num1 contentType=colorscale/>
  <Column id=rank_p95 title="निकृष्टतम (p95)" fmt=num0/>
</DataTable>

---

## 🎯 मजबूती — स्वयं निर्णय का विश्वास अंतराल

> **समस्या।** भार कभी यथार्थ नहीं होते — वे अधिमान के आकलन हैं। यदि दो प्रतिशत अंक पहले और दूसरे स्थान को आपस में बदल दें, तो वह “विजेता” अंशांकन की कृति है।
>
> **समाधान।** हम `w' ~ Dirichlet(κ·w)` से विचलित करते हैं और **2,000 बार** पुनः क्रमित करते हैं। डिरिक्ले का आधार ठीक सिम्पलेक्स है और वह `E[w'] = w` को संतुष्ट करता है — हम **पूर्वाग्रह के बिना** विचलित करते हैं।

<BigValue data={robustez_top} value=rotulo title="विचलित भारों पर अग्रणी"/>
<BigValue data={robustez_top} value=prob_vitoria title="जीत (%)" fmt=num1/>
<BigValue data={robustez_top} value=rank_p95 title="सबसे खराब संभावित स्थान" fmt=num0/>

<img src="/mc/{params.caso}/मजबूती.png" alt="मजबूती sob pesos perturbados" style="width:100%;border-radius:8px;"/>

<DataTable data={robustez_c} rows=15 rowShading=true>
  <Column id=rotulo title="विकल्प"/>
  <Column id=prob_vitoria title="सहमति जीतता है (%)" fmt=num1 contentType=colorscale/>
  <Column id=prob_top3 title="Top-3 (%)" fmt=num1/>
  <Column id=rank_medio title="विशिष्ट स्थान" fmt=num2/>
  <Column id=rank_p05 title="सर्वोत्तम (p05)" fmt=num0/>
  <Column id=rank_p95 title="निकृष्टतम (p95)" fmt=num0/>
</DataTable>

### स्थानों का पूर्ण वितरण

> पूरी तरह हरी पट्टी वह स्थान है जो **भारों पर निर्भर नहीं**। चितकबरी पट्टी विवादित स्थान है।

<img src="/mc/{params.caso}/distribuicao_posicoes.png" alt="Distribuição das posições" style="width:100%;border-radius:8px;"/>

---

## 🎲 Matriz BCG — que आईटीPO de aposta é cada विकल्प

> O consenso responde **qual escolher**. A BCG responde **que tipo de aposta cada uma é** — pergunta diferente, e igualmente decisiva na hora de assinar.
>
> Dois eixos, ambos derivados dos **mesmos pesos do DEMATEL** que alimentam os dez métodos (renormalizados por grupo, de modo que a BCG é um segundo corte da mesma modelagem, não uma segunda modelagem):
>
> - **आकर्षण** (Y) — desempenho ponderado nos मानदंडs de **लाभ** - **लागत स्थिति** (X) — quanto entrega por unidade de **sacrifício**
>
> Os cortes são as **medianas** de cada eixo, não o ponto médio: mediana divide o conjunto em duas metades reais, enquanto 0,5 deixaria quadrantes vazios num conjunto assimétrico — e quadrante vazio não informa nada.

<BigValue data={bcg_res_c} value=estrelas title="⭐ सितारे" fmt=num0/>
<BigValue data={bcg_res_c} value=vacas title="🐄 दुधारू गायें" fmt=num0/>
<BigValue data={bcg_res_c} value=interrogacoes title="❓ प्रश्नचिह्न" fmt=num0/>
<BigValue data={bcg_res_c} value=abacaxis title="🐕 कुत्ते" fmt=num0/>

<img src="/mc/{params.caso}/matriz_bcg.png" alt="Matriz BCG" style="width:100%;border-radius:8px;"/>

| चतुर्थांश | Leitura de decisão |
|---|---|
| ⭐ **Estrela** | Alta atratividade **e** boa posição de लागत — a aposta natural: investir e padronizar. |
| 🐄 **Vaca leiteira** | Entrega o essencial pelo **menor sacrifício**. É a escolha de quem tem orçamento apertado. |
| ❓ **Interrogação** | Desempenho alto a **preço alto**. Só se justifica se o prêmio for necessário. |
| 🐕 **Abacaxi** | Nem entrega, nem é barata. **Descartar.** |

> **O cruzamento é onde mora o achado.** Um 2º colocado que é 🐄 Vaca costuma ser a escolha real de quem tem restrição orçamentária; um 2º colocado ❓ Interrogação só compensa se você precisa do prêmio de desempenho que ele cobra.

<DataTable data={bcg_c} rows=15 rowShading=true>
  <Column id=rank_consenso title="#" contentType=colorscale/>
  <Column id=rotulo title="विकल्प"/>
  <Column id=quadrante_rotulo title="चतुर्थांश"/>
  <Column id=atratividade title="आकर्षण" fmt=num3 contentType=colorscale/>
  <Column id=posicao title="लागत स्थिति" fmt=num3 contentType=colorscale/>
  <Column id=acao title="क्या करें"/>
</DataTable>

---

## 📏 DRSA — वह नियम जो पिछले निर्णयों को समझाता है

> शेष ग्यारह मॉडल **घोषित** अधिमान माँगते हैं: भार, तुलनाएँ, देहली। **DRSA** (Greco, Matarazzo और Słowiński) उल्टा रास्ता लेता है — वह पहले से लिए गए निर्णय लेता है और उन्हें समझाने वाला **नियम** लौटाता है, सरल भाषा में, उसके लिए भी जो नहीं जानता कि सदिश सामान्यीकरण क्या है। यहाँ यही एकमात्र परिवार है जो इतिहास से सीखता है, बजाय इसके कि कोई अपनी पसंद घोषित करना जानता हो।

<div class="grid grid-cols-3 gap-4">
<BigValue data={drsa_q} value=gamma title="γ — सन्निकटन की गुणवत्ता" fmt=pct1/>
<BigValue data={drsa_q} value=n_regras title="प्रेरित नियम" fmt=num0/>
<BigValue data={drsa_q} value=n_violacoes title="प्रभुत्व का उल्लंघन करने वाले युग्म" fmt=num0/>
</div>

<DataTable data={drsa_r} rows=all rowShading=true>
  <Column id=n_regra title="#"/>
  <Column id=texto title="नियम"/>
  <Column id=cobertura title="आच्छादन" fmt=num0/>
  <Column id=certeza title="निश्चितता" fmt=pct0/>
</DataTable>

> [!NOTE] **γ = 100%** का अर्थ है कि प्रभुत्व-संबंध सभी विकल्पों को बिना किसी संदिग्धता के वर्गीकृत करता है: इतिहास संगत है और नियम उसे पूरी तरह वर्णित करते हैं। **γ < 100%** दोष नहीं, निदान है — यह बताता है कि ऐसे युग्म हैं जिनमें पराभूत विकल्प को वरीयता मिली, और *प्रभुत्व का उल्लंघन करने वाले युग्म* स्तंभ उनकी संख्या गिनता है। उस स्थिति में पिछले निर्णय में अपवाद हैं, और यह जानना एक साफ़-सुथरे क्रम से अधिक मूल्यवान है।

---

## 📐 निर्णय मैट्रिक्स

> Os dados de entrada. **Substitua pela sua cotação, seu edital ou seu ensaio** — o motor é o mesmo; os dados é que são seus.

<DataTable data={matriz_c} rows=25 rowShading=true search=true>
  <Column id=alternativa_rotulo title="विकल्प"/>
  <Column id=criterio_rotulo title="मानदंड"/>
  <Column id=direcao title="दिशा"/>
  <Column id=valor title="मान" fmt=num2/>
  <Column id=unidade title="इकाई"/>
</DataTable>

<LinkButton url='/hi'>← Voltar ao índice de casos</LinkButton>

---

<div style="text-align:center;margin-top:2rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="120" style="display:inline-block;opacity:0.9;"/>
  <div style="font-weight:700;margin-top:0.4rem;">ProfBru © 2026</div>
  <div style="margin-top:0.5rem;font-style:italic;font-size:0.9rem;color:#64748b;">
    MCDM Studio — Modelos Multiमानदंड de Decisão<br/>
    Autor: <strong>ProfBru - Bruno Penedo</strong> © 2026 — सर्वाधिकार सुरक्षित<br/>
    profbruanbima@gmail.com
  </div>
</div>
