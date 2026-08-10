import unittest

from promotion import assess_shared_lifecycle_promotion


class PromotionTests(unittest.TestCase):
    def test_one_exact_consumer_does_not_earn_production_package(self):
        result = assess_shared_lifecycle_promotion(
            [
                {"owner": "ordivon-computing", "materiallyDifferent": True, "requiresExactSharedVocabulary": True, "deletionFailure": "maintenance projection loses stable lifecycle meaning"},
                {"owner": "ordivon-runtime", "materiallyDifferent": True, "requiresExactSharedVocabulary": False, "deletionFailure": "runtime retains native retention and reclaim semantics"},
                {"owner": "ordivon-world", "materiallyDifferent": True, "requiresExactSharedVocabulary": False, "deletionFailure": "world retains owner-native provider/retention semantics"},
            ]
        )
        self.assertFalse(result["productionSharedPackageEarned"])
        self.assertEqual(result["decision"], "keep_experiment_local")
        self.assertFalse(result["newRepositoryEarned"])

    def test_two_exact_consumers_only_earn_smallest_contract_not_repository(self):
        result = assess_shared_lifecycle_promotion(
            [
                {"owner": "a", "materiallyDifferent": True, "requiresExactSharedVocabulary": True, "deletionFailure": "a fails"},
                {"owner": "b", "materiallyDifferent": True, "requiresExactSharedVocabulary": True, "deletionFailure": "b fails"},
            ]
        )
        self.assertTrue(result["productionSharedPackageEarned"])
        self.assertFalse(result["newRepositoryEarned"])


if __name__ == "__main__":
    unittest.main()
