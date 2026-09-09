---
title: MCDM Studio — Decisão MultiCritère
---

<div style="text-align:center;">

🌐 [Português](/) · [English](/en) · [Español](/es) · **Français** · [Deutsch](/de) · [中文](/zh) · [한국어](/ko) · [हिन्दी](/hi) · [עברית](/he) · [Русский](/ru) · [Svenska](/sv) · [Suomi](/fi)

<div style="text-align:center;margin:1.2rem 0 1.6rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="200" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.5rem;font-size:1.05rem;">ProfBru © 2026</div>
</div>

_MCDM Studio — Modelos MultiCritère de Decisão · Autor: **ProfBru - Bruno Penedo** © 2026 — TOUS DROITS RÉSERVÉS · profbruanbima@gmail.com_

</div>

<!--
  ÍNDICE LEVE, DE PROPÓSITO.
  Só consultas AGREGADAS (uma linha por caso). As tabelas detalhadas — ranking por
  método (3.744 linhas), Matrice de décision (3.514), distribuição (4.230), Robustesse por
  método (4.160) — vivem nas páginas de caso, onde estão filtradas por `id_caso`.
  Carregá-las todas aqui somava ~16 mil linhas e travava o navegador. Ver bugs.md #BUG-028.
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

# 🎯 Decisão MultiCritère — nove escolas, um Verdict com intervalo de confiança

> **A planilha não erra a conta. Ela erra a pergunta.**
> Ordenar por preço elege o mais barato. Ordenar por nota de especialista elege o mais caro.
> Filtrar por "atende a todos os requisitos" costuma esvaziar a lista. Nenhuma das três
> responde à pergunta que foi feita: *entre Alternatives que se contradizem, qual escolher —
> e com que confiança?*

Este painel roda **nove métodos multiCritère** sobre cada caso, tira o vencedor do **consenso
de Borda** entre eles e depois **perturba os pesos 2.000 vezes** para responder à única
pergunta que o comitê realmente faz: *e se a gente tivesse dado um peso um pouco diferente?*

<BigValue data={totais} value=casos title="Casos de decisão" fmt=num0/>
<BigValue data={totais} value=alternativas title="Alternativas avaliadas" fmt=num0/>
<BigValue data={totais} value=robustos title="Vereditos ROBUSTOS" fmt=num0/>
<BigValue data={totais} value=frageis title="Vereditos FRÁGEIS" fmt=num0/>

## 📋 Casos de decisão

> Clique em qualquer caso para abrir o **relatório completo**: diagrama causa-efeito do
> DEMATEL, mapa das nove escolas, núcleo do ELECTRE, dupla normalização do TOPSIS,
> Consensus de Borda, Robustesse sob 2.000 universos, matriz BCG e a Matrice de décision.

<DataTable data={casos} rows=all rowShading=true link=link>
  <Column id=nome title="Caso"/>
  <Column id=dominio title="Domínio"/>
  <Column id=n_alternativas title="Alternativas" fmt=num0/>
  <Column id=vencedor_rotulo title="🏆 Vencedor"/>
  <Column id=prob_vitoria title="Confiança (%)" fmt=num1 contentType=colorscale/>
  <Column id=classificacao title="Veredito"/>
</DataTable>

> **Como ler o Verdict.** `ROBUSTO` (≥ 90%) = a escolha não depende da calibração fina dos
> pesos; pode ir ao comitê. `PROVÁVEL` (60–90%) = se sustenta na maioria dos cenários, mas o
> vice é competitivo. `FRÁGIL` (abaixo de 60%) = **o 1º lugar é artefato dos pesos** — o
> sistema diz isso em vez de exibir um troféu.

<BarChart data={resumo_dominio} x=dominio y=casos title="Casos por domínio de aplicação" yAxisTitle="Casos"/>

## 🧮 DEMATEL — a causa raiz de cada decisão

> A pergunta que quase ninguém faz antes de atribuir pesos: **os Critères são
> independentes?** Quase nunca são. Consumo energético *causa* autonomia; blindagem
> *causa* peso, que *causa* perda de mobilidade. Somar os dois como independentes conta a
> mesma coisa duas vezes.
>
> O **DEMATEL** (Gabus & Fontela, Battelle) monta a matriz de relação total
> `T = X(I−X)⁻¹` — que soma influências diretas **e indiretas** de qualquer comprimento de
> caminho — e separa: `R+C` = importância no sistema; `R−C > 0` = **CAUSA** (alavanca:
> mexa aqui) e `R−C < 0` = **EFEITO** (termômetro: resultado do que já se fez).
>
> A coluna **Causa raiz** abaixo é o Critère de maior `R−C` de cada caso: é nele que uma
> intervenção move o sistema inteiro.

<DataTable data={alavancas} rows=all rowShading=true>
  <Column id=nome title="Caso"/>
  <Column id=n_criterios title="Critérios" fmt=num0/>
  <Column id=n_causas title="Causas" fmt=num0 contentType=colorscale/>
  <Column id=causa_raiz title="🔧 Causa raiz (maior R−C)"/>
  <Column id=criterio_maior_peso title="Critério de maior peso"/>
  <Column id=maior_peso_pct title="Peso (%)" fmt=num1/>
</DataTable>

<BarChart data={alavancas} x=nome y={['n_causas','n_criterios']} type=grouped title="Critérios que são CAUSA em cada caso (alavancas contra o total)" yAxisTitle="Critérios" swapXY=true/>

> **Abra um caso** para ver o diagrama causa-efeito completo, a tabela com `R` e `C`
> separados e a **matriz de relação total** com as ligações uma a uma.

## 🎲 Matriz BCG — mapa de oportunidades por categoria

> Além de *qual escolher*, cada categoria tem um **perfil de oportunidade**: quantas
> Alternatives são ⭐ Estrela (investir), 🐄 Vaca (colher), ❓ Interrogação (avaliar o prêmio)
> e 🐕 Abacaxi (descartar). Uma categoria só de Interrogações é um mercado caro; uma cheia de
> Vacas é um mercado maduro, onde o dinheiro decide pouco.

<DataTable data={bcg_geral} rows=all rowShading=true>
  <Column id=nome title="Categoria"/>
  <Column id=estrelas title="⭐" fmt=num0 contentType=colorscale/>
  <Column id=vacas title="🐄" fmt=num0 contentType=colorscale/>
  <Column id=interrogacoes title="❓" fmt=num0 contentType=colorscale/>
  <Column id=abacaxis title="🐕" fmt=num0 contentType=colorscale/>
  <Column id=total title="Total" fmt=num0/>
  <Column id=quadrante_do_vencedor title="Quadrante do 1º colocado"/>
</DataTable>

## ⚖️ As nove escolas de decisão

> Cada método é uma **teoria diferente sobre o que significa "melhor"**, e é por isso que
> rodamos todos: quando nove escolas independentes elegem o mesmo vencedor, a escolha não é
> artefato de um método. Quando divergem, a divergência aponta onde está o trade-off real.

| Método | Escola | O que assume | Quando é a ferramenta certa |
|---|---|---|---|
| **AHP-TOPSIS 2n** | Distância à solução ideal | Compensação total entre Critères | Critères quantitativos, decisor único |
| **ELECTRE I** | Surclassement | Incomparabilidade é permitida | Triagem: eliminar o que é dominado |
| **ELECTRE II** | Surclassement | Limiares forte e fraco | Ordenação completa com veto |
| **PROMETHEE II** | Surclassement | Preferência gradual (6 funções) | Quando "um pouco melhor" não é "melhor" |
| **MAUT** | Utilidade | Independência aditiva + Aversion au risque | Decisão sob incerteza |
| **MCDA-C** | Construtivista | Níveis Neutro/Bom ancorados | Diagnóstico absoluto, não só ranking |
| **VIKOR** | Compromisso | Utilidade do grupo × arrependimento máximo | Quando compensar é inaceitável |
| **TODIM** | Teoria dos Prospectos | Perda dói mais que ganho equivalente | Decisor avesso a perda (todos são) |
| **SAPEVO-M** | Ordinal multidecisor | Julgamento ordinal de vários decisores | Comitê que não concorda entre si |

## 🎯 Robustesse — o intervalo de confiança da própria decisão

> **O problema.** Todo método MCDM devolve um vencedor com confiança implícita de 100%. Mas
> os pesos nunca são exatos — são estimativas de preferência. Se dois pontos percentuais no
> peso de um Critère trocam o 1º com o 2º colocado, o "vencedor" é artefato da calibração,
> não fato do conjunto. Ninguém reporta isso. **É onde as decisões morrem no comitê.**
>
> **A solução.** Perturbamos os pesos com `w' ~ Dirichlet(κ·w)` e reranqueamos 2.000 vezes.
> A Dirichlet é a escolha natural: seu suporte é exatamente o simplex (pesos positivos que
> somam 1) e ela satisfaz `E[w'] = w` — perturbamos **sem enviesar**. Com κ = 200, um peso de
> 13% oscila ±2,4 p.p.
>
> O Verdict deixa de ser *"o Modelo C é o melhor"* e passa a ser **"o Modelo C vence em 96%
> dos universos de preferência plausíveis"**.

**Abra um caso na tabela acima** para ver o diagrama causa-efeito, o mapa das nove escolas, a
matriz BCG e a distribuição completa das posições nos 2.000 universos.

---

<div style="text-align:center;margin-top:2rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="120" style="display:inline-block;opacity:0.9;"/>
  <div style="font-weight:700;margin-top:0.4rem;">ProfBru © 2026</div>
  <div style="margin-top:0.5rem;font-style:italic;font-size:0.9rem;color:#64748b;">
    MCDM Studio — Modelos MultiCritère de Decisão<br/>
    Autor: <strong>ProfBru - Bruno Penedo</strong> © 2026 — TOUS DROITS RÉSERVÉS<br/>
    profbruanbima@gmail.com
  </div>
</div>
