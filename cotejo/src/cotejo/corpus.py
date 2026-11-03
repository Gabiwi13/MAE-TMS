"""Corpus de fuentes: descarga, extracción de texto y caché con procedencia."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

from . import __version__
from .texto import palabras

AGENTE = f"cotejo/{__version__} (cotejo local de similitud)"
EXT_TEXTO = {".txt", ".md", ".tex", ".rst"}


def ahora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _clave_segura(clave: str) -> str:
    return re.sub(r"[^\w.\-]+", "_", clave)[:120]


class _Html(HTMLParser):
    OMITIR = {"script", "style", "noscript", "nav", "header", "footer", "svg", "form", "aside"}
    BLOQUE = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "section",
              "article", "blockquote", "td", "th", "figcaption", "dd", "dt"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes: list[str] = []
        self.omitir = 0
        self.titulo = ""
        self._en_titulo = False

    def handle_starttag(self, tag, attrs):
        if tag in self.OMITIR:
            self.omitir += 1
        if tag == "title":
            self._en_titulo = True
        if tag in self.BLOQUE:
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in self.OMITIR and self.omitir:
            self.omitir -= 1
        if tag == "title":
            self._en_titulo = False
        if tag in self.BLOQUE:
            self.partes.append("\n")

    def handle_data(self, data):
        if self._en_titulo:
            self.titulo += data
        elif not self.omitir:
            self.partes.append(data)


def texto_html(datos: bytes, charset: str | None = None) -> tuple[str, str]:
    m = re.search(rb'charset=["\']?([\w-]+)', datos[:4000])
    cod = charset or (m.group(1).decode() if m else "utf-8")
    try:
        html = datos.decode(cod, errors="replace")
    except LookupError:
        html = datos.decode("utf-8", errors="replace")
    p = _Html()
    p.feed(html)
    texto = re.sub(r"[ \t]+", " ", "".join(p.partes))
    texto = re.sub(r"\n\s*\n+", "\n\n", texto)
    return texto.strip(), " ".join(p.titulo.split())


def texto_pdf(ruta: Path, metodo: str = "auto") -> tuple[str, str]:
    if metodo in ("auto", "pdftotext") and shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", "-enc", "UTF-8", str(ruta), "-"],
                           capture_output=True, timeout=300)
        if r.returncode == 0 and r.stdout.strip():
            return _unir_guiones(r.stdout.decode("utf-8", errors="replace")), "pdftotext"
        if metodo == "pdftotext":
            raise RuntimeError(r.stderr.decode(errors="replace")[:300])
    from pypdf import PdfReader
    lector = PdfReader(str(ruta))
    paginas = [(p.extract_text() or "") for p in lector.pages]
    return _unir_guiones("\n\f".join(paginas)), "pypdf"


def _unir_guiones(t: str) -> str:
    return re.sub(r"(\w)-\n\s*(\w)", r"\1\2", t.replace("\r", ""))


def texto_archivo(ruta: Path) -> tuple[str, str]:
    suf = ruta.suffix.lower()
    if suf == ".pdf":
        return texto_pdf(ruta)
    if suf in (".html", ".htm"):
        return texto_html(ruta.read_bytes())[0], "html"
    return ruta.read_text(encoding="utf-8", errors="replace"), "texto"


def plantilla_desde_bib(bib: Path) -> list[dict]:
    from .bib import leer_bib, _limpiar
    salida = []
    for clave, e in leer_bib(bib).items():
        url = e.get("url", "")
        doi = e.get("doi", "")
        salida.append({
            "clave": clave,
            "titulo": _limpiar(e.get("title", "")),
            "url_pdf": url if url.lower().endswith(".pdf") else "",
            "url_html": "" if url.lower().endswith(".pdf") else (url or (f"https://doi.org/{doi}" if doi else "")),
            "licencia": "",
        })
    return salida


def cargar_fuentes(ruta: Path) -> list[dict]:
    datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
    if isinstance(datos, dict):
        datos = datos.get("fuentes", [])
    salida = []
    for f in datos:
        if not isinstance(f, dict) or not f.get("clave"):
            raise ValueError(f"Fuente sin «clave»: {f!r}")
        salida.append(f)
    return salida


class Corpus:
    def __init__(self, cache: Path):
        self.cache = Path(cache)
        (self.cache / "crudo").mkdir(parents=True, exist_ok=True)
        (self.cache / "texto").mkdir(parents=True, exist_ok=True)
        self.ruta_manifiesto = self.cache / "manifiesto.json"
        self.manifiesto: dict = {"fuentes": {}}
        if self.ruta_manifiesto.exists():
            self.manifiesto = json.loads(self.ruta_manifiesto.read_text(encoding="utf-8"))

    def guardar(self):
        self.ruta_manifiesto.write_text(json.dumps(self.manifiesto, ensure_ascii=False, indent=1),
                                        encoding="utf-8")

    def _registrar(self, clave: str, datos: bytes, texto: str, **meta):
        nombre = _clave_segura(clave)
        (self.cache / "texto" / f"{nombre}.txt").write_text(texto, encoding="utf-8")
        reg = {"clave": clave, "sha256": hashlib.sha256(datos).hexdigest(),
               "palabras": len(palabras(texto)), "archivo_texto": f"texto/{nombre}.txt",
               "estado": "ok" if texto.strip() else "sin_texto", "error": "", **meta}
        self.manifiesto["fuentes"][clave] = reg
        return reg

    def _fallo(self, clave: str, error: str, **meta):
        reg = {"clave": clave, "estado": "error", "error": error[:500], "palabras": 0, **meta}
        self.manifiesto["fuentes"][clave] = reg
        return reg

    def descargar(self, fuente: dict, refrescar: bool = False, abrir=urllib.request.urlopen):
        clave = fuente["clave"]
        url = fuente.get("url_pdf") or fuente.get("url_html") or ""
        meta = {"origen": url, "tipo": fuente.get("tipo", "referencia"),
                "licencia": fuente.get("licencia", ""), "titulo": fuente.get("titulo", ""),
                "fecha": ahora()}
        previo = self.manifiesto["fuentes"].get(clave)
        if previo and previo.get("estado") == "ok" and previo.get("origen") == url and not refrescar:
            return previo
        if not url:
            return self._fallo(clave, "sin URL en la lista de fuentes", **meta)
        if not url.lower().startswith(("http://", "https://")):
            return self._fallo(clave, "URL no admitida (solo http/https)", **meta)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
            with abrir(req, timeout=90) as r:
                datos = r.read(60_000_000)
                tipo_mime = (r.headers.get("Content-Type") or "").lower()
                meta["url_final"] = r.geturl() if hasattr(r, "geturl") else url
        except Exception as e:
            return self._fallo(clave, f"{type(e).__name__}: {e}", **meta)
        nombre = _clave_segura(clave)
        try:
            if datos[:5] == b"%PDF-":
                crudo = self.cache / "crudo" / f"{nombre}.pdf"
                crudo.write_bytes(datos)
                texto, metodo = texto_pdf(crudo)
            else:
                crudo = self.cache / "crudo" / f"{nombre}.html"
                crudo.write_bytes(datos)
                texto, titulo = texto_html(datos)
                metodo = "html"
                meta["titulo"] = meta["titulo"] or titulo
                if fuente.get("url_pdf") and "pdf" not in tipo_mime:
                    meta["aviso"] = "se pidió PDF y llegó HTML (posible página de acceso o resumen)"
        except Exception as e:
            return self._fallo(clave, f"extracción: {type(e).__name__}: {e}", **meta)
        return self._registrar(clave, datos, texto, metodo=metodo, **meta)

    def agregar_local(self, ruta: Path, clave: str | None = None, tipo: str = "referencia"):
        ruta = Path(ruta)
        clave = clave or ruta.stem
        meta = {"origen": ruta.name, "tipo": tipo, "licencia": "", "titulo": "",
                "fecha": ahora()}
        try:
            texto, metodo = texto_archivo(ruta)
        except Exception as e:
            return self._fallo(clave, f"{type(e).__name__}: {e}", **meta)
        return self._registrar(clave, ruta.read_bytes(), texto, metodo=metodo, **meta)

    def textos(self) -> dict[str, tuple[dict, str]]:
        salida = {}
        for clave, reg in self.manifiesto["fuentes"].items():
            if reg.get("estado") != "ok":
                continue
            ruta = self.cache / reg["archivo_texto"]
            if ruta.exists():
                salida[clave] = (reg, ruta.read_text(encoding="utf-8"))
        return salida


def construir(cache: Path, fuentes: Path | None = None, pdfs: Path | None = None,
              locales: list[Path] | None = None, refrescar: bool = False,
              sin_red: bool = False, avisar=print) -> dict:
    c = Corpus(cache)
    if fuentes:
        for f in cargar_fuentes(fuentes):
            if sin_red:
                continue
            reg = c.descargar(f, refrescar=refrescar)
            avisar(f"  {reg['clave']}: {reg['estado']} {reg.get('error', '')}".rstrip())
            c.guardar()
    if pdfs:
        for ruta in sorted(Path(pdfs).iterdir()):
            if ruta.suffix.lower() in {".pdf", ".html", ".htm"} | EXT_TEXTO:
                reg = c.agregar_local(ruta)
                avisar(f"  {reg['clave']} (local): {reg['estado']} {reg.get('error', '')}".rstrip())
    for ruta in locales or []:
        reg = c.agregar_local(Path(ruta), clave=f"propio:{Path(ruta).name}", tipo="propio")
        avisar(f"  {reg['clave']}: {reg['estado']}")
    c.guardar()
    return c.manifiesto
