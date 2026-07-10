"""HTML report generation."""

from __future__ import annotations

import html

from llmops_governance.schemas.evaluation import EvaluationRunResult
from llmops_governance.schemas.governance import GovernanceDecision, RiskRegisterItem


def governance_report_html(run: EvaluationRunResult, decision: GovernanceDecision, risks: list[RiskRegisterItem]) -> str:
    risk_rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(risk.risk_id)}</td>"
        f"<td>{html.escape(risk.category)}</td>"
        f"<td>{html.escape(risk.severity)}</td>"
        f"<td>{risk.score:.2f}</td>"
        f"<td>{html.escape(risk.mitigation)}</td>"
        "</tr>"
        for risk in risks
    )
    failed_rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(item.question_id)}</td>"
        f"<td>{html.escape(item.test_type)}</td>"
        f"<td>{html.escape(item.risk_category)}</td>"
        f"<td>{html.escape('; '.join(item.failure_reasons))}</td>"
        "</tr>"
        for item in run.items
        if item.pass_fail == "fail"
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>LLMOps Governance Report</title>
  <style>
    body {{ font-family: Inter, Segoe UI, Arial, sans-serif; margin: 32px; color: #17202a; }}
    .status {{ display: inline-block; padding: 6px 10px; border-radius: 6px; background: #eef2ff; font-weight: 700; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 24px 0; }}
    .metric {{ border: 1px solid #d7dde8; border-radius: 8px; padding: 14px; background: #fbfcfe; }}
    .metric span {{ display: block; color: #5d6d7e; font-size: 12px; text-transform: uppercase; }}
    .metric strong {{ font-size: 24px; }}
    table {{ border-collapse: collapse; width: 100%; margin: 18px 0; }}
    th, td {{ border: 1px solid #d7dde8; padding: 9px; text-align: left; vertical-align: top; }}
    th {{ background: #f1f4f9; }}
  </style>
</head>
<body>
  <h1>Enterprise LLMOps AI Governance Report</h1>
  <p class="status">{html.escape(decision.status.upper())}</p>
  <p>{html.escape(decision.leadership_summary)}</p>
  <section class="grid">
    <div class="metric"><span>Pass Rate</span><strong>{run.summary['pass_rate']}</strong></div>
    <div class="metric"><span>Groundedness</span><strong>{run.summary['average_groundedness']}</strong></div>
    <div class="metric"><span>Hallucination Risk</span><strong>{run.summary['average_hallucination_risk']}</strong></div>
    <div class="metric"><span>Injection Risk</span><strong>{run.summary['average_prompt_injection_risk']}</strong></div>
  </section>
  <h2>Risk Register</h2>
  <table><thead><tr><th>Risk ID</th><th>Category</th><th>Severity</th><th>Score</th><th>Mitigation</th></tr></thead><tbody>{risk_rows}</tbody></table>
  <h2>Failed Case Review</h2>
  <table><thead><tr><th>Question</th><th>Type</th><th>Risk</th><th>Reason</th></tr></thead><tbody>{failed_rows or '<tr><td colspan="4">No failed cases.</td></tr>'}</tbody></table>
</body>
</html>
"""

