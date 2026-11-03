# Experimento 11 con los directorios del protocolo corregidos

Escrito antes de correr (2 nov 2026). Worktree `MAE-TMS-exp11fix`, desacoplado en `df2f893`.

## Pregunta

En `run_experiment11_monolithic.py`, cada proceso del Pool carga los especialistas una vez (`init_worker`) y cada trabajo forma los directorios perspectivales (`mem_dir` de texto y `mem_dir_R` de imagen) encima de esos mismos objetos. El `TME()` sí era nuevo en cada trabajo, pero los directorios de los especialistas acumulaban las formaciones de los trabajos anteriores del mismo proceso. Un trabajo de la semilla 43 podía rutear con los directorios de la 42 y la 43 sumados, y el tamaño del círculo de una misma entrada cambia de un trozo a otro dentro de una semilla (7 u 8).

¿Cuánto cambian las cifras de `T-protocolo` en exp11 (texto, imagen y fuera de dominio) cuando cada trabajo forma sus directorios desde cero? ¿Sigue en pie la lectura de M1 del jurado (clase correcta sobre el total, empate con la EHAM única)?

## Lectura del código antes de cambiar nada

- `M` (EHAM única) usa `gate_accepts([mono])`, `recall_lived(mono)`, `recognize_gated_right(mono)` y `evoke_labels(mono)`. No toca ningún directorio.
- `T-oraculo` usa `recognize_gated` y `recognize_gated_right` de los especialistas (memoria de contenido) y el recuerdo del especialista de la verdad de terreno. No toca ningún directorio.
- `T-protocolo` rutea con `route_transactive`, que lee `mem_dir` o `mem_dir_R` de los especialistas y sus `agent_counts` (el círculo y la calibración ÷ conteo). Es el único brazo afectado.
- El error estaba en los tres tipos de trabajo: `run_job` (texto, y fuera de dominio con las 12 consultas del trozo 0), `run_image_job` (imagen) y `run_ood_job` (fuera de dominio con las 40 consultas). En `run_ood_job` hay un trabajo por semilla, así que la acumulación iba de una semilla a otra.
- La corrida oficial (`MAE-TMS-una-hetero/logs_comparacion/grupo2/`) usó 10 procesos en texto, 6 en imagen y 10 en fuera de dominio, con un Pool nuevo por corte. Si el Pool repartió un trabajo por proceso al inicio, salieron limpios: en texto la semilla 42 y los trozos 0–3 de la 43; en imagen la semilla 42; en fuera de dominio las diez semillas (10 trabajos en 10 procesos). Esos trabajos sirven de control: el ruteo nuevo debe coincidir con el viejo en ellos.

## Corrección

- `reset_directories(specialists)` al inicio de `run_job`, `run_image_job` y `run_ood_job`: `mem_dir` y `mem_dir_R` nuevos en cada trabajo, igual que `run_experiment13_augmentation.py:259-262`.
- `--arms` (por defecto los tres brazos) para correr solo `T-protocolo`.
- `EXP11_RAW`: carpeta de los raw, para que el informe automático del script no pise este README.
- Nada más cambia en la lógica.

## Diseño

- Solo `T-protocolo`, con el diseño original: semillas 42–51, cortes N = 25, 50, 100 y 200, 3 sorteos por consulta, 6 trozos por semilla y corte. Imagen: `--image-only`, 10 imágenes de prueba por clase, 6 trozos. Fuera de dominio: `--ood-only` con `results/experimento11/consultas_fuera_dominio.txt` (40 consultas).
- Memorias: los cachés oficiales `N*_V16.pkl`, enlazados con una unión a `MAE-TMS-una-hetero/cache/exp11/` y solo para lectura. Control: `control_igual_al_oficial` del caché N = 200.
- Las filas `M` y `T-oraculo` salen de los raw oficiales (`results/experimento11/raw/`); las de `T-protocolo`, de los raw nuevos (`raw/`).
- Diferencia esperada que no es efecto: al correr solo un brazo, el recuerdo del protocolo usa otra parte del generador aleatorio que en la corrida de tres brazos. El ruteo (entrada, destino, círculo) es determinista dada la semilla y no depende de eso. El recuerdo y la evocación cambian como al cambiar de semilla.

### Medidas

- Las tablas del README de exp11, con lo viejo y lo nuevo lado a lado.
- Clase correcta (1-NN, centroide y clasificador) sobre las 171 consultas, con la no respuesta contada como fallo.
- McNemar exacto pareado entre `T-protocolo` y `M`: sobre los pares (semilla, consulta, sorteo) y por semilla. Además, un bootstrap pareado por consulta de la diferencia.
- Diagnóstico del arreglo: tamaño del círculo por entrada en cada trozo (debe ser constante dentro de una semilla) y coincidencia del destino nuevo con el viejo por semilla (la semilla 42 debe coincidir si salió limpia).

### Qué apoyaría cada lectura

- **El error no movió las conclusiones:** ruteo, cobertura y clase de `T-protocolo` cambian menos que el ancho de sus intervalos (alrededor de un punto), y el signo de la diferencia con `M` se mantiene en los cuatro cortes.
- **El error favorecía al protocolo:** el protocolo corregido baja más de un intervalo en ruteo o clase, o la diferencia con `M` cambia de signo.
- **El error perjudicaba al protocolo:** el protocolo corregido sube más de un intervalo.
- **Lectura de M1 (clase sobre el total):** se sostiene el empate si McNemar no rechaza (p > 0.05) en N = 200 y la diferencia sobre el total es menor de 2 puntos. Si el protocolo queda por encima con p < 0.05, vuelve a tener apoyo «clasifica algo mejor»; si queda por debajo, el criterio §8.1 de la propuesta se cumple con más fuerza.
- **Fuera de dominio y compuerta:** se mantiene 4/40 aceptadas y 2/40 con compuerta, o cambia. Cualquier cambio se reporta por consulta.

## Resultados

La proyección de la prueba corta dio unas 12.5 h con 2 procesos, por encima del límite de 8 h del primer encargo, así que el trabajo se detuvo después de la prueba. Lo que sigue es la prueba, la proyección y el reanálisis de los raw oficiales. Después, a pedido del coordinador, se corrió el **solo ruteo** completo: 10 semillas, 4 cortes, texto, imagen y fuera de dominio, en 19 min (sección «Solo ruteo»). Por último se lanzó la **corrida completa** con recuerdo y jueces, del 2 nov 14:15 al 3 nov 04:46 (sección «Corrida completa», al final).

### Control del caché

`control_igual_al_oficial` del caché `N200_V16.pkl` (unión de solo lectura a `MAE-TMS-una-hetero/cache/exp11/`): apple 0, car 600, cow 600, cup 0, dog 1200, horse 600, pear 0 y tomato 0 celdas distintas. No es «todo cero»: 4 de 8 clases son idénticas a los `agent_*.pkl`, igual que en la corrida oficial (mismo diccionario en `results/experimento11/raw/s*_N200_c*.json` y en su README). El caché es el mismo que usó la corrida oficial.

### Prueba corta (semilla 43; texto e imagen con N = 25 y 6 trozos; solo `T-protocolo`)

Raw en `prueba/raw/`; comparación en `prueba/agregado/comparacion.md`.

- **El arreglo funciona.** Círculo por entrada (consultas resueltas sin saltos), por trozo: antes `car` y `cow` valían 7 en los trozos 0–3 y 5, y 8 en el 4. Ahora valen 7 en los seis trozos y ninguna entrada cambia entre trozos.
- **El ruteo nuevo coincide con el viejo donde el viejo salió limpio.** En texto, el destino y el círculo son idénticos en los trozos 0, 1, 2, 3 y 5 (143 de 143 consultas). En el trozo 4, que en la corrida oficial heredó directorios de otro trabajo, cambian 9 de 28. En imagen coinciden los 80 destinos y en el fuera de dominio las 12 consultas del trozo 0.
- **Efecto en s43, N = 25** (una semilla, sin intervalo útil):

| medida (T-protocolo) | viejo | corregido |
|---|---|---|
| ruteo ok | 95.9 | 97.1 |
| responde | 98.8 | 99.4 |
| clase 1-NN sobre respondidas | 97.0 | 97.6 |
| clase 1-NN sobre el total | 95.9 | 97.1 (M: 98.2) |
| McNemar P contra M, pares (consulta, sorteo) | b = 21, c = 9, p = 0.043 | b = 15, c = 9, p = 0.31 |
| imagen: acepta / hit laxo / hit estricto | 63.7 / 41.2 / 40.0 | 63.7 / 41.2 / 41.2 |

  La diferencia en hit estricto es una imagen de 80 y viene del muestreo de la evocación, no del ruteo (los 80 destinos son iguales).
- **Sonda de tiempo con N = 200** (s43, trozos 0 y 1, 2 procesos): ruteo idéntico al viejo en las 58 consultas (esos trozos salieron limpios en la corrida oficial). La sonda se detuvo a mano tras 2 de 6 trabajos porque la memoria libre bajó a 0.86 GB.

### Tiempos medidos y proyección

| parte | trabajos | s por trabajo | horas-proceso |
|---|---|---|---|
| texto N = 25 | 60 | 149 (medido, 6 trabajos, 1 proceso; formación 21 s de eso) | 2.5 |
| texto N = 50 | 60 | ~185 (estimado: 149 × 796/640, razón de medianas oficiales) | 3.1 |
| texto N = 100 | 60 | ~258 (149 × 1109/640) | 4.3 |
| texto N = 200 | 60 | 409 (medido, 2 trabajos: 330 y 489 s con 2 procesos) | 6.8 |
| imagen N = 25 | 60 | 55 (medido, 6 trabajos; formación 0.9 s) | 0.9 |
| imagen N = 50, 100, 200 | 180 | ~98, ~139, ~170 (55 × razones oficiales 586/329, 830/329, 1017/329) | 6.8 |
| fuera de dominio | 40 | ~30 (oficial 30–32 s con tres brazos) | 0.3 |
| **total** | 520 | | **~24.7** |

Con 2 procesos: texto ~8.3 h, imagen ~3.9 h, fuera de dominio ~10 min y ~20 min de preparar cada corte: **~12.5 h**. Con `--chunks 1` la formación se haría una vez por semilla y corte, y se ahorran ~0.6 h; sigue por encima de 8 h. Con 1 proceso, ~25 h.

En la corrida oficial el protocolo pesaba poco: con los tres brazos, un trabajo de texto N = 25 tardaba 640 s y el protocolo solo, 149 s. Lo caro es el recuerdo y los jueces de cada fila, no la formación.

### Memoria

- 1 proceso: hasta 2.8 GB de working set; la memoria libre bajó a 1.6 GB.
- 2 procesos (Pool con memoria compartida): la memoria libre pasó de 5.47 GB al lanzar a 0.86 GB. El umbral de 5 GB deja menos de 1 GB de margen con dos procesos; haría falta esperar a unos 6 GB.
- La prueba esperó casi 2 h a que hubiera memoria: entre las 8:27 y las 10:22 la memoria libre estuvo entre 2.2 y 4.7 GiB (`logs/memoria.log`). Arrancó con 1 proceso y umbral de 3.6 GiB; la sonda de N = 200 con 2 procesos arrancó con 5.2 GiB.

### Reanálisis de los raw oficiales (sin correr nada)

`agregar.py` reproduce el README oficial de exp11 carácter por carácter (`prueba/agregado/tablas_viejas/README.md`) y reproduce las cifras de M1 del jurado. Clase 1-NN sobre el total, con la no respuesta como fallo (N = 25 / 50 / 100 / 200):

- M: 97.6, 97.5, 97.6 y 96.9.
- Protocolo viejo: 95.3, 97.4, 97.4 y 97.0.
- Oráculo: 100 en los cuatro cortes.

En los raw oficiales, la clase del protocolo sobre el total es igual a su ruteo ok en los cuatro cortes (95.3, 97.4, 97.4 y 97.0).

McNemar del protocolo viejo contra M, con 5130 pares (semilla, consulta, sorteo) por corte. P − M sobre el total, con el bootstrap pareado por consulta entre corchetes:

| N | P − M [bootstrap] | p de McNemar | semillas con p < 0.05 |
|---|---|---|---|
| 25 | −2.3 [−5.9, +1.1] | 8·10⁻¹⁰ | 5 de 10, todas a favor de M |
| 50 | −0.1 [−3.0, +2.8] | 0.85 | ninguna |
| 100 | −0.2 [−3.1, +2.7] | 0.66 | ninguna |
| 200 | +0.1 [−2.9, +3.1] | 0.82 | ninguna |

El p de McNemar trata como independientes los 30 sorteos de cada consulta y es optimista. El bootstrap por consulta incluye el cero en los cuatro cortes. Para reproducir: `EXP11FIX_NEW=results/experimento11/raw EXP11FIX_OUT=<carpeta> python results/experimento11_protocolo_corregido/agregar.py` (las columnas «corregido» salen iguales a las viejas).

### Alcance del error en la corrida oficial

Según los logs de la corrida oficial (10 procesos en texto, 6 en imagen y 10 en fuera de dominio) y la prueba:

- **Texto:** sin acumulación quedaron solo los primeros 10 trabajos de cada corte (la semilla 42 y los trozos 0–3 de la 43). Los otros 50 de 60 heredaron directorios de trabajos anteriores.
- **Imagen:** sin acumulación quedó la semilla 42. En s43 con N = 25 los destinos no cambiaron.
- **Fuera de dominio:** los 40 trabajos `_o` fueron uno por proceso. Probablemente salieron limpios, y la prueba coincide en las 12 consultas comparables.

En s43 con N = 25 el error tocó 9 de 171 consultas y bajaba el ruteo 1.2 puntos. El efecto agregado sobre el ruteo, la cobertura y la clase está en la sección «Solo ruteo».

## Solo ruteo del protocolo corregido (diseño escrito al lanzar, antes de ver resultados)

El coordinador pidió esta opción después de la prueba. Script: `ruteo_solo.py`, con 1 proceso y sin recuerdo ni jueces. Salidas en `ruteo/`.

- **Alcance:** 10 semillas y 4 cortes. Texto: las 171 reservadas. Imagen: 80 por semilla. Fuera de dominio: las 40 consultas, con y sin la segunda compuerta.
- **Igual que en exp11:**
  - las funciones de formación (`form_text_directories`, `form_image_directories`) y de ruteo (`route_transactive`, `ood_rows_for`), con las mismas semillas y la misma entrada por consulta;
  - directorios nuevos en cada (semilla, corte).
- **Cobertura (responde).** Sale de la compuerta del recuerdo: la proyección del destino sin filas vacías, con los mismos pesos que `recall_from_left` y `recall_from_right`. Es determinista. El muestreo que sigue nunca devuelve vacío, así que no decide si hay respuesta. Se comprueba contra la respuesta oficial en las filas cuyo destino coincide.
- **Clase correcta sobre el total.**
  - Texto: responde y ruteo correcto. Se comprueba fila a fila en los raw oficiales limpios que equivale a «responde y clase 1-NN correcta».
  - Imagen: responde en el especialista correcto. Se comprueba fila a fila que equivale al hit laxo oficial.
- **Reproducción primero.** En cada corte se corren antes las semillas 42 y 43, y el script se detiene si no reproduce exactamente:
  - en texto, los trabajos oficiales limpios (s42 completa y trozos 0–3 de s43): entrada, destino, círculo, saltos y aceptación;
  - en imagen, la semilla 42: destino y aceptación;
  - en fuera de dominio, las semillas 42 y 43: aceptación, compuerta y destino.
- **Comparaciones.**
  - Contra la EHAM única de los raw oficiales: McNemar exacto pareado y bootstrap remuestreando consultas o imágenes.
  - Contra el protocolo viejo: lado a lado.
- **Qué no cubre:** d_nn, compat, niveles vivos, F, la clase 1-NN sobre respondidas, ni hit estricto, dominio y otro dominio en imagen. Todo eso depende del recuerdo muestreado y de los jueces.
- **Qué apoyaría cada lectura:** las mismas de la sección de diseño. Además, si una identidad de verificación falla, la cifra derivada de ella no se reporta como equivalente.

### Resultados del solo ruteo

Tablas completas en `ruteo/ruteo.md`, filas en `ruteo/filas_N*.json` y resumen en `ruteo/resumen.json`. El cómputo tardó 19 min con 1 proceso: unos 28 s por semilla y corte, para texto, fuera de dominio e imagen juntos.

**Reproducción y verificaciones.** Todas pasan:

| comprobación | iguales / total |
|---|---|
| texto, trabajos oficiales limpios (entrada, destino, círculo, saltos, acepta) | 1144 / 1144 |
| imagen, trabajos oficiales limpios (destino, acepta) | 320 / 320 |
| fuera de dominio, los 40 trabajos `_o` (acepta, compuerta, destino) | 1600 / 1600 |
| texto, trabajos que heredaron directorios | 4047 / 5696 (cambian 1649 de 5696 = 29 %) |
| imagen, trabajos que heredaron directorios | 2880 / 2880 |
| clase oficial sobre el total = responde y ruteo ok (todas las filas oficiales) | 20520 / 20520 |
| clase oficial = ruteo ok (filas oficiales limpias) | 3432 / 3432 |
| hit laxo oficial = responde y ruteo ok (imagen, todas las filas) | 3200 / 3200 |
| compuerta del recuerdo = responde oficial (texto / imagen, mismo destino) | 19869 / 19869 y 3200 / 3200 |

**Texto: clase correcta sobre el total (= ruteo ok). Media entre semillas e IC 95 %.**

| N | protocolo viejo | protocolo corregido | EHAM única | P corregido − M [bootstrap por consulta] | p de McNemar |
|---|---|---|---|---|---|
| 25 | 95.3 [94.6, 96.1] | **93.2 [91.9, 94.6]** | 97.6 [97.4, 97.8] | −4.4 [−8.1, −0.9] | 6·10⁻²⁷ |
| 50 | 97.4 [97.1, 97.8] | 96.8 [96.3, 97.4] | 97.5 [97.3, 97.7] | −0.7 [−3.3, +2.0] | 0.039 |
| 100 | 97.4 [97.0, 97.8] | 96.8 [96.3, 97.4] | 97.6 [97.4, 97.8] | −0.7 [−3.4, +2.0] | 0.020 |
| 200 | 97.0 [96.6, 97.4] | 96.8 [96.3, 97.4] | 96.9 [96.7, 97.1] | −0.1 [−2.9, +2.9] | 0.86 |

- Cobertura (responde) del corregido: 98.4, 98.7, 98.7 y 98.7 %, igual que la vieja. La EHAM única responde el 100 %.
- El ruteo de N = 50 y N = 100 es idéntico consulta por consulta. Con N = 200 solo cambian 2 destinos de 1710, y la tasa por semilla es la misma. La formación decide los mismos ganadores en esos cortes.
- El ruteo por semilla varía de verdad: con N = 25 va de 90.6 a 97.1 %.
- El p de McNemar trata como independientes los 3 sorteos de M de cada (semilla, consulta), así que es optimista. El bootstrap por consulta solo excluye el cero con N = 25.

**Imagen.** El corregido es idéntico al viejo en los 3200 destinos (los directorios acumulados no cambiaron ningún destino visual).

| N | acepta | responde | clase (respuesta del especialista correcto = hit laxo) |
|---|---|---|---|
| 25 | 63.7 | 41.2 | 41.2 |
| 50 | 77.5 | 67.5 | 67.5 |
| 100 | 80.0 | 78.7 | 78.7 |
| 200 | 81.2 | 81.2 | 81.2 |

El ruteo ok es 100 % en los cuatro cortes. La EHAM única tiene un hit laxo de 78.0, 93.9, 96.7 y 97.5. P − M va de −36.8 [−47.8, −26.1] con N = 25 a −16.3 [−24.8, −8.5] con N = 200.

**Fuera de dominio, 40 consultas.** Idéntico al viejo en las 1600 filas: el protocolo acepta 10 % sin la segunda compuerta y 5 % con ella en los cuatro cortes. Las consultas aceptadas son:
- «kitchen appliance» → apple y «wooden table» → cup, que pasan también la compuerta;
- «piano» → dog y «thunderstorm» → car, que la compuerta atrapa.

La EHAM única acepta 5.0, 5.0, 12.5 y 20.0 %. Con la compuerta, P − M = −15.0 [−27.5, −5.0] con N = 200 (p = 2·10⁻¹⁸) y −7.5 [−17.5, 0.0] con N = 100.

**Lectura.**
- El error favorecía al protocolo en texto con N = 25. El ruteo corregido baja 2.1 puntos, de 95.3 a 93.2, sin solape de intervalos. Ahí la EHAM única clasifica mejor sobre el total: −4.4 puntos, con un bootstrap por consulta que excluye el cero.
- Con N = 50 y 100 el protocolo corregido baja 0.6 puntos, menos que un intervalo. Con N = 200 baja 0.2.
- Con N = 200 se sostiene el empate de M1: −0.1 puntos, p = 0.86.
- «Clasifica algo mejor» no tiene apoyo en ningún corte.
- Imagen y fuera de dominio no cambian. Las ventajas defendibles del protocolo siguen siendo las de rechazo fuera de dominio con N ≥ 100.
- La fidelidad (d_nn) y F dependen del recuerdo muestreado y no salen del solo ruteo; están en la sección «Corrida completa».

### Desvíos del diseño

- La corrida completa no se lanzó con el primer encargo (la proyección pasaba de 8 h); se lanzó después, sin el fuera de dominio (ver «Corrida completa»).
- La prueba con N = 25 usó 1 proceso, no 2, y esperó a 3.6 GiB libres en vez de 5. Tras casi 2 h de espera, la memoria libre no llegaba a 5 GiB. El umbral de 5 GB era para la corrida completa.
- Se agregó una sonda de tiempo con N = 200 y 2 procesos, que no estaba en el encargo. Se detuvo tras 2 de 6 trabajos, cuando la memoria libre bajó a 0.86 GB.
- Al script se le agregaron dos cosas que no tocan la lógica: `segundos_formacion` en el meta, para separar la formación del resto en la proyección, y la variable de entorno `EXP11_RAW`.
- La comparación pareada con lo viejo usa las mismas (semilla, consulta, sorteo) en los dos lados. Lo viejo se resume también sobre los mismos pares (semilla, corte), en `tablas_viejas_mismos_pares/`.
- En el solo ruteo, la cobertura sale de la compuerta del recuerdo y la clase de ruteo y respuesta, no del recuerdo y los jueces. Las equivalencias se comprobaron fila a fila en los raw oficiales (ver la tabla de verificaciones). El fuera de dominio reutiliza los directorios de texto de la misma semilla, que son los mismos que forma `run_ood_job`; coincide en 1600 de 1600 filas.

### Archivos

- `README.md`: este archivo.
- `agregar.py`: junta M y T-oráculo de lo oficial con T-protocolo nuevo, reproduce las tablas y calcula la clase sobre el total, McNemar y los diagnósticos.
- `ruteo_solo.py` y `ruteo/`: el solo ruteo, con `filas_N*.json` (filas por semilla de texto, imagen y fuera de dominio), `resumen.json` y `ruteo.md`. Logs en `logs/ruteo_*.log`.
- `correr_protocolo.sh`: lanzador por fases que espera memoria antes de cada corte.
- `prueba/raw/`: raw de la prueba (`s43_N25_c0–5`, `s43_N25_i0–5`, `s43_N200_c0–1`).
- `prueba/agregado/`: `comparacion.md` y `comparacion.json`, más `tablas_viejas/` (todo lo oficial), `tablas_viejas_mismos_pares/` y `tablas_nuevas/` (s43 con N = 25).
- `prueba/informe_script/`: informe automático del script (solo protocolo; las columnas M y oráculo salen vacías).
- `comparacion.md` y `comparacion.json`: corrida completa, viejo contra corregido por corte, clase sobre el total, McNemar, d_nn pareado contra M, diagnóstico del arreglo y tiempo por trabajo.
- `tablas_nuevas/`, `tablas_viejas/` y `tablas_viejas_mismos_pares/`: las tablas del README de exp11 con el protocolo corregido, con todo lo oficial y con lo oficial sobre los mismos pares.
- `informe_script/`: informe automático del script de la corrida completa (solo protocolo).
- `raw/` no se copió a este repositorio (23 MB, 480 archivos): está en el worktree `MAE-TMS-exp11fix`, en esta misma ruta.
- `logs/`: salidas de cada fase, `tiempos.log`, `memoria.log` y `muestras_memoria.log` (memoria libre y de los procesos cada 30 s).
- Cambio al script: `git diff run_experiment11_monolithic.py` en el worktree (reinicio de directorios, `--arms`, `EXP11_RAW` y `segundos_formacion` en el meta).

## Corrida completa (con recuerdo y jueces)

Solo `T-protocolo`, con el diseño de la sección «Diseño»: semillas 42–51, cortes 25, 50, 100 y 200, texto con 6 trozos y 3 sorteos, imagen con 10 imágenes por clase y 6 trozos. Lanzador `correr_protocolo.sh` con 2 procesos y espera de memoria antes de cada corte. El fuera de dominio no se volvió a correr: el solo ruteo ya lo reproduce en 1600 de 1600 filas, y su fila sale «—» en `tablas_nuevas/`. Los 6 trabajos de texto y los 6 de imagen de s43 con N = 25, y los trozos 0 y 1 de s43 con N = 200, son los de la prueba (archivos idénticos byte a byte en `raw/` y `prueba/raw/`); por eso el log dice 54 y 58 trabajos en esos cortes.

### Tiempos (`logs/tiempos.log`)

| fase | inicio | fin | min |
|---|---|---|---|
| texto N = 25 | 2 nov 14:15 | 2 nov 16:35 | 140 |
| texto N = 50 | 2 nov 16:35 | 2 nov 17:53 | 77 |
| texto N = 100 | 2 nov 17:53 | 2 nov 19:45 | 111 |
| texto N = 200 | 2 nov 21:27 | 2 nov 23:57 | 150 |
| imagen N = 25 | 3 nov 00:00 | 3 nov 00:22 | 22 |
| imagen N = 50 | 3 nov 00:22 | 3 nov 01:20 | 58 |
| imagen N = 100 | 3 nov 01:20 | 3 nov 02:53 | 92 |
| imagen N = 200 | 3 nov 02:53 | 3 nov 04:45 | 112 |

Texto 478 min (8.0 h) e imagen 284 min (4.7 h): 12.7 h de cómputo con 2 procesos, contra 12.5 h proyectadas. De reloj fueron 14.5 h, con 1 h 42 min de espera de memoria entre texto N = 100 y N = 200. En horas-proceso (suma por trabajo, `comparacion.md`): texto 16.2 y imagen 9.5, contra 16.7 y 7.7 proyectadas.

### Resultados

`T-protocolo`, media de las diez semillas; «viejo» es la corrida oficial. Intervalos en `comparacion.md`.

| medida | N = 25 | N = 50 | N = 100 | N = 200 |
|---|---|---|---|---|
| clase 1-NN sobre el total, viejo → corregido | 95.3 → 93.2 | 97.4 → 96.8 | 97.4 → 96.8 | 97.0 → 96.8 |
| clase 1-NN sobre respondidas | 96.9 → 94.7 | 98.8 → 98.1 | 98.8 → 98.1 | 98.3 → 98.2 |
| d_nn | 18.97 → 19.54 | 20.67 → 20.81 | 23.78 → 23.75 | 26.98 → 27.18 |
| d_nn, protocolo corregido − M, pareado por consulta | −3.37 [−4.33, −2.43] | −5.79 [−6.59, −5.01] | −5.68 [−6.47, −4.92] | −5.39 [−6.30, −4.49] |
| F (M: 1.81, 1.48, 1.32, 1.28) | 2.02 → 2.37 | 1.42 → 1.64 | 1.28 → 1.42 | 1.25 → 1.30 |
| fracción con pista compartida | 4.5 → 5.8 | 4.1 → 4.1 | 4.1 → 4.1 | 4.1 → 4.1 |
| clase 1-NN con pista compartida (M: 48.3, 47.8, 52.2, 51.1) | 80.3 → 53.7 | 82.9 → 70.0 | 84.3 → 70.0 | 78.6 → 71.4 |
| imagen: hit estricto | 41.1 → 41.2 | 67.4 → 66.6 | 77.5 → 77.1 | 79.8 → 79.2 |
| imagen: otro dominio (M: 5.5, 7.5, 10.5, 10.9) | 0.2 → 0.1 | 1.8 → 1.5 | 2.2 → 3.1 | 3.0 → 3.1 |

- **Coincide con el solo ruteo.** La clase sobre el total (93.2, 96.8, 96.8 y 96.8), la cobertura y el McNemar contra M salen iguales a los del solo ruteo; en imagen, acepta, responde y hit laxo no cambian.
- **Clase sobre respondidas:** baja 2.1 puntos con N = 25 y 0.6, 0.6 y 0.1 en los otros cortes. Queda por encima de M desde N = 50 y por debajo con N = 25.
- **Fidelidad:** d_nn sube 0.57 con N = 25 y 0.21 con N = 200, fuera de los intervalos viejos; con 50 y 100 cambia menos de 0.15. El protocolo sigue recordando más cerca que M en los cuatro cortes, con intervalos que excluyen el cero.
- **F** sube en los cuatro cortes y ahora queda por encima de M en todos; antes quedaba por debajo con N = 100 y 200.
- **Pista compartida:** es la medida que más cambia. La clase cae 27 puntos con N = 25 y de 7 a 14 en los otros cortes; con 25, 50 y 100 la media nueva queda fuera del intervalo viejo, con 200 dentro. Sigue por encima de M en los cuatro cortes, pero con N = 25 los intervalos se solapan ([47.1, 62.7] contra [42.8, 54.4]).
- **Imagen:** dominio ajeno de 0.1 a 3.1 %, siempre por debajo de M (5.5 a 10.9 %). Los cambios vienen del muestreo de la evocación: los 3200 destinos son los mismos.
