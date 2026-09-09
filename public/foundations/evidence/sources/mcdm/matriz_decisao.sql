-- Matriz de decisão original (alternativas × critérios), com unidades.
SELECT av.id_caso, av.alternativa, al.rotulo AS alternativa_rotulo,
       av.criterio, cr.rotulo AS criterio_rotulo, cr.direcao, cr.unidade,
       av.valor
FROM avaliacao av
JOIN alternativa al ON al.id_caso = av.id_caso AND al.alternativa = av.alternativa
JOIN criterio cr   ON cr.id_caso = av.id_caso AND cr.criterio = av.criterio
ORDER BY av.id_caso, al.ordem, cr.ordem;
