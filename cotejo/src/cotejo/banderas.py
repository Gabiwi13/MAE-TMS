"""Alertas de integridad del documento: texto oculto, sustitución de caracteres y metadatos."""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

INVISIBLES = {"\u200b": "espacio de ancho cero", "\u200c": "no unión de ancho cero",
              "\u200d": "unión de ancho cero", "\u2060": "unión de palabra",
              "\ufeff": "BOM/espacio no separable de ancho cero", "\u00ad": "guion blando",
              "\u180e": "separador de vocal mongol"}
BIDI = {chr(c) for c in list(range(0x202A, 0x202F)) + list(range(0x2066, 0x206A))}
ESPACIOS_RAROS = {chr(c) for c in list(range(0x2000, 0x200B)) + [0x202F, 0x205F, 0x3000]}
RE_PAL = re.compile(r"\w+", re.UNICODE)


def _escritura(c: str) -> str:
    try:
        nombre = unicodedata.name(c)
    except ValueError:
        return ""
    for e in ("LATIN", "CYRILLIC", "GREEK"):
        if nombre.startswith(e):
            return e
    return ""


def _uso_privado(c: str) -> bool:
    return unicodedata.category(c) == "Co"


def caracteres(texto: str) -> list[dict]:
    """Posiciones de caracteres que suelen usarse para sustituir o esconder texto."""
    hallazgos = []
    for k, c in enumerate(texto):
        if c in INVISIBLES:
            hallazgos.append({"pos": k, "tipo": "invisible", "detalle": INVISIBLES[c], "cp": f"U+{ord(c):04X}"})
        elif c in BIDI:
            hallazgos.append({"pos": k, "tipo": "control bidireccional", "detalle": unicodedata.name(c, ""), "cp": f"U+{ord(c):04X}"})
        elif _uso_privado(c):
            hallazgos.append({"pos": k, "tipo": "uso privado", "detalle": "carácter de uso privado (puede venir de una fuente matemática sin mapa Unicode)", "cp": f"U+{ord(c):04X}"})
        elif c in ESPACIOS_RAROS:
            hallazgos.append({"pos": k, "tipo": "espacio poco común", "detalle": unicodedata.name(c, ""), "cp": f"U+{ord(c):04X}"})
    for m in RE_PAL.finditer(texto):
        w = m.group()
        esc = [_escritura(c) for c in w]
        escrituras = set(esc) - {""}
        if "LATIN" in escrituras and escrituras & {"CYRILLIC", "GREEK"}:
            ajenos = [f"{c} U+{ord(c):04X} {unicodedata.name(c, '')}" for c, e in zip(w, esc)
                      if e in ("CYRILLIC", "GREEK")]
            interior = any(e in ("CYRILLIC", "GREEK") and "LATIN" in esc[:k] and "LATIN" in esc[k + 1:]
                           for k, e in enumerate(esc))
            hallazgos.append({"pos": m.start(),
                              "tipo": "escritura mezclada" if interior else "símbolo no latino pegado",
                              "detalle": f"«{w}» mezcla latín con: " + "; ".join(ajenos),
                              "cp": ""})
        elif escrituras == {"CYRILLIC"}:
            hallazgos.append({"pos": m.start(), "tipo": "palabra cirílica",
                              "detalle": f"«{m.group()}»", "cp": ""})
    return hallazgos


PRIORIDAD_CAR = {"escritura mezclada": "alta", "símbolo no latino pegado": "baja", "invisible": "media", "control bidireccional": "alta",
                 "uso privado": "baja", "espacio poco común": "baja", "palabra cirílica": "media"}


def _hallazgos_car(lista: list[tuple[dict, dict]], recomendacion: str, extra=None) -> list[dict]:
    """lista de (hallazgo de caracteres, ubicación). Los de prioridad alta van uno por uno;
    los demás se agrupan por tipo cuando son más de cinco."""
    por_tipo: dict[str, list] = {}
    for h, u in lista:
        por_tipo.setdefault(h["tipo"], []).append((h, u))
    salida = []
    for tipo, items in por_tipo.items():
        prio = PRIORIDAD_CAR[tipo]
        regla = "CAR-" + tipo.upper().replace(" ", "-")
        if prio == "alta" or len(items) <= 5:
            for h, u in items:
                salida.append(_hallazgo(regla, "sustitución de caracteres", prio, "confirmado",
                                        f"{h['tipo']}: {h['detalle']} {h['cp']}".strip(), [u],
                                        recomendacion, (extra or {}).get(id(h), {})))
        else:
            ejemplos = sorted({f"{h['detalle']} {h['cp']}".strip() for h, _ in items})[:10]
            salida.append(_hallazgo(regla, "sustitución de caracteres", prio, "confirmado",
                                    f"{len(items)} casos de «{tipo}». Ejemplos: " + " | ".join(ejemplos),
                                    [u for _, u in items[:10]], recomendacion,
                                    {"casos": len(items)}))
    return salida


def _contexto(texto: str, pos: int, ancho: int = 40) -> str:
    frag = texto[max(0, pos - ancho):pos + ancho]
    return "".join(f"⟦U+{ord(c):04X}⟧" if c in INVISIBLES or c in BIDI else c for c in frag).replace("\n", " ")


def _hallazgo(regla, categoria, prioridad, evidencia, mensaje, ubicaciones, recomendacion, extra=None):
    return {"regla": regla, "categoria": categoria, "prioridad": prioridad,
            "estado_evidencia": evidencia, "mensaje": mensaje, "ubicaciones": ubicaciones,
            "evidencia": extra or {}, "recomendacion": recomendacion}


# ---------------------------------------------------------------- .tex
def _sin_comentarios(linea: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", linea)


BLANCOS = [r"white", r"White", r"blanco"]
RE_DEF_COLOR = re.compile(r"\\definecolor\{([^}]+)\}\{(rgb|RGB|gray|HTML|cmyk)\}\{([^}]+)\}")


def _es_blanco(modelo: str, valor: str) -> bool:
    v = [x.strip() for x in valor.split(",")]
    try:
        if modelo == "rgb":
            return all(float(x) >= 0.97 for x in v)
        if modelo == "RGB":
            return all(float(x) >= 248 for x in v)
        if modelo == "gray":
            return float(v[0]) >= 0.97
        if modelo == "HTML":
            return v[0].upper() in ("FFFFFF", "FEFEFE", "FDFDFD")
        if modelo == "cmyk":
            return all(float(x) <= 0.03 for x in v)
    except ValueError:
        return False
    return False


def banderas_tex(archivos: dict[str, Path]) -> list[dict]:
    hallazgos = []
    nombres_blancos = set(BLANCOS)
    textos = {rel: ruta.read_text(encoding="utf-8", errors="replace") for rel, ruta in archivos.items()}
    for texto in textos.values():
        for m in RE_DEF_COLOR.finditer(texto):
            if _es_blanco(m.group(2), m.group(3)):
                nombres_blancos.add(re.escape(m.group(1)))
    blanco = "|".join(nombres_blancos)
    reglas = [
        ("TEX-COLOR-BLANCO", "texto oculto", "media",
         re.compile(r"\\(?:textcolor|color)\s*\{\s*(?:" + blanco + r")\s*\}"
                    r"|\\(?:textcolor|color)\s*\[(?:rgb|RGB|gray|HTML|cmyk)\]\s*\{\s*(?:1\s*,\s*1\s*,\s*1|255\s*,\s*255\s*,\s*255|1|FFFFFF|ffffff|0\s*,\s*0\s*,\s*0\s*,\s*0)\s*\}"),
         "Texto con color blanco o equivalente declarado en la fuente.",
         "El blanco no es invisible por sí solo: compruebe el fondo en el PDF."),
        ("TEX-FANTASMA", "texto oculto", "baja",
         re.compile(r"\\[hv]?phantom\s*\{([^}]*\s[^}]*\s[^}]*)\}"),
         "\\phantom con varias palabras: ocupa espacio sin imprimirse.",
         "En matemáticas suele ser legítimo; revise si contiene prosa."),
        ("TEX-TAMANO", "texto oculto", "media",
         re.compile(r"\\fontsize\s*\{\s*0*(?:\.\d+|0)\s*(?:pt)?\s*\}|\\scalebox\s*\{\s*0?\.0\d*\s*\}"
                    r"|\\resizebox\s*\{\s*0*(?:\.\d+)?\s*(?:pt|mm|cm)\s*\}"),
         "Tamaño de letra o escala casi nula.", "Compruebe en el PDF si el texto es legible."),
        ("TEX-RENDER", "texto oculto", "alta",
         re.compile(r"\\pdfliteral|\\pdfextension\s+literal|\\special\s*\{\s*pdf|\\pdfrender|\b[37]\s+Tr\b"),
         "Instrucción PDF directa (puede cambiar el modo de render del texto).",
         "Revise qué hace; el modo 3 vuelve el texto invisible pero extraíble."),
        ("TEX-FUERA", "texto oculto", "media",
         re.compile(r"\\put\s*\(\s*-?\d{4,}|\\[hv]space\*?\s*\{\s*-\s*\d{2,}(?:\.\d+)?\s*(?:cm|in)\s*\}"
                    r"|\\raisebox\s*\{\s*-?\d{2,}(?:\.\d+)?\s*(?:cm|in)\s*\}|\\begin\{textblock\*?\}"),
         "Desplazamiento grande: el texto podría quedar fuera de la página.",
         "Compruebe la posición en el PDF."),
    ]
    for rel, texto in textos.items():
        comentarios = 0
        for n, linea in enumerate(texto.splitlines(), 1):
            if re.search(r"(?<!\\)%\s*\S", linea):
                comentarios += 1
            activa = _sin_comentarios(linea)
            for regla, cat, prio, rx, msg, rec in reglas:
                for m in rx.finditer(activa):
                    extra = {}
                    if regla == "TEX-COLOR-BLANCO":
                        extra["fondo_en_la_linea"] = bool(re.search(
                            r"\\(?:cellcolor|rowcolor|colorbox|fcolorbox|pagecolor)|fill\s*=", activa))
                    hallazgos.append(_hallazgo(regla, cat, prio, "candidato", msg,
                                               [{"archivo": rel, "linea": n, "fragmento": activa.strip()[:200]}],
                                               rec, extra))
        lineas = texto.splitlines()
        lista, extra = [], {}
        for h in caracteres(texto):
            n = texto.count("\n", 0, h["pos"]) + 1
            linea = lineas[n - 1] if n <= len(lineas) else ""
            col = h["pos"] - texto.rfind("\n", 0, h["pos"]) - 1
            extra[id(h)] = {"en_comentario": bool(re.search(r"(?<!\\)%", linea[:col]))}
            lista.append((h, {"archivo": rel, "linea": n, "fragmento": _contexto(texto, h["pos"])}))
        hallazgos += _hallazgos_car(
            lista, "Reemplace por el carácter latino o elimine el invisible si no es intencional.", extra)
        if comentarios:
            hallazgos.append(_hallazgo(
                "TEX-COMENTARIOS", "documento", "informativa", "informativo",
                f"{comentarios} líneas con comentarios. No aparecen en el PDF; sí en los .tex si se entregan.",
                [{"archivo": rel, "linea": None, "fragmento": ""}],
                "Si entrega los .tex, revise que los comentarios puedan leerse por terceros."))
    return hallazgos


def metadatos_tex(raiz: Path) -> list[dict]:
    texto = raiz.read_text(encoding="utf-8", errors="replace")
    salida = []
    for n, linea in enumerate(texto.splitlines(), 1):
        activa = _sin_comentarios(linea)
        for m in re.finditer(r"(pdf(?:author|title|subject|keywords|creator|producer))\s*=\s*\{?([^,}]*)", activa):
            salida.append({"campo": m.group(1), "valor": m.group(2).strip()[:200], "procedencia": f"{raiz.name}:{n} (hypersetup)"})
        for cmd in ("title", "author", "date"):
            m = re.search(r"\\" + cmd + r"\s*(\{.*)", activa)
            if m:
                salida.append({"campo": f"\\{cmd}", "valor": m.group(1)[:200], "procedencia": f"{raiz.name}:{n}"})
    return salida


# ---------------------------------------------------------------- PDF
EXPLICACION_META = {
    "/Producer": "Programa que escribió el PDF (p. ej. xdvipdfmx, pdfTeX). No identifica a quien redactó el texto.",
    "/Creator": "Programa que originó el documento. No identifica a quien redactó el texto.",
    "/Author": "Autor declarado (hyperref o la clase). Revise que sea el correcto.",
    "/Title": "Título declarado.",
    "/CreationDate": "Fecha de creación del archivo. No mide el tiempo de investigación ni de redacción.",
    "/ModDate": "Fecha de última modificación del archivo.",
    "/Trapped": "Marca técnica de impresión.",
}


def _rgb(color) -> tuple[float, float, float] | None:
    if color is None:
        return (0.0, 0.0, 0.0)
    if isinstance(color, (int, float)):
        color = (color,)
    try:
        v = [float(x) for x in color]
    except (TypeError, ValueError):
        return None
    if len(v) == 1:
        return (v[0],) * 3
    if len(v) == 3:
        return tuple(v)
    if len(v) == 4:
        c, m, y, k = v
        return ((1 - c) * (1 - k), (1 - m) * (1 - k), (1 - y) * (1 - k))
    return None


def _analizar_pdf(ruta: Path):
    from pdfminer.converter import PDFLayoutAnalyzer
    from pdfminer.layout import LAParams
    from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
    from pdfminer.pdfpage import PDFPage
    from pdfminer.utils import apply_matrix_pt

    class Dispositivo(PDFLayoutAnalyzer):
        def __init__(self, rsrc):
            super().__init__(rsrc, pageno=1, laparams=LAParams())
            self.chars, self.rects, self.orden, self.render = [], [], 0, 0

        def render_string(self, textstate, seq, ncs, graphicstate):
            self.render = textstate.render
            super().render_string(textstate, seq, ncs, graphicstate)

        def render_char(self, matrix, font, fontsize, scaling, rise, cid, ncs, graphicstate):
            adv = super().render_char(matrix, font, fontsize, scaling, rise, cid, ncs, graphicstate)
            ch = self.cur_item._objs[-1]
            self.orden += 1
            self.chars.append({"t": ch.get_text(), "bbox": (ch.x0, ch.y0, ch.x1, ch.y1),
                               "tam": ch.size, "rgb": _rgb(graphicstate.ncolor),
                               "render": self.render, "orden": self.orden})
            return adv

        def paint_path(self, gstate, stroke, fill, evenodd, path):
            if fill:
                pts = [apply_matrix_pt(self.ctm, (seg[-2], seg[-1])) for seg in path
                       if len(seg) >= 3 and seg[0] in "mlc"]
                if len(pts) >= 3:
                    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
                    self.orden += 1
                    self.rects.append({"bbox": (min(xs), min(ys), max(xs), max(ys)),
                                       "rgb": _rgb(gstate.ncolor), "orden": self.orden})
            super().paint_path(gstate, stroke, fill, evenodd, path)

    rsrc = PDFResourceManager()
    dev = Dispositivo(rsrc)
    interp = PDFPageInterpreter(rsrc, dev)
    with open(ruta, "rb") as f:
        for n, pagina in enumerate(PDFPage.get_pages(f), 1):
            dev.chars, dev.rects, dev.orden = [], [], 0
            interp.process_page(pagina)
            caja = pagina.cropbox or pagina.mediabox
            yield n, caja, dev.chars, dev.rects


def _fondo(ch, rects):
    cx = (ch["bbox"][0] + ch["bbox"][2]) / 2
    cy = (ch["bbox"][1] + ch["bbox"][3]) / 2
    fondo = None
    for r in rects:
        if r["orden"] < ch["orden"] and r["rgb"] is not None:
            x0, y0, x1, y1 = r["bbox"]
            if x0 <= cx <= x1 and y0 <= cy <= y1:
                fondo = r
    return fondo


def _dist(a, b) -> float:
    return max(abs(x - y) for x, y in zip(a, b))


def texto_oculto_pdf(ruta: Path, tam_min: float = 1.0) -> tuple[list[dict], list[str]]:
    hallazgos, paginas_texto = [], []
    for n, caja, chars, rects in _analizar_pdf(ruta):
        paginas_texto.append("".join(c["t"] for c in chars))
        corridas = []
        for ch in chars:
            if not ch["t"].strip():
                if corridas and ch["orden"] - corridas[-1]["ult"] <= 1:
                    corridas[-1]["texto"] += " "
                    corridas[-1]["ult"] = ch["orden"]
                continue
            motivos = []
            if ch["render"] in (3, 7):
                motivos.append(f"modo de render {ch['render']} (no pinta el texto)")
            if ch["tam"] < tam_min:
                motivos.append(f"tamaño {ch['tam']:.2f} pt (< {tam_min} pt)")
            x0, y0, x1, y1 = ch["bbox"]
            if x1 < caja[0] or x0 > caja[2] or y1 < caja[1] or y0 > caja[3]:
                motivos.append("fuera de la caja visible de la página")
            fondo = _fondo(ch, rects)
            fondo_rgb = fondo["rgb"] if fondo else (1.0, 1.0, 1.0)
            if ch["rgb"] is not None and _dist(ch["rgb"], fondo_rgb) < 0.03:
                motivos.append("mismo color que el fondo " + ("(rectángulo pintado debajo)" if fondo
                                                             else "(sin rectángulo debajo; se supone página blanca)"))
            elif ch["rgb"] is not None and min(ch["rgb"]) >= 0.97:
                motivos.append("texto blanco sobre fondo de otro color (probablemente visible)")
            if not motivos:
                continue
            clave = tuple(motivos)
            if corridas and corridas[-1]["clave"] == clave and ch["orden"] - corridas[-1]["ult"] <= 3:
                c = corridas[-1]
                hueco = ch["bbox"][0] - c["x1"]
                if not c["texto"].endswith(" ") and (hueco > 0.15 * max(ch["tam"], 0.1)
                                                     or abs(ch["bbox"][1] - c["y0"]) > ch["tam"]):
                    c["texto"] += " "
                c["texto"] += ch["t"]
                c["ult"], c["x1"], c["y0"] = ch["orden"], ch["bbox"][2], ch["bbox"][1]
                c["n"] += 1
            else:
                corridas.append({"clave": clave, "texto": ch["t"], "ult": ch["orden"], "n": 1,
                                 "x1": ch["bbox"][2], "y0": ch["bbox"][1],
                                 "bbox": [round(v, 1) for v in ch["bbox"]], "rgb": ch["rgb"],
                                 "tam": round(ch["tam"], 2), "render": ch["render"],
                                 "fondo": fondo_rgb, "fondo_detectado": bool(fondo)})
        for c in corridas:
            probable_visible = all("probablemente visible" in m for m in c["clave"])
            hallazgos.append(_hallazgo(
                "PDF-TEXTO-OCULTO" if not probable_visible else "PDF-TEXTO-BLANCO",
                "texto oculto", "baja" if probable_visible else "alta",
                "informativo" if probable_visible else "candidato",
                "; ".join(c["clave"]),
                [{"pagina": n, "fragmento": c["texto"].strip()[:200]}],
                "Abra la página y compruebe si el texto se ve; el color solo no prueba invisibilidad.",
                {"caracteres": c["n"], "bbox_primer_caracter": c["bbox"], "color_texto_rgb": c["rgb"],
                 "color_fondo_rgb": c["fondo"], "fondo_detectado": c["fondo_detectado"],
                 "tamano_pt": c["tam"], "modo_render": c["render"], "caja_pagina": list(caja)}))
    return hallazgos, paginas_texto


def metadatos_pdf(ruta: Path) -> tuple[list[dict], list[dict]]:
    from pypdf import PdfReader
    campos, hallazgos = [], []
    try:
        lector = PdfReader(str(ruta))
    except Exception as e:
        return [], [_hallazgo("PDF-META-ERROR", "metadatos", "media", "error de lectura",
                              f"No se pudo leer el PDF: {type(e).__name__}: {e}", [], "Revise el archivo.")]
    try:
        info = lector.metadata or {}
    except Exception as e:
        info = {}
        hallazgos.append(_hallazgo("PDF-META-ERROR", "metadatos", "media", "error de lectura",
                                   f"Diccionario Info ilegible: {e}", [], "Revise el archivo."))
    for k, v in info.items():
        campos.append({"campo": str(k), "valor": str(v)[:200], "procedencia": "Info",
                       "explicacion": EXPLICACION_META.get(str(k), "")})
    if not info:
        campos.append({"campo": "(Info)", "valor": "", "procedencia": "Info",
                       "explicacion": "El PDF no declara diccionario Info (ausencia, no error)."})
    try:
        xmp = lector.xmp_metadata
    except Exception as e:
        xmp = None
        campos.append({"campo": "(XMP)", "valor": f"error de lectura: {e}", "procedencia": "XMP", "explicacion": ""})
    if xmp is not None:
        for attr in ("dc_creator", "dc_title", "dc_description", "pdf_producer", "pdf_keywords",
                     "xmp_creator_tool", "xmp_create_date", "xmp_modify_date", "xmp_metadata_date",
                     "xmpmm_document_id", "xmpmm_instance_id"):
            try:
                v = getattr(xmp, attr)
            except Exception:
                continue
            if v:
                campos.append({"campo": attr, "valor": str(v)[:200], "procedencia": "XMP", "explicacion": ""})
    else:
        campos.append({"campo": "(XMP)", "valor": "", "procedencia": "XMP", "explicacion": "Sin metadatos XMP."})
    campos.append({"campo": "versión PDF", "valor": lector.pdf_header, "procedencia": "cabecera", "explicacion": ""})
    campos.append({"campo": "páginas", "valor": str(len(lector.pages)), "procedencia": "árbol de páginas", "explicacion": ""})
    campos.append({"campo": "cifrado", "valor": str(lector.is_encrypted), "procedencia": "trailer", "explicacion": ""})
    try:
        adjuntos = list(lector.attachments)
    except Exception:
        adjuntos = []
    if adjuntos:
        hallazgos.append(_hallazgo("PDF-ADJUNTOS", "documento", "media", "confirmado",
                                   f"Archivos incrustados: {', '.join(adjuntos)[:200]}", [],
                                   "Confirme que deben ir en la entrega."))
    anot = {}
    for n, p in enumerate(lector.pages, 1):
        for a in p.get("/Annots", []) or []:
            try:
                tipo = str(a.get_object().get("/Subtype"))
            except Exception:
                tipo = "?"
            anot.setdefault(tipo, []).append(n)
    for tipo, pags in anot.items():
        if tipo in ("/Link",):
            continue
        hallazgos.append(_hallazgo("PDF-ANOTACIONES", "documento", "baja", "confirmado",
                                   f"{len(pags)} anotaciones {tipo}", [{"pagina": p} for p in pags[:20]],
                                   "Las notas o comentarios del PDF pueden contener texto que no se ve impreso."))
    return campos, hallazgos


def banderas_pdf(ruta: Path, tam_min: float = 1.0) -> dict:
    campos, hallazgos = metadatos_pdf(ruta)
    try:
        ocultos, paginas = texto_oculto_pdf(ruta, tam_min)
    except Exception as e:
        ocultos, paginas = [], []
        hallazgos.append(_hallazgo("PDF-ANALISIS-ERROR", "texto oculto", "media", "error de lectura",
                                   f"No se pudo analizar el contenido: {type(e).__name__}: {e}", [],
                                   "El análisis de texto oculto no cubre este PDF."))
    hallazgos += ocultos
    try:
        from .corpus import texto_pdf
        texto, metodo = texto_pdf(ruta)
        paginas_txt = texto.split("\f")
    except Exception as e:
        paginas_txt, metodo = [], ""
        hallazgos.append(_hallazgo("PDF-TEXTO-ERROR", "sustitución de caracteres", "media", "error de lectura",
                                   f"No se pudo extraer el texto: {type(e).__name__}: {e}", [],
                                   "La revisión de caracteres no cubre este PDF."))
    lista = [(h, {"pagina": n, "fragmento": _contexto(t, h["pos"])})
             for n, t in enumerate(paginas_txt, 1) for h in caracteres(t)]
    hallazgos += _hallazgos_car(lista, "Compruebe el carácter en la fuente; en notación matemática "
                                       "suele ser legítimo.")
    return {"metadatos": campos, "hallazgos": hallazgos, "paginas_analizadas": len(paginas),
            "extraccion_caracteres": metodo}


def ejecutar(extr: dict, base: Path, pdf: Path | None, tam_min: float = 1.0) -> dict:
    archivos = {rel: base / rel for rel in extr["archivos"]}
    salida = {"tex": {"archivos": sorted(archivos), "hallazgos": banderas_tex(archivos),
                      "metadatos_declarados": metadatos_tex(base / extr["raiz"])},
              "pdf": None, "limitaciones": [
                  "Texto oculto en PDF: se consideran color de relleno, rectángulos rellenos pintados antes, "
                  "tamaño, modo de render y caja de página. No se consideran imágenes de fondo, recortes "
                  "(clip), transparencias ni capas opcionales.",
                  "El texto blanco no se declara invisible por sí solo; se informa el fondo detectado.",
                  "Un carácter que la fuente tipográfica no tiene (p. ej. cirílico con Latin Modern) no llega "
                  "al PDF: la sustitución de caracteres se revisa también en los .tex.",
                  "En los .tex se buscan patrones; las macros propias que oculten texto pueden no detectarse.",
                  "No se buscan marcas de agua estadísticas de modelos de lenguaje: capacidad no disponible "
                  "(no es un resultado negativo).",
              ]}
    if pdf:
        if Path(pdf).exists():
            salida["pdf"] = {"archivo": Path(pdf).name, **banderas_pdf(Path(pdf), tam_min)}
        else:
            salida["pdf"] = {"archivo": str(pdf), "error": "no existe", "metadatos": [], "hallazgos": []}
    return salida
