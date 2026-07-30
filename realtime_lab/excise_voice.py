"""Extirpa de app_tme.py los bloques de voz/en-vivo (por anclas de línea)
y los guarda en salvaged_voice_camera.py. Uso único, idempotente-no."""
from pathlib import Path

APP = Path(__file__).parent.parent / "app_tme.py"
OUT = Path(__file__).parent / "salvaged_voice_camera.py"

src = APP.read_text(encoding="utf-8")
lines = src.splitlines(keepends=True)


def find(pred, start=0):
    for i in range(start, len(lines)):
        if pred(lines[i]):
            return i
    raise SystemExit(f"ancla no encontrada desde {start}")


# Bloque A: load_whisper ... voice_query_ui (termina antes del decorador
# de load_experiment_state)
a0 = find(lambda l: l.startswith("@st.cache_resource(show_spinner=False)"))
a_end_def = find(lambda l: l.startswith("def load_experiment_state"))
a1 = a_end_def - 1  # su decorador @st.cache_resource
assert lines[a1].startswith("@st.cache_resource")

# Bloque B: _score_bars_html + render_live_pipeline
b0 = find(lambda l: l.startswith("def _score_bars_html("))
b1 = find(lambda l: l.startswith("def render_pipeline_trace("))

# Bloque C: tab En vivo (desde el comentario TAB 0 hasta antes de TAB 1)
c0 = find(lambda l: l.strip().startswith("# TAB 0: En vivo"))
c1 = find(lambda l: l.strip().startswith("# TAB 1: Pipeline Trace"))

assert a0 < a1 < b0 < b1 < c0 < c1

salvaged = (
    '"""Código de voz/cámara/en-vivo extirpado de app_tme.py (16 jul '
    '2026)\npara el experimento aislado en tiempo real. Todo VALIDADO '
    'en la app:\n- load_whisper: GPU vía preload ctypes de DLLs '
    'nvidia-pip + fallback CPU\n- transcribe_query: task=translate '
    '(es/en -> en) + reintento sin VAD\n- wav_stats/_amplify_wav: '
    'detección de silencio + rescate de ganancia\n- _MIC_TEST_HTML: '
    'probador getUserMedia con medidor en vivo\n- voice_query_ui / '
    'process_voice_recording: UI Streamlit de dictado\n- '
    '_score_bars_html / render_live_pipeline: show escénico del '
    'pipeline\n- bloque del tab "0 · En vivo" (al final, comentado '
    'como referencia)\nNo importable tal cual (depende de st/CLASSES/'
    'etc. de app_tme): es cantera.\n"""\n\n'
    + "# %% ==== Bloque A: motor de voz + UI de dictado ====\n"
    + "".join(lines[a0:a1])
    + "\n\n# %% ==== Bloque B: show escénico del pipeline ====\n"
    + "".join(lines[b0:b1])
    + "\n\n# %% ==== Bloque C: tab '0 · En vivo' (era codigo de main) "
      "====\n"
    + "".join("# " + l if l.strip() else l for l in lines[c0:c1])
)
OUT.write_text(salvaged, encoding="utf-8")

new = "".join(lines[:a0] + lines[a1:b0] + lines[b1:c0] + lines[c1:])
APP.write_text(new, encoding="utf-8")
print(f"extirpadas {(a1-a0) + (b1-b0) + (c1-c0)} lineas; "
      f"salvamento en {OUT.name}")
