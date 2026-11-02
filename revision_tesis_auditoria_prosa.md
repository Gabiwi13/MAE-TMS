# Propuesta viejo/nuevo: la tesis contra los resultados actuales (auditoría del 29 oct)

**Estado:** pendiente de aprobación. Nada aplicado a `.tex8`. Las cifras de exp11 se actualizaron el 1 nov con los resultados de una sola hetero (`revision_una_hetero_prosa.md` §7).

Corrige los hallazgos de `auditoria_redaccion_29oct.md`. Complementa `revision_pesos_homo_principal_prosa.md` y no repite lo que ella ya cubre. La redactaron tres agentes por archivo, cada cambio con su fuente. Las cifras que cambian el significado las verifiqué contra los archivos de resultados.

- **Parte 1:** resumen, introducción, marco teórico y arquitectura (28 cambios, 20 de significado).
- **Parte 2:** metodología, resultados y figuras.
- **Parte 3:** discusión y conclusiones (16 cambios).

## Cambios al código hechos con esta revisión

- `src/stage8_mature.py`: una consulta rechazada por la compuerta de contenido contaba como coincidencia si el directorio apuntaba al mismo agente. Ahora no cuenta. Re-corrida la etapa 8: la fidelidad sigue en 16/16, porque ninguna de las 16 consultas se rechaza.
- Docstrings de `stage5_fill.py`, `stage6_interaction.py` y `stage8_mature.py` que describían 4 variantes, el registro en todos los agentes y la lectura de un solo directorio.

## Decisiones que necesito de ti

**Regla (1 nov).** En el `.tex8` va solo el estado actual: la historia de versiones sale («la versión anterior», «la de julio», «con 4 variantes»), salvo el cambio de arquitectura de `revision_una_hetero_prosa.md`. Las comparaciones que son el resultado de un experimento descrito en la tesis (ablación, exp11, exp13) se quedan. Los textos nuevos de esta propuesta ya siguen la regla, salvo 1f y 2i, que dependen de las decisiones 5 y 9.

1. **98.75 % (introducción):** es de una versión anterior; con la regla, se quita.
2. **93.0 % del resumen:** sale de la ablación, que usa un directorio compartido, no el protocolo perspectival. ¿Se dice?
3. **El puente descartado:** la introducción habla del TME y la arquitectura del `M^H_dom` del agente de entrada. Hay que elegir uno.
4. **(Reemplazada por `revision_una_hetero_prosa.md`: una sola memoria de contenido por módulo.)** **Las cinco memorias son redundantes en parte.** La marginal derecha de la hetero es idéntica a la homo latente, celda por celda; la izquierda tiene el mismo soporte que la homo de labels, con conteos proporcionales. Lo verifiqué en `models/` (apple y horse). ¿Se discute en el capítulo 6?
5. **Rescate léxico:** resuelta el 1 nov. Se volvió a medir con el sistema actual: +21.7 puntos sobre 46 consultas afectadas (43/46 contra 33/46). Ver 1f y A12.
6. **Candidatos de pear y tomato:** el caché da 11 → 68 y 12 → 86; la tesis dice 70 y 93, que solo están en un mensaje de commit.
7. **τ cierra 90 u 88 %** según se cuente: alguna clase ajena la acepta (137/152) o la clase propia no la acepta (88/100).
8. **Figura 15:** regenerarla aplicando τ. La actual muestra aceptada la fuga que τ cierra.
9. **Costo computacional:** con la regla no se dejan los tiempos de 4 variantes. Volver a medir el pipeline (etapas 1–8) con el sistema actual en una carpeta aparte, o quitar la tabla. La fila de la batería sale en cualquier caso.
10. **Recorte del min–max:** 6 de 1 638 400 componentes. Lo calculó un agente sobre `models/` y no está en `results/`. ¿Se incluye?
11. **El 50 % de la binarización por signo** no tiene fuente: se quita.
12. **exp11, imagen→texto:** el protocolo responde 81.2 % porque ese script forma el directorio visual sin variantes. ¿Se dice?
13. **Las 16 variantes se eligieron mirando exp13**, que mide sobre test. ¿Se declara en la limitación (f)?
14. **Wegner (1987):** verificar si dice literalmente «todos los miembros».
15. **En la evocación,** una palabra compartida por dos vocabularios cuenta como acierto para las dos clases.
16. **La figura de la fase temprana** dibuja flechas a todos los agentes: hay que rehacerla.

---

# Propuesta viejo/nuevo, parte 1: resumen, introducción, marco teórico y arquitectura (`.tex8`)

**Estado:** pendiente de aprobación. Nada aplicado.

**Alcance.** `main.tex` (resumen), `01_introduccion.tex`, `02_marco_teorico.tex` y `03_arquitectura.tex`. Corrige los hallazgos T1, T3–T7 y T9 de `auditoria_redaccion_29oct.md` y sus puntos de precisión en estos archivos. Lo que ya cubre `revision_pesos_homo_principal_prosa.md` (tabla de calibración, ι × κ, 04–07) no se repite aquí.

**Fuentes del núcleo.** Commit d0df16c (re-corrida con pesos homo):
- fase A 99.9 %;
- ruteo visual de test 631/656 = 96.2 % con 2 falsos;
- rechazo 3.5 %;
- evocación top-3 97.4 %;
- fidelidad 16/16.

La etapa 7 no deja JSON; las cifras se usan tal cual.

**Lecturas de `models/` hechas para esta propuesta.** Solo lectura de los pickles, sin correr ninguna etapa. Los scripts fueron temporales y no se versionaron:
- un script temporal no versionado (`leer_dirs.py`): conteos y entropía de los 18 directorios;
- un script temporal no versionado (`counts_vs_rel.py`): `_counts` contra la masa de la relación;
- un script temporal no versionado (`marginales.py`): marginales de la hetero de contenido contra las homo.

Resultados:

| directorio | conteos | entropía (bits) |
|---|---|---|
| TME visual (registro completo) | [2048, 2016, 2016, 2016, 2016, 2032, 2048, 2048] | 3.000 |
| TME texto (16 consultas de la etapa 6) | [12, 6, 6, 7, 5, 5, 4, 7] | 2.920 |
| visual de cada agente | 2016–2048 propios, 144–368 de cada otro; los ocho conteos > 0 en los ocho | 2.223 (pear) – 2.412 (cup) |
| texto de apple, car, horse | solo se conocen a sí mismos | 0 |

- En los 18 directorios, la masa de la columna «conoce» de cada agente es igual a `_counts`, en todas las características.
- La marginal derecha de `M^H_dom` coincide celda a celda con `M^R_dom` (apple y horse, 3200 registros).
- La marginal izquierda tiene el mismo soporte que `M^L_dom`, con conteos proporcionales: factor 32–33 en apple y 22–23 en horse.

---

## 1. `main.tex` (resumen)

### M1. Directorios perspectivales (líneas 64–66)

**Viejo:**
> Un mediador inicial (TME) coordina las interacciones tempranas y deja de ser necesario cuando cada agente construye sus propios directorios internos de especialización, uno por modalidad: textual y visual.

**Nuevo:**
```latex
Un mediador inicial (TME) coordina las interacciones tempranas y deja de ser necesario
cuando cada agente construye sus propios directorios internos de especialización, uno
por modalidad (textual y visual), con las transacciones en que participa.
```
**Fuente:** `src/stage6_interaction.py:259–279` (`register_transaction`: registran la entrada, el ganador y el TME).

**Por qué:** el resumen describe directorios sin decir que cada agente registra solo lo que presenció; desde el 14 de septiembre (a423950) es así.

### M2. Cifras del sistema (T1, líneas 74–79)

**Viejo:**
> Con ocho agentes, el sistema alcanza una precisión temprana del 88.0\% y una precisión madura del 93.2\% con la lectura normalizada B1 del directorio (banco de 411 consultas, $N{=}400$, 5 semillas), con el sesgo histórico hacia el agente \textit{apple} reducido a una participación del 13.0\% (ideal 12.5\%). El hemisferio visual enruta el 75.0\% de las imágenes de prueba con \textbf{cero falsos enrutamientos} y un directorio visual perfectamente balanceado (3.000 de 3.000 bits).

**Nuevo:**
```latex
Con ocho agentes, el sistema alcanza una precisión temprana del 90.0\% y una precisión
madura del 93.0\% con la lectura normalizada B1 del directorio (banco de 411 consultas,
$N{=}400$, 5 semillas), con el sesgo histórico hacia el agente \textit{apple} reducido
a una participación del 13.8\% (ideal 12.5\%).
El hemisferio visual enruta el 96.2\% de las imágenes de prueba (631 de 656), con un
rechazo del 3.5\% y dos falsos enrutamientos, y el registro visual completo del grupo
queda perfectamente balanceado (3.000 de 3.000 bits).
```
**Fuente:**
- `results/ablation_mdir_bias/ablation_report.md:40` (B1, N=400: temprana 90.00 %, madura 93.00 %);
- `ablation_metrics.csv`, `winner_pct_apple` = 0.1375 en las 5 semillas de B1 N=400;
- ruteo, rechazo y falsos: commit d0df16c;
- 3.000 bits: `models/tme.pkl`, `mem_dir_R`.

**Por qué:**
- el ruteo visual pasa de 75.0 a 96.2 % y ya no tiene cero falsos;
- el 3.000 es del registro completo del TME, no de los directorios de los agentes (2.22–2.41 bits): «un directorio visual» perfectamente balanceado ya no describe lo que rutea.

---

## 2. `01_introduccion.tex`

### I1. Actualización del directorio (líneas 17–18)

**Viejo:**
> Primero, la \emph{actualización del directorio}: tras cada interacción, todos los miembros, incluso quienes no respondieron directamente, registran quién supo responder.

**Nuevo:**
```latex
Primero, la \emph{actualización del directorio}: tras cada interacción, los
miembros que la presenciaron registran quién supo responder.
```
**Fuente:** `src/stage6_interaction.py:259–279`.

**Por qué:** el sistema ya no registra en todos; la introducción no debe presentar como modelo lo que el sistema dejó de hacer. Ver duda 2.

### I2. Cifra del reporte previo (líneas 26–29)

**Viejo:**
> Un reporte previo de este proyecto mostró que un sistema de tres agentes especialistas sobre memorias asociativas puras desarrolla el directorio transactivo de Wegner por interacción acumulativa, alcanzando una precisión madura del 98.75\% en tres categorías de ETH-80.

**Nuevo:**
```latex
Un reporte previo de este proyecto mostró que un sistema de tres agentes especialistas
sobre memorias asociativas puras desarrolla el directorio transactivo de Wegner por
interacción acumulativa en tres categorías de ETH-80.
```
**Fuente:** ninguna en `results/`. `results/exp3_corrected_routing/summary.json` se sobrescribió con la corrida de 8 clases (`results/auditoria_integral/report.md:49`).

Se propone quitar la cifra. Alternativa (duda 1): la cifra existe en git, en `git show 0ff1619:results/exp3_corrected_routing/summary.json` (`mature_acc_b1: 0.9875`, 22 jun 2026), y es la que reporta `.tex/secciones/05_resultados.tex:18`. Se podría conservar citando ese reporte.

### I3. Fase madura con directorios perspectivales (líneas 47–50)

**Viejo:**
> Conforme cada agente acumula registros en sus memorias de directorio internas (una textual y una visual), el TME deja de hacer falta: en la fase madura, cualquier agente puede determinar a quién reenviar una consulta desconocida, sea una frase o una imagen, sin intervención del mediador.

**Nuevo:**
```latex
Conforme cada agente acumula en sus memorias de directorio internas (una textual y una
visual) las transacciones en que participa, el TME deja de hacer falta: en la fase
madura, cualquier agente puede determinar, con su directorio y los de los agentes que
conoce, a quién reenviar una consulta desconocida, sea una frase o una imagen, sin
intervención del mediador.
```
**Fuente:** `src/stage6_interaction.py:282–327` (`route_transactive`).

**Por qué:** el agente de entrada no decide solo con su directorio (T4).

### I4. «Sin cambios en el mecanismo» (líneas 75–76)

**Viejo:**
> Los resultados muestran que los directorios, la lectura normalizada B1, el rechazo por containment y la coordinación punto a punto escalan sin cambios en el mecanismo.

**Nuevo:**
```latex
Los resultados muestran que los directorios, la lectura normalizada B1, el rechazo
por containment y la coordinación punto a punto escalan a ocho agentes; el protocolo
de registro y de coordinación cambió en esta versión (contribución~3).
```
**Fuente:** a423950 (registro por transacción y ruteo transactivo, 14 sep); `src/stage6_interaction.py:259–327`.

**Por qué:** frente a la versión de tres agentes, la coordinación sí cambió.

### I5. Efecto de la cuantización (líneas 82–83)

**Viejo:**
> Este cambio de representación elevó la precisión temprana de 8 clases del 50\% al rango de 85--88\% sin tocar la maquinaria asociativa.

**Nuevo:**
```latex
Con esta representación, sin tocar la maquinaria asociativa, la precisión temprana de
8 clases es del 90.0\%.
```
**Fuente:**
- 90.0: `results/ablation_mdir_bias/ablation_report.md:40`;
- 88.0: `git show 9f50751^:results/ablation_mdir_bias/ablation_report.md`, línea 36 (B1, N=400, temprana 88.00 %). No está en el `results/` actual;
- el 50 % no tiene archivo y se quita; el rango «85–88» tampoco tiene fuente.

**Por qué:** sin el 50 % se pierde el «desde»; la frase solo puede decir a dónde llegó. Si el autor tiene el archivo del 50 %, se puede restituir.

### I6. Contribución 3 (líneas 85–90)

**Viejo:**
> \item \textbf{Directorio visual por agente.} Cada agente incorpora un directorio hetero-asociativo visual propio ($M^R_{\mathrm{dir}}$), de modo que una imagen puede entrar por \emph{cualquier} agente y ser redirigida punto a punto al especialista, replicando para la modalidad visual la coordinación de recuperación de Wegner. La alternativa de un puente por el TME traducía 0\% y fue descartada.

**Nuevo:**
```latex
    \item \textbf{Directorios perspectivales por agente.}
    Cada agente incorpora, junto al de texto, un directorio hetero-asociativo visual
    propio ($M^R_{\mathrm{dir}}$), y en ambos registra solo las transacciones en que
    participó, como agente de entrada o como ganador.
    Una frase o una imagen puede entrar por \emph{cualquier} agente, que suma su
    directorio y los de los agentes que conoce y la redirige punto a punto al
    especialista, replicando para las dos modalidades la coordinación de recuperación
    de Wegner.
    La alternativa de un puente por el TME se evaluó y fue descartada.
```
**Fuente:**
- `src/stage6_interaction.py:259–327`;
- `src/stage7_bidirectional.py:195–200` (fase A: registran entrada, ganador y TME);
- el «0 %» no tiene fuente (ningún archivo de `results/` lo mide) y se quita.

**Por qué:** el registro perspectival y el ruteo agregado son lo nuevo de esta versión y la contribución no los nombraba. Ver duda 4 sobre qué puente era.

### I7. Código byte-idéntico (líneas 95–96, opcional)

**Viejo:**
> se verificó que el código de Pineda \& Morales permanece byte-idéntico,

**Nuevo:**
```latex
se verificó que el código de Pineda \& Morales permanece byte-idéntico (salvo una
guarda que evita cargar sus clasificadores y no toca ninguna operación de memoria),
```
**Fuente:**
- `results/auditoria_integral/report.md:11` («byte-idéntico al upstream […] salvo el guard documentado `fold is not None`»);
- `src/hetero_lib/hetero_associative_4d.py:68`.

---

## 3. `02_marco_teorico.tex`

### F1. Qué κ se barre (líneas 78–80)

**Viejo:**
> El parámetro $\kappa$ define un umbral de reconocimiento relativo: se considera reconocido si el peso medio $\bar{w} \geq \kappa \cdot \bar{\mu}$, donde $\bar{\mu}$ es la media global de la memoria.

**Nuevo:**
```latex
El parámetro $\kappa$ define un umbral de reconocimiento relativo: en la memoria
homo-asociativa se considera reconocido si el peso medio $\bar{w} \geq \kappa \cdot \bar{\mu}$,
donde $\bar{\mu}$ es la media global de la memoria.
La hetero-asociativa de referencia define el criterio solo para un par de pistas; con
una sola pista, este trabajo lo aplica a la proyección (Sección~\ref{sec:hetero4d}):
compara la activación media por celda de $\Pi$, por coordenada de la pista, con
$\kappa \cdot \bar{\mu}$ de la memoria de contenido.
Ese es el $\kappa$ que barre la Sección~\ref{sec:param-iota-kappa}; el de la memoria
homo-asociativa no interviene, porque el sistema usa sus pesos y no su decisión.
```
**Fuente:**
- `src/hetero_lib/associative.py:198–203` (criterio homo);
- `src/hetero_lib/hetero_associative_4d.py:233–241` (criterio hetero, para el par `cue_a, cue_b`);
- `run_experiment2_iota_kappa.py:98–101, 124–130, 136–139` (`gate_ratio`);
- `src/associative_memory.py`, `HomoAssociativeMemory.recog_weights`, que descarta el booleano.

**Por qué:** la definición del marco no era la que actúa en el barrido.

### F2. Pesos y cinco memorias (líneas 200–203)

**Reemplazada por `revision_una_hetero_prosa.md` §1c.** Se deja como registro.

**Viejo:**
> Los pesos $w'_i$ ponderan la suma por la frecuencia con que cada característica de la pista ha sido observada en la memoria homo-asociativa: características muy frecuentes en la pista pesan más, lo cual permite que la memoria homo-asociativa module la hetero-asociativa de forma nativa y justifica la arquitectura de cinco memorias por agente.

**Nuevo:**
```latex
Los pesos $w'_i$ ponderan la suma por la frecuencia con que cada característica de la pista
ha sido observada en la memoria homo-asociativa: características muy frecuentes en la pista
pesan más, lo cual permite que la memoria homo-asociativa module la hetero-asociativa
de forma nativa.
```
**Fuente:** la de F3.

**Por qué:** la justificación de las cinco memorias se reformula en F3.

### F3. «La hetero no genera pesos» (T9, líneas 218–227)

**Reemplazada por `revision_una_hetero_prosa.md` §1e.** Se deja como registro.

**Viejo:**
> \subsubsection*{Asimetría entre dominios}
> La memoria homo-asociativa de un dominio modela la \emph{distribución marginal} de ese dominio: genera pesos $w_i$ que reflejan cuán típica es una pista dentro de ese espacio. La memoria hetero-asociativa, en cambio, modela la \emph{distribución conjunta} de dos dominios y, por construcción, \textbf{no genera pesos por característica} del dominio derecho. Esta asimetría es propia del modelo y justifica que cada agente en EAM-TMS requiera \emph{cinco} memorias: dos homo-asociativas (una por dominio, como árbitros de pertenencia y fuente de pesos), una hetero-asociativa de contenido, y dos hetero-asociativas de directorio (una de texto y una visual, una por modalidad de pista).

**Nuevo:**
```latex
\subsubsection*{Marginales y pesos}

La memoria homo-asociativa de un dominio modela la \emph{distribución marginal} de ese
dominio: genera pesos $w_i$ que reflejan cuán típica es una pista dentro de ese espacio.
La memoria hetero-asociativa modela la \emph{distribución conjunta} de dos dominios, y
las marginales están contenidas en ella: sumando la relación sobre el otro dominio se
obtiene cuántas veces se registró cada valor en cada característica, lo mismo que daría
una memoria homo-asociativa llenada con las mismas pistas.
Los directorios, que no tienen memoria homo-asociativa propia, toman sus pesos de esa
lectura.
Que cada agente en EAM-TMS tenga \emph{cinco} memorias es, por tanto, una decisión de
diseño y no una exigencia del modelo: dos homo-asociativas (una por dominio, como
árbitros de pertenencia de cada dominio por separado y fuente de pesos), una
hetero-asociativa de contenido, y dos hetero-asociativas de directorio (una de texto y
una visual, una por modalidad de pista).
```
**Fuente:**
- `src/associative_memory.py:60–76` (`relation_weights`) y `187–189` (`DirectoryMemory.weights`);
- en `models/`, la marginal derecha de `M^H_dom` es igual a `M^R_dom` y la izquierda proporcional a `M^L_dom` (cabecera de este archivo).

**Por qué:** la frase vieja es falsa. La asimetría que justificaba «requiera cinco memorias» no existe; las cinco memorias se sostienen como diseño. Ver duda 5.

### F4. Wegner, actualización del directorio (líneas 245–250)

**Viejo:**
> tras cada interacción de recuperación exitosa, \emph{todos} los miembros del grupo, incluso quienes no respondieron, actualizan su directorio anotando quién fue el especialista. Este proceso distribuye la información de especialización incluso a los miembros que no participaron activamente en la respuesta.

**Nuevo:**
```latex
    tras cada interacción de recuperación exitosa, los miembros actualizan su
    directorio anotando quién fue el especialista.
    En este sistema la actualización es perspectival: anotan la interacción quienes
    participaron en ella, de modo que cada miembro sabe de los demás lo que presenció
    (Sección~\ref{sec:componentes}).
```
**Fuente:** `src/stage6_interaction.py:259–279`.

**Por qué:** igual que I1. Ver duda 2.

### F5. Entropía máxima como estado deseable (líneas 275–281)

**Viejo:**
> La \textbf{entropía del directorio} resume el estado del sistema transactivo: un directorio con entropía máxima $\log_2 K$ (siendo $K$ el número de agentes; $\log_2 8 = 3$ bits en esta versión) indica especialización perfectamente balanceada; una entropía baja indica colapso hacia un solo agente o formación incompleta. A diferencia de la entropía de una memoria de contenido, aquí el diagnóstico se hace sobre la \emph{distribución de registros entre agentes}, y el estado deseable es el máximo: que el grupo reparta la experticia de forma pareja.

**Nuevo:**
```latex
La \textbf{entropía del directorio} resume el estado del sistema transactivo.
En el registro completo del grupo, la entropía máxima $\log_2 K$ (siendo $K$ el número
de agentes; $\log_2 8 = 3$ bits en esta versión) indica especialización perfectamente
balanceada, y una entropía baja, colapso hacia un solo agente o formación incompleta.
A diferencia de la entropía de una memoria de contenido, aquí el diagnóstico se hace
sobre la \emph{distribución de registros entre agentes}, y en el registro completo el
estado deseable es el máximo: que el grupo reparta la experticia de forma pareja.
En el directorio de cada agente no lo es: si cada uno registra lo que presenció, su
directorio se carga hacia sí mismo y queda por debajo del máximo aunque el grupo esté
balanceado.
```
**Fuente:** `models/tme.pkl` y `models/agent_*.pkl`. TME visual 3.000 bits; directorios visuales de los agentes 2.22–2.41 (cabecera).

**Por qué:** el máximo como meta solo aplica al registro completo.

---

## 4. `03_arquitectura.tex`

### A1. Papel de los directorios del TME (líneas 71–72)

**Viejo:**
> El TME conserva además sus propios $M^L_{\mathrm{dir}}$ y $M^R_{\mathrm{dir}}$, usados en la formación temprana.

**Nuevo:**
```latex
El TME conserva además sus propios $M^L_{\mathrm{dir}}$ y $M^R_{\mathrm{dir}}$, con el
registro completo del grupo; sirven de diagnóstico y ningún ruteo los consulta.
```
**Fuente:**
- `src/stage6_interaction.py:236–242` (docstring de `TME`);
- `process_query` decide al ganador por difusión, sin leer el directorio del TME;
- `route_transactive` solo lee directorios de agentes.

**Por qué:** «usados en la formación temprana» sugiere que rutean.

### A2. Quién registra (T3, líneas 73–79)

**Viejo:**
> Cuando se registra un par $(\mathbf{v}_q, g)$, la representación de la pista (semántica en $M_{\mathrm{dir}}$, latente en $M^R_{\mathrm{dir}}$) se asocia al identificador del agente ganador; \emph{todos} los agentes, incluidos los perdedores, registran esta asociación en el directorio de la modalidad correspondiente (\emph{directory updating} de Wegner). Esto permite la coordinación de recuperación de Wegner también para imágenes: una imagen puede entrar por \emph{cualquier} agente, que consulta su propio $M^R_{\mathrm{dir}}$ y redirige al especialista (o rechaza si nadie la contiene).

**Nuevo:**
```latex
Cuando se registra un par $(\mathbf{v}_q, g)$, la representación de la pista (semántica en
$M_{\mathrm{dir}}$, latente en $M^R_{\mathrm{dir}}$) se asocia al identificador del agente
ganador.
Registran la transacción solo quienes participaron en ella: el agente por el que entró
la consulta y el ganador; el TME las registra todas (\emph{directory updating} de Wegner
por transacción).
Los directorios son, por tanto, \emph{perspectivales}: cada agente sabe de los demás lo
que los vio ganar.
En el directorio visual, cada percepción se registra con sus 16 variantes
(Figura~\ref{fig:arq-llenado}) y el mismo ganador.
Esto permite la coordinación de recuperación de Wegner también para imágenes: una imagen
puede entrar por \emph{cualquier} agente, que consulta su $M^R_{\mathrm{dir}}$ y los de los
agentes que conoce y redirige al especialista (o rechaza si nadie la contiene;
Sección~\ref{sec:operaciones}).
```
**Fuente:**
- `src/stage6_interaction.py:259–279`;
- `src/stage7_bidirectional.py:181–200` (`image_variants_to_latents`, las 16 variantes con el mismo `widx`);
- `src/stage5_fill.py:49` (`FILL_VARIANTS = 16`).

**Por qué:** el registro en los nueve directorios solo queda en la ablación y en exp2–4 (`run_ablation.py:331–333`, `run_experiment3.py:123–125`), no en el sistema.

### A3. Cifra del puente (líneas 80–84)

**Viejo:**
> El directorio visual por agente es nuevo en esta versión: la alternativa evaluada previamente (un puente por el $M^H_{\mathrm{dom}}$ del agente de entrada hacia el directorio de texto) no redirige en absoluto cuando el agente de entrada no es el especialista (0\% de traducción), porque la memoria de contenido de un no-especialista no contiene el latente ajeno.

**Nuevo:**
```latex
El directorio visual por agente es nuevo en esta versión: la alternativa evaluada
previamente (un puente por el $M^H_{\mathrm{dom}}$ del agente de entrada hacia el
directorio de texto) no redirige cuando el agente de entrada no es el
especialista, porque la memoria de contenido de un no-especialista
no contiene el latente ajeno.
```
**Fuente:** el «0 %» no tiene archivo en `results/`; se quita junto con «en absoluto».

### A4. Variantes del llenado (T6, pie de la figura de llenado, líneas 169–174)

**Viejo:**
> La rama visual cuantiza los códigos ResNet18; cada imagen de llenado se registra junto con variantes de augmentación (espejo y rotaciones de $\pm12^\circ$). El registro en $M^H_{\mathrm{dom}}$ sigue el esquema \emph{imagen-etiqueta}: la imagen $i$-ésima se registra emparejada con el label $\mathbf{v}_q^{(i \bmod L)}$ de la secuencia expandida por frecuencias (de longitud $L$), de modo que cada clase aporta el mismo número de registros.

**Nuevo:**
```latex
La rama visual cuantiza los códigos ResNet18; cada una de las 200 imágenes de llenado
por clase se registra junto con 15 variantes de augmentación (espejo, rotaciones de
$\pm6^\circ$ y $\pm12^\circ$, el espejo rotado $\pm12^\circ$, escala 0.9 y 1.1, brillo
0.85 y 1.15 y traslaciones de 6 píxeles en cada dirección), 3200 registros por clase.
El registro en $M^H_{\mathrm{dom}}$ sigue el esquema \emph{imagen-etiqueta}:
el latente $i$-ésimo (cada variante cuenta como uno) se registra emparejado con el label
$\mathbf{v}_q^{(i \bmod L)}$ de la secuencia expandida por frecuencias
(de longitud $L$), de modo que cada clase aporta el mismo número de registros.
```
**Fuente:**
- `src/stage5_fill.py:43, 49` (`N_FILL = 200`, `FILL_VARIANTS = 16`);
- `src/stage5_fill.py:78–101` (`augment_variants`);
- `src/stage5_fill.py:193–195` (`label_seq[i % L]` por latente);
- `models/`: 3200 registros en `M^H` y `M^R` de apple y horse.

**Por qué:** el llenado tiene 16 variantes desde el 23 de septiembre, no 4.

### A5. Figura de la fase temprana (T3, líneas 264–265, 268–269 y 278–279)

**Viejo (nodo, 264–265):**
> `{Los 8 agentes y el TME\\ registran $\lambda(\mathbf{v}_q, g)$}`

**Nuevo:**
```latex
    {Entrada, ganador y TME\\ registran $\lambda(\mathbf{v}_q, g)$};
```

**Viejo (nota, 268–269):**
> `{También los perdedores anotan\\(\textit{directory updating}, Wegner)}`

**Nuevo:**
```latex
    {Anota quien participó\\(\textit{directory updating}, Wegner)};
```

**Viejo (pie, 278–279):**
> Los ocho agentes y el propio TME registran el par $(\mathbf{v}_q, g)$ en sus respectivos directorios, incluyendo los agentes perdedores.

**Nuevo:**
```latex
Registran el par $(\mathbf{v}_q, g)$ el agente por el que entró la consulta (al azar),
el ganador y el TME; los demás agentes no presenciaron la transacción.
```
**Fuente:** `src/stage6_interaction.py:527` y `657–661` (entrada con `RandomState(42)`, `register_transaction`).

**Por qué:** igual que A2. Las flechas punteadas que van de «Actualización de directorio» a los tres agentes dibujados siguen sugiriendo registro en todos (duda 9).

### A6. Figura de la fase madura, nodos (T4, T5; líneas 310 y 313)

**Viejo (310):** `{Agente de\\entrada\\(aleatorio)}`

**Nuevo:**
```latex
\node[box, right=of query] (entrada) {Agente de\\entrada};
```

**Viejo (313):** `{$M_{\mathrm{dir}}$ / $M^R_{\mathrm{dir}}$\\lectura B1\\($\xi{=}0$ texto, $\xi{=}2$ visual)}`

**Nuevo:**
```latex
\node[box, right=1.6cm of entrada] (mdir) {$M_{\mathrm{dir}}$ / $M^R_{\mathrm{dir}}$\\propio y de conocidos\\lectura B1 ($\xi{=}0$)};
```
**Fuente:**
- `src/stage7_bidirectional.py:46` (`XI_VISUAL = 0`) y `:231` (entrada visual = agente de la clase siguiente);
- `src/stage8_mature.py:158` (entrada de texto al azar);
- `src/stage6_interaction.py:282–327`.

**Por qué:** ξ = 2 ya no se usa, y la entrada visual no es aleatoria.

### A7. Figura de la fase madura, pie (T4, T5, T7; líneas 358–364)

**Viejo:**
> Fase madura: recuperación punto a punto. Un agente de entrada (seleccionado aleatoriamente) consulta su directorio de la modalidad correspondiente ($M_{\mathrm{dir}}$ para texto con $\xi{=}0$, $M^R_{\mathrm{dir}}$ para imágenes con $\xi{=}2$) mediante la lectura B1 y reenvía directamente al agente destino sin pasar por el TME (dibujado en gris punteado). Si ningún agente obtiene soporte para la pista, el sistema emite un rechazo claro: el grupo no inventa referentes.

**Nuevo:**
```latex
\caption{Fase madura: recuperación punto a punto.
La consulta entra por un agente (al azar en texto; en la evaluación visual, uno que no
es el especialista), que suma la lectura B1 de su directorio de la modalidad
correspondiente ($M_{\mathrm{dir}}$ o $M^R_{\mathrm{dir}}$, ambos con $\xi{=}0$) y la de
los directorios de los agentes que conoce, y reenvía al agente destino sin pasar por el
TME (dibujado en gris punteado); si nadie en ese círculo tiene soporte, la consulta pasa
a los conocidos.
Una imagen cuyo latente no alcanza la energía mínima $\tau$ se rechaza antes de cualquier
memoria, y en texto el destino responde solo si su contenido contiene la pista.
Si ningún directorio alcanzable tiene soporte, el sistema emite un rechazo claro: el
grupo no inventa referentes.}
```
**Fuente:**
- `src/stage6_interaction.py:282–327`;
- `src/stage7_bidirectional.py:46, 224–233`;
- `src/stage8_mature.py:92–101` (doble compuerta);
- `models/latent_energy_threshold.json` (τ).

**Por qué:** describe el ruteo transactivo, ξ = 0 y el umbral de energía, que el texto omitía.

### A8. Conteos del protocolo completo (líneas 431–432)

**Viejo:**
> en la corrida del protocolo completo de 8 clases los conteos finales fueron $[50, 16, 44, 25, 30, 14, 17, 31]$.

**Nuevo:**
```latex
protocolo completo de 8 clases los conteos finales fueron
$[46, 16, 40, 25, 30, 18, 21, 31]$.
```
**Fuente:**
- `results/exp3_corrected_routing/report.md:21`;
- `results/exp4_directory_formation/report.md:14–21`;
- `results/exp2_iota_kappa/report.md:46`.

### A9. Dónde vive `c_k` (líneas 437–439)

**Viejo:**
> Esta es la \textbf{única normalización externa} del sistema de directorios; está encapsulada en la propia memoria de directorio y su necesidad se demuestra empíricamente en la Sección~\ref{sec:calibracion}.

**Nuevo:**
```latex
Esta es la \textbf{única normalización externa} del sistema de directorios.
El conteo $c_k$ lo lleva la memoria de directorio como un contador aparte de la relación,
pero no agrega información: es la masa que la relación acumula en la columna ``conoce''
del agente $k$, igual para cualquier característica.
Su necesidad se demuestra empíricamente en la Sección~\ref{sec:calibracion}.
```
**Fuente:**
- `src/associative_memory.py:172, 185, 205` (`_counts` y la división por `_counts + eps`);
- en los 18 directorios de `models/`, la masa de la columna «conoce» es igual a `_counts` en todas las características (`counts_vs_rel.py`);
- `results/auditoria_integral/report.md:76`.

**Por qué:** la auditoría dice que `_counts` «está fuera de la relación». Es cierto que se guarda aparte, pero su valor sale de la relación. Hay que decir las dos cosas.

### A10. Coordinación transactiva (T4, subsección nueva después de la línea 439)

**Viejo:** (no existe)

**Nuevo:**
```latex
\subsubsection*{Coordinación transactiva de la recuperación}

En la fase madura, el agente de entrada suma la lectura B1 de su directorio y la de los
directorios de los agentes que conoce (los que vio ganar alguna transacción) y reenvía
al de mayor puntuación.
Si nadie en ese círculo tiene soporte, la consulta pasa al conocido con más registros,
que suma a su vez los directorios de sus propios conocidos que aún no se consultaron, y
así hasta encontrar soporte o agotar a los alcanzables; si ninguno lo tiene, el sistema
rechaza.
En texto, la puntuación de cada directorio es la suma de B1 sobre los tokens de la
consulta, y el destino aplica una segunda compuerta: responde solo si su memoria de
contenido contiene alguna de las pistas (Ecuación~\eqref{eq:score-gated}); si no, la
consulta se rechaza.
En imagen, durante la fase A cada agente vio ganar a los otros siete, de modo que el
primer círculo ya reúne los ocho directorios visuales.
```
**Fuente:**
- `src/stage6_interaction.py:282–327` (`known_by` ordena por conteo; la cola antepone a los conocidos);
- `src/associative_memory.py:261–274` (`route_multi`);
- `src/stage8_mature.py:76–101`;
- `models/agent_*.pkl`: los ocho conteos de cada `mem_dir_R` son > 0.

**Por qué:** la tesis decía que el agente de entrada consulta su directorio y reenvía. Hoy suma el suyo y el de sus conocidos, encadena, y en texto aplica doble compuerta.

### A11. Lectura visual estricta y umbral de energía (T5, T7; líneas 441–452)

**Viejo:**
> \subsubsection*{Lectura tolerante del directorio visual ($\xi = 2$)}
> El directorio visual $M^R_{\mathrm{dir}}$ usa la misma lectura B1 con una tolerancia $\xi = 2$: hasta dos coordenadas del latente sin soporte marginal se marcan como \emph{indefinidas} (los centinelas de funciones parciales de la EHAM, Sección~\ref{sec:hetero4d}) y la proyección las omite. Es maquinaria nativa del modelo (funciones parciales), no una relajación externa. El valor $\xi = 2$ proviene de un barrido medido ($\xi \in \{0,\ldots,3\}$): es el punto dulce de cobertura, la ganancia satura en $\xi = 3$ y la especificidad permaneció intacta en todo el rango de aquel barrido, hecho con el llenado de 4 variantes. El directorio de \emph{texto} permanece en $\xi = 0$: la tolerancia allí agravaría la fuga de consultas fuera de dominio (Sección~\ref{sec:limitaciones}).

**Nuevo:**
```latex
\subsubsection*{Lectura estricta del directorio visual y umbral de energía}

El directorio visual $M^R_{\mathrm{dir}}$ usa la misma lectura B1, con $\xi = 0$ como el
de texto.
No tolera huecos porque, en directorios perspectivales, una coordenada sería hueco si
su valor nunca se registró en ese directorio, para ningún módulo, y eso depende de lo
que el dueño del directorio presenció de los demás: la tolerancia no sería una
propiedad del módulo.

Antes de cualquier memoria visual, el latente continuo pasa un umbral de energía: si su
norma es menor que $\tau$, la imagen se rechaza.
El encoder lleva las entradas sin estructura (gris uniforme, desenfoque fuerte, contraste
casi nulo) cerca del origen, donde caen dentro del soporte de \textit{cow}, \textit{dog}
y \textit{horse}.
$\tau = 16.61$ es la norma mínima de los 1600 originales del llenado (18.45) menos un
margen del 10\%; rechaza una de las 1024 percepciones de la fase A y 4 de las 656
imágenes de prueba.
```
**Fuente:**
- ξ = 0: `src/stage7_bidirectional.py:41–46`; `results/experimento10/README.md:9, 74` (la tolerancia como propiedad del grupo);
- definición de hueco: `src/associative_memory.py:223–232` (`support_gaps`);
- barrido sobre test: `results/auditoria_integral/report.md:33–34`;
- τ: `models/latent_energy_threshold.json` (`tau` 16.607, `min_norma_llenado` 18.453, `margen` 0.1, `n` 1600); `src/stage7_bidirectional.py:47–89, 184, 224`;
- rechazos: `results/experimento14/README.md:7–10` (fase A 1 de 1024; test 4 de 656);
- especialistas que aceptan las entradas degeneradas: tabla de `results/experimento14/README.md:43–`.

**Por qué:**
- ξ = 2 dejó de usarse en a423950;
- el umbral de energía no aparecía en la arquitectura;
- la frase sobre el texto en ξ = 0 se quita porque ahora las dos modalidades usan ξ = 0. Si el autor quiere conservar la razón del texto, se puede agregar al final del primer párrafo: «(en texto, además, la tolerancia agravaría la fuga de consultas fuera de dominio; Sección~\ref{sec:limitaciones})».

### A12. Entropía del directorio (líneas 463–466)

**Viejo:**
> Con $K=8$ agentes, el máximo teórico es $\log_2 8 = 3$ bits, alcanzado cuando la especialización es perfectamente balanceada. Una entropía menor indica o bien que un agente acapara el directorio (colapso) o bien que el directorio está poco poblado (formación incompleta).

**Nuevo:**
```latex
Con $K=8$ agentes, el máximo teórico es $\log_2 8 = 3$ bits,
alcanzado cuando la especialización es perfectamente balanceada.
Esa lectura vale para el registro completo del grupo (el del TME y el directorio
compartido de los experimentos de calibración), donde una entropía menor indica o bien
que un agente acapara el directorio (colapso) o bien que está poco poblado (formación
incompleta); el registro visual del TME queda en 3.000 bits.
No vale para el directorio de cada agente: como cada uno registra todo lo que ganó y
solo parte de lo ajeno, su directorio se carga hacia sí mismo por construcción.
Los directorios visuales de los agentes quedan entre 2.22 y 2.41 bits, con 2016--2048
registros propios contra 144--368 de cada otro agente.
```
**Fuente:**
- `models/tme.pkl` y `models/agent_*.pkl` (`leer_dirs.py`; tabla de la cabecera);
- el directorio compartido en calibración: `run_ablation.py:331–333`, `run_experiment3.py:123–125`.

**Por qué:** igual que F5.

### A13. Diccionario de la evocación (línea 485)

**Viejo:**
> Se buscan los 3 vecinos más cercanos de $\hat{\mathbf{v}}_q$ en el diccionario fastText mediante similitud coseno, y se devuelven como labels asociados a la imagen.

**Nuevo:**
```latex
    \item Se buscan los 3 vecinos más cercanos de $\hat{\mathbf{v}}_q$, por similitud
    coseno, entre los labels de los ocho vocabularios de llenado (168 entradas, 159
    palabras distintas), y se devuelven como labels asociados a la imagen.
```
**Fuente:**
- `src/stage7_bidirectional.py:163–167, 139–146` (`all_vecs` es la unión de `load_all_vectors()`, sin alias);
- `label_vectors_*.json`: 21 por clase, 159 claves distintas en la unión.

**Por qué:** la búsqueda no es sobre todo fastText. La auditoría dice «168 labels», pero al unir los diccionarios quedan 159 candidatos distintos.

### A14. Definición de fidelidad (líneas 500–501)

**Viejo:**
> La \textbf{fidelidad} se define como la fracción de consultas en la fase madura en las que el agente de entrada enruta hacia el mismo agente ganador que la fase temprana:

**Nuevo:**
```latex
La \textbf{fidelidad} se define como la fracción de consultas en la fase madura en las
que la coordinación de la recuperación, desde el agente de entrada, llega al mismo
agente ganador que la fase temprana:
```
**Fuente:** `src/stage8_mature.py:76–90, 158–163`.

**Por qué:** el destino ya no lo decide solo el directorio del agente de entrada (T4).

---

## Cuántos cambios hay y cuáles cambian el significado

Son 28 bloques: 2 en el resumen, 7 en la introducción, 5 en el marco teórico y 14 en la arquitectura.

**Cambian el significado (20):**
- M1, M2;
- I1, I3, I4, I6;
- F1, F2, F3, F4, F5;
- A1, A2, A5, A6, A7, A10, A11, A12, A14.

**Solo cifras o precisión (8):**
- I2 y A3 quitan cifras sin fuente;
- I5 corrige la cifra y quita el 50 %;
- I7, A4, A8, A9 y A13 corrigen datos o precisan.

---

## Dudas para el autor

1. **98.75 %** (I2). Quitarla, o conservarla citando el reporte de tres agentes (`.tex`) y el `summary.json` de git (0ff1619).
2. **Wegner y «todos los miembros»** (I1, F4). Si Wegner (1987) dice explícitamente que actualizan todos, conviene conservar la teoría tal cual y solo decir que el sistema implementa la versión perspectival. No lo pude verificar contra el texto.
3. **El 93.0 % del resumen** sale de la ablación, que registra en los nueve directorios (directorio compartido), no del protocolo perspectival oficial. ¿Se declara en el resumen o basta con metodología?
4. **¿Qué puente se descartó?** 01:90 dice «un puente por el TME» y 03:81 «un puente por el $M^H_{\mathrm{dom}}$ del agente de entrada». Hay que elegir uno.
5. **(Reemplazada por `revision_una_hetero_prosa.md`.)** **Cinco memorias** (F3). Con la verificación sobre `models/`, las homo no aportan información que no esté en la hetero de contenido: la marginal derecha es idéntica y la izquierda proporcional. ¿Se conserva la arquitectura como decisión de diseño (lo que propongo) o se discute en 06?
6. **Fidelidad con la doble compuerta.** `stage8_mature.py:163` compara `res["winner"]`. Cuando la compuerta de contenido rechaza, `winner` es el destino que señaló el directorio, así que una consulta rechazada por contenido cuenta como coincidencia si el destino coincide. No sé si afecta al 16/16 sin correr la etapa 8. ¿Debe contar como no coincidencia?
7. **Acierto de la evocación.** Una palabra que comparten dos vocabularios cuenta como acierto para las dos clases (`stage7_bidirectional.py:245`). ¿Se declara?
8. **Docstrings viejos en `src/`** (fuera de la tesis, no los toqué):
   - `stage6_interaction.py:7` («TODOS los agentes registran»);
   - `stage5_fill.py:12` («800 registros/clase») y `:41–42` («4x por imagen»);
   - `stage8_mature.py:5` («consulta su propio directorio»).
9. **Figura de la fase temprana.** Las tres flechas punteadas de «Actualización de directorio» a los agentes siguen dibujando registro en todos. ¿Se dejan con el pie nuevo o se redibuja con solo entrada y ganador?

---

# Propuesta viejo/nuevo, parte 2: metodología y resultados (tesis, `.tex8`)

**Estado:** pendiente de aprobación. Nada aplicado.

**Alcance:** `.tex8/secciones/04_metodologia.tex` y `.tex8/secciones/05_resultados.tex`. Corrige los hallazgos de `auditoria_redaccion_29oct.md` que caen en estas dos secciones. Lo que ya cubre `revision_pesos_homo_principal_prosa.md` no se repite: tabla de calibración, B1/G, apple/pear (97–103), fidelidad 95.2, 71.2/93.5, ι×κ, 208, 231 y variedad L1. El bloque 1f toca la misma línea 175 que el 1b de esa propuesta y ya trae su redacción de κ.

Las líneas son las del archivo actual (`0490eea`).

---

## 1. Metodología (`04_metodologia.tex`)

### 1a. Las 16 variantes del llenado (líneas 36–38)

**Viejo:**
```latex
    Cada imagen se registra junto con variantes de \emph{augmentación} (imagen espejo y
    dos rotaciones de $\pm 12^{\circ}$), lo que densifica la distribución latente
    acumulada sin tocar el mecanismo de la memoria: es más percepción, no otro modelo.
```

**Nuevo:**
```latex
    Cada imagen se registra junto con 15 variantes de \emph{augmentación} (16 patrones
    por imagen, 3200 por clase): espejo; rotaciones de $\pm 12^{\circ}$ de la imagen y
    de su espejo, y de $\pm 6^{\circ}$ de la imagen; escalas de 0.9 y 1.1; brillo de
    0.85 y 1.15, y desplazamientos de 6 píxeles en las cuatro direcciones. Esto
    densifica la distribución latente acumulada sin tocar el mecanismo de la memoria:
    es más percepción, no otro modelo.
```

**Fuente:** `src/stage5_fill.py:49` (`FILL_VARIANTS = 16`) y `:78–101` (`augment_variants`). 3200 filas por clase en `models/instance_latents_*.json` (25 600 en total, `c0a0d61`).

**Por qué:** el texto describe el llenado de 4 variantes, vigente hasta el 23 de septiembre.

### 1b. La fase A visual también registra las 16 (líneas 39–41)

**Viejo:**
```latex
    \item \textbf{Interacciones visuales}: imágenes \texttt{train[200:328]} de cada
    clase, usadas para simular las interacciones de percepción durante la formación del
    directorio visual (1024 imágenes en total, 128 por clase).
```

**Nuevo:**
```latex
    \item \textbf{Interacciones visuales}: imágenes \texttt{train[200:328]} de cada
    clase, usadas para simular las interacciones de percepción durante la formación del
    directorio visual (1024 imágenes en total, 128 por clase). Cada percepción decide
    su ganador con la imagen original y registra sus 16 variantes con ese mismo ganador.
```

**Fuente:** `src/stage7_bidirectional.py:181–200`.

### 1c. Relaciones de ConceptNet (líneas 54–56): hallazgo nuevo, no está en la auditoría

**Viejo:**
```latex
Se consultó ConceptNet~5.7~\cite{speer2017conceptnet} con las relaciones \texttt{IsA},
\texttt{HasProperty}, \texttt{RelatedTo}, \texttt{HasPart}, \texttt{HasA},
\texttt{MadeOf} y \texttt{CapableOf}.
```

**Nuevo:**
```latex
Se consultó ConceptNet~5.7~\cite{speer2017conceptnet} con las relaciones \texttt{IsA},
\texttt{HasProperty}, \texttt{RelatedTo}, \texttt{HasPart}, \texttt{HasA},
\texttt{MadeOf}, \texttt{CapableOf}, \texttt{AtLocation}, \texttt{UsedFor},
\texttt{PartOf}, \texttt{Synonym} y \texttt{SimilarTo}.
```

**Fuente:** `src/stage3_conceptnet.py:35–51` (`RELATIONS`) y `cache/conceptnet_extracted.json`, campo `_meta.relations` (12 relaciones, `2c584fd`, 4 jul).

### 1d. Candidatos de pear y tomato (líneas 59–60)

**Viejo:**
```latex
candidatos de las clases con vocabulario pobre (\texttt{pear} pasó de 11 a 70 candidatos
crudos; \texttt{tomato} de 12 a 93).
```

**Nuevo:**
```latex
candidatos de las clases con vocabulario pobre (\texttt{pear} pasó de 11 a 68 candidatos
crudos; \texttt{tomato} de 12 a 86).
```

**Fuente:** número de claves por clase en `cache/conceptnet_extracted.json`. La versión vigente (`2c584fd`) da pear 68 y tomato 86. La anterior (`git show b281f9c:cache/conceptnet_extracted.json`) da pear 11 y tomato 12.

**Por qué:** 70 y 93 solo aparecen en el mensaje del commit `2c584fd`; el caché versionado en ese mismo commit da 68 y 86. Si se prefiere no dar cifras, la alternativa es «multiplica por seis o siete los candidatos de las clases con vocabulario pobre», con la misma fuente.

### 1e. Escala de cuantización de las etiquetas (línea 74)

**Viejo:** `$S = 0.1864$), se recorta a $[-1, 1]$ y se mapea uniformemente a $m = 16$ niveles.`

**Nuevo:** `$S = 0.1881$), se recorta a $[-1, 1]$ y se mapea uniformemente a $m = 16$ niveles.`

**Fuente:** `models/label_quant_scale.json`: `scale 0.18809`, 159 vectores (sin cambios desde `2c584fd`, 4 jul).

### 1e'. La misma escala en la auditoría de fidelidad (líneas 194–195)

La auditoría no lo marca, pero también es 0.1864. Esa cifra era correcta el 2 de julio: `git show cbe57d8:models/label_quant_scale.json` da 0.18644 con 133 vectores. Solo hay que fecharla.

**Viejo:**
```latex
escala global de cuantización} de todos los labels ($S = 0.2276$ con el sintético
frente a $S = 0.1864$ real).
```

**Nuevo:**
```latex
escala global de cuantización} de todos los labels ($S = 0.2276$ con el sintético
frente a $S = 0.1864$ sin él, con el vocabulario de entonces; con el vocabulario
actual, $S = 0.1881$).
```

**Fuente:** `cbe57d8:models/label_quant_scale.json` y `models/label_quant_scale.json`. El 0.2276 no lo verifiqué: no queda ningún archivo con esa escala.

### 1f. Rescate léxico (líneas 91–96): medido de nuevo con el sistema actual

Se midió el 1 nov con `run_rescate_lexico.py` (`results/rescate_lexico/`): el ganador temprano de las 411 consultas del banco, con la regla y con `tokenize_query` sin sus dos vías de rescate. La regla solo agrega tokens en las 411.

**Viejo:**
```latex
El efecto de esta regla está medido y se declara como parte del protocolo: sobre el
banco completo afecta a 42 consultas, que con el rescate aciertan 41/42 (97.6\%) y
sin él 31/42 (73.8\%) --- \textbf{+23.8 puntos sobre las consultas afectadas}, con
los diez cambios de ganador moviéndose todos hacia la clase correcta (los tokens
rescatados son precisamente los más discriminativos: \texttt{bark}, \texttt{moo},
\texttt{saddle}, \texttt{wheel}, \texttt{brake}\ldots).
```

**Nuevo:**
```latex
El efecto de esta regla está medido y se declara como parte del protocolo: sobre el
banco completo afecta a 46 consultas, que con el rescate aciertan 43/46 (93.5\%) y
sin él 33/46 (71.7\%) --- \textbf{+21.7 puntos sobre las consultas afectadas}; sin
él, cuatro de ellas se rechazan. Los diez cambios de ganador van todos hacia la clase
correcta, y los tokens rescatados son de los más discriminativos (\texttt{bark},
\texttt{moo}, \texttt{canine}, \texttt{riding}, \texttt{wheel}\ldots).
```

**Fuente:** `results/rescate_lexico/resumen.json`. En todo el banco: 371 aciertos con la regla y 361 sin ella. La regla sigue en `src/stage6_interaction.py:107–113`.

`06_discusion.tex:268` cita la misma cifra: ver A12.

### 1g. Rango min–max del latente (líneas 137–139)

**Viejo:**
```latex
Los vectores latentes se cuantizaron a $m = 32$ niveles mediante normalización global
min-max con un margen del 10\%, calculada exclusivamente sobre el pool de llenado
(\texttt{train[0:200]} por clase).
```

**Nuevo:**
```latex
Los vectores latentes se cuantizaron a $m = 32$ niveles mediante normalización global
min-max con un margen del 10\%, calculada exclusivamente sobre el pool de llenado
(\texttt{train[0:200]} por clase) con cuatro de sus variantes (original, espejo y
rotaciones de $\pm 12^{\circ}$); lo que cae fuera del rango se recorta al nivel extremo.
```

**Fuente:**
- Las estadísticas se leen del caché `models/latent_global_stats.json` (`src/stage5_fill.py:124–127`) y no cambian desde `af2c6de` (5 jul). El recorte está en `quantize_latent_global` (`:150–156`).
- Lo verifiqué contra `models/instance_latents_*.json`. El rango guardado coincide exactamente (diferencia 0.0) con el min–max más el 10 % de margen de las variantes 0–3, y difiere hasta en 7.5 del de las 16.
- Fuera del rango quedan 6 componentes de 1 638 400 (25 600 latentes × 64), en 5 latentes, y todas son de variantes nuevas.
- El cálculo es mío y no está en `results/`. Lo reproduce este comando:
  ```
  python -I -c "import json,numpy as np;s=json.load(open('models/latent_global_stats.json'));a,b=np.array(s['global_min']),np.array(s['global_max']);Z=np.concatenate([np.array(json.load(open(f'models/instance_latents_{c}.json'))) for c in ['apple','car','cow','cup','dog','horse','pear','tomato']]);print(((Z<a)|(Z>b)).sum(), Z.size)"
  ```

**Por qué:** el texto da a entender que el rango sale del llenado actual. El método no cambia: solo se dice de qué llenado sale el rango.

### 1h. Umbral de energía (nuevo párrafo, después de la línea 140)

**Viejo:** (no existe)

**Nuevo:**
```latex
Antes de llegar a la memoria, toda percepción pasa un \textbf{umbral de energía}: si
la norma de su latente continuo es menor que $\tau = 16.61$, se rechaza sin consultar
la memoria.
$\tau$ es el mínimo de esa norma sobre las 1600 imágenes originales del llenado
(18.45) con un margen del 10\%. Se introdujo porque el encoder lleva las entradas sin
estructura (gris uniforme, desenfoque, contraste nulo) cerca del origen, donde la
memoria les da soporte (experimento 14, Sección~\ref{sec:hemisferio-visual}).
Es un criterio previo a la EAM y tiene costo: no rechaza ninguna imagen del llenado,
pero sí 1 de las 1024 de la fase A y 4 de las 656 de prueba, cuatro vistas de vaca
que el directorio ruteaba bien y que su especialista aceptaba.
```

**Fuente:**
- `models/latent_energy_threshold.json`: `tau 16.607`, `min_norma_llenado 18.453`, `margen 0.1`, `n 1600`.
- `src/stage7_bidirectional.py:47–89, 184, 224`.
- Los costos (0 / 1 / 4) y el detalle de las cuatro vacas (`contenido propio acepta; directorio → cow`) vienen de `results/experimento14/README.md`.

**Por qué:** hoy la metodología no lo menciona, aunque decide antes que la memoria (T7).

### 1i. ξ (líneas 164–182)

**Viejo:**
```latex
Los parámetros de la EAM se fijaron en:
$\iota = 0$, $\kappa = 0$, $\sigma = 0.1$, y tolerancia de reconocimiento
$\xi = 0$ para el dominio textual y $\xi = 2$ para el directorio visual.
Estos valores siguen el modelo W-EAM y su extensión hetero-asociativa, descritos en el
marco teórico.
La propia línea W-EAM ha mostrado que estos hiperparámetros admiten optimización
automática multi-objetivo \cite{lopez2025hyperopt}; aquí se fijan por barrido directo,
cuya justificación experimental se presenta en la Sección~\ref{sec:param-iota-kappa}
(barrido $\iota \times \kappa$) y en la Sección~\ref{sec:hemisferio-visual}
(barrido de $\xi$ visual).
En síntesis: $\iota > 0$ elimina conocimiento escaso pero válido antes de eliminar
relaciones espurias, $\kappa$ no cambió ningún resultado en el rango probado, y
$\xi = 2$ en el directorio visual amplía la cobertura sin costo en especificidad.
Debe declararse que el barrido de $\xi$ visual se midió sobre el enrutamiento del
conjunto de \emph{prueba}: $\xi = 2$ es, por tanto, un hiperparámetro seleccionado
sobre el mismo conjunto que después se reporta.
$\xi$ es un mecanismo nativo de la EHAM (tolerancia de funciones parciales), no un
umbral supervisado ad hoc --- la observación afecta al protocolo de selección, no a
la operación (Sección~\ref{sec:limitaciones}).
```

**Nuevo:**
```latex
Los parámetros de la EAM se fijaron en:
$\iota = 0$, $\kappa = 0$, $\sigma = 0.1$, y tolerancia de reconocimiento
$\xi = 0$ en los dos hemisferios, también en el directorio visual.
Estos valores siguen el modelo W-EAM y su extensión hetero-asociativa, descritos en el
marco teórico.
La propia línea W-EAM ha mostrado que estos hiperparámetros admiten optimización
automática multi-objetivo \cite{lopez2025hyperopt}; aquí se fijan por barrido directo,
cuya justificación experimental se presenta en la Sección~\ref{sec:param-iota-kappa}
(barrido $\iota \times \kappa$) y en la Sección~\ref{sec:hemisferio-visual}
($\xi$ visual).
En síntesis: $\iota > 0$ elimina conocimiento escaso pero válido antes de eliminar
relaciones espurias; $\kappa$ solo rechaza: en todo el rango en que actúa baja la
precisión y nunca la mejora; y $\xi > 0$ no se usa en el directorio visual porque,
con directorios perspectivales, la tolerancia de un agente dependería de lo que
presenciaron los demás.
Las cifras visuales de la Sección~\ref{sec:hemisferio-visual} se obtienen con $\xi = 0$.
```

**Fuente:**
- `src/stage7_bidirectional.py:41–46`: `XI_VISUAL = 0`, con el comentario sobre los directorios perspectivales; el cambio es de `a423950` (14 sep).
- `results/experimento10/README.md`, línea 9: «con xi=2 el ruteo del dominio propio *baja* al subir f».
- La redacción de κ viene de `revision_pesos_homo_principal_prosa.md` §1b.

**Por qué:** la tesis declara un hiperparámetro elegido sobre test que el sistema ya no usa. La salvedad de selección sobre test deja de aplicar al sistema actual.

---

## 2. Resultados (`05_resultados.tex`)

### 2a. Prioridad: «Línea base: una sola EHAM con las ocho clases» (líneas 390–419)

**Viejo:** la subsección completa, líneas 390–419, desde `\subsection{Línea base: una sola EHAM con las ocho clases}` hasta `Tablas completas en \texttt{results/experimento11/}.` Las frases que cambian de significado son:
- «Los especialistas reconstruidos son bit a bit los modelos oficiales.»
- «la EHAM única acierta la clase el 97.4\,\% … frente al 97.5\,\% del protocolo»
- «su respuesta cae a 26.7 … frente a 22.8 y 22.2, y la brecha crece con el contenido (2.0 con 100 registros por clase, 4.5 con 800)»
- «acierta la clase el 44\,\% y su patrón mezcla clases (73\,\% …)»
- «la EHAM única responde al 96\,\% … frente al 79\,\% del especialista, y responde con un dominio ajeno el 9\,\% frente al 1\,\% … (el especialista responde el 0, 5, 45 y 79\,\% … la EHAM única, el 5, 54, 81 y 96\,\%)»
- «Fuera de dominio … el protocolo acepta 4 y la EHAM única 3»
- «El protocolo queda 2.5 puntos por debajo del oráculo en todos los cortes»

**Nuevo:**
```latex
\subsection{Línea base: una sola EHAM con las ocho clases}

Para medir qué aporta la partición en especialistas, se construyó una
EHAM única (una memoria hetero-asociativa) con los mismos pares etiqueta--latente
que reciben los ocho especialistas (25\,600 con 200 imágenes por clase y 16
variantes) y se evaluó con las mismas operaciones
(\texttt{recognize\_gated}, \texttt{recall\_from\_left}), sin ruteo. Se
compararon tres brazos: la EHAM única, los especialistas con el agente
elegido por la verdad de terreno (oráculo, un techo) y el protocolo
transactivo completo, sobre las 171 consultas reservadas, diez semillas y
cortes de 25 a 200 imágenes por clase. En el corte de 200, cuatro de los
ocho especialistas reconstruidos son bit a bit los modelos oficiales; los
otros cuatro difieren porque el experimento recalcula los latentes en GPU,
y el redondeo puede mover un registro al nivel vecino.

Con 25 imágenes por clase la EHAM única acierta la clase algo más que el
protocolo (97.6\,\% frente a 96.9\,\%; juez: vecino real más cercano), con
intervalos de 95\,\% que casi se tocan ($[97.4, 97.8]$ y $[96.3, 97.6]$). Desde
50 el orden se invierte y los intervalos se separan: el protocolo queda entre
98.3 y 98.8\,\% y la EHAM única entre 96.9 y 97.6\,\%
(con 200, intervalos de 95\,\% $[97.9, 98.6]$ y $[96.7, 97.1]$); el oráculo
acierta el 100\,\%. La respuesta de la EHAM única queda más lejos de la
instancia real más cercana en los cuatro cortes (32.5, frente a 27.0 del
protocolo y 26.8 del oráculo, con 200), pero la brecha con el oráculo no
crece con el contenido: 4.6, 6.2, 6.1 y 5.7 con 25, 50, 100 y 200 imágenes
por clase. Cuando la primera pista reconocida es una etiqueta compartida
entre clases (\emph{fruit}, \emph{animal}, \emph{red}; el 3.5\,\% de las
respuestas), la EHAM única acierta la clase entre el 48 y el 52\,\% y su
patrón tiene soporte en una sola clase en el 74--77\,\% de las coordenadas;
el protocolo, entre el 79 y el 84\,\%, y el oráculo, el 100\,\%.

En imagen\,$\to$\,texto la EHAM única responde más y se equivoca más de
dominio. El especialista responde el 43.8, 75.0, 92.5 y 97.5\,\% de las
imágenes de prueba con 25, 50, 100 y 200 imágenes por clase, y la EHAM
única el 78.7, 95.0, 98.8 y 100\,\%; con 200, la EHAM única responde con un
dominio ajeno el 10.9\,\% de las imágenes, frente al 4.1\,\% del especialista
y el 3.0\,\% del protocolo. Fuera de dominio, sobre 40 consultas, la EHAM
única acepta más a medida que crece el contenido (2, 2, 5 y 8); el oráculo
acepta 2 en todos los cortes y el protocolo 4, que bajan a 2, como el
oráculo, con la doble compuerta de contenido (el agente destino debe
contener la pista). El precio del directorio, la distancia del protocolo al
oráculo en clase, es de 3.1 puntos con 25 imágenes por clase y de 1.2 a 1.7 desde
50. Tablas completas en \texttt{results/experimento11/}.
```

**Fuente:** `results/experimento11/README.md` y `resumen.json` (`0c70824`, una sola hetero, 16 variantes). La primera cifra de cada lista de `resumen.json` es la media; las otras dos, el intervalo.

| cifra | campo |
|---|---|
| 25 600 registros | encabezado del README («N = 200 (3200 registros por clase; monolítica 25600)») |
| 4/8 bit a bit | `control` en `resumen.json`: apple, cup, pear y tomato `true`; car, cow, dog y horse `false`. El README explica el redondeo en GPU. `experimento13/README.md` midió esa diferencia: 148 niveles de 409 600 (0.036 %). |
| clase 97.6 / 96.9 (N=25) | `texto["M|N=25"].nn_ok`, `texto["T-protocolo|N=25"].nn_ok` |
| 98.8 / 98.8 / 98.3 (N=50, 100, 200) | `T-protocolo|N=…`: 0.9875, 0.9875, 0.9828 |
| M 97.5 / 97.6 / 96.9 | `M|N=50`: 0.9750; `M|N=100`: 0.9758; `M|N=200`: 0.9692 |
| intervalos con N=200 | README: protocolo [97.9, 98.6], M [96.7, 97.1] |
| d_nn 32.5 / 27.0 / 26.8 | `d_nn_truth` con N=200: 32.53, 26.98, 26.78 |
| brecha 4.6 / 6.2 / 6.1 / 5.7 | M − oráculo en `d_nn_truth`: 4.642, 6.185, 6.059, 5.747 |
| pista compartida: 3.5 %, 48–52 %, 74–77 %, 79–84 % | `fraccion_pista_compartida` 0.0351; `nn_ok_pista_compartida` de M 48.3 / 47.8 / 52.2 / 51.1 y del protocolo 80.3 / 82.9 / 84.3 / 78.6; `compat_max_pista_compartida` de M 0.76 / 0.74 / 0.77 / 0.75 |
| imagen→texto | `imagen[…].responde`: oráculo 0.4375 / 0.75 / 0.925 / 0.975; M 0.7875 / 0.95 / 0.988 / 1.0. `otro_dominio` con N=200: M 10.9, oráculo 4.1, protocolo 3.0 |
| fuera de dominio | `ood` × 40: M 2 / 2 / 5 / 8; oráculo 2; protocolo 4. `ood_compuerta`: protocolo 2 |
| precio del directorio | oráculo − protocolo en `nn_ok`: 3.15 / 1.25 / 1.25 / 1.72 |

**Por qué:** cambia la conclusión. Con 16 variantes, la partición también clasifica mejor desde N=50, con intervalos separados. La brecha de fidelidad existe en todos los cortes, pero no crece. La memoria única acepta más fuera de dominio a medida que crece el contenido: P3 se ve, y antes no. «Bit a bit» pasa a 4/8.

**Nota sobre el encargo:** se pidió la brecha como 4.6 / 6.1 / **6.0** / 5.7. `resumen.json` da 6.051 en N=100, que redondea a 6.1. La auditoría (T2) tiene razón con 6.1. Solo restando los valores ya redondeados del README (29.49 − 23.44 = 6.05) cabe la duda.

### 2b. Desglose por dominio (líneas 78–84)

**Viejo:**
```latex
Con la lectura B1 en $N = 400$, la precisión madura por dominio fue:
\texttt{cup} y \texttt{tomato} 100\%, \texttt{car} 98\%, \texttt{cow} y \texttt{dog}
96\%, \texttt{apple} 88\%, \texttt{pear} 86\% y \texttt{horse} 82\%
(Figura~\ref{fig:dominio}).
Las clases de fruta comparten el léxico genérico (\textit{fruit}, \textit{red},
\textit{green}, \textit{round}, \textit{tree}), lo que explica que concentren los
errores residuales.
```

**Nuevo:**
```latex
Con la lectura B1 en $N = 400$, la precisión madura por dominio fue:
\texttt{cow}, \texttt{cup} y \texttt{tomato} 100\%, \texttt{car} 98\%, \texttt{dog}
93.9\%, \texttt{apple} 88.2\%, \texttt{horse} 88\% y \texttt{pear} 76\%
(Figura~\ref{fig:dominio}).
Las clases de fruta comparten el léxico genérico (\textit{fruit}, \textit{red},
\textit{green}, \textit{round}, \textit{tree}) y concentran 18 de los 28 errores
residuales, la mayoría \texttt{pear} $\to$ \texttt{apple} (9); el otro foco es
\texttt{horse} $\to$ \texttt{cow} (6).
```

**Fuente:** `results/ablation_mdir_bias/ablation_metrics.csv` (`d0df16c`), condición B1 con N=400 y 5 semillas idénticas.
- `mature_acc_*`: apple 0.8824, car 0.98, cow 1.0, cup 1.0, dog 0.9388, horse 0.88, pear 0.76, tomato 1.0.
- Matriz `cm_*` (fila = clase real):
  - apple 45 bien, 3 → pear, 3 → tomato;
  - pear 38 bien, 9 → apple, 3 → tomato;
  - horse 44 bien, 6 → cow;
  - dog 46 de 49;
  - car 49 de 50.
- Errores: 28 en total (400 × 0.07). Los de fruta son 6 + 12 + 0 = 18.

**Por qué:** pear pasa a ser la peor clase, y horse cae en un error que no es de fruta. El causal «lo que explica» se quita, porque la cuenta no lo demuestra.

### 2c. Pie de la Figura 2 (líneas 64–65): opcional

**Viejo:**
```latex
    B1 es la mejor lectura en todo el rango; la cruda (A) queda sistemáticamente por debajo.}
```

**Nuevo:**
```latex
    Entre las condiciones que solo cambian la lectura, B1 es la mejor en todo el rango;
    la cruda (A) queda sistemáticamente por debajo. D y G, que además balancean las
    consultas, superan a B1 en $N = 50$.}
```

**Fuente:** `ablation_metrics.csv`, `mature_accuracy` media por condición y N. Con N=50: B1 78.0, D 90.0, G 91.7. G supera a B1 en los cuatro N (93.5 contra 93.0 en N=400). La curva regenerada lo muestra.

### 2d. Error residual de la réplica (líneas 150–153)

**Viejo:**
```latex
La réplica con las 16 \texttt{TEST\_QUERIES} (2 por dominio) enruta correctamente las
ocho clases, con conteos $[12, 6, 6, 7, 5, 5, 4, 7]$; los errores residuales
corresponden a consultas de fruta con léxico compartido
(``sweet fruit from an orchard tree'' $\to$ \texttt{apple}).
```

**Nuevo:**
```latex
La réplica con las 16 \texttt{TEST\_QUERIES} (2 por dominio) enruta correctamente 15
de las 16, con al menos un acierto en cada clase y conteos $[12, 6, 6, 7, 5, 5, 4, 7]$;
el único error es una consulta de fruta con léxico compartido
(``a ripe green pear from the orchard'' $\to$ \texttt{apple}).
```

**Fuente:** `results/exp3_corrected_routing/report.md` (tabla de ganadores) y `summary.json` (`test_queries_counts`). La verdad de terreno está en `src/stage6_interaction.py:626–643`: «sweet fruit from an orchard tree» es de apple, así que es un acierto.

**Por qué:** el ejemplo citado era un acierto.

### 2e. ξ y «625 de 656» (líneas 321–333)

«625 de 656» no tiene fuente actual. Viene de `f77c6e0` (13 jul), con el llenado de 4 variantes y los directorios idénticos.

**Viejo:**
```latex
\paragraph{Justificación de $\xi = 2$.}
El barrido $\xi \in \{0, \ldots, 3\}$ mostró que $\xi = 2$ es el punto dulce de
cobertura, con saturación en $\xi = 3$ y especificidad intacta en todo el rango
(0 falsos sobre sondas sintéticas fuera de dominio).
El análisis del residual es informativo: 625 de las 656 imágenes de test tienen
\emph{cero} coordenadas sin soporte marginal, de modo que el rechazo restante no viene
de huecos por coordenada (que $\xi$ tolera) sino del \emph{containment conjunto}: la
proyección AND no encuentra celdas que sobrevivan a las 64 coordenadas simultáneamente.
Por eso $\xi$ satura, y la palanca para ese residual es densificar el llenado, no
aumentar la tolerancia. El experimento 13 lo midió y esta versión lo adopta: con 16
variantes por imagen en el contenido y por percepción en el directorio, el ruteo de
test sube del 73.6\,\% al 96.2\,\% y la evocación del 85.3 al 97.4\,\%, con dos falsos
de 656 (Sección~\ref{sec:limitaciones}).
```

**Nuevo:**
```latex
\paragraph{Por qué $\xi = 0$.}
Con directorios perspectivales la tolerancia no es del módulo: los huecos que
$\xi$ admite se definen sobre el soporte de todos los agentes del directorio, y con
$\xi = 2$ el ruteo del dominio propio baja a medida que el agente presencia más
dominios ajenos (experimento 10). El sistema usa $\xi = 0$, y la palanca para la
cobertura fue densificar el llenado, no tolerar huecos. El experimento 13 lo midió y
esta versión lo adopta: con 16 variantes por imagen en el contenido y por percepción
en el directorio, el ruteo de test sube del 73.6\,\% al 96.2\,\% y la evocación del
85.3 al 97.4\,\%, con dos falsos de 656 (Sección~\ref{sec:limitaciones}).
```

**Fuente:**
- `src/stage7_bidirectional.py:41–46`.
- `results/experimento10/README.md`, líneas 9 y 74.
- Las cifras 73.6 → 96.2, 85.3 → 97.4 y los 2 falsos no cambian; son las del texto actual, aprobadas en `revision_v16_prosa.md` (`c0a0d61`).

**Por qué:** el párrafo justificaba un valor que el sistema no usa y se apoyaba en un análisis sin archivo.

### 2f. Fuga con entradas degeneradas (líneas 349–356)

**Viejo:**
```latex
La tercera sonda sintética, un lienzo de color sólido uniforme, \emph{sí} obtiene
soporte y se acepta: es la excepción honesta del panel. El experimento 14 localizó la
causa: no es el fondo liso (los sólidos negro, blanco, de colores y del color de fondo
de ETH-80 se rechazan) sino que el encoder colapsa toda entrada sin estructura, el gris
medio, un objeto desenfocado o sin contraste, en un mismo latente cerca del origen, y
ese punto cae dentro de la envolvente por coordenada de \texttt{horse}, a tres veces la
distancia intraclase de cualquier instancia registrada.
Esta fuga con entradas degeneradas se retoma en la Sección~\ref{sec:limitaciones}.
```

**Nuevo:**
```latex
La tercera sonda sintética, un lienzo gris uniforme, \emph{sí} obtiene soporte del
contenido: es la excepción honesta del panel. El experimento 14 localizó la causa: el
encoder lleva las entradas sin estructura (gris uniforme, un objeto desenfocado o sin
contraste) a latentes de norma baja que caen dentro de la envolvente por coordenada de
los animales. Los grises de nivel 120 a 160 (el del panel, 127, cae en ese tramo) los
aceptan a la vez \texttt{cow}, \texttt{dog} y \texttt{horse}, aunque la instancia real más cercana
está a entre 2.4 y 4.4 veces la mediana de la distancia intraclase.
No es cualquier fondo liso: de 12 sólidos de color se aceptan 2.
Esos grises tienen norma de 10.7 a 13.0, por debajo de $\tau = 16.61$, y el umbral de
energía los rechaza antes de la memoria (Sección~\ref{sec:percepcion}).
Esta fuga con entradas degeneradas se retoma en la Sección~\ref{sec:limitaciones}.
```

**Fuente:** `results/experimento14/README.md` (`224f7cd`).
- Tabla «Entradas degeneradas aceptadas»: grises 120–160 → `cow,dog,horse`, con normas 11.21, 10.69, 10.73, 11.23, 11.95 y 13.04.
- La razón de distancias va del gris 120 (13.9 / 5.7 = 2.4) a los grises 104 y 112 (29.5 y 29.6 / 6.7 = 4.4).
- «Por familia»: color, 2 aceptados de 12 (magenta → apple y (63, 77, 150) → dog).
- El gris del panel es el nivel 127: `generate_paper_figures.py:1141`.

**Por qué:** la fuga no es solo de horse, y el panel ya no es el sistema completo, porque τ la cierra. El gris 176 (norma 17.34, aceptado por cow) sí pasa τ. Por eso el texto habla del tramo 120–160, que es el del panel, y no de todos los grises.

### 2g. Pie de la Figura 15 (líneas 367–373)

**Viejo:**
```latex
    Arriba: imágenes reales aceptadas y enrutadas. En medio: imágenes reales no
    contenidas, rechazadas ($\xi = 0$). Abajo: sondas sintéticas fuera de dominio:
    el ruido y los píxeles barajados se rechazan; el color sólido uniforme se acepta,
    una fuga con entradas degeneradas que se discute en la
    Sección~\ref{sec:limitaciones}. El rechazo emerge de la ausencia de soporte, y la
    figura muestra también su excepción.}
```

**Nuevo:**
```latex
    Arriba: imágenes reales aceptadas por el contenido. En medio: imágenes reales no
    contenidas, rechazadas ($\xi = 0$). Abajo: sondas sintéticas fuera de dominio:
    el ruido y los píxeles barajados se rechazan; el gris uniforme obtiene soporte,
    una fuga con entradas degeneradas que en el sistema completo cierra el umbral de
    energía (la figura no lo aplica) y que se discute en la
    Sección~\ref{sec:limitaciones}. El rechazo emerge de la ausencia de soporte, y la
    figura muestra también su excepción.}
```

**Fuente:** `generate_paper_figures.py:1151–1185`: la figura decide con `recognize_gated_right` de los ocho especialistas, sin directorio y sin `latent_has_energy`. La imagen regenerada (`papers_images/es/fig15_image_rejection.png`, `c0a0d61`) rotula la sonda «solid: aceptada» y es un gris uniforme.

**Por qué:** «enrutadas» no es lo que hace la figura, porque elige por contenido. Con τ, la sonda gris ya no se acepta.

### 2h. Pie de la Figura 16 (líneas 380–385)

**Viejo:**
```latex
    \caption{Salida semántica imagen $\to$ etiquetas (dos ejemplos por clase). Por cada
    imagen aceptada: entrada (pista), reconstrucción evocada por la memoria (no la
    entrada) y las etiquetas recuperadas, con marca de coincidencia con el vocabulario
    de la clase real.
    Se muestran tanto aciertos como fallos de evocación, coherentes con el 97.4\%
    agregado.}
```

**Nuevo:**
```latex
    \caption{Salida semántica imagen $\to$ etiquetas (dos ejemplos por clase). Por cada
    imagen aceptada por el contenido (el agente es el de mayor soporte, sin pasar por el
    directorio): entrada (pista), reconstrucción evocada por la memoria (no la entrada)
    y las etiquetas recuperadas, con marca de coincidencia con el vocabulario de la
    clase real. En 15 de los 16 ejemplos alguna etiqueta es del dominio; en el restante
    (\texttt{dog}) la recuperación no devuelve etiquetas. Sobre el test completo, con el
    directorio, la evocación acierta el 97.4\%.}
```

**Fuente:**
- La imagen regenerada `papers_images/es/fig16_image_to_labels.png` (`d0df16c`): 15 marcas ✓; la primera fila de dog muestra «→ dog» sin etiquetas y ✗.
- Selección por contenido: `generate_paper_figures.py:1233–1237`.
- 97.4 %: líneas 335–339 del texto, sin cambios según `revision_pesos_homo_principal_prosa.md`.

**Por qué:** la imagen de la tesis es la del 13 de julio. El pie decía «aciertos como fallos» sin decir cuántos.

### 2i. Costo computacional (tabla, líneas 432–447)

**Viejo (pie, 432–434):**
```latex
    \caption{Costo computacional de la reproducción completa a ocho clases (CPU, sin
    GPU). El entrenamiento del encoder concentra el costo; las decisiones del sistema de
    memorias son operaciones matriciales sobre vectores cuantizados.}
```

**Nuevo:**
```latex
    \caption{Costo computacional de la reproducción completa a ocho clases (CPU, sin
    GPU), medido en julio de 2026 con el llenado de 4 variantes por imagen, antes de
    adoptar las 16 variantes; no se volvió a medir. El entrenamiento del encoder
    concentra el costo; las decisiones del sistema de memorias son operaciones
    matriciales sobre vectores cuantizados. La ablación de la batería terminó con error,
    así que su tiempo es el de una corrida incompleta.}
```

**Viejo (filas, 446–447):**
```latex
        Pipeline completo (etapas 1--8) & \textbf{133.5 min} \\
        Batería de análisis completa (calibración, barridos, figuras) & 293.4 min \\
```

**Nuevo:**
```latex
        Pipeline completo (etapas 1--8) & \textbf{133.5 min} \\
        Batería de análisis (calibración, barridos, figuras) & 159.9 min \\
        Total (pipeline + batería) & 293.4 min \\
```

**Fuente:** `results/computational_cost/comparacion_laptops.md`:
- encabezado «laptop 1 (julio de 2026)»;
- tabla «Batería»: batería 159.9; total (pipeline CPU + batería) 293.4;
- salvedad (1): «La ablación falló en la laptop 1 (rc=1 a los 39 min)»;
- `report.md`: `ablation … ✗`.

Las 16 variantes son de `66a6225` (23 sep).

**Por qué:** 293.4 estaba rotulado como la batería sola.

### 2j. Segunda laptop (líneas 461 y 468–470)

**Viejo (461):** `La misma medición, repetida en una segunda laptop (Intel Core Ultra 7 265HX, 20 hilos,`

**Nuevo:** `La misma medición, repetida el 22 de septiembre de 2026 (también con 4 variantes) en una segunda laptop (Intel Core Ultra 7 265HX, 20 hilos,`

**Viejo (468–470):**
```latex
hemisferio visual no la usan. En esa máquina la parte cara del sistema deja de ser el
entrenamiento y pasa a ser la memoria: llenado y hemisferio visual suman 25 de los
32~min. Tabla completa en \texttt{results/computational\_cost/comparacion\_laptops.md}.
```

**Nuevo:**
```latex
hemisferio visual no la usan. En esa máquina la parte cara del sistema deja de ser el
entrenamiento y pasa a ser la memoria: llenado y hemisferio visual suman 25 de los
32~min. Con 16 variantes el llenado registra cuatro veces más patrones y la fase A
dieciséis veces más, y esos tiempos no se volvieron a medir.
Tabla completa en \texttt{results/computational\_cost/comparacion\_laptops.md}.
```

**Fuente:**
- `comparacion_laptops.md`: título «laptop 2 (22 de septiembre de 2026)»; llenado 10.1 + hemisferio visual 14.6 = 24.7 de 31.9 min con GPU.
- Llenado: 4 → 16 variantes (`src/stage5_fill.py:46–49`).
- Fase A: 1 → 16 registros por percepción. `results/experimento13/README.md`, «A0: oficial (Vc=4, Vd=1)», y `66a6225`.

No doy tiempos nuevos.

---

## 3. Figuras

La tesis toma las figuras de `.tex8/figuras/` (`main.tex:17`, `\graphicspath{{figuras/}}`). Todas son del 13 de julio (`f77c6e0`). Las regeneradas están en `papers_images/es/`. Las verifiqué con `cmp` y `git log`:

| archivo | dónde se usa | `.tex8/figuras/` | `papers_images/es/` | ¿copiar? |
|---|---|---|---|---|
| `fig02_mature_accuracy_vs_N.png` | 05:63 | f77c6e0, 13 jul | d0df16c, 28 oct | sí |
| `fig03_heatmap_condition_N.png` | 05:71 | f77c6e0 | d0df16c | sí |
| `fig04_domain_accuracy_N80.png` | 05:88 | f77c6e0 | d0df16c | sí |
| `fig09_winner_distribution_N80.png` | 05:108 | f77c6e0 | d0df16c | sí |
| `fig15_image_rejection.png` | 05:366 | f77c6e0 | c0a0d61, 23 sep (16 variantes; no cambió con los pesos homo) | sí |
| `fig16_image_to_labels.png` | 05:379 | f77c6e0 | d0df16c | sí |
| `fig11_semantic_space.png` | 06:30 | f77c6e0 | 0b46b53, 11 jul | no: byte a byte igual |

Las seis existen. Las de la ablación salen del caché `papers_images/ablation_rows.csv` (`d0df16c`), y sus medias por condición y N coinciden con `results/ablation_mdir_bias/ablation_metrics.csv`.

```powershell
foreach ($f in 'fig02_mature_accuracy_vs_N','fig03_heatmap_condition_N','fig04_domain_accuracy_N80','fig09_winner_distribution_N80','fig15_image_rejection','fig16_image_to_labels') {
  Copy-Item "papers_images\es\$f.png" ".tex8\figuras\$f.png"
}
```

En `fig16` el título de la figura se monta sobre los rótulos de la primera fila. Es cosmético y está en la imagen, no en el pie.

---

## 4. Dudas para el autor

1. **Rescate léxico (1f).** Propongo fecharlo. La otra opción es volver a medirlo con las memorias actuales: una pasada de la fase temprana sobre el banco de 411, con y sin la regla. No estimé cuánto tarda, y es una corrida, así que la decides tú.
2. **Recorte del min–max (1g).** La cifra «6 de 1 638 400» la calculé yo sobre los archivos de `models/`, pero no está en `results/`. ¿La dejas en el texto con el comando como fuente, o dices solo «se recorta» sin dar cifra?
3. **Candidatos (1d).** El commit `2c584fd` dice 70 y 93; el caché de ese mismo commit da 68 y 86. Tomé el caché. ¿Hubo un conteo previo a algún filtro, como ASCII o `DerivedFrom`?
4. **Figura 15.** No aplica τ, así que muestra una fuga que el sistema completo cierra. Puedes dejar el pie como propongo o regenerarla aplicando `latent_has_energy` (unos minutos con `generate_paper_figures.py`, pero es una corrida).
5. **Costo (2i–2j).** Los tiempos son de 4 variantes. Volver a medir el pipeline completo tarda unos 32 min en la laptop 2 con GPU, más lo que agreguen las 16 variantes. ¿Se queda declarado así?
6. **Fuera de mi parte, pero lo encontré:**
   - `05:317–318` dice «75.0 % con ξ = 2». Debe de ser de los directorios idénticos; si se mantiene, convendría decirlo.
   - Las limitaciones (b) y (f) de `06` (líneas 177–180 y 258–260) y `03:313, 360, 441–452` siguen con ξ = 2 (T5).
   - `06:268` repite el rescate léxico.
7. **README de exp11.** Dice que el juez usa «las 6400 instancias reales», pero `Judge` carga todo `instance_latents_*.json`: 25 600 con 16 variantes (`run_experiment9_member_loss.py:229–232`). Es texto fijo en `run_experiment11_monolithic.py:825`. La tesis no lo cita, pero el README está mal.
8. **Auditoría.** Todo lo que verifiqué de ella se sostiene: T2, T5, T6, T7, la sección 2 y T10. El único desacuerdo es con el encargo: la brecha de exp11 en N=100 es 6.1, no 6.0.

---

# Propuesta viejo/nuevo, parte 3: discusión y conclusiones (`.tex8`)

**Estado:** pendiente de aprobación. Nada aplicado.

**Alcance:** `06_discusion.tex` y `07_conclusiones.tex`, con los hallazgos de `auditoria_redaccion_29oct.md`. Lo que ya cubre `revision_pesos_homo_principal_prosa.md` no se repite: líneas 50, 56, 72 y 109 de discusión, y 14–16 y 36 de conclusiones.

**Fuentes:** todas son de la corrida con 16 variantes y pesos homo (d0df16c). Las cifras de exp11 son medias de 10 semillas con bootstrap del 95 %.

---

## A. Discusión (`06_discusion.tex`)

### A1. Temprana con la cuantización (línea 22)

**Viejo** (21–23): «La cuantización por magnitud sobre una escala global (Sección~\ref{sec:pipeline-semantico}) recuperó el rango de 85--88\% de precisión temprana \emph{sin tocar una línea de la maquinaria asociativa}.»

**Nuevo:**
> Con la cuantización por magnitud sobre una escala global (Sección~\ref{sec:pipeline-semantico}), la precisión temprana es del 90.0\% \emph{sin tocar una línea de la maquinaria asociativa}.

**Fuente:**
- 88.0: `git show 57e61f3~1:results/ablation_mdir_bias/ablation_metrics.csv` (B1, N=400, 5 semillas). También `CONTEXTO_SEP2026.md:139`, «88.0 → 90.0».
- 90.0: `results/ablation_mdir_bias/ablation_metrics.csv` (B1, N=400).

**Por qué:** el 90 no lo da la cuantización sola; una parte viene de las 16 variantes. El 85 no tiene archivo.

### A2. pear con 16 variantes (líneas 73–74)

**Viejo:** «…\emph{sin cambiar el vocabulario} (78\% con el llenado de 16 variantes).»

**Nuevo:** «…\emph{sin cambiar el vocabulario} (76\% con el llenado de 16 variantes).»

**Fuente:** `results/ablation_mdir_bias/ablation_metrics.csv`: B1, N=400, `mature_acc_pear` = 76.0 (media de 5 semillas).

### A3. Desglose por clase (líneas 120–122)

**Viejo:** «Las clases cuyas consultas usan léxico exclusivo (\texttt{cup}, \texttt{tomato}, \texttt{car}) alcanzan 98--100\%; las que preguntan con léxico compartido (\texttt{pear}, \texttt{horse}) quedan en 82--86\%.»

**Nuevo:**
> Las clases cuyas consultas usan léxico exclusivo (\texttt{cup}, \texttt{tomato}, \texttt{car}) alcanzan 98--100\%; las que preguntan con léxico compartido (\texttt{pear}, \texttt{horse}) quedan en 76 y 88\%.

**Fuente:** `results/ablation_mdir_bias/ablation_metrics.csv`, B1, N=400, `mature_acc_*` (media de 5 semillas):

| clase | % |
|---|---|
| cup | 100 |
| tomato | 100 |
| cow | 100 |
| car | 98.0 |
| dog | 93.9 |
| apple | 88.2 |
| horse | 88.0 |
| pear | 76.0 |

(Duda 6: apple.)

### A4. Especificidad «exacta» (líneas 129–133)

**Viejo:**
> \item \textbf{El rechazo colectivo escala.} Con ocho especialistas y siete clases contrarias por agente, la especificidad se mantiene exacta: 0\% de falsos aceptados en contenido en todo el rango de $N$, y dos falsos enrutamientos visuales de 656, del mismo objeto hacia la clase vecina. El grupo sigue sin inventar referentes.

**Nuevo:**
> \item \textbf{El rechazo colectivo escala.} Con ocho especialistas y siete clases contrarias por agente, la especificidad del contenido es casi exacta: con el llenado de un latente por imagen no acepta ningún falso en todo el rango de $N$, y con 16 variantes acepta 5 de 656 imágenes de test, todas entre animales (vacas y caballos aceptados por \texttt{dog}, un caballo por \texttt{cow}). El directorio visual comete dos falsos enrutamientos de 656, del mismo objeto hacia la clase vecina. Los errores que quedan son entre clases vecinas; el grupo sigue sin inventar referentes.

**Fuente:**
- El 0 %: `results/exp6_capacity/report.md`, columna «falsos». exp6 llena con un latente por imagen (`run_experiment6.py:100–108`).
- Los 5 de 656: `results/experimento13/README.md`, A3, V=16, «falso contenido» = 0.8 %.
- Los pares: `results/experimento13/raw/Vc16_N200_Vd16_s4*.json`. Son los mismos en las 5 semillas:
  - cow3-066-117 → dog;
  - cow6-035-045 → dog;
  - horse7-000-000 → dog;
  - horse7-035-135 → dog;
  - horse8-022-090 → cow.

**Por qué:** el 0 % solo vale para el llenado sin variantes. El sistema actual acepta 5 falsos en contenido.

### A5. Partición frente a EHAM única (líneas 139–151) — prioridad

**Viejo:**
> La comparación con la EHAM única acota lo que la maquinaria transactiva aporta. No es exactitud: sobre el banco completo ambas clasifican igual. Es fidelidad, coherencia y precisión: la relación de una EHAM acumula por coordenada y valor, y dos conceptos distintos comparten valores cuantizados en muchas coordenadas, así que una memoria con varios dominios mezcla al recordar aunque las palabras difieran. Partir el contenido evita la mezcla porque la decisión de dominio ocurre antes del recall, en el directorio, y no dentro del sorteo. El precio es cobertura: el containment de un especialista es estricto en las 64 coordenadas del latente y deja fuera al 21\,\% de las imágenes de prueba, que la unión de soportes contiene; es el rechazo residual del hemisferio visual (limitación (b)), ahora identificado como costo de la partición. A eso se suman 2.5 puntos del directorio y ocho veces las celdas.

**Nuevo:**
> La comparación con la EHAM única acota lo que la maquinaria transactiva aporta. Ante todo es fidelidad, coherencia y precisión: la relación de una EHAM acumula por coordenada y valor, y dos conceptos distintos comparten valores cuantizados en muchas coordenadas, así que una memoria con varios dominios mezcla al recordar aunque las palabras difieran. Partir el contenido evita la mezcla porque la decisión de dominio ocurre antes del recall, en el directorio, y no dentro del sorteo. La respuesta de la EHAM única queda más lejos de la instancia real más cercana en todos los cortes (de 4.6 a 6.2 más que el oráculo), sin tendencia con el contenido. Fuera de dominio, la EHAM única acepta más cuanto más contiene (de 2 a 8 de 40 consultas); el protocolo con doble compuerta acepta 2 en todos los cortes. La exactitud de clase también mejora, pero poco: desde 50 imágenes por clase el protocolo acierta entre 98.3 y 98.8\,\% frente a 96.9--97.6\,\% de la EHAM única, con intervalos separados; con 25 la EHAM única queda arriba (97.6 frente a 96.9\,\%, con intervalos que casi se tocan), porque el directorio todavía rutea peor (95.3\,\% de ruteo correcto). El precio es cobertura: el containment de un especialista es estricto en las 64 coordenadas del latente y deja sin respuesta al 2.5\,\% de las imágenes de prueba con 200 por clase, que la EHAM única responde; es parte del rechazo residual del hemisferio visual (limitación (b)). A eso se suman de 1.2 a 1.7 puntos del directorio desde 50 imágenes por clase (3.1 con 25) y ocho veces las celdas.

**Fuente:** `results/experimento11/README.md` y `resumen.json`. Columnas de texto: clase 1-NN, `d_nn`, ruteo ok. Imagen→texto: responde. Fuera de dominio: aceptación sobre 40 consultas.

| N | clase 1-NN: M / oráculo / protocolo | `d_nn`: M − oráculo | precio del directorio (oráculo − protocolo) | ruteo ok del protocolo | fuera de dominio: M / protocolo con compuerta (de 40) |
|---|---|---|---|---|---|
| 25 | 97.6 [97.4, 97.8] / 100 / 96.9 [96.3, 97.6] | 4.6 | 3.1 | 95.3 | 2 / 2 |
| 50 | 97.5 [97.3, 97.7] / 100 / 98.8 [98.6, 98.9] | 6.2 | 1.2 | 97.4 | 2 / 2 |
| 100 | 97.6 [97.4, 97.8] / 100 / 98.8 [98.4, 99.1] | 6.1 | 1.2 | 97.4 | 5 / 2 |
| 200 | 96.9 [96.7, 97.1] / 100 / 98.3 [97.9, 98.6] | 5.7 | 1.7 | 97.0 | 8 / 2 |

- Cobertura del especialista en imagen→texto con N=200: el oráculo responde 97.5 %; la EHAM única, 100 %.
- «Parte del rechazo residual»:
  - el contenido propio rechaza el 1.4 % de las 656 de test (`results/experimento13/README.md`, A3, V=16, contenido acepta 98.6);
  - el rechazo total de la etapa 7 es 3.5 % (`CONTEXTO_SEP2026.md:138`).

**Por qué:**
- La partición ya no compra solo fidelidad. Compra fidelidad, también exactitud de clase salvo con poco contenido, y especificidad fuera de dominio.
- La ventaja de clase es chica: 1.3 puntos con N=50, 1.2 con N=100 y 1.4 con N=200.
- Con N=25 pierde por el directorio, no por la partición: el oráculo sigue en 100.
- La brecha de fidelidad no crece con el contenido: se mantiene entre 4.6 y 6.2.
- El costo de cobertura del especialista baja de 21 % a 2.5 %.

### A6. Doble compuerta sobre las reservadas (líneas 167–169)

**Viejo:** «…las filas que rechaza (1.4\,\% con 200 imágenes por clase, 21\,\% con 25) ya no producían recall en el destino, y en los cortes grandes son todas ruteos equivocados.»

**Nuevo:** «…las filas que rechaza (1.5\,\% con 200 imágenes por clase, 2.1\,\% con 25) ya no producían recall en el destino, y en todos los cortes son ruteos equivocados.»

**Fuente:** `results/experimento11/compuerta_reservadas.md`:
- N=25: 35 de 1710 (2.05 %).
- N=200: 26 de 1710 (1.52 %).
- «pierde respuesta» vale 0 en los cuatro cortes.
- Las 15 combinaciones consulta-destino listadas tienen «ruteo ok = False».

**Por qué:** ahora son ruteos equivocados también en N=25.

### A7. Árbitro y margen (líneas 170–173)

**Viejo:** «…empeora el ruteo de texto (96.1 $\to$ 90.6\,\% de acierto, experimento 15): el índice calibrado compara mejor que la activación del contenido, y la abstención por margen de score quita un acierto por cada error a cualquier umbral.»

**Nuevo:** «…empeora el ruteo de texto (96.8 $\to$ 93.6\,\% de acierto, experimento 15): el índice calibrado compara mejor que la activación del contenido, y la abstención por margen de score quita más de un acierto por cada error que evita, a cualquier umbral (1.2 con $\delta = 0.05$, 8 con $\delta = 0.5$).»

**Fuente:** `results/experimento15/README.md`:
- Tabla «Texto»: argmax 96.8, árbitro 93.6.
- «Curva de δ»: aciertos perdidos por cada error que se evita.
  - δ = 0.05: (96.8 − 95.6) / (3.2 − 2.2) = 1.2.
  - δ = 0.50: (96.8 − 75.9) / (3.2 − 0.6) = 8.0.

**Por qué:** antes era un acierto por error. Ahora el margen cuesta más que eso a cualquier umbral.

### A8. Limitación (b): punto de partida (líneas 176–180)

**Viejo:**
> El 25\% de rechazo del enrutamiento visual de test no proviene de huecos por coordenada (625 de 656 imágenes tienen soporte marginal completo) sino de la conjunción AND sobre las 64 coordenadas simultáneas, por lo que aumentar $\xi$ no lo reduce ($\xi$ satura en 2--3).

**Nuevo:**
> La lectura del directorio visual es estricta ($\xi = 0$): con directorios perspectivales, los huecos tolerados dependerían de lo que presenció cada módulo.

El resto del párrafo («La palanca es densificar…» hasta «…el rechazo en 3.5\,\%») queda igual. Ese resto ya da el estado actual.

**Fuente:**
- 26.4: `results/experimento13/README.md`, A0, directorio acepta 73.6 con ξ = 0. También `results/experimento15/README.md`, «Imagen (Vc = 4, Vd = 1)», rechazo 26.4.
- ξ = 0: `src/stage7_bidirectional.py:46` (`XI_VISUAL = 0`); el porqué está en el comentario de las líneas 41–45.
- 3.5 %: `CONTEXTO_SEP2026.md:138`.
- 625 de 656: solo tiene fuente en la tesis (`05_resultados.tex:325`, primera versión de ocho agentes). Ver duda 7.

**Por qué:** el párrafo viejo describía como actual un rechazo del 25 % con ξ = 2. Hoy el rechazo es 3.5 % y ξ = 0.

### A9. Umbral de energía τ (líneas 200–213)

**Viejo** (200–205): «El experimento 14 midió la mitigación: un umbral sobre la norma del latente continuo, fijado con el mínimo de las imágenes de llenado y un margen del 10\,\% ($\tau = 16.6$), cierra el 94\,\% de esa fuga (79 de las 83 entradas degeneradas aceptadas por una clase ajena caen bajo $\tau$: grises medios, desenfoques de radio $\geq 8$, contrastes $\leq 0.2$) y el 88\,\% con el llenado de 16 variantes, a costa de cinco imágenes reales de 3280, todas vistas oscuras de \texttt{cow} que el directorio ya rechazaba.»

**Nuevo:**
> El experimento 14 midió la mitigación: un umbral sobre la norma del latente continuo, fijado con el mínimo de las imágenes de llenado y un margen del 10\,\% ($\tau = 16.6$), cierra el 90\,\% de esa fuga (137 de las 152 entradas degeneradas aceptadas por una clase ajena caen bajo $\tau$: grises de 104 a 168, desenfoques de radio $\geq 12$, contrastes $\leq 0.2$), a costa de cinco imágenes reales de 3280, todas vistas oscuras de \texttt{cow}. No es gratis: las cuatro de test las ruteaba bien el directorio y su contenido las aceptaba.

**Viejo** (207–209): «Lo que sobrevive al umbral son confusiones de contenido entre clases (un \texttt{dog} desenfocado aceptado por \texttt{cow}), no entradas degeneradas.»

**Nuevo:**
> Lo que sobrevive al umbral son sobre todo confusiones de contenido entre clases (11 de 15 son objetos desenfocados o de bajo contraste, como un \texttt{dog} desenfocado aceptado por \texttt{cow}); las otras cuatro son superficies casi uniformes de norma alta (un gris claro, dos colores sólidos y un gris con ruido).

**Viejo** (210–213): «El umbral está instalado en la codificación de la percepción; en la etapa 7 rechaza una percepción de 1024 en la fase A y cuatro imágenes de 656 en test, sin cambiar el ruteo (medido con el llenado de 4 variantes; con el de 16 rechaza las mismas cuatro).»

**Nuevo:**
> El umbral está instalado en la codificación de la percepción; rechaza una percepción de 1024 en la fase A y cuatro imágenes de 656 en test, las cuatro vacas que el directorio ruteaba a \texttt{cow}: cuesta cuatro aciertos de test.

**Fuente:**
- τ = 16.607 y el costo: `results/experimento14/resumen.json` (`tau.norma`; `reales.norma`: llenado 0, fase A 1, test 4).
- Las cuatro de test: `reales.norma.test_detalle`. Son cow3-035-135, cow3-068-090, cow3-066-117 y cow6-035-045, todas con `contenido_propio: true` y `destino: cow`.
- La de fase A: `results/experimento14/reales.json` (cow4-066-027, norma 15.23).
- 137 de 152: `results/experimento14/banco_degenerado.json`. Se cuentan las entradas cuyo `contenido` incluye una clase distinta de la de origen (en grises y colores, cualquier clase) y que no pasan la norma.
  - Si se cuentan solo las entradas que la clase propia no acepta, son 88 de 100: 88 %.
  - Con el banco del 23 de septiembre (629b277, 4 variantes), las dos definiciones daban 79 de 83.
  - El 88 % viejo «con 16 variantes» usaba la segunda definición.
- Grises, radios y contrastes: mismo archivo.
  - Grises: caen 104–168; pasan gris 176 y gris 127 + ruido σ = 8.
  - Desenfoques: todos los de radio ≥ 12 caen; con r = 8 caen 4 de 7.
  - Contrastes: todos los ≤ 0.2 caen.
- Los 15 que sobreviven: mismo archivo.
  - Cuatro casi uniformes: gris 176, color (255, 0, 255), color (63, 77, 150) y gris 127 + ruido σ = 8.
  - Once objetos desenfocados o de bajo contraste.
- «Cuesta cuatro aciertos»: también `auditoria_redaccion_29oct.md` T7 y §5.3.

**Por qué:**
- τ ya no es «sin cambiar el ruteo»: las cuatro vacas de test eran aciertos.
- Lo que sobrevive al umbral ya no son solo confusiones de contenido.
- Con el llenado oficial de 16 variantes desaparece la distinción entre 4 y 16 variantes.

### A10. Objetos nuevos (líneas 248–250)

**Viejo:** «La brecha no vive en clases sino en objetos concretos: 74 de los 80 objetos reservados superan el 70\,\% y seis (dos manzanas, dos peras, un perro, una taza) concentran el resto.»

**Nuevo:**
> La brecha no vive en clases sino en objetos concretos: 71 de los 80 objetos reservados superan el 70\,\%, y nueve (dos manzanas, dos peras, dos perros, una taza, un coche y una vaca) concentran el 57\,\% de los fallos.

**Fuente:** `results/experimento16/raw/pliegue_*.json`, banco «nuevo», `e2e` por (clase, objeto), 41 vistas cada uno.
- 71 objetos superan el 70 %.
- Los 9 de abajo:
  - apple 3: 0 %;
  - pear 9: 9.8 %;
  - apple 10: 31.7 %;
  - dog 10: 48.8 %;
  - pear 6: 58.5 %;
  - cup 10: 61.0 %;
  - car 6: 63.4 %;
  - dog 3: 65.9 %;
  - cow 2: 68.3 %.
- Juntos suman 202 de los 355 fallos (57 %).

**Por qué:** antes eran seis objetos y «el resto» de los fallos. Ahora son nueve y concentran poco más de la mitad.

### A11. Limitación (f): ξ elegido sobre test (líneas 255–263)

**Viejo:**
> Dos elementos del protocolo se eligieron mirando el conjunto de prueba, por ausencia de una partición de validación separada: el punto de control del encoder (RMSE mínimo sobre test entre $\approx$5 candidatos, Sección~\ref{sec:percepcion}) y la tolerancia $\xi = 2$ del directorio visual (barrido medido sobre el enrutamiento de test, Sección~\ref{sec:parametros}). Ambas selecciones son de alcance acotado y ninguna introduce un mecanismo ajeno a las memorias, pero inflan potencialmente las cifras visuales reportadas; la corrección de protocolo (partición train/val/test) es directa y queda pendiente.

**Nuevo:**
> El punto de control del encoder se eligió mirando el conjunto de prueba, por ausencia de una partición de validación separada (RMSE mínimo sobre test entre $\approx$5 candidatos, Sección~\ref{sec:percepcion}). La tolerancia del directorio visual también se había fijado así ($\xi = 2$), pero la versión actual lee estricto ($\xi = 0$) y no depende de ese barrido. La selección es de alcance acotado y no introduce un mecanismo ajeno a las memorias, pero infla potencialmente las cifras visuales reportadas; la corrección de protocolo (partición train/val/test) es directa y queda pendiente.

**Fuente:** `src/stage7_bidirectional.py:46` (`XI_VISUAL = 0`).

**Por qué:** ξ = 2 ya no se usa. Ver duda 4: el número de variantes también se fijó mirando test.

### A12. Limitación (g): rescate léxico (líneas 266–268)

**Viejo:** «…su efecto medido es de +23.8 puntos sobre las 42 consultas afectadas del banco.»

**Nuevo:** «…su efecto medido es de +21.7 puntos sobre las 46 consultas afectadas del banco (43 de 46 correctas con rescate, 33 sin él).»

**Fuente:** `results/rescate_lexico/resumen.json` (1 nov, sistema actual).

**Por qué:** la cifra vieja era de una versión anterior; se volvió a medir.

### A13. Fuera de la lista: registro del directorio (líneas 10–11)

**Viejo:** «…los directorios hetero-asociativos, la lectura B1, el rechazo por containment, la actualización de directorio de todos los agentes y la coordinación punto a punto operan idénticos…»

**Nuevo:** «…los directorios hetero-asociativos, la lectura B1, el rechazo por containment, la actualización perspectival del directorio y la coordinación punto a punto operan idénticos…»

**Fuente:** `src/stage6_interaction.py:259–279`. `register_transaction` registra en el agente de entrada y en el ganador; el TME anota todas.

**Por qué:** es el hallazgo T3 de la auditoría, que solo lo lista en `03`. La misma frase está aquí.

---

## B. Conclusiones (`07_conclusiones.tex`)

### B1. Especificidad (líneas 26–27)

**Viejo:** «La especificidad del contenido fue \textbf{perfecta} en todo el rango de llenado probado (0\% de falsos aceptados con siete clases contrarias por agente).»

**Nuevo:**
> La especificidad del contenido fue casi perfecta: con siete clases contrarias por agente, ningún falso aceptado al llenar con un latente por imagen, y 5 de 656 imágenes de test (0.8\%), todas entre animales, con el llenado de 16 variantes.

**Fuente:** igual que A4 (`results/exp6_capacity/report.md`; `results/experimento13/README.md`, A3, V=16; `raw/Vc16_N200_Vd16_s4*.json`).

**Por qué:** el sistema actual no tiene 0 % de falsos.

### B2. «50 % → 90 %» (líneas 34–35)

**Viejo:** «…(resuelta con la cuantización por magnitud, que llevó la precisión temprana del 50\% al 90\%), …»

**Nuevo:** «…(resuelta con la cuantización por magnitud, que llevó la precisión temprana del 50\% al 88\%; el llenado de 16 variantes la subió a 90\%), …»

**Fuente:** igual que A1. El 50 % no tiene archivo (duda 1).

**Por qué:** el 90 no lo da la cuantización sola.

### B3. Frente a una EHAM única (líneas 42–46)

**Viejo:**
> Con el mismo contenido, el sistema transactivo no clasifica mejor; recuerda con más fidelidad, no mezcla dominios cuando la pista es compartida y se equivoca de dominio siete veces menos, a cambio de cubrir menos y de pagar un índice.

**Nuevo:**
> Con el mismo contenido, el sistema transactivo recuerda con más fidelidad, no mezcla dominios cuando la pista es compartida, acepta menos consultas fuera de dominio cuando el contenido crece y en imagen se equivoca de dominio unas tres veces menos. Desde 50 imágenes por clase también clasifica algo mejor (1.4 puntos con 200); con 25, no. A cambio cubre menos y paga un índice.

**Fuente:** `results/experimento11/README.md` (tabla de A5).
- Dominio ajeno en imagen→texto con N=200, «otro dominio», sobre el total de imágenes:
  - EHAM única: 10.9;
  - oráculo: 4.1 (2.7 veces menos);
  - protocolo: 3.0 (3.6 veces menos).
- Fuera de dominio: EHAM única 8 de 40 con N=200; protocolo con compuerta, 2.

**Por qué:**
- «No clasifica mejor» ya no vale desde N=50.
- «Siete veces» pasa a unas tres.
- La partición también da especificidad fuera de dominio.
- Se deja «cubre menos» sin matizar a propósito. El especialista cubre casi todo (97.5 %), pero el protocolo de exp11 responde al 81.2 % de las imágenes (duda 3).

---

## Dudas para el autor

1. **El 50 % con la binarización por signo** (`06:16`, `07:35`, `01:82`) no tiene archivo en `results/`, `archive/` ni en el historial. Hay que conservarlo como dato de la versión anterior o quitarlo.
2. **τ: 90 % u 88 %.** Depende de si «aceptadas por una clase ajena» significa que alguna clase ajena la acepta (137 de 152) o que la clase propia no la acepta (88 de 100). Propongo la primera, que es la lectura literal de la frase vieja. El 88 % viejo usaba la segunda.
3. **Cobertura del protocolo en exp11 imagen→texto: 81.2 % con N=200, ya antes de los pesos homo.**
   - La tesis no lo dice. Ni la frase vieja ni la nueva lo cubren: hablan del especialista.
   - La causa probable es que exp11 forma los directorios visuales con un latente por imagen (`run_experiment11_monolithic.py:130–136, 309–330`), y la fase A oficial registra 16 variantes. En exp13 sin variantes en el directorio, este acepta 77.0 (A2, V=16).
   - Si se quiere, en A5 cabe media frase: «(el protocolo de este experimento forma su directorio visual sin variantes y responde al 81\,\%)».
4. **Selección sobre test.** Las 16 variantes se adoptaron después de ver exp13, que mide sobre las 656 de test. Son el máximo de la rejilla y no un óptimo ajustado, pero la limitación (f) podría decirlo.
5. **Imprecisión de la auditoría (T2).** Dice «gana en clase desde N=50 (98.5 contra 96.8)», pero 96.8 es la EHAM única con N=200. Con N=50 es 97.6, así que con las homo la ventaja iba de 0.9 puntos (N=50) a 1.7 (N=200). Con una sola hetero la EHAM única queda en 97.5 con N=50 y la ventaja va de 1.2 a 1.4 puntos; por eso A5 da el rango 96.9–97.6 y B3 dice «1.4 con 200». Lo demás de la auditoría que revisé cuadra con los archivos:
   - la compuerta (2.05 %);
   - el árbitro (96.8 → 93.6);
   - los 71 objetos;
   - los 5 de 656;
   - fuera de dominio 2/2/5/8;
   - el precio 1.5 / 4.4 (con una sola hetero, 1.2–1.7 / 3.1).
6. **Desglose por clase.** apple queda en 88.2 %, igual que horse; cow, otro animal, en 100 %. Si se considera que las consultas de apple usan léxico compartido de fruta, A3 podría decir «(\texttt{pear}, \texttt{horse}, \texttt{apple}) quedan en 76--88\%». Lo dejé fuera porque es interpretación.
7. **«625 de 656 con soporte marginal completo»** (A8) solo tiene fuente en la propia tesis (`05:325`) y en el primer reporte de ocho agentes. No lo pude rastrear a un archivo de `results/`. Si `05:321–329` se reescribe en otra parte, conviene decidir si el número se conserva.
8. **A13** no estaba en la lista. Lo incluyo porque contradice `register_transaction` en este mismo archivo.
