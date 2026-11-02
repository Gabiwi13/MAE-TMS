"""
Efecto del rescate léxico de tokenize_query sobre la fase temprana, con el
sistema actual. Sin la regla, un token entra solo si spaCy lo etiqueta NOUN,
ADJ o PROPN en contexto. Se compara el ganador temprano de las consultas del
banco con y sin la regla. Solo lee models/.
"""
import contextlib
import io
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import stage6_interaction as s6
from eval_bank import ALL_QUERIES, GROUND_TRUTH
from quantizer import quantize_binary
from stage5_fill import load_agent_memories

OUT = ROOT / "results" / "rescate_lexico"


def tokens_sin_rescate(query, nlp):
    """tokenize_query sin sus dos vías de rescate."""
    out, seen = [], set()
    for tok in nlp(query.lower()):
        if tok.is_stop or not tok.is_alpha or tok.pos_ not in s6.ACCEPTED_POS:
            continue
        if tok.lemma_ not in seen:
            seen.add(tok.lemma_)
            out.append(tok.lemma_)
    return out


def token_scores(tok, agents, vectors, cache):
    """Puntaje de cada módulo para un token; None si no tiene vector."""
    if tok not in cache:
        v = s6.get_fasttext_vector(tok, vectors, allow_fallback=False)
        if v is None:
            cache[tok] = None
        else:
            v_q = quantize_binary(np.asarray(v, dtype=np.float32), s6.M_LABEL)
            cache[tok] = np.array([agents[c].recognize_gated(v_q) for c in s6.CLASSES])
    return cache[tok]


def winner(tokens, agents, vectors, cache):
    """Ganador temprano como en run_experiment3.process_query_early."""
    total = np.zeros(len(s6.CLASSES))
    for tok in tokens:
        sc = token_scores(tok, agents, vectors, cache)
        if sc is not None:
            total += sc
    if total.max() == 0.0:
        return None
    return s6.CLASSES[int(np.argmax(total))]


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        agents = {c: s6.Agent(c, load_agent_memories(c)) for c in s6.CLASSES}
        nlp = s6.get_nlp()
        vectors = s6.load_all_vectors(nlp)
    rows = []
    for q in ALL_QUERIES:
        rows.append({"consulta": q, "con": s6.tokenize_query(q, nlp),
                     "sin": tokens_sin_rescate(q, nlp)})
    with contextlib.redirect_stdout(io.StringIO()):
        s6.prevectorize(vectors, {t for r in rows for t in r["con"] + r["sin"]},
                        allow_fallback=False)

    cache = {}
    for r, truth in zip(rows, GROUND_TRUTH):
        r["verdad"] = truth
        r["rescatados"] = [t for t in r["con"] if t not in r["sin"]]
        r["solo_agrega"] = all(t in r["con"] for t in r["sin"])
        r["ganador_con"] = winner(r["con"], agents, vectors, cache)
        r["ganador_sin"] = winner(r["sin"], agents, vectors, cache)

    def acc(rs, key):
        return sum(r[key] == r["verdad"] for r in rs)

    afectadas = [r for r in rows if r["con"] != r["sin"]]
    cambian = [r for r in afectadas if r["ganador_con"] != r["ganador_sin"]]
    direccion = Counter(
        "hacia la verdad" if r["ganador_con"] == r["verdad"]
        else "desde la verdad" if r["ganador_sin"] == r["verdad"]
        else "entre errores" for r in cambian)
    res = {
        "consultas": len(rows),
        "la_regla_solo_agrega_tokens": sum(r["solo_agrega"] for r in rows),
        "afectadas": len(afectadas),
        "aciertos_afectadas_con": acc(afectadas, "ganador_con"),
        "aciertos_afectadas_sin": acc(afectadas, "ganador_sin"),
        "rechazos_afectadas_con": sum(r["ganador_con"] is None for r in afectadas),
        "rechazos_afectadas_sin": sum(r["ganador_sin"] is None for r in afectadas),
        "aciertos_banco_con": acc(rows, "ganador_con"),
        "aciertos_banco_sin": acc(rows, "ganador_sin"),
        "cambios_de_ganador": len(cambian),
        "direccion_de_los_cambios": dict(direccion),
        "tokens_rescatados_mas_frecuentes": Counter(
            t for r in afectadas for t in r["rescatados"]).most_common(15),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "resumen.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "filas.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
