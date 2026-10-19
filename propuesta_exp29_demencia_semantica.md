# Propuesta del experimento 29: la demencia semántica como pérdida de conteos

**Estado:** propuesta; nada corrido. Se fija antes de correr y pide aprobación. Sale de la oportunidad C1 de `MAE-TMS/reports/Memorias asociativas en salud.md`; las citas y sus marcas de verificación están ahí y en `research_notes/Memorias asociativas en salud/modelos_enfermedades_memoria.md`.

## Pregunta

Si una memoria asociativa entrópica (MAE) heteroasociativa aprende objetos en el ambiente de Rogers et al. (2004) y se la daña quitando conteos, ¿reproduce el patrón de errores de los pacientes con demencia semántica (DS)? ¿Reproduce también lo que el modelo canónico no manipuló, los efectos de frecuencia y tipicidad? ¿Y lo hace mejor que los rivales con el mismo ambiente y el mismo daño medido?

Es la prueba más barata del camino «la MAE como modelo cognitivo». Si sale negativa, ese camino se debilita.

## Lo que se sabe de los pacientes (la vara)

| fenómeno | fuente |
|---|---|
| Con más severidad suben las **omisiones** y, menos, los **errores superordinados** («animal» por «perro»). Los **errores semánticos** (otro nombre de la misma categoría) primero suben y luego bajan. Hay **pocos errores entre dominios** | Rogers et al. 2004, DOI 10.1037/0033-295X.111.1.205: pacientes por cuartil de severidad, emparejados con 10/20/25/35 % de conexiones quitadas |
| Conforme cae la precisión, los nombres incorrectos son **más típicos que el blanco** | Woollams et al. 2008, DOI 10.1016/j.neuropsychologia.2008.04.005 (78 pacientes; solo resumen leído) |
| Un nombre prototipo se extiende a toda la categoría («perro» para cualquier cuadrúpedo) | Hodges, Graham y Patterson 1995, DOI 10.1080/09658219508253161 |
| Al dibujar se pierden primero los **rasgos distintivos** y aparecen **rasgos compartidos del dominio** (el pato de cuatro patas) | Bozeat et al. 2003, DOI 10.1080/02643290244000176; Rogers 2004 |
| Se acierta más con conceptos **familiares** y **típicos** | Rogers et al. 2015, DOI 10.1016/j.neuropsychologia.2015.04.015 |
| Hay **sub- y sobregeneralización** a la vez, moduladas por tipicidad | Mayberry et al. 2011, DOI 10.1162/jocn.2010.21582 |
| Atenuar las representaciones da un deterioro global (DS); distorsionarlas da un déficit de categoría (encefalitis herpética) | Lambon Ralph, Lowe y Rogers 2007, DOI 10.1093/brain/awm025 |

Rogers 2004 declara que no manipuló la frecuencia ni la familiaridad. En la MAE la frecuencia viene dada: es el número de veces que se registró algo.

## Paso 0: el ambiente exacto

- **Ya verificado** en las notas: seis categorías (pájaro, mamífero, fruta, vehículo, objeto doméstico, herramienta), en dos dominios (seres vivos y artefactos). Cada categoría tiene un prototipo con rasgos compartidos activos con p = 0.8 y rasgos idiosincrásicos con p = 0.2. Cada ítem distorsiona el prototipo cambiando cada rasgo con p = 0.2. Hay una capa visual y una verbal, y en la verbal hay nombres de tres niveles (general, básico y específico) y otras proposiciones.
- **Antes de programar**, se extraen del texto completo el número de ítems, de unidades visuales y de unidades verbales, y la forma de leer el nombre.
- **Las proporciones de error de los pacientes por cuartil** se transcriben de la tabla o la figura de Rogers 2004. Si solo están en la figura, se digitalizan y se declara.
- Todo lo que el artículo no especifique se fija aquí y se declara como decisión propia.

## Diseño

**Ambiente:** el de Rogers 2004, con 10 semillas de generación de ítems. Se agrega un factor nuevo, **frecuencia × tipicidad**:
- **Frecuencia:** en cada categoría, la mitad de los ítems tiene frecuencia alta (4 exposiciones) y la otra mitad baja (1 exposición), asignada al azar.
- **Tipicidad:** se mide después de generar el ítem, como la fracción de rasgos que comparte con el prototipo de su categoría. La mitad de arriba es «típica».

**Modelos.** Todos con el mismo ambiente y la misma frecuencia de exposición, y con un daño que crece en el mismo sentido.

| modelo | memoria | frecuencia | daño principal |
|---|---|---|---|
| **MAE** | `HeteroAssociativeMemory` del proyecto (código de Pineda y Morales sin cambios); izquierda = rasgos visuales, derecha = rasgos verbales, cada rasgo binario como columna con 2 niveles | número de registros | **quitar conteos:** cada unidad de conteo se borra con probabilidad d (binomial por celda) |
| **PDP simplificado** (réplica de Rogers 2004) | visual ↔ capa semántica oculta ↔ verbal, entrenado con retropropagación para ir de visual a verbal y de verbal a visual | probabilidad de muestrear el ítem | quitar una fracción d de los pesos, como Rogers |
| **MINERVA 2** (Hintzman 1986, DOI 10.1037/0033-295X.93.4.411) | un trazo por exposición; recuperación por eco ponderado por similitud al cubo | número de trazos | borrar cada rasgo de cada trazo con probabilidad d |
| **Vecino más cercano** (el más simple) | un vector por ítem; responde el ítem más parecido | sin efecto (un solo vector) | borrar cada rasgo guardado con probabilidad d |

El PDP no es idéntico al de Rogers (su red recurrente se entrenaba en el tiempo). Si no reproduce sus curvas en el paso de verificación, se reporta y se usa igual como rival declarado.

**Severidad:** d de 0 a 0.9 en pasos de 0.05, con 50 lesiones independientes por nivel y por semilla. Como d no significa lo mismo en cada modelo, **los modelos se comparan a igual exactitud de denominación**, no a igual d. Los cuartiles de pacientes se ubican por su exactitud.

**Tareas** (las de Rogers 2004, con la lectura fijada antes de correr):
- **Denominación (visual → verbal):** se toma la unidad de nombre más activa (en la MAE, el valor recuperado).
  - **correcto:** el nombre específico del ítem;
  - **error semántico:** el nombre específico de otro ítem de la misma categoría;
  - **error de categoría vecina:** otro ítem del mismo dominio pero de otra categoría (se reporta aparte y se suma a semántico, como Rogers);
  - **superordinado:** solo un nombre básico o general;
  - **entre dominios:** un nombre del otro dominio;
  - **omisión:** ningún nombre. En la MAE es el rechazo (sin soporte); en los demás, la activación por debajo de un umbral fijado sin daño para que las omisiones a d = 0 sean ≤ 2 %.
- **Dibujo diferido (nombre → visual):** la pista es solo la unidad del nombre específico. Se cuentan los rasgos idiosincrásicos perdidos y los rasgos compartidos del dominio que aparecen sin pertenecer al ítem (intrusiones).
- **Tipicidad de los errores:** en cada error semántico, la tipicidad del nombre dado menos la del blanco, y la frecuencia del nombre dado frente a la del blanco.

En la MAE, la recuperación es estocástica: cada ensayo es un muestreo, con 10 ensayos por ítem y lesión. En los rivales, la lectura es determinista dada la lesión.

## Predicciones

| | predicción para la MAE con quitar conteos | cómo se decide |
|---|---|---|
| P1 | las omisiones crecen de forma monótona con el daño | pendiente positiva en cada semilla |
| P2 | los errores superordinados crecen, pero menos que las omisiones | a la exactitud del peor cuartil: superordinados < omisiones |
| P3 | los errores semánticos suben y luego bajan (U invertida) | el máximo cae en un daño intermedio, no en los extremos |
| P4 | los errores entre dominios son pocos | < 5 % de las respuestas a todo nivel de daño |
| P5 | los nombres erróneos son más típicos que el blanco, y la diferencia crece con el daño (Woollams 2008) | diferencia media > 0 y pendiente positiva contra el daño |
| P6 | los ítems frecuentes resisten más, y los nombres intrusos vienen sobre todo de ítems frecuentes; el efecto crece con el daño (interacción frecuencia × daño) | exactitud alta − baja > 0 y creciente; intrusiones de nombres frecuentes > 50 % |
| P7 | al dibujar se pierden antes los rasgos idiosincrásicos que los compartidos, y las intrusiones de rasgos compartidos del dominio crecen con el daño | curva de pérdida idiosincrásica por encima de la compartida; intrusiones con pendiente positiva |
| P8 | **la prueba que exige el informe:** el sesgo a lo típico **crece con el daño** y no solo existe. La fracción de respuestas al nombre más frecuente o típico de la categoría sube con el daño | pendiente positiva respecto de d = 0 |
| P9 | (incierta) los rivales reproducen P1–P4 (Rogers ya lo mostró con el PDP), pero MINERVA 2 y el vecino más cercano no producen la U invertida de P3, y el PDP no produce P6 sin frecuencia de entrenamiento | por modelo |

Predicciones sobre los rivales, para no sobreinterpretar: con frecuencia de entrenamiento o número de trazos, el PDP y MINERVA 2 **también** podrían producir P5 y P6. Si lo hacen, la frecuencia no distingue a la MAE.

## Criterio

- **«La MAE es un modelo viable de la DS» (sostenido):**
  - cumple P1–P4 en dirección;
  - sus proporciones de omisión, superordinado y semántico a la exactitud de cada cuartil quedan dentro de ±10 puntos de las de los pacientes de Rogers 2004 en al menos 3 de 4 cuartiles;
  - y cumple P8.
- **Refutado si** con quitar conteos no aparece la U invertida (P3), o si el sesgo a lo típico no crece con el daño (P8). En ese caso el camino cognitivo se debilita, como dice el informe.
- **«Aporta algo que el modelo canónico no»:** solo si la MAE cumple P5 y P6 **y** el PDP con la misma frecuencia de exposición no las cumple o las cumple claramente peor: al menos 10 puntos menos de efecto de frecuencia, o una diferencia de tipicidad de los errores menor a la mitad. Si el PDP o MINERVA 2 las reproducen igual, se reporta que la frecuencia no distingue a la MAE.
- **Análisis secundario, sin criterio propio** (es el experimento 30, C2): el mismo barrido con **ruido** (cambiar conteos de nivel) en lugar de quitarlos, para ver si da un déficit más específico de categoría, como predice el contraste atenuar/distorsionar de Lambon Ralph 2007.

## Verificación

- Antes de dañar: sin daño, cada modelo nombra bien ≥ 95 % de los ítems y dibuja sus rasgos con ≥ 90 % de exactitud. Si un modelo no llega, se ajusta solo su entrenamiento (épocas, tasa) y se declara.
- La MAE usa `register`, `recall_from_left` y `recall_from_right` del código oficial sin modificarlo. El borrado de conteos opera sobre la relación guardada y se verifica que la entropía y el número de celdas con soporte bajan de forma monótona con d.
- El PDP se valida contra la dirección de las curvas de Rogers 2004 (omisiones crecientes, U invertida) antes de usarlo como rival.

## Costo

- **Programar:** 1 a 2 días (ambiente, cuatro modelos, tareas y lectura).
- **Correr:** CPU, sin GPU ni descargas: 10 semillas × 19 niveles × 50 lesiones × 4 modelos, con ambientes de decenas de ítems. Del orden de una hora; la MAE es lo más lento por el muestreo.
- **Leer el texto completo de Rogers 2004** para el paso 0 (es de acceso abierto en la página de Stanford): sin costo de datos.

## Archivos

- `run_experiment29_demencia_semantica.py`
- `results/experimento29/` (`README.md`, `resumen.txt`, `resultados.json`)

Están propuestos en la rama `medico-demo`, junto a exp20–28, para seguir la numeración. Si prefieres una rama propia para la línea cognitiva (con un nombre neutro), se crea antes de empezar.

## Lo que no responde

- **Pacientes reales individuales:** solo hay curvas agregadas publicadas.
- **El gradiente temporal invertido de la DS y el control semántico:** requieren mecanismos que la MAE no tiene (consolidación, control).
- **Alzheimer y DCL** (familiaridad contra recolección, falso reconocimiento DRM): son C2 y C3.

---

## Anexo: decisiones del paso 0 (fijadas antes de correr nada)

La especificación extraída está en `MAE-TMS/research_notes/Memorias asociativas en salud/rogers2004_especificacion.md`. El artículo deja huecos y tiene discrepancias internas. Se resuelven así:

- **Ambiente.** Los prototipos se toman de la Figura 3 tal como se leyeron:
  - visual: 64 unidades;
  - verbal: 61 perceptuales, 32 funcionales y 18 enciclopédicas (la figura, no las 64 y 16 de la Figura 1);
  - 40 nombres: 36 únicos y 4 generales (bird, animal, tool, vehicle), asignados como en el texto (p. 212).

  Regla por ítem:
  - «+» se enciende con p = 0.8, «0» con p = 0.2 y «−» nunca.
  - Excepción: en la parte verbal de las frutas, «−» también se enciende con p = 0.2 (el texto dice que ahí se distorsionan todas las propiedades).
  - Se regenera hasta que no haya dos ítems iguales.
- **Frecuencia:** en cada categoría, 4 ítems al azar con 4 exposiciones y 4 con 1.
- **Tipicidad:** la fracción de rasgos visuales del ítem que coinciden con el valor modal de su categoría.
- **Ítems de prueba de denominación:** los 28 con nombre específico, sin frutas (como Rogers).
- **Clasificación de respuestas:**
  - superordinado = un nombre general que abarca al ítem (bird o animal para aves, animal para mamíferos, vehicle, tool);
  - semántico = cualquier otro nombre del mismo dominio (vivo: aves, mamíferos y frutas; artefacto: los otros tres);
  - entre dominios = un nombre del otro dominio;
  - omisión = ningún nombre.
- **MAE:**
  - `HeteroAssociativeMemory` con izquierda = verbal (151 columnas, 2 niveles) y derecha = visual (64 columnas, 2 niveles);
  - cada exposición es un `register` del par (verbal completo, visual);
  - denominación = `recall_from_right` con la pista visual completa;
  - dibujo = `recall_from_left` con una pista parcial: solo la columna del nombre específico definida (= 1) y el resto indefinido;
  - daño = adelgazamiento binomial de los conteos del interior de la relación, sin tocar los márgenes de funciones parciales.
- **Dos lecturas de la denominación en la MAE, declaradas ahora:**
  - **(a) principal:** el valor recuperado por el recall oficial (muestreo y búsqueda). Entre los nombres = 1 gana el de mayor peso en la proyección; con rechazo o sin nombre = 1 es omisión;
  - **(b) secundaria:** la proyección como activación, con p(nombre = 1) = peso del nivel 1 / suma de los dos niveles. Gana el nombre más activo por encima de 0.5, la regla de Rogers. Con rechazo es omisión.

  Si la lectura (a) no llega al 95 % sin daño, el criterio se evalúa con (b) y se dice así.
- **PDP:** red recurrente con capa semántica de 64 conectada en ambos sentidos con la visual y la verbal, más recurrencia semántica, sesgo fijo −2 y sigmoide.
  - **Ensayo:** 3 pasos con la entrada fijada, 2 libres y 2 con error, con una actualización por paso (no 4 subpasos).
  - **Patrones:** entrada visual, verbal sin nombres y nombre (los generales con un miembro al azar).
  - **Blanco:** todas las visibles.
  - **Aprendizaje:** retropropagación en el tiempo con Adam, hasta que el criterio sin daño se cumpla, como máximo 2000 épocas.
  - **Frecuencia:** los ítems de alta frecuencia aparecen 4 veces por época.
  - **Daño:** poner a cero una fracción d de todos los pesos entrenables.
- **MINERVA 2:**
  - rasgos ±1 y nombres incluidos en el trazo;
  - sonda = visual con la parte verbal en 0;
  - eco normalizado por la suma de |activación|;
  - nombre = la unidad de nombre más activa con eco > 0;
  - frecuencia = número de trazos;
  - daño = poner a 0 cada rasgo de cada trazo con probabilidad d.
- **Vecino más cercano:**
  - un vector ±1 por ítem;
  - responde los nombres que sobreviven en el ítem más parecido (coseno sobre la parte visual): el específico si sobrevivió, si no el general, si no omisión;
  - omisión también si el coseno máximo < 0.5.
- **Si el costo de la MAE lo exige,** se bajan las lesiones por nivel o los ensayos por ítem y se declara en el informe.
