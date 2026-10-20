<!--
MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
-->

<div align="center">

# 🎯 MCDM Studio — מודלים רב-קריטריוניים לקבלת החלטות

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="820"/>

**ProfBru © 2026**

### הפסיקו לבחור עם גיליון אלקטרוני. התחילו להחליט עם הוכחה.

**עשר אסכולות החלטה. מנצח אחד. ולראשונה — ההסתברות שהמנצח הזה נכון.**

[![MCDM](https://img.shields.io/badge/שיטות_MCDM-10-2563eb?style=for-the-badge)](#-תשע-אסכולות-ההחלטה--ולמה-תשע)
[![Engines](https://img.shields.io/badge/מנועים-Python_+_Rust-c2410c?style=for-the-badge)](#-שני-מנועים-עצמאיים-הבדיקה-הצולבת)
[![i18n](https://img.shields.io/badge/שפות-12-16a34a?style=for-the-badge)](#-12-שפות--זיכרון-תרגום-sdl-trados)
[![Robustez](https://img.shields.io/badge/יקומים_מדומים-2.000-8f3d56?style=for-the-badge)](#-השאלה-שאיש-אינו-עונה-עליה-ומה-אם-המשקלים-שגויים)

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Rust](https://img.shields.io/badge/Rust-1.96-000000?logo=rust&logoColor=white)](https://www.rust-lang.org)
[![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?logo=numpy&logoColor=white)](https://numpy.org)
[![Numba](https://img.shields.io/badge/Numba-JIT-00A3E0?logo=numba&logoColor=white)](https://numba.pydata.org)
[![Evidence](https://img.shields.io/badge/Evidence.dev-Dashboard-f4b548)](https://evidence.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/רישיון-קנייני-red)](#-רישיון-ובעלות)

🌐 [Português](README.md) · [English](README.en.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [中文](README.zh.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · **עברית** · [Русский](README.ru.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md)

</div>

---

## 💀 הכאב: כבר הפסדתם כסף בגלל גיליון אלקטרוני

חשבו על ההחלטה היקרה האחרונה שקיבלתם. לקנות את הרכב. לבחור את הספק. לאשר את הפרויקט. לקבוע את המחשב הנייד ש-200 אנשים ישתמשו בו ארבע שנים.

**פתחתם גיליון אלקטרוני. האפשרויות בשורות, המאפיינים בעמודות. ואז עשיתם אחד משלושה דברים:**

| מה עשיתם | מה באמת קרה |
|---|---|
| 🔻 **מיינתם לפי עמודת המחיר** | בחרתם את הזול ביותר. לשם כך לא הייתם צריכים גיליון אלקטרוני. |
| 🔺 **מיינתם לפי ציון המומחה** | בחרתם את היקר ביותר. גם לשם כך לא הייתם צריכים. |
| 🔍 **סיננתם לפי «עומד בכל הדרישות»** | הרשימה התרוקנה. אז ריככתם דרישה אחת. איזו? **זו שהפריעה.** |

> [!WARNING]
> **לשלוש הפעולות אותו פגם: אף אחת מהן אינה עונה על השאלה ששאלתם.**
> השאלה הייתה *«בין אפשרויות הסותרות זו את זו, במה לבחור?»* — ומיון לפי עמודה הוא, בהגדרה, הכרעה לפי קריטריון **אחד**. את שבעת האחרים לא ניצלתם. הם היו שם רק כדי שתרגישו טוב יותר.

ויש הבעיה שאיש אינו רואה: **חיברתם דברים שכבר חוברו.** נתתם 20% ל«צריכת אנרגיה» ו-25% ל«טווח נסיעה» — אבל הצריכה *גורמת* לטווח. ספרתם את אותו הדבר פעמיים וקראתם לזה ניתוח.

### הרגע שבו ההחלטה מתה

זה קורה בישיבה. אתם מציגים את הדירוג. מישהו בוועדה שואל:

> *ומה אם הטווח היה שווה 30% במקום 25%?*

ואתם לא יודעים. **אף אחד לא יודע.** כי הגיליון מחזיר מספר **אחד**, עם ביטחון מובלע של 100% שאין לו שום דרך להחזיק בו. אתם חוזרים אחרי שיעורי בית, משנים את המשקלים, ומגלים שהמקום השני הופך לראשון בהפרש של **שתי נקודות אחוז**.

אותו «מנצח» מעולם לא היה מנצח. הוא היה **תוצר של הכיול שלכם** — וכמעט חתמתם עליו.

---

## 💊 הפתרון: עשר אסכולות, קונצנזוס אחד, ורווח בר-סמך

**MCDM Studio מריץ **עשר שיטות רב-קריטריוניות מבוססות** על אותה בעיה, מפיק את המנצח מתוך ה**קונצנזוס** ביניהן, ואז עושה את הדבר היחיד שבאמת חשוב:**

> ### 🎲 הוא מפריע למשקלים **2,000 פעמים** וסופר בכמה יקומים המנצח ממשיך לנצח.

הפסק חדל להיות מספר והופך ל**משפט ששורד את הוועדה**:

<div align="center">

| ❌ מה אומר הגיליון | ✅ מה אומר MCDM Studio |
|---|---|
| «דגם C הוא הטוב ביותר.» | **«דגם C מנצח ב-96% מיקומי ההעדפות הסבירים. פסק חסין: הבחירה אינה תלויה בכיול עדין של המשקלים.»** |
| *(אין תשובה)* | **«דגם A מנצח ב-51%. פסק שביר: המקום הראשון הוא תוצר של המשקלים. אל תחליטו לפי הדירוג בלבד.»** |

</div>

**שימו לב למקרה השני. מערכת ישרה חייבת להיות מסוגלת לומר *«אל תסמכו עליי כאן»*. זה ההבדל בין תמיכה בקבלת החלטות לבין מחולל הצדקות להחלטה שכבר רציתם לקבל.**

---

## 🖼️ ראו את זה עובד

### 1. מי סיבה ומי תוצאה — לפני כל משקל

<div align="center"><img src="docs/telas/caca_multifuncao/dematel_causa_efeito.png" alt="DEMATEL" width="820"/></div>

**הכאב שזה פותר:** אתם מקצים משקלים בהנחה שהקריטריונים עצמאיים. **הם כמעט לעולם אינם.** צריכת אנרגיה *גורמת* לטווח. שריון *גורם* למשקל, שגורם לאובדן ניידות. לחבר אותם כעצמאיים זו ספירה כפולה.

**DEMATEL** בונה את מטריצת היחס הכולל `T = X(I−X)⁻¹` — המסכמת השפעות ישירות **ועקיפות** בכל אורך מסלול — ומפרידה בין מה שאפשר **למשוך** (סיבות, מעל הקו) לבין מה שרק **מודד תוצאה** (תוצאות, מתחת). המשקלים נגזרים משם: מהשפעה מערכתית, לא מניחוש.

> במקרה שלמעלה, **העברת טכנולוגיה** ו**חתימת מכ"ם** הן סיבות: הזזתן מזיזה את המערכת כולה. **זמינות הצי** היא תוצאה — מדחום, לא מנוף. מכרז המנקד זמינות ומתעלם מהעברת טכנולוגיה מודד חום ומתעלם מהזיהום.

### 2. עשר אסכולות על אותה בעיה

<div align="center"><img src="docs/telas/veiculo_eletrico/mapa_metodos.png" alt="Métodos" width="900"/></div>

**הכאב שזה פותר:** בכל שיטת MCDM מוטמעת תיאוריה על משמעות המילה «טוב יותר» — והיא משנה את המנצח. לבחור שיטה ולהציג את התוצאה זה לבחור את התוצאה.

אנחנו מריצים את כל העשר. כשהן מסכימות, הבחירה **אינה תוצר של שיטה**. כשהן חלוקות, **המחלוקת היא הממצא**.

> למעלה: ה**היברידי הנטען** ראשון בשבע שיטות, אך **שישי ב-ELECTRE I**. זה לא רעש — זו אינפורמציה. ELECTRE I מתיר *וטו*: הוא אומר שלהיברידי יש חיסרון חמור דיו באחד הקריטריונים כדי להיפסל, טוב ככל שיהיה בשאר. **זו בדיוק השאלה שתרצו להביא לוועדה.**

### 3. רווח בר-סמך על ההחלטה עצמה

<div align="center"><img src="docs/telas/portfolio_startup/robustez.png" alt="Robustez" width="820"/></div>

**הכאב שזה פותר:** שאלת הוועדה — *«ומה אם המשקל היה אחר?»*. נענית **לפני** שמישהו שואל.

אנו מפריעים למשקלים באמצעות `w' ~ Dirichlet(κ·w)` ומדרגים מחדש 2,000 פעמים. דיריכלה היא הבחירה הטבעית: התומך שלה הוא בדיוק הסימפלקס (משקלים חיוביים שסכומם 1) והיא מקיימת `E[w'] = w` — כלומר מפריעים **בלי להטות**.

### 4. היכן האינטואיציה שלכם טועה

<div align="center"><img src="docs/telas/blindado/pesos_dematel_ahp.png" alt="DEMATEL x AHP" width="820"/></div>

**הכאב שזה פותר:** אתם חושבים שאתם יודעים מה חשוב. שתי משפחות משקלים בוחנות זאת.

**AHP** (Saaty) שואל בהשוואות זוגיות כמה קריטריון אחד חשוב יותר מאחר. **DEMATEL** מודד השפעה מערכתית. **היכן שהם נחלקים נמצא אפקט הסדר השני שהמעטתם בערכו** — והתרשים מסמן באדום את הפער הגדול ביותר.

### 5. היכן כל חלופה מסיימת, על פני 2,000 תרחישים

<div align="center"><img src="docs/telas/estacao_trabalho/distribuicao_posicoes.png" alt="Distribuição" width="820"/></div>

עמודה ירוקה לחלוטין היא מיקום ש**אינו תלוי במשקלים**. עמודה מנומרת היא מיקום שנוי במחלוקת. במבט אחד רואים היכן הדירוג הוא עובדה והיכן הוא דעה.

---

## 🎯 למה זה משמש — הבחירה המותאמת

המנוע **אגנוסטי לתחום**: היחידה היא *מקרה ההחלטה* (חלופות × קריטריונים), ללא סמנטיקה עסקית מוטמעת. החלפת תחום היא החלפת נתונים, לא קוד.

<div align="center">

| תחום | ההחלטה | הכאב הספציפי |
|---|---|---|
| 📱 **אלקטרוניקה** | טלפון, מחשב נייד, ציוד | לזול ביותר יש המצלמה הגרועה ביותר; לבעל המצלמה הטובה ביותר יש הסוללה הגרועה ביותר. אין «הטוב ביותר» — יש **הטוב ביותר לשימוש שלכם**. |
| 🚗 **רכבים חשמליים** | צי או שימוש אישי | טווח, טעינה, רשת שירות וערך מכירה מושכים לכיוונים מנוגדים. והקריטריון המכריע (**טווח אמיתי**, לא זה שבקטלוג) הוא הקשה ביותר למדידה. |
| 🎖️ **ביטחון** | מטוסי קרב, רק"ם, רחפנים, בסיס לוגיסטי | מחזור חיים של 30 שנה, בלתי הפיך, תחת ביקורת ציבורית. **מחיר היחידה הוא פחות משליש מהעלות הכוללת.** העברת טכנולוגיה ועלות לשעת טיסה קובעות את תקציב שלושת העשורים הבאים. |
| 🏢 **ארגוני** | ספק, ERP, מיקור חוץ, התרחבות | ועדה שאינה מסכימה עם עצמה. **SAPEVO-M** נבנה בדיוק לשם כך: הוא מצרף שיפוט סדר מ**מקבלי החלטות רבים** בלי לדרוש הסכמה מוקדמת. |
| 🚀 **סטארט-אפים** | תיק פרויקטים, הקצאת הון | מי שמחליט לפי תשואה צפויה בוחר תמיד בהימור המסוכן ביותר — **התוחלת מתעלמת מהזנב**. כאן הסיכון הוא **קריטריון**, לא הערת שוליים בשקף 14. |
| 💻 **מערכות מידע** | תקינת מלאי הציוד | ההחלטה מוכפלת ב-200 ונמשכת 4 שנים. משך הסוללה ואחריות באתר שווים יותר, בעלות הבעלות הכוללת, משתי נקודות בבנצ'מרק סינתטי. |

</div>

### מקרים מוכנים להרצה

```bash
python3 pipeline.py --listar
```

| # | מקרה | תחום | חלופות | קריטריונים | פסק | מחברים / מקור |
|--:|---|---|--:|--:|---|---|
| 1 | `smartphone` | צריכה | 6 | 8 | סביר 63% | מידול עצמי |
| 2 | `veiculo_eletrico` | רכב | 7 | 8 | יציב 99% | מידול עצמי |
| 3 | `caca_multifuncao` | ביטחון | 6 | 9 | יציב 100% | מידול עצמי |
| 4 | `blindado` | ביטחון | 5 | 8 | יציב 93% | מידול עצמי |
| 5 | `portfolio_startup` | ארגוני | 7 | 9 | יציב 96% | מידול עצמי |
| 6 | `estacao_trabalho` | מערכות מידע | 6 | 8 | יציב 98% | מידול עצמי |
| 7 | `carros_eletricos` | רכב | 38 | 9 | יציב 96% | מידול עצמי |
| 8 | `smartphones_2026` | צריכה | 38 | 9 | סביר 73% | מידול עצמי |
| 9 | `tablets` | צריכה | 34 | 8 | סביר 67% | מידול עצמי |
| 10 | `smartwatches` | צריכה | 31 | 8 | סביר 84% | מידול עצמי |
| 11 | `notebooks` | מערכות מידע | 32 | 8 | סביר 83% | מידול עצמי |
| 12 | `maquinario_agricola` | אגרו-עסקים | 35 | 8 | יציב 100% | מידול עצמי |
| 13 | `sbc_iot` | מערכות מידע | 33 | 8 | יציב 100% | מידול עצמי |
| 14 | `mineracao_asic` | תשתיות | 31 | 8 | שביר 50% | מידול עצמי |
| 15 | `minipcs` | מערכות מידע | 10 | 8 | יציב 91% | מידול עצמי |
| 16 | `impressoras_3d_miniaturas` | ייצור | 30 | 9 | שביר 48% | מידול עצמי |
| 17 | `impressoras_3d_producao` | ייצור | 30 | 9 | שביר 58% | מידול עצמי |
| 18 | `plotters_formato` | ייצור | 24 | 9 | יציב 96% | מידול עצמי |
| 19 | `impressoras_3d_miniaturas_triadas` | ייצור | 13 | 9 | יציב 100% | מידול עצמי |
| 20 | `acoes_b3` 📚 | פיננסי | 20 | 7 | שביר 39% | COSTA, L. S. da · VÁSQUEZ, J. A.; ESCOBAR, J. W.; MANOTAS, D. F. · [DOI](https://doi.org/10.3390/risks10010004) |
| 21 | `fundos_imobiliarios` 📚 | פיננסי | 18 | 8 | סביר 85% | SANTOS, V. V. dos (orient. ALMEIDA FILHO, A. T. de) |
| 22 | `fintech` 📚 | פיננסי | 16 | 8 | סביר 67% | WIBOWO, S.; GRANDHI, L.; GRANDHI, S.; WELLS, M. · [DOI](https://doi.org/10.3390/math10020225) |
| 23 | `avaliacao_imoveis` 📚 | נדל"ן | 16 | 8 | יציב 94% | DUARTE, D. C. de O. · MARQUES, J. P. M. |
| 24 | `ordens_servico` 📚 | תפעול | 18 | 8 | יציב 97% | ALENCAR, L. G. de; TAVARES, F. R. M.; MENDONÇA, F. J. S. de F.; DUARTE, A. K. G. |
| 25 | `cloud_providers` 📚 | מערכות מידע | 14 | 8 | יציב 100% | SOLOMON, T. |
| 26 | `venture_capital` 📚 | ארגוני | 16 | 8 | יציב 96% | BEIM, G.; LÉVESQUE, M. · DHOCHAK, M.; DOLIYA, P. · AFFUL-DADZIE, E.; AFFUL-DADZIE, A.; OPLATKOVÁ, Z. K. · [DOI](https://doi.org/10.1002/mcda.1703) |
| 27 | `instrutores` 📚 | ארגוני | 15 | 8 | יציב 100% | SILVA, C. E. J. da; SALLES-NETO, L. L. de; SANTOS, M. dos |
| 28 | `cripto_portfolio` 📚 | פיננסי | 9 | 7 | יציב 100% | ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. · [DOI](https://doi.org/10.3390/math9141677) |
| 29 | `portfolio_crise` 📚 | פיננסי | 8 | 4 | סביר 77% | COSTA, I. P. de A.; MAÊDA, S. M. do N.; TEIXEIRA, L. F. H. de S. de B.; GOMES, C. F. S.; SANTOS, M. dos |
| 30 | `cenarios_va` 📚 | רכב | 16 | 9 | סביר 73% | LI, S.; ZHOU, R.; HUANG, H. · [DOI](https://doi.org/10.1007/s42154-024-00344-6) |
| 31 | `impressora_3d_energia` 📚 | ייצור | 12 | 7 | סביר 69% | OLIVEIRA, V. A. R. de; ALVARADO SILVA, C. A.; OLIVEIRA, G. C. R. de; TAJIMA, F. M.; FARIA NETO, A. dos R.; SALOMON, V. A. P.; GUIDI, E. S. · [DOI](https://doi.org/10.18687/LACCEI2025.1.1.1193) |
| 32 | `impressoras_juridico` 📚 | תפעול | 12 | 4 | יציב 100% | OLIVEIRA, N. C.; OLIVEIRA, P. F. C. de; GOMES, C. F. S.; SANTOS, M. dos |
| 33 | `fundos_hedge` 📚 | פיננסי | 20 | 8 | יציב 94% | SILVA, F. P. da; RIBEIRO, C. de O. |
| 34 | `modelos_previsao` 📚 | מערכות מידע | 7 | 8 | יציב 95% | SHAH, S. |
| 35 | `policultivo_rj` 📚 | אגרו-עסקים | 8 | 8 | סביר 86% | PENEDO, B. |
| 36 | `parafusadeiras_domesticas` 📚 | צריכה | 14 | 8 | סביר 70% | COMPROU AVALIOU (canal) · [vídeo](https://youtu.be/pgdqVYEjZtk) |
| 37 | `parafusadeiras_profissionais` 📚 | ייצור | 12 | 8 | יציב 100% | FERRAMENTAS EM AÇÃO — ASSIS PIRES (canal) · [vídeo](https://youtube.com/shorts/9SIs3agoZKc) |
| 38 | `crowdfunding_startups` 📚 | ארגוני | 16 | 9 | יציב 93% | SKARE, M.; GAVUROVA, B.; POLISHCHUK, V. · [DOI](https://doi.org/10.1016/j.jbusres.2023.113719) |

> [!NOTE]
> מטריצות המקרים הן **להמחשה** — סדרי גודל ציבוריים וסבירים, להדגמת השיטה. מה ש**אינו** להמחשה הוא ה**מידול**: קריטריונים, כיוונים, מטריצת הסיבתיות של DEMATEL ומטריצת Saaty. שם שוכן הערך. **החליפו את המספרים בהצעת המחיר שלכם, במכרז שלכם או בבדיקת המעבדה שלכם** — המנוע זהה; הנתונים שלכם.

> [!TIP]
> ה**פסק** מודד בכמה מתוך 2,000 יקומי העדפה מדומים המנצח ממשיך לנצח, בהפרעת המשקלים לפי דיריכלה (κ=200). **יציב** ≥ 90%: הבחירה אינה תלויה בכיול. **סביר** 60–89%: המקום השני תחרותי, השוו בין השניים. **שביר** < 60%: המקום הראשון הוא תוצר של המשקלים — וזהו ממצא לגיטימי, לא כישלון. משמעו שהנתונים אינם מכריעים, וההכרעה חוזרת לאדם.

### 📚 מקרי בוחן הנגזרים מן הספרות

> [!IMPORTANT]
> במקרים שבטבלה שלהלן **הקריטריונים והמבנה הסיבתי נלקחו מן העבודות המפורטות** — מאמרים שעברו שיפוט עמיתים, עבודות גמר, כינוסים מדעיים ודוחות טכניים. הקריטריונים לא הומצאו: הם מגיעים מטקסט המקור, והקרדיט נשמר כאן ובכותרת המודול המתאים. **מטריצות המספרים** הן יצירה עצמית — שום נתון מן העבודות המקוריות לא שוחזר. היכן שקיים DOI מאונדקס, הקישור מוביל לעבודה; היכן שלא, ההפניה הטקסטואלית המלאה מאפשרת לאתרה.

| מקרה | תחום | מחברים | הפניה |
|---|---|---|---|
| `acoes_b3` | פיננסי | COSTA, L. S. da · VÁSQUEZ, J. A.; ESCOBAR, J. W.; MANOTAS, D. F. | *Uma metodologia para a pré-seleção de ações utilizando o método multicritério TOPSIS* (COSTA, UERJ) · *AHP–TOPSIS Methodology for Stock Portfolio Investments*, Risks, v.10, n.1, 4, 2022 (Universidad del Valle) · [DOI](https://doi.org/10.3390/risks10010004) |
| `fundos_imobiliarios` | פיננסי | SANTOS, V. V. dos (orient. ALMEIDA FILHO, A. T. de) | *Avaliação do método Random Forest para auxílio à seleção de fundos de investimento imobiliário listados na Bolsa de Valores*. Trabalho de Graduação, Engenharia da Computação, CIn/UFPE, set. 2023 |
| `fintech` | פיננסי | WIBOWO, S.; GRANDHI, L.; GRANDHI, S.; WELLS, M. | *A Fuzzy Multicriteria Group Decision Making Approach for Evaluating and Selecting Fintech Projects*. Mathematics, v.10, n.2, 225, 2022 — CQUniversity, Austrália · [DOI](https://doi.org/10.3390/math10020225) |
| `avaliacao_imoveis` | נדל"ן | DUARTE, D. C. de O. · MARQUES, J. P. M. | *Análise multicritério e geoestatística aplicadas na avaliação em massa de imóveis urbanos*. Tese, UFV, 2019 · *As formas de avaliar imóvel em leilão judicial*. Universidade São Judas Tadeu, 2023 |
| `ordens_servico` | תפעול | ALENCAR, L. G. de; TAVARES, F. R. M.; MENDONÇA, F. J. S. de F.; DUARTE, A. K. G. | *Priorização de ordens de serviço aplicando métodos de tomada de decisão: o AHP integrado ao PROMETHEE*. Revista Produção Online, v.22, n.2, p.2763-2784, 2022 — URCA, Ceará |
| `cloud_providers` | מערכות מידע | SOLOMON, T. | *Ranking of Cloud Service Providers Using a Dynamic TOPSIS Model for Provisioning of Enterprise IT Infrastructure in the Cloud*. Praxis (Doctor of Engineering), The George Washington University, 2017 |
| `venture_capital` | ארגוני | BEIM, G.; LÉVESQUE, M. · DHOCHAK, M.; DOLIYA, P. · AFFUL-DADZIE, E.; AFFUL-DADZIE, A.; OPLATKOVÁ, Z. K. | *Selecting projects for venture capital funding: a multiple criteria decision approach* (Case Western Reserve University) · *Valuation of a startup: moving towards strategic approaches*, J. Multi-Criteria Decision Analysis, 2019 · *Assessing commercial viability of technology start-up businesses in a government venture capital under intuitionistic fuzzy environment*, Int. J. Fuzzy Systems, 2016 · [DOI](https://doi.org/10.1002/mcda.1703) · [DOI](https://doi.org/10.1007/s40815-016-0141-9) |
| `instrutores` | ארגוני | SILVA, C. E. J. da; SALLES-NETO, L. L. de; SANTOS, M. dos | *Modelagem matemática com os métodos AHP e TOPSIS para ordenação de instrutores em uma escola da FAB*. LIV SBPO, Juiz de Fora, 2022 — ITA / UNIFESP / IME |
| `cripto_portfolio` | פיננסי | ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. | *Cryptocurrency Portfolio Selection — A Multicriteria Approach*. Mathematics, v.9, n.14, 1677, 2021 — University of Split, Croácia — **pesos AHP do artigo** · [DOI](https://doi.org/10.3390/math9141677) |
| `portfolio_crise` | פיננסי | COSTA, I. P. de A.; MAÊDA, S. M. do N.; TEIXEIRA, L. F. H. de S. de B.; GOMES, C. F. S.; SANTOS, M. dos | *Finanças em períodos de crise: aplicação do método SAPEVO-M para composição de portfólios de investimentos*. Pesquisa Operacional para o Desenvolvimento, v.13, e13004, 2021 — UFF / CASNAV / IME — **matriz de decisão do artigo** |
| `cenarios_va` | רכב | LI, S.; ZHOU, R.; HUANG, H. | *Multidimensional Evaluation of Autonomous Driving Test Scenarios Based on AHP-EWM-TOPSIS Models*. Automotive Innovation, 2025 · [DOI](https://doi.org/10.1007/s42154-024-00344-6) |
| `impressora_3d_energia` | ייצור | OLIVEIRA, V. A. R. de; ALVARADO SILVA, C. A.; OLIVEIRA, G. C. R. de; TAJIMA, F. M.; FARIA NETO, A. dos R.; SALOMON, V. A. P.; GUIDI, E. S. | *Multicriteria Analysis for 3D Printer Selection*. 23rd LACCEI International Multi-Conference, Cidade do México, 2025 — UNESP / Universidad César Vallejo · [DOI](https://doi.org/10.18687/LACCEI2025.1.1.1193) |
| `impressoras_juridico` | תפעול | OLIVEIRA, N. C.; OLIVEIRA, P. F. C. de; GOMES, C. F. S.; SANTOS, M. dos | *Aplicação do método AHP TOPSIS 2N como apoio à tomada de decisão: estudo de caso no departamento jurídico da Secretaria Municipal de Saúde de Duque de Caxias* — UNIGRANRIO / UFF / IME |
| `fundos_hedge` | פיננסי | SILVA, F. P. da; RIBEIRO, C. de O. | *Análise comparativa de fundos de hedge brasileiros utilizando DEA e bootstrap*. XII SIMPEP, Bauru-SP, 2005 — Escola Politécnica da USP |
| `modelos_previsao` | מערכות מידע | SHAH, S. | *Comparison of Stochastic Forecasting Models*. Stochastic Differential Equations Course Project, Johns Hopkins University — o artigo compara os modelos; a modelagem multicritério sobre eles é deste projeto |
| `policultivo_rj` | אגרו-עסקים | PENEDO, B. | *AGTech PoliCultivo 4.0 — Otimização de Portfólio de Cultivos em Ambiente Controlado (RJ)*. Relatório técnico, 03/08/2026, seção 14 — **matriz e pesos do relatório** |
| `parafusadeiras_domesticas` | צריכה | COMPROU AVALIOU (canal) | *As 5 Melhores Parafusadeira De 2025*, 14/05/2024 — especificações extraídas da narração · [vídeo](https://youtu.be/pgdqVYEjZtk) |
| `parafusadeiras_profissionais` | ייצור | FERRAMENTAS EM AÇÃO — ASSIS PIRES (canal) | *As Melhores Parafusadeiras Do Mundo*, 04/01/2024 — modelos e baterias lidos dos quadros do vídeo · [vídeo](https://youtube.com/shorts/9SIs3agoZKc) |
| `crowdfunding_startups` | ארגוני | SKARE, M.; GAVUROVA, B.; POLISHCHUK, V. | *A decision-making support model for financing start-up projects by venture capital funds on a crowdfunding platform*. Journal of Business Research, v.158, 113719, 2023 — **critérios e escalas do artigo** · [DOI](https://doi.org/10.1016/j.jbusres.2023.113719) |

---

## ⚡ התקנה

### המסלול המהיר ביותר (Python)

```bash
git clone <url> multicriteriadecisionmodels
cd multicriteriadecisionmodels/public/foundations/pipeline
pip install -r requirements.txt
python3 pipeline.py
```

זהו. כל ששת המקרים רצים, עם דוח מלא.

<details>
<summary><b>דרישות מוקדמות מפורטות</b></summary>

| רכיב | גרסה מזערית | חובה? | לשם מה |
|---|---|---|---|
| Python | 3.10 | ✅ | מנוע ייחוס |
| NumPy | 2.0 | ✅ | האלגברה של כל השיטות |
| numba | 0.60 | ⚠️ | JIT לגרעינים — בלעדיו התוצאה זהה, רק איטית יותר |
| SciPy | 1.10 | ✅ | סטטיסטיקה עזר |
| matplotlib | 3.7 | ✅ | 5 מסכים לכל מקרה |
| Rust / cargo | 1.75 | ⭕ | מנוע בדיקה צולבת |
| Node.js | 18 | ⭕ | לוח מחוונים Evidence |
| screen | — | ⭕ | הרצה ברקע |

</details>

### צנרת מלאה

```bash
./run_all.sh                    # בדיקות → צנרת → מסכים → i18n → Rust → הצלבה
./run_all.sh --rapido           # מדלג על Rust ו-i18n
./run_all.sh --caso smartphone  # מקרה יחיד
./run_all.sh --background       # רץ ב-screen (חיבור מחדש: screen -r mcdm)
```

### מנוע Rust — קובץ בינארי ללא סביבת ריצה

```bash
cd public/foundations/rust/mcdm_core
cargo test --release
cargo build --release

./target/release/mcdm --exemplo > problema.mcdm
./target/release/mcdm problema.mcdm
./target/release/mcdm problema.mcdm --json
```

### לוח מחוונים

```bash
cd public/foundations/evidence
npm install
npm run dev               # http://localhost:3000
```

<details>
<summary><b>פקודות מתקדמות</b></summary>

```bash
python3 pipeline.py caca_multifuncao --workers 8 --iter 5000
python3 testes_nucleo.py
python3 exportar_rust.py
python3 gerar_i18n.py --tudo
python3 gerar_i18n.py --verificar
python3 gerar_graficos.py --workers 6
```

| משתנה | ברירת מחדל | השפעה |
|---|---|---|
| `MCDM_WORKERS` | auto | תהליכי `ProcessPoolExecutor` |
| `MCDM_NUMBA` | `1` | JIT פעיל; `0` לניפוי ב-NumPy טהור |
| `MCDM_SEED` | `42` | שחזוריות |
| `ROBUSTEZ_ITER` | `2000` | יקומי העדפה |
| `ROBUSTEZ_KAPPA` | `200` | ריכוז הדיריכלה (גבוה יותר = משקלים קרובים יותר למקור) |
| `MAUT_AVERSAO` | `2.0` | שנאת סיכון (r > 0 = קעורה) |
| `PROMETHEE_TIPO` | `linear` | פונקציית העדפה (6 זמינות) |

</details>

---

## ⚖️ עשר אסכולות ההחלטה — ולמה עשר

> [!IMPORTANT]
> **כל שיטה היא תיאוריה שונה על משמעות המילה «טוב יותר».** להשתמש רק באחת פירושו לבחור את התשובה יחד עם השאלה. אנו מריצים את כל התשע משום ש**הסכמה בין תיאוריות עצמאיות** היא הראיה החזקה ביותר שבעיית החלטה מאפשרת.

<div align="center">

| שיטה | אסכולה | מה היא מניחה | מתי היא הכלי **הנכון** | מקור |
|---|---|---|---|---|
| **AHP-TOPSIS 2n** | מרחק מהאידיאל | פיצוי מלא | קריטריונים כמותיים, מחליט יחיד | Saaty (1980); Hwang & Yoon (1981) |
| **ELECTRE I** | דירוג-על | אי-השוואתיות מותרת | **סינון**: לסלק את הנשלט | Roy (1968) |
| **ELECTRE II** | דירוג-על | ספים חזק וחלש | דירוג מלא **עם וטו** | Roy & Bertier (1971) |
| **PROMETHEE II** | דירוג-על | העדפה הדרגתית (6 פונקציות) | כאשר «קצת יותר טוב» ≠ «טוב יותר» | Brans & Vincke (1985) |
| **MAUT** | תועלת | אי-תלות חיבורית + שנאת סיכון | החלטה תחת אי-ודאות | Keeney & Raiffa (1976) |
| **MCDA-C** | קונסטרוקטיביסטית | רמות ניטרלי/טוב מעוגנות | **אבחון מוחלט**, לא רק דירוג | Ensslin, Montibeller & Noronha (2001) |
| **VIKOR** | פשרה | תועלת הקבוצה × חרטה מרבית | כאשר **פיצוי אינו מקובל** | Opricovic (1979); Opricovic & Tzeng (2002-07) |
| **TODIM** | תורת הפרוספקט | הפסד כואב יותר מרווח שווה ערך | מחליט שונא הפסד — **כולם כאלה** | Gomes & Lima (1992); Kahneman & Tversky (1979) |
| **SAPEVO-M** | סדר, מרובה מחליטים | שיפוט סדר של מחליטים רבים | **ועדה שאינה מסכימה עם עצמה** | Gomes et al. (1997); Teixeira, Santos & Gomes (2019) |
| **TOPSIS Fuzzy** | עמום | שהנתון הוא **טווח**, לא נקודה | המדידה אינה מדויקת ואתם רוצים לדעת אם הדירוג שורד זאת | Zadeh (1965); Chen (2000) |

</div>

> [!NOTE]
> **TOPSIS עמום** אינו AHP-TOPSIS עם רעש: מלבד המספרים המשולשים, הוא מחליף את הנרמול (לינארי במקום וקטורי) ואת הפתרון האידיאלי (מוחלט במקום יחסי). **סטייה מ-AHP-TOPSIS 2n היא ההתנהגות הצפויה**, והיא מודדת כמה הדירוג תלוי בבחירות הללו. **AHP עמום** (Buckley) מצטרף כמקור משקל שלישי, לצד DEMATEL ו-AHP: הוא מקבל את אותו שיפוט זוגי אך נושא את אי-הדיוק עד הסוף — בפיזור אחיד הערך המרכזי זהה לזה של AHP, ומה שהוא מוסיף הוא ה**טווח**, שעונה אם סדר העדיפויות שורד את אי-הדיוק של מקבל ההחלטה עצמו.

<details>
<summary><b>מדוע שלוש אלה ראויות לתשומת לב מיוחדת</b></summary>

### VIKOR — כאשר פיצוי אינו מקובל
VIKOR מחשב **שני** מדדים: `S` (תועלת הקבוצה — סכום משוקלל, ה**מקבל** שביצוע גרוע במיוחד יקוזז בכמה טובים) ו-`R` (חרטה אישית מרבית — מינימקס, ה**דוחה** פיצוי).

רק"ם בעל ניידות מצוינת והגנה גרועה יקבל `S` מצוין ו-`R` איום. הסכום המשוקלל היה בוחר בו; VIKOR מתריע. וכאשר `S` ו-`R` חלוקים, התנאים **C1** (יתרון מקובל) ו-**C2** (יציבות מקובלת) מדווחים במפורש שלהחלטה יש נקודה עיוורת.

### TODIM — ההפסד כואב יותר מהרווח
מבוסס על **תורת הפרוספקט** של Kahneman ו-Tversky: לאבד 10 נקודות טווח כואב יותר משמרוויחים 10 מסב הנאה. הסכום המשוקלל הקלאסי מתעלם מאי-סימטריה זו ומתייחס לרווח ולהפסד כסימטריים — **מה שאף מקבל החלטות אנושי אינו עושה.** המקדם `θ` מכייל את העוצמה: `θ < 1` מגביר את שנאת ההפסד.

### SAPEVO-M — הוועדה שאינה מסכימה
כל שאר השיטות דורשות וקטור משקלים. **מהיכן הוא מגיע כשחמישה מחליטים חלוקים בדעתם?** SAPEVO-M פותר זאת במקור: כל מחליט מביע העדפה **סדרית** («הטווח חשוב הרבה יותר מהמחיר», בסולם בן שבע נקודות), והשיטה מצרפת **בלי לדרוש סדר הסכמה מוקדם**. כך ועדה באמת מתבטאת — איש אינו אומר «הטווח שווה 0.237».

</details>

### מנוע הקונצנזוס

```
DEMATEL ──► משקלים לפי השפעה ──► 10 שיטות ──► קונצנזוס בורדה ──► מנצח
                                                    │
                        2,000 יקומי דיריכלה ─────────────────┘
                                    ▼
                     פסק: ROBUSTO / PROVÁVEL / FRÁGIL
```

| פסק | ביטחון | מה לעשות |
|---|---|---|
| 🟢 **חסין** | ≥ 90% | הבחירה אינה תלויה בכיול עדין. **אפשר להביא אותה לוועדה.** |
| 🟡 **סביר** | 60–90% | היא מחזיקה ברוב התרחישים, אך המקום השני תחרותי. **השוו בין השניים.** |
| 🔴 **שביר** | < 60% | המקום הראשון הוא **תוצר של המשקלים**. אל תחליטו לפי הדירוג בלבד: חזרו למקבל ההחלטות וכיילו מחדש. |

---

## 🔬 שני מנועים עצמאיים: הבדיקה הצולבת

> [!TIP]
> **למה לממש הכול מחדש ב-Rust?** מפני ש«הקוד רץ» אינו ראיה לכך שה**מתמטיקה** נכונה.

שגיאת שעתוק נוסחה כמעט לעולם אינה חוזרת **זהה** בשתי שפות שהאלגברה הליניארית שלהן עצמאית. מנוע ה-Python משתמש ב-NumPy/LAPACK; מנוע ה-Rust מממש חילוץ גאוס עם פיבוט חלקי ואת שיטת החזקות **ידנית, ללא כל תלות חיצונית**.

```bash
python3 exportar_rust.py
```
```
✅ smartphone           8 שיטות זהות · מנצח=C     (Δ ≤ 4.7e-11)
✅ veiculo_eletrico     8 שיטות זהות · מנצח=EV6   (Δ ≤ 4.1e-11)
✅ caca_multifuncao     8 שיטות זהות · מנצח=C3    (Δ ≤ 4.5e-11)
✅ blindado             8 שיטות זהות · מנצח=B3    (Δ ≤ 4.6e-11)
✅ portfolio_startup    8 שיטות זהות · מנצח=P3    (Δ ≤ 4.9e-11)
✅ estacao_trabalho     8 שיטות זהות · מנצח=W5    (Δ ≤ 5.0e-11)
```

**בונוס: הקובץ הבינארי של Rust אינו זקוק ל-Python, ל-NumPy, ל-numba ולא לסביבה וירטואלית. כמה מגה-בייט שרצים על שרת, מכולה או מכונה משובצת — מה שחשוב כשהמנוע מלווה מערכת בשטח.**

---

## 🚀 ביצועים: מהיר פי 26, אותה תשובה

ניתוח החוסן מריץ 2,000 יקומים × 10 שיטות. המימוש הנאיבי ארך **42 שניות** למקרה.

<div align="center">

| שלב | זמן | האצה |
|---|---|---|
| גרעיני JIT לכל יקום | 42,33 s | — |
| **הידור מוקדם לטנזורים** | 2,41 s | **17,6×** |
| `ranks` תחת JIT + מצב לכל תהליך | **1,63 s** | **26,0×** |

</div>

> **האופטימיזציה המשתלמת ביותר לא הייתה מקבילות ולא JIT.** היא הייתה ההבנה שארבע מעשר השיטות **ליניאריות בווקטור המשקלים** — מה שמאפשר לחשב טנזורים מראש ולצמצם כל יקום למכפלת מטריצה-וקטור אחת. **אלגברה לפני תשתית.**

והתוצאה **זהה סיבית-לסיבית** למסלול האיטי — 100 יקומים × 10 שיטות נבדקים בכל הרצה של הסוויטה. אופטימיזציה המשנה את התוצאה היא תקלה, לא רווח.

<details>
<summary><b>מדיניות ההרצה של הפרויקט</b></summary>

| כלל | יישום |
|---|---|
| **מקבילות** | `ProcessPoolExecutor` לעבודה עתירת מעבד; לעולם לא תהליכונים (ה-GIL מסדר בטור) |
| **סף** | טורי מול מקבילי נקבע לפי **נפח העבודה** (`n_iter · m² · k`), לא לפי מספר הפריטים — להקביל בעיה קטנה **איטי יותר** מלפתור אותה |
| **JIT** | `numba` עם `cache=True` על גרעיני O(m²k); יורד ל-NumPy טהור בהיעדרו |
| **רקע** | `screen`, לעולם לא `nohup` — מאפשר חיבור מחדש ואינטראקציה |
| **שחזוריות** | חלוקה קבועה ובלתי תלויה במספר התהליכים: אותו זרע → תוצאה זהה עם תהליך אחד או 32 |

</details>

---

## 🌐 12 שפות — זיכרון תרגום SDL Trados

זה אינו תרגום מכונה של README. זו **צנרת לוקליזציה** עם זיכרון תרגום בתקן **SDL Trados Studio**.

```
translation.memory.md          ← מקור קנוני, מנוהל בגרסאות ב-git
   │  --tm
   ▼
strings.<locale>.json          ← תוצר נצרך
   │  --paginas
   ▼
12 עמודי לוח מחוונים + 12 קובצי README
   │  --tmx
   ▼
translation.memory.tmx         ← ניתן לייבוא ל-SDL Trados Studio
```

| פריט | מספרים |
|---|---|
| אזורי שפה | **12** (pt-BR · en · es · fr · de · zh · ko · hi · **he RTL** · ru · sv · fi) |
| יחידות תרגום | 56 |
| מונחי מילון (MultiTerm) | 22 |
| מקטעים ב-TMX | **948** |
| קידוד | UTF-8 · LF · NFC |

```bash
python3 gerar_i18n.py --verificar
```

בקרת האיכות משכפלת את ה-**Verify** של Trados: עקביות מונחית, שמירת placeables, כיסוי מקטעים, קידוד קפדני ובלתי-מתורגמים ללא פגע — עם כלל נבדל לפי מערכת כתב (ראשי תיבות טכניים נשארים בלטינית בכל שפה; שמות פרטיים עוברים **תעתיק** היכן שהכתב אינו לטיני).

---

## 📁 מה יש בפנים

```
multicriteriadecisionmodels/
├── README.md (+11)                     חלון ראווה ב-12 שפות
├── docs/                               לוגו ומסכים עבור קובצי README
│
└── public/foundations/
    ├── pipeline/                       מנוע PYTHON (ייחוס)
    │   ├── nucleo.py                   DEMATEL · ELECTRE I/II · PROMETHEE II
    │   │                               MAUT · MCDA-C · AHP · TOPSIS 2N
    │   ├── metodos_br.py               SAPEVO-M · VIKOR · TODIM · Copeland
    │   ├── robustez.py                 דיריכלה + ProcessPoolExecutor
    │   ├── pipeline.py                 מתזמר
    │   ├── gerar_graficos.py           5 מסכים לכל מקרה
    │   ├── gerar_i18n.py               TM → מחרוזות → עמודים → TMX
    │   ├── testes_nucleo.py            16 בדיקות מתמטיות
    │   ├── exportar_rust.py            הצלבה בין המנועים
    │   ├── casos/catalogo.py           6 מקרים + אימות
    │   └── run_all.sh                  צנרת (screen)
    │
    ├── rust/mcdm_core/                 מנוע RUST (אימות + הפצה)
    │   └── src/lib.rs                  כל השיטות, אפס תלויות
    │
    └── evidence/                       לוח מחוונים (Evidence.dev)
        ├── sources/mcdm/               11 שאילתות SQL
        └── pages/                      12 נתיבי שפה
```

---

## 🧠 בסיס עיוני

הפרויקט בנוי על ספרות שעברה שיפוט, לא על אינטואיציה. ארכיטקטורת השילוב הולכת בעקבות **John (2025)**, *«Integration of DEMATEL with Other MCDM Methods for Comprehensive Techno-Economic Analysis»*: DEMATEL חושף את מבנה הסיבתיות וגוזר **משקלים לפי השפעה**, המזינים אחר כך את שיטות הדירוג — במקום משקלים שרירותיים.

שיטות ה**אסכולה הברזילאית לתמיכה רב-קריטריונית בהחלטות** (SAPEVO-M, TODIM-FSE, ELECTRE II, VIKOR, שיטות סדר) הולכות בעקבות עבודות **IME**, **UFF**, **CASNAV**, **AMAN** ו-**FURB** — לרבות יישומים ממשיים ב**הערכת רחפנים ללוחמה ימית**, ב**סיווג בסיס לוגיסטי של חטיבה** וב**דירוג קורבטות לצי הברזילאי**.

> [!NOTE]
> **הבעלות על השיטות שייכת במלואה ליוצריהן,** המקבלים קרדיט פרטני בכותרות `nucleo.py` ו-`metodos_br.py`. תרומת הפרויקט היא המימוש, השילוב ומנוע הקונצנזוס — **לא השיטות**.

---

## ❓ שאלות שתשאלו

<details>
<summary><b>אני כבר משתמש במטריצת החלטה משוקללת. זה לא אותו דבר?</b></summary>

לא, משלוש סיבות. **(1)** מטריצה משוקללת היא שיטה **אחת** (סכום משוקלל), ובה תיאוריה מוטמעת: פיצוי מלא. היא מניחה שביצוע גרוע בקריטריון אחד ניתן לקיזוז במקום אחר — מה שאינו נכון בבטיחות, בהגנה משוריינת ובעמידה ברגולציה. **(2)** היא מניחה קריטריונים עצמאיים, ואתם כמעט תמיד מחברים דברים שכבר חוברו. **(3)** היא מחזירה מספר בלי רווח בר-סמך, ולכן אינה שורדת את השאלה הראשונה של הוועדה.
</details>

<details>
<summary><b>איך אני בוחר את המשקלים?</b></summary>

אתם לא בוחרים — **שלושה מסלולים גוזרים אותם**. **DEMATEL** מחלץ אותם ממבנה הסיבתיות שהצהרתם עליו (מי משפיע על מי). **AHP** מחלץ אותם מהשוואות זוגיות, עם בדיקת עקביות ה**פוסלת** שיפוט סותר. **SAPEVO-M** מחלץ אותם משיפוט סדר של מחליטים רבים. ואחר כך ניתוח החוסן שואל עד כמה התוצאה עדיין **תלויה** בהם.
</details>

<details>
<summary><b>ומה אם בבעיה שלי יש 200 חלופות?</b></summary>

זה רץ. סף המקביליות מזהה את סדר הגודל ומחלק בין התהליכים. נמדד: 60 חלופות × 12 קריטריונים × 2,000 יקומים ב-3.8 שניות עם 4 תהליכים. מעל כ-700 חלופות טנזור ההעדפות חורג ממגבלת הזיכרון שהוגדרה, והמנוע מתריע במקום להיתקע.
</details>

<details>
<summary><b>השיטות חלוקות. ומה עכשיו?</b></summary>

**זה המוצר, לא הבעיה.** המחלוקת אומרת שההחלטה שלכם רגישה לאסכולה שנבחרה — ונוקבת באיזו. אם ELECTRE מוריד בדירוג את מי שכל השאר בוחרים, קיים קריטריון שבו החלופה הזו חמורה דיה לוטו. הביאו לוועדה **את זה**, לא את הדירוג.
</details>

<details>
<summary><b>אפשר להשתמש בנתונים שלי?</b></summary>

בדיוק לשם כך זה נועד. מקרה הוא מבנה הצהרתי ב-`casos/catalogo.py`: קריטריונים (עם כיוון ויחידה), חלופות, מטריצת החלטה, מטריצת הסיבתיות של DEMATEL ומטריצת Saaty. המאמת דוחה מקרה פגום **לפני** כל חישוב — ממדים לא עקביים, אלכסון שגוי, מטריצת Saaty לא הדדית, קריטריון קבוע שאינו מבחין בין דבר.
</details>

---

## 📜 רישיון ובעלות

<div align="center">

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="420"/>

**ProfBru © 2026**

**MCDM Studio — מודלים רב-קריטריוניים לקבלת החלטות**
מחבר: **ProfBru - Bruno Penedo** © 2026 — **כל הזכויות שמורות**
📧 profbruanbima@gmail.com

</div>

פרויקט **קנייני**. מאגר זה אינו מעניק כל רישיון לשימוש, העתקה, שינוי, הפצה או יצירת יצירות נגזרות. שימוש מסחרי, אקדמי או מוסדי מחייב אישור בכתב מהמחבר.

**ייחוס לצדדים שלישיים:** השיטות הרב-קריטריוניות הן יצירתם של יוצריהן — Saaty, Roy, Bertier, Brans, Vincke, Keeney, Raiffa, Ensslin, Montibeller, Noronha, Gabus, Fontela, Opricovic, Tzeng, Hwang, Yoon, Kahneman, Tversky, Borda, Copeland, Gomes, Lima, Santos, Teixeira, Moreira, Rangel, Neves, Hein, Kroenke, Keunecke ו-Gomes Júnior — המקבלים קרדיט פרטני בקוד המקור.
