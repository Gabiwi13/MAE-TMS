# Costo de la doble compuerta sobre las consultas reservadas (T-protocolo)

Filas: una por consulta reservada y semilla (171 × 10 por corte), primer sorteo. «Directorio acepta»: `route_transactive` da destino. «Compuerta rechaza»: el destino no da `recognize_gated > 0` para ninguna pista. Entre las rechazadas, «pierde respuesta» son las que sí tenían recall (`responde`), separadas por si el destino era el correcto.

| corte | consultas | directorio acepta | compuerta rechaza | pierde respuesta, ruteo ok (clase ok) | pierde respuesta, ruteo mal | sin respuesta de todos modos |
|---|---|---|---|---|---|---|
| 25 | 1710 | 1710 (100.0 %) | 28 (1.64 % de las aceptadas) | 0 (0) | 0 | 28 |
| 50 | 1710 | 1710 (100.0 %) | 22 (1.29 % de las aceptadas) | 0 (0) | 0 | 22 |
| 100 | 1710 | 1710 (100.0 %) | 22 (1.29 % de las aceptadas) | 0 (0) | 0 | 22 |
| 200 | 1710 | 1710 (100.0 %) | 23 (1.35 % de las aceptadas) | 0 (0) | 0 | 23 |

Consultas rechazadas por la compuerta, agregadas por consulta y destino (semillas: en cuántas de las 10 ocurre):

| corte | consulta | clase | destino | ruteo ok | respondía | semillas |
|---|---|---|---|---|---|---|
| 25 | a mare and foal in a pasture | horse | cow | False | False | 10 |
| 25 | a cow swishing its tail at flies | cow | dog | False | False | 4 |
| 25 | a cow with a bell around its neck | cow | pear | False | False | 4 |
| 25 | a horse cantering across a field | horse | cow | False | False | 3 |
| 25 | a horse with strong hooves | horse | cow | False | False | 3 |
| 25 | a horse grazing in a paddock | horse | cow | False | False | 1 |
| 25 | a horse with a bridle and reins | horse | cow | False | False | 1 |
| 25 | a horse with shiny hooves | horse | cow | False | False | 1 |
| 25 | a wild horse galloping free | horse | cow | False | False | 1 |
| 50 | a mare and foal in a pasture | horse | cow | False | False | 10 |
| 50 | a cow swishing its tail at flies | cow | dog | False | False | 4 |
| 50 | a horse cantering across a field | horse | cow | False | False | 2 |
| 50 | a cow with a bell around its neck | cow | pear | False | False | 1 |
| 50 | a horse being ridden by a rider | horse | cow | False | False | 1 |
| 50 | a horse pulling a cart | horse | cow | False | False | 1 |
| 50 | a horse trotting down a trail | horse | cow | False | False | 1 |
| 50 | a horse with a bridle and reins | horse | cow | False | False | 1 |
| 50 | a wild horse galloping free | horse | cow | False | False | 1 |
| 100 | a mare and foal in a pasture | horse | cow | False | False | 10 |
| 100 | a cow swishing its tail at flies | cow | dog | False | False | 4 |
| 100 | a horse cantering across a field | horse | cow | False | False | 2 |
| 100 | a cow with a bell around its neck | cow | pear | False | False | 1 |
| 100 | a horse being ridden by a rider | horse | cow | False | False | 1 |
| 100 | a horse pulling a cart | horse | cow | False | False | 1 |
| 100 | a horse trotting down a trail | horse | cow | False | False | 1 |
| 100 | a horse with a bridle and reins | horse | cow | False | False | 1 |
| 100 | a wild horse galloping free | horse | cow | False | False | 1 |
| 200 | a mare and foal in a pasture | horse | cow | False | False | 10 |
| 200 | a cow swishing its tail at flies | cow | dog | False | False | 4 |
| 200 | a horse cantering across a field | horse | cow | False | False | 2 |
| 200 | a cow with a bell around its neck | cow | pear | False | False | 1 |
| 200 | a horse being ridden by a rider | horse | cow | False | False | 1 |
| 200 | a horse grazing in a paddock | horse | cow | False | False | 1 |
| 200 | a horse pulling a cart | horse | cow | False | False | 1 |
| 200 | a horse trotting down a trail | horse | cow | False | False | 1 |
| 200 | a horse with a bridle and reins | horse | cow | False | False | 1 |
| 200 | a wild horse galloping free | horse | cow | False | False | 1 |
