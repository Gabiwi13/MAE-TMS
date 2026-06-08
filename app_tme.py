"""
Visualizador interactivo del MAE-TMS.
Muestra en tiempo real cómo el TME rutea queries entre agentes,
cómo M_dir acumula sesgo, y cómo la fase madura redirige.

Ejecutar:
  streamlit run app_tme.py

No modifica ningún archivo del experimento core.
"""
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import streamlit as st
import plotly.graph_objects as go
import torch
from PIL import Image
from torchvision import transforms

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from quantizer import quantize_binary
from stage6_interaction import (
    CLASSES, AGENT_LIST, MODELS_DIR, Agent,
    get_nlp, load_all_vectors,
    tokenize_query, get_fasttext_vector, M_LABEL, N,
)
from pineda_am import PinedaDirectoryMemory

# ─────────────────────────────────────────────────────────────────
# Constantes visuales
# ─────────────────────────────────────────────────────────────────

DOMAIN_COLOR = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60"}
DOMAIN_EMOJI = {"apple": "🍎", "horse": "🐴", "car": "🚗"}
Q_LATENT = 32

# Posiciones de nodos en el grafo (x, y)
NODE_POS = {
    "TME":   (0.0,  0.0),
    "apple": (-2.0, 0.0),
    "horse": (1.0,  1.7),
    "car":   (1.0, -1.7),
}


# ─────────────────────────────────────────────────────────────────
# Carga de modelos (cacheados, se cargan una vez)
# ─────────────────────────────────────────────────────────────────

@st.cache_resource
def load_models():
    """Carga todos los modelos necesarios. No modifica ningún archivo."""
    from stage2_encoder import Decoder
    from stage5_fill import load_agent_memories

    # Decoder
    decoder = Decoder()
    decoder.load_state_dict(torch.load(
        MODELS_DIR / "decoder.pt", map_location="cpu"))
    decoder.eval()

    # Agentes con 4 AMRs: M_dom_H + M_dom_L + M_dom_R + M_dir vacío
    # M_dom_L se usa para pesos de reconocimiento (Pineda's left_eam pattern)
    agents = {}
    for cls in CLASSES:
        mem_H, mem_L, mem_R = load_agent_memories(cls)
        agents[cls] = Agent(cls, mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)

    # Vectores fastText (cache en memoria)
    vectors_cache = load_all_vectors()

    # Stats globales del espacio latente
    stats = json.loads((MODELS_DIR / "latent_global_stats.json").read_text())
    g_min = np.array(stats["global_min"])
    g_max = np.array(stats["global_max"])

    # spaCy (pesado, cargarlo una sola vez)
    nlp = get_nlp()

    # Una imagen real de referencia por dominio
    splits = json.loads((ROOT / "data" / "eth80" / "splits.json").read_text())
    to_t = transforms.ToTensor()
    ref_imgs = {}
    for cls in CLASSES:
        path = splits[cls]["train"][0]
        img = Image.open(path).convert("RGB").resize((128, 128))
        ref_imgs[cls] = to_t(img)

    return decoder, agents, vectors_cache, g_min, g_max, nlp, ref_imgs


# ─────────────────────────────────────────────────────────────────
# Funciones de routing (no tocan archivos existentes)
# ─────────────────────────────────────────────────────────────────

def dequantize_latent(q_vals, g_min, g_max):
    v_norm = q_vals.astype(float) / (Q_LATENT - 1)
    return (v_norm * (g_max - g_min) + g_min).astype(np.float32)


def decode_image(recalled_q, g_min, g_max, decoder):
    v_lat = dequantize_latent(recalled_q, g_min, g_max)
    z = torch.tensor(v_lat).unsqueeze(0)
    with torch.no_grad():
        img = decoder(z)[0].clamp(0, 1)
    return img.permute(1, 2, 0).numpy()


def route_query_early(query, agents, vectors_cache, g_min, g_max, decoder, nlp):
    """
    Reproduce la fase temprana:
    query → tokens → M_dom scores → ganador → recall imagen.

    Usa agent.recognize(v_q) que aplica M_dom_L.recog_weights() como pesos
    sobre M_dom_H.recognize_from_left() — patrón Pineda left_eam → hetero_eam.
    También registra los vectores ganadores en st.session_state.mdir_mem
    (PinedaDirectoryMemory) para routing real en la fase madura.
    """
    tokens = tokenize_query(query, nlp)
    if not tokens:
        return None

    per_token_scores = {}   # tok → {cls: score}
    token_vecs = {}         # tok → v_q

    for tok in tokens:
        v = get_fasttext_vector(tok, vectors_cache)
        v_q = quantize_binary(v, M_LABEL)
        token_vecs[tok] = v_q
        # agent.recognize() aplica pesos de M_dom_L internamente
        per_token_scores[tok] = {
            cls: float(agents[cls].recognize(v_q))
            for cls in CLASSES
        }

    # Suma y promedio de scores por agente
    total_scores = {cls: 0.0 for cls in CLASSES}
    for tok in tokens:
        for cls in CLASSES:
            total_scores[cls] += per_token_scores[tok][cls]
    avg_scores = {cls: total_scores[cls] / len(tokens) for cls in CLASSES}

    winner = max(avg_scores, key=avg_scores.get)
    winner_idx = AGENT_LIST.index(winner)

    # Registrar en M_dir de sesión (PinedaDirectoryMemory — B1 normalizable)
    for v_q in token_vecs.values():
        st.session_state.mdir_mem.register(v_q, winner_idx)

    # Recall imagen del ganador con el primer token reconocido
    recalled_img = None
    for tok, v_q in token_vecs.items():
        recalled_q, recognized, _ = agents[winner].mem_dom_H.recall_from_left(v_q)
        if recognized:
            recalled_img = decode_image(recalled_q, g_min, g_max, decoder)
            break

    return {
        "query":            query,
        "tokens":           tokens,
        "token_vecs":       token_vecs,
        "per_token_scores": per_token_scores,
        "total_scores":     total_scores,
        "avg_scores":       avg_scores,
        "winner":           winner,
        "winner_idx":       winner_idx,
        "recalled_img":     recalled_img,
    }


def route_query_mature(query, agents, vectors_cache,
                       g_min, g_max, decoder, nlp, entry_cls=None, seed=None):
    """
    Fase madura: usa st.session_state.mdir_mem (PinedaDirectoryMemory) para redirigir.
    Aplica normalización B1 (÷count) — congruente con la condición G del ablation.
    """
    tokens = tokenize_query(query, nlp)
    if not tokens:
        return None

    if entry_cls is None:
        rng = np.random.RandomState(seed if seed else 42)
        entry_cls = CLASSES[rng.randint(0, 3)]

    mdir_mem = st.session_state.mdir_mem
    counts = mdir_mem.agent_counts

    # Routing real: predict_normalized(B1) agregado sobre todos los tokens
    agg_scores = np.zeros(len(CLASSES), dtype=float)
    for tok in tokens:
        v = get_fasttext_vector(tok, vectors_cache)
        v_q = quantize_binary(v, M_LABEL)
        agg_scores += mdir_mem.predict_normalized(v_q, mode="linear")

    if agg_scores.sum() == 0:
        # M_dir vacío: distribución uniforme
        mdir_scores = {cls: 1 / 3 for cls in CLASSES}
        dest_cls = entry_cls
    else:
        dest_idx  = int(np.argmax(agg_scores))
        dest_cls  = CLASSES[dest_idx]
        mdir_scores = {cls: float(agg_scores[i]) for i, cls in enumerate(CLASSES)}

    # Recall desde el agente destino (M_dom_H)
    recalled_img = None
    for tok in tokens:
        v = get_fasttext_vector(tok, vectors_cache)
        v_q = quantize_binary(v, M_LABEL)
        recalled_q, recognized, _ = agents[dest_cls].mem_dom_H.recall_from_left(v_q)
        if recognized:
            recalled_img = decode_image(recalled_q, g_min, g_max, decoder)
            break

    return {
        "query":        query,
        "tokens":       tokens,
        "entry_cls":    entry_cls,
        "dest_cls":     dest_cls,
        "mdir_scores":  mdir_scores,
        "recalled_img": recalled_img,
    }


# ─────────────────────────────────────────────────────────────────
# Gráficas Plotly
# ─────────────────────────────────────────────────────────────────

def make_routing_graph(avg_scores: dict, winner: str,
                       title: str = "", highlight_path=None):
    """
    Grafo TME → agentes.
    avg_scores: {cls: score}
    winner: agente ganador
    highlight_path: tupla (from_node, to_node) para fase madura
    """
    max_score = max(avg_scores.values()) if avg_scores else 1
    fig = go.Figure()

    # ── Aristas (flechas de TME a cada agente) ────────────────────
    for cls in CLASSES:
        x0, y0 = NODE_POS["TME"]
        x1, y1 = NODE_POS[cls]
        score  = avg_scores.get(cls, 0)
        norm   = score / max(max_score, 1e-9)
        is_win = cls == winner

        color = DOMAIN_COLOR[cls] if is_win else "#c8c8c8"
        width = 6 if is_win else max(1, 3 * norm)

        # Línea de arista
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1],
            mode="lines",
            line=dict(color=color, width=width),
            hoverinfo="none", showlegend=False,
        ))
        # Anotación de score en el centro de la arista
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        fig.add_annotation(
            x=mid_x, y=mid_y,
            text=f"{score:.2f}",
            showarrow=False,
            font=dict(size=10, color=color if is_win else "#888"),
            bgcolor="white",
            opacity=0.85,
        )

    # ── Arista de fase madura (si aplica) ─────────────────────────
    if highlight_path:
        from_node, to_node = highlight_path
        x0, y0 = NODE_POS[from_node]
        x1, y1 = NODE_POS[to_node]
        fig.add_annotation(
            x=x1, y=y1,
            ax=x0, ay=y0,
            xref="x", yref="y",
            axref="x", ayref="y",
            arrowhead=3, arrowwidth=5,
            arrowcolor="#f39c12",
            text="",
        )

    # ── Nodos ─────────────────────────────────────────────────────
    for name, (nx, ny) in NODE_POS.items():
        is_win  = name == winner
        is_tme  = name == "TME"
        color   = DOMAIN_COLOR.get(name, "#2c3e50")
        label   = f"{DOMAIN_EMOJI.get(name, '')} {name}"

        marker_size    = 32 if is_tme else (28 if is_win else 22)
        border_color   = "gold" if is_win else "white"
        border_width   = 5    if is_win else 2

        fig.add_trace(go.Scatter(
            x=[nx], y=[ny],
            mode="markers+text",
            marker=dict(
                size=marker_size, color=color,
                line=dict(width=border_width, color=border_color),
            ),
            text=[label],
            textposition=("middle left" if nx < 0
                          else "top center" if ny > 0
                          else "bottom center"),
            textfont=dict(
                size=13 if is_win else 11,
                color=color,
                family="monospace",
            ),
            hoverinfo="text",
            hovertext=name,
            showlegend=False,
        ))

    fig.update_layout(
        xaxis=dict(visible=False, range=[-3.0, 2.5]),
        yaxis=dict(visible=False, range=[-2.8, 2.8]),
        height=360,
        margin=dict(l=10, r=10, t=50, b=10),
        title=dict(text=title, x=0.5, font=dict(size=14)),
        plot_bgcolor="white",
        paper_bgcolor="#f8f9fa",
    )
    return fig


def make_mdir_bar(mdir_counts: np.ndarray, query_n: int):
    """Barras de registros M_dir acumulados por agente."""
    fig = go.Figure()
    colors = [DOMAIN_COLOR[cls] for cls in CLASSES]
    labels = [f"{DOMAIN_EMOJI[cls]} {cls}" for cls in CLASSES]
    values = mdir_counts.tolist()

    fig.add_trace(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        marker_line_color="white", marker_line_width=2,
        text=[f"{v}" for v in values],
        textposition="outside",
    ))

    total = sum(values)
    ideal = total / 3 if total > 0 else 0
    if ideal > 0:
        fig.add_hline(y=ideal, line_dash="dot", line_color="#7f8c8d",
                      annotation_text=f"Ideal ({ideal:.0f})",
                      annotation_position="right")

    fig.update_layout(
        title=dict(
            text=f"Registros M_dir — {query_n} queries procesadas",
            x=0.5, font=dict(size=13)),
        yaxis_title="Registros acumulados",
        height=280,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="white",
        paper_bgcolor="#f8f9fa",
        showlegend=False,
    )
    return fig


def make_token_score_table(per_token_scores: dict):
    """Tabla de scores por token × agente."""
    tokens = list(per_token_scores.keys())
    apple_s = [per_token_scores[t]["apple"] for t in tokens]
    horse_s = [per_token_scores[t]["horse"] for t in tokens]
    car_s   = [per_token_scores[t]["car"]   for t in tokens]

    fig = go.Figure(data=[
        go.Bar(name="🍎 apple", x=tokens, y=apple_s,
               marker_color=DOMAIN_COLOR["apple"]),
        go.Bar(name="🐴 horse", x=tokens, y=horse_s,
               marker_color=DOMAIN_COLOR["horse"]),
        go.Bar(name="🚗 car",   x=tokens, y=car_s,
               marker_color=DOMAIN_COLOR["car"]),
    ])
    fig.update_layout(
        barmode="group",
        title=dict(text="Score de M_dom por token × agente", x=0.5,
                   font=dict(size=13)),
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="white",
        paper_bgcolor="#f8f9fa",
        legend=dict(orientation="h", y=1.12),
        yaxis_title="Peso de reconocimiento",
    )
    return fig


def tensor_to_pil(t):
    arr = np.clip(t, 0, 1) if isinstance(t, np.ndarray) else t
    return (arr * 255).astype(np.uint8)


# ─────────────────────────────────────────────────────────────────
# Inicialización del estado de sesión
# ─────────────────────────────────────────────────────────────────

def init_session():
    if "mdir_counts" not in st.session_state:
        st.session_state.mdir_counts = np.zeros(3, dtype=np.int64)
    if "mdir_mem" not in st.session_state:
        # PinedaDirectoryMemory para routing real en fase madura (B1 normalizado)
        st.session_state.mdir_mem = PinedaDirectoryMemory(N, M_LABEL, len(CLASSES))
    if "history" not in st.session_state:
        st.session_state.history = []   # lista de resultados
    if "query_n" not in st.session_state:
        st.session_state.query_n = 0


def reset_session():
    st.session_state.mdir_counts = np.zeros(3, dtype=np.int64)
    st.session_state.mdir_mem = PinedaDirectoryMemory(N, M_LABEL, len(CLASSES))
    st.session_state.history = []
    st.session_state.query_n = 0


# ─────────────────────────────────────────────────────────────────
# App principal
# ─────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="MAE-TMS Visualizador",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session()

    # ── Sidebar ───────────────────────────────────────────────────
    with st.sidebar:
        st.title("MAE-TMS")
        st.caption("Visualizador interactivo del sistema de memoria transactiva")
        st.divider()

        st.subheader("Estado de la sesión")
        qn = st.session_state.query_n
        counts = st.session_state.mdir_counts
        st.metric("Queries procesadas", qn)
        for i, cls in enumerate(CLASSES):
            st.metric(f"M_dir {DOMAIN_EMOJI[cls]} {cls}", int(counts[i]))

        total = counts.sum()
        if total > 0:
            entropy = 0.0
            for c in counts:
                if c > 0:
                    p = c / total
                    entropy -= p * np.log2(p)
            st.metric("Entropía M_dir", f"{entropy:.3f} bits",
                      delta=f"máx={np.log2(3):.2f}",
                      delta_color="normal")

        st.divider()
        if st.button("Resetear sesión", type="secondary", width='stretch'):
            reset_session()
            st.rerun()

        st.divider()
        st.caption("Los modelos se cargan una vez y se reutilizan.\n"
                   "El core del experimento no es modificado.")

    # ── Carga modelos ─────────────────────────────────────────────
    with st.spinner("Cargando modelos (primera vez puede tardar ~15s)..."):
        decoder, agents, vectors_cache, g_min, g_max, nlp, ref_imgs = load_models()

    # ── Tabs ──────────────────────────────────────────────────────
    tab_routing, tab_mdir, tab_madura, tab_info = st.tabs([
        "Routing en vivo",
        "Evolución M_dir",
        "Fase Madura",
        "Referencia ETH-80",
    ])

    # ═══════════════════════════════════════════════════════════════
    # TAB 1: Routing en vivo
    # ═══════════════════════════════════════════════════════════════
    with tab_routing:
        st.header("Routing de query en vivo")
        st.caption(
            "Escribe una query en lenguaje natural. "
            "El sistema la tokeniza, consulta M_dom de cada agente "
            "y muestra cómo el TME decide a quién enviarla."
        )

        col_input, col_examples = st.columns([3, 1])
        with col_input:
            query = st.text_input(
                "Query:",
                placeholder="Ej: a round red fruit  /  animal with a mane  /  fast vehicle",
                label_visibility="collapsed",
            )
        with col_examples:
            example = st.selectbox(
                "Ejemplos rápidos",
                ["", "a round red fruit", "animal with a mane",
                 "fast vehicle with wheels", "has an engine",
                 "large powerful mammal", "made into pie",
                 "equine with saddle", "passenger seats inside"],
                label_visibility="collapsed",
            )
            if example:
                query = example

        process = st.button("Procesar query", type="primary",
                             width='stretch', disabled=not query)

        if process and query:
            result = route_query_early(
                query, agents, vectors_cache, g_min, g_max, decoder, nlp)

            if result is None:
                st.warning("No se encontraron tokens válidos en la query.")
            else:
                winner = result["winner"]
                wcolor = DOMAIN_COLOR[winner]

                # ── Actualizar estado M_dir ────────────────────────
                winner_idx = result["winner_idx"]
                n_tokens   = len(result["tokens"])
                st.session_state.mdir_counts[winner_idx] += n_tokens
                st.session_state.query_n += 1
                st.session_state.history.append(result)

                # ── Banner del ganador ─────────────────────────────
                st.markdown(
                    f"""<div style='background:{wcolor}22; border-left:6px solid {wcolor};
                    padding:16px; border-radius:8px; margin:12px 0'>
                    <span style='font-size:28px'>{DOMAIN_EMOJI[winner]}</span>
                    <span style='font-size:20px; font-weight:bold; color:{wcolor}'>
                     → Agente <b>{winner.upper()}</b></span>
                    <span style='color:#555; margin-left:16px'>
                    score={result["avg_scores"][winner]:.2f}</span>
                    </div>""",
                    unsafe_allow_html=True,
                )

                # ── Tokens ────────────────────────────────────────
                tok_badges = "  ".join(
                    f"`{t}`" for t in result["tokens"])
                st.markdown(f"**Tokens spaCy:** {tok_badges}")

                # ── Fila principal: grafo + tabla scores + imagen ──
                col_graph, col_scores, col_img = st.columns([2, 1.5, 1])

                with col_graph:
                    fig_graph = make_routing_graph(
                        result["avg_scores"], winner,
                        title=f'"{query}"')
                    st.plotly_chart(fig_graph, width='stretch')

                with col_scores:
                    st.markdown("**Scores de M_dom por agente:**")
                    max_s = max(result["avg_scores"].values())
                    for cls in CLASSES:
                        s = result["avg_scores"][cls]
                        pct = s / max(max_s, 1e-9)
                        color = DOMAIN_COLOR[cls]
                        bold  = "**" if cls == winner else ""
                        st.markdown(
                            f"{DOMAIN_EMOJI[cls]} {bold}{cls}{bold}",
                            unsafe_allow_html=False,
                        )
                        st.progress(float(pct),
                                    text=f"{s:.3f}")

                with col_img:
                    st.markdown(f"**Imagen recuperada ({winner}):**")
                    if result["recalled_img"] is not None:
                        st.image(tensor_to_pil(result["recalled_img"]),
                                 width='stretch',
                                 caption=f"Prototipo {winner}")
                    else:
                        st.info("No reconocido")
                    st.image(
                        tensor_to_pil(
                            ref_imgs[winner].permute(1,2,0).numpy()),
                        width='stretch',
                        caption=f"ETH-80 ref")

                # ── Detalle por token ──────────────────────────────
                with st.expander("Ver scores por token (detalle)"):
                    if len(result["tokens"]) > 0:
                        fig_tok = make_token_score_table(
                            result["per_token_scores"])
                        st.plotly_chart(fig_tok, width='stretch')

                # ── Historial de queries ───────────────────────────
                if len(st.session_state.history) > 1:
                    with st.expander(
                            f"Historial de sesión ({len(st.session_state.history)} queries)"):
                        rows = []
                        for r in reversed(st.session_state.history):
                            rows.append({
                                "Query": r["query"],
                                "Tokens": " | ".join(r["tokens"]),
                                "Ganador": f"{DOMAIN_EMOJI[r['winner']]} {r['winner']}",
                                "Score": f"{r['avg_scores'][r['winner']]:.3f}",
                            })
                        import pandas as pd
                        st.dataframe(pd.DataFrame(rows), width='stretch')

    # ═══════════════════════════════════════════════════════════════
    # TAB 2: Evolución M_dir
    # ═══════════════════════════════════════════════════════════════
    with tab_mdir:
        st.header("Evolución de M_dir — acumulación de sesgo")
        st.caption(
            "Cada vez que procesas una query en 'Routing en vivo', "
            "el agente ganador acumula registros en M_dir. "
            "Aquí ves cómo se desarrolla el sesgo query a query."
        )

        qn = st.session_state.query_n
        counts = st.session_state.mdir_counts

        if qn == 0:
            st.info("Procesa al menos una query en la tab 'Routing en vivo' para ver la evolución.")
        else:
            # Barras actuales
            fig_bar = make_mdir_bar(counts, qn)
            st.plotly_chart(fig_bar, width='stretch')

            # Diagnóstico
            total = counts.sum()
            max_c = counts.max()
            min_c = counts.min()

            col_d1, col_d2, col_d3 = st.columns(3)
            with col_d1:
                dominant = CLASSES[int(counts.argmax())]
                st.metric("Agente dominante",
                          f"{DOMAIN_EMOJI[dominant]} {dominant}",
                          f"{counts.max()}/{total} registros")
            with col_d2:
                ratio = max_c / max(min_c, 1)
                st.metric("Ratio máx/mín", f"{ratio:.1f}x",
                          delta="sesgo alto" if ratio > 2 else "balanceado",
                          delta_color="inverse" if ratio > 2 else "normal")
            with col_d3:
                if total > 0:
                    p = counts / total
                    h = -np.sum(p * np.log2(np.where(p == 0, 1, p)))
                    st.metric("Entropía M_dir", f"{h:.3f} bits",
                              f"máx={np.log2(3):.3f}")

            # Evolución línea a línea
            if len(st.session_state.history) > 1:
                st.subheader("Evolución query a query")

                # Reconstruir evolución
                running = np.zeros(3, dtype=np.int64)
                evo = {"apple": [], "horse": [], "car": [], "q": []}
                for i, r in enumerate(st.session_state.history):
                    running[r["winner_idx"]] += len(r["tokens"])
                    for j, cls in enumerate(CLASSES):
                        evo[cls].append(int(running[j]))
                    evo["q"].append(i + 1)

                fig_evo = go.Figure()
                for cls in CLASSES:
                    fig_evo.add_trace(go.Scatter(
                        x=evo["q"], y=evo[cls],
                        name=f"{DOMAIN_EMOJI[cls]} {cls}",
                        line=dict(color=DOMAIN_COLOR[cls], width=2.5),
                        mode="lines+markers",
                    ))
                fig_evo.update_layout(
                    title=dict(text="Registros acumulados en M_dir por query",
                               x=0.5, font=dict(size=13)),
                    xaxis_title="Nº query",
                    yaxis_title="Registros acumulados",
                    height=300,
                    legend=dict(orientation="h", y=1.1),
                    plot_bgcolor="white",
                    paper_bgcolor="#f8f9fa",
                    margin=dict(l=20, r=20, t=60, b=20),
                )
                st.plotly_chart(fig_evo, width='stretch')

            # Consejo
            dominant = CLASSES[int(counts.argmax())]
            ratio = max_c / max(min_c, 1)
            if ratio > 2 and qn >= 5:
                st.warning(
                    f"**Sesgo detectado:** {DOMAIN_EMOJI[dominant]} {dominant} "
                    f"domina M_dir con ratio {ratio:.1f}x. "
                    f"En fase madura, la mayoría de queries serán redirigidas a {dominant}."
                )
            elif qn >= 3:
                st.success("M_dir relativamente balanceada.")

    # ═══════════════════════════════════════════════════════════════
    # TAB 3: Fase Madura
    # ═══════════════════════════════════════════════════════════════
    with tab_madura:
        st.header("Fase Madura — routing por M_dir")
        st.caption(
            "En la fase madura, el TME usa M_dir (lo que aprendió en la fase temprana) "
            "en lugar de M_dom. El agente de entrada es aleatorio; "
            "la query 'salta' al agente que M_dir indica."
        )

        qn = st.session_state.query_n
        if qn < 3:
            st.info(
                "Procesa al menos 3 queries en 'Routing en vivo' primero "
                "para que M_dir tenga algo aprendido.")
        else:
            query_m = st.text_input(
                "Query para fase madura:",
                placeholder="Ej: animal with a mane",
                key="query_madura",
            )

            col_entry, col_btn = st.columns([2, 1])
            with col_entry:
                entry_cls = st.selectbox(
                    "Agente de entrada (aleatorio en el sistema real):",
                    CLASSES,
                    format_func=lambda c: f"{DOMAIN_EMOJI[c]} {c}",
                )
            with col_btn:
                run_mature = st.button("Ejecutar fase madura",
                                       type="primary",
                                       width='stretch',
                                       disabled=not query_m)

            if run_mature and query_m:
                res_m = route_query_mature(
                    query_m,
                    agents, vectors_cache, g_min, g_max, decoder, nlp,
                    entry_cls=entry_cls,
                )
                if res_m is None:
                    st.warning("No se encontraron tokens.")
                else:
                    dest = res_m["dest_cls"]
                    same = entry_cls == dest
                    redirected = not same

                    # ── Visualización del salto ────────────────────
                    if redirected:
                        st.markdown(
                            f"""<div style='background:#f39c1222; border-left:6px solid #f39c12;
                            padding:14px; border-radius:8px; margin:10px 0'>
                            <b>Redirección detectada</b><br>
                            <span style='font-size:18px'>
                            {DOMAIN_EMOJI[entry_cls]} {entry_cls}
                            &nbsp;→&nbsp;
                            <span style='color:{DOMAIN_COLOR[dest]}; font-weight:bold'>
                            {DOMAIN_EMOJI[dest]} {dest.upper()}
                            </span></span>
                            </div>""",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""<div style='background:#2ecc7122; border-left:6px solid #2ecc71;
                            padding:14px; border-radius:8px; margin:10px 0'>
                            <b>Sin redirección:</b> agente de entrada = destino
                            &nbsp; {DOMAIN_EMOJI[entry_cls]} {entry_cls}
                            </div>""",
                            unsafe_allow_html=True,
                        )

                    col_mg, col_ms, col_mi = st.columns([2, 1.5, 1])

                    with col_mg:
                        # Grafo con la flecha del salto
                        fig_m = make_routing_graph(
                            res_m["mdir_scores"], dest,
                            title=f'Fase madura: "{query_m}"',
                            highlight_path=(entry_cls, dest) if redirected else None,
                        )
                        st.plotly_chart(fig_m, width='stretch')
                        st.caption(
                            "La flecha naranja indica el salto del agente de entrada "
                            "al agente destino según M_dir."
                            if redirected else
                            "El agente de entrada y destino son el mismo."
                        )

                    with col_ms:
                        st.markdown("**Distribución M_dir actual:**")
                        total_m = sum(res_m["mdir_scores"].values())
                        for cls in CLASSES:
                            s = res_m["mdir_scores"][cls]
                            pct = s / max(total_m, 1)
                            st.markdown(f"{DOMAIN_EMOJI[cls]} {cls}")
                            st.progress(float(pct),
                                        text=f"{int(s)} reg. ({pct:.0%})")

                    with col_mi:
                        st.markdown(f"**Imagen ({dest}):**")
                        if res_m["recalled_img"] is not None:
                            st.image(tensor_to_pil(res_m["recalled_img"]),
                                     width='stretch')
                        else:
                            st.info("Sin recall")

                    # ── Comparar con fase temprana ─────────────────
                    with st.expander("Comparar con fase temprana"):
                        early = route_query_early(
                            query_m, agents, vectors_cache, g_min, g_max, decoder, nlp)
                        if early:
                            e_winner = early["winner"]
                            match = e_winner == dest
                            st.metric(
                                "Fase temprana (M_dom)",
                                f"{DOMAIN_EMOJI[e_winner]} {e_winner}",
                            )
                            st.metric(
                                "Fase madura (M_dir)",
                                f"{DOMAIN_EMOJI[dest]} {dest}",
                            )
                            if match:
                                st.success("Fidelidad OK: fase madura coincide con fase temprana.")
                            else:
                                st.error(
                                    f"Fidelidad FALLA: early={e_winner}, mature={dest}. "
                                    "M_dir está sesgado hacia otro agente.")

    # ═══════════════════════════════════════════════════════════════
    # TAB 4: Referencia ETH-80
    # ═══════════════════════════════════════════════════════════════
    with tab_info:
        st.header("Imágenes de referencia — ETH-80")
        st.caption("Una muestra real por dominio del dataset de entrenamiento.")

        cols = st.columns(3)
        for col, cls in zip(cols, CLASSES):
            with col:
                st.subheader(f"{DOMAIN_EMOJI[cls]} {cls}")
                img_np = ref_imgs[cls].permute(1, 2, 0).numpy()
                st.image(tensor_to_pil(img_np),
                         caption=f"ETH-80 — {cls}",
                         width='stretch')

        st.divider()
        st.subheader("Labels ConceptNet por dominio")
        col_a, col_h, col_c = st.columns(3)
        for col, cls in zip([col_a, col_h, col_c], CLASSES):
            with col:
                labels_path = ROOT / f"labels_{cls}.json"
                labels = json.loads(labels_path.read_text())
                st.markdown(f"**{DOMAIN_EMOJI[cls]} {cls}** ({len(labels)} labels)")
                for word, freq in sorted(labels.items(),
                                         key=lambda x: -x[1])[:15]:
                    st.markdown(f"- `{word}` (freq={freq})")


if __name__ == "__main__":
    main()
