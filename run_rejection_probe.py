"""
Micro-test diagnóstico — rechazo por la EAM, no por filtro léxico.

El banco principal casi nunca rechaza por falta de soporte: sus consultas
describen los 8 dominios ETH-80. Este probe usa consultas que (a) producen al
menos un vector fastText real —son representables, no se filtran por léxico—
y (b) NO pertenecen a ninguno de los 8 dominios del sistema (apple, car, cow,
cup, dog, horse, pear, tomato). Si la EAM es el mecanismo de rechazo, deberían
rechazarse por containment (recognize_gated → 0 en todos los agentes), no por
una regla externa.

NO se asume 100 % de rechazo: se corre y se reporta lo que salga. Es
diagnóstico, separado del benchmark de accuracy principal.

Protocolo idéntico al oficial: tokenize_query → prevectorize (fastText real,
sin fallback) → recognize_gated → rechazo si max(score)==0.

Salidas en results/rejection_probe/.  Uso:  python run_rejection_probe.py
"""
import json
import io
import sys
import contextlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = ROOT / "results" / "rejection_probe"
OUT_DIR.mkdir(parents=True, exist_ok=True)

from quantizer import quantize_binary
from stage5_fill import load_agent_memories
from stage6_interaction import (
    Agent, CLASSES, M_LABEL,
    get_nlp, load_all_vectors, tokenize_query, prevectorize,
    get_fasttext_vector,
)

# Consultas representables (palabras reales con vector fastText) que NO
# pertenecen a ninguno de los 8 dominios. La EAM debería rechazarlas por
# containment. Nota v4: con 8 clases se retiraron dos probes de la versión
# de 3 clases que ahora SÍ son de dominio ("a glass container for water" →
# cup; "a green plant in a pot" → tomato/herb): contarlas como falso ruteo
# sería miscalibrar el diagnóstico.
PROBE_QUERIES = [
    "a musical instrument with strings",
    "a kitchen appliance that heats food",
    "a flying bird with feathers",
    "a sailing boat on the ocean",
    "a piece of furniture for sitting",
    "a tall building with many floors",
    "a cold mountain covered in snow",
    "a book with printed pages",
    "a river flowing to the sea",
    "a telephone for making calls",
    "a wooden table and chairs",
    "a pair of leather shoes",
]


def main():
    print("=" * 64)
    print("  MICRO-TEST — rechazo por la EAM (consultas fuera de dominio)")
    print("=" * 64)

    agents = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for cls in CLASSES:
            mem_H, mem_L, mem_R = load_agent_memories(cls)
            agents[cls] = Agent(cls, mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)

    nlp = get_nlp()
    vectors = load_all_vectors(nlp)
    toks = set()
    for q in PROBE_QUERIES:
        toks.update(tokenize_query(q, nlp))
    prevectorize(vectors, toks, allow_fallback=False)

    rows = []
    n_representable = n_mae_rejected = n_false_routes = 0
    for q in PROBE_QUERIES:
        scores = {cls: 0.0 for cls in CLASSES}
        represented, unrepresented = [], []
        for tok in tokenize_query(q, nlp):
            v = get_fasttext_vector(tok, vectors, allow_fallback=False)
            if v is None:
                unrepresented.append(tok)
                continue
            represented.append(tok)
            v_q = quantize_binary(np.asarray(v, dtype=np.float32), M_LABEL)
            for cls in CLASSES:
                scores[cls] += agents[cls].recognize_gated(v_q)

        if not represented:
            verdict, winner = "no_representable_tokens", None
        elif max(scores.values()) == 0.0:
            verdict, winner = "mae_rejected", None
            n_representable += 1
            n_mae_rejected += 1
        else:
            winner = max(scores, key=scores.get)
            verdict = "mae_false_route"
            n_representable += 1
            n_false_routes += 1

        rows.append({
            "query": q, "represented_tokens": represented,
            "unrepresented_tokens": unrepresented,
            "scores": {c: round(scores[c], 5) for c in CLASSES},
            "verdict": verdict, "winner": winner,
        })
        mark = {"mae_rejected": "RECHAZA (EAM)",
                "mae_false_route": f"rutea→{winner}",
                "no_representable_tokens": "sin pista"}[verdict]
        print(f"  [{mark:>16}]  '{q}'  repr={len(represented)}")

    summary = {
        "n_queries": len(PROBE_QUERIES),
        "representable_queries": n_representable,
        "mae_rejected": n_mae_rejected,
        "mae_false_routes": n_false_routes,
        "no_representable": len(PROBE_QUERIES) - n_representable,
        "notes": ("Probe diagnóstico de rechazo, no parte del benchmark de "
                  "accuracy. Consultas representables fuera de los 8 dominios "
                  "ETH-80; el rechazo (o no) sale de recognize_gated, sin "
                  "filtro léxico."),
    }
    (OUT_DIR / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT_DIR / "results_per_query.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n" + "-" * 64)
    print(f"  representables: {n_representable}/{len(PROBE_QUERIES)}")
    print(f"  rechazadas por la EAM: {n_mae_rejected}")
    print(f"  falsos routings (soporte espurio): {n_false_routes}")
    print(f"\nSalidas -> {OUT_DIR}")
    print("MICRO-TEST COMPLETADO.")


if __name__ == "__main__":
    main()
