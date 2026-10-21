<!--
MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
-->

<div align="center">

# 🎯 MCDM Studio — Modèles de Décision Multicritère

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="820"/>

**ProfBru © 2026**

### Arrêtez de choisir avec un tableur. Commencez à décider avec des preuves.

**Douze écoles de décision. Un gagnant. Et — pour la première fois — la probabilité que ce gagnant soit le bon.**

[![MCDM](https://img.shields.io/badge/Méthodes_MCDM-12-2563eb?style=for-the-badge)](#-les-douze-écoles-de-décision--et-pourquoi-douze)
[![Engines](https://img.shields.io/badge/Moteurs-Python_+_Rust-c2410c?style=for-the-badge)](#-deux-moteurs-indépendants--la-vérification-croisée)
[![i18n](https://img.shields.io/badge/Langues-12-16a34a?style=for-the-badge)](#-12-langues--mémoire-de-traduction-sdl-trados)
[![Robustez](https://img.shields.io/badge/Univers_simulés-2.000-8f3d56?style=for-the-badge)](#le-moteur-de-consensus)

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Rust](https://img.shields.io/badge/Rust-1.96-000000?logo=rust&logoColor=white)](https://www.rust-lang.org)
[![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?logo=numpy&logoColor=white)](https://numpy.org)
[![Numba](https://img.shields.io/badge/Numba-JIT-00A3E0?logo=numba&logoColor=white)](https://numba.pydata.org)
[![Evidence](https://img.shields.io/badge/Evidence.dev-Dashboard-f4b548)](https://evidence.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/Licence-Propriétaire-red)](#-licence-et-paternité)

🌐 [Português](README.md) · [English](README.en.md) · [Español](README.es.md) · **Français** · [Deutsch](README.de.md) · [中文](README.zh.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [עברית](README.he.md) · [Русский](README.ru.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md)

</div>

---

## 💀 La douleur : vous avez déjà perdu de l'argent à cause d'un tableur

Pensez à la dernière décision coûteuse que vous avez prise. Acheter la voiture. Choisir le fournisseur. Approuver le projet. Définir l'ordinateur portable que 200 personnes utiliseront pendant quatre ans.

**Vous avez ouvert un tableur. Les options en lignes, les attributs en colonnes. Puis vous avez fait l'une de ces trois choses :**

| Ce que vous avez fait | Ce qui s'est vraiment passé |
|---|---|
| 🔻 **Trié par la colonne du prix** | Vous avez choisi le moins cher. Vous n'aviez pas besoin d'un tableur pour cela. |
| 🔺 **Trié par la note de l'expert** | Vous avez choisi le plus cher. Vous n'en aviez pas besoin non plus. |
| 🔍 **Filtré par « répond à toutes les exigences »** | La liste s'est vidée. Alors vous avez assoupli une exigence. Laquelle ? **Celle qui gênait.** |

> [!WARNING]
> **Les trois opérations ont le même défaut : aucune ne répond à la question que vous avez posée.**
> La question était *« parmi des options qui se contredisent, laquelle choisir ? »* — et trier par une colonne, c'est par définition décider selon **un** critère. Vous n'avez pas utilisé les sept autres. Ils étaient là uniquement pour vous rassurer.

Et il y a le problème que personne ne voit : **vous avez additionné des choses déjà additionnées.** Vous avez donné 20 % à la « consommation énergétique » et 25 % à l'« autonomie » — mais la consommation *cause* l'autonomie. Vous avez compté deux fois la même chose et appelé cela une analyse.

### Le moment où la décision meurt

C'est en réunion. Vous présentez le classement. Quelqu'un du comité demande :

> *Et si l'autonomie valait 30 % au lieu de 25 % ?*

Et vous ne savez pas. **Personne ne sait.** Parce que le tableur renvoie **un** nombre, avec une confiance implicite de 100 % qu'il n'a aucun moyen d'avoir. Vous revenez avec vos devoirs, vous ajustez les poids, et vous découvrez que le deuxième devient premier avec **deux points de pourcentage** d'écart.

Ce « gagnant » n'en a jamais été un. C'était un **artefact de votre calibrage** — et vous avez failli le signer.

---

## 💊 La solution : douze écoles, un consensus, et un intervalle de confiance

**MCDM Studio exécute **douze modèles multicritères** consacrés sur le même problème, tire le gagnant du **consensus** entre les dix qui produisent un classement, puis fait la seule chose qui compte vraiment :**

> ### 🎲 Il perturbe les poids **2 000 fois** et compte dans combien d'univers le gagnant continue de gagner.

Le verdict cesse d'être un nombre et devient une **phrase qui survit au comité** :

<div align="center">

| ❌ Ce que dit le tableur | ✅ Ce que dit MCDM Studio |
|---|---|
| « Le Modèle C est le meilleur. » | **« Le Modèle C gagne dans 96 % des univers de préférence plausibles. Verdict ROBUSTE : le choix ne dépend pas du réglage fin des poids. »** |
| *(pas de réponse)* | **« Le Modèle A gagne dans 51 %. Verdict FRAGILE : la première place est un artefact des poids. Ne décidez pas sur le seul classement. »** |

</div>

**Regardez le second cas. Un système honnête doit pouvoir dire *« ne me faites pas confiance ici »*. C'est la différence entre l'aide à la décision et un générateur de justification pour la décision que vous vouliez déjà prendre.**

---

## 🖼️ Voyez-le fonctionner

### 1. Qui est cause et qui est effet — avant tout poids

<div align="center"><img src="docs/telas/caca_multifuncao/dematel_causa_efeito.png" alt="DEMATEL" width="820"/></div>

**La douleur que cela résout :** vous attribuez des poids en supposant que les critères sont indépendants. **Ils ne le sont presque jamais.** La consommation énergétique *cause* l'autonomie. Le blindage *cause* le poids, qui *cause* la perte de mobilité. Les additionner comme indépendants, c'est compter deux fois.

**DEMATEL** construit la matrice de relation totale `T = X(I−X)⁻¹` — qui somme les influences directes **et indirectes**, de toute longueur de chemin — et sépare ce que vous pouvez **actionner** (causes, au-dessus de la ligne) de ce qui ne fait que **mesurer le résultat** (effets, en dessous). Les poids en découlent : par influence systémique, non par intuition.

> Dans le cas ci-dessus, **Transfert de Technologie** et **Signature Radar** sont des CAUSES : les toucher déplace tout le système. **Disponibilité de la flotte** est un EFFET — c'est un thermomètre, pas un levier. Un appel d'offres qui note la disponibilité et ignore le ToT mesure la fièvre et ignore l'infection.

### 2. Dix écoles sur le même problème

<div align="center"><img src="docs/telas/veiculo_eletrico/mapa_metodos.png" alt="Métodos" width="900"/></div>

**La douleur que cela résout :** toute méthode MCDM porte une théorie implicite de ce que « meilleur » signifie — et elle change le gagnant. Choisir une méthode et présenter le résultat, c'est choisir le résultat.

Nous exécutons les dix. Quand elles s'accordent, le choix **n'est pas un artefact de méthode**. Quand elles divergent, **la divergence est la trouvaille**.

> Ci-dessus : l'**hybride rechargeable** est 1er dans sept méthodes, mais **6e dans ELECTRE I**. Ce n'est pas du bruit — c'est de l'information. ELECTRE I autorise le *veto* : il indique que l'hybride présente un désavantage assez grave sur un critère pour être écarté, si bon soit-il par ailleurs. **C'est exactement la question que vous voulez porter au comité.**

### 3. L'intervalle de confiance de la décision elle-même

<div align="center"><img src="docs/telas/portfolio_startup/robustez.png" alt="Robustez" width="820"/></div>

**La douleur que cela résout :** la question du comité — *« et si le poids était différent ? »*. Répondue **avant** que quiconque ne la pose.

Nous perturbons les poids avec `w' ~ Dirichlet(κ·w)` et reclassons 2 000 fois. La Dirichlet est le choix naturel : son support est exactement le simplexe (poids positifs de somme 1) et elle satisfait `E[w'] = w` — nous perturbons **sans biaiser**.

### 4. Là où votre intuition se trompe

<div align="center"><img src="docs/telas/blindado/pesos_dematel_ahp.png" alt="DEMATEL, AHP, AHP Fuzzy e BWM" width="820"/></div>

**La douleur que cela résout :** vous croyez savoir ce qui compte. Deux familles de poids le mettent à l'épreuve.

L'**AHP** (Saaty) demande, par paires, combien un critère importe plus qu'un autre. Le **DEMATEL** mesure l'influence systémique. **Là où ils divergent se trouve l'effet de second ordre que vous avez sous-estimé** — et le graphique marque la plus grande divergence en rouge.

### 5. Où chaque alternative termine, sur 2 000 scénarios

<div align="center"><img src="docs/telas/estacao_trabalho/distribuicao_posicoes.png" alt="Distribuição" width="820"/></div>

Une barre entièrement verte est une position qui **ne dépend pas des poids**. Une barre tachetée est une position disputée. Vous voyez d'un coup d'œil où le classement est un fait et où il est une opinion.

---

## 🎯 À quoi cela sert — le choix sur mesure

Le moteur est **agnostique au domaine** : l'unité est le *cas de décision* (alternatives × critères), sans sémantique métier intégrée. Changer de domaine, c'est changer de données, pas de code.

<div align="center">

| Domaine | La décision | La douleur spécifique |
|---|---|---|
| 📱 **Électronique** | Téléphone, ordinateur portable, équipement | Le moins cher a le pire appareil photo ; celui au meilleur appareil photo a la pire batterie. Il n'existe pas « le meilleur » — il existe **le meilleur pour votre usage**. |
| 🚗 **Voitures électriques** | Flotte ou usage personnel | Autonomie, recharge, réseau d'assistance et revente tirent dans des sens opposés. Et le critère décisif (**l'autonomie réelle**, pas celle du catalogue) est le plus difficile à mesurer. |
| 🎖️ **Défense** | Chasseurs, blindés, drones, base logistique | Cycle de vie de 30 ans, irréversible, sous scrutin public. **Le prix unitaire représente moins d'un tiers du coût total.** Le transfert de technologie et le coût horaire décident du budget de trois décennies. |
| 🏢 **Entreprise** | Fournisseur, ERP, externalisation, expansion | Un comité qui ne s'accorde pas avec lui-même. **SAPEVO-M** a été conçu exactement pour cela : il agrège le jugement ordinal de **plusieurs décideurs** sans exiger de consensus préalable. |
| 🚀 **Startups** | Portefeuille de projets, allocation de capital | Décider par rendement espéré élit toujours le pari le plus risqué — **l'espérance ignore la queue de distribution**. Ici le risque est un **critère**, pas une note de bas de page de la diapositive 14. |
| 💻 **Informatique** | Standardisation du parc | La décision se multiplie par 200 et dure 4 ans. L'autonomie et la garantie sur site valent plus, en coût total de possession, que deux points de benchmark synthétique. |

</div>

### Cas prêts à exécuter

```bash
python3 pipeline.py --listar
```

| # | Cas | Domaine | Alternatives | Critères | Verdict | Auteurs / source |
|--:|---|---|--:|--:|---|---|
| 1 | `smartphone` | grand public | 6 | 8 | PROBABLE 63% | Modélisation propre |
| 2 | `veiculo_eletrico` | automobile | 7 | 8 | ROBUSTE 99% | Modélisation propre |
| 3 | `caca_multifuncao` | défense | 6 | 9 | ROBUSTE 100% | Modélisation propre |
| 4 | `blindado` | défense | 5 | 8 | ROBUSTE 93% | Modélisation propre |
| 5 | `portfolio_startup` | entreprise | 7 | 9 | ROBUSTE 96% | Modélisation propre |
| 6 | `estacao_trabalho` | informatique | 6 | 8 | ROBUSTE 98% | Modélisation propre |
| 7 | `carros_eletricos` | automobile | 38 | 9 | ROBUSTE 96% | Modélisation propre |
| 8 | `smartphones_2026` | grand public | 38 | 9 | PROBABLE 73% | Modélisation propre |
| 9 | `tablets` | grand public | 34 | 8 | PROBABLE 67% | Modélisation propre |
| 10 | `smartwatches` | grand public | 31 | 8 | PROBABLE 84% | Modélisation propre |
| 11 | `notebooks` | informatique | 32 | 8 | PROBABLE 83% | Modélisation propre |
| 12 | `maquinario_agricola` | agro-industrie | 35 | 8 | ROBUSTE 100% | Modélisation propre |
| 13 | `sbc_iot` | informatique | 33 | 8 | ROBUSTE 100% | Modélisation propre |
| 14 | `mineracao_asic` | infrastructure | 31 | 8 | FRAGILE 50% | Modélisation propre |
| 15 | `minipcs` | informatique | 10 | 8 | ROBUSTE 91% | Modélisation propre |
| 16 | `impressoras_3d_miniaturas` | fabrication | 30 | 9 | FRAGILE 48% | Modélisation propre |
| 17 | `impressoras_3d_producao` | fabrication | 30 | 9 | FRAGILE 58% | Modélisation propre |
| 18 | `plotters_formato` | fabrication | 24 | 9 | ROBUSTE 96% | Modélisation propre |
| 19 | `impressoras_3d_miniaturas_triadas` | fabrication | 13 | 9 | ROBUSTE 100% | Modélisation propre |
| 20 | `acoes_b3` 📚 | finance | 20 | 7 | FRAGILE 39% | COSTA, L. S. da · VÁSQUEZ, J. A.; ESCOBAR, J. W.; MANOTAS, D. F. · [DOI](https://doi.org/10.3390/risks10010004) |
| 21 | `fundos_imobiliarios` 📚 | finance | 18 | 8 | PROBABLE 85% | SANTOS, V. V. dos (orient. ALMEIDA FILHO, A. T. de) |
| 22 | `fintech` 📚 | finance | 16 | 8 | PROBABLE 67% | WIBOWO, S.; GRANDHI, L.; GRANDHI, S.; WELLS, M. · [DOI](https://doi.org/10.3390/math10020225) |
| 23 | `avaliacao_imoveis` 📚 | immobilier | 16 | 8 | ROBUSTE 94% | DUARTE, D. C. de O. · MARQUES, J. P. M. |
| 24 | `ordens_servico` 📚 | opérations | 18 | 8 | ROBUSTE 97% | ALENCAR, L. G. de; TAVARES, F. R. M.; MENDONÇA, F. J. S. de F.; DUARTE, A. K. G. |
| 25 | `cloud_providers` 📚 | informatique | 14 | 8 | ROBUSTE 100% | SOLOMON, T. |
| 26 | `venture_capital` 📚 | entreprise | 16 | 8 | ROBUSTE 96% | BEIM, G.; LÉVESQUE, M. · DHOCHAK, M.; DOLIYA, P. · AFFUL-DADZIE, E.; AFFUL-DADZIE, A.; OPLATKOVÁ, Z. K. · [DOI](https://doi.org/10.1002/mcda.1703) |
| 27 | `instrutores` 📚 | entreprise | 15 | 8 | ROBUSTE 100% | SILVA, C. E. J. da; SALLES-NETO, L. L. de; SANTOS, M. dos |
| 28 | `cripto_portfolio` 📚 | finance | 9 | 7 | ROBUSTE 100% | ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. · [DOI](https://doi.org/10.3390/math9141677) |
| 29 | `portfolio_crise` 📚 | finance | 8 | 4 | PROBABLE 77% | COSTA, I. P. de A.; MAÊDA, S. M. do N.; TEIXEIRA, L. F. H. de S. de B.; GOMES, C. F. S.; SANTOS, M. dos |
| 30 | `cenarios_va` 📚 | automobile | 16 | 9 | PROBABLE 73% | LI, S.; ZHOU, R.; HUANG, H. · [DOI](https://doi.org/10.1007/s42154-024-00344-6) |
| 31 | `impressora_3d_energia` 📚 | fabrication | 12 | 7 | PROBABLE 69% | OLIVEIRA, V. A. R. de; ALVARADO SILVA, C. A.; OLIVEIRA, G. C. R. de; TAJIMA, F. M.; FARIA NETO, A. dos R.; SALOMON, V. A. P.; GUIDI, E. S. · [DOI](https://doi.org/10.18687/LACCEI2025.1.1.1193) |
| 32 | `impressoras_juridico` 📚 | opérations | 12 | 4 | ROBUSTE 100% | OLIVEIRA, N. C.; OLIVEIRA, P. F. C. de; GOMES, C. F. S.; SANTOS, M. dos |
| 33 | `fundos_hedge` 📚 | finance | 20 | 8 | ROBUSTE 94% | SILVA, F. P. da; RIBEIRO, C. de O. |
| 34 | `modelos_previsao` 📚 | informatique | 7 | 8 | ROBUSTE 95% | SHAH, S. |
| 35 | `policultivo_rj` 📚 | agro-industrie | 8 | 8 | PROBABLE 86% | PENEDO, B. |
| 36 | `parafusadeiras_domesticas` 📚 | grand public | 14 | 8 | PROBABLE 70% | COMPROU AVALIOU (canal) · [vídeo](https://youtu.be/pgdqVYEjZtk) |
| 37 | `parafusadeiras_profissionais` 📚 | fabrication | 12 | 8 | ROBUSTE 100% | FERRAMENTAS EM AÇÃO — ASSIS PIRES (canal) · [vídeo](https://youtube.com/shorts/9SIs3agoZKc) |
| 38 | `crowdfunding_startups` 📚 | entreprise | 16 | 9 | ROBUSTE 93% | SKARE, M.; GAVUROVA, B.; POLISHCHUK, V. · [DOI](https://doi.org/10.1016/j.jbusres.2023.113719) |

> [!NOTE]
> Les matrices des cas sont **illustratives** — des ordres de grandeur publics et plausibles, pour démontrer la méthode. Ce qui **n'est pas** illustratif, c'est la **modélisation** : critères, sens, matrice causale du DEMATEL et matrice de Saaty. C'est là que réside la valeur. **Remplacez les nombres par votre devis, votre appel d'offres ou votre essai de laboratoire** — le moteur est le même ; les données sont les vôtres.

> [!TIP]
> Le **verdict** mesure dans combien des 2 000 univers de préférence simulés le gagnant continue de gagner, en perturbant les poids par Dirichlet (κ=200). **ROBUSTE** ≥ 90 % : le choix ne dépend pas du calibrage. **PROBABLE** 60–89 % : le second est compétitif, comparez les deux. **FRAGILE** < 60 % : la première place est un artefact des poids — et c'est un résultat légitime, pas un échec. Cela signifie que les données ne tranchent pas, et la décision revient à l'humain.

### 📚 Études de cas issues de la littérature

> [!IMPORTANT]
> Les cas du tableau ci-dessous ont leurs **critères et leur structure causale tirés des travaux listés** — articles évalués par les pairs, thèses, actes de congrès et rapports techniques. Les critères n'ont pas été inventés : ils viennent du texte d'origine, et la paternité est préservée ici et dans l'en-tête du module correspondant. Les **matrices numériques** sont nos propres instanciations — aucune donnée des travaux originaux n'a été reproduite. Lorsqu'un DOI indexé existe, le lien mène au travail ; sinon, la référence textuelle complète permet de le retrouver.

| Cas | Domaine | Auteurs | Référence |
|---|---|---|---|
| `acoes_b3` | finance | COSTA, L. S. da · VÁSQUEZ, J. A.; ESCOBAR, J. W.; MANOTAS, D. F. | *Uma metodologia para a pré-seleção de ações utilizando o método multicritério TOPSIS* (COSTA, UERJ) · *AHP–TOPSIS Methodology for Stock Portfolio Investments*, Risks, v.10, n.1, 4, 2022 (Universidad del Valle) · [DOI](https://doi.org/10.3390/risks10010004) |
| `fundos_imobiliarios` | finance | SANTOS, V. V. dos (orient. ALMEIDA FILHO, A. T. de) | *Avaliação do método Random Forest para auxílio à seleção de fundos de investimento imobiliário listados na Bolsa de Valores*. Trabalho de Graduação, Engenharia da Computação, CIn/UFPE, set. 2023 |
| `fintech` | finance | WIBOWO, S.; GRANDHI, L.; GRANDHI, S.; WELLS, M. | *A Fuzzy Multicriteria Group Decision Making Approach for Evaluating and Selecting Fintech Projects*. Mathematics, v.10, n.2, 225, 2022 — CQUniversity, Austrália · [DOI](https://doi.org/10.3390/math10020225) |
| `avaliacao_imoveis` | immobilier | DUARTE, D. C. de O. · MARQUES, J. P. M. | *Análise multicritério e geoestatística aplicadas na avaliação em massa de imóveis urbanos*. Tese, UFV, 2019 · *As formas de avaliar imóvel em leilão judicial*. Universidade São Judas Tadeu, 2023 |
| `ordens_servico` | opérations | ALENCAR, L. G. de; TAVARES, F. R. M.; MENDONÇA, F. J. S. de F.; DUARTE, A. K. G. | *Priorização de ordens de serviço aplicando métodos de tomada de decisão: o AHP integrado ao PROMETHEE*. Revista Produção Online, v.22, n.2, p.2763-2784, 2022 — URCA, Ceará |
| `cloud_providers` | informatique | SOLOMON, T. | *Ranking of Cloud Service Providers Using a Dynamic TOPSIS Model for Provisioning of Enterprise IT Infrastructure in the Cloud*. Praxis (Doctor of Engineering), The George Washington University, 2017 |
| `venture_capital` | entreprise | BEIM, G.; LÉVESQUE, M. · DHOCHAK, M.; DOLIYA, P. · AFFUL-DADZIE, E.; AFFUL-DADZIE, A.; OPLATKOVÁ, Z. K. | *Selecting projects for venture capital funding: a multiple criteria decision approach* (Case Western Reserve University) · *Valuation of a startup: moving towards strategic approaches*, J. Multi-Criteria Decision Analysis, 2019 · *Assessing commercial viability of technology start-up businesses in a government venture capital under intuitionistic fuzzy environment*, Int. J. Fuzzy Systems, 2016 · [DOI](https://doi.org/10.1002/mcda.1703) · [DOI](https://doi.org/10.1007/s40815-016-0141-9) |
| `instrutores` | entreprise | SILVA, C. E. J. da; SALLES-NETO, L. L. de; SANTOS, M. dos | *Modelagem matemática com os métodos AHP e TOPSIS para ordenação de instrutores em uma escola da FAB*. LIV SBPO, Juiz de Fora, 2022 — ITA / UNIFESP / IME |
| `cripto_portfolio` | finance | ALJINOVIĆ, Z.; MARASOVIĆ, B.; ŠESTANOVIĆ, T. | *Cryptocurrency Portfolio Selection — A Multicriteria Approach*. Mathematics, v.9, n.14, 1677, 2021 — University of Split, Croácia — **pesos AHP do artigo** · [DOI](https://doi.org/10.3390/math9141677) |
| `portfolio_crise` | finance | COSTA, I. P. de A.; MAÊDA, S. M. do N.; TEIXEIRA, L. F. H. de S. de B.; GOMES, C. F. S.; SANTOS, M. dos | *Finanças em períodos de crise: aplicação do método SAPEVO-M para composição de portfólios de investimentos*. Pesquisa Operacional para o Desenvolvimento, v.13, e13004, 2021 — UFF / CASNAV / IME — **matriz de decisão do artigo** |
| `cenarios_va` | automobile | LI, S.; ZHOU, R.; HUANG, H. | *Multidimensional Evaluation of Autonomous Driving Test Scenarios Based on AHP-EWM-TOPSIS Models*. Automotive Innovation, 2025 · [DOI](https://doi.org/10.1007/s42154-024-00344-6) |
| `impressora_3d_energia` | fabrication | OLIVEIRA, V. A. R. de; ALVARADO SILVA, C. A.; OLIVEIRA, G. C. R. de; TAJIMA, F. M.; FARIA NETO, A. dos R.; SALOMON, V. A. P.; GUIDI, E. S. | *Multicriteria Analysis for 3D Printer Selection*. 23rd LACCEI International Multi-Conference, Cidade do México, 2025 — UNESP / Universidad César Vallejo · [DOI](https://doi.org/10.18687/LACCEI2025.1.1.1193) |
| `impressoras_juridico` | opérations | OLIVEIRA, N. C.; OLIVEIRA, P. F. C. de; GOMES, C. F. S.; SANTOS, M. dos | *Aplicação do método AHP TOPSIS 2N como apoio à tomada de decisão: estudo de caso no departamento jurídico da Secretaria Municipal de Saúde de Duque de Caxias* — UNIGRANRIO / UFF / IME |
| `fundos_hedge` | finance | SILVA, F. P. da; RIBEIRO, C. de O. | *Análise comparativa de fundos de hedge brasileiros utilizando DEA e bootstrap*. XII SIMPEP, Bauru-SP, 2005 — Escola Politécnica da USP |
| `modelos_previsao` | informatique | SHAH, S. | *Comparison of Stochastic Forecasting Models*. Stochastic Differential Equations Course Project, Johns Hopkins University — o artigo compara os modelos; a modelagem multicritério sobre eles é deste projeto |
| `policultivo_rj` | agro-industrie | PENEDO, B. | *AGTech PoliCultivo 4.0 — Otimização de Portfólio de Cultivos em Ambiente Controlado (RJ)*. Relatório técnico, 03/08/2026, seção 14 — **matriz e pesos do relatório** |
| `parafusadeiras_domesticas` | grand public | COMPROU AVALIOU (canal) | *As 5 Melhores Parafusadeira De 2025*, 14/05/2024 — especificações extraídas da narração · [vídeo](https://youtu.be/pgdqVYEjZtk) |
| `parafusadeiras_profissionais` | fabrication | FERRAMENTAS EM AÇÃO — ASSIS PIRES (canal) | *As Melhores Parafusadeiras Do Mundo*, 04/01/2024 — modelos e baterias lidos dos quadros do vídeo · [vídeo](https://youtube.com/shorts/9SIs3agoZKc) |
| `crowdfunding_startups` | entreprise | SKARE, M.; GAVUROVA, B.; POLISHCHUK, V. | *A decision-making support model for financing start-up projects by venture capital funds on a crowdfunding platform*. Journal of Business Research, v.158, 113719, 2023 — **critérios e escalas do artigo** · [DOI](https://doi.org/10.1016/j.jbusres.2023.113719) |

---

## ⚡ Installation

### Chemin le plus rapide (Python)

```bash
git clone <url> multicriteriadecisionmodels
cd multicriteriadecisionmodels/public/foundations/pipeline
pip install -r requirements.txt
python3 pipeline.py
```

C'est tout. Les six cas s'exécutent, avec un rapport complet.

<details>
<summary><b>Prérequis détaillés</b></summary>

| Composant | Version minimale | Obligatoire ? | Pour quoi |
|---|---|---|---|
| Python | 3.10 | ✅ | moteur de référence |
| NumPy | 2.0 | ✅ | algèbre de toutes les méthodes |
| numba | 0.60 | ⚠️ | JIT des noyaux — sans lui, même résultat, plus lent |
| SciPy | 1.10 | ✅ | statistique auxiliaire |
| matplotlib | 3.7 | ✅ | les 5 écrans par cas |
| Rust / cargo | 1.75 | ⭕ | moteur de vérification croisée |
| Node.js | 18 | ⭕ | tableau de bord Evidence |
| screen | — | ⭕ | exécution en arrière-plan |

</details>

### Chaîne complète

```bash
./run_all.sh                    # tests → pipeline → écrans → i18n → Rust → vérification
./run_all.sh --rapido           # saute Rust et i18n
./run_all.sh --caso smartphone  # un seul cas
./run_all.sh --background       # exécute dans screen (rattacher : screen -r mcdm)
```

### Moteur Rust — binaire sans runtime

```bash
cd public/foundations/rust/mcdm_core
cargo test --release
cargo build --release

./target/release/mcdm --exemplo > problema.mcdm
./target/release/mcdm problema.mcdm
./target/release/mcdm problema.mcdm --json
```

### Tableau de bord

```bash
cd public/foundations/evidence
npm install
npm run dev               # http://localhost:3000
```

<details>
<summary><b>Commandes avancées</b></summary>

```bash
python3 pipeline.py caca_multifuncao --workers 8 --iter 5000
python3 testes_nucleo.py
python3 exportar_rust.py
python3 gerar_i18n.py --tudo
python3 gerar_i18n.py --verificar
python3 gerar_graficos.py --workers 6
```

| Variable | Par défaut | Effet |
|---|---|---|
| `MCDM_WORKERS` | auto | processus du `ProcessPoolExecutor` |
| `MCDM_NUMBA` | `1` | JIT activé ; `0` pour déboguer en NumPy pur |
| `MCDM_SEED` | `42` | reproductibilité |
| `ROBUSTEZ_ITER` | `2000` | univers de préférence |
| `ROBUSTEZ_KAPPA` | `200` | concentration de la Dirichlet (plus élevée = poids plus fidèles) |
| `MAUT_AVERSAO` | `2.0` | aversion au risque (r > 0 = concave) |
| `PROMETHEE_TIPO` | `linear` | fonction de préférence (6 disponibles) |

</details>

---

## ⚖️ Les douze écoles de décision — et pourquoi douze

> [!IMPORTANT]
> **Chaque méthode est une théorie différente de ce que « meilleur » signifie.** N'en utiliser qu'une, c'est choisir la réponse en même temps que la question. Nous les exécutons toutes parce que **l'accord entre théories indépendantes** est la preuve la plus forte qu'un problème de décision admette.

<div align="center">

| Méthode | École | Ce qu'elle suppose | Quand c'est **l'**outil adéquat | Origine |
|---|---|---|---|---|
| **AHP-TOPSIS 2n** | distance à l'idéal | compensation totale | critères quantitatifs, décideur unique | Saaty (1980); Hwang & Yoon (1981) |
| **ELECTRE I** | surclassement | l'incomparabilité est permise | **tri** : éliminer le dominé | Roy (1968) |
| **ELECTRE II** | surclassement | seuils fort et faible | classement complet **avec veto** | Roy & Bertier (1971) |
| **PROMETHEE II** | surclassement | préférence graduelle (6 fonctions) | quand « un peu mieux » ≠ « mieux » | Brans & Vincke (1985) |
| **MAUT** | utilité | indépendance additive + aversion au risque | décision sous incertitude | Keeney & Raiffa (1976) |
| **MCDA-C** | constructiviste | niveaux Neutre/Bon ancrés | **diagnostic absolu**, pas seulement un classement | Ensslin, Montibeller & Noronha (2001) |
| **VIKOR** | compromis | utilité du groupe × regret maximal | quand **compenser est inacceptable** | Opricovic (1979); Opricovic & Tzeng (2002-07) |
| **TODIM** | Théorie des Perspectives | une perte fait plus mal qu'un gain équivalent | décideur averse à la perte — **tous le sont** | Gomes & Lima (1992); Kahneman & Tversky (1979) |
| **SAPEVO-M** | ordinal multi-décideur | jugement ordinal de plusieurs décideurs | **comité qui ne s'accorde pas** | Gomes et al. (1997); Teixeira, Santos & Gomes (2019) |
| **TOPSIS Fuzzy** | Floue | que la donnée a une PLAGE, pas un point | la mesure est imprécise et vous voulez savoir si le classement y survit | Zadeh (1965); Chen (2000) |
| **BWM** | source de poids | que le décideur sait désigner le meilleur et le pire critère | **la matrice de Saaty est impossible à remplir** : 2n−3 comparaisons au lieu de n(n−1)/2 | Rezaei (2015; 2016) |
| **DRSA** | induction de règles | qu'il existe des décisions passées, et qu'elles respectent la dominance | personne ne peut déclarer de poids, mais **il existe un historique** — et la réponse doit être une **règle lisible** | Greco, Matarazzo & Słowiński (1999; 2001) |

</div>

> [!NOTE]
> Le **TOPSIS flou** n'est pas l'AHP-TOPSIS avec du bruit : outre les nombres triangulaires, il change la normalisation (linéaire au lieu de vectorielle) et la solution idéale (absolue au lieu de relative). **Diverger de l'AHP-TOPSIS 2n est le comportement attendu**, et cela mesure à quel point le classement dépend de ces choix. L'**AHP flou** (Buckley) devient une troisième source de poids, aux côtés du DEMATEL et de l'AHP : il reçoit le même jugement par paires, mais porte l'imprécision jusqu'au bout — avec un étalement uniforme la valeur centrale coïncide avec celle de l'AHP, et ce qu'il ajoute est la **plage**, qui dit si l'ordre de priorité survit à l'imprécision du décideur lui-même.

> [!IMPORTANT]
> **BWM et DRSA occupent une place différente des dix autres.** Le BWM est une **source de poids** — alternative à l'AHP et au DEMATEL — et le DRSA **induit des règles** à partir de décisions passées. Aucun des deux ne produit de classement propre, et c'est pourquoi le **consensus de Borda et l'analyse de robustesse restent calculés sur les dix méthodes de classement**.

<details>
<summary><b>Pourquoi ces trois méritent une attention particulière</b></summary>

### VIKOR — quand compenser est inacceptable
VIKOR calcule **deux** mesures : `S` (utilité du groupe — somme pondérée, qui **accepte** qu'une performance catastrophique soit compensée par plusieurs bonnes) et `R` (regret individuel maximal — minimax, qui **refuse** la compensation).

Un blindé à mobilité excellente et protection catastrophique a un `S` optimal et un `R` désastreux. La somme pondérée l'élirait ; VIKOR le signale. Et quand `S` et `R` divergent, les conditions **C1** (avantage acceptable) et **C2** (stabilité acceptable) signalent explicitement que la décision comporte un angle mort.

### TODIM — la perte fait plus mal que le gain
Fondé sur la **Théorie des Perspectives** de Kahneman et Tversky : perdre 10 points d'autonomie fait plus mal que gagner 10 ne fait plaisir. La somme pondérée classique ignore cette asymétrie et traite gain et perte comme symétriques — **ce qu'aucun décideur humain ne fait.** Le facteur `θ` en règle l'intensité : `θ < 1` amplifie l'aversion à la perte.

### SAPEVO-M — le comité qui ne s'accorde pas
Toutes les autres méthodes exigent un vecteur de poids. **D'où vient-il quand cinq décideurs ont des avis différents ?** SAPEVO-M règle cela à la source : chaque décideur exprime une préférence **ordinale** (« l'autonomie est bien plus importante que le prix », sur une échelle à sept points), et la méthode agrège **sans exiger de pré-ordre de consensus**. C'est ainsi qu'un comité s'exprime réellement — personne ne dit « l'autonomie vaut 0,237 ».

</details>

### Le moteur de consensus

```
DEMATEL · AHP · AHP Fuzzy · BWM ──► poids par influence ──► 10 méthodes ──► consensus de Borda ──► gagnant
                                                                        │
                                        2 000 univers de Dirichlet ───────────────────┘
                                                    ▼
                                 verdict: ROBUSTO / PROVÁVEL / FRÁGIL

DRSA ──────────────────────────────► règles lisibles à partir de décisions passées
```

| Verdict | Confiance | Que faire |
|---|---|---|
| 🟢 **ROBUSTE** | ≥ 90% | Le choix ne dépend pas du réglage fin. **Vous pouvez le porter au comité.** |
| 🟡 **PROBABLE** | 60–90% | Il tient dans la plupart des scénarios, mais le second est compétitif. **Comparez les deux.** |
| 🔴 **FRAGILE** | < 60% | La première place est un **artefact des poids**. Ne décidez pas sur le seul classement : revenez au décideur et recalibrez. |

---

## 🔬 Deux moteurs indépendants : la vérification croisée

> [!TIP]
> **Pourquoi tout réimplémenter en Rust ?** Parce que « le code s'exécute » n'est pas une preuve que les **mathématiques** sont justes.

Une erreur de transcription de formule se répète rarement **à l'identique** dans deux langages à algèbre linéaire indépendante. Le moteur Python utilise NumPy/LAPACK ; le moteur Rust implémente l'élimination de Gauss avec pivot partiel et la méthode des puissances **à la main, sans la moindre dépendance externe**.

```bash
python3 exportar_rust.py
```
```
✅ smartphone           8 méthodes identiques · gagnant=C     (Δ ≤ 4.7e-11)
✅ veiculo_eletrico     8 méthodes identiques · gagnant=EV6   (Δ ≤ 4.1e-11)
✅ caca_multifuncao     8 méthodes identiques · gagnant=C3    (Δ ≤ 4.5e-11)
✅ blindado             8 méthodes identiques · gagnant=B3    (Δ ≤ 4.6e-11)
✅ portfolio_startup    8 méthodes identiques · gagnant=P3    (Δ ≤ 4.9e-11)
✅ estacao_trabalho     8 méthodes identiques · gagnant=W5    (Δ ≤ 5.0e-11)
```

**Bonus : le binaire Rust n'a besoin ni de Python, ni de NumPy, ni de numba, ni d'environnement virtuel. Quelques Mo qui tournent sur un serveur, un conteneur ou une machine embarquée — ce qui compte quand le moteur accompagne un système sur le terrain.**

---

## 🚀 Performance : 26× plus rapide, même réponse

L'analyse de robustesse exécute 2 000 univers × 10 méthodes. L'implémentation naïve prenait **42 secondes** par cas.

<div align="center">

| Étape | Temps | Gain |
|---|---|---|
| Noyaux JIT par univers | 42,33 s | — |
| **Précompilation en tenseurs** | 2,41 s | **17,6×** |
| `ranks` sous JIT + état par processus | **1,63 s** | **26,0×** |

</div>

> **L'optimisation la plus rentable n'a été ni le parallélisme ni le JIT.** C'est d'avoir compris que quatre des dix méthodes sont **linéaires dans le vecteur de poids** — ce qui permet de précalculer des tenseurs et de réduire chaque univers à un produit matrice-vecteur. **L'algèbre avant l'infrastructure.**

Et le résultat est **identique bit à bit** au chemin lent — 100 univers × 10 méthodes vérifiés à chaque exécution de la suite. Une optimisation qui change le résultat est un bogue, pas un gain.

<details>
<summary><b>Politique d'exécution du projet</b></summary>

| Règle | Application |
|---|---|
| **Parallélisme** | `ProcessPoolExecutor` pour le travail CPU-bound ; jamais de threads (le GIL sérialise) |
| **Seuil** | Série ou parallèle décidé par le **travail** (`n_iter · m² · k`), non par le nombre d'éléments — paralléliser un petit problème est **plus lent** que de le résoudre |
| **JIT** | `numba` avec `cache=True` sur les noyaux O(m²k) ; se dégrade en NumPy pur s'il est absent |
| **Arrière-plan** | `screen`, jamais `nohup` — permet de rattacher et d'interagir |
| **Reproductibilité** | Partition fixe et indépendante du nombre de processus : même graine → résultat identique avec 1 ou 32 processus |

</details>

---

## 🌐 12 langues — mémoire de traduction SDL Trados

Ce n'est pas la traduction automatique d'un README. C'est un **pipeline de localisation** avec mémoire de traduction au standard **SDL Trados Studio**.

```
translation.memory.md          ← source canonique, versionnée dans git
   │  --tm
   ▼
strings.<locale>.json          ← artefact consommé
   │  --paginas
   ▼
12 pages du tableau de bord + 12 READMEs
   │  --tmx
   ▼
translation.memory.tmx         ← importable dans SDL Trados Studio
```

| Élément | Chiffres |
|---|---|
| Locales | **12** (pt-BR · en · es · fr · de · zh · ko · hi · **he RTL** · ru · sv · fi) |
| Unités de traduction | 56 |
| Termes de glossaire (MultiTerm) | 22 |
| Segments dans le TMX | **948** |
| Encodage | UTF-8 · LF · NFC |

```bash
python3 gerar_i18n.py --verificar
```

Le QA reproduit le **Verify** de Trados : cohérence terminologique, placeables préservés, couverture de segment, encodage strict et non-traduisibles intacts — avec une règle différenciée par système d'écriture (les sigles techniques restent en caractères latins dans toutes les langues ; les noms propres sont **translittérés** là où l'écriture n'est pas latine).

---

## 📁 Ce qu'il y a à l'intérieur

```
multicriteriadecisionmodels/
├── README.md (+11)                     vitrine en 12 langues
├── docs/                               logo et écrans des READMEs
│
└── public/foundations/
    ├── pipeline/                       MOTEUR PYTHON (référence)
    │   ├── nucleo.py                   DEMATEL · ELECTRE I/II · PROMETHEE II
    │   │                               MAUT · MCDA-C · AHP · TOPSIS 2N
    │   ├── metodos_br.py               SAPEVO-M · VIKOR · TODIM · Copeland
    │   ├── fuzzy.py                    AHP Fuzzy · TOPSIS Fuzzy
    │   ├── bwm.py                      BWM (Rezaei)
    │   ├── drsa.py                     DRSA (Greco · Matarazzo · Słowiński)
    │   ├── robustez.py                 Dirichlet + ProcessPoolExecutor
    │   ├── pipeline.py                 orchestrateur
    │   ├── gerar_graficos.py           6 écrans par cas
    │   ├── gerar_i18n.py               TM → strings → pages → TMX
    │   ├── testes_nucleo.py            99 vérifications mathématiques
    │   ├── exportar_rust.py            vérification entre moteurs
    │   ├── casos/                     38 cas + validation
    │   └── run_all.sh                  chaîne (screen)
    │
    ├── rust/mcdm_core/                 MOTEUR RUST (vérification + distribution)
    │   └── src/lib.rs                  toutes les méthodes, zéro dépendance
    │
    └── evidence/                       TABLEAU DE BORD (Evidence.dev)
        ├── sources/mcdm/               11 requêtes SQL
        └── pages/                      12 routes de langue
```

---

## 🧠 Fondements

Le projet repose sur une littérature revue, non sur l'intuition. L'architecture d'intégration suit **John (2025)**, *« Integration of DEMATEL with Other MCDM Methods for Comprehensive Techno-Economic Analysis »* : le DEMATEL révèle la structure causale et dérive des **poids par influence**, qui alimentent ensuite les méthodes de classement — au lieu de poids arbitrés.

Les méthodes de l'**école brésilienne d'Aide Multicritère à la Décision** (SAPEVO-M, TODIM-FSE, ELECTRE II, VIKOR, méthodes ordinales) suivent les travaux de l'**IME**, de l'**UFF**, du **CASNAV**, de l'**AMAN** et de la **FURB** — y compris des applications réelles à l'**évaluation de drones pour la guerre navale**, à la **classification de base logistique de brigade** et au **classement de corvettes pour la Marine brésilienne**.

> [!NOTE]
> **La paternité des méthodes revient intégralement à leurs créateurs,** crédités individuellement dans les en-têtes de `nucleo.py` et `metodos_br.py`. Ce projet apporte l'implémentation, l'intégration et le moteur de consensus — **pas les méthodes**.

---

## ❓ Les questions que vous allez poser

<details>
<summary><b>J'utilise déjà une matrice de décision pondérée. N'est-ce pas la même chose ?</b></summary>

Non, pour trois raisons. **(1)** Une matrice pondérée est **une** méthode (somme pondérée), avec une théorie intégrée : la compensation totale. Elle suppose qu'une performance catastrophique sur un critère peut être compensée ailleurs — ce qui est faux en sécurité, en protection blindée et en conformité réglementaire. **(2)** Elle suppose des critères indépendants, et vous additionnez presque toujours des choses déjà additionnées. **(3)** Elle renvoie un nombre sans intervalle de confiance, et ne survit donc pas à la première question du comité.
</details>

<details>
<summary><b>Comment choisir les poids ?</b></summary>

Vous ne les choisissez pas — **cinq chemins les dérivent**. Le **DEMATEL** les extrait de la structure causale que vous déclarez (qui influence qui). L'**AHP** les extrait de comparaisons par paires, avec une vérification de cohérence qui **rejette** le jugement contradictoire. L'**AHP flou** fait de même en admettant que chaque jugement est une plage, non un point. Le **BWM** ne demande que le meilleur et le pire critère — 2n−3 comparaisons au lieu de n(n−1)/2, ce qui le rend remplissable là où l'AHP ne l'est pas. Le **SAPEVO-M** les extrait du jugement ordinal de plusieurs décideurs. Et après cela, l'analyse de robustesse demande à quel point le résultat en **dépend** encore.
</details>

<details>
<summary><b>Et si mon problème comporte 200 alternatives ?</b></summary>

Cela fonctionne. Le seuil de parallélisme détecte le régime et répartit sur les processus. Mesuré : 60 alternatives × 12 critères × 2 000 univers en 3,8 s avec 4 processus. Au-delà d'environ 700 alternatives, le tenseur de préférence dépasse la limite mémoire configurée et le moteur vous avertit, au lieu de se bloquer.
</details>

<details>
<summary><b>Les méthodes ont divergé. Et maintenant ?</b></summary>

**C'est le produit, pas le problème.** La divergence indique que votre décision est sensible à l'école adoptée — et nomme laquelle. Si ELECTRE rétrograde celui que tous les autres élisent, il existe un critère sur lequel cette alternative est assez grave pour justifier un veto. Portez **cela** au comité, pas le classement.
</details>

<details>
<summary><b>Puis-je utiliser mes propres données ?</b></summary>

C'est fait pour. Un cas est une structure déclarative dans `casos/catalogo.py` : critères (avec sens et unité), alternatives, matrice de décision, matrice causale du DEMATEL et matrice de Saaty. Le validateur rejette un cas mal formé **avant** tout calcul — dimensions incohérentes, diagonale erronée, matrice de Saaty non réciproque, critère constant qui ne discrimine rien.
</details>

---

## 📜 Licence et paternité

<div align="center">

<img src="docs/MCDM_Studio_logo.png" alt="MCDM Studio — ProfBru" width="420"/>

**ProfBru © 2026**

**MCDM Studio — Modèles de Décision Multicritère**
Auteur: **ProfBru - Bruno Penedo** © 2026 — **TOUS DROITS RÉSERVÉS**
📧 profbruanbima@gmail.com

</div>

Projet **propriétaire**. Ce dépôt n'accorde aucune licence d'utilisation, de copie, de modification, de distribution ou d'œuvre dérivée. Tout usage commercial, académique ou institutionnel requiert l'autorisation écrite de l'auteur.

**Attribution de tiers:** les méthodes multicritères sont l'œuvre de leurs créateurs respectifs — Saaty, Roy, Bertier, Brans, Vincke, Keeney, Raiffa, Ensslin, Montibeller, Noronha, Gabus, Fontela, Opricovic, Tzeng, Hwang, Yoon, Kahneman, Tversky, Borda, Copeland, Gomes, Lima, Santos, Teixeira, Moreira, Rangel, Neves, Hein, Kroenke, Keunecke et Gomes Júnior — crédités individuellement dans le code source.
