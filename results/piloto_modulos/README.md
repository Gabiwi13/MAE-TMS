# Piloto: el sistema transactivo como organizador de una flota de módulos

Prueba piloto para decidir si el sistema transactivo, construido con memorias asociativas entrópicas, merece una línea de investigación propia como **organizador de una flota de módulos especializados**. Diseño, predicciones y criterio fijados antes de correr en [`propuesta_piloto_modulos.md`](../../propuesta_piloto_modulos.md). Script: [`run_piloto_modulos.py`](../../run_piloto_modulos.py). Detalle en `resumen.txt` y `resultados.json`.

**Resultado en una línea:** el sistema **aprende cuál módulo lo hace mejor** solo a partir de sus transacciones y sin índice central: con la lectura de calidad (éxitos / intentos), 79.0 % de las consultas va al mejor de los dos módulos de su dominio, contra 52.6 % de la lectura oficial (azar). Supera al router central kNN (71.6 %) y queda por encima de la cota «todos», que conoce la pieza verdadera (76.2 %). También incorpora un módulo nuevo en unas 20 transacciones, tolera la salida de uno y se abstiene ante el 100 % de lo desconocido. Pero **no cumple el criterio de costo y acierto**: consulta 19 de 24 módulos (el criterio pedía ≤ 6) y queda 7.5 puntos por debajo del router central, porque se abstiene en el 8.9 % de las consultas conocidas. Según lo fijado, el resultado es intermedio.

## Montaje

- **Flota:** 24 módulos, 12 piezas de VisA × 2 redes especializadas de distinta calidad. A es la red base. El segundo módulo es la variante más débil (de las ya entrenadas con sintéticas o anti-colapso), elegida por su acierto en la mitad de aprendizaje. Acierto en evaluación, del 55.8 % (pcb1/B) al 98.3 % (chewinggum/B). En 7 dominios los dos difieren en ≥ 5 puntos.
- **Ruteo:** percepción común (ResNet18 + PCA64, nivel 1 del demo industrial). El contenido de cada módulo es una MAE con las normales de su pieza. Los dos módulos de un dominio tienen el mismo contenido: solo la experiencia los distingue.
- **Directorios:** dos por módulo, **intentos** y **éxitos**. Registran la transacción (16 variantes) el módulo de entrada y el que respondió.
- **Aprendizaje:** 816 consultas con retroalimentación; 790 transacciones (las otras 26 no las contenía ningún módulo), 684 exitosas. **Evaluación:** 823 consultas conocidas y 756 desconocidas (fondo de ojo 300, piel 300, mama 156).

## Resultados

| método | acierto | abstención en conocidas | acierto de lo respondido | abstención en desconocidas | módulos consultados por consulta conocida |
|---|---|---|---|---|---|
| R1 oficial (pertenencia) | 77.5 | 8.9 | 85.1 | 100.0 | 19.2 |
| **R2 calidad (éxitos / intentos)** | **80.8** | 8.9 | **88.7** | 100.0 | 19.2 |
| router central kNN | **88.3** | 1.2 | 89.4 | 100.0 | (índice central) |
| compuerta aprendida | 87.8 | 2.2 | 89.8 | 100.0 | (índice central) |
| cota «todos» con la pieza verdadera (el más confiado de su pieza; no es rival) | 86.3 | 4.7 | 90.6 | 100.0 | 24 consultas de contenido; contienen 1.9 |
| al azar entre los que contienen | 80.6 | 4.7 | 84.6 | 100.0 | 24 consultas de contenido |
| oráculo | 93.7 | — | — | — | — |

**Preferencia por el mejor módulo** (dominios con diferencia de ≥ 5 puntos; fracción de lo ruteado a su dominio que va al mejor):

| dominio (mejor contra peor) | R1 | **R2** | central | compuerta | todos (cota) |
|---|---|---|---|---|---|
| candle (96.1 contra 85.5) | 52.7 | 77.0 | 89.5 | 100 | 82.4 |
| capsules (90.0 contra 74.0) | 72.1 | 55.8 | 35.4 | 0 | 86.0 |
| chewinggum (98.3 contra 91.5) | 46.3 | 82.9 | 34.5 | 100 | 17.4 |
| pcb1 (89.5 contra 55.8) | 50.6 | 91.1 | 91.8 | 100 | 76.5 |
| pcb2 (92.9 contra 77.6) | 46.8 | 87.3 | 85.9 | 100 | 91.4 |
| pcb3 (86.7 contra 77.1) | 35.4 | 78.0 | 74.7 | 100 | 84.1 |
| pipe_fryum (92.2 contra 74.5) | 63.9 | 80.6 | 89.4 | 100 | 95.3 |
| **media** | **52.6** | **79.0** | 71.6 | 85.7 | 76.2 |

La compuerta elige un solo módulo por dominio con su tasa global: acierta del todo o falla del todo (capsules 0 %). R2 decide por la tasa de éxito **local** de cada pista y se equivoca menos de forma sistemática.

**Eventos:**

| evento | resultado |
|---|---|
| E1, alta de candle (antes: 100 % de abstención en candle) | tras 5, 10, 20 y 40 transacciones: 22.4, 52.6, **89.5** y 92.1 % de candle va a sus módulos; acierto 22.4, 48.7, 81.6 y 85.5 % |
| E2, baja de pcb1/A (el mejor de pcb1) | las consultas de pcb1 van a pcb1/B (76) o se abstienen (10); acierto 48.8 % (antes 79.1 %; pcb1/B solo acierta 55.8 %). Ningún error grave: lo que sale va al único módulo competente que queda |

## Predicciones y criterio

| | predicción | resultado |
|---|---|---|
| PP1 | R1 y R2 a ≤ 3 puntos del central, consultando 2 a 4 módulos | **No se cumple**: a 7.5 (R2) y 10.8 (R1) puntos, consultando 19 de 24 |
| PP2 | R1 reparte cerca de 50/50; R2 prefiere al mejor en más del 70 % (incierto) | **Se cumple**: R1 52.6 %, R2 79.0 % |
| PP3 | abstención en la mayoría de las desconocidas | **Se cumple**: 100 % en todos los métodos (dominios médicos muy lejanos de VisA) |
| PP4 | E1: ≥ 80 % de candle a sus módulos tras 20 transacciones; E2: las consultas pasan al otro módulo con su acierto | **Se cumple**: 89.5 %; pcb1 pasa a pcb1/B (48.8 % contra 55.8 % de ese módulo) |

**Criterio:**
- «**Sigue**» pedía R2 a ≤ 3 puntos del central **con** ≤ 6 módulos consultados, **y** ≥ 70 % al mejor. Se cumple lo segundo (79.0 %), no lo primero (7.5 puntos y 19 módulos).
- «**No sigue**» pedía < 70 % al mejor **y** la compuerta > 5 puntos por encima. No se da: R2 sí aprende la calidad.
- **Resultado intermedio**, como se previó en la propuesta: se reporta y se discute.

## Lectura

1. **Lo nuevo funciona.** Un directorio hecho solo de memorias asociativas, con dos registros (intentos y éxitos) y sin índice central, estima la tasa de éxito local de cada módulo y elige al mejor el 79 % de las veces, por encima de un kNN central con las mismas transacciones. Es la primera vez en el proyecto que el sistema transactivo aprende **calidad** y no solo pertenencia, y es justamente lo que hace falta para organizar una flota de módulos.
2. **El costo de consulta no es bajo con este protocolo.** Como la entrada de cada transacción se sorteó entre los 24 módulos, cada uno terminó «conociendo» a unos 19, y `route_transactive` suma todos esos directorios. La ventaja de la descentralización del exp10 no aparece cuando cualquiera puede ser la entrada de cualquier cosa. Hace falta una entrada con estructura (por ejemplo, entradas por línea o por familia de piezas) o limitar el círculo.
3. **La abstención en lo conocido (8.9 %) es el costo de la contención estricta (ξ = 0)** sobre directorios formados con unas 790 transacciones. Lo que responde, lo responde casi tan bien como el central (88.7 contra 89.4 %). Una lectura tolerante o más transacciones lo atacarían.
4. **Dinámica sana:** un módulo nuevo se adopta en unas 20 transacciones, sin tocar a los demás. Cuando sale el mejor, el sistema pasa al que queda y no inventa destinos.

## ¿Vale una tesis?

Hay un resultado positivo y nuevo: aprender quién lo hace mejor, de forma descentralizada, con memorias asociativas. También hay dos problemas concretos y medibles: el costo de consulta y la cobertura. Una tesis tendría preguntas claras:
- ¿Con qué estructura de entradas se consulta a pocos módulos sin perder la preferencia por calidad?
- ¿Con qué lectura (tolerante, por cantidad de evidencia) baja la abstención sin rutear mal?
- ¿Escala a cientos de módulos y a módulos que no son de visión?

Un piloto no basta para afirmar que el sistema es mejor que un router central. Basta para decir que **la pregunta está bien planteada y la idea central funciona**.

## Notas

- Una sola semilla. Las 7 piezas con diferencia de ≥ 5 puntos tienen de 50 a 85 consultas de evaluación cada una.
- La lectura R2 (éxitos / intentos) se definió para este piloto; no está en el código oficial. Usa solo las proyecciones de las memorias de directorio.
- **«Todos» es una cota asistida por un oráculo de pieza, no un rival** (corregido el 26 oct 2026). Consulta el contenido de los 24 módulos. Entre los que contienen (1.9 en promedio), solo considera los de la **pieza verdadera** y elige el de mayor confianza de su red. Los de otra pieza quedan con confianza 0, porque sus redes no se guardaron y no hay predicciones suyas sobre imágenes ajenas. Saber la pieza es justo lo que los demás métodos tienen que averiguar, así que su 86.3 % no se compara con R1/R2, el central o la compuerta como un método más.
- El router central y la compuerta guardan todas las transacciones en un solo lugar.
- En `resumen.txt`, la columna de módulos consultados (21.5) promedia también las desconocidas, que recorren los 24. La tabla de arriba da la media de las conocidas (19.2; mediana 19, mínimo 9), calculada después desde `resultados.json`.
- En E1, el acierto de R2 en las demás piezas (72.7 %) es menor que en la corrida principal (80.8 %). Es otra corriente de aprendizaje, sin las transacciones de candle y con otro orden aleatorio. No se investigó más.
