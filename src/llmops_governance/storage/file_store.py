"""File-based storage for local runs."""

from __future__ import annotations

from pathlib import Path

from llmops_governance.schemas.evaluation import EvaluationRunResult
from llmops_governance.utils import read_json, write_json


class FileStore:
    def __init__(self, directory: Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def save_run(self, run: EvaluationRunResult) -> Path:
        path = self.directory / f"{run.run_id}.json"
        write_json(path, run)
        write_json(self.directory / "latest_run.json", run)
        return path

    def load_latest(self) -> dict:
        return read_json(self.directory / "latest_run.json", default={})

