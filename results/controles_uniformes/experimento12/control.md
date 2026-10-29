# Control de exp12 con pesos uniformes

Memorias actuales (16 variantes), `MAE_PESOS=uniforme`. El oráculo y M8 se leen de `results/experimento11/raw`, que es la corrida con pesos homo: aquí solo M2 cambia de pesos.

| corrida | brecha M2 media | ρ brecha–solap. etiquetas | p | ρ d M2–solap. | ρ d oráculo–solap. |
|---|---|---|---|---|---|
| vieja (4 variantes, uniformes) | 1.55 | 0.45 | 0.017 | 0.16 | 0.01 |
| actual, pesos uniformes (este control) | 1.82 | 0.06 | 0.750 | 0.22 | 0.20 |
| actual, pesos homo | 2.82 | −0.00 | 0.996 | 0.20 | 0.20 |

- La correlación se pierde con las 16 variantes: con pesos uniformes sobre las memorias actuales tampoco aparece (0.06).
- Los pesos homo alejan a M2 del vecino más cercano en 1.00 en promedio (de 0.02 a 2.74 según el par, en los 28 pares), sin relación con el solapamiento (ρ −0.05, p 0.79).
- Falta el oráculo con pesos uniformes, así que la brecha de este control mezcla M2 uniforme con oráculo homo. Si los pesos homo también alejan al especialista, la brecha uniforme real sería mayor que 1.82.
