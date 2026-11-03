import json
import re

import pytest

from cotejo.cli import main
from cotejo.parafrasis import parafrasis
from cotejo.web import muestra
from conftest import FUENTE1, FUENTE2
from pdfsint import escribir_pdf, rect, texto


@pytest.fixture
def corrida(proyecto, tmp_path, capsys):
    pdfs = tmp_path / "pdfs"
    pdfs.mkdir()
    (pdfs / "fuente1.txt").write_text(FUENTE1, encoding="utf-8")
    (pdfs / "fuente2.txt").write_text(FUENTE2, encoding="utf-8")
    notas = tmp_path / "revision_notas.md"
    notas.write_text("Este archivo vuelve a incluir el capítulo y forma un ciclo.", encoding="utf-8")
    pdf = escribir_pdf(tmp_path / "doc.pdf", [texto(72, 700, "Los sistemas de memoria transactiva")
                                              + rect(70, 590, 300, 30) + texto(72, 600, "blanco", color="1 g")])
    salida, cache = tmp_path / "salida", tmp_path / "cache"
    main(["todo", "--raiz", str(proyecto / "tex" / "main.tex"), "--salida", str(salida), "--cache", str(cache),
          "--pdfs", str(pdfs), "--locales", str(notas), "--pdf", str(pdf), "--excluir-bibliografia",
          "--excluir-menores", "8", "--muestra", "3"])
    return salida, capsys.readouterr().out


def test_flujo_completo(corrida):
    salida, salida_texto = corrida
    for nombre in ("extraccion.json", "similitud.json", "banderas.json", "web_muestra.md",
                   "reporte.html", "reporte.json", "summary.md"):
        assert (salida / nombre).exists(), nombre
    assert "No equivale al índice del servicio comercial" in salida_texto
    datos = json.loads((salida / "reporte.json").read_text(encoding="utf-8"))
    cob = datos["cobertura"]
    assert cob["citadas_en_corpus"] == ["fuente1"] and cob["otras"] == ["fuente2"]
    assert cob["propias"] == ["propio:revision_notas.md"]
    assert datos["similitud"]["fuente_definicion"]["consultada"] is False
    assert datos["detectores"] is None
    assert datos["banderas"]["pdf"]["archivo"] == "doc.pdf"
    resumen = (salida / "summary.md").read_text(encoding="utf-8")
    assert "sin cita" in resumen and "No equivale" in resumen


def test_html_escapado_y_autocontenido(corrida):
    html = (corrida[0] / "reporte.html").read_text(encoding="utf-8")
    assert "<script>alert" not in html
    assert "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;" in html
    assert not re.search(r"<(?:script|link|img|iframe)[^>]+(?:src|href)=", html)
    assert "<mark" in html and 'id="seg-' in html
    assert "tex/cap1.tex:12" in html
    assert "Detectores abiertos" in html and "Cobertura del corpus" in html


def test_reporte_con_detectores_no_disponibles(corrida, capsys):
    salida = corrida[0]
    (salida / "detectores.json").write_text(json.dumps({"disponible": False, "motivo": "sin torch",
                                                         "limitaciones": ["x"]}), encoding="utf-8")
    main(["reporte", "--salida", str(salida)])
    html = (salida / "reporte.html").read_text(encoding="utf-8")
    assert "No disponible: sin torch" in html


def test_muestra_web(extr):
    m = muestra(extr, 2, min_palabras=5)
    assert len(m) <= 2 and m
    assert all("x_i" not in c["texto"] and "cita en bloque" not in c["texto"] for c in m)


def test_parafrasis_con_codificador_falso(extr):
    np = pytest.importorskip("numpy")
    def cod(textos):
        v = np.array([[t.count("memoria") + 0.1, t.count("redes") + 0.1, 1.0] for t in textos], dtype="float32")
        return v / np.linalg.norm(v, axis=1, keepdims=True)
    r = parafrasis(extr, {"fuente1": ({}, FUENTE1)}, cod, top=3, min_palabras=5)
    assert r["disponible"] and len(r["pares"]) == 3
    assert all(-1.0 <= p["coseno"] <= 1.0001 for p in r["pares"])


def test_parafrasis_sin_modelo_avisa(proyecto, tmp_path, capsys, monkeypatch):
    import cotejo.parafrasis as par

    def falla(*a, **k):
        raise OSError("modelo no disponible sin red")
    monkeypatch.setattr(par, "cargar_codificador", falla)
    salida = tmp_path / "s"
    main(["extraer", "--raiz", str(proyecto / "tex" / "main.tex"), "--salida", str(salida)])
    main(["similitud", "--salida", str(salida), "--cache", str(tmp_path / "c"), "--parafrasis"])
    sim = json.loads((salida / "similitud.json").read_text(encoding="utf-8"))
    assert sim["parafrasis"]["disponible"] is False and "sin red" in sim["parafrasis"]["motivo"]
    assert "corpus está vacío" in capsys.readouterr().out
