# Synthetic Privacy Policy

## Purpose
This synthetic policy defines how customer data must be minimized, redacted, retained, and escalated.

## Scope
The policy applies to support, analytics, AI assistants, quality review, and vendor integrations.

## Policy Rules
- Customer personal data must not be exposed in model responses unless explicitly authorized by a privacy workflow.
- AI assistants must redact email addresses, phone numbers, SSN-like values, credit-card-like values, tokens, passwords, and private keys.
- Privacy incidents must be escalated to the privacy response lead within one business day.
- Analytics exports must use synthetic, aggregated, or de-identified data by default.
- Prompts and retrieved context must not include real credentials or confidential customer records.

## Approval Requirements
Any release that processes personal data requires privacy review, retention mapping, and deletion workflow documentation.

## Audit Requirements
Privacy reviews must include data category, retention period, allowed purpose, reviewer, and residual risk rating.
