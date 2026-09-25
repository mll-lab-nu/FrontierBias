#!/bin/bash
#
# Re-score every experiment of the released outputs (HF dataset MLL-Lab/MultiBBQ-results)
# with the settings behind the paper's tables. This is how analysis/ in that repo is made.
#
# Usage (from a directory holding the released results/ tree):
#   hf download MLL-Lab/MultiBBQ-results --repo-type dataset --include "results/**" --local-dir .
#   bash /path/to/MultiBBQ/scripts/score_released_results.sh [RESULTS_DIR] [ANALYSIS_DIR]
#
# Per-experiment settings:
#   * mitigation (reasoning, reasoning_w_fairness, nonreasoning_w_fairness): --tail-slice 18,
#     so hedges inside a chain of thought ("not sure", "unclear") are not read as Unknown;
#   * real-image comparison (realworld, main4realworld): --include-categories race gender,
#     the 58 race and gender items of the paper's real-image tables (the 20 age items are
#     released but not scored: the face set covers adults only);
#   * everything else: defaults.
# All experiments use the default 'strict' answer parser; add --parser legacy to reproduce v1.0.

set -euo pipefail

RESULTS=${1:-results}
ANALYSIS=${2:-analysis}

for dir in "$RESULTS"/*/; do
    exp=$(basename "$dir")
    opts=()
    case "$exp" in
        *_reasoning|*_reasoning_w_fairness|*_nonreasoning_w_fairness) opts=(--tail-slice 18) ;;
        *_realworld|*_main4realworld) opts=(--include-categories race gender --categories race gender) ;;
    esac
    echo "== $exp ${opts[*]:-}"
    rm -rf "${ANALYSIS:?}/$exp"
    multibbq pipeline --input "$RESULTS/$exp" --output "$ANALYSIS/$exp" ${opts[@]+"${opts[@]}"}
    # The per-file *_w_metrics.json copies repeat the raw predictions; every file's metrics
    # are also in combined_metrics.json, so the released analysis/ keeps only that and the CSVs.
    rm -rf "${ANALYSIS:?}/$exp/analysis"
done
