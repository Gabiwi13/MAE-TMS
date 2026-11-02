"""
Solo el ruteo de T-protocolo en exp11, con directorios nuevos en cada
(semilla, corte). Sin recuerdo ni jueces: la cobertura (responde) sale de la
compuerta del recuerdo (la proyección del destino sin filas vacías), que es
determinista; el muestreo del recuerdo no decide si hay respuesta.

Antes de seguir con cada corte reproduce los trabajos oficiales que salieron
limpios (texto: s42 y trozos 0-3 de s43; imagen: s42; fuera de dominio: s42 y
s43) y se detiene si alguno no coincide.

Uso:  python results/experimento11_protocolo_corregido/ruteo_solo.py [--cuts 25,50,100,200]
      python results/experimento11_protocolo_corregido/ruteo_solo.py --solo-analisis
"""
import argparse
import contextlib
import io
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
import run_experiment11_monolithic as e11  # noqa: E402
from hetero_memory import _norm_weights  # noqa: E402

OLD = ROOT / "results" / "experimento11" / "raw"
OUT = HERE / "ruteo"
OOD_FILE = ROOT / "results" / "experimento11" / "consultas_fuera_dominio.txt"
P = "T-protocolo"
SEEDS = e11.SEEDS
CUTS = e11.CUTS
CLEAN_TEXT = {(42, k) for k in range(6)} | {(43, k) for k in range(4)}
CLEAN_IMG = {(42, k) for k in range(6)}
CLEAN_OOD_FIRST = (42, 43)


def quiet(f, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return f(*a, **kw)


def gate_recall(mem, cue, dim, weights=None):
    """La compuerta de recall_from_left/right: hay respuesta si la proyección
    no tiene filas vacías (mismos pesos que el recuerdo)."""
    w = _norm_weights(mem._default_weights(cue, weights, dim), len(cue))
    proj = quiet(mem.project, mem.validate(cue, dim), w, dim)
    return bool(np.count_nonzero(np.sum(proj, axis=1) == 0) == 0)


def prepare():
    nlp = e11.get_nlp()
    vectors = e11.load_all_vectors(nlp)
    bank = e11.load_bank(nlp, vectors)
    train, held = e11.split_bank(bank, e11.N_TEXT_TRAIN_PER_CLASS)
    bank = train + held
    train_idx = list(range(len(train)))
    queries = [l.strip() for l in OOD_FILE.read_text(encoding="utf-8").splitlines()
               if l.strip() and not l.startswith("#")]
    ood = e11.load_ood(nlp, vectors, queries)
    g_min, g_max = e11.load_global_stats()
    img_pools = e11.load_image_pools(g_min, g_max, e11.N_IMG_TRAIN, e11.N_IMG_TEST)
    return bank, train_idx, ood, img_pools


def run_seed(seed, cut, specialists, bank, train_idx, ood, img_pools, memo):
    t0 = time.time()
    train = [bank[i] for i in train_idx]
    train_set = set(train_idx)
    held_idx = [i for i, it in enumerate(bank) if it["cues"] and i not in train_set]

    e11.reset_directories(specialists)
    form_t = e11.form_text_directories(specialists, e11.TME(), train, np.random.RandomState(seed))
    texto = []
    for pos, idx in enumerate(held_idx):
        it = bank[idx]
        entry = e11.AGENT_LIST[int(np.random.RandomState(seed * 1000 + idx).randint(e11.K))]
        dest, _s, consulted, hops = quiet(e11.route_transactive, entry, specialists,
                                          [v for _, v in it["cues"]], modality="text")
        responde = False
        if dest >= 0:
            key = ("t", dest, idx)
            if key not in memo:
                mem = specialists[e11.CLASSES[dest]].mem_dom_H
                memo[key] = any(gate_recall(mem, v, 0) for _, v in it["cues"])
            responde = memo[key]
        texto.append({"semilla": seed, "corte": cut, "query": it["query"], "truth": it["truth"],
                      "trozo": pos % 6, "entrada": entry,
                      "destino": e11.CLASSES[dest] if dest >= 0 else None,
                      "consultados": len(consulted), "saltos": hops, "acepta": dest >= 0,
                      "ruteo_ok": (dest == it["tidx"]) if dest >= 0 else None,
                      "responde": responde, "clase_ok": bool(responde and dest == it["tidx"])})
    # run_ood_job forma con la misma semilla y el mismo orden: son los mismos directorios.
    fuera = quiet(e11.ood_rows_for, seed, cut, specialists, None, ood, (P,))

    e11.reset_directories(specialists)
    img_train, img_test = img_pools
    form_i = quiet(e11.form_image_directories, specialists, e11.TME(), img_train,
                   np.random.RandomState(seed))
    imagen = []
    for j, (path, z_q, ci) in enumerate(img_test):
        entry = e11.CLASSES[(ci + 1) % e11.K]
        d, *_ = quiet(e11.route_transactive, entry, specialists, z_q,
                      modality="image", xi=e11.XI_VISUAL)
        responde = False
        if d >= 0:
            key = ("i", d, j)
            if key not in memo:
                ag = specialists[e11.CLASSES[d]]
                memo[key] = gate_recall(ag.mem_dom_H, z_q, 1, weights=ag.mem_dom_R.recog_weights(z_q))
            responde = memo[key]
        imagen.append({"semilla": seed, "corte": cut, "imagen": Path(path).name,
                       "truth": e11.CLASSES[ci], "trozo": j % 6, "entrada": entry,
                       "destino": e11.CLASSES[d] if d >= 0 else None, "acepta": d >= 0,
                       "ruteo_ok": (d == ci) if d >= 0 else None, "responde": responde,
                       "clase_ok": bool(responde and d == ci)})
    return {"meta": {"semilla": seed, "corte": cut, "formacion_texto": form_t,
                     "formacion_imagen": form_i, "segundos": round(time.time() - t0, 1)},
            "texto": texto, "ood": fuera, "imagen": imagen}


# ---------- raw oficiales ----------

def load_old():
    """Filas oficiales por brazo, con el trozo de origen."""
    old = {"texto": [], "imagen": [], "ood": []}
    for f in sorted(OLD.glob("s*_N*_*.json")):
        kind = f.stem.split("_")[2]
        raw = json.loads(f.read_text(encoding="utf-8"))
        k = int(kind[1:])
        if kind[0] == "c":
            for r in raw["texto"]:
                r = {x: v for x, v in r.items() if x != "z"}
                r["trozo"] = k
                old["texto"].append(r)
        elif kind[0] == "i":
            for r in raw["imagen"]:
                r = dict(r, imagen=Path(r["imagen"]).name, trozo=k)
                old["imagen"].append(r)
        elif kind[0] == "o":
            old["ood"] += raw["ood"]
    return old


def verify(new_runs, old, seeds=None):
    """Compara el ruteo nuevo con el oficial. Devuelve conteos de coincidencia
    en los trabajos limpios y en el resto."""
    sel = lambda s: seeds is None or s in seeds
    o_t = {(r["semilla"], r["corte"], r["query"]): r for r in old["texto"]
           if r["brazo"] == P and r["rep"] == 0}
    o_i = {(r["semilla"], r["corte"], r["imagen"]): r for r in old["imagen"] if r["brazo"] == P}
    o_o = {(r["semilla"], r["corte"], r["query"]): r for r in old["ood"] if r["brazo"] == P}
    res = defaultdict(lambda: [0, 0])
    bad = []
    for run in new_runs:
        for r in run["texto"]:
            if not sel(r["semilla"]):
                continue
            o = o_t[(r["semilla"], r["corte"], r["query"])]
            clean = (o["semilla"], o["trozo"]) in CLEAN_TEXT
            same = all(o[k] == r[k] for k in ("entrada", "destino", "consultados", "saltos", "acepta"))
            res["texto_limpio" if clean else "texto_resto"][0] += same
            res["texto_limpio" if clean else "texto_resto"][1] += 1
            if clean and not same:
                bad.append(("texto", r["semilla"], r["corte"], r["query"]))
        for r in run["imagen"]:
            if not sel(r["semilla"]):
                continue
            o = o_i[(r["semilla"], r["corte"], r["imagen"])]
            clean = (o["semilla"], o["trozo"]) in CLEAN_IMG
            same = o["destino"] == r["destino"] and o["acepta"] == r["acepta"]
            res["imagen_limpio" if clean else "imagen_resto"][0] += same
            res["imagen_limpio" if clean else "imagen_resto"][1] += 1
            if clean and not same:
                bad.append(("imagen", r["semilla"], r["corte"], r["imagen"]))
        for r in run["ood"]:
            if not sel(r["semilla"]):
                continue
            o = o_o[(r["semilla"], r["corte"], r["query"])]
            same = all(o[k] == r[k] for k in ("acepta", "acepta_compuerta", "destino"))
            res["ood"][0] += same
            res["ood"][1] += 1
            if not same:
                bad.append(("ood", r["semilla"], r["corte"], r["query"]))
    return {k: {"iguales": v[0], "total": v[1]} for k, v in res.items()}, bad


# ---------- análisis ----------

def binom_two_sided(k, n):
    import math
    if n == 0:
        return 1.0
    k = min(k, n - k)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def paired(a, b, unit):
    """a, b: dict clave -> 0/1 sobre las mismas claves; unit(clave) agrupa para
    el bootstrap. McNemar exacto (b10: a sí y b no; b01: b sí y a no) y
    bootstrap por unidad de la diferencia b − a."""
    keys = sorted(set(a) & set(b))
    n10 = sum(a[k] and not b[k] for k in keys)
    n01 = sum(b[k] and not a[k] for k in keys)
    groups = defaultdict(list)
    for k in keys:
        groups[unit(k)].append(b[k] - a[k])
    d = np.array([np.mean(v) for v in groups.values()])
    rng = np.random.RandomState(0)
    boots = d[rng.randint(0, len(d), size=(10000, len(d)))].mean(axis=1)
    return {"pares": len(keys), "M_si_P_no": n10, "P_si_M_no": n01,
            "p": binom_two_sided(n10, n10 + n01), "diferencia": float(np.mean([b[k] - a[k] for k in keys])),
            "unidades": len(d), "bootstrap": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}


def per_seed(rows, fn, seeds):
    by = defaultdict(list)
    for r in rows:
        v = fn(r)
        if v is not None:
            by[r["semilla"]].append(float(v))
    return e11._ci([float(np.mean(by[s])) for s in seeds if by[s]])


def analyze(new_runs, old):
    seeds = sorted({r["meta"]["semilla"] for r in new_runs})
    cuts = sorted({r["meta"]["corte"] for r in new_runs})
    nt = [r for run in new_runs for r in run["texto"]]
    ni = [r for run in new_runs for r in run["imagen"]]
    no = [r for run in new_runs for r in run["ood"]]
    keep = lambda r: r["semilla"] in seeds and r["corte"] in cuts
    ot = [r for r in old["texto"] if keep(r)]
    oi = [r for r in old["imagen"] if keep(r)]
    oo = [r for r in old["ood"] if keep(r)]
    S = {"semillas": seeds, "cortes": cuts, "texto": {}, "imagen": {}, "ood": {}, "pruebas": {}, "identidades": {}}

    # Identidades sobre los raw oficiales.
    def ident(rows, lhs, rhs):
        n = len(rows)
        eq = sum(lhs(r) == rhs(r) for r in rows)
        return {"iguales": eq, "total": n}
    otp = [r for r in ot if r["brazo"] == P]
    oip = [r for r in oi if r["brazo"] == P]
    clean_t = [r for r in otp if (r["semilla"], r["trozo"]) in CLEAN_TEXT]
    clean_i = [r for r in oip if (r["semilla"], r["trozo"]) in CLEAN_IMG]
    cls_old = lambda r: bool(r["responde"]) and bool(r.get("nn_ok"))
    cls_route = lambda r: bool(r["responde"]) and bool(r["ruteo_ok"])
    S["identidades"] = {
        "texto_clase_igual_responde_y_ruteo_limpios": ident(clean_t, cls_old, cls_route),
        "texto_clase_igual_responde_y_ruteo_todos": ident(otp, cls_old, cls_route),
        "texto_clase_igual_ruteo_limpios": ident(clean_t, cls_old, lambda r: bool(r["ruteo_ok"])),
        "imagen_hit_igual_responde_y_ruteo_limpios": ident(clean_i, lambda r: bool(r["hit"]), cls_route),
        "imagen_hit_igual_responde_y_ruteo_todos": ident(oip, lambda r: bool(r["hit"]), cls_route),
    }
    # La compuerta del recuerdo contra la respuesta oficial, donde el destino coincide.
    nt_by = {(r["semilla"], r["corte"], r["query"]): r for r in nt}
    ni_by = {(r["semilla"], r["corte"], r["imagen"]): r for r in ni}
    same_t = [(o, nt_by[(o["semilla"], o["corte"], o["query"])]) for o in otp
              if nt_by[(o["semilla"], o["corte"], o["query"])]["destino"] == o["destino"]]
    same_i = [(o, ni_by[(o["semilla"], o["corte"], o["imagen"])]) for o in oip
              if ni_by[(o["semilla"], o["corte"], o["imagen"])]["destino"] == o["destino"]]
    S["identidades"]["texto_responde_compuerta_igual_oficial"] = {
        "iguales": sum(bool(o["responde"]) == n["responde"] for o, n in same_t), "total": len(same_t)}
    S["identidades"]["imagen_responde_compuerta_igual_oficial"] = {
        "iguales": sum(bool(o["responde"]) == n["responde"] for o, n in same_i), "total": len(same_i)}

    for cut in cuts:
        c = lambda rows, arm=None: [r for r in rows if r["corte"] == cut and (arm is None or r["brazo"] == arm)]
        t_new, t_old, t_m = c(nt), c(ot, P), c(ot, "M")
        S["texto"][cut] = {
            "nuevo": {"acepta": per_seed(t_new, lambda r: r["acepta"], seeds),
                      "ruteo_ok": per_seed(t_new, lambda r: r["ruteo_ok"], seeds),
                      "responde": per_seed(t_new, lambda r: r["responde"], seeds),
                      "clase_total": per_seed(t_new, lambda r: r["clase_ok"], seeds)},
            "viejo": {"acepta": per_seed(t_old, lambda r: r["acepta"], seeds),
                      "ruteo_ok": per_seed(t_old, lambda r: r["ruteo_ok"], seeds),
                      "responde": per_seed(t_old, lambda r: r["responde"], seeds),
                      "clase_total": per_seed(t_old, cls_old, seeds)},
            "M": {"acepta": per_seed(t_m, lambda r: r["acepta"], seeds),
                  "responde": per_seed(t_m, lambda r: r["responde"], seeds),
                  "clase_total": per_seed(t_m, cls_old, seeds)}}
        m = {(r["semilla"], r["query"], r["rep"]): int(cls_old(r)) for r in t_m}
        pn = {k: int(nt_by[(k[0], cut, k[1])]["clase_ok"]) for k in m}
        po = {(r["semilla"], r["query"], r["rep"]): int(cls_old(r)) for r in t_old}
        S["pruebas"][f"texto|{cut}"] = {"nuevo": paired(m, pn, lambda k: k[1]),
                                        "viejo": paired(m, po, lambda k: k[1])}

        i_new, i_old, i_m = c(ni), c(oi, P), c(oi, "M")
        S["imagen"][cut] = {
            "nuevo": {k: per_seed(i_new, lambda r, k=k: r[k], seeds) for k in ("acepta", "ruteo_ok", "responde", "clase_ok")},
            "viejo": {"acepta": per_seed(i_old, lambda r: r["acepta"], seeds),
                      "ruteo_ok": per_seed(i_old, lambda r: r.get("ruteo_ok"), seeds),
                      "responde": per_seed(i_old, lambda r: r["responde"], seeds),
                      "clase_ok": per_seed(i_old, lambda r: r["hit"], seeds)},
            "M": {"acepta": per_seed(i_m, lambda r: r["acepta"], seeds),
                  "responde": per_seed(i_m, lambda r: r["responde"], seeds),
                  "clase_ok": per_seed(i_m, lambda r: r["hit"], seeds)}}
        m = {(r["semilla"], r["imagen"]): int(r["hit"]) for r in i_m}
        pn = {(r["semilla"], r["imagen"]): int(r["clase_ok"]) for r in i_new}
        po = {(r["semilla"], r["imagen"]): int(r["hit"]) for r in i_old}
        S["pruebas"][f"imagen|{cut}"] = {"nuevo": paired(m, pn, lambda k: k[1]),
                                         "viejo": paired(m, po, lambda k: k[1])}

        o_new, o_old, o_m = c(no), c(oo, P), c(oo, "M")
        S["ood"][cut] = {
            "nuevo": {k: per_seed(o_new, lambda r, k=k: r[k], seeds) for k in ("acepta", "acepta_compuerta")},
            "viejo": {k: per_seed(o_old, lambda r, k=k: r[k], seeds) for k in ("acepta", "acepta_compuerta")},
            "M": {"acepta": per_seed(o_m, lambda r: r["acepta"], seeds)}}
        m = {(r["semilla"], r["query"]): int(r["acepta"]) for r in o_m}
        S["pruebas"][f"ood|{cut}"] = {
            k: paired(m, {(r["semilla"], r["query"]): int(r[k]) for r in o_new}, lambda x: x[1])
            for k in ("acepta", "acepta_compuerta")}
        acc = defaultdict(lambda: [0, 0, set()])
        for r in o_new:
            if r["acepta"]:
                acc[r["query"]][0] += 1
                acc[r["query"]][2].add(r["destino"])
            acc[r["query"]][1] += int(r["acepta_compuerta"])
        S["ood"][cut]["aceptadas_nuevo"] = {q: {"semillas": a, "con_compuerta": g, "destinos": sorted(d)}
                                            for q, (a, g, d) in acc.items() if a}
    return S


def fmt(ci):
    return e11._fmt(ci)


def report(S, ver, times):
    L = ["# exp11, solo ruteo de T-protocolo con directorios corregidos", "",
         f"Semillas {S['semillas']}, cortes {S['cortes']}. Media entre semillas e IC 95 % bootstrap "
         "sobre semillas. «Viejo» y M salen de los raw oficiales de exp11.", "",
         "## Reproducción de los trabajos oficiales limpios", "",
         "| conjunto | iguales / total |", "|---|---|"]
    for k, v in ver.items():
        L.append(f"| {k} | {v['iguales']} / {v['total']} |")
    L += ["", "Texto compara entrada, destino, círculo, saltos y aceptación; imagen, destino y aceptación; "
          "fuera de dominio, aceptación con y sin compuerta y destino. «resto» son los trabajos que en la "
          "corrida oficial heredaron directorios: ahí las diferencias son el efecto del error.", "",
          "## Identidades comprobadas en los raw oficiales", "", "| identidad | iguales / filas |", "|---|---|"]
    for k, v in S["identidades"].items():
        L.append(f"| {k} | {v['iguales']} / {v['total']} |")
    L += ["", "## Texto (171 reservadas por semilla)", "",
          "| N | brazo | acepta | ruteo ok | responde | clase correcta sobre el total |", "|---|---|---|---|---|---|"]
    for cut, d in S["texto"].items():
        for arm, lab in (("viejo", "protocolo viejo"), ("nuevo", "protocolo corregido"), ("M", "EHAM única")):
            x = d[arm]
            L.append(f"| {cut} | {lab} | {fmt(x['acepta'])} | {fmt(x.get('ruteo_ok'))} | "
                     f"{fmt(x['responde'])} | {fmt(x['clase_total'])} |")
    L += ["", "## Imagen (80 por semilla)", "",
          "Clase: en M y en el protocolo viejo es el hit laxo (una de las 3 etiquetas evocadas es del "
          "vocabulario de la clase); en el corregido, responde en el especialista correcto (igual al hit "
          "laxo en los raw oficiales, ver identidades).", "",
          "| N | brazo | acepta | ruteo ok | responde | clase |", "|---|---|---|---|---|---|"]
    for cut, d in S["imagen"].items():
        for arm, lab in (("viejo", "protocolo viejo"), ("nuevo", "protocolo corregido"), ("M", "EHAM única")):
            x = d[arm]
            L.append(f"| {cut} | {lab} | {fmt(x['acepta'])} | {fmt(x.get('ruteo_ok'))} | "
                     f"{fmt(x['responde'])} | {fmt(x['clase_ok'])} |")
    L += ["", "## Fuera de dominio (40 consultas)", "",
          "| N | brazo | acepta | acepta con compuerta |", "|---|---|---|---|"]
    for cut, d in S["ood"].items():
        for arm, lab in (("viejo", "protocolo viejo"), ("nuevo", "protocolo corregido")):
            L.append(f"| {cut} | {lab} | {fmt(d[arm]['acepta'])} | {fmt(d[arm]['acepta_compuerta'])} |")
        L.append(f"| {cut} | EHAM única | {fmt(d['M']['acepta'])} | {fmt(d['M']['acepta'])} |")
    L += ["", "## Protocolo contra EHAM única", "",
          "McNemar exacto sobre los pares; bootstrap de la diferencia P − M remuestreando consultas "
          "(o imágenes), con cada una promediada entre semillas y sorteos. En texto los pares son "
          "(semilla, consulta, sorteo de M): el protocolo corregido es determinista por (semilla, consulta), "
          "así que el p de McNemar es optimista; el bootstrap por consulta es la prueba conservadora.", "",
          "| prueba | N | lado | pares | M sí, P no | P sí, M no | P − M | p | bootstrap por consulta |",
          "|---|---|---|---|---|---|---|---|---|"]
    for key, d in S["pruebas"].items():
        kind, cut = key.split("|")
        for lado, x in d.items():
            L.append(f"| {kind} | {cut} | {lado} | {x['pares']} | {x['M_si_P_no']} | {x['P_si_M_no']} | "
                     f"{x['diferencia']*100:+.2f} | {x['p']:.3g} | "
                     f"{x['bootstrap'][0]*100:+.2f}, {x['bootstrap'][1]*100:+.2f} |")
    L += ["", "En fuera de dominio, «acepta» y «acepta_compuerta» comparan la aceptación del protocolo "
          "(sin y con la segunda compuerta) con la de M; ahí aceptar es fallar.", "",
          "## Fuera de dominio aceptadas por el protocolo corregido", ""]
    for cut, d in S["ood"].items():
        L.append(f"- N = {cut}: " + "; ".join(f"«{q}» {x['semillas']} semillas, {x['con_compuerta']} con "
                                              f"compuerta → {x['destinos']}" for q, x in d["aceptadas_nuevo"].items()))
    L += ["", "## Tiempo", "", "| corte | semillas | s por semilla (texto + fuera de dominio + imagen) |",
          "|---|---|---|"]
    for cut, v in sorted(times.items()):
        L.append(f"| {cut} | {len(v)} | {np.mean(v):.0f} |")
    return L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cuts", default=",".join(str(c) for c in CUTS))
    ap.add_argument("--solo-analisis", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    old = load_old()

    if not args.solo_analisis:
        t0 = time.time()
        bank, train_idx, ood, img_pools = prepare()
        print(f"preparación {time.time()-t0:.0f}s", flush=True)
        order = list(CLEAN_OOD_FIRST) + [s for s in SEEDS if s not in CLEAN_OOD_FIRST]
        for cut in (int(c) for c in args.cuts.split(",")):
            path = OUT / f"filas_N{cut}.json"
            if path.exists():
                print(f"N={cut} ya está", flush=True)
                continue
            t1 = time.time()
            cached = e11.load_cache(cut)
            specialists = cached["specialists"]
            del cached
            print(f"N={cut}: caché cargado en {time.time()-t1:.0f}s", flush=True)
            memo, runs = {}, []
            for seed in order:
                runs.append(run_seed(seed, cut, specialists, bank, train_idx, ood, img_pools, memo))
                print(f"  s{seed} N{cut}: {runs[-1]['meta']['segundos']}s", flush=True)
                if seed == CLEAN_OOD_FIRST[-1]:
                    ver, bad = verify(runs, old)
                    print(f"  verificación N={cut}: {ver}", flush=True)
                    clean_bad = [b for b in bad if b[0] != "ood" or b[1] in CLEAN_OOD_FIRST]
                    if any(v["iguales"] != v["total"] for k, v in ver.items() if "limpio" in k or k == "ood") \
                            or clean_bad:
                        (OUT / f"verificacion_fallida_N{cut}.json").write_text(
                            json.dumps({"conteos": ver, "distintas": bad}, ensure_ascii=False, indent=2),
                            encoding="utf-8")
                        sys.exit(f"N={cut}: el ruteo no reproduce los trabajos oficiales limpios; se detiene")
            path.write_text(json.dumps(runs, ensure_ascii=False), encoding="utf-8")
            del specialists
        print(f"ruteo terminado en {(time.time()-t0)/60:.1f} min", flush=True)

    new_runs = []
    for f in sorted(OUT.glob("filas_N*.json")):
        new_runs += json.loads(f.read_text(encoding="utf-8"))
    ver, bad = verify(new_runs, old)
    S = analyze(new_runs, old)
    times = defaultdict(list)
    for run in new_runs:
        times[run["meta"]["corte"]].append(run["meta"]["segundos"])
    (OUT / "resumen.json").write_text(json.dumps({"verificacion": ver, "distintas": bad, **S},
                                                 ensure_ascii=False, indent=2, default=list), encoding="utf-8")
    L = report(S, ver, times)
    (OUT / "ruteo.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
