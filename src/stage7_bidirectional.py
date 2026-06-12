"""
Etapa 7 — Hemisferio visual: el directorio de imagenes.

Fase A (interacciones visuales): las imagenes de entrenamiento que no
participaron del llenado (indices [N_FILL:]) se presentan al grupo,
intercaladas por clase. Cada agente puntua la percepcion con su lado
latente —pesos de M_dom_R modulando la proyeccion de M_dom_H, el espejo
derecho del scoring de la etapa 6— y el TME registra (latente -> ganador)
en su directorio visual. Solo percepciones reales entran al directorio.

Fase B (evaluacion): las imagenes de test rutean por mem_dir_R con
lectura B1, y el agente destino evoca labels con recall_from_right
modulado por los pesos de M_dom_R. La metrica de evocacion es top-3
domain hit: algun label evocado pertenece al vocabulario de la clase.
"""
import io
import json
import sys
import contextlib
from pathlib import Path

import numpy as np
import torch
from torchvision import transforms
from PIL import Image

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from stage5_fill import quantize_latent_global, N_FILL
from stage6_interaction import (
    CLASSES, AGENT_LIST, MODELS_DIR, DEVICE,
    load_tme_and_agents, load_all_vectors,
)

DATA_DIR = ROOT / "data" / "eth80"
N, M_LABEL, P, Q_IMG = 300, 16, 64, 32
N_EVOKE = 15

IMG_TRANSFORM = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def load_global_stats():
    stats = json.loads((MODELS_DIR / "latent_global_stats.json").read_text())
    return np.array(stats["global_min"]), np.array(stats["global_max"])


def load_encoder():
    from stage2_encoder import Encoder
    enc = Encoder().to(DEVICE)
    enc.load_state_dict(torch.load(MODELS_DIR / "encoder.pt",
                                   map_location=DEVICE))
    enc.eval()
    return enc


def image_to_latent(img_path: str, encoder) -> np.ndarray:
    img = Image.open(img_path).convert("RGB").resize((128, 128))
    t = IMG_TRANSFORM(img).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        return encoder(t).cpu().numpy()[0]


def recognize_gated_right(agent, z_q: np.ndarray) -> float:
    """Score visual de un agente: activacion media de la proyeccion
    derecha de M_dom_H, modulada por los pesos de M_dom_R y gateada
    por containment. Espejo de Agent.recognize_gated desde el dominio
    latente."""
    r_w = agent.mem_dom_R.recog_weights(z_q)
    mx = r_w.max()
    weights = (r_w / mx) if mx > 0 else np.ones(len(z_q), dtype=float)
    mem_H = agent.mem_dom_H
    cb = mem_H.validate(z_q, 1)
    with contextlib.redirect_stdout(io.StringIO()):
        proj = mem_H.project(cb, weights, 1)
    if np.count_nonzero(np.sum(proj, axis=1) == 0) > 0:
        return 0.0
    count = int(np.count_nonzero(proj))
    return float(np.sum(proj)) / count if count > 0 else 0.0


def evoke_labels(agent, z_q: np.ndarray, vectors: dict, top_k: int = 3):
    """Evoca labels desde una imagen: recall inverso modulado por los
    pesos de M_dom_R, luego vecinos por coseno en el diccionario. El
    patron recordado es una muestra de la distribucion de labels del
    agente, no una palabra exacta; el diccionario lo interpreta."""
    r_w = agent.mem_dom_R.recog_weights(z_q)
    with contextlib.redirect_stdout(io.StringIO()):
        recalled_q, recognized, weight, *_ = agent.mem_dom_H.recall_from_right(
            z_q, weights=r_w)
    if not recognized:
        return []
    recalled_cont = (recalled_q.astype(float) / max(M_LABEL - 1, 1)) * 2.0 - 1.0
    sims = []
    for word, vec in vectors.items():
        v = np.array(vec, dtype=np.float32)
        sim = float(np.dot(recalled_cont, v) /
                    (np.linalg.norm(recalled_cont) * np.linalg.norm(v) + 1e-8))
        sims.append((word, sim))
    sims.sort(key=lambda x: -x[1])
    return [w for w, s in sims[:top_k]]


def run():
    print("Etapa 7 — hemisferio visual")
    encoder = load_encoder()
    g_min, g_max = load_global_stats()
    splits = json.loads((DATA_DIR / "splits.json").read_text())

    print("Cargando TME + agentes (etapa 6)...")
    tme, agents = load_tme_and_agents()
    label_vecs = load_all_vectors()
    vocab_by_cls = {cls: set(label_vecs[cls].keys()) for cls in CLASSES}
    all_vecs = {}
    for cls in CLASSES:
        all_vecs.update(label_vecs[cls])

    print(f"\n--- Fase A: interacciones visuales (train[{N_FILL}:]) ---")
    pools = {cls: splits[cls]["train"][N_FILL:] for cls in CLASSES}
    n_inter = max(len(p) for p in pools.values())
    a_ok = a_seen = a_rej = 0
    for i in range(n_inter):
        for cls in CLASSES:
            if i >= len(pools[cls]):
                continue
            z = image_to_latent(pools[cls][i], encoder)
            z_q = quantize_latent_global(z, g_min, g_max, Q_IMG)
            scores = {c: recognize_gated_right(agents[c], z_q)
                      for c in CLASSES}
            if sum(scores.values()) == 0:
                a_rej += 1
                continue
            winner = max(scores, key=scores.get)
            with contextlib.redirect_stdout(io.StringIO()):
                tme.update_directory_latent(z_q, AGENT_LIST.index(winner))
            a_seen += 1
            a_ok += int(winner == cls)
        if (i + 1) % 32 == 0:
            print(f"  interaccion {i+1}/{n_inter}  "
                  f"(acc visual {a_ok/max(a_seen,1)*100:.1f}%)")
    total_a = a_seen + a_rej
    print(f"  Fase A: {total_a} imagenes · routing visual "
          f"{a_ok/max(a_seen,1)*100:.1f}% · rechazo "
          f"{a_rej/max(total_a,1)*100:.1f}%")
    print(f"  mem_dir_R counts: {tme.mem_dir_R.agent_counts.tolist()}  "
          f"entropia: {tme.mem_dir_R.entropy():.3f} bits")

    print("\n--- Fase B: routing por mem_dir_R (B1) sobre test ---")
    b_ok = b_rej = b_total = 0
    evoke_hits = evoke_tried = 0
    sample_rows = []
    for cls in CLASSES:
        for j, p in enumerate(splits[cls]["test"]):
            z = image_to_latent(p, encoder)
            z_q = quantize_latent_global(z, g_min, g_max, Q_IMG)
            b_total += 1
            agg = tme.mem_dir_R.predict_normalized(z_q, mode="linear")
            if agg.sum() == 0:
                b_rej += 1
                continue
            dest = CLASSES[int(np.argmax(agg))]
            if dest == cls:
                b_ok += 1
            if j < N_EVOKE:
                evoke_tried += 1
                labels = evoke_labels(agents[dest], z_q, all_vecs)
                hit = any(w in vocab_by_cls[cls] for w in labels)
                evoke_hits += int(hit)
                if j < 3:
                    sample_rows.append((cls, dest, labels, hit))

    acc_b = b_ok / max(b_total, 1)
    rej_b = b_rej / max(b_total, 1)
    evoke_rate = evoke_hits / max(evoke_tried, 1)
    print(f"  Routing test: {b_ok}/{b_total} = {acc_b*100:.1f}%  "
          f"(rechazo {rej_b*100:.1f}%)")
    print(f"  Evocacion top-3 domain-hit: {evoke_hits}/{evoke_tried} "
          f"= {evoke_rate*100:.1f}%")
    print("\n  Muestras (clase real -> ruteado · labels evocados):")
    for cls, dest, labels, hit in sample_rows:
        mark = "OK" if hit else "X "
        print(f"    {mark} {cls:>6} -> {dest:<6} · {labels}")

    import pickle
    with open(MODELS_DIR / "tme.pkl", "wb") as f:
        pickle.dump(tme, f)
    print("\n  TME actualizado (mem_dir_R entrenado) -> tme.pkl")

    print("\nEtapa 7 COMPLETADA.")
    return {"visual_early_acc": a_ok / max(a_seen, 1),
            "routing_test_acc": acc_b, "routing_test_rej": rej_b,
            "evoke_top3_hit": evoke_rate}


if __name__ == "__main__":
    run()
