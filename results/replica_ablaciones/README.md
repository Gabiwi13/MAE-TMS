# Réplica y ablaciones del diseño congelado

El diseño que cumplió el criterio en la etapa 2 (entrada por receptor, ruteo dirigido R3 con ξ = 1) se congeló y se probó de dos maneras. Primero, con 10 semillas en la flota de VisA y en una flota médica nueva que nunca se usó para diseñar. Segundo, con ablaciones para ver qué componente carga el resultado. Diseño, predicciones y criterio fijados antes de correr en [`propuesta_replica_ablaciones.md`](../../propuesta_replica_ablaciones.md). Las predicciones salen del [modelo formal](../revision_cientifica/modelo_formal.md). Script: [`run_replica_ablaciones.py`](../../run_replica_ablaciones.py).

**Resultado en una línea:** en VisA el resultado **se replica** (74.5 % al mejor módulo, a 2.7 puntos del router central), pero **una tabla de conteos simple lo hace mejor** (87.8 % al mejor), y una tasa global por módulo, mejor aún (89.1 %). En la flota médica nueva **no se replica**: R3 queda 13.3 puntos bajo el router central y elige al peor módulo con la misma frecuencia que el azar. La memoria de directorio **no aporta como mecanismo de decisión**. Lo que sí aporta la MAE es **reconocer el dominio por contenido**: con eso, contar éxitos entre los candidatos que reconoce el contenido rinde mejor que R3 en las dos flotas.

## Flotas

- **VisA:** 12 piezas × 2 redes especializadas (la base y la más débil según la mitad de aprendizaje). Mejor módulo fijo por dominio: 92.0 % de acierto.
- **MedMNIST (nueva):** 4 modalidades × 3 módulos reales del demo médico (la cabeza entrenada, kNN y la memoria de nivel 2), hasta 600 consultas por modalidad. El peor módulo queda ≥ 5 puntos bajo el mejor en tórax y piel. Mejor módulo fijo: 70.6 %. Desconocidas: 400 imágenes de retina.

## Resultados (media de 10 semillas [IC 95 % por bootstrap])

**VisA:**

| lectura | acierto | pérdida vs mejor fijo | abst. conocidas | abst. desconocidas | costo | al mejor |
|---|---|---|---|---|---|---|
| **R3** (diseño congelado) | 86.3 [85.7, 86.8] | 5.7 | 3.9 | 100 | 2.4 | **74.5** [71.0, 78.2] |
| TAB: tabla de conteos, sin filtro | 87.4 [87.0, 87.9] | 4.6 | 0.0 | **0.0** | 1.0 | 87.8 [83.8, 91.8] |
| PROPIO: solo el directorio propio | 86.3 [85.8, 86.8] | 5.7 | 4.0 | 100 | 2.8 | 75.6 [72.6, 79.0] |
| GLOBAL: tasa global por módulo | 87.4 [86.8, 88.0] | 4.6 | 4.1 | 100 | — | **89.1** [84.8, 94.2] |
| *TAB entre candidatos (posterior)* | *87.1 [86.7, 87.6]* | *4.8* | *4.1* | *100* | *2.0* | *87.8 [83.7, 91.9]* |
| router central kNN | **89.0** [88.3, 89.7] | 3.0 | 1.1 | 100 | — | 72.7 [69.4, 75.8] |
| azar entre candidatos | 83.0 [82.3, 83.7] | 9.0 | 4.1 | 100 | — | 50.7 |

R3 − TAB en «al mejor»: **−13.3 [−16.2, −10.1]**. R3 − GLOBAL: **−14.7 [−19.1, −11.2]**. R3 − PROPIO: −1.1 [−1.9, −0.5]. Router central − R3 en acierto: 2.7 [2.1, 3.2].

**MedMNIST (nueva):**

| lectura | acierto | pérdida vs mejor fijo | abst. conocidas | abst. desconocidas | costo | al peor (azar 33 %) |
|---|---|---|---|---|---|---|
| **R3** | 54.7 [54.2, 55.2] | 15.9 | 3.0 | 5.0 | 12.9 | **30.0** [24.3, 36.6] |
| TAB, sin filtro | 24.1 [22.0, 26.5] | 46.5 | 0.0 | 0.0 | 1.0 | 8.1 |
| PROPIO | 60.0 [59.3, 60.6] | 10.6 | 3.1 | 5.0 | 16.7 | 17.3 |
| GLOBAL | 55.8 [54.7, 57.0] | 14.8 | 3.1 | 5.0 | — | 10.0 |
| *TAB entre candidatos (posterior)* | *62.3 [61.2, 63.3]* | *8.3* | *3.1* | *5.0* | *1.7* | ***5.8*** [1.6, 10.6] |
| router central kNN | **68.0** [67.6, 68.4] | 2.7 | 1.7 | 2.3 | — | 22.3 |
| azar entre candidatos | 55.9 [55.3, 56.6] | 14.7 | 3.1 | 5.0 | — | 33.6 |

Router central − R3: **13.3 [12.7, 13.9]**. R3 − TAB entre candidatos, en pérdida: −7.6 puntos (posterior).

**Diagnóstico de la flota médica** (hecho al ver el 24 % de TAB): el contenido de nivel 1 médico **no separa bien las modalidades**. Una imagen de órganos también cabe en la envolvente de piel, así que el receptor a veces es de otro dominio. TAB, que ignora la pista, manda casi todas las consultas de órganos a piel (283 de 300 en la semilla 0). R3 las manda a su dominio (284 de 300), pero eligiendo mal el módulo dentro del dominio. Lo mismo explica la abstención casi nula ante la retina (5 %), como ya mostró el exp20 en el demo médico (de 6 a 24 %).

## Predicciones y criterio

| | predicción | resultado |
|---|---|---|
| PF1 | TAB rinde igual que R3 | **Refutada en contra de la memoria**: TAB es 13 puntos **mejor** en VisA. En MedMNIST, TAB sin filtro es mucho peor, porque no condiciona en la pista; restringida a los candidatos, es mejor que R3 |
| PF2 | GLOBAL igual o mejor que R3 | **Se cumple**: mejor en VisA (+14.7) y en MedMNIST (al peor: 10.0 contra 30.0) |
| PF3 | PROPIO igual que R3 | **Se cumple en VisA** (−1.1). En MedMNIST PROPIO es mejor que R3 (pérdida 10.6 contra 15.9): los conocidos introducen módulos de otros dominios |
| PF4 | el núcleo solo aportaría con heterogeneidad de calidad dentro del dominio | Hay heterogeneidad (el mejor módulo global pierde por ≥ 5 puntos en alguna clase en 2.2 de 12 dominios de VisA y en 2.2 de 4 de MedMNIST), **pero el núcleo no la aprovecha**: R3 queda por debajo de los contadores |
| PF5 | en MedMNIST, R3 evita al peor (< 33 %) | **No se cumple**: 30.0 [24.3, 36.6], el intervalo incluye el azar |

**Criterio «la memoria de directorio aporta como mecanismo de decisión»:** **refutado** en las dos flotas. R3 queda por debajo de la tabla de conteos y de la tasa global por 13 a 15 puntos en «al mejor» (VisA) y por 7.6 puntos en pérdida frente a la tabla entre candidatos (MedMNIST).

**Criterio «el resultado de la etapa 2 se replica»:** **sostenido en VisA** (74.5 % al mejor con límite inferior 71.0; 2.7 puntos del central). **Refutado en MedMNIST** (13.3 puntos del central; al peor en el azar).

## Lectura

1. **El modelo formal acertó en lo esencial y se quedó corto en una cosa.** Predijo que, con entrada por receptor, la decisión se reduce a contar éxitos por dominio. Pero no predijo que la memoria de directorio cuente **peor** que una tabla. La causa probable está en la Proposición 2: el filtro de soporte anula la proyección de un módulo en cuanto una sola coordenada no tiene conteos para él, y eso favorece al módulo que **cubre** más el espacio, no al que **acierta** más. Es una hipótesis que no se probó aquí.
2. **Lo que aporta la MAE es el contenido, no el directorio.** Reconocer el dominio por contenido da el receptor, la abstención ante lo desconocido (100 % en VisA) y el filtro de candidatos que hace funcionar a la tabla de conteos (TAB entre candidatos). Donde el contenido no separa los dominios (nivel 1 médico), todo el sistema se degrada, y ningún mecanismo de directorio lo compensa.
3. **El resultado de la etapa 2 era frágil, como sospechamos.** Se replica con semillas en la flota donde se diseñó, pero no en una flota nueva. Es la confirmación del riesgo del jardín de caminos que se bifurcan: la quinta configuración probada sobre los mismos datos se ajustó a esos datos.

## Notas

- «TAB entre candidatos» se agregó después de ver el resultado de TAB en la semilla 0 de MedMNIST, para separar el efecto del filtro por contenido del efecto del núcleo. Está marcada como posterior en todas las tablas.
- Las pistas médicas no tienen variantes (el demo no las guardó para el test), así que cada transacción registra una pista en vez de 16.
- En MedMNIST, la «memoria» como módulo cuenta su rechazo como error; por eso es el peor módulo en tórax y piel.
