-- Posição de cada alternativa em cada escola de decisão (formato longo).
SELECT m.id_caso, m.alternativa, a.rotulo, m.metodo, m.score, m.rank_
FROM decisao_mcdm m
JOIN alternativa a ON a.id_caso = m.id_caso AND a.alternativa = m.alternativa
ORDER BY m.id_caso, m.metodo, m.rank_;
