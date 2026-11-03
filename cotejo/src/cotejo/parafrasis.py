"""Paráfrasis cercana con embeddings multilingües (opcional; no entra al índice de similitud)."""
from __future__ import annotations

from .texto import oraciones, palabras

MODELO = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def cargar_codificador(nombre: str = MODELO):
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer(nombre)
    return lambda textos: m.encode(textos, batch_size=64, normalize_embeddings=True,
                                   convert_to_numpy=True, show_progress_bar=False)


def _oraciones_doc(extr: dict, min_palabras: int):
    salida = []
    for s in extr["segmentos"]:
        if s["tipo"] not in ("prosa", "leyenda"):
            continue
        for a, b in oraciones(s["texto"]):
            t = s["texto"][a:b].strip()
            if len(palabras(t)) >= min_palabras:
                salida.append({"segmento": s["id"], "archivo": s["archivo"], "linea": s["linea_ini"],
                               "texto": t, "citas": s["citas"]})
    return salida


def parafrasis(extr: dict, textos: dict, codificador, top: int = 50, min_palabras: int = 10,
               cubiertos: set[int] | None = None) -> dict:
    import numpy as np
    docs = [o for o in _oraciones_doc(extr, min_palabras) if o["segmento"] not in (cubiertos or set())]
    fuentes = []
    for clave, (_, texto) in textos.items():
        for a, b in oraciones(" ".join(texto.split())):
            t = " ".join(texto.split())[a:b].strip()
            if len(palabras(t)) >= min_palabras:
                fuentes.append((clave, t))
    if not docs or not fuentes:
        return {"disponible": True, "pares": [], "nota": "sin oraciones suficientes"}
    ed = np.asarray(codificador([d["texto"] for d in docs]), dtype="float32")
    ef = np.asarray(codificador([t for _, t in fuentes]), dtype="float32")
    mejores = []
    for i in range(0, len(ed), 256):
        sim = ed[i:i + 256] @ ef.T
        j = sim.argmax(axis=1)
        for k, (jj, v) in enumerate(zip(j, sim[np.arange(len(j)), j])):
            mejores.append((float(v), i + k, int(jj)))
    mejores.sort(reverse=True)
    pares = []
    for v, i, j in mejores[:top]:
        d, (clave, t) = docs[i], fuentes[j]
        pares.append({"coseno": round(v, 4), "fuente": clave, "archivo": d["archivo"],
                      "linea": d["linea"], "texto_documento": d["texto"], "texto_fuente": t,
                      "citada_en_parrafo": clave in d["citas"]})
    return {"disponible": True, "pares": pares,
            "nota": (f"Las {top} oraciones con mayor coseno respecto a alguna oración del corpus. "
                     "Es una lista para revisar a mano, no un índice ni un umbral: un coseno alto "
                     "puede ser solo el mismo tema.")}
