from __future__ import annotations
import pathlib,unittest
HERE=pathlib.Path(__file__).resolve().parents[1]
class ControlContractTests(unittest.TestCase):
 def test_runner_contains_independent_semantic_mutants(self):
  s=(HERE/'control_plane_mutation.py').read_text()
  for token in ('owner_revision_movement_automatically_changes_shared_world_model','Research scores automatically own product merge','Retain every existing Computer structure by default','A single mechanical score owns priority','mandatory prerequisite for itself'): self.assertIn(token,s)
 def test_baseline_records_current_real_faults(self):
  s=(HERE/'evidence/control-audit-baseline.json').read_text()
  for fid in ('CTRL-F01','CTRL-F02','CTRL-F03','CTRL-F04','CTRL-F05'): self.assertIn(fid,s)
if __name__=='__main__':unittest.main()
