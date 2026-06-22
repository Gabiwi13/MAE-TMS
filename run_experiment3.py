"""
Experimento 3 — Protocolo completo del experimento 1 con el routing corregido.

Scoring oficial (validado en exp. 2):
  1. Gate de containment (η re-acoplado): fila vacía en la proyección → score 0.
     Mecanismo nativo de Pineda; el score es la activación media de las celdas
     no nulas (Agent.recognize_gated), SIN división por mem.mean. Con el llenado
     por instancias las masas quedan igualadas por construcción y ÷mem.mean es
     redundante (exp. 2 lo confirma: gate solo da 100% en el diagnóstico).
  2. B1 (÷count+1) en fase madura, como en la condición B1 del ablation.

Protocolo (idéntico al exp. 1 / stages 6+8, arquitectura 4-AMR completa):
  - Agentes con M_dom_L/R/H de stage5 (solo lectura) + M_dir EHAM fresco.
  - TME con M_dir_L / M_dir_R (DirectoryMemory) frescos.
  - Fase temprana: broadcast → score corregido → argmax → los 4 componentes
    registran (v_q → ganador) → recall en ganador → learn_latent en M_dir_R.
  - Fase madura: TME apagado, entrada aleatoria (seed 42), routing por M_dir
    del agente de entrada con B1, rechazo explícito.

Corpus: banco de 80 queries del ablation (ground truth 27/27/26) +
réplica del protocolo original de 10 TEST_QUERIES para comparación directa.

No modifica ningún artefacto del exp. 1 (models/*.pkl intactos).
Salidas en results/exp3_corrected_routing/

Uso:  python run_experiment3.py
"""
import csv
import io
import json
import pickle
import sys
import contextlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = ROOT / "results" / "exp3_corrected_routing"
OUT_DIR.mkdir(parents=True, exist_ok=True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from quantizer import quantize_binary
from stage5_fill import load_agent_memories
from stage6_interaction import (
    Agent, TME, CLASSES, AGENT_LIST, M_LABEL, N,
    get_nlp, load_all_vectors, tokenize_query,
    get_fasttext_vector, token_in_vocabulary, TEST_QUERIES,
)

DOMAIN_COLOR = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60"}


# Routing oficial (exp. 2): gate de containment, sin división por mem.mean

def corrected_score(agent, v_q):
    """Scoring oficial: Agent.recognize_gated (activación media de las celdas
    no nulas, gateada por containment). Sin calibración ÷mem.mean."""
    return agent.recognize_gated(v_q)


def process_query_early(query, agents, tme, nlp, vectors, tok_cache,
                        do_recall=True):
    """
    Fase temprana corregida — protocolo de stage6.process_query:
    tokenize → broadcast → argmax → aprendizaje en los 4 M_dir →
    recall en ganador → learn_latent.
    """
    tokens = [t for t in tokenize_query(query, nlp)
              if token_in_vocabulary(t, vectors)]
    if not tokens:
        return {"winner": None, "tokens": [], "rejected": True}

    for tok in tokens:
        if tok not in tok_cache:
            v = np.array(get_fasttext_vector(tok, vectors), dtype=np.float32)
            tok_cache[tok] = quantize_binary(v, M_LABEL)

    scores = {cls: 0.0 for cls in CLASSES}
    for tok in tokens:
        v_q = tok_cache[tok]
        for cls in CLASSES:
            scores[cls] += corrected_score(agents[cls], v_q)

    if sum(scores.values()) == 0:
        return {"winner": None, "tokens": tokens, "rejected": True}

    winner = max(scores, key=scores.get)
    widx = AGENT_LIST.index(winner)

    # Aprendizaje — los 4 componentes registran (fiel a stage6:293-297)
    for tok in tokens:
        v_q = tok_cache[tok]
        tme.update_directory(v_q, widx)
        for agent in agents.values():
            agent.update_directory(v_q, widx)

    # Recall en el ganador + learn_latent (fiel a stage6:299-324)
    if do_recall:
        for tok in tokens:
            with contextlib.redirect_stdout(io.StringIO()):
                r_q, recognized, weight, *_ = agents[winner].recall(
                    tok_cache[tok])
            if recognized:
                tme.update_directory_latent(r_q.astype(np.int32), widx)
                break

    return {"winner": winner, "tokens": tokens, "rejected": False,
            "scores": scores}


def route_mature(tokens, entry_agent, tok_cache, b1=True):
    """Fase madura — protocolo de stage8: M_dir del agente de entrada, B1."""
    agg = np.zeros(len(CLASSES), dtype=float)
    for tok in tokens:
        v_q = tok_cache[tok]
        agg += (entry_agent.mem_dir.predict_normalized(v_q, mode="linear")
                if b1 else entry_agent.mem_dir.predict(v_q))
    if agg.sum() == 0:
        return None
    return CLASSES[int(np.argmax(agg))]


# Main

def main():
    print("=" * 64)
    print("  EXPERIMENTO 3 — exp. 1 completo con routing corregido")
    print("  (gate η en temprana · B1 en madura)")
    print("=" * 64)

    print("\nCargando M_dom de stage5 (solo lectura) y construyendo "
          "arquitectura fresca...")
    agents = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for cls in CLASSES:
            mem_H, mem_L, mem_R = load_agent_memories(cls)
            agents[cls] = Agent(cls, mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)
        tme = TME()

    nlp = get_nlp()
    vectors = load_all_vectors(nlp)   # alias por lema: spaCy es parte del core
    from eval_bank import ALL_QUERIES, GROUND_TRUTH
    queries, gt = ALL_QUERIES[:80], GROUND_TRUTH[:80]
    tok_cache = {}

    # FASE TEMPRANA (80 queries, con aprendizaje y recall)
    print("\n--- Fase temprana corregida (80 queries) ---")
    early_results = []
    e_ok = e_rej = 0
    for i, (query, truth) in enumerate(zip(queries, gt)):
        res = process_query_early(query, agents, tme, nlp, vectors, tok_cache)
        res["query"], res["truth"] = query, truth
        early_results.append(res)
        if res["rejected"]:
            e_rej += 1
        elif res["winner"] == truth:
            e_ok += 1
        if (i + 1) % 20 == 0:
            print(f"  {i+1}/80 procesadas  "
                  f"(acc parcial {e_ok/(i+1)*100:.1f}%)")
    early_acc = e_ok / len(queries)
    early_rej = e_rej / len(queries)
    counts = tme.mem_dir_L.agent_counts
    print(f"\n  Early accuracy: {early_acc*100:.1f}%   "
          f"rechazo: {early_rej*100:.1f}%")
    print(f"  M_dir counts (TME): {counts.tolist()}   "
          f"entropía: {tme.mem_dir_L.entropy():.3f} bits")

    # FASE MADURA (TME apagado, entrada aleatoria, B1)
    print("\n--- Fase madura (punto a punto, B1) ---")
    rng = np.random.RandomState(42)
    m_ok = m_rej = fid = 0
    m_ok_raw = 0
    mature_log = []
    for res in early_results:
        if not res["tokens"]:
            m_rej += 1
            # Las consultas sin tokens se rechazan, pero deben quedar en el CSV
            # como REJ: omitirlas dejaba 78 de 80 filas y daba la falsa
            # impresion de un desempeno perfecto sobre el denominador completo.
            mature_log.append({
                "query": res["query"], "truth": res["truth"],
                "early": res["winner"] or "REJ",
                "entry": "NA", "mature_b1": "REJ", "mature_raw": "REJ",
            })
            continue
        entry_cls = CLASSES[rng.randint(0, len(CLASSES))]
        dest = route_mature(res["tokens"], agents[entry_cls], tok_cache, b1=True)
        dest_raw = route_mature(res["tokens"], agents[entry_cls], tok_cache,
                                b1=False)
        if dest is None:
            m_rej += 1
        else:
            if dest == res["truth"]:
                m_ok += 1
            if dest == res["winner"]:
                fid += 1
        if dest_raw is not None and dest_raw == res["truth"]:
            m_ok_raw += 1
        mature_log.append({
            "query": res["query"], "truth": res["truth"],
            "early": res["winner"] or "REJ",
            "entry": entry_cls, "mature_b1": dest or "REJ",
            "mature_raw": dest_raw or "REJ",
        })
    n = len(queries)
    mature_acc, mature_raw_acc = m_ok / n, m_ok_raw / n
    fidelity = fid / n
    print(f"  Mature accuracy (B1):  {mature_acc*100:.1f}%")
    print(f"  Mature accuracy (RAW): {mature_raw_acc*100:.1f}%")
    print(f"  Fidelidad (madura == temprana): {fidelity*100:.1f}%")

    # Réplica del protocolo original: 10 TEST_QUERIES
    print("\n--- Réplica 10 TEST_QUERIES (protocolo exacto del exp. 1) ---")
    with contextlib.redirect_stdout(io.StringIO()):
        agents10 = {}
        for cls in CLASSES:
            mem_H, mem_L, mem_R = load_agent_memories(cls)
            agents10[cls] = Agent(cls, mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)
        tme10 = TME()
    tq_winners = []
    for query in TEST_QUERIES:
        res = process_query_early(query, agents10, tme10, nlp, vectors,
                                  tok_cache, do_recall=False)
        tq_winners.append((query, res["winner"]))
        print(f"  '{query}' -> {res['winner']}")
    counts10 = tme10.mem_dir_L.agent_counts
    print(f"  M_dir counts exp3: {counts10.tolist()}  "
          f"(exp1 fue [7, 4, 2] — sesgo apple)")

    # Guardar M_dir entrenado (pequeño, para la app)
    mdir_state = {
        "tme_dir_L": tme.mem_dir_L, "tme_dir_R": tme.mem_dir_R,
        "agent_dirs": {cls: agents[cls].mem_dir for cls in CLASSES},
    }
    with open(OUT_DIR / "exp3_mdir_state.pkl", "wb") as f:
        pickle.dump(mdir_state, f)

    # CSV por query
    with open(OUT_DIR / "results_per_query.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(mature_log[0].keys()))
        w.writeheader(); w.writerows(mature_log)

    # Summary JSON
    summary = {
        "early_acc": round(early_acc, 4), "early_rej": round(early_rej, 4),
        "mature_acc_b1": round(mature_acc, 4),
        "mature_acc_raw": round(mature_raw_acc, 4),
        "fidelity": round(fidelity, 4),
        "mdir_counts_tme": counts.tolist(),
        "mdir_entropy_bits": round(tme.mem_dir_L.entropy(), 4),
        "test_queries_counts": counts10.tolist(),
        "exp1_reference": {
            "_nota": "Exp. 1 ORIGINAL (llenado promediado, score crudo sin "
                     "gate). Ancla histórica, NO es la condición A del ablation "
                     "actual (que usa el directorio hetero).",
            "early_acc_raw": "~34% (Exp. 1 original)",
            "mature_acc_raw": 0.338, "mature_acc_b1": 0.988,
            "test_queries_counts": [7, 4, 2],
        },
    }
    (OUT_DIR / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")

    # Figuras
    # 1) comparativa exp1 vs exp3
    fig, ax = plt.subplots(figsize=(8.4, 5))
    labels = ["Early acc.", "Mature acc. (B1)", "Fidelidad"]
    exp1_v = [0.34, 0.988, 1.00]
    exp3_v = [early_acc, mature_acc, fidelity]
    x = np.arange(len(labels)); wdt = 0.36
    b1 = ax.bar(x - wdt/2, exp1_v, wdt, label="Exp. 1 (scores crudos)",
                color="#95a5a6")
    b2 = ax.bar(x + wdt/2, exp3_v, wdt,
                label="Exp. 3 (gate η + B1)", color="#1D9E75")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.015,
                    f"{b.get_height()*100:.0f}%", ha="center", fontsize=10)
    ax.set_xticks(x, labels); ax.set_ylim(0, 1.12)
    ax.set_title("Exp. 3 — routing corregido vs exp. 1 (banco de 80 queries)")
    ax.legend(); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(OUT_DIR / "fig1_exp1_vs_exp3.png", dpi=150)
    plt.close(fig)

    # 2) counts M_dir exp1 vs exp3 (sesgo de registro)
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    x = np.arange(len(CLASSES))
    exp1_c = np.array([81, 52, 31]); exp1_c = exp1_c / exp1_c.sum()
    exp3_c = counts / max(counts.sum(), 1)
    ax.bar(x - 0.18, exp1_c, 0.36, label="Exp. 1-estilo (crudo, exp2 downstream)",
           color="#95a5a6")
    ax.bar(x + 0.18, exp3_c, 0.36, label="Exp. 3 (corregido)",
           color=[DOMAIN_COLOR[c] for c in CLASSES])
    ax.axhline(1/3, ls=":", c="k", lw=1, label="ideal (1/3)")
    ax.set_xticks(x, CLASSES)
    ax.set_ylabel("proporción de registros M_dir")
    ax.set_title("Distribución de registros en M_dir — el sesgo de captura")
    ax.legend(); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(OUT_DIR / "fig2_mdir_counts.png", dpi=150)
    plt.close(fig)

    # Reporte
    rep = [
        "# Experimento 3 — protocolo completo con routing corregido",
        "",
        "## Configuración",
        "- Fase temprana: gate de containment (η), activación media de celdas "
        "no nulas (sin ÷mem.mean)",
        "- Aprendizaje: los 4 componentes registran (TME + 3 agentes), "
        "learn_latent en M_dir_R",
        "- Fase madura: TME apagado, entrada aleatoria (seed 42), M_dir con B1",
        "- Arquitectura 4-AMR completa con DirectoryMemory (EHAM real)",
        "- ι=κ=ξ=0, σ=0.1 · M_dom de stage5 sin modificar",
        "",
        "## Resultados (banco de 80 queries, GT 27/27/26)",
        "",
        "| métrica | exp. 1 (crudo) | exp. 3 (corregido) |",
        "|---|---|---|",
        f"| early accuracy | ~34% | **{early_acc:.1%}** |",
        f"| early rechazo | — | {early_rej:.1%} |",
        f"| mature accuracy B1 | 98.8% (ablation B1) | **{mature_acc:.1%}** |",
        f"| mature accuracy RAW | 33.8% | {mature_raw_acc:.1%} |",
        f"| fidelidad | 100% (sobre routing sesgado) | **{fidelity:.1%}** "
        "(sobre routing correcto) |",
        f"| M_dir counts | [81, 52, 31] estilo-crudo | {counts.tolist()} |",
        f"| M_dir entropía | — | {tme.mem_dir_L.entropy():.3f} bits "
        "(máx 1.585) |",
        "",
        "## Réplica de las 10 TEST_QUERIES del exp. 1",
        "",
        f"- counts exp. 1: [7, 4, 2] (apple capturó vehicle, engine, red…)",
        f"- counts exp. 3: {counts10.tolist()}",
        "",
        "| query | winner exp. 3 |",
        "|---|---|",
    ]
    for q, w_ in tq_winners:
        rep.append(f"| {q} | {w_} |")
    rep += [
        "",
        "## Archivos",
        "- summary.json · results_per_query.csv · exp3_mdir_state.pkl",
        "- fig1_exp1_vs_exp3.png · fig2_mdir_counts.png",
    ]
    (OUT_DIR / "report.md").write_text("\n".join(rep), encoding="utf-8")
    print(f"\nSalidas -> {OUT_DIR}")
    print("EXPERIMENTO 3 COMPLETADO.")


if __name__ == "__main__":
    main()
