# Propuesta viejo/nuevo: figuras y diagramas de toda la tesis (consejo de redacción)

**Estado:** pendiente de aprobación. Nada aplicado.

Lo que más pesa: la figura `fig16` se imprime a 3.6 cm de ancho (no se lee ninguna etiqueta) y los paneles B y C de `fig11` están mal dibujados (las barras de una palabra caen encima de las de la siguiente); el diagrama de la fase temprana sale a escala 0.41 (letra de unos 3 pt) y el de la fase madura no dibuja ni τ ni la compuerta de contenido; las cuatro figuras de calibración dicen «Agente ganador», «E32 m=32 binary» y nombres en inglés que no son los de la Tabla 2, y en `fig02` la leyenda tapa justo lo que afirma el pie. Ninguna figura necesita datos nuevos: con el script corregido y la opción `--solo` de C0, las seis PNG se regeneran en unos 5–6 minutos (casi todo es `fig16`). **No compilé LaTeX ni corrí Python**: el código TikZ y el de matplotlib están listos para probar, no probados.

Numeración: la figura se nombra por su archivo y su `\label`; entre paréntesis, el número que tiene hoy en el PDF. La figura 15 (`fig15_image_rejection.png`) no se toca aquí.

Coordinación con las otras propuestas:
- El pie de `fig02` va sobre el texto de **hechos E4**; el de `fig16`, sobre **hechos E10**; el diagrama de la fase temprana incluye **hechos C3** (PROPN) y el de la fase madura resuelve **hechos C4**.
- El pie nuevo de la fase madura (D2) sustituye al que propone `claridad_03_04` M3 para esa figura: ese pie quitaba τ y la compuerta, que ahora sí se dibujan. El pie de la figura de llenado y el párrafo de cuerpo de M3 quedan para el consolidador de 03.
- Los rótulos de los diagramas que dependen de la **decisión T** (label → etiqueta, encoder/decoder → codificador/decodificador, recall → recuperación, augmentación → variantes) van marcados «(T)»: si el autor rechaza T, se dejan como están.

---

## Parte 0. Cómo regenerar y cuánto cuesta

Tiempos medidos con las marcas de tiempo de `papers_images/en/` de la corrida del 30 oct: `fig01`–`fig11` tardan 2–3 s en total por idioma; `fig12`+`fig13`, unos 4 min; `fig14`+`fig15`, unos 2 min; `fig16`, unos 5 min; cada idioma, unos 11.5 min. El script completo vuelve a hacer todo en inglés y en español aunque la tesis solo usa `papers_images/es/`.

| Archivo (Fig. del PDF) | Función | Datos que lee | ¿En caché? | Tiempo con `--solo` |
|---|---|---|---|---|
| `fig02` (4) | `fig_mature_accuracy` (l. 315) | `papers_images/ablation_rows.csv` (md5 igual a `results/ablation_mdir_bias/ablation_metrics.csv`) | sí | < 1 s |
| `fig03` (5) | `fig_heatmap` (l. 341) | ídem | sí | < 1 s |
| `fig04` (6) | `fig_domain_accuracy` (l. 364) | ídem | sí | < 1 s |
| `fig09` (7) | `fig_winner_distribution` (l. 480) | ídem | sí | < 1 s |
| `fig11` (10) | `fig_semantic_space` (l. 808) | `label_vectors_*.json`; con los cambios de F5 todas las palabras están en esa caché y no se abre el modelo fastText | sí | ~1 s |
| `fig16` (9) | `fig_image_to_labels` (l. 1227) | `models/encoder.pt`, `models/decoder.pt`, memorias de los ocho módulos, `latent_global_stats`, `latent_energy_threshold.json`, `data/eth80/splits.json` e imágenes de prueba | sí (todo en disco) | ~5 min |

Nada obliga a correr la ablación ni las etapas 5–8. Lo único con cómputo real es `fig16` (codifica imágenes y muestrea recuerdos): conviene correrlo cuando termine el cronómetro de costo.

### C0. Opción `--solo` en `main()` (l. 1322–1344)

**Viejo:**
```python
    for lang in ["en", "es"]:
        T           = TEXTS[lang]
        OUT_CURRENT = out_root / lang
        OUT_CURRENT.mkdir(exist_ok=True)

        print(f"\n[{'2' if lang=='en' else '3'}/3] Generating figures [{lang.upper()}] -> papers_images/{lang}/")
        fig_early_accuracy(agg)
        ...
        fig_image_to_labels()
```
**Nuevo:**
```python
    solo = next((a.split("=", 1)[1].split(",") for a in sys.argv
                 if a.startswith("--solo=")), None)
    figuras = [
        ("fig01", lambda: fig_early_accuracy(agg)),
        ("fig02", lambda: fig_mature_accuracy(agg)),
        ("fig03", lambda: fig_heatmap(agg)),
        ("fig04", lambda: fig_domain_accuracy(agg)),
        ("fig05", lambda: fig_fidelity(agg)),
        ("fig06", lambda: fig_entropy(agg)),
        ("fig07", lambda: fig_registrations(agg)),
        ("fig08", lambda: fig_early_vs_mature(agg)),
        ("fig09", lambda: fig_winner_distribution(agg)),
        ("fig10", lambda: fig_summary_table(agg)),
        ("fig11", fig_semantic_space),
        ("fig12", fig_recognition_heatmap),
        ("fig13", fig_precision_recall),
        ("fig14", fig_recall_grid),
        ("fig15", fig_image_rejection),
        ("fig16", fig_image_to_labels),
    ]
    # Con --solo se generan solo esas figuras y solo en español (las de la tesis)
    for lang in (["es"] if solo else ["en", "es"]):
        T           = TEXTS[lang]
        OUT_CURRENT = out_root / lang
        OUT_CURRENT.mkdir(exist_ok=True)

        print(f"\nGenerating figures [{lang.upper()}] -> papers_images/{lang}/")
        for nombre, f in figuras:
            if solo is None or nombre in solo:
                f()
```
Uso: `python generate_paper_figures.py --solo=fig02,fig03,fig04,fig09,fig11,fig16` y copiar las seis PNG de `papers_images/es/` a `.tex8/figuras/`. Si el coordinador vuelve a correr `fig15`, puede añadirla a la misma lista.

---

## Parte 1. Cambios comunes del script

### C1. Nombres de condición iguales a los de la Tabla 2 (`tab:calibracion`)

Hoy las figuras usan `CONDITION_LABELS` de `run_ablation.py:81` («A Baseline», «B1 Norm/count», «C Balanced M\_dir», «E32 m=32 binary»…). «binary» no describe lo que se corrió: E32/E64 cuantizan **por magnitud** las pistas del directorio en 32/64 niveles (`run_ablation.py:187–191` y 291–292; el contenido sigue en 16), y la tabla dice «Cuantización en 32/64 niveles». Las claves internas (`PALETTE`, `KEY`) no se tocan; solo cambia lo que se imprime.

Añadir en `TEXTS["es"]` (l. 162) y una función después de `pct_fmt` (l. 265):
```python
        "cond": {"A Baseline": "A (cruda)", "B1 Norm/count": "B1", "B2 Norm/sqrt": "B2",
                 "C Balanced M_dir": "C", "D Balanced queries": "D",
                 "E32 m=32 binary": "E32", "E64 m=64 binary": "E64",
                 "F Curated ConceptNet": "F", "G Best (D+B1+F)": "G (D+B1+F)"},
```
```python
def cname(c):
    return T.get("cond", {}).get(c, c)
```
Las descripciones quedan en la Tabla 2, y los pies remiten a ella.

### C2. Textos en `TEXTS["es"]` (l. 162–249)

| Clave | Viejo | Nuevo |
|---|---|---|
| `n_queries` | `"Número de queries (N)"` | `"Consultas de formación ($N$)"` |
| `mature_acc_y` | `"Precisión fase madura"` | `"Precisión madura"` |
| `winner_agent` | `"Agente ganador"` | `"Módulo ganador"` |
| `bins_x` | `"Bin de cuantización"` | `"Nivel de cuantización"` |
| `bins_y` | `"Proporción de features"` | `"Proporción de componentes"` |
| `img2lbl_input` | `"Entrada (pista)"` | `"Entrada"` |
| `img2lbl_recon` | `"Reconstrucción evocada (MAE)"` | `"Reconstrucción evocada"` |
| (nueva) `img2lbl_module` | — | `"módulo"` |
| (nueva) `img2lbl_hit` | — | `"del vocabulario de la clase"` |
| `reg_title`, `recog_x`, `prf_title`, `prf_agent`, `prf_note_fp` | «agente» | «módulo» (figuras que no están en la tesis; se corrige para que no vuelva) |

### C3. Sin títulos internos en las figuras de la tesis

Quitar `ax.set_title(...)` en l. 333, 352, 382 y 505, los `set_title` de los paneles y el `suptitle` de `fig11` (l. 885, 913, 942, 945) y el `suptitle` de `fig16` (l. 1286–1288). Repiten el pie, están en inglés a medias («M\_dir», «queries», «recall MAE») y uno afirma algo que la figura no muestra («la cuantización por magnitud preserva la separación»). En `fig16` además pisa la primera fila.

---

## Parte 2. Figuras PNG

### F1. `fig02_mature_accuracy_vs_N.png` (`fig:mature-vs-n`, Fig. 4)

**Problemas:** la leyenda (9 entradas, l. 337) cubre los puntos de B1, D y G en $N = 50$–200, justo lo que afirma el pie; el eje va de 0 a 110 % para datos entre 66 y 94 %; la línea de F se dibuja encima de la de A (son idénticas); las bandas de A y B1 tienen ancho cero (en el CSV, A, B1, B2, C, E32, E64 y F dan el mismo valor con las 5 semillas; solo D y G varían), así que la única banda visible es la de G.

**Código** (`fig_mature_accuracy`, l. 315–338):
```python
def fig_mature_accuracy(agg):
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    KEY = {"A Baseline", "G Best (D+B1+F)", "B1 Norm/count"}
    for cond, sub in agg.groupby("condition"):
        if cond == "F Curated ConceptNet":   # idéntica a A; lo dice el pie
            continue
        sub = sub.sort_values("N")
        lw = 2.8 if cond in KEY else 1.3
        ls = "-"  if cond in KEY else "--"
        mk = "o"  if cond in KEY else "s"
        ax.plot(sub["N"], sub["mature_accuracy_mean"],
                marker=mk, linewidth=lw, linestyle=ls,
                label=cname(cond), color=PALETTE.get(cond, "#bdc3c7"))
        if cond == "G Best (D+B1+F)":
            ax.fill_between(sub["N"],
                            sub["mature_accuracy_mean"] - sub["mature_accuracy_std"],
                            sub["mature_accuracy_mean"] + sub["mature_accuracy_std"],
                            alpha=0.15, color=PALETTE[cond])
    ax.set_xlabel(T["n_queries"])
    ax.set_ylabel(T["mature_acc_y"])
    ax.set_xticks(N_VALUES)
    ax.set_ylim(0.6, 1.0)
    ax.yaxis.set_major_formatter(pct_fmt)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=8, frameon=False)
    savefig("fig02_mature_accuracy_vs_N.png", fig)
```
(El valor más bajo es A en $N = 50$, 66.0 %; la banda de G no baja de 87.5 %: el eje de 60 a 100 % no corta nada.)

**LaTeX** `05:62`: `width=0.72\textwidth` → `width=0.9\textwidth`.

**Pie** (`05:63–66`; sobre el texto de hechos E4):
- **Viejo (tras hechos E4):** `\caption{Precisión madura en función de $N$ por condición de lectura. Entre las condiciones que solo cambian la lectura, B1 es la mejor en todo el rango; la cruda (A) queda sistemáticamente por debajo. G, que además balancea las consultas, queda por encima de B1 en todo el rango; D lo supera en $N = 50$ y $200$.}`
- **Nuevo:**
```latex
    \caption{Precisión madura en función de $N$ para las condiciones de la
    Tabla~\ref{tab:calibracion} ($N$ consultas del banco de 411, media de 5 semillas; la
    banda es $\pm 1$ desviación estándar de G).
    Entre las condiciones que solo cambian la lectura, B1 es la mejor en todo el rango y
    la cruda (A) queda por debajo.
    G, que además balancea las consultas, queda por encima de B1 en todo el rango; D lo
    supera en $N = 50$ y $200$.
    F coincide con A en todos los puntos y no se dibuja.}
```
- **Por qué:** dice de dónde salen los datos, qué es la banda y por qué falta F.
- **Fuente:** `results/ablation_mdir_bias/ablation_metrics.csv` (F = A en los cuatro $N$; desviación estándar de G 4.2, 3.7, 0.6 y 0.3 puntos; cero en A y B1).

### F2. `fig03_heatmap_condition_N.png` (`fig:heatmap-condicion`, Fig. 5)

**Problemas:** la escala rojo-amarillo-verde va de 0 a 1 y todos los valores están entre 66 y 94 %, así que todas las celdas son casi del mismo verde (y en gris no se distinguen); `f"{val:.0%}"` imprime 88 % para E32 (88.5) y 94 % para G (93.5), mientras la Tabla 2 dice 88.5 y 93.5.

**Código** (`fig_heatmap`, l. 341–361; añadir `from matplotlib.ticker import PercentFormatter` en la cabecera, l. 23):
```python
def fig_heatmap(agg):
    cond_order = list(CONDITION_LABELS.values())
    pivot = agg.pivot_table(index="condition", columns="N",
                            values="mature_accuracy_mean").reindex(cond_order)
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    im = ax.imshow(pivot.values, aspect="auto", cmap="viridis", vmin=0.6, vmax=1.0)
    ax.set_xticks(range(len(N_VALUES)))
    ax.set_xticklabels([f"$N={n}$" for n in N_VALUES])
    ax.set_yticks(range(len(cond_order)))
    ax.set_yticklabels([cname(c) for c in cond_order], fontsize=8)
    for i in range(len(cond_order)):
        for j in range(len(N_VALUES)):
            val = pivot.values[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"{val * 100:.1f}", ha="center", va="center",
                        fontsize=8, color="white" if val < 0.85 else "black")
    cb = plt.colorbar(im, ax=ax, fraction=0.035, format=PercentFormatter(1.0))
    cb.set_label(T["mature_acc_y"])
    ax.grid(False)
    savefig("fig03_heatmap_condition_N.png", fig)
```
**LaTeX** `05:72`: `width=0.9\textwidth` → `width=0.75\textwidth`.

**Pie** (`05:73–74`):
- **Viejo:** `\caption{Mapa de calor de precisión madura por condición experimental y número de consultas $N$.}`
- **Nuevo:**
```latex
    \caption{Precisión madura (\%) por condición de la Tabla~\ref{tab:calibracion} y
    número de consultas de formación $N$ (mismos datos que la
    Figura~\ref{fig:mature-vs-n}).
    Hasta $N = 200$, A, C, E32, E64 y F quedan entre 66 y 77\%; B1 sube de 78 a 93\%, y
    D y G pasan del 86\% en todo el rango.}
```
- **Por qué:** el pie de hoy repite el título y no dice qué mirar (junta `figuras` 5.2 y `claridad_05` M4).
- **Fuente:** `ablation_metrics.csv`: hasta $N = 200$, A/F 66.0–70.0, C 74.0–77.0, E32 68.0–72.0, E64 68.0–73.5; B1 78.0 → 93.0; mínimo de D 86.5, de G 90.0.
- **Alternativa:** quitar la figura (da las mismas 36 cifras que la Figura 4 y la Tabla 2) y la frase que la cita en `05:21–22`. No la recomiendo como primera opción porque es la única que da las cifras de todos los $N$.

### F3. `fig04_domain_accuracy_N80.png` (`fig:dominio`, Fig. 6)

**Problemas:** el recuadro «Dominio» (l. 385) tapa las barras de A y B1 de apple, car, cow y cup, que `05:79–82` manda a mirar; los rótulos del eje x están en inglés y girados; el nombre dice N80 y la figura es de $N = 400$.

**Código** (`fig_domain_accuracy`, l. 364–387; solo las líneas que cambian):
```python
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ...
    ax.set_xticks(x)
    ax.set_xticklabels([cname(c) for c in n80["condition"]], fontsize=8)
    ax.set_ylabel(T["domain_acc_y"])
    ax.set_ylim(0, 1.05)
    ax.yaxis.set_major_formatter(pct_fmt)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=8,
              fontsize=8, frameon=False)
    ax.axhline(1.0, color="#636e72", lw=0.8, linestyle="--", alpha=0.5)
    savefig("fig04_domain_accuracy_N400.png", fig)
```
(se borran `ax.set_title` y la leyenda con título; la leyenda pasa encima del eje, donde ya no hay título).

**LaTeX** `05:90`: `\includegraphics[width=0.85\textwidth]{fig04_domain_accuracy_N80.png}` → `\includegraphics[width=\textwidth]{fig04_domain_accuracy_N400.png}`.

**Pie** (`05:91`):
- **Viejo:** `\caption{Precisión madura por dominio y condición ($N = 400$).}`
- **Nuevo:**
```latex
    \caption{Precisión madura por dominio y condición de la
    Tabla~\ref{tab:calibracion} ($N = 400$, media de 5 semillas).
    \texttt{pear} es el dominio más bajo en todas las condiciones; la lectura B1 lo lleva
    de 40 a 76\% respecto de la cruda (A), y a \texttt{horse} de 68 a 88\%.}
```
- **Fuente:** `ablation_metrics.csv`, $N = 400$: `mature_acc_pear` A 0.400, B1 0.760 (y el menor de las nueve condiciones: B2 0.62, C 0.48, D 0.508, E32 0.54, E64 0.58, F 0.40, G 0.796); `mature_acc_horse` A 0.680, B1 0.880.

### F4. `fig09_winner_distribution_N80.png` (`fig:winner`, Fig. 7)

**Problemas:** «Agente ganador» (regla 1); la leyenda (l. 508) tapa los segmentos de tomato y pear de D, E32, E64, F y G; las cifras dentro de las barras redondean 13.75 a «14%» mientras el texto dice 13.8; nombre N80.

**Código** (`fig_winner_distribution`, l. 480–509; líneas que cambian):
```python
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ...
            if v > 0.06:
                ax.text(xi, b + v / 2, f"{v * 100:.1f}",
                        ha="center", va="center", fontsize=7,
                        color="white", fontweight="bold")
    ...
    ax.set_xticks(x)
    ax.set_xticklabels([cname(c) for c in n80["condition"]], fontsize=8)
    ax.set_ylabel(T["winner_y"])
    ax.set_ylim(0, 1.0)
    ax.yaxis.set_major_formatter(pct_fmt)
    ax.legend(title=T["winner_agent"], loc="lower center", bbox_to_anchor=(0.5, 1.01),
              ncol=9, fontsize=8, frameon=False)
    savefig("fig09_winner_distribution_N400.png", fig)
```
**LaTeX** `05:106`: `\includegraphics[width=0.85\textwidth]{fig09_winner_distribution_N80.png}` → `\includegraphics[width=\textwidth]{fig09_winner_distribution_N400.png}`.

**Pie** (`05:107–108`):
- **Viejo:** `\caption{Distribución de módulos ganadores en fase madura por condición ($N = 400$). La línea discontinua marca el ideal balanceado de $1/8 = 12.5\%$.}`
- **Nuevo:**
```latex
    \caption{Distribución de módulos ganadores en fase madura por condición de la
    Tabla~\ref{tab:calibracion} ($N = 400$, media de 5 semillas; cifras en \%, sin cifra
    en los segmentos menores del 6\%).
    La línea discontinua marca el ideal balanceado de $1/8 = 12.5\%$, con el que se
    compara el segmento inferior (\texttt{apple}).}
```
- **Por qué:** la línea del ideal solo se compara con el segmento de abajo; el pie de hoy no lo dice.

### F5. `fig11_semantic_space.png` (`fig:espacio-semantico`, Fig. 10)

**Problemas:**
- Paneles B y C mal dibujados: `width = 0.26` con 8 dominios (l. 898, 922) hace que cada grupo ocupe 2.08 unidades con separación 1, así que las barras de una palabra (o de un nivel) caen encima de las de las dos siguientes; los ticks no están en el centro de su grupo.
- Panel A: anota las 168 etiquetas (mancha ilegible), superpone los rótulos «Centroide …», y dibuja «engine», «motor» y «machine» como tokens «Cross-domain» con una flecha «Semántica correcta». *engine* y *motor* son hoy etiquetas de `car` (`label_vectors_car.json`): la historia de la polisemia que cuenta el panel ya no existe (la Tabla 2 dice que el vocabulario no contiene los labels polisémicos).
- Panel B mide la similitud de *engine*, *motor*, *machine*, *computer* y *mac* con cada clase: ninguna frase de la tesis usa ese panel.
- Panel C: título «quantize\_binary(v, m=16)» (nombre de función; la cuantización es por magnitud), líneas rojas en los extremos (resto de la comparación con el signo) y leyenda encima de las barras.

**Propuesta:** dos paneles (A y C), sin panel B; en A solo se rotulan las etiquetas que comparten dos o tres clases; en C, líneas en vez de barras.

**Código** (`fig_semantic_space`, sustituye l. 808–946):
```python
def fig_semantic_space():
    from quantizer import quantize_binary
    from stage6_interaction import get_fasttext_vector, load_all_vectors

    words, vecs, domains = _load_all_label_vectors()
    vc = load_all_vectors()

    pca   = PCA(n_components=2, random_state=42)
    pts2d = pca.fit_transform(vecs)
    var   = pca.explained_variance_ratio_
    idx = {d: [i for i, dom in enumerate(domains) if dom == d] for d in SYS_CLASSES}
    centroids = {d: pts2d[idx[d]].mean(axis=0) for d in SYS_CLASSES}
    # Solo se rotulan las etiquetas que están en más de una clase
    compartidas = sorted({w for w in words
                          if sum(w in vc[c] for c in SYS_CLASSES) > 1})

    DOM_MARKERS = {"apple": "o", "car": "^", "cow": "P", "cup": "X",
                   "dog": "*", "horse": "s", "pear": "v", "tomato": "d"}

    fig = plt.figure(figsize=(9, 4.2))
    gs  = gridspec.GridSpec(1, 2, width_ratios=[1.35, 1], wspace=0.28)
    ax_pca, ax_bins = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

    for dom in SYS_CLASSES:
        pts = pts2d[idx[dom]]
        _add_convex_hull(ax_pca, pts, DOMAIN_COLOR[dom])
        ax_pca.scatter(pts[:, 0], pts[:, 1], c=DOMAIN_COLOR[dom],
                       marker=DOM_MARKERS[dom], s=30, alpha=0.8, zorder=3,
                       label=dom, edgecolors="white", linewidth=0.4)
        ax_pca.scatter(*centroids[dom], marker="*", s=220, color=DOMAIN_COLOR[dom],
                       edgecolors="black", linewidth=0.8, zorder=5)
    for w in compartidas:
        ax_pca.annotate(w, pts2d[words.index(w)], fontsize=8,
                        xytext=(3, 3), textcoords="offset points", zorder=6)
    ax_pca.set_xlabel(f"PC1 ({var[0]:.1%} var.)")
    ax_pca.set_ylabel(f"PC2 ({var[1]:.1%} var.)")
    ax_pca.grid(True, alpha=0.2)

    M = 16
    for dom in SYS_CLASSES:
        v_q = quantize_binary(np.array(get_fasttext_vector(dom, vc)), M)
        cnt = np.bincount(v_q.astype(int), minlength=M) / v_q.size
        ax_bins.plot(np.arange(M), cnt, marker="o", ms=3, lw=1.2,
                     color=DOMAIN_COLOR[dom])
    ax_bins.set_xticks(range(0, M, 3))
    ax_bins.set_xlabel(T["bins_x"])
    ax_bins.set_ylabel(T["bins_y"])

    handles, labels = ax_pca.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 1.0),
               ncol=8, fontsize=8, frameon=False)
    savefig("fig11_semantic_space.png", fig)
```
Las etiquetas compartidas que salen de `label_vectors_*.json` son seis: *fruit* (apple, pear, tomato), *pome* (apple, pear), *red* (apple, tomato), *animal* y *mammal* (cow, dog, horse) y *table* (cup, dog). En C se usa la etiqueta con el nombre de la clase (antes, `car` usaba *engine*); las ocho están en el vocabulario de su clase, así que la función no abre el modelo fastText.

**Pie** (`06:30–32`):
- **Viejo:** `\caption{Análisis del espacio semántico de los labels de las ocho clases: proyección PCA 2D con centroides de dominio y tokens ambiguos, similitud coseno de tokens problemáticos y ocupación de los 16 niveles de la cuantización por magnitud.}`
- **Nuevo:**
```latex
    \caption{Espacio semántico de las etiquetas de llenado de las ocho clases (vectores
    fastText del vocabulario de la Sección~\ref{sec:pipeline-semantico}).
    Izquierda: proyección PCA 2D, con la envolvente y el centroide (estrella) de cada
    clase; se rotulan solo las etiquetas que comparten dos o tres clases (\textit{fruit},
    \textit{pome}, \textit{red}, \textit{animal}, \textit{mammal} y \textit{table}).
    Derecha: proporción de las 300 componentes que cae en cada uno de los 16 niveles de
    la cuantización por magnitud, para la etiqueta con el nombre de cada clase.}
```
(«etiquetas» depende de la decisión T.) El pie no da el porcentaje de varianza: sin las tres palabras extra, el PCA cambia y la cifra está en los ejes de la figura nueva.

**Ubicación (opcional):** sin el panel B la figura solo describe la representación; `claridad_06_07` M13 propone moverla al final de `sec:pipeline-semantico` en 04 (donde `04:82–83` ya la cita). Es mover el bloque `06:27–34` detrás de `04:83`; `06:23` sigue citándola por `\ref`.

### F6. `fig16_image_to_labels.png` (`fig:imagen-etiquetas`, Fig. 9)

**Problemas:** 16 filas × 3 columnas a `height=0.78\textheight` dan una tira de 3.6 cm de ancho con imágenes de 1.1 cm y texto de ~1.5 pt; el `suptitle` (puesto después de `tight_layout`) pisa la primera fila; «domain-hit ✓», «recall MAE», «(MAE)»; y la figura no aplica el umbral τ que el sistema aplica antes de cualquier memoria (la figura 15 ya lo aplica, l. 1157–1166).

**Código** (`fig_image_to_labels`, sustituye l. 1227–1290):
```python
def fig_image_to_labels():
    """Salida semántica: imagen → reconstrucción evocada → etiquetas."""
    import random
    from PIL import Image
    from stage5_fill import quantize_latent_global
    from stage7_bidirectional import (evoke_labels, latent_energy_threshold,
                                      latent_has_energy)
    classes = list(SYS_CLASSES)
    enc, dec, agents, g_min, g_max, all_vecs, vocab, splits = _load_visual_assets()
    tau = latent_energy_threshold()
    random.seed(0)   # recuerdo muestreado reproducible; la semilla no se ajusta

    samples = []
    for cls in classes:
        taken = 0
        for p in splits[cls]["test"]:
            z = _encode_img(Image.open(p), enc)
            if not latent_has_energy(z, tau):
                continue
            z_q = quantize_latent_global(z, g_min, g_max, 32)
            sc = _visual_scores(agents, z_q, classes)
            if max(sc.values()) == 0:
                continue
            w = max(sc, key=sc.get)
            labels = evoke_labels(agents[w], z_q, all_vecs)
            hit = any(lbl in vocab[cls] for lbl in labels)
            recon = _mae_reconstruction(agents[w], z_q, g_min, g_max, dec)
            samples.append((Image.open(p).convert("RGB").resize((128, 128)),
                            recon, w, labels, hit))
            taken += 1
            if taken >= 2:
                break

    filas = max((len(samples) + 1) // 2, 1)
    fig, axes = plt.subplots(filas, 6, figsize=(9, 1.25 * filas), squeeze=False)
    for ax in axes.flat:
        ax.axis("off")
    for r, (inp, recon, w, labels, hit) in enumerate(samples):
        ax0, ax1, ax2 = axes[r // 2][3 * (r % 2): 3 * (r % 2) + 3]
        ax0.imshow(np.asarray(inp))
        if recon is not None:
            ax1.imshow(np.clip(recon, 0, 1))
        if r < 2:
            ax0.set_title(T.get("img2lbl_input", "Input"), fontsize=9)
            ax1.set_title(T.get("img2lbl_recon", "Evoked reconstruction"), fontsize=9)
        ax2.text(0.0, 0.92, f"{T.get('img2lbl_module', 'module')}: {w}",
                 fontsize=9, fontweight="bold", va="top")
        ax2.text(0.0, 0.70, "\n".join(labels) if labels else "—",
                 fontsize=8.5, va="top")
        ax2.text(0.0, 0.02, f"{T.get('img2lbl_hit', 'in class vocabulary')}: "
                            f"{'sí' if hit else 'no'}",
                 fontsize=8, color="#27ae60" if hit else "#c0392b")
    savefig("fig16_image_to_labels.png", fig)
```
El recuerdo es muestreado (el código de Pineda y Morales usa `random.random()`), así que cada corrida da etiquetas distintas. `random.seed(0)` solo hace la figura reproducible; si se prefiere no fijar semilla, se quita la línea, y en ambos casos **la cuenta del pie se lee de la figura nueva**. Docstring de `_mae_reconstruction` (l. 1121–1123), de paso: «La lectura latente de la hetero (`mem_dom_R`) completa la percepción y el decoder la dibuja; no es la imagen de entrada.»

**LaTeX** `05:383`: `\includegraphics[height=0.78\textheight,keepaspectratio]{fig16_image_to_labels.png}` → `\includegraphics[width=\textwidth]{fig16_image_to_labels.png}` (unos 16.6 × 18.4 cm; imágenes de unos 2 cm y texto de 6–7 pt; sigue en `figure[p]`).

**Pie** (`05:384–390`; la última frase es la de hechos E10):
- **Viejo:** `\caption{Salida semántica imagen $\to$ etiquetas (dos ejemplos por clase). Por cada imagen aceptada por el contenido (el módulo es el de mayor soporte, sin pasar por el directorio): entrada (pista), reconstrucción evocada por la memoria (no la entrada) y las etiquetas recuperadas, con marca de coincidencia con el vocabulario de la clase real. En 15 de los 16 ejemplos alguna etiqueta es del dominio; en el restante (\texttt{dog}) la recuperación no devuelve etiquetas. Sobre el test completo, con el directorio, la evocación acierta el 97.4\%.}`
- **Nuevo:**
```latex
    \caption{Salida semántica imagen $\to$ etiquetas: las dos primeras imágenes de test de
    cada clase que pasan el umbral de energía y que algún módulo contiene (el de mayor
    soporte, sin pasar por el directorio).
    Por imagen: la entrada, la reconstrucción que evoca la memoria (no la entrada) y las
    tres etiquetas recuperadas, con la marca de si alguna es del vocabulario de la clase
    real.
    En [X] de los 16 ejemplos alguna etiqueta es del dominio[; en el restante, …].
    Con el directorio, sobre las primeras 15 imágenes de test de cada clase que el ruteo
    acepta (116), la evocación acierta el 97.4\% (113).}
```
- **Por qué:** dice qué imágenes se muestran (antes «aceptada por el contenido» sin el umbral) y deja la cuenta para leerla de la figura regenerada. Hoy es 15 de 16 con un `dog` sin etiquetas; puede cambiar.

---

## Parte 3. Diagramas TikZ (`03_arquitectura.tex`)

No compilé. Las medidas salen de sumar `minimum width` y `node distance`; conviene compilar y ajustar distancias si algo se encima. El `\textwidth` es de 16.6 cm (carta, márgenes de 2.5 cm).

### D1. Fase temprana (`fig:arq-temprana`, Fig. 2): de escala 0.41 a ~0.89

**Problema:** la cadena horizontal mide unos 39 cm (consulta → spaCy → fastText → $\mathbf{v}_q$ → TME → módulos → argmax → Recall → Decoder → Imagen); `\resizebox` la reduce a 0.41 y el `\scriptsize` queda en ~3 pt.

**Propuesta:** el camino de la consulta baja en una columna a la izquierda, la salida baja en otra a la derecha y el centro queda TME → módulos → ganador. Las dos rutas grises punteadas («módulo de entrada», «ganador $g$») se sustituyen por la nota que ya decía lo mismo. Ancho natural ~18.6 cm, escala ~0.89, letra `\footnotesize` a ~8 pt. Incluye hechos C3 (PROPN) y, (T), «Recuperación $\beta$» y «Decodificador».

**Viejo:** `03:192–299`, desde `\begin{figure}[H]` (el del comentario «Diagrama 2: Fase temprana») hasta `\end{figure}`.

**Nuevo:**
```latex
\begin{figure}[H]
\centering
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
    node distance = 0.55cm and 1.0cm,
    box/.style = {
        rectangle, draw, line width=0.4pt,
        align=center, font=\footnotesize,
        minimum height=0.9cm, minimum width=2.5cm,
        inner sep=3pt
    },
    mod/.style = {box, minimum height=1.2cm, minimum width=3.2cm},
    arr/.style = {-{Stealth[length=2mm]}, line width=0.4pt},
    lbl/.style = {font=\footnotesize, midway, above=1pt, fill=white, inner sep=1pt},
]

% ---- Columna izquierda: de la consulta a la pista ----
\node[box] (query) {Consulta de texto\\(entra por un\\módulo al azar)};
\node[box, below=of query] (spacy) {spaCy: lemas\\NOUN/ADJ/PROPN\\+ rescate léxico};
\node[box, below=of spacy] (vq) {fastText, $v/S$,\\16 niveles: $\mathbf{v}_q$};

% ---- TME ----
\node[box, right=1.1cm of vq, minimum height=1.4cm] (tme) {TME\\(mediador)};

% ---- Módulos ----
\node[mod, right=1.5cm of tme] (A1) {Módulo $k$\\$w$ y $\Pi$ de $M^H$};
\node[mod, above=0.9cm of A1] (A0) {Módulo 0 (\texttt{apple})\\$w$ y $\Pi$ de $M^H$};
\node[mod, below=0.9cm of A1] (A7) {Módulo 7 (\texttt{tomato})\\$w$ y $\Pi$ de $M^H$};
\node at ($(A0.south)!0.5!(A1.north)$) {$\vdots$};
\node at ($(A1.south)!0.5!(A7.north)$) {$\vdots$};

% ---- Ganador y salida ----
\node[box, right=1.4cm of A1] (argmax) {ganador\\$g = \arg\max_k \sum s_k$};
\node[box, right=1.0cm of argmax] (rec) {Recuperación $\beta$\\$\hat{\mathbf{z}}_q$};
\node[box, below=of rec] (dec) {Decodificador};
\node[box, below=of dec] (img) {Imagen\\recuperada};

% ---- Actualización del directorio ----
\node[box, below=1.0cm of tme, minimum width=3.2cm] (dirup)
    {Actualización del\\directorio $(\mathbf{v}_q \to g)$};
\node[font=\footnotesize\itshape, below=0.15cm of dirup, text width=4.2cm, align=center]
    {Registran el módulo de entrada,\\el ganador y el TME\\(\textit{directory updating})};

% ---- Flechas ----
\draw[arr] (query) -- (spacy);
\draw[arr] (spacy) -- (vq);
\draw[arr] (vq) -- (tme);
\draw[arr] (tme.east) -- (A0.west);
\draw[arr] (tme.east) -- (A1.west);
\draw[arr] (tme.east) -- (A7.west);
\draw[arr] (A0.east) -| node[pos=0.25, above, font=\footnotesize]{$s_0$} (argmax.north);
\draw[arr] (A1.east) -- node[lbl]{$s_k$} (argmax.west);
\draw[arr] (A7.east) -| node[pos=0.25, below, font=\footnotesize]{$s_7$} (argmax.south);
\draw[arr] (argmax) -- (rec);
\draw[arr] (rec) -- (dec);
\draw[arr] (dec) -- (img);
\draw[arr] (tme) -- (dirup);

\end{tikzpicture}%
}
\caption{Fase temprana: aprendizaje mediado por el TME.
La consulta se codifica con fastText y cuantización por magnitud, el TME la difunde a
los ocho módulos, cada módulo devuelve una puntuación $s_k$ con la proyección de su
memoria heteroasociativa, ponderada por los pesos que lee de ella misma, y el ganador
$g = \arg\max_k \sum s_k$ ejecuta la recuperación $\beta$ hacia el espacio latente.
Registran el par $(\mathbf{v}_q, g)$ el módulo por el que entró la consulta (al azar),
el ganador y el TME; los demás módulos no presenciaron la transacción.}
\label{fig:arq-temprana}
\end{figure}
```
El pie solo cambia «memoria hetero» → «memoria heteroasociativa» (`claridad_03_04` B7, `consistencia` 1.11).

### D2. Fase madura (`fig:arq-madura`, Fig. 3): τ y la compuerta dibujados

**Problema:** el pie y el texto (`03:475–478`, `491–498`) describen el umbral de energía τ y la compuerta de contenido del destino; el dibujo no tiene ninguno de los dos (hechos C4). Además mide ~31.6 cm (escala 0.53), la llave de salida dice «imagen, labels, ubicación» («ubicación» no aparece en otro lugar) y la salida de imagen (evocación de etiquetas) no se ve.

**Propuesta:** fila principal consulta → τ (solo imagen) → módulo de entrada → directorios → destino; debajo del destino, la compuerta (solo texto) y la salida de cada modalidad; un solo RECHAZO bajo los directorios recibe las tres flechas (τ, sin soporte, el destino no contiene la pista); el TME, en gris, arriba. Ancho natural ~17.9 cm, escala ~0.93, letra ~8.3 pt.

**Viejo:** `03:304–388`, desde `\begin{figure}[H]` (el del comentario «Diagrama 3: Fase madura») hasta `\end{figure}`.

**Nuevo:**
```latex
\begin{figure}[H]
\centering
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
    node distance = 0.6cm and 0.8cm,
    box/.style = {
        rectangle, draw, line width=0.4pt,
        align=center, font=\footnotesize,
        minimum height=1.0cm, minimum width=2.2cm,
        inner sep=3pt
    },
    boxg/.style = {box, draw=gray, dashed, text=gray},
    arr/.style  = {-{Stealth[length=2mm]}, line width=0.4pt},
    arrg/.style = {arr, draw=gray, dashed},
    lbl/.style  = {font=\footnotesize, midway, above=1pt, fill=white, inner sep=1pt},
]

% ---- Fila principal ----
\node[box] (query) {Consulta\\(texto o imagen)};
\node[box, right=of query] (tau) {Solo imagen:\\$\|\mathbf{z}\| \geq \tau$};
\node[box, right=of tau] (entrada) {Módulo de\\entrada};
\node[box, right=1.4cm of entrada] (mdir)
    {$M_{\mathrm{dir}}$ / $M^R_{\mathrm{dir}}$ propios\\y de los conocidos\\lectura B1, $\xi{=}0$};
\node[box, right=1.4cm of mdir] (destino) {Módulo\\destino};

% ---- Compuerta, salida y rechazo ----
\node[box, below=1.2cm of destino] (gate) {Solo texto: ¿su\\contenido contiene\\la pista?};
\node[box, below=1.0cm of gate] (salida)
    {Texto: recuperación $\beta$\\y decodificador $\to$ imagen\\Imagen: evocación $\to$ etiquetas};
\node[box] (rechazo) at (mdir |- gate) {RECHAZO\\(el grupo no inventa\\referentes)};

% ---- TME fuera del circuito ----
\node[boxg, above=1.0cm of entrada] (tme) {TME};
\node[font=\footnotesize\itshape, text=gray, right=0.2cm of tme, align=left]
    {fuera del circuito:\\el mediador ya no participa};

% ---- Flechas ----
\draw[arr] (query) -- (tau);
\draw[arr] (tau) -- (entrada);
\draw[arr] (entrada) -- node[lbl]{$\mathbf{v}_q$ / $\mathbf{z}_q$} (mdir);
\draw[arr] (mdir) -- node[lbl]{soporte} (destino);
\draw[arr] (destino) -- (gate);
\draw[arr] (gate) -- node[right, font=\footnotesize]{sí} (salida);
\draw[arr] (gate) -- node[above, font=\footnotesize]{no} (rechazo);
\draw[arr] (mdir) -- node[right, font=\footnotesize]{sin soporte} (rechazo);
\draw[arr] (tau.south) |- node[pos=0.25, left, font=\footnotesize]{$\|\mathbf{z}\| < \tau$} (rechazo.west);
\draw[arrg] (entrada) -- (tme);

\end{tikzpicture}%
}
\caption{Fase madura: recuperación punto a punto.
La consulta entra por un módulo (al azar en texto; en la evaluación visual, uno que no
es el especialista).
Una imagen cuyo latente no alcanza la energía mínima $\tau$ se rechaza antes de
cualquier memoria.
El módulo de entrada suma la lectura B1 de su directorio de la modalidad de la pista
($M_{\mathrm{dir}}$ o $M^R_{\mathrm{dir}}$, ambos con $\xi{=}0$) y la de los
directorios de los módulos que conoce, y reenvía al de mayor puntuación sin pasar por
el TME (en gris); si nadie en ese círculo tiene soporte, la consulta pasa a los
conocidos.
En texto, el destino responde solo si su memoria de contenido contiene la pista.
Si ningún directorio alcanzable tiene soporte, o el destino no contiene la pista, el
sistema rechaza: el grupo no inventa referentes.}
\label{fig:arq-madura}
\end{figure}
```
- **Por qué del pie:** el de hoy dice lo mismo pero en otro orden (τ al final); el nuevo sigue el dibujo de izquierda a derecha. Sustituye al pie de `claridad_03_04` M3 para esta figura, que quitaba τ y la compuerta.
- **Fuente:** `src/stage7_bidirectional.py:225–228` (τ antes de cuantizar, en la fase B); `src/stage8_mature.py:93–102` (doble compuerta solo en texto); la salida de imagen es la evocación de `03:520–539`.

### D3. Llenado (`fig:arq-llenado`, Fig. 1): rótulos

Se lee bien (escala ~0.7); solo rótulos:

| Línea | Viejo | Nuevo |
|---|---|---|
| `03:134` | `{Secuencia\\de labels\\(expandida por\\frecuencia)}` | `{Secuencia\\de etiquetas\\(expandida por\\frecuencia)}` (T) |
| `03:137` | `{ETH-80\\8 clases\\200 imágenes/clase\\(+ augmentación)}` | `{ETH-80\\8 clases\\200 imágenes/clase\\(16 variantes)}` (T; `consistencia` 1.4) |
| `03:138` | `{Encoder\\ResNet18\\$128\!\times\!128$}` | `{Codificador\\ResNet18\\$128\!\times\!128$}` (T) |
| `03:144` | `{$M^H_{\mathrm{dom}}$\\hetero\\$(300,16\!\leftrightarrow\!64,32)$}` | `{$M^H_{\mathrm{dom}}$\\heteroasociativa\\$(300,16\!\leftrightarrow\!64,32)$}` |
| `03:147` | `node[lbl]{labels,\\frec.}` | `node[lbl]{etiquetas,\\frec.}` (T) |
| `03:171` | `\caption{Llenado de la memoria de contenido (etapas 3--5).` | `\caption{Llenado de la memoria de contenido.` (la tesis no define esa numeración; `figuras` 1.2, `consistencia` 6.4, `claridad_03_04` M4) |

---

## Parte 4. Figuras y tablas sin `\ref`

`fig:arq-temprana`, `fig:arq-madura` y `tab:capacidad` no se citan en ninguna parte (las demás etiquetas tienen al menos una `\ref`).

### R1. `03:94–96`
- **Viejo:** `Los tres diagramas siguientes muestran las tres etapas operativas del sistema:` / `el llenado de la memoria de contenido, la recuperación mediada por el TME (fase temprana)` / `y la recuperación punto a punto (fase madura).`
- **Nuevo:**
```latex
Los tres diagramas siguientes muestran las tres etapas operativas del sistema: el
llenado de la memoria de contenido (Figura~\ref{fig:arq-llenado}), la recuperación
mediada por el TME en la fase temprana (Figura~\ref{fig:arq-temprana}) y la
recuperación punto a punto en la fase madura (Figura~\ref{fig:arq-madura}).
```
- Si el consolidador de 03 adopta el párrafo de cuerpo de `claridad_03_04` M3 (que ya cita las tres figuras), este cambio sobra.

### R2. `05:255`, al final del párrafo
- **Viejo:** `Los \textit{falsos} son imágenes de otras clases presentadas al módulo.`
- **Nuevo:** `Los \textit{falsos} son imágenes de otras clases presentadas al módulo. La Tabla~\ref{tab:capacidad} reúne las métricas para cada $N$.` (con $N_{\mathrm{img}}$ si se aprueba `consistencia` 4.1).

---

## Parte 5. Notación de las lecturas: $M^L$, $M^R$ en toda la tesis

Hoy la figura de llenado, la Tabla 1, `03:30`, `03:402`, `03:527` y `05:362` llaman a las lecturas $M^L$ y $M^R$; la ecuación que las define (`eq:marginal`, `02:234–236`), `02:243` y `05:450–452` las llaman $\mathbf{R}^{L}$ y $\mathbf{R}^{R}$, y ningún lugar dice que son lo mismo.

**Propuesta: $M^L$ y $M^R$.** Es el esquema de nombres de la Tabla 1 ($M^H_{\mathrm{dom}}$, $M_{\mathrm{dir}}$, $M^R_{\mathrm{dir}}$), es el que usan las figuras y las ecuaciones de 03 (`\eta(\mathbf{v}_q, M^L)`), y en 02 $\mathbf{R}$ queda como «la relación de la memoria que se está definiendo». Son cuatro cambios de texto y no se regenera ninguna figura (con $\mathbf{R}^L$ habría que tocar la figura de llenado, la Tabla 1 y cuatro ecuaciones de 03).

| Línea | Viejo | Nuevo |
|---|---|---|
| `02:234` | `\mathbf{R}^{L}[i, k] = \sum_{l=0}^{q} \mathbf{R}[i, j, k, l],` | `M^{L}[i, k] = \sum_{l=0}^{q} \mathbf{R}[i, j, k, l],` |
| `02:236` | `\mathbf{R}^{R}[j, l] = \sum_{k=0}^{m} \mathbf{R}[i, j, k, l],` | `M^{R}[j, l] = \sum_{k=0}^{m} \mathbf{R}[i, j, k, l],` |
| `02:243` | `$\mathbf{R}^{L}$ y $\mathbf{R}^{R}$ son las relaciones de memorias homoasociativas` | `Estas lecturas, $M^{L}$ y $M^{R}$, son las relaciones de memorias homoasociativas` |
| `05:450` | `módulos, a la lectura $\mathbf{R}^{R}$ de la ecuación~\eqref{eq:marginal}.` | `módulos, a la lectura $M^{R}$ de la ecuación~\eqref{eq:marginal}.` |
| `05:452` | `imagen: tiene el mismo soporte que $\mathbf{R}^{L}$, con conteos multiplicados por un` | `imagen: tiene el mismo soporte que $M^{L}$, con conteos multiplicados por un` |

Si se aprueba el cambio de índice $k \to u$ de `consistencia` 4.2, se aplica sobre estas mismas líneas. Esta propuesta sustituye la frase puente de `consistencia` 4.5 («$\mathbf{R}^{L}$ y $\mathbf{R}^{R}$ son las relaciones de las lecturas $M^L$ y $M^R$…») y la de `figuras` 1.1.

---

## Descartado o remitido

- `figuras` 8.1–8.4 y `claridad_05` M22 (figura 15: pie con τ, rótulos «noise/solid/scrambled», rechazadas todas de `apple`, copia desfasada): no se tocan aquí; quedan para quien regenera la figura 15.
- `claridad_05` A6 (decir en el pie que «agente» es módulo) y `claridad_05` M3 (listar en el pie de la Tabla 2 los nombres en inglés de las figuras): sobran si se regeneran las figuras con C1–C2.
- `claridad_03_04` M6 (quitar de la fase temprana la cola β → decodificador → imagen): con dos columnas la escala ya llega a ~0.89, y la cola muestra que en la fase temprana el ganador sí recupera una imagen.
- `figuras` 3.1 (nodo τ entre la entrada y el directorio): el umbral actúa antes del módulo de entrada (`stage7_bidirectional.py:225`), por eso D2 lo pone entre la consulta y la entrada.
- `figuras` 6.3 (rayado por dominio para lectura en gris) y 10.6 (apilar los paneles de `fig11`): de gusto o resueltos por F5.
- `figuras` 4.4 (`[H]` deja media página en blanco): se decide al maquetar con la plantilla de la UACJ.
- `figuras` 10.3 (cambiar las sondas del panel B por *fruit*, *red*, *green*, *round*, *tree*, *animal*): el panel se quita; además *green*, *round* y *tree* solo son etiquetas de `apple`.
- `figuras` 10.5 (pie con «13.9 % de la varianza» y «las frutas y los animales se solapan»): la varianza cambia al rehacer el PCA, y el solapamiento lo interpreta el texto (`06:23–25`), no el pie.
- `figuras` 7.3, `figuras` 4.2 (cifras de G y D en el pie de `fig02`), `cifras_05` A2 y M9: ya están en hechos E3, E4 y E10.
