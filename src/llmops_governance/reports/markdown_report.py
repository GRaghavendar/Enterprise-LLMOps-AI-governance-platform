"""Markdown governance report generation."""

from __future__ import annotations

from llmops_governance.schemas.evaluation import EvaluationRunResult
from llmops_governance.schemas.governance import GovernanceDecision, RiskRegisterItem


def evaluation_summary_markdown(run: EvaluationRunResult, decision: GovernanceDecision) -> str:
    top_failures = [item for item in run.items if item.pass_fail == "fail"][:10]
    failed_rows = "\n".join(
        f"| {item.question_id} | {item.test_type} | {item.risk_category} | {', '.join(item.failure_reasons)} |"
        for item in top_failures
    )
    if not failed_rows:
        failed_rows = "| None | None | None | No failed cases in this run. |"

    return f"""# Evaluation Summary

## Executive Snapshot
- Run ID: `{run.run_id}`
- Timestamp: {run.evaluation_timestamp}
- Governance status: **{decision.status}**
- Total cases: {run.summary['total_cases']}
- Pass rate: {run.summary['pass_rate']}
- Average groundedness: {run.summary['average_groundedness']}
- Average retrieval score: {run.summary['average_retrieval_score']}
- Average citation coverage: {run.summary['average_citation_coverage']}
- Average hallucination risk: {run.summary['average_hallucination_risk']}
- Average prompt injection risk: {run.summary['average_prompt_injection_risk']}
- Average PII/secrets risk: {run.summary['average_pii_secrets_risk']}

## Leadership Summary
{decision.leadership_summary}

## Top Failed Cases
| Question ID | Test Type | Risk Category | Failure Reasons |
| --- | --- | --- | --- |
{failed_rows}
"""


def governance_report_markdown(
    run: EvaluationRunResult,
    decision: GovernanceDecision,
    risks: list[RiskRegisterItem],
) -> str:
    checklist_rows = "\n".join(
        f"| {item['control']} | {item['status']} |" for item in decision.checklist
    )
    category_rows = "\n".join(
        f"| {category.replace('_', ' ').title()} | {score:.2f} |" for category, score in decision.category_scores.items()
    )
    risk_rows = "\n".join(
        f"| {risk.risk_id} | {risk.category} | {risk.severity} | {risk.score:.2f} | {risk.mitigation} |"
        for risk in risks
    )
    mitigations = "\n".join(f"- {item}" for item in decision.mitigation_recommendations)
    return f"""# Governance Report

## Decision
**{decision.status.upper()}**

{decision.leadership_summary}

## Release Gate Checklist
| Control | Status |
| --- | --- |
{checklist_rows}

## Category Scores
| Category | Score |
| --- | ---: |
{category_rows}

## Risk Register
| Risk ID | Category | Severity | Score | Mitigation |
| --- | --- | --- | ---: | --- |
{risk_rows}

## Mitigation Recommendations
{mitigations}

## Traceability
Run `{run.run_id}` evaluated dataset `{run.dataset_version}` with prompt version `{run.prompt_version}` and model version `{run.model_version}`.
"""

