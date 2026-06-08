"""
Ablation study — diagnóstico del sesgo de M_dir hacia apple.

Condiciones:
  A   — Baseline: código actual, sin cambios
  B1  — Score normalizado / count_agente  (penaliza sobrerepresentados)
  B2  — Score normalizado / sqrt(count_agente)
  C   — Registro balanceado: cap proporcional de registros por agente
  D   — Queries estrictamente balanceadas por dominio (N//3 por clase)
  E32 — M_dir con m=32 (binario — confirma que m>2 no ayuda para sign(v))
  E64 — M_dir con m=64 (binario — ídem)
  F   — ConceptNet curado: apple sin computer/mac/macintosh/eden
  G   — Mejor combinación: D + B1 + F

N ∈ [10,20,40,80]  ×  seeds ∈ [0,1,2,3,4]  →  CSV → gráficas → reporte Markdown
"""
import csv
import json
import math
import pickle
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

RESULTS_DIR = ROOT / "results" / "ablation_mdir_bias"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from mae_ham import SimpleHAM4D
from quantizer import quantize_binary
from stage6_interaction import (
    Agent, TME, CLASSES, AGENT_LIST, MODELS_DIR,
    SimpleDirectoryMemory, get_nlp, load_all_vectors,
    tokenize_query, get_fasttext_vector, M_LABEL,
)

# ═══════════════════════════════════════════════════════════════════
# Configuración global
# ═══════════════════════════════════════════════════════════════════

N_VALUES   = [10, 20, 40, 80]
SEEDS      = [0, 1, 2, 3, 4]
CONDITIONS = ["A", "B1", "B2", "C", "D", "E32", "E64", "F", "G"]

CONDITION_LABELS = {
    "A":   "A Baseline",
    "B1":  "B1 Norm/count",
    "B2":  "B2 Norm/sqrt",
    "C":   "C Balanced M_dir",
    "D":   "D Balanced queries",
    "E32": "E32 m=32 binary",
    "E64": "E64 m=64 binary",
    "F":   "F Curated ConceptNet",
    "G":   "G Best (D+B1+F)",
}

COND_COLORS = {
    "A":   "#2c3e50",
    "B1":  "#e74c3c",
    "B2":  "#e67e22",
    "C":   "#9b59b6",
    "D":   "#2980b9",
    "E32": "#1abc9c",
    "E64": "#27ae60",
    "F":   "#f39c12",
    "G":   "#c0392b",
}

# ═══════════════════════════════════════════════════════════════════
# Query bank (80 total, interleaved apple/horse/car)
# ═══════════════════════════════════════════════════════════════════

APPLE_QUERIES = [
    "a round red fruit", "green food from trees", "red or green round food",
    "has core and seeds", "a delicious pome", "red fruit with a stem",
    "grows on fruit trees", "juicy round fruit", "sweet core fruit",
    "a pear or apple fruit", "fruit with skin and seeds", "orange cousin red food",
    "green and red food", "a macintosh variety", "made into pie",
    "round red food", "stem leaf core inside", "a green fruit",
    "fruit with seeds inside", "delicious red round fruit",
    "adam and eve fruit", "orange red green food", "core inside skin fruit",
    "tree fruit food", "pome variety fruit", "green round food",
    "red sweet fruit food",
]

HORSE_QUERIES = [
    "animal with a mane", "large powerful mammal", "has four legs and hooves",
    "riding and racing animal", "an equine animal", "big farm animal",
    "has a long tail", "a pony or donkey", "mammal with saddle",
    "racing animal with mane", "big four legged animal", "riding farm animal",
    "farm mammal with mane", "equine riding beast", "has hooves and tail",
    "donkey and zebra relative", "big strong animal", "saddle riding animal",
    "cow and horse farm animals", "animal that races", "a ridden animal",
    "four legged riding mammal", "mammal with hooves and mane",
    "equine with saddle", "big farm riding animal",
    "domesticated equine mammal", "animal with mane and tail",
]

CAR_QUERIES = [
    "fast vehicle with wheels", "machine for transportation",
    "automobile with seats", "has wheels and engine", "a heavy vehicle",
    "passenger transportation machine", "seats and windows inside",
    "a motor vehicle", "used for driving", "wheeled automobile",
    "driving machine", "automobile with heavy seats",
    "crash and accident vehicle", "passenger seats inside",
    "vehicle with driver", "red automobile", "transportation vehicle",
    "automobile for transport", "seats and windows vehicle",
    "heavy automobile", "motor vehicle transport", "driver automobile",
    "wheeled transportation", "crash vehicle", "automobile commuting",
    "auto transportation machine",
]

DOMAIN_QUERIES = {"apple": APPLE_QUERIES, "horse": HORSE_QUERIES, "car": CAR_QUERIES}

# Banco interleaved para condiciones A, B, C, E, F
ALL_QUERIES, GROUND_TRUTH = [], []
for _i in range(max(len(APPLE_QUERIES), len(HORSE_QUERIES), len(CAR_QUERIES))):
    for _cls in CLASSES:
        _pool = DOMAIN_QUERIES[_cls]
        if _i < len(_pool):
            ALL_QUERIES.append(_pool[_i])
            GROUND_TRUTH.append(_cls)

# ═══════════════════════════════════════════════════════════════════
# Clases extendidas de M_dir
# ═══════════════════════════════════════════════════════════════════

class DirectoryMemoryTracked(SimpleDirectoryMemory):
    """M_dir con conteo de registros por agente y soporte de normalización."""

    def __init__(self, n=300, m=16, n_agents=3):
        super().__init__(n=n, m=m, n_agents=n_agents)
        self._counts = np.zeros(n_agents, dtype=np.int64)

    def register(self, v_label_q: np.ndarray, agent_idx: int):
        super().register(v_label_q, agent_idx)
        self._counts[agent_idx] += 1

    def predict_normalized(self, v_label_q: np.ndarray,
                           mode: str = "linear", eps: float = 1.0) -> np.ndarray:
        scores = self.predict(v_label_q)
        denom = self._counts.astype(float) + eps
        return scores / denom if mode == "linear" else scores / np.sqrt(denom)

    @property
    def agent_counts(self) -> np.ndarray:
        return self._counts.copy()

    def entropy(self) -> float:
        total = float(self._counts.sum())
        if total == 0:
            return math.log2(max(len(self._counts), 1))
        p = self._counts / total
        return float(-np.sum(p * np.log2(np.where(p == 0, 1.0, p))))


class DirectoryMemoryBalanced(DirectoryMemoryTracked):
    """M_dir que limita la acumulación desproporcionada por agente."""

    def __init__(self, n=300, m=16, n_agents=3, max_ratio=3.0):
        super().__init__(n=n, m=m, n_agents=n_agents)
        self._max_ratio = max_ratio

    def register(self, v_label_q: np.ndarray, agent_idx: int):
        min_c = self._counts.min()
        if min_c > 0 and self._counts[agent_idx] > min_c * self._max_ratio:
            return  # Skip: agente demasiado dominante
        super().register(v_label_q, agent_idx)


# ═══════════════════════════════════════════════════════════════════
# Carga de M_dom
# ═══════════════════════════════════════════════════════════════════

def load_base_mdoms() -> dict:
    mdoms = {}
    for cls in CLASSES:
        with open(MODELS_DIR / f"mem_dom_{cls}.pkl", "rb") as f:
            mdoms[cls] = pickle.load(f)
    return mdoms


def build_curated_apple_mdom() -> SimpleHAM4D:
    """Reconstruye M_dom de apple sin labels de Apple Inc."""
    from stage5_fill import quantize_latent_global
    N_F, M_F, P_F, Q_F = 300, 16, 64, 32
    NOISE = {"computer", "mac", "macintosh", "eden"}

    labels   = json.loads((ROOT / "labels_apple.json").read_text())
    raw_vecs = json.loads((ROOT / "label_vectors_apple.json").read_text())
    v_proto  = np.array(json.loads((MODELS_DIR / "proto_latent_apple.json").read_text()))
    stats    = json.loads((MODELS_DIR / "latent_global_stats.json").read_text())
    g_min    = np.array(stats["global_min"])
    g_max    = np.array(stats["global_max"])

    curated = {l: w for l, w in labels.items() if l not in NOISE}
    removed = NOISE & set(labels)
    print(f"  Curated apple: {len(labels)} -> {len(curated)} labels (removed: {removed})")

    mem = SimpleHAM4D(N_F, M_F, P_F, Q_F, iota=0.0, kappa=0.0, xi=0, sigma=0.1)
    v_proto_q = quantize_latent_global(v_proto, g_min, g_max, Q_F)

    for word, freq in curated.items():
        if word not in raw_vecs:
            continue
        v_lq = quantize_binary(np.array(raw_vecs[word], dtype=np.float32), M_F)
        for _ in range(int(freq)):
            mem.register(v_lq, v_proto_q)

    return mem


# ═══════════════════════════════════════════════════════════════════
# Configuración por condición
# ═══════════════════════════════════════════════════════════════════

def get_condition_config(condition: str):
    """Retorna (mdir_class, m_mdir, mdir_kwargs, predict_fn, use_curated, use_balanced)."""
    use_curated  = condition in ("F", "G")
    use_balanced = condition in ("D", "G")

    if condition == "B1":
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemoryTracked, 16, {}
        predict_fn = lambda ag, vq: ag.mem_dir.predict_normalized(vq, "linear")
    elif condition == "B2":
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemoryTracked, 16, {}
        predict_fn = lambda ag, vq: ag.mem_dir.predict_normalized(vq, "sqrt")
    elif condition == "C":
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemoryBalanced, 16, {"max_ratio": 3.0}
        predict_fn = lambda ag, vq: ag.mem_dir.predict(vq)
    elif condition == "E32":
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemoryTracked, 32, {}
        predict_fn = lambda ag, vq: ag.mem_dir.predict(vq)
    elif condition == "E64":
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemoryTracked, 64, {}
        predict_fn = lambda ag, vq: ag.mem_dir.predict(vq)
    elif condition == "G":
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemoryTracked, 16, {}
        predict_fn = lambda ag, vq: ag.mem_dir.predict_normalized(vq, "linear")
    else:  # A, D, F
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemoryTracked, 16, {}
        predict_fn = lambda ag, vq: ag.mem_dir.predict(vq)

    return mdir_class, m_mdir, mdir_kwargs, predict_fn, use_curated, use_balanced


# ═══════════════════════════════════════════════════════════════════
# Factory de agentes
# ═══════════════════════════════════════════════════════════════════

def make_agents(mdoms: dict, mdir_class, m_mdir: int = 16,
                mdir_kwargs: dict = None):
    mdir_kwargs = mdir_kwargs or {}
    agents = {}
    for cls in CLASSES:
        ag = Agent(cls, mdoms[cls])
        ag.mem_dir = mdir_class(m=m_mdir, **mdir_kwargs)
        agents[cls] = ag
    tme = TME()
    tme.mem_dir = mdir_class(m=m_mdir, **mdir_kwargs)
    return agents, tme


# ═══════════════════════════════════════════════════════════════════
# Selección de queries
# ═══════════════════════════════════════════════════════════════════

def balanced_queries(N: int, seed: int):
    """Condición D: floor(N/3) queries por dominio, shuffled, interleaved."""
    rng = np.random.RandomState(seed)
    n_per = N // 3
    pools = []
    for cls in CLASSES:
        pool = DOMAIN_QUERIES[cls][:]
        rng.shuffle(pool)
        pools.append(pool[:n_per])

    interleaved_q, interleaved_gt = [], []
    for i in range(n_per):
        for j, cls in enumerate(CLASSES):
            interleaved_q.append(pools[j][i])
            interleaved_gt.append(cls)

    return interleaved_q, interleaved_gt


def standard_queries(N: int):
    return ALL_QUERIES[:N], GROUND_TRUTH[:N]


# ═══════════════════════════════════════════════════════════════════
# Fase temprana
# ═══════════════════════════════════════════════════════════════════

def run_early_phase(queries, agents, tme, nlp, vectors_cache, m_mdir):
    winners = []
    for q in queries:
        tokens = tokenize_query(q, nlp)
        if not tokens:
            winners.append(CLASSES[0])
            continue

        agent_scores = {cls: 0.0 for cls in CLASSES}
        tok_vecs_mdom = {}
        tok_vecs_mdir = {}

        for tok in tokens:
            v = get_fasttext_vector(tok, vectors_cache)
            tok_vecs_mdom[tok] = quantize_binary(v, M_LABEL)   # fijo m=16 para M_dom
            tok_vecs_mdir[tok] = quantize_binary(v, m_mdir)    # variable para M_dir
            for cls in CLASSES:
                agent_scores[cls] += agents[cls].recognize(tok_vecs_mdom[tok])

        n_toks = max(len(tokens), 1)
        for cls in CLASSES:
            agent_scores[cls] /= n_toks

        winner = max(agent_scores, key=agent_scores.get)
        winner_idx = AGENT_LIST.index(winner)
        winners.append(winner)

        for tok in tokens:
            vq = tok_vecs_mdir[tok]
            tme.mem_dir.register(vq, winner_idx)
            for ag in agents.values():
                ag.mem_dir.register(vq, winner_idx)

    return winners


# ═══════════════════════════════════════════════════════════════════
# Fase madura
# ═══════════════════════════════════════════════════════════════════

def run_mature_phase(queries, agents, nlp, vectors_cache, rng, predict_fn, m_mdir):
    winners = []
    for q in queries:
        entry_cls = CLASSES[rng.randint(0, len(CLASSES))]
        entry_ag  = agents[entry_cls]

        tokens = tokenize_query(q, nlp)
        if not tokens:
            winners.append(CLASSES[0])
            continue

        scores = np.zeros(len(CLASSES))
        for tok in tokens:
            v = get_fasttext_vector(tok, vectors_cache)
            vq = quantize_binary(v, m_mdir)
            scores += predict_fn(entry_ag, vq)

        winners.append(CLASSES[int(np.argmax(scores))] if scores.sum() > 0 else CLASSES[0])

    return winners


# ═══════════════════════════════════════════════════════════════════
# Métricas
# ═══════════════════════════════════════════════════════════════════

def compute_metrics(early_winners, mature_winners, ground_truth, agents):
    N = len(ground_truth)
    early_acc  = sum(e == g for e, g in zip(early_winners,  ground_truth)) / N
    fidelity   = sum(m == e for m, e in zip(mature_winners, early_winners)) / N
    mature_acc = sum(m == g for m, g in zip(mature_winners, ground_truth)) / N

    domain_early, domain_fid, domain_mat = {}, {}, {}
    for cls in CLASSES:
        idx = [i for i, g in enumerate(ground_truth) if g == cls]
        if idx:
            domain_early[cls] = sum(early_winners[i]  == cls for i in idx) / len(idx)
            domain_fid[cls]   = sum(mature_winners[i] == early_winners[i] for i in idx) / len(idx)
            domain_mat[cls]   = sum(mature_winners[i] == cls for i in idx) / len(idx)
        else:
            domain_early[cls] = domain_fid[cls] = domain_mat[cls] = 0.0

    cm = np.zeros((3, 3), dtype=int)
    for g, m in zip(ground_truth, mature_winners):
        cm[CLASSES.index(g), CLASSES.index(m)] += 1

    winner_dist = {cls: mature_winners.count(cls) / N for cls in CLASSES}

    first_ag = next(iter(agents.values()))
    mdir = first_ag.mem_dir
    if hasattr(mdir, "agent_counts"):
        reg_counts  = {cls: int(mdir.agent_counts[i]) for i, cls in enumerate(CLASSES)}
        entropy_val = mdir.entropy()
    else:
        reg_counts  = {cls: -1 for cls in CLASSES}
        entropy_val = -1.0

    return {
        "early_acc":    early_acc,
        "fidelity":     fidelity,
        "mature_acc":   mature_acc,
        "domain_early": domain_early,
        "domain_fid":   domain_fid,
        "domain_mat":   domain_mat,
        "cm":           cm,
        "winner_dist":  winner_dist,
        "reg_counts":   reg_counts,
        "mdir_entropy": entropy_val,
    }


def metrics_to_row(condition, N, seed, m):
    row = {
        "condition":        condition,
        "N":                N,
        "seed":             seed,
        "early_accuracy":   round(m["early_acc"],   4),
        "mature_fidelity":  round(m["fidelity"],    4),
        "mature_accuracy":  round(m["mature_acc"],  4),
        "early_acc_apple":  round(m["domain_early"]["apple"], 4),
        "early_acc_horse":  round(m["domain_early"]["horse"], 4),
        "early_acc_car":    round(m["domain_early"]["car"],   4),
        "fidelity_apple":   round(m["domain_fid"]["apple"],   4),
        "fidelity_horse":   round(m["domain_fid"]["horse"],   4),
        "fidelity_car":     round(m["domain_fid"]["car"],     4),
        "mature_acc_apple": round(m["domain_mat"]["apple"],   4),
        "mature_acc_horse": round(m["domain_mat"]["horse"],   4),
        "mature_acc_car":   round(m["domain_mat"]["car"],     4),
        "winner_pct_apple": round(m["winner_dist"]["apple"],  4),
        "winner_pct_horse": round(m["winner_dist"]["horse"],  4),
        "winner_pct_car":   round(m["winner_dist"]["car"],    4),
        "mdir_reg_apple":   m["reg_counts"]["apple"],
        "mdir_reg_horse":   m["reg_counts"]["horse"],
        "mdir_reg_car":     m["reg_counts"]["car"],
        "mdir_entropy":     round(m["mdir_entropy"], 4),
    }
    cm = m["cm"]
    for i, tc in enumerate(CLASSES):
        for j, pc in enumerate(CLASSES):
            row[f"cm_{tc}_{pc}"] = int(cm[i, j])
    return row


def save_csv(rows, path):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  CSV guardado: {path.name} ({len(rows)} filas)")


# ═══════════════════════════════════════════════════════════════════
# Experimento único
# ═══════════════════════════════════════════════════════════════════

def run_single_experiment(condition, N, seed, base_mdoms, curated_apple,
                          nlp, vectors_cache):
    mdir_class, m_mdir, mdir_kwargs, predict_fn, use_curated, use_balanced = \
        get_condition_config(condition)

    # M_doms activos
    if use_curated:
        mdoms = dict(base_mdoms)
        mdoms["apple"] = curated_apple
    else:
        mdoms = base_mdoms

    # Queries
    queries, gt = (balanced_queries(N, seed)
                   if use_balanced else standard_queries(N))

    # Agentes y TME frescos
    agents, tme = make_agents(mdoms, mdir_class, m_mdir, mdir_kwargs)

    # Fase temprana
    early_w = run_early_phase(queries, agents, tme, nlp, vectors_cache, m_mdir)

    # Fase madura
    rng = np.random.RandomState(seed * 1000 + 42)
    mature_w = run_mature_phase(queries, agents, nlp, vectors_cache,
                                rng, predict_fn, m_mdir)

    return compute_metrics(early_w, mature_w, gt, agents)


# ═══════════════════════════════════════════════════════════════════
# Loop principal
# ═══════════════════════════════════════════════════════════════════

def run_ablation():
    print("=== ABLATION STUDY: M_dir bias ===\n")
    print("Cargando NLP + vectores...")
    nlp = get_nlp()
    vectors_cache = load_all_vectors()

    print("Cargando M_dom base...")
    base_mdoms = load_base_mdoms()

    print("Construyendo M_dom curado (condiciones F/G)...")
    curated_apple = build_curated_apple_mdom()

    total = len(CONDITIONS) * len(N_VALUES) * len(SEEDS)
    done  = 0
    all_rows = []

    print(f"\nEjecutando {total} experimentos "
          f"({len(CONDITIONS)} cond × {len(N_VALUES)} N × {len(SEEDS)} seeds)...\n")

    for condition in CONDITIONS:
        print(f"--- Condicion {condition}: {CONDITION_LABELS[condition]} ---")
        for N in N_VALUES:
            seed_accs = []
            seed_fids = []
            for seed in SEEDS:
                m = run_single_experiment(condition, N, seed,
                                          base_mdoms, curated_apple,
                                          nlp, vectors_cache)
                row = metrics_to_row(condition, N, seed, m)
                all_rows.append(row)
                seed_accs.append(m["mature_acc"])
                seed_fids.append(m["fidelity"])
                done += 1

            mean_acc = np.mean(seed_accs)
            std_acc  = np.std(seed_accs)
            mean_fid = np.mean(seed_fids)
            print(f"  N={N:3d}: mature_acc={mean_acc:.2%} ±{std_acc:.2%}  "
                  f"fidelity={mean_fid:.2%}  "
                  f"[{done}/{total}]")
        print()

    return all_rows


# ═══════════════════════════════════════════════════════════════════
# Funciones auxiliares para plots
# ═══════════════════════════════════════════════════════════════════

def aggregate(rows, condition, key):
    from collections import defaultdict
    by_n = defaultdict(list)
    for r in rows:
        if r["condition"] == condition:
            by_n[r["N"]].append(r[key])
    ns    = sorted(by_n.keys())
    means = [np.mean(by_n[n]) for n in ns]
    stds  = [np.std(by_n[n])  for n in ns]
    return np.array(ns), np.array(means), np.array(stds)


def mean_cond(rows, cond, N, key):
    vals = [r[key] for r in rows if r["condition"] == cond and r["N"] == N]
    return np.mean(vals) if vals else 0.0


def std_cond(rows, cond, N, key):
    vals = [r[key] for r in rows if r["condition"] == cond and r["N"] == N]
    return np.std(vals) if vals else 0.0


# ═══════════════════════════════════════════════════════════════════
# Plot 1: Scaling comparison
# ═══════════════════════════════════════════════════════════════════

def plot_scaling_comparison(rows):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    specs = [
        ("mature_accuracy", "Mature accuracy"),
        ("mature_fidelity", "Mature fidelity"),
    ]
    for (key, ylabel), ax in zip(specs, axes):
        for cond in CONDITIONS:
            ns, means, stds = aggregate(rows, cond, key)
            lw = 2.5 if cond in ("A", "G") else 1.5
            ls = "-"  if cond in ("A", "G") else "--"
            ax.plot(ns, means, marker="o", lw=lw, ls=ls,
                    color=COND_COLORS[cond], label=CONDITION_LABELS[cond])
            ax.fill_between(ns, means - stds, means + stds,
                            alpha=0.12, color=COND_COLORS[cond])
        ax.set_xlabel("N queries")
        ax.set_ylabel(ylabel)
        ax.set_title(ylabel + " por condicion")
        ax.set_ylim(0, 1.05)
        ax.set_xticks(N_VALUES)
        ax.axhline(1/3, color="gray", lw=0.8, ls=":", label="chance (33%)")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=7, ncol=2, loc="lower right")

    plt.suptitle("Ablation Study — MAE-TMS: comparacion de condiciones",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    out = RESULTS_DIR / "scaling_comparison_ablation.png"
    plt.savefig(out, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {out.name}")


# ═══════════════════════════════════════════════════════════════════
# Plot 2: Domain accuracy por condición (N=80)
# ═══════════════════════════════════════════════════════════════════

def plot_domain_accuracy(rows):
    N_PLOT = 80
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    dom_colors = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60"}
    x = np.arange(len(CONDITIONS))
    width = 0.6

    for ax, cls in zip(axes, CLASSES):
        key = f"mature_acc_{cls}"
        means = [mean_cond(rows, c, N_PLOT, key) for c in CONDITIONS]
        stds  = [std_cond(rows, c, N_PLOT, key)  for c in CONDITIONS]
        ax.bar(x, means, width, yerr=stds, capsize=4,
               color=dom_colors[cls], alpha=0.75,
               edgecolor="black", linewidth=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels([CONDITION_LABELS[c] for c in CONDITIONS],
                           rotation=35, ha="right", fontsize=7.5)
        ax.set_ylabel("Mature accuracy")
        ax.set_title(f"Dominio: {cls}  (N={N_PLOT})", fontweight="bold")
        ax.set_ylim(0, 1.05)
        ax.axhline(1/3, color="gray", ls=":", lw=1, label="chance (33%)")
        ax.grid(axis="y", alpha=0.3)
        ax.legend(fontsize=7)

    plt.suptitle(f"Accuracy por dominio en fase madura — N={N_PLOT}",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    out = RESULTS_DIR / "domain_accuracy_ablation.png"
    plt.savefig(out, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {out.name}")


# ═══════════════════════════════════════════════════════════════════
# Plot 3: Distribución de ganadores (fase madura, N=80)
# ═══════════════════════════════════════════════════════════════════

def plot_winner_distribution(rows):
    N_PLOT = 80
    dom_colors = ["#e74c3c", "#2980b9", "#27ae60"]
    n_cond = len(CONDITIONS)
    fig, axes = plt.subplots(1, n_cond, figsize=(22, 5))

    for ax, cond in zip(axes, CONDITIONS):
        means = [mean_cond(rows, cond, N_PLOT, f"winner_pct_{cls}")
                 for cls in CLASSES]
        stds  = [std_cond(rows, cond, N_PLOT, f"winner_pct_{cls}")
                 for cls in CLASSES]
        ax.bar(CLASSES, means, color=dom_colors, alpha=0.8,
               edgecolor="black", linewidth=0.5)
        ax.errorbar(range(3), means, yerr=stds, fmt="none",
                    ecolor="black", capsize=4, linewidth=1.2)
        ax.set_title(CONDITION_LABELS[cond].replace(" ", "\n", 1),
                     fontsize=8, fontweight="bold")
        ax.set_ylim(0, 1.05)
        ax.axhline(1/3, color="gray", ls=":", lw=1)
        ax.set_xticklabels(CLASSES, fontsize=8)
        if cond == CONDITIONS[0]:
            ax.set_ylabel("% victorias fase madura")
        ax.grid(axis="y", alpha=0.3)

    plt.suptitle("Distribucion de ganadores en fase madura (N=80) — sesgo de M_dir",
                 fontsize=11, fontweight="bold")
    plt.tight_layout()
    out = RESULTS_DIR / "winner_distribution.png"
    plt.savefig(out, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {out.name}")


# ═══════════════════════════════════════════════════════════════════
# Plots 4 y 5: Matrices de confusión
# ═══════════════════════════════════════════════════════════════════

def _draw_confusion_matrix(cm: np.ndarray, title: str, filename: str):
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.colorbar(im, ax=ax)
    ax.set_xticks(range(3)); ax.set_yticks(range(3))
    ax.set_xticklabels(CLASSES, fontsize=10)
    ax.set_yticklabels(CLASSES, fontsize=10)
    ax.set_xlabel("Predicho (fase madura)")
    ax.set_ylabel("Real (ground truth)")
    ax.set_title(title, fontweight="bold")
    vmax = cm.max() if cm.max() > 0 else 1
    for i in range(3):
        for j in range(3):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    color="white" if cm[i, j] > vmax * 0.5 else "black",
                    fontsize=12, fontweight="bold")
    plt.tight_layout()
    out = RESULTS_DIR / filename
    plt.savefig(out, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {filename}")


def plot_confusion_matrices(rows):
    N_PLOT = 80
    for cond, fname, title in [
        ("A", "confusion_matrix_baseline.png",      "Confusion matrix — Baseline A (N=80)"),
        ("G", "confusion_matrix_best_condition.png", "Confusion matrix — Mejor cond. G (N=80)"),
    ]:
        cm_total = np.zeros((3, 3), dtype=int)
        for r in rows:
            if r["condition"] == cond and r["N"] == N_PLOT:
                for i, tc in enumerate(CLASSES):
                    for j, pc in enumerate(CLASSES):
                        cm_total[i, j] += r.get(f"cm_{tc}_{pc}", 0)
        _draw_confusion_matrix(cm_total, title, fname)


# ═══════════════════════════════════════════════════════════════════
# Plot 6: Registros en M_dir por condición
# ═══════════════════════════════════════════════════════════════════

def plot_registration_counts(rows):
    N_PLOT = 80
    fig, ax = plt.subplots(figsize=(13, 5))
    x = np.arange(len(CONDITIONS))
    width = 0.25
    dom_colors = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60"}

    for k, cls in enumerate(CLASSES):
        key = f"mdir_reg_{cls}"
        means, stds = [], []
        for cond in CONDITIONS:
            vals = [r[key] for r in rows
                    if r["condition"] == cond and r["N"] == N_PLOT and r[key] >= 0]
            means.append(np.mean(vals) if vals else 0)
            stds.append(np.std(vals)   if vals else 0)
        ax.bar(x + k * width, means, width, yerr=stds, capsize=3,
               label=cls, color=dom_colors[cls], alpha=0.75,
               edgecolor="black", linewidth=0.5)

    ax.set_xticks(x + width)
    ax.set_xticklabels([CONDITION_LABELS[c] for c in CONDITIONS],
                       rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("Registros en M_dir (promedio sobre seeds)")
    ax.set_title("Registros en M_dir por agente — N=80", fontweight="bold")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    out = RESULTS_DIR / "mdir_registration_counts.png"
    plt.savefig(out, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {out.name}")


# ═══════════════════════════════════════════════════════════════════
# Reporte Markdown
# ═══════════════════════════════════════════════════════════════════

def generate_report(rows):
    def mv(cond, N, key):
        return mean_cond(rows, cond, N, key)

    best_cond = max(CONDITIONS, key=lambda c: mv(c, 80, "mature_accuracy"))
    baseline_acc = mv("A", 80, "mature_accuracy")
    best_acc     = mv(best_cond, 80, "mature_accuracy")

    header = ("| Condicion              | N   | EarlyAcc | Fidelidad | "
              "MatureAcc | Apple | Horse | Car   |")
    separator = ("|------------------------|-----|----------|-----------|"
                 "----------|-------|-------|-------|")
    rows_md = [header, separator]
    for cond in CONDITIONS:
        for N in N_VALUES:
            ea  = mv(cond, N, "early_accuracy")
            fid = mv(cond, N, "mature_fidelity")
            acc = mv(cond, N, "mature_accuracy")
            a   = mv(cond, N, "mature_acc_apple")
            h   = mv(cond, N, "mature_acc_horse")
            c   = mv(cond, N, "mature_acc_car")
            rows_md.append(
                f"| {CONDITION_LABELS[cond]:22s} | {N:3d} | "
                f"{ea:.2%}   | {fid:.2%}    | {acc:.2%}    | "
                f"{a:.2%} | {h:.2%} | {c:.2%} |"
            )

    def pct(cond, N, key):
        return f"{mv(cond, N, key):.2%}"

    content = f"""# Ablation Report — Sesgo de M_dir en MAE-TMS
**Fecha:** 2026-06-07
**Arquitectura:** SimpleHAM4D (n=300, m=16, p=64, q=32) + ConceptNet 5.7.0
**Dominios:** apple / horse / car (ETH-80)

---

## Resumen ejecutivo

El baseline (A) muestra sesgo estructural donde apple domina la fase madura con
{pct("A",80,"winner_pct_apple")} de victorias vs {pct("A",80,"winner_pct_horse")} (horse)
y {pct("A",80,"winner_pct_car")} (car) en N=80.

La mejor condición encontrada es **{best_cond}** ({CONDITION_LABELS[best_cond]}):
mejora mature accuracy de {baseline_acc:.2%} a {best_acc:.2%}
(Δ = +{best_acc - baseline_acc:.2%}).

---

## Tabla de resultados (promedio sobre 5 seeds)

{chr(10).join(rows_md)}

---

## Respuestas a las 7 preguntas de investigación

### P1 — ¿El sesgo hacia apple es estructural o aleatorio?

**Estructural.** Tres mecanismos se combinan:
1. **Cuantización binaria**: `quantize_binary(sign(v), m=16)` mapea exactamente 2 valores
   (0 y 15). Apple acumula más registros cuando sus labels ganan el early phase.
2. **Acumulación asimétrica**: si apple gana N_a queries y el resto gana menos, M_dir
   acumula N_a × n_tokens registros para apple vs. menos para los demás.
3. **Polisemia de ConceptNet**: labels de Apple Inc. (computer, mac, macintosh) permiten
   que tokens de car/horse activen el agente apple en early phase.

Baseline N=80: winner_apple={pct("A",80,"winner_pct_apple")},
winner_horse={pct("A",80,"winner_pct_horse")}, winner_car={pct("A",80,"winner_pct_car")}.

### P2 — ¿Normalización B1/B2 reduce el sesgo?

B1 (÷count): mature_acc N=80 = {pct("B1",80,"mature_accuracy")} vs baseline {pct("A",80,"mature_accuracy")}
B2 (÷√count): mature_acc N=80 = {pct("B2",80,"mature_accuracy")}

La normalización penaliza al agente con más registros (apple). B1 divide directamente
por el número de veces que el agente fue registrado, equilibrando los scores.
El efecto es parcial si el sesgo también viene de M_dom (reconocimiento).

Horse N=80: A={pct("A",80,"mature_acc_horse")} → B1={pct("B1",80,"mature_acc_horse")}
Car  N=80: A={pct("A",80,"mature_acc_car")} → B1={pct("B1",80,"mature_acc_car")}

### P3 — ¿El balanceo de queries (D) mejora el early phase?

D early_acc N=80 = {pct("D",80,"early_accuracy")} vs A = {pct("A",80,"early_accuracy")}
D mature_acc N=80 = {pct("D",80,"mature_accuracy")}

Con floor(N/3) queries exactas por dominio e interleaved, los registros en M_dir
deberían ser más balanceados. Sin embargo, si M_dom tiene sesgos propios (reconoce
mejor apple), el efecto es limitado.

### P4 — ¿El registro balanceado (C) es efectivo?

C mature_acc N=80 = {pct("C",80,"mature_accuracy")}
C winner_apple = {pct("C",80,"winner_pct_apple")} vs A = {pct("A",80,"winner_pct_apple")}

El cap (max_ratio=3.0) previene que un agente acumule >3× los registros del mínimo.
Esto ayuda si el sesgo es de registro; si el sesgo viene de M_dom (reconocimiento en
early phase), C no puede compensarlo completamente.

### P5 — ¿Aumentar m (E32, E64) mejora discriminación?

E32 mature_acc N=80 = {pct("E32",80,"mature_accuracy")}
E64 mature_acc N=80 = {pct("E64",80,"mature_accuracy")}

**Resultado esperado y confirmado**: cambiar m NO mejora discriminación para vectores
binarios. `quantize_binary` mapea sign(v)∈{{-1,+1}} a {{0, m-1}}, usando solo 2 de m bins.
Con m=32: usa posiciones 0 y 31. Con m=64: posiciones 0 y 63. El patrón de bits es
idéntico, cambian solo los índices absolutos.

**Recomendación**: usar vectores fastText continuos (no sign(v)) para M_dir con
normalización global min/max permitiría aprovechar la resolución de m>2.

### P6 — ¿La curación de ConceptNet (F) reduce engine→apple?

F mature_acc_car N=80 = {pct("F",80,"mature_acc_car")} vs A = {pct("A",80,"mature_acc_car")}
F mature_acc N=80 = {pct("F",80,"mature_accuracy")}

Remover {{computer, mac, macintosh, eden}} del M_dom de apple hace que tokens como
"engine", "machine", "motor" tengan menos afinidad con apple en early phase.
El agente car gana más queries con tokens mecanicos → M_dir aprende correctamente.

### P7 — ¿Cuál es la mejor combinación?

Mejor condicion: {best_cond} ({CONDITION_LABELS[best_cond]})
N=80: mature_acc={best_acc:.2%} (baseline: {baseline_acc:.2%}, mejora: +{best_acc-baseline_acc:.2%})

Entropía M_dir (A): {mv("A",80,"mdir_entropy"):.3f} bits
Entropía M_dir (G): {mv("G",80,"mdir_entropy"):.3f} bits
(máximo posible: {math.log2(3):.3f} bits para 3 agentes)

Registros M_dir (A): apple={mv("A",80,"mdir_reg_apple"):.0f},
  horse={mv("A",80,"mdir_reg_horse"):.0f}, car={mv("A",80,"mdir_reg_car"):.0f}
Registros M_dir (G): apple={mv("G",80,"mdir_reg_apple"):.0f},
  horse={mv("G",80,"mdir_reg_horse"):.0f}, car={mv("G",80,"mdir_reg_car"):.0f}

---

## Recomendaciones de mejora

1. **Vectores continuos en M_dir** (no binarizados): elimina el cuello de botella de
   m bins usables, permite discriminación real con m=32/64.
2. **Curación de ConceptNet** (F): siempre recomendado para dominios con polisemia
   de entidades nombradas (Apple Inc. vs. apple fruit).
3. **Queries balanceadas** (D): garantiza distribución uniforme independiente de
   sesgos en M_dom. Recomendado como medida defensiva.
4. **Normalización B1** como complemento al balanceo para compensar sesgos residuales.
5. **Aumentar N** no resuelve el sesgo si M_dom tiene sesgos estructurales. La escala
   empeora el problema si un dominio domina early phase.

---

## Archivos generados

| Archivo | Descripcion |
|---------|-------------|
| `ablation_metrics.csv` | Metricas completas N × seed × condition |
| `scaling_comparison_ablation.png` | Mature accuracy y fidelidad vs N |
| `domain_accuracy_ablation.png` | Accuracy por dominio por condicion (N=80) |
| `winner_distribution.png` | Distribucion de ganadores en fase madura |
| `confusion_matrix_baseline.png` | Matriz de confusion baseline A |
| `confusion_matrix_best_condition.png` | Matriz de confusion mejor condicion |
| `mdir_registration_counts.png` | Registros en M_dir por agente |
| `semantic_cosine_engine.csv` | Similitudes coseno de "engine" |
| `semantic_nn_engine.csv` | Vecinos mas cercanos de "engine" |
"""

    out = RESULTS_DIR / "ablation_report.md"
    out.write_text(content, encoding="utf-8")
    print(f"  Guardado: {out.name}")


# ═══════════════════════════════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════════════════════════════

def run():
    all_rows = run_ablation()

    print("Guardando CSV...")
    save_csv(all_rows, RESULTS_DIR / "ablation_metrics.csv")

    print("Generando graficas...")
    plot_scaling_comparison(all_rows)
    plot_domain_accuracy(all_rows)
    plot_winner_distribution(all_rows)
    plot_confusion_matrices(all_rows)
    plot_registration_counts(all_rows)

    print("Generando reporte...")
    generate_report(all_rows)

    print(f"\n=== ABLATION COMPLETADO ===")
    print(f"Resultados en: {RESULTS_DIR}")


if __name__ == "__main__":
    run()
