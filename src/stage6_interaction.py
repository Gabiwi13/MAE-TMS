"""
Etapa 6 — TME y M_dir.
Implementa el loop de interacción completo (fase temprana / topología estrella):
  query -> spaCy -> fastText -> broadcast -> argmax -> aprendizaje M_dir -> recall -> triple Wegner

Arquitectura (4 AMR por agente, 2 AMR por TME):
  Agent:
    mem_dom_L  PinedaAssociativeMemory(300, 16)        homo label
    mem_dom_R  PinedaAssociativeMemory(64, 32)          homo latent
    mem_dom_H  PinedaHAM4D(300,16,64,32)               hetero label↔latent
    mem_dir    PinedaDirectoryMemory(300, 16)           directorio routing

  TME:
    mem_dir_L  PinedaDirectoryMemory(300, 16)           label→agent
    mem_dir_R  PinedaDirectoryMemory(64, 32)            latent→agent (reservado)
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
from pineda_am import PinedaAssociativeMemory, PinedaDirectoryMemory
from quantizer import quantize_binary, quantize, dequantize

CLASSES = ["apple", "horse", "car"]
AGENT_VECS = {
    "apple": np.array([1, 0, 0], dtype=np.int32),
    "horse": np.array([0, 1, 0], dtype=np.int32),
    "car":   np.array([0, 0, 1], dtype=np.int32),
}
AGENT_LIST = CLASSES
N, M_LABEL = 300, 16
P_LATENT, Q_LATENT = 64, 32
MODELS_DIR = ROOT / "models"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ------------------------------------------------------------------
# NLP preprocessing
# ------------------------------------------------------------------

def get_nlp():
    import spacy
    return spacy.load("en_core_web_sm")


# Positive POS filter — only keep semantically meaningful content words.
# Spec: solo sustantivos y adjetivos (+ proper nouns for entity safety).
ACCEPTED_POS = {"NOUN", "ADJ", "PROPN"}


def tokenize_query(query: str, nlp) -> list:
    """spaCy tokenize + stopword filter + positive POS filter (NOUN/ADJ/PROPN)."""
    doc = nlp(query.lower())
    tokens = []
    for tok in doc:
        if tok.is_stop:
            continue
        if tok.pos_ not in ACCEPTED_POS:
            continue
        if not tok.is_alpha:
            continue
        tokens.append(tok.lemma_)
    return list(set(tokens))   # deduplicate


# ------------------------------------------------------------------
# Agent system — 4 AMRs per agent
# ------------------------------------------------------------------

class Agent:
    """
    Agente TMS con 4 memorias asociativas:
      mem_dom_L  — homo-asociativa dominio label  (PinedaAssociativeMemory)
      mem_dom_R  — homo-asociativa dominio latente (PinedaAssociativeMemory)
      mem_dom_H  — hetero-asociativa label↔latente (PinedaHAM4D / SimpleHAM4D)
      mem_dir    — directorio routing               (PinedaDirectoryMemory)

    mem_dom is a backward-compat property returning mem_dom_H.
    """

    def __init__(self, name: str, mem_dom_H,
                 mem_dom_L: PinedaAssociativeMemory = None,
                 mem_dom_R: PinedaAssociativeMemory = None):
        self.name      = name
        self.mem_dom_H = mem_dom_H
        # If M_dom_L/R not provided, create empty ones (uniform weights fallback)
        self.mem_dom_L = mem_dom_L if mem_dom_L is not None \
            else PinedaAssociativeMemory(N, M_LABEL)
        self.mem_dom_R = mem_dom_R if mem_dom_R is not None \
            else PinedaAssociativeMemory(P_LATENT, Q_LATENT)
        self.mem_dir   = PinedaDirectoryMemory(N, M_LABEL, len(AGENT_LIST))

    # ------------------------------------------------------------------
    # Backward compatibility
    # ------------------------------------------------------------------

    @property
    def mem_dom(self):
        """Backward-compat alias → mem_dom_H."""
        return self.mem_dom_H

    # ------------------------------------------------------------------
    # Pickle migration: handle agents pickled with the old structure
    # (mem_dom + mem_dir=SimpleDirectoryMemory before the 4-AMR migration).
    # ------------------------------------------------------------------

    def __setstate__(self, state):
        if "mem_dom_H" not in state and "mem_dom" in state:
            # Old pickle format: migrate on load
            state["mem_dom_H"] = state.pop("mem_dom")
            state["mem_dom_L"] = PinedaAssociativeMemory(N, M_LABEL)
            state["mem_dom_R"] = PinedaAssociativeMemory(P_LATENT, Q_LATENT)
            # M_dir: try to migrate from old SimpleDirectoryMemory
            old_dir = state.get("mem_dir")
            if old_dir is not None and not isinstance(old_dir, PinedaDirectoryMemory):
                # Rebuild as PinedaDirectoryMemory (old routing is lost)
                state["mem_dir"] = PinedaDirectoryMemory(N, M_LABEL, len(AGENT_LIST))
        self.__dict__.update(state)

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def recognize(self, v_label_q: np.ndarray) -> float:
        """
        One-sided recognition score from left (label) domain.

        Uses M_dom_L per-feature weights to modulate the hetero projection —
        following Pineda's architecture where left_eam.recog_weights feed
        into hetero_eam recognition.
        """
        left_weights = self.mem_dom_L.recog_weights(v_label_q)
        return self.mem_dom_H.recognize_from_left(v_label_q,
                                                   left_weights=left_weights)

    def recall(self, v_label_q: np.ndarray):
        """Hetero recall: label cue → latent. Returns (r_io, recognized, weight)."""
        return self.mem_dom_H.recall_from_left(v_label_q)

    def learn_dir(self, v_label_q: np.ndarray, winner_idx: int):
        """Register label→winner in this agent's directory memory."""
        self.mem_dir.register(v_label_q, winner_idx)


class TME:
    """
    Transactive Memory Engine — 2 AMRs:
      mem_dir_L  PinedaDirectoryMemory(300, 16) — label space routing
      mem_dir_R  PinedaDirectoryMemory(64,  32) — latent space routing (inverse)

    mem_dir is a backward-compat property returning mem_dir_L.
    """

    def __init__(self):
        self.mem_dir_L = PinedaDirectoryMemory(N, M_LABEL, len(AGENT_LIST))
        self.mem_dir_R = PinedaDirectoryMemory(P_LATENT, Q_LATENT, len(AGENT_LIST))

    @property
    def mem_dir(self):
        """Backward-compat alias → mem_dir_L."""
        return self.mem_dir_L

    def learn(self, v_label_q: np.ndarray, winner_idx: int):
        """Register label→winner in label-space directory."""
        self.mem_dir_L.register(v_label_q, winner_idx)

    def learn_latent(self, v_latent_q: np.ndarray, winner_idx: int):
        """Register latent→winner in latent-space directory."""
        self.mem_dir_R.register(v_latent_q, winner_idx)

    def route(self, v_label_q: np.ndarray) -> int:
        """Route from label space. Returns -1 for unseen tokens."""
        return self.mem_dir_L.nearest_agent(v_label_q)

    def route_latent(self, v_latent_q: np.ndarray) -> int:
        """Route from latent space (inverse direction)."""
        return self.mem_dir_R.nearest_agent(v_latent_q)

    def __setstate__(self, state):
        """Pickle migration from old single-AMR TME."""
        if "mem_dir_L" not in state:
            old_dir = state.get("mem_dir")
            state["mem_dir_L"] = PinedaDirectoryMemory(N, M_LABEL, len(AGENT_LIST))
            state["mem_dir_R"] = PinedaDirectoryMemory(P_LATENT, Q_LATENT, len(AGENT_LIST))
            state.pop("mem_dir", None)
        self.__dict__.update(state)


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
    a) tokenize -> b) fastText -> c) broadcast -> d) argmax ->
    e) learn M_dir (4 components) -> f) recall -> triple Wegner.

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
            # Uses M_dom_L weights internally (Pineda architecture)
            w = agents[cls].recognize(v_q)
            agent_scores[cls] += w

    # Average over tokens
    n_toks = len(tokens)
    for cls in CLASSES:
        agent_scores[cls] /= n_toks

    # --- Argmax over mean_weight ---
    winner = max(agent_scores, key=agent_scores.get)
    winner_idx = AGENT_LIST.index(winner)

    if verbose:
        score_str = "  ".join(f"{c}={agent_scores[c]:.2f}" for c in CLASSES)
        print(f"  Scores: {score_str}  -> winner: {winner}")

    # --- Learning M_dir in all 4 components (TME + 3 agents) ---
    for tok, v_q in token_vectors.items():
        tme.learn(v_q, winner_idx)            # TME label-space M_dir
        for agent in agents.values():
            agent.learn_dir(v_q, winner_idx)  # each agent's M_dir

    # --- Recall: use the first recognized token ---
    recalled_image = None
    recalled_labels = tokens
    _stats_path = MODELS_DIR / "latent_global_stats.json"
    _stats = json.loads(_stats_path.read_text())
    _g_min = np.array(_stats["global_min"])
    _g_max = np.array(_stats["global_max"])

    recalled_q_winner = None
    for tok, v_q in token_vectors.items():
        recalled_q, recognized, weight = agents[winner].recall(v_q)
        if recognized:
            recalled_q_winner = recalled_q
            # Dequantize using global stats (consistent with stage5 filling)
            v_norm = recalled_q.astype(float) / (Q_LATENT - 1)
            v_latent = (v_norm * (_g_max - _g_min) + _g_min).astype(np.float32)
            z = torch.tensor(v_latent).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                img = decoder(z)[0].cpu()
            recalled_image = img
            break

    # Also register recalled latent in TME's latent-space M_dir
    if recalled_q_winner is not None:
        v_latent_q = recalled_q_winner.astype(np.int32)
        tme.learn_latent(v_latent_q, winner_idx)

    return {
        "query": query,
        "tokens": tokens,
        "agent_scores": agent_scores,
        "winner": winner,
        "image": recalled_image,
        "labels": recalled_labels,
    }


def load_agents() -> dict:
    """Load agents with all 3 domain memories (H, L, R)."""
    from stage5_fill import load_agent_memories
    agents = {}
    for cls in CLASSES:
        mem_H, mem_L, mem_R = load_agent_memories(cls)
        agents[cls] = Agent(cls, mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)
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

    # Remap __main__ to stage6_interaction for unpickling objects saved
    # when stage6 was run directly as __main__.
    old_main = sys.modules.get("__main__")
    sys.modules["__main__"] = _s6

    try:
        with open(MODELS_DIR / "tme.pkl", "rb") as f:
            tme = pickle.load(f)
        agents = {}
        for cls in CLASSES:
            with open(MODELS_DIR / f"agent_{cls}.pkl", "rb") as f:
                agents[cls] = pickle.load(f)
    finally:
        if old_main is not None:
            sys.modules["__main__"] = old_main

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
