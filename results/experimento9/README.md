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

| política | responde | clase perdida (clf · vecino) | d a instancia real de k | niveles vivos / coord. | disp. misma consulta | disp. consultas distintas | F |
|---|---|---|---|---|---|---|---|
| vivido (k presente) | 98.3% | 100% · 100% | **21.9** | **8.41** / 32 | 31.4 | 32.3 | 1.64 |
| sustitución | 24.5% | 0% · 0% | 48.3 (21.5 a su propia clase) | 7.98 | 30.5 | 34.4 | 2.89 |
| descripción | **100%** | 100% · 100% | 23.3 | 9.31 / 32 | 32.5 | 32.7 | 1.46 |

Por clase (responde / d / niveles vivos):

| perdido | ruteadas a k | vivido | descripción | sustitución (responde / clase ok) |
|---|---|---|---|---|
| apple | 35 | 1.00 / 20.9 / 8.2 | 1.00 / 24.6 / 9.9 | 0.26 / 0 (responde tomato, pear) |
| car | 23 | 0.87 / 25.8 / 9.7 | 1.00 / 26.2 / 10.7 | 0 |
| cow | 31 | 1.00 / 20.7 / 7.9 | 1.00 / 21.8 / 8.7 | 0.26 / 0 (horse) |
| cup | 35 | 1.00 / 25.1 / 8.9 | 1.00 / 26.3 / 10.6 | 0 |
| dog | 23 | 1.00 / 25.4 / 9.5 | 1.00 / 24.7 / 9.8 | 0 |
| horse | 22 | 0.95 / 19.9 / 7.9 | 1.00 / 21.3 / 8.8 | 0.59 / 0 (cow, dog) |
| pear | 19 | 1.00 / 19.8 / 8.6 | 1.00 / 21.4 / 8.5 | 0.32 / 0 (apple) |
| tomato | 41 | 1.00 / 19.1 / 7.5 | 1.00 / 20.5 / 7.8 | 0.49 / 0 (apple) |

- La **sustitución confabula o calla**: cuando responde (24.5%) siempre es con la clase del sustituto (tomate por manzana, vaca por caballo), a 48 unidades de cualquier instancia de k. Cuando el directorio no da score a ningún sobreviviente (car, cup, dog) no responde.
- La **descripción conserva la clase siempre** (100% por los dos jueces) con una fidelidad apenas menor que la del especialista: 23.3 contra 21.9 (+6%), y una pista de identidad que deja 9.3 niveles vivos por coordenada contra 8.4 de la pista de texto en la memoria de contenido (+11%).
- **Ninguna respuesta depende de la pista, tampoco la del especialista.** La dispersión entre consultas distintas es igual a la dispersión entre sorteos de la misma consulta (32.3 contra 31.4 en vivido; 32.7 contra 32.5 en descripción), y F está cerca de 1 en las dos (1.64 y 1.46). "Manzana roja" y "manzana verde" producen la misma distribución de latentes en el especialista. Fig. 1 lo muestra: la respuesta vivida y la descrita son la misma envolvente borrosa del dominio.

### Imagen → texto (65 imágenes ruteadas a k)

| política | responde | alguna etiqueta del dominio perdido | etiquetas típicas |
|---|---|---|---|
| vivido (k presente) | 89.2% | 100% de las respondidas | apple: «red skin green», «fruit green pome» |
| sustitución | 0% | — | ningún sobreviviente reconoce la imagen |
| descripción | **100%** | **98.5%** | tomato: «soup sauce vegetable»; dog: «pet dog canine»; horse: «horse animal mane» |

Aquí la descripción responde más que el especialista (100% contra 89%) y acierta casi igual: la lectura inversa del directorio de texto es un vector de etiqueta de k y cae en su vocabulario. La sustitución no responde nunca, porque `evoke_labels` exige que la homo latente del sustituto contenga la imagen, y una imagen ajena nunca cabe.

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
3. **La descripción responde siempre y conserva la clase siempre**, con fidelidad 6% menor y una envolvente 11% más ancha que la del especialista. En imagen→texto responde más que el especialista.
4. **La tesis A, como se operacionalizó, no se sostiene**: el recall del especialista no depende de la pista dentro del dominio (F ≈ 1) y su fidelidad es casi la del testigo. La razón está en el llenado: las etiquetas de ConceptNet son del dominio, no de la imagen, y `stage5_fill` empareja cada etiqueta con una instancia arbitraria. La memoria de contenido nunca recibió pares etiqueta-instancia con correspondencia, así que solo puede devolver la envolvente del dominio (exp5: prototipo emergente; exp8: la memoria no contiene la figura, contiene el conjunto de las compatibles). Para reproducir, el especialista y el testigo saben lo mismo.
5. **La familiaridad se desplaza del reproducir al reconocer.** El especialista reconoce el 98% de las consultas de su dominio; el no-especialista el 16%; el directorio rutea el 56%. La diferencia entre familiaridad y descripción, en este sistema, es de cobertura del reconocimiento, no de fidelidad de la reproducción. Eso reformula a Russell sin abandonarlo: conocer por familiaridad es poder decir "esto es mío" ante lo nunca visto; conocer por descripción es poder decir "esto era de él" ante lo que se le vio.
6. Consecuencia para el TME: un miembro que sabe todo por descripción (la lectura inversa del directorio) puede sostener las respuestas del grupo cuando falta un especialista, con la misma clase y casi la misma fidelidad, pero no puede reconocer lo que el especialista no ganó delante de él.

## Archivos
- `results_text.csv`, `results_image.csv` — todas las respuestas (por consulta, política y sorteo) más una fila `ruteo` por clase
- `resumen.json` — las tablas de arriba
- `sonda_reconocimiento.json` — reconocimiento del especialista, del no-especialista y del directorio sobre el banco
- `fig1_respuestas.png` — por clase perdida: imagen real y la respuesta bajo cada política a la misma consulta
- `fig2_resumen_texto.png`, `fig3_resumen_imagen.png` — resúmenes por política

## Notas
- `run_experiment9_member_loss.py --text | --image | --report`; `run_experiment9_probe_recognition.py` para la sonda. No se modifica ninguna memoria ni etapa; `DirectoryMemory.recall_domain` es la lectura inversa declarada en esta corrida (antes vivía en el script de exp8).
- La fidelidad se mide en el espacio latente (distancia euclidiana a la instancia real más cercana). El juez clasificador es permisivo (exp8) y por eso no decide solo.
- Los recalls muestrean con el RNG global de numpy (semilla 42 al inicio de cada corrida).
