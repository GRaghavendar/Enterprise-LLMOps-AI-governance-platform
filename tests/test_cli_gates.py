import unittest

from llmops_governance.cli.main import main


class CliGateTests(unittest.TestCase):
    def test_grounded_gate_exits_zero(self):
        self.assertEqual(main(["run-gate", "--model-mode", "grounded", "--limit", "12"]), 0)

    def test_unsafe_gate_exits_nonzero(self):
        self.assertNotEqual(main(["run-gate", "--model-mode", "unsafe", "--limit", "6"]), 0)


if __name__ == "__main__":
    unittest.main()

