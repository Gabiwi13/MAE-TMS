# Revisión por fases: Sección 4.2, Discusiones

Base: `59cca47` (rama `una-hetero`). Archivos tocados: `.tex8/secciones/06_discusion.tex` y su parte regenerada en `.tex_uacj/Capitulo4.tex` (desde `\section{Discusiones}`). `05_resultados.tex` y `referencias.bib` no se tocaron.

## 1. Estructura vieja y nueva

| Viejo (06) | Nuevo (06) | Qué pasó |
|---|---|---|
| — | 4.2.1 Creencias iniciales y lo que se encontró (`sec:creencias`) | Nueva: tres tablas (`fase:tab-creencias-formacion`, `fase:tab-creencias-imagen`, `fase:tab-creencias-directorio`) con 18 creencias y tres párrafos. |
| — | 4.2.2 El directorio como índice y como metamemoria (`fase:disc-metamemoria`) | Nueva: exp7, exp8, exp15 y líneas base. Recibe el ítem de Wegner «El directorio está separado del contenido» (Sparrow, Teyler y DiScenna, Damasio, el límite del mediador). |
| Lectura desde la teoría de memoria transactiva de Wegner (`sec:disc-wegner`) | 4.2.3 La perspectiva y la pérdida de un miembro: lectura desde Wegner (`sec:disc-wegner`) | Se conservan la salvedad del directorio compartido y los ítems «Conocerse cuesta interacción» y «El orden de las experiencias». Se agregan exp10 (directorios perspectivales) y exp9 (pérdida de un miembro). La salvedad «analogías estructurales» pasa al inicio de 4.2.2. |
| Una memoria por módulo: familiaridad, nombre y daño (`sec:disc-una-memoria`) | 4.2.4 Reconocer y recordar: envolvente, contención y familiaridad (`fase:disc-reconocer`, `sec:disc-una-memoria`) | Texto íntegro, más un párrafo inicial con exp13, exp14, exp16 y el codificador por pliegue. Se quita la frase «Como en la sección anterior, las analogías…», porque la salvedad ya está en 4.2.2. |
| La normalización necesaria es B1 (`sec:disc-b1`) y El sesgo hacia un módulo (`sec:disc-dominancia`) | 4.2.5 Tamaño, lectura del directorio y partición (`fase:disc-tamano`, `sec:disc-b1`, `sec:disc-dominancia`) | Los dos textos íntegros como párrafos, más el matiz de exp22, el ítem de Wegner «Las pistas compartidas degradan el enrutamiento» y exp12. |
| — | 4.2.6 Imagen y palabra (`fase:disc-imagen-palabra`) | Nueva: exp17, exp18 y exp19. |
| El mecanismo transactivo funciona con ocho dominios (`sec:disc-escala`) | 4.2.7 Límites: lo que pone la representación y lo que pone el mecanismo (`fase:disc-limites`, `sec:disc-escala`) | Texto íntegro, más el ítem de Wegner «El rechazo se sostiene con ocho dominios», la sonda de rechazo (10 de 12) y un párrafo sobre la fase 5. |
| Qué aporta la partición frente a una EHAM única (sin etiqueta) y Qué agrega la memoria asociativa frente a decisores simples (`sec:disc-lineas-base`) | 4.2.8 Qué aporta la partición y qué agrega la memoria frente a decisores simples (`sec:disc-lineas-base`) | Los dos textos íntegros en una subsección, con títulos de párrafo nuevos para la parte de la EHAM única. |
| Limitaciones (a) a (l) (`sec:limitaciones`) | 4.2.9 Limitaciones (a) a (o) | (a) a (l) sin cambios de letra ni de texto. Nuevas: (m) comparabilidad entre fases, (n) fase 5 sin cifras ni salida cruda, (o) experimentos con el protocolo anterior (exp9, y 7, 8 y 10). |

Varias etiquetas viejas apuntan ahora a la misma subsección nueva (`sec:disc-b1` y `sec:disc-dominancia` a 4.2.5; `sec:disc-una-memoria` a 4.2.4; `sec:disc-escala` a 4.2.7). Las remisiones de otros capítulos siguen resolviendo y su sentido se conserva: 05 remite a `sec:disc-dominancia` para el origen del sesgo y a `sec:disc-b1` para la normalización; 07 y el Apéndice A remiten a `sec:disc-wegner` para los directorios perspectivales y el criterio de madurez, que siguen en 4.2.3.

## 2. Prosa nueva

Lo nuevo está en el parche. Los bloques que se escribieron desde cero son:
- 4.2.1 completo (tablas y tres párrafos);
- 4.2.2, párrafos 1, 2 y 4, y las frases sobre Teyler y Hart del párrafo 3;
- 4.2.3, párrafos «Directorios perspectivales» y «La pérdida de un miembro»;
- 4.2.4, párrafo 1;
- 4.2.5, el párrafo de exp22 y «Partir el contenido y el número de dominios»;
- 4.2.6 completo;
- 4.2.7, la frase sobre la generalización del atributo, la sonda de rechazo y el párrafo de la fase 5;
- 4.2.9, limitaciones (m), (n) y (o).

## 3. Fuente de cada cifra nueva

| Cifra | Dónde | Fuente |
|---|---|---|
| +3.0 puntos con 400; +0.2 con 200, +1.3 con 291; 92.5 % | Tabla, creencia 1 | Ya en 06 (`sec:calibracion`, `sec:calibracion-fija`) |
| Coincidencia 97.5 % (fase 1, banco de 80) | Creencia 2 | `results/fase1_tres_modulos/experimento1/informe.md:22` |
| El 100 % contaba rechazos como coincidencia | Creencia 2 | Mensaje del commit `3f665ab` (`plan_reestructura/inventario_fase1_tres_modulos.md:59`). Sin cifra en el texto. |
| κ de 81.2 a 0.0 %; ι = 0.25 de 81.2 a 82.5 % | Creencia 3 | `05_resultados.tex`, `sec:param-iota-kappa`; `results/exp2_iota_kappa/report.md:17-20` |
| apple 78.75 %; B1 de 53.75 a 98.75 % (fase 1) | Creencia 4 | `results/fase1_tres_modulos/ablation_mdir_bias/ablation_report.md:75-80` |
| 20.5 %, 13.8 %, 9 de 28 | Creencia 4 | Ya en 06 (`sec:disc-dominancia`) |
| 90.0 % sobre 411 | Creencia 5 | Ya en 06 (`sec:disc-escala`) |
| 81.9 contra 81.9 %; 91.0 contra 93.6 % con 1/32; 83 % de celdas; 3.56 saltos; 20.7 % de error con 1/64; 94.3 % con 1/4 (cuatro consultas, una semilla); anillo 56.4 y 73.9 % | Creencia 6 y 4.2.3 | `results/experimento10/README.md:24, 33, 40, 54, 57, 59, 63` |
| 73.6→96.2, 76→96, 66.5→94.5 | Creencia 7 | Ya en 06 (limitación (b)) |
| 631 de 656 (96.2 %) | Creencia 8 | `results/hemisferio_visual` (ya en 06); la cifra retirada no se cita (`results/auditoria_integral/report.md:45`) |
| 5 de 656; 1 → 3 especialistas; 137 de 152; 136 en 3280 | Creencia 9 | Ya en 06 (limitaciones (b), (c), (f)) |
| 96.2→70.4; 2→169; 23 imágenes; 1 % de daño | Creencia 11 | Ya en 06 |
| 336 ms, 302 ms, ≈0.6 s, 54 ms por cuadro | Creencia 12 y (n) | `results/mundo_real/smtex_05_resultados.tex:19-23`; `results/mundo_real/realtime_lab_README.md:113, 115` |
| Imagen evocada unos 2 s después | Creencia 12 | `results/mundo_real/smtex_05_resultados.tex:49` |
| 22, 18 y 15 de 24 | 4.2.7 | `results/mundo_real/smtex_05_resultados.tex:102-104` |
| Pantalla de teléfono no viable; papel mate sí; corrimiento de color | 4.2.7 | `results/mundo_real/smtex_05_resultados.tex:80-88` |
| 96.2 % unificado y separado; puntuaciones idénticas; 96.2→91.2→88.8; 23.8 contra 100.0 %; 32 niveles, dentro de muestra | Creencia 13 y 4.2.2 | `results/experimento7/README.md:7, 14, 17, 26-27, 32, 41-43` |
| 80/80, 112/112; 2.9 a 5.5 veces; 0 de 10 por identidad imposible; 59 % y 100 %; precisión 1.00; 3.3 → 20.5; 981 registros | Creencia 13 y 4.2.2 | `results/experimento8/README.md:5, 16-18, 20, 43, 87-91, 99-106, 114, 124` |
| Prototipo 7.0 a 9.0; ST y SS 0.0 a 1.2 (v5) | Creencia 14 | `results/mundo_real/smtex_05_resultados.tex:142-145` |
| 229 de 411 (55.7 %); 65 de 80; 24.5 %; 0 % imagen→texto; 19.3 contra 21.9; 98.3 % y 16.1 %; 16 consultas | Creencia 15 y 4.2.3 | `results/experimento9/README.md:23, 27, 33-35, 59-61, 72-74` |
| −0.1 a −0.7 puntos; 25 gana la EHAM | Creencia 16 | Ya en 06 (partición) |
| 96.8 → 93.6 % | Creencia 17 | Ya en 06 (limitación (a)); `results/experimento15/README.md:11-12` |
| 81.2, 79.4, 81.5 %; 652-655 contra 631 | Creencia 18 | Ya en 06 (`sec:disc-lineas-base`) |
| exp22: 96.3 contra 96.2 %, 1 decisión de 656; 28.5 contra 28.7 %, 8 de 411; 59.4 % de rechazo | 4.2.5 | `results/experimento22/resumen.txt:4-15`; `results/experimento22/README.md:7-10` |
| exp12: ρ 0.01 (p 0.95); ρ 0.49 (p 0.008); medias 2.54 y 5.66; 26 de 28 | 4.2.5 | `results/experimento12/README.md:9-17` y la tabla por par (medias y conteo recalculados de esa tabla: 2.543, 5.664, 26) |
| exp14: 15 a 19; mediana 5.8; corrida con 4 variantes | 4.2.4 | `results/experimento14/veredicto.md:3, 16` |
| exp16 95.5 → 89.2; 87.6 %; 136 en 3280 | 4.2.4 | Ya en 06 (limitación (f)) |
| exp17: 96.0 %, 48.0 %, 38.9 %; 40.8 % (azar 10), 51.2 %; 74.4 contra 55.5; 57.8 contra 49.5; manzana verde → roja | 4.2.6 | `results/experimento17/parte_a_resumen.txt:6, 8, 25`; `results/experimento17/README.md:33, 61, 63, 71, 73, 77` |
| exp18: 62.7 a 72.3 %; 98-99 % y 1-6 %; vacas 8 %; sonda en el azar; 59 contra 91 | 4.2.6 | `results/experimento18/README.md:20-22, 30-38, 46-55, 94` |
| exp19: 96.2 → 80.5 %; 2 → 83; 89.2 → 60.8 %; unos 5 puntos | 4.2.6 | `results/experimento19/README.md:15-23, 46-48`. Se cita 80.5, que es lo que trae la carpeta y lo que usa 05; el 79.6 de `sintesis_26oct` no tiene fuente en `results/`. |
| Sonda de rechazo: 10 de 12; las 2 que pasan comparten tokens con el vocabulario | 4.2.7 | `results/rejection_probe/report.md:26-27, 32`; ya en 06 como «deja pasar 2 de 12» |
| Fase 1: 90 % tras 13 interacciones, final 98.8 % | (m) | `results/fase1_tres_modulos/exp4_directory_formation/report.md:12` |
| 8 módulos: ninguna llega al 90 %, final 81.2 % | (m) | `05_resultados.tex`, `sec:formacion` |

## 4. Lo que no entró y por qué

- **Creencia 19 del inventario (resumen de CIFIN, «fallas pequeñas 28→59 %»):** sin soporte y del caso industrial, fuera del reporte.
- **Cifras retiradas:** el 47.1 % de enrutamiento visual (creencia 6 del inventario) y el 5/10 del experimento 1 original no aparecen; la creencia se formula sin ellas.
- **Partes médicas e industriales** de las creencias y de los temas (exp20, exp21, exp23 a exp29, piloto de módulos, industrial monolítico, demo médico): fuera, por la decisión del autor. La parte médica de la creencia 14 del inventario (exp25) se quitó.
- **exp9, curva de formación perspectival (`formacion_texto/curva.json`):** no se usa, por la discrepancia del «90 de 411» que señala el índice.
- **exp15** se corrió con la arquitectura anterior; solo se cita como ya lo hacía 06 (limitación (a)).

## 5. Citas que no se pudieron verificar

La política de red de esta sesión rechaza `doi.org`, `api.crossref.org`, `sciencedirect.com` y `academic.oup.com` (respuesta 403 del proxy), así que ninguna cita nueva se verificó contra la fuente primaria y **no se agregó nada a `referencias.bib`**. Por eso no se usan:
- Nelson y Narens (1990), metamemoria (exp8). La lectura de metamemoria se apoya en Hart 1965 y Sparrow 2011, que ya están en el `.bib`.
- Russell (1911), familiaridad y descripción (exp9). El texto lo dice en los términos del sistema («esto es mío», «esto era de él») sin atribuirlo.
- Tenenbaum y Griffiths (2001), principio de tamaño (exp22). Se describe la regla y se nombra como la llama el experimento 22, sin cita.
- Hutchins (1995) y Vygotsky (1978), pizarrón e internalización (exp10). Sin nombrarlos.
- Yonelinas (2002), dos procesos del reconocimiento (exp17), y McClelland, McNaughton y O'Reilly (1995), sistemas complementarios (exp19). Sin nombrarlos.

Con red, los DOI a revisar son `10.1016/S0079-7421(08)60053-5`, `10.1093/aristotelian/11.1.108`, `10.1017/S0140525X01000061`, `10.7551/mitpress/1881.001.0001`, `10.1006/jmla.2002.2864` y `10.1037/0033-295X.102.3.419`.

## 6. Etiquetas

- Nuevas: `sec:creencias`, `fase:tab-creencias-formacion`, `fase:tab-creencias-imagen`, `fase:tab-creencias-directorio`, `fase:disc-metamemoria`, `fase:disc-reconocer`, `fase:disc-tamano`, `fase:disc-imagen-palabra`, `fase:disc-limites`.
- Eliminadas: ninguna. Las limitaciones (a) a (l) conservan su letra; las nuevas son (m), (n) y (o).
