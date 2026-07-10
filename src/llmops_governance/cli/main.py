"""CLI for evaluation, gates, reports, API, and dashboard commands."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from llmops_governance.config.settings import Settings
from llmops_governance.data.sample_data_generator import generate_sample_assets
from llmops_governance.evaluators.rag_evaluator import RAGEvaluationPipeline
from llmops_governance.governance.readiness import assess_readiness
from llmops_governance.reports.generator import generate_reports
from llmops_governance.utils import write_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="llmops-governance",
        description="Offline-first LLMOps governance evaluation platform.",
    )
    subparsers = parser.add_subparsers(dest="command")

    evaluate = subparsers.add_parser("evaluate", help="Run the synthetic RAG evaluation suite.")
    evaluate.add_argument("--model-mode", default="grounded", choices=["grounded", "weak", "unsafe", "llm"])
    evaluate.add_argument("--limit", type=int, default=None)

    compare = subparsers.add_parser("compare-models", help="Compare grounded, weak, and unsafe response modes.")
    compare.add_argument("--limit", type=int, default=None)

    gate = subparsers.add_parser("run-gate", help="Run CI/CD governance gate and exit non-zero when blocked.")
    gate.add_argument("--model-mode", default="grounded", choices=["grounded", "weak", "unsafe", "llm"])
    gate.add_argument("--limit", type=int, default=None)

    reports = subparsers.add_parser("generate-reports", help="Generate report artifacts from a fresh evaluation.")
    reports.add_argument("--model-mode", default="grounded", choices=["grounded", "weak", "unsafe", "llm"])
    reports.add_argument("--limit", type=int, default=None)

    subparsers.add_parser("generate-data", help="Generate synthetic policy documents and datasets.")
    subparsers.add_parser("serve-api", help="Start FastAPI with uvicorn.")
    subparsers.add_parser("dashboard", help="Start the Streamlit dashboard.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0

    settings = Settings.from_env()

    if args.command == "generate-data":
        generate_sample_assets(settings.root_dir)
        print(f"Synthetic assets generated under {settings.root_dir}")
        return 0

    if args.command == "evaluate":
        run = RAGEvaluationPipeline(settings).run(model_mode=args.model_mode, limit=args.limit)
        generate_reports(run, settings)
        print_summary(run)
        print(f"Reports written to {settings.generated_reports_dir}")
        return 0

    if args.command == "compare-models":
        rows = []
        for mode in ["grounded", "weak", "unsafe"]:
            run = RAGEvaluationPipeline(settings).run(model_mode=mode, limit=args.limit)
            decision = assess_readiness(run, settings.thresholds)
            rows.append(
                {
                    "model_mode": mode,
                    "governance_status": decision.status,
                    "pass_rate": run.summary["pass_rate"],
                    "average_groundedness": run.summary["average_groundedness"],
                    "average_hallucination_risk": run.summary["average_hallucination_risk"],
                    "average_prompt_injection_risk": run.summary["average_prompt_injection_risk"],
                    "average_pii_secrets_risk": run.summary["average_pii_secrets_risk"],
                }
            )
        output_path = settings.generated_reports_dir / "model_comparison.csv"
        write_csv(output_path, rows)
        write_csv(settings.sample_reports_dir / "model_comparison.csv", rows)
        print(f"Model comparison written to {output_path}")
        return 0

    if args.command == "run-gate":
        run = RAGEvaluationPipeline(settings).run(model_mode=args.model_mode, limit=args.limit)
        paths = generate_reports(run, settings)
        decision = assess_readiness(run, settings.thresholds)
        print_summary(run)
        print(f"Governance status: {decision.status}")
        print(f"Gate result: {paths['latest_gate_result']}")
        if decision.status == "blocked":
            return 2
        if decision.status == "needs_review":
            return 1
        return 0

    if args.command == "generate-reports":
        run = RAGEvaluationPipeline(settings).run(model_mode=args.model_mode, limit=args.limit)
        paths = generate_reports(run, settings)
        for name, path in paths.items():
            print(f"{name}: {path}")
        return 0

    if args.command == "serve-api":
        return _run_subprocess([sys.executable, "-m", "uvicorn", "llmops_governance.api.main:app", "--reload"])

    if args.command == "dashboard":
        dashboard_path = Path(settings.root_dir / "app" / "streamlit_app.py")
        return _run_subprocess([sys.executable, "-m", "streamlit", "run", str(dashboard_path)])

    parser.print_help()
    return 0


def print_summary(run) -> None:
    print(f"Run ID: {run.run_id}")
    print(f"Mode: {run.model_mode}")
    print(f"Total cases: {run.summary['total_cases']}")
    print(f"Pass rate: {run.summary['pass_rate']}")
    print(f"Groundedness: {run.summary['average_groundedness']}")
    print(f"Hallucination risk: {run.summary['average_hallucination_risk']}")
    print(f"Prompt injection risk: {run.summary['average_prompt_injection_risk']}")
    print(f"PII/secrets risk: {run.summary['average_pii_secrets_risk']}")


def _run_subprocess(command: list[str]) -> int:
    try:
        completed = subprocess.run(command, check=False)
        return int(completed.returncode)
    except FileNotFoundError as exc:
        print(f"Unable to start command: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
