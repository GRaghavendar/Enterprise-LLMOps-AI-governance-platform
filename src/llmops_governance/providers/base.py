"""Provider interface for generation adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod

from llmops_governance.schemas.evaluation import ModelResponse


class ModelProvider(ABC):
    provider_name = "base"

    @abstractmethod
    def generate(self, prompt: str, **kwargs: object) -> ModelResponse:
        raise NotImplementedError

