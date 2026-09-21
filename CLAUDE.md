# Reglas para trabajar en este repositorio

## Commits

- Los commits llevan solo la autoría del dueño del repositorio (`Gabiwi13`). Nunca uses tu propio nombre como autor ni agregues un trailer `Co-Authored-By`.

## Comentarios en el código

- Comentarios mínimos, en lenguaje simple. Un comentario explica algo que el código no dice por sí mismo; no repite lo que hace la línea ni justifica de más.
- Si al editar un archivo encuentras comentarios largos, redundantes o sobreexplicativos, acórtalos o elimínalos en esa misma edición.

## Honestidad en el código y los resultados

- Nunca hagas bypasses: nada de valores hardcodeados, casos especiales con numpy, semillas ajustadas ni parches que fuerzan un resultado esperado.
- Si algo no se puede lograr o un resultado no sale como se esperaba, dilo tal cual y muestra los números.

## Contexto

- Idioma de trabajo: español.
- Estado del proyecto y pendientes: `CONTEXTO_SEP2026.md`.
- Entorno: Python 3.13 en `.venv` (activar con `.\.venv\Scripts\Activate.ps1`). Torch con CUDA. Los modelos y datos no versionados se restauran según `LEEME_RESTAURAR.md`.
