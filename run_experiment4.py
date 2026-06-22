"""
Experimento 4 — Curva de formación del directorio transactivo.

Pregunta: ¿cuántas interacciones necesita el grupo para que el directorio
(M_dir) sea confiable y el TME pueda apagarse? ¿La formación depende del
orden de llegada de las experiencias? ¿El sesgo de densidad (routing crudo)
retrasa o impide la convergencia?

Protocolo
---------
Fase temprana corregida (gate η + ÷mem.mean, exp. 3) sobre el banco de 80
queries. Tras CADA interacción k se congela el M_dir y se evalúa la fase
madura completa (80 queries, routing B1, rechazo explícito) → curvas de:
  - accuracy madura(k)        ¿ya puedo apagar el TME?
  - tasa de rechazo(k)        cobertura del vocabulario aprendido
  - entropía del M_dir(k)     balance de la especialización
  - counts por agente(k)      dinámica de captura

Condiciones
-----------
  A  corregido · orden original (intercalado apple/horse/car)
  B  corregido · 5 órdenes barajados (media ± desv.)
  C  corregido · orden bloqueado (27 apple, luego 27 horse, luego 26 car)
  D  crudo (exp. 1: sin gate, sin norm) · orden original — control del sesgo

Nota de instrumentación: en la arquitectura real los 4 M_dir (TME + 3
agentes) reciben registros idénticos; aquí se instrumenta uno solo
(DirectoryMemory, EHAM real) que representa ese estado compartido.
La fase temprana no hace recall (learn_latent llena M_dir_R, que no
participa del routing por labels medido aquí; validado en exp. 3).

Solo lectura de stage5; nada del exp. 1–3 se modifica.
Salidas en results/exp4_directory_formation/

Uso:  python run_experiment4.py
"""
import csv
import io
import json
import sys
import contextlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = ROOT / "results" / "exp4_directory_formation"
OUT_DIR.mkdir(parents=True, exist_ok=True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from quantizer import quantize_binary
from associative_memory import DirectoryMemory
from stage5_fill import load_agent_memories
from stage6_interaction import (
    Agent, CLASSES, AGENT_LIST, M_LABEL, N,
    get_nlp, load_all_vectors, tokenize_query, prevectorize,
    get_fasttext_vector, token_in_vocabulary,
)

DOMAIN_COLOR = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60"}
SHUFFLE_SEEDS = [0, 1, 2, 3, 4]
ACC_THRESHOLD = 0.90


# Scoring temprano: corregido (exp. 3) y crudo (exp. 1)

def corrected_score(agent, v_q, mem_mean):
    """Scoring oficial: Agent.recognize_gated (gate de containment)."""
    return agent.recognize_gated(v_q)


def raw_score(agent, v_q, mem_mean):
    """Estilo exp. 1: activación media sin gate y sin normalizar."""
    l_w = agent.mem_dom_L.recog_weights(v_q)
    mx = l_w.max()
    weights = (l_w / mx) if mx > 0 else np.ones(len(v_q), dtype=float)
    mem_H = agent.mem_dom_H
    ca = mem_H.validate(v_q, 0)
    with contextlib.redirect_stdout(io.StringIO()):
        proj = mem_H.project(ca, weights, 0)
    count = int(np.count_nonzero(proj))
    return float(np.sum(proj)) / count if count > 0 else 0.0


# Formación + evaluación

def prepare_bank(nlp, vectors):
    """Tokeniza el banco una sola vez. Sin filtro léxico: cada token se
    representa con fastText real (allow_fallback=False); los no representables
    se descartan como pista y la EAM decide el resto."""
    from eval_bank import ALL_QUERIES, GROUND_TRUTH
    qg = list(zip(ALL_QUERIES[:80], GROUND_TRUTH[:80]))
    all_tokens = set()
    for query, _ in qg:
        all_tokens.update(tokenize_query(query, nlp))
    prevectorize(vectors, all_tokens, allow_fallback=False)
    bank = []
    for query, truth in qg:
        tokens = tokenize_query(query, nlp)
        vqs, repr_toks = [], []
        for tok in tokens:
            v = get_fasttext_vector(tok, vectors, allow_fallback=False)
            if v is None:
                continue
            repr_toks.append(tok)
            vqs.append(quantize_binary(np.asarray(v, dtype=np.float32), M_LABEL))
        bank.append({"query": query, "truth": truth,
                     "tokens": repr_toks, "vqs": vqs})
    return bank


def eval_mature(mdir, bank):
    """Fase madura congelada: routing B1 sobre todo el banco."""
    ok = rej = 0
    for item in bank:
        if not item["vqs"]:
            rej += 1
            continue
        agg = np.zeros(len(CLASSES), dtype=float)
        for v_q in item["vqs"]:
            agg += mdir.predict_normalized(v_q, mode="linear")
        if agg.sum() == 0:
            rej += 1
            continue
        if CLASSES[int(np.argmax(agg))] == item["truth"]:
            ok += 1
    n = len(bank)
    return ok / n, rej / n


def run_formation(bank_order, agents, mem_means, score_fn, label=""):
    """
    Corre la fase temprana en el orden dado, registrando snapshot tras
    cada interacción. Devuelve dict de series (longitud = len(bank_order)).
    """
    with contextlib.redirect_stdout(io.StringIO()):
        mdir = DirectoryMemory(N, M_LABEL, len(CLASSES))
    series = {"k": [], "mature_acc": [], "mature_rej": [],
              "entropy": [], "counts": [], "early_winner_ok": []}
    e_ok = e_seen = 0
    for k, item in enumerate(bank_order, 1):
        winner = None
        if item["vqs"]:
            scores = {cls: 0.0 for cls in CLASSES}
            for v_q in item["vqs"]:
                for cls in CLASSES:
                    scores[cls] += score_fn(agents[cls], v_q, mem_means[cls])
            if sum(scores.values()) > 0:
                winner = max(scores, key=scores.get)
        if winner is not None:
            e_seen += 1
            e_ok += int(winner == item["truth"])
            widx = AGENT_LIST.index(winner)
            for v_q in item["vqs"]:
                with contextlib.redirect_stdout(io.StringIO()):
                    mdir.register(v_q, widx)
        acc, rej = eval_mature(mdir, bank_order)
        series["k"].append(k)
        series["mature_acc"].append(acc)
        series["mature_rej"].append(rej)
        series["entropy"].append(mdir.entropy())
        series["counts"].append(mdir.agent_counts.tolist())
        series["early_winner_ok"].append(e_ok / max(e_seen, 1))
        if k % 20 == 0:
            print(f"    [{label}] k={k:2d}  mature_acc={acc*100:5.1f}%  "
                  f"rej={rej*100:4.1f}%  H={mdir.entropy():.3f}")
    return series


def transition_k(series, thr=ACC_THRESHOLD):
    """Primer k con acc>=thr, y primer k sostenido (>=thr hasta el final)."""
    acc = series["mature_acc"]
    first = next((k for k, a in zip(series["k"], acc) if a >= thr), None)
    sustained = None
    for i in range(len(acc)):
        if all(a >= thr for a in acc[i:]):
            sustained = series["k"][i]
            break
    return first, sustained


# Main

def main():
    print("=" * 64)
    print("  EXPERIMENTO 4 — curva de formación del directorio")
    print("=" * 64)

    print("\nCargando M_dom de stage5 (solo lectura)...")
    agents = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for cls in CLASSES:
            mem_H, mem_L, mem_R = load_agent_memories(cls)
            agents[cls] = Agent(cls, mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)
    # mem.mean es constante (no registramos en M_dom) — cachear
    mem_means = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for cls in CLASSES:
            mem_means[cls] = float(agents[cls].mem_dom_H.mean)

    nlp = get_nlp()
    vectors = load_all_vectors(nlp)   # alias por lema: spaCy es parte del core
    print("Tokenizando banco de 80 queries (una sola vez)...")
    bank = prepare_bank(nlp, vectors)

    runs = {}   # name -> series

    print("\n--- A · corregido, orden original (intercalado) ---")
    runs["A_interleaved"] = run_formation(bank, agents, mem_means,
                                          corrected_score, "A")

    print("\n--- B · corregido, 5 órdenes barajados ---")
    for seed in SHUFFLE_SEEDS:
        order = list(bank)
        np.random.RandomState(seed).shuffle(order)
        runs[f"B_shuffle_{seed}"] = run_formation(order, agents, mem_means,
                                                  corrected_score,
                                                  f"B s{seed}")

    print("\n--- C · corregido, orden bloqueado por dominio ---")
    blocked = sorted(bank, key=lambda it: CLASSES.index(it["truth"]))
    runs["C_blocked"] = run_formation(blocked, agents, mem_means,
                                      corrected_score, "C")

    print("\n--- D · crudo (exp. 1), orden original — control ---")
    runs["D_raw"] = run_formation(bank, agents, mem_means, raw_score, "D")

    # Transiciones
    print(f"\nTransición (mature_acc ≥ {ACC_THRESHOLD:.0%}):")
    trans = {}
    for name, s in runs.items():
        first, sust = transition_k(s)
        trans[name] = {"first": first, "sustained": sust,
                       "final_acc": s["mature_acc"][-1],
                       "final_entropy": s["entropy"][-1],
                       "final_counts": s["counts"][-1]}
        print(f"  {name:<16} primer k={str(first):>4}  sostenido k="
              f"{str(sust):>4}  acc final={s['mature_acc'][-1]*100:5.1f}%  "
              f"counts={s['counts'][-1]}")

    # CSV largo
    with open(OUT_DIR / "results_formation.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["run", "k", "mature_acc", "mature_rej", "entropy",
                    "count_apple", "count_horse", "count_car",
                    "early_acc_running"])
        for name, s in runs.items():
            for i in range(len(s["k"])):
                c = s["counts"][i]
                w.writerow([name, s["k"][i],
                            round(s["mature_acc"][i], 4),
                            round(s["mature_rej"][i], 4),
                            round(s["entropy"][i], 4),
                            c[0], c[1], c[2],
                            round(s["early_winner_ok"][i], 4)])

    # Figuras
    ks = runs["A_interleaved"]["k"]
    B = np.array([runs[f"B_shuffle_{s}"]["mature_acc"]
                  for s in SHUFFLE_SEEDS])

    # fig1 — accuracy madura vs k
    fig, ax = plt.subplots(figsize=(9.6, 5.6))
    ax.fill_between(ks, B.min(axis=0), B.max(axis=0), alpha=0.18,
                    color="#1D9E75", label="B · barajados (rango, 5 seeds)")
    ax.plot(ks, B.mean(axis=0), color="#1D9E75", lw=2.2,
            label="B · barajados (media)")
    ax.plot(ks, runs["A_interleaved"]["mature_acc"], color="#534AB7", lw=2.2,
            label="A · intercalado")
    ax.plot(ks, runs["C_blocked"]["mature_acc"], color="#e67e22", lw=2.2,
            ls="--", label="C · bloqueado por dominio")
    ax.plot(ks, runs["D_raw"]["mature_acc"], color="#95a5a6", lw=2.2,
            ls=":", label="D · routing crudo (sesgo)")
    ax.axhline(ACC_THRESHOLD, color="k", lw=0.8, ls=":",
               label=f"umbral {ACC_THRESHOLD:.0%}")
    ax.set_xlabel("interacciones de fase temprana (k)")
    ax.set_ylabel("accuracy madura si el TME se apaga en k")
    ax.set_title("Formación del directorio — ¿cuándo puede apagarse el TME?")
    ax.set_ylim(0, 1.04); ax.legend(loc="lower right", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig1_formation_curve.png", dpi=150)
    plt.close(fig)

    # fig2 — entropía del M_dir vs k
    fig, ax = plt.subplots(figsize=(9.6, 5.0))
    Bh = np.array([runs[f"B_shuffle_{s}"]["entropy"] for s in SHUFFLE_SEEDS])
    ax.fill_between(ks, Bh.min(axis=0), Bh.max(axis=0), alpha=0.18,
                    color="#1D9E75")
    ax.plot(ks, Bh.mean(axis=0), color="#1D9E75", lw=2, label="B · barajados")
    ax.plot(ks, runs["A_interleaved"]["entropy"], color="#534AB7", lw=2,
            label="A · intercalado")
    ax.plot(ks, runs["C_blocked"]["entropy"], color="#e67e22", lw=2, ls="--",
            label="C · bloqueado")
    ax.plot(ks, runs["D_raw"]["entropy"], color="#95a5a6", lw=2, ls=":",
            label="D · crudo")
    ax.axhline(np.log2(3), color="k", lw=0.8, ls=":",
               label="máx (log₂3 = 1.585)")
    ax.set_xlabel("interacciones (k)"); ax.set_ylabel("entropía M_dir (bits)")
    ax.set_title("Balance del directorio durante la formación")
    ax.legend(fontsize=9); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig2_entropy_curve.png", dpi=150)
    plt.close(fig)

    # fig3 — rechazo (cobertura) vs k
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ax.plot(ks, runs["A_interleaved"]["mature_rej"], color="#534AB7", lw=2,
            label="A · intercalado")
    Br = np.array([runs[f"B_shuffle_{s}"]["mature_rej"]
                   for s in SHUFFLE_SEEDS])
    ax.plot(ks, Br.mean(axis=0), color="#1D9E75", lw=2, label="B · barajados")
    ax.plot(ks, runs["C_blocked"]["mature_rej"], color="#e67e22", lw=2,
            ls="--", label="C · bloqueado")
    ax.set_xlabel("interacciones (k)")
    ax.set_ylabel("tasa de rechazo madura")
    ax.set_title("Cobertura del vocabulario aprendido (rechazo ↓)")
    ax.legend(fontsize=9); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig3_rejection_curve.png", dpi=150)
    plt.close(fig)

    # fig4 — dinámica de counts (A)
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    Ca = np.array(runs["A_interleaved"]["counts"])
    ax.stackplot(ks, Ca.T, labels=CLASSES,
                 colors=[DOMAIN_COLOR[c] for c in CLASSES], alpha=0.85)
    ax.set_xlabel("interacciones (k)")
    ax.set_ylabel("registros acumulados en M_dir")
    ax.set_title("Dinámica de especialización (A · intercalado)")
    ax.legend(loc="upper left", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig4_counts_dynamics.png", dpi=150)
    plt.close(fig)

    # Reporte
    rep = [
        "# Experimento 4 — curva de formación del directorio transactivo",
        "",
        "## Pregunta",
        "¿Cuántas interacciones necesita el grupo para que el routing punto a",
        "punto sea confiable (el TME pueda apagarse)? ¿Importa el orden de las",
        "experiencias? ¿El sesgo de densidad impide la convergencia?",
        "",
        "## Transiciones (accuracy madura ≥ 90%)",
        "",
        "| condición | primer k | k sostenido | acc final | entropía final | counts |",
        "|---|---|---|---|---|---|",
    ]
    label_map = {
        "A_interleaved": "A · intercalado",
        **{f"B_shuffle_{s}": f"B · barajado s{s}" for s in SHUFFLE_SEEDS},
        "C_blocked": "C · bloqueado",
        "D_raw": "D · crudo (control sesgo)",
    }
    for name, t in trans.items():
        rep.append(
            f"| {label_map[name]} | {t['first']} | {t['sustained']} | "
            f"{t['final_acc']:.1%} | {t['final_entropy']:.3f} | "
            f"{t['final_counts']} |")
    rep += [
        "",
        "## Archivos",
        "- results_formation.csv (formato largo: run, k, métricas)",
        "- fig1_formation_curve.png — la figura central",
        "- fig2_entropy_curve.png · fig3_rejection_curve.png · "
        "fig4_counts_dynamics.png",
        "",
        "## Notas de instrumentación",
        "- M_dom de stage5 solo lectura; M_dir fresco por corrida "
        "(DirectoryMemory, EHAM real).",
        "- Los 4 M_dir de la arquitectura reciben registros idénticos; se "
        "instrumenta uno que representa el estado compartido.",
        "- Sin recall en temprana (M_dir_R no participa del routing por "
        "labels; pipeline completo validado en exp. 3).",
    ]
    (OUT_DIR / "report.md").write_text("\n".join(rep), encoding="utf-8")
    print(f"\nSalidas -> {OUT_DIR}")
    print("EXPERIMENTO 4 COMPLETADO.")


if __name__ == "__main__":
    main()
