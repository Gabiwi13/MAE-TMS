"""
Experimento 15: árbitro por contenido y abstención por margen sobre el ruteo
maduro. Diseño en propuesta_exp15_arbitro_margen.md.

Una corrida guarda, por consulta, el vector agregado del directorio y el
score de contenido de los ocho agentes; las políticas (argmax, árbitro,
margen, ambas, contenido solo) se evalúan sobre esos datos en el reporte.

Uso:
  python run_experiment15_arbiter.py --seeds-texto 42-51 --seeds-imagen 42-46
  python run_experiment15_arbiter.py --report-only
"""
import argparse
import contextlib
import io
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from stage6_interaction import (CLASSES, AGENT_LIST, TME, route_transactive,  # noqa: E402
                                get_nlp, load_all_vectors)
from stage7_bidirectional import (recognize_gated_right, XI_VISUAL,  # noqa: E402
                                  latent_energy_threshold, latent_has_energy)
from run_experiment11_monolithic import (load_bank, split_bank, load_ood, load_cache,  # noqa: E402
                                         form_text_directories, N_TEXT_TRAIN_PER_CLASS,
                                         parse_seeds, _ci, _fmt)
import run_experiment13_augmentation as e13  # noqa: E402

OUT_DIR = Path(os.environ.get("EXP15_OUT", ROOT / "results" / "experimento15"))
RAW_DIR = OUT_DIR / "raw"
K = len(AGENT_LIST)
DELTA = 0.2
DELTAS = [round(x, 2) for x in np.arange(0, 0.55, 0.05)]
TOP = 3
OOD_FILE = ROOT / "results" / "experimento11" / "consultas_fuera_dominio.txt"


def content_scores_text(agents, cues):
    return [max(agents[c].recognize_gated(v_q) for _, v_q in cues) for c in CLASSES]


def content_scores_image(agents, z_q):
    return [recognize_gated_right(agents[c], z_q) for c in CLASSES]


def route_row(agents, entry, cues, modality):
    with contextlib.redirect_stdout(io.StringIO()):
        d, total, consulted, hops = route_transactive(entry, agents, cues, modality=modality,
                                                       xi=XI_VISUAL if modality == "image" else 0)
    return d, [float(x) for x in total], len(consulted), hops


# ---------- texto ----------

def run_text(seed):
    out = RAW_DIR / f"texto_s{seed}.json"
    if out.exists():
        return
    t0 = time.time()
    agents = load_cache(200)["specialists"]
    nlp = get_nlp()
    vectors = load_all_vectors(nlp)
    train, held = split_bank(load_bank(nlp, vectors), N_TEXT_TRAIN_PER_CLASS)
    ood_q = [l.strip() for l in OOD_FILE.read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.startswith("#")]
    ood = load_ood(nlp, vectors, ood_q)
    rng = np.random.RandomState(seed)
    tme = TME()
    # Directorios de texto vacíos por semilla: form_text_directories acumula.
    from associative_memory import DirectoryMemory
    from stage6_interaction import N as N_LAB, M_LABEL
    for c in CLASSES:
        agents[c].mem_dir = DirectoryMemory(N_LAB, M_LABEL, K)
    meta = {"semilla": seed, "formacion": form_text_directories(agents, tme, train, rng)}
    rows = []
    for idx, it in enumerate(held):
        entry_rng = np.random.RandomState(seed * 1000 + len(train) + idx)
        entry = AGENT_LIST[int(entry_rng.randint(K))]
        d, total, n_cons, hops = route_row(agents, entry, [v for _, v in it["cues"]], "text")
        rows.append({"banco": "reservado", "query": it["query"], "truth": it["tidx"],
                     "entrada": entry, "directorio": total, "contenido": content_scores_text(agents, it["cues"]),
                     "argmax": d, "consultados": n_cons, "saltos": hops})
    for k, it in enumerate(ood):
        if not it["cues"]:
            continue
        entry_rng = np.random.RandomState(seed * 1000 + 900 + k)
        entry = AGENT_LIST[int(entry_rng.randint(K))]
        d, total, n_cons, hops = route_row(agents, entry, [v for _, v in it["cues"]], "text")
        rows.append({"banco": "ood", "query": it["query"], "truth": None, "entrada": entry,
                     "directorio": total, "contenido": content_scores_text(agents, it["cues"]),
                     "argmax": d, "consultados": n_cons, "saltos": hops})
    meta["segundos"] = round(time.time() - t0, 1)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"meta": meta, "filas": rows}, ensure_ascii=False))
    print(f"  texto s{seed}: {len(rows)} filas ({meta['segundos']}s)", flush=True)


# ---------- imagen ----------

def run_image(seed, vd, ctx):
    out = RAW_DIR / f"imagen_Vd{vd}_s{seed}.json"
    if out.exists():
        return
    t0 = time.time()
    agents, train_q, test_q, tau = ctx
    meta = {"semilla": seed, "Vd": vd, "formacion": e13.form_directories(agents, train_q, vd, seed)}
    rows = []
    for path, z_q, z, ci in test_q:
        if not latent_has_energy(z, tau):
            rows.append({"banco": "test", "imagen": path, "truth": ci, "sin_energia": True})
            continue
        entry = CLASSES[(ci + 1) % K]
        d, total, n_cons, hops = route_row(agents, entry, z_q, "image")
        cont = content_scores_image(agents, z_q)
        resp = {c: e13.hetero_recognizes(agents[c], z_q) for c in CLASSES if cont[CLASSES.index(c)] > 0}
        rows.append({"banco": "test", "imagen": path, "truth": ci, "sin_energia": False, "entrada": entry,
                     "directorio": total, "contenido": cont, "responde": resp,
                     "argmax": d, "consultados": n_cons, "saltos": hops})
    meta["segundos"] = round(time.time() - t0, 1)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"meta": meta, "filas": rows}, ensure_ascii=False))
    print(f"  imagen Vd{vd} s{seed}: {len(rows)} filas ({meta['segundos']}s)", flush=True)


def image_context():
    import pickle
    with open(e13.CACHE_DIR / "Vc4_N200.pkl", "rb") as f:
        agents = pickle.load(f)["specialists"]
    train_q, test_q, _, _ = e13.load_latents()
    test = json.loads((e13.OUT_DIR / "latentes_test.json").read_text())
    test_full = [(p, z_q, np.asarray(test[p], dtype=np.float32), ci) for p, z_q, ci in test_q]
    return agents, train_q, test_full, latent_energy_threshold()


# ---------- políticas ----------

def decide(row, policy, delta=DELTA):
    """Devuelve el índice del destino o -1 (rechazo / abstención)."""
    if row.get("sin_energia"):
        return -1
    total = np.array(row["directorio"])
    cont = np.array(row["contenido"])
    d = row["argmax"]
    if policy == "contenido":
        return int(np.argmax(cont)) if cont.max() > 0 else -1
    if d < 0:
        return -1
    if policy == "argmax":
        return d
    if policy in ("margen", "ambas"):
        order = np.argsort(-total)
        s1, s2 = total[order[0]], (total[order[1]] if total[order[1]] > 0 else 0.0)
        if s1 <= 0 or (s1 - s2) / s1 < delta:
            return -1
        if policy == "margen":
            return d
    # árbitro (o ambas tras el margen)
    cands = [int(i) for i in np.argsort(-total)[:TOP] if total[i] > 0]
    best = max(cands, key=lambda i: cont[i])
    return best if cont[best] > 0 else -1


POLICIES = ("argmax", "arbitro", "margen", "ambas", "contenido")


def evaluate(rows, policy, delta=DELTA):
    """Tasas sobre todas las filas del banco."""
    n = len(rows)
    ok = err = rej = e2e = 0
    for r in rows:
        dest = decide(r, policy, delta)
        if dest < 0:
            rej += 1
        elif r["truth"] is None:
            err += 1            # fuera de dominio aceptada
        elif dest == r["truth"]:
            ok += 1
            if r.get("responde", {}).get(CLASSES[dest], False):
                e2e += 1
        else:
            err += 1
    return {"ok": ok / n, "error": err / n, "rechazo": rej / n, "e2e": e2e / n, "n": n}


def transitions(rows, policy):
    """Qué le pasa a cada decisión del argmax con la política."""
    t = {"acierto->acierto": 0, "acierto->error": 0, "acierto->rechazo": 0,
         "error->acierto": 0, "error->error": 0, "error->rechazo": 0, "rechazo->rechazo": 0,
         "rechazo->acierto": 0, "rechazo->error": 0}
    def lab(dest, truth):
        return "rechazo" if dest < 0 else ("acierto" if dest == truth else "error")
    for r in rows:
        if r["truth"] is None or r.get("sin_energia"):
            continue
        a, b = lab(decide(r, "argmax"), r["truth"]), lab(decide(r, policy), r["truth"])
        t[f"{a}->{b}"] += 1
    return t


def aggregate():
    summary = {"texto": {}, "imagen": {}, "curva": {}, "transiciones": {}, "casos": {}}
    # texto
    raws = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(RAW_DIR.glob("texto_s*.json"))]
    if raws:
        for banco in ("reservado", "ood"):
            for pol in POLICIES:
                per = [evaluate([r for r in raw["filas"] if r["banco"] == banco], pol) for raw in raws]
                summary["texto"][f"{banco}|{pol}"] = {k: _ci([p[k] for p in per]) for k in ("ok", "error", "rechazo")}
            for pol in ("arbitro", "ambas", "contenido"):
                tr = [transitions([r for r in raw["filas"] if r["banco"] == banco], pol) for raw in raws]
                summary["transiciones"][f"texto|{banco}|{pol}"] = {k: float(np.mean([t[k] for t in tr])) for k in tr[0]}
        for pol in ("margen", "ambas"):
            summary["curva"][f"texto|{pol}"] = [
                {"delta": dl, **{k: float(np.mean([evaluate([r for r in raw["filas"] if r["banco"] == "reservado"], pol, dl)[k]
                                                   for raw in raws])) for k in ("ok", "error", "rechazo")}}
                for dl in DELTAS]
        summary["curva"]["texto"] = summary["curva"]["texto|margen"]
        # pistas compartidas: consultas cuyo argmax falla en alguna semilla
        summary["texto"]["semillas"] = len(raws)
    # imagen
    for vd in (1, 16):
        raws = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(RAW_DIR.glob(f"imagen_Vd{vd}_s*.json"))]
        if not raws:
            continue
        for pol in POLICIES:
            per = [evaluate(raw["filas"], pol) for raw in raws]
            summary["imagen"][f"Vd{vd}|{pol}"] = {k: _ci([p[k] for p in per]) for k in ("ok", "error", "rechazo", "e2e")}
        for pol in ("arbitro", "ambas", "contenido"):
            tr = [transitions(raw["filas"], pol) for raw in raws]
            summary["transiciones"][f"imagen|Vd{vd}|{pol}"] = {k: float(np.mean([t[k] for t in tr])) for k in tr[0]}
        summary["curva"][f"imagen_Vd{vd}"] = [
            {"delta": dl, **{k: float(np.mean([evaluate(raw["filas"], "ambas", dl)[k] for raw in raws]))
                             for k in ("ok", "error", "rechazo")}} for dl in DELTAS]
        # el caso horse7-000-000
        for raw in raws:
            for r in raw["filas"]:
                if r.get("imagen", "").endswith("horse7-000-000.png") and not r.get("sin_energia"):
                    key = f"horse7|Vd{vd}|s{raw['meta']['semilla']}"
                    summary["casos"][key] = {
                        "argmax": CLASSES[r["argmax"]] if r["argmax"] >= 0 else None,
                        "directorio": {CLASSES[i]: round(v, 4) for i, v in enumerate(r["directorio"]) if v > 0},
                        "contenido": {CLASSES[i]: round(v, 2) for i, v in enumerate(r["contenido"]) if v > 0},
                        "arbitro": (CLASSES[decide(r, "arbitro")] if decide(r, "arbitro") >= 0 else None),
                        "ambas": (CLASSES[decide(r, "ambas")] if decide(r, "ambas") >= 0 else None)}
        summary["imagen"][f"Vd{vd}|semillas"] = len(raws)
    (OUT_DIR / "resumen.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    return summary


def write_report(summary):
    L = ["# Experimento 15 — árbitro por contenido y abstención por margen", "",
         f"Políticas sobre la misma salida de `route_transactive`: argmax (oficial); árbitro (entre los {TOP} mejores "
         "del directorio decide el contenido); margen (abstención si (s1 − s2)/s1 < δ, δ = "
         f"{DELTA} pre-registrado); ambas; contenido (los ocho por contenido, diagnóstico). Intervalos: bootstrap "
         "del 95 % sobre semillas. Diseño en `propuesta_exp15_arbitro_margen.md`.", ""]
    if summary["texto"]:
        L += [f"## Texto (N = 200, {summary['texto']['semillas']} semillas)", "",
              "171 reservadas: acierto / error / rechazo (% de las consultas). Fuera de dominio (40): aceptadas.", "",
              "| política | acierto | error | rechazo | OOD aceptadas |", "|---|---|---|---|---|"]
        for pol in POLICIES:
            r = summary["texto"][f"reservado|{pol}"]; o = summary["texto"][f"ood|{pol}"]
            L.append(f"| {pol} | {_fmt(r['ok'])} | {_fmt(r['error'])} | {_fmt(r['rechazo'])} | {_fmt(o['error'])} |")
        L += ["", "Transiciones respecto del argmax (media de consultas por semilla, reservadas):", "",
              "| política | acierto→error | acierto→rechazo | error→acierto | error→rechazo | rechazo→acierto |",
              "|---|---|---|---|---|---|"]
        for pol in ("arbitro", "ambas", "contenido"):
            t = summary["transiciones"][f"texto|reservado|{pol}"]
            L.append(f"| {pol} | {t['acierto->error']:.1f} | {t['acierto->rechazo']:.1f} | {t['error->acierto']:.1f} | "
                     f"{t['error->rechazo']:.1f} | {t['rechazo->acierto']:.1f} |")
        L += ["", "Curva de δ (reservadas): margen solo / ambas.", "",
              "| δ | acierto | error | rechazo | acierto (ambas) | error (ambas) | rechazo (ambas) |",
              "|---|---|---|---|---|---|---|"]
        for cm, ca in zip(summary["curva"]["texto|margen"], summary["curva"]["texto|ambas"]):
            L.append(f"| {cm['delta']:.2f} | {cm['ok']*100:.1f} | {cm['error']*100:.1f} | {cm['rechazo']*100:.1f} | "
                     f"{ca['ok']*100:.1f} | {ca['error']*100:.1f} | {ca['rechazo']*100:.1f} |")
        L.append("")
    for vd in (1, 16):
        if f"Vd{vd}|argmax" not in summary["imagen"]:
            continue
        L += [f"## Imagen (Vc = 4, Vd = {vd}, {summary['imagen'][f'Vd{vd}|semillas']} semillas)", "",
              "656 de test (4 rechazadas antes por energía): acierto / error / rechazo / punta a punta.", "",
              "| política | acierto | error | rechazo | e2e |", "|---|---|---|---|---|"]
        for pol in POLICIES:
            r = summary["imagen"][f"Vd{vd}|{pol}"]
            L.append(f"| {pol} | {_fmt(r['ok'])} | {_fmt(r['error'])} | {_fmt(r['rechazo'])} | {_fmt(r['e2e'])} |")
        L += ["", "Transiciones respecto del argmax (media por semilla):", "",
              "| política | acierto→error | acierto→rechazo | error→acierto | error→rechazo | rechazo→acierto |",
              "|---|---|---|---|---|---|"]
        for pol in ("arbitro", "ambas", "contenido"):
            t = summary["transiciones"][f"imagen|Vd{vd}|{pol}"]
            L.append(f"| {pol} | {t['acierto->error']:.1f} | {t['acierto->rechazo']:.1f} | {t['error->acierto']:.1f} | "
                     f"{t['error->rechazo']:.1f} | {t['rechazo->acierto']:.1f} |")
        L.append("")
    if summary["casos"]:
        L += ["## El caso `horse7-000-000`", "", "| directorios | semilla | argmax | directorio (>0) | contenido (>0) | árbitro | ambas |",
              "|---|---|---|---|---|---|---|"]
        for key, c in summary["casos"].items():
            _, vd, s = key.split("|")
            L.append(f"| {vd} | {s} | {c['argmax']} | {c['directorio']} | {c['contenido']} | {c['arbitro']} | {c['ambas']} |")
        L.append("")
    L += ["## Archivos", "- `raw/texto_s<semilla>.json`, `raw/imagen_Vd<Vd>_s<semilla>.json`: por consulta, vector del directorio y "
          "scores de contenido de los ocho agentes", "- `resumen.json`, `fig1_curva_margen.png`"]
    (OUT_DIR / "README.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def make_figure(summary):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    keys = [k for k in ("texto", "imagen_Vd1", "imagen_Vd16") if k in summary["curva"]]
    fig, axes = plt.subplots(1, len(keys), figsize=(4.5 * len(keys), 4), squeeze=False)
    for ax, k in zip(axes[0], keys):
        c = summary["curva"][k]
        xs = [x["delta"] for x in c]
        ax.plot(xs, [x["ok"] * 100 for x in c], "o-", color="#27ae60", label="acierto")
        ax.plot(xs, [x["error"] * 100 for x in c], "o-", color="#c0392b", label="error")
        ax.plot(xs, [x["rechazo"] * 100 for x in c], "o-", color="#7f8c8d", label="rechazo")
        ax.axvline(DELTA, color="k", ls="--"); ax.set_title(k); ax.set_xlabel("δ"); ax.set_ylabel("%")
        ax.spines[["top", "right"]].set_visible(False); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(OUT_DIR / "fig1_curva_margen.png", dpi=150); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds-texto", default="42-51")
    ap.add_argument("--seeds-imagen", default="42-46")
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not args.report_only:
        print("Texto...", flush=True)
        for s in parse_seeds(args.seeds_texto):
            run_text(s)
        print("Imagen...", flush=True)
        ctx = image_context()
        for vd in (1, 16):
            for s in parse_seeds(args.seeds_imagen):
                run_image(s, vd, ctx)
    summary = aggregate()
    write_report(summary)
    make_figure(summary)
    print(f"Salidas -> {OUT_DIR}")


if __name__ == "__main__":
    main()
