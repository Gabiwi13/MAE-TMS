# Experimento 25 — la organización transactiva contra rivales federados y descentralizados

Diseño, brazos y predicciones en `propuesta_exp25_transactivo.md` (fijados antes de correr). Un agente por dominio con su contenido (corrida balanceada; rasgos ajustados por nivel). Fase A: cada consulta entra por un agente al azar y la gana el especialista que reconoce con más fuerza. Todos los brazos descentralizados ven **las mismas transacciones** y solo cambia qué guardan y cómo leen. Test hasta 300 por dominio, con entrada distinta del especialista. Script `run_experiment25_transactivo.py`; detalle en `resumen.txt` y `resultados.json`.

Nota de corrección: la primera corrida falló al pasar al segundo nivel. El caché de soportes del principio de tamaño usaba `id()` como clave y podía leer el soporte de un directorio ya liberado. Se corrigió guardándolo en el propio directorio (`run_experiment20_size_principle.py`) y se rehizo todo. Exp20 y exp22 no estaban afectados: mantenían vivos todos los directorios.

## Acierto de ruteo con las mismas transacciones (%)

| nivel · visibilidad | MAE B1 | MAE tamaño | prototipos transactivos | kNN transactivo | gossip de prototipos |
|---|---|---|---|---|---|
| órganos (11) · f = 0 | 93.3 (rechazo 4.4) | 93.2 | **96.6** | 96.3 | **96.6** |
| órganos · f = 1 | 93.2 | 92.4 | **96.6** | 96.2 | **96.6** |
| órganos · anillo r = 1 | 93.2 | 92.7 | **96.6** | 96.2 | **96.6** |
| modalidad (4) · f = 0 | 93.0 (rechazo 5.8) | 92.9 | 98.4 | **99.9** | 98.4 |
| modalidad · f = 1 | 93.4 | 91.8 | 98.4 | **99.7** | 98.4 |

Cotas: FedProto 96.6 / 98.4 (28 KB / 3 KB de comunicación), FedAvg 96.6 / 99.9 (3.1 MB / 0.4 MB y servidor central), oráculo kNN central 96.8 / 100.

Comunicación durante la formación, órganos f = 0: MAE 11.6 MB de pistas cuantizadas, prototipos y kNN 46.5 MB (las mismas pistas en coma flotante), gossip 0.4 MB.

## Pérdida, ingreso y lo ajeno (visibilidad f = 0)

| prueba | MAE B1 | prototipos | kNN |
|---|---|---|---|
| pérdida del especialista k: ubica sus consultas en k (órganos / modalidad) | 93 / 93 % | 97 / 98 % | 96 / 100 % |
| ingreso de un dominio nuevo: acierto con 8 transacciones nuevas (órganos / modalidad) | 41 / 5 % | **98 / 100 %** | 95 / 90 % |
| … con 32 transacciones | 81 / 50 % | 98 / 100 % | 97 / 97 % |
| … con 128 transacciones | 90 / 89 % | 97 / 100 % | 99 / 99 % |
| fondo de ojo rechazado, a igual aceptación de lo propio (órganos) | 100 % | 98 % | 100 % |
| fondo de ojo rechazado, a igual aceptación de lo propio (modalidad) | **24 %** | 0 % | 1 % |

## Predicciones

- **P1 (los directorios por distancia rutean igual o mejor): se cumple.** Con las mismas transacciones los prototipos transactivos rutean 3.3 puntos más en órganos y 5.4 más en modalidad, sin rechazo.
- **P2 (FedProto, mejor acierto con poquísima comunicación, pero con una ronda explícita): se cumple, y el gossip de prototipos logra lo mismo sin ningún centro** (96.6 %, 0.4 MB, solo con mensajes entre vecinos de un anillo).
- **P3 (con visibilidad mínima el encadenado mantiene el alcance; la diferencia es de comparación): se cumple.** Ningún brazo cambia más de 1.6 puntos entre f = 0 y f = 1.
- **P4 (MAE y prototipos conservan la ubicación al perder un miembro): se cumple para todos los brazos descentralizados** (93–100 %). Los prototipos y el kNN la conservan algo mejor que la MAE.
- **P5 (la MAE rechaza más lo ajeno a igual aceptación de lo propio): se cumple solo en el nivel de modalidad** (24 % contra 0–1 %). En órganos empatan, porque todos rechazan casi todo el fondo de ojo. Y ese 24 % sigue por debajo de los detectores centrales de exp20 (Mahalanobis 49 %, MSP 100 %).

## Veredicto según el criterio fijado

El criterio pedía que la MAE ganara claramente, en al menos una de las propiedades 2 a 5, al mejor rival descentralizado a igual información:
- **Comunicación:** pierde contra el gossip de prototipos.
- **Pérdida de un miembro:** empata o pierde.
- **Ingreso de un miembro:** pierde claramente; necesita 30–100 transacciones donde a los prototipos les bastan 8.
- **Lo ajeno:** gana solo en modalidad y solo contra puntajes de similitud simples.

**La organización transactiva se sostiene; la memoria asociativa como su implementación, no.** Con la misma organización (especialistas, directorios perspectivales, encadenado y agregado) y las mismas transacciones, un directorio de prototipos rutea mejor, incorpora miembros nuevos más rápido y, en forma de gossip, comunica una fracción mínima. Lo valioso del sistema es la arquitectura transactiva de Wegner, que funciona igual con otra memoria debajo, y no la memoria asociativa que hoy la implementa.
