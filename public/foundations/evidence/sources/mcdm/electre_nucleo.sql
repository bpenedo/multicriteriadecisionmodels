-- ELECTRE I: núcleo (kernel) — quem não é sobreclassificado por ninguém.
SELECT e.id_caso, e.alternativa, a.rotulo, e.no_nucleo, e.domina, e.dominada
FROM electre_nucleo e
JOIN alternativa a ON a.id_caso = e.id_caso AND a.alternativa = e.alternativa
ORDER BY e.id_caso, e.no_nucleo DESC, e.domina DESC;
