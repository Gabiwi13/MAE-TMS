"""
Ablation study — diagnóstico del sesgo de M_dir hacia apple.

Directorio: el DirectoryMemory hetero OFICIAL (associative_memory), el mismo que
usa el sistema en produccion. La version previa usaba SlotDirectoryMemory (una
HomoAssociativeMemory por agente), archivada en archive/legacy_slot_directory/;
sus numeros no representaban la arquitectura final y no deben citarse como tales.

Condiciones:
  A   — Baseline: lectura cruda del directorio (predict, sin normalizar)
  B1  — Score normalizado / count_agente  (penaliza sobrerepresentados)
  B2  — Score normalizado / sqrt(count_agente)
  C   — Registro balanceado: cap proporcional de registros por agente
  D   — Queries estrictamente balanceadas por dominio (N//K por clase, K=8)
  E32 — M_dir con m=32  [HISTÓRICO: nació para probar m>2 con sign(v); con la
        cuantización por MAGNITUD vigente ya no mide lo mismo]
  E64 — M_dir con m=64  [HISTÓRICO, ídem]
  F   — ConceptNet curado: apple sin computer/mac/macintosh/eden  [NO-OP en v4:
        esos labels ya no están en labels_apple.json → F ≡ A]
  G   — Mejor combinación: D + B1 + F  (con F no-op, G ≡ D + B1)

N ∈ [50,100,200,400]  ×  seeds ∈ [0,1,2,3,4]  →  CSV → gráficas → reporte Markdown
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

from hetero_memory import HeteroAssociativeMemory
from associative_memory import DirectoryMemory
from quantizer import quantize_binary
from eval_bank import ALL_QUERIES, GROUND_TRUTH, DOMAIN_QUERIES
from stage6_interaction import (
    Agent, TME, CLASSES, AGENT_LIST, MODELS_DIR,
    get_nlp, load_all_vectors, prevectorize,
    tokenize_query, get_fasttext_vector, M_LABEL,
)




class DirectoryMemoryCapped(DirectoryMemory):
    """Condicion C: DirectoryMemory hetero que limita la acumulacion
    desproporcionada por agente (cap proporcional por max_ratio)."""

    def __init__(self, n=300, m=16, n_agents=None, max_ratio=3.0):
        # n_agents obligatorio (lo valida DirectoryMemory).
        super().__init__(n=n, m=m, n_agents=n_agents)
        self._max_ratio = max_ratio

    def register(self, v_q: np.ndarray, agent_idx: int) -> None:
        min_c = self._counts.min()
        if min_c > 0 and self._counts[agent_idx] > min_c * self._max_ratio:
            return  # Skip: agente demasiado dominante
        super().register(v_q, agent_idx)


# Configuración global

# Banco de 411 consultas (8 clases): N escala respecto al banco original de 80.
N_VALUES   = [50, 100, 200, 400]
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

# Paleta por dominio (8 clases ETH-80) para los plots diagnósticos.
DOMAIN_COLOR = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60",
                "cow": "#8e44ad", "cup": "#f39c12", "dog": "#16a085",
                "pear": "#7f8c8d", "tomato": "#c0392b"}
# N de referencia para los plots por dominio: el banco completo (debe estar
# en N_VALUES). Antes era 80 —de la era de 3 clases y AUSENTE de N_VALUES—,
# así que los plots agregaban 0 filas.
N_PLOT = N_VALUES[-1]
CHANCE = 1.0 / len(CLASSES)

# El banco de 80 consultas (APPLE/HORSE/CAR_QUERIES, DOMAIN_QUERIES,
# ALL_QUERIES, GROUND_TRUTH) vive en src/eval_bank.py y se importa arriba:
# modulo neutral para que los experimentos oficiales no dependan de este script.


# Carga de M_dom

def load_base_mdoms() -> dict:
    mdoms = {}
    for cls in CLASSES:
        with open(MODELS_DIR / f"mem_dom_{cls}.pkl", "rb") as f:
            mdoms[cls] = pickle.load(f)
    return mdoms


def build_curated_apple_mdom() -> HeteroAssociativeMemory:
    """Reconstruye M_dom de apple sin labels de Apple Inc., con el mismo
    protocolo de llenado por instancias de stage5 (los latentes del pool
    se reusan desde instance_latents_apple.json)."""
    from stage5_fill import quantize_latent_global
    N_F, M_F, P_F, Q_F = 300, 16, 64, 32
    NOISE = {"computer", "mac", "macintosh", "eden"}

    labels   = json.loads((ROOT / "labels_apple.json").read_text())
    raw_vecs = json.loads((ROOT / "label_vectors_apple.json").read_text())
    latents  = json.loads(
        (MODELS_DIR / "instance_latents_apple.json").read_text())
    stats    = json.loads((MODELS_DIR / "latent_global_stats.json").read_text())
    g_min    = np.array(stats["global_min"])
    g_max    = np.array(stats["global_max"])

    curated = {l: w for l, w in labels.items() if l not in NOISE}
    removed = NOISE & set(labels)
    print(f"  Curated apple: {len(labels)} -> {len(curated)} labels "
          f"(removed: {removed})")
    if not removed:
        # El vocabulario v4 (masa asociativa) ya no contiene los labels de
        # Apple Inc.: las condiciones F/G quedan como NO-OP (F ≡ A). Se avisa
        # en vez de narrar en el reporte un efecto que no ocurre.
        print("  AVISO: la curación F/G no removió NADA (los labels de Apple "
              "Inc. ya no están en labels_apple.json). F ≡ A en esta corrida.")

    label_seq = []
    for word, freq in curated.items():
        if word not in raw_vecs:
            continue
        v_lq = quantize_binary(np.array(raw_vecs[word], dtype=np.float32), M_F)
        label_seq.extend([v_lq] * int(freq))

    mem = HeteroAssociativeMemory(N_F, M_F, P_F, Q_F)
    L = len(label_seq)
    for i, z in enumerate(latents):
        z_q = quantize_latent_global(np.array(z), g_min, g_max, Q_F)
        mem.register(label_seq[i % L], z_q)
    return mem


# Configuración por condición

def get_condition_config(condition: str):
    """Retorna (mdir_class, m_mdir, mdir_kwargs, predict_fn, use_curated, use_balanced)."""
    use_curated  = condition in ("F", "G")
    use_balanced = condition in ("D", "G")

    if condition == "B1":
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemory, 16, {}
        predict_fn = lambda ag, vq: ag.mem_dir.predict_normalized(vq, "linear")
    elif condition == "B2":
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemory, 16, {}
        predict_fn = lambda ag, vq: ag.mem_dir.predict_normalized(vq, "sqrt")
    elif condition == "C":
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemoryCapped, 16, {"max_ratio": 3.0}
        predict_fn = lambda ag, vq: ag.mem_dir.predict(vq)
    elif condition == "E32":
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemory, 32, {}
        predict_fn = lambda ag, vq: ag.mem_dir.predict(vq)
    elif condition == "E64":
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemory, 64, {}
        predict_fn = lambda ag, vq: ag.mem_dir.predict(vq)
    elif condition == "G":
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemory, 16, {}
        predict_fn = lambda ag, vq: ag.mem_dir.predict_normalized(vq, "linear")
    else:  # A, D, F
        mdir_class, m_mdir, mdir_kwargs = DirectoryMemory, 16, {}
        predict_fn = lambda ag, vq: ag.mem_dir.predict(vq)

    return mdir_class, m_mdir, mdir_kwargs, predict_fn, use_curated, use_balanced


# Factory de agentes

# Memoizaciones de rendimiento (resultados idénticos):
#   _LR_CACHE     evita re-deserializar L/R (y la H de ~160MB que
#                 load_agent_memories arrastra) en cada uno de los experimentos.
#                 L/R solo se LEEN durante la ablación (los registros van al
#                 mem_dir fresco de cada experimento), así que compartirlas es seguro.
#   _SCORE_CACHE  recognize_gated(token) es determinista dado (M_dom_H, M_dom_L);
#                 las mdoms se construyen UNA vez (base y curada) y se reusan, así
#                 que (id(mem_dom_H), token) identifica el score entre experimentos.
_LR_CACHE = {}
_SCORE_CACHE = {}


def _load_LR(cls: str):
    if cls not in _LR_CACHE:
        with open(MODELS_DIR / f"mem_dom_L_{cls}.pkl", "rb") as f:
            mem_L = pickle.load(f)
        with open(MODELS_DIR / f"mem_dom_R_{cls}.pkl", "rb") as f:
            mem_R = pickle.load(f)
        _LR_CACHE[cls] = (mem_L, mem_R)
    return _LR_CACHE[cls]


def _gated_score_cached(agent, tok: str, vq_mdom) -> float:
    key = (id(agent.mem_dom_H), tok)
    if key not in _SCORE_CACHE:
        _SCORE_CACHE[key] = agent.recognize_gated(vq_mdom)
    return _SCORE_CACHE[key]


def make_agents(mdoms: dict, mdir_class, m_mdir: int = 16,
                mdir_kwargs: dict = None):
    """Create fresh Agent+TME set for one ablation experiment.

    mdoms[cls] is the H memory (may be curated for conditions F/G).
    M_dom_L/R are loaded from disk (non-curated) for weighted recognition.
    """
    mdir_kwargs = mdir_kwargs or {}
    agents = {}
    for cls in CLASSES:
        # L/R para el reconocimiento ponderado (H llega vía mdoms)
        mem_L, mem_R = _load_LR(cls)
        ag = Agent(cls, mdoms[cls], mem_dom_L=mem_L, mem_dom_R=mem_R)
        # Override the default mem_dir with the ablation-specific class.
        # n_agents explícito: el default de DirectoryMemory es 3 y el sistema
        # ahora tiene len(CLASSES) agentes.
        ag.mem_dir = mdir_class(m=m_mdir, n_agents=len(CLASSES), **mdir_kwargs)
        agents[cls] = ag
    tme = TME()
    # mem_dir is a read-only property alias; set mem_dir_L directly
    tme.mem_dir_L = mdir_class(m=m_mdir, n_agents=len(CLASSES), **mdir_kwargs)
    return agents, tme


# Selección de queries

def balanced_queries(N: int, seed: int):
    """Condición D: floor(N/K) queries por dominio, shuffled, interleaved."""
    rng = np.random.RandomState(seed)
    n_per = N // len(CLASSES)
    pools = []
    for cls in CLASSES:
        pool = DOMAIN_QUERIES[cls][:]
        rng.shuffle(pool)
        pools.append(pool[:n_per])

    interleaved_q, interleaved_gt = [], []
    for i in range(n_per):
        for j, cls in enumerate(CLASSES):
            # Tolerar pools desiguales: una clase puede tener menos consultas
            # que n_per (p.ej. dog tiene 49 y N=400//8 pide 50).
            if i < len(pools[j]):
                interleaved_q.append(pools[j][i])
                interleaved_gt.append(cls)

    return interleaved_q, interleaved_gt


def standard_queries(N: int):
    return ALL_QUERIES[:N], GROUND_TRUTH[:N]


# Fase temprana

def run_early_phase(queries, agents, tme, nlp, vectors_cache, m_mdir):
    """Sin tokens o sin señal, la consulta se rechaza ("REJ"): defaultear
    a un agente fijo inflaria artificialmente sus metricas."""
    winners = []
    for q in queries:
        tokens = tokenize_query(q, nlp)
        if not tokens:
            winners.append("REJ")
            continue

        agent_scores = {cls: 0.0 for cls in CLASSES}
        tok_vecs_mdir = {}

        # Sin filtro léxico ni fallback sintético: cada token con vector
        # fastText real entra como pista y el scoring oficial es recognize_gated
        # (gate de containment). Los no representables se descartan.
        for tok in tokens:
            v = get_fasttext_vector(tok, vectors_cache, allow_fallback=False)
            if v is None:
                continue
            v = np.asarray(v, dtype=np.float32)
            vq_mdom = quantize_binary(v, M_LABEL)             # m=16 para M_dom
            tok_vecs_mdir[tok] = quantize_binary(v, m_mdir)   # variable para M_dir
            for cls in CLASSES:
                agent_scores[cls] += _gated_score_cached(agents[cls], tok, vq_mdom)

        if not tok_vecs_mdir:
            winners.append("REJ")   # no_representable_tokens
            continue
        for cls in CLASSES:
            agent_scores[cls] /= len(tok_vecs_mdir)

        if max(agent_scores.values()) == 0.0:
            winners.append("REJ")   # mae_no_support
            continue

        winner = max(agent_scores, key=agent_scores.get)
        winner_idx = AGENT_LIST.index(winner)
        winners.append(winner)

        for tok, vq in tok_vecs_mdir.items():
            tme.mem_dir_L.register(vq, winner_idx)
            for ag in agents.values():
                ag.mem_dir.register(vq, winner_idx)

    return winners


# Fase madura

def run_mature_phase(queries, agents, nlp, vectors_cache, rng, predict_fn, m_mdir):
    """Routing punto a punto por el directorio del agente de entrada.
    Sin tokens o sin señal, rechaza ("REJ")."""
    winners = []
    for q in queries:
        entry_cls = CLASSES[rng.randint(0, len(CLASSES))]
        entry_ag  = agents[entry_cls]

        tokens = tokenize_query(q, nlp)
        if not tokens:
            winners.append("REJ")
            continue

        scores = np.zeros(len(CLASSES))
        used = 0
        for tok in tokens:
            v = get_fasttext_vector(tok, vectors_cache, allow_fallback=False)
            if v is None:
                continue
            used += 1
            vq = quantize_binary(np.asarray(v, dtype=np.float32), m_mdir)
            scores += predict_fn(entry_ag, vq)

        winners.append(CLASSES[int(np.argmax(scores))]
                       if used > 0 and scores.sum() > 0 else "REJ")

    return winners


# Métricas

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

    cm = np.zeros((len(CLASSES), len(CLASSES)), dtype=int)
    for g, m in zip(ground_truth, mature_winners):
        if m in CLASSES:
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
        "mdir_entropy":     round(m["mdir_entropy"], 4),
    }
    # Columnas por dominio para TODAS las clases (antes hardcodeadas a 3).
    for cls in CLASSES:
        row[f"early_acc_{cls}"]  = round(m["domain_early"][cls], 4)
        row[f"fidelity_{cls}"]   = round(m["domain_fid"][cls],   4)
        row[f"mature_acc_{cls}"] = round(m["domain_mat"][cls],   4)
        row[f"winner_pct_{cls}"] = round(m["winner_dist"][cls],  4)
        row[f"mdir_reg_{cls}"]   = m["reg_counts"][cls]
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


# Experimento único

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


# Loop principal

def run_ablation():
    print("=== ABLATION STUDY: M_dir bias ===\n")
    print("Cargando NLP + vectores...")
    nlp = get_nlp()
    vectors_cache = load_all_vectors(nlp)   # alias por lema (spaCy core)
    # Pre-vectorizar todos los tokens del banco en una pasada (fastText real,
    # sin fallback sintético): el rechazo lo decide la EAM, no el léxico.
    _bank_tokens = set()
    for _q in ALL_QUERIES:
        _bank_tokens.update(tokenize_query(_q, nlp))
    prevectorize(vectors_cache, _bank_tokens, allow_fallback=False)

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


# Funciones auxiliares para plots

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


# Plot 1: Scaling comparison

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
        ax.axhline(CHANCE, color="gray", lw=0.8, ls=":",
                   label=f"chance ({CHANCE*100:.1f}%)")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=7, ncol=2, loc="lower right")

    plt.suptitle("Ablation Study — EAM-TMS: comparacion de condiciones",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    out = RESULTS_DIR / "scaling_comparison_ablation.png"
    plt.savefig(out, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {out.name}")


# Plot 2: Domain accuracy por condición (N=N_PLOT)

def plot_domain_accuracy(rows):
    ncol = 4
    nrow = int(np.ceil(len(CLASSES) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(5 * ncol, 4.2 * nrow))
    axes = np.atleast_1d(axes).ravel()
    x = np.arange(len(CONDITIONS))
    width = 0.6

    for ax, cls in zip(axes, CLASSES):
        key = f"mature_acc_{cls}"
        means = [mean_cond(rows, c, N_PLOT, key) for c in CONDITIONS]
        stds  = [std_cond(rows, c, N_PLOT, key)  for c in CONDITIONS]
        ax.bar(x, means, width, yerr=stds, capsize=4,
               color=DOMAIN_COLOR[cls], alpha=0.75,
               edgecolor="black", linewidth=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels([CONDITION_LABELS[c] for c in CONDITIONS],
                           rotation=35, ha="right", fontsize=7.5)
        ax.set_ylabel("Mature accuracy")
        ax.set_title(f"Dominio: {cls}  (N={N_PLOT})", fontweight="bold")
        ax.set_ylim(0, 1.05)
        ax.axhline(CHANCE, color="gray", ls=":", lw=1,
                   label=f"chance ({CHANCE*100:.0f}%)")
        ax.grid(axis="y", alpha=0.3)
        ax.legend(fontsize=7)
    for ax in axes[len(CLASSES):]:      # apagar ejes sobrantes de la grilla
        ax.axis("off")

    plt.suptitle(f"Accuracy por dominio en fase madura — N={N_PLOT}",
                 fontsize=12, fontweight="bold")
    plt.tight_layout()
    out = RESULTS_DIR / "domain_accuracy_ablation.png"
    plt.savefig(out, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {out.name}")


# Plot 3: Distribución de ganadores (fase madura, N=N_PLOT)

def plot_winner_distribution(rows):
    dom_colors = [DOMAIN_COLOR[c] for c in CLASSES]
    n_cond = len(CONDITIONS)
    fig, axes = plt.subplots(1, n_cond, figsize=(2.4 * n_cond, 5))

    for ax, cond in zip(axes, CONDITIONS):
        means = [mean_cond(rows, cond, N_PLOT, f"winner_pct_{cls}")
                 for cls in CLASSES]
        stds  = [std_cond(rows, cond, N_PLOT, f"winner_pct_{cls}")
                 for cls in CLASSES]
        ax.bar(CLASSES, means, color=dom_colors, alpha=0.8,
               edgecolor="black", linewidth=0.5)
        ax.errorbar(range(len(CLASSES)), means, yerr=stds, fmt="none",
                    ecolor="black", capsize=4, linewidth=1.2)
        ax.set_title(CONDITION_LABELS[cond].replace(" ", "\n", 1),
                     fontsize=8, fontweight="bold")
        ax.set_ylim(0, 1.05)
        ax.axhline(CHANCE, color="gray", ls=":", lw=1)
        ax.set_xticks(range(len(CLASSES)))
        ax.set_xticklabels(CLASSES, fontsize=7, rotation=45, ha="right")
        if cond == CONDITIONS[0]:
            ax.set_ylabel("% victorias fase madura")
        ax.grid(axis="y", alpha=0.3)

    plt.suptitle(f"Distribucion de ganadores en fase madura (N={N_PLOT}) "
                 "— sesgo de M_dir", fontsize=11, fontweight="bold")
    plt.tight_layout()
    out = RESULTS_DIR / "winner_distribution.png"
    plt.savefig(out, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {out.name}")


# Plots 4 y 5: Matrices de confusión

def _draw_confusion_matrix(cm: np.ndarray, title: str, filename: str):
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.colorbar(im, ax=ax)
    k = len(CLASSES)
    ax.set_xticks(range(k)); ax.set_yticks(range(k))
    ax.set_xticklabels(CLASSES, fontsize=10, rotation=45, ha="right")
    ax.set_yticklabels(CLASSES, fontsize=10)
    ax.set_xlabel("Predicho (fase madura)")
    ax.set_ylabel("Real (ground truth)")
    ax.set_title(title, fontweight="bold")
    vmax = cm.max() if cm.max() > 0 else 1
    for i in range(k):
        for j in range(k):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    color="white" if cm[i, j] > vmax * 0.5 else "black",
                    fontsize=9, fontweight="bold")
    plt.tight_layout()
    out = RESULTS_DIR / filename
    plt.savefig(out, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {filename}")


def plot_confusion_matrices(rows):
    for cond, fname, title in [
        ("A", "confusion_matrix_baseline.png",
         f"Confusion matrix — Baseline A (N={N_PLOT})"),
        ("G", "confusion_matrix_best_condition.png",
         f"Confusion matrix — Mejor cond. G (N={N_PLOT})"),
    ]:
        cm_total = np.zeros((len(CLASSES), len(CLASSES)), dtype=int)
        for r in rows:
            if r["condition"] == cond and r["N"] == N_PLOT:
                for i, tc in enumerate(CLASSES):
                    for j, pc in enumerate(CLASSES):
                        cm_total[i, j] += r.get(f"cm_{tc}_{pc}", 0)
        _draw_confusion_matrix(cm_total, title, fname)


# Plot 6: Registros en M_dir por condición

def plot_registration_counts(rows):
    fig, ax = plt.subplots(figsize=(15, 5))
    x = np.arange(len(CONDITIONS))
    width = 0.10                       # 8 barras por condición

    for k, cls in enumerate(CLASSES):
        key = f"mdir_reg_{cls}"
        means, stds = [], []
        for cond in CONDITIONS:
            vals = [r[key] for r in rows
                    if r["condition"] == cond and r["N"] == N_PLOT and r[key] >= 0]
            means.append(np.mean(vals) if vals else 0)
            stds.append(np.std(vals)   if vals else 0)
        ax.bar(x + k * width, means, width, yerr=stds, capsize=3,
               label=cls, color=DOMAIN_COLOR[cls], alpha=0.75,
               edgecolor="black", linewidth=0.5)

    ax.set_xticks(x + width * (len(CLASSES) - 1) / 2)
    ax.set_xticklabels([CONDITION_LABELS[c] for c in CONDITIONS],
                       rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("Registros en M_dir (promedio sobre seeds)")
    ax.set_title(f"Registros en M_dir por agente — N={N_PLOT}",
                 fontweight="bold")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    out = RESULTS_DIR / "mdir_registration_counts.png"
    plt.savefig(out, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {out.name}")


# Reporte Markdown

def generate_report(rows):
    def mv(cond, N, key):
        return mean_cond(rows, cond, N, key)

    best_cond = max(CONDITIONS, key=lambda c: mv(c, N_PLOT, "mature_accuracy"))
    baseline_acc = mv("A", N_PLOT, "mature_accuracy")
    best_acc     = mv(best_cond, N_PLOT, "mature_accuracy")

    header = ("| Condicion              | N   | EarlyAcc | Fidelidad | "
              "MatureAcc |")
    separator = ("|------------------------|-----|----------|-----------|"
                 "----------|")
    rows_md = [header, separator]
    for cond in CONDITIONS:
        for N in N_VALUES:
            ea  = mv(cond, N, "early_accuracy")
            fid = mv(cond, N, "mature_fidelity")
            acc = mv(cond, N, "mature_accuracy")
            rows_md.append(
                f"| {CONDITION_LABELS[cond]:22s} | {N:3d} | "
                f"{ea:.2%}   | {fid:.2%}    | {acc:.2%}    |"
            )

    def pct(cond, N, key):
        return f"{mv(cond, N, key):.2%}"

    content = f"""# Ablation Report — Sesgo de M_dir en EAM-TMS
**Arquitectura:** HeteroAssociativeMemory (n=300, m=16, p=64, q=32) + ConceptNet 5.7.0
**Dominios:** {" / ".join(CLASSES)} (ETH-80, {len(CLASSES)} clases)

> **Nota:** los NÚMEROS de este reporte salen de la corrida actual de 8 clases
> (N={N_PLOT}, 5 seeds). La NARRATIVA cualitativa de P1–P7 abajo es el
> diagnóstico histórico de la era v2 (3 clases, cuantización `sign(v)`,
> polisemia de Apple Inc.); la cuantización actual es por MAGNITUD y el
> análisis vigente vive en el paper (.tex) y en generate_paper_figures.py.

---

## Resumen ejecutivo

El baseline (A) muestra sesgo estructural donde apple domina la fase madura con
{pct("A", N_PLOT,"winner_pct_apple")} de victorias vs {pct("A", N_PLOT,"winner_pct_horse")} (horse)
y {pct("A", N_PLOT,"winner_pct_car")} (car) en N={N_PLOT}.

La mejor condición encontrada es **{best_cond}** ({CONDITION_LABELS[best_cond]}):
mejora mature accuracy de {baseline_acc:.2%} a {best_acc:.2%}
(Δ = +{best_acc - baseline_acc:.2%}).

---

## Tabla de resultados (promedio sobre 5 seeds)

{chr(10).join(rows_md)}

---

## Respuestas a las 7 preguntas de investigación

> **[HISTÓRICO v2/3-clases]** P1–P7 describen el diagnóstico de la era de
> `sign(v)` + Apple Inc.; NO aplican a la cuantización por magnitud vigente
> (ver disclaimer arriba). Los NÚMEROS de la tabla sí son de la corrida actual.

### P1 — ¿El sesgo hacia apple es estructural o aleatorio?

**[HISTÓRICO]** **Estructural.** Tres mecanismos se combinan:
1. **Cuantización binaria** *(ya no vigente: hoy es por magnitud)*:
   `quantize_binary(sign(v), m=16)` mapeaba exactamente 2 valores
   (0 y 15). Apple acumula más registros cuando sus labels ganan el early phase.
2. **Acumulación asimétrica**: si apple gana N_a queries y el resto gana menos, M_dir
   acumula N_a × n_tokens registros para apple vs. menos para los demás.
3. **Polisemia de ConceptNet**: labels de Apple Inc. (computer, mac, macintosh) permiten
   que tokens de car/horse activen el agente apple en early phase.

Baseline N={N_PLOT}: winner_apple={pct("A", N_PLOT,"winner_pct_apple")},
winner_horse={pct("A", N_PLOT,"winner_pct_horse")}, winner_car={pct("A", N_PLOT,"winner_pct_car")}.

### P2 — ¿Normalización B1/B2 reduce el sesgo?

B1 (÷count): mature_acc N={N_PLOT} = {pct("B1", N_PLOT,"mature_accuracy")} vs baseline {pct("A", N_PLOT,"mature_accuracy")}
B2 (÷√count): mature_acc N={N_PLOT} = {pct("B2", N_PLOT,"mature_accuracy")}

La normalización penaliza al agente con más registros (apple). B1 divide directamente
por el número de veces que el agente fue registrado, equilibrando los scores.
El efecto es parcial si el sesgo también viene de M_dom (reconocimiento).

Horse N={N_PLOT}: A={pct("A", N_PLOT,"mature_acc_horse")} → B1={pct("B1", N_PLOT,"mature_acc_horse")}
Car  N={N_PLOT}: A={pct("A", N_PLOT,"mature_acc_car")} → B1={pct("B1", N_PLOT,"mature_acc_car")}

### P3 — ¿El balanceo de queries (D) mejora el early phase?

D early_acc N={N_PLOT} = {pct("D", N_PLOT,"early_accuracy")} vs A = {pct("A", N_PLOT,"early_accuracy")}
D mature_acc N={N_PLOT} = {pct("D", N_PLOT,"mature_accuracy")}

Con floor(N/3) queries exactas por dominio e interleaved, los registros en M_dir
deberían ser más balanceados. Sin embargo, si M_dom tiene sesgos propios (reconoce
mejor apple), el efecto es limitado.

### P4 — ¿El registro balanceado (C) es efectivo?

C mature_acc N={N_PLOT} = {pct("C", N_PLOT,"mature_accuracy")}
C winner_apple = {pct("C", N_PLOT,"winner_pct_apple")} vs A = {pct("A", N_PLOT,"winner_pct_apple")}

El cap (max_ratio=3.0) previene que un agente acumule >3× los registros del mínimo.
Esto ayuda si el sesgo es de registro; si el sesgo viene de M_dom (reconocimiento en
early phase), C no puede compensarlo completamente.

### P5 — ¿Aumentar m (E32, E64) mejora discriminación?

E32 mature_acc N={N_PLOT} = {pct("E32", N_PLOT,"mature_accuracy")}
E64 mature_acc N={N_PLOT} = {pct("E64", N_PLOT,"mature_accuracy")}

**[HISTÓRICO — sign(v), ya no vigente]** Cuando la cuantización era binaria,
cambiar m NO mejoraba discriminación: `quantize_binary` mapeaba sign(v)∈{{-1,+1}}
a {{0, m-1}}, usando solo 2 de m bins. HOY la cuantización es por MAGNITUD y usa
todos los m niveles, así que E32/E64 ya no prueban lo que su nombre sugiere;
la recomendación de "usar vectores continuos" YA se aplicó (fastText crudo).

### P6 — ¿La curación de ConceptNet (F) reduce engine→apple?

**[NO-OP en v4]** Los labels de Apple Inc. (computer/mac/macintosh/eden) ya no
están en labels_apple.json (vocabulario por masa asociativa), así que F no
remueve nada y F ≡ A; los números F/A abajo deben coincidir.

F mature_acc_car N={N_PLOT} = {pct("F", N_PLOT,"mature_acc_car")} vs A = {pct("A", N_PLOT,"mature_acc_car")}
F mature_acc N={N_PLOT} = {pct("F", N_PLOT,"mature_accuracy")}

Remover {{computer, mac, macintosh, eden}} del M_dom de apple hace que tokens como
"engine", "machine", "motor" tengan menos afinidad con apple en early phase.
El agente car gana más queries con tokens mecanicos → M_dir aprende correctamente.

### P7 — ¿Cuál es la mejor combinación?

Mejor condicion: {best_cond} ({CONDITION_LABELS[best_cond]})
N={N_PLOT}: mature_acc={best_acc:.2%} (baseline: {baseline_acc:.2%}, mejora: +{best_acc-baseline_acc:.2%})

Entropía M_dir (A): {mv("A", N_PLOT,"mdir_entropy"):.3f} bits
Entropía M_dir (G): {mv("G", N_PLOT,"mdir_entropy"):.3f} bits
(máximo posible: {math.log2(len(CLASSES)):.3f} bits para {len(CLASSES)} agentes)

Registros M_dir (A): apple={mv("A", N_PLOT,"mdir_reg_apple"):.0f},
  horse={mv("A", N_PLOT,"mdir_reg_horse"):.0f}, car={mv("A", N_PLOT,"mdir_reg_car"):.0f}
Registros M_dir (G): apple={mv("G", N_PLOT,"mdir_reg_apple"):.0f},
  horse={mv("G", N_PLOT,"mdir_reg_horse"):.0f}, car={mv("G", N_PLOT,"mdir_reg_car"):.0f}

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
| `domain_accuracy_ablation.png` | Accuracy por dominio por condicion (N={N_PLOT}) |
| `winner_distribution.png` | Distribucion de ganadores en fase madura |
| `confusion_matrix_baseline.png` | Matriz de confusion baseline A |
| `confusion_matrix_best_condition.png` | Matriz de confusion mejor condicion |
| `mdir_registration_counts.png` | Registros en M_dir por agente |
"""

    out = RESULTS_DIR / "ablation_report.md"
    out.write_text(content, encoding="utf-8")
    print(f"  Guardado: {out.name}")


# Entry point

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
