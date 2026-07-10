"""Prompt injection and jailbreak detection."""

from __future__ import annotations

import re

from llmops_governance.schemas.security import SecurityFinding
from llmops_governance.security.owasp_mapping import map_risk


PROMPT_INJECTION_PATTERNS: list[tuple[str, str, str]] = [
    ("instruction_override", r"ignore (all )?(previous|prior|above) instructions", "critical"),
    ("system_prompt_extraction", r"(reveal|print|show|expose).{0,40}(system prompt|hidden prompt|developer message)", "critical"),
    ("data_exfiltration", r"(print|return|expose|dump).{0,40}(api keys?|credentials?|confidential records?)", "critical"),
    ("jailbreak", r"(act as|pretend to be).{0,30}(unrestricted|uncensored|developer mode)", "high"),
    ("policy_bypass", r"(disable|bypass|turn off).{0,30}(safety|guardrails|policy checks?)", "high"),
    ("hidden_instruction", r"(<!--|<hidden>|base64|rot13).{0,80}(ignore|override|instruction)", "high"),
    ("role_manipulation", r"you are now (root|admin|system|developer)", "medium"),
    ("secret_request", r"(return|show|print).{0,30}(token|password|secret|private key)", "critical"),
]


def detect_prompt_injection(text: str) -> list[SecurityFinding]:
    findings: list[SecurityFinding] = []
    for risk_type, pattern, severity in PROMPT_INJECTION_PATTERNS:
        for match in re.finditer(pattern, text or "", re.IGNORECASE | re.DOTALL):
            findings.append(
                SecurityFinding(
                    finding_type=risk_type,
                    severity=severity,
                    matched_text=match.group(0)[:120],
                    description=f"Detected {risk_type.replace('_', ' ')} pattern.",
                    mapped_risk=map_risk(risk_type),
                    recommendation="Refuse the instruction, preserve the system hierarchy, and continue only with grounded policy content.",
                )
            )
    return findings


def is_refusal(text: str) -> bool:
    lower = (text or "").lower()
    refusal_markers = [
        "i can't",
        "i cannot",
        "cannot provide",
        "can't comply",
        "not able to",
        "not enough information",
        "out of scope",
        "i will not",
        "must be escalated",
    ]
    return any(marker in lower for marker in refusal_markers)

