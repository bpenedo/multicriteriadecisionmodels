-- QUATRO famílias de peso sobre o mesmo problema:
--   DEMATEL   — influência sistêmica (não conta a mesma coisa duas vezes)
--   AHP       — julgamento par a par, pontual
--   AHP Fuzzy — o MESMO julgamento, com a imprecisão preservada (Buckley, 1985)
--   BWM       — só o melhor e o pior critério: 2n−3 comparações em vez de
--               n(n−1)/2, preenchível onde a matriz de Saaty não é (Rezaei, 2015)
--
-- O espalhamento (l, u) vem junto de propósito: é ele que diz se a ordem dos pesos
-- sobrevive à imprecisão que o decisor de fato tem. Trazer só o centroide faria o
-- AHP Fuzzy parecer "mais um número", que é justamente o que ele não é.
SELECT d.id_caso, d.rotulo, d.papel,
       d.peso AS peso_dematel,
       h.peso AS peso_ahp,
       f.peso AS peso_ahp_fuzzy,
       f.l AS fuzzy_l, f.m AS fuzzy_m, f.u AS fuzzy_u,
       (f.u - f.l) AS fuzzy_amplitude,
       f.fuzziness,
       b.peso AS peso_bwm,
       b.ksi AS bwm_ksi, b.cr AS bwm_cr, b.consistente AS bwm_consistente,
       b.n_comparacoes AS bwm_n_comp, b.n_comp_ahp AS bwm_n_comp_ahp,
       (h.peso - b.peso) AS divergencia_bwm,
       (d.peso - h.peso) AS divergencia,
       (h.peso - f.peso) AS divergencia_fuzzy,
       h.cr, h.consistente
FROM dematel_criterio d
JOIN ahp_peso h ON h.id_caso = d.id_caso AND h.criterio = d.criterio
LEFT JOIN ahp_fuzzy_peso f ON f.id_caso = d.id_caso AND f.criterio = d.criterio
LEFT JOIN bwm_peso b ON b.id_caso = d.id_caso AND b.criterio = d.criterio
ORDER BY d.id_caso, ABS(d.peso - h.peso) DESC;
