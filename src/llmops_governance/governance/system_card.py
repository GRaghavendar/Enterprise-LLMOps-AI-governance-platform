"""System card generation."""

from __future__ import annotations

from llmops_governance.schemas.evaluation import EvaluationRunResult
from llmops_governance.schemas.governance import GovernanceDecision


def generate_system_card(run: EvaluationRunResult, decision: GovernanceDecision) -> str:
    return f"""# System Card: Enterprise LLMOps AI Governance Platform

## System Purpose
Evaluate RAG and LLM applications before production deployment using deterministic metrics, security scanners, governance rules, and optional LLM-as-judge review.

## Architecture
The platform loads synthetic policy documents, retrieves local context with TF-IDF, evaluates responses, scans for injection and sensitive-data risks, and generates audit-ready reports.

## Governance Decision
- Status: {decision.status}
- Summary: {decision.leadership_summary}

## Traceability
Each evaluation item includes run ID, trace ID, dataset version, prompt version, model mode, retrieved sources, metric scores, failure reasons, and recommendations.

## Data Privacy
All included data is synthetic. The project must not be run with real PII, PHI, PCI, secrets, credentials, employer records, or customer records.

## Human Oversight
High-risk or blocked decisions require a human governance reviewer before production release.
"""

