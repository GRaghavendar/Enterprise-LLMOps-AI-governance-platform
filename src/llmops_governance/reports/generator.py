"""Generate all project report artifacts."""

from __future__ import annotations

import shutil
from pathlib import Path

from llmops_governance.config.settings import Settings
from llmops_governance.governance.model_card import generate_model_card
from llmops_governance.governance.readiness import assess_readiness
from llmops_governance.governance.risk_register import build_risk_register
from llmops_governance.governance.system_card import generate_system_card
from llmops_governance.observability.audit_log import build_audit_events
from llmops_governance.observability.traces import build_traces
from llmops_governance.reports.html_report import governance_report_html
from llmops_governance.reports.markdown_report import evaluation_summary_markdown, governance_report_markdown
from llmops_governance.schemas.evaluation import EvaluationRunResult
from llmops_governance.utils import ensure_dir, to_plain_data, write_csv, write_json, write_jsonl


def generate_reports(
    run: EvaluationRunResult,
    settings: Settings | None = None,
    write_sample_copy: bool = True,
) -> dict[str, Path]:
    settings = settings or Settings.from_env()
    output_dir = ensure_dir(settings.generated_reports_dir)
    sample_dir = ensure_dir(settings.sample_reports_dir)
    decision = assess_readiness(run, settings.thresholds)
    run.governance_status = decision.status
    risks = build_risk_register(run, settings.thresholds)

    paths: dict[str, Path] = {
        "evaluation_summary": output_dir / "evaluation_summary.md",
        "governance_report_md": output_dir / "governance_report.md",
        "governance_report_html": output_dir / "governance_report.html",
        "model_card": output_dir / "model_card.md",
        "system_card": output_dir / "system_card.md",
        "evaluation_results": output_dir / "evaluation_results.csv",
        "model_comparison": output_dir / "model_comparison.csv",
        "risk_register": output_dir / "risk_register.csv",
        "audit_log": output_dir / "audit_log.jsonl",
        "latest_gate_result": output_dir / "latest_gate_result.json",
        "latest_run": output_dir / "latest_run.json",
        "traces": output_dir / "traces.json",
    }

    paths["evaluation_summary"].write_text(evaluation_summary_markdown(run, decision), encoding="utf-8")
    paths["governance_report_md"].write_text(governance_report_markdown(run, decision, risks), encoding="utf-8")
    paths["governance_report_html"].write_text(governance_report_html(run, decision, risks), encoding="utf-8")
    paths["model_card"].write_text(generate_model_card(run), encoding="utf-8")
    paths["system_card"].write_text(generate_system_card(run, decision), encoding="utf-8")
    write_csv(paths["evaluation_results"], flatten_items(run))
    write_csv(paths["model_comparison"], model_comparison_rows(run))
    write_csv(paths["risk_register"], [to_plain_data(risk) for risk in risks])
    write_jsonl(paths["audit_log"], build_audit_events(run, decision))
    write_json(paths["latest_gate_result"], {"run_id": run.run_id, "status": decision.status, "summary": run.summary, "failed_rules": decision.failed_rules})
    write_json(paths["latest_run"], run)
    write_json(paths["traces"], build_traces(run))

    if write_sample_copy:
        for path in paths.values():
            if path.suffix in {".md", ".html", ".csv", ".json", ".jsonl"}:
                shutil.copy2(path, sample_dir / path.name)
    return paths


def flatten_items(run: EvaluationRunResult) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in run.items:
        rows.append(
            {
                "run_id": run.run_id,
                "question_id": item.question_id,
                "test_type": item.test_type,
                "severity": item.severity,
                "risk_category": item.risk_category,
                "pass_fail": item.pass_fail,
                "retrieval_score": item.retrieval_score,
                "source_match_score": item.source_match_score,
                "context_relevance_score": item.context_relevance_score,
                "context_precision_score": item.context_precision_score,
                "context_recall_score": item.context_recall_score,
                "answer_relevance_score": item.answer_relevance_score,
                "groundedness_score": item.groundedness_score,
                "faithfulness_score": item.faithfulness_score,
                "citation_coverage_score": item.citation_coverage_score,
                "unsupported_claim_score": item.unsupported_claim_score,
                "hallucination_risk_score": item.hallucination_risk_score,
                "prompt_injection_risk_score": item.prompt_injection_risk_score,
                "pii_secrets_risk_score": item.pii_secrets_risk_score,
                "unsafe_output_risk_score": item.unsafe_output_risk_score,
                "overall_risk_score": item.overall_risk_score,
                "trace_id": item.trace_id,
                "failure_reasons": "; ".join(item.failure_reasons),
                "recommendations": "; ".join(item.recommendations),
            }
        )
    return rows


def model_comparison_rows(run: EvaluationRunResult) -> list[dict[str, object]]:
    return [
        {
            "model_mode": run.model_mode,
            "provider": run.provider,
            "model_version": run.model_version,
            "pass_rate": run.summary["pass_rate"],
            "average_groundedness": run.summary["average_groundedness"],
            "average_hallucination_risk": run.summary["average_hallucination_risk"],
            "average_prompt_injection_risk": run.summary["average_prompt_injection_risk"],
            "governance_status": run.governance_status,
        }
    ]

