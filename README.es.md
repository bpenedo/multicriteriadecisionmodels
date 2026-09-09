<!--
MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
-->

<div align="center">

# 🎯 MCDM Studio — Modelos Multicriterio de Decisión

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="820"/>

**ProfBru © 2026**

### Deje de elegir con una hoja de cálculo. Empiece a decidir con pruebas.

**Nueve escuelas de decisión. Un ganador. Y —por primera vez— la probabilidad de que ese ganador sea el correcto.**

[![MCDM](https://img.shields.io/badge/Métodos_MCDM-9-2563eb?style=for-the-badge)](#-las-nueve-escuelas-de-decisión--y-por-qué-nueve)
[![Engines](https://img.shields.io/badge/Motores-Python_+_Rust-c2410c?style=for-the-badge)](#-dos-motores-independientes-la-prueba-cruzada)
[![i18n](https://img.shields.io/badge/Idiomas-12-16a34a?style=for-the-badge)](#-12-idiomas--memoria-de-traducción-sdl-trados)
[![Robustez](https://img.shields.io/badge/Universos_simulados-2.000-8f3d56?style=for-the-badge)](#-la-pregunta-que-nadie-responde-y-si-los-pesos-están-mal)

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Rust](https://img.shields.io/badge/Rust-1.96-000000?logo=rust&logoColor=white)](https://www.rust-lang.org)
[![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?logo=numpy&logoColor=white)](https://numpy.org)
[![Numba](https://img.shields.io/badge/Numba-JIT-00A3E0?logo=numba&logoColor=white)](https://numba.pydata.org)
[![Evidence](https://img.shields.io/badge/Evidence.dev-Dashboard-f4b548)](https://evidence.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/Licencia-Propietaria-red)](#-licencia-y-autoría)

🌐 [Português](README.md) · [English](README.en.md) · **Español** · [Français](README.fr.md) · [Deutsch](README.de.md) · [中文](README.zh.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [עברית](README.he.md) · [Русский](README.ru.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md)

</div>

---

## 💀 El dolor: usted ya ha perdido dinero por culpa de una hoja de cálculo

Piense en la última decisión cara que tomó. Comprar el coche. Elegir el proveedor. Aprobar el proyecto. Definir el portátil que 200 personas usarán durante cuatro años.

**Abrió una hoja de cálculo. Las opciones en las filas, los atributos en las columnas. Y entonces hizo una de estas tres cosas:**

| Lo que hizo | Lo que realmente pasó |
|---|---|
| 🔻 **Ordenó por la columna del precio** | Eligió el más barato. No necesitaba una hoja de cálculo para eso. |
| 🔺 **Ordenó por la nota del experto** | Eligió el más caro. Tampoco lo necesitaba. |
| 🔍 **Filtró por «cumple todos los requisitos»** | La lista quedó vacía. Entonces relajó un requisito. ¿Cuál? **El que estorbaba.** |

> [!WARNING]
> **Las tres operaciones tienen el mismo defecto: ninguna responde a la pregunta que usted hizo.**
> La pregunta era *«entre opciones que se contradicen, ¿cuál elegir?»* — y ordenar por una columna es, por definición, decidir por **un** criterio. No usó los otros siete. Estaban ahí solo para que usted se sintiera mejor.

Y está el problema que nadie ve: **sumó cosas que ya estaban sumadas.** Dio un peso del 20 % al «consumo energético» y del 25 % a la «autonomía» — pero el consumo *causa* la autonomía. Contó lo mismo dos veces y lo llamó análisis.

### El momento en que la decisión muere

Ocurre en la reunión. Usted presenta el ranking. Alguien del comité pregunta:

> *¿Y si la autonomía valiera un 30 % en lugar de un 25 %?*

Y usted no lo sabe. **Nadie lo sabe.** Porque la hoja de cálculo devuelve **un** número, con una confianza implícita del 100 % que no tiene forma de tener. Vuelve con los deberes hechos, ajusta los pesos y descubre que el segundo se convierte en primero con **dos puntos porcentuales** de diferencia.

Aquel «ganador» nunca fue un ganador. Era un **artefacto de su calibración** — y usted casi lo firma.

---

## 💊 La solución: nueve escuelas, un consenso y un intervalo de confianza

**MCDM Studio ejecuta **nueve métodos multicriterio** consagrados sobre el mismo problema, extrae el ganador del **consenso** entre ellos y luego hace lo único que realmente importa:**

> ### 🎲 Perturba los pesos **2.000 veces** y cuenta en cuántos universos el ganador sigue ganando.

El veredicto deja de ser un número y pasa a ser una **frase que sobrevive al comité**:

<div align="center">

| ❌ Lo que dice la hoja de cálculo | ✅ Lo que dice MCDM Studio |
|---|---|
| «El Modelo C es el mejor.» | **«El Modelo C gana en el 96 % de los universos de preferencia plausibles. Veredicto ROBUSTO: la elección no depende del ajuste fino de los pesos.»** |
| *(sin respuesta)* | **«El Modelo A gana en el 51 %. Veredicto FRÁGIL: el primer puesto es un artefacto de los pesos. No decida solo por el ranking.»** |

</div>

**Fíjese en el segundo caso. Un sistema honesto tiene que ser capaz de decir *«no confíe en mí aquí»*. Esa es la diferencia entre apoyo a la decisión y un generador de justificaciones para la decisión que ya quería tomar.**

---

## 🖼️ Véalo funcionando

### 1. Qué es causa y qué es efecto — antes de cualquier peso

<div align="center"><img src="docs/telas/caca_multifuncao/dematel_causa_efeito.png" alt="DEMATEL" width="820"/></div>

**El dolor que esto resuelve:** usted asigna pesos suponiendo que los criterios son independientes. **Casi nunca lo son.** El consumo energético *causa* la autonomía. El blindaje *causa* peso, que *causa* pérdida de movilidad. Sumarlos como independientes es contar dos veces.

**DEMATEL** construye la matriz de relación total `T = X(I−X)⁻¹` — que suma influencias directas **e indirectas**, de cualquier longitud de camino — y separa lo que usted puede **mover** (causas, por encima de la línea) de lo que solo **mide el resultado** (efectos, por debajo). Los pesos salen de ahí: por influencia sistémica, no por corazonada.

> En el caso anterior, **Transferencia de Tecnología** y **Firma Radar** son CAUSAS: moverlas mueve todo el sistema. **Disponibilidad de flota** es EFECTO — es termómetro, no palanca. Un pliego que puntúa disponibilidad e ignora la ToT está midiendo la fiebre e ignorando la infección.

### 2. Nueve escuelas sobre el mismo problema

<div align="center"><img src="docs/telas/veiculo_eletrico/mapa_metodos.png" alt="Métodos" width="900"/></div>

**El dolor que esto resuelve:** todo método MCDM lleva incorporada una teoría sobre qué significa «mejor» — y esa teoría cambia al ganador. Elegir un método y presentar el resultado es elegir el resultado.

Ejecutamos los nueve. Cuando coinciden, la elección **no es un artefacto del método**. Cuando divergen, **la divergencia es el hallazgo**.

> Arriba: el **Híbrido enchufable** es 1.º en siete métodos, pero **6.º en ELECTRE I**. No es ruido — es información. ELECTRE I permite el *veto*: dice que el híbrido tiene una desventaja lo bastante grave en algún criterio como para ser eliminado, por bueno que sea en el resto. **Esa es exactamente la pregunta que quiere llevar al comité.**

### 3. El intervalo de confianza de la propia decisión

<div align="center"><img src="docs/telas/portfolio_startup/robustez.png" alt="Robustez" width="820"/></div>

**El dolor que esto resuelve:** la pregunta del comité — *«¿y si el peso fuera otro?»*. Respondida **antes** de que alguien pregunte.

Perturbamos los pesos con `w' ~ Dirichlet(κ·w)` y reordenamos 2.000 veces. La Dirichlet es la elección natural: su soporte es exactamente el símplex (pesos positivos que suman 1) y satisface `E[w'] = w` — perturbamos **sin sesgar**.

### 4. Dónde se equivoca su intuición

<div align="center"><img src="docs/telas/blindado/pesos_dematel_ahp.png" alt="DEMATEL x AHP" width="820"/></div>

**El dolor que esto resuelve:** usted cree que sabe qué es importante. Dos familias de pesos lo ponen a prueba.

El **AHP** (Saaty) pregunta, par a par, cuánto más importa un criterio que otro. El **DEMATEL** mide la influencia sistémica. **Donde divergen está el efecto de segundo orden que usted subestimó** — y el gráfico marca la mayor divergencia en rojo.

### 5. Dónde termina cada alternativa, en 2.000 escenarios

<div align="center"><img src="docs/telas/estacao_trabalho/distribuicao_posicoes.png" alt="Distribuição" width="820"/></div>

Una barra completamente verde es una posición que **no depende de los pesos**. Una barra moteada es una posición en disputa. Ve de un vistazo dónde el ranking es un hecho y dónde es una opinión.

---

## 🎯 Para qué sirve — la elección a medida

El motor es **agnóstico de dominio**: la unidad es el *caso de decisión* (alternativas × criterios), sin semántica de negocio incorporada. Cambiar de dominio es cambiar datos, no código.

<div align="center">

| Dominio | La decisión | El dolor específico |
|---|---|---|
| 📱 **Electrónica** | Móvil, portátil, equipamiento | El más barato tiene la peor cámara; el de mejor cámara tiene la peor batería. No existe «el mejor» — existe **el mejor para su uso**. |
| 🚗 **Coches eléctricos** | Flota o uso personal | Autonomía, recarga, red de asistencia y reventa tiran en direcciones opuestas. Y el criterio decisivo (**autonomía real**, no la de catálogo) es el más difícil de medir. |
| 🎖️ **Defensa** | Cazas, blindados, drones, base logística | Ciclo de vida de 30 años, irreversible, bajo escrutinio público. **El precio unitario es menos de 1/3 del coste total.** La transferencia de tecnología y el coste por hora deciden el presupuesto de tres décadas. |
| 🏢 **Corporativo** | Proveedor, ERP, externalización, expansión | Un comité que no se pone de acuerdo consigo mismo. **SAPEVO-M** se hizo exactamente para eso: agrega el juicio ordinal de **varios decisores** sin exigir consenso previo. |
| 🚀 **Startups** | Cartera de proyectos, asignación de capital | Quien decide por retorno esperado siempre elige la apuesta más arriesgada — **el valor esperado ignora la cola**. Aquí el riesgo es **criterio**, no una nota al pie de la diapositiva 14. |
| 💻 **TI** | Estandarización del parque | La decisión se multiplica por 200 y dura 4 años. La autonomía y la garantía in situ valen más, en el coste total de propiedad, que dos puntos de benchmark sintético. |

</div>

### Casos listos para ejecutar

```bash
python3 pipeline.py --listar
```

| # | Caso | Dominio | Alternativas | Criterios | Veredicto |
|--:|---|---|--:|--:|---|
| 1 | `smartphone` | consumo | 6 | 8 | PROBABLE 85% |
| 2 | `veiculo_eletrico` | automoción | 7 | 8 | ROBUSTO 96% |
| 3 | `caca_multifuncao` | defensa | 6 | 9 | ROBUSTO 100% |
| 4 | `blindado` | defensa | 5 | 8 | ROBUSTO 90% |
| 5 | `portfolio_startup` | corporativo | 7 | 9 | ROBUSTO 97% |
| 6 | `estacao_trabalho` | TI | 6 | 8 | ROBUSTO 98% |
| 7 | `carros_eletricos` | automoción | 38 | 9 | ROBUSTO 99% |
| 8 | `smartphones_2026` | consumo | 38 | 9 | PROBABLE 65% |
| 9 | `tablets` | consumo | 34 | 8 | PROBABLE 62% |
| 10 | `smartwatches` | consumo | 31 | 8 | PROBABLE 79% |
| 11 | `notebooks` | TI | 32 | 8 | PROBABLE 76% |
| 12 | `maquinario_agricola` | agronegocio | 35 | 8 | ROBUSTO 100% |
| 13 | `sbc_iot` | TI | 33 | 8 | ROBUSTO 100% |
| 14 | `mineracao_asic` | infraestructura | 31 | 8 | FRÁGIL 51% |
| 15 | `minipcs` | TI | 10 | 8 | ROBUSTO 96% |
| 16 | `impressoras_3d_miniaturas` | manufactura | 30 | 9 | FRÁGIL 35% |
| 17 | `impressoras_3d_producao` | manufactura | 30 | 9 | FRÁGIL 45% |
| 18 | `plotters_formato` | manufactura | 24 | 9 | PROBABLE 86% |
| 19 | `impressoras_3d_miniaturas_triadas` | manufactura | 13 | 9 | ROBUSTO 100% |
| 20 | `acoes_b3` 📚 | financiero | 20 | 7 | FRÁGIL 52% |
| 21 | `fundos_imobiliarios` 📚 | financiero | 18 | 8 | PROBABLE 61% |
| 22 | `fintech` 📚 | financiero | 16 | 8 | PROBABLE 78% |
| 23 | `avaliacao_imoveis` 📚 | inmobiliario | 16 | 8 | ROBUSTO 96% |
| 24 | `ordens_servico` 📚 | operaciones | 18 | 8 | ROBUSTO 92% |
| 25 | `cloud_providers` 📚 | TI | 14 | 8 | ROBUSTO 100% |
| 26 | `venture_capital` 📚 | corporativo | 16 | 8 | ROBUSTO 97% |
| 27 | `instrutores` 📚 | corporativo | 15 | 8 | ROBUSTO 100% |

> [!NOTE]
> Las matrices de los casos son **ilustrativas** — órdenes de magnitud públicos y plausibles, para demostrar el método. Lo que **no** es ilustrativo es el **modelado**: criterios, direcciones, matriz causal del DEMATEL y matriz de Saaty. Ahí reside el valor. **Sustituya los números por su cotización, su pliego o su ensayo de laboratorio** — el motor es el mismo; los datos son suyos.

> [!TIP]
> El **veredicto** mide en cuántos de los 2.000 universos de preferencia simulados el ganador sigue ganando, perturbando los pesos por Dirichlet (κ=200). **ROBUSTO** ≥ 90%: la elección no depende de la calibración. **PROBABLE** 60–89%: el segundo es competitivo, compare ambos. **FRÁGIL** < 60%: el primer puesto es un artefacto de los pesos — y eso es un hallazgo legítimo, no un fallo. Significa que los datos no deciden, y la decisión vuelve al humano.

### 📚 Estudios de caso derivados de la literatura

> [!IMPORTANT]
> Ocho de los casos tienen sus **criterios y estructura causal extraídos de artículos y tesis revisados** — acciones, fondos inmobiliarios, fintechs, tasación de inmuebles, órdenes de trabajo, proveedores de nube, capital de riesgo y ordenación de instructores. Los criterios no fueron inventados: provienen del texto de origen, y la autoría de cada trabajo se preserva en la cabecera del módulo correspondiente. Las **matrices numéricas** son instanciaciones propias — no se reprodujo ningún dato de los trabajos originales.

| Caso | Dominio | Referencia y autoría |
|---|---|---|
| `acoes_b3` | financiero | COSTA, L. S. *Uma metodologia para a pré-seleção de ações utilizando o método multicritério TOPSIS*; *AHP–TOPSIS Methodology for Stock Portfolio Investments*, Risks 10(4):4, 2022 |
| `fundos_imobiliarios` | financiero | SANTOS, V. V. *TCC*, Engenharia da Computação, UFPE |
| `fintech` | financiero | *A Fuzzy Multicriteria Group Decision Making Approach for Evaluating and Selecting Fintech Projects* |
| `avaliacao_imoveis` | inmobiliario | DUARTE, D. C. O. *Análise multicritério e geoestatística aplicadas na avaliação de imóveis*; MARQUES, J. P. M. |
| `ordens_servico` | operaciones | *Priorização de ordens de serviço: o AHP integrado ao PROMETHEE*. Revista Produção Online, v.22, n.2, 2022 |
| `cloud_providers` | TI | SOLOMON. *Ranking of Cloud Service Providers Using a Dynamic TOPSIS Model*. The George Washington University |
| `venture_capital` | corporativo | BEIM, G.; LÉVESQUE, M.; DHOCHAK, M. et al. (2019); AFFUL-DADZIE, E. et al.; MILKOVA/ANDREICHIKOV (IJAHP) |
| `instrutores` | corporativo | *Modelagem matemática com os métodos AHP e TOPSIS para ordenação de instrutores em uma escola da FAB*. LIV SBPO, 2022 |

---

## ⚡ Instalación

### Camino más rápido (Python)

```bash
git clone <url> multicriteriadecisionmodels
cd multicriteriadecisionmodels/public/foundations/pipeline
pip install -r requirements.txt
python3 pipeline.py
```

Listo. Los seis casos se ejecutan, con informe completo.

<details>
<summary><b>Requisitos detallados</b></summary>

| Componente | Versión mínima | ¿Obligatorio? | Para qué |
|---|---|---|---|
| Python | 3.10 | ✅ | motor de referencia |
| NumPy | 2.0 | ✅ | álgebra de todos los métodos |
| numba | 0.60 | ⚠️ | JIT de los kernels — sin él funciona igual, más lento |
| SciPy | 1.10 | ✅ | estadística auxiliar |
| matplotlib | 3.7 | ✅ | las 5 pantallas por caso |
| Rust / cargo | 1.75 | ⭕ | motor de verificación cruzada |
| Node.js | 18 | ⭕ | dashboard Evidence |
| screen | — | ⭕ | ejecución en segundo plano |

</details>

### Cadena completa

```bash
./run_all.sh                    # pruebas → pipeline → pantallas → i18n → Rust → cotejo
./run_all.sh --rapido           # omite Rust e i18n
./run_all.sh --caso smartphone  # un solo caso
./run_all.sh --background       # ejecuta en screen (reanudar: screen -r mcdm)
```

### Motor Rust — binario sin runtime

```bash
cd public/foundations/rust/mcdm_core
cargo test --release
cargo build --release

./target/release/mcdm --exemplo > problema.mcdm
./target/release/mcdm problema.mcdm
./target/release/mcdm problema.mcdm --json
```

### Dashboard

```bash
cd public/foundations/evidence
npm install
npm run dev               # http://localhost:3000
```

<details>
<summary><b>Comandos avanzados</b></summary>

```bash
python3 pipeline.py caca_multifuncao --workers 8 --iter 5000
python3 testes_nucleo.py
python3 exportar_rust.py
python3 gerar_i18n.py --tudo
python3 gerar_i18n.py --verificar
python3 gerar_graficos.py --workers 6
```

| Variable | Predeterminado | Efecto |
|---|---|---|
| `MCDM_WORKERS` | auto | procesos del `ProcessPoolExecutor` |
| `MCDM_NUMBA` | `1` | JIT activado; `0` para depurar en NumPy puro |
| `MCDM_SEED` | `42` | reproducibilidad |
| `ROBUSTEZ_ITER` | `2000` | universos de preferencia |
| `ROBUSTEZ_KAPPA` | `200` | concentración de la Dirichlet (mayor = pesos más fieles) |
| `MAUT_AVERSAO` | `2.0` | aversión al riesgo (r > 0 = cóncava) |
| `PROMETHEE_TIPO` | `linear` | función de preferencia (6 disponibles) |

</details>

---

## ⚖️ Las nueve escuelas de decisión — y por qué nueve

> [!IMPORTANT]
> **Cada método es una teoría distinta sobre qué significa «mejor».** Usar uno solo es elegir la respuesta junto con la pregunta. Ejecutamos los nueve porque la **coincidencia entre teorías independientes** es la evidencia más fuerte que admite un problema de decisión.

<div align="center">

| Método | Escuela | Qué asume | Cuándo es **la** herramienta correcta | Origen |
|---|---|---|---|---|
| **AHP-TOPSIS 2n** | distancia al ideal | compensación total | criterios cuantitativos, decisor único | Saaty (1980); Hwang & Yoon (1981) |
| **ELECTRE I** | sobreclasificación | se permite la incomparabilidad | **cribado**: eliminar lo dominado | Roy (1968) |
| **ELECTRE II** | sobreclasificación | umbrales fuerte y débil | ordenación completa **con veto** | Roy & Bertier (1971) |
| **PROMETHEE II** | sobreclasificación | preferencia gradual (6 funciones) | cuando «algo mejor» ≠ «mejor» | Brans & Vincke (1985) |
| **MAUT** | utilidad | independencia aditiva + aversión al riesgo | decisión bajo incertidumbre | Keeney & Raiffa (1976) |
| **MCDA-C** | constructivista | niveles Neutro/Bueno anclados | **diagnóstico absoluto**, no solo ranking | Ensslin, Montibeller & Noronha (2001) |
| **VIKOR** | compromiso | utilidad del grupo × arrepentimiento máximo | cuando **compensar es inaceptable** | Opricovic (1979); Opricovic & Tzeng (2002-07) |
| **TODIM** | Teoría de las Perspectivas | la pérdida duele más que la ganancia equivalente | decisor averso a la pérdida — **todos lo son** | Gomes & Lima (1992); Kahneman & Tversky (1979) |
| **SAPEVO-M** | ordinal multidecisor | juicio ordinal de varios decisores | **comité que no se pone de acuerdo** | Gomes et al. (1997); Teixeira, Santos & Gomes (2019) |

</div>

<details>
<summary><b>Por qué estos tres merecen atención especial</b></summary>

### VIKOR — cuando compensar es inaceptable
VIKOR calcula **dos** medidas: `S` (utilidad del grupo — suma ponderada, que **acepta** que un desempeño pésimo se compense con varios buenos) y `R` (arrepentimiento individual máximo — minimax, que **rechaza** la compensación).

Un blindado con movilidad excelente y protección pésima tiene un `S` óptimo y un `R` terrible. La suma ponderada lo elegiría; VIKOR lo señala. Y cuando `S` y `R` discrepan, las condiciones **C1** (ventaja aceptable) y **C2** (estabilidad aceptable) informan explícitamente de que la decisión tiene un punto ciego.

### TODIM — la pérdida duele más que la ganancia
Basado en la **Teoría de las Perspectivas** de Kahneman y Tversky: perder 10 puntos de autonomía duele más de lo que agrada ganar 10. La suma ponderada clásica ignora esa asimetría y trata ganancia y pérdida como simétricas — **algo que ningún decisor humano hace.** El factor `θ` calibra cuánto: `θ < 1` amplifica la aversión a la pérdida.

### SAPEVO-M — el comité que no se pone de acuerdo
Todos los demás métodos exigen un vector de pesos. **¿De dónde sale cuando hay cinco decisores con opiniones distintas?** SAPEVO-M lo resuelve en el origen: cada decisor expresa una preferencia **ordinal** («la autonomía es mucho más importante que el precio», en una escala de siete puntos), y el método agrega **sin exigir un orden previo de consenso**. Así es como se expresa realmente un comité — nadie dice «la autonomía vale 0,237».

</details>

### El motor de consenso

```
DEMATEL ──► pesos por influencia ──► 9 métodos ──► consenso de Borda ──► ganador
                                                    │
                        2.000 universos de Dirichlet ─────────────────┘
                                    ▼
                     veredicto: ROBUSTO / PROVÁVEL / FRÁGIL
```

| Veredicto | Confianza | Qué hacer |
|---|---|---|
| 🟢 **ROBUSTO** | ≥ 90% | La elección no depende del ajuste fino. **Puede llevarla al comité.** |
| 🟡 **PROBABLE** | 60–90% | Se sostiene en la mayoría de los escenarios, pero el segundo es competitivo. **Compare ambos.** |
| 🔴 **FRÁGIL** | < 60% | El primer puesto es un **artefacto de los pesos**. No decida solo por el ranking: vuelva al decisor y recalibre. |

---

## 🔬 Dos motores independientes: la prueba cruzada

> [!TIP]
> **¿Por qué reimplementarlo todo en Rust?** Porque «el código funciona» no es evidencia de que las **matemáticas** sean correctas.

Un error de transcripción de fórmula rara vez se repite **idéntico** en dos lenguajes con álgebra lineal independiente. El motor Python usa NumPy/LAPACK; el motor Rust implementa eliminación gaussiana con pivoteo parcial y el método de las potencias **a mano, sin dependencia externa alguna**.

```bash
python3 exportar_rust.py
```
```
✅ smartphone           8 métodos idénticos · ganador=C     (Δ ≤ 4.7e-11)
✅ veiculo_eletrico     8 métodos idénticos · ganador=EV6   (Δ ≤ 4.1e-11)
✅ caca_multifuncao     8 métodos idénticos · ganador=C3    (Δ ≤ 4.5e-11)
✅ blindado             8 métodos idénticos · ganador=B3    (Δ ≤ 4.6e-11)
✅ portfolio_startup    8 métodos idénticos · ganador=P3    (Δ ≤ 4.9e-11)
✅ estacao_trabalho     8 métodos idénticos · ganador=W5    (Δ ≤ 5.0e-11)
```

**Extra: el binario Rust no necesita Python, NumPy, numba ni entorno virtual. Unos pocos MB que se ejecutan en servidor, contenedor o máquina embebida — lo que importa cuando el motor acompaña a un sistema en campo.**

---

## 🚀 Rendimiento: 26× más rápido, la misma respuesta

El análisis de robustez ejecuta 2.000 universos × 9 métodos. La implementación ingenua tardaba **42 segundos** por caso.

<div align="center">

| Etapa | Tiempo | Mejora |
|---|---|---|
| Kernels JIT por universo | 42,33 s | — |
| **Precompilación en tensores** | 2,41 s | **17,6×** |
| `ranks` bajo JIT + estado por proceso | **1,63 s** | **26,0×** |

</div>

> **La optimización más rentable no fue el paralelismo ni el JIT.** Fue darse cuenta de que cuatro de los nueve métodos son **lineales en el vector de pesos** — lo que permite precomputar tensores y reducir cada universo a un producto matriz-vector. **Álgebra antes que infraestructura.**

Y el resultado es **idéntico bit a bit** al camino lento — 100 universos × 9 métodos verificados en cada ejecución de la suite. Una optimización que cambia el resultado es un fallo, no una mejora.

<details>
<summary><b>Política de ejecución del proyecto</b></summary>

| Regla | Aplicación |
|---|---|
| **Paralelismo** | `ProcessPoolExecutor` para trabajo CPU-bound; nunca hilos (el GIL serializa) |
| **Umbral** | Serie frente a paralelo decidido por el **trabajo** (`n_iter · m² · k`), no por el número de elementos — paralelizar un problema pequeño es **más lento** que resolverlo |
| **JIT** | `numba` con `cache=True` en los kernels O(m²k); degrada a NumPy puro si falta |
| **Segundo plano** | `screen`, nunca `nohup` — permite reanudar e interactuar |
| **Reproducibilidad** | Partición fija e independiente del nº de procesos: misma semilla → resultado idéntico con 1 o 32 procesos |

</details>

---

## 🌐 12 idiomas — memoria de traducción SDL Trados

No es traducir automáticamente un README. Es un **pipeline de localización** con memoria de traducción en el estándar **SDL Trados Studio**.

```
translation.memory.md          ← fuente canónica, versionada en git
   │  --tm
   ▼
strings.<locale>.json          ← artefacto consumido
   │  --paginas
   ▼
12 páginas del dashboard + 12 READMEs
   │  --tmx
   ▼
translation.memory.tmx         ← importable en SDL Trados Studio
```

| Elemento | Números |
|---|---|
| Locales | **12** (pt-BR · en · es · fr · de · zh · ko · hi · **he RTL** · ru · sv · fi) |
| Unidades de traducción | 56 |
| Términos de glosario (MultiTerm) | 22 |
| Segmentos en el TMX | **948** |
| Codificación | UTF-8 · LF · NFC |

```bash
python3 gerar_i18n.py --verificar
```

El QA replica el **Verify** de Trados: consistencia terminológica, placeables preservados, cobertura de segmento, codificación estricta y no traducibles intactos — con una regla diferenciada por sistema de escritura (las siglas técnicas permanecen en latino en cualquier idioma; los nombres propios se **transliteran** donde la escritura no es latina).

---

## 📁 Qué hay dentro

```
multicriteriadecisionmodels/
├── README.md (+11)                     escaparate en 12 idiomas
├── docs/                               logo y pantallas de los READMEs
│
└── public/foundations/
    ├── pipeline/                       MOTOR PYTHON (referencia)
    │   ├── nucleo.py                   DEMATEL · ELECTRE I/II · PROMETHEE II
    │   │                               MAUT · MCDA-C · AHP · TOPSIS 2N
    │   ├── metodos_br.py               SAPEVO-M · VIKOR · TODIM · Copeland
    │   ├── robustez.py                 Dirichlet + ProcessPoolExecutor
    │   ├── pipeline.py                 orquestador
    │   ├── gerar_graficos.py           5 pantallas por caso
    │   ├── gerar_i18n.py               TM → strings → páginas → TMX
    │   ├── testes_nucleo.py            16 verificaciones matemáticas
    │   ├── exportar_rust.py            cotejo entre motores
    │   ├── casos/catalogo.py           6 casos + validación
    │   └── run_all.sh                  cadena (screen)
    │
    ├── rust/mcdm_core/                 MOTOR RUST (verificación + distribución)
    │   └── src/lib.rs                  todos los métodos, cero dependencias
    │
    └── evidence/                       DASHBOARD (Evidence.dev)
        ├── sources/mcdm/               11 consultas SQL
        └── pages/                      12 rutas de idioma
```

---

## 🧠 Fundamentación

El proyecto se construye sobre literatura revisada, no sobre intuición. La arquitectura de integración sigue a **John (2025)**, *«Integration of DEMATEL with Other MCDM Methods for Comprehensive Techno-Economic Analysis»*: el DEMATEL revela la estructura causal y deriva **pesos por influencia**, que luego alimentan los métodos de ordenación — en lugar de pesos arbitrados.

Los métodos de la **escuela brasileña de Apoyo Multicriterio a la Decisión** (SAPEVO-M, TODIM-FSE, ELECTRE II, VIKOR, métodos ordinales) siguen los trabajos del **IME**, **UFF**, **CASNAV**, **AMAN** y **FURB** — incluidas aplicaciones reales en **evaluación de drones para la guerra naval**, **clasificación de base logística de brigada** y **ordenación de corbetas para la Marina de Brasil**.

> [!NOTE]
> **La autoría de los métodos corresponde íntegramente a sus creadores,** acreditados individualmente en las cabeceras de `nucleo.py` y `metodos_br.py`. De este proyecto son la implementación, la integración y el motor de consenso — **no los métodos**.

---

## ❓ Preguntas que usted va a hacer

<details>
<summary><b>Ya uso una matriz de decisión ponderada. ¿No es lo mismo?</b></summary>

No, por tres razones. **(1)** Una matriz ponderada es **un** método (suma ponderada), con una teoría incorporada: compensación total. Asume que un desempeño pésimo en un criterio puede compensarse con un buen desempeño en otros — algo falso en seguridad, en protección blindada y en cumplimiento normativo. **(2)** Asume criterios independientes, y usted casi siempre suma cosas que ya están sumadas. **(3)** Devuelve un número sin intervalo de confianza, y por eso no sobrevive a la primera pregunta del comité.
</details>

<details>
<summary><b>¿Cómo elijo los pesos?</b></summary>

No los elige — **tres caminos los derivan**. El **DEMATEL** los extrae de la estructura causal que usted declara (quién influye sobre quién). El **AHP** los extrae de comparaciones par a par, con una verificación de consistencia que **rechaza** el juicio contradictorio. El **SAPEVO-M** los extrae del juicio ordinal de varios decisores. Y después de eso, el análisis de robustez pregunta cuánto **depende** todavía el resultado de ellos.
</details>

<details>
<summary><b>¿Y si mi problema tiene 200 alternativas?</b></summary>

Funciona. El umbral de paralelismo detecta el régimen y distribuye en procesos. Medido: 60 alternativas × 12 criterios × 2.000 universos en 3,8 s con 4 procesos. Por encima de unas 700 alternativas el tensor de preferencia supera el límite de memoria configurado y el motor avisa, en lugar de bloquearse.
</details>

<details>
<summary><b>Los métodos discreparon. ¿Y ahora?</b></summary>

**Eso es el producto, no el problema.** La divergencia dice que su decisión es sensible a la escuela adoptada — y nombra cuál. Si ELECTRE degrada a quien todos los demás eligen, existe un criterio en el que esa alternativa es lo bastante grave como para vetarla. Lleve **eso** al comité, no el ranking.
</details>

<details>
<summary><b>¿Puedo usar mis propios datos?</b></summary>

Para eso sirve. Un caso es una estructura declarativa en `casos/catalogo.py`: criterios (con dirección y unidad), alternativas, matriz de decisión, matriz causal del DEMATEL y matriz de Saaty. El validador rechaza un caso mal formado **antes** de cualquier cálculo — dimensiones incoherentes, diagonal errónea, matriz de Saaty no recíproca, criterio constante que no discrimina nada.
</details>

---

## 📜 Licencia y autoría

<div align="center">

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="420"/>

**ProfBru © 2026**

**MCDM Studio — Modelos Multicriterio de Decisión**
Autor: **ProfBru - Bruno Penedo** © 2026 — **TODOS LOS DERECHOS RESERVADOS**
📧 profbruanbima@gmail.com

</div>

Proyecto **propietario**. Este repositorio no concede licencia de uso, copia, modificación, distribución ni obra derivada. El uso comercial, académico o institucional requiere autorización escrita del autor.

**Atribución de terceros:** los métodos multicriterio son autoría de sus respectivos creadores — Saaty, Roy, Bertier, Brans, Vincke, Keeney, Raiffa, Ensslin, Montibeller, Noronha, Gabus, Fontela, Opricovic, Tzeng, Hwang, Yoon, Kahneman, Tversky, Borda, Copeland, Gomes, Lima, Santos, Teixeira, Moreira, Rangel, Neves, Hein, Kroenke, Keunecke y Gomes Júnior — acreditados individualmente en el código fuente.
