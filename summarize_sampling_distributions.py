"""
Resume los muestreos de run_sampling_distributions.py: media y desviación
estándar sobre semillas (y rango) de cada cantidad, condición ceros contra nan.
Escribe results/experimento8/muestreo_resumen.json y
results/experimento9/muestreo_resumen.json e imprime las tablas.
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from stage6_interaction import CLASSES

OUT8 = ROOT / "results" / "experimento8"
OUT9 = ROOT / "results" / "experimento9"
CAPACITY_SIZES = ("1", "2", "4", "8", "16", "32", "64", "128", "256", "512", "800")


def stats(values):
    v = np.array([x for x in values if x is not None and not np.isnan(x)], dtype=float)
    if v.size == 0:
        return {"media": float("nan"), "sd": float("nan"), "min": float("nan"), "max": float("nan"), "n": 0}
    return {"media": float(v.mean()), "sd": float(v.std(ddof=1)) if v.size > 1 else 0.0,
            "min": float(v.min()), "max": float(v.max()), "n": int(v.size)}


def fmt(s):
    return f"{s['media']:.2f} ± {s['sd']:.2f} [{s['min']:.1f}, {s['max']:.1f}]"


def load(path):
    return json.loads(path.read_text()) if path.exists() else None


def summarize_exp8():
    res = {}
    data = {c: load(OUT8 / f"muestreo_{c}.json") for c in ("ceros", "nan")}
    for cond, d in data.items():
        if d is None:
            continue
        r = {"semillas": len(d["semillas"])}
        if "fidelidad" in d:
            r["fidelidad"] = {c: {k: stats([row[c][k] for row in d["fidelidad"]])
                                  for k in ("d_nn", "dispersion", "acierto_clf", "acierto_nn", "responde")}
                              for c in CLASSES}
            r["fidelidad"]["media_clases"] = {k: stats([np.mean([row[c][k] for c in CLASSES])
                                                        for row in d["fidelidad"]])
                                              for k in ("d_nn", "dispersion", "acierto_clf", "acierto_nn")}
        if "capacidad" in d:
            r["capacidad"] = {N: {k: stats([row[N][k] for row in d["capacidad"]])
                                  for k in ("d_nn", "dispersion", "acierto")} for N in CAPACITY_SIZES}
        res[cond] = r
    (OUT8 / "muestreo_resumen.json").write_text(json.dumps(res, indent=1))

    print("\n== exp8 · fidelidad por clase (d a instancia real más cercana; media ± sd [min, max] sobre semillas)")
    print(f"{'clase':8s} {'ceros':>34s} {'nan':>34s}")
    for c in CLASSES + ["media_clases"]:
        row = [c]
        for cond in ("ceros", "nan"):
            row.append(fmt(res[cond]["fidelidad"][c]["d_nn"]) if cond in res and "fidelidad" in res[cond] else "—")
        print(f"{row[0]:8s} {row[1]:>34s} {row[2]:>34s}")
    print("\n== exp8 · dispersión entre sorteos por clase")
    for c in CLASSES + ["media_clases"]:
        row = [fmt(res[cond]["fidelidad"][c]["dispersion"]) if cond in res and "fidelidad" in res[cond] else "—"
               for cond in ("ceros", "nan")]
        print(f"{c:8s} {row[0]:>34s} {row[1]:>34s}")
    print("\n== exp8 · acierto de clase (vecino real / clasificador), media sobre clases")
    for cond in ("ceros", "nan"):
        if cond in res and "fidelidad" in res[cond]:
            m = res[cond]["fidelidad"]["media_clases"]
            print(f"  {cond}: vecino {fmt(m['acierto_nn'])}  clasificador {fmt(m['acierto_clf'])}")
    print("\n== exp8 · capacidad por registros por agente (d_nn | dispersión | acierto)")
    for N in CAPACITY_SIZES:
        row = [f"N={N:>3s}"]
        for cond in ("ceros", "nan"):
            if cond in res and "capacidad" in res[cond]:
                s = res[cond]["capacidad"][N]
                row.append(f"{s['d_nn']['media']:5.1f}±{s['d_nn']['sd']:.1f} | {s['dispersion']['media']:5.1f}±{s['dispersion']['sd']:.1f} | {s['acierto']['media']:.3f} [{s['acierto']['min']:.3f}, {s['acierto']['max']:.3f}]")
            else:
                row.append("—")
        print(f"  {row[0]}  ceros: {row[1]:<48s} nan: {row[2]}")
    return res


def summarize_exp9():
    res = {}
    for cond in ("ceros", "nan"):
        d = load(OUT9 / f"muestreo_{cond}.json")
        if d is None or not d.get("descripcion"):
            continue
        rows = d["descripcion"]
        res[cond] = {"semillas": len(rows), "consultas_ruteadas": d["consultas_ruteadas"],
                     "descripcion": {c: {k: stats([r[c][k] for r in rows])
                                         for k in ("d_nn", "dispersion_entre_consultas", "acierto_nn", "responde")}
                                     for c in CLASSES}}
        res[cond]["descripcion"]["media_clases"] = {
            k: stats([np.nanmean([r[c][k] for c in CLASSES]) for r in rows])
            for k in ("d_nn", "dispersion_entre_consultas", "acierto_nn", "responde")}
    dv = load(OUT9 / "muestreo_vivido.json")
    if dv and dv.get("vivido"):
        rows = dv["vivido"]
        res["vivido"] = {"semillas": len(rows),
                         "vivido": {c: {k: stats([r[c][k] for r in rows])
                                        for k in ("d_nn", "dispersion_entre_consultas", "acierto_nn", "responde")}
                                    for c in CLASSES}}
        res["vivido"]["vivido"]["media_clases"] = {
            k: stats([np.nanmean([r[c][k] for c in CLASSES]) for r in rows])
            for k in ("d_nn", "dispersion_entre_consultas", "acierto_nn", "responde")}
    (OUT9 / "muestreo_resumen.json").write_text(json.dumps(res, indent=1))

    print("\n== exp9 · fidelidad de la respuesta por clase perdida (d a instancia real más cercana de k)")
    print(f"{'clase':8s} {'descripción ceros':>34s} {'descripción nan':>34s} {'vivido (especialista)':>34s}")
    for c in CLASSES + ["media_clases"]:
        cells = []
        for key in ("ceros", "nan"):
            cells.append(fmt(res[key]["descripcion"][c]["d_nn"]) if key in res else "—")
        cells.append(fmt(res["vivido"]["vivido"][c]["d_nn"]) if "vivido" in res else "—")
        print(f"{c:8s} {cells[0]:>34s} {cells[1]:>34s} {cells[2]:>34s}")
    print("\n== exp9 · acierto de clase por vecino real (media sobre clases) y semillas")
    for key, sub in (("ceros", "descripcion"), ("nan", "descripcion"), ("vivido", "vivido")):
        if key in res:
            m = res[key][sub]["media_clases"]
            print(f"  {key}: acierto {fmt(m['acierto_nn'])}  responde {fmt(m['responde'])}  semillas {res[key]['semillas']}")
    return res


if __name__ == "__main__":
    summarize_exp8()
    summarize_exp9()
