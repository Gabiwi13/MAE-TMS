"""
EAM-TMS Visualizador Interactivo v2 — Pipeline Trace completo.

Muestra paso a paso cómo el sistema procesa una query:
  Stage 1 — Sentence Decomposition   (spaCy tokenization + POS)
  Stage 2 — FastText Serialization   (300D vector → binary quantization)
  Stage 3 — TME Broadcast            (v_q sent to ALL agents simultaneously)
  Stage 4 — Per-Agent AMR Processing (M_dom_L weights → M_dom_H score, per agent)
  Stage 5 — TME Decision + M_dir     (argmax winner + M_dir registration)
  Stage 6 — Recall & Reconstruction  (recalled_q → dequantize → decoder → image)

Ejecutar:
  streamlit run app_tme.py

No modifica ningún archivo del experimento core.
"""
import base64
import json
import sys
from io import BytesIO
from pathlib import Path

import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import torch
from PIL import Image
from torchvision import transforms

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from quantizer import quantize_binary, label_scale
from stage6_interaction import (
    CLASSES, AGENT_LIST, MODELS_DIR, Agent,
    get_nlp, load_all_vectors,
    tokenize_query, get_fasttext_vector, token_in_vocabulary,
    M_LABEL, N, P_LATENT, Q_LATENT,
)
from associative_memory import DirectoryMemory

# Visual constants

DOMAIN_COLOR = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60",
                "cow": "#8e44ad", "cup": "#f39c12", "dog": "#16a085",
                "pear": "#7f8c8d", "tomato": "#c0392b"}
DOMAIN_EMOJI = {"apple": "🍎", "horse": "🐴", "car": "🚗",
                "cow": "🐄", "cup": "☕", "dog": "🐕", "pear": "🍐", "tomato": "🍅"}

# Posiciones del grafo de ruteo: TME al centro y los agentes en una elipse,
# generadas desde CLASSES (antes hardcodeadas a las 3 clases originales, lo
# que rompía _routing_graph con el sistema de 8 agentes).
NODE_POS = {"TME": (0.0, 0.0)}
for _i, _cls in enumerate(CLASSES):
    _ang = 2.0 * np.pi * _i / len(CLASSES) + np.pi / 2.0
    NODE_POS[_cls] = (round(2.3 * np.cos(_ang), 3), round(1.9 * np.sin(_ang), 3))


# Model loading (cached — runs once per session)

@st.cache_resource
def load_models():
    from stage2_encoder import Decoder
    from stage5_fill import load_agent_memories

    decoder = Decoder()
    decoder.load_state_dict(
        torch.load(MODELS_DIR / "decoder.pt", map_location="cpu"))
    decoder.eval()

    agents = {}
    for cls in CLASSES:
        mem_H, mem_L, mem_R = load_agent_memories(cls)
        agents[cls] = Agent(cls, mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)

    nlp = get_nlp()
    vectors_cache = load_all_vectors(nlp)

    stats = json.loads((MODELS_DIR / "latent_global_stats.json").read_text())
    g_min = np.array(stats["global_min"])
    g_max = np.array(stats["global_max"])


    splits = json.loads((ROOT / "data" / "eth80" / "splits.json").read_text())
    to_t = transforms.ToTensor()
    ref_imgs = {}
    for cls in CLASSES:
        path = splits[cls]["train"][0]
        img = Image.open(path).convert("RGB").resize((128, 128))
        ref_imgs[cls] = to_t(img)

    return decoder, agents, vectors_cache, g_min, g_max, nlp, ref_imgs


# Hemisferio visual (imagen → etiquetas). Aditivo: no toca load_models.
# El encoder ResNet18 es solo el "ojo" que produce la pista vectorial; el
# reconocimiento, el rechazo y la reconstrucción son de la MAE.

_IMG_TF = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


@st.cache_resource
def load_image_encoder():
    from stage2_encoder import Encoder
    enc = Encoder()
    enc.load_state_dict(
        torch.load(MODELS_DIR / "encoder.pt", map_location="cpu"))
    enc.eval()
    return enc


def encode_pil(img, encoder):
    """PIL → latente. Usa la normalización ImageNet que el encoder espera
    (no la ToTensor cruda)."""
    t = _IMG_TF(img.convert("RGB").resize((128, 128))).unsqueeze(0)
    with torch.no_grad():
        return encoder(t).cpu().numpy()[0]


@st.cache_resource
def load_experiment_state():
    """
    Load the REAL trained TME + agents from the experiment (stage6 output:
    models/tme.pkl + agent_*.pkl). Read-only — the experiment files are
    never modified. Their M_dir memories hold what the system learned
    during the full early-phase run.
    """
    from stage6_interaction import load_tme_and_agents
    return load_tme_and_agents()


@st.cache_resource
def train_mdir_n80(normalized: bool):
    """
    Train a fresh M_dir IN MEMORY by replaying the first 80 queries of the
    8-class evaluation bank (eval_bank.ALL_QUERIES, 10 per class — read-only
    import) through the early phase.

    normalized=True routes each query with the official gated M_dom score
    (recognize_gated, gate de containment) → clean associations; False uses
    raw scores → reproduces the biased learning. Nothing is written to disk;
    cached per mode.

    Returns (mdir, stats) where stats includes routing accuracy vs the
    ablation's ground truth and the learned token→agent vocabulary.
    """
    decoder, agents, vectors_cache, g_min, g_max, nlp, _ = load_models()
    from eval_bank import ALL_QUERIES, GROUND_TRUTH
    from stage6_interaction import prevectorize
    # Pre-vectorizar el banco en una pasada (usa models/token_vectors.json si
    # existe) para no hacer un stream del modelo de 1 GB por palabra.
    _toks = set()
    for _q in ALL_QUERIES[:80]:
        _toks.update(tokenize_query(_q, nlp))
    prevectorize(vectors_cache, _toks, allow_fallback=False)

    mdir = DirectoryMemory(N, M_LABEL, len(CLASSES))
    stats = {"n": 0, "correct": 0, "vocab": {}}

    for query, truth in zip(ALL_QUERIES[:80], GROUND_TRUTH[:80]):
        tokens = tokenize_query(query, nlp)
        # Sin filtro léxico: cada token con vector fastText real entra como
        # pista; los no representables se descartan.
        scores  = {cls: 0.0 for cls in CLASSES}
        tok_vecs = {}
        for tok in tokens:
            v = get_fasttext_vector(tok, vectors_cache, allow_fallback=False)
            if v is None:
                continue
            v_q = quantize_binary(np.asarray(v, dtype=np.float32), M_LABEL)
            tok_vecs[tok] = v_q
            for cls in CLASSES:
                ag  = agents[cls]
                l_w = ag.mem_dom_L.recog_weights(v_q)
                h = (ag.recognize_gated(v_q) if normalized
                     else float(ag.mem_dom_H.recognize_from_left(
                         v_q, left_weights=l_w)))
                scores[cls] += h
        # Rechazo EAM: sin pistas representables o sin soporte, no se asigna
        # ganador por desempate (apple ganaría siempre con scores en cero).
        if not tok_vecs or max(scores.values()) == 0.0:
            stats["n"] += 1
            continue
        winner = max(scores, key=scores.get)
        widx   = AGENT_LIST.index(winner)
        for tok, v_q in tok_vecs.items():
            mdir.register(v_q, widx)
            stats["vocab"][tok] = winner
        stats["n"]       += 1
        stats["correct"] += int(winner == truth)

    return mdir, stats


# Core pipeline computation  (pure — no session-state side effects)

def _dequantize(q_vals, g_min, g_max):
    v_norm = q_vals.astype(float) / (Q_LATENT - 1)
    return (v_norm * (g_max - g_min) + g_min).astype(np.float32)


def _decode(recalled_q, g_min, g_max, decoder):
    z = torch.tensor(_dequantize(recalled_q, g_min, g_max)).unsqueeze(0)
    with torch.no_grad():
        img = decoder(z)[0].clamp(0, 1)
    return img.permute(1, 2, 0).numpy()


def compute_pipeline_trace(query, agents, vectors_cache, g_min, g_max, decoder, nlp,
                           normalize=True):
    """
    Full pipeline trace — pure computation, zero side effects on session state.

    Two-pass design for speed:
      Pass 1 (fast): l_weights + h_score for ALL agents via project() — no sampling.
      Pass 2 (slow): recall_from_left (127-iter stochastic) ONLY for the winner agent.

    normalize=True usa el scoring oficial Agent.recognize_gated (gate de
    containment: activación media de las celdas no nulas). NO divide por
    mem.mean — con el llenado por instancias las masas quedan igualadas y esa
    calibración es redundante (exp. 2). normalize=False usa el score crudo
    h_raw, que reproduce el sesgo de masa histórico para comparación.
    Diagnóstico: crudo 64% → gateado 100%.
    """
    # Stage 1: spaCy decomposition
    doc = nlp(query.lower())
    spacy_tokens = []
    for tok in doc:
        if tok.is_alpha and len(tok.text) > 1:
            spacy_tokens.append({
                "text":    tok.text,
                "lemma":   tok.lemma_,
                "pos":     tok.pos_,
                "dep":     tok.dep_,
                "is_stop": tok.is_stop,
            })

    tokens = tokenize_query(query, nlp)
    if not tokens:
        return None

    # Representación: cada token con vector fastText real entra como pista (sin
    # filtro léxico). token_in_vocabulary queda solo como metadato de display.
    tok_vecs = {}
    for t in tokens:
        v = get_fasttext_vector(t, vectors_cache, allow_fallback=False)
        if v is not None:
            tok_vecs[t] = np.asarray(v, dtype=np.float32)
    tokens_known   = [t for t in tokens if token_in_vocabulary(t, vectors_cache)]
    tokens_unknown = [t for t in tokens if not token_in_vocabulary(t, vectors_cache)]
    if not tok_vecs:
        return None   # no_representable_tokens (frontera del encoder, no EAM)

    # PASS 1: serialization + recognition scores (fast)
    # recog_weights() and recognize_from_left() use only matrix projection —
    # no stochastic sampling, runs in milliseconds.
    per_token = {}
    for tok, raw_v in tok_vecs.items():
        # Paso intermedio REAL de quantize_binary (cuantización por magnitud):
        # v/S recortado a [-1,1] con la escala global S. (La visualización
        # anterior mostraba sign(v), un paso que ya no existe en el pipeline.)
        scaled_v = np.clip(raw_v / label_scale(), -1.0, 1.0)
        q_v      = quantize_binary(raw_v, M_LABEL)

        per_agent = {}
        for cls in CLASSES:
            ag  = agents[cls]
            l_w = ag.mem_dom_L.recog_weights(q_v)
            h_raw = float(ag.mem_dom_H.recognize_from_left(q_v, left_weights=l_w))
            mem_mean = float(ag.mem_dom_H.mean)
            h_score = ag.recognize_gated(q_v) if normalize else h_raw
            per_agent[cls] = {
                "l_weights":     l_w,
                "l_mean":        float(l_w.mean()),
                "l_nonzero":     int((l_w > 0).sum()),
                "h_raw":         h_raw,
                "mem_mean":      mem_mean,
                "h_score":       h_score,
                # recall fields populated in pass 2 for winner only
                "recognized":    None,
                "recall_weight": None,
                "recalled_q":    None,
                "recalled_img":  None,
            }

        per_token[tok] = {
            "raw_vec":    raw_v,
            "scaled_vec": scaled_v,
            "q_vec":      q_v,
            "per_agent":  per_agent,
        }

    # TME decision (after pass 1)
    n_tok = len(per_token)
    avg_scores = {
        cls: sum(per_token[t]["per_agent"][cls]["h_score"]
                 for t in per_token) / n_tok
        for cls in CLASSES
    }
    # Rechazo de la EAM: si ningún agente contiene las pistas, no se declara
    # ganador por desempate (apple ganaría siempre con scores en cero).
    tokens_representable = list(per_token.keys())
    tokens_unrepresentable = [t for t in tokens if t not in per_token]
    if max(avg_scores.values()) == 0.0:
        return {
            "query": query, "spacy_tokens": spacy_tokens, "tokens": tokens,
            "tokens_known": tokens_known, "tokens_unknown": tokens_unknown,
            "tokens_representable": tokens_representable,
            "tokens_unrepresentable": tokens_unrepresentable,
            "per_token": per_token, "avg_scores": avg_scores,
            "winner": None, "winner_idx": None, "n_tokens": n_tok,
            "normalized": bool(normalize), "rejected": True,
            "reason": "mae_no_support",
            "final_recalled_img": None, "final_recalled_tok": None,
        }
    winner     = max(avg_scores, key=avg_scores.get)
    winner_idx = AGENT_LIST.index(winner)

    # PASS 2: full recall for winner only (slow)
    # recall_from_left calls recall_with_sampling_n_search (127 stochastic
    # iterations + hill-climbing). We do this ONLY for the winner agent,
    # not all 3 — reduces calls from n_tokens×3 to n_tokens.
    final_recalled_img = None
    final_recalled_tok = None
    for tok, td in per_token.items():
        q_v = td["q_vec"]
        r_q, recognized, r_weight, *_ = (
            agents[winner].mem_dom_H.recall_from_left(q_v))
        rec_img = None
        if bool(recognized):
            try:
                rec_img = _decode(r_q, g_min, g_max, decoder)
            except Exception:
                pass
        td["per_agent"][winner].update({
            "recognized":    bool(recognized),
            "recall_weight": float(r_weight),
            "recalled_q":    r_q,
            "recalled_img":  rec_img,
        })
        if bool(recognized) and rec_img is not None and final_recalled_img is None:
            final_recalled_img = rec_img
            final_recalled_tok = tok

    return {
        "query":              query,
        "spacy_tokens":       spacy_tokens,
        "tokens":             tokens,
        "tokens_known":       tokens_known,
        "tokens_unknown":     tokens_unknown,
        "tokens_representable":   tokens_representable,
        "tokens_unrepresentable": tokens_unrepresentable,
        "per_token":          per_token,
        "avg_scores":         avg_scores,
        "winner":             winner,
        "winner_idx":         winner_idx,
        "n_tokens":           n_tok,
        "normalized":         bool(normalize),
        "rejected":           False,
        "reason":             "mae_support",
        "final_recalled_img": final_recalled_img,
        "final_recalled_tok": final_recalled_tok,
    }


# Plotly helpers

def _vec_heatmap(vec, title="", rows=15, colorscale="RdBu_r", height=165):
    """Render a 1D float vector as a 2D colour-grid heatmap."""
    n    = len(vec)
    cols = int(np.ceil(n / rows))
    pad  = np.zeros(rows * cols, dtype=float)
    pad[:n] = vec
    grid = pad.reshape(rows, cols)

    fig = go.Figure(go.Heatmap(
        z=grid[::-1],
        colorscale=colorscale,
        showscale=False,
        xgap=0.8, ygap=0.8,
    ))
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=10)),
        height=height,
        margin=dict(l=0, r=0, t=28, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def _routing_graph(avg_scores, winner, title="", highlight_path=None):
    """Plotly routing graph: TME → agents with score annotations."""
    max_score = max(avg_scores.values()) if avg_scores else 1.0
    fig = go.Figure()

    for cls in CLASSES:
        x0, y0 = NODE_POS["TME"]
        x1, y1 = NODE_POS[cls]
        score  = avg_scores.get(cls, 0.0)
        norm   = score / max(max_score, 1e-9)
        is_win = cls == winner
        color  = DOMAIN_COLOR[cls] if is_win else "#c0c0c0"
        width  = 7 if is_win else max(1.0, 3.0 * norm)

        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1], mode="lines",
            line=dict(color=color, width=width),
            hoverinfo="none", showlegend=False,
        ))
        fig.add_annotation(
            x=(x0 + x1) / 2, y=(y0 + y1) / 2,
            text=f"{score:.4f}",
            showarrow=False,
            font=dict(size=10, color=color if is_win else "#999"),
            bgcolor="white", opacity=0.9,
        )

    if highlight_path:
        fx, fy = NODE_POS[highlight_path[0]]
        tx, ty = NODE_POS[highlight_path[1]]
        fig.add_annotation(
            x=tx, y=ty, ax=fx, ay=fy,
            xref="x", yref="y", axref="x", ayref="y",
            arrowhead=3, arrowwidth=5, arrowcolor="#f39c12", text="",
        )

    for name, (nx, ny) in NODE_POS.items():
        is_win = name == winner
        color  = DOMAIN_COLOR.get(name, "#2c3e50")
        label  = f"{DOMAIN_EMOJI.get(name, '')} {name}"
        fig.add_trace(go.Scatter(
            x=[nx], y=[ny],
            mode="markers+text",
            marker=dict(
                size=33 if name == "TME" else (30 if is_win else 22),
                color=color,
                line=dict(width=5 if is_win else 2,
                          color="gold" if is_win else "white"),
            ),
            text=[label],
            textposition=("middle left" if nx < 0
                          else "top center" if ny > 0
                          else "bottom center"),
            textfont=dict(size=13 if is_win else 11, color=color,
                          family="monospace"),
            hoverinfo="text", hovertext=name, showlegend=False,
        ))

    fig.update_layout(
        xaxis=dict(visible=False, range=[-3.4, 3.4]),
        yaxis=dict(visible=False, range=[-2.8, 2.8]),
        height=360, margin=dict(l=10, r=10, t=50, b=10),
        title=dict(text=title, x=0.5, font=dict(size=14)),
        plot_bgcolor="white", paper_bgcolor="#f8f9fa",
    )
    return fig


def _mdir_bar(counts, qn):
    """Bar chart of accumulated M_dir registrations per agent."""
    fig = go.Figure(go.Bar(
        x=[f"{DOMAIN_EMOJI[cls]} {cls}" for cls in CLASSES],
        y=counts.tolist(),
        marker_color=[DOMAIN_COLOR[cls] for cls in CLASSES],
        marker_line_color="white", marker_line_width=2,
        text=[str(int(v)) for v in counts],
        textposition="outside",
    ))
    total = counts.sum()
    ideal = total / len(CLASSES) if total > 0 else 0.0
    if ideal > 0:
        fig.add_hline(y=ideal, line_dash="dot", line_color="#7f8c8d",
                      annotation_text=f"Ideal ({ideal:.0f})",
                      annotation_position="right")
    fig.update_layout(
        title=dict(text=f"M_dir registrations — {qn} queries processed",
                   x=0.5, font=dict(size=13)),
        yaxis_title="Cumulative registrations",
        height=280, margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="white", paper_bgcolor="#f8f9fa", showlegend=False,
    )
    return fig


def _t2img(arr):
    """Convert [0,1] float numpy array to uint8 for st.image."""
    return (np.clip(arr, 0, 1) * 255).astype(np.uint8)


def _img_b64(arr):
    """[0,1] float HxWx3 numpy array → base64 PNG string (for HTML embed)."""
    img = Image.fromarray(_t2img(arr))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


# Animated pipeline flow (HTML/CSS/JS component)

_ANIM_TEMPLATE = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:transparent;font-family:'Segoe UI',system-ui,sans-serif}
#anim{position:relative;width:100%;max-width:1000px;margin:0 auto;
  background:linear-gradient(160deg,#0e1130 0%,#1b1f4b 55%,#101332 100%);
  border-radius:16px;padding:20px 24px 16px;color:#e8eaf6;overflow:hidden;
  box-shadow:0 8px 32px rgba(0,0,0,.35)}
.phase-label{position:absolute;top:16px;right:22px;font-size:11px;letter-spacing:2px;
  color:#8d93c8;text-transform:uppercase;transition:opacity .4s;text-align:right}
#sentence{min-height:46px;font-size:21px;font-style:italic;color:#fff;
  display:flex;align-items:center;justify-content:center;text-align:center;
  transition:opacity .6s}
#caret{display:inline-block;width:2px;height:22px;background:#ffd54f;margin-left:2px;
  animation:blink .7s infinite}
@keyframes blink{50%{opacity:0}}
#words,#tokens{min-height:58px;display:flex;flex-wrap:wrap;gap:8px;
  align-items:center;justify-content:center;padding:4px 0;transition:opacity .6s}
.chip{padding:5px 13px;border-radius:16px;background:#2b3060;color:#dfe3ff;font-size:14px;
  opacity:0;transform:translateY(-14px) scale(.8);
  transition:all .45s cubic-bezier(.2,.8,.3,1.2)}
.chip.show{opacity:1;transform:none}
.chip.drop{background:#23253f;color:#5c5f86;text-decoration:line-through;
  opacity:.4!important;transform:translateY(8px) scale(.9)!important}
.chip.keep{background:#0e7c66;color:#fff;box-shadow:0 0 14px rgba(36,222,166,.45)}
.chip .why{font-size:9px;opacity:.85;margin-left:5px;text-decoration:none;
  display:inline-block;vertical-align:super}
.tok{display:flex;flex-direction:column;align-items:center;gap:6px;opacity:0;
  transform:scale(.7);transition:all .5s cubic-bezier(.2,.8,.3,1.25)}
.tok.show{opacity:1;transform:none}
.tok .lab{padding:4px 14px;border-radius:14px;background:#5b3df5;color:#fff;font-size:14px;
  font-weight:600;box-shadow:0 0 16px rgba(122,92,255,.5)}
.tok .lab small{font-weight:400;font-size:10px;opacity:.75;margin-left:4px}
.grid{display:grid;grid-template-columns:repeat(12,9px);gap:1px}
.cell{width:9px;height:9px;border-radius:2px;background:#1a1d3d;opacity:0;
  transform:scale(0);transition:all .25s}
.cell.on{opacity:1;transform:scale(1)}
#net{position:relative;height:362px;margin-top:4px}
#net svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.edge{stroke:#3a3f78;stroke-width:2;transition:all .5s}
.edge.flash{stroke:#7da4ff;stroke-width:3;stroke-dasharray:8 7;
  animation:dash .6s linear infinite}
.edge.winedge{stroke:#ffd54f;stroke-width:5;filter:drop-shadow(0 0 6px #ffd54f)}
.edge.dim{opacity:.2}
@keyframes dash{to{stroke-dashoffset:-15}}
#tme{position:absolute;left:50%;top:44px;transform:translate(-50%,-50%);
  width:92px;height:92px;border-radius:50%;
  background:radial-gradient(circle at 35% 30%,#3d4db7,#1d2566);
  border:3px solid #6b79e8;display:flex;flex-direction:column;align-items:center;
  justify-content:center;font-weight:700;color:#fff;z-index:3}
#tme small{font-size:8px;color:#aab3ff;font-weight:400}
#tme.pulse{animation:pulse .9s ease-out 2}
#tme.off{filter:grayscale(.85);opacity:.4;border-color:#3a3f78}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(120,140,255,.8)}
  100%{box-shadow:0 0 0 36px rgba(120,140,255,0)}}
.agent.entry{border-color:#7da4ff;box-shadow:0 0 18px rgba(125,164,255,.4)}
.agent.consult{animation:pulse .9s ease-out 2;border-color:#7da4ff}
.agent{position:absolute;width:172px;transform:translate(-50%,0);background:#181c44;
  border:2px solid #303670;border-radius:14px;padding:10px 12px;z-index:3;
  transition:all .5s}
.agent h4{font-size:15px;display:flex;align-items:center;gap:6px;color:#fff}
.agent .crown{margin-left:auto;opacity:0;transform:scale(0);
  transition:all .5s cubic-bezier(.3,1.6,.4,1)}
.agent .barwrap{height:9px;background:#0d0f29;border-radius:5px;margin-top:8px;
  overflow:hidden}
.agent .bar{height:100%;width:0%;border-radius:5px;
  transition:width 1.1s cubic-bezier(.2,.8,.3,1)}
.agent .score{font-family:monospace;font-size:12px;color:#aab3ff;margin-top:4px;
  text-align:right}
.agent.win{border-color:#ffd54f;box-shadow:0 0 26px rgba(255,213,79,.45);
  transform:translate(-50%,0) scale(1.07)}
.agent.win .crown{opacity:1;transform:scale(1.25)}
.agent.lose{opacity:.4;filter:saturate(.4)}
.agent.relearn{opacity:1;filter:none}
.mdir{display:flex;align-items:center;gap:6px;margin-top:8px;padding-top:7px;
  border-top:1px dashed #303670;font-size:10px;color:#8d93c8}
.mdir .mname{letter-spacing:1px}
.onehot{display:flex;gap:3px}
.onehot .bit{width:15px;height:15px;border-radius:3px;background:#0d0f29;
  border:1px solid #303670;display:flex;align-items:center;justify-content:center;
  font-size:9px;color:#5c5f86;transition:all .45s}
.onehot .bit.hot{color:#fff;border-color:#fff;transform:scale(1.15)}
.mcount{margin-left:auto;font-family:monospace;color:#5c5f86;transition:all .35s}
.mcount.pop{color:#ffd54f;transform:scale(1.4)}
.pair{position:absolute;z-index:6;padding:3px 10px;border-radius:10px;
  background:#241f54;border:1px solid #6b79e8;color:#cfd4ff;font-size:11px;
  font-family:monospace;transition:all .85s cubic-bezier(.45,.05,.4,1);
  transform:translate(-50%,-50%);white-space:nowrap;opacity:.95}
#tmebadge{position:absolute;left:50%;top:92px;transform:translateX(-50%);
  font-size:10px;font-family:monospace;color:#ffd54f;opacity:0;
  transition:opacity .4s;z-index:4;white-space:nowrap;text-align:center;
  background:#1a164055;padding:2px 8px;border-radius:8px}
.dot{position:absolute;width:14px;height:14px;border-radius:50%;background:#ffd54f;
  box-shadow:0 0 12px #ffd54f,0 0 26px rgba(255,213,79,.7);z-index:5;
  transition:all .85s cubic-bezier(.45,.05,.4,1);transform:translate(-50%,-50%)}
.dot.violet{background:#9d7bff;box-shadow:0 0 12px #9d7bff,0 0 26px rgba(157,123,255,.7)}
#bclabel{position:absolute;left:50%;top:112px;transform:translateX(-50%);font-size:11px;
  letter-spacing:2px;color:#7da4ff;opacity:0;transition:opacity .4s;z-index:4;
  white-space:nowrap}
#result{display:flex;align-items:center;gap:18px;justify-content:center;
  min-height:118px;opacity:0;transform:translateY(16px);transition:all .7s}
#result.show{opacity:1;transform:none}
#result img{width:104px;height:104px;border-radius:10px;border:3px solid #ffd54f;
  box-shadow:0 0 22px rgba(255,213,79,.4)}
#result .txt{font-size:15px;line-height:1.55;max-width:560px}
#result .txt b{color:#ffd54f}
#replay{position:absolute;top:12px;left:16px;background:#2b3060;
  border:1px solid #4a508f;color:#cfd4ff;border-radius:8px;padding:5px 14px;
  font-size:12px;cursor:pointer;z-index:9}
#replay:hover{background:#3a4080}
</style></head><body>
<div id="anim">
  <button id="replay" onclick="run()">&#8635; Replay</button>
  <div class="phase-label" id="plabel"></div>
  <div id="sentence"></div>
  <div id="words"></div>
  <div id="tokens"></div>
  <div id="net">
    <svg id="edges"></svg>
    <div id="tme">TME<small>broadcast</small></div>
    <div id="bclabel">BROADCAST v_q &rarr; ALL AGENTS</div>
    <div id="tmebadge"></div>
  </div>
  <div id="result"></div>
</div>
<script>
const D = __DATA__;
// Agentes desde los datos reales (antes hardcodeados a apple/horse/car:
// con 8 clases el JS reventaba si el ganador/entrada no estaba en la lista).
const AG = D.agents;
const $ = id => document.getElementById(id);
const sleep = ms => new Promise(r => setTimeout(r, ms));
// Layout dinamico: hasta 4 agentes por fila (8 agentes -> dos filas).
const PER_ROW = AG.length > 4 ? Math.ceil(AG.length/2) : AG.length;
const N_ROWS  = Math.ceil(AG.length / PER_ROW);
const ROW_H   = 158;
const POS = {};
AG.forEach((c,i)=>{
  const row = Math.floor(i/PER_ROW), col = i%PER_ROW;
  const inRow = Math.min(PER_ROW, AG.length - row*PER_ROW);
  POS[c] = {left:(100*(col+0.5)/inRow)+'%', row:row};
});
let running = false;

function centerOf(el, ref){
  const a = el.getBoundingClientRect(), b = ref.getBoundingClientRect();
  return [a.left + a.width/2 - b.left, a.top + a.height/2 - b.top];
}

function cellColor(v){
  const t = v / 15;
  const a = [36,30,86], b = [255,202,64];
  const c = a.map((x,i) => Math.round(x + (b[i]-x)*t));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}

function countUp(el, target, dur){
  const t0 = performance.now();
  function f(t){
    const p = Math.min(1, (t-t0)/dur);
    el.textContent = (target*p).toFixed(5);
    if (p < 1) requestAnimationFrame(f);
  }
  requestAnimationFrame(f);
}

function setup(){
  $('sentence').innerHTML=''; $('sentence').style.opacity=1;
  $('words').innerHTML='';   $('words').style.opacity=1;
  $('tokens').innerHTML='';  $('tokens').style.opacity=1;
  $('result').innerHTML='';  $('result').classList.remove('show');
  $('bclabel').style.opacity=0;
  $('tmebadge').style.opacity=0; $('tmebadge').textContent='';
  $('tme').classList.remove('pulse');
  document.querySelectorAll('.dot').forEach(d=>d.remove());
  const net=$('net');
  net.querySelectorAll('.agent').forEach(a=>a.remove());
  net.style.height=(362+(N_ROWS-1)*ROW_H)+'px';
  const H=net.clientHeight;
  const BIT=AG.length>4?11:15, BFS=AG.length>4?7:9;
  const MNAME=AG.length<=4?'<span class="mname">M_dir</span>':'';
  for(const cls of AG){
    const d=document.createElement('div'); d.className='agent'; d.id='ag-'+cls;
    d.style.left=POS[cls].left;
    d.style.top=(H-168-(N_ROWS-1-POS[cls].row)*ROW_H)+'px';
    d.innerHTML=`<h4>${D.emoji[cls]} ${cls}</h4>
      <div class="barwrap"><div class="bar" id="bar-${cls}"
           style="background:${D.colors[cls]}"></div></div>
      <div class="score" id="sc-${cls}">&mdash;</div>
      <div class="mdir">${MNAME}
        <div class="onehot" id="oh-${cls}">${
          AG.map(a=>`<div class="bit" data-a="${a}" style="width:${BIT}px;height:${BIT}px;font-size:${BFS}px">${a[0].toUpperCase()}</div>`).join('')
        }</div>
        <span class="mcount" id="mc-${cls}">+0</span></div>`;
    net.appendChild(d);
  }
  const svg=$('edges'); svg.innerHTML='';
  const tc=centerOf($('tme'),net);
  for(const cls of AG){
    const ac=centerOf($('ag-'+cls),net);
    const l=document.createElementNS('http://www.w3.org/2000/svg','line');
    l.setAttribute('x1',tc[0]); l.setAttribute('y1',tc[1]);
    l.setAttribute('x2',ac[0]); l.setAttribute('y2',ac[1]);
    l.setAttribute('class','edge'); l.id='edge-'+cls;
    svg.appendChild(l);
  }
  // Mature mode: TME disabled, entry agent highlighted, star edges dimmed
  if(D.mode==='mature'){
    $('tme').classList.add('off');
    $('tme').querySelector('small').textContent='disabled';
    document.querySelectorAll('.edge').forEach(e=>e.classList.add('dim'));
    $('ag-'+D.entry).classList.add('entry');
  } else {
    $('tme').classList.remove('off');
    $('tme').querySelector('small').textContent='broadcast';
  }
}

async function run(){
  if(running) return; running=true;
  setup();
  const lbl=$('plabel'), anim=$('anim');

  // ── P1: typewriter sentence ──
  lbl.textContent='1 / sentence';
  const s=$('sentence');
  const span=document.createElement('span'); s.appendChild(span);
  const caret=document.createElement('span'); caret.id='caret'; s.appendChild(caret);
  const txt='"'+D.query+'"';
  const spd=Math.max(14, Math.min(40, 1300/txt.length));
  for(const ch of txt){ span.textContent+=ch; await sleep(spd); }
  await sleep(350); caret.remove();

  // ── P2: decomposition ──
  lbl.textContent='2 / spaCy decomposition';
  const wr=$('words'); const chips=[];
  for(const w of D.words){
    const c=document.createElement('span'); c.className='chip'; c.textContent=w.text;
    wr.appendChild(c); chips.push(c);
  }
  for(const c of chips){ await sleep(65); c.classList.add('show'); }
  await sleep(500);
  D.words.forEach((w,i)=>{
    if(w.keep){ chips[i].classList.add('keep'); }
    else{
      chips[i].classList.add('drop');
      const y=document.createElement('span'); y.className='why';
      y.textContent=w.reason; chips[i].appendChild(y);
    }
  });
  s.style.opacity=.3;
  await sleep(900);

  // ── P3: labels → quantized vectors ──
  lbl.textContent='3 / fastText 300D → quantize [0,15]';
  const tr=$('tokens'); const toks=[];
  for(const t of D.tokens){
    const d=document.createElement('div'); d.className='tok';
    d.innerHTML=`<div class="lab">${t.lemma}<small>300D→v_q</small></div>`;
    const g=document.createElement('div'); g.className='grid';
    for(const v of t.vq){
      const cell=document.createElement('div'); cell.className='cell';
      cell.style.background=cellColor(v); g.appendChild(cell);
    }
    d.appendChild(g); tr.appendChild(d); toks.push(d);
  }
  wr.style.opacity=.3;
  for(const d of toks){ d.classList.add('show'); await sleep(150); }
  const cells=tr.querySelectorAll('.cell');
  for(let i=0;i<cells.length;i++){
    cells[i].classList.add('on');
    if(i%4===0) await sleep(7);
  }
  await sleep(700);

  // ── P4: cues travel to the hub (TME in early, entry agent in mature) ──
  const isMature = (D.mode === 'mature');
  const hubEl = isMature ? $('ag-'+D.entry) : $('tme');
  lbl.textContent = isMature
    ? '4 / cues → entry agent ('+D.entry+') — TME is OFF'
    : '4 / cues → TME';
  const tc=centerOf(hubEl,anim);
  for(const d of toks){
    const g=d.querySelector('.grid');
    const c0=centerOf(g,anim);
    const dot=document.createElement('div'); dot.className='dot violet';
    dot.style.left=c0[0]+'px'; dot.style.top=c0[1]+'px';
    anim.appendChild(dot);
    requestAnimationFrame(()=>requestAnimationFrame(()=>{
      dot.style.left=tc[0]+'px'; dot.style.top=tc[1]+'px';
    }));
  }
  tr.style.opacity=.3;
  await sleep(950);
  document.querySelectorAll('.dot').forEach(d=>d.remove());
  if(isMature){ hubEl.classList.add('consult'); }
  else { $('tme').classList.add('pulse'); }
  await sleep(600);

  // ── P5: broadcast (early)  /  M_dir consult (mature) ──
  if(isMature){
    lbl.textContent='5 / entry consults its M_dir (B1 ÷count)';
    const p=document.createElement('div'); p.className='pair';
    p.innerHTML='M_dir.predict_norm(v_q)';
    p.style.left=tc[0]+'px'; p.style.top=(tc[1]-64)+'px';
    anim.appendChild(p);
    // entry's M_dir strip lights all bits briefly — it holds scores for everyone
    $('oh-'+D.entry).querySelectorAll('.bit').forEach(b=>{
      b.style.background=D.colors[b.dataset.a];
      b.style.boxShadow='0 0 8px '+D.colors[b.dataset.a];
      b.classList.add('hot');
    });
    await sleep(1500);
    p.remove(); hubEl.classList.remove('consult');
  } else {
    lbl.textContent='5 / broadcast';
    $('bclabel').style.opacity=1;
    for(const cls of AG) $('edge-'+cls).classList.add('flash');
    for(const cls of AG){
      const dot=document.createElement('div'); dot.className='dot';
      dot.style.left=tc[0]+'px'; dot.style.top=tc[1]+'px';
      dot.style.background=D.colors[cls];
      dot.style.boxShadow='0 0 12px '+D.colors[cls];
      anim.appendChild(dot);
      const ac=centerOf($('ag-'+cls),anim);
      requestAnimationFrame(()=>requestAnimationFrame(()=>{
        dot.style.left=ac[0]+'px'; dot.style.top=ac[1]+'px';
      }));
    }
    await sleep(950);
    document.querySelectorAll('.dot').forEach(d=>d.remove());
    for(const cls of AG) $('edge-'+cls).classList.remove('flash');
    $('bclabel').style.opacity=0;
  }

  // ── P6: AMR scores ──
  lbl.textContent = isMature
    ? '6 / M_dir scores per agent (B1 normalized)'
    : '6 / M_dom_L weights → M_dom_H scores';
  const mx=Math.max(...AG.map(c=>D.avg[c]), 1e-9);
  for(const cls of AG){
    $('bar-'+cls).style.width=(100*D.avg[cls]/mx)+'%';
    countUp($('sc-'+cls), D.avg[cls], 900);
  }
  await sleep(1300);

  // ── P7: winner ──
  lbl.textContent = isMature ? '7 / argmax → destination agent' : '7 / argmax → winner';
  for(const cls of AG){
    if(cls===D.winner){
      $('ag-'+cls).classList.add('win');
      if(!isMature) $('edge-'+cls).classList.add('winedge');
    } else {
      if(!(isMature && cls===D.entry)) $('ag-'+cls).classList.add('lose');
      if(!isMature) $('edge-'+cls).classList.add('dim');
    }
  }
  await sleep(900);

  // ── Mature: point-to-point redirect entry → dest ──
  if(isMature && D.redirect){
    lbl.textContent='7b / REDIRECT  '+D.entry+' → '+D.winner+'  (point-to-point, no TME)';
    const net=$('net');
    const ec=centerOf($('ag-'+D.entry),net), dc=centerOf($('ag-'+D.winner),net);
    const l=document.createElementNS('http://www.w3.org/2000/svg','line');
    l.setAttribute('x1',ec[0]); l.setAttribute('y1',ec[1]);
    l.setAttribute('x2',dc[0]); l.setAttribute('y2',dc[1]);
    l.setAttribute('class','edge winedge');
    $('edges').appendChild(l);
    const ea=centerOf($('ag-'+D.entry),anim), da=centerOf($('ag-'+D.winner),anim);
    const rdot=document.createElement('div'); rdot.className='dot';
    rdot.style.left=ea[0]+'px'; rdot.style.top=ea[1]+'px';
    anim.appendChild(rdot);
    requestAnimationFrame(()=>requestAnimationFrame(()=>{
      rdot.style.left=da[0]+'px'; rdot.style.top=da[1]+'px';
    }));
    await sleep(950); rdot.remove();
  }

  // ── P8: M_dir learning (EARLY ONLY — mature phase does not learn) ──
  const onehot='['+AG.map(a=>a===D.winner?'1':'0').join(' ')+']';
  if(!isMature){
    // Faithful to stage6 process_query: tme.update_directory(v_q, winner_idx) and
    // every agent.update_directory(v_q, winner_idx) — the directory EHAMs fill up.
    lbl.textContent='8 / learning: register(v_q → '+D.winner+') in every M_dir';
    const tb=$('tmebadge');
    tb.innerHTML='M_dir_L.register(v_q, '+onehot+')';
    tb.style.opacity=1;
    // losers wake up to learn — everyone registers the association
    for(const cls of AG) $('ag-'+cls).classList.add('relearn');
    // association pairs fly TME → all 3 agents
    for(const cls of AG){
      const p=document.createElement('div'); p.className='pair';
      p.innerHTML='v_q&rarr;'+D.emoji[D.winner];
      p.style.left=tc[0]+'px'; p.style.top=tc[1]+'px';
      anim.appendChild(p);
      const ac=centerOf($('ag-'+cls),anim);
      requestAnimationFrame(()=>requestAnimationFrame(()=>{
        p.style.left=ac[0]+'px'; p.style.top=(ac[1]+26)+'px';
      }));
    }
    await sleep(950);
    document.querySelectorAll('.pair').forEach(p=>p.remove());
    // every agent's M_dir lights the winner bit + counter pops
    for(const cls of AG){
      $('oh-'+cls).querySelectorAll('.bit').forEach(b=>{
        if(b.dataset.a===D.winner){
          b.style.background=D.colors[D.winner];
          b.style.boxShadow='0 0 8px '+D.colors[D.winner];
          b.classList.add('hot');
        }
      });
      const mc=$('mc-'+cls);
      mc.textContent='+'+D.ntok;
      mc.classList.add('pop');
    }
    await sleep(1300);
    tb.style.opacity=0;
  }

  // ── P9: recall returns ──
  lbl.textContent = (isMature ? '8' : '9') + ' / recall → reconstruction';
  const wc=centerOf($('ag-'+D.winner),anim);
  const dot=document.createElement('div'); dot.className='dot';
  dot.style.left=wc[0]+'px'; dot.style.top=wc[1]+'px';
  anim.appendChild(dot);
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    dot.style.left=tc[0]+'px'; dot.style.top=tc[1]+'px';
  }));
  await sleep(950); dot.remove();

  // M_dir_R (visual directory) is trained ONLY from real image perceptions in
  // stage7. Recalled latents are echoes of the memory and are never registered
  // in M_dir_R, so the early phase shows no such registration here.

  const res=$('result');
  let inner='';
  if(D.img) inner+=`<img src="data:image/png;base64,${D.img}">`;
  if(isMature){
    inner+=`<div class="txt">Entry ${D.emoji[D.entry]} ${D.entry} `+
      (D.redirect
        ? `&rarr; redirected to <b>${D.emoji[D.winner]} ${D.winner.toUpperCase()}</b>`
        : `kept the query (<b>${D.emoji[D.winner]} ${D.winner.toUpperCase()}</b> = entry)`)+
      `&nbsp;&middot;&nbsp;M_dir B1 score ${D.avg[D.winner].toFixed(4)}`+
      `<br><span style="color:#8d93c8">`+
      (D.img
        ? 'point-to-point recall at destination &rarr; decoder &rarr; image'
        : 'destination M_dom_H did not recognize the cue (no recall)')+
      `</span></div>`;
  } else {
    inner+=`<div class="txt">Query routed to <b>${D.emoji[D.winner]} `+
      `${D.winner.toUpperCase()}</b>&nbsp;&middot;&nbsp;score `+
      `${D.avg[D.winner].toFixed(5)}<br><span style="color:#8d93c8">`+
      (D.img
        ? 'M_dom_H recall &rarr; 64D latent &rarr; decoder &rarr; reconstructed prototype'
        : 'cue not recognized by winner M_dom_H (no recall)')+
      `</span></div>`;
  }
  res.innerHTML=inner; res.classList.add('show');
  lbl.textContent='done — replay ↻';
  running=false;
}
window.addEventListener('load', ()=>setTimeout(run, 300));
</script></body></html>"""


def build_flow_animation(trace) -> str:
    """Serialize real trace data into the animated HTML component."""
    accepted_pos = {"NOUN", "ADJ", "PROPN"}
    representable = trace.get("tokens_representable", trace["tokens_known"])
    unrepresentable = trace.get("tokens_unrepresentable", trace["tokens_unknown"])
    words = []
    for t in trace["spacy_tokens"]:
        keep = t["lemma"] in representable
        if keep:
            reason = ""
        elif t["is_stop"]:
            reason = "stop"
        elif t["pos"] not in accepted_pos:
            reason = t["pos"]
        elif t["lemma"] in unrepresentable:
            reason = "no-repr"
        else:
            reason = "dup"
        words.append({"text": t["text"], "keep": keep, "reason": reason})

    tokens = []
    for tok in list(trace["per_token"].keys())[:6]:
        td = trace["per_token"][tok]
        tokens.append({
            "lemma": tok,
            "vq": [int(x) for x in td["q_vec"][::5]],   # 60-dim sample
        })

    data = {
        "mode":     "early",
        "entry":    None,
        "redirect": False,
        "agents": list(CLASSES),
        "query":  trace["query"],
        "words":  words,
        "tokens": tokens,
        "avg":    {cls: float(trace["avg_scores"][cls]) for cls in CLASSES},
        "winner": trace["winner"],
        "ntok":   int(trace["n_tokens"]),
        "colors": DOMAIN_COLOR,
        "emoji":  DOMAIN_EMOJI,
        "img":    (_img_b64(trace["final_recalled_img"])
                   if trace["final_recalled_img"] is not None else None),
    }
    return _ANIM_TEMPLATE.replace("__DATA__", json.dumps(data))


def _decompose_anim_data(query, nlp, vectors_cache):
    """Word/token serialization shared by the mature-phase animation."""
    accepted_pos = {"NOUN", "ADJ", "PROPN"}
    doc = nlp(query.lower())
    tokens  = tokenize_query(query, nlp)
    # Sin filtro léxico: "keep" = token representable por fastText (entra como
    # pista). token_in_vocabulary no decide nada aquí.
    representable = [
        t for t in tokens
        if get_fasttext_vector(t, vectors_cache, allow_fallback=False) is not None
    ]
    unrepresentable = [t for t in tokens if t not in representable]

    words = []
    for tok in doc:
        if not (tok.is_alpha and len(tok.text) > 1):
            continue
        keep = tok.lemma_ in representable
        if keep:
            reason = ""
        elif tok.is_stop:
            reason = "stop"
        elif tok.pos_ not in accepted_pos:
            reason = tok.pos_
        elif tok.lemma_ in unrepresentable:
            reason = "no-repr"
        else:
            reason = "dup"
        words.append({"text": tok.text, "keep": keep, "reason": reason})

    toks = []
    for t in representable[:6]:
        v   = np.asarray(get_fasttext_vector(t, vectors_cache,
                                             allow_fallback=False), dtype=np.float32)
        q_v = quantize_binary(v, M_LABEL)
        toks.append({"lemma": t, "vq": [int(x) for x in q_v[::5]]})

    return words, toks, representable


def build_mature_animation(query, words, toks, entry, dest,
                           scores, img_arr) -> str:
    """Animated mature-phase flow: TME off, entry agent consults M_dir,
    point-to-point redirect, recall at destination."""
    data = {
        "mode":     "mature",
        "entry":    entry,
        "redirect": entry != dest,
        "agents":   list(CLASSES),
        "query":    query,
        "words":    words,
        "tokens":   toks,
        "avg":      {cls: float(scores.get(cls, 0.0)) for cls in CLASSES},
        "winner":   dest,
        "ntok":     len(toks),
        "colors":   DOMAIN_COLOR,
        "emoji":    DOMAIN_EMOJI,
        "img":      _img_b64(img_arr) if img_arr is not None else None,
    }
    return _ANIM_TEMPLATE.replace("__DATA__", json.dumps(data))


# Animated visual-hemisphere flow (imagen → etiquetas), estilo fase madura:
# entrada por un agente cualquiera → directorio visual del TME (M_dir_R, B1) →
# redirige al especialista o rechaza. Componente autocontenido en su propio iframe;
# no reutiliza _ANIM_TEMPLATE ni los builders de la fase de texto.
_ANIM_IMG2LBL_TEMPLATE = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:transparent;font-family:'Segoe UI',system-ui,sans-serif}
#anim{position:relative;width:100%;max-width:1000px;margin:0 auto;
  background:linear-gradient(160deg,#0e1130 0%,#1b1f4b 55%,#101332 100%);
  border-radius:16px;padding:22px 24px 18px;color:#e8eaf6;overflow:hidden;
  box-shadow:0 8px 32px rgba(0,0,0,.35)}
.phase-label{position:absolute;top:16px;right:22px;font-size:11px;letter-spacing:2px;
  color:#8d93c8;text-transform:uppercase;text-align:right}
#replay{position:absolute;top:12px;left:16px;background:#2b3060;border:1px solid #4a508f;
  color:#cfd4ff;border-radius:8px;padding:5px 14px;font-size:12px;cursor:pointer;z-index:9}
#replay:hover{background:#3a4080}
#top{display:flex;align-items:center;justify-content:center;gap:14px;
  margin-top:30px;min-height:132px}
.stagebox{display:flex;flex-direction:column;align-items:center;gap:6px}
.cap{font-size:10px;letter-spacing:1px;color:#8d93c8;text-transform:uppercase}
#cue{opacity:0;transition:opacity .6s}
#cueimg{width:96px;height:96px;border-radius:10px;border:2px solid #6b79e8;
  box-shadow:0 0 16px rgba(107,121,232,.4);object-fit:cover}
.arrow{font-size:26px;color:#5c6190}
#eye{width:90px;height:90px;border-radius:50%;
  background:radial-gradient(circle at 35% 30%,#3d4db7,#1d2566);
  border:3px solid #6b79e8;display:flex;flex-direction:column;align-items:center;
  justify-content:center;color:#fff;font-weight:700}
#eye .ico{font-size:24px;line-height:1}
#eye small{font-size:8px;color:#aab3ff;font-weight:400;margin-top:2px}
#eye.pulse{animation:pulse .9s ease-out 2}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(120,140,255,.8)}
  100%{box-shadow:0 0 0 30px rgba(120,140,255,0)}}
#latentwrap{transition:opacity .5s}
.grid{display:grid;grid-template-columns:repeat(16,10px);gap:1px}
.cell{width:10px;height:10px;border-radius:2px;background:#1a1d3d;opacity:0;
  transform:scale(0);transition:all .25s}
.cell.on{opacity:1;transform:scale(1)}
#net{display:flex;flex-wrap:wrap;gap:14px;justify-content:center;margin-top:16px}
.agent{width:212px;background:#181c44;border:2px solid #303670;border-radius:14px;
  padding:11px 13px;transition:all .5s}
.agent h4{font-size:15px;display:flex;align-items:center;gap:6px;color:#fff}
.agent .sub{font-size:9px;color:#8d93c8;margin-top:2px;letter-spacing:.5px}
.agent .crown{margin-left:auto;opacity:0;transform:scale(0);
  transition:all .5s cubic-bezier(.3,1.6,.4,1)}
.agent .crown.show{opacity:1;transform:scale(1.25)}
.agent .barwrap{height:9px;background:#0d0f29;border-radius:5px;margin-top:9px;overflow:hidden}
.agent .bar{height:100%;width:0%;border-radius:5px;transition:width 1.1s cubic-bezier(.2,.8,.3,1)}
.agent .score{font-family:monospace;font-size:12px;color:#aab3ff;margin-top:4px;text-align:right}
.agent.win{border-color:#ffd54f;box-shadow:0 0 26px rgba(255,213,79,.45);transform:scale(1.05)}
.agent.lose{opacity:.4;filter:saturate(.4)}
.agent.reject{border-color:#ff6b6b;box-shadow:0 0 18px rgba(255,107,107,.35)}
.agent.entry{border-color:#7da4ff;box-shadow:0 0 18px rgba(125,164,255,.4)}
.agent .tag{font-size:8px;letter-spacing:1px;color:#7da4ff;opacity:0;transition:opacity .4s}
.agent .tag.show{opacity:1}
#hubwrap{display:flex;justify-content:center;margin-top:14px}
#hub{padding:10px 18px;border-radius:12px;text-align:center;
  background:radial-gradient(circle at 35% 30%,#3d4db7,#1d2566);
  border:2px solid #6b79e8;color:#fff;font-weight:700;font-size:14px;transition:all .5s}
#hub small{display:block;font-size:9px;color:#aab3ff;font-weight:400;margin-top:2px}
#hub.pulse{animation:pulse .9s ease-out 2}
#labels{display:flex;flex-wrap:wrap;gap:9px;align-items:center;justify-content:center;
  min-height:42px;margin-top:14px}
.lchip{padding:6px 15px;border-radius:16px;background:#0e7c66;color:#fff;font-size:15px;
  font-weight:600;box-shadow:0 0 14px rgba(36,222,166,.4);opacity:0;
  transform:translateY(-12px) scale(.8);transition:all .45s cubic-bezier(.2,.8,.3,1.2)}
.lchip.show{opacity:1;transform:none}
#result{display:flex;align-items:center;gap:16px;justify-content:center;min-height:118px;
  margin-top:8px;opacity:0;transform:translateY(16px);transition:all .7s}
#result.show{opacity:1;transform:none}
#result img{width:100px;height:100px;border-radius:10px;border:2px solid #6b79e8;object-fit:cover}
#result img.recon{border-color:#ffd54f;box-shadow:0 0 22px rgba(255,213,79,.4)}
#result .arrowbig{font-size:30px;color:#ffd54f}
#result .txt{font-size:14px;line-height:1.6;max-width:520px}
#result .txt b{color:#ffd54f}
#result .txt code{background:#0e7c66;color:#fff;padding:1px 7px;border-radius:8px;font-size:13px}
#result .muted{color:#8d93c8;font-size:12px}
.dot{position:absolute;width:14px;height:14px;border-radius:50%;background:#ffd54f;
  box-shadow:0 0 12px #ffd54f;z-index:5;transition:all .8s cubic-bezier(.45,.05,.4,1);
  transform:translate(-50%,-50%)}
</style></head><body>
<div id="anim">
  <button id="replay" onclick="run()">&#8635; Replay</button>
  <div class="phase-label" id="plabel"></div>
  <div id="top">
    <div class="stagebox" id="cue"><div class="cap">imagen (pista)</div><img id="cueimg"></div>
    <div class="arrow">&rarr;</div>
    <div id="eye"><div class="ico">&#128065;</div><small>ResNet18</small></div>
    <div class="arrow">&rarr;</div>
    <div class="stagebox" id="latentwrap"><div class="cap">z_q &#8712; [0,31]&#8310;&#8308;</div>
      <div class="grid" id="latentgrid"></div></div>
  </div>
  <div id="hubwrap"><div id="hub">M_dir_R<small>directorio visual del agente &middot; B1</small></div></div>
  <div id="net"></div>
  <div id="labels"></div>
  <div id="result"></div>
</div>
<script>
const D=__DATA__;
// Agentes desde los datos reales (antes hardcodeados a apple/horse/car).
const AG=D.agents;
const $=id=>document.getElementById(id);
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let running=false;
function centerOf(el,ref){const a=el.getBoundingClientRect(),b=ref.getBoundingClientRect();
  return [a.left+a.width/2-b.left,a.top+a.height/2-b.top];}
function cellColor(v){const t=v/31,a=[26,29,61],b=[124,164,255];
  const c=a.map((x,i)=>Math.round(x+(b[i]-x)*t));return `rgb(${c[0]},${c[1]},${c[2]})`;}
function countUp(el,target,dur){const t0=performance.now();
  function f(t){const p=Math.min(1,(t-t0)/dur);el.textContent=(target*p).toFixed(0);
  if(p<1)requestAnimationFrame(f);}requestAnimationFrame(f);}
function mkdot(c,color){const d=document.createElement('div');d.className='dot';
  d.style.left=c[0]+'px';d.style.top=c[1]+'px';d.style.background=color;
  d.style.boxShadow='0 0 12px '+color;return d;}
function move(d,c){requestAnimationFrame(()=>requestAnimationFrame(()=>{
  d.style.left=c[0]+'px';d.style.top=c[1]+'px';}));}

function setup(){
  const net=$('net');net.innerHTML='';
  for(const cls of AG){
    const d=document.createElement('div');d.className='agent';d.id='ag-'+cls;
    d.innerHTML=`<h4>${D.emoji[cls]} ${cls}<span class="crown" id="cr-${cls}">&#128081;</span></h4>
      <div class="sub">especialista &middot; score B1 del directorio</div>
      <div class="tag" id="tag-${cls}">ENTRADA</div>
      <div class="barwrap"><div class="bar" id="bar-${cls}" style="background:${D.colors[cls]}"></div></div>
      <div class="score" id="sc-${cls}">&mdash;</div>`;
    net.appendChild(d);
  }
  const g=$('latentgrid');g.innerHTML='';
  for(let i=0;i<D.latent.length;i++){const c=document.createElement('div');c.className='cell';g.appendChild(c);}
  $('cueimg').src='data:image/png;base64,'+D.queryImg;
  $('labels').innerHTML='';$('result').innerHTML='';$('result').classList.remove('show');
  $('cue').style.opacity=0;$('eye').classList.remove('pulse');$('latentwrap').style.opacity=.25;
  $('hub').classList.remove('pulse');
  document.querySelectorAll('.dot').forEach(x=>x.remove());
}

function showResult(rejected){
  const res=$('result');let inner='';
  inner+=`<img src="data:image/png;base64,${D.queryImg}" title="entrada">`;
  if(rejected){
    inner+=`<div class="txt"><b style="color:#ff6b6b">RECHAZADA</b><br>`+
      `<span class="muted">el directorio visual M_dir_R no tiene soporte &middot; `+
      `ning&uacute;n especialista lo conoce &middot; el grupo no inventa referente</span></div>`;
  }else{
    inner+=`<div class="arrowbig">&rarr;</div>`;
    if(D.reconImg)inner+=`<img class="recon" src="data:image/png;base64,${D.reconImg}" title="reconstruccion">`;
    const route=D.redirect
      ? `${D.emoji[D.entry]} ${D.entry} &rarr; redirige a <b>${D.emoji[D.winner]} ${D.winner.toUpperCase()}</b>`
      : `<b>${D.emoji[D.winner]} ${D.winner.toUpperCase()}</b> (entrada = especialista)`;
    inner+=`<div class="txt">${route}`+
      `<br>etiquetas: ${D.labels.map(w=>'<code>'+w+'</code>').join(' ')}`+
      `<br><span class="muted">la reconstrucci&oacute;n la evoca la MAE (no es la entrada)</span></div>`;
  }
  res.innerHTML=inner;res.classList.add('show');
}

async function run(){
  if(running)return;running=true;setup();
  const lbl=$('plabel'),anim=$('anim');

  lbl.textContent='1 / percepción (imagen de entrada)';
  $('cue').style.opacity=1;await sleep(750);

  lbl.textContent='2 / ResNet18 (ojo) → z ∈ ℝ⁶⁴';
  {const dot=mkdot(centerOf($('cueimg'),anim),'#7da4ff');anim.appendChild(dot);
   move(dot,centerOf($('eye'),anim));await sleep(800);dot.remove();}
  $('eye').classList.add('pulse');await sleep(500);

  lbl.textContent='3 / cuantización z → z_q ∈ [0,31]⁶⁴';
  {const dot=mkdot(centerOf($('eye'),anim),'#9d7bff');anim.appendChild(dot);
   move(dot,centerOf($('latentgrid'),anim));await sleep(750);dot.remove();}
  $('latentwrap').style.opacity=1;
  const cells=$('latentgrid').querySelectorAll('.cell');
  for(let i=0;i<cells.length;i++){cells[i].style.background=cellColor(D.latent[i]);
    cells[i].classList.add('on');if(i%4===0)await sleep(6);}
  await sleep(500);

  // P4: z_q llega a un agente de entrada cualquiera
  lbl.textContent='4 / z_q llega al agente de entrada ('+D.entry+')';
  $('ag-'+D.entry).classList.add('entry');$('tag-'+D.entry).classList.add('show');
  {const dot=mkdot(centerOf($('latentgrid'),anim),D.colors[D.entry]);anim.appendChild(dot);
   move(dot,centerOf($('ag-'+D.entry),anim));await sleep(850);dot.remove();}

  // P5: la entrada consulta el directorio visual del TME (M_dir_R)
  lbl.textContent='5 / '+D.entry+' consulta SU directorio visual M_dir_R';
  {const dot=mkdot(centerOf($('ag-'+D.entry),anim),'#7da4ff');anim.appendChild(dot);
   move(dot,centerOf($('hub'),anim));await sleep(800);dot.remove();}
  $('hub').classList.add('pulse');await sleep(500);

  // P6: el directorio reparte el score B1 a cada especialista
  lbl.textContent='6 / M_dir_R reparte score B1 por especialista';
  const hc=centerOf($('hub'),anim);
  for(const cls of AG){const dot=mkdot(hc,D.colors[cls]);anim.appendChild(dot);
    move(dot,centerOf($('ag-'+cls),anim));}
  await sleep(850);document.querySelectorAll('.dot').forEach(x=>x.remove());
  const mx=Math.max(...AG.map(c=>D.scores[c]),1e-9);
  for(const cls of AG){$('bar-'+cls).style.width=(100*D.scores[cls]/mx)+'%';
    countUp($('sc-'+cls),D.scores[cls],900);}
  await sleep(1250);

  // P7: rechazo, o redirección punto a punto al especialista
  if(D.winner===null){
    lbl.textContent='7 / RECHAZADA — M_dir_R sin soporte: nadie lo conoce';
    for(const cls of AG)$('ag-'+cls).classList.add('reject');
    await sleep(400);showResult(true);
    lbl.textContent='done — replay ↻';running=false;return;
  }
  for(const cls of AG){
    if(cls===D.winner){$('ag-'+cls).classList.add('win');$('cr-'+cls).classList.add('show');}
    else if(cls!==D.entry)$('ag-'+cls).classList.add('lose');
  }
  if(D.redirect){
    lbl.textContent='7 / redirige '+D.entry+' → '+D.winner+' (punto a punto)';
    const dot=mkdot(centerOf($('ag-'+D.entry),anim),'#ffd54f');anim.appendChild(dot);
    move(dot,centerOf($('ag-'+D.winner),anim));await sleep(950);dot.remove();
  }else{
    lbl.textContent='7 / '+D.entry+' se queda la consulta (entrada = especialista)';
    await sleep(700);
  }

  lbl.textContent='8 / evoke_labels en el destino (recall inverso → top-3 coseno)';
  const lw=$('labels');
  for(const w of D.labels){
    const chip=document.createElement('span');chip.className='lchip';chip.textContent=w;
    lw.appendChild(chip);await sleep(130);chip.classList.add('show');
  }
  await sleep(700);

  if(D.reconImg){lbl.textContent='9 / mem_dom_R.recall → decode → reconstrucción';await sleep(250);}
  showResult(false);
  lbl.textContent='done — replay ↻';running=false;
}
window.addEventListener('load',()=>setTimeout(run,250));
</script></body></html>"""


def build_image_to_labels_animation(pil, z_q, scores, entry, winner, agents,
                                    all_vecs, decoder, gmin_v, gmax_v) -> str:
    """Serializa el flujo imagen → etiquetas estilo fase madura: la imagen entra
    por `entry` y se rutea con el directorio visual del TME (M_dir_R, B1) hacia el
    especialista `winner` (None = rechazo), que evoca etiquetas y reconstruye.
    La decisión de ruteo la toma el tab (vía la memoria) y se recibe aquí; este
    builder NO re-decide. Solo visualiza; no altera nada."""
    import io as _io
    import contextlib as _ctx
    from stage7_bidirectional import evoke_labels

    scores = {c: float(scores[c]) for c in CLASSES}

    labels, recon_b64 = [], None
    if winner is not None:
        labels = list(evoke_labels(agents[winner], z_q, all_vecs))
        with _ctx.redirect_stdout(_io.StringIO()):
            r_io, recognized, _w = agents[winner].mem_dom_R.recall(z_q)
        if recognized:
            recon_b64 = _img_b64(_decode(r_io, gmin_v, gmax_v, decoder))

    q_np = np.asarray(pil.convert("RGB").resize((128, 128)), dtype=np.float32) / 255.0
    data = {
        "queryImg": _img_b64(q_np),
        "reconImg": recon_b64,
        "agents":   list(CLASSES),
        "latent":   [int(x) for x in np.asarray(z_q).ravel().tolist()],
        "scores":   scores,
        "winner":   winner,
        "entry":    entry,
        "redirect": (winner is not None and winner != entry),
        "labels":   labels,
        "colors":   DOMAIN_COLOR,
        "emoji":    DOMAIN_EMOJI,
    }
    return _ANIM_IMG2LBL_TEMPLATE.replace("__DATA__", json.dumps(data))


# Alturas de los iframes de animación: con más de 4 agentes el grid de
# especialistas ocupa una fila extra.
_ANIM_H     = 890 + (158 if len(CLASSES) > 4 else 0)
_ANIM_IMG_H = 760 + (140 if len(CLASSES) > 4 else 0)


def _video_export_ui(key: str, sig: str, builder=None, html: str = None,
                     height: int = None):
    """Exportación a MP4 de una animación de ruteo.

    Vía principal: grabación EXACTA de la animación HTML (el mismo markup
    que muestra la app) en un Edge headless vía screencast CDP — pixel por
    pixel lo que se ve en Streamlit (app_video_dom). Si el navegador o
    playwright no están disponibles, cae al renderer PIL (app_video) con
    los mismos datos. En ambos casos el video consume decisiones YA tomadas
    por la MAE: visualiza, no re-decide. `sig` invalida el cache al cambiar
    la consulta/imagen."""
    if st.session_state.get(f"vidsig_{key}") != sig:
        st.session_state.pop(f"vid_{key}", None)
    with st.expander("🎬 Exportar la animación a video (MP4 descargable)"):
        st.caption(
            "Graba la animación real en un navegador headless (idéntica a la "
            "de arriba). Con los datos reales de esta corrida: scores, "
            "ganador, redirección e imágenes evocadas."
        )
        if st.button("Generar video", key=f"btn_{key}"):
            data = None
            if html:
                with st.spinner("Grabando la animación en el navegador "
                                "headless (~30–60 s, corre completa)…"):
                    try:
                        from app_video_dom import record_animation_html
                        data = record_animation_html(
                            html, height or _ANIM_H)
                    except Exception as e:
                        st.warning(
                            f"Captura del navegador no disponible "
                            f"({type(e).__name__}); usando el renderer PIL.")
            if data is None and builder is not None:
                with st.spinner("Renderizando MP4 (PIL, ~5–10 s)…"):
                    data = builder()
            if data:
                st.session_state[f"vid_{key}"] = data
                st.session_state[f"vidsig_{key}"] = sig
        data = st.session_state.get(f"vid_{key}")
        if data:
            st.video(data)
            st.download_button(
                "⬇ Descargar MP4", data, file_name=f"{key}.mp4",
                mime="video/mp4", key=f"dl_{key}",
                use_container_width=True)


# Session state management

def _init_session():
    if "mdir_mem" not in st.session_state:
        st.session_state.mdir_mem    = DirectoryMemory(N, M_LABEL, len(CLASSES))
    if "mdir_counts" not in st.session_state:
        st.session_state.mdir_counts = np.zeros(len(CLASSES), dtype=np.int64)
    if "history" not in st.session_state:
        st.session_state.history     = []
    if "query_n" not in st.session_state:
        st.session_state.query_n     = 0
    if "last_trace" not in st.session_state:
        st.session_state.last_trace  = None


def _reset_session():
    st.session_state.mdir_mem    = DirectoryMemory(N, M_LABEL, len(CLASSES))
    st.session_state.mdir_counts = np.zeros(len(CLASSES), dtype=np.int64)
    st.session_state.history     = []
    st.session_state.query_n     = 0
    st.session_state.last_trace  = None


# Pipeline Trace UI renderer

def _stage_header(num, icon, title, subtitle=""):
    sub = (f"<div style='color:#aaa;font-size:12px;margin-top:2px'>{subtitle}</div>"
           if subtitle else "")
    st.markdown(
        f"""<div style='
            background:linear-gradient(90deg,#1a1a2e 0%,#16213e 100%);
            border-left:4px solid #e94560;
            border-radius:6px; padding:10px 18px; margin:18px 0 10px 0'>
          <span style='color:#e94560;font-size:11px;font-weight:700;
                       letter-spacing:2px;text-transform:uppercase'>
            STAGE {num}</span>
          <div style='color:white;font-size:17px;font-weight:700;margin-top:3px'>
            {(icon + " ") if icon else ""}{title}</div>
          {sub}
        </div>""",
        unsafe_allow_html=True,
    )


def render_pipeline_trace(trace, ref_imgs, g_min, g_max):
    """Full 6-stage pipeline visualisation."""

    # ANIMATED FLOW — cinematic overview of the whole pipeline
    st.markdown("### Animated Pipeline Flow")
    st.caption(
        "Watch the query decompose into words, transform into quantized cues, "
        "broadcast through the TME, and return as a reconstructed memory — "
        "all values are the real ones computed by the AMRs."
    )
    _anim_html = build_flow_animation(trace)
    components.html(_anim_html, height=_ANIM_H, scrolling=False)

    _ref_np = ref_imgs[trace["winner"]].permute(1, 2, 0).numpy() \
        if trace.get("winner") else None
    from app_video import render_early_video
    _video_export_ui(
        "ruteo_temprano", trace["query"],
        html=_anim_html, height=_ANIM_H,
        builder=lambda: render_early_video(trace, list(CLASSES), DOMAIN_COLOR,
                                           ref_img=_ref_np))

    st.markdown("---")
    st.markdown("### Detailed Stage-by-Stage Breakdown")

    # STAGE 1 — Sentence Decomposition
    _stage_header(1, "", "Sentence Decomposition",
        "spaCy en_core_web_sm: tokenise → lemmatise → filter stopwords + keep NOUN/ADJ/PROPN")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("**Input query**")
        st.markdown(
            f"<div style='background:#f0f2f6;padding:10px;border-radius:6px;"
            f"font-size:17px;font-style:italic'>\"{trace['query']}\"</div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown("**spaCy token analysis**")
        badges = ""
        _repr = trace.get("tokens_representable", trace["tokens_known"])
        _unrepr = trace.get("tokens_unrepresentable", trace["tokens_unknown"])
        for t in trace["spacy_tokens"]:
            used = t["lemma"] in _repr
            oov  = t["lemma"] in _unrepr
            if used:
                bg = "#27ae60"
            elif oov:
                bg = "#e67e22"
            else:
                bg = "#95a5a6"
            stop_mark = "✗" if t["is_stop"] else ""
            badges += (
                f"<span style='background:{bg};color:white;padding:4px 10px;"
                f"border-radius:14px;margin:3px;display:inline-block;font-size:13px'>"
                f"{t['text']}"
                f"<span style='font-size:9px;opacity:.8'> [{t['pos']}]{stop_mark}</span>"
                f"</span>"
            )
        st.markdown(f"<div style='line-height:2.4'>{badges}</div>",
                    unsafe_allow_html=True)

        repr_str = " · ".join(f"`{t}`" for t in trace["per_token"].keys())
        invocab_str = (" · ".join(f"`{t}`" for t in trace["tokens_known"])
                       if trace["tokens_known"] else "—")
        st.caption(
            f"Tokens representables (entran como pista): {repr_str}   ·   "
            f"en vocab de labels (diagnóstico): {invocab_str}")

    # STAGE 2 — FastText Serialization
    _stage_header(2, "", "FastText Serialization",
        f"token → 300D float  →  v/S recortado a [−1,1] (escala global S)  →  "
        f"quantize_binary(v, M={M_LABEL}) por magnitud  →  v_q ∈ [0,{M_LABEL-1}]^{N}")

    tokens_list = list(trace["per_token"].keys())
    sel_tok = (st.selectbox("Inspect token:", tokens_list, key="s2_tok")
               if len(tokens_list) > 1 else tokens_list[0])
    if len(tokens_list) == 1:
        st.caption(f"Token: **{sel_tok}**")

    td = trace["per_token"][sel_tok]

    c_ft, c_sign, c_q = st.columns(3)
    with c_ft:
        st.markdown("**① fastText → 300D float**")
        fig = _vec_heatmap(
            td["raw_vec"],
            title=f"min={td['raw_vec'].min():.2f}  max={td['raw_vec'].max():.2f}",
            rows=15, colorscale="RdBu_r",
        )
        st.plotly_chart(fig, use_container_width=True, key=f"s2_ft_{sel_tok}")
        st.caption(f"μ={td['raw_vec'].mean():.3f}   σ={td['raw_vec'].std():.3f}")

    with c_sign:
        st.markdown("**② v/S → [−1, 1]  (magnitud)**")
        _clipped = int((np.abs(td["scaled_vec"]) >= 1.0).sum())
        fig = _vec_heatmap(
            td["scaled_vec"],
            title=(f"S={label_scale():.4f}   "
                   f"recortadas: {_clipped}/300"),
            rows=15, colorscale="RdBu_r",
        )
        st.plotly_chart(fig, use_container_width=True, key=f"s2_scaled_{sel_tok}")
        st.caption("Escala global S (p99 de |componente|) — la magnitud se preserva")

    with c_q:
        st.markdown(f"**③ v_q ∈ [0,{M_LABEL-1}]  (input to AMRs)**")
        fig = _vec_heatmap(
            td["q_vec"].astype(float),
            title=f"range [0,{M_LABEL-1}]  •  15×20 grid",
            rows=15, colorscale="Viridis",
        )
        st.plotly_chart(fig, use_container_width=True, key=f"s2_q_{sel_tok}")
        st.caption("This v_q is broadcast to every agent's M_dom_H")

    # STAGE 3 — TME Broadcast
    _stage_header(3, "", "TME Broadcast",
        "v_q sent simultaneously to all agents — each processes independently, no inter-agent communication")

    _agents_html = " &nbsp;|&nbsp; ".join(
        f"<span style='color:{DOMAIN_COLOR[c]}'>{DOMAIN_EMOJI[c]} {c}</span>"
        for c in CLASSES)
    st.markdown(
        f"""<div style='text-align:center;padding:14px;background:#f8f9fa;
            border-radius:8px;margin:8px 0;border:1px solid #ddd'>
          <span style='font-size:15px;color:#2c3e50'>
            <b>TME</b> broadcasts
            <code style='background:#eee;padding:2px 6px;border-radius:4px'>
              v_q[{sel_tok}] ∈ [0,{M_LABEL-1}]^{N}</code>
            &nbsp;→&nbsp; M_dom_H de: {_agents_html}
          </span>
        </div>""",
        unsafe_allow_html=True,
    )
    st.caption(
        "Each agent has 4 AMRs. Only M_dom_L and M_dom_H participate in routing. "
        "M_dom_R (latent homo-AM) and M_dir (routing hetero-AM) are updated separately."
    )

    # STAGE 4 — Per-Agent AMR Processing
    _stage_header(4, "", "Per-Agent AMR Processing",
        "M_dom_L.recog_weights(v_q) → per-feature weights  →  M_dom_H.recognize_from_left(v_q, w) → score")

    # Filas de 4 columnas para cubrir TODAS las clases (st.columns(3) + zip
    # truncaba la vista a 3 de los 8 agentes; el ganador podía ni aparecer).
    _PER_ROW = 4
    agent_cells = []
    for _start in range(0, len(CLASSES), _PER_ROW):
        _chunk = CLASSES[_start:_start + _PER_ROW]
        agent_cells.extend(zip(st.columns(_PER_ROW), _chunk))
    for col, cls in agent_cells:
        pa     = td["per_agent"][cls]
        is_win = (cls == trace["winner"])
        color  = DOMAIN_COLOR[cls]
        border = f"3px solid {color}" if is_win else f"1px solid {color}55"
        bg     = f"{color}11"         if is_win else "#fafafa"
        crown  = ""

        with col:
            st.markdown(
                f"""<div style='background:{bg};border:{border};border-radius:10px;
                    padding:12px 14px;margin-bottom:10px'>
                  <div style='font-size:18px;font-weight:700;color:{color}'>
                    {DOMAIN_EMOJI[cls]} {cls.upper()}{crown}</div>
                  <div style='font-size:11px;color:#666;margin-top:2px'>
                    4 AMRs: M_dom_L · M_dom_R · M_dom_H · M_dir</div>
                </div>""",
                unsafe_allow_html=True,
            )

            # AMR 1: M_dom_L
            with st.expander(
                    f"AMR 1 · M_dom_L  (homo label)   "
                    f"mean_w={pa['l_mean']:.4f}   "
                    f"nonzero={pa['l_nonzero']}/{N}"):
                fig = _vec_heatmap(
                    pa["l_weights"],
                    title=f"recog_weights(v_q)  •  AssocMem({N},{M_LABEL})",
                    rows=15, colorscale="YlOrRd", height=145,
                )
                st.plotly_chart(fig, use_container_width=True,
                                key=f"s4_lw_{cls}_{sel_tok}")
                st.caption(
                    "AssociativeMemory(n=300, m=16) — homo-associative label domain. "
                    "Per-feature weights fed into M_dom_H as left_weights (Pineda architecture)."
                )

            # AMR 2: M_dom_H
            with st.expander(
                    f"AMR 2 · M_dom_H  (hetero label↔latent)   "
                    f"score={pa['h_score']:.5f}"):
                norm_tag = " (gateado)" if trace.get("normalized") else " (raw)"
                st.metric(f"Recognition score{norm_tag}", f"{pa['h_score']:.5f}")
                if trace.get("normalized"):
                    st.caption(
                        "gate de containment: "
                        + ("contenido" if pa['h_score'] > 0 else "rechazado")
                    )
                st.caption(
                    f"HAM4D(n={N}, m={M_LABEL}, p={P_LATENT}, q={Q_LATENT}) · "
                    "project(v_q, l_weights, dim=0) → AND containment"
                )
                if is_win:
                    # Full recall computed only for winner (pass 2)
                    if pa["recognized"] is not None:
                        st.metric("Recall", "recognized" if pa["recognized"]
                                  else "not recognized")
                        if pa["recognized"]:
                            st.metric("Recall weight", f"{pa['recall_weight']:.5f}")
                        if pa["recalled_img"] is not None:
                            st.image(_t2img(pa["recalled_img"]),
                                     width=100, caption=f"Recalled {cls}")
                else:
                    st.caption(
                        "Recall skipped for non-winner agents "
                        "(recall_with_sampling_n_search only runs on the winner "
                        "to keep response time fast)."
                    )

            # AMRs 3+4 (info only)
            with st.expander("AMR 3 · M_dom_R  (homo latent) + AMR 4 · M_dir  (routing)"):
                st.caption(
                    f"**M_dom_R** AssocMem({P_LATENT},{Q_LATENT}) — latent domain homo-AM. "
                    f"Provides per-feature weights for inverse recall (label reconstruction). "
                    f"Not involved in early-phase routing.\n\n"
                    f"**M_dir** HAMDir({N},{M_LABEL}→{len(CLASSES)},2) — hetero routing AM. "
                    f"Learns label→agent associations during early phase. "
                    f"Used in mature phase for point-to-point routing."
                )

            # Score bar
            max_s = max(trace["per_token"][t]["per_agent"][cls]["h_score"]
                        for t in trace["per_token"])
            max_all = max(
                trace["per_token"][t]["per_agent"][c]["h_score"]
                for t in trace["per_token"] for c in CLASSES
            )
            pct = pa["h_score"] / max(max_all, 1e-9)
            st.markdown(f"**Score: `{pa['h_score']:.5f}`**")
            st.progress(float(np.clip(pct, 0, 1)))

    # Multi-token breakdown
    if len(trace["per_token"]) > 1:
        with st.expander(
                f"Aggregate — scores across all {trace['n_tokens']} tokens"):
            fig = go.Figure()
            toks = list(trace["per_token"].keys())
            for cls in CLASSES:
                scores = [trace["per_token"][t]["per_agent"][cls]["h_score"]
                          for t in toks]
                fig.add_trace(go.Bar(
                    name=f"{DOMAIN_EMOJI[cls]} {cls}", x=toks, y=scores,
                    marker_color=DOMAIN_COLOR[cls],
                ))
            fig.update_layout(
                barmode="group",
                title=dict(text="M_dom_H score per token × agent", x=0.5,
                           font=dict(size=12)),
                height=240, margin=dict(l=20, r=20, t=50, b=20),
                plot_bgcolor="white", paper_bgcolor="#f8f9fa",
                legend=dict(orientation="h", y=1.1),
            )
            st.plotly_chart(fig, use_container_width=True, key="s4_multitok")

    # STAGE 5 — TME Decision + M_dir Update
    _stage_header(5, "", "TME Decision + M_dir Update",
        "winner = argmax(avg_scores)  →  register all tokens in M_dir[winner]")

    winner = trace["winner"]
    wcolor = DOMAIN_COLOR[winner]

    c_dec, c_mdir = st.columns([1, 1])
    with c_dec:
        mode_tag = ("official scoring (containment gate)"
                    if trace.get("normalized") else "raw scores (no gate)")
        st.markdown(f"**Aggregated scores (avg over tokens)** — {mode_tag}:")
        max_s = max(trace["avg_scores"].values())
        for cls in CLASSES:
            s   = trace["avg_scores"][cls]
            pct = s / max(max_s, 1e-9)
            bld = "**" if cls == winner else ""
            st.markdown(f"{DOMAIN_EMOJI[cls]} {bld}{cls}{bld}")
            st.progress(float(np.clip(pct, 0, 1)),
                        text=f"{'> ' if cls == winner else ''}{s:.5f}")

        st.markdown(
            f"""<div style='background:{wcolor}22;border-left:5px solid {wcolor};
                padding:12px;border-radius:6px;margin-top:14px'>
              <b>Winner → {DOMAIN_EMOJI[winner]} {winner.upper()}</b><br>
              <span style='font-size:12px;color:#555'>
                TME routes query to {winner} agent •
                registers {trace['n_tokens']} token(s) in M_dir
              </span>
            </div>""",
            unsafe_allow_html=True,
        )

    with c_mdir:
        st.markdown("**M_dir state after this query:**")
        counts = st.session_state.mdir_mem.agent_counts
        st.plotly_chart(_mdir_bar(counts, st.session_state.query_n),
                        use_container_width=True, key="s5_mdir")
        total = counts.sum()
        if total > 0:
            h = st.session_state.mdir_mem.entropy()
            st.caption(
                f"Entropy: {h:.3f} bits (max={np.log2(len(CLASSES)):.3f})  •  "
                f"Counts: {dict(zip(CLASSES, counts.tolist()))}"
            )

    # STAGE 6 — Recall & Image Reconstruction
    _stage_header(6, "", "Recall & Image Reconstruction",
        f"Winner ({winner}): M_dom_H.recall_from_left(v_q) → recalled_q (64D) → dequantize → decoder → image")

    if trace["final_recalled_img"] is not None:
        best_tok  = trace["final_recalled_tok"]
        pa_win    = trace["per_token"][best_tok]["per_agent"][winner]
        r_q       = pa_win["recalled_q"]
        r_weight  = pa_win["recall_weight"]

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown("**① recalled_q  (64D)**")
            st.caption(f"from `{best_tok}` via M_dom_H")
            fig = _vec_heatmap(
                r_q.astype(float),
                title=f"[0,{Q_LATENT-1}]  •  8×8 grid",
                rows=8, colorscale="Plasma", height=150,
            )
            st.plotly_chart(fig, use_container_width=True, key="s6_rq")
            st.caption(f"recall_weight = {r_weight:.5f}")

        with c2:
            st.markdown("**② dequantize → latent**")
            st.caption("v_norm × (g_max − g_min) + g_min")
            v_lat = _dequantize(r_q, g_min, g_max)
            fig = _vec_heatmap(
                v_lat,
                title=f"64D latent   μ={v_lat.mean():.3f}",
                rows=8, colorscale="RdBu_r", height=150,
            )
            st.plotly_chart(fig, use_container_width=True, key="s6_lat")
            st.caption("ResNet18 encoded space (continuous float)")

        with c3:
            st.markdown("**③ decoder → image**")
            st.caption("ConvTranspose2d · 64→128×128 RGB")
            st.image(_t2img(trace["final_recalled_img"]),
                     caption=f"Reconstructed {winner}", width=120)

        with c4:
            st.markdown("**④ ETH-80 reference**")
            st.caption("Ground truth for comparison")
            ref_np = ref_imgs[winner].permute(1, 2, 0).numpy()
            st.image(_t2img(ref_np), caption=f"ETH-80 {winner}", width=120)

        st.success(
            f"Pipeline complete:  \"{trace['query']}\"  →  **{winner.upper()}**  "
            f"via token `{best_tok}`  (recall_weight={r_weight:.4f})"
        )

    else:
        st.warning(
            f"Winner agent **{winner}** did not recognize any token in M_dom_H "
            f"({trace['n_tokens']} token(s) tried).  "
            f"Try a more on-topic query — e.g., "
            f"*'red fruit'*, *'horse with saddle'*, *'car engine'*."
        )

        # Show why each token failed
        st.markdown("**Per-token recall diagnostic:**")
        for tok, td2 in trace["per_token"].items():
            pa2 = td2["per_agent"][winner]
            icon = "OK" if pa2["recognized"] else "X "
            st.caption(
                f"{icon} `{tok}` → score={pa2['h_score']:.5f}  "
                f"recognized={pa2['recognized']}  weight={pa2['recall_weight']:.5f}"
            )


# Main application

def main():
    st.set_page_config(
        page_title="EAM-TMS — Pipeline Trace",
        page_icon="🍎",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown("""<style>
      .block-container{padding-top:1.6rem}
      div[data-testid="stMetric"]{background:#f5f6fa;border-radius:10px;
        padding:8px 12px;border:1px solid #e6e8f0}
      .stTabs [data-baseweb="tab"]{font-size:15px;font-weight:600}
      .stProgress > div > div{border-radius:6px}
    </style>""", unsafe_allow_html=True)

    _init_session()

    # Sidebar
    with st.sidebar:
        st.title("EAM-TMS")
        st.caption("Multi-Agent Associative Memory\nTransactive Memory System")
        st.divider()

        st.subheader("Session")
        qn     = st.session_state.query_n
        counts = st.session_state.mdir_counts
        st.metric("Queries processed", qn)
        for i, cls in enumerate(CLASSES):
            st.metric(f"M_dir {DOMAIN_EMOJI[cls]} {cls}", int(counts[i]))

        total = int(counts.sum())
        if total > 0:
            h = st.session_state.mdir_mem.entropy()
            st.metric("M_dir entropy", f"{h:.3f} bits",
                      delta=f"max={np.log2(len(CLASSES)):.3f}",
                      delta_color="normal")

        st.divider()
        st.subheader("Architecture")
        st.markdown(f"""
**Each Agent — 4 AMRs:**
| AMR | Type | Dims |
|-----|------|------|
| M_dom_L | homo label | ({N},{M_LABEL}) |
| M_dom_R | homo latent | ({P_LATENT},{Q_LATENT}) |
| M_dom_H | hetero | ({N},{M_LABEL}↔{P_LATENT},{Q_LATENT}) |
| M_dir | hetero routing | ({N},{M_LABEL}→{len(CLASSES)},2) |

**TME — 2 AMRs:**
| AMR | Dims |
|-----|------|
| M_dir_L | ({N},{M_LABEL}→{len(CLASSES)},2) |
| M_dir_R | ({P_LATENT},{Q_LATENT}→{len(CLASSES)},2) |
        """)
        st.divider()
        if st.button("Reset session", type="secondary",
                     use_container_width=True):
            _reset_session()
            st.rerun()
        st.caption("Core experiment files are read-only.")

    # Model loading
    with st.spinner("Loading models (first run ~15 s)…"):
        decoder, agents, vectors_cache, g_min, g_max, nlp, ref_imgs = load_models()

    # Shared query input
    st.markdown("## Query")
    c_q, c_ex = st.columns([3, 1])
    with c_q:
        query = st.text_input(
            "Enter a natural-language query:",
            placeholder=(
                "e.g.:  a round red fruit  ·  animal with a mane  ·  "
                "fast vehicle with wheels  ·  grows on trees"
            ),
            label_visibility="collapsed",
            key="main_query",
        )
    with c_ex:
        example = st.selectbox(
            "Quick examples", label_visibility="collapsed",
            options=[
                "", "a round red fruit", "animal with a mane",
                "fast vehicle with wheels", "has an engine",
                "farm animal that gives milk", "a mug for hot coffee",
                "a barking domestic pet", "a bosc pear from the orchard",
                "red fruit used for sauce", "made into pie",
                "a mare with a foal", "a puppy in the kennel",
            ],
            key="example_sel",
        )
        if example:
            query = example

    col_run, col_norm = st.columns([2, 2])
    with col_run:
        run_btn = st.button("Run pipeline", type="primary",
                             use_container_width=True, disabled=not query)
    with col_norm:
        norm_on = st.toggle(
            "Scoring oficial (gate de containment)",
            value=True, key="norm_toggle",
            help="ON: activación media gateada por containment (el agente no opina "
                 "sobre cues fuera de su relación). OFF: score crudo sin gate.",
        )

    if run_btn and query:
        with st.spinner("Running full pipeline trace…"):
            trace = compute_pipeline_trace(
                query, agents, vectors_cache, g_min, g_max, decoder, nlp,
                normalize=norm_on)

        if trace is None:
            st.warning(
                "Ningún token es representable (sin vector fastText real). "
                "No hay pista que entregar a la memoria."
            )
        elif trace.get("rejected"):
            st.warning(
                "Rechazo de la EAM: ningún agente contiene las pistas "
                "(scores en cero). No se asigna ganador por desempate."
            )
        else:
            # Register in session M_dir (side effect happens exactly once here)
            for td in trace["per_token"].values():
                st.session_state.mdir_mem.register(td["q_vec"], trace["winner_idx"])
            st.session_state.mdir_counts[trace["winner_idx"]] += trace["n_tokens"]
            st.session_state.query_n += 1
            st.session_state.last_trace = trace
            st.session_state.history.append({
                "query":      trace["query"],
                "tokens":     trace.get("tokens_representable",
                                        trace["tokens_known"]),
                "winner":     trace["winner"],
                "winner_idx": trace["winner_idx"],
                "avg_scores": trace["avg_scores"],
                "n_tokens":   trace["n_tokens"],
            })

    st.divider()

    # Tabs
    tab_trace, tab_routing, tab_mdir, tab_mature, tab_image, tab_info = st.tabs([
        "Pipeline Trace",
        "Routing Summary",
        "M_dir Evolution",
        "Mature Phase",
        "Imagen → Etiquetas",
        "ETH-80 Reference",
    ])

    # TAB 1: Pipeline Trace
    with tab_trace:
        if st.session_state.last_trace is None:
            st.info(
                "Enter a query above and click **▶ Run pipeline** to see the "
                "full step-by-step trace of how EAM-TMS processes it."
            )
            st.markdown("""
### What the trace shows

| Stage | What you see |
|-------|-------------|
| **1 · Sentence Decomposition** | spaCy tokens with POS tags, stopword flags, vocabulary status |
| **2 · Serialization** | FastText 300D heatmap → v/S ∈ [−1,1] → quantize_binary() (magnitud) visualised as colour grids |
| **3 · TME Broadcast** | v_q sent simultaneously to all agents |
| **4 · Per-Agent AMR Processing** | For each agent: M_dom_L recog_weights (300D heatmap), M_dom_H recognition score + recall result |
| **5 · TME Decision + M_dir** | Aggregated scores, winner, M_dir bar chart after update |
| **6 · Recall & Reconstruction** | recalled_q (64D heatmap) → dequantize → decoder → reconstructed image vs. ETH-80 reference |
            """)
        else:
            render_pipeline_trace(
                st.session_state.last_trace, ref_imgs, g_min, g_max)

    # TAB 2: Routing Summary
    with tab_routing:
        st.header("Routing Summary")
        if st.session_state.last_trace is None:
            st.info("Run a query to see routing results.")
        else:
            trace  = st.session_state.last_trace
            winner = trace["winner"]
            wcolor = DOMAIN_COLOR[winner]

            st.markdown(
                f"""<div style='background:{wcolor}22;border-left:6px solid {wcolor};
                    padding:16px;border-radius:8px;margin:12px 0'>
                  <span style='font-size:28px'>{DOMAIN_EMOJI[winner]}</span>
                  <span style='font-size:20px;font-weight:bold;color:{wcolor}'>
                   → Agent <b>{winner.upper()}</b></span>
                  <span style='color:#555;margin-left:16px'>
                  score={trace['avg_scores'][winner]:.5f}</span>
                </div>""",
                unsafe_allow_html=True,
            )

            tok_badges = "  ".join(
                f"`{t}`" for t in trace.get("tokens_representable",
                                            trace["tokens_known"]))
            st.markdown(f"**Tokens usados (representables):** {tok_badges}")

            c_g, c_s, c_i = st.columns([2, 1.5, 1])
            with c_g:
                st.plotly_chart(
                    _routing_graph(trace["avg_scores"], winner,
                                   title=f'"{trace["query"]}"'),
                    use_container_width=True,
                    key="tab2_graph",
                )
            with c_s:
                st.markdown("**Scores per agent:**")
                max_s = max(trace["avg_scores"].values())
                for cls in CLASSES:
                    s   = trace["avg_scores"][cls]
                    pct = s / max(max_s, 1e-9)
                    bld = "**" if cls == winner else ""
                    st.markdown(f"{DOMAIN_EMOJI[cls]} {bld}{cls}{bld}")
                    st.progress(float(np.clip(pct, 0, 1)), text=f"{s:.5f}")
            with c_i:
                st.markdown(f"**Recalled ({winner}):**")
                if trace["final_recalled_img"] is not None:
                    st.image(_t2img(trace["final_recalled_img"]),
                             width=120, caption=f"Prototype {winner}")
                else:
                    st.info("Not recognized")
                ref_np = ref_imgs[winner].permute(1, 2, 0).numpy()
                st.image(_t2img(ref_np), width=120, caption="ETH-80 ref")

            with st.expander("Per-token score breakdown"):
                fig = go.Figure()
                toks = list(trace["per_token"].keys())
                for cls in CLASSES:
                    scores = [trace["per_token"][t]["per_agent"][cls]["h_score"]
                              for t in toks]
                    fig.add_trace(go.Bar(
                        name=f"{DOMAIN_EMOJI[cls]} {cls}", x=toks, y=scores,
                        marker_color=DOMAIN_COLOR[cls],
                    ))
                fig.update_layout(
                    barmode="group",
                    title=dict(text="M_dom_H score per token × agent",
                               x=0.5, font=dict(size=12)),
                    height=240, margin=dict(l=20, r=20, t=50, b=20),
                    plot_bgcolor="white", paper_bgcolor="#f8f9fa",
                    legend=dict(orientation="h", y=1.1),
                )
                st.plotly_chart(fig, use_container_width=True, key="tab2_tokbar")

        if len(st.session_state.history) > 1:
            with st.expander(
                    f"Session history ({len(st.session_state.history)} queries)"):
                import pandas as pd
                rows = []
                for r in reversed(st.session_state.history):
                    rows.append({
                        "Query":   r["query"],
                        "Tokens":  " | ".join(r["tokens"]),
                        "Winner":  f"{DOMAIN_EMOJI[r['winner']]} {r['winner']}",
                        "Score":   f"{r['avg_scores'][r['winner']]:.5f}",
                        "#Tokens": r["n_tokens"],
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True)

    # TAB 3: M_dir Evolution
    with tab_mdir:
        st.header("M_dir Evolution — Bias Accumulation")
        st.caption(
            "Every time a query routes to an agent, that agent's M_dir slot grows. "
            "Over many queries, dominant agents accumulate bias. "
            "B1 normalisation (÷count) corrects this in the mature phase."
        )
        qn     = st.session_state.query_n
        counts = st.session_state.mdir_counts

        if qn == 0:
            st.info("Process at least one query to see M_dir evolution.")
        else:
            st.plotly_chart(_mdir_bar(counts, qn), use_container_width=True,
                            key="tab3_mdir")

            total = int(counts.sum())
            max_c = int(counts.max())
            min_c = int(counts.min())
            c1, c2, c3 = st.columns(3)
            with c1:
                dom = CLASSES[int(counts.argmax())]
                st.metric("Dominant agent",
                          f"{DOMAIN_EMOJI[dom]} {dom}",
                          f"{max_c}/{total} registrations")
            with c2:
                ratio = max_c / max(min_c, 1)
                st.metric("max/min ratio", f"{ratio:.1f}×",
                          delta="biased" if ratio > 2 else "balanced",
                          delta_color="inverse" if ratio > 2 else "normal")
            with c3:
                if total > 0:
                    h = st.session_state.mdir_mem.entropy()
                    st.metric("M_dir entropy", f"{h:.3f} bits",
                              delta=f"max={np.log2(len(CLASSES)):.3f}")

            if len(st.session_state.history) > 1:
                st.subheader("Query-by-query evolution")
                running = np.zeros(len(CLASSES), dtype=np.int64)
                evo = {"q": [], **{cls: [] for cls in CLASSES}}
                for i, r in enumerate(st.session_state.history):
                    running[r["winner_idx"]] += r["n_tokens"]
                    evo["q"].append(i + 1)
                    for j, cls in enumerate(CLASSES):
                        evo[cls].append(int(running[j]))

                fig_evo = go.Figure()
                for cls in CLASSES:
                    fig_evo.add_trace(go.Scatter(
                        x=evo["q"], y=evo[cls],
                        name=f"{DOMAIN_EMOJI[cls]} {cls}",
                        line=dict(color=DOMAIN_COLOR[cls], width=2.5),
                        mode="lines+markers",
                    ))
                fig_evo.update_layout(
                    title=dict(
                        text="Cumulative M_dir registrations per query",
                        x=0.5, font=dict(size=13)),
                    xaxis_title="Query #",
                    yaxis_title="Cumulative registrations",
                    height=300, legend=dict(orientation="h", y=1.1),
                    plot_bgcolor="white", paper_bgcolor="#f8f9fa",
                    margin=dict(l=20, r=20, t=60, b=20),
                )
                st.plotly_chart(fig_evo, use_container_width=True, key="tab3_evo")

            dom = CLASSES[int(counts.argmax())]
            ratio = max_c / max(min_c, 1)
            if ratio > 2 and qn >= 5:
                st.warning(
                    f"**Bias detected:** {DOMAIN_EMOJI[dom]} **{dom}** dominates M_dir "
                    f"({ratio:.1f}× max/min). In the mature phase, most queries will be "
                    f"routed to {dom} unless B1 normalisation is applied."
                )
            elif qn >= 3:
                st.success("M_dir is relatively balanced.")

    # TAB 4: Mature Phase
    with tab_mature:
        st.header("Mature Phase — Point-to-Point Routing via M_dir")
        st.caption(
            "TME disabled. Entry agent receives query, consults its M_dir "
            "(what it learned during early phase), and routes to the correct agent. "
            "B1 normalisation (÷count+eps) corrects frequency bias."
        )

        # M_dir source: session / experiment pickles / live N=80
        src_mode = st.radio(
            "Fuente de M_dir:",
            ["Sesión actual (lo que enseñaste en esta sesión)",
             "Experimento entrenado (stage6 real — models/agent_*.pkl)",
             "Entrenado en vivo — 80 queries del banco (10 por clase)"],
            horizontal=True, key="mdir_src",
        )
        use_experiment = src_mode.startswith("Experimento")
        use_n80        = src_mode.startswith("Entrenado en vivo")

        b1_on = st.toggle(
            "Normalización B1 (÷count+1) — condición B1 del ablation",
            value=True, key="b1_toggle",
            help="ON = routing con B1 (condición B1: 98-100% accuracy). "
                 "OFF = scores crudos de M_dir (condición A: 33-40%) — "
                 "verás el sesgo de frecuencia en vivo.",
        )

        if use_experiment:
            st.caption(
                "Modo experimento: usa los agentes entrenados del experimento real. "
                "Con B1 ON ejecuta `stage8_mature.route_mature()` **sin modificación**; "
                "con B1 OFF lee el mismo M_dir entrenado con scores crudos "
                "(condición A del ablation) — solo lectura en ambos casos."
            )
            with st.expander("Vocabulario que el M_dir del experimento aprendió "
                             "(todo lo demás se rechaza)"):
                with st.spinner("Cargando estado del experimento…"):
                    tme_v, _agents_v = load_experiment_state()
                from stage6_interaction import TEST_QUERIES as _TQ
                vocab_rows = []
                for _q in _TQ:
                    for _t in tokenize_query(_q, nlp):
                        if not token_in_vocabulary(_t, vectors_cache):
                            continue
                        _vq = quantize_binary(np.array(
                            get_fasttext_vector(_t, vectors_cache),
                            dtype=np.float32), M_LABEL)
                        _s = tme_v.mem_dir_L.predict(_vq)
                        if _s.sum() > 0:
                            vocab_rows.append(
                                (_t, CLASSES[int(np.argmax(_s))]))
                vocab_rows = sorted(set(vocab_rows))
                st.markdown("  ".join(
                    f"`{t}`→{DOMAIN_EMOJI[o]}" for t, o in vocab_rows))
                st.caption(
                    f"{len(vocab_rows)} tokens con señal en M_dir, aprendidos de "
                    f"las {len(_TQ)} TEST_QUERIES de la fase temprana. "
                    "Nota: entra como pista todo token representable por fastText "
                    "(no solo los del vocabulario de labels); aquí se listan los "
                    "que el directorio efectivamente aprendió."
                )
        mdir80 = None
        if use_n80:
            norm80 = st.session_state.get("norm_toggle", True)
            with st.spinner("Entrenando M_dir con 80 queries del banco "
                            "(en memoria, primera vez ~10–30 s)…"):
                mdir80, stats80 = train_mdir_n80(norm80)
            acc80 = stats80["correct"] / max(stats80["n"], 1)
            cm1, cm2, cm3 = st.columns(3)
            with cm1:
                st.metric("Queries de entrenamiento", stats80["n"])
            with cm2:
                st.metric("Routing correcto (vs ground truth)",
                          f"{acc80*100:.1f}%",
                          delta="scoring gateado (recognize_gated)" if norm80
                          else "RAW (sesgo activo)",
                          delta_color="normal" if norm80 else "inverse")
            with cm3:
                st.metric("Vocabulario M_dir",
                          f"{len(stats80['vocab'])} tokens",
                          delta=f"counts={mdir80.agent_counts.tolist()}")
            st.caption(
                "M_dir entrenado en memoria con las primeras 80 queries del "
                "banco de evaluación de 8 clases (eval_bank.ALL_QUERIES, "
                "10 por clase, importado solo-lectura). "
                "El routing de entrenamiento usa el toggle de normalización de arriba — "
                "cámbialo para comparar M_dir limpio vs M_dir sesgado. "
                "Nada se escribe a disco."
            )
            with st.expander(f"Vocabulario aprendido "
                             f"({len(stats80['vocab'])} tokens)"):
                st.markdown("  ".join(
                    f"`{t}`→{DOMAIN_EMOJI[o]}"
                    for t, o in sorted(stats80["vocab"].items())))

        qn = st.session_state.query_n
        if not use_experiment and not use_n80 and qn < 3:
            st.info("Procesa al menos 3 queries en fase temprana primero, "
                    "o cambia a 'Experimento entrenado' / '80 queries'.")
        else:
            query_m = st.text_input(
                "Query for mature phase:",
                placeholder="e.g.: animal with a mane",
                key="query_mature",
            )
            c_e, c_b = st.columns([2, 1])
            with c_e:
                entry_cls = st.selectbox(
                    "Entry agent (random in the real system):", CLASSES,
                    format_func=lambda c: f"{DOMAIN_EMOJI[c]} {c}",
                )
            with c_b:
                run_m = st.button("Run mature phase", type="primary",
                                  use_container_width=True,
                                  disabled=not query_m)

            if run_m and query_m:
                # Compute routing (two backends, same visualisation)
                dest_cls = None
                mdir_scores = {}
                recalled_img = None
                rejected = False

                # Shared tokenization. Sin filtro léxico: tokens representables
                # (con vector fastText real); el rechazo lo decide la memoria.
                tokens_all   = tokenize_query(query_m, nlp)
                tokens_vocab = [
                    t for t in tokens_all
                    if get_fasttext_vector(t, vectors_cache, allow_fallback=False)
                    is not None]

                if use_experiment:
                    with st.spinner("Cargando agentes entrenados del experimento "
                                    "(primera vez ~20 s, pickles de 170 MB)…"):
                        tme_exp, agents_exp = load_experiment_state()
                    if b1_on:
                        # REAL experiment path: stage8 logic, untouched (uses B1)
                        from stage8_mature import route_mature
                        res = route_mature(
                            query_m, agents_exp[entry_cls], agents_exp, nlp,
                            vectors_cache, decoder, g_min, g_max, verbose=False)
                        if res.get("rejected") or res["winner"] is None:
                            rejected = True
                        else:
                            dest_cls = res["winner"]
                            scores_list = res.get("scores", [0.0]*len(CLASSES))
                            mdir_scores = {c: float(s)
                                           for c, s in zip(CLASSES, scores_list)}
                            if res["image"] is not None:
                                recalled_img = np.clip(
                                    res["image"].permute(1, 2, 0).numpy(), 0, 1)
                    else:
                        # Raw read of the SAME trained M_dir (ablation condition A)
                        if not tokens_vocab:
                            rejected = True
                        else:
                            entry_exp = agents_exp[entry_cls]
                            agg = np.zeros(len(CLASSES), dtype=float)
                            for tok in tokens_vocab:
                                v_q = quantize_binary(np.array(
                                    get_fasttext_vector(tok, vectors_cache),
                                    dtype=np.float32), M_LABEL)
                                agg += entry_exp.mem_dir.predict(v_q)
                            if agg.sum() == 0:
                                rejected = True
                            else:
                                dest_cls = CLASSES[int(np.argmax(agg))]
                                mdir_scores = {c: float(agg[i])
                                               for i, c in enumerate(CLASSES)}
                                for tok in tokens_vocab:
                                    v_q = quantize_binary(np.array(
                                        get_fasttext_vector(tok, vectors_cache),
                                        dtype=np.float32), M_LABEL)
                                    r_q2, rec2, wt2, *_ = (
                                        agents_exp[dest_cls].mem_dom_H
                                        .recall_from_left(v_q))
                                    if rec2:
                                        recalled_img = _decode(
                                            r_q2, g_min, g_max, decoder)
                                        break
                else:
                    # Session path OR live-trained N=80 M_dir (same routing logic)
                    mdir = mdir80 if use_n80 else st.session_state.mdir_mem
                    if not tokens_vocab:
                        rejected = True
                    else:
                        cues = [quantize_binary(np.array(
                                    get_fasttext_vector(tok, vectors_cache),
                                    dtype=np.float32), M_LABEL)
                                for tok in tokens_vocab]
                        if b1_on:
                            # Decisión multi-pista DENTRO de la MAE (B1)
                            widx, agg = mdir.route_multi(cues, mode="linear")
                        else:
                            # Lectura cruda: condición A del ablation (diagnóstico)
                            agg = np.zeros(len(CLASSES), dtype=float)
                            for v_q in cues:
                                agg += mdir.predict(v_q)
                            widx = -1 if agg.sum() == 0 else int(np.argmax(agg))
                        if widx < 0:
                            rejected = True
                        else:
                            dest_cls    = CLASSES[widx]
                            mdir_scores = {cls: float(agg[i])
                                           for i, cls in enumerate(CLASSES)}
                        if dest_cls is not None:
                            for tok in tokens_vocab:
                                v_q = quantize_binary(np.array(
                                    get_fasttext_vector(tok, vectors_cache),
                                    dtype=np.float32), M_LABEL)
                                r_q2, rec2, wt2, *_ = (
                                    agents[dest_cls].mem_dom_H
                                    .recall_from_left(v_q))
                                if rec2:
                                    recalled_img = _decode(
                                        r_q2, g_min, g_max, decoder)
                                    break

                if rejected:
                    st.warning(
                        "REJECTED — sin señal de routing: el sistema rechaza "
                        "en vez de rutear al azar.")
                    # Per-token diagnostics: WHY was it rejected?
                    st.markdown("**Diagnóstico por token:**")
                    if use_experiment:
                        _tme_d, _ = load_experiment_state()
                        _mdir_d = _tme_d.mem_dir_L
                    elif use_n80:
                        _mdir_d = mdir80
                    else:
                        _mdir_d = st.session_state.mdir_mem
                    if not tokens_all:
                        st.caption("spaCy no extrajo ningún token NOUN/ADJ/PROPN "
                                   "de la query.")
                    for tok in tokens_all:
                        vec = get_fasttext_vector(tok, vectors_cache,
                                                  allow_fallback=False)
                        in_vocab = token_in_vocabulary(tok, vectors_cache)
                        tag = "label" if in_vocab else "no-label"
                        if vec is None:
                            st.caption(
                                f"NO  `{tok}` — no representable por fastText "
                                f"(sin pista para la EAM)")
                            continue
                        v_q = quantize_binary(np.asarray(vec, dtype=np.float32),
                                              M_LABEL)
                        sig = _mdir_d.predict(v_q)
                        if sig.sum() > 0:
                            st.caption(
                                f"OK  `{tok}` ({tag}) — tiene señal en M_dir "
                                f"→ {CLASSES[int(np.argmax(sig))]}")
                        else:
                            st.caption(
                                f"!!  `{tok}` ({tag}) — representable, pero **sin "
                                f"señal en M_dir** (la EAM no lo contiene / no "
                                f"apareció en la fase temprana)")
                    st.info(
                        "La fase temprana rutea con **M_dom** (conoce los "
                        "~60 labels de ConceptNet); la madura rutea con **M_dir** "
                        "(solo conoce los tokens enseñados en interacciones). "
                        "Es el comportamiento Wegner: el directorio solo contiene "
                        "lo que fue comunicado socialmente.")
                else:
                    redirected = entry_cls != dest_cls
                    dcolor     = DOMAIN_COLOR[dest_cls]

                    # Animated mature flow
                    st.markdown("### Animated Mature Flow")
                    st.caption(
                        "TME apagado (gris) · el cue viaja al agente de entrada · "
                        "consulta su M_dir (B1) · redirección punto a punto · "
                        "recall en el destino. Sin aprendizaje: M_dir está congelado."
                    )
                    words_m, toks_m, known_m = _decompose_anim_data(
                        query_m, nlp, vectors_cache)
                    _mat_html = None
                    if toks_m:
                        _mat_html = build_mature_animation(
                            query_m, words_m, toks_m, entry_cls, dest_cls,
                            mdir_scores, recalled_img)
                        components.html(_mat_html, height=_ANIM_H,
                                        scrolling=False)
                    # Payload para exportar a video: sobrevive los reruns que
                    # provoca el botón "Generar video" (run_m vuelve a False).
                    st.session_state["mature_vid_payload"] = {
                        "query": query_m, "tokens": known_m,
                        "entry": entry_cls, "dest": dest_cls,
                        "scores": dict(mdir_scores), "img": recalled_img,
                        "html": _mat_html,
                    }

                    # Banner
                    if redirected:
                        st.markdown(
                            f"""<div style='background:#f39c1222;
                                border-left:6px solid #f39c12;
                                padding:14px;border-radius:8px;margin:10px 0'>
                              <b>Redirect detected</b>
                              {'· <i>experimento real (stage8)</i>' if use_experiment else ''}<br>
                              <span style='font-size:18px'>
                                {DOMAIN_EMOJI[entry_cls]} {entry_cls}
                                &nbsp;→&nbsp;
                                <span style='color:{dcolor};font-weight:bold'>
                                  {DOMAIN_EMOJI[dest_cls]} {dest_cls.upper()}
                                </span>
                              </span>
                            </div>""",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""<div style='background:#2ecc7122;
                                border-left:6px solid #2ecc71;
                                padding:14px;border-radius:8px;margin:10px 0'>
                              <b>No redirect</b> — entry = destination:
                              {DOMAIN_EMOJI[entry_cls]} {entry_cls}
                              {'· <i>experimento real (stage8)</i>' if use_experiment else ''}
                            </div>""",
                            unsafe_allow_html=True,
                        )

                    c_g, c_s, c_i = st.columns([2, 1.5, 1])
                    with c_g:
                        fig_m = _routing_graph(
                            mdir_scores, dest_cls,
                            title=f'Mature: "{query_m}"',
                            highlight_path=(entry_cls, dest_cls) if redirected else None,
                        )
                        st.plotly_chart(fig_m, use_container_width=True,
                                        key="tab4_mature")
                        if redirected:
                            st.caption(
                                "Orange arrow = M_dir-driven redirect "
                                "(point-to-point, no TME involved).")

                    with c_s:
                        src_lbl = ("M_dir del experimento (stage6 entrenado)"
                                   if use_experiment
                                   else "M_dir N=80 (banco del ablation)"
                                   if use_n80 else "M_dir de la sesión")
                        b1_lbl = ("B1 ÷count" if b1_on
                                  else "RAW — condición A (sesgo activo)")
                        st.markdown(f"**{src_lbl} — scores {b1_lbl}:**")
                        total_m = sum(mdir_scores.values())
                        for cls in CLASSES:
                            s   = mdir_scores.get(cls, 0.0)
                            pct = s / max(total_m, 1e-9)
                            st.markdown(f"{DOMAIN_EMOJI[cls]} {cls}")
                            st.progress(float(np.clip(pct, 0, 1)),
                                        text=f"{s:.3f} ({pct:.0%})")

                    with c_i:
                        st.markdown(f"**Recall ({dest_cls}):**")
                        if recalled_img is not None:
                            st.image(_t2img(recalled_img), width=120)
                        else:
                            st.info("Not recalled")

                    with st.expander("Compare early vs mature"):
                        early = compute_pipeline_trace(
                            query_m, agents, vectors_cache,
                            g_min, g_max, decoder, nlp,
                            normalize=st.session_state.get("norm_toggle", True))
                        if early:
                            e_w = early["winner"]
                            st.metric("Early phase (M_dom)",
                                      f"{DOMAIN_EMOJI[e_w]} {e_w}")
                            st.metric("Mature phase (M_dir)",
                                      f"{DOMAIN_EMOJI[dest_cls]} {dest_cls}")
                            if e_w == dest_cls:
                                st.success("Fidelity OK — mature matches early phase.")
                            else:
                                st.error(
                                    f"Fidelity FAIL: "
                                    f"early={e_w}, mature={dest_cls}. "
                                    f"M_dir bias may be affecting routing."
                                )

            # Exportación a video del último ruteo maduro (persiste en
            # session_state, así que sobrevive el rerun del botón).
            _mp = st.session_state.get("mature_vid_payload")
            if _mp:
                from app_video import render_mature_video
                _video_export_ui(
                    "ruteo_maduro",
                    _mp["query"] + ">" + _mp["entry"] + ">" + _mp["dest"],
                    html=_mp.get("html"), height=_ANIM_H,
                    builder=lambda: render_mature_video(
                        _mp["query"], _mp["tokens"], _mp["entry"],
                        _mp["dest"], _mp["scores"], list(CLASSES),
                        DOMAIN_COLOR, _mp["img"]))

    # TAB 5: ETH-80 Reference
    with tab_image:
        st.header("Imagen → Etiquetas (hemisferio visual)")
        st.caption(
            "El encoder ResNet18 es solo el «ojo» que convierte la imagen en una "
            "pista vectorial. Ruteo estilo fase madura: la imagen entra por el agente "
            "que elijas, y ese agente consulta SU PROPIO directorio visual "
            "(M_dir_R, lectura B1) — si ningún especialista la conoce se rechaza, y si "
            "alguien la conoce redirige a ese especialista, que evoca etiquetas y "
            "reconstruye desde su memoria (no es la imagen de entrada).")

        entry = st.selectbox(
            "Agente de entrada (cualquiera puede recibir la imagen)", CLASSES,
            format_func=lambda c: f"{DOMAIN_EMOJI[c]} {c}", key="img_entry")
        up = st.file_uploader("Sube una imagen (png/jpg)",
                              type=["png", "jpg", "jpeg"])
        if up is not None:
            from stage5_fill import quantize_latent_global
            from stage7_bidirectional import evoke_labels, load_global_stats
            import io as _io
            import contextlib as _ctx
            encoder = load_image_encoder()
            gmin_v, gmax_v = load_global_stats()
            tme, exp_agents = load_experiment_state()  # agentes con su mem_dir_R
            all_vecs = {}
            for _c in CLASSES:
                all_vecs.update(vectors_cache.get(_c, {}))

            pil = Image.open(_io.BytesIO(up.getvalue()))
            z = encode_pil(pil, encoder)
            z_q = quantize_latent_global(z, gmin_v, gmax_v, Q_LATENT)

            # Ruteo estilo fase madura, per-agente: el agente de entrada consulta SU
            # propio directorio visual (mem_dir_R, lectura B1 con tolerancia eta
            # XI_VISUAL — funciones parciales nativas de la EHAM) y redirige, o
            # rechaza si nadie lo conoce. La decisión la toma la MAE
            # (DirectoryMemory.route); una sola decisión para estático y animación.
            from stage7_bidirectional import XI_VISUAL
            entry_agent = exp_agents[entry]
            agg = entry_agent.mem_dir_R.predict_tolerant(z_q, xi=XI_VISUAL,
                                                         mode="linear")
            scores = {CLASSES[i]: float(agg[i]) for i in range(len(CLASSES))}
            widx = entry_agent.mem_dir_R.route(z_q, mode="linear", xi=XI_VISUAL)
            winner = CLASSES[widx] if widx >= 0 else None

            vid_labels, vid_recon = [], None   # capturados para el video
            c_in, c_out = st.columns([1, 1.4])
            with c_in:
                st.image(pil.convert("RGB").resize((128, 128)),
                         caption=f"Entrada · agente de entrada: "
                                 f"{DOMAIN_EMOJI[entry]} {entry}",
                         use_container_width=True)
                for c in CLASSES:
                    st.metric(f"{DOMAIN_EMOJI[c]} {c} · M_dir_R (B1)",
                              f"{scores[c]:.3f}")

            with c_out:
                if winner is None:
                    st.error(
                        "RECHAZADA — el directorio visual (M_dir_R) no tiene soporte "
                        "para esta percepción: ningún especialista la conoce. "
                        "El grupo no inventa referente.")
                else:
                    if winner == entry:
                        st.success(
                            f"El agente de entrada {DOMAIN_EMOJI[entry]} {entry} "
                            f"**se queda la consulta** (M_dir_R B1 {scores[winner]:.3f}).")
                    else:
                        st.success(
                            f"{DOMAIN_EMOJI[entry]} {entry} no la conoce → **redirige a "
                            f"{DOMAIN_EMOJI[winner]} {winner}** vía M_dir_R "
                            f"(B1 {scores[winner]:.3f}).")
                    labels = evoke_labels(exp_agents[winner], z_q, all_vecs)
                    vid_labels = list(labels)
                    st.markdown("**Etiquetas evocadas (top-3):** " +
                                "  ".join(f"`{w}`" for w in labels))
                    with _ctx.redirect_stdout(_io.StringIO()):
                        r_io, recognized, _w = exp_agents[winner].mem_dom_R.recall(z_q)
                    if recognized:
                        rec_img = _decode(r_io, gmin_v, gmax_v, decoder)
                        vid_recon = rec_img
                        st.image(_t2img(rec_img),
                                 caption="Reconstrucción evocada por la MAE "
                                         "(decode(mem_dom_R.recall), no la entrada)",
                                 use_container_width=True)
                    else:
                        st.info("El especialista destino recibió la consulta pero su "
                                "recall no produjo un patrón estable para reconstruir.")

            # Animación del flujo imagen → etiquetas (estilo fase madura: entrada →
            # directorio visual M_dir_R del TME → redirige/rechaza).
            st.divider()
            st.subheader("Animación del flujo imagen → etiquetas (estilo fase madura)")
            _img_html = build_image_to_labels_animation(
                pil, z_q, scores, entry, winner, exp_agents, all_vecs,
                decoder, gmin_v, gmax_v)
            components.html(_img_html, height=_ANIM_IMG_H, scrolling=False)

            _q_np = np.asarray(pil.convert("RGB").resize((128, 128)),
                               dtype=np.float32) / 255.0
            from app_video import render_image_video
            _video_export_ui(
                "ruteo_imagen",
                f"{up.name}>{entry}>{winner}",
                html=_img_html, height=_ANIM_IMG_H,
                builder=lambda: render_image_video(
                    _q_np, z_q, scores, entry, winner, vid_labels,
                    list(CLASSES), DOMAIN_COLOR, recon_img=vid_recon))

    with tab_info:
        st.header("ETH-80 Reference Images")
        st.caption("One representative training image per domain.")

        # Filas de 4 para las 8 clases (antes st.columns(3)+zip truncaba a 3).
        _PR = 4
        for _start in range(0, len(CLASSES), _PR):
            _chunk = CLASSES[_start:_start + _PR]
            for col, cls in zip(st.columns(_PR), _chunk):
                with col:
                    st.subheader(f"{DOMAIN_EMOJI[cls]} {cls}")
                    img_np = ref_imgs[cls].permute(1, 2, 0).numpy()
                    st.image(_t2img(img_np), caption=f"ETH-80 — {cls}",
                             use_container_width=True)

        st.divider()
        st.subheader("ConceptNet labels per domain")
        for _start in range(0, len(CLASSES), _PR):
            _chunk = CLASSES[_start:_start + _PR]
            for col, cls in zip(st.columns(_PR), _chunk):
                with col:
                    lpath  = ROOT / f"labels_{cls}.json"
                    labels = json.loads(lpath.read_text())
                    st.markdown(f"**{DOMAIN_EMOJI[cls]} {cls}** — "
                                f"{len(labels)} labels")
                    for word, freq in sorted(labels.items(),
                                             key=lambda x: -x[1])[:15]:
                        st.markdown(f"- `{word}` (freq={freq})")


if __name__ == "__main__":
    main()
