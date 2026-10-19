"""
Experimento 21: memoria única contra partición, sobre el demo médico.

Mismo contenido (pozo de la muestra: 200 de llenado x 16 variantes por agente,
fase A 128) y mismo test, por nivel:
  M              una sola memoria hetero imagen <-> etiqueta con todos los dominios;
                 la etiqueta es el vector fastText del término del dominio (media de
                 sus palabras, terminos.json), como en exp11. Decide por el soporte
                 de cada etiqueta en la proyección; rechaza si la proyección tiene
                 una fila vacía.
  T-especialistas  una memoria por dominio; decide el especialista que reconoce con
                 más fuerza (recognize_gated_right), sin directorio.
  T-protocolo    el sistema con directorios perspectivales (route_transactive).
Predicción (exp11-12): M confunde más entre dominios cuyos términos comparten
palabras (lados izquierdo/derecho, queratosis actínica/benigna).

Uso: python run_experiment21_monolitica.py [--workers 5]
"""
import argparse
import contextlib
import io
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

OUT = ROOT / "results" / "experimento21"
CACHE = ROOT / "results" / "medico" / "cache"
LEVELS = {"nivel1": "nivel1", "nivel2_tc_abdomen": "tc_abdomen", "nivel2_dermatoscopia": "dermatoscopia",
          "nivel2_rx_torax": "rx_torax", "nivel2_us_mama": "us_mama"}


def label_vectors(level_key, names):
    from quantizer import quantize_binary
    terms = json.loads((OUT / "medico_terminos.json").read_text())[level_key]
    ft = json.loads((OUT / "medico_terminos_fasttext.json").read_text())
    out = {}
    for n, t in zip(names, terms):
        v = np.mean([np.asarray(ft[w], dtype=float) for w in t.split()], axis=0)
        out[n] = quantize_binary(v, 16)
    return out, dict(zip(names, terms))


def run_level(tag):
    import run_medico_demo as demo
    import run_experiment20_size_principle as e20
    from stage7_bidirectional import recognize_gated_right
    from hetero_memory import HeteroAssociativeMemory, _norm_weights
    from associative_memory import HomoAssociativeMemory
    from run_experiment17_specific_word import support_ranking
    t0 = time.time()
    names, fill, pa, test = e20.load_pool(CACHE, tag)
    lv, terms = label_vectors(LEVELS[tag], names)
    level = demo.Level(tag, names, None, fill, pa)            # T-especialistas y T-protocolo
    with contextlib.redirect_stdout(io.StringIO()):
        mem_H = HeteroAssociativeMemory(300, 16, 64, 32)
        mem_R = HomoAssociativeMemory(64, 32)
    n_max = max(len(fill[n]) for n in names)
    for i in range(n_max):                                     # intercalado por dominio
        for n in names:
            if i < len(fill[n]):
                for z in fill[n][i]:
                    zq = level.q(z)
                    mem_H.register(lv[n], zq)
                    mem_R.register(zq)
    t_fill = time.time() - t0
    rows = []
    for k, n in enumerate(names):
        for z in test[n]:
            row = {"verdad": n}
            if np.linalg.norm(z) < level.tau:
                row.update(M=None, esp=None, prot=None)
                rows.append(row)
                continue
            zq = level.q(z)
            with contextlib.redirect_stdout(io.StringIO()):
                proj = mem_H.project(mem_H.validate(zq, 1), _norm_weights(mem_R.recog_weights(zq), 64), 1)
            ok = np.count_nonzero(np.sum(proj, axis=1) == 0) == 0
            row["M"] = support_ranking(proj, names, lv)[0][0] if ok else None
            sc = {m: recognize_gated_right(level.agents[m], zq) for m in names}
            row["esp"] = max(sc, key=sc.get) if sum(sc.values()) > 0 else None
            row["prot"] = level.route(z, k)[0]
            rows.append(row)
    print(f"  {tag}: llenado de M {t_fill / 60:.0f} min, total {(time.time() - t0) / 60:.0f} min", flush=True)
    return tag, {"nombres": names, "terminos": terms, "filas": rows, "minutos_llenado_M": round(t_fill / 60, 1)}


def summarize(d, arm):
    rows, names = d["filas"], d["nombres"]
    n = len(rows)
    ok = sum(r[arm] == r["verdad"] for r in rows)
    rej = sum(r[arm] is None for r in rows)
    bal = np.mean([np.mean([r[arm] == c for r in rows if r["verdad"] == c]) for c in names])
    conf = {}
    for r in rows:
        if r[arm] and r[arm] != r["verdad"]:
            conf[(r["verdad"], r[arm])] = conf.get((r["verdad"], r[arm]), 0) + 1
    return (f"acierto {100 * ok / n:5.1f} · rechazo {100 * rej / n:5.1f} · falso {100 * (n - ok - rej) / n:5.1f} · "
            f"respondido {100 * ok / max(n - rej, 1):5.1f} · balanceado {100 * bal:5.1f}",
            sorted(conf.items(), key=lambda x: -x[1])[:5])


def report(res):
    lines = ["Exp21: memoria única (M) contra especialistas (sin directorio) y protocolo transactivo, mismo contenido."]
    for tag, d in res.items():
        lines.append(f"\n[{tag}] n={len(d['filas'])}  términos: {d['terminos']}")
        for arm, lab in (("M", "M (única)        "), ("esp", "T-especialistas  "), ("prot", "T-protocolo      ")):
            s, conf = summarize(d, arm)
            lines.append(f"  {lab}: {s}")
            lines.append("      falsos: " + ", ".join(f"{a}->{b} {c}" for (a, b), c in conf))
    text = "\n".join(lines)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    raw = OUT / "filas.json"
    if not args.report_only:
        with Pool(args.workers) as pool:
            res = dict(pool.imap_unordered(run_level, list(LEVELS)))
        raw.write_text(json.dumps(res, ensure_ascii=False))
    report(json.loads(raw.read_text()))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
