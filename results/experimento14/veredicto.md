# Experimento 14: lectura de los resultados

**Corrida:** 23 de septiembre de 2026, `run_experiment14_latent_energy.py`. Umbral sobre la norma del latente continuo, calibrado con el mínimo de los 1600 originales del llenado y margen del 10 %: **τ = 16.6** (mínimo 18.45). Banco degenerado de 231 entradas (§4 de la propuesta). Memoria oficial v5 (contenido y directorio) y contenido de 16 variantes de exp13. Tablas en `README.md`.

## Criterio de refutación (§7)

- (i) Costo real: rechaza 0 del llenado (por construcción), **1 de 1024 de la fase A** (`cow4-066-027`, norma 15.2: una vista oscura de vaca, con desviación de píxeles 44.8; no es una imagen degenerada, es una imagen real de poca energía) y 4 de 656 de test (0.6 %; las cuatro son vacas, `cow3-035-135`, `cow3-068-090`, `cow3-066-117`, `cow6-035-045`, y el directorio ya rechazaba las cuatro, así que el sistema no pierde ninguna respuesta que diera). La letra del criterio no admitía ninguna imagen de la fase A: **por la letra, (i) refuta.** Por el número, el costo es 5 imágenes reales de 3280, todas vacas oscuras que el encoder manda cerca del origen.
- (ii) Fuga: de las 103 entradas degeneradas que la memoria oficial acepta, el criterio deja pasar 18 (cierra el 83 %, umbral 75 %). Contando solo la fuga real, la aceptación **por una clase que no es la de origen**, son 83 y pasan 5 (cierra el 94 %). Se cumple.

Veredicto: **confirmado en lo que importa y refutado en la letra por una imagen.** El criterio cierra la fuga de entradas degeneradas casi entera, con un costo de cinco imágenes reales de vaca que el sistema tampoco resolvía.

## Lo que muestran los datos

**La fuga es una región, no un color.** Las 79 entradas que `horse` acepta en falso (grises 112–128, todo desenfoque de radio ≥ 8–10, todo contraste ≤ 0.2, gris con ruido σ ≤ 2) tienen norma entre 9.9 y 16.8 y desviación entre 1.2 y 2.0: el encoder colapsa cualquier entrada sin estructura en el mismo punto cerca del origen. Los sólidos negro, blanco, de colores y del fondo de ETH-80 quedan lejos (norma 19–58) y se rechazan; el único color aceptado es el magenta puro, por `apple`.

**Es la envolvente, no una instancia (P4 refutada).** La distancia de esas entradas a la instancia real más cercana de `horse` es de 15 a 19, tres veces la distancia mediana entre vecinos de la clase (5.8): `horse` no registró nada cerca del origen; su soporte por coordenada es lo bastante ancho para que la conjunción de las 64 coordenadas pase por ahí. Es el mismo mecanismo de exp8 (la relación guarda soportes por coordenada, no ejemplares) visto desde la entrada.

**Con 16 variantes la región crece y la comparten tres clases.** El contenido de exp13 acepta 100 entradas degeneradas con clase equivocada (`dog` 87, `horse` 75, `cow` 59, `apple` 5), contra 83 de la oficial; el mismo τ deja pasar 12 (cierra el 88 %). Lo que pasa son desenfoques leves de `car` y `cup` (radio 6–10, norma 17–21) que caen en el par animal o en `apple`, y el gris 176 en `cow`.

**Qué estadístico sirve (P2 confirmada).** Norma y desviación del latente son equivalentes (dejan pasar 18 y 17 de las 103); la desviación de píxeles deja pasar 50, porque un objeto desenfocado conserva contraste de píxeles y ya no tiene estructura para el encoder; los niveles vivos no separan nada (13–14 en las degeneradas contra un mínimo real de 11).

**Lo que pasa el umbral no es fuga.** De las 18 aceptaciones que sobreviven a τ, 13 son entradas degradadas reconocidas por su propia clase (desenfoque de radio 2, contraste 0.3–0.5: `car` como `car`, `cow` como `cow`, `tomato` como `tomato`), que es lo deseable. Las 5 restantes son la fuga residual: `dog` con desenfoque 2 y 6 (a `cow` y `horse`), `pear` con contraste 0.3–0.4 (a `cow`) y el magenta (a `apple`). Todas tienen norma entre 16.8 y 27.6, dentro del rango de las imágenes reales, y ningún umbral las separa sin costo: son confusiones de contenido, no entradas degeneradas.

**El directorio.** Rutea 7 entradas del banco, 6 a la clase correcta y una mal (`pear` con contraste 0.4 → `cow`); ninguna cae bajo τ. El directorio nunca rutea las entradas cercanas al origen: la fuga vive en el contenido.

## Lo que no decide

- El costo real está en vacas oscuras (`cow3`, `cow4`, `cow6`): el encoder las acerca al origen. Un margen mayor las salva pero abre la fuga (curva de τ en `README.md`); es un límite del encoder, no del criterio.
- No dice dónde instalar el criterio. El lugar natural es la codificación de la percepción (`image_to_latent` de la etapa 7 y `encode_pil` de la app), como rechazo previo a cualquier memoria, con τ guardado junto a `latent_global_stats.json`; cambiar eso exige re-correr la etapa 7 (la fase A perdería una percepción) y la app.
