"""Lector mínimo de BibTeX: claves, campos y línea de cada entrada."""
from __future__ import annotations

import re
from pathlib import Path

RE_ENTRADA = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.M)


def _valor(s: str, i: int) -> tuple[str, int]:
    if s[i] == "{":
        prof, j = 0, i
        while j < len(s):
            if s[j] == "\\":
                j += 2
                continue
            if s[j] == "{":
                prof += 1
            elif s[j] == "}":
                prof -= 1
                if prof == 0:
                    return s[i + 1:j], j + 1
            j += 1
        return s[i + 1:], len(s)
    if s[i] == '"':
        j = i + 1
        while j < len(s) and s[j] != '"':
            j += 2 if s[j] == "\\" else 1
        return s[i + 1:j], j + 1
    m = re.match(r"[^,}\s]+", s[i:])
    return (m.group() if m else ""), i + (m.end() if m else 0)


def leer_bib(ruta: Path) -> dict[str, dict]:
    s = ruta.read_text(encoding="utf-8", errors="replace")
    entradas = {}
    for m in RE_ENTRADA.finditer(s):
        tipo, clave = m.group(1).lower(), m.group(2)
        if tipo in ("comment", "preamble", "string"):
            continue
        e = {"_tipo": tipo, "_linea": s.count("\n", 0, m.start()) + 1}
        i = m.end()
        while i < len(s):
            c = re.compile(r"\s*(\w[\w-]*)\s*=\s*").match(s, i)
            if not c:
                break
            valor, i = _valor(s, c.end())
            e[c.group(1).lower()] = " ".join(valor.split())
            c2 = re.compile(r"\s*,?").match(s, i)
            i = c2.end()
            if i < len(s) and s[i] == "}":
                break
        entradas[clave] = e
    return entradas


def _limpiar(v: str) -> str:
    v = re.sub(r"\\[a-zA-Z]+\s*", "", v)
    return " ".join(v.replace("{", "").replace("}", "").replace("~", " ").split())


def formatear(e: dict) -> str:
    partes = []
    for campo in ("author", "title", "journal", "booktitle", "publisher", "school",
                  "institution", "volume", "number", "pages", "year", "doi", "url"):
        if e.get(campo):
            v = _limpiar(e[campo])
            partes.append(f"«{v}»" if campo == "title" else v)
    return ", ".join(partes) + "."
