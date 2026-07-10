"""Audit event helpers."""

from __future__ import annotations

from llmops_governance.schemas.evaluation import EvaluationRunResult
from llmops_governance.schemas.governance import GovernanceDecision
from llmops_governance.utils import utc_now_iso


def build_audit_events(run: EvaluationRunResult, decision: GovernanceDecision) -> list[dict[str, object]]:
    events: list[dict[str, object]] = [
        {
            "timestamp": run.evaluation_timestamp,
            "event_type": "evaluation_run_created",
            "run_id": run.run_id,
            "dataset_version": run.dataset_version,
            "model_version": run.model_version,
            "total_cases": run.summary["total_cases"],
        },
        {
            "timestamp": utc_now_iso(),
            "event_type": "governance_decision_created",
            "run_id": run.run_id,
            "status": decision.status,
            "failed_rules": decision.failed_rules,
        },
    ]
    for item in run.items:
        if item.pass_fail == "fail":
            events.append(
                {
                    "timestamp": utc_now_iso(),
                    "event_type": "failed_case_review_required",
                    "run_id": run.run_id,
                    "trace_id": item.trace_id,
                    "question_id": item.question_id,
                    "risk_category": item.risk_category,
                    "failure_reasons": item.failure_reasons,
                }
            )
    return events

