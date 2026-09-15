"""
Experimento 9 — Pérdida de un miembro.

Tesis (Russell, 1910): el especialista conoce su dominio por familiaridad
(vivió las instancias); los demás lo conocen por descripción (presenciaron
que él ganaba y guardaron una envolvente de qué ganaba). La descripción
puede ubicar y rutear, pero no reemplaza a la familiaridad.

Protocolo: se quita un agente k del grupo y las consultas de su dominio
entran por un sobreviviente. El directorio sigue señalando a k (el índice no
se pierde con el miembro). El grupo puede responder de tres maneras:

  rechazo       sabe que k sabía y que k no está: no contesta.
  sustitución   el mejor sobreviviente según el directorio responde con su
                propio contenido (recall_from_left de la pista).
  descripción   un sobreviviente responde con lo que presenció de k: la
                lectura inversa de su directorio (recall_domain(k)).

Referencia con el miembro presente: vivido, recall_from_left del especialista.

Se mide, en el hemisferio texto -> imagen (consultas del banco de 8 clases,
respuesta = latente decodificado) y en el hemisferio imagen -> texto (imágenes
de test, respuesta = etiquetas evocadas):
  - si responde, y si la respuesta es de la clase perdida (clasificador y
    vecino real más cercano);
  - fidelidad: distancia a la instancia real más cercana del dominio perdido;
  - dependencia de la pista: dispersión entre consultas distintas contra
    dispersión entre repeticiones de la misma consulta. La familiaridad
    responde a la pista; la descripción es la misma para cualquier pista.

Uso:  python run_experiment9_member_loss.py [--quick] [--text] [--image] [--figures]
"""
import argparse
import contextlib
import csv
import io
import json
import pickle
import random
import sys
import time
from pathlib import Path

import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from quantizer import quantize_binary
from stage5_fill import N_FILL, quantize_latent_global
from stage6_interaction import (
    CLASSES, AGENT_LIST, MODELS_DIR, DEVICE, M_LABEL, P_LATENT, Q_LATENT,
    get_nlp, tokenize_query, get_fasttext_vector, prevectorize,
    load_all_vectors,
)
from stage7_bidirectional import load_global_stats, evoke_labels, XI_VISUAL

OUT_DIR = ROOT / "results" / "experimento9"
DATA_DIR = ROOT / "data" / "eth80"
LATENT_CACHE = ROOT / "results" / "experimento7" / "latents_cache.json"

K = len(AGENT_LIST)
SEED = 42
REPS = 3                 # repeticiones por consulta (el recall muestrea)
REPS_IMG = 1             # la evocacion de etiquetas tarda ~20 s por llamada
N_IMG_TEST = 10          # imágenes de test por clase (las del caché de exp7)
POLICIES = ("vivido", "sustitucion", "descripcion")

DOMAIN_COLOR = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60",
                "cow": "#8e44ad", "cup": "#c9760a", "dog": "#16a085",
                "pear": "#7d8f22", "tomato": "#c0392b"}
POLICY_COLOR = {"vivido": "#27ae60", "sustitucion": "#c9760a",
                "descripcion": "#2980b9", "rechazo": "#7f8c8d"}

plt.rcParams.update({"figure.dpi": 300, "savefig.dpi": 300,
                     "font.family": "DejaVu Sans", "font.size": 10})


# ---------- carga ----------

def load_agent(name):
    with open(MODELS_DIR / f"agent_{name}.pkl", "rb") as f:
        return pickle.load(f)


def load_decoder():
    from stage2_encoder import Decoder
    dec = Decoder().to(DEVICE)
    dec.load_state_dict(torch.load(MODELS_DIR / "decoder.pt", map_location=DEVICE))
    dec.eval()
    return dec


def load_classifier():
    from stage2_encoder import Classifier
    clf = Classifier().to(DEVICE)
    clf.load_state_dict(torch.load(MODELS_DIR / "classifier.pt", map_location=DEVICE))
    clf.eval()
    return clf


def dequantize_latent(z_q, g_min, g_max):
    return ((np.asarray(z_q, dtype=float) / (Q_LATENT - 1))
            * (g_max - g_min) + g_min).astype(np.float32)


def decode_image(z, decoder):
    with torch.no_grad():
        img = decoder(torch.tensor(z).unsqueeze(0).to(DEVICE))[0].clamp(0, 1)
    return img.cpu().permute(1, 2, 0).numpy()


def load_bank(nlp, vectors, per_class=None):
    """Banco de 8 clases (eval_bank), tokenizado y cuantizado a 16 niveles."""
    from eval_bank import ALL_QUERIES, GROUND_TRUTH
    pairs = list(zip(ALL_QUERIES, GROUND_TRUTH))
    if per_class is not None:
        kept, seen = [], {c: 0 for c in CLASSES}
        for q, t in pairs:
            if seen[t] < per_class:
                kept.append((q, t)); seen[t] += 1
        pairs = kept
    tokens = set()
    for q, _ in pairs:
        tokens.update(tokenize_query(q, nlp))
    prevectorize(vectors, tokens, allow_fallback=False)
    bank = []
    for q, t in pairs:
        vqs = []
        for tok in tokenize_query(q, nlp):
            v = get_fasttext_vector(tok, vectors, allow_fallback=False)
            if v is not None:
                vqs.append((tok, quantize_binary(np.asarray(v, dtype=np.float32),
                                                 M_LABEL)))
        bank.append({"query": q, "truth": t, "tidx": AGENT_LIST.index(t),
                     "cues": vqs})
    return bank


def load_test_latents(g_min, g_max, per_class=N_IMG_TEST):
    cache = json.loads(LATENT_CACHE.read_text())
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    out = []
    for ci, cls in enumerate(CLASSES):
        paths = [p for p in splits[cls]["test"] if p in cache][:per_class]
        for p in paths:
            out.append((p, quantize_latent_global(np.array(cache[p]), g_min,
                                                  g_max, Q_LATENT), ci))
    return out


# ---------- juez ----------

class Judge:
    def __init__(self, clf, g_min, g_max):
        self.clf, self.g_min, self.g_max = clf, g_min, g_max
        self.instances = {c: np.array(json.loads(
            (MODELS_DIR / f"instance_latents_{c}.json").read_text()),
            dtype=np.float32) for c in CLASSES}
        self.all_inst = np.concatenate([self.instances[c] for c in CLASSES])
        self.all_cls = np.concatenate([[ci] * len(self.instances[c])
                                       for ci, c in enumerate(CLASSES)])

    def classify(self, z):
        with torch.no_grad():
            return int(self.clf(torch.tensor(z).unsqueeze(0).to(DEVICE)).argmax(1))

    def judge(self, z_q, target):
        """Clase del clasificador, clase del vecino real más cercano y distancia
        a la instancia más cercana del dominio objetivo."""
        z = dequantize_latent(z_q, self.g_min, self.g_max)
        d_all = np.linalg.norm(self.all_inst - z, axis=1)
        j = int(np.argmin(d_all))
        d_t = float(np.linalg.norm(self.instances[CLASSES[target]] - z, axis=1).min())
        return {"clf": self.classify(z), "nn_cls": int(self.all_cls[j]),
                "d_nn_target": d_t, "d_nn_any": float(d_all[j]), "z": z}


# ---------- recalls ----------

def recall_lived(agent, cues):
    """Recall del especialista con la primera pista reconocida (como stage 8)."""
    for tok, v_q in cues:
        with contextlib.redirect_stdout(io.StringIO()):
            z_q, recognized, *_ = agent.mem_dom_H.recall_from_left(v_q)
        if recognized:
            return z_q, tok
    return None, None


def live_levels_lived(agent, cues):
    """Niveles vivos por coordenada del latente en la proyección desde la
    pista de texto: cuánto restringe la pista al dominio."""
    mem = agent.mem_dom_H
    for tok, v_q in cues:
        with contextlib.redirect_stdout(io.StringIO()):
            proj = mem.project(mem.validate(v_q, 0), np.ones(len(v_q)), 0)
        if np.count_nonzero(np.sum(proj, axis=1) == 0) == 0:
            return float((proj > 0).sum(axis=1).mean())
    return float("nan")


def live_levels_description(mdir, k):
    proj = mdir.domain_projection(k)
    return float((proj > 0).sum(axis=1).mean())


def words_from_label_cue(cue_q, all_vecs, top_k=3):
    """Vector de etiqueta cuantizado -> palabras vecinas por coseno (mismo
    diccionario que evoke_labels)."""
    cont = (np.asarray(cue_q, dtype=float) / max(M_LABEL - 1, 1)) * 2.0 - 1.0
    sims = []
    for w, vec in all_vecs.items():
        v = np.array(vec, dtype=np.float32)
        sims.append((w, float(np.dot(cont, v) /
                              (np.linalg.norm(cont) * np.linalg.norm(v) + 1e-8))))
    sims.sort(key=lambda x: -x[1])
    return [w for w, _ in sims[:top_k]]


def spread(zs):
    if len(zs) < 2:
        return float("nan")
    return float(np.mean([np.linalg.norm(zs[i] - zs[j])
                          for i in range(len(zs)) for j in range(i + 1, len(zs))]))


# ---------- hemisferio texto -> imagen ----------

def run_text(agents, bank, judge, decoder, quick=False):
    print("\nHemisferio texto -> imagen")
    rows, samples = [], {}
    t0 = time.time()
    for k, lost in enumerate(CLASSES):
        survivor = agents[CLASSES[(k + 1) % K]]
        queries = [it for it in bank if it["tidx"] == k and it["cues"]]
        n_routed_k = n_rej = n_other = 0
        per_query = {p: [] for p in POLICIES}
        for it in queries:
            with contextlib.redirect_stdout(io.StringIO()):
                dest, scores = survivor.mem_dir.route_multi(
                    [v for _, v in it["cues"]], mode="linear")
            if dest < 0:
                n_rej += 1
                continue
            if dest != k:
                n_other += 1
                continue
            n_routed_k += 1
            # sustitución: el mejor sobreviviente según el directorio
            s = scores.copy(); s[k] = 0.0
            sub_idx = int(np.argmax(s)) if s.sum() > 0 else -1

            for policy in POLICIES:
                zs = []
                for r in range(REPS):
                    if policy == "vivido":
                        z_q, tok = recall_lived(agents[lost], it["cues"])
                    elif policy == "sustitucion":
                        z_q, tok = (recall_lived(agents[CLASSES[sub_idx]], it["cues"])
                                    if sub_idx >= 0 else (None, None))
                    else:
                        z_q, ok = survivor.mem_dir_R.recall_domain(k)
                        z_q, tok = (z_q if ok else None), None
                    row = {"perdido": lost, "query": it["query"], "politica": policy,
                           "rep": r, "responde": z_q is not None,
                           "agente_responde": (lost if policy == "vivido" else
                                               CLASSES[sub_idx] if policy == "sustitucion" and sub_idx >= 0
                                               else survivor.name)}
                    if z_q is not None:
                        j = judge.judge(z_q, k)
                        zs.append(j["z"])
                        row.update({"clf_ok": j["clf"] == k, "nn_ok": j["nn_cls"] == k,
                                    "clf": CLASSES[j["clf"]], "nn": CLASSES[j["nn_cls"]],
                                    "d_nn_perdido": j["d_nn_target"],
                                    "d_nn_cualquiera": j["d_nn_any"]})
                        if r == 0 and (lost, policy) not in samples:
                            samples[(lost, policy)] = (it["query"], j["z"], row)
                    rows.append(row)
                if zs:
                    per_query[policy].append(np.stack(zs))
                    rows[-1]["disp_intra"] = spread(zs)
                    rows[-1]["niveles_vivos"] = (
                        live_levels_lived(agents[lost], it["cues"]) if policy == "vivido"
                        else live_levels_description(survivor.mem_dir_R, k) if policy == "descripcion"
                        else live_levels_lived(agents[CLASSES[sub_idx]], it["cues"]))
        # dependencia de la pista: dispersión entre consultas distintas (un
        # sorteo por consulta) contra dispersión entre sorteos de la misma
        # consulta; y razón F = var(medias por consulta) / (var dentro / REPS),
        # con las dos varianzas insesgadas (Bessel: G-1 y REPS-1). Bajo el
        # nulo de independencia de la pista, E[F] = 1.
        dep = {}
        for p in POLICIES:
            groups = [g for g in per_query[p] if len(g) > 1]
            intra = [r["disp_intra"] for r in rows
                     if r["perdido"] == lost and r["politica"] == p and "disp_intra" in r]
            entre = spread([g[0] for g in groups])
            if len(groups) > 1:
                means = np.stack([g.mean(axis=0) for g in groups])
                G = len(groups)
                var_b = float(((means - means.mean(axis=0)) ** 2).sum(axis=1).sum() / (G - 1))
                var_w = float(np.mean([((g - g.mean(axis=0)) ** 2).sum(axis=1).sum() / (len(g) - 1)
                                       for g in groups]))
                F = var_b / (var_w / REPS) if var_w > 0 else float("nan")
            else:
                F = float("nan")
            dep[p] = {"entre_consultas": entre,
                      "dentro_consulta": float(np.nanmean(intra)) if intra else float("nan"),
                      "F_dependencia": F}
        print(f"  {lost:>7}: {len(queries)} consultas · ruteadas a {lost} {n_routed_k}"
              f" · a otro {n_other} · rechazadas {n_rej}  "
              + "  ".join(f"{p[:4]} entre {dep[p]['entre_consultas']:.1f}/dentro "
                          f"{dep[p]['dentro_consulta']:.1f}" for p in POLICIES)
              + f"  ({time.time()-t0:.0f}s)", flush=True)
        rows.append({"perdido": lost, "query": "__ruteo__", "politica": "ruteo",
                     "rep": 0, "consultas": len(queries), "a_perdido": n_routed_k,
                     "a_otro": n_other, "rechazadas": n_rej,
                     "dependencia": json.dumps(dep)})
    return rows, samples


# ---------- hemisferio imagen -> texto ----------

def run_image(agents, test_latents, judge, all_vecs, vocab_by_cls):
    print("\nHemisferio imagen -> texto")
    rows = []
    t0 = time.time()
    for k, lost in enumerate(CLASSES):
        survivor = agents[CLASSES[(k + 1) % K]]
        imgs = [(p, z, c) for p, z, c in test_latents if c == k]
        n_routed_k = n_rej = n_other = 0
        for p, z_q, _ in imgs:
            with contextlib.redirect_stdout(io.StringIO()):
                dest = survivor.mem_dir_R.route(z_q, mode="linear", xi=XI_VISUAL)
            if dest < 0:
                n_rej += 1; continue
            if dest != k:
                n_other += 1; continue
            n_routed_k += 1
            with contextlib.redirect_stdout(io.StringIO()):
                s = survivor.mem_dir_R.predict_tolerant(z_q, xi=XI_VISUAL)
            s[k] = 0.0
            sub_idx = int(np.argmax(s)) if s.sum() > 0 else -1
            for policy in POLICIES:
                for r in range(REPS_IMG):
                    if policy == "vivido":
                        words = evoke_labels(agents[lost], z_q, all_vecs)
                    elif policy == "sustitucion":
                        words = (evoke_labels(agents[CLASSES[sub_idx]], z_q, all_vecs)
                                 if sub_idx >= 0 else [])
                    else:
                        cue_q, ok = survivor.mem_dir.recall_domain(k)
                        words = words_from_label_cue(cue_q, all_vecs) if ok else []
                    rows.append({"perdido": lost, "imagen": Path(p).name,
                                 "politica": policy, "rep": r,
                                 "responde": bool(words),
                                 "hit_perdido": any(w in vocab_by_cls[lost] for w in words),
                                 "hit_sustituto": (any(w in vocab_by_cls[CLASSES[sub_idx]]
                                                       for w in words) if sub_idx >= 0 else False),
                                 "palabras": " ".join(words)})
        res = {p: [r for r in rows if r["perdido"] == lost and r["politica"] == p]
               for p in POLICIES}
        print(f"  {lost:>7}: {len(imgs)} imágenes · ruteadas a {lost} {n_routed_k}"
              f" · a otro {n_other} · rechazadas {n_rej}  "
              + "  ".join(f"{p[:4]} resp {np.mean([r['responde'] for r in res[p]]):.2f}"
                          f" hit {np.mean([r['hit_perdido'] for r in res[p]]):.2f}"
                          for p in POLICIES)
              + f"  ({time.time()-t0:.0f}s)", flush=True)
        rows.append({"perdido": lost, "imagen": "__ruteo__", "politica": "ruteo",
                     "rep": 0, "consultas": len(imgs), "a_perdido": n_routed_k,
                     "a_otro": n_other, "rechazadas": n_rej})
    return rows


# ---------- resumen y figuras ----------

def summarize_text(rows):
    out = {}
    for p in POLICIES:
        rs = [r for r in rows if r["politica"] == p]
        ans = [r for r in rs if r["responde"]]
        out[p] = {
            "responde": np.mean([r["responde"] for r in rs]) if rs else float("nan"),
            "clase_clf": np.mean([r["clf_ok"] for r in ans]) if ans else float("nan"),
            "clase_nn": np.mean([r["nn_ok"] for r in ans]) if ans else float("nan"),
            "d_nn_perdido": float(np.mean([r["d_nn_perdido"] for r in ans])) if ans else float("nan"),
            "d_nn_cualquiera": float(np.mean([r["d_nn_cualquiera"] for r in ans])) if ans else float("nan"),
            "n": len(rs),
        }
    deps = {p: {"entre": [], "dentro": [], "F": []} for p in POLICIES}
    ruteo = {"consultas": 0, "a_perdido": 0, "a_otro": 0, "rechazadas": 0}
    for r in rows:
        if r["politica"] == "ruteo":
            for key in ruteo:
                ruteo[key] += r[key]
            d = json.loads(r["dependencia"])
            for p in POLICIES:
                deps[p]["entre"].append(d[p]["entre_consultas"])
                deps[p]["dentro"].append(d[p]["dentro_consulta"])
                deps[p]["F"].append(d[p]["F_dependencia"])
    for p in POLICIES:
        e, d = np.nanmean(deps[p]["entre"]), np.nanmean(deps[p]["dentro"])
        out[p]["disp_entre_consultas"] = float(e)
        out[p]["disp_dentro_consulta"] = float(d)
        out[p]["dependencia_de_la_pista"] = float(e / d) if d > 0 else float("nan")
        out[p]["F_dependencia"] = float(np.nanmean(deps[p]["F"]))
        niv = [r["niveles_vivos"] for r in rows
               if r["politica"] == p and "niveles_vivos" in r and not np.isnan(r["niveles_vivos"])]
        out[p]["niveles_vivos_por_coordenada"] = float(np.mean(niv)) if niv else float("nan")
    out["ruteo"] = ruteo
    return out


def summarize_image(rows):
    out = {}
    for p in POLICIES:
        rs = [r for r in rows if r["politica"] == p]
        ans = [r for r in rs if r["responde"]]
        out[p] = {"responde": np.mean([r["responde"] for r in rs]) if rs else float("nan"),
                  "hit_perdido": np.mean([r["hit_perdido"] for r in ans]) if ans else float("nan"),
                  "hit_sustituto": np.mean([r["hit_sustituto"] for r in ans]) if ans else float("nan"),
                  "n": len(rs)}
    ruteo = {"consultas": 0, "a_perdido": 0, "a_otro": 0, "rechazadas": 0}
    for r in rows:
        if r["politica"] == "ruteo":
            for key in ruteo:
                ruteo[key] += r[key]
    out["ruteo"] = ruteo
    return out


def figure_answers(samples, judge, decoder):
    """Por clase perdida: imagen real, y la respuesta del grupo bajo cada
    política a la misma consulta."""
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    cols = ["ETH-80\n(real)", "vivido\n(miembro presente)",
            "sustitución\n(otro contenido)", "descripción\n(directorio)"]
    fig, axes = plt.subplots(K, 4, figsize=(9, 2.1 * K))
    for ci, cls in enumerate(CLASSES):
        panels = [np.asarray(Image.open(splits[cls]["train"][0]).convert("RGB")
                             .resize((128, 128)), dtype=np.float32) / 255.0]
        labels = [""]
        for p in POLICIES:
            s = samples.get((cls, p))
            if s is None:
                panels.append(None); labels.append("no responde"); continue
            q, z, row = s
            panels.append(decode_image(z, decoder))
            labels.append(f"{row['agente_responde']} · juez: {row['clf']}"
                          f" · d={row['d_nn_perdido']:.1f}")
        for k, (ax, img) in enumerate(zip(axes[ci], panels)):
            if img is not None:
                ax.imshow(img)
            else:
                ax.set_facecolor("#ecf0f1")
                ax.text(0.5, 0.5, "rechazado", ha="center", va="center",
                        fontsize=9, color="#7f8c8d", transform=ax.transAxes)
            ax.set_xticks([]); ax.set_yticks([])
            for sp in ax.spines.values():
                sp.set_edgecolor(DOMAIN_COLOR[cls] if k else "#888")
                sp.set_linewidth(1.6 if k else 0.8)
            if ci == 0:
                ax.set_title(cols[k], fontsize=9, pad=6)
            if labels[k]:
                ax.set_xlabel(labels[k], fontsize=7)
        q = samples.get((cls, "vivido"), (None,))[0] or samples.get((cls, "descripcion"), ("",))[0]
        axes[ci, 0].set_ylabel(f"{cls.upper()}\n«{q}»", fontsize=8, fontweight="bold",
                               color=DOMAIN_COLOR[cls], labelpad=8)
    fig.suptitle("Pérdida de un miembro: la misma consulta respondida sin el especialista",
                 fontsize=12, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.985])
    path = OUT_DIR / "fig1_respuestas.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> {path}")


def figure_summary(st, si):
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    x = np.arange(len(POLICIES))
    names = ["vivido", "sustitución", "descripción"]
    colors = [POLICY_COLOR[p] for p in POLICIES]

    ax = axes[0]
    ax.bar(x - 0.2, [st[p]["responde"] for p in POLICIES], 0.4, color=colors, alpha=0.45,
           label="responde")
    ax.bar(x + 0.2, [st[p]["responde"] * st[p]["clase_nn"] for p in POLICIES], 0.4,
           color=colors, label="responde y es de la clase perdida")
    ax.set_xticks(x); ax.set_xticklabels(names)
    ax.set_ylim(0, 1.05); ax.set_title("texto → imagen: responde / acierta")
    ax.legend(fontsize=7, loc="lower left"); ax.grid(axis="y", alpha=0.3)

    ax = axes[1]
    ax.bar(x, [st[p]["d_nn_perdido"] for p in POLICIES], 0.6, color=colors)
    ax.set_xticks(x); ax.set_xticklabels(names)
    ax.set_title("distancia a la instancia real más cercana\ndel dominio perdido")
    ax.grid(axis="y", alpha=0.3)

    ax = axes[2]
    ax.bar(x - 0.2, [st[p]["disp_dentro_consulta"] for p in POLICIES], 0.4,
           color=colors, alpha=0.45, label="misma consulta repetida")
    ax.bar(x + 0.2, [st[p]["disp_entre_consultas"] for p in POLICIES], 0.4,
           color=colors, label="consultas distintas")
    ax.set_xticks(x); ax.set_xticklabels(names)
    ax.set_title("dispersión de la respuesta")
    ax.legend(fontsize=7, loc="upper left"); ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    path = OUT_DIR / "fig2_resumen_texto.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> {path}")

    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    ax.bar(x - 0.2, [si[p]["responde"] for p in POLICIES], 0.4, color=colors, alpha=0.45,
           label="responde")
    ax.bar(x + 0.2, [si[p]["responde"] * si[p]["hit_perdido"] for p in POLICIES], 0.4,
           color=colors, label="alguna etiqueta del dominio perdido")
    ax.set_xticks(x); ax.set_xticklabels(names)
    ax.set_ylim(0, 1.05); ax.set_title("imagen → texto: etiquetas evocadas")
    ax.legend(fontsize=7, loc="lower left"); ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    path = OUT_DIR / "fig3_resumen_imagen.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> {path}")


def write_csv(rows, path):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader(); w.writerows(rows)
    print(f"  -> {path}")


def read_csv(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out = {}
            for k, v in r.items():
                if v is None or v == "":
                    continue
                if v in ("True", "False"):
                    out[k] = v == "True"
                else:
                    try:
                        out[k] = float(v) if k not in ("perdido", "query", "politica",
                                                       "agente_responde", "clf", "nn",
                                                       "imagen", "palabras", "dependencia") else v
                    except ValueError:
                        out[k] = v
            rows.append(out)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="5 consultas y 3 imágenes por clase")
    ap.add_argument("--text", action="store_true", help="hemisferio texto -> imagen")
    ap.add_argument("--image", action="store_true", help="hemisferio imagen -> texto")
    ap.add_argument("--report", action="store_true",
                    help="resumen y figuras a partir de los CSV ya escritos")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    np.random.seed(SEED)
    random.seed(SEED)

    if args.report:
        rows = read_csv(OUT_DIR / "results_text.csv")
        rows_i = read_csv(OUT_DIR / "results_image.csv")
        summary = {"texto_a_imagen": summarize_text(rows),
                   "imagen_a_texto": summarize_image(rows_i)}
        figure_summary(summary["texto_a_imagen"], summary["imagen_a_texto"])
        path = OUT_DIR / "resumen.json"
        path.write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=float))
        print(json.dumps(summary, indent=2, ensure_ascii=False, default=float))
        print(f"  -> {path}")
        return

    print("Cargando agentes, juez y banco...")
    g_min, g_max = load_global_stats()
    agents = {c: load_agent(c) for c in CLASSES}
    judge = Judge(load_classifier(), g_min, g_max)
    decoder = load_decoder()
    nlp = get_nlp()
    vectors = load_all_vectors(nlp)
    all_vecs = {}
    for c in CLASSES:
        all_vecs.update(vectors[c])
    vocab_by_cls = {c: set(vectors[c]) for c in CLASSES}
    tag = "_quick" if args.quick else ""

    if args.text or not args.image:
        bank = load_bank(nlp, vectors, per_class=5 if args.quick else None)
        print(f"  banco: {len(bank)} consultas", flush=True)
        rows, samples = run_text(agents, bank, judge, decoder, quick=args.quick)
        write_csv(rows, OUT_DIR / f"results_text{tag}.csv")
        figure_answers(samples, judge, decoder)
        print(json.dumps(summarize_text(rows), indent=2, ensure_ascii=False, default=float))
    if args.image or not args.text:
        test_latents = load_test_latents(g_min, g_max, 3 if args.quick else N_IMG_TEST)
        print(f"  imágenes de test: {len(test_latents)}", flush=True)
        rows_i = run_image(agents, test_latents, judge, all_vecs, vocab_by_cls)
        write_csv(rows_i, OUT_DIR / f"results_image{tag}.csv")
        print(json.dumps(summarize_image(rows_i), indent=2, ensure_ascii=False, default=float))


if __name__ == "__main__":
    main()
