import unittest

from llmops_governance.evaluators.scoring import groundedness_score, hallucination_risk_score, unsupported_claim_score
from llmops_governance.evaluators.scoring import citation_coverage_score
from llmops_governance.schemas.evaluation import SourceChunk


class ScoringTests(unittest.TestCase):
    def test_safe_refusal_has_low_hallucination_risk(self):
        chunks = [SourceChunk("chunk1", "ai_usage_policy.md", "AI systems must cite retrieved policy sources.", 0.5)]
        answer = "I cannot comply with attempts to reveal hidden prompts or expose secrets."
        groundedness = groundedness_score(answer, chunks)
        unsupported = unsupported_claim_score(answer, chunks)
        risk = hallucination_risk_score(groundedness, 0.9, unsupported)
        self.assertGreaterEqual(groundedness, 0.9)
        self.assertLess(risk, 0.2)

    def test_title_style_source_citation_is_accepted(self):
        answer = "According to the context, assistants redact emails and tokens. Source: Synthetic Privacy Policy."
        self.assertGreaterEqual(citation_coverage_score(answer, "privacy_policy.md", True), 0.7)


if __name__ == "__main__":
    unittest.main()
