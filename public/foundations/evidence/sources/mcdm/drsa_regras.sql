-- REGRAS induzidas pelo DRSA (Greco, Matarazzo & Słowiński).
--
-- Os outros onze modelos pedem preferências DECLARADAS — pesos, comparações,
-- limiares. O DRSA faz o caminho inverso: recebe decisões já tomadas (as classes
-- em que as alternativas caíram) e devolve a regra que as explica, legível por
-- quem não sabe o que é normalização vetorial.
--
-- `certeza` é a fração dos objetos cobertos pela condição que de fato pertencem
-- à classe: regra com certeza 1 é certa no sentido da aproximação inferior.
SELECT id_caso, n_regra, classe_min, condicoes, cobertura, certeza, texto
FROM drsa_regra
ORDER BY id_caso, classe_min DESC, cobertura DESC, n_regra;
