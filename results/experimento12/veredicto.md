# Experimento 12: lectura de los resultados

**Corrida:** 21 de septiembre de 2026. 28 pares de clases, semillas 42 a 46, 3 sorteos, consultas reservadas de las dos clases del par (40 a 46 por par). Tablas y coeficientes en `README.md`; diseño y predicción en la cabecera de `run_experiment12_overlap.py`.

## La predicción, en dos partes

Se pre-registró que la brecha de fidelidad de la EHAM de dos clases (M2) respecto del especialista **crece con el solapamiento** entre las dos clases y que **con pares disjuntos es cercana a cero**.

| estadístico (28 pares) | ρ de Spearman | p |
|---|---|---|
| brecha de fidelidad contra solapamiento de soportes en etiquetas | 0.45 | 0.017 |
| error de clase contra solapamiento en etiquetas | 0.49 | 0.008 |
| brecha contra número de etiquetas compartidas | 0.32 | 0.098 |
| brecha contra solapamiento de soportes en el latente | −0.07 | 0.71 |

**Primera parte: confirmada, y en el lado que el mecanismo predice.** La brecha crece con el solapamiento de los soportes de las etiquetas (la pista), no con el del latente (la respuesta). Es lo que dice el mecanismo de exp11: la contaminación ocurre en la proyección de la pista, coordenada por coordenada, donde dos clases registraron los mismos valores cuantizados. El latente que se mezcla es consecuencia, no causa. Los pares con etiquetas compartidas están en el extremo alto: apple–tomato +4.6, apple–pear +2.9, cow–horse +2.4; y son los únicos con errores de clase (94.5%, 98.4% y 97.6%; los otros 25 pares, 100%).

**Segunda parte: no se cumple.** No hay par con brecha cercana a cero. El mínimo es +0.5 (car–cow) y la mediana +1.2; las 28 brechas son positivas. Con solo dos clases y sin ninguna etiqueta compartida, la EHAM única ya reproduce peor que el especialista. La razón está en el rango del solapamiento: el Jaccard medio de soportes en etiquetas va de 0.57 a 0.65 en todos los pares, es decir, cualquier par de clases comparte más de la mitad de los valores cuantizados en cada coordenada. Con 16 niveles sobre 300 coordenadas y vectores fastText, "dominios disjuntos" no existe en esta representación; solo hay grados de solapamiento. La brecha mínima de medio punto es el piso que impone la cuantización.

## Lo que agrega respecto de exp11

- Con dos clases la brecha es de 0.5 a 4.6; con ocho (M8, misma consulta y semillas) va de 0.0 a 11.2. La mezcla se acumula con cada clase que entra, y para las consultas de apple y tomato la EHAM de ocho clases está entre 8 y 11 unidades por encima del especialista.
- La quimera (clase incorrecta, compat baja) necesita etiquetas compartidas; la pérdida de fidelidad no. Son dos efectos con dos causas: la palabra compartida produce la quimera; el valor cuantizado compartido produce la brecha.
- La compat con la otra clase del par está entre 0.48 y 0.70 en todos los pares: cualquier respuesta de M2 tiene entre la mitad y dos tercios de sus coordenadas dentro del soporte de la otra clase, aunque la clase sea correcta.

## Lo que se puede decir en la tesis

"Mejor en dominios solapados" es cierto pero incompleto. La formulación que los datos sostienen: **la ventaja de partir existe para cualquier par de dominios en esta representación, y crece con el solapamiento de las pistas**. Para que la EHAM única igualara al especialista haría falta una cuantización donde los dominios no compartieran valores por coordenada, y esa no es la representación del sistema.

## Límites

- 28 pares de un solo dataset; el rango de solapamiento es estrecho (0.57–0.65) y las tres correlaciones significativas descansan en parte en los pares de frutas y de mamíferos.
- La referencia del especialista es la de exp11 (mismas consultas y semillas, sorteos distintos); la comparación es entre medias por consulta.
- No se corrió el protocolo con dos agentes: con solo dos, el directorio decide entre dos y no mide nada que el oráculo no mida ya.
