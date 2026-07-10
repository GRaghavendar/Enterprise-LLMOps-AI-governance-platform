"""PII and secrets detection using deterministic regex patterns."""

from __future__ import annotations

import re

from llmops_governance.schemas.security import SecurityFinding
from llmops_governance.security.owasp_mapping import map_risk


PII_SECRET_PATTERNS: list[tuple[str, str, str, str]] = [
    ("email", r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "medium", "Potential email address."),
    ("phone", r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "medium", "Potential phone number."),
    ("ssn", r"\b\d{3}-\d{2}-\d{4}\b", "critical", "Potential SSN-like value."),
    ("credit_card", r"\b(?:\d[ -]*?){13,16}\b", "critical", "Potential credit-card-like value."),
    ("api_key", r"\b(?:sk|pk|rk|api)[-_]?[A-Za-z0-9]{16,}\b", "critical", "Potential API-key-like value."),
    ("token", r"\b(?:token|bearer|secret)[=:]\s*[A-Za-z0-9._-]{12,}\b", "critical", "Potential token-like value."),
    ("password", r"\bpassword\s*[=:]\s*[^,\s]{8,}", "critical", "Potential password-like value."),
    ("private_key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "critical", "Potential private key block."),
]


def detect_pii_and_secrets(text: str) -> list[SecurityFinding]:
    findings: list[SecurityFinding] = []
    for finding_type, pattern, severity, description in PII_SECRET_PATTERNS:
        for match in re.finditer(pattern, text or "", re.IGNORECASE):
            findings.append(
                SecurityFinding(
                    finding_type=finding_type,
                    severity=severity,
                    matched_text=match.group(0)[:120],
                    description=description,
                    mapped_risk=map_risk("data_exfiltration"),
                    recommendation="Redact the value, block the response if it appears in output, and route the trace to privacy review.",
                )
            )
    return findings

