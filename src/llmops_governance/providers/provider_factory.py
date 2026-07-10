"""Provider factory with graceful offline fallback."""

from __future__ import annotations

from llmops_governance.config.settings import Settings
from llmops_governance.providers.mock_provider import MockProvider
from llmops_governance.providers.ollama_provider import OllamaProvider
from llmops_governance.providers.openai_provider import OpenAIProvider


def get_provider(settings: Settings | None = None, purpose: str = "app"):
    settings = settings or Settings.from_env()
    model = settings.app_model if purpose == "app" else settings.eval_judge_model
    provider_name = settings.llm_provider.lower()
    if provider_name == "ollama":
        provider = OllamaProvider(model=model, base_url=settings.ollama_base_url)
        if provider.is_available:
            return provider
    if provider_name == "openai" or settings.enable_llm_judge:
        provider = OpenAIProvider(model=model)
        if provider.is_available:
            return provider
    return MockProvider(model=f"mock-{purpose}-model")
