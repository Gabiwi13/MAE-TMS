# Piloto: el sistema transactivo como organizador de una flota de módulos

**Fecha:** 19 de octubre de 2026
**Estado:** fijada antes de correr. Lo que cambie después se declara en el informe como desviación. Es una prueba piloto para decidir si la línea merece una tesis propia.

## 1. Pregunta

En una flota de módulos especializados, donde cada uno guarda solo las transacciones en que participó y no hay índice central, ¿el sistema transactivo aprende **quién sabe qué** y **quién lo hace bien**? ¿Rutea casi como un router central, consultando a pocos módulos? ¿Se abstiene ante lo que ningún módulo sabe? ¿Incorpora un módulo nuevo y tolera la salida de uno?

## 2. Flota

- **24 módulos:** 12 dominios (las piezas de VisA) × 2 módulos por dominio.
  - **Módulo A:** la red especializada base (buenas contra malas, WideResNet50).
  - **Módulo B:** la variante más débil del dominio entre las tres ya entrenadas (con sintéticas; con sintéticas y anti-colapso; con anti-colapso). Se elige por su acierto en la **mitad de aprendizaje**, nunca en la de evaluación.
- **Respuesta de un módulo:** la predicción de su red (buena o mala). Es correcta si el módulo es del dominio de la imagen y su predicción coincide con la etiqueta. Un módulo de otro dominio cuenta como error.
- **Percepción del ruteo, común a todos:** ResNet18 de ImageNet + PCA a 64 ajustada sobre las normales de train de VisA (el nivel 1 del demo industrial).
- **Contenido de cada módulo:** una MAE con las 270 normales de llenado de su pieza × 16 variantes. Los dos módulos de un dominio tienen el mismo contenido; solo los distingue su calidad.

## 3. Consultas

- **Conocidas:** las imágenes de test de cada pieza: normales, fallas de tipos entrenados y fallas del tipo excluido. Se reparten 50/50 por pieza (estratificado por etiqueta, semilla 42) en **aprendizaje** y **evaluación**.
- **Desconocidas** (solo en evaluación): 300 imágenes de cada uno de retinamnist, dermamnist y breastmnist (MedMNIST+ 128 px, leídas de `MAE-TMS-medico/data/medmnist`). Lo correcto es abstenerse.
- Cada consulta entra por un módulo activo al azar.

## 4. Protocolo transactivo

**Fase de aprendizaje** (corriente con retroalimentación, orden aleatorio):
1. Los módulos cuyo contenido contiene la pista (contención, ξ = 0) son candidatos. Si ninguno la contiene, no hay transacción.
2. **Exploración:** se le pregunta a un candidato elegido al azar.
3. Se registra la transacción (pista con sus 16 variantes → módulo) en dos directorios del módulo de entrada y del módulo que respondió: **intentos**, siempre, y **éxitos**, solo si acertó.

**Fase de evaluación** (directorios congelados), dos lecturas sobre el mismo recorrido de `route_transactive` (entrada, su círculo y los conocidos encadenados):
- **R1 oficial:** `route_transactive` con la lectura B1 (pertenencia, dividida por el número de registros).
- **R2 calidad:** entre los módulos con soporte, puntaje = proyección en éxitos / proyección en intentos. Es una tasa de éxito local estimada con la propia memoria. Gana el máximo. Si ningún directorio alcanzado tiene soporte, se abstiene.

**Eventos:**
- **E1, alta:** los dos módulos de candle no existen en la fase de aprendizaje. Después entran: se llena su contenido y llegan 5, 10, 20 y 40 consultas de candle con exploración. Se mide el ruteo de las consultas de evaluación de candle tras cada tramo.
- **E2, baja:** después del aprendizaje se retira el mejor módulo de pcb1. Se mide adónde van las consultas de pcb1 y el acierto.

## 5. Rivales (con las mismas transacciones de aprendizaje)

- **Router central kNN:** guarda todas las transacciones (pista, módulo, éxito). Para una pista, toma los 10 vecinos más cercanos y elige el módulo con mayor tasa de éxito entre ellos. Se abstiene si el vecino más cercano está más lejos que el percentil 99 de las distancias de aprendizaje.
- **Compuerta aprendida:** regresión logística pista → dominio, y luego el módulo con mejor tasa de éxito global en ese dominio. Se abstiene si la probabilidad máxima queda bajo el percentil 1 de las de aprendizaje.
- **Preguntarle a todos los que contienen:** el más confiado (probabilidad máxima de su red).
- **Al azar** entre los que contienen.
- **Oráculo:** acierta si algún módulo del dominio acierta.

## 6. Medidas

- Acierto del sistema en las consultas conocidas, abstención en conocidas y acierto de lo respondido.
- Abstención en desconocidas.
- **Fracción enviada al mejor módulo** del dominio (el de mayor acierto en evaluación), en los dominios donde los dos difieren en ≥ 5 puntos.
- **Módulos consultados por consulta:** directorios sumados en el recorrido. Para «preguntarle a todos»: los módulos que contienen.
- E1: fracción de las consultas de candle que van a un módulo de candle tras 5, 10, 20 y 40 transacciones. E2: acierto en pcb1 antes y después de la baja.

## 7. Predicciones

- **PP1.** R1 y R2 rutean al dominio correcto casi como el router central (a ≤ 3 puntos), consultando 2 a 4 módulos de 24.
- **PP2.** R1 reparte cerca de 50/50 entre los dos módulos de un dominio (no ve calidad). R2 prefiere al mejor en más del 70 % de los casos, pero **no lo sé**: es lo nuevo del piloto.
- **PP3.** Desconocidas: la MAE se abstiene en la mayoría (dominios muy lejanos, en contraste con el exp20, donde se rechazaba poco). El riesgo es que alguna envolvente de VisA contenga imágenes médicas.
- **PP4.** E1: tras 20 transacciones, ≥ 80 % de candle va a sus módulos. E2: las consultas de pcb1 pasan al otro módulo de pcb1, con un acierto igual al de ese módulo.

## 8. Criterio de decisión

- **Sigue (vale una tesis):** R2 queda a ≤ 3 puntos de acierto del router central consultando ≤ 6 de 24 módulos, **y** envía ≥ 70 % al mejor módulo en los dominios con diferencia de ≥ 5 puntos.
- **No sigue:** R2 envía < 70 % al mejor módulo **y** la compuerta aprendida supera a R2 por más de 5 puntos de acierto. Significaría que el directorio aprende pertenencia, pero no calidad.
- Entre los dos casos se reporta tal cual y se discute.

## 9. Entregables

`run_piloto_modulos.py` (caché en `results/piloto_modulos/cache/`, fuera de git) y `results/piloto_modulos/{README.md, resumen.txt, resultados.json}`.
