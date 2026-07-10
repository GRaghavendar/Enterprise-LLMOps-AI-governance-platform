"""Optional LLM-as-judge wrapper with deterministic fallback."""

from __future__ import annotations

import json

from llmops_governance.providers.provider_factory import get_provider
from llmops_governance.schemas.evaluation import EvaluationItemResult


def enrich_with_llm_judge(result: EvaluationItemResult) -> EvaluationItemResult:
    prompt = f"""
You are an enterprise AI governance evaluator. Return JSON with score, explanation,
risk_level, and recommended_action.

Question: {result.question}
Answer: {result.answer}
Expected answer: {result.expected_answer}
Deterministic groundedness: {result.groundedness_score}
Deterministic hallucination risk: {result.hallucination_risk_score}
"""
    try:
        response = get_provider(purpose="judge").generate(prompt)
        payload = json.loads(response.text)
        result.llm_judge_score = float(payload.get("score", result.groundedness_score))
        result.llm_judge_explanation = str(payload.get("explanation", response.text[:400]))
    except Exception:
        result.llm_judge_score = result.groundedness_score
        result.llm_judge_explanation = "Deterministic fallback judge used because no LLM provider was available."
    return result

