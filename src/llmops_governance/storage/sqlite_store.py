"""Minimal SQLite storage adapter for teams that want relational run metadata."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from llmops_governance.schemas.evaluation import EvaluationRunResult


class SQLiteStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _init(self) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS evaluation_runs (
                    run_id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    model_version TEXT,
                    pass_rate REAL,
                    governance_status TEXT
                )
                """
            )

    def save_run_metadata(self, run: EvaluationRunResult) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO evaluation_runs VALUES (?, ?, ?, ?, ?)",
                (
                    run.run_id,
                    run.evaluation_timestamp,
                    run.model_version,
                    float(run.summary["pass_rate"]),
                    run.governance_status,
                ),
            )

