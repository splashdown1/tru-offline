# Projects/TRU

Canonical TRU builds and the modular source tree.

`tru-offline/` is the full monorepo (brain + KJV + every phase + helper scripts). `Projects/TRU/` is the slim working view of the currently canonical build — what you point at when you want to run TRU without trawling the rest of the repo.

## Layout

```text
Projects/TRU/
├── README.md
├── README_NEXT.md
├── BUILD_SOP.md
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

**APEX10 release candidate, verified 20 July 2026.** `TRU_APEX10_RELEASE.html` is the current release candidate: an 87 MB standalone offline build with the APEX9 polysemic engine, 63,337 embedded source brain nodes, 5 capability nodes, 31,100 KJV verses, WordNet definitions, Strong's, commentary, local teaching, persistence, and export.

`TRU_APEX9.html` remains the prior polysemic baseline. `TRU_PHASE28.html` remains the smaller capability-layer baseline. Neither is overwritten.

Build the release candidate with `python3 build-scripts/build_apex10_release_candidate.py` from the workspace root. The script refuses to overwrite an existing output; remove the output manually only when intentionally rebuilding.

## Status snapshot

- mode: offline, no keys
- release candidate: `TRU_APEX10_RELEASE.html`
- brain: local JSON, no external fetch
- scripture: KJV inlined
- build: `python3 current/build_phase27.py`
- smoke test: `python3 current/smoke_phase27.py`
- apex 10 candidate build: `python3 build-scripts/build_apex10_release_candidate.py`

## Larger merged builds

The current experimental large builds live at the repo root:

- `TRU_INFINITE.html`
- `TRU_INFINITE_PLUS.html`
- `TRU_GIGA.html`
- `TRU_ALL_KNOWLEDGE.html`

They are built from the modular merge pipeline in `build-scripts/` and expanded with drop data from `Projects/TRU/drop/`.

## Bundled archive

- `Projects/TRU/ship/TRU_GIGA_bundle.zip` — packaged bundle of the current large builds plus the merged builders and readme.

## Modular build notes

- `Projects/TRU/build-scripts/build_100_modular.py` is the ceiling-aware modular build.
- `Projects/TRU/build-scripts/build_70.py` is the one-pass merged build that emits the larger merged builds.
- `Projects/TRU/build-scripts/build_giga.py` builds `TRU_GIGA.html` by merging the shell, data blocks, and archived lineage payloads.
- `Projects/TRU/build-scripts/build_all_knowledge.py` builds `TRU_ALL_KNOWLEDGE.html` from the shell plus all knowledge layers.
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
