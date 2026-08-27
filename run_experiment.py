"""
Orquestador principal del experimento EAM-TMS.
Ejecuta las 8 etapas en orden, verifica cada una antes de continuar.
"""
import sys
from pathlib import Path

# En Windows la consola usa cp1252 por defecto y los print con símbolos como
# '✓', '→' o '≈' (presentes en todas las etapas) revientan con UnicodeEncodeError.
# Forzar UTF-8 aquí arregla la salida de las 8 etapas, que comparten este stdout.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))


def banner(stage, title):
    print(f"\n{'='*60}")
    print(f"  ETAPA {stage}: {title}")
    print(f"{'='*60}\n")


def run():
    # -----------------------------------------------------------
    banner(1, "Dataset ETH-80")
    # -----------------------------------------------------------
    from stage1_dataset import download, extract, organize, verify, make_splits
    download()
    extract()
    organize()
    if not verify():
        sys.exit("Etapa 1 fallida — aborting.")
    make_splits()
    print("\n✓ Etapa 1 OK")

    # -----------------------------------------------------------
    banner(2, "CNN Encoder/Decoder")
    # -----------------------------------------------------------
    from stage2_encoder import (ensure_models, evaluate, get_loaders,
                                 visualize_reconstructions, _inv_norm)

    # ensure_models() valida lo que haya en disco y reentrena si falta, esta
    # corrupto o no cumple los criterios, en vez de seguir con un encoder a
    # medio entrenar.
    try:
        encoder, decoder, classifier = ensure_models()
    except RuntimeError as e:
        sys.exit(f"Etapa 2 fallida: {e}")

    _, test_loader = get_loaders()
    rmse, acc = evaluate(encoder, decoder, classifier, test_loader, _inv_norm())
    print(f"  RMSE={rmse:.4f}  accuracy={acc:.1f}%")
    visualize_reconstructions(encoder, decoder, test_loader)
    print("\n✓ Etapa 2 OK")

    # -----------------------------------------------------------
    banner(3, "Labels semánticos via ConceptNet")
    # -----------------------------------------------------------
    from stage3_conceptnet import run as stage3_run
    all_labels, shared = stage3_run()
    print(f"  Shared labels: {shared}")
    print("\n✓ Etapa 3 OK")

    # -----------------------------------------------------------
    banner(4, "Vectorización fastText")
    # -----------------------------------------------------------
    from stage4_fasttext import run as stage4_run
    stage4_run()
    print("\n✓ Etapa 4 OK")

    # -----------------------------------------------------------
    banner(5, "Llenado M_dom")
    # -----------------------------------------------------------
    from stage5_fill import run as stage5_run
    agents_raw = stage5_run()
    print("\n✓ Etapa 5 OK")

    # -----------------------------------------------------------
    banner(6, "TME y M_dir — fase temprana")
    # -----------------------------------------------------------
    from stage6_interaction import run as stage6_run
    tme, agents, results6 = stage6_run()
    print("\n✓ Etapa 6 OK")

    # -----------------------------------------------------------
    banner(7, "Recuperación bidireccional")
    # -----------------------------------------------------------
    from stage7_bidirectional import run as stage7_run
    results7 = stage7_run()
    print("\n✓ Etapa 7 OK")

    # -----------------------------------------------------------
    banner(8, "Fase madura — punto a punto")
    # -----------------------------------------------------------
    from stage8_mature import run as stage8_run
    fidelity = stage8_run()
    print(f"  Fidelidad: {fidelity*100:.1f}%")
    print("\n✓ Etapa 8 OK")

    print("\n" + "="*60)
    print("  EXPERIMENTO COMPLETADO")
    print(f"  Fidelidad fase madura: {fidelity*100:.1f}%")
    print("="*60)


if __name__ == "__main__":
    run()
