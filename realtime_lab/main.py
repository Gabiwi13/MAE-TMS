"""MAE en tiempo real — ventana nativa (M1+M2+M3).

Uso:
  python main.py                  ventana con cámara + escucha continua
  python main.py --entry cow      agente de entrada del hemisferio visual
  python main.py --selftest 8     8 s sin ventana: guarda frame anotado y
                                  reporta mic/visión (para verificación)
  python main.py --wavtest f.wav  inyecta un WAV por el camino del mic
                                  (VAD → whisper → ruteo) y termina
Teclas: q salir · m mute mic · t modo voz (early/mature) · e agente de
        entrada (siguiente clase) · +/= agrandar recuadro · -/_ achicarlo.
"""
import argparse
import queue
import sys
import threading
import time
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import overlay                      # noqa: E402
from audio_worker import AudioWorker, SR  # noqa: E402
from router import Router, CLASSES  # noqa: E402
from stt import load_whisper        # noqa: E402

VISION_EVERY_S = 0.25
SMOOTH_N = 5


class VisionWorker(threading.Thread):
    """Analiza el frame más reciente ~4 veces/s con suavizado por
    mayoría (la etiqueta no parpadea)."""

    def __init__(self, router, state):
        super().__init__(daemon=True)
        self.router = router
        self.state = state
        self.recent = []

    def run(self):
        while not self.state.get("stop"):
            frame = self.state.get("frame")
            if frame is None:
                time.sleep(0.05)
                continue
            t0 = time.time()
            res = self.router.route_frame(
                frame, crop_frac=self.state.get("crop_frac", 0.55),
                entry=self.state.get("entry"))
            self.recent.append(res["winner"])
            self.recent = self.recent[-SMOOTH_N:]
            # mayoría (None cuenta como voto de rechazo)
            best = max(set(self.recent), key=self.recent.count)
            self.state["vision"] = {
                "winner": best,
                "scores": res["scores"],
                "eye": res["eye_bgr"],
                "entry": res["entry"],
                "color_fix": res["color_fix"],
                "ms": res["ms"],
            }
            time.sleep(max(0.0, VISION_EVERY_S - (time.time() - t0)))


def mic_probe(seconds=1.0):
    """RMS del micrófono al arrancar — detecta el bloqueo de privacidad
    de Windows antes de que el usuario hable al vacío."""
    import sounddevice as sd
    try:
        rec = sd.rec(int(seconds * SR), samplerate=SR, channels=1,
                     dtype="float32")
        sd.wait()
        return float(np.sqrt((rec ** 2).mean())), None
    except Exception as e:
        return 0.0, f"mic unreachable: {type(e).__name__}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entry", default="apple", choices=list(CLASSES))
    ap.add_argument("--camera", type=int, default=0)
    ap.add_argument("--selftest", type=float, default=0.0)
    ap.add_argument("--wavtest", default="")
    args = ap.parse_args()

    print("[main] loading models (once)…")
    router = Router(entry_agent=args.entry)
    whisper, dev = load_whisper()

    state = {"stop": False, "crop_frac": 0.55, "entry": args.entry,
             "voice_mode": "early"}
    phrases = queue.Queue()

    # ---- modo wavtest: voz sintética end-to-end, sin mic ni ventana ----
    if args.wavtest:
        import wave
        from scipy.signal import resample_poly
        with wave.open(args.wavtest) as w:
            sr0 = w.getframerate()
            raw = np.frombuffer(w.readframes(w.getnframes()),
                                dtype=np.int16).astype(np.float32) / 32768.0
        audio = resample_poly(raw, SR, sr0).astype(np.float32) \
            if sr0 != SR else raw
        aw = AudioWorker(whisper, phrases, state)
        aw.feed_wav(audio)
        aw.run_injected()
        try:
            ph = phrases.get_nowait()
        except queue.Empty:
            print("[wavtest] FAIL: VAD produced no phrase")
            return 1
        route = router.route_text(ph["text"])
        print(f"[wavtest] early: '{ph['text']}' "
              f"(stt {ph['stt_ms']:.0f} ms) -> {route['winner']} "
              f"(routing {route['ms']:.1f} ms) "
              f"scores_max={max(route['scores'].values()):.1f}")
        print(f"[wavtest] session M_dir registered: "
              f"{dict(zip(CLASSES, router.session_counts.tolist()))}")
        for ent in ("apple", "cow"):
            rm = router.route_text_mature(ph["text"], entry=ent)
            print(f"[wavtest] mature entry={ent}: -> "
                  f"{rm['winner'] or 'REJECTED'} "
                  f"(routed={rm['routed']}, {rm['ms']:.1f} ms)")
        if route["winner"]:
            res = router.evoke(route["winner"], route["q_vecs"])
            print(f"[wavtest] recall: "
                  f"{'image OK' if res['img_bgr'] is not None else 'not recognized'} "
                  f"in {res['ms']:.0f} ms (token {res['token']}, "
                  f"weight {res['weight']:.0f})")
            if res["img_bgr"] is not None:
                out = Path(__file__).parent / "wavtest_evocacion.png"
                cv2.imwrite(str(out), res["img_bgr"])
                print(f"[wavtest] recalled memory -> {out.name}")
        return 0

    # ---- cámara ----
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print("[main] no camera — voice-only mode")
        cap = None

    # ---- micrófono ----
    rms0, mic_err = mic_probe()
    if mic_err is None and rms0 < 1e-5:
        mic_err = ("mic is SILENT (rms=0): Windows -> Privacy -> "
                   "Microphone -> desktop apps")
    if mic_err:
        print(f"[main] WARNING: {mic_err}")
        state["mic_error"] = mic_err
    aw = AudioWorker(whisper, phrases, state)
    aw.start()
    vw = VisionWorker(router, state)
    if cap is not None:
        vw.start()

    last_route = None
    t_start, n_frames, fps = time.time(), 0, 0.0
    headless = args.selftest > 0
    end_at = time.time() + args.selftest if headless else None
    print(f"[main] running ({'selftest' if headless else 'window'}); "
          f"vision entry '{args.entry}', whisper on {dev}")

    while not state.get("stop"):
        if cap is not None:
            ok, frame = cap.read()
            if not ok:
                break
            state["frame"] = frame
        else:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)

        try:
            ph = phrases.get_nowait()
            if state["voice_mode"] == "mature":
                route = router.route_text_mature(ph["text"],
                                                 entry=state["entry"])
            else:
                route = router.route_text(ph["text"])
            route["stt_ms"] = ph["stt_ms"]
            last_route = route
            _dest = route["winner"] or "REJECTED"
            _via = (f"{state['entry']} -> {_dest} [mature/M_dir]"
                    if route["mode"] == "mature"
                    else f"TME -> {_dest} [early]")
            print(f"[voice] '{route['query']}' : {_via} "
                  f"(stt {ph['stt_ms']:.0f} ms + routing {route['ms']:.1f} ms)")
            if route["winner"]:
                # Evocación asíncrona: el recall estocástico es lo único
                # lento — el video y la voz siguen fluidos mientras el
                # ganador "recuerda", y la imagen aparece al estar lista.
                state["evoked"] = {"status": "pending",
                                   "cls": route["winner"]}

                def _evoke(w=route["winner"], qv=route["q_vecs"]):
                    try:
                        res = router.evoke(w, qv)
                        state["evoked"] = {
                            "status": "ok", "cls": w,
                            "img": res["img_bgr"], "token": res["token"],
                            "weight": res["weight"],
                            "proto": res["proto_bgr"],
                            "d_ss": res["d_ss"], "d_proto": res["d_proto"]}
                        print(f"[recall] {w}: "
                              f"{'image' if res['img_bgr'] is not None else 'not recognized'} "
                              f"in {res['ms']:.0f} ms (token {res['token']})")
                    except Exception as e:
                        # Sin esto, un fallo en router.evoke() deja
                        # state["evoked"] en {"status": "pending"} para
                        # siempre y el overlay muestra "recalling..." de
                        # forma indefinida.
                        state["evoked"] = {"status": "error", "cls": w}
                        print(f"[recall] {w}: FAILED ({type(e).__name__}: {e})")

                threading.Thread(target=_evoke, daemon=True).start()
        except queue.Empty:
            pass

        n_frames += 1
        fps = n_frames / max(time.time() - t_start, 1e-6)
        view = frame.copy()
        if cap is not None:
            overlay.draw_vision_label(view, state.get("vision"),
                                      state["crop_frac"])
            vis = state.get("vision") or {}
            overlay.draw_eye(view, vis.get("eye"),
                             vis.get("color_fix", False))
        overlay.draw_subtitles(view, state.get("partial", ""),
                               state.get("listening", False))
        canvas = overlay.compose_canvas(view)
        overlay.draw_header(canvas, fps, state["entry"],
                            state.get("mic_muted", False),
                            state.get("mic_error"))
        overlay.draw_side_panel(
            canvas, frame.shape[1], state["voice_mode"], state["entry"],
            last_route, state.get("evoked"), state.get("vision"),
            router.session_counts, list(CLASSES))

        if headless:
            if time.time() >= end_at:
                out = Path(__file__).parent / "selftest_frame.png"
                cv2.imwrite(str(out), canvas)
                vis = state.get("vision") or {}
                print(f"[selftest] fps={fps:.1f} "
                      f"mic_rms0={rms0:.5f} "
                      f"vision={vis.get('winner')} "
                      f"({vis.get('ms', 0):.0f} ms/frame) "
                      f"frame={out.name}")
                break
            time.sleep(0.01)
        else:
            cv2.imshow("MAE realtime", canvas)
            k = cv2.waitKey(1) & 0xFF
            if k == ord("q"):
                break
            if k == ord("m"):
                state["mic_muted"] = not state["mic_muted"]
            if k in (ord("+"), ord("=")):
                state["crop_frac"] = min(1.0, state["crop_frac"] + 0.05)
            if k in (ord("-"), ord("_")):
                state["crop_frac"] = max(0.25, state["crop_frac"] - 0.05)
            if k == ord("t"):
                state["voice_mode"] = ("mature"
                                       if state["voice_mode"] == "early"
                                       else "early")
                print(f"[main] voice mode: {state['voice_mode']}")
            if k == ord("e"):
                classes = list(CLASSES)
                i = classes.index(state["entry"])
                state["entry"] = classes[(i + 1) % len(classes)]
                print(f"[main] entry agent: {state['entry']}")

    state["stop"] = True
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
