# Experimento 16: propuesta de diseño para la partición leave-object-out

**Fecha:** 24 de septiembre de 2026
**Estado:** propuesta aprobada en el chat (10 pliegues, una semilla). Decisiones fijadas aquí antes de correr.

## 1. Qué falta

ETH-80 tiene 10 objetos físicos por clase y 41 vistas de cada uno. El split oficial es por imagen, así que los diez objetos de cada clase aparecen en el llenado y en el test (hallazgo M4 de la auditoría). Todas las cifras visuales del reporte (96.2 % de ruteo, 97.4 % de evocación, exp8, exp13) miden generalización a **vistas nuevas de objetos conocidos**. La tesis afirma que el sistema reconoce el dominio de una imagen; para eso el objeto no puede estar en el llenado. Exp8 mostró que la memoria guarda una envolvente por coordenada y no ejemplares; la pregunta es si esa envolvente cubre un objeto que nunca contribuyó a ella.

## 2. Pregunta

**¿Cuánto del reconocimiento visual sobrevive cuando el objeto de la imagen nunca entró al llenado ni a la fase A, y cuánto de la cifra oficial es memorización de los diez objetos?**

## 3. Diseño

Validación cruzada leave-one-object-out, 10 pliegues. En el pliegue $k$ se reserva el objeto $k$ de **cada** clase (8 objetos, 328 imágenes) y el sistema se construye solo con los otros nueve:

- **Pool del pliegue:** las 369 vistas de los 9 objetos restantes de cada clase, barajadas con semilla fija (`RandomState(1000 + k)`), independiente del split oficial.
- **Contenido:** las primeras 200 del pool, con las 16 variantes oficiales (`augment_variants`), 3200 registros por agente, cuantización con los stats oficiales (`latent_global_stats.json`, sin recalcular) y etiquetas por `build_label_sequence`. Es el protocolo de la etapa 5 con otro conjunto de imágenes.
- **Fase A:** las siguientes 128 del pool, con 16 variantes por percepción, ganador por `recognize_gated_right` con la original, umbral de energía, registro por entrada + ganador + TME (`register_transaction`), semilla 42 para la entrada. Es la etapa 7 con otro conjunto.
- **Banco «objeto nuevo»:** las 41 vistas del objeto reservado de cada clase (328).
- **Banco «objeto conocido»:** las 41 vistas restantes del pool (posiciones 328–368) de cada clase (328): vistas nuevas de objetos que sí contribuyeron. Es el control interno: mismos modelos, misma cantidad, misma semilla; la única diferencia es si el objeto se conocía.
- **Ruteo:** `route_transactive` desde una entrada no especialista (`CLASSES[(ci+1) % 8]`), ξ = 0, con el umbral de energía; «responde» con una proyección de la hetero (`hetero_recognizes`, verificado en exp13); evocación completa (`evoke_labels`, 17 s por imagen) sobre 3 imágenes de objeto nuevo por clase y pliegue (240 en total).

Una semilla por pliegue: la variación que importa es entre objetos. Costo: 10 llenados de 25 600 registros (~35 min cada uno), 2 procesos, ~3.5 h; reanudable por pliegue.

## 4. Métricas

Por pliegue, clase y banco: contenido acepta (especialista propio), responde, directorio acepta, ruteo correcto, falso ruteo, rechazo, punta a punta (ruteo correcto y responde), y sobre la muestra evocada el acierto estricto y el dominio ajeno. Agregado: media y bootstrap sobre los 10 pliegues; por clase, la media sobre pliegues. **Brecha de memorización** = objeto conocido − objeto nuevo, por medida.

## 5. Predicciones

- P1. El contenido acepta menos objetos nuevos que vistas nuevas de objetos conocidos, y la brecha es mayor en las clases con más variación de forma entre objetos (cow, horse, dog, car) que en las de forma uniforme (apple, tomato, pear, cup).
- P2. Los falsos ruteos suben con objetos nuevos y se concentran en pares vecinos (horse ↔ cow ↔ dog; apple ↔ tomato ↔ pear), no en cruces arbitrarios.
- P3. El directorio sigue al contenido: donde el objeto nuevo cae dentro de la envolvente, el directorio lo rutea; el rechazo es la salida dominante para lo que no cabe, no el ruteo equivocado.
- P4. La brecha de memorización es positiva en las ocho clases, pero la cobertura de objeto nuevo queda por encima de la mitad de la de objeto conocido: la envolvente por coordenada generaliza en parte porque las vistas de objetos distintos comparten valores en la mayoría de las 64 coordenadas.

## 6. Criterio

La afirmación «el sistema reconoce el dominio de un objeto nuevo» queda **sostenida** si la cobertura de punta a punta sobre objetos nuevos es al menos el 75 % de la de objetos conocidos en el mismo pliegue y los falsos ruteos sobre objetos nuevos no superan el 2 %. Queda **refutada** si cae por debajo de la mitad o los falsos superan el 5 %. Entre medias se reporta la cifra y el reporte la adopta como la de generalización, con la brecha explícita.

## 7. Entregables

`run_experiment16_leave_object_out.py` (caché de latentes en `.npy` fuera de git, un archivo `raw/` por pliegue, `--workers`, `--report-only`), `results/experimento16/{README.md, resumen.json, raw/, fig1_nuevo_vs_conocido.png, veredicto.md}` y la prosa viejo/nuevo para la limitación (b) del `.tex8` («generalización a vistas nuevas de objetos conocidos»), la metodología (§4, que declara que no se impone leave-object-out) y las conclusiones.
