from __future__ import annotations
import json,pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
class ContentCloseoutTests(unittest.TestCase):
 def test_unique_metadata_value_is_narrow(self):
  d=json.loads((HERE/'evidence/content-wave-v1.json').read_text()); a=d['attacks'][0]; self.assertIn('BLOCKED',a['customResult']); self.assertEqual((a['markdownlint'],a['cspell'],a['vale']),('pass','pass','pass'))
 def test_templates_and_fixtures_do_not_survive_by_default(self):
  d=json.loads((HERE/'content-wave-v1-closeout.json').read_text()); self.assertIn('archive/delete',d['preliminaryDispositions']['CONTENT-03']); self.assertIn('archive/delete',d['preliminaryDispositions']['CONTENT-04'])
if __name__=='__main__':unittest.main()
