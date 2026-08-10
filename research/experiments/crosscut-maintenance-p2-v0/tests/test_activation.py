import unittest

from activation import project_delivery


class ActivationTests(unittest.TestCase):
    def test_active_source_can_be_ahead_of_publication_without_activation_gap(self):
        result = project_delivery(owner="runtime", source_revision="b", published_revision="a", active_revision="b", deployable=True, publication_authority="remote", activation_authority="runtime")
        self.assertEqual(result["state"], "active_source_not_published")
        self.assertEqual(set(result["gaps"]), {"source_vs_published", "published_vs_active"})
        self.assertNotIn("source_vs_active", result["gaps"])

    def test_published_source_can_lag_activation(self):
        result = project_delivery(owner="runtime", source_revision="b", published_revision="b", active_revision="a", deployable=True, publication_authority="remote", activation_authority="runtime")
        self.assertEqual(result["state"], "published_source_not_active")
        self.assertEqual(set(result["gaps"]), {"source_vs_active", "published_vs_active"})

    def test_non_deployable_owner_does_not_invent_activation_gap(self):
        result = project_delivery(owner="computing", source_revision="a", published_revision="a", active_revision=None, deployable=False, publication_authority="remote")
        self.assertEqual(result["state"], "source_published")
        self.assertEqual(result["gaps"], [])


if __name__ == "__main__":
    unittest.main()
