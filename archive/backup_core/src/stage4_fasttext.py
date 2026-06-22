"""
Etapa 4 — Vectorización de labels con fastText.
Stream-lee fasttext-wiki-news-subwords-300.gz para extraer solo
los ~36 words necesarios. Guarda label_vectors_{dominio}.json.
"""
import gzip
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent.parent
MODELS_DIR = ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)

CLASSES = ["apple", "horse", "car"]
DIM = 300

# Gensim downloads to ~/gensim-data/
GENSIM_MODEL_PATH = (
    Path.home() / "gensim-data"
    / "fasttext-wiki-news-subwords-300"
    / "fasttext-wiki-news-subwords-300.gz"
)

_cache: dict = {}   # word -> np.ndarray (binarized)


def _stream_lookup(needed_words: set) -> dict:
    """Stream through the gz vec file and collect only needed words."""
    found = {}
    missing = set(needed_words)

    if not GENSIM_MODEL_PATH.exists():
        print(f"  Model not found at {GENSIM_MODEL_PATH}")
        return found

    print(f"  Streaming fastText model for {len(missing)} words...")
    with gzip.open(GENSIM_MODEL_PATH, "rt", encoding="utf-8", errors="ignore") as f:
        header = f.readline().strip()
        # Header is either "vocab_size dim" or just the first vector
        parts = header.split()
        if len(parts) == 2 and parts[0].isdigit():
            pass  # true header line, skip it
        else:
            # No header — first line is a word vector; process it
            word = parts[0].lower()
            if word in missing and len(parts) == DIM + 1:
                v = np.array([float(x) for x in parts[1:]], dtype=np.float32)
                bv = np.sign(v)
                bv = np.where(bv == 0.0, 1.0, bv)
                found[word] = bv
                missing.discard(word)

        for line in f:
            if not missing:
                break
            parts = line.rstrip().split(" ")
            word = parts[0].lower()
            if word not in missing:
                continue
            if len(parts) != DIM + 1:
                continue
            v = np.array([float(x) for x in parts[1:]], dtype=np.float32)
            bv = np.sign(v)
            bv = np.where(bv == 0.0, 1.0, bv)
            found[word] = bv
            missing.discard(word)

    if missing:
        print(f"  {len(missing)} words not found, using deterministic fallback: {missing}")
        for w in missing:
            rng = np.random.RandomState(hash(w) % (2**31))
            found[w] = rng.choice([-1.0, 1.0], DIM).astype(np.float32)

    return found


def get_binary_vector(word: str) -> np.ndarray:
    """Return sign(fastText(word)) as float32 {-1.0, +1.0}^300."""
    word = word.lower()
    if word in _cache:
        return _cache[word]
    result = _stream_lookup({word})
    _cache.update(result)
    return result[word]


def get_vector(word: str) -> np.ndarray:
    return get_binary_vector(word)


def build_label_vectors(cls: str) -> dict:
    labels_path = ROOT / f"labels_{cls}.json"
    labels = json.loads(labels_path.read_text())
    needed = set(labels.keys()) | {cls}

    result = _stream_lookup(needed)
    _cache.update(result)

    vectors = {w: v.tolist() for w, v in result.items()}
    out_path = ROOT / f"label_vectors_{cls}.json"
    out_path.write_text(json.dumps(vectors))
    print(f"  {cls}: {len(vectors)} vectors saved -> {out_path.name}")
    return {w: np.array(v) for w, v in vectors.items()}


def run():
    # Collect all words across all domains at once for a single pass
    all_needed = set()
    for cls in CLASSES:
        labels_path = ROOT / f"labels_{cls}.json"
        labels = json.loads(labels_path.read_text())
        all_needed.update(labels.keys())
        all_needed.add(cls)

    print(f"Streaming fastText for {len(all_needed)} words: {sorted(all_needed)}")
    all_vecs = _stream_lookup(all_needed)

    for cls in CLASSES:
        labels_path = ROOT / f"labels_{cls}.json"
        labels = json.loads(labels_path.read_text())
        needed = set(labels.keys()) | {cls}
        vectors = {w: all_vecs[w].tolist() for w in needed if w in all_vecs}
        out_path = ROOT / f"label_vectors_{cls}.json"
        out_path.write_text(json.dumps(vectors))
        print(f"  {cls}: {len(vectors)} vectors saved -> {out_path.name}")

    print("\nEtapa 4 COMPLETADA.")


if __name__ == "__main__":
    run()
