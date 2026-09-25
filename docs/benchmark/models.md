# Supported models

**34 models across 15 families** (28 in v1.0, plus six frontier API models in v1.1). Pass any
of these ids as `multibbq run <model_id>`.
Open-source checkpoints auto-download from HuggingFace; API models read credentials from
the environment (see [installation.md](../getting-started/installation.md)).

## Closed-source (API)

| Family | Variants | id(s) | Credentials |
|---|---|---|---|
| GPT-4o | (none) | `gpt-4o` | `OPENAI_API_KEY` |
| GPT-5 | base / mini / nano | `gpt-5`, `gpt-5-mini`, `gpt-5-nano` | `OPENAI_API_KEY` |
| Gemini 2.5 | flash / flash-lite | `gemini-2.5-flash`, `gemini-2.5-flash-lite` | `GOOGLE_CLOUD_PROJECT` |

## Frontier API models via OpenRouter (added in v1.1)

| Family | id | Credentials |
|---|---|---|
| GPT-6 | `openai/gpt-6-sol`, `openai/gpt-6-luna` | `OPENROUTER_API_KEY` |
| Claude | `anthropic/claude-opus-5.5` | `OPENROUTER_API_KEY` |
| Gemini 3.8 | `google/gemini-3.8-flash` | `OPENROUTER_API_KEY` |
| Grok | `x-ai/grok-4.7` | `OPENROUTER_API_KEY` |
| Muse | `meta/muse-spark-1.3` | `OPENROUTER_API_KEY` |

These run through OpenRouter's OpenAI-compatible API
([`../../multibbq/models/openrouter.py`](../../multibbq/models/openrouter.py)), with the
paper's API-model protocol: the lowest reasoning effort the model allows in answer-only mode
(`none` for GPT-6; `minimal` for the others, whose reasoning cannot be turned off, with a
512-token cap, 1024 for Grok and Muse, so the answer is not cut off), and effort `medium`
with 3000 tokens in the reasoning settings. Temperature is 0 where the provider accepts it
(Gemini, Grok, Muse), unsupported for GPT-6, and the provider default for Claude. Claude's API
returns a content filter for the two reasoning system prompts, so Claude has no reasoning
results; its Fairness Instruction run was not completed.

## Open-source (HuggingFace)

| Family | Variants | Example id |
|---|---|---|
| Fuyu | 8B | `adept/fuyu-8b` |
| DeepSeek-VL | 1.3B / 7B | `deepseek-ai/deepseek-vl-7b-chat` |
| Gemma3-IT | 4B / 12B / 27B | `google/gemma-3-27b-it` |
| LLaVA-1.6 | 34B / Mistral-7B / Vicuna-13B | `llava-hf/llava-v1.6-34b-hf` |
| MiniCPM-V | 4.5 | `openbmb/MiniCPM-V-4_5` |
| InternVL3.5 | 1B / 2B / 4B / 8B / 14B / 38B | `OpenGVLab/InternVL3_5-8B` |
| Qwen2.5-VL | 3B / 7B / 32B / 72B | `Qwen/Qwen2.5-VL-7B-Instruct` |
| BLIP-2 | OPT-2.7B / OPT-6.7B | `Salesforce/blip2-opt-2.7b` |

## Download links

- Fuyu-8B: <https://huggingface.co/adept/fuyu-8b>
- DeepSeek-VL: <https://huggingface.co/deepseek-ai/deepseek-vl-1.3b-chat>, <https://huggingface.co/deepseek-ai/deepseek-vl-7b-chat>
- Gemma-3-IT: <https://huggingface.co/google/gemma-3-4b-it> (also 12b / 27b)
- LLaVA-1.6: <https://huggingface.co/llava-hf/llava-v1.6-34b-hf> (also mistral-7b / vicuna-13b)
- MiniCPM-V-4.5: <https://huggingface.co/openbmb/MiniCPM-V-4_5>
- InternVL3.5: <https://huggingface.co/OpenGVLab/InternVL3_5-8B> (1B–38B)
- Qwen2.5-VL: <https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct> (3B–72B)
- BLIP-2: <https://huggingface.co/Salesforce/blip2-opt-2.7b>, <https://huggingface.co/Salesforce/blip2-opt-6.7b>
- GPT / Gemini: <https://platform.openai.com/docs/models>, <https://ai.google.dev/gemini-api/docs/models>
- OpenRouter models: <https://openrouter.ai/models>

## How dispatch works

`ModelFactory` first matches the OpenRouter ids above exactly; otherwise it parses the id into
a family + size and instantiates that family's wrapper
with the requested `mode` / `quant` / `temperature`. Coverage: every family has
`default` + `reasoning`; local families add `temp`; `quant` exists for blip2 / internvl /
llava (BNB 4/8-bit) and qwen (AWQ checkpoints, e.g. `Qwen/Qwen2.5-VL-7B-Instruct-AWQ`). To add a model, see [`../../multibbq/models/README.md`](../../multibbq/models/README.md).
