"""FastAPI backend for RAG/LLM governance evaluation."""

from __future__ import annotations

from typing import Any

from llmops_governance.config.settings import Settings
from llmops_governance.evaluators.rag_evaluator import RAGEvaluationPipeline
from llmops_governance.governance.readiness import assess_readiness
from llmops_governance.reports.generator import generate_reports
from llmops_governance.utils import to_plain_data

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
except Exception:  # pragma: no cover - exercised only in dependency-free import checks.
    FastAPI = None  # type: ignore
    HTTPException = Exception  # type: ignore

    class BaseModel:  # type: ignore
        pass


class EvaluationRequest(BaseModel):
    question: str | None = None
    model_mode: str = "grounded"
    limit: int | None = None


def health() -> dict[str, str]:
    return {"status": "ok", "service": "llmops-governance-api"}


def _run_suite(model_mode: str = "grounded", limit: int | None = None) -> dict[str, Any]:
    settings = Settings.from_env()
    pipeline = RAGEvaluationPipeline(settings)
    run = pipeline.run(model_mode=model_mode, limit=limit)
    paths = generate_reports(run, settings)
    decision = assess_readiness(run, settings.thresholds)
    run.governance_status = decision.status
    return {"run": to_plain_data(run), "decision": to_plain_data(decision), "reports": {k: str(v) for k, v in paths.items()}}


if FastAPI is not None:
    app = FastAPI(
        title="Enterprise LLMOps AI Governance Platform",
        description="Evaluate RAG/LLM systems for groundedness, security, privacy, and governance readiness.",
        version="0.1.0",
    )

    @app.get("/")
    def root() -> dict[str, str]:
        return {"message": "Enterprise LLMOps AI Governance Platform", "docs": "/docs"}

    @app.get("/health")
    def health_endpoint() -> dict[str, str]:
        return health()

    @app.post("/evaluate-question")
    def evaluate_question(request: EvaluationRequest) -> dict[str, Any]:
        if not request.question:
            raise HTTPException(status_code=400, detail="question is required")
        pipeline = RAGEvaluationPipeline(Settings.from_env())
        run = pipeline.evaluate_question(request.question, model_mode=request.model_mode)
        return to_plain_data(run)

    @app.post("/run-evaluation")
    def run_evaluation(request: EvaluationRequest) -> dict[str, Any]:
        return _run_suite(model_mode=request.model_mode, limit=request.limit)

    @app.post("/run-gate")
    def run_gate(request: EvaluationRequest) -> dict[str, Any]:
        result = _run_suite(model_mode=request.model_mode, limit=request.limit)
        decision = result["decision"]
        return {"status": decision["status"], "failed_rules": decision["failed_rules"], "summary": result["run"]["summary"]}

    @app.get("/latest-results")
    def latest_results() -> dict[str, Any]:
        from llmops_governance.utils import read_json

        path = Settings.from_env().generated_reports_dir / "latest_run.json"
        return read_json(path, default={"message": "No evaluation run has been generated yet."})

    @app.get("/governance-report")
    def governance_report() -> dict[str, str]:
        path = Settings.from_env().generated_reports_dir / "governance_report.md"
        return {"path": str(path), "content": path.read_text(encoding="utf-8") if path.exists() else ""}

    @app.get("/risk-register")
    def risk_register() -> dict[str, str]:
        path = Settings.from_env().generated_reports_dir / "risk_register.csv"
        return {"path": str(path), "content": path.read_text(encoding="utf-8") if path.exists() else ""}

    @app.get("/model-card")
    def model_card() -> dict[str, str]:
        path = Settings.from_env().generated_reports_dir / "model_card.md"
        return {"path": str(path), "content": path.read_text(encoding="utf-8") if path.exists() else ""}

    @app.get("/system-card")
    def system_card() -> dict[str, str]:
        path = Settings.from_env().generated_reports_dir / "system_card.md"
        return {"path": str(path), "content": path.read_text(encoding="utf-8") if path.exists() else ""}

    @app.get("/traces/{run_id}")
    def traces(run_id: str) -> dict[str, Any]:
        from llmops_governance.utils import read_json

        path = Settings.from_env().generated_reports_dir / "traces.json"
        traces_payload = read_json(path, default=[])
        return {"run_id": run_id, "traces": [trace for trace in traces_payload if trace.get("run_id") == run_id]}
else:
    class OfflineApp:
        """Fallback object so imports still succeed before FastAPI is installed."""

        title = "Enterprise LLMOps AI Governance Platform"

    app = OfflineApp()

