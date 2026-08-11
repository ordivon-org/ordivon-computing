# EX2-C diagnosis — the final failure is a role-label collision

The third held-out relation test reached near-ceiling accuracy but still failed the preregistered critical-native-fact gate.

- compact responsibility: 335/336 = 99.70% query exact; 143/144 = 99.31% case exact;
- typed relations v2: 333/336 = 99.11% query exact; 141/144 = 97.92% case exact;
- owner/carrier, shared promotion, negative inference, admission, reconciliation, mapping, local execution, time and state semantics were otherwise stable;
- the only systematic typed-relation failure was `V05.security_destination_materialization`: three of six runs chose `AGENT_OR_DOMAIN` instead of `EXTERNAL_PROVIDER_OR_DOMAIN`.

The free-text reasons show that those three answers understood the fact correctly: each said Security's own destination adapter / Security as the domain owner records and proves material admission. The error therefore comes from the benchmark labels themselves. Both alternatives contain the word `DOMAIN`, but one means semantic judgment and the other means native external state authority.

EX2-D performs a terminology-invariance test without adding any new relation type. It replaces the colliding labels with role-pure names:

- `SEMANTIC_AGENT_OR_DOMAIN_JUDGE` — strategy/meaning/acceptance;
- `NATIVE_EXTERNAL_SYSTEM` — provider/source/destination native occurrence or state.

The relation model is retained only if fresh held-out cases remain stable under this role-pure vocabulary. This does not retroactively change EX2-C's preregistered `REJECT_OR_REVISE` result.
