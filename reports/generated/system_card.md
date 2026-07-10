# System Card: Enterprise LLMOps AI Governance Platform

## System Purpose
Evaluate RAG and LLM applications before production deployment using deterministic metrics, security scanners, governance rules, and optional LLM-as-judge review.

## Architecture
The platform loads synthetic policy documents, retrieves local context with TF-IDF, evaluates responses, scans for injection and sensitive-data risks, and generates audit-ready reports.

## Governance Decision
- Status: approved
- Summary: The evaluated RAG system meets the configured governance release gate.

## Traceability
Each evaluation item includes run ID, trace ID, dataset version, prompt version, model mode, retrieved sources, metric scores, failure reasons, and recommendations.

## Data Privacy
All included data is synthetic. The project must not be run with real PII, PHI, PCI, secrets, credentials, employer records, or customer records.

## Human Oversight
High-risk or blocked decisions require a human governance reviewer before production release.
