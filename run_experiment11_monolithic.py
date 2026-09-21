"""
Experimento 11 — MAE monolítica contra sistema transactivo.

Mismo contenido, mismo sustrato, tres brazos:
  M            una sola memoria (hetero + dos homo) con las 8 clases; sin ruteo.
  T-oraculo    ocho especialistas; el especialista lo elige la verdad de terreno.
  T-protocolo  ocho especialistas + directorios perspectivales (v5); fase
               temprana con las consultas de formación, fase madura con
               route_transactive desde una entrada al azar.

Cortes N (imágenes por clase, x4 variantes) para los tres brazos. Diseño y
criterio de refutación en propuesta_fase5_mae_monolitica.md.

Uso:  python run_experiment11_monolithic.py [--quick] [--cuts 25,50,100,200]
          [--seeds 42-51] [--reps 3] [--workers 6] [--image] [--report-only]
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

from stage5_fill import build_label_sequence, quantize_latent_global
from stage6_interaction import (
    CLASSES, AGENT_LIST, MODELS_DIR, M_LABEL, N, P_LATENT, Q_LATENT,
    Agent, TME, get_nlp, load_all_vectors, tokenize_query, get_fasttext_vector,
    prevectorize, register_transaction, route_transactive,
)
from stage7_bidirectional import (
    load_global_stats, recognize_gated_right, evoke_labels, XI_VISUAL,
)
from hetero_memory import HeteroAssociativeMemory
from associative_memory import HomoAssociativeMemory
from quantizer import quantize_binary
from run_experiment9_member_loss import (
    Judge, load_classifier, load_bank, load_test_latents, recall_lived,
    live_levels_lived, spread,
)
from run_rejection_probe import PROBE_QUERIES

OUT_DIR = ROOT / "results" / "experimento11"
RAW_DIR = OUT_DIR / "raw"
LATENT_CACHE = ROOT / "results" / "experimento7" / "latents_cache.json"
DATA_DIR = ROOT / "data" / "eth80"

K = len(AGENT_LIST)
ARMS = ("M", "T-oraculo", "T-protocolo")
CUTS = (25, 50, 100, 200)
SEEDS = tuple(range(42, 52))
REPS = 3
N_TEXT_TRAIN_PER_CLASS = 30      # misma partición que exp10: 240 / 171
N_IMG_TRAIN = 128                # pool visual de la etapa 7 (train[200:328])
N_IMG_TEST = 10
VARIANTS = 4                     # variantes por imagen en el pool de llenado


# ---------- datos ----------

def load_pool():
    """Latentes del pool de llenado ya codificados (800 por clase, image-major)
    y secuencias de etiquetas, cuantizados como en la etapa 5. La etapa 5
    cuantizó en float32 (latentes del encoder y stats de un stack float32);
    en float64 un latente de car, cow y dog cae en otro nivel y la memoria
    deja de ser bit a bit la oficial."""
    g_min, g_max = load_global_stats()
    g_min, g_max = g_min.astype(np.float32), g_max.astype(np.float32)
    pool, seqs = {}, {}
    for cls in CLASSES:
        lat = json.loads((MODELS_DIR / f"instance_latents_{cls}.json").read_text())
        pool[cls] = [quantize_latent_global(np.array(z, dtype=np.float32), g_min, g_max, Q_LATENT)
                     for z in lat]
        seqs[cls] = build_label_sequence(cls)
    return pool, seqs


def split_bank(bank, per_class):
    """Formación: las primeras per_class consultas con pistas de cada clase;
    reservado: el resto. Es la regla de exp10.load_text."""
    train, held, seen = [], [], {c: 0 for c in CLASSES}
    for it in bank:
        if not it["cues"]:
            continue
        if seen[it["truth"]] < per_class:
            train.append(it)
        else:
            held.append(it)
        seen[it["truth"]] += 1
    return train, held


def load_ood(nlp, vectors):
    tokens = set()
    for q in PROBE_QUERIES:
        tokens.update(tokenize_query(q, nlp))
    prevectorize(vectors, tokens, allow_fallback=False)
    out = []
    for q in PROBE_QUERIES:
        cues = []
        for tok in tokenize_query(q, nlp):
            v = get_fasttext_vector(tok, vectors, allow_fallback=False)
            if v is not None:
                cues.append((tok, quantize_binary(np.asarray(v, dtype=np.float32), M_LABEL)))
        out.append({"query": q, "cues": cues})
    return out


def shared_labels():
    """Etiquetas que aparecen en el vocabulario de más de una clase."""
    count = {}
    for cls in CLASSES:
        for w in json.loads((ROOT / f"label_vectors_{cls}.json").read_text()):
            count[w] = count.get(w, 0) + 1
    return {w for w, n in count.items() if n > 1}


def load_image_pools(g_min, g_max, n_train, n_test):
    cache = json.loads(LATENT_CACHE.read_text())
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    train = []
    for ci, cls in enumerate(CLASSES):
        paths = [p for p in splits[cls]["train"][200:200 + N_IMG_TRAIN] if p in cache][:n_train]
        train.append([(quantize_latent_global(np.array(cache[p]), g_min, g_max, Q_LATENT), ci)
                      for p in paths])
    test = load_test_latents(g_min, g_max, per_class=n_test)
    return train, test


# ---------- memorias ----------

def _fill(mem_H, mem_R, seq, latents):
    L = len(seq)
    with contextlib.redirect_stdout(io.StringIO()):
        for i, z_q in enumerate(latents):
            mem_H.register(seq[i % L], z_q)
            mem_R.register(z_q)


def build_specialists(pool, seqs, n_img):
    agents = {}
    for cls in CLASSES:
        with contextlib.redirect_stdout(io.StringIO()):
            mem_H = HeteroAssociativeMemory(N, M_LABEL, P_LATENT, Q_LATENT)
            mem_L = HomoAssociativeMemory(N, M_LABEL)
            mem_R = HomoAssociativeMemory(P_LATENT, Q_LATENT)
        for v_q in seqs[cls]:
            mem_L.register(v_q)
        _fill(mem_H, mem_R, seqs[cls], pool[cls][:VARIANTS * n_img])
        agents[cls] = Agent(cls, mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)
    return agents


def build_monolithic(pool, seqs, n_img):
    """Una memoria con las ocho clases, llenada intercalando por clase. La
    relación es aditiva, así que el orden no cambia el resultado."""
    with contextlib.redirect_stdout(io.StringIO()):
        mem_H = HeteroAssociativeMemory(N, M_LABEL, P_LATENT, Q_LATENT)
        mem_L = HomoAssociativeMemory(N, M_LABEL)
        mem_R = HomoAssociativeMemory(P_LATENT, Q_LATENT)
    for cls in CLASSES:
        for v_q in seqs[cls]:
            mem_L.register(v_q)
    n = VARIANTS * n_img
    with contextlib.redirect_stdout(io.StringIO()):
        for i in range(n):
            for cls in CLASSES:
                mem_H.register(seqs[cls][i % len(seqs[cls])], pool[cls][i])
                mem_R.register(pool[cls][i])
    return Agent("monolitica", mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)


def same_as_official(agents):
    """Control: en el corte 200 los especialistas reconstruidos deben tener la
    misma relación que los agent_*.pkl oficiales."""
    import pickle
    ok = {}
    for cls in CLASSES:
        with open(MODELS_DIR / f"agent_{cls}.pkl", "rb") as f:
            official = pickle.load(f)
        ok[cls] = bool(np.array_equal(official.mem_dom_H.relation,
                                      agents[cls].mem_dom_H.relation))
    return ok


CACHE_DIR = ROOT / "cache" / "exp11"


def build_cache(cut):
    """Las memorias no dependen de la semilla: se construyen una vez por corte.
    Cada registro cuesta ~80 ms en hetero_lib, así que un corte completo tarda
    unos 17 minutos; cargarlo del caché, segundos."""
    import pickle
    path = CACHE_DIR / f"N{cut}.pkl"
    if path.exists():
        return str(path)
    t0 = time.time()
    pool, seqs = load_pool()
    specialists = build_specialists(pool, seqs, cut)
    mono = build_monolithic(pool, seqs, cut)
    control = same_as_official(specialists) if cut == 200 else None
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump({"specialists": specialists, "mono": mono, "control": control},
                    f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"  cache N={cut} construido en {time.time()-t0:.0f}s", flush=True)
    return str(path)


def load_cache(cut):
    import pickle
    with open(CACHE_DIR / f"N{cut}.pkl", "rb") as f:
        return pickle.load(f)


# Las dos relaciones de cada hetero (86 MB cada una, 9 memorias por corte) se
# comparten entre procesos en memoria compartida de solo lectura. Los procesos
# reciben un esqueleto de los objetos sin esos arreglos y los reconectan.
BIG_ATTRS = ("_relation", "_iota_relation")


def share_cut(cut):
    """Devuelve (esqueleto en bytes, lista de bloques, handles) para un corte."""
    import pickle
    from multiprocessing import shared_memory
    cached = load_cache(cut)
    agents = dict(cached["specialists"], monolitica=cached["mono"])
    blocks, handles = [], []
    for name, ag in agents.items():
        mem = ag.mem_dom_H
        with contextlib.redirect_stdout(io.StringIO()):
            _ = mem.entropy          # actualiza iota_relation y entropías si hace falta
        for attr in BIG_ATTRS:
            arr = np.ascontiguousarray(getattr(mem, attr))
            shm = shared_memory.SharedMemory(create=True, size=arr.nbytes)
            view = np.ndarray(arr.shape, dtype=arr.dtype, buffer=shm.buf)
            view[:] = arr
            blocks.append((name, attr, shm.name, arr.shape, str(arr.dtype)))
            handles.append(shm)
            setattr(mem, attr, None)
    skeleton = pickle.dumps({"agents": agents, "control": cached["control"]},
                            protocol=pickle.HIGHEST_PROTOCOL)
    return skeleton, blocks, handles


def attach_cut(skeleton, blocks):
    import pickle
    from multiprocessing import shared_memory
    data = pickle.loads(skeleton)
    handles = []
    for name, attr, shm_name, shape, dtype in blocks:
        shm = shared_memory.SharedMemory(name=shm_name)
        view = np.ndarray(shape, dtype=np.dtype(dtype), buffer=shm.buf)
        view.flags.writeable = False
        setattr(data["agents"][name].mem_dom_H, attr, view)
        handles.append(shm)
    mono = data["agents"].pop("monolitica")
    return {"specialists": data["agents"], "mono": mono,
            "control": data["control"], "_handles": handles}


# ---------- protocolo ----------

def gate_accepts(agent_list, cues):
    """Rechazo del protocolo: ningún agente da soporte a ninguna pista."""
    best = 0.0
    for _, v_q in cues:
        for ag in agent_list:
            best = max(best, ag.recognize_gated(v_q))
    return best > 0


def form_text_directories(agents, tme, train, rng):
    """Fase temprana sobre las consultas de formación: el grupo decide al
    ganador por broadcast (como process_query) y registran la transacción la
    entrada, el ganador y el TME."""
    n_reg = n_rej = ok = 0
    for it in train:
        entry = AGENT_LIST[int(rng.randint(K))]
        scores = np.zeros(K)
        for _, v_q in it["cues"]:
            for ci, cls in enumerate(CLASSES):
                scores[ci] += agents[cls].recognize_gated(v_q)
        if scores.max() == 0:
            n_rej += 1
            continue
        w = int(np.argmax(scores))
        ok += int(w == it["tidx"])
        n_reg += 1
        for _, v_q in it["cues"]:
            register_transaction(entry, w, agents, tme, v_q, "text")
    return {"registradas": n_reg, "rechazadas": n_rej,
            "acierto_temprano": ok / max(n_reg, 1)}


def form_image_directories(agents, tme, img_train, rng):
    n_reg = n_rej = ok = 0
    n = max(len(p) for p in img_train)
    for i in range(n):
        for ci in range(K):
            if i >= len(img_train[ci]):
                continue
            z_q, truth = img_train[ci][i]
            scores = {c: recognize_gated_right(agents[c], z_q) for c in CLASSES}
            if sum(scores.values()) == 0:
                n_rej += 1
                continue
            w = max(scores, key=scores.get)
            widx = AGENT_LIST.index(w)
            ok += int(widx == truth)
            n_reg += 1
            entry = AGENT_LIST[int(rng.randint(K))]
            with contextlib.redirect_stdout(io.StringIO()):
                register_transaction(entry, widx, agents, tme, z_q, "image")
    return {"registradas": n_reg, "rechazadas": n_rej,
            "acierto_temprano": ok / max(n_reg, 1)}


def compat(z_q, specialists):
    """Fracción de coordenadas del patrón con soporte en la homo latente de
    cada clase. El máximo mide si el patrón sale de una sola clase."""
    fr = [float(np.mean(specialists[c].mem_dom_R.recog_weights(z_q) > 0))
          for c in CLASSES]
    j = int(np.argmax(fr))
    return fr[j], j


def dependence(groups, reps):
    """Razón F de exp9 con corrección de Bessel; E[F]=1 si la respuesta no
    depende de la pista."""
    groups = [g for g in groups if len(g) > 1]
    if len(groups) < 2:
        return {"entre_consultas": spread([g[0] for g in groups]) if groups else float("nan"),
                "dentro_consulta": float("nan"), "F": float("nan")}
    means = np.stack([g.mean(axis=0) for g in groups])
    G = len(groups)
    var_b = float(((means - means.mean(axis=0)) ** 2).sum(axis=1).sum() / (G - 1))
    var_w = float(np.mean([((g - g.mean(axis=0)) ** 2).sum(axis=1).sum() / (len(g) - 1)
                           for g in groups]))
    return {"entre_consultas": spread([g[0] for g in groups]),
            "dentro_consulta": float(np.mean([spread(list(g)) for g in groups])),
            "F": var_b / (var_w / reps) if var_w > 0 else float("nan")}


# ---------- un trabajo (semilla, corte) ----------

def run_job(args):
    """Un trozo de las consultas reservadas de una semilla y un corte. Los
    directorios de T-protocolo se forman igual en cada trozo (la formación es
    determinista dada la semilla); el muestreo del recall usa una semilla
    distinta por trozo y la entrada de cada consulta se sortea con su índice."""
    (seed, cut, chunk, n_chunks, bank, train_idx, ood, img_pools, reps, shared,
     do_image, shm) = args
    out = RAW_DIR / f"s{seed}_N{cut}_c{chunk}.json"
    if out.exists():
        return str(out)          # la corrida se puede reanudar
    random.seed(seed * 100 + chunk)
    np.random.seed(seed * 100 + chunk)
    rng = np.random.RandomState(seed)
    t0 = time.time()

    cached = attach_cut(*shm) if shm is not None else load_cache(cut)
    specialists, mono = cached["specialists"], cached["mono"]
    g_min, g_max = load_global_stats()
    judge = Judge(load_classifier(), g_min, g_max)
    centroids = np.stack([judge.instances[c].mean(axis=0) for c in CLASSES])
    meta = {"semilla": seed, "corte": cut,
            "registros_por_clase": VARIANTS * cut,
            "registros_monolitica": VARIANTS * cut * K}
    if cached["control"] is not None:
        meta["control_igual_al_oficial"] = cached["control"]

    tme = TME()
    train_set = set(train_idx)
    train = [bank[i] for i in train_idx]
    meta["formacion_texto"] = form_text_directories(specialists, tme, train, rng)

    held_idx = [i for i, it in enumerate(bank) if it["cues"] and i not in train_set]
    mine = held_idx[chunk::n_chunks]
    rows = []
    for idx in mine:
        it = bank[idx]
        banco = "reservado"
        entry_rng = np.random.RandomState(seed * 1000 + idx)
        for arm in ARMS:
            base = {"semilla": seed, "corte": cut, "brazo": arm, "banco": banco,
                    "query": it["query"], "truth": it["truth"]}
            if arm == "M":
                responder, acepta = mono, gate_accepts([mono], it["cues"])
                base.update({"destino": "monolitica", "ruteo_ok": None})
            elif arm == "T-oraculo":
                responder = specialists[it["truth"]]
                acepta = gate_accepts(list(specialists.values()), it["cues"])
                base.update({"destino": it["truth"], "ruteo_ok": True})
            else:
                entry = AGENT_LIST[int(entry_rng.randint(K))]
                with contextlib.redirect_stdout(io.StringIO()):
                    dest, _s, consulted, hops = route_transactive(
                        entry, specialists, [v for _, v in it["cues"]], modality="text")
                acepta = dest >= 0
                responder = specialists[CLASSES[dest]] if dest >= 0 else None
                base.update({"destino": CLASSES[dest] if dest >= 0 else None,
                             "ruteo_ok": (dest == it["tidx"]) if dest >= 0 else None,
                             "entrada": entry, "consultados": len(consulted), "saltos": hops})
            zs = []
            for r in range(reps):
                row = dict(base, rep=r, acepta=acepta, responde=False)
                if responder is not None:
                    z_q, tok = recall_lived(responder, it["cues"])
                    if z_q is not None:
                        j = judge.judge(z_q, it["tidx"])
                        cmax, ccls = compat(z_q, specialists)
                        d_cent = np.linalg.norm(centroids - j["z"], axis=1)
                        row.update({
                            "responde": True, "pista": tok,
                            "pista_compartida": tok in shared,
                            "clf_ok": j["clf"] == it["tidx"],
                            "nn_ok": j["nn_cls"] == it["tidx"],
                            "centroide_ok": int(np.argmin(d_cent)) == it["tidx"],
                            "nn_cls": CLASSES[j["nn_cls"]],
                            "d_nn_truth": j["d_nn_target"], "d_nn_any": j["d_nn_any"],
                            "compat_max": cmax, "compat_ok": ccls == it["tidx"],
                            "compat_cls": CLASSES[ccls],
                            "z": [round(float(x), 4) for x in j["z"]]})
                        if r == 0:
                            row["niveles_vivos"] = live_levels_lived(responder, it["cues"])
                rows.append(row)

    ood_rows = []
    for k, it in enumerate(ood if chunk == 0 else []):
        if not it["cues"]:
            continue
        entry_rng = np.random.RandomState(seed * 1000 + 900 + k)
        for arm in ARMS:
            if arm == "M":
                acepta = gate_accepts([mono], it["cues"])
                dest = "monolitica" if acepta else None
            elif arm == "T-oraculo":
                acepta = gate_accepts(list(specialists.values()), it["cues"])
                dest = None
            else:
                entry = AGENT_LIST[int(entry_rng.randint(K))]
                with contextlib.redirect_stdout(io.StringIO()):
                    d, *_ = route_transactive(entry, specialists,
                                              [v for _, v in it["cues"]], modality="text")
                acepta, dest = d >= 0, (CLASSES[d] if d >= 0 else None)
            ood_rows.append({"semilla": seed, "corte": cut, "brazo": arm,
                             "query": it["query"], "acepta": acepta, "destino": dest})

    img_rows = []
    if do_image and chunk == 0:
        img_train, img_test = img_pools
        meta["formacion_imagen"] = form_image_directories(specialists, tme, img_train, rng)
        vectors = load_all_vectors()
        vocab = {c: set(vectors[c]) for c in CLASSES}
        all_vecs = {}
        for c in CLASSES:
            all_vecs.update(vectors[c])
        for path, z_q, ci in img_test:
            for arm in ARMS:
                row = {"semilla": seed, "corte": cut, "brazo": arm,
                       "imagen": path, "truth": CLASSES[ci]}
                if arm == "M":
                    acepta = recognize_gated_right(mono, z_q) > 0
                    responder, dest = mono, "monolitica"
                elif arm == "T-oraculo":
                    acepta = any(recognize_gated_right(specialists[c], z_q) > 0 for c in CLASSES)
                    responder, dest = specialists[CLASSES[ci]], CLASSES[ci]
                else:
                    entry = CLASSES[(ci + 1) % K]
                    with contextlib.redirect_stdout(io.StringIO()):
                        d, *_ = route_transactive(entry, specialists, z_q,
                                                  modality="image", xi=XI_VISUAL)
                    acepta = d >= 0
                    responder = specialists[CLASSES[d]] if d >= 0 else None
                    dest = CLASSES[d] if d >= 0 else None
                    row["ruteo_ok"] = (d == ci) if d >= 0 else None
                labels = evoke_labels(responder, z_q, all_vecs) if (acepta and responder) else []
                row.update({"acepta": acepta, "destino": dest, "responde": bool(labels),
                            "labels": labels, "hit": any(w in vocab[CLASSES[ci]] for w in labels)})
                img_rows.append(row)

    meta["segundos"] = round(time.time() - t0, 1)
    meta["trozo"] = chunk
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"meta": meta, "texto": rows, "ood": ood_rows,
                               "imagen": img_rows}, ensure_ascii=False))
    print(f"  s{seed} N{cut} trozo {chunk}: {len(mine)} consultas, {len(rows)} filas "
          f"({meta['segundos']}s)", flush=True)
    return str(out)


# ---------- agregación ----------

def _rate(rows, key, cond=None):
    sel = [r for r in rows if cond is None or cond(r)]
    vals = [r[key] for r in sel if r.get(key) is not None]
    return float(np.mean(vals)) if vals else float("nan")


def _ci(values):
    vals = [v for v in values if not (isinstance(v, float) and np.isnan(v))]
    if not vals:
        return [float("nan")] * 3
    if len(vals) == 1:
        return [vals[0], vals[0], vals[0]]
    rng = np.random.RandomState(0)
    boots = [float(np.mean(rng.choice(vals, size=len(vals), replace=True))) for _ in range(2000)]
    return [float(np.mean(vals)), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]


METRICS = (("acepta", "acepta", None),
           ("responde", "responde", None),
           ("nn_ok", "nn_ok", "responde"),
           ("centroide_ok", "centroide_ok", "responde"),
           ("clf_ok", "clf_ok", "responde"),
           ("d_nn_truth", "d_nn_truth", "responde"),
           ("compat_max", "compat_max", "responde"),
           ("compat_ok", "compat_ok", "responde"),
           ("niveles_vivos", "niveles_vivos", "responde"),
           ("ruteo_ok", "ruteo_ok", None),
           ("nn_ok_pista_compartida", "nn_ok", "pista_compartida"),
           ("compat_max_pista_compartida", "compat_max", "pista_compartida"),
           ("fraccion_pista_compartida", "pista_compartida", "responde"))


def load_runs():
    """Une los trozos de cada (semilla, corte) y calcula la dependencia de la
    pista (F) por brazo a partir de los latentes guardados en las filas."""
    runs = {}
    for f in sorted(RAW_DIR.glob("s*_N*_c*.json")):
        raw = json.loads(f.read_text())
        key = (raw["meta"]["semilla"], raw["meta"]["corte"])
        run = runs.setdefault(key, {"meta": raw["meta"], "texto": [], "ood": [], "imagen": []})
        for k in ("texto", "ood", "imagen"):
            run[k] += raw[k]
    for run in runs.values():
        dep = {}
        for arm in ARMS:
            by_query = {}
            for r in run["texto"]:
                if r["brazo"] == arm and r.get("responde"):
                    by_query.setdefault(r["query"], []).append(np.array(r["z"]))
            groups = [np.stack(v) for v in by_query.values()]
            reps = max((len(g) for g in groups), default=1)
            dep[arm] = dependence(groups, reps)
        run["meta"]["dependencia"] = dep
    return list(runs.values())


def aggregate():
    raws = load_runs()
    cuts = sorted({r["meta"]["corte"] for r in raws})
    seeds = sorted({r["meta"]["semilla"] for r in raws})
    summary = {"cortes": cuts, "semillas": seeds, "texto": {}, "ood": {}, "imagen": {},
               "formacion": {}, "dependencia": {}, "control": {}}
    for raw in raws:
        m = raw["meta"]
        if "control_igual_al_oficial" in m:
            summary["control"] = m["control_igual_al_oficial"]
    for cut in cuts:
        for arm in ARMS:
            key = f"{arm}|N={cut}"
            per_seed = {name: [] for name, _, _ in METRICS}
            ood_seed, img_seed, f_seed, form_seed = [], {"acepta": [], "hit": [], "ruteo_ok": []}, [], []
            for raw in raws:
                if raw["meta"]["corte"] != cut:
                    continue
                rows = [r for r in raw["texto"] if r["brazo"] == arm and r["banco"] == "reservado"]
                for name, k, cond in METRICS:
                    c = (None if cond is None else (lambda r, cond=cond: bool(r.get(cond))))
                    per_seed[name].append(_rate(rows, k, c))
                ood_seed.append(_rate([r for r in raw["ood"] if r["brazo"] == arm], "acepta"))
                img = [r for r in raw["imagen"] if r["brazo"] == arm]
                if img:
                    for k in img_seed:
                        img_seed[k].append(_rate(img, k))
                f_seed.append(raw["meta"]["dependencia"][arm]["F"])
                if arm == "T-protocolo":
                    form_seed.append(raw["meta"]["formacion_texto"])
            summary["texto"][key] = {name: _ci(v) for name, v in per_seed.items()}
            summary["ood"][key] = _ci(ood_seed)
            if img_seed["hit"]:
                summary["imagen"][key] = {k: _ci(v) for k, v in img_seed.items()}
            summary["dependencia"][key] = _ci(f_seed)
            if form_seed:
                summary["formacion"][key] = {
                    k: _ci([f[k] for f in form_seed]) for k in form_seed[0]}
    (OUT_DIR / "resumen.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


def _fmt(ci, pct=True):
    if ci is None or np.isnan(ci[0]):
        return "—"
    if pct:
        return f"{ci[0]*100:.1f} [{ci[1]*100:.1f}, {ci[2]*100:.1f}]"
    return f"{ci[0]:.2f} [{ci[1]:.2f}, {ci[2]:.2f}]"


def write_report(summary):
    L = ["# Experimento 11 — MAE monolítica contra sistema transactivo", "",
         f"Semillas: {summary['semillas']}. Cortes N (imágenes por clase, ×4 variantes): "
         f"{summary['cortes']}. Intervalos: bootstrap del 95% sobre las medias por semilla. "
         "Banco: las consultas reservadas (no usadas para formar directorios), para los tres brazos. "
         "Diseño y criterio de refutación en `propuesta_fase5_mae_monolitica.md`.", ""]
    if summary["control"]:
        ok = all(summary["control"].values())
        L += [f"Control del llenado en N=200: especialistas reconstruidos "
              f"{'idénticos' if ok else 'DISTINTOS'} a los `agent_*.pkl` oficiales "
              f"({sum(summary['control'].values())}/8 clases).", ""]
    for cut in summary["cortes"]:
        L += [f"## N = {cut} ({cut*VARIANTS} registros por clase; monolítica {cut*VARIANTS*K})", "",
              "| brazo | acepta | responde | clase 1-NN | centroide | clasificador | d_nn | compat máx | compat ok | niveles vivos | ruteo ok | F |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for arm in ARMS:
            t = summary["texto"][f"{arm}|N={cut}"]
            L.append(f"| {arm} | {_fmt(t['acepta'])} | {_fmt(t['responde'])} | {_fmt(t['nn_ok'])} | "
                     f"{_fmt(t['centroide_ok'])} | {_fmt(t['clf_ok'])} | {_fmt(t['d_nn_truth'], False)} | "
                     f"{_fmt(t['compat_max'], False)} | {_fmt(t['compat_ok'])} | "
                     f"{_fmt(t['niveles_vivos'], False)} | {_fmt(t['ruteo_ok'])} | "
                     f"{_fmt(summary['dependencia'][f'{arm}|N={cut}'], False)} |")
        L += ["", "Consultas cuya primera pista reconocida es una etiqueta compartida entre clases:", "",
              "| brazo | fracción de respuestas | clase 1-NN | compat máx |", "|---|---|---|---|"]
        for arm in ARMS:
            t = summary["texto"][f"{arm}|N={cut}"]
            L.append(f"| {arm} | {_fmt(t['fraccion_pista_compartida'])} | "
                     f"{_fmt(t['nn_ok_pista_compartida'])} | {_fmt(t['compat_max_pista_compartida'], False)} |")
        L += ["", "Fuera de dominio (12 consultas de `run_rejection_probe`): tasa de aceptación.", "",
              "| brazo | acepta |", "|---|---|"]
        for arm in ARMS:
            L.append(f"| {arm} | {_fmt(summary['ood'][f'{arm}|N={cut}'])} |")
        if f"T-protocolo|N={cut}" in summary["formacion"]:
            f = summary["formacion"][f"T-protocolo|N={cut}"]
            L += ["", f"Formación de directorios (T-protocolo): registradas {_fmt(f['registradas'], False)}, "
                  f"rechazadas {_fmt(f['rechazadas'], False)}, acierto temprano {_fmt(f['acierto_temprano'])}."]
        if f"M|N={cut}" in summary["imagen"]:
            L += ["", "Imagen → texto (top-3 domain hit):", "", "| brazo | acepta | hit | ruteo ok |", "|---|---|---|---|"]
            for arm in ARMS:
                im = summary["imagen"].get(f"{arm}|N={cut}")
                if im:
                    L.append(f"| {arm} | {_fmt(im['acepta'])} | {_fmt(im['hit'])} | {_fmt(im['ruteo_ok'])} |")
        L.append("")
    L += ["## Archivos", "- `raw/s<semilla>_N<corte>.json`: filas por consulta, sorteo y brazo",
          "- `resumen.json`: medias e intervalos", "- `fig1_clase_vs_N.png`, `fig2_dnn_vs_N.png`, "
          "`fig3_compat.png`, `fig4_ood.png`"]
    (OUT_DIR / "README.md").write_text("\n".join(L), encoding="utf-8")


def make_figures(summary):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    color = {"M": "#c0392b", "T-oraculo": "#27ae60", "T-protocolo": "#2980b9"}
    cuts = summary["cortes"]

    def curve(ax, metric, ylabel, pct):
        for arm in ARMS:
            v = np.array([summary["texto"][f"{arm}|N={c}"][metric] for c in cuts])
            f = 100 if pct else 1
            ax.errorbar(cuts, v[:, 0] * f, yerr=[(v[:, 0] - v[:, 1]) * f, (v[:, 2] - v[:, 0]) * f],
                        fmt="o-", color=color[arm], label=arm, capsize=3)
        ax.set_xlabel("N imágenes por clase"); ax.set_ylabel(ylabel); ax.legend()
        ax.spines[["top", "right"]].set_visible(False)

    fig, ax = plt.subplots(figsize=(6, 4)); curve(ax, "nn_ok", "clase correcta, 1-NN (%)", True)
    fig.tight_layout(); fig.savefig(OUT_DIR / "fig1_clase_vs_N.png", dpi=150); plt.close(fig)
    fig, ax = plt.subplots(figsize=(6, 4)); curve(ax, "d_nn_truth", "d a la instancia real más cercana", False)
    fig.tight_layout(); fig.savefig(OUT_DIR / "fig2_dnn_vs_N.png", dpi=150); plt.close(fig)

    top = cuts[-1]
    fig, ax = plt.subplots(figsize=(6, 4))
    for arm in ("M", "T-oraculo"):
        vals = []
        for f in RAW_DIR.glob(f"s*_N{top}.json"):
            raw = json.loads(f.read_text())
            vals += [r["compat_max"] for r in raw["texto"]
                     if r["brazo"] == arm and r["banco"] == "reservado" and r.get("responde")]
        ax.hist(vals, bins=np.linspace(0, 1, 21), alpha=0.6, color=color[arm], label=arm)
    ax.set_xlabel(f"compat máximo del patrón recuperado (N={top})"); ax.set_ylabel("respuestas"); ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(OUT_DIR / "fig3_compat.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    w = 0.25
    for i, arm in enumerate(ARMS):
        v = np.array([summary["ood"][f"{arm}|N={c}"] for c in cuts]) * 100
        ax.bar(np.arange(len(cuts)) + (i - 1) * w, v[:, 0], w, color=color[arm], label=arm,
               yerr=[v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], capsize=2)
    ax.set_xticks(range(len(cuts))); ax.set_xticklabels([f"N={c}" for c in cuts])
    ax.set_ylabel("consultas fuera de dominio aceptadas (%)"); ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(OUT_DIR / "fig4_ood.png", dpi=150); plt.close(fig)


# ---------- main ----------

def parse_seeds(s):
    if "-" in s:
        a, b = s.split("-")
        return tuple(range(int(a), int(b) + 1))
    return tuple(int(x) for x in s.split(","))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--cuts", default=None)
    ap.add_argument("--seeds", default=None)
    ap.add_argument("--reps", type=int, default=None)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--chunks", type=int, default=6, help="trozos por semilla y corte")
    ap.add_argument("--image", action="store_true")
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not args.report_only:
        cuts = tuple(int(c) for c in args.cuts.split(",")) if args.cuts else ((50, 200) if args.quick else CUTS)
        seeds = parse_seeds(args.seeds) if args.seeds else ((42, 43, 44) if args.quick else SEEDS)
        reps = args.reps or (1 if args.quick else REPS)
        per_class = 8 if args.quick else N_TEXT_TRAIN_PER_CLASS

        print("Preparando banco, fuera de dominio e imágenes...")
        nlp = get_nlp()
        vectors = load_all_vectors(nlp)
        bank = load_bank(nlp, vectors)
        train, held = split_bank(bank, per_class)
        if args.quick:
            keep, seen = [], {c: 0 for c in CLASSES}
            for it in held:
                if seen[it["truth"]] < 4:
                    keep.append(it); seen[it["truth"]] += 1
            held = keep
        bank = train + held
        train_idx = list(range(len(train)))
        ood = load_ood(nlp, vectors)
        shared = shared_labels()
        g_min, g_max = load_global_stats()
        img_pools = load_image_pools(g_min, g_max,
                                     16 if args.quick else N_IMG_TRAIN,
                                     2 if args.quick else N_IMG_TEST) if args.image else None
        n_held = len([it for it in bank if it["cues"]]) - len(train_idx)
        print(f"  formación {len(train_idx)} · reservadas {n_held} · fuera de dominio {len(ood)} · "
              f"cortes {cuts} · semillas {seeds} · sorteos {reps} · etiquetas compartidas {sorted(shared)}")

        t0 = time.time()
        missing = [c for c in cuts if not (CACHE_DIR / f"N{c}.pkl").exists()]
        if missing:
            print(f"Construyendo memorias de los cortes {missing}...", flush=True)
            if args.workers > 1 and len(missing) > 1:
                # Cada construcción ocupa unos 2.3 GB de RAM.
                with Pool(processes=min(3, len(missing))) as pool:
                    pool.map(build_cache, missing)
            else:
                for c in missing:
                    build_cache(c)
        if args.workers > 1:
            # Un corte a la vez: sus 9 memorias viven en memoria compartida y
            # los procesos solo cargan el esqueleto. Los cortes van en el
            # orden pedido.
            for c in cuts:
                skeleton, blocks, handles = share_cut(c)
                jobs = [(s, c, k, args.chunks, bank, train_idx, ood, img_pools, reps,
                         shared, args.image, (skeleton, blocks))
                        for s in seeds for k in range(args.chunks)]
                print(f"Corte N={c}: {len(jobs)} trabajos en {min(args.workers, len(jobs))} procesos",
                      flush=True)
                with Pool(processes=min(args.workers, len(jobs))) as pool:
                    pool.map(run_job, jobs, chunksize=1)
                for h in handles:
                    h.close(); h.unlink()
        else:
            for s in seeds:
                for c in cuts:
                    for k in range(args.chunks):
                        run_job((s, c, k, args.chunks, bank, train_idx, ood, img_pools,
                                 reps, shared, args.image, None))
        print(f"Corridas terminadas en {(time.time()-t0)/60:.1f} min")

    summary = aggregate()
    write_report(summary)
    make_figures(summary)
    print(f"Salidas -> {OUT_DIR}")


if __name__ == "__main__":
    main()
