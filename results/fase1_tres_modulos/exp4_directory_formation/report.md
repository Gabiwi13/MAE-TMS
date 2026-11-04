# Experimento 4 — curva de formación del directorio transactivo

## Pregunta
¿Cuántas interacciones necesita el grupo para que el routing punto a
punto sea confiable (el TME pueda apagarse)? ¿Importa el orden de las
experiencias? ¿El sesgo de densidad impide la convergencia?

## Transiciones (accuracy madura ≥ 90%)

| condición | primer k | k sostenido | acc final | entropía final | counts |
|---|---|---|---|---|---|
| A · intercalado | 13 | 47 | 98.8% | 1.567 | [78, 65, 53] |
| B · barajado s0 | 24 | 24 | 98.8% | 1.567 | [78, 65, 53] |
| B · barajado s1 | 20 | 25 | 98.8% | 1.567 | [78, 65, 53] |
| B · barajado s2 | 15 | 30 | 98.8% | 1.567 | [78, 65, 53] |
| B · barajado s3 | 24 | 24 | 98.8% | 1.567 | [78, 65, 53] |
| B · barajado s4 | 18 | 44 | 98.8% | 1.567 | [78, 65, 53] |
| C · bloqueado | 67 | 67 | 98.8% | 1.567 | [78, 65, 53] |
| D · crudo (control sesgo) | 14 | 66 | 93.8% | 1.541 | [84, 67, 45] |

## Archivos
- results_formation.csv (formato largo: run, k, métricas)
- fig1_formation_curve.png — la figura central
- fig2_entropy_curve.png · fig3_rejection_curve.png · fig4_counts_dynamics.png

## Notas de instrumentación
- M_dom de stage5 solo lectura; M_dir fresco por corrida (DirectoryMemory, EHAM real).
- Los 4 M_dir de la arquitectura reciben registros idénticos; se instrumenta uno que representa el estado compartido.
- Sin recall en temprana (M_dir_R no participa del routing por labels; pipeline completo validado en exp. 3).