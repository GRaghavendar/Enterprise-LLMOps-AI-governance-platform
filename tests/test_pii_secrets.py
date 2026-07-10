import unittest

from llmops_governance.security.pii_secrets import detect_pii_and_secrets


class PiiSecretsTests(unittest.TestCase):
    def test_detects_fake_sensitive_values(self):
        findings = detect_pii_and_secrets("Use fake user jane.demo@example.test and SSN 123-45-6789.")
        types = {finding.finding_type for finding in findings}
        self.assertIn("email", types)
        self.assertIn("ssn", types)


if __name__ == "__main__":
    unittest.main()

