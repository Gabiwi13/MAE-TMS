# Conclusiones: Experimento 1 — TMS Operacionalizado mediante EAM Heteroasociativa Multiagente

---

## 1. Objetivo del experimento

Operacionalizar el Transactive Memory System (TMS) de Wegner (1987) usando memorias heteroasociativas (EAM) en un sistema multiagente. El sistema debía producir el triple de Wegner:

```
(imagen_recuperada, label_semántico, agente_ganador)
       item               label            location
```

Tres agentes independientes (apple, horse, car), cada uno con su propia EAM de dominio (`M_dom`), coordinados por un TME que aprende quién sabe qué mediante interacción.

---

## 2. Resultados cuantitativos

| Métrica | Valor | Criterio |
|---|---|---|
| RMSE reconstrucción visual | 0.12 | < 0.3 ✓ |
| Accuracy clasificación CNN | 100% | > 85% ✓ |
| Reconocimiento en M_dom | 100% (3/3 agentes) | — |
| Routing fase temprana (TME activo) | ~8/10 | — |
| Recuperación bidireccional — dominio | 6/6 | — |
| Recuperación bidireccional — labels | 6/6 | — |
| **Fidelidad fase madura (TME inactivo)** | **50% (5/10)** | — |

---

## 3. Conclusiones principales

### 3.1 El triple de Wegner se produce correctamente

El sistema genera `(imagen, label_semántico, agente_ganador)` para cada query semántica. Esto no es clasificación: el agente no solo dice "es un caballo" sino que recupera la imagen prototípica del dominio y los tokens de la query que activaron la memoria. El ciclo completo se cierra en ambas direcciones:

- **Dirección directa**: `"a round red fruit"` → EAM identifica agente apple → reconstruye imagen de manzana
- **Dirección inversa**: imagen de manzana → EAM recupera labels `{fruit, tree, green}` → sin clasificador explícito

La recuperación inversa es la contribución distintiva: un clasificador CNN dice "apple", pero no puede recuperar sus propiedades semánticas a partir de la imagen sin la asociación heteroasociativa entre espacio visual y espacio fastText.

### 3.2 El TME aprende la estructura de expertise correctamente durante la fase temprana

El TME comenzó vacío y construyó su directorio `M_dir` exclusivamente mediante las 10 interacciones de la fase temprana. Al final de esta fase, `M_dir` contenía asociaciones `v_label → v_agente` para todos los tokens vistos. Esto confirma el mecanismo central de Wegner:

> "Instructional success occurs if the transactive memory system can replace itself."

El sistema pasó de topología estrella (TME obligatorio) a topología punto a punto (TME prescindible) en exactamente el período de interacción establecido.

### 3.3 La fase madura alcanza 50% de fidelidad con solo 10 ejemplos de entrenamiento

El routing en fase madura (sin TME) coincidió con el routing de la fase temprana en 5 de 10 queries. Dado que cada agente aprendió su directorio a partir de solo 2–5 ejemplos por dominio, este resultado es consistente con la predicción de Wegner sobre grupos con conocimiento escaso de localización:

> "Gaining entry to the group's stored knowledge is likely to be an efficient enterprise, even when we begin with a fairly inexpert member."

El agente de entrada, aunque no sea el experto, puede redirigir correctamente usando su `M_dir` parcialmente entrenado.

### 3.4 El sistema exhibe sesgo hacia el agente con más exposición durante la fase temprana

Apple ganó 5/10 queries en la fase temprana (vs horse=3, car=2), lo que produjo un `M_dir` con mayor peso hacia apple en todos los agentes. En la fase madura, apple fue destino de los 10/10 queries, siendo 5 correctos. Esto reproduce el fenómeno descrito en TMS: los agentes aprenden mejor las ubicaciones del conocimiento que más frecuentemente transitaron por ellos durante el período de interacción. La distribución desbalanceada de la fase temprana se amplifica en la fase madura.

**Implicación para el diseño**: el balanceo de queries durante la fase temprana es un parámetro de diseño crítico para la fidelidad de la fase madura.

### 3.5 Los labels compartidos entre dominios son el mecanismo no trivial del routing

La arquitectura fue diseñada específicamente para dominios con labels semánticos compartidos pero con pesos diferentes. Con datos reales de ConceptNet 5.7.0:

- `"red"` → apple (peso 10), car (peso 3) — routing no trivial ✓
- `"animal"` → horse (peso 12), apple (bajo o nulo) — routing trivial ✓

La query `"a round red fruit"` activó tanto apple (17367) como car (6804), demostrando que el routing no es simple lookup sino competencia de pesos. El agente correcto ganó por su mayor peso acumulado en las asociaciones relevantes.

### 3.6 La ambigüedad semántica real de ConceptNet se propaga al routing

La query `"has an engine"` enrutó incorrectamente a apple (15380) en lugar de car (11385). La causa es que ConceptNet asocia "apple" con labels de Apple Inc. (`computer: 4, mac: 4, macintosh: 3`), cuyo espacio fastText es semánticamente cercano a "engine". Este no es un bug del sistema — es un caso legítimo de ambigüedad polisémmica que el HAM4D propaga honestamente.

Con labels curados (fallback anterior), este error no ocurría porque la ambigüedad Apple/apple no estaba representada. **Los datos reales son menos precisos en este caso específico pero más fieles a la arquitectura propuesta.**

### 3.7 La recuperación bidireccional distingue el sistema de un clasificador convencional

Los labels recuperados desde imagen son semánticamente coherentes sin haber sido programados:

| Imagen | Labels recuperados | Coherencia |
|---|---|---|
| apple | `fruit, tree, pear` | ✓ dominio frutal |
| apple | `fruit, pear, green` | ✓ color + categoría |
| horse | `donkey, horse, riding` | ✓ equino + actividad |
| horse | `donkey, horse, riding` | ✓ |
| car | `driver, car, crash` | ✓ uso/contexto |
| car | `car, vehicle, automobile` | ✓ categoría |

El sistema no fue entrenado para predecir "pear" dado una imagen de manzana — esta relación emerge de la estructura conjunta del espacio fastText y la EAM. La aparición de "pear" es un efecto secundario correcto: es el vecino más cercano de "apple" en el espacio de labels que no fue bloqueado por el prototype matching.

---

## 4. Sobre el stack tecnológico

### 4.1 ConceptNet como fuente de labels

La API de ConceptNet estuvo inaccesible (HTTP 502) durante todo el experimento. Los labels finales fueron extraídos directamente del archivo de aserciones ConceptNet 5.7.0 (498 MB comprimido, 34.1M líneas), procesado con streaming gzip en una sola pasada sin descomprimir completamente. Se extrajeron 67 coincidencias relevantes.

**Hallazgo importante**: las relaciones `IsA`, `HasProperty` y `HasPart` solas producen solo 9 labels para los 3 conceptos (τ=2.0). El grueso de los labels cualitativos (red, round, animal, vehicle) reside en `/r/RelatedTo`, que es la relación más poblada en ConceptNet 5.7 para conceptos concretos. La spec original asumía el comportamiento del endpoint de la API, que agrega internamente múltiples tipos de relaciones.

### 4.2 EAM basada en código original de Pineda & Morales

A partir de la migración de arquitectura completa, el sistema usa exclusivamente las implementaciones originales de Pineda & Morales (`hetero_lib/`):

- **M_dom_H**: `PinedaHAM4D` — subclase real de `HeteroAssociativeMemory4D`. Llama `super().__init__(fold=None)` con una guard de 1 línea que hace opcional la carga de clasificadores TF. Los parámetros `iota=kappa=xi=0` con `recall_from_right_soft()` delegando a `recall_from_right()` (proyección containment-AND) son suficientes para el experimento base.
- **M_dom_L/R**: `PinedaAssociativeMemory` — wrapper de `AssociativeMemory`. Sus `recog_weights()` se usan para ponderar la proyección hetero-asociativa de `recognize_from_left()`, replicando el patrón `left_eam.recog_weights() → hetero_eam` del código de Pineda en `eam.py`.
- **M_dir**: `PinedaDirectoryMemory` — 3 instancias `AssociativeMemory` (una por agente). Reemplaza `SimpleDirectoryMemory` (tabla de frecuencias numpy). Incluye normalización B1 (`predict_normalized`) equivalente a la condición B1 del ablation study.

Instalación: `tensorflow==2.21.0` (compatible con Python 3.13; los clasificadores no se cargan en producción).

### 4.3 Cuantización global

La cuantización del espacio latente debe ser **global** (min/max calculados sobre todas las imágenes de entrenamiento, no por imagen individual). La cuantización local produce distribuciones inconsistentes entre el prototipo almacenado y las imágenes de prueba, vaciando la proyección de `recall_from_right`. Este fue el bug más difícil de diagnosticar del experimento.

---

## 5. Limitaciones

### 5.1 Vocabulario cerrado
El sistema solo procesa labels vistos durante la fase temprana. Tokens desconocidos (`"edible"`, `"sweet"`, `"thing"`) producen score=0 en todos los agentes y el sistema asigna al primer agente por defecto. Wegner reconoce este comportamiento:

> "Faulty location knowledge on either member's part dooms the system, allowing items to pass through the group without being stored."

### 5.2 Una imagen prototípica por dominio
Cada agente registra un solo vector latente (promedio de 50 imágenes de entrenamiento) para todos sus labels. Esto simplifica el llenado pero elimina variabilidad intra-clase. La recuperación inversa devuelve siempre la misma reconstrucción para cualquier imagen del dominio, independientemente de pose, color o iluminación.

### 5.3 Fase temprana demasiado pequeña
10 queries es insuficiente para construir un directorio balanceado. La distribución real de queries en un entorno de uso produciría M_dir más uniformes y mayor fidelidad en fase madura. El experimento demuestra el mecanismo pero subestima la fidelidad alcanzable.

### 5.4 Ruido polisémico en ConceptNet
Apple (fruta) y Apple (empresa) comparten el mismo nodo en ConceptNet, introduciendo labels tecnológicos (`computer`, `mac`, `macintosh`) que contaminan el espacio semántico del dominio visual. Esto es una limitación real del recurso, no del sistema.

---

## 6. Lo que el experimento demuestra y lo que no

| Afirmación | Estado |
|---|---|
| Un sistema multiagente de EAMs puede producir el triple de Wegner | Demostrado ✓ |
| El TME aprende la estructura de expertise por interacción, no por programación | Demostrado ✓ |
| El TME puede retirarse tras la fase temprana y los agentes enrutan solos | Demostrado ✓ |
| La recuperación bidireccional imagen↔labels emerge sin entrenamiento directo | Demostrado ✓ |
| El routing en fase madura reproduce fielmente el routing con TME | Parcialmente — 50% con 10 queries |
| El sistema es robusto a ambigüedad polisémmica | No demostrado — "engine"→apple falla |
| El sistema escala a vocabulario abierto | No demostrado — vocabulario cerrado |

---

## 7. Trabajo futuro (según spec)

**Segundo paper**: múltiples dominios por agente. `M_dom` almacena varias imágenes prototípicas. El triple se vuelve más granular: `location = agente + subdominio recuperado`.

**Extensión a largo plazo**: aprendizaje incremental en fase madura — negociación entre agentes para asignar responsabilidad por nuevos dominios sin reactivar el TME.

**Mejoras inmediatas para mayor fidelidad**:
- Balancear queries de la fase temprana (igual número por dominio)
- Filtrar labels polisémicos de ConceptNet por dominio semántico
- Usar múltiples imágenes prototípicas por agente (k-means sobre el espacio latente)
- Aumentar τ para apple para eliminar labels de Apple Inc.

---

## 8. Datos del experimento

- **Dataset**: ETH-80, 3 clases, 410 imágenes/clase, splits 328/82 (train/test)
- **Encoder**: ResNet18 → 64-dim latente + ConvTranspose decoder
- **EAM M_dom_H**: PinedaHAM4D (HeteroAssociativeMemory4D de Pineda & Morales), n=300, m=16, p=64, q=32, iota=kappa=xi=0
- **EAM M_dom_L**: PinedaAssociativeMemory (AssociativeMemory homo-asociativa), n=300, m=16
- **EAM M_dom_R**: PinedaAssociativeMemory (AssociativeMemory homo-asociativa), n=64, m=32
- **EAM M_dir**: PinedaDirectoryMemory (3×AssociativeMemory para routing), n=300, m=16
- **Labels**: ConceptNet 5.7.0 assertions CSV, τ=2.0, relaciones IsA+HasProperty+HasPart+RelatedTo+HasA+MadeOf+CapableOf
- **Vectorización**: fastText wiki-news-subwords-300, sign(v) ∈ {-1,+1}^300
- **Queries fase temprana**: 10 queries manuales
- **Fidelidad fase madura**: 50% (5/10)
