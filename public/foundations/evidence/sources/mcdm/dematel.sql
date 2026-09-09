-- DEMATEL: R, C, proeminência (R+C), relação (R−C), papel causa/efeito e peso.
SELECT d.id_caso, d.criterio, d.rotulo,
       d.r AS influencia_exercida,   -- R: soma da linha de T
       d.c AS influencia_recebida,   -- C: soma da coluna de T
       d.prominencia, d.relacao,
       d.papel, d.peso, cr.unidade, cr.direcao
FROM dematel_criterio d
JOIN criterio cr ON cr.id_caso = d.id_caso AND cr.criterio = d.criterio
ORDER BY d.id_caso, d.prominencia DESC;
