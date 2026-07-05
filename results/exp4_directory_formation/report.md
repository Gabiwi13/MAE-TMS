# Experimento 4 — curva de formación del directorio transactivo

## Pregunta
¿Cuántas interacciones necesita el grupo para que el routing punto a
punto sea confiable (el TME pueda apagarse)? ¿Importa el orden de las
experiencias? ¿El sesgo de densidad impide la convergencia?

## Transiciones (accuracy madura ≥ 90%)

| condición | primer k | k sostenido | acc final | entropía final | counts |
|---|---|---|---|---|---|
| A · intercalado | None | None | 77.5% | 2.693 | [72, 16, 37, 25, 30, 21, 3, 23] |
| B · barajado s0 | None | None | 77.5% | 2.693 | [72, 16, 37, 25, 30, 21, 3, 23] |
| B · barajado s1 | None | None | 77.5% | 2.693 | [72, 16, 37, 25, 30, 21, 3, 23] |
| B · barajado s2 | None | None | 77.5% | 2.693 | [72, 16, 37, 25, 30, 21, 3, 23] |
| B · barajado s3 | None | None | 77.5% | 2.693 | [72, 16, 37, 25, 30, 21, 3, 23] |
| B · barajado s4 | None | None | 77.5% | 2.693 | [72, 16, 37, 25, 30, 21, 3, 23] |
| C · bloqueado | None | None | 77.5% | 2.693 | [72, 16, 37, 25, 30, 21, 3, 23] |
| D · crudo (control sesgo) | None | None | 77.5% | 2.693 | [72, 16, 37, 25, 30, 21, 3, 23] |

## Archivos
- results_formation.csv (formato largo: run, k, métricas)
- fig1_formation_curve.png — la figura central
- fig2_entropy_curve.png · fig3_rejection_curve.png · fig4_counts_dynamics.png

## Notas de instrumentación
- M_dom de stage5 solo lectura; M_dir fresco por corrida (DirectoryMemory, EHAM real).
- Los 4 M_dir de la arquitectura reciben registros idénticos; se instrumenta uno que representa el estado compartido.
- Temprana semántica registra solo el directorio de labels; mem_dir_R (visual) se entrena solo con percepciones reales en stage7.