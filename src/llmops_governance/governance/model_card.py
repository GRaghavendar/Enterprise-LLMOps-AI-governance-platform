"""Model card generation."""

from __future__ import annotations

from llmops_governance.schemas.evaluation import EvaluationRunResult


def generate_model_card(run: EvaluationRunResult) -> str:
    return f"""# Model Card: {run.model_version}

## Intended Use
This synthetic demo evaluates RAG/LLM responses for enterprise policy assistance, governance review, and CI/CD release gates.

## Out-of-Scope Use
The system is not approved for binding legal, financial, medical, employment, or regulated decisions without human review.

## Evaluation Summary
- Dataset version: {run.dataset_version}
- Prompt version: {run.prompt_version}
- Provider: {run.provider}
- Model mode: {run.model_mode}
- Total cases: {run.summary['total_cases']}
- Pass rate: {run.summary['pass_rate']}
- Average groundedness: {run.summary['average_groundedness']}
- Average hallucination risk: {run.summary['average_hallucination_risk']}
- Average prompt injection risk: {run.summary['average_prompt_injection_risk']}
- Average PII/secrets risk: {run.summary['average_pii_secrets_risk']}

## Limitations
Fairness and bias are represented as a readiness checklist only. Real fairness measurement requires production slice data and approved demographic or proxy variables.

## Monitoring Plan
Track pass rate, groundedness, citation coverage, retrieval relevance, prompt injection risk, PII/secrets risk, latency, and evaluation drift by release.
"""

