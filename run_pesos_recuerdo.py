"""
A. ¿Los pesos hacen mejor el recuerdo texto→latente, o solo distinto?
Con los modelos oficiales se recuerda con pesos uniformes, homo y marginal,
y el latente recordado se clasifica por vecino más cercano entre los
latentes de llenado. Criterio en plan_cierre_pesos_homo.md (29 oct).

Cada pasada (pesos × semilla) corre en su propio proceso; las pistas se
calculan una vez y se guardan, para no cargar fastText en cada uno.
"""
import contextlib
import io
import json
import pickle
import random
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

import run_homo_marginal as hm
from eval_bank import ALL_QUERIES, GROUND_TRUTH

s6, s7 = hm.s6, hm.s7
CLASSES = hm.CLASSES
SEEDS = (0, 100_000)
MAX_PROCS = 2          # cada pasada ocupa ~3.9 GB
CUES = Path(tempfile.gettempdir()) / "mae_tms_pistas_banco.pkl"


def bank_cues():
    if not CUES.exists():
        with contextlib.redirect_stdout(io.StringIO()):
            nlp = s6.get_nlp()
            vectors_cache = s6.load_all_vectors(nlp)
        CUES.write_bytes(pickle.dumps(hm.text_cues(list(ALL_QUERIES), nlp, vectors_cache)))
    return pickle.loads(CUES.read_bytes())


def fill_latents_q():
    """Latentes de llenado cuantizados de los ocho agentes y su clase."""
    g_min, g_max = s7.load_global_stats()
    zs, ys = [], []
    for ci, c in enumerate(CLASSES):
        raw = json.loads((s6.MODELS_DIR / f"instance_latents_{c}.json").read_text())
        zs.extend(hm.quantize_latent_global(np.asarray(z), g_min, g_max, s7.Q_IMG) for z in raw)
        ys.extend([ci] * len(raw))
    return np.stack(zs).astype(np.int16), np.asarray(ys)


def early_items(agents, cues_by_q):
    """(k, agente, índice de pista) del ganador temprano de cada consulta."""
    items = []
    for k, cues in enumerate(cues_by_q):
        if not cues:
            continue
        scores = [[agents[c].recognize_gated(v) for c in CLASSES] for v in cues]
        tot = np.sum(scores, axis=0)
        if tot.sum() <= 0:
            continue
        a = int(np.argmax(tot))
        ti = int(np.argmax([s[a] for s in scores]))
        items.append((k, a, ti))
    return items


def recall_quality(agents, cues_by_q, items, truth, bank_z, bank_y, uniform, seed):
    """Acierto del vecino más cercano del latente recordado contra la clase
    verdadera y contra el agente que recordó; distancia L1 media por coordenada."""
    hit = hit_agent = n_rec = 0
    dist = []
    for k, a, ti in items:
        cue = cues_by_q[k][ti]
        w = np.ones(len(cue)) if uniform else None
        random.seed(seed + k)
        with contextlib.redirect_stdout(io.StringIO()):
            r_q, ok, *_ = agents[CLASSES[a]].mem_dom_H.recall_from_left(cue, weights=w)
        if not ok:
            continue
        n_rec += 1
        r = np.asarray(r_q)
        d = r < s7.Q_IMG
        l1 = np.abs(bank_z[:, d] - r[d]).mean(axis=1)
        nn = int(np.argmin(l1))
        hit += int(bank_y[nn] == truth[k])
        hit_agent += int(bank_y[nn] == a)
        dist.append(float(l1[nn]))
    n = len(items)
    return {"consultas": n, "recordados": n_rec,
            "acierto_clase_verdadera_pct": 100 * hit / n,
            "vecino_en_clase_del_agente_pct": 100 * hit_agent / n,
            "distancia_l1_media": float(np.mean(dist)) if dist else None}


def one_pass(args):
    """Una pasada: heteros (oficiales o de un archivo), pesos y semilla."""
    with contextlib.redirect_stdout(io.StringIO()):
        agents = s6.load_agents()
    if args["heteros"]:
        heteros = pickle.loads(Path(args["heteros"]).read_bytes())
        for c, a in agents.items():
            a.mem_dom_H = heteros[c]
            a.mem_dom_H.attach_homo(a.mem_dom_L, a.mem_dom_R)
    cues = pickle.loads(CUES.read_bytes())
    truth = [CLASSES.index(g) for g in GROUND_TRUTH]
    bank_z, bank_y = fill_latents_q()
    items = early_items(agents, cues)
    if args["pesos"] == "marginal":
        hm.use(agents, {c: (hm.marginal_homo(a.mem_dom_H, a.mem_dom_L, 0),
                            hm.marginal_homo(a.mem_dom_H, a.mem_dom_R, 1))
                        for c, a in agents.items()})
    res = recall_quality(agents, cues, items, truth, bank_z, bank_y,
                         args["pesos"] == "uniforme", args["semilla"])
    res["ganador_temprano_acierto_pct"] = 100 * float(np.mean([a == truth[k] for k, a, _ in items]))
    Path(args["salida"]).write_text(json.dumps(res), encoding="utf-8")


def run_passes(specs):
    """{nombre: args sin 'salida'} -> {nombre: resultado}, hasta MAX_PROCS a la vez."""
    tmp = Path(tempfile.mkdtemp())
    names = list(specs)
    out = {}
    for k in range(0, len(names), MAX_PROCS):
        procs = {}
        for name in names[k:k + MAX_PROCS]:
            args = dict(specs[name], salida=str(tmp / f"{len(out) + len(procs)}.json"))
            procs[name] = (subprocess.Popen([sys.executable, __file__, "pasada", json.dumps(args)]),
                           args["salida"])
        for name, (pr, path) in procs.items():
            if pr.wait() != 0:
                raise RuntimeError(f"falló la pasada {name}")
            out[name] = json.loads(Path(path).read_text(encoding="utf-8"))
            print(name, json.dumps(out[name]), flush=True)
    return out


def main():
    hm.OUT.mkdir(parents=True, exist_ok=True)
    bank_cues()
    specs = {f"{p}_semilla_{s}": {"heteros": None, "pesos": p, "semilla": s}
             for p in ("uniforme", "homo", "marginal") for s in SEEDS}
    res = run_passes(specs)
    (hm.OUT / "pesos_recuerdo.json").write_text(json.dumps(res, indent=2, ensure_ascii=False),
                                                encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "pasada":
        one_pass(json.loads(sys.argv[2]))
    else:
        main()
