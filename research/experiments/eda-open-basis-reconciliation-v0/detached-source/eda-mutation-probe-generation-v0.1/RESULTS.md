# EDA Mutation Probe Generation v0.1

Purpose: transfer open-probe construction pressure from synthetic decision tables into a real KiCad schematic responsibility.

The generator is not told the known hand-authored label-equivalent answer or its coordinate. It receives only the admitted correct schematic and a bounded mutation grammar:

- add one fresh local label at any unique existing wire endpoint;
- remove one existing wire.

Every generated mutation is actually executed through KiCad 10.0.5 CLI and projected to:

- electrical ERC cleanliness;
- whether R1.1/U1.1/U1.7 remain one net;
- whether that net's name changed from baseline.

Two explicit research hypotheses are then evaluated against the provider-derived consequences:

- `H_connectivity_semantic`: connectivity + ERC are responsibility-relevant, exact net name is incidental;
- `H_exact_net_name`: connectivity + ERC + exact baseline target net name are all required.

Any mutation that preserves connectivity/ERC while changing only the target net name separates these hypotheses.

This is **grammar-bounded probe generation**, not unrestricted open-world experiment invention. It asks whether a domain mutation grammar plus provider execution can generate discriminator candidates without an Agent hand-authoring the known counterfactual.
