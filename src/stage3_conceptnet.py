"""
Etapa 3 — Labels semánticos via ConceptNet.

Estrategia (en orden):
  1. Cache de extracción previa (cache/conceptnet_extracted.json) — instantáneo.
  2. API REST de ConceptNet — si responde (actualmente con 502 frecuentes).
  3. Descarga del CSV de aserciones (~1.1 GB) en modo streaming:
       - se guarda en cache/ para reutilización
       - se procesa línea a línea sin descomprimir completo
       - se extraen SOLO las líneas relevantes para las clases ETH-80
       - resultado neto almacenado: ~5 KB
  4. Fallback curado (último recurso, sin fidelidad teórica).
"""
import gzip
import json
import time
import requests
from pathlib import Path

ROOT = Path(__file__).parent.parent
CACHE_DIR = ROOT / "cache"
CACHE_DIR.mkdir(exist_ok=True)

CLASSES = ["apple", "car", "cow", "cup", "dog", "horse", "pear", "tomato"]
# IsA + HasProperty + HasPart (spec) + RelatedTo + HasA + MadeOf + CapableOf.
# En ConceptNet 5.7 el grueso de las propiedades cualitativas (red, round, fast)
# está en /r/RelatedTo — omitirla deja solo ~3 labels por concepto.
RELATIONS = {
    "/r/HasProperty",
    "/r/IsA",
    "/r/HasPart",
    "/r/RelatedTo",
    "/r/HasA",
    "/r/MadeOf",
    "/r/CapableOf",
}
TAU = 1.0
# Tope de labels por clase: equilibra el vocabulario para que ninguna clase
# domine el routing por tamaño (clases pobres ~10-12, ricas se recortan aquí).
MAX_LABELS = 20
# Ruido de polisemia / términos no visuales que ConceptNet asocia con peso alto
# pero contaminan el routing (Apple Inc. vs manzana-fruta; cf. condición F).
NOISE_LABELS = {
    "adam", "eve", "eden", "computer", "mac", "macintosh", "ipod", "iphone",
    "ipad", "steve", "jobs", "logo", "company", "corporation", "inc",
    "digital", "unit", "carriage", "woman", "family", "warden", "eated",
}

BASE_URL = "https://api.conceptnet.io"
ASSERTIONS_URL = (
    "https://s3.amazonaws.com/conceptnet/downloads/2019/edges/"
    "conceptnet-assertions-5.7.0.csv.gz"
)
ASSERTIONS_GZ   = CACHE_DIR / "conceptnet-assertions-5.7.0.csv.gz"
EXTRACTED_CACHE = CACHE_DIR / "conceptnet_extracted.json"

# Curado: último recurso si todo lo anterior falla
FALLBACK_LABELS = {
    "apple": {
        "fruit": 8.1, "red": 4.2, "round": 3.8, "sweet": 3.1,
        "edible": 3.0, "food": 2.8, "seed": 2.5, "green": 2.4,
        "tree": 2.3, "plant": 2.2,
    },
    "horse": {
        "animal": 7.5, "fast": 4.5, "large": 4.8, "mammal": 4.2,
        "leg": 3.9, "tail": 3.5, "mane": 3.3, "hoof": 3.1,
        "ride": 2.8, "strong": 2.6,
    },
    "car": {
        "vehicle": 7.8, "fast": 6.2, "wheel": 5.5, "engine": 4.9,
        "door": 4.2, "metal": 3.8, "road": 3.5, "speed": 3.2,
        "transport": 3.0, "large": 2.4,
    },
}


# ---------------------------------------------------------------------------
# 1. Cache de extracción previa
# ---------------------------------------------------------------------------

def _load_extracted_cache() -> dict | None:
    if not EXTRACTED_CACHE.exists():
        return None
    try:
        data = json.loads(EXTRACTED_CACHE.read_text())
        if all(c in data for c in CLASSES):
            print(f"  Usando cache de extraccion previa: {EXTRACTED_CACHE.name}")
            return data
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# 2. API REST (rápida si funciona)
# ---------------------------------------------------------------------------

def _try_api(concept: str) -> dict:
    """Retorna {label: weight} desde la API. Vacío si falla."""
    aggregated: dict = {}
    for rel in RELATIONS:
        url = f"{BASE_URL}/query"
        params = {"start": f"/c/en/{concept}", "rel": rel, "limit": 50}
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            for edge in resp.json().get("edges", []):
                uri = edge.get("end", {}).get("@id", "")
                if not uri.startswith("/c/en/"):
                    continue
                label = uri[len("/c/en/"):].split("/")[0].lower()
                if "_" in label or label == concept or not label.isalpha():
                    continue
                w = float(edge.get("weight", 1.0))
                if w >= TAU:
                    aggregated[label] = max(aggregated.get(label, 0.0), w)
        except Exception:
            pass
        time.sleep(0.3)
    return aggregated


def _try_all_api() -> dict | None:
    """Intenta la API para todos los conceptos. Retorna None si alguno falla."""
    print("  Probando API REST de ConceptNet...")
    all_data = {}
    for cls in CLASSES:
        data = _try_api(cls)
        if not data:
            print(f"  API no disponible para '{cls}' — descartando.")
            return None
        all_data[cls] = data
        print(f"  API OK para '{cls}': {len(data)} labels")
    return all_data


# ---------------------------------------------------------------------------
# 3. Descarga + streaming del CSV de aserciones
# ---------------------------------------------------------------------------

def _download_assertions() -> bool:
    """Descarga el .gz a cache/. Retorna True si el archivo queda disponible."""
    min_expected = 400_000_000  # >400 MB = descarga completa (~498 MB real)

    if ASSERTIONS_GZ.exists() and ASSERTIONS_GZ.stat().st_size > min_expected:
        print(f"  Archivo de aserciones ya descargado: {ASSERTIONS_GZ.name} "
              f"({ASSERTIONS_GZ.stat().st_size / 1e9:.2f} GB)")
        return True

    print(f"\n  Descargando ConceptNet assertions (~500 MB)...")
    print(f"  URL: {ASSERTIONS_URL}")
    print(f"  Destino: {ASSERTIONS_GZ}")
    print(f"  (esto se hace UNA SOLA VEZ; el archivo queda en cache/ para reutilizacion)\n")

    try:
        with requests.get(ASSERTIONS_URL, stream=True, timeout=60) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            downloaded = 0
            with open(ASSERTIONS_GZ, "wb") as f:
                for chunk in r.iter_content(chunk_size=512 * 1024):  # 512 KB chunks
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = 100.0 * downloaded / total
                        mb = downloaded / 1e6
                        print(f"\r  {pct:5.1f}%  {mb:7.0f} MB / {total/1e6:.0f} MB", end="", flush=True)
        print(f"\n  Descarga completa: {ASSERTIONS_GZ.stat().st_size / 1e9:.2f} GB")
        return True
    except Exception as e:
        print(f"\n  Error en descarga: {e}")
        if ASSERTIONS_GZ.exists():
            ASSERTIONS_GZ.unlink()
        return False


def _stream_extract(gz_path: Path) -> dict:
    """
    Lee línea a línea el .gz, extrae SOLO las aserciones de las clases ETH-80.
    Formato TSV: assertion_id \\t relation \\t start \\t end \\t json_meta
    """
    if EXTRACTED_CACHE.exists():
        try:
            cached = json.loads(EXTRACTED_CACHE.read_text())
            if all(c in cached for c in CLASSES):
                return cached
        except Exception:
            pass

    results: dict = {c: {} for c in CLASSES}
    concept_uris = {f"/c/en/{c}": c for c in CLASSES}

    print(f"\n  Procesando aserciones en streaming...")
    print(f"  (buscando {len(CLASSES)} conceptos en ~34M lineas)\n")

    line_count = 0
    match_count = 0

    with gzip.open(gz_path, "rt", encoding="utf-8", errors="replace") as f:
        for raw_line in f:
            line_count += 1
            if line_count % 2_000_000 == 0:
                print(f"\r  {line_count/1e6:.0f}M lineas... {match_count} coincidencias",
                      end="", flush=True)

            # Pre-filtro rápido antes de parsear
            if not any(uri in raw_line for uri in concept_uris):
                continue

            parts = raw_line.rstrip("\n").split("\t")
            if len(parts) != 5:
                continue

            _, rel, start, end, meta_str = parts

            if rel not in RELATIONS:
                continue

            # Identificar concepto de inicio (exact match o sub-tipo /c/en/car/n)
            concept = None
            for uri, name in concept_uris.items():
                if start == uri or start.startswith(uri + "/"):
                    concept = name
                    break
            if concept is None:
                continue

            # El destino debe ser inglés
            if not end.startswith("/c/en/"):
                continue

            # Extraer label simple (sin subtipo ni multi-palabra)
            label = end[len("/c/en/"):].split("/")[0].lower()
            if "_" in label or label == concept or not label.isalpha():
                continue

            # Extraer peso del JSON de metadatos
            try:
                meta = json.loads(meta_str)
                weight = float(meta.get("weight", 1.0))
            except Exception:
                weight = 1.0

            if weight < TAU:
                continue

            results[concept][label] = max(results[concept].get(label, 0.0), weight)
            match_count += 1

    print(f"\n  Streaming completo: {line_count/1e6:.1f}M lineas, {match_count} coincidencias")

    # Guardar extracción en cache pequeño (~5 KB)
    EXTRACTED_CACHE.write_text(json.dumps(results, indent=2))
    print(f"  Cache guardado: {EXTRACTED_CACHE.name}")
    return results


def _extract_from_assertions() -> dict | None:
    """Orquesta descarga + streaming. Retorna datos o None si falla."""
    if not _download_assertions():
        return None
    return _stream_extract(ASSERTIONS_GZ)


# ---------------------------------------------------------------------------
# Punto de entrada público
# ---------------------------------------------------------------------------

def get_conceptnet_labels() -> dict:
    """
    Retorna {cls: {label: weight}} para todos los CLASSES.
    Intenta en orden: cache > API > assertions CSV > fallback curado.
    """
    # 1. Cache de extracción previa
    cached = _load_extracted_cache()
    if cached:
        return cached

    # 2. API REST
    api_data = _try_all_api()
    if api_data:
        EXTRACTED_CACHE.write_text(json.dumps(api_data, indent=2))
        print(f"  Cache guardado: {EXTRACTED_CACHE.name}")
        return api_data

    # 3. CSV de aserciones (descarga + streaming)
    print("\n  API no disponible. Descargando CSV de aserciones ConceptNet...")
    csv_data = _extract_from_assertions()
    if csv_data and any(csv_data[c] for c in CLASSES):
        return csv_data

    # 4. Fallback curado (avisa explícitamente)
    print("\n  ADVERTENCIA: usando fallback curado (sin fidelidad teorica).")
    print("  Para datos reales ejecuta de nuevo cuando ConceptNet API responda,")
    print("  o verifica que la URL de descarga sea accesible.")
    return {c: dict(FALLBACK_LABELS[c]) for c in CLASSES}


def find_shared_labels(label_dicts: dict) -> list:
    """Labels que aparecen en 2+ dominios."""
    from collections import Counter
    cnt = Counter()
    for labels in label_dicts.values():
        cnt.update(labels.keys())
    return [label for label, count in cnt.items() if count >= 2]


def run():
    print("=== Etapa 3: Labels semanticos via ConceptNet ===\n")
    all_data = get_conceptnet_labels()

    all_labels = {}
    other_class_names = set(CLASSES)
    for cls in CLASSES:
        raw = all_data.get(cls, {})
        # Aplicar threshold τ; quitar ruido de polisemia y los NOMBRES de otras
        # clases (p.ej. apple no debe tener "pear"); quedarse con las MAX_LABELS
        # de mayor peso: da vocabulario real a las clases pobres sin dejar que
        # las ricas dominen el routing por puro tamaño de vocabulario.
        others = other_class_names - {cls}
        filtered = {l: w for l, w in raw.items()
                    if w >= TAU and l not in NOISE_LABELS and l not in others}
        top = sorted(filtered.items(), key=lambda x: -x[1])[:MAX_LABELS]
        freq = {l: max(1, round(w)) for l, w in top}
        # El NOMBRE PROPIO de la clase es su label más distintivo (una consulta
        # que dice "pear" debe rutear a pear). ConceptNet no siempre lo incluye,
        # así que lo añadimos con frecuencia alta. Es crítico para clases con
        # vocabulario pobre (pear/tomato), cuyo único token distintivo es su nombre.
        freq[cls] = max(freq.values(), default=1)
        all_labels[cls] = freq

        out_path = ROOT / f"labels_{cls}.json"
        out_path.write_text(json.dumps(freq, indent=2))
        top = sorted(freq.items(), key=lambda x: -x[1])[:8]
        print(f"\n  {cls} ({len(freq)} labels, tau={TAU}):")
        for label, f in top:
            print(f"    {label}: {f}")

    shared = find_shared_labels(all_labels)
    print(f"\nLabels compartidos entre 2+ dominios ({len(shared)}): {shared}")

    if len(shared) == 0:
        print("ADVERTENCIA: sin labels compartidos — routing trivial.")
    else:
        print("\nEtapa 3 COMPLETADA.")

    return all_labels, shared


if __name__ == "__main__":
    run()
