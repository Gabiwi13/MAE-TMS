# Grupo 1: `main.tex`, `01_introduccion.tex`, `02_marco_teorico.tex`

Fuentes: `revision_una_hetero_prosa.md` (UH), `revision_tesis_auditoria_prosa.md` (AUD), `revision_pesos_homo_principal_prosa.md` (PH). Las líneas son las del archivo ya editado. Sin compilar, sin commit, sin tocar figuras.

## Aplicados tal cual

- UH §0, título → `main.tex:43–46` (título del Encuentro, mayúscula solo inicial, «Versión de 8 módulos»)
- UH §0, «multi-agente» del resumen → `main.tex:57` («sistema distribuido de memoria transactiva»)
- UH §0, «multi-agente» de la introducción → `01_introduccion.tex:38–41`
- AUD M1 → `main.tex:65–67`
- AUD I1 → `01_introduccion.tex:17–18`
- AUD I2 (decisión 1, sin el 98.75 %) → `01_introduccion.tex:26–28`
- AUD I3 → `01_introduccion.tex:48–52`
- AUD I5 (decisión 11, sin el 50 %) → `01_introduccion.tex:85–86`
- AUD I7 (marcado «opcional»; la guarda `fold is not None` sigue en `src/hetero_lib/hetero_associative_4d.py:68` y `hetero_lib` no cambió entre b0542ab y HEAD) → `01_introduccion.tex:104–105`
- UH 1a → `02_marco_teorico.tex:73–75`
- UH 1b → `02_marco_teorico.tex:186–188`
- UH 1c (en lugar de AUD F2) → `02_marco_teorico.tex:206–207`
- UH 1d → `02_marco_teorico.tex:216–219`
- UH 1e (en lugar de AUD F3), con la etiqueta `eq:marginal` → `02_marco_teorico.tex:225–257`
- AUD F5 → `02_marco_teorico.tex:304–313`
- Regla «agente» → «módulo»: `main.tex` (título y 61, 66, 75, 78, 83), `01` (las 12 apariciones: 26, 33, 42, 46, 48–50, 73, 88–97, 123) y `02` (172, 269, 305–311; las de 203 y 224 salen con 1c y 1e). Los «miembros» de Wegner se quedan como miembros.
- Prefijos sin guion: `main.tex:59`; `01:58, 89, 120`; `02:74, 139, 142, 160, 172, 174, 221`. Los bloques nuevos (F1, 1a, 1e, I6) van también sin guion («homoasociativa», «heteroasociativa», «autoasociativas»).

## Aplicados con ajuste

- **AUD M2 + decisión 2** → `main.tex:75–82`. Cifras del bloque Nuevo (90.0, 93.0, 13.8, 96.2 = 631/656, 3.5 %, dos falsos, 3.000 bits). Para la decisión 2 agregué al paréntesis «ablación de calibración, con un directorio compartido». Las tres cifras de texto (temprana, madura y apple) salen de esa ablación, así que el paréntesis vale para las tres.
- **AUD I4** → `01_introduccion.tex:77–79`. El Nuevo decía «el protocolo de registro y de coordinación cambió en esta versión (contribución~3)». Eso es historia de versiones, y la regla del estado final no deja agregarla. Quedó así: «escalan a ocho módulos, con el registro por transacción y la coordinación de la contribución~3». Se quita igual el «sin cambios en el mecanismo», que era lo falso.
- **AUD I6 + decisión 3** → `01_introduccion.tex:88–98`. Apliqué el Nuevo y cambié la última frase. En lugar de «La alternativa de un puente por el TME se evaluó y fue descartada» va el mecanismo de `03_arquitectura.tex`, como razón de diseño, sin «nuevo en esta versión» y sin «0 %»: «El directorio visual es propio porque un puente por la memoria de contenido del módulo de entrada hacia el directorio de texto no redirige cuando ese módulo no es el especialista: su memoria de contenido no contiene el latente ajeno».
- **AUD F1** → `02_marco_teorico.tex:78–87`. Choca con la arquitectura de una sola memoria, porque el Nuevo cerraba con «el de la memoria homo-asociativa no interviene, porque el sistema usa sus pesos y no su decisión», y el sistema ya no tiene memorias homo. Quedó así: «el criterio homoasociativo no interviene: de las lecturas de dominio de la memoria de contenido (ecuación~\eqref{eq:marginal}) el sistema usa los pesos y no esa decisión». Lo comprobé en el código de la copia. `DomainView._am` fija κ = 0. `recog_weights` solo da pesos. El reconocimiento visual (`stage7_bidirectional.py:122–125`) aplica containment sobre esos pesos, no κ. El resto de F1 va igual.
- **AUD F4 + decisión 14** → `02_marco_teorico.tex:275–279`. Wegner va parafraseado, sin comillas. En la frase sobre el sistema («de modo que cada miembro sabe de los demás lo que presenció») cambié «miembro» por «módulo»: habla del sistema, no del grupo de Wegner.

## No aplicados

- AUD F2 y F3: reemplazados por UH 1c y 1e, como pide el encargo.
- PH: ningún bloque cae en estos tres archivos (1a y 1b van en 04; lo demás, en 05, 06 y 07).
- Contribución 5 (`01:108–113`), «junto con el costo computacional de la reproducción íntegra»: sin tocar (decisión 9).

## Historia de versiones que dejé para el autor (ninguna propuesta la cubre)

- `main.tex:57`: «describe la segunda versión del sistema…».
- `main.tex:61`: «El sistema escala de tres a ocho módulos especialistas».
- `01:26–36`: el párrafo del reporte previo de tres módulos (I2 solo quitó la cifra) y la pregunta de investigación, que plantea la tesis como escalado «de tres a ocho».
- `01:41`: «se compone en esta versión de».
- `01:61–62`: «(un cambio central de esta versión frente a la binarización por signo anterior)».
- `01:70`: «cinco contribuciones concretas respecto a la versión anterior».
- `01:73–76`, contribución 1: «El sistema pasa de 3 a 8 categorías…, con el encoder visual reentrenado…, el vocabulario semántico regenerado y el banco de evaluación extendido…».
- `01:81–84`, contribución 2: «La binarización por signo de fastText (…) se reemplaza por…».
- `01:100–106`, contribución 4: «se eliminó el único vector sintético…» y «corridas posteriores a esa auditoría».
- Dentro de bloques aplicados, lo dejé como venía: «sesgo histórico» (`main.tex:78`, M2) y «3 bits en esta versión» (`02:306`, F5).
- `main.tex:48`, `\date{Julio 2026}`: no es historia, pero es una fecha que ya no corresponde.

## Problemas encontrados

1. **`02:153` contradice a 1e.** Dice que $(m+1)$ y $(q+1)$ «incorporan \emph{centinelas} en la posición cero». El 1e nuevo, y el código, ponen el valor indefinido en el último índice ($k = m$, $l = q$). En el código, `undefined(dim)` devuelve `m` o `q` (`hetero_associative_4d.py:201–202`) y `_set_margins` llena `[:, :, m, :]` (`:696`). Ninguna propuesta lo cubre y no lo cambié. Arreglo sugerido: «en la última posición».
2. **`02:269`**: con la regla, «no contienen nociones de directorio, agentes ni memoria transactiva» pasó a «…directorio, módulos ni…». Ahí «agentes» se refería a la idea de multiagente, y «módulos» puede leerse raro. Conviene revisarlo.
3. Referencias que crean otros archivos: `sec:una-memoria` (05) se usa en `02:255`; `sec:param-iota-kappa` (05:167) y `sec:componentes` (03:12) ya existen. `eq:marginal` se define en `02:237` y F1 y 1b la citan antes, por adelantado.
4. La nota al pie de 1e usa `\url`, que da `hyperref` (ya cargado). No compilé.
