# Objetos nuevos con el codificador reentrenado por pliegue

Worktree `MAE-TMS-pliegues`, desacoplado en `df2f893`. Responde a M4 de la lectura de jurado (`revision_jurado/jurado_metodologia.md`).

## Pregunta

¿El sistema generaliza a objetos que tampoco vio el codificador? En exp16 (`results/experimento16`), el objeto reservado de cada pliegue no entra al llenado ni a la fase A, pero el codificador oficial (`src/stage2_encoder.py`, MSE + 0.1·CE) se entrenó sobre todo `train`, con los diez objetos de cada clase. El objeto «nuevo» es nuevo para las memorias, pero no para el codificador. Exp16 da 89.2 [85.1, 93.2] % de punta a punta con objeto nuevo, contra 95.5 % con objeto conocido.

## Diseño (escrito antes de correr)

En cada pliegue k de exp16 (el mismo objeto reservado por clase, el mismo `fold_split`):

1. **Codificador del pliegue.** `stage2_encoder.train()` corre sin cambios: misma arquitectura, 50 épocas, semilla 42, `CLS_WEIGHT=0.1`, Adam 1e-3, lote 32 y mismas transformaciones. La selección del punto de control también es la oficial: el menor RMSE de test cada 10 épocas. Solo cambia el corte: `splits.json` sin ninguna imagen de los objetos reservados del pliegue, ni en `train` ni en `test` (el `test` elige el punto de control). Entrena en la GPU. Se exigen los criterios oficiales de aceptación (RMSE < 0.3, acc ≥ 85 %).
2. **Latentes.** `encode_all()` de exp16 recalcula las 410 × 16 vistas por clase con el codificador del pliegue.
3. **Escala y τ con la regla oficial,** recalculadas con el codificador del pliegue sobre el llenado del pliegue (las 200 imágenes por clase de `fold_split`):
   - Escala min-max: `stage5_fill.compute_global_latent_stats()` sobre las variantes 0–3, con margen del 10 %.
   - τ: `stage7_bidirectional.latent_energy_threshold()`, es decir, 0.9 × la norma mínima de los originales (variante 0) del llenado.

   Antes de correr comprobé que estas dos funciones, aplicadas a los `instance_latents_*.json` oficiales, reproducen lo guardado: τ = 16.607264, igual a `latent_energy_threshold.json`; escala con diferencia máxima de 1.3e-6 contra `latent_global_stats.json`.
4. **Lógica de exp16 sin cambios.** `run_fold(k)` del script oficial, importado tal cual. El script de esta carpeta solo apunta las rutas de latentes, escala y τ a la carpeta del pliegue.

**Diferencias con exp16, además del codificador:**
- La escala y τ se recalculan por pliegue. Exp16 usó las oficiales, que vienen del llenado oficial con los diez objetos, pero con otro codificador el espacio latente es otro.
- El codificador oficial se entrenó en CPU (torch 2.12.0+cpu) y los de los pliegues en GPU (2.12.0+cu130). Con la misma semilla tampoco serían idénticos bit a bit.
- Cada codificador ve 9/10 de las imágenes de entrenamiento.

**Control opcional, solo si el tiempo alcanza:** reentrenar en GPU con todo `train` (sin reservar nada) y correr el pliegue 1. Así se separa el efecto de reentrenar y recalcular la escala del efecto de quitar el objeto.

## Qué apoyaría cada lectura

Comparación pareada por pliegue contra `results/experimento16/raw` (mismos pliegues, mismos bancos de 328 + 328 imágenes).

- **La fuga no infla la cifra** (la generalización viene de la memoria y de lo que el codificador aprendió de los otros nueve objetos). Se apoya si:
  - el e2e con objeto nuevo cae menos de 3 puntos contra el oficial, o el IC 95 % de la diferencia pareada incluye 0;
  - la brecha conocido − nuevo, medida con el mismo codificador del pliegue, no crece de forma clara (IC de su diferencia con la brecha oficial incluye 0);
  - los falsos ruteos sobre objeto nuevo siguen ≤ 2 %.
- **La fuga infla la cifra** (el codificador supervisado ya había separado ese objeto). Se apoya si:
  - el e2e con objeto nuevo cae 3 puntos o más con IC que excluye 0, y la caída es mayor que la del banco conocido (la brecha crece);
  - o los falsos ruteos sobre objeto nuevo pasan de 2 %.
- **Si conocido y nuevo caen lo mismo,** la caída se debe a reentrenar (menos datos, GPU, otra escala), no a la fuga. El control opcional lo ayudaría a separar.
- Se mantiene el criterio §6 de exp16: «sostenida» si la razón e2e nuevo/conocido es ≥ 0.75 y los falsos ≤ 2 %; «refutada» si la razón es < 0.5 o los falsos > 5 %.

## Tiempo y alcance

Se mide el primer entrenamiento y se proyecta el total (10 entrenamientos más la lógica de exp16, unos 45 min por pliegue con dos procesos según los `meta` de exp16). Si la proyección pasa de 5 h, se corren primero 2 pliegues completos, se reporta y se detiene.

**Lo que pasó.** Los 10 pliegues se corrieron en tres tandas con el mismo script, sin cambios entre ellas.
- **Tanda 1** (2 nov, 07:33 a 08:44, dos carriles): pliegues 1 y 2.
  - La lógica tomó unos 59 min por pliegue, contra unos 45 en exp16, con otros experimentos en la máquina. La proyección para 10 pliegues subió a unas 5.6 h, así que la corrida se detuvo tras esos dos, como fijaba la regla de las 5 h.
  - Los entrenamientos de los pliegues 3 y 4 iban a la mitad y se descartaron (se borraron sus carpetas).
- **Tanda 2** (2 nov): pliegue 3. El lanzador esperó de 08:48 a 13:27 a tener 6 GB libres. Después la cola se pausó porque otro experimento necesitaba la memoria.
- **Tanda 3** (3 nov, 04:46 a 10:42): pliegues 4 a 10, en un solo proceso. El segundo proceso nunca encontró 6 GB libres y no arrancó.
- No se corrió el control opcional.

| pliegue | entrenar codificador (GPU) | latentes | lógica de exp16 (CPU) |
|---|---|---|---|
| 1 | 5.5 min | 0.8 min | 59.6 min |
| 2 | 5.7 min | 0.6 min | 58.3 min |
| 3 | 4.8 min | 0.5 min | 41.5 min |
| 4 | 4.5 min | 0.4 min | 38.7 min |
| 5 | 4.5 min | 0.4 min | 38.9 min |
| 6 | 4.5 min | 0.4 min | 39.0 min |
| 7 | 4.5 min | 0.4 min | 95.1 min |
| 8 | 4.7 min | 0.4 min | 35.7 min |
| 9 | 4.6 min | 0.4 min | 36.4 min |
| 10 | 4.6 min | 0.4 min | 36.4 min |

## Resultados (10 pliegues)

Media de los 10 pliegues con bootstrap 95 % sobre pliegues (2000 remuestreos, semilla 0), como en exp16. Tablas completas en `tablas.md`.

### Punta a punta, objeto conocido contra nuevo (formato de exp16)

| banco | contenido acepta | responde | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | hit estricto | otro dominio |
|---|---|---|---|---|---|---|---|---|
| objeto conocido | 98.8 [98.4, 99.1] | 95.7 [94.8, 96.6] | 97.1 [96.6, 97.6] | 99.8 [99.7, 100.0] | 0.2 [0.0, 0.3] | 94.8 [93.8, 95.9] | — | — |
| objeto nuevo | 93.0 [90.8, 95.3] | 88.8 [85.5, 92.3] | 94.5 [92.2, 96.8] | 95.6 [94.3, 96.8] | 4.1 [3.0, 5.4] | 87.6 [84.3, 91.0] | 99.0 [97.5, 100.0] | 1.5 [0.0, 3.0] |

Razón e2e nuevo/conocido por pliegue: 0.92 [0.89, 0.96] (oficial: 0.93 [0.89, 0.97]).

### Contra exp16 oficial

| medida | exp16 oficial | codificador por pliegue | diferencia pareada (pliegue − oficial) |
|---|---|---|---|
| e2e objeto conocido | 95.5 [95.1, 95.9] | 94.8 [93.8, 95.9] | −0.6 [−1.6, 0.3] |
| e2e objeto nuevo | 89.2 [85.1, 93.2] | 87.6 [84.3, 91.0] | −1.6 [−5.7, 3.2] |
| brecha conocido − nuevo | 6.3 [2.5, 10.4] | 7.2 [4.1, 10.4] | 0.9 [−4.0, 5.3] |
| falsos ruteos, objeto nuevo (de 3280) | 2 | 136 (4.1 %) | |
| falsos ruteos, objeto conocido (de 3280) | 3 | 5 | |

| pliegue | e2e conocido: oficial → pliegue | e2e nuevo: oficial → pliegue | falsos nuevo (de 328): oficial / pliegue |
|---|---|---|---|
| 1 | 95.7 → 94.2 | 94.2 → 89.6 | 0 / 5 |
| 2 | 94.5 → 91.8 | 89.0 → 87.2 | 0 / 22 |
| 3 | 96.0 → 94.2 | 79.3 → 91.2 | 1 / 6 |
| 4 | 96.0 → 97.3 | 98.8 → 95.4 | 0 / 9 |
| 5 | 95.7 → 95.7 | 91.8 → 84.5 | 0 / 26 |
| 6 | 95.1 → 93.9 | 89.0 → 80.2 | 0 / 17 |
| 7 | 96.6 → 94.5 | 93.9 → 92.7 | 1 / 15 |
| 8 | 95.1 → 96.3 | 94.5 → 82.9 | 0 / 12 |
| 9 | 94.8 → 96.6 | 82.6 → 93.0 | 0 / 14 |
| 10 | 95.1 → 93.9 | 78.7 → 79.6 | 0 / 10 |

- Los codificadores cumplen los criterios oficiales: RMSE de 0.105 a 0.118 y acc de test de 98.3 a 99.7 %. El oficial tiene RMSE 0.1096 y acc 99.7 %.
- τ por pliegue: de 8.38 a 17.05, contra 16.61 del oficial.
- Fase A: de 1009 a 1018 registradas por pliegue (media 1013), como el oficial (1008 a 1017).

### Falsos ruteos

| banco: par | imágenes |
|---|---|
| nuevo: horse → cow | 35 |
| nuevo: horse → dog | 33 |
| nuevo: cow → dog | 23 |
| nuevo: cow → car | 20 |
| nuevo: dog → horse | 12 |
| nuevo: cow → horse | 7 |
| nuevo: dog → cow | 5 |
| nuevo: dog → car | 1 |
| conocido: cow → horse | 3 |
| conocido: horse → cow | 1 |
| conocido: cow → dog | 1 |

- Los 136 falsos sobre objeto nuevo salen de las tres clases de animales. 115 caen en otro animal y 21 en `car`; 20 de esos 21 son de `cow5`.
- Por pliegue, los falsos sobre objeto nuevo son 1.5, 6.7, 1.8, 2.7, 7.9, 5.2, 4.6, 3.7, 4.3 y 3.0 %. Dos pliegues quedan en 2 % o menos y tres pasan de 5 % (2, 5 y 6).
- Se reparten en 24 de los 80 objetos. Nueve tienen 5 o más y suman 105. Cuatro (`cow5` 23, `horse2` 22, `horse7` 14, `cow6` 12) suman 71, la mitad.

### Por objeto reservado (e2e sobre sus 41 vistas)

- Con 70 % o más: 71 de 80 objetos con el oficial y 68 de 80 con el codificador de cada pliegue.
- Las caídas más grandes:
  - `cow5`: de 100 a 29 %, con 23 falsos (20 a `car`).
  - `horse2`: de 80 a 27 %, con 22 falsos.
  - `cow6`: de 95 a 37 %, con 12 falsos.
  - `apple6`: de 100 a 46 %, sin falsos (el resto se rechaza).
- Las subidas más grandes: `apple3` de 0 a 100 % y `pear9` de 10 a 100 %.
- El resto, en `por_objeto.csv`.

**Qué hace la cabeza clasificadora** (`destinos_objeto_nuevo.json`). No participa en el sistema; solo sirve de diagnóstico. Sobre las 41 vistas de cada objeto:

| objeto | cabeza clasificadora | destino del ruteo |
|---|---|---|
| `horse2` | cow 23, horse 15, dog 3 | cow 17, horse 12, dog 5, rechazo 7 |
| `cow5` | cow 20, car 16, dog 5 | car 20, cow 17, dog 3, rechazo 1 |
| `cow6` | cow 29, dog 7, car 3, horse 2 | cow 17, rechazo 12, dog 11, horse 1 |

- En `horse2` y `cow5`, el codificador que no vio el objeto lo pone en la región de otra clase, y la memoria lo rutea ahí.
- En `cow6` la cabeza acierta 29 de 41, pero el ruteo manda 11 a `dog`: ahí el error no se explica solo por la cabeza.
- En toda la cabeza, el acierto sobre objeto nuevo va de 90.9 a 97.3 % por pliegue (media 94.5); sobre objeto conocido, de 98.2 a 100 % (media 99.7).

## Lectura (10 pliegues)

- **Cobertura: la fuga no infla la cifra.**
  - Sin la fuga, el e2e con objeto nuevo baja 1.6 puntos, con IC [−5.7, 3.2] que incluye 0. Se cumplen las dos condiciones fijadas antes de correr: cae menos de 3 puntos y el IC incluye 0.
  - El banco conocido baja 0.6 [−1.6, 0.3].
  - La brecha conocido − nuevo pasa de 6.3 a 7.2. La diferencia pareada, 0.9 [−4.0, 5.3], incluye 0: no crece de forma clara.
  - Pliegue por pliegue, la diferencia va en los dos sentidos: de −11.6 (pliegue 8) a +11.9 (pliegue 3).
- **Falsos: la fuga sí importa.**
  - Con el codificador limpio, los falsos sobre objeto nuevo suben de 2 a 136 de 3280 (4.1 % [3.0, 5.4]). Pasan el umbral de 2 % fijado antes de correr para «la fuga infla la cifra».
  - En el banco conocido no cambian: 5 contra 3 de 3280.
  - Con el criterio §6 de exp16 (razón 0.92 ≥ 0.75; falsos entre 2 y 5 %), la afirmación queda en la zona intermedia: ni «sostenida» ni «refutada». El extremo alto del IC (5.4 %) y tres pliegues pasan del 5 % de «refutada».
- **La propiedad de exp16 que no sobrevive es «el fallo es rechazo, no invención».** Con el codificador que vio todos los objetos hubo 2 falsos en 3280. Sin él, el sistema asigna a otra clase parte de los objetos que el codificador acerca a esa clase, en vez de rechazarlos.
  - La lectura preliminar no sabía si `horse2` era un caso aislado. No lo es: los falsos tocan 24 objetos, todos animales, y cuatro concentran la mitad.
  - Fuera de los animales (`apple`, `car`, `cup`, `pear`, `tomato`), con objeto nuevo no hay ningún falso ruteo.
- **Lo que no decide.** No separa el efecto de quitar el objeto del de reentrenar en GPU con menos datos y recalcular escala y τ; lo separaría el control opcional, que no se corrió. Pero el banco conocido, con el mismo codificador reentrenado, casi no baja y no gana falsos. Eso sugiere que el aumento de falsos viene de quitar el objeto, no del reentrenamiento.

## Desvíos del diseño

1. **Tres tandas en lugar de una corrida.** El plan era detenerse tras 2 pliegues si la proyección pasaba de 5 h; así se hizo, y después se completaron los 8 restantes en dos tandas más. El script no cambió entre tandas: los `raw/` de los pliegues 1 a 3 son idénticos byte a byte a los de la copia parcial de 3 pliegues.
2. **Escala y τ recalculadas por pliegue,** como pedía el diseño. Exp16 usó las oficiales.
3. **CPU contra GPU.** El oficial se entrenó en CPU y los de los pliegues en GPU.
4. **No se corrió el control opcional.**
5. **Entrenamientos descartados.** Los de los pliegues 3 y 4 de la tanda 1 iban a la mitad y se borraron; se rehicieron completos en las tandas 2 y 3.
6. **Un solo proceso en la tanda 3.** Por falta de memoria, los pliegues 4 a 10 corrieron uno tras otro. No cambia los resultados, solo el tiempo.

## Archivos

- `run_codificador_por_pliegue.py`: el script. `lanzar_con_memoria.ps1`: el lanzador que espera a tener memoria libre.
- `raw/pliegue_<k>.json`: filas por imagen, en el formato de exp16.
- `resumen.json`, `fig1_nuevo_vs_conocido.png`: el agregado de exp16 sobre estos pliegues.
- `comparacion_oficial.json`, `por_pliegue.csv`, `por_objeto.csv`, `tablas.md`: la comparación con el oficial.
- `destinos_objeto_nuevo.json`: por objeto reservado, la clase que da la cabeza clasificadora del codificador del pliegue junto al destino del ruteo.
- `tiempos/` y `logs/`: los tiempos y la salida de cada proceso.
- Fuera de git, en `models/codificador_por_pliegue/pliegue_<k>/`: el codificador, el corte, la escala, τ, los latentes y el diagnóstico de cada pliegue.
