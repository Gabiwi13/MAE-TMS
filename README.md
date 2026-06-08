# ResearchEHAM

**Experiment on Heteroassociative Associative Memory with Transactive Memory System**

This repository contains the implementation and experimental results for the MAE-TMS (Masked Autoencoder + Transactive Memory System) research project, which models Wegner's (1987) Transactive Memory System using neural associative memories.

## Overview

The system combines:
- **MAE (Masked Autoencoder)**: ResNet18 encoder → 64-dim latent; ConvTranspose decoder trained on ETH-80 dataset (apple, horse, car)
- **SimpleHAM4D**: Pure-numpy 4D heteroassociative memory mapping label vectors → prototype latent representations
- **SimpleDirectoryMemory**: 2D associative memory implementing M_dir — routes queries to domain agents
- **fastText + spaCy**: NLP pipeline for tokenizing queries into binary vectors (sign(v) ∈ {-1,+1}³⁰⁰)

## Key Results

| Condition | Mature Accuracy | Notes |
|-----------|----------------|-------|
| A Baseline | 33.75% | M_dir bias: apple saturates |
| B1 ÷count | **98.75%** | Normalize by registration count |
| G (D+B1+F) | **100.00%** | Balanced queries + B1 + curated labels |

## Project Structure

```
src/                    # Core experiment modules
  stage2_encoder.py     # MAE encoder/decoder (ResNet18 + ConvTranspose)
  stage3_conceptnet.py  # Label extraction from ConceptNet
  stage4_fasttext.py    # fastText binary vectors
  stage5_fill.py        # M_dom training (SimpleHAM4D)
  stage6_interaction.py # TME early phase + M_dir learning
  stage7_bidirectional.py
  stage8_mature.py      # M_dir mature phase routing
  mae_ham.py            # SimpleHAM4D implementation
  quantizer.py          # Quantize/dequantize latent vectors

run_ablation.py         # 9 conditions × 4 N × 5 seeds = 180 experiments
run_experiment.py       # Full experiment pipeline
analyze_semantic.py     # Semantic space analysis
app_tme.py              # Streamlit visualization app
generate_paper_figures.py  # Paper-quality figures (EN + ES)

papers_images/
  en/                   # 14 figures in English
  es/                   # 14 figures in Spanish
  architectural_changes.md

results/
  ablation_mdir_bias/   # Ablation study results (180 experiments)

backup_core/            # Backup of core files before app development
```

## Requirements

```
torch torchvision
numpy scipy matplotlib seaborn pandas
spacy fasttext
streamlit plotly
scikit-learn
```

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
