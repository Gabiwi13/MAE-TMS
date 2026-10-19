# Olvido exacto y privacidad de la MAE

Dos propiedades que no son de exactitud: ¿la MAE puede olvidar un registro como si nunca lo hubiera registrado? ¿Cuánto revela de un registro individual? Diseño, predicciones y criterio fijados antes de correr en [`propuesta_olvido_y_flota.md`](../../propuesta_olvido_y_flota.md) (parte A). Script: [`run_olvido_privacidad.py`](../../run_olvido_privacidad.py). Detalle en `resumen.txt` y `resultados.json`.

**Resultado en una línea:** olvidar es exacto. Restar la relación que sumó el registro deja el contenido y los directorios celda por celda iguales a reconstruir sin ese registro, y lo hace unas 300 veces más rápido. Hay una sola excepción, esperada: la fase A depende del camino, y al reconstruir 1 de 2160 percepciones cambia de destino. En privacidad, la MAE no revela pertenencia más que una media: AUROC del ataque de 0.47 a 0.53, contra 1.00 de kNN, que guarda los ejemplares.

## Olvidar

La MAE oficial no tiene una operación para olvidar. Se definió **olvidar = restar la relación que sumó el registro**, la inversa de `abstract`, válida mientras ningún conteo llegue al tope de 2¹⁶ − 1 (aquí el máximo es 4320). Datos: nivel 1 industrial (12 piezas, protocolo `Level`, ResNet18 + PCA64).

**Verificación previa:** la fase A con registro de transacciones que uso da exactamente los mismos directorios y el mismo contenido que `Level._phase_a` oficial (0 celdas distintas, misma formación). Construir dos veces da 0 diferencias.

| prueba | qué se olvida | contra qué | resultado |
|---|---|---|---|
| A1a, contenido | 27 imágenes por pieza (10 %, 5184 registros con variantes) | reconstruir sin ellas, con la misma cuantización y las mismas entradas | **contenido: 0 celdas distintas**. Fase A: 1 de 2160 percepciones con otro destino (15 627 celdas de directorio distintas, todas de esa transacción: cada registro toca 64 × 12 celdas). **Test: 0 de 2162 decisiones distintas** |
| A1b, transacciones | 213 de 2133 percepciones de fase A (10 %) | rehacer la fase A sin ellas, con las mismas entradas | **directorios: 0 celdas distintas; test: 0 decisiones distintas**. Olvidarlas cambió 13 decisiones respecto de antes de olvidar |

Tiempo: olvidar 0.09 s (A1a) y 2.7 s (A1b), contra 30 s de reconstruir. Reentrenar una cabeza logística con los mismos latentes cuesta 0.3 s, así que la ventaja de velocidad cuenta frente a reconstruir la memoria o a reentrenar un encoder, no frente a un clasificador lineal.

**La dependencia del camino es real pero chica.** El contenido es una suma y no depende del orden. Los directorios sí dependen del orden: guardan transacciones cuyo ganador se decidió con el contenido de ese momento. Olvidar contenido no rehace esas decisiones; la diferencia fue 1 percepción de 2160 y ninguna decisión de test.

kNN (borrar la fila) y NCM (restar de la suma) también olvidan exactamente, por construcción. El olvido exacto no distingue a la MAE de ellos; la distingue de los modelos entrenados por gradiente.

## Privacidad: ataque de pertenencia

Miembros: las imágenes de llenado. No miembros: imágenes de la misma distribución que no se registraron (fase A o calibración). El atacante tiene el latente del candidato y el estado guardado de cada método. AUROC: 0.5 significa que no distingue a los miembros. Celdas únicas: coordenadas de un miembro que caen en una celda que solo él ocupó, de modo que su valor queda atribuido a él.

| dominios | MAE | kNN | NCM | gaussiana | celdas únicas por miembro (miembros con alguna) |
|---|---|---|---|---|---|
| industrial, nivel 1 (12 piezas, 270/180) | **0.525** | 1.000 | 0.508 | 0.720 | 0.01 (1.1 %) |
| industrial, PCA por pieza (12, 270/180) | **0.465** | 1.000 | 0.449 | 0.449 | 0.03 (2.7 %) |
| médico, modalidad (4, 328/218) | **0.534** | 1.000 | 0.512 | 0.652 | 0.05 (4.1 %) |
| médico, órganos (11, 815/542) | **0.505** | 1.000 | 0.505 | 0.527 | 0.01 (0.2 %) |

- La MAE revela de un miembro lo mismo que la media de su dominio. Con más registros por agente (órganos, 815), queda en el azar.
- La gaussiana revela más que la MAE donde hay pocos registros por dimensión (270 en 64 dimensiones: 0.72). La covarianza se ajusta a los miembros.
- Con la PCA por pieza, todos los métodos de agregados quedan por debajo de 0.5. La PCA se ajustó con los miembros: capta toda su varianza en 64 dimensiones, y los no miembros proyectan con menos varianza, más cerca del centro. Es un efecto de la percepción, no de la memoria.
- Casi ningún miembro queda expuesto en alguna coordenada (de 0.2 a 4.1 %, en las colas).

Fuera de alcance, como se declaró: quien vea la memoria antes y después de un registro recupera los niveles de ese registro (la diferencia de conteos). Con NCM pasa lo mismo (la diferencia de sumas da el latente). El ataque es sobre el latente: no se probó reconstruir la imagen desde el latente.

## Predicciones y criterio

| | predicción | resultado |
|---|---|---|
| PA1 | A1a (contenido) y A1b: 0 diferencias. A1a (directorios): < 1 % de la fase A y del test cambian | **Se cumple**: 0 y 0. Fase A 1/2160 (0.05 %), test 0/2162 |
| PA2 | kNN ≥ 0.95. MAE de 0.50 a 0.65, cerca de NCM y de la gaussiana. Pocas celdas únicas | **Se cumple**: kNN 1.000; MAE de 0.47 a 0.53, a ≤ 0.03 de NCM. La gaussiana revela más que lo predicho en el nivel 1 (0.65–0.72) |

**Criterio «la MAE olvida exactamente»:** sostenido (0 diferencias en A1a contenido y en A1b). **Criterio «no guarda ejemplares en un sentido útil para la privacidad»:** sostenido (MAE 0.507 de media, NCM 0.494, kNN 1.000).

## Lectura

1. **Aprender es sumar, y olvidar es restar.** En la memoria de contenido, el olvido es exacto y barato. Esto vale para un paciente que retira su consentimiento o para un lote mal etiquetado en la planta: se resta y la memoria queda como si nunca lo hubiera visto, sin reentrenar nada.
2. **El directorio recuerda la historia.** Una transacción se olvida exactamente, pero si se olvida contenido, las decisiones que ese contenido tomó en el pasado no se rehacen solas. Aquí el efecto fue mínimo; en un sistema con más solapamiento entre dominios podría ser mayor.
3. **La MAE guarda un resumen, no un archivo.** Ante un ataque de pertenencia se comporta como una media por dominio, y mucho mejor que kNN, que guarda cada caso. Para un hospital es una diferencia práctica: el sistema puede rutear y abstenerse sin conservar ninguna imagen ni latente de paciente.
4. **Ninguna de las dos propiedades es exclusiva.** NCM olvida exactamente y revela lo mismo, y ocupa menos. Lo que tiene la MAE es la combinación con el ruteo con abstención y los directorios, que NCM no da.

## Notas

- La operación de olvido es nueva (no está en el código de Pineda). Se verificó contra la reconstrucción desde cero, no contra una referencia oficial.
- Para que la reconstrucción sea un contrafactual limpio, la cuantización y el umbral de energía se mantienen fijos (son parte de la percepción), y cada transacción conserva su entrada. Las percepciones que solo se registran en la reconstrucción sortean su entrada con otra semilla.
- Los latentes médicos se leyeron de `MAE-TMS-medico/results/medico_balanceado/cache`, sin escribir en esa carpeta.
- Una sola semilla.
