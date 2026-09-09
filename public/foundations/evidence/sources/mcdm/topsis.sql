-- AHP-TOPSIS 2N: as duas normalizações e a concordância entre elas.
SELECT t.id_caso, t.alternativa, a.rotulo, t.ci_vector, t.ci_minmax, t.ci_final,
       t.rank_final, t.rank_vector, t.rank_minmax, t.concordante
FROM decisao_topsis t
JOIN alternativa a ON a.id_caso = t.id_caso AND a.alternativa = t.alternativa
ORDER BY t.id_caso, t.rank_final;
