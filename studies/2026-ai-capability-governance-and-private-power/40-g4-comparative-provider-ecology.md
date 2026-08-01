# G4 — Comparative Provider Ecology

Status: completed as a public-governance comparison; not a behavioral ranking

## Compared governance modes

G4 adds five materially different cases to the OpenAI/Anthropic deep cases:

- hosted API with configurable safety and explicit abuse logging — Google Gemini;
- hosted service with broad contractual restrictions and discretionary monitoring — xAI;
- China-based hosted API with public terms and state-linked content/compliance duties — DeepSeek;
- China/Singapore-linked hosted API with explicit API content review and no-training claim — Kimi;
- downloadable weights governed by a private community license and acceptable-use policy — Meta Llama 4.

Provider files:

- [`providers/google.md`](providers/google.md)
- [`providers/xai.md`](providers/xai.md)
- [`providers/deepseek.md`](providers/deepseek.md)
- [`providers/kimi.md`](providers/kimi.md)
- [`providers/meta-open-weight.md`](providers/meta-open-weight.md)

## Comparative matrix

| Case | Distribution | Rule enforcement point | Monitoring disclosure | Capability differentiation | Exit strength | Main residual concentration |
|---|---|---|---|---|---|---|
| OpenAI | hosted chat/API/agent | Provider request, model, account, product | classifiers, reasoning models, hashes, human review | Trusted Access, model/surface/account class | medium | frontier model, private state, account and product |
| Anthropic | hosted chat/API/cloud channels | Provider classifier, model, account, organization | Safeguards monitoring and aggregate enforcement | organization verification, retention and channel conditions | medium | constitution, access licensing, Provider/cloud path |
| Google Gemini | hosted API/AI Studio/cloud | automated/manual abuse monitoring, safety settings, project/account | 55-day abuse data for Gemini API; project review | paid/free, region, safety settings, model routing and review | medium | Google project/account/cloud and safety approval |
| xAI | hosted consumer/enterprise/API | Provider safeguards, account and service access | monitoring and account review reserved; less quantified | consumer/enterprise and feature/persona differences | medium | service, X integration, broad contractual discretion |
| DeepSeek | hosted consumer/API | Provider moderation, account/API and Chinese legal compliance | terms/privacy disclose processing; less mechanism detail | consumer/API/model variants and region/legal eligibility | medium | hosted model, China jurisdiction, account and API |
| Kimi | hosted consumer/API/agent tools | built-in content review, request errors, account/platform | API safety review and request ID; limited enforcement statistics | consumer/API/enterprise; region and product differences | medium | hosted service, platform account, content-review implementation |
| Meta Llama 4 | downloadable weights under license | license/AUP, distributors, deployer, cloud/host chosen by user | no central inference monitoring after lawful local download by default | 700M MAU special license; EU multimodal and trade restrictions | high for inference continuity | hardware, cloud, license, distribution, updates and upstream weights |

## Findings

### 1. Hosted versus downloadable is the largest structural split

Hosted Providers can change model routing, request handling, account access, and
retention without the user possessing the model. Downloadable weights reduce
remote request-level revocation and permit local behavioral modification.

They do not eliminate:

```text
license conditions
trade and regional restrictions
hardware and cloud concentration
upstream weight and update control
distributor account controls
legal liability
```

### 2. Google exposes unusually concrete operational monitoring terms

The Gemini API documentation states that automated systems scan usage, suspicious
projects may receive manual review, and prompts/responses may be retained for 55
days for abuse prevention and legal disclosure. Interventions can include contact,
rate or model changes, temporary suspension, account closure, and appeal links.

This is more operationally specific than many Provider pages, though it still
does not disclose classifier thresholds or error rates.

### 3. xAI's freedom rhetoric coexists with broad private ordering

xAI states an aim to maximize user control, but its 2026 AUP prohibits jailbreak,
adversarial prompting, prompt injection, model distillation, scraping, protective-
measure bypass, hacking, and broad harmful/illegal uses. Enterprise terms reserve
monitoring and immediate termination and prohibit probing, scanning, penetration,
and benchmarking of the service.

The relevant comparison is therefore not branding. It is the exact surface,
contract, monitoring, account consequence, and exit path.

### 4. DeepSeek and Kimi publish less enforcement-process detail

Both publish current terms and privacy materials. Kimi additionally states that
API inputs/outputs are not used for model training and describes built-in content
review returning an error with a request ID. Public materials provide less detail
about account-level thresholds, aggregate bans, reversal counts, or independent
appeal than Anthropic and less operational monitoring detail than Google.

Absence of disclosure is not evidence that monitoring or enforcement is absent.
It is a legibility finding.

### 5. Open-weight licenses retain private constituent power

Llama 4 permits broad download, modification, derivative work, and redistribution,
but remains a private community license, not an OSI-style unrestricted grant. It
incorporates an Acceptable Use Policy, trade compliance, attribution and naming
conditions, a special license requirement above 700 million monthly active users,
and regional restrictions for some multimodal rights.

Open weights therefore strengthen technical exit while preserving upstream legal
and supply-chain power.

## G4 disposition

Retain the **governance-mode taxonomy**, not a Provider score:

```text
hosted discretionary service
hosted administratively tiered service
cloud/project monitored service
jurisdiction-bound hosted service
licensed downloadable weights
fully permissive or public-domain weights (not represented by Llama)
```

Any future recommendation must name the user's required capability, data mode,
region, state portability, Tool authority, and tolerance for legal/operational
concentration.
