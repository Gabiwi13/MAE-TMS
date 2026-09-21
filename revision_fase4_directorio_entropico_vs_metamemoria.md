# Fase 4: la contradicción entre los dos documentos sobre el directorio

**Fecha:** 20 de septiembre de 2026
**Alcance:** material para decidir. No se modificó ningún documento ni código. Las citas van por archivo y línea, sobre el commit c60a2ae de la rama `exp7-directorio-unificado`. La decisión es del autor.

---

## 1. Las dos posiciones

### A. 30 de agosto: el directorio no es entrópico

`discusion_directorio_entropico.md`:

- Línea 27: "σ nunca importa porque el directorio **nunca llama a `recall`**. La parte genuinamente entrópica de una MAE —el recall constructivo y estocástico (`reduce`/`choose` sobre la distribución de la celda)— jamás se ejercita en el directorio."
- Línea 61: "no es entrópico (nunca opera sobre sus distribuciones). Lo que es: una representación distribucional con una operación determinista. [...] lo único que hace con esa distribución es el argmax. Entropía en potencia, nunca en acto."
- Línea 69: "Un directorio entrópico fallaría en su única tarea, como una libreta de direcciones difusa."
- Línea 92: "la maquinaria entrópica del sustrato deliberadamente no se ejercita ahí, y el carácter entrópico del sistema vive en las memorias de contenido".

### B. 14 de septiembre: el directorio es metamemoria y contiene contenido

`discusion_marco_teorico_directorio.md`:

- Línea 12: "El directorio contiene contenido. Leído por identidad (`recall_domain`), reconstruye el dominio del agente al 100%, propio o ajeno."
- Línea 39: "La lectura inversa de exp8 es una reinstalación por índice."
- Línea 43: "El directorio monitorea [...] y controla (rutea). Que use el mismo sustrato MAE que la memoria de contenido no es una confusión: es la tesis. [...] 'El directorio es una memoria per se' deja de ser una objeción y pasa a ser la definición de metamemoria."
- Línea 130: "El directorio es metamemoria: contiene una descripción del dominio de cada agente [...] que basta para responder en su ausencia con la clase correcta."

## 2. Lo que hace el código hoy

### 2.1 El directorio sí llama a `recall`, por la lectura inversa

`src/associative_memory.py`:

- 248–259: `DirectoryMemory.recall_domain` llama a `self._ham.recall_from_right(cue, ...)`.
- 264–268 de `src/hetero_lib/hetero_associative_4d.py`: `recall_from_right` llama a `recall` con el método por defecto `recall_with_sampling_n_search`.
- 270–290: `recall` proyecta, y si hay soporte llama a `optimal_recall`.
- 304–308: `sample_n_search_recall` llama a `reduce`.
- 512–516: `reduce` llama a `choose` por columna.
- 525–545: `choose` muestrea con `random.random()` (línea 538). Es el recall constructivo y estocástico que la línea 27 del documento A dice que "jamás se ejercita en el directorio".

Cronología: A se escribió el 30 de agosto. La lectura inversa apareció en el script de exp8 el 9 de septiembre (commit 4aa996a) y se declaró en `DirectoryMemory` el 14 de septiembre (ddef014, 5532c93). Cuando A se escribió, su afirmación era cierta. Hoy no lo es tal como está escrita.

### 2.2 El ruteo sigue sin llamar a `recall`

Ningún camino del protocolo oficial usa `recall_domain`:

- `src/stage6_interaction.py`, `src/stage7_bidirectional.py`, `src/stage8_mature.py` y `app_tme.py` rutean con `predict`, `route`, `route_multi` y `route_transactive`, que llaman a `project` (línea 142 de `associative_memory.py`) y toman argmax (línea 204). Deterministas.
- La única llamada a `recall` en el protocolo, `agents[winner].recall(v_q)` en `stage6_interaction.py:520`, es sobre la memoria de contenido del ganador, no sobre el directorio.
- `recall_domain` y `domain_projection` se usan solo en `run_experiment8_directory_recall.py`, `run_experiment9_member_loss.py`, `run_experiment9_probe_phase2.py` y `run_sampling_distributions.py`. En `src/` no hay ningún llamador.

La afirmación de A es cierta del protocolo y falsa del objeto: el directorio, como memoria, tiene una operación entrópica declarada; el ruteo no la usa.

### 2.3 Detalles que afectan la redacción

- **σ**: sigue sin importar, pero por otra razón. `sample_n_search_recall` no usa σ; σ solo entra en `cue_recall` (línea 432) y en las rutas con prototipo (710, 749), que `recall_domain` no invoca. La línea 27 de A acierta en la conclusión y falla en el porqué.
- **`domain_projection`** (237–246) es determinista: solo `project`. La reconstrucción "al 100%" de la línea 12 de B vale para las dos lecturas: el argmax determinista ya clasifica en el dominio correcto en los ocho casos (`results/experimento8/README.md:52`); el muestreo agrega dispersión, no clase.
- **`entropy()`** (265–277) es la entropía del balance de cuentas entre agentes, como dice A en la línea 29. Los reportes en LaTeX (`.tex8/secciones/03_arquitectura.tex:454-465`, `04_metodologia.tex:214`, `02_marco_teorico.tex:275-276`) la usan solo en ese sentido. No afirman ni niegan que el directorio sea entrópico; no dependen de ninguna de las dos posiciones.
- **Cuánto muestrea la lectura inversa**, con la pista nan y semillas (`CONTEXTO_SEP2026.md:97`, `results/experimento9/sonda_fase2.json`): 9.34 niveles vivos por coordenada y 2.78 bits en el directorio visual; dispersión entre sorteos 27.4 contra 32.1 de la memoria de contenido condicionada por etiqueta. La entropía del directorio está en acto, y es del mismo orden que la del contenido.

## 3. Dónde está la contradicción exactamente

No es que A y B describan hechos distintos. Los hechos son compatibles: el ruteo es determinista y la lectura inversa es estocástica. La contradicción está en tres frases de A que niegan la existencia de lo que B usa como evidencia central:

| A dice | B y el código dicen |
|---|---|
| "nunca llama a `recall`" (27) | `recall_domain` llama a `recall_from_right` |
| "nunca opera sobre sus distribuciones [...] Entropía en potencia, nunca en acto" (61) | exp8 y exp9 muestrean de esas distribuciones; 2.78 bits en acto |
| "la maquinaria entrópica del sustrato deliberadamente no se ejercita ahí" (92) | está declarada en la clase (`recall_domain`) y documentada en `README.md:67` |

Y en una frase de B que A calificaría de error de categoría:

| B dice | A dice |
|---|---|
| "El directorio contiene contenido" (12); "es metamemoria [...] basta para responder en su ausencia" (130) | "la hetero asocia contenidos; el directorio designa" (69); "un directorio entrópico fallaría en su única tarea" (69) |

El punto de choque real es este: B convierte la lectura inversa en una **capacidad** del directorio (la política "descripción" de exp9 responde con la clase correcta el 100% de las veces y supera al especialista en fidelidad, `CONTEXTO_SEP2026.md:90`). A sostiene que el directorio **no debe** tener esa capacidad porque su tarea es nombrar. Si la descripción sostiene las respuestas del grupo cuando falta un especialista, el directorio hace algo más que designar.

## 4. Lo que depende de cada posición

### Depende de A (habría que tocar si A cae)

- `discusion_directorio_entropico.md` líneas 27, 61, 69, 92 (las citadas).
- Nada en `src/`, `results/*/README.md` ni `.tex*`. La recomendación de A (línea 92) nunca se aplicó a los reportes: ningún `.tex` glosa `entropy()` como "entropía del balance".

### Depende de B (habría que tocar si B cae)

- `discusion_marco_teorico_directorio.md` líneas 12, 39, 43, 55 (el principio reformulado), 105, 107, 130, 131, 181, 185.
- `README.md` línea 13 ("read backwards, what does this agent know? (`recall_domain`)") y 67–68 ("Inverse read declared").
- `results/experimento8/README.md`: todo el método (línea 4) y las secciones "Las tres condiciones no se distinguen" (12–28), "Lo recuperado no es una copia" (30–43) y "Cuánta indeterminación resuelve el recall" (45–52).
- `results/experimento9/README.md` líneas 11, 62, 82, 92 (la política "descripción" y su consecuencia para el TME).
- `CONTEXTO_SEP2026.md` líneas 13, 90, 97.
- `src/associative_memory.py` 221–259: `_identity_cue`, `domain_projection`, `recall_domain`. Si B cae, siguen siendo válidas como sondas, pero el docstring de `recall_domain` ("Es el sentido quién → qué, simétrico del ruteo") las presenta como operación de la memoria, no como sonda.
- Cuatro scripts: `run_experiment8_directory_recall.py`, `run_experiment9_member_loss.py`, `run_experiment9_probe_phase2.py`, `run_sampling_distributions.py`.

B tiene mucho más apoyado encima que A.

## 5. Tres salidas posibles

### 5.1 Restringir A al protocolo (cambio mínimo)

Reescribir las tres frases de A para que hablen del ruteo y no del objeto:

- 27: "el **ruteo** nunca llama a `recall`; la lectura inversa `recall_domain` (exp8, exp9) sí, y no forma parte del protocolo".
- 61: "Entropía en potencia en el ruteo; en acto solo en la lectura inversa, que es diagnóstica".
- 92: "la maquinaria entrópica del sustrato no se ejercita en el ruteo".

Y añadir a A un párrafo que la propia B ya contiene en germen (línea 35): la relación del directorio tiene dos lados. El izquierdo es icónico (la pista, con métrica); el derecho es indicial (la identidad, sin métrica). Leer de izquierda a derecha es rutear: indeterminación en el lado derecho sería error, así que argmax. Leer de derecha a izquierda es describir: indeterminación en el lado izquierdo es generalización, así que muestreo. El principio "la entropía vive en el ícono, la decisión en el índice" (B, línea 55) queda intacto y explica por qué la misma relación es nítida en un sentido y entrópica en el otro.

Costo: tres frases y un párrafo en A. B no cambia. La frase de A "un directorio entrópico fallaría en su única tarea" (69) queda como está, porque habla del ruteo.

Lo que esta salida no resuelve por sí sola: la sección 5 de A ("Dejar de presentar el directorio como memoria heteroasociativa entrópica") pide una cosa y B (línea 43, "es la tesis") pide la contraria. Hay que elegir una redacción para los reportes. La compatible con las dos: *el directorio es una heteroasociativa completa; el protocolo solo ejercita su lectura determinista, y la lectura entrópica se usa para medir qué guarda.*

### 5.2 Mantener A fuerte y degradar B

Tratar `recall_domain` como sonda experimental, no como operación del directorio, y quitar de B la idea de que el directorio "contiene contenido" y "basta para responder". La política "descripción" de exp9 pasa a ser una medición de qué hay en la relación, no una capacidad del grupo.

Costo: todo lo listado en 4 bajo B. Además, la reformulación de Russell (B, línea 105: la familiaridad es cobertura del reconocimiento, no fidelidad de la reproducción) se apoya en que la descripción reproduce igual que el especialista; si la descripción deja de ser una capacidad, esa reformulación pierde su evidencia y la tesis A del marco vuelve a estar sin resolver.

### 5.3 Dejar los dos documentos como están, con una nota cronológica

Agregar a A una nota de que el 14 de septiembre se declaró la lectura inversa y remitir a B.

Costo: mínimo. Riesgo: un lector que compare las líneas 27 y 61 de A con la línea 12 de B verá una contradicción sin resolver en dos documentos de la misma tesis con quince días de diferencia. Es la salida que un revisor adversarial señalaría primero.

## 6. Lo que no es contradicción y no hay que tocar

- "No es MINERVA" (A, 20–22): sigue siendo cierto. La lectura inversa devuelve una muestra de la relación fundida, no una traza.
- "Es una tabla" (A, 31–38): sigue siendo cierto del ruteo. La lectura inversa usa el lado izquierdo, donde sí hay estructura métrica, y exp7 mostró que no hay acoplamiento rasgo-rasgo. Las dos cosas son compatibles.
- `entropy()` como balance de cuentas (A, 29): cierto y sin cambios en el código.
- El principio de la línea 79 de A y el de la línea 55 de B: son el mismo principio con dos vocabularios. B lo reformuló, no lo contradijo.
