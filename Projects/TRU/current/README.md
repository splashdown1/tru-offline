# TRU Phase 27 — Canonical

Current canonical TRU build.

## Files

- `index.html` — open this in a browser
- `brain.json` — canonical source brain copied from `/home/workspace/TRU_MEGA_BRAIN.json`
- `build_phase27.py` — rebuild helper
- `smoke_phase27.py` — offline checks

## Status

- phase: 27
- nodes: 31015
- mode: offline, no keys
- base: `TRU_SUPER.html`
- exported copy: `../TRU_PHASE27_CANONICAL.html`

## Fixed from audit

- canonical home created under `Projects/TRU/current/`
- isolated phase 27 localStorage keys
- version command added
- direct teaching accepts `X is Y`, `X means Y`, and `teach X is Y`
- scripture lookup adds aliases like `jn 3:16`, `john 3:16`, `1 corinthians 13:4`

## Smoke tests

Run:

```bash
python3 /home/workspace/Projects/TRU/current/smoke_phase27.py
```
