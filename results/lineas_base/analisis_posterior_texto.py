"""Análisis agregado después de ver los resultados de texto (declarado en el
README como posterior): compuerta de la EAM contra pertenencia léxica,
McNemar con las dos cotas de empate y qué consultas fuera de dominio pasan.

Uso:  python results/lineas_base/analisis_posterior_texto.py
"""
import contextlib
import io
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from quantizer import quantize_binary
from stage6_interaction import CLASSES, M_LABEL, get_nlp, load_all_vectors, tokenize_query, get_fasttext_vector
from run_experiment9_member_loss import load_bank
import run_ablation as abl
from lineas_base_texto import mcnemar, OOD_FILE


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    nlp = get_nlp()
    vectors = load_all_vectors(nlp)
    with contextlib.redirect_stdout(io.StringIO()):
        bank = load_bank(nlp, vectors)
    ood_q = [l.strip() for l in OOD_FILE.read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.startswith("#")]
    mdoms = abl.load_base_mdoms()
    agents = {c: abl.Agent(c, mdoms[c]) for c in CLASSES}
    vocab = {c: set(vectors[c].keys()) for c in CLASSES}

    # 1. compuerta (recognize_gated > 0) contra pertenencia al vocabulario, por token y clase
    toks = set()
    for q in [it["query"] for it in bank] + ood_q:
        toks.update(tokenize_query(q, nlp))
    tab = defaultdict(int)
    raros = []
    for t in sorted(toks):
        v = get_fasttext_vector(t, vectors, allow_fallback=False)
        if v is None:
            continue
        vq = quantize_binary(np.asarray(v, dtype=np.float32), M_LABEL)
        for c in CLASSES:
            g = agents[c].recognize_gated(vq) > 0
            m = t in vocab[c]
            tab[(m, g)] += 1
            if m != g:
                raros.append({"token": t, "clase": c, "en_vocabulario": m, "compuerta_acepta": g})
    gate = {"vocab_y_acepta": tab[(True, True)], "vocab_y_rechaza": tab[(True, False)],
            "fuera_y_acepta": tab[(False, True)], "fuera_y_rechaza": tab[(False, False)],
            "discrepancias": raros}

    # 2. McNemar con cotas de empate (inf: empate = fallo; sup: empate a favor de la verdad)
    rows = json.loads((OUT / "filas_texto.json").read_text(encoding="utf-8"))
    by = defaultdict(dict)
    for r in rows:
        by[(r["particion"], r["decisor"])][r["query"]] = r
    resumen = json.loads((OUT / "resumen_texto.json").read_text(encoding="utf-8"))
    exp11 = {}
    import glob
    for f in glob.glob(str(ROOT / "results" / "experimento11" / "raw" / "s*_N200_c*.json")):
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        for r in d["texto"]:
            if r["brazo"] == "T-protocolo" and r["rep"] == 0 and r["banco"] == "reservado":
                exp11.setdefault(r["semilla"], {})[r["query"]] = int(bool(r["ruteo_ok"]))
    pares = {}
    for p in ("cal400", "proto80", "res171"):
        qs = list(by[(p, "eam_temprana")].keys())
        eam = [by[(p, "eam_temprana")][q]["inf"] for q in qs]
        best = resumen["mcnemar"][p]["mejor_linea_base"]
        out = {}
        for d in ("voto|-|-", best, "tabla_conteos"):
            for cota in ("inf", "sup"):
                b = [by[(p, d)][q][cota] for q in qs]
                out[f"{d} ({cota}) vs eam_temprana"] = mcnemar(b, eam)
                if p == "res171":
                    vals = [mcnemar(b, [exp11[s][q] for q in qs]) for s in sorted(exp11)]
                    out[f"{d} ({cota}) vs T-protocolo, rango de p en 10 semillas"] = \
                        [min(v[2] for v in vals), max(v[2] for v in vals)]
        pares[p] = out

    # 3. qué fuera de dominio acepta cada decisor con rechazo
    ood = {}
    for d in ("voto|-|-", "eam_temprana", "tabla_conteos[cal400]", "tabla_conteos[res171]"):
        ood[d] = [{"query": q, "pred": r["pred"]} for q, r in by[("ood40", d)].items() if r["decide"]]

    # 4. acepta la EAM exactamente las mismas consultas que el voto
    misma = {}
    for p in ("cal400", "proto80", "res171", "ood40"):
        a = by[(p, "eam_temprana")]; v = by[(p, "voto|-|-")]
        misma[p] = {"eam_acepta": sum(r["decide"] for r in a.values()),
                    "voto_acepta": sum(r["decide"] for r in v.values()),
                    "difieren": [q for q in a if a[q]["decide"] != v[q]["decide"]]}

    # 5. voto ponderado por la frecuencia de la etiqueta (posterior): absoluta y
    # relativa al total de la clase, que es la proporción con que entra al llenado
    from lineas_base_texto import outcome, split_bank, N_TEXT_TRAIN_PER_CLASS
    train, held = split_bank(bank, N_TEXT_TRAIN_PER_CLASS)
    parts = {"cal400": bank[:400], "proto80": bank[:80], "res171": held}
    freq = {}
    for c in CLASSES:
        f = json.loads((ROOT / f"labels_{c}.json").read_text())
        lv = json.loads((ROOT / f"label_vectors_{c}.json").read_text())
        f = {w: n for w, n in f.items() if w in lv}
        lem = {}
        for w, n in f.items():
            l = nlp(w)[0].lemma_
            if l != w and l not in f:
                lem[l] = n
        f.update(lem)
        freq[c] = f
    tot = {c: sum(n for w, n in json.loads((ROOT / f"labels_{c}.json").read_text()).items()
                  if w in json.loads((ROOT / f"label_vectors_{c}.json").read_text())) for c in CLASSES}
    voto_frec = {}
    for p, items in parts.items():
        eam = {it["query"]: by[(p, "eam_temprana")][it["query"]] for it in items}
        for modo in ("abs", "rel"):
            res_p, igual = [], 0
            for it in items:
                toks_q = tokenize_query(it["query"], nlp)
                s = np.array([sum(freq[c].get(t, 0) / (tot[c] if modo == "rel" else 1) for t in toks_q)
                              for c in CLASSES])
                o = outcome(s, it["tidx"], s.max() > 0)
                res_p.append(o)
                e = eam[it["query"]]
                igual += int((o["pred"] or []) == (e["pred"] or []))
            n = len(items)
            voto_frec[f"{p}|{modo}"] = {
                "acierto_pct": round(100 * sum(o["esperado"] for o in res_p) / n, 2),
                "empates": sum(o["empate"] for o in res_p),
                "misma_decision_que_eam": igual, "n": n,
                "mcnemar_inf_vs_eam": mcnemar([o["inf"] for o in res_p],
                                              [eam[it["query"]]["inf"] for it in items])}

    res = {"compuerta_vs_vocabulario": gate, "mcnemar_cotas": pares,
           "ood_aceptadas": ood, "aceptacion_eam_vs_voto": misma,
           "voto_ponderado_por_frecuencia": voto_frec}
    (OUT / "analisis_posterior_texto.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
