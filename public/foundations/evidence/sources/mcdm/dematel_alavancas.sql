-- As alavancas de cada caso: os critérios classificados como CAUSA pelo DEMATEL.
-- Agregado (uma linha por caso) para que o índice possa exibi-lo sem carregar as
-- 152 linhas da tabela de critérios nem as 1.192 da matriz de relação. Ver bugs.md #BUG-028.
SELECT d.id_caso, c.nome,
       COUNT(*)                                                        AS n_criterios,
       SUM(CASE WHEN d.papel = 'causa' THEN 1 ELSE 0 END)              AS n_causas,
       MAX(CASE WHEN d.papel = 'causa' THEN d.rotulo END)              AS alavanca_exemplo,
       (SELECT rotulo FROM dematel_criterio x
         WHERE x.id_caso = d.id_caso ORDER BY x.peso DESC LIMIT 1)     AS criterio_maior_peso,
       (SELECT ROUND(peso * 100, 1) FROM dematel_criterio x
         WHERE x.id_caso = d.id_caso ORDER BY x.peso DESC LIMIT 1)     AS maior_peso_pct,
       (SELECT rotulo FROM dematel_criterio x
         WHERE x.id_caso = d.id_caso AND x.papel = 'causa'
         ORDER BY x.relacao DESC LIMIT 1)                              AS causa_raiz,
       ROUND(MAX(d.relacao), 3)                                        AS relacao_maxima
FROM dematel_criterio d
JOIN caso c ON c.id_caso = d.id_caso
GROUP BY d.id_caso, c.nome
ORDER BY c.nome;
