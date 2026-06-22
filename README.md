# ResearchEHAM

**Experiment on Heteroassociative Associative Memory with a Transactive Memory System**

This repository contains the implementation and experimental results for the MAE-TMS research project, which models Wegner's (1987) Transactive Memory System on top of the associative memories of Pineda & Morales. The system runs end to end — text → image and image → text — using only associative memories, with explicit rejection in both directions.

## Overview

The system combines:
- **MAE (Masked Autoencoder)**: ResNet18 encoder → 64-dim latent; ConvTranspose decoder trained on ETH-80 (apple, horse, car).
- **`HeteroAssociativeMemory`** (`mem_dom_H`): subclass of `HeteroAssociativeMemory4D` (Pineda & Morales) — the content bridge mapping binary label vectors ↔ quantized prototype latents, modulated by per-feature weights from the homo-associative memories.
- **`HomoAssociativeMemory`** (`mem_dom_L`, `mem_dom_R`): wrapper around `AssociativeMemory` (Pineda & Morales) — models the distribution of a single domain and is the only memory that produces per-feature recognition weights (`recog_weights`).
- **`DirectoryMemory`** (`mem_dir`): Wegner's transactive directory — a `HeteroAssociativeMemory4D` whose right domain is the agent identity (one-hot, q=2). Answers "who knows this cue?" and supports directory updating, retrieval coordination, and (externally) information allocation.
- **fastText + spaCy**: NLP pipeline tokenizing queries into binary vectors (sign(v) ∈ {−1,+1}³⁰⁰), with lemma-normalized vocabulary.

### Architecture per agent (4 AMRs)

```
Agent (apple / horse / car)
  ├── mem_dom_H  HeteroAssociativeMemory(n=300, m=16, p=64, q=32)   hetero label↔latent
  ├── mem_dom_L  HomoAssociativeMemory(n=300, m=16)                 homo label  → recog weights
  ├── mem_dom_R  HomoAssociativeMemory(n=64,  m=32)                 homo latent → recog weights
  └── mem_dir    DirectoryMemory(n=300, m=16, n_agents=3)           routing label→agent

TME
  ├── mem_dir_L  DirectoryMemory(n=300, m=16, n_agents=3)           label-space routing
  └── mem_dir_R  DirectoryMemory(n=64,  m=32, n_agents=3)           latent-space routing (inverse)
```

### What changed in v3

- **Instance-based filling**: λ accumulates the real domain distribution (N=200 images per class) instead of a single averaged prototype. This eliminates the domain density bias at the root — masses are equalized by construction.
- **Gate-only scoring**: the official score is `Agent.recognize_gated` (mean activation gated by containment). The `÷mem.mean` calibration — indispensable on the defective averaged base — is now redundant and was dropped from final scoring.
- **Real visual hemisphere**: image → agent → labels evocation works at 94.1% (was 0/6 before).
- **Meaningful names**: classes renamed to `HomoAssociativeMemory` / `HeteroAssociativeMemory` / `DirectoryMemory`; Wegner vocabulary (`update_directory`).

## Key Results — Experimento 1

Full characterization re-run as a single experiment (sections A–E). EAM parameters ι=0, κ=0, ξ=0, σ=0.1. Evaluation bank: 80 queries with ground truth (27/27/26). Report: [`results/experimento1/informe.md`](results/experimento1/informe.md).

| Metric | Value | Note |
|--------|-------|------|
| Early-phase accuracy | 96.2% | 2.5% honest rejection |
| Mature accuracy, B1 read | **97.5%** | directory ÷count normalization |
| Mature accuracy, raw read | 83.8% | density bias of raw HAM score |
| Early↔mature fidelity | 96.2% | |
| Directory formation (interleaved) | k≈14 | ~26 shuffled, 57 blocked-by-domain |
| Visual evocation (top-3 domain hit) | 94.1% | image → labels |

**Central finding**: with instance-based filling, the domain density bias disappears and `÷mean` becomes redundant — the only calibration that remains irreducible is **B1** on the directory read (97.5% vs 83.8%), because genuine specialization produces unequal masses.

## Project Structure

```
src/                        # Core modules
  associative_memory.py     # HomoAssociativeMemory + DirectoryMemory
  hetero_memory.py          # HeteroAssociativeMemory (HeteroAssociativeMemory4D subclass)
  hetero_lib/               # Pineda & Morales original code (vendored)
  quantizer.py              # Global quantize/dequantize (latent_global_stats.json)
  stage1_dataset.py         # ETH-80 dataset loading
  stage2_encoder.py         # MAE encoder/decoder (ResNet18 + ConvTranspose)
  stage3_conceptnet.py      # Label extraction from ConceptNet 5.7.0
  stage4_fasttext.py        # fastText binary vectors (sign(v) ∈ {−1,+1}³⁰⁰)
  stage5_fill.py            # mem_dom filling by instances (H + L + R per agent)
  stage6_interaction.py     # Agent + TME early phase: routing + 4-AMR learning
  stage7_bidirectional.py   # Bidirectional recall (image → labels), visual hemisphere
  stage8_mature.py          # Mature phase: point-to-point routing via mem_dir

run_experiment3.py          # Sec. A — full protocol (early → directory → mature)
run_experiment2_iota_kappa.py  # Sec. B — native parameters ι × κ
run_experiment4.py          # Sec. C — directory formation curve
run_experiment6.py          # Sec. D — filling-capacity curve
run_ablation.py             # M_dir bias ablation (9 conditions × N × seeds)
app_tme.py                  # Streamlit visualization app
generate_paper_figures.py   # Paper-quality figures (EN + ES)

results/
  experimento1/             # Integrated report (informe.md)
  exp3_corrected_routing/   # Sec. A artifacts
  exp2_iota_kappa/          # Sec. B artifacts
  exp4_directory_formation/ # Sec. C artifacts
  exp6_capacity/            # Sec. D artifacts
  ablation_mdir_bias/       # Ablation CSV + plots

.tex/                       # LaTeX report (sources + figures)
papers_images/{en,es}/      # Paper figures, 14 each
```

## Requirements

Python 3.13. Install all dependencies with:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Key packages: `torch==2.12.0`, `tensorflow==2.21.0`, `numpy==2.4.6`, `spacy==3.8.14`, `streamlit==1.58.0`.
TensorFlow is required by `src/hetero_lib/` (Pineda & Morales original code); classifiers are not loaded in production.

## Running the Streamlit App

```bash
streamlit run app_tme.py
```

The app starts with an **empty mem_dir** (no prior training). Interact via queries in the "Routing en vivo" tab — each query trains the directory incrementally. The "Fase Madura" tab becomes active after enough registrations.

## Reproducing Experimento 1

```bash
python run_experiment3.py            # Sec. A — full protocol → results/exp3_corrected_routing/
python run_experiment2_iota_kappa.py # Sec. B — ι × κ sweep   → results/exp2_iota_kappa/
python run_experiment4.py            # Sec. C — formation      → results/exp4_directory_formation/
python run_experiment6.py            # Sec. D — capacity       → results/exp6_capacity/
```

None of these scripts mutate the trained artifacts in `models/`. The integrated narrative lives in [`results/experimento1/informe.md`](results/experimento1/informe.md).

## Paper Figures

```bash
python generate_paper_figures.py
```

Generates 14 figures × 2 languages → `papers_images/en/` and `papers_images/es/`.

## Note on Large Files

Model weights (`models/*.pkl`, `models/*.pt`) and the ETH-80 dataset (`data/`) are excluded from this repository due to size. Contact the authors for access.

## Reference

Wegner, D. M. (1987). Transactive memory: A contemporary analysis of the group mind. In B. Mullen & G. R. Goethals (Eds.), *Theories of Group Behavior* (pp. 185–208). Springer.
