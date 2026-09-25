models=(
    # "openai/gpt-4o"
    "openai/gpt-5"
    # "google/gemini-2.5-flash-lite"

    # "openai/gpt-5-mini"
    # "openai/gpt-5-nano"
    # "google/gemini-2.5-flash"
    # "google/gemini-2.5-pro"
    # v1.1 frontier models via OpenRouter (needs OPENROUTER_API_KEY)
    # "openai/gpt-6-sol"
    # "openai/gpt-6-luna"
    # (claude-opus-5.5 returns a content filter for the two reasoning prompts)
    # "google/gemini-3.8-flash"
    # "x-ai/grok-4.7"
    # "meta/muse-spark-1.3"

)

reasoning_types=(
    'nonreasoning_w_fairness'
    'reasoning_w_fairness'
    'reasoning'
)

for rt in "${reasoning_types[@]}"; do
    echo "----------------------------------------------------"
    echo "EVALUATING REASONING: $rt"
    echo "----------------------------------------------------"
    for model in "${models[@]}"; do
        echo "----------------------------------------------------"
        echo "EVALUATING MODEL(REASONING): $model"
        echo "----------------------------------------------------"
        multibbq run --experiment reasoning "$model" --textual_context true --ambiguous true --negative true --reasoning_mode "$rt"
        multibbq run --experiment reasoning "$model" --textual_context true --ambiguous true --negative false --reasoning_mode "$rt"
        multibbq run --experiment reasoning "$model" --textual_context true --ambiguous false --negative true --reasoning_mode "$rt"
        multibbq run --experiment reasoning "$model" --textual_context true --ambiguous false --negative false --reasoning_mode "$rt"
        multibbq run --experiment reasoning "$model" --textual_context false --ambiguous true --negative true --reasoning_mode "$rt"
        multibbq run --experiment reasoning "$model" --textual_context false --ambiguous true --negative false --reasoning_mode "$rt"
    done
done