# Demo médico — EAM-TMS sobre MedMNIST+

Copia `MAE-TMS-medico`, rama `medico-demo`. Datos: MedMNIST+ v3.0 a 128 px (Zenodo 10.5281/zenodo.10519652, CC BY 4.0; DermaMNIST viene de HAM10000, CC BY-NC). Archivos verificados por md5, fuera de git en `data/medmnist/`. Script: `run_medico_demo.py`. Diseño fijado antes de correr; una sola corrida, sin ajustes posteriores. Investigación, no uso clínico.

## Diseño

- **Nivel 1, modalidad** (4 agentes): rx_torax (ChestMNIST), tc_abdomen (OrganAMNIST), dermatoscopia (DermaMNIST), us_mama (BreastMNIST). Encoder: ResNet18 de ImageNet congelado + PCA a 64 ajustada con 2000 imágenes de train por modalidad.
- **Nivel 2, hallazgo u órgano como dominio**, un índice por modalidad: 11 órganos de TC; 7 lesiones de piel; en tórax, sin hallazgo más los 13 hallazgos con ≥ 200 casos de un único hallazgo en train (hernia, con 71, queda fuera); mama maligno / normal-benigno. Encoder por modalidad: ResNet18 de ImageNet ajustado 8 épocas con la clasificación del hallazgo (muestreo balanceado por clase, Adam 1e-4). El latente es la capa de 64.
- **Memoria con el protocolo oficial:** 200 de llenado + 128 de fase A por agente (clases con < 328 casos: 60 % / 40 %), 16 variantes, Q = 32, umbral de energía, ξ = 0, directorios perspectivales y entrada por un no especialista.
- **Test:** split oficial, hasta 300 imágenes por dominio.
- **Comparaciones sobre los mismos latentes:** kNN (k = 5, contra el pozo de llenado) y la cabeza lineal entrenada. Ninguna de las dos se abstiene nunca.
- **Fuera de distribución:** RetinaMNIST (fondo de ojo), nunca registrada. **Transferencia:** PneumoniaMNIST (tórax pediátrico de otro hospital).

## Resultados

| nivel · dominio | memoria: acierto | rechazo | falso | **acierto de lo respondido** | kNN | cabeza |
|---|---|---|---|---|---|---|
| nivel 1 · modalidad | 85.7 | 13.6 | 0.7 | **99.2** | 99.9 | — |
| tc_abdomen · 11 órganos | 87.7 | 10.0 | 2.3 | **97.4** | 95.0 | 95.0 |
| us_mama · 2 clases | 88.5 | 1.9 | 9.6 | 90.2 | 89.7 | 87.8 |
| dermatoscopia · 7 lesiones | 72.7 | 6.3 | 21.0 | 77.6 | 76.3 | 75.6 |
| rx_torax · 14 dominios | 22.4 | 1.1 | 76.5 | 22.7 | 24.7 | 25.5 |

Balanceado (memoria / kNN / cabeza): órganos 87.7 / 95.0 / 95.0; dermatoscopia 64.5 / 74.5 / 73.7; mama 82.3 / 85.5 / 84.9; tórax 23.0 / 23.3 / 23.9. Detalle por dominio y confusiones en `resumen.txt`.

- **Órganos:** lung-left 293/300, liver 293/300, sin falsos en ninguno de los dos. Los falsos que hay son entre vecinos anatómicos o lados (riñón izquierdo ↔ derecho, fémur izquierdo ↔ derecho).
- **Piel:** melanoma 175/223 (kNN 158, cabeza 176). Las clases más raras rechazan más y aciertan menos que las comparaciones: dermatofibroma 10/23 (8 rechazos; kNN y cabeza 17) y lesión vascular 15/29 (12 rechazos; 23). Falso más frecuente: nevo → melanoma (48).
- **Tórax:** todos los métodos quedan cerca del 23–25 % (azar 7 %). La memoria casi nunca dice «sin hallazgo» (3/300; kNN 60, cabeza 46) y casi no rechaza (1.1 %). «Nódulo» sale en 3/300.

**Fuera de distribución (fondo de ojo, 300):** la memoria rechaza el **29.7 %**; el resto lo manda a us_mama 104, tc_abdomen 72 y dermatoscopia 35. kNN responde siempre (dermatoscopia 260).

**Transferencia (PneumoniaMNIST, 300):** el nivel 1 rechaza 164 y manda 122 a rx_torax. En el nivel 2 ninguna neumonía llega al agente de neumonía (kNN tampoco). Es tórax pediátrico de otro hospital: el cambio de dominio se nota.

**Jerarquía:** el nivel 1 entrega a la modalidad correcta 258/300 (tórax), 254/300 (abdomen), 256/300 (piel), 137/156 (mama). De punta a punta, en órganos ≈ 0.85 × 0.88 ≈ 75 %.

## Lectura

- **Donde los dominios son visualmente distintos** (modalidad, órganos, mama), el sistema se acerca al clasificador estándar y **lo que responde es más confiable**: 99.2 % en modalidad y 97.4 % en órganos, porque se abstiene en lo dudoso. El precio es cobertura: rechaza el 10–14 %.
- **Donde los hallazgos se superponen** (radiografía de tórax), todos fallan, y la memoria falla **sin abstenerse**. Es lo mismo que en exp17–18: dentro de una región compartida, la contención dice sí a casi todos y decide la densidad. Para un uso médico es el modo de falla más peligroso, porque manda sanos a hallazgos.
- **El rechazo fuera de distribución existe pero es parcial** (30 % del fondo de ojo). Es mejor que un clasificador que siempre responde, pero no alcanza para prometer seguridad.
- **Las clases raras** salen parecidas a la cabeza cuando tienen cientos de casos (melanoma). Con decenas (dermatofibroma, vascular), la memoria rechaza más.
- Con datos reales lo que se puede esperar es triaje y especialistas por órgano con abstención. No sirve para hallazgos finos en radiografía sin una percepción mucho mejor (más resolución, encoder médico preentrenado). Y hay que medir el rechazo fuera de distribución antes de prometerlo.

## Archivos

- `run_medico_demo.py` (en la raíz de la copia; `DEMO_SMOKE=1` para la prueba corta)
- `resumen.txt`, `filas.json`, `run.log` (fuera de git el `.log`)
- `cache/`: encoders y latentes, fuera de git

**Umbral de energía (nota del 26 oct 2026).** El umbral de norma del latente rechaza antes de consultar la memoria. Aquí casi no actúa: de los 663 rechazos, 8 son del umbral (7 en tc_abdomen y 1 en dermatoscopia, en el nivel 2) y 655 de la memoria; en el fondo de ojo, ninguno. Contado desde `filas.json` (campo `motivo`).
