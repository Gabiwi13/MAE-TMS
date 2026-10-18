# Demo médico, corrida balanceada

Todos los datos de test, fuera de distribución y transferencia, y los mismos encoders que la corrida completa. Solo cambia el registro: cada agente usa N = máx(328, clase más chica del nivel) imágenes de train, o todas si tiene menos, con 60 % para llenar y 40 % para la fase A. El 328 es lo que tenía cada agente en la muestra (200 + 128). Regla fijada antes de correr. N resultante: modalidad 546, órganos 1357, tórax 328 (neumonía 210), piel 328 (dermatofibroma 80, vascular 99, queratosis actínica 228), mama 328 (maligno 147). `DEMO_BAL=1 python run_medico_demo.py`, 10 min. Detalle en `resumen.txt`.

## Tres corridas

Muestra: test hasta 300 por dominio. Completo y balanceado: todo el test, mismos encoders.

| medida | muestra | completo | **balanceado** | kNN (bal.) | cabeza |
|---|---|---|---|---|---|
| modalidad: acierto / rechazo / falso | 85.7 / 13.6 / 0.7 | 94.9 / 0.1 / 5.1 | **92.1 / 7.5 / 0.4** | 99.6 | — |
| modalidad: acierto de lo respondido | 99.2 | 94.9 | **99.6** | — | — |
| piel entregada a piel | 85 % | 37 % | **91 %** | 100 % | — |
| mama entregada a mama | 88 % | 2 % | **94 %** | 100 % | — |
| órganos: acierto (de lo respondido) | 87.7 (97.4) | 95.2 (97.3) | **94.1 (97.5)** | 96.9 | 96.9 |
| piel: acierto / balanceado | 72.7 / 64.5 | 76.7 / 46.3 | **73.8 / 62.6** | 80.6 / 74.7 | 82.2 / 74.1 |
| melanoma | 175/223 | 37/223 | **175/223** | 171 | 172 |
| nevo dicho melanoma | — | 0 | **192/1341** | — | — |
| tórax: acierto / balanceado | 22.4 / 23.0 | 65.6 / 7.1 | **7.2 / 21.1** | 25.4 / 20.6 | 30.8 / 20.6 |
| tórax: «sin hallazgo» reconocido | — | 11924/11928 | **13/11928** | 3075 | 3794 |
| tórax: hallazgos dichos «sin hallazgo» | — | todos | casi ninguno | — | — |
| mama (nivel 2): acierto | 88.5 | 87.2 | 87.8 | 89.7 | 87.8 |
| fondo de ojo rechazado | 29.7 % | 0.0 % | **24.2 %** | 0 % | — |
| PneumoniaMNIST rechazada en el nivel 1 | 55 % | 0.5 % | 32 % | — | — |

## Lectura

- **Balancear devuelve el comportamiento de la muestra con todo el test:** la jerarquía vuelve a entregar piel y mama a su modalidad (91 % y 94 %), lo respondido en modalidad acierta el 99.6 %, melanoma vuelve a 175/223 y el fondo de ojo vuelve a rechazarse en parte (24 %). Órganos queda en 94 %, con 97.5 % de lo respondido, cerca de kNN y de la cabeza (96.9 %).
- **Con igual tamaño, el dominio heterogéneo queda corto.** «Sin hallazgo» es la clase más variada de tórax. Con 328 imágenes su envolvente no cubre la variedad real, y casi todas sus placas caen en la de algún hallazgo (→ nódulo 2995, → atelectasia 1257, → masa 1182). En piel pasa algo parecido con nevo → melanoma (192). El sistema pasa de no ver ningún hallazgo (completo) a verlos en todas partes (balanceado). El balanceado de tórax (21.1) es el de kNN y la cabeza (20.6): el límite de esa tarea es la percepción.
- **El tamaño de la envolvente es el parámetro que manda.** Demasiado grande, se traga a los vecinos y desaparece el rechazo (completo). Igual para todos, castiga al dominio más variado (balanceado). Lo correcto sería que el ancho de cada envolvente siguiera la variedad real del dominio, no su frecuencia ni un número fijo. Un análogo de B1 que divida por el ancho de la envolvente (la fracción de celdas con soporte) en vez de por el conteo es el siguiente paso natural; no se probó.
- Para datos reales: con registro balanceado el sistema sirve para triaje por modalidad y órgano con abstención (99.6 % y 97.5 % de lo respondido). En hallazgos de radiografía de tórax, con estos rasgos de 128 px, no sirve: ni la memoria ni los clasificadores estándar pasan de ≈ 21 % balanceado.
