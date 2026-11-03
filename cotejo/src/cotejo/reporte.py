"""Reporte: reporte.html autocontenido, reporte.json y summary.md."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from html import escape
from pathlib import Path

from . import __version__
from .texto import palabras

COLORES = ["#f4a261", "#7fb3d5", "#a3d9a5", "#e9a3c9", "#f6e27a", "#c3aed6", "#f19c99",
           "#9fd8cb", "#d4b483", "#b5c7e8", "#e6b0aa", "#c5e1a5"]
LIMITACIONES = [
    "El índice compara solo contra el corpus local; no es una comparación universal ni equivale al "
    "porcentaje del servicio comercial que use la universidad, con otro corpus (web, publicaciones, "
    "trabajos entregados), otra normalización y otros filtros.",
    "Fuentes no descargadas o de acceso cerrado no se cotejaron; vea la sección de cobertura.",
    "La coincidencia es literal tras normalizar (minúsculas, sin acentos). La traducción y la paráfrasis "
    "no se detectan con shingles; el módulo de paráfrasis es opcional y no entra al índice.",
    "Las fuentes en otro idioma solo coinciden si el documento las copia en ese idioma.",
    "Que una fuente esté citada no vuelve aceptable una copia literal sin comillas; que no lo esté no "
    "prueba plagio (puede ser una frase común o terminología).",
    "El texto se extrae de los .tex: macros propias no se expanden y la portada generada por la clase "
    "no se incluye.",
]


def _e(x) -> str:
    return escape("" if x is None else str(x), quote=True)


def _cargar(ruta: Path):
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else None


def cobertura(extr: dict, manifiesto: dict | None) -> dict:
    fuentes = (manifiesto or {}).get("fuentes", {})
    claves_bib = set(extr.get("claves_bib", []))
    citadas = list(extr.get("citadas", []))
    ok = {c for c, r in fuentes.items() if r.get("estado") == "ok"}
    return {
        "referencias_citadas": len(citadas),
        "referencias_en_bib": len(claves_bib),
        "citadas_en_corpus": sorted(c for c in citadas if c in ok),
        "citadas_con_error": [{"clave": c, "error": fuentes[c].get("error", ""), "origen": fuentes[c].get("origen", "")}
                              for c in citadas if c in fuentes and c not in ok],
        "citadas_sin_fuente": sorted(c for c in citadas if c not in fuentes),
        "propias": sorted(c for c in ok if fuentes[c].get("tipo") == "propio"),
        "otras": sorted(c for c in ok if c not in citadas and fuentes[c].get("tipo") != "propio"),
        "avisos": [{"clave": c, "aviso": r["aviso"]} for c, r in fuentes.items() if r.get("aviso")],
        "palabras_corpus": sum(r.get("palabras", 0) for c, r in fuentes.items() if c in ok),
        "licencias": {c: r.get("licencia", "") for c, r in fuentes.items() if c in ok},
    }


def _texto_resaltado(extr: dict, sim: dict | None, colores: dict) -> str:
    marcas = {}
    if sim:
        for a, b, c in sim["marcas"]:
            for i in range(a, b):
                marcas[i] = c
    partes, gi, archivo_actual = [], 0, None
    for s in extr["segmentos"]:
        if s["archivo"] != archivo_actual:
            if archivo_actual is not None:
                partes.append("</details>")
            archivo_actual = s["archivo"]
            partes.append(f"<details><summary>{_e(archivo_actual)}</summary>")
        texto = s["texto"]
        offs = palabras(texto)
        html, cur, abierta = [], 0, None
        for k, (_, a, b) in enumerate(offs):
            fuente = marcas.get(gi + k)
            if fuente != abierta:
                if abierta is not None:
                    html.append("</mark>")
                html.append(_e(texto[cur:a]))
                if fuente is not None:
                    html.append(f'<mark style="background:{colores.get(fuente, "#ddd")}" title="{_e(fuente)}">')
                abierta = fuente
            else:
                html.append(_e(texto[cur:a]))
            html.append(_e(texto[a:b]))
            cur = b
        html.append(_e(texto[cur:]))
        if abierta is not None:
            html.append("</mark>")
        clase = "seg" + (" con" if any(gi + k in marcas for k in range(len(offs))) else "")
        gi += len(offs)
        partes.append(f'<p class="{clase} t-{_e(s["tipo"])}" id="seg-{s["id"]}">'
                      f'<span class="loc">{_e(s["archivo"])}:{s["linea_ini"]}</span> {"".join(html)}</p>')
    if archivo_actual is not None:
        partes.append("</details>")
    return "\n".join(partes)


CSS = """
:root{--fondo:#fff;--texto:#1d1d1f;--tenue:#6b6b70;--borde:#ddd;--caja:#f6f6f8;--alerta:#b3261e}
@media (prefers-color-scheme:dark){:root{--fondo:#17171a;--texto:#e8e8ea;--tenue:#a0a0a8;--borde:#3a3a40;--caja:#222227;--alerta:#ff8a80}}
body{background:var(--fondo);color:var(--texto);font:15px/1.5 system-ui,sans-serif;max-width:1100px;margin:0 auto;padding:16px}
h1{font-size:1.5em}h2{border-bottom:1px solid var(--borde);padding-bottom:4px;margin-top:2em}
table{border-collapse:collapse;width:100%;font-size:.9em;display:block;overflow-x:auto}
td,th{border:1px solid var(--borde);padding:4px 6px;vertical-align:top;text-align:left}
th{background:var(--caja)}.num{text-align:right;font-variant-numeric:tabular-nums}
.grande{font-size:2.2em;font-weight:700}.tenue{color:var(--tenue)}.caja{background:var(--caja);padding:8px 12px;border-radius:6px}
.loc{font-family:ui-monospace,monospace;font-size:.75em;color:var(--tenue);margin-right:.4em}
mark{color:#111;border-radius:2px}.sin{color:var(--alerta);font-weight:600}
p.seg{margin:.35em 0}p.t-titulo{font-weight:700}details{margin:.3em 0}summary{cursor:pointer}
.par{display:grid;grid-template-columns:1fr 1fr;gap:8px}@media (max-width:700px){.par{grid-template-columns:1fr}}
.cuadro{display:inline-block;width:.9em;height:.9em;border-radius:2px;vertical-align:middle}
"""


def _tabla(filas: list[list], cabecera: list[str], num: set[int] = frozenset()) -> str:
    h = "".join(f"<th>{_e(c)}</th>" for c in cabecera)
    cuerpo = "".join("<tr>" + "".join(f'<td class="num">{c}</td>' if i in num else f"<td>{c}</td>"
                                      for i, c in enumerate(f)) + "</tr>" for f in filas)
    return f"<table><thead><tr>{h}</tr></thead><tbody>{cuerpo}</tbody></table>"


def generar(salida: Path, cache: Path | None = None) -> dict:
    salida = Path(salida)
    extr = _cargar(salida / "extraccion.json")
    if extr is None:
        raise FileNotFoundError("Falta extraccion.json; corra primero «cotejo extraer».")
    sim = _cargar(salida / "similitud.json")
    ban = _cargar(salida / "banderas.json")
    det = _cargar(salida / "detectores.json")
    web = _cargar(salida / "web_muestra.json")
    cache = Path(cache) if cache else (Path(sim["corpus_cache"]) if sim and sim.get("corpus_cache") else None)
    manifiesto = _cargar(cache / "manifiesto.json") if cache else None
    cob = cobertura(extr, manifiesto)
    fecha = datetime.now(timezone.utc).isoformat(timespec="seconds")
    colores = {f["clave"]: COLORES[i % len(COLORES)] for i, f in enumerate((sim or {}).get("fuentes", []))}

    hallazgos = []
    if ban:
        hallazgos += ban["tex"]["hallazgos"]
        if ban.get("pdf"):
            hallazgos += ban["pdf"].get("hallazgos", [])

    datos = {
        "schema_version": "1.0", "herramienta": f"cotejo {__version__}", "fecha": fecha,
        "raiz": extr["raiz"], "archivos": extr["archivos"],
        "extraccion": {"segmentos": len(extr["segmentos"]),
                       "palabras": sum(len(s["palabras"]) for s in extr["segmentos"]),
                       "faltantes": extr["faltantes"], "ciclos": extr["ciclos"],
                       "citas_sin_entrada": extr.get("citas_sin_entrada", [])},
        "cobertura": cob,
        "similitud": None if sim is None else {k: sim[k] for k in sim if k != "marcas"},
        "banderas": ban, "detectores": det, "muestra_web": web,
        "limitaciones": LIMITACIONES,
    }
    (salida / "reporte.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")

    h = [f"<!doctype html><html lang=\"es\"><head><meta charset=\"utf-8\">"
         f"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
         f"<title>Cotejo de similitud</title><style>{CSS}</style></head><body>",
         "<h1>Cotejo local de similitud e integridad</h1>",
         f"<p class=\"tenue\">{_e(extr['raiz'])} · cotejo {__version__} · {_e(fecha)}</p>",
         "<div class=\"caja\">Este reporte no reproduce el servicio comercial de similitud que use la "
         "universidad ni sustituye su revisión. Ningún porcentaje de aquí equivale al suyo y ningún "
         "detector prueba autoría.</div>"]

    h.append("<h2>Índice de similitud</h2>")
    if sim:
        h.append(f"<p><span class=\"grande\">{sim['indice']:.1f} %</span> "
                 f"<span class=\"tenue\">({sim['palabras_coincidentes']} de {sim['palabras_documento']} palabras; "
                 f"{_e(sim['filtros_nombre'])}; corpus de {len(sim['fuentes_cotejadas'])} fuentes)</span></p>")
        fd = sim["fuente_definicion"]
        h.append(f"<p>{_e(sim['definicion'])}</p><p class=\"tenue\">{_e(fd['nota'])} "
                 f"Referencia: <a href=\"{_e(fd['url'])}\">{_e(fd['url'])}</a></p>")
        h.append(_tabla([[_e(v["nombre"]) + (" <b>(elegido)</b>" if v["elegido"] else ""),
                          v["palabras_documento"], v["palabras_coincidentes"], f"{v['indice']:.2f} %"]
                         for v in sim["indices"]],
                        ["Filtros", "Palabras consideradas", "Coincidentes", "Índice"], {1, 2, 3}))
        p = sim["parametros"]
        h.append(f"<p class=\"tenue\">Shingles de {p['n_shingle']} palabras; huecos de hasta {p['hueco']} "
                 f"palabras dentro de un pasaje; shingles con más de {p['max_ocurrencias']} apariciones en el "
                 f"corpus se ignoran. Normalización: {_e(p['normalizacion'])}.</p>")
    else:
        h.append("<p class=\"sin\">No se corrió la similitud.</p>")

    h.append("<h2>Cobertura del corpus</h2>")
    h.append(_tabla([
        ["Referencias citadas en el documento", cob["referencias_citadas"]],
        ["… con texto en el corpus", len(cob["citadas_en_corpus"])],
        ["… con descarga o extracción fallida", len(cob["citadas_con_error"])],
        ["… sin fuente en la lista ni PDF local", len(cob["citadas_sin_fuente"])],
        ["Fuentes propias (autoplagio)", len(cob["propias"])],
        ["Otras fuentes del corpus (no citadas)", len(cob["otras"])],
        ["Palabras en el corpus", cob["palabras_corpus"]]], ["Concepto", "Cantidad"], {1}))
    if cob["citadas_sin_fuente"] or cob["citadas_con_error"]:
        h.append("<details><summary>Fuentes no cotejadas</summary><ul>"
                 + "".join(f"<li><code>{_e(c)}</code>: sin fuente</li>" for c in cob["citadas_sin_fuente"])
                 + "".join(f"<li><code>{_e(x['clave'])}</code>: {_e(x['error'])}</li>" for x in cob["citadas_con_error"])
                 + "</ul></details>")
    for a in cob["avisos"]:
        h.append(f"<p class=\"tenue\"><code>{_e(a['clave'])}</code>: {_e(a['aviso'])}</p>")
    h.append("<p class=\"tenue\">No cubre: la web abierta, bases de trabajos entregados, publicaciones de "
             "acceso cerrado ni fuentes en otros idiomas salvo copia literal en ese idioma.</p>")

    if sim:
        h.append("<h2>Fuentes coincidentes</h2>")
        h.append(_tabla([[f"<span class=\"cuadro\" style=\"background:{colores[f['clave']]}\"></span> <code>{_e(f['clave'])}</code>"
                          + (f"<br><span class=\"tenue\">{_e(f['titulo'])}</span>" if f["titulo"] else ""),
                          _e(f["tipo"]), f"{f['porcentaje_primario']:.2f} %", f"{f['porcentaje']:.2f} %",
                          f["pasajes"], (f"<span class=\"sin\">{f['pasajes_sin_cita']}</span>" if f["pasajes_sin_cita"] else "0"),
                          {True: "sí", False: "<span class=\"sin\">no</span>", None: "n/a"}[f["citada_en_documento"]]]
                         for f in sim["fuentes"]],
                        ["Fuente", "Tipo", "% atribuido", "% con solapes", "Pasajes", "Sin cita", "Citada en el documento"],
                        {2, 3, 4, 5}))
        h.append("<p class=\"tenue\">«% atribuido»: cada palabra cuenta solo para la fuente con más coincidencias "
                 "(suman el índice). «% con solapes»: todas las palabras que coinciden con esa fuente.</p>")
        h.append("<h2>Pasajes coincidentes</h2><p class=\"tenue\">Ordenados por gravedad: primero lo que "
                 "coincide sin cita en el párrafo.</p>")
        contados = [p for p in sim["pasajes"] if p["palabras_contadas"]]
        for p in contados[:400]:
            estado = p["estado_cita"]
            h.append(f"<details><summary><span class=\"{'sin' if estado == 'sin cita' else ''}\">{_e(estado)}</span> · "
                     f"<code>{_e(p['fuente'])}</code> · <a href=\"#seg-{p['segmentos'][0]}\">{_e(p['archivo'])}:{p['linea']}</a> · "
                     f"{p['palabras_contadas']} palabras · alineación {p['razon_alineacion']:.2f}"
                     + (f" · {int(p['fraccion_entre_comillas'] * 100)} % entre comillas" if p["fraccion_entre_comillas"] else "")
                     + f"</summary><div class=\"par\"><div><b>Documento</b><br>{_e(p['texto_documento'])}</div>"
                     f"<div><b>Fuente</b><br>{_e(p['texto_fuente'])}</div></div></details>")
        if len(contados) > 400:
            h.append(f"<p class=\"tenue\">… {len(contados) - 400} pasajes más en reporte.json.</p>")
        par = sim.get("parafrasis")
        h.append("<h2>Paráfrasis cercana (no entra al índice)</h2>")
        if par and par.get("disponible"):
            h.append(f"<p class=\"tenue\">{_e(par.get('nota', ''))} Modelo: {_e(par.get('modelo', ''))}</p>")
            h.append(_tabla([[f"{x['coseno']:.3f}", f"<code>{_e(x['fuente'])}</code>", _e(f"{x['archivo']}:{x['linea']}"),
                              _e(x["texto_documento"]), _e(x["texto_fuente"])] for x in par["pares"]],
                            ["Coseno", "Fuente", "Ubicación", "Documento", "Fuente"], {0}))
        else:
            h.append(f"<p class=\"tenue\">Desactivada: {_e((par or {}).get('motivo', 'no se pidió (--parafrasis)'))}</p>")

    h.append("<h2>Texto con coincidencias resaltadas</h2><p class=\"tenue\">Cada párrafo indica archivo y "
             "línea de inicio en la fuente LaTeX.</p>")
    h.append(_texto_resaltado(extr, sim, colores))

    h.append("<h2>Alertas de integridad</h2>")
    if ban:
        orden = {"alta": 0, "media": 1, "baja": 2, "informativa": 3}
        filas = []
        for x in sorted(hallazgos, key=lambda x: (orden.get(x["prioridad"], 9), x["regla"])):
            ub = "; ".join(f"{u.get('archivo') or ''}{':' + str(u['linea']) if u.get('linea') else ''}"
                           f"{'p. ' + str(u['pagina']) if u.get('pagina') else ''}" for u in x["ubicaciones"][:5])
            frag = x["ubicaciones"][0].get("fragmento", "") if x["ubicaciones"] else ""
            filas.append([_e(x["prioridad"]), _e(x["estado_evidencia"]), f"<code>{_e(x['regla'])}</code>",
                          _e(x["mensaje"]), _e(ub), f"<code>{_e(frag)}</code>",
                          _e(json.dumps(x.get("evidencia") or {}, ensure_ascii=False)), _e(x["recomendacion"])])
        h.append(_tabla(filas, ["Prioridad", "Evidencia", "Regla", "Mensaje", "Ubicación", "Fragmento",
                                "Datos", "Qué hacer"]) if filas else "<p>Sin alertas en lo revisado.</p>")
        if ban.get("pdf"):
            pdf = ban["pdf"]
            h.append(f"<h3>Metadatos del PDF {_e(pdf.get('archivo'))}</h3>")
            if pdf.get("error"):
                h.append(f"<p class=\"sin\">{_e(pdf['error'])}</p>")
            h.append(_tabla([[_e(c["campo"]), _e(c["valor"]), _e(c["procedencia"]), _e(c.get("explicacion", ""))]
                             for c in pdf.get("metadatos", [])], ["Campo", "Valor", "Procedencia", "Nota"]))
            h.append(f"<p class=\"tenue\">Páginas analizadas: {pdf.get('paginas_analizadas', 0)}.</p>")
        else:
            h.append("<p class=\"sin\">No se analizó ningún PDF (use --pdf). Solo se revisaron los .tex.</p>")
        if ban["tex"].get("metadatos_declarados"):
            h.append("<h3>Metadatos declarados en la fuente</h3>")
            h.append(_tabla([[_e(c["campo"]), _e(c["valor"]), _e(c["procedencia"])]
                             for c in ban["tex"]["metadatos_declarados"]], ["Campo", "Valor", "Procedencia"]))
        h.append("<ul>" + "".join(f"<li class=\"tenue\">{_e(l)}</li>" for l in ban["limitaciones"]) + "</ul>")
    else:
        h.append("<p class=\"sin\">No se corrieron las alertas.</p>")

    h.append("<h2>Detectores abiertos de texto generado</h2>")
    h.append("<div class=\"caja\"><b>Léase antes de mirar números.</b><ul>"
             + "".join(f"<li>{_e(l)}</li>" for l in (det or {}).get("limitaciones", []) or ["Módulo no ejecutado."])
             + "</ul></div>")
    if det and det.get("disponible"):
        h.append("<p>Métodos: " + "; ".join(f"{_e(m['nombre'])} ({_e(m['referencia'])}, {_e(m['codigo'])}): {_e(m['direccion'])}"
                                            for m in det["metodos"]) + "</p>")
        h.append(f"<p class=\"tenue\">Modelos: {_e(json.dumps(det['modelos'], ensure_ascii=False))}; "
                 f"dispositivo {_e(det['dispositivo'])}; párrafos de al menos {det['parametros']['min_palabras']} "
                 f"palabras, truncados a {det['parametros']['max_tokens']} tokens.</p>")
        if det.get("aviso_referencia"):
            h.append(f"<p class=\"sin\">{_e(det['aviso_referencia'])}</p>")
        ref = det.get("referencia")
        cab = ["Sección", "Párrafos", "Binoculars (mediana)", "Fast-DetectGPT (mediana)"]
        if ref:
            cab += ["Bino.: pos. en humano", "Bino.: pos. en generado", "F-DGPT: pos. en humano", "F-DGPT: pos. en generado"]
        filas = []
        for s in det["secciones"]:
            f = [_e(s["seccion"]), s["parrafos"], _e(s["binoculars_mediana"]), _e(s["fast_detectgpt_mediana"])]
            if ref:
                f += [_e(s.get(f"pos_{m}_{g}")) for m in ("binoculars", "fast_detectgpt") for g in ("humano", "generado")]
            filas.append(f)
        h.append(_tabla(filas, cab, set(range(1, len(cab)))))
        if ref:
            h.append("<p class=\"tenue\">«pos.» = percentil del valor dentro de los puntajes del conjunto de "
                     "referencia indicado. Referencia: " + "; ".join(
                         f"{_e(g)}: {d['parrafos']} párrafos de {d['archivos']} archivos" for g, d in ref["grupos"].items()) + ".</p>")
        h.append("<details><summary>Puntajes por párrafo</summary>")
        h.append(_tabla([[f"<a href=\"#seg-{p['segmento']}\">{_e(p['archivo'])}:{p['linea']}</a>", p["tokens"],
                          _e(None if p["binoculars"] is None else round(p["binoculars"], 4)),
                          _e(None if p["fast_detectgpt"] is None else round(p["fast_detectgpt"], 4))]
                         for p in det["parrafos"]], ["Párrafo", "Tokens", "Binoculars", "Fast-DetectGPT"], {1, 2, 3}))
        h.append("</details>")
    else:
        h.append(f"<p class=\"tenue\">No disponible: {_e((det or {}).get('motivo', 'no se corrió «cotejo detectar»'))}</p>")

    h.append("<h2>Limitaciones</h2><ul>" + "".join(f"<li>{_e(l)}</li>" for l in LIMITACIONES) + "</ul>")
    h.append("</body></html>")
    (salida / "reporte.html").write_text("\n".join(h), encoding="utf-8")
    (salida / "summary.md").write_text(_resumen_md(datos, sim, hallazgos, det, cob), encoding="utf-8")
    return datos


def _resumen_md(datos, sim, hallazgos, det, cob) -> str:
    l = ["# Resumen del cotejo", "", f"- Documento: `{datos['raiz']}` ({datos['extraccion']['palabras']} palabras extraídas)",
         f"- Herramienta: {datos['herramienta']}, {datos['fecha']}", ""]
    l += ["## Similitud (corpus local)", ""]
    if sim:
        l.append(f"- Índice: **{sim['indice']:.1f} %** ({sim['filtros_nombre']}). No equivale al del servicio comercial que use la universidad.")
        for v in sim["indices"]:
            l.append(f"  - {v['nombre']}: {v['indice']:.2f} %")
        sin = [p for p in sim["pasajes"] if p["estado_cita"] == "sin cita" and p["palabras_contadas"]]
        l.append(f"- Pasajes que coinciden **sin cita** en su párrafo: {len(sin)}")
        for p in sin[:10]:
            l.append(f"  - `{p['archivo']}:{p['linea']}` ↔ `{p['fuente']}` ({p['palabras_contadas']} palabras)")
        orden = sorted(sim["fuentes"], key=lambda f: -f["porcentaje_primario"])
        l.append("- Fuentes con más palabras atribuidas: " + ", ".join(
            f"`{f['clave']}` {f['porcentaje_primario']:.1f} %" for f in orden[:8]))
    else:
        l.append("- No se corrió.")
    l += ["", "## Cobertura", "",
          f"- Referencias citadas: {cob['referencias_citadas']}; con texto en el corpus: {len(cob['citadas_en_corpus'])}; "
          f"fallidas: {len(cob['citadas_con_error'])}; sin fuente: {len(cob['citadas_sin_fuente'])}.",
          f"- Fuentes propias: {len(cob['propias'])}.", ""]
    l += ["## Alertas de integridad", ""]
    cuenta = {}
    for x in hallazgos:
        cuenta[x["prioridad"]] = cuenta.get(x["prioridad"], 0) + 1
    l.append("- " + (", ".join(f"{k}: {v}" for k, v in sorted(cuenta.items())) or "sin alertas en lo revisado"))
    for x in [x for x in hallazgos if x["prioridad"] == "alta"][:10]:
        u = x["ubicaciones"][0] if x["ubicaciones"] else {}
        l.append(f"  - {x['regla']}: {x['mensaje']} ({u.get('archivo', '')}{':' + str(u['linea']) if u.get('linea') else ''}"
                 f"{' p. ' + str(u['pagina']) if u.get('pagina') else ''})")
    pdf = (datos.get("banderas") or {}).get("pdf")
    if not pdf:
        l.append("- No se analizó PDF.")
    l += ["", "## Detectores", ""]
    if det and det.get("disponible"):
        l.append(f"- {len(det['parrafos'])} párrafos puntuados con {', '.join(det['modelos'].values())}.")
        l.append("- " + (det.get("aviso_referencia") or "Con conjunto de referencia: ver posiciones en el HTML."))
        l.append("- Ningún puntaje es prueba de autoría.")
    else:
        l.append(f"- No disponible: {(det or {}).get('motivo', 'no se corrió')}.")
    l += ["", "## Limitaciones", ""] + [f"- {x}" for x in LIMITACIONES]
    return "\n".join(l) + "\n"
