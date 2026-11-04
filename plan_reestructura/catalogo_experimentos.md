# Catalogo de experimentos (results/ de MAE-TMS-una-hetero)

Solo lectura. Fecha = primer commit que agrega la carpeta (git log --diff-filter=A); no es la fecha de corrida: varias carpetas entraron juntas en lote (10-18 y 11-02) y algunas contienen corridas posteriores (por ejemplo computational_cost con nov2026_cpu). Fase: 1 prototipo de 3 modulos, 2 escalado a 8 modulos (ETH-80, e incluye las extensiones a otros datos y flotas, marcadas en la columna de datos), 3 mundo real, auxiliar. Apendice A = nombre de la carpeta en ApendiceA.tex. Citado = nombre de la carpeta o la expresion experimento N en otro .tex de .tex_uacj (Capitulo*, Difusion, etc.). La coincidencia es textual; no verifica que se use la cifra.

| Fecha | Carpeta | Modulos / dataset | Que mide | Fase | Estado | Apendice A | Citado en |
|---|---|---|---|---|---|---|---|
| 2026-06-07 | ablation_mdir_bias | 8 clases, ETH-80 (numeros 8 clases; narrativa P1-P7 historica de 3 clases) | Sesgo de densidad de M_dir y condiciones A-G (normalizacion B1, etc.); mejor condicion G 85.3 a 93.5 % maduro, evaluada dentro de muestra | 2 | vigente (numeros); narrativa P1-P7 historica. Evaluacion dentro de muestra, ver calibracion_evaluacion_fija | si | no |
| 2026-06-12 | exp2_iota_kappa | 8 clases, ETH-80 | Si la poda iota y el umbral kappa nativos sustituyen la normalizacion B1 contra el sesgo de masa (rejilla iota x kappa) | 2 | vigente (dentro de muestra) | si | no |
| 2026-06-12 | exp3_corrected_routing | 8 clases, ETH-80 | Protocolo completo con ruteo corregido: temprana 81.2 %, madura B1 81.2 %, fidelidad 92.5 %, 80 consultas | 2 | vigente; re-corrida de 8 clases que reemplaza las cifras de 3 clases de experimento1 | si | no |
| 2026-06-12 | exp4_directory_formation | 8 clases, ETH-80 | Curva de formacion del directorio por orden de experiencias; ninguna condicion cruza 90 % (todas terminan en 81.2 %) | 2 | vigente, resultado negativo (sin transicion); dentro de muestra | si | no |
| 2026-06-12 | exp5_entropic_prototype | 8 clases, ETH-80 | Prototipo emergente: llenado por delta (promedio) contra instancias; variedad de recuerdo 1 contra 12 | 2 | vigente | no | no |
| 2026-06-12 | exp6_capacity | 8 clases, ETH-80 | Curva de capacidad del llenado por instancias (N=25 a 328): test propio 0 a 56 %, falsos 0 % | 2 | vigente | si | no |
| 2026-06-12 | experimento1 | 3 clases (apple/horse/car), ETH-80, v3 | Primera caracterizacion del sistema: temprana 97.5 %, madura B1 98.75 %, directorio TME con entropia 1.567 bits | 1 | reemplazado: cifras historicas v3 de 3 clases; la re-corrida de 8 clases esta en exp3_corrected_routing. Unica carpeta de 3 modulos | no | no |
| 2026-06-22 | computational_cost | Pipeline completo; CPU y laptops | Costo de reproducir todo el experimento: pipeline 133.5 min, total 293.4 min; subcarpetas por maquina y nov2026_cpu | auxiliar | vigente (nov2026_cpu es la vigente; en la corrida ablation figura fallida) | si | Capitulo4 |
| 2026-06-22 | rejection_probe | 8 dominios, ETH-80 | Micro-test: 12 consultas fuera de dominio; la EAM rechaza 10 de 12, 2 falsos routings | 2 | vigente; el .md de 3 clases (22 jun) quedo obsoleto y fue reescrito el 2 ago | si | no |
| 2026-08-02 | auditoria_integral | Repositorio (rama v5-multimodal) | Auditoria de sanidad y fidelidad en 5 frentes; 0 CRITICAL de codigo, 2 documentales | auxiliar | vigente como auditoria de 2 ago; el codigo auditado es anterior al sistema actual | no | no |
| 2026-08-02 | missing_cue | 4 pistas, ETH-80 | Caracterizacion distribucional de la pista faltante (RS/ST/SS), 30 corridas por metodo | 2 | vigente; hay una copia distinta en controles_uniformes/missing_cue | no | no |
| 2026-08-31 | experimento7 | 8 agentes, ETH-80 texto+imagen | Directorio unificado texto+imagen en una sola DirectoryMemory (364 features, mitad ausente como nan) | 2 | vigente (texto dentro de muestra) | no | no |
| 2026-09-09 | experimento8 | 8 agentes, ETH-80 | Recuperacion desde el directorio: lectura inversa agente a pista y fraccion presenciada | 2 | vigente | no | no |
| 2026-09-14 | experimento10 | 8 agentes, ETH-80 | Directorios perspectivales (fraccion f y anillo r) y ruteo encadenado contra pizarron, Vygotsky contra Hutchins | 2 | vigente; v1_sin_agregado es la version previa, ampliada con el protocolo agregado | si | Capitulo4 |
| 2026-09-14 | experimento9 | 8 agentes, ETH-80 | Perdida de un miembro: rechazo, sustitucion y descripcion; familiaridad contra descripcion (Russell, Wegner) | 2 | vigente (la cifra de 98.5 % de una corrida sin semilla fue corregida en el README) | no | no |
| 2026-09-21 | experimento11 | 8 clases, ETH-80, 10 semillas | MAE monolitica contra sistema transactivo (clase 1-NN, centroide, clasificador) con N=25 a 200 | 2 | corregido: T-protocolo reeditado en experimento11_protocolo_corregido (directorios acumulados entre trabajos del Pool) | si | Capitulo4 |
| 2026-09-21 | experimento12 | 28 pares de clases, ETH-80 | Ventaja de partir contra el solapamiento entre dominios; brecha contra solapamiento, rho 0.01 p 0.95 | 2 | corregido: veredicto.md conserva la lectura vieja (rho 0.45, p 0.017, 4 variantes) que se pierde con 16 variantes; ver controles_uniformes/experimento12 | no | no |
| 2026-09-23 | experimento13 | 8 clases, ETH-80 | Augmentacion del llenado visual (V variantes): cobertura y falsos contra V | 2 | vigente | si | Capitulo4 |
| 2026-09-23 | experimento14 | 8 clases, ETH-80 | Criterio de energia minima del latente y su costo en imagenes reales (rechaza 0 a 5 de 656) | 2 | vigente | si | Capitulo3, Capitulo4 |
| 2026-09-23 | experimento15 | 8 clases, texto e imagen, ETH-80 | Arbitro por contenido y abstencion por margen contra argmax (texto 96.8 % argmax) | 2 | vigente | si | Capitulo4 |
| 2026-09-24 | experimento16 | 8 clases, 10 pliegues, ETH-80 | Leave-one-object-out: e2e 95.5 % objeto conocido contra 89.2 % nuevo, el fallo es rechazo | 2 | vigente; ampliado por objetos_nuevos_codificador_por_pliegue | si | Capitulo4 |
| 2026-10-17 | experimento17 | 8 clases, ETH-80 | De la imagen a una palabra especifica: dominio 96.0 %, nombre de clase 48.0 %, color en objetos nuevos 57.8 % (base 49.5) | 2 | vigente | no | no |
| 2026-10-17 | experimento18 | 8 clases (cow, horse, dog, cup, car), ETH-80 | Heteroasociacion con caracteristicas visibles (patron, techo, pelo), tambien en objetos nuevos | 2 | vigente | no | no |
| 2026-10-18 | enrutador_flota | Flota de detectores, VisA (12 piezas) | Enrutador de una flota de detectores PatchCore: la MAE contra kNN y abstencion ante pieza desconocida | 2 | vigente (aplicacion, otros datos) | no | no |
| 2026-10-18 | experimento19 | 8 clases, ETH-80 con otros codificadores | Sistema completo con una percepcion que conserva detalle (sin perdida de clase; ImageNet+PCA 80.5 % de ruteo) | 2 | vigente; ampliado por codificador_sin_clase | si | Capitulo4 |
| 2026-10-18 | experimento20 | Modulos medicos, MedMNIST+ (BloodMNIST, OCTMNIST fuera de dominio) | Principio de tamano para leer el directorio y rechazo de lo ajeno | 2 | vigente (otros datos) | no | no |
| 2026-10-18 | experimento21 | Niveles de MedMNIST+ | Memoria unica contra particion (M, T-especialistas, T-protocolo) sobre MedMNIST+ | 2 | vigente (otros datos) | no | no |
| 2026-10-18 | experimento23 | MedMNIST+ (organos 11, torax 14, piel 7, mama 2) | La ambiguedad como respuesta: conjuntos S desconocido, claro, ambiguo, contra kNN y clasificador | 2 | vigente (otros datos) | no | no |
| 2026-10-18 | experimento24 | MedMNIST+ | Pruebas duras contra rivales actuales: conformal Mondrian, incrementales, Hopfield moderno, HDC, OOD | 2 | vigente (otros datos) | no | no |
| 2026-10-18 | industrial | 12 piezas, VisA | Demo industrial: ruteo por pieza 98.4 %; deteccion de fallas por rechazo no funciona con vectores globales (deja pasar 94 %) | 2 | vigente (resultado negativo en deteccion) | no | no |
| 2026-10-18 | industrial_clip | 12 piezas, VisA + CLIP | Texto como pista con CLIP como percepcion compartida y descripciones de fallas | 2 | vigente | no | no |
| 2026-10-18 | industrial_monolitica | 12 piezas, VisA | Memoria unica contra particion (12 especialistas) en el demo industrial | 2 | vigente | no | no |
| 2026-10-18 | medico | 4 modalidades + hallazgos, MedMNIST+ 128 px | Demo medico, muestra de 200 por agente, dos niveles (modalidad y hallazgo u organo) | 2 | vigente; ampliado por medico_completo y medico_balanceado | no | no |
| 2026-10-18 | medico_balanceado | MedMNIST+ | Corrida con registro balanceado, N = max(328, clase mas chica), todos los datos de test | 2 | vigente | no | no |
| 2026-10-18 | medico_completo | MedMNIST+ (RetinaMNIST fuera de dominio, PneumoniaMNIST transferencia) | Corrida completa con todo el train (62 min) contra la muestra | 2 | vigente | no | no |
| 2026-10-18 | olvido_privacidad | MAE sobre flota VisA | Olvido exacto (restar la relacion; igual a reconstruir, 300 veces mas rapido) y privacidad del registro | auxiliar | vigente | no | no |
| 2026-10-18 | sintesis_aplicaciones | Sintesis de demos industriales y medicos | Resume para que sirve el sistema hoy; sin cifras nuevas | auxiliar | vigente (sintesis) | no | no |
| 2026-10-19 | cascada_modulos | Flota VisA (malas, buenas, revision humana) | Cascada de modulos: partir el modulo de buenas en k especialistas para que las fallas nuevas no se escondan | 2 | vigente | no | no |
| 2026-10-19 | cierre_mae | 12 piezas, VisA, WideResNet50 | Cierre: la MAE como detector con la mejor percepcion; detecta 5.8 % global, 26.8 % parches contra PatchCore 70.6 % | auxiliar | vigente (cierre negativo como detector) | no | no |
| 2026-10-19 | deriva_olvido | Flota VisA, deriva | Aprendizaje en linea con deriva: el olvido exacto permite adaptarse | 2 | vigente | no | no |
| 2026-10-19 | etapa1_ruteo_dirigido | Flota 24 modulos, VisA | Ruteo dirigido, lectura tolerante y respaldo por contenido para bajar costo y abstencion | 2 | vigente; precedido por piloto_modulos, seguido por etapa2_evidencia | no | no |
| 2026-10-19 | etapa2_evidencia | Flota 24 modulos, VisA | Acumular evidencia (Wilson) y entrada por receptor para conciliar costo y calidad | 2 | vigente | no | no |
| 2026-10-19 | parametros_mae | Deteccion de fallas, VisA | Parametros nativos iota y kappa como lectura para detectar fallas | auxiliar | vigente | no | no |
| 2026-10-19 | piloto_modulos | Flota de 24 modulos, 12 piezas VisA x 2 redes | El sistema aprende cual modulo es mejor solo de sus transacciones: 79.0 % al mejor, contra kNN 71.6 % | 2 | vigente | no | no |
| 2026-10-19 | red_sintetica | Redes sobre VisA | Fallas sinteticas y termino anti-colapso para la red de buenas contra malas | auxiliar | vigente | no | no |
| 2026-10-19 | replica_ablaciones | Flota VisA y flota medica nueva, 10 semillas | Replica y ablaciones del diseno congelado de ruteo dirigido | 2 | vigente | no | no |
| 2026-10-19 | revision_cientifica | Lineas de aplicacion (industria, medicina, flota) | Revision critica y modelo formal; registro de afirmaciones con estado y evidencia | auxiliar | vigente | no | no |
| 2026-10-28 | controles_uniformes | 28 pares, ETH-80 y 4 pistas | Controles con pesos uniformes de exp12 y copia de missing_cue | auxiliar | vigente; control de experimento12 (la correlacion se pierde por las 16 variantes) | no | no |
| 2026-10-28 | experimento22 | 8 clases, ETH-80 oficial, solo lectura | Principio de tamano sobre los modelos oficiales equivale a B1: imagen 96.3 contra 96.2 %, texto 28.5 contra 28.7 % | 2 | vigente; candidata a reemplazar la lectura B1 | no | no |
| 2026-10-29 | homo_marginal | 8 agentes, ETH-80 | Las homo como marginal de la hetero: se reemplazan por lecturas de una sola hetero (lesion, borde, emparejamiento) | 2 | vigente; reemplaza las memorias homo del diseno anterior | si | no |
| 2026-11-02 | calibracion_evaluacion_fija | 8 clases, ETH-80, 411 consultas | Calibracion con conjunto de evaluacion fijo (jurado M2): quita el sesgo dentro de muestra de run_ablation | auxiliar | vigente; corrige la evaluacion de ablation_mdir_bias | si | Capitulo4 |
| 2026-11-02 | codificador_sin_clase | 8 clases, ETH-80 | Sistema de punta a punta con codificador sin perdida de clase (CLS_WEIGHT=0) | 2 | vigente | si | Capitulo4 |
| 2026-11-02 | experimento11_protocolo_corregido | 8 clases, ETH-80 | Exp11 con directorios perspectivales sin acumular entre trabajos del Pool | 2 | vigente; reemplaza el brazo T-protocolo de experimento11 | si | Capitulo4 |
| 2026-11-02 | hemisferio_visual | 8 modulos, ETH-80 | Log de la etapa 7 (26 oct): fase A 99.9 %, fase B 631/656, evocacion 113/116 | 2 | vigente | si | no |
| 2026-11-02 | lineas_base | 8 clases, texto e imagen, ETH-80 | Lineas base ajenas a la memoria asociativa con los mismos vectores (jurado M3) | auxiliar | vigente | si | Capitulo4 |
| 2026-11-02 | reanalisis_jurado | Datos de exp11, ablation y exp14 | Reanalisis estadistico pedido por el jurado (M1, M2, M3, M5, M6) | auxiliar | vigente | si | Capitulo3, Capitulo4 |
| 2026-11-02 | rescate_lexico | 411 consultas, ETH-80 | Cuanto aporta la regla de rescate lexico de tokenize_query en la fase temprana | auxiliar | vigente | si | no |
| 2026-11-03 | objetos_nuevos_codificador_por_pliegue | 8 clases, 10 pliegues, ETH-80 | Objetos nuevos con el codificador reentrenado por pliegue (jurado M4) | 2 | vigente; amplia experimento16 | no | Capitulo4 |

## Conteos

- Carpetas en results/: 58
- Por fase: fase 1 = 1; fase 2 = 44 (de ellas 17 son extensiones a otros datos o flotas, no ETH-80); fase 3 = 0; auxiliar = 13
- En el Apendice A: 22; en el Apendice A o citadas en otro .tex: 23
- No aparecen en ningun .tex (ni apendice ni cuerpo): 35
- Corregidas, retractadas o reemplazadas (total o parcial): 3
  - experimento1: reemplazado: cifras historicas v3 de 3 clases; la re-corrida de 8 clases esta en exp3_corrected_routing. Unica carpeta de 3 modulos
  - experimento11: corregido: T-protocolo reeditado en experimento11_protocolo_corregido (directorios acumulados entre trabajos del Pool)
  - experimento12: corregido: veredicto.md conserva la lectura vieja (rho 0.45, p 0.017, 4 variantes) que se pierde con 16 variantes; ver controles_uniformes/experimento12

## Notas

- Fase 1 (3 modulos): solo experimento1 mide 3 clases, y sus cifras son historicas (v3); summary.json de exp3 ya no las contiene. ablation_mdir_bias conserva narrativa de 3 clases pero sus numeros son de 8.
- Fase 3 (mundo real, voz y vision): results/ no tiene carpeta con esos resultados. Existe el directorio realtime_lab/ (decisiones de diseno del 16 jul 2026) fuera de results/; su estado de medicion no se reviso aqui.
- Dentro de muestra: ablation_mdir_bias, exp2, exp3, exp4 y el texto de exp7 evaluan sobre las mismas consultas que forman el directorio; calibracion_evaluacion_fija lo corrige para la ablacion.
- Las demos industriales y medicas, y la flota de modulos (VisA, MedMNIST+), no son ETH-80 ni 8 modulos; se contaron en fase 2 como extension y quizas convenga una fase propia.
- Duplicados: missing_cue y controles_uniformes/missing_cue difieren; experimento12 y controles_uniformes/experimento12 difieren (el segundo usa pesos uniformes).
