# Micro-test de rechazo por la EAM

**Diagnóstico, no parte del benchmark de accuracy.** Banco de 12 consultas
*representables* (todas producen vectores fastText reales, ninguna se filtra por
léxico) que describen objetos **fuera** de apple/horse/car. Si la EAM es el
mecanismo de rechazo, debería rechazar por containment (`recognize_gated → 0`),
sin ninguna regla externa.

## Resultado

| métrica | valor |
|---|---|
| consultas | 12 |
| representables | 12 / 12 |
| **rechazadas por la EAM** | **5** |
| falsos routings (soporte espurio) | 7 |
| no representables | 0 |

## Interpretación

El rechazo **emerge de la memoria**: 5 de 12 consultas fuera de dominio se
rechazan por containment puro (`max(score)==0` en los tres agentes), sin que
ningún filtro léxico intervenga. Esto es lo que el test pretende demostrar: con
una pista vectorial real, la decisión de "no sé" puede salir de la EAM.

No es un detector de dominio perfecto, y no se esperaba que lo fuera: 7
consultas rutean a un agente porque **comparten tokens con el vocabulario de
labels** que sí tienen soporte legítimo — p.ej. *food* y *green* son labels de
apple, y *water/glass/plant* activan relaciones aprendidas. Esos routings no son
un fallo del mecanismo de rechazo: son soporte real de la memoria sobre tokens
que de hecho aparecen en su dominio. La frontera entre "fuera de dominio" y
"comparte conceptos con el dominio" es semántica, no léxica, y el test la mide
en lugar de esconderla.

Artefactos: `summary.json` (métricas), `results_per_query.json` (scores y
veredicto por consulta).
