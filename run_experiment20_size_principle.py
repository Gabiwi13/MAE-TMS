"""
Experimento 20, parte 1: leer el directorio con el principio de tamaño.

B1 divide el score de cada agente por su número de registros. El principio de
tamaño (Tenenbaum y Griffiths 2001) trata la envolvente de cada agente como una
densidad uniforme sobre su soporte: entre los agentes que contienen la pista,
log-verosimilitud = -sum_i log|soporte del agente en la coordenada i|. Gana la
envolvente más estrecha que la contiene. El recorrido (círculo, encadenado) es el
de route_transactive; entre directorios se suman las verosimilitudes, como B1
suma sus scores. Rechazar es igual en las dos lecturas: ningún agente contiene.

Predicciones fijadas antes de correr:
  1. En el completo (desbalanceado) la lectura por tamaño devuelve piel y mama a
     su modalidad y recupera melanoma a niveles cercanos al balanceado.
  2. Empeoran los dominios heterogéneos (sin hallazgo, nevo), que son anchos.

Uso: python run_experiment20_size_principle.py
"""
import contextlib
import io
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_medico_demo as demo  # noqa: E402
import stage6_interaction as s6  # noqa: E402

OUT = ROOT / "results" / "experimento20"
RUNS = {"muestra": ROOT / "results" / "medico" / "cache",
        "completo": ROOT / "results" / "medico_completo" / "cache",
        "balanceado": ROOT / "results" / "medico_balanceado" / "cache"}
LEVELS = ["nivel1"] + [f"nivel2_{m}" for m in demo.MODALITIES]


def load_pool(cache, tag):
    z = np.load(cache / f"pool_{tag}.npz", allow_pickle=False)
    names = [k[5:] for k in z.files if k.startswith("fill_")]
    return (names, {n: z[f"fill_{n}"] for n in names}, {n: z[f"a_{n}"] for n in names},
            {n: z[f"test_{n}"] for n in names})


_SUPPORT = {}


def support(d):
    """(soporte bool (64, agentes, 32), log|soporte| (64, agentes)) de un directorio."""
    key = id(d)
    if key not in _SUPPORT:
        rel = d._ham.relation[:, :, :d._m, 1] > 0            # (n, agentes, m)
        size = rel.sum(axis=2)
        _SUPPORT[key] = (rel, np.log(np.maximum(size, 1)))
    return _SUPPORT[key]


def size_scores(d, v_q):
    """Log-verosimilitud por agente; -inf si no contiene la pista."""
    rel, logsize = support(d)
    contained = rel[np.arange(len(v_q)), :, v_q].all(axis=0)
    return np.where(contained, -logsize.sum(axis=0), -np.inf)


def route(level, z, entry_idx, reading):
    """route_transactive con la lectura elegida. reading: 'b1' o 'tamano'."""
    if np.linalg.norm(z) < level.tau:
        return None
    v = level.q(z)
    names = level.names
    agents = level.agents

    def known_by(a):
        c = agents[a].mem_dir_R.agent_counts
        return [names[int(j)] for j in np.argsort(-c) if c[j] > 0 and names[int(j)] != a]

    def scores_of(a):
        if reading == "b1":
            with contextlib.redirect_stdout(io.StringIO()):
                return agents[a].mem_dir_R.predict_tolerant(v, xi=0, mode="linear")
        return size_scores(agents[a].mem_dir_R, v)

    summed = set()
    total = np.zeros(len(names)) if reading == "b1" else np.full(len(names), -np.inf)
    visited, queue = set(), [names[(entry_idx + 1) % len(names)]]
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
            return names[int(np.argmax(total))]
        queue = [n for n in known_by(a) if n not in visited] + queue
    return None


def evaluate(level, test):
    rows = []
    for k, n in enumerate(level.names):
        for z in test[n]:
            rows.append({"verdad": n, "b1": route(level, z, k, "b1"), "tamano": route(level, z, k, "tamano")})
    return rows


def check_official(level, test, n_check=200):
    """La reimplementación con B1 debe dar lo mismo que route_transactive."""
    bad = tot = 0
    for k, n in enumerate(level.names):
        for z in test[n][:max(1, n_check // len(level.names))]:
            tot += 1
            bad += int(level.route(z, k)[0] != route(level, z, k, "b1"))
    return bad, tot


def summary(rows, names, read):
    n = len(rows)
    ok = sum(r[read] == r["verdad"] for r in rows)
    rej = sum(r[read] is None for r in rows)
    bal = np.mean([np.mean([r[read] == c for r in rows if r["verdad"] == c]) for c in names])
    per = {c: f"{sum(r[read] == c for r in rows if r['verdad'] == c)}/{sum(r['verdad'] == c for r in rows)}"
           for c in names}
    return {"acierto": 100 * ok / n, "rechazo": 100 * rej / n, "falso": 100 * (n - ok - rej) / n,
            "respondido": 100 * ok / max(n - rej, 1), "balanceado": 100 * bal, "por_dominio": per}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / "tamano_filas.json"
    res = json.loads(raw.read_text()) if raw.exists() else {}
    t0 = time.time()
    for run, cache in RUNS.items():
        for tag in LEVELS:
            key = f"{run}|{tag}"
            if key in res:
                continue
            names, fill, pa, test = load_pool(cache, tag)
            _SUPPORT.clear()
            level = demo.Level(tag, names, None, fill, pa)
            bad, tot = check_official(level, test)
            rows = evaluate(level, test)
            res[key] = {"chequeo_b1": [bad, tot], "filas": rows, "nombres": names}
            raw.write_text(json.dumps(res, ensure_ascii=False))
            print(f"  {key}: chequeo B1 {tot - bad}/{tot} iguales al oficial ({time.time() - t0:.0f} s)", flush=True)
    report(res)


def report(res):
    lines = ["Exp20 parte 1: B1 (÷conteo) contra principio de tamaño, mismas memorias y directorios."]
    for key, d in res.items():
        names = d["nombres"]
        b, t = summary(d["filas"], names, "b1"), summary(d["filas"], names, "tamano")
        lines.append(f"\n[{key}] chequeo B1 = oficial en {d['chequeo_b1'][1] - d['chequeo_b1'][0]}/{d['chequeo_b1'][1]}")
        for lab, s in (("B1    ", b), ("tamaño", t)):
            lines.append(f"  {lab}: acierto {s['acierto']:5.1f} · rechazo {s['rechazo']:5.1f} · falso {s['falso']:5.1f} · "
                         f"respondido {s['respondido']:5.1f} · balanceado {s['balanceado']:5.1f}")
        lines.append("  por dominio (B1 → tamaño): " + " · ".join(
            f"{c} {b['por_dominio'][c]} → {t['por_dominio'][c]}" for c in names))
    text = "\n".join(lines)
    (OUT / "tamano_resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
