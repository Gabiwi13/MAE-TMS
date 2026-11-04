# Índice nuevo del reporte por fases (camino A) — propuesta para aprobar

Base: `una-hetero` @ `0d47674`. Fuentes de este índice: `inventario_fase1_tres_modulos.md`, `inventario_fase2_escalado.md`, `inventario_fase3_mundo_real.md`, `inventario_hallazgos.md`, `creencias_iniciales.md` y `catalogo_experimentos.md` (esta carpeta).

## Reglas que valen para todo el texto nuevo
1. Cada cifra va con la arquitectura de su fase. Las de 3 módulos se rotulan así: «con la arquitectura de la fase 1: tres módulos, cuatro memorias por módulo, cuantización por signo y TME mediador». No se presentan como comparación controlada con el sistema final.
2. Cada cifra tiene una fuente versionada en `results/`. Las de 3 módulos se copian de `origin/v3-experimento1` (commits `0ff1619` y `54f30ca`) a `results/fase1_tres_modulos/`, con los informes originales y sin recalcular nada. Lo del laboratorio en tiempo real se copia a `results/mundo_real/`, con la etiqueta v5 y la salvedad de que no quedó salida cruda.
3. El escalado se cuenta como lo que pasó: al pasar de 3 a 8 cambiaron a la vez el codificador, la cuantización, las memorias por módulo, el banco y el mediador. La evidencia controlada del efecto de crecer es la EHAM única contra la partición (exp11) y la EHAM de 2 clases contra la de 8 (exp12).
4. Sin experimentos nuevos. Lo que pida medirse va a trabajo futuro o a limitaciones.
5. Toda la prosa va como propuesta viejo/nuevo. Se respetan «módulo», los prefijos sin guion y la palabra prohibida.
6. **Reglas contra los patrones de texto generado.** Son las de la sección 7 de `texaudit/PLAN.md`, las de la revisión de patrones ya aplicada (`revision_patrones_prosa.md`) y las de `antipatrones.md` (carpeta `consejo` de la sesión anterior). La prosa nueva no puede tener:
   - vaguedad ni afirmaciones genéricas que no dicen nada medible;
   - énfasis sin respaldo («claramente», «notablemente», «crucial», «robusto», «sin duda», «de forma robusta»);
   - frases que anuncian en vez de decir («cabe destacar», «es importante señalar», «en este sentido»);
   - transiciones sin relación lógica con lo anterior;
   - conclusiones repetidas sin interpretación nueva;
   - tríadas o enumeraciones de relleno;
   - antítesis de plantilla («no es X, sino Y»);
   - dos puntos explicativos en serie;
   - ritmo uniforme;
   - cambios de registro o restos conversacionales;
   - muletillas o comienzos repetidos («así», «La tabla», «El directorio», «El sistema»).

   Tampoco se vale la variación artificial (errores, sinónimos rebuscados o cambios de términos técnicos para «parecer humano»). Los términos definidos no cambian.
   Cada sesión que redacte revisa su texto con esta lista antes de entregarlo. Después de integrar, la revisión contextual de patrones se corre como sexta auditoría, junto con el recuento de muletillas por capítulo.

## Capítulo 1. Planteamiento del Problema
- **1.1 Antecedentes.** Igual que ahora, más un párrafo con el arco de la investigación.
- **1.2 Definición del problema.** Se conserva el techo entrópico como motivo para repartir el contenido. El problema pasa a tener cinco partes: que el directorio emerja del uso, cómo leerlo, que escale, qué propiedades muestra y si funciona con entradas del mundo real.
- **1.3 Objetivo general:** construir un sistema distribuido de memoria transactiva sobre memorias asociativas entrópicas y estudiarlo por fases.
  - **OE1. Emergencia (fase 1, 3 módulos):** comprobar que el directorio emerge de la experiencia.
  - **OE2. Lectura del directorio (fase 2, 3 módulos):** determinar cómo leer el directorio. Aquí se elige la normalización B1.
  - **OE3. Escalado (fase 3, 8 módulos sobre ETH-80):** comprobar que el sistema escala a ocho módulos con una memoria heteroasociativa por módulo, y compararlo con una sola memoria y con decisores simples.
  - **OE4. Hallazgos (fase 4, 8 módulos):** caracterizar las propiedades del sistema escalado: metamemoria, perspectiva, envolvente, tamaño y partición, imagen y palabra, y límites. Leerlas desde Wegner, la psicología y la neurociencia.
  - **OE5. Mundo real (fase 5):** integrar voz (Whisper) y cámara en tiempo real. Es una demostración de integración, no una evaluación con cifras de acierto.
- **1.4 Justificación.** Se ajusta.
- **1.5 Alcances y limitaciones.** Se ajusta: hoy excluye las consultas en otros idiomas y las fotos de otro origen, y la fase 5 las toca como demostración.
- **Preguntas de investigación:** una por objetivo.

## Capítulo 2. Marco Teórico
Queda igual. Se agregan solo las citas nuevas que pidan los hallazgos (Nelson y Narens para la metamemoria, entre otras), cada una verificada antes de entrar a `referencias.bib`.

## Capítulo 3. Desarrollo del Proyecto (fases como secciones, como pide la plantilla)
- **3.1 Producto propuesto.** El sistema final, con 3.1.1 a 3.1.3 como ahora.
- **3.2 Descripción de la metodología.** Las cinco fases, con una figura del arco y lo que cambió en cada una. Incluye las métricas comunes.
- **3.3 Fase 1: prototipo de tres módulos.** Apple, horse y car; cuatro memorias por módulo; TME mediador; formación del directorio.
- **3.4 Fase 2: lectura del directorio.** Las condiciones de lectura (cruda, B1, B2, C, D, E32, E64) y por qué B1. Toma lo que hoy está en «Lectura normalizada por conteo».
- **3.5 Fase 3: escalado a ocho módulos.** Lo que cambió (commits `b281f9c` a `d5b93fa`) y los métodos del sistema final: conjunto de datos, representación de texto, percepción visual, banco, parámetros, auditoría de trazabilidad y organización del experimento. Son las secciones actuales 3.3 a 3.10, que pasan a ser subsecciones.
- **3.6 Fase 4: experimentos de propiedades.** El diseño de los experimentos 7 a 24 que entran.
- **3.7 Fase 5: laboratorio en tiempo real.** Voz y cámara, con la versión v5 del sistema.

## Capítulo 4. Resultados y Discusiones
- **4.1 Resultados, por fase.**
  - **4.1.1 Fase 1.** Formación del directorio con tres módulos:
    - 26 % con una interacción, 91 % con 13 y 98.75 % con 80; el rechazo baja de 72.5 a 1.25 %;
    - con el orden bloqueado se queda en 33.75 %;
    - las cuentas finales son [78, 65, 53];
    - se midió dentro de muestra y se dice.
  - **4.1.2 Fase 2.** Calibración de la lectura: B1 contra las otras condiciones (lo que hoy está en «Calibración»), la calibración con conjunto fijo, y exp22 (el principio de tamaño equivale a B1 en ETH-80, 1 decisión distinta de 656).
  - **4.1.3 Fase 3.** Escalado: el protocolo completo, ι × κ, la formación con 8 (no llega al 90 %, queda en 81.2), la capacidad, el hemisferio visual, los objetos nuevos, el codificador sin clase, la EHAM única contra la partición (exp11), las 2 clases contra 8 (exp12, nuevo), una memoria por módulo, las líneas base y el costo. Todo lo de hoy, reordenado, más exp12.
  - **4.1.4 Fase 4.** Hallazgos con ETH-80 y 8 módulos. Entran los 7 que faltan: exp7, exp8, exp9, exp12 si no entra en 4.1.3, exp17, exp18 y exp22. Se agrupan en los 6 temas del inventario de hallazgos, con exp10 y exp19 completos.
  - **4.1.5 Fase 5.** Demostración en tiempo real:
    - latencias de 336 ms de transcripción más 302 ms de enrutamiento (≈0.6 s) y visión a 54 ms por cuadro, todas de una sola medición de julio sin salida cruda;
    - el cuadro real ajeno a ETH-80 que se rechaza;
    - corrección de color en simulación: 22, 18 y 15 de 24;
    - sin tasa de error de transcripción ni aciertos con voz, y se dice.
- **4.2 Discusiones.**
  - **4.2.1 Creencias iniciales y lo que se encontró.** Las 19 de `creencias_iniciales.md`, con la decisión que cambió cada una y el experimento que la decidió.
  - **4.2.2 a 4.2.7 Lectura por tema:** metamemoria, perspectiva y pérdida de un miembro, reconocer y recordar, tamaño y partición, imagen y palabra, y límites. Integra la lectura desde Wegner que hay hoy.
  - **4.2.8 Qué aporta la partición y qué agrega la memoria frente a decisores simples.** Lo de hoy.
  - **4.2.9 Limitaciones.** Las de hoy, más las de comparabilidad entre fases, la fase 5 sin cifras y exp9 con el protocolo anterior.

## Capítulo 5. Conclusiones
- **5.1 Con respecto a las preguntas de investigación:** una respuesta por objetivo, OE1 a OE5.
- **5.2 Con respecto al objetivo general.**
- **5.3 Recomendaciones para trabajo a futuro:** se agregan el barrido de K con la arquitectura final, repetir exp9 con el protocolo corregido y medir la voz con cifras.
- **5.4 Difusión y productos derivados:** igual que ahora.

## Resumen, Abstract e Introducción
Se reescriben con el arco de las cinco fases y deben caber en una página.

## Apéndice A
Los 58 experimentos, ordenados por fase: carpeta, qué mide, arquitectura, estado (vigente, corregido o reemplazado) y dónde se reporta.

## Erratas que hay que resolver antes de citar (de los inventarios)
- `results/computational_cost/report.md:36`: dice «984 imágenes» en la corrida de 8 clases.
- exp11: hay dos versiones del ruteo del protocolo; se cita solo la corregida (`experimento11_protocolo_corregido`).
- exp12: ya no sostiene que la ventaja de partir crezca con el solapamiento (ρ 0.01); las síntesis viejas sí lo dicen.
- exp19: 80.5 en el reporte contra 79.6 en `sintesis_26oct`; hay que fijar la vigente.
- exp9: «90 de 411 con 16 interacciones» no coincide con `curva.json`.
- La cifra «fallas pequeñas 28→59 %» del resumen de CIFIN no tiene soporte (le toca a la sesión del artículo).

## Decisiones del autor (4 nov)
1. Aplicaciones médica e industrial: fuera del reporte. Solo se mencionan como casos aplicados en curso, como ya hace la Sección 5.4, junto al 12.º Encuentro.
2. Fase 5: entra como demostración de integración, con sus latencias y sus límites.
3. Creencias iniciales: van en la Discusión (4.2.1) y se retoman en las Conclusiones.
4. exp9: se reporta con la salvedad de que usa el protocolo anterior.

## Decisiones abiertas (ya respondidas arriba)
1. **Las aplicaciones médica (MedMNIST+) e industrial (VisA).** Son 13 de los 20 hallazgos que faltan y cuentan como evidencia de generalidad. ¿Entran como parte de la fase 5 («fuera de ETH-80»), como una fase propia o se quedan fuera porque son del artículo de CULCYT?
2. **La fase 5** ¿entra solo como demostración, con sus latencias y su salvedad?
3. **La sección de creencias iniciales** ¿va en la Discusión (4.2.1, como se propone) o en las Conclusiones?
4. **exp9 y la pérdida de un miembro,** que se corrió con el protocolo anterior: ¿se reporta con esa salvedad o se deja fuera?
