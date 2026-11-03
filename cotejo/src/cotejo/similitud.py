"""Coincidencias literales entre el documento y el corpus: shingles, índice invertido y alineación."""
from __future__ import annotations

import difflib
from collections import defaultdict
from dataclasses import asdict, dataclass

from .texto import CITA_TEXTUAL, CODIGO, MATEMATICAS, normalizar, palabras, palabras_normalizadas

DEFINICION = ("Índice de similitud = palabras del documento (tras los filtros indicados) que "
              "coinciden con alguna fuente del corpus local, dividido entre las palabras del "
              "documento tras los mismos filtros, por 100.")
FUENTE_DEFINICION = {
    "url": "https://guides.turnitin.com/hc/en-us/articles/23435833938701-Understanding-the-similarity-score",
    "consultada": False,
    "nota": ("La definición sigue la guía pública enlazada (porcentaje de palabras del envío que "
             "coinciden). La página no se pudo abrir desde el entorno donde se escribió esta "
             "herramienta (3 nov 2026, red bloqueada); verifíquela antes de citarla. El corpus, la "
             "normalización y los filtros del servicio comercial son distintos y privados: este "
             "número no es equivalente al suyo."),
}


@dataclass
class Filtros:
    bibliografia: bool = False
    citas: bool = False
    menores: int = 0
    ecuaciones: bool = False
    codigo: bool = False

    def nombre(self) -> str:
        p = [n for n, v in (("bibliografía", self.bibliografia), ("citas textuales", self.citas),
                            ("ecuaciones", self.ecuaciones), ("código", self.codigo)) if v]
        if self.menores:
            p.append(f"coincidencias < {self.menores} palabras")
        return "excluye " + ", ".join(p) if p else "sin filtros"


def palabras_documento(extr: dict) -> list[dict]:
    salida = []
    for seg in extr["segmentos"]:
        offs = palabras(seg["texto"])
        for (w, linea, banderas), (_, a, b) in zip(seg["palabras"], offs):
            salida.append({"w": w, "n": normalizar(w), "seg": seg["id"], "linea": linea,
                           "b": banderas, "tipo": seg["tipo"], "a": a, "b_": b})
    return salida


def _texto_original(docw: list[dict], segs: dict, i: int, j: int) -> str:
    partes, k = [], i
    while k < j:
        s = docw[k]["seg"]
        fin = k
        while fin + 1 < j and docw[fin + 1]["seg"] == s:
            fin += 1
        partes.append(segs[s]["texto"][docw[k]["a"]:docw[fin]["b_"]])
        k = fin + 1
    return " ¶ ".join(partes)


def excluida(p: dict, f: Filtros) -> bool:
    if f.bibliografia and p["tipo"] == "bibliografia":
        return True
    if f.ecuaciones and (p["b"] & MATEMATICAS or p["tipo"] == "ecuacion"):
        return True
    if f.codigo and (p["b"] & CODIGO or p["tipo"] == "codigo"):
        return True
    return bool(f.citas and p["b"] & CITA_TEXTUAL)


@dataclass
class Pasaje:
    fuente: str
    di: int
    de: int
    sj: int
    se: int
    exactos: list


def _indice(fuentes: dict[str, list[str]], n: int):
    idx = defaultdict(list)
    for clave, toks in fuentes.items():
        for j in range(len(toks) - n + 1):
            idx[tuple(toks[j:j + n])].append((clave, j))
    return idx


def alinear(doc: list[str], fuentes: dict[str, list[str]], n: int = 5, hueco: int = 3,
            max_ocurrencias: int = 50) -> list[Pasaje]:
    idx = _indice(fuentes, n)
    cubierto: dict[tuple[str, int], int] = {}
    exactos = defaultdict(list)
    for i in range(len(doc) - n + 1):
        lista = idx.get(tuple(doc[i:i + n]))
        if not lista or len(lista) > max_ocurrencias:
            continue
        for clave, j in lista:
            diag = j - i
            if cubierto.get((clave, diag), -1) > i:
                continue
            src = fuentes[clave]
            a, b = i, j
            while a > 0 and b > 0 and doc[a - 1] == src[b - 1]:
                a, b = a - 1, b - 1
            e, f = i + n, j + n
            while e < len(doc) and f < len(src) and doc[e] == src[f]:
                e, f = e + 1, f + 1
            cubierto[(clave, diag)] = e
            exactos[clave].append((a, e, b, f))
    pasajes = []
    for clave, lista in exactos.items():
        lista.sort()
        actual = None
        for a, e, b, f in lista:
            if actual and a <= actual.de + hueco and actual.sj - hueco <= b <= actual.se + hueco:
                actual.de = max(actual.de, e)
                actual.sj = min(actual.sj, b)
                actual.se = max(actual.se, f)
                actual.exactos.append((a, e))
            else:
                actual = Pasaje(clave, a, e, b, f, [(a, e)])
                pasajes.append(actual)
    pasajes.sort(key=lambda p: (p.di, p.fuente))
    return pasajes


def _contados(p: Pasaje, docw: list[dict], f: Filtros) -> set[int]:
    s = {k for a, e in p.exactos for k in range(a, e) if not excluida(docw[k], f)}
    return s if not f.menores or len(s) >= f.menores else set()


def medir(docw: list[dict], pasajes: list[Pasaje], f: Filtros) -> dict:
    total = sum(1 for p in docw if not excluida(p, f))
    por_fuente = defaultdict(set)
    for p in pasajes:
        por_fuente[p.fuente] |= _contados(p, docw, f)
    union = set().union(*por_fuente.values()) if por_fuente else set()
    orden = sorted(por_fuente, key=lambda c: (-len(por_fuente[c]), c))
    asignadas, primaria = set(), {}
    for c in orden:
        propias = por_fuente[c] - asignadas
        primaria[c] = propias
        asignadas |= propias
    return {"total": total, "union": union, "por_fuente": por_fuente, "primaria": primaria,
            "orden": [c for c in orden if por_fuente[c]]}


def _pct(a: int, b: int) -> float:
    return round(100.0 * a / b, 2) if b else 0.0


def cotejar(extr: dict, textos: dict[str, tuple[dict, str]], filtros: Filtros, n: int = 5,
            hueco: int = 3, max_ocurrencias: int = 50) -> dict:
    docw = palabras_documento(extr)
    doc = [p["n"] for p in docw]
    tok_fuentes, offs = {}, {}
    for clave, (_, texto) in textos.items():
        ws = palabras_normalizadas(texto)
        tok_fuentes[clave] = [w for w, _, _ in ws]
        offs[clave] = [(a, b) for _, a, b in ws]
    pasajes = alinear(doc, tok_fuentes, n, hueco, max_ocurrencias)
    segs = {s["id"]: s for s in extr["segmentos"]}
    citadas_doc = set(extr.get("citadas", []))

    variantes = [Filtros(), Filtros(bibliografia=True), Filtros(citas=True),
                 Filtros(ecuaciones=True, codigo=True)]
    if filtros.menores:
        variantes.append(Filtros(menores=filtros.menores))
    variantes += [Filtros(True, True, filtros.menores, True, True), filtros]
    indices, vistos = [], set()
    for v in variantes:
        clave_v = tuple(asdict(v).values())
        if clave_v in vistos:
            continue
        vistos.add(clave_v)
        m = medir(docw, pasajes, v)
        indices.append({"nombre": v.nombre(), "filtros": asdict(v), "elegido": v == filtros,
                        "palabras_documento": m["total"], "palabras_coincidentes": len(m["union"]),
                        "indice": _pct(len(m["union"]), m["total"])})
    m = medir(docw, pasajes, filtros)

    salida_pasajes = []
    for k, p in enumerate(pasajes):
        reg, texto = textos[p.fuente]
        cont = _contados(p, docw, filtros)
        ids_seg = sorted({docw[i]["seg"] for i in range(p.di, p.de)})
        citas = {c for s in ids_seg for c in segs[s]["citas"]}
        propio = reg.get("tipo") == "propio"
        exactas = sum(e - a for a, e in _fusionar(p.exactos))
        en_comillas = sum(1 for a, e in p.exactos for i in range(a, e) if docw[i]["b"] & CITA_TEXTUAL)
        oa, ob = offs[p.fuente][p.sj][0], offs[p.fuente][p.se - 1][1]
        razon = difflib.SequenceMatcher(None, doc[p.di:p.de], tok_fuentes[p.fuente][p.sj:p.se],
                                        autojunk=False).ratio()
        if propio:
            estado = "fuente propia"
        elif p.fuente in citas:
            estado = "citada en el párrafo"
        elif p.fuente in citadas_doc:
            estado = "citada en otro lugar del documento, no en este párrafo"
        else:
            estado = "sin cita"
        primero = segs[ids_seg[0]]
        salida_pasajes.append({
            "id": k, "fuente": p.fuente, "palabra_ini": p.di, "palabra_fin": p.de,
            "palabras_exactas": exactas, "palabras_contadas": len(cont),
            "fraccion_entre_comillas": round(en_comillas / max(1, exactas), 2),
            "razon_alineacion": round(razon, 3), "segmentos": ids_seg,
            "archivo": primero["archivo"], "linea": docw[p.di]["linea"],
            "linea_fin": docw[p.de - 1]["linea"], "seccion": primero["seccion"],
            "tipo_segmento": primero["tipo"], "estado_cita": estado,
            "texto_documento": _texto_original(docw, segs, p.di, p.de),
            "texto_fuente": texto[oa:ob][:1500],
        })
    gravedad = {"sin cita": 0, "citada en otro lugar del documento, no en este párrafo": 1,
                "fuente propia": 2, "citada en el párrafo": 3}
    salida_pasajes.sort(key=lambda x: (gravedad[x["estado_cita"]], -x["palabras_contadas"], x["id"]))

    fuentes = []
    for c in m["orden"]:
        reg = textos[c][0]
        ps = [x for x in salida_pasajes if x["fuente"] == c and x["palabras_contadas"]]
        fuentes.append({
            "clave": c, "titulo": reg.get("titulo", ""), "tipo": reg.get("tipo", ""),
            "origen": reg.get("origen", ""), "palabras_coincidentes": len(m["por_fuente"][c]),
            "porcentaje": _pct(len(m["por_fuente"][c]), m["total"]),
            "palabras_primarias": len(m["primaria"][c]),
            "porcentaje_primario": _pct(len(m["primaria"][c]), m["total"]),
            "pasajes": len(ps),
            "pasajes_sin_cita": sum(1 for x in ps if x["estado_cita"] == "sin cita"),
            "citada_en_documento": None if reg.get("tipo") == "propio" else c in citadas_doc,
        })
    marcas, actual = [], None
    dueño = {i: c for c, s in m["primaria"].items() for i in s}
    for i in range(len(docw)):
        c = dueño.get(i)
        if actual and c == actual[2] and i == actual[1]:
            actual[1] = i + 1
        elif c:
            actual = [i, i + 1, c]
            marcas.append(actual)
    return {
        "definicion": DEFINICION, "fuente_definicion": FUENTE_DEFINICION,
        "parametros": {"n_shingle": n, "hueco": hueco, "max_ocurrencias": max_ocurrencias,
                       "normalizacion": "minúsculas, sin acentos, NFKC, confusables cirílicos/griegos plegados, invisibles quitados"},
        "filtros": asdict(filtros), "filtros_nombre": filtros.nombre(),
        "indice": _pct(len(m["union"]), m["total"]),
        "palabras_documento": m["total"], "palabras_coincidentes": len(m["union"]),
        "indices": indices, "fuentes": fuentes, "pasajes": salida_pasajes, "marcas": marcas,
        "fuentes_cotejadas": sorted(textos),
    }


def _fusionar(rangos):
    salida = []
    for a, e in sorted(rangos):
        if salida and a <= salida[-1][1]:
            salida[-1][1] = max(salida[-1][1], e)
        else:
            salida.append([a, e])
    return salida
