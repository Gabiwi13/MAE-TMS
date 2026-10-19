# Revisión científica de las líneas de aplicación (industria, medicina y flota de módulos)

Revisión crítica hecha **antes de seguir agregando variantes**, para separar lo que está establecido de lo que fue ajuste a los datos. Contiene:
- el [modelo formal](modelo_formal.md) de lo que calcula cada pieza del sistema, con predicciones;
- la [réplica con 10 semillas y las ablaciones](../replica_ablaciones/README.md) del diseño congelado, en la flota de diseño y en una flota nueva;
- el registro de afirmaciones de abajo, con su estado y su evidencia.

## Riesgos de método identificados

1. **Jardín de caminos que se bifurcan.** En la línea de módulos se probaron, uno tras otro sobre los mismos datos, R1, R2, R3, R4, la entrada por receptor y Thompson con ventana. Cada criterio se fijó antes de correr, pero la secuencia se adaptó a los fracasos. La configuración que cumplió (la quinta) **no se replicó en una flota nueva**.
2. **Una sola semilla** en casi todos los experimentos hasta la réplica.
3. **Componentes no aislados:** hasta la ablación no se sabía si el resultado venía de la memoria de directorio o de contar éxitos.

## Registro de afirmaciones

| # | afirmación | estado | evidencia |
|---|---|---|---|
| 1 | La MAE no es competitiva como detector ni como clasificador; la calidad la fija la percepción | **sostenida** (robusta) | industrial, cierre_mae, cascada_modulos, red_sintetica, exp18–20, exp24: con 4 percepciones, 2 conjuntos de datos y diferencias de 20 a 40 puntos |
| 2 | La contención acepta el producto de los soportes marginales: generaliza la pertenencia y no ve desviaciones conjuntas | **sostenida** (mecanismo más evidencia) | modelo formal, Prop. 1; pérdida sistemática contra Mahalanobis y kNN |
| 3 | El ancho de la envolvente manda (desbalance, saturación), y partir en especialistas la estrecha | **sostenida** | demo médico, industrial_monolitica (inclusión verificada sin excepciones) |
| 4 | Olvido exacto restando conteos | **sostenida** (algebraica) | olvido_privacidad: 0 diferencias |
| 5 | Guarda agregados, no ejemplares (pertenencia como una media) | **sostenida** | olvido_privacidad: AUROC 0.47–0.53, contra 1.00 de kNN, en 4 conjuntos |
| 6 | El reconocimiento por contenido identifica el dominio y se abstiene ante lo desconocido **cuando el latente separa los dominios** | **sostenida, condicional** | VisA: 100 % de abstención ante imágenes médicas; ruteo de 98 %. MedMNIST nivel 1: el contenido se superpone y la abstención ante la retina es del 5 % (exp20: 6–24 %) |
| 7 | El sistema aprende qué módulo lo hace mejor | **sostenida solo en VisA, y no por la memoria de directorio** | réplica: R3 74.5 % al mejor en VisA, pero la tabla de conteos da 87.8 % y la tasa global 89.1 %; en MedMNIST, R3 elige al peor como el azar |
| 8 | La memoria de directorio aporta como mecanismo de decisión frente a contar | **refutada** | réplica: R3 por debajo de TAB y de GLOBAL por 13–15 puntos (VisA, IC excluye el 0) y de TAB entre candidatos por 7.6 en pérdida (MedMNIST) |
| 9 | Los directorios perspectivales y el encadenamiento a conocidos aportan algo propio | **no demostrada** (sin aporte medible) | con entrada por receptor se lee 1 directorio de mediana; PROPIO = R3 en VisA y mejor que R3 en MedMNIST |
| 10 | El olvido exacto permite adaptarse a la deriva | **sostenida como mecanismo, sin ventaja propia** | deriva_olvido: sin olvido no se recupera y con ventana sí; es lo mismo que hace cualquier contador con ventana (el bandido central se recupera más rápido) |
| 11 | La heteroasociación con texto funciona sin pares registrados | **refutada** | industrial_clip: 0 de 1232 oraciones |
| 12 | Una red especializada más la MAE detecta fallas nuevas mejor que la confianza de la red | **refutada** | cierre_mae, cascada_modulos, red_sintetica |

## Qué queda en pie, dicho con precisión

El aporte defendible del sistema EAM-TMS **no es un mecanismo de decisión**. Es una **memoria de contenido declarativa y agregada** que:
1. reconoce la pertenencia a un dominio por contención (producto de soportes marginales), con abstención cuando la pista cae fuera, **si la percepción separa los dominios**;
2. olvida exactamente;
3. no guarda ejemplares;
4. se puede inspeccionar y es determinista.

Organizada en especialistas, esa memoria funciona como **filtro de dominio** delante de cualquier otro mecanismo. En la línea de módulos, el sistema que mejor rinde es «el contenido de la MAE elige los candidatos y una tabla de conteos elige entre ellos». La parte transactiva propiamente dicha (directorios perspectivales, encadenamiento) no mostró ventaja medible sobre contar.

## Implicaciones para seguir

- **No seguir agregando lecturas de directorio** sin una predicción del modelo formal que diga por qué deberían ganarle a contar.
- Si se sigue con la línea de flotas, el componente de investigación es el **reconocimiento de dominio por contenido**: cuándo separa (depende de la percepción) y cómo combinarlo con estimadores estándar. Es una pregunta más modesta y más honesta.
- Lo que sí está sólido (afirmaciones 1 a 6) es lo que la tesis puede defender, con el modelo formal como explicación.
- Cualquier experimento nuevo se replica en una flota o un conjunto de datos que no se haya usado para diseñarlo.
