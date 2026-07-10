# Model Card: grounded

## Intended Use
This synthetic demo evaluates RAG/LLM responses for enterprise policy assistance, governance review, and CI/CD release gates.

## Out-of-Scope Use
The system is not approved for binding legal, financial, medical, employment, or regulated decisions without human review.

## Evaluation Summary
- Dataset version: synthetic-policy-eval-v1
- Prompt version: governance-rag-prompt-v1
- Provider: deterministic
- Model mode: grounded
- Total cases: 72
- Pass rate: 0.9722
- Average groundedness: 0.9361
- Average hallucination risk: 0.0761
- Average prompt injection risk: 0.0167
- Average PII/secrets risk: 0.0

## Limitations
Fairness and bias are represented as a readiness checklist only. Real fairness measurement requires production slice data and approved demographic or proxy variables.

## Monitoring Plan
Track pass rate, groundedness, citation coverage, retrieval relevance, prompt injection risk, PII/secrets risk, latency, and evaluation drift by release.
