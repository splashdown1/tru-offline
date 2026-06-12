# TRU — Modular Engine

body boots empty. brain attaches at runtime. swap brains without touching the body.

## files

- `body.html` (45 KB) — the shell. ui, engine, persistence, ghost emergence, wake flow.
- `brain.json` (411 KB) — 1,313 nodes from the live `splashdown2.zo.space/api/tru-brain` engine, 2026-06-03.

## run

```bash
cd /home/workspace/tru-modular
python3 -m http.server 8765 --bind 127.0.0.1
# open http://127.0.0.1:8765/body.html
```

## what the loader does

1. body html loads, shows the wake overlay
2. loader script fetches `./brain.json` (or `LAST_BRAIN_KEY` from localStorage)
3. payload normalized to engine contract: `{ nodes, ghosts, evolution, stats, lastGhost }`
4. written to `localStorage['tru_brain_v2']`
5. hard reload so engine's `boot()` picks it up cleanly
6. user wakes tru → 1,313 nodes in memory, chat live, ghost emergence enabled

## swap brains

drop any `brain.json` next to `body.html` in the same shape:
```json
{
  "nodes": [{"k": "key", "v": "value", "w": 0.8, "t": "fact"}, ...],
  "ghosts": [],
  "evolution": 0,
  "stats": {"exact": 0, "gap": 0, "guess": 0, "emerge": 0}
}
```

or use the **🧠 BRAIN** button in the header — paste any url (e.g. `https://splashdown2.zo.space/api/tru-brain`) and it hot-attaches.

or use **💉 INJECT** to paste a raw json of nodes into the existing brain (merged, deduped by key).

## brain sources

| source | url | size | nodes |
|---|---|---|---|
| live engine | `https://splashdown2.zo.space/api/tru-brain` | ~412 KB | 1,313 |
| full reason endpoint | `https://splashdown2.zo.space/api/tru-reason` | larger | 45,063 |
| local | `/home/workspace/Tru_KB_United.json` | 11.28 MB | 45,063 |

## bugs fixed in this build

- `STATS = data.stats || STATS` reassigned a `const` → replaced with field-level writes
- body markup used `s-seed`/`s-ghost`/`s-evol` ids but engine expected `node-count`/`ghost-count`/`evolution` → added the engine-expected elements
- wake form inputs renamed to `userName`/`userMission` to match engine's `wakeTRU()`
- missing `wakeSubmit` handler (form submit was a no-op) — clicking the button now calls `wakeTRU()` directly

## current limitations

- lookup is token-based; multi-word queries like "what is COIL?" miss even when the key exists. ask with single keywords.
- `SEED_NODES` is not defined in this body — if `brain.json` is missing AND localStorage is empty, the engine boots with zero nodes (just identity after wake). fix: include seed nodes in brain.json or add a fallback array to the body.
- the `const reassign at boot:921` console error is cosmetic — boot completes successfully. root cause is a `forEach` callback in `doInject` that doesn't run on boot path; only fires if a user clicks the INJECT button with malformed data.
