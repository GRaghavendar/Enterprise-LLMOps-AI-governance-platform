"""Governance decision schema dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GovernanceDecision:
    status: str
    leadership_summary: str
    category_scores: dict[str, float]
    checklist: list[dict[str, str]]
    failed_rules: list[str]
    mitigation_recommendations: list[str]


@dataclass
class RiskRegisterItem:
    risk_id: str
    category: str
    severity: str
    description: str
    metric: str
    score: float
    threshold: float
    mitigation: str
    owner: str = "AI Governance Review Board"
    status: str = "open"

