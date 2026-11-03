import io
import json
import urllib.error

from cotejo.corpus import Corpus, cargar_fuentes, construir, plantilla_desde_bib, texto_html
from pdfsint import escribir_pdf, texto


class _Resp(io.BytesIO):
    def __init__(self, datos, tipo, url):
        super().__init__(datos)
        self.headers = {"Content-Type": tipo}
        self._url = url

    def geturl(self):
        return self._url

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _abridor(respuestas):
    def abrir(req, timeout=None):
        r = respuestas[req.full_url]
        if isinstance(r, Exception):
            raise r
        return _Resp(*r, req.full_url)
    return abrir


def test_html_sin_scripts():
    t, titulo = texto_html(b"<html><head><title>T\xc3\xadtulo</title><script>var x=1;</script></head>"
                           b"<body><nav>menu</nav><p>Hola <b>mundo</b></p><p>Otro</p></body></html>")
    assert titulo == "Título"
    assert "var x" not in t and "menu" not in t
    assert "Hola mundo" in t and "Otro" in t


def test_descarga_pdf_html_y_fallos(tmp_path):
    pdf = escribir_pdf(tmp_path / "a.pdf", [texto(72, 700, "Contenido de la fuente en PDF")]).read_bytes()
    c = Corpus(tmp_path / "cache")
    abrir = _abridor({
        "https://x.org/a.pdf": (pdf, "application/pdf"),
        "https://x.org/b": (b"<p>Texto de la pagina</p>", "text/html"),
        "https://x.org/c.pdf": (b"<p>Acceso restringido</p>", "text/html"),
        "https://x.org/d": urllib.error.URLError("sin red"),
    })
    r = c.descargar({"clave": "a", "url_pdf": "https://x.org/a.pdf", "licencia": "CC-BY"}, abrir=abrir)
    assert r["estado"] == "ok" and r["licencia"] == "CC-BY" and r["fecha"] and r["sha256"]
    assert "Contenido de la fuente" in (tmp_path / "cache" / r["archivo_texto"]).read_text(encoding="utf-8")
    assert c.descargar({"clave": "b", "url_html": "https://x.org/b"}, abrir=abrir)["metodo"] == "html"
    assert "aviso" in c.descargar({"clave": "c", "url_pdf": "https://x.org/c.pdf"}, abrir=abrir)
    falla = c.descargar({"clave": "d", "url_html": "https://x.org/d"}, abrir=abrir)
    assert falla["estado"] == "error" and "sin red" in falla["error"]
    assert c.descargar({"clave": "e"}, abrir=abrir)["error"] == "sin URL en la lista de fuentes"
    assert "no admitida" in c.descargar({"clave": "f", "url_html": "file:///etc/passwd"}, abrir=abrir)["error"]
    assert set(c.textos()) == {"a", "b", "c"}


def test_cache_no_redescarga(tmp_path):
    c = Corpus(tmp_path / "cache")
    llamadas = []

    def abrir(req, timeout=None):
        llamadas.append(req.full_url)
        return _Resp(b"<p>uno</p>", "text/html", req.full_url)
    f = {"clave": "a", "url_html": "https://x.org/a"}
    c.descargar(f, abrir=abrir)
    c.guardar()
    Corpus(tmp_path / "cache").descargar(f, abrir=abrir)
    assert len(llamadas) == 1
    Corpus(tmp_path / "cache").descargar(f, refrescar=True, abrir=abrir)
    assert len(llamadas) == 2


def test_construir_local_y_propias(tmp_path):
    pdfs = tmp_path / "pdfs"
    pdfs.mkdir()
    escribir_pdf(pdfs / "fuente1.pdf", [texto(72, 700, "Texto local de la fuente uno")])
    nota = tmp_path / "README.md"
    nota.write_text("Notas propias del autor.", encoding="utf-8")
    m = construir(tmp_path / "cache", pdfs=pdfs, locales=[nota], avisar=lambda *_: None)
    assert m["fuentes"]["fuente1"]["estado"] == "ok"
    assert m["fuentes"]["propio:README.md"]["tipo"] == "propio"
    assert json.loads((tmp_path / "cache" / "manifiesto.json").read_text(encoding="utf-8"))["fuentes"]


def test_plantilla_y_lista(proyecto, tmp_path):
    p = plantilla_desde_bib(proyecto / "refs.bib")
    por = {f["clave"]: f for f in p}
    assert por["fuente1"]["url_html"] == "https://doi.org/10.0000/prueba.1"
    assert por["fuente2"]["url_pdf"] == "https://ejemplo.org/redes.pdf"
    ruta = tmp_path / "f.json"
    ruta.write_text(json.dumps({"fuentes": p}), encoding="utf-8")
    assert len(cargar_fuentes(ruta)) == 3
