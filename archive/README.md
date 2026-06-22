# Archive — código histórico

Este directorio contiene código de versiones previas del experimento. **No se
usa para los resultados finales y no debe importarse desde scripts oficiales.**

## Contenido

- `legacy_slot_directory/slot_directory_memory.py` — `SlotDirectoryMemory`, el
  directorio aproximado del ablation original (una memoria homo-asociativa por
  agente). El sistema oficial usa `DirectoryMemory` hetero
  (`src/associative_memory.py`). `SlotDirectoryMemory` exageraba el sesgo de
  densidad, así que sus números (p. ej. condición A ~33% → B1 ~98%) **no**
  representan la arquitectura final. El ablation actual (`run_ablation.py`) ya
  usa el directorio hetero oficial.

- `backup_core/` — copia de seguridad de scripts y módulos de una versión
  anterior. Conservado solo como respaldo histórico; puede contener nombres de
  clases y rutas ya obsoletos.

## Reglas

1. Ningún script oficial (`run_experiment*.py`, `run_ablation.py`, `app_tme.py`)
   importa desde `archive/`.
2. Excluir `archive/` del artefacto/zip final de entrega.
