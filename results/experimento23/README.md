# Experimento 23 — la ambigüedad como respuesta

Memorias de la corrida balanceada del demo médico. Para cada imagen de test, S = conjunto de especialistas cuya memoria de contenido la reconoce (contención en las 64 coordenadas), ordenado por el principio de tamaño. Tres grupos: **desconocido** (|S| = 0), **claro** (|S| = 1) y **ambiguo** (|S| ≥ 2). Comparación a igual tamaño, imagen por imagen: kNN y el clasificador entrenado dan su top-|S|. Además, 4233 placas de tórax de test con ≥ 2 hallazgos (excluidas del demo). Script `run_experiment23_ambiguedad.py`; detalle en `resumen.txt` y `filas.json`.

## Cuánto se reparte en cada grupo y cuánto acierta el argmax

| nivel | \|S\| medio | desconocido | claro | ambiguo | argmax: claro → ambiguo | verdad dentro de S (ambiguo) |
|---|---|---|---|---|---|---|
| órganos (11) | 1.01 | 3.0 % | 93.6 % | 3.4 % | **97.3 → 69.9** | 95.4 % (2.1 candidatos) |
| piel (7) | 1.52 | 3.3 % | 57.6 % | 39.2 % | **88.0 → 58.2** | 95.7 % (2.4) |
| mama (2) | 1.21 | 3.2 % | 73.1 % | 23.7 % | **92.1 → 78.4** | 100 % (2.0) |
| tórax (14) | 8.74 | 0.7 % | 1.4 % | 97.9 % | 9.6 → 7.2 | 93.0 % (8.9) |

En el grupo desconocido el argmax del protocolo casi nunca acierta (2–19 %; mama 60 % con n = 5).

## Cobertura a igual tamaño de lista (imágenes con |S| ≥ 1)

| nivel | memoria | kNN top-\|S\| | clasificador top-\|S\| |
|---|---|---|---|
| tórax | 91.8 | 92.0 | 94.4 |
| órganos | 98.2 | 98.1 | 98.3 |
| piel | 93.7 | 92.7 | 94.0 |
| mama | 94.0 | 94.7 | 94.7 |

El conjunto del directorio (agentes con soporte en los directorios consultados) es peor que el de contenido: en tórax contiene la verdad en el 59.2 %.

## Placas con varios hallazgos (4233, |S| medio 8.2)

| contiene … de los presentes | memoria | azar del mismo tamaño | clasificador top-\|S\| |
|---|---|---|---|
| ≥ 1 | 94.7 | 81.6 | 95.7 |
| ≥ 2 | **72.1** | 46.3 | 74.3 |

## Predicciones

1. *El argmax falla mucho más en el grupo ambiguo.* **Se cumple** donde hay grupo claro: órganos 97.3 → 69.9, piel 88.0 → 58.2, mama 92.1 → 78.4. En tórax casi todo es ambiguo.
2. *Tórax con conjuntos grandes, órganos chicos.* **Se cumple:** 8.7 de 14 contra 1.01 de 11.
3. *En placas con varios hallazgos, S contiene a dos o más presentes más seguido que el azar.* **Se cumple:** 72.1 contra 46.3. El clasificador con la misma lista da 74.3.

## Lectura

- **La memoria distingue tres estados sin ningún umbral:** «no lo reconozco» (nadie contiene), «es esto» (uno contiene) y «es uno de estos» (varios contienen). El estado predice el error: en piel, el 57.6 % de las imágenes sale claro con 88 % de acierto. El 39.2 % sale ambiguo; ahí el argmax baja a 58 %, pero la lista de 2.4 candidatos contiene la verdad el 95.7 % de las veces. Es un diagnóstico diferencial que sale del mecanismo.
- **La lista no es mejor que la de un clasificador o un kNN del mismo tamaño** (diferencias de 0–2.6 puntos). Lo que aporta la memoria es **decidir el tamaño por sí misma**, imagen por imagen, con una razón legible (qué especialistas contienen la imagen). Un clasificador necesita un umbral calibrado aparte para saber cuándo dar uno y cuándo varios. La comparación contra predicción conformal, que es lo que se usa para eso, está en la sección siguiente.
- **En tórax la ambigüedad es honesta pero poco útil:** el sistema dice «es uno de 9 de 14» casi siempre. La evidencia de estos rasgos no distingue los hallazgos, y la memoria lo declara en lugar de inventar una respuesta.
- **Con varios hallazgos a la vez**, la lista contiene a dos o más de los presentes el 72 % de las veces (azar 46 %). La ambigüedad de la memoria refleja en parte la ambigüedad real de la placa.

## Contra predicción conformal a igual cobertura

Conformal partido (LAC) sobre el clasificador entrenado: puntaje 1 − p(verdad), calibrado con el split de validación de MedMNIST, que no se usó en ningún paso anterior. La cobertura objetivo es la que logra la memoria en test (verdad dentro de S, contando como fallo las listas vacías). Script `run_experiment23_conformal.py`; detalle en `conformal_resumen.txt` y `conformal.json`.

| nivel | cobertura memoria / conformal | tamaño medio memoria / conformal |
|---|---|---|
| tórax (14) | 91.2 / 91.3 | 8.74 / **5.34** |
| piel (7) | 90.6 / 91.9 | 1.52 / **1.33** |
| mama (2) | 91.0 / 89.1 | 1.21 / 1.03 |
| órganos (11) | **95.3** / 86.2 | 1.01 / 0.87 |

**Cobertura por clase en tórax** (memoria / conformal): sin hallazgo 94/99, infiltración 94/99, derrame 87/90, atelectasia 92/89; masa 83/**58**, nódulo 87/**68**, neumonía 27/**7**, consolidación 72/**33**, enfisema 74/**39**, fibrosis 63/**25**, engrosamiento pleural 76/**36**.
En piel: lesión vascular 34/**97**, dermatofibroma 57/**78**, queratosis benigna 93/83, melanoma 88/89. En mama, maligno 86/79.

Lectura:
- **A igual cobertura total, conformal da listas más cortas** (tórax 5.3 contra 8.7; piel 1.33 contra 1.52). En eficiencia promedio, el clasificador con conformal es mejor.
- **Pero conformal reparte la cobertura según la frecuencia de la clase.** En tórax alcanza el 91 % cubriendo casi siempre lo frecuente (sin hallazgo 99 %) y poco lo raro (neumonía 7 %, fibrosis 25 %, consolidación 33 %). La lista de la memoria cubre los hallazgos raros 2 a 4 veces más (neumonía 27, fibrosis 63, consolidación 72). Cada especialista tiene su propia envolvente, así que un hallazgo raro entra en la lista si su envolvente contiene la imagen, sin competir con la frecuencia de los demás. En medicina eso pesa: lo raro suele ser lo grave.
- **La excepción son las clases con muy pocos casos de llenado** (lesión vascular, 60; dermatofibroma, 48): ahí la memoria las deja fuera como «desconocido» y conformal las cubre mejor.
- **En órganos, conformal no alcanzó la cobertura pedida** (86.2 contra el 95.3 objetivo, con 2388 listas vacías). Su garantía supone que validación y test son intercambiables; aquí no lo son del todo (pacientes distintos por split). La memoria no depende de esa calibración.
- La comparación más exigente que falta es conformal **por clase** (Mondrian), que fuerza la misma cobertura en cada clase y competiría directamente con la propiedad de la memoria.
