"""
Etapa 6 — Fase temprana del sistema transactivo.

Implementa los tres procesos de la memoria transactiva de Wegner:
  asignacion de informacion   cada consulta se asigna al especialista
                              que mejor la reconoce (broadcast + argmax),
  actualizacion de directorio el TME y TODOS los agentes registran
                              (cue -> ganador) en sus directorios,
  coordinacion de recuperacion el ganador evoca el contenido asociado
                              (recall hetero -> decoder -> imagen).

Arquitectura por agente (5 memorias, K = len(CLASSES) agentes):
  mem_dom_L  HomoAssociativeMemory(300,16)   dominio label, pesos por feature
  mem_dom_R  HomoAssociativeMemory(64,32)    dominio latente, pesos por feature
  mem_dom_H  HeteroAssociativeMemory(300,16,64,32)  contenido label <-> latente
  mem_dir    DirectoryMemory(300,16 -> K,2)  quien sabe que (labels)
  mem_dir_R  DirectoryMemory(64,32 -> K,2)   quien sabe que (latentes visuales)

TME (2 memorias):
  mem_dir_L  DirectoryMemory(300,16 -> K,2)  directorio por labels
  mem_dir_R  DirectoryMemory(64,32 -> K,2)   directorio por latentes,
             se entrena en la etapa 7 con percepciones visuales
"""
import hashlib
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from associative_memory import HomoAssociativeMemory, DirectoryMemory
from quantizer import quantize_binary

CLASSES = ["apple", "car", "cow", "cup", "dog", "horse", "pear", "tomato"]
AGENT_LIST = CLASSES
N, M_LABEL = 300, 16
P_LATENT, Q_LATENT = 64, 32
MODELS_DIR = ROOT / "models"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_nlp():
    import spacy
    return spacy.load("en_core_web_sm")


ACCEPTED_POS = {"NOUN", "ADJ", "PROPN"}


def tokenize_query(query: str, nlp) -> list:
    """Lemas NOUN/ADJ/PROPN sin stopwords, deduplicados preservando el
    orden de aparicion (un set desordenado haria no determinista que
    token alimenta el recall)."""
    doc = nlp(query.lower())
    tokens = []
    seen = set()
    for tok in doc:
        if tok.is_stop or not tok.is_alpha:
            continue
        if tok.pos_ not in ACCEPTED_POS:
            continue
        if tok.lemma_ not in seen:
            seen.add(tok.lemma_)
            tokens.append(tok.lemma_)
    return tokens


class Agent:
    """Especialista de dominio con sus cuatro memorias asociativas."""

    def __init__(self, name: str, mem_dom_H,
                 mem_dom_L: HomoAssociativeMemory = None,
                 mem_dom_R: HomoAssociativeMemory = None):
        self.name = name
        self.mem_dom_H = mem_dom_H
        self.mem_dom_L = mem_dom_L if mem_dom_L is not None \
            else HomoAssociativeMemory(N, M_LABEL)
        self.mem_dom_R = mem_dom_R if mem_dom_R is not None \
            else HomoAssociativeMemory(P_LATENT, Q_LATENT)
        # Directorios transactivos por agente (Wegner): uno por modalidad de pista.
        #   mem_dir   : pista de texto  (label 300x16) -> agente
        #   mem_dir_R : pista de imagen (latente 64x32) -> agente
        # Mismo destino (identidad de agente), dos espacios de entrada distintos,
        # por eso son dos DirectoryMemory (una HAM no admite dos formas de pista).
        self.mem_dir = DirectoryMemory(N, M_LABEL, len(AGENT_LIST))
        self.mem_dir_R = DirectoryMemory(P_LATENT, Q_LATENT, len(AGENT_LIST))

    def recognize(self, v_label_q: np.ndarray) -> float:
        """Score crudo: activacion media sin gate ni calibracion.
        Lo conserva el ablation como condicion de linea base; el
        protocolo oficial usa recognize_gated."""
        left_weights = self.mem_dom_L.recog_weights(v_label_q)
        return self.mem_dom_H.recognize_from_left(v_label_q,
                                                  left_weights=left_weights)

    def recognize_gated(self, v_label_q: np.ndarray) -> float:
        """Score oficial de routing: activacion media de la proyeccion,
        gateada por containment (mismo criterio de pertenencia que el
        recall: una fila vacia significa que el cue no esta contenido
        en la relacion y el agente no opina).

        Con el llenado por instancias las masas de las memorias quedan
        igualadas por construccion, asi que la activacion media es
        directamente comparable entre agentes sin calibracion adicional.
        """
        import io as _io
        import contextlib as _ctx
        l_w = self.mem_dom_L.recog_weights(v_label_q)
        mx = l_w.max()
        weights = (l_w / mx) if mx > 0 else np.ones(len(v_label_q),
                                                    dtype=float)
        mem_H = self.mem_dom_H
        ca = mem_H.validate(v_label_q, 0)
        with _ctx.redirect_stdout(_io.StringIO()):
            proj = mem_H.project(ca, weights, 0)
        if np.count_nonzero(np.sum(proj, axis=1) == 0) > 0:
            return 0.0
        count = int(np.count_nonzero(proj))
        return float(np.sum(proj)) / count if count > 0 else 0.0

    def recall(self, v_label_q: np.ndarray):
        """label -> latente via la memoria de contenido."""
        return self.mem_dom_H.recall_from_left(v_label_q)

    def update_directory(self, v_label_q: np.ndarray, winner_idx: int):
        """Wegner: tambien los no-ganadores anotan quien gano (pista de texto)."""
        self.mem_dir.register(v_label_q, winner_idx)

    def update_directory_latent(self, v_latent_q: np.ndarray, winner_idx: int):
        """Wegner para el hemisferio visual: cada agente anota qué agente ganó
        esta percepción de imagen en su propio directorio visual. Solo se
        registran percepciones reales, nunca ecos del recall."""
        self.mem_dir_R.register(v_latent_q, winner_idx)


class TME:
    """Mediador transactivo: mantiene los directorios compartidos.

    Activo solo en la fase temprana; en la madura los agentes rutean
    punto a punto con sus propios directorios y el TME queda fuera
    del circuito.
    """

    def __init__(self):
        self.mem_dir_L = DirectoryMemory(N, M_LABEL, len(AGENT_LIST))
        self.mem_dir_R = DirectoryMemory(P_LATENT, Q_LATENT, len(AGENT_LIST))

    def update_directory(self, v_label_q: np.ndarray, winner_idx: int):
        self.mem_dir_L.register(v_label_q, winner_idx)

    def update_directory_latent(self, v_latent_q: np.ndarray,
                                winner_idx: int):
        """Registra una percepcion visual (latente de imagen real).
        Las salidas del recall no se registran nunca: el directorio
        indexa experiencias, no ecos de la propia memoria."""
        self.mem_dir_R.register(v_latent_q, winner_idx)


_TOKENS_CACHE_PATH = ROOT / "models" / "token_vectors.json"


def get_fasttext_vector(word: str, vectors_cache: dict,
                        allow_fallback: bool = False):
    """Pista vectorial del token, o None si no hay representacion real.

    Orden de busqueda:
      1. cache de labels (incluye alias por lema),
      2. bucket de tokens ya pre-vectorizados (vectors_cache['_tokens']),
      3. fastText real (stream del modelo) — se memoiza en el bucket.
    Con allow_fallback=False (protocolo oficial) una palabra fuera del
    vocabulario fastText devuelve None: el rechazo lo decide la EAM, no un
    vector sintetico. allow_fallback=True (solo debug) sintetiza un vector
    determinista para no romper demos exploratorias."""
    for cls in CLASSES:
        if word in vectors_cache.get(cls, {}):
            return np.array(vectors_cache[cls][word])

    bucket = vectors_cache.setdefault("_tokens", {})
    if word in bucket:
        v = bucket[word]
        return None if v is None else np.asarray(v, dtype=np.float32)

    v = None
    try:
        from stage4_fasttext import get_vector
        v = get_vector(word, allow_fallback=allow_fallback)
    except Exception:
        v = None
    if v is None and allow_fallback:
        seed = int(hashlib.md5(word.encode("utf-8")).hexdigest()[:8], 16)
        v = np.random.RandomState(seed).choice([-1.0, 1.0], 300).astype(np.float32)

    bucket[word] = None if v is None else np.asarray(v, dtype=np.float32)
    return bucket[word]


def prevectorize(vectors_cache: dict, tokens, allow_fallback: bool = False,
                 persist: bool = True) -> dict:
    """Vectoriza todos los `tokens` en UNA pasada de stream (el modelo pesa
    1 GB; un lookup por palabra suelto seria inviable). Llena
    vectors_cache['_tokens'] (incluyendo None para los no representables) para
    que get_fasttext_vector no vuelva a tocar el modelo. Opcionalmente persiste
    un cache en models/token_vectors.json para corridas reproducibles sin el
    .gz."""
    bucket = vectors_cache.setdefault("_tokens", {})
    if persist and not bucket and _TOKENS_CACHE_PATH.exists():
        try:
            raw = json.loads(_TOKENS_CACHE_PATH.read_text())
            bucket.update({k: (None if v is None else np.asarray(v, dtype=np.float32))
                           for k, v in raw.items()})
        except Exception:
            pass

    needed = set()
    for t in tokens:
        if any(t in vectors_cache.get(cls, {}) for cls in CLASSES):
            continue
        if t in bucket:
            continue
        needed.add(t)

    if needed:
        from stage4_fasttext import _stream_lookup
        found = _stream_lookup(set(needed), allow_fallback=allow_fallback)
        for t in needed:
            v = found.get(t)
            bucket[t] = None if v is None else np.asarray(v, dtype=np.float32)
        if persist:
            try:
                _TOKENS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
                serial = {k: (None if v is None else np.asarray(v).tolist())
                          for k, v in bucket.items()}
                _TOKENS_CACHE_PATH.write_text(json.dumps(serial))
            except Exception:
                pass
    return vectors_cache


def token_in_vocabulary(word: str, vectors_cache: dict) -> bool:
    """SOLO para logging/analisis: indica si el token pertenece al vocabulario
    de labels de ConceptNet. NO debe usarse para decidir routing ni rechazo —
    eso lo decide la EAM (recognize_gated) sobre la pista vectorial."""
    return any(word in vectors_cache.get(cls, {}) for cls in CLASSES)


def load_all_vectors(nlp=None) -> dict:
    """Carga los vectores de labels. Con nlp se agregan alias por lema:
    los labels de ConceptNet vienen sin lematizar (wheels, hooves) y las
    consultas se lematizan, asi que sin el alias 'wheel' quedaria fuera
    de vocabulario aunque 'wheels' este registrado."""
    cache = {}
    for cls in CLASSES:
        path = ROOT / f"label_vectors_{cls}.json"
        cache[cls] = json.loads(path.read_text())
    if nlp is not None:
        for cls in CLASSES:
            aliases = {}
            for word, vec in cache[cls].items():
                lemma = nlp(word)[0].lemma_
                if lemma != word and lemma not in cache[cls]:
                    aliases[lemma] = vec
            cache[cls].update(aliases)
    return cache


def process_query(query: str, agents: dict, tme: TME, nlp,
                  vectors_cache: dict, decoder, verbose: bool = True,
                  allow_fallback: bool = False) -> dict:
    """Una interaccion de fase temprana completa.

    Devuelve el triple de Wegner (imagen, labels, ubicacion) o el rechazo
    explicito. Hay dos clases de rechazo, distintas conceptualmente:
      - no_representable_tokens: ningun token tiene vector fastText real, asi
        que no hay pista que entregar a la memoria (frontera del encoder
        linguistico, no decision de la EAM);
      - mae_no_support: hay pistas representables pero ningun agente produce
        soporte (max score == 0). Este es el rechazo que decide la EAM.
    No se usa token_in_vocabulary como filtro: el vocabulario de labels llena la
    memoria, no censura consultas. Una palabra real que no sea label (p.ej.
    'powerful') entra como pista y la EAM la rechaza sola via recognize_gated.
    """
    tokens = tokenize_query(query, nlp)
    if not tokens:
        return {"query": query, "tokens": [], "winner": None,
                "image": None, "labels": [], "agent": None,
                "rejected": True, "reason": "no_tokens",
                "represented_tokens": [], "unrepresented_tokens": [],
                "token_logs": []}

    if verbose:
        print(f"  Query: '{query}'  tokens={tokens}")

    agent_scores = {cls: 0.0 for cls in CLASSES}
    token_vectors = {}
    unrepresented_tokens = []
    token_logs = []
    for tok in tokens:
        vec = get_fasttext_vector(tok, vectors_cache, allow_fallback=allow_fallback)
        if vec is None:
            unrepresented_tokens.append(tok)
            token_logs.append({"token": tok, "representable": False,
                               "in_label_vocab": token_in_vocabulary(tok, vectors_cache),
                               "reason": "no_fasttext_vector"})
            continue
        v_q = quantize_binary(vec, M_LABEL)
        token_vectors[tok] = v_q
        tok_scores = {cls: agents[cls].recognize_gated(v_q) for cls in CLASSES}
        for cls in CLASSES:
            agent_scores[cls] += tok_scores[cls]
        token_logs.append({"token": tok, "representable": True,
                           "in_label_vocab": token_in_vocabulary(tok, vectors_cache),
                           "scores": tok_scores,
                           "recognized_by_any_agent": max(tok_scores.values()) > 0.0})

    if verbose and unrepresented_tokens:
        print(f"  Tokens no representables (sin vector fastText): {unrepresented_tokens}")

    if not token_vectors:
        if verbose:
            print(f"  RECHAZADA (no_representable_tokens): tokens={tokens}.")
        return {"query": query, "tokens": tokens, "winner": None,
                "image": None, "labels": tokens, "agent": None,
                "rejected": True, "reason": "no_representable_tokens",
                "agent_scores": agent_scores,
                "represented_tokens": list(token_vectors),
                "unrepresented_tokens": unrepresented_tokens,
                "token_logs": token_logs}

    if max(agent_scores.values()) == 0.0:
        if verbose:
            print(f"  RECHAZADA (mae_no_support): la EAM no contiene las pistas.")
        return {"query": query, "tokens": tokens, "winner": None,
                "image": None, "labels": tokens, "agent": None,
                "rejected": True, "reason": "mae_no_support",
                "agent_scores": agent_scores,
                "represented_tokens": list(token_vectors),
                "unrepresented_tokens": unrepresented_tokens,
                "token_logs": token_logs}

    n_toks = len(token_vectors)
    for cls in CLASSES:
        agent_scores[cls] /= n_toks

    winner = max(agent_scores, key=agent_scores.get)
    winner_idx = AGENT_LIST.index(winner)

    if verbose:
        score_str = "  ".join(f"{c}={agent_scores[c]:.2f}" for c in CLASSES)
        print(f"  Scores: {score_str}  -> ganador: {winner}")

    # Actualizacion de directorio en los cuatro componentes.
    for tok, v_q in token_vectors.items():
        tme.update_directory(v_q, winner_idx)
        for agent in agents.values():
            agent.update_directory(v_q, winner_idx)

    # Recuperacion en el ganador con el primer token reconocido.
    recalled_image = None
    stats = json.loads((MODELS_DIR / "latent_global_stats.json").read_text())
    g_min = np.array(stats["global_min"])
    g_max = np.array(stats["global_max"])
    for tok, v_q in token_vectors.items():
        recalled_q, recognized, weight, *_ = agents[winner].recall(v_q)
        if recognized:
            v_norm = recalled_q.astype(float) / (Q_LATENT - 1)
            v_latent = (v_norm * (g_max - g_min) + g_min).astype(np.float32)
            z = torch.tensor(v_latent).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                recalled_image = decoder(z)[0].cpu()
            break

    return {
        "query": query,
        "tokens": tokens,
        "agent_scores": agent_scores,
        "winner": winner,
        "image": recalled_image,
        "labels": tokens,
        "rejected": False,
        "reason": "mae_support",
        "represented_tokens": list(token_vectors),
        "unrepresented_tokens": unrepresented_tokens,
        "token_logs": token_logs,
    }


def load_agents() -> dict:
    from stage5_fill import load_agent_memories
    agents = {}
    for cls in CLASSES:
        mem_H, mem_L, mem_R = load_agent_memories(cls)
        agents[cls] = Agent(cls, mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)
    return agents


def load_decoder():
    from stage2_encoder import Decoder, DEVICE as DEV
    decoder = Decoder().to(DEV)
    decoder.load_state_dict(torch.load(
        MODELS_DIR / "decoder.pt", map_location=DEV))
    decoder.eval()
    return decoder


def save_tme_and_agents(tme: TME, agents: dict):
    with open(MODELS_DIR / "tme.pkl", "wb") as f:
        pickle.dump(tme, f)
    for cls, agent in agents.items():
        with open(MODELS_DIR / f"agent_{cls}.pkl", "wb") as f:
            pickle.dump(agent, f)
    print("TME y agentes guardados.")


def load_tme_and_agents():
    import stage6_interaction as _s6
    # Los pickles guardados desde __main__ requieren este remapeo.
    old_main = sys.modules.get("__main__")
    sys.modules["__main__"] = _s6
    try:
        with open(MODELS_DIR / "tme.pkl", "rb") as f:
            tme = pickle.load(f)
        agents = {}
        for cls in CLASSES:
            with open(MODELS_DIR / f"agent_{cls}.pkl", "rb") as f:
                agents[cls] = pickle.load(f)
    finally:
        if old_main is not None:
            sys.modules["__main__"] = old_main
    return tme, agents


def visualize_result(result: dict, idx: int):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    img = result.get("image")
    if img is None:
        return
    fig, ax = plt.subplots(1, 1, figsize=(4, 4))
    ax.imshow(img.permute(1, 2, 0).numpy().clip(0, 1))
    ax.set_title(f"Q{idx}: '{result.get('query', '')}'\n"
                 f"winner={result.get('winner', '?')}", fontsize=7)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(ROOT / f"stage6_query_{idx:02d}.png", dpi=80)
    plt.close()


# Interacciones de la fase temprana del pipeline oficial: 2 por dominio,
# intercaladas (16 en total). La versión anterior eran las 10 queries de la
# era de 3 clases (apple/horse/car) y dejaba 5 dominios sin presenciar:
# sus directorios quedaban vacíos ("no ruteas lo que no presenciaste").
TEST_QUERIES = [
    "a crunchy red fruit with a core",             # apple
    "fast vehicle with wheels",                    # car
    "farm animal that gives milk",                 # cow
    "a mug for drinking coffee",                   # cup
    "a barking domestic pet",                      # dog
    "animal with a mane",                          # horse
    "sweet green fruit with a narrow neck",        # pear
    "red juicy fruit used in salads",              # tomato
    "sweet fruit from an orchard tree",            # apple
    "machine for transportation with an engine",   # car
    "bovine beast that moos",                      # cow
    "small container for a hot drink",             # cup
    "canine with a wagging tail",                  # dog
    "riding animal with hooves",                   # horse
    "teardrop shaped orchard fruit",               # pear
    "round red fruit growing on a vine",           # tomato
]


def run():
    print("Cargando modelos y agentes...")
    agents = load_agents()
    tme = TME()
    nlp = get_nlp()
    decoder = load_decoder()
    vectors_cache = load_all_vectors(nlp)

    results = []
    print("\n--- Fase temprana (TME activo) ---")
    for i, query in enumerate(TEST_QUERIES):
        res = process_query(query, agents, tme, nlp, vectors_cache, decoder)
        results.append(res)
        visualize_result(res, i)
        print(f"  -> Triple: imagen={'si' if res['image'] is not None else 'no'}, "
              f"labels={res['labels']}, ubicacion={res['winner']}")

    save_tme_and_agents(tme, agents)
    print("\nEtapa 6 COMPLETADA.")
    return tme, agents, results


if __name__ == "__main__":
    run()
