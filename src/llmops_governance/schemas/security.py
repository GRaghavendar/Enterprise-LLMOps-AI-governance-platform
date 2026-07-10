"""Security scan schema dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SecurityFinding:
    finding_type: str
    severity: str
    matched_text: str
    description: str
    mapped_risk: str
    recommendation: str


@dataclass
class SecurityScanResult:
    findings: list[SecurityFinding] = field(default_factory=list)
    prompt_injection_risk: float = 0.0
    pii_secrets_risk: float = 0.0
    unsafe_output_risk: float = 0.0
    mapped_risks: list[str] = field(default_factory=list)

    @property
    def has_critical_findings(self) -> bool:
        return any(finding.severity.lower() == "critical" for finding in self.findings)

