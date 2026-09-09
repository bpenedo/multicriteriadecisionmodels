-- Histograma completo das posições no consenso.
SELECT d.id_caso, d.alternativa, a.rotulo, d.posicao, d.frequencia, d.pct
FROM mcdm_robustez_dist d
JOIN alternativa a ON a.id_caso = d.id_caso AND a.alternativa = d.alternativa
ORDER BY d.id_caso, d.alternativa, d.posicao;
