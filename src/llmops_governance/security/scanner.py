"""Combined security scanner."""

from __future__ import annotations

from llmops_governance.schemas.security import SecurityFinding, SecurityScanResult
from llmops_governance.security.pii_secrets import detect_pii_and_secrets
from llmops_governance.security.prompt_injection import detect_prompt_injection, is_refusal
from llmops_governance.security.unsafe_output import classify_unsafe_output
from llmops_governance.utils import clamp


SEVERITY_WEIGHT = {"low": 0.15, "medium": 0.35, "high": 0.7, "critical": 1.0}


def _risk(findings: list[SecurityFinding], refusal_discount: bool = False) -> float:
    if not findings:
        return 0.0
    value = max(SEVERITY_WEIGHT.get(finding.severity.lower(), 0.3) for finding in findings)
    if refusal_discount:
        value *= 0.10
    return clamp(value)


def scan_security(prompt: str, response: str, retrieved_context: str = "") -> SecurityScanResult:
    prompt_findings = detect_prompt_injection(prompt)
    context_findings = detect_prompt_injection(retrieved_context)
    response_injection_findings = detect_prompt_injection(response)
    pii_response_findings = detect_pii_and_secrets(response)
    pii_context_findings = detect_pii_and_secrets(retrieved_context)
    unsafe_findings = classify_unsafe_output(response)
    refused = is_refusal(response)

    findings = [
        *prompt_findings,
        *context_findings,
        *response_injection_findings,
        *pii_response_findings,
        *pii_context_findings,
        *unsafe_findings,
    ]
    mapped_risks = sorted({finding.mapped_risk for finding in findings})

    return SecurityScanResult(
        findings=findings,
        prompt_injection_risk=_risk([*prompt_findings, *context_findings, *response_injection_findings], refused),
        pii_secrets_risk=_risk([*pii_response_findings, *pii_context_findings], False),
        unsafe_output_risk=_risk(unsafe_findings, refused),
        mapped_risks=mapped_risks,
    )
