import shutil
import subprocess
from pathlib import Path

import pytest

from cotejo.banderas import banderas_pdf, banderas_tex, caracteres, ejecutar, metadatos_pdf
from pdfsint import escribir_pdf, rect, texto

AQUI = Path(__file__).parent


def test_caracteres():
    tipos = {h["tipo"] for h in caracteres("m\u0435moria pa\u200blabra \ue000 a\u202eb normal")}
    assert tipos == {"escritura mezclada", "invisible", "uso privado", "control bidireccional"}
    assert caracteres("Texto normal con acentos: canción, pingüino, ñandú.") == []
    assert caracteres("λ sola") == []
    assert [h["tipo"] for h in caracteres("desviación σm y κ")] == ["símbolo no latino pegado"]


def test_agrupacion_de_avisos_menores():
    from cotejo.banderas import _hallazgos_car
    lista = [(h, {"pagina": 1}) for h in caracteres(" ".join(["σm"] * 7 + ["m\u0435moria"] * 2))]
    hs = _hallazgos_car(lista, "x")
    assert sorted((h["regla"], h["prioridad"]) for h in hs) == [
        ("CAR-ESCRITURA-MEZCLADA", "alta"), ("CAR-ESCRITURA-MEZCLADA", "alta"),
        ("CAR-SÍMBOLO-NO-LATINO-PEGADO", "baja")]
    assert next(h for h in hs if h["prioridad"] == "baja")["evidencia"]["casos"] == 7


def test_banderas_tex(extr, proyecto):
    archivos = {rel: proyecto / rel for rel in extr["archivos"]}
    hs = banderas_tex(archivos)
    blancos = [h for h in hs if h["regla"] == "TEX-COLOR-BLANCO"]
    assert {h["ubicaciones"][0]["linea"] for h in blancos} == {5, 7}
    assert len(blancos) == 3
    assert [h["evidencia"]["fondo_en_la_linea"] for h in blancos if h["ubicaciones"][0]["linea"] == 7] == [True]
    assert all(h["estado_evidencia"] == "candidato" for h in blancos)
    car = {h["regla"]: h for h in hs if h["regla"].startswith("CAR-")}
    assert car["CAR-ESCRITURA-MEZCLADA"]["ubicaciones"][0] == {
        "archivo": "tex/cap2.tex", "linea": 4,
        "fragmento": car["CAR-ESCRITURA-MEZCLADA"]["ubicaciones"][0]["fragmento"]}
    assert "⟦U+200B⟧" in car["CAR-INVISIBLE"]["ubicaciones"][0]["fragmento"]
    assert any(h["regla"] == "TEX-COMENTARIOS" for h in hs)


def _pdf_prueba(ruta):
    contenido = (texto(72, 700, "Texto visible normal")
                 + texto(72, 650, "blanco sin fondo", color="1 g")
                 + rect(70, 590, 300, 30) + texto(72, 600, "blanco sobre negro", color="1 1 1 rg")
                 + texto(72, 550, "modo invisible", render=3)
                 + texto(72, 500, "diminuto", tam=0.3)
                 + texto(-900, -900, "fuera de pagina")
                 + rect(70, 440, 300, 30, color="0.2 0.4 0.6 rg")
                 + texto(72, 450, "mismo color", color="0.2 0.4 0.6 rg"))
    return escribir_pdf(ruta, [contenido], info={"Author": "Autor", "Producer": "xdvipdfmx"})


def test_texto_oculto_pdf(tmp_path):
    r = banderas_pdf(_pdf_prueba(tmp_path / "p.pdf"))
    por = {h["ubicaciones"][0]["fragmento"]: h for h in r["hallazgos"] if h["categoria"] == "texto oculto"}
    assert "Texto visible normal" not in por
    assert por["blanco sobre negro"]["estado_evidencia"] == "informativo"
    assert por["blanco sobre negro"]["evidencia"]["fondo_detectado"] is True
    assert por["blanco sin fondo"]["estado_evidencia"] == "candidato"
    assert "modo de render 3" in por["modo invisible"]["mensaje"]
    assert "tamaño" in por["diminuto"]["mensaje"]
    assert "fuera" in por["fuera de pagina"]["mensaje"]
    assert "rectángulo pintado debajo" in por["mismo color"]["mensaje"]
    assert r["paginas_analizadas"] == 1


def test_metadatos_presencia_ausencia_error(tmp_path):
    con, _ = metadatos_pdf(_pdf_prueba(tmp_path / "con.pdf"))
    assert {"/Author", "/Producer"} <= {c["campo"] for c in con}
    assert "No identifica" in next(c for c in con if c["campo"] == "/Producer")["explicacion"]
    sin, _ = metadatos_pdf(escribir_pdf(tmp_path / "sin.pdf", [texto(72, 700, "x")]))
    assert any(c["campo"] == "(Info)" and "ausencia" in c["explicacion"] for c in sin)
    roto = tmp_path / "roto.pdf"
    roto.write_bytes(b"esto no es un pdf")
    campos, hs = metadatos_pdf(roto)
    assert campos == [] and hs[0]["estado_evidencia"] == "error de lectura"


def test_ejecutar_con_y_sin_pdf(extr, proyecto, tmp_path):
    sin = ejecutar(extr, proyecto, None)
    assert sin["pdf"] is None and sin["tex"]["hallazgos"]
    assert any(m["campo"] == "pdfauthor" for m in sin["tex"]["metadatos_declarados"])
    con = ejecutar(extr, proyecto, _pdf_prueba(tmp_path / "p.pdf"))
    assert con["pdf"]["hallazgos"]
    falta = ejecutar(extr, proyecto, tmp_path / "noexiste.pdf")
    assert falta["pdf"]["error"] == "no existe"


@pytest.mark.skipif(shutil.which("xelatex") is None, reason="xelatex no instalado")
def test_trampas_en_pdf_real_de_xelatex(tmp_path):
    shutil.copy(AQUI / "fixtures" / "trampas.tex", tmp_path / "t.tex")
    subprocess.run(["xelatex", "-no-shell-escape", "-interaction=nonstopmode", "t.tex"], cwd=tmp_path,
                   capture_output=True, timeout=300)
    if not (tmp_path / "t.pdf").exists():
        pytest.skip("la compilación no produjo PDF (¿falta DejaVu Serif?)")
    hs = banderas_pdf(tmp_path / "t.pdf")["hallazgos"]
    por = {h["ubicaciones"][0].get("fragmento"): h for h in hs if h["categoria"] == "texto oculto"}
    assert por["Texto blanco sobre página blanca."]["estado_evidencia"] == "candidato"
    assert por["Blanco sobre caja negra."]["estado_evidencia"] == "informativo"
    assert "tamaño" in por["Letra diminuta escondida."]["mensaje"]
    assert "render 3" in por["Texto con modo de render invisible."]["mensaje"]
    assert any(h["regla"] == "CAR-ESCRITURA-MEZCLADA" for h in hs)
    assert "Texto normal visible en la página." not in por
