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

Los objetos más parecidos en el latente no comparten la característica: todo queda en el azar. Con el color, la misma sonda dio 41 % con azar 12.5 %. El MAE de 64 dimensiones separa los objetos por forma, pose y color, pero no codifica de forma compartida si un animal tiene manchas, si un perro tiene pelo rizado o si un auto es descapotable. Ninguna lectura de la memoria puede sacar lo que el latente no trae.

## Lectura

- Que la heteroasociación sea significativa es necesario, pero no basta. Con etiquetas verdaderas la memoria las asocia en los objetos que vio (normalizado: balanceada 63–72 %), pero no las abstrae a objetos nuevos.
- Pasa lo mismo que con el color minoritario en exp17, y la sonda lo explica: el límite está en el latente, no en la memoria.
- En objetos nuevos el fallo es confusión sin rechazo. El contenido reconoce el 93–96 % de las vistas y responde el valor común.
- Para una palabra específica que generalice (el «nódulo» de un paciente nuevo) hace falta un latente que codifique esa característica de forma compartida entre instancias: un encoder entrenado o ajustado para eso, o rasgos locales en vez de un vector global. Hay que medirlo antes con esta misma sonda.

## Archivos

- `run_experiment18_attributes.py` (en la raíz de la copia; reanuda desde `filas.json`)
- `caracteristicas_borrador.json` (etiquetas aprobadas), `attribute_vectors.json` (fastText crudo)
- `filas.json` (filas por imagen de los 58 pliegues), `resumen.txt`, `run.log`
- `modelos/`: memorias del pliegue 0, fuera de git
