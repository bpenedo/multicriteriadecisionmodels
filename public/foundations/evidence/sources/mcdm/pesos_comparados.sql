-- Duas famílias de peso sobre o mesmo problema: influência sistêmica × julgamento par a par.
SELECT d.id_caso, d.rotulo, d.papel,
       d.peso AS peso_dematel, h.peso AS peso_ahp,
       (d.peso - h.peso) AS divergencia, h.cr, h.consistente
FROM dematel_criterio d
JOIN ahp_peso h ON h.id_caso = d.id_caso AND h.criterio = d.criterio
ORDER BY d.id_caso, ABS(d.peso - h.peso) DESC;
