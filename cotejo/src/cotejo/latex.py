"""Texto del reporte desde los .tex, con archivo y línea de cada palabra."""
from __future__ import annotations

import bisect
import hashlib
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from .texto import CITA_TEXTUAL, CODIGO, MATEMATICAS, palabras

SECCIONES = {"part": 0, "chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4,
             "paragraph": 5, "subparagraph": 6}
CITAS = {"cite", "citep", "citet", "citealp", "citealt", "parencite", "textcite", "autocite",
         "footcite", "citeauthor", "citeyear", "Cite", "Citep", "Citet", "Parencite",
         "Textcite", "Autocite", "supercite", "nocite"}
# comando -> número de argumentos obligatorios que se descartan (los opcionales se saltan siempre)
DESCARTAR = {
    "label": 1, "ref": 1, "eqref": 1, "pageref": 1, "autoref": 1, "cref": 1, "Cref": 1,
    "nameref": 1, "includegraphics": 1, "vspace": 1, "hspace": 1, "setlength": 2,
    "addtolength": 2, "setcounter": 2, "addtocounter": 2, "stepcounter": 1, "usepackage": 1,
    "RequirePackage": 1, "documentclass": 1, "bibliographystyle": 1, "graphicspath": 1,
    "newcommand": 2, "renewcommand": 2, "providecommand": 2, "DeclareRobustCommand": 2,
    "newenvironment": 3, "renewenvironment": 3, "definecolor": 3, "color": 1,
    "pagenumbering": 1, "thispagestyle": 1, "pagestyle": 1, "linespread": 1, "newtheorem": 2,
    "lstset": 1, "lstdefinestyle": 2, "hypersetup": 1, "tikzset": 1, "usetikzlibrary": 1,
    "addcontentsline": 3, "markboth": 2, "markright": 1, "url": 1, "phantom": 1,
    "hphantom": 1, "vphantom": 1, "rule": 2, "captionsetup": 1, "fontsize": 2, "cline": 1,
    "cmidrule": 1, "pagecolor": 1, "rowcolor": 1, "cellcolor": 1, "columncolor": 1,
    "arrayrulecolor": 1, "AddToHook": 2, "input@path": 1, "bibitem": 1, "lstinputlisting": 1,
    "newlength": 1, "settowidth": 2, "nolinkurl": 1, "selectlanguage": 1, "decimalpoint": 0,
    "renewcommand*": 2, "newcommand*": 2, "let": 0, "def": 0, "makeatletter": 0,
    "enlargethispage": 1, "addvspace": 1, "setstretch": 1, "includepdf": 1, "vskip": 0,
    "bibliography": 1, "addbibresource": 1, "printbibliography": 0, "titleformat": 5,
    "geometry": 1, "newgeometry": 1, "numberwithin": 2, "DeclareMathOperator": 2,
}
# comando -> argumentos que se descartan antes del que sí lleva texto
PREFIJO = {"textcolor": 1, "colorbox": 1, "fcolorbox": 2, "href": 1, "multicolumn": 2,
           "multirow": 2, "resizebox": 2, "scalebox": 1, "parbox": 1, "rotatebox": 1,
           "raisebox": 1, "foreignlanguage": 1, "hyperlink": 1, "hypertarget": 1,
           "makebox": 0, "framebox": 0, "mbox": 0}
SIMBOLOS = {"ldots": "…", "dots": "…", "textellipsis": "…", "LaTeX": "LaTeX", "TeX": "TeX",
            "textendash": "–", "textemdash": "—", "S": "§", "guillemotleft": "«",
            "guillemotright": "»", "og": "«", "fg": "»", "textless": "<", "textgreater": ">",
            "textbackslash": "\\", "i": "ı", "o": "ø", "ss": "ß", "aa": "å", "ae": "æ",
            "copyright": "©", "textregistered": "®", "texttrademark": "™", "euro": "€",
            "textdegree": "°", "degree": "°", "percent": "%", "textasciitilde": "~",
            "textquotedblleft": "“", "textquotedblright": "”", "quad": " ", "qquad": " ",
            "newline": " ", "linebreak": " ", "allowbreak": "", "hfill": " ", "space": " ",
            "enspace": " ", "thinspace": " ", "tabularnewline": "\n\n", "par": "\n\n",
            "medskip": "\n\n", "bigskip": "\n\n", "smallskip": "\n\n"}
ACENTOS = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303",
           "=": "\u0304", ".": "\u0307", "u": "\u0306", "v": "\u030c", "H": "\u030b",
           "c": "\u0327", "k": "\u0328", "r": "\u030a"}
ENT_MATE = {"equation", "equation*", "align", "align*", "gather", "gather*", "multline",
            "multline*", "eqnarray", "eqnarray*", "displaymath", "math", "flalign",
            "flalign*", "alignat", "alignat*", "dmath", "dmath*"}
ENT_CODIGO = {"verbatim", "verbatim*", "Verbatim", "lstlisting", "minted", "BVerbatim",
              "alltt", "pyglist"}
ENT_OMITIR = {"tikzpicture", "pgfpicture", "comment", "filecontents", "filecontents*"}
ENT_CITA = {"quote", "quotation", "verse", "displayquote"}
ENT_TABLA = {"tabular", "tabular*", "tabularx", "longtable", "array", "tabulary", "supertabular"}
ENT_ARGS = {"tabular": 1, "tabular*": 2, "tabularx": 2, "tabulary": 2, "longtable": 1,
            "array": 1, "minipage": 1, "wrapfigure": 2, "wraptable": 2, "subfigure": 1,
            "multicols": 1, "adjustbox": 1, "list": 2, "minted": 1, "thebibliography": 1,
            "supertabular": 1, "otherlanguage": 1}


@dataclass
class Segmento:
    id: int
    archivo: str
    linea_ini: int
    linea_fin: int
    tipo: str
    seccion: str
    texto: str
    citas: list[str] = field(default_factory=list)
    palabras: list[list] = field(default_factory=list)  # [palabra, línea, banderas]


@dataclass
class _Estado:
    archivo: str
    texto: str
    lineas: list[int]


class Extractor:
    def __init__(self, raiz: Path):
        self.raiz = Path(raiz).resolve()
        self.base = self.raiz.parent
        self.segmentos: list[Segmento] = []
        self.archivos: dict[str, str] = {}
        self.faltantes: list[str] = []
        self.ciclos: list[str] = []
        self.bibliografias: list[str] = []
        self.secciones = [""] * 7
        self._pila: list[Path] = []
        self._buf: list[tuple[str, int, int]] = []
        self._citas: list[str] = []
        self._est: _Estado | None = None
        self._tipos = ["prosa"]
        self._citando = 0

    # -- control de archivos
    def ejecutar(self) -> "Extractor":
        self._archivo(self.raiz, cuerpo=True)
        return self

    def _rel(self, ruta: Path) -> str:
        try:
            return ruta.resolve().relative_to(self.base.parent).as_posix()
        except ValueError:
            return ruta.name

    def _archivo(self, ruta: Path, cuerpo: bool = False):
        ruta = ruta.resolve()
        if ruta in self._pila:
            self.ciclos.append(" -> ".join(self._rel(p) for p in self._pila + [ruta]))
            return
        if not ruta.exists():
            self.faltantes.append(self._rel(ruta))
            return
        datos = ruta.read_bytes()
        texto = datos.decode("utf-8", errors="replace")
        rel = self._rel(ruta)
        self.archivos[rel] = hashlib.sha256(datos).hexdigest()
        previo = self._est
        self._cerrar()
        self._pila.append(ruta)
        self._est = _Estado(rel, texto, [i for i, c in enumerate(texto) if c == "\n"])
        ini, fin = 0, len(texto)
        if cuerpo:
            m = re.search(r"^[^%\n]*?\\begin\{document\}", texto, re.M)
            if m:
                ini = m.end()
                for linea in texto[:m.start()].splitlines():
                    b = re.search(r"\\(?:bibliography|addbibresource)\{([^}]*)\}", linea.split("%")[0])
                    if b:
                        self.bibliografias.append(b.group(1))
                f = re.search(r"\\end\{document\}", texto[ini:])
                fin = ini + f.start() if f else fin
        self._proc(ini, fin)
        self._cerrar()
        self._pila.pop()
        self._est = previo

    def _resolver(self, nombre: str) -> Path:
        p = Path(nombre.strip())
        if p.suffix != ".tex":
            p = p.with_name(p.name + ".tex")
        return p if p.is_absolute() else self.base / p

    # -- salida
    def _emitir(self, txt: str, pos: int, banderas: int = 0):
        if self._citando:
            banderas |= CITA_TEXTUAL
        for c in txt:
            if c == "\n":
                self._cerrar()
            else:
                self._buf.append((c, pos, banderas))

    def _cerrar(self, tipo: str | None = None):
        if not self._buf:
            return
        est = self._est
        chars, limpio, prev_esp = self._buf, [], True
        for c, p, b in chars:
            if c.isspace():
                if prev_esp:
                    continue
                limpio.append((" ", p, b))
                prev_esp = True
            else:
                if c in ",.;:)]" and limpio and limpio[-1][0] == " ":
                    limpio.pop()
                limpio.append((c, p, b))
                prev_esp = False
        while limpio and limpio[-1][0] == " ":
            limpio.pop()
        self._buf = []
        texto = "".join(c for c, _, _ in limpio)
        citas, self._citas = self._citas, []
        if not any(c.isalnum() for c in texto):
            return
        banderas = [b for _, _, b in limpio]
        _marcar_comillas(texto, banderas)
        linea = lambda p: bisect.bisect_left(est.lineas, p) + 1
        pals = []
        for w, a, b in palabras(texto):
            f = 0
            for k in range(a, b):
                f |= banderas[k]
            pals.append([w, linea(limpio[a][1]), f])
        lineas = [linea(p) for _, p, _ in limpio]
        self.segmentos.append(Segmento(
            len(self.segmentos), est.archivo, min(lineas), max(lineas),
            tipo or self._tipos[-1], " › ".join(s for s in self.secciones if s), texto,
            sorted(set(citas), key=citas.index), pals))

    # -- análisis
    def _proc(self, i: int, fin: int, banderas: int = 0):
        s = self._est.texto
        inicio_linea = True
        while i < fin:
            c = s[i]
            if c == "%":
                j = s.find("\n", i, fin)
                i = fin if j < 0 else j + 1
                continue
            if c == "\n":
                if inicio_linea:
                    self._cerrar()
                    while i < fin and s[i] in " \t\n":
                        i += 1
                    continue
                self._emitir(" ", i, banderas)
                inicio_linea = True
                i += 1
                continue
            if c in " \t\r":
                self._emitir(" ", i, banderas)
                i += 1
                continue
            inicio_linea = False
            if c == "\\":
                i = self._comando(i, fin, banderas)
            elif c == "$":
                doble = s.startswith("$$", i)
                cierre = _buscar_cierre(s, i + (2 if doble else 1), fin, "$$" if doble else "$")
                self._mate(s[i + (2 if doble else 1):cierre], i, aparte=doble)
                i = min(fin, cierre + (2 if doble else 1))
            elif c in "{}":
                i += 1
            elif c == "~":
                self._emitir(" ", i, banderas)
                i += 1
            elif c == "&":
                self._emitir(" ", i, banderas)
                i += 1
            elif s.startswith("---", i):
                self._emitir("—", i, banderas); i += 3
            elif s.startswith("--", i):
                self._emitir("–", i, banderas); i += 2
            elif s.startswith("``", i):
                self._emitir("“", i, banderas); i += 2
            elif s.startswith("''", i):
                self._emitir("”", i, banderas); i += 2
            elif s.startswith("<<", i) or s.startswith(">>", i):
                self._emitir("«" if c == "<" else "»", i, banderas); i += 2
            else:
                self._emitir(c, i, banderas)
                i += 1

    def _comando(self, i: int, fin: int, banderas: int) -> int:
        s = self._est.texto
        j = i + 1
        if j >= fin:
            return fin
        if not s[j].isalpha():
            c = s[j]
            if c in "%&_#${}":
                self._emitir(c, i, banderas)
                return j + 1
            if c == "\\":
                self._emitir(" ", i, banderas)
                k = _saltar_esp(s, j + 1, fin)
                if k < fin and s[k] == "*":
                    k += 1
                k2 = _saltar_esp(s, k, fin)
                return _saltar_opcional(s, k2, fin) if k2 < fin and s[k2] == "[" else k
            if c in ",;:! ":
                self._emitir(" ", i, banderas)
                return j + 1
            if c in ACENTOS and c not in ".=" or c in ".=" and j + 1 < fin and s[j + 1] in "{aeiouAEIOUcgzCGZ":
                return self._acento(c, j + 1, fin, i, banderas)
            if c == "(":
                cierre = s.find("\\)", j, fin)
                cierre = fin if cierre < 0 else cierre
                self._mate(s[j + 1:cierre], i, aparte=False)
                return min(fin, cierre + 2)
            if c == "[":
                cierre = s.find("\\]", j, fin)
                cierre = fin if cierre < 0 else cierre
                self._mate(s[j + 1:cierre], i, aparte=True)
                return min(fin, cierre + 2)
            return j + 1
        k = j
        while k < fin and s[k].isalpha():
            k += 1
        nombre = s[j:k]
        if k < fin and s[k] == "*":
            nombre += "*"
            k += 1
        base = nombre.rstrip("*")
        if base in ACENTOS and len(base) == 1:
            return self._acento(base, k, fin, i, banderas)
        if nombre in ("begin", "end"):
            return self._entorno(nombre, k, fin, i, banderas)
        if base in ("include", "input", "subfile"):
            a, b, k2 = _grupo(s, _saltar_esp(s, k, fin), fin)
            if a is not None:
                self._archivo(self._resolver(s[a:b]))
                return k2
            return k
        if base == "IfFileExists":
            args, k2 = _args(s, k, fin, 3)
            if len(args) == 3:
                existe = self._resolver(s[args[0][0]:args[0][1]]).exists()
                a, b = args[1] if existe else args[2]
                self._proc(a, b, banderas)
                return k2
            return k
        if base in SECCIONES:
            k = _saltar_opcional(s, _saltar_esp(s, k, fin), fin)
            a, b, k2 = _grupo(s, _saltar_esp(s, k, fin), fin)
            if a is None:
                return k
            self._cerrar()
            nivel = SECCIONES[base]
            self._tipos.append("titulo")
            self._proc(a, b, banderas)
            titulo = "".join(c for c, _, _ in self._buf)
            self.secciones[nivel] = " ".join(titulo.split())
            for n in range(nivel + 1, len(self.secciones)):
                self.secciones[n] = ""
            self._cerrar()
            self._tipos.pop()
            return k2
        if base in CITAS:
            k = _saltar_opcional(s, _saltar_esp(s, k, fin), fin)
            k = _saltar_opcional(s, _saltar_esp(s, k, fin), fin)
            a, b, k2 = _grupo(s, _saltar_esp(s, k, fin), fin)
            if a is None:
                return k
            self._citas.extend(x.strip() for x in s[a:b].split(",") if x.strip())
            return k2
        if base in ("caption", "footnote", "footnotetext"):
            k = _saltar_opcional(s, _saltar_esp(s, k, fin), fin)
            a, b, k2 = _grupo(s, _saltar_esp(s, k, fin), fin)
            if a is None:
                return k
            if base == "caption":
                self._cerrar()
                self._tipos.append("leyenda")
                self._proc(a, b, banderas)
                self._cerrar()
                self._tipos.pop()
            else:
                self._emitir(" ", a, banderas)
                self._proc(a, b, banderas)
                self._emitir(" ", b, banderas)
            return k2
        if base in ("say", "enquote", "textquote"):
            a, b, k2 = _grupo(s, _saltar_esp(s, k, fin), fin)
            if a is None:
                return k
            self._emitir("«", i, banderas)
            self._proc(a, b, banderas | CITA_TEXTUAL)
            self._emitir("»", b, banderas)
            return k2
        if base in ("verb", "lstinline", "mintinline"):
            if base == "mintinline":
                _, _, k = _grupo(s, _saltar_esp(s, k, fin), fin)
            k = _saltar_opcional(s, k, fin)
            if k >= fin:
                return fin
            delim = "}" if s[k] == "{" else s[k]
            cierre = s.find(delim, k + 1, fin)
            cierre = fin if cierre < 0 else cierre
            self._emitir(s[k + 1:cierre], k + 1, banderas | CODIGO)
            return cierre + 1
        if base == "item":
            self._cerrar()
            k2 = _saltar_esp(s, k, fin)
            if k2 < fin and s[k2] == "[":
                cierre = _cierre_corchete(s, k2, fin)
                self._proc(k2 + 1, cierre, banderas)
                self._emitir(" ", cierre, banderas)
                return cierre + 1
            return k
        if base in SIMBOLOS:
            self._emitir(SIMBOLOS[base], i, banderas)
            return k + 2 if base in ("ldots", "dots", "LaTeX", "TeX") and s.startswith("{}", k) else k
        if base in ("bibliography", "addbibresource"):
            a, b, _ = _grupo(s, _saltar_esp(s, k, fin), fin)
            if a is not None:
                self.bibliografias.append(s[a:b])
        if base in DESCARTAR:
            n = DESCARTAR[base]
            if base in ("newcommand", "renewcommand", "providecommand", "DeclareRobustCommand") \
                    and k < fin and s[_saltar_esp(s, k, fin)] != "{":
                k = _saltar_nombre(s, _saltar_esp(s, k, fin), fin)
                n -= 1
            if base == "cmidrule":
                k2 = _saltar_esp(s, k, fin)
                if k2 < fin and s[k2] == "(":
                    k = s.find(")", k2, fin) + 1
            if base == "def":
                k = _saltar_nombre(s, _saltar_esp(s, k, fin), fin)
                while k < fin and s[k] != "{":
                    k += 1
                n = 1
            _, k = _args(s, k, fin, n)
            return k
        if base in PREFIJO:
            _, k = _args(s, k, fin, PREFIJO[base])
            k = _saltar_opcional(s, _saltar_esp(s, k, fin), fin)
            return k
        return k

    def _acento(self, acento: str, k: int, fin: int, i: int, banderas: int) -> int:
        s = self._est.texto
        k = _saltar_esp(s, k, fin) if acento.isalpha() else k
        if k < fin and s[k] == "{":
            a, b, k2 = _grupo(s, k, fin)
            letra = s[a:b].strip().lstrip("\\")
        else:
            letra, k2 = (s[k] if k < fin else ""), k + 1
        if letra:
            self._emitir(unicodedata.normalize("NFC", letra[0] + ACENTOS[acento]) + letra[1:], i, banderas)
        return k2

    def _entorno(self, cual: str, k: int, fin: int, i: int, banderas: int) -> int:
        s = self._est.texto
        a, b, k2 = _grupo(s, _saltar_esp(s, k, fin), fin)
        if a is None:
            return k
        nombre = s[a:b].strip()
        if cual == "end":
            if nombre in ENT_CITA:
                self._citando = max(0, self._citando - 1)
            if nombre in ENT_CITA or nombre in ENT_TABLA or nombre == "thebibliography":
                self._cerrar()
                if len(self._tipos) > 1:
                    self._tipos.pop()
            elif nombre in ("itemize", "enumerate", "description", "list", "figure", "table"):
                self._cerrar()
            return k2
        if nombre in ENT_MATE or nombre in ENT_CODIGO or nombre in ENT_OMITIR:
            m = re.compile(r"\\end\s*\{" + re.escape(nombre) + r"\}").search(s, k2, fin)
            cierre, sig = (m.start(), m.end()) if m else (fin, fin)
            if nombre in ENT_MATE:
                self._mate(s[k2:cierre], k2, aparte=True)
            elif nombre in ENT_CODIGO:
                if nombre == "minted":
                    _, _, k2 = _grupo(s, _saltar_esp(s, _saltar_opcional(s, k2, fin), fin), fin)
                else:
                    k2 = _saltar_opcional(s, k2, fin)
                self._cerrar()
                self._buf = [(" " if c == "\n" else c, k2 + n, CODIGO)
                             for n, c in enumerate(s[k2:cierre])]
                self._cerrar("codigo")
            return sig
        k2 = _saltar_opcional(s, k2, fin)
        _, k2 = _args(s, k2, fin, ENT_ARGS.get(nombre, 0))
        if nombre in ENT_CITA:
            self._cerrar()
            self._citando += 1
            self._tipos.append("prosa")
        elif nombre in ENT_TABLA:
            self._cerrar()
            self._tipos.append("tabla")
        elif nombre == "thebibliography":
            self._cerrar()
            self._tipos.append("bibliografia")
        elif nombre in ("itemize", "enumerate", "description", "list", "figure", "table"):
            self._cerrar()
        return k2

    def _mate(self, contenido: str, pos: int, aparte: bool):
        texto = _limpiar_mate(contenido)
        if aparte:
            self._cerrar()
            self._emitir(texto, pos, MATEMATICAS)
            self._cerrar("ecuacion")
        else:
            self._emitir(texto, pos, MATEMATICAS)


GRIEGAS = {n: chr(c) for n, c in (
    ("alpha", 0x3B1), ("beta", 0x3B2), ("gamma", 0x3B3), ("delta", 0x3B4), ("epsilon", 0x3B5),
    ("varepsilon", 0x3B5), ("zeta", 0x3B6), ("eta", 0x3B7), ("theta", 0x3B8), ("iota", 0x3B9),
    ("kappa", 0x3BA), ("lambda", 0x3BB), ("mu", 0x3BC), ("nu", 0x3BD), ("xi", 0x3BE), ("pi", 0x3C0),
    ("rho", 0x3C1), ("sigma", 0x3C3), ("tau", 0x3C4), ("upsilon", 0x3C5), ("phi", 0x3C6),
    ("varphi", 0x3C6), ("chi", 0x3C7), ("psi", 0x3C8), ("omega", 0x3C9), ("Gamma", 0x393),
    ("Delta", 0x394), ("Theta", 0x398), ("Lambda", 0x39B), ("Xi", 0x39E), ("Pi", 0x3A0),
    ("Sigma", 0x3A3), ("Phi", 0x3A6), ("Psi", 0x3A8), ("Omega", 0x3A9))}


def _limpiar_mate(m: str) -> str:
    m = re.sub(r"%[^\n]*", " ", m)
    m = re.sub(r"\\([A-Za-z]+)(?![A-Za-z])", lambda x: f" {GRIEGAS[x.group(1)]} " if x.group(1) in GRIEGAS else x.group(), m)
    m = re.sub(r"\\(?:label|tag|nonumber|notag)\*?(\{[^}]*\})?", " ", m)
    m = re.sub(r"\\(?:text|mathrm|textrm|operatorname|mbox)\{([^}]*)\}", r" \1 ", m)
    m = re.sub(r"\\[a-zA-Z]+", " ", m)
    m = re.sub(r"[^\w.,=+\-<>/|()\[\]]", " ", m)
    return " ".join(m.split())


def _marcar_comillas(texto: str, banderas: list[int]):
    pares = {"«": "»", "“": "”"}
    pila: list[tuple[str, int]] = []
    recta = None
    for k, c in enumerate(texto):
        if c in pares:
            pila.append((pares[c], k))
        elif pila and c == pila[-1][0]:
            _, a = pila.pop()
            if not pila:
                for n in range(a, k + 1):
                    banderas[n] |= CITA_TEXTUAL
        elif c == '"':
            if recta is None:
                recta = k
            else:
                for n in range(recta, k + 1):
                    banderas[n] |= CITA_TEXTUAL
                recta = None


def _saltar_esp(s: str, i: int, fin: int) -> int:
    nuevas = 0
    while i < fin and s[i] in " \t\r\n":
        if s[i] == "\n":
            nuevas += 1
            if nuevas > 1:
                break
        i += 1
    return i


def _saltar_nombre(s: str, i: int, fin: int) -> int:
    if i < fin and s[i] == "{":
        return _grupo(s, i, fin)[2]
    if i < fin and s[i] == "\\":
        i += 1
        while i < fin and s[i].isalpha() or i < fin and s[i] == "@":
            i += 1
    return i


def _cierre_corchete(s: str, i: int, fin: int) -> int:
    prof, j = 0, i + 1
    while j < fin:
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            prof += 1
        elif c == "}":
            prof -= 1
        elif c == "]" and prof <= 0:
            return j
        j += 1
    return fin


def _saltar_opcional(s: str, i: int, fin: int) -> int:
    if i < fin and s[i] == "[":
        return min(fin, _cierre_corchete(s, i, fin) + 1)
    return i


def _grupo(s: str, i: int, fin: int):
    """Grupo entre llaves desde `i`; devuelve (inicio, fin) del contenido y la posición siguiente."""
    if i >= fin or s[i] != "{":
        if i < fin and s[i] == "\\":
            j = _saltar_nombre(s, i, fin)
            return i, j, j
        return None, None, i
    prof, j = 0, i
    while j < fin:
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "%":
            n = s.find("\n", j, fin)
            j = fin if n < 0 else n + 1
            continue
        if c == "{":
            prof += 1
        elif c == "}":
            prof -= 1
            if prof == 0:
                return i + 1, j, j + 1
        j += 1
    return i + 1, fin, fin


def _args(s: str, k: int, fin: int, n: int):
    args = []
    for _ in range(n):
        k = _saltar_opcional(s, _saltar_esp(s, k, fin), fin)
        a, b, k2 = _grupo(s, _saltar_esp(s, k, fin), fin)
        if a is None:
            break
        args.append((a, b))
        k = k2
    return args, k


def _buscar_cierre(s: str, i: int, fin: int, delim: str) -> int:
    j = i
    while j < fin:
        if s[j] == "\\":
            j += 2
            continue
        if s.startswith(delim, j):
            return j
        j += 1
    return fin


def extraer(raiz: Path, bib: Path | None = None, con_bibliografia: bool = True) -> dict:
    ex = Extractor(raiz).ejecutar()
    citadas: list[str] = []
    for seg in ex.segmentos:
        citadas.extend(c for c in seg.citas if c not in citadas)
    bib_ruta = bib
    if bib_ruta is None and ex.bibliografias:
        primero = ex.bibliografias[0].split(",")[0].strip()
        bib_ruta = ex.base / (primero if primero.endswith(".bib") else primero + ".bib")
    entradas = {}
    if bib_ruta and Path(bib_ruta).exists():
        from .bib import leer_bib, formatear
        entradas = leer_bib(Path(bib_ruta))
        if con_bibliografia:
            rel = ex._rel(Path(bib_ruta))
            for clave in citadas:
                e = entradas.get(clave)
                if not e:
                    continue
                texto = formatear(e)
                ex.segmentos.append(Segmento(
                    len(ex.segmentos), rel, e["_linea"], e["_linea"], "bibliografia",
                    "Bibliografía", texto, [clave],
                    [[w, e["_linea"], 0] for w, _, _ in palabras(texto)]))
    return {
        "raiz": ex._rel(ex.raiz),
        "archivos": ex.archivos,
        "faltantes": ex.faltantes,
        "ciclos": ex.ciclos,
        "bib": str(ex._rel(Path(bib_ruta))) if bib_ruta else None,
        "citadas": citadas,
        "claves_bib": sorted(entradas),
        "citas_sin_entrada": [c for c in citadas if entradas and c not in entradas],
        "segmentos": [vars(s) for s in ex.segmentos],
    }
