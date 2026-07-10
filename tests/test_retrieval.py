import unittest

from llmops_governance.config.settings import Settings
from llmops_governance.evaluators.rag_evaluator import RAGEvaluationPipeline


class RetrievalTests(unittest.TestCase):
    def test_retriever_returns_policy_chunks(self):
        pipeline = RAGEvaluationPipeline(Settings.from_env())
        results = pipeline.retriever.retrieve("What must AI systems cite?", top_k=2)
        self.assertTrue(results)
        self.assertTrue(any(result.source_document.endswith(".md") for result in results))


if __name__ == "__main__":
    unittest.main()

