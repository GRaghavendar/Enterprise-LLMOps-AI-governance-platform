"""Evaluation drift and release-to-release change detection."""

from __future__ import annotations

from llmops_governance.schemas.evaluation import EvaluationRunResult


DRIFT_FIELDS = [
    "pass_rate",
    "average_groundedness",
    "average_hallucination_risk",
    "average_context_relevance",
    "average_prompt_injection_risk",
    "average_pii_secrets_risk",
]


def compare_runs(previous: EvaluationRunResult, current: EvaluationRunResult) -> dict[str, float]:
    return {
        field: round(float(current.summary.get(field, 0.0)) - float(previous.summary.get(field, 0.0)), 4)
        for field in DRIFT_FIELDS
    }

