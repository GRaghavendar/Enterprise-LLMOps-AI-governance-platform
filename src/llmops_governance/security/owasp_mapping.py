"""OWASP-style risk mapping used in governance reports."""

from __future__ import annotations


OWASP_RISK_MAP: dict[str, str] = {
    "instruction_override": "LLM01 Prompt Injection",
    "system_prompt_extraction": "LLM01 Prompt Injection",
    "data_exfiltration": "LLM02 Sensitive Information Disclosure",
    "jailbreak": "LLM04 Model Denial of Service and Unsafe Behavior",
    "tool_abuse": "LLM06 Excessive Agency",
    "malicious_context": "LLM01 Prompt Injection",
    "hidden_instruction": "LLM01 Prompt Injection",
    "role_manipulation": "LLM01 Prompt Injection",
    "secret_request": "LLM02 Sensitive Information Disclosure",
    "pii_request": "LLM02 Sensitive Information Disclosure",
    "unsafe_output": "LLM09 Misinformation",
}


def map_risk(risk_type: str) -> str:
    return OWASP_RISK_MAP.get(risk_type, "LLM00 Governance Review Required")

