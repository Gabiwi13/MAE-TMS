# Experimento 11: lectura de los resultados

**Corridas:** 21 y 22 de septiembre de 2026. Texto→imagen: cortes N ∈ {25, 50, 100, 200} imágenes por clase (×4 variantes), 10 semillas (42–51), 3 sorteos por consulta, 171 consultas reservadas. Imagen→texto: los mismos cortes y semillas, 10 imágenes de prueba por clase. Fuera de dominio: 40 consultas, con y sin doble compuerta de contenido en el protocolo. Tablas completas con intervalos en `README.md`; criterio de refutación en `../../propuesta_fase5_mae_monolitica.md` §8. Control: en N=200 los especialistas reconstruidos son bit a bit los `agent_*.pkl` oficiales (8/8).

## Las curvas

| medida | brazo | N=25 | N=50 | N=100 | N=200 |
|---|---|---|---|---|---|
| clase correcta (1-NN, %) | M | 95.9 | 97.1 | 97.7 | 97.4 |
| | T-oráculo | 100 | 100 | 100 | 100 |
| | T-protocolo | 98.5 | 97.9 | 97.3 | 97.5 |
| d a la instancia real más cercana | M | 17.26 | 21.29 | 23.88 | 26.69 |
| | T-oráculo | 15.25 | 18.85 | 19.66 | 22.20 |
| | T-protocolo | 15.72 | 19.60 | 20.42 | 22.75 |
| responde (%) | M | 81.3 | 100 | 100 | 100 |
| | T-oráculo | 80.1 | 100 | 100 | 100 |
| | T-protocolo | 78.9 | 98.5 | 98.6 | 98.6 |
| niveles vivos por coordenada | M | 4.04 | 5.68 | 7.51 | 9.03 |
| | T-oráculo | 3.88 | 5.48 | 7.23 | 8.69 |
| clase con primera pista compartida (%) | M | 37.2 | 33.9 | 50.6 | 44.4 |
| | T-oráculo | 100 | 100 | 100 | 100 |
| | T-protocolo | 78.6 | 65.7 | 62.5 | 65.7 |
| compat máx con pista compartida | M | 0.71 | 0.72 | 0.74 | 0.73 |
| fuera de dominio aceptadas (de 40) | M | 2 | 2 | 3 | 3 |
| | T-oráculo | 2 | 2 | 2 | 2 |
| | T-protocolo | 3 | 4 | 4 | 4 |
| | T-protocolo con compuerta | 2 | 2 | 2 | 2 |
| ruteo correcto (%) | T-protocolo | 95.4 | 96.4 | 96.0 | 96.1 |
| F (dentro de clase) | M | 3.37 | 1.83 | 1.59 | 1.36 |
| | T-oráculo | 1.83 | 1.26 | 1.15 | 1.08 |
| | T-protocolo | 2.95 | 2.15 | 1.98 | 1.75 |

## Criterio de refutación (§8), sobre N=200

1. Clase 1-NN: M 97.4 [97.3, 97.7] contra T-protocolo 97.5 [97.1, 97.9]. Diferencia de 0.1 puntos, intervalos solapados. **Se cumple.**
2. Fidelidad: M 26.69 [26.64, 26.75] contra T-protocolo 22.75 [22.59, 22.88]. Diferencia de 3.9 unidades, umbral 1. **No se cumple.**
3. Fuera de dominio, con el banco de 40 consultas (`consultas_fuera_dominio.txt`: las 12 originales más 28 nuevas de categorías ausentes, sin palabras del vocabulario de etiquetas): la EHAM única acepta 3 de 40 en N ≥ 100 (2 en N ≤ 50), el oráculo 2 de 40 en todos los cortes, el protocolo 4 de 40. Las dos que aceptan todos son las originales con palabras del vocabulario (`food`, `table`); de las 28 nuevas la EHAM única acepta una (`a piece of furniture for sitting`) y los especialistas ninguna. Misma dirección que P3, con una consulta de diferencia: no separable. **No se cumple como refutación ni como confirmación.** Con la doble compuerta de contenido (el agente destino debe contener la pista, no solo el directorio señalarlo) el protocolo baja a 2 de 40 en los cuatro cortes, las mismas dos que el oráculo.

La tesis **no queda refutada**: el criterio exigía las tres condiciones a la vez. Tampoco se sostiene en la forma fuerte que preveía la propuesta (M perdiendo en clase sobre el banco completo).

## Lo que sí muestran los datos

**La partición compra fidelidad, y la ventaja crece con el contenido.** La distancia de la respuesta a una instancia real es peor en M en los cuatro cortes, y la diferencia con el oráculo sube de 2.0 (N=25) a 4.5 (N=200). Es la predicción P2. El mecanismo está en los niveles vivos: la proyección de M es solo un 4% más ancha que la del especialista (9.03 contra 8.69 en N=200), pero esos niveles extra son valores que otras clases registraron en la misma coordenada, y el sorteo por coordenada cae lejos cuando los toma. La contaminación no es por palabra compartida sino por coordenada: dos etiquetas distintas comparten valores cuantizados en muchas de las 300 coordenadas.

**La quimera existe y está donde se predijo, pero es rara.** Cuando la primera pista reconocida es una etiqueta compartida (fruit, animal, mammal, red, pome, table), M acierta la clase entre el 34% y el 51% y su patrón tiene soporte en una sola clase en el 71–74% de las coordenadas. Es la predicción P1. Pero esas consultas son el 3.5–4.4% de las respuestas del banco, así que sobre el banco completo M iguala a T-protocolo en clase desde N=100. En N=25 y N=50 T-protocolo gana en clase por 2.6 y 0.8 puntos (intervalos separados en N=25).

**El precio del directorio quedó medido y es estable.** T-protocolo pierde 2.5 puntos de clase respecto del oráculo en todos los cortes: 1.4% de consultas sin respuesta y 3.6–4.6% de ruteos a otro agente. Con pista compartida el ruteo acierta menos (63–79%), porque la pista que confunde a la memoria de contenido también confunde al directorio. Es la predicción P5.

**Cobertura.** M no responde más que T-oráculo: en N=25 los dos aceptan el 81.3% de las consultas, porque la homo de M es la unión de las ocho y el containment acepta exactamente lo que acepta el mejor especialista. La predicción P4 (M responde más) solo se cumple frente a T-protocolo, por el 1.4% que el directorio rechaza.

**Dependencia de la pista.** F dentro de clase queda en 1.08 para el oráculo en N=200 (exp9 midió 1.14 para el especialista con las memorias oficiales, consistente). M da 1.36 y T-protocolo 1.75. En T-protocolo la F sube porque los ruteos equivocados producen respuestas de otra clase para algunas consultas, lo que infla la varianza entre consultas dentro de la clase; no es dependencia de la pista sino del destino.

## Imagen → texto (cuatro cortes, 10 semillas, 10 imágenes de test por clase)

| medida (sobre 800 imágenes por brazo, N=200) | M | T-oráculo | T-protocolo |
|---|---|---|---|
| acepta (containment de la homo latente; T-protocolo: el directorio rutea) | 100 | 97.5 | 81.2 |
| responde (recall_from_right reconoce) | 96.2 | 78.7 | 72.5 |
| hit laxo (alguna etiqueta del vocabulario del dominio, etapa 7) | 95.2 | 78.7 | 72.5 |
| hit estricto (alguna etiqueta exclusiva de la clase) | 92.8 | 78.0 | 71.5 |
| dominio correcto por mayoría de etiquetas exclusivas | 87.4 | 77.5 | 70.9 |
| dominio de otra clase | 8.9 | 1.2 | 1.6 |
| precisión del dominio cuando responde | 90.9 | 98.5 | 97.8 |
| ruteo correcto | — | — | 100 |

Por corte, la cobertura crece con el contenido en los tres brazos: el especialista responde el 0, 5, 45 y 79 % con 25, 50, 100 y 200 imágenes por clase; la EHAM única, el 5, 54, 81 y 96 %. La ventaja de cobertura de la EHAM única es máxima en N=50 (49 puntos) y baja a 17.5 en N=200. Su dominio ajeno sube con N (0, 2.6, 4.9, 8.9 %); el de los especialistas queda entre 0 y 1.6 %.

Aquí la memoria única gana en cobertura y pierde en precisión, y las dos cosas salen del mismo mecanismo. El recall de un especialista exige que el latente de test quede contenido en su relación en las 64 coordenadas; el 21% de las imágenes de test caen fuera del soporte del especialista y no hay respuesta (es el rechazo residual del 25% que la tesis reporta en el hemisferio visual). La memoria única tiene la unión de los ocho soportes por coordenada, así que contiene al 96%. A cambio, el 9% de sus respuestas tienen dominio de otra clase: apple evocado como `vegetable`, `fruitwood` o `pear`, cup como `car`. Los especialistas se equivocan de dominio entre el 1 y el 2%. El ruteo visual de T-protocolo no comete errores (0 falsos ruteos, como en la tesis), pero rechaza el 19% en el directorio y otro 9% en el recall.

Lectura conjunta de los dos hemisferios: partir el contenido compra precisión y fidelidad, y cuesta cobertura. En texto→imagen la cobertura no se ve porque las pistas de texto son cortas y ambas arquitecturas contienen casi todas; en imagen→texto la pista tiene 64 coordenadas a 32 niveles y el containment estricto del especialista se nota.

## Por clase y ejemplos

`por_clase.md` desglosa clase, fidelidad y compat por clase y corte. Los errores de M se concentran donde se predijo: apple↔tomato (por `red` y `fruit`) y horse→cow (por `animal` y `mammal`); car, cow, cup, dog y pear quedan al 100%, igual que el especialista. `fig5_quimeras.png` muestra dos casos con la pista `red`: para la consulta de tomate M devuelve una manzana (compat 0.69, distancia 46 a una instancia real de tomate contra 17.9 del especialista) y para la de manzana una mezcla cuya instancia real más cercana es un caballo.

## Lo que este experimento no decide

- La especificidad fuera de dominio (P3): con 40 consultas la diferencia entre la EHAM única y los especialistas es una consulta. Lo que sí aparece es que el directorio deja pasar dos consultas que el contenido rechaza (`a piano with black and white keys` → dog, `a thunderstorm with heavy rain` → car, en las diez semillas): el índice de texto es relativo (16 niveles sobre 300 rasgos, exp10) y acepta pistas que la memoria de contenido no contiene. Es la fuga de la limitación (a) del reporte. La doble compuerta de contenido (el destino debe contener la pista; columna «acepta con compuerta» del README, campo `acepta_compuerta` en `raw/*_o0.json`) la cierra en este banco: el protocolo acepta 2 de 40 en los cuatro cortes, las dos originales con palabras del vocabulario (`food`, `table`), que también acepta el contenido. Lo que no se midió es cuánta cobertura legítima cuesta la compuerta sobre las 171 reservadas; en las 16 consultas de la etapa 8 no rechaza ninguna.
- El hemisferio imagen→texto con los cuatro cortes confirma que la cobertura del especialista sube con N (0 → 79 %), como en exp6, y que la de la EHAM única sube antes (5 → 96 %). No decide si siguen subiendo más allá de 200 imágenes por clase, que es el máximo del split.
- La comparación es a misma memoria y mismos datos (§3.1 y §3.2 de la propuesta). T usa ocho veces más celdas; ese costo no se compensa aquí con nada, se declara.
