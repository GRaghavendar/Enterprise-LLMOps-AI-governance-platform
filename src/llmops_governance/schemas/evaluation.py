"""Evaluation schema dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvalQuestion:
    question_id: str
    question: str
    expected_answer: str
    expected_source: str
    risk_category: str
    test_type: str
    expected_pass_fail: str
    expected_citations_required: bool
    severity: str
    notes: str = ""


@dataclass
class SourceChunk:
    chunk_id: str
    source_document: str
    text: str
    similarity_score: float


@dataclass
class ModelResponse:
    text: str
    provider: str
    model: str
    latency_ms: int
    token_estimate: int
    cost_estimate: float
    raw_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationItemResult:
    question_id: str
    question: str
    answer: str
    expected_answer: str
    expected_source: str
    test_type: str
    severity: str
    risk_category: str
    trace_id: str
    retrieval_context: list[SourceChunk]
    retrieval_score: float
    source_match_score: float
    context_relevance_score: float
    context_precision_score: float
    context_recall_score: float
    answer_relevance_score: float
    groundedness_score: float
    faithfulness_score: float
    citation_coverage_score: float
    unsupported_claim_score: float
    hallucination_risk_score: float
    prompt_injection_risk_score: float
    pii_secrets_risk_score: float
    unsafe_output_risk_score: float
    overall_risk_score: float
    pass_fail: str
    failure_reasons: list[str]
    recommendations: list[str]
    llm_judge_score: float | None = None
    llm_judge_explanation: str | None = None


@dataclass
class EvaluationRunResult:
    run_id: str
    app_version: str
    prompt_version: str
    dataset_version: str
    model_version: str
    provider: str
    model_mode: str
    evaluation_timestamp: str
    items: list[EvaluationItemResult]
    summary: dict[str, float | int | str]
    governance_status: str = "needs_review"

