# Revisión por fases: Capítulo 5 (Conclusiones) y Apéndice A

Base: `59cca47` (rama `una-hetero`). Archivos tocados:
- `.tex8/secciones/07_conclusiones.tex` (y `.tex_uacj/Capitulo5.tex`, regenerado con `generar_capitulos.py`, que termina con 0 líneas perdidas);
- `.tex_uacj/ConclusionObjetivoGeneral.tex`;
- `.tex_uacj/ApendiceA.tex`.

`Difusion.tex` no se tocó. El texto viejo completo se lee con `git show 59cca47:<ruta>`; aquí va un resumen de lo viejo y el texto nuevo, sección por sección, con la fuente de cada cifra.

---

## Apertura del capítulo (antes de 5.1)

**Viejo.** Un párrafo que presenta EAM-TMS como sistema de ocho módulos y un `\paragraph{Resultados principales.}` con unas veinte cifras del sistema final (calibración fija, dentro de muestra, reservadas, `apple` 13.8 %, hemisferio visual, objetos nuevos, capacidad, líneas base).

**Nuevo.** El mismo párrafo de alcance (clasificadores, etiquetas, Wegner), más el arco de las cinco fases y la regla de comparabilidad entre fases. Se quitó «Resultados principales»: sus cifras pasan a las respuestas por objetivo de 5.1, donde cada una va con su fase.

## 5.1 Con respecto a las preguntas de investigación

**Viejo.** «Respuesta a la pregunta de investigación» (techo entrópico, reparto, límites), «Frente a una EHAM única», «Una memoria de contenido por módulo» y «Lecciones». Todo sobre el sistema de ocho módulos.

**Nuevo.** Se conserva la marca `\paragraph{Respuesta a la pregunta de investigación.}` y le siguen seis párrafos:
1. emergencia (fase 1);
2. lectura (fase 2);
3. escalado (fase 3);
4. propiedades (fase 4);
5. voz y cámara (fase 5);
6. «Lo que se sostuvo y lo que cambió», que remite a `\ref{sec:creencias}`.

La respuesta al techo entrópico («hasta 200 imágenes por clase la memoria única no llega a un techo») queda dentro de la fase 3, junto a exp11 y exp12. «Frente a una EHAM única» y «Una memoria de contenido por módulo» se resumen en la fase 3. Las «Lecciones» (sesgo de lectura y entropía de cuentas) pasan a la fase 2.

### Fuentes de las cifras de 5.1

**Fase 1** (arquitectura: tres módulos, cuatro memorias por módulo, signo, TME, banco de 80). Rutas bajo `results/fase1_tres_modulos/`.

| Cifra | Fuente |
|---|---|
| 26.25 % de acierto y 72.5 % de rechazo con 1 interacción | `exp4_directory_formation/results_formation.csv:2` |
| 91.25 % con 13 | `exp4_directory_formation/results_formation.csv:14` |
| 98.75 % y 1.25 % de rechazo con 80; temprana acumulada 98.73 % | `exp4_directory_formation/results_formation.csv:81` |
| bloqueado: 33.75 % mientras solo hay `apple` | `exp4_directory_formation/results_formation.csv:501` (k = 20, cuentas [55, 0, 0]) |
| bloqueado cruza el 90 % en k = 67 | `exp4_directory_formation/results_formation.csv:548`; `report.md:19` |
| A, B y C terminan en [78, 65, 53] | `exp4_directory_formation/report.md:12-19` |
| ocho módulos: ninguna condición cruza el 90 %, todas en 81.2 % | `results/exp4_directory_formation/report.md:14-21` |

**Fase 2.**

| Cifra | Fuente |
|---|---|
| cruda 53.75 %, B1 98.75 %, B2 75.0 % (tres módulos, N = 80) | `results/fase1_tres_modulos/ablation_mdir_bias/ablation_report.md:27,31,35` |
| `apple` gana el 78.75 % con la lectura cruda | `results/fase1_tres_modulos/ablation_mdir_bias/ablation_report.md:11` |
| B1 supera a la cruda por 4.5 a 8.8 puntos | `results/calibracion_evaluacion_fija/README.md:131` |
| madura 78.9 → 91.0 % (50 a 291 consultas), temprana 89.7 % | `results/calibracion_evaluacion_fija/README.md:109,115,122` |
| principio de tamaño: 1 decisión distinta de 656 y 8 de 411 | `results/experimento22/resumen.txt:8,15` |
| `apple` 20.5 % con la cruda, 2.974 bits | `results/ablation_mdir_bias/ablation_report.md:20,151` |
| B1 deja a `apple` en 13.8 % | reporte vigente, Sección `sec:calibracion` (cifra que ya estaba en las conclusiones viejas) |

**Fase 3** (arquitectura final de ocho módulos, salvo la cifra de tres que se cita para decir que no se compara).

| Cifra | Fuente |
|---|---|
| madura B1 98.75 % (tres) y 81.2 % (ocho) | `results/fase1_tres_modulos/exp3_corrected_routing/summary.json:4`; `results/exp3_corrected_routing/summary.json` (tabla en `plan_reestructura/inventario_fase2_escalado.md`, §2.1 A) |
| 631/656 = 96.2 %, 2 falsos; evocación 113/116 | `results/hemisferio_visual/README.md:3`; `stage7_bidirectional.log:26` |
| objetos nuevos 89.2 % | `results/experimento16/README.md:7-8` |
| codificador por pliegue 87.6 %, falsos 2 → 136 de 3280 | `results/objetos_nuevos_codificador_por_pliegue/README.md:77,88` |
| una memoria por módulo: mismas decisiones en imagen, casi todas en texto | `results/homo_marginal/README.md`; Sección `sec:una-memoria` |
| 96.8 contra 96.9 % con 200 por clase, p = 0.86; empate desde 50 | `results/experimento11_protocolo_corregido/README.md:174-177` |
| fidelidad: −5.39 (5.4 unidades) | `results/experimento11_protocolo_corregido/README.md:262` |
| pista compartida 71.4 contra 51.1 % | `results/experimento11_protocolo_corregido/README.md:265` |
| fuera de dominio 2 contra 8 de 40 (5 % y 20 %) | `results/experimento11_protocolo_corregido/README.md:199` (sección «Fuera de dominio, 40 consultas») |
| imagen: responde 81.2 % contra 100 % | `results/experimento11_protocolo_corregido/README.md:191` (tabla de imagen, N = 200) |
| exp12: brecha 2.54 contra 5.66, M8 peor en 26 de 28 | `UNA_HETERO.md:106-110` |
| exp12: ρ 0.01 (brecha) y ρ 0.49, p 0.008 (error de clase) | `results/experimento12/README.md:13,15` |
| decisores simples 76.0 a 81.5 % contra 81.2 %; imagen 652–655 contra 631 | `results/lineas_base/README.md:180-187`; Sección `sec:lineas-base` |
| `pear` → `apple` 9 y `horse` → `cow` 6 de 28 | `.tex8/secciones/06_discusion.tex:83` (ya estaba en las conclusiones viejas) |
| sin pérdida de clase: 70.4 % | `results/codificador_sin_clase/README.md:60-61` |

**Fase 4** (ocho módulos; arquitectura de cada experimento según `plan_reestructura/inventario_hallazgos.md`).

| Cifra | Fuente | Arquitectura |
|---|---|---|
| directorio unificado: texto 96.2 % unificado y separado | `results/experimento7/README.md:14,17` | final (lectura) |
| lectura inversa: 80/80 y 112/112; 2.9 a 5.5 veces | `results/experimento8/README.md:16-18,43` | anterior (todos registran todo) |
| encadenado 81.9 % con f = 1/64 | `results/experimento10/README.md:24` | anterior (visual sin variantes) |
| agregado en texto 91.0 contra 93.6 % con f = 1/32 | `results/experimento10/README.md:54,63` | anterior |
| sustitución 24.5 % y 0 % de clase; descripción 100 % | `results/experimento9/README.md:33-35` | anterior |
| especialista 98.3 %, ajeno 16.1 % | `results/experimento9/README.md:72-73` | anterior |
| τ cierra 137 de 152 entradas | `.tex8/secciones/06_discusion.tex:496`; Sección `sec:hemisferio-visual` | final |
| 1 % de celdas destruidas → 92 % sin nombre | `.tex8/secciones/06_discusion.tex:248`; `results/homo_marginal/README.md` | final |
| primer término en el vocabulario 96.0 %, nombre 48.0 % | `results/experimento17/parte_a_resumen.txt:6,8` | final |
| color en objetos nuevos 57.8 contra 49.5 % | `results/experimento17/README.md:71,73` | final |
| atributo: mayoritario 98–99 %, minoritario 1–6 % | `results/experimento18/README.md:30-36` | final |
| sonda de rechazo: 10 de 12 | `results/rejection_probe/report.md:26-27` | final |
| 23 imágenes rechazadas que un 1-NN acierta | `.tex8/secciones/05_resultados.tex:1157` | final |

**Fase 5** (versión v5: ocho módulos con tres memorias de contenido por módulo).

| Cifra | Fuente |
|---|---|
| «Farm animal that gives milk» → `cow`; 336 ms + 302 ms ≈ 0.6 s; WAV inyectado | `results/mundo_real/realtime_lab_README.md:113`; `smtex_05_resultados.tex:19-21` |
| 54 ms por cuadro, 26 fps | `results/mundo_real/realtime_lab_README.md:115`; `smtex_05_resultados.tex:23-24` |
| cuadro de cámara rechazado | `results/mundo_real/selftest_frame.png` («RECHAZO (nadie la reconoce)») |
| corrección de color 22, 18 y 15 de 24 | `results/mundo_real/realtime_lab_README.md:174-175`; `smtex_05_resultados.tex:102-104` |
| cámara física: solo `cow` fiable | `results/mundo_real/realtime_lab_README.md:163-164` |
| sin salida cruda, mediciones únicas de julio | `results/mundo_real/README.md` |

**Creencias** (párrafo final de 5.1): filas 1, 2, 4, 8, 11, 12, 14, 15 y 16 de `plan_reestructura/creencias_iniciales.md`. No trae cifras nuevas: la de 10 de 10 sale del mensaje del commit `3f665ab`, citado en la fila 2.

## 5.2 Con respecto al objetivo general (`ConclusionObjetivoGeneral.tex`)

**Viejo.** Seis párrafos con las etiquetas `oe:arquitectura`, `oe:formacion`, `oe:lineas-base`, `oe:rechazo`, `oe:recuperacion` y `oe:vision`, más «En suma».

**Nuevo.** Una frase de cumplimiento y un párrafo por objetivo con las etiquetas nuevas `oe:emergencia`, `oe:lectura`, `oe:escalado`, `oe:hallazgos` y `oe:mundo-real` (las define la sesión del Capítulo 1). Cada párrafo dice si el objetivo se cumplió, con qué alcance y qué quedó pendiente; las cifras son las de 5.1 y tienen las mismas fuentes. La de coincidencia, 92.5 %, sale de `results/calibracion_evaluacion_fija/README.md:69`. «En suma» se quitó porque repetía el cierre del capítulo.

## 5.3 Trabajo futuro

Se conservan los nueve puntos y se agregan tres, en las posiciones 2 a 4:
1. **Barrido del número de módulos con la arquitectura final.** Se toman subconjuntos de 2 a 8 módulos sin reentrenar y se forman de nuevo los directorios. Cuesta unos 17 min por número de módulos y semilla: la etapa 6 tarda 0.61 min, la 7, 15.8 min, y la 8, 1.05 min (`results/computational_cost/comparacion_laptops.md:22-24`, laptop 2, 22 sep). La propuesta sale de `plan_reestructura/inventario_fase2_escalado.md` §4.
2. **Pérdida de un miembro con el protocolo final.** Repetir exp9 con directorios perspectivales, una sola hetero y 16 variantes.
3. **Voz y cámara con cifras.** WER, acierto de enrutamiento con voz, latencias repetidas y conteo con la cámara física, con la arquitectura final y guardando la salida cruda (`plan_reestructura/inventario_fase3_mundo_real.md` §4).

El párrafo de cierre se reescribió en tres oraciones, sin repetir la lista de 5.1.

## Apéndice A

**Viejo.** Tres tablas: hemisferio textual, hemisferio visual y comparaciones. Tenían 22 carpetas y no incluían las de la fase 1 ni las de la fase 5.

**Nuevo.** Hay siete tablas, una o más por fase:
- fase 1;
- fase 2;
- fase 3, en tres tablas: protocolo y formación, tamaño y comparaciones, e imagen;
- fase 4;
- fase 5;
- auxiliares.

Cada tabla tiene cinco columnas: carpeta, qué mide, arquitectura, estado y dónde se reporta. Las abreviaturas de arquitectura se definen al inicio: F1, final, final (lectura), 8 anterior y v5. En total entran todas las carpetas de `results/` del reporte:
- 35 de la raíz;
- las 10 de `results/fase1_tres_modulos/`;
- `results/mundo_real`;
- la comparación «sin carpeta» (`logs_comparacion/`).

Las 23 carpetas médicas, de VisA y de la flota se mencionan en una línea como casos aplicados en curso. La cobertura se comprobó con un script contra `ls results/`.

Estados según `plan_reestructura/catalogo_experimentos.md` y los inventarios:
- **corregidos:** `ablation_mdir_bias` (su evaluación la sustituye `calibracion_evaluacion_fija`), `experimento11` (lo sustituye `experimento11_protocolo_corregido`), `experimento12` (su `veredicto.md` es viejo) y, en parte, `fase1_tres_modulos/exp2_iota_kappa` (vale ι y no κ);
- **reemplazados:** `fase1_tres_modulos/rejection_probe` (por `rejection_probe`), `fase1_tres_modulos/experimento1` y `results/experimento1` (por `fase1_tres_modulos/` y `exp3_corrected_routing`).

**`longtable`:** el preámbulo de `tesis_uacj.tex` no carga `longtable`, y ese archivo no es de esta parte. Por eso las tablas son `table` con `[H]`, partidas para que cada una quepa en una página. Si el integrador prefiere una sola tabla, basta con agregar `\usepackage{longtable}` al preámbulo y convertirlas.

**Columna «Dónde».** Usa solo etiquetas que ya existen (`sec:calibracion`, `sec:eham-unica`, etc.). Para lo que la sesión del Capítulo 4 reporta en secciones nuevas (fase 1, exp7, exp8, exp9, exp12, exp17, exp18, exp22 y fase 5), dice «`\ref{sec:resultados}`, fase N». Si esa sesión define etiquetas `sec:fase…`, conviene cambiarlas al integrar.

---

## Etiquetas

- **Conservadas:** `sec:conclusiones`, `apendiceA`, `tab:exp-texto` (ahora en la tabla de la fase 2), `tab:exp-visual` (fase 3, imagen) y `tab:exp-comparaciones` (fase 3, tamaño y comparaciones). Solo `ApendiceA.tex` citaba las tres de tabla.
- **Nuevas:** `tab:fase1-experimentos`, `tab:fase2-experimentos`, `tab:fase3-experimentos`, `tab:fase3-comparaciones`, `tab:fase3-visual`, `tab:fase4-experimentos`, `tab:fase5-experimentos` y `tab:fase-auxiliares`.
- **Eliminadas:** ninguna.
- **Referencias a etiquetas de otras sesiones:** `oe:emergencia`, `oe:lectura`, `oe:escalado`, `oe:hallazgos` y `oe:mundo-real` (Capítulo 1), y `sec:creencias` (Discusiones). Las viejas `oe:arquitectura` … `oe:vision` ya no se citan desde estos archivos.

## Citas

Solo se usan claves que ya están en `.tex8/referencias.bib`: `pineda2021entropic`, `pineda2022weighted`, `morales2025missing`, `watkins1975buildup` y `wegner1987transactive`. La metamemoria (Nelson y Narens) y Russell no se citan; el texto remite a la Discusión, que puede agregarlas.

## Lo que no pude sostener o dejé fuera

- **exp19** (80.5 contra 79.6 %): no se cita ninguna cifra en el capítulo. En el Apéndice queda como «dos cifras por conciliar».
- **exp9, «90 de 411 con 16 interacciones»:** no se cita. La salvedad del protocolo va en 5.1, 5.2 y el trabajo futuro.
- **exp12, «la ventaja crece con el solapamiento»:** no se usa. Se cita el README vigente (ρ 0.01).
- **Binarización de 8 clases (50 → 85 %):** solo está en el mensaje de un commit, así que no se cita. El cambio de signo a magnitud se menciona sin cifra.
- **Fase 1, κ:** el `README.md` de `fase1_tres_modulos` dice que la copia de `exp2_iota_kappa` es la corregida. Pero el arreglo `29f401c` es de octubre, sobre ocho módulos, y la tabla de tres módulos sale idéntica en todas las columnas de κ, que es la firma del error (`inventario_fase1_tres_modulos.md`, E2). En el Apéndice va como «vale lo de ι». No se usa ninguna cifra de κ de tres módulos.
- **`selftest_frame.png`:** el inventario lo describe como un cuadro de webcam con ropa y habitación. La copia en `results/mundo_real/` muestra un cuadro gris con el aviso «RECHAZO (nadie la reconoce)». El texto dice «un cuadro de la cámara sin ningún objeto de las ocho clases se rechaza», que vale para las dos descripciones.
- **Compilación:** no hay TeX en el entorno. `generar_capitulos.py` termina sin error, y las llaves y los entornos están balanceados (revisado con script).
