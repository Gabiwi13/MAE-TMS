# Plan del artículo · CIFIN 2026

- **Congreso:** 2.º Congreso Internacional de las Fronteras de las Ingenierías 2026 (UACJ).
- **Eje:** «Inteligencia Artificial: Redefiniendo el Rol del Ingeniero»; ponencia.
- **Autores:** Gabriel Gonzalez, Karla Olmos-Sánchez y Jorge Rodas-Osollo.
- **Fechas:** el resumen se envía el 20 de octubre de 2026 (`Resumen_CIFIN2026_Gonzalez.docx`) y el artículo completo se entrega el 30 de octubre.

## Hilo del artículo

Se evalúa la MAE organizada como memoria transactiva para la inspección visual en líneas con varios tipos de pieza:

1. **Detección.** Leída en grado, la MAE iguala a Mahalanobis sobre latentes globales, pero pierde con PatchCore en fallas locales.
2. **Sistema mixto.** La MAE identifica la pieza y PatchCore decide si hay falla; el sistema completo detecta igual que un detector ideal.
3. **Lo que conserva la MAE:**
   - reconoce lo desconocido;
   - permite agregar o quitar módulos;
   - olvida de forma exacta;
   - no guarda imágenes (privacidad).
4. **Caja blanca.** Lo que falta es medirla. Los experimentos de abajo la convierten de afirmación en resultado.

## Experimentos pendientes

Cada uno lleva su propuesta con predicciones y criterio antes de correr, igual que los anteriores.

| fecha | experimento | propuesta | para qué |
|---|---|---|---|
| 21 oct | **Nombrar el tipo de falla en palabras** (heteroasociativa, imagen → nombre del tipo) y avisar si el tipo no está registrado | [`propuesta_nombrar_falla.md`](propuesta_nombrar_falla.md) | que el sistema diga **qué** falla es, en palabras |
| 21–22 oct | **Mapa de dónde está la falla** con la MAE por parches, contra las máscaras de VisA y frente al mapa de PatchCore | por escribir | que la MAE explique **dónde** está la falla |
| 22–23 oct | **Calibración** de las estimaciones del directorio: ¿la tasa que dice es la que obtiene? | por escribir | que sus explicaciones **sean confiables** |
| 23–24 oct | **Edición sin efectos colaterales:** agregar u olvidar un módulo no cambia las decisiones de los demás | por escribir | que la memoria **sea editable** |
| 24–28 oct | Redacción, con las figuras de la arquitectura mixta y la comparación | — | — |
| 29–30 oct | Revisión con la doctora y entrega | — | — |

## Material que ya existe

- **Registro de afirmaciones:** [`results/revision_cientifica/README.md`](results/revision_cientifica/README.md).
- **Síntesis:** [`results/sintesis_aplicaciones/README.md`](results/sintesis_aplicaciones/README.md).
- **Figuras:**
  - `arquitectura_mixta` y `comparacion_modelos` están en el worktree `industrial-demo-4132e4`, sin commit.
  - Hay que traerlas a esta rama cuando se aprueben.
- **Referencias verificadas:** [`referencias_congreso.md`](referencias_congreso.md).

## Pendientes de información

- Formato y extensión del artículo completo: no hay plantilla aún.
- Confirmar con la doctora el nombre del departamento en la afiliación.
