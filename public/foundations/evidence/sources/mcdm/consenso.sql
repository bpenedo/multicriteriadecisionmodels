-- Consenso de Borda entre os métodos, cruzado com a robustez.
SELECT c.id_caso, c.alternativa, a.rotulo, c.rank_medio, c.borda,
       c.rank_final, c.unanime,
       r.prob_vitoria, r.prob_top3, r.rank_p05, r.rank_p95
FROM decisao_consenso c
JOIN alternativa a ON a.id_caso = c.id_caso AND a.alternativa = c.alternativa
LEFT JOIN mcdm_robustez r
  ON r.id_caso = c.id_caso AND r.alternativa = c.alternativa
 AND r.metodo = 'CONSENSO (Borda)'
ORDER BY c.id_caso, c.rank_final;
