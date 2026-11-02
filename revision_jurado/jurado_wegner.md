# Dictamen de jurado: fundamento teórico (sesión en la nube, 2 nov 2026)

Resumen fiel del último mensaje de la sesión «Jurado: Wegner, psicología y neurociencia» . La lista completa de literatura, con el estado de verificación de cada cita, está en esa sesión.

El revisor no pudo abrir nature.com, arXiv ni Crossref: comparó la EAM, la W-EAM y la EHAM con `src/hetero_lib/` y con resúmenes encontrados por búsqueda web. Marca cada cita así: V (verificó los metadatos), V+ (verificó también el contenido citado) y P (preprint).

## Veredicto
Aprobar con correcciones mayores al marco y a la discusión. La disciplina de fuentes en la parte EAM es ejemplar. El marco transactivo es delgado:
- la asignación de información aparece en cuatro versiones incompatibles;
- se atribuyen a Wegner decisiones que son del sistema;
- las analogías apuntan a memoria episódica, cuando el sistema guarda asociaciones de categoría.

Casi todo es redacción; dos puntos piden controles pequeños.

## Fortalezas
- Las atribuciones de la EAM coinciden con el código: la anulación conjuntiva en `project()`, κ solo en el reconocimiento de pares, `recall_with_sampling_n_search` como recuperación por defecto y la saturación en 2^16−1.
- El puente entre la memoria transactiva y la EAM se declara como aporte propio (02:277-279).
- Las limitaciones son francas, y las analogías se presentan como «estructurales, no causales» (06:170).
- Leer la familiaridad y el nombre de una sola memoria, con Plaut (2002), es una contribución al debate de uno contra dos almacenes.

## Observaciones mayores

### M1. La asignación de información aparece en cuatro versiones incompatibles
- **Dónde:** main:74-76 dice que se modelan los tres procesos; 02:292-296 dice que la asignación es el enrutamiento; 03:379-381 dice que la suma hace de asignación; 06:283-285 y 07:91-93 dicen que no se modela.
- **Problema:** Wegner (1995) la define como *assigning memory items to group members*, es decir, decidir dónde se guarda lo nuevo. En este sistema eso lo hace el experimentador, por etiqueta.
- **Corrección:** decir en el resumen, 01 y 02 que el sistema modela la actualización y la coordinación de la recuperación; retirar 03:379-381.
- **Opcional:** un experimento en fase madura donde una imagen nueva entre por cualquier módulo y se registre en el especialista.

### M2. Decisiones del sistema atribuidas a Wegner, y confusión entre 1987 y 1995
- **01:15-21:** «los miembros que la presenciaron» y «sin pasar por un intermediario» son rasgos del sistema.
- **02:285-287:** la actualización no ocurre solo «tras cada interacción exitosa»; también se aprende por estereotipos (Hollingshead y Fraidin, 2003) o porque alguien informa (Moreland y Myaskovsky, 2000).
- **02:298-301:** «sin coordinador central» no es parte de la definición.
- **02:281-282:** el resumen de 1995 no dice «red de directorios compartidos», y el término choca con los directorios perspectivales.
- **06:83:** cita 1987 para los mecanismos, cuando los tres procesos con nombre son de 1995; *directory updating* ya aparece en Wegner, Erber y Raymond (1991).
- **06:95-96:** la regla de anotar quién respondió es del sistema.
- **06:105-106, 04:176-178 y 07:49-52:** «comunicación distintiva» y «las señas del que pregunta» no son constructos de Wegner; lo más cercano es Hollingshead (1998) y la sobrecarga de pistas.
- **01:6-9 y 02:271-276:** falta la mitad de la definición de 1987 (p. 186): «a set of individual memory systems in combination with the communication that takes place between individuals».
- **Corrección:** una tabla en 2.3 con tres columnas (Wegner 1987, Wegner 1995 y decisión de EAM-TMS), y las frases citadas reescritas con «en este sistema».

### M3. La especialización está asignada, no emerge
- **Dónde:** main:62-63; 01:34-35 y 55-57; 07:9-10, 38-39 y 106-108.
- **Problema:** la etiqueta decide quién guarda qué, y el ganador temprano es en sustancia un clasificador generativo condicionado a la clase. Además, el codificador tiene una cabeza de entropía cruzada. Esto corresponde a la estructura asignada de Wegner, Erber y Raymond (1991).
- **Corrección:** reformular como «sin clasificadores discriminativos en las decisiones de enrutamiento y rechazo; la partición usa las etiquetas y el codificador tuvo supervisión auxiliar», y separar lo que emerge (el directorio) de lo que se impone (la especialización).

### M4. Las lecturas transactivas salen de un directorio compartido
- **Dónde:** 04:275-281 frente a 06:86-109 y 07:49-52.
- **Problema:**
  - Un directorio único y completo es lo contrario de lo que Wegner considera característico.
  - El mediador «sale del circuito» aunque su registro sea el directorio con que se enruta.
  - El paso a la fase madura lo fija el protocolo, no el grupo (01:22-23).
- **Corrección:**
  - Declarar en 06 que esas lecturas valen para un directorio compartido.
  - Repetir la curva de formación con directorios perspectivales.
  - Medir la convergencia entre directorios (*sharedness*; Austin, 2003; Brandon y Hollingshead, 2004).
  - Proponer un criterio interno de madurez.
  - Citar a Lewis (2004).

### M5. La invariancia al orden es una propiedad del modelo
- **Dónde:** 05:262-270 y 06:92-98.
- **Problema:** es la conmutatividad de la suma. En personas ocurre lo contrario: primeras impresiones (Asch, 1946) y estereotipos.
- **Corrección:** decir «por construcción» y discutir qué haría falta para que el orden importara: olvido, saturación o un prior.

### M6. La entropía del directorio no mide especialización
- **Dónde:** 02:313-322; 03:446-462; 06:51-54; 07:23-24 y 78-80.
- **Problema:** H_dir es la entropía de los ganadores: con un banco balanceado, un enrutamiento al azar también da unos 3 bits. Además es poco sensible: un desbalance de 186 frente a 112 sigue dando 2.974 bits.
- **Corrección:**
  - Reportar I(dominio; ganador) o H(ganador | dominio), normalizadas.
  - Ligarlas con las dimensiones de Lewis (2003) y Austin (2003).
  - Aclarar la tensión entre 02:130-132 y 02:316-319.

### M7. Las analogías de familiaridad y recuerdo apuntan a memoria episódica
- **Dónde:** 06:126-154 y 07:72-75.
- **Problema:**
  - El emparejamiento imagen–etiqueta es por turno (03:188-190): es coocurrencia de categoría, y la memoria no completa ítems concretos (05:592-595).
  - YR, las ratas de Fortin y el modelo perirrinal/hipocampal tratan de episodios.
  - La contención por coordenada se parece a un modelo de memoria compuesta y predice errores de conjunción (Reinitz et al., 1992).
  - En Mayes et al. (2004) no pudo confirmar «caras con nombres hablados» (06:140-141).
- **Corrección:**
  - Reorientar las analogías hacia la memoria semántica y la denominación: anomia, demencia semántica (Hodges et al., 1992; Rogers et al., 2004) y Bruce y Young (1986).
  - Para un solo almacén, citar a Murdock (1982), Humphreys, Bain y Pike (1989) y MINERVA 2 (Hintzman, 1984 y 1988).

### M8. La lesión produce una disociación simple que sale de la asimetría de las lecturas
- **Dónde:** 06:135-154 y 331-336; tabla de la lesión.
- **Problema:**
  - Nombrar exige un AND sobre 64 coordenadas y reconocer suma 17 valores: la diferencia de redundancia viene por construcción (Shallice, 1988; Dunn y Kirsner, 1988; Plaut, 1995).
  - Que con un 1 % de daño se pierda el nombre en el 92 % de las imágenes es lo contrario de la degradación gradual (Hinton y Shallice, 1991).
  - Dos lecturas de un mismo almacén apoyan «un almacén, dos procesos», no un solo proceso (Squire, Wixted y Clark, 2007).
- **Corrección:**
  - Repetir la lesión con un nombrar graduado y buscar la disociación inversa.
  - Comparar con daño difuso, como el Alzheimer (Hodges, Salmon y Butters, 1991).
  - Probar si las etiquetas derivan hacia supraordinadas como *fruit* o *animal*.

### M9. Faltan las analogías mejor respaldadas
Cada resultado de la tesis, con su vínculo en la literatura:

| Resultado | Vínculo |
|---|---|
| Errores entre frutas y entre animales | Déficits de categoría (Warrington y Shallice, 1984; Farah y McClelland, 1991; McRae et al., 1997; Tyler y Moss, 2001) |
| Etiquetas compartidas degradan el enrutamiento | Sobrecarga de pistas (Watkins y Watkins, 1975); Nairne (2002); efecto abanico (Anderson, 1974) |
| B1 corrige al módulo más activo | Tiempo de palabra frente a experticia (Bottger, 1984); CORI con colecciones dispares (Si y Callan, 2003); balance de carga en MoE (Shazeer et al., 2017) |
| El mediador temprano deja de hacer falta | Indexación hipocampal (Teyler y DiScenna, 1986); zonas de convergencia (Damasio, 1989); consolidación sistémica (McClelland et al., 1995; Frankland y Bontempi, 2005); trazas múltiples (Nadel y Moscovitch, 1997) |
| Directorio separado del contenido | Sparrow, Liu y Wegner (2011) |
| Reconocer sin nombrar | Sensación de saber (Reder y Ritter, 1992; Koriat, 1993); descarga cognitiva (Risko y Gilbert, 2016) |
| Rechazo | Decidir rápido «no sé» (Glucksberg y McCloskey, 1981) |
| Nombres frágiles | Paradoja baker/Baker (McWeeny et al., 1987); Young, Hay y Ellis (1985) |

### M10. «Los límites están en la representación, no en el mecanismo» va más allá de los datos
- **Dónde:** main:101-103 y 07:43 y 109-110.
- **Problema:** la tesis misma atribuye límites al mecanismo (06:178-181, 06:228-238, 06:331-336 y 05:592-595).
- **Corrección:** un control con los mismos vectores y otro decisor (centroide o kNN); si pear sigue cerca del 76 %, el límite es de representación. Mientras tanto, matizar.

### M11. Falta una sección de trabajo relacionado
- **Problema:** de 25 referencias, solo dos son de memoria transactiva. Faltan:
  - *mixture of experts* (Jacobs et al., 1991; Jordan y Jacobs, 1994; Shazeer et al., 2017; Fedus et al., 2022);
  - memorias asociativas (Willshaw et al., 1969; Kosko, 1988, BAM; Hopfield, 1982; Kanerva, 1988; Krotov y Hopfield, 2016; Ramsauer et al., 2021);
  - memoria transactiva computacional (Ren, Carley y Argote, 2006; Palazzolo et al., 2006);
  - sistemas multiagente (*contract net* de Smith, 1980, que es la fase temprana; agentes intermediarios de Decker, Sycara y Williamson, 1997, que equivalen al TME);
  - enrutamiento distribuido (*routing indices* de Crespo y Garcia-Molina, 2002; búsqueda federada de Callan, 2000).
- **Precedentes que conviene citar:** B1 y la partición los tienen. B1 se parece a la normalización por tamaño de colección y al balance de carga; la ventaja de partir se parece a la interferencia y a los estados mezcla (Amit et al., 1985; McCloskey y Cohen, 1989).
- **Corrección:** agregar un apartado 2.4, «Trabajo relacionado».

## Observaciones menores
- **«Hemisferio»** sugiere lateralización; conviene «vía» o «rama».
- **«Metadirectorio» y «todos los miembros mantienen»** (02:275-276) no se encuentran en Wegner.
- **«Un grupo recuerda más»:** matizar con la inhibición colaborativa (Weldon y Bellinger, 1997; Rajaram y Pereira-Pasarin, 2010).
- **B1:**
  - La puntuación cruda estima P(pista, k) y B1 estima P(pista | k).
  - Lo que B1 quita es un prior inflado.
  - Con tasas base desiguales, ese prior sería legítimo.
  - Precedentes: Church y Hanks (1990) y la fuerza asociativa de ACT-R (página por confirmar).
- **Punta de la lengua:** implica acceso parcial, así que habría que operacionalizarlo como la fracción de coordenadas con soporte. Para la sensación de saber, medir si la familiaridad predice un enrutamiento correcto.
- **Aviso de analogías:** llevar «estructurales, no causales» al inicio de 6.4 y 6.5: los módulos no son personas.
- **«Recordar es muestrear»:** apoyarlo en la memoria constructiva (Schacter y Addis, 2007) o atribuirlo a Pineda y Morales.
- **Lecturas marginales:** la identidad vale mientras no se sature ninguna celda; decirlo.
- **Pineda, Fuentes y Morales (2021):** tiene una Author Correction (agosto de 2021, PMC8385088) que corrige las figuras 3 y 4.
- **ConceptNet:** aclarar que el artículo de 5.5 es la cita canónica de los datos 5.7.
- **02:252-255 y 02:257-260:** merecen ecuación o página exacta.
- **«Transactive Memory Expert»:** confunde, porque en esa literatura los expertos son los especialistas.

## Literatura prioritaria (★)
- **Memoria transactiva:**
  - Wegner (1995), Social Cognition 13(3):319-339 (V+); Wegner (1987), pp. 185-208 (V+).
  - Wegner, Erber y Raymond (1991), JPSP 61(6):923-929 (V+).
  - Moreland y Myaskovsky (2000), OBHDP 82(1):117-133 (V+).
  - Lewis (2003), J. Appl. Psych. 88(4):587-604 (V).
  - Austin (2003), J. Appl. Psych. 88(5):866-878 (V).
  - Brandon y Hollingshead (2004), Organization Science 15(6):633-644 (V).
- **Memoria transactiva computacional:** Ren, Carley y Argote (2006), Management Science 52(5):671-682 (V); Palazzolo et al. (2006), Communication Theory 16(2):223-250 (V).
- **Sistemas multiagente:** Smith (1980), IEEE Trans. Computers C-29(12) (V); Decker, Sycara y Williamson (1997), IJCAI (V+).
- **Enrutamiento y búsqueda federada:** Crespo y Garcia-Molina (2002), ICDCS (V); Si y Callan (2003), SIGIR (V+).
- **Mixture of experts:** Jacobs, Jordan, Nowlan y Hinton (1991), Neural Computation 3(1):79-87 (V); Jacobs, Jordan y Barto (1991), Cognitive Science 15(2) (V); Shazeer et al. (2017), ICLR (V).
- **Memorias asociativas:** Willshaw et al. (1969), Nature 222 (V); Kosko (1988), IEEE SMC 18(1) (V); Krotov y Hopfield (2016) (V); Ramsauer et al. (2021) (V).
- **Psicología de la memoria:**
  - Murdock (1982), Psych. Rev. 89(6) (V); Humphreys, Bain y Pike (1989), Psych. Rev. 96(2) (V); Hintzman (1984) (V).
  - Reinitz, Lammers y Cochran (1992) (V+); Watkins y Watkins (1975) (V).
  - Bruce y Young (1986) (V); McWeeny et al. (1987) (V+).
- **Neuropsicología y neurociencia:**
  - Shallice (1988) (V); Dunn y Kirsner (1988) (V); Plaut (1995) (V).
  - Warrington y Shallice (1984) (V); Hodges et al. (1992) (V+); Rogers et al. (2004) (V).
  - Teyler y DiScenna (1986) (V); Damasio (1989) (V).

## Preguntas para la defensa
1. ¿Cuál de las cuatro versiones de la asignación es la correcta?
2. ¿Qué parte del sistema emerge y cuál se impone?
3. ¿Se reproducen las curvas con directorios perspectivales, y convergen entre sí?
4. ¿Qué criterio interno indica que llegó la madurez?
5. ¿Cómo distingue H_dir un grupo especializado de un enrutamiento al azar?
6. ¿Sigue siendo correcta B1 con tasas base desiguales?
7. ¿Qué experimento separa representación de mecanismo?
8. ¿Por qué comparar con YR y Fortin y no con la memoria semántica?
9. ¿Se mantiene la disociación con un nombrar tolerante? ¿Hay disociación inversa?
10. ¿Las etiquetas derivan hacia supraordinadas?
11. ¿Cómo se relacionan los errores con los déficits de categoría?
12. ¿Produce el sistema errores de conjunción?
