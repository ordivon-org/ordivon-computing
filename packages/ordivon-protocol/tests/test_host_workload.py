from __future__ import annotations

import json
import unittest

from anc_canonical import canonical_bytes, canonical_digest
from ordivon_protocol import vector_text
from ordivon_protocol.host_workload import (
    WorkloadAdmissionError,
    WorkloadValidationError,
    admit_model_decision,
    validate_host_workload_object,
)


class HostWorkloadProtocolTests(unittest.TestCase):
    def test_normative_vectors_validate_and_admit(self) -> None:
        document = json.loads(vector_text("host-workload-vectors-v1.json"))
        self.assertEqual(document["kind"], "ordivon.host-workload-conformance-vectors")
        for case in document["cases"]:
            with self.subTest(case=case["caseId"]):
                if case["operation"] == "validate":
                    if case["expected"]["accepted"]:
                        validate_host_workload_object(case["input"])
                        self.assertEqual(
                            canonical_digest(case["input"]),
                            case["expected"]["digest"],
                        )
                    else:
                        with self.assertRaises(WorkloadValidationError):
                            validate_host_workload_object(case["input"])
                elif case["operation"] == "admit-decision":
                    arguments = case["arguments"]
                    if case["expected"]["accepted"]:
                        admitted = admit_model_decision(
                            arguments["context"],
                            arguments["decision"],
                            current_state_refs=arguments["currentStateRefs"],
                            completed_effect_ids=tuple(arguments["completedEffectIds"]),
                            unresolved_dispatch_ids=tuple(arguments["unresolvedDispatchIds"]),
                        )
                        self.assertEqual(admitted, case["expected"]["admitted"])
                        self.assertEqual(
                            canonical_digest(admitted),
                            case["expected"]["digest"],
                        )
                    else:
                        with self.assertRaises(WorkloadAdmissionError) as captured:
                            admit_model_decision(
                                arguments["context"],
                                arguments["decision"],
                                current_state_refs=arguments["currentStateRefs"],
                                completed_effect_ids=tuple(arguments["completedEffectIds"]),
                                unresolved_dispatch_ids=tuple(arguments["unresolvedDispatchIds"]),
                            )
                        self.assertEqual(captured.exception.code, case["expected"]["code"])
                else:  # pragma: no cover - normative vector gate
                    self.fail(f"unsupported vector operation: {case['operation']}")

    def test_compiled_context_detects_digest_or_length_tampering(self) -> None:
        document = json.loads(vector_text("host-workload-vectors-v1.json"))
        context = next(
            case["input"]
            for case in document["cases"]
            if case["caseId"] == "validate-compiled-context"
        )
        self.assertEqual(context["byteLength"], len(canonical_bytes(context["payload"])))
        forged = {**context, "byteLength": context["byteLength"] + 1}
        with self.assertRaises(WorkloadValidationError):
            validate_host_workload_object(forged)


if __name__ == "__main__":
    unittest.main()
