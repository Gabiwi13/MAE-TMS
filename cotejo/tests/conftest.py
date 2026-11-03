import shutil
import sys
from pathlib import Path

import pytest

AQUI = Path(__file__).parent
sys.path.insert(0, str(AQUI))

FUENTE1 = ("Introducción. Los sistemas de memoria transactiva distribuyen el conocimiento entre los "
           "miembros de un grupo de modo que cada uno sabe quién sabe qué, según la teoría original. "
           "La memoria transactiva es un sistema compartido para codificar almacenar y recuperar "
           "información en grupos pequeños.")
FUENTE2 = ("En este libro se explica que las redes neuronales profundas aprenden representaciones "
           "jerárquicas de los datos a partir de grandes cantidades de ejemplos etiquetados y ajustan "
           "millones de parámetros con descenso de gradiente estocástico, lo cual exige cómputo.")


@pytest.fixture
def proyecto(tmp_path) -> Path:
    destino = tmp_path / "proyecto"
    shutil.copytree(AQUI / "fixtures" / "proyecto", destino)
    cap2 = destino / "tex" / "cap2.tex"
    cap2.write_text(cap2.read_text(encoding="utf-8").replace("{{ZWSP}}", "\u200b"), encoding="utf-8")
    return destino


@pytest.fixture
def raiz(proyecto) -> Path:
    return proyecto / "tex" / "main.tex"


@pytest.fixture
def extr(raiz):
    from cotejo.latex import extraer
    return extraer(raiz)


@pytest.fixture
def textos():
    return {"fuente1": ({"tipo": "referencia"}, FUENTE1),
            "fuente2": ({"tipo": "referencia"}, FUENTE2)}
