# Experimento 16: lectura de los resultados

**Corrida:** 24 de septiembre de 2026, `run_experiment16_leave_object_out.py`, 10 pliegues (uno por objeto de cada clase, en el orden de la clase), una semilla, ~49 min por pliegue con dos procesos. En cada pliegue el contenido (200 imágenes × 16 variantes) y la fase A (128 percepciones × 16) se construyen con los nueve objetos restantes; se evalúan sobre los mismos modelos 328 vistas del objeto reservado («nuevo») y 328 vistas no usadas de los objetos que contribuyeron («conocido»). Tablas en `README.md`.

## Criterio (§6)

**Sostenida.** La cobertura de punta a punta sobre objetos nuevos es el **93 %** de la de objetos conocidos en el mismo pliegue (razón 0.93 [0.89, 0.97] sobre pliegues; umbral 0.75) y los falsos ruteos sobre objetos nuevos son **2 de 3280** (0.1 %; umbral 2 %): `cow → dog` y `horse → dog`, una vez cada uno.

## Las cifras

| medida (% de 328 por pliegue, media de 10) | objeto conocido | objeto nuevo | brecha |
|---|---|---|---|
| contenido acepta (especialista propio) | 99.1 | 95.2 | 3.9 [1.6, 6.9] |
| responde (hetero) | 96.2 | 91.0 | 5.2 [1.7, 9.0] |
| directorio acepta | 98.0 | 92.2 | 5.8 [2.7, 9.1] |
| ruteo correcto sobre las aceptadas | 99.9 | 99.9 | — |
| punta a punta | 95.5 | **89.2** [85.1, 93.2] | 6.3 [2.5, 10.4] |

La cifra de objeto conocido (95.5 %) reproduce, con modelos construidos con nueve objetos, el 96.2 % del sistema oficial: el protocolo del pliegue es el oficial con otro conjunto de imágenes.

## Lo que muestran los datos

**La envolvente generaliza a objetos nuevos, con una brecha de 6 puntos.** Perder un objeto de cada clase cuesta 6.3 puntos de cobertura sobre ese objeto y ninguno de precisión: el ruteo correcto sobre las aceptadas sigue en 99.9 %. Es la predicción P4, y con más margen del previsto (0.93 contra el 0.5 que fijaba el umbral de refutación). La lectura teórica es la de exp8: la memoria guarda soportes por coordenada, y las vistas de un objeto nuevo comparten con las de los otros nueve la mayoría de los 64 valores cuantizados.

**El fallo es rechazo, no invención (P3 confirmada).** De las 328 vistas nuevas por pliegue, las que el sistema no cubre (10.8 %) se rechazan en el contenido o en el directorio; solo 2 de 3280 se rutean a otra clase, y ambas al par animal (P2 confirmada: `cow → dog`, `horse → dog`).

**La brecha vive en objetos concretos, no en clases (P1 refutada).** La predicción era que las clases de forma variable (animales, coches) generalizarían peor que las de forma uniforme (frutas). Es al revés: `horse` (94.4 % de punta a punta sobre objetos nuevos) y `tomato` (95.9 %) son las mejores, y las peores son `apple` (82.4 %) y `pear` (83.9 %). Por objeto, 74 de los 80 objetos reservados quedan por encima del 70 %; los seis restantes concentran la brecha: `apple3` (0 %), `pear9` (10 %), `apple10` (32 %), `dog10` (49 %), `pear6` (59 %), `cup10` (61 %), `car6` (63 %), `cow2` (68 %). Son objetos cuyo aspecto (color o forma) no cabe en la envolvente que forman los otros nueve; el sistema los rechaza en vez de asignarlos a otra clase. Por pliegue, la cobertura de objeto nuevo va del 78.7 % (pliegue 10) al 98.8 % (pliegue 4).

**La evocación no se degrada.** Sobre las vistas nuevas que responden, el acierto estricto es del 99.1 % y el dominio ajeno del 1.8 % (240 imágenes evocadas).

## Lo que no decide

- Con diez objetos por clase, «objeto nuevo» sigue siendo un objeto de la misma colección fotografiada en las mismas condiciones (fondo, iluminación, distancia). La generalización a fotos de otro origen es otra pregunta (el laboratorio en vivo la tocó: la cadena impresora–cámara saca el latente del soporte).
- No dice si los seis objetos difíciles lo son por el encoder (latente lejos de los demás) o por la cuantización; medirlo es una sonda de distancias como la de exp8.

## Consecuencia para el reporte

La cifra de generalización visual a objetos nunca vistos es **89.2 % de cobertura de punta a punta con 0.1 % de falsos ruteos**, seis puntos por debajo de la cifra por imagen (95.5 % en el mismo protocolo; 96.2 % de ruteo en el sistema oficial). La limitación (b) y la metodología pueden dejar de declarar el leave-object-out como pendiente y citar esta cifra con su brecha.
