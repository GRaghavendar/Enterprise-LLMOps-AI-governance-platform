import unittest

from llmops_governance.config.settings import Settings
from llmops_governance.evaluators.rag_evaluator import RAGEvaluationPipeline
from llmops_governance.reports.generator import generate_reports


class ReportTests(unittest.TestCase):
    def test_generate_core_reports(self):
        settings = Settings.from_env()
        run = RAGEvaluationPipeline(settings).run(model_mode="grounded", limit=12)
        paths = generate_reports(run, settings)
        self.assertTrue(paths["governance_report_md"].exists())
        self.assertTrue(paths["evaluation_results"].exists())
        self.assertTrue(paths["latest_gate_result"].exists())


if __name__ == "__main__":
    unittest.main()

