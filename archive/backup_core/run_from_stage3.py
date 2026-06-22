"""
Re-ejecuta el experimento desde Etapa 3 (labels ConceptNet) hasta Etapa 8.
Usa modelos ya entrenados de Etapas 1-2 (encoder, decoder, dataset).

Borra los modelos que dependen de los labels antes de re-ejecutar,
para que stage5 no reutilice los pickles del llenado anterior.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

MODELS_DIR = ROOT / "models"
CLASSES = ["apple", "horse", "car"]


def clean_dependent_models():
    """Borra modelos que dependen de los labels (stage5+)."""
    to_delete = []
    # stage5: M_dom relleno con labels anteriores
    for cls in CLASSES:
        to_delete.append(MODELS_DIR / f"mem_dom_{cls}.pkl")
        to_delete.append(MODELS_DIR / f"proto_latent_{cls}.json")
    # stage6: TME y agentes con M_dir entrenado
    to_delete.append(MODELS_DIR / "tme.pkl")
    for cls in CLASSES:
        to_delete.append(MODELS_DIR / f"agent_{cls}.pkl")

    deleted = []
    for p in to_delete:
        if p.exists():
            p.unlink()
            deleted.append(p.name)

    if deleted:
        print(f"  Modelos borrados ({len(deleted)}): {', '.join(deleted)}")
    else:
        print("  No habia modelos previos de stages 5-6.")


def banner(stage, title):
    print(f"\n{'='*60}")
    print(f"  ETAPA {stage}: {title}")
    print(f"{'='*60}\n")


def run():
    print("Re-ejecutando experimento desde Etapa 3")
    print("(Etapas 1-2 ya completas, encoder.pt y dataset intactos)")

    print("\nLimpiando modelos dependientes de labels anteriores...")
    clean_dependent_models()

    # ---------------------------------------------------------------
    banner(3, "Labels semánticos via ConceptNet")
    # ---------------------------------------------------------------
    from stage3_conceptnet import run as stage3_run
    all_labels, shared = stage3_run()
    print(f"\n  Labels compartidos: {shared}")
    print("OK Etapa 3")

    # ---------------------------------------------------------------
    banner(4, "Vectorización fastText")
    # ---------------------------------------------------------------
    from stage4_fasttext import run as stage4_run
    stage4_run()
    print("OK Etapa 4")

    # ---------------------------------------------------------------
    banner(5, "Llenado M_dom")
    # ---------------------------------------------------------------
    from stage5_fill import run as stage5_run
    stage5_run()
    print("OK Etapa 5")

    # ---------------------------------------------------------------
    banner(6, "TME y M_dir — fase temprana")
    # ---------------------------------------------------------------
    from stage6_interaction import run as stage6_run
    tme, agents, results6 = stage6_run()
    correct6 = sum(1 for r in results6 if r.get("correct"))
    print(f"  Routing fase temprana: {correct6}/{len(results6)}")
    print("OK Etapa 6")

    # ---------------------------------------------------------------
    banner(7, "Recuperación bidireccional")
    # ---------------------------------------------------------------
    from stage7_bidirectional import run as stage7_run
    results7 = stage7_run()
    print("OK Etapa 7")

    # ---------------------------------------------------------------
    banner(8, "Fase madura — punto a punto")
    # ---------------------------------------------------------------
    from stage8_mature import run as stage8_run
    fidelity = stage8_run()
    print(f"  Fidelidad fase madura: {fidelity*100:.1f}%")
    print("OK Etapa 8")

    print("\n" + "=" * 60)
    print("  EXPERIMENTO COMPLETADO (con labels reales de ConceptNet)")
    print(f"  Fidelidad fase madura: {fidelity*100:.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    run()
