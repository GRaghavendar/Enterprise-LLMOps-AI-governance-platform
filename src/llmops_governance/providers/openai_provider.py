"""Optional OpenAI provider adapter.

The base project never requires paid API calls. This adapter is used only when
OPENAI_API_KEY is present and ENABLE_LLM_JUDGE=true or LLM_PROVIDER=openai.
"""

from __future__ import annotations

import json
import os
import time
from urllib import request

from llmops_governance.schemas.evaluation import ModelResponse
from llmops_governance.utils import tokenize


class OpenAIProvider:
    provider_name = "openai"

    def __init__(self, model: str):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY", "")

    @property
    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate(self, prompt: str, **kwargs: object) -> ModelResponse:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured.")
        start = time.perf_counter()
        payload = json.dumps({"model": self.model, "input": prompt}).encode("utf-8")
        req = request.Request(
            "https://api.openai.com/v1/responses",
            data=payload,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=30) as response:
            raw = json.loads(response.read().decode("utf-8"))
        text = self._extract_text(raw)
        latency_ms = int((time.perf_counter() - start) * 1000)
        usage = raw.get("usage") or {}
        token_estimate = int(usage.get("total_tokens") or len(tokenize(prompt)) + len(tokenize(text)))
        return ModelResponse(
            text=text,
            provider=self.provider_name,
            model=self.model,
            latency_ms=latency_ms,
            token_estimate=token_estimate,
            cost_estimate=0.0,
            raw_metadata={"usage": usage},
        )

    def _extract_text(self, raw: dict[str, object]) -> str:
        if isinstance(raw.get("output_text"), str):
            return str(raw["output_text"])
        output = raw.get("output")
        if isinstance(output, list):
            parts: list[str] = []
            for item in output:
                if isinstance(item, dict):
                    content = item.get("content")
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and isinstance(block.get("text"), str):
                                parts.append(block["text"])
            if parts:
                return "\n".join(parts)
        return ""

