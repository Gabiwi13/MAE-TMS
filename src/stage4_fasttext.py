"""
Etapa 4 — Vectorización de labels con fastText.
Stream-lee fasttext-wiki-news-subwords-300.gz para extraer solo
los ~36 words necesarios. Guarda label_vectors_{dominio}.json.
"""
import gzip
import hashlib
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


def _stream_lookup(needed_words: set, allow_fallback: bool = True) -> dict:
    """Stream through the gz vec file and collect only needed words.

    allow_fallback=True (build time): las palabras no halladas reciben un vector
    sintetico determinista, para que la construccion de label_vectors nunca
    falte un label. allow_fallback=False (protocolo oficial): las palabras no
    halladas simplemente se OMITEN del dict; el caller las trata como None
    (token no representable), de modo que el rechazo lo decida la EAM y no un
    vector inventado."""
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

    if missing and allow_fallback:
        print(f"  {len(missing)} words not found, using deterministic fallback: {missing}")
        for w in missing:
            # Digest estable: hash() esta salteado por PYTHONHASHSEED y haria
            # que el vector fallback cambiara entre procesos.
            seed = int(hashlib.md5(w.encode("utf-8")).hexdigest()[:8], 16)
            rng = np.random.RandomState(seed)
            found[w] = rng.choice([-1.0, 1.0], DIM).astype(np.float32)
    # Si allow_fallback=False, las palabras en `missing` se quedan fuera de
    # `found`: el caller las interpreta como no representables.

    return found


def get_binary_vector(word: str, allow_fallback: bool = True):
    """Return sign(fastText(word)) as float32 {-1.0, +1.0}^300, or None when
    the word is not in the fastText vocabulary and allow_fallback=False."""
    word = word.lower()
    if word in _cache:
        return _cache[word]
    result = _stream_lookup({word}, allow_fallback=allow_fallback)
    _cache.update(result)
    return result.get(word)


def get_vector(word: str, allow_fallback: bool = True):
    return get_binary_vector(word, allow_fallback=allow_fallback)


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
