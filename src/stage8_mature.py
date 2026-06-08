"""
Etapa 8 — Fase madura.
TME desactivado. Routing punto a punto via M_dir de cada agente.
Métrica: fidelidad = queries con mismo resultado / total queries.
"""
import json
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from quantizer import quantize_binary, dequantize
from stage6_interaction import (
    CLASSES, MODELS_DIR, DEVICE,
    load_tme_and_agents, get_nlp, load_decoder, load_all_vectors,
    tokenize_query, get_fasttext_vector, TEST_QUERIES,
)

M_LABEL = 16


def route_mature(query: str, entry_agent, agents: dict, nlp,
                 vectors_cache: dict, decoder, verbose: bool = True) -> dict:
    """
    Mature phase: no TME. Entry agent receives query, consults its M_dir,
    routes to correct agent (or self), and recalls.
    """
    tokens = tokenize_query(query, nlp)
    if not tokens:
        return {"query": query, "winner": None, "image": None, "routed": False}

    token_vectors = {tok: quantize_binary(
        get_fasttext_vector(tok, vectors_cache), M_LABEL)
        for tok in tokens}

    # Aggregate routing votes over tokens from entry_agent's M_dir
    agent_scores = np.zeros(len(CLASSES), dtype=float)
    for v_q in token_vectors.values():
        scores = entry_agent.mem_dir.predict(v_q)
        agent_scores += scores

    if agent_scores.sum() == 0:
        # Unknown -> fallback to first agent
        dest_idx = 0
    else:
        dest_idx = int(np.argmax(agent_scores))

    dest_name = CLASSES[dest_idx]
    dest_agent = agents[dest_name]
    routed = (dest_name != entry_agent.name)

    if verbose:
        score_str = "  ".join(f"{c}={agent_scores[i]:.1f}"
                              for i, c in enumerate(CLASSES))
        print(f"  Entry={entry_agent.name}  scores=[{score_str}]"
              f"  -> dest={dest_name}  routed={routed}")

    # Recall at destination
    recalled_image = None
    for tok, v_q in token_vectors.items():
        recalled_q, recognized, weight = dest_agent.mem_dom.recall_from_left(v_q)
        if recognized:
            v_latent = dequantize(recalled_q.astype(float), 32).astype(np.float32)
            z = torch.tensor(v_latent).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                img = decoder(z)[0].cpu()
            recalled_image = img
            break

    return {
        "query": query,
        "winner": dest_name,
        "image": recalled_image,
        "routed": routed,
        "scores": agent_scores.tolist(),
    }


def run():
    print("Loading agents (mature phase — TME disabled)...")
    tme, agents = load_tme_and_agents()
    nlp = get_nlp()
    decoder = load_decoder()
    vectors_cache = load_all_vectors()

    # Re-run same 10 queries with TME to get ground truth
    from stage6_interaction import process_query, TME
    tme_ref = TME()  # fresh TME for reference (reuse saved tme)
    tme_ref = tme    # use already-trained TME

    print("\n--- Early phase reference (TME active) ---")
    early_results = {}
    for query in TEST_QUERIES:
        from stage6_interaction import process_query
        res = process_query(query, agents, tme_ref, nlp, vectors_cache, decoder, verbose=False)
        early_results[query] = res["winner"]
        print(f"  '{query}' -> {res['winner']}")

    print("\n--- Mature phase (point-to-point) ---")
    # Each query enters via a random agent
    mature_results = {}
    rng = np.random.RandomState(42)
    fidelity_count = 0

    for i, query in enumerate(TEST_QUERIES):
        entry_cls = CLASSES[rng.randint(0, len(CLASSES))]
        entry_agent = agents[entry_cls]
        res = route_mature(query, entry_agent, agents, nlp, vectors_cache, decoder)
        mature_results[query] = res["winner"]

        early_winner = early_results.get(query)
        match = (res["winner"] == early_winner)
        if match:
            fidelity_count += 1
        print(f"  Q{i+1}: early={early_winner}  mature={res['winner']}  "
              f"match={'OK' if match else 'X'}  entry={entry_cls}")

    fidelity = fidelity_count / len(TEST_QUERIES)
    print(f"\nFidelidad: {fidelity_count}/{len(TEST_QUERIES)} = {fidelity*100:.1f}%")

    # Visualize
    _visualize_mature(TEST_QUERIES, early_results, mature_results)

    print("\nEtapa 8 COMPLETADA.")
    return fidelity


def _visualize_mature(queries, early, mature):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n = len(queries)
    matches = [early[q] == mature.get(q) for q in queries]
    colors = ["green" if m else "red" for m in matches]

    fig, ax = plt.subplots(figsize=(10, 4))
    y = range(n)
    ax.barh(list(y), [1]*n, color=colors, alpha=0.7)
    labels_txt = [f"Q{i+1}: early={early[q]} | mature={mature.get(q,'?')}"
                  for i, q in enumerate(queries)]
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels_txt, fontsize=7)
    ax.set_xlabel("match (green) / mismatch (red)")
    ax.set_title("Mature phase fidelity")
    plt.tight_layout()
    out = ROOT / "stage8_fidelity.png"
    plt.savefig(out, dpi=80)
    print(f"Fidelity chart saved -> {out.name}")


if __name__ == "__main__":
    run()
