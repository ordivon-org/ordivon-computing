# Meta Llama 4 and Licensed Open-Weight Governance

Observed through: 2026-08-01

## Why this is a different case

A downloadable model moves request-level execution from the upstream Provider to
the deployer. After lawful acquisition, Meta does not need to observe each local
prompt or remotely route each response. This materially strengthens technical
exit and reproducibility.

## License remains governance

Llama 4 is distributed under the Llama 4 Community License effective 2025-04-05,
not a public-domain or standard permissive software license. The license:

- permits use, modification, derivatives, and redistribution under conditions;
- incorporates the Llama 4 Acceptable Use Policy;
- requires attribution and `Built with Llama` / naming conditions in specified
  downstream distributions;
- requires a separate Meta license for products above 700 million monthly active
  users, which Meta may grant in its discretion;
- requires trade-law compliance;
- contains regional limitations for some multimodal rights.

The AUP prohibits broad unlawful, harmful, deceptive, privacy-invasive, and
safety-circumvention uses.

## Shifted rather than eliminated power

Open-weight deployment redistributes power toward:

```text
local deployer
cloud or hardware operator
model distributor
fine-tuner
application Host
sector regulator
```

It reduces upstream request/account power but can increase downstream deployer
power over users. Hardware, energy, high-end accelerators, update supply, model
provenance, and legal enforcement remain concentrated.

## Assessment

Llama 4 provides stronger inference continuity and behavior forkability than a
hosted frontier API. It does not establish complete governance freedom or full
infrastructure sovereignty. G4 therefore records “licensed downloadable weights”
as its own governance mode.

## References

[G050], [G051], [G052].
