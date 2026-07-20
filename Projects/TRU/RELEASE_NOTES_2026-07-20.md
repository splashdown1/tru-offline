# tru apex 10 release candidate

**timestamp:** 20 july 2026, 00:27 america/chicago

## status

`TRU_APEX10_RELEASE_CANDIDATE.html` is the verified release candidate. it is additive to the existing apex 9 and phase 28 builds; neither was replaced.

## local runtime

- 63,337 embedded source brain nodes
- 5 capability nodes
- 31,100 embedded kjv verses
- 62,026 runtime local nodes before user overlay changes
- zero executable network primitives outside embedded data
- localStorage conversation and teaching persistence retained

## routing fix

curated doctrine now runs before dictionary and encyclopedia fallback. `what is grace` returns the curated doctrine answer rather than an unrelated dictionary or encyclopedia hit.

## verified prompts

- identity and operational state
- `what is grace`
- `define apple`
- `john 3:16`
- `james 1`
- planning boundary for `what should we do today?`
- awake craniotomy
- fire-making safety
- fire extinguishing and runaway-fire safety
- explicit local teaching and taught retrieval
- stats

browser boot completed with no console errors.

## build

```sh
python3 Projects/TRU/build-scripts/build_apex10_release_candidate.py
```

The script refuses to overwrite an existing output and audits executable network primitives before writing the candidate.
