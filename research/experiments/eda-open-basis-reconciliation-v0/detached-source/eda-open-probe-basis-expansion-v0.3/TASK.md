# Clean-Agent EDA Probe Basis Expansion Task — Standing-compiled v0.3

You are a research Agent proposing a **new KiCad schematic discriminator**, not the owner of the final contract.

The current correct baseline project is in `project/`. `BASELINE-STANDING.json` is a deterministic, independently provider-checked projection of the baseline for this exact research question. Treat that Standing as current; do **not** spend the episode rebuilding the same baseline ERC/netlist/pin facts unless a candidate Effect needs verification.

Two hypotheses remain:
- `H_connectivity_semantic`: acceptance depends on electrical ERC cleanliness and preservation of the target connectivity; exact net-name representation is incidental.
- `H_exact_net_name`: acceptance requires the same conditions **and** preservation of the exact baseline target net name.

Current mutation basis contains only `remove_wire`; exhaustive provider execution produced no discriminator. The useful missing mutation kind is intentionally not named.

Your responsibility is only the unresolved frontier:
1. infer one new single-edit mutation idea that should make the two hypotheses disagree;
2. implement it by changing only `project/ecc83-pp_v2.kicad_sch`;
3. use KiCad if useful to verify the candidate;
4. write `proposal.json` with exactly:
   - `mutationSummary`: short string;
   - `expectedDiscrimination`: short string;
   - `selfCheckedWithKiCad`: boolean.

The KiCad CLI is:
`/root/.local/share/ordivon/laboratory/providers/kicad-10.0.5-appimage-lite/bin/kicad-cli`

Do not search Ordivon research history or files outside this cell except that executable and ordinary system utilities. `BASELINE-STANDING.json` does not authorize owner contract mutation; it only removes already-solved representation/currentness work from your cognition budget.
