# Plan de implementación: auditoría académica de proyectos LaTeX

Especificación para ejecutar con Codex u otro asistente de código. Versión 1.0, 2 de noviembre de 2026.

## 1. Objetivo y contexto

Construir una herramienta local que audite un reporte técnico de licenciatura de aproximadamente 140 páginas, dividido en capítulos LaTeX, con bibliografía y una declaración de uso de IA ya incorporada. Producir hallazgos verificables sobre redacción, consistencia científica, referencias e integridad documental, sin alterar el manuscrito.

La herramienta ayudará al autor a revisar el trabajo; no certificará autoría, ausencia de plagio ni aceptación institucional. Separará explícitamente similitud, clasificación de IA, marcas estadísticas, inspección del archivo y evaluación académica.

Nombre provisional del comando: `texaudit`. Elegir un nombre definitivo tras comprobar colisiones en el entorno. No publicar paquetes ni crear servicios externos como parte de este encargo.

## 2. Decisiones de arquitectura

- Python como núcleo local, CLI como interfaz inicial y HTML autocontenido como reporte navegable.
- Analizador sintáctico de LaTeX con ubicaciones originales, complementado por reglas puntuales. No depender exclusivamente de expresiones regulares.
- Representación intermedia estructurada que conserve procedencia, contexto y cobertura de extracción.
- Comprobaciones deterministas separadas de la revisión contextual del agente.
- Sin API de modelos obligatoria. Preparar paquetes revisables por Codex u otro asistente de código e importar sus observaciones con un esquema validado.
- PDF como artefacto de presentación; fuentes LaTeX como origen principal para trazabilidad. Usar ambos cuando estén disponibles.
- Configuración versionada y resultados de auditoría fuera del árbol de fuentes del manuscrito, salvo decisión expresa del autor.
- Primera versión sin base de datos: JSON y archivos de configuración son suficientes. Sin aplicación web, usuarios, servidor, contenedores ni infraestructura remota obligatorios.

## 3. Alcance y exclusiones

### Incluido

1. Descubrimiento de estructura y dependencias del documento.
2. Citas, referencias cruzadas y consistencia bibliográfica interna.
3. Repeticiones y características medibles de prosa.
4. Revisión contextual por capítulo y entre capítulos.
5. Consistencia de términos, notación y cifras identificables.
6. Inventario de metadatos y anomalías del PDF y fuentes.
7. Verificación externa opcional de referencias y afirmaciones.
8. Reportes, decisiones del autor y comparación entre versiones.

### Excluido

- Clasificar un texto como humano o IA, generar porcentajes de humanidad o predecir Turnitin.
- Inferir el algoritmo privado de un proveedor a partir de sus resultados.
- Sustituir bases privadas de similitud o emitir un dictamen de plagio.
- Afirmar que se ha verificado una referencia por encontrar únicamente su título o DOI.
- Aplicar cambios al manuscrito durante una auditoría.

## 4. Inspección inicial del repositorio

Leer primero AGENTS.md y las instrucciones equivalentes existentes. Identificar archivo principal, motor, herramienta de compilación, codificación, estructura, comandos personalizados, bibliografía, clases, paquetes, diagramas y origen de resultados. Registrar el estado del árbol de trabajo sin exponer secretos.

Si hay varios documentos principales, presentar candidatos y continuar con inventario general; no elegir silenciosamente uno para una auditoría definitiva. Preferir configuración existente y convenciones del proyecto. Si no hay repositorio, mantener un área separada para el programa y sus salidas.

Generar `project_inventory.json` con: archivos incluidos, dependencias, archivos encontrados pero no incluidos, bibliografías, activos, herramientas disponibles, configuración de compilación y problemas de resolución. Respetar `includeonly`, importaciones y rutas del proyecto; registrar soporte parcial cuando se usen mecanismos no implementados.

## 5. Representación intermedia y mapa de origen

Construir nodos para capítulo, sección, párrafo, cita, referencia, ecuación, tabla, figura, título y comentario. Cada nodo debe conservar:

- Identificador, tipo, archivo relativo y hash del archivo.
- Inicio y fin en el original, usando offsets Unicode documentados y líneas/columnas de base uno.
- Texto original y texto normalizado para análisis; nunca sustituir uno por otro.
- Sección jerárquica, etiquetas y claves de citas asociadas.
- Indicadores de cita textual, ecuación, código, bibliografía y contenido no interpretado.
- Calidad de extracción y motivo de cualquier omisión.

Mantener un mapa entre caracteres normalizados y rangos del original. Los textos concatenados desde varios nodos deben conservar todos los rangos involucrados. Detectar `%` escapado, comentarios, comandos anidados, argumentos opcionales, `verbatim`, `minted` y entornos matemáticos. No ejecutar TeX para extraer macros.

Permitir configurar macros de contenido: por ejemplo, comandos de énfasis que conservan su argumento y comandos de glosario que requieren tratamiento especial. No expandir macros arbitrarias. Los comandos desconocidos se contabilizan en cobertura y se muestran para revisión.

Para grandes proyectos, informar cobertura por archivo y tipo de contenido. Distinguir cantidad de texto procesado, archivos visitados y revisión semántica efectivamente terminada. Un archivo visitado no equivale a un capítulo revisado.

## 6. Catálogo de reglas y evidencia

Crear un catálogo versionado. Cada regla tendrá ID, descripción, categoría, implementación, alcance, exclusiones, parámetros, fuente si corresponde, fecha de consulta y limitaciones. Clasificar su fundamento:

- **Proveedor:** capacidad descrita oficialmente, identificando producto y alcance.
- **Investigación:** característica evaluada en un estudio, identificando corpus, idioma y fecha.
- **Editorial:** heurística de esta herramienta para mejorar el documento, sin atribuirla a detectores comerciales.

No convertir los grupos anteriores en niveles de certeza de autoría. Una regla editorial puede detectar un error real; una función de proveedor puede producir falsas alarmas.

### Catálogo mínimo

| ID | Comprobación | Salida y cautelas |
|---|---|---|
| STRUCT-001 | Include inexistente, ambiguo o cíclico | Ruta y cadena de dependencias; admitir documentos incompletos. |
| XREF-001 | Etiqueta duplicada | Todas las definiciones y usos. |
| XREF-002 | Referencia sin destino | Comando y clave; considerar comandos configurados y referencias externas. |
| BIB-001 | Cita sin entrada | Cita exacta, archivo y línea. |
| BIB-002 | Clave bibliográfica duplicada | Comparar bases y entradas. |
| BIB-003 | Referencia no citada | Observación informativa; considerar `nocite` y bibliografías por capítulo. |
| BIB-004 | Campos bibliográficos faltantes | Requisitos según tipo, no campos universales. |
| BIB-005 | Entradas posiblemente duplicadas | DOI normalizado o combinación de título/autores/año; revisión humana. |
| EDIT-001 | Párrafo repetido | Duplicación exacta normalizada; excluir citas y plantillas legítimas. |
| EDIT-002 | Párrafos casi repetidos | Similitud configurable, fragmentos y motivo; no confundir tema compartido con copia. |
| EDIT-003 | Muletillas y comienzos reiterados | Frecuencia absoluta y por mil palabras, con contexto. |
| EDIT-004 | Distribución de longitudes | Descriptiva por capítulo; sin umbral de autoría. |
| EDIT-005 | Marcadores pendientes | TODO, claves provisionales, texto de plantilla; excluir ejemplos intencionales. |
| TERM-001 | Variantes terminológicas | Glosario y contexto; respetar sinónimos y definiciones. |
| CLAIM-001 | Afirmación que requiere respaldo | Observación del agente, no error confirmado sin consulta. |
| RESULT-001 | Cifra contradictoria | Dos ubicaciones y contexto experimental antes de concluir. |
| UNICODE-001 | Caracteres inusuales | Punto de código, nombre, cantidad y contexto legítimo posible. |
| PDF-001 | Metadatos efectivos | Inventario y diferencias frente a configuración fuente. |
| PDF-002 | Posible texto no visible | Evidencia de objetos/posición/renderizado; marcar ambigüedad. |
| BUILD-001 | Advertencias de compilación | Separar referencias, fuentes y maquetación. |

## 7. Patrones de redacción: medición y revisión

Separar bibliografía, citas literales, fórmulas, código, captions y anexos cuando corresponda. Informar denominadores y ámbitos. Distinguir repeticiones dentro de un capítulo de las esperables entre resumen e introducción.

Medir n-gramas de palabras, conectores configurables, comienzos de oración, similitud de párrafos y distribución de longitud. Conservar acentos para presentación; documentar normalizaciones usadas para comparar. Elegir candidatos de duplicación mediante índices o shingles para evitar comparar todos los pares innecesariamente.

Las observaciones contextuales deben buscar: vaguedad, énfasis sin respaldo, transiciones sin relación lógica, conclusiones reiteradas sin interpretación, uniformidad que perjudique lectura, cambios de registro y residuos conversacionales. No perseguir variación artificial, añadir errores ni sustituir términos técnicos para aparentar autoría humana.

No usar perplejidad, entropía o diversidad léxica como clasificador de autoría. Si se incorporan métricas descriptivas futuras, indicar modelo, definición, población de referencia y límites. No presentar cifras universales de aceptación.

## 8. Revisión contextual con Codex u otro asistente de código

### Paquetes por capítulo

Generar archivos de lectura con: texto, ubicaciones, glosario vigente, etiquetas, citas, tablas relevantes y candidatos detectados por reglas. Mantener acceso al original para verificar ecuaciones y macros. Dimensionar lotes según el contexto disponible del agente, sin fragmentar argumentos arbitrariamente.

Primera pasada: revisar estructura y argumentos. Segunda: examinar candidatos y relaciones con tablas, citas y resultados. Evitar que la lista automática limite toda la revisión. Registrar capítulos, secciones y nodos revisados y pendientes.

El agente devuelve observaciones JSON validadas. El importador comprueba que los archivos y rangos existen, que el fragmento coincide y que la versión del proyecto es compatible. Rechazar o poner en cuarentena observaciones con referencias inventadas o caducadas. No confiar en JSON por el solo hecho de ser sintácticamente válido.

### Revisión transversal

Construir matrices trazables:

1. Objetivo → procedimiento → evidencia → conclusión.
2. Experimento → conjunto de datos → partición → configuración → métrica → resultado → limitación.
3. Término/símbolo → definición → usos.
4. Afirmación principal → fuente o experimento que la respalda.

Para contradicciones, incluir al menos dos pasajes cuando existan. No tratar resúmenes generados por el agente como sustitutos definitivos de la evidencia original. Recuperar pasajes fuente antes de cerrar hallazgos.

### Declaración de IA

Localizar la declaración existente y comprobar su presencia y referencias internas. Evaluar si describe herramientas, propósito y partes afectadas según lo que el autor haya confirmado. No inferir exhaustivamente el proceso de elaboración a partir de estilo o metadatos. Si falta información, dejar una pregunta concreta, sin acusar una omisión.

## 9. Referencias, atribución y similitud

Implementar tres estados separados:

- **Consistencia interna:** citas y bibliografía corresponden formalmente.
- **Identidad externa:** publicación, autores, año y DOI fueron contrastados con un registro o fuente primaria.
- **Respaldo de contenido:** se consultó el texto y se identificó el pasaje que sostiene la afirmación.

Registrar resultado como verificado, discrepante, ambiguo o no verificado, con URL, fecha y alcance. Un DOI que resuelve no valida la interpretación de la fuente. Si solo hay resumen, indicar esa limitación. No convertir falta de acceso en inexistencia.

Modo sin conexión por defecto. La verificación externa será una fase explícita; enviar solo los datos mínimos necesarios, no capítulos completos. Priorizar fuentes editoriales y registros oficiales. Cachear respuestas con procedencia y fecha; respetar límites de acceso.

Permitir comparación con un corpus de fuentes proporcionadas y mostrar pasajes coincidentes y atribución. Informar cobertura del corpus; no llamarlo comparación universal ni asignar un porcentaje equivalente a Turnitin. La traducción o paráfrasis no elimina la obligación de atribuir ideas.

## 10. Consistencia de resultados y notación

Soportar inicialmente CSV/JSON y tablas LaTeX sencillas. Si se necesitan otros formatos, añadir adaptadores. Definir explícitamente claves de experimento; no emparejar resultados únicamente por el nombre de una métrica.

Preservar unidades, escalas 0–1 frente a porcentajes, denominadores, redondeo, medias, dispersiones, particiones y variantes del algoritmo. Comprobar diferencias con tolerancias configuradas y justificadas. Distinguir mejora absoluta de mejora relativa.

En este proyecto, prestar atención a que resultados de diferentes cantidades de agentes, modalidades, etapas de memoria o normalizaciones no se mezclen. Esto es una prioridad contextual que debe confirmarse en los archivos reales, no una afirmación sobre sus cifras actuales.

No extraer automáticamente valores de gráficas como verdad exacta. Preferir archivos de origen. Las ecuaciones complejas y sus supuestos se revisan contextualmente; no prometer demostración matemática automática.

## 11. Metadatos, PDF y compilación

Inspeccionar configuración fuente, incluyendo metadatos declarados por paquetes, y propiedades efectivas Info/XMP del PDF. Listar campo, valor minimizado, procedencia y explicación limitada. No afirmar que un generador de PDF identifica al redactor del texto.

Separar archivos que el autor entregará de los que permanecerán en el proyecto. Un comentario de un `.tex` no es automáticamente visible para quien recibe únicamente un PDF. Un tiempo corto de creación del PDF tampoco mide el tiempo de investigación.

Comparar extracción del PDF y fuente con cautela por ligaduras, guiones, columnas, símbolos y ecuaciones. Revisar candidatos de texto oculto considerando color de fondo, posición, recorte y modo de representación. No etiquetar todo texto blanco como invisible.

No implementar detección de marcas estadísticas sin especificación, detector compatible y validación. Registrar esta capacidad como no disponible, nunca como resultado negativo.

Para compilación, inspeccionar primero scripts y configuración. Ejecutar en copia o directorio aislado con salidas separadas y límites de tiempo. Usar listas de argumentos en subprocess, sin interpolación de shell. Deshabilitar shell-escape; si el proyecto depende de él, registrar el bloqueo y continuar el análisis fuente. Limitar acceso de archivos y red mediante aislamiento disponible; no afirmar aislamiento si no existe.

Las advertencias de `overfull`/`underfull` requieren revisión visual; no todas justifican cambios. Si hay SyncTeX, puede usarse para apoyar ubicación fuente/PDF, registrando sus límites. No inventar páginas cuando el vínculo no sea verificable.

## 12. Modelo de hallazgos

Definir esquema JSON con validación estricta. Campos mínimos:

```json
{
  "schema_version": "1.0",
  "finding_id": "identificador-estable",
  "rule_id": "XREF-002",
  "category": "cross_reference",
  "priority": "high",
  "evidence_status": "confirmed",
  "origin": "deterministic",
  "message": "Referencia sin destino en el alcance inspeccionado",
  "locations": [{
    "file": "chapters/resultados.tex",
    "start_line": 120,
    "end_line": 120,
    "snippet": "fragmento exacto del original",
    "file_hash": "hash-del-archivo"
  }],
  "recommendation": "Revisar la clave y el alcance de compilación",
  "review_status": "open"
}
```

El ejemplo define estructura, no un hallazgo real. Prioridad y estado de evidencia son ejes distintos: alta prioridad no implica certeza. Estados de revisión: abierto, aceptado para corregir, corregido pendiente de comprobar, resuelto, descartado con motivo y pendiente de información.

Derivar identificadores de regla y ancla contextual, no exclusivamente de número de línea. Para comparación entre versiones, combinar ID, fragmento y contexto; mostrar emparejamientos ambiguos. No marcar resuelto algo que desapareció porque falló la extracción o se excluyó el capítulo.

## 13. CLI y organización propuesta

```text
texaudit inventory --project ./tesis --main main.tex
texaudit check --project ./tesis --config audit.yaml --out ./audit/run-001
texaudit review-pack --run ./audit/run-001
texaudit import-review --run ./audit/run-001 --file review.json
texaudit report --run ./audit/run-001
texaudit compare --before ./audit/run-001 --after ./audit/run-002
```

Los comandos son el contrato propuesto, no herramientas instaladas. La fase de compilación debe activarse explícitamente mediante una opción o comando documentado. Registrar capacidades y dependencias opcionales; seguir produciendo un reporte parcial útil si falta PDF o compilador.

Organizar paquete en módulos de descubrimiento, parsing, mapa de origen, reglas, bibliografía, PDF, revisión, reportes y CLI. Mantener fixtures y pruebas separadas. Incluir `pyproject.toml`, configuración de ejemplo, instrucciones breves y catálogo de reglas. Usar herramientas del entorno cuando sean suficientes; elegir y fijar dependencias tras verificar su documentación actual.

## 14. Reportes y experiencia de revisión

Generar `report.json`, `report.html`, `summary.md`, inventario y manifiesto de ejecución. El manifiesto incluirá versión de herramienta, configuración, hashes, herramientas ejecutadas, cobertura, reglas desactivadas y tareas pendientes; no secretos ni rutas personales innecesarias.

HTML autocontenido, sin recursos remotos, con filtros por capítulo, regla, prioridad, evidencia y estado. Mostrar contexto y recomendación junto al hallazgo. Escapar contenido del manuscrito para impedir ejecución de HTML/JavaScript. Normalizar rutas y no convertirlas en comandos ejecutables.

Separar bloques: errores estructurales, verificación científica pendiente, observaciones editoriales y privacidad/documento. Mostrar totales de hallazgos sin llamarlos índice de riesgo de IA. El resumen debe priorizar acciones útiles, no saturar al autor con todas las repeticiones menores.

## 15. Validación y pruebas

Crear un proyecto sintético pequeño con varios capítulos, bibliografía, macros, tablas y ecuaciones. Sembrar errores conocidos y contrapartes legítimas. No usar el manuscrito completo como único test.

| Caso | Criterio de aceptación |
|---|---|
| Includes anidados y ciclo | Mapa correcto y terminación sin bucle. |
| Comentario, porcentaje escapado, verbatim | No se confunden con prosa ni comandos activos. |
| Macro anidada y Unicode | Fragmento y ubicación exactos en el original. |
| Cita ausente y nocite legítimo | Error real detectado y caso legítimo distinguido. |
| Etiquetas duplicadas y referencia externa | Duplicado mostrado; soporte externo declarado. |
| Párrafo duplicado frente a término técnico | Duplicación localizada sin acusar vocabulario técnico. |
| PDF con texto blanco sobre fondo oscuro | No se concluye invisibilidad solo por color. |
| PDF con metadatos y PDF sin ellos | Presencia, ausencia y error de lectura diferenciados. |
| Agente con ubicación inventada | Importación rechazada o puesta en cuarentena. |
| Texto fuente cambiado tras revisión | Observación marcada caducada. |
| Capítulo excluido en segunda pasada | No se declara automáticamente resuelto. |
| Contenido con HTML o instrucciones | No se ejecuta en reporte ni gobierna al agente. |
| Dependencia opcional ausente | Reporte parcial con limitación explícita. |

Comprobar hashes del manuscrito antes y después: la auditoría no debe alterar entradas. Validar esquemas y estabilidad de resultados para la misma versión/configuración; separar timestamps de contenido reproducible. Probar instalación y un flujo CLI completo en entorno limpio razonable. Registrar precisión de ubicaciones y falsas alarmas de reglas, sin llamarlas precisión de detección de IA.

La revisión semántica necesita evaluación del autor: muestrear hallazgos importantes, comprobar respaldo y registrar desacuerdos. No fijar una precisión científica ficticia a partir de unas pocas pruebas.

## 16. Fases de ejecución y puertas de salida

### Fase 0: reconocimiento

Entregar inventario, arquitectura adaptada al proyecto, riesgos reales de extracción y backlog. Continuar con decisiones reversibles; preguntar solo por ambigüedades que cambien el alcance de auditoría.

### Fase 1: núcleo trazable

Implementar estructura, mapa de origen, configuración, esquema y CLI mínima. Salida: extracción trazable sobre el fixture y un capítulo real. No añadir revisión semántica antes de verificar ubicaciones.

### Fase 2: reglas deterministas y reportes

Implementar referencias, bibliografía interna, repeticiones, pendientes y Unicode. Salida: HTML/JSON/Markdown útiles y pruebas de integración. Esta es la primera versión operativa.

### Fase 3: revisión con agente

Implementar paquetes, prompts, validación de observaciones y revisión transversal. Salida: un capítulo revisado con todas las observaciones localizables, seguido de cobertura progresiva del documento completo.

### Fase 4: PDF y compilación

Añadir propiedades, advertencias y validación visual de candidatos. Salida: límites de inspección claros y trazabilidad al PDF donde sea posible. No bloquear el resto si el entorno no compila.

### Fase 5: fuentes y resultados

Añadir verificación externa explícita y adaptadores de datos. Priorizar afirmaciones principales y resultados que sustentan conclusiones. Salida: estado de respaldo y procedencia, sin confundir hallazgo bibliográfico con verificación de contenido.

### Fase 6: revisión de cambios

Implementar decisiones del autor, comparación de ejecuciones y auditoría posterior a correcciones. Salida: hallazgos nuevos, persistentes, resueltos, caducados y no comparables.

No estimar horas rígidas sin inspeccionar el proyecto. Entregar avances funcionales por fase; no desarrollar una interfaz compleja antes de que el núcleo aporte hallazgos útiles.

## 17. Primer uso sobre el reporte real

1. Inventariar proyecto y PDF entregable, conservando la versión original.
2. Ejecutar comprobaciones internas sobre todos los archivos incluidos.
3. Revisar un capítulo representativo para calibrar macros, glosario y ruido editorial.
4. Corregir el programa si las ubicaciones o la extracción fallan; no compensarlo con interpretaciones del agente.
5. Revisar todos los capítulos con cobertura registrada.
6. Priorizar metodología, resultados, conclusiones y sus fuentes; después estilo general.
7. Revisar declaración de IA únicamente contra el proceso confirmado por el autor.
8. Entregar acciones priorizadas y preguntas científicas concretas.
9. Aplicar solo las correcciones solicitadas en una copia o cambio revisable.
10. Recompilar, verificar cambios y emitir reporte final con pendientes explícitos.

## 18. Relación con la skill existente

La skill `revisar-redaccion-metadatos` coordinará la auditoría; el software implementará comprobaciones repetibles. Actualizarla después de tener un CLI probado para que invoque comandos reales, lea el catálogo, prepare revisión contextual e interprete resultados. Mantenerla breve y colocar especificaciones técnicas en recursos referenciados. No afirmar que la skill actual ya implementa estos módulos.

## 19. Fuentes iniciales para el catálogo

Estas referencias orientan el diseño; el ejecutor debe comprobar su vigencia antes de atribuir capacidades actuales. No son acceso al algoritmo privado ni evidencia de funciones habilitadas en la UACJ.

- Turnitin, uso y limitaciones del reporte de IA: https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report
- Turnitin, similitud: https://guides.turnitin.com/hc/en-us/articles/23435833938701-Understanding-the-similarity-score
- Turnitin, alertas documentales: https://guides.turnitin.com/hc/en-us/articles/23351259442829-Flags-in-the-Similarity-Report
- Turnitin, detalles y metadatos: https://guides.turnitin.com/hc/en-us/articles/23980873584909-Viewing-document-details
- Copyleaks, resultados y explicaciones: https://docs.copyleaks.com/reference/data-types/authenticity/results/ai-detection
- GPTZero, límites de explicaciones basadas en perplejidad: https://support.gptzero.me/articles/9585228410-how-do-i-interpret-burstiness-or-perplexity
- RAID, evaluación de robustez de detectores, ACL 2024: https://aclanthology.org/2024.acl-long.674/
- DetectGPT, ICML 2023: https://proceedings.mlr.press/v202/mitchell23a.html
- Marcas estadísticas, ICML 2023: https://proceedings.mlr.press/v202/kirchenbauer23a.html
- SynthID-Text, Nature 2024: https://www.nature.com/articles/s41586-024-08025-4
- UACJ, postura: https://www.uacj.mx/document/Postura-Universitaria.pdf
- UACJ, guía: https://www.uacj.mx/document/Guia-Practica.pdf

Los estudios históricos describen condiciones y versiones concretas. No trasladar sus porcentajes de error a un documento actual en español. La política institucional y las condiciones de evaluación se revisan por separado de las capacidades técnicas del software.

## 20. Instrucción de arranque para Codex u otro asistente de código

> Lee este plan completo y las instrucciones del repositorio. Implementa la herramienta local de auditoría LaTeX por fases, adaptándola a la estructura real. Empieza con el inventario, el mapa de origen y un flujo CLI probado; continúa con las fases sin pedir confirmaciones rutinarias. Mantén intacto el manuscrito, separa hechos de observaciones del agente y registra cobertura y limitaciones. No entrenes un detector de IA, no prometas resultados de Turnitin y no contrates servicios ni publiques nada. Comprueba la documentación actual de las dependencias que elijas. En cada entrega explica qué funciona, cómo se comprobó y qué queda pendiente. No declares implementadas funciones que solo están descritas. Si falta el proyecto LaTeX, construye y prueba el núcleo con fixtures sintéticos y deja documentado cómo ejecutarlo sobre el proyecto real.
