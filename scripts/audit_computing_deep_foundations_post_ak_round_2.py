#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "research/evidence/computing-deep-foundations-post-ak-round-2-access-revelation-change-20260818.json"
ARTIFACT = ROOT / "research/COMPUTING-DEEP-FOUNDATIONS-POST-AK-ROUND-2-ACCESS-REVELATION-CHANGE-DESTRUCTIVE-TOURNAMENT-20260818.md"

data = json.loads(EVIDENCE.read_text())
text = ARTIFACT.read_text()
checks = []

def check(name, cond):
    checks.append((name, bool(cond)))

check("status_complete", data["status"] == "round-complete")
check("hypothesis_exact", data["hypothesis"] == "ComputationalAccessRevelationAndChangeResponsibility")
check("hypothesis_rejected_sibling", data["hypothesis_disposition"] == "REJECTED_AS_CLEAN_INDEPENDENT_SIBLING")
check("no_foundation_admission", data["foundation_admission"] == "NONE")
check("cdf0_not_admitted", data["cdf0"] == "NOT_ADMITTED")
check("closure_not_claimed", data["whole_computing_closure"] == "NOT_CLAIMED")
check("regime_count_ge_10", len(data["regimes"]) >= 10)
check("anti_collapse_count_ge_15", len(data["anti_collapse_laws"]) >= 15)
check("burden_deletion_count_12", len(data["burden_deletion"]) == 12)
check("rival_count_6", len(data["rival_verdicts"]) == 6)
check("XA_M1_rejected", data["rival_verdicts"]["XA-M1_access_only_scalar_resource"] == "REJECTED")
check("XA_M3_survives", data["rival_verdicts"]["XA-M3_access_B_I_regime"] == "STRONG_SURVIVOR")
check("XA_M4_survives", data["rival_verdicts"]["XA-M4_query_update_change_C_semantics"] == "STRONG_SURVIVOR")
check("XA_M5_rejected", data["rival_verdicts"]["XA-M5_incrementality_is_J_retention"] == "REJECTED")
check("XA_M6_rejected", data["rival_verdicts"]["XA-M6_independent_access_revelation_change_responsibility"] == "REJECTED_AS_CLEAN_SIBLING")
check("A_not_reopened", "NOT_REOPENED" in data["architecture_effects"]["A"])
check("B_not_reopened", "NOT_REOPENED" in data["architecture_effects"]["B"])
check("C_strengthened", data["architecture_effects"]["C"].startswith("STRENGTHENED"))
check("I_oracle_power", "ORACLE_RELATIVE_POWER" in data["architecture_effects"]["I"])
check("J_narrowed", data["architecture_effects"]["J"].startswith("NARROWED"))
check("D_conditional", data["architecture_effects"]["D"] == "CONDITIONAL_ONLY")
check("F_conditional", data["architecture_effects"]["F"] == "CONDITIONAL_ONLY")
check("K_conditional", data["architecture_effects"]["K"] == "CONDITIONAL_ONLY")
check("G_conditional", data["architecture_effects"]["G"] == "CONDITIONAL_ONLY")
check("three_consolidations", data["saturation_signal"]["sequence"] == ["J_CONSOLIDATED", "K_CONSOLIDATED", "X-A_CONSOLIDATED"])
check("closure_test_not_yet", data["saturation_signal"]["formal_closure_test"].startswith("NOT_YET"))
check("next_tournament_unknown", data["next"]["next_computing_research_tournament"].startswith("UNKNOWN"))
check("next_cdf_unknown", data["next"]["next_cdf"] == "UNKNOWN")
check("numbered_cdf_zero", data["next"]["numbered_cdf_count"] == 0)

for law in data["anti_collapse_laws"]:
    check("artifact_has_law_" + law.split(" != ")[0], law in text)

for section in [
    "Online paging",
    "Streaming",
    "External-memory",
    "Cell-probe",
    "Query / property-testing",
    "Oracle-relative computation",
    "Incremental view maintenance",
    "Self-adjusting computation",
    "Differential dataflow",
    "Direct deletion test",
    "Saturation signal"
]:
    check("artifact_section_" + section.replace(" ", "_").replace("/", "_"), section in text)

required_phrases = [
    "AccessModel\n!= ResourceAmount",
    "RetainedState\n!= ValidIncrementalReuse",
    "IndependentXABurdenAfterSubtraction\n= EMPTY AT CURRENT EVIDENCE FRONTIER",
    "ComputationalAccessRevelationAndChangeResponsibility\n= REJECTED AS CLEAN INDEPENDENT SIBLING",
    "WholeComputingClosure\n= NOT CLAIMED",
    "CDF0\n= NOT ADMITTED",
    "NextComputingResearchTournament\n= UNKNOWN UNTIL FRESH POST-XA RERANKING"
]
for phrase in required_phrases:
    check("artifact_required_" + phrase.splitlines()[0], phrase in text)

failed = [name for name, ok in checks if not ok]
print(f"checks={len(checks)} passed={len(checks)-len(failed)} failed={len(failed)}")
if failed:
    for name in failed:
        print("FAIL", name)
    raise SystemExit(1)
for name, _ in checks:
    print("PASS", name)
