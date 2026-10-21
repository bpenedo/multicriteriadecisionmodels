---
title: MCDM Studio — Decisão MultiКритерий
---

<div style="text-align:center;">

🌐 [Português](/) · [English](/en/) · [Español](/es/) · [Français](/fr/) · [Deutsch](/de/) · [中文](/zh/) · [한국어](/ko/) · [हिन्दी](/hi/) · [עברית](/he/) · **Русский** · [Svenska](/sv/) · [Suomi](/fi/)

<div style="text-align:center;margin:1.2rem 0 1.6rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="200" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.5rem;font-size:1.05rem;">ProfBru © 2026</div>
</div>

_MCDM Studio — Modelos MultiКритерий de Decisão · Autor: **ProfBru - Bruno Penedo** © 2026 — ВСЕ ПРАВА ЗАЩИЩЕНЫ · profbruanbima@gmail.com_

</div>

<!--
  ÍNDICE LEVE, DE PROPÓSITO.
  Só consultas AGREGADAS (uma linha por caso). As tabelas detalhadas — ranking por
  método (3.744 linhas), Матрица решений (3.514), distribuição (4.230), Робастность por
  método (4.160) — vivem nas páginas de caso, onde estão filtradas por `id_caso`.
  Carregá-las todas aqui somava ~16 mil linhas e travava o navegador.
-->

```sql casos
select *, '/ru/casos/' || id_caso as link from mcdm.casos
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

# 🎯 Многокритериальное решение — десять школ, один вердикт с доверительным интервалом

> **Таблица не ошибается в счёте. Она ошибается в вопросе.** Сортировка по цене выбирает самое дешёвое. Сортировка по оценке эксперта выбирает самое дорогое. Фильтр «соответствует всем требованиям» обычно опустошает список. Ни один из трёх не отвечает на заданный вопрос: *среди альтернатив, противоречащих друг другу, какую выбрать — и с какой уверенностью?*

Эта панель выполняет **десять многокритериальных методов** для каждого кейса, выводит победителя из **консенсуса Борда** между ними, а затем **возмущает веса 2 000 раз**, чтобы ответить на единственный вопрос, который комитет действительно задаёт: *а если бы мы задали чуть иной вес?*

<BigValue data={totais} value=casos title="Случаи принятия решений" fmt=num0/>
<BigValue data={totais} value=alternativas title="Оценённые альтернативы" fmt=num0/>
<BigValue data={totais} value=robustos title="РОБАСТНЫЕ вердикты" fmt=num0/>
<BigValue data={totais} value=frageis title="ХРУПКИЕ вердикты" fmt=num0/>

## 📋 Случаи принятия решений

> Нажмите на любой кейс, чтобы открыть **полный отчёт**: диаграмма причина-следствие DEMATEL, карта десяти школ, ядро ELECTRE, двойная нормализация TOPSIS, консенсус Борда, робастность на 2 000 вселенных, матрица BCG и матрица решения.

<DataTable data={casos} rows=all rowShading=true link=link>
  <Column id=nome title="Случай"/>
  <Column id=dominio title="Область"/>
  <Column id=n_alternativas title="Альтернативы" fmt=num0/>
  <Column id=vencedor_rotulo title="🏆 Победитель"/>
  <Column id=prob_vitoria title="Уверенность (%)" fmt=num1 contentType=colorscale/>
  <Column id=classificacao title="Вердикт"/>
</DataTable>

> **Как читать вердикт.** `РОБАСТНЫЙ` (≥ 90%) = выбор не зависит от тонкой калибровки весов; его можно вынести на комитет. `ВЕРОЯТНЫЙ` (60–90%) = держится в большинстве сценариев, но второй конкурентоспособен. `ХРУПКИЙ` (ниже 60%) = **первое место — артефакт весов**, и система говорит это вместо того, чтобы выставлять трофей.

<BarChart data={resumo_dominio} x=dominio y=casos title="Кейсы по области применения" yAxisTitle="Casos"/>

## 🧮 DEMATEL — первопричина каждого решения

> Вопрос, который почти никто не задаёт перед назначением весов: **независимы ли критерии?** Почти никогда. Энергопотребление *вызывает* запас хода; броня *вызывает* массу, а масса *вызывает* потерю подвижности. Складывать их как независимые — значит считать одно и то же дважды.
>
> **DEMATEL** (Gabus и Fontela, Battelle) строит матрицу полных связей `T = X(I−X)⁻¹` — она суммирует прямые **и косвенные** влияния любой длины пути — и разделяет: `R+C` = важность в системе; `R−C > 0` = **ПРИЧИНА** (рычаг: действовать здесь) и `R−C < 0` = **СЛЕДСТВИЕ** (термометр: результат уже сделанного).
>
> Столбец **Первопричина** ниже — это критерий с наибольшим `R−C` в каждом кейсе: именно там одно вмешательство двигает всю систему.

<DataTable data={alavancas} rows=all rowShading=true>
  <Column id=nome title="Случай"/>
  <Column id=n_criterios title="Критерии" fmt=num0/>
  <Column id=n_causas title="Причины" fmt=num0 contentType=colorscale/>
  <Column id=causa_raiz title="🔧 Первопричина (наибольшее R−C)"/>
  <Column id=criterio_maior_peso title="Критерий с наибольшим весом"/>
  <Column id=maior_peso_pct title="Вес (%)" fmt=num1/>
</DataTable>

<BarChart data={alavancas} x=nome y={['n_causas','n_criterios']} type=grouped title="Критерии, являющиеся ПРИЧИНОЙ в каждом кейсе (рычаги относительно общего числа)" yAxisTitle="Critérios" swapXY=true/>

> **Откройте кейс**, чтобы увидеть полную диаграмму причина-следствие, таблицу с раздельными `R` и `C` и **матрицу полных связей** со связями по одной.

## 🎲 Матрица BCG — карта возможностей по категориям

> Помимо *что выбрать*, у каждой категории есть **профиль возможностей**: сколько альтернатив являются ⭐ Звездой (вкладывать), 🐄 Коровой (собирать урожай), ❓ Знаком вопроса (взвесить приз) и 🐕 Собакой (отбросить). Категория из одних знаков вопроса — дорогой рынок; полная коров — зрелый рынок, где деньги решают мало.

<DataTable data={bcg_geral} rows=all rowShading=true>
  <Column id=nome title="Категория"/>
  <Column id=estrelas title="⭐" fmt=num0 contentType=colorscale/>
  <Column id=vacas title="🐄" fmt=num0 contentType=colorscale/>
  <Column id=interrogacoes title="❓" fmt=num0 contentType=colorscale/>
  <Column id=abacaxis title="🐕" fmt=num0 contentType=colorscale/>
  <Column id=total title="Итого" fmt=num0/>
  <Column id=quadrante_do_vencedor title="Квадрант первого места"/>
</DataTable>

## ⚖️ Десять школ принятия решений

> Каждый метод — это **иная теория о том, что значит «лучше»**, и потому мы запускаем их все: когда десять независимых школ выбирают одного и того же победителя, выбор не является артефактом одного метода. Когда они расходятся, расхождение указывает, где лежит настоящий компромисс.

| Método | Escola | O que assume | Quando é a ferramenta certa |
|---|---|---|---|
| **AHP-TOPSIS 2n** | Distância à solução ideal | Compensação total entre Критерийs | Критерии quantitativos, decisor único |
| **ELECTRE I** | Превосходитção | Incomparabilidade é permitida | Triagem: eliminar o que é dominado |
| **ELECTRE II** | Превосходитção | Limiares forte e fraco | Ordenação completa com veto |
| **PROMETHEE II** | Превосходитção | Preferência gradual (6 funções) | Quando "um pouco melhor" não é "melhor" |
| **MAUT** | Utilidade | Independência aditiva + Неприятие риска | Decisão sob incerteza |
| **MCDA-C** | Construtivista | Níveis Neutro/Bom ancorados | Diagnóstico absoluto, não só ranking |
| **VIKOR** | Compromisso | Utilidade do grupo × arrependimento máximo | Quando compensar é inaceitável |
| **TODIM** | Teoria dos Prospectos | Perda dói mais que ganho equivalente | Decisor avesso a perda (todos são) |
| **SAPEVO-M** | Ordinal multidecisor | Julgamento ordinal de vários decisores | Comitê que não concorda entre si |

## 🎯 Робастность — доверительный интервал самого решения

> **Проблема.** Любой метод MCDM возвращает победителя с неявной уверенностью 100%. Но веса никогда не точны — это оценки предпочтений. Если два процентных пункта в весе одного критерия меняют первое и второе место, «победитель» — артефакт калибровки, а не факт о множестве. Об этом никто не сообщает. **Именно здесь решения умирают в комитете.**
>
> **Решение.** Мы возмущаем веса как `w' ~ Dirichlet(κ·w)` и переранжируем 2 000 раз. Дирихле — естественный выбор: её носитель — в точности симплекс (положительные веса с суммой 1), и она удовлетворяет `E[w'] = w` — мы возмущаем **без смещения**. При κ = 200 вес 13% колеблется на ±2,4 п.п.
>
> Вердикт перестаёт быть *«Модель C — лучшая»* и становится **«Модель C побеждает в 96% правдоподобных вселенных предпочтений»**.

**Откройте кейс из таблицы выше**, чтобы увидеть диаграмму причина-следствие, карту десяти школ, матрицу BCG и полное распределение мест по 2 000 вселенных.

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
