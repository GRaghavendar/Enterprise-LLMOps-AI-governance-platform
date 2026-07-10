# API Reference

Run locally:

```powershell
uvicorn llmops_governance.api.main:app --reload
```

Endpoints:

- `GET /`
- `GET /health`
- `POST /evaluate-question`
- `POST /run-evaluation`
- `POST /run-gate`
- `GET /latest-results`
- `GET /governance-report`
- `GET /risk-register`
- `GET /model-card`
- `GET /system-card`
- `GET /traces/{run_id}`

Example request:

```json
{
  "model_mode": "grounded",
  "limit": 20
}
```

