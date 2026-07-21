# tru master roadmap

**timestamp:** 21 july 2026, 06:18 america/chicago
**status:** phase 0 specification lock
**implementation status:** planning only; no engine code authorised by this document
**protected baseline:** `TRU_APEX10_RELEASE_CANDIDATE.html`
**repository:** `tru-offline`

## 1. purpose

this is the single coordinating roadmap for the next tru generation. it reconciles the existing blueprint and sop library with the current project instructions. it does not replace the existing build, provenance, evaluation, performance, memory, or release sops. those documents remain the operating procedures for their areas.

tru next will improve retrieval, answer quality, startup, maintainability, persistence, and interpretive discipline while preserving the defining constraint:

> tru remains useful, inspectable, and complete at its core with no internet, api key, account, or required cloud model.

## 2. authoritative product definition

**tru is a modular, offline-first personal intelligence system.** its sovereign deterministic core retrieves and composes answers from declared local knowledge. specialist modules add scripture, dictionary, lexical, commentary, reference, and interpretive capabilities. portable state carries the user’s conversation, teachings, seals, preferences, and feedback separately from source knowledge.

tru is not presented as a general-purpose neural language model. an optional local neural adapter may improve composition or query expansion only after the deterministic core passes its own gates. the adapter is never the authority layer and never becomes a required dependency.

## 3. non-negotiable constraints

1. **offline sovereignty:** no required network request, api key, account, telemetry service, or cloud model.
2. **protected artifacts:** existing releases, source data, and lineage files remain preserved. new work is additive until a specific replacement is approved.
3. **evidence before claims:** route, retrieval, confidence, provenance, state, and performance must be measurable.
4. **fact boundary:** retrieved source, synthesis, interpretation, unresolved possibility, and user teaching remain visibly distinct.
5. **profile separation:** core, study, complete, max, and exported-state products are named and accurately reported.
6. **reproducibility:** builds come from canonical inputs, declared transforms, manifests, and checksums.
7. **release discipline:** a failed required test blocks release; visual improvement does not override a regression.
8. **state independence:** missing or damaged state never prevents a clean boot.
9. **no silent degradation:** absent modules, low confidence, and profile limits are reported instead of concealed.

## 4. product architecture

### 4.1 sovereign kernel

small startup-critical layer containing:

- shell and interaction state
- query normalisation
- intent and route selection
- confidence and gap policy
- answer/evidence contract
- offline capability checks
- state read/write contract
- manifest and module readiness display

### 4.2 knowledge modules

separate declared packs containing the brain, kjv, strong’s, dictionary, commentary, cross-references, encyclopedia, filings, and future approved sources. every pack carries identity, schema, source class, licence note, record count, size, checksum, dependencies, and supported profile(s).

### 4.3 retrieval and reasoning

staged processing:

1. normalise the query and extract entities.
2. detect intent and candidate routes.
3. run exact and alias lookups.
4. run lexical retrieval.
5. expand with approved local synonyms or aliases.
6. rerank by intent, source class, type, authority, and evidence compatibility.
7. detect duplication, contradiction, and ambiguity.
8. select evidence or return a gap.
9. create an answer plan.
10. compose only from the accepted evidence.

### 4.4 answer and interpretation layers

all result sentences belong to one declared evidence class:

- **source** — directly retrieved material
- **synthesis** — combination of accepted sources
- **interpretation** — declared doctrinal, typological, applied, or theological reading
- **unresolved** — possible connection below the settled-evidence threshold

PaRDeS remains available, but peshat, remez, derash, and sod must carry their supporting evidence and boundary labels. sod is opt-in and never silently presented as direct fact.

### 4.5 portable state

state is an independent append-only event stream with checkpoints, export/import, recovery, migration, and quota handling. it includes conversation turns, teachings, seals, release intentions, feedback, bookmarks, preferences, and migration records. it never silently becomes canonical knowledge.

## 5. release profiles

| profile | purpose | required content | priority |
|---|---|---|---|
| **core** | fastest evaluation and low-memory use | kernel, essential brain, kjv, help, status, gap handling | startup and memory |
| **study** | scripture and theology | core plus dictionary, strong’s, commentary, and approved xrefs | specialist usefulness |
| **complete** | everyday desktop use | study plus approved broad reference modules | balance |
| **max** | research and preservation | all approved modules and archive material | content |
| **exported state** | personal continuity | any profile plus portable state package | recovery and portability |

no profile may claim a capability until the corresponding module is actually ready. the maximum archive must never be the hidden default burden on mobile.

## 6. phased execution plan

### phase 0 — specification lock

**goal:** freeze terminology, boundaries, profiles, benchmark seed, and budgets before implementation.

**deliverables:** this roadmap; `TRU_REQUIREMENTS_MATRIX.md`; accepted test corpus; numeric baseline plan; decision record for optional neural work.

**exit gate:** all requirements have an owner, acceptance test, profile scope, and release consequence; contradictions between the roadmap, `README_NEXT.md`, `BUILD_SOP.md`, and the docs library are resolved.

### phase 1 — observability baseline

**goal:** expose current behaviour without changing answer behaviour.

**deliverables:** structured result contract, route trace, provenance fields, confidence state, performance measurements, storage measurements, baseline report for the protected APEX10 candidate.

**exit gate:** a test can identify route, candidates, selected evidence, confidence, answer class, module readiness, latency, and failure reason.

### phase 2 — routing and retrieval reliability

**goal:** reduce wrong-route answers and improve useful recall.

**deliverables:** intent taxonomy, candidate sets, exact/lexical/alias retrieval, source-aware reranking, ambiguity handling, gap thresholds, negative controls.

**exit gate:** wrong-route rate falls and useful-top-3 rate rises without fixed-prompt, grounding, or provenance regression.

### phase 3 — modular runtime and device profiles

**goal:** make practical builds fast without discarding max content.

**deliverables:** module manifest v2, profile builders, load states, lazy specialist packs, mobile limits, optional-module failure handling.

**exit gate:** core and study profiles meet measured startup/first-answer/memory budgets; max remains reproducible and accurately labelled.

### phase 4 — answer composition and council

**goal:** improve clarity and naturalness while preserving evidence.

**deliverables:** answer plans, concise/standard/deep modes, truth/witness/reason views, feedback signals, composition benchmark.

**exit gate:** blind review improves clarity and naturalness; source attachment remains correct; disagreement is not hidden.

### phase 5 — provenance-gated recursive interpretation

**goal:** make PaRDeS and recursive reasoning useful without turning speculation into fact.

**deliverables:** source-to-synthesis graph, four evidence classes, interpretive boundary labels, contradiction handling, review process for new typology and sod patterns.

**exit gate:** every interpretive claim traces to accepted evidence and unsupported leaps are marked unresolved or omitted.

### phase 6 — durable state and portable identity

**goal:** make memory survive reload, export, import, profile changes, and failed writes.

**deliverables:** event journal, checkpoints, state package, quota policy, recovery and migration tests.

**exit gate:** teachings, sessions, bookmarks, and preferences survive the supported lifecycle; damaged state cannot destroy the last valid recovery point.

### phase 7 — optional local neural composition

**goal:** add local language assistance without weakening sovereignty or grounding.

**deliverables:** adapter contract, model/runtime matrix, offline package, fallback behaviour, enhanced-mode benchmark.

**exit gate:** core-only mode remains complete; enhanced mode is explicit; no generated citation or factual payload can bypass evidence.

this phase is parked until phases 1–6 establish a reliable baseline. no cloud model is in scope.

### phase 8 — reproducible release and distribution

**goal:** ship dependable practical, study, complete, max, and state products.

**deliverables:** clean build pipeline, manifests, checksums, package channels, release notes, rollback package.

**exit gate:** all required static, boot, regression, provenance, performance, state, offline, and packaging tests pass.

## 7. phase 1 implementation boundary

phase 1 may add measurement and inspectability only. it may not silently change routing, ranking, answer wording, source data, PaRDeS behaviour, state semantics, or release identity.

required observations:

- original and normalised query
- route candidates and selected route
- candidate ids and scores
- selected evidence ids and source classes
- confidence band
- answer class and answer mode
- transformation/synthesis steps
- unresolved or contradiction flags
- module load state
- shell, interactive, first-answer, and full-readiness timings
- memory and storage measurements where available
- state generation and recovery status

## 8. baseline artifacts and protection

- protected baseline: `TRU_APEX10_RELEASE_CANDIDATE.html`
- prior comparison: `TRU_APEX9.html`
- modular source tree: `Projects/TRU/current/`, `Projects/TRU/data/`, `Projects/TRU/build-scripts/`, and `Projects/TRU/ship/`
- existing operating documents: `BUILD_SOP.md`, `DATA_INVENTORY.md`, `MODIFICATION_GUIDE.md`, and the docs library
- experimental variants remain lineage or comparison artifacts until explicitly promoted

no phase may overwrite the protected baseline. every candidate receives a new name and a dated report.

## 9. definition of done

tru next is ready when a user can:

- open a practical profile quickly on desktop and phone
- ask a question and see the route and confidence boundary when needed
- distinguish source, synthesis, interpretation, unresolved material, and teaching
- receive a useful answer or an honest gap
- use scripture and specialist modules without loading the archive
- reload, export, import, and recover personal state
- rebuild profiles from canonical sources with matching manifests and checksums
- use the system with no internet, account, api key, or required neural model

**next authorised work:** phase 1 measurement and observability design, with no feature or answer-behaviour changes.
