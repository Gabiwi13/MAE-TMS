# Costo de la doble compuerta sobre las consultas reservadas (T-protocolo)

Filas: una por consulta reservada y semilla (171 × 10 por corte), primer sorteo. «Directorio acepta»: `route_transactive` da destino. «Compuerta rechaza»: el destino no da `recognize_gated > 0` para ninguna pista. Entre las rechazadas, «pierde respuesta» son las que sí tenían recall (`responde`), separadas por si el destino era el correcto.

| corte | consultas | directorio acepta | compuerta rechaza | pierde respuesta, ruteo ok (clase ok) | pierde respuesta, ruteo mal | sin respuesta de todos modos |
|---|---|---|---|---|---|---|
| 25 | 1710 | 1710 (100.0 %) | 361 (21.11 % de las aceptadas) | 0 (0) | 0 | 361 |
| 50 | 1710 | 1710 (100.0 %) | 26 (1.52 % de las aceptadas) | 0 (0) | 0 | 26 |
| 100 | 1710 | 1710 (100.0 %) | 24 (1.40 % de las aceptadas) | 0 (0) | 0 | 24 |
| 200 | 1710 | 1710 (100.0 %) | 24 (1.40 % de las aceptadas) | 0 (0) | 0 | 24 |

Consultas rechazadas por la compuerta, agregadas por consulta y destino (semillas: en cuántas de las 10 ocurre):

| corte | consulta | clase | destino | ruteo ok | respondía | semillas |
|---|---|---|---|---|---|---|
| 25 | a car parked at the curb | car | car | True | False | 10 |
| 25 | a car parked in a garage | car | car | True | False | 10 |
| 25 | a car refueling at a station | car | car | True | False | 10 |
| 25 | a car with a dashboard and steering wheel | car | car | True | False | 10 |
| 25 | a car with a full tank of fuel | car | car | True | False | 10 |
| 25 | a car with a steering wheel | car | car | True | False | 10 |
| 25 | a car with alloy wheels | car | car | True | False | 10 |
| 25 | a car with headlights on | car | car | True | False | 10 |
| 25 | a car with tinted windows | car | car | True | False | 10 |
| 25 | a dog guarding the front door | dog | dog | True | False | 10 |
| 25 | a dog howling at the moon | dog | dog | True | False | 10 |
| 25 | a dog jumping to catch a frisbee | dog | dog | True | False | 10 |
| 25 | a dog licking its paws | dog | dog | True | False | 10 |
| 25 | a dog panting after a walk | dog | dog | True | False | 10 |
| 25 | a dog resting its paws on the floor | dog | dog | True | False | 10 |
| 25 | a dog sleeping on a soft bed | dog | apple | False | False | 10 |
| 25 | a dog wagging its tail at the door | dog | dog | True | False | 10 |
| 25 | a dog with a collar and tag | dog | dog | True | False | 10 |
| 25 | a dog with floppy ears | dog | dog | True | False | 10 |
| 25 | a family car with seats for five | car | car | True | False | 10 |
| 25 | a horse grazing in a paddock | horse | horse | True | False | 10 |
| 25 | a horse trained for a race | horse | horse | True | False | 10 |
| 25 | a horse with shiny hooves | horse | horse | True | False | 10 |
| 25 | a mare and foal in a pasture | horse | cow | False | False | 10 |
| 25 | a sedan car on the street | car | car | True | False | 10 |
| 25 | a shiny new car | car | car | True | False | 10 |
| 25 | a dog digging in the garden | dog | tomato | False | False | 9 |
| 25 | a horse cantering across a field | horse | cow | False | False | 9 |
| 25 | a horse pulling a cart | horse | horse | True | False | 9 |
| 25 | a horse trotting down a trail | horse | horse | True | False | 9 |
| 25 | a horse with a bridle and reins | horse | horse | True | False | 9 |
| 25 | a stable full of horses | horse | horse | True | False | 9 |
| 25 | a wild horse galloping free | horse | horse | True | False | 9 |
| 25 | a horse in a stable eating hay | horse | horse | True | False | 8 |
| 25 | a horse with strong hooves | horse | horse | True | False | 8 |
| 25 | a cow swishing its tail at flies | cow | dog | False | False | 6 |
| 25 | a cow with a bell around its neck | cow | pear | False | False | 6 |
| 25 | a horse with strong hooves | horse | cow | False | False | 2 |
| 25 | a dog digging in the garden | dog | dog | True | False | 1 |
| 25 | a horse being ridden by a rider | horse | cow | False | False | 1 |
| 25 | a horse cantering across a field | horse | horse | True | False | 1 |
| 25 | a horse pulling a cart | horse | cow | False | False | 1 |
| 25 | a horse trotting down a trail | horse | cow | False | False | 1 |
| 25 | a horse with a bridle and reins | horse | cow | False | False | 1 |
| 25 | a spotted cow in a green field | cow | pear | False | False | 1 |
| 25 | a wild horse galloping free | horse | cow | False | False | 1 |
| 50 | a mare and foal in a pasture | horse | cow | False | False | 10 |
| 50 | a cow swishing its tail at flies | cow | dog | False | False | 6 |
| 50 | a cow with a bell around its neck | cow | pear | False | False | 2 |
| 50 | a horse cantering across a field | horse | cow | False | False | 2 |
| 50 | a horse with strong hooves | horse | cow | False | False | 2 |
| 50 | a spotted cow in a green field | cow | pear | False | False | 2 |
| 50 | a horse with a bridle and reins | horse | cow | False | False | 1 |
| 50 | a wild horse galloping free | horse | cow | False | False | 1 |
| 100 | a mare and foal in a pasture | horse | cow | False | False | 10 |
| 100 | a cow swishing its tail at flies | cow | dog | False | False | 6 |
| 100 | a cow with a bell around its neck | cow | pear | False | False | 2 |
| 100 | a horse cantering across a field | horse | cow | False | False | 2 |
| 100 | a horse with strong hooves | horse | cow | False | False | 2 |
| 100 | a spotted cow in a green field | cow | pear | False | False | 2 |
| 200 | a mare and foal in a pasture | horse | cow | False | False | 8 |
| 200 | a cow swishing its tail at flies | cow | dog | False | False | 6 |
| 200 | a cow with a bell around its neck | cow | pear | False | False | 2 |
| 200 | a horse cantering across a field | horse | cow | False | False | 2 |
| 200 | a horse with strong hooves | horse | cow | False | False | 2 |
| 200 | a mare and foal in a pasture | horse | apple | False | False | 2 |
| 200 | a horse with a bridle and reins | horse | cow | False | False | 1 |
| 200 | a wild horse galloping free | horse | cow | False | False | 1 |
