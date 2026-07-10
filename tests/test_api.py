import unittest

from llmops_governance.api.main import health


class ApiTests(unittest.TestCase):
    def test_health_payload(self):
        self.assertEqual(health()["status"], "ok")


if __name__ == "__main__":
    unittest.main()

