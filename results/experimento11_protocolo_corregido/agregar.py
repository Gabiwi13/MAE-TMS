"""
Junta las filas M y T-oraculo de los raw oficiales de exp11 con las de
T-protocolo corregidas y reproduce las tablas del README de exp11 (viejo y
nuevo). Agrega la clase correcta sobre el total (no respuesta = fallo),
McNemar exacto pareado protocolo contra EHAM única y un diagnóstico del
arreglo (círculo por entrada y coincidencia de destinos).

Uso:  python results/experimento11_protocolo_corregido/agregar.py
"""
import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
import run_experiment11_monolithic as e11  # noqa: E402

OLD = ROOT / "results" / "experimento11" / "raw"
NEW = Path(os.environ.get("EXP11FIX_NEW", HERE / "raw"))
OUTD = Path(os.environ.get("EXP11FIX_OUT", HERE))
CUTS = (25, 50, 100, 200)
JUDGES = ("nn_ok", "centroide_ok", "clf_ok")
P = "T-protocolo"
LOAD_RUNS = e11.load_runs


def runs_from(raw_dir):
    e11.RAW_DIR = raw_dir
    return {(r["meta"]["semilla"], r["meta"]["corte"]): r for r in LOAD_RUNS()}


def merge(old, new):
    """M y T-oraculo de lo viejo, T-protocolo de lo nuevo. F se calcula por
    brazo con sus propias filas, así que se toma de cada lado."""
    out = []
    for key in sorted(old):
        if key not in new:
            continue
        o, n = old[key], new[key]
        meta = dict(o["meta"])
        for k in ("formacion_texto", "formacion_imagen", "control_igual_al_oficial"):
            if k in n["meta"]:
                meta[k] = n["meta"][k]
        meta["dependencia"] = {a: (n if a == P else o)["meta"]["dependencia"][a] for a in e11.ARMS}
        run = {"meta": meta}
        for part in ("texto", "ood", "imagen"):
            # Sin archivo _o el fuera de dominio nuevo es el de 12 consultas del trozo 0.
            fresh = [] if part == "ood" and "ood_n" not in n["meta"] else n[part]
            run[part] = ([r for r in o[part] if r["brazo"] != P]
                         + [r for r in fresh if r["brazo"] == P])
        out.append(run)
    return out


def summarize(runs, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    e11.load_runs = lambda: runs
    e11.OUT_DIR = out_dir
    s = e11.aggregate()
    e11.write_report(s)
    return s


# ---------- clase sobre el total y McNemar ----------

def correct(r, judge):
    return bool(r.get("responde")) and bool(r.get(judge))


def text_index(runs, arm):
    """(semilla, corte, consulta, sorteo) -> fila."""
    idx = {}
    for run in runs.values():
        for r in run["texto"]:
            if r["brazo"] == arm and r["banco"] == "reservado":
                idx[(r["semilla"], r["corte"], r["query"], r["rep"])] = r
    return idx


def over_total(idx, cut, judge):
    per_seed = defaultdict(list)
    for (s, c, _q, _r), row in idx.items():
        if c == cut:
            per_seed[s].append(correct(row, judge))
    return e11._ci([float(np.mean(v)) for _, v in sorted(per_seed.items())])


def binom_two_sided(k, n):
    """McNemar exacto: binomial(n, 1/2) de dos colas sobre los discordantes."""
    if n == 0:
        return 1.0
    k = min(k, n - k)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def mcnemar(idx_m, idx_p, cut, judge, seed=None):
    b = c = n = 0
    for key, rm in idx_m.items():
        if key[1] != cut or (seed is not None and key[0] != seed) or key not in idx_p:
            continue
        m_ok, p_ok = correct(rm, judge), correct(idx_p[key], judge)
        n += 1
        b += int(m_ok and not p_ok)
        c += int(p_ok and not m_ok)
    return {"pares": n, "M_si_P_no": b, "P_si_M_no": c, "p": binom_two_sided(b, b + c),
            "diferencia_P_menos_M": (c - b) / n if n else float("nan")}


def dnn_paired(idx_m, idx_p, cut, n_boot=10000):
    """d_nn de P − M por consulta: media de d_nn de cada brazo sobre sus
    respuestas (semillas × sorteos) y bootstrap remuestreando consultas que
    tienen respuesta en los dos brazos."""
    acc = defaultdict(lambda: [[], []])
    for key, rm in idx_m.items():
        if key[1] != cut or key not in idx_p:
            continue
        rp = idx_p[key]
        if rm.get("responde"):
            acc[key[2]][0].append(rm["d_nn_truth"])
        if rp.get("responde"):
            acc[key[2]][1].append(rp["d_nn_truth"])
    d = np.array([np.mean(p) - np.mean(m) for m, p in acc.values() if m and p])
    rng = np.random.RandomState(0)
    boots = d[rng.randint(0, len(d), size=(n_boot, len(d)))].mean(axis=1)
    return {"consultas": len(d), "media": float(d.mean()),
            "ic95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}


def query_bootstrap(idx_m, idx_p, cut, judge, n_boot=10000):
    """Diferencia P − M sobre el total, promediando por consulta las 10
    semillas × 3 sorteos y remuestreando consultas."""
    acc = defaultdict(lambda: [[], []])
    for key, rm in idx_m.items():
        if key[1] == cut and key in idx_p:
            acc[key[2]][0].append(correct(rm, judge))
            acc[key[2]][1].append(correct(idx_p[key], judge))
    d = np.array([np.mean(p) - np.mean(m) for m, p in acc.values()])
    rng = np.random.RandomState(0)
    boots = d[rng.randint(0, len(d), size=(n_boot, len(d)))].mean(axis=1)
    return {"consultas": len(d), "media": float(d.mean()),
            "ic95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}


# ---------- diagnóstico del arreglo ----------

def circle_by_chunk(raw_dir):
    """Por (semilla, corte): entradas cuyo círculo (consultados con 0 saltos)
    cambia entre trozos."""
    sizes = defaultdict(lambda: defaultdict(set))
    for f in raw_dir.glob("s*_N*_c*.json"):
        raw = json.loads(f.read_text(encoding="utf-8"))
        k = raw["meta"]["trozo"]
        per = defaultdict(set)
        for r in raw["texto"]:
            if r["brazo"] == P and r["rep"] == 0 and r.get("saltos") == 0:
                per[r["entrada"]].add(r["consultados"])
        for e, v in per.items():
            sizes[(raw["meta"]["semilla"], raw["meta"]["corte"])][e].add((k, tuple(sorted(v))))
    out = {}
    for key, ents in sizes.items():
        var = {e: sorted(v) for e, v in ents.items() if len({x[1] for x in v}) > 1}
        out[key] = var
    return out


def chunk_of(raw_dir):
    """(semilla, corte, consulta) -> trozo, para ubicar diferencias."""
    m = {}
    for f in raw_dir.glob("s*_N*_c*.json"):
        raw = json.loads(f.read_text(encoding="utf-8"))
        for r in raw["texto"]:
            if r["brazo"] == P and r["rep"] == 0:
                m[(r["semilla"], r["corte"], r["query"])] = raw["meta"]["trozo"]
    return m


def dest_agreement(old, new):
    rows = []
    chunks = chunk_of(OLD)
    for key in sorted(new):
        if key not in old:
            continue
        o = {(r["query"], r["rep"]): r for r in old[key]["texto"] if r["brazo"] == P}
        n = {(r["query"], r["rep"]): r for r in new[key]["texto"] if r["brazo"] == P}
        qs = [k for k in n if k[1] == 0 and k in o]
        diff = [k[0] for k in qs if o[k]["destino"] != n[k]["destino"] or o[k]["consultados"] != n[k]["consultados"]]
        oi = {(Path(r["imagen"]).name): r for r in old[key]["imagen"] if r["brazo"] == P}
        ni = {(Path(r["imagen"]).name): r for r in new[key]["imagen"] if r["brazo"] == P}
        ims = [k for k in ni if k in oi]
        oo = {r["query"]: r for r in old[key]["ood"] if r["brazo"] == P}
        no = {r["query"]: r for r in new[key]["ood"] if r["brazo"] == P}
        oqs = [k for k in no if k in oo]
        rows.append({
            "semilla": key[0], "corte": key[1],
            "texto_consultas": len(qs), "texto_destino_distinto": len(diff),
            "texto_trozos_con_diferencias": sorted({chunks.get((key[0], key[1], q)) for q in diff}),
            "imagen_n": len(ims),
            "imagen_destino_distinto": sum(oi[k]["destino"] != ni[k]["destino"] for k in ims),
            "ood_n": len(oqs),
            "ood_distinto": sum((oo[k]["acepta"], oo[k]["acepta_compuerta"], oo[k]["destino"])
                                != (no[k]["acepta"], no[k]["acepta_compuerta"], no[k]["destino"])
                                for k in oqs),
        })
    return rows


def ood_accepted(runs, arm, cut):
    """Consultas fuera de dominio aceptadas, con cuántas semillas."""
    acc = defaultdict(lambda: [0, 0, set()])
    for (s, c), run in runs.items():
        if c != cut:
            continue
        for r in run["ood"]:
            if r["brazo"] == arm:
                acc[r["query"]][0] += int(r["acepta"])
                acc[r["query"]][1] += int(r["acepta_compuerta"])
                if r["destino"]:
                    acc[r["query"]][2].add(r["destino"])
    return {q: {"acepta": a, "compuerta": g, "destinos": sorted(d)}
            for q, (a, g, d) in acc.items() if a or g}


# ---------- informe ----------

def f(ci, pct=True):
    return e11._fmt(ci, pct)


def side_by_side(s_old, s_new):
    L = ["## T-protocolo: viejo contra corregido", "",
         "Media entre semillas e IC 95 % bootstrap. «sobre respondidas» es la métrica del README de exp11; "
         "M y T-oráculo no cambian (mismas filas).", ""]
    tm = (("acepta", "acepta", True), ("responde", "responde", True), ("ruteo_ok", "ruteo ok", True),
          ("nn_ok", "clase 1-NN (sobre respondidas)", True), ("centroide_ok", "centroide", True),
          ("clf_ok", "clasificador", True), ("d_nn_truth", "d_nn", False),
          ("compat_max", "compat máx", False), ("compat_ok", "compat ok", True),
          ("niveles_vivos", "niveles vivos", False),
          ("fraccion_pista_compartida", "fracción pista compartida", True),
          ("nn_ok_pista_compartida", "clase 1-NN con pista compartida", True))
    for cut in CUTS:
        k = f"{P}|N={cut}"
        if k not in s_new["texto"]:
            continue
        L += [f"### N = {cut}", "", "| medida | viejo | corregido |", "|---|---|---|"]
        for key, name, pct in tm:
            L.append(f"| {name} | {f(s_old['texto'][k][key], pct)} | {f(s_new['texto'][k][key], pct)} |")
        L.append(f"| F | {f(s_old['dependencia'][k], False)} | {f(s_new['dependencia'][k], False)} |")
        L.append(f"| fuera de dominio, acepta | {f(s_old['ood'][k])} | {f(s_new['ood'][k])} |")
        L.append(f"| fuera de dominio, con compuerta | {f(s_old['ood_compuerta'].get(k))} | "
                 f"{f(s_new['ood_compuerta'].get(k))} |")
        fo, fn = s_old["formacion"].get(k), s_new["formacion"].get(k)
        if fo and fn:
            L.append(f"| formación: registradas / rechazadas / acierto temprano | "
                     f"{f(fo['registradas'], False)} / {f(fo['rechazadas'], False)} / {f(fo['acierto_temprano'])} | "
                     f"{f(fn['registradas'], False)} / {f(fn['rechazadas'], False)} / {f(fn['acierto_temprano'])} |")
        io_, in_ = s_old["imagen"].get(k), s_new["imagen"].get(k)
        if io_ and in_:
            for key, name in (("acepta", "imagen: acepta"), ("responde", "imagen: responde"),
                              ("hit", "imagen: hit laxo"), ("hit_exclusivo", "imagen: hit estricto"),
                              ("dominio_ok", "imagen: dominio ok"), ("otro_dominio", "imagen: otro dominio"),
                              ("ruteo_ok", "imagen: ruteo ok")):
                L.append(f"| {name} | {f(io_[key])} | {f(in_[key])} |")
        L.append("")
    return L


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    old = runs_from(OLD)
    new = runs_from(NEW)
    # Completo: el raw nuevo trae todas las consultas reservadas de ese
    # (semilla, corte). Las tablas solo usan pares completos; lo viejo se
    # resume también sobre esos mismos pares para comparar igual con igual.
    n_q = lambda run: len({r["query"] for r in run["texto"] if r["brazo"] == P})
    complete = sorted(k for k in new if k in old and n_q(new[k]) == n_q(old[k]))
    merged = merge(old, {k: new[k] for k in complete})
    print(f"(semilla, corte) completos en el raw nuevo: {len(complete)} de {len(old)}; "
          f"parciales: {sorted(set(new) - set(complete))}")

    summarize(list(old.values()), OUTD / "tablas_viejas")
    s_old = summarize([old[k] for k in complete], OUTD / "tablas_viejas_mismos_pares")
    s_new = summarize(merged, OUTD / "tablas_nuevas")

    # Estadística pareada: solo las (semilla, consulta, sorteo) que tiene lo nuevo.
    idx_n = text_index(new, P)
    keep = lambda ix: {k: v for k, v in ix.items() if k in idx_n}
    idx_m = keep(text_index(old, "M"))
    idx_o = keep(text_index(old, P))
    idx_or = keep(text_index(old, "T-oraculo"))
    stats = {"sobre_total": {}, "mcnemar": {}, "mcnemar_por_semilla": {}, "bootstrap_consulta": {},
             "d_nn": {}}
    for cut in CUTS:
        if not any(k[1] == cut for k in idx_n):
            continue
        stats["d_nn"][f"N={cut}"] = {
            "viejo": dnn_paired(idx_m, idx_o, cut), "corregido": dnn_paired(idx_m, idx_n, cut),
            "oraculo": dnn_paired(idx_m, idx_or, cut)}
        for judge in JUDGES:
            key = f"N={cut}|{judge}"
            stats["sobre_total"][key] = {
                "M": over_total(idx_m, cut, judge),
                "T-oraculo": over_total(idx_or, cut, judge),
                "P_viejo": over_total(idx_o, cut, judge),
                "P_corregido": over_total(idx_n, cut, judge)}
            stats["mcnemar"][key] = {"viejo": mcnemar(idx_m, idx_o, cut, judge),
                                     "corregido": mcnemar(idx_m, idx_n, cut, judge)}
            stats["bootstrap_consulta"][key] = {"viejo": query_bootstrap(idx_m, idx_o, cut, judge),
                                                "corregido": query_bootstrap(idx_m, idx_n, cut, judge)}
            seeds = sorted({k[0] for k in idx_n if k[1] == cut})
            stats["mcnemar_por_semilla"][key] = {
                lado: [dict(mcnemar(idx_m, ix, cut, judge, seed=s), semilla=s) for s in seeds]
                for lado, ix in (("viejo", idx_o), ("corregido", idx_n))}

    circ_old, circ_new = circle_by_chunk(OLD), circle_by_chunk(NEW)
    agree = dest_agreement(old, new)
    # Fuera de dominio: solo los pares con archivo _o nuevo (40 consultas), igual en los dos lados.
    with_o = {k for k in new if "ood_n" in new[k]["meta"] and k in old}
    sub = lambda runs: {k: runs[k] for k in with_o}
    ood_lists = {f"N={c}": {"M": ood_accepted(sub(old), "M", c),
                            "T-oraculo": ood_accepted(sub(old), "T-oraculo", c),
                            "P_viejo": ood_accepted(sub(old), P, c), "P_corregido": ood_accepted(sub(new), P, c)}
                 for c in CUTS if any(k[1] == c for k in with_o)}
    tiempos = defaultdict(list)
    for fpath in NEW.glob("s*_N*_*.json"):
        raw = json.loads(fpath.read_text(encoding="utf-8"))
        kind = fpath.stem.split("_")[2][0]
        tiempos[f"{kind}|N={raw['meta']['corte']}"].append(raw["meta"]["segundos"])

    out = {"pares": len(complete), "estadistica": stats,
           "circulo_variable_viejo": {f"s{k[0]}_N{k[1]}": v for k, v in circ_old.items() if v},
           "circulo_variable_nuevo": {f"s{k[0]}_N{k[1]}": v for k, v in circ_new.items() if v},
           "coincidencia_destinos": agree, "fuera_de_dominio_aceptadas": ood_lists,
           "segundos_por_trabajo": {k: {"n": len(v), "media": float(np.mean(v)), "suma_h": sum(v) / 3600}
                                    for k, v in sorted(tiempos.items())}}
    (OUTD / "comparacion.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False, default=list), encoding="utf-8")

    L = ["# exp11, T-protocolo corregido: comparación", "",
         f"Pares (semilla, corte) completos en el raw nuevo: {len(complete)} de {len(old)} "
         f"({', '.join(f's{s} N={c}' for s, c in complete)}). Las tablas lado a lado usan solo esos pares; "
         "la estadística pareada usa todas las (semilla, consulta, sorteo) con raw nuevo. "
         "Tablas con los tres brazos: `tablas_viejas/README.md` (todo lo oficial; debe coincidir con el "
         "README de exp11), `tablas_viejas_mismos_pares/README.md` y `tablas_nuevas/README.md`.", ""]
    L += side_by_side(s_old, s_new)
    L += ["## Clase correcta sobre el total (no respuesta = fallo)", "",
          "Consultas reservadas × 3 sorteos por semilla (las mismas en todos los brazos); media entre semillas e IC 95 % bootstrap.", "",
          "| N | juez | M | T-oráculo | P viejo | P corregido |", "|---|---|---|---|---|---|"]
    for key, v in stats["sobre_total"].items():
        cut, judge = key.split("|")
        L.append(f"| {cut[2:]} | {judge} | {f(v['M'])} | {f(v['T-oraculo'])} | {f(v['P_viejo'])} | "
                 f"{f(v['P_corregido'])} |")
    L += ["", "## McNemar exacto, T-protocolo contra M (clase correcta sobre el total)", "",
          "Pares (semilla, consulta, sorteo). b: M acierta y P no; c: P acierta y M no. Los sorteos de una "
          "misma consulta no son independientes, así que este p es optimista; el bootstrap por consulta "
          "(cada consulta con la media de sus pares entre semillas y sorteos) es la prueba conservadora.", "",
          "| N | juez | lado | pares | b | c | P − M | p | bootstrap por consulta | semillas con p < 0.05 (P arriba / M arriba) |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for key, v in stats["mcnemar"].items():
        cut, judge = key.split("|")
        for lado in ("viejo", "corregido"):
            m = v[lado]
            bq = stats["bootstrap_consulta"][key][lado]
            ps = stats["mcnemar_por_semilla"][key][lado]
            up = sum(x["p"] < 0.05 and x["P_si_M_no"] > x["M_si_P_no"] for x in ps)
            down = sum(x["p"] < 0.05 and x["M_si_P_no"] > x["P_si_M_no"] for x in ps)
            L.append(f"| {cut[2:]} | {judge} | {lado} | {m['pares']} | {m['M_si_P_no']} | {m['P_si_M_no']} | "
                     f"{m['diferencia_P_menos_M']*100:+.2f} | {m['p']:.3g} | "
                     f"{bq['media']*100:+.2f} [{bq['ic95'][0]*100:+.2f}, {bq['ic95'][1]*100:+.2f}] | "
                     f"{up} / {down} de {len(ps)} |")
    L += ["", "## d_nn contra la EHAM única, pareado por consulta", "",
          "Por consulta: media de d_nn de cada brazo sobre sus respuestas (semillas × sorteos); diferencia "
          "brazo − M y bootstrap remuestreando consultas. Negativo: el brazo recuerda más cerca de una "
          "instancia real de la clase.", "",
          "| N | brazo | consultas | brazo − M [IC 95 %] |", "|---|---|---|---|"]
    for cut, v in stats["d_nn"].items():
        for lado, lab in (("viejo", "P viejo"), ("corregido", "P corregido"), ("oraculo", "T-oráculo")):
            x = v[lado]
            L.append(f"| {cut[2:]} | {lab} | {x['consultas']} | {x['media']:+.2f} "
                     f"[{x['ic95'][0]:+.2f}, {x['ic95'][1]:+.2f}] |")
    L += ["", "## Diagnóstico del arreglo", "",
          f"- Entradas con círculo variable entre trozos (consultas resueltas sin saltos): viejo en "
          f"{sum(1 for v in circ_old.values() if v)} de {len(circ_old)} pares (semilla, corte); corregido en "
          f"{sum(1 for v in circ_new.values() if v)} de {len(circ_new)}.", "",
          "Coincidencia del ruteo viejo con el corregido (texto: destino y tamaño del círculo, sorteo 0; "
          "imagen: destino; fuera de dominio: acepta, compuerta y destino):", "",
          "| semilla | corte | texto distintas / consultas | trozos con diferencias | imagen distintas / n | fuera de dominio distintas / n |",
          "|---|---|---|---|---|---|"]
    for a in agree:
        L.append(f"| {a['semilla']} | {a['corte']} | {a['texto_destino_distinto']} / {a['texto_consultas']} | "
                 f"{a['texto_trozos_con_diferencias']} | {a['imagen_destino_distinto']} / {a['imagen_n']} | "
                 f"{a['ood_distinto']} / {a['ood_n']} |")
    L += ["", "## Fuera de dominio aceptadas por T-protocolo (semillas que aceptan / con compuerta)", ""]
    for cut, d in ood_lists.items():
        L.append(f"- {cut}: viejo " + "; ".join(f"«{q}» {x['acepta']}/{x['compuerta']} → {x['destinos']}"
                                                for q, x in d["P_viejo"].items())
                 + " · corregido " + "; ".join(f"«{q}» {x['acepta']}/{x['compuerta']} → {x['destinos']}"
                                               for q, x in d["P_corregido"].items()))
    L += ["", "## Tiempo por trabajo (corrida corregida)", "",
          "| tipo y corte | trabajos | media (s) | suma (h) |", "|---|---|---|---|"]
    for k, v in out["segundos_por_trabajo"].items():
        L.append(f"| {k} | {v['n']} | {v['media']:.0f} | {v['suma_h']:.2f} |")
    (OUTD / "comparacion.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
