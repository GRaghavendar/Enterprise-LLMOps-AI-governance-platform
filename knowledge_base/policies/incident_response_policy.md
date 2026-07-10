# Synthetic Incident Response Policy

## Purpose
This synthetic policy defines how security, privacy, and AI safety incidents are triaged and remediated.

## Scope
The policy applies to engineering, security, privacy, legal, and customer operations teams.

## Policy Rules
- Critical incidents require notification to the incident commander within 30 minutes.
- Suspected credential exposure requires immediate token rotation, evidence preservation, and access review.
- AI incidents involving hallucinated high-risk advice require rollback, test reproduction, and customer impact review.
- Privacy incidents require containment, legal review, and root cause analysis.
- Post-incident reviews must capture timeline, detection source, blast radius, and preventive controls.

## Escalation Thresholds
Escalate any incident involving credentials, personal data exposure, regulatory impact, or production outage.

## Audit Requirements
Incident records must include severity, timeline, owner, affected systems, customer impact, evidence links, and closure approval.
