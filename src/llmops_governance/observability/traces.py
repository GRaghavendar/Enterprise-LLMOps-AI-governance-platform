"""Trace construction helpers."""

from __future__ import annotations

from llmops_governance.schemas.evaluation import EvaluationRunResult
from llmops_governance.schemas.traces import EvaluationTrace


def build_traces(run: EvaluationRunResult) -> list[EvaluationTrace]:
    traces: list[EvaluationTrace] = []
    for item in run.items:
        traces.append(
            EvaluationTrace(
                trace_id=item.trace_id,
                run_id=run.run_id,
                question_id=item.question_id,
                prompt=item.question,
                response=item.answer,
                retrieved_sources=[chunk.source_document for chunk in item.retrieval_context],
                model_name=run.model_version,
                provider=run.provider,
                latency_ms=0,
                token_estimate=len(item.question.split()) + len(item.answer.split()),
                cost_estimate=0.0,
                app_version=run.app_version,
                prompt_version=run.prompt_version,
                dataset_version=run.dataset_version,
                model_version=run.model_version,
                evaluation_timestamp=run.evaluation_timestamp,
            )
        )
    return traces

