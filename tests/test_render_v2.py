import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from render_v2 import render,wrap
class EnhancedTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/"examples"/"architecture.json").read_text(encoding="utf-8"))
    def test_themes(self):
        self.assertIn("#101722",render(self.data,"dark"))
        self.assertIn("#F7F9FC",render(self.data,"light"))
    def test_cjk(self):
        self.assertTrue(len(wrap("智能故障诊断与知识协同决策",12))>1)
    def test_escape(self):
        self.data["nodes"][0]["label"]="<script>"
        self.assertNotIn("<script>",render(self.data))
    def test_lr(self):
        self.data["direction"]="LR"
        self.assertIn("<svg",render(self.data))
if __name__=="__main__":unittest.main()
