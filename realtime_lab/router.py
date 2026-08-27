"""Puente SOLO-LECTURA al experimento base: carga agentes/vocabulario/
encoder una vez y expone dos rutas rápidas (milisegundos):

- route_text(query): scoring gateado de los 8 agentes (fase temprana,
  sin reconstrucción — el recall estocástico no se necesita en vivo).
- route_frame(bgr): frame de webcam → ResNet18 → latente cuantizado →
  directorio visual del agente de entrada (estilo fase madura).

Nunca escribe en models/ — el experimento queda intacto.
"""
import sys
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

LAB = Path(__file__).resolve().parent
ROOT = LAB.parent
sys.path.insert(0, str(ROOT / "src"))

from quantizer import quantize_binary                        # noqa: E402
from associative_memory import DirectoryMemory               # noqa: E402
from stage6_interaction import (                             # noqa: E402
    CLASSES, MODELS_DIR, Agent, get_nlp, load_all_vectors,
    tokenize_query, get_fasttext_vector, load_tme_and_agents,
    M_LABEL, N, Q_LATENT,
)
from stage5_fill import load_agent_memories, quantize_latent_global  # noqa: E402
from stage7_bidirectional import XI_VISUAL, load_global_stats        # noqa: E402

_IMG_TF = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


class Router:
    def __init__(self, entry_agent: str = "apple", log=print):
        t0 = time.time()
        log("[router] loading text agents…")
        self.agents = {}
        for cls in CLASSES:
            mem_H, mem_L, mem_R = load_agent_memories(cls)
            self.agents[cls] = Agent(cls, mem_H, mem_dom_L=mem_L,
                                     mem_dom_R=mem_R)
        log("[router] loading spaCy + fastText…")
        self.nlp = get_nlp()
        self.vectors = load_all_vectors(self.nlp)

        log("[router] loading visual hemisphere…")
        from stage2_encoder import Encoder, Decoder
        self.encoder = Encoder()
        self.encoder.load_state_dict(
            torch.load(MODELS_DIR / "encoder.pt", map_location="cpu"))
        self.encoder.eval()
        self.decoder = Decoder()
        self.decoder.load_state_dict(
            torch.load(MODELS_DIR / "decoder.pt", map_location="cpu"))
        self.decoder.eval()
        self.g_min, self.g_max = load_global_stats()
        _tme, self.exp_agents = load_tme_and_agents()
        self.entry_agent = entry_agent

        # SESSION M_dir: the directory that learns from what you dictate
        # in early mode (in memory; never touches models/).
        self.session_dir = DirectoryMemory(N, M_LABEL, len(CLASSES))
        self.session_counts = np.zeros(len(CLASSES), dtype=np.int64)

        # Reference color moments (per-channel RGB mean/std over train
        # images): anchor for the adaptive normalization that corrects
        # washed-out/grayish cameras and printer shifts — glasses for
        # the eye, the MAE is untouched. Validated in
        # test_phone_rescue.py (rescued brightness-shift routing).
        import cv2
        import json
        splits = json.loads(
            (ROOT / "data" / "eth80" / "splits.json").read_text())
        means, stds = [], []
        for cls in CLASSES:
            img = cv2.imread(splits[cls]["train"][0])
            if img is None:
                continue
            rgb = cv2.resize(img, (128, 128))[:, :, ::-1].astype(np.float32)
            means.append(rgb.mean(axis=(0, 1)))
            stds.append(rgb.std(axis=(0, 1)))
        self.ref_mean = np.mean(means, axis=0)
        self.ref_std = np.mean(stds, axis=0)
        log(f"[router] ready in {time.time() - t0:.1f}s")

    def _color_fix(self, rgb: np.ndarray) -> np.ndarray:
        """Re-ancla media y desviación por canal a los momentos ETH-80 —
        el antídoto para cámaras grisáceas y corrimiento de impresora.
        No lleva umbral: la política es «reintentar con lentes» SOLO
        cuando el ruteo crudo rechaza (un detector por distancia de
        momentos no separa limpia-colorida de lavada: medido, las
        distribuciones se traslapan)."""
        x = rgb.astype(np.float32)
        m = x.mean(axis=(0, 1))
        s = x.std(axis=(0, 1))
        for c in range(3):
            x[:, :, c] = ((x[:, :, c] - m[c]) / (s[c] + 1e-6)
                          * self.ref_std[c] + self.ref_mean[c])
        return np.clip(x, 0, 255).astype(np.uint8)

    # ---- texto (voz transcrita) ----
    def route_text(self, query: str) -> dict:
        """Scoring gateado promedio sobre tokens representables (pass 1
        del pipeline oficial; sin recall)."""
        t0 = time.time()
        tokens = tokenize_query(query, self.nlp)
        tok_vecs = {}
        for t in tokens:
            v = get_fasttext_vector(t, self.vectors, allow_fallback=False)
            if v is not None:
                tok_vecs[t] = np.asarray(v, dtype=np.float32)
        if not tok_vecs:
            return {"query": query, "tokens": tokens, "scores": None,
                    "winner": None, "rejected": True,
                    "reason": "no representable tokens",
                    "ms": (time.time() - t0) * 1000}
        scores = {cls: 0.0 for cls in CLASSES}
        q_vecs = {}
        for t, v in tok_vecs.items():
            q_v = quantize_binary(v, M_LABEL)
            q_vecs[t] = q_v
            for cls in CLASSES:
                _lw, _raw, gated = self.agents[cls].recognize_both(q_v)
                scores[cls] += gated / len(tok_vecs)
        rejected = max(scores.values()) == 0.0
        winner = None if rejected else max(scores, key=scores.get)
        if winner is not None:
            # Fase temprana = cuando el directorio aprende: registrar
            # cada pista a nombre del ganador en el M_dir de sesión.
            widx = CLASSES.index(winner)
            for q_v in q_vecs.values():
                self.session_dir.register(q_v, widx)
            self.session_counts[widx] += len(q_vecs)
        return {"query": query, "tokens": list(tok_vecs.keys()),
                "q_vecs": q_vecs, "mode": "early", "entry": None,
                "scores": scores, "winner": winner, "rejected": rejected,
                "routed": None,
                "reason": "mae_no_support" if rejected else "ok",
                "ms": (time.time() - t0) * 1000}

    def route_text_mature(self, query: str, entry: str = None) -> dict:
        """Fase madura (protocolo stage8): el AGENTE DE ENTRADA consulta
        SU M_dir entrenado (route_multi, lectura B1) y redirige al
        especialista — o rechaza si su directorio no tiene señal. El TME
        está apagado: es memoria transactiva punto a punto."""
        t0 = time.time()
        entry = entry or self.entry_agent
        tokens = tokenize_query(query, self.nlp)
        q_vecs = {}
        for t in tokens:
            v = get_fasttext_vector(t, self.vectors, allow_fallback=False)
            if v is not None:
                q_vecs[t] = quantize_binary(
                    np.asarray(v, dtype=np.float32), M_LABEL)
        base = {"query": query, "tokens": list(q_vecs.keys()),
                "q_vecs": q_vecs, "mode": "mature", "entry": entry,
                "ms": 0.0}
        if not q_vecs:
            return {**base, "scores": None, "winner": None,
                    "rejected": True, "routed": None,
                    "reason": "no representable tokens"}
        dest_idx, agg = self.exp_agents[entry].mem_dir.route_multi(
            q_vecs.values(), mode="linear")
        scores = {CLASSES[i]: float(agg[i]) for i in range(len(CLASSES))}
        base["ms"] = (time.time() - t0) * 1000
        if dest_idx < 0:
            return {**base, "scores": scores, "winner": None,
                    "rejected": True, "routed": None,
                    "reason": "directory_no_support"}
        winner = CLASSES[dest_idx]
        return {**base, "scores": scores, "winner": winner,
                "rejected": False, "routed": winner != entry,
                "reason": "ok"}

    # ---- evocación (la imagen que el ganador recuerda) ----
    def _decode_q(self, q: np.ndarray) -> np.ndarray:
        """Latente cuantizado → dequantización → decoder → BGR 128²."""
        v_norm = q.astype(float) / (Q_LATENT - 1)
        z = v_norm * (self.g_max - self.g_min) + self.g_min
        zt = torch.tensor(z.astype(np.float32)).unsqueeze(0)
        with torch.no_grad():
            img = self.decoder(zt)[0].clamp(0, 1)
        rgb = (img.permute(1, 2, 0).numpy() * 255).astype(np.uint8)
        return rgb[:, :, ::-1].copy()

    def evoke(self, winner: str, q_vecs: dict) -> dict:
        """Recall completo del ganador (M_dom_H.recall_from_left, el paso
        estocástico lento) → dequantización → decoder → imagen BGR 128².
        Prueba los tokens en orden y devuelve la primera reconstrucción
        reconocida — igual que final_recalled_img del pipeline oficial.

        Además devuelve el PROTOTIPO EMERGENTE (argmax por columna del
        plano proyectado — la "plastilina" leída sin muestreo) y las
        distancias retro-proyectadas de ambos (el test del paper de la
        pista faltante, morales2025missing): el recall oficial ES
        sample-and-search, el mejor de los tres métodos del paper."""
        t0 = time.time()
        for tok, q_v in q_vecs.items():
            mem = self.agents[winner].mem_dom_H
            r_q, recognized, r_weight, *_ = mem.recall_from_left(q_v)
            if not bool(recognized):
                continue
            proto_q, _ = mem.prototype_from_left(q_v)
            d_ss = mem.backward_distance_from_left(q_v, r_q)
            d_proto = (mem.backward_distance_from_left(q_v, proto_q)
                       if proto_q is not None else None)
            return {"img_bgr": self._decode_q(r_q), "token": tok,
                    "weight": float(r_weight),
                    "proto_bgr": (self._decode_q(proto_q)
                                  if proto_q is not None else None),
                    "d_ss": float(d_ss),
                    "d_proto": (None if d_proto is None else float(d_proto)),
                    "ms": (time.time() - t0) * 1000}
        return {"img_bgr": None, "token": None, "weight": 0.0,
                "proto_bgr": None, "d_ss": None, "d_proto": None,
                "ms": (time.time() - t0) * 1000}

    # ---- visión (frame de webcam) ----
    def route_frame(self, bgr: np.ndarray, crop_frac: float = 1.0,
                    entry: str = None) -> dict:
        """Frame BGR → recorte cuadrado central (fracción `crop_frac` del
        lado menor — más chico = la imagen impresa lo llena a distancia
        de enfoque cómoda) → 128×128 → latente → directorio visual del
        agente de entrada. Devuelve también `eye_bgr`: exactamente lo que
        vio el encoder, para mostrarlo en la UI."""
        t0 = time.time()
        h, w = bgr.shape[:2]
        s = max(32, int(min(h, w) * crop_frac))
        y0, x0 = (h - s) // 2, (w - s) // 2
        crop = bgr[y0:y0 + s, x0:x0 + s, ::-1]  # BGR→RGB
        rgb128 = np.asarray(Image.fromarray(crop).resize((128, 128)))
        entry = entry or self.entry_agent
        ag = self.exp_agents[entry]

        def _try(rgb):
            with torch.no_grad():
                z = self.encoder(
                    _IMG_TF(Image.fromarray(rgb)).unsqueeze(0)
                ).cpu().numpy()[0]
            z_q = quantize_latent_global(z, self.g_min, self.g_max,
                                         Q_LATENT)
            agg = ag.mem_dir_R.predict_tolerant(z_q, xi=XI_VISUAL,
                                                mode="linear")
            widx = ag.mem_dir_R.route(z_q, mode="linear", xi=XI_VISUAL)
            return widx, agg

        # Intento 1: crudo (las entradas limpias pasan intactas).
        widx, agg = _try(rgb128)
        fixed = False
        eye_rgb = rgb128
        if widx < 0:
            # Intento 2 — «lentes»: normalización de color a momentos
            # ETH-80; solo se paga cuando el crudo rechaza, así una
            # corrección innecesaria no puede dañar una entrada limpia.
            rgb_fix = self._color_fix(rgb128)
            widx2, agg2 = _try(rgb_fix)
            if widx2 >= 0:
                widx, agg, fixed, eye_rgb = widx2, agg2, True, rgb_fix

        scores = {CLASSES[i]: float(agg[i]) for i in range(len(CLASSES))}
        winner = CLASSES[widx] if widx >= 0 else None
        return {"scores": scores, "winner": winner, "entry": entry,
                "routed": (winner is not None and winner != entry),
                "rejected": winner is None,
                "eye_bgr": eye_rgb[:, :, ::-1].copy(),
                "color_fix": fixed,
                "ms": (time.time() - t0) * 1000}
