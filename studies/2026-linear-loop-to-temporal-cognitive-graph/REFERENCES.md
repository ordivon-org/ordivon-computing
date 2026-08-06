# References

## Foundational model and long-context research

- Vaswani et al., “Attention Is All You Need,” 2017.  
  https://arxiv.org/abs/1706.03762
- Liu et al., “Lost in the Middle: How Language Models Use Long Contexts,” 2023/2024.  
  https://arxiv.org/abs/2307.03172
- Hsieh et al., “RULER: What's the Real Context Size of Your Long-Context Language Models?”, 2024.  
  https://arxiv.org/abs/2404.06654
- Modarressi et al., “NoLiMa: Long-Context Evaluation Beyond Literal Matching,” 2025.  
  https://arxiv.org/abs/2502.05167

## Non-linear reasoning and external memory

- Yao et al., “Tree of Thoughts: Deliberate Problem Solving with Large Language Models,” 2023.  
  https://arxiv.org/abs/2305.10601
- Besta et al., “Graph of Thoughts: Solving Elaborate Problems with Large Language Models,” 2023.  
  https://arxiv.org/abs/2308.09687
- Packer et al., “MemGPT: Towards LLMs as Operating Systems,” 2023.  
  https://arxiv.org/abs/2310.08560
- Zhang, Kraska, and Khattab, “Recursive Language Models,” revised May 2026.  
  https://arxiv.org/abs/2512.24601
- Lumer et al., “Recursive Agent Harnesses,” June 2026.  
  https://arxiv.org/abs/2606.13643

## Multi-Agent systems and failure

- Fourney et al., “Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks,” 2024.  
  https://arxiv.org/abs/2411.04468
- Cemri et al., “Why Do Multi-Agent LLM Systems Fail?”, 2025.  
  https://arxiv.org/abs/2503.13657
- Google Research, “Blackboard Multi-Agent Systems for Information Discovery in Data Science.”  
  https://research.google/pubs/blackboard-multi-agent-systems-for-information-discovery-in-data-science/
- Google Research, “Accelerating scientific breakthroughs with an AI co-scientist,” 2025.  
  https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/

## Harness adaptation and self-improvement

- Karten et al., “Continual Harness: Online Adaptation for Self-Improving Foundation Agents,” May 2026.  
  https://arxiv.org/abs/2605.09998
- Google DeepMind, “AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms,” 2025.  
  https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
- Prime Intellect, “Prime Agent: A self-improving RLM agent,” 5 August 2026.  
  https://www.primeintellect.ai/blog/prime-agent
- Prime Intellect, `prime-agent` source repository.  
  https://github.com/PrimeIntellect-ai/prime-agent

## Agent–computer and Harness interface research

- Yang et al., “SWE-agent: Agent–Computer Interfaces Enable Automated Software Engineering,” 2024.  
  https://arxiv.org/abs/2405.15793
- OpenAI, “Unrolling the Codex agent loop,” 23 January 2026.  
  https://openai.com/index/unrolling-the-codex-agent-loop/
- OpenAI, “Unlocking the Codex harness: how we built the App Server,” 4 February 2026.  
  https://openai.com/index/unlocking-the-codex-harness/
- OpenAI, “The next evolution of the Agents SDK,” 15 April 2026.  
  https://openai.com/index/the-next-evolution-of-the-agents-sdk/
- OpenAI, “Harness engineering: leveraging Codex in an agent-first world,” 2026.  
  https://openai.com/index/harness-engineering/
- Anthropic, “Effective harnesses for long-running agents,” 26 November 2025.  
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic, “How we built our multi-agent research system,” 13 June 2025.  
  https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic, “Effective context engineering for AI agents,” 29 September 2025.  
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic, “Building a C compiler with a team of parallel Claudes,” 5 February 2026.  
  https://www.anthropic.com/engineering/building-c-compiler
- Anthropic, “Harness design for long-running application development,” 24 March 2026.  
  https://www.anthropic.com/engineering/harness-design-long-running-apps
- Anthropic, “Scaling Managed Agents: Decoupling the brain from the hands,” 8 April 2026.  
  https://www.anthropic.com/engineering/scaling-managed-agents
- Anthropic, “Demystifying evals for AI agents,” 9 January 2026.  
  https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

## Ordivon sources

- [`../2026-model-to-work-and-ordivon-harness/`](../2026-model-to-work-and-ordivon-harness/)
- [`../2026-agent-system-concept-system/`](../2026-agent-system-concept-system/)
- [`../2026-classical-to-agent-native-computing/`](../2026-classical-to-agent-native-computing/)
- [`../2026-ordivon-paradigm-reform/`](../2026-ordivon-paradigm-reform/)
- [`../../knowledge/models/transformer-learning-and-inference.md`](../../knowledge/models/transformer-learning-and-inference.md)
- [`../../knowledge/agents/probabilistic-work-control-loop.md`](../../knowledge/agents/probabilistic-work-control-loop.md)
- [`../../core/primitives.md`](../../core/primitives.md)
- [`../../research/questions/ANC-HARNESS-002-ordivon-harness.md`](../../research/questions/ANC-HARNESS-002-ordivon-harness.md)
- [`evidence/source-audit-20260806.json`](evidence/source-audit-20260806.json)

## Source limitations

- Company engineering reports describe the authors' own systems and may select favorable examples or internal evaluations.
- Preprints may change and do not establish production reliability.
- Graph of Thoughts, Tree of Thoughts, RLM, RAH, and MemGPT evaluate different tasks, models, and cost envelopes; their reported numbers are not directly comparable.
- Multi-Agent benefits are workload-dependent and often consume substantially more tokens.
- Prime Agent was released one day before this study; its long-term operational evidence and complete technical report are not yet available.
- Ordivon source findings bind the exact revisions in the evidence ledger and should not be treated as current after later repository changes.
- No external result substitutes for the proposed Ordivon ablations.
