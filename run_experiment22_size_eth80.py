"""
Experimento 22: el principio de tamaño (exp20) sobre el sistema oficial de ETH-80.

Solo lee los modelos oficiales (models/agent_*.pkl, tme.pkl) y compara dos
lecturas de los mismos directorios perspectivales:
  b1      route_transactive oficial (÷conteo)
  tamano  entre los agentes que contienen la pista gana la envolvente más
          estrecha (-sum log|soporte|); entre directorios y entre pistas de
          texto se suman verosimilitudes, como B1 suma scores.
Imagen: las 656 de test (etapa 7, entrada por la clase siguiente, xi = 0).
Texto: el banco de 411 consultas (eval_bank, tokenizado como exp9/exp11),
entrada al azar con RandomState(42).
Predicción: con registro balanceado (ETH-80), tamaño ≈ B1.

Uso: python run_experiment22_size_eth80.py
"""
import contextlib
import io
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from stage6_interaction import (CLASSES, load_tme_and_agents, get_nlp, load_all_vectors,  # noqa: E402
                                route_transactive)
from stage7_bidirectional import (load_encoder, load_global_stats, image_to_latent,  # noqa: E402
                                  latent_energy_threshold, latent_has_energy, XI_VISUAL, DATA_DIR)
from stage5_fill import quantize_latent_global  # noqa: E402
from run_experiment9_member_loss import load_bank  # noqa: E402

OUT = ROOT / "results" / "experimento22"
_SUP = {}


def support(d):
    if id(d) not in _SUP:
        rel = d._ham.relation[:, :, :d._m, 1] > 0
        _SUP[id(d)] = (rel, np.log(np.maximum(rel.sum(axis=2), 1)))
    return _SUP[id(d)]


def size_scores(d, cues):
    """Log-verosimilitud por agente sumando (en verosimilitud) sobre las pistas."""
    rel, logsize = support(d)
    tot = np.full(rel.shape[1], -np.inf)
    for v in cues:
        contained = rel[np.arange(len(v)), :, v].all(axis=0)
        tot = np.logaddexp(tot, np.where(contained, -logsize.sum(axis=0), -np.inf))
    return tot


def route(agents, entry, cues, modality, reading):
    attr = "mem_dir" if modality == "text" else "mem_dir_R"

    def known_by(a):
        c = getattr(agents[a], attr).agent_counts
        return [CLASSES[int(j)] for j in np.argsort(-c) if c[j] > 0 and CLASSES[int(j)] != a]

    def scores_of(a):
        d = getattr(agents[a], attr)
        if reading == "b1":
            with contextlib.redirect_stdout(io.StringIO()):
                if modality == "text":
                    return d.route_multi(cues, mode="linear", xi=0)[1]
                return d.predict_tolerant(cues[0], xi=XI_VISUAL, mode="linear")
        return size_scores(d, cues)

    summed = set()
    total = np.zeros(len(CLASSES)) if reading == "b1" else np.full(len(CLASSES), -np.inf)
    visited, queue = set(), [entry]
    while queue:
        a = queue.pop(0)
        if a in visited:
            continue
        visited.add(a)
        for n in [a] + known_by(a):
            if n not in summed:
                summed.add(n)
                s = scores_of(n)
                total = total + s if reading == "b1" else np.logaddexp(total, s)
        if (total.sum() > 0) if reading == "b1" else np.isfinite(total).any():
            return CLASSES[int(np.argmax(total))]
        queue = [n for n in known_by(a) if n not in visited] + queue
    return None


def official(agents, entry, cues, modality):
    with contextlib.redirect_stdout(io.StringIO()):
        d, *_ = route_transactive(entry, agents, cues if modality == "text" else cues[0],
                                  modality=modality, xi=XI_VISUAL if modality == "image" else 0)
    return CLASSES[d] if d >= 0 else None


def summary(rows, read):
    n = len(rows)
    ok = sum(r[read] == r["verdad"] for r in rows)
    rej = sum(r[read] is None for r in rows)
    per = {c: f"{sum(r[read] == c for r in rows if r['verdad'] == c)}/{sum(r['verdad'] == c for r in rows)}"
           for c in CLASSES}
    return (f"acierto {100 * ok / n:5.1f} · rechazo {100 * rej / n:5.1f} · falso {100 * (n - ok - rej) / n:5.1f}", per)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()):
        _tme, agents = load_tme_and_agents()
    res = {"imagen": [], "texto": []}
    # imagen
    enc = load_encoder()
    g = load_global_stats()
    tau = latent_energy_threshold()
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    for ci, cls in enumerate(CLASSES):
        for p in splits[cls]["test"]:
            z = image_to_latent(p, enc)
            row = {"verdad": cls}
            if not latent_has_energy(z, tau):
                row.update(oficial=None, b1=None, tamano=None)
            else:
                cue = [quantize_latent_global(z, *g, 32)]
                entry = CLASSES[(ci + 1) % len(CLASSES)]
                row.update(oficial=official(agents, entry, cue, "image"),
                           b1=route(agents, entry, cue, "image", "b1"),
                           tamano=route(agents, entry, cue, "image", "tamano"))
            res["imagen"].append(row)
    # texto
    nlp = get_nlp()
    bank = load_bank(nlp, load_all_vectors(nlp))
    rng = np.random.RandomState(42)
    for it in bank:
        entry = CLASSES[rng.randint(len(CLASSES))]
        cues = [v for _t, v in it["cues"]]
        row = {"verdad": it["truth"], "consulta": it["query"]}
        if not cues:
            row.update(oficial=None, b1=None, tamano=None)
        else:
            row.update(oficial=official(agents, entry, cues, "text"),
                       b1=route(agents, entry, cues, "text", "b1"),
                       tamano=route(agents, entry, cues, "text", "tamano"))
        res["texto"].append(row)
    (OUT / "filas.json").write_text(json.dumps(res, ensure_ascii=False))
    lines = ["Exp22: principio de tamaño contra B1 sobre los modelos oficiales de ETH-80 (solo lectura)."]
    for mod, rows in res.items():
        same = sum(r["oficial"] == r["b1"] for r in rows)
        lines.append(f"\n[{mod}] n={len(rows)} · reimplementación B1 = oficial en {same}/{len(rows)}")
        for read in ("b1", "tamano"):
            s, per = summary(rows, read)
            lines.append(f"  {read:<7}: {s}")
            lines.append("    por clase: " + " · ".join(f"{c} {v}" for c, v in per.items()))
        diff = [r for r in rows if r["b1"] != r["tamano"]]
        lines.append(f"  decisiones distintas entre lecturas: {len(diff)} "
                     f"(tamaño acierta {sum(r['tamano'] == r['verdad'] for r in diff)}, "
                     f"B1 acierta {sum(r['b1'] == r['verdad'] for r in diff)})")
    text = "\n".join(lines)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
