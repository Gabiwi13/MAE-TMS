"""
Experimento 10 — Directorios perspectivales y ruteo encadenado.

En el protocolo actual todos los agentes registran todos los broadcasts, así
que los ocho directorios son la misma relación (exp8) y el TME es una novena
copia. Eso deja dos lecturas teóricas indistinguibles:

  Vygotsky (1978): la coordinación aparece primero entre agentes (el TME de la
  fase temprana) y después dentro de cada uno. Pero cada quien internaliza lo
  que participó, desde su posición: los directorios deberían ser parciales y
  distintos, y el grupo rutea encadenando lo que cada uno sabe de los demás.

  Hutchins (1995): la coordinación vive en un artefacto compartido (un
  pizarrón) que nadie internaliza del todo; el grupo lo consulta.

Aquí cada agente presencia solo una parte de los broadcasts ajenos, bajo dos
modelos de perspectiva:
  azar f    presencia cada broadcast ajeno con probabilidad f;
  anillo r  presencia solo los broadcasts ganados por agentes a distancia <= r
            en un anillo (vecindad estructurada).

Y el grupo rutea de tres maneras:
  directo     el agente de entrada consulta su directorio; sin soporte, rechaza
              (protocolo actual de la fase madura);
  encadenado  sin soporte, pregunta a los agentes que conoce (los que vio ganar
              algo), por orden de familiaridad, y la consulta salta hasta que
              alguien tiene soporte o se agotan los conocidos;
  agregado    pregunta a todos los que conoce y suma sus scores calibrados: la
              decisión es comparativa entre perspectivas, no la del primero
              que tiene soporte.

La referencia es el pizarrón: un directorio único con todos los registros
(equivale a f=1 directo). Se mide acierto, rechazo, error, saltos, y cuánto
difieren los directorios entre sí (perspectiva).

Uso:  python run_experiment10_perspectival_routing.py [--quick]
"""
import argparse
import contextlib
import csv
import io
import json
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from associative_memory import DirectoryMemory
from quantizer import quantize_binary
from stage5_fill import N_FILL, quantize_latent_global
from stage6_interaction import (
    CLASSES, AGENT_LIST, M_LABEL, P_LATENT, Q_LATENT, N,
    get_nlp, tokenize_query, get_fasttext_vector, prevectorize,
    load_all_vectors,
)
from stage7_bidirectional import load_global_stats, XI_VISUAL

OUT_DIR = ROOT / "results" / "experimento10"
DATA_DIR = ROOT / "data" / "eth80"
LATENT_CACHE = ROOT / "results" / "experimento7" / "latents_cache.json"

K = len(AGENT_LIST)
SEED = 42
SEEDS = (42, 43, 44)
N_IMG_TRAIN = 128
N_IMG_TEST = 20
N_TEXT_TRAIN_PER_CLASS = 30        # 240 consultas de formación, el resto se reserva
FRACTIONS = (0.0, 1 / 64, 1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2, 1.0)
RADII = (0, 1, 2, 3, 4)
PROTOCOLS = ("directo", "encadenado", "agregado")
# Lectura estricta tambien en imagen: con xi>0 los huecos se definen sobre el
# soporte de TODOS los agentes del directorio, asi que lo que presenciaron los
# demas cambiaria la tolerancia del propio dominio y confundiria la curva.
XI_IMG = 0

plt.rcParams.update({"figure.dpi": 300, "savefig.dpi": 300,
                     "font.family": "DejaVu Sans", "font.size": 10})
COLOR = {"directo": "#c0392b", "encadenado": "#2980b9", "agregado": "#27ae60",
         "pizarron": "#7f8c8d"}


# ---------- datos ----------

def load_text(nlp, vectors, quick=False):
    """Consultas del banco de 8 clases, tokenizadas y cuantizadas. Formación:
    las primeras N_TEXT_TRAIN_PER_CLASS por clase; reservado: el resto."""
    from eval_bank import ALL_QUERIES, GROUND_TRUTH
    pairs = list(zip(ALL_QUERIES, GROUND_TRUTH))
    tokens = set()
    for q, _ in pairs:
        tokens.update(tokenize_query(q, nlp))
    prevectorize(vectors, tokens, allow_fallback=False)
    train, held = [], []
    seen = {c: 0 for c in CLASSES}
    n_train = 8 if quick else N_TEXT_TRAIN_PER_CLASS
    for q, t in pairs:
        cues = []
        for tok in tokenize_query(q, nlp):
            v = get_fasttext_vector(tok, vectors, allow_fallback=False)
            if v is not None:
                cues.append(quantize_binary(np.asarray(v, dtype=np.float32), M_LABEL))
        if not cues:
            continue
        item = {"query": q, "tidx": AGENT_LIST.index(t), "cues": cues}
        if seen[t] < n_train:
            train.append(item); seen[t] += 1
        elif not quick or seen[t] < n_train + 4:
            held.append(item); seen[t] += 1
    return train, held


def load_images(g_min, g_max, quick=False):
    cache = json.loads(LATENT_CACHE.read_text())
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    n_tr = 32 if quick else N_IMG_TRAIN
    n_te = 5 if quick else N_IMG_TEST
    train, test = [], []
    for ci, cls in enumerate(CLASSES):
        tr = [p for p in splits[cls]["train"][N_FILL:N_FILL + N_IMG_TRAIN] if p in cache][:n_tr]
        te = [p for p in splits[cls]["test"] if p in cache][:n_te]
        train.append([(quantize_latent_global(np.array(cache[p]), g_min, g_max, Q_LATENT), ci)
                      for p in tr])
        test += [(quantize_latent_global(np.array(cache[p]), g_min, g_max, Q_LATENT), ci)
                 for p in te]
    # intercalado por clase, como la etapa 7
    stream = [train[ci][i] for i in range(len(train[0])) for ci in range(K)]
    return stream, test


# ---------- perspectiva ----------

def ring_distance(i, j):
    d = abs(i - j)
    return min(d, K - d)


def build_directories(text_stream, img_stream, witness, rng):
    """witness(i, winner) -> bool: el agente i presencia ese broadcast.
    El ganador siempre registra lo suyo. Devuelve (dirs_texto, dirs_imagen,
    pizarron_texto, pizarron_imagen)."""
    with contextlib.redirect_stdout(io.StringIO()):
        dirs_t = [DirectoryMemory(N, M_LABEL, K) for _ in range(K)]
        dirs_i = [DirectoryMemory(P_LATENT, Q_LATENT, K) for _ in range(K)]
        board_t = DirectoryMemory(N, M_LABEL, K)
        board_i = DirectoryMemory(P_LATENT, Q_LATENT, K)
    with contextlib.redirect_stdout(io.StringIO()):
        for dirs, board, stream in ((dirs_t, board_t, text_stream),
                                    (dirs_i, board_i, img_stream)):
            for v_q, w in stream:
                board.register(v_q, w)
                for i in range(K):
                    if i == w or witness(i, w, rng):
                        dirs[i].register(v_q, w)
    return dirs_t, dirs_i, board_t, board_i


def perspective_stats(dirs, m):
    """Cuánto difieren los directorios: distancia de Jaccard media entre los
    soportes (celdas con masa en la cara 'ganó') de cada par de agentes, y
    a cuántos agentes conoce cada uno (vio ganar algo)."""
    sup = [np.asarray(d._ham._full_iota_relation)[:, :, :m, 1] > 0 for d in dirs]
    jac = []
    for i in range(K):
        for j in range(i + 1, K):
            inter = np.logical_and(sup[i], sup[j]).sum()
            union = np.logical_or(sup[i], sup[j]).sum()
            jac.append(1.0 - inter / union if union else 0.0)
    known = [int((d.agent_counts > 0).sum()) for d in dirs]
    return {"divergencia_jaccard": float(np.mean(jac)),
            "conocidos_por_agente": float(np.mean(known)),
            "entropia_media": float(np.mean([d.entropy() for d in dirs]))}


# ---------- ruteo ----------

def route_text(d, cues):
    with contextlib.redirect_stdout(io.StringIO()):
        dest, _ = d.route_multi(cues, mode="linear")
    return dest


def route_img(d, z_q):
    with contextlib.redirect_stdout(io.StringIO()):
        return d.route(z_q, mode="linear", xi=XI_IMG)


def scores_text(d, cues):
    with contextlib.redirect_stdout(io.StringIO()):
        _, total = d.route_multi(cues, mode="linear")
    return total


def scores_img(d, z_q):
    with contextlib.redirect_stdout(io.StringIO()):
        return d.predict_normalized(z_q, mode="linear")


def route_aggregate(dirs, entry, payload, scores_fn):
    """Consulta agregada: el agente de entrada suma los scores calibrados de
    su directorio y de los de todos los agentes que conoce, y decide por
    argmax. Devuelve (destino, consultas)."""
    counts = dirs[entry].agent_counts
    asked = [entry] + [int(j) for j in np.argsort(-counts) if counts[j] > 0 and j != entry]
    total = np.zeros(K)
    for a in asked:
        total += scores_fn(dirs[a], payload)
    dest = -1 if total.sum() == 0 else int(np.argmax(total))
    return dest, len(asked)


def route_chain(dirs, entry, payload, route_fn):
    """Consulta encadenada: el agente consultado rutea si tiene soporte; si no,
    pasa la consulta a los agentes que conoce, por familiaridad (registros
    que les vio ganar), sin repetir. Devuelve (destino, consultas)."""
    visited, stack, consults = set(), [entry], 0
    while stack:
        a = stack.pop(0)
        if a in visited:
            continue
        visited.add(a); consults += 1
        dest = route_fn(dirs[a], payload)
        if dest >= 0:
            return dest, consults
        counts = dirs[a].agent_counts
        acq = [int(j) for j in np.argsort(-counts)
               if counts[j] > 0 and j != a and j not in visited]
        stack = acq + stack
    return -1, consults


def evaluate(dirs, board, items, route_fn, payload_of, scores_fn):
    """Todas las consultas por todas las entradas, bajo los dos protocolos y
    el pizarrón."""
    def blank():
        return {"ok": 0, "rej": 0, "err": 0, "err_menos_presenciado": 0,
                "consults_ok": [], "consults_rej": [], "n": 0}
    res = {p: blank() for p in PROTOCOLS}
    res["pizarron"] = blank()

    def tally(r, dest, truth, consults, counts=None):
        r["n"] += 1
        if dest < 0:
            r["rej"] += 1; r["consults_rej"].append(consults)
            return
        r["consults_ok"].append(consults)
        if dest == truth:
            r["ok"] += 1
        else:
            r["err"] += 1
            # el error va hacia un agente del que el directorio consultado
            # tiene menos registros que del agente correcto: la calibracion
            # B1 (÷count) infla a los poco presenciados
            if counts is not None and counts[dest] < counts[truth]:
                r["err_menos_presenciado"] += 1

    for it in items:
        payload, truth = payload_of(it), it["tidx"]
        tally(res["pizarron"], route_fn(board, payload), truth, 1)
        for entry in range(K):
            d0 = route_fn(dirs[entry], payload)
            tally(res["directo"], d0, truth, 1, dirs[entry].agent_counts)
            if d0 >= 0:
                dc, nc = d0, 1
            else:
                dc, nc = route_chain(dirs, entry, payload, route_fn)
            tally(res["encadenado"], dc, truth, nc)
            da, na = route_aggregate(dirs, entry, payload, scores_fn)
            tally(res["agregado"], da, truth, na)
    out = {}
    for p, r in res.items():
        n = max(r["n"], 1)
        out[p] = {"acierto": r["ok"] / n, "rechazo": r["rej"] / n, "error": r["err"] / n,
                  "error_hacia_menos_presenciado": (r["err_menos_presenciado"] / r["err"]
                                                    if r["err"] else float("nan")),
                  "saltos_media": (float(np.mean(r["consults_ok"])) - 1.0
                                   if r["consults_ok"] else float("nan")),
                  "consultas_en_rechazo": (float(np.mean(r["consults_rej"]))
                                           if r["consults_rej"] else float("nan")),
                  "n": r["n"]}
    return out


# ---------- corrida ----------

def run_condition(model, level, seed, text_train, text_held, img_train, img_test):
    text_stream = [(v, it["tidx"]) for it in text_train for v in it["cues"]]
    rng = np.random.RandomState(seed)
    if model == "azar":
        witness = lambda i, w, r: r.random() < level
    else:
        witness = lambda i, w, r: ring_distance(i, w) <= level
    dirs_t, dirs_i, board_t, board_i = build_directories(text_stream, img_train, witness, rng)
    rows = []
    persp = {"texto": perspective_stats(dirs_t, M_LABEL),
             "imagen": perspective_stats(dirs_i, Q_LATENT)}
    banks = (("texto_formacion", dirs_t, board_t, text_train, route_text, scores_text,
              lambda it: it["cues"]),
             ("texto_reservado", dirs_t, board_t, text_held, route_text, scores_text,
              lambda it: it["cues"]),
             ("imagen_test", dirs_i, board_i, img_test, route_img, scores_img,
              lambda it: it["z"]))
    for bank, dirs, board, items, fn, sfn, pay in banks:
        ev = evaluate(dirs, board, items, fn, pay, sfn)
        for proto, m in ev.items():
            rows.append({"modelo": model, "nivel": level, "semilla": seed, "banco": bank,
                         "protocolo": proto, **m,
                         **{f"persp_{k}": v for k, v in
                            persp["imagen" if bank.startswith("imagen") else "texto"].items()}})
    return rows


def aggregate(rows):
    """Media sobre semillas por (modelo, nivel, banco, protocolo)."""
    keys = {}
    for r in rows:
        k = (r["modelo"], r["nivel"], r["banco"], r["protocolo"])
        keys.setdefault(k, []).append(r)
    agg = []
    for (model, level, bank, proto), rs in keys.items():
        row = {"modelo": model, "nivel": level, "banco": bank, "protocolo": proto,
               "semillas": len(rs)}
        for f in ("acierto", "rechazo", "error", "error_hacia_menos_presenciado",
                  "saltos_media", "consultas_en_rechazo",
                  "persp_divergencia_jaccard", "persp_conocidos_por_agente",
                  "persp_entropia_media"):
            row[f] = float(np.nanmean([r[f] for r in rs]))
        agg.append(row)
    return agg


def figures(agg):
    def pick(model, bank, proto, field):
        levels = sorted({r["nivel"] for r in agg if r["modelo"] == model})
        ys = []
        for lv in levels:
            rs = [r for r in agg if r["modelo"] == model and r["nivel"] == lv
                  and r["banco"] == bank and r["protocolo"] == proto]
            ys.append(rs[0][field] if rs else np.nan)
        return levels, ys

    banks = (("texto_formacion", "texto · consultas de formación"),
             ("texto_reservado", "texto · consultas reservadas"),
             ("imagen_test", "imagen · test"))
    for model, xlabel, fname in (("azar", "fracción presenciada de los broadcasts ajenos (f)",
                                  "fig1_azar.png"),
                                 ("anillo", "radio de vecindad presenciada (r)",
                                  "fig2_anillo.png")):
        fig, axes = plt.subplots(2, 3, figsize=(13, 7))
        for col, (bank, title) in enumerate(banks):
            ax = axes[0, col]
            for proto in PROTOCOLS:
                x, y = pick(model, bank, proto, "acierto")
                ax.plot(x, y, "o-", color=COLOR[proto], label=proto)
            x, y = pick(model, bank, "pizarron", "acierto")
            ax.axhline(np.nanmean(y), color=COLOR["pizarron"], ls="--", label="pizarrón (compartido)")
            for proto in PROTOCOLS:
                x, y = pick(model, bank, proto, "error")
                ax.plot(x, y, "x:", color=COLOR[proto], alpha=0.7,
                        label=f"{proto} · error")
            if model == "azar":
                ax.set_xscale("symlog", linthresh=1 / 64)
            ax.set_ylim(-0.03, 1.03); ax.set_title(title, fontsize=10)
            ax.grid(alpha=0.3)
            if col == 0:
                ax.set_ylabel("proporción"); ax.legend(fontsize=7, loc="center right")
            ax = axes[1, col]
            x, y = pick(model, bank, "encadenado", "saltos_media")
            ax.plot(x, y, "s-", color=COLOR["encadenado"], label="saltos (encadenado)")
            ax2 = ax.twinx()
            x, y = pick(model, bank, "directo", "persp_divergencia_jaccard")
            ax2.plot(x, y, "d-", color="#8e44ad", label="divergencia entre directorios")
            ax2.set_ylim(-0.03, 1.03)
            if model == "azar":
                ax.set_xscale("symlog", linthresh=1 / 64)
            ax.set_xlabel(xlabel); ax.grid(alpha=0.3)
            if col == 0:
                ax.set_ylabel("saltos promedio")
            if col == 2:
                ax2.set_ylabel("divergencia Jaccard", color="#8e44ad")
            h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
            if col == 0:
                ax.legend(h1 + h2, l1 + l2, fontsize=7, loc="upper right")
        fig.suptitle(f"Directorios perspectivales ({model}): directo, encadenado, agregado, pizarrón",
                     fontsize=12)
        fig.tight_layout()
        path = OUT_DIR / fname
        fig.savefig(path, bbox_inches="tight"); plt.close(fig)
        print(f"  -> {path}")


def write_csv(rows, path):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(rows)
    print(f"  -> {path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Cargando consultas e imágenes...")
    nlp = get_nlp()
    vectors = load_all_vectors(nlp)
    text_train, text_held = load_text(nlp, vectors, quick=args.quick)
    g_min, g_max = load_global_stats()
    img_train, img_test = load_images(g_min, g_max, quick=args.quick)
    text_stream = [(v, it["tidx"]) for it in text_train for v in it["cues"]]
    img_items = [{"z": z, "tidx": c} for z, c in img_test]
    print(f"  texto: {len(text_train)} consultas de formación ({len(text_stream)} pistas), "
          f"{len(text_held)} reservadas · imagen: {len(img_train)} formación, {len(img_test)} test")

    seeds = SEEDS[:1] if args.quick else SEEDS
    rows, t0 = [], time.time()
    conditions = [("azar", f) for f in FRACTIONS] + [("anillo", r) for r in RADII]
    for model, level in conditions:
        for seed in (seeds if model == "azar" else seeds[:1]):
            rs = run_condition(model, level, seed, text_train, text_held, img_train, img_items)
            rows += rs
            line = []
            for bank in ("texto_formacion", "texto_reservado", "imagen_test"):
                d = next(r for r in rs if r["banco"] == bank and r["protocolo"] == "directo")
                e = next(r for r in rs if r["banco"] == bank and r["protocolo"] == "encadenado")
                g = next(r for r in rs if r["banco"] == bank and r["protocolo"] == "agregado")
                line.append(f"{bank[:6]} dir {d['acierto']*100:4.1f} enc {e['acierto']*100:4.1f}"
                            f" (saltos {e['saltos_media']:.2f}) agr {g['acierto']*100:4.1f}")
            print(f"  {model:>6} {level:<7.4g} s{seed}  " + " | ".join(line)
                  + f"  ({time.time()-t0:.0f}s)", flush=True)
    write_csv(rows, OUT_DIR / ("results_quick.csv" if args.quick else "results_raw.csv"))
    agg = aggregate(rows)
    write_csv(agg, OUT_DIR / ("results_agg_quick.csv" if args.quick else "results.csv"))
    if not args.quick:
        figures(agg)


if __name__ == "__main__":
    main()
