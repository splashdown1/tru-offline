# tru evolution blueprint

**timestamp:** 21 july 2026, 05:25 america/chicago
**status:** blueprint only; implementation not authorised
**baseline:** `TRU_APEX10_RELEASE_CANDIDATE.html`

## 1. mission

build the next tru as a sovereign, offline-first intelligence system that combines deterministic knowledge retrieval, structured reasoning, optional local neural assistance, durable personal state, and inspectable provenance.

tru will not be defined as a general-purpose neural language model. the target is stronger and more honest:

> tru is a modular personal intelligence system whose deterministic core guarantees sovereignty and grounding, while optional composition and local neural layers improve breadth, fluency, and reasoning without becoming a hidden dependency.

## 2. the eight problems and the strategic answer

| current limitation | strategic answer | first proof |
|---|---|---|
| not a general-purpose neural language model | define a layered capability model; add an optional offline neural adapter only after the deterministic core is reliable | the same query works in core-only mode and clearly labels enhanced mode |
| answers depend on embedded data and routing quality | canonical source graph, hybrid retrieval, candidate sets, reranking, confidence, and explicit gap handling | benchmark measures grounded hit rate and wrong-route rate |
| large builds load slowly, especially on phones | small engine shell, modular data packs, lazy loading, device profiles, and a mobile budget | cold-start and memory budgets pass on a defined phone profile |
| deterministic retrieval misses nuance or chooses the wrong node | retrieve several candidates, classify intent, rerank by type/source/authority, and show alternatives when confidence is low | top-1 accuracy and useful-top-3 accuracy improve without increasing hallucinated answers |
| responses sound less natural than cloud llms | structured answer plans, sentence composition, answer-length control, and optional local composition | blind human rating improves while citations and source boundaries remain intact |
| recursive interpretation can become speculative | four-layer evidence contract: source, synthesis, interpretation, unresolved | every interpretation is visibly marked and traceable to accepted inputs |
| large bundles are hard to maintain and distribute | one canonical data graph, profile manifests, deterministic builds, chunked packs, checksums, and release channels | same source commit produces byte-audited reproducible profile outputs |
| browser storage and session memory are limited | append-only event state, checkpoints, export/import, quota-aware policy, and recovery packages | reload, export, import, and recovery tests pass across the supported browsers |

## 3. product shape

### 3.1 the four layers

1. **sovereign kernel**
   - routing, normalisation, safety boundaries, state contract, provenance contract, and user interface shell.
   - small enough to start quickly.
   - no network requirement.

2. **knowledge modules**
   - brain, kjv, strong's, dictionary, commentary, encyclopedia, cross-references, and future verified sources.
   - each module has a schema, source class, version, checksum, size, licence, and supported queries.

3. **reasoning and composition modules**
   - candidate retrieval, reranking, council views, pardes interpretation, synthesis, answer formatting, and gap generation.
   - each module returns evidence and a typed result rather than an opaque string.

4. **state and export layer**
   - conversation events, teachings, seals, user preferences, confidence feedback, bookmarks, and export metadata.
   - state is portable and never required for first boot.

### 3.2 release profiles

tru should stop treating one giant html file as the only product. it should produce named profiles from the same source graph:

| profile | target user | design target |
|---|---|---|
| **core** | low-memory devices and first evaluation | kernel + brain core + kjv; fastest start |
| **study** | scripture and theology work | core + dictionary + strong's + commentary + xrefs |
| **complete** | everyday desktop use | study + broader reference modules |
| **max** | researchers and offline archives | all approved modules, slower and larger |
| **exported state** | a user’s personal copy | any profile plus portable state package |

one profile must never silently masquerade as another. the boot screen and manifest state exactly what is loaded.

### 3.3 optional local neural adapter

this is a later phase, not a prerequisite. the adapter is allowed only if it satisfies all conditions:

- it runs locally and offline.
- it is optional; core-only mode remains complete and usable.
- it cannot overwrite source evidence.
- it cannot invent citations or claim that generated text is retrieved fact.
- its model, size, licence, runtime, and device requirements appear in the manifest.
- if unavailable, tru falls back to deterministic composition without a broken boot path.

its role is language composition, query expansion, candidate comparison, and explanation. it is not the authority layer.

## 4. phased gameplan

### phase 0 — freeze the contract

**purpose:** settle what tru is before adding capability.

outputs:

- approved product definition.
- accepted terminology for fact, synthesis, interpretation, teaching, gap, and confidence.
- approved release profiles.
- frozen benchmark seed set.
- explicit decision on whether an optional local neural adapter is in scope for the next build or parked.

exit criteria:

- no unresolved contradiction between `README_NEXT.md`, `BUILD_SOP.md`, and this blueprint.
- every requested limitation has an owner document and a measurable target.

### phase 1 — observability before improvement

**purpose:** make failure visible before trying to make answers better.

outputs:

- structured result contract documented.
- route trace design documented.
- source and provenance display design documented.
- benchmark runner specification documented.
- cold-start, memory, and storage measurement protocol documented.

exit criteria:

- a test can identify the selected route, candidate sources, confidence state, answer class, and failure reason.
- baseline numbers exist for the apex10 candidate.

### phase 2 — retrieval and routing reliability

**purpose:** reduce wrong-node answers and improve useful recall.

outputs:

- intent taxonomy.
- candidate-set retrieval instead of single-hit retrieval.
- type/source/authority-aware reranking.
- ambiguity handling.
- explicit gap threshold.
- query families for doctrine, scripture, definition, commentary, factual, planning, and identity questions.

exit criteria:

- wrong-route rate decreases against the baseline.
- useful-top-3 rate increases.
- no regression in fixed smoke prompts.
- low-confidence answers show alternatives or request clarification rather than presenting a weak hit as certain.

### phase 3 — modular runtime and device profiles

**purpose:** fix startup and phone usability without discarding the maximum build.

outputs:

- module manifest v2.
- core/study/complete/max profile specifications.
- lazy module policy.
- mobile memory budget.
- loading and progress states.
- failure recovery when an optional module is unavailable.

exit criteria:

- core profile boots within its approved budget.
- study profile loads scripture workflows without loading unrelated large modules.
- max profile remains available as an archive product.
- every profile reports its actual loaded modules.

### phase 4 — answer composition and council

**purpose:** improve naturalness and usefulness without hiding evidence.

outputs:

- answer-plan specification.
- concise, standard, and deep answer modes.
- truth/witness/reason views from `README_NEXT.md`.
- user feedback signal design.
- composition quality benchmark.

exit criteria:

- answers read naturally in blind review.
- source citations survive composition.
- composition cannot change the underlying fact payload.
- council disagreement is visible rather than flattened into false certainty.

### phase 5 — provenance-gated recursive interpretation

**purpose:** make pardes and future recursive reasoning powerful without allowing unsupported claims to appear as facts.

outputs:

- source-to-synthesis graph.
- four-level evidence display.
- interpretation confidence and boundary labels.
- contradiction and unresolved-meaning handling.
- review policy for new typology and sod patterns.

exit criteria:

- every interpretive sentence can be traced to source nodes and declared transformations.
- unsupported leaps are labelled unresolved or omitted.
- theological interpretation follows the project’s accepted doctrinal boundary rather than arbitrary retrieval proximity.

### phase 6 — durable state and portable identity

**purpose:** make memory survive reloads, exports, browser changes, and profile changes.

outputs:

- append-only state journal specification.
- checkpoint format.
- export/import package format.
- quota policy.
- recovery and migration tests.

exit criteria:

- a teaching survives reload and export/import.
- a session can be restored after a failed write.
- state is not required to boot the engine.
- the user can inspect what tru remembers and why.

### phase 7 — optional local neural composition

**purpose:** add broader language ability while preserving the sovereign core.

outputs:

- adapter contract.
- approved model/runtime matrix.
- offline packaging plan.
- fallback behaviour.
- separate enhanced-mode evaluation set.

exit criteria:

- core-only and enhanced-mode answers are distinguishable in logs and ui.
- enhanced mode never fabricates provenance.
- removing the adapter does not break the core build.
- device profiles state whether the adapter is installed and active.

### phase 8 — release engineering and distribution

**purpose:** turn the modular system into dependable products.

outputs:

- reproducible build pipeline.
- profile manifests and checksums.
- practical downloads, archive downloads, and state exports.
- release notes with known limitations.
- rollback and recovery package.

exit criteria:

- clean rebuild from canonical inputs succeeds.
- every published artifact has a matching manifest.
- offline network-audit passes.
- all required benchmark, boot, reload, export, and profile tests pass.

## 5. definition of done for the next tru generation

tru is not ready because it contains more data. it is ready when:

- a user can open a practical profile quickly on desktop and phone.
- a question follows the correct route or transparently reports ambiguity.
- answers distinguish retrieved fact, composed synthesis, interpretation, and gap.
- source evidence is visible without making the interface unusable.
- memory survives the supported lifecycle.
- builds are reproducible and profiles are maintainable.
- the maximum archive remains available without forcing every user to load it.
- the system remains useful with no internet, no api key, and no neural model.

## 6. decisions deliberately postponed

- which local neural runtime, if any, becomes the first adapter.
- whether the council is always visible or user-invoked.
- exact mobile size and memory budgets after baseline measurement.
- which additional sources qualify for inclusion.
- whether the online counterpart mirrors every offline profile or only the public behaviour contract.

these are decisions for phase 0, not assumptions to smuggle into implementation.
