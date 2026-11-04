# Inventario de evidencia, fase 2: de 3 a 8 módulos sobre ETH-80

Revisión de solo lectura, 4 nov 2026. No se cambió ninguna rama ni archivo de los repositorios.

**Abreviaturas de rutas**
- `[WT]` = `C:\Users\aq99l\Projects\MAE-TMS-una-hetero` (rama `una-hetero`, la del reporte actual).
- `[MAIN]` = `C:\Users\aq99l\Projects\MAE-TMS` (rama `exp7-directorio-unificado`).
- `[v3]ruta` = `git show origin/v3-experimento1:ruta` (sistema de 3 módulos, junio 2026).
- `[v4]ruta` = `git show origin/v4-8clases:ruta` (primer sistema de 8 módulos, julio 2026).
- `[pre]ruta` = `git show 62995a8^:ruta` en `[WT]` (el reporte `.tex8` antes del replanteamiento del 1 nov).

En el código y en los resultados se dice «agente»; aquí, «módulo».

---

## 0. Lo esencial

1. **No hay ningún experimento que varíe el número de módulos con lo demás fijo.** Todas las comparaciones 3 contra 8 cruzan dos versiones del sistema que difieren a la vez en clases, codificador, cuantización de etiquetas, número de memorias por módulo, banco de consultas y, para imagen, directorio visual, ξ y variantes de llenado.
2. **El reporte actual no tiene ninguna comparación con el sistema de 3 módulos.** Se quitaron todas el 1 nov (`[WT]revision_replanteamiento_prosa.md:3-5`), y el cambio se aplicó en el commit 62995a8 (2 nov). La razón escrita: «ese sistema ya no existe y sus cifras no se pueden volver a medir» (`:5`).
3. **Las comparaciones históricas que sí existen** tienen el mismo script en las dos versiones: protocolo completo (exp3), formación (exp4), capacidad (exp6), ablación, sonda de rechazo, hemisferio visual y costo. Sus cifras salen de archivos versionados en `origin/v3-experimento1` y se pueden citar como antecedente, no como medición controlada.
4. **El cambio de homo a una sola hetero no forma parte del paso 3→8.** Ocurrió cuatro meses después (30 oct a 1 nov) sobre 8 módulos, y en imagen da las mismas decisiones (`[WT]UNA_HETERO.md:33-37`).
5. **La única medición con la misma métrica y arquitectura que varía cuántas clases guarda una memoria** es exp12 (EHAM de 2 clases contra EHAM de 8). No está en el reporte.

---

## 1. Paso de 3 a 8: qué cambió

Los commits del paso 3→8 son 22, de `b281f9c` (1 jul 2026) a `d5b93fa` (14 jul 2026): `git log origin/v3-experimento1..origin/v4-8clases`. La rama `exp7-directorio-unificado` contiene copias rebasadas de esos mismos commits con otros hashes (por ejemplo, `d4a7e3a` = `b281f9c`).

| Aspecto | 3 módulos (v3) | 8 módulos (v4, jul) | 8 módulos (actual, `una-hetero`) | Fuente / commit |
|---|---|---|---|---|
| Clases | apple, horse, car | las 8 de ETH-80 | igual | `[v3]src/stage1_dataset.py:18`; `[v4]src/stage1_dataset.py:18` |
| Codificador | ResNet18, 3 clases, 984 imágenes | reentrenado a 8 clases, 2624 imágenes; nuevo reentrenamiento determinista adoptado el 5 jul (seed 42, RMSE 0.110, acc 99.7 %) | igual que v4 | `[v3]results/computational_cost/report.md:44`; `[WT]results/computational_cost/comparacion_laptops.md:18`; commit `af2c6de` (5 jul) |
| Pistas de texto | `sign(v)`, usa 2 de 16 niveles | magnitud `v/S` con escala global (p99); escala corregida de 0.2276 a 0.1864 al quitar un vector sintético | `S = 0.1881` | `[v3]src/stage4_fasttext.py:58,73`; commits `b281f9c` y `cbe57d8` (2 jul); `[WT].tex_uacj/Capitulo3.tex:800` |
| Memorias por módulo | 4: H (hetero), L y R (homo), `mem_dir` | 5: se agrega `mem_dir_R` (directorio visual por módulo) | 3: la hetero más dos directorios; L y R son lecturas de la hetero (`DomainView`) | `[v3]README.md:20-23`; `[v4]README.md:16-24`; `[WT]UNA_HETERO.md:3,9-12`; commits `b0542ab` (30 oct) y `0c70824` (1 nov) |
| Mediador (TME) | difunde a los 3; registran los 3 módulos y el TME | igual con 8 («Los 4 M_dir… reciben registros idénticos») | perspectival: registran solo entrada, ganador y TME; ruteo `route_transactive` (agregado + encadenado) | `[v3]results/exp3_corrected_routing/report.md:6`; `[v4]results/exp4_directory_formation/report.md:28`; `[MAIN]CONTEXTO_SEP2026.md:58-59`; commit `f54d64f`/`a423950` (14 sep) |
| Llenado | `N_FILL = 200` imágenes por clase, sin variantes | 200 con aumento ×4 (original, espejo, ±12°) | 200 × 16 variantes (3200 registros por módulo) | `[v3]src/stage5_fill.py:39`; mensaje de `b281f9c`; `[WT]src/stage5_fill.py:42,48`; `[MAIN]CONTEXTO_SEP2026.md:138` (23 sep) |
| ξ visual | 0 | 2 | 0 | `[WT]results/experimento1/informe.md:10`; `[v4]src/stage7_bidirectional.py:44`; `[WT]src/stage7_bidirectional.py:46` |
| Umbral de energía del latente | no | no | sí | commit `cc37d2e` (23 sep) |
| Banco de texto | 80 consultas (27/27/26) | 411 (~51 por clase); exp3, exp4 y exp6 usan las 80 primeras (10 por clase) | igual | `[WT]results/experimento1/informe.md:10`; `[v4]README.md:41`; `[WT]run_experiment6.py:182`; `[WT]results/exp3_corrected_routing/report.md:12` |
| Prueba visual | 246 imágenes (3×82); evocación sobre 17 | 656 (8×82); evocación sobre 116 | igual | `[WT].tex/secciones/05_resultados.tex:199,205`; `[WT].tex_uacj/Capitulo4.tex:535,562` |
| Ablación | N ∈ {10, 20, 40, 80} consultas | N ∈ {50, 100, 200, 400} | igual | `[v3]results/ablation_mdir_bias/ablation_report.md:22-59`; `[WT]results/ablation_mdir_bias/ablation_report.md:31-68` |
| Métricas | entropía máxima log2 3 = 1.585 bits; azar 1/3 | log2 8 = 3.000; azar 1/8 (corregido en `0a75c3e`, 6 jul) | igual | `[v3]results/exp3_corrected_routing/report.md:21`; `[WT]results/exp3_corrected_routing/report.md:22` |

Otros cambios del 1 jul (mensaje de `b281f9c`): vocabulario de ConceptNet con TAU 1.0, tope de 20 etiquetas y lista de polisemia (Apple Inc.); el reconocimiento visual deja de pasar por M_dom_H. El puente M_dom_H→directorio de texto se probó y se descartó (no especialista traduce 0 %); esa cifra solo está en el mensaje del commit.

---

## 2. Comparaciones de escala

### 2.1 3 contra 8 módulos (mismo script, otra versión del sistema)

**A. Protocolo completo (exp3), 80 consultas, dentro de muestra**

| métrica | 3 módulos | 8 (v4, jul) | 8 (actual) |
|---|---|---|---|
| precisión temprana | 97.5 % | 80.0 % | 81.2 % |
| rechazo temprano | 1.25 % | 5.0 % | 5.0 % |
| madura B1 | 98.75 % | 82.5 % | 81.2 % |
| madura cruda | 53.75 % | 68.8 % | 72.5 % |
| fidelidad temprana↔madura | 97.5 % | 90.0 % | 92.5 % |
| entropía del directorio | 1.567 de 1.585 | 2.866 de 3.000 | 2.914 de 3.000 |

Fuentes: `[v3]results/exp3_corrected_routing/summary.json:2-6,12`; `[v4]results/exp3_corrected_routing/summary.json:2-6,17`; `[WT]results/exp3_corrected_routing/summary.json:2-6,17`. La copia histórica de 3 módulos está también en `[WT]results/experimento1/informe.md:21-27`.

- **Misma métrica:** sí (mismo script `run_experiment3.py`).
- **Misma arquitectura:** no. Cambian las memorias por módulo (4 contra 5 contra 3), la cuantización, el codificador y el mediador (difusión contra perspectival).
- **Mismo banco:** no. Los dos tienen 80 consultas, pero son unas 27 por clase contra 10. En el sistema actual, el 13.8 % de esas 80 traen el nombre de su clase (`[WT].tex_uacj/Capitulo4.tex:311-313`); para el banco de 3 módulos no encontré esa cifra.
- **Normalizado por azar** (derivado en esta revisión, (acc − 1/K)/(1 − 1/K), de las líneas citadas): B1 = 0.981 con 3 módulos contra 0.786 con 8 (actual); temprana = 0.963 contra 0.786.

**B. Formación del directorio (exp4), 80 consultas**

- 3 módulos: intercalado cruza el 90 % en k = 13; barajado en 15 a 24; bloqueado en 67; final 98.75 % (`[WT]results/experimento1/informe.md:66-69`).
- 8 módulos: ninguna condición llega al 90 %; todas terminan en 81.2 % con 2.914 bits (`[WT]results/exp4_directory_formation/report.md:14-21`; `[WT].tex_uacj/Capitulo4.tex:427-449`).
- **Umbrales comunes**, derivados en esta revisión de los CSV `results_formation.csv`, que tienen las mismas columnas en las dos versiones. Para cada corrida, primer k en que la precisión madura alcanza el umbral:

| umbral | 3 módulos: intercalado / barajado (5 semillas) / bloqueado | 8 módulos actual: intercalado / barajado / bloqueado |
|---|---|---|
| 70 % | 6 / 8–15 / 56 | 13 / 28–42 / 59 |
| 75 % | 9 / 11–18 / 57 | 18 / 40–51 / 71 |
| 90 % | 13 / 15–24 / 67 | nunca / nunca / nunca |

  Filas de referencia en `[v3]results/exp4_directory_formation/results_formation.csv`: línea 7 (A, k=6, 0.7125), 10 (A, k=9, 0.85), 14 (A, k=13, 0.9125), 537 (C, k=56, 0.725), 538 (C, k=57, 0.775), 548 (C, k=67, 0.925). En `[WT]results/exp4_directory_formation/results_formation.csv`: línea 14 (A, k=13, 0.7125), 19 (A, k=18, 0.75), 540 (C, k=59, 0.70), 552 (C, k=71, 0.7875). Las cifras de 8 módulos coinciden con `Capitulo4.tex:447-449`. Las de 3 módulos con el 70 y el 75 % no están escritas en ningún archivo.
- **Misma métrica:** sí. **Misma arquitectura:** no (lo de A). Además, k cuenta interacciones totales: con 3 módulos, 13 interacciones son unas 4 por clase.
- **Aviso.** La frase vieja «Con tres agentes, 10 consultas por dominio bastaban para cruzar el 90 %» (`[pre].tex8/secciones/06_discusion.tex:106-108`) no cuadra con el banco de 3 módulos, que tenía 27/27/26 por clase.

**C. Capacidad de llenado (exp6): la curva de capacidad**

| N por clase | prueba propia, 3 / 8 | falsos, 3 / 8 | precisión temprana por contenido, 3 / 8 | entropía H, 3 / 8 |
|---|---|---|---|---|
| 25 | 0 / 0 % | 0 / 0 | 60.0 / 61.3 | 3.306 / 3.648 |
| 50 | 0 / 0 % | 0 / 0 | 93.8 / 72.5 | 3.722 / 4.369 |
| 100 | 12 / 2 % | 0 / 0 | 98.8 / 78.8 | 3.931 / 4.950 |
| 200 | 57 / 20 % | 0 / 0 | 97.5 / 81.2 | 4.002 / 5.204 |
| 328 | 78 / 56 % | 0 / 0 | 85.0 / 81.2 | 4.039 / 5.318 |

Fuentes: `[v3]results/exp6_capacity/report.md:5-9`; `[WT]results/exp6_capacity/report.md:5-9`; v4: `[v4]results/exp6_capacity/report.md:5-9` (solo N=50 cambia: 71.2 contra 72.5; explicado en `[WT]UNA_HETERO.md:65`).

- **Misma métrica:** sí (mismo script, misma rejilla de N, las 80 primeras consultas del banco).
- **Misma arquitectura:** no (codificador, cuantización, banco). Además, en la copia una-hetero la homo de etiquetas cambia de fondo (`[WT]UNA_HETERO.md:49`).
- **Lo comparable más limpio:** con 0 % de falsos en todo N, la especificidad se sostiene con 7 clases contrarias por módulo en lugar de 2. Pero cuidado: v3 llenaba 1 latente por imagen y exp6 sigue así (`Capitulo4.tex:496`).
- La «precisión temprana» es el ganador por contenido, sin directorio (`Capitulo4.tex:469-470`). Su azar es 33 % contra 12.5 %.

**D. Calibración del directorio (ablación)**

- 3 módulos, N=80: A 53.75 %, B1 98.75 % (`[v3]results/ablation_mdir_bias/ablation_report.md:27,31`).
- 8 módulos, N=400: A 85.25 %, B1 93.00 %, G 93.53 % (`[WT]results/ablation_mdir_bias/ablation_report.md:36,40,68`; en el reporte, `Capitulo4.tex:87-88,101-102`).
- **No son comparables punto a punto:** las N son distintas (no comparten ningún valor), v3 usaba cuantización binaria y F/G quedaron sin efecto con el vocabulario de 8 (mensaje de `0a75c3e`). Solo se sostiene la lectura cualitativa: B1 corrige la lectura cruda en las dos versiones. La brecha cruda−B1 es de 45 puntos con 3 módulos (`[WT].tex/secciones/05_resultados.tex:22`) y de 7.8 con 8 (`Capitulo4.tex:101`).

**E. Hemisferio visual**

| | 3 módulos | 8 (v4, jul) | 8 (actual) |
|---|---|---|---|
| rechazo en la formación (fase A) | 49.7 % (384 imágenes) | — | 0.8 % (1024) |
| enrutamiento de prueba | 81/246 = 32.9 % (100 % sobre aceptadas) | 75.0 %, 0 falsos | 631/656 = 96.2 %, 2 falsos |
| evocación imagen→palabras (top-3) | 16/17 = 94.1 % | 85.3 % | 113/116 = 97.4 % |
| entropía del directorio visual | 1.466 bits | 3.000 de 3.0 | 3.000 |

Fuentes: `[WT]results/experimento1/informe.md:106-109`; `[WT].tex/secciones/05_resultados.tex:194,199,205`; `[v4]README.md:62-64`; `[WT].tex_uacj/Capitulo4.tex:535,562`; `[WT]UNA_HETERO.md:34-36`.

- **No es la misma arquitectura.** Con 8 módulos el directorio visual es por módulo, y ξ, las variantes de llenado y el umbral de energía cambian. Con 3, el directorio visual era el único del TME.
- **Las muestras son muy desiguales:** la evocación con 3 módulos se midió sobre 17 imágenes.

**F. Sonda de rechazo fuera de dominio (12 consultas)**

- 3 módulos: 5 rechazadas y 7 falsos enrutamientos (`[v3]results/rejection_probe/summary.json:4-5`).
- 8 módulos: 10 y 2 (`[WT]results/rejection_probe/summary.json:4-5`; en el reporte, `Capitulo4.tex:339`).
- No es el mismo banco: se reemplazaron 2 de las 12 sondas al recalibrar a 8 dominios (mensaje de `cbe57d8`).

**G. Costo computacional (misma laptop 1, mismo `run_cost_benchmark.py`)**

| etapa (min) | 3 módulos | 8 módulos (jul, 4 variantes) |
|---|---|---|
| encoder | 24.32 | 79.91 |
| llenado (stage5) | 0.50 | 15.73 |
| fase temprana (stage6) | 0.49 | 1.00 |
| hemisferio visual (stage7) | 0.22 | 33.99 |
| fase madura (stage8) | 0.79 | 1.86 |
| pipeline / total con batería | 26.6 / 64.0 | 133.5 / 293.4 |

Fuentes: `[v3]results/computational_cost/report.md:18,21-24,40`; `[WT]results/computational_cost/report.md:18,21-24,34`. Es la misma máquina (i5 de 13.ª generación con RTX 2050 sin usar): `[v3]…report.md:7-9`, `[WT]…report.md:7-9`, `[WT]results/computational_cost/comparacion_laptops.md:7-9`.

- Mediciones posteriores, solo de 8 módulos: laptop 2, 50.6 min en CPU y 31.9 con GPU (`comparacion_laptops.md:25`); 1 nov, 16 variantes, 102.9 min (`[WT]results/computational_cost/nov2026_cpu/report.md:26`; en el reporte, `Capitulo4.tex:1287`).
- **El crecimiento no separa el número de módulos de otras causas.** Cambian también: imágenes del encoder ×8/3, aumento ×4 en el llenado, y formación visual de 384 a 1024 interacciones con directorio visual por módulo. La frase vieja «escala con los datos… no con el número de agentes» (`[pre].tex8/secciones/05_resultados.tex:454-457`) no tenía una medición que la separara.
- **Errata:** `[WT]results/computational_cost/report.md:36` sigue diciendo «984 imágenes» en la corrida de 8 clases. Es el texto fijo del script; `nov2026_cpu/report.md:28` ya dice 2624.

**H. Tamaño de las memorias (analítico, del código)**

- El directorio es una EHAM con p = número de módulos y q = 2 (`[WT]src/associative_memory.py:233-234`). El directorio de texto tiene 300·16·K·2 celdas: 28 800 con K = 3 y 76 800 con K = 8 (derivado). El visual tiene 64·32·K·2: 12 288 contra 32 768 (derivado).
- Cada módulo lleva un directorio de cada modalidad y el TME dos, así que el total de celdas de directorio crece con K². Esto es cálculo, no medición.
- La memoria de contenido de un módulo no depende de K: 9 830 400 celdas (`[WT]results/experimento11/README.md:5`). Un `register` de hetero tarda unos 80 ms sobre una relación de 86 MB (`comparacion_laptops.md:49`).

**I. Afirmación sin archivo de resultados**

Con 8 clases y binarización por signo: temprana 50 % (contra 84.7 % con magnitud), madura B1 65 % (contra 89.0), visual 47 % (contra 73.0), y pear y tomato en 0 %. Estas cifras solo aparecen en el mensaje del commit `b281f9c`. El replanteamiento las quitó porque «hoy no tiene fuente» (`[WT]revision_replanteamiento_prosa.md:183`).

### 2.2 Escala dentro del sistema de 8 módulos (misma arquitectura y métrica)

**J. EHAM única contra partición (exp11), cortes N = 25, 50, 100 y 200 imágenes por clase, 10 semillas**

Se mide el tamaño del contenido, no el número de módulos. Los tres brazos usan la misma arquitectura y las mismas operaciones (`[WT]results/experimento11/README.md:143-154`).

| medida | N=25 | N=50 | N=100 | N=200 | fuente |
|---|---|---|---|---|---|
| clase 1-NN, EHAM única | 97.6 | 97.5 | 97.6 | 96.9 | `Capitulo4.tex:898` |
| distancia d, EHAM única / protocolo / oráculo | 22.9 / 19.5 / 18.2 | 26.6 / 20.8 / 20.4 | 29.4 / 23.7 / 23.3 | 32.5 / 27.2 / 26.8 | `Capitulo4.tex:909-911` |
| imagen→texto, dominio ajeno, EHAM única | 5.5 | 7.5 | 10.5 | 10.9 | `Capitulo4.tex:917` |
| fuera de dominio aceptadas de 40, EHAM única | 2 | 2 | 5 | 8 | `Capitulo4.tex:921` |

- La tabla del protocolo en el reporte sale de `experimento11_protocolo_corregido`.
- La tabla de `experimento11/README.md` (líneas 13, 47, 81, 115) da para el protocolo un ruteo de 95.3, 97.4, 97.4 y 97.0. El reporte da 93.2 y 96.8 (`Capitulo4.tex:907`). **Son dos versiones del protocolo; conviene citar solo la corregida.**

**K. exp12: una EHAM de 2 clases (M2) contra una de 8 (M8), 28 pares, 5 semillas**

- Brecha de fidelidad media respecto del especialista: M2 2.54, M8 5.66. M8 queda peor que M2 en 26 de 28 pares (`[WT]UNA_HETERO.md:106-110`; filas por par en `[WT]results/experimento12/README.md:20-47`).
- Es la única medición, con la misma arquitectura y la misma métrica, de qué pasa cuando una memoria guarda más clases. Apoya el argumento de partir en módulos al crecer el número de dominios.
- **No está en el reporte:** `ApendiceA.tex` no lista `experimento12`.

**L. Capacidad del directorio leído por identidad (exp8), de 1 a 800 registros por módulo**

- La distancia a la instancia real pasa de 3.3 a 20.5 y se estabiliza desde unos 16 registros. El acierto de clase es 80/80 en todo el rango (`[WT]results/experimento8/README.md:112-126`).
- Es de 8 módulos y no está en el reporte.

**M. exp10, directorios perspectivales**

- Varía la fracción f de transmisiones ajenas que presencia cada módulo, no K. El encadenado iguala al pizarrón desde f = 1/64 (`[MAIN]CONTEXTO_SEP2026.md:51-52`).
- En el reporte aparece como `experimento10` (`ApendiceA.tex:80-84`).

### 2.3 Flotas fuera de ETH-80 (otra memoria, otro dominio)

- **Piloto de 24 módulos** sobre VisA, con consultas de medicina como desconocidas: r2 80.8 %, central 88.3, oráculo 93.7; abstención en desconocidas 100 % (`[WT]results/piloto_modulos/resumen.txt:1,7-13`). Etapas 1 y 2 sobre la misma flota: `[WT]results/etapa1_ruteo_dirigido/resumen.txt:5-12`; `[WT]results/etapa2_evidencia/resumen.txt:5-21`.
- **Enrutador de 12 detectores PatchCore:** la MAE manda el 92.4 % a su pieza y 0 % a otra (`[WT]results/enrutador_flota/resumen.txt:6`); estado de 2 027 520 bytes (`:2`).
- **Cascada:** k es el número de piezas candidatas, no de módulos. Los resultados son idénticos con k = 1, 2, 4 y 8 (`[WT]results/cascada_modulos/resumen.txt:5-8`).
- Usan una homo latente por módulo, no el sistema de ETH-80 (`[WT]UNA_HETERO.md:15`).
- Los README escritos a mano del piloto y de las etapas 1 y 2 tienen cifras viejas; los `resumen.txt` están al día (`[WT]inventario_experimentos.md:68-70`).
- En el reporte solo aparece la mención de `Difusion.tex:7`.

---

## 3. Qué está en el reporte actual (`[WT].tex_uacj`)

**Está (solo 8 módulos):**
- Calibración: `Capitulo4.tex:13-200` (tabla en 87-94).
- Protocolo completo y sonda de rechazo: `Capitulo4.tex:305-340`.
- Formación: `Capitulo4.tex:415-449`.
- Capacidad (la curva): `Capitulo4.tex:452-507`, tabla en 480-484.
- Hemisferio visual: `Capitulo4.tex:510-562`.
- EHAM única con cortes de N: `Capitulo4.tex:851-926`.
- Una memoria por módulo: `Capitulo4.tex:1171-1197`.
- Costo de 102.9 min: `Capitulo4.tex:1263-1299`.
- Discusión «funciona con ocho dominios»: `Capitulo4.tex:1305-1342`.
- Apéndice: `ApendiceA.tex:54-61` (exp4 y exp6), `:128-137` (exp11), `:158-161` (costo).

**No está:**
- Ninguna cifra ni mención del sistema de 3 módulos. La búsqueda de «tres módulos/agentes» en `.tex_uacj` solo da `Capitulo4.tex:1466`, que habla de la palabra *fruit* y no de la versión.
- Las frases quitadas estaban en:
  - `[pre].tex8/secciones/01_introduccion.tex:26,34,72` (reporte previo, pregunta «de tres a ocho», contribución 1);
  - `[pre].tex8/secciones/05_resultados.tex:52,226,238,280,302,454-457` (B1 «igual que en tres», formación, invariancia, siete clases contrarias, rechazo visual de ~50 %, costo de 26.6 a 133.5);
  - `[pre].tex8/secciones/06_discusion.tex:9-17,50-51,106-110` («la maquinaria transactiva escala», binarización, «un grupo más grande necesita más interacción»);
  - `[pre].tex8/secciones/07_conclusiones.tex:31,36`.
  
  El detalle de cada cambio está en `[WT]revision_replanteamiento_prosa.md:13-257`.
- exp12 (M2 contra M8), exp8 (capacidad del directorio), el costo por etapa y su comparación entre laptops, y las flotas industriales.
- El reporte de 3 módulos sigue en `[WT].tex/` (por ejemplo, `05_resultados.tex:14-26,106,136-150,194-205,289`) y en `[v3].tex/`.

---

## 4. Qué falta para sostener «el sistema escala de 3 a 8»

**Falta:**
1. **Una comparación controlada en K.** Ninguna medición cambia solo el número de módulos. Todas las diferencias de A a G mezclan K con el codificador, la cuantización, las memorias, el banco, ξ, las variantes y el mediador.
2. **Métricas comparables entre K.** El azar (1/3 contra 1/8), la entropía máxima y las consultas por clase difieren. No hay métrica normalizada en los archivos; la de A es derivada.
3. **El costo atribuible a K**, separado de los datos y de las variantes.
4. **La medición de la binarización con 8 clases**, que solo está en un mensaje de commit.

**Qué se puede obtener sin experimentos nuevos:**
- Releer los CSV y JSON versionados de las dos versiones: los umbrales comunes de formación (2.1 B, ya calculados), la precisión normalizada por azar (2.1 A) y la forma de la curva de capacidad (2.1 C). Así se sostiene a lo sumo «el mismo mecanismo opera con 3 y con 8, con estas cifras», y hay que declarar que las versiones difieren en otros aspectos.
- El argumento analítico del tamaño de las memorias (2.1 H) y exp12 (2.2 K), que sí es una medición controlada sobre cuántas clases guarda una memoria.
- Lo que no se puede: atribuir a K las caídas (98.75 a 81.2 en exp3, por ejemplo). Los modelos de v3 no se guardaron: `[MAIN]LEEME_RESTAURAR.md:26-33` lista solo los modelos v4 y v5. El código está en `origin/v3-experimento1`, pero reentrenar su codificador ya dejó una vez el hemisferio visual en 0 % (`[v3]results/computational_cost/report.md:34-38`), así que volver a correrlo sería un experimento nuevo y sin garantía de reproducir las cifras.

**Lo más barato si se decide medir:** un barrido de K sobre el sistema actual.
- Se toman subconjuntos de 2 a 8 módulos de los modelos actuales, sin reentrenar ni volver a llenar, porque las memorias de contenido son independientes por módulo. Se forman de nuevo los directorios (etapas 6 a 8).
- Costo por K en la laptop 2, con los tiempos medidos: etapa 6 0.6 min, etapa 7 15.8 min, etapa 8 1.05 min (`comparacion_laptops.md:22-24`). Unos 17 min por K y semilla.
- El codificador seguiría siendo el de 8 clases, un confusor que habría que declarar, pero fija todo lo demás.
- Esto sería un experimento nuevo y necesita propuesta y aprobación.

**No está claro:**
- La fracción de consultas con el nombre de su clase en el banco de 3 módulos.
- Si las 80 consultas de v3 se escribieron con el mismo criterio que las 10 por clase de v4.
- Las cifras de N = 25 y 50 del informe de v3, que están marcadas como artefacto de cobertura (`[WT]results/experimento1/informe.md:84-91`).
