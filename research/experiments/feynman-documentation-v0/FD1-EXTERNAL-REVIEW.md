# FD1 external documentation review

FD1 compares Ordivon's strongest existing explanations with mature external documentation practices. The purpose is not to import a branded framework. It is to identify which repeated reader problems already have stable solutions elsewhere, which solutions fit Ordivon's authority/currentness model, and which should remain outside the Feynman rewrite.

All external material below was reviewed on 2026-08-12 from the named primary/official sources. The notes are paraphrases, not copied style rules.

## External source set

| Source | What it optimizes | Useful pressure for Ordivon | Disposition |
| --- | --- | --- | --- |
| [Diátaxis](https://diataxis.fr/) | separate tutorials, how-to guides, reference, and explanation by reader need | one document cannot simultaneously optimize learning, doing, lookup, and understanding | **adopt the separation principle; reject mandatory site taxonomy** |
| [GitHub Docs content design principles](https://docs.github.com/en/contributing/writing-for-github-docs/content-design-principles) | user goals, clarity, meaning, correctness, consistency, and just-enough documentation | documentation volume has a discovery cost; structure should follow what the reader is trying to do | **adopt** |
| [GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) | first repository orientation: what, why useful, how to start, where to get help | README is an entry surface, not the place to reproduce the whole implementation or research history | **adopt and strengthen with Ordivon authority/currentness boundaries** |
| [GitHub content model](https://docs.github.com/en/contributing/style-guide-and-content-model/about-combining-multiple-content-types) | combine content types only when a reader needs them together; keep reference quickly easy to consult | conceptual context can surround reference, but large exact inventories should not dominate explanation | **adopt selectively** |
| [Google developer documentation style guide](https://developers.google.com/style/highlights) | clear actor, active voice, second-person instructions, conditions before actions, globally readable language | causal responsibility is easier to reconstruct when the actor/owner is grammatical subject | **adopt as sentence-level default, not a semantic authority rule** |
| [Microsoft scannable content](https://learn.microsoft.com/en-us/style-guide/scannable-content/) | important information first, short sections, headings/lists/tables as visual landmarks | long expert prose should reveal its judgment before derivation and let readers stop early | **adopt** |
| [Stripe quick-start guides](https://docs.stripe.com/quickstarts guides) | outcome/use-case-first entry with end-to-end examples and short implementation paths | action docs should route by desired outcome rather than explain the entire platform before first success | **adopt for quick-start guides/how-to; reject as README replacement** |
| [The Rust Programming Language](https://doc.rust-lang.org/stable/book/ch00-00-introduction.html) | declared audience, multiple reading paths, concept chapters plus project chapters, deliberate failing examples | readers can enter by practice or concept; examples that fail can teach boundaries better than perfect happy paths | **adopt for learning paths and counterexamples** |
| [Kubernetes concepts/tasks/tutorials](https://kubernetes.io/docs/concepts/) | explicit separation of understanding, single tasks, and larger guided goals | reinforces that conceptual explanation should not absorb task/reference material | **adopt the separation principle** |
| [Write the Docs documentation principles](https://www.writethedocs.org/guide/writing/docs-principles/) | currentness, examples, ease of scanning, and disjoint source scopes | incorrect/stale duplication is worse than an owner link; multiple sources are safe only when their scopes are disjoint | **strongly adopt because it matches owner-native authority** |

## Where the external systems converge

### 1. Start by choosing the reader's job

Diátaxis, GitHub's content model, and Kubernetes all converge on a simple fact: a reader who wants to understand a system is not in the same mode as a reader trying to execute one command or look up an exact field. Ordivon should therefore rewrite as causal explanation **entry and explanation paths**, not every document.

### 2. The entry surface must orient before it inventories

GitHub's README guidance treats the README as a first encounter with what a project does, why it is useful, and how to begin. Stripe similarly routes readers to concrete outcomes before exposing the entire API. This supports moving phase genealogy, detailed platform requirements, and large capability inventories below the first causal journey.

### 3. Exact reference can stay dry

GitHub's reference model explicitly optimizes fast lookup and structured presentation. Ordivon should not turn Tool catalogs, contracts, operations tables, or protocol fields into narrative prose merely to make the repository feel stylistically uniform.

### 4. Actor clarity is semantic clarity

Google's preference for active voice is especially relevant to Ordivon because many of our hardest errors are ownership errors. `Runtime records the local Attempt` is stronger than `the Attempt is recorded` when the identity of the actor constrains what the evidence can prove.

### 5. Put the judgment before the derivation

Microsoft's scan-friendly structure guidance and GitHub's user-centered content design both favor leading with the important information and making long material navigable. This matches Human's executive judgment and Security's `Decision` opening: a reader should learn the retained rule before encountering the experiment genealogy that produced it.

### 6. Examples should expose the boundary, not decorate the page

Rust's project chapters and intentional failure examples, Stripe's end-to-end quick-start guides, and Write the Docs' example guidance all support examples that let the reader predict or perform something. Ordivon examples earn space when they expose a responsibility boundary, a failure/recovery path, or a choice that changes action.

### 7. Currentness and duplication are documentation correctness

Write the Docs' currentness and source-scope principles strongly match FD0: duplicated current facts create parallel-maintenance failure. Ordivon should link to owner-native technical truth rather than copying it into Computing, Studio, or Web.

## Where Ordivon must go beyond the external patterns

The external systems mostly optimize documentation usability. Ordivon additionally needs three correctness dimensions that are unusually important in a fast-moving multi-owner Agent system:

1. **authority:** which owner can prove the fact;
2. **currentness:** owner-current, published, target, historical, and generated views can differ;
3. **negative proof:** a successful lower-level event must not silently imply a stronger semantic consequence.

These are not reasons to invent a new documentation taxonomy. They are constraints applied to the relevant entry/explanation/currentness passages.

## Rejected external imitation

FD1 explicitly rejects:

- turning every repository into a literal Diátaxis four-folder tree;
- forcing every README into the same section sequence;
- making every technical contract conversational or example-heavy;
- using quickstart success as proof that the reader understands system responsibility;
- importing marketing-style use-case language when the real project pressure is a truth/authority boundary;
- measuring quality mainly by brevity, heading count, or visual scan score.
