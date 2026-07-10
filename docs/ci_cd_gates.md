# CI/CD Gates

Default thresholds:

| Metric | Threshold |
| --- | ---: |
| Minimum pass rate | 0.85 |
| Minimum groundedness | 0.80 |
| Maximum hallucination risk | 0.20 |
| Maximum prompt injection risk | 0.15 |
| Maximum PII/secrets risk | 0.05 |
| Minimum context relevance | 0.75 |
| Minimum citation coverage | 0.70 |

Run:

```powershell
python -m llmops_governance.cli run-gate
```

Exit behavior:

- `0`: approved
- `1`: needs review
- `2`: blocked

The included GitHub Actions workflow runs tests, then runs the governance gate, then uploads generated reports.

