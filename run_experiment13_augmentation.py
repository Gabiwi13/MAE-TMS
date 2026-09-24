"""
Experimento 13: augmentación del llenado visual. Diseño en
propuesta_exp13_augmentacion_visual.md.

Dos compuertas rechazan imágenes nuevas: el directorio visual (mem_dir_R,
formado en la fase A sin augmentar) y el recall de la hetero (conjunción por
celda de project). Se mide qué quita la augmentación en cada una y a qué
precio en falsos, con familias anidadas de V variantes aplicadas al
contenido (Vc), al directorio (Vd) o a ambos.

Uso:
  python run_experiment13_augmentation.py --seeds 42-46 --workers 3
  python run_experiment13_augmentation.py --report-only

Los latentes se codifican una vez (GPU) y se guardan en results/experimento13;
las variantes 0-3 de train[:200] son los latentes oficiales de la etapa 5,
para que Vc=4, N=200 sea bit a bit el llenado oficial.
"""
import argparse
import contextlib
import io
import json
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from stage5_fill import (CLASSES, N_FILL, MODELS_DIR, DATA_DIR, IMG_TRANSFORM,  # noqa: E402
                         FILL_VARIANTS, build_label_sequence, quantize_latent_global)
from stage6_interaction import (Agent, AGENT_LIST, TME, register_transaction,  # noqa: E402
                                route_transactive, load_all_vectors,
                                N as N_LAB, M_LABEL, P_LATENT, Q_LATENT)
from stage7_bidirectional import (recognize_gated_right, evoke_labels, XI_VISUAL,  # noqa: E402
                                  load_global_stats, load_encoder)
from associative_memory import DirectoryMemory, HomoAssociativeMemory  # noqa: E402
from hetero_memory import HeteroAssociativeMemory, _norm_weights  # noqa: E402
from run_experiment11_monolithic import (_fill, exclusive_vocab, image_strict,  # noqa: E402
                                         _ci, _rate, _fmt, parse_seeds, same_as_official)

OUT_DIR = Path(os.environ.get("EXP13_OUT", ROOT / "results" / "experimento13"))
RAW_DIR = OUT_DIR / "raw"
CACHE_DIR = ROOT / "cache" / "exp13"
K = len(AGENT_LIST)
V_MAX = 16
V_FAMILY = (1, 4, 8, 12, 16)
N_A = 128                      # percepciones de la fase A: train[200:328]
N_EVOKE = 5                    # imágenes de test por clase con evocación completa (17 s cada una)
SEEDS = tuple(range(42, 47))
IMG = 128

# (Vc, N, Vd) -> brazo. A0 oficial; A1 solo directorio; A2 solo contenido;
# A3 ambos; N328 más imágenes reales en vez de variantes.
COMBOS = [(4, 200, 1), (4, 200, 4), (4, 200, 8), (4, 200, 12), (4, 200, 16),
          (1, 200, 1), (8, 200, 1), (12, 200, 1), (16, 200, 1),
          (8, 200, 8), (12, 200, 12), (16, 200, 16),
          (4, 328, 1)]


def arms_of(vc, n, vd):
    arms = []
    if (vc, n, vd) == (4, 200, 1):
        arms.append(("A0", 4))
    if n == 200 and vc == 4 and vd >= 4:
        arms.append(("A1", vd))
    if n == 200 and vd == 1:
        arms.append(("A2", vc))
    if n == 200 and vc == vd:
        arms.append(("A3", vc))
    if n == 328:
        arms.append(("N328", vc))
    return arms


# ---------- variantes ----------

def _scaled(img, s, bg):
    from PIL import Image
    w = int(round(IMG * s))
    r = img.resize((w, w), Image.BILINEAR)
    if s < 1:
        canvas = Image.new("RGB", (IMG, IMG), bg)
        canvas.paste(r, ((IMG - w) // 2, (IMG - w) // 2))
        return canvas
    o = (w - IMG) // 2
    return r.crop((o, o, o + IMG, o + IMG))


def variants(img, V=V_MAX):
    """Familia anidada y determinista. Las cuatro primeras son las de la
    etapa 5 (esquinas negras en las rotaciones, como allí); las nuevas
    rellenan con el color del fondo de la propia imagen."""
    from PIL import Image, ImageEnhance
    bg = img.getpixel((0, 0))
    out = [img, img.transpose(Image.FLIP_LEFT_RIGHT),
           img.rotate(-12, resample=Image.BILINEAR), img.rotate(12, resample=Image.BILINEAR)]
    if V > 4:
        out += [img.rotate(-6, resample=Image.BILINEAR, fillcolor=bg),
                img.rotate(6, resample=Image.BILINEAR, fillcolor=bg),
                _scaled(img, 0.9, bg), _scaled(img, 1.1, bg)]
    if V > 8:
        f = out[1]
        out += [f.rotate(-12, resample=Image.BILINEAR, fillcolor=bg),
                f.rotate(12, resample=Image.BILINEAR, fillcolor=bg),
                ImageEnhance.Brightness(img).enhance(0.85),
                ImageEnhance.Brightness(img).enhance(1.15)]
    if V > 12:
        out += [img.rotate(0, translate=(dx, dy), fillcolor=bg)
                for dx, dy in ((6, 0), (-6, 0), (0, 6), (0, -6))]
    return out[:V]


def synthetic_probes():
    from PIL import Image
    rng = np.random.RandomState(0)
    noise = (rng.rand(IMG, IMG, 3) * 255).astype(np.uint8)
    solid = np.full((IMG, IMG, 3), 127, dtype=np.uint8)
    scram = (rng.rand(IMG, IMG, 3) * 255).astype(np.uint8).reshape(-1, 3)
    rng.shuffle(scram)
    return [("noise", Image.fromarray(noise)), ("solid", Image.fromarray(solid)),
            ("scrambled", Image.fromarray(scram.reshape(IMG, IMG, 3)))]


# ---------- codificación ----------

def _encode_batch(encoder, imgs):
    import torch
    dev = next(encoder.parameters()).device
    t = torch.stack([IMG_TRANSFORM(im) for im in imgs]).to(dev)
    with torch.no_grad():
        return encoder(t).cpu().numpy().astype(np.float32)


def rel(path):
    return str(Path(path).as_posix().split("data/eth80/")[-1])


def encode_all():
    """Latentes de las 328 de train por clase (V_MAX variantes), las 82 de
    test y las sondas. Reanudable por archivo."""
    from PIL import Image
    f_fill, f_test, f_probe = (OUT_DIR / "latentes_llenado.json", OUT_DIR / "latentes_test.json",
                               OUT_DIR / "latentes_sondas.json")
    if f_fill.exists() and f_test.exists() and f_probe.exists():
        return
    encoder = load_encoder()
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    if not f_fill.exists():
        out, t0 = {}, time.time()
        for cls in CLASSES:
            for p in splits[cls]["train"]:
                img = Image.open(p).convert("RGB").resize((IMG, IMG))
                out[rel(p)] = _encode_batch(encoder, variants(img, V_MAX)).tolist()
            print(f"  {cls}: {len(splits[cls]['train'])} imágenes × {V_MAX} variantes "
                  f"({time.time()-t0:.0f}s)", flush=True)
        f_fill.write_text(json.dumps(out))
    if not f_test.exists():
        out = {}
        for cls in CLASSES:
            paths = splits[cls]["test"]
            imgs = [Image.open(p).convert("RGB").resize((IMG, IMG)) for p in paths]
            zs = _encode_batch(encoder, imgs)
            out.update({rel(p): z.tolist() for p, z in zip(paths, zs)})
        f_test.write_text(json.dumps(out))
    if not f_probe.exists():
        probes = synthetic_probes()
        zs = _encode_batch(encoder, [im for _, im in probes])
        f_probe.write_text(json.dumps({name: z.tolist() for (name, _), z in zip(probes, zs)}))


def load_latents():
    g_min, g_max = load_global_stats()
    g_min, g_max = g_min.astype(np.float32), g_max.astype(np.float32)

    def q(z):
        return quantize_latent_global(np.asarray(z, dtype=np.float32), g_min, g_max, Q_LATENT)

    splits = json.loads((DATA_DIR / "splits.json").read_text())
    fill = json.loads((OUT_DIR / "latentes_llenado.json").read_text())
    test = json.loads((OUT_DIR / "latentes_test.json").read_text())
    probes = json.loads((OUT_DIR / "latentes_sondas.json").read_text())
    # train[i] -> lista de V_MAX latentes cuantizados; las variantes 0-3 de
    # las 200 primeras son las oficiales (etapa 5, float32).
    train_q, control = {}, {}
    for cls in CLASSES:
        official = json.loads((MODELS_DIR / f"instance_latents_{cls}.json").read_text())
        rows, diff, cells = [], 0, 0
        for i, p in enumerate(splits[cls]["train"]):
            zs = [q(z) for z in fill[rel(p)]]
            if i < N_FILL:
                for v in range(min(4, FILL_VARIANTS)):
                    off = q(official[FILL_VARIANTS * i + v])
                    diff += int(np.count_nonzero(off != zs[v]))
                    cells += off.size
                    zs[v] = off
            rows.append(zs)
        train_q[cls] = rows
        control[cls] = {"niveles_distintos": diff, "celdas": cells}
    test_q = [(rel(p), q(test[rel(p)]), ci) for ci, cls in enumerate(CLASSES)
              for p in splits[cls]["test"]]
    probes_q = {name: q(z) for name, z in probes.items()}
    return train_q, test_q, probes_q, control


# ---------- memorias de contenido ----------

def content_key(vc, n):
    return f"Vc{vc}_N{n}"


def density_R(mem):
    r = np.asarray(mem._am.relation)
    return float(np.count_nonzero(r) / r.size)


def build_content(args):
    vc, n = args
    path = CACHE_DIR / f"{content_key(vc, n)}.pkl"
    if path.exists():
        return str(path)
    import pickle
    t0 = time.time()
    train_q, _, _, control_enc = load_latents()
    agents = {}
    for cls in CLASSES:
        seq = build_label_sequence(cls)
        with contextlib.redirect_stdout(io.StringIO()):
            mem_H = HeteroAssociativeMemory(N_LAB, M_LABEL, P_LATENT, Q_LATENT)
            mem_L = HomoAssociativeMemory(N_LAB, M_LABEL)
            mem_R = HomoAssociativeMemory(P_LATENT, Q_LATENT)
        for v_q in seq:
            mem_L.register(v_q)
        pool = [z for i in range(n) for z in train_q[cls][i][:vc]]
        _fill(mem_H, mem_R, seq, pool)
        agents[cls] = Agent(cls, mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)
    meta = {"Vc": vc, "N": n, "registros_por_clase": n * vc,
            "densidad_R": {c: density_R(agents[c].mem_dom_R) for c in CLASSES},
            "control_encoder": control_enc,
            "control_igual_al_oficial": same_as_official(agents) if (vc, n) == (FILL_VARIANTS, N_FILL) else None,
            "segundos": round(time.time() - t0)}
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump({"specialists": agents, "meta": meta}, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"  contenido {content_key(vc, n)}: {n * vc} registros/clase en {meta['segundos']}s"
          f"{'  control ' + str(meta['control_igual_al_oficial']) if meta['control_igual_al_oficial'] else ''}",
          flush=True)
    return str(path)


# ---------- directorios y evaluación ----------

def density_dir(d):
    ham = d._ham
    r = np.asarray(ham._full_iota_relation)[:, :, :, :ham.q]
    return float(np.count_nonzero(r.sum(axis=(1, 3))) / (r.shape[0] * r.shape[2]))


def form_directories(agents, train_q, vd, seed):
    """Fase A de la etapa 7 con protocolo v5. Cada percepción decide ganador
    con la variante original; con vd > 1 registra sus vd variantes."""
    for c in CLASSES:
        agents[c].mem_dir_R = DirectoryMemory(P_LATENT, Q_LATENT, K)
    tme = TME()
    rng = np.random.RandomState(seed)
    n_reg = n_rej = ok = 0
    for i in range(N_FILL, N_FILL + N_A):
        for ci, cls in enumerate(CLASSES):
            zs = train_q[cls][i]
            scores = {c: recognize_gated_right(agents[c], zs[0]) for c in CLASSES}
            if sum(scores.values()) == 0:
                n_rej += 1
                continue
            w = max(scores, key=scores.get)
            widx = AGENT_LIST.index(w)
            ok += int(widx == ci)
            n_reg += 1
            entry = AGENT_LIST[int(rng.randint(K))]
            with contextlib.redirect_stdout(io.StringIO()):
                for z in zs[:vd]:
                    register_transaction(entry, widx, agents, tme, z, "image")
    return {"registradas": n_reg, "rechazadas": n_rej, "acierto_temprano": ok / max(n_reg, 1),
            "densidad_dir": {c: density_dir(agents[c].mem_dir_R) for c in CLASSES}}


def hetero_recognizes(agent, z_q):
    """Lo que decide `recall_from_right`: ninguna fila vacía en la proyección
    ponderada por la homo latente. Sin la búsqueda por muestreo, que cuesta
    17 s por imagen y solo hace falta para leer etiquetas."""
    mem_H = agent.mem_dom_H
    w = _norm_weights(agent.mem_dom_R.recog_weights(z_q), P_LATENT)
    cb = mem_H.validate(z_q, 1)
    with contextlib.redirect_stdout(io.StringIO()):
        proj = mem_H.project(cb, w, 1)
    return bool(np.count_nonzero(np.sum(proj, axis=1) == 0) == 0)


CTX = {}


def _init(cache_path):
    import pickle
    with open(cache_path, "rb") as f:
        CTX["cache"] = pickle.load(f)
    train_q, test_q, probes_q, _ = load_latents()
    CTX.update(train_q=train_q, test_q=test_q, probes_q=probes_q)
    vectors = load_all_vectors()
    CTX["vocab"] = {c: set(vectors[c]) for c in CLASSES}
    CTX["all_vecs"] = {w: v for c in CLASSES for w, v in vectors[c].items()}
    CTX["excl"] = exclusive_vocab()


def run_job(args):
    vc, n, vd, seed = args
    out = RAW_DIR / f"Vc{vc}_N{n}_Vd{vd}_s{seed}.json"
    if out.exists():
        return str(out)
    t0 = time.time()
    agents = CTX["cache"]["specialists"]
    meta = dict(CTX["cache"]["meta"], Vd=vd, semilla=seed, brazos=arms_of(vc, n, vd))
    meta["formacion"] = form_directories(agents, CTX["train_q"], vd, seed)

    rows, seen = [], {c: 0 for c in CLASSES}
    for path, z_q, ci in CTX["test_q"]:
        truth = CLASSES[ci]
        own = recognize_gated_right(agents[truth], z_q) > 0
        ajenos = [c for c in CLASSES if c != truth and recognize_gated_right(agents[c], z_q) > 0]
        responde = own and hetero_recognizes(agents[truth], z_q)
        entry = CLASSES[(ci + 1) % K]
        with contextlib.redirect_stdout(io.StringIO()):
            d, _s, consulted, hops = route_transactive(entry, agents, z_q,
                                                       modality="image", xi=XI_VISUAL)
        dest = CLASSES[d] if d >= 0 else None
        responde_dest = bool(dest) and hetero_recognizes(agents[dest], z_q)
        evocada = seen[truth] < N_EVOKE
        seen[truth] += 1
        labels = evoke_labels(agents[truth], z_q, CTX["all_vecs"]) if (evocada and responde) else []
        row = {"imagen": path, "truth": truth,
               "contenido_acepta": own, "falso_contenido": bool(ajenos), "ajenos": ajenos,
               "responde": responde, "evocada": evocada, "labels": labels,
               "dir_acepta": d >= 0, "destino": dest, "ruteo_ok": (d == ci) if d >= 0 else None,
               "falso_ruteo": (d >= 0 and d != ci), "consultados": len(consulted), "saltos": hops,
               "responde_destino": responde_dest,
               "e2e": bool(d == ci and responde_dest)}
        rows.append(row)
    image_strict(rows, CTX["excl"])

    probes = {}
    for name, z_q in CTX["probes_q"].items():
        acc = [c for c in CLASSES if recognize_gated_right(agents[c], z_q) > 0]
        with contextlib.redirect_stdout(io.StringIO()):
            d, *_ = route_transactive(CLASSES[0], agents, z_q, modality="image", xi=XI_VISUAL)
        probes[name] = {"contenido_acepta": acc, "directorio": CLASSES[d] if d >= 0 else None}

    meta["segundos"] = round(time.time() - t0, 1)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"meta": meta, "test": rows, "sondas": probes}, ensure_ascii=False))
    print(f"  Vc{vc} N{n} Vd{vd} s{seed}: {len(rows)} imágenes ({meta['segundos']}s)", flush=True)
    return str(out)


# ---------- reporte ----------

METRICS = ("contenido_acepta", "responde", "hit_exclusivo", "otro_dominio", "falso_contenido",
           "dir_acepta", "ruteo_ok", "falso_ruteo", "e2e")


def aggregate():
    raws = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(RAW_DIR.glob("*.json"))]
    summary = {"combos": {}, "brazos": {}, "control": {}}
    by_combo = {}
    for raw in raws:
        m = raw["meta"]
        by_combo.setdefault((m["Vc"], m["N"], m["Vd"]), []).append(raw)
        if m.get("control_igual_al_oficial"):
            summary["control"]["igual_al_oficial"] = m["control_igual_al_oficial"]
        summary["control"]["encoder"] = m["control_encoder"]
    for (vc, n, vd), rs in sorted(by_combo.items()):
        per = {k: [] for k in METRICS}
        probes = {}
        for raw in rs:
            rows = raw["test"]
            for k in METRICS:
                cond = {"ruteo_ok": lambda r: r["dir_acepta"],
                        "hit_exclusivo": lambda r: r["evocada"] and r["responde"],
                        "otro_dominio": lambda r: r["evocada"] and r["responde"]}.get(k)
                per[k].append(_rate(rows, k, cond))
            for name, p in raw["sondas"].items():
                probes.setdefault(name, {"contenido": [], "directorio": []})
                probes[name]["contenido"].append(len(p["contenido_acepta"]))
                probes[name]["directorio"].append(p["directorio"] is not None)
        entry = {k: _ci(v) for k, v in per.items()}
        entry["semillas"] = len(rs)
        entry["densidad_R"] = float(np.mean(list(rs[0]["meta"]["densidad_R"].values())))
        entry["densidad_dir"] = float(np.mean([np.mean(list(r["meta"]["formacion"]["densidad_dir"].values()))
                                              for r in rs]))
        entry["formacion"] = {k: float(np.mean([r["meta"]["formacion"][k] for r in rs]))
                              for k in ("registradas", "rechazadas", "acierto_temprano")}
        entry["sondas"] = {name: {"contenido_media": float(np.mean(p["contenido"])),
                                  "directorio_frac": float(np.mean(p["directorio"]))}
                           for name, p in probes.items()}
        key = f"Vc{vc}|N{n}|Vd{vd}"
        summary["combos"][key] = entry
        for arm, v in arms_of(vc, n, vd):
            summary["brazos"].setdefault(arm, {})[str(v)] = key
    (OUT_DIR / "resumen.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    return summary


ARM_DESC = {"A0": "oficial (Vc=4, Vd=1)", "A1": "solo directorio (Vc=4, Vd=V)",
            "A2": "solo contenido (Vc=V, Vd=1)", "A3": "ambos (Vc=Vd=V)",
            "N328": "328 imágenes reales, Vc=4, Vd=1"}


def write_report(summary):
    L = ["# Experimento 13 — augmentación del llenado visual", "",
         "656 imágenes de test (82 por clase). Intervalos: bootstrap del 95 % sobre las medias por semilla. "
         "Contenido: `recognize_gated_right` del especialista propio. Responde: `recall_from_right` del "
         "especialista propio reconoce (proyección sin filas vacías, el criterio de `recall_from_right`). "
         "Hit estricto y otro dominio: sobre las respuestas de las primeras 5 imágenes de test por clase, con "
         "la evocación completa. Directorio: `route_transactive` desde una entrada no especialista, "
         "ξ = 0. e2e: rutea a la clase correcta y el destino responde. Falso contenido: algún especialista "
         "ajeno acepta. Diseño en `propuesta_exp13_augmentacion_visual.md`.", ""]
    ctrl = summary["control"]
    if ctrl.get("igual_al_oficial"):
        L.append(f"Control: Vc=4, N=200 igual a los `agent_*.pkl` oficiales en "
                 f"{sum(ctrl['igual_al_oficial'].values())}/8 clases.")
    enc = ctrl.get("encoder", {})
    if enc:
        tot = sum(v["niveles_distintos"] for v in enc.values())
        cells = sum(v["celdas"] for v in enc.values())
        L.append(f"Encoder en GPU contra los latentes oficiales (variantes 0-3 de train[:200], cuantizados): "
                 f"{tot} niveles distintos de {cells} ({tot / max(cells, 1) * 100:.3f} %); se usan los oficiales.")
    L.append("")
    for arm in ("A0", "A1", "A2", "A3", "N328"):
        if arm not in summary["brazos"]:
            continue
        L += [f"## {arm}: {ARM_DESC[arm]}", "",
              "| V | contenido acepta | responde | hit estricto | otro dominio | falso contenido | "
              "directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | densidad R | densidad dir |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for v, key in sorted(summary["brazos"][arm].items(), key=lambda kv: int(kv[0])):
            e = summary["combos"][key]
            L.append(f"| {v} | " + " | ".join(_fmt(e[k]) for k in METRICS) +
                     f" | {e['densidad_R']*100:.1f} % | {e['densidad_dir']*100:.1f} % |")
        L.append("")
    L += ["## Sondas sintéticas", "", "Especialistas que aceptan (de 8, media por semilla) y fracción de "
          "semillas en que el directorio rutea.", "",
          "| combinación | ruido | color sólido | píxeles barajados |", "|---|---|---|---|"]
    for key, e in summary["combos"].items():
        s = e["sondas"]
        L.append(f"| {key} | " + " | ".join(
            f"{s[n]['contenido_media']:.1f} / {s[n]['directorio_frac']*100:.0f} %"
            for n in ("noise", "solid", "scrambled")) + " |")
    L += ["", "## Formación de directorios (fase A, media por semilla)", "",
          "| combinación | registradas | rechazadas | acierto temprano |", "|---|---|---|---|"]
    for key, e in summary["combos"].items():
        f = e["formacion"]
        L.append(f"| {key} | {f['registradas']:.0f} | {f['rechazadas']:.0f} | {f['acierto_temprano']*100:.1f} |")
    L += ["", "## Archivos", "- `raw/Vc<Vc>_N<N>_Vd<Vd>_s<semilla>.json`: filas por imagen de test, sondas y formación",
          "- `resumen.json`, `fig1_cobertura_vs_V.png`, `fig2_falsos_vs_V.png`",
          "- `latentes_llenado.json`, `latentes_test.json`, `latentes_sondas.json`: latentes continuos del encoder"]
    (OUT_DIR / "README.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def make_figures(summary):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    color = {"A1": "#2980b9", "A2": "#c0392b", "A3": "#27ae60"}

    def series(arm, metric):
        pts = sorted(((int(v), summary["combos"][k][metric]) for v, k in summary["brazos"][arm].items()))
        return [p[0] for p in pts], np.array([p[1] for p in pts])

    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
    for ax, metric, title in zip(axes, ("dir_acepta", "responde", "e2e"),
                                 ("directorio acepta", "contenido responde", "punta a punta")):
        for arm in ("A1", "A2", "A3"):
            if arm not in summary["brazos"]:
                continue
            xs, v = series(arm, metric)
            ax.errorbar(xs, v[:, 0] * 100, yerr=[(v[:, 0] - v[:, 1]) * 100, (v[:, 2] - v[:, 0]) * 100],
                        fmt="o-", color=color[arm], label=arm, capsize=3)
        if "N328" in summary["brazos"]:
            e = summary["combos"][summary["brazos"]["N328"]["4"]][metric]
            ax.axhline(e[0] * 100, color="gray", ls="--", label="N=328, V=4")
        ax.set_title(title); ax.set_xlabel("V variantes"); ax.set_xticks(V_FAMILY)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("% de las 656 de test"); axes[0].legend()
    fig.tight_layout(); fig.savefig(OUT_DIR / "fig1_cobertura_vs_V.png", dpi=150); plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(9, 4), sharey=True)
    for ax, metric, title in zip(axes, ("falso_contenido", "falso_ruteo"),
                                 ("algún especialista ajeno acepta", "ruteo a otra clase")):
        for arm in ("A1", "A2", "A3"):
            if arm not in summary["brazos"]:
                continue
            xs, v = series(arm, metric)
            ax.errorbar(xs, v[:, 0] * 100, yerr=[(v[:, 0] - v[:, 1]) * 100, (v[:, 2] - v[:, 0]) * 100],
                        fmt="o-", color=color[arm], label=arm, capsize=3)
        ax.set_title(title); ax.set_xlabel("V variantes"); ax.set_xticks(V_FAMILY)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("% de las 656 de test"); axes[0].legend()
    fig.tight_layout(); fig.savefig(OUT_DIR / "fig2_falsos_vs_V.png", dpi=150); plt.close(fig)


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default=None)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--combos", default=None, help="índices de COMBOS separados por coma")
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not args.report_only:
        seeds = parse_seeds(args.seeds) if args.seeds else SEEDS
        combos = [COMBOS[int(i)] for i in args.combos.split(",")] if args.combos else COMBOS
        print("Codificando latentes (llenado × variantes, test, sondas)...", flush=True)
        encode_all()

        keys = sorted({(vc, n) for vc, n, _ in combos}, key=lambda k: k[0] * k[1])
        todo = [k for k in keys if not (CACHE_DIR / f"{content_key(*k)}.pkl").exists()]
        if todo:
            print(f"Construyendo {len(todo)} memorias de contenido ({args.workers} procesos)...", flush=True)
            if args.workers > 1:
                with Pool(min(args.workers, len(todo))) as pool:
                    list(pool.imap_unordered(build_content, todo))
            else:
                for k in todo:
                    build_content(k)

        for key in keys:
            jobs = [(vc, n, vd, s) for vc, n, vd in combos if (vc, n) == key for s in seeds
                    if not (RAW_DIR / f"Vc{vc}_N{n}_Vd{vd}_s{s}.json").exists()]
            if not jobs:
                continue
            cache_path = str(CACHE_DIR / f"{content_key(*key)}.pkl")
            print(f"Contenido {content_key(*key)}: {len(jobs)} trabajos", flush=True)
            if args.workers > 1:
                with Pool(min(args.workers, len(jobs)), initializer=_init, initargs=(cache_path,)) as pool:
                    list(pool.imap_unordered(run_job, jobs))
            else:
                _init(cache_path)
                for j in jobs:
                    run_job(j)

    summary = aggregate()
    write_report(summary)
    make_figures(summary)
    print(f"Salidas -> {OUT_DIR}")


if __name__ == "__main__":
    main()
