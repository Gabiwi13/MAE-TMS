# Experimento 7 — directorio unificado texto+imagen

## Método
- Un solo `DirectoryMemory(n=364, m=32, n_agents=8)`: texto en las features 0..299 (fastText recuantizado a 32 niveles con la misma escala global), latentes en las features 300..363 (cuantización de stage7, q=32).
- La mitad ausente de un cue se registra y consulta como indefinida: se pasa `np.nan`, `validate()` la mapea a la fila m y `project()` la salta. `hetero_lib` no se toca. Ojo: pasar el entero m no sirve (`validate` lo recorta a m-1); tiene que ser nan.
- Verificación previa (memorias chicas): el registro con mitad indefinida no deja masa en las features indefinidas y la proyección de un cue mitad-definida es idéntica a la de un directorio puro del subespacio. Pasó.
- Datos: banco de 80 queries de exp4 (236 tokens con vector fastText real) para texto; las 128 imgs/clase de train[200:] (el pool visual completo de stage7) para formar y 20 imgs test/clase para evaluar (submuestreo de las 82, por tiempo de corrida). Maestro de registro = ground truth (exp4 usa el scoring de fase temprana, ~97.5% correcto; aquí el objeto de estudio es el directorio, no la selección del ganador). El texto se evalúa sobre las mismas 80 queries cuyos tokens se registraron: mide memorización de tokens etiquetados con la verdad, no generalización. La imagen sí se evalúa en test.
- Lectura: B1 (÷count) + argmax; texto xi=0, imagen xi=2 (como stage7). k cuenta registros individuales (un token o una imagen).

## Resultados finales

| corrida | métrica | primer k>=90% | sostenido | acc final | rechazo | entropía | counts |
|---|---|---|---|---|---|---|---|
| A · unificado, solo texto | text | 160 | 160 | 96.2% | 0.0% | 2.975 | [28, 21, 34, 25, 34, 24, 33, 37] |
| B · unificado, solo imagen | img | None | None | 81.9% | 18.1% | 3.000 | [128, 128, 128, 128, 128, 128, 128, 128] |
| C · unificado, emparejado | pair | None | None | 25.0% | 75.0% | 2.975 | [28, 21, 34, 25, 34, 24, 33, 37] |
| Base · mem_dir_L (texto) | text | 160 | 160 | 95.0% | 0.0% | 2.975 | [28, 21, 34, 25, 34, 24, 33, 37] |
| Base · mem_dir_R (imagen) | img | None | None | 81.9% | 18.1% | 3.000 | [128, 128, 128, 128, 128, 128, 128, 128] |

Sobre el directorio C (llenado emparejado), consultas por modalidad:

| consulta | acc | rechazo |
|---|---|---|
| solo texto | 96.2% | 0.0% |
| solo imagen | 26.9% | 73.1% |
| emparejada | 25.0% | 75.0% |
| emparejada (base: media texto dir_L + imagen dir_R) | 97.5% | 0.0% |

## Sondas cruzadas
- Imagen sobre el directorio solo-texto (A): rechazo 100% (acc 0%).
- Texto sobre el directorio solo-imagen (B): rechazo 100% (acc 0%).
- Scores de texto de A vs C: diferencia máxima 0.00e+00 sobre los 236 tokens del banco.

## ¿Puede haber interacción entre mitades?
En la relación, no. `project()` (hetero_associative_4d) acumula evidencia por feature de la pista y el veto conjuntivo (`integration==0 | projection==0`) corre solo sobre las features DEFINIDAS de la query; la relación es por par (feature, agente), sin ningún término feature-feature. Como texto e imagen viven en features disjuntas, lo que se registra en una mitad no puede alterar la proyección de la otra. Empíricamente: los scores de texto de A y C son idénticos y la modalidad no registrada se rechaza al 100%.

El ÚNICO canal de acople es el denominador de B1 cuando se toma de `_counts`, un arreglo de Python que cuenta registros de cualquier modalidad. El conteo de texto leído de la relación no cambia con los registros de imagen. Medido sobre A:

| estado del directorio | acc texto |
|---|---|
| solo texto (236 registros) | 96.2% |
| + 1024 imgs balanceadas | 90.0% |
| + 32 re-registros de imgs de apple | 87.5% |

Counts finales tras el desbalance: [188, 149, 162, 153, 162, 152, 161, 165].

## Hallazgos
1. Por modalidad, el unificado replica a los dos directorios: la curva de imagen es idéntica snapshot a snapshot (final 81.9% en ambos) y la de texto difiere solo por la recuantización 32 vs 16 niveles (96.2% vs 95.0%). No se forma ninguna representación compartida: las mitades son independientes por construcción.
2. La query emparejada es el punto débil del unificado, y el 25.0% no es una cifra del veto sino de la cobertura de la mitad de imagen: en el mismo directorio C, la consulta solo-imagen acierta 26.9% y rechaza 73.1%, y la emparejada acierta 25.0% y rechaza 75.0%. El veto conjuntivo corre sobre todas las features definidas del cue, así que la consulta plena hereda el rechazo de su mitad de imagen aunque la mitad de texto rutee sola al 96.2%. La fusión de dos directorios, donde cada modalidad se rechaza por separado, da 97.5%.
3. La imagen en C queda corta por cobertura, no por la unificación: el llenado emparejado solo aporta tantas imágenes distintas como tokens (21-37 por clase) contra las 128 de B; consistente con la curva de capacidad de exp6.
4. El costo vía B1 es de la normalización, no de compartir el espacio: con el denominador tomado de `_counts`, sumar registros de imagen baja el ruteo de texto de 96.2% a 90.0% (balanceado) y 87.5% (desbalanceado) sin tocar la relación. Si B1 lee el conteo de texto de la relación, los registros de imagen no lo cambian y la proyección de texto tampoco, así que no hay caída por construcción. Falta medirlo sobre exp7: el script ya tiene esa columna, pero no se volvió a correr.

En suma: bajo esta proyección el directorio unificado no puede transferir nada entre modalidades y sí paga el veto conjuntivo en queries plenas, que hereda el rechazo de la modalidad menos cubierta. El costo del denominador compartido aparece solo si B1 cuenta registros de cualquier modalidad. Por el veto, los dos directorios separados siguen siendo preferibles.

> **Nota (26 oct 2026):** el hallazgo 4 decía antes «compartir el espacio sí cobra un costo real» y el resumen contaba el denominador como un segundo costo de la unificación. Se corrigió porque el acople viene de dónde se lee el conteo, no de la memoria. En una memoria sintética, 30 registros de solo imagen para un agente bajan su score B1 de texto de 250 a 41.7 con `_counts` (y cambian el ganador), mientras que con el conteo de la relación el score no cambia.

## Archivos
- `results_formation.csv` — series de formación (k, acc, rechazo, entropía, counts por corrida)
- `fig1_formation_unified.png` — curvas de formación por modalidad
- `latents_cache.json` — caché de latentes codificados (CPU)

## Notas
- `run_experiment7_unified_dir.py` no modifica etapas ni memorias existentes; DirectoryMemory se usa tal cual (la lectura tolerante a nan vive en el script porque `predict_tolerant` valida con enteros).
- El registro con mitad indefinida acumula masa en la fila-margen m de `_relation`; esa fila nunca entra a `project()` ni a la iota-relation, así que no afecta ninguna lectura.