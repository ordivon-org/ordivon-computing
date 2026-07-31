# References

## Official industry sources

### OpenAI

- OpenAI, “Unrolling the Codex agent loop,” 23 January 2026.  
  https://openai.com/index/unrolling-the-codex-agent-loop/
- OpenAI, “Unlocking the Codex harness: how we built the App Server,” 4 February 2026.  
  https://openai.com/index/unlocking-the-codex-harness/
- OpenAI Platform, Responses API and Tool documentation.  
  https://platform.openai.com/docs/

### Anthropic

- Anthropic, “Effective harnesses for long-running agents,” 26 November 2025.  
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic, “Building a C compiler with a team of parallel Claudes,” 5 February 2026.  
  https://www.anthropic.com/engineering/building-c-compiler
- Anthropic, “Harness design for long-running application development,” 24 March 2026.  
  https://www.anthropic.com/engineering/harness-design-long-running-apps
- Anthropic, “Scaling Managed Agents: Decoupling the brain from the hands,” 8 April 2026.  
  https://www.anthropic.com/engineering/scaling-managed-agents

### Microsoft

- Microsoft Learn, “Microsoft Agent Framework overview.”  
  https://learn.microsoft.com/en-us/agent-framework/overview/
- Microsoft Learn, “Agent Harnesses.”  
  https://learn.microsoft.com/en-us/agent-framework/agents/harness
- Microsoft Learn, Agent Framework workflows.  
  https://learn.microsoft.com/en-us/agent-framework/workflows/

### Google

- Google Cloud, “Vertex AI Agent Engine overview.”  
  https://cloud.google.com/vertex-ai/generative-ai/docs/reasoning-engine/overview
- Google Developers Blog, Agent Development Kit and graph-workflow material.  
  https://developers.googleblog.com/

## Ordivon authoritative evidence

### Continuation

- `research/experiments/task-continuation-v0/README.md`
- `research/experiments/task-continuation-v0/EVIDENCE.md`
- `research/experiments/task-continuation-v0/evidence/provider-comparison-1cdbbdc.json`
- `research/experiments/task-continuation-v0/evidence/provider-evaluation-1cdbbdc.json`

### Core Work System Round 1

- `research/experiments/core-work-system-v1/REPORT.md`
- `research/experiments/core-work-system-v1/RESULTS.md`
- `research/experiments/core-work-system-v1/DECISIONS.md`
- `research/experiments/core-work-system-v1/evidence/round1-report-receipt.json`

### Host Harness H1–H5

Authoritative repository: https://github.com/zycxfyh/ordivon-host

- `docs/harness-boundary-stage1.md`
- `docs/harness-boundary-h5-decision.md`
- `evidence/codex-app-h3-live-64ab44b-20260731.json`
- `evidence/hermes-acp-h4-live-3d9a559-20260731.json`
- `evidence/harness-replacement-h5-live-76420e4-20260731.json`
- Host merge revision: `e1ad5b669ca4c24a1ecdae7dfce659245f8b26e9`

### Computing immutable snapshot

- `research/evidence/snapshots/harness-boundary-h5-20260731t031134z.json`

## Source limitations

- Official company sources describe their own architecture and product goals; they are not neutral comparative evaluations.
- Product terms such as Harness, Agent, Runtime, Session, and Workflow do not have one universal boundary.
- Provider and framework implementations can change after the pinned dates.
- Ordivon token, timing, byte, and code-size values come from different protocols and fixtures and must not be treated as normalized benchmarks.
- Raw Provider reasoning is not part of the committed Ordivon evidence corpus; digests, counts, usage, Tool observations, Artifacts, and terminal evidence are retained instead.
