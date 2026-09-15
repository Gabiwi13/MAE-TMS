"""
Sonda de la pista de identidad (fase 1 de la revisión).

Compara, coordenada por coordenada, la columna de la que muestrea el recall
inverso bajo tres pistas de identidad para el agente k:
  one_hot   1 en k y 0 explícito en los demás (lo que hacía _identity_cue)
  nan       1 en k y nan (indefinido) en los demás
  propia    la distribución de valores que k registró como ganador,
            rel[:, k, :, 1] normalizada por coordenada (referencia)

Reporta la distancia de variación total media entre columnas y qué fracción
de la masa de la columna one_hot proviene de registros ganados por agentes
distintos de k. Escribe results/experimento8/sonda_pista_identidad.json.
"""
import contextlib
import io
import json
import pickle
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from stage6_interaction import CLASSES, AGENT_LIST, MODELS_DIR, M_LABEL, Q_LATENT

K = len(AGENT_LIST)
OUT = ROOT / "results" / "experimento8" / "sonda_pista_identidad.json"


def column(ham, cue):
    with contextlib.redirect_stdout(io.StringIO()):
        proj = ham.project(ham.validate(np.asarray(cue, dtype=float), 1),
                           np.ones(K, dtype=float), 1)
    return np.asarray(proj, dtype=float)


def normalize_rows(M):
    s = M.sum(axis=1, keepdims=True)
    return np.where(s > 0, M / np.where(s == 0, 1, s), 0.0)


def tvd_rows(P, Q):
    """Distancia de variación total por coordenada, media sobre coordenadas
    con soporte."""
    live = (P.sum(axis=1) > 0) & (Q.sum(axis=1) > 0)
    return float((0.5 * np.abs(P[live] - Q[live]).sum(axis=1)).mean())


def analyze(mdir, m, tag):
    ham = mdir._ham
    rel = np.asarray(ham._full_iota_relation)
    n_all = rel[:, :, :m, 1].sum(axis=1)             # registros por (i, v), cualquier ganador
    out = {}
    for k in range(K):
        one_hot = np.zeros(K); one_hot[k] = 1.0
        nan_cue = np.full(K, np.nan); nan_cue[k] = 1.0
        col_oh = column(ham, one_hot)[:, :m]
        col_nan = column(ham, nan_cue)[:, :m]
        own = rel[:, k, :m, 1].astype(float)
        support = col_oh > 0
        # masa por origen dentro del soporte de k: los registros ganados por k
        # aparecen en su cara positiva y en las 7 caras negativas ajenas (8 N_k);
        # los ganados por otro m aparecen en 6 caras negativas (6 (N_all - N_k))
        n_k = own
        mass_k = 8.0 * n_k[support]
        mass_others = 6.0 * (n_all[support] - n_k[support])
        col_theory = np.where(support, 6.0 * n_all + 2.0 * n_k, 0.0)
        P_oh, P_nan, P_own = normalize_rows(col_oh), normalize_rows(col_nan), normalize_rows(own)
        out[AGENT_LIST[k]] = {
            "coincide_6Nall_2Nk": bool(np.allclose(col_oh, col_theory)),
            "nan_igual_a_propia": bool(np.allclose(col_nan, own)),
            "mismo_soporte": bool(np.array_equal(col_oh > 0, col_nan > 0)),
            "niveles_vivos_one_hot": float((col_oh > 0).sum(axis=1).mean()),
            "niveles_vivos_nan": float((col_nan > 0).sum(axis=1).mean()),
            "tvd_one_hot_vs_propia": tvd_rows(P_oh, P_own),
            "tvd_nan_vs_propia": tvd_rows(P_nan, P_own),
            "fraccion_masa_de_otros_agentes": float(mass_others.sum() / (mass_k.sum() + mass_others.sum())),
        }
    agg = {key: float(np.mean([v[key] for v in out.values()]))
           for key in ("niveles_vivos_one_hot", "niveles_vivos_nan",
                       "tvd_one_hot_vs_propia", "tvd_nan_vs_propia",
                       "fraccion_masa_de_otros_agentes")}
    agg["coincide_6Nall_2Nk_todos"] = all(v["coincide_6Nall_2Nk"] for v in out.values())
    agg["nan_igual_a_propia_todos"] = all(v["nan_igual_a_propia"] for v in out.values())
    agg["mismo_soporte_todos"] = all(v["mismo_soporte"] for v in out.values())
    print(f"[{tag}] " + "  ".join(f"{k}={v:.3f}" if isinstance(v, float) else f"{k}={v}"
                                   for k, v in agg.items()))
    return {"por_agente": out, "resumen": agg}


def main():
    with open(MODELS_DIR / "agent_car.pkl", "rb") as f:
        car = pickle.load(f)
    res = {"vision_64x32": analyze(car.mem_dir_R, Q_LATENT, "vision"),
           "texto_300x16": analyze(car.mem_dir, M_LABEL, "texto"),
           "modelos": "directorios de car (identicos entre agentes en v4)"}
    OUT.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
