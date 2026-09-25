# Síntesis: qué se aprendió del sistema entre el experimento 7 y el 16

**Fecha:** 25 de septiembre de 2026. Lectura de conjunto de `results/experimento7` a `results/experimento16`, las fases 0–5 de revisión y los cambios instalados en el pipeline (doble compuerta, umbral de energía, llenado de 16 variantes). Los detalles y las cifras con intervalos están en los `veredicto.md` de cada experimento; aquí va lo que se entendió, en el orden en que se fue entendiendo.

## 1. Qué clase de cosa es el directorio (exp7, exp8, fase 4)

Empezó como una pregunta de arquitectura (¿un directorio o dos?) y salió una de naturaleza. Exp7 mostró que el directorio unificado texto+imagen no produce ninguna interacción entre modalidades: la relación es por (rasgo, agente), no hay término rasgo–rasgo, y lo único que se acopla es el denominador de la calibración, que daña. Conclusión: **el directorio es un índice**, una tabla de cuentas que dice quién ganó qué, no una memoria que funde contenido. De ahí el principio que atravesó todo lo demás: *la entropía vive en el ícono, la decisión en el índice* (Peirce para las dos caras; Kripke para el nombre como designador sin métrica).

Exp8 complicó eso de la mejor manera: leído al revés, el índice devuelve una descripción del dominio. No un ejemplar, una **envolvente**: siempre de la clase correcta, siempre lejos de cualquier instancia real (2.9 a 5.5 veces la distancia entre vecinos). El directorio es metamemoria en el sentido de Nelson y Narens (un nivel meta que contiene un modelo del nivel objeto) y se aparta de la teoría del índice hipocampal de Teyler y DiScenna justo en que sí tiene contenido. La fase 4 dejó la formulación exacta: la misma relación es nítida cuando se lee hacia la identidad y entrópica cuando se lee hacia el contenido; «el directorio no es entrópico» solo vale para el ruteo.

## 2. Dónde vive el saber (exp9, exp10)

Exp9 quitó un especialista y preguntó qué quedaba. Los demás pueden responder por descripción (la lectura inversa de su directorio), y hasta con más fidelidad que el especialista vivo. Pero lo que no pueden es reconocer: el especialista acepta el 98 % de lo suyo ante lo nunca visto, un no especialista el 16 %. Russell reformulado: **conocer por familiaridad es poder decir «esto es mío»; por descripción, «esto era de él»**. La pérdida transactiva de Wegner es exacta: se pierde la respuesta, no la ubicación. Y la familiaridad resultó ser la contención por coordenada, una puerta que la descripción no tiene.

Exp10 respondió qué es el mediador. Con directorios perspectivales (cada agente registra solo lo que presenció) el grupo rutea igual que con el pizarrón, encadenando (alcance) y agregando (comparación), que son operaciones distintas. El TME de la fase temprana es un andamio (Wood, Bruner y Ross) que se internaliza (Vygotsky), y cada quien internaliza lo que participó. El pizarrón de Hutchins no aporta acierto, solo ahorra consultas. Eso se volvió el protocolo oficial (v5).

## 3. Qué compra partir el contenido (exp11, exp12)

La comparación con una sola EHAM del mismo contenido fue el experimento central y no salió como la versión fuerte esperaba: en clase, la memoria única empata. Lo que la partición compra es **fidelidad, coherencia y precisión**, y lo que cuesta es cobertura, un índice y ocho veces las celdas. El mecanismo es por coordenada, no por palabra: dos conceptos distintos comparten valores cuantizados, y una memoria con varios dominios mezcla al recordar aunque las palabras difieran. La frase que lo resume: *el sistema transactivo es una EHAM que ha decidido antes de recordar*; la memoria única tiene que decidir dentro del sorteo, y ahí falla. Exp12 fijó cuándo: la ventaja existe para cualquier par y crece con el solapamiento de las pistas. Y de exp11 salió la primera fuga honesta, el directorio de texto que deja pasar lo que el contenido rechaza, y con ella la doble compuerta.

## 4. Qué es reconocer (exp13, exp14, exp16)

Este bloque cambió la comprensión más que ningún otro. El 25 % de rechazo visual que el reporte llamaba limitación no era una compuerta sino dos (el directorio formado sin variantes y la conjunción del recall), y cada una cedía solo con su propia densificación. Reconocer, en esta memoria, es una **conjunción de 64 soportes por coordenada**: no hay ejemplares, hay una envolvente, y la envolvente se ensancha registrando los valores vecinos de lo que ya se vio. La augmentación no es un truco: es más percepción registrada, y su precio (dos vistas de un caballo hacia `dog`) aparece exactamente donde las envolventes vecinas se tocan.

Exp14 mostró la cara oscura de la envolvente: el encoder colapsa toda entrada sin estructura en un punto cerca del origen, y ese punto cae dentro del soporte de `horse` sin que `horse` tenga ninguna instancia cerca, a tres veces la distancia intraclase. La memoria acepta lo que su envolvente cubre, no lo que se parece a algo que vio. Por eso la mitigación tuvo que ser externa, un umbral de energía antes de la memoria, calibrado con «nada más débil que lo registrado».

Exp16 fue la prueba de fuego de la misma idea: si la memoria guarda envolventes, un objeto que nunca contribuyó debería caber en la de sus nueve compañeros. Cabe el 89 % de las veces, y cuando no cabe se rechaza, no se inventa. La brecha no vive en clases sino en objetos concretos que no se parecen a los demás de su clase. Generalizar, aquí, es caer dentro de una envolvente formada por otros.

## 5. Qué decide mejor (exp15)

La única política nueva que se probó sobre el ruteo salió refutada, y eso también enseña: entre los candidatos que el directorio ordena, la activación del contenido elige peor que el directorio, y el margen entre scores no separa errores de aciertos. El índice, calibrado por cuentas, compara mejor que la memoria que guarda el contenido, que es la tesis original vista desde su alternativa. Los errores de texto no son empates estrechos: son confusiones de vocabulario compartido, y ninguna abstención barata los quita.

## 6. Lo que cambió en cómo se trabaja

Cada experimento llevó propuesta con predicciones y criterio de refutación antes de correr, y cinco predicciones salieron al revés (la hetero no cede más despacio que el directorio, los falsos aparecen con geometría y no con fotometría, la fuga de color sólido no es el fondo liso, el árbitro empeora, los animales generalizan mejor que las frutas). Las correcciones de honestidad de las fases 0–2 (la pista de identidad con nan, la siembra de `random`, Bessel) y las de la última semana (la etapa 7 que duplicaba directorios al re-correrse, la verificación de que exp11 no acumuló directorios entre semillas, la fragilidad de la conjunción ante un 0.036 % de niveles distintos entre CPU y GPU) son parte del resultado: el sistema es reproducible bit a bit cuando se cuidan el float32 y el dispositivo, y no lo es si no.

## 7. La naturaleza del sistema, en una frase por pieza

- Las memorias de dominio son icónicas y entrópicas: guardan soportes por coordenada, reconocen por conjunción, recuerdan por muestreo y generalizan por envolvente; fallan rechazando.
- El directorio es indicial cuando rutea y descriptivo cuando se lee al revés; compara mejor que el contenido porque cuenta evidencia por interacción.
- El grupo sabe más que cualquier miembro solo a través del índice, y el índice se forma en la interacción y se internaliza por perspectiva.
- Partir el contenido no hace saber más: hace decidir antes de recordar.
- Todo lo anterior es la mitad estática de Wegner. Lo que el sistema todavía no hace es aprender en operación: asignar lo nuevo a alguien y seguir actualizando el índice cuando el mediador ya no está.

## 8. Estado numérico al cierre (sistema oficial: 16 variantes, umbral de energía, doble compuerta)

| medida | 21 de septiembre | 25 de septiembre |
|---|---|---|
| ruteo visual de test (656) | 73.6 % | 96.2 % |
| rechazo visual | 26.4 % | 3.5 % |
| falsos ruteos visuales | 0 | 2 (0.3 %) |
| evocación imagen → etiquetas | 85.3 % | 97.4 % |
| objetos nunca vistos (punta a punta) | sin medir | 89.2 % (0.1 % de falsos) |
| texto: temprana / madura B1 | 88.0 / 93.2 % | 90.0 / 93.5 % |
| fuera de dominio textual (40) | 4 aceptadas | 2 (doble compuerta) |
| etapa 8 | 16/16 | 16/16 |
