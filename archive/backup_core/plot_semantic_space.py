"""
Visualización del espacio semántico fastText para todos los labels del experimento.

Muestra:
  - Clusters por dominio (apple / horse / car)
  - Labels compartidos entre dominios
  - Labels de "Apple Inc." (computer, mac, macintosh) que contaminan el dominio apple
  - Tokens de queries que enrutan mal (engine cerca de computer/mac)
  - Por qué "has an engine" activa el agente apple en lugar de car
"""
import json
import sys
from pathlib import Path
from collections import defaultdict

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

CLASSES = ["apple", "horse", "car"]

# -----------------------------------------------------------------------
# Palabras extra para visualizar (tokens de queries que no son labels)
# -----------------------------------------------------------------------
EXTRA_WORDS = [
    "engine",    # token de "has an engine" — deberia ir a car pero va a apple
    "fast",      # token de "fast vehicle"
    "powerful",  # token de "large powerful mammal"
    "large",     # en apple labels (!) — ambiguedad
    "motor",     # sinonimo de engine
    "speed",     # relacionado con car y horse
    "gasoline",  # relacionado con car
    "rider",     # relacionado con horse
    "wheel",     # lemma de "wheels" (en car labels como "wheels")
    "seed",      # lemma de "seeds" (en apple labels como "seeds")
    "hoof",      # lemma de "hooves" (en horse labels como "hooves")
    "leg",       # lemma de "legs" (en horse labels como "legs")
]

# Labels que son ruido polisemico de "Apple Inc."
APPLE_INC_NOISE = {"computer", "mac", "macintosh", "eden"}

# Labels compartidos entre 2+ dominios
SHARED_LABELS = {"red", "four", "large"}

# Tokens de queries que enrutan incorrectamente
MISROUTED_TOKENS = {"engine"}


def load_all_vectors() -> dict:
    """Carga todos los vectores de labels (label_vectors_{cls}.json)."""
    all_vecs = {}
    for cls in CLASSES:
        path = ROOT / f"label_vectors_{cls}.json"
        d = json.loads(path.read_text())
        for word, vec in d.items():
            all_vecs[word] = np.array(vec, dtype=np.float32)
    return all_vecs


def load_extra_vectors(extra_words: list, all_vecs: dict) -> dict:
    """Obtiene vectores para palabras extra no en los labels (via fasttext live lookup)."""
    needed = [w for w in extra_words if w not in all_vecs]
    if not needed:
        return {}

    extra = {}
    try:
        from stage4_fasttext import _stream_lookup
        found = _stream_lookup(set(needed))
        extra.update(found)
    except Exception as e:
        print(f"  Advertencia: no se pudieron cargar vectores extra ({e})")

    return extra


def get_domain_membership(all_vecs: dict) -> dict:
    """Retorna {word: [domains]} indicando en qué dominio(s) aparece cada label."""
    membership = defaultdict(list)
    for cls in CLASSES:
        path = ROOT / f"labels_{cls}.json"
        labels = json.loads(path.read_text())
        for word in labels:
            if word in all_vecs:
                membership[word].append(cls)
    return membership


def reduce_tsne(matrix: np.ndarray, perplexity: int = 8) -> np.ndarray:
    from sklearn.manifold import TSNE
    tsne = TSNE(n_components=2, perplexity=perplexity, max_iter=2000,
                random_state=42, init="pca")
    return tsne.fit_transform(matrix)


def plot_semantic_space(all_vecs: dict, membership: dict,
                        extra_vecs: dict, extra_words: list):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.lines import Line2D

    # ---- Construir matriz de vectores ----
    words = list(all_vecs.keys())
    extra_only = [w for w in extra_vecs if w not in all_vecs]
    all_words = words + extra_only
    matrix = np.stack([
        all_vecs.get(w, extra_vecs.get(w)) for w in all_words
    ])

    print(f"  t-SNE sobre {len(all_words)} palabras x {matrix.shape[1]} dims...")
    coords = reduce_tsne(matrix, perplexity=min(10, len(all_words) // 3))

    # ---- Colores y estilos ----
    DOMAIN_COLORS = {
        "apple": "#e74c3c",
        "horse": "#2980b9",
        "car":   "#27ae60",
        "apple_horse": "#9b59b6",
        "apple_car":   "#e67e22",
        "horse_car":   "#16a085",
        "all":         "#2c3e50",
        "none":        "#95a5a6",
    }

    def get_color(word):
        doms = membership.get(word, [])
        if not doms:
            return DOMAIN_COLORS["none"]
        if set(doms) == {"apple"}:   return DOMAIN_COLORS["apple"]
        if set(doms) == {"horse"}:   return DOMAIN_COLORS["horse"]
        if set(doms) == {"car"}:     return DOMAIN_COLORS["car"]
        if set(doms) >= {"apple", "horse"} and "car" not in doms:
            return DOMAIN_COLORS["apple_horse"]
        if set(doms) >= {"apple", "car"} and "horse" not in doms:
            return DOMAIN_COLORS["apple_car"]
        if set(doms) >= {"horse", "car"} and "apple" not in doms:
            return DOMAIN_COLORS["horse_car"]
        return DOMAIN_COLORS["all"]

    fig, axes = plt.subplots(1, 2, figsize=(20, 9))

    # =========================================================
    # Plot 1: Espacio completo con todos los labels
    # =========================================================
    ax = axes[0]

    for i, word in enumerate(all_words):
        x, y = coords[i]
        color = get_color(word)
        is_noise = word in APPLE_INC_NOISE
        is_extra = word in extra_only
        is_shared = word in SHARED_LABELS
        is_misrouted = word in MISROUTED_TOKENS

        # Marcador
        if is_noise:
            marker, size, zorder = "X", 120, 5
        elif is_misrouted:
            marker, size, zorder = "^", 130, 6
        elif is_shared:
            marker, size, zorder = "D", 100, 4
        elif is_extra:
            marker, size, zorder = "s", 70, 3
        else:
            marker, size, zorder = "o", 60, 2

        ax.scatter(x, y, c=color, marker=marker, s=size, zorder=zorder,
                   edgecolors="white" if not is_noise else "black",
                   linewidths=0.5 if not is_noise else 1.2, alpha=0.9)

        # Etiqueta de texto
        fontsize = 7
        fontweight = "bold" if (is_noise or is_misrouted or is_shared) else "normal"
        fontstyle = "italic" if is_extra else "normal"
        color_text = "black"

        offset_x = 3 if x > coords[:, 0].mean() else -3
        ax.annotate(word, (x, y), fontsize=fontsize, fontweight=fontweight,
                    fontstyle=fontstyle, color=color_text,
                    xytext=(offset_x, 3), textcoords="offset points",
                    ha="left" if offset_x > 0 else "right")

    ax.set_title("Espacio semantico fastText — labels ConceptNet + tokens de queries",
                 fontsize=11, fontweight="bold")
    ax.set_xlabel("t-SNE dim 1")
    ax.set_ylabel("t-SNE dim 2")
    ax.grid(True, alpha=0.15)

    # Leyenda
    legend_elements = [
        mpatches.Patch(color=DOMAIN_COLORS["apple"],       label="Solo apple"),
        mpatches.Patch(color=DOMAIN_COLORS["horse"],       label="Solo horse"),
        mpatches.Patch(color=DOMAIN_COLORS["car"],         label="Solo car"),
        mpatches.Patch(color=DOMAIN_COLORS["apple_car"],   label="apple + car (shared)"),
        mpatches.Patch(color=DOMAIN_COLORS["none"],        label="Extra (query token)"),
        Line2D([0], [0], marker="X", color="w", markerfacecolor="#e74c3c",
               markersize=9, markeredgecolor="black", label="Ruido Apple Inc."),
        Line2D([0], [0], marker="^", color="w", markerfacecolor="#95a5a6",
               markersize=9, label="Token de query mal enrutado"),
        Line2D([0], [0], marker="D", color="w", markerfacecolor="#e67e22",
               markersize=8, label="Label compartido"),
    ]
    ax.legend(handles=legend_elements, fontsize=7.5, loc="lower left",
              framealpha=0.85)

    # =========================================================
    # Plot 2: Zoom en la zona critica (apple labels + engine)
    # =========================================================
    ax2 = axes[1]

    # Encontrar indices de palabras de interes
    words_of_interest = set()
    for w in all_words:
        doms = membership.get(w, [])
        if "apple" in doms:
            words_of_interest.add(w)
    words_of_interest.update({"engine", "motor", "fast", "speed", "wheel",
                               "vehicle", "automobile", "crash", "machine",
                               "transportation", "computer", "mac", "macintosh"})
    words_of_interest = {w for w in words_of_interest if w in all_words}

    indices_interest = [i for i, w in enumerate(all_words) if w in words_of_interest]

    if indices_interest:
        coords_sub = coords[indices_interest]
        words_sub = [all_words[i] for i in indices_interest]

        # Margenes con padding
        pad = 0.15
        x_min, x_max = coords_sub[:, 0].min(), coords_sub[:, 0].max()
        y_min, y_max = coords_sub[:, 1].min(), coords_sub[:, 1].max()
        x_range = x_max - x_min
        y_range = y_max - y_min

        for i_sub, (i_orig, word) in enumerate(zip(indices_interest, words_sub)):
            x, y = coords[i_orig]
            color = get_color(word)
            is_noise = word in APPLE_INC_NOISE
            is_misrouted = word in MISROUTED_TOKENS
            is_car = membership.get(word, []) == ["car"]
            is_shared = word in SHARED_LABELS

            if is_noise:
                marker, size, zorder = "X", 200, 5
            elif is_misrouted:
                marker, size, zorder = "^", 200, 6
            elif is_shared:
                marker, size, zorder = "D", 150, 4
            else:
                marker, size, zorder = "o", 100, 2

            ax2.scatter(x, y, c=color, marker=marker, s=size, zorder=zorder,
                        edgecolors="white" if not is_noise else "black",
                        linewidths=0.8 if not is_noise else 1.5, alpha=0.9)

            fw = "bold" if (is_noise or is_misrouted) else "normal"
            fs = 8.5 if (is_noise or is_misrouted) else 7.5
            ax2.annotate(word, (x, y), fontsize=fs, fontweight=fw,
                         xytext=(4, 4), textcoords="offset points")

        # Dibujar elipse alrededor del cluster de Apple Inc. noise
        noise_indices = [i for i, w in enumerate(all_words) if w in APPLE_INC_NOISE]
        if len(noise_indices) >= 2:
            noise_coords = coords[noise_indices]
            cx, cy = noise_coords.mean(axis=0)
            rx = noise_coords[:, 0].std() * 2.5 + 1.5
            ry = noise_coords[:, 1].std() * 2.5 + 1.5
            ellipse = plt.matplotlib.patches.Ellipse(
                (cx, cy), width=rx*2, height=ry*2,
                fill=False, edgecolor="#e74c3c", linewidth=2,
                linestyle="--", zorder=7, alpha=0.7)
            ax2.add_patch(ellipse)
            ax2.annotate("Cluster\nApple Inc.", (cx + rx, cy), fontsize=8,
                         color="#e74c3c", fontweight="bold",
                         xytext=(8, 0), textcoords="offset points")

        # Dibujar elipse alrededor de los labels de car relevantes
        car_core = {"vehicle", "automobile", "machine", "transportation",
                    "crash", "engine", "motor", "wheel"}
        car_indices = [i for i, w in enumerate(all_words) if w in car_core]
        if len(car_indices) >= 2:
            car_coords = coords[car_indices]
            cx2, cy2 = car_coords.mean(axis=0)
            rx2 = car_coords[:, 0].std() * 2.5 + 1.5
            ry2 = car_coords[:, 1].std() * 2.5 + 1.5
            ellipse2 = plt.matplotlib.patches.Ellipse(
                (cx2, cy2), width=rx2*2, height=ry2*2,
                fill=False, edgecolor="#27ae60", linewidth=2,
                linestyle="--", zorder=7, alpha=0.7)
            ax2.add_patch(ellipse2)
            ax2.annotate("Cluster car\n(espacio semantico)", (cx2, cy2 - ry2),
                         fontsize=8, color="#27ae60", fontweight="bold",
                         xytext=(0, -18), textcoords="offset points", ha="center")

        ax2.set_xlim(x_min - x_range * pad, x_max + x_range * pad)
        ax2.set_ylim(y_min - y_range * pad, y_max + y_range * pad)
        ax2.set_title(
            "Zoom: labels apple vs car\n"
            '"engine" y "computer"/"mac" en el mismo vecindario semantico',
            fontsize=10, fontweight="bold")
        ax2.set_xlabel("t-SNE dim 1")
        ax2.set_ylabel("t-SNE dim 2")
        ax2.grid(True, alpha=0.15)

        legend2 = [
            mpatches.Patch(color=DOMAIN_COLORS["apple"], label="Labels apple"),
            mpatches.Patch(color=DOMAIN_COLORS["car"],   label="Labels car"),
            mpatches.Patch(color=DOMAIN_COLORS["apple_car"], label="Compartido apple+car"),
            Line2D([0], [0], marker="X", color="w", markerfacecolor="#e74c3c",
                   markersize=10, markeredgecolor="black",
                   label="Apple Inc. (ruido polisemico)"),
            Line2D([0], [0], marker="^", color="w", markerfacecolor="#95a5a6",
                   markersize=10, label='"engine": deberia ir a car\npero activa apple'),
        ]
        ax2.legend(handles=legend2, fontsize=8, loc="upper right", framealpha=0.85)

    plt.suptitle(
        "Por que 'engine' activa el agente apple en lugar de car:\n"
        "Proximidad en espacio fastText entre vocabulario tecnologico (Apple Inc.) y terminos mecanicos",
        fontsize=11, fontweight="bold", y=1.01)

    plt.tight_layout()
    out = ROOT / "semantic_space.png"
    plt.savefig(out, dpi=130, bbox_inches="tight")
    print(f"Grafica guardada -> {out.name}")


def run():
    print("Cargando vectores...")
    all_vecs = load_all_vectors()
    membership = get_domain_membership(all_vecs)

    print(f"  {len(all_vecs)} palabras en labels")
    print(f"  Cargando vectores extra para tokens de queries...")
    extra_vecs = load_extra_vectors(EXTRA_WORDS, all_vecs)
    print(f"  {len(extra_vecs)} vectores extra cargados")

    print("  Reduciendo dimensionalidad con t-SNE...")
    plot_semantic_space(all_vecs, membership, extra_vecs, EXTRA_WORDS)
    print("Visualizacion completada.")


if __name__ == "__main__":
    run()
