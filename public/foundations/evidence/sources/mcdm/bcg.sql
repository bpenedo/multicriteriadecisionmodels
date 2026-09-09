-- Matriz BCG: quadrante de cada alternativa, cruzado com a posição no consenso.
-- Os eixos vêm dos MESMOS pesos do DEMATEL que alimentam os nove métodos,
-- renormalizados dentro dos grupos de benefício e de custo.
SELECT b.id_caso, b.alternativa, a.rotulo, b.atratividade, b.posicao,
       b.quadrante, b.corte_atratividade, b.corte_posicao, b.rank_consenso,
       CASE b.quadrante
            WHEN 'ESTRELA'      THEN '⭐ Estrela'
            WHEN 'VACA'         THEN '🐄 Vaca leiteira'
            WHEN 'INTERROGACAO' THEN '❓ Interrogação'
            WHEN 'ABACAXI'      THEN '🐕 Abacaxi'
       END AS quadrante_rotulo,
       CASE b.quadrante
            WHEN 'ESTRELA'      THEN 'investir e padronizar'
            WHEN 'VACA'         THEN 'colher — melhor entrega por unidade de sacrifício'
            WHEN 'INTERROGACAO' THEN 'decisão de investimento: o prêmio se justifica?'
            WHEN 'ABACAXI'      THEN 'descartar — nem entrega, nem é barata'
       END AS acao
FROM bcg_quadrante b
JOIN alternativa a ON a.id_caso = b.id_caso AND a.alternativa = b.alternativa
ORDER BY b.id_caso, b.rank_consenso;
