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

🌐 [Português](/casos/{params.caso}) · [English](/en/casos/{params.caso}) · [Español](/es/casos/{params.caso}) · **Français** · [Deutsch](/de/casos/{params.caso}) · [中文](/zh/casos/{params.caso}) · [한국어](/ko/casos/{params.caso}) · [हिन्दी](/hi/casos/{params.caso}) · [עברית](/he/casos/{params.caso}) · [Русский](/ru/casos/{params.caso}) · [Svenska](/sv/casos/{params.caso}) · [Suomi](/fi/casos/{params.caso})

# {caso[0].nome}

> **{caso[0].descricao}**
>
> _Décideur modélisé : {caso[0].decisor} · Domaine : {caso[0].dominio}_

<BigValue data={caso} value=vencedor_rotulo title="🏆 Gagnant du consensus"/>
<BigValue data={caso} value=prob_vitoria title="Gagne dans (% des univers)" fmt=num1/>
<BigValue data={caso} value=classificacao title="Verdict"/>
<BigValue data={caso} value=n_alternativas title="Alternatives" fmt=num0/>
<BigValue data={caso} value=n_metodos title="Méthodes qui classent" fmt=num0/>
<BigValue data={caso} value=n_modelos title="Modèles appliqués" fmt=num0/>

---

## 🧮 DEMATEL — quels critères sont causes et lesquels sont effets

> Antes de qualquer peso: **os Critères não são independentes**. O DEMATEL monta a matriz de relação total `T = X(I−X)⁻¹` — somando influência direta **e indireta** de qualquer comprimento de caminho — e separa o que você pode **puxar** (CAUSA) do que apenas **mede o resultado** (EFEITO). Os pesos saem daí, por influência sistêmica.

<img src="/mc/{params.caso}/dematel_cause_effet.png" alt="Diagrama cause-effet DEMATEL" style="width:100%;border-radius:8px;"/>

<DataTable data={dematel_c} rows=all rowShading=true>
  <Column id=rotulo title="Critère"/>
  <Column id=unidade title="Unité"/>
  <Column id=direcao title="Sens"/>
  <Column id=influencia_exercida title="R (influence exercée)" fmt=num3/>
  <Column id=influencia_recebida title="C (influence reçue)" fmt=num3/>
  <Column id=prominencia title="Proéminence (R+C)" fmt=num3 contentType=colorscale/>
  <Column id=relacao title="Relation (R−C)" fmt=num3 contentType=colorscale/>
  <Column id=papel title="Rôle"/>
  <Column id=peso title="Poids dérivé" fmt=pct2/>
</DataTable>

<BarChart data={dematel_c} x=rotulo y=relacao title="Diagramme cause–effet DEMATEL (R−C) : au-dessus de zéro = CAUSE" yAxisTitle="R − C" sort=false>
  <ReferenceLine y=0 color=info label="fronteira causa / efeito"/>
</BarChart>

### Matriz de relação total — quem influencia quem

> A tabela acima resume cada Critère em dois números. **Esta matriz mostra as ligações uma a uma**: `T = X(I − X)⁻¹` soma os caminhos diretos **e indiretos** de qualquer comprimento, e por isso revela influências que o especialista nunca declarou diretamente — A influencia B, B influencia C, logo A influencia C, e a matriz total contabiliza isso.
>
> Só aparecem as arestas **acima do limiar α** (a média de T). Abaixo dele, a intensidade é indistinguível de ruído de arredondamento, e um diagrama que desenhasse todas as ligações não informaria nada — toda matriz densa parece igualmente conectada.

<DataTable data={relacao_c} rows=12 rowShading=true>
  <Column id=origem_rotulo title="Source (influence)"/>
  <Column id=origem_papel title="Rôle de la source"/>
  <Column id=destino_rotulo title="Cible (est influencée)"/>
  <Column id=destino_papel title="Rôle de la cible"/>
  <Column id=intensidade title="Intensité tᵢⱼ" fmt=num4 contentType=colorscale/>
</DataTable>

<BarChart data={relacao_c} x=origem_rotulo y=intensidade series=destino_rotulo type=stacked title="Influence totale exercée par chaque critère, décomposée par cible" yAxisTitle="Intensidade acumulada" swapXY=true/>

### Quatro famílias de peso sobre o mesmo problema

> O **AHP** pergunta, par a par, quanto um Critère importa mais que outro. O **DEMATEL** mede influência sistêmica. **Onde divergem está o effet de segunda ordem subestimado.**
>
> O **AHP Fuzzy** (Buckley, 1985) recebe o mesmo julgamento do AHP, mas não descarta a imprecisão: quem disse "5" quis dizer algo entre 4 e 6, e essa faixa é carregada até o fim. As colunas `l` e `u` são os limites do número triangular de cada peso.
>
> O **BWM** (Rezaei, 2015) resolve um problema operacional, não teórico: a matriz de Saaty com 9 Critères exige 36 comparações e **ninguém a preenche com atenção até o fim**. O BWM pede apenas o melhor e o pior Critère e deriva o resto — 2n−3 comparações. A coluna `BWM CR` diz se o julgamento resultante é consistente.

<img src="/mc/{params.caso}/pesos_dematel_ahp.png" alt="DEMATEL, AHP e AHP Fuzzy" style="width:100%;border-radius:8px;"/>

<DataTable data={pesos_c} rows=all rowShading=true>
  <Column id=rotulo title="Critère"/>
  <Column id=papel title="Rôle"/>
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

> [!NOTE] O AHP Fuzzy **achata os extremos** em relação ao AHP crisp: a média geométrica com incerteza puxa os pesos para o centro. Um Critère que o AHP coloca em 50% costuma cair, e um que ele deixa em 0,4% costuma subir. Isso não é correção de erro, é o que acontece quando se admite que o julgamento tinha uma faixa. Se a ORDEM dos pesos muda entre os dois, a prioridade declarada não sobrevive à imprecisão do próprio decisor, e isso é informação para o comitê.

---

## ⚖️ Dix écoles de décision sur le même problème

> [!IMPORTANT] **Douze modèles sont appliqués à ce cas, et dix entrent dans ce graphique.** Le **BWM** renvoie des poids de critère (voir le tableau des quatre familles, ci-dessus) et le **DRSA** renvoie des règles (section propre, plus loin) — aucun des deux ne produit de position d'alternative, et c'est pourquoi le **consensus de Borda et la robustesse sont calculés sur ces dix**. Compter les douze ici laisserait croire que le consensus agrège ce qu'il n'agrège pas.

> Chaque méthode est une **théorie différente de ce que « meilleur » signifie**. Quand les dix s'accordent, le choix n'est pas un artefact de méthode. **Quand elles divergent, la divergence est la trouvaille** — et elle désigne en général exactement où se trouve le vrai compromis.
>
> Le **TOPSIS flou** (Chen, 2000) mérite une lecture à part : ce n'est pas « l'AHP-TOPSIS avec du bruit ». Outre les nombres triangulaires, il change la normalisation (linéaire au lieu de vectorielle) et la solution idéale (absolue au lieu de relative). Diverger de l'AHP-TOPSIS 2n est le comportement **attendu**, et cela mesure à quel point le classement dépend de ces choix.

<img src="/mc/{params.caso}/mapa_metodos.png" alt="Position por escola de decisão" style="width:100%;border-radius:8px;"/>

<BarChart data={metodos_c} x=rotulo y=rank_ series=metodo type=grouped title="Position par école de décision (1er = meilleur)" yAxisTitle="Posição" swapXY=true/>

### ELECTRE I — le noyau (kernel)

> Avant de classer, **éliminez** : le noyau est l'ensemble qu'aucune autre alternative ne surclasse. Un noyau à un seul élément clôt la décision ; un noyau trop grand indique que les critères ne discriminent pas — et le problème est de modélisation, non de calcul.

<DataTable data={nucleo_c} rows=12 rowShading=true>
  <Column id=rotulo title="Alternative"/>
  <Column id=no_nucleo title="Dans le noyau ?" fmt=boolean/>
  <Column id=domina title="Surclasse" fmt=num0/>
  <Column id=dominada title="Est surclassée par" fmt=num0/>
</DataTable>

### AHP-TOPSIS 2N — la double normalisation

> Le TOPSIS est **sensible à la normalisation choisie**. Nous exécutons les deux (vectorielle et min-max) et rapportons la concordance : la colonne **Robuste ?** est de l'honnêteté méthodologique.

<DataTable data={topsis_c} rows=12 rowShading=true>
  <Column id=rank_final title="#"/>
  <Column id=rotulo title="Alternative"/>
  <Column id=ci_vector title="Ci vectoriel" fmt=num4/>
  <Column id=ci_minmax title="Ci min-max" fmt=num4/>
  <Column id=ci_final title="Ci final" fmt=num4 contentType=colorscale/>
  <Column id=concordante title="Robuste ?" fmt=boolean/>
</DataTable>

---

## 🤝 Consensus de Borda

<DataTable data={consenso_c} rows=all rowShading=true>
  <Column id=rank_final title="#" contentType=colorscale/>
  <Column id=rotulo title="Alternative"/>
  <Column id=borda title="Points de Borda" fmt=num0/>
  <Column id=rank_medio title="Position moyenne" fmt=num2/>
  <Column id=unanime title="Unanime ?" fmt=boolean/>
  <Column id=prob_vitoria title="Gagne dans (%)" fmt=num1 contentType=colorscale/>
  <Column id=rank_p95 title="Pire cas (p95)" fmt=num0/>
</DataTable>

---

## 🎯 Robustesse — l'intervalle de confiance de la décision elle-même

> **Le problème.** Les poids ne sont jamais exacts — ce sont des estimations de préférence. Si deux points de pourcentage échangent la 1re et la 2e place, le « gagnant » est un artefact du calibrage.
>
> **La solution.** Nous perturbons avec `w' ~ Dirichlet(κ·w)` et reclassons **2 000 fois**. La Dirichlet a pour support exactement le simplexe et satisfait `E[w'] = w` — nous perturbons **sans biaiser**.

<BigValue data={robustez_top} value=rotulo title="Leader sous poids perturbés"/>
<BigValue data={robustez_top} value=prob_vitoria title="Gagne dans (%)" fmt=num1/>
<BigValue data={robustez_top} value=rank_p95 title="Pire position plausible" fmt=num0/>

<img src="/mc/{params.caso}/Robustesse.png" alt="Robustesse sob pesos perturbados" style="width:100%;border-radius:8px;"/>

<DataTable data={robustez_c} rows=15 rowShading=true>
  <Column id=rotulo title="Alternative"/>
  <Column id=prob_vitoria title="Gagne le consensus (%)" fmt=num1 contentType=colorscale/>
  <Column id=prob_top3 title="Top-3 (%)" fmt=num1/>
  <Column id=rank_medio title="Position typique" fmt=num2/>
  <Column id=rank_p05 title="Meilleur cas (p05)" fmt=num0/>
  <Column id=rank_p95 title="Pire cas (p95)" fmt=num0/>
</DataTable>

### Distribution complète des positions

> Une barre entièrement verte est une position qui **ne dépend pas des poids**. Une barre tachetée est une position disputée.

<img src="/mc/{params.caso}/distribuicao_posicoes.png" alt="Distribuição das posições" style="width:100%;border-radius:8px;"/>

---

## 🎲 Matriz BCG — que informatiquePO de aposta é cada Alternative

> O consenso responde **qual escolher**. A BCG responde **que tipo de aposta cada uma é** — pergunta diferente, e igualmente decisiva na hora de assinar.
>
> Dois eixos, ambos derivados dos **mesmos pesos do DEMATEL** que alimentam os dez métodos (renormalizados por grupo, de modo que a BCG é um segundo corte da mesma modelagem, não uma segunda modelagem):
>
> - **Attractivité** (Y) — desempenho ponderado nos Critères de **bénéfice** - **Position de coût** (X) — quanto entrega por unidade de **sacrifício**
>
> Os cortes são as **medianas** de cada eixo, não o ponto médio: mediana divide o conjunto em duas metades reais, enquanto 0,5 deixaria quadrantes vazios num conjunto assimétrico — e quadrante vazio não informa nada.

<BigValue data={bcg_res_c} value=estrelas title="⭐ Étoiles" fmt=num0/>
<BigValue data={bcg_res_c} value=vacas title="🐄 Vaches à lait" fmt=num0/>
<BigValue data={bcg_res_c} value=interrogacoes title="❓ Dilemmes" fmt=num0/>
<BigValue data={bcg_res_c} value=abacaxis title="🐕 Poids morts" fmt=num0/>

<img src="/mc/{params.caso}/matriz_bcg.png" alt="Matriz BCG" style="width:100%;border-radius:8px;"/>

| Quadrant | Leitura de decisão |
|---|---|
| ⭐ **Estrela** | Alta atratividade **e** boa posição de coût — a aposta natural: investir e padronizar. |
| 🐄 **Vaca leiteira** | Entrega o essencial pelo **menor sacrifício**. É a escolha de quem tem orçamento apertado. |
| ❓ **Interrogação** | Desempenho alto a **preço alto**. Só se justifica se o prêmio for necessário. |
| 🐕 **Abacaxi** | Nem entrega, nem é barata. **Descartar.** |

> **O cruzamento é onde mora o achado.** Um 2º colocado que é 🐄 Vaca costuma ser a escolha real de quem tem restrição orçamentária; um 2º colocado ❓ Interrogação só compensa se você precisa do prêmio de desempenho que ele cobra.

<DataTable data={bcg_c} rows=15 rowShading=true>
  <Column id=rank_consenso title="#" contentType=colorscale/>
  <Column id=rotulo title="Alternative"/>
  <Column id=quadrante_rotulo title="Quadrant"/>
  <Column id=atratividade title="Attractivité" fmt=num3 contentType=colorscale/>
  <Column id=posicao title="Position de coût" fmt=num3 contentType=colorscale/>
  <Column id=acao title="Que faire"/>
</DataTable>

---

## 📏 DRSA — la règle qui explique les décisions passées

> Les onze autres modèles demandent des préférences **déclarées** : poids, comparaisons, seuils. Le **DRSA** (Greco, Matarazzo & Słowiński) fait le chemin inverse — il reçoit les décisions déjà prises et renvoie la **règle** qui les explique, en langage clair, pour qui ne sait pas ce qu'est une normalisation vectorielle. C'est la seule famille ici qui apprend de l'historique au lieu d'exiger que quelqu'un sache déclarer ce qu'il préfère.

<div class="grid grid-cols-3 gap-4">
<BigValue data={drsa_q} value=gamma title="γ — qualité de l'approximation" fmt=pct1/>
<BigValue data={drsa_q} value=n_regras title="Règles induites" fmt=num0/>
<BigValue data={drsa_q} value=n_violacoes title="Paires violant la dominance" fmt=num0/>
</div>

<DataTable data={drsa_r} rows=all rowShading=true>
  <Column id=n_regra title="#"/>
  <Column id=texto title="Règle"/>
  <Column id=cobertura title="Couvre" fmt=num0/>
  <Column id=certeza title="Certitude" fmt=pct0/>
</DataTable>

> [!NOTE] **γ = 100 %** signifie que la relation de dominance classe toutes les alternatives sans ambiguïté : l'historique est cohérent et les règles le décrivent entièrement. **γ < 100 %** est un diagnostic, non un défaut — cela dit qu'il existe des paires où l'alternative dominée a été préférée, et la colonne *Paires violant la dominance* en compte le nombre. Dans ce cas la décision passée comporte des exceptions, et le savoir vaut mieux qu'un classement propre.

---

## 📐 Matrice de décision

> Os dados de entrada. **Substitua pela sua cotação, seu edital ou seu ensaio** — o motor é o mesmo; os dados é que são seus.

<DataTable data={matriz_c} rows=25 rowShading=true search=true>
  <Column id=alternativa_rotulo title="Alternative"/>
  <Column id=criterio_rotulo title="Critère"/>
  <Column id=direcao title="Sens"/>
  <Column id=valor title="Valeur" fmt=num2/>
  <Column id=unidade title="Unité"/>
</DataTable>

<LinkButton url='/fr'>← Voltar ao índice de casos</LinkButton>

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
