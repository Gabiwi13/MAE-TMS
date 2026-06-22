# Experimento 4 — curva de formación del directorio transactivo

## Pregunta
¿Cuántas interacciones necesita el grupo para que el routing punto a
punto sea confiable (el TME pueda apagarse)? ¿Importa el orden de las
experiencias? ¿El sesgo de densidad impide la convergencia?

## Transiciones (accuracy madura ≥ 90%)

| condición | primer k | k sostenido | acc final | entropía final | counts |
|---|---|---|---|---|---|
| A · intercalado | 13 | 13 | 98.8% | 1.563 | [71, 58, 46] |
| B · barajado s0 | 23 | 23 | 98.8% | 1.563 | [71, 58, 46] |
| B · barajado s1 | 27 | 27 | 98.8% | 1.563 | [71, 58, 46] |
| B · barajado s2 | 15 | 15 | 98.8% | 1.563 | [71, 58, 46] |
| B · barajado s3 | 24 | 24 | 98.8% | 1.563 | [71, 58, 46] |
| B · barajado s4 | 18 | 18 | 98.8% | 1.563 | [71, 58, 46] |
| C · bloqueado | 57 | 57 | 98.8% | 1.563 | [71, 58, 46] |
| D · crudo (control sesgo) | 14 | 46 | 95.0% | 1.508 | [81, 59, 35] |

## Archivos
- results_formation.csv (formato largo: run, k, métricas)
- fig1_formation_curve.png — la figura central
- fig2_entropy_curve.png · fig3_rejection_curve.png · fig4_counts_dynamics.png

## Notas de instrumentación
- M_dom de stage5 solo lectura; M_dir fresco por corrida (DirectoryMemory, EHAM real).
- Los 4 M_dir de la arquitectura reciben registros idénticos; se instrumenta uno que representa el estado compartido.
- Sin recall en temprana (M_dir_R no participa del routing por labels; pipeline completo validado en exp. 3).