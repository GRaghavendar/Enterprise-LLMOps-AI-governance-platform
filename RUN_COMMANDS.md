# Run Commands

## First-Time Setup

Open PowerShell in the project folder:

```powershell
cd C:\Users\ragha\Documents\Codex\2026-07-09\let\enterprise-llmops-ai-governance-platform
.\scripts\setup_windows.ps1
```

If PowerShell blocks scripts, run this once in the same terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then rerun:

```powershell
.\scripts\setup_windows.ps1
```

## Start FastAPI

Use Terminal 1:

```powershell
cd C:\Users\ragha\Documents\Codex\2026-07-09\let\enterprise-llmops-ai-governance-platform
.\scripts\run_api.ps1
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Start Streamlit Dashboard

Use Terminal 2:

```powershell
cd C:\Users\ragha\Documents\Codex\2026-07-09\let\enterprise-llmops-ai-governance-platform
.\scripts\run_dashboard.ps1
```

Open:

```text
http://localhost:8501
```

## Offline CLI Commands

```powershell
python -m llmops_governance.cli evaluate
python -m llmops_governance.cli run-gate
python -m llmops_governance.cli compare-models
python -m llmops_governance.cli generate-reports
```

## Optional Free Local LLM Mode

Install Ollama separately, then:

```powershell
ollama pull qwen3:4b
ollama pull qwen3:8b
```

Set environment variables for the current PowerShell session:

```powershell
$env:LLM_PROVIDER="ollama"
$env:APP_MODEL="qwen3:4b"
$env:EVAL_JUDGE_MODEL="qwen3:8b"
$env:OLLAMA_BASE_URL="http://localhost:11434"
```

Then choose `LLM Generated` in the dashboard.

## Validate Project

```powershell
.\scripts\run_offline_validation.ps1
```

