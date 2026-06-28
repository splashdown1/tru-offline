# Projects/TRU

Canonical TRU builds, organised by phase.

`tru-offline/` is the full monorepo (brain + KJV + every phase + helper scripts). `Projects/TRU/` is the slim view of the currently-canonical build — what you point at when you want to run TRU without trawling the rest of the repo.

## Layout

```
Projects/TRU/
├── README.md           ← you are here
└── current/            ← latest canonical build (Phase 27)
    ├── README.md
    ├── index.html      ← open this
    ├── brain.json
    ├── build_phase27.py
    └── smoke_phase27.py
```

## Current canonical

**Phase 27.** See `current/README.md` for what shipped and which fixes landed.

## Status snapshot

- mode: offline, no keys
- brain: local JSON, no external fetch
- scripture: KJV inlined
- build: `python3 current/build_phase27.py`
- smoke test: `python3 current/smoke_phase27.py`

## Older phases

Older phase builds live in `tru-offline/` directly (e.g. `TRU_PHASE26*.html`, `TRU_Greek_NT_Download-*.html`). When a new phase graduates, it gets copied into `current/` and the previous one stays where it is for reference.

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