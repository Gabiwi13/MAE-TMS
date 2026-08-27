"""Caracterizacion distribucional de los metodos de pista faltante.

Para cada pista de la tabla del reporte .SMTex (seccion 5.4) corre N_RUNS
veces cada metodo estocastico (RS, ST, SS) con semillas fijas y reporta
media +/- desviacion de la distancia de retro-proyeccion y del tiempo.
El prototipo es determinista: un solo valor por pista.

Salida: results/missing_cue/characterization.json + report.md
"""
import json
import random
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from quantizer import quantize_binary                      # noqa: E402
from stage6_interaction import (                           # noqa: E402
    M_LABEL, load_agents, load_all_vectors, get_fasttext_vector)

N_RUNS = 30
BASE_SEED = 1000
# Las mismas pistas de la tabla del reporte: token -> agente especialista.
CUES = [("pear", "pear"), ("car", "car"),
        ("green", "apple"), ("animal", "horse")]
METHODS = ["random", "sample_test", "sample_search"]
OUT_DIR = ROOT / "results" / "missing_cue"


def main():
    print("Cargando agentes y vectores...")
    agents = load_agents()
    vc = load_all_vectors()
    results = []

    for tok, cls in CUES:
        v = get_fasttext_vector(tok, vc, allow_fallback=False)
        assert v is not None, f"sin vector fastText para '{tok}'"
        q_v = quantize_binary(v, M_LABEL)
        mem = agents[cls].mem_dom_H

        proto_q, _ = mem.prototype_from_left(q_v)
        d_proto = mem.backward_distance_from_left(q_v, proto_q)
        entry = {"cue": tok, "agent": cls,
                 "prototype": {"distance": float(d_proto)}}
        print(f"\n[{tok} -> {cls}]  prototipo d={d_proto:.4f}")

        for method in METHODS:
            dists, times = [], []
            for i in range(N_RUNS):
                # hetero_lib usa el modulo random de Python; np.random por
                # si algun camino lo toca. Semilla por corrida, no por metodo.
                random.seed(BASE_SEED + i)
                np.random.seed(BASE_SEED + i)
                t0 = time.time()
                r_q, ok, _w, _p, _s = mem.recall_from_left(q_v, method=method)
                times.append(time.time() - t0)
                assert ok, f"{method} no reconocio '{tok}' (corrida {i})"
                # Metrica comun del reporte para los tres metodos.
                dists.append(mem.backward_distance_from_left(q_v, r_q))
            d = np.array(dists)
            entry[method] = {
                "mean": float(d.mean()), "std": float(d.std(ddof=1)),
                "min": float(d.min()), "max": float(d.max()),
                "zero_rate": float((d < 1e-9).mean()),
                "time_mean_s": float(np.mean(times)),
                "distances": [float(x) for x in d],
            }
            print(f"  {method:14s} d = {d.mean():.3f} +/- {d.std(ddof=1):.3f} "
                  f"[{d.min():.3f}, {d.max():.3f}]  "
                  f"d=0 en {int((d < 1e-9).sum())}/{N_RUNS}  "
                  f"t={np.mean(times):.2f}s")
        results.append(entry)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    meta = {"n_runs": N_RUNS, "base_seed": BASE_SEED,
            "date": time.strftime("%Y-%m-%d"), "results": results}
    (OUT_DIR / "characterization.json").write_text(
        json.dumps(meta, indent=2))

    lines = [
        "# Caracterizacion distribucional — pista faltante (RS/ST/SS)",
        "",
        f"{N_RUNS} corridas por metodo y pista, semillas {BASE_SEED}.."
        f"{BASE_SEED + N_RUNS - 1} (random + np.random). Metrica: distancia "
        "de retro-proyeccion (backward_distance_from_left), la misma de la "
        "tabla del reporte .SMTex. Prototipo = argmax por columna "
        "(determinista, 1 valor).",
        "",
        "| Pista | Agente | Prototipo | RS (media±σ) | ST (media±σ) | "
        "SS (media±σ) | RS d=0 | ST d=0 | SS d=0 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for e in results:
        def f(m):
            return (f"{e[m]['mean']:.3f} ± {e[m]['std']:.3f}")

        def z(m):
            return f"{int(e[m]['zero_rate'] * N_RUNS)}/{N_RUNS}"

        lines.append(
            f"| {e['cue']} | {e['agent']} | "
            f"{e['prototype']['distance']:.3f} | {f('random')} | "
            f"{f('sample_test')} | {f('sample_search')} | "
            f"{z('random')} | {z('sample_test')} | {z('sample_search')} |")
    lines += [
        "",
        "Tiempos medios por corrida: " + ", ".join(
            f"{m} {np.mean([e[m]['time_mean_s'] for e in results]):.2f}s"
            for m in METHODS) + ".",
    ]
    (OUT_DIR / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nEscrito: {OUT_DIR / 'characterization.json'}")
    print(f"Escrito: {OUT_DIR / 'report.md'}")


if __name__ == "__main__":
    main()
