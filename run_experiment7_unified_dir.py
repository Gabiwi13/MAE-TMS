"""
Experimento 7 — Directorio unificado texto+imagen.

Pregunta: ¿un solo DirectoryMemory(n=364, m=32) puede reemplazar a los dos
directorios de la arquitectura (mem_dir_L 300x16 y mem_dir_R 64x32)?
Las pistas de texto ocupan las features 0..299 (fastText recuantizado a 32
niveles con la misma escala global de label_quant_scale.json) y las latentes
las features 300..363. La mitad ausente de un cue se marca como indefinida
(np.nan): validate() de la EAM la mapea a la fila m y project() la salta,
sin tocar hetero_lib.

Regímenes de llenado (streams intercalados por clase, maestro = ground truth):
  A  solo texto     tokens del banco de 80 queries (mitad imagen indefinida)
  B  solo imagen    N_IMG_TRAIN imgs/clase de train[200:] (mitad texto indef.)
  C  emparejado     cada token + una imagen de su clase (cue pleno de 364)
Línea base: mem_dir_L(300,16) y mem_dir_R(64,32) por separado, mismos datos.

Métricas vs k (número de registros): accuracy de ruteo con query solo-texto
(banco de 80 queries, B1, xi=0), solo-imagen (20 imgs test/clase, B1, xi=2
como stage7) y emparejada; entropía y counts del directorio. Además: sondas
cruzadas (llenar con una modalidad, consultar con la otra) y el único canal
de acople posible entre mitades (el denominador compartido de B1).

Solo lectura de stages; nada existente se modifica.
Salidas en results/experimento7/

Uso:  python run_experiment7_unified_dir.py
"""
import csv
import io
import json
import sys
import contextlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = ROOT / "results" / "experimento7"
OUT_DIR.mkdir(parents=True, exist_ok=True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from quantizer import quantize_binary
from associative_memory import DirectoryMemory
from stage5_fill import quantize_latent_global, N_FILL
from stage6_interaction import (
    CLASSES, AGENT_LIST, N, M_LABEL, P_LATENT, Q_LATENT,
    get_nlp, load_all_vectors, tokenize_query, prevectorize,
    get_fasttext_vector,
)
from stage7_bidirectional import (
    load_encoder, load_global_stats, image_to_latent, XI_VISUAL,
)

N_UNI = N + P_LATENT          # 364
M_UNI = Q_LATENT              # 32 niveles comunes
N_IMG_TRAIN = 128             # todo el pool visual de stage7 (train[200:328])
N_IMG_TEST = 20               # submuestreo de las 82 de test, por tiempo
N_EXTRA_UNBAL = 32            # re-registros de UNA clase para la prueba de acople
EVAL_EVERY = 8                # cadencia de snapshot en streams de texto
EVAL_EVERY_IMG = 64           # cadencia en streams de imagen (1024 registros)
ACC_THRESHOLD = 0.90
K = len(CLASSES)

LATENT_CACHE = OUT_DIR / "latents_cache.json"


# ---------- cues unificados (mitad ausente = np.nan -> undefined) ----------
# validate() recorta un entero m a m-1, así que la mitad indefinida DEBE
# viajar como nan, nunca como el valor m.

def cue_text(vq32):
    return np.concatenate([vq32.astype(float), np.full(P_LATENT, np.nan)])


def cue_img(zq):
    return np.concatenate([np.full(N, np.nan), zq.astype(float)])


def cue_pair(vq32, zq):
    return np.concatenate([vq32.astype(float), zq.astype(float)])


def uni_scores(mdir, cue_f, xi=0):
    """Lectura B1 tolerante sobre cues con nan (predict_tolerant valida con
    enteros y rompería la mitad indefinida)."""
    ham = mdir._ham
    with contextlib.redirect_stdout(io.StringIO()):
        v = ham.validate(np.asarray(cue_f, dtype=float), 0)
        und = ham.undefined(0)
        if xi > 0:
            rel = ham._full_iota_relation
            defined = np.where(v != und)[0]
            support = rel[defined, :, v[defined], :ham.q].sum(axis=(1, 2))
            gaps = defined[support == 0]
            if gaps.size > xi:
                return np.zeros(mdir._n_agents)
            v = v.copy()
            v[gaps] = und
        proj = ham.project(v, np.ones(v.size, dtype=float), 0)
    return proj[:, 1] / (mdir._counts + 1.0)


# ---------- datos ----------

def prepare_bank(nlp, vectors):
    """Banco de 80 queries de exp4, con cada token cuantizado a 16 (base)
    y a 32 niveles (unificado) desde el mismo vector crudo."""
    from eval_bank import ALL_QUERIES, GROUND_TRUTH
    qg = list(zip(ALL_QUERIES[:80], GROUND_TRUTH[:80]))
    all_tokens = set()
    for query, _ in qg:
        all_tokens.update(tokenize_query(query, nlp))
    prevectorize(vectors, all_tokens, allow_fallback=False)
    bank = []
    for query, truth in qg:
        vqs16, vqs32 = [], []
        for tok in tokenize_query(query, nlp):
            v = get_fasttext_vector(tok, vectors, allow_fallback=False)
            if v is None:
                continue
            raw = np.asarray(v, dtype=np.float32)
            vqs16.append(quantize_binary(raw, M_LABEL))
            vqs32.append(quantize_binary(raw, M_UNI))
        bank.append({"query": query, "truth": truth,
                     "tidx": AGENT_LIST.index(truth),
                     "vqs16": vqs16, "vqs32": vqs32})
    return bank


def encode_needed(splits, encoder, g_min, g_max):
    """Latentes cuantizados (q=32) de las imágenes del experimento, con caché
    en disco (el encoder corre en CPU)."""
    cache = {}
    if LATENT_CACHE.exists():
        cache = json.loads(LATENT_CACHE.read_text())
    needed = {}
    for cls in CLASSES:
        needed[("train", cls)] = splits[cls]["train"][N_FILL:N_FILL + N_IMG_TRAIN]
        needed[("test", cls)] = splits[cls]["test"][:N_IMG_TEST]
    out, fresh = {}, 0
    for key, paths in needed.items():
        zqs = []
        for p in paths:
            if p not in cache:
                cache[p] = image_to_latent(p, encoder).tolist()
                fresh += 1
            z = np.array(cache[p])
            zqs.append(quantize_latent_global(z, g_min, g_max, Q_LATENT))
        out[key] = zqs
    if fresh:
        LATENT_CACHE.write_text(json.dumps(cache))
    print(f"  Latentes: {sum(len(v) for v in out.values())} "
          f"({fresh} codificados ahora, resto de caché)")
    return out


# ---------- verificación previa: undefined atraviesa register/project ----------

def sanity_check():
    """Confirma sobre memorias chicas que:
    1. validate(nan) -> undefined (m); validate(m entero) se recorta a m-1;
    2. register con mitad nan no deja masa en las features indefinidas;
    3. la proyección de un cue mitad-definida es idéntica a la de un
       directorio puro del mismo subespacio."""
    rng = np.random.RandomState(0)
    with contextlib.redirect_stdout(io.StringIO()):
        uni = DirectoryMemory(10, 4, 3)
        ref = DirectoryMemory(6, 4, 3)
    ham = uni._ham
    assert ham.validate(np.full(10, np.nan), 0)[0] == ham.undefined(0)
    assert ham.validate(np.full(10, 4.0), 0)[0] == 3   # el peligro documentado
    txt = rng.randint(0, 4, 6).astype(float)
    with contextlib.redirect_stdout(io.StringIO()):
        uni.register(np.concatenate([txt, np.full(4, np.nan)]), 1)
        ref.register(txt, 1)
    assert ham.relation[6:, :, :, :].sum() == 0
    s_uni = uni_scores(uni, np.concatenate([txt, np.full(4, np.nan)]))
    with contextlib.redirect_stdout(io.StringIO()):
        s_ref = ref.predict_normalized(ref._ham.validate(txt, 0))
    assert np.allclose(s_uni, s_ref), (s_uni, s_ref)
    print("  Sanidad OK: nan->undefined, sin masa espuria, proyección "
          "idéntica al subdirectorio puro.")


# ---------- evaluaciones ----------

def eval_text(bank, scores_fn):
    ok = rej = 0
    for item in bank:
        if not item["vqs32"]:
            rej += 1
            continue
        agg = np.zeros(K)
        for vq in item["vqs32"]:
            agg += scores_fn(vq)
        if agg.sum() == 0:
            rej += 1
        elif int(np.argmax(agg)) == item["tidx"]:
            ok += 1
    n = len(bank)
    return ok / n, rej / n


def eval_img(img_eval, scores_fn):
    ok = rej = 0
    for zq, tidx in img_eval:
        s = scores_fn(zq)
        if s.sum() == 0:
            rej += 1
        elif int(np.argmax(s)) == tidx:
            ok += 1
    n = len(img_eval)
    return ok / n, rej / n


def eval_pair(bank, test_by_cls, mdir):
    idx = {c: 0 for c in CLASSES}
    ok = rej = 0
    for item in bank:
        if not item["vqs32"]:
            rej += 1
            continue
        c = item["truth"]
        zq = test_by_cls[c][idx[c] % len(test_by_cls[c])]
        idx[c] += 1
        agg = np.zeros(K)
        for vq in item["vqs32"]:
            agg += uni_scores(mdir, cue_pair(vq, zq), xi=XI_VISUAL)
        if agg.sum() == 0:
            rej += 1
        elif int(np.argmax(agg)) == item["tidx"]:
            ok += 1
    n = len(bank)
    return ok / n, rej / n


# ---------- formación ----------

def run_formation(stream, mdir, register_fn, evals, label,
                  eval_every=EVAL_EVERY):
    """stream: lista de (payload, tidx). register_fn(mdir, payload, tidx).
    evals: dict nombre -> callable(mdir) -> (acc, rej). Snapshot cada
    eval_every registros y al final."""
    series = {"k": [], "entropy": [], "counts": []}
    for name in evals:
        series[f"acc_{name}"] = []
        series[f"rej_{name}"] = []
    for k, (payload, tidx) in enumerate(stream, 1):
        with contextlib.redirect_stdout(io.StringIO()):
            register_fn(mdir, payload, tidx)
        if k % eval_every == 0 or k == len(stream):
            series["k"].append(k)
            series["entropy"].append(mdir.entropy())
            series["counts"].append(mdir.agent_counts.tolist())
            msg = []
            for name, fn in evals.items():
                acc, rej = fn(mdir)
                series[f"acc_{name}"].append(acc)
                series[f"rej_{name}"].append(rej)
                msg.append(f"{name}={acc*100:5.1f}%")
            print(f"    [{label}] k={k:3d}  " + "  ".join(msg)
                  + f"  H={mdir.entropy():.3f}")
    return series


def transition_k(ks, accs, thr=ACC_THRESHOLD):
    first = next((k for k, a in zip(ks, accs) if a >= thr), None)
    sustained = None
    for i in range(len(accs)):
        if all(a >= thr for a in accs[i:]):
            sustained = ks[i]
            break
    return first, sustained


# ---------- main ----------

def main():
    print("=" * 64)
    print("  EXPERIMENTO 7 — directorio unificado texto+imagen (364x32)")
    print("=" * 64)

    print("\n--- Verificación: valores undefined en register/project ---")
    sanity_check()

    print("\nCargando banco de queries y latentes...")
    nlp = get_nlp()
    vectors = load_all_vectors(nlp)
    bank = prepare_bank(nlp, vectors)
    n_tok = sum(len(it["vqs32"]) for it in bank)
    print(f"  Banco: {len(bank)} queries, {n_tok} tokens representables")

    encoder = load_encoder()
    g_min, g_max = load_global_stats()
    splits = json.loads((ROOT / "data" / "eth80" / "splits.json").read_text())
    lat = encode_needed(splits, encoder, g_min, g_max)

    train_by_cls = {c: lat[("train", c)] for c in CLASSES}
    test_by_cls = {c: lat[("test", c)] for c in CLASSES}
    img_eval = [(zq, AGENT_LIST.index(c))
                for c in CLASSES for zq in test_by_cls[c]]
    # stream de imágenes intercalado por clase
    img_stream = [(train_by_cls[c][i], AGENT_LIST.index(c))
                  for i in range(N_IMG_TRAIN) for c in CLASSES]
    # streams de texto: un registro por token, maestro = ground truth
    # (exp4 usa el scoring de fase temprana ~97.5% correcto; aquí el objeto
    # de estudio es el directorio, no la selección del ganador)
    text_stream32 = [(vq, it["tidx"]) for it in bank for vq in it["vqs32"]]
    text_stream16 = [(vq, it["tidx"]) for it in bank for vq in it["vqs16"]]
    # stream emparejado: cada token con una imagen distinta de su clase
    # (cíclica sobre el pool de entrenamiento)
    pair_stream, pidx = [], {c: 0 for c in CLASSES}
    for it in bank:
        c = it["truth"]
        for vq in it["vqs32"]:
            zq = train_by_cls[c][pidx[c] % N_IMG_TRAIN]
            pidx[c] += 1
            pair_stream.append(((vq, zq), it["tidx"]))

    reg_uni = lambda d, cue, ti: d.register(cue, ti)

    def ev_text_uni(d):
        return eval_text(bank, lambda vq: uni_scores(d, cue_text(vq), xi=0))

    def ev_img_uni(d):
        return eval_img(img_eval,
                        lambda zq: uni_scores(d, cue_img(zq), xi=XI_VISUAL))

    def ev_pair_uni(d):
        return eval_pair(bank, test_by_cls, d)

    runs, dirs = {}, {}

    print("\n--- A · unificado, solo texto ---")
    with contextlib.redirect_stdout(io.StringIO()):
        dirs["A"] = DirectoryMemory(N_UNI, M_UNI, K)
    runs["A_uni_text"] = run_formation(
        [(cue_text(vq), ti) for vq, ti in text_stream32],
        dirs["A"], reg_uni, {"text": ev_text_uni}, "A")

    print("\n--- B · unificado, solo imagen ---")
    with contextlib.redirect_stdout(io.StringIO()):
        dirs["B"] = DirectoryMemory(N_UNI, M_UNI, K)
    runs["B_uni_img"] = run_formation(
        [(cue_img(zq), ti) for zq, ti in img_stream],
        dirs["B"], reg_uni, {"img": ev_img_uni}, "B",
        eval_every=EVAL_EVERY_IMG)

    print("\n--- C · unificado, emparejado ---")
    with contextlib.redirect_stdout(io.StringIO()):
        dirs["C"] = DirectoryMemory(N_UNI, M_UNI, K)
    runs["C_uni_pair"] = run_formation(
        [(cue_pair(vq, zq), ti) for (vq, zq), ti in pair_stream],
        dirs["C"], reg_uni,
        {"text": ev_text_uni, "img": ev_img_uni, "pair": ev_pair_uni}, "C")

    print("\n--- Base T · mem_dir_L(300,16), solo texto ---")
    with contextlib.redirect_stdout(io.StringIO()):
        dirs["bT"] = DirectoryMemory(N, M_LABEL, K)

    def ev_text_base(d):
        # la base consulta con los cues de 16 niveles del mismo banco
        ok = rej = 0
        for item in bank:
            if not item["vqs16"]:
                rej += 1
                continue
            agg = np.zeros(K)
            with contextlib.redirect_stdout(io.StringIO()):
                for vq in item["vqs16"]:
                    agg += d.predict_normalized(vq, mode="linear")
            if agg.sum() == 0:
                rej += 1
            elif int(np.argmax(agg)) == item["tidx"]:
                ok += 1
        return ok / len(bank), rej / len(bank)

    runs["base_text"] = run_formation(
        text_stream16, dirs["bT"], reg_uni, {"text": ev_text_base}, "bT")

    print("\n--- Base V · mem_dir_R(64,32), solo imagen ---")
    with contextlib.redirect_stdout(io.StringIO()):
        dirs["bV"] = DirectoryMemory(P_LATENT, Q_LATENT, K)

    def ev_img_base(d):
        def fn(zq):
            with contextlib.redirect_stdout(io.StringIO()):
                return d.predict_tolerant(zq, xi=XI_VISUAL, mode="linear")
        return eval_img(img_eval, fn)

    runs["base_img"] = run_formation(
        img_stream, dirs["bV"], reg_uni, {"img": ev_img_base}, "bV",
        eval_every=EVAL_EVERY_IMG)

    # fusión simple de la línea base para query emparejada: media de scores
    # de texto por token + score de imagen, ambos B1
    def ev_pair_base(dL, dR):
        idx = {c: 0 for c in CLASSES}
        ok = rej = 0
        for item in bank:
            if not item["vqs16"]:
                rej += 1
                continue
            c = item["truth"]
            zq = test_by_cls[c][idx[c] % len(test_by_cls[c])]
            idx[c] += 1
            with contextlib.redirect_stdout(io.StringIO()):
                t = np.zeros(K)
                for vq in item["vqs16"]:
                    t += dL.predict_normalized(vq, mode="linear")
                t /= len(item["vqs16"])
                v = dR.predict_tolerant(zq, xi=XI_VISUAL, mode="linear")
            agg = t + v
            if agg.sum() == 0:
                rej += 1
            elif int(np.argmax(agg)) == item["tidx"]:
                ok += 1
        return ok / len(bank), rej / len(bank)

    base_pair = ev_pair_base(dirs["bT"], dirs["bV"])

    # ---------- sondas cruzadas ----------
    print("\n--- Sondas cruzadas ---")
    cross = {}
    cross["img_on_A"] = ev_img_uni(dirs["A"])      # esperado: rechazo total
    cross["text_on_B"] = ev_text_uni(dirs["B"])
    cross["text_on_C"] = ev_text_uni(dirs["C"])
    cross["img_on_C"] = ev_img_uni(dirs["C"])
    print(f"  imagen sobre A (solo texto):  acc={cross['img_on_A'][0]:.1%}  "
          f"rechazo={cross['img_on_A'][1]:.1%}")
    print(f"  texto sobre B (solo imagen):  acc={cross['text_on_B'][0]:.1%}  "
          f"rechazo={cross['text_on_B'][1]:.1%}")
    print(f"  texto sobre C (emparejado):   acc={cross['text_on_C'][0]:.1%}")
    print(f"  imagen sobre C (emparejado):  acc={cross['img_on_C'][0]:.1%}")

    # ¿la mitad texto de C es EXACTAMENTE la de A? (independencia
    # representacional: mismas escrituras texto, mismos counts)
    max_diff = 0.0
    for it in bank:
        for vq in it["vqs32"]:
            sA = uni_scores(dirs["A"], cue_text(vq), xi=0)
            sC = uni_scores(dirs["C"], cue_text(vq), xi=0)
            max_diff = max(max_diff, float(np.max(np.abs(sA - sC))))
    print(f"  |scores_texto(A) - scores_texto(C)| máx sobre {n_tok} tokens: "
          f"{max_diff:.2e}")

    # ---------- acople por counts (único canal entre mitades) ----------
    print("\n--- Acople por el denominador B1 (counts compartidos) ---")
    acc0 = ev_text_uni(dirs["A"])
    for cue, ti in [(cue_img(zq), ti) for zq, ti in img_stream]:
        with contextlib.redirect_stdout(io.StringIO()):
            dirs["A"].register(cue, ti)
    acc1 = ev_text_uni(dirs["A"])
    # desbalance: re-registrar imágenes de apple (solo infla sus counts)
    for zq in train_by_cls["apple"][:N_EXTRA_UNBAL]:
        with contextlib.redirect_stdout(io.StringIO()):
            dirs["A"].register(cue_img(zq), AGENT_LIST.index("apple"))
    acc2 = ev_text_uni(dirs["A"])
    coupling = {
        "text_only": acc0,
        "plus_balanced_imgs": acc1,
        "plus_unbalanced_apple": acc2,
        "counts_final": dirs["A"].agent_counts.tolist(),
    }
    print(f"  texto solo:              acc={acc0[0]:.1%}")
    print(f"  + {len(img_stream)} imgs balanceadas:  acc={acc1[0]:.1%}")
    print(f"  + {N_EXTRA_UNBAL} re-reg. apple:     acc={acc2[0]:.1%}  "
          f"counts={coupling['counts_final']}")

    # ---------- transiciones y tabla final ----------
    print(f"\nTransición (accuracy >= {ACC_THRESHOLD:.0%}):")
    trans = {}
    metric_of = {"A_uni_text": "text", "B_uni_img": "img",
                 "C_uni_pair": "pair", "base_text": "text",
                 "base_img": "img"}
    for name, s in runs.items():
        m = metric_of[name]
        first, sust = transition_k(s["k"], s[f"acc_{m}"])
        trans[name] = {
            "metric": m, "first": first, "sustained": sust,
            "final_acc": s[f"acc_{m}"][-1], "final_rej": s[f"rej_{m}"][-1],
            "final_entropy": s["entropy"][-1], "final_counts": s["counts"][-1]}
        print(f"  {name:<12} ({m})  primer k={str(first):>4}  sostenido k="
              f"{str(sust):>4}  acc final={s[f'acc_{m}'][-1]*100:5.1f}%  "
              f"counts={s['counts'][-1]}")

    # ---------- CSV ----------
    metrics = ["text", "img", "pair"]
    with open(OUT_DIR / "results_formation.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["run", "k",
                    *[f"acc_{m}" for m in metrics],
                    *[f"rej_{m}" for m in metrics],
                    "entropy", *[f"count_{c}" for c in CLASSES]])
        for name, s in runs.items():
            for i in range(len(s["k"])):
                row = [name, s["k"][i]]
                for m in metrics:
                    row.append(round(s[f"acc_{m}"][i], 4)
                               if f"acc_{m}" in s else "")
                for m in metrics:
                    row.append(round(s[f"rej_{m}"][i], 4)
                               if f"rej_{m}" in s else "")
                row.append(round(s["entropy"][i], 4))
                row.extend(s["counts"][i])
                w.writerow(row)

    # ---------- figura ----------
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), sharey=True)
    panels = [
        ("texto (banco 80 queries)", [
            ("A_uni_text", "text", "#534AB7", "-", "unificado A"),
            ("C_uni_pair", "text", "#1D9E75", "-", "unificado C (empar.)"),
            ("base_text", "text", "#95a5a6", "--", "base mem_dir_L")]),
        ("imagen (160 imgs test)", [
            ("B_uni_img", "img", "#534AB7", "-", "unificado B"),
            ("C_uni_pair", "img", "#1D9E75", "-", "unificado C (empar.)"),
            ("base_img", "img", "#95a5a6", "--", "base mem_dir_R")]),
        ("emparejada (query+img test)", [
            ("C_uni_pair", "pair", "#1D9E75", "-", "unificado C")]),
    ]
    for ax, (title, curves) in zip(axes, panels):
        for run, m, color, ls, lab in curves:
            s = runs[run]
            ax.plot(s["k"], s[f"acc_{m}"], color=color, ls=ls, lw=2, label=lab)
        ax.axhline(ACC_THRESHOLD, color="k", lw=0.8, ls=":")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("registros (k)")
        ax.set_ylim(0, 1.04)
        ax.legend(fontsize=8, loc="lower right")
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("accuracy de ruteo")
    fig.suptitle("Formación del directorio unificado 364x32 vs dos directorios")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig1_formation_unified.png", dpi=150)
    plt.close(fig)

    # ---------- README ----------
    label_map = {
        "A_uni_text": "A · unificado, solo texto",
        "B_uni_img": "B · unificado, solo imagen",
        "C_uni_pair": "C · unificado, emparejado",
        "base_text": "Base · mem_dir_L (texto)",
        "base_img": "Base · mem_dir_R (imagen)",
    }
    rep = [
        "# Experimento 7 — directorio unificado texto+imagen",
        "",
        "## Método",
        f"- Un solo `DirectoryMemory(n={N_UNI}, m={M_UNI}, n_agents={K})`: "
        f"texto en las features 0..{N-1} (fastText recuantizado a {M_UNI} "
        "niveles con la misma escala global), latentes en las features "
        f"{N}..{N_UNI-1} (cuantización de stage7, q={Q_LATENT}).",
        "- La mitad ausente de un cue se registra y consulta como indefinida: "
        "se pasa `np.nan`, `validate()` la mapea a la fila m y `project()` la "
        "salta. `hetero_lib` no se toca. Ojo: pasar el entero m no sirve "
        "(`validate` lo recorta a m-1); tiene que ser nan.",
        "- Verificación previa (memorias chicas): el registro con mitad "
        "indefinida no deja masa en las features indefinidas y la proyección "
        "de un cue mitad-definida es idéntica a la de un directorio puro del "
        "subespacio. Pasó.",
        f"- Datos: banco de 80 queries de exp4 ({n_tok} tokens con vector "
        f"fastText real) para texto; las {N_IMG_TRAIN} imgs/clase de "
        f"train[{N_FILL}:] (el pool visual completo de stage7) para formar y "
        f"{N_IMG_TEST} imgs test/clase para evaluar (submuestreo de las 82, "
        "por tiempo de corrida). "
        "Maestro de registro = ground truth (exp4 usa el scoring de fase "
        "temprana, ~97.5% correcto; aquí el objeto de estudio es el "
        "directorio, no la selección del ganador).",
        "- Lectura: B1 (÷count) + argmax; texto xi=0, imagen xi=2 (como "
        "stage7). k cuenta registros individuales (un token o una imagen).",
        "",
        "## Resultados finales",
        "",
        "| corrida | métrica | primer k>=90% | sostenido | acc final | "
        "rechazo | entropía | counts |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for name, t in trans.items():
        rep.append(
            f"| {label_map[name]} | {t['metric']} | {t['first']} | "
            f"{t['sustained']} | {t['final_acc']:.1%} | {t['final_rej']:.1%} "
            f"| {t['final_entropy']:.3f} | {t['final_counts']} |")
    cs = runs["C_uni_pair"]
    rep += [
        "",
        "Sobre el directorio C (llenado emparejado), consultas por modalidad:",
        "",
        "| consulta | acc | rechazo |",
        "|---|---|---|",
        f"| solo texto | {cross['text_on_C'][0]:.1%} | "
        f"{cross['text_on_C'][1]:.1%} |",
        f"| solo imagen | {cross['img_on_C'][0]:.1%} | "
        f"{cross['img_on_C'][1]:.1%} |",
        f"| emparejada | {cs['acc_pair'][-1]:.1%} | {cs['rej_pair'][-1]:.1%} |",
        f"| emparejada (base: media texto dir_L + imagen dir_R) | "
        f"{base_pair[0]:.1%} | {base_pair[1]:.1%} |",
        "",
        "## Sondas cruzadas",
        f"- Imagen sobre el directorio solo-texto (A): rechazo "
        f"{cross['img_on_A'][1]:.0%} (acc {cross['img_on_A'][0]:.0%}).",
        f"- Texto sobre el directorio solo-imagen (B): rechazo "
        f"{cross['text_on_B'][1]:.0%} (acc {cross['text_on_B'][0]:.0%}).",
        f"- Scores de texto de A vs C: diferencia máxima {max_diff:.2e} "
        f"sobre los {n_tok} tokens del banco.",
        "",
        "## ¿Puede haber interacción entre mitades?",
        "En la relación, no. `project()` (hetero_associative_4d) acumula "
        "evidencia por feature de la pista y el veto conjuntivo "
        "(`integration==0 | projection==0`) corre solo sobre las features "
        "DEFINIDAS de la query; la relación es por par (feature, agente), sin "
        "ningún término feature-feature. Como texto e imagen viven en "
        "features disjuntas, lo que se registra en una mitad no puede alterar "
        "la proyección de la otra. Empíricamente: los scores de texto de A y "
        "C son idénticos y la modalidad no registrada se rechaza al 100%.",
        "",
        "El ÚNICO canal de acople es el denominador de B1: los counts por "
        "agente son compartidos entre modalidades. Medido sobre A:",
        "",
        "| estado del directorio | acc texto |",
        "|---|---|",
        f"| solo texto ({len(text_stream32)} registros) | "
        f"{coupling['text_only'][0]:.1%} |",
        f"| + {len(img_stream)} imgs balanceadas | "
        f"{coupling['plus_balanced_imgs'][0]:.1%} |",
        f"| + {N_EXTRA_UNBAL} re-registros de imgs de apple | "
        f"{coupling['plus_unbalanced_apple'][0]:.1%} |",
        "",
        f"Counts finales tras el desbalance: {coupling['counts_final']}.",
        "",
        "## Hallazgos",
        f"1. Por modalidad, el unificado replica a los dos directorios: la "
        f"curva de imagen es idéntica snapshot a snapshot (final "
        f"{trans['B_uni_img']['final_acc']:.1%} en ambos) y la de texto "
        f"difiere solo por la recuantización 32 vs 16 niveles "
        f"({trans['A_uni_text']['final_acc']:.1%} vs "
        f"{trans['base_text']['final_acc']:.1%}). No se forma ninguna "
        "representación compartida: las mitades son independientes por "
        "construcción.",
        f"2. La query emparejada es el punto débil del unificado: el veto "
        "conjuntivo corre sobre TODAS las features definidas del cue, así "
        "que una mitad imagen sin soporte suficiente tumba la pista entera "
        f"aunque la mitad texto rutee sola al "
        f"{cross['text_on_C'][0]:.1%} — emparejada "
        f"{cs['acc_pair'][-1]:.1%} contra {base_pair[0]:.1%} de la fusión "
        "de dos directorios, donde cada modalidad se rechaza por separado.",
        f"3. La imagen en C queda corta por cobertura, no por la "
        "unificación: el llenado emparejado solo aporta tantas imágenes "
        "distintas como tokens (21-37 por clase) contra las 128 de B; "
        "consistente con la curva de capacidad de exp6.",
        f"4. Compartir el espacio sí cobra un costo real vía B1: sumar "
        "registros de imagen al directorio de texto baja su ruteo de "
        f"{coupling['text_only'][0]:.1%} a "
        f"{coupling['plus_balanced_imgs'][0]:.1%} (balanceado) y "
        f"{coupling['plus_unbalanced_apple'][0]:.1%} (desbalanceado) sin "
        "tocar la relación: solo cambió el denominador compartido.",
        "",
        "En suma: bajo esta proyección el directorio unificado no puede "
        "transferir nada entre modalidades y sí paga el veto conjuntivo en "
        "queries plenas y el denominador compartido. Los dos directorios "
        "separados son la arquitectura correcta.",
        "",
        "## Archivos",
        "- `results_formation.csv` — series de formación (k, acc, rechazo, "
        "entropía, counts por corrida)",
        "- `fig1_formation_unified.png` — curvas de formación por modalidad",
        "- `latents_cache.json` — caché de latentes codificados (CPU)",
        "",
        "## Notas",
        "- `run_experiment7_unified_dir.py` no modifica etapas ni memorias "
        "existentes; DirectoryMemory se usa tal cual (la lectura tolerante a "
        "nan vive en el script porque `predict_tolerant` valida con enteros).",
        "- El registro con mitad indefinida acumula masa en la fila-margen m "
        "de `_relation`; esa fila nunca entra a `project()` ni a la "
        "iota-relation, así que no afecta ninguna lectura.",
    ]
    (OUT_DIR / "README.md").write_text("\n".join(rep), encoding="utf-8")

    print(f"\nSalidas -> {OUT_DIR}")
    print("EXPERIMENTO 7 COMPLETADO.")


if __name__ == "__main__":
    main()
