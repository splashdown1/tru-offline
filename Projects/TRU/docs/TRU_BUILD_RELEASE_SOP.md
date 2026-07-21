# tru build and release sop

**timestamp:** 21 july 2026, 05:25 america/chicago
**status:** planning sop; existing builders remain unchanged

## purpose

this sop turns the blueprints into a repeatable build and distribution discipline while preserving every existing artifact.

## 1. source hierarchy

- canonical source data remains under the paths declared by `DATA_INVENTORY.md`.
- existing release candidates remain immutable inputs unless a new additive candidate is intentionally produced.
- experimental trees remain isolated until reviewed.
- mirrors are not promoted merely because they are larger or newer-looking.

## 2. candidate naming

new artifacts receive an explicit name containing:

- project family.
- profile.
- generation or phase.
- release status.
- date when needed.

examples:

- `tru_core_next_candidate.html`
- `tru_study_next_candidate.zip`
- `tru_max_next_candidate.zip`
- `tru_state_export_2026-07-21.json`

existing files are not overwritten during blueprint implementation.

## 3. manifest requirements

before an artifact is called a candidate, its manifest records:

- artifact name and profile.
- source manifest version.
- builder name and version.
- build timestamp.
- source hashes.
- embedded module ids.
- module counts and sizes.
- supported routes and capabilities.
- optional enhancement status.
- offline status.
- state schema compatibility.
- checksums for the final artifact and package members.

## 4. build sequence

1. confirm the approved blueprint and phase scope.
2. confirm the exact source tree and protected artifacts.
3. validate source data and manifests.
4. build an additive candidate.
5. inspect candidate size, slots, and embedded manifest.
6. run static offline checks.
7. run boot and fixed smoke tests.
8. run routing, grounding, profile, performance, and state tests required by the phase.
9. compare against the baseline artifact.
10. write a dated release note with passed, failed, and blocked tests.
11. package practical and maximum profiles separately when appropriate.
12. preserve rollback inputs and checksums.

## 5. offline verification

an offline release must demonstrate:

- no required network request.
- no required api key.
- no silent external dependency.
- all advertised core capabilities available from embedded or explicitly installed local modules.
- clear status when an optional module is absent.

## 6. packaging channels

### practical profile

small, fast, and suitable for ordinary desktop or mobile use. it favours startup and memory over maximum content.

### study profile

scripture and theological study capabilities with specialist modules selected intentionally.

### maximum archive

all approved content for research and preservation. it is allowed to be large and slower, but it must remain reproducible and clearly labelled.

### state export

portable user memory separate from the knowledge profile.

## 7. rollback policy

if a candidate fails after packaging:

- preserve the failed candidate and its report.
- do not silently relabel it as a release.
- restore the last verified release path for users.
- record the failure class and affected profile.
- add a regression case before the next candidate.

## 8. release note minimum

include:

- timestamp in america/chicago.
- artifact names and sizes.
- profile and capability summary.
- source and builder identifiers.
- tests run and exact totals.
- known failures and limitations.
- state compatibility.
- offline verification result.
- checksum location.

## 9. final release gate

no release is ready until:

- all required static, boot, regression, provenance, performance, state, and packaging tests pass.
- the manifest matches the artifact.
- the practical profile is usable without the maximum archive.
- the maximum archive remains available when promised.
- no existing protected file was overwritten.
- the release notes state what was verified rather than what was intended.
