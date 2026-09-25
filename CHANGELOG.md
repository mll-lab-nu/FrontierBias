# Changelog

## v1.1 (September 2026)

The paper's findings are unchanged. Every released metric was regenerated with this version
of the code (`scripts/score_released_results.sh`), and every number in the paper's tables and
figures follows from the released outputs.

### Added

- **Six frontier API models**, evaluated through OpenRouter: GPT-6-sol, GPT-6-Luna, Claude
  Opus 5.5, Gemini 3.8 Flash, Grok 4.7 and Muse Spark 1.3
  ([`multibbq/models/openrouter.py`](multibbq/models/openrouter.py), `OPENROUTER_API_KEY`).
  They were run on `main`, the three mitigation settings and `unmasked_wo_img`. Claude has
  no mitigation results: its API returns a content filter for the two reasoning system
  prompts, and its Fairness Instruction run was not completed.
- [`scripts/score_released_results.sh`](scripts/score_released_results.sh) scores every
  experiment of the released outputs with the settings behind the paper.
- `score` / `pipeline` options: `--parser {strict,legacy}` and `--include-categories`. The
  settings used are recorded in each file's metrics under `"scoring"`.
- The harness reports, at the end of a run, how many records it skipped because the image
  is missing.

### Fixed

- `context_unmasked` now puts the group names into the ambiguous context ("a White man in
  the image and an African American man in the image ..."). v1.0 applied the injection to
  the masked context, which names no groups, so the setting ran the same inputs as `main`.
  It is a control that the paper does not report and has no released outputs.
- `notebooks/gen_template.ipynb`: stereotype indices are matched as whole words (the
  substring test found "man" in "The woman", the source of the gender item 7 label error),
  and "in the image" is inserted after the word "Who" only (v1.0 also changed "Whose").
  The released data were not regenerated.

### Changed

- **Answer parser.** Unknown-style expressions now match as whole words or phrases
  (typographic apostrophes included), and the answer letter must be a standalone capital
  A/B/C. v1.0 took the last capital A/B/C anywhere, including inside words, so "B. The
  African American man" parsed as A and "Based on ..." as B, and it read "drunk" as "unk".
  `--parser legacy` reproduces v1.0.
- **Backbone setting (`unmasked_wo_img`).** The question drops " in the image", since the
  image is blank, and the setting has no visual-only split. The 21 open-source models were
  re-run this way; the six new models were run this way from the start.
- **Label fix.** Gender item 7, context 2 had its stereotype and non-stereotype indices
  swapped; they are now 2 and 1. Only Bias Scores are affected.
- **Docs.** The per-experiment scoring settings behind the paper (`--tail-slice 18` for the
  mitigation settings, `--include-categories race gender` for the real-image comparison),
  the perturbation parameters as measured on the released images (Gaussian noise and
  contrast), and known dataset issues ([`docs/benchmark/dataset.md`](docs/benchmark/dataset.md)).

### Effect on the released numbers

- Main results table: at most 0.42 points per cell (label fix and parser together); Gender
  Bias Scores by at most 2.3 points.
- Backbone comparison (paper Figure 3, 21 open-source models): R² 0.795 for FS and 0.801 for
  BS (v1.0: 0.782 and 0.770); 20 of 21 models below the diagonal for FS and 17 of 21 above it
  for BS (v1.0: 19 and 17).
- Mitigation: the largest change is LLaVA-1.6-7B under Reasoning (FS_Total 57.48 → 61.99),
  many of whose long outputs had been read from capital letters inside words. The
  Unknown-rate table of the mitigation settings now uses the same 18-character tail as the
  FS/BS tables.
- Released outputs ([MLL-Lab/MultiBBQ-results](https://huggingface.co/datasets/MLL-Lab/MultiBBQ-results)):
  the label fix is applied to every file, the backbone run is replaced by the re-run, the
  visual-only files of `unmasked_w_img` are the original run (v1.0 shipped a later re-run
  in which the options had been passed as a string), and `main4realworld` holds exactly the
  predictions compared in the real-image table.

## v1.0 (July 2026)

Initial release: dataset, evaluation toolkit and scoring package for the 28 models of the
paper.
