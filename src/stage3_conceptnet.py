"""
Etapa 3 — Labels semánticos via ConceptNet.

Estrategia (orden real de get_conceptnet_labels):
  1. Cache de extracción previa versionado (cache/conceptnet_extracted.json,
     EXTRACT_VERSION) — instantáneo.
  2. CSV de aserciones si YA está descargado en cache/ (extracción bidireccional
     determinista) — antes que la API, que solo da aristas salientes.
  3. API REST de ConceptNet (fallback en línea; a menudo con 502).
  4. Descarga del CSV de aserciones (~500 MB) + streaming:
       - se guarda en cache/ para reutilización
       - se procesa línea a línea sin descomprimir completo
       - se extraen SOLO las líneas relevantes para las clases ETH-80
       - resultado neto almacenado: ~5 KB
  5. Fallback curado (último recurso, solo cubre apple/horse/car — con más
     clases, ABORTA en vez de fabricar labels, por fidelidad).
"""
import gzip
import json
import time
import requests
import numpy as np
from pathlib import Path

ROOT = Path(__file__).parent.parent
CACHE_DIR = ROOT / "cache"
CACHE_DIR.mkdir(exist_ok=True)

CLASSES = ["apple", "car", "cow", "cup", "dog", "horse", "pear", "tomato"]
# En ConceptNet 5.7 el grueso de las propiedades cualitativas (red, round, fast)
# está en /r/RelatedTo — omitirla deja solo ~3 labels por concepto. El set se
# amplió (v4.1) con relaciones semánticas adicionales porque las clases pobres
# (pear/tomato) quedaban con ~10 candidatos crudos y su experto nunca
# presenciaba sus propias palabras distintivas: apple capturaba sus queries.
RELATIONS = {
    "/r/HasProperty",
    "/r/IsA",
    "/r/HasPart",
    "/r/RelatedTo",
    "/r/HasA",
    "/r/MadeOf",
    "/r/CapableOf",
    "/r/AtLocation",
    "/r/UsedFor",
    "/r/PartOf",
    "/r/Synonym",
    "/r/SimilarTo",
    # /r/DerivedFrom se probó y se DESCARTÓ: aporta casi solo morfología
    # (pearlike, tomatoless, tomatoey) que desplaza candidatos semánticos
    # reales del cap por clase.
}
TAU = 1.0
# Piso de vocabulario por clase: si tras el filtro τ una clase queda por
# debajo, se relaja τ SOLO para ella (tomando por peso descendente) hasta
# alcanzar el piso. Balancea el conocimiento entre expertos sin curación
# manual: todo label sigue saliendo de ConceptNet.
MIN_LABELS = 15
# Tope de labels por clase: equilibra el vocabulario para que ninguna clase
# domine el routing por tamaño (clases pobres ~10-12, ricas se recortan aquí).
MAX_LABELS = 20
# No se filtra por coseno entre el candidato y el nombre de la clase: el
# nombre es polisémico en fastText ("cup" queda dominado por World Cup y poda
# drink/mug/glass; "apple" por Apple Inc. y poda red/green/core). El filtrado
# se hace por masa asociativa y por representabilidad: un candidato sin vector
# fastText real queda fuera.
# Versión del formato/parámetros de extracción: invalida el cache crudo
# cuando cambian RELATIONS o la direccionalidad (v2 = bidireccional;
# v3 = sin DerivedFrom + solo labels ASCII; v4 = el peso de un label es la
# MASA ASOCIATIVA acumulada — suma de pesos de todas sus aserciones, no el
# máximo: un label respaldado por varias aristas pesa más que uno casual).
EXTRACT_VERSION = 4
# Ruido de polisemia / términos no visuales que ConceptNet asocia con peso alto
# pero contaminan el routing (Apple Inc. vs manzana-fruta; cf. condición F).
NOISE_LABELS = {
    "adam", "eve", "eden", "computer", "mac", "macintosh", "ipod", "iphone",
    "ipad", "steve", "jobs", "logo", "company", "corporation", "inc",
    "digital", "unit", "carriage", "woman", "family", "warden", "eated",
    # polisemia detectada en v4: "pear of anguish" (instrumento de tortura)
    "torture",
    # ruido detectado en la extracción bidireccional v4.1: ficción de Los
    # Simpson asociada a tomato, y geografía no visual compartida entre clases
    "tomacco", "sacratomato", "canada",
    # fragmento no-palabra ("es") y polisemia verbal ("to cow/overawe")
    "es", "overawe",
}

BASE_URL = "https://api.conceptnet.io"
ASSERTIONS_URL = (
    "https://s3.amazonaws.com/conceptnet/downloads/2019/edges/"
    "conceptnet-assertions-5.7.0.csv.gz"
)
ASSERTIONS_GZ   = CACHE_DIR / "conceptnet-assertions-5.7.0.csv.gz"
EXTRACTED_CACHE = CACHE_DIR / "conceptnet_extracted.json"

# Curado: último recurso si todo lo anterior falla. SOLO cubre apple/horse/car
# (reliquia de la era de 3 clases); get_conceptnet_labels ABORTA si CLASSES
# incluye una clase ausente aquí, en vez de fabricar labels a mano (fidelidad).
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
        version_ok = data.get("_meta", {}).get("version") == EXTRACT_VERSION
        if not version_ok:
            print("  Cache de extraccion de version anterior "
                  "(unidireccional/relaciones viejas) — se re-extrae.")
            return None
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


def _match_concept(uri: str, concept_uris: dict):
    """Nombre de la clase si la URI es el concepto (o un sub-tipo /c/en/car/n)."""
    for base, name in concept_uris.items():
        if uri == base or uri.startswith(base + "/"):
            return name
    return None


def _simple_label(uri: str):
    """Label simple en inglés (sin subtipo ni multi-palabra), o None.
    Solo ASCII: el encoder léxico es fastText wiki-news EN; labels con
    diacríticos (beurré, bonchrétien) no tienen vector y solo desplazarían
    candidatos representables del cap por clase."""
    if not uri.startswith("/c/en/"):
        return None
    label = uri[len("/c/en/"):].split("/")[0].lower()
    if "_" in label or not label.isalpha() or not label.isascii():
        return None
    return label


def _stream_extract(gz_path: Path) -> dict:
    """
    Lee línea a línea el .gz, extrae SOLO las aserciones de las clases ETH-80.
    Formato TSV: assertion_id \\t relation \\t start \\t end \\t json_meta

    v2 (bidireccional): una aserción cuenta si el concepto aparece en
    CUALQUIER extremo; el label es el extremo contrario. La asociación
    semántica que interesa (RelatedTo y afines) es simétrica, y solo mirar
    aristas salientes dejaba a pear/tomato con ~10 candidatos (todo lo que
    apunta HACIA ellos — vine, salad, ketchup… — se perdía). No se aplica τ
    aquí: el cache crudo guarda todos los pesos y run() filtra/adapta.
    """
    cached = _load_extracted_cache()
    if cached:
        return cached

    results: dict = {c: {} for c in CLASSES}
    concept_uris = {f"/c/en/{c}": c for c in CLASSES}

    print(f"\n  Procesando aserciones en streaming (bidireccional)...")
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

            # Concepto en cualquiera de los dos extremos; label = el contrario.
            concept = _match_concept(start, concept_uris)
            other = end
            if concept is None:
                concept = _match_concept(end, concept_uris)
                other = start
            if concept is None:
                continue

            label = _simple_label(other)
            if label is None or label == concept:
                continue

            # Extraer peso del JSON de metadatos
            try:
                meta = json.loads(meta_str)
                weight = float(meta.get("weight", 1.0))
            except Exception:
                weight = 1.0

            # v4: masa asociativa acumulada (suma sobre todas las aserciones)
            results[concept][label] = results[concept].get(label, 0.0) + weight
            match_count += 1

    print(f"\n  Streaming completo: {line_count/1e6:.1f}M lineas, {match_count} coincidencias")

    results["_meta"] = {"version": EXTRACT_VERSION,
                        "relations": sorted(RELATIONS),
                        "bidirectional": True}
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
    # 1. Cache de extracción previa (versionado)
    cached = _load_extracted_cache()
    if cached:
        return cached

    # 2. CSV de aserciones si ya está descargado: extracción bidireccional
    #    determinista (la API solo da aristas salientes y depende de la red).
    if ASSERTIONS_GZ.exists():
        csv_data = _stream_extract(ASSERTIONS_GZ)
        if csv_data and any(csv_data.get(c) for c in CLASSES):
            return csv_data

    # 3. API REST (fallback en línea; unidireccional, sin _meta v2 para que
    #    una corrida futura con el CSV disponible la reemplace)
    api_data = _try_all_api()
    if api_data:
        EXTRACTED_CACHE.write_text(json.dumps(api_data, indent=2))
        print(f"  Cache guardado: {EXTRACTED_CACHE.name}")
        return api_data

    # 4. CSV de aserciones (descarga + streaming)
    print("\n  API no disponible. Descargando CSV de aserciones ConceptNet...")
    csv_data = _extract_from_assertions()
    if csv_data and any(csv_data.get(c) for c in CLASSES):
        return csv_data

    # 5. Fallback curado — SOLO para las clases que estén en FALLBACK_LABELS.
    # Fabricar labels curados a mano para clases sin datos reales violaría la
    # fidelidad (contenido inventado); si falta alguna clase, se ABORTA con un
    # mensaje claro en vez de reventar con KeyError o rellenar con datos falsos.
    missing = [c for c in CLASSES if c not in FALLBACK_LABELS]
    if missing:
        raise RuntimeError(
            "ConceptNet no disponible (cache/API/CSV fallaron) y el fallback "
            f"curado no cubre {missing}. No se fabrican labels a mano por "
            "fidelidad: consigue el CSV de aserciones (cache/) o espera a que "
            "la API responda, y re-ejecuta la etapa 3.")
    print("\n  ADVERTENCIA: usando fallback curado (sin fidelidad teorica).")
    print("  Para datos reales ejecuta de nuevo cuando ConceptNet API responda,")
    print("  o verifica que la URL de descarga sea accesible.")
    return {c: dict(FALLBACK_LABELS[c]) for c in CLASSES}


# Frecuencia máxima por label en el llenado: la masa asociativa satura para
# mantener el rango de frecuencias del diseño original (~1-8) y que ningún
# label monopolice la distribución de mem_dom_L.
FREQ_CAP = 8


def _semantic_vectors(all_data: dict) -> dict:
    """Vectores fastText de TODOS los candidatos + nombres de clase, en una
    sola pasada del modelo. Sin fallback: candidato sin vector real queda
    fuera (el mismo criterio de representabilidad del protocolo oficial)."""
    from stage4_fasttext import _stream_lookup
    needed = set(CLASSES)
    for cls in CLASSES:
        needed.update(k for k in all_data.get(cls, {}) if not k.startswith("_"))
    print(f"\n  Verificando representabilidad (vector fastText real) de "
          f"{len(needed)} candidatos, una pasada...")
    return _stream_lookup(needed, allow_fallback=False)


def _cosine(a, b) -> float:
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    return float(np.dot(a, b) / (na * nb)) if na > 0 and nb > 0 else 0.0


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
    vecs = _semantic_vectors(all_data)
    other_class_names = set(CLASSES)
    for cls in CLASSES:
        raw = all_data.get(cls, {})
        # Selección por clase, sin curación manual de contenido:
        #   1. fuera ruido de polisemia y nombres de otras clases,
        #   2. fuera candidatos sin vector fastText real (no representables:
        #      mismo criterio del protocolo oficial de consulta),
        #   3. ranking por masa asociativa acumulada; corte primario τ; si la
        #      clase queda bajo el piso MIN_LABELS se relaja τ solo para ella.
        others = other_class_names - {cls}
        clean, dropped_repr = [], []
        for l, w in sorted(raw.items(), key=lambda x: -x[1]):
            if l.startswith("_") or l in NOISE_LABELS or l in others:
                continue
            if vecs.get(l) is None:
                dropped_repr.append(l)
                continue
            clean.append((l, w))
        # Desempate de la cola de masa 1.0 (aserciones únicas): coseno al
        # CENTROIDE de los labels fuertes de la clase (masa >= 2), no al
        # nombre de la clase (polisémico en fastText: cup≈World Cup). Entre
        # candidatos de igual respaldo en ConceptNet, entra primero el más
        # cercano al conocimiento ya establecido del experto — comice/forelle
        # antes que coma/cadillac en pear. Solo reordena empates: la masa
        # asociativa sigue mandando.
        head = [np.asarray(vecs[l]) for l, w in clean if w >= 2.0]
        if head:
            centroid = np.mean(np.stack(head), axis=0)
            clean.sort(key=lambda lw: (-lw[1],
                                       -_cosine(vecs[lw[0]], centroid)))
        top = [(l, w) for l, w in clean if w >= TAU][:MAX_LABELS]
        if len(top) < MIN_LABELS:
            extra = [(l, w) for l, w in clean if w < TAU]
            top += extra[:MIN_LABELS - len(top)]
        freq = {l: min(FREQ_CAP, max(1, round(w))) for l, w in top}
        if dropped_repr:
            print(f"  {cls}: {len(dropped_repr)} candidatos sin vector "
                  f"fastText, fuera (p.ej. {dropped_repr[:6]})")
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
