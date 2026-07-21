# tru data and provenance sop

**timestamp:** 21 july 2026, 05:25 america/chicago
**status:** planning sop; no ingestion or build changes authorised

## purpose

this sop controls what may enter tru, how it is labelled, how it reaches an answer, and how interpretation is kept separate from source fact.

## 1. source classes

| class | meaning | default answer authority |
|---|---|---|
| `canonical` | approved project source for a defined domain | highest within that domain |
| `reference` | external or historical reference material accepted for lookup | high, with citation |
| `commentary` | interpretive or explanatory material | explanatory, not raw fact authority |
| `teaching` | user-provided material stored by tru | user-specific; never silently treated as verified |
| `derived` | generated index, summary, alias, or transformation | supports retrieval; does not outrank source |
| `experimental` | test material not approved for release | excluded from release profiles |
| `unknown` | missing or insufficient provenance | never presented as authoritative |

## 2. intake record

before a source is accepted, record:

- stable source id.
- human-readable name.
- source class.
- origin path or url if applicable.
- licence or usage note.
- acquisition timestamp.
- content hash.
- byte size.
- schema and schema version.
- record count.
- transform history.
- reviewer and review status.
- target modules and release profiles.

missing metadata is a review failure, not an invitation to guess.

## 3. intake procedure

1. place the source in an additive staging location.
2. inspect the schema and encoding.
3. run control-character and parse validation.
4. record count, size, hash, and source metadata.
5. classify the source.
6. identify duplicates and mirrors without removing them.
7. identify possible prompt injection, build noise, secrets, binaries, or unrelated content.
8. define the transform, if any, in writing.
9. review a sample of transformed records against the original.
10. approve the source for a named module and profile.
11. update the manifest and inventory.
12. run the affected benchmark family.

## 4. transform rules

- preserve original source material in its staging or canonical location.
- write transformed output to a new named artefact.
- never silently change meaning while compacting or normalising.
- preserve source ids and provenance through every transform.
- record lossy transforms explicitly.
- keep derived summaries separate from source text.
- reject a transform that cannot explain how a result maps back to its input.

## 5. answer evidence contract

an answer may contain four evidence classes:

### source

directly retrieved material. cite the source id and relevant key, reference, or record.

### synthesis

a combination of source records. list the input source ids and describe the joining rule.

### interpretation

an applied, doctrinal, typological, or theological reading. label the layer and list the supporting source records.

### unresolved

a possible connection or answer that does not meet the evidence threshold. do not phrase it as settled fact.

## 6. routing and provenance

routing must preserve provenance rather than return only a final string. for every answer, retain:

- original query.
- normalised query.
- route name.
- candidate ids considered.
- selected ids.
- confidence band.
- evidence class.
- answer mode.
- transformation or synthesis steps.
- unresolved flags.

if provenance is unavailable, the answer must be downgraded or returned as a gap.

## 7. doctrine and pardes review

new doctrine entries, remez mappings, sod patterns, and identity claims require a separate review because they can alter many answers at once.

review questions:

1. what source supports the entry?
2. is the claim direct source, synthesis, or interpretation?
3. does the wording overstate the source?
4. could a broad keyword route unrelated material into this answer?
5. does the entry conflict with an existing accepted entry?
6. is the entry appropriate for all profiles or only a specialised profile?
7. does the benchmark include a positive and negative control?

no new interpretive pattern enters a release profile solely because it produces a compelling answer.

## 8. teaching policy

user teaching is valuable and persistent, but it must remain visibly distinct from canonical or reference material.

- store the exact teaching event.
- store the user’s wording and timestamp.
- label it `teaching`.
- allow the user to inspect, revise, or release its influence.
- never cite a teaching as an external source.
- never merge a teaching into canonical data without a separate review and new source record.

## 9. release provenance check

before release:

- every embedded module has a manifest entry.
- every manifest entry points to a known source or derived artefact.
- every answer-critical source has a recorded hash.
- no unknown source class is included in the release profile.
- no secret, binary, build log, or unrelated staging file entered the profile.
- doctrine and interpretation changes have review records.
- the embedded manifest matches the actual payload.

## 10. incident handling

if an answer is found to be wrong or unsupported:

1. preserve the failing query and the exact release artifact.
2. record the route trace and selected evidence.
3. classify the failure as source, routing, ranking, composition, provenance, or state.
4. add a regression case.
5. correct the smallest canonical layer that owns the fault.
6. rebuild an additive candidate.
7. rerun the full affected benchmark family.
8. publish the known failure and correction in release notes.

never repair a provenance failure by hiding the source trace.
