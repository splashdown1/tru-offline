# tru requirements matrix

**timestamp:** 21 july 2026, 06:18 america/chicago
**status:** phase 0 specification lock
**implementation status:** planning only
**baseline:** `TRU_APEX10_RELEASE_CANDIDATE.html`

## 1. reading this matrix

- **must:** release-blocking requirement.
- **should:** required for the target phase, but not necessarily every profile.
- **parked:** deliberately deferred; no implementation may assume it is complete.
- **owner:** the architecture layer responsible for the requirement.
- **proof:** the minimum evidence needed to accept the requirement.

this matrix is the acceptance companion to `TRU_MASTER_ROADMAP.md`. existing files and release candidates remain protected.

## 2. global requirements

| id | requirement | priority | owner | proof | release consequence |
|---|---|---|---|---|---|
| G-01 | core boots and answers without internet, api keys, accounts, telemetry, or cloud models | must | sovereign kernel | offline network audit plus tier 1 boot and fixed prompts | block all releases |
| G-02 | existing protected artifacts are preserved and new candidates are additive | must | build/release | changed-file audit and candidate naming check | block candidate promotion |
| G-03 | every release is built from declared canonical inputs | must | build/release | source manifest, builder id, hashes, and clean-build report | block release |
| G-04 | advertised capabilities match modules actually present and ready | must | module/runtime | profile capability test and manifest comparison | block affected profile |
| G-05 | source, synthesis, interpretation, unresolved material, and teaching remain distinguishable | must | provenance/answer | evidence-class audit over fixed and adversarial prompts | block affected route |
| G-06 | failed required tests block release even when visual output improves | must | evaluation | dated report with passed, failed, blocked, and not-applicable totals | block release |
| G-07 | state is independent of knowledge and never required for clean boot | must | state/runtime | first boot without state and damaged-state boot tests | block all profiles |
| G-08 | mobile and maximum-content products remain separate named profiles | must | profile/build | profile manifest and device test | block profile release |

## 3. capability and boundary requirements

| id | limitation addressed | requirement | priority | owner | proof | release consequence |
|---|---|---|---|---|---|---|
| C-01 | not a general-purpose neural language model | describe deterministic core capability accurately; do not imply unrestricted neural knowledge | must | product contract | README, manifest, and status wording review | block release documentation |
| C-02 | optional neural enhancement | if added, local and offline; optional; explicit; removable; never authority for facts or citations | parked | enhancement adapter | core-only comparison, network block, provenance audit | no adapter release until all pass |
| C-03 | unsupported queries | unsupported or insufficiently grounded input returns a useful named gap with next action | must | router/gap | unsupported and negative-control corpus | block affected route |
| C-04 | user teaching | teaching persists under a teaching label and is never silently cited as canonical source | must | state/provenance | teaching, reload, export/import, and citation tests | block state release |
| C-05 | identity | identity responses remain project-defined and distinguish product voice from factual source evidence | should | answer/provenance | identity regression family and evidence-class review | block only if identity contract is advertised |

## 4. routing and retrieval requirements

| id | requirement | priority | owner | proof | release consequence |
|---|---|---|---|---|---|
| R-01 | preserve specialist priority for exact scripture, strong’s, define, commentary, help, status, and state commands | must | router | fixed route corpus with expected routes | block route release |
| R-02 | report normalised query, intent, routes considered, candidates, reranking, selected evidence, answer class, and gap reason | must | observability | route-trace schema and trace completeness test | block phase 1 exit |
| R-03 | retrieve a candidate set rather than relying on one opaque hit | should | retrieval | useful-top-3 benchmark | block phase 2 exit |
| R-04 | rerank by intent, source class, node type, authority, and evidence compatibility | should | reranker | source-type precision and wrong-route benchmark | block phase 2 exit |
| R-05 | detect ambiguity and present alternatives or request clarification when evidence is weak | must | router/gap | ambiguous terms: grace, faith, logos, spirit, life | block affected route |
| R-06 | use explicit confidence bands: high, medium, low, or gap | must | evidence contract | calibration report against labelled cases | block phase 1 exit |
| R-07 | expose contradictions and duplicates instead of silently flattening them | should | retrieval/provenance | contradiction and duplicate corpus | block phase 2/5 exit |
| R-08 | preserve current fixed smoke prompts and verified APEX10 prompts as regression cases | must | evaluation | tier 2 report with exact totals | block all engine candidates |

## 5. answer quality and interpretation requirements

| id | requirement | priority | owner | proof | release consequence |
|---|---|---|---|---|---|
| A-01 | separate answer content from presentation mode | should | answer planner | concise, standard, and deep output checks | block phase 4 exit |
| A-02 | compose only from accepted evidence payloads | must | answer planner/provenance | source payload before/after comparison | block affected route |
| A-03 | attach citations or source ids to the claims they support | must | provenance | citation attachment audit | block release |
| A-04 | no markup leakage into visible answer or text-to-speech text | must | renderer/voice | rendered text and TTS sanitisation test | block release |
| A-05 | improve clarity, coherence, usefulness, naturalness, and length without increasing unsupported claims | should | answer planner/evaluation | blind 1–5 review plus grounding comparison | block phase 4 exit |
| A-06 | every interpretive sentence declares interpretation layer and supporting evidence | must | PaRDeS/provenance | interpretive trace audit | block phase 5 exit |
| A-07 | peshat, remez, derash, and sod use distinct evidence rules | must | PaRDeS review | positive/negative controls for each layer | block phase 5 exit |
| A-08 | sod is opt-in and never silently stated as direct source fact | must | PaRDeS/UI | default and opt-in tests | block release |
| A-09 | unsupported theological or typological leaps are labelled unresolved or omitted | must | PaRDeS/gap | adversarial overclaim corpus | block release |
| A-10 | council disagreement remains visible when multiple accepted views differ | should | council/answer | disagreement fixture and output review | block phase 4 exit |

## 6. runtime, performance, and profile requirements

| id | requirement | priority | owner | proof | release consequence |
|---|---|---|---|---|---|
| P-01 | shell renders before nonessential modules load | must | runtime/kernel | load-sequence trace | block phase 3 exit |
| P-02 | first supported query becomes interactive before archive-only modules load | must | runtime/profile | first-answer timing test | block phase 3 exit |
| P-03 | every module reports bytes, records, schema, checksum, dependencies, and load state | must | manifest/runtime | manifest/runtime comparison | block phase 1/3 exit |
| P-04 | core, study, complete, max, and exported-state profiles are explicit | must | profile/build | profile matrix and capability test | block profile release |
| P-05 | mobile excludes archive-only material by default | must | profile/build | low-memory mobile profile inspection | block mobile release |
| P-06 | numeric file, cold-start, first-answer, peak-memory, steady-state, and readiness budgets are recorded before optimisation | must | performance/evaluation | dated baseline report | block phase 0/1 exit |
| P-07 | profile never claims ready before required modules work | must | runtime/manifest | forced delayed or failed module test | block affected profile |
| P-08 | long sessions do not silently grow retained answers or lose state | should | runtime/state | long-session memory and reload test | block phase 3/6 exit |
| P-09 | maximum archive remains reproducible even when practical profile is split | must | build/release | clean max rebuild and checksum report | block max release |

## 7. state and portability requirements

| id | requirement | priority | owner | proof | release consequence |
|---|---|---|---|---|---|
| S-01 | every event has id, type, timestamp, schema version, session id, payload, profile, and optional parent | must | state | event schema validation | block state release |
| S-02 | valid event is written before dependent visible state is updated | must | state/runtime | interrupted-write fixture | block state release |
| S-03 | last valid checkpoint survives malformed or partial later data | must | state/recovery | corruption and recovery test | block state release |
| S-04 | reload, close/reopen, export/import, and profile migration preserve supported state | must | state/migration | state tier report | block state release |
| S-05 | quota pressure warns and offers inspectable export without silent deletion | must | state/UI | quota fixture and warning review | block state release |
| S-06 | imported state shows restored, skipped, and incompatible records | must | state/import | import report fixture | block state release |
| S-07 | source knowledge, conversation memory, teaching, and sealed material remain distinguishable | must | state/provenance | cross-profile citation and UI audit | block release |

## 8. packaging, provenance, and release requirements

| id | requirement | priority | owner | proof | release consequence |
|---|---|---|---|---|---|
| B-01 | every module has stable id, schema, source class, licence note, source hash, size, count, transform history, and review status | must | data intake | manifest audit | block release |
| B-02 | transformed data remains traceable to preserved input | must | data intake | sample round-trip/provenance audit | block release |
| B-03 | no secrets, binaries, build noise, or unverified overrides enter release profiles | must | data intake/build | static scan and staged-file audit | block release |
| B-04 | doctrine, routing, identity, remez, and sod changes receive separate review | must | review/evaluation | review record plus positive/negative controls | block affected release |
| B-05 | manifest matches embedded payload and package members | must | build/release | manifest/hash comparison | block release |
| B-06 | checksums verify after packaging and extraction | must | build/release | package verification | block release |
| B-07 | release notes state exact artifact, profile, source, builder, tests, failures, limitations, and state compatibility | must | release | dated release-note audit | block release |
| B-08 | failed candidates remain preserved and are not relabelled as releases | must | release | failure artifact and rollback inspection | block promotion |
| B-09 | offline network audit passes for every offline profile | must | evaluation/release | static and runtime network audit | block release |

## 9. phase gates

### gate 0 — blueprint approved

required:

- roadmap and matrix accepted
- product definition and boundaries settled
- release profiles named
- optional neural work parked unless separately approved
- benchmark families and regression seed identified
- numeric performance baseline collection authorised

### gate 1 — architecture approved

required:

- module and manifest contract
- structured result and route trace contract
- state event and export contract
- profile load sequence
- provenance/evidence-class rules

### gate 2 — evaluation approved

required:

- labelled routing corpus
- retrieval relevance labels
- grounding and interpretation rubric
- device targets and measurement protocol
- release-blocking thresholds

### gate 3 — implementation approved

required:

- phase scope named
- affected files named
- protected baseline verified
- additive candidate path prepared
- rollback path prepared

### gate 4 — release approved

required:

- all required tests pass
- manifests and checksums agree
- offline audit passes
- profile claims are true
- state lifecycle passes
- release note is complete

## 10. current decision record

- **deterministic core:** approved and protected as the foundation.
- **modular profiles:** approved direction.
- **hybrid candidate retrieval and reranking:** approved direction for phase 2.
- **provenance-gated PaRDeS:** approved direction; no unreviewed interpretive expansion.
- **portable append-only state:** approved direction.
- **optional local neural adapter:** parked until the deterministic baseline and observability gates pass.
- **cloud dependency:** rejected for the offline product.
- **phase 1:** measurement and observability only; no answer-behaviour changes.

## 11. minimum phase 1 proof package

before implementation moves beyond observability, the following dated artifacts must exist:

1. baseline artifact hash and size.
2. route trace schema and sample traces.
3. fixed regression report with exact pass/fail totals.
4. offline network audit.
5. shell, interactive, first-answer, full-readiness, and memory measurements.
6. storage/state baseline.
7. changed-file audit proving protected artifacts were not overwritten.
8. phase 1 exit report naming every blocked or not-applicable test.
