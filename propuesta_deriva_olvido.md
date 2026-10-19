# Aprendizaje en línea con deriva: el olvido exacto como mecanismo de adaptación

**Fecha:** 19 de octubre de 2026
**Estado:** fijada antes de correr. Lo que cambie después se declara en el informe como desviación.

## 1. Pregunta

En una flota real los módulos cambian: uno que era el mejor se degrada (un sensor sucio, una red mal reentrenada). ¿El sistema transactivo, aprendiendo en línea, nota el cambio y pasa al otro módulo? ¿El **olvido exacto** de transacciones viejas (ventana deslizante restando conteos) hace que se adapte, comparado con no olvidar y con un bandido central con ventana, que es la solución estándar?

## 2. Montaje

- Flota y consultas del piloto: 24 módulos, 12 piezas × 2, con la percepción y el contenido de siempre.
- **Entrada por receptor** y **ruteo dirigido R3** (la combinación que cumplió el criterio en la etapa 2).
- **Corriente en línea de T = 6000 consultas:** se sortea con reposición entre todas las consultas conocidas (aprendizaje y evaluación del piloto), y como pista se usa una de sus 16 variantes al azar.
- **Decisión con exploración que sale de la memoria (muestreo de Thompson):** los candidatos son los módulos cuyo contenido contiene la pista (los mismos que definen al receptor). Para cada candidato se toma la evidencia (éxitos e intentos efectivos) leída en el directorio del recorrido de R3. Se muestrea de Beta(éxitos + 1, fallas + 1) y gana el mayor. No hay ε ni tasa de exploración fija.
- **Retroalimentación:** después de responder se registra la transacción (16 variantes) en intentos y, si acertó, en éxitos, en el directorio de entrada y en el del módulo que respondió.
- **Deriva** en t = 3000: en los 7 dominios donde un módulo era mejor por ≥ 5 puntos, ese módulo **se degrada**: su respuesta se invierte con probabilidad 0.5 (semilla fija). Desde ahí el mejor es el otro.

## 3. Variantes de memoria

- **F0:** sin olvido.
- **FW:** ventana deslizante exacta de W transacciones. Cuando entra una, se olvida la más vieja, restando exactamente sus conteos (la operación verificada en olvido_privacidad). W ∈ {300, 600, 1200}, barrido declarado.

## 4. Rivales (misma corriente, misma deriva)

- **Bandido central por dominio** (muestreo de Thompson con el dominio verdadero, una ventaja que la memoria no tiene): sin ventana y con ventana de W transacciones globales.
- **Oráculo:** siempre el mejor módulo vigente.

## 5. Medidas

- Acierto en línea por tramos:
  - antes de la deriva (t de 2000 a 3000);
  - justo después (3000 a 3500);
  - recuperación (3500 a 4500);
  - final (5000 a 6000).
- **Fracción al mejor módulo vigente** en los 7 dominios con deriva, por tramos de 250.
- **Pasos hasta recuperar:** primer tramo de 250 tras la deriva con ≥ 70 % al nuevo mejor.
- Costo: directorios leídos por consulta.

## 6. Predicciones

- **PD1.** Antes de la deriva todas las variantes prefieren al mejor (≥ 70 %).
- **PD2.** Sin olvido (F0), tras la deriva la memoria sigue mandando al módulo degradado durante mucho tiempo: la evidencia vieja pesa. No recupera el 70 % en los 3000 pasos restantes, o tarda > 1500.
- **PD3.** Con ventana, se recupera en ≤ 1000 pasos; más rápido con W chica, a costa de más ruido antes de la deriva.
- **PD4.** La memoria con ventana queda a ≤ 3 puntos del bandido central con la misma ventana en el tramo final, sin conocer el dominio y sin índice central.

## 7. Criterio

**«El olvido exacto es un mecanismo de adaptación del sistema»** queda **sostenido** si, para algún W:
- la variante con ventana alcanza ≥ 70 % al nuevo mejor en ≤ 1500 pasos tras la deriva, mientras F0 no lo alcanza o tarda al menos el doble;
- su acierto en el tramo final queda a ≤ 3 puntos del bandido central con la misma ventana.

Queda **refutado** si F0 se recupera igual de rápido que la ventana (el olvido no aporta), o si la ventana queda > 5 puntos bajo el bandido con ventana.

## 8. Entregables

`run_deriva_olvido.py` y `results/deriva_olvido/{README.md, resumen.txt, resultados.json}`.
