from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ConsumerAdoptionEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.receipt = json.loads(
            (ROOT / "evidence" / "a1-consumer-adoption-acceptance.json").read_text(
                encoding="utf-8"
            )
        )

    def test_security_failure_required_both_digest_and_byte_count(self) -> None:
        trial = self.receipt["consumerTrials"]["securityRuntimeArtifact"]
        before = trial["preFixReproduction"]
        after = trial["postFix"]
        self.assertTrue(before["readDigestMatched"])
        self.assertEqual(before["descriptorRetainedBytes"], 31)
        self.assertEqual(before["readNextOffset"], 10)
        self.assertTrue(before["oldConsumerAccepted"])
        self.assertTrue(after["earlyEofByteCountMismatchRejected"])
        self.assertTrue(after["eofOvershootByteCountMismatchRejected"])
        self.assertFalse(after["newProductionDependencyAdded"])

    def test_second_cross_boundary_consumer_already_protects_the_pair(self) -> None:
        trial = self.receipt["consumerTrials"]["worldBrowserArtifact"]
        self.assertFalse(trial["productionChangeRequired"])
        self.assertTrue(trial["receiptDigestDriftRejected"])
        self.assertTrue(trial["receiptByteCountDriftRejected"])
        self.assertTrue(trial["mediaTypeRemainsSeparateOwnerSemanticCheck"])

    def test_package_promotion_is_rejected_on_current_cost(self) -> None:
        dependency = self.receipt["dependencyAssessment"]
        decision = self.receipt["decision"]
        self.assertEqual(dependency["securityDeclaredProductionDependenciesBefore"], 0)
        self.assertTrue(dependency["securityWouldNeedNewProtocolDependencyForSharedValueObject"])
        self.assertTrue(dependency["worldWouldNeedDirectProtocolDependencyForCorrectDirectImport"])
        self.assertFalse(dependency["sharedPackageWouldRemoveMaterialOwnerLifecycleCode"])
        self.assertTrue(decision["contentIdentitySemanticCandidateRetained"])
        self.assertFalse(decision["promoteToOrdivonProtocol"])
        self.assertFalse(decision["createSharedContentLibrary"])
        self.assertFalse(decision["createArtifactRepository"])


if __name__ == "__main__":
    unittest.main()
