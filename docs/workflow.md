# Workflow

1. Generate synthetic policy documents and datasets.
2. Retrieve top-k policy chunks with local TF-IDF.
3. Generate answers in one of four modes: `grounded`, `weak`, `unsafe`, or `llm`.
4. Score groundedness, faithfulness, retrieval quality, citation coverage, unsupported claims, and hallucination risk.
5. Scan prompts, context, and responses for prompt injection, PII, secrets, and unsafe output.
6. Apply governance thresholds.
7. Produce JSON, CSV, Markdown, HTML, model card, system card, risk register, and audit log artifacts.
8. Fail CI/CD if the gate returns `needs_review` or `blocked`.

## Manual Evaluation Playground

The Streamlit dashboard includes a single-question playground. It uses the same retrieval, answer-generation, scoring, security scanning, and trace logic as the API endpoint `POST /evaluate-question`.

This is useful for demos because it makes the full flow visible:

```text
manual question -> retrieved policy chunks -> generated answer -> scores -> pass/fail -> trace
```

When the mode is `LLM Generated`, the platform sends the retrieved context and question to the configured provider. For a free local setup, use Ollama:

```text
LLM_PROVIDER=ollama
APP_MODEL=qwen3:4b
OLLAMA_BASE_URL=http://localhost:11434
```

If Ollama is not running, the provider factory falls back to the mock provider so local demos and CI still work.

## Local Commands

```powershell
python -m llmops_governance.cli evaluate
python -m llmops_governance.cli run-gate
python -m llmops_governance.cli compare-models
python -m llmops_governance.cli generate-reports
```
