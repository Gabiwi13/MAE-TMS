"""
Experimento de escalado: fidelidad fase madura para N = 10, 20, 40, 80 queries.
Para cada N:
  1. Carga M_dom pre-entrenados (stage5, read-only).
  2. Crea agentes con M_dir vacio.
  3. Corre fase temprana con N queries -> llena M_dir.
  4. Corre fase madura con las mismas N queries -> mide fidelidad.
  5. Calcula tambien accuracy vs ground truth.
"""
import pickle
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from stage6_interaction import (
    Agent, TME, CLASSES, MODELS_DIR, DEVICE,
    process_query, get_nlp, load_decoder, load_all_vectors,
    tokenize_query, get_fasttext_vector,
)
from stage8_mature import route_mature
from quantizer import quantize_binary

M_LABEL = 16

# -----------------------------------------------------------------------
# Banco de 80 queries (interleaved: apple/horse/car/apple/horse/car/...)
# Cada query usa tokens presentes en los labels de ConceptNet del dominio.
# -----------------------------------------------------------------------

APPLE_QUERIES = [
    "a round red fruit",
    "green food from trees",
    "red or green round food",
    "has core and seeds",
    "a delicious pome",
    "red fruit with a stem",
    "grows on fruit trees",
    "juicy round fruit",
    "sweet core fruit",
    "a pear or apple fruit",
    "fruit with skin and seeds",
    "orange cousin red food",
    "green and red food",
    "a macintosh variety",
    "made into pie",
    "round red food",
    "stem leaf core inside",
    "a green fruit",
    "fruit with seeds inside",
    "delicious red round fruit",
    "adam and eve fruit",
    "orange red green food",
    "core inside skin fruit",
    "tree fruit food",
    "pome variety fruit",
    "green round food",
    "red sweet fruit food",
]

HORSE_QUERIES = [
    "animal with a mane",
    "large powerful mammal",
    "has four legs and hooves",
    "riding and racing animal",
    "an equine animal",
    "big farm animal",
    "has a long tail",
    "a pony or donkey",
    "mammal with saddle",
    "racing animal with mane",
    "big four legged animal",
    "riding farm animal",
    "farm mammal with mane",
    "equine riding beast",
    "has hooves and tail",
    "donkey and zebra relative",
    "big strong animal",
    "saddle riding animal",
    "cow and horse farm animals",
    "animal that races",
    "a ridden animal",
    "four legged riding mammal",
    "mammal with hooves and mane",
    "equine with saddle",
    "big farm riding animal",
    "domesticated equine mammal",
    "animal with mane and tail",
]

CAR_QUERIES = [
    "fast vehicle with wheels",
    "machine for transportation",
    "automobile with seats",
    "has wheels and engine",
    "a heavy vehicle",
    "passenger transportation machine",
    "seats and windows inside",
    "a motor vehicle",
    "used for driving",
    "wheeled automobile",
    "driving machine",
    "automobile with heavy seats",
    "crash and accident vehicle",
    "passenger seats inside",
    "vehicle with driver",
    "red automobile",
    "transportation vehicle",
    "automobile for transport",
    "seats and windows vehicle",
    "heavy automobile",
    "motor vehicle transport",
    "driver automobile",
    "wheeled transportation",
    "crash vehicle",
    "automobile commuting",
    "auto transportation machine",
]

# Interleaved: apple[i], horse[i], car[i]
ALL_QUERIES = []
GROUND_TRUTH = []
max_len = max(len(APPLE_QUERIES), len(HORSE_QUERIES), len(CAR_QUERIES))
for i in range(max_len):
    if i < len(APPLE_QUERIES):
        ALL_QUERIES.append(APPLE_QUERIES[i])
        GROUND_TRUTH.append("apple")
    if i < len(HORSE_QUERIES):
        ALL_QUERIES.append(HORSE_QUERIES[i])
        GROUND_TRUTH.append("horse")
    if i < len(CAR_QUERIES):
        ALL_QUERIES.append(CAR_QUERIES[i])
        GROUND_TRUTH.append("car")

assert len(ALL_QUERIES) == 80, f"Expected 80 queries, got {len(ALL_QUERIES)}"

N_VALUES = [10, 20, 40, 80]


# -----------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------

def load_fresh_agents() -> dict:
    """Load M_dom from stage5 pickles, create Agent with fresh (empty) M_dir."""
    agents = {}
    for cls in CLASSES:
        with open(MODELS_DIR / f"mem_dom_{cls}.pkl", "rb") as f:
            mem = pickle.load(f)
        agents[cls] = Agent(cls, mem)
    return agents


def run_one_experiment(N: int, nlp, decoder, vectors_cache: dict,
                       verbose: bool = False) -> dict:
    """
    Full experiment for N queries:
    - early phase: build M_dir from N queries
    - mature phase: test same N queries without TME
    Returns dict with fidelity, early_accuracy, mature_accuracy, and per-query details.
    """
    queries = ALL_QUERIES[:N]
    gt = GROUND_TRUTH[:N]

    agents = load_fresh_agents()
    tme = TME()

    # ---- EARLY PHASE ----
    early_winners = []
    for q in queries:
        res = process_query(q, agents, tme, nlp, vectors_cache, decoder,
                            verbose=verbose)
        early_winners.append(res["winner"])

    early_accuracy = sum(e == g for e, g in zip(early_winners, gt)) / N

    # ---- MATURE PHASE ----
    rng = np.random.RandomState(42)
    mature_winners = []
    for q in queries:
        entry_cls = CLASSES[rng.randint(0, len(CLASSES))]
        entry_agent = agents[entry_cls]
        res = route_mature(q, entry_agent, agents, nlp, vectors_cache, decoder,
                           verbose=verbose)
        mature_winners.append(res["winner"])

    fidelity = sum(m == e for m, e in zip(mature_winners, early_winners)) / N
    mature_accuracy = sum(m == g for m, g in zip(mature_winners, gt)) / N

    # Per-domain breakdown
    domain_fidelity = {}
    for cls in CLASSES:
        indices = [i for i, g in enumerate(gt) if g == cls]
        if indices:
            match = sum(mature_winners[i] == early_winners[i] for i in indices)
            domain_fidelity[cls] = match / len(indices)
        else:
            domain_fidelity[cls] = 0.0

    domain_early_acc = {}
    for cls in CLASSES:
        indices = [i for i, g in enumerate(gt) if g == cls]
        if indices:
            match = sum(early_winners[i] == cls for i in indices)
            domain_early_acc[cls] = match / len(indices)
        else:
            domain_early_acc[cls] = 0.0

    return {
        "N": N,
        "early_accuracy": early_accuracy,
        "fidelity": fidelity,
        "mature_accuracy": mature_accuracy,
        "domain_fidelity": domain_fidelity,
        "domain_early_acc": domain_early_acc,
        "early_winners": early_winners,
        "mature_winners": mature_winners,
        "ground_truth": gt,
    }


# -----------------------------------------------------------------------
# Visualización
# -----------------------------------------------------------------------

def plot_comparison(all_results: list):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    Ns = [r["N"] for r in all_results]
    early_accs = [r["early_accuracy"] * 100 for r in all_results]
    fidelities = [r["fidelity"] * 100 for r in all_results]
    mature_accs = [r["mature_accuracy"] * 100 for r in all_results]

    # ---- Plot 1: lineas generales ----
    ax = axes[0]
    ax.plot(Ns, early_accs,  "o-", color="#e67e22", linewidth=2, markersize=7,
            label="Early-phase accuracy (vs ground truth)")
    ax.plot(Ns, fidelities,  "s-", color="#2980b9", linewidth=2, markersize=7,
            label="Fidelity (mature matches early)")
    ax.plot(Ns, mature_accs, "^-", color="#27ae60", linewidth=2, markersize=7,
            label="Mature accuracy (vs ground truth)")

    ax.set_xlabel("Numero de queries en fase temprana (N)", fontsize=11)
    ax.set_ylabel("Porcentaje (%)", fontsize=11)
    ax.set_title("Fidelidad vs tamaño de fase temprana", fontsize=12)
    ax.set_xticks(Ns)
    ax.set_ylim(0, 105)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    for x, y1, y2, y3 in zip(Ns, early_accs, fidelities, mature_accs):
        ax.annotate(f"{y1:.0f}%", (x, y1), textcoords="offset points",
                    xytext=(6, 4), fontsize=8, color="#e67e22")
        ax.annotate(f"{y2:.0f}%", (x, y2), textcoords="offset points",
                    xytext=(6, -12), fontsize=8, color="#2980b9")
        ax.annotate(f"{y3:.0f}%", (x, y3), textcoords="offset points",
                    xytext=(6, 4), fontsize=8, color="#27ae60")

    # ---- Plot 2: fidelidad por dominio ----
    ax2 = axes[1]
    colors_domain = {"apple": "#e74c3c", "horse": "#3498db", "car": "#2ecc71"}
    for cls in CLASSES:
        vals = [r["domain_fidelity"][cls] * 100 for r in all_results]
        ax2.plot(Ns, vals, "o-", color=colors_domain[cls], linewidth=2,
                 markersize=7, label=f"Fidelidad {cls}")
        for x, y in zip(Ns, vals):
            ax2.annotate(f"{y:.0f}%", (x, y), textcoords="offset points",
                         xytext=(5, 3), fontsize=8, color=colors_domain[cls])

    ax2.set_xlabel("Numero de queries en fase temprana (N)", fontsize=11)
    ax2.set_ylabel("Fidelidad por dominio (%)", fontsize=11)
    ax2.set_title("Fidelidad por dominio vs N", fontsize=12)
    ax2.set_xticks(Ns)
    ax2.set_ylim(0, 105)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.suptitle("TMS Multiagente — Impacto del tamaño de fase temprana", fontsize=13,
                 fontweight="bold")
    plt.tight_layout()
    out = ROOT / "scaling_comparison.png"
    plt.savefig(out, dpi=120)
    print(f"\nGrafica guardada -> {out.name}")


def print_summary_table(all_results: list):
    print("\n" + "="*70)
    print(f"{'N':>5} | {'Early acc':>10} | {'Fidelidad':>10} | {'Mature acc':>10}")
    print("-"*70)
    for r in all_results:
        print(f"{r['N']:>5} | {r['early_accuracy']*100:>9.1f}% | "
              f"{r['fidelity']*100:>9.1f}% | {r['mature_accuracy']*100:>9.1f}%")
    print("="*70)

    print("\nFidelidad por dominio:")
    print(f"{'N':>5} | {'apple':>8} | {'horse':>8} | {'car':>8}")
    print("-"*40)
    for r in all_results:
        a = r["domain_fidelity"]["apple"] * 100
        h = r["domain_fidelity"]["horse"] * 100
        c = r["domain_fidelity"]["car"] * 100
        print(f"{r['N']:>5} | {a:>7.1f}% | {h:>7.1f}% | {c:>7.1f}%")


def run():
    print("Cargando modelos...")
    nlp = get_nlp()
    decoder = load_decoder()
    vectors_cache = load_all_vectors()

    print(f"Banco de queries: {len(ALL_QUERIES)} total "
          f"({GROUND_TRUTH.count('apple')} apple, "
          f"{GROUND_TRUTH.count('horse')} horse, "
          f"{GROUND_TRUTH.count('car')} car)")

    all_results = []
    for N in N_VALUES:
        print(f"\n--- N = {N} queries ---")
        result = run_one_experiment(N, nlp, decoder, vectors_cache, verbose=False)
        all_results.append(result)
        print(f"  Early accuracy:  {result['early_accuracy']*100:.1f}%")
        print(f"  Fidelidad:       {result['fidelity']*100:.1f}%")
        print(f"  Mature accuracy: {result['mature_accuracy']*100:.1f}%")
        for cls in CLASSES:
            df = result["domain_fidelity"][cls]
            da = result["domain_early_acc"][cls]
            print(f"    {cls}: early_acc={da*100:.1f}%  fidelity={df*100:.1f}%")

    print_summary_table(all_results)
    plot_comparison(all_results)
    print("\nExperimento de escalado COMPLETADO.")
    return all_results


if __name__ == "__main__":
    run()
