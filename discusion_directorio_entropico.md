# El estatus del directorio en la MAE transactiva: revisión, evidencia y posición

**Fecha:** 30 de agosto de 2026
**Nota del 21 de septiembre de 2026:** tres frases de este documento (secciones 2.2, 4 y 5) decían que el directorio nunca llama a `recall`. Desde el 14 de septiembre `DirectoryMemory.recall_domain` sí lo hace (exp8, exp9), aunque ningún camino del protocolo lo usa. Se restringieron esas frases al ruteo y se añadió el párrafo de los dos lados de la relación; el resto queda como se escribió. Material y salidas consideradas en `revision_fase4_directorio_entropico_vs_metamemoria.md`.

**Contexto:** Los doctores observaron que la memoria directorio "parece la memoria asociativa de MINERVA", que "no se ve entrópica" y que "parece una tabla, no una heteroasociativa". Este documento recoge la revisión del código, un experimento nuevo (directorio unificado texto+visión) y la posición teórica que proponemos defender.

---

## 1. Qué computa el directorio (verificado en código)

`DirectoryMemory` envuelve una `HeteroAssociativeMemory4D` cuyo dominio derecho es la identidad del agente (one-hot, q=2).

**Registro** (`vectors_to_relation` + `abstract`): con la pista one-hot del agente ganador *k*, cada registro hace `rel[i, k, v_i, 1] += 1`. Esa rebanada es, literalmente, una **tabla de frecuencias valor-por-rasgo por agente**: T_k[i, v] = "cuántas veces el agente k registró el valor v en el rasgo i".

**Ruteo** (`predict` → `project`): score_j = Σᵢ T_j[i, vᵢ], con veto conjuntivo (cualquier rasgo-valor sin soporte → 0), dividido externamente por el número de registros del agente (calibración B1, un arreglo numpy fuera de la memoria) y argmax. Determinista, basado en cuentas.

**Efecto colateral:** cada registro también escribe `rel[i, j≠k, v, 0] += 1` para todos los agentes no dueños (producto exterior del one-hot). `predict` ignora esa columna, pero la relación carga esa masa estructural sin interpretación.

## 2. Veredicto sobre las tres críticas

### 2.1 "Es MINERVA" — mecánicamente no, pero la intuición señala algo real

MINERVA 2 guarda cada episodio como traza separada, su almacenamiento crece con las instancias y la abstracción ocurre al recuperar (eco ponderado por similitud). Nuestro directorio hace lo opuesto: funde las instancias al almacenar en una relación de tamaño fijo; las trazas individuales son irrecuperables. Esa diferencia es real y defendible (almacenamiento constante, propiedad anti-MINERVA). Sin embargo, conductualmente el ruteo es un argmax de frecuencias de ejemplares: su comportamiento entrada-salida se parece al de un clasificador por cuentas. La etiqueta es incorrecta; la conducta percibida, no.

### 2.2 "No es entrópica" — correcto, para el directorio tal como se usa

- El ruteo nunca consulta la entropía. `_update_entropies` corre, pero sus números no van a ninguna parte.
- Todos los parámetros operativos entrópicos están neutralizados en el ruteo: ι=κ=ξ=0 en el protocolo oficial (y el experimento 2 mostró κ inerte, ι destructiva). El ruteo **nunca llama a `recall`**: `predict`, `route` y `route_transactive` proyectan y toman argmax. La parte genuinamente entrópica de una MAE, el recall constructivo y estocástico (`reduce`/`choose` sobre la distribución de la celda), solo se ejercita en el directorio por la lectura inversa `recall_domain` (declarada el 14 de septiembre; exp8 y exp9), que no forma parte del protocolo. σ sigue sin importar, pero por otra razón: el muestreo por defecto (`sample_n_search_recall`) no lo usa; σ solo entra en `cue_recall` y en las rutas con prototipo.
- Con q=2 la distribución del dominio derecho por celda es una Bernoulli degenerada; casi no hay distribución sobre la cual ser entrópico.
- La `entropy()` que reportamos para el directorio es la entropía del **balance de cuentas entre agentes** —un diagnóstico de formación—, no la entropía de la relación en el formalismo MAE. La colisión de nombres invita a la lectura equivocada.

### 2.3 "Es una tabla, no heteroasociativa" — funcionalmente, en gran medida correcto

Con pistas derechas one-hot, la HAM 4D se factoriza en K tablas de cuentas 2D independientes: nunca se forma asociación *entre* agentes. Las capacidades que definen a una heteroasociativa (recall bidireccional agente→pista, reconstrucción, modulación de pesos desde una homo) no se usan en el directorio; solo proyecta y toma argmax. Nuestra propia ablación (experimento 1 v3) encontró que el único ingrediente irreducible es B1 = ÷cuentas: contabilidad externa, no maquinaria de memoria.

**Lo que sí se puede defender:**
- Almacenamiento de tamaño constante, independiente del número de instancias.
- El veto conjuntivo es contención relacional, no conteo ingenuo: es lo que da la especificidad perfecta (0% falsos positivos en el experimento 6). Una tabla de sumas plana no lo tendría.
- Conceptualmente, el directorio de Wegner *es* un índice ("quién sabe qué"). Un órgano con forma de tabla es discutiblemente la forma funcional correcta para ese papel. El carácter entrópico del sistema vive en las memorias de contenido (`mem_dom_H`, `mem_dom_L/R`), que sí hacen recall estocástico con σ y mostraron conducta distribucional real (experimento 5).

## 3. Experimento 7: directorio unificado texto+visión (364×32)

Se probó fundir `mem_dir_L` (texto, 300×16) y `mem_dir_R` (latentes, 64×32) en un solo directorio de 364 rasgos, con mitades indefinidas vía `np.nan` (la fila margen de la relación existe justo para funciones parciales y `project()` salta lo indefinido). Datos reales: banco de 80 queries / 236 tokens, 128 imágenes de entrenamiento y 20 de prueba por clase, lectura B1.

| Query | Unificado | Línea base (dos directorios) |
|---|---|---|
| Solo texto | 96.2% | 95.0% (`mem_dir_L`) |
| Solo imagen | 81.9% | 81.9% (`mem_dir_R`), idéntico en cada corte de formación |
| Pareada | **25.0%** | **97.5%** (fusión de ambos) |

- El +1.2 en texto viene de recuantizar a 32 niveles, no de la unificación.
- El colapso pareado es el veto conjuntivo: corre sobre todos los rasgos definidos, así que una mitad de imagen sin soporte mata una pista cuya mitad de texto rutea al 96%.
- **La interacción intermodal es imposible, analítica y empíricamente.** La relación es por (rasgo, agente), sin término rasgo-rasgo; mitades disjuntas no pueden tocarse. Las sondas cruzadas rechazan al 100% y los scores de texto bajo llenado pareado son bit-idénticos al llenado solo-texto (dif. máx. 0.0).
- El único canal de acoplamiento es el denominador B1 compartido, y es dañino: 1024 registros de imagen balanceados bajan el ruteo de texto de 96.2% a 90.0%, y 32 registros solo-manzana lo bajan a 87.5% *sin cambiar la relación en absoluto*.

**Conclusión:** el directorio unificado no transfiere nada entre modalidades y paga dos costos reales. Dos directorios separados es la arquitectura correcta — ahora con números.

Este resultado además alimenta la crítica de los doctores: ninguna representación compartida puede formarse precisamente porque el directorio es una tabla de cuentas por rasgo, sin ligadura relacional entre rasgos. Una heteroasociativa genuina tendría dónde vivir esa estructura; esta demostrablemente no.

## 4. Posición: el punto medio tiene nombre

El directorio no es MINERVA (abstrae al almacenar) y su ruteo no es entrópico (nunca opera sobre sus distribuciones). Lo que es: **una representación distribucional con una operación determinista en el sentido en que el protocolo la usa**. Acumula frecuencias, casi una estimación frecuentista de P(agente|pista), una tabla de transición si se quiere, y para rutear lo único que hace con esa distribución es el argmax. Entropía en potencia en el ruteo; en acto solo en la lectura inversa (exp8 y exp9: 9.3 niveles vivos por coordenada y 2.8 bits en el directorio visual), que es diagnóstica y sirve para medir qué guarda la relación.

La relación del directorio tiene dos lados, y el principio se aplica a cada uno. El lado izquierdo es la pista: icónico, con métrica. El derecho es la identidad: indicial, sin métrica (Peirce y Kripke, `discusion_marco_teorico_directorio.md` §2.3). Leer de izquierda a derecha es rutear; indeterminación en el lado derecho sería error, así que argmax. Leer de derecha a izquierda es describir; indeterminación en el lado izquierdo es generalización, así que muestreo. La misma relación es nítida en un sentido y entrópica en el otro. No es una inconsistencia: es la forma que toma el principio en una memoria con un lado de cada clase.

### Por qué no se puede meter todo en una hetero

La entropía de la MAE es funcional, no decorativa: vale porque el recall es constructivo. La memoria guarda una distribución por rasgo y recordar es muestrear de ella; la indeterminación significa algo porque el espacio de valores tiene estructura métrica —niveles vecinos se parecen— y entonces indeterminación = generalización.

El dominio derecho del directorio es **identidad**, y la identidad no tiene métrica ni vecindad: no existe "algo entre el agente manzana y el agente perro". Una distribución sobre nombres no admite recall constructivo; muestrear de ella no construye nada, solo se equivoca. En cuanto el dominio derecho es un one-hot, la hetero no falla: **degenera**, porque se le pide indeterminación sobre lo único que no la admite. Rutear es decidir, decidir es nombrar, y un nombre o es o no es.

En una línea: *la hetero asocia contenidos; el directorio designa*. La asociación vive de la incertidumbre; la designación tiene que ser nítida para servir a la coordinación. Un directorio entrópico fallaría en su única tarea, como una libreta de direcciones difusa.

### El punto medio no es indecisión: es arquitectura

La misma forma aparece en otros sistemas de memoria: en los sistemas complementarios del cerebro, contenido distribuido y superpuesto en cortex, e índice hipocampal disperso y separado a propósito —deliberadamente no entrópico, porque su función es apuntar sin interferir. La distinción dirección/contenido de von Neumann es la misma: el contenido puede ser difuso, la dirección tiene que ser exacta. Wegner responde "quién", y "quién" es discreto.

Otra lectura útil: el directorio no es memoria de experiencia sino **memoria de decisiones** —sedimento de asignaciones pasadas (por eso son cuentas). Las decisiones son discretas; la forma de tabla se hereda de ahí, no de una falla de diseño. Y la integración transactiva ocurre *a través del agente*, no dentro del directorio: el directorio es delgado a propósito (el experimento 7 lo confirma).

### El principio a proponer

> **La entropía pertenece al contenido; la decisión pertenece a la identidad.** Un sistema de memorias entrópicas necesita al menos un órgano no entrópico que las coordine. El precio de tener contenido distribuido e indeterminado es un índice nítido. El directorio muestra el *límite* del principio entrópico —dónde debe detenerse— y ese límite es una aportación, no un defecto.

### Caminos si se quiere incertidumbre operativa en el directorio (trabajo futuro, sin romper nada)

1. Rutear muestreando de los scores calibrados en vez de argmax ("creo que María sabe esto"): la incertidumbre se actúa, con costo en precisión.
2. Ruteo por coherencia (probabilidad/entropía, al estilo de `protos_coherence`) en lugar de cuentas crudas.
3. Dejar que el ruteo emerja del reconocimiento entrópico de las homo de cada agente (broadcast) y tratar el directorio como lo que ya es: la cristalización de esas decisiones.
4. Dominio derecho más rico que el one-hot (q>2, grados de conocimiento) si se insiste en que el directorio mismo porte distribución.

Aun así, el acto final sigue siendo nombrar a alguien. La entropía puede llegar hasta la puerta de la decisión; no puede cruzarla.

## 5. Recomendación de encuadre para los reportes

Presentar el *directorio* como una heteroasociativa completa cuyo protocolo solo ejercita la lectura determinista: *índice transactivo sobre el sustrato MAE; el ruteo proyecta y decide por argmax, sin recall; la lectura entrópica (`recall_domain`) existe y se usa para medir qué guarda el índice, no para coordinar*. El carácter entrópico del sistema en operación vive en las memorias de contenido. Renombrar o glosar la `entropy()` del directorio como "entropía del balance de especialización" para evitar el equívoco con la entropía de la relación.
