# Experimento 13: lectura de los resultados

**Corrida:** 22–23 de septiembre de 2026. 13 combinaciones (Vc variantes en el contenido, Vd en el directorio, N imágenes de llenado) × 5 semillas (42–46), 656 imágenes de test, tablas con intervalos en `README.md`, diseño y criterio en `../../propuesta_exp13_augmentacion_visual.md`. Controles: Vc=4, N=200 es bit a bit el llenado oficial (8/8); el encoder en GPU cambia 148 de 409 600 niveles (0.036 %) respecto de los latentes oficiales, que son los que se usan.

## Las curvas

| medida (% de las 656) | brazo | V=1 | V=4 (oficial) | V=8 | V=12 | V=16 |
|---|---|---|---|---|---|---|
| directorio acepta | A1 solo directorio | — | 73.6 → 87.7 | 92.4 | 95.0 | 96.2 |
| | A2 solo contenido | 63.7 | 73.6 | 75.0 | 76.7 | 77.0 |
| | A3 ambos | 63.7 | 87.7 | 93.0 | 95.6 | 97.1 |
| contenido responde (hetero) | A2 / A3 | 19.1 | 76.2 | 86.4 | 93.3 | 96.2 |
| contenido acepta (homo) | A2 / A3 | 82.9 | 93.6 | 96.3 | 97.7 | 98.6 |
| punta a punta | A1 | — | 74.8 | 75.3 | 75.6 | 75.8 |
| | A2 | 18.4 | 66.5 | 72.3 | 76.4 | 76.8 |
| | A3 | 18.4 | 74.8 | 85.4 | 91.7 | **94.5** |
| falso ruteo | A1 / A3 | 0 | 0 | 0.2 / 0.3 | 0.2 / 0.4 | 0.2 / 0.2 |
| falso contenido (algún ajeno acepta) | A2 / A3 | 0 | 0.2 | 0.6 | 0.6 | 0.8 |
| densidad de `mem_dom_R` (celdas vivas) | | 31.5 | 35.4 | 37.5 | 39.3 | 40.0 |
| densidad de `mem_dir_R` (A3) | | 66.9 | 74.1 | 76.1 | 79.8 | 80.7 |

En A1 la fila «V=4» es la primera con augmentación en el directorio (el oficial es Vd=1: 73.6 %). N=328 con V=4 y Vd=1: directorio 77.4, responde 87.3, punta a punta 75.6.

## Criterio de refutación (§8), sobre A3 con V=16

- (a) Cobertura de punta a punta: 66.5 → 94.5, **+28.0 puntos** (umbral 10). Se cumple.
- (b) Falsos: 1 ruteo equivocado de 656 (0.2 %) y 5 imágenes aceptadas por un especialista ajeno (0.8 %); umbral 1 %. Se cumple.
- (c) Sondas sintéticas: ruido y píxeles barajados siguen rechazados por todos; el color sólido pasa de 1 a 3 especialistas (de 8, menos de la mitad) y **el directorio empieza a rutearlo** (a partir de Vd=8 en A3, Vd=16 en A1), cosa que antes no hacía. No alcanza el umbral, pero es un costo real: la fuga de «color sólido» de la limitación (b) crece con la densidad.

La hipótesis del reporte («la augmentación del llenado reduce el rechazo residual manteniendo cero falsos») queda **confirmada en la cobertura y matizada en los falsos**: no son cero, son 1 de 656 en el ruteo y 5 de 656 en el contenido, y la sonda de color sólido se acepta más.

## Lo que muestran los datos

**Son dos compuertas y cada una cede solo con su augmentación.** Augmentar solo el directorio (A1) lleva su aceptación de 73.6 a 96.2 % pero la cobertura total se estanca en 76 %, que es lo que responde la hetero. Augmentar solo el contenido (A2) lleva la respuesta de la hetero de 76 a 96 % pero el directorio sigue en 77 %. Solo A3 sube las dos, y la punta a punta llega al 94.5 %. Es la predicción P1; la P2 (la hetero cede más despacio) no se cumple: la conjunción de `project` gana casi al mismo ritmo que los huecos marginales del directorio (76 → 86 → 93 → 96 contra 74 → 88 → 92 → 95 → 96).

**La palanca es la densidad, y el rendimiento es decreciente.** Cada cuatro variantes más llenan 2 puntos de celdas de `mem_dom_R` (35 → 37.5 → 39 → 40 %) y de 2 a 4 del directorio; la cobertura sube 8.6, 7.0 y 2.9 puntos por escalón. Sin augmentación (V=1) la hetero responde el 19 % de las imágenes nuevas: el llenado oficial de 4 variantes ya aportaba 57 puntos.

**Imágenes reales contra variantes.** 128 imágenes reales más (N=328, 1312 registros por clase) dan a la hetero 87.3 % de respuesta, casi lo mismo que 4 variantes más de las 200 (Vc=8, 1600 registros: 86.4 %): por registro, la imagen real rinde un poco más, como decía P4, pero ninguna de las dos mueve el directorio (77.4 contra 75.0), porque el directorio se forma con sus propias percepciones.

**El precio.** Los falsos aparecen ya con la familia geométrica (V=8), antes de la fotometría; P3 predijo lo contrario. Son siempre los mismos: `horse7-000-000` (vista frontal) ruteada a dog en las cinco semillas desde Vd=8, `cow3-066-117` a dog en una semilla con V=16, y en el contenido horse y cow aceptadas por dog (y una horse por cow). Es el par animal que ya confunde al hemisferio textual. La sonda de color sólido es el otro costo: el especialista que la acepta pasa de 1 a 3 y el directorio la rutea con Vd ≥ 8 (A3). Un criterio de varianza mínima de la entrada, previo a la memoria, sigue siendo la mitigación pendiente para esa fuga.

**Precisión de la evocación.** Sobre las 5 imágenes evocadas por clase, el acierto estricto queda entre 96 y 100 % y el dominio ajeno entre 1 y 6 % sin tendencia clara con V (intervalos anchos: son 40 respuestas por semilla). No hay señal de que densificar degrade lo que se evoca.

## Lo que no decide

- Generalización a objetos nuevos: el split es por imagen, así que estas cifras son de vistas nuevas de los 10 objetos ya vistos de cada clase.
- Si conviene cambiar el llenado oficial (`models/`): con V=16 en contenido y directorio la cobertura pasaría de 66.5 a 94.5 % con 1 falso ruteo; la decisión es del autor y exige rehacer la etapa 5, la fase A y las verificaciones 8/8 y 16/16. Este experimento solo mide.
- Qué familia importa: las variantes son anidadas, así que se sabe cuánto suma cada escalón pero no si, por ejemplo, la escala rinde más que la rotación.
