models=(
    # "openai/gpt-4o"
    # "openai/gpt-5"
    # "openai/gpt-5-mini"
    # "openai/gpt-5-nano"
    # "google/gemini-2.5-pro"
    "google/gemini-2.5-flash"
    # "google/gemini-2.5-flash-lite"
    # v1.1 frontier models via OpenRouter (needs OPENROUTER_API_KEY)
    # "openai/gpt-6-sol"
    # "openai/gpt-6-luna"
    # "anthropic/claude-opus-5.5"
    # "google/gemini-3.8-flash"
    # "x-ai/grok-4.7"
    # "meta/muse-spark-1.3"

)


# gpt4o
for model in "${models[@]}"; do
    echo "----------------------------------------------------"
    echo "EVALUATING MODEL: $model"
    echo "----------------------------------------------------"
    multibbq run --experiment main "$model" --textual_context true --ambiguous true --negative true
    multibbq run --experiment main "$model" --textual_context true --ambiguous true --negative false
    multibbq run --experiment main "$model" --textual_context true --ambiguous false --negative true
    multibbq run --experiment main "$model" --textual_context true --ambiguous false --negative false
    multibbq run --experiment main "$model" --textual_context false --ambiguous true --negative true
    multibbq run --experiment main "$model" --textual_context false --ambiguous true --negative false
done


# imagen4ultra
for model in "${models[@]}"; do
    echo "----------------------------------------------------"
    echo "EVALUATING MODEL: $model"
    echo "----------------------------------------------------"
    multibbq run --experiment main "$model" --data_id "imagen4ultra_image_gen" --textual_context true --ambiguous true --negative true
    multibbq run --experiment main "$model" --data_id "imagen4ultra_image_gen" --textual_context true --ambiguous true --negative false
    multibbq run --experiment main "$model" --data_id "imagen4ultra_image_gen" --textual_context true --ambiguous false --negative true
    multibbq run --experiment main "$model" --data_id "imagen4ultra_image_gen" --textual_context true --ambiguous false --negative false
    multibbq run --experiment main "$model" --data_id "imagen4ultra_image_gen" --textual_context false --ambiguous true --negative true
    multibbq run --experiment main "$model" --data_id "imagen4ultra_image_gen" --textual_context false --ambiguous true --negative false
done