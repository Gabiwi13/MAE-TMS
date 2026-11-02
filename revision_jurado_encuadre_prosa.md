# Propuesta viejo/nuevo: el encuadre de la tesis tras los experimentos de la lectura de jurado

## Estado

Pendiente de tu aprobación. No apliqué nada: `.tex8` no cambió, no hay commit, ni push, ni ramas nuevas. La base es `una-hetero` en `6197bc3`.


- **Cotejo:** un script comprobó los 9 bloques «Viejo» contra `.tex8` por rango de líneas, y los 9 coinciden.
- **Pliegues:** el README de `objetos_nuevos_codificador_por_pliegue_parcial` dice 2 pliegues, pero `raw/` y `tablas.md` tienen 3. Uso los 3 de `tablas.md`; el README hay que actualizarlo.
- **Falta una pieza:** 05 todavía no tiene secciones de resultados para las líneas base, la calibración fija y el codificador sin pérdida de clase. Los textos nuevos las citan como `sec:lineas-base`, `sec:calibracion-fija` y `sec:codificador-sin-clase`. Hace falta una propuesta de resultados que las cree antes de aplicar esta.
- **Exp11:**
  - Lo que depende solo del enrutamiento ya está corrido con los directorios reiniciados: clase sobre el total, cobertura, fuera de dominio y destinos visuales.
  - Lo que depende del recuerdo (d_nn, dominio ajeno, el 79–84 %) es de la corrida anterior y va con `[PENDIENTE: exp11 d_nn]`.

## Tesis central en tres frases

1. EAM-TMS es un sistema de memoria transactiva hecho de memorias asociativas que funciona: reparte consultas de texto e imagen entre ocho especialistas, recupera el contenido asociado en los dos sentidos y rechaza lo que ningún módulo contiene, y cada decisión se lee en registros concretos de sus memorias.
2. Lo que la memoria asociativa agrega no es acierto de clase.
   - Sobre las mismas representaciones, decisores sin memoria la igualan en el enrutamiento de texto, donde su compuerta es exactamente la pertenencia al vocabulario.
   - En imagen la superan: aciertan de 652 a 655 de 656, contra 631.
   - Lo que sí agrega: rechazo sin umbral ajustado, recuerdo de la otra modalidad y, frente a una sola memoria con las ocho clases, un rechazo fuera de dominio que no empeora cuando crece el contenido.
3. Dos condiciones sostienen esos resultados, y ninguna sale del mecanismo asociativo: la lectura normalizada por conteo (B1) y un latente en que cada coordenada separe las clases, que da el codificador entrenado con supervisión de clase. Con evaluación fija, el directorio reproduce la decisión de la fase temprana sin consultar a los ocho módulos, pero no la mejora.

## Encuadre: qué ya no se sostiene y qué se defiende

**Ya no se sostiene:**

| Afirmación actual | Dónde | Qué dicen los datos | Fuente |
|---|---|---|---|
| La madura mejora a la temprana con la formación | `main:85-89`, `06:86-88`, `07:49-51` | Con un conjunto fijo, madura − temprana da +0.2 (N = 200) y +1.3 (N = 291). En el sorteo principal da −0.8, con bootstrap [−5.8, +4.2]. | `calibracion_evaluacion_fija` |
| «Clasifica algo mejor» que la EHAM única | `07:60-61`, `06:189-193` | Con N = 200, 96.8 contra 96.9 (−0.1 [−2.9, +2.9], p = 0.86). Con N = 25, 93.2 contra 97.6. | `experimento11_protocolo_corregido/ruteo/ruteo.md` |
| 97.0 % sobre las reservadas | `07:17-18` | 96.8 [96.3, 97.4] | `ruteo.md` |
| «Límites en la representación, no en el mecanismo» | `main:101-103`, `06:8-9`, `07:109-110` | Un 1-NN sobre los mismos latentes acierta 21 a 24 imágenes que el sistema no da bien. El mecanismo necesita B1 y un código separable por coordenada. | `lineas_base`, `codificador_sin_clase` |
| «Sin clasificadores supervisados» | `main:62-63`, `01:35`, `07:108` | Sin la pérdida de clase del codificador, el enrutamiento visual baja de 96.2 a 70.4 %, con 169 falsos. | `codificador_sin_clase` |
| «El fallo es rechazo, no invención» con objetos nuevos | `06:294-296` | Con un codificador que no vio el objeto, 33 falsos de 984 (3.4 %) en 3 pliegues, contra 1 del oficial. | `…pliegue_parcial/tablas.md` |

**Se defiende:**

| Resultado | Cifra | Fuente |
|---|---|---|
| Rechazo sin umbral ajustado | Los decisores sin umbral aceptan 40 de 40 y el sistema 2. Un umbral de coseno da AUROC de 0.97 a 0.99, pero si no pierde ninguna reservada deja pasar de 9 a 23 de 40. | `lineas_base` |
| Doble compuerta frente a EHAM única | 2 de 40 en todos los cortes, contra 2, 2, 5 y 8. McNemar sobre las 40 consultas: p = 0.25 con N = 100 y p = 0.031 con N = 200. La segunda compuerta se decidió después de ver esas consultas. | `salida.md` M5.1 |
| Recuperación en los dos sentidos | Imagen → texto: 97.4 % de 116, contra un azar de 34.8. Texto → imagen: d_nn de 27.0 en el protocolo, 32.5 en la EHAM única y 26.8 en el oráculo `[PENDIENTE: exp11 d_nn]`. | `05:369-372`; `salida.md` E.1; `experimento11` |
| El recuerdo depende del índice | Con el codificador sin pérdida de clase, una imagen bien enrutada evoca su dominio en 80 de 81 casos. | `codificador_sin_clase` |
| Decisiones legibles | Compuerta igual a registro en 3064 pares. Un voto por frecuencia toma la misma decisión que la fase temprana en 380/400. Directorio igual a tabla de conteos (p = 0.58). | `lineas_base` |
| B1 es necesaria | Supera a la lectura cruda por 4.5 a 8.8 puntos; sin ella, la madura queda −7.5 por debajo de la temprana. | `calibracion_evaluacion_fija` |
| El directorio reemplaza al mediador | Concordancia con la fase temprana del 92.5 % en consultas no vistas, con acierto equivalente. | `calibracion_evaluacion_fija` |
| Separación por coordenada | Mediana 5.34 contra 0.24. Otras memorias contienen la imagen en el 0.5 % contra el 82.9 % de los casos. | `codificador_sin_clase` |

**Vínculo teórico** (analogías estructurales):

- **El directorio localiza:** `wegner1995computer` describe la coordinación de la recuperación como planear cómo encontrar cada ítem, y `sparrow2011google` muestra que se recuerda más dónde encontrar la información que la información misma.
- **Cuándo conviene el directorio:** en `ren2006contingent`, saber quién sabe qué conviene más en grupos grandes y en entornos cambiantes. Aquí son ocho módulos, contenido fijo y especialización asignada (`wegner1991transactive`).
- **Almacén único:** la familiaridad como suma sobre todas las huellas (`clark1996global`).
- **Separar antes de guardar:** separación de patrones en el hipocampo (`yassa2011pattern`, V+) y aprendizaje de categorías que aumenta la sensibilidad a las dimensiones que distinguen (`goldstone1994influences`, V+ parcial).

Las dos últimas citas son nuevas y las verifiqué en esta sesión. Glucksberg y McCloskey (1981), sobre decidir «no sé», quedó fuera: no encontré su registro primario.

## Puntos viejo/nuevo

| Punto | Pasaje | Qué hace |
|---|---|---|
| E1 | `main:57-104`, resumen completo | Reemplaza |
| E2 | `01:29-38`, la pregunta | Reemplaza; decisión tuya |
| E3 | `01:69-114`, contribuciones | Reemplaza |
| E4 | `06:5-24`, apertura de 6.1 | Reemplaza; las figuras de `06:26-37` no cambian |
| E5 | después de `06:203` | Subsección nueva |
| E6 | `07:8-10`, apertura | Reemplaza |
| E7 | `07:12-32`, resultados principales | Reemplaza |
| E8 | `07:34-52`, respuesta a la pregunta | Reemplaza |
| E9 | `07:54-63`, frente a una EHAM única | Reemplaza |
| E10 | después de `07:101`, trabajo futuro | Punto nuevo |
| E11 | `07:106-110`, cierre | Reemplaza |

**E1. Resumen** (`main:57-104`). Cambia, con respecto a estructura 9.1:
- 97.0 pasa a 96.8, y se queda la composición de las reservadas (87.7 frente a 49.8 %).
- Salen el 93.0 dentro de muestra y el 20.5 → 13.8 de `apple`.
- Entran la clase igual a la de la EHAM única (96.8 frente a 96.9), las líneas base (voto y vecinos al nivel del sistema en texto; 652–655 de 656 en imagen, sin rechazo), «lo que la memoria agrega es rechazar sin un umbral ajustado y devolver el contenido asociado», las dos condiciones (−7.5 sin B1; 70.4 % y 169 falsos sin la pérdida de clase), el directorio que reproduce sin mejorar, y 89.3 % con 33 de 984 falsos `[PENDIENTE: pliegues 10/10]`.
- Se conservan de 9.1 los dos procesos de Wegner, la especialización asignada, «vistas nuevas de objetos conocidos», la compuerta decidida después y la lesión (64 de 800).

**E2. La pregunta** (`01:29-38`). Este es el texto nuevo:
```latex
Este trabajo pregunta si la organización que describe Wegner puede construirse con
estas memorias y qué agregan ellas a las decisiones del sistema:

\begin{quote}
¿Puede un sistema de memoria transactiva construido sobre memorias asociativas
entrópicas repartir consultas de texto e imagen entre ocho especialistas, recordar el
contenido asociado y rechazar lo que no conoce, sin clasificadores discriminativos en
las decisiones de enrutamiento y rechazo? ¿Qué agrega la memoria asociativa frente a
decisores simples que usan las mismas representaciones? Y donde aparezcan límites,
¿provienen del mecanismo asociativo o de las representaciones que lo alimentan?
\end{quote}
```
La pregunta es tuya, así que agregar la pregunta del medio lo decides tú. Te recomiendo agregarla: es lo que preguntará la defensa, y la tesis ya tiene con qué contestarla. Sin ella, se aplica estructura 3.1 tal cual.

**E3. Contribuciones** (`01:69-114`). Son seis:
1. Sistema de ocho especialistas con decisiones legibles: una pista se acepta solo si está registrada en el módulo, y el enrutamiento suma transacciones registradas, normalizadas por conteo.
2. Cuantización por magnitud, igual que hoy.
3. Directorios perspectivales, más lo que el directorio sí logra: reproducir la decisión temprana sin consultar a los ocho.
4. Frente a una EHAM única: misma clase (96.8 frente a 96.9), recuerdo más fiel (27.0 frente a 32.5) `[PENDIENTE: exp11 d_nn]`, y 2 frente a 8 de 40 fuera de dominio.
5. Familiaridad y nombre de una sola memoria.
6. Nueva: qué agrega la memoria, medido contra decisores simples, más la evaluación fija y el codificador sin pérdida de clase, junto con el resto de la evaluación.

**E4. Apertura de 6.1** (`06:5-24`). El título pasa a «El mecanismo transactivo funciona con ocho dominios; la clase la decide la representación». El párrafo que lo justifica:
```latex
Qué clase recibe cada consulta, en cambio, lo decide sobre todo la representación.
Con los mismos vectores y otros decisores, \texttt{pear} sigue siendo la clase difícil
en las 400 consultas de la calibración.
Un centroide la acierta el 8.0\,\% de las veces, los cinco vecinos más cercanos entre
el 62 y el 63\,\% y el vecino más cercano entre el 67 y el 71\,\%, frente al 70.0\,\% de
la fase temprana y al 76\,\% de la lectura normalizada (Sección~\ref{sec:lineas-base}).
[…]
Con un codificador entrenado sin la pérdida de clase y el mismo mecanismo, el
enrutamiento visual baja del 96.2 al 70.4\,\% y los falsos enrutamientos suben de 2 a
169 de 656 (Sección~\ref{sec:codificador-sin-clase}).

El mecanismo tiene también límites propios.
La lectura del directorio necesita una normalización externa
(Sección~\ref{sec:disc-b1}); la contención estricta por coordenada rechaza 23 imágenes
de prueba que un vecino más cercano sobre los mismos latentes clasifica bien
(Sección~\ref{sec:disc-lineas-base}); el nombre se pierde con un daño del 1\,\%
(limitación (j)), y el contenido visual da soporte a entradas sin estructura
(limitación (c)).
```
Para ser honesto: una tabla de conteos formada con las mismas 400 consultas acierta `pear` en el 82 %. No lo pongo en el texto porque compararía dos cifras dentro de muestra.

**E5. Subsección nueva de 06:** «Qué agrega la memoria asociativa frente a decisores simples» (`sec:disc-lineas-base`). Va después de `06:203`, antes de Limitaciones. Tiene cinco párrafos con título:
- **«En la clase, no agrega».** Proto80: 79.4 y 81.5 contra 81.2. La compuerta es igual a la pertenencia al vocabulario en 3064 pares. El voto por frecuencia toma la misma decisión que la fase temprana en 380/400. Tabla de conteos contra directorio: 92.3 contra 93.0, p = 0.58. En imagen: 652–655 contra 631, y las 23 rechazadas las clasifica bien el 1-NN.
- **«Agrega rechazo sin un umbral ajustado».** Rechaza 40 de 40 de lo que aceptan los decisores sin umbral. AUROC de 0.97 a 0.99, pero el umbral que no pierde reservadas deja pasar de 9 a 23. Dice que en texto este rechazo vale lo que una búsqueda léxica, y que su ventaja aparece frente a un almacén único (2 frente a 2–8), con `clark1996global`. Sin fotos reales de fuera de dominio.
- **«Agrega recuerdo».** d_nn `[PENDIENTE: exp11 d_nn]`, 97.4 contra un azar de 34.8, y 80 de 81 bien enrutadas con el codificador sin clase.
- **«Lo sostienen dos condiciones externas al mecanismo asociativo».** B1 (+4.5 a +8.8; −7.5 sin ella). Separación por coordenada (sonda 94.2 %, mediana 5.34 contra 0.24, 0.5 contra 82.9 %), con `yassa2011pattern` y `goldstone1994influences`.
- **«El directorio localiza; no decide mejor».** Concordancia 92.5 %, +0.2 y +1.3, con `wegner1995computer`, `sparrow2011google` y `ren2006contingent`.

Cierra con «la clase la deciden las representaciones» y con el aviso de que las analogías son estructurales, no causales.

**E6. Apertura de 07** (`07:8-10`). Es estructura 7.5 más «de la que depende el enrutamiento visual».

**E7. Resultados principales** (`07:12-32`). Agrega la evaluación fija (+0.2 y +1.3; la cruda queda −7.5), 96.8 con la composición de las reservadas, «vistas nuevas de objetos conocidos», el azar de 34.8, el codificador por pliegue (89.3 %, 33 de 984) `[PENDIENTE: pliegues 10/10]` y una frase de líneas base.

**E8. Respuesta a la pregunta** (`07:34-52`). Responde en tres párrafos, uno por parte:
- **Sí, se puede**, con lo que no sale de las memorias y el alcance del rechazo.
- **Frente a decisores simples, no agrega clase.** Agrega rechazo sin umbral, recuerdo, rechazo que no empeora con el contenido y decisiones legibles.
- **Los límites vienen de las dos partes.** La clase la decide la representación (`pear` es difícil para todos los decisores; 70.4 % sin la pérdida de clase). El mecanismo necesita B1, su contención estricta cuesta cobertura, el nombre es frágil y el contenido acepta entradas degeneradas. El directorio es un índice. Cierra con `watkins1975buildup`.

**E9. Frente a una EHAM única** (`07:54-63`). Clase igual (96.8 frente a 96.9; con N = 25, 93.2 frente a 97.6). Fidelidad, 79–84 % y dominio ajeno 3.0 frente a 10.9 `[PENDIENTE: exp11 d_nn]`. Fuera de dominio 2 frente a 2–8, p = 0.031, con la compuerta decidida después. Cobertura 81.2 frente a 100, y 3.2 puntos frente al oráculo.

**E10. Trabajo futuro, punto nuevo:** rechazo con fotografías reales de otras categorías y con un banco de consultas escrito por terceros.

**E11. Cierre** (`07:106-110`):
```latex
En resumen, las Memorias Asociativas Entrópicas de Pineda y Morales bastan para
construir un sistema distribuido de memoria transactiva de ocho especialistas,
bidireccional y con rechazo explícito, sin clasificadores discriminativos en las
decisiones de enrutamiento y rechazo.
Frente a decisores simples sobre las mismas representaciones, no clasifican mejor; lo
que aportan es un rechazo que no necesita umbral ajustado, el recuerdo del contenido
asociado y decisiones que se leen en sus registros.
La clase la deciden las representaciones, y el mecanismo necesita dos cosas que no
salen de él: la normalización por conteo del directorio y un código en que cada
coordenada separe las clases.
```

## Cruces con la propuesta de estructura

| Estructura | Pasaje | Aquí | Qué pasa |
|---|---|---|---|
| 1.1 | `main:74-76` | E1 | Incorpora |
| 3.1 | `01:32-38` | E2 | Incorpora y amplía con la segunda pregunta |
| 3.2 | `01:55-60` | — | Lo deja igual; E2 quita «solo» en `01:29` para que no choque |
| 3.3, limitación (k) | después de `06:336` | — | Lo deja igual y llena sus marcadores: 70.4 % y 59.3 %, y sugiere agregar «2 → 169 falsos» |
| 3.4 | cuatro menciones de «supervisados» | E1, E6, E8, E11 | Incorpora |
| 4.4 | `06:78-120` | — | Lo deja igual y llena su marcador de calibración fija (texto en el archivo) |
| 7.1 | `06:5`, `06:8-12` | E4 | Reemplaza; conserva sus límites del mecanismo y aplica su propia regla de título |
| 7.3 | `06:178-182` | E5 (borde) | Lo deja igual |
| 7.5 | `07:8-10` | E6 | Incorpora |
| 7.6 | `07:34-52` | E8 | Reemplaza; conserva las salvedades y la cita de Watkins, y llena sus marcadores |
| 7.7 | `07:55-57` | E9 | Incorpora «mezcla menos» y «con 200 imágenes por clase» |
| 7.8 | `07:106-110` | E11 | Reemplaza |
| 9.1 | `main:57-104` | E1 | Reemplaza; incorpora casi todo y cambia lo indicado en E1 |
| 9.2 | `01:69-114` | E3 | Reemplaza; conserva la estructura de seis y cambia 1, 3, 4 y 6 |
| 9.3 | `07:17-18`, `07:21-22` | E7 | Incorpora, con 96.8 |
| 9.4, 6.3, 1.2, 1.6, 4.5, 8.2 | — | — | Los deja igual |

**Bordes con la propuesta de metodología:**
- M1.6 (`07:58-63`): E9 la reemplaza.
- M2.9 y Me.2: E7 los incorpora.
- M4.1: su marcador pasa a `[PENDIENTE: pliegues 10/10]`.
- M1.4: sus cifras del protocolo deben pasar a las corregidas (−0.1, p = 0.86; 3.2 puntos).

## Marcadores pendientes

| Marcador | Depende de | Dónde | Cuántos |
|---|---|---|---|
| `[PENDIENTE: exp11 d_nn]` | la corrida completa de exp11 con recuerdo (d_nn, dominio ajeno, F y el 79–84 %) | E1, E3 (contribución 4), E5 (párrafo «Agrega recuerdo»), E9 | 4 |
| `[PENDIENTE: pliegues 10/10]` | exp16 con el codificador por pliegue, hoy en 3 de 10 | E1, E7 | 2 |

**Efecto en los marcadores de las otras propuestas:**
- De los 24 `[PENDIENTE: exp11 corregido]`, los de enrutamiento, clase, cobertura y fuera de dominio ya se pueden llenar con `ruteo.md`. Los que tocan el recuerdo pasan a `exp11 d_nn`.
- `líneas base`, `calibración con conjunto fijo` y `codificador sin pérdida de clase` quedan llenos con las cifras de arriba.

Sources:
- [Yassa y Stark 2011, PubMed](https://pubmed.ncbi.nlm.nih.gov/21788086)
- [Yassa y Stark 2011, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3183227)
- [Goldstone 1994, página del autor](https://pcl.sitehost.iu.edu/rgoldsto/catdiscrim.html)
- [Goldstone 1994, laboratorio](https://pc.cogs.indiana.edu/?p=115)
- [Foundations of Metacognition, mención secundaria de Glucksberg y McCloskey; no usada](https://academic.oup.com/book/11865/chapter/160994966)
