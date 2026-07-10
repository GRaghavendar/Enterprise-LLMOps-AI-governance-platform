import os
import unittest

from llmops_governance.config.settings import Settings
from llmops_governance.providers.provider_factory import get_provider


class ProviderFallbackTests(unittest.TestCase):
    def test_mock_provider_without_api_key(self):
        original = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = ""
        try:
            provider = get_provider(Settings.from_env(), purpose="judge")
            self.assertEqual(provider.provider_name, "mock")
        finally:
            if original is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = original

    def test_ollama_provider_falls_back_when_server_unavailable(self):
        settings = Settings(llm_provider="ollama", app_model="qwen3:4b", ollama_base_url="http://127.0.0.1:9")
        provider = get_provider(settings, purpose="app")
        self.assertEqual(provider.provider_name, "mock")


if __name__ == "__main__":
    unittest.main()
