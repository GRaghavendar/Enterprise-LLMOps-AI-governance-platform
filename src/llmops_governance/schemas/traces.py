"""Trace schema dataclasses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvaluationTrace:
    trace_id: str
    run_id: str
    question_id: str
    prompt: str
    response: str
    retrieved_sources: list[str]
    model_name: str
    provider: str
    latency_ms: int
    token_estimate: int
    cost_estimate: float
    app_version: str
    prompt_version: str
    dataset_version: str
    model_version: str
    evaluation_timestamp: str

