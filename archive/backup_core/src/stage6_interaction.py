"""
Etapa 6 — TME y M_dir.
Implementa el loop de interacción completo (fase temprana / topología estrella):
  query -> spaCy -> fastText -> broadcast -> argmax -> aprendizaje M_dir -> recall -> triple Wegner
"""
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import torch
from torchvision import transforms

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from mae_ham import SimpleHAM4D
from quantizer import quantize_binary, quantize, dequantize

CLASSES = ["apple", "horse", "car"]
AGENT_VECS = {
    "apple": np.array([1, 0, 0], dtype=np.int32),
    "horse": np.array([0, 1, 0], dtype=np.int32),
    "car":   np.array([0, 0, 1], dtype=np.int32),
}
AGENT_LIST = CLASSES
N, M_LABEL = 300, 16
MODELS_DIR = ROOT / "models"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ------------------------------------------------------------------
# NLP preprocessing
# ------------------------------------------------------------------

def get_nlp():
    import spacy
    return spacy.load("en_core_web_sm")


STOPWORD_POS = {"DET", "PUNCT", "SPACE", "AUX", "CCONJ", "SCONJ", "PART", "PRON"}


def tokenize_query(query: str, nlp) -> list:
    """spaCy tokenize + filter stopwords + POS filter -> list of lemmas."""
    doc = nlp(query.lower())
    tokens = []
    for tok in doc:
        if tok.is_stop:
            continue
        if tok.pos_ in STOPWORD_POS:
            continue
        if not tok.is_alpha:
            continue
        tokens.append(tok.lemma_)
    return list(set(tokens))   # deduplicate


# ------------------------------------------------------------------
# M_dir: AssociativeMemory (n=300 -> 3) using SimpleHAM4D degenerate case
# We use a simple 2D structure: n_label_features x n_agents
# ------------------------------------------------------------------

class SimpleDirectoryMemory:
    """
    Lightweight 2-D associative memory: maps v_label (n=300, m=16) -> v_agent (3).
    Stores frequency table rel[i, k, j] = count(v_label[i]==k ∧ agent==j).
    """
    def __init__(self, n: int = 300, m: int = 16, n_agents: int = 3):
        self._n = n
        self._m = m
        self._n_agents = n_agents
        # rel[feature_idx, quantized_value, agent_idx]
        self._rel = np.zeros((n, m, n_agents), dtype=np.int32)

    def register(self, v_label_q: np.ndarray, agent_idx: int):
        for i, k in enumerate(v_label_q):
            k = int(np.clip(k, 0, self._m - 1))
            self._rel[i, k, agent_idx] += 1

    def predict(self, v_label_q: np.ndarray) -> np.ndarray:
        """Return score vector over agents by summing votes."""
        scores = np.zeros(self._n_agents, dtype=float)
        for i, k in enumerate(v_label_q):
            k = int(np.clip(k, 0, self._m - 1))
            scores += self._rel[i, k, :]
        return scores

    def nearest_agent(self, v_label_q: np.ndarray) -> int:
        scores = self.predict(v_label_q)
        if scores.sum() == 0:
            return -1  # unknown
        return int(np.argmax(scores))


# ------------------------------------------------------------------
# Agent system
# ------------------------------------------------------------------

class Agent:
    def __init__(self, name: str, mem_dom: SimpleHAM4D):
        self.name = name
        self.mem_dom = mem_dom
        self.mem_dir = SimpleDirectoryMemory()

    def recognize(self, v_label_q: np.ndarray) -> float:
        """One-sided recognition from left (label) domain."""
        return self.mem_dom.recognize_from_left(v_label_q)

    def recall(self, v_label_q: np.ndarray):
        return self.mem_dom.recall_from_left(v_label_q)

    def learn_dir(self, v_label_q: np.ndarray, winner_idx: int):
        self.mem_dir.register(v_label_q, winner_idx)


class TME:
    def __init__(self):
        self.mem_dir = SimpleDirectoryMemory()

    def learn(self, v_label_q: np.ndarray, winner_idx: int):
        self.mem_dir.register(v_label_q, winner_idx)

    def route(self, v_label_q: np.ndarray) -> int:
        return self.mem_dir.nearest_agent(v_label_q)


# ------------------------------------------------------------------
# Full interaction loop
# ------------------------------------------------------------------

def get_fasttext_vector(word: str, vectors_cache: dict) -> np.ndarray:
    for cls in CLASSES:
        if word in vectors_cache[cls]:
            return np.array(vectors_cache[cls][word])
    # Fallback: live lookup from fasttext model
    try:
        from stage4_fasttext import get_vector
        return get_vector(word)
    except Exception:
        pass
    # Last resort: deterministic random
    rng = np.random.RandomState(hash(word) % (2**31))
    return rng.choice([-1.0, 1.0], 300).astype(np.float32)


def load_all_vectors() -> dict:
    cache = {}
    for cls in CLASSES:
        path = ROOT / f"label_vectors_{cls}.json"
        cache[cls] = json.loads(path.read_text())
    return cache


def process_query(query: str, agents: dict, tme: TME, nlp,
                  vectors_cache: dict, decoder, verbose: bool = True) -> dict:
    """
    Full early-phase interaction:
    a) tokenize -> b) fastText -> c) broadcast -> d) argmax -> e) learn dir -> f) recall
    Returns dict with wegner triple.
    """
    tokens = tokenize_query(query, nlp)
    if not tokens:
        return {"query": query, "tokens": [], "winner": None,
                "image": None, "labels": [], "agent": None}

    if verbose:
        print(f"  Query: '{query}'  tokens={tokens}")

    # --- Aggregate mean_weight per agent across all tokens ---
    agent_scores = {cls: 0.0 for cls in CLASSES}
    token_vectors = {}

    for tok in tokens:
        v = get_fasttext_vector(tok, vectors_cache)
        v_q = quantize_binary(v, M_LABEL)
        token_vectors[tok] = v_q

        for cls in CLASSES:
            w = agents[cls].recognize(v_q)
            agent_scores[cls] += w

    # Average over tokens
    n_toks = len(tokens)
    for cls in CLASSES:
        agent_scores[cls] /= n_toks

    # --- Argmax ---
    winner = max(agent_scores, key=agent_scores.get)
    winner_idx = AGENT_LIST.index(winner)

    if verbose:
        score_str = "  ".join(f"{c}={agent_scores[c]:.2f}" for c in CLASSES)
        print(f"  Scores: {score_str}  -> winner: {winner}")

    # --- Learning M_dir ---
    for tok, v_q in token_vectors.items():
        tme.learn(v_q, winner_idx)
        for agent in agents.values():
            agent.learn_dir(v_q, winner_idx)

    # --- Recall: use the first recognized token ---
    recalled_image = None
    recalled_labels = tokens
    # Load global latent stats for correct dequantization (q → actual latent range)
    _stats_path = MODELS_DIR / "latent_global_stats.json"
    _stats = json.loads(_stats_path.read_text())
    _g_min = np.array(_stats["global_min"])
    _g_max = np.array(_stats["global_max"])
    for tok, v_q in token_vectors.items():
        recalled_q, recognized, weight = agents[winner].recall(v_q)
        if recognized:
            v_norm = recalled_q.astype(float) / 31.0          # [0, 1]
            v_latent = (v_norm * (_g_max - _g_min) + _g_min).astype(np.float32)
            z = torch.tensor(v_latent).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                img = decoder(z)[0].cpu()
            recalled_image = img
            break

    return {
        "query": query,
        "tokens": tokens,
        "agent_scores": agent_scores,
        "winner": winner,
        "image": recalled_image,
        "labels": recalled_labels,
    }


def load_agents() -> dict:
    agents = {}
    for cls in CLASSES:
        path = MODELS_DIR / f"mem_dom_{cls}.pkl"
        with open(path, "rb") as f:
            mem = pickle.load(f)
        agents[cls] = Agent(cls, mem)
    return agents


def load_decoder():
    from stage2_encoder import Decoder, DEVICE
    decoder = Decoder().to(DEVICE)
    decoder.load_state_dict(torch.load(
        MODELS_DIR / "decoder.pt", map_location=DEVICE))
    decoder.eval()
    return decoder


def save_tme_and_agents(tme: TME, agents: dict):
    with open(MODELS_DIR / "tme.pkl", "wb") as f:
        pickle.dump(tme, f)
    for cls, agent in agents.items():
        with open(MODELS_DIR / f"agent_{cls}.pkl", "wb") as f:
            pickle.dump(agent, f)
    print("TME and agents saved.")


def load_tme_and_agents():
    import sys
    import stage6_interaction as _s6

    # When stage6 was run directly, pickle recorded __main__.TME.
    # Temporarily remap __main__ to stage6_interaction for unpickling.
    old_main = sys.modules.get('__main__')
    sys.modules['__main__'] = _s6

    try:
        with open(MODELS_DIR / "tme.pkl", "rb") as f:
            tme = pickle.load(f)
        agents = {}
        for cls in CLASSES:
            with open(MODELS_DIR / f"agent_{cls}.pkl", "rb") as f:
                agents[cls] = pickle.load(f)
    finally:
        if old_main is not None:
            sys.modules['__main__'] = old_main

    return tme, agents


def visualize_result(result: dict, idx: int):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    img = result.get("image")
    winner = result.get("winner", "?")
    query = result.get("query", "")
    if img is None:
        return
    fig, ax = plt.subplots(1, 1, figsize=(4, 4))
    ax.imshow(img.permute(1, 2, 0).numpy().clip(0, 1))
    ax.set_title(f"Q{idx}: '{query}'\nwinner={winner}", fontsize=7)
    ax.axis("off")
    plt.tight_layout()
    out = ROOT / f"stage6_query_{idx:02d}.png"
    plt.savefig(out, dpi=80)
    plt.close()


TEST_QUERIES = [
    "a round red fruit",
    "fast vehicle with wheels",
    "animal with a mane",
    "sweet edible thing",
    "large powerful mammal",
    "machine for transportation",
    "grows on trees",
    "has four legs and hooves",
    "has an engine",
    "fruit with seeds inside",
]


def run():
    print("Loading models and agents...")
    agents = load_agents()
    tme = TME()
    nlp = get_nlp()
    decoder = load_decoder()
    vectors_cache = load_all_vectors()

    results = []
    print("\n--- Early phase (TME active) ---")
    for i, query in enumerate(TEST_QUERIES):
        res = process_query(query, agents, tme, nlp, vectors_cache, decoder)
        results.append(res)
        visualize_result(res, i)
        print(f"  -> Triple: image={'yes' if res['image'] is not None else 'no'}, "
              f"labels={res['labels']}, location={res['winner']}")

    save_tme_and_agents(tme, agents)
    print("\nEtapa 6 COMPLETADA.")
    return tme, agents, results


if __name__ == "__main__":
    run()
