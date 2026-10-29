# Propuesta viejo/nuevo: pesos homo en el sistema principal (tesis, `.tex8`)

**Estado:** pendiente de aprobación. Nada aplicado.

**Fuentes:**
- `results/ablation_mdir_bias/` (d0df16c);
- `results/exp2_iota_kappa/` (re-corrida con κ por cuantiles);
- `results/exp3_corrected_routing/summary.json`;
- `results/exp6_capacity/report.md`.

Todas son corridas con pesos homo en todas las lecturas (763c902).

**Qué no cambia:**
- el núcleo: fase A 99.9 %; ruteo visual 631/656 = 96.2 % con 2 falsos; evocación 97.4 %; fidelidad 16/16;
- la temprana (90.0 %);
- las entropías del directorio (2.974 y 2.977);
- la formación del directorio (exp4: todas las condiciones terminan en 81.2 %, conteos y entropía 2.914 iguales);
- containment, rechazo y falsos en todos los experimentos.

`.SMTex` es una copia del 2 de agosto que no cita estas cifras; no se toca.

---

## 1. Metodología (`04_metodologia.tex`)

### 1a. Declarar los pesos (nuevo párrafo, después de «Los parámetros de la EAM se fijaron en…»)

**Viejo:** (no existe)

**Nuevo:**
> Todas las proyecciones usan los pesos por rasgo de la Ecuación~\ref{eq:pesos}: en las memorias de contenido, los de la memoria homo-asociativa del dominio de la pista; en los directorios, los de su propia relación (cuántas veces se registró cada valor en cada rasgo, lo mismo que daría una memoria homo-asociativa llenada con las mismas pistas). Los pesos solo cambian magnitudes: el containment, y con él la aceptación y el rechazo, no depende de ellos.

### 1b. Síntesis de los parámetros (línea 175)

**Viejo:** «…$\kappa$ no cambió ningún resultado en el rango probado, y…»

**Nuevo:** «…$\kappa$ solo rechaza: en todo el rango en que actúa baja la precisión y nunca la mejora, y…»

---

## 2. Resultados (`05_resultados.tex`)

### 2a. Tabla `tab:calibracion` (N = 400, 5 semillas)

| Condición | Viejo (temprana · fidelidad · madura) | Nuevo |
|---|---|---|
| A (cruda) | 90.0 · 92.0 · 87.0 | 90.0 · 90.5 · 85.2 |
| B1 | 90.0 · 95.2 · **93.5** | 90.0 · 95.8 · **93.0** |
| B2 | 90.0 · 95.2 · 93.2 | 90.0 · 95.2 · 91.8 |
| C | 90.0 · 92.5 · 89.5 | 90.0 · 91.2 · 88.0 |
| D | 90.5 · 92.5 · 89.0 | 90.5 · 91.4 · 87.3 |
| E32 | 90.0 · 93.5 · 90.5 | 90.0 · 92.2 · 88.5 |
| E64 | 90.0 · 93.2 · 92.2 | 90.0 · 93.0 · 89.8 |
| F | 90.0 · 92.0 · 87.0 | 90.0 · 90.5 · 85.2 |
| G (D+B1+F) | 90.5 · 95.3 · 94.0 | 90.5 · 95.7 · 93.5 |

### 2b. «B1 sigue siendo la corrección irreducible» (líneas 52–58)

**Viejo:** «…la lectura cruda del directorio (A) pierde 6.5 puntos frente a la lectura normalizada por conteo (87.0\% frente a 93.5\%; con el llenado de 4 variantes la brecha era de 13 puntos: …), y ninguna condición que manipula síntomas (B2, C, D, E32, E64) la alcanza, aunque B2 queda a tres décimas. La combinación G supera a B1 sola por medio punto (94.0\% frente a 93.5\%), dentro del ruido de cinco semillas…»

**Nuevo:** «…la lectura cruda del directorio (A) pierde 7.8 puntos frente a la lectura normalizada por conteo (85.2\% frente a 93.0\%; con el llenado de 4 variantes la brecha era de 13 puntos: …), y ninguna condición que manipula síntomas (B2, C, D, E32, E64) la alcanza; la más cercana, B2, queda a 1.2 puntos. La combinación G supera a B1 sola por medio punto (93.5\% frente a 93.0\%), dentro del ruido de cinco semillas…»

### 2c. Distribución de ganadores (líneas 97–103)

**Viejo:** «…la participación de \texttt{apple} bajo la lectura B1 baja a \textbf{13.2\%} \emph{sin cambiar el vocabulario}; \texttt{pear} queda en 78\% (86\% con el llenado de 4 variantes: …). La misma figura muestra que bajo la lectura cruda (A) \texttt{apple} todavía captura el 19.5\% de las victorias: … y con B1 ningún agente se desvía más de 2 puntos del ideal.»

**Nuevo:** «…la participación de \texttt{apple} bajo la lectura B1 baja a \textbf{13.8\%} \emph{sin cambiar el vocabulario}; \texttt{pear} queda en 76\% (86\% con el llenado de 4 variantes: …). La misma figura muestra que bajo la lectura cruda (A) \texttt{apple} todavía captura el 20.5\% de las victorias: … y con B1 ningún agente se desvía más de 2.2 puntos del ideal.»

### 2d. Estado del directorio (línea 119)

**Viejo:** «La fidelidad temprana-madura con B1 es del 95.2\%.»

**Nuevo:** «La fidelidad temprana-madura con B1 es del 95.8\%.»

### 2e. Protocolo completo (líneas 136–145)

**Viejo:** «…con lectura cruda, 71.2\%. … inferior a la del banco completo (93.5\%)…»

**Nuevo:** «…con lectura cruda, 72.5\%. … inferior a la del banco completo (93.0\%)…»

(Temprana 81.2 %, B1 81.2 %, fidelidad 92.5 %, conteos y entropía 2.914: iguales.)

### 2f. Sección $\iota \times \kappa$ (líneas 166–211): se reescribe

**Por qué.** La tabla vieja mostraba las cuatro columnas de κ idénticas. La compuerta comparaba una celda de la proyección, que suma las 300 coordenadas de la pista, contra κ·mem.mean, que es por celda (26 oct). Ya corregida, κ ≤ 1.5 tampoco rechazaba nada, porque la razón que compara la compuerta vale entre 1.52 y 2.10. La rejilla nueva no se elige a mano: es 0 más los cuantiles 10, 25, 50, 75, 90 y 100 % de esa razón, medida con ι = 0 sobre los 260 pares token-agente contenidos del banco.

**Viejo (párrafo de entrada):** «Se realizó un barrido de cuadrícula con $\iota \in \{0, 0.25, 0.5, 1.0\}$ y $\kappa \in \{0, 0.5, 1.0, 1.5\}$ sobre el subconjunto de 80 consultas.»

**Nuevo:** «Se realizó un barrido de cuadrícula con $\iota \in \{0, 0.25, 0.5, 1.0\}$ y $\kappa$ en $\{0\}$ más los cuantiles 10, 25, 50, 75, 90 y 100\,\% de la razón que compara la compuerta (activación media por celda de la proyección entre la media de la memoria), medida con $\iota = 0$ sobre los 260 pares token-agente contenidos del subconjunto de 80 consultas: $\kappa \in \{0, 1.754, 1.801, 1.844, 1.937, 2.059, 2.104\}$.»

**Viejo (tabla):** una columna «κ (cualquier valor)».

**Nuevo (tabla):** precisión temprana (rechazo), en %.

| ι \ κ | 0 | 1.754 | 1.801 | 1.844 | 1.937 | 2.059 | 2.104 |
|---|---|---|---|---|---|---|---|
| 0.00 | 81.2 (5.0) | 77.5 (6.2) | 65.0 (10.0) | 57.5 (18.8) | 35.0 (45.0) | 12.5 (85.0) | 2.5 (96.2) |
| 0.25 | 82.5 (5.0) | igual en todas las columnas | | | | | |
| 0.50 | 75.0 (11.2) | igual en todas las columnas | | | | | |
| 1.00 | 8.8 (86.2) | igual en todas las columnas | | | | | |

**Viejo («Efecto de κ»):** «El parámetro de umbral $\kappa$ no cambió ningún resultado en el rango probado: las proyecciones superan la media del tensor en órdenes de magnitud, de modo que el umbral relativo nunca es vinculante.»

**Nuevo:**
> **Efecto de $\kappa$.** Con $\iota = 0$, $\kappa$ solo rechaza: a medida que sube, la precisión baja de 81.2\% a 2.5\% y el rechazo sube de 5.0\% a 96.2\%, y ninguna columna mejora la línea base. El umbral relativo descarta por igual pistas válidas y espurias, porque la razón que compara (entre 1.52 y 2.10) no separa a unas de otras. Con $\iota \geq 0.25$, $\kappa$ no actúa en este rango: la poda concentra la activación en las celdas que sobreviven y la media de la memoria no cambia, así que la razón mínima sube a 2.33, 2.78 y 3.96, por encima del $\kappa$ máximo. $\kappa$ no es una defensa contra el sesgo de masa.

### 2g. «Ninguna condición nativa sustituye a B1» (línea 208)

**Viejo:** «(71.2\% frente a 81.2\% en la línea base; 78.8\% frente a 83.8\% en la mejor condición nativa)»

**Nuevo:** «(72.5\% frente a 81.2\% en la línea base; 80.0\% frente a 83.8\% en la mejor condición nativa)»

### 2h. Formación (línea 231)

**Viejo:** «(el mismo protocolo con el banco completo alcanza 93.5\%, …)»

**Nuevo:** «(el mismo protocolo con el banco completo alcanza 93.0\%, …)»

### 2i. Tabla `tab:capacidad`, columna «Variedad $L_1$»

| N | Viejo | Nuevo |
|---|---|---|
| 25 | 1.91 | 1.87 |
| 50 | 1.89 | 1.83 |
| 100 | 1.75 | 1.74 |
| 200 | 1.94 | 1.97 |
| 328 | 2.17 | 2.17 |

Las demás columnas (train, test, falsos, enrutamiento, entropía) son iguales.

---

## 3. Discusión (`06_discusion.tex`)

- **Línea 50.** Viejo: «(87.0\% frente a 93.5\%)» → Nuevo: «(85.2\% frente a 93.0\%)».
- **Línea 56.** Viejo: «(94.0\% frente a 93.5\%)» → Nuevo: «(93.5\% frente a 93.0\%)».
- **Línea 72.** Viejo: «…cayó de 20.0\% a 13.2\%…» → Nuevo: «…cayó de 20.0\% a 13.8\%…».
- **Línea 109.** Viejo: «…alcanzar el 93.5\%.» → Nuevo: «…alcanzar el 93.0\%.»

## 4. Conclusiones (`07_conclusiones.tex`)

- **Líneas 14–16.** Viejo: «…una \textbf{precisión madura del 93.5\%} … fidelidad temprana-madura del 95.2\% y la participación de \texttt{apple} … en \textbf{13.2\%}…» → Nuevo: «…una \textbf{precisión madura del 93.0\%} … fidelidad temprana-madura del 95.8\% y la participación de \texttt{apple} … en \textbf{13.8\%}…».
- **Línea 36.** Viejo: «20\% $\to$ 13.2\%» → Nuevo: «20\% $\to$ 13.8\%».

---

## 5. Opcional: metaconocimiento perspectival (no está en la tesis)

Si se quiere en la presentación o en la discusión, exp9 da ahora una curva limpia. Se cuentan las consultas de un dominio cuyo especialista se perdió y que llegan al especialista perdido, de 411; las 240 consultas de formación son las de exp10, con entrada al azar y registro oficial (entrada + ganador):

| Interacciones de texto | Directorio del sobreviviente | Ruteo transactivo oficial, sin el perdido | Pizarrón (techo) |
|---|---|---|---|
| 0 (directorios oficiales, 16 consultas de la etapa 6) | 40 | 90 | — |
| 16 | 70 | 100 | 202 |
| 60 | 176 | 302 | 354 |
| 120 | 185 | 332 | 380 |
| 240 | 250 | **368** | 393 |

En las 171 consultas que no se usaron para formar: 149 con el ruteo transactivo contra 161 del pizarrón.

**Lectura:** el metaconocimiento perspectival se forma con la experiencia. Con el protocolo oficial (agregar a los conocidos y encadenar) llega al 90 % de las consultas a 240 interacciones, a 6 puntos del pizarrón. Con 16 interacciones de texto, como en la etapa 6, apenas hay qué consultar.

La columna transactiva se agregó después de ver la del sobreviviente; la curva del sobreviviente y el pizarrón eran lo declarado en el plan.

Propuesta de texto, si se incluye (después del párrafo de formación del directorio):

> **El metaconocimiento perspectival requiere experiencia.** Cada agente registra solo las transacciones en que participó, de modo que lo que sabe de los demás crece con el número de interacciones. Al retirar un miembro, las consultas de su dominio que llegan a él por el ruteo transactivo pasan de 90 de 411 con las 16 consultas de la etapa 6 a 368 de 411 con 240 interacciones, frente a 393 del registro completo.

## 6. Fuera de la tesis (README y documentos de trabajo)

- **exp12:** la correlación brecha–solapamiento desaparece (r 0.45, p 0.017 → r −0.00, p 0.996). Viene de las 16 variantes: el control con pesos uniformes sobre las memorias actuales da r 0.06 (p 0.75). Los pesos homo alejan a M2 del vecino más cercano en 1.0 en promedio, parejo en los 28 pares (`results/controles_uniformes/experimento12/control.md`).
- **missing_cue:** la baja de recuperaciones perfectas viene de las 16 variantes, no de los pesos. El control con pesos uniformes sobre las memorias actuales da lo mismo: sample-and-search 24/9/6/7 contra 25/7/3/8 con homo. El orden SS < ST < RS se mantiene.
- **exp14:** con el mismo código, los rechazos de fase A por «niveles» varían entre corridas (0 o 3 de 1024), porque la GPU redondea distinto (diferencias de 1e-4 en los latentes).
