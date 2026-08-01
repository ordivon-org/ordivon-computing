# G2 Local Schemas

These JSON Schemas support revision-bound G3-G6 research records:

- `case.schema.json` — one normalized governance case;
- `policy-revision.schema.json` — one exact rule revision and change set;
- `enforcement-event.schema.json` — one observed or reported intervention,
  appeal, and consequence;
- `provider-observation.schema.json` — one controlled model/Provider/Host/Runtime
  observation with layer separation.

They are research-local and intentionally incomplete. They must not be used as a
Provider reputation score, user risk score, policy enforcement service, or global
telemetry contract.

Validation in G2 checks JSON syntax, required local examples, unique identities,
and local links. It does not claim full semantic validation of future records.
