"""Whisper para el lab (sin Streamlit). Misma receta validada en la app:
GPU vía preload ctypes de los DLLs nvidia-pip (os.add_dll_directory no
basta para ctranslate2) + validación con inferencia de silencio +
fallback a CPU int8. Medido: 0.6 s/frase corta en la RTX 2050."""
import ctypes
import site
import time
from pathlib import Path

import numpy as np


def load_whisper(log=print):
    from faster_whisper import WhisperModel
    for sp in site.getsitepackages():
        base = Path(sp) / "nvidia"
        if base.is_dir():
            for dll in sorted(base.glob("*/bin/*.dll")):
                try:
                    ctypes.WinDLL(str(dll))
                except OSError:
                    pass
    t0 = time.time()
    try:
        model = WhisperModel("small", device="cuda", compute_type="float16")
        # La construcción no valida los DLLs: forzar inferencia mínima.
        list(model.transcribe(np.zeros(16000, dtype=np.float32))[0])
        dev = "cuda"
    except Exception as e:
        log(f"[stt] CUDA unavailable ({type(e).__name__}) → CPU int8")
        model = WhisperModel("small", device="cpu", compute_type="int8")
        dev = "cpu"
    log(f"[stt] whisper small ready in {time.time() - t0:.1f}s "
        f"(device={dev})")
    return model, dev


def transcribe(model, audio_16k: np.ndarray, final: bool = True) -> str:
    """Audio float32 mono 16 kHz → texto en inglés (task=translate: se
    puede hablar español o inglés). Parciales con beam 1 (velocidad);
    finales con beam 5 (calidad)."""
    segments, _info = model.transcribe(
        audio_16k, task="translate", beam_size=5 if final else 1,
        vad_filter=False)
    text = " ".join(s.text.strip() for s in segments).strip()
    return text.rstrip(".!?")
