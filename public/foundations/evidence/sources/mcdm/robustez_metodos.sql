-- Probabilidade de vitória por método: revela consenso que mascara divergência.
SELECT r.id_caso, r.alternativa, a.rotulo, r.metodo, r.prob_vitoria
FROM mcdm_robustez r
JOIN alternativa a ON a.id_caso = r.id_caso AND a.alternativa = r.alternativa
WHERE r.metodo <> 'CONSENSO (Borda)'
ORDER BY r.id_caso, r.metodo, r.prob_vitoria DESC;
