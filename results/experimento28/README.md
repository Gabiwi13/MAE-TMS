# Experimento 28: ¿más datos ayudan en cáncer de mama?

El diseño, las predicciones y el criterio están en `propuesta_exp28_curva_mama.md` y se fijaron antes de correr. Datos: BreastMNIST a 128 px (ultrasonido; 147 malignos y 399 benignos en train). El test es fijo: 42 malignos y 114 benignos. Se probaron fracciones de 25, 50, 75 y 100 % del train, cada una con 5 semillas.
- **Brazo A:** el encoder queda fijo (el de la corrida balanceada); solo cambia lo que se registra.
- **Brazo B:** el encoder se reentrena con la fracción, con el mismo número de pasos en todas.
- **Registro:** completo, o igualado (las dos clases con el tamaño de la más chica).

Script: `run_experiment28_curva_mama.py`, 142 s en total. Detalle en `resumen.txt` (media de 5 semillas, con mínimo y máximo), `resultados.json` y `filas.json`.

## Verificación

- **Memoria:** con el encoder y los pools en caché de la corrida balanceada, el nivel 2 de mama da 28/42 malignos y 109/114 benignos, y la cabeza 33/42. Es lo que reporta `medico_balanceado`. Los latentes de test recalculados coinciden con la caché (diferencia 0).
- **Encoder:** el reentrenado con la semilla 42 y el 100 % **no es idéntico** al de la caché (diferencia máxima de pesos 1.07). En `trained_level2` la red se crea antes de fijar la semilla, así que su inicialización no se puede reproducir. Por eso la cabeza del brazo B con la semilla 42 detecta 30/42 y no 33/42. Esa diferencia da una idea de cuánto varía el resultado de un entrenamiento a otro.

## Resultados (brazo B, registro completo: el sistema entero con más o menos datos)

| método | 25 % | 50 % | 75 % | 100 % |
|---|---|---|---|---|
| memoria, balanceado | 45.1 [38.7, 49.8] | 63.2 | 73.4 | **77.3** [74.8, 78.6] |
| prototipos, balanceado | 72.6 [69.2, 77.7] | 77.9 | 83.2 | **86.1** [83.4, 88.7] |
| kNN, balanceado | 72.7 | 78.0 | 84.0 [81.0, 87.5] | **86.3** [84.0, 88.3] |
| cabeza, balanceado | 72.6 | 77.5 | 84.8 | **85.1** [82.6, 88.3] |
| cabeza, AUROC | 0.854 | 0.884 | 0.915 | 0.923 |
| memoria, sensibilidad | 14.3 | 39.5 | 56.2 | **61.9** [57.1, 64.3] |
| prototipos, sensibilidad | 48.6 | 61.0 | 72.4 | **77.6** |
| cabeza, sensibilidad | 49.5 | 60.0 | 75.7 | **76.7** |
| memoria, especificidad | 76.0 | 86.8 | 90.5 | 92.6 |
| memoria, rechazo | 32.8 | 13.7 | 6.4 | 5.0 |

**Brazo A (encoder fijo):** los prototipos y kNN no cambian con la fracción (balanceado 85.5 → 85.4 y 85.3 → 84.8; AUROC de prototipos 0.937 en todas). La memoria sí cambia: 53.1 → 76.6 balanceado y 28.6 → 59.5 de sensibilidad, con el rechazo bajando de 26.8 a 4.2 %.

**Registro igualado, al 100 %:** la sensibilidad de la memoria sube y la especificidad baja.

| brazo | sensibilidad, completo → igualado | especificidad, completo → igualado |
|---|---|---|
| A | 59.5 → 69.0 | 93.7 → 84.2 |
| B | 61.9 → 71.9 | 92.6 → 79.6 |

Los métodos por distancia casi no cambian con el registro.

**Malignos que se escapan en silencio, a igual carga de revisión** (brazo B, 100 %, de 42; la revisión es la fracción que la memoria manda a un humano):

| registro | a revisión | memoria | cabeza con umbral | Mondrian |
|---|---|---|---|---|
| completo | 26.5 % | 5.0 | 3.6 | 3.2 |
| igualado | 30.1 % | 4.2 | 3.4 | 2.8 |

La carga de Mondrian quedó a menos de 3 casos de la de la memoria en todos los cortes (41.2 contra 41.4 casos al 100 %).

**Intervalos (semilla 42, 100 %, Wilson al 95 %)**, brazo B completo:
- memoria 26/42 [47, 75];
- prototipos 34/42 [67, 90];
- kNN 32/42 [61, 87];
- cabeza 30/42 [56, 83].

## Predicciones

| | predicción | resultado |
|---|---|---|
| P1 | En B, los métodos por distancia ganan ≥ 5 puntos balanceados del 25 al 100 %; en A, ≤ 3 | **Se cumple.** En B: prototipos +13.5, kNN +13.6, cabeza +12.5. En A: −0.1 y −0.5. El dato le sirve a la percepción, no al registro de esos métodos |
| P2 | Con registro completo, la sensibilidad de la memoria no sube (≤ +3); al 100 %, el igualado le gana al completo en ≥ 5 puntos de sensibilidad, a costa de especificidad | **La primera parte se refuta:** la sensibilidad sube mucho (A +30.9; B +47.6), porque con pocos datos la envolvente maligna no cubre y la memoria rechaza. **La segunda se cumple:** +9.5 (A) y +10.0 (B), con 9.5 y 13.0 puntos menos de especificidad |
| P3 | (incierta) La curva del mejor método no está saturada: la ganancia del 75 al 100 % supera el rango entre semillas | **No se cumple.** kNN gana +2.3 del 75 al 100 % y el rango al 100 % es de 4.3 puntos; los prototipos ganan +2.9 con rango 5.3, y la cabeza +0.3. La AUROC de la cabeza pasa de 0.915 a 0.923 |
| P4 | A igual carga de revisión, la memoria deja escapar en silencio igual o más malignos que la cabeza y Mondrian | **Se cumple.** 5.0 contra 3.6 y 3.2 (completo); 4.2 contra 3.4 y 2.8 (igualado) |
| P5 | Al 100 %, los intervalos de Wilson miden ≥ 25 puntos y se solapan | **Se cumple casi del todo.** Los anchos van de 26 a 28 puntos, salvo los prototipos del brazo B (23, por debajo del umbral). Los intervalos de la memoria, kNN y la cabeza se solapan: memoria [47, 75], kNN [61, 87], cabeza [56, 83] |

## Criterio

- **«Más datos del mismo tipo ayudan»: no sostenido, pero tampoco refutado.**
  - La primera condición se cumple: el mejor método gana 13.6 puntos del 25 al 100 %.
  - La segunda no: del 75 al 100 % la ganancia (+2.3) es menor que el rango entre semillas.
  - No se refuta porque la ganancia total supera los 2 puntos.
  - Lectura: con 400–550 casos la curva ya se está aplanando para este conjunto y esta percepción. Duplicar ultrasonidos del mismo tipo daría probablemente pocos puntos, y con 42 malignos de prueba no se podría medir.
- **«La memoria aprovecha los datos como los demás»: sostenido**, y más que eso: depende más de ellos. En B gana 32.2 puntos, contra 13.5 de los prototipos. En A es el único método que mejora, porque su envolvente necesita casos para cubrir. Aun con todo el train queda 9 puntos por debajo en balanceado y 15.7 en sensibilidad.
- **«La revisión de la memoria tiene valor propio»: refutado.** A igual carga de revisión no deja escapar menos malignos que la cabeza con umbral ni que Mondrian. Deja escapar entre 0.8 y 1.8 más.

## Lectura

1. **Para estos datos, el cuello no es la cantidad, es lo que la percepción saca de la imagen.** Con el encoder fijo, los métodos por distancia dan lo mismo con el 25 % que con el 100 % (AUROC 0.937). Lo que mejora con más datos es el encoder: del 25 al 75 % sube mucho y del 75 al 100 % casi nada.
2. **La memoria necesita más datos que los demás para llegar al mismo lugar, y no llega.** Con pocos casos, su envolvente no cubre y rechaza (33 % con el 25 % del train). Con más casos rechaza menos y acierta más, pero se queda en 77 % balanceado, contra 85–86 % de los métodos por distancia.
3. **Igualar el registro cambia sensibilidad por especificidad.** Es el mismo mecanismo del ancho de envolvente de exp20, en una sola modalidad: la envolvente benigna, registrada con más casos, contiene imágenes malignas.
4. **Ningún método es seguro como detector con esta evidencia.** En la mejor configuración, entre 3 y 5 de 42 malignos se escapan sin aviso aun mandando a revisión un 26–30 % de los casos. Los intervalos de sensibilidad miden unos 25 puntos. Una afirmación clínica pediría muchos más malignos de prueba.

## Para la reunión con médicos

- Más ultrasonidos del mismo tipo, por sí solos, no parecen la prioridad: la curva se aplana.
- Lo que más podría cambiar el resultado es la información que este experimento no tiene:
  - mejor imagen (resolución original, no 128 px);
  - otras fuentes del mismo paciente (mamografía, BI-RADS, edad);
  - y un conjunto de prueba con cientos de malignos confirmados por biopsia, para que la sensibilidad se pueda medir con un margen útil.
- La parte del sistema que tiene sentido ofrecer es la organización transactiva con abstención y revisión, implementada con prototipos o con el clasificador. No la memoria asociativa como detector.

## Notas

- Una semilla por configuración en el entrenamiento del encoder, cinco en total por fracción. Al 100 %, las semillas solo cambian el entrenamiento.
- **Casos de revisión del contenido claro:** cuando la memoria de contenido es clara pero el protocolo no responde lo mismo, el caso va a revisión. Casi siempre es porque el directorio lo rechaza: su envolvente sale de la fase A y es más estrecha. Fueron de 5 a 7 casos al 100 % y 20 al 25 % (semilla 42).
- **Mondrian:** alfa se eligió para igualar la carga de revisión de la memoria en el test. Usa el tamaño de las listas, no las etiquetas.
- **Brazo A:** el encoder vio todo el train al ajustarse, así que ese brazo mide solo el registro, no un sistema que haya visto menos datos.
