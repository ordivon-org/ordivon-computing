# DeepSeek Capability-Governance Case

Observed through: 2026-08-01

## Surface and revisions

DeepSeek provides consumer services and an Open Platform API. Current public
materials observed in G4 include:

- Terms of Use updated 2026-03-27;
- Open Platform Terms released 2026-04-22 and effective 2026-04-29;
- Privacy Policy updated and effective 2026-02-10;
- API changelog introducing V4-Pro and V4-Flash on 2026-04-24.

The API supports OpenAI-compatible and Anthropic-compatible interfaces, making it
useful for G6 surface portability without changing the underlying Provider.

## Governance structure

DeepSeek's public terms bind users to platform rules, applicable law, account and
API requirements, content and downstream-developer responsibilities. Consumer and
API data are governed by different relationships; downstream application end-user
data may fall outside the consumer privacy policy and into the developer's duties.

As a China-based Provider, DeepSeek also operates within Chinese filing,
algorithm, content, data, and security requirements. Provider policy and public
law are therefore especially difficult to separate empirically.

## Transparency limits

The public corpus gives current legal texts and model/API revisions but less
operational detail on:

- classifier or human-review mechanisms;
- account-level risk aggregation;
- warning/suspension thresholds;
- aggregate bans and appeal reversals;
- exact safety retention triggered by flags.

This is a disclosure gap, not proof of absence.

## R6 evidence

R6 supplies E5 evidence for DeepSeek V4 Flash/Pro through a real Host/Harness/
Runtime path. It found Provider/model refusal for tested document injections but
a successful Tool-description attack under ambient authority. This demonstrates
why Provider behavior and physical Effect containment must remain separate.

## References

[G043], [G044], [G045], [G046], plus the bound R6 evidence.
