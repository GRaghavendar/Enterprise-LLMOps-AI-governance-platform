"""Offline model provider used for local demos and tests."""

from __future__ import annotations

from time import perf_counter

from llmops_governance.schemas.evaluation import ModelResponse
from llmops_governance.utils import tokenize


class MockProvider:
    provider_name = "mock"

    def __init__(self, model: str = "mock-governance-model"):
        self.model = model

    def generate(self, prompt: str, **kwargs: object) -> ModelResponse:
        start = perf_counter()
        text = self._mock_text(prompt)
        latency_ms = int((perf_counter() - start) * 1000) + 8
        token_estimate = len(tokenize(prompt)) + len(tokenize(text))
        return ModelResponse(
            text=text,
            provider=self.provider_name,
            model=self.model,
            latency_ms=latency_ms,
            token_estimate=token_estimate,
            cost_estimate=0.0,
            raw_metadata={"mode": "offline_mock"},
        )

    def _mock_text(self, prompt: str) -> str:
        lower = prompt.lower()
        if any(marker in lower for marker in ["ignore previous", "reveal system", "api key", "private key"]):
            return "I cannot comply with requests to override instructions, reveal hidden prompts, or expose secrets."
        if "not enough information" in lower or "out of scope" in lower:
            return "The provided policy context does not contain enough information to answer that safely."
        return "Based on the retrieved policy context, the request should follow the documented approval, escalation, and audit requirements."

