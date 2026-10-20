# Propuesta: nombrar en palabras el tipo de falla (VisA)

Fijada el 20 de octubre de 2026, antes de correr. Parte del plan del artículo para el congreso ([`plan_articulo.md`](plan_articulo.md)).

## Pregunta

En el sistema mixto, PatchCore decide si hay falla. ¿Puede la parte heteroasociativa de la MAE, con imágenes de falla registradas junto con el nombre de su tipo, **decir en palabras qué falla es** («chunk of wax missing», «melt», «bent»…)? ¿Y puede **avisar cuando la falla es de un tipo que nunca se le registró**, en vez de ponerle el nombre de otro?

Es la parte del texto que sí es natural para la memoria: la palabra sale como respuesta a una imagen que se registró con ella, no entra como pista nueva. Las oraciones nunca registradas ya se probaron y no llegan a ninguna pieza ([`results/industrial_clip`](results/industrial_clip/README.md)), que es lo esperado.

## Antecedente que esta prueba tiene que superar

El demo industrial ya probó los tipos de falla como análisis secundario ([`results/industrial/README.md`](results/industrial/README.md), «Tipos de falla como dominios»). Usó una memoria por tipo, la percepción global G2, la lectura por contención y una sola partición 60/40. La memoria quedó por debajo de kNN en las 11 piezas, y solo por encima del azar en pcb1–pcb3; además rechazó entre 11 y 74 % del test.

Esta prueba cambia dos cosas, por razones que se dieron antes de verla:

1. **Percepción local.** La falla es local, y un vector global de la imagen casi no la registra. Ese es el mismo motivo por el que PatchCore le gana a la MAE en detección. Aquí la percepción son los parches que PatchCore marca como más anómalos.
2. **Lectura graduada.** Leída en grado (H, suma de log-frecuencias), la MAE igualó a Mahalanobis en detección ([`results/parametros_mae`](results/parametros_mae/README.md)), mientras que leída en sí/no perdía.

Es un segundo intento sobre los mismos datos, así que se declara como tal: se usan piezas de diseño y de confirmación, y el criterio solo se evalúa en confirmación.

## Datos

- **VisA**, las 1200 imágenes de falla, con el tipo de cada una según `image_anno.csv`. Solo entran las imágenes de **etiqueta única**: las que tienen varios tipos a la vez se excluyen y se reporta cuántas son.
- **Tipos que entran:** los que tienen al menos 10 imágenes de etiqueta única, igual que el antecedente. Una pieza entra si tiene al menos 2 tipos así. capsules queda fuera (un solo tipo).
- **Piezas de diseño:** candle, cashew, macaroni1, pcb2, pcb3, pcb4; es la misma partición de [`parametros_mae`](results/parametros_mae/README.md).
- **Piezas de confirmación:** chewinggum, fryum, macaroni2, pcb1, pipe_fryum.
- **Particiones:** por tipo, 60 % de registro y 40 % de prueba, estratificado, con 10 semillas (0 a 9). Se reportan la media y el rango.

## Percepción

- **L (local, principal).** Es el mapa de PatchCore del demo: capas 2 y 3 de ResNet18, 784 parches de 384 canales, PCA a 64 ajustada sobre los parches normales de llenado de la pieza y distancia de cada parche al parche normal más cercano. De cada imagen de falla se toman los **k parches más anómalos**, y cada uno es una percepción de 64. El mapa usa solo piezas normales: no ve ninguna etiqueta de tipo ni ninguna máscara.
- **G (global, control).** Es la G2 del demo (ResNet18, PCA a 64 de la pieza), como en el antecedente. Sirve para separar el efecto de la percepción del efecto de la lectura.
- **k se elige en diseño** entre 1, 8 y 16.

## Métodos (los mismos datos para todos)

Cada imagen de registro aporta sus k parches, con su tipo, y cada imagen de prueba se representa con sus k parches.

- **MAE heteroasociativa oficial (palabras).** Es una memoria etiqueta ↔ latente como la memoria única M de [`industrial_monolitica`](results/industrial_monolitica/README.md). La etiqueta de cada tipo es el vector fastText de su nombre (media de sus palabras), cuantizado como en M, y el latente usa Q = 32 con el rango del registro + 10 %. La respuesta es la etiqueta con más soporte en la proyección de los k parches, **decodificada a su nombre**. Hay abstención («tipo no registrado») si ninguna etiqueta tiene soporte. Si dos tipos quedan con la misma etiqueta cuantizada, se fusionan y se reporta.
- **MAE graduada.** Es una relación de conteos por tipo, leída con H = Σᵢ log(1 + R[i, qᵢ(z)]) y sumada sobre los k parches; responde el tipo de H máximo, con su nombre. La abstención usa un umbral de H fijado en el registro: el percentil 10 de H en dejar-uno-fuera dentro del registro.
- **Rivales:**
  - kNN coseno (k = 5, media sobre parches);
  - NCM (distancia a la media del tipo);
  - regresión logística multinomial (L2, C = 1, sobre la media de los k parches);
  - azar (uniforme) y clase mayoritaria.
- Para la parte de tipos no registrados, kNN y NCM usan un umbral igual al de la MAE graduada (percentil 10 en dejar-uno-fuera del registro).

**Lo que se elige en diseño:** k y cuál lectura de la MAE es la principal (oficial o graduada). Las dos se reportan en confirmación, pero el criterio usa la principal.

## Medidas

1. **Nombrar:**
   - acierto balanceado por pieza (la abstención cuenta como error);
   - acierto entre las que responde y tasa de abstención;
   - matriz de confusión por pieza.
2. **Tipo no registrado:** se deja fuera un tipo a la vez, se registran los demás y se prueba con las imágenes del tipo excluido. Se mide qué fracción se reporta como «tipo no registrado» y, a la vez, cuánto se abstiene con los tipos registrados (falso rechazo).
3. **Dentro del sistema mixto:** las mismas medidas, solo con las fallas que PatchCore detecta a su umbral del 95 % de [`enrutador_flota`](results/enrutador_flota/README.md).

## Predicciones

- **P1.** La percepción local supera a la global en al menos 5 puntos de acierto balanceado, para kNN y para la MAE (media de las piezas de confirmación).
- **P2.** Con L, kNN y la regresión logística quedan entre 45 y 65 % de acierto balanceado. La MAE graduada queda a menos de 5 puntos de kNN, como en detección. La MAE oficial, por contención, queda más de 10 puntos debajo de kNN y se abstiene en más del 30 %.
- **P3.** Ante un tipo no registrado, ningún método lo reconoce bien, porque los tipos de una pieza se parecen entre sí. La MAE graduada y kNN con umbral reportan como «no registrado» entre 20 y 40 %, sin ventaja de más de 10 puntos para ninguno.

## Criterio (solo en confirmación, con la lectura y el k elegidos en diseño)

- **C1 «La MAE nombra el tipo de falla en palabras».**
  - **Sostenido** si su acierto balanceado supera al azar por al menos 15 puntos en 4 de 5 piezas **y** su media queda a no más de 5 puntos de kNN.
  - **Refutado** si su media queda más de 10 puntos debajo de kNN o menos de 5 puntos sobre el azar.
  - En medio, **sin decidir**.
- **C2 «La percepción local es la que permite nombrar».**
  - **Sostenido** si L − G ≥ 5 puntos de acierto balanceado para kNN y para la MAE.
  - **Refutado** si L − G < 0 para ambos.
- **C3 «La MAE avisa cuando el tipo de falla no está registrado».**
  - **Sostenido** si, con falso rechazo de 15 % o menos en los tipos registrados, reporta como «no registrado» al menos 10 puntos más que kNN con umbral.
  - **Refutado** si reporta igual o menos que kNN.

## Qué significaría

- **Si C1 y C2 se sostienen**, el sistema mixto agrega una explicación en palabras: PatchCore dice dónde está la falla y la MAE dice qué falla es, con el registro de ejemplos que sostiene esa respuesta. Ese es el lado de caja blanca que el sistema mixto conserva.
- **Si C1 se refuta**, el resultado del demo se mantiene: la MAE identifica la pieza, pero no el tipo de falla. Esto se reporta así en el artículo.
- **C3** es la versión, para tipos de falla, de la ventaja que la MAE ya mostró con piezas nuevas (100 % frente a 0 % de kNN sin umbral).

## Límites declarados de antemano

- **Pocos ejemplos.** Por tipo hay de 6 a 29 imágenes de registro, así que cada punto por pieza es una o dos imágenes. Por eso se usan 10 semillas.
- **Tipos.** Son los que definieron los anotadores de VisA. Algunos se parecen mucho entre sí («different colour spot» contra «similar colour spot»).
- **Etiquetas.** Los nombres están en inglés, como vienen en VisA, y fastText es en inglés. Traducirlos para mostrarlos no cambia nada.
- **Mapa.** El mapa de PatchCore se usa para elegir parches; si marca mal la falla, nombrarla es más difícil para todos los métodos por igual.
- **Segundo intento.** Se declara como tal (ver el antecedente). Lo que se reporta es la confirmación.

## Script y salida

`run_nombrar_falla.py`, que reutiliza las imágenes y los parches del demo industrial (`results/industrial/cache` del worktree del demo) sin escribir en ellos. Salida en `results/nombrar_falla/{README.md, resumen.txt, resultados.json}`.
