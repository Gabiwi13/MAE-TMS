"""
Sonda de exp9: dónde vive la familiaridad si no vive en el recall.

Para cada consulta del banco con verdad k se mide:
  - si el especialista k la reconoce (recognize_gated > 0 en algún token),
  - si un no-especialista la reconoce con su propio contenido,
  - si el directorio (de cualquier agente, son idénticos) la rutea a k.
Escribe results/experimento9/sonda_reconocimiento.json.
"""
import contextlib, io, json, pickle, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from stage6_interaction import CLASSES, AGENT_LIST, MODELS_DIR, get_nlp, load_all_vectors
import run_experiment9_member_loss as E

K = len(CLASSES)
nlp = get_nlp(); vectors = load_all_vectors(nlp)
bank = E.load_bank(nlp, vectors)
agents = {c: E.load_agent(c) for c in CLASSES}
out = {"por_clase": {}, "total": {}}
tot = {"n": 0, "especialista_reconoce": 0, "no_especialista_reconoce": 0,
       "directorio_a_k": 0, "directorio_a_otro": 0, "directorio_rechaza": 0,
       "especialista_reconoce_y_directorio_no": 0}
for k, cls in enumerate(CLASSES):
    other = agents[CLASSES[(k + 1) % K]]
    row = dict.fromkeys(tot, 0)
    for it in bank:
        if it["tidx"] != k or not it["cues"]:
            continue
        row["n"] += 1
        with contextlib.redirect_stdout(io.StringIO()):
            spec = max(agents[cls].recognize_gated(v) for _, v in it["cues"]) > 0
            non = max(other.recognize_gated(v) for _, v in it["cues"]) > 0
            dest, _ = other.mem_dir.route_multi([v for _, v in it["cues"]], mode="linear")
        row["especialista_reconoce"] += spec
        row["no_especialista_reconoce"] += non
        row["directorio_a_k"] += dest == k
        row["directorio_a_otro"] += dest >= 0 and dest != k
        row["directorio_rechaza"] += dest < 0
        row["especialista_reconoce_y_directorio_no"] += spec and dest != k
    out["por_clase"][cls] = row
    for key in tot:
        tot[key] += row[key]
    print(cls, row, flush=True)
out["total"] = tot
out["tasas"] = {key: tot[key] / tot["n"] for key in tot if key != "n"}
print(json.dumps(out["tasas"], indent=2))
(ROOT / "results" / "experimento9" / "sonda_reconocimiento.json").write_text(
    json.dumps(out, indent=2, ensure_ascii=False))
