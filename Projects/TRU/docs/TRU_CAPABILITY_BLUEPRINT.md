# tru capability blueprint

**timestamp:** 21 july 2026, 05:25 america/chicago
**status:** design only; no code or data changes

this document translates the eight limitations from the audit into concrete system boundaries and acceptance tests.

## 1. capability model

tru should report capability by layer instead of using one vague intelligence label.

| layer | promise | does not promise |
|---|---|---|
| retrieval | finds relevant embedded material | complete world knowledge |
| grounded answer | states or quotes material with provenance | unrestricted conversation |
| synthesis | combines accepted evidence into an answer | new factual authority |
| interpretation | offers a declared reading of evidence | proof that an interpretation is objectively exhaustive |
| teaching | stores user-provided knowledge under a teaching label | automatic verification of the teaching |
| local enhancement | improves query expansion or language composition | permission to invent sources or facts |
| gap | identifies absent or insufficient evidence | a failure-free answer to every question |

## 2. limitation: not a general-purpose neural language model

### blueprint

keep the deterministic engine as the sovereign authority layer. add capability through composition and optional local enhancement rather than hiding a cloud dependency inside the product.

### required behaviour

- core-only mode answers from embedded data and declared rules.
- enhanced mode is explicitly named in status and export metadata.
- generated language cannot create a citation, source, verse, or node that was not supplied by the evidence layer.
- a missing model never prevents core boot.
- query types unsupported by the current layer return a useful gap with next action.

### acceptance tests

- disconnect or block all network access; core still boots and answers fixed prompts.
- remove optional enhancement; core still passes the same grounding tests.
- compare source payload before and after composition; factual payload is unchanged.
- ask a broad conversational prompt; response either composes from evidence or reports the boundary plainly.

## 3. limitation: data and routing quality

### blueprint

replace one verdict with a route trace and candidate set.

route trace fields:

1. normalised query.
2. detected intent and confidence.
3. routes considered.
4. candidates returned by each route.
5. reranking factors.
6. selected evidence.
7. final answer class.
8. gap or ambiguity reason when applicable.

### routing policy

- exact scripture reference has priority when the input is a reference.
- explicit dictionary and strong's requests retain their specialist route.
- explicit commentary requests retain commentary route.
- doctrine and identity questions use curated entries before broad retrieval.
- broad factual questions use hybrid candidate retrieval.
- ambiguous queries return the best supported candidates, not an arbitrary single hit.

### acceptance tests

- measure route accuracy by intent family.
- measure wrong-route rate separately from no-answer rate.
- test ambiguous terms such as grace, faith, logos, spirit, and life in multiple phrasings.
- test negative controls designed to attract irrelevant nodes.

## 4. limitation: large builds and phones

### blueprint

separate code, indexes, and data modules. the first screen should not require every module to be parsed.

runtime rules:

- kernel loads first.
- core brain and essential scripture index load next.
- specialist packs load on demand or by profile.
- commentary, encyclopedia, filings, and archive material never load into the mobile profile unless explicitly selected.
- every module reports bytes, records, schema version, and load state.
- failed optional module loads degrade to a named gap, not a silent empty object.

### profiles

- core: smallest useful system.
- study: scripture, dictionary, strong's, commentary.
- complete: everyday broad reference.
- max: archive and research.

### acceptance tests

- cold start time measured from file open to interactive state.
- first answer time measured separately from full module readiness.
- peak memory measured during boot and after a representative session.
- mobile profile tested on a low-memory phone target and a modern phone target.
- no profile claims a module is available until its manifest and lookup are ready.

## 5. limitation: deterministic retrieval and nuance

### blueprint

use a staged retrieval pipeline:

1. query normalisation and entity extraction.
2. intent classification.
3. exact and alias lookup.
4. lexical retrieval.
5. semantic or synonym expansion from local resources.
6. source/type-aware reranking.
7. contradiction and duplication checks.
8. answer selection or candidate presentation.

this is still deterministic in core mode. the improvement comes from combining evidence paths and making uncertainty visible.

### confidence bands

- **high:** exact or strongly supported match with compatible source type.
- **medium:** several related hits agree, but wording or intent is not exact.
- **low:** weak lexical match, conflicting material, or broad interpretation.
- **gap:** no candidate meets the minimum evidence threshold.

### acceptance tests

- top-1 exactness.
- useful-top-3 rate.
- source-type precision.
- duplicate-answer rate.
- contradiction exposure rate.
- confidence calibration: high-confidence answers must fail less often than medium-confidence answers.

## 6. limitation: naturalness

### blueprint

separate answer content from answer presentation.

answer plan fields:

- opening verdict.
- evidence blocks.
- explanation blocks.
- related references.
- boundary or gap statement.
- optional next question.

presentation modes:

- concise: verdict plus strongest evidence.
- standard: verdict, explanation, and sources.
- deep: layered synthesis, alternatives, and interpretation boundary.

naturalness must come from controlled composition, not unsupported improvisation.

### acceptance tests

- blind rating for clarity, coherence, usefulness, and naturalness.
- source retention score: citations remain attached to the claims they support.
- no repeated opening or duplicated conclusion.
- no html or markup leakage into text-to-speech.
- answer length stays within the selected mode.

## 7. limitation: speculative recursive interpretation

### blueprint

make every answer sentence belong to one evidence class:

1. **source:** directly retrieved or quoted.
2. **synthesis:** combination of two or more accepted sources.
3. **interpretation:** a declared reading, typology, doctrine, or application.
4. **unresolved:** a possible connection not strong enough to present as settled.

pardes remains valuable, but each layer must carry its evidence class and supporting references.

### rules

- peshat may state direct textual meaning.
- remez must identify the typological or thematic bridge.
- derash must identify the doctrine or application being applied.
- sod must be opt-in, clearly labelled, and supported by the project’s accepted source boundary.
- a pattern match alone is not proof of a theological conclusion.
- unresolved connections may be shown as questions or omitted from the default answer.

### acceptance tests

- every interpretive output has a traceable support list.
- unsupported claims are downgraded to unresolved or rejected.
- reviewers can distinguish source text from tru’s composition.
- changing one source changes only the dependent synthesis, not unrelated facts.

## 8. limitation: maintainability and distribution

### blueprint

maintain one canonical source graph and compile named profile outputs from it. do not hand-patch giant html exports as the normal workflow.

required metadata per module:

- stable id.
- schema version.
- source path.
- source class.
- licence or usage note.
- record count.
- uncompressed and compressed bytes.
- content hash.
- build timestamp.
- builder version.
- dependencies.

### acceptance tests

- clean rebuild from a known source tree.
- manifest and embedded content agree.
- no undeclared slot remains empty.
- checksums verify after packaging and extraction.
- profile output names and capability claims match the manifest.

## 9. limitation: browser storage and session memory

### blueprint

use a portable state model independent of the data profile.

state categories:

- conversation events.
- user teachings.
- sealed nodes and release intentions.
- preferences and voice settings.
- answer feedback.
- bookmarks and saved studies.
- export and migration metadata.

state rules:

- each event has an id, timestamp, type, payload, and schema version.
- writes are append-first and recoverable.
- checkpoints provide faster restore without changing the original event record.
- state is inspectable and exportable.
- quota pressure produces a visible state warning and export path.
- an empty or damaged state package never blocks a clean boot.

### acceptance tests

- reload preserves the active conversation.
- close and reopen preserves a teaching.
- export and import preserve events, teachings, and bookmarks.
- interrupted write recovers to the last valid checkpoint.
- a profile upgrade preserves state schema or performs a recorded migration.

## 10. the product promise after these fixes

tru will still have boundaries. the difference is that the boundaries become designed behaviour rather than accidental weaknesses:

- it will not know everything, but it will know what it used.
- it will not be a cloud llm, but it will compose more useful language.
- it will not force a phone to load an archive, but it will offer a practical profile.
- it will not hide interpretation inside fact claims.
- it will not lose a user’s state merely because a browser reloads or a profile changes.
