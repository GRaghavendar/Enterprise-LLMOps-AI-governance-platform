"""JSON report helpers."""

from __future__ import annotations

from pathlib import Path

from llmops_governance.utils import write_json


def write_json_report(path: Path, payload: object) -> None:
    write_json(path, payload)

