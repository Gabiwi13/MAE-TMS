"""
Demo industrial con texto: CLIP ViT-B/16 (OpenAI) como percepción compartida.
Diseño fijado en propuesta_industrial_clip.md.

  T  oración -> pieza por route_transactive (cruda y con la brecha de modalidad corregida)
  Z  detección solo con texto: agentes normal/anómalo llenos de oraciones
  N  especialista de normales (como G2) + agente de texto anómalo
Imágenes y registro del demo industrial (results/industrial/cache).

Uso:
  python run_industrial_clip.py --clip C:/Users/aq99l/Datasets/CLIP_ViT-B-16_openai/open_clip_model.safetensors
  python run_industrial_clip.py --report-only
"""
import argparse
import contextlib
import io
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_industrial_demo as ind  # noqa: E402
import run_medico_demo as demo  # noqa: E402
import stage6_interaction as s6  # noqa: E402
from associative_memory import HomoAssociativeMemory  # noqa: E402
from stage5_fill import augment_variants  # noqa: E402

OUT = ROOT / "results" / "industrial_clip"
CACHE = OUT / "cache"            # fuera de git
PIECES, N_FILL, Q, PAD = ind.PIECES, ind.N_FILL, ind.Q, ind.PAD
DEV = demo.DEV
NAMES = {"candle": "candle", "capsules": "capsule", "cashew": "cashew", "chewinggum": "chewing gum",
         "fryum": "fryum", "macaroni1": "macaroni", "macaroni2": "macaroni", "pcb1": "printed circuit board",
         "pcb2": "printed circuit board", "pcb3": "printed circuit board", "pcb4": "printed circuit board",
         "pipe_fryum": "pipe fryum"}
NORMAL_STATES = ["{}", "flawless {}", "perfect {}", "unblemished {}", "{} without flaw",
                 "{} without defect", "{} without damage"]
ANOMAL_STATES = ["damaged {}", "{} with flaw", "{} with defect", "{} with damage"]
TEMPLATES = ["a cropped photo of the {}.", "a cropped photo of a {}.", "a close-up photo of a {}.",
             "a close-up photo of the {}.", "a bright photo of a {}.", "a bright photo of the {}.",
             "a dark photo of the {}.", "a dark photo of a {}.", "a jpeg corrupted photo of a {}.",
             "a jpeg corrupted photo of the {}.", "a blurry photo of the {}.", "a blurry photo of a {}.",
             "a photo of a {}.", "a photo of the {}.", "a photo of a small {}.", "a photo of the small {}.",
             "a photo of a large {}.", "a photo of the large {}.", "a photo of the {} for visual inspection.",
             "a photo of a {} for visual inspection.", "a photo of the {} for anomaly detection.",
             "a photo of a {} for anomaly detection."]
TF = transforms.Compose([transforms.ToTensor(),
                         transforms.Normalize((0.48145466, 0.4578275, 0.40821073),
                                              (0.26862954, 0.26130258, 0.27577711))])


def sentences(name, states):
    return [t.format(s.format(name)) for s in states for t in TEMPLATES]


def defect_words(p):
    return sorted({w.strip().strip('"') for t in ind.imgs()[f"testtipo_{p}"] if t for w in t.split(",") if w.strip().strip('"')})


def unit(X):
    X = np.asarray(X, dtype=np.float64)
    return X / np.linalg.norm(X, axis=-1, keepdims=True)


# ---------- CLIP ----------

def clip_model(path):
    import open_clip
    m, _, _ = open_clip.create_model_and_transforms("ViT-B-16", pretrained=path)
    return m.to(DEV).eval(), open_clip.get_tokenizer("ViT-B-16")


def enc_images(m, arr, variants=False):
    out = []
    step = 16 if variants else 128
    with torch.no_grad():
        for i in range(0, len(arr), step):
            pil = [Image.fromarray(a) for a in arr[i:i + step]]
            if variants:
                pil = [v for im in pil for v in augment_variants(im)]
            f = m.encode_image(torch.stack([TF(p) for p in pil]).to(DEV)).float().cpu().numpy()
            out.append(f.reshape(-1, 16, f.shape[-1]) if variants else f)
    return unit(np.concatenate(out)).astype(np.float32)


def enc_text(m, tok, texts):
    with torch.no_grad():
        return unit(m.encode_text(tok(texts).to(DEV)).float().cpu().numpy()).astype(np.float32)


def features(clip_path):
    path = CACHE / "clip.npz"
    if path.exists():
        return dict(np.load(path, allow_pickle=False))
    m, tok = clip_model(clip_path)
    out = {}
    for p in PIECES:
        out[f"reg_{p}"] = enc_images(m, ind.imgs()[f"reg_{p}"], variants=True)
        out[f"test_{p}"] = enc_images(m, ind.imgs()[f"test_{p}"])
        out[f"tn_{p}"] = enc_text(m, tok, sentences(NAMES[p], NORMAL_STATES))
        out[f"ta_{p}"] = enc_text(m, tok, sentences(NAMES[p], ANOMAL_STATES))
        out[f"tv_{p}"] = enc_text(m, tok, [t.format(f"{NAMES[p]} with {w}") for w in defect_words(p) for t in TEMPLATES])
        print(f"  CLIP {p} listo", flush=True)
    np.savez(path, **out)
    return out


# ---------- memoria ----------

class Agent:
    """Contenido de un agente: memoria homo con cuantización dada."""

    def __init__(self, Z, g):
        self.g = g
        self.mem = HomoAssociativeMemory(64, Q)
        for z in np.asarray(Z).reshape(-1, 64):
            self.mem.register(self.q(z))

    def q(self, z):
        return demo.quantize_latent_global(np.asarray(z, dtype=np.float32), *self.g, Q)

    def weights(self, z):
        return self.mem.recog_weights(self.q(z))

    def score(self, z):
        """recognize_gated_right: 0 si alguna coordenada no está contenida."""
        w = self.weights(z)
        return 0.0 if np.any(w == 0) else float(w.mean())

    def uncovered(self, z):
        return int(np.count_nonzero(self.weights(z) == 0))


def grid(Z):
    Z = np.asarray(Z).reshape(-1, 64)
    lo, hi = Z.min(0), Z.max(0)
    return lo - PAD * (hi - lo), hi + PAD * (hi - lo)


def cpe(x, tn, ta):
    """p(anómalo) de CLIP cero ejemplos con la ensamble de prompts."""
    c = np.stack([x @ unit(tn.mean(0)), x @ unit(ta.mean(0))], 1) * 100
    c = np.exp(c - c.max(1, keepdims=True))
    return c[:, 1] / c.sum(1)


# ---------- partes ----------

def part_T(F):
    P = ind.pca(np.concatenate([F[f"reg_{p}"][:, 0] for p in PIECES]))
    reg = {p: ind.proj(P, F[f"reg_{p}"]) for p in PIECES}
    L1 = demo.Level("clip_nivel1", PIECES, None, {p: reg[p][:N_FILL] for p in PIECES},
                    {p: reg[p][N_FILL:] for p in PIECES})
    mu_img = np.concatenate([F[f"reg_{p}"][:N_FILL, 0] for p in PIECES]).mean(0)
    mu_txt = np.concatenate([F[f"tn_{p}"] for p in PIECES]).mean(0)
    proto = unit(np.stack([F[f"reg_{p}"][:N_FILL, 0].mean(0) for p in PIECES]))
    res = {"formacion": L1.form, "filas": []}
    done = set()
    for k, p in enumerate(PIECES):
        if NAMES[p] in done:
            continue
        done.add(NAMES[p])
        T = F[f"tn_{p}"]
        for version, X in (("cruda", T), ("corregida", T - mu_txt + mu_img)):
            for t, x in zip(T, X):
                d, why = L1.route(ind.proj(P, x[None])[0], k)
                res["filas"].append({"nombre": NAMES[p], "version": version, "destino": d, "motivo": why,
                                     "coseno": PIECES[int(np.argmax(proto @ t))]})
    # Post hoc: las oraciones corregidas caen bajo el umbral de energía; mismo ruteo sin ese umbral.
    res["diag_sin_energia"] = []
    done = set()
    for k, p in enumerate(PIECES):
        if NAMES[p] in done:
            continue
        done.add(NAMES[p])
        for x in F[f"tn_{p}"] - mu_txt + mu_img:
            with L1.ctx(), contextlib.redirect_stdout(io.StringIO()):
                d, *_ = s6.route_transactive(PIECES[(k + 1) % len(PIECES)], L1.agents,
                                             L1.q(ind.proj(P, x[None])[0]), modality="image", xi=0)
            res["diag_sin_energia"].append({"nombre": NAMES[p], "destino": PIECES[d] if d >= 0 else None})
    # pruebas de imagen del nivel 1 con CLIP, como control
    res["imagenes"] = []
    for k, p in enumerate(PIECES):
        z = ind.proj(P, F[f"test_{p}"])
        for zi, y in zip(z, ind.imgs()[f"testy_{p}"]):
            d, _ = L1.route(zi, k)
            res["imagenes"].append({"verdad": p, "falla": int(y), "destino": d})
    return res


def part_Z(F):
    allT = np.concatenate([np.concatenate([F[f"tn_{p}"], F[f"ta_{p}"]]) for p in PIECES])
    P = ind.pca(allT)
    g = grid(ind.proj(P, allT))
    mu_img = np.concatenate([F[f"reg_{p}"][:N_FILL, 0] for p in PIECES]).mean(0)
    mu_txt = allT.mean(0)
    out = {}
    for p in PIECES:
        an, aa = Agent(ind.proj(P, F[f"tn_{p}"]), g), Agent(ind.proj(P, F[f"ta_{p}"]), g)
        y = ind.imgs()[f"testy_{p}"]
        cal, te = F[f"reg_{p}"][N_FILL:, 0], F[f"test_{p}"]
        s_cpe = lambda X: -cpe(X, F[f"tn_{p}"], F[f"ta_{p}"])
        r = {}
        for version, shift in (("cruda", 0.0), ("corregida", mu_txt - mu_img)):
            def read(X):
                Z = ind.proj(P, X + shift)
                sn = np.array([an.score(z) for z in Z])
                sa = np.array([aa.score(z) for z in Z])
                grad = np.array([aa.uncovered(z) - an.uncovered(z) for z in Z])
                return sn, sa, grad
            sn_c, sa_c, g_c = read(cal)
            sn_t, sa_t, g_t = read(te)
            acc_cal = np.mean(sn_c > sa_c)
            rej = ~(sn_t > sa_t)
            row = ind.compare(acc_cal, rej, {"memoria_graduada": g_c, "cpe": s_cpe(cal)},
                              {"memoria_graduada": g_t, "cpe": s_cpe(te)}, y)
            row["rechazo_ambos"] = {"calibracion": float(np.mean((sn_c == 0) & (sa_c == 0))),
                                    "test": float(np.mean((sn_t == 0) & (sa_t == 0)))}
            r[version] = row
        r["cpe_auroc"] = ind.auroc(s_cpe(te)[y == 0], s_cpe(te)[y == 1])
        out[p] = r
    return out


def part_N(F):
    out = {}
    for p in PIECES:
        y = ind.imgs()[f"testy_{p}"]
        fill0 = F[f"reg_{p}"][:N_FILL, 0]
        P2 = ind.pca(fill0)
        reg2, test2 = ind.proj(P2, F[f"reg_{p}"]), ind.proj(P2, F[f"test_{p}"])
        cal2 = reg2[N_FILL:, 0]
        sp = ind.Specialist(reg2[:N_FILL])
        mu_txt = np.concatenate([F[f"tn_{p}"], F[f"ta_{p}"]]).mean(0)
        shift = lambda T: ind.proj(P2, T - mu_txt + fill0.mean(0))
        g = ind.Gauss(reg2[:N_FILL, 0])
        cal_raw, te_raw = F[f"reg_{p}"][N_FILL:, 0], F[f"test_{p}"]
        p_c, p_t = cpe(cal_raw, F[f"tn_{p}"], F[f"ta_{p}"]), cpe(te_raw, F[f"tn_{p}"], F[f"ta_{p}"])
        ref = lambda X: (1 - (X @ fill0.T).max(1)) / 2
        s_cal = {"memoria_graduada": -np.array([sp.uncovered(z) for z in cal2]),
                 "knn_euclid": ind.knn_euclid(reg2[:N_FILL, 0], cal2), "maha": g.score(cal2),
                 "cpe": -p_c, "cpe_knn": -(p_c + ref(cal_raw)) / 2}
        s_te = {"memoria_graduada": -np.array([sp.uncovered(z) for z in test2]),
                "knn_euclid": ind.knn_euclid(reg2[:N_FILL, 0], test2), "maha": g.score(test2),
                "cpe": -p_t, "cpe_knn": -(p_t + ref(te_raw)) / 2}
        acc_c = np.array([sp.accepts(z) for z in cal2])
        acc_t = np.array([sp.accepts(z) for z in test2])
        r = {}
        for variant, T in (("sin_texto", None), ("texto_cpe", F[f"ta_{p}"]),
                           ("texto_cpe_vocabulario", np.concatenate([F[f"ta_{p}"], F[f"tv_{p}"]]))):
            if T is None:
                tc, tt = np.zeros(len(cal2), bool), np.zeros(len(test2), bool)
            else:
                ag = Agent(shift(T), sp.g)
                tc = np.array([ag.uncovered(z) == 0 for z in cal2])
                tt = np.array([ag.uncovered(z) == 0 for z in test2])
            row = ind.compare(np.mean(acc_c & ~tc), ~acc_t | tt, s_cal, s_te, y)
            row["texto_acepta"] = {"calibracion": float(tc.mean()), "test_normales": float(tt[y == 0].mean()),
                                   "test_fallas": float(tt[y == 1].mean())}
            r[variant] = row
        out[p] = r
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", default="C:/Users/aq99l/Datasets/CLIP_ViT-B-16_openai/open_clip_model.safetensors")
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    raw = OUT / "resultados.json"
    if not args.report_only:
        t0 = time.time()
        F = features(args.clip)
        print(f"rasgos listos ({time.time() - t0:.0f} s)", flush=True)
        res = {"T": part_T(F)}
        print(f"T listo ({time.time() - t0:.0f} s)", flush=True)
        res["Z"] = part_Z(F)
        print(f"Z listo ({time.time() - t0:.0f} s)", flush=True)
        res["N"] = part_N(F)
        res["segundos"] = round(time.time() - t0)
        raw.write_text(json.dumps(res, ensure_ascii=False))
    report(json.loads(raw.read_text()))


def pct(x):
    return f"{100 * x:5.1f}"


def report(res):
    from collections import Counter
    L = ["Demo industrial con CLIP ViT-B/16 (OpenAI). Registro del demo: 270 normales x 16 variantes + 180 de calibración por pieza."]
    T = res["T"]
    L.append(f"\n[T · oración -> pieza] formación de directorios: {json.dumps(T['formacion'])}")
    imgs = T["imagenes"]
    for lab, nm in ((0, "normales"), (1, "fallas")):
        rs = [r for r in imgs if r["falla"] == lab]
        L.append(f"  control, imágenes {nm} n={len(rs)}: a su pieza {pct(np.mean([r['destino'] == r['verdad'] for r in rs]))} · "
                 f"rechazo {pct(np.mean([r['destino'] is None for r in rs]))}")
    for version in ("cruda", "corregida"):
        rs = [r for r in T["filas"] if r["version"] == version]
        ok = [r["destino"] is not None and NAMES[r["destino"]] == r["nombre"] for r in rs]
        rej = [r["destino"] is None for r in rs]
        cos = [NAMES[r["coseno"]] == r["nombre"] for r in rs]
        L.append(f"  oraciones {version} n={len(rs)}: a su nombre {pct(np.mean(ok))} · rechazo {pct(np.mean(rej))} · "
                 f"de lo respondido {pct(sum(ok) / max(len(rs) - sum(rej), 1))} · coseno CLIP {pct(np.mean(cos))} · "
                 f"motivos {dict(Counter(r['motivo'] for r in rs))}")
        for nm in dict.fromkeys(r["nombre"] for r in rs):
            q = [r for r in rs if r["nombre"] == nm]
            dest = Counter(NAMES[r["destino"]] if r["destino"] else "rechazo" for r in q)
            L.append(f"    {nm:<22} n={len(q)}  {dict(dest.most_common(4))} · coseno {sum(NAMES[r['coseno']] == nm for r in q)}")

    if "diag_sin_energia" in T:
        rs = T["diag_sin_energia"]
        ok = [r["destino"] is not None and NAMES[r["destino"]] == r["nombre"] for r in rs]
        rej = [r["destino"] is None for r in rs]
        L.append(f"  post hoc, corregida sin umbral de energía n={len(rs)}: a su nombre {pct(np.mean(ok))} · rechazo {pct(np.mean(rej))} · "
                 f"de lo respondido {pct(sum(ok) / max(len(rs) - sum(rej), 1))}")
        for nm in dict.fromkeys(r["nombre"] for r in rs):
            q = [r for r in rs if r["nombre"] == nm]
            L.append(f"    {nm:<22} n={len(q)}  {dict(Counter(NAMES[r['destino']] if r['destino'] else 'rechazo' for r in q).most_common(4))}")

    def block(title, rows, keys, extra=None):
        L.append(f"\n[{title}] detección / falsa alarma en test; detectores a la aceptación de calibración de la memoria; AUROC")
        for p in PIECES:
            r = rows[p]
            e = extra(r) if extra else ""
            L.append(f"    {p:<11} acepta cal {pct(r['acepta_calibracion'])} · memoria {pct(r['memoria']['deteccion'])} / "
                     f"{pct(r['memoria']['falsa_alarma'])} · " + " · ".join(
                         f"{k} {pct(r[k]['deteccion'])} / {pct(r[k]['falsa_alarma'])} ({r[k]['auroc']:.3f})" for k in keys) + e)
        m = lambda f: np.mean([f(rows[p]) for p in PIECES])
        L.append(f"    media       acepta cal {pct(m(lambda r: r['acepta_calibracion']))} · memoria "
                 f"{pct(m(lambda r: r['memoria']['deteccion']))} / {pct(m(lambda r: r['memoria']['falsa_alarma']))} · "
                 + " · ".join(f"{k} {pct(m(lambda r: r[k]['deteccion']))} / {pct(m(lambda r: r[k]['falsa_alarma']))} "
                              f"({m(lambda r: r[k]['auroc']):.3f})" for k in keys)
                 + (f" · {extra(None, m)}" if extra else ""))

    for version in ("cruda", "corregida"):
        rows = {p: res["Z"][p][version] for p in PIECES}
        block(f"Z · solo texto, {version}", rows, ("memoria_graduada", "cpe"),
              lambda r, m=None: (f" · ninguno contiene: cal {pct(r['rechazo_ambos']['calibracion'])} test {pct(r['rechazo_ambos']['test'])}"
                                 if r else f"ninguno contiene (test) {pct(m(lambda r: r['rechazo_ambos']['test']))}"))
    for variant in ("sin_texto", "texto_cpe", "texto_cpe_vocabulario"):
        rows = {p: res["N"][p][variant] for p in PIECES}
        block(f"N · especialista de normales + {variant}", rows, ("memoria_graduada", "knn_euclid", "maha", "cpe", "cpe_knn"),
              lambda r, m=None: (f" · texto acepta: cal {pct(r['texto_acepta']['calibracion'])} normales {pct(r['texto_acepta']['test_normales'])} fallas {pct(r['texto_acepta']['test_fallas'])}"
                                 if r else f"texto acepta fallas {pct(m(lambda r: r['texto_acepta']['test_fallas']))} normales {pct(m(lambda r: r['texto_acepta']['test_normales']))}"))
    L.append(f"\nTiempo total: {res.get('segundos', 0) / 60:.0f} min")
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
