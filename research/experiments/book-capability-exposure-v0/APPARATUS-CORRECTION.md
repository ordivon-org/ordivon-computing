# Apparatus correction v1b

The initial structured-result pilot is INVALID_FOR_EFFICACY. GESTALT failed 3/3 and REORDER failed 2/4 because the Provider emitted malformed JSON for `submit_run_conclusion`; retained Harness trace reports `conclusion_rejected.argumentError=invalid_json`. This is a carrier/conformance interaction, not evidence that capability representation is semantically worse.

v1b keeps the same Book arms, Provider/model, semantic question and zero-Tool intent, but transports the semantic answer in ordinary assistant content under completion `mode=record`. The full assistant content—not the short conclusion summary—is the efficacy object. All efficacy arms are rerun from scratch under v1b. The invalid structured runs remain apparatus evidence only.
