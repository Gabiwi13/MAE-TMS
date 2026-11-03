# cotejo

Cotejo local y abierto para un reporte en LaTeX antes de entregarlo. Hace cuatro cosas:

1. **Extrae** el texto de los `.tex` (sigue `\include`/`\input`) y guarda el archivo y la línea de cada palabra.
2. **Mide la similitud** contra un corpus que usted arma (PDFs y páginas de sus referencias, más textos propios). Usa shingles, un índice invertido y alineación local. Opcionalmente busca paráfrasis cercana con embeddings.
3. **Revisa la integridad** del documento: texto oculto, sustitución de caracteres y metadatos, en el PDF y en los `.tex`.
4. **Puntúa con detectores abiertos** de texto generado (Binoculars y Fast-DetectGPT). Es un módulo opcional.

Lo que **no** es:

- No reproduce el servicio comercial de similitud que use la universidad. Ese servicio usa otro corpus (web, publicaciones, trabajos entregados) y otros filtros, y ninguno de los porcentajes de aquí equivale al suyo.
- Ningún detector prueba autoría. Sin un conjunto de referencia propio (`--referencia`), sus números no se interpretan.
- Lo que no está en el corpus no se cotejó. La sección «Cobertura» del reporte dice qué fuentes faltan.

## Instalación en Windows (PowerShell, con `.venv`)

Requiere Python 3.11 o superior.

```powershell
cd C:\ruta\a\MAE-TMS
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e ".\cotejo[prueba]"
pytest cotejo\tests
```

Para los detectores y la paráfrasis, instale primero PyTorch con CUDA. Copie el comando para Windows, pip y su versión de CUDA desde <https://pytorch.org/get-started/locally/>; se ve así:

```powershell
pip install torch --index-url https://download.pytorch.org/whl/cu128
pip install -e ".\cotejo[detectores,parafrasis]"
python -c "import torch; print(torch.cuda.is_available())"
```

La primera vez que se usan, los modelos se descargan de Hugging Face. Qwen2.5-1.5B pesa unos 3 GB y su versión Instruct otros tantos; el modelo de paráfrasis, unos 0.5 GB.

## Uso

Corra todo desde la raíz del repositorio del manuscrito (rama `una-hetero`).

```powershell
# 1. Texto del reporte (y comparación con el PDF compilado, si existe)
cotejo extraer --raiz .tex_uacj\tesis_uacj.tex --pdf .tex_uacj\tesis_uacj.pdf --salida cotejo_salida

# 2. Corpus. Si aún no tiene la lista de URL de acceso abierto, genere una plantilla desde el .bib:
cotejo corpus --plantilla fuentes.json --bib .tex8\referencias.bib
#    Llene url_pdf / url_html / licencia y descargue. Los PDFs que ya tenga van en una carpeta
#    con el nombre de la clave BibTeX (p. ej. pineda2021entropic.pdf):
cotejo corpus --cache .cotejo_corpus --fuentes fuentes.json --pdfs pdfs_referencias --locales README.md "revision_*.md"

# 3. Alertas de integridad (PDF y .tex)
cotejo banderas --salida cotejo_salida --pdf .tex_uacj\tesis_uacj.pdf

# 4. Similitud. Los filtros son opcionales; el reporte siempre muestra también el índice sin filtros.
cotejo similitud --salida cotejo_salida --cache .cotejo_corpus --excluir-bibliografia --excluir-citas --excluir-menores N --parafrasis

# 5. Oraciones para buscar a mano en la web (no se envía nada)
cotejo web --salida cotejo_salida --muestra 25

# 6. Detectores (opcional; GPU recomendada)
cotejo detectar --salida cotejo_salida --referencia referencia

# 7. Reporte: cotejo_salida\reporte.html, reporte.json y summary.md
cotejo reporte --salida cotejo_salida
```

`cotejo todo` encadena los pasos 1 a 7 con las mismas opciones; los detectores solo corren si se agrega `--detectar`.

### Lista de fuentes

Es un JSON con una lista de objetos `{"clave", "url_pdf" o "url_html", "licencia"}`. También acepta `{"fuentes": [...]}`. La clave debe ser la de BibTeX: así se sabe si el párrafo que coincide cita esa fuente. Cada descarga se guarda en `--cache` con la URL, la fecha y el SHA-256. Las fuentes no se vuelven a descargar salvo con `--refrescar`.

### Filtros (como los que describe la guía pública citada abajo)

| Opción | Excluye |
|---|---|
| `--excluir-bibliografia` | el texto de la bibliografía, que se genera desde el `.bib` con las entradas citadas |
| `--excluir-citas` | lo que está entre «», “” o "", `\say`, `\enquote` y los entornos `quote` |
| `--excluir-menores N` | las coincidencias de menos de N palabras |
| `--excluir-ecuaciones` | las ecuaciones en línea y en bloque |
| `--excluir-codigo` | `verbatim`, `lstlisting`, `minted` y `\verb` |

No se sabe con qué filtros revisará la UACJ. Por eso la tabla del reporte muestra el índice con cada filtro por separado y sin filtros.

### Conjunto de referencia para los detectores

```
referencia\
  humano\     textos en español escritos por personas antes de 2022 (.txt o .md)
  generado\   textos generados por modelos sobre temas parecidos (.txt o .md)
```

Separe los párrafos con una línea en blanco; se usan los de al menos `--min-palabras` palabras (40 por defecto). Para cada párrafo y sección del reporte, el resultado da su percentil dentro de cada grupo. No da una etiqueta. Con pocos párrafos de referencia, esa posición es inestable.

Modelos: `--pares pequeno` (por defecto) usa Qwen/Qwen2.5-1.5B como base y Qwen/Qwen2.5-1.5B-Instruct como instruct. En bf16 ocupan unos 7 GB de GPU; en CPU, `--dispositivo cpu` usa float32 y unos 13 GB de RAM. `--pares articulo` usa tiiuae/falcon-7b y tiiuae/falcon-7b-instruct, como los artículos, pero necesita unos 28 GB y no cabe en una máquina con 15.5 GB de RAM. Con `--base` y `--instruct` se elige cualquier par que comparta tokenizador.

## Métodos y referencias

- Binoculars: A. Hans et al., «Spotting LLMs With Binoculars: Zero-Shot Detection of Machine-Generated Text», ICML 2024, arXiv:2401.12070, <https://github.com/ahans30/Binoculars>. El puntaje es la perplejidad del modelo instruct dividida entre la perplejidad cruzada entre los dos modelos, igual que en `binoculars/metrics.py`.
- Fast-DetectGPT: G. Bao et al., «Fast-DetectGPT: Efficient Zero-Shot Detection of Machine-Generated Text via Conditional Probability Curvature», ICLR 2024, arXiv:2310.05130, <https://github.com/baoguangsheng/fast-detect-gpt>. Se usa el criterio analítico (`get_sampling_discrepancy_analytic`), con el modelo base para el muestreo y el instruct para la puntuación.
- Las guías públicas de Turnitin sirven solo de referencia para la definición del índice y de las alertas: <https://guides.turnitin.com/hc/en-us/articles/23435833938701-Understanding-the-similarity-score> y <https://guides.turnitin.com/hc/en-us/articles/23351259442829-Flags-in-the-Similarity-Report>. No se pudieron abrir desde el entorno donde se escribió esta herramienta; verifíquelas antes de citarlas.

## Limitaciones

- La extracción no expande macros propias ni incluye la portada que genera la clase.
- La coincidencia es literal tras normalizar. No detecta traducción y detecta la paráfrasis solo si se activa `--parafrasis`, y aun así no la suma al índice.
- El análisis de texto oculto en el PDF no considera imágenes de fondo, recortes, transparencias ni capas. El texto blanco se informa con el fondo detectado, nunca como invisible por sí solo.
- No se buscan marcas de agua estadísticas de modelos de lenguaje. Esa capacidad no está disponible, lo cual no es un resultado negativo.
