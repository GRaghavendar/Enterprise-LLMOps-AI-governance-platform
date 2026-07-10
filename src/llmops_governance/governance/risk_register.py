"""Risk register generation."""

from __future__ import annotations

from llmops_governance.config.thresholds import Thresholds
from llmops_governance.schemas.evaluation import EvaluationRunResult
from llmops_governance.schemas.governance import RiskRegisterItem


def build_risk_register(run: EvaluationRunResult, thresholds: Thresholds) -> list[RiskRegisterItem]:
    risks: list[RiskRegisterItem] = []
    metric_specs = [
        ("hallucination", "accuracy_and_reliability", run.summary["average_hallucination_risk"], thresholds.maximum_hallucination_risk, "Reduce unsupported claims and strengthen citations."),
        ("prompt_injection", "security", run.summary["average_prompt_injection_risk"], thresholds.maximum_prompt_injection_risk, "Add stronger injection refusal and retrieved-context sanitization."),
        ("pii_secrets", "privacy", run.summary["average_pii_secrets_risk"], thresholds.maximum_pii_secrets_risk, "Add output redaction and secret scanning before response release."),
        ("context_relevance", "retrieval_quality", 1 - float(run.summary["average_context_relevance"]), 1 - thresholds.minimum_context_relevance, "Improve chunking and retrieval ranking."),
        ("citation_coverage", "transparency", 1 - float(run.summary["average_citation_coverage"]), 1 - thresholds.minimum_citation_coverage, "Require source citations in policy answers."),
    ]
    for index, (metric, category, score, threshold, mitigation) in enumerate(metric_specs, start=1):
        severity = "high" if float(score) > float(threshold) else "low"
        risks.append(
            RiskRegisterItem(
                risk_id=f"RISK-{index:03d}",
                category=category,
                severity=severity,
                description=f"{metric.replace('_', ' ').title()} measured at {float(score):.2f} against threshold {float(threshold):.2f}.",
                metric=metric,
                score=round(float(score), 4),
                threshold=round(float(threshold), 4),
                mitigation=mitigation,
                status="open" if severity == "high" else "monitoring",
            )
        )
    return risks

