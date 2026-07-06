"""
Etapa 8 — Fase madura: coordinacion de recuperacion punto a punto.

El TME queda fuera del circuito. Cada consulta entra por un agente
aleatorio, que consulta su propio directorio para decidir quien debe
atenderla. La lectura del directorio usa B1 (÷count): el score crudo de
una HAM crece con la masa de registros del agente y, sin calibrar, el
mas registrado gana aunque no sepa.

Metrica: fidelidad = consultas donde la fase madura llega al mismo
agente que la temprana. Mide coincidencia con lo aprendido, no acierto
contra ground truth.
"""
import json
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from quantizer import quantize_binary
from stage6_interaction import (
    CLASSES, MODELS_DIR, DEVICE,
    load_tme_and_agents, get_nlp, load_decoder, load_all_vectors,
    tokenize_query, get_fasttext_vector, token_in_vocabulary, TEST_QUERIES,
)

M_LABEL = 16
Q_LATENT = 32


def _load_global_stats():
    stats = json.loads((MODELS_DIR / "latent_global_stats.json").read_text())
    return np.array(stats["global_min"]), np.array(stats["global_max"])


def route_mature(query: str, entry_agent, agents: dict, nlp,
                 vectors_cache: dict, decoder,
                 g_min: np.ndarray, g_max: np.ndarray,
                 verbose: bool = True) -> dict:
    """El agente de entrada decide con su directorio a quien rutear.
    Sin señal en el directorio, rechaza: el grupo no inventa expertos."""
    tokens = tokenize_query(query, nlp)
    if not tokens:
        return {"query": query, "winner": None, "image": None,
                "routed": False}

    # Sin filtro léxico: cada token con vector fastText real entra como pista;
    # los no representables se descartan. El rechazo lo decide el directorio.
    token_vectors = {}
    unrepresented_tokens = []
    for tok in tokens:
        v = get_fasttext_vector(tok, vectors_cache, allow_fallback=False)
        if v is None:
            unrepresented_tokens.append(tok)
            continue
        token_vectors[tok] = quantize_binary(
            np.asarray(v, dtype=np.float32), M_LABEL)

    if verbose and unrepresented_tokens:
        print(f"  Tokens no representables (sin vector fastText): {unrepresented_tokens}")

    if not token_vectors:
        return {"query": query, "winner": None, "image": None,
                "routed": False, "scores": [0.0] * len(CLASSES),
                "rejected": True, "reason": "no_representable_tokens"}

    # La decisión multi-pista la toma la MAE (DirectoryMemory.route_multi):
    # suma calibrada B1 por token + argmax dentro de la memoria.
    dest_idx, agent_scores = entry_agent.mem_dir.route_multi(
        token_vectors.values(), mode="linear")

    if dest_idx < 0:
        if verbose:
            print(f"  RECHAZADA (directory_no_support): '{query}'.")
        return {"query": query, "winner": None, "image": None,
                "routed": False, "scores": agent_scores.tolist(),
                "rejected": True, "reason": "directory_no_support"}

    dest_name = CLASSES[dest_idx]
    dest_agent = agents[dest_name]
    routed = dest_name != entry_agent.name

    if verbose:
        score_str = "  ".join(f"{c}={agent_scores[i]:.1f}"
                              for i, c in enumerate(CLASSES))
        print(f"  Entrada={entry_agent.name}  scores=[{score_str}]"
              f"  -> destino={dest_name}  routed={routed}")

    recalled_image = None
    for tok, v_q in token_vectors.items():
        recalled_q, recognized, weight, *_ = \
            dest_agent.mem_dom_H.recall_from_left(v_q)
        if recognized:
            v_norm = recalled_q.astype(float) / (Q_LATENT - 1)
            v_latent = (v_norm * (g_max - g_min) + g_min).astype(np.float32)
            z = torch.tensor(v_latent).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                recalled_image = decoder(z)[0].cpu()
            break

    return {
        "query": query,
        "winner": dest_name,
        "image": recalled_image,
        "routed": routed,
        "scores": agent_scores.tolist(),
    }


def run():
    print("Cargando agentes (fase madura — TME desactivado)...")
    tme, agents = load_tme_and_agents()
    nlp = get_nlp()
    decoder = load_decoder()
    vectors_cache = load_all_vectors(nlp)
    g_min, g_max = _load_global_stats()

    from stage6_interaction import process_query

    print("\n--- Referencia de fase temprana (TME activo) ---")
    early_results = {}
    for query in TEST_QUERIES:
        res = process_query(query, agents, tme, nlp, vectors_cache, decoder,
                            verbose=False)
        early_results[query] = res["winner"]
        print(f"  '{query}' -> {res['winner']}")

    print("\n--- Fase madura (punto a punto) ---")
    mature_results = {}
    rng = np.random.RandomState(42)
    fidelity_count = 0

    for i, query in enumerate(TEST_QUERIES):
        entry_cls = CLASSES[rng.randint(0, len(CLASSES))]
        res = route_mature(query, agents[entry_cls], agents, nlp,
                           vectors_cache, decoder, g_min, g_max, verbose=False)
        mature_results[query] = res["winner"]
        early_winner = early_results.get(query)
        match = res["winner"] == early_winner
        fidelity_count += int(match)
        print(f"  Q{i+1}: temprana={early_winner}  madura={res['winner']}  "
              f"match={'OK' if match else 'X'}  entrada={entry_cls}")

    fidelity = fidelity_count / len(TEST_QUERIES)
    print(f"\nFidelidad: {fidelity_count}/{len(TEST_QUERIES)} "
          f"= {fidelity*100:.1f}%")

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
    ax.barh(range(n), [1] * n, color=colors, alpha=0.7)
    labels_txt = [f"Q{i+1}: temprana={early[q]} | madura={mature.get(q, '?')}"
                  for i, q in enumerate(queries)]
    ax.set_yticks(range(n))
    ax.set_yticklabels(labels_txt, fontsize=7)
    ax.set_xlabel("match (verde) / mismatch (rojo)")
    ax.set_title("Fidelidad de la fase madura")
    plt.tight_layout()
    plt.savefig(ROOT / "stage8_fidelity.png", dpi=80)
    print("Grafica de fidelidad -> stage8_fidelity.png")


if __name__ == "__main__":
    run()
