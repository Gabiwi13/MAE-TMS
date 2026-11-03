"""Normalización y separación en palabras, comunes a todos los módulos."""
from __future__ import annotations

import re
import unicodedata

CITA_TEXTUAL = 1
MATEMATICAS = 2
CODIGO = 4

_INV = "\u200b\u200c\u200d\u2060\ufeff\u00ad\u180e"
RE_PALABRA = re.compile(rf"[^\W_]+(?:(?:['’\-][{_INV}]*|[{_INV}]+)[^\W_]+)*")
RE_ORACION = re.compile(r"(?<=[.!?…])\s+(?=[¿¡«“\"(\[]?[A-ZÁÉÍÓÚÑÜ0-9])")

# Confusables frecuentes (cirílico y griego) plegados a su par latino solo para comparar.
CONFUSABLES = str.maketrans({
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x", "і": "i",
    "ј": "j", "ѕ": "s", "ԁ": "d", "ɡ": "g", "һ": "h", "ӏ": "l", "ԛ": "q", "ԝ": "w",
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H", "О": "O", "Р": "P",
    "С": "C", "Т": "T", "Х": "X", "У": "Y", "І": "I", "Ј": "J", "Ѕ": "S",
    "ο": "o", "α": "a", "ν": "v", "ι": "i", "κ": "k", "ρ": "p", "τ": "t", "υ": "u",
    "Α": "A", "Β": "B", "Ε": "E", "Ζ": "Z", "Η": "H", "Ι": "I", "Κ": "K", "Μ": "M",
    "Ν": "N", "Ο": "O", "Ρ": "P", "Τ": "T", "Υ": "Y", "Χ": "X",
})
INVISIBLES = dict.fromkeys(map(ord, _INV), None)


def normalizar(palabra: str) -> str:
    p = unicodedata.normalize("NFKC", palabra).translate(INVISIBLES).translate(CONFUSABLES)
    p = unicodedata.normalize("NFKD", p.lower())
    return "".join(c for c in p if not unicodedata.combining(c)).replace("’", "'")


def palabras(texto: str) -> list[tuple[str, int, int]]:
    """Devuelve (palabra original, inicio, fin); los invisibles dentro de una palabra no la cortan."""
    return [(m.group(), m.start(), m.end()) for m in RE_PALABRA.finditer(texto)]


def palabras_normalizadas(texto: str) -> list[tuple[str, int, int]]:
    return [(normalizar(w), a, b) for w, a, b in palabras(texto)]


def oraciones(texto: str) -> list[tuple[int, int]]:
    cortes, inicio = [], 0
    for m in RE_ORACION.finditer(texto):
        cortes.append((inicio, m.start()))
        inicio = m.end()
    cortes.append((inicio, len(texto)))
    return [(a, b) for a, b in cortes if texto[a:b].strip()]
