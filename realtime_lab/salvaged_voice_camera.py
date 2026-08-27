"""Código de voz, cámara y modo en vivo sacado de app_tme.py para el
experimento aislado en tiempo real. Funcionó en la app:
- load_whisper: GPU vía preload ctypes de DLLs nvidia-pip + fallback CPU
- transcribe_query: task=translate (es/en -> en) + reintento sin VAD
- wav_stats/_amplify_wav: detección de silencio + rescate de ganancia
- _MIC_TEST_HTML: probador getUserMedia con medidor en vivo
- voice_query_ui / process_voice_recording: UI Streamlit de dictado
- _score_bars_html / render_live_pipeline: show escénico del pipeline
- bloque del tab "0 · En vivo" (al final, comentado como referencia)
No importable tal cual (depende de st/CLASSES/etc. de app_tme): es cantera.
"""

# %% ==== Bloque A: motor de voz + UI de dictado ====
@st.cache_resource(show_spinner=False)
def load_whisper():
    """
    Speech-to-text local (faster-whisper `small`). Es solo el «oído» de la
    interfaz — convierte voz en texto y ese texto entra al pipeline por el
    mismo camino que el teclado; no toca la maquinaria de memorias.
    Intenta GPU y cae a CPU int8 si CUDA no está utilizable.
    """
    import ctypes
    import site
    from faster_whisper import WhisperModel

    # ctranslate2 busca cuBLAS/cuDNN por nombre con LoadLibrary y no ve los
    # directorios de os.add_dll_directory; precargarlos con ctypes hace que
    # ya estén en el proceso. Los DLLs vienen de los paquetes pip
    # nvidia-cublas-cu12 / nvidia-cudnn-cu12 (ausentes ⇒ se cae a CPU).
    for sp in site.getsitepackages():
        for dll in sorted((Path(sp) / "nvidia").glob("*/bin/*.dll")):
            try:
                ctypes.WinDLL(str(dll))
            except OSError:
                pass
    try:
        model = WhisperModel("small", device="cuda", compute_type="float16")
        # La construcción no valida los DLLs: forzar una inferencia mínima
        # (1 s de silencio) para detectar aquí un CUDA roto y no a mitad
        # de una consulta del usuario.
        list(model.transcribe(np.zeros(16000, dtype=np.float32))[0])
        return model
    except Exception:
        return WhisperModel("small", device="cpu", compute_type="int8")


def wav_stats(wav_bytes: bytes) -> tuple:
    """(duración s, pico [0,1]) del WAV PCM del navegador — para distinguir
    una grabación en silencio (permiso/dispositivo de micrófono) de una
    que Whisper no entendió."""
    import wave
    with wave.open(BytesIO(wav_bytes)) as w:
        n, sr = w.getnframes(), w.getframerate()
        raw = w.readframes(n)
    if not raw or sr == 0:
        return 0.0, 0.0
    x = np.frombuffer(raw, dtype=np.int16)
    return n / float(sr), float(np.abs(x).max()) / 32768.0


def transcribe_query(wav_bytes: bytes) -> tuple:
    """WAV del navegador → (texto en inglés, idioma detectado).

    task="translate" hace que Whisper emita SIEMPRE inglés (para audio en
    inglés equivale a transcribir), que es el idioma del vocabulario
    fastText de los agentes — así se puede dictar en español o inglés.
    Si el VAD descarta todo (voz suave/lejos del micrófono), reintenta
    sin filtro antes de rendirse.
    """
    model = load_whisper()
    segments, info = model.transcribe(
        BytesIO(wav_bytes), task="translate", beam_size=5, vad_filter=True)
    text = " ".join(s.text.strip() for s in segments).strip()
    if not text:
        segments, info = model.transcribe(
            BytesIO(wav_bytes), task="translate", beam_size=5,
            vad_filter=False)
        text = " ".join(s.text.strip() for s in segments).strip()
    return text.rstrip(".!?"), info.language


def _amplify_wav(wav_bytes: bytes, peak: float, target: float = 0.9) -> bytes:
    """Re-empaqueta el WAV PCM16 escalado para que el pico llegue a
    `target` — rescata micrófonos con ganancia muy baja sin tocar el
    sample rate (Whisper es robusto, pero no con señal casi inaudible)."""
    import wave
    with wave.open(BytesIO(wav_bytes)) as w:
        params = w.getparams()
        raw = w.readframes(w.getnframes())
    if params.sampwidth != 2 or peak <= 0:
        return wav_bytes
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
    x *= (target * 32767.0) / (peak * 32768.0)
    out = BytesIO()
    with wave.open(out, "wb") as w:
        w.setparams(params)
        w.writeframes(np.clip(x, -32768, 32767).astype(np.int16).tobytes())
    return out.getvalue()


# Probador de micrófono en vivo: corre DENTRO del navegador (getUserMedia),
# así diagnostica exactamente lo que la grabadora de Streamlit va a ver —
# dispositivo activo, sample rate y nivel en tiempo real.
_MIC_TEST_HTML = """
<div style="font-family:system-ui,sans-serif;font-size:13px;color:#1c1e33">
  <div id="out">Pidiendo acceso al micrófono…</div>
  <div style="margin-top:8px;background:#eef0f8;border:1px solid #d9dcea;
              border-radius:6px;height:18px;overflow:hidden">
    <div id="bar" style="height:100%;width:0%;background:#178f4a"></div>
  </div>
  <div id="lvl" style="color:#5a5e7d;margin-top:4px">nivel: —</div>
</div>
<script>
(async () => {
  const out = document.getElementById('out');
  const bar = document.getElementById('bar');
  const lvl = document.getElementById('lvl');
  try {
    const stream = await navigator.mediaDevices.getUserMedia({audio: true});
    const track = stream.getAudioTracks()[0];
    const devs = await navigator.mediaDevices.enumerateDevices();
    const mics = devs.filter(d => d.kind === 'audioinput' && d.label);
    const ctx = new AudioContext();
    const an = ctx.createAnalyser(); an.fftSize = 2048;
    ctx.createMediaStreamSource(stream).connect(an);
    out.innerHTML = '<b>Dispositivo activo:</b> ' + track.label +
      ' · ' + ctx.sampleRate + ' Hz<br><b>Micrófonos visibles:</b> ' +
      (mics.map(m => m.label).join(' · ') || '(sin etiquetas)') +
      '<br>Habla ahora — la barra debe moverse y ponerse verde:';
    const buf = new Float32Array(an.fftSize);
    setInterval(() => {
      an.getFloatTimeDomainData(buf);
      let p = 0;
      for (const v of buf) p = Math.max(p, Math.abs(v));
      bar.style.width = Math.min(100, p * 300) + '%';
      bar.style.background = p > 0.02 ? '#178f4a' : '#c05f0e';
      lvl.textContent = 'nivel pico instantáneo: ' + p.toFixed(4) +
        (p < 0.002 ? '  — SILENCIO: Windows o el dispositivo no entregan señal'
                   : '');
    }, 120);
  } catch (e) {
    out.innerHTML = '<b style="color:#b3271e">getUserMedia falló: ' + e.name +
      '</b><br>' + (e.name === 'NotAllowedError'
        ? 'Permiso denegado — revisa el candado del sitio Y en Windows: ' +
          'Configuración → Privacidad y seguridad → Micrófono → activa el ' +
          'acceso general y el de aplicaciones de escritorio.'
        : e.name === 'NotFoundError'
        ? 'Chrome no ve ningún micrófono — revisa que esté conectado y ' +
          'habilitado en el Administrador de dispositivos.'
        : String(e.message));
  }
})();
</script>
"""


def process_voice_recording(wav_bytes: bytes) -> tuple:
    """Grabación → (texto, idioma, dur, pico, err).

    err: None si hay texto; "silence" si la señal nunca llegó (regrabar,
    re-transcribir no ayuda); "nowords" si hubo audio sin palabras.
    Aplica el rescate de ganancia baja antes de Whisper.
    """
    dur, peak = wav_stats(wav_bytes)
    if peak < 0.0015:
        return None, None, dur, peak, "silence"
    if peak < 0.2:
        wav_bytes = _amplify_wav(wav_bytes, peak)
    text, lang = transcribe_query(wav_bytes)
    if not text:
        return None, lang, dur, peak, "nowords"
    return text, lang, dur, peak, None


_MSG_SILENCE = (
    "La grabación llegó **en silencio** ({dur:.1f} s, pico {peak:.4f}) — "
    "el permiso del sitio no basta si la señal no llega. Activa el "
    "**probador de micrófono** y revisa, en este orden: ① que la barra se "
    "mueva al hablar; ② Windows → Configuración → Privacidad y seguridad → "
    "Micrófono (acceso general **y** para apps de escritorio); ③ que "
    "Chrome use el micrófono correcto (🔒 junto a la URL → Micrófono → "
    "dispositivo). Cuando la barra se mueva, **graba de nuevo**.")
_MSG_NOWORDS = (
    "Hubo audio ({dur:.1f} s, pico {peak:.2f}) pero Whisper no reconoció "
    "palabras — habla más cerca del micrófono y graba de nuevo.")


def voice_query_ui(target_key: str, rec_key: str):
    """Expander de dictado que escribe la transcripción en
    st.session_state[target_key].

    Debe llamarse ANTES de instanciar el text_input con esa key (Streamlit
    prohíbe modificar el estado de un widget ya instanciado en el mismo
    run). El botón «Reintentar» olvida el hash de la última grabación para
    volver a transcribirla sin regrabar.
    """
    import hashlib
    hkey, lkey = f"voice_hash_{rec_key}", f"voice_lang_{rec_key}"
    with st.expander("🎤 Dictar la consulta por voz"):
        st.caption(
            "Graba una frase corta en **español o inglés**: Whisper la "
            "convierte a texto en inglés (el idioma del vocabulario "
            "fastText) y entra al pipeline igual que si la escribieras.")
        rec = st.audio_input("Grabar consulta", key=rec_key,
                             label_visibility="collapsed")
        if st.checkbox("🎙️ Probar micrófono (medidor en vivo)",
                       key=f"{rec_key}_mictest",
                       help="Muestra qué dispositivo usa el navegador y su "
                            "nivel en tiempo real, sin grabar nada."):
            components.html(_MIC_TEST_HTML, height=170)
        if rec is None:
            return
        if st.button("🔁 Re-transcribir esta grabación",
                     key=f"{rec_key}_retry",
                     help="Vuelve a pasar la MISMA grabación por Whisper. "
                          "Si la grabación llegó en silencio, esto no la "
                          "arregla: usa el probador y graba de nuevo."):
            st.session_state.pop(hkey, None)
        h = hashlib.md5(rec.getvalue()).hexdigest()
        if st.session_state.get(hkey) != h:
            with st.spinner("Transcribiendo… (la primera vez descarga "
                            "el modelo Whisper, ~460 MB)"):
                text, lang, dur, peak, err = process_voice_recording(
                    rec.getvalue())
            st.session_state[hkey] = h
            st.session_state[lkey] = lang if not err else None
            st.session_state[f"voice_stats_{rec_key}"] = (dur, peak)
            if err == "silence":
                st.error(_MSG_SILENCE.format(dur=dur, peak=peak))
            elif err == "nowords":
                st.warning(_MSG_NOWORDS.format(dur=dur, peak=peak))
            else:
                st.session_state[target_key] = text
        if st.session_state.get(lkey):
            _d, _p = st.session_state.get(f"voice_stats_{rec_key}", (0, 0))
            st.caption(
                f"Idioma detectado: **{st.session_state[lkey]}** · "
                f"audio {_d:.1f} s · pico {_p:.2f} → "
                f"consulta: “{st.session_state.get(target_key, '')}”")




# %% ==== Bloque B: show escénico del pipeline ====
def _score_bars_html(scores, frac, winner=None, reveal_winner=False):
    """Barras de score por agente para el modo en vivo. `frac` ∈ (0,1]
    anima el llenado; con reveal_winner los no-ganadores se atenúan."""
    mx = max(scores.values()) or 1e-9
    rows = []
    for cls in CLASSES:
        s = scores[cls]
        w = (s / mx) * 100.0 * frac
        dim = reveal_winner and cls != winner
        star = " 👑" if (reveal_winner and cls == winner) else ""
        rows.append(
            f"<div style='display:flex;align-items:center;gap:8px;"
            f"margin:3px 0;opacity:{0.35 if dim else 1}'>"
            f"<div style='width:110px;font-size:13px'>"
            f"{DOMAIN_EMOJI[cls]} {cls}{star}</div>"
            f"<div style='flex:1;background:#eef0f8;border-radius:6px;"
            f"height:14px;overflow:hidden'>"
            f"<div style='width:{w:.1f}%;background:{DOMAIN_COLOR[cls]};"
            f"height:100%;border-radius:6px'></div></div>"
            f"<div style='width:96px;font-family:monospace;font-size:12px;"
            f"text-align:right'>{s * frac:,.2f}</div></div>")
    return "<div>" + "".join(rows) + "</div>"


def render_live_pipeline(trace, ref_imgs, from_voice=False):
    """Reproducción escénica del pipeline: los MISMOS números del trace
    real (compute_pipeline_trace), revelados por etapas con pausas — la
    consulta se teclea, spaCy descompone token a token, la pista se pinta,
    el broadcast enciende agentes en secuencia, los scores compiten y el
    ganador evoca su memoria. Cero cómputo simulado: solo dramaturgia."""
    import time

    def beat(s=0.5):
        time.sleep(s)

    # 1 · spaCy, token a token
    _stage_header(1, "", "spaCy descompone la oración",
                  "tokenise → lemma → filtro de stopwords/POS")
    ph_tok = st.empty()
    reps = set(trace["tokens_representable"])
    unrep = set(trace["tokens_unrepresentable"])
    chips = ""
    for t in trace["spacy_tokens"]:
        c = ("#178f4a" if t["lemma"] in reps
             else "#c05f0e" if t["lemma"] in unrep else "#767d94")
        chips += (
            f"<span style='background:{c};color:white;padding:4px 10px;"
            f"border-radius:14px;margin:3px;display:inline-block;"
            f"font-size:14px'>{t['text']}"
            f"<span style='font-size:9px;opacity:.8'> [{t['pos']}]"
            f"{'✗' if t['is_stop'] else ''}</span></span> ")
        ph_tok.markdown(f"<div style='line-height:2.6'>{chips}</div>",
                        unsafe_allow_html=True)
        beat(0.28)
    st.caption("verde = entra como pista · naranja = sin vector fastText · "
               "gris = descartado (stopword/POS)")

    # 2 · La pista se cuantiza y se pinta
    tok0 = next(iter(trace["per_token"]))
    q_vec = trace["per_token"][tok0]["q_vec"].astype(float)
    _stage_header(2, "", f"fastText serializa «{tok0}»",
                  f"300D float → v_q ∈ [0,{M_LABEL - 1}]^{N} (cuantización "
                  f"por magnitud)")
    ph_hm = st.empty()
    for frac in (0.25, 0.5, 0.75, 1.0):
        v = q_vec.copy()
        v[int(len(v) * frac):] = np.nan
        ph_hm.plotly_chart(
            _vec_heatmap(v, title=f"v_q[{tok0}] — {int(frac * 100)}%",
                         colorscale="Viridis"),
            use_container_width=True)
        beat(0.22)

    # 3 · Broadcast: los agentes se encienden en secuencia
    _stage_header(3, "", "El TME difunde v_q a los 8 especialistas",
                  "simultáneo en el sistema real; aquí en cámara lenta")
    ph_bc = st.empty()
    for k in range(len(CLASSES) + 1):
        cells = ""
        for i, cls in enumerate(CLASSES):
            on = i < k
            cells += (
                f"<div style='flex:1;text-align:center;border:2px solid "
                f"{DOMAIN_COLOR[cls] if on else '#d9dcea'};border-radius:10px;"
                f"padding:7px 2px;opacity:{1 if on else 0.45};"
                f"background:#ffffff'>"
                f"<div style='font-size:17px'>{DOMAIN_EMOJI[cls]}</div>"
                f"<div style='font-size:11px'>{cls}</div>"
                f"<div style='font-size:10px;color:#5a5e7d'>"
                f"{'v_q 📶' if on else '…'}</div></div>")
        ph_bc.markdown(f"<div style='display:flex;gap:6px'>{cells}</div>",
                       unsafe_allow_html=True)
        beat(0.13)

    # 4 · Los scores compiten
    _stage_header(4, "", "Cada agente opina desde sus memorias",
                  "M_dom_L.recog_weights(v_q) → M_dom_H score "
                  f"({'gate de containment' if trace['normalized'] else 'crudo'})")
    ph_sc = st.empty()
    frames = 10
    for f in range(1, frames + 1):
        ph_sc.markdown(_score_bars_html(trace["avg_scores"], f / frames),
                       unsafe_allow_html=True)
        beat(0.11)

    # 5 · Decisión (o rechazo honesto)
    if trace.get("rejected") or trace["winner"] is None:
        beat(0.4)
        st.error("🚫 **Rechazo de la EAM**: ningún agente contiene las "
                 "pistas (todos los scores en cero) — no se declara "
                 "ganador por desempate. Eso también es memoria honesta.")
        return
    winner = trace["winner"]
    beat(0.4)
    ph_sc.markdown(
        _score_bars_html(trace["avg_scores"], 1.0, winner=winner,
                         reveal_winner=True),
        unsafe_allow_html=True)
    wcolor = DOMAIN_COLOR[winner]
    _stage_header(5, "", "Decisión del grupo + directorio",
                  "argmax de los scores; M_dir aprende quién sabe qué")
    beat(0.35)
    st.markdown(
        f"<div style='background:{wcolor}22;border-left:6px solid {wcolor};"
        f"padding:14px;border-radius:8px'>"
        f"<span style='font-size:26px'>{DOMAIN_EMOJI[winner]}</span> "
        f"<b style='font-size:20px;color:{wcolor}'>→ {winner.upper()}</b> "
        f"<span style='color:#5a5e7d'>· M_dir registra "
        f"{trace['n_tokens']} token(s) a nombre de {winner}</span></div>",
        unsafe_allow_html=True)

    # 6 · El ganador evoca su memoria
    _stage_header(6, "", "El especialista evoca lo que recuerda",
                  "M_dom_H.recall_from_left → dequantización → decoder")
    beat(0.5)
    c1, c2, c3 = st.columns([1, 1, 2])
    img = trace.get("final_recalled_img")
    with c1:
        if img is not None:
            st.image(_t2img(img), width=170,
                     caption=f"Memoria reconstruida ({winner})")
        else:
            st.info("Reconoció la pista, pero sin reconstrucción que "
                    "mostrar.")
    with c2:
        try:
            ref_np = ref_imgs[winner].permute(1, 2, 0).numpy()
            st.image(_t2img(ref_np), width=170,
                     caption=f"ETH-80 {winner} (referencia)")
        except Exception:
            pass
    with c3:
        st.success(
            f"“{trace['query']}” → {DOMAIN_EMOJI[winner]} "
            f"**{winner.upper()}** — todos los valores mostrados son los "
            f"reales del pipeline; solo las pausas son teatro.")




# %% ==== Bloque C: tab '0 · En vivo' (era codigo de main) ====
#     # TAB 0: En vivo — dictas (o escribes) y VES el pipeline suceder
#     with tab_live:
#         st.header("🎬 En vivo — habla y mira el pipeline suceder")
#         st.caption(
#             "Dicta una consulta (o escríbela) y obsérvala pasar por el "
#             "sistema paso a paso: spaCy la descompone, fastText la vuelve "
#             "pista cuantizada, el TME la difunde, los 8 especialistas "
#             "compiten y el ganador evoca su memoria. Los números son los "
#             "reales del pipeline — solo el ritmo es escénico. La corrida "
#             "también se registra en el M_dir de sesión (pestañas 2 y 3).")
#         c_rec, c_txt = st.columns([1, 1.4])
#         with c_rec:
#             live_rec = st.audio_input("🎤 Graba tu consulta",
#                                       key="live_rec")
#         with c_txt:
#             live_txt = st.text_input(
#                 "…o escríbela:", key="live_query_txt",
#                 placeholder="e.g.: farm animal that gives milk")
#             live_go = st.button("▶ Ver en vivo", type="primary",
#                                 key="live_go",
#                                 disabled=not (live_txt or live_rec))

#         live_query, live_voiced = None, False
#         if live_rec is not None:
#             import hashlib
#             _lh = hashlib.md5(live_rec.getvalue()).hexdigest()
#             if st.session_state.get("live_hash") != _lh:
#                 st.session_state["live_hash"] = _lh
#                 with st.spinner("Transcribiendo…"):
#                     _t, _lang, _d, _p, _err = process_voice_recording(
#                         live_rec.getvalue())
#                 if _err == "silence":
#                     st.error(_MSG_SILENCE.format(dur=_d, peak=_p))
#                 elif _err == "nowords":
#                     st.warning(_MSG_NOWORDS.format(dur=_d, peak=_p))
#                 else:
#                     st.session_state["live_voice_text"] = _t
#                     # Una grabación NUEVA dispara el show sola — dictar ES
#                     # correr el pipeline, sin botón intermedio.
#                     live_query, live_voiced = _t, True
#         if live_go:
#             live_query = live_txt or st.session_state.get("live_voice_text")
#             live_voiced = not live_txt

#         if live_query:
#             # Feedback inmediato: la consulta se teclea sola ANTES del
#             # cómputo pesado (el recall estocástico tarda ~1 min en CPU).
#             import time as _time
#             _ph_q = st.empty()
#             _icon = "🎤" if live_voiced else "⌨️"
#             _words = live_query.split()
#             for _i in range(1, len(_words) + 1):
#                 _ph_q.markdown(
#                     f"<div class='dcard' style='font-size:21px;"
#                     f"font-style:italic;text-align:center;padding:14px'>"
#                     f"{_icon} “{' '.join(_words[:_i])}"
#                     f"<span style='color:#4653c9'>▌</span>”</div>",
#                     unsafe_allow_html=True)
#                 _time.sleep(0.16)
#             _ph_q.markdown(
#                 f"<div class='dcard' style='font-size:21px;"
#                 f"font-style:italic;text-align:center;padding:14px'>"
#                 f"{_icon} “{live_query}”</div>", unsafe_allow_html=True)
#             with st.spinner("Los 8 especialistas están consultando sus "
#                             "memorias (recall estocástico real, ~1 min en "
#                             "CPU)…"):
#                 trace_live = compute_pipeline_trace(
#                     live_query, agents, vectors_cache, g_min, g_max,
#                     decoder, nlp, normalize=norm_on)
#             if trace_live is None:
#                 st.warning("Ningún token es representable (sin vector "
#                            "fastText real) — no hay pista que entregar.")
#             else:
#                 render_live_pipeline(trace_live, ref_imgs,
#                                      from_voice=live_voiced)
#                 if not trace_live.get("rejected"):
#                     # Mismos efectos de sesión que el botón normal
#                     for td in trace_live["per_token"].values():
#                         st.session_state.mdir_mem.register(
#                             td["q_vec"], trace_live["winner_idx"])
#                     st.session_state.mdir_counts[
#                         trace_live["winner_idx"]] += trace_live["n_tokens"]
#                     st.session_state.query_n += 1
#                     st.session_state.last_trace = trace_live
#                     st.session_state.history.append({
#                         "query":      trace_live["query"],
#                         "tokens":     trace_live["tokens_representable"],
#                         "winner":     trace_live["winner"],
#                         "winner_idx": trace_live["winner_idx"],
#                         "avg_scores": trace_live["avg_scores"],
#                         "n_tokens":   trace_live["n_tokens"],
#                     })

