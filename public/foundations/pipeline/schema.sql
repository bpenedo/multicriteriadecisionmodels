-- MCDM Studio — Modelos Multicritério de Decisão
-- Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
-- E-mail: profbruanbima@gmail.com
--
-- Schema GENÉRICO de decisão multicritério.
--
-- Diferença arquitetural em relação ao framework de origem (Framework_VPL_ProjetosIA):
-- lá o schema era acoplado ao domínio (project_name, vpl, tir, kpi_psr...). Aqui a
-- unidade é o CASO DE DECISÃO — um par (alternativas × critérios) sem qualquer
-- semântica de negócio embutida. É o que permite o mesmo motor ranquear celulares,
-- carros elétricos, aeronaves de caça, fornecedores ou projetos de startup.
--
-- Idempotente: toda criação usa a cláusula IF NOT EXISTS.
-- (a frase evita a forma literal, que faria `grep -c` contar este comentário
--  como se fosse uma tabela — foi o que produziu a contagem errada de 18)

-- ---------------------------------------------------------------------------
-- 1. ESTRUTURA DO PROBLEMA (entrada)
-- ---------------------------------------------------------------------------

-- Um caso de decisão: "qual celular comprar", "qual caça adquirir", ...
CREATE TABLE IF NOT EXISTS caso (
    id_caso     TEXT PRIMARY KEY,
    nome        TEXT NOT NULL,
    dominio     TEXT,      -- consumo | automotivo | defesa | corporativo | startup | ti
    descricao   TEXT,
    decisor     TEXT,      -- quem decide (perfil de preferência)
    criado_em   TEXT DEFAULT (datetime('now'))
);

-- Alternativas discretas do caso (MADM: conjunto finito conhecido a priori).
CREATE TABLE IF NOT EXISTS alternativa (
    id_caso     TEXT NOT NULL,
    alternativa TEXT NOT NULL,
    rotulo      TEXT,
    ordem       INTEGER,
    PRIMARY KEY (id_caso, alternativa),
    FOREIGN KEY (id_caso) REFERENCES caso(id_caso)
);

-- Critérios de avaliação. direcao: 'benefit' (maior é melhor) | 'cost' (menor é melhor).
CREATE TABLE IF NOT EXISTS criterio (
    id_caso  TEXT NOT NULL,
    criterio TEXT NOT NULL,
    rotulo   TEXT,
    direcao  TEXT NOT NULL CHECK (direcao IN ('benefit', 'cost')),
    unidade  TEXT,
    ordem    INTEGER,
    PRIMARY KEY (id_caso, criterio),
    FOREIGN KEY (id_caso) REFERENCES caso(id_caso)
);

-- Matriz de decisão em formato longo: valor de cada alternativa em cada critério.
CREATE TABLE IF NOT EXISTS avaliacao (
    id_caso     TEXT NOT NULL,
    alternativa TEXT NOT NULL,
    criterio    TEXT NOT NULL,
    valor       REAL NOT NULL,
    PRIMARY KEY (id_caso, alternativa, criterio),
    FOREIGN KEY (id_caso, alternativa) REFERENCES alternativa(id_caso, alternativa),
    FOREIGN KEY (id_caso, criterio)    REFERENCES criterio(id_caso, criterio)
);

-- Matriz de RELAÇÃO DIRETA do DEMATEL (julgamento de especialista, 0..4).
CREATE TABLE IF NOT EXISTS dematel_entrada (
    id_caso     TEXT NOT NULL,
    origem      TEXT NOT NULL,
    destino     TEXT NOT NULL,
    intensidade REAL NOT NULL,   -- 0 nenhuma · 1 baixa · 2 média · 3 alta · 4 muito alta
    PRIMARY KEY (id_caso, origem, destino)
);

-- Matriz de comparação par a par de Saaty para o AHP (escala 1/9 .. 9).
CREATE TABLE IF NOT EXISTS ahp_entrada (
    id_caso  TEXT NOT NULL,
    linha    TEXT NOT NULL,
    coluna   TEXT NOT NULL,
    valor    REAL NOT NULL,
    PRIMARY KEY (id_caso, linha, coluna)
);

-- ---------------------------------------------------------------------------
-- 2. RESULTADOS (saída dos métodos)
-- ---------------------------------------------------------------------------

-- DEMATEL: papel causal e peso derivado por influência.
CREATE TABLE IF NOT EXISTS dematel_criterio (
    id_caso      TEXT NOT NULL,
    criterio     TEXT NOT NULL,
    rotulo       TEXT,
    r            REAL,     -- soma da linha da matriz total T (influência exercida)
    c            REAL,     -- soma da coluna da matriz total T (influência recebida)
    prominencia  REAL,     -- R + C  (importância no sistema)
    relacao      REAL,     -- R - C  (> 0 = causa; < 0 = efeito)
    papel        TEXT,     -- 'causa' | 'efeito'
    peso         REAL,     -- peso derivado, normalizado para somar 1
    PRIMARY KEY (id_caso, criterio)
);

-- DEMATEL: arestas da matriz de relação total T.
CREATE TABLE IF NOT EXISTS dematel_relacao (
    id_caso       TEXT NOT NULL,
    origem        TEXT NOT NULL,
    destino       TEXT NOT NULL,
    intensidade   REAL,     -- t_ij da matriz de relação total
    acima_limiar  INTEGER,  -- 1 se t_ij > limiar alpha (aresta do diagrama de influência)
    PRIMARY KEY (id_caso, origem, destino)
);

-- AHP: pesos por autovetor principal + razão de consistência do caso.
CREATE TABLE IF NOT EXISTS ahp_peso (
    id_caso   TEXT NOT NULL,
    criterio  TEXT NOT NULL,
    peso      REAL,
    cr        REAL,     -- razão de consistência (mesma para todo o caso; CR < 0,10 = aceitável)
    consistente INTEGER, -- 1 se CR < 0,10
    PRIMARY KEY (id_caso, criterio)
);

-- AHP Fuzzy — Buckley (1985). Terceira fonte de pesos, ao lado do DEMATEL e do
-- AHP crisp. Guarda o TFN inteiro (l, m, u), não só o centroide: é o espalhamento
-- que diz se a ordem dos pesos sobrevive à imprecisão do julgamento. Descartar
-- l e u aqui jogaria fora exatamente a informação que motivou rodar fuzzy.
CREATE TABLE IF NOT EXISTS ahp_fuzzy_peso (
    id_caso    TEXT NOT NULL,
    criterio   TEXT NOT NULL,
    peso       REAL,    -- centroide (l+m+u)/3, normalizado para somar 1
    l          REAL,    -- limite inferior do TFN
    m          REAL,    -- valor modal
    u          REAL,    -- limite superior do TFN
    fator      REAL,    -- fator geométrico g do espalhamento (1 = sem espalhamento)
    fuzziness  REAL,    -- Φ = Σ(u−l)/Σm — o mesmo para todo o caso
    PRIMARY KEY (id_caso, criterio)
);

-- BWM — Rezaei (2015/2016). QUARTA fonte de pesos. O que o distingue das outras
-- três não é o resultado, é o CUSTO DE ELICITAÇÃO: 2n−3 comparações contra as
-- n(n−1)/2 do AHP (15 contra 36, para 9 critérios). Guardamos o nº de comparações
-- junto porque é o argumento do método, não um detalhe.
CREATE TABLE IF NOT EXISTS bwm_peso (
    id_caso       TEXT NOT NULL,
    criterio      TEXT NOT NULL,
    peso          REAL,
    melhor        INTEGER,  -- 1 se é o critério eleito MELHOR
    pior          INTEGER,  -- 1 se é o eleito PIOR
    ksi           REAL,     -- ξᴸ* do programa linear (0 = julgamento coerente)
    cr            REAL,     -- razão de consistência ξᴸ*/CI(a_BW)
    consistente   INTEGER,
    n_comparacoes INTEGER,  -- 2n−3
    n_comp_ahp    INTEGER,  -- n(n−1)/2, para contraste
    PRIMARY KEY (id_caso, criterio)
);

-- DRSA — Greco, Matarazzo & Słowiński. Não produz score: produz REGRAS legíveis
-- induzidas das classes observadas, e a qualidade da aproximação γ, que denuncia
-- violação do princípio de dominância nos próprios dados.
CREATE TABLE IF NOT EXISTS drsa_regra (
    id_caso     TEXT NOT NULL,
    n_regra     INTEGER NOT NULL,
    classe_min  INTEGER,  -- "ENTÃO classe ≥ classe_min"
    condicoes   TEXT,     -- texto legível: "maturidade ≥ 15 E time ≥ 8.2"
    cobertura   INTEGER,  -- quantas alternativas a regra cobre
    certeza     REAL,     -- 1.0 (só induzimos regras CERTAS)
    texto       TEXT,     -- a frase inteira, pronta para o relatório
    PRIMARY KEY (id_caso, n_regra)
);

-- DRSA — diagnóstico por caso (uma linha), separado das regras.
CREATE TABLE IF NOT EXISTS drsa_qualidade (
    id_caso      TEXT PRIMARY KEY,
    gamma        REAL,     -- fração não ambígua; γ < 1 = inconsistência NOS DADOS
    n_classes    INTEGER,
    n_ambiguas   INTEGER,
    n_violacoes  INTEGER,  -- pares em que o dominante foi classificado pior
    n_regras     INTEGER
);

-- AHP-TOPSIS 2N: coeficiente de proximidade nas duas normalizações.
CREATE TABLE IF NOT EXISTS decisao_topsis (
    id_caso     TEXT NOT NULL,
    alternativa TEXT NOT NULL,
    ci_vector   REAL,     -- closeness coefficient (normalização vetorial/Euclidiana)
    ci_minmax   REAL,     -- closeness coefficient (normalização min-max/linear)
    ci_final    REAL,     -- média das duas (ranking final)
    rank_final  INTEGER,
    rank_vector INTEGER,
    rank_minmax INTEGER,
    concordante INTEGER,  -- 1 se as duas normalizações concordam na posição
    PRIMARY KEY (id_caso, alternativa)
);

-- Score e posição de cada alternativa em cada método (formato longo).
CREATE TABLE IF NOT EXISTS decisao_mcdm (
    id_caso     TEXT NOT NULL,
    alternativa TEXT NOT NULL,
    metodo      TEXT NOT NULL,  -- 'ELECTRE I' | 'PROMETHEE II' | 'MAUT' | 'MCDA-C' | 'AHP-TOPSIS 2n'
    score       REAL,
    rank_       INTEGER,
    PRIMARY KEY (id_caso, alternativa, metodo)
);

-- ELECTRE I: núcleo (kernel) das alternativas não dominadas.
CREATE TABLE IF NOT EXISTS electre_nucleo (
    id_caso     TEXT NOT NULL,
    alternativa TEXT NOT NULL,
    no_nucleo   INTEGER,  -- 1 se pertence ao núcleo (não é sobreclassificada por ninguém)
    domina      INTEGER,  -- quantas alternativas ela sobreclassifica
    dominada    INTEGER,  -- por quantas é sobreclassificada
    PRIMARY KEY (id_caso, alternativa)
);

-- Consenso de Borda entre os métodos.
CREATE TABLE IF NOT EXISTS decisao_consenso (
    id_caso       TEXT NOT NULL,
    alternativa   TEXT NOT NULL,
    rank_medio    REAL,     -- média das posições entre os métodos
    borda         INTEGER,  -- pontos de Borda (n - posição), somados
    rank_final    INTEGER,
    unanime       INTEGER,  -- 1 se todos os métodos deram a mesma posição
    PRIMARY KEY (id_caso, alternativa)
);

-- Robustez sob perturbação de Dirichlet nos pesos.
CREATE TABLE IF NOT EXISTS mcdm_robustez (
    id_caso       TEXT NOT NULL,
    alternativa   TEXT NOT NULL,
    metodo        TEXT NOT NULL,  -- método de ranqueamento ou 'CONSENSO (Borda)'
    prob_vitoria  REAL,     -- % das simulações em que ficou em 1º
    prob_top3     REAL,     -- % em que ficou entre as 3 primeiras
    rank_medio    REAL,
    rank_p05      REAL,     -- percentil 5% da posição (melhor caso plausível)
    rank_p95      REAL,     -- percentil 95% da posição (pior caso plausível)
    PRIMARY KEY (id_caso, alternativa, metodo)
);

-- Distribuição completa das posições no consenso (histograma do dashboard).
CREATE TABLE IF NOT EXISTS mcdm_robustez_dist (
    id_caso     TEXT NOT NULL,
    alternativa TEXT NOT NULL,
    posicao     INTEGER,
    frequencia  INTEGER,
    pct         REAL,
    PRIMARY KEY (id_caso, alternativa, posicao)
);

-- Veredito final legível por humano (o que vai para o comitê).
CREATE TABLE IF NOT EXISTS veredito (
    id_caso        TEXT PRIMARY KEY,
    vencedor       TEXT,
    prob_vitoria   REAL,     -- % dos universos de preferência em que o vencedor vence
    classificacao  TEXT,     -- 'ROBUSTO' | 'PROVÁVEL' | 'FRÁGIL'
    vice           TEXT,
    prob_vice      REAL,
    n_metodos      INTEGER,
    n_alternativas INTEGER,
    unanimidade    REAL,     -- % de alternativas com posição unânime entre métodos
    gerado_em      TEXT DEFAULT (datetime('now'))
);

-- Matriz BCG: quadrante de cada alternativa dentro da sua categoria.
-- Eixos derivados dos MESMOS pesos do DEMATEL que alimentam os dez métodos,
-- renormalizados dentro dos grupos de benefício e de custo.
CREATE TABLE IF NOT EXISTS bcg_quadrante (
    id_caso            TEXT NOT NULL,
    alternativa        TEXT NOT NULL,
    atratividade       REAL,     -- eixo Y: desempenho ponderado nos critérios de BENEFÍCIO
    posicao            REAL,     -- eixo X: posição ponderada nos critérios de CUSTO
    quadrante          TEXT,     -- 'ESTRELA' | 'VACA' | 'INTERROGACAO' | 'ABACAXI'
    corte_atratividade REAL,     -- mediana do eixo Y neste caso
    corte_posicao      REAL,     -- mediana do eixo X neste caso
    rank_consenso      INTEGER,  -- posição no consenso de Borda, para o cruzamento
    PRIMARY KEY (id_caso, alternativa)
);

-- Índices de leitura do dashboard.
CREATE INDEX IF NOT EXISTS ix_avaliacao_caso    ON avaliacao(id_caso);
CREATE INDEX IF NOT EXISTS ix_decisao_mcdm_caso ON decisao_mcdm(id_caso, metodo);
CREATE INDEX IF NOT EXISTS ix_robustez_caso     ON mcdm_robustez(id_caso, metodo);

CREATE INDEX IF NOT EXISTS ix_bcg_caso ON bcg_quadrante(id_caso, quadrante);
