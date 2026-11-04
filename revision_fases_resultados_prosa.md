# Revisión por fases: Sección 4.1, Resultados

Base `59cca47`. Archivos tocados: `.tex8/secciones/05_resultados.tex` y su salida regenerada en `.tex_uacj/Capitulo4.tex` (solo la parte de Resultados; la de Discusiones sale igual). `generar_capitulos.py` termina sin error: «líneas de .tex8 que no aparecen en la salida: 0». No hay `xelatex` en la sesión, así que no se compiló.

## 1. Estructura vieja y nueva

Las subsecciones existentes bajan un nivel (`\subsection` → `\subsubsection`) y quedan dentro de su fase. No se reordenó nada: el orden actual ya era el que pide la fase 3. El texto viejo se conserva salvo los cambios de la sección 3 de este documento.

| Antes (5.x / 4.1.x) | Después |
|---|---|
| — | **4.1.1 Fase 1: formación del directorio con tres módulos** (`sec:fase1-resultados`), nuevo |
| — | **4.1.2 Fase 2: lectura del directorio** (`sec:fase2-resultados`), párrafo nuevo con la ablación de tres módulos |
| Calibración del directorio con ocho módulos (`sec:calibracion`) | dentro de 4.1.2, sin cambios |
| Calibración con un conjunto de evaluación fijo (`sec:calibracion-fija`) | dentro de 4.1.2, sin cambios |
| — | Principio de tamaño contra B1 (`sec:fase2-tamano`), nuevo (exp22) |
| — | **4.1.3 Fase 3: escalado a ocho módulos** (`sec:fase3-resultados`), párrafo nuevo |
| Protocolo completo, ι×κ, Formación, Capacidad, Hemisferio visual, Objetos nuevos, Codificador sin pérdida de clase, EHAM única | dentro de 4.1.3, en el mismo orden |
| — | Una EHAM de dos clases contra una de ocho (`sec:fase3-dos-clases`), nuevo (exp12), después de la EHAM única |
| Líneas base, Una memoria por módulo, Costo | dentro de 4.1.3, en el mismo orden |
| — | **4.1.4 Fase 4: hallazgos con ocho módulos** (`sec:fase4-resultados`), nuevo: índice (exp7, exp8), perspectiva y pérdida de un miembro (exp10, exp9), imagen y palabra (exp17, exp18, exp19) |
| — | **4.1.5 Fase 5: demostración en tiempo real** (`sec:fase5-resultados`), nuevo |

En la plantilla UACJ las `\subsubsection` no llevan número (secnumdepth 2), así que una remisión a `sec:calibracion`, `sec:eham-unica`, etc. imprime el número de la fase que la contiene (4.1.2, 4.1.3). Las remisiones siguen llevando a la sección correcta.

## 2. Etiquetas

- **Se conservan todas** las de 59cca47 (`sec:calibracion` … `sec:costo`, todas las `tab:` y `fig:`). Se verificó con `diff` sobre la lista de `\label`.
- **Nuevas:** `sec:fase1-resultados`, `sec:fase2-resultados`, `sec:fase2-tamano`, `sec:fase3-resultados`, `sec:fase3-dos-clases`, `sec:fase4-resultados`, `sec:fase4-indice`, `sec:fase4-perspectiva`, `sec:fase4-imagen-palabra`, `sec:fase5-resultados`, `tab:fase1-formacion`, `tab:fase4-perspectiva`.
- **Eliminadas:** ninguna.
- Todas las `\ref` de 05 resuelven a etiquetas que existen en `.tex8/secciones/` de 59cca47.
- No se agregó ningún `\cite`.

## 3. Cambios en el texto que ya existía

**Apertura de la sección.**
- Viejo: «Las secciones siguen el orden de la Sección~\ref{sec:organizacion}. Salvo indicación en contrario, los experimentos usan los parámetros de la Sección~\ref{sec:parametros}, y todos los números son trazables a corridas de este sistema (Sección~\ref{sec:auditoria}).»
- Nuevo: «Los resultados siguen las cinco fases de la Sección~\ref{sec:organizacion}. Las cifras de la fase 1 son de su propia arquitectura, con tres módulos, y se rotulan así. Con ocho módulos, en las fases 2 a 4, los experimentos usan los parámetros de la Sección~\ref{sec:parametros} salvo indicación en contrario. Todos los números son trazables a archivos de `results/` (Sección~\ref{sec:auditoria}), y los de la fase 5 son mediciones únicas de una demostración.»

**Formación del directorio transactivo** (`sec:formacion`), al final del párrafo «Con 10 consultas por clase, ninguna condición llega al 90 %», se agregan dos oraciones:
- «Con tres módulos, la misma curva, sobre 80 consultas de unas 27 por clase, cruzaba el 90 % tras 13 interacciones y terminaba en el 98.75 % (Sección~\ref{sec:fase1-resultados}). Entre las dos corridas cambiaron también el banco, el codificador, la cuantización y el registro del directorio, así que la diferencia no se atribuye al número de módulos.»
- Fuente: `results/fase1_tres_modulos/exp4_directory_formation/report.md` (fila A) y `results_formation.csv:14`, `:81`.

**Hemisferio visual**, párrafo «Más variantes, más cobertura»:
- Viejo: «(experimento 10).»
- Nuevo: «(experimento 10, Sección~\ref{sec:fase4-perspectiva}).»

## 4. Texto nuevo y fuente de cada cifra

### 4.1.1 Fase 1
Rótulo de arquitectura: tres módulos, cuatro memorias por módulo, cuantización por signo, TME mediador, directorio compartido y banco de 80 (27/27/26). Se dice que no se volvió a medir ni se compara como experimento controlado. Fuente: `results/fase1_tres_modulos/README.md`.

| Cifra | Fuente |
|---|---|
| temprana 97.5 % (78/80), 1 rechazo por token sin vector, 0 rechazos de la memoria | `fase1_tres_modulos/exp3_corrected_routing/summary.json` (`early_acc`, `rejection_breakdown`) |
| madura B1 98.75 %, cruda 53.75 %, concordancia 97.5 % | ídem (`mature_acc_b1`, `mature_acc_raw`, `fidelity`) |
| registros [78, 65, 53], 1.567 bits; máximo 1.585 | ídem (`mdir_counts_tme`, `mdir_entropy_bits`); `exp3_corrected_routing/report.md` |
| Tabla `tab:fase1-formacion` (k = 1, 3, 13, 27, 40, 47, 67, 80; intercalado y bloqueado) | `exp4_directory_formation/results_formation.csv`, filas `A_interleaved` y `C_blocked` |
| 26.25 % y 72.5 % con k = 1; 3 tokens de apple | csv línea 2 |
| 1.561 bits en k = 3 | csv línea 4 |
| cruza 90 % en k = 13 (91.25 %, 8.75 %); baja a 88.75 % en k = 40; sostenido desde 47; final 98.75 % y 1.25 % | csv líneas 14, 41, 48, 81; `report.md` (A: 13 / 47) |
| barajado: primer k 15–24, sostenido 24–44 | `exp4_directory_formation/report.md` (filas B s0–s4) |
| bloqueado: [77, 0, 0], entropía 0 de k = 1 a 27; 33.75 %; 1.25 % de rechazo desde k = 20; 63.75 % en k = 40; 92.5 % en k = 67 | csv (C_blocked) k = 20, 27, 40, 67; `report.md` (C: 67) |
| A, B y C terminan en [78, 65, 53] y 1.567 | `report.md` |
| control crudo: 93.75 %, [84, 67, 45], temprana acumulada 72.15 % | `report.md` (fila D); csv `D_raw` k = 80 |
| Alcance: dentro de muestra, techo de la temprana, necesita B1 | `fase1_tres_modulos/README.md` (exp4); `inventario_fase1_tres_modulos.md` §3 |

### 4.1.2 Fase 2 (párrafo de apertura)
| Cifra | Fuente |
|---|---|
| A 53.75 %, B1 98.75 %, B2 75.0 %, F 80.0 %; C, D, E32 y E64 entre 52.8 y 53.75 % (N = 80, 5 semillas) | `fase1_tres_modulos/ablation_mdir_bias/ablation_report.md`, tabla de resultados |
| victorias en A: apple 78.75 %, horse 17.5 %, car 2.5 % | ídem, resumen ejecutivo y P1 |

### Principio de tamaño contra B1 (exp22)
| Cifra | Fuente |
|---|---|
| B1 = oficial en 656/656 y 411/411 | `results/experimento22/resumen.txt` |
| imagen: B1 96.2 / 3.5 / 0.3; tamaño 96.3 / 3.5 / 0.2; 1 decisión distinta (horse, a favor del tamaño) | ídem, bloque [imagen] y «por clase» (horse 79 → 80) |
| texto: 28.7 contra 28.5; 8 distintas (3 tamaño, 4 B1) | ídem, bloque [texto] |
| directorios de texto con 16 consultas; 59.4 % de rechazo | `experimento22/README.md` y `resumen.txt` |
| predicción fijada antes de correr; no probado con directorios de texto bien formados | `experimento22/README.md` |

### 4.1.3 Fase 3 (párrafo de apertura)
Sin cifras. Dice qué cambió a la vez entre fases y remite a exp11 y exp12 como evidencia controlada (regla 3 del brief).

### Una EHAM de dos clases contra una de ocho (exp12)
| Cifra | Fuente |
|---|---|
| 28 pares, N = 200, 5 semillas, 3 sorteos, 40 a 46 consultas por par | `results/experimento12/README.md`, cabecera y tabla |
| brecha media M2 2.54, M8 5.66 | promedio de `brecha_M2` y `brecha_M8` en `experimento12/resumen.json` (2.543 y 5.672) |
| M8 peor que M2 en 26 de 28; excepciones car–dog y car–horse | ídem, por par |
| clase M2 100 % en 25 pares; apple–tomato 93.9, cow–horse 97.6, apple–pear 99.0, con 2 etiquetas compartidas | `README.md`, columnas «clase M2» y «etiq. compartidas» |
| ρ brecha–solapamiento de etiquetas 0.01 (p 0.95); latente 0.21 (p 0.29); error de clase 0.49 (p 0.008) | `README.md`, tabla de estadísticos; `resumen.json` |
| solapamiento 0.57 a 0.65 | `README.md`, columna «solap. etiquetas» |

### 4.1.4 Fase 4
Párrafo de apertura sin cifras: remite a lo que ya está en las fases 2 y 3 y avisa del protocolo anterior.

**exp7** (`results/experimento7/README.md`)
- 364 rasgos, texto en 32 niveles, maestro de registro = verdad, texto dentro de muestra: líneas 4, 7.
- 96.2 % texto unificado y separado; 81.9 % imagen: líneas 14-18.
- diferencia máxima 0 en 236 tokens: línea 32.
- emparejada 23.8 % contra 100.0 %: líneas 26-27.
- denominador de B1: 96.2 → 91.2 → 88.8 %; con la relación, 96.2 %: líneas 39-43.

**exp8** (`results/experimento8/README.md`)
- Protocolo anterior (todos registran todo, 981 registros visuales sin variantes): líneas 5, 20.
- 80/80, 80/80, 112/112: líneas 16-18.
- 2.9 a 5.5 veces; siete de ocho sobre el radio: línea 43.
- identidades imposibles 0/10, 9 a 63 coordenadas vacías: líneas 85-93.
- masa 7:1 y 63 % contra 100 %: líneas 56-61, 76-81.
- 1 transmisión → 59 %, 8 → 100 %, precisión 1.00: líneas 97-106.
- 3.3 → 18.5 → 20.5, 80/80 en 11 tamaños y 20 semillas: líneas 112-126.
- 4-8 para reconstruir, 64-128 para enrutar; 10.4, 62.1 y 81.9 %: líneas 135-147.

**exp10** (`results/experimento10/README.md`; tabla `tab:fase4-perspectiva`)
- Diseño, maestro = verdad, ξ = 0 (con ξ = 2 el propio baja): líneas 7-14.
- Imagen directo y encadenado: líneas 23-31. Saltos 3.56 y 1.89; divergencia 0.83: líneas 24, 29.
- Texto reservadas, directo y encadenado (27.4/79.3, 43.4/80.9, 82.2/89.4, 36.6/73.9; error 20.7): líneas 40-45.
- Agregado: 85.0, 91.0, 91.9, 94.3, 56.4 en texto y 73.8, 81.9, 51.2 en imagen: líneas 53-59.
- 94.3 = cuatro consultas en una semilla: línea 63. Pizarrón 81.9 y 93.6: líneas 23, 39.

**exp9** (`results/experimento9/README.md`), con la salvedad del protocolo anterior (decisión 4 del autor)
- Protocolo: líneas 7-13; 52 registros de 16 consultas: línea 27.
- 229 (55.7 %) y 65 (81.3 %): líneas 23-25.
- sustitución 24.5 %, 0 % de clase; descripción 100 % y 19.3 contra 21.9: líneas 33-35, 52.
- imagen → texto: 89.2 %, 0 %, 100 %: líneas 60-62.
- reconocimiento 98.3 %, 16.1 %, 55.7 %: líneas 72-74.
- Formación perspectival: `experimento9/formacion_texto/curva.json`, claves «16 transactivo» (100), «60 transactivo» (302), «120 transactivo» (332), «240 transactivo» (368) y «240 pizarrón» (393), columna `al_perdido` sobre «todas». El significado de las claves sale de `run_experiment9_member_loss.py` (`form_text_directories`, `text_routing_counts`, `transactive_without`).
- N240: descripción responde 1.0 con clase 1.0 y d 18.8; vivido d 27.6; sustitución responde 0.352 con clase 0.0: `formacion_texto/N240/resumen.json`.

**exp17** (`results/experimento17/README.md`, `parte_a_resumen.txt`)
- 116 enrutadas, 96.0 %, 48.0 %, 38.9 %, margen 0.025, apple 0/45: README líneas 15-25; `parte_a_resumen.txt`.
- palabra por objeto 40.8 % (azar 10) y 51.2 %: líneas 31-37.
- sonda de color 41.1 contra 47.0 (azar 12.5): líneas 41-48.
- color, conocidos: normalizado 74.4, base 55.5: líneas 58-63. Nuevos: soporte 57.8, base 49.5: líneas 69-73.
- apple4 y horse5, 41/41: línea 77.

**exp18** (`results/experimento18/README.md`)
- lecturas de conjunto cerrado: línea 14.
- conocidos, normalizado balanceado 62.7–72.3: líneas 18-22.
- nuevos, mayoritario 98–99 %, minoritario 1–6 %: líneas 30-36. cow 8 %: línea 38.
- sonda en el azar: líneas 44-55. ResNet18-IN cow 91.2: línea 71.
- memoria 59.0 / 65.9 contra kNN 91.2 / 84.1: líneas 86-89.
- tolerante r = 1: reconoce 63 → 90 % (apple); +8.5 apple, +4.7 dog, −0.8 cow: líneas 104-107.

**exp19** (`results/experimento19/README.md`)
- copia anterior a una hetero: línea 3 (`MAE-TMS-exp18`); igualdad en imagen: `sec:una-memoria`.
- 96.2 → 80.5; 2 → 83: líneas 15-17. 89.2 → 60.8; 14.4 %: líneas 22-23. Entre animales: línea 25.
- atributo: 44.8, 53.2, azar 47.6; apple 75.6, dog 66.8 (r = 1); conocidos 63.1–100: tabla de «El especialista gana poco» y párrafo siguiente.
- tensión índice-especialista y dos percepciones no medidas: «Lectura».

### 4.1.5 Fase 5 (`results/mundo_real/`)
| Cifra o hecho | Fuente |
|---|---|
| v5, ocho módulos, tres memorias de contenido; sin corrida con la arquitectura final | `mundo_real/README.md` |
| una sola medición, 16-18 jul 2026; sin log, JSON ni WAV | ídem |
| RTX 2050 para Whisper; codificador en CPU | `smtex_05_resultados.tex`, título de la tabla de latencias |
| WAV «Farm animal that gives milk» → cow; 336 ms + 302 ms ≈ 0.6 s | `realtime_lab_README.md:113`; `smtex_05_resultados.tex:19-21`, `:41-46` |
| redirección apple → cow, 56 ms | `smtex_05_resultados.tex:46-47` |
| evocación ~2 s, asíncrona | `realtime_lab_README.md:114`; `smtex_05_resultados.tex:26-27`, `:50-52` |
| 54 ms por cuadro, 26 fps | `realtime_lab_README.md:115`; `smtex_05_resultados.tex:23-24` |
| cuadro gris con candado (cámara bloqueada por el sistema operativo) rechazado, «nadie la reconoce» | `mundo_real/selftest_frame.png`; `realtime_lab_README.md` (párrafo del «placeholder gris con candado») |
| teléfono falló; hoja impresa, solo cow fiable | `realtime_lab_README.md` («Prueba física con la cámara», «Color»); `smtex_05_resultados.tex:80-86` |
| política de reintento con normalización de momentos | `realtime_lab_README.md` («Color: reintentar con lentes») |
| 22/24 (reintento en 1/24), 18/24, 15/24 frente a ~0 | `realtime_lab_README.md:174-175`; `smtex_05_resultados.tex:102-104` |
| sin WER ni aciertos con voz; frase no hablada en vivo | `mundo_real/README.md` |

No se cita el «75.0 % de enrutamiento visual» del README del laboratorio, que `mundo_real/README.md` marca como obsoleto.

## 5. Erratas del índice

- **`computational_cost/report.md:36` («984 imágenes»).** La tabla `tab:costo` ya cita `results/computational_cost/nov2026_cpu/` con 2624 imágenes. No se tocó.
- **exp11.** El texto ya cita solo `experimento11_protocolo_corregido`. Sin cambio.
- **exp12.** Se cita `experimento12/README.md` (ρ 0.01, p 0.95). No se cita `veredicto.md` (ρ 0.45), que es anterior, ni la frase «la ventaja crece con el solapamiento».
- **exp19.** Se cita 80.5 % de `experimento19/README.md:15`. El 79.6 de `sintesis_26oct` no está versionado en `results/` y no entra.
- **exp9.** «90 de 411 con 16 interacciones» no se cita. Según `formacion_texto/curva.json`, 90 es la cifra sin formación («0 transactivo») y con 16 interacciones son 100. El texto da 100, 302, 332 y 368.
- **«Fallas pequeñas 28→59 %».** No aparece en 05.

## 6. Lo que no pude sostener o dejé fuera

- **El cuadro real de la fase 5.** El inventario describe `selftest_frame.png` como un cuadro de webcam con ropa y una habitación, rechazado con «REJECTED (closest: apple 0.00)», y cita una versión del 25 ago (`f75dde3`). La copia en `results/mundo_real/` es la de `d4740da` y muestra otra cosa: el cuadro gris con candado que entrega la cámara bloqueada, con «RECHAZO (nadie la reconoce)». Reporté lo que hay en `results/`.
- **Tras la corrección de color no se repitió la prueba física.** No está escrito así en las fuentes. Puse «No hay registro de una prueba física posterior a la corrección de color».
- **Tema 3 y tema 6 del inventario de hallazgos.** No tienen hallazgos nuevos de ETH-80 con 8 módulos fuera de los que ya están en la fase 3. exp13, exp14, exp15, exp16, el codificador por pliegue, `homo_marginal`, la sonda de rechazo y las líneas base siguen donde estaban; la fase 4 remite a ellos.
- **MedMNIST+ y VisA** (exp20, 21, 23-29, piloto, industrial monolítico): fuera, según la decisión 1 del autor.
- **Citas.** Los vínculos naturales (Nelson y Narens para exp8, Russell para exp9, Vygotsky y Hutchins para exp10, Tenenbaum y Griffiths para exp22) no están en `referencias.bib`. Resultados no cita a ninguno; le tocan a la Discusión.
- **No se agregaron figuras**, porque los PNG de `results/fase1_tres_modulos/` y `results/experimento*/` no están en `.tex8/figuras/` y la tarea no permite tocar otros archivos. Si se quiere la curva de formación de la fase 1 como figura, hay que copiar `exp4_directory_formation/fig1_formation_curve.png` a `.tex8/figuras/`.

## 7. Revisión de estilo

- «módulo» siempre; 0 apariciones de «agente».
- `\,\%` en todas las cifras nuevas y comillas angulares.
- Se buscaron «cabe destacar», «es importante», «claramente», «notablemente», «crucial», «robusto», «sin duda», «en este sentido» y «sino»: 0 en 05.
- Se revisaron los comienzos repetidos consecutivos del texto nuevo y se cambiaron los que se seguían dentro del mismo párrafo.
- El nombre del asistente no aparece en el parche.
