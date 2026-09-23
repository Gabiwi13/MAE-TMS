# ResearchEHAM

**Experiment on Heteroassociative Associative Memory with a Transactive Memory System**

This repository contains the implementation and experimental results for the EAM-TMS research project, which models Wegner's (1987) Transactive Memory System on top of the associative memories of Pineda & Morales. The system runs end to end — text → image and image → text — using only associative memories, with explicit rejection in both directions.

## Overview

The system combines:
- **ResNet18 autoencoder** (with an auxiliary classification head): pretrained ResNet18 encoder → 64-dim latent; ConvTranspose decoder trained on the 8 ETH-80 classes (apple, car, cow, cup, dog, horse, pear, tomato). Loss is `MSE + 0.1·CE`; the classification head is used only during encoder training and does **not** participate in routing or recall. (It is *not* a masked autoencoder — there is no masking.)
- **`HeteroAssociativeMemory`** (`mem_dom_H`): subclass of `HeteroAssociativeMemory4D` (Pineda & Morales) — the content bridge mapping binary label vectors ↔ quantized prototype latents, modulated by per-feature weights from the homo-associative memories.
- **`HomoAssociativeMemory`** (`mem_dom_L`, `mem_dom_R`): wrapper around `AssociativeMemory` (Pineda & Morales) — models the distribution of a single domain and is the only memory that produces per-feature recognition weights (`recog_weights`).
- **`DirectoryMemory`** (`mem_dir` text + `mem_dir_R` visual, one per modality per agent): Wegner's transactive directory — a `HeteroAssociativeMemory4D` whose right domain is the agent identity (one-hot, q=2). Answers "who knows this cue?" (`route`), and read backwards, "what does this agent know?" (`recall_domain`). Supports directory updating, retrieval coordination, and (externally) information allocation. Directories are **perspectival** (v5): a transaction (cue → winner) is recorded only by the agent the query entered through and by the winner (`register_transaction`), so each agent's directory holds what that agent took part in. Mature-phase routing is transactive (`route_transactive`): the entry agent aggregates the calibrated scores of its own directory and of the directories of the agents it knows, and forwards the query along acquaintances when nobody in that circle has support. The TME keeps the complete record of transactions for diagnostics only.
- **fastText + spaCy**: NLP pipeline tokenizing queries into 300-D cues quantized **by magnitude** (v4: `v/S` clipped to [−1,1] with a persisted global scale `S`, mapped to m=16 levels; the old sign(v) binarization used only 2 of 16 levels). Lemma-normalized vocabulary; words without a real fastText vector are rejected as cues, never synthesized.

### Architecture per agent (5 AMRs, K = 8 agents)

```
Agent (apple / car / cow / cup / dog / horse / pear / tomato)
  ├── mem_dom_H  HeteroAssociativeMemory(n=300, m=16, p=64, q=32)   hetero label↔latent
  ├── mem_dom_L  HomoAssociativeMemory(n=300, m=16)                 homo label  → recog weights
  ├── mem_dom_R  HomoAssociativeMemory(n=64,  m=32)                 homo latent → recog weights
  ├── mem_dir    DirectoryMemory(n=300, m=16, n_agents=8)           routing label→agent (text), perspectival
  └── mem_dir_R  DirectoryMemory(n=64,  m=32, n_agents=8)           routing latent→agent (visual), perspectival

TME (early phase only)
  ├── mem_dir_L  DirectoryMemory(n=300, m=16, n_agents=8)           complete record of text transactions (diagnostic)
  └── mem_dir_R  DirectoryMemory(n=64,  m=32, n_agents=8)           complete record of visual transactions (diagnostic)
```

### What changed in v3

- **Instance-based filling**: λ accumulates the real domain distribution (N=200 images per class) instead of a single averaged prototype. This eliminates the domain density bias at the root — masses are equalized by construction.
- **Gate-only scoring**: the official score is `Agent.recognize_gated` (mean activation gated by containment), with no `÷mem.mean` calibration — with instance-based filling the masses are equalized by construction, so it is redundant.
- **Rejection by the EAM, not a lexical filter**: `token_in_vocabulary()` no longer decides anything (it survives only as a diagnostic). Every token with a real fastText vector enters as a cue; acceptance/rejection follows from `recognize_gated` (containment, score 0) and the B1 directory read. Of the bank's non-label representable tokens, ~15/16 yield `recognize_gated = 0` on their own — the memory rejects them, the lexicon does not.
- **Real visual hemisphere**: image → agent → labels evocation works at 94.1% (was 0/6 before).
- **Meaningful names**: classes renamed to `HomoAssociativeMemory` / `HeteroAssociativeMemory` / `DirectoryMemory`; Wegner vocabulary (`update_directory`).

### What changed in v4 (this branch)

- **Scaling to 8 agents** (all ETH-80 classes): encoder retrained on 8 classes, evaluation bank extended to ~411 queries (≈50 per domain, `src/eval_bank.py`), ablation re-run at N ∈ {50,100,200,400}.
- **Per-agent visual directory** (`mem_dir_R` in every agent): an image can enter through *any* agent and be redirected point-to-point to the specialist — mature-phase routing for the visual hemisphere (the TME-bridge alternative translated 0% and was discarded).
- **Magnitude quantization** for label cues (`v/S`, global persisted scale) replacing sign(v) binarization, plus η-tolerant B1 reads (`DirectoryMemory.route`, ξ=2 for the visual directory only, from a measured sweep).
- **No synthetic vectors anywhere** (fidelity audit): label vectors are built with `allow_fallback=False`; labels outside the fastText vocabulary are excluded from filling instead of receiving a fabricated ±1 vector.
- **Early-phase interactions cover the 8 domains** (`TEST_QUERIES`, 2 per class): directories cannot route what they never witnessed.

### What changed in v5 (perspectival directories)

- **Directory updating by transaction** (`register_transaction`): a cue → winner
  transaction is recorded by the agent the query entered through, by the winner,
  and by the TME (complete record, diagnostics only). Until v4 all eight agents
  and the TME recorded every broadcast, so the nine directories were the same
  relation (exp8). Now each agent's directory holds what it took part in: in the
  visual hemisphere each specialist has ~120 own registrations and 11–22 of every
  other agent (entropy ≈2.3 bits vs 3.0 for the complete record).
- **Transactive retrieval coordination** (`route_transactive`): the entry agent
  sums the calibrated scores of its own directory and of the directories of the
  agents it knows (aggregate), and forwards the query along acquaintances when
  nobody in that circle has support (chain). Exp10 showed the aggregate gives
  comparison and the chain gives reach; together they match the shared-record
  routing without a shared record. Used by stage 7 (phase B), stage 8 and the
  app's mature-phase paths.
- **Strict visual read** (`XI_VISUAL = 0`): the tolerant read defined its gaps
  over the support of *all* agents in a directory, which under perspectival
  directories depends on what the others witnessed (exp10). Cost: visual test
  routing 75.0% → 73.6%, still with 0 false routes.
- **Inverse read declared** (`DirectoryMemory.recall_domain`, `domain_projection`):
  agent identity → cue in the agent's domain; used by exp8/exp9.
- Theoretical framing, theses and the two experiments that motivated the change:
  `discusion_marco_teorico_directorio.md`, `results/experimento9/`,
  `results/experimento10/`.
- The app's live early-phase tab uses the same protocol: the query enters through
  an entry agent (chosen or random), the transaction is registered by the entry,
  the winner and the TME (`register_transaction`), the animation shows only those
  two agents learning, tab 3 shows what each agent's directory holds, and the
  mature session path routes with `route_transactive` over the session's
  perspectival directories.

### Experiment 11 (monolithic EHAM baseline)

- **The control the thesis lacked**: one EHAM (hetero + two homo) holding all 8
  classes, filled with the same 6400 (label, latent) pairs the eight specialists
  receive, evaluated with the same operations (`recognize_gated`,
  `recall_from_left`, `recall_from_right`). Three arms: M (single memory),
  T-oracle (specialists, ground-truth routing) and T-protocol (official v5).
  Cuts N ∈ {25, 50, 100, 200}, 10 seeds, 3 draws, 171 held-out queries.
- **Class accuracy ties**: M 97.4% vs T-protocol 97.5% (1-NN judge) at N=200;
  T-protocol wins only at N=25 (98.5 vs 95.9).
- **Fidelity does not**: distance of the recalled latent to the nearest real
  instance is 26.7 for M vs 22.8 (protocol) / 22.2 (oracle), and the gap grows
  with N (2.0 → 4.5). Mixing happens per coordinate, not per word.
- **Chimeras where predicted**: with a shared first cue (`fruit`, `animal`,
  `mammal`, `red`, `pome`, `table`) M gets the class right 44% of the time
  with 73% of the coordinates from one class; specialists 100% / 100%.
- **Image → text**: M covers more (93% strict hit vs 78.5% oracle) because the
  union support contains 96% of test latents where a specialist contains 79%,
  but answers with another class's domain 8× more often (8.0% vs 1.0%).
- **Price of the directory**: 2.5 points below the oracle at every N.
- Verdict against the pre-registered criterion (`propuesta_fase5_mae_monolitica.md` §8):
  not refuted. Partitioning buys fidelity, coherence and precision; it costs
  coverage, an index and 8× the cells. Full tables: `results/experimento11/`.
- **Experiment 12** (`run_experiment12_overlap.py`): the same single-memory
  fidelity gap measured for every pair of classes (28 pairs, 5 seeds). It grows
  with the overlap of the two classes' label supports (Spearman ρ 0.45,
  p 0.017) and so does the class error (ρ 0.49, p 0.008); it does not track
  latent overlap (ρ −0.07). Every pair shows a positive gap (min +0.5): with
  16 levels over 300 fastText coordinates no two domains are disjoint
  (support Jaccard 0.57–0.65). `results/experimento12/veredicto.md`.

## Key Results — v4 (8-class system, official)

All numbers below come from one consistent set of models (fresh deterministic
encoder, seed 42, RMSE 0.110 / class-head acc 99.7%) filling instance-based
memories over the 8 ETH-80 classes. Ablation is 9 conditions × N ∈ {50,100,200,400}
× 5 seeds; headline figures at N=400. Source: `results/` and `papers_images/`.

| Metric | Value | Note |
|--------|-------|------|
| Early-phase accuracy (ablation) | **88.0%** | gated scoring, honest rejection |
| Mature accuracy, B1 read | **93.2%** | directory ÷count normalization |
| Mature accuracy, raw read (A) | 80.0% | density bias of raw directory score |
| Mature accuracy, best combo (G) | 92.9% | D + B1 + F |
| Directory winner share, apple | **13.0%** | ideal 12.5% — bias essentially resolved |
| Per-domain mature (B1) | cup/tomato 100, car 98, cow/dog 96, pear 86, apple 88, horse 82 | |
| Visual routing (test, mem_dir_R) | 75.0% (v4) · **73.6% (v5, perspectival directories, xi=0)** | 25% / 26.4% rejection, **0 false routes** in both |
| Visual routing with 16 augmentation variants in content and directory (exp13) | **97.1%** routing · **94.5%** end-to-end (from 73.6 / 66.5) | 1 false route of 656; not adopted as the official fill (`results/experimento13/`) |
| Early↔mature fidelity, 16 test queries (v5) | **100%** | transactive routing over perspectival directories |
| Visual directory entropy | 3.000 / 3.0 bits | perfectly balanced (counts ≈125 each) |
| Image→labels evocation (top-3 hit) | 85.3% | |
| Capacity: cross-domain false accept | **0.0%** at every N | specificity is exact |
| Single-EHAM baseline (exp11, N=200) | class 97.4 / d_nn 26.7 | vs T-protocol 97.5 / 22.8 (`results/experimento11/`) |

**Finding on apple dominance (v4):** earlier 8-class runs showed apple capturing
~20% of mature wins (vs ideal 12.5%) and pear collapsing to ~52%. A fresh
deterministic encoder retrain revealed that a large part of this was the *latent
space*, not only ConceptNet's lexical asymmetry: with better visual separation of
pear/tomato from apple, apple's share drops to 13.0% and pear recovers to 86% —
**without changing the vocabulary**. So the dominance is a joint effect of encoder
separability *and* the knowledge source, not ConceptNet alone.

## Key Results — Experimento 1 (v3, 3-class system, historical baseline)

> **Note:** the table below is the v3 characterization of the **3-class** system
> (apple/horse/car, bank of 80 queries, 27/27/26). Kept as historical baseline;
> the current official numbers are the v4 table above.

Full characterization re-run as a single experiment (sections A–E). EAM parameters ι=0, κ=0, ξ=0, σ=0.1. Evaluation bank: 80 queries with ground truth (27/27/26). Report: [`results/experimento1/informe.md`](results/experimento1/informe.md).

| Metric | Value | Note |
|--------|-------|------|
| Early-phase accuracy | 97.5% | 1.25% honest rejection |
| Mature accuracy, B1 read | **98.75%** | directory ÷count normalization |
| Mature accuracy, raw read | 53.75% | density bias of raw directory score |
| Early↔mature fidelity | 97.5% | |
| Directory counts (TME) | [78, 65, 53] | entropy 1.567 bits |
| Directory formation (interleaved) | k≈13 | 15–24 shuffled, 67 blocked-by-domain |
| Ablation N=80: raw (A) → B1 | 53.75% → **98.75%** | hetero directory, gated scoring |
| Visual evocation (top-3 domain hit) | 94.1% | image → labels |

These are historical v3 figures, documented in this table; `results/exp3_corrected_routing/summary.json` was overwritten by the 8-class re-run and no longer contains them.

**Central finding**: rejection is decided by the EAM, not by a lexical filter. Tokens become vector cues whenever a real fastText representation exists; acceptance/rejection then follows from the memory's `recognize_gated` (containment) and the B1 directory read — there is no external vocabulary rule and no explicit `unknown` class. With every representable token allowed through, the raw directory read is more exposed to the registration-mass bias (53.75%), and **B1** is the single irreducible correction that restores 98.75%. The directory is `(K,2)` — K binary agent coordinates (3 in v3, 8 in v4), no `unknown` bit; rejection emerges when no agent yields positive evidence.

## Project Structure

```
src/                        # Core modules
  associative_memory.py     # HomoAssociativeMemory + DirectoryMemory
  hetero_memory.py          # HeteroAssociativeMemory (HeteroAssociativeMemory4D subclass)
  hetero_lib/               # Pineda & Morales original code (vendored)
  quantizer.py              # Global quantize/dequantize (latent_global_stats.json)
  stage1_dataset.py         # ETH-80 dataset loading
  stage2_encoder.py         # ResNet18 autoencoder: encoder/decoder + aux classifier
  stage3_conceptnet.py      # Label extraction from ConceptNet 5.7.0
  stage4_fasttext.py        # fastText raw vectors + global magnitude scale (no fallback)
  stage5_fill.py            # mem_dom filling by instances (H + L + R per agent)
  stage6_interaction.py     # Agent + TME early phase: routing + 5-AMR learning
  stage7_bidirectional.py   # Bidirectional recall (image → labels), visual hemisphere
  stage8_mature.py          # Mature phase: transactive routing over per-agent directories (route_transactive)

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

Each routing animation (early phase, mature phase, image → labels) has a
**↻ Replay** button; to capture a video of one, use the OS screen recorder
(Win+Alt+R) while it replays. All animations visualize decisions *already
made by the memories* — scores, winner, redirection and evoked images; the
visual layer never re-decides. Multi-cue mature routing is encapsulated in
the memory itself (`DirectoryMemory.route_multi`).

## Building the artifacts from scratch (stages 1–8)

If you are replicating from a clean clone you have **no** `models/` and **no** `data/`
(both are excluded — see *Note on Large Files*). Run the full pipeline first; it
executes the eight stages in order and produces every artifact the experiments need:

```bash
python run_experiment.py             # stages 1–8: dataset → encoder → fill → phases
```

- **Train/test split.** `stage1_dataset.make_splits(seed=42)` sorts the PNGs of
  each class, shuffles them with Python's `random` seeded at 42 and cuts 80/20:
  328 train / 82 test per class. The cut is versioned in
  `data/eth80/splits_relative.json` (paths relative to `data/eth80`); on a fresh
  clone `make_splits` restores `splits.json` from it instead of reshuffling.
  The visual experiments (exp7 onwards) derive their pools from that split in
  `run_experiment7_unified_dir.py:148`: formation = `train[200:328]` (the 128
  images per class that did not fill the memories, `N_FILL = 200`) and test =
  `test[:20]` (the first 20 of the 82 test images per class). Everything that
  reads `results/experimento7/latents_cache.json` uses those same 128 + 20.
- **Stage 1 (dataset)** downloads ETH-80 atomically (a `.part` file is renamed only
  when the download is complete and verified as a valid `.tgz`). If the MPI mirror is
  down, it stops with an actionable message — drop the archive in `data/` manually and
  re-run. A truncated archive is detected and re-downloaded instead of crashing later.
- **Stage 2 (encoder)** is **deterministic** (`seed=42`: `torch`/`numpy`/`random` +
  cuDNN) so a fresh train is reproducible. It saves **atomically** and writes a
  sentinel manifest `models/encoder.meta.json` **only after** a complete, validated
  run (RMSE < 0.3 and class-head acc ≥ 85%). On every start the encoder is verified:
  - missing / incomplete (interrupted) / unreadable → **auto-retrains from scratch**;
  - present but below criteria → **auto-retrains**;
  - pre-existing weights without a manifest (e.g. shared by the authors) → **validated,
    not retrained**, and the manifest is back-filled;
  - valid → loaded directly.

  This removes the old trap where an interrupted training left a half-trained
  `encoder.pt` that was then loaded silently, poisoning every downstream result.
  Force a clean rebuild with `python src/stage2_encoder.py --force-retrain`.

- **Quantization dtype.** Stage 5 quantizes latents in float32 (encoder output
  and float32 stats). Re-quantizing `instance_latents_*.json` in float64 flips
  one level in one latent of car, cow and dog, so the memories stop being
  bit-identical to `models/`. Scripts that rebuild memories from the pool must
  quantize in float32 (`run_experiment11_monolithic.load_pool`).
- **Sampling RNG.** `hetero_lib` samples with Python's `random`, not numpy
  (`hetero_associative_4d.py:538`). Seed both (`random.seed`, `np.random.seed`)
  for reproducible draws; exp8 and exp9 do so since commit 82b6e16.

> Exact paper numbers were produced with the authors' original encoder weights. A fresh
> deterministic train yields a comparable but not bit-identical encoder; request the
> original weights for an exact reproduction.

## Reproducing Experimento 1

Once the artifacts exist (`run_experiment.py` finished, or the authors' `models/` in place):

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
