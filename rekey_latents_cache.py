"""
Reescribe las claves de results/experimento7/latents_cache.json (y las rutas
de data/eth80/splits.json si existe) para la maquina actual. Ambos archivos
guardan rutas absolutas de la maquina donde se generaron; en otra maquina
exp7, exp8, exp9 y exp10 no encontrarian ninguna imagen en el cache.

La clave se reconstruye a partir de la parte relativa a data/eth80.

Uso: python rekey_latents_cache.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data" / "eth80"
CACHE = ROOT / "results" / "experimento7" / "latents_cache.json"
SPLITS = DATA_DIR / "splits.json"
SPLITS_REL = DATA_DIR / "splits_relative.json"

_REL = re.compile(r"data[\\/]eth80[\\/](.+)$")


def relocate(path: str) -> str:
    m = _REL.search(path)
    if not m:
        raise ValueError(f"ruta sin data/eth80: {path}")
    return str(DATA_DIR / m.group(1).replace("\\", "/"))


def main():
    if not DATA_DIR.exists():
        sys.exit(f"No existe {DATA_DIR}: copia primero data/eth80.")
    if CACHE.exists():
        cache = json.loads(CACHE.read_text())
        new = {relocate(k): v for k, v in cache.items()}
        missing = [k for k in new if not Path(k).exists()]
        CACHE.write_text(json.dumps(new))
        print(f"latents_cache: {len(new)} claves reescritas, {len(missing)} sin archivo en disco")
    if SPLITS_REL.exists():
        rel = json.loads(SPLITS_REL.read_text())
        splits = {cls: {k: [str(DATA_DIR / p) for p in v] for k, v in d.items()}
                  for cls, d in rel.items()}
        SPLITS.write_text(json.dumps(splits, indent=2))
        print(f"splits.json reescrito desde splits_relative.json ({sum(len(d['train']) + len(d['test']) for d in splits.values())} rutas)")
    elif SPLITS.exists():
        s = json.loads(SPLITS.read_text())
        s = {cls: {k: [relocate(p) for p in v] for k, v in d.items()} for cls, d in s.items()}
        SPLITS.write_text(json.dumps(s, indent=2))
        print("splits.json reescrito")


if __name__ == "__main__":
    main()
