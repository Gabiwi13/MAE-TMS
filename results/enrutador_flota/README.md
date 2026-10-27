# Enrutador de una flota de detectores (VisA)

En una línea con un detector PatchCore por pieza, el enrutador decide qué detector recibe cada imagen, o se abstiene y la manda a un humano. ¿La MAE rutea la flota igual que kNN? ¿Su abstención protege cuando llega una pieza que el sistema no conoce? Diseño, predicciones y criterio fijados antes de correr en [`propuesta_olvido_y_flota.md`](../../propuesta_olvido_y_flota.md) (parte B). Script: [`run_enrutador_flota.py`](../../run_enrutador_flota.py). Detalle en `resumen.txt` y `resultados.json`.

**Resultado en una línea:** con piezas conocidas, la MAE deja pasar las mismas fallas que el oráculo (37.9 contra 39.2 %), a cambio de mandarle a un humano el 1.6 % de las normales y el 12.5 % de las fallas. Con una pieza nueva, se abstiene en el 100 % de los casos en los 12 pliegues. kNN con abstención, también. En VisA las piezas están tan separadas que la prueba fue fácil.

## Montaje

- **Detectores:** PatchCore por pieza (parches de las capas 2 y 3 de ResNet18, PCA a 64 por pieza, distancia al parche más cercano del llenado y máximo sobre la imagen). Umbral para aceptar el 95 % de las normales de calibración de su pieza. Si una imagen va a otra pieza, la decide el detector de esa pieza, con sus parches proyectados con la PCA de esa pieza.
- **Enrutadores sobre el nivel 1 del demo** (ResNet18 + PCA64):
  - MAE: `Level` y `route_transactive`, entrada por un no especialista.
  - kNN: coseno, 5 vecinos, sin abstención.
  - kNN con abstención: distancia media a 5 vecinos, umbral a la aceptación de calibración de la MAE (99.0 %).
  - Oráculo: la pieza verdadera.

## B1 · piezas conocidas (todo el test: 962 normales y 1200 fallas)

| enrutador | a su pieza | a otra | normales: alarma / a humano / pasa | fallas: alarma / a humano / pasa (silenciosa) |
|---|---|---|---|---|
| oráculo | 100.0 | 0.0 | 7.6 / 0.0 / 92.4 | 60.8 / 0.0 / 39.2 |
| **MAE** | 92.4 | 0.0 | 7.4 / 1.6 / 91.1 | 49.6 / 12.5 / **37.9** |
| kNN | 100.0 | 0.0 | 7.6 / 0.0 / 92.4 | 60.8 / 0.0 / 39.2 |
| kNN con abstención | 97.2 | 0.0 | 7.3 / 1.0 / 91.7 | 57.5 / 4.2 / 38.3 |

Ningún enrutador manda una imagen a otra pieza. La MAE se abstiene más en las fallas que en las normales (12.5 contra 1.6 %), igual que en el demo. Algunas de esas fallas el detector las habría dejado pasar, así que la falla silenciosa baja 1.3 puntos respecto del oráculo. El precio es mandarle a un humano 1.6 % de las normales.

**Tamaño del estado:** MAE 1 013 760 celdas de conteo (2.0 MB en uint16), casi todo en los directorios. kNN: 3240 latentes de 64 flotantes (0.83 MB).

## B2 · una pieza nueva, que no está en el sistema (12 pliegues)

En cada pliegue el sistema se construye con 11 piezas, y llegan las 150 a 201 imágenes de test de la pieza que falta.

| enrutador | a humano (deseable) | a otro detector, que da alarma | a otro detector, que la deja pasar (falla silenciosa) |
|---|---|---|---|
| **MAE** | **100.0** en los 12 pliegues | 0.0 | 0.0 |
| kNN sin abstención | 0.0 | 100.0 | 0.0 |
| kNN con abstención | 100.0 | 0.0 | 0.0 |

**Comprobación de que no es un error** (hecha al ver el 100 %): con kNN, la imagen nueva más cercana queda 1.4 veces por encima del umbral de abstención (pcb2: 9.67 contra 6.99), y la mediana entre 1.8 y 3.2 veces. kNN sin abstención manda cada pieza nueva a su vecina (macaroni1 a macaroni2, pcb2 a pcb4, cashew a chewinggum), y el detector de la vecina da alarma en todas. Ninguna pasa en silencio.

Así que en VisA la abstención **no hace falta para la seguridad**: un detector de otra pieza da alarma con cualquier pieza extraña. La diferencia está en **qué dice el sistema**. La MAE dice «pieza desconocida». kNN sin abstención dice «falla en macaroni2» para el 100 % de los macaroni1 sanos, y eso lleva a diagnosticar mal y a descartar piezas buenas.

## Predicciones y criterio

| | predicción | resultado |
|---|---|---|
| PB1 | piezas conocidas: MAE ≈ kNN ≈ oráculo (< 1 punto); la MAE se abstiene en 1–2 % de normales y en 10–15 % de fallas | **Se cumple en abstención** (1.6 y 12.5). **En el borde en el sistema completo**: contando la abstención como alarma, la MAE marca 62.1 % de las fallas contra 60.8 y 9.0 % de las normales contra 7.6 (1.3 y 1.4 puntos) |
| PB2 | pieza nueva: kNN sin abstención manda el 100 % a otro detector; la MAE se abstiene en ≥ 50 % pero no en todo, porque las piezas parecidas se contendrían; kNN con abstención, cerca de la MAE | **Se cumple** lo de kNN (100 %) y que kNN con abstención quede igual que la MAE. **No se cumple que las vecinas contengan a la nueva**: la MAE se abstiene en el 100 %, incluso con pcb y macaroni |
| PB3 | el estado de la MAE pesa más que el de kNN | **Se cumple**: 2.0 contra 0.83 MB |

**Criterio B** («la abstención de la MAE protege a la flota de una pieza nueva»): **no se puede decidir con estos datos**. La falla silenciosa es 0 para todos los enrutadores, así que la condición de 20 puntos menos que kNN no puede cumplirse. Y la abstención (100 %) está muy lejos del umbral de refutación (< 30 %). La prueba no discrimina, porque las piezas de VisA están demasiado separadas y los detectores atrapan cualquier pieza extraña.

## Lectura

1. **La MAE funciona como enrutador de la flota** y no daña el sistema: deja pasar las mismas fallas que el oráculo. Su abstención agrega trabajo humano (1.6 % de normales), concentrado donde hay fallas.
2. **Reconocer «esto no es de nadie» la MAE lo hace bien cuando lo nuevo es claramente distinto**, igual que kNN con un umbral. No hay ventaja medible sobre kNN con abstención, igual que en exp20.
3. **El valor de la abstención aquí es el diagnóstico, no la seguridad.** Sin abstención, una pieza nueva se reporta como una falla de otra pieza. Con abstención, se reporta como desconocida. En una planta, la segunda respuesta es la correcta.
4. **Para medir lo que de verdad importaría** (una pieza nueva muy parecida a una conocida, como una variante de la misma placa) hace falta un conjunto con variantes cercanas, que VisA no tiene.

## Notas

- El umbral de kNN con abstención se fijó con las normales de calibración (fase A), como se declaró. La MAE las tiene registradas en los directorios, así que su aceptación ahí (99.0 %) es mayor que en test (98.4 %).
- El tamaño de la MAE cuenta las celdas de todos sus arreglos de conteo (incluido el margen para valores indefinidos); el de kNN, solo los latentes del llenado.
- Una sola semilla. Cada punto porcentual por pieza son 1 o 2 imágenes.

- **Umbral de energía (nota del 26 oct 2026).** La MAE rutea con `run_medico_demo.Level.route`, que rechaza antes de consultar la memoria si la norma del latente queda bajo el umbral. El script guarda el destino pero no el motivo, así que no se sabe qué parte de la abstención de la MAE es del umbral y no de la memoria. Falta medirlo.
