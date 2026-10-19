# Propuesta del experimento 25 — la organización transactiva contra rivales federados y descentralizados

**Estado:** propuesta; nada corrido.

## Pregunta

Exp24 mostró que, como clasificador, la memoria pierde contra NCM, kNN, RanPAC y Mondrian sobre los mismos rasgos. Lo que ningún rival comparte es la **organización transactiva**: el conocimiento está repartido entre especialistas, nadie tiene todos los datos, las consultas entran por cualquier agente y cada agente aprende **quién sabe qué** solo de las transacciones en las que participa, sin servidor central ni ronda de intercambio explícita (exp10). La pregunta dura: **¿esa organización hace algo que los rivales federados o descentralizados no hacen, a igual información y a igual costo de comunicación?**

## Escenario

- **Dominios:** los 11 órganos (OrganAMNIST) y las 4 modalidades del demo médico. Un agente por dominio, con su contenido (200 × 16 variantes) y sus rasgos (los ajustados del nivel 2, para no pelear con la percepción).
- **Formación:** 128 consultas de fase A por dominio. Cada una entra por un agente al azar. **Visibilidad parcial**, como en exp10: la transacción la registran el agente de entrada y el ganador (protocolo oficial), y además cada otro agente con probabilidad f ∈ {0, 1/16, 1/4, 1}, o solo sus vecinos en un anillo de radio r ∈ {1, 2}.
- **Prueba:** test oficial, entrada por un agente al azar distinto del especialista.

## Brazos

Todos los brazos descentralizados ven **exactamente las mismas transacciones**. Solo cambia cómo guardan y leen «quién sabe qué».

| brazo | qué guarda cada agente | cómo rutea | central |
|---|---|---|---|
| **MAE** (el sistema) | directorio asociativo de las transacciones presenciadas | `route_transactive` (agregado + encadenado), B1 y principio de tamaño | no |
| **Prototipos transactivos** | para cada agente j, el promedio de las pistas presenciadas que ganó j | prototipo más cercano entre los conocidos; mismo encadenado | no |
| **kNN transactivo** | las pistas presenciadas con su ganador | 5 vecinos; mismo encadenado | no |
| **Gossip de prototipos** | cada agente comparte su propio prototipo con sus vecinos durante T rondas (T igual al número de mensajes que implica la fase A) | prototipo más cercano | no |
| **FedProto** (cota) | cada agente envía su prototipo una vez a todos | NCM global | ronda explícita de difusión |
| **FedAvg** de una cabeza lineal (cota) | rondas con servidor, clientes no iid de una clase | clasificador global | sí |
| **Oráculo central** | todo el contenido junto | NCM y kNN globales | sí |

## Qué se mide

1. **Acierto de punta a punta** (ruteo y reconocimiento del especialista destino), rechazo y falsos ruteos, en función de f y r.
2. **Comunicación:** mensajes y bytes durante la formación y por consulta. También **qué se revela**: pistas crudas, prototipos o parámetros.
3. **Pérdida de un miembro** (exp9): se quita al especialista k. ¿Las consultas de su dominio se ubican como «de k, ausente», se rutean mal o se rechazan?
4. **Ingreso de un miembro:** se agrega un dominio nuevo. ¿Cuántas transacciones hacen falta para que los demás lo ruteen bien? ¿Hay que tocar algo de lo que ya existía?
5. **Lo ajeno:** consultas de una modalidad nunca vista (fondo de ojo). ¿El brazo dice «nadie sabe» o las manda a alguien?

## Predicciones (fijadas antes de correr)

- **P1.** Con las mismas transacciones, los directorios por distancia (prototipos o kNN transactivos) rutean igual o mejor que el directorio MAE. Exp24 hace esperar que la contención pierda contra la distancia.
- **P2.** FedProto alcanza el mejor acierto con muy poca comunicación (un mensaje de 64 números por agente), pero necesita una ronda explícita de difusión que el sistema transactivo no necesita.
- **P3.** Con visibilidad muy baja (f = 0, anillo r = 1), el encadenado mantiene el alcance en todos los brazos descentralizados. La diferencia entre brazos estará en la comparación, no en el alcance (exp10).
- **P4.** Ante la pérdida de un miembro, el directorio MAE y el de prototipos conservan la ubicación («era de k»). FedAvg no, porque el conocimiento quedó mezclado en los parámetros globales.
- **P5.** Ante lo ajeno, el directorio MAE rechaza más que los directorios por distancia, que siempre devuelven al más cercano. Eso solo cuenta como ventaja si no viene acompañado de más rechazo de lo propio (se compara a igual aceptación, como en exp20).

**Criterio:** la organización transactiva de la MAE se sostiene como aportación si gana claramente en al menos una de las propiedades 2 a 5, a igual información, frente al mejor rival descentralizado. Se refuta si en todas iguala o pierde frente a los prototipos transactivos, que tienen la misma organización y comparan por distancia: en ese caso lo valioso sería la organización transactiva en sí, no la memoria asociativa que la implementa.

## Costo

≈ 2–3 h de cómputo con las cachés del demo médico. Sin descargas.
