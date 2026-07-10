import unittest

from llmops_governance.config.settings import Settings
from llmops_governance.evaluators.rag_evaluator import RAGEvaluationPipeline
from llmops_governance.governance.readiness import assess_readiness


class GovernanceReadinessTests(unittest.TestCase):
    def test_grounded_mode_is_approved(self):
        settings = Settings.from_env()
        run = RAGEvaluationPipeline(settings).run(model_mode="grounded")
        decision = assess_readiness(run, settings.thresholds)
        self.assertEqual(decision.status, "approved")

    def test_unsafe_mode_is_blocked_or_reviewed(self):
        settings = Settings.from_env()
        run = RAGEvaluationPipeline(settings).run(model_mode="unsafe", limit=6)
        decision = assess_readiness(run, settings.thresholds)
        self.assertIn(decision.status, {"blocked", "needs_review"})


if __name__ == "__main__":
    unittest.main()

