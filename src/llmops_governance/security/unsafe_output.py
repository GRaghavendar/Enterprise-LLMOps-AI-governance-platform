"""Unsafe output classifier for deterministic governance checks."""

from __future__ import annotations

import re

from llmops_governance.schemas.security import SecurityFinding
from llmops_governance.security.owasp_mapping import map_risk


UNSAFE_PATTERNS: list[tuple[str, str, str]] = [
    ("unsafe_output", r"\b(confidential|do not share|internal only|restricted record)\b", "high"),
    ("unsafe_output", r"\b(i can bypass|i have disabled|safety checks are off)\b", "critical"),
    ("unsafe_output", r"\b(use this private key|here is the password|api key is)\b", "critical"),
]


def classify_unsafe_output(text: str) -> list[SecurityFinding]:
    findings: list[SecurityFinding] = []
    for finding_type, pattern, severity in UNSAFE_PATTERNS:
        for match in re.finditer(pattern, text or "", re.IGNORECASE):
            findings.append(
                SecurityFinding(
                    finding_type=finding_type,
                    severity=severity,
                    matched_text=match.group(0)[:120],
                    description="Output contains language that suggests unsafe disclosure or disabled controls.",
                    mapped_risk=map_risk(finding_type),
                    recommendation="Block the answer and require human review.",
                )
            )
    return findings

