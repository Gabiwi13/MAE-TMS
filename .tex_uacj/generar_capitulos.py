"""Escribe los capítulos 2 a 5 de la plantilla UACJ a partir de la tesis en ../.tex8.

No cambia el texto: lo reparte entre los archivos de la plantilla, ajusta el nivel de los
títulos y, en las remisiones a lo que aquí es capítulo, cambia «Sección» por «Capítulo».
Los demás .tex de esta carpeta son contenido propio y el script no los escribe; el 01 de
la tesis lo reemplazan Introduccion.tex y Capitulo1.tex.
Uso: python generar_capitulos.py
"""
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ORIGEN = AQUI.parent / ".tex8"
SECCIONES = ORIGEN / "secciones"

GENERADOS = ["Capitulo2.tex", "Capitulo3.tex", "Capitulo4.tex", "Capitulo5.tex"]
REEMPLAZADOS = {"01_introduccion.tex"}
NIVELES = ["chapter", "section", "subsection", "subsubsection"]
RE_TITULO = re.compile(r"^(\s*)\\(chapter|section|subsection|subsubsection)(\*?)(?=[\[{])", re.M)
CABECERA = "% Generado por generar_capitulos.py a partir de ../.tex8; no editar a mano\n"


def leer(ruta):
    return ruta.read_text(encoding="utf-8")


def escribir(nombre, texto):
    if nombre not in GENERADOS:
        raise ValueError(f"{nombre} es contenido propio; el generador no lo escribe")
    texto = re.sub(r"\n{3,}", "\n\n", texto).strip() + "\n"
    (AQUI / nombre).write_text(CABECERA + texto, encoding="utf-8", newline="\n")
    print(f"escrito {nombre}")


def mover_niveles(texto, delta):
    """delta = -1 sube un nivel (\\subsection -> \\section). \\paragraph no se toca."""
    def cambio(m):
        i = NIVELES.index(m.group(2)) + delta
        if not 0 <= i < len(NIVELES):
            raise ValueError(f"nivel fuera de rango: {m.group(0)!r}")
        return f"{m.group(1)}\\{NIVELES[i]}{m.group(3)}"
    return RE_TITULO.sub(cambio, texto)


def quitar_encabezado(texto):
    """Quita '\\section{...}' y su '\\label{...}' del inicio; devuelve (label, cuerpo)."""
    m = re.match(r"\s*\\section\{[^}]*\}\s*\\label\{([^}]*)\}\s*\n", texto)
    if not m:
        raise ValueError("el archivo no empieza con \\section{...}\\label{...}")
    return m.group(1), texto[m.end():]


def partir(texto, marca):
    """Parte el texto en la única línea que empieza con `marca`."""
    pos = [m.start() for m in re.finditer(r"^" + re.escape(marca), texto, re.M)]
    if len(pos) != 1:
        raise ValueError(f"se esperaba una sola aparición de {marca!r}, hay {len(pos)}")
    return texto[:pos[0]], texto[pos[0]:]


def quitar_linea(texto, linea):
    antes, despues = partir(texto, linea)
    return antes, despues[len(linea):]


# Etiquetas de .tex8 que aquí quedan en un \chapter.
ETQ_CAPITULO = [quitar_encabezado(leer(SECCIONES / f))[0]
                for f in ["02_marco_teorico.tex", "07_conclusiones.tex"]]
ALT_CAPITULO = "|".join(map(re.escape, ETQ_CAPITULO))
RE_REMISION = re.compile(r"Secci[óo]n(~|\s+)\\ref\{(" + ALT_CAPITULO + r")\}")


def remisiones(texto):
    return RE_REMISION.sub(r"Capítulo\1\\ref{\2}", texto)


# ---------------------------------------------------------------- 02
etq02, cuerpo02 = quitar_encabezado(leer(SECCIONES / "02_marco_teorico.tex"))
escribir("Capitulo2.tex",
         f"\\chapter{{Marco Teórico}}\n\\label{{{etq02}}}\n"
         "% <- 02\n" + remisiones(mover_niveles(cuerpo02, -1)))

# ---------------------------------------------------------------- 03 y 04
etq03, cuerpo03 = quitar_encabezado(leer(SECCIONES / "03_arquitectura.tex"))
producto, resto03 = partir(cuerpo03, r"\subsection{Diagramas de flujo}")
etq04, cuerpo04 = quitar_encabezado(leer(SECCIONES / "04_metodologia.tex"))
# La apertura (las cinco fases y las métricas) queda dentro de «Descripción de la
# metodología»; cada fase sube a \section y sus métodos a \subsection.
apertura04, resto04 = partir(cuerpo04, r"\subsection{Fase 1: prototipo de tres módulos}")

escribir("Capitulo3.tex", remisiones(
         "\\chapter{Desarrollo del Proyecto}\\label{cap:desarrollo}\n\n"
         f"\\section{{Producto propuesto}}\n\\label{{{etq03}}}\n"
         "% <- 03\n" + producto + resto03 +
         f"\n\\section{{Descripción de la metodología}}\n\\label{{{etq04}}}\n"
         "% <- 04\n" + apertura04 + mover_niveles(resto04, -1)))

# ---------------------------------------------------------------- 05 y 06
etq05, cuerpo05 = quitar_encabezado(leer(SECCIONES / "05_resultados.tex"))
etq06, cuerpo06 = quitar_encabezado(leer(SECCIONES / "06_discusion.tex"))
escribir("Capitulo4.tex", remisiones(
         "\\chapter{Resultados y Discusiones}\\label{cap:resultados}\n\n"
         f"\\section{{Resultados}}\n\\label{{{etq05}}}\n% <- 05\n" + cuerpo05 +
         f"\n\\section{{Discusiones}}\n\\label{{{etq06}}}\n% <- 06\n" + cuerpo06))

# ---------------------------------------------------------------- 07
PARRAFO_RESPUESTA = r"\paragraph{Respuesta a la pregunta de investigación.}"
PARRAFO_FUTURO = r"\paragraph{Trabajo futuro.}"
etq07, cuerpo07 = quitar_encabezado(leer(SECCIONES / "07_conclusiones.tex"))
apertura07, resto07 = quitar_linea(cuerpo07, PARRAFO_RESPUESTA)
respuesta07, futuro07 = quitar_linea(resto07, PARRAFO_FUTURO)
escribir("Capitulo5.tex", remisiones(
         f"\\chapter{{Conclusiones}}\\label{{conclusiones}}\n\\label{{{etq07}}}\n"
         "% <- 07\n" + apertura07 +
         "\n\\section{Con respecto a las preguntas de investigación}\n"
         "% <- 07, «Respuesta a la pregunta de investigación» hasta antes de «Trabajo futuro»\n"
         + respuesta07.lstrip() +
         "\n\\section{Con respecto al objetivo general}\n"
         "\\input{ConclusionObjetivoGeneral}\n\n"
         "\\section{Recomendaciones para trabajo a futuro}\n"
         "% <- 07, «Trabajo futuro» y párrafo final\n" + futuro07.lstrip() +
         "\n\\section{Difusión y productos derivados}\n"
         "\\input{Difusion}\n"))

# Una remisión a capítulo con otra palabra delante (p. ej. «Secciones») se revisa a mano.
for nombre in GENERADOS:
    for m in re.finditer(r"(\w*)[~\s]+\\ref\{(" + ALT_CAPITULO + r")\}", leer(AQUI / nombre)):
        if m.group(1) != "Capítulo":
            raise ValueError(f"{nombre}: remisión a capítulo sin «Capítulo»: {m.group(0)!r}")


# ---------------------------------------------------------------- verificación
def normal(linea):
    linea = RE_TITULO.sub(lambda m: m.group(1) + "\\TIT" + m.group(3), remisiones(linea))
    return linea.strip()


# Títulos de .tex8 que la plantilla sustituye por los suyos.
ESPERADAS = {PARRAFO_RESPUESTA, PARRAFO_FUTURO}
for f in SECCIONES.glob("*.tex"):
    ESPERADAS.add(normal(re.match(r"\s*(\\section\{[^}]*\})", leer(f)).group(1)))

salida = {normal(l) for f in GENERADOS for l in leer(AQUI / f).split("\n")}
faltan, reemplazadas = [], 0
for f in sorted(SECCIONES.glob("*.tex")):
    for l in leer(f).split("\n"):
        n = normal(l)
        if not n:
            continue
        if f.name in REEMPLAZADOS:
            reemplazadas += 1
        elif n not in salida and n not in ESPERADAS:
            faltan.append(f"{f.name}: {n}")
print(f"líneas de {', '.join(sorted(REEMPLAZADOS))} reemplazadas por contenido propio: {reemplazadas}")
print(f"líneas de .tex8 que no aparecen en la salida: {len(faltan)}")
for x in faltan:
    print("  ", x)
sys.exit(1 if faltan else 0)
