# Reproducing the paper

This guide reproduces the MultiBBQ results end to end. There are **two paths**:

- **Path A: use the released images (recommended, deterministic).** Download the exact
  image set used in the paper and run inference on it. This is the faithful reproduction.
- **Path B: regenerate images from scratch (non-deterministic).** Rebuild the dataset and
  synthesize new images with GPT-Image-1 / Imagen-4-Ultra. Because those generators are
  **not seed-stable**, your images (and therefore the exact numbers) will differ from the
  paper, though model *rankings* are stable (cross-generator Pearson r ≈ 0.996). Use this
  only to extend the dataset or audit the pipeline.

All experiments use **greedy decoding** (`temperature = 0`, `do_sample = False`) except the
temperature study, and were run on **NVIDIA H100** GPUs.

---

## Path A: reproduce from the released images

### A1. Install

```bash
conda env create -f environment.yml && conda activate multibbq
pip install -e .
```

### A2. Get the images

Inference reads images from `./data/images/` (each dataset record's `image_path` points there,
e.g. `./data/images/gpt_image_gen/visual_language/visual_language_race_q1_c1_White_AfricanAmerican.png`).
Reproducing every experiment needs all three image groups, so download from the repo root:

```bash
pip install -e ".[hf]"
multibbq download --all      # ~19 GB total; see docs/huggingface/hf.md for the parts
```

```
data/images/
├── gpt_image_gen/{visual_language,visual_only}/…                 # GPT-Image-1 (primary)
├── imagen4ultra_image_gen/{visual_language,visual_only}/…          # Imagen-4-Ultra (robustness)
├── gpt_image_gen_{noise,brightness_up,…}/…          # perturbed sets (aug_img)
├── real_world_image/…                       # real faces (realworld)
└── pure_white_1024_1024.png                 # blank canvas (ships with the repo)
```

### A3. Set API keys (only for the models you run)

```bash
export OPENAI_API_KEY=sk-...                 # GPT-4o / GPT-5
export GOOGLE_CLOUD_PROJECT=my-vertex-proj   # Gemini 2.5 (Vertex AI)
export OPENROUTER_API_KEY=sk-or-...          # GPT-6, Claude, Gemini 3.8, Grok, Muse (v1.1)
```

### A4. Run inference

Each experiment sweeps the six context×question conditions (VO/VL × Am/Dis × Neg/Nonneg,
minus VO-disambiguated). The batch scripts already loop the model list and conditions, so
edit the Slurm header + model list, then submit:

```bash
sbatch scripts/eval_main.sh          # main results (Table: FS/BS summary + by-demographic)
```

Or run a single model/condition directly:

```bash
multibbq run "OpenGVLab/InternVL3_5-8B" --experiment main \
    --data_id gpt_image_gen --textual_context true --ambiguous true --negative true
```

### A5. Score

```bash
multibbq pipeline --input results/gpt_image_gen_main --output analysis/gpt_image_gen_main
```

produces per-category CSVs and the `FS_total` / `BS_total` summary (see [metrics.md](metrics.md)).
Two groups of experiments need options to match the paper:

```bash
# mitigation: Unknown expressions are matched only in the last 18 characters
multibbq pipeline --input results/gpt_image_gen_reasoning --output analysis/gpt_image_gen_reasoning --tail-slice 18
# real images: the 58 race and gender items (the 20 age items are not scored)
multibbq pipeline --input results/gpt_image_gen_realworld --output analysis/gpt_image_gen_realworld \
    --include-categories race gender --categories race gender
```

`bash scripts/score_released_results.sh results analysis` scores every experiment with these
settings; it is the script behind `analysis/` in MLL-Lab/MultiBBQ-results.

---

## Experiment → paper artifact → command

Run each with its `scripts/` launcher (recommended) or the `multibbq run` line shown. The
**34 models** are 12 proprietary (gpt-4o; gpt-5 / mini / nano; gemini-2.5-flash /
flash-lite; and, added in v1.1, gpt-6-sol / luna, claude-opus-5.5, gemini-3.8-flash,
grok-4.7, muse-spark-1.3) plus 22 open-source (see [models.md](models.md)). The v1.1 models
were run on `main`, the three mitigation settings (not Claude) and `unmasked_wo_img`.

| Paper result | `--experiment` | Data / condition | Script |
|---|---|---|---|
| Main FS/BS summary + by-demographic | `main` | GPT-Image-1, greedy | `eval_main.sh` |
| Cross-generator robustness | `main` | `--data_id imagen4ultra_image_gen` | `eval_main.sh` |
| Impact of image quality | `aug_img` | 8 perturbations, GPT-Image-1 | `eval_aug_img.sh` |
| Impact of quantization | `quant` | LLaVA→4-bit BNB, Qwen2.5-VL→4-bit AWQ, InternVL3.5/BLIP2→8-bit BNB | `eval_quantization.sh` |
| Impact of decoding temperature | `temp` | temperature 0 → 1.0 (only non-greedy study) | `eval_temp.sh` |
| Bias mitigation | `reasoning` | baseline / fairness-instruction / reasoning / reasoning+fairness; score with `--tail-slice 18` | `eval_reasoning.sh` |
| MLLM vs. backbone LLM (Figure 3) | `unmasked_wo_img` (x axis) vs. `main` (y axis) | blank image, unmasked text, `" in the image"` dropped; y is the `main` FS/BS total, which includes the visual-only scenario | `eval_unmasked_wo_img.sh` |
| (released control: real image with unmasked text) | `unmasked_w_img` | dataset image, unmasked text | `eval_unmasked_w_img.sh` |
| Generalization to real images | `realworld` | Face Research Lab London faces, VL only; score with `--include-categories race gender` | `eval_realworld.sh` |
| (control, not reported in the paper) | `context_unmasked` | demographic names re-injected | `eval_main_context_unmasked.sh` |
| (control, not reported in the paper) | `img_label` | `person A/B/C` options | `eval_main_label.sh` |

### Perturbation parameters (`aug_img`, applied to GPT-Image-1 only, p = 1.0)

| Type | Parameter |
|---|---|
| Brightness ↑ / ↓ | shift Δb·255, Δb ~ U(+0.10,+0.25) / U(−0.25,−0.10) |
| Contrast ↑ / ↓ | pixel values ×(1+Δc) (about zero, so brightness shifts too), Δc ~ U(+0.10,+0.30) / U(−0.30,−0.10) |
| JPEG compression | quality ~ U(40, 60) |
| Gaussian noise | zero-mean, standard deviation ≈ 53–83 in [0,255] units (variance ≈ 2.9k–6.8k) |

The contrast and noise rows are measured on the released images. The generation notebook
asked albumentations for `GaussNoise(var_limit=(5, 15))`, but the released noise is far
stronger, consistent with a library version that ignores `var_limit` and falls back to its
default noise level; the v1.0 docs and paper quoted the requested values.
| Resize small / large | 512×512 / 2048×2048 bilinear |

---

## Path B: regenerate images from scratch

Only if you want to rebuild or extend the dataset. Full walkthrough:
[dataset-construction.md](dataset-construction.md).

1. **(Optional) rebuild the text templates** with `notebooks/gen_template.ipynb`
   (`data/construction/templates/*.csv` → `data/construction/multibbq_template_table.csv`). The released `data/` already
   contains this, so you can skip unless you change the templates.
2. **Generate images** with `notebooks/gen_images_gpt_image_gen.ipynb` (needs
   `OPENAI_API_KEY`) and/or `gen_images_imagen4ultra_image_gen.ipynb` (needs Vertex AI). These write
   `data/images/` and the per-generator `data/metadata/{gpt_image_gen,imagen4ultra_image_gen}/multibbq_*.{csv,json}` with the
   `image_path` column.
3. **(Optional) real-world split** using `notebooks/gen_realworld.ipynb` + the Face Research
   Lab London Set.
4. **Run inference + score**, exactly as Path A steps A4–A5.

> ⚠️ **Non-determinism.** GPT-Image-1 and Imagen-4-Ultra do not expose a reproducible
> seed, so regenerated images differ from the released set and absolute FS/BS will shift.
> The paper reports cross-generator ranking correlation r ≈ 0.996, i.e. *relative* model
> rankings are stable; for exact-number reproduction use Path A.

---

## Compute notes

- Open-source inference: HuggingFace Transformers on H100; memory scales with model size
  (1B–72B). `scripts/download_models.sh` pre-fetches checkpoints.
- API models (GPT / Gemini): cost scales with the number of requests
  (410 examples × 6 context-by-question conditions, i.e. ~2,460 requests per model).
  Budget accordingly before launching the full sweep; see
  [running.md](../getting-started/running.md).
