"""Detectores abiertos de texto generado: Binoculars y Fast-DetectGPT (opcional, requiere torch).

Binoculars: Hans et al., «Spotting LLMs With Binoculars: Zero-Shot Detection of
Machine-Generated Text», ICML 2024, arXiv:2401.12070; código: github.com/ahans30/Binoculars.
Fast-DetectGPT: Bao et al., «Fast-DetectGPT: Efficient Zero-Shot Detection of Machine-Generated
Text via Conditional Probability Curvature», ICLR 2024, arXiv:2310.05130; código:
github.com/baoguangsheng/fast-detect-gpt (criterio analítico de scripts/fast_detect_gpt.py).
"""
from __future__ import annotations

import bisect
import re
import statistics
from pathlib import Path

METODOS = [
    {"nombre": "Binoculars", "referencia": "Hans et al., ICML 2024, arXiv:2401.12070",
     "codigo": "https://github.com/ahans30/Binoculars",
     "direccion": "más bajo = más parecido a lo que el par de modelos espera de texto generado"},
    {"nombre": "Fast-DetectGPT (analítico)", "referencia": "Bao et al., ICLR 2024, arXiv:2310.05130",
     "codigo": "https://github.com/baoguangsheng/fast-detect-gpt",
     "direccion": "más alto = más parecido a lo que el par de modelos espera de texto generado"},
]
PARES = {
    "pequeno": ("Qwen/Qwen2.5-1.5B", "Qwen/Qwen2.5-1.5B-Instruct"),
    "articulo": ("tiiuae/falcon-7b", "tiiuae/falcon-7b-instruct"),
}
LIMITACIONES = [
    "Ningún puntaje es prueba de autoría ni de uso de IA; son estadísticos de un par de modelos.",
    "No hay umbral de decisión validado para español académico ni para estos modelos; no se etiqueta nada.",
    "Los umbrales publicados (p. ej. los de Binoculars con Falcon-7B) no se trasladan a otros modelos, "
    "idiomas ni tipos de texto.",
    "Texto técnico, formulaico, traducido o muy editado puede puntuar como «generado», y al revés.",
    "Sin un conjunto de referencia del propio dominio (--referencia) el número no se interpreta.",
    "Los párrafos se extraen del .tex: sin ecuaciones renderizadas ni formato; eso cambia los puntajes.",
]


# ---------------------------------------------------------------- matemáticas (torch)
def binoculars(logits_obs, logits_int, ids):
    """Puntaje de Binoculars para un lote de 1, como en binoculars/metrics.py del repositorio."""
    import torch
    import torch.nn.functional as F
    lo, li = logits_obs[0].float(), logits_int[0].float()
    ppl = F.cross_entropy(li[:-1], ids[0, 1:], reduction="mean")
    p_obs = torch.softmax(lo, dim=-1)
    x_ppl = -(p_obs * torch.log_softmax(li, dim=-1)).sum(-1).mean()
    return float(ppl / x_ppl)


def fast_detectgpt(logits_ref, logits_score, etiquetas):
    """Discrepancia de muestreo analítica (get_sampling_discrepancy_analytic)."""
    import torch
    lr, ls = logits_ref.float(), logits_score.float()
    if lr.size(-1) != ls.size(-1):
        v = min(lr.size(-1), ls.size(-1))
        lr, ls = lr[..., :v], ls[..., :v]
    etiquetas = etiquetas.unsqueeze(-1)
    lp = torch.log_softmax(ls, dim=-1)
    pr = torch.softmax(lr, dim=-1)
    ll = lp.gather(dim=-1, index=etiquetas).squeeze(-1)
    media = (pr * lp).sum(-1)
    var = (pr * lp.square()).sum(-1) - media.square()
    d = (ll.sum(-1) - media.sum(-1)) / var.sum(-1).sqrt()
    return float(d.mean())


class Modelos:
    """Par base/instruct: Binoculars usa observador=base e intérprete=instruct; Fast-DetectGPT
    usa muestreo=base y puntuación=instruct, como los valores por defecto actuales del repositorio."""

    def __init__(self, tokenizador, base, instruct, nombres=("", ""), dispositivo="cpu"):
        self.tok, self.base, self.instruct = tokenizador, base, instruct
        self.nombres, self.dispositivo = nombres, dispositivo

    @classmethod
    def cargar(cls, base: str, instruct: str, dispositivo: str | None = None):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        dispositivo = dispositivo or ("cuda" if torch.cuda.is_available() else "cpu")
        dtype = torch.bfloat16 if dispositivo.startswith("cuda") else torch.float32
        tok = AutoTokenizer.from_pretrained(base)
        tok2 = AutoTokenizer.from_pretrained(instruct)
        if tok.get_vocab() != tok2.get_vocab():
            raise ValueError("Los dos modelos no comparten tokenizador; ambos métodos lo requieren.")
        mods = []
        for nombre in (base, instruct):
            m = AutoModelForCausalLM.from_pretrained(nombre, dtype=dtype).to(dispositivo)
            m.eval()
            mods.append(m)
        return cls(tok, mods[0], mods[1], (base, instruct), dispositivo)

    def puntuar(self, texto: str, max_tokens: int = 512) -> dict:
        import torch
        enc = self.tok(texto, return_tensors="pt", truncation=True, max_length=max_tokens,
                       return_token_type_ids=False)
        ids = enc["input_ids"].to(self.dispositivo)
        if ids.shape[1] < 3:
            return {"tokens": int(ids.shape[1]), "binoculars": None, "fast_detectgpt": None}
        with torch.inference_mode():
            lb = self.base(input_ids=ids).logits
            li = self.instruct(input_ids=ids).logits
        return {"tokens": int(ids.shape[1]),
                "binoculars": binoculars(lb, li, ids),
                "fast_detectgpt": fast_detectgpt(lb[:, :-1], li[:, :-1], ids[:, 1:])}


# ---------------------------------------------------------------- referencia y agregados
def _parrafos_archivo(ruta: Path, min_palabras: int) -> list[str]:
    texto = ruta.read_text(encoding="utf-8", errors="replace")
    partes = [" ".join(p.split()) for p in re.split(r"\n\s*\n", texto)]
    return [p for p in partes if len(p.split()) >= min_palabras]


def _posicion(valor, ordenados: list[float]):
    if valor is None or not ordenados:
        return None
    return round(100.0 * bisect.bisect_right(ordenados, valor) / len(ordenados), 1)


def _resumen(vals: list[float]) -> dict:
    vals = [v for v in vals if v is not None]
    if not vals:
        return {"n": 0}
    q = statistics.quantiles(vals, n=4) if len(vals) >= 2 else [vals[0]] * 3
    return {"n": len(vals), "mediana": round(statistics.median(vals), 4),
            "q1": round(q[0], 4), "q3": round(q[2], 4),
            "min": round(min(vals), 4), "max": round(max(vals), 4)}


def puntuar_referencia(modelos: Modelos, carpeta: Path, min_palabras: int, max_tokens: int,
                       avisar=print) -> dict:
    salida = {"carpeta": Path(carpeta).name, "grupos": {}}
    for grupo in ("humano", "generado"):
        sub = Path(carpeta) / grupo
        puntajes = []
        archivos = sorted(p for p in sub.glob("**/*") if p.suffix.lower() in (".txt", ".md")) if sub.exists() else []
        for ruta in archivos:
            for p in _parrafos_archivo(ruta, min_palabras):
                puntajes.append(modelos.puntuar(p, max_tokens))
        avisar(f"  referencia {grupo}: {len(archivos)} archivos, {len(puntajes)} párrafos")
        salida["grupos"][grupo] = {
            "archivos": len(archivos), "parrafos": len(puntajes),
            "binoculars": sorted(x["binoculars"] for x in puntajes if x["binoculars"] is not None),
            "fast_detectgpt": sorted(x["fast_detectgpt"] for x in puntajes if x["fast_detectgpt"] is not None),
        }
    return salida


def detectar(extr: dict, modelos: Modelos | None, referencia: Path | None = None,
             min_palabras: int = 40, max_tokens: int = 512, tipos=("prosa",), avisar=print,
             motivo: str = "") -> dict:
    base = {"metodos": METODOS, "limitaciones": LIMITACIONES,
            "parametros": {"min_palabras": min_palabras, "max_tokens": max_tokens, "tipos": list(tipos)}}
    if modelos is None:
        return {**base, "disponible": False, "motivo": motivo or "módulo no ejecutado",
                "parrafos": [], "secciones": [], "referencia": None}
    parrafos = []
    candidatos = [s for s in extr["segmentos"] if s["tipo"] in tipos and len(s["palabras"]) >= min_palabras]
    for k, s in enumerate(candidatos, 1):
        r = modelos.puntuar(s["texto"], max_tokens)
        parrafos.append({"segmento": s["id"], "archivo": s["archivo"], "linea": s["linea_ini"],
                         "seccion": s["seccion"], "palabras": len(s["palabras"]), **r})
        if k % 25 == 0:
            avisar(f"  {k}/{len(candidatos)} párrafos")
    ref = None
    if referencia:
        ref = puntuar_referencia(modelos, Path(referencia), min_palabras, max_tokens, avisar)
        for p in parrafos:
            for grupo, g in ref["grupos"].items():
                for m in ("binoculars", "fast_detectgpt"):
                    p[f"pos_{m}_{grupo}"] = _posicion(p[m], g[m])
        for g in ref["grupos"].values():
            g["resumen_binoculars"] = _resumen(g["binoculars"])
            g["resumen_fast_detectgpt"] = _resumen(g["fast_detectgpt"])
    grupos: dict[str, list] = {}
    for p in parrafos:
        partes = p["seccion"].split(" › ")
        grupos.setdefault(" › ".join(partes[:2]), []).append(p)
    secciones = []
    for nombre, ps in grupos.items():
        tok = sum(p["tokens"] for p in ps) or 1
        fila = {"seccion": nombre, "parrafos": len(ps), "tokens": tok}
        for m in ("binoculars", "fast_detectgpt"):
            vals = [(p[m], p["tokens"]) for p in ps if p[m] is not None]
            fila[m + "_media_ponderada"] = round(sum(v * t for v, t in vals) / sum(t for _, t in vals), 4) if vals else None
            fila[m + "_mediana"] = round(statistics.median(v for v, _ in vals), 4) if vals else None
            if ref:
                for grupo, g in ref["grupos"].items():
                    fila[f"pos_{m}_{grupo}"] = _posicion(fila[m + "_mediana"], g[m])
        secciones.append(fila)
    return {**base, "disponible": True, "motivo": "",
            "modelos": {"base (observador/muestreo)": modelos.nombres[0],
                        "instruct (intérprete/puntuación)": modelos.nombres[1]},
            "dispositivo": modelos.dispositivo, "parrafos": parrafos, "secciones": secciones,
            "referencia": ref,
            "aviso_referencia": None if ref else "Sin conjunto de referencia: el número no se interpreta."}
