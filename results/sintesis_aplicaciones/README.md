# Síntesis: ¿para qué sirve hoy el sistema EAM-TMS en la industria y en medicina?

Reúne los resultados de los demos y experimentos de aplicación, todos con diseño y predicciones fijados antes de correr. Cada fila remite a su informe. No hay cifras nuevas: todas salen de esos informes.

| informe | datos |
|---|---|
| [`industrial/`](../industrial/README.md) | demo industrial, VisA, 12 piezas |
| [`industrial_monolitica/`](../industrial_monolitica/README.md) | memoria única contra partición |
| [`industrial_clip/`](../industrial_clip/README.md) | texto y CLIP como percepción compartida |
| [`olvido_privacidad/`](../olvido_privacidad/README.md) | olvido exacto y ataque de pertenencia (VisA y MedMNIST+) |
| [`enrutador_flota/`](../enrutador_flota/README.md) | enrutador de detectores PatchCore |
| [`cierre_mae/`](../cierre_mae/README.md) | cierre: WideResNet50 congelada y red especializada en buenas contra malas |
| [`cascada_modulos/`](../cascada_modulos/README.md) | cascada malas → buenas partidas → revisión humana |
| [`medico_balanceado/`](../medico_balanceado/), [`experimento20/`](../experimento20/README.md), [`experimento21/`](../experimento21/README.md), [`experimento23/`](../experimento23/README.md), [`experimento24/`](../experimento24/README.md) | demo médico, MedMNIST+ |

## Qué es el sistema, en una línea

Una memoria **de caja blanca, determinista y declarativa**. Aprender es sumar conteos por coordenada en una tabla de 64 × 32 por especialista. Reconocer es comprobar que cada coordenada de la entrada cae dentro de lo registrado. Rutear es consultar directorios de «quién sabe qué», formados por transacciones. No hay entrenamiento por gradiente: la percepción la pone un encoder congelado (ResNet18 o CLIP) y la memoria no la cambia.

## Tabla final de comparación

Cada fila compara la MAE contra la mejor alternativa medida sobre los mismos latentes y, cuando aplica, a igual punto de operación.

| capacidad | MAE | mejor alternativa medida | veredicto | informe |
|---|---|---|---|---|
| **Rutear al especialista** (12 piezas) | 98.4 % a su pieza, 0 a otra, 1.6 % de abstención | kNN 100 % (sin abstención) | **sirve**; empata, con abstención | industrial |
| **Rutear por modalidad médica** (4) | 92.1 % de acierto, 7.5 % de rechazo, 99.6 % de lo respondido | kNN 99.6 % (sin abstención) | **sirve**; acierta igual en lo que responde, pero se abstiene más | medico_balanceado |
| **Abstenerse ante una pieza nueva** (12 pliegues) | 100 % de abstención | kNN con umbral: 100 %; kNN sin umbral la reporta como falla de otra pieza | **sirve**; igual que kNN con umbral | enrutador_flota |
| **Enrutar una flota de detectores** | 37.9 % de fallas pasan, 1.6 % de normales a humano | oráculo: 39.2 % pasan | **sirve**; no daña al sistema | enrutador_flota |
| **Olvidar un registro** | exacto: 0 celdas y 0 decisiones distintas; 0.09 s | kNN y NCM también exactos; un modelo entrenado necesita reentrenar | **sirve**; no exclusivo | olvido_privacidad |
| **No exponer registros individuales** | ataque de pertenencia: AUROC 0.51 | NCM 0.49 · gaussiana 0.59 · kNN 1.00 | **sirve**; como una media, mucho mejor que kNN | olvido_privacidad |
| **Partición frente a una sola memoria** | ruteo igual (99.1); detección con parches 39.3 contra 14.6 % | — | **la partición aporta** | industrial_monolitica |
| **Separar claro, ambiguo y desconocido** (sin umbral) | órganos: claro 93.6 % con 97.3 % de acierto; ambiguo 3.4 % con 69.9 % | a igual tamaño de lista, kNN y el clasificador igualan la cobertura | **sirve**; no es superior | experimento23 |
| **Cubrir clases raras** (lista de candidatos) | peor clase de tórax 27.1 % | conformal por clase 88.0 % | **no compite** | experimento24 |
| **Aprendizaje incremental por clases** | 35.9 % de acierto final | NCM, kNN, Hopfield y RanPAC: 75.6–86.4 % | **no compite** | experimento24 |
| **Rechazar lo lejano** (otra modalidad) | rechaza 6–24 % | MSP 99.8–100 % | **no compite** | experimento20 |
| **Rechazar lo cercano** (órgano nunca registrado) | 96.3 % | kNN 97.7 · Mahalanobis 96.6 | **empata** | experimento20 |
| **Detectar fallas, vector global** | 5.8 % de detección (falsa alarma 0.2) | Mahalanobis 29.1 % (AUROC 0.817) | **no compite** | industrial |
| **Detectar fallas, por parches** | 45.6 % (falsa alarma 14.8) | PatchCore 73.9 % (AUROC 0.864) | **no compite** | industrial |
| **Detectar fallas con la mejor percepción congelada** (WideResNet50) | global 5.8 %; parches 26.8 % | Mahalanobis 29.9 %; PatchCore 1536 70.6 % (AUROC 0.886) | **no compite** (11/12 y 12/12 piezas por debajo) | cierre_mae |
| **Detectar fallas sobre una red especializada** (buenas contra malas) | 90.5 % (falsa alarma 1.8) | cabeza de la red 93.0 % (3.4), AUROC 0.994 | **cerca, sin superarla**; la que separa es la red | cierre_mae |
| **Abstenerse ante un tipo de falla nunca visto** | 2.6 % de abstención, 34.2 % pasa en silencio | MSP 6.0 %, 24.1 % pasa en silencio | **no hay nicho** | cierre_mae |
| **Cascada malas → buenas → revisión, con el módulo de buenas partido en k** | idéntica para k = 1 a 8: 31.8 % de las fallas nuevas pasan en silencio | MSP a igual revisión: 24.1 % | **no funciona**: la red colapsa las buenas en 1–3 direcciones | cascada_modulos |
| **Usar texto como pista** (con CLIP) | 0 de 1232 oraciones llegan a su pieza | coseno de CLIP: 57.7 % | **no funciona** sin pares registrados | industrial_clip |
| **Detectar fallas con descripciones** | +0.2 puntos de detección | CLIP sin ejemplos de falla: AUROC 0.667 | **no funciona** | industrial_clip |
| **Tamaño del estado** (12 piezas) | 2.0 MB de conteos | kNN 0.83 MB; NCM unas 32 veces menos que la MAE (exp24) | **no es ventaja** | enrutador_flota |

## ¿Sirve de algo hoy, tal como está?

**Sí, para una tarea concreta: ser la capa que organiza y responde de qué sabe el sistema. No para ser el que decide si algo está bien o mal.**

Lo que ya hace bien, con evidencia:
1. **Enrutar con abstención:** manda cada pieza, imagen o caso al especialista que corresponde, sin errores entre dominios separables, y dice «no es de nadie» cuando llega algo distinto.
2. **Caja blanca de verdad:** cada decisión se explica con la propia memoria. Se puede decir qué especialista respondió, qué coordenadas quedaron fuera de lo registrado y cuántos registros sostienen cada celda. Es determinista: la misma memoria da siempre la misma respuesta, sin semillas ni épocas.
3. **Olvido a pedido:** retirar el aporte de un paciente o de un lote mal etiquetado es una resta exacta, sin reentrenar.
4. **No conserva ejemplares:** guarda un resumen por coordenada. Ante un ataque de pertenencia se comporta como una media del dominio (AUROC 0.51), mientras que kNN expone cada registro (1.00).
5. **Modularidad:** un dominio nuevo es un especialista nuevo, sin tocar a los demás, y la partición estrecha las envolventes (detecta casi el triple que una sola memoria con parches).

Lo que no debe hacer:
- Detectar fallas o anomalías finas, clasificar con la mejor exactitud, cubrir clases raras o aprender de forma incremental con alta exactitud. En todo eso hay alternativas simples que la superan con claridad.

**El matiz que hay que declarar siempre:** casi cada propiedad, por separado, la tiene un método simple. kNN con umbral se abstiene igual, NCM olvida igual de exacto y revela lo mismo, y kNN también es determinista e interpretable (muestra vecinos). Lo que la MAE ofrece es **reunirlas todas en un mismo mecanismo**, más la organización transactiva: directorios perspectivales sin índice central y especialistas modulares.

## Cuándo elegirla y cuándo no

| conviene la MAE como capa de ruteo y memoria si… | no conviene si… |
|---|---|
| hay que justificar o auditar cada decisión (sector regulado, trazabilidad) | lo que importa es la máxima exactitud o detección |
| los datos individuales no deben conservarse (pacientes, clientes) | se pueden guardar los ejemplos y basta kNN |
| hay que poder olvidar a pedido (consentimiento retirado, lote erróneo) | el catálogo es fijo y nunca se retira nada |
| el catálogo de dominios cambia (productos nuevos, nuevos modelos especialistas) | hay un solo dominio |
| conviene abstenerse y mandar a un humano lo desconocido | cualquier respuesta es mejor que ninguna |

**Arquitectura recomendada con lo que hay hoy:** la MAE como enrutador con abstención y registro auditable, y detrás de ella un detector o clasificador estándar por dominio. En la planta: PatchCore (AUROC 0.886 con WideResNet50) si solo hay piezas sanas, o una red especializada (AUROC 0.994) si hay fallas etiquetadas. En el hospital: el modelo de cada modalidad. En el demo, esa combinación deja pasar las mismas fallas que con la pieza verdadera.

**Cierre de la línea «solo MAE»** ([`cierre_mae/`](../cierre_mae/README.md)): con la mejor percepción congelada la memoria pierde en 11 y 12 de 12 piezas. Sobre una red especializada llega a 90.5 % de detección, contra 93.0 % de la red, porque lee lo que la red ya separó. Y ante un tipo de falla nuevo no se abstiene más que la red. La MAE no se usa como detector; se usa como capa sobre una red.

## Límites

- Una semilla por experimento. Un conjunto industrial (VisA, cuyas piezas están muy separadas entre sí) y uno médico (MedMNIST+, 128 px).
- La caja blanca explica la decisión de la memoria, no la del encoder congelado que produce los latentes.
- La privacidad se midió sobre el latente, no sobre la imagen, y no cubre a quien observa la memoria antes y después de un registro.
- Abierto: una pieza nueva parecida a una conocida, una memoria por zona de la pieza y reconstruir la imagen desde el estado guardado.
