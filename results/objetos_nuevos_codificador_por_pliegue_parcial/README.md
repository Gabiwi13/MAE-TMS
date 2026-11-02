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

**Lo que pasó.** La corrida se detuvo tras 2 de 10 pliegues (1 y 2) porque la proyección pasó de 5 h.
- El primer entrenamiento tomó 5.5 min en GPU. Con la lógica a 45 min por pliegue, el total proyectado era de unas 4.3 h, así que se lanzaron dos carriles: pliegues impares y pares.
- La lógica del pliegue 1 tomó 59.6 min (el llenado, 52 min, contra 38 en exp16), con otros experimentos corriendo en la máquina.
- Con eso, la proyección para 10 pliegues subió a unas 5.6 h: unos 66 min por pliegue, cinco por carril. Quedarían unas 4.4 h para los 8 pliegues restantes.
- Se detuvieron los dos carriles en cuanto terminaron los pliegues 1 y 2. Los entrenamientos de los pliegues 3 y 4 iban a la mitad y se descartaron (se borraron sus carpetas).
- No se corrió el control opcional.

| pliegue | entrenar codificador (GPU) | latentes | lógica de exp16 (CPU) | de ella, llenado |
|---|---|---|---|---|
| 1 | 5.5 min | 0.8 min | 59.6 min | 52 min |
| 2 | 5.7 min | 0.6 min | 58.3 min | 51 min |

Tiempo de reloj: de 07:33 a 08:44 (unos 71 min), con dos procesos.

## Resultados (pliegues 1 y 2)

Con dos pliegues, el bootstrap sobre pliegues no da intervalos útiles: con n = 2 solo remuestrea dos valores. Por eso se dan los valores de cada pliegue. Tablas completas en `tablas.md`.

### Punta a punta, objeto conocido contra nuevo (formato de exp16)

| banco | contenido acepta | responde | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | hit estricto | otro dominio |
|---|---|---|---|---|---|---|---|---|
| objeto conocido | 98.6 [97.9, 99.4] | 94.1 [92.7, 95.4] | 97.0 [96.6, 97.3] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 93.0 [91.8, 94.2] | — | — |
| objeto nuevo | 92.2 [90.5, 93.9] | 89.5 [88.1, 90.9] | 94.7 [93.6, 95.7] | 95.7 [93.0, 98.4] | 4.1 [1.5, 6.7] | 88.4 [87.2, 89.6] | 97.7 [95.5, 100.0] | 2.3 [0.0, 4.5] |

Razón e2e nuevo/conocido: 0.95 en cada pliegue.

### Contra exp16 oficial, pliegue por pliegue

| pliegue | e2e conocido: oficial → por pliegue | e2e nuevo: oficial → por pliegue | brecha conocido − nuevo: oficial → por pliegue | falsos ruteos, objeto nuevo (de 328): oficial / por pliegue |
|---|---|---|---|---|
| 1 | 95.7 → 94.2 | 94.2 → 89.6 | 1.5 → 4.6 | 0 / 5 |
| 2 | 94.5 → 91.8 | 89.0 → 87.2 | 5.5 → 4.6 | 0 / 22 |
| media | 95.1 → 93.0 (−2.1) | 91.6 → 88.4 (−3.2) | 3.5 → 4.6 | 0 / 27 de 656 (4.1 %) |

- En objeto conocido, el codificador de cada pliegue tuvo 0 falsos ruteos, contra 1 del oficial.
- Los codificadores cumplen los criterios oficiales: RMSE 0.1054 y 0.1107, acc de test 99.7 y 99.5 %. El oficial tiene RMSE 0.1096 y acc 99.7 %.
- τ por pliegue: 17.05 y 10.10, contra 16.61 del oficial.
- Fase A: 1013 y 1009 registradas, contra 1012 y 1015 del oficial.

### Falsos ruteos

En los dos pliegues, los 27 falsos ruteos caen sobre objeto nuevo y todos entre animales:

| par | imágenes |
|---|---|
| horse → cow | 17 |
| horse → dog | 5 |
| cow → horse | 2 |
| dog → horse | 2 |
| dog → cow | 1 |

22 de los 27 son de un solo objeto: `horse2` (pliegue 2).

### Por objeto reservado (e2e sobre sus 41 vistas)

- Con 70 % o más: 15 de 16 objetos, tanto con el oficial como con el codificador de cada pliegue.
- Objetos que cambian:
  - `horse2` baja de 80 % a **27 %**, con 22 falsos ruteos (oficial: 0).
  - `cow2` sube de 68 a 88 %.
- El resto, en `por_objeto.csv`.

**Qué pasó con `horse2`** (`destinos_objeto_nuevo.json`). La cabeza clasificadora del codificador del pliegue 2 no participa en el sistema; solo sirve de diagnóstico. Sobre las 41 vistas de `horse2`:
- La cabeza dice `cow` 23, `horse` 15 y `dog` 3.
- El ruteo manda 17 a `cow`, 12 a `horse` y 5 a `dog`, y rechaza 7.

El codificador que no vio a `horse2` lo pone en la región de `cow`, y la memoria lo rutea a donde el codificador lo puso. Con el codificador oficial, que sí vio a `horse2`, el mismo objeto tenía 80 % de punta a punta y ningún falso ruteo.

En toda la cabeza clasificadora, el acierto sobre objeto nuevo es de 97.3 % (pliegue 1) y 92.1 % (pliegue 2); sobre objeto conocido, de 100 y 99.7 %.

## Lectura (preliminar: 2 de 10 pliegues)

- **Cobertura: la fuga explica poco.**
  - Sin la fuga, el e2e con objeto nuevo baja 3.2 puntos en promedio (−4.6 y −1.8).
  - El banco conocido baja 2.1 puntos (−1.5 y −2.7).
  - La brecha conocido − nuevo crece en el pliegue 1 (1.5 → 4.6) y se achica en el 2 (5.5 → 4.6).
  - Así que, en cobertura, no hay señal clara de que el codificador supervisado inflara la cifra de objeto nuevo más que la de objeto conocido. La razón nuevo/conocido es 0.95.
- **Falsos: la fuga sí importa.**
  - Con codificador limpio, los falsos ruteos sobre objeto nuevo suben de 0 a 27 de 656 (4.1 %). Pasan el umbral de 2 % que se fijó antes de correr para «la fuga infla la cifra».
  - En el pliegue 2 llegan a 6.7 %, por encima del 5 % que exp16 §6 fija para «refutada».
  - Con el criterio §6 sobre los dos pliegues juntos (razón ≥ 0.75, falsos entre 2 y 5 %), la afirmación queda en la zona intermedia, no «sostenida».
- **La propiedad de exp16 que no sobrevive es «el fallo es rechazo, no invención».** Con el codificador que vio todos los objetos hubo 2 falsos en 3280. Sin él, un objeto (`horse2`) cae en la región de otra clase y el sistema lo asigna ahí en vez de rechazarlo. El caso se explica entero por el codificador: su propia cabeza clasificadora confunde a `horse2` con `cow` casi en la misma proporción.
- **Lo que no decide:**
  - Con dos pliegues no se sabe cuántos de los 80 objetos se comportan como `horse2`. En exp16 oficial, los dos falsos sobre objeto nuevo fueron `cow3` y `horse7`, uno cada uno.
  - No separa el efecto de quitar el objeto del de reentrenar en GPU con menos datos y recalcular escala y τ. Lo separaría el control opcional, que no se corrió.
  - La caída en el banco conocido (−2.1) sugiere que reentrenar por sí solo cuesta un par de puntos.

## Archivos

- `run_codificador_por_pliegue.py`: el script.
- `raw/pliegue_<k>.json`: filas por imagen, en el formato de exp16.
- `resumen.json`, `fig1_nuevo_vs_conocido.png`: el agregado de exp16 sobre estos pliegues.
- `comparacion_oficial.json`, `por_pliegue.csv`, `por_objeto.csv`, `tablas.md`: la comparación con el oficial.
- `destinos_objeto_nuevo.json`: por objeto reservado, la clase que da la cabeza clasificadora del codificador del pliegue junto al destino del ruteo.
- `tiempos/` y `logs/`: los tiempos y la salida de cada proceso.
- Fuera de git, en `models/codificador_por_pliegue/pliegue_<k>/`: el codificador, el corte, la escala, τ, los latentes y el diagnóstico de cada pliegue.
