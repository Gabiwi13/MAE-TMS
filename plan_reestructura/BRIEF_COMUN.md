# Brief común para las sesiones de reescritura por fases

Trabajo en español. El reporte técnico de titulación (UACJ, entrega hoy, 4 nov 2026) se reescribe con el arco real de la investigación, en cinco fases:
1. prototipo de 3 módulos, donde emerge el directorio;
2. lectura del directorio, donde se elige B1;
3. escalado a 8 módulos;
4. hallazgos;
5. mundo real, solo como demostración.

El índice aprobado por el autor está en `plan_reestructura/INDICE_REESTRUCTURA_FASES.md`. Léelo completo primero, junto con los inventarios de la misma carpeta, porque son la fuente de toda cifra nueva.

## Base y entrega
- `git fetch origin una-hetero && git checkout --detach 59cca47`. Todo parte de ese commit.
- Toca **solo** los archivos que te asigna tu tarea. Las otras sesiones trabajan los demás en paralelo.
- Sin commit, sin push y sin ramas: el push da 403.
- **Entrega:**
  - un parche `git diff 59cca47` con tus archivos (incluye los nuevos con `git add -N`), verificado con `git apply --check` sobre `59cca47` en un worktree limpio;
  - un archivo `revision_fases_<parte>_prosa.md` en la raíz, con las secciones viejas y nuevas y la fuente de cada cifra.
- **Mensaje final:**
  - un resumen breve: qué cambió, cifras nuevas con su fuente, qué no pudiste sostener y por qué, etiquetas `\label` nuevas o eliminadas y citas que necesitarías y no están en el `.bib`;
  - el parche en un bloque ```diff``` precedido de `SHA256: <hash>`. Si pesa más de unos 150 KB, mándalo como archivo adjunto y pon el hash en el mensaje.

## Reglas de evidencia
1. **Cifras por fase.** Cada cifra va con la arquitectura de su fase. Las de la fase 1 se rotulan (tres módulos, cuatro memorias por módulo, cuantización por signo, TME, banco de 80) y no se comparan como experimento controlado con el sistema final.
2. **Fuentes.** Toda cifra tiene fuente en `results/`. Las de 3 módulos están en `results/fase1_tres_modulos/`; las del laboratorio, en `results/mundo_real/`. Si una cifra no tiene fuente o está marcada como corregida o retractada en los inventarios, no entra. Las erratas listadas en el índice se resuelven citando la versión vigente.
3. **Escalado.** Se cuenta como lo que pasó: al pasar de 3 a 8 cambiaron varias cosas a la vez. La evidencia controlada del efecto del tamaño es exp11 (EHAM única contra la partición) y exp12 (2 clases contra 8).
4. **Sin experimentos nuevos.** Lo que pida medirse va a limitaciones o a trabajo futuro.
5. **Fuera del reporte** quedan las aplicaciones médica (MedMNIST+) e industrial (VisA). Solo se mencionan como casos aplicados en curso, como hace la Sección 5.4.

## Reglas de estilo (obligatorias)
- Se dice «módulo», nunca «agente». Prefijos sin guion. `\,\%`. Comillas angulares. Lenguaje simple.
- El nombre del asistente de IA (la marca de seis letras que empieza con C) no puede aparecer en ningún archivo ni en el parche; `git diff | grep -ci` debe dar 0.
- Hay que revisar los patrones de texto generado antes de entregar: la sección 7 de `texaudit/PLAN.md` (`git show origin/texaudit:texaudit/PLAN.md`), `plan_reestructura/antipatrones.md` y la regla 6 del índice. El texto no puede tener:
  - vaguedad;
  - énfasis sin respaldo;
  - frases que anuncian;
  - transiciones sin lógica;
  - conclusiones repetidas;
  - tríadas de relleno;
  - «no es X, sino Y»;
  - dos puntos en serie;
  - ritmo uniforme;
  - cambios de registro;
  - muletillas o comienzos repetidos.
- Tampoco se vale la variación artificial, y los términos definidos (módulo, directorio, compuerta, fase temprana y madura, B1, EHAM, TME) no cambian.
- Solo cuenta la historia de las fases como metodología. Nada de «en la versión anterior» ni de «corregido tras el jurado».

## Reglas técnicas
- Los capítulos 2 a 5 de `.tex_uacj/` se generan desde `.tex8/secciones/` con `python .tex_uacj/generar_capitulos.py`, que falla si se pierde una línea. Edita `.tex8/secciones/` y regenera; el parche incluye los dos lados.
- No toques `generar_capitulos.py` salvo que tu tarea lo diga. Conserva las marcas que usa: `\paragraph{Respuesta a la pregunta de investigación.}` y `\paragraph{Trabajo futuro.}` en `07_conclusiones.tex`, y el `\subsection{Diagramas de flujo}` y el `\subsection{Conjunto de datos}` que parten los capítulos 3 y 4.
- Conserva las etiquetas `\label` existentes, porque otros capítulos las citan. Las nuevas llevan prefijo `fase`.
- Solo `\cite` con claves que ya estén en `.tex8/referencias.bib`, salvo la sesión de Discusiones, que puede agregar entradas verificadas.
- Si hay `xelatex` (TeX Live), compila `.tex_uacj/tesis_uacj.tex` para revisar; si no, basta con que `generar_capitulos.py` termine sin error.
