"""OpenRouter wrapper for the frontier API models added in v1.1.

GPT-6-sol, GPT-6-Luna, Claude Opus 5.5, Gemini 3.8 Flash, Grok 4.7 and Muse Spark 1.3
were evaluated through OpenRouter's OpenAI-compatible Chat Completions API with the
settings below, which follow the paper's API-model protocol (see gpt.py, gemini.py):

    answer-only mode ('default'): the lowest reasoning effort the model allows and a
        short output cap. GPT-6 accepts effort 'none' (0 reasoning tokens) and keeps
        the 20-token cap of GPT-5; the other four cannot disable reasoning on
        OpenRouter ("Reasoning is mandatory for this endpoint"), so they use effort
        'minimal' with a 512-token cap (1024 for Grok and Muse, whose hidden
        reasoning reached ~550 tokens), so the answer is not cut off.
    reasoning mode: effort 'medium', 3000 output tokens, and the think rule appended
        to the system message (as for GPT-5 and Gemini 2.5).

The system instruction is sent as a system message. Temperature is 0 where the
provider accepts it (Gemini, Grok, Muse, as for Gemini 2.5 in the paper), unsupported
for GPT-6 (as for GPT-5), and left at the provider default for Claude, whose thinking
is always on. GPT-6 gets the image at detail 'low' (as GPT-4o / GPT-5); the others get
the full image. Claude returns a content filter for the paper's two reasoning system
prompts, so Claude has no reasoning results.

Model ids are the OpenRouter ids (e.g. "openai/gpt-6-sol"); `run` writes results to
results/<data_id>_<token>/<model id>/, the layout of MLL-Lab/MultiBBQ-results.
Needs OPENROUTER_API_KEY.
"""
import base64
import logging
import os
import random
import time

from .base import BaseModel

# OpenRouter id -> settings; name/size give the result file prefix (e.g. gpt_sol_...)
OPENROUTER_MODELS = {
    "openai/gpt-6-sol": dict(
        name="gpt", size="sol", image_detail="low", temperature=None,
        reasoning={"default": {"effort": "none"}, "reasoning": {"effort": "medium"}},
        max_tokens={"default": 20, "reasoning": 3000},
    ),
    "openai/gpt-6-luna": dict(
        name="gpt", size="luna", image_detail="low", temperature=None,
        reasoning={"default": {"effort": "none"}, "reasoning": {"effort": "medium"}},
        max_tokens={"default": 20, "reasoning": 3000},
    ),
    "anthropic/claude-opus-5.5": dict(
        name="claude", size="5.5", image_detail=None, temperature=None,
        reasoning={"default": {"effort": "minimal"}, "reasoning": {"effort": "medium"}},
        max_tokens={"default": 512, "reasoning": 3000},
    ),
    "google/gemini-3.8-flash": dict(
        name="gemini", size="3.8_flash", image_detail=None, temperature=0,
        reasoning={"default": {"effort": "minimal"}, "reasoning": {"effort": "medium"}},
        max_tokens={"default": 512, "reasoning": 3000},
    ),
    "x-ai/grok-4.7": dict(
        name="grok", size="4.7", image_detail=None, temperature=0,
        reasoning={"default": {"effort": "minimal"}, "reasoning": {"effort": "medium"}},
        max_tokens={"default": 1024, "reasoning": 3000},
    ),
    "meta/muse-spark-1.3": dict(
        name="muse", size="spark_1.3", image_detail=None, temperature=0,
        reasoning={"default": {"effort": "minimal"}, "reasoning": {"effort": "medium"}},
        max_tokens={"default": 1024, "reasoning": 3000},
    ),
}


class OpenRouterModel(BaseModel):
    def __init__(self, model_id, mode="default", quant=False, temperature=None):
        if quant or mode == "temp":
            raise ValueError("OpenRouterModel supports only 'default' / 'reasoning' modes")
        if model_id not in OPENROUTER_MODELS:
            raise ValueError(f"Unsupported OpenRouter model: {model_id!r}")
        super().__init__(model_id, mode=mode, quant=quant, temperature=temperature)
        import openai
        from openai import OpenAI

        self._openai = openai
        self.model_name = model_id
        self.spec = OPENROUTER_MODELS[model_id]
        self.name, self.size = self.spec["name"], self.spec["size"]
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1",
                             api_key=os.environ["OPENROUTER_API_KEY"], max_retries=0, timeout=300)

    def run(self, image_path: str, user_prompt: str, system_msg: str):
        if self.reasoning:
            system_msg = f"{system_msg}\n{self.think_rule}"
        with open(image_path, "rb") as f:
            image = {"url": "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")}
        if self.spec["image_detail"]:
            image["detail"] = self.spec["image_detail"]
        kwargs = dict(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": [{"type": "text", "text": user_prompt},
                                             {"type": "image_url", "image_url": image}]},
            ],
            max_tokens=self.spec["max_tokens"][self.mode],
            extra_body={"reasoning": self.spec["reasoning"][self.mode]},
        )
        if self.spec["temperature"] is not None:
            kwargs["temperature"] = self.spec["temperature"]

        errors = self._openai
        for attempt in range(8):
            try:
                resp = self.client.chat.completions.create(**kwargs)
            except (errors.RateLimitError, errors.APITimeoutError, errors.APIConnectionError,
                    errors.InternalServerError) as e:
                wait = min(120, 2 * 2 ** attempt) * (0.8 + 0.4 * random.random())
                logging.info(f"[retry {attempt}] {type(e).__name__}: {e}; sleep {wait:.0f}s")
                time.sleep(wait)
                continue
            except errors.APIStatusError as e:  # e.g. a content filter: no answer
                logging.info(f"[api error] {e.status_code}: {e.message}")
                return None
            if not resp.choices:  # OpenRouter reports some upstream failures in-band
                time.sleep(2 * 2 ** attempt)
                continue
            text = resp.choices[0].message.content
            return text.strip() if text and text.strip() else None
        return None
