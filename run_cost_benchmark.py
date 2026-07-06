"""
Benchmark de costo computacional — mide el tiempo de pared (wall-clock) de
reproducir el experimento completo desde cero en esta máquina.

Pipeline (en proceso, en orden): etapas 1–8, FORZANDO el entrenamiento del
encoder (stage2.train, sobrescribe los modelos). Luego la batería de análisis
(exp2–6 + ablation + rejection_probe + figuras) como subprocesos aislados.

Captura hardware (CPU, RAM, torch CPU/GPU) y escribe
results/computational_cost/{cost.json, report.md}.

Uso:  python run_cost_benchmark.py     (largo: el entrenamiento es la parte cara)
"""
import os
import sys
import time
import json
import platform
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = ROOT / "results" / "computational_cost"
OUT.mkdir(parents=True, exist_ok=True)

timings = []


def _now():
    return datetime.now().strftime("%H:%M:%S")


def record(name, dt, ok=True, note=""):
    timings.append({"step": name, "seconds": round(dt, 2),
                    "minutes": round(dt / 60, 3), "ok": ok, "note": note})
    print(f"[COST {_now()}] {name}: {dt:.1f}s ({dt/60:.2f} min) "
          f"{'OK' if ok else 'FAIL: ' + note}", flush=True)
    # volcado incremental por si el run se interrumpe
    (OUT / "cost_partial.json").write_text(
        json.dumps(timings, indent=2, ensure_ascii=False), encoding="utf-8")


def timed_call(name, fn):
    t0 = time.perf_counter()
    ok, note = True, ""
    try:
        fn()
    except Exception as e:  # noqa: BLE001
        ok, note = False, repr(e)[:300]
    record(name, time.perf_counter() - t0, ok, note)


def timed_script(name, script):
    t0 = time.perf_counter()
    env = dict(os.environ, PYTHONHASHSEED="0")
    r = subprocess.run([sys.executable, script], cwd=str(ROOT), env=env)
    record(name, time.perf_counter() - t0, r.returncode == 0, f"rc={r.returncode}")


def _n_train_imgs() -> int:
    """Total de imágenes de entrenamiento reales (suma sobre las 8 clases).
    Antes estaba hardcodeado a 984 = 328×3, cifra de la era de 3 clases."""
    try:
        splits = json.loads((ROOT / "data" / "eth80" / "splits.json").read_text())
        from stage6_interaction import CLASSES
        return sum(len(splits[c]["train"]) for c in CLASSES)
    except Exception:
        return -1


def hardware():
    import torch
    info = {
        "platform": platform.platform(),
        "machine": platform.machine(),
        # Sin fabricar un modelo de CPU ajeno si platform.processor() viene vacío.
        "processor": platform.processor() or "desconocido (platform.processor vacío)",
        "cpu_count_logical": os.cpu_count(),
        "ram_total_gb": None,
        "python": platform.python_version(),
        "torch_version": torch.__version__,
        "torch_cuda_available": torch.cuda.is_available(),
        "torch_num_threads": torch.get_num_threads(),
        "gpu_present_unused": "NVIDIA RTX 2050 4GB (torch es CPU-only, no se usa)",
    }
    try:
        import ctypes
        if os.name == "nt":
            class MS(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong),
                            ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong),
                            ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong),
                            ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong),
                            ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            ms = MS(); ms.dwLength = ctypes.sizeof(MS)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(ms))
            info["ram_total_gb"] = round(ms.ullTotalPhys / 1e9, 1)
    except Exception:
        pass
    return info


def main():
    print("=" * 64)
    print("  BENCHMARK DE COSTO COMPUTACIONAL — reproducción completa")
    print("=" * 64)
    hw = hardware()
    print(json.dumps(hw, indent=2, ensure_ascii=False))

    t_all = time.perf_counter()

    # ---- Pipeline 1–8 (en proceso, en orden) ----
    from stage1_dataset import download, extract, organize, verify, make_splits

    def s1():
        download(); extract(); organize(); verify(); make_splits()
    timed_call("stage1_dataset", s1)

    # Etapa 2: FORZAR entrenamiento (sobrescribe modelos) + regenerar la
    # imagen de reconstrucciones (igual que run_experiment.py).
    from stage2_encoder import (train, get_loaders, evaluate,
                                visualize_reconstructions, _inv_norm)

    def s2():
        rmse, acc, encoder, decoder, classifier = train()
        _, test_loader = get_loaders()
        # Reusar la normalización inversa oficial en vez de re-escribir sus
        # constantes (se desincronizaría en silencio si cambia el dataset).
        evaluate(encoder, decoder, classifier, test_loader, _inv_norm())
        visualize_reconstructions(encoder, decoder, test_loader)
    timed_call("stage2_train_encoder", s2)

    from stage3_conceptnet import run as s3
    timed_call("stage3_conceptnet", s3)
    from stage4_fasttext import run as s4
    timed_call("stage4_fasttext", s4)
    from stage5_fill import run as s5
    timed_call("stage5_fill", s5)
    from stage6_interaction import run as s6
    timed_call("stage6_interaction", s6)
    from stage7_bidirectional import run as s7
    timed_call("stage7_bidirectional", s7)
    from stage8_mature import run as s8
    timed_call("stage8_mature", s8)

    pipeline_seconds = time.perf_counter() - t_all

    # ---- Batería de análisis (subprocesos aislados) ----
    for name, script in [
        ("exp2_iota_kappa",  "run_experiment2_iota_kappa.py"),
        ("exp3_routing",     "run_experiment3.py"),
        ("exp4_formation",   "run_experiment4.py"),
        ("exp5_entropic",    "run_experiment5.py"),
        ("exp6_capacity",    "run_experiment6.py"),
        ("ablation",         "run_ablation.py"),
        ("rejection_probe",  "run_rejection_probe.py"),
        ("paper_figures",    "generate_paper_figures.py"),
    ]:
        timed_script(name, script)

    total_seconds = time.perf_counter() - t_all

    summary = {
        "hardware": hw,
        "date": datetime.now().isoformat(timespec="seconds"),
        "pipeline_seconds": round(pipeline_seconds, 1),
        "pipeline_minutes": round(pipeline_seconds / 60, 2),
        "total_seconds": round(total_seconds, 1),
        "total_minutes": round(total_seconds / 60, 2),
        "steps": timings,
    }
    (OUT / "cost.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- Reporte markdown ----
    lines = [
        "# Costo computacional — reproducción completa del experimento EAM-TMS",
        "",
        "Tiempo de pared (wall-clock) de reproducir el experimento desde cero en "
        "esta máquina. **Todo corre en CPU** (PyTorch CPU-only); la GPU NVIDIA "
        "presente no se utiliza.",
        "",
        "## Máquina",
        "",
        f"- CPU: {hw['processor']}  ·  {hw['cpu_count_logical']} hilos lógicos  "
        f"(torch usa {hw['torch_num_threads']})",
        f"- RAM: {hw['ram_total_gb']} GB",
        f"- GPU: {hw['gpu_present_unused']}",
        f"- SO: {hw['platform']}",
        f"- Python {hw['python']}  ·  torch {hw['torch_version']}  ·  "
        f"CUDA disponible: {hw['torch_cuda_available']}",
        "",
        "## Tiempos por etapa",
        "",
        "| paso | minutos | segundos | ok |",
        "|---|---:|---:|:--:|",
    ]
    for s in timings:
        lines.append(f"| {s['step']} | {s['minutes']:.2f} | {s['seconds']:.1f} | "
                     f"{'✓' if s['ok'] else '✗'} |")
    lines += [
        "",
        f"**Pipeline (etapas 1–8): {summary['pipeline_minutes']:.1f} min**  ·  "
        f"**Total (con batería de análisis): {summary['total_minutes']:.1f} min**",
        "",
        f"El entrenamiento del encoder (stage2, 50 épocas sobre {_n_train_imgs()} "
        "imágenes) domina el costo; el resto del sistema —memorias asociativas, "
        "routing, directorios— es de bajo costo porque son operaciones "
        "matriciales sobre vectores cuantizados, no entrenamiento por gradiente.",
    ]
    (OUT / "report.md").write_text("\n".join(lines), encoding="utf-8")

    print("\n" + "=" * 64)
    print(f"  Pipeline 1–8: {summary['pipeline_minutes']:.1f} min")
    print(f"  TOTAL: {summary['total_minutes']:.1f} min")
    print(f"  Reporte -> {OUT}")
    print("BENCHMARK COMPLETADO.")


if __name__ == "__main__":
    main()
