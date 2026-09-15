"""
Distribuciones de las cantidades muestreadas de exp8 y exp9 (fase 1 de la
revisión). Cada cantidad se estima con N sorteos de semillas distintas, bajo
dos pistas de identidad para la lectura inversa del directorio:

  ceros  1 en el agente k y 0 explícito en los demás (la pista original de
         exp8/exp9: la columna de muestreo queda en 6·N_all + 2·N_k)
  nan    1 en k y nan (indefinido) en los demás (la columna es la propia de k)

Se fijan random.seed y np.random.seed por sorteo: el muestreador de
hetero_lib usa el módulo random de Python.

Partes:
  fidelidad   directorio visual v4 (car, idéntico entre agentes): por clase,
              distancia a la instancia real más cercana, dispersión entre
              sorteos, acierto de clase (clasificador y vecino real)
  capacidad   directorios nuevos con N registros por agente (como exp8):
              distancia, dispersión, acierto por N
  exp9        política descripción de exp9 (texto -> imagen): fidelidad de la
              envolvente por clase perdida, contra el recall vivido del
              especialista (independiente de la pista; se corre una vez)

Uso: python run_sampling_distributions.py --condition ceros|nan [--seeds 20]
         [--parts fidelidad capacidad exp9] [--skip-lived]
"""
import argparse
import contextlib
import io
import json
import pickle
import random
import sys
import time
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from associative_memory import DirectoryMemory
from quantizer import quantize_binary
from stage5_fill import quantize_latent_global
from stage6_interaction import (CLASSES, AGENT_LIST, MODELS_DIR, DEVICE, M_LABEL,
                                P_LATENT, Q_LATENT, get_nlp, load_all_vectors)
from stage7_bidirectional import load_global_stats

K = len(AGENT_LIST)
REPS = 10
CAPACITY_SIZES = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 800)
OUT8 = ROOT / "results" / "experimento8"
OUT9 = ROOT / "results" / "experimento9"


def set_identity_cue(condition: str):
    """Fija la pista de identidad que usa DirectoryMemory.recall_domain."""
    def zeros(self, agent_idx):
        cue = np.zeros(self._n_agents, dtype=np.int32)
        cue[int(agent_idx)] = 1
        return cue

    def nans(self, agent_idx):
        cue = np.full(self._n_agents, np.nan)
        cue[int(agent_idx)] = 1.0
        return cue
    DirectoryMemory._identity_cue = zeros if condition == "ceros" else nans


def seed_all(s):
    random.seed(s)
    np.random.seed(s)


def dequantize(z_q, g_min, g_max):
    return ((np.asarray(z_q, dtype=float) / (Q_LATENT - 1)) * (g_max - g_min) + g_min).astype(np.float32)


def load_agent(name):
    with open(MODELS_DIR / f"agent_{name}.pkl", "rb") as f:
        return pickle.load(f)


def load_classifier():
    from stage2_encoder import Classifier
    clf = Classifier().to(DEVICE)
    clf.load_state_dict(torch.load(MODELS_DIR / "classifier.pt", map_location=DEVICE))
    clf.eval()
    return clf


class Judge:
    def __init__(self, g_min, g_max):
        self.g_min, self.g_max = g_min, g_max
        self.clf = load_classifier()
        self.inst = {c: np.array(json.loads((MODELS_DIR / f"instance_latents_{c}.json").read_text()),
                                 dtype=np.float32) for c in CLASSES}
        self.all_inst = np.concatenate([self.inst[c] for c in CLASSES])
        self.all_cls = np.concatenate([[ci] * len(self.inst[c]) for ci, c in enumerate(CLASSES)])

    def judge(self, z_q, k):
        z = dequantize(z_q, self.g_min, self.g_max)
        with torch.no_grad():
            clf = int(self.clf(torch.tensor(z).unsqueeze(0).to(DEVICE)).argmax(1))
        d_all = np.linalg.norm(self.all_inst - z, axis=1)
        nn = int(self.all_cls[int(np.argmin(d_all))])
        d_k = float(np.linalg.norm(self.inst[CLASSES[k]] - z, axis=1).min())
        return z, clf == k, nn == k, d_k


def spread(zs):
    if len(zs) < 2:
        return float("nan")
    return float(np.mean([np.linalg.norm(zs[i] - zs[j]) for i in range(len(zs)) for j in range(i + 1, len(zs))]))


def part_fidelidad(mdir, judge, seeds):
    out = []
    for s in seeds:
        seed_all(s)
        row = {"semilla": s}
        for k, c in enumerate(CLASSES):
            zs, dks, clf_ok, nn_ok = [], [], 0, 0
            for _ in range(REPS):
                z_q, ok = mdir.recall_domain(k)
                if not ok:
                    continue
                z, a, b, dk = judge.judge(z_q, k)
                zs.append(z); dks.append(dk); clf_ok += a; nn_ok += b
            row[c] = {"responde": len(zs) / REPS, "d_nn": float(np.mean(dks)) if dks else float("nan"),
                      "dispersion": spread(zs), "acierto_clf": clf_ok / max(len(zs), 1),
                      "acierto_nn": nn_ok / max(len(zs), 1)}
        out.append(row)
        print(f"  fidelidad semilla {s}: d_nn medio {np.mean([row[c]['d_nn'] for c in CLASSES]):.2f}", flush=True)
    return out


def part_capacidad(judge, g_min, g_max, seeds):
    qz = {c: [quantize_latent_global(z, g_min, g_max, Q_LATENT) for z in judge.inst[c]] for c in CLASSES}
    dirs = {}
    for N in CAPACITY_SIZES:
        with contextlib.redirect_stdout(io.StringIO()):
            d = DirectoryMemory(P_LATENT, Q_LATENT, K)
            for ci, c in enumerate(CLASSES):
                for z_q in qz[c][:N]:
                    d.register(z_q, ci)
        dirs[N] = d
    out = []
    for s in seeds:
        seed_all(s)
        row = {"semilla": s}
        t0 = time.time()
        for N in CAPACITY_SIZES:
            reps = 1 if N == 1 else REPS      # con un registro por agente el recall es determinista
            dks, disp, hit, tot = [], [], 0, 0
            for k, c in enumerate(CLASSES):
                zs = []
                for _ in range(reps):
                    z_q, ok = dirs[N].recall_domain(k)
                    if not ok:
                        continue
                    z, a, _b, dk = judge.judge(z_q, k)
                    zs.append(z); dks.append(dk); hit += a; tot += 1
                if len(zs) > 1:
                    disp.append(spread(zs))
            row[str(N)] = {"d_nn": float(np.mean(dks)), "dispersion": float(np.mean(disp)) if disp else 0.0,
                           "acierto": hit / max(tot, 1), "sorteos": tot}
        out.append(row)
        print(f"  capacidad semilla {s}: d_nn N=8 {row['8']['d_nn']:.1f}  N=800 {row['800']['d_nn']:.1f} "
              f"acierto N=800 {row['800']['acierto']:.3f}  ({time.time()-t0:.0f}s)", flush=True)
    return out


def routed_queries(survivor_dir_by_k, nlp, vectors):
    """Consultas del banco ruteadas a su propia clase k por el directorio de
    texto (determinista): las mismas que llegan a las políticas de exp9."""
    from eval_bank import ALL_QUERIES, GROUND_TRUTH
    from stage6_interaction import tokenize_query, get_fasttext_vector, prevectorize
    pairs = list(zip(ALL_QUERIES, GROUND_TRUTH))
    toks = set()
    for q, _ in pairs:
        toks.update(tokenize_query(q, nlp))
    prevectorize(vectors, toks, allow_fallback=False)
    routed = {k: [] for k in range(K)}
    for q, t in pairs:
        k = AGENT_LIST.index(t)
        cues = []
        for tok in tokenize_query(q, nlp):
            v = get_fasttext_vector(tok, vectors, allow_fallback=False)
            if v is not None:
                cues.append(quantize_binary(np.asarray(v, dtype=np.float32), M_LABEL))
        if not cues:
            continue
        with contextlib.redirect_stdout(io.StringIO()):
            dest, _ = survivor_dir_by_k[k].route_multi(cues, mode="linear")
        if dest == k:
            routed[k].append((q, cues))
    return routed


def part_exp9(agents, judge, seeds, skip_lived, only_lived=False):
    nlp = get_nlp()
    vectors = load_all_vectors(nlp)
    survivors = {k: agents[CLASSES[(k + 1) % K]] for k in range(K)}
    routed = routed_queries({k: survivors[k].mem_dir for k in range(K)}, nlp, vectors)
    print("  consultas ruteadas a k:", {CLASSES[k]: len(v) for k, v in routed.items()}, flush=True)
    out = {"consultas_ruteadas": {CLASSES[k]: len(v) for k, v in routed.items()}, "descripcion": [], "vivido": []}
    for s in seeds:
        t0 = time.time()
        seed_all(s)
        row = {"semilla": s}
        for k, c in enumerate(CLASSES):
            dks, zs, ok_nn, n = [], [], 0, 0
            for _q, _cues in ([] if only_lived else routed[k]):
                z_q, ok = survivors[k].mem_dir_R.recall_domain(k)
                if not ok:
                    continue
                z, _a, b, dk = judge.judge(z_q, k)
                dks.append(dk); zs.append(z); ok_nn += b; n += 1
            row[c] = {"responde": n / max(len(routed[k]), 1), "d_nn": float(np.mean(dks)) if dks else float("nan"),
                      "dispersion_entre_consultas": spread(zs), "acierto_nn": ok_nn / max(n, 1)}
        if not only_lived:
            out["descripcion"].append(row)
        msg = f"  exp9 semilla {s}:" + ("" if only_lived else
              f" descripcion d_nn medio {np.nanmean([row[c]['d_nn'] for c in CLASSES]):.2f}")
        if not skip_lived:
            seed_all(s)
            rowl = {"semilla": s}
            for k, c in enumerate(CLASSES):
                dks, zs, ok_nn, n, tried = [], [], 0, 0, 0
                for _q, cues in routed[k]:
                    tried += 1
                    for v_q in cues:
                        with contextlib.redirect_stdout(io.StringIO()):
                            z_q, recognized, *_ = agents[c].mem_dom_H.recall_from_left(v_q)
                        if recognized:
                            z, _a, b, dk = judge.judge(z_q, k)
                            dks.append(dk); zs.append(z); ok_nn += b; n += 1
                            break
                rowl[c] = {"responde": n / max(tried, 1), "d_nn": float(np.mean(dks)) if dks else float("nan"),
                           "dispersion_entre_consultas": spread(zs), "acierto_nn": ok_nn / max(n, 1)}
            out["vivido"].append(rowl)
            msg += f"  vivido {np.nanmean([rowl[c]['d_nn'] for c in CLASSES]):.2f}"
        print(msg + f"  ({time.time()-t0:.0f}s)", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", choices=("ceros", "nan"), required=True)
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--parts", nargs="+", default=("fidelidad", "capacidad", "exp9"))
    ap.add_argument("--skip-lived", action="store_true")
    ap.add_argument("--only-lived", action="store_true",
                    help="solo el recall vivido del especialista (no depende de la pista)")
    args = ap.parse_args()
    set_identity_cue(args.condition)
    seeds = list(range(1000, 1000 + args.seeds))
    g_min, g_max = load_global_stats()
    judge = Judge(g_min, g_max)
    tag = args.condition

    if "fidelidad" in args.parts or "capacidad" in args.parts:
        res = {"condicion": tag, "semillas": seeds, "reps_por_sorteo": REPS,
               "modelos": "directorios v4 (models_backup_pre_perspectival), car"}
        if "fidelidad" in args.parts:
            car = load_agent("car")
            print("fidelidad", flush=True)
            res["fidelidad"] = part_fidelidad(car.mem_dir_R, judge, seeds)
            del car
        if "capacidad" in args.parts:
            print("capacidad", flush=True)
            res["capacidad"] = part_capacidad(judge, g_min, g_max, seeds)
        path = OUT8 / f"muestreo_{tag}.json"
        path.write_text(json.dumps(res, indent=1))
        print(f"-> {path}")
    if "exp9" in args.parts:
        agents = {c: load_agent(c) for c in CLASSES}
        print("exp9", flush=True)
        res = {"condicion": tag, "semillas": seeds,
               **part_exp9(agents, judge, seeds, args.skip_lived, args.only_lived)}
        path = OUT9 / ("muestreo_vivido.json" if args.only_lived else f"muestreo_{tag}.json")
        path.write_text(json.dumps(res, indent=1))
        print(f"-> {path}")


if __name__ == "__main__":
    main()
