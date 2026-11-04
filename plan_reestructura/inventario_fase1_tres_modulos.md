# Inventario de evidencia: fase 1 (tres módulos, apple / horse / car)

Solo lectura. No se cambió de rama ni se tocó ningún árbol de trabajo.

## 0. Dónde vive la evidencia (lo primero que hay que saber)

- **La fase 1 solo existe íntegra en la rama `origin/v3-experimento1`** (punta `c6f0f3d`, 29 jun 2026; no hay rama local con ese nombre). Las cifras de los reportes son de los commits `0ff1619` y `54f30ca` (22 jun 2026).
- **Las carpetas homónimas de `MAE-TMS-una-hetero/results/` NO son la fase 1.** `exp2_iota_kappa`, `exp3_corrected_routing`, `exp4_directory_formation`, `exp5_entropic_prototype`, `exp6_capacity`, `rejection_probe` y `ablation_mdir_bias` se re-corrieron con 8 clases y sobrescribieron los archivos de 3 clases. Comparé byte a byte los 14 archivos de reporte o métricas de v3 contra los de una-hetero y los 14 difieren.
  - `una-hetero:results/exp3_corrected_routing/report.md:14` pone lado a lado «v3 · 3 clases» y «8 clases».
  - `una-hetero:results/rejection_probe/report.md:3-9` declara obsoleta la versión de 3 clases.
  - `una-hetero:results/ablation_mdir_bias/ablation_report.md:5-9` dice que los números son de 8 clases y que la narrativa P1–P7 es «diagnóstico histórico de la era v2 (3 clases…)».
- **La única excepción es `una-hetero:results/experimento1/informe.md`.** Conserva el texto v3 con las cifras de 3 clases, pero su línea 13 avisa que el `summary.json` que cita ya no las contiene. La auditoría lo señaló como puntero roto (`una-hetero:results/auditoria_integral/report.md:48`, M8).
- **Notación de las citas.**
  - `v3:<ruta>:<línea>` = `git show origin/v3-experimento1:<ruta>`, con el número de línea del archivo extraído.
  - `uh:<ruta>:<línea>` = archivo en `C:\Users\aq99l\Projects\MAE-TMS-una-hetero`.
- **Otros sitios revisados sin evidencia de fase 1.**
  - `research_notes/` y `reports/`: tratan de salud y de las homo; la «v3» que aparece ahí es MedMNIST v3.
  - `TRASPASO_19OCT2026.md`: nada de fase 1.
  - `CONTEXTO_SEP2026.md`: su «Fase 1» (línea 75) es una fase de revisión de septiembre, no esta fase.
  - `piloto_modulos`, `cascada_modulos`, `hemisferio_visual` y otras carpetas de `uh:results/`: son de 8 clases o de la línea industrial.

## 1. Arquitectura de la fase 1 (común a todos los experimentos v3)

Fuente: `v3:README.md:9-35`, salvo donde se indica otra.

- **Módulos:** 3 agentes, uno por clase: apple, horse, car.
- **Datos:** ETH-80, 410 imágenes por clase, partición 328/82 (`6001770:conclusiones_experimento1.md:169`).
- **Codificador:** ResNet18 a latente de 64 dimensiones, entrenado sobre las 3 clases (`v3:README.md:10`).
- **Memorias por agente: 4 AMR** (`v3:README.md:16-23`).
  - `mem_dom_H`: hetero etiqueta ↔ latente (n=300, m=16, p=64, q=32).
  - `mem_dom_L`: homo de etiquetas (n=300, m=16).
  - `mem_dom_R`: homo de latentes (n=64, m=32).
  - `mem_dir`: directorio hetero (n=300, m=16, 3 agentes).
  - En suma: tres memorias de contenido (1 hetero y 2 homo) más un directorio.
- **Mediador:** sí, el TME, con `mem_dir_L` (etiquetas → agente) y `mem_dir_R` (latente → agente) (`v3:README.md:25-27`).
- **Fase temprana (TME activo):** la consulta va a los 3 agentes y gana el de mayor `recognize_gated`. Se registra pista → ganador. **Los 4 directorios (TME y 3 agentes) reciben registros idénticos**: es un directorio compartido, no perspectival (`v3:run_experiment4.py:26-28`; bucle en líneas 150-166).
- **Fase madura (TME apagado):** el agente de entrada se elige al azar (semilla 42) y rutea con su `M_dir` en lectura B1, que divide entre (cuentas + 1) (`v3:results/exp3_corrected_routing/report.md:7`; `v3:src/associative_memory.py:130-136`).
- **Pistas de texto:** fastText binarizado con sign(v) ∈ {−1,+1}³⁰⁰ (`v3:README.md:14`).
- **Llenado:** por instancias, N=200 imágenes por clase (`v3:README.md:32`).
- **Parámetros:** ι=κ=ξ=0, σ=0.1 (`v3:results/experimento1/informe.md:11`).
- **Banco de evaluación:** 80 consultas con verdad de base, 27/27/26 (`v3:results/experimento1/informe.md:10`).
- **«Entropía del directorio»:** es la entropía de las **cuentas** de registro por agente, no de la relación. Máximo log2 3 = 1.585 bits (`v3:src/associative_memory.py:147-159`).

## 2. Experimentos de la fase 1

### E0. Experimento 1 original (antes de v3)

- **Rama y fecha:** commits `7a64e4d` / `6001770` / `3f665ab`, del 7 al 8 jun 2026.
- **Arquitectura:**
  - 3 agentes con 4 AMR.
  - Llenado con **un solo latente promediado** por clase (`6001770:conclusiones_experimento1.md:129`).
  - `M_dir` formado por 3 `AssociativeMemory`, una por agente (línea 111).
  - Fase temprana de 10 consultas a mano (línea 177).
- **Qué midió:** si se produce el triple de Wegner y la fidelidad entre la fase temprana y la madura.
- **Cifras:**
  - Ruteo temprano «~8/10» (`6001770:conclusiones_experimento1.md:25`).
  - Fidelidad madura **50 % (5/10)** (líneas 28 y 178).
  - En fase madura, apple fue destino de las 10 consultas (línea 61).
  - La re-corrida `3f665ab` anuncia «fidelidad 10/10 = 100 %», pero su propio mensaje de commit dice que cuenta como coincidencia los dos casos None = None.
- **Estado:** **reemplazado.** `conclusiones_experimento1.md` se borró en `33ba107` (22 jun). La cifra de referencia «~34 %» de acierto temprano crudo de este experimento queda como ancla histórica (`v3:results/exp3_corrected_routing/summary.json:24-27`).
- **Reproducible con una-hetero:** no.

### E1. Experimento 1 v3, sección A (protocolo completo): carpeta `exp3_corrected_routing`

- **Rama y fecha:** `origin/v3-experimento1`; cifras de `0ff1619` y `54f30ca` (22 jun 2026). La carpeta nace en `98b166c` (12 jun).
- **Qué midió:** la secuencia temprana → directorio → madura sobre el banco de 80 consultas.
- **Cifras:** `v3:results/exp3_corrected_routing/summary.json:2-23` y `v3:results/experimento1/informe.md:19-25`.
  - Temprana: **97.5 %**, con 1.25 % de rechazo.
  - Madura con lectura B1: **98.75 %**. Madura con lectura cruda: **53.75 %**.
  - Fidelidad: **97.5 %**.
  - Cuentas del TME **[78, 65, 53]**, entropía **1.567 bits** (máximo 1.585).
  - Rechazo: 79 consultas ruteadas, **0 rechazos de la EAM**, 1 por frontera del codificador (sin vector fastText) (`summary.json:13-17`).
  - Réplica de las 10 TEST_QUERIES: cuentas [6, 7, 6] (`summary.json:19-23`).
- **Estado:** histórico; no está retractado.
  - **Dentro de muestra:** la fase madura se evalúa sobre las mismas 80 consultas que llenaron el directorio. Se declaró después, en `0258d59` (26 oct), y aplica al mismo protocolo (`uh:results/exp3_corrected_routing/report.md:8`).
  - En el banco principal la EAM no rechazó nada: el único rechazo es léxico (de frontera).
  - La cifra de 98.75 % ya **no tiene fuente en `results/`** de una-hetero (`uh:revision_tesis_auditoria_prosa.md:134-148`, duda 1 en la línea 703). Su fuente válida es `git show 0ff1619:results/exp3_corrected_routing/summary.json`.
- **Reproducible con una-hetero:** no (ver §5).

### E2. Sección B (ι × κ): carpeta `exp2_iota_kappa`

- **Rama y fecha:** v3, 22 jun 2026.
- **Qué midió:** si ι y κ quitan el sesgo de masa sin la normalización B1.
- **Cifras:**
  - ι=0: 98 % con 1 % de rechazo; ι=0.25: 78 % (21 % de rechazo); ι=0.5: 54 % (45 %); ι=1.0: 0 % (100 % de rechazo). Los valores son **idénticos en todas las columnas de κ** (`v3:results/exp2_iota_kappa/report.md:24-27`).
  - Diagnóstico con 11 pistas: 100 % con solo la compuerta, contra 90.9 % con la división entre mem.mean (`v3:results/experimento1/informe.md:43-44`).
  - Flujo posterior: la madura cruda da 53.8 % y la B1 98.8 % en las tres condiciones (`report.md:33-35`).
- **Estado:**
  - La conclusión «κ inerte» está **corregida como bug**. El commit `29f401c` (26 oct) explica que la compuerta comparaba una suma sobre las coordenadas de la pista contra κ·mem.mean, que es una cantidad por celda (razón ~364–388), «así que la compuerta nunca se disparaba».
  - La tabla v3, idéntica en todas las columnas de κ, tiene la misma firma. Por eso lo de κ en v3 no prueba nada.
  - Lo de ι sigue en pie como observación de 3 clases.
- **Reproducible con una-hetero:** no. El script de una-hetero es otro: compara por celda y saca la rejilla de κ de cuantiles (`abf1735`).

### E3. Sección C (formación del directorio): carpeta `exp4_directory_formation`. Evidencia central

- **Rama y fecha:** v3, 22 jun 2026 (`0ff1619`).
- **Qué midió:** después de cada interacción k (k = consulta del banco, no imagen), congela el `M_dir` y evalúa la fase madura sobre las 80 consultas. Registra acierto, rechazo, entropía de cuentas y cuentas.
  - Condiciones: A intercalado; B barajado con 5 semillas; C bloqueado por dominio; D control con puntuación cruda en la fase temprana (`v3:run_experiment4.py:9-24`).
- **Cifras** (`v3:results/exp4_directory_formation/report.md:12-19`). La transición se define como acierto madura ≥ 90 %; se da el primer k y el k desde el que se sostiene.
  - A: primer k = 13, sostenido desde 47, final 98.8 %.
  - B: primer k entre 15 y 24, sostenido entre 24 y 44, final 98.8 % en las 5 semillas.
  - C: k = 67 (primero y sostenido), final 98.8 %.
  - D: primer k = 14, sostenido desde 66, final **93.8 %**, cuentas [84, 67, 45], entropía 1.541.
  - A, B y C terminan en las mismas cuentas [78, 65, 53] y la misma entropía 1.567.
- **Curva A** (`v3:results/exp4_directory_formation/results_formation.csv`; cada valor con su línea):

  | k | acierto madura | rechazo | entropía (bits) | línea |
  |---|---|---|---|---|
  | 1 | 26.25 % | 72.5 % | 0 | 2 |
  | 3 | 58.75 % | 40.0 % | 1.561 | 4 |
  | 10 | 87.5 % | 11.25 % | — | 11 |
  | 13 | 91.25 % | 8.75 % | — | 14 |
  | 27 | 97.5 % | 2.5 % | — | 28 |
  | 40 | 88.75 % | 1.25 % | — | 41 |
  | 80 | 98.75 % | 1.25 % | 1.567 | 81 |

  - En k = 40 la curva **baja de 90 %**: no es monótona.
  - El acierto temprano acumulado al final es 98.73 % (línea 81): la madura llega al mismo techo que la temprana.
- **Curva C (bloqueado):**
  - De k = 1 a k = 27 solo registra apple: cuentas [77, 0, 0] y entropía 0 (líneas 482-508).
  - El acierto se queda en **33.75 %**, que es la parte de apple en el banco, con rechazo de 1.25 % desde k = 20 (línea 501).
  - Sube a 63.75 % cuando entra horse (k = 40, línea 521) y a 92.5 % ya en el bloque de car (k = 67, línea 548).
- **Curva D:** el acierto temprano acumulado cae a 72.15 % (línea 641). El sesgo de la fase temprana se hereda en el directorio.
- **Estado:**
  - **Vigente como resultado de 3 clases, con una limitación declarada después.** La curva mide cuánto del banco cubren los tokens ya registrados, no generalización (`0258d59`; texto en `uh:results/exp4_directory_formation/report.md:8`).
  - Error menor de redacción en el .tex v3: dice «presentando las imágenes» (`v3:.tex/secciones/05_resultados.tex:92`), pero k cuenta consultas de texto.
  - El .tex y el informe dan «k = 13» sin decir que el acierto vuelve a bajar de 90 % antes de sostenerse en 47 (`v3:results/experimento1/informe.md:64`).
  - **Con 8 clases el resultado no se repite:** ninguna condición llega a 90 % y todas terminan en 81.2 %, incluido el control crudo (`uh:results/exp4_directory_formation/report.md:14-21`).
- **Reproducible con una-hetero:** no tal cual. `run_experiment4.py` existe con el mismo protocolo, pero corre sobre 8 clases y cuantiza por magnitud (§5).

### E4. Sección D (capacidad de llenado): carpeta `exp6_capacity`

- **Rama y fecha:** v3, 22 jun 2026.
- **Qué midió:** generalización a imágenes nuevas, falsos positivos entre clases y ruteo por etiquetas según N.
- **Cifras** (`v3:results/exp6_capacity/results_capacity.csv:2-6`; `report.md:5-9`):

  | N | test propio | falsos | ruteo |
  |---|---|---|---|
  | 25 | 0 % | 0 % | 60.0 % |
  | 100 | 11.7 % | 0 % | 98.8 % |
  | 200 | 56.7 % | 0 % | 97.5 % |
  | 328 | 78.3 % | 0 % | 85.0 % |

  - El informe aclara que con N < 92 hay un artefacto de cobertura (`v3:results/experimento1/informe.md:88-89`).
- **Estado:** histórico. Una-hetero lo re-corrió con 8 clases y da otros números: con N=200, test propio 20 % y ruteo 81.2 % (`uh:results/exp6_capacity/report.md:8`).
- **Reproducible con una-hetero:** no.

### E5. Prototipo entrópico: carpeta `exp5_entropic_prototype`

- **Rama y fecha:** v3, **solo `98b166c` (12 jun)**. No se re-corrió en el saneamiento del 22 jun.
- **Qué midió:** llenado delta (latente promediado) contra llenado por instancias, con 50 instancias por clase (`v3:results/exp5_entropic_prototype/report.md:3-6`).
- **Cifras** (`report.md:12-16`):
  - Recuerdos distintos: 1/12 → 12/12.
  - Aceptación inversa en entrenamiento: 0 → 100 %; en prueba: 0 → 0 %.
  - Ruteo temprano: 97.5 % (2.5 % de rechazo) en ambos llenados.
  - Entropía de M_dom_H: 0.775 → 3.933.
- **Estado:**
  - Anterior al protocolo final de v3: usa 50 instancias y no 200, y su rechazo de 2.5 % no coincide con el 1.25 % de E1.
  - Sirve como evidencia cualitativa de que el llenado por instancias da variedad, no como cifra del sistema v3.
  - No dice nada del directorio.
- **Reproducible con una-hetero:** no.

### E6. Sonda de rechazo: carpeta `rejection_probe`

- **Rama y fecha:** v3, `54f30ca` (22 jun 2026).
- **Qué midió:** 12 consultas representables fuera de apple/horse/car.
- **Cifras:** **5 rechazadas por la EAM**, 7 ruteos falsos (`v3:results/rejection_probe/summary.json:4-5`; `report.md:15-16`).
- **Estado:** el .md de 3 clases quedó **obsoleto** (`uh:results/rejection_probe/report.md:3-9`; `uh:results/auditoria_integral/report.md:22`, C2). En git, la cifra de 3 clases vale.
- **Reproducible con una-hetero:** no.

### E7. Ablación del sesgo de M_dir: carpeta `ablation_mdir_bias`

- **Rama y fecha:** v3; fechada el 7 jun y re-corrida el 22 jun (`0ff1619`).
- **Qué midió:** 9 condiciones × N ∈ {10, 20, 40, 80} × 5 semillas (`v3:results/ablation_mdir_bias/ablation_report.md:20-59`).
- **Cifras en N=80:**
  - A, base: madura 53.75 %, fidelidad 56.25 % (línea 27).
  - **B1: 98.75 %** (línea 31).
  - B2 (÷√cuentas): 75.0 % (línea 35).
  - F (ConceptNet curado): 80.0 % (línea 55).
  - G (D + B1 + F): 98.72 % (línea 59).
  - Ganadores en A: apple 78.75 %, horse 17.5 %, car 2.5 % (líneas 75-76).
  - Cuentas en A: [78, 65, 53] (líneas 139-140).
- **Estado:**
  - Narrativa histórica (`uh:results/ablation_mdir_bias/ablation_report.md:5-9`); también dentro de muestra.
  - Una relectura posterior sostiene que B1 (dividir entre cuentas) es «contabilidad externa, no maquinaria de memoria». El directorio con pistas derechas one-hot se factoriza en K tablas de cuentas independientes (`uh:discusion_directorio_entropico.md:35`).
- **Reproducible con una-hetero:** no.

### E8. Sección E (hemisferio visual)

- **Fuente:** el informe remite a un log de la etapa 7, `v3:rerun_refactor.log`, del **12 jun** (`98b166c`; igual en `rerun_oficial.log:118-125`).
- **Cifras** (`v3:rerun_refactor.log:110-117`):
  - Fase A: 384 imágenes, ruteo 100 %, **rechazo 49.7 %**.
  - Cuentas de `mem_dir_R`: [91, 71, 31], entropía 1.466 bits.
  - Ruteo de test: **81/246 = 32.9 %**, con 67.1 % de rechazo.
  - Evocación top-3: **16/17 = 94.1 %**, una muestra muy chica.
- **Estado:**
  - El log es anterior al saneamiento del 22 jun. El informe afirma que esta etapa no se vio afectada (`v3:results/experimento1/informe.md:109-110`), y no encontré una corrida posterior que lo confirme.
  - Fragilidad documentada: con un codificador re-entrenado, el hemisferio visual quedó en 0 % de aceptación (`v3:results/computational_cost/report.md:34-38`).
  - Reemplazado por la versión con aumentación: el rechazo de fase A bajó del «≈50 % de la versión de tres agentes» (`uh:revision_v16_prosa.md:7`).
- **Reproducible con una-hetero:** no.

### E9. Costo computacional

- **Rama y fecha:** v3, `5360b45` (22 jun).
- **Cifras:**
  - Pipeline de 26.6 min, de los cuales 24.3 son del codificador.
  - Todo el sistema asociativo tarda menos de 2.5 min en CPU (`v3:results/computational_cost/report.md:18`, `40` y `46-48`).
- **Estado:** histórico; no es comparable con los costos de 8 módulos.

## 3. ¿Emerge el directorio con el uso? (3 módulos)

- **Arranque.** El directorio empieza vacío. Con una interacción la fase madura acierta 26.25 % y rechaza 72.5 %. En k = 13 ya acierta 91.25 % y rechaza 8.75 %; en k = 80 acierta 98.75 % y rechaza 1.25 % (`v3:…/exp4_directory_formation/results_formation.csv:2`, `14` y `81`).
- **Rechazo.** Baja a medida que se registran tokens; aquí «rechazo» significa que ningún agente tiene soporte en el directorio.
- **Entropía.** Las cuentas se equilibran en 3 interacciones (1.561 bits, línea 4) y terminan en 1.567 de 1.585.
- **Experimento más claro: el orden bloqueado.** Mientras solo se vio apple, el directorio solo rutea apple: se queda en 33.75 % con entropía 0 (líneas 482-508). Solo cruza 90 % ya en el bloque de car (k = 67). El directorio no rutea lo que no presenció.
- **El orden afecta la velocidad, no el destino.** A, B y C terminan en [78, 65, 53] (`v3:…/report.md:12-18`).
- **Solidez: media.** El efecto es real y fácil de leer, pero:
  - (a) Se evalúa **dentro de muestra**, sobre las mismas 80 consultas que lo llenan; la curva mide cobertura de tokens, no generalización (`0258d59`).
  - (b) El techo lo pone la fase temprana: el directorio copia al ganador por contenido (98.73 % temprano contra 98.75 % maduro, línea 81).
  - (c) Un solo banco, un solo codificador y 5 barajados; no hay intervalos.
  - (d) Hace falta B1 (98.75 % contra 53.75 % crudo), que es división externa entre cuentas.
  - (e) La «entropía» es de cuentas, no de estructura.
  - (f) El directorio era compartido, no perspectival.
  - (g) **Con 8 clases no se reproduce el umbral:** no se llega a 90 % y el final es 81.2 % (`uh:results/exp4_directory_formation/report.md:14`).

## 4. Diferencias entre la fase 1 y el sistema final (una-hetero)

| aspecto | fase 1 (v3) | sistema final | fuente del final |
|---|---|---|---|
| módulos y clases | 3 (apple, horse, car) | 8 de ETH-80 | `uh:src/eval_bank.py:12` |
| memorias de contenido por módulo | 3 (1 hetero y 2 homo) | 1 hetero; las homo son lecturas (`DomainView`) | `uh:UNA_HETERO.md:3-13`; commit `0c70824` |
| directorios | 4 idénticos (TME + 3), compartidos | uno textual y uno visual por agente, perspectivales (registran el de entrada, el ganador y el TME); ruteo transactivo (agregado y encadenado) | `uh:README.md:47-60`; `a423950` |
| directorio visual | solo en el TME | en cada agente | `uh:README.md:18-23` |
| pistas de texto | sign(v), 2 de 16 niveles | por magnitud, v/S con escala global | `uh:src/quantizer.py:50-58` |
| llenado | 200 imágenes por clase | 16 variantes, 3200 registros por agente | `CONTEXTO_SEP2026.md:113` |
| fase madura textual | solo B1 | B1 más doble compuerta de contenido | `CONTEXTO_SEP2026.md:131` |
| banco | 80 consultas (27/27/26) | ~411 (≈50 por dominio) | `uh:README.md` (sección v4) |
| codificador | entrenado con 3 clases | re-entrenado con 8 | `uh:README.md:10` |
| azar y entropía máxima | 1/3 y 1.585 bits | 1/8 y 3.0 bits | — |

- **Conclusión.** Las cifras de la fase 1 **no son comparables numéricamente** con las del sistema final: cambian el número de clases, el azar, la cuantización, las memorias, el registro y el banco. Solo se comparan en sentido cualitativo, por la dirección de los efectos.
- **Nota.** La tabla de `uh:README.md:16-28` todavía describe «5 AMRs», que es anterior a `0c70824`.

## 5. Reproducibilidad

- **Con el código de una-hetero: no.**
  - Las 3 clases no se pueden fijar con un parámetro: `CLASSES` está escrita con 8 clases en al menos siete módulos (`uh:src/eval_bank.py:12`, `stage1_dataset.py:18`, `stage2_encoder.py:32`, `stage3_conceptnet.py:29`, `stage4_fasttext.py:17`, `stage5_fill.py:37`, `stage6_interaction.py:42-43`).
  - Correrlo con 3 clases exigiría re-entrenar el codificador y rehacer el banco. Con la cuantización por magnitud, una sola hetero y el registro perspectival, el resultado sería un experimento nuevo, no una reproducción.
- **Desde `origin/v3-experimento1`: el código está completo en git, pero faltan los modelos.**
  - Los pesos (`models/*.pt`, `*.pkl`) no están versionados (`v3:README.md:169`).
  - El README advierte que las cifras exactas necesitan el codificador original (`v3:README.md:142-144`).
  - En `MAE-TMS/models` solo hay modelos de 8 clases. No encontré los pesos del codificador de 3 clases, aunque no revisé a fondo las carpetas de respaldo, que según `LEEME_RESTAURAR.md:26` son v4 y v5.
  - Un re-entrenamiento ya demostró ser frágil: el hemisferio visual quedó en 0 % (`v3:results/computational_cost/report.md:34-38`).

## 6. Lo que no está claro

- No encontré una corrida de la etapa 7 (hemisferio visual) posterior al 22 jun que respalde las cifras de E8.
- No verifiqué ejecutando que el bug de κ (`29f401c`) esté en el script v3. Lo infiero porque la tabla v3 es idéntica en todas las columnas de κ, que es la firma descrita en el commit.
- El informe v3 dice que el llenado es de 200 por clase, pero exp5 usa 50. Es la versión del 12 jun y no se alineó.
