# Experimento 18 — heteroasociación con características visibles

Corre en la copia `MAE-TMS-exp18` (rama `exp18-heteroasociacion-significativa`); el pipeline oficial no se toca.

Pregunta: si cada imagen se heteroasocia con una característica que de verdad tiene (no con la siguiente palabra de la lista de la clase), ¿la memoria devuelve la característica correcta, también en objetos que nunca vio?

Diseño: una memoria hetero por eje y clase. Etiquetas a mano por objeto (`caracteristicas_borrador.json`, aprobado el 17 oct 2026); solo objetos claros en cada eje.
- **patrón** (plain / spotted / decorated): cow, horse, dog, cup
- **techo** (convertible / hardtop): car
- **pelo** (curly / smooth): dog

El color se midió en exp17 con el mismo procedimiento. Las palabras de cada eje se separan bien en fastText (coseno 0.39–0.65, contra 0.93 de white–black). Se usan los latentes de exp16, 200 vistas × 16 variantes por memoria, y la evaluación es en el agente de la clase verdadera. Pliegue 0: 41 vistas nuevas de objetos conocidos. Leave-object-out **completo**: un pliegue por objeto claro, 52 pliegues. Lecturas: soporte y soporte normalizado por la marginal (exp17), reportadas las dos.

## Objetos conocidos (vistas nuevas)

| eje | soporte (bal.) | normalizado (bal.) | base |
|---|---|---|---|
| patrón | 73.8 (44.0) | 68.3 (**62.7**) | 68.9 |
| pelo | 70.7 (50.0) | 78.0 (**72.3**) | 70.7 |
| techo | 74.4 (50.0) | 56.4 (**64.1**) | 74.4 |

El soporte sin normalizar coincide con la base: responde el valor mayoritario. El normalizado separa algo: la balanceada queda entre 63 y 72 %, con azar en 33–50 %.

## Objetos nuevos (leave-object-out)

| eje | soporte | normalizado | base | valor mayoritario: soporte / norm | valor minoritario: soporte / norm |
|---|---|---|---|---|---|
| patrón | 64.2 (bal. 29.9) | 58.9 (bal. 32.9) | 63.1 | 98.7 / 68.6 | 5.6 / 46.1 |
| pelo | 64.8 (bal. 52.1) | 57.5 (bal. 48.6) | 63.8 | 98.0 / 80.6 | 6.1 / 16.7 |
| techo | 66.6 (bal. 49.8) | 39.1 (bal. 42.5) | 67.1 | 98.7 / 32.5 | 0.9 / 52.6 |

«Mayoritario» y «minoritario» se refieren al valor del objeto nuevo frente a los del agente. Los porcentajes por grupo excluyen el caso imposible: dog6, el único perro manchado.

- **Soporte:** es la base exacta. Dice el valor mayoritario en el 98–99 % de las vistas y acierta el minoritario en 1–6 %.
- **Normalizado:** reparte los errores en vez de quitarlos. La balanceada queda en el azar o por debajo (patrón 32.9 con azar 33, pelo 48.6 y techo 42.5 con azar 50).
- **cow** es la prueba más limpia, porque tiene 4 objetos manchados y 4 lisos: al sacar cualquiera, la mayoría pasa al otro valor. Con soporte acierta el 8 % de las vistas, es decir, dice sistemáticamente lo contrario. Con normalizado acierta los lisos (151/163) y falla los manchados (29/151).

Objeto por objeto: `resumen.txt`.

## Por qué: el latente no lleva estas características entre objetos

Sonda de vecinos (k = 5, leave-object-out dentro de la clase, latente continuo):

| eje · clase | balanceada | azar |
|---|---|---|
| techo · car | 42.5 | 50 |
| patrón · cow | 54.9 | 50 |
| patrón · cup | 39.0 | 50 |
| patrón · dog | 45.9 | 50 |
| patrón · horse | 45.0 | 50 |
| pelo · dog | 42.9 | 50 |

Los objetos más parecidos en el latente no comparten la característica: todo queda en el azar. Con el color, la misma sonda dio 41 % con azar 12.5 %. El encoder del proyecto (latente de 64 dimensiones) separa los objetos por forma, pose y color, pero no codifica de forma compartida si un animal tiene manchas, si un perro tiene pelo rizado o si un auto es descapotable. Ninguna lectura de la memoria puede sacar lo que el latente no trae.

## Lectura

- Que la heteroasociación sea significativa es necesario, pero no basta. Con etiquetas verdaderas la memoria las asocia en los objetos que vio (normalizado: balanceada 63–72 %), pero no las abstrae a objetos nuevos.
- Pasa lo mismo que con el color minoritario en exp17. Con el encoder propio la sonda lo explica, porque el latente no trae la característica; la sección de diagnóstico muestra que, aun con rasgos que sí la traen, la memoria tampoco la generaliza del todo.
- En objetos nuevos el fallo es confusión sin rechazo. El contenido reconoce el 93–96 % de las vistas y responde el valor común.
- Para una palabra específica que generalice (el «nódulo» de un paciente nuevo) hacen falta dos cosas: un latente que codifique esa característica de forma compartida entre instancias, y una lectura que generalice por similitud en vez de exigir soporte en cada coordenada.

## Diagnóstico con otros rasgos: ¿es el encoder o es la memoria?

El encoder del proyecto parte de ResNet18 de ImageNet y se ajusta con reconstrucción + 0.1 × clasificación de clase. Se comparan con la misma sonda tres rasgos de la vista original: el latente propio (64), ResNet18 de ImageNet **sin** ese ajuste (512, y reducido a 64 con PCA sin etiquetas) y DINOv2-small (384, y a 64). Son solo un diagnóstico; no entran al pipeline oficial. Detalle en `sonda_rasgos_resumen.txt`.

| eje · clase | azar | propio | ResNet18-IN (64) | DINOv2 (64) |
|---|---|---|---|---|
| color · apple | 50 | 36.6 | 87.6 | 94.7 |
| patrón · cow | 50 | 63.7 | 91.2 | 98.5 |
| pelo · dog | 50 | 35.0 | 84.1 | 62.4 |
| color · horse | 33 | 60.2 | 61.0 | 75.6 |
| techo · car | 50 | 38.2 | 46.3 | 56.3 |
| patrón · dog / horse / cup | 50 | 47 / 41 / 40 | 48 / 47 / 51 | 50 / 50 / 57 |

(Esta sonda usa coseno; la de arriba usaba distancia euclidiana, por eso el propio cambia algo.)

- Con el mismo backbone sin nuestro ajuste, las características aparecen: el ajuste del encoder borra lo que varía dentro de la clase. No es la pérdida de clase: un encoder reentrenado sin ella (exp19, `results/experimento19`) recupera el color de apple (72.2) pero no las manchas de cow (53.7) ni el pelo de dog (23.3). Lo que las borra es comprimir a 64 dimensiones con reconstrucción MSE.
- Donde ningún rasgo sale del azar, hay 1–2 objetos minoritarios: el límite son los datos.

Después se repitió la memoria con los latentes de ResNet18-IN reducidos a 64, con las 16 variantes de cada vista y estadísticas min/max de las originales con margen del 10 %. Se usaron los casos donde la sonda pasa, con leave-object-out completo (33 pliegues), y el mismo protocolo con el encoder propio como control (`filas_resnet18_in.json`, `filas_propio_color.json`). Acierto balanceado con soporte normalizado; «reconoce» es la fracción de vistas nuevas que el contenido acepta.

| eje · clase | azar | kNN propio | kNN ResNet18-IN | memoria propio | memoria ResNet18-IN | reconoce propio / ResNet |
|---|---|---|---|---|---|---|
| color · apple | 50 | 36.6 | 87.6 | 39.6 | 55.2 | 75 / 63 % |
| color · horse | 33 | 60.2 | 61.0 | 39.6 | 38.1 | 95 / 80 % |
| patrón · cow | 50 | 63.7 | 91.2 | 55.9 | 59.0 | 96 / 76 % |
| pelo · dog | 50 | 35.0 | 84.1 | 48.6 | 65.9 | 96 / 68 % |

En objetos conocidos (vistas nuevas) la memoria con ResNet18-IN sí mejora mucho: cow 64.6 → 85.6, dog 72.3 → 96.3, apple 92.9 → 100; horse 80.3 → 74.2.

Lectura:
- **Hay dos cuellos de botella, no uno.** El encoder propio borra las características. Pero con rasgos que sí las traen, la memoria las aprovecha para los objetos que vio y **no las generaliza** como un vecino más cercano sobre esos mismos rasgos: cow queda en 59 contra 91 del kNN y dog en 66 contra 84.
- La causa probable es cómo reconoce la memoria: una conjunción de soportes por coordenada sobre valores cuantizados. Un objeto nuevo cae en celdas que el llenado no cubrió, y entonces la memoria lo rechaza (con ResNet rechaza el 20–37 % de las vistas nuevas) o responde lo que dicta la marginal. Un kNN compara por similitud global y no tiene ese problema.
- Para la aportación: el cálculo de pesos de la memoria funciona como **reconocimiento con rechazo**, no como generalización por similitud. Con mejores rasgos mejora la parte de memoria (objetos vistos), pero transferir un atributo a un objeto nuevo sigue requiriendo algo que la memoria no hace.

## Lectura tolerante: ¿se cierra la brecha con el kNN sin salir de la MAE?

`project()` integra con un AND sobre las 64 coordenadas latentes: si una coordenada del objeto nuevo cae en un nivel que nunca coincidió con cierto valor de etiqueta, esa celda queda en cero. La lectura tolerante usa la misma integración, pero cada coordenada aporta la suma de su nivel y los vecinos a distancia ≤ r. Los pesos de la homo llevan la misma tolerancia y no se rellena nada. Radios fijados antes de correr: r = 1 como lectura principal, r = 2 como sensibilidad. Con r = 0 coincide exactamente con `project()`. Leave-object-out completo, mismos 4 casos, soporte normalizado (`filas_tol_resnet18_in.json`, `filas_tol_propio.json`).

| caso | ResNet18-IN r=0 | **r=1** | r=2 | kNN mismos rasgos | reconoce r=0 → r=1 → r=2 |
|---|---|---|---|---|---|
| color · apple | 55.2 | **63.7** | 76.1 | 87.6 | 63 → 90 → 99 % |
| color · horse | 38.1 | **41.8** | 46.1 | 61.0 | 80 → 95 → 99 % |
| patrón · cow | 59.0 | **58.2** | 62.6 | 91.2 | 76 → 86 → 90 % |
| pelo · dog | 65.9 | **70.6** | 71.6 | 84.1 | 68 → 85 → 94 % |

Con el encoder propio la tolerancia no cambia casi nada (r = 1: cow 55.6, dog 46.7, apple 41.9, horse 29.9).

- La tolerancia sobre todo **baja el rechazo**: las vistas nuevas vuelven a caber en la envolvente.
- La transferencia del atributo mejora poco (apple +8, dog +5 con r = 1) y en cow, la prueba más limpia (4 contra 4 objetos), nada. Sigue lejos del kNN.
- Que el objeto nuevo quepa no basta: dentro del dominio, el valor del atributo lo sigue decidiendo la masa de lo registrado. La lectura por soporte compara cuánto se registró de cada valor en las celdas del objeto, no a qué objetos vistos se parece.

## Archivos

- `run_experiment18_attributes.py` (en la raíz de la copia; reanuda desde `filas.json`; `EXP18_LAT`, `EXP18_STATS`, `EXP18_RAW` y `EXP18_CASES` para otros rasgos)
- `run_experiment18_feature_probe.py` (sonda de rasgos; `--variantes` genera los latentes de ResNet18-IN)
- `sonda_rasgos_resumen.txt`, `sonda_rasgos.json`; `filas_resnet18_in.json`, `filas_propio_color.json` y sus `resumen_*.txt`
- `rasgos/`: rasgos y latentes externos, fuera de git
- `caracteristicas_borrador.json` (etiquetas aprobadas), `attribute_vectors.json` (fastText crudo)
- `filas.json` (filas por imagen de los 58 pliegues), `resumen.txt`, `run.log`
- `modelos/`: memorias del pliegue 0, fuera de git
