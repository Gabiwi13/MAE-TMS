"""
Etapa 7 — Hemisferio visual: el directorio de imagenes.

Fase A (interacciones visuales): las imagenes de entrenamiento que no
participaron del llenado (indices [N_FILL:]) entran al grupo por un agente
de entrada, intercaladas por clase. Cada agente puntua la percepcion con su
homo latente (M_dom_R) y la transaccion (latente -> ganador) la registran
el agente de entrada, el ganador y el TME (register_transaction): los
directorios visuales son perspectivales. Solo percepciones reales entran.

Fase B (evaluacion): las imagenes de test entran por un agente no
especialista y rutean con route_transactive (agregado de los directorios
conocidos, encadenado si nadie tiene soporte); el agente destino evoca
labels con recall_from_right modulado por los pesos de M_dom_R. La metrica
de evocacion es top-3 domain hit.
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
    register_transaction, route_transactive,
)

DATA_DIR = ROOT / "data" / "eth80"
N, M_LABEL, P, Q_IMG = 300, 16, 64, 32
N_EVOKE = 15
# Tolerancia del ruteo visual (directorio mem_dir_R). Con directorios
# identicos y completos xi=2 daba +1.7 pts; con directorios perspectivales
# los huecos tolerados se definen sobre el soporte de todos los agentes del
# directorio y dependen de lo que presenciaron los demas (exp10), asi que la
# lectura vuelve a ser estricta.
XI_VISUAL = 0
# Umbral de energía del latente (exp14): el encoder colapsa las entradas sin
# estructura (gris medio, desenfoque, contraste nulo) cerca del origen, dentro
# de la envolvente de horse. Nada más débil que lo registrado entra a memoria.
LATENT_ENERGY_MARGIN = 0.1
ENERGY_PATH = MODELS_DIR / "latent_energy_threshold.json"

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


def latent_energy_threshold() -> float:
    """Mínimo de la norma sobre los originales del llenado, con margen."""
    if ENERGY_PATH.exists():
        return float(json.loads(ENERGY_PATH.read_text())["tau"])
    from stage5_fill import FILL_AUGMENT, FILL_VARIANTS
    step = FILL_VARIANTS if FILL_AUGMENT else 1
    norms = np.concatenate([
        np.linalg.norm(np.asarray(json.loads((MODELS_DIR / f"instance_latents_{c}.json").read_text()),
                                  dtype=np.float32)[::step], axis=1) for c in CLASSES])
    tau = float(norms.min() * (1 - LATENT_ENERGY_MARGIN))
    ENERGY_PATH.write_text(json.dumps({"tau": tau, "min_norma_llenado": float(norms.min()),
                                       "margen": LATENT_ENERGY_MARGIN, "n": int(norms.size)}))
    return tau


def latent_has_energy(z: np.ndarray, tau: float) -> bool:
    return float(np.linalg.norm(z)) >= tau


def image_to_latent(img_path: str, encoder) -> np.ndarray:
    img = Image.open(img_path).convert("RGB").resize((128, 128))
    t = IMG_TRANSFORM(img).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        return encoder(t).cpu().numpy()[0]


def image_variants_to_latents(img_path: str, encoder) -> np.ndarray:
    """Latentes de la imagen y sus variantes (la primera fila es la original)."""
    from stage5_fill import augment_variants, FILL_AUGMENT
    img = Image.open(img_path).convert("RGB").resize((128, 128))
    variants = augment_variants(img) if FILL_AUGMENT else [img]
    t = torch.stack([IMG_TRANSFORM(v) for v in variants]).to(DEVICE)
    with torch.no_grad():
        return encoder(t).cpu().numpy()


def recognize_gated_right(agent, z_q: np.ndarray) -> float:
    """Score visual PURO de un agente: reconocimiento homo del dominio latente
    (mem_dom_R) — containment + activacion media de los pesos por caracteristica.

    Antes proyectaba por M_dom_H (hetero), lo que ACOPLABA el reconocimiento
    visual a la cuantizacion de las etiquetas: al pasar a magnitud, el lado
    etiqueta de M_dom_H quedaba disperso y el gate de containment rechazaba de
    mas. El reconocimiento visual debe depender solo del espacio latente, que usa
    su propia cuantizacion (quantize_latent_global), independiente de las labels.
    Sigue siendo una operacion de la MAE (recog_weights = R[i, z_q[i]] con gate
    por containment); no hay bypass.
    """
    w = agent.mem_dom_R.recog_weights(z_q)     # w_i = R[i, z_q[i]] (homo latente)
    if np.count_nonzero(w == 0) > 0:           # containment estricto (xi=0)
        return 0.0
    return float(np.mean(w))


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
    # Los directorios visuales se forman aquí y solo aquí: si los pickles ya
    # traen una fase A (re-corrida), se parte de cero para no registrarla dos veces.
    from associative_memory import DirectoryMemory
    tme.mem_dir_R = DirectoryMemory(P, Q_IMG, len(AGENT_LIST))
    for cls in CLASSES:
        agents[cls].mem_dir_R = DirectoryMemory(P, Q_IMG, len(AGENT_LIST))
    label_vecs = load_all_vectors()
    vocab_by_cls = {cls: set(label_vecs[cls].keys()) for cls in CLASSES}
    all_vecs = {}
    for cls in CLASSES:
        all_vecs.update(label_vecs[cls])

    tau = latent_energy_threshold()
    print(f"Umbral de energía del latente: {tau:.2f}")

    print(f"\n--- Fase A: interacciones visuales (train[{N_FILL}:]) ---")
    pools = {cls: splits[cls]["train"][N_FILL:] for cls in CLASSES}
    n_inter = max(len(p) for p in pools.values())
    a_ok = a_seen = a_rej = a_deg = 0
    rng = np.random.RandomState(42)   # agente de entrada por percepcion
    for i in range(n_inter):
        for cls in CLASSES:
            if i >= len(pools[cls]):
                continue
            # La percepción decide ganador y energía con la imagen original;
            # sus variantes se registran con el mismo ganador (exp13).
            zs = image_variants_to_latents(pools[cls][i], encoder)
            if not latent_has_energy(zs[0], tau):
                a_deg += 1
                continue
            z_q = quantize_latent_global(zs[0], g_min, g_max, Q_IMG)
            scores = {c: recognize_gated_right(agents[c], z_q)
                      for c in CLASSES}
            if sum(scores.values()) == 0:
                a_rej += 1
                continue
            winner = max(scores, key=scores.get)
            widx = AGENT_LIST.index(winner)
            entry = AGENT_LIST[int(rng.randint(len(AGENT_LIST)))]
            with contextlib.redirect_stdout(io.StringIO()):
                # Registran quien recibio la percepcion, quien la gano y el TME.
                for z_v in zs:
                    register_transaction(entry, widx, agents, tme,
                                         quantize_latent_global(z_v, g_min, g_max, Q_IMG), "image")
            a_seen += 1
            a_ok += int(winner == cls)
        if (i + 1) % 32 == 0:
            print(f"  interaccion {i+1}/{n_inter}  "
                  f"(acc visual {a_ok/max(a_seen,1)*100:.1f}%)")
    total_a = a_seen + a_rej + a_deg
    print(f"  Fase A: {total_a} imagenes · routing visual "
          f"{a_ok/max(a_seen,1)*100:.1f}% · rechazo "
          f"{a_rej/max(total_a,1)*100:.1f}% · sin energía (antes de la memoria) {a_deg}")
    print(f"  TME mem_dir_R (registro completo): counts={tme.mem_dir_R.agent_counts.tolist()}"
          f"  entropia {tme.mem_dir_R.entropy():.3f} bits")
    for cls in CLASSES:
        agents[cls].mem_dir_R.print_stats(f"{cls} visual")

    print("\n--- Fase B: routing transactivo por mem_dir_R per-agente sobre test ---")
    b_ok = b_rej = b_total = b_deg = 0
    hops_total = consulted_total = 0
    evoke_hits = evoke_tried = 0
    sample_rows = []
    for ci, cls in enumerate(CLASSES):
        for j, p in enumerate(splits[cls]["test"]):
            z = image_to_latent(p, encoder)
            b_total += 1
            if not latent_has_energy(z, tau):
                b_deg += 1
                b_rej += 1
                continue
            z_q = quantize_latent_global(z, g_min, g_max, Q_IMG)
            # La entrada es a proposito un agente no especialista: agrega los
            # directorios visuales que conoce y encadena si hace falta.
            entry = CLASSES[(ci + 1) % len(CLASSES)]
            widx, _scores, consulted, hops = route_transactive(
                entry, agents, z_q, modality="image", xi=XI_VISUAL)
            hops_total += hops
            consulted_total += len(consulted)
            if widx < 0:
                b_rej += 1
                continue
            dest = CLASSES[widx]
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
          f"(rechazo {rej_b*100:.1f}%, de las cuales {b_deg} sin energía antes de la memoria)  "
          f"directorios consultados "
          f"{consulted_total/max(b_total,1):.2f}  saltos {hops_total/max(b_total,1):.2f}")
    print(f"  Evocacion top-3 domain-hit: {evoke_hits}/{evoke_tried} "
          f"= {evoke_rate*100:.1f}%")
    print("\n  Muestras (clase real -> ruteado · labels evocados):")
    for cls, dest, labels, hit in sample_rows:
        mark = "OK" if hit else "X "
        print(f"    {mark} {cls:>6} -> {dest:<6} · {labels}")

    import pickle
    with open(MODELS_DIR / "tme.pkl", "wb") as f:
        pickle.dump(tme, f)
    for cls in CLASSES:
        with open(MODELS_DIR / f"agent_{cls}.pkl", "wb") as f:
            pickle.dump(agents[cls], f)
    print("\n  TME + agentes actualizados (mem_dir_R perspectival por agente) -> *.pkl")

    print("\nEtapa 7 COMPLETADA.")
    return {"visual_early_acc": a_ok / max(a_seen, 1),
            "routing_test_acc": acc_b, "routing_test_rej": rej_b,
            "evoke_top3_hit": evoke_rate}


if __name__ == "__main__":
    run()
