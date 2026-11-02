# Calibración con un conjunto de evaluación fijo (jurado M2)

Worktree `MAE-TMS-lineasbase`, desacoplado en `df2f893`. Usa la lógica de `run_ablation.py` sin cambios; solo cambia qué consultas forman el directorio y cuáles se evalúan. Lee las `mem_dom_*.pkl` oficiales; no reentrena nada.

## Problema

- En `run_ablation.py` la fase madura se evalúa sobre las primeras N consultas, las mismas que forman el directorio.
- La composición de esas consultas cambia con N: la temprana, que no depende del directorio, sube de 82.5 a 90.0 % entre N = 200 y N = 400.
- En 7 de las 9 condiciones las 5 semillas dan resultados idénticos, porque la semilla solo sortea el agente de entrada y todos los directorios son iguales.

## Diseño (escrito antes de correr)

**Banco.** Las 411 consultas de `src/eval_bank.py` (`ALL_QUERIES`, `GROUND_TRUTH`).

**Conjunto de evaluación E.**
- 15 consultas por clase, 120 en total, sorteadas dentro de cada clase con `RandomState(0)`.
- Las de E nunca registran en el directorio.
- Elijo 15 y no 10 por clase: con 120 consultas una consulta vale 0.83 puntos (con 80 valdría 1.25), y aun así quedan 291 para formar, más que N = 200.
- Se reporta qué fracción de E trae el nombre de su clase.

**Resto R.** Las 291 consultas que no están en E.

**Formación.** Para cada semilla s ∈ {0, 1, 2, 3, 4}, con `rng = RandomState(100 + s)`:
- `A` y `B1`: las primeras N de una permutación aleatoria de R, sin estratificar.
- `D` y `G`: N // 8 por clase, sorteadas dentro de cada clase de R e intercaladas por clase, como `balanced_queries`. Si una clase tiene menos de N // 8 en R, entran todas (pasa con N máximo).
- N ∈ {50, 100, 200, 291}. Con N = 291, A y B1 usan R completo en todas las semillas y solo cambia el orden. Como el registro es aditivo y la temprana no depende del directorio, ahí la desviación entre semillas es 0 por construcción. D y G con N máximo toman 36 por clase o todas las que haya.

**Condiciones**, con `get_condition_config` de `run_ablation.py`:
- `A`: lectura cruda, `predict`.
- `B1`: ÷count, `predict_normalized(..., "linear")`.
- `D`: formación estratificada y lectura cruda.
- `G`: D + B1. F no quita nada, así que G usa las memorias oficiales, sin `build_curated_apple_mdom`.

**Corrida por (condición, N, semilla).**
1. Agentes y TME frescos (`make_agents`).
2. `run_early_phase` sobre las N de formación, que registra al ganador temprano en los directorios igual que el sistema.
3. `run_mature_phase` sobre E con `rng = RandomState(s*1000 + 42)`, como en `run_single_experiment`.
4. La temprana sobre E con `run_early_phase` en agentes desechables. No depende del directorio, así que es la misma en todas las corridas.

**Métricas sobre E.**
- temprana, madura, fidelidad (madura = temprana) y la diferencia madura − temprana, con REJ como fallo y denominador 120;
- también la temprana sobre las N de formación, para ver cómo cambia su composición con N, y la fracción de la formación que trae el nombre de la clase.

**Intervalos.**
- Entre semillas: media, desviación estándar, mínimo, máximo e intervalo t del 95 % (t₀.₉₇₅,₄ = 2.776).
- Por el tamaño de E: bootstrap pareado sobre las consultas de E (2000 remuestreos, `RandomState(7)`) de la diferencia madura − temprana promediada entre semillas.

**Robustez, declarada.** Se repite todo con otros 4 sorteos de E (`RandomState(1..4)`) y se reporta la diferencia media por sorteo.

**Control.** Con la lógica original, `run_single_experiment` para A y B1 con N = 400 y semilla 0 debe dar temprana 90.0, madura A 85.25 y madura B1 93.0.

## Qué apoyaría o debilitaría cada lectura

- **La formación del directorio mejora la decisión en consultas que no vio.** Lo apoyaría que, con B1, madura − temprana sobre E sea positiva con un intervalo que excluya 0 y que crezca con N.
- **El crecimiento con N venía de la composición del conjunto y de evaluar dentro de muestra.** Lo apoyaría que la madura sobre E quede plana con N, o que madura − temprana sea ≈ 0 o negativa. Entonces lo que la tesis atribuye a la formación sería la dificultad de las consultas.
- **D y G.** Si con el mismo resto R su ventaja sobre A y B1 desaparece, la ventaja original venía de sortear del banco completo, con consultas más fáciles (M2).
- **B1 contra A.** Si B1 supera a A sobre E, la calibración ÷count no es un artefacto de la evaluación dentro de muestra.

## Resultados

**Tiempo.** 2462.7 s (41 min): el control 40 s y unos 480 s por cada sorteo de E (80 corridas). Va en `tiempos.txt`.

**Control.** La lógica original con N = 400 y semilla 0 da temprana 90.0, madura A 85.25 y madura B1 93.0, como en `results/ablation_mdir_bias`.

### Composición

| sorteo de E | consultas con el nombre de su clase (de 120) | temprana sobre E |
|---|---|---|
| 0 (principal) | 60 | 92.5 |
| 1 | 70 | 92.5 |
| 2 | 56 | 85.8 |
| 3 | 59 | 90.0 |
| 4 | 52 | 87.5 |

- Con formación sorteada, la composición ya no cambia con N: la fracción de la formación con el nombre de la clase queda entre 46 y 55 % para todo N.
- La temprana sobre la formación queda entre 87 y 92 % para todo N.
- En el diseño original, en cambio, la temprana subía de 82.5 a 90.0 entre N = 200 y 400.

### Sorteo principal E0 (media entre 5 semillas)

- IC t: intervalo entre semillas.
- Bootstrap: sobre las 120 consultas de E.
- Temprana sobre E: 92.5.

| condición | N | madura (IC t) | madura − temprana (IC t) | bootstrap sobre E | fidelidad |
|---|---|---|---|---|---|
| A | 50 | 77.8 [74.1, 81.5] | −14.7 [−18.4, −11.0] | [−20.0, −9.2] | 76.3 |
| A | 100 | 85.0 [81.3, 88.7] | −7.5 [−11.2, −3.8] | [−12.7, −2.0] | 82.5 |
| A | 200 | 86.2 [83.6, 88.8] | −6.3 [−8.9, −3.7] | [−11.3, −1.3] | 87.0 |
| A | 291 | 84.2 (de = 0) | −8.3 | [−15.0, −1.7] | 85.0 |
| **B1** | 50 | 81.5 [77.6, 85.4] | −11.0 [−14.9, −7.1] | [−16.0, −5.7] | 80.3 |
| **B1** | 100 | 89.8 [86.6, 93.1] | −2.7 [−5.9, +0.6] | [−6.8, +1.7] | 89.0 |
| **B1** | 200 | 91.7 [90.6, 92.7] | −0.8 [−1.9, +0.2] | [−5.2, +3.3] | 92.5 |
| **B1** | 291 | 91.7 (de = 0) | −0.8 | [−5.8, +4.2] | 92.5 |
| D | 48 | 77.8 [65.8, 89.9] | −14.7 [−26.8, −2.6] | [−19.8, −9.3] | 78.5 |
| D | 286 | 83.8 [83.3, 84.4] | −8.7 [−9.2, −8.1] | [−14.8, −2.3] | 85.7 |
| G | 48 | 81.8 [75.1, 88.6] | −10.7 [−17.4, −3.9] | [−15.5, −5.7] | 82.5 |
| G | 100 | 88.0 [82.9, 93.1] | −4.5 [−9.6, +0.6] | [−9.2, +0.3] | 87.2 |
| G | 200 | 91.0 [89.3, 92.7] | −1.5 [−3.2, +0.2] | [−5.3, +2.5] | 92.3 |
| G | 286 | 91.8 [90.7, 93.0] | −0.7 [−1.8, +0.5] | [−5.2, +3.8] | 93.0 |

D y G con N estratificado toman N // 8 por clase: 48, 96, 200 y 286 consultas. Todas las filas están en `filas.csv` y `resumen.json`.

### Los 5 sorteos de E juntos (25 corridas por celda)

| condición | N = 50 | 100 | 200 | 291 |
|---|---|---|---|---|
| A, madura | 74.4 | 80.8 | 82.9 | 82.2 |
| B1, madura | 78.9 | 86.0 | 89.8 | 91.0 |
| D, madura | 72.9 | 78.8 | 81.8 | 82.7 |
| G, madura | 79.7 | 86.1 | 89.9 | 91.3 |
| B1, madura − temprana (rango de medias por E) | −10.7 (−12.8 a −7.5) | −3.7 (−7.5 a +1.0) | +0.2 (−2.3 a +5.5) | +1.3 (−0.8 a +6.7) |
| G, madura − temprana (rango) | −9.9 (−11.3 a −7.2) | −3.6 (−5.7 a +0.5) | +0.3 (−1.5 a +4.2) | +1.7 (−0.7 a +6.3) |

- La temprana sobre E, en promedio de los 5 sorteos, es 89.7.
- Con B1 y N = 291, la madura supera a la temprana en 3 de los 5 sorteos: +0.8, +0.8 y +6.7. En los otros dos queda en −0.8.
- El +6.7 es el sorteo 2, donde la temprana es más baja (85.8): ahí el directorio gana, en neto, 8 consultas a la temprana.

### Lectura

- **La formación sí mejora la madura en consultas que no vio.**
  - Con B1, sobre conjuntos fijos, la madura sube de 78.9 a 91.0 % entre N = 50 y N = 291, y la desviación entre semillas baja con N.
  - Ese crecimiento no puede venir de la composición, porque el conjunto evaluado es el mismo para todo N.
- **Pero lo que crece es la madura acercándose a la temprana, no superándola.**
  - madura − temprana pasa de −10.7 a +0.2 (N = 200) y +1.3 (N = 291).
  - En el sorteo principal queda en −0.8 con N = 200 y con N = 291, con un bootstrap sobre E de unos ±5 puntos.
  - Ninguna diferencia positiva es robusta entre sorteos de E.
  - La cifra de la tesis, madura 93.0 contra temprana 90.0 dentro de muestra (+3.0), y el +5.5 de N = 200 (88.0 contra 82.5) no se reproducen con evaluación fija.
  - Lo defendible es que el directorio, ya formado con unas 200 consultas, reproduce la decisión temprana sin el broadcast (fidelidad de 92–93 % en E0) con un acierto equivalente.
- **D y G no tienen ventaja propia.** Con el mismo resto R, D queda por debajo de A salvo con N máximo (82.7 contra 82.2) y G igual que B1 (91.3 contra 91.0). La ventaja original de D y G venía de sortear del banco completo, con consultas más fáciles (M2).
- **B1 contra A sí se sostiene.** B1 supera a A en todos los N y todos los sorteos: de +4.5 a +8.8 puntos en promedio. Sin la calibración, la madura nunca alcanza a la temprana (−7.5 con N máximo).

### Desviaciones del diseño

- Ninguna en el diseño.
- Una precisión: con N = 291, A y B1 tienen desviación 0 entre semillas por construcción, como se había anunciado. D y G con N máximo varían poco, porque solo cambia qué 1 o 2 consultas sobran en las clases con más de 36 en R; en el sorteo 4 las 5 semillas coinciden.

## Archivos

- `calibracion_fija.py`: el script.
- `filas.csv`: una fila por sorteo de E, condición, N y semilla (400 corridas).
- `resumen.json`: agregados, intervalos, bootstrap de E0 y control.
- `por_consulta_E0.json`: acierto por consulta en E0.
- `log.txt` y `tiempos.txt`.
