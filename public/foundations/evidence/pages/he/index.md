---
dir: rtl
title: MCDM Studio — Decisão Multiקריטריון
---

<div style="text-align:center;">

🌐 [Português](/) · [English](/en) · [Español](/es) · [Français](/fr) · [Deutsch](/de) · [中文](/zh) · [한국어](/ko) · [हिन्दी](/hi) · **עברית** · [Русский](/ru) · [Svenska](/sv) · [Suomi](/fi)

<div style="text-align:center;margin:1.2rem 0 1.6rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="200" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.5rem;font-size:1.05rem;">ProfBru © 2026</div>
</div>

_MCDM Studio — Modelos Multiקריטריון de Decisão · Autor: **ProfBru - Bruno Penedo** © 2026 — כל הזכויות שמורות · profbruanbima@gmail.com_

</div>

<!--
  ÍNDICE LEVE, DE PROPÓSITO.
  Só consultas AGREGADAS (uma linha por caso). As tabelas detalhadas — ranking por
  método (3.744 linhas), מטריצת החלטה (3.514), distribuição (4.230), חוסן por
  método (4.160) — vivem nas páginas de caso, onde estão filtradas por `id_caso`.
  Carregá-las todas aqui somava ~16 mil linhas e travava o navegador.
-->

```sql casos
select *, '/casos/' || id_caso as link from mcdm.casos
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

# 🎯 החלטה רב-קריטריונית — עשר אסכולות, פסק אחד עם רווח בר-סמך

> **הגיליון האלקטרוני לא טועה בחשבון. הוא טועה בשאלה.** מיון לפי מחיר בוחר את הזול ביותר. מיון לפי ציון מומחה בוחר את היקר ביותר. סינון לפי "עומד בכל הדרישות" מרוקן בדרך כלל את הרשימה. אף אחת מן השלוש אינה עונה על השאלה שנשאלה: *בין חלופות הסותרות זו את זו, במה לבחור — ובאיזו מידת ביטחון?*

לוח זה מריץ **עשר שיטות רב-קריטריוניות** על כל מקרה, מפיק את המנצח מתוך **קונצנזוס בורדה** ביניהן, ולאחר מכן **מטריד את המשקלים 2,000 פעמים** כדי לענות על השאלה האחת שהוועדה באמת שואלת: *ומה אם היינו נותנים משקל מעט שונה?*

<BigValue data={totais} value=casos title="מקרי החלטה" fmt=num0/>
<BigValue data={totais} value=alternativas title="חלופות שהוערכו" fmt=num0/>
<BigValue data={totais} value=robustos title="פסקים חסינים" fmt=num0/>
<BigValue data={totais} value=frageis title="פסקים שבירים" fmt=num0/>

## 📋 מקרי החלטה

> הקליקו על מקרה כלשהו כדי לפתוח את **הדוח המלא**: תרשים סיבה-תוצאה של DEMATEL, מפת עשר האסכולות, גרעין ה-ELECTRE, הנרמול הכפול של TOPSIS, קונצנזוס בורדה, חוסן על פני 2,000 יקומים, מטריצת BCG ומטריצת ההחלטה.

<DataTable data={casos} rows=all rowShading=true link=link>
  <Column id=nome title="מקרה"/>
  <Column id=dominio title="תחום"/>
  <Column id=n_alternativas title="חלופות" fmt=num0/>
  <Column id=vencedor_rotulo title="🏆 מנצח"/>
  <Column id=prob_vitoria title="ביטחון (%)" fmt=num1 contentType=colorscale/>
  <Column id=classificacao title="פסק"/>
</DataTable>

> **איך קוראים את הפסק.** `חסין` (≥ 90%) = הבחירה אינה תלויה בכיול העדין של המשקלים; אפשר להביאה לוועדה. `סביר` (60–90%) = היא מחזיקה ברוב התרחישים, אבל השני תחרותי. `שביר` (מתחת ל-60%) = **המקום הראשון הוא תוצר של המשקלים** — המערכת אומרת זאת במקום להציג גביע.

<BarChart data={resumo_dominio} x=dominio y=casos title="מקרים לפי תחום יישום" yAxisTitle="Casos"/>

## 🧮 DEMATEL — שורש הסיבה של כל החלטה

> השאלה שכמעט אף אחד אינו שואל לפני שהוא מקצה משקלים: **האם הקריטריונים עצמאיים?** כמעט לעולם לא. צריכת האנרגיה *גורמת* לטווח; השריון *גורם* למשקל, והמשקל *גורם* לאיבוד ניידות. חיבור השניים כעצמאיים מונה את אותו דבר פעמיים.
>
> ה-**DEMATEL** (Gabus ו-Fontela, Battelle) בונה את מטריצת הקשר הכולל `T = X(I−X)⁻¹` — המסכמת השפעות ישירות **ועקיפות** בכל אורך מסלול — ומפרידה: `R+C` = חשיבות במערכת; `R−C > 0` = **סיבה** (מנוף: כאן מתערבים) ו-`R−C < 0` = **תוצאה** (מדחום: תוצר של מה שכבר נעשה).
>
> עמודת **שורש הסיבה** שלהלן היא הקריטריון בעל ה-`R−C` הגבוה ביותר בכל מקרה: שם התערבות אחת מזיזה את המערכת כולה.

<DataTable data={alavancas} rows=all rowShading=true>
  <Column id=nome title="מקרה"/>
  <Column id=n_criterios title="קריטריונים" fmt=num0/>
  <Column id=n_causas title="סיבות" fmt=num0 contentType=colorscale/>
  <Column id=causa_raiz title="🔧 שורש הסיבה (R−C הגבוה ביותר)"/>
  <Column id=criterio_maior_peso title="הקריטריון בעל המשקל הגבוה ביותר"/>
  <Column id=maior_peso_pct title="משקל (%)" fmt=num1/>
</DataTable>

<BarChart data={alavancas} x=nome y={['n_causas','n_criterios']} type=grouped title="קריטריונים שהם סיבה בכל מקרה (מנופים מול הסך)" yAxisTitle="Critérios" swapXY=true/>

> **פתחו מקרה** כדי לראות את תרשים הסיבה-תוצאה המלא, את הטבלה שבה `R` ו-`C` מופרדים, ואת **מטריצת הקשר הכולל** עם הקשרים אחד-אחד.

## 🎲 מטריצת BCG — מפת הזדמנויות לפי קטגוריה

> מעבר ל*במה לבחור*, לכל קטגוריה יש **פרופיל הזדמנות**: כמה מן החלופות הן ⭐ כוכב (להשקיע), 🐄 פרה (לקצור), ❓ סימן שאלה (לשקול את הפרס) ו-🐕 כלב (לזנוח). קטגוריה שכולה סימני שאלה היא שוק יקר; קטגוריה מלאה בפרות היא שוק בוגר, שבו לכסף יש מעט השפעה על ההכרעה.

<DataTable data={bcg_geral} rows=all rowShading=true>
  <Column id=nome title="קטגוריה"/>
  <Column id=estrelas title="⭐" fmt=num0 contentType=colorscale/>
  <Column id=vacas title="🐄" fmt=num0 contentType=colorscale/>
  <Column id=interrogacoes title="❓" fmt=num0 contentType=colorscale/>
  <Column id=abacaxis title="🐕" fmt=num0 contentType=colorscale/>
  <Column id=total title="סך הכול" fmt=num0/>
  <Column id=quadrante_do_vencedor title="הרביע של המקום הראשון"/>
</DataTable>

## ⚖️ עשר אסכולות ההחלטה

> כל שיטה היא **תיאוריה אחרת לשאלה מה פירוש "טוב יותר"**, ולכן אנו מריצים את כולן: כששר אסכולות עצמאיות בוחרות באותו מנצח, הבחירה אינה תוצר של שיטה אחת. כשהן חלוקות, המחלוקת מצביעה על מקומו של חילוף התמורות האמיתי.

| Método | Escola | O que assume | Quando é a ferramenta certa |
|---|---|---|---|
| **AHP-TOPSIS 2n** | Distância à solução ideal | Compensação total entre קריטריוןs | קריטריונים quantitativos, decisor único |
| **ELECTRE I** | דירוג-על | Incomparabilidade é permitida | Triagem: eliminar o que é dominado |
| **ELECTRE II** | דירוג-על | Limiares forte e fraco | Ordenação completa com veto |
| **PROMETHEE II** | דירוג-על | Preferência gradual (6 funções) | Quando "um pouco melhor" não é "melhor" |
| **MAUT** | Utilidade | Independência aditiva + שנאת סיכון | Decisão sob incerteza |
| **MCDA-C** | Construtivista | Níveis Neutro/Bom ancorados | Diagnóstico absoluto, não só ranking |
| **VIKOR** | Compromisso | Utilidade do grupo × arrependimento máximo | Quando compensar é inaceitável |
| **TODIM** | Teoria dos Prospectos | Perda dói mais que ganho equivalente | Decisor avesso a perda (todos são) |
| **SAPEVO-M** | Ordinal multidecisor | Julgamento ordinal de vários decisores | Comitê que não concorda entre si |

## 🎯 חוסן — רווח בר-סמך על ההחלטה עצמה

> **הבעיה.** כל שיטת MCDM מחזירה מנצח בביטחון מובלע של 100%. אבל המשקלים מעולם אינם מדויקים — הם אומדני העדפה. אם שתי נקודות אחוז במשקלו של קריטריון מחליפות בין המקום הראשון לשני, ה"מנצח" הוא תוצר של הכיול ולא עובדה על הקבוצה. אף אחד אינו מדווח על כך. **שם ההחלטות מתות בוועדה.**
>
> **הפתרון.** אנו מטרידים את המשקלים ב-`w' ~ Dirichlet(κ·w)` ומדרגים מחדש 2,000 פעמים. הדיריכלה היא הבחירה הטבעית: תומכה הוא בדיוק הסימפלקס (משקלים חיוביים שסכומם 1) והיא מקיימת `E[w'] = w` — אנו מטרידים **בלי להטות**. עם κ = 200, משקל של 13% נע ב-±2.4 נקודות אחוז.
>
> הפסק חדל להיות *"מודל C הוא הטוב ביותר"* והופך ל**"מודל C מנצח ב-96% מיקומי ההעדפה הסבירים"**.

**פתחו מקרה מן הטבלה שלמעלה** כדי לראות את תרשים הסיבה-תוצאה, את מפת עשר האסכולות, את מטריצת BCG ואת ההתפלגות המלאה של המקומות על פני 2,000 היקומים.

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
