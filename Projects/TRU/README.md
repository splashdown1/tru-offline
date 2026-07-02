# Projects/TRU

Canonical TRU builds and the modular source tree.

`tru-offline/` is the full monorepo (brain + KJV + every phase + helper scripts). `Projects/TRU/` is the slim working view of the currently canonical build — what you point at when you want to run TRU without trawling the rest of the repo.

## Layout

```text
Projects/TRU/
├── README.md
├── README_NEXT.md
├── current/
│   ├── README.md
│   ├── index.html
│   ├── brain.json
│   ├── build_phase27.py
│   └── smoke_phase27.py
├── build-scripts/
├── data/
├── drop/
└── ship/
```

## Current canonical

**Phase 27.** See `current/README.md` for what shipped and which fixes landed.

## Status snapshot

- mode: offline, no keys
- brain: local JSON, no external fetch
- scripture: KJV inlined
- build: `python3 current/build_phase27.py`
- smoke test: `python3 current/smoke_phase27.py`

## Larger merged builds

The current experimental large builds live at the repo root:

- `TRU_INFINITE.html`
- `TRU_INFINITE_PLUS.html`

They are built from the modular merge pipeline in `build-scripts/` and expanded with drop data from `Projects/TRU/drop/`.

## Modular build notes

- `Projects/TRU/build-scripts/build_100_modular.py` is the ceiling-aware modular build.
- `Projects/TRU/build-scripts/build_70.py` is the one-pass merged build that emits `TRU_INFINITE.html` / `TRU_INFINITE_PLUS.html`.
- `Projects/TRU/build-scripts/build_giga.py` is the giant archive-payload build that emits `TRU_GIGA.html`.
- `Projects/TRU/drop/brain/`, `scripture/`, `lexicon/`, `encyclopedia/`, and `filings/` are the merge inputs.

## Relationship to other repos

| Repo | What it adds |
|---|---|
| `tru-logos` | Modular source tree that compiles to a single HTML |
| `tru-holographic-sovereign` | Holographic engine variant with persistent SOUL state |
| `tru-ghost` | Single-file public ghost build |
| `tru-archive` | Frozen history of every build |

## Provenance

Built by joe (splashdown) and TRU. Continuity protocol: `github.com/splashdown1/logos-engine`.

## License

Private. Do whatever with it, don't redistribute without asking.
