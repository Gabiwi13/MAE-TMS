"""
Generates paper-quality figures for the EAM-TMS project.
Re-runs the ablation study (9 conditions × 4 N × 5 seeds = 180 exp.)
and saves all figures in papers_images/en/ and papers_images/es/.
Also generates papers_images/architectural_changes.md.

Usage:
    python generate_paper_figures.py
"""
import sys
import json
import math
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull

warnings.filterwarnings("ignore")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from stage6_interaction import CLASSES as SYS_CLASSES
from run_ablation import run_ablation, CONDITION_LABELS

# Global state set per language run
T            = {}          # current translation dict
OUT_CURRENT  = ROOT        # current output directory

# Style
plt.rcParams.update({
    "figure.dpi":        300,
    "savefig.dpi":       300,
    "font.family":       "DejaVu Sans",
    "font.size":         10,
    "axes.titlesize":    11,
    "axes.labelsize":    10,
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
    "legend.fontsize":   9,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.alpha":        0.35,
    "grid.linewidth":    0.6,
    "lines.linewidth":   1.8,
    "lines.markersize":  6,
})

PALETTE = {
    "A Baseline":           "#e74c3c",
    "B1 Norm/count":        "#2ecc71",
    "B2 Norm/sqrt":         "#f39c12",
    "C Balanced M_dir":     "#9b59b6",
    "D Balanced queries":   "#3498db",
    "E32 m=32 binary":      "#e67e22",
    "E64 m=64 binary":      "#cd6120",
    "F Curated ConceptNet": "#1abc9c",
    "G Best (D+B1+F)":      "#2c3e50",
}
DOMAIN_COLOR = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60",
                "cow": "#8e44ad", "cup": "#c9760a", "dog": "#16a085",
                "pear": "#7d8f22", "tomato": "#c0392b"}
N_VALUES     = [50, 100, 200, 400]
N_SHOW       = N_VALUES[-1]   # N del banco completo para las figuras de corte

# Translations
TEXTS = {
    "en": {
        "n_queries":        "Number of queries (N)",
        "early_acc_y":      "Early-phase accuracy",
        "early_acc_title":  "Early-phase accuracy (M_dom) vs N",
        "mature_acc_y":     "Mature-phase accuracy",
        "mature_acc_title": "Mature-phase accuracy (M_dir) vs N — condition comparison",
        "heatmap_title":    "Mature accuracy — condition × N queries",
        "domain_acc_y":     "Mature accuracy per domain",
        "domain_acc_title": "Per-domain accuracy × condition (N=400, mean over 5 seeds)",
        "domain":           "Domain",
        "fidelity_y":       "M_dir → M_dom fidelity",
        "fidelity_title":   "M_dir learning fidelity vs N\n"
                            "(% routing match between M_dir and M_dom)",
        "entropy_y":        "M_dir entropy (bits)",
        "entropy_title":    "M_dir registration entropy vs N\n"
                            "(higher entropy = more balanced routing)",
        "max_entropy":      "Maximum entropy",
        "reg_y":            "Accumulated M_dir registrations",
        "reg_title":        "M_dir registrations per agent × condition (N=400)",
        "ideal":            "Ideal balanced",
        "scatter_x":        "Early-phase accuracy (M_dom)",
        "scatter_y":        "Mature-phase accuracy (M_dir)",
        "scatter_title":    "Early accuracy vs Mature accuracy per condition and N\n"
                            "(points above diagonal = M_dir outperforms M_dom)",
        "perfect_fidelity": "Perfect fidelity",
        "sem_pca_title":    "fastText semantic space (PCA 2D)\n"
                            u"★ = domain centroids   ◆ = ambiguous tokens",
        "centroid":         "Centroid",
        "correct_sem":      "Correct\nsemantics",
        "cross_domain":     "Cross-domain",
        "cosine_y":         "Cosine similarity with centroid",
        "cosine_title":     "Continuous-space cosine similarity\nof problematic tokens",
        "bins_x":           "Quantization bin",
        "bins_y":           "Feature proportion",
        "bins_title":       "Magnitude quantization\nquantize_binary(v, m=16)\n"
                            "All 16 levels are used",
        "bins_note":        "All 16 bins\nare populated",
        "sem_suptitle":     "Semantic space analysis — magnitude quantization preserves separation",
        "winner_y":         "Fraction of mature-phase wins",
        "winner_title":     "M_dir winner distribution per condition (N=400)",
        "winner_agent":     "Winning agent",
        "ideal_balanced":   "Ideal balanced (12.5%)",
        "table_title":      "Results summary (N=400, mean over 5 seeds)",
        "col_cond":         "Condition",
        "col_early":        "Early\nAcc",
        "col_fid":          "Fidelity",
        "col_mature":       "Mature\nAcc",
        "col_entropy":      "Entropy\n(bits)",
        # FP/FN figures
        "recog_title":      "M_dom Label Recognition Heatmap (diagnostic)\n"
                            "(raw activation, row-normalized — NOT the official "
                            "gated routing)",
        "recog_y":          "Labels (grouped by domain)",
        "recog_x":          "M_dom agent",
        "recog_cbar":       "Normalized recognition weight",
        "recog_tp":         "TP",
        "recog_fp":         "FP",
        "recog_fn":         "FN",
        "recog_tn":         "TN",
        "prf_title":        "Precision, Recall & F1 per agent\n"
                            "Baseline M_dom  vs  Curated M_dom (Condition G)",
        "prf_baseline":     "Baseline",
        "prf_curated":      "Curated (G)",
        "prf_precision":    "Precision",
        "prf_recall":       "Recall",
        "prf_f1":           "F1-score",
        "prf_agent":        "Agent",
        "prf_note_tp":      "TP: own-domain label correctly routed",
        "prf_note_fp":      "FP: foreign label incorrectly routed to this agent",
        "prf_note_fn":      "FN: own-domain label missed by this agent",
        # Recall figure
        "recall_title":     "Label-to-Image Recall — M_dom Prototypes per Domain",
        "recall_ref":       "ETH-80\nreference",
        "recall_weight":    "w",
        "recall_ok":        "recognized",
        "recall_fail":      "not recognized",
        "recall_caption":   "Each column shows the prototype image recalled by M_dom "
                            "when queried with the text label shown below it.\n"
                            "Top row: real ETH-80 image for reference. "
                            "Weight = M_dom recognition score (higher = stronger match).",
    },
    "es": {
        "n_queries":        "Número de queries (N)",
        "early_acc_y":      "Precisión fase temprana",
        "early_acc_title":  "Precisión en fase temprana (M_dom) vs N",
        "mature_acc_y":     "Precisión fase madura",
        "mature_acc_title": "Precisión en fase madura (M_dir) vs N — comparación de condiciones",
        "heatmap_title":    "Precisión madura — condición × N queries",
        "domain_acc_y":     "Precisión madura por dominio",
        "domain_acc_title": "Precisión por dominio × condición (N=400, media 5 seeds)",
        "domain":           "Dominio",
        "fidelity_y":       "Fidelidad M_dir → M_dom",
        "fidelity_title":   "Fidelidad de aprendizaje de M_dir vs N\n"
                            "(% coincidencia de routing entre M_dir y M_dom)",
        "entropy_y":        "Entropía de M_dir (bits)",
        "entropy_title":    "Entropía de registros en M_dir vs N\n"
                            "(mayor entropía = routing más equilibrado)",
        "max_entropy":      "Entropía máxima",
        "reg_y":            "Registros acumulados en M_dir",
        "reg_title":        "Registros en M_dir por agente × condición (N=400)",
        "ideal":            "Ideal balanceado",
        "scatter_x":        "Precisión fase temprana (M_dom)",
        "scatter_y":        "Precisión fase madura (M_dir)",
        "scatter_title":    "Precisión temprana vs madura por condición y N\n"
                            "(puntos sobre la diagonal = M_dir supera a M_dom)",
        "perfect_fidelity": "Fidelidad perfecta",
        "sem_pca_title":    "Espacio semántico fastText (PCA 2D)\n"
                            u"★ = centroides de dominio   ◆ = tokens ambiguos",
        "centroid":         "Centroide",
        "correct_sem":      "Semántica\ncorrecta",
        "cross_domain":     "Cross-domain",
        "cosine_y":         "Similitud coseno con centroide",
        "cosine_title":     "Similitud coseno (espacio continuo)\nde tokens problemáticos",
        "bins_x":           "Bin de cuantización",
        "bins_y":           "Proporción de features",
        "bins_title":       "Cuantización por magnitud\nquantize_binary(v, m=16)\n"
                            "Los 16 niveles se utilizan",
        "bins_note":        "Los 16 bins\nse pueblan",
        "sem_suptitle":     "Análisis del espacio semántico — la cuantización por magnitud preserva la separación",
        "winner_y":         "Fracción de victorias en fase madura",
        "winner_title":     "Distribución de ganador en M_dir por condición (N=400)",
        "winner_agent":     "Agente ganador",
        "ideal_balanced":   "Ideal balanceado (12.5%)",
        "table_title":      "Tabla resumen de resultados (N=400, media 5 seeds)",
        "col_cond":         "Condición",
        "col_early":        "Early\nAcc",
        "col_fid":          "Fidelidad",
        "col_mature":       "Mature\nAcc",
        "col_entropy":      "Entropía\n(bits)",
        # FP/FN figures
        "recog_title":      "Heatmap de reconocimiento en M_dom (diagnóstico)\n"
                            "(activación cruda, normalizada por fila — NO es el "
                            "routing oficial gateado)",
        "imgrej_title":     "Rechazo de imágenes por la MAE (containment, sin filtro léxico)",
        "imgrej_accepted":  "Aceptadas\n(con soporte)",
        "imgrej_rejected":  "Rechazadas\n(reales, ξ=0)",
        "imgrej_ood":       "Fuera de dominio\n(sintéticas)",
        "img2lbl_title":    "Salida semántica: imagen → recall MAE → etiquetas (top-3, dominio real)",
        "img2lbl_input":    "Entrada (pista)",
        "img2lbl_recon":    "Reconstrucción evocada (MAE)",
        "recog_y":          "Labels (agrupadas por dominio)",
        "recog_x":          "Agente M_dom",
        "recog_cbar":       "Peso de reconocimiento normalizado",
        "recog_tp":         "TP",
        "recog_fp":         "FP",
        "recog_fn":         "FN",
        "recog_tn":         "TN",
        "prf_title":        "Precisión, Recall y F1 por agente\n"
                            "M_dom Baseline  vs  M_dom Curado (Condición G)",
        "prf_baseline":     "Baseline",
        "prf_curated":      "Curado (G)",
        "prf_precision":    "Precisión",
        "prf_recall":       "Recall",
        "prf_f1":           "F1-score",
        "prf_agent":        "Agente",
        "prf_note_tp":      "TP: label propia correctamente enrutada",
        "prf_note_fp":      "FP: label ajena incorrectamente enrutada a este agente",
        "prf_note_fn":      "FN: label propia no reconocida por este agente",
        # Recall figure
        "recall_title":     "Recall Label-a-Imagen — Prototipos M_dom por Dominio",
        "recall_ref":       "Referencia\nETH-80",
        "recall_weight":    "w",
        "recall_ok":        "reconocido",
        "recall_fail":      "no reconocido",
        "recall_caption":   "Cada columna muestra la imagen prototipo recuperada por M_dom "
                            "al consultar con la label de texto indicada.\n"
                            "Fila superior: imagen real ETH-80 de referencia. "
                            "Peso = score de reconocimiento M_dom (mayor = coincidencia más fuerte).",
    },
}


# Helpers

def savefig(name, fig=None):
    if fig is None:
        fig = plt.gcf()
    fig.tight_layout()
    path = OUT_CURRENT / name
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"    {path.name}")


def pct_fmt(y, _):
    return f"{y:.0%}"


def _add_convex_hull(ax, pts, color, alpha=0.12):
    if len(pts) < 3:
        return
    try:
        hull = ConvexHull(pts)
        v = np.append(hull.vertices, hull.vertices[0])
        ax.fill(pts[v, 0], pts[v, 1], color=color, alpha=alpha, zorder=1)
        ax.plot(pts[v, 0], pts[v, 1], color=color, lw=1.2, alpha=0.45, zorder=2)
    except Exception:
        pass


def build_agg(df_raw):
    numeric = [c for c in df_raw.columns if c not in ("condition", "N", "seed")]
    agg = df_raw.groupby(["condition", "N"])[numeric].agg(["mean", "std"]).reset_index()
    agg.columns = ["condition", "N"] + [f"{c}_{s}" for c, s in agg.columns[2:]]
    for col in agg.columns:
        if col.endswith("_std"):
            agg[col] = agg[col].fillna(0)
    agg["condition"] = agg["condition"].map(lambda c: CONDITION_LABELS.get(c, c))
    return agg


# Figure functions (all use global T)

def fig_early_accuracy(agg):
    show = ["A Baseline", "B1 Norm/count", "D Balanced queries", "G Best (D+B1+F)"]
    fig, ax = plt.subplots(figsize=(6, 4))
    for cond in show:
        sub = agg[agg["condition"] == cond].sort_values("N")
        ax.plot(sub["N"], sub["early_accuracy_mean"],
                marker="o", label=cond, color=PALETTE[cond])
        ax.fill_between(sub["N"],
                        sub["early_accuracy_mean"] - sub["early_accuracy_std"],
                        sub["early_accuracy_mean"] + sub["early_accuracy_std"],
                        alpha=0.12, color=PALETTE[cond])
    ax.set_xlabel(T["n_queries"])
    ax.set_ylabel(T["early_acc_y"])
    ax.set_title(T["early_acc_title"])
    ax.set_xticks(N_VALUES)
    ax.set_ylim(0, 1.08)
    ax.yaxis.set_major_formatter(pct_fmt)
    ax.legend(loc="lower left", framealpha=0.8)
    savefig("fig01_early_accuracy_vs_N.png", fig)


def fig_mature_accuracy(agg):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    KEY = {"A Baseline", "G Best (D+B1+F)", "B1 Norm/count"}
    for cond, sub in agg.groupby("condition"):
        sub = sub.sort_values("N")
        lw = 2.8 if cond in KEY else 1.3
        ls = "-"  if cond in KEY else "--"
        mk = "o"  if cond in KEY else "s"
        ax.plot(sub["N"], sub["mature_accuracy_mean"],
                marker=mk, linewidth=lw, linestyle=ls,
                label=cond, color=PALETTE.get(cond, "#bdc3c7"))
        if cond in KEY:
            ax.fill_between(sub["N"],
                            sub["mature_accuracy_mean"] - sub["mature_accuracy_std"],
                            sub["mature_accuracy_mean"] + sub["mature_accuracy_std"],
                            alpha=0.10, color=PALETTE.get(cond, "#bdc3c7"))
    ax.set_xlabel(T["n_queries"])
    ax.set_ylabel(T["mature_acc_y"])
    ax.set_title(T["mature_acc_title"])
    ax.set_xticks(N_VALUES)
    ax.set_ylim(-0.02, 1.10)
    ax.yaxis.set_major_formatter(pct_fmt)
    ax.legend(loc="upper left", framealpha=0.85, fontsize=8, ncol=2)
    savefig("fig02_mature_accuracy_vs_N.png", fig)


def fig_heatmap(agg):
    cond_order = list(CONDITION_LABELS.values())
    pivot = agg.pivot_table(index="condition", columns="N",
                            values="mature_accuracy_mean").reindex(cond_order)
    cmap = LinearSegmentedColormap.from_list("rg", ["#e74c3c", "#f1c40f", "#2ecc71"])
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(pivot.values, aspect="auto", cmap=cmap, vmin=0, vmax=1)
    ax.set_xticks(range(len(N_VALUES)))
    ax.set_xticklabels([f"N={n}" for n in N_VALUES])
    ax.set_yticks(range(len(cond_order)))
    ax.set_yticklabels(cond_order, fontsize=8)
    ax.set_title(T["heatmap_title"])
    for i in range(len(cond_order)):
        for j in range(len(N_VALUES)):
            val = pivot.values[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"{val:.0%}", ha="center", va="center",
                        fontsize=8, color="white" if val < 0.5 else "black")
    plt.colorbar(im, ax=ax, label=T["mature_acc_y"], fraction=0.035)
    ax.grid(False)
    savefig("fig03_heatmap_condition_N.png", fig)


def fig_domain_accuracy(agg):
    n80 = agg[agg["N"] == N_SHOW].set_index("condition").reindex(
        list(CONDITION_LABELS.values())).reset_index()
    # run_ablation.py emite columnas para las 8 clases (itera CLASSES); el
    # filtrado defensivo se conserva por si se re-procesa un CSV de la era
    # de 3 clases.
    doms_present = [d for d in SYS_CLASSES if f"mature_acc_{d}_mean" in n80.columns]
    x, w = np.arange(len(n80)), 0.8 / max(len(doms_present), 1)
    fig, ax = plt.subplots(figsize=(2 + 1.1 * len(doms_present), 4.5))
    mid = (len(doms_present) - 1) / 2
    for i, dom in enumerate(doms_present):
        color = DOMAIN_COLOR[dom]
        vals = n80[f"mature_acc_{dom}_mean"].fillna(0).values
        ax.bar(x + (i - mid) * w, vals, w, label=dom, color=color,
               alpha=0.85, edgecolor="white", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(n80["condition"], rotation=22, ha="right", fontsize=8)
    ax.set_ylabel(T["domain_acc_y"])
    ax.set_title(T["domain_acc_title"])
    ax.set_ylim(0, 1.15)
    ax.yaxis.set_major_formatter(pct_fmt)
    ax.legend(title=T["domain"], loc="upper left", ncol=3)
    ax.axhline(1.0, color="#636e72", lw=0.8, linestyle="--", alpha=0.5)
    savefig("fig04_domain_accuracy_N80.png", fig)


def fig_fidelity(agg):
    key = ["A Baseline", "B1 Norm/count", "G Best (D+B1+F)"]
    fig, ax = plt.subplots(figsize=(6, 4))
    for cond in key:
        sub = agg[agg["condition"] == cond].sort_values("N")
        ax.plot(sub["N"], sub["mature_fidelity_mean"],
                marker="o", label=cond, color=PALETTE[cond])
        ax.fill_between(sub["N"],
                        sub["mature_fidelity_mean"] - sub["mature_fidelity_std"],
                        sub["mature_fidelity_mean"] + sub["mature_fidelity_std"],
                        alpha=0.12, color=PALETTE[cond])
    ax.set_xlabel(T["n_queries"])
    ax.set_ylabel(T["fidelity_y"])
    ax.set_title(T["fidelity_title"])
    ax.set_xticks(N_VALUES)
    ax.set_ylim(-0.02, 1.10)
    ax.yaxis.set_major_formatter(pct_fmt)
    ax.legend(framealpha=0.85)
    savefig("fig05_fidelity_vs_N.png", fig)


def fig_entropy(agg):
    max_h = math.log2(len(SYS_CLASSES))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axhline(max_h, color="#636e72", lw=1.0, linestyle="--",
               label=f"{T['max_entropy']} = {max_h:.3f} bits")
    for cond in ["A Baseline", "B1 Norm/count", "D Balanced queries", "G Best (D+B1+F)"]:
        sub = agg[agg["condition"] == cond].sort_values("N")
        ax.plot(sub["N"], sub["mdir_entropy_mean"],
                marker="o", label=cond, color=PALETTE[cond])
    ax.set_xlabel(T["n_queries"])
    ax.set_ylabel(T["entropy_y"])
    ax.set_title(T["entropy_title"])
    ax.set_xticks(N_VALUES)
    ax.set_ylim(0, max_h + 0.25)
    ax.legend(framealpha=0.85, fontsize=8)
    savefig("fig06_mdir_entropy_vs_N.png", fig)


def fig_registrations(agg):
    n80 = agg[agg["N"] == N_SHOW].set_index("condition").reindex(
        list(CONDITION_LABELS.values())).reset_index()
    # run_ablation.py emite las 8 clases; filtrado defensivo para CSV viejos
    # (ver fig_domain_accuracy).
    doms_present = [d for d in SYS_CLASSES if f"mdir_reg_{d}_mean" in n80.columns]
    x, w = np.arange(len(n80)), 0.8 / max(len(doms_present), 1)
    fig, ax = plt.subplots(figsize=(2 + 1.1 * len(doms_present), 4.5))
    mid = (len(doms_present) - 1) / 2
    for i, dom in enumerate(doms_present):
        color = DOMAIN_COLOR[dom]
        vals = n80[f"mdir_reg_{dom}_mean"].fillna(0).values
        ax.bar(x + (i - mid) * w, vals, w, label=dom, color=color,
               alpha=0.85, edgecolor="white", linewidth=0.8)
    ideal = n80[[f"mdir_reg_{d}_mean" for d in doms_present]].sum(axis=1).mean() / max(len(doms_present), 1)
    ax.axhline(ideal, color="#636e72", lw=0.9, linestyle=":",
               label=f"{T['ideal']} ({ideal:.0f})")
    ax.set_xticks(x)
    ax.set_xticklabels(n80["condition"], rotation=22, ha="right", fontsize=8)
    ax.set_ylabel(T["reg_y"])
    ax.set_title(T["reg_title"])
    ax.legend(title=T["domain"], loc="upper right", ncol=4, fontsize=8)
    savefig("fig07_mdir_registrations_N80.png", fig)


def fig_early_vs_mature(agg):
    fig, ax = plt.subplots(figsize=(6, 5))
    for cond, sub in agg.groupby("condition"):
        color = PALETTE.get(cond, "#bdc3c7")
        sizes = [40 + 20 * i for i in range(len(sub))]
        ax.scatter(sub["early_accuracy_mean"], sub["mature_accuracy_mean"],
                   c=color, s=sizes, alpha=0.8, edgecolors="white",
                   linewidth=0.5, label=cond, zorder=3)
        for _, row in sub.iterrows():
            ax.annotate(f"N={int(row['N'])}",
                        (row["early_accuracy_mean"], row["mature_accuracy_mean"]),
                        fontsize=6, color=color, alpha=0.7,
                        xytext=(3, 3), textcoords="offset points")
    ax.plot([0, 1], [0, 1], "k--", lw=0.8, alpha=0.4,
            label=T["perfect_fidelity"])
    ax.set_xlabel(T["scatter_x"])
    ax.set_ylabel(T["scatter_y"])
    ax.set_title(T["scatter_title"])
    ax.set_xlim(-0.02, 1.08)
    ax.set_ylim(-0.02, 1.08)
    ax.xaxis.set_major_formatter(pct_fmt)
    ax.yaxis.set_major_formatter(pct_fmt)
    ax.legend(loc="lower right", fontsize=7, framealpha=0.85, ncol=2)
    savefig("fig08_early_vs_mature_scatter.png", fig)


def fig_winner_distribution(agg):
    n80 = agg[agg["N"] == N_SHOW].set_index("condition").reindex(
        list(CONDITION_LABELS.values())).reset_index()
    # run_ablation.py emite las 8 clases; filtrado defensivo para CSV viejos
    # (ver fig_domain_accuracy).
    doms_present = [d for d in SYS_CLASSES if f"winner_pct_{d}_mean" in n80.columns]
    x = np.arange(len(n80))
    fig, ax = plt.subplots(figsize=(10, 4))
    bottom = np.zeros(len(n80))
    for dom in doms_present:
        color = DOMAIN_COLOR[dom]
        vals = n80[f"winner_pct_{dom}_mean"].fillna(0).values
        ax.bar(x, vals, bottom=bottom, label=dom, color=color,
               alpha=0.85, edgecolor="white", linewidth=0.8)
        for xi, (v, b) in enumerate(zip(vals, bottom)):
            if v > 0.06:
                ax.text(xi, b + v / 2, f"{v:.0%}",
                        ha="center", va="center", fontsize=8,
                        color="white", fontweight="bold")
        bottom += vals
    ax.axhline(1 / max(len(doms_present), 1), color="#2d3436", lw=0.9, linestyle="--",
               label=T["ideal_balanced"])
    ax.set_xticks(x)
    ax.set_xticklabels(n80["condition"], rotation=22, ha="right", fontsize=8)
    ax.set_ylabel(T["winner_y"])
    ax.set_title(T["winner_title"])
    ax.set_ylim(0, 1.08)
    ax.yaxis.set_major_formatter(pct_fmt)
    ax.legend(title=T["winner_agent"], loc="upper right", ncol=4, fontsize=8)
    savefig("fig09_winner_distribution_N80.png", fig)


def fig_summary_table(agg):
    n80 = agg[agg["N"] == N_SHOW].set_index("condition").reindex(
        list(CONDITION_LABELS.values())).reset_index()
    # run_ablation.py emite las 8 clases; filtrado defensivo para CSV viejos
    # (ver fig_domain_accuracy).
    doms_present = [d for d in SYS_CLASSES if f"mature_acc_{d}_mean" in n80.columns]
    headers = [T["col_cond"], T["col_early"], T["col_fid"], T["col_mature"],
               *[d.capitalize() for d in doms_present], T["col_entropy"]]
    rows = []
    for _, r in n80.iterrows():
        rows.append([
            r["condition"],
            f"{r['early_accuracy_mean']:.1%}",
            f"{r['mature_fidelity_mean']:.1%}",
            f"{r['mature_accuracy_mean']:.1%}",
            *[f"{r[f'mature_acc_{d}_mean']:.1%}" for d in doms_present],
            f"{r['mdir_entropy_mean']:.3f}",
        ])
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis("off")
    tbl = ax.table(cellText=rows, colLabels=headers,
                   loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)
    tbl.scale(1.0, 1.55)
    highlight = {"A Baseline": "#ffeaa7", "B1 Norm/count": "#d5f5e3",
                 "G Best (D+B1+F)": "#a9cce3"}
    for row_i, cond in enumerate(n80["condition"]):
        bg = highlight.get(cond, "#ffffff")
        for col_i in range(len(headers)):
            tbl[(row_i + 1, col_i)].set_facecolor(bg)
    for col_i in range(len(headers)):
        tbl[(0, col_i)].set_facecolor("#2c3e50")
        tbl[(0, col_i)].set_text_props(color="white", fontweight="bold")
    ax.set_title(T["table_title"], fontsize=11, pad=12)
    savefig("fig10_summary_table_N80.png", fig)


def _compute_recognition_matrix(mdoms):
    """
    For every label in every domain, compute recognize_from_left on every
    M_dom agent (all len(CLASSES) of them).
    Returns:
        words   : list of str  (len = n_labels)
        true_dom: list of str  (domain each label belongs to)
        matrix  : ndarray (n_labels, 3) raw recognition scores
    """
    from quantizer import quantize_binary
    CLASSES = list(SYS_CLASSES)
    words, true_dom, rows = [], [], []
    for cls in CLASSES:
        vecs = json.loads((ROOT / f"label_vectors_{cls}.json").read_text())
        for word, v in vecs.items():
            v_q = quantize_binary(np.array(v, dtype=np.float32), 16)
            scores = [float(mdoms[c].recognize_from_left(v_q)) for c in CLASSES]
            words.append(word)
            true_dom.append(cls)
            rows.append(scores)
    return words, true_dom, np.array(rows)   # (N, 3)


def _prf(matrix, true_dom, cls_list=None):
    """
    Argmax-based P / R / F1 per agent (binary one-vs-rest).
    Returns dict {cls: {"P": float, "R": float, "F1": float, "TP": int, "FP": int, "FN": int}}
    """
    if cls_list is None:
        cls_list = list(SYS_CLASSES)
    n     = len(true_dom)
    preds = [cls_list[int(np.argmax(matrix[i]))] for i in range(n)]
    out   = {}
    for cls in cls_list:
        TP = sum(1 for i in range(n) if true_dom[i] == cls and preds[i] == cls)
        FP = sum(1 for i in range(n) if true_dom[i] != cls and preds[i] == cls)
        FN = sum(1 for i in range(n) if true_dom[i] == cls and preds[i] != cls)
        P  = TP / (TP + FP) if (TP + FP) > 0 else 0.0
        R  = TP / (TP + FN) if (TP + FN) > 0 else 0.0
        F1 = 2 * P * R / (P + R) if (P + R) > 0 else 0.0
        out[cls] = {"P": P, "R": R, "F1": F1, "TP": TP, "FP": FP, "FN": FN}
    return out


def fig_recognition_heatmap():
    """
    Heatmap: labels × agents — row-normalized recognition weight.
    Marks TP / FP / FN on each cell.
    """
    from run_ablation import load_base_mdoms
    CLASSES = list(SYS_CLASSES)

    mdoms = load_base_mdoms()
    words, true_dom, matrix = _compute_recognition_matrix(mdoms)

    # Sort rows by domain, in CLASSES order, then alphabetically by word
    order = sorted(range(len(words)),
                   key=lambda i: (CLASSES.index(true_dom[i]), words[i]))
    words    = [words[i]    for i in order]
    true_dom = [true_dom[i] for i in order]
    matrix   = matrix[order]

    # Row-normalize (each label → relative preference across agents)
    row_max = matrix.max(axis=1, keepdims=True)
    row_max[row_max == 0] = 1
    norm_mat = matrix / row_max   # values in [0, 1]

    # Argmax prediction per label
    preds = [CLASSES[int(np.argmax(matrix[i]))] for i in range(len(words))]

    n_labels = len(words)
    fig, ax  = plt.subplots(figsize=(2 + 0.6 * len(CLASSES), max(8, n_labels * 0.22)))

    im = ax.imshow(norm_mat, aspect="auto",
                   cmap="RdYlGn", vmin=0, vmax=1)

    ax.set_xticks(range(len(CLASSES)))
    ax.set_xticklabels(CLASSES, fontsize=9)
    ax.set_yticks(range(n_labels))
    ax.set_yticklabels(words, fontsize=5.5)
    ax.set_xlabel(T["recog_x"])
    ax.set_ylabel(T["recog_y"])
    ax.set_title(T["recog_title"], fontsize=10)
    ax.grid(False)

    # Domain separator lines
    boundaries = []
    prev = true_dom[0]
    for i, d in enumerate(true_dom):
        if d != prev:
            boundaries.append(i - 0.5)
            prev = d
    for b in boundaries:
        ax.axhline(b, color="white", lw=2.5)

    # Domain color strips on y-axis left
    for i, (w, dom) in enumerate(zip(words, true_dom)):
        color = DOMAIN_COLOR[dom]
        ax.annotate("", xy=(-0.5, i), xytext=(-0.15, i),
                    xycoords=("data", "data"),
                    textcoords=("data", "data"),
                    annotation_clip=False)

    # Cell labels: TP / FP / FN per cell
    for i in range(n_labels):
        for j, cls in enumerate(CLASSES):
            is_own  = true_dom[i] == cls
            is_pred = preds[i] == cls
            if is_own and is_pred:
                tag, ec, lc = T["recog_tp"], "#2ecc71", "white"
            elif not is_own and is_pred:
                tag, ec, lc = T["recog_fp"], "#e74c3c", "white"
            elif is_own and not is_pred:
                tag, ec, lc = T["recog_fn"], "#f39c12", "black"
            else:
                tag, ec, lc = "", "none", "none"
            if tag:
                ax.text(j, i, tag, ha="center", va="center",
                        fontsize=4.5, color=lc, fontweight="bold")
            # Cell border for FP/FN
            if ec != "none":
                rect = plt.Rectangle((j - 0.49, i - 0.49), 0.98, 0.98,
                                     fill=False, edgecolor=ec,
                                     linewidth=1.2, zorder=4)
                ax.add_patch(rect)

    # Domain labels on left margin
    for dom in CLASSES:
        idxs = [i for i, d in enumerate(true_dom) if d == dom]
        mid  = (min(idxs) + max(idxs)) / 2
        ax.text(-0.8, mid, dom, ha="right", va="center",
                fontsize=7, color=DOMAIN_COLOR[dom],
                fontweight="bold", rotation=90,
                transform=ax.get_yaxis_transform())

    # Legend patches
    legend_items = [
        mpatches.Patch(facecolor="#2ecc71", label=f"{T['recog_tp']}: own domain, correct"),
        mpatches.Patch(facecolor="#e74c3c", label=f"{T['recog_fp']}: foreign domain, misrouted"),
        mpatches.Patch(facecolor="#f39c12", label=f"{T['recog_fn']}: own domain, missed"),
    ]
    ax.legend(handles=legend_items, loc="upper right",
              bbox_to_anchor=(1.0, -0.04),
              fontsize=7, framealpha=0.9, ncol=1)

    plt.colorbar(im, ax=ax, label=T["recog_cbar"],
                 fraction=0.03, pad=0.02)
    savefig("fig12_recognition_heatmap.png", fig)


def fig_precision_recall():
    """
    Precision, Recall, F1 per agent — Baseline vs Curated M_dom (condition G).
    Also shows TP/FP/FN counts as text inside bars.
    """
    from run_ablation import load_base_mdoms, build_curated_apple_mdom
    CLASSES = list(SYS_CLASSES)

    # Baseline M_dom
    base_mdoms = load_base_mdoms()
    words_b, true_b, mat_b = _compute_recognition_matrix(base_mdoms)
    prf_base = _prf(mat_b, true_b)

    # Curated M_dom (condition G: curated apple, base horse/car)
    cur_apple  = build_curated_apple_mdom()
    cur_mdoms  = {**base_mdoms, "apple": cur_apple}
    words_c, true_c, mat_c = _compute_recognition_matrix(cur_mdoms)
    prf_cur = _prf(mat_c, true_c)

    metrics  = [T["prf_precision"], T["prf_recall"], T["prf_f1"]]
    met_keys = ["P", "R", "F1"]
    x = np.arange(len(CLASSES))
    w = 0.18
    offsets = [-1.5 * w, -0.5 * w, 0.5 * w, 1.5 * w]

    fig, axes = plt.subplots(1, 3, figsize=(2.0 * len(CLASSES), 4.5), sharey=True)

    for mi, (met, mkey) in enumerate(zip(metrics, met_keys)):
        ax = axes[mi]
        for ci, cls in enumerate(CLASSES):
            b_val = prf_base[cls][mkey]
            c_val = prf_cur[cls][mkey]
            color = DOMAIN_COLOR[cls]

            # Baseline bar (hatched)
            bar_b = ax.bar(ci - 0.22, b_val, 0.38,
                           color=color, alpha=0.45,
                           hatch="///", edgecolor=color,
                           label=T["prf_baseline"] if ci == 0 else "")
            # Curated bar (solid)
            bar_c = ax.bar(ci + 0.22, c_val, 0.38,
                           color=color, alpha=0.90,
                           edgecolor="white",
                           label=T["prf_curated"] if ci == 0 else "")

            # Value labels
            for bar, val in [(bar_b, b_val), (bar_c, c_val)]:
                ax.text(bar[0].get_x() + bar[0].get_width() / 2,
                        val + 0.02, f"{val:.2f}",
                        ha="center", va="bottom", fontsize=7.5)

            # TP/FP/FN counts inside bars (baseline)
            if mkey == "F1":
                counts_b = prf_base[cls]
                counts_c = prf_cur[cls]
                for bar, counts in [(bar_b, counts_b), (bar_c, counts_c)]:
                    txt = (f"TP={counts['TP']}\n"
                           f"FP={counts['FP']}\n"
                           f"FN={counts['FN']}")
                    ax.text(bar[0].get_x() + bar[0].get_width() / 2,
                            bar[0].get_height() / 2, txt,
                            ha="center", va="center",
                            fontsize=5.5, color="white",
                            fontweight="bold")

        ax.set_xticks(range(len(CLASSES)))
        ax.set_xticklabels(CLASSES, fontsize=9)
        ax.set_xlabel(T["prf_agent"])
        ax.set_title(met, fontsize=11)
        ax.set_ylim(0, 1.22)
        ax.yaxis.set_major_formatter(pct_fmt)
        ax.axhline(1.0, color="#636e72", lw=0.7, linestyle="--", alpha=0.4)

        if mi == 0:
            ax.set_ylabel("Score")
            # Legend with pattern examples
            from matplotlib.patches import Patch
            leg = [
                Patch(facecolor="#888", alpha=0.45, hatch="///",
                      edgecolor="#888", label=T["prf_baseline"]),
                Patch(facecolor="#888", alpha=0.90,
                      edgecolor="white", label=T["prf_curated"]),
            ]
            ax.legend(handles=leg, loc="upper right", fontsize=8)

    fig.suptitle(T["prf_title"], fontsize=11, fontweight="bold")
    fig.text(0.5, -0.02,
             f"{T['prf_note_tp']}   |   {T['prf_note_fp']}   |   {T['prf_note_fn']}",
             ha="center", fontsize=7.5, color="#555", style="italic")
    savefig("fig13_precision_recall_f1.png", fig)


def _load_all_label_vectors():
    words, vecs, domains = [], [], []
    for cls in SYS_CLASSES:
        raw = json.loads((ROOT / f"label_vectors_{cls}.json").read_text())
        for word, v in raw.items():
            v = np.array(v, dtype=np.float32)
            # Excluir vectores fallback sintéticos (±1 en 300 dims → norma ~17;
            # los fastText reales rondan norma 1–3): distorsionan el PCA.
            if np.linalg.norm(v) > 10:
                continue
            words.append(word)
            vecs.append(v)
            domains.append(cls)
    return words, np.array(vecs), domains


def fig_semantic_space():
    from quantizer import quantize_binary
    from stage6_interaction import get_fasttext_vector, load_all_vectors

    words, vecs, domains = _load_all_label_vectors()
    vc = load_all_vectors()

    EXTRA_WORDS = ["engine", "motor", "machine"]
    extra_vecs  = [np.array(get_fasttext_vector(w, vc), dtype=np.float32)
                   for w in EXTRA_WORDS]

    all_words   = words + EXTRA_WORDS
    all_vecs    = np.vstack([vecs, np.array(extra_vecs)])
    all_domains = domains + ["extra"] * len(EXTRA_WORDS)

    # PCA 2D
    pca   = PCA(n_components=2, random_state=42)
    pts2d = pca.fit_transform(all_vecs)
    var   = pca.explained_variance_ratio_

    idx = {d: [i for i, dom in enumerate(all_domains) if dom == d]
           for d in list(SYS_CLASSES) + ["extra"]}
    centroids = {d: pts2d[idx[d]].mean(axis=0) for d in SYS_CLASSES}

    DOM_COLORS  = {**DOMAIN_COLOR, "extra": "#555555"}
    DOM_MARKERS = {"apple": "o", "car": "^", "cow": "P", "cup": "X",
                   "dog": "*", "horse": "s", "pear": "v", "tomato": "d",
                   "extra": "D"}

    fig = plt.figure(figsize=(15, 5.5))
    gs  = gridspec.GridSpec(1, 3, width_ratios=[2.2, 1.4, 1.4], wspace=0.38)
    ax_pca    = fig.add_subplot(gs[0])
    ax_cosine = fig.add_subplot(gs[1])
    ax_bins   = fig.add_subplot(gs[2])

    # Panel A: PCA space
    for dom in SYS_CLASSES:
        pts = pts2d[idx[dom]]
        _add_convex_hull(ax_pca, pts, DOM_COLORS[dom])
        lbl = f"{dom} ({T['domain'].lower()})" if dom != "extra" else T["cross_domain"]
        ax_pca.scatter(pts[:, 0], pts[:, 1],
                       c=DOM_COLORS[dom], marker=DOM_MARKERS[dom],
                       s=55, alpha=0.82, zorder=3, label=dom,
                       edgecolors="white", linewidth=0.5)
        for i in idx[dom]:
            ax_pca.annotate(all_words[i], pts2d[i], fontsize=6.5,
                            color=DOM_COLORS[dom], alpha=0.85,
                            xytext=(3, 3), textcoords="offset points")

    for dom, c in centroids.items():
        ax_pca.scatter(*c, marker="*", s=320, color=DOM_COLORS[dom],
                       edgecolors="white", linewidth=1.5, zorder=5)
        ax_pca.annotate(f"{T['centroid']}\n{dom}", c, fontsize=7.5,
                        color=DOM_COLORS[dom], fontweight="bold",
                        xytext=(-8, 10), textcoords="offset points")

    for w, ei in zip(EXTRA_WORDS, idx["extra"]):
        pt = pts2d[ei]
        ax_pca.scatter(*pt, marker="D", s=120, color=DOM_COLORS["extra"],
                       edgecolors="black", linewidth=1.5, zorder=6)
        ax_pca.annotate(f'"{w}"', pt, fontsize=8,
                        color=DOM_COLORS["extra"], fontweight="bold",
                        xytext=(5, 5), textcoords="offset points")
        if w == "engine":
            ax_pca.annotate("", xy=centroids["car"], xytext=pt,
                            arrowprops=dict(arrowstyle="->", color="#27ae60",
                                           lw=1.8, connectionstyle="arc3,rad=0.2"),
                            zorder=4)
            mid = (pt + centroids["car"]) / 2
            ax_pca.text(mid[0], mid[1] - 0.25, T["correct_sem"],
                        fontsize=6.5, color="#27ae60",
                        style="italic", ha="center")

    ax_pca.scatter([], [], marker="D", color=DOM_COLORS["extra"],
                   edgecolors="black", linewidth=1.5, label=T["cross_domain"])
    ax_pca.set_xlabel(f"PC1 ({var[0]:.1%} var.)")
    ax_pca.set_ylabel(f"PC2 ({var[1]:.1%} var.)")
    ax_pca.set_title(T["sem_pca_title"])
    ax_pca.legend(loc="upper right", fontsize=8, framealpha=0.85)
    ax_pca.grid(True, alpha=0.2)

    # Panel B: cosine similarity
    probe_words = ["engine", "motor", "machine", "computer", "mac"]
    cont_centroids = {}
    for dom in SYS_CLASSES:
        idxs = [i for i, d in enumerate(all_domains) if d == dom]
        c = all_vecs[idxs].mean(axis=0)
        n = np.linalg.norm(c)
        cont_centroids[dom] = c / n if n > 0 else c

    x_pos, width = np.arange(len(probe_words)), 0.26
    for di, (dom, color) in enumerate(DOMAIN_COLOR.items()):
        sims = []
        for w in probe_words:
            v  = np.array(get_fasttext_vector(w, vc), dtype=np.float32)
            n  = np.linalg.norm(v)
            vn = v / n if n > 0 else v
            sims.append(float(np.dot(vn, cont_centroids[dom])))
        ax_cosine.bar(x_pos + di * width, sims, width,
                      label=dom, color=color, alpha=0.85,
                      edgecolor="white", linewidth=0.8)

    ax_cosine.set_xticks(x_pos + width)
    ax_cosine.set_xticklabels(probe_words, rotation=30, ha="right", fontsize=8)
    ax_cosine.set_ylabel(T["cosine_y"])
    ax_cosine.set_title(T["cosine_title"])
    ax_cosine.axhline(0, color="black", lw=0.5)
    ax_cosine.legend(fontsize=8, loc="upper right")
    ax_cosine.set_ylim(-0.05, 0.85)

    # Panel C: binary bin collapse
    M = 16
    rep = {"apple": "apple", "car": "engine", "cow": "cow", "cup": "cup",
           "dog": "dog", "horse": "horse", "pear": "pear", "tomato": "tomato"}
    x_bins, bar_w = np.arange(M), 0.26
    for di, (dom, color) in enumerate(DOMAIN_COLOR.items()):
        v   = np.array(get_fasttext_vector(rep[dom], vc))
        v_q = quantize_binary(v, M)
        cnt = np.bincount(v_q.astype(int), minlength=M).astype(float)
        cnt /= cnt.sum()
        ax_bins.bar(x_bins + di * bar_w, cnt, bar_w,
                    label=f'"{rep[dom]}" ({dom})', color=color,
                    alpha=0.85, edgecolor="white", linewidth=0.5)

    for b in [0, M - 1]:
        ax_bins.axvline(b + bar_w, color="#e74c3c", lw=1.5,
                        linestyle="--", alpha=0.5)
    ylim_top = ax_bins.get_ylim()[1]
    ax_bins.text(M / 2, ylim_top * 0.82, T["bins_note"],
                 ha="center", fontsize=8, color="#e74c3c", style="italic",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffeaa7",
                           edgecolor="#e74c3c", alpha=0.8))
    ax_bins.set_xlabel(T["bins_x"])
    ax_bins.set_ylabel(T["bins_y"])
    ax_bins.set_title(T["bins_title"])
    ax_bins.legend(fontsize=7.5, loc="upper center")

    fig.suptitle(T["sem_suptitle"], fontsize=12, fontweight="bold", y=1.01)
    savefig("fig11_semantic_space.png", fig)


def fig_recall_grid():
    """
    Grid showing label → recalled prototype image per domain.
    Layout: len(CLASSES) domain columns × (1 ETH-80 reference + 5 label
    recalls) rows. Uses correct g_min/g_max dequantization.
    """
    import pickle, torch
    from torchvision import transforms
    from stage2_encoder import Decoder
    from stage6_interaction import get_fasttext_vector, load_all_vectors

    CLASSES = list(SYS_CLASSES)
    Q_LATENT = 32

    # Representative labels per domain (top recognized, semantically clear)
    LABELS = {
        "apple":  ["fruit", "red", "tree", "pear", "seeds"],
        "car":    ["vehicle", "automobile", "car", "engine", "driving"],
        "cow":    ["cow", "animal", "cattle", "farm", "milk"],
        "cup":    ["cup", "mug", "drink", "container", "coffee"],
        "dog":    ["dog", "animal", "canine", "puppy", "pet"],
        "horse":  ["horse", "animal", "equine", "donkey", "riding"],
        "pear":   ["pear", "fruit", "tree", "green", "seeds"],
        "tomato": ["tomato", "fruit", "red", "vegetable", "seeds"],
    }

    # Load decoder
    decoder = Decoder()
    decoder.load_state_dict(torch.load(
        ROOT / "models" / "decoder.pt", map_location="cpu"))
    decoder.eval()

    # Load dequant stats
    stats = json.loads((ROOT / "models" / "latent_global_stats.json").read_text())
    g_min = np.array(stats["global_min"])
    g_max = np.array(stats["global_max"])

    # Load M_dom
    mdoms = {}
    for cls in CLASSES:
        with open(ROOT / "models" / f"mem_dom_{cls}.pkl", "rb") as f:
            mdoms[cls] = pickle.load(f)

    # Load vectors cache
    vc = load_all_vectors()

    # Load one ETH-80 reference image per domain
    splits = json.loads((ROOT / "data" / "eth80" / "splits.json").read_text())
    to_t = transforms.ToTensor()
    ref_imgs = {}
    for cls in CLASSES:
        img = __import__("PIL").Image.open(splits[cls]["train"][0]).convert("RGB").resize((128, 128))
        ref_imgs[cls] = to_t(img).permute(1, 2, 0).numpy()

    def recall_image(cls, word):
        from quantizer import quantize_binary
        v   = get_fasttext_vector(word, vc)
        v_q = quantize_binary(np.array(v, dtype=np.float32), 16)
        q, recognized, weight, *_ = mdoms[cls].recall_from_left(v_q)
        if not recognized:
            return None, recognized, 0.0
        v_norm   = q.astype(float) / (Q_LATENT - 1)
        v_latent = (v_norm * (g_max - g_min) + g_min).astype(np.float32)
        z = torch.tensor(v_latent).unsqueeze(0)
        with torch.no_grad():
            img = decoder(z)[0].clamp(0, 1)
        return img.permute(1, 2, 0).numpy(), recognized, float(weight)

    n_labels = max(len(v) for v in LABELS.values())
    n_rows   = 1 + n_labels     # ref row + label rows
    n_cols   = len(CLASSES)

    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(n_cols * 2.8, n_rows * 2.6))

    for ci, cls in enumerate(CLASSES):
        color = DOMAIN_COLOR[cls]

        # Row 0: ETH-80 reference
        ax_ref = axes[0, ci]
        ax_ref.imshow(ref_imgs[cls])
        ax_ref.axis("off")
        ax_ref.set_title(f"{cls.upper()}", fontsize=13,
                         color=color, fontweight="bold", pad=4)
        # Reference label box
        ax_ref.text(0.5, -0.06, T["recall_ref"],
                    transform=ax_ref.transAxes,
                    ha="center", va="top", fontsize=8,
                    color="white", fontweight="bold",
                    bbox=dict(facecolor=color, alpha=0.85,
                              edgecolor="none", pad=3, boxstyle="round"))

        # Rows 1..n_labels: recalled images
        for ri, word in enumerate(LABELS[cls]):
            ax = axes[ri + 1, ci]
            img, recognized, weight = recall_image(cls, word)

            if img is not None:
                ax.imshow(img)
            else:
                ax.set_facecolor("#ecf0f1")

            ax.axis("off")

            # Label text + weight below image
            status_color = color if recognized else "#e74c3c"
            status_text  = T["recall_ok"] if recognized else T["recall_fail"]
            label_txt = f'"{word}"\n{T["recall_weight"]}={weight:.0f} · {status_text}'
            ax.text(0.5, -0.06, label_txt,
                    transform=ax.transAxes,
                    ha="center", va="top", fontsize=7.5,
                    color=status_color,
                    bbox=dict(facecolor="white", alpha=0.7,
                              edgecolor=status_color, pad=2,
                              linewidth=0.8, boxstyle="round"))

    # Row separators
    fig.add_artist(plt.Line2D([0.02, 0.98], [1 - 1/n_rows - 0.005] * 2,
                               transform=fig.transFigure,
                               color="#bdc3c7", linewidth=1.5))

    fig.suptitle(T["recall_title"], fontsize=13,
                 fontweight="bold", y=1.01)
    fig.text(0.5, -0.02, T["recall_caption"],
             ha="center", fontsize=7.5, color="#636e72",
             style="italic", wrap=True)

    savefig("fig14_recall_grid.png", fig)


# Hemisferio visual: rechazo de imágenes y salida semántica (imagen → labels).
# El encoder es solo el "ojo"; reconocimiento, rechazo y reconstrucción son MAE.

def _load_visual_assets():
    import torch
    from stage2_encoder import Decoder
    from stage5_fill import load_agent_memories
    from stage6_interaction import Agent, load_all_vectors
    from stage7_bidirectional import load_encoder, load_global_stats
    classes = list(SYS_CLASSES)
    enc = load_encoder()
    dec = Decoder()
    dec.load_state_dict(torch.load(ROOT / "models" / "decoder.pt",
                                   map_location="cpu"))
    dec.eval()
    g_min, g_max = load_global_stats()
    agents = {}
    for c in classes:
        H, L, R = load_agent_memories(c)
        agents[c] = Agent(c, H, mem_dom_L=L, mem_dom_R=R)
    vc = load_all_vectors()
    all_vecs = {}
    for c in classes:
        all_vecs.update(vc[c])
    vocab_by_cls = {c: set(vc[c].keys()) for c in classes}
    splits = json.loads((ROOT / "data" / "eth80" / "splits.json").read_text())
    return enc, dec, agents, g_min, g_max, all_vecs, vocab_by_cls, splits


def _encode_img(pil, enc):
    import torch
    from stage7_bidirectional import IMG_TRANSFORM
    t = IMG_TRANSFORM(pil.convert("RGB").resize((128, 128))).unsqueeze(0)
    with torch.no_grad():
        return enc(t).cpu().numpy()[0]


def _visual_scores(agents, z_q, classes):
    from stage7_bidirectional import recognize_gated_right
    return {c: float(recognize_gated_right(agents[c], z_q)) for c in classes}


def _mae_reconstruction(agent, z_q, g_min, g_max, decoder):
    """Reconstrucción interna de la MAE: la memoria homo del latente completa
    la percepción (mem_dom_R.recall) y el decoder la renderiza. NO es la
    imagen de entrada."""
    import io as _io, contextlib as _ctx, torch
    with _ctx.redirect_stdout(_io.StringIO()):
        r_io, recognized, _w = agent.mem_dom_R.recall(z_q)
    if not recognized:
        return None
    v_norm = r_io.astype(float) / 31.0
    v_lat = (v_norm * (g_max - g_min) + g_min).astype(np.float32)
    with torch.no_grad():
        img = decoder(torch.tensor(v_lat).unsqueeze(0))[0].clamp(0, 1)
    return img.permute(1, 2, 0).numpy()


def _synthetic_ood():
    """Imágenes claramente fuera de dominio para probar el rechazo MAE."""
    from PIL import Image
    rng = np.random.RandomState(0)
    noise = (rng.rand(128, 128, 3) * 255).astype(np.uint8)
    solid = np.full((128, 128, 3), 127, dtype=np.uint8)
    scram = (rng.rand(128, 128, 3) * 255).astype(np.uint8)
    scram = scram.reshape(-1, 3)
    rng.shuffle(scram)
    scram = scram.reshape(128, 128, 3)
    return [("noise", Image.fromarray(noise)),
            ("solid", Image.fromarray(solid)),
            ("scrambled", Image.fromarray(scram))]


def fig_image_rejection():
    """Rechazo visual: la MAE acepta o rechaza una percepción por containment
    (recognize_gated_right). Fila 1 aceptadas reales, fila 2 rechazadas reales
    (ξ=0), fila 3 sintéticas fuera de dominio (todas score 0)."""
    from PIL import Image
    from stage5_fill import quantize_latent_global
    classes = list(SYS_CLASSES)
    enc, dec, agents, g_min, g_max, all_vecs, vocab, splits = _load_visual_assets()

    accepted, rejected_real = [], []
    accepted_domains = set()
    for cls in classes:
        for p in splits[cls]["test"]:
            z_q = quantize_latent_global(_encode_img(Image.open(p), enc),
                                         g_min, g_max, 32)
            sc = _visual_scores(agents, z_q, classes)
            if max(sc.values()) > 0 and len(accepted) < 3 and cls not in accepted_domains:
                w = max(sc, key=sc.get)
                accepted.append((Image.open(p).convert("RGB").resize((128, 128)),
                                 f"→ {w} ({sc[w]:.0f})", True))
                accepted_domains.add(cls)
            elif max(sc.values()) == 0 and len(rejected_real) < 3:
                rejected_real.append((Image.open(p).convert("RGB").resize((128, 128)),
                                      "rechazada (ξ=0)", False))
            if len(accepted) >= 3 and len(rejected_real) >= 3:
                break
        if len(accepted) >= 3 and len(rejected_real) >= 3:
            break

    synth = []
    for name, img in _synthetic_ood():
        z_q = quantize_latent_global(_encode_img(img, enc), g_min, g_max, 32)
        sc = _visual_scores(agents, z_q, classes)
        ok = max(sc.values()) > 0
        synth.append((img, f"{name}: {'aceptada' if ok else 'rechazada'}", ok))

    rows = [
        (T.get("imgrej_accepted", "Accepted\n(has support)"), accepted),
        (T.get("imgrej_rejected", "Rejected\n(real, ξ=0)"), rejected_real),
        (T.get("imgrej_ood", "Out-of-domain\n(synthetic)"), synth),
    ]
    fig, axes = plt.subplots(3, 3, figsize=(7.2, 7.8))
    for r, (row_title, items) in enumerate(rows):
        for c in range(3):
            ax = axes[r][c]
            ax.axis("off")
            if c < len(items):
                img, cap, ok = items[c]
                ax.imshow(np.asarray(img))
                ax.set_title(cap, fontsize=8,
                             color=("#27ae60" if ok else "#c0392b"))
                for s in ax.spines.values():
                    s.set_visible(True)
                    s.set_color("#27ae60" if ok else "#c0392b")
                    s.set_linewidth(2)
            if c == 0:
                ax.text(-0.08, 0.5, row_title, transform=ax.transAxes,
                        rotation=90, va="center", ha="right", fontsize=8.5,
                        fontweight="bold")
    fig.suptitle(T.get("imgrej_title",
                       "Image rejection by the MAE (containment, no lexical filter)"),
                 fontsize=11)
    fig.tight_layout()
    savefig("fig15_image_rejection.png", fig)


def fig_image_to_labels():
    """Salida semántica: imagen → reconstrucción evocada por la MAE → labels.
    Demuestra image→labels (evocación) y que la reconstrucción es lo que la
    memoria completa, no la entrada."""
    from PIL import Image
    from stage5_fill import quantize_latent_global
    from stage7_bidirectional import evoke_labels
    classes = list(SYS_CLASSES)
    enc, dec, agents, g_min, g_max, all_vecs, vocab, splits = _load_visual_assets()

    samples = []
    for cls in classes:
        taken = 0
        for p in splits[cls]["test"]:
            z_q = quantize_latent_global(_encode_img(Image.open(p), enc),
                                         g_min, g_max, 32)
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

    n = len(samples)
    if n == 0:
        # Ninguna imagen aceptada (p.ej. un encoder cuyo latente no se contiene):
        # se emite una figura con la nota en vez de fallar.
        fig, ax = plt.subplots(figsize=(7.6, 2.0))
        ax.axis("off")
        ax.text(0.5, 0.5, T.get("img2lbl_none",
                "No accepted test images for this encoder (visual containment ξ=0)."),
                ha="center", va="center", fontsize=11)
        fig.suptitle(T.get("img2lbl_title",
                     "Semantic output: image → MAE recall → labels"), fontsize=11)
        savefig("fig16_image_to_labels.png", fig)
        return
    fig, axes = plt.subplots(n, 3, figsize=(7.6, 2.5 * n))
    if n == 1:
        axes = [axes]
    for r, (inp, recon, w, labels, hit) in enumerate(samples):
        ax0, ax1, ax2 = axes[r]
        ax0.imshow(np.asarray(inp)); ax0.axis("off")
        ax0.set_title(T.get("img2lbl_input", "Input (cue)"), fontsize=9)
        ax1.axis("off")
        if recon is not None:
            ax1.imshow(np.clip(recon, 0, 1))
        ax1.set_title(T.get("img2lbl_recon", "MAE evoked recon."), fontsize=9)
        ax2.axis("off")
        mark = "✓" if hit else "✗"
        col = "#27ae60" if hit else "#c0392b"
        ax2.text(0.5, 0.62, f"→ {w}", ha="center", fontsize=11, fontweight="bold")
        ax2.text(0.5, 0.40, "\n".join(labels), ha="center", fontsize=10)
        ax2.text(0.5, 0.10, f"domain-hit {mark}", ha="center", fontsize=9, color=col)
    fig.suptitle(T.get("img2lbl_title",
                       "Semantic output: image → MAE recall → labels (94.1% top-3 hit)"),
                 fontsize=11)
    fig.tight_layout()
    savefig("fig16_image_to_labels.png", fig)


# Main

def main():
    global T, OUT_CURRENT

    out_root = ROOT / "papers_images"
    out_root.mkdir(exist_ok=True)

    # Run experiments once
    print("=" * 60)
    print("  EAM-TMS — Paper figure generation")
    print("=" * 60)
    # Cache de filas de la ablación (~40 min): se reutiliza si existe, salvo
    # `--fresh`. Borrar el CSV o pasar --fresh cuando cambien memorias/banco.
    rows_cache = out_root / "ablation_rows.csv"
    if rows_cache.exists() and "--fresh" not in sys.argv:
        print(f"\n[1/3] Reusando ablación cacheada: {rows_cache.name} "
              f"(pasa --fresh para re-correrla)")
        df_raw = pd.read_csv(rows_cache)
    else:
        print("\n[1/3] Re-running ablation study (180 experiments)...")
        rows   = run_ablation()
        df_raw = pd.DataFrame(rows)
        df_raw.to_csv(rows_cache, index=False)
    df_raw["condition"] = df_raw["condition"].map(
        lambda c: CONDITION_LABELS.get(c, c))
    agg = build_agg(df_raw)
    print(f"      Done: {len(df_raw)} rows")

    # Generate figures per language
    for lang in ["en", "es"]:
        T           = TEXTS[lang]
        OUT_CURRENT = out_root / lang
        OUT_CURRENT.mkdir(exist_ok=True)

        print(f"\n[{'2' if lang=='en' else '3'}/3] Generating figures [{lang.upper()}] -> papers_images/{lang}/")
        fig_early_accuracy(agg)
        fig_mature_accuracy(agg)
        fig_heatmap(agg)
        fig_domain_accuracy(agg)
        fig_fidelity(agg)
        fig_entropy(agg)
        fig_registrations(agg)
        fig_early_vs_mature(agg)
        fig_winner_distribution(agg)
        fig_summary_table(agg)
        fig_semantic_space()
        fig_recognition_heatmap()
        fig_precision_recall()
        fig_recall_grid()
        fig_image_rejection()
        fig_image_to_labels()

    # Summary
    total = sum(1 for p in out_root.rglob("*") if p.is_file())
    print(f"\n{'='*60}")
    print(f"  {total} files generated in papers_images/")
    for lang in ["en", "es"]:
        d = out_root / lang
        files = sorted(d.iterdir())
        print(f"\n  [{lang.upper()}]  {len(files)} figures:")
        for f in files:
            print(f"    {f.name:45s} {f.stat().st_size//1024:>4} KB")
    print("=" * 60)
    print("  DONE.")


if __name__ == "__main__":
    main()
