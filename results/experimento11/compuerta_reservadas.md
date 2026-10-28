# Costo de la doble compuerta sobre las consultas reservadas (T-protocolo)

Filas: una por consulta reservada y semilla (171 × 10 por corte), primer sorteo. «Directorio acepta»: `route_transactive` da destino. «Compuerta rechaza»: el destino no da `recognize_gated > 0` para ninguna pista. Entre las rechazadas, «pierde respuesta» son las que sí tenían recall (`responde`), separadas por si el destino era el correcto.

| corte | consultas | directorio acepta | compuerta rechaza | pierde respuesta, ruteo ok (clase ok) | pierde respuesta, ruteo mal | sin respuesta de todos modos |
|---|---|---|---|---|---|---|
| 25 | 1710 | 1710 (100.0 %) | 35 (2.05 % de las aceptadas) | 0 (0) | 0 | 35 |
| 50 | 1710 | 1710 (100.0 %) | 20 (1.17 % de las aceptadas) | 0 (0) | 0 | 20 |
| 100 | 1710 | 1710 (100.0 %) | 22 (1.29 % de las aceptadas) | 0 (0) | 0 | 22 |
| 200 | 1710 | 1710 (100.0 %) | 26 (1.52 % de las aceptadas) | 0 (0) | 0 | 26 |

Consultas rechazadas por la compuerta, agregadas por consulta y destino (semillas: en cuántas de las 10 ocurre):

| corte | consulta | clase | destino | ruteo ok | respondía | semillas |
|---|---|---|---|---|---|---|
| 25 | a cow swishing its tail at flies | cow | dog | False | False | 10 |
| 25 | a cow with a bell around its neck | cow | pear | False | False | 9 |
| 25 | a mare and foal in a pasture | horse | cow | False | False | 6 |
| 25 | a dog sleeping on a soft bed | dog | apple | False | False | 4 |
| 25 | a mare and foal in a pasture | horse | apple | False | False | 4 |
| 25 | a horse with strong hooves | horse | cow | False | False | 2 |
| 50 | a mare and foal in a pasture | horse | cow | False | False | 10 |
| 50 | a cow with a bell around its neck | cow | pear | False | False | 6 |
| 50 | a cow swishing its tail at flies | cow | dog | False | False | 4 |
| 100 | a mare and foal in a pasture | horse | cow | False | False | 10 |
| 100 | a cow with a bell around its neck | cow | pear | False | False | 7 |
| 100 | a cow swishing its tail at flies | cow | dog | False | False | 5 |
| 200 | a mare and foal in a pasture | horse | cow | False | False | 10 |
| 200 | a cow swishing its tail at flies | cow | dog | False | False | 8 |
| 200 | a cow with a bell around its neck | cow | pear | False | False | 8 |
