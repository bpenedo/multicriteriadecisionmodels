-- Matriz de relação TOTAL do DEMATEL: T = X(I − X)⁻¹.
--
-- Cada célula t_ij é a influência de `origem` sobre `destino`, somando os caminhos
-- DIRETOS e INDIRETOS de qualquer comprimento (série de Neumann ΣXᵏ). É por isso que
-- a matriz total revela relações que a matriz de julgamento direto não mostra: um
-- critério pode influenciar outro fortemente sem que o especialista tenha declarado
-- qualquer ligação direta entre os dois.
--
-- `acima_limiar` = 1 quando t_ij supera o limiar α (a média de T): são essas as arestas
-- que entram no diagrama de influência, e o resto é ruído de arredondamento.
SELECT r.id_caso, r.origem, r.destino, r.intensidade, r.acima_limiar,
       co.rotulo AS origem_rotulo,
       cd.rotulo AS destino_rotulo,
       do_.papel  AS origem_papel,
       dd.papel   AS destino_papel
FROM dematel_relacao r
JOIN criterio co ON co.id_caso = r.id_caso AND co.criterio = r.origem
JOIN criterio cd ON cd.id_caso = r.id_caso AND cd.criterio = r.destino
LEFT JOIN dematel_criterio do_ ON do_.id_caso = r.id_caso AND do_.criterio = r.origem
LEFT JOIN dematel_criterio dd  ON dd.id_caso  = r.id_caso AND dd.criterio  = r.destino
WHERE r.origem <> r.destino
ORDER BY r.id_caso, r.intensidade DESC;
