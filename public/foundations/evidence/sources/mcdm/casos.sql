-- Catálogo de casos de decisão com o veredito de cada um.
SELECT c.id_caso, c.nome, c.dominio, c.descricao, c.decisor,
       v.vencedor, a.rotulo AS vencedor_rotulo, v.prob_vitoria,
       v.classificacao, v.vice, v.prob_vice, v.n_metodos,
       -- Total de MODELOS aplicados ao caso: os que ordenam (n_metodos) mais o BWM
       -- e o DRSA, que rodaram e gravaram mas não produzem posição de alternativa.
       -- Derivado do banco, nunca escrito à mão: o número que envelhece é o literal.
       v.n_metodos
         + (SELECT COUNT(DISTINCT 1) FROM bwm_peso b WHERE b.id_caso = c.id_caso)
         + (SELECT COUNT(DISTINCT 1) FROM drsa_qualidade q WHERE q.id_caso = c.id_caso)
         AS n_modelos,
       v.n_alternativas, v.unanimidade
FROM caso c
LEFT JOIN veredito v ON v.id_caso = c.id_caso
LEFT JOIN alternativa a ON a.id_caso = v.id_caso AND a.alternativa = v.vencedor
ORDER BY c.dominio, c.nome;
