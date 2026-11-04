# Resumen CIFIN 2026 (P176): propuesta de corrección

Pendiente de aprobación; no se ha tocado el `.docx`. Fuente: `Downloads/Resumen_CIFIN2026_Gonzalez.docx` (enviado el 20 oct). Límite de la plantilla: 300 palabras.

## Los pesos homo no cambian ninguna cifra

Las 9 corridas industriales con pesos homo salen idénticas a las uniformes; solo cambian los tiempos (commit a2898e2). Las lecturas industriales ya son homo. El ruteo lee los directorios con pesos homo: en el nivel 1, los 1239 puntajes con soporte cambian con el modo de pesos, pero en cada pista una sola pieza tiene soporte, así que el ganador no puede cambiar (0 de 2162 decisiones distintas). Los especialistas leen contención (no depende de pesos) o el puntaje medio de `recog_weights`, que son los pesos homo R[i, a_i]; la monolítica pasa esos mismos pesos de forma explícita.

| Cifra del resumen | Fuente | Con pesos homo |
|---|---|---|
| AUROC 0.789 · 0.800 · 0.784 | `parametros_mae`, confirmación, G2 ResNet18 | igual |
| 0.695 contra 0.830 | `parametros_mae`, parches ResNet18 | igual |
| 98.4 %, sin confusiones | `industrial`, normales (962): 98.4 a su pieza, 1.6 rechazo, 0 a otra | igual |
| 28 % → 59 % | `parametros_mae`, parches: H 28.2 / 6.1 contra PatchCore 58.7 / 7.9 (detección / falsa alarma, 95 % de aceptación) | igual |
| 37.9 contra 39.2 % | `enrutador_flota`, B1 | igual |
| 100 % contra 0 % de kNN | `enrutador_flota`, B2 (12 pliegues) | igual |

«28 % → 59 %» sí tiene fuente: es la tabla de parches de `parametros_mae`.

## Lo que corrijo y por qué

1. **«Fallas pequeñas».** Ningún resultado separa las fallas por tamaño. 0.695 contra 0.830 y 28 contra 59 % son la lectura por parches sobre **todas** las fallas de las 6 piezas de confirmación. Además, 59 % es PatchCore solo con la pieza conocida, no la arquitectura mixta de punta a punta.
   - Viejo: «Con fallas pequeñas y locales pierde frente a PatchCore (0.695 contra 0.830). […] La detección de fallas pequeñas pasa de 28 % a 59 %, y el sistema deja escapar…»
   - Nuevo: «Por parches pierde frente a PatchCore (AUROC 0.695 contra 0.830; detección 28 contra 59 %). […] El sistema deja escapar…»
2. **37.9 contra 39.2 %.** La MAE deja escapar menos porque envía a una persona el 12.5 % de las fallas y el 1.6 % de las buenas. Con eso, su alarma baja de 60.8 a 49.6 %.
   - Viejo: «…contra 39.2 % de un detector que ya conoce la pieza.»
   - Nuevo: «…contra 39.2 % de un detector que ya conoce la pieza, porque envía a revisión humana 12.5 % de las fallas y 1.6 % de las buenas.»
3. **100 % contra 0 % de kNN.** kNN **con** umbral de abstención también llega a 100 %. El 0 % es kNN sin umbral, y el README dice que en VisA las piezas están tan separadas que la prueba fue fácil.
   - Viejo: «(100 %, contra 0 % de kNN)»
   - Nuevo: «(100 %; kNN sin umbral, 0 %)»
4. **Recortes para no pasar de 300 palabras.**
   - «La MAE se organizó» → «Se organizó».
   - «Estos resultados indican que esta propuesta podría servir» → «Esta propuesta podría servir».

## Para que decidas

- **(a) Propiedades.** «Agregar o retirar sin reentrenar» y «olvido exacto» también los tiene kNN (se agregan o borran vectores). Lo que solo tiene la MAE es no guardar imágenes ni vectores (solo conteos) y abstenerse sin un umbral aparte. No lo cambié porque es una decisión de argumento. Si quieres, propongo una frase.
- **(b) Falsa alarma.** 28 contra 59 % es a igual aceptación de calibración (95 %). En el test, la falsa alarma de PatchCore es 7.9 % contra 6.1 % de la MAE. No cupo en el límite; para la revista sí conviene ponerlo.

## Texto propuesto

**Resumen** (298 palabras sin «Resumen—»)

Este trabajo evalúa si la memoria asociativa entrópica (MAE), un modelo de caja blanca inspirado en la memoria natural, puede sostener la inspección visual en líneas con varios tipos de pieza. Se organizó como un sistema de memoria transactiva, con un especialista por pieza y un directorio que registra qué módulo resuelve cada caso. Se comparó con detectores estándar en el conjunto público VisA (12 tipos de pieza, fotografías y fallas reales), con predicciones fijadas antes de cada experimento. Leída en grado, la MAE detecta fallas con un AUROC de 0.789, cercano al de Mahalanobis (0.800) y superior al de kNN (0.784). Cada decisión indica en qué rasgos la pieza se aparta de lo registrado. Por parches pierde frente a PatchCore (AUROC 0.695 contra 0.830; detección 28 contra 59 %). Por eso se propone una arquitectura mixta en la que la MAE identifica la pieza (98.4 %, sin confusiones) y PatchCore decide si hay falla. El sistema deja escapar 37.9 % de las fallas, contra 39.2 % de un detector que ya conoce la pieza, porque envía a revisión humana 12.5 % de las fallas y 1.6 % de las buenas. En esta arquitectura, la elección del módulo se explica con los conteos de la memoria y los aciertos de cada módulo, mientras que la decisión de PatchCore no es de caja blanca. Las pruebas son de laboratorio y falta validarlas en una línea real. La MAE conserva propiedades que los detectores estándar no tienen juntas: reportó como desconocidas todas las piezas nunca registradas (100 %; kNN sin umbral, 0 %), permite agregar o retirar productos sin reentrenar, olvida datos de forma exacta y no almacena imágenes. Esta propuesta podría servir para organizar la inspección en líneas con catálogo cambiante, con un detector especializado para las fallas finas.

**Abstract** (290 words)

This work evaluates whether the entropic associative memory (EAM), a white-box model inspired by natural memory, can support visual inspection on lines with several part types. It was organized as a transactive memory system, with one specialist per part and a directory that records which module solves each case. It was then compared with standard detectors on the public VisA dataset (12 part types, real photographs and defects), with predictions fixed before each experiment. Read in a graded way, the EAM detects defects with an AUROC of 0.789, close to Mahalanobis (0.800) and above kNN (0.784). Each decision shows in which features the part departs from what was registered. By patches it falls behind PatchCore (AUROC 0.695 versus 0.830; detection 28 versus 59 %). This motivates a mixed architecture in which the EAM identifies the part (98.4 %, with no confusions) and PatchCore decides whether there is a defect. The system lets 37.9 % of defects through, versus 39.2 % for a detector that already knows the part, because it sends 12.5 % of defects and 1.6 % of good parts to human review. In this architecture, the choice of module is explained by the memory's counts and the recorded successes of each module, while PatchCore's defect decision is not white-box. The tests come from the laboratory and still have to be validated on a real line. The EAM keeps properties that standard detectors do not offer together: it reported every never-registered part as unknown (100 %; kNN without a threshold, 0 %), allows products to be added or withdrawn without retraining, forgets data exactly and stores no images. This proposal could serve to organize inspection on lines with a changing product catalogue, with a specialized detector for fine defects.
