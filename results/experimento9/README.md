# Experimento 9 — pérdida de un miembro

## Tesis
Russell (1910): el especialista conoce su dominio por familiaridad (vivió las instancias); los demás lo conocen por descripción (presenciaron que él ganaba y guardaron una envolvente de qué ganaba, exp8). La descripción puede ubicar y rutear, pero no debería reemplazar a la familiaridad. Wegner (1987) discute la pérdida transactiva cuando un miembro deja el grupo: el directorio sigue apuntando a alguien que ya no está. Marco completo en `discusion_marco_teorico_directorio.md`.

## Método
- Memorias oficiales de 8 clases (`models/agent_*.pkl`, etapas 6 y 7). Se quita un agente k y las consultas de su dominio entran por un sobreviviente (el siguiente en la lista; los directorios son idénticos entre agentes, exp8). El ruteo es el de la fase madura: `mem_dir.route_multi` (B1, xi=0) para texto, `mem_dir_R.route` (B1, xi=2) para imagen. Solo las consultas que el directorio rutea a k llegan a las políticas.
- Tres políticas del grupo sin k, y una referencia con k presente:
  - **vivido** (referencia): `mem_dom_H.recall_from_left` del especialista con la primera pista reconocida (etapa 8).
  - **sustitución**: el mejor sobreviviente según los scores del directorio responde con su propio contenido (mismo recall). Si ningún sobreviviente tiene score, no responde.
  - **descripción**: el sobreviviente responde con lo que presenció de k: `mem_dir_R.recall_domain(k)` (latente, hemisferio texto→imagen) o `mem_dir.recall_domain(k)` traducido a palabras por coseno (hemisferio imagen→texto).
  - **rechazo**: no responder. Su tasa es la de las otras dos políticas cuando no responden.
- Banco: las 411 consultas de 8 clases (`eval_bank`), 3 repeticiones por consulta (el recall muestrea). Imágenes: 10 de test por clase, 1 repetición (la evocación de etiquetas tarda ~20 s).
- Juez del hemisferio texto→imagen: clase del clasificador latente y clase del vecino real más cercano (6400 instancias), distancia a la instancia real más cercana del dominio perdido, y **dependencia de la pista**: dispersión entre consultas distintas (un sorteo por consulta) contra dispersión entre sorteos de la misma consulta, más la razón F = var(medias por consulta) / (var dentro / 3). F ≈ 1 significa que la respuesta no depende de la pista. También se mide cuántos niveles vivos por coordenada deja la proyección (cuánto restringe la pista).
- Juez del hemisferio imagen→texto: alguna de las 3 palabras evocadas pertenece al vocabulario ConceptNet del dominio perdido (como la etapa 7).

## Resultados

### El índice sobrevive al miembro

| ruteo del directorio (411 consultas, 80 imágenes) | texto | imagen |
|---|---|---|
| a k (el agente perdido) | 229 (55.7%) | 65 (81.3%) |
| a otro agente | 65 (15.8%) | 0 |
| rechazada | 117 (28.5%) | 15 (18.7%) |

El directorio apunta a k igual que antes: no sabe que k no está. Lo que el grupo pierde no es el índice sino la respuesta. El directorio de texto oficial tiene 52 registros (las 16 consultas de la fase temprana, exp8), de ahí que solo cubra el 56% del banco; pear y tomato se confunden entre sí y con apple (34 y 12 «a otro»).

### Texto → imagen (229 consultas × 3 sorteos = 687 por política)

| política | responde | clase perdida (clf · vecino) | d a instancia real de k | niveles vivos / coord. | disp. misma consulta | disp. consultas distintas | F (Bessel) |
|---|---|---|---|---|---|---|---|
| vivido (k presente) | 98.3% | 100% · 100% | 21.9 | **8.41** / 32 | 31.3 | 32.3 | 1.14 |
| sustitución | 24.5% | 0% · 0% | 48.0 (21.0 a su propia clase) | 7.98 | 30.1 | 33.5 | 2.08 |
| descripción | **100%** | 100% · 100% | **19.3** | 9.31 / 32 | 27.4 | 27.7 | 1.00 |

Corrida única con pista nan, semilla fija (`random` y `numpy`) y F con corrección de Bessel (commit bbde155). Con 20 semillas la descripción da 19.30 ± 0.13 y el vivido 22.03 ± 0.21 (`muestreo_resumen.json`).

Por clase (vivido | descripción: responde / d / niveles vivos; sustitución: responde / clase ok):

| perdido | ruteadas a k | vivido | descripción | sustitución |
|---|---|---|---|---|
| apple | 35 | 1.00 / 21.2 / 8.2 | 1.00 / 21.0 / 9.9 | 0.26 / 0 (responde tomato, pear) |
| car | 23 | 0.87 / 26.1 / 9.7 | 1.00 / 23.3 / 10.7 | 0 |
| cow | 31 | 1.00 / 20.2 / 7.9 | 1.00 / 16.3 / 8.7 | 0.26 / 0 (horse) |
| cup | 35 | 1.00 / 25.1 / 8.9 | 1.00 / 22.8 / 10.6 | 0 |
| dog | 23 | 1.00 / 25.3 / 9.5 | 1.00 / 19.8 / 9.8 | 0 |
| horse | 22 | 0.95 / 19.9 / 7.9 | 1.00 / 16.7 / 8.8 | 0.59 / 0 (cow, dog) |
| pear | 19 | 1.00 / 20.3 / 8.6 | 1.00 / 17.4 / 8.5 | 0.32 / 0 (apple) |
| tomato | 41 | 1.00 / 18.7 / 7.5 | 1.00 / 16.8 / 7.8 | 0.49 / 0 (apple) |

- La **sustitución confabula o calla**: cuando responde (24.5%) siempre es con la clase del sustituto (tomate por manzana, vaca por caballo), a 48 unidades de cualquier instancia de k. Cuando el directorio no da score a ningún sobreviviente (car, cup, dog) no responde.
- La **descripción conserva la clase siempre** (100% por los dos jueces) y cae más cerca de las instancias reales que el especialista: 19.3 contra 21.9 (12% menos), en siete de ocho clases (apple empata: 21.0 contra 21.2). Lo hace con una pista de identidad que deja 9.3 niveles vivos por coordenada contra 8.4 de la pista de texto en la memoria de contenido (11% más). Una proyección más ancha que cae más cerca se explica por lo que cada memoria guarda (`sonda_fase2.json`): el directorio visual registró unas 122 imágenes reales sin aumentación por agente; la memoria de contenido, 800 latentes con aumentación emparejados con etiquetas sin correspondencia (`stage5_fill` registra `label_seq[i % L]` con `z_q[i]`, cada etiqueta con 38 instancias distintas en promedio). Condicionar la memoria de contenido por etiqueta recorta niveles (8.28) y aun así dispersa más (32.1 contra 27.4).
- **La descripción no depende de la pista; el especialista, apenas.** La dispersión entre consultas distintas es casi la dispersión entre sorteos de la misma consulta (32.3 contra 31.3 en vivido; 27.7 contra 27.4 en descripción). La razón F con corrección de Bessel da 1.14 en vivido y 1.00 en descripción; bajo el nulo de independencia el F simulado es 1.00 (p5 0.98, p95 1.03), así que el vivido muestra una dependencia débil pero real y la descripción ninguna. Sin Bessel el nulo daba 1.44 y los valores publicados antes (1.64 y 1.46) eran ese sesgo. "Manzana roja" y "manzana verde" producen la misma distribución de latentes en el especialista. Fig. 1 lo muestra: la respuesta vivida y la descrita son la misma envolvente borrosa del dominio.

### Imagen → texto (65 imágenes ruteadas a k)

| política | responde | alguna etiqueta del dominio perdido | etiquetas típicas |
|---|---|---|---|
| vivido (k presente) | 89.2% | 100% de las respondidas | apple: «red skin green», «fruit green pome» |
| sustitución | 0% | — | ningún sobreviviente reconoce la imagen |
| descripción | **100%** | **100%** | tomato: «soup sauce vegetable»; dog: «pet dog canine»; horse: «horse animal mane» |

Aquí la descripción responde más que el especialista (100% contra 89%) y acierta igual (corrida con semilla; el 98.5% anterior era de una corrida sin semilla): la lectura inversa del directorio de texto es un vector de etiqueta de k y cae en su vocabulario. La sustitución no responde nunca, porque `evoke_labels` exige que la homo latente del sustituto contenga la imagen, y una imagen ajena nunca cabe.

### Dónde vive entonces la familiaridad (sonda)

Si el especialista no reproduce mejor que el testigo, ¿qué lo distingue? Sobre las 411 consultas del banco (`sonda_reconocimiento.json`):

| quién | reconoce las consultas de su dominio |
|---|---|
| el especialista (`recognize_gated` con su contenido) | **98.3%** |
| un no-especialista con su contenido | 16.1% (casi todo pear/tomato/dog, vecinos de apple) |
| el directorio (52 registros) las rutea a k | 55.7% |

El 43.6% de las consultas que el especialista reconoce no las rutea el directorio. La familiaridad no está en lo que el especialista *reproduce* sino en lo que *reconoce*: su contenido acepta casi cualquier pista de su dominio, incluso las que nadie le vio ganar; el directorio solo conoce las que presenció.

## Hallazgos
1. **La pérdida transactiva es asimétrica**: el índice no se pierde (el directorio sigue ruteando a k como si estuviera) y la respuesta sí. Es la situación que Wegner describe cuando un miembro deja el grupo.
2. **La sustitución es la peor política**: confabula con la clase del sustituto o calla. El grupo no debería redirigir al segundo mejor.
3. **La descripción responde siempre y conserva la clase siempre**, con fidelidad 12% mayor y una envolvente 11% más ancha que la del especialista. En imagen→texto responde más que el especialista.
4. **La tesis A, como se operacionalizó, no se sostiene**: el recall del especialista depende poco de la pista dentro del dominio (F 1.14 contra 1.00 del nulo) y su fidelidad es menor que la del testigo (21.9 contra 19.3). La razón está en el llenado: las etiquetas de ConceptNet son del dominio, no de la imagen, y `stage5_fill` empareja cada etiqueta con una instancia arbitraria. La memoria de contenido nunca recibió pares etiqueta-instancia con correspondencia, así que solo puede devolver la envolvente del dominio (exp5: prototipo emergente; exp8: la memoria no contiene la figura, contiene el conjunto de las compatibles). Para reproducir, el testigo sabe incluso algo más compacto que el especialista, porque su envolvente está hecha de imágenes reales sin aumentación.
5. **La familiaridad se desplaza del reproducir al reconocer.** El especialista reconoce el 98% de las consultas de su dominio; el no-especialista el 16%; el directorio rutea el 56%. La diferencia entre familiaridad y descripción, en este sistema, es de cobertura del reconocimiento, no de fidelidad de la reproducción. El reconocimiento tiene además una puerta que la descripción no tiene: los cuatro fallos del especialista (car 3, horse 1) son contención por coordenada, cada pista tiene de 12 a 76 coordenadas de etiqueta cuyo valor cuantizado el agente nunca registró, y coinciden exactamente con los ceros de su homo izquierda; la lectura inversa del directorio no pasa por esa puerta. Eso reformula a Russell sin abandonarlo: conocer por familiaridad es poder decir "esto es mío" ante lo nunca visto; conocer por descripción es poder decir "esto era de él" ante lo que se le vio.
6. Consecuencia para el TME: un miembro que sabe todo por descripción (la lectura inversa del directorio) puede sostener las respuestas del grupo cuando falta un especialista, con la misma clase y mejor fidelidad, pero no puede reconocer lo que el especialista no ganó delante de él.

## Archivos
- `results_text.csv`, `results_image.csv` — todas las respuestas (por consulta, política y sorteo) más una fila `ruteo` por clase
- `resumen.json` — las tablas de arriba
- `sonda_reconocimiento.json` — reconocimiento del especialista, del no-especialista y del directorio sobre el banco
- `fig1_respuestas.png` — por clase perdida: imagen real y la respuesta bajo cada política a la misma consulta
- `fig2_resumen_texto.png`, `fig3_resumen_imagen.png` — resúmenes por política

## Notas
- `run_experiment9_member_loss.py --text | --image | --report`; `run_experiment9_probe_recognition.py` para la sonda. No se modifica ninguna memoria ni etapa; `DirectoryMemory.recall_domain` es la lectura inversa declarada en esta corrida (antes vivía en el script de exp8).
- La fidelidad se mide en el espacio latente (distancia euclidiana a la instancia real más cercana). El juez clasificador es permisivo (exp8) y por eso no decide solo.
- Los recalls muestrean con `random` de Python (`hetero_lib`); la corrida siembra `random` y `numpy` con 42 al inicio. Las corridas anteriores a bbde155 solo sembraban numpy y no eran reproducibles.
