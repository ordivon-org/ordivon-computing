import json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
class T(unittest.TestCase):
 def test_frozen(self):
  c=json.loads((HERE/'fixtures/cards.json').read_text())['cards']; o=json.loads((HERE/'fixtures/oracle.json').read_text())['labels']; self.assertEqual(len(c),8); self.assertFalse(any('expected' in x for x in c)); self.assertEqual({x['id'] for x in c},set(o))
 def test_rule(self):
  p=json.loads((HERE/'plan-v1.json').read_text()); self.assertIn('<=0.75',p['promotionRule']); self.assertIn('no V2 tuning',p['stopRule'])
if __name__=='__main__':unittest.main()
