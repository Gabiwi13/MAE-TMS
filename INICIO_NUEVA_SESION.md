# Arranque para una sesión nueva (estado al 22 de septiembre de 2026)

Léelo entero antes de tocar nada. Complementa a `CLAUDE.md` (reglas) y a `CONTEXTO_SEP2026.md` (historia detallada del 13 al 22 de septiembre). Este archivo es el resumen operativo.

## 1. Qué es el proyecto

MAE-TMS: sistema de memoria transactiva (Wegner) sobre memorias asociativas entrópicas (EAM/EHAM de Pineda y Morales). Ocho agentes especialistas (clases de ETH-80: apple, car, cow, cup, dog, horse, pear, tomato), cada uno con una hetero de contenido etiqueta↔latente, dos homo y dos directorios (texto e imagen). Texto→imagen e imagen→texto con rechazo. Es una tesis; el dueño del repo es `Gabiwi13`.

Repo: `https://github.com/Gabiwi13/MAE-TMS`, rama `exp7-directorio-unificado`. Clon local: `C:\Users\aq99l\Projects\MAE-TMS`. Al 22 de septiembre la rama local va por delante del remoto: código de la doble compuerta (3538b4a), resultados largos de exp11 (ee06bd6) y la prosa de esta ronda; sin push.

## 2. Reglas (resumen de `CLAUDE.md`)

- Commits solo con la identidad del dueño (`git config` local ya está en Gabiwi13). Nunca coautoría ni menciones a Claude en mensajes. Push solo cuando lo pida; se hace desde esta máquina (credenciales guardadas).
- Comentarios mínimos y simples; arreglar los sobreexplicativos al editar.
- Nada de bypasses: sin valores fijos, casos especiales, semillas elegidas ni parches que fuercen resultados. Si algo no sale, decirlo con los números.
- Idioma: español.
- Prosa de los README la aprueba el usuario; se le entrega en formato "viejo / nuevo" antes de aplicar (así se hizo en la fase 3).

## 3. Entorno de esta laptop

- Windows 11 LTSC, Core Ultra 7 265HX (20 hilos), 15.8 GB RAM, RTX PRO 1000 (8 GB, driver 581.97, CUDA 13.0).
- Python 3.13.15 vía Python install manager (el instalador .exe de python.org falla aquí). Venv en `.venv`; activar con `.\.venv\Scripts\Activate.ps1`. Torch 2.12 cu130, TensorFlow 2.21 (solo la importa `hetero_lib`), spaCy `en_core_web_sm`, python-pptx. `fasttext-wheel` omitido a propósito: no compila en 3.13 y nada lo importa.
- Git en `C:\Program Files\Git\cmd`. No hay winget, node ni LibreOffice.
- Datos y modelos no versionados ya restaurados: `models/`, `data/eth80/` (3280 imágenes), `cache/`, `~/gensim-data/` (fastText), `app_sample_images/`. `results/experimento7/latents_cache.json` tiene rutas absolutas de esta máquina y está marcado `skip-worktree` para que no entre en commits.
- **RAM es el límite, no la CPU.** Cada proceso de evaluación pesa ~1 GB por importar TensorFlow y torch. Con las demás apps cerradas caben 12; con Chrome y Teams abiertos, 5.

## 4. Estado de los modelos

- `models/` tiene desde el 21 de septiembre los 9 pickles (8 agentes + TME) del protocolo **v5** (directorios perspectivales). Las memorias de contenido son bit a bit las mismas que en v4; solo cambian `mem_dir`, `mem_dir_R` y el TME. Etapa 8 verificada 16/16 tras el cambio.
- `models_backup_pre_perspectival/` tiene los **v4** (directorios idénticos entre agentes): son los que produjeron exp8, exp9 y las fases 1 y 2. `models_v5_perspectival/` conserva la copia de los v5. Ambas carpetas están excluidas de git.
- `cache/exp11/N{25,50,100,200}.pkl` (1.5 GB cada uno): memorias reconstruidas por corte para exp11 y exp12. Excluidas de git.

## 5. Qué se hizo el 20 y 21 de septiembre

| fase | resultado | dónde |
|---|---|---|
| 0–2 (antes) | pista de identidad con nan, siembra de `random`, Bessel en F, split versionado | `CONTEXTO_SEP2026.md` §6 |
| 3, prosa | aplicada con aprobación: exp7, exp8, exp9, exp10, marco teórico (cifras), README, CONTEXTO, tex8 | `revision_fase3_prosa.md` (viejo/nuevo) |
| 4, contradicción | salida 5.1: las frases "no entrópico" se restringen al ruteo; `recall_domain` existe y es diagnóstica; párrafo de los dos lados de la relación | `revision_fase4_directorio_entropico_vs_metamemoria.md`, `discusion_directorio_entropico.md` |
| 5, exp11 | EHAM única contra sistema transactivo, 4 cortes × 10 semillas × 3 sorteos, 171 consultas reservadas | `propuesta_fase5_mae_monolitica.md`, `run_experiment11_monolithic.py`, `results/experimento11/` |
| exp12 | brecha de fidelidad de una EHAM de dos clases contra el solapamiento, 28 pares | `run_experiment12_overlap.py`, `results/experimento12/` |
| app | fase temprana en vivo con directorios perspectivales; fase madura de sesión con `route_transactive` | `app_tme.py` |
| deck | 12 diapositivas con los hallazgos de exp7 a exp11 | `hallazgos_exp7_a_exp11.pptx` |
| imagen→texto largo | 4 cortes × 10 semillas; cobertura del especialista 0 → 79 % con N | `results/experimento11/README.md` |
| compuerta | doble compuerta de contenido en la fase madura textual; protocolo fuera de dominio 4/40 → 2/40 | `stage8_mature.py`, `app_tme.py`, `run_experiment11_monolithic.py` |
| exp13 | augmentación del llenado visual: dos compuertas, punta a punta 66.5 → 94.5 % con 16 variantes, 1 falso ruteo de 656 | `run_experiment13_augmentation.py`, `results/experimento13/` |

## 6. Resultados clave (para no re-derivarlos)

**Exp11, N=200 (corte oficial):**

| medida | EHAM única (M) | transactivo, oráculo | transactivo, protocolo |
|---|---|---|---|
| clase correcta, 1-NN (%) | 97.4 | 100 | 97.5 |
| distancia a instancia real | 26.7 | 22.2 | 22.8 |
| clase con pista compartida (%) | 44 | 100 | 66 |
| imagen→texto: responde / dominio ajeno (%) | 96 / 9 | 79 / 1 | 72 / 2 |
| fuera de dominio aceptadas (de 40) | 3 | 2 | 4 |
| fuera de dominio con doble compuerta | 3 | 2 | 2 |

Veredicto: no refutada por el criterio pre-registrado (clase empata, fidelidad difiere en 3.9 con umbral 1). Partir compra fidelidad (brecha crece 2.0 → 4.5 con N), coherencia y precisión; cuesta cobertura (containment estricto del especialista), 2.5 puntos de directorio y 8× las celdas. El directorio de texto deja pasar dos consultas fuera de dominio que el contenido rechaza (piano → dog, thunderstorm → car). Con la doble compuerta el protocolo acepta 2/40 en los cuatro cortes y no pierde ninguna respuesta sobre las 171 reservadas. Imagen→texto con los cuatro cortes: la cobertura del especialista sube 0 → 79 % con N; la EHAM única 5 → 96 % y su dominio ajeno 0 → 9 %.

**Exp12:** la brecha crece con el solapamiento de soportes en etiquetas (ρ 0.45, p 0.017) y el error de clase también (ρ 0.49, p 0.008); no con el latente (ρ −0.07). Las 28 brechas son positivas (mínimo +0.5): no hay dominios disjuntos con esta cuantización (Jaccard 0.57–0.65). Formulación: la ventaja de partir existe para cualquier par y crece con el solapamiento de las pistas.

**Exp13:** el rechazo visual son dos compuertas (directorio y recall de la hetero) y cada una cede solo con su augmentación; con 16 variantes en las dos, ruteo 73.6 → 97.1 % y punta a punta 66.5 → 94.5 %, con 1 falso ruteo de 656 y la sonda de color sólido aceptada por 3 especialistas. No adoptado como llenado oficial.

**Exp9 tras la corrección de la pista:** la descripción (lectura inversa del directorio) supera al especialista en fidelidad (19.3 contra 21.9); la familiaridad vive en el reconocimiento (98% contra 16%), con la contención por coordenada como puerta que la descripción no tiene.

**Exp8 corregido:** envolvente 2.9 a 5.5 veces la distancia entre instancias; de 8 a 800 registros pierde 4 unidades, no 10; 80/80 en todas las semillas; el óptimo 4–8 es de reconstrucción, para rutear hacen falta 64–128 o encadenar; la transición del barrido presenciado es 1 − (1 − f)^128.

## 7. Cómo correr las cosas

```powershell
.\.venv\Scripts\Activate.ps1
$env:CUDA_VISIBLE_DEVICES="-1"; $env:OMP_NUM_THREADS="1"; $env:PYTHONUNBUFFERED="1"   # "" no oculta la GPU

# exp11 (reanudable: salta los trozos con archivo)
python run_experiment11_monolithic.py --cuts 200,50,100,25 --seeds 42-51 --reps 3 --chunks 6 --workers 10
python run_experiment11_monolithic.py --image-only --cuts 200,50,100,25 --seeds 42-51 --img-per-class 10 --workers 6   # 134 min; con Chrome abierto caben 6
python run_experiment11_monolithic.py --ood-only --ood-file results\experimento11\consultas_fuera_dominio.txt --cuts 200,50,100,25 --seeds 42-51 --workers 10
python run_experiment11_monolithic.py --report-only
python run_experiment11_probes.py            # por clase, fig5 quimeras, fig6 comparación

# exp12
python run_experiment12_overlap.py --seeds 42-46 --reps 3 --workers 8

# exp13 (reanudable; latentes y contenido en caché; ~50 min de llenados + ~4 h de evaluación con 2 procesos)
python run_experiment13_augmentation.py --seeds 42-46 --workers 2
python run_experiment13_augmentation.py --report-only

# app (o con .claude/launch.json, nombre app-tme)
python -m streamlit run app_tme.py
```

Pruebas sin ensuciar resultados: `EXP11_OUT=<carpeta>` y `EXP12_OUT=<carpeta>` redirigen la salida; `--quick` en exp11.

## 8. Trampas conocidas

- **Cuantización en float32.** La etapa 5 cuantizó latentes y stats en float32. Releer `instance_latents_*.json` en float64 cambia un nivel en un latente de car, cow y dog y las memorias dejan de ser bit a bit las oficiales. `load_pool` de exp11 ya lo hace bien.
- **Siembra.** `hetero_lib` muestrea con `random` de Python, no numpy. Sembrar los dos.
- **Registro lento.** Cada `register` de una hetero cuesta ~80 ms (reconstruye la relación de 86 MB). Por eso hay caché por corte y memoria compartida entre procesos.
- **`Pool.map` con tareas grandes se cuelga** si un trabajador muere al arrancar. Los datos van por `initializer`; las tareas son tuplas pequeñas; `imap_unordered`.
- **Los latentes de test** de imagen solo están en caché para 20 por clase; para las 82 hay que codificar con el encoder.
- **Primer arranque de la app** descarga los pesos de ResNet18 desde PyTorch (45 MB); en esta red fue lento (45 kB/s). Queda en `~/.cache/torch/hub/checkpoints/`.
- **`import` locales dentro de `main()` de `app_tme.py`** hacen sombra a los de módulo (ya se quitó uno de `route_transactive`).
- **Streamlit no recarga los módulos de `src/` importados dentro de `main()`** (`from stage8_mature import route_mature`): tras editar uno hay que reiniciar el servidor, no basta con recargar la página.
- **`$env:CUDA_VISIBLE_DEVICES=""` en PowerShell borra la variable** (torch sí ve la GPU); para ocultarla hay que usar `"-1"`. Los modelos se cargan en `DEVICE` (cuda si torch la ve): toda entrada nueva va con `.to(next(modelo.parameters()).device)`; `run_experiment5.py`, `run_experiment6.py` y `generate_paper_figures.py` fallaban por eso hasta el 22 de septiembre.
- **`evoke_labels` / `recall_from_right` cuestan ~17 s por imagen** (búsqueda por muestreo de `hetero_lib`, 3000 proyecciones); para medir cobertura basta una proyección (`hetero_recognizes` de exp13), la evocación completa solo para leer etiquetas.
- No tocar `src/hetero_lib/` (código vendido de Pineda y Morales).

## 9. Pendiente

- Deck externo de Drive (`exp7-10_literatura_corta (2).pptx`): lista viejo/nuevo entregada el 22 de septiembre (envolvente 2.9 a 5.5, descripción 19.3 contra 21.9 y familiaridad, 3.5 saltos); sin aplicar.
- Decidir si el llenado con 16 variantes (contenido y fase A) pasa a ser el oficial: rehacer etapa 5 y fase A, re-verificar 8/8 y 16/16, re-correr lo que depende de `models/` (exp8, exp9, exp11, app) y actualizar las cifras de 75 % / 0 falsos del reporte.
- Criterio de varianza mínima de la entrada visual, medido con las tres sondas y las 656 de test (que no rechace ninguna imagen real); cierra la fuga de color sólido que exp13 hizo crecer.
