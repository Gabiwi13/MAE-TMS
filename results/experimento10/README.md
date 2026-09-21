# Experimento 10 — directorios perspectivales y ruteo encadenado

## Tesis
Vygotsky contra Hutchins. En el protocolo oficial cada agente registra todos los broadcasts, así que los ocho directorios son la misma relación y el TME es una novena copia (exp8). Eso no permite distinguir si la coordinación transactiva vive en cada agente (internalización perspectival, Vygotsky 1978) o en un artefacto compartido que el grupo consulta (pizarrón, Hutchins 1995). Aquí cada agente presencia solo parte de lo ajeno, los directorios divergen, y se mide si el grupo recupera el ruteo del pizarrón encadenando lo que cada uno sabe de los demás. Marco completo en `discusion_marco_teorico_directorio.md`.

## Método
- **Perspectiva.** El ganador siempre registra lo suyo. Un no-ganador registra el broadcast (a) al azar con probabilidad f ∈ {0, 1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 1}, tres semillas; o (b) solo si el ganador está a distancia ≤ r en un anillo de los 8 agentes, r ∈ {0, 1, 2, 3, 4} (r=4 es presenciar todo). f=0 y r=0 son agentes que solo se conocen a sí mismos.
- **Directorios.** `DirectoryMemory` tal cual, 8 de texto (300×16) y 8 de imagen (64×32) por condición, más un pizarrón por modalidad con todos los registros. Formación con maestro de registro = ground truth (como exp7/exp8): el objeto de estudio es el directorio, no la selección del ganador.
- **Datos.** Texto: banco de 8 clases (`eval_bank`), 30 consultas por clase para formar (240 consultas, 711 pistas) y las 171 restantes reservadas. Imagen: 128 latentes de train por clase para formar (caché de exp7) y 20 de test por clase. Lectura B1 (÷count, eps=1) y argmax. **xi=0 también en imagen**: con xi>0 los huecos tolerados se definen sobre el soporte de *todos* los agentes del directorio, así que lo que presenciaron los demás cambiaría la tolerancia del propio dominio y confundiría la curva (verificado: con xi=2 el ruteo del dominio propio *baja* al subir f).
- **Protocolos.** Cada consulta entra por cada uno de los 8 agentes (8 entradas × consultas).
  - *directo*: el agente de entrada consulta su directorio; sin soporte, rechaza (fase madura actual).
  - *encadenado*: sin soporte, pasa la consulta a los agentes que conoce (los que vio ganar algo), por orden de familiaridad (registros que les vio ganar), sin repetir; la consulta salta hasta que alguien tiene soporte o se agotan los conocidos. Saltos = consultas adicionales hasta responder.
  - *agregado*: pregunta a todos los que conoce y suma los scores calibrados; decide por argmax. La decisión es comparativa entre perspectivas.
  - *pizarrón*: el directorio único con todos los registros (referencia; equivale a f=1 directo).
- **Perspectiva medida.** Divergencia de Jaccard media entre los soportes (celdas con masa en la cara «ganó») de cada par de directorios; conocidos por agente (agentes con count>0); entropía media de cuentas.

## Resultados

### Imagen (test, 160 imágenes × 8 entradas)

| perspectiva | directo acierto / rechazo / error | encadenado acierto / rechazo / error | saltos | pizarrón | divergencia | conocidos |
|---|---|---|---|---|---|---|
| f = 0 · r = 0 | 10.2 / 89.8 / 0.0 | 10.2 / 89.8 / 0.0 | — | 81.9 | 1.00 | 1.0 |
| f = 1/64 | 10.2 / 89.8 / 0.0 | **81.9** / 18.1 / 0.0 | 3.56 | 81.9 | 0.83 | 7.2 |
| f = 1/16 | 10.4 / 89.6 / 0.0 | **81.9** / 18.1 / 0.0 | 3.53 | 81.9 | 0.53 | 8.0 |
| f = 1/4 | 32.4 / 67.6 / 0.0 | **81.9** / 18.1 / 0.0 | 1.87 | 81.9 | 0.19 | 8.0 |
| f = 1/2 | 62.1 / 37.9 / 0.0 | **81.9** / 18.1 / 0.0 | 0.50 | 81.9 | 0.09 | 8.0 |
| f = 1 | 81.9 / 18.1 / 0.0 | 81.9 / 18.1 / 0.0 | 0.00 | 81.9 | 0.00 | 8.0 |
| r = 1 | 30.7 / 69.3 / 0.0 | **81.9** / 18.1 / 0.0 | 1.89 | 81.9 | 0.80 | 3.0 |
| r = 2 | 51.2 / 48.8 / 0.0 | **81.9** / 18.1 / 0.0 | 0.64 | 81.9 | 0.58 | 5.0 |
| r = 3 | 71.6 / 28.4 / 0.0 | **81.9** / 18.1 / 0.0 | 0.13 | 81.9 | 0.25 | 7.0 |

El encadenado iguala al pizarrón en **todas** las condiciones con f>0 o r≥1, con cero errores, mientras los directorios difieren hasta en el 83% de sus celdas. El 18.1% de rechazo es el del pizarrón mismo (containment). El costo es el número de saltos: 3.5 con f=1/64, medio salto con f=1/2, y con anillo r=1 (cada agente conoce a dos vecinos) bastan 1.9 saltos. En la imagen, el ruteo directo con f<1/8 está en el piso del dominio propio (10%): nadie rutea lo que no presenció (exp4), y con directorios perspectivales eso es casi todo.

### Texto (consultas de formación, 240 × 8 entradas; reservadas, 171 × 8)

| perspectiva | formación: directo | formación: encadenado (saltos) | reservadas: directo | reservadas: encadenado (saltos) | pizarrón form. / res. |
|---|---|---|---|---|---|
| f = 0 · r = 0 | 12.5 (err 17.5) | 12.5 | 12.4 (err 8.9) | 12.4 | 96.7 / 93.6 |
| f = 1/64 | 33.6 (err 23.2) | 66.9 (err 33.1) · 1.11 | 27.4 (err 10.1) | 79.3 (err 20.7) · 1.87 | |
| f = 1/16 | 58.7 (err 20.4) | 77.2 (err 22.8) · 0.44 | 43.4 (err 12.9) | 80.9 (err 19.1) · 1.10 | |
| f = 1/4 | 87.2 (err 10.2) | 89.7 (err 10.3) · 0.04 | 82.2 (err 10.1) | 89.4 (err 10.6) · 0.10 | |
| f = 1/2 | 93.6 (err 6.1) | 93.9 (err 6.1) · 0.01 | 92.0 (err 6.9) | 93.0 (err 7.0) · 0.01 | |
| f = 1 | 96.7 (err 3.3) | 96.7 | 93.6 (err 6.4) | 93.6 | |
| r = 1 | 37.0 (err 24.3) | 64.8 (err 35.2) · 0.95 | 36.6 (err 16.5) | 73.9 (err 26.1) · 1.27 | |
| r = 2 | 61.1 (err 22.8) | 75.3 (err 24.7) · 0.27 | 60.0 (err 17.2) | 80.8 (err 19.2) · 0.38 | |
| r = 3 | 85.0 (err 10.8) | 89.2 (err 10.8) · 0.04 | 82.5 (err 11.0) | 88.9 (err 11.1) · 0.06 | |

### Protocolo agregado (pregunta a todos los conocidos y suma scores)

| perspectiva | texto formación: agregado (agentes consultados) | texto reservadas: agregado | imagen: agregado | pizarrón form. / res. / img |
|---|---|---|---|---|
| f = 1/64 | 80.6 (err 15.6) · 6.5 | 85.0 (err 7.6) · 6.6 | 73.8 (rech 26.2) · 7.3 | 96.7 / 93.6 / 81.9 |
| f = 1/32 | 86.5 (err 12.3) · 7.5 | 91.0 (err 6.9) · 7.5 | 79.8 · 7.8 | |
| f = 1/16 | 91.3 (err 8.7) · 8 | 91.9 (err 8.1) · 8 | **81.9** · 8 | |
| f = 1/8 | 93.5 (err 6.5) · 8 | 92.0 (err 8.0) · 8 | 81.9 | |
| f = 1/4 | 94.4 (err 5.6) · 8 | **94.3** (err 5.7) · 8 | 81.9 | |
| f = 1/2 | 96.1 (err 3.9) · 8 | 94.2 · 8 | 81.9 | |
| r = 1 (3 conocidos) | 55.4 (rech 16.0, err 28.6) · 3 | 56.4 (rech 22.8) · 3 | 51.2 (rech 48.8) · 3 | |
| r = 2 (5 conocidos) | 88.0 (err 12.0) · 5 | 87.1 (err 12.9) · 5 | 81.9 · 5 | |
| r = 3 (7 conocidos) | 96.5 (err 3.5) · 7 | 93.3 (err 6.7) · 7 | 81.9 · 7 | |

En texto el agregado sí alcanza al pizarrón: 91–92% en reservadas desde f=1/32 (pizarrón 93.6) y 94.3% con f=1/4. Esa última cifra no es una superación: la diferencia con el pizarrón son cuatro consultas de 171 en una de las tres semillas; es igualación dentro del ruido. Lo que le faltaba al encadenado no era soporte sino comparación: sumar los scores calibrados de varias perspectivas parciales reconstruye la decisión comparativa del directorio completo. El costo es consultar a todos los conocidos (hasta 8 agentes por consulta) en vez de saltar hasta el primero con soporte.

Con anillo r=1 el agregado es peor que el encadenado (55 contra 65–74): solo consulta a los tres agentes que conoce y no salta más allá, así que su alcance es la vecindad. El encadenado alcanza a todo el grupo por transitividad. Los dos protocolos son complementarios: el encadenado da alcance, el agregado da comparación.

## Hallazgos
1. **En imagen, la internalización perspectival basta.** Directorios que difieren en más del 80% de sus celdas, encadenados por familiaridad, rutean exactamente igual que el pizarrón (81.9%, cero errores) con f=1/64 y con anillo r=1. El TME sobra como artefacto en el hemisferio visual: el sistema transactivo es la red de directorios parciales (Vygotsky).
2. **En texto, la internalización basta si la consulta es comparativa.** El encadenado (primero con soporte decide) elimina el rechazo pero deja errores del 20–33% con f pequeño; el agregado (todos los conocidos suman scores) alcanza al pizarrón desde f=1/32 en reservadas (91.0 contra 93.6) y lo iguala con f=1/4 (94.3 contra 93.6, cuatro consultas en una semilla). La ventaja del pizarrón no era tener los registros sino tener a los competidores juntos para el argmax; sumar perspectivas recupera eso sin un artefacto central.
3. **La diferencia entre modalidades es de resolución del signo, no de arquitectura.** El mismo directorio, con 32 niveles sobre 64 rasgos, es un índice absoluto (una pista ajena no cabe: error 0 en todas las condiciones); con 16 niveles sobre 300 rasgos, es un índice relativo (una pista ajena cabe el 20% de las veces en un directorio que solo se conoce a sí mismo, y el argmax necesita competidores). Conecta con exp1 (B1 irreducible en texto) y exp7 (el denominador B1 como único acople).
4. **Alcance y comparación son cosas distintas.** El encadenado alcanza a todo el grupo por transitividad pero decide con la primera perspectiva; el agregado decide comparando pero solo llega hasta los conocidos directos (con anillo r=1 cae a 55%). Un protocolo transactivo completo necesita las dos operaciones.
5. **Perspectiva sin pérdida.** La divergencia de Jaccard entre directorios llega a 0.83 con f=1/64 sin que el acierto encadenado (imagen) o agregado (texto, desde f=1/32) baje de manera apreciable.
6. **El costo de la perspectiva es la consulta, no el error**: 3.5 saltos con f=1/64 en imagen, 0.5 con f=1/2; con vecindad estructurada (anillo r=1) 1.9. El agregado consulta a todos los conocidos siempre.
7. **La tolerancia xi es una propiedad del grupo, no del agente**: los huecos se definen sobre el soporte de todos los agentes del directorio, así que en directorios perspectivales cambia con lo que presenciaron los demás. Por eso esta corrida usa xi=0 en imagen.

## Archivos
- `results.csv` — media sobre semillas por (modelo, nivel, banco, protocolo)
- `results_raw.csv` — por semilla
- `fig1_azar.png`, `fig2_anillo.png` — acierto (líneas) y error (cruces) de los tres protocolos contra f o r, línea del pizarrón, saltos del encadenado y divergencia entre directorios
- `v1_sin_agregado/` — primera corrida (mismas semillas), sin el protocolo agregado

## Notas
- `run_experiment10_perspectival_routing.py` no modifica etapas ni memorias existentes; construye directorios nuevos por condición.
- El maestro de registro es la verdad de terreno; con el scoring de fase temprana (~88%) los directorios heredarían sus errores y el efecto de la perspectiva quedaría confundido.
- Los saltos se promedian solo sobre consultas respondidas; `consultas_en_rechazo` reporta cuántos agentes se consultaron cuando nadie tuvo soporte (en imagen, los 8).
