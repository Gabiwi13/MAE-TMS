"""
Etapa 7 -- Recuperacion bidireccional.
Direccion inversa: imagen -> CNN_encoder -> v_latente ->
M_dom.recall_from_right(v_latente) -> nearest_neighbor -> top-3 labels.
"""
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import torch
from torchvision import transforms
from PIL import Image

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from mae_ham import SimpleHAM4D
from quantizer import quantize_binary
from stage5_fill import quantize_latent_global
from stage6_interaction import CLASSES, MODELS_DIR, DEVICE, load_tme_and_agents

DATA_DIR = ROOT / "data" / "eth80"
N, M_LABEL, P, Q_IMG = 300, 16, 64, 32

IMG_TRANSFORM = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def load_global_stats():
    stats = json.loads((MODELS_DIR / "latent_global_stats.json").read_text())
    return np.array(stats["global_min"]), np.array(stats["global_max"])


def load_proto_latents():
    protos = {}
    for cls in CLASSES:
        path = MODELS_DIR / f"proto_latent_{cls}.json"
        protos[cls] = np.array(json.loads(path.read_text()))
    return protos


def load_encoder():
    from stage2_encoder import Encoder
    enc = Encoder().to(DEVICE)
    enc.load_state_dict(torch.load(MODELS_DIR / "encoder.pt", map_location=DEVICE))
    enc.eval()
    return enc


def image_to_latent(img_path: str, encoder) -> np.ndarray:
    img = Image.open(img_path).convert("RGB").resize((128, 128))
    t = IMG_TRANSFORM(img).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        z = encoder(t).cpu().numpy()[0]
    return z


def find_winner_agent(v_latent: np.ndarray, proto_latents: dict) -> str:
    """Level-1: find closest domain prototype (Euclidean in latent space)."""
    best_cls = None
    best_dist = float("inf")
    for cls, proto in proto_latents.items():
        dist = np.linalg.norm(v_latent - proto)
        if dist < best_dist:
            best_dist = dist
            best_cls = cls
    return best_cls


def recover_labels(v_latent: np.ndarray, agent, g_min, g_max,
                   vectors: dict, top_k: int = 3) -> list:
    """Level-2: recall label vector from image latent and find nearest labels."""
    v_q = quantize_latent_global(v_latent, g_min, g_max, Q_IMG)

    # Use soft recall to tolerate test-image deviation from stored prototype
    recalled_q, score = agent.mem_dom.recall_from_right_soft(v_q)
    if score == 0.0:
        return []

    # Convert recalled label indices to continuous {-1,+1} space
    recalled_cont = (recalled_q.astype(float) / max(M_LABEL - 1, 1)) * 2.0 - 1.0

    # Find nearest neighbors in label dictionary (cosine similarity)
    similarities = []
    for word, vec in vectors.items():
        v = np.array(vec, dtype=np.float32)
        sim = float(np.dot(recalled_cont, v) / (
            np.linalg.norm(recalled_cont) * np.linalg.norm(v) + 1e-8))
        similarities.append((word, sim))

    similarities.sort(key=lambda x: -x[1])
    return [w for w, s in similarities[:top_k]]


def run():
    print("Loading encoder and agents...")
    encoder = load_encoder()
    g_min, g_max = load_global_stats()
    proto_latents = load_proto_latents()

    tme, agents_full = load_tme_and_agents()

    # Load label vectors
    all_vectors = {}
    for cls in CLASSES:
        path = ROOT / f"label_vectors_{cls}.json"
        all_vectors[cls] = json.loads(path.read_text())

    # Get test images
    splits_path = DATA_DIR / "splits.json"
    splits = json.loads(splits_path.read_text())

    print("\n--- Inverse retrieval: image -> labels ---")
    results = []
    for cls in CLASSES:
        test_imgs = splits[cls]["test"][:2]
        for img_path in test_imgs:
            v_latent = image_to_latent(img_path, encoder)

            # Level 1: domain detection
            winner_cls = find_winner_agent(v_latent, proto_latents)

            # Level 2: label recovery
            top_labels = recover_labels(
                v_latent, agents_full[winner_cls],
                g_min, g_max, all_vectors[winner_cls])

            print(f"  [{cls}] image={Path(img_path).name}")
            print(f"         domain_found={winner_cls}  top-3 labels={top_labels}")
            coherent = winner_cls == cls
            results.append({
                "true_class": cls,
                "predicted_class": winner_cls,
                "top_labels": top_labels,
                "coherent": coherent,
            })

    correct_domain = sum(1 for r in results if r["coherent"])
    print(f"\nDomain accuracy (Level 1): {correct_domain}/{len(results)}")
    labels_nonempty = sum(1 for r in results if r["top_labels"])
    print(f"Queries with recovered labels: {labels_nonempty}/{len(results)}")

    _visualize(results, splits, proto_latents)
    print("\nEtapa 7 COMPLETADA.")
    return results


def _visualize(results, splits, proto_latents):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n = len(results)
    fig, axes = plt.subplots(1, n, figsize=(3*n, 4))
    if n == 1:
        axes = [axes]

    img_idx = 0
    for cls in CLASSES:
        for img_path in splits[cls]["test"][:2]:
            img = Image.open(img_path).convert("RGB").resize((128, 128))
            r = results[img_idx]
            ax = axes[img_idx]
            ax.imshow(np.array(img))
            label_str = ", ".join(r["top_labels"]) if r["top_labels"] else "none"
            color = "green" if r["coherent"] else "red"
            ax.set_title(f"true:{cls}\npred:{r['predicted_class']}\n{label_str}",
                         fontsize=6, color=color)
            ax.axis("off")
            img_idx += 1

    plt.tight_layout()
    out = ROOT / "stage7_inverse_retrieval.png"
    plt.savefig(out, dpi=80)
    print(f"Saved -> {out.name}")


if __name__ == "__main__":
    run()
