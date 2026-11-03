"""cotejo extraer|corpus|similitud|web|banderas|detectar|reporte|todo"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__


def _guardar(ruta: Path, datos):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")


def _leer(ruta: Path):
    if not ruta.exists():
        sys.exit(f"Falta {ruta}. Corra antes el paso que lo genera.")
    return json.loads(ruta.read_text(encoding="utf-8"))


def cmd_extraer(a):
    from .latex import extraer
    extr = extraer(Path(a.raiz), Path(a.bib) if a.bib else None, con_bibliografia=not a.sin_bibliografia)
    extr["raiz_absoluta"] = str(Path(a.raiz).resolve())
    if a.pdf:
        extr["comparacion_pdf"] = _comparar_pdf(extr, Path(a.pdf))
    _guardar(Path(a.salida) / "extraccion.json", extr)
    n = sum(len(s["palabras"]) for s in extr["segmentos"])
    print(f"{len(extr['segmentos'])} segmentos, {n} palabras, {len(extr['archivos'])} archivos")
    if extr["faltantes"]:
        print("Archivos no encontrados:", ", ".join(extr["faltantes"]))
    if extr["ciclos"]:
        print("Inclusiones cíclicas omitidas:", "; ".join(extr["ciclos"]))
    if extr.get("comparacion_pdf"):
        c = extr["comparacion_pdf"]
        print(f"PDF ({c['metodo']}): {c['palabras_pdf']} palabras; trigramas del .tex presentes en el PDF: "
              f"{c['trigramas_tex_en_pdf']:.1%}; del PDF presentes en el .tex: {c['trigramas_pdf_en_tex']:.1%}")


def _comparar_pdf(extr: dict, pdf: Path) -> dict:
    from .corpus import texto_pdf
    from .texto import palabras_normalizadas, normalizar
    texto, metodo = texto_pdf(pdf)
    wp = [w for w, _, _ in palabras_normalizadas(texto)]
    wt = [normalizar(w) for s in extr["segmentos"] for w, _, _ in s["palabras"]]
    tp = {tuple(wp[i:i + 3]) for i in range(len(wp) - 2)}
    tt = {tuple(wt[i:i + 3]) for i in range(len(wt) - 2)}
    lineas = []
    for linea in texto.splitlines():
        ws = [w for w, _, _ in palabras_normalizadas(linea)]
        tri = [tuple(ws[i:i + 3]) for i in range(len(ws) - 2)]
        if len(tri) >= 5 and sum(t in tt for t in tri) / len(tri) < 0.2:
            lineas.append(linea.strip()[:200])
    return {"archivo": pdf.name, "metodo": metodo, "palabras_pdf": len(wp), "palabras_tex": len(wt),
            "trigramas_tex_en_pdf": len(tt & tp) / max(1, len(tt)),
            "trigramas_pdf_en_tex": len(tt & tp) / max(1, len(tp)),
            "lineas_pdf_ausentes_en_tex": lineas[:200],
            "nota": "Ligaduras, guiones, encabezados, índices, ecuaciones y la portada explican parte de la diferencia."}


def cmd_corpus(a):
    from .corpus import construir, plantilla_desde_bib
    if a.plantilla:
        datos = plantilla_desde_bib(Path(a.bib))
        Path(a.plantilla).write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Plantilla con {len(datos)} fuentes en {a.plantilla}; complete url_pdf/url_html y licencia.")
        return
    locales = []
    for patron in a.locales or []:
        p = Path(patron)
        locales += sorted(p.parent.glob(p.name)) if any(c in p.name for c in "*?[") else [p]
    m = construir(Path(a.cache), Path(a.fuentes) if a.fuentes else None, Path(a.pdfs) if a.pdfs else None,
                  locales, refrescar=a.refrescar, sin_red=a.sin_red)
    ok = sum(1 for r in m["fuentes"].values() if r.get("estado") == "ok")
    print(f"Corpus: {ok} fuentes con texto de {len(m['fuentes'])} registradas en {a.cache}")


def _filtros(a):
    from .similitud import Filtros
    return Filtros(bibliografia=a.excluir_bibliografia, citas=a.excluir_citas, menores=a.excluir_menores,
                   ecuaciones=a.excluir_ecuaciones, codigo=a.excluir_codigo)


def cmd_similitud(a):
    from .corpus import Corpus
    from .similitud import cotejar
    extr = _leer(Path(a.salida) / "extraccion.json")
    corpus = Corpus(Path(a.cache))
    textos = corpus.textos()
    if not textos:
        print("Aviso: el corpus está vacío; el índice será 0 por falta de fuentes, no por originalidad.")
    sim = cotejar(extr, textos, _filtros(a), n=a.n, hueco=a.hueco, max_ocurrencias=a.max_ocurrencias)
    sim["corpus_cache"] = str(Path(a.cache).resolve())
    if a.parafrasis:
        from .parafrasis import MODELO, cargar_codificador, parafrasis
        try:
            cod = cargar_codificador(a.modelo_parafrasis or MODELO)
            cubiertos = {s for p in sim["pasajes"] if p["palabras_contadas"] for s in p["segmentos"]}
            sim["parafrasis"] = parafrasis(extr, textos, cod, top=a.top_parafrasis, cubiertos=cubiertos)
            sim["parafrasis"]["modelo"] = a.modelo_parafrasis or MODELO
        except Exception as e:
            sim["parafrasis"] = {"disponible": False, "motivo": f"{type(e).__name__}: {e}"}
            print(f"Paráfrasis desactivada: {type(e).__name__}: {e}")
    else:
        sim["parafrasis"] = {"disponible": False, "motivo": "no se pidió (--parafrasis)"}
    _guardar(Path(a.salida) / "similitud.json", sim)
    print(f"Índice de similitud contra el corpus local: {sim['indice']:.2f} % ({sim['filtros_nombre']}); "
          f"{len(sim['fuentes'])} fuentes con coincidencias. No equivale al índice del servicio comercial que use la universidad.")


def cmd_web(a):
    from .web import markdown, muestra
    extr = _leer(Path(a.salida) / "extraccion.json")
    elegidas = muestra(extr, a.muestra)
    _guardar(Path(a.salida) / "web_muestra.json", elegidas)
    (Path(a.salida) / "web_muestra.md").write_text(markdown(elegidas), encoding="utf-8")
    print(f"{len(elegidas)} oraciones en {Path(a.salida) / 'web_muestra.md'} (no se envió nada)")


def cmd_banderas(a):
    from .banderas import ejecutar
    extr = _leer(Path(a.salida) / "extraccion.json")
    base = Path(extr["raiz_absoluta"]).parent.parent
    ban = ejecutar(extr, base, Path(a.pdf) if a.pdf else None, a.tam_min)
    _guardar(Path(a.salida) / "banderas.json", ban)
    n = len(ban["tex"]["hallazgos"]) + len((ban.get("pdf") or {}).get("hallazgos", []))
    print(f"{n} alertas ({'con' if a.pdf else 'sin'} PDF)")


def cmd_detectar(a):
    from .detectores import PARES, Modelos, detectar
    extr = _leer(Path(a.salida) / "extraccion.json")
    base, instruct = PARES[a.pares]
    base, instruct = a.base or base, a.instruct or instruct
    try:
        modelos = Modelos.cargar(base, instruct, a.dispositivo)
        motivo = ""
    except Exception as e:
        modelos, motivo = None, f"no se pudieron cargar {base} / {instruct}: {type(e).__name__}: {e}"
        print(motivo)
    det = detectar(extr, modelos, Path(a.referencia) if a.referencia else None, a.min_palabras,
                   a.max_tokens, motivo=motivo)
    _guardar(Path(a.salida) / "detectores.json", det)
    if det["disponible"]:
        print(f"{len(det['parrafos'])} párrafos puntuados. " + (det.get("aviso_referencia") or ""))


def cmd_reporte(a):
    from .reporte import generar
    generar(Path(a.salida), Path(a.cache) if a.cache else None)
    print(f"Reporte en {Path(a.salida) / 'reporte.html'}, reporte.json y summary.md")


def cmd_todo(a):
    cmd_extraer(a)
    if a.fuentes or a.pdfs or a.locales:
        cmd_corpus(a)
    cmd_banderas(a)
    cmd_similitud(a)
    cmd_web(a)
    if a.detectar:
        cmd_detectar(a)
    cmd_reporte(a)


def _opciones(p, *grupos):
    if "salida" in grupos:
        p.add_argument("--salida", default="cotejo_salida", help="carpeta de resultados")
    if "extraer" in grupos:
        p.add_argument("--raiz", required=True, help="archivo .tex principal (p. ej. .tex_uacj/tesis_uacj.tex)")
        p.add_argument("--bib", help="archivo .bib (por defecto, el de \\bibliography)")
        p.add_argument("--sin-bibliografia", action="store_true", help="no generar texto de la bibliografía")
    if "pdf" in grupos:
        p.add_argument("--pdf", help="PDF compilado (para comparar y para las alertas)")
    if "corpus" in grupos:
        p.add_argument("--cache", default=".cotejo_corpus", help="carpeta de caché del corpus")
        p.add_argument("--fuentes", help="JSON con clave, url_pdf o url_html, licencia")
        p.add_argument("--pdfs", help="carpeta con PDFs locales; el nombre del archivo es la clave")
        p.add_argument("--locales", nargs="*", help="textos propios (README, revision_*.md) para autoplagio")
        p.add_argument("--refrescar", action="store_true", help="volver a descargar aunque esté en caché")
        p.add_argument("--sin-red", action="store_true", help="no descargar nada")
    if "similitud" in grupos:
        p.add_argument("--n", type=int, default=5, help="palabras por shingle")
        p.add_argument("--hueco", type=int, default=3, help="palabras distintas toleradas dentro de un pasaje")
        p.add_argument("--max-ocurrencias", type=int, default=50)
        p.add_argument("--excluir-bibliografia", action="store_true")
        p.add_argument("--excluir-citas", action="store_true", help="texto entre comillas o en quote")
        p.add_argument("--excluir-menores", type=int, default=0, metavar="N",
                       help="excluir coincidencias de menos de N palabras")
        p.add_argument("--excluir-ecuaciones", action="store_true")
        p.add_argument("--excluir-codigo", action="store_true")
        p.add_argument("--parafrasis", action="store_true", help="activar embeddings (sentence-transformers)")
        p.add_argument("--modelo-parafrasis")
        p.add_argument("--top-parafrasis", type=int, default=50)
    if "web" in grupos:
        p.add_argument("--muestra", type=int, default=20, help="número de oraciones")
    if "banderas" in grupos:
        p.add_argument("--tam-min", type=float, default=1.0, help="tamaño (pt) por debajo del cual se avisa")
    if "detectar" in grupos:
        p.add_argument("--pares", choices=["pequeno", "articulo"], default="pequeno")
        p.add_argument("--base", help="modelo base (observador / muestreo)")
        p.add_argument("--instruct", help="modelo instruct (intérprete / puntuación)")
        p.add_argument("--dispositivo", help="cuda, cuda:0 o cpu")
        p.add_argument("--referencia", help="carpeta con subcarpetas humano/ y generado/")
        p.add_argument("--min-palabras", type=int, default=40)
        p.add_argument("--max-tokens", type=int, default=512)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="cotejo", description=__doc__)
    ap.add_argument("--version", action="version", version=f"cotejo {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)
    tabla = {
        "extraer": (cmd_extraer, ("salida", "extraer", "pdf")),
        "corpus": (cmd_corpus, ("corpus",)),
        "similitud": (cmd_similitud, ("salida", "corpus", "similitud")),
        "web": (cmd_web, ("salida", "web")),
        "banderas": (cmd_banderas, ("salida", "pdf", "banderas")),
        "detectar": (cmd_detectar, ("salida", "detectar")),
        "reporte": (cmd_reporte, ("salida",)),
        "todo": (cmd_todo, ("salida", "extraer", "pdf", "corpus", "similitud", "web", "banderas", "detectar")),
    }
    for nombre, (fn, grupos) in tabla.items():
        p = sub.add_parser(nombre)
        _opciones(p, *grupos)
        if nombre == "corpus":
            p.add_argument("--plantilla", help="escribir una plantilla de fuentes desde --bib y salir")
            p.add_argument("--bib", help="archivo .bib para --plantilla")
        if nombre == "reporte":
            p.add_argument("--cache", help="carpeta del corpus (por defecto, la usada en similitud)")
        if nombre == "todo":
            p.add_argument("--detectar", action="store_true", help="correr también los detectores")
            p.add_argument("--plantilla", help=argparse.SUPPRESS)
        p.set_defaults(fn=fn)
    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
