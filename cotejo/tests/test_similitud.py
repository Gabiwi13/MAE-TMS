from cotejo.similitud import Filtros, alinear, cotejar


def test_alinear_exacto_y_hueco():
    doc = "a b c d e f g h i j k".split()
    fuente = "x y c d e f g Z i j k w".split()
    ps = alinear(doc, {"f": fuente}, n=3, hueco=2)
    assert len(ps) == 1
    p = ps[0]
    assert (p.di, p.de, p.sj, p.se) == (2, 11, 2, 11)
    assert sorted(p.exactos) == [(2, 7), (8, 11)]


def test_alinear_ignora_shingles_frecuentes():
    doc = "a b c".split()
    fuentes = {f"f{k}": "a b c".split() for k in range(5)}
    assert alinear(doc, fuentes, n=3, max_ocurrencias=4) == []
    assert len(alinear(doc, fuentes, n=3, max_ocurrencias=5)) == 5


def test_indice_y_estado_de_cita(extr, textos):
    s = cotejar(extr, textos, Filtros(), n=5)
    assert 0 < s["indice"] < 100
    claves = {f["clave"]: f for f in s["fuentes"]}
    assert set(claves) == {"fuente1", "fuente2"}
    assert claves["fuente2"]["citada_en_documento"] is False
    assert claves["fuente2"]["pasajes_sin_cita"] == 1
    primero = s["pasajes"][0]
    assert primero["fuente"] == "fuente2" and primero["estado_cita"] == "sin cita"
    assert primero["archivo"] == "tex/cap1.tex" and primero["linea"] == 12
    assert primero["palabras_exactas"] == 28
    estados = {(p["fuente"], p["linea"]): p["estado_cita"] for p in s["pasajes"]}
    assert estados[("fuente1", 9)] == "citada en el párrafo"
    assert estados[("fuente1", 1)] == "citada en el párrafo"
    cruzado = next(p for p in s["pasajes"] if p["linea"] == 1)
    assert cruzado["texto_documento"].startswith("Introducción ¶ Los sistemas")
    assert "quién sabe qué" in cruzado["texto_documento"]
    assert cruzado["segmentos"] == [0, 1]
    assert abs(sum(f["porcentaje_primario"] for f in s["fuentes"]) - s["indice"]) < 0.05


def test_filtros(extr, textos):
    s = cotejar(extr, textos, Filtros(citas=True, menores=17, bibliografia=True))
    por = {i["nombre"]: i for i in s["indices"]}
    base = por["sin filtros"]
    citas = por["excluye citas textuales"]
    assert citas["palabras_coincidentes"] < base["palabras_coincidentes"]
    assert por["excluye bibliografía"]["palabras_documento"] < base["palabras_documento"]
    assert por["excluye coincidencias < 17 palabras"]["palabras_coincidentes"] < base["palabras_coincidentes"]
    elegido = [i for i in s["indices"] if i["elegido"]]
    assert len(elegido) == 1 and elegido[0]["indice"] == s["indice"]


def test_homoglifos_no_evitan_la_coincidencia(extr):
    texto = "Este párrafo contiene una palabra con homoglifo: memoria, y un espacioinvisible."
    s = cotejar(extr, {"f": ({"tipo": "referencia"}, texto)}, Filtros(), n=5)
    assert s["pasajes"] and s["pasajes"][0]["palabras_exactas"] >= 10


def test_fuente_propia(extr):
    texto = "Este archivo vuelve a incluir el capítulo y forma un ciclo."
    s = cotejar(extr, {"propio:notas.md": ({"tipo": "propio"}, texto)}, Filtros())
    assert s["pasajes"][0]["estado_cita"] == "fuente propia"
    assert s["fuentes"][0]["citada_en_documento"] is None


def test_corpus_vacio(extr):
    s = cotejar(extr, {}, Filtros())
    assert s["indice"] == 0 and s["fuentes"] == [] and s["pasajes"] == []
