# Modelos computacionales que separan memoria de ítem y memoria asociativa, y su relación con una arquitectura conjunta-vs-marginal (MAE-TMS)

Nota de método: ~22 llamadas de búsqueda/lectura. Se pudo leer texto completo solo de los artículos de EAM/EHAM (arXiv HTML, PMC) y del abstract de Norman & O'Reilly 2003. De los artículos clásicos (Murdock, Eich, Pike, Humphreys et al., SAM, REM, Hopfield, Kosko) solo se verificaron los **registros bibliográficos**; la descripción de su mecánica interna viene de conocimiento previo y se marca como **[mecánica no verificada en texto en esta sesión]**. Ver tabla de verificación al final de la sección 6 (Gaps).

---

## 1. TODAM, CHARM y modelos de matriz/tensor: ¿componentes separados en un solo almacén?

### Takeaway
Los modelos distribuidos clásicos guardan la información de ítem y la asociativa como **términos distintos y explícitos**, aunque a veces sumados en un mismo vector (TODAM) o en almacenes de distinto orden (matriz/tensor). En ninguno la información de ítem se *deriva* de la asociativa: se escribe aparte, con su propio peso. Es lo más parecido a "homo + hetero" en la literatura clásica, pero la razón es que la operación asociativa (convolución, producto externo) no conserva de forma recuperable la información de ítem, cosa que sí ocurre en una tabla de conteos conjunta.

### Cited Findings
- Murdock, B. B. (1982). A theory for the storage and retrieval of item and associative information. *Psychological Review*, 89(6), 609–626. DOI 10.1037/0033-295X.89.6.609. Registro verificado; presenta TODAM (Theory of Distributed Associative Memory) — [Loterre/registro](https://loterre-skosmos.loterre.fr/P66/en/page/-CP362442-G); [Vanderbilt, cita](https://www.vanderbilt.edu/AnS/psychology/grads/diwadkar/research/semantic.htm)
- TODAM representa asociaciones como vectores de ítems "conjuntados" (convolución) — [Buchler, Light & Reder 2008 (PDF CMU)](https://www.cmu.edu/dietrich/psychology/memorylab/publications/08BuchlerLightReder.pdf)
- "The memory models differ in their assumption of whether item memory and associative memory are independent" (Yang et al. 2016, citando Murdock 1997 para TODAM y Gillund & Shiffrin 1984 para SAM) — [Yang et al. 2016, Learning & Memory 23(7):365–378, PMC4918786](https://pmc.ncbi.nlm.nih.gov/articles/PMC4918786)
- **[mecánica no verificada en texto en esta sesión]** En TODAM 1982 cada par (f, g) se añade a un único vector de memoria M como suma ponderada de tres términos: ítems (γ1·f + γ2·g) y asociación (γ3·f∗g), con olvido α·M. Reconocimiento de ítem = producto punto sonda·M; recuerdo con clave = correlación de la clave con M. Es decir: **componentes separados (ítem y asociación), almacén único (un vector)**. Cita del artículo: DOI 10.1037/0033-295X.89.6.609.
- Murdock (1993) TODAM2 (*Psychological Review*, 100(2), 183–203, DOI 10.1037/0033-295X.100.2.183) extiende a ítem, asociación y orden serial; Murdock (1997) añade contexto y mediadores (*Psychological Review*, 104(4), 839–862). **[registro bibliográfico no verificado en esta sesión; Yang et al. 2016 cita "Murdock 1997" para TODAM]**
- Pike, R. (1984). Comparison of convolution and matrix distributed memory systems for associative recall and recognition. *Psychological Review*, 91(3), 281–294 — [PhilPapers / registro citado](https://philpapers.org/s/Ray%20Pike) (DOI 10.1037/0033-295X.91.3.281, no comprobado en esta sesión)
- Humphreys, M. S., Bain, J. D., & Pike, R. (1989). Different ways to cue a coherent memory system: A theory for episodic, semantic, and procedural tasks. *Psychological Review*, 96(2), 208–233. DOI 10.1037/0033-295X.96.2.208 — [ModelDB/registro](https://modeldb.science/citations/68936)
- Descripción secundaria del modelo de matriz: las memorias son patrones de conexión definidos por el producto (externo) de vectores de ítem; la especificidad episódica viene de asociar la memoria con un vector de contexto, también por producto. Cita de Humphreys et al. (p. 209): "All memories are superimposed (summated) in this representation so that, without appropriate cuing, their individual identities are lost" — [Loterre, concepto "matrix model"](https://loterre-skosmos.loterre.fr/P66/en/page/-G0RH1Q4B-X)
- **[mecánica no verificada en texto en esta sesión]** En Humphreys, Bain & Pike (1989) el reconocimiento de ítem usa una memoria de segundo orden (contexto ⊗ ítem) y el reconocimiento asociativo/recuerdo con clave usa una memoria de tercer orden (contexto ⊗ ítem ⊗ ítem). Ambos tipos de traza se almacenan **explícitamente**; las tareas difieren en cómo se combinan las claves ("different ways to cue a coherent memory system").
- CHARM: Eich, J. M. (1982). A composite holographic associative recall model. *Psychological Review*, 89(6), 627–661. **[registro no verificado en esta sesión; mismo número que Murdock 1982]**. Usa convolución/correlación en una sola traza compuesta, como TODAM.

### Inferences
- En TODAM y CHARM la convolución f∗g dispersa la información de f y g: de la traza asociativa sola **no se puede leer** de forma limpia la familiaridad de f (el producto punto f·(f∗g) es aproximadamente ruido). Por eso esos modelos necesitan el término de ítem aparte. En una tabla de conteos conjunta (EAM hetero), en cambio, la marginal se obtiene **exactamente** sumando sobre la otra modalidad. El argumento clásico para "dos componentes" depende de que la codificación asociativa pierda la información de ítem; ese argumento **no se transfiere** a MAE-TMS, donde la homo es exactamente la marginal cuando todo llega en pares (lo que el autor ya comprobó).
- Lo que sí se transfiere: en TODAM los pesos γ1, γ2, γ3 son libres, de modo que ítem y asociación pueden tener **fuerza de codificación distinta** (atención a ítem vs a la relación). Una homo que difiere de la marginal solo si recibe datos o pesos distintos a la hetero es el análogo directo.
- Humphreys et al. (1989) muestran que el número de "almacenes" importa menos que *qué claves* se combinan; su modelo es "un sistema coherente" con trazas de distinto orden. Esto apoya presentar las homo como otro modo de interrogar el mismo contenido, no como un sistema independiente.

### Gaps
- No se leyó el texto de Murdock 1982/1993/1997, Eich 1982, Pike 1984 ni Humphreys et al. 1989; la descripción de ecuaciones viene de conocimiento previo. Verificar contra el PDF antes de citar fórmulas.
- No se encontró ningún análisis en estos modelos de "almacenar la marginal aparte cuando ya se tiene la conjunta": la pregunta no se plantea porque sus representaciones conjuntas no son tablas de frecuencias.

---

## 2. SAM, REM y disociaciones ítem vs asociativo (Hockley)

### Takeaway
SAM y REM codifican ítem y asociación dentro de las mismas imágenes/trazas (un solo almacén de trazas episódicas); la diferencia ítem/asociación es de *qué fuerza o qué rasgos* se consultan. Las disociaciones empíricas (curvas de olvido distintas) son la evidencia clásica que se usó contra modelos de un solo término, pero los resultados son mixtos y no se pudo verificar el contenido de Hockley (1992).

### Cited Findings
- Raaijmakers, J. G. W., & Shiffrin, R. M. (1981). Search of associative memory. *Psychological Review*, 88(2), 93–134 — [PDF en el sitio de Raaijmakers](https://raaijmakers.edu.fmg.uva.nl/PDFs/Raaijmakers%20and%20Shiffrin%201981.pdf) (registro confirmado por el enlace; contenido no leído)
- Shiffrin, R. M., & Steyvers, M. (1997). A model for recognition memory: REM—Retrieving effectively from memory. *Psychonomic Bulletin & Review*, 4(2), 145–166 — [ACNP](https://acnpsearch.tweb-dev.unibo.it/singlejournalindex/7318055); REM desciende de SAM y su idea central es la diferenciación: las repeticiones de un ítem se acumulan en una sola traza — [APS, discurso de Shiffrin](https://www.psychologicalscience.org/observer/models-of-memory-award-address-by-richard-m-shiffrin)
- En REM 1997 el foco es reconocimiento de ítem (efecto de fuerza de lista, efecto espejo); los resultados de búsqueda no mencionan reconocimiento asociativo — [ACNP](https://acnpsearch.tweb-dev.unibo.it/singlejournalindex/7318055)
- Hockley, W. E. (1992). Item versus associative information: Further comparisons of forgetting rates. *Journal of Experimental Psychology: Learning, Memory, and Cognition*, 18(6), 1321–1330 (DOI probable 10.1037/0278-7393.18.6.1321, no verificado) — registro mencionado en [Consoli 1996, tesis WLU](https://scholars.wlu.ca/etd/577)
- Evidencia mixta sobre olvido: "Studies have shown that associative memory or source memory declines to a greater extent than item memory", mientras que otros estudios, incluido Hockley & Consoli (1999), hallaron tasas similares hasta una semana — [Yang et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4918786)
- Consoli (1996, tesis supervisada en la línea de Hockley): sin diferencia de olvido entre ítem y asociación en una semana, pero más respuestas "remember" para pares — [scholars.wlu.ca/etd/577](https://scholars.wlu.ca/etd/577)
- Yang et al. (2016) atribuyen la memoria asociativa principalmente a la recolección y afirman que "the hippocampus is critical for and more involved in associative memory than in item memory" (señalando que Squire et al. 2007 lo disputan) — [PMC4918786](https://pmc.ncbi.nlm.nih.gov/articles/PMC4918786)

### Inferences
- Si ítem y asociación se olvidan a ritmos distintos (cualquiera sea el signo), una memoria que solo guarda la conjunta y deriva el ítem como marginal **no puede** reproducirlo: la marginal decae exactamente como la conjunta. Para modelar una disociación de olvido se necesita un almacén de ítem con dinámica propia (decaimiento, peso o tasa de aprendizaje distintos). Este es el argumento más directo de la literatura conductual a favor de homo separadas, y se aplica a MAE-TMS solo si las homo tuvieran decaimiento o pesos distintos de la hetero.
- SAM/REM no son un argumento a favor de dos almacenes: usan una sola estructura de trazas y separan ítem/asociación en el proceso de recuperación.

### Gaps
- No se pudo leer Hockley (1991, 1992) ni confirmar el sentido de su hallazgo. De memoria (no verificado): Hockley reportó que el reconocimiento asociativo decae más lento que el de ítem con ítems intercalados, lo que contradice la afirmación de Yang et al. sobre el sentido "habitual". **No citar el sentido del efecto sin leer el artículo.**
- No se verificó cómo REM trata el reconocimiento asociativo (extensiones posteriores, p. ej. de Criss & Shiffrin, no comprobadas).

---

## 3. Sistemas de aprendizaje complementarios (CLS): por qué dos sistemas

### Takeaway
En CLS los dos sistemas reciben **la misma entrada**; la justificación de tenerlos separados es que aprenden distinto (rápido/separado vs lento/solapado) y por eso producen señales con propiedades operativas distintas (recuerdo de detalles vs familiaridad escalar). No es un argumento de "conjunta vs marginal": la corteza no es una marginal del hipocampo.

### Cited Findings
- Norman, K. A., & O'Reilly, R. C. (2003). Modeling hippocampal and neocortical contributions to recognition memory: A complementary-learning-systems approach. *Psychological Review*, 110(4), 611–646. DOI 10.1037/0033-295X.110.4.611 — [Princeton, registro](https://collaborate.princeton.edu/en/publications/modeling-hippocampal-and-neocortical-contributions-to-recognition/)
- El hipocampo sostiene el recuerdo de detalles estudiados; la corteza del lóbulo temporal medial (MTLC) da una señal de familiaridad escalar: "The MTLC component cannot support recall, but one can extract a scalar familiarity signal from MTLC" — [Princeton, abstract](https://collaborate.princeton.edu/en/publications/modeling-hippocampal-and-neocortical-contributions-to-recognition/)
- Las simulaciones muestran que la similitud blanco-señuelo y la interferencia afectan de forma distinta a las dos señales, y examinan lesiones hipocampales parciales vs completas — [Princeton, abstract](https://collaborate.princeton.edu/en/publications/modeling-hippocampal-and-neocortical-contributions-to-recognition/)
- Una cita de 2010 en *Hippocampus* da por error "104:611-646"; el volumen correcto es 110 — [resultado de búsqueda sobre el registro APA](https://collaborate.princeton.edu/en/publications/modeling-hippocampal-and-neocortical-contributions-to-recognition/)
- McClelland, J. L., McNaughton, B. L., & O'Reilly, R. C. (1995). Why there are complementary learning systems in the hippocampus and neocortex. *Psychological Review*, 102(3), 419–457. **[registro no verificado en esta sesión]**. Argumento central (conocimiento previo): la neocorteza aprende lento con representaciones solapadas e intercaladas para extraer estructura sin interferencia catastrófica; el hipocampo aprende rápido con representaciones separadas (pattern separation) para episodios.

### Inferences
- Lo que CLS justifica es: **dos sistemas cuando difieren en tasa de aprendizaje o en grado de solapamiento de representaciones**. En MAE-TMS las homo y la hetero usan la misma regla de conteo sobre los mismos rasgos; por eso, con datos pareados, la homo coincide con la marginal y no cambia decisiones. CLS no da razón para mantenerlas *tal como están*; sí da razón si la homo se diseñara con otra dinámica (p. ej., aprendizaje más lento/acumulativo o más tolerante, como señal de familiaridad; la hetero como sistema rápido y específico de pares).
- La analogía funcional más defendible: homo ≈ "familiaridad de ítem" (¿esto lo he visto?) y hetero ≈ "recuerdo de la pareja". La literatura predice que el reconocimiento de ítem sobrevive cuando falla la asociación (lesión hipocampal parcial; Yang et al. 2016 sobre el rol del hipocampo en lo asociativo). En MAE-TMS el caso equivalente es justamente el de datos sin pareja: una vista que la homo reconoce y la hetero no puede nombrar (resultado B del commit 9ffe77c: 10 o 38 vistas más).
- Sobre reconocimiento asociativo con pares reordenados: los modelos de familiaridad pura tienden a fallar porque los dos ítems de un par reordenado son ambos familiares; un almacén solo de marginales no distingue AB de AD si A y D son familiares. Esto es un argumento a favor de **la hetero** (no puede eliminarse), no a favor de las homo. **[Inferencia; no se pudo leer la sección de Norman & O'Reilly sobre pares reordenados]**

### Gaps
- El PDF de Norman & O'Reilly (ccnlab.org) se descargó pero no se pudo extraer el texto (no hay pypdf en el entorno); no se verificaron sus predicciones sobre reconocimiento asociativo ni sobre list-strength.
- No se leyó McClelland et al. 1995.

---

## 4. Hopfield (auto-asociativa) y Kosko BAM (hetero-asociativa); arquitecturas que combinan ambas

### Takeaway
Hopfield es el modelo canónico auto-asociativo y BAM de Kosko el hetero-asociativo bidireccional; el propio artículo EHAM de Morales y Pineda se posiciona frente a ambos. No se encontró en esta sesión un modelo clásico que combine explícitamente una auto- y una hetero-asociativa con justificación formal.

### Cited Findings
- Kosko, B. (1988). Bidirectional associative memories. *IEEE Transactions on Systems, Man, and Cybernetics*, 18(1), 49–60. DOI 10.1109/21.87054 (título en plural según Crossref; algunas listas usan el singular) — [ModelDB](https://modeldb.science/citations/78671); [Wikipedia](https://en.wikipedia.org/wiki/Bidirectional_associative_memory); copia en el curso de Pineda: [turing.iimas.unam.mx](https://turing.iimas.unam.mx/~luis/cursos/MARE2024-2/lecturas/bidirectional.pdf)
- Hopfield, J. J. (1982). Neural networks and physical systems with emergent collective computational abilities. *PNAS*, 79(8), 2554–2558. DOI 10.1073/pnas.79.8.2554. **[registro no verificado en esta sesión]**
- Morales & Pineda (EHAM): "Hetero-associative neural networks models were explicitly introduced with Kosko's BAM model"; contrastan EHAM con BAM "in the same ways that EAM oppose auto-associative neural network-based models" — [arXiv 2411.02438 HTML](https://arxiv.org/html/2411.02438v1)

### Inferences
- En BAM la matriz de pesos W = Σ x yᵀ es una sola memoria hetero; la recuperación bidireccional (x→y→x) actúa como su propia "prueba" de consistencia. El procedimiento *sample and test* de EHAM (ver sección 5) es análogo: vuelve del objeto recuperado a la clave para validarlo. Ni BAM ni EHAM requieren una auto-asociativa para esa validación.

### Gaps
- No se buscaron arquitecturas híbridas auto+hetero específicas (p. ej. modelos de hipocampo CA3 auto-asociativo + CA3→CA1 hetero-asociativo, o las memorias multimodales tipo Hopfield moderno). Queda pendiente si se necesita.

---

## 5. Memoria Asociativa Entrópica (Pineda et al.): ¿justifican homo junto a hetero? ¿mismo espacio latente?

### Takeaway
Los artículos de EAM **no justifican** mantener memorias auto-asociativas junto a la hetero-asociativa ni discuten marginales. En EHAM (Morales & Pineda 2024/2025) se construyen dos memorias auto-asociativas (MNIST, EMNIST), pero solo se reportan como desempeño de referencia y para fijar el tamaño de tabla; el texto no dice que participen en la recuperación hetero. La palabra "latent" no aparece en EHAM. Corrección de cita: "Entropic associative memory for manuscript symbols" es Morales et al. 2022 en *PLoS ONE*, no Pineda, Fuentes & Morales 2021.

### Cited Findings
**Bibliografía verificada**
- Pineda, L. A., Fuentes, G., & Morales, R. (2021). An entropic associative memory. *Scientific Reports*, 11, 6948 (marzo 2021). PMC7994563; preprint arXiv 2009.13058 — [DOAJ](https://doaj.org/article/23c7c74af93a45528faef4a2a9da2700); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7994563); [arXiv](https://arxiv.org/abs/2009.13058v1). (DOI 10.1038/s41598-021-86270-7 de memoria, no comprobado)
- Morales, R., Hernández, N., Cruz, R., Cruz, V. D., & Pineda, L. A. (2022). Entropic associative memory for manuscript symbols. *PLoS ONE*, 17(8), e0272386. PMC9352019; arXiv 2202.08413 — [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9352019/); [RePEc](https://ideas.repec.org/a/plo/pone00/0272386.html). (Nombres completos de los coautores "Cruz" no verificados; el resultado de búsqueda lista "Morales, Hernández, Cruz, Cruz and Pineda".)
- Pineda, L. A., & Morales, R. (2023). Imagery in the entropic associative memory. *Scientific Reports*, 13, 9553. DOI 10.1038/s41598-023-36761-6 — [PMC10261031](https://pmc.ncbi.nlm.nih.gov/articles/PMC10261031/)
- Morales, R., & Pineda, L. A. (2024). Entropic Hetero-Associative Memory. arXiv:2411.02438 (2 nov 2024) — [arXiv](https://arxiv.org/abs/2411.02438v1)
- Morales, R., & Pineda, L. A. (2025). The missing cue problem in hetero associative memory retrieval. *Scientific Reports*, 15, 21850 — [IIMAS](https://turing.iimas.unam.mx/publications/the-missing-cue-problem-in-hetero-associative-memory-retrieval/) (texto de la versión publicada no leído)
- "Entropic associative memory for real world images", arXiv 2405.12500 (2024) — [arXiv HTML](https://arxiv.org/html/2405.12500v1) (autores no verificados; la atribución "Hernández et al." no se confirmó)

**Lo que dicen sobre homo/hetero**
- EHAM guarda pares (posiblemente de dominios o modalidades distintos) en una relación 4-D h ⊂ A×B×V×Z; la recuperación reduce la relación 4-D a un plano 2-D específico de la clave. Tamaño usado: "64×64×16×16" — [arXiv 2411.02438 (ar5iv)](https://ar5iv.labs.arxiv.org/html/2411.02438)
- "We created two auto-associative models using the weighted EAM system" y "the performances of the auto-associative memories are presented in Figure 2"; sus resultados se usan para elegir el tamaño de tabla (64×16) — [arXiv HTML](https://arxiv.org/html/2411.02438v1)
- El texto **no** dice que las memorias auto-asociativas participen en el reconocimiento o la recuperación hetero, ni que completen o validen la clave; tampoco habla de proyectar/marginalizar la tabla hetero ni de redundancia — [ar5iv](https://ar5iv.labs.arxiv.org/html/2411.02438)
- Describen EAM previa como "mostly auto-associative" y la hetero-asociación como forma más general; no argumentan que se necesiten ambas — [ar5iv](https://ar5iv.labs.arxiv.org/html/2411.02438)
- Codificación: "The architecture uses an autoencoder and classifier neural network"; ambos dominios se representan como funciones de 64 argumentos y 16 valores; no se dice si los codificadores son compartidos o separados; "latent" no aparece en el texto — [arXiv HTML](https://arxiv.org/html/2411.02438v1)
- Problema de clave faltante, tres métodos: aleatorio (muestra de la distribución de la columna), *sample and test* (cada objeto muestreado se lleva de vuelta al dominio fuente y su relación inversa se compara con la clave original; si falla la prueba de reconocimiento η, la distancia es infinita) y búsqueda local (descenso aleatorio). El arXiv lo llama "sample and search"; el resumen de la versión 2025 lo llama "search and test" — [ar5iv](https://ar5iv.labs.arxiv.org/html/2411.02438); [IIMAS](https://turing.iimas.unam.mx/publications/the-missing-cue-problem-in-hetero-associative-memory-retrieval/)
- Justificación cognitiva en EHAM: la operación de registro modela "a form of Hebb's learning rule" y el mecanismo "may support Bartlett's emphatic observation that remembering is a conventional and rationalized task"; "human memory" no aparece — [arXiv HTML](https://arxiv.org/html/2411.02438v1)
- Trabajo futuro en EHAM: solo métodos de recuperación mejores y si la recuperación puede verse como inferencia bayesiana; nada sobre combinar auto- y hetero-asociación — [arXiv HTML](https://arxiv.org/html/2411.02438v1)
- *Imagery* (2023) pasa de registros por clase a **un solo registro** para todo el dominio: "overcomes the problem of partitioning the memory in local regions, optimizes the use of the medium, and learning is now unsupervised"; memoria y clasificador son "independent modules"; la extensión hetero-asociativa queda como trabajo futuro; se declara consistente con el marco de Hintzman (Minerva); el autoencoder se considera memoria procedimental — [PMC10261031](https://pmc.ncbi.nlm.nih.gov/articles/PMC10261031/)
- *Manuscript symbols* (2022): registros AMR por clase con un registro auxiliar para la clave; compromiso de entropía: menos entropía da más precisión de reconocimiento y menos recall — [PMC9352019](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9352019/); [arXiv PDF](https://arxiv.org/pdf/2202.08413)

### Inferences
- La línea de Pineda llegó a la hetero-asociación **después** de la auto-asociación, y en EHAM las auto-asociativas aparecen como antecedente y calibración, no como componente de la arquitectura. Atribuir a estos artículos una justificación de "homo + hetero" sería incorrecto; lo honesto es decir que MAE-TMS toma esa combinación como decisión de diseño propia.
- El movimiento de *Imagery* (un registro único en vez de registros por clase, "ahora no supervisado") va en la dirección de **menos almacenes separados**, lo que en todo caso es un argumento a favor de quedarse con una sola tabla conjunta cuando los datos llegan pareados.
- El *test* de EHAM ya usa la propia tabla hetero en sentido inverso (y una prueba de reconocimiento η) para validar candidatos. Si la prueba η se hace sobre la relación hetero restringida por la clave, la homo no es necesaria para esa validación.

### Gaps
- No se pudo leer la versión publicada (Sci Rep 2025): podría diferir del preprint, incluido el papel de las auto-asociativas.
- No queda claro sobre qué relación se evalúa la prueba de reconocimiento η en *sample and test*; el resumen del lector no lo precisó.
- No se revisó si algún artículo de Pineda (p. ej. los de memoria con pesos/aprendizaje fonético) discute "mismo espacio latente" para ambas modalidades. En EHAM la palabra no aparece.

---

## 6. Argumentos formales: ¿cuándo conviene guardar marginales aparte?

### Takeaway
En aprendizaje automático, los modelos multimodales que deben funcionar con modalidades faltantes usan un componente **por modalidad** además del conjunto (p. ej. MVAE con producto de expertos), y lo justifican precisamente por datos sin pareja y supervisión incompleta. Con tablas de conteo, la homo solo aporta información cuando recibe datos que la hetero no recibe, o cuando tiene otra dinámica (decaimiento, peso, tasa). Eso coincide con lo que el autor ya midió.

### Cited Findings
- Wu, M., & Goodman, N. (2018). Multimodal Generative Models for Scalable Weakly-Supervised Learning. *NeurIPS 2018* (pp. 5575–5585); arXiv 1802.05335 — [NeurIPS proceedings](https://proceedings.neurips.cc/paper/2018/hash/1102a326d5f7c9e04fc3c89d0ede88c9-Abstract.html); [arXiv](https://arxiv.org/abs/1802.05335v3)
- El MVAE comparte parámetros entre todas las combinaciones de modalidades observadas; la red de inferencia correcta es un producto de expertos, con **un codificador por modalidad**; si falta una modalidad, su experto se omite; es "robust to incomplete supervision" y aplicable a aprendizaje débilmente supervisado; los enfoques previos o no aprenden la conjunta o requieren cómputo extra para datos faltantes — [NeurIPS abstract](https://proceedings.neurips.cc/paper/2018/hash/1102a326d5f7c9e04fc3c89d0ede88c9-Abstract.html); [arXiv](https://arxiv.org/abs/1802.05335v3)

### Inferences
- **Cálculo directo (no requiere fuente):** si la hetero acumula conteos N(v,z) solo de pares y la homo de imagen acumula N_I(v) de todas las imágenes, entonces N_I(v) = Σ_z N(v,z) + U(v), donde U son las imágenes sin pareja. Con U = 0 la homo es redundante (exactamente la marginal); con U > 0 contiene información que la tabla conjunta no puede representar sin inventar la otra mitad del par. Ese es el único caso en que la homo agrega algo con la misma regla de aprendizaje, y coincide con los resultados B y C2 del commit 9ffe77c.
- Razones adicionales para separar, todas condicionadas a que la homo **difiera** en algo de la marginal:
  1. Datos sin pareja (semi-supervisado; MVAE): sí, ya medido.
  2. Decaimiento u olvido distintos (disociaciones ítem/asociación, Hockley y Yang et al. 2016): solo si se implementa.
  3. Tasa/estilo de aprendizaje distintos (CLS): solo si se implementa.
  4. Capacidad y costo: la tabla hetero 4-D (64×64×16×16 en EHAM) crece como el producto; la homo 2-D es mucho más barata de consultar. Consultar la marginal precomputada es equivalente a guardar la homo, así que este argumento es de ingeniería, no de modelado. **[inferencia]**
  5. Señal de familiaridad independiente del par (Norman & O'Reilly): análogo funcional, pero en CLS la diferencia viene de la representación, no de marginalizar.
- Lo que una memoria **solo conjunta** no puede hacer: (a) aprender de ítems sin pareja sin imputar la otra modalidad; (b) olvidar ítem y asociación a ritmos distintos; (c) dar reconocimiento de ítem con una ruta que sobreviva al daño de la asociativa. Lo que una memoria **solo de marginales** no puede hacer: distinguir pares estudiados de pares reordenados (ambos ítems familiares) — por eso la hetero es imprescindible y las homo, con datos pareados, no.

### Gaps
- No se encontró un resultado formal en psicología matemática que trate explícitamente "almacenar la marginal de una tabla conjunta de frecuencias" como opción de diseño.
- Tabla de verificación de citas:
  - Verificadas en esta sesión (registro y al menos abstract/texto): Pineda, Fuentes & Morales 2021 (Sci Rep 11:6948); Morales et al. 2022 (PLoS ONE e0272386); Pineda & Morales 2023 (Sci Rep 13:9553); Morales & Pineda 2024 (arXiv 2411.02438); Morales & Pineda 2025 (Sci Rep 15:21850, solo abstract vía IIMAS); Norman & O'Reilly 2003; Wu & Goodman 2018; Yang et al. 2016.
  - Solo registro bibliográfico verificado: Murdock 1982; Humphreys, Bain & Pike 1989; Pike 1984; Raaijmakers & Shiffrin 1981; Shiffrin & Steyvers 1997; Kosko 1988; Hockley 1992 (título/revista/páginas; DOI no confirmado).
  - No verificadas en esta sesión (de memoria): Murdock 1993 (TODAM2), Murdock 1997, Eich 1982, McClelland, McNaughton & O'Reilly 1995, Hopfield 1982, Gillund & Shiffrin 1984, Hockley & Consoli 1999 (citada por Yang et al. 2016), autores de arXiv 2405.12500, DOI de Pineda et al. 2021.
