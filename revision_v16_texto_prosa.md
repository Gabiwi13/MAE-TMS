# Revisión de prosa: cifras de texto tras re-correr la ablación y exp2–6 sobre los modelos con 16 variantes (23 de septiembre de 2026)

**Estado:** pendiente de aprobación. Nada aplicado. Los resultados ya están confirmados en git (`9f50751`); esta ronda solo actualiza la prosa que los cita. Viejo / nuevo por archivo.

Fuente: `results/ablation_mdir_bias/ablation_report.md` (N = 400, 5 semillas), `results/exp2_iota_kappa/results_grid.csv`, `results/exp3_corrected_routing/`, `results/exp4_directory_formation/`, `results/exp6_capacity/report.md`, `results/rejection_probe/`. El llenado de 16 variantes densifica también la hetero de contenido (3200 pares etiqueta–latente por agente en vez de 800), y eso mueve las cifras de texto; los directorios de texto de la fase temprana oficial son idénticos.

## A. `.tex8/secciones/05_resultados.tex`

**Tabla de calibración (líneas 38–46), temprana / fidelidad / madura:**

| condición | viejo | nuevo |
|---|---|---|
| A (cruda) | 88.0 / 87.3 / 80.0 | 90.0 / 92.0 / 87.0 |
| B1 | 88.0 / 93.5 / **93.2** | 90.0 / 95.2 / **93.5** |
| B2 | 88.0 / 95.0 / 89.0 | 90.0 / 95.2 / 93.2 |
| C | 88.0 / 91.5 / 86.5 | 90.0 / 92.5 / 89.5 |
| D | 88.6 / 89.6 / 82.8 | 90.5 / 92.5 / 89.0 |
| E32 | 88.0 / 91.3 / 84.8 | 90.0 / 93.5 / 90.5 |
| E64 | 88.0 / 92.0 / 86.5 | 90.0 / 93.2 / 92.2 |
| F | 88.0 / 87.3 / 80.0 | 90.0 / 92.0 / 87.0 |
| G (D+B1+F) | 88.6 / 93.6 / 92.9 | 90.5 / 95.3 / 94.0 |

**Párrafo «B1 sigue siendo la corrección irreducible» (51–57).** Viejo: «la lectura cruda del directorio (A) pierde 13 puntos frente a la lectura normalizada por conteo (80.0 % frente a 93.2 %), y ninguna condición que manipula síntomas (B2, C, D, E32, E64) la alcanza. La combinación G no supera a B1 sola (92.9 % frente a 93.2 %): una vez corregida la causa […] no aportan nada adicional.» Nuevo: «la lectura cruda del directorio (A) pierde 6.5 puntos frente a la lectura normalizada por conteo (87.0 % frente a 93.5 %; con el llenado de 4 variantes la brecha era de 13 puntos: el contenido más denso reduce el sesgo de masa pero no lo elimina), y ninguna condición que manipula síntomas (B2, C, D, E32, E64) la alcanza, aunque B2 queda a tres décimas. La combinación G supera a B1 sola por medio punto (94.0 % frente a 93.5 %), dentro del ruido de cinco semillas: una vez corregida la causa (evidencia por registro en vez de evidencia total), el balanceo de consultas y la curación de vocabulario aportan poco.»

**Párrafo «El sesgo hacia apple quedó esencialmente resuelto» (91–101).** Viejo: «la participación de apple bajo la lectura B1 baja a 13.0 % y pear se recupera a 86 % sin cambiar el vocabulario […] bajo la lectura cruda (A) apple todavía captura el 24 % de las victorias […] con B1 ningún agente se desvía más de 2.5 puntos del ideal.» Nuevo: «la participación de apple bajo la lectura B1 baja a 13.2 % sin cambiar el vocabulario; pear queda en 78 % (86 % con el llenado de 4 variantes: el contenido más denso no la ayuda) […] bajo la lectura cruda (A) apple todavía captura el 19.5 % de las victorias […] con B1 ningún agente se desvía más de 2 puntos del ideal.»

**«Estado del directorio» (113–117).** «2.955 bits en la condición A y 2.961 bits en G […] balanceada al 98.5 %» → «2.974 bits en la condición A y 2.977 en G […] balanceada al 99.1 %»; «La fidelidad temprana-madura con B1 es del 93.5 %» → «95.2 %».

**Protocolo completo (127–145).** «precisión temprana del 80.0 % con una tasa de rechazo del 5.0 %» → «81.2 % […] 5.0 %»; «Con la lectura B1 la precisión madura fue del 82.5 %; con lectura cruda, 68.8 %. La fidelidad temprana-madura fue del 90.0 %.» → «81.2 %; con lectura cruda, 71.2 %. La fidelidad temprana-madura fue del 92.5 %.»; conteos «[50, 16, 44, 25, 30, 14, 17, 31] […] 2.866 bits» → «[46, 16, 40, 25, 30, 18, 21, 31] […] 2.914 bits»; «la fase madura sobre este subconjunto (82.5 %) es inferior a la del banco completo (93.2 %)» → «(81.2 %) […] (93.5 %)».

**Rejilla ι × κ (tabla 181–184 y párrafos 189–205).** Tabla: 0.00 → 81.2 / 5.0; 0.25 → 82.5 / 5.0; 0.50 → 75.0 / 11.2; 1.00 → 8.8 / 86.2. Párrafo: «mejora marginalmente la fase temprana (82.5 % frente a 80.0 %) […] (B1: 83.8 % frente a 82.5 %) y el patrón destructivo reaparece de inmediato: ι = 0.5 pierde 15 puntos con un rechazo del 14 %, y ι = 1.0 rechaza todo.» → «(82.5 % frente a 81.2 %) […] (B1: 83.8 % frente a 81.2 %) y el patrón destructivo reaparece: ι = 0.5 pierde 6 puntos con un rechazo del 11 %, y ι = 1.0 rechaza el 86 % (con el llenado de 4 variantes perdía 15 puntos y rechazaba todo: la poda muerde menos sobre una relación más densa).» «(68.8 % frente a 82.5 % en la línea base; 77.5 % frente a 83.8 % en la mejor condición nativa)» → «(71.2 % frente a 81.2 %; 78.8 % frente a 83.8 %)».

**Formación (224, 231–232).** «todas convergen al 82.5 % final» → «81.2 %»; «conteos [50, 16, 44, 25, 30, 14, 17, 31] y entropía 2.866 bits» → «[46, 16, 40, 25, 30, 18, 21, 31] y entropía 2.914 bits». La frase «el mismo protocolo con el banco completo alcanza 93.2 %» (227) → «93.5 %».

**Capacidad (tabla 260–264).** Solo la variedad L1, que viene del muestreo del recall: 50: 1.87 → 1.89; 100: 1.74 → 1.75; 328: 2.18 → 2.17. Todo lo demás igual (test propio 0/0/2/20/56, falsos 0).

**Sonda de rechazo (153–161).** Sin cambio: 10 de 12.

## B. `.tex8/secciones/06_discusion.tex`

- 50–51: «(80.0 % frente a 93.2 %)» → «(87.0 % frente a 93.5 %)».
- 52–53: «(2.955 de 3.000 bits)» → «(2.974 de 3.000 bits)».
- 55–57: «y la combinación G no supera a B1 sola: una vez corregida la causa, las correcciones auxiliares son redundantes.» → «y la combinación G supera a B1 sola por medio punto (94.0 % frente a 93.5 %), dentro del ruido: una vez corregida la causa, las correcciones auxiliares aportan poco.»
- 72–73: «cayó de 20.0 % a 13.0 % (ideal 12.5 %) y pear subió de ≈52 % a 86 % sin cambiar el vocabulario.» → «cayó de 20.0 % a 13.2 % (ideal 12.5 %) y pear subió de ≈52 % a 86 % sin cambiar el vocabulario (78 % con el llenado de 16 variantes).»
- 107–108: «se queda en 82.5 %, y hace falta el banco completo (≈50 por dominio) para alcanzar el 93.2 %.» → «se queda en 81.2 % […] 93.5 %».

## C. `.tex8/secciones/07_conclusiones.tex`

- 13–17: «precisión temprana del 88.0 % y una precisión madura del 93.2 % […] fidelidad temprana-madura del 93.5 % […] apple […] en 13.0 %» → «90.0 % […] 93.5 % […] 95.2 % […] 13.2 %».
- 31–33: «que llevó la precisión temprana del 50 % al 88 %» → «del 50 % al 90 %»; «20 % → 13.0 %» → «20 % → 13.2 %».

## D. `README.md`, tabla (119–124) y párrafo (137)

- Early-phase accuracy 88.0 % → 90.0 %; Mature B1 93.2 % → 93.5 %; raw (A) 80.0 % → 87.0 %; best combo (G) 92.9 % → 94.0 %; apple share 13.0 % → 13.2 %; per-domain mature (B1): «cup/tomato 100, car 98, cow/dog 96, pear 86, apple 88, horse 82» → «cow/cup/tomato 100, car 98, dog 96, apple 88, horse 88, pear 78».
- 137: «apple's share drops to 13.0% and pear recovers to 86%» → «apple's share drops to 13.2% and pear recovers to 86% with the 4-variant fill (78% with 16 variants)».

## E. `CONTEXTO_SEP2026.md` §9 e `INICIO_NUEVA_SESION.md` §6

Viñeta nueva: «Cifras de texto re-medidas sobre los modelos con 16 variantes (23 de septiembre, commit 9f50751): la hetero de contenido más densa sube la temprana (88.0 → 90.0), la madura cruda (80.0 → 87.0: el sesgo de masa se reduce, brecha con B1 de 13 a 6.5 puntos), B1 (93.25 → 93.5) y G (92.93 → 94.03, ahora medio punto sobre B1); apple cruda 24 → 19.5 %; pear con B1 baja de 86 a 78 %. Protocolo de 80: temprana 80.0 → 81.2, madura B1 82.5 → 81.2, fidelidad 90.0 → 92.5, entropía 2.866 → 2.914. Rejilla ι: 0.5 de 65 a 75 %, 1.0 de 0 a 8.8 %. Capacidad y sonda sin cambio. exp8–exp15 se hicieron sobre los modelos de 4 variantes y quedan como experimentos de ese estado.»
