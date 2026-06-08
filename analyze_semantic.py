"""
Análisis semántico en el espacio fastText original (300 dims).
Calcula similitudes coseno e identifica por qué ciertos tokens
activan dominios incorrectos (e.g. engine → apple).
Guarda: results/ablation_mdir_bias/semantic_cosine_engine.csv
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

RESULTS_DIR = ROOT / "results" / "ablation_mdir_bias"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

CLASSES = ["apple", "horse", "car"]

# Palabras de interés para el análisis (token sospechoso + vecindario)
FOCUS_WORDS = [
    "engine", "motor", "machine", "automobile", "vehicle",
    "transportation", "computer", "mac", "macintosh", "windows",
    "apple", "fruit", "red", "crash", "wheel",
]


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-10 or nb < 1e-10:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def load_all_label_vectors() -> dict:
    vecs = {}
    for cls in CLASSES:
        path = ROOT / f"label_vectors_{cls}.json"
        raw = json.loads(path.read_text())
        for w, v in raw.items():
            vecs[w] = np.array(v, dtype=np.float32)
    return vecs


def load_extra_vectors(words: list, known: dict) -> dict:
    needed = [w for w in words if w not in known]
    if not needed:
        return {}
    try:
        from stage4_fasttext import _stream_lookup
        return _stream_lookup(set(needed))
    except Exception as e:
        print(f"  Advertencia al cargar vectores extra: {e}")
        return {}


def get_domain_membership(vecs: dict) -> dict:
    """Retorna {word: list_of_domains}."""
    membership = {}
    for cls in CLASSES:
        path = ROOT / f"labels_{cls}.json"
        labels = json.loads(path.read_text())
        for w in labels:
            if w in vecs:
                membership.setdefault(w, []).append(cls)
    return membership


def nearest_neighbors(query_vec: np.ndarray, all_vecs: dict,
                      exclude: set = None, top_k: int = 10) -> list:
    exclude = exclude or set()
    sims = []
    for w, v in all_vecs.items():
        if w in exclude:
            continue
        sims.append((w, cosine(query_vec, v)))
    sims.sort(key=lambda x: -x[1])
    return sims[:top_k]


def run():
    print("Cargando vectores de labels...")
    label_vecs = load_all_label_vectors()
    print(f"  {len(label_vecs)} labels cargados")

    print("Cargando vectores extra...")
    extra_vecs = load_extra_vectors(FOCUS_WORDS, label_vecs)
    all_vecs = {**label_vecs, **extra_vecs}
    print(f"  {len(all_vecs)} vectores totales")

    membership = get_domain_membership(all_vecs)

    # ── 1. Tabla de similitudes coseno centrada en "engine" ──────────────────
    engine_vec = all_vecs.get("engine")
    if engine_vec is None:
        print("  AVISO: vector 'engine' no disponible")
        return

    print("\nSimilitudes coseno con 'engine':")
    print(f"  {'palabra':20s}  {'coseno':>8}  {'dominio'}")
    rows_cosine = []
    for word in FOCUS_WORDS:
        if word == "engine" or word not in all_vecs:
            continue
        sim = cosine(engine_vec, all_vecs[word])
        dom = ", ".join(membership.get(word, ["(extra)"]))
        print(f"  {word:20s}  {sim:8.4f}  {dom}")
        rows_cosine.append({
            "word": word,
            "cosine_with_engine": round(sim, 6),
            "domain": dom,
        })

    cosine_path = RESULTS_DIR / "semantic_cosine_engine.csv"
    with open(cosine_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["word", "cosine_with_engine", "domain"])
        writer.writeheader()
        writer.writerows(rows_cosine)
    print(f"\n  Guardado: {cosine_path.name}")

    # ── 2. Nearest neighbors de "engine" en el espacio de labels ────────────
    print("\nNearest neighbors de 'engine' (entre todos los labels):")
    nn = nearest_neighbors(engine_vec, all_vecs, exclude={"engine"}, top_k=15)
    nn_rows = []
    for rank, (w, sim) in enumerate(nn, 1):
        dom = ", ".join(membership.get(w, ["(extra)"]))
        print(f"  {rank:2d}. {w:20s}  sim={sim:.4f}  [{dom}]")
        nn_rows.append({
            "rank": rank, "word": w,
            "cosine": round(sim, 6),
            "domain": dom,
        })

    nn_path = RESULTS_DIR / "semantic_nn_engine.csv"
    with open(nn_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["rank", "word", "cosine", "domain"])
        writer.writeheader()
        writer.writerows(nn_rows)
    print(f"  Guardado: {nn_path.name}")

    # ── 3. Tabla de similitudes inter-dominio (centroide de cada dominio) ───
    print("\nSimilitudes de 'engine' con centroide de cada dominio:")
    for cls in CLASSES:
        path = ROOT / f"labels_{cls}.json"
        domain_labels = list(json.loads(path.read_text()).keys())
        domain_vecs = [all_vecs[w] for w in domain_labels if w in all_vecs]
        if not domain_vecs:
            continue
        centroid = np.mean(domain_vecs, axis=0)
        sim = cosine(engine_vec, centroid)
        print(f"  engine vs centroid({cls}): {sim:.4f}")

    # ── 4. Similitud cruzada entre dominios (Apple Inc. noise analysis) ──────
    noise_words = [w for w in ["computer", "mac", "macintosh"] if w in all_vecs]
    car_core_words = [w for w in ["vehicle", "automobile", "machine", "crash"] if w in all_vecs]

    if noise_words and car_core_words:
        print("\nSimilitud entre ruido Apple Inc. y labels de car:")
        cross_rows = []
        for nw in noise_words:
            for cw in car_core_words:
                sim = cosine(all_vecs[nw], all_vecs[cw])
                print(f"  cosine({nw:12s}, {cw:12s}) = {sim:.4f}")
                cross_rows.append({"word_apple_noise": nw, "word_car": cw,
                                   "cosine": round(sim, 6)})
        cross_path = RESULTS_DIR / "semantic_noise_vs_car.csv"
        with open(cross_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["word_apple_noise", "word_car", "cosine"])
            writer.writeheader()
            writer.writerows(cross_rows)
        print(f"  Guardado: {cross_path.name}")

    print("\nAnalisis semantico completado.")


if __name__ == "__main__":
    run()
