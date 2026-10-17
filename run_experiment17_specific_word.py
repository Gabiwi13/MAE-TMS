"""
Experimento 17, parte A: ¿la evocación imagen -> palabra da una palabra?

Sobre los modelos oficiales (etapa 7) y las mismas 120 imágenes de test que
miden el top-3 (15 por clase, entrada por un agente no especialista), se lee
el ranking completo de palabras y se mide top-1 en vez de top-3. Dos lecturas:
  oficial    recall_from_right (muestreo), 3 repeticiones con semilla fija por
             imagen para medir si la palabra cambia entre recuerdos.
  prototipo  argmax por columna de la misma proyección (determinista).
Cada patrón se compara por coseno contra el diccionario crudo (como
evoke_labels) y contra el diccionario cuantizado (lo que de verdad se guardó).

Uso:
  python run_experiment17_specific_word.py --workers 6
  python run_experiment17_specific_word.py --report-only
"""
import argparse
import contextlib
import io
import json
import random
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from stage5_fill import CLASSES, quantize_latent_global  # noqa: E402
from stage6_interaction import (load_tme_and_agents, load_all_vectors, route_transactive,  # noqa: E402
                                M_LABEL, Q_LATENT, P_LATENT, N as N_LAB)
from stage7_bidirectional import (load_encoder, load_global_stats, image_to_latent, latent_energy_threshold,  # noqa: E402
                                  latent_has_energy, XI_VISUAL, N_EVOKE, DATA_DIR)
from hetero_memory import _norm_weights  # noqa: E402
from quantizer import quantize_binary  # noqa: E402
from run_experiment11_monolithic import exclusive_vocab  # noqa: E402

OUT_DIR = ROOT / "results" / "experimento17"
RAW_A = OUT_DIR / "parte_a_filas.json"
N_REP = 3
TOP = 5

W = {}


def _to_cont(v_q):
    return (np.asarray(v_q, dtype=float) / max(M_LABEL - 1, 1)) * 2.0 - 1.0


def dictionaries():
    vecs = load_all_vectors()
    words = sorted({w for c in CLASSES for w in vecs[c]})
    raw = {w: np.asarray(next(vecs[c][w] for c in CLASSES if w in vecs[c]), dtype=float) for w in words}
    quant = {w: _to_cont(quantize_binary(raw[w], M_LABEL)) for w in words}
    return words, raw, quant


def ranking(pattern, words, dic):
    m = np.stack([dic[w] for w in words])
    sims = m @ pattern / (np.linalg.norm(m, axis=1) * np.linalg.norm(pattern) + 1e-8)
    order = np.argsort(-sims)
    return [(words[i], float(sims[i])) for i in order]


def load_agent(cls):
    """Un solo agente: los ocho juntos pesan 3.9 GB por proceso."""
    import pickle
    import stage6_interaction as _s6
    old_main = sys.modules.get("__main__")
    sys.modules["__main__"] = _s6
    try:
        with open(_s6.MODELS_DIR / f"agent_{cls}.pkl", "rb") as f:
            return pickle.load(f)
    finally:
        sys.modules["__main__"] = old_main


def _summary(rank, cls, dest_vocab):
    names = [w for w, _ in rank]
    in_dest = [w for w in names if w in dest_vocab]
    return {"top": rank[:TOP], "rango_nombre": names.index(cls) + 1,
            "margen": rank[0][1] - rank[1][1], "top1_vocab_destino": in_dest[0] if in_dest else None}


def evaluate_group(group):
    dest, items = group
    ag = load_agent(dest)
    W["words"], W["raw"], W["quant"] = dictionaries()
    return [evaluate(ag, dest, *it) for it in items]


def evaluate(ag, dest, cls, j, z_q):
    words = W["words"]
    ci = CLASSES.index(cls)
    row = {"clase": cls, "j": j, "destino": dest}
    dest_vocab = set(load_all_vectors()[dest])
    r_w = ag.mem_dom_R.recog_weights(z_q)

    row["oficial"] = []
    for rep in range(N_REP):
        random.seed(1000 * ci + 10 * j + rep)
        np.random.seed(1000 * ci + 10 * j + rep)
        with contextlib.redirect_stdout(io.StringIO()):
            rec_q, recognized, _wt, *_ = ag.mem_dom_H.recall_from_right(z_q, weights=r_w)
        if not recognized:
            row["oficial"].append(None)
            continue
        p = _to_cont(rec_q)
        row["oficial"].append({"crudo": _summary(ranking(p, words, W["raw"]), cls, dest_vocab),
                               "cuant": _summary(ranking(p, words, W["quant"]), cls, dest_vocab)})

    mem_H = ag.mem_dom_H
    with contextlib.redirect_stdout(io.StringIO()):
        proj = mem_H.project(mem_H.validate(z_q, 1), _norm_weights(r_w, P_LATENT), 1)
    if np.count_nonzero(np.sum(proj, axis=1) == 0) > 0:
        row["prototipo"] = None
    else:
        p = _to_cont(np.argmax(proj, axis=1))
        row["prototipo"] = {"crudo": _summary(ranking(p, words, W["raw"]), cls, dest_vocab),
                            "cuant": _summary(ranking(p, words, W["quant"]), cls, dest_vocab)}
    return row


def build_items():
    encoder = load_encoder()
    g_min, g_max = load_global_stats()
    tau = latent_energy_threshold()
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    items, sin_energia = [], 0
    for cls in CLASSES:
        for j, p in enumerate(splits[cls]["test"][:N_EVOKE]):
            z = image_to_latent(p, encoder)
            if not latent_has_energy(z, tau):
                sin_energia += 1
                continue
            items.append((cls, j, quantize_latent_global(z, g_min, g_max, Q_LATENT)))
    # El ruteo es barato: se hace aquí, con los ocho agentes cargados una sola vez.
    with contextlib.redirect_stdout(io.StringIO()):
        _tme, agents = load_tme_and_agents()
    groups, unrouted = {}, []
    for cls, j, z_q in items:
        ci = CLASSES.index(cls)
        with contextlib.redirect_stdout(io.StringIO()):
            d, *_ = route_transactive(CLASSES[(ci + 1) % len(CLASSES)], agents, z_q,
                                      modality="image", xi=XI_VISUAL)
        if d < 0:
            unrouted.append({"clase": cls, "j": j, "destino": None})
        else:
            groups.setdefault(CLASSES[d], []).append((cls, j, z_q))
    return groups, unrouted, sin_energia


def report():
    rows = json.loads(RAW_A.read_text())["filas"]
    excl = exclusive_vocab()
    vocab = {c: set(load_all_vectors()[c]) for c in CLASSES}
    n = len(rows)
    n_words = len(dictionaries()[0])
    lines = [f"Imágenes evaluadas: {n}; ruteadas: {sum(r['destino'] is not None for r in rows)}; "
             f"ruteo correcto: {sum(r['destino'] == r['clase'] for r in rows)}"]

    def block(name, reads):
        # reads: lista de (fila, resumen) con resumen None si no reconoció
        ok = [(r, s) for r, s in reads if s is not None]
        k = len(reads)

        def pct(x):
            return f"{100 * x / max(k, 1):5.1f} %"

        t3_dom = sum(any(w in vocab[r["clase"]] for w, _ in s["top"][:3]) for r, s in ok)
        t3_exc = sum(any(w in excl[r["clase"]] for w, _ in s["top"][:3]) for r, s in ok)
        t1_dom = sum(s["top"][0][0] in vocab[r["clase"]] for r, s in ok)
        t1_exc = sum(s["top"][0][0] in excl[r["clase"]] for r, s in ok)
        t1_nom = sum(s["top"][0][0] == r["clase"] for r, s in ok)
        t1_dest_nom = sum(s["top1_vocab_destino"] == r["clase"] for r, s in ok)
        rangos = [s["rango_nombre"] for _, s in ok]
        margen = [s["margen"] for _, s in ok]
        out = [f"\n[{name}]  lecturas {k}, reconocidas {len(ok)}",
               f"  top-3 en vocabulario de la clase (métrica oficial) {pct(t3_dom)}",
               f"  top-3 con palabra exclusiva de la clase            {pct(t3_exc)}",
               f"  top-1 en vocabulario de la clase                  {pct(t1_dom)}",
               f"  top-1 exclusiva de la clase                       {pct(t1_exc)}",
               f"  top-1 = nombre de la clase                        {pct(t1_nom)}",
               f"  top-1 dentro del vocab. del destino = nombre      {pct(t1_dest_nom)}"]
        if rangos:
            out.append(f"  rango del nombre de la clase: mediana {np.median(rangos):.0f}, "
                       f"p90 {np.percentile(rangos, 90):.0f} (de {n_words} palabras)")
            out.append(f"  margen coseno top1-top2: mediana {np.median(margen):.3f}, p10 {np.percentile(margen, 10):.3f}")
        tops = {}
        for _, s in ok:
            tops[s["top"][0][0]] = tops.get(s["top"][0][0], 0) + 1
        out.append("  palabras top-1 más frecuentes: " +
                   ", ".join(f"{w} {c}" for w, c in sorted(tops.items(), key=lambda x: -x[1])[:10]))
        return out

    for dic in ("crudo", "cuant"):
        reads = [(r, o[dic] if o else None) for r in rows if r["destino"] for o in r["oficial"]]
        lines += block(f"oficial (muestreo, {N_REP} repeticiones) · diccionario {dic}", reads)
        reads = [(r, r["prototipo"][dic] if r["prototipo"] else None) for r in rows if r["destino"]]
        lines += block(f"prototipo (argmax) · diccionario {dic}", reads)
        stable = [r for r in rows if r["destino"] and all(r["oficial"])]
        same = sum(len({o[dic]["top"][0][0] for o in r["oficial"]}) == 1 for r in stable)
        lines.append(f"\n  estabilidad ({dic}): top-1 idéntico en las {N_REP} repeticiones en "
                     f"{same}/{len(stable)} imágenes ({100 * same / max(len(stable), 1):.1f} %)")

    lines.append("\nPor clase (oficial, crudo, top-1 = nombre / top-1 en vocab):")
    for c in CLASSES:
        rs = [(r, o["crudo"]) for r in rows if r["clase"] == c and r["destino"] for o in r["oficial"] if o]
        a = sum(s["top"][0][0] == c for _, s in rs)
        b = sum(s["top"][0][0] in vocab[c] for _, s in rs)
        lines.append(f"  {c:>6}: {a}/{len(rs)} · {b}/{len(rs)}")
    text = "\n".join(lines)
    (OUT_DIR / "parte_a_resumen.txt").write_text(text, encoding="utf-8")
    print(text)


# ---------- parte B: una palabra por objeto ----------

LAT_PATH = ROOT / "results" / "experimento16" / "latentes.npy"   # (8, 410, 16, 64)
IDX_PATH = ROOT / "results" / "experimento16" / "latentes_indice.json"
MODELS_B = OUT_DIR / "modelos_b"     # fuera de git
RAW_B = OUT_DIR / "parte_b_filas.json"
N_FILL_B, N_TEST_B, N_SEEN_B = 200, 41, 41
SEED_B = 17


def object_id(path):
    import re
    return int(re.match(r"^[a-z]+(\d+)-", Path(path).name).group(1))


def object_words():
    """Objeto k de la clase -> k-ésima palabra exclusiva de su vocabulario (sin
    el nombre de la clase). La palabra es arbitraria; lo que se prueba es si
    la memoria devuelve la que se le enseñó para ese objeto."""
    excl = exclusive_vocab()
    index = json.loads(IDX_PATH.read_text())
    out = {}
    for cls in CLASSES:
        ids = sorted({object_id(p) for p in index[cls]})
        words = [w for w in json.loads((ROOT / f"labels_{cls}.json").read_text()) if w in excl[cls] and w != cls]
        out[cls] = {oid: words[k] for k, oid in enumerate(ids)}
    return out


def split_b(index, cls):
    idx = np.arange(len(index[cls]))
    np.random.RandomState(SEED_B + CLASSES.index(cls)).shuffle(idx)
    return {"llenado": idx[:N_FILL_B].tolist(), "test": idx[N_FILL_B:N_FILL_B + N_TEST_B].tolist(),
            "vista_llenado": idx[:N_SEEN_B].tolist()}


def fill_b(cls):
    import pickle
    from hetero_memory import HeteroAssociativeMemory
    from associative_memory import HomoAssociativeMemory
    from stage5_fill import FILL_VARIANTS
    out = MODELS_B / f"{cls}.pkl"
    if out.exists():
        return cls
    t0 = time.time()
    arr = np.load(LAT_PATH, mmap_mode="r")
    index = json.loads(IDX_PATH.read_text())
    g_min, g_max = (x.astype(np.float32) for x in load_global_stats())
    ci = CLASSES.index(cls)
    words = object_words()[cls]
    raw = load_all_vectors()[cls]
    with contextlib.redirect_stdout(io.StringIO()):
        mem_H = HeteroAssociativeMemory(N_LAB, M_LABEL, P_LATENT, Q_LATENT)
        mem_R = HomoAssociativeMemory(P_LATENT, Q_LATENT)
        for i in split_b(index, cls)["llenado"]:
            w_q = quantize_binary(np.asarray(raw[words[object_id(index[cls][i])]], dtype=float), M_LABEL)
            for v in range(FILL_VARIANTS):
                z_q = quantize_latent_global(np.asarray(arr[ci, i, v]), g_min, g_max, Q_LATENT)
                mem_H.register(w_q, z_q)
                mem_R.register(z_q)
    MODELS_B.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        pickle.dump((mem_H, mem_R), f)
    print(f"  {cls}: llenado en {time.time() - t0:.0f} s", flush=True)
    return cls


def support_ranking(proj, words, dic_q):
    """Soporte de cada palabra candidata en la proyección: probabilidad media,
    coordenada por coordenada, del valor que la palabra tiene ahí."""
    p = proj / np.maximum(proj.sum(axis=1, keepdims=True), 1e-12)
    rows = np.arange(p.shape[0])
    s = [(w, float(np.mean(p[rows, dic_q[w]]))) for w in words]
    return sorted(s, key=lambda x: -x[1])


def evaluate_group_b(group):
    import pickle
    cls, items = group
    with open(MODELS_B / f"{cls}.pkl", "rb") as f:
        W["mems"] = {cls: pickle.load(f)}
    _init_b()
    return [evaluate_b(it) for it in items]


def _init_b():
    W["words"], W["raw"], W["quant"] = dictionaries()
    vecs = load_all_vectors()
    W["quant_int"] = {w: quantize_binary(np.asarray(next(vecs[c][w] for c in CLASSES if w in vecs[c]),
                                                     dtype=float), M_LABEL) for w in W["words"]}
    W["obj_words"] = object_words()
    W["arr"] = np.load(LAT_PATH, mmap_mode="r")
    W["g"] = tuple(x.astype(np.float32) for x in load_global_stats())


def evaluate_b(item):
    cls, i, path, bank, sample = item
    mem_H, mem_R = W["mems"][cls]
    ci = CLASSES.index(cls)
    truth = W["obj_words"][cls][object_id(path)]
    own = list(W["obj_words"][cls].values())
    z_q = quantize_latent_global(np.asarray(W["arr"][ci, i, 0]), *W["g"], Q_LATENT)
    row = {"clase": cls, "banco": bank, "imagen": Path(path).name, "objeto": object_id(path), "verdad": truth}
    r_w = mem_R.recog_weights(z_q)
    with contextlib.redirect_stdout(io.StringIO()):
        proj = mem_H.project(mem_H.validate(z_q, 1), _norm_weights(r_w, P_LATENT), 1)
    row["reconoce"] = bool(np.count_nonzero(np.sum(proj, axis=1) == 0) == 0)
    if not row["reconoce"]:
        return row
    proto = _to_cont(np.argmax(proj, axis=1))
    sup = support_ranking(proj, own, W["quant_int"])
    row["soporte"] = sup
    row["prototipo_propias"] = ranking(proto, own, W["quant"])[:3]
    row["prototipo_global"] = ranking(proto, W["words"], W["quant"])[:3]
    if sample:
        random.seed(100000 * ci + i)
        with contextlib.redirect_stdout(io.StringIO()):
            rec_q, recognized, *_ = mem_H.recall_from_right(z_q, weights=r_w)
        if recognized:
            p = _to_cont(rec_q)
            row["oficial_propias"] = ranking(p, own, W["quant"])[:3]
            row["oficial_global"] = ranking(p, W["words"], W["quant"])[:3]
    return row


def report_b():
    data = json.loads(RAW_B.read_text())
    rows = data["filas"]
    lines = ["Parte B: una palabra por objeto (10 por clase; azar = 10 % dentro del agente).",
             "Evaluado sobre el agente de la clase verdadera (el ruteo se mide aparte)."]
    for bank in ("test", "vista_llenado"):
        rs = [r for r in rows if r["banco"] == bank]
        rec = [r for r in rs if r["reconoce"]]
        lines.append(f"\n[{bank}] imágenes {len(rs)}, reconocidas {len(rec)} ({100 * len(rec) / max(len(rs), 1):.1f} %)")
        for key in ("soporte", "prototipo_propias", "prototipo_global", "oficial_propias", "oficial_global"):
            ok = [r for r in rec if key in r]
            if not ok:
                continue
            t1 = sum(r[key][0][0] == r["verdad"] for r in ok)
            t3 = sum(any(w == r["verdad"] for w, _ in r[key][:3]) for r in ok)
            lines.append(f"  {key:<18} n={len(ok):>3}  top-1 {100 * t1 / len(ok):5.1f} %   top-3 {100 * t3 / len(ok):5.1f} %")
        sup = [r for r in rec if "soporte" in r]
        if sup:
            m = [r["soporte"][0][1] - r["soporte"][1][1] for r in sup]
            lines.append(f"  margen de soporte top1-top2: mediana {np.median(m):.4f}")
            lines.append("  por clase (soporte, top-1):")
            for c in CLASSES:
                cs = [r for r in sup if r["clase"] == c]
                if cs:
                    lines.append(f"    {c:>6}: {sum(r['soporte'][0][0] == r['verdad'] for r in cs)}/{len(cs)}")
    text = "\n".join(lines)
    (OUT_DIR / "parte_b_resumen.txt").write_text(text, encoding="utf-8")
    print(text)


def main_b(args):
    if not args.report_only:
        t0 = time.time()
        with Pool(min(args.workers, len(CLASSES))) as pool:
            for cls in pool.imap_unordered(fill_b, CLASSES):
                print(f"  memoria {cls} lista ({time.time() - t0:.0f} s)", flush=True)
        index = json.loads(IDX_PATH.read_text())
        items = []
        for cls in CLASSES:
            sp = split_b(index, cls)
            items += [(cls, i, index[cls][i], "test", True) for i in sp["test"]]
            items += [(cls, i, index[cls][i], "vista_llenado", False) for i in sp["vista_llenado"]]
        if args.limit:
            items = items[:args.limit]
        groups = {}
        for it in items:
            groups.setdefault(it[0], []).append(it)
        rows = []
        with Pool(min(args.workers, len(groups))) as pool:
            for out in pool.imap_unordered(evaluate_group_b, groups.items()):
                rows += out
                print(f"  {out[0]['clase']} evaluada ({time.time() - t0:.0f} s)", flush=True)
        RAW_B.write_text(json.dumps({"palabras_por_objeto": object_words(), "filas": rows},
                                    indent=1, ensure_ascii=False, default=str))
        print(f"Listo en {time.time() - t0:.0f} s")
    report_b()


# ---------- parte C: el color del objeto ----------

COLORS_PATH = OUT_DIR / "colores_borrador.json"     # aprobado tal cual el 16 oct 2026
COLOR_VECS_PATH = OUT_DIR / "color_vectors.json"   # fastText crudo de las 8 palabras
N_FOLDS_C = 3


def models_c(fold):
    return OUT_DIR / ("modelos_c" if fold == 0 else f"modelos_c_lo{fold}")


def raw_c(fold):
    return OUT_DIR / ("parte_c_filas.json" if fold == 0 else f"parte_c_lo{fold}_filas.json")


def color_of(cls, path):
    lab = json.loads(COLORS_PATH.read_text(encoding="utf-8"))[cls][str(object_id(path))]
    return lab["color"] if lab["claro"] else None


def split_c(index, cls, fold=0):
    """Solo vistas de objetos con color claro. Pliegue 0: 41 vistas de test y
    hasta 200 de llenado, de los mismos objetos. Pliegue k: se reserva el
    k-ésimo objeto claro de la clase (sus 41 vistas) y se llena con los demás."""
    idx = [i for i, p in enumerate(index[cls]) if color_of(cls, p)]
    if fold == 0:
        idx = np.array(idx)
        np.random.RandomState(SEED_B + CLASSES.index(cls)).shuffle(idx)
        return {"test": idx[:N_TEST_B].tolist(), "llenado": idx[N_TEST_B:N_TEST_B + N_FILL_B].tolist()}
    held = sorted({object_id(index[cls][i]) for i in idx})[fold - 1]
    rest = np.array([i for i in idx if object_id(index[cls][i]) != held])
    np.random.RandomState(SEED_B + 100 * fold + CLASSES.index(cls)).shuffle(rest)
    return {"nuevo": [i for i in idx if object_id(index[cls][i]) == held], "llenado": rest[:N_FILL_B].tolist()}


def color_vectors_q():
    raw = json.loads(COLOR_VECS_PATH.read_text())
    return {w: quantize_binary(np.asarray(v, dtype=float), M_LABEL) for w, v in raw.items()}


def fill_c(job):
    import pickle
    from hetero_memory import HeteroAssociativeMemory
    from associative_memory import HomoAssociativeMemory
    from stage5_fill import FILL_VARIANTS
    cls, fold = job
    out = models_c(fold) / f"{cls}.pkl"
    if out.exists():
        return job
    t0 = time.time()
    arr = np.load(LAT_PATH, mmap_mode="r")
    index = json.loads(IDX_PATH.read_text())
    g_min, g_max = (x.astype(np.float32) for x in load_global_stats())
    ci = CLASSES.index(cls)
    cq = color_vectors_q()
    with contextlib.redirect_stdout(io.StringIO()):
        mem_H = HeteroAssociativeMemory(N_LAB, M_LABEL, P_LATENT, Q_LATENT)
        mem_R = HomoAssociativeMemory(P_LATENT, Q_LATENT)
        for i in split_c(index, cls, fold)["llenado"]:
            w_q = cq[color_of(cls, index[cls][i])]
            for v in range(FILL_VARIANTS):
                z_q = quantize_latent_global(np.asarray(arr[ci, i, v]), g_min, g_max, Q_LATENT)
                mem_H.register(w_q, z_q)
                mem_R.register(z_q)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        pickle.dump((mem_H, mem_R), f)
    print(f"  {cls} (pliegue {fold}): llenado en {time.time() - t0:.0f} s", flush=True)
    return job


def label_marginal(mem_H):
    """Lo que la memoria tiene del lado de la etiqueta sin mirar ninguna imagen:
    la relación sumada sobre todo el lado latente, (n, m)."""
    return mem_H._relation[:, :, :M_LABEL, :Q_LATENT].sum(axis=(1, 3)).astype(float)


def normalized_support(proj, marg, words, dic_q):
    """Soporte con la imagen dividido entre soporte sin ella (análogo de B1:
    el color más registrado no gana solo por haberse registrado más)."""
    cond = dict(support_ranking(proj, words, dic_q))
    prior = dict(support_ranking(marg, words, dic_q))
    s = [(w, cond[w] / max(prior[w], 1e-12)) for w in words]
    return sorted(s, key=lambda x: -x[1])


def evaluate_group_c(job):
    import pickle
    cls, fold = job
    with open(models_c(fold) / f"{cls}.pkl", "rb") as f:
        mem_H, mem_R = pickle.load(f)
    marg = label_marginal(mem_H)
    arr = np.load(LAT_PATH, mmap_mode="r")
    index = json.loads(IDX_PATH.read_text())
    g = tuple(x.astype(np.float32) for x in load_global_stats())
    ci = CLASSES.index(cls)
    cq = color_vectors_q()
    cont = {w: _to_cont(v) for w, v in cq.items()}
    sp = split_c(index, cls, fold)
    own = sorted({color_of(cls, index[cls][i]) for i in sp["llenado"]})
    rows = []
    for bank in [b for b in sp if b != "llenado"] + ["llenado"]:
        for i in sp[bank][:N_TEST_B]:
            path = index[cls][i]
            z_q = quantize_latent_global(np.asarray(arr[ci, i, 0]), *g, Q_LATENT)
            row = {"clase": cls, "pliegue": fold, "banco": bank, "imagen": Path(path).name,
                   "objeto": object_id(path), "verdad": color_of(cls, path), "colores_agente": own}
            with contextlib.redirect_stdout(io.StringIO()):
                proj = mem_H.project(mem_H.validate(z_q, 1), _norm_weights(mem_R.recog_weights(z_q), P_LATENT), 1)
            row["reconoce"] = bool(np.count_nonzero(np.sum(proj, axis=1) == 0) == 0)
            if row["reconoce"]:
                row["soporte_propios"] = support_ranking(proj, own, cq)
                row["soporte_norm"] = normalized_support(proj, marg, own, cq)
                row["soporte_todos"] = support_ranking(proj, list(cq), cq)
                row["prototipo_todos"] = ranking(_to_cont(np.argmax(proj, axis=1)), list(cq), cont)[:3]
            rows.append(row)
    return rows


READS_C = ("soporte_propios", "soporte_norm", "soporte_todos", "prototipo_todos")


def _block_c(rs, label):
    rec = [r for r in rs if r["reconoce"]]
    multi = [r for r in rec if len(r["colores_agente"]) > 1]
    posible = [r for r in multi if r["verdad"] in r["colores_agente"]]
    out = [f"\n[{label}] vistas {len(rs)}, reconocidas {len(rec)}; en clases con más de un color {len(multi)}"
           f" (su color está en el agente: {len(posible)})"]
    if not multi:
        return out
    for key in READS_C:
        ok = sum(r[key][0][0] == r["verdad"] for r in multi)
        bal = np.mean([np.mean([r[key][0][0] == c for r in multi if r["verdad"] == c])
                       for c in {r["verdad"] for r in multi}])
        out.append(f"  {key:<16} top-1 {100 * ok / len(multi):5.1f} %   balanceada {100 * bal:5.1f} %")
    # base: decir siempre el color más registrado en el llenado de ese agente
    base = sum(r["verdad"] == r["base"] for r in multi)
    out.append(f"  base (el color más registrado del agente) {100 * base / len(multi):5.1f} %")
    for key in ("soporte_propios", "soporte_norm"):
        out.append(f"  por clase ({key} top-1):  " + "  ".join(
            f"{c} {sum(r[key][0][0] == r['verdad'] for r in rec if r['clase'] == c)}/"
            f"{sum(r['clase'] == c for r in rec)}" for c in CLASSES if any(r["clase"] == c for r in rec)))
        conf = {}
        for r in multi:
            k = (r["verdad"], r[key][0][0])
            if k[0] != k[1]:
                conf[k] = conf.get(k, 0) + 1
        out.append(f"  confusiones ({key}): " + ", ".join(
            f"{a}->{b} {n}" for (a, b), n in sorted(conf.items(), key=lambda x: -x[1])[:6]))
    return out


def report_c(folds):
    cq = color_vectors_q()
    words = list(cq)
    diff = {(a, b): int(np.sum(cq[a] != cq[b])) for a in words for b in words if a < b}
    lines = ["Parte C: el color del objeto (8 palabras; solo objetos con color claro).",
             "Evaluado sobre el agente de la clase verdadera.",
             "Coordenadas distintas entre palabras cuantizadas (de 300): " +
             ", ".join(f"{a}-{b} {d}" for (a, b), d in sorted(diff.items(), key=lambda x: x[1])[:5]) + " …"]
    index = json.loads(IDX_PATH.read_text())
    allrows = {}
    for fold in folds:
        if not raw_c(fold).exists():
            continue
        rows = json.loads(raw_c(fold).read_text())["filas"]
        for r in rows:
            fill = [color_of(r["clase"], index[r["clase"]][i]) for i in split_c(index, r["clase"], fold)["llenado"]]
            v, n = np.unique(fill, return_counts=True)
            r["base"] = str(v[np.argmax(n)])
        allrows[fold] = rows
    if 0 in allrows:
        for bank in ("test", "llenado"):
            lines += _block_c([r for r in allrows[0] if r["banco"] == bank],
                              f"pliegue 0 · {bank} (objetos conocidos)")
    lo = [r for f in allrows if f > 0 for r in allrows[f] if r["banco"] == "nuevo"]
    if lo:
        held = sorted({(r["pliegue"], r["clase"], r["objeto"], r["verdad"]) for r in lo})
        lines.append(f"\nLeave-object-out, pliegues {sorted(f for f in allrows if f > 0)}; objetos reservados: " +
                     ", ".join(f"{c}{o}={col}" for _f, c, o, col in held))
        lines += _block_c(lo, "objetos nuevos (todos los pliegues)")
        lines += _block_c([r for f in allrows if f > 0 for r in allrows[f] if r["banco"] == "llenado"],
                          "vistas del llenado de esos pliegues")
    text = "\n".join(lines)
    (OUT_DIR / "parte_c_resumen.txt").write_text(text, encoding="utf-8")
    print(text)


def main_c(args):
    folds = [int(f) for f in args.folds.split(",")]
    if not args.report_only:
        t0 = time.time()
        classes = CLASSES[:args.limit] if args.limit else CLASSES
        jobs = [(c, f) for f in folds for c in classes]
        with Pool(min(args.workers, len(jobs))) as pool:
            for job in pool.imap_unordered(fill_c, jobs):
                print(f"  memoria {job} lista ({time.time() - t0:.0f} s)", flush=True)
        for fold in folds:
            rows = []
            with Pool(min(args.workers, len(classes))) as pool:
                for out in pool.imap_unordered(evaluate_group_c, [(c, fold) for c in classes]):
                    rows += out
            raw_c(fold).write_text(json.dumps({"filas": rows}, indent=1, ensure_ascii=False))
        print(f"Listo en {time.time() - t0:.0f} s")
    report_c(list(range(0, N_FOLDS_C + 1)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parte", choices=("a", "b", "c"), default="a")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0, help="solo las primeras N imágenes (prueba)")
    ap.add_argument("--report-only", action="store_true")
    ap.add_argument("--folds", default="0", help="parte c: pliegues separados por coma (0 = objetos conocidos)")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if args.parte == "b":
        return main_b(args)
    if args.parte == "c":
        return main_c(args)
    if not args.report_only:
        t0 = time.time()
        groups, rows, sin_energia = build_items()
        if args.limit:
            groups = {d: g[:args.limit] for d, g in list(groups.items())[:1]}
        print(f"{sum(map(len, groups.values()))} ruteadas, {len(rows)} sin ruteo, sin energía {sin_energia}; "
              f"por destino {{{', '.join(f'{d}: {len(g)}' for d, g in groups.items())}}}", flush=True)
        with Pool(min(args.workers, len(groups))) as pool:
            for out in pool.imap_unordered(evaluate_group, groups.items()):
                rows += out
                print(f"  destino {out[0]['destino']} listo ({time.time() - t0:.0f} s)", flush=True)
        rows.sort(key=lambda r: (CLASSES.index(r["clase"]), r["j"]))
        RAW_A.write_text(json.dumps({"sin_energia": sin_energia, "n_rep": N_REP, "filas": rows}, indent=1))
        print(f"Listo en {time.time() - t0:.0f} s")
    report()


if __name__ == "__main__":
    main()
