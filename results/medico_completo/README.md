# Demo médico, corrida completa — todos los datos

Mismo diseño que `results/medico` (la «muestra»), con todos los datos: todo el train de cada dominio (60 % llenado, 40 % fase A, 16 variantes), todo el test oficial, PCA del nivel 1 con todo el train y épocas completas en los encoders del nivel 2. Fuera de distribución: las 1600 imágenes de RetinaMNIST. Transferencia: las 5856 de PneumoniaMNIST. Una corrida, 62 min, `DEMO_FULL=1 python run_medico_demo.py`. Detalle en `resumen.txt`.

## Muestra (200 por agente) contra completo (todo el train)

| medida | muestra | completo | kNN completo | cabeza completo |
|---|---|---|---|---|
| nivel 1: acierto / rechazo / falso | 85.7 / 13.6 / 0.7 | 94.9 / 0.1 / **5.1** | 100.0 | — |
| nivel 1: piel entregada a piel | 256/300 | **736/2005** (37 %) | 2004/2005 | — |
| nivel 1: mama entregada a mama | 137/156 | **3/156** | 156/156 | — |
| órganos: acierto (de lo respondido) | 87.7 (97.4) | **95.2 (97.3)** | 97.0 | 96.9 |
| piel: acierto / balanceado | 72.7 / 64.5 | 76.7 / **46.3** | 83.7 / 71.9 | 82.2 / 74.1 |
| melanoma | 175/223 | **37/223** (→ nevo 174) | 138/223 | 172/223 |
| tórax: acierto / balanceado | 22.4 / 23.0 | 65.6 / **7.1** | 62.0 / 12.4 | 30.8 / 20.6 |
| tórax: hallazgos dichos como «sin hallazgo» | — | **todos** (6244/6244) | — | — |
| mama (nivel 2): acierto | 88.5 | 87.2 | 89.1 | 87.8 |
| fondo de ojo rechazado | 29.7 % | **0.0 %** (1446 → tc_abdomen) | 0 % | — |

En tórax el 65.6 % es solo la proporción de placas sin hallazgo en test: el sistema responde «sin hallazgo» a todo, y el balanceado (7.1) es el azar de 14 dominios.

## El mecanismo: la envolvente más ancha se traga a las demás

Fracción de imágenes de test que la envolvente de cada agente contiene **sin ningún hueco** (soporte por coordenada del llenado; filas = dominio verdadero):

| nivel 1 | rx_torax | tc_abdomen | dermatoscopia | us_mama |
|---|---|---|---|---|
| muestra: piel | 0 % | 0 % | 93 % | 0 % |
| muestra: mama | 0 % | 10 % | 2 % | 96 % |
| completo: piel | **93 %** | 44 % | 100 % | 10 % |
| completo: mama | **89 %** | **96 %** | 67 % | 99 % |

| piel, nivel 2: melanoma contenido por… | melanoma | nevo |
|---|---|---|
| muestra (200 cada uno) | 90 % | 46 % |
| completo (468 contra 2816) | 94 % | **88 %** |

Cobertura de celdas (coordenada, nivel) con soporte: sin-hallazgo pasa de 66 % (200 imágenes) a 85 % (25 443); nevo de 53 % a 65 %. Los dominios chicos no cambian: mama 59 %, lesión vascular 35 %.

- Con el mismo número de imágenes por agente (la muestra), las envolventes tienen anchos parecidos y casi no se contienen entre sí.
- Con todos los datos, los dominios grandes ensanchan su envolvente hasta contener a los chicos. El agente correcto también contiene la imagen, así que pasa la contención, pero el directorio elige al grande. La normalización B1 (÷conteo) no lo corrige: no es un sesgo de conteo sino de **ancho de envolvente**.
- Por lo mismo desaparece el rechazo: el fondo de ojo cabe en la envolvente de tc_abdomen (0 % rechazado, antes 29.7 %).
- Órganos mejora (87.7 → 95.2 %) porque sus 11 dominios son de tamaño parecido (784–3285 en test).

## Lectura

- **Más datos no ayuda por sí solo; ayuda si llegan balanceados.** En una memoria de soportes por coordenada, la envolvente crece con lo registrado. Un dominio frecuente termina conteniendo a los raros, y el raro se pierde sin rechazo (melanoma → nevo, todo hallazgo → sin hallazgo, mama → tórax).
- En medicina es el modo de falla más grave, porque lo raro suele ser lo importante. Es exp17–18 a escala: dentro de una región compartida decide la masa, y aquí la masa ensancha la región.
- **Consecuencia de diseño:** el registro tiene que estar acotado y balanceado por agente (la muestra lo estaba por construcción), o la lectura tiene que compensar el ancho de la envolvente, no solo el conteo.
- kNN y la cabeza entrenada con muestreo balanceado sufren mucho menos (melanoma 138 y 172 de 223).

## Archivos

- `resumen.txt`, `filas.json`; `run.log` y `cache/` fuera de git

**Umbral de energía (nota del 26 oct 2026).** El umbral de norma del latente rechaza antes de consultar la memoria. En la corrida completa, de los 444 rechazos 12 son del umbral (11 en tc_abdomen y 1 en dermatoscopia) y 432 de la memoria; en el fondo de ojo, ninguno. Contado desde `filas.json` (campo `motivo`).
