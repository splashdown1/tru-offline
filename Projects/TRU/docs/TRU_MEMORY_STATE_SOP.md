# tru memory and state sop

**timestamp:** 21 july 2026, 05:25 america/chicago
**status:** planning sop; no state format changes authorised

## purpose

this sop defines how conversation memory, teachings, seals, feedback, and exports survive browser limits without becoming a hidden dependency for boot.

## 1. state contract

state is separate from embedded knowledge. a profile can boot with no state, and state can move between compatible profiles.

every event records:

- event id.
- event type.
- timestamp.
- schema version.
- session id.
- payload.
- source profile.
- optional parent event.

## 2. event categories

- conversation turn.
- answer feedback.
- teaching.
- seal.
- release intention.
- bookmark.
- preference.
- checkpoint.
- export.
- migration.
- recovery notice.

## 3. write policy

- write a valid event before updating the visible state that depends on it.
- keep the last known valid checkpoint.
- detect malformed or partial state on load.
- never block a clean boot because state is absent or damaged.
- show the user when state is unavailable, stale, or awaiting export.
- preserve the original event record when deriving a checkpoint or summary.

## 4. browser quota policy

when storage pressure is detected:

1. warn before the next risky write.
2. offer export of the state package.
3. identify the approximate state size and major contributors.
4. allow a new session to continue without silently losing the old one.
5. record the recovery or export action.

state compaction is a future reviewed feature. it must preserve an inspectable source history or a user-approved archive package; it must never silently make events disappear.

## 5. export package

an export contains:

- profile name and version.
- state schema version.
- export timestamp.
- event records or an approved inspectable archive.
- user teachings.
- seals and release intentions.
- bookmarks and preferences.
- source manifest references needed to interpret the state.
- checksums.

an export must not pretend to contain source modules that are not included.

## 6. import procedure

1. validate the package structure.
2. validate checksums.
3. check schema compatibility.
4. show the user what categories will be restored.
5. preserve the pre-import state as a recovery point.
6. import into a new state generation.
7. run the state regression suite.
8. report restored, skipped, and incompatible records.

## 7. teaching and memory boundaries

- conversation memory describes what was said; it is not automatically truth.
- teaching is user-provided and labelled.
- sealed material is load-bearing by user intent but still retains provenance and review status.
- release intentions are instructions for future state handling, not proof of correctness.
- source knowledge and user state remain distinguishable in the answer trace.

## 8. required tests

- first boot without state.
- reload with a normal session.
- close and reopen with a teaching.
- export and import into the same profile.
- import into a smaller profile.
- interrupted write.
- malformed package.
- schema migration.
- quota warning.
- recovery after a failed import.

## 9. state release gate

state work fails release if:

- the engine cannot boot without state.
- a teaching disappears after reload or export/import.
- a damaged package overwrites the valid recovery point.
- source facts and user teachings become indistinguishable.
- the user cannot inspect what was restored.
