-- Robustez do consenso sob perturbação de Dirichlet nos pesos.
SELECT r.id_caso, r.alternativa, a.rotulo, r.prob_vitoria, r.prob_top3,
       r.rank_medio, r.rank_p05, r.rank_p95
FROM mcdm_robustez r
JOIN alternativa a ON a.id_caso = r.id_caso AND a.alternativa = r.alternativa
WHERE r.metodo = 'CONSENSO (Borda)'
ORDER BY r.id_caso, r.prob_vitoria DESC;
