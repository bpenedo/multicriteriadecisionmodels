---
title: MCDM Studio — Decisão Multiमानदंड
---

<div style="text-align:center;">

🌐 [Português](/) · [English](/en/) · [Español](/es/) · [Français](/fr/) · [Deutsch](/de/) · [中文](/zh/) · [한국어](/ko/) · **हिन्दी** · [עברית](/he/) · [Русский](/ru/) · [Svenska](/sv/) · [Suomi](/fi/)

<div style="text-align:center;margin:1.2rem 0 1.6rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="200" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.5rem;font-size:1.05rem;">ProfBru © 2026</div>
</div>

_MCDM Studio — Modelos Multiमानदंड de Decisão · Autor: **ProfBru - Bruno Penedo** © 2026 — सर्वाधिकार सुरक्षित · profbruanbima@gmail.com_

</div>

<!--
  ÍNDICE LEVE, DE PROPÓSITO.
  Só consultas AGREGADAS (uma linha por caso). As tabelas detalhadas — ranking por
  método (3.744 linhas), निर्णय मैट्रिक्स (3.514), distribuição (4.230), मजबूती por
  método (4.160) — vivem nas páginas de caso, onde estão filtradas por `id_caso`.
  Carregá-las todas aqui somava ~16 mil linhas e travava o navegador.
-->

```sql casos
select *, '/hi/casos/' || id_caso as link from mcdm.casos
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

# 🎯 बहु-मानदंड निर्णय — दस विचारधाराएँ, विश्वास अंतराल के साथ एक निर्णय

> **स्प्रेडशीट गणना में गलती नहीं करती। वह प्रश्न में गलती करती है।** मूल्य से क्रमित करें तो सबसे सस्ता चुना जाता है। विशेषज्ञ अंक से क्रमित करें तो सबसे महँगा। “सभी आवश्यकताएँ पूरी करता है” से छाँटें तो सूची आमतौर पर खाली हो जाती है। तीनों में से कोई भी पूछे गए प्रश्न का उत्तर नहीं देता: *परस्पर विरोधी विकल्पों में से कौन सा चुनें — और कितने विश्वास के साथ?*

यह पटल प्रत्येक प्रकरण पर **दस बहु-मानदंड विधियाँ** चलाता है, उनके बीच की **बोर्डा सहमति** से विजेता निकालता है, और फिर **भारों को 2,000 बार विचलित** करता है, ताकि उस एक प्रश्न का उत्तर दे सके जो समिति वास्तव में पूछती है: *और यदि हमने थोड़ा भिन्न भार दिया होता?*

<BigValue data={totais} value=casos title="निर्णय प्रकरण" fmt=num0/>
<BigValue data={totais} value=alternativas title="मूल्यांकित विकल्प" fmt=num0/>
<BigValue data={totais} value=robustos title="मजबूत निर्णय" fmt=num0/>
<BigValue data={totais} value=frageis title="नाज़ुक निर्णय" fmt=num0/>

## 📋 निर्णय प्रकरण

> किसी भी प्रकरण पर क्लिक करें और **पूर्ण रिपोर्ट** खुलेगी: DEMATEL का कारण-प्रभाव आरेख, दस विचारधाराओं का नक्शा, ELECTRE का कोर, TOPSIS का दोहरा सामान्यीकरण, बोर्डा सहमति, 2,000 ब्रह्मांडों पर मजबूती, BCG आव्यूह और निर्णय आव्यूह।

<DataTable data={casos} rows=all rowShading=true link=link>
  <Column id=nome title="प्रकरण"/>
  <Column id=dominio title="क्षेत्र"/>
  <Column id=n_alternativas title="विकल्प" fmt=num0/>
  <Column id=vencedor_rotulo title="🏆 विजेता"/>
  <Column id=prob_vitoria title="विश्वास (%)" fmt=num1 contentType=colorscale/>
  <Column id=classificacao title="निर्णय"/>
</DataTable>

> **निर्णय कैसे पढ़ें।** `मजबूत` (≥ 90%) = चयन भारों के सूक्ष्म अंशांकन पर निर्भर नहीं है; यह समिति तक जा सकता है। `संभावित` (60–90%) = अधिकांश परिदृश्यों में टिकता है, पर दूसरा स्थान प्रतिस्पर्धी है। `नाज़ुक` (60% से नीचे) = **पहला स्थान भारों की कृति है** — प्रणाली ट्रॉफी दिखाने के बजाय यही कहती है।

<BarChart data={resumo_dominio} x=dominio y=casos title="अनुप्रयोग क्षेत्र के अनुसार प्रकरण" yAxisTitle="Casos"/>

## 🧮 DEMATEL — हर निर्णय का मूल कारण

> भार देने से पहले वह प्रश्न जो लगभग कोई नहीं पूछता: **क्या मानदंड स्वतंत्र हैं?** वे लगभग कभी नहीं होते। ऊर्जा खपत परिसर को *उत्पन्न करती है*; कवच भार को *उत्पन्न करता है*, और भार गतिशीलता की हानि को *उत्पन्न करता है*। दोनों को स्वतंत्र मानकर जोड़ना एक ही बात को दो बार गिनना है।
>
> **DEMATEL** (Gabus और Fontela, Battelle) कुल संबंध आव्यूह `T = X(I−X)⁻¹` बनाता है — जो किसी भी पथ-लंबाई के प्रत्यक्ष **और अप्रत्यक्ष** प्रभावों को जोड़ता है — और पृथक करता है: `R+C` = प्रणाली में महत्त्व; `R−C > 0` = **कारण** (लीवर: यहाँ हस्तक्षेप करें) और `R−C < 0` = **प्रभाव** (थर्मामीटर: जो पहले किया गया उसका परिणाम)।
>
> नीचे का **मूल कारण** स्तंभ प्रत्येक प्रकरण का सर्वाधिक `R−C` वाला मानदंड है: वहीं एक हस्तक्षेप पूरी प्रणाली को हिला देता है।

<DataTable data={alavancas} rows=all rowShading=true>
  <Column id=nome title="प्रकरण"/>
  <Column id=n_criterios title="मानदंड" fmt=num0/>
  <Column id=n_causas title="कारण" fmt=num0 contentType=colorscale/>
  <Column id=causa_raiz title="🔧 मूल कारण (सर्वाधिक R−C)"/>
  <Column id=criterio_maior_peso title="सर्वाधिक भार वाला मानदंड"/>
  <Column id=maior_peso_pct title="भार (%)" fmt=num1/>
</DataTable>

<BarChart data={alavancas} x=nome y={['n_causas','n_criterios']} type=grouped title="प्रत्येक प्रकरण में कारण बनने वाले मानदंड (कुल के सापेक्ष लीवर)" yAxisTitle="Critérios" swapXY=true/>

> **कोई प्रकरण खोलें** और देखें पूरा कारण-प्रभाव आरेख, `R` तथा `C` को अलग दिखाने वाली तालिका, और एक-एक कड़ी के साथ **कुल संबंध आव्यूह**।

## 🎲 BCG आव्यूह — श्रेणी-वार अवसरों का नक्शा

> *कौन सा चुनें* के अलावा, हर श्रेणी का एक **अवसर-प्रोफ़ाइल** होता है: कितने विकल्प ⭐ सितारा (निवेश), 🐄 गाय (फसल काटें), ❓ प्रश्नचिह्न (पुरस्कार आँकें) और 🐕 कुत्ता (छोड़ दें) हैं। केवल प्रश्नचिह्नों वाली श्रेणी एक महँगा बाज़ार है; गायों से भरी श्रेणी एक परिपक्व बाज़ार है, जहाँ पैसा कम निर्णय करता है।

<DataTable data={bcg_geral} rows=all rowShading=true>
  <Column id=nome title="श्रेणी"/>
  <Column id=estrelas title="⭐" fmt=num0 contentType=colorscale/>
  <Column id=vacas title="🐄" fmt=num0 contentType=colorscale/>
  <Column id=interrogacoes title="❓" fmt=num0 contentType=colorscale/>
  <Column id=abacaxis title="🐕" fmt=num0 contentType=colorscale/>
  <Column id=total title="कुल" fmt=num0/>
  <Column id=quadrante_do_vencedor title="प्रथम स्थान का चतुर्थांश"/>
</DataTable>

## ⚖️ निर्णय की दस विचारधाराएँ

> प्रत्येक विधि **इस बात का भिन्न सिद्धांत है कि “बेहतर” का अर्थ क्या है**, और इसीलिए हम सभी चलाते हैं: जब दस स्वतंत्र विचारधाराएँ एक ही विजेता चुनती हैं, तो वह चयन किसी एक विधि की कृति नहीं होता। जब वे भिन्न होती हैं, वह भिन्नता बताती है कि असली समझौता कहाँ है।

| Método | Escola | O que assume | Quando é a ferramenta certa |
|---|---|---|---|
| **AHP-TOPSIS 2n** | Distância à solução ideal | Compensação total entre मानदंडs | मानदंड quantitativos, decisor único |
| **ELECTRE I** | पराभूत करता हैção | Incomparabilidade é permitida | Triagem: eliminar o que é dominado |
| **ELECTRE II** | पराभूत करता हैção | Limiares forte e fraco | Ordenação completa com veto |
| **PROMETHEE II** | पराभूत करता हैção | Preferência gradual (6 funções) | Quando "um pouco melhor" não é "melhor" |
| **MAUT** | Utilidade | Independência aditiva + जोखिम से बचाव | Decisão sob incerteza |
| **MCDA-C** | Construtivista | Níveis Neutro/Bom ancorados | Diagnóstico absoluto, não só ranking |
| **VIKOR** | Compromisso | Utilidade do grupo × arrependimento máximo | Quando compensar é inaceitável |
| **TODIM** | Teoria dos Prospectos | Perda dói mais que ganho equivalente | Decisor avesso a perda (todos são) |
| **SAPEVO-M** | Ordinal multidecisor | Julgamento ordinal de vários decisores | Comitê que não concorda entre si |

## 🎯 मजबूती — स्वयं निर्णय का विश्वास अंतराल

> **समस्या।** प्रत्येक MCDM विधि एक विजेता देती है, जिसका अंतर्निहित विश्वास 100% होता है। पर भार कभी यथार्थ नहीं होते — वे अधिमान के आकलन हैं। यदि किसी मानदंड के भार में दो प्रतिशत अंक पहले और दूसरे स्थान को आपस में बदल देते हैं, तो वह “विजेता” अंशांकन की कृति है, समुच्चय का तथ्य नहीं। इसकी सूचना कोई नहीं देता। **निर्णय समिति में यहीं मरते हैं।**
>
> **समाधान।** हम भारों को `w' ~ Dirichlet(κ·w)` से विचलित करते हैं और 2,000 बार पुनः क्रमित करते हैं। डिरिक्ले स्वाभाविक चुनाव है: उसका आधार ठीक सिम्पलेक्स है (धनात्मक भार जिनका योग 1 है) और वह `E[w'] = w` को संतुष्ट करता है — हम **पूर्वाग्रह के बिना** विचलित करते हैं। κ = 200 पर 13% का भार ±2.4 प्रतिशत अंक झूलता है।
>
> निर्णय अब *“मॉडल C सर्वोत्तम है”* नहीं रहता, बल्कि बनता है **“मॉडल C प्रशंसनीय अधिमान-ब्रह्मांडों के 96% में जीतता है”**।

**ऊपर की तालिका से कोई प्रकरण खोलें** और देखें कारण-प्रभाव आरेख, दस विचारधाराओं का नक्शा, BCG आव्यूह, तथा 2,000 ब्रह्मांडों में स्थानों का पूर्ण वितरण।

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
