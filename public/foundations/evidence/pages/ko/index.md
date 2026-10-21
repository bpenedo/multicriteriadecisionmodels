---
title: MCDM Studio — Decisão Multi기준
---

<div style="text-align:center;">

🌐 [Português](/) · [English](/en/) · [Español](/es/) · [Français](/fr/) · [Deutsch](/de/) · [中文](/zh/) · **한국어** · [हिन्दी](/hi/) · [עברית](/he/) · [Русский](/ru/) · [Svenska](/sv/) · [Suomi](/fi/)

<div style="text-align:center;margin:1.2rem 0 1.6rem;">
  <img src="/img/logo_capa.png" alt="ProfBru" width="200" style="display:inline-block;"/>
  <div style="font-weight:700;margin-top:0.5rem;font-size:1.05rem;">ProfBru © 2026</div>
</div>

_MCDM Studio — Modelos Multi기준 de Decisão · Autor: **ProfBru - Bruno Penedo** © 2026 — 모든 권리 보유 · profbruanbima@gmail.com_

</div>

<!--
  ÍNDICE LEVE, DE PROPÓSITO.
  Só consultas AGREGADAS (uma linha por caso). As tabelas detalhadas — ranking por
  método (3.744 linhas), 의사결정 행렬 (3.514), distribuição (4.230), 견고성 por
  método (4.160) — vivem nas páginas de caso, onde estão filtradas por `id_caso`.
  Carregá-las todas aqui somava ~16 mil linhas e travava o navegador.
-->

```sql casos
select *, '/ko/casos/' || id_caso as link from mcdm.casos
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

# 🎯 다기준 의사결정 — 열 학파, 신뢰구간이 있는 하나의 판정

> **스프레드시트는 계산을 틀리지 않습니다. 질문을 틀립니다.** 가격으로 정렬하면 가장 싼 것이 뽑힙니다. 전문가 점수로 정렬하면 가장 비싼 것이 뽑힙니다. “모든 요건을 충족”으로 거르면 목록이 비기 마련입니다. 세 가지 모두 정작 제기된 질문에는 답하지 않습니다. *서로 모순되는 대안들 가운데 무엇을 고를 것인가 — 그리고 얼마나 확신할 수 있는가?*

이 대시보드는 사례마다 **열 가지 다기준 방법**을 실행하고, 그 사이의 **보르다 합의**로 선정안을 도출한 뒤, **가중치를 2,000번 교란**하여 위원회가 실제로 묻는 단 하나의 질문에 답합니다. *가중치를 조금 다르게 주었더라면?*

<BigValue data={totais} value=casos title="의사결정 사례" fmt=num0/>
<BigValue data={totais} value=alternativas title="평가된 대안" fmt=num0/>
<BigValue data={totais} value=robustos title="견고 판정" fmt=num0/>
<BigValue data={totais} value=frageis title="취약 판정" fmt=num0/>

## 📋 의사결정 사례

> 아무 사례나 클릭하면 **전체 보고서**가 열립니다. DEMATEL 인과 다이어그램, 열 학파 대조도, ELECTRE 핵, TOPSIS 이중 정규화, 보르다 합의, 2,000개 세계에 대한 견고성, BCG 매트릭스, 그리고 의사결정 행렬.

<DataTable data={casos} rows=all rowShading=true link=link>
  <Column id=nome title="사례"/>
  <Column id=dominio title="영역"/>
  <Column id=n_alternativas title="대안" fmt=num0/>
  <Column id=vencedor_rotulo title="🏆 선정안"/>
  <Column id=prob_vitoria title="신뢰도 (%)" fmt=num1 contentType=colorscale/>
  <Column id=classificacao title="판정"/>
</DataTable>

> **판정 읽는 법.** `견고`(≥ 90%) = 선택이 가중치의 미세 조정에 좌우되지 않으므로 위원회에 올릴 수 있습니다. `유력`(60–90%) = 대부분의 시나리오에서 유지되지만 2위가 경쟁력이 있습니다. `취약`(60% 미만) = **1위가 가중치의 산물입니다** — 시스템은 트로피를 내보이는 대신 이 사실을 말합니다.

<BarChart data={resumo_dominio} x=dominio y=casos title="적용 영역별 사례" yAxisTitle="Casos"/>

## 🧮 DEMATEL — 모든 결정의 근본 원인

> 가중치를 주기 전에 거의 아무도 묻지 않는 질문. **기준들이 서로 독립인가?** 거의 그렇지 않습니다. 에너지 소비는 주행거리를 *일으키고*, 장갑은 무게를 *일으키며*, 무게는 기동성 상실을 *일으킵니다*. 이 둘을 독립인 것처럼 더하면 같은 것을 두 번 세는 셈입니다.
>
> **DEMATEL**(Gabus & Fontela, Battelle)은 총관계 행렬 `T = X(I−X)⁻¹`를 만듭니다 — 임의 경로 길이의 직접 **및 간접** 영향을 모두 합산합니다 — 그리고 구분합니다. `R+C` = 시스템 내 중요도, `R−C > 0` = **원인**(레버: 여기를 건드린다), `R−C < 0` = **결과**(온도계: 이미 한 일의 산물).
>
> 아래 **근본 원인** 열은 각 사례에서 `R−C`가 가장 큰 기준입니다. 바로 거기서 하나의 개입이 시스템 전체를 움직입니다.

<DataTable data={alavancas} rows=all rowShading=true>
  <Column id=nome title="사례"/>
  <Column id=n_criterios title="기준" fmt=num0/>
  <Column id=n_causas title="원인" fmt=num0 contentType=colorscale/>
  <Column id=causa_raiz title="🔧 근본 원인(최대 R−C)"/>
  <Column id=criterio_maior_peso title="가중치가 가장 큰 기준"/>
  <Column id=maior_peso_pct title="가중치(%)" fmt=num1/>
</DataTable>

<BarChart data={alavancas} x=nome y={['n_causas','n_criterios']} type=grouped title="각 사례에서 원인인 기준 (총계 대비 레버)" yAxisTitle="Critérios" swapXY=true/>

> **사례를 열면** 전체 인과 다이어그램, `R`과 `C`를 분리한 표, 그리고 연결을 하나하나 보여 주는 **총관계 행렬**을 볼 수 있습니다.

## 🎲 BCG 매트릭스 — 범주별 기회 지도

> *무엇을 고를지* 외에도 각 범주에는 **기회 프로필**이 있습니다. 대안 중 몇 개가 ⭐ 스타(투자), 🐄 캐시카우(수확), ❓ 물음표(상금을 따져볼 대상), 🐕 개(정리)인지입니다. 물음표만 있는 범주는 값비싼 시장이고, 캐시카우로 가득한 범주는 돈이 거의 결정하지 못하는 성숙한 시장입니다.

<DataTable data={bcg_geral} rows=all rowShading=true>
  <Column id=nome title="범주"/>
  <Column id=estrelas title="⭐" fmt=num0 contentType=colorscale/>
  <Column id=vacas title="🐄" fmt=num0 contentType=colorscale/>
  <Column id=interrogacoes title="❓" fmt=num0 contentType=colorscale/>
  <Column id=abacaxis title="🐕" fmt=num0 contentType=colorscale/>
  <Column id=total title="합계" fmt=num0/>
  <Column id=quadrante_do_vencedor title="1위의 사분면"/>
</DataTable>

## ⚖️ 열 개의 의사결정 학파

> 각 방법은 **“더 좋다”가 무엇인지에 대한 서로 다른 이론**이며, 그래서 전부 실행합니다. 열 개의 독립적인 학파가 같은 선정안을 뽑으면 그 선택은 한 방법의 산물이 아닙니다. 갈릴 때는, 그 갈림이 진짜 트레이드오프가 어디인지 가리킵니다.

| Método | Escola | O que assume | Quando é a ferramenta certa |
|---|---|---|---|
| **AHP-TOPSIS 2n** | Distância à solução ideal | Compensação total entre 기준s | 기준 quantitativos, decisor único |
| **ELECTRE I** | 우월함ção | Incomparabilidade é permitida | Triagem: eliminar o que é dominado |
| **ELECTRE II** | 우월함ção | Limiares forte e fraco | Ordenação completa com veto |
| **PROMETHEE II** | 우월함ção | Preferência gradual (6 funções) | Quando "um pouco melhor" não é "melhor" |
| **MAUT** | Utilidade | Independência aditiva + 위험 회피 | Decisão sob incerteza |
| **MCDA-C** | Construtivista | Níveis Neutro/Bom ancorados | Diagnóstico absoluto, não só ranking |
| **VIKOR** | Compromisso | Utilidade do grupo × arrependimento máximo | Quando compensar é inaceitável |
| **TODIM** | Teoria dos Prospectos | Perda dói mais que ganho equivalente | Decisor avesso a perda (todos são) |
| **SAPEVO-M** | Ordinal multidecisor | Julgamento ordinal de vários decisores | Comitê que não concorda entre si |

## 🎯 견고성 — 결정 그 자체의 신뢰구간

> **문제.** 모든 MCDM 방법은 암묵적으로 100% 확신을 지닌 선정안을 내놓습니다. 그러나 가중치는 결코 정확하지 않습니다 — 선호의 추정치입니다. 어떤 기준의 가중치가 2퍼센트포인트 움직여 1위와 2위가 바뀐다면, 그 “선정안”은 집합에 관한 사실이 아니라 보정의 산물입니다. 아무도 이것을 보고하지 않습니다. **결정이 위원회에서 죽는 지점이 바로 여기입니다.**
>
> **해법.** `w' ~ Dirichlet(κ·w)`로 가중치를 교란하고 2,000번 다시 순위를 매깁니다. 디리클레는 자연스러운 선택입니다. 그 지지집합이 정확히 단체(합이 1인 양의 가중치)이고 `E[w'] = w`를 만족하기 때문입니다 — **편향 없이** 교란합니다. κ = 200일 때 13%의 가중치는 ±2.4%p 흔들립니다.
>
> 판정은 더 이상 *“모델 C가 최고다”*가 아니라 **“모델 C는 그럴듯한 선호 세계의 96%에서 승리한다”**가 됩니다.

**위 표에서 사례를 열면** 인과 다이어그램, 열 학파 대조도, BCG 매트릭스, 그리고 2,000개 세계에 걸친 순위의 전체 분포를 볼 수 있습니다.

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
