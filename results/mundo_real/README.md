# Fase 5: laboratorio en tiempo real (voz y cámara)

Copia de los archivos del laboratorio en el commit `d4740da` (2 ago 2026), que es su versión ya auditada:
- `realtime_lab_README.md`: el README del laboratorio.
- `smtex_05_resultados.tex`: la sección de resultados del reporte de la extensión multimodal.
- `selftest_frame.png` y `wavtest_evocacion.png`: dos salidas de prueba.

## Lo que hay y lo que no
- **Versión del sistema:** v5, con ocho módulos y tres memorias de contenido por módulo. No es la arquitectura final de una memoria heteroasociativa por módulo, y no hay ninguna corrida con la arquitectura final.
- **Voz:** Whisper `small` (faster-whisper) con un detector de voz por energía propio; el VAD de Silero está desactivado (`vad_filter=False`). La frase de punta a punta se probó desde un WAV, no hablada en vivo.
- **Cifras:** salen todas de una sola medición del 16 al 18 de julio de 2026, y no quedó log, JSON ni WAV. Son latencias y una prueba de color en simulación.
- **Lo que no existe:** tasa de error de transcripción, aciertos de enrutamiento con voz y conteos con la cámara física. Las pruebas con la cámara son cualitativas.
- **Cifra obsoleta:** el README cita un 75.0 % de enrutamiento visual que ya no vale. La cifra vigente es 631 de 656 (96.2 %), en `results/hemisferio_visual`.

Por todo esto, la fase 5 se reporta como demostración de integración y no como evaluación.
