"""Runtime settings loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from llmops_governance.config.thresholds import Thresholds
from llmops_governance.utils import project_root


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    llm_provider: str = "mock"
    enable_llm_judge: bool = False
    eval_judge_model: str = "gpt-5.6-sol"
    app_model: str = "gpt-5.6-terra"
    batch_eval_model: str = "gpt-5.6-luna"
    embedding_model: str = "text-embedding-3-large"
    ollama_base_url: str = "http://localhost:11434"
    default_evaluation_mode: str = "deterministic"
    openai_api_key: str = ""
    root_dir: Path = project_root()
    thresholds: Thresholds = Thresholds()

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            llm_provider=os.getenv("LLM_PROVIDER", "mock"),
            enable_llm_judge=_bool_env("ENABLE_LLM_JUDGE", False),
            eval_judge_model=os.getenv("EVAL_JUDGE_MODEL", "gpt-5.6-sol"),
            app_model=os.getenv("APP_MODEL", "gpt-5.6-terra"),
            batch_eval_model=os.getenv("BATCH_EVAL_MODEL", "gpt-5.6-luna"),
            embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-large"),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            default_evaluation_mode=os.getenv("DEFAULT_EVALUATION_MODE", "deterministic"),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            root_dir=project_root(),
            thresholds=Thresholds.from_env(),
        )

    @property
    def sample_data_dir(self) -> Path:
        return self.root_dir / "data" / "sample"

    @property
    def knowledge_base_dir(self) -> Path:
        return self.root_dir / "knowledge_base" / "policies"

    @property
    def generated_reports_dir(self) -> Path:
        return self.root_dir / "reports" / "generated"

    @property
    def sample_reports_dir(self) -> Path:
        return self.root_dir / "reports" / "sample"
