# Fase 3: prosa desactualizada, párrafo viejo y párrafo propuesto

**Fecha:** 21 de septiembre de 2026. Sobre el commit 5b6cda6.
**Regla:** nada de esto está aplicado. Cada entrada da el archivo y la línea, el texto actual, el texto propuesto y de dónde sale cada número. Apruebas, corriges o descartas; después se aplica.

Fuentes de las cifras nuevas: `results/experimento8/sondas.json` y `muestreo_resumen.json` (pista nan, semilla 42; 20 semillas), `results/experimento9/resumen.json` y `results_text.csv` (corrida única con nan, semilla y Bessel, commit bbde155), `results/experimento9/sonda_fase2.json`, `results/experimento10/results.csv`, `results/experimento11/`.

Lo que **no** está aquí porque depende de la fase 4: el marco teórico 2.4 y la sección 5 de `discusion_directorio_entropico.md`. De esos dos documentos solo se proponen las correcciones numéricas.

---

## A. `results/experimento8/README.md`

### A1. Tabla "Lo recuperado no es una copia" (líneas 30–43)

**Viejo:**

| clase | d(recuperado, instancia real más cercana) | d típica entre instancias vecinas | radio de la clase | dispersión entre sorteos |
|---|---|---|---|---|
| apple | 24.8 | 4.4 | 19.5 | 35.1 |
| car | 27.5 | 5.5 | 22.7 | 37.4 |
| cow | 22.0 | 5.1 | 16.2 | 31.1 |
| cup | 24.9 | 4.8 | 19.2 | 33.8 |
| dog | 24.8 | 6.6 | 22.3 | 33.7 |
| horse | 21.2 | 5.7 | 16.4 | 29.6 |
| pear | 21.3 | 5.9 | 17.4 | 29.5 |
| tomato | 20.5 | 2.9 | 14.5 | 28.3 |

Está entre tres y siete veces más lejos de cualquier instancia real de lo que las instancias están entre sí, y más lejos que el radio propio de la clase. Y la dispersión entre sorteos supera al radio: cada recall cae en un sitio distinto, más lejos entre sí que dos ejemplares reales cualesquiera.

**Nuevo:**

| clase | d(recuperado, instancia real más cercana) | d típica entre instancias vecinas | radio de la clase | dispersión entre sorteos | media de 20 semillas: d · dispersión |
|---|---|---|---|---|---|
| apple | 20.7 | 4.4 | 19.5 | 28.8 | 20.9 ± 0.6 · 30.1 |
| car | 22.2 | 5.5 | 22.7 | 30.5 | 23.1 ± 0.7 · 31.9 |
| cow | 16.9 | 5.1 | 16.2 | 24.4 | 16.5 ± 0.5 · 24.0 |
| cup | 22.4 | 4.8 | 19.2 | 31.1 | 22.9 ± 0.7 · 31.9 |
| dog | 19.3 | 6.6 | 22.3 | 28.1 | 20.1 ± 0.5 · 28.7 |
| horse | 16.9 | 5.7 | 16.4 | 24.6 | 16.7 ± 0.5 · 23.5 |
| pear | 18.1 | 5.9 | 17.4 | 25.9 | 17.5 ± 0.4 · 24.7 |
| tomato | 15.9 | 2.9 | 14.5 | 22.9 | 17.1 ± 0.4 · 24.7 |

Está entre 2.9 (dog) y 5.5 (tomato) veces más lejos de cualquier instancia real de lo que las instancias están entre sí, y en siete de ocho clases por encima del radio propio de la clase (en dog queda por debajo: 19.3 contra 22.3). La dispersión entre sorteos supera al radio en todas: cada recall cae en un sitio distinto, más lejos entre sí que dos ejemplares reales cualesquiera. Las cifras son de la pista de identidad con nan en los no ganadores y semilla fija (ver Notas); con ceros explícitos salían 3.6 a 7.1 veces, porque la cara «no ganó» de los otros siete agentes entraba en la columna de muestreo.

*Fuente:* `sondas.json` → `fidelidad`; `muestreo_resumen.json` → `nan.fidelidad`.

### A2. Tabla "Cuatro lecturas de la misma memoria" (líneas 63–72)

**Viejo (línea 72):** El one-hot y la cara positiva sola dan idéntico: las siete coordenadas en `0` no recortan un solo nivel. La cara negativa tiene toda la masa y ningún poder de restricción cuando acompaña a un positivo.

**Nuevo:** El one-hot y la cara positiva sola tienen el mismo soporte: las siete coordenadas en `0` no recortan un solo nivel. Pero sí cambian la masa de la columna que se muestrea: con ceros la columna es 6·N_all + 2·N_k (la cara «no ganó» de cada otro agente aporta toda la masa ajena), con nan es exactamente N_k (`sonda_pista_identidad.json`: TVD contra la distribución propia 0.235 en visión con ceros, 0 con nan; con ceros el 70% de la masa muestreada viene de otros agentes). Por eso todas las cifras de fidelidad, dispersión y capacidad de este README se miden con nan (`DirectoryMemory._identity_cue`, commit 65a7829). La cara negativa no restringe niveles cuando acompaña a un positivo; sí desplaza el sorteo.

*Fuente:* `sonda_pista_identidad.json`; CONTEXTO §6 fase 1.

### A3. Tabla de la cara negativa (líneas 76–81)

**Viejo:** «no ganó» | 0.602 – 0.630 | 0 de 8 | 0.93 – 0.95. […] El dominio propio aparece 1 de 160 sorteos (0.6%) contra 12.5% por azar.

**Nuevo:** «no ganó» | 0.595 – 0.645 | 0 de 8 | 0.94 – 0.97. […] El dominio propio aparece 4 de 160 sorteos (2.5%) con la semilla fija; otras semillas dan entre 1 y 5 de 160, siempre por debajo del 12.5% del azar.

*Fuente:* `sondas.json` → `caras`, `propio_en_cara_negativa`.

### A4. Fracción presenciada (líneas 95–106): agregar la curva

**Agregar después de la tabla:**

La transición es la probabilidad de haber presenciado al menos uno de los 128 broadcasts del agente: 1 − (1 − f)^128 da 0.63, 0.87, 0.98 y 1.00 para 1, 2, 4 y 8 broadcasts esperados; lo medido es 0.59, 0.89, 0.98 y 1.00. La curva de «responde» no mide nada de la memoria, mide el sorteo de qué se presenció. Lo que sí es de la memoria es que la precisión sea 1.00 desde el primer registro.

*Fuente:* `results_witnessed_fraction.csv` (columna `reconocido`, dominio ajeno).

### A5. Tabla de capacidad (líneas 108–124)

**Viejo:**

| registros por agente | niveles vivos | dispersión entre sorteos | d a instancia real | acierto |
|---|---|---|---|---|
| 1 | 1.00 | 0.0 | 3.3 | 80/80 |
| 2 | 1.58 | 8.0 | 7.4 | 80/80 |
| 4 | 2.61 | 14.9 | 12.0 | 80/80 |
| 8 | 4.09 | 21.4 | 15.9 | 80/80 |
| 16 | 6.02 | 26.7 | 19.0 | 80/80 |
| 32 | 7.53 | 28.6 | 20.6 | 80/80 |
| 64 | 8.64 | 30.2 | 21.6 | 80/80 |
| 128 | 9.63 | 32.7 | 23.2 | 80/80 |
| 256 | 10.43 | 34.5 | 24.5 | 80/80 |
| 512 | 11.04 | 36.0 | 25.5 | 80/80 |
| 800 | 11.34 | 36.4 | 25.8 | 79/80 |

Con un registro por agente la reconstrucción cae a 3.3 de una instancia real, con dispersión 0 […]. Con 800 —los que tiene la memoria de contenido de cada especialista— cae a 25.8. El acierto se sostiene en 80/80 hasta 512 registros y baja a 79/80 en 800: la clase aguanta casi hasta el final, lo que se pierde antes es la especificidad.

**Nuevo:**

| registros por agente | niveles vivos | dispersión entre sorteos | d a instancia real | d, media de 20 semillas | acierto (20 semillas) |
|---|---|---|---|---|---|
| 1 | 1.00 | 0.0 | 3.3 | 3.3 ± 0.00 | 80/80 en todas |
| 2 | 1.58 | 8.3 | 7.3 | 7.3 ± 0.06 | 80/80 |
| 4 | 2.61 | 15.4 | 12.1 | 12.1 ± 0.09 | 80/80 |
| 8 | 4.09 | 22.4 | 16.1 | 16.0 ± 0.12 | 80/80 |
| 16 | 6.02 | 26.1 | 18.5 | 18.4 ± 0.17 | 80/80 |
| 32 | 7.53 | 27.7 | 19.0 | 18.9 ± 0.23 | 80/80 |
| 64 | 8.64 | 28.2 | 19.6 | 19.3 ± 0.13 | 80/80 |
| 128 | 9.63 | 29.1 | 19.8 | 19.9 ± 0.17 | 80/80 |
| 256 | 10.43 | 29.2 | 20.1 | 20.2 ± 0.25 | 80/80 |
| 512 | 11.04 | 29.1 | 20.2 | 20.2 ± 0.24 | 80/80 |
| 800 | 11.34 | 29.5 | 20.5 | 20.0 ± 0.18 | 80/80 |

Con un registro por agente la reconstrucción cae a 3.3 de una instancia real, con dispersión 0: hay un solo valor admisible por coordenada y no queda nada que sortear. Con 800, los que tiene la memoria de contenido de cada especialista, cae a 20.5. La fidelidad se pierde entre 1 y 16 registros (3.3 → 18.5) y después se estabiliza: de 16 a 800 cambia 2 unidades. El acierto de clase es 80/80 en los once tamaños y en las 20 semillas; el 79/80 en N=800 de la corrida original con ceros no reapareció en 40 corridas (20 con nan, 20 con ceros; con ceros hubo un solo 79/80, en N=256 de una semilla).

*Fuente:* `sondas.json` → `capacidad`; `muestreo_resumen.json` → `nan.capacidad` y `ceros.capacidad`.

### A6. Hallazgos 2 y 7 (líneas 128 y 133)

**Viejo (2):** […] correctamente ubicado (1-NN y centroide dan la clase pedida siempre) y a la vez fuera de la nube de instancias reales.

**Nuevo (2):** […] correctamente ubicado (1-NN y centroide dan la clase pedida siempre) y a la vez fuera de la nube de instancias reales: de 2.9 a 5.5 veces la distancia típica entre instancias, por encima del radio de clase en siete de ocho.

**Viejo (7):** Cobertura y especificidad tiran para lados opuestos: más registros hacen que conteste siempre pero ensanchan la envolvente, y de 8 a 800 registros la reconstrucción pierde 10 unidades de fidelidad sin ganar nada en cobertura, y en 800 aparece el primer fallo de clase (79/80). El óptimo está en 4 a 8 percepciones ajenas presenciadas. El límite no son los datos: la pista de identidad no selecciona nada dentro del dominio, así que cada registro nuevo solo agrega varianza.

**Nuevo (7):** Cobertura y especificidad tiran para lados opuestos: más registros hacen que conteste siempre pero ensanchan la envolvente. De 8 a 800 registros la reconstrucción pierde 4 unidades de fidelidad (16.1 → 20.5) sin ganar nada en cobertura, y la clase no falla en ninguna semilla. El óptimo de fidelidad está en 4 a 8 percepciones ajenas presenciadas, pero es un óptimo de reconstrucción, no de ruteo: con esos mismos 4 a 8 registros el directorio no rutea las consultas de ese agente. Exp10 lo mide con ruteo directo (sin encadenar) según los broadcasts presenciados de cada otro agente:

| presenciados de 128 | ruteo directo, imagen (test) | ruteo directo, texto (reservadas) |
|---|---|---|
| 2 | 10.2% | 27.4% |
| 4 | 10.2% | 34.1% |
| 8 | 10.4% | 43.4% |
| 16 | 12.9% | 64.6% |
| 32 | 32.4% | 82.2% |
| 64 | 62.1% | 92.0% |
| 128 | 81.9% | 93.6% |

Para reconstruir bastan 4 a 8; para rutear directo hacen falta 64 a 128, o encadenar. El límite no son los datos: la pista de identidad no selecciona nada dentro del dominio, así que cada registro nuevo solo agrega varianza.

*Fuente:* `results/experimento10/results.csv` (modelo azar, protocolo directo; f × 128).

### A7. Notas (línea 149)

**Viejo:** Los recalls muestrean con el RNG global de numpy. Las figuras fijan la semilla; sin eso cada corrida devuelve un sorteo distinto, que es justamente lo que muestra `fig3_sorteos.png`.

**Nuevo:** Los recalls muestrean con `random` de Python, no con numpy (`hetero_lib/hetero_associative_4d.py:538`, `choose`). Las figuras y sondas siembran `random` y `numpy` juntos (semilla 42); antes solo se sembraba numpy y ningún sorteo era reproducible. Sin semilla cada corrida devuelve un sorteo distinto, que es justamente lo que muestra `fig3_sorteos.png`. El barrido de fracción presenciada no se regeneró: su métrica `reconocido` depende solo del soporte y no cambia con la pista ni con la semilla.

### A8. Nota nueva: cuantización del pool

**Agregar en Notas:** La curva de capacidad reconstruye memorias desde `instance_latents_*.json`. La etapa 5 cuantizó esos latentes en float32; releerlos en float64 cambia un nivel en un latente de car, cow y dog (600 celdas de 9.8 millones por memoria). Para reproducir bit a bit las memorias oficiales hay que cuantizar en float32 (`run_experiment11_monolithic.load_pool`). El efecto sobre esta curva es una coordenada de un latente y no se re-corrió.

---

## B. `results/experimento9/README.md`

### B1. Tabla texto → imagen (líneas 29–35)

**Viejo:**

| política | responde | clase perdida (clf · vecino) | d a instancia real de k | niveles vivos / coord. | disp. misma consulta | disp. consultas distintas | F |
|---|---|---|---|---|---|---|---|
| vivido (k presente) | 98.3% | 100% · 100% | **21.9** | **8.41** / 32 | 31.4 | 32.3 | 1.64 |
| sustitución | 24.5% | 0% · 0% | 48.3 (21.5 a su propia clase) | 7.98 | 30.5 | 34.4 | 2.89 |
| descripción | **100%** | 100% · 100% | 23.3 | 9.31 / 32 | 32.5 | 32.7 | 1.46 |

**Nuevo:**

| política | responde | clase perdida (clf · vecino) | d a instancia real de k | niveles vivos / coord. | disp. misma consulta | disp. consultas distintas | F (Bessel) |
|---|---|---|---|---|---|---|---|
| vivido (k presente) | 98.3% | 100% · 100% | 21.9 | **8.41** / 32 | 31.3 | 32.3 | 1.14 |
| sustitución | 24.5% | 0% · 0% | 48.0 (21.0 a su propia clase) | 7.98 | 30.1 | 33.5 | 2.08 |
| descripción | **100%** | 100% · 100% | **19.3** | 9.31 / 32 | 27.4 | 27.7 | 1.00 |

Corrida única con pista nan, semilla fija (`random` y `numpy`) y F con corrección de Bessel (commit bbde155). Con 20 semillas la descripción da 19.30 ± 0.13 y el vivido 22.03 ± 0.21 (`muestreo_resumen.json`).

### B2. Tabla por clase (líneas 37–48)

**Nuevo (vivido | descripción: responde / d / niveles vivos; sustitución: responde / clase ok):**

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

*Fuente:* `results_text.csv`.

### B3. Viñeta de la descripción (línea 51)

**Viejo:** La **descripción conserva la clase siempre** (100% por los dos jueces) con una fidelidad apenas menor que la del especialista: 23.3 contra 21.9 (+6%), y una pista de identidad que deja 9.3 niveles vivos por coordenada contra 8.4 de la pista de texto en la memoria de contenido (+11%).

**Nuevo:** La **descripción conserva la clase siempre** (100% por los dos jueces) y cae más cerca de las instancias reales que el especialista: 19.3 contra 21.9 (12% menos), en siete de ocho clases (apple empata: 21.0 contra 21.2). Lo hace con una pista de identidad que deja 9.3 niveles vivos por coordenada contra 8.4 de la pista de texto en la memoria de contenido (11% más). Una proyección más ancha que cae más cerca se explica por lo que cada memoria guarda (`sonda_fase2.json`): el directorio visual registró unas 122 imágenes reales sin aumentación por agente; la memoria de contenido, 800 latentes con aumentación emparejados con etiquetas sin correspondencia (`stage5_fill` registra `label_seq[i % L]` con `z_q[i]`, cada etiqueta con 38 instancias distintas en promedio). Condicionar la memoria de contenido por etiqueta recorta niveles (8.28) y aun así dispersa más (32.1 contra 27.4).

### B4. Viñeta de la dependencia de la pista (línea 53)

**Viejo:** **Ninguna respuesta depende de la pista, tampoco la del especialista.** La dispersión entre consultas distintas es igual a la dispersión entre sorteos de la misma consulta (32.3 contra 31.4 en vivido; 32.7 contra 32.5 en descripción), y F está cerca de 1 en las dos (1.64 y 1.46).

**Nuevo:** **La descripción no depende de la pista; el especialista, apenas.** La dispersión entre consultas distintas es casi la dispersión entre sorteos de la misma consulta (32.3 contra 31.3 en vivido; 27.7 contra 27.4 en descripción). La razón F con corrección de Bessel da 1.14 en vivido y 1.00 en descripción; bajo el nulo de independencia el F simulado es 1.00 (p5 0.98, p95 1.03), así que el vivido muestra una dependencia débil pero real y la descripción ninguna. Sin Bessel el nulo daba 1.44 y los valores publicados antes (1.64 y 1.46) eran ese sesgo.

### B5. Tabla imagen → texto (líneas 57–61)

**Viejo:** descripción | **100%** | **98.5%** | […]

**Nuevo:** descripción | **100%** | **100%** | […]. Y en el párrafo siguiente: «acierta igual» en vez de «acierta casi igual». (Corrida única con semilla; el 98.5% era de una corrida sin semilla.)

### B6. Hallazgos 3, 4, 5 y 6 (líneas 78–83)

**Viejo (3):** […] con fidelidad 6% menor y una envolvente 11% más ancha que la del especialista.
**Nuevo (3):** […] con fidelidad 12% mayor y una envolvente 11% más ancha que la del especialista.

**Viejo (4):** […] el recall del especialista no depende de la pista dentro del dominio (F ≈ 1) y su fidelidad es casi la del testigo. […]
**Nuevo (4):** […] el recall del especialista depende poco de la pista dentro del dominio (F 1.14 contra 1.00 del nulo) y su fidelidad es menor que la del testigo (21.9 contra 19.3). La razón está en el llenado: […] (el resto igual) […] Para reproducir, el testigo sabe incluso algo más compacto que el especialista, porque su envolvente está hecha de imágenes reales sin aumentación.

**Viejo (5):** […] La diferencia entre familiaridad y descripción, en este sistema, es de cobertura del reconocimiento, no de fidelidad de la reproducción.
**Nuevo (5):** […] La diferencia entre familiaridad y descripción, en este sistema, es de cobertura del reconocimiento, no de fidelidad de la reproducción. El reconocimiento tiene además una puerta que la descripción no tiene: los cuatro fallos del especialista (car 3, horse 1) son contención por coordenada, cada pista tiene de 12 a 76 coordenadas de etiqueta cuyo valor cuantizado el agente nunca registró, y coinciden exactamente con los ceros de su homo izquierda. La lectura inversa del directorio no pasa por esa puerta.

**Viejo (6):** […] con la misma clase y casi la misma fidelidad, pero […]
**Nuevo (6):** […] con la misma clase y mejor fidelidad, pero […]

### B7. Notas (línea 94)

**Viejo:** Los recalls muestrean con el RNG global de numpy (semilla 42 al inicio de cada corrida).
**Nuevo:** Los recalls muestrean con `random` de Python (`hetero_lib`); la corrida siembra `random` y `numpy` con 42 al inicio. Las corridas anteriores a bbde155 solo sembraban numpy y no eran reproducibles.

---

## C. `results/experimento10/README.md`

### C1. Párrafo del agregado (línea 63)

**Viejo:** En texto el agregado sí alcanza al pizarrón: 91–92% en reservadas desde f=1/32 (pizarrón 93.6), y 94.3% con f=1/4, por encima del pizarrón.

**Nuevo:** En texto el agregado sí alcanza al pizarrón: 91–92% en reservadas desde f=1/32 (pizarrón 93.6) y 94.3% con f=1/4. Esa última cifra no es una superación: la diferencia con el pizarrón son cuatro consultas de 171 en una de las tres semillas; es igualación dentro del ruido.

### C2. Hallazgo 2 (línea 78)

**Viejo:** […] el agregado […] alcanza al pizarrón desde f=1/32 en reservadas (91.0 contra 93.6) y lo supera con f=1/4 (94.3).
**Nuevo:** […] el agregado […] alcanza al pizarrón desde f=1/32 en reservadas (91.0 contra 93.6) y lo iguala con f=1/4 (94.3 contra 93.6, cuatro consultas en una semilla).

---

## D. `results/experimento7/README.md`

### D1. Hallazgo 2 (línea 49) y cierre (línea 53)

**Viejo (49):** La query emparejada es el punto débil del unificado: el veto conjuntivo corre sobre TODAS las features definidas del cue, así que una mitad imagen sin soporte suficiente tumba la pista entera aunque la mitad texto rutee sola al 96.2% — emparejada 25.0% contra 97.5% de la fusión de dos directorios, donde cada modalidad se rechaza por separado.

**Nuevo (49):** La query emparejada es el punto débil del unificado, y el 25.0% no es una cifra del veto sino de la cobertura de la mitad de imagen: en el mismo directorio C, la consulta solo-imagen acierta 26.9% y rechaza 73.1%, y la emparejada acierta 25.0% y rechaza 75.0%. El veto conjuntivo corre sobre todas las features definidas del cue, así que la consulta plena hereda el rechazo de su mitad de imagen aunque la mitad de texto rutee sola al 96.2%. La fusión de dos directorios, donde cada modalidad se rechaza por separado, da 97.5%.

**Viejo (53):** En suma: bajo esta proyección el directorio unificado no puede transferir nada entre modalidades y sí paga el veto conjuntivo en queries plenas y el denominador compartido.
**Nuevo (53):** En suma: bajo esta proyección el directorio unificado no puede transferir nada entre modalidades y sí paga dos costos: en queries plenas hereda por el veto conjuntivo el rechazo de la modalidad menos cubierta, y el denominador compartido degrada el texto.

---

## E. `discusion_marco_teorico_directorio.md` (solo cifras; lo conceptual espera a la fase 4)

### E1. Sección 2.2 (línea 29)

**Viejo:** […] a la vez fuera de la nube de instancias reales (3 a 7 veces más lejos de cualquier instancia de lo que las instancias están entre sí).
**Nuevo:** […] a la vez fuera de la nube de instancias reales (2.9 a 5.5 veces más lejos de cualquier instancia de lo que las instancias están entre sí, medido con la pista de identidad corregida).

### E2. Sección 4.1 (líneas 98–107)

**Viejo (100):** […] a 23.3 de la instancia real más cercana contra 21.9 del especialista (+6%), con 9.3 niveles vivos por coordenada contra 8.4 (+11%). Etiquetas evocadas desde una imagen: 98.5% en el vocabulario del dominio perdido, contra 100% del especialista, que sin embargo responde menos (89% contra 100%).
**Nuevo (100):** […] a 19.3 de la instancia real más cercana contra 21.9 del especialista (12% más cerca), con 9.3 niveles vivos por coordenada contra 8.4 (11% más). Etiquetas evocadas desde una imagen: 100% en el vocabulario del dominio perdido, igual que el especialista, que sin embargo responde menos (89% contra 100%).

**Viejo (101):** **Ninguna respuesta depende de la pista, tampoco la del especialista.** La dispersión entre consultas distintas iguala a la dispersión entre sorteos de la misma consulta (32.3 contra 31.4), y la razón F está cerca de 1 (1.64 vivido, 1.46 descripción).
**Nuevo (101):** **La descripción no depende de la pista; el especialista, apenas.** La dispersión entre consultas distintas casi iguala a la dispersión entre sorteos de la misma consulta (32.3 contra 31.3), y la razón F con corrección de Bessel da 1.14 en el especialista y 1.00 en la descripción, contra 1.00 del nulo.

**Viejo (103):** La predicción central de la tesis A era que la descripción se distinguiría de la familiaridad en fidelidad y en dependencia de la pista. No se distingue en ninguna de las dos de manera apreciable.
**Nuevo (103):** La predicción central de la tesis A era que la descripción se distinguiría de la familiaridad por menor fidelidad y por no depender de la pista. Se distingue en la dirección contraria en fidelidad (es mejor) y apenas en dependencia de la pista.

**Viejo (107):** […] con la misma clase y casi la misma fidelidad.
**Nuevo (107):** […] con la misma clase y mejor fidelidad.

### E3. Sección 4.2 (línea 114)

**Viejo:** […] y 94.3% con f=1/4, por encima del pizarrón.
**Nuevo:** […] y 94.3% con f=1/4, que iguala al pizarrón dentro del ruido (cuatro consultas en una semilla).

### E4. Sección 4.3, tabla y punto 3 (líneas 125 y 131)

**Viejo (125):** **Parcialmente refutada.** Misma clase (100%), fidelidad casi igual (+6%), y *ninguna* de las dos depende de la pista.
**Nuevo (125):** **Refutada en su forma original.** Misma clase (100%), fidelidad mejor en la descripción (19.3 contra 21.9), y la dependencia de la pista es nula en la descripción y débil en el especialista (F 1.00 contra 1.14).

**Viejo (131):** […] un miembro que sabe todo por descripción puede sostener respuestas, no reconocimientos.
**Nuevo (131):** sin cambio de texto; solo verificar que «casi la misma fidelidad» no aparezca en el párrafo (aparece en 4.1, corregido arriba).

---

## F. `README.md` (principal, en inglés)

### F1. Bloque nuevo después de "What changed in v5" (línea 74)

```
### Experiment 11 (monolithic EHAM baseline)

- **The control the thesis lacked**: one EHAM (hetero + two homo) holding all 8
  classes, filled with the same 6400 (label, latent) pairs the eight specialists
  receive, evaluated with the same operations (`recognize_gated`,
  `recall_from_left`, `recall_from_right`). Three arms: M (single memory),
  T-oracle (specialists, ground-truth routing) and T-protocol (official v5).
  Cuts N ∈ {25, 50, 100, 200}, 10 seeds, 3 draws, 171 held-out queries.
- **Class accuracy ties**: M 97.4% vs T-protocol 97.5% (1-NN judge) at N=200;
  T-protocol wins only at N=25 (98.5 vs 95.9).
- **Fidelity does not**: distance of the recalled latent to the nearest real
  instance is 26.7 for M vs 22.8 (protocol) / 22.2 (oracle), and the gap grows
  with N (2.0 → 4.5). Mixing happens per coordinate, not per word.
- **Chimeras where predicted**: with a shared first cue (`fruit`, `animal`,
  `mammal`, `red`, `pome`, `table`) M gets the class right 44% of the time
  with 73% of the coordinates from one class; specialists 100% / 100%.
- **Image → text**: M covers more (93% strict hit vs 78.5% oracle) because the
  union support contains 96% of test latents where a specialist contains 79%,
  but answers with another class's domain 8× more often (8.0% vs 1.0%).
- **Price of the directory**: 2.5 points below the oracle at every N.
- Verdict against the pre-registered criterion (`propuesta_fase5_mae_monolitica.md` §8):
  not refuted. Partitioning buys fidelity, coherence and precision; it costs
  coverage, an index and 8× the cells. Full tables: `results/experimento11/`.
```

### F2. Tabla "Key Results — v4" (líneas 83–95): fila nueva

```
| Single-EHAM baseline (exp11, N=200) | class 97.4 / d_nn 26.7 | vs T-protocol 97.5 / 22.8 |
```

### F3. Sección de reproducibilidad (líneas ~205–215): nota nueva

```
- **Quantization dtype**: stage 5 quantizes latents in float32 (encoder output
  and float32 stats). Re-quantizing `instance_latents_*.json` in float64 flips
  one level in one latent of car, cow and dog, so the memories stop being
  bit-identical to `models/`. Scripts that rebuild memories from the pool must
  quantize in float32 (`run_experiment11_monolithic.load_pool`).
- **Sampling RNG**: `hetero_lib` samples with Python's `random`, not numpy.
  Seed both (`random.seed`, `np.random.seed`) for reproducible draws.
```

---

## G. `CONTEXTO_SEP2026.md`

### G1. Sección nueva 9 (antes de "Pendiente")

```
## 9. Fases 4 y 5 (20 y 21 de septiembre)

- Fase 4: material en `revision_fase4_directorio_entropico_vs_metamemoria.md`. La
  contradicción es real y acotada: `recall_domain` sí llama a `recall`
  (`recall_from_right` → `sample_n_search_recall` → `choose`, `random.random()`),
  pero ningún camino del protocolo lo usa. σ sigue sin importar porque el
  muestreo por defecto no lo usa. Tres salidas; decisión pendiente.
- Fase 5: diseño en `propuesta_fase5_mae_monolitica.md`, implementación
  `run_experiment11_monolithic.py`, resultados y `veredicto.md` en
  `results/experimento11/`. Tres brazos (M, T-oráculo, T-protocolo), cortes
  {25, 50, 100, 200}, 10 semillas, 3 sorteos, 171 reservadas. Control: los
  especialistas reconstruidos en float32 son bit a bit los `agent_*.pkl`.
  No refutada por el criterio pre-registrado (clase empata en 0.1 puntos,
  fidelidad difiere en 3.9). La partición compra fidelidad (brecha 2.0 → 4.5
  con N), coherencia con pista compartida (M 44% de clase, compat 0.73) y
  precisión en imagen→texto (dominio ajeno 8% contra 1%); cuesta cobertura
  (79% contra 96% en imagen), 2.5 puntos de directorio y 8× las celdas.
- Infraestructura: cache de memorias por corte (`cache/exp11/`, 1.5 GB cada
  uno; el registro de hetero_lib cuesta 80 ms), relaciones en memoria
  compartida entre procesos, trabajos por trozos, `--image-only`, `--ood-only`.
- Hallazgo de reproducibilidad: la etapa 5 cuantizó en float32; en float64
  cambia un nivel en un latente de car, cow y dog.
- Deck mínimo: `hallazgos_exp7_a_exp11.pptx`.
```

### G2. Sección 8 "Pendiente": reemplazar por

```
- Fase 3: aplicar `revision_fase3_prosa.md` una vez aprobado.
- Fase 4: decidir entre las tres salidas.
- Exp11: banco fuera de dominio de ~40 consultas (`--ood-only --ood-file`);
  imagen→texto con los cuatro cortes si se quiere la versión larga.
- Experimento de solapamiento: los tres brazos de exp11 con pares de clases
  elegidos por distancia entre centroides.
- Restaurar los modelos v5 en `models/` cuando cierren las fases de arreglos.
- App: migrar la fase temprana en vivo a directorios perspectivales.
```

---

## H. `.tex8` (reporte)

Tres párrafos para que los coloques donde corresponda; el reporte no tiene hoy ninguna línea base contra una memoria única.

**Resultados:**

```latex
\paragraph{Línea base: una sola EHAM con las ocho clases.}
Para medir qué aporta la partición en especialistas, se construyó una
EHAM única (hetero y dos homo) con los mismos 6400 pares etiqueta--latente
que reciben los ocho especialistas y se evaluó con las mismas operaciones
(\texttt{recognize\_gated}, \texttt{recall\_from\_left}), sin ruteo. Sobre las
171 consultas reservadas y diez semillas, la EHAM única acierta la clase el
97.4\,\% (juez: vecino real más cercano) frente al 97.5\,\% del protocolo
transactivo y al 100\,\% del oráculo (especialista elegido por la verdad de
terreno); pero su respuesta cae a 26.7 de la instancia real más cercana
frente a 22.8 y 22.2, y la brecha crece con el contenido (2.0 con 100
registros por clase, 4.5 con 800). Cuando la primera pista reconocida es una
etiqueta compartida entre clases (\emph{fruit}, \emph{animal}, \emph{red}),
la EHAM única acierta la clase el 44\,\% y su patrón mezcla clases (73\,\% de
las coordenadas de una sola clase); los especialistas, 100\,\%. En
imagen\,$\to$\,texto la EHAM única responde al 96\,\% de las imágenes de test
frente al 79\,\% del especialista, y responde con un dominio ajeno el 8\,\%
frente al 1\,\%.
```

**Discusión:**

```latex
La comparación con la EHAM única acota lo que la maquinaria transactiva
aporta. No es exactitud: sobre el banco completo ambas clasifican igual. Es
fidelidad, coherencia y precisión: la relación de una EHAM acumula por
coordenada y valor, y dos conceptos distintos comparten valores cuantizados
en muchas coordenadas, así que una memoria con varios dominios mezcla al
recordar aunque las palabras difieran. Partir el contenido evita la mezcla
porque la decisión de dominio ocurre antes del recall, en el directorio, y
no dentro del sorteo. El precio es cobertura: el containment de un
especialista es estricto en las 64 coordenadas del latente y deja fuera al
21\,\% de las imágenes de prueba, que la unión de soportes contiene; es el
rechazo residual del hemisferio visual, ahora identificado como costo de la
partición. A eso se suman 2.5 puntos del directorio y ocho veces las celdas.
```

**Conclusiones, "Respuesta a la pregunta de investigación", frase final:**

```latex
Frente a una EHAM única con el mismo contenido, el sistema transactivo no
clasifica mejor; recuerda con más fidelidad, no mezcla dominios cuando la
pista es compartida y se equivoca de dominio ocho veces menos, a cambio de
cubrir menos y de pagar un índice.
```

---

## I. Deck externo (Drive, no está en el repo)

«3.6 a 7.1 veces» → «2.9 a 5.5 veces». Si el deck también cita 23.3 contra 21.9 o el 98.5 % de imagen→texto, aplican B3 y B5.

---

## J. Lo que no se toca

- `results/experimento8/README.md` líneas 12–28 (las tres condiciones, controles): sin cambio; `sondas.json` regenerado da 80/80, 80/80, 112/112.
- Las tablas de exp10 y sus hallazgos 1, 3–7: sin cambio.
- `discusion_directorio_entropico.md`: espera a la fase 4.
