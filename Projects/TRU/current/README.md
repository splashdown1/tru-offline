# TRU — current (phase 27)

This is the **active canonical build.** The one being iterated on day-to-day. Everything in `Projects/TRU/current/` is what the next build pulls from.

## Files

| file | what it is |
|---|---|
| `index.html` | the canonical engine (engine code + UI, brain loaded from `brain.json`) |
| `brain.json` | the purified 1,363-node canonical brain (post-dedupe + existential) |
| `template.html` | the shell template used by the build script |
| `build_phase27.py` | the builder: brain.json + template.html → index.html |
| `smoke_phase27.py` | the headless test: boot + send + verse/brain/dict/strongs queries |

## Quick start

```bash
python3 build_phase27.py        # rebuild index.html from template + brain
python3 smoke_phase27.py        # headless test it boots + answers
open index.html                  # or just double-click
```

## How to talk to it

See `file 'Projects/TRU/README.md'` for the full interaction guide. TL;DR:

- plain English: `who is jesus`, `what is grace`, `why do we pray`
- scripture: `john 3:16`, `genesis 1:1`
- Strong's: `H1`, `G26`
- teach: `teach: prayer = talking to god`
- dictionary: `define: love` (only in COMPLETE / DICTIONARY builds)

## Where this fits

```
Projects/TRU/
├── README.md          ← how to interact with TRU (the engine)
├── README_NEXT.md     ← the "play the game" spec for the next build
├── SOUL.md            ← voice / identity spec
├── current/           ← active canonical build (this folder)
│   ├── README.md      ← this file
│   ├── index.html     ← the engine
│   ├── brain.json     ← 1,363-node brain
│   └── build scripts
├── versions/          ← all lineage HTMLs (v46–v66, COIL, PASTORAL, SUPER, ...)
├── data/              ← brain JSONs + lexicon + scripture sources
├── drop/              ← modular drop folder — drop JSONs here, rebuild
├── build-scripts/     ← all build scripts for the workspace-root HTMLs
└── ...
```

For the bigger picture: `file 'README.md'` (workspace root).