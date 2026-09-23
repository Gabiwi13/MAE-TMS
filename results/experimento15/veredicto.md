# Experimento 15: lectura de los resultados

**Corrida:** 23 de septiembre de 2026, `run_experiment15_arbiter.py`. Texto: N = 200, contenido oficial, directorios formados por semilla con las 240 de formación, 171 reservadas y 40 fuera de dominio, 10 semillas. Imagen: contenido oficial (Vc = 4), directorios con Vd = 1 y Vd = 16, 656 de test con el umbral de energía, 5 semillas. Las políticas se evalúan sobre las mismas decisiones guardadas. Tablas en `README.md`. El argmax reproduce exp11 (96.1 / 3.9 / 0.0) y exp13 (73.6 y 95.4 de ruteo).

## Criterio (§6)

**Refutado en las dos políticas.**

- **Árbitro por contenido (texto):** convierte 11.4 aciertos por semilla en errores y corrige 2 (de 171): acierto 96.1 → 90.6, error 3.9 → 8.8. El contenido solo, sobre los ocho agentes, hace lo mismo (90.6 / 9.4). No cambia la cobertura ni añade rechazos.
- **Margen (texto), δ = 0.2:** error 3.9 → 1.9 a costa de 4.3 puntos de acierto (96.1 → 91.8). La curva no tiene región barata: a cualquier δ el margen quita alrededor de un acierto por cada error que elimina (δ = 0.05: −0.6 de error por −0.5 de acierto; δ = 0.10: −1.0 por −1.8).
- **Fuera de dominio:** el árbitro baja las aceptaciones de 4 a 2 de 40, exactamente lo que ya hace la doble compuerta; el margen no las toca.
- **Imagen:** con Vd = 1 ninguna política cambia nada (donde el directorio rutea, el destino contiene la imagen). Con Vd = 16 el árbitro quita el único falso ruteo (`horse7-000-000` → `dog`: `dog` la acepta por el directorio pero ningún especialista le da soporte de contenido, así que el árbitro rechaza) y rechaza además 27 imágenes por semilla que el directorio ruteaba bien; la cobertura de punta a punta no se mueve (75.8 %) porque esas 27 tampoco producían recall. El margen no hace nada útil con ξ = 0: casi siempre hay un solo candidato.

## Lo que muestran los datos

**El índice compara mejor que el contenido.** Es la predicción P1 al revés, y coincide con lo que la tesis ya había medido desde otro lado: la fase temprana (argmax de `recognize_gated` sobre los ocho) acierta el 88 % y la fase madura con directorio B1 el 93.2 %. Aquí, entre los tres candidatos que el directorio ordena, la activación del contenido elige peor que el directorio: en 11 de cada 171 consultas el destino equivocado activa más que el correcto (las pistas compartidas activan fuerte en varias clases). El directorio, calibrado por cuentas, resuelve esos empates mejor que la memoria que guarda el contenido. Es el principio «la decisión vive en el índice» con números en contra de la alternativa.

**El error de texto no vive en empates estrechos.** Si viviera, el margen lo quitaría barato. La curva muestra que los errores tienen márgenes parecidos a los de los aciertos: para quitar los 3.9 puntos de error hay que abstenerse en el 16 % de las consultas (δ = 0.4) y perder 13 puntos de acierto. La abstención por margen no es una política útil para este directorio.

**En imagen el árbitro es la doble compuerta.** Rechaza lo que el contenido no contiene y nada más; corrige el falso de `horse7` porque ese error es del directorio densificado (Vd = 16) y no del contenido: la imagen tiene energía normal (el umbral de exp14 no la toca) y ningún especialista le da soporte, así que la compuerta de contenido la detiene. El costo de punta a punta es cero.

**Cota diagnóstica.** El contenido solo rutea el 93.1 % de las imágenes con cero errores, contra 73.6 % del directorio oficial: el directorio cuesta 19.5 puntos de cobertura y no compra precisión en imagen. Es la misma lectura de exp13 (con Vd = 16 el directorio llega a 95.4). En texto es al revés: el contenido solo pierde 5.5 puntos frente al directorio.

## Lo que no decide

- Un árbitro con otro comparador (por ejemplo la distancia del patrón recuperado a las instancias reales, que es lo que usa exp11 para juzgar clase) podría rendir distinto; aquí se probó la activación de `recognize_gated`, que es la operación de reconocimiento del sistema.
- El margen se midió sobre el score agregado B1; otra calibración (`sqrt`) o el margen sobre los directorios individuales no se probó.
