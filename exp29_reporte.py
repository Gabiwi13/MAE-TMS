"""Informe del experimento 29: predicciones P1-P9 y criterio de la propuesta, a partir de filas_s*.json."""
import json
from pathlib import Path

import numpy as np

CLASSES = ("correcto", "omision", "superordinado", "semantico", "entre_dominios")
MODELS = ("mae", "mae_proy", "pdp", "minerva", "vecino")
# Rogers 2004, Figura 6 (lectura calibrada, ±0.005).
PATIENTS = {
    "Q1": {"correcto": .796, "omision": .104, "semantico": .089, "superordinado": .010, "entre_dominios": .001},
    "Q2": {"correcto": .381, "omision": .312, "semantico": .241, "superordinado": .063, "entre_dominios": .005},
    "Q3": {"correcto": .129, "omision": .560, "semantico": .170, "superordinado": .141, "entre_dominios": .002},
    "Q4": {"correcto": .045, "omision": .822, "semantico": .070, "superordinado": .059, "entre_dominios": .006},
}


def load(out):
    metas, rows = {}, []
    for f in sorted(out.glob("filas_s*.json")):
        z = json.loads(f.read_text())
        for m in z["metas"]:
            metas[m["semilla"]] = m
        rows += z["filas"]
    return metas, rows


def classify(items, i, name):
    from run_experiment29_demencia_semantica import NAMES, SPECIFIC, GENERAL, SUPER, LIVING, CATS
    if name is None:
        return "omision"
    it = items[i]
    if name == it["name"]:
        return "correcto"
    word = NAMES[name]
    if word in SUPER[it["cat"]]:
        return "superordinado"
    owner = next(c for c in CATS if word in SPECIFIC[c] or GENERAL.get(c) == word)
    return "semantico" if (owner in LIVING) == (it["cat"] in LIVING) else "entre_dominios"


def tabulate(metas, rows):
    """Por modelo y d: proporciones, exactitud por frecuencia, tipicidad y frecuencia de los errores, dibujo."""
    levels = sorted({r["d"] for r in rows})
    res = {m: {} for m in MODELS}
    seeds = sorted(metas)
    for m in MODELS:
        for d in levels:
            res[m][d] = {"cls": {c: 0 for c in CLASSES}, "n": 0, "acc_f": {4: [0, 0], 1: [0, 0]},
                         "typ_diff": [], "resp_high": [], "typ_up": [], "intruso_frecuente": 0,
                         "por_semilla": {s: {c: 0 for c in CLASSES} | {"n": 0} for s in seeds},
                         "dib": {}}
    for r in rows:
        items = metas[r["semilla"]]["items"]
        i, d = r["item"], r["d"]
        it = items[i]
        owner = {it2["name"]: k for k, it2 in enumerate(items) if it2["specific"]}
        same_cat = [k for k, it2 in enumerate(items) if it2["cat"] == it["cat"] and it2["specific"] and k != i]
        most_typ = max(same_cat, key=lambda k: items[k]["typ"]) if same_cat else None
        for m in MODELS:
            e = res[m][d]
            for name in r["resp"][m]:
                c = classify(items, i, name)
                e["cls"][c] += 1; e["n"] += 1
                ps = e["por_semilla"][r["semilla"]]; ps[c] += 1; ps["n"] += 1
                e["acc_f"][it["freq"]][0] += c == "correcto"; e["acc_f"][it["freq"]][1] += 1
                if c in ("semantico", "entre_dominios") and name in owner:
                    j = owner[name]
                    e["typ_diff"].append(items[j]["typ"] - it["typ"])
                    e["typ_up"].append(items[j]["typ"] > it["typ"])
                    e["resp_high"].append(items[j]["freq"] > 1)
                if name is not None and name in owner and owner[name] != i and items[owner[name]]["cat"] == it["cat"] \
                        and (items[owner[name]]["freq"] > 1 or owner[name] == most_typ):
                    e["intruso_frecuente"] += 1
        for m, st in r["dibujo"].items():
            dib = res[m][d]["dib"]
            for k, (a, b) in st.items():
                x = dib.setdefault(k, [0, 0]); x[0] += a; x[1] += b
    return levels, res


def prop(e, c):
    return e["cls"][c] / e["n"] if e["n"] else float("nan")


def at_accuracy(levels, res_m, target):
    """Interpola cada proporción en el primer cruce de la exactitud con `target`."""
    acc = [prop(res_m[d], "correcto") for d in levels]
    for k in range(len(levels) - 1):
        a0, a1 = acc[k], acc[k + 1]
        if (a0 - target) * (a1 - target) <= 0 and a0 != a1:
            t = (a0 - target) / (a0 - a1)
            return {c: (1 - t) * prop(res_m[levels[k]], c) + t * prop(res_m[levels[k + 1]], c) for c in CLASSES} | \
                   {"d": (1 - t) * levels[k] + t * levels[k + 1], "k": k, "t": t}
    return None


def slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(y)
    return float(np.polyfit(x[ok], y[ok], 1)[0]) if ok.sum() >= 3 else float("nan")


def evaluate(levels, res, metas):
    seeds = sorted(metas)
    ev = {}
    for m in MODELS:
        R = res[m]
        e = {}
        acc0 = prop(R[0.0], "correcto")
        e["exactitud_sin_daño"] = acc0
        omis = [prop(R[d], "omision") for d in levels]
        e["P1_pendientes_por_semilla"] = [slope(levels, [R[d]["por_semilla"][s]["omision"] / max(R[d]["por_semilla"][s]["n"], 1)
                                                          for d in levels]) for s in seeds]
        e["P1"] = all(v > 0 for v in e["P1_pendientes_por_semilla"])
        q4 = at_accuracy(levels, R, PATIENTS["Q4"]["correcto"])
        e["P2"] = bool(q4 and q4["superordinado"] < q4["omision"])
        sem = [prop(R[d], "semantico") for d in levels]
        k = int(np.nanargmax(sem))
        e["semantico_max"] = (levels[k], sem[k], sem[0], sem[-1])
        e["P3"] = 0 < k < len(levels) - 1 and sem[k] >= max(sem[0], sem[-1]) + 0.01
        cross = [prop(R[d], "entre_dominios") for d in levels]
        e["entre_dominios_max"] = float(np.nanmax(cross))
        e["P4"] = e["entre_dominios_max"] < 0.05
        td = [(d, np.mean(R[d]["typ_diff"]), len(R[d]["typ_diff"])) for d in levels if len(R[d]["typ_diff"]) >= 20]
        e["tipicidad_errores"] = td
        alltd = [x for d in levels for x in R[d]["typ_diff"]]
        e["P5_media"] = float(np.mean(alltd)) if alltd else float("nan")
        e["P5_pendiente"] = slope([t[0] for t in td], [t[1] for t in td]) if len(td) >= 3 else float("nan")
        e["P5"] = bool(alltd) and e["P5_media"] > 0 and e["P5_pendiente"] > 0
        fe = []
        for d in levels:
            hi, lo = R[d]["acc_f"][4], R[d]["acc_f"][1]
            a = prop(R[d], "correcto")
            if 0.05 <= a <= 0.95 and hi[1] and lo[1]:
                fe.append((d, hi[0] / hi[1] - lo[0] / lo[1]))
        e["efecto_frecuencia"] = fe
        e["P6_media"] = float(np.mean([x for _, x in fe])) if fe else float("nan")
        e["P6_pendiente"] = slope([x for x, _ in fe], [y for _, y in fe]) if len(fe) >= 3 else float("nan")
        rh = [x for d in levels for x in R[d]["resp_high"]]
        e["P6_intrusos_frecuentes"] = float(np.mean(rh)) if rh else float("nan")
        e["P6"] = bool(fe) and e["P6_media"] > 0 and e["P6_pendiente"] > 0 and (e["P6_intrusos_frecuentes"] > 0.5)
        dib = {d: R[d]["dib"] for d in levels if R[d]["dib"]}
        rate = lambda d, key: (dib[d][key][0] / dib[d][key][1]
                               if d in dib and dib[d].get(key) and dib[d][key][1] else float("nan"))
        dmg = [d for d in levels if d > 0]
        om_dist = np.nanmean([rate(d, "omis_distintivo") for d in dmg])
        om_shared = np.nanmean([np.nanmean([rate(d, "omis_dominio"), rate(d, "omis_categoria")]) for d in dmg])
        intr_dom = [rate(d, "intr_dominio") for d in levels]
        e["dibujo"] = {"omis_distintivo": float(om_dist), "omis_compartido": float(om_shared),
                       "intr_dominio_pendiente": slope(levels, intr_dom),
                       "intr_dominio": [(d, rate(d, "intr_dominio")) for d in levels]}
        e["P7"] = om_dist > om_shared and e["dibujo"]["intr_dominio_pendiente"] > 0
        n_all = [R[d]["n"] for d in levels]
        tf = [R[d]["intruso_frecuente"] / n for d, n in zip(levels, n_all)]
        e["P8_serie"] = list(zip(levels, tf))
        e["P8_pendiente"] = slope(levels, tf)
        e["P8"] = e["P8_pendiente"] > 0
        cuart = {}
        for q, p in PATIENTS.items():
            x = at_accuracy(levels, R, p["correcto"])
            if x is None:
                cuart[q] = None
                continue
            ok = all(abs(x[c] - p[c]) <= 0.10 for c in ("omision", "superordinado", "semantico"))
            cuart[q] = {c: x[c] for c in CLASSES} | {"d": x["d"], "dentro": ok}
        e["cuartiles"] = cuart
        e["cuartiles_dentro"] = sum(1 for v in cuart.values() if v and v["dentro"])
        fe_q = []
        for q, p in PATIENTS.items():
            x = at_accuracy(levels, R, p["correcto"])
            if x is None:
                continue
            d0, d1 = levels[x["k"]], levels[x["k"] + 1]
            f = lambda d: (R[d]["acc_f"][4][0] / max(R[d]["acc_f"][4][1], 1)) - (R[d]["acc_f"][1][0] / max(R[d]["acc_f"][1][1], 1))
            fe_q.append((1 - x["t"]) * f(d0) + x["t"] * f(d1))
        e["efecto_frecuencia_en_cuartiles"] = float(np.mean(fe_q)) if fe_q else float("nan")
        ev[m] = e
    return ev


def report(out):
    out = Path(out)
    metas, rows = load(out)
    metas = {int(k): v for k, v in metas.items()}
    levels, res = tabulate(metas, rows)
    ev = evaluate(levels, res, metas)
    L = [f"Exp29: demencia semántica como pérdida de conteos. Semillas {sorted(metas)}; niveles {levels}.",
         "PDP épocas por semilla: " + ", ".join(str(metas[s]["pdp_epocas"]) for s in sorted(metas))]
    for m in MODELS:
        e = ev[m]
        L.append(f"\n[{m}] exactitud sin daño {100 * e['exactitud_sin_daño']:.1f} %")
        L.append("  d      " + "  ".join(f"{c[:5]:>6}" for c in CLASSES) + "   n")
        for d in levels:
            L.append(f"  {d:<5}  " + "  ".join(f"{100 * prop(res[m][d], c):6.1f}" for c in CLASSES) + f"   {res[m][d]['n']}")
        L.append("  a la exactitud de cada cuartil de pacientes (modelo / paciente):")
        for q, v in e["cuartiles"].items():
            if v is None:
                L.append(f"    {q}: el modelo no cruza esa exactitud")
            else:
                L.append(f"    {q} (d ≈ {v['d']:.3f}): " + ", ".join(
                    f"{c} {100 * v[c]:.1f}/{100 * PATIENTS[q][c]:.1f}" for c in CLASSES) + f" · dentro ±10: {v['dentro']}")
        L.append(f"  P1 omisiones crecientes en cada semilla: {e['P1']} (pendientes {np.round(e['P1_pendientes_por_semilla'], 2).tolist()})")
        L.append(f"  P2 superordinado < omisión en Q4: {e['P2']}")
        dk, sk, s0, s9 = e["semantico_max"]
        L.append(f"  P3 U invertida en semánticos: {e['P3']} (máximo {100 * sk:.1f} % en d = {dk}; extremos {100 * s0:.1f} y {100 * s9:.1f})")
        L.append(f"  P4 entre dominios < 5 %: {e['P4']} (máximo {100 * e['entre_dominios_max']:.1f} %)")
        L.append(f"  P5 errores más típicos que el blanco y creciente: {e['P5']} (media {e['P5_media']:+.3f}, pendiente {e['P5_pendiente']:+.3f}; "
                 f"niveles con >= 20 errores: {len(e['tipicidad_errores'])})")
        L.append(f"  P6 frecuencia: {e['P6']} (alta − baja media {100 * e['P6_media']:+.1f} pts, pendiente {e['P6_pendiente']:+.2f}, "
                 f"intrusos de alta frecuencia {100 * e['P6_intrusos_frecuentes']:.1f} %; efecto en cuartiles {100 * e['efecto_frecuencia_en_cuartiles']:+.1f} pts)")
        dd = e["dibujo"]
        L.append(f"  P7 dibujo: {e['P7']} (omisión distintivos {100 * dd['omis_distintivo']:.1f} % contra compartidos {100 * dd['omis_compartido']:.1f} %; "
                 f"pendiente de intrusiones de dominio {dd['intr_dominio_pendiente']:+.3f})")
        L.append(f"  P8 respuestas a nombres frecuentes o más típicos de la categoría crecen con el daño: {e['P8']} (pendiente {e['P8_pendiente']:+.3f})")
        L.append(f"  cuartiles dentro de ±10 puntos: {e['cuartiles_dentro']} de 4")
    mae, pdp = ev["mae"], ev["pdp"]
    viable = mae["P1"] and mae["P2"] and mae["P3"] and mae["P4"] and mae["cuartiles_dentro"] >= 3 and mae["P8"]
    aporta = (mae["P5"] and mae["P6"] and
              ((not pdp["P5"] or not pdp["P6"]) or
               (pdp["efecto_frecuencia_en_cuartiles"] <= mae["efecto_frecuencia_en_cuartiles"] - 0.10) or
               (pdp["P5_media"] < mae["P5_media"] / 2)))
    L.append(f"\nCRITERIO · MAE modelo viable de la DS: {viable} · MAE aporta algo que el PDP no: {aporta}")
    text = "\n".join(L)
    (out / "resumen.txt").write_text(text, encoding="utf-8")
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    (out / "resultados.json").write_text(json.dumps({"niveles": levels, "evaluacion": ev}, ensure_ascii=False, default=float))
    print(text)
