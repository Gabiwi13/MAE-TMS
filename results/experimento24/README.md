# Experimento 24 — pruebas duras contra las opciones actuales

Objetivo: no partir de que el sistema es mejor. Se buscan las propiedades donde podría ganar y se lo pone contra los mejores rivales actuales en esas propiedades, sobre los mismos rasgos y los mismos registros. El panorama de rivales se revisó en la literatura 2016–2026. Las memorias asociativas acopladas a LLMs (Larimar, CAMELoT, MemoryLLM, Titans, kNN-LM, Memorizing Transformers) son de texto y no se han evaluado en imagen ni en clasificación con rechazo, así que quedan como referencia conceptual. Los rivales numéricos justos son las memorias asociativas modernas (Hopfield moderno), hyperdimensional computing, los métodos incrementales con rasgos congelados (SimpleCIL/NCM, RanPAC), la predicción conformal por clase y los detectores fuera de distribución. Las predicciones y los criterios se fijaron antes de correr.

## A. Cobertura de clases raras: memoria contra conformal por clase (Mondrian)

Exp23 mostró que, a igual cobertura total, la lista de la memoria cubre los hallazgos raros de tórax de 2 a 4 veces más que el conformal marginal. Aquí se la compara con el conformal por clase (Mondrian: un cuantil por clase, calibrado con el split de validación), con alfa elegido para igualar la cobertura total de la memoria. Script `run_experiment24_mondrian.py`; detalle en `mondrian_resumen.txt`.

| nivel | memoria: tamaño / peor clase | conformal marginal | **Mondrian** |
|---|---|---|---|
| tórax (14) | 8.74 / 27.1 | 5.31 / 6.8 | 10.61 / **88.0** |
| piel (7) | 1.52 / 34.5 | 1.25 / 66.7 | 1.80 / **84.5** |
| órganos (11) | 1.01 / 82.9 | 0.97 / 86.4 | 1.97 / **85.1** |
| mama (2) | 1.21 / 85.7 | 1.03 / 78.6 | **1.08 / 89.5** |

Mondrian cubre en tórax neumonía 100 %, fibrosis 90 % y consolidación 93 %, con listas algo más largas. **La ventaja en clases raras desaparece frente al estado del arte.** La memoria queda entre el conformal marginal y Mondrian. Lo único que conserva es que no necesita conjunto de calibración (Mondrian funcionó con solo 12 casos de validación de dermatofibroma).

## B. Aprendizaje incremental por clases

OrganAMNIST, 11 órganos en 4 tareas (3+3+3+2). Rasgos congelados del nivel 1 (ResNet18 de ImageNet + PCA a 64; la PCA vio imágenes de órganos sin etiquetas). Todos los métodos reciben los mismos 328 registros por clase con 16 variantes. Script `run_experiment24_incremental.py`; detalle en `incremental_resumen.txt` e `incremental.json`.

| método | acierto final | medio | olvido | AURC (↓) | cobertura | bytes |
|---|---|---|---|---|---|---|
| memoria (contención + principio de tamaño) | 35.9 | 38.3 | 15.5 | 41.34 | 98.0 | 90 112 |
| NCM / SimpleCIL | 75.6 | 72.6 | 9.5 | 7.48 | 100 | 2 816 |
| HDC (10 000 bits) | 75.9 | 73.5 | 9.7 | 7.51 | 100 | 190 000 |
| Hopfield moderno | 78.2 | 75.6 | 7.0 | 5.56 | 100 | 14.8 M |
| kNN | 82.4 | 79.8 | 4.5 | 6.58 | 100 | 14.8 M |
| RanPAC | **86.4** | **85.7** | 5.4 | **2.67** | 100 | 32.7 M |
| lineal sin repaso | 23.9 | 51.7 | 82.8 | 64.79 | 100 | 2 860 |
| lineal con repaso (20 por clase) | 29.6 | 54.2 | 76.7 | 57.25 | 100 | 59 180 |

Sensibilidad (`sensibilidad.txt`; declarada como tal, no reemplaza lo anterior):

| acierto final | memoria, tamaño | memoria, regla oficial (el que reconoce con más fuerza) | NCM | kNN | RanPAC |
|---|---|---|---|---|---|
| rasgos genéricos | 35.9 | 65.4 | 75.6 | 82.4 | 86.4 |
| rasgos ajustados a los 11 órganos | 93.1 | 93.3 | **97.0** | 96.8 | **97.0** |

Predicciones: *la memoria no olvida, como NCM, HDC, Hopfield y kNN* — **no se cumple del todo**. Sus especialistas viejos no cambian, pero cada clase nueva agrega un contenedor que compite (olvido 15.5, mayor que el de NCM). *Menor acierto que kNN y RanPAC* — **se cumple, y el margen es mayor del esperado**: queda también por debajo de NCM y HDC. *Posible ventaja en abstención y en tamaño fijo* — **no se cumple**: su AURC es el peor después de los lineales que olvidan, y NCM ocupa 32 veces menos.

## Lectura

- **Sobre los mismos rasgos, la memoria no supera a ninguna opción actual en ninguna de las propiedades medidas:** exactitud, olvido, abstención (AURC), cobertura de clases raras (Mondrian) ni tamaño (NCM). El rival más simple, un prototipo medio por clase, también se llena sin gradiente, agrega clases sin reentrenar y es igual de interpretable, y le gana por unos 4 puntos con buenos rasgos y por 10 con rasgos genéricos.
- **El principio de tamaño tiene un límite nuevo:** corrige el desbalance de ancho (exp20), pero cuando todas las envolventes se solapan casi por completo, «la más estrecha que contiene» es una mala regla (35.9 contra 65.4).
- **La contención por coordenada es menos eficiente que la similitud** como regla de decisión sobre rasgos continuos: los métodos que comparan por distancia (NCM, kNN, Hopfield, RanPAC) dominan.
- Lo que el sistema sigue ofreciendo y estos rivales no prueban: la organización transactiva (directorios perspectivales sin registro central, exp10), la asociación bidireccional imagen ↔ texto en la misma memoria y los tres estados de respuesta sin calibración (exp23). Ninguna de esas propiedades se ha medido contra un rival. Si el sistema tiene una ventaja defendible, está ahí y no en la clasificación.
