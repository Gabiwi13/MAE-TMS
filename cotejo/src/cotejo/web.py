"""Muestra de oraciones para buscar a mano en la web, sin enviar capítulos completos."""
from __future__ import annotations

import math
from collections import Counter

from .texto import CITA_TEXTUAL, CODIGO, MATEMATICAS, normalizar, oraciones, palabras


def muestra(extr: dict, k: int, min_palabras: int = 12, max_palabras: int = 35) -> list[dict]:
    candidatas = []
    for s in extr["segmentos"]:
        if s["tipo"] not in ("prosa", "leyenda"):
            continue
        banderas = [b for _, _, b in s["palabras"]]
        pos = 0
        for a, b in oraciones(s["texto"]):
            t = s["texto"][a:b].strip()
            n = len(palabras(t))
            bs, pos = banderas[pos:pos + n], pos + n
            if not (min_palabras <= n <= max_palabras):
                continue
            if any(x & (MATEMATICAS | CODIGO | CITA_TEXTUAL) for x in bs):
                continue
            capitulo = s["seccion"].split(" › ")[0]
            candidatas.append({"texto": t, "archivo": s["archivo"], "linea": s["linea_ini"],
                               "capitulo": capitulo, "citas": s["citas"],
                               "normas": [normalizar(w) for w, _, _ in palabras(t)]})
    if not candidatas:
        return []
    df = Counter(w for c in candidatas for w in set(c["normas"]))
    n = len(candidatas)
    for c in candidatas:
        c["especificidad"] = round(sum(math.log(n / df[w]) for w in c["normas"]) / len(c["normas"]), 3)
    por_cap: dict[str, list] = {}
    for c in candidatas:
        por_cap.setdefault(c["capitulo"], []).append(c)
    total = len(candidatas)
    cupos = {cap: max(1, round(k * len(cs) / total)) for cap, cs in por_cap.items()}
    while sum(cupos.values()) > k:
        mayor = max(cupos, key=lambda c: cupos[c])
        cupos[mayor] -= 1
        if cupos[mayor] == 0:
            del cupos[mayor]
    elegidas = []
    for cap, cupo in cupos.items():
        cs = sorted(por_cap[cap], key=lambda c: (-c["especificidad"], c["linea"]))
        elegidas.extend(cs[:cupo])
    elegidas.sort(key=lambda c: (c["archivo"], c["linea"]))
    for c in elegidas:
        c.pop("normas")
    return elegidas[:k]


def markdown(elegidas: list[dict]) -> str:
    lineas = ["# Oraciones para buscar en la web", "",
              "Nada de esto se envió a ningún servicio. Copie cada oración entre comillas en un "
              "buscador; un resultado vacío no prueba originalidad (cobertura del buscador, "
              "paywalls, PDFs no indexados).", ""]
    for n, c in enumerate(elegidas, 1):
        cita = f" (cita: {', '.join(c['citas'])})" if c["citas"] else ""
        lineas += [f"{n}. `{c['archivo']}:{c['linea']}` — {c['capitulo']}{cita}", "",
                   f"   \"{c['texto']}\"", ""]
    return "\n".join(lineas)
