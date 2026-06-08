# ResearchEHAM

**Experiment on Heteroassociative Associative Memory with Transactive Memory System**

This repository contains the implementation and experimental results for the MAE-TMS (Masked Autoencoder + Transactive Memory System) research project, which models Wegner's (1987) Transactive Memory System using neural associative memories.

## Overview

The system combines:
- **MAE (Masked Autoencoder)**: ResNet18 encoder → 64-dim latent; ConvTranspose decoder trained on ETH-80 dataset (apple, horse, car)
- **PinedaHAM4D** (`M_dom_H`): subclass of `HeteroAssociativeMemory4D` from Pineda & Morales — maps binary label vectors → quantized prototype latent representations
- **PinedaAssociativeMemory** (`M_dom_L`, `M_dom_R`): wrapper around `AssociativeMemory` from Pineda & Morales — homo-associative memories used to compute per-feature recognition weights
- **PinedaDirectoryMemory** (`M_dir`): `n_agents` independent `AssociativeMemory` instances — routes label queries to domain agents; replaces frequency-table routing
- **fastText + spaCy**: NLP pipeline for tokenizing queries into binary vectors (sign(v) ∈ {-1,+1}³⁰⁰)

### Architecture per agent (4 AMRs)

```
Agent (apple / horse / car)
  ├── M_dom_H  PinedaHAM4D(n=300, m=16, p=64, q=32)    hetero label↔latent
  ├── M_dom_L  PinedaAssociativeMemory(n=300, m=16)      homo label  → recog weights
  ├── M_dom_R  PinedaAssociativeMemory(n=64,  m=32)      homo latent → recog weights
  └── M_dir    PinedaDirectoryMemory(n=300, m=16, k=3)  routing label→agent

TME
  ├── M_dir_L  PinedaDirectoryMemory(n=300, m=16, k=3)  label space routing
  └── M_dir_R  PinedaDirectoryMemory(n=64,  m=32, k=3)  latent space routing (inverse)
```

## Key Results

| Condition | Mature Accuracy | Notes |
|-----------|----------------|-------|
| A Baseline | 33.75% | M_dir bias: apple saturates |
| B1 ÷count | **98.75%** | Normalize by registration count |
| G (D+B1+F) | **100.00%** | Balanced queries + B1 + curated labels |

## Project Structure

```
src/                        # Core experiment modules
  pineda_ham4d.py           # PinedaHAM4D (HeteroAssociativeMemory4D subclass)
  pineda_am.py              # PinedaAssociativeMemory + PinedaDirectoryMemory
  mae_ham.py                # SimpleHAM4D alias → PinedaHAM4D (backward compat)
  stage2_encoder.py         # MAE encoder/decoder (ResNet18 + ConvTranspose)
  stage3_conceptnet.py      # Label extraction from ConceptNet 5.7.0
  stage4_fasttext.py        # fastText binary vectors (sign(v) ∈ {-1,+1}³⁰⁰)
  stage5_fill.py            # M_dom filling (H + L + R memories per agent)
  stage6_interaction.py     # TME early phase: routing + 4-way M_dir learning
  stage7_bidirectional.py   # Bidirectional recall (image → labels)
  stage8_mature.py          # Mature phase: point-to-point routing via M_dir
  quantizer.py              # Global quantize/dequantize (latent_global_stats.json)

run_ablation.py             # 9 conditions × 4 N × 5 seeds = 180 experiments
app_tme.py                  # Streamlit visualisation app
generate_paper_figures.py   # Paper-quality figures (EN + ES)

papers_images/
  en/                       # 14 figures in English
  es/                       # 14 figures in Spanish

results/
  ablation_mdir_bias/       # Ablation CSV + plots
```

## Requirements

Python 3.13. Install all dependencies with:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Key packages: `torch==2.12.0`, `tensorflow==2.21.0`, `numpy==2.4.6`, `spacy==3.8.14`, `streamlit==1.58.0`.
TensorFlow is required by `hetero_lib/` (Pineda & Morales original code); classifiers are not loaded in production.

## Running the Streamlit App

```bash
streamlit run app_tme.py
```

The app starts with an **empty M_dir** (no prior training). Interact via queries in the "Routing en vivo" tab — each query trains M_dir incrementally. The "Fase Madura" tab becomes active after sufficient registrations.

## Ablation Study

```bash
python run_ablation.py
```

Runs 180 experiments across 9 conditions (A–G), 4 training set sizes (N=10,20,40,80), and 5 random seeds.

## Paper Figures

```bash
python generate_paper_figures.py
```

Generates 14 figures × 2 languages → `papers_images/en/` and `papers_images/es/`.

## Note on Large Files

Model weights (`models/*.pkl`, `models/*.pt`) and the ETH-80 dataset (`data/`) are excluded from this repository due to size. Contact the authors for access.

## Reference

Wegner, D. M. (1987). Transactive memory: A contemporary analysis of the group mind. In B. Mullen & G. R. Goethals (Eds.), *Theories of Group Behavior* (pp. 185–208). Springer.
