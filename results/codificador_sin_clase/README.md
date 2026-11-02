# Codificador sin pérdida de clase, de punta a punta

Copia `MAE-TMS-sinclase` (worktree desacoplado en `df2f893`, rama `una-hetero`). Referencia: la copia oficial `MAE-TMS-una-hetero`, solo lectura.

## Pregunta

¿Cuánto depende el sistema visual de la pérdida de clase del codificador? El codificador oficial se entrena con MSE + 0.1·CE (`src/stage2_encoder.py`, `CLS_WEIGHT=0.1`). En exp19, cambiar todo el codificador por ImageNet + PCA bajó el ruteo de test de 96.2 a 80.5 %, pero ahí cambian a la vez la supervisión y la representación. Aquí solo se quita la supervisión de clase.

## Diseño (escrito antes de correr)

**Factor que cambia.** El codificador de `MAE-TMS-exp18/models/encoder_sin_clase/`: misma clase `Encoder`, mismo `stage2_encoder.py` (idéntico byte a byte al de `df2f893`), 50 épocas, semilla 42, `CLS_WEIGHT=0`. Con 0 la cabeza se entrena sobre `z.detach()`: es una sonda y no mueve el codificador. RMSE 0.082 (oficial 0.110); sonda lineal 94.2 % (cabeza oficial 99.7 %). `encoder.meta.json` declara `"cls_weight": 0.0`.

**Todo lo demás, con la regla oficial y sin tocarlo a mano.**
- `models/` lleva el codificador, decodificador, cabeza y manifiesto sin clase. Se conservan los insumos que no dependen del codificador: `label_quant_scale.json` (etapa 4) y `token_vectors.json`. Se borran `latent_global_stats.json`, `latent_energy_threshold.json` e `instance_latents_*.json`. No se copian `mem_dom_*`, `agent_*` ni `tme.pkl`: los regeneran las etapas 5, 6 y 7.
- Escala min-max del latente: la recalcula la etapa 5 sobre las variantes 0–3 del pool de llenado (`compute_global_latent_stats`).
- Umbral τ: la regla está en el código, `latent_energy_threshold()` de `src/stage7_bidirectional.py`: mínimo de la norma de los 1600 originales del llenado (200 por clase, variante 0) por (1 − 0.1). Con el codificador oficial da 18.45 × 0.9 = 16.61, el valor guardado. Se calcula una vez, justo después de la etapa 5.
- Latentes de instancia: los escribe la etapa 5.
- Etapas 5, 6, 7 y 8 con `run()` de cada módulo; exp16 con `run_experiment16_leave_object_out.py`, 10 pliegues, sin cambios.
- `data/eth80/splits.json` se regenera con `rekey_latents_cache.py` desde `splits_relative.json`; mismo orden que el oficial (comprobado).

**Medidas, contra el oficial.**
1. Fase A de la etapa 7: acierto al formar directorios, rechazo, sin energía.
2. Ruteo de test sobre 656, con los falsos (filas por imagen).
3. Rechazo de test.
4. Evocación top-3 de dominio sobre las imágenes ruteadas entre las 15 primeras por clase (116 en el oficial).
5. Fidelidad temprana ↔ madura de la etapa 8 (16/16 en el oficial) y ganadores de la etapa 6.
6. exp16: objeto conocido y nuevo, cobertura de punta a punta, directorio acepta, falsos.

**Añadido para medir, sin cambiar el sistema.** `eval_fase_b.py` repite la fase B de la etapa 7 en solo lectura, sobre la copia oficial y sobre esta, y guarda una fila por imagen. El ruteo es determinista, así que debe reproducir los conteos del log. La evocación muestrea con `random` sin semilla (la etapa 7 no la fija), así que un solo número varía entre corridas; el script la repite con las semillas 0 a 9 en los dos codificadores y da la media y el rango. Las semillas se fijan aquí, antes de ver datos.

**Cambios durante la corrida (declarados).**
1. *Evocación con una semilla, no diez.* Con la máquina cargada cada evocación tardó unos 15 s: diez pasadas de 113–116 costaban unas 4.7 h por codificador, en la ruta crítica. Se cortó la primera corrida antes de que terminara la semilla 0 (no se vio ninguna evocación repetida) y se hace una pasada con semilla 0 por codificador. El número de la etapa 7 (sin semilla) se reporta aparte.
2. *Orden de los procesos.* Para no pasar de dos procesos pesados se detuvo una primera fase B oficial que corría junto a la etapa 5, y luego la fase B sin clase de la cadena. Al cortarse la cadena, exp16 6–10 se lanzó a mano con el mismo comando. La fase B con evocación de las dos copias corre al terminar exp16 1–5. Nada de esto cambia qué se mide.
3. *Diagnóstico añadido después de ver el ruteo* (`diag_envolventes.py`, solo lectura, en las dos copias): cuántas memorias de contenido contienen cada imagen de test, y la separación de clases coordenada por coordenada (varianza entre medias de clase sobre varianza dentro de clase, en los 1600 originales del llenado). Explica el resultado; no entra en los umbrales de arriba.
4. *exp16 en dos procesos de un trabajador* (pliegues 1–5 y 6–10) en lugar de `--workers 4`, por la misma regla. La lógica por pliegue es la misma; el reporte se generó con `--report-only` al final.

## Qué apoyaría cada lectura (fijado antes de correr)

El punto medio entre el oficial (96.2 %) y exp19 (80.5 %) es 88.4 %.

- **La supervisión de clase sostiene el índice visual** si el ruteo de test queda en 88 % o menos, o los falsos llegan a 20 o más de 656 (≥ 3 %), o exp16 en objeto nuevo baja a 80 % o menos de punta a punta. Es decir, más de la mitad de la caída de exp19 se explicaría por quitar la pérdida de clase.
- **El mecanismo se sostiene sin supervisión de clase** si el ruteo de test queda en 93 % o más, los falsos en 7 o menos (≈ 1 %) y exp16 en objeto nuevo en 85 % o más con falso ruteo ≤ 1 %. La caída de exp19 sería sobre todo del cambio de representación.
- Entre los dos umbrales: dependencia parcial; se reportan los números sin forzar una lectura.

## Qué no separa este experimento

- Los dos codificadores parten de ResNet18 con pesos de ImageNet, que se entrenaron con etiquetas de ImageNet. Aquí se quita la supervisión con las clases de ETH-80, no esa.
- Los dos se entrenan con todo train, con los 10 objetos de cada clase. La fuga de exp16 que señala el jurado (M4) sigue, ahora solo por reconstrucción.
- Los dos eligen el mejor punto de control por RMSE de test. El oficial se entrenó en CPU y el sin clase en GPU.

## Resultados

Tabla completa en `comparacion.md` (la genera `comparar.py` desde los logs, las filas y los `resumen.json`; también `comparacion.json`). Oficial = `MAE-TMS-una-hetero` (logs de la corrida oficial y su `results/experimento16/`).

| medida | oficial (MSE + 0.1·CE) | sin pérdida de clase |
|---|---|---|
| τ (regla del código: 0.9 × norma mínima de los 1600 originales) | 16.61 | 13.79 |
| fase A, acierto al formar directorios (1024) | 99.9 % | **81.0 %** |
| fase A, rechazo / sin energía | 0.8 % / 1 | 0.9 % / 0 |
| ruteo de test | 631/656 = 96.2 % | **462/656 = 70.4 %** |
| falsos ruteos de test | 2 (0.3 %) | **169 (25.8 %)** |
| rechazo de test (sin energía) | 23 = 3.5 % (4) | 25 = 3.8 % (0) |
| evocación top-3, log de la etapa 7 | 113/116 = 97.4 % | 84/113 = 74.3 % |
| evocación top-3, semilla 0 | 113/116 = 97.4 % | 87/113 = 77.0 % |
| evocación, semilla 0, bien ruteadas / mal ruteadas | 113/116 / — | 80/81 / 7/32 |
| etapa 6, ganadores iguales al oficial | 16/16 | 16/16 |
| etapa 8, fidelidad | 16/16 | 16/16 |
| exp16, objeto conocido, punta a punta | 95.5 [95.1, 95.9] | **69.9** [68.0, 71.6] |
| exp16, objeto conocido, falso ruteo | 0.1 % (3 de 3280) | **23.6 %** (773) |
| exp16, objeto nuevo, punta a punta | 89.2 [85.1, 93.2] | **59.3** [55.5, 62.9] |
| exp16, objeto nuevo, directorio acepta | 92.2 [88.6, 95.4] | 95.5 [94.2, 96.6] |
| exp16, objeto nuevo, falso ruteo | 0.1 % (2 de 3280) | **30.2 %** (992) |
| exp16, brecha de punta a punta conocido − nuevo | 6.3 [2.5, 10.4] | 10.6 [6.8, 14.8] |
| exp16, fase A por pliegue (acierto de las registradas) | 1013/1014 | 832/1013 |

- **Falsos de test.** Se concentran entre animales y hacia dog: horse → dog 34, cow → dog 31, horse → cow 15, car → dog 11, tomato → apple 9, apple → tomato 8. Por clase, aciertos de 82: horse 31, cow 38, car 53; las demás entre 66 y 71. El oficial tiene 2 falsos, los dos horse → dog.
- **Falsos de exp16 en objeto nuevo.** horse → dog 161, cow → dog 114, dog → horse 93, horse → cow 76, cow → horse 64, dog → cow 56; 564 de los 992 son entre animales.
- **Texto.** Las etapas 6 y 8 dan los mismos 16 ganadores y la misma fidelidad que el oficial. El ruteo de texto no pasa por el codificador.
- **El directorio de la fase A ya nace sesgado.** El TME registra 2880 a dog contra 1616 a horse (oficial: 2016–2048 por agente).

**Diagnóstico** (`diag_envolventes_*.json`, añadido después de ver el ruteo):

| | oficial | sin clase |
|---|---|---|
| la memoria de contenido propia contiene la imagen de test | 98.6 % | 98.3 % |
| al menos una memoria ajena también la contiene | 0.5 % | **82.9 %** (cow 98.8, dog 97.6, horse 97.6, cup 62.2) |
| memorias ajenas que la contienen, media | 0.005 | 2.27 |
| separación por coordenada (entre/dentro), mediana de 64 | 5.34 | **0.24** |
| coordenadas con separación > 1 | 64 de 64 | 5 de 64 |
| niveles ocupados por clase y coordenada (de 32) | 8.1–12.5 | 15.5–20.2 |

## Lectura

- **Se cumple la lectura «la supervisión de clase sostiene el índice visual»**, y por los tres criterios fijados antes: ruteo de 70.4 % (umbral ≤ 88), 169 falsos (umbral ≥ 20), exp16 en objeto nuevo 59.3 % (umbral ≤ 80). Quitar solo la pérdida de clase cuesta 25.8 puntos de ruteo, más que los 15.7 de exp19 al cambiar todo el codificador por ImageNet + PCA (80.5 %, 83 falsos). En exp16, el objeto nuevo queda casi igual que en exp19 (59.3 contra 60.8) con el doble de falsos (30.2 contra 14.4 %).
- **El fallo deja de ser rechazo.** El rechazo de test no se mueve (3.5 → 3.8 %); lo que crece son los falsos (0.3 → 25.8 %). La propiedad «el fallo es rechazo, no invención» depende de la pérdida de clase.
- **Por qué.** La sonda lineal sobre este latente da 94.2 %: la clase sigue ahí, pero repartida en combinaciones de coordenadas. La memoria no lee combinaciones: contiene una imagen si cada coordenada cae dentro de lo registrado. Sin la pérdida de clase, ninguna coordenada separa bien las clases (mediana 0.24 contra 5.34). Cada clase ocupa casi el doble de niveles, y en el 83 % de las imágenes de test otra memoria también las contiene. La compuerta de contenido deja de excluir y el directorio, formado con 19 % de percepciones mal asignadas, rutea mal. Con el codificador oficial las envolventes casi no se tocan (0.5 %).
- **La evocación cae por el ruteo, no por la memoria.** Bien ruteada, la imagen evoca su dominio en 80 de 81 casos; mal ruteada, en 7 de 32, por vocabulario compartido.
- **Mejor reconstrucción, peor índice.** RMSE 0.082 contra 0.110.
- **Para «sin clasificadores supervisados».** Es cierto que ningún clasificador participa en la memoria: la cabeza no se usa en las etapas 5–8 ni en exp16. Pero el ruteo visual depende de que el codificador se entrenó con las etiquetas de clase de ETH-80. Sin ellas, con la misma receta, baja de 96.2 a 70.4 %. El texto no depende de eso.

## Límites

- Un codificador por condición, semilla 42. No hay varianza entre entrenamientos.
- Los dos parten de pesos de ImageNet (supervisados con etiquetas de ImageNet) y vieron los 10 objetos de cada clase. La fuga de exp16 sigue en las dos condiciones.
- La evocación es una sola pasada por codificador (semilla 0). La diferencia (97.4 contra 77.0 %) es mucho mayor que la que hay entre la pasada sin semilla y la de semilla 0 (oficial 113 y 113; sin clase 84 y 87).

## Tiempos

`tiempos.txt`. Etapa 5: 55 min (referencia 36). Etapa 7: 34 min (referencia 25). exp16: dos procesos de 225 min en paralelo (referencia 102 min con 4 trabajadores); cada pliegue tomó 43–50 min. Cada pasada de evocación tomó 31–38 min, y el ruteo de la fase B, 7 s. De punta a punta, de 07:34 a 13:26: 5 h 52 min de reloj. Durante las dos primeras horas corrían en la máquina otros dos procesos pesados de otro experimento.

## Archivos

- `correr.sh`: pipeline (etapas 5–8, τ, latentes y pliegues de exp16). `correr.out` está vacío. La cadena se cortó en `fase_b` (rc 127 = detenida a mano, ver cambio 2), y exp16 6–10 y el reporte se corrieron a mano con los mismos comandos.
- `eval_fase_b.py`: filas por imagen de la fase B, con evocación con semilla. Salidas `filas_fase_b_{sinclase,oficial}.json` y `fase_b_{sinclase,oficial}.log`. `fase_b.log` es la corrida detenida.
- `diag_envolventes.py` → `diag_envolventes_{sinclase,oficial}.json`.
- `comparar.py` → `comparacion.md`, `comparacion.json`.
- `stage*.log`, `tau.log`, `exp16_*.log`; `exp16/` (README, resumen, figura, filas por pliegue, `latentes.npy`).
- En `models/` de la copia quedan el codificador sin clase y todo lo regenerado. No se escribió nada en la copia oficial: los scripts sobre ella corrieron con `python -B` y solo leen.
