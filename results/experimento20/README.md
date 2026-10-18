# Experimento 20 — principio de tamaño y rechazo de lo ajeno

Copia `MAE-TMS-medico`, sobre las memorias del demo médico (MedMNIST+ 128 px). Dos preguntas, con diseño y predicciones fijados antes de correr. BloodMNIST y OCTMNIST se descargaron de Zenodo (mismo registro, md5 verificado; fuera de git en `data/medmnist_ood/`).

## Parte 1 — leer el directorio con el principio de tamaño

B1 divide el puntaje de cada agente por su número de registros. El principio de tamaño (Tenenbaum y Griffiths 2001) trata la envolvente como una densidad uniforme sobre su soporte. Entre los agentes que contienen la pista, la log-verosimilitud es −Σᵢ log|soporte del agente en la coordenada i|: gana la envolvente más estrecha que la contiene. El recorrido es el de `route_transactive` y entre directorios se suman las verosimilitudes. El rechazo es idéntico **por construcción** (ningún agente contiene la pista), así que no se reporta como hallazgo. La reimplementación con B1 coincide con el ruteo oficial en el 100 % de los casos verificados (200 por nivel, 15 niveles). Script: `run_experiment20_size_principle.py`; detalle en `tamano_resumen.txt`.

| corrida · nivel | B1 | tamaño |
|---|---|---|
| completo · piel entregada a piel | 736/2005 | **1785/2005** |
| completo · mama entregada a mama | 3/156 | 37/156 |
| completo · modalidad, balanceado | 58.6 | **77.8** |
| completo · piel, balanceado | 46.3 | **62.5** (la corrida balanceada da 62.6) |
| completo · melanoma | 37/223 | **147/223** |
| completo · nevo | 1325/1341 | 1129/1341 |
| completo · tórax | todo «sin hallazgo» | igual |
| muestra y balanceado · todos los niveles | — | ± 1–2 puntos de B1 |
| balanceado · tórax, «sin hallazgo» | 13/11928 | 634/11928 |

Predicciones:
1. *En el completo, piel y mama vuelven a su modalidad y melanoma se recupera.* **Se cumple para piel y melanoma** (piel queda al nivel del registro balanceado). **No se cumple para mama** (24 % contra 94 % balanceado) **ni para tórax** (sin cambio).
2. *Empeoran los dominios heterogéneos.* **Se cumple donde son anchos** (completo: nevo 1325 → 1129). En el balanceado, donde no son más anchos, mejoran (nevo 1020 → 1105, sin hallazgo 13 → 634).

Lectura: el principio de tamaño **solo reordena a los agentes que contienen la pista**. Corrige el sesgo de ancho entre ellos: es lo que rompía piel y melanoma, y sin balancear el registro recupera lo mismo que el registro balanceado. Cuando la envolvente correcta es chica y no contiene la imagen (mama, 328 imágenes y 59 % de celdas cubiertas; los hallazgos de tórax frente a «sin hallazgo»), solo queda el agente grande y ninguna lectura la recupera. Hay dos fallas separables: **sesgo de ancho entre contenedores** (lo corrige la lectura) y **falta de contención de las envolventes chicas** (pide cobertura: más registros, variantes o tolerancia). Con anchos parecidos el principio de tamaño equivale a B1, así que no estorba.

## Parte 3 — ¿rechaza lo ajeno mejor que los detectores estándar?

Memorias de la corrida balanceada. La memoria tiene un único punto de operación. Cada detector estándar se fija para aceptar **la misma fracción de imágenes propias de test** que acepta la memoria, y se compara cuánto rechaza de lo ajeno. Detectores sobre los mismos latentes: kNN (similitud media a 5 vecinos del llenado), Mahalanobis (covarianza compartida) y MSP (probabilidad máxima de una regresión logística ajustada al llenado). Script: `run_experiment20_ood.py`; detalle en `ood_resumen.txt` y `ood_resultados.json`.

Ventaja metodológica a favor de los detectores: su umbral se fija con la distribución de las imágenes propias **de test**. El de la memoria se fija sin verlas.

**Nivel 1, modalidad** (la memoria acepta el 92.5 % de 42 372 propias). Rechazo de lo ajeno, con AUROC entre paréntesis:

| ajeno | memoria | kNN | Mahalanobis | MSP |
|---|---|---|---|---|
| fondo de ojo (1600) | 24.2 | 0.1 (0.563) | 49.3 (0.901) | **100.0** (0.999) |
| sangre (17 092) | 11.4 | 0.8 (0.538) | 8.0 (0.670) | **100.0** (0.999) |
| OCT (6000) | 5.9 | 11.1 (0.596) | 19.0 (0.648) | **99.8** (0.994) |
| tórax de otro hospital (5856) | 31.8 | **75.0** (0.936) | 56.1 (0.889) | 57.3 (0.870) |

**Dentro del dominio:**

| ajeno | memoria | kNN | Mahalanobis | MSP |
|---|---|---|---|---|
| hernia en tórax (110; nunca registrada ni vista por el encoder) | 0.0 | 1.8 | 0.0 | 0.0 |
| órgano fuera (leave-one-organ-out, media de 11) | 96.3 | **97.7** | 96.6 | 75.0 |

Lectura:
- **La memoria no rechaza lo ajeno mejor que los detectores estándar.** Lejos de su dominio (otras modalidades) rechaza poco (6–24 %) y MSP lo rechaza casi todo. En el cambio de hospital rechaza menos que todos (31.8 contra 56–75 %).
- **Dentro de un dominio** (un órgano que nunca registró) rechaza el 96 %, igual que kNN y Mahalanobis, y mucho más que MSP (75 %). Se comporta como un detector no paramétrico de cobertura, que es lo que es.
- **Un hallazgo nuevo dentro de una modalidad** (hernia) no lo detecta nadie: con estos rasgos se ve como una radiografía de tórax más.
- Por qué la memoria rechaza poco lo lejano: el nivel 1 usa rasgos genéricos (ResNet de ImageNet + PCA) y cuatro modalidades muy distintas registradas con 16 variantes. Las envolventes cubren mucho espacio (73–86 % de las celdas), y una imagen ajena cae dentro de alguna. MSP aprovecha que las cuatro modalidades se separan trivialmente: lo propio sale con probabilidad ≈ 1 y casi cualquier cosa ajena sale con menos.

## Lo que deja el experimento

- **Hallazgo positivo:** el principio de tamaño es una lectura con fundamento que corrige el sesgo de ancho de envolvente sin balancear el registro, y no estorba cuando los anchos son parecidos. Su límite queda identificado: no crea contención.
- **Hallazgo negativo:** «falla rechazando» no es una ventaja medible sobre los detectores estándar. La memoria rechaza como un detector de cobertura (bien un órgano ajeno dentro de su modalidad; poco una modalidad entera fuera de su espacio) y no mejor que kNN o Mahalanobis a igual aceptación. Es una propiedad útil porque viene integrada en el mismo mecanismo que rutea, pero no es superior.
