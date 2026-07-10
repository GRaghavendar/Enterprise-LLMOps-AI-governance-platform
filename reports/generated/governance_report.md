# Governance Report

## Decision
**APPROVED**

The evaluated RAG system meets the configured governance release gate.

## Release Gate Checklist
| Control | Status |
| --- | --- |
| Pass rate meets threshold | pass |
| Groundedness meets threshold | pass |
| Hallucination risk below threshold | pass |
| Prompt injection risk below threshold | pass |
| PII/secrets risk below threshold | pass |
| Retrieval quality meets threshold | pass |
| Citation coverage meets threshold | pass |

## Category Scores
| Category | Score |
| --- | ---: |
| Accuracy And Reliability | 0.93 |
| Security | 0.98 |
| Privacy | 1.00 |
| Transparency | 1.00 |
| Monitoring Readiness | 0.90 |
| Human Escalation Readiness | 0.84 |
| Auditability | 0.92 |
| Data Governance | 0.88 |
| Deployment Risk | 0.97 |
| Fairness Bias Review Readiness | 0.50 |

## Risk Register
| Risk ID | Category | Severity | Score | Mitigation |
| --- | --- | --- | ---: | --- |
| RISK-001 | accuracy_and_reliability | low | 0.08 | Reduce unsupported claims and strengthen citations. |
| RISK-002 | security | low | 0.02 | Add stronger injection refusal and retrieved-context sanitization. |
| RISK-003 | privacy | low | 0.00 | Add output redaction and secret scanning before response release. |
| RISK-004 | retrieval_quality | low | 0.14 | Improve chunking and retrieval ranking. |
| RISK-005 | transparency | low | 0.00 | Require source citations in policy answers. |

## Mitigation Recommendations
- Continue monitoring evaluation drift and review failed edge cases after each release.

## Traceability
Run `run_bbe37cf275a2` evaluated dataset `synthetic-policy-eval-v1` with prompt version `governance-rag-prompt-v1` and model version `grounded`.
