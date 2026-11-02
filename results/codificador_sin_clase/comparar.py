"""Compara el codificador sin pérdida de clase contra el oficial (solo lectura de la copia oficial).

Uso: python comparar.py  ->  comparacion.json y la tabla en markdown por la salida estándar.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).parent
OFI = Path(r"C:\Users\aq99l\Projects\MAE-TMS-una-hetero")
LOGS = {
    "oficial": {"stage6": OFI / "logs_comparacion" / "stage6_interaction.log",
                "stage7": OFI / "results" / "hemisferio_visual" / "stage7_bidirectional.log",
                "stage8": OFI / "logs_comparacion" / "stage8_mature.log",
                "fase_b": AQUI / "filas_fase_b_oficial.json",
                "exp16": OFI / "results" / "experimento16"},
    "sin_clase": {"stage6": AQUI / "stage6_interaction.log",
                  "stage7": AQUI / "stage7_bidirectional.log",
                  "stage8": AQUI / "stage8_mature.log",
                  "fase_b": AQUI / "filas_fase_b_sinclase.json",
                  "exp16": AQUI / "exp16"},
}


def leer(p):
    b = Path(p).read_bytes()
    if b[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return b.decode("utf-16")
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("cp1252")


def stage7(p):
    t = leer(p)
    a = re.search(r"Fase A: (\d+) imagenes · routing visual ([\d.]+)% · rechazo ([\d.]+)% · "
                  r"sin energía \(antes de la memoria\) (\d+)", t)
    b = re.search(r"Routing test: (\d+)/(\d+) = ([\d.]+)%\s+\(rechazo ([\d.]+)%, de las cuales (\d+) sin energía", t)
    e = re.search(r"Evocacion top-3 domain-hit: (\d+)/(\d+)", t)
    return {"tau": float(re.search(r"Umbral de energía del latente: ([\d.]+)", t).group(1)),
            "fase_a_n": int(a.group(1)), "fase_a_acierto_pct": float(a.group(2)),
            "fase_a_rechazo_pct": float(a.group(3)), "fase_a_sin_energia": int(a.group(4)),
            "tme_entropia": float(re.search(r"entropia ([\d.]+) bits", t).group(1)),
            "dir_entropias": {m.group(1): float(m.group(2))
                              for m in re.finditer(r"\[Dir (\w+) visual\] counts=\[[^\]]*\] entropy=([\d.]+)", t)},
            "test_ok": int(b.group(1)), "test_n": int(b.group(2)), "test_pct": float(b.group(3)),
            "test_rechazo_pct": float(b.group(4)), "test_sin_energia": int(b.group(5)),
            "evocacion_log": [int(e.group(1)), int(e.group(2))]}


def stage6(p):
    return re.findall(r"ubicacion=(\w+)", leer(p))


def stage8(p):
    t = leer(p)
    f = re.search(r"Fidelidad: (\d+)/(\d+)", t)
    return {"fidelidad": [int(f.group(1)), int(f.group(2))],
            "pares": re.findall(r"Q\d+: temprana=(\w+)\s+madura=(\w+)", t)}


def exp16(d):
    s = json.loads((d / "resumen.json").read_text(encoding="utf-8"))
    falsos = {"nuevo": 0, "conocido": 0}
    n = {"nuevo": 0, "conocido": 0}
    for f in sorted((d / "raw").glob("pliegue_*.json")):
        for r in json.loads(f.read_text(encoding="utf-8"))["filas"]:
            n[r["banco"]] += 1
            falsos[r["banco"]] += int(r["falso_ruteo"])
    return {"pliegues": s["pliegues"], "bancos": s["bancos"], "brecha": s["brecha"],
            "formacion": s["formacion"], "falsos_pares_nuevo": s["falsos"],
            "falsos": falsos, "n": n, "por_clase": s["por_clase"]}


res = {}
for k, L in LOGS.items():
    fb = json.loads(Path(L["fase_b"]).read_text(encoding="utf-8"))["resumen"]
    res[k] = {"stage6_ganadores": stage6(L["stage6"]), "stage7": stage7(L["stage7"]),
              "stage8": stage8(L["stage8"]), "fase_b": fb, "exp16": exp16(L["exp16"])}
(AQUI / "comparacion.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

o, s = res["oficial"], res["sin_clase"]


def pct(v):
    return f"{100 * v[0]:.1f} [{100 * v[1]:.1f}, {100 * v[2]:.1f}]"


def ev(fb):
    e = fb["evocacion"]
    return f"{e['hits'][0]}/{e['denominador']} = {e['media_pct']:.1f} %"


def ev_partida(k):
    filas = json.loads(Path(LOGS[k]["fase_b"]).read_text(encoding="utf-8"))["filas"]
    rs = [r for r in filas if r["evoca"]]
    bien = [r for r in rs if r["destino"] == r["clase"]]
    mal = [r for r in rs if r["destino"] != r["clase"]]
    h = lambda xs: sum(r["evocacion"][0]["hit"] for r in xs)  # noqa: E731
    return f"{h(bien)}/{len(bien)} bien ruteadas · {h(mal)}/{len(mal)} mal ruteadas"


filas = [
    ("τ (umbral de energía)", f"{o['stage7']['tau']:.2f}", f"{s['stage7']['tau']:.2f}"),
    ("fase A, acierto al formar directorios", f"{o['stage7']['fase_a_acierto_pct']:.1f} %",
     f"{s['stage7']['fase_a_acierto_pct']:.1f} %"),
    ("fase A, rechazo / sin energía", f"{o['stage7']['fase_a_rechazo_pct']:.1f} % / {o['stage7']['fase_a_sin_energia']}",
     f"{s['stage7']['fase_a_rechazo_pct']:.1f} % / {s['stage7']['fase_a_sin_energia']}"),
    ("entropía de los directorios visuales (bits)",
     f"{min(o['stage7']['dir_entropias'].values()):.2f}–{max(o['stage7']['dir_entropias'].values()):.2f}",
     f"{min(s['stage7']['dir_entropias'].values()):.2f}–{max(s['stage7']['dir_entropias'].values()):.2f}"),
    ("ruteo de test (656)", f"{o['fase_b']['ruteo_ok']}/656 = {o['fase_b']['ruteo_pct']:.1f} %",
     f"{s['fase_b']['ruteo_ok']}/656 = {s['fase_b']['ruteo_pct']:.1f} %"),
    ("falsos ruteos de test", f"{o['fase_b']['falsos']} ({100 * o['fase_b']['falsos'] / 656:.1f} %)",
     f"{s['fase_b']['falsos']} ({100 * s['fase_b']['falsos'] / 656:.1f} %)"),
    ("rechazo de test (de ellas sin energía)", f"{o['fase_b']['rechazo']} = {o['fase_b']['rechazo_pct']:.1f} % ({o['fase_b']['sin_energia']})",
     f"{s['fase_b']['rechazo']} = {s['fase_b']['rechazo_pct']:.1f} % ({s['fase_b']['sin_energia']})"),
    ("evocación top-3, log de la etapa 7", "{}/{}".format(*o['stage7']['evocacion_log']),
     "{}/{}".format(*s['stage7']['evocacion_log'])),
    ("evocación top-3, semilla 0 (eval_fase_b.py)", ev(o["fase_b"]), ev(s["fase_b"])),
    ("evocación, semilla 0, según el ruteo", ev_partida("oficial"), ev_partida("sin_clase")),
    ("etapa 6, ganadores iguales al oficial", "16/16",
     f"{sum(a == b for a, b in zip(o['stage6_ganadores'], s['stage6_ganadores']))}/{len(o['stage6_ganadores'])}"),
    ("etapa 8, fidelidad", "{}/{}".format(*o["stage8"]["fidelidad"]), "{}/{}".format(*s["stage8"]["fidelidad"])),
]
for banco in ("conocido", "nuevo"):
    for m, nom in (("e2e", "punta a punta"), ("dir_acepta", "directorio acepta"),
                   ("contenido_acepta", "contenido acepta"), ("falso_ruteo", "falso ruteo")):
        filas.append((f"exp16, objeto {banco}, {nom}", pct(o["exp16"]["bancos"][banco][m]),
                      pct(s["exp16"]["bancos"][banco][m])))
    filas.append((f"exp16, objeto {banco}, falsos (de {o['exp16']['n'][banco]})",
                  str(o["exp16"]["falsos"][banco]), str(s["exp16"]["falsos"][banco])))
filas.append(("exp16, brecha e2e conocido − nuevo (puntos)", pct(o["exp16"]["brecha"]["e2e"]),
              pct(s["exp16"]["brecha"]["e2e"])))

print("| medida | oficial (MSE + 0.1·CE) | sin pérdida de clase |\n|---|---|---|")
for f in filas:
    print(f"| {f[0]} | {f[1]} | {f[2]} |")
print("\nFalsos de test, sin clase:", s["fase_b"]["falsos_pares"])
print("Falsos de test, oficial:", o["fase_b"]["falsos_pares"])
print("exp16 falsos en objeto nuevo, sin clase:", s["exp16"]["falsos_pares_nuevo"])
print("Ruteo de test por clase (ok/rechazo de 82), oficial -> sin clase:")
for c in o["fase_b"]["por_clase"]:
    a, b = o["fase_b"]["por_clase"][c], s["fase_b"]["por_clase"][c]
    print(f"  {c}: {a['ok']}/{a['rechazo']} -> {b['ok']}/{b['rechazo']}")
print("Etapa 6, ganadores:", list(zip(o["stage6_ganadores"], s["stage6_ganadores"])))
