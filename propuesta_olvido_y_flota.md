# Olvido exacto, privacidad y enrutador de una flota: propuesta de diseño

**Fecha:** 18 de octubre de 2026
**Estado:** fijada antes de correr. Lo que cambie después se declara en el informe como desviación.

Dos experimentos sobre las propiedades de la MAE que no son de exactitud: aprender es registrar conteos, la memoria no guarda ejemplares y el sistema rutea con abstención. Datos: las cachés del demo industrial (VisA; latentes ResNet18 + PCA64 del nivel 1 y de cada pieza, y parches) y las del demo médico balanceado (solo lectura, desde `MAE-TMS-medico/results/medico_balanceado/cache`).

## A · Olvido exacto y privacidad

### A1. ¿Olvidar un registro deja la memoria como si nunca se hubiera registrado?

La MAE oficial no tiene una operación para olvidar. Se define **olvidar = restar la misma relación que sumó el registro** (`relation −= to_relation(v)`, y en los directorios `relation −= vectors_to_relation(v, agente)` con el contador del agente − 1). Es la inversa exacta de `abstract` mientras ningún conteo llegue al tope de 2¹⁶ − 1 (el máximo aquí es 270 × 16 = 4320).

Nivel 1 industrial (12 piezas, el protocolo `Level`), semilla 42:
- **A1a, olvidar contenido:** el 10 % de las imágenes de llenado de cada pieza (27, con sus 16 variantes). Se compara la memoria con olvido contra una memoria construida desde cero sin esas imágenes:
  - (i) la relación de cada especialista, celda por celda;
  - (ii) los directorios. La fase A decidió sus ganadores con el contenido completo, así que la construcción desde cero puede decidir otros. Se mide cuántas percepciones de fase A cambian de destino, y cuántas decisiones de test difieren entre las dos memorias.
- **A1b, olvidar transacciones:** el 10 % de las percepciones de fase A. Se restan de los directorios de los dos participantes y del TME. La construcción de referencia rehace la fase A sin esas percepciones, con la misma entrada para cada transacción que queda. La entrada es parte de la transacción; volver a sortearla mezclaría el efecto del azar con el del olvido. Se compara cada directorio celda por celda y todas las decisiones de test.
- **Verificación previa:** la fase A con registro de transacciones que uso tiene que dar exactamente los mismos directorios que `Level._phase_a` oficial.
- **Comparaciones:** kNN y NCM olvidan exactamente por construcción (se borra la fila o se resta de la suma). La cabeza logística ajustada al llenado no olvida sin reentrenar. Se reporta el costo en tiempo de olvidar contra el de reconstruir.

### A2. ¿Cuánto revela la memoria de un registro individual?

Los miembros son las imágenes registradas (llenado) y los no miembros, imágenes de la misma distribución que no se registraron (calibración o fase A). El atacante tiene el latente original del candidato y el estado guardado de cada método:

- **MAE:** puntaje = Σᵢ log(1 + conteo en el nivel del candidato en la coordenada i), del especialista de su dominio.
- **kNN:** menos la distancia al registro más cercano (guarda los ejemplares).
- **NCM:** menos la distancia a la media del dominio.
- **Gaussiana:** menos la distancia de Mahalanobis (+0.01 I).

Se reporta el AUROC del ataque de pertenencia por dominio. También la **exposición por celdas únicas**: cuántas coordenadas de un miembro caen en una celda que solo él (con sus variantes) ocupó, de modo que esa coordenada queda atribuida a él. Dominios: las 12 piezas industriales (latentes G2 por pieza y del nivel 1) y el demo médico (nivel 1 de modalidad y órganos).

Fuera de alcance, y se declara: un atacante que ve la memoria antes y después de un registro recupera ese registro en cualquiera de los métodos (la diferencia de conteos da sus niveles; la de sumas, su latente).

### Predicciones A

- **PA1.** A1a (i) y A1b: igualdad exacta, con 0 celdas distintas y 0 decisiones distintas. A1a (ii): la fase A depende del camino; cambia el destino de menos del 1 % de las percepciones de fase A y de menos del 1 % de las decisiones de test.
- **PA2.** kNN: AUROC de pertenencia ≥ 0.95, porque guarda el registro. MAE: de 0.50 a 0.65, del lado de los métodos de agregados, cerca de NCM y de la gaussiana. Exposición: pocos miembros con coordenadas únicas (en las colas de la distribución).

### Criterio A

«La MAE olvida exactamente» queda sostenida si A1a (i) y A1b dan 0 diferencias; una sola diferencia la refuta. «La MAE no guarda ejemplares en un sentido útil para la privacidad» queda sostenida si su AUROC de pertenencia, en la media de los dominios, está más cerca del de NCM que del de kNN, y refutada si queda a menos de 0.1 del de kNN.

## B · Enrutador de una flota de detectores

En la línea de VisA hay un detector PatchCore por pieza (kNN por parches, como en el demo, con el umbral fijado para aceptar el 95 % de las normales de calibración de su pieza). El enrutador decide qué detector recibe cada imagen o si ninguno: si se abstiene, la imagen va a un humano.

- **Enrutadores:** MAE (nivel 1 con el protocolo `Level`); kNN (5 vecinos) sin abstención; kNN con abstención (distancia media a 5 vecinos, umbral fijado para aceptar la misma fracción de normales de calibración que acepta la MAE); y oráculo (la pieza verdadera).
- **B1, piezas conocidas:** todo el test. Por enrutador: a la pieza correcta, abstención y a otra pieza. Punta a punta: detección de fallas, falsa alarma y abstenciones. Si una imagen va a otra pieza, la decide el detector de esa pieza, con los parches de la imagen proyectados con la PCA de esa pieza.
- **B2, pieza nueva sin registrar:** 12 pliegues dejando una pieza fuera. El sistema se construye con 11 piezas y llegan las imágenes de test de la pieza ausente. Lo deseable es abstenerse. Lo peor es mandarla a otro detector y que pase como normal (falla silenciosa). Se mide para los cuatro enrutadores.
- **Tamaño:** bytes del estado de cada enrutador.

### Predicciones B

- **PB1.** Con piezas conocidas, la MAE y kNN empatan en el sistema completo con el oráculo (diferencias de menos de 1 punto en detección y en falsa alarma). La MAE se abstiene en el 1–2 % de las normales y en el 10–15 % de las fallas, lo que suma alarmas.
- **PB2.** Con una pieza nueva, kNN sin abstención manda el 100 % a otro detector. La MAE se abstiene en una parte grande (≥ 50 %), pero no en todas: con piezas parecidas (pcb, macaroni, fryum), la envolvente de la vecina contiene a la nueva. kNN con abstención a igual aceptación queda cerca de la MAE (exp20: la memoria rechaza lo cercano como kNN).
- **PB3.** El estado de la MAE pesa más que el de kNN con estos tamaños de registro (12 especialistas de 64 × 32 conteos, más los directorios de 64 × 12 × 32 × 2 por agente, contra 3240 × 64 flotantes).

### Criterio B

«La abstención de la MAE protege a la flota de una pieza nueva» queda sostenida si la falla silenciosa con la MAE es al menos 20 puntos menor que con kNN sin abstención y no mayor que con kNN con abstención más 5 puntos. Queda refutada si la abstención de la MAE ante la pieza nueva es menor de 30 % en la media de los pliegues.

## Entregables

`run_olvido_privacidad.py`, `run_enrutador_flota.py` y `results/{olvido_privacidad, enrutador_flota}/{README.md, resumen.txt, resultados.json}`.
