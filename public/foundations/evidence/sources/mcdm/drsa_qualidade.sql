-- QUALIDADE da aproximação do DRSA, por caso.
--
-- `gamma` (γ) é a fração dos objetos que a relação de dominância classifica sem
-- ambiguidade. γ = 1 significa que nenhum par viola a dominância: a decisão
-- passada é coerente e as regras a descrevem inteiramente. γ < 1 é diagnóstico,
-- não defeito — diz que o histórico contém pares em que a alternativa dominada
-- foi preferida, e `n_violacoes` conta quantos.
SELECT id_caso, gamma, n_classes, n_ambiguas, n_violacoes, n_regras
FROM drsa_qualidade
ORDER BY id_caso;
