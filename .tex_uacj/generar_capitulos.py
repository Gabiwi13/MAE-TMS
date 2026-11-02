"""Escribe los capítulos de la plantilla UACJ a partir de la tesis en ../.tex8.

No cambia el texto: lo reparte entre los archivos de la plantilla y ajusta el nivel
de los títulos. Lo que no tiene origen queda como [PENDIENTE: ...].
Uso: python generar_capitulos.py
"""
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ORIGEN = AQUI.parent / ".tex8"
SECCIONES = ORIGEN / "secciones"

NIVELES = ["chapter", "section", "subsection", "subsubsection"]
RE_TITULO = re.compile(r"^(\s*)\\(chapter|section|subsection|subsubsection)(\*?)(?=[\[{])", re.M)
CABECERA = "% Generado por generar_capitulos.py a partir de ../.tex8\n"


def leer(ruta):
    return ruta.read_text(encoding="utf-8")


def escribir(nombre, texto):
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


def entre(texto, inicio, fin):
    i = texto.index(inicio) + len(inicio)
    return texto[i:texto.index(fin, i)]


# ---------------------------------------------------------------- 01
_, cuerpo01 = quitar_encabezado(leer(SECCIONES / "01_introduccion.tex"))
antes_cita, resto = partir(cuerpo01, r"\begin{quote}")
cita, despues_cita = partir(resto, r"\end{quote}")
cita += r"\end{quote}" + "\n"
despues_cita = despues_cita[len(r"\end{quote}"):]

# La frase que abre la pregunta empieza después de la última línea terminada en punto.
lineas = antes_cita.rstrip().split("\n")
if not lineas[-1].rstrip().endswith(":"):
    raise ValueError("el párrafo antes de la pregunta no termina en ':'")
k = len(lineas) - 1
while k > 0 and not lineas[k - 1].rstrip().endswith("."):
    k -= 1
marco01 = "\n".join(lineas[:k]) + "\n"
entrada_pregunta = "\n".join(lineas[k:]) + "\n"

escribir("Introduccion.tex",
         "\\chapter*{Introducción}\\label{introduccion}\\label{sec:introduccion}\n"
         "\\thispagestyle{empty}\n"
         "[PENDIENTE: recortar a una cuartilla]\n\n"
         "% <- 01, párrafos antes de la pregunta de investigación\n"
         + marco01)

escribir("Capitulo1.tex",
         "\\chapter{Planteamiento del Problema}\\label{cap:pp}\n"
         "\\section{Antecedentes}\n"
         "% <- 01 sin la pregunta (los primeros párrafos se repiten en la Introducción)\n"
         + marco01 + "\n" + despues_cita +
         "\n\\section{Definición del problema}\n"
         "% <- 01, pregunta de investigación\n"
         + entrada_pregunta + "\n" + cita +
         "\n\\section{Objetivo general}\\label{secc:og}\n"
         "[PENDIENTE: redactar desde las contribuciones de 01]\n\n"
         "\\subsection{Objetivos específicos}\n"
         "[PENDIENTE: redactar desde las contribuciones de 01]\n\n"
         "\\section{Justificación}\n"
         "[PENDIENTE]\n\n"
         "\\section{Alcances y limitaciones}\n"
         "[PENDIENTE: redactar alcances y limitaciones. Las limitaciones (a)--(j) están en "
         "la Sección~\\ref{sec:limitaciones}.]\n")

# ---------------------------------------------------------------- 02
etq02, cuerpo02 = quitar_encabezado(leer(SECCIONES / "02_marco_teorico.tex"))
escribir("Capitulo2.tex",
         f"\\chapter{{Marco Teórico}}\n\\label{{{etq02}}}\n"
         "% <- 02\n" + mover_niveles(cuerpo02, -1))

# ---------------------------------------------------------------- 03 y 04
etq03, cuerpo03 = quitar_encabezado(leer(SECCIONES / "03_arquitectura.tex"))
producto, resto03 = partir(cuerpo03, r"\subsection{Diagramas de flujo}")
etq04, cuerpo04 = quitar_encabezado(leer(SECCIONES / "04_metodologia.tex"))
apertura04, resto04 = partir(cuerpo04, r"\subsection{Conjunto de datos}")

escribir("Capitulo3.tex",
         "\\chapter{Desarrollo del Proyecto}\n\n"
         f"\\section{{Producto propuesto}}\n\\label{{{etq03}}}\n"
         "% <- 03, introducción y componentes\n" + producto +
         f"\n\\section{{Descripción de la metodología}}\n\\label{{{etq04}}}\n"
         "% <- 04, apertura\n" + apertura04 + "\n\n"
         "% <- 03, diagramas y operaciones\n" + mover_niveles(resto03, -1) +
         "\n% <- 04, secciones\n" + mover_niveles(resto04, -1))

# ---------------------------------------------------------------- 05 y 06
etq05, cuerpo05 = quitar_encabezado(leer(SECCIONES / "05_resultados.tex"))
etq06, cuerpo06 = quitar_encabezado(leer(SECCIONES / "06_discusion.tex"))
escribir("Capitulo4.tex",
         "\\chapter{Resultados y discusiones}\n\n"
         f"\\section{{Resultados}}\n\\label{{{etq05}}}\n% <- 05\n" + cuerpo05 +
         f"\n\\section{{Discusiones}}\n\\label{{{etq06}}}\n% <- 06\n" + cuerpo06)

# ---------------------------------------------------------------- 07
etq07, cuerpo07 = quitar_encabezado(leer(SECCIONES / "07_conclusiones.tex"))
apertura07, resto07 = quitar_linea(cuerpo07, r"\paragraph{Respuesta a la pregunta de investigación.}")
respuesta07, futuro07 = quitar_linea(resto07, r"\paragraph{Trabajo futuro.}")
escribir("Capitulo5.tex",
         f"\\chapter{{Conclusiones}}\\label{{conclusiones}}\n\\label{{{etq07}}}\n"
         "% <- 07\n" + apertura07 +
         "\n\\section{Con respecto a las preguntas de investigación}\n"
         "% <- 07, «Respuesta a la pregunta de investigación» hasta antes de «Trabajo futuro»\n"
         + respuesta07.lstrip() +
         "\n\\section{Con respecto al objetivo general}\n"
         "[PENDIENTE: 07 no tiene este material; depende del objetivo general "
         "(Sección~\\ref{secc:og})]\n\n"
         "\\section{Recomendaciones para trabajo a futuro}\n"
         "% <- 07, «Trabajo futuro» y párrafo final\n" + futuro07.lstrip())

# ---------------------------------------------------------------- resumen y extras
resumen = entre(leer(ORIGEN / "main.tex"), r"\begin{abstract}", r"\end{abstract}")
escribir("Resumen.tex",
         "\\chapter*{Resumen}\n\\markboth{chapter name}{Sinopsis}\n\n"
         "% <- resumen de main.tex\n" + resumen.strip() + "\n\n"
         "\\hfill\n\n\\textbf{Palabras clave}: [PENDIENTE]\n")

escribir("Agradecimientos.tex",
         "\\begin{thanks}\n[PENDIENTE: agradecimientos, los escribe el autor]\n\\end{thanks}\n")
escribir("Dedicatoria.tex",
         "\\chapter*{Dedicatoria}\n\n[PENDIENTE: dedicatoria, la escribe el autor]\n")
escribir("ApendiceA.tex",
         "\\chapter{Tabla de experimentos}\\label{apendiceA}\n\n"
         "[PENDIENTE: tabla de experimentos, sección y qué mide]\n")


# ---------------------------------------------------------------- verificación
def normal(linea):
    linea = RE_TITULO.sub(lambda m: m.group(1) + "\\TIT" + m.group(3), linea)
    return linea.strip()


salida = "\n".join(normal(l) for f in ["Introduccion.tex", "Capitulo1.tex", "Capitulo2.tex",
                                         "Capitulo3.tex", "Capitulo4.tex", "Capitulo5.tex",
                                         "Resumen.tex"]
                   for l in leer(AQUI / f).split("\n"))
faltan = []
for f in sorted(SECCIONES.glob("*.tex")):
    for l in leer(f).split("\n"):
        n = normal(l)
        if n and n not in salida:
            faltan.append(f"{f.name}: {n}")
print(f"líneas de .tex8 que no aparecen en la salida: {len(faltan)}")
for x in faltan:
    print("  ", x)
