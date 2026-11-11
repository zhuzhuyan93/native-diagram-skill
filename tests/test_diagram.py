import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate import validate
from render import render


class DiagramTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples" / "architecture.json").read_text(encoding="utf-8"))

    def test_example_valid(self):
        self.assertEqual(validate(self.data), [])

    def test_render_svg(self):
        result = render(self.data)
        self.assertIn("<svg", result)
        self.assertIn("Agent Orchestration", result)

    def test_unknown_edge_rejected(self):
        self.data["edges"].append({"from": "missing", "to": "agent"})
        self.assertTrue(validate(self.data))


if __name__ == "__main__":
    unittest.main()
