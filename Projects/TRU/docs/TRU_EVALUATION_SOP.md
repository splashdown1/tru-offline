# tru evaluation and regression sop

**timestamp:** 21 july 2026, 05:25 america/chicago
**status:** planning sop; baseline measurements still to be collected

## purpose

this sop defines how tru improvements are measured. no implementation is considered successful because a few hand-picked prompts look better.

## 1. benchmark families

### routing

tests whether the correct specialist path is selected.

examples:

- exact verse references.
- chapter requests.
- define and bare-word requests.
- strong's requests.
- commentary requests.
- doctrine and identity questions.
- broad factual questions.
- planning and advice questions.

metrics:

- route accuracy.
- wrong-route rate.
- ambiguity detection rate.
- gap precision.

### retrieval

measures whether the useful evidence appears in the candidate set.

metrics:

- exact top-1 hit rate.
- useful top-3 rate.
- source-type precision.
- duplicate rate.
- irrelevant-hit rate.

### grounding

measures whether the answer is supported by its selected evidence.

metrics:

- supported-claim rate.
- citation attachment accuracy.
- unsupported-claim rate.
- interpretation labelling accuracy.
- contradiction visibility.

### composition

measures language quality without rewarding unsupported content.

human scores from 1 to 5:

- clarity.
- coherence.
- usefulness.
- naturalness.
- appropriate length.
- source transparency.

### performance

measures startup and device cost.

- file open to interactive.
- first answer latency.
- full profile readiness.
- peak memory.
- steady-state memory after a session.
- package size compressed and uncompressed.
- mobile battery or thermal observations when available.

### state

measures durability.

- reload recovery.
- close and reopen recovery.
- export/import fidelity.
- interrupted-write recovery.
- profile migration fidelity.
- quota warning behaviour.

## 2. test tiers

### tier 0 — static checks

- parse all changed json.
- validate manifest references.
- verify expected slots.
- check for undeclared executable network primitives in offline artifacts.
- check that only approved files changed.

### tier 1 — boot smoke

- clean boot.
- no console errors.
- chat input visible.
- send action works.
- answer container renders.
- reload works.

### tier 2 — fixed regression prompts

retain the existing fixed prompts from `BUILD_SOP.md`:

- what is life
- what is hope
- define love
- define plastic
- who is jesus
- john 3:16
- help
- status

also retain the apex10 verified prompts:

- what is grace
- define apple
- james 1
- what should we do today?
- awake craniotomy
- fire-making safety
- fire extinguishing and runaway-fire safety
- explicit local teaching and taught retrieval
- stats

### tier 3 — adversarial and ambiguity tests

include:

- misspellings.
- mixed-intent questions.
- terms with theological and ordinary meanings.
- prompts containing generic words that previously drove false matches.
- prompts designed to attract encyclopedia or filing noise.
- unsupported questions that must produce a gap.
- questions that tempt pardes to overclaim.
- long sessions that stress state and rendering.

### tier 4 — profile and device tests

run the same essential cases against core, study, complete, and max profiles where the capability exists. test at least one low-memory mobile target and one desktop target.

## 3. scoring rule

an improvement is accepted only if:

1. it improves the target metric.
2. it does not regress tier 1 or tier 2.
3. it does not increase unsupported-claim rate beyond the approved threshold.
4. it stays within the profile’s startup, memory, and size budget.
5. its provenance trace remains complete.

if quality improves but grounding worsens, the change fails.
if size improves but a required route silently degrades, the change fails.
if naturalness improves by removing uncertainty labels, the change fails.

## 4. failure taxonomy

| class | symptom | owning layer |
|---|---|---|
| source | missing, malformed, duplicate, or wrong content | data intake |
| route | specialist or intent path is wrong | router |
| retrieval | useful record is not surfaced | index/search |
| ranking | weak candidate outranks strong candidate | reranker |
| synthesis | sources are combined incorrectly | reasoning |
| composition | wording is repetitive, clipped, or unclear | answer planner |
| provenance | citation or evidence class is missing/wrong | evidence layer |
| state | memory is lost, duplicated, or unrecoverable | state layer |
| packaging | manifest, size, or profile claims are wrong | build/release |
| performance | boot or memory exceeds budget | runtime/profile |

## 5. regression case format

for every accepted failure case, record:

- case id.
- date and release.
- prompt.
- expected route.
- expected evidence class.
- acceptable answer properties.
- unacceptable answer properties.
- observed output summary.
- failure taxonomy.
- owning source or module.
- correction status.

## 6. report format

start every audit with:

- timestamp in america/chicago.
- artifact path and size.
- profile name.
- source manifest version.
- browser and device target.
- test tier.

report totals plainly:

- passed.
- failed.
- blocked.
- not applicable.

include failing prompts and the exact failure class. do not report only a percentage.

## 7. release gate

release is blocked by any of the following:

- boot failure.
- chat or answer layout failure.
- fixed smoke regression.
- unlabelled unsupported claim in a tested path.
- missing provenance for a source-backed answer.
- manifest mismatch.
- unapproved network dependency in an offline profile.
- state loss in reload or export/import tests.
- profile capability claim that is not true at runtime.
