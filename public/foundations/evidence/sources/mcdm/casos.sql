-- Catálogo de casos de decisão com o veredito de cada um.
SELECT c.id_caso, c.nome, c.dominio, c.descricao, c.decisor,
       v.vencedor, a.rotulo AS vencedor_rotulo, v.prob_vitoria,
       v.classificacao, v.vice, v.prob_vice, v.n_metodos,
       v.n_alternativas, v.unanimidade
FROM caso c
LEFT JOIN veredito v ON v.id_caso = c.id_caso
LEFT JOIN alternativa a ON a.id_caso = v.id_caso AND a.alternativa = v.vencedor
ORDER BY c.dominio, c.nome;
