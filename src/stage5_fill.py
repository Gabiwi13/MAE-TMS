"""
Etapa 5 — Llenado de M_dom por agente.

Genera 3 archivos pkl por clase:
  mem_dom_{cls}.pkl    — M_dom_H: PinedaHAM4D(n=300, m=16, p=64, q=32)
  mem_dom_L_{cls}.pkl  — M_dom_L: PinedaAssociativeMemory(n=300, m=16) homo label
  mem_dom_R_{cls}.pkl  — M_dom_R: PinedaAssociativeMemory(n=64,  m=32) homo latent

Para cada label: register(v_label_q, v_proto_q) × freq en M_dom_H
                 register(v_label_q)             × freq en M_dom_L
Para el prototipo: register(v_proto_q)            ×   1  en M_dom_R
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
from pineda_am import PinedaAssociativeMemory
from quantizer import quantize_binary, quantize
from stage4_fasttext import get_vector as ft_get_vector

CLASSES = ["apple", "horse", "car"]
N, M, P, Q = 300, 16, 64, 32
MODELS_DIR = ROOT / "models"
DATA_DIR = ROOT / "data" / "eth80"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

IMG_TRANSFORM = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def load_encoder():
    from stage2_encoder import Encoder, load_models
    encoder, _, _ = load_models()
    return encoder


def get_prototype_latent(encoder, cls: str) -> np.ndarray:
    splits_path = DATA_DIR / "splits.json"
    splits = json.loads(splits_path.read_text())
    paths = splits[cls]["train"]
    zs = []
    encoder.eval()
    with torch.no_grad():
        for p in paths[:50]:   # use first 50 for speed
            img = Image.open(p).convert("RGB").resize((128, 128))
            img_t = IMG_TRANSFORM(img).unsqueeze(0).to(DEVICE)
            z = encoder(img_t).cpu().numpy()[0]
            zs.append(z)
    return np.mean(zs, axis=0)


def compute_global_latent_stats(encoder) -> tuple:
    """Compute global min/max across all training images for consistent quantization."""
    stats_path = MODELS_DIR / "latent_global_stats.json"
    if stats_path.exists():
        s = json.loads(stats_path.read_text())
        return np.array(s["global_min"]), np.array(s["global_max"])

    print("  Computing global latent statistics...")
    splits_path = DATA_DIR / "splits.json"
    splits = json.loads(splits_path.read_text())
    all_zs = []
    encoder.eval()
    with torch.no_grad():
        for cls in CLASSES:
            for p in splits[cls]["train"][:30]:
                img = Image.open(p).convert("RGB").resize((128, 128))
                img_t = IMG_TRANSFORM(img).unsqueeze(0).to(DEVICE)
                z = encoder(img_t).cpu().numpy()[0]
                all_zs.append(z)
    all_zs = np.stack(all_zs)
    g_min = all_zs.min(axis=0)
    g_max = all_zs.max(axis=0)
    # Add small margin to avoid boundary effects
    margin = 0.1 * (g_max - g_min)
    g_min -= margin
    g_max += margin
    stats_path.write_text(json.dumps({
        "global_min": g_min.tolist(),
        "global_max": g_max.tolist(),
    }))
    print(f"  Global stats saved (min range: {g_min.min():.3f}, max range: {g_max.max():.3f})")
    return g_min, g_max


def quantize_latent_global(v: np.ndarray, g_min: np.ndarray,
                           g_max: np.ndarray, q: int) -> np.ndarray:
    """Quantize latent vector using global min/max (consistent across all images)."""
    rng = g_max - g_min
    rng = np.where(rng == 0, 1e-8, rng)
    v_norm = np.clip((v - g_min) / rng, 0.0, 1.0)
    q_vals = np.floor(v_norm * q).astype(np.int32)
    return np.clip(q_vals, 0, q - 1)


def fill_agent(cls: str, encoder, g_min: np.ndarray, g_max: np.ndarray):
    """
    Fill M_dom_H (hetero), M_dom_L (homo label) and M_dom_R (homo latent)
    for one agent class.

    Returns (mem_dom_H, mem_dom_L, mem_dom_R).
    """
    labels_path = ROOT / f"labels_{cls}.json"
    vectors_path = ROOT / f"label_vectors_{cls}.json"
    labels = json.loads(labels_path.read_text())     # {word: freq}
    raw_vecs = json.loads(vectors_path.read_text())  # {word: [300 floats]}

    # Get prototype latent vector for this class
    print(f"  Computing prototype latent for {cls}...")
    v_proto = get_prototype_latent(encoder, cls)   # (64,) continuous
    v_proto_q = quantize_latent_global(v_proto, g_min, g_max, Q)

    # Save prototype latent for stage7
    proto_path = MODELS_DIR / f"proto_latent_{cls}.json"
    proto_path.write_text(json.dumps(v_proto.tolist()))

    # ── M_dom_H: PinedaHAM4D (hetero label↔latent) ──────────────────
    mem_H = SimpleHAM4D(N, M, P, Q, iota=0.0, kappa=0.0, xi=0, sigma=0.1)

    # ── M_dom_L: AssociativeMemory (homo label domain) ───────────────
    mem_L = PinedaAssociativeMemory(N, M)

    # ── M_dom_R: AssociativeMemory (homo latent domain) ──────────────
    mem_R = PinedaAssociativeMemory(P, Q)

    n_registered = 0
    for word, freq in labels.items():
        if word not in raw_vecs:
            continue
        v_label = np.array(raw_vecs[word], dtype=np.float32)  # {-1, +1}^300
        v_label_q = quantize_binary(v_label, M)                 # [0, M-1]^300

        for _ in range(freq):
            # Hetero: label↔latent association
            mem_H.register(v_label_q, v_proto_q)
            # Homo label: learn the label distribution for this domain
            mem_L.register(v_label_q)
        n_registered += freq

    # Register prototype latent in M_dom_R (latent homo memory)
    mem_R.register(v_proto_q)

    print(f"  {cls}: {len(labels)} labels, {n_registered} hetero+homo registrations")
    mem_H.print_stats(cls)
    mem_L.print_stats(f"{cls}_L")
    mem_R.print_stats(f"{cls}_R")

    return mem_H, mem_L, mem_R


def probe_recall(mem_H: SimpleHAM4D, cls: str, encoder, n_probes: int = 5):
    """Quick sanity check: query known labels and decode."""
    from stage2_encoder import Decoder, load_models
    _, decoder, _ = load_models()

    labels_path = ROOT / f"labels_{cls}.json"
    vectors_path = ROOT / f"label_vectors_{cls}.json"
    labels = json.loads(labels_path.read_text())
    raw_vecs = json.loads(vectors_path.read_text())

    inv_norm = transforms.Normalize(
        mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
        std=[1/0.229, 1/0.224, 1/0.225])

    sample_words = list(labels.keys())[:n_probes]
    print(f"  Probing {cls} with: {sample_words}")

    decoder.eval()
    results = []
    for word in sample_words:
        if word not in raw_vecs:
            continue
        v_label = np.array(raw_vecs[word], dtype=np.float32)
        v_label_q = quantize_binary(v_label, M)
        recalled_q, recognized, weight = mem_H.recall_from_left(v_label_q)

        if recognized:
            from quantizer import dequantize
            v_latent = dequantize(recalled_q.astype(float), Q).astype(np.float32)
            z = torch.tensor(v_latent).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                img_recon = decoder(z)[0].cpu()
            results.append((word, recognized, weight, img_recon))
        else:
            results.append((word, False, 0.0, None))

    return results


def save_agent_memories(mem_H: SimpleHAM4D,
                        mem_L: PinedaAssociativeMemory,
                        mem_R: PinedaAssociativeMemory,
                        cls: str):
    """Save the three domain memories for one agent class."""
    # M_dom_H
    path_H = MODELS_DIR / f"mem_dom_{cls}.pkl"
    with open(path_H, "wb") as f:
        pickle.dump(mem_H, f)
    print(f"  Saved M_dom_H_{cls} -> {path_H.name}")

    # M_dom_L
    path_L = MODELS_DIR / f"mem_dom_L_{cls}.pkl"
    with open(path_L, "wb") as f:
        pickle.dump(mem_L, f)
    print(f"  Saved M_dom_L_{cls} -> {path_L.name}")

    # M_dom_R
    path_R = MODELS_DIR / f"mem_dom_R_{cls}.pkl"
    with open(path_R, "wb") as f:
        pickle.dump(mem_R, f)
    print(f"  Saved M_dom_R_{cls} -> {path_R.name}")


def load_agent_memories(cls: str):
    """
    Load M_dom_H, M_dom_L, M_dom_R for one agent class.
    Returns (mem_H, mem_L, mem_R) — mem_L and mem_R may be None if
    their pkl files don't exist yet (backward compat).
    """
    path_H = MODELS_DIR / f"mem_dom_{cls}.pkl"
    with open(path_H, "rb") as f:
        mem_H = pickle.load(f)

    path_L = MODELS_DIR / f"mem_dom_L_{cls}.pkl"
    mem_L = None
    if path_L.exists():
        with open(path_L, "rb") as f:
            mem_L = pickle.load(f)

    path_R = MODELS_DIR / f"mem_dom_R_{cls}.pkl"
    mem_R = None
    if path_R.exists():
        with open(path_R, "rb") as f:
            mem_R = pickle.load(f)

    return mem_H, mem_L, mem_R


# ── Keep old single-memory API for backward compat ──────────────────

def load_agent(cls: str) -> SimpleHAM4D:
    """Backward-compat: load only M_dom_H."""
    path = MODELS_DIR / f"mem_dom_{cls}.pkl"
    with open(path, "rb") as f:
        return pickle.load(f)


def save_agent(mem: SimpleHAM4D, cls: str):
    """Backward-compat: save only M_dom_H."""
    path = MODELS_DIR / f"mem_dom_{cls}.pkl"
    with open(path, "wb") as f:
        pickle.dump(mem, f)
    print(f"  Saved M_dom_{cls} -> {path.name}")


def visualize_probes(results: list, cls: str):
    """Save probe reconstructions to PNG."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    good = [(w, img) for w, ok, wt, img in results if ok and img is not None]
    if not good:
        print(f"  No recognized probes for {cls}")
        return
    n = len(good)
    fig, axes = plt.subplots(1, n, figsize=(3*n, 3))
    if n == 1:
        axes = [axes]
    for ax, (word, img) in zip(axes, good):
        ax.imshow(img.permute(1, 2, 0).numpy().clip(0, 1))
        ax.set_title(word, fontsize=8)
        ax.axis("off")
    plt.suptitle(f"M_dom_H_{cls} — recall probes")
    plt.tight_layout()
    out = ROOT / f"stage5_probes_{cls}.png"
    plt.savefig(out, dpi=80)
    print(f"  Probes saved -> {out.name}")


def run():
    encoder = load_encoder()
    g_min, g_max = compute_global_latent_stats(encoder)
    agents_H = {}

    for cls in CLASSES:
        print(f"\n--- Filling M_dom for agent {cls} ---")
        path_H = MODELS_DIR / f"mem_dom_{cls}.pkl"
        path_L = MODELS_DIR / f"mem_dom_L_{cls}.pkl"
        path_R = MODELS_DIR / f"mem_dom_R_{cls}.pkl"

        if path_H.exists() and path_L.exists() and path_R.exists():
            print(f"  All 3 memory files exist, loading.")
            mem_H, mem_L, mem_R = load_agent_memories(cls)
        else:
            if path_H.exists():
                print(f"  M_dom_H exists; regenerating M_dom_L + M_dom_R.")
            mem_H, mem_L, mem_R = fill_agent(cls, encoder, g_min, g_max)
            save_agent_memories(mem_H, mem_L, mem_R, cls)

        agents_H[cls] = mem_H
        results = probe_recall(agents_H[cls], cls, encoder)
        for word, ok, wt, _ in results:
            print(f"    '{word}': recognized={ok}, weight={wt:.2f}")
        visualize_probes(results, cls)

    print("\nEtapa 5 COMPLETADA.")
    return agents_H


if __name__ == "__main__":
    run()
