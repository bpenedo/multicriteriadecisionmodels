-- Contagem por quadrante em cada categoria — o "mapa de oportunidades" do caso.
SELECT c.id_caso, c.nome, c.dominio,
       SUM(CASE WHEN b.quadrante = 'ESTRELA'      THEN 1 ELSE 0 END) AS estrelas,
       SUM(CASE WHEN b.quadrante = 'VACA'         THEN 1 ELSE 0 END) AS vacas,
       SUM(CASE WHEN b.quadrante = 'INTERROGACAO' THEN 1 ELSE 0 END) AS interrogacoes,
       SUM(CASE WHEN b.quadrante = 'ABACAXI'      THEN 1 ELSE 0 END) AS abacaxis,
       COUNT(*) AS total,
       MAX(CASE WHEN b.rank_consenso = 1 THEN b.quadrante END) AS quadrante_do_vencedor
FROM bcg_quadrante b JOIN caso c ON c.id_caso = b.id_caso
GROUP BY c.id_caso, c.nome, c.dominio
ORDER BY c.dominio, c.nome;
