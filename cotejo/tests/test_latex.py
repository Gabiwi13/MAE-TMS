from cotejo.latex import extraer
from cotejo.texto import CITA_TEXTUAL, CODIGO, MATEMATICAS, normalizar, palabras


def _seg(extr, fragmento):
    return next(s for s in extr["segmentos"] if fragmento in s["texto"])


def test_inclusiones_anidadas_ciclo_y_condicional(extr):
    assert set(extr["archivos"]) == {"tex/main.tex", "tex/cap1.tex", "tex/cap1b.tex", "tex/cap2.tex"}
    assert extr["ciclos"] == ["tex/main.tex -> tex/cap1.tex -> tex/cap1b.tex -> tex/cap1.tex"]
    assert extr["faltantes"] == []
    assert sum("Zanahoria" in s["texto"] for s in extr["segmentos"]) == 1


def test_inclusion_faltante(proyecto):
    (proyecto / "tex" / "cap2.tex").unlink()
    r = extraer(proyecto / "tex" / "main.tex")
    assert r["faltantes"] == ["tex/cap2.tex"]


def test_comentarios_y_porcentaje_escapado(extr):
    texto = " ".join(s["texto"] for s in extr["segmentos"])
    assert "comentario" not in texto
    assert "50 % de la Zanahoria" in texto


def test_ubicacion_exacta_por_palabra(extr, proyecto):
    lineas = (proyecto / "tex" / "cap1.tex").read_text(encoding="utf-8").splitlines()
    seg = _seg(extr, "Zanahoria")
    w = next(p for p in seg["palabras"] if p[0] == "Zanahoria")
    assert "Zanahoria" in lineas[w[1] - 1]
    assert seg["archivo"] == "tex/cap1.tex" and seg["linea_ini"] == 5


def test_palabras_alineadas_con_texto(extr):
    for s in extr["segmentos"]:
        assert [w for w, _, _ in palabras(s["texto"])] == [p[0] for p in s["palabras"]]


def test_tipos_y_banderas(extr):
    assert _seg(extr, "codigo_de_prueba")["tipo"] == "codigo"
    assert all(p[2] & CODIGO for p in _seg(extr, "codigo_de_prueba")["palabras"])
    ec = next(s for s in extr["segmentos"] if s["tipo"] == "ecuacion")
    assert all(p[2] & MATEMATICAS for p in ec["palabras"])
    inline = _seg(extr, "La variable")
    assert "α" in inline["texto"]
    assert any(p[2] & MATEMATICAS for p in inline["palabras"])
    assert not any(p[2] & MATEMATICAS for p in inline["palabras"] if p[0] == "variable")
    assert _seg(extr, "Celda uno")["tipo"] == "tabla"
    assert _seg(extr, "Introducción")["tipo"] == "titulo"


def test_comillas_y_bloque_de_cita(extr):
    seg = _seg(extr, "Según el autor")
    marcadas = [p[0] for p in seg["palabras"] if p[2] & CITA_TEXTUAL]
    assert marcadas[0] == "la" and marcadas[-1] == "pequeños"
    assert "Según" not in marcadas
    assert all(p[2] & CITA_TEXTUAL for p in _seg(extr, "cita en bloque")["palabras"])


def test_citas_por_parrafo_y_secciones(extr):
    assert _seg(extr, "Zanahoria")["citas"] == ["fuente1"]
    assert _seg(extr, "redes neuronales")["citas"] == []
    assert _seg(extr, "homoglifo")["seccion"] == "Métodos › Datos"
    assert extr["citadas"] == ["fuente1"]


def test_acentos_legados_y_notas(extr):
    assert "canción y ñandú" in _seg(extr, "antigua")["texto"]
    assert "escapar. Nota al pie" in _seg(extr, "escapar")["texto"]
    assert "b) Segundo elemento" in _seg(extr, "Segundo")["texto"]


def test_bibliografia_solo_citadas(extr):
    bib = [s for s in extr["segmentos"] if s["tipo"] == "bibliografia"]
    assert [s["citas"] for s in bib] == [["fuente1"]]
    assert bib[0]["archivo"] == "refs.bib" and bib[0]["linea_ini"] == 1
    assert extr["claves_bib"] == ["fuente1", "fuente2", "fuente3"]


def test_sin_bibliografia(raiz):
    r = extraer(raiz, con_bibliografia=False)
    assert not [s for s in r["segmentos"] if s["tipo"] == "bibliografia"]


def test_normalizacion():
    assert normalizar("M\u0415MORIA") == normalizar("memoria")
    assert normalizar("Canción") == "cancion"
    assert normalizar("pa\u200blabra") == "palabra"
    assert [w for w, _, _ in palabras("pa\u200blabra, otra")] == ["pa\u200blabra", "otra"]
