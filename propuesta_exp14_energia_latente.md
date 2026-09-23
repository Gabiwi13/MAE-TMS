# Experimento 14: propuesta de diseño para el criterio de entrada previo a la memoria visual

**Fecha:** 23 de septiembre de 2026
**Estado:** propuesta. No hay código nuevo ni corridas oficiales; solo dos sondas exploratorias con los agentes oficiales. Decisiones abiertas marcadas como **[decisión]**.

---

## 1. Qué dice el reporte y qué muestra la exploración

La limitación (b) del reporte deja como mitigación pendiente «un criterio de varianza mínima de la pista latente, previo a la memoria», para la fuga en que «una imagen de color sólido uniforme obtiene soporte y se acepta». Exp13 mostró que esa fuga crece con la densidad (1 → 3 especialistas, y el directorio la rutea con 16 variantes).

Dos sondas exploratorias (23 de septiembre, agentes oficiales v5, 656 de test y 1600 de llenado) acotan el fenómeno:

- **No es «color sólido».** Los sólidos negro, blanco, gris 96, gris 160, rojo y el color de fondo de ETH-80 se rechazan. Se aceptan los grises 112 a 128, y siempre por `horse`.
- **Es una región cerca del origen del latente.** Toda entrada de poca energía (gris medio, un objeto real con desenfoque gaussiano de radio ≥ 12, contraste ≤ 0.2, gris con ruido σ = 2) cae en un latente de norma 10.7–15.8 y desviación 1.3–1.9, y ese punto está dentro del soporte de `horse` (una vez `dog`). Es la conjunción de dos cosas: el encoder colapsa las entradas sin estructura hacia un mismo latente, y una clase lo registró.
- **Las imágenes reales viven lejos de ese punto, con una excepción.** Norma del latente: llenado (originales de `train[:200]`) mínimo 18.45, percentil 1 en 27.5, mediana 49; test mínimo 10.77, percentil 1 en 19.7. La única imagen real por debajo de 18 es `cow3-066-117` (norma 10.77), que es exactamente la que exp13 ruteó en falso a `dog` con 16 variantes: para el sistema esa imagen ya se parece a una entrada degenerada.
- **La desviación de píxeles no basta.** Separa los sólidos (0 contra un mínimo real de 15.4) pero no el desenfoque (una `apple` con radio 16 tiene desviación de píxeles 18.4, por encima del mínimo real, y la memoria la acepta como `horse`).
- **La desviación del latente sola tampoco separa limpiamente**: el gris 128 da 1.323 y la imagen real más débil de test 1.345.

Lo que la exploración sugiere es un criterio de **energía mínima del latente** (su norma), calibrado sobre el llenado, que es donde el sistema sabe cómo son sus percepciones.

## 2. Pregunta

**¿Un umbral sobre la norma del latente, fijado solo con las imágenes de llenado, cierra la fuga de entradas degeneradas sin rechazar imágenes reales, y qué estadístico la cierra mejor?**

## 3. El criterio

Para una percepción con latente continuo $z \in \mathbb{R}^{64}$ (antes de cuantizar, antes de cualquier memoria): se rechaza si $\|z\| < \tau$. **[decisión]** La regla de $\tau$:

- (a) $\tau = (1 - m)\,\min$ de la norma sobre los 1600 originales del llenado, con margen $m = 0.1$ → $\tau \approx 16.6$. Es la regla que garantiza cero rechazos en el llenado por construcción y deja un margen declarado.
- (b) $\tau$ = percentil 0.5 del llenado (≈ 24). Rechazaría más entradas degeneradas y también alguna real de test (percentil 1 de test: 19.7).

Recomiendo (a): el criterio se justifica como «nada más débil que lo que la memoria registró», no como un ajuste sobre el test. Se pre-registra y no se mueve.

Se comparan, con la misma regla de calibración, cuatro estadísticos: norma del latente, desviación del latente, desviación de píxeles en gris, y niveles vivos de la pista cuantizada. Se reporta cuál cierra más fuga a cero costo real. **[decisión]** Reportar los cuatro; recomiendo sí, porque el reporte nombra «varianza» y hay que decir con números por qué la norma (o la varianza) es la que sirve.

## 4. Bancos

- **Reales:** las 656 de test y las 1600 del llenado (originales); las 1024 percepciones de la fase A (`train[200:328]`). Se cuenta cuántas rechaza el criterio y, para cada rechazada, qué hacía el sistema con ella (rutea bien, rutea mal, rechaza).
- **Degeneradas, generadas de forma sistemática y declarada:**
  - sólidos: grises 0–255 de 8 en 8 (33) y 12 colores saturados y del fondo de ETH-80;
  - desenfoque gaussiano de radio 2 a 32 de 2 en 2 sobre una imagen de test por clase (8 × 16 = 128);
  - contraste 0.5 a 0.05 sobre las mismas ocho (8 × 6 = 48);
  - gris 127 con ruido gaussiano σ ∈ {1, 2, 4, 8, 16, 32} (6);
  - gradientes lineal y radial, ruido uniforme, píxeles barajados (4, las sondas del reporte incluidas).
  Para cada una: aceptación del contenido (qué especialistas), ruteo del directorio oficial, y el valor de los cuatro estadísticos.
- **Con las memorias de 16 variantes de exp13** (`cache/exp13/Vc16_N200.pkl`): aceptación del contenido sobre el mismo banco degenerado, para medir cuánto crece la fuga y si el mismo $\tau$ la cierra. **[decisión]** Incluirlo; es barato (la caché existe) y es el caso que motivó esto.

## 5. Métricas

1. **Fuga residual:** entradas degeneradas que la memoria acepta (contenido o directorio) y el criterio deja pasar, por familia y en total.
2. **Costo real:** imágenes reales rechazadas por el criterio (llenado, fase A, test), y qué pasaba con ellas sin criterio.
3. **Separación:** para cada estadístico, la fracción de la fuga que cierra con costo cero en el llenado.
4. **Dónde vive la fuga:** qué especialista acepta cada entrada degenerada y la distancia del latente degenerado a la instancia real más cercana de esa clase (la sonda de exp8/exp9), para decir si `horse` registró algo cerca del origen o si es la envolvente.

## 6. Predicciones

- P1. Con $\tau$ de (a), la fuga residual del contenido oficial queda en cero para sólidos, desenfoques y contrastes; el costo real es una imagen de test (`cow3-066-117`) y ninguna del llenado ni de la fase A.
- P2. La norma y la desviación del latente rinden igual (en 64 dimensiones con media cercana a cero son casi la misma cantidad); la desviación de píxeles deja pasar el desenfoque; los niveles vivos no separan (13–14 en degeneradas contra mínimo real 11).
- P3. Con 16 variantes la fuga crece (más grises y más radios de desenfoque aceptados, y el directorio rutea) pero sigue dentro de la misma región de norma baja, así que el mismo $\tau$ la cierra.
- P4. La clase que acepta es `horse` porque alguna de sus instancias de llenado tiene norma baja (vistas oscuras o de bajo contraste); si es así, la distancia del gris al vecino real más cercano de `horse` será del orden de la distancia intraclase, no una envolvente.

## 7. Criterio de refutación

El criterio queda **refutado** si, con $\tau$ de (a): (i) rechaza alguna imagen del llenado o de la fase A, o más del 1 % de las de test (7 de 656); o (ii) deja pasar más de la cuarta parte de las entradas degeneradas que la memoria oficial acepta. Queda **confirmado** si rechaza a lo sumo 1 % de test con cero en llenado y cierra al menos tres cuartas partes de la fuga. Entre medias se reporta la curva de $\tau$.

## 8. Qué no decide

- No cierra la fuga de imágenes reales de baja energía que el encoder confunde (`cow3`): eso es del encoder, no del criterio.
- No dice si el criterio debe adoptarse en el pipeline oficial (`image_to_latent` de la etapa 7 y `encode_pil` de la app); ese cambio se decide con el resultado y se verifica con la etapa 7 completa.

## 9. Entregables

`run_experiment14_latent_energy.py` (minutos de cómputo, GPU para codificar), `results/experimento14/{README.md, resumen.json, banco_degenerado.json, fig1_norma_vs_aceptacion.png, veredicto.md}` y la prosa viejo/nuevo para la limitación (b) y el trabajo futuro.
