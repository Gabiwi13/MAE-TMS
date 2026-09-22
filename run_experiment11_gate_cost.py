"""Costo de la doble compuerta de contenido sobre las consultas reservadas de
exp11 (brazo T-protocolo). Reusa los destinos guardados en raw/*_c*.json y las
memorias en caché: no repite ruteos ni sorteos.

Uso: python run_experiment11_gate_cost.py [--cuts 25,50,100,200]
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from run_experiment11_monolithic import (  # noqa: E402
    CUTS, N_TEXT_TRAIN_PER_CLASS, OUT_DIR, RAW_DIR,
    gate_accepts, get_nlp, load_all_vectors, load_bank, load_cache, split_bank)


def write_md(out, cuts):
    L = ["# Costo de la doble compuerta sobre las consultas reservadas (T-protocolo)", "",
         "Filas: una por consulta reservada y semilla (171 × 10 por corte), primer sorteo. "
         "«Directorio acepta»: `route_transactive` da destino. «Compuerta rechaza»: el destino no da "
         "`recognize_gated > 0` para ninguna pista. Entre las rechazadas, «pierde respuesta» son las que "
         "sí tenían recall (`responde`), separadas por si el destino era el correcto.", "",
         "| corte | consultas | directorio acepta | compuerta rechaza | pierde respuesta, ruteo ok (clase ok) | pierde respuesta, ruteo mal | sin respuesta de todos modos |",
         "|---|---|---|---|---|---|---|"]
    for cut in cuts:
        c = out["cortes"][str(cut)]
        n, acc = c["consultas"], c.get("directorio_acepta", 0)
        rej = c.get("compuerta_rechaza", 0)
        L.append(f"| {cut} | {n} | {acc} ({acc/n*100:.1f} %) | {rej} ({rej/max(acc,1)*100:.2f} % de las aceptadas) | "
                 f"{c.get('pierde_respuesta_ruteo_ok', 0)} ({c.get('pierde_respuesta_ruteo_ok_clase_ok', 0)}) | "
                 f"{c.get('pierde_respuesta_ruteo_mal', 0)} | {c.get('sin_respuesta_de_todos_modos', 0)} |")
    if out["detalle"]:
        agg = Counter()
        for d in out["detalle"]:
            agg[(d["corte"], d["query"], d["truth"], d["destino"], d["ruteo_ok"], d["responde"])] += 1
        L += ["", "Consultas rechazadas por la compuerta, agregadas por consulta y destino (semillas: en cuántas de las 10 ocurre):", "",
              "| corte | consulta | clase | destino | ruteo ok | respondía | semillas |", "|---|---|---|---|---|---|---|"]
        for (cut, q, truth, dest, rok, resp), n in sorted(agg.items(), key=lambda kv: (kv[0][0], -kv[1], kv[0][1])):
            L.append(f"| {cut} | {q} | {truth} | {dest} | {rok} | {resp} | {n} |")
    else:
        L += ["", "La compuerta no rechaza ninguna consulta reservada aceptada por el directorio."]
    (OUT_DIR / "compuerta_reservadas.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"-> {OUT_DIR / 'compuerta_reservadas.md'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cuts", default=None)
    ap.add_argument("--report-only", action="store_true", help="solo el .md desde el .json")
    args = ap.parse_args()
    cuts = tuple(int(c) for c in args.cuts.split(",")) if args.cuts else CUTS
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if args.report_only:
        out = json.loads((OUT_DIR / "compuerta_reservadas.json").read_text(encoding="utf-8"))
        write_md(out, cuts)
        return

    nlp = get_nlp()
    vectors = load_all_vectors(nlp)
    train, held = split_bank(load_bank(nlp, vectors), N_TEXT_TRAIN_PER_CLASS)
    cues = {it["query"]: it["cues"] for it in train + held}

    out = {"cortes": {}, "detalle": []}
    for cut in cuts:
        specialists = load_cache(cut)["specialists"]
        rows = []
        for f in sorted(RAW_DIR.glob(f"s*_N{cut}_c*.json")):
            raw = json.loads(f.read_text(encoding="utf-8"))
            rows += [r for r in raw["texto"]
                     if r["brazo"] == "T-protocolo" and r["rep"] == 0 and r["banco"] == "reservado"]
        c = Counter()
        for r in rows:
            c["consultas"] += 1
            if not r["acepta"]:
                c["directorio_rechaza"] += 1
                continue
            c["directorio_acepta"] += 1
            ok = gate_accepts([specialists[r["destino"]]], cues[r["query"]])
            if ok:
                c["compuerta_acepta"] += 1
                continue
            c["compuerta_rechaza"] += 1
            if r["responde"]:
                key = "pierde_respuesta_" + ("ruteo_ok" if r["ruteo_ok"] else "ruteo_mal")
                c[key] += 1
                if r["ruteo_ok"] and r.get("nn_ok"):
                    c["pierde_respuesta_ruteo_ok_clase_ok"] += 1
            else:
                c["sin_respuesta_de_todos_modos"] += 1
            out["detalle"].append({"corte": cut, "semilla": r["semilla"], "query": r["query"],
                                   "truth": r["truth"], "destino": r["destino"],
                                   "ruteo_ok": r["ruteo_ok"], "responde": r["responde"],
                                   "pista": r.get("pista")})
        out["cortes"][str(cut)] = dict(c)
        print(f"N={cut}: {dict(c)}", flush=True)
        del specialists

    (OUT_DIR / "compuerta_reservadas.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    write_md(out, cuts)


if __name__ == "__main__":
    main()
