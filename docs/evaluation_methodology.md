# Evaluation Methodology

The project uses transparent deterministic metrics by default.

## RAG Metrics

- `retrieval_score`: average top-k retrieval similarity.
- `source_match_score`: whether the expected policy source appears in retrieved context.
- `context_relevance_score`: retrieval evidence using query overlap, source match, and expected-answer recall.
- `context_precision_score`: share of retrieved chunks from the expected source.
- `context_recall_score`: expected-answer token coverage in retrieved context.
- `answer_relevance_score`: answer overlap with the question and expected answer.
- `groundedness_score`: answer support from retrieved context, with explicit credit for safe refusals.
- `faithfulness_score`: overlap with expected answer and retrieved context.
- `citation_coverage_score`: whether required policy citations are present.
- `unsupported_claim_score`: share of answer tokens not supported by retrieved context.
- `hallucination_risk_score`: weighted risk from low groundedness, low faithfulness, and unsupported claims.

## Security Metrics

- `prompt_injection_risk_score`
- `pii_secrets_risk_score`
- `unsafe_output_risk_score`
- `overall_risk_score`

The scanner discounts detected adversarial prompts when the answer safely refuses the attack. Unsafe mode intentionally leaks fake placeholder data to prove the gate can block failures.

