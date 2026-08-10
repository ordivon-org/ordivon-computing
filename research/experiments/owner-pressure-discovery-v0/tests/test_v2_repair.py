from __future__ import annotations
import hashlib,json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
from run_live_pressure_discovery import instruction
class V2RepairTests(unittest.TestCase):
 def test_scientific_assets_are_byte_frozen(self):
  plan=json.loads((HERE/'plan-v2.json').read_text()); refs={'fixtures/cards.json':'cardsDigest','fixtures/oracle.json':'oracleDigest','evaluator.py':'evaluatorDigest','plan-v1.json':'planV1Digest'}
  for rel,key in refs.items(): self.assertEqual('sha256:'+hashlib.sha256((HERE/rel).read_bytes()).hexdigest(),plan['scientificAssets'][key])
 def test_selective_limit_is_agent_visible_without_evidence_body(self):
  cards=json.loads((HERE/'fixtures/cards.json').read_text())['cards']; dev=[c for c in cards if c['split']=='development']; hold=[c for c in cards if c['split']=='holdout']; d=instruction('development',dev,include_evidence=False); h=instruction('holdout',hold,include_evidence=False); self.assertIn('at most 3 distinct owner evidence cards',d); self.assertIn('at most 2 distinct owner evidence cards',h); self.assertNotIn(dev[0]['evidence'][:500],d)
 def test_promotion_rule_unchanged(self):
  self.assertEqual(json.loads((HERE/'plan-v1.json').read_text())['promotionRule'],json.loads((HERE/'plan-v2.json').read_text())['promotionRule'])
if __name__=='__main__':unittest.main()
