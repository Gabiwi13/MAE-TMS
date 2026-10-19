# Experimento 22 — principio de tamaño sobre el sistema oficial de ETH-80

Exp20 (copia `MAE-TMS-medico`) propuso leer el directorio con el principio de tamaño: entre los agentes que contienen la pista gana la envolvente más estrecha, −Σᵢ log|soporte|. Ahí corrigió la absorción de dominios chicos con registro desbalanceado. Aquí se prueba que, donde el registro es balanceado, no rompe nada. Solo se leen los modelos oficiales (`models/agent_*.pkl`, `tme.pkl`, 23 sep); nada se modifica. Script: `run_experiment22_size_eth80.py`. Predicción fijada antes de correr: tamaño ≈ B1.

| hemisferio | n | reimplementación B1 = oficial | B1: acierto / rechazo / falso | tamaño: acierto / rechazo / falso | decisiones distintas |
|---|---|---|---|---|---|
| imagen (test de la etapa 7) | 656 | 656/656 | 96.2 / 3.5 / 0.3 | **96.3 / 3.5 / 0.2** | 1 (acierta tamaño) |
| texto (banco de 411 consultas) | 411 | 411/411 | 28.7 / 59.4 / 11.9 | 28.5 / 59.4 / 12.2 | 8 (tamaño 3, B1 4) |

Los directorios de texto oficiales se forman solo con las 16 consultas de la fase temprana, por eso rechazan el 59 %. El 93.5 % del README corresponde a la ablación, con directorios formados con más consultas. La comparación entre lecturas usa los mismos directorios y es válida igual.

Lectura: **se cumple la predicción.** Con registro balanceado el principio de tamaño equivale a B1 (imagen: una sola decisión distinta en 656, y a favor). Junto con exp20, que lo corrige donde B1 falla por desbalance, queda como lectura candidata para reemplazar a B1: igual donde B1 funciona, mejor donde B1 se rompe por ancho de envolvente. No se probó en el texto con directorios bien formados (la ablación) ni en exp16.

Archivos: `filas.json`, `resumen.txt`.
