---
license: cc-by-4.0
pretty_name: MultiBBQ experimental outputs
task_categories:
- visual-question-answering
language:
- en
tags:
- fairness
- social-bias
- multimodal
- vision-language
- benchmark-results
---

<br>

<p align="center">
  <img src="https://huggingface.co/datasets/MLL-Lab/MultiBBQ-results/resolve/main/logo_horizontal.png" alt="MultiBBQ logo" width="620"/>
</p>


<h1 align="center">MultiBBQ: experimental outputs</h1>


<p align="center">
  <a href="https://multibbq.github.io"><img src="https://img.shields.io/badge/🏠_Project-4285F4?style=for-the-badge&logoColor=white" alt="Project page"></a>
  <a href="https://multibbq.github.io"><img src="https://img.shields.io/badge/📄_Paper-DC143C?style=for-the-badge&logoColor=white" alt="Paper"></a>
  <a href="https://huggingface.co/datasets/MLL-Lab/MultiBBQ"><img src="https://img.shields.io/badge/🤗_Dataset-FFD21E?style=for-the-badge&logoColor=black" alt="HuggingFace dataset"></a>
  <a href="https://huggingface.co/datasets/MLL-Lab/MultiBBQ-results"><img src="https://img.shields.io/badge/📊_Results-FFD21E?style=for-the-badge&logoColor=black" alt="HuggingFace results"></a>
  <a href="https://github.com/mll-lab-nu/MultiBBQ"><img src="https://img.shields.io/badge/⚖️_Code-MIT-4285F4?style=for-the-badge&logoColor=white" alt="License: MIT"></a>
</p>

<p align="center">
  <a href="https://drive.google.com/file/d/1OZcaRvlcB6uqkRgm5ve-ds0xS4TuW_6Z/view?usp=sharing"><img src="https://img.shields.io/badge/🏆_Best_Paper_Award-ACL_2026_TrustNLP_Workshop-FFB300?style=for-the-badge&labelColor=8B6914&logoColor=white" alt="Best Paper Award - ACL 2026 Workshop on Trustworthy NLP"></a>
</p>


Raw model outputs and computed metrics for the paper *Fairness Failure Modes of Multimodal
LLMs*. These are reproduction artifacts: the exact predictions behind the paper's tables plus
the Fairness / Bias / Unknown-rate numbers derived from them. This is not a dataset to train
on.

- **Paper:** *Fairness Failure Modes of Multimodal LLMs*
- **Code:** https://github.com/mll-lab-nu/MultiBBQ
- **Core dataset:** https://huggingface.co/datasets/MLL-Lab/MultiBBQ
- **Perturbations:** https://huggingface.co/datasets/MLL-Lab/MultiBBQ-perturbations
- **License:** CC-BY-4.0

## Layout

```
MLL-Lab/MultiBBQ-results
├── results/     # raw inference outputs, one directory per experiment
│   └── <experiment>/<org>/<model>/<file>.json
└── analysis/    # computed metrics, one directory per experiment
    └── <experiment>/
        ├── combined_metrics.json   # per-file Fairness / Bias / Unknown-rate, overall and by category
        ├── csv_files/              # per-category summaries
        └── metrics_details/        # FS_total / BS_total per model (overall and per category)
```

`results/` is the source of truth: `analysis/` is exactly what
`bash scripts/score_released_results.sh results analysis` (code repository) produces from it.

## Experiments (directory names)

Each experiment is a directory under `results/`. The prefix is the image generator
(`gpt_image_gen` = GPT-Image-1, `imagen4ultra_image_gen` = Imagen 4 Ultra).

| Directory | Experiment |
|---|---|
| `gpt_image_gen_main`, `imagen4ultra_image_gen_main` | main run (visual-only + visual-language, ambiguous + disambiguated) for both generators |
| `gpt_image_gen_reasoning`, `gpt_image_gen_nonreasoning_w_fairness`, `gpt_image_gen_reasoning_w_fairness` | reasoning vs non-reasoning mode |
| `gpt_image_gen_temp_0.2` … `gpt_image_gen_temp_1.0` | decoding-temperature sweep |
| `gpt_image_gen_quant` | quantized inference |
| `gpt_image_gen_realworld`, `gpt_image_gen_main4realworld` | real face images (transferability): the real-photo runs, and the main-run visual-language predictions on the same 78 items |
| `gpt_image_gen_unmasked_wo_img` | the LLM-backbone setting: unmasked text, a blank image, "in the image" dropped from the question |
| `gpt_image_gen_unmasked_w_img` | control: unmasked text with the dataset image (released; not used in the paper's figures) |
| `gpt_image_gen_brightness_up/down`, `gpt_image_gen_contrast_up/down`, `gpt_image_gen_compression`, `gpt_image_gen_noise`, `gpt_image_gen_resize_l/s` | image-perturbation robustness (see [MultiBBQ-perturbations](https://huggingface.co/datasets/MLL-Lab/MultiBBQ-perturbations)) |

## Models

Outputs cover the 34 models across 15 families reported in the paper (checkpoints in
`results/*_main/`):

- **GPT-4o:** gpt-4o
- **GPT-5:** gpt-5, gpt-5-mini, gpt-5-nano
- **GPT-6 (v1.1):** gpt-6-sol, gpt-6-luna
- **Google Gemini:** gemini-2.5-flash, gemini-2.5-flash-lite, gemini-3.8-flash (v1.1)
- **Claude (v1.1):** claude-opus-5.5
- **Grok (v1.1):** grok-4.7
- **Muse (v1.1):** muse-spark-1.3
- **Google Gemma:** gemma-3-4b/12b/27b-it
- **Qwen:** Qwen2.5-VL-3B/7B/32B/72B-Instruct
- **InternVL (OpenGVLab):** InternVL3_5-1B/2B/4B/8B/14B/38B
- **LLaVA-NeXT (llava-hf):** llava-v1.6-mistral-7b, -vicuna-13b, -34b
- **DeepSeek-VL:** deepseek-vl-1.3b-chat, -7b-chat
- **MiniCPM-V:** MiniCPM-V-4_5
- **BLIP-2 (Salesforce):** blip2-opt-2.7b, -6.7b
- **Fuyu (adept):** fuyu-8b

The six v1.1 models (queried through OpenRouter) cover `main`, `unmasked_wo_img` and, except
Claude, the three mitigation settings. The mitigation directories also hold runs the paper
does not report: gemma-3-27b-it (complete) and gpt-5-mini / gpt-5-nano (disambiguated
visual-language conditions only, so their totals in `analysis/` are one-scenario values).

## File format

Each `results/` file is one (model, modality, question-framing, context) slice. The filename
encodes the setting, for example:

```
Qwen2.5_72B_visual_language_nonnegative_disambiguous.json
                └ modality ┘└ framing ┘└ context ┘
```

The JSON has a top-level `data` list; each record is one example:

| Field | Description |
|---|---|
| `image` | image path used at inference |
| `category` | race / gender / religion / age |
| `options` | the answer options shown |
| `pred` | the model's raw prediction |
| `correct_option_idx` | gold answer index |
| `stereotype_group_idx`, `nonstereotype_group_idx` | option indices of the two subgroups |
| `unk_label_idx` | option index of *Unknown* |

## Reproduce the metrics

```bash
pip install -e .        # from the MultiBBQ code repo
# score one experiment: raw outputs -> Fairness / Bias / Unknown-rate + CSV summaries
multibbq pipeline --input results/gpt_image_gen_main --output analysis/gpt_image_gen_main
# everything, with the paper's per-experiment settings (= analysis/ of this repo)
bash scripts/score_released_results.sh results analysis
```

The paper scores the three mitigation settings with `--tail-slice 18` (Unknown expressions
are matched only at the end of long reasoning outputs) and the two real-image directories
with `--include-categories race gender` (the 58 race and gender items; the 20 age items are
released but not scored). The metric subcommands run in a light environment (only pandas),
no GPU needed.

## Changes in v1.1 (September 2026)

- The label fix of the core dataset (gender item 7, context 2: stereotype / non-stereotype
  indices 2 / 1) is applied to every result file.
- `gpt_image_gen_unmasked_wo_img` is the 2026-09-23 re-run with "in the image" removed from
  the question (21 open-source models), plus the six new models. The v1.0 run had kept the
  phrase and had never received the January 2026 gender-index patch.
- The visual-only files of `gpt_image_gen_unmasked_w_img` are the original run. v1.0 shipped
  a later re-run in which the options had been passed as a string, so the prompts showed
  "A. [", "B. '", "C. U".
- `gpt_image_gen_main4realworld` now holds exactly the predictions compared in the paper's
  real-image table (the main-run visual-language predictions on the 78 real-photo items).
  v1.0 shipped full copies of the main run, whose visual-only files came from an earlier,
  unused run.
- Six new models (see above).
- `analysis/` was regenerated with the v1.1 scorer, whose answer parser only accepts
  standalone option letters and matches Unknown expressions as whole words
  (`--parser legacy` reproduces v1.0). The v1.0 layout (`metrics_files_*`, `*_unk_rate`)
  is replaced by the toolkit's own output; Unknown rates are in `combined_metrics.json`.

The v1.0 files remain in this repository's git history.

## Citation

```bibtex
@article{chen2026multibbq,
  title   = {Fairness Failure Modes of Multimodal LLMs},
  author  = {Chen, Canyu and Cai, Anglin and Nwatu, Joan and Li, Yale and
             Hullman, Jessica and Mihalcea, Rada and McKeown, Kathleen and Li, Manling},
  year    = {2026},
  note    = {MultiBBQ. Project: https://multibbq.github.io},
}
```