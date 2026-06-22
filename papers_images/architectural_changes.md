# Architectural Changes — EAM-TMS
**Project:** Associative Transactive Memory (Wegner 1987) on ETH-80
**Versions:** v1.0 (initial) → v2.0 (current)
**Date:** 2026-06-07

---

## Version 1.0 — Initial architecture

### Components
| Module | Description | Parameters |
|--------|-------------|------------|
| **Encoder** | Pretrained ResNet18 → linear(512→64) | latent: 64 dims |
| **Decoder** | ConvTranspose 64→3×128×128 + Sigmoid | target: [0,1] |
| **Quantizer** | `quantize(v, q=32)` with fixed vmin=-1, vmax=1 | 32 bins |
| **fastText** | sign(v) ∈ {-1,+1}^300, `quantize_binary(v, m=16)` | 2 of 16 bins used |
| **M_dom** | HeteroAssociativeMemory(n=300, m=16, p=64, q=32) per agent | 3 agents |
| **M_dir** | SimpleDirectoryMemory(n=300, m=16, n_agents=3) | predict = vote sum |
| **TME** | Star topology, broadcast early → argmax → M_dir.register | early/mature phase |
| **Labels** | ConceptNet 5.7.0 RelatedTo (~62 words per domain) | includes "computer","mac" |

### Early-phase flow (v1)
```
query → spaCy → lemmas → fastText → sign() → quantize_binary()
      → broadcast to 3 M_dom → recognize_from_left() → argmax → winner
      → M_dir.register(v_label_q, winner_idx) per token
      → M_dom[winner].recall_from_left() → dequantize(q, 32) → decoder → image
```

### Mature-phase flow (v1)
```
query → tokens → v_q → M_dir.predict() → argmax → destination agent
```

### Problems identified in v1
1. **Critical dequantization bug**: `dequantize(q, 32)` used hardcoded vmin=-1, vmax=1.
   Actual encoder latent space is ≈[-16, +20]. Images appeared as blue backgrounds
   with black artifacts — no real visual content.
2. **Structural M_dir bias**: apple won ~86-100% of queries in early phase.
   At N=80, 100% of mature queries were routed to apple regardless of content.
3. **ConceptNet polysemy**: Apple Inc. labels (computer, mac, macintosh, eden)
   contaminated M_dom[apple], causing car/horse tokens to activate the apple agent.
4. **Underused binary bins**: `quantize_binary(sign(v), m=16)` maps only to {0, 15},
   using 2 of 16 possible bins. Increasing m (to 32, 64) does not improve discrimination.

---

## Version 2.0 — Changes and improvements

### 1. Critical fix: correct dequantization
**Files:** `src/stage6_interaction.py`, `test_label_recall.py`

```python
# v1 (wrong):
v_latent = dequantize(recalled_q.astype(float), 32)   # vmin=-1, vmax=1

# v2 (correct):
stats  = json.loads((MODELS_DIR / "latent_global_stats.json").read_text())
g_min  = np.array(stats["global_min"])   # shape (64,), range ≈ [-16, +20]
g_max  = np.array(stats["global_max"])
v_norm   = recalled_q.astype(float) / 31.0
v_latent = (v_norm * (g_max - g_min) + g_min).astype(np.float32)
```
**Impact:** Retrieved images changed from blue/black backgrounds to recognizable
prototypes (beige sphere for apple, dark blob for horse, flat shape for car).

---

### 2. Ablation study: 9 diagnostic conditions
**File:** `run_ablation.py` (new, ~500 lines)

| Condition | Description | Mature acc N=80 |
|-----------|-------------|-----------------|
| A | Original baseline | 33.75% |
| B1 | ÷ registration count (linear normalization) | **98.75%** |
| B2 | ÷ √count (sub-linear normalization) | 37.50% |
| C | Registration cap (max_ratio=3.0) | 33.75% |
| D | Balanced queries (N//3 per domain) | 33.33% |
| E32 | M_dir with m=32 bins | 33.75% |
| E64 | M_dir with m=64 bins | 33.75% |
| F | Curated ConceptNet (no computer/mac/macintosh) | 37.50% |
| **G** | D + B1 + F | **100.00%** |

**Key finding:** B1 normalization (÷count) alone resolves 98.75% of the bias.
Combination G eliminates the bias completely.

**New class:** `DirectoryMemoryTracked` extends `SimpleDirectoryMemory` with
`_counts` per agent and `predict_normalized(mode="linear"|"sqrt")` method.

---

### 3. fastText semantic analysis
**File:** `analyze_semantic.py` (new)

Confirmed: in continuous space (300 dims), "engine" is semantically closer to
car (cosine=0.57) than to apple (cosine=0.24). Routing error occurs ONLY after
binary quantization sign(v) → {0, 15}.

cosine(computer, machine) = 0.43 explains why Apple Inc. labels contaminate
the routing of mechanical tokens.

---

### 4. Label → image recall test
**File:** `test_label_recall.py` (new)

End-to-end test: text → M_dom → recall → decoder → image.
Includes 3 test sets: own-domain labels (18), multi-token (6), cross-domain (6).
Uses corrected v2 dequantization.

---

### 5. Streamlit visualizer
**File:** `app_tme.py` (new, ~840 lines)

Interactive web interface without modifying any core files:
- **Tab 1 — Live routing:** query → tokenization → M_dom scores → Plotly graph
  → retrieved image. Session M_dir accumulates query by query.
- **Tab 2 — M_dir evolution:** registration bars, per-query bias line,
  automatic entropy diagnostics.
- **Tab 3 — Mature phase:** M_dir-based routing, jump visualization,
  early vs mature comparison.
- **Tab 4 — ETH-80 reference:** real images and ConceptNet labels.

**Note:** App M_dir starts empty per session (does not load tme.pkl).
M_dom and decoder loaded from pkl via @st.cache_resource.

---

## Summary of new files in v2

| File | Type | Description |
|------|------|-------------|
| `run_ablation.py` | Script | Ablation study 9 cond × 4 N × 5 seeds |
| `analyze_semantic.py` | Script | fastText cosine analysis |
| `test_label_recall.py` | Script | Text→image recall test |
| `app_tme.py` | App | Streamlit visualizer |
| `generate_paper_figures.py` | Script | Paper-quality figures (this file) |
| `backup_core/` | Directory | Core backup before app development |
| `papers_images/en/` | Directory | English paper figures |
| `papers_images/es/` | Directory | Spanish paper figures |
| `results/ablation_mdir_bias/` | Directory | Ablation CSV + plots |
| `results/label_recall/` | Directory | Text→image recall images |

---

## Recommendations for v3

1. **Continuous vectors in M_dir**: use raw fastText (not binarized) with global
   min/max normalization to exploit the full m-bin resolution.
2. **Load trained M_dir in app**: sidebar toggle to load `tme.pkl` and show the
   real post-training state (not an empty session).
3. **Full early-phase training in app**: "Run full early phase" button that
   streams all ConceptNet labels through the system with a progress bar.
4. **Systematic ConceptNet curation** for any domain with named-entity polysemy
   (Apple Inc., Ford, etc.).
