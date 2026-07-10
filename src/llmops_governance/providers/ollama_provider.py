"""Optional Ollama provider adapter for free local LLM inference."""

from __future__ import annotations

import json
import time
from urllib import error, request

from llmops_governance.schemas.evaluation import ModelResponse
from llmops_governance.utils import tokenize


class OllamaProvider:
    """Generate answers with a local Ollama model.

    Ollama runs on localhost by default, so this provider does not require API
    keys or per-token billing. If Ollama is not running, the provider factory
    falls back to MockProvider.
    """

    provider_name = "ollama"

    def __init__(self, model: str, base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")

    @property
    def is_available(self) -> bool:
        try:
            with request.urlopen(f"{self.base_url}/api/tags", timeout=0.4) as response:
                return 200 <= response.status < 300
        except (OSError, error.URLError, TimeoutError):
            return False

    def generate(self, prompt: str, **kwargs: object) -> ModelResponse:
        start = time.perf_counter()
        payload = json.dumps(
            {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": float(kwargs.get("temperature", 0.1)),
                    "num_predict": int(kwargs.get("num_predict", 450)),
                },
            }
        ).encode("utf-8")
        req = request.Request(
            f"{self.base_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=float(kwargs.get("timeout", 90))) as response:
            raw = json.loads(response.read().decode("utf-8"))
        text = str(raw.get("response", "")).strip()
        latency_ms = int((time.perf_counter() - start) * 1000)
        token_estimate = int(raw.get("prompt_eval_count") or 0) + int(raw.get("eval_count") or 0)
        if token_estimate <= 0:
            token_estimate = len(tokenize(prompt)) + len(tokenize(text))
        return ModelResponse(
            text=text,
            provider=self.provider_name,
            model=self.model,
            latency_ms=latency_ms,
            token_estimate=token_estimate,
            cost_estimate=0.0,
            raw_metadata={
                "base_url": self.base_url,
                "done": raw.get("done"),
                "total_duration": raw.get("total_duration"),
                "prompt_eval_count": raw.get("prompt_eval_count"),
                "eval_count": raw.get("eval_count"),
            },
        )

