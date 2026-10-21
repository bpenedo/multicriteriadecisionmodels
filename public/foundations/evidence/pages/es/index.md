---
title: MCDM Studio — Decisão MultiCriterio
---

<div style="text-align:center;">

🌐 [Português](/) · [English](/en/) · **Español** · [Français](/fr/) · [Deutsch](/de/) · [中文](/zh/) · [한국어](/ko/) · [हिन्दी](/hi/) · [עברית](/he/) · [Русский](/ru/) · [Svenska](/sv/) · [Suomi](/fi/)

<div style="text-align:center;margin:1.2rem 0 1.6rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="200" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.5rem;font-size:1.05rem;">ProfBru © 2026</div>
</div>

_MCDM Studio — Modelos MultiCriterio de Decisão · Autor: **ProfBru - Bruno Penedo** © 2026 — TODOS LOS DERECHOS RESERVADOS · profbruanbima@gmail.com_

</div>

<!--
  ÍNDICE LEVE, DE PROPÓSITO.
  Só consultas AGREGADAS (uma linha por caso). As tabelas detalhadas — ranking por
  método (3.744 linhas), Matriz de decisión (3.514), distribuição (4.230), robustez por
  método (4.160) — vivem nas páginas de caso, onde estão filtradas por `id_caso`.
  Carregá-las todas aqui somava ~16 mil linhas e travava o navegador.
-->

```sql casos
select *, '/es/casos/' || id_caso as link from mcdm.casos
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

# 🎯 Decisión Multicriterio — diez escuelas, un veredicto con intervalo de confianza

> **La hoja de cálculo no se equivoca en la cuenta. Se equivoca en la pregunta.** Ordenar por precio elige el más barato. Ordenar por nota de experto elige el más caro. Filtrar por "cumple todos los requisitos" suele vaciar la lista. Ninguna de las tres responde a la pregunta que se hizo: *entre alternativas que se contradicen, cuál elegir — y con qué confianza?*

Este panel ejecuta **diez métodos multicriterio** sobre cada caso, extrae el ganador del **consenso de Borda** entre ellos y después **perturba los pesos 2.000 veces** para responder a la única pregunta que el comité realmente hace: *¿y si hubiéramos dado un peso un poco distinto?*

<BigValue data={totais} value=casos title="Casos de decisión" fmt=num0/>
<BigValue data={totais} value=alternativas title="Alternativas evaluadas" fmt=num0/>
<BigValue data={totais} value=robustos title="Veredictos ROBUSTOS" fmt=num0/>
<BigValue data={totais} value=frageis title="Veredictos FRÁGILES" fmt=num0/>

## 📋 Casos de decisión

> Haz clic en cualquier caso para abrir el **informe completo**: diagrama causa-efecto del DEMATEL, mapa de las diez escuelas, núcleo del ELECTRE, doble normalización del TOPSIS, consenso de Borda, robustez bajo 2.000 universos, matriz BCG y la matriz de decisión.

<DataTable data={casos} rows=all rowShading=true link=link>
  <Column id=nome title="Caso"/>
  <Column id=dominio title="Dominio"/>
  <Column id=n_alternativas title="Alternativas" fmt=num0/>
  <Column id=vencedor_rotulo title="🏆 Ganador"/>
  <Column id=prob_vitoria title="Confianza (%)" fmt=num1 contentType=colorscale/>
  <Column id=classificacao title="Veredicto"/>
</DataTable>

> **Cómo leer el Veredicto.** `ROBUSTO` (≥ 90%) = la elección no depende de la calibración fina de los pesos; puede ir al comité. `PROBABLE` (60–90%) = se sostiene en la mayoría de los escenarios, pero el segundo es competitivo. `FRÁGIL` (por debajo del 60%) = **el 1.º puesto es un artefacto de los pesos** — el sistema lo dice en lugar de exhibir un trofeo.

<BarChart data={resumo_dominio} x=dominio y=casos title="Casos por dominio de aplicación" yAxisTitle="Casos"/>

## 🧮 DEMATEL — la causa raíz de cada decisión

> La pregunta que casi nadie hace antes de asignar pesos: **¿son independientes los criterios?** Casi nunca lo son. El consumo energético *causa* autonomía; el blindaje *causa* peso, que *causa* pérdida de movilidad. Sumar ambos como independientes cuenta lo mismo dos veces.
>
> El **DEMATEL** (Gabus & Fontela, Battelle) monta la matriz de relación total `T = X(I−X)⁻¹` — que suma influencias directas **e indirectas** de cualquier longitud de camino — y separa: `R+C` = importancia en el sistema; `R−C > 0` = **CAUSA** (palanca: actúa aquí) y `R−C < 0` = **EFECTO** (termómetro: resultado de lo ya hecho).
>
> La columna **Causa raíz** de abajo es el criterio de mayor `R−C` de cada caso: es ahí donde una intervención mueve el sistema entero.

<DataTable data={alavancas} rows=all rowShading=true>
  <Column id=nome title="Caso"/>
  <Column id=n_criterios title="Criterios" fmt=num0/>
  <Column id=n_causas title="Causas" fmt=num0 contentType=colorscale/>
  <Column id=causa_raiz title="🔧 Causa raíz (mayor R−C)"/>
  <Column id=criterio_maior_peso title="Criterio de mayor peso"/>
  <Column id=maior_peso_pct title="Peso (%)" fmt=num1/>
</DataTable>

<BarChart data={alavancas} x=nome y={['n_causas','n_criterios']} type=grouped title="Criterios que son CAUSA en cada caso (palancas frente al total)" yAxisTitle="Critérios" swapXY=true/>

> **Abre un caso** para ver el diagrama causa-efecto completo, la tabla con `R` y `C` separados y la **matriz de relación total** con los enlaces uno a uno.

## 🎲 Matriz BCG — mapa de oportunidades por categoría

> Además de *cuál elegir*, cada categoría tiene un **perfil de oportunidad**: cuántas alternativas son ⭐ Estrella (invertir), 🐄 Vaca (cosechar), ❓ Interrogante (evaluar el premio) y 🐕 Perro (descartar). Una categoría solo de interrogantes es un mercado caro; una llena de vacas es un mercado maduro, donde el dinero decide poco.

<DataTable data={bcg_geral} rows=all rowShading=true>
  <Column id=nome title="Categoría"/>
  <Column id=estrelas title="⭐" fmt=num0 contentType=colorscale/>
  <Column id=vacas title="🐄" fmt=num0 contentType=colorscale/>
  <Column id=interrogacoes title="❓" fmt=num0 contentType=colorscale/>
  <Column id=abacaxis title="🐕" fmt=num0 contentType=colorscale/>
  <Column id=total title="Total" fmt=num0/>
  <Column id=quadrante_do_vencedor title="Cuadrante del 1.º puesto"/>
</DataTable>

## ⚖️ Las diez escuelas de decisión

> Cada método es una **teoría distinta sobre lo que significa "mejor"**, y por eso ejecutamos todos: cuando diez escuelas independientes eligen al mismo ganador, la elección no es un artefacto de un método. Cuando divergen, la divergencia señala dónde está el trade-off real.

| Método | Escola | O que assume | Quando é a ferramenta certa |
|---|---|---|---|
| **AHP-TOPSIS 2n** | Distância à solução ideal | Compensação total entre Criterios | Criterios quantitativos, decisor único |
| **ELECTRE I** | Sobreclasificação | Incomparabilidade é permitida | Triagem: eliminar o que é dominado |
| **ELECTRE II** | Sobreclasificação | Limiares forte e fraco | Ordenação completa com veto |
| **PROMETHEE II** | Sobreclasificação | Preferência gradual (6 funções) | Quando "um pouco melhor" não é "melhor" |
| **MAUT** | Utilidade | Independência aditiva + Aversión al riesgo | Decisão sob incerteza |
| **MCDA-C** | Construtivista | Níveis Neutro/Bom ancorados | Diagnóstico absoluto, não só ranking |
| **VIKOR** | Compromisso | Utilidade do grupo × arrependimento máximo | Quando compensar é inaceitável |
| **TODIM** | Teoria dos Prospectos | Perda dói mais que ganho equivalente | Decisor avesso a perda (todos são) |
| **SAPEVO-M** | Ordinal multidecisor | Julgamento ordinal de vários decisores | Comitê que não concorda entre si |

## 🎯 Robustez — el intervalo de confianza de la propia decisión

> **El problema.** Todo método MCDM devuelve un ganador con confianza implícita del 100%. Pero los pesos nunca son exactos — son estimaciones de preferencia. Si dos puntos porcentuales en el peso de un criterio intercambian el 1.º con el 2.º, el "ganador" es un artefacto de la calibración, no un hecho del conjunto. Nadie informa de esto. **Es donde las decisiones mueren en el comité.**
>
> **La solución.** Perturbamos los pesos con `w' ~ Dirichlet(κ·w)` y reordenamos 2.000 veces. La Dirichlet es la elección natural: su soporte es exactamente el simplex (pesos positivos que suman 1) y satisface `E[w'] = w` — perturbamos **sin sesgar**. Con κ = 200, un peso del 13% oscila ±2,4 p.p.
>
> El veredicto deja de ser *"el Modelo C es el mejor"* y pasa a ser **"el Modelo C gana en el 96% de los universos de preferencia plausibles"**.

**Abre un caso de la tabla de arriba** para ver el diagrama causa-efecto, el mapa de las diez escuelas, la matriz BCG y la distribución completa de las posiciones en los 2.000 universos.

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
