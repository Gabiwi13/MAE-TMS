# Líneas base ajenas a la memoria asociativa (jurado M3)

Worktree `MAE-TMS-lineasbase`, desacoplado en `df2f893` (rama `una-hetero`). Solo lee las memorias, el codificador y los latentes oficiales (`models/`, copiados de `MAE-TMS-una-hetero`); no reentrena ni escribe en ellos.

## Pregunta

¿Qué agrega la memoria asociativa sobre decisores simples que usan exactamente los mismos vectores?

## Diseño (escrito antes de correr)

### Texto

**Entradas, las mismas del sistema.**
- Tokens: `tokenize_query` de `src/stage6_interaction.py`, con spaCy `en_core_web_sm` y el rescate léxico incluido.
- Vectores: `get_fasttext_vector` sobre `load_all_vectors(nlp)`, con alias por lema y el caché `models/token_vectors.json`, sin vectores sintéticos. Un token sin vector se descarta igual que en el sistema.
- Variante cuantizada: `quantize_binary(v, 16)`, la pista que ve la memoria, llevada al centro de cada nivel, `x = 2(q+0.5)/16 − 1`, para que el coseno tenga sentido.

**Clases.**
- Puntos: las 21 etiquetas con vector de `label_vectors_<clase>.json`, el nombre de la clase incluido. Hay 168 puntos; las etiquetas compartidas (animal, fruit, mammal, pome, red, table) aparecen una vez por clase.
- Pesos: la frecuencia de `labels_<clase>.json`, la misma que expande `build_label_sequence` al llenar.

**Decisores.**
- `voto`: s_c es el número de tokens de la consulta que están en el vocabulario de la clase, tomado como las llaves de `load_all_vectors(nlp)[c]`, es decir, etiquetas más alias por lema. Si ninguna clase recibe voto, el decisor se abstiene.
- `centroide`: μ_c es la media de los vectores de las etiquetas.
- `centroide_frec`: μ_c es la media ponderada por la frecuencia.
- `1nn`: la etiqueta más cercana por coseno.
- `5nn`: las 5 etiquetas más cercanas por coseno, con un voto por punto. Si hay puntos empatados con el quinto, por ejemplo una etiqueta compartida, entran todos.

**Agregación de la consulta, las dos declaradas.**
- `token`: cada token decide o puntúa por separado y se suma.
  - Centroide: s_c = Σ_t cos(v_t, μ_c).
  - 1nn: cada token da un voto a la clase de su vecino; si el vecino es una etiqueta compartida, el voto se reparte en partes iguales.
  - 5nn: cada token reparte un voto entre sus vecinos.
- `media`: un solo vector v̄, la media de los vectores de los tokens, y la misma regla.

**Representación.** Vectores crudos y cuantizados (m = 16). El voto no depende de la representación.

**Empates.** Se declaran así:
- La decisión es el argmax de s_c.
- Si varias clases empatan en el máximo, el acierto se cuenta como su esperanza bajo un sorteo uniforme entre las empatadas: 1/k si la verdad está entre las k.
- Se reportan también el número de empates y las cotas: el empate como abstención (inferior) y el empate resuelto a favor de la verdad (superior).
- No se usa el orden de `CLASSES`, que favorecería a apple.

**Rechazo.** Ningún decisor tiene umbral. Todos aceptan cualquier consulta con al menos un token con vector; el voto acepta si algún token está en algún vocabulario. Las 40 consultas fuera de dominio se escribieron sin palabras del vocabulario (`results/experimento11/consultas_fuera_dominio.txt`; las 12 primeras son anteriores a esa regla), así que el rechazo del voto ahí viene en buena parte de cómo se construyó el banco.

**Particiones.**
- `cal400`: las primeras 400 de `ALL_QUERIES`, la calibración de `run_ablation.py` con N = 400. Sistema: temprana 90.0, madura B1 93.0 %.
- `proto80`: las primeras 80, el protocolo completo de `run_experiment3.py`. Sistema: temprana 81.2, madura B1 81.2 %.
- `res171`: las reservadas de exp11, con `load_bank` + `split_bank(bank, 30)` de `run_experiment11_monolithic.py` (240 de formación, 171 reservadas). Sistema: T-protocolo con N = 200, ruteo correcto sobre las 171, en promedio 97.0 % (de 95.9 a 97.7 % entre las 10 semillas de `results/experimento11/raw`).
- `ood40`: las 40 fuera de dominio. Se reporta cuántas acepta cada decisor.

**Referencias del sistema que se recalculan aquí, solo con lectura.**
- `eam_temprana`: el broadcast de la fase temprana, la suma de `recognize_gated` sobre los tokens y el argmax, sin directorio. Se calcula en las cuatro particiones con las `mem_dom_*.pkl` oficiales. Rechaza si ningún agente da soporte.
- Madura B1 de `cal400` y `proto80` por consulta: `run_single_experiment("B1", N, 0)` de `run_ablation.py`, como control de que el entorno reproduce 93.0 y 81.2.
- `res171` por consulta: las filas de T-protocolo de `results/experimento11/raw` (N = 200, rep 0, 10 semillas).

**Extras declarados.**
- `tabla_conteos`, la comparación del directorio contra una tabla de conteos que pide M3:
  - Se forma con las mismas consultas y el mismo ganador temprano con que se forma el directorio: las 400, las 80 o las 240 de formación de exp11.
  - Para cada token exacto se cuentan los registros por clase.
  - Lectura: s_c = Σ_t cuenta[t, c] / (registros_c + 1), la misma calibración B1 del directorio (`predict_normalized`, eps = 1), pero con identidad exacta del token en lugar de memoria asociativa.
  - Sin soporte, se abstiene.
- Separabilidad dentro contra fuera de dominio, sin elegir umbral, para los decisores de similitud con agregación `media`:
  - el AUROC de un puntaje de confianza entre `res171` y `ood40`. El puntaje es el coseno máximo a un centroide en los centroides, el coseno a la etiqueta más cercana en 1nn y el coseno medio de los vecinos en 5nn;
  - cuántas de las 40 se aceptarían con el umbral que deja pasar el 100 % y el 95 % de `res171`. Ese umbral se fija con los datos de evaluación, lo que favorece a la línea base.
- McNemar exacto (binomial de los pares discordantes) entre la mejor línea base de cada partición y el sistema, consulta por consulta.

### Imagen

**Datos.**
- Prueba: las 656 imágenes `splits[clase]["test"]` (82 por clase), con las rutas de `splits.json` remapeadas a `data/eth80` de este worktree.
- Latentes de prueba: `image_to_latent` de `src/stage7_bidirectional.py` con `models/encoder.pt`, solo la imagen original, igual que la fase B.
- Llenado: `models/instance_latents_<clase>.json`, 3200 por clase (200 imágenes × 16 variantes, imagen por imagen).
  - `16var`: los 3200.
  - `var0`: solo la variante 0, índices `::16`, 200 por clase.

**Decisores.**
- Centroide euclidiano y coseno.
- 1-NN y 5-NN, euclidiano y coseno.
- En 5-NN gana la mayoría. Un empate de mayoría lo resuelve la menor distancia media entre las empatadas; si persiste, se usa la esperanza uniforme.

**Representación.** El latente crudo (principal). Como extra, el cuantizado que ve el directorio (`quantize_latent_global`, 32 niveles) llevado al centro del nivel.

**Rechazo.** Sin umbral, los decisores aceptan las 656. El sistema rechaza antes de la memoria los latentes sin energía (`latent_has_energy`); se reporta cuántas imágenes caen ahí.

**Referencias.**
- `sistema`: `route_transactive` con las `agent_*.pkl` oficiales (directorios visuales de la etapa 7), la misma regla de entrada (`CLASSES[(ci+1) % 8]`), `XI_VISUAL` y la compuerta de energía. Debe dar 631/656 con 2 falsos; si no, se reporta la diferencia.
- `clasificador`, extra declarado: la cabeza `models/classifier.pt` entrenada junto con el codificador (MSE + 0.1·CE), sobre los mismos latentes. No es un decisor sin entrenamiento; indica cuánto separa el propio codificador.
- McNemar exacto contra el sistema, imagen por imagen.

### Qué apoyaría o debilitaría cada lectura

- **El mecanismo aporta en la decisión de clase.** Lo apoyaría que el sistema supere con claridad a las líneas base en las particiones fuera de muestra (`res171`, `proto80`) con el mismo rechazo, o que las iguale rechazando mucho más fuera de dominio. Lo debilitaría que alguna línea base sin memoria iguale o supere el acierto del sistema.
- **El aporte está en el rechazo y no en la clase.** Lo apoyaría que las líneas base igualen la clase pero acepten las 40 fuera de dominio (o, con umbral a posteriori, muchas), mientras el sistema acepta 2.
- **El banco premia la coincidencia léxica (M3).** Lo apoyaría que el voto exacto se acerque al sistema en `res171`, donde el 88 % trae el nombre de la clase, y se aleje en `proto80`.
- **El directorio contra la tabla de conteos.** Si la tabla iguala la madura B1, el directorio asociativo no agrega sobre contar tokens exactos en estas consultas. Si la supera, el aporte está en la generalización entre tokens parecidos.
- **Imagen.** Si un 1-NN o un centroide sobre los mismos latentes da ≥ 631/656 con 2 falsos o menos, el enrutamiento visual no agrega en clase sobre el codificador (M4). Si da menos, la diferencia es lo que agrega el directorio. Sin umbral, ningún decisor rechaza, así que los falsos de la línea base son todos sus errores.

## Resultados

Tiempos: texto 47.7 s, imagen 21.3 s y análisis posterior 39 s (`tiempos.txt`). Controles: el entorno reproduce la temprana de 90.0 y la madura B1 de 93.0 en `cal400`, 81.25 y 81.25 en `proto80`, y 631/656 con 2 falsos y 23 rechazos en imagen.

### Composición de las particiones

| partición | n | trae el nombre de la clase | algún token del vocabulario propio | algún token exclusivo de su clase |
|---|---|---|---|---|
| cal400 | 400 | 199 | 393 | 359 |
| proto80 | 80 | 11 | 76 | 64 |
| res171 | 171 | 150 | 171 | 170 |
| ood40 | 40 | — | 2 (con algún token de algún vocabulario) | — |

### Texto: acierto sobre el total

- Acierto esperado con desempate uniforme. Cada celda dice «crudo / cuantizado» cuando difieren; entre corchetes, las cotas por empate; `e`, el número de empates.
- El voto y la tabla no dependen de la representación.

| decisor | cal400 | proto80 | res171 | ood40 acepta |
|---|---|---|---|---|
| voto | 87.1 [81.5, 93.8] e49 | 79.4 [73.8, 86.3] e10 | 95.1 [91.8, 98.8] e12 | 2 |
| centroide, token | 82.8 / 82.5 | 77.5 | 86.5 / 86.0 | 40 |
| centroide, media | 81.3 / 81.5 | 77.5 | 84.8 | 40 |
| centroide_frec, token | 83.8 / 82.8 | 78.8 / 77.5 | 87.7 / 87.1 | 40 |
| centroide_frec, media | 83.3 / 82.8 | 78.8 | 87.1 | 40 |
| 1nn, token | 80.8 [73.3, 89.0] e63 / 80.8 | 80.0 [75.0, 85.0] e8 / 79.4 | 79.7 [67.8, 93.6] e44 / 80.1 | 40 |
| 1nn, media | 85.6 [78.8, 96.8] e73 / 85.2 | 76.0 [65.0, 93.8] e23 | 95.1 [92.4, 98.8] e11 / 94.5 | 40 |
| 5nn, token | 84.0 [82.0, 86.0] e16 / 83.6 | 80.0 [78.8, 81.3] e2 / 78.8 | 87.3 [84.8, 90.1] e9 / 87.7 | 40 |
| 5nn, media | 87.5 [81.3, 94.0] e52 / 88.0 | 81.5 [73.8, 90.0] e13 | 92.7 [89.5, 95.9] e11 / 93.6 | 40 |
| tabla de conteos (extra) | 92.3 | 78.8 | 94.7 | 8 / 3 / 4 (tablas de 400 / 80 / 240) |
| **EAM temprana, sin directorio** | **90.0** | **81.25** | **97.7** | **2** |
| **sistema, fase madura** | **93.0** (B1, dentro de muestra) | **81.25** | **97.0** (T-protocolo; 95.9–97.7 en 10 semillas) | **4 en el directorio, 2 con la compuerta** (exp11, N = 200) |

**Separabilidad sin umbral previo**, agregación `media`, `res171` contra `ood40`:

| decisor | AUROC crudo / cuant | ood aceptadas con el umbral que deja pasar el 100 % de res171 | ídem con el 95 % |
|---|---|---|---|
| centroide | 0.987 / 0.986 | 23 / 22 | 3 / 3 |
| centroide_frec | 0.992 / 0.991 | 20 / 16 | 2 / 2 |
| 1nn | 0.973 / 0.974 | 9 / 9 | 2 / 2 |
| 5nn | 0.971 / 0.971 | 18 / 22 | 4 / 4 |

**McNemar exacto**, con los pares discordantes (solo la línea base acierta, solo el sistema acierta):
- **cal400**, contra la madura B1:
  - mejor línea base (5nn media cuant), contando el empate como fallo: 4 contra 50, p = 4·10⁻¹¹;
  - voto: 2 contra 48;
  - tabla de conteos: 5 contra 8, p = 0.58.
- **proto80**, contra la madura B1:
  - mejor línea base (5nn media crudo): 6 contra 12, p = 0.24;
  - voto: 1 contra 7, p = 0.07;
  - tabla: 2 contra 4, p = 0.69.
- **res171**, contra T-protocolo, el intervalo de p entre las 10 semillas:
  - voto con el empate como fallo: de 3–5 contra 11–14, p de 0.02 a 0.14;
  - voto con el empate a favor de la verdad: p de 0.18 a 0.69;
  - tabla: de 0–5 contra 4–7, p de 0.06 a 0.77.

### Análisis posterior (hecho después de ver lo anterior; `analisis_posterior_texto.py`)

1. **La compuerta de la EAM es la pertenencia léxica.**
   - Se recorrieron todos los tokens del banco y de las 40 fuera de dominio contra las 8 clases, 3064 pares. `recognize_gated > 0` ocurre exactamente cuando el token está en el vocabulario de la clase (etiquetas más alias por lema): 101 pares aceptan y están en el vocabulario, 2963 rechazan y están fuera, y no hay ninguna discrepancia.
   - Por eso la EAM temprana acepta exactamente las mismas consultas que el voto en las cuatro particiones: 393/400, 76/80, 171/171 y 2/40, consulta por consulta.
   - Las dos fuera de dominio que pasan son las mismas en el voto y en la EAM: «a kitchen appliance that heats food» (food → apple) y «a wooden table and chairs» (table → cup). Son las únicas 2 de las 40 con algún token del vocabulario, así que también son las 2 que acepta T-protocolo con compuerta en exp11.
2. **Lo que la EAM agrega sobre el voto en texto es el desempate.** Entre las clases que contienen algún token, la activación media decide.
   - Contra el voto con desempate al azar: +2.9 puntos en cal400 (90.0 contra 87.1), +1.9 en proto80 y +2.5 en res171.
   - En las consultas donde el voto tiene un ganador único, la EAM acierta exactamente donde acierta el voto: McNemar de 0 contra 34, 0 contra 6 y 0 contra 10 con el empate como fallo, y de 15 contra 0, 4 contra 0 y 2 contra 0 con el empate a favor de la verdad.
   - Toda la diferencia está en las consultas empatadas:

     | partición | empates | aciertos de la EAM en ellos | esperanza del sorteo |
     |---|---|---|---|
     | cal400 | 49 | 34 | 22.5 |
     | proto80 | 10 | 6 | 4.5 |
     | res171 | 12 | 10 | 5.7 |
3. **Un voto ponderado por la frecuencia relativa de la etiqueta reproduce casi todas las decisiones de la EAM.** Es frecuencia / total de la clase, la proporción con que la etiqueta entra al llenado.
   - Toma la misma decisión en 380/400, 76/80 y 167/171 consultas.
   - Acierta 88.0, 80.0 y 96.5 % contra 90.0, 81.25 y 97.7 de la EAM (McNemar de 5 contra 13, p = 0.10; 1 contra 2; 1 contra 3).
   - Con la frecuencia absoluta queda en 81.0, 69.8 y 90.9.

### Imagen: 656 imágenes de prueba

| decisor | 16 variantes | variante 0 | falsos (16var / var0) | rechazos |
|---|---|---|---|---|
| **sistema** (route_transactive, etapa 7) | **631 (96.2 %)** | — | 2 | 23 (4 sin energía) |
| clasificador del codificador (extra) | 654 (99.7 %) | — | 2 | 0 |
| centroide euclidiano | 652 (99.4) | 652 (99.4) | 4 / 4 | 0 |
| centroide coseno | 653 (99.5) | 653 (99.5) | 3 / 3 | 0 |
| 1-NN euclidiano | 655 (99.8) | 652 (99.4) | 1 / 4 | 0 |
| 1-NN coseno | 655 (99.8) | 654 (99.7) | 1 / 2 | 0 |
| 5-NN euclidiano | 655 (99.8) | 654 (99.7) | 1 / 2 | 0 |
| 5-NN coseno | 655 (99.8) | 654 (99.7) | 1 / 2 | 0 |

- Con los latentes cuantizados que ve el directorio (extra), los resultados son iguales o difieren en una imagen: de 652 a 655. No hubo empates.
- McNemar contra el sistema, en todas las variantes: la línea base acierta sola en 23–24 imágenes y el sistema en 0–3, con p < 10⁻⁴.
- **Las 23 imágenes que el sistema rechaza las clasifica bien el 1-NN euclidiano**, con 16 variantes y con la variante 0, incluidas las 4 sin energía. El centroide euclidiano y el clasificador fallan una de ellas (cow3-068-090 → horse).
- De los 2 falsos del sistema, horse7-000-000 → dog lo fallan también todas las líneas base; horse7-035-135 → dog lo aciertan todas.

### Lectura

- **Texto, clase.**
  - En la partición más difícil (proto80, 11 de 80 con el nombre de la clase), los decisores sin memoria quedan al nivel del sistema: 5nn media 81.5, 1nn por token 80.0 y voto 79.4, contra 81.25.
  - En las reservadas (res171, 88 % con el nombre), el voto y el 1nn media dan 95.1 contra 97.0 de T-protocolo y 97.7 de la EAM temprana. Son unas 3 o 4 consultas de 171, y su significancia depende de cómo se cuenten los empates y de la semilla.
  - En cal400 la madura B1 (93.0) supera a todas las líneas base sin formación (88.0 como máximo). Pero esa ventaja viene de formarse con las mismas 400 consultas que se evalúan: una tabla de conteos de tokens exactos formada igual da 92.3 y no se distingue del directorio (5 contra 8, p = 0.58). Lo mismo en proto80 y res171. **En estas consultas, el directorio asociativo no agrega sobre contar tokens exactos.**
- **Texto, rechazo.**
  - Los decisores sin umbral aceptan las 40 fuera de dominio, y el sistema 2.
  - Ese rechazo es idéntico al del voto léxico, porque la compuerta de la EAM es la pertenencia al vocabulario y el banco fuera de dominio se escribió sin palabras del vocabulario.
  - Un umbral de coseno puesto a posteriori separa bien (AUROC de 0.97 a 0.99), pero para no perder ninguna reservada deja pasar de 9 a 23 de las 40.
  - El aporte del sistema en rechazo es real frente al coseno, pero no frente a la búsqueda léxica.
- **Imagen.** El enrutamiento visual queda 3.6 puntos por debajo de cualquier decisor simple sobre los mismos latentes (631 contra 652–655 de 656), sin ganar en falsos (2 contra 1–4). Lo que pierde son rechazos de imágenes de dominio que un 1-NN clasifica bien. La separación de clases la hace el codificador supervisado (su propia cabeza da 654/656), lo que apoya M4. El rechazo visual, que sería lo que el directorio agrega, no se puede valorar aquí porque no hay imágenes reales de otras categorías (M7).

### Desviaciones del diseño

- El McNemar del diseño no decía cómo contar los empates. En la tabla se cuentan como fallo, la cota desfavorable a la línea base. En el análisis posterior se da también la cota favorable.
- El análisis posterior completo (compuerta contra vocabulario, voto por frecuencia, McNemar con las dos cotas y las fuera de dominio aceptadas) se agregó después de ver los resultados. No cambia ninguna cifra de las tablas declaradas.
- La primera corrida de texto falló por una llave mal nombrada (`raw` contra `crudo`) antes de producir cifras. Se corrigió y se volvió a correr.

## Archivos

- `lineas_base_texto.py`, `lineas_base_imagen.py`, `analisis_posterior_texto.py`
- `resumen_texto.json`, `filas_texto.json` (una fila por consulta y decisor), `analisis_posterior_texto.json`
- `resumen_imagen.json`, `filas_imagen.json`
- `log_texto.txt`, `log_imagen.txt`, `log_posterior.txt`, `tiempos.txt`
