"""Hilo de escucha continua: sounddevice en streaming (16 kHz, bloques
de 30 ms) + VAD por energía con piso de ruido adaptativo.

Mientras hay habla, emite transcripciones PARCIALES (~1.2 s, beam 1)
para el subtítulo vivo; al detectar ~0.6 s de silencio cierra el
segmento, lo transcribe en FINAL (beam 5) y lo pone en phrase_queue
para que main lo rutee. Estado compartido en `state` (dict + lock del
GIL: escrituras atómicas de claves).
"""
import queue
import threading
import time

import numpy as np

SR = 16000
BLOCK = 480                # 30 ms
PREROLL_S = 0.3            # audio previo al arranque de voz
START_BLOCKS = 3           # bloques seguidos sobre umbral para arrancar
END_SILENCE_S = 0.6        # silencio que cierra la frase
PARTIAL_EVERY_S = 1.2      # cadencia de subtítulo parcial
MAX_SEGMENT_S = 15.0       # tope de frase
MIN_SEGMENT_S = 0.35       # descartar chasquidos


class AudioWorker(threading.Thread):
    def __init__(self, whisper_model, phrase_queue: queue.Queue,
                 state: dict, log=print):
        super().__init__(daemon=True)
        self.model = whisper_model
        self.phrases = phrase_queue
        self.state = state
        self.log = log
        self.blocks = queue.Queue()
        self.noise_floor = 0.003   # EMA del RMS en silencio
        state.setdefault("partial", "")
        state.setdefault("rms", 0.0)
        state.setdefault("mic_muted", False)
        state.setdefault("listening", False)

    def _callback(self, indata, frames, t, status):
        self.blocks.put(indata[:, 0].copy())

    def run(self):
        import sounddevice as sd
        try:
            stream = sd.InputStream(samplerate=SR, channels=1,
                                    dtype="float32", blocksize=BLOCK,
                                    callback=self._callback)
            stream.start()
        except Exception as e:
            self.state["mic_error"] = (
                f"Could not open microphone ({type(e).__name__}). "
                f"Check Windows -> Privacy -> Microphone (desktop "
                f"apps).")
            self.log("[audio] " + self.state["mic_error"])
            return
        self.log(f"[audio] listening ({sd.query_devices(kind='input')['name']})")

        preroll = []
        segment = []            # bloques de la frase en curso
        speaking = False
        above = 0
        silent_blocks = 0
        last_partial_t = 0.0

        while not self.state.get("stop"):
            try:
                b = self.blocks.get(timeout=0.5)
            except queue.Empty:
                continue
            rms = float(np.sqrt((b ** 2).mean()))
            self.state["rms"] = rms
            if self.state["mic_muted"]:
                speaking, segment, above = False, [], 0
                self.state["partial"] = ""
                self.state["listening"] = False
                continue

            thr = max(0.006, self.noise_floor * 4.0)
            if not speaking:
                # piso de ruido solo se adapta en silencio
                self.noise_floor = 0.95 * self.noise_floor + 0.05 * rms
                preroll.append(b)
                if len(preroll) > int(PREROLL_S * SR / BLOCK):
                    preroll.pop(0)
                above = above + 1 if rms > thr else 0
                if above >= START_BLOCKS:
                    speaking = True
                    segment = list(preroll)
                    silent_blocks = 0
                    last_partial_t = time.time()
                    self.state["listening"] = True
            else:
                segment.append(b)
                silent_blocks = silent_blocks + 1 if rms < thr else 0
                seg_s = len(segment) * BLOCK / SR
                ended = (silent_blocks >= int(END_SILENCE_S * SR / BLOCK)
                         or seg_s >= MAX_SEGMENT_S)
                if ended:
                    speaking, above = False, 0
                    self.state["listening"] = False
                    self.state["partial"] = ""
                    voiced_s = seg_s - silent_blocks * BLOCK / SR
                    if voiced_s >= MIN_SEGMENT_S:
                        audio = np.concatenate(segment)
                        t0 = time.time()
                        from stt import transcribe
                        text = transcribe(self.model, audio, final=True)
                        ms = (time.time() - t0) * 1000
                        if text:
                            self.phrases.put(
                                {"text": text, "stt_ms": ms,
                                 "audio_s": seg_s})
                    segment = []
                elif time.time() - last_partial_t >= PARTIAL_EVERY_S:
                    last_partial_t = time.time()
                    from stt import transcribe
                    audio = np.concatenate(segment)
                    self.state["partial"] = transcribe(
                        self.model, audio, final=False)

    # Para el selftest: inyectar un WAV como si viniera del micrófono.
    def feed_wav(self, audio_16k: np.ndarray):
        for i in range(0, len(audio_16k) - BLOCK, BLOCK):
            self.blocks.put(audio_16k[i:i + BLOCK].astype(np.float32))
        self.blocks.put(np.zeros(BLOCK, dtype=np.float32))
        for _ in range(int((END_SILENCE_S + 0.3) * SR / BLOCK)):
            self.blocks.put(np.zeros(BLOCK, dtype=np.float32))

    def run_injected(self):
        """Variante del selftest: procesa solo lo inyectado con feed_wav
        (sin abrir micrófono). Reusa la máquina de estados de run()."""
        self._orig_stream = None
        # misma lógica que run() pero sin InputStream:
        preroll, segment = [], []
        speaking, above, silent_blocks = False, 0, 0
        last_partial_t = 0.0
        while not self.state.get("stop"):
            try:
                b = self.blocks.get(timeout=1.0)
            except queue.Empty:
                break
            rms = float(np.sqrt((b ** 2).mean()))
            self.state["rms"] = rms
            thr = max(0.006, self.noise_floor * 4.0)
            if not speaking:
                self.noise_floor = 0.95 * self.noise_floor + 0.05 * rms
                preroll.append(b)
                if len(preroll) > int(PREROLL_S * SR / BLOCK):
                    preroll.pop(0)
                above = above + 1 if rms > thr else 0
                if above >= START_BLOCKS:
                    speaking, segment = True, list(preroll)
                    silent_blocks, last_partial_t = 0, time.time()
            else:
                segment.append(b)
                silent_blocks = silent_blocks + 1 if rms < thr else 0
                seg_s = len(segment) * BLOCK / SR
                if (silent_blocks >= int(END_SILENCE_S * SR / BLOCK)
                        or seg_s >= MAX_SEGMENT_S):
                    speaking = False
                    audio = np.concatenate(segment)
                    from stt import transcribe
                    t0 = time.time()
                    text = transcribe(self.model, audio, final=True)
                    if text:
                        self.phrases.put(
                            {"text": text,
                             "stt_ms": (time.time() - t0) * 1000,
                             "audio_s": seg_s})
                    segment = []
