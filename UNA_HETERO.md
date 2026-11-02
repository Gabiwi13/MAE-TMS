# Copia con una sola hetero por agente

Rama `una-hetero`, cortada de `b0542ab`. Cada agente guarda su contenido en una sola memoria, la hetero label ↔ latente. Las dos homo dejan de existir como memorias: sus pesos se leen de la hetero con `DomainView` (`src/associative_memory.py`), que cuenta cuántas veces se registró cada valor en cada coordenada, con pareja (interior) o sin ella (borde de valor indefinido).

La base para comparar es `MAE-TMS-base-homo`: el mismo commit, sin cambios.

## Qué cambió

- `src/associative_memory.py`: `DomainView` (pesos, reconocimiento, relación, entropía, recuerdo; no registra).
- `src/hetero_memory.py`: la hetero saca sus pesos de sí misma; sin `attach_homo`.
- `src/stage5_fill.py`: llena y guarda solo la hetero.
- `src/stage6_interaction.py`: `Agent(nombre, hetero)` con tres memorias. `mem_dom_L` y `mem_dom_R` son lecturas de la hetero. Un agente sin hetero (módulos solo de imagen) guarda su contenido en una homo latente, que es su única memoria de contenido.
- Scripts que construían sus propias homo o las cargaban: exp2, 3, 4, 5, 6, 11, 12, 13, 16, 17, 18, 21, ablación, industrial monolítico, app, router de `realtime_lab`, figuras, sonda de rechazo.

Sin cambios porque ya tienen una sola memoria de contenido (una homo latente por módulo): demo industrial, CLIP industrial, cierre MAE, parámetros MAE, piloto de módulos, demo médica, olvido y privacidad, enrutador de flota, exp24.

No aplican en esta copia (comparan homo contra hetero): `run_homo_marginal.py`, `run_homo_marginal_semilla.py`, `run_homo_sin_pareja.py`, `run_homo_borde.py`, `run_pesos_recuerdo.py`, `run_emparejamiento_desigual.py`.

## Verificación

Vista contra las homo oficiales, en los 8 agentes:

| | Resultado |
|---|---|
| Latente | idéntica celda por celda; pesos iguales en 50 pistas al azar con coordenadas indefinidas y fuera de rango; misma entropía |
| Etiquetas | mismo soporte; conteos multiplicados por un factor de 21 a 95 que varía entre celdas (la homo vieja registraba cada palabra una vez, la hetero la empareja con muchas imágenes) |
| Borde | vacío (el llenado oficial está todo emparejado) |

Etapas 6 a 8, corridas igual en los dos folders (la 5 no: la hetero es la misma):

| | Base con homo | Una hetero |
|---|---|---|
| Etapa 6, ganador por consulta | 16 | los mismos 16 (puntajes a ≤ 0.15 %) |
| Etapa 7, fase A | routing 99.9 %, rechazo 0.8 % | igual, mismos conteos de directorio |
| Etapa 7, fase B | 631/656 = 96.2 %, rechazo 3.5 % | igual |
| Evocación top-3 | 113/116 = 97.4 % | igual |
| Etapa 8, fidelidad | 16/16 | 16/16, log idéntico |
| exp3 | — | log idéntico |
| Sonda de rechazo | 10 rechazadas, 2 falsos | igual (puntajes a < 0.2 %) |

Las palabras de muestra de la etapa 7 cambian entre corridas porque esa etapa no fija semilla.

Logs en `logs_comparacion/` de cada folder.

## Cambios de fondo en algunos experimentos

Donde la homo vieja no era la marginal de la hetero, el experimento mide otra cosa en esta copia:

- exp6 (capacidad): con N imágenes la homo de etiquetas oficial tenía todas las palabras; ahora solo las N emparejadas.
- Ablación F/G: la hetero curada usaba las homo sin curar; ahora usa sus propios pesos.
- Industrial monolítico: si una celda de la homo latente se saturaba en 65 535, la vista no satura.

## Grupo 1 (30 oct, 2 h)

Corrido en esta copia y comparado contra los resultados con homo de `results/` (git diff contra `b0542ab`). Logs y tiempos en `logs_comparacion/grupo1/`.

| Script | Contra la base con homo |
|---|---|
| exp4 | sin cambios en sus archivos |
| Ablación (incluidas F y G) | regenerada; `ablation_metrics.csv`, el reporte y las figuras idénticos byte a byte |
| Figuras (`--fresh`) | `ablation_rows.csv` idéntico. Cambian fig12, fig14 y fig16. En fig12 la matriz de reconocimiento (168 etiquetas × 8 agentes) tiene el mismo ganador en las 168 y los mismos ceros; los valores se mueven hasta 0.29 %. fig14 y fig16 muestran recuerdos muestreados |
| Industrial monolítico | idéntico salvo el tiempo (M única 99.1 % normales, 90.1 % fallas, sin falsos) |
| exp9, sonda de fase 2 | mismas cifras de ruteo (23 ruteadas, 17 comparten primera pista); entropías al quinto decimal |
| exp5 | misma variedad (12/12 y 1/12); distancia entre recuerdos ±0.03 a ±0.14 (muestreo) |
| exp6 | acierto temprano con N = 50: 71.2 → 72.5 %; los otros cortes iguales |
| exp2 | los κ salen de cuantiles medidos y se corren un poco (1.754 → 1.755, 2.059 → 2.056). Con ι = 0 el corte del 90 % pasa de 12 % de acierto (rechazo 85 %) a 19 % (64 %), y el del 100 % de 2 % a 0 %. Sin κ sigue 81.2 %; la mejor columna con κ sigue 77.5 % |

## Grupo 2 (30–31 oct, 25 h)

Misma receta que la corrida base, en CPU. Los cachés de exp11 se reconstruyeron en la copia. Logs y tiempos en `logs_comparacion/grupo2/`. Tiempos: texto 694 min (incluye 2 h 40 min con la laptop suspendida), imagen 494, fuera de dominio 7.

### exp11

Comparado fila por fila contra los raw con homo (`git show HEAD:`), 10 semillas × 4 cortes.

| | Contra la base con homo |
|---|---|
| Imagen → texto (3 brazos, 3200 filas cada uno) | idéntico: misma aceptación, mismo destino, mismas etiquetas evocadas |
| Fuera de dominio (3 brazos, 2080 filas cada uno) | idéntico, con y sin compuerta |
| Texto, M y T-oráculo (20 520 filas cada uno) | mismas decisiones: acepta, destino, primera pista y responde iguales en todas |
| Texto, T-protocolo | destino distinto en 273 de 20 520 filas (1.3 %) |
| Recuerdo (texto, los 3 brazos) | el latente recordado cambia: `recall_from_left` pesa la pista de etiquetas con la vista, cuyos conteos no son proporcionales a los de la homo vieja. Clase 1-NN de M 97.33 → 97.40 % (117 filas pasan a error, 132 a acierto); oráculo 100 % |
| Control del llenado en N = 200 | las mismas 4 clases distintas de la oficial (car, cow, dog, horse; 600 a 1200 celdas de 9.8 millones) |

Ruteo correcto de T-protocolo por corte (5130 filas por corte):

| N | Base con homo | Una hetero | Filas con destino distinto (mejoran / empeoran) |
|---|---|---|---|
| 25 | 93.6 % | 95.3 % | 129 (102 / 15) |
| 50 | 97.3 % | 97.4 % | 42 (24 / 18) |
| 100 | 97.2 % | 97.4 % | 42 (27 / 15) |
| 200 | 97.0 % | 97.0 % | 60 (30 / 30) |

En N = 25 la formación de directorios acierta un poco más temprano (83.3 → 84.1 %, 2 de 233 consultas) y T-protocolo pasa de 95.6 a 96.9 % de clase 1-NN; M sigue en 97.6 %. En los otros cortes las diferencias quedan dentro de los intervalos.

### exp12

337 min. 28 pares, semillas 42–46, 3 sorteos. Contra el `README.md` con homo (commit d0df16c):

| estadístico (28 pares) | Base con homo | Una hetero |
|---|---|---|
| brecha M2 contra solapamiento en etiquetas | ρ −0.00 (p 0.996) | ρ 0.01 (p 0.95) |
| brecha M2 contra solapamiento latente | ρ 0.20 (p 0.30) | ρ 0.21 (p 0.29) |
| error de clase contra solapamiento en etiquetas | ρ 0.49 (p 0.008) | igual |
| brecha M2 contra etiquetas compartidas | ρ 0.18 (p 0.37) | ρ 0.21 (p 0.28) |
| brecha M2, media (mín a máx) | 2.83 (0.3 a 6.5) | 2.54 (−0.2 a 5.1) |
| brecha M8, media (mín a máx) | 5.82 (0.1 a 9.7) | 5.66 (0.6 a 9.1) |
| clase M2 en los pares con error | apple–tomato 93.3, apple–pear 99.1, cow–horse 97.6 | 93.9, 99.0, 97.6 |

Por par, la brecha de M2 se mueve hasta 1.4 unidades (media −0.28). 27 de 28 brechas siguen positivas; dog–horse pasa de +0.6 a −0.2. Ningún coeficiente cambia de lectura: la brecha no sigue al solapamiento en etiquetas, el error de clase sí, y M8 queda peor que M2 en 26 de 28 pares (igual que en la base).

`veredicto.md` (21 sep) es anterior a la re-corrida con pesos homo y ya no coincide con el README de la base (ρ 0.45 contra −0.00); eso viene de antes de esta copia.

## Grupo 3 (31 oct – 1 nov, 16 h de cómputo)

Logs y tiempos en `logs_comparacion/grupo3/`. Tiempos: exp21 78 min, exp17 114 (A 32, B 25, C 57), exp18 con sus 4 variantes 224, exp13 326, exp16 227. Windows se reinició dos veces durante exp18 (pantalla azul 0x7E en `MiPageFreeToZero`, del kernel, no del script); se reanudó desde los pliegues guardados con menos procesos.

| Script | Contra la base con homo (`git show HEAD:`) |
|---|---|
| exp18 y sus 4 variantes | idéntico fila por fila (2624, 697 y 3 × 1517 filas; soportes con diferencia 0) |
| exp17 B y C | idéntico fila por fila |
| exp17 A | 1 de 118 imágenes distinta (tomato j=3); top-1 en vocabulario 96.3 → 96.6 %, exclusivo 85.9 → 86.2 %. Cambia también el brazo prototipo, que no pasa por las memorias nuevas: la imagen se codifica al correr y el cambio viene del redondeo del encoder |
| exp13 (42 640 filas) | mismas decisiones en todas: contenido, responde, directorio, destino, ruteo, e2e. Cambian las etiquetas evocadas en 2064 filas |
| exp16 (6560 filas) | mismas decisiones en todas. Cambian las etiquetas evocadas en 208 filas: hit estricto de objeto nuevo 99.6 → 98.1 %, otro dominio 1.8 → 2.3 % |
| exp21 | idéntico a la base corrida de nuevo (1 nov, 75 min): mismo `resumen.txt` byte a byte, filas iguales salvo el tiempo de llenado. Contra los raw de git, T-protocolo cambia (us_mama 88.5 → 86.5, dermatoscopia 72.7 → 72.5, rx_torax 22.4 → 22.2): eso viene de los commits posteriores al 26 oct, no de esta copia |

La evocación de etiquetas es una muestra de la hetero sin semilla fija. En la propia base, dos semillas con la misma memoria de contenido difieren en 32 de 656 etiquetas (Vc4) y 39 (Vc16); base contra copia, en 32 y 38. Es el mismo ruido.

Los raw de exp21 en git son del 26 oct (25f84b7), anteriores a los cambios de pesos homo y del directorio (763c902, 3fd2c76, aa283f6, f4ef4c3, bae22c2), y ya no corresponden al código de `b0542ab`. Los README de `experimento21` y `medico*` siguen citando us_mama 88.5 para T-protocolo; con el código actual sale 86.5.

Dos problemas de exp13 que vienen de antes de esta copia:

- El control contra los `agent_*.pkl` oficiales se calcula con Vc = `FILL_VARIANTS` (16 desde el 23 sep). exp13 solo sustituye las variantes 0 a 3 por los latentes oficiales; las 4 a 15 salen de su propia codificación, así que su Vc16 difiere de los oficiales en 30 412 a 58 222 celdas por clase. Los raw de git traían el control de un caché viejo (Vc4, todo igual).
- El README suma esas celdas y escribe «323364/8 clases»: la línea cuenta celdas como si fueran clases.

## Costo de volver a correr

Solo hace falta correr la copia: los resultados con homo de la base son los que ya están en `results/`. Tiempos medidos en corridas anteriores (bateria_v16_tiempos.txt, raw/*.json, README de cada experimento); los de varias horas son suma de segundos por trabajo entre procesos, aproximados.

| Grupo | Scripts | Tiempo | Por qué |
|---|---|---|---|
| 1 | exp2 (5 min), exp4 (5), exp5 (10), exp6 (17), exp9 (~30, sin medición completa), ablación (23–29), industrial monolítico (5), figuras (29) | ~2.5 h | rápidos; exp6 y la ablación F/G cambian de fondo |
| 2 | exp11 (imagen 134 min + texto ~8.6 h), exp12 (4–7 h) | ~13–16 h | lado de texto, donde los pesos de etiquetas cambian de escala |
| 3 | exp13 (4–8 h), exp16 (~8–9 h), exp17 (sin medición), exp18 (~3–5 h), exp21 (75 min) | ~20–25 h | lado de imagen, donde la vista latente es la homo celda por celda |

El grupo 3 debería salir igual por construcción: sus homo latentes recibían exactamente los latentes de su hetero. Un pliegue de exp16 y un corte de exp13 (~1–2 h) lo comprobarían sin correr todo.

Los cachés de exp11 (`N*_V16.pkl`, 27 oct) y exp13 están en `pesos-homo/cache/`; la hetero es la misma, y al cargarlos el agente descarta sus homo viejas. Reusarlos ahorra los llenados (~1 h en exp11, ~50 min en exp13).
