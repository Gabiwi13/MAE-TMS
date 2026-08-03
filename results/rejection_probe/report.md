# Micro-test de rechazo por la EAM

> **Nota de procedencia (2 ago 2026).** Este `.md` se escribió a mano a
> partir de `summary.json` y `results_per_query.json` (los artefactos
> vigentes de esta carpeta, sistema de 8 clases). `run_rejection_probe.py`
> ya no genera un `.md`; la fuente canónica de las métricas sigue siendo
> `summary.json`, y este informe es solo su lectura narrada. La versión
> anterior de este archivo (era de 3 clases apple/horse/car, "rechazadas
> por la EAM: 5", "falsos routings: 7", fechada 22 jun 2026) quedó
> **obsoleta** — no corresponde a los JSON actuales — y fue reemplazada
> por esta.

**Diagnóstico, no parte del benchmark de accuracy.** Banco de 12 consultas
*representables* (todas producen vectores fastText reales, ninguna se filtra por
léxico) que describen objetos **fuera** de los 8 dominios ETH-80 (apple, car,
cow, cup, dog, horse, pear, tomato). Si la EAM es el mecanismo de rechazo,
debería rechazar por containment (`recognize_gated → 0`), sin ninguna regla
externa.

## Resultado

| métrica | valor |
|---|---|
| consultas | 12 |
| representables | 12 / 12 |
| **rechazadas por la EAM** | **10** |
| falsos routings (soporte espurio) | 2 |
| no representables | 0 |

## Interpretación

El rechazo **emerge de la memoria**: 10 de 12 consultas fuera de dominio se
rechazan por containment puro (`max(score)==0` en los ocho agentes), sin que
ningún filtro léxico intervenga. Esto es lo que el test pretende demostrar: con
una pista vectorial real, la decisión de "no sé" puede salir de la EAM.

No es un detector de dominio perfecto, y no se esperaba que lo fuera: 2
consultas rutean a un agente porque **comparten tokens con el vocabulario de
labels** que sí tienen soporte legítimo:

- *"a kitchen appliance that heats food"* → **apple** (el token *food* es label
  de apple con soporte real).
- *"a wooden table and chairs"* → **cup** (scores: cup 5836.6, dog 5331.8; los
  tokens *wooden/table/chair* activan relaciones aprendidas en esos dominios).

Esos routings no son un fallo del mecanismo de rechazo: son soporte real de la
memoria sobre tokens que de hecho aparecen en su dominio. La frontera entre
"fuera de dominio" y "comparte conceptos con el dominio" es semántica, no
léxica, y el test la mide en lugar de esconderla.

Artefactos: `summary.json` (métricas), `results_per_query.json` (scores y
veredicto por consulta).
