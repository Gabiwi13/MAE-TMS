"""Generador mínimo de PDFs sintéticos para las pruebas (Helvetica estándar, sin compresión)."""
from __future__ import annotations

from pathlib import Path


def _cadena(t: str) -> str:
    return "(" + t.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") + ")"


def texto(x, y, t, tam=12, color="0 g", render=0) -> str:
    return f"{color} BT {render} Tr /F1 {tam} Tf {x} {y} Td {_cadena(t)} Tj ET\n"


def rect(x, y, w, h, color="0 g") -> str:
    return f"{color} {x} {y} {w} {h} re f\n"


def escribir_pdf(ruta: Path, paginas: list[str], info: dict | None = None) -> Path:
    objs: list[bytes] = []
    n_pag = len(paginas)
    # 1 catálogo, 2 páginas, 3 fuente, luego (página, contenido) por cada una, al final Info
    kids = " ".join(f"{4 + 2 * k} 0 R" for k in range(n_pag))
    objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objs.append(f"<< /Type /Pages /Kids [{kids}] /Count {n_pag} >>".encode())
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    for k, contenido in enumerate(paginas):
        datos = contenido.encode("latin-1")
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                    f"/Resources << /Font << /F1 3 0 R >> >> /Contents {5 + 2 * k} 0 R >>".encode())
        objs.append(f"<< /Length {len(datos)} >>\nstream\n".encode() + datos + b"\nendstream")
    info_ref = ""
    if info:
        campos = " ".join(f"/{k} {_cadena(v)}" for k, v in info.items())
        objs.append(f"<< {campos} >>".encode("latin-1"))
        info_ref = f" /Info {len(objs)} 0 R"
    salida = bytearray(b"%PDF-1.4\n")
    offs = []
    for i, o in enumerate(objs, 1):
        offs.append(len(salida))
        salida += f"{i} 0 obj\n".encode() + o + b"\nendobj\n"
    xref = len(salida)
    salida += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for o in offs:
        salida += f"{o:010d} 00000 n \n".encode()
    salida += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R{info_ref} >>\nstartxref\n{xref}\n%%EOF\n".encode()
    Path(ruta).write_bytes(bytes(salida))
    return Path(ruta)
