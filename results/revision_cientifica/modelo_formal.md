# Modelo formal del sistema EAM-TMS tal como está implementado

Objetivo: describir con precisión qué calcula cada pieza del sistema, para explicar los resultados obtenidos y derivar predicciones antes de seguir experimentando. Todo lo que sigue describe el código del repositorio (`src/hetero_lib/associative.py`, `src/hetero_lib/hetero_associative_4d.py`, `src/associative_memory.py`, `src/stage6_interaction.py` y los scripts de la línea de módulos), con ι = κ = 0, que es como se usó.

## 1. Percepción y cuantización

Un encoder fijo E lleva una imagen a un latente z ∈ ℝ⁶⁴. La cuantización usa un rango global por coordenada, [ℓᵢ, uᵢ], que es el del llenado con un margen del 10 %:

  qᵢ(z) = ⌊ 32 · clip((zᵢ − ℓᵢ)/(uᵢ − ℓᵢ), 0, 1) ⌋,  con el valor 32 llevado a 31.

Todo lo que viene después depende solo de q(z) ∈ {0,…,31}⁶⁴. **La MAE no ve el latente: ve 64 niveles independientes.**

## 2. Memoria de contenido (homoasociativa)

**Estado:** R ∈ ℕ^{64×32}, donde R[i, a] cuenta los registros cuyo nivel en la coordenada i es a. Registrar z suma 1 en R[i, qᵢ(z)] para cada i.

**Soporte marginal:** Sᵢ = { a : R[i, a] > 0 }.

**Reconocimiento estricto (ξ = 0):** z es aceptado ⇔ qᵢ(z) ∈ Sᵢ para todo i. Con tolerancia ξ, se aceptan hasta ξ coordenadas fuera.

**Peso:** w(z) = (1/64) Σᵢ R[i, qᵢ(z)] (lo que devuelve `recognize_gated_right` cuando acepta).

**Proposición 1 (el conjunto aceptado es un producto de soportes marginales).** A(R) = S₁ × S₂ × … × S₆₄. *Demostración:* la condición de aceptación es una conjunción de condiciones sobre cada coordenada por separado. ∎

Consecuencias:
- **C1.1 · Generaliza la pertenencia.** Acepta cualquier combinación de niveles vistos por separado, aunque la combinación nunca se haya visto. Por eso reconoce vistas nuevas de un dominio (exp16) y rutea bien dominios separables.
- **C1.2 · No ve desviaciones conjuntas.** Si una entrada anómala tiene en cada coordenada un nivel que alguna entrada normal tuvo, se acepta, aunque la combinación sea muy improbable. Un detector que mide estructura conjunta (Mahalanobis, kNN) sí la separa. Es la causa de que la MAE pierda como detector de fallas en todas las piezas (industrial, cierre): una falla local mueve poco cada coordenada.
- **C1.3 · Monotonía.** Registrar más solo agranda A(R). Con registro desbalanceado, el dominio con más registros tiene la caja más grande y se traga a los demás (demo médico completo); balancear el registro lo corrige.
- **C1.4 · Inclusión de la unión.** Una memoria con dominios D₁ ∪ D₂ tiene Sᵢ ⊇ Sᵢ(D₁), así que acepta todo lo que acepta el especialista de D₁, y más. Por eso la memoria única rechaza a lo sumo lo que rechaza el especialista (verificado sin excepciones en `industrial_monolitica`), y la partición estrecha las envolventes.
- **C1.5 · Saturación.** Si N registros cubren la densidad marginal de cada coordenada, |Sᵢ| tiende al número de niveles con densidad no nula. Con cientos de miles de parches, casi todo el rango queda cubierto (`industrial`, parches: 27.8 de 32 niveles), y solo se rechazan valores extremos.

**Probabilidad de rechazar una entrada ajena x:** 1 − Πᵢ P(qᵢ(x) ∈ Sᵢ). Es grande solo si lo ajeno sale del soporte en al menos una coordenada. Esto explica por qué la memoria rechaza lo cercano cuando el latente lo separa coordenada por coordenada (órgano nunca visto, exp20: 96.3 %) y por qué rechaza poco lo lejano que cae dentro del rango (otra modalidad, exp20: 6 a 24 %).

## 3. Memoria de directorio (heteroasociativa de pista a agente)

**Estado:** D ∈ ℕ^{64×K×32×2}. Una transacción (pista z → agente k) suma 1 en D[i, k, qᵢ(z), 1] y en D[i, j, qᵢ(z), 0] para todo j ≠ k.

**Proyección** (`project`, dim = 0) con pesos uniformes, para cada agente k y bit b:

  P_k(z) = Σᵢ D[i, k, qᵢ(z), 1] si ese término es positivo en todas las coordenadas definidas, y 0 si alguno es cero.

(La implementación anula la integración en cuanto una coordenada da cero.)

**Proposición 2 (la proyección es un estimador con núcleo aditivo, filtrado por soporte).** Si el filtro no anula, P_k(z) = Σ_t 1[agente_t = k] · Σᵢ 1[qᵢ(z_t) = qᵢ(z)], donde t recorre las transacciones registradas. Es decir, P_k(z) / 64 = Σ_t 1[agente_t = k] · κ(z, z_t), con κ(z, z') = fracción de coordenadas en que z y z' caen en el mismo nivel. *Demostración:* se intercambian las sumas sobre coordenadas y transacciones. ∎

Consecuencias:
- **C2.1 · Cuenta efectiva.** n_k(z) = P_k(z) / (64 · 16) es una cuenta de transacciones hacia k, ponderada por cuánto se parecen sus pistas a z (16 variantes por transacción). Es lo que usan R4 y Thompson.
- **C2.2 · El núcleo κ es ancho.** Dos pistas comparten nivel en muchas coordenadas aunque sean de imágenes distintas del mismo dominio. Con dominios separables, κ alto equivale casi a «mismo dominio». **Predicción: la localidad dentro de un dominio es débil, y la lectura del directorio se parece a una cuenta por dominio.**
- **C2.3 · B1 borra la calidad.** La lectura oficial divide P_k por el número de registros de k. Si el módulo k tiene una tasa de éxito pₖ y se registran solo los éxitos, P_k crece con pₖ · intentos, y la división por registros lo cancela. Por eso R1 reparte 50/50 (piloto: 52.6 %). Hace falta registrar intentos y éxitos por separado y tomar el cociente (R2).
- **C2.4 · El cociente es un estimador de Nadaraya-Watson.** P_k^éxitos(z) / P_k^intentos(z) = Σ_t éxito_t · κ(z, z_t) / Σ_t κ(z, z_t), sobre las transacciones hacia k: una tasa de éxito local con el núcleo κ.

## 4. Registro perspectival y recorrido

**Registro:** cada transacción se anota en el directorio del agente de entrada y en el del ganador.

**Proposición 3 (evidencia por directorio).** Con T transacciones y entradas uniformes entre K módulos, cada directorio recibe en esperanza alrededor de 2T/K transacciones, repartidas entre los D dominios en proporción a su frecuencia. *Cuenta directa.* Con T = 790, K = 24 y D = 12: unas 66 transacciones por directorio y unas 5 por dominio. Con unas 5 transacciones repartidas entre dos módulos, el intervalo de la tasa de éxito es tan ancho que no distingue módulos que difieren 10 o 15 puntos. **Por eso R3 con entrada al azar pierde la calidad (54.7 %) y R2, que suma unos 19 directorios, la conserva (79 %).**

**Proposición 4 (con entrada por receptor, el sistema se reduce a un bandido local por receptor).** Si la entrada es un módulo cuyo contenido contiene la pista, y los contenidos separan los dominios, todas las transacciones del directorio de k son de su dominio. Entonces el recorrido R3 lee el directorio del receptor (mediana: 1 lectura) y decide con su cociente de Nadaraya-Watson. **El sistema equivale a un estimador de tasa de éxito por dominio, con la evidencia del dominio repartida entre sus receptores** (aquí 2) **y con el núcleo κ.** Consecuencias:
- debería rendir como un bandido por dominio que usa la mitad de la evidencia: más lento que el bandido central para adaptarse a la deriva (observado: 1250 contra 1000 pasos con la misma ventana);
- **la parte transactiva (conocidos, encadenamiento) casi no interviene**: es una predicción que hay que comprobar con ablaciones.

## 5. Olvido

Restar la contribución de un registro es la operación inversa exacta mientras ningún conteo llegue a 2¹⁶ − 1, porque el estado es una suma (verificado: 0 diferencias). La ventana deslizante convierte cualquier estimador de la sección 3 en su versión con ventana.

## 6. Predicciones para las ablaciones (antes de correrlas)

Con entrada por receptor, sobre la flota de VisA:
- **PF1.** Cambiar los directorios por una **tabla de conteos** de éxitos e intentos por (receptor, módulo), sin núcleo, da la misma preferencia por el mejor módulo y el mismo acierto, dentro del ruido entre semillas. Se sigue de C2.2 y la Proposición 4.
- **PF2.** Una **tasa global por módulo**, que junta la evidencia de todos los receptores, da una preferencia igual o mayor, porque usa el doble de evidencia por dominio.
- **PF3.** Leer **solo el directorio propio**, sin conocidos, da lo mismo que R3.
- **PF4.** El núcleo κ solo podría aportar si la calidad relativa de los módulos **cambia dentro del dominio** (por ejemplo, uno es mejor en normales y otro en fallas). Se mide esa heterogeneidad. Si no existe, la localidad no tiene nada que aprovechar.
- **PF5.** En una flota nueva, no usada para diseñar (MedMNIST: cabeza entrenada, kNN y memoria como módulos de cada modalidad), se reproduce lo mismo: el sistema aprende la calidad, y la tabla de conteos rinde igual.

Si PF1 a PF3 se cumplen, lo que funciona en la línea de módulos es **contar éxitos por módulo con entrada en el dominio correcto**, y la MAE aporta: (a) el reconocimiento del dominio por contenido, que es el que da el receptor y la abstención; (b) el olvido exacto; (c) que todo es agregado y auditable. No aporta un mecanismo de decisión que un contador no tenga. Esa sería una conclusión honesta y publicable.
