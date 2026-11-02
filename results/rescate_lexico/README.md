# Rescate léxico en la fase temprana (1 nov 2026)

**Pregunta:** ¿cuánto aporta la regla de `tokenize_query` que rescata tokens mal etiquetados por spaCy? Un token descartado por su etiqueta en contexto entra igual si, aislado, es NOUN, ADJ o PROPN, o si es una etiqueta registrada del sistema.

**Método** (`run_rescate_lexico.py`, solo lee `models/`). Las 411 consultas del banco, con el sistema actual (una sola hetero por módulo). Para cada consulta se calcula el ganador temprano como en `run_experiment3.process_query_early`: suma de `recognize_gated` sobre los tokens con vector y argmax entre los 8 módulos. Se hace dos veces: con `tokenize_query` y con la misma función sin sus dos vías de rescate.

| | Con la regla | Sin la regla |
|---|---|---|
| Consultas afectadas (los tokens difieren) | 46 | 46 |
| Aciertos en las afectadas | 43 (93.5 %) | 33 (71.7 %) |
| Rechazos en las afectadas | 0 | 4 |
| Aciertos en todo el banco | 371 de 411 | 361 de 411 |

- La regla solo agrega tokens: en las 411 consultas, los tokens sin la regla están todos en la lista con la regla.
- Cambia el ganador en 10 consultas, y las 10 pasan a la clase correcta.
- Tokens rescatados más frecuentes: *bark*, *riding*, *drink*, *canine*, *drive*, *run*, *moo*, *racing*.

Efecto: **+21.7 puntos sobre las consultas afectadas** (+2.4 sobre el banco).
