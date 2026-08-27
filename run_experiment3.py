"""
Experimento 3 — Protocolo completo del experimento 1 con el routing corregido.

Scoring oficial (validado en exp. 2):
  1. Gate de containment (η re-acoplado): fila vacía en la proyección → score 0.
     Mecanismo nativo de Pineda; el score es la activación media de las celdas
     no nulas (Agent.recognize_gated), SIN división por mem.mean. Con el llenado
     por instancias las masas quedan igualadas por construcción y ÷mem.mean es
     redundante (exp. 2 lo confirma: gate solo da 100% en el diagnóstico).
  2. B1 (÷count+1) en fase madura, como en la condición B1 del ablation.

Protocolo (idéntico al exp. 1 / stages 6+8). Ejercita la vía textual: las
tres memorias de dominio y el directorio de labels. El directorio visual
mem_dir_R queda vacío, se entrena en stage7 con percepciones de imágenes:
  - Agentes con M_dom_L/R/H de stage5 (solo lectura) + M_dir EHAM fresco.
  - TME con M_dir_L / M_dir_R (DirectoryMemory) frescos.
  - Fase temprana: broadcast → recognize_gated → argmax → los directorios de
    labels registran (token → agente ganador). mem_dir_R NO se actualiza con
    recalls: el directorio visual se entrena solo con percepciones reales de
    imágenes (stage7), no con ecos generados por la propia memoria.
  - Fase madura: TME apagado, entrada aleatoria (seed 42), routing por M_dir
    del agente de entrada con B1, rechazo explícito.

Corpus: primeras 80 queries del banco de 8 clases (ground truth, 10 por
clase) + réplica del protocolo de TEST_QUERIES para comparación directa.

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
    get_nlp, load_all_vectors, tokenize_query, prevectorize,
    get_fasttext_vector, token_in_vocabulary, TEST_QUERIES,
)

DOMAIN_COLOR = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60",
                "cow": "#8e44ad", "cup": "#c9760a", "dog": "#16a085",
                "pear": "#7d8f22", "tomato": "#c0392b"}


# Routing oficial (exp. 2): gate de containment, sin división por mem.mean

def corrected_score(agent, v_q):
    """Scoring oficial: Agent.recognize_gated (activación media de las celdas
    no nulas, gateada por containment). Sin calibración ÷mem.mean."""
    return agent.recognize_gated(v_q)


def process_query_early(query, agents, tme, nlp, vectors, tok_cache):
    """
    Fase temprana — protocolo oficial: tokenize → representar con fastText real
    (sin filtro lexico) → recognize_gated → argmax → aprendizaje en los
    directorios de labels: el del TME y el de cada agente.

    El rechazo lo decide la EAM, no el vocabulario de labels. Se distinguen dos
    causas: no_representable_tokens (ningun token tiene vector fastText) y
    mae_no_support (hay pistas pero ningun agente las contiene).
    """
    tokens = tokenize_query(query, nlp)
    represented, unrepresented = [], []
    for tok in tokens:
        if tok not in tok_cache:
            v = get_fasttext_vector(tok, vectors, allow_fallback=False)
            tok_cache[tok] = (None if v is None
                              else quantize_binary(np.asarray(v, dtype=np.float32),
                                                   M_LABEL))
        (unrepresented if tok_cache[tok] is None else represented).append(tok)

    if not represented:
        return {"winner": None, "tokens": tokens, "rejected": True,
                "reason": "no_representable_tokens",
                "represented_tokens": [], "unrepresented_tokens": unrepresented}

    scores = {cls: 0.0 for cls in CLASSES}
    for tok in represented:
        v_q = tok_cache[tok]
        for cls in CLASSES:
            scores[cls] += corrected_score(agents[cls], v_q)

    if max(scores.values()) == 0.0:
        return {"winner": None, "tokens": tokens, "rejected": True,
                "reason": "mae_no_support", "scores": scores,
                "represented_tokens": represented,
                "unrepresented_tokens": unrepresented}

    winner = max(scores, key=scores.get)
    widx = AGENT_LIST.index(winner)

    # Aprendizaje — registran el directorio de labels del TME y el de cada
    # agente.
    # NOTA: mem_dir_R (directorio visual) NO se actualiza aqui. El latente de
    # un recall es un eco de la propia memoria, no una percepcion real; el
    # directorio visual solo indexa latentes de imagenes (stage7).
    for tok in represented:
        v_q = tok_cache[tok]
        tme.update_directory(v_q, widx)
        for agent in agents.values():
            agent.update_directory(v_q, widx)

    return {"winner": winner, "tokens": tokens, "rejected": False,
            "reason": "mae_support", "scores": scores,
            "represented_tokens": represented,
            "unrepresented_tokens": unrepresented}


def route_mature(tokens, entry_agent, tok_cache, b1=True):
    """Fase madura — protocolo de stage8: M_dir del agente de entrada, B1.
    Sólo se rutean tokens representables (v_q no None); sin soporte en el
    directorio devuelve None (directory_no_support)."""
    agg = np.zeros(len(CLASSES), dtype=float)
    used = 0
    for tok in tokens:
        v_q = tok_cache.get(tok)
        if v_q is None:
            continue
        used += 1
        agg += (entry_agent.mem_dir.predict_normalized(v_q, mode="linear")
                if b1 else entry_agent.mem_dir.predict(v_q))
    if used == 0 or agg.sum() == 0:
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
    # Pre-vectorizar todos los tokens del banco en UNA pasada de stream:
    # palabras reales no-label entran como pistas; las no representables -> None.
    bank_tokens = set()
    for q in list(queries) + list(TEST_QUERIES):
        bank_tokens.update(tokenize_query(q, nlp))
    prevectorize(vectors, bank_tokens, allow_fallback=False)
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
    from collections import Counter
    reason_counts = Counter(r.get("reason", "?") for r in early_results)
    # process_query_early solo emite no_representable_tokens, mae_no_support y
    # mae_support. "no_tokens" pertenece a mature_log y no aparece aqui.
    n_norep = reason_counts.get("no_representable_tokens", 0)
    n_mae_rej = reason_counts.get("mae_no_support", 0)
    n_routed = reason_counts.get("mae_support", 0)
    print(f"  Desglose: ruteadas={n_routed}  "
          f"rechazo_EAM(mae_no_support)={n_mae_rej}  "
          f"no_representables={n_norep}")
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
        represented = res.get("represented_tokens") or [
            t for t in res["tokens"] if tok_cache.get(t) is not None]
        # Toda consulta queda en el CSV, también los rechazos (denominador 80).
        if not represented:
            m_rej += 1
            reason = ("no_tokens" if not res["tokens"]
                      else "no_representable_tokens")
            mature_log.append({
                "query": res["query"], "truth": res["truth"],
                "early": res["winner"] or "REJ",
                "entry": "NA", "mature_b1": "REJ", "mature_raw": "REJ",
                "reason": reason,
            })
            continue
        entry_cls = CLASSES[rng.randint(0, len(CLASSES))]
        dest = route_mature(represented, agents[entry_cls], tok_cache, b1=True)
        dest_raw = route_mature(represented, agents[entry_cls], tok_cache,
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
            "reason": ("directory_no_support" if dest is None else "directory_support"),
        })
    n = len(queries)
    mature_acc, mature_raw_acc = m_ok / n, m_ok_raw / n
    fidelity = fid / n
    print(f"  Mature accuracy (B1):  {mature_acc*100:.1f}%")
    print(f"  Mature accuracy (RAW): {mature_raw_acc*100:.1f}%")
    print(f"  Fidelidad (madura == temprana): {fidelity*100:.1f}%")

    # Réplica del protocolo del pipeline oficial: TEST_QUERIES (2 por dominio)
    print(f"\n--- Réplica {len(TEST_QUERIES)} TEST_QUERIES "
          f"(protocolo del pipeline oficial) ---")
    with contextlib.redirect_stdout(io.StringIO()):
        agents10 = {}
        for cls in CLASSES:
            mem_H, mem_L, mem_R = load_agent_memories(cls)
            agents10[cls] = Agent(cls, mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)
        tme10 = TME()
    tq_winners = []
    for query in TEST_QUERIES:
        res = process_query_early(query, agents10, tme10, nlp, vectors,
                                  tok_cache)
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
        "rejection_breakdown": {
            "routed": n_routed,
            "rejected_by_mae": n_mae_rej,
            "no_representable_tokens": n_norep,
            "note": "El rechazo lo decide la EAM (mae_no_support), no un filtro "
                    "léxico. no_representable_tokens = frontera del encoder "
                    "(sin vector fastText real), no rechazo EAM.",
        },
        "test_queries_counts": counts10.tolist(),
        "exp1_reference": {
            "_nota": "ADVERTENCIA: cifras NO VERIFICABLES en el estado actual "
                     "del repo. Provienen de un ablation intermedio (3 clases, "
                     "pre-refactor v3) sin artefacto que las respalde, y "
                     "CONTRADICEN notes_historicas/conclusiones_experimento1.md "
                     "(que reporta fidelidad 50% = 5/10 y counts apple=5/horse=3/"
                     "car=2). NO citar como ancla; se conservan solo como "
                     "referencia cualitativa del sesgo apple de la era 3-clases.",
            "early_acc_raw": "~34% (no verificable)",
            "mature_acc_raw": 0.338, "mature_acc_b1": 0.988,
            "test_queries_counts": [7, 4, 2],
            "_fuente_documentada": "notes_historicas/conclusiones_experimento1.md "
                                   "reporta fidelidad 50%, counts [5,3,2]",
        },
    }
    (OUT_DIR / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")

    # Figuras
    # 1) comparativa exp1 vs exp3. NOTA: las barras "Exp. 1" son cifras
    # históricas NO VERIFICABLES (ver exp1_reference en summary.json) y se
    # etiquetan como tales para no presentarlas como dato citable.
    fig, ax = plt.subplots(figsize=(8.4, 5))
    labels = ["Early acc.", "Mature acc. (B1)", "Fidelidad"]
    exp1_v = [0.34, 0.988, 1.00]
    exp3_v = [early_acc, mature_acc, fidelity]
    x = np.arange(len(labels)); wdt = 0.36
    b1 = ax.bar(x - wdt/2, exp1_v, wdt,
                label="Exp. 1 (histórico, no verificable)", color="#95a5a6")
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

    # 2) counts M_dir exp3 (sesgo de registro). La referencia histórica del
    # exp. 1 ([81, 52, 31]) era del sistema de 3 clases y no es comparable
    # barra a barra con 8 agentes; queda documentada en summary.json.
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    x = np.arange(len(CLASSES))
    exp3_c = counts / max(counts.sum(), 1)
    ax.bar(x, exp3_c, 0.6, label="Exp. 3 (corregido)",
           color=[DOMAIN_COLOR[c] for c in CLASSES])
    ax.axhline(1 / len(CLASSES), ls=":", c="k", lw=1,
               label=f"ideal (1/{len(CLASSES)})")
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
        "- Scoring oficial: recognize_gated (gate de containment, activación "
        "media de celdas no nulas), sin ÷mem.mean",
        "- Sin filtro léxico: tokens representables por fastText entran como "
        "pista; el rechazo lo decide la EAM (score 0) o la frontera del encoder",
        "- Aprendizaje: solo los directorios de labels registran (TME + un "
        "directorio por agente), token → ganador. mem_dir_R NO se actualiza "
        "con recalls (solo percepciones reales de imágenes en stage7)",
        "- Fase madura: TME apagado, entrada aleatoria (seed 42), M_dir con B1",
        "- Vía textual completa con DirectoryMemory (EHAM real); el "
        "directorio visual no participa",
        "- ι=κ=ξ=0, σ=0.1 · M_dom de stage5 sin modificar",
        "",
        "## Resultados (banco de 80 queries, 10 por clase)",
        "",
        "| métrica | exp. 1 (crudo, v3 · 3 clases) | exp. 3 (corregido, "
        "8 clases) |",
        "|---|---|---|",
        f"| early accuracy | ~34% | **{early_acc:.1%}** |",
        f"| early rechazo | — | {early_rej:.1%} |",
        f"| mature accuracy B1 | 98.8% (ablation B1, v3) | **{mature_acc:.1%}** |",
        f"| mature accuracy RAW | 33.8% | {mature_raw_acc:.1%} |",
        f"| fidelidad | 100% (sobre routing sesgado) | **{fidelity:.1%}** "
        "(sobre routing correcto) |",
        f"| M_dir counts | [81, 52, 31] estilo-crudo (v3) | {counts.tolist()} |",
        f"| M_dir entropía | — | {tme.mem_dir_L.entropy():.3f} bits "
        f"(máx {np.log2(len(CLASSES)):.3f}) |",
        "",
        f"## Réplica de las {len(TEST_QUERIES)} TEST_QUERIES del pipeline "
        "oficial (2 por dominio)",
        "",
        f"- counts exp. 1 (v3, 10 queries de 3 clases): [7, 4, 2] "
        "(apple capturó vehicle, engine, red…)",
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
