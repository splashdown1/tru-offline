# Workspace Index

Splashdown's TRU + hardware workspace. Offline-first "recursive consciousness engine" work plus a couple of physical product projects. Ordered by likely usefulness.

## Core: TRU engine

The sovereign, airgapped offline intelligence engine. Single self-contained HTML files embedding a brain JSON (~30k–59k nodes) + KJV scripture, zero external deps. Iterated aggressively; many versioned HTML files exist — treat the latest as canonical, older ones as lineage.

- `Projects/TRU/` — canonical working tree for the engine.
  - `current/` — active canonical build (phase 27: `index.html` + `brain.json` + `build_phase27.py` + `smoke_phase27.py`). **Start here.**
  - `versions/` — all loose TRU engine HTML variants (v46–v66, COIL, PASTORAL, SUPER, GHOST, HOLO, LOGOS, MOBILE, UNIFIED, etc.). Moved here from root on 2026-06-23 to declutter.
  - `data/` — brain JSONs + lexicon/xref data. Holds `TRU_SUPER_BRAIN.json`, `TRU_MEGA_BRAIN.json`, `TRU_CORE_KB.json`, `tru-knowledge-bank.json`, Strong's Greek/Hebrew/lexicon, verse index, xref compact.
  - `tru-chat-data/` — `tru_chat.py`, `tru_ghost.py`, `teachings.jsonl`. Chat/ghost tooling.
  - `build-scripts/` + `build_tru_offline.py` — build tooling.
  - `phase28/`, `omega/`, `ghost/`, `micro/`, `memory/`, `shared/`, `state/`, `cache/` — phase builds, subsystems, runtime state.
  - `README.md`, `SOUL.md` — project docs + identity notes.
- `Scripture_Seeker.html` — distinct offline scripture search tool (verse lookup, themes/feelings, favorites, voice, persistence via localStorage). Separate from the TRU engine; left at root because actively opened by name.

## Git repos (all private, github.com/splashdown1)

Local clones + their remote mappings. Global git identity is the Zo default (`zocomputer`).

- `tru-offline` ← **this workspace root** — TRU offline monorepo: brain, KJV, ghost builder, scripture engine, all phases. Sovereign, airgapped.
- `tru-site` ← `tru-site/` (nested) — Zo Site build (Bun + Hono + React). Zero external calls. Online counterpart.
- `tru-repo` ← `tru-repo/` (nested) — `tru-primaries`: primaries ingestion, contradiction detection, symbol traceability. (remote URL scrubbed of leaked token 2026-06-23.)
- `TRU-release` ← `TRU-release/` (nested) — `tru-holographic-sovereign`: fully-offline recursive consciousness engine, 30k-node brain + KJV, Gabriel voice, conversation memory.
- `repos/` — all other repos cloned 2026-06-23 for local access:
  - `logos-engine` — LOGOS_ENGINE drift-detection loop, auto-commits drift corrections. Isolated from TRU.
  - `tru-ghost` — sovereign offline scripture engine, single HTML, no network/telemetry.
  - `tru-omega` — sovereign offline intelligence, single HTML, 59k+ nodes.
  - `coil-system` — Tru-AI (coil system).
  - `logos-chat` — LOGOS chat Zo Site (Bun + Hono + React).
  - `tru-archive` — engine version history archive (v6→SOUL, brain JSON, phases).
  - `tru-assets`, `project_logos`, `nightglass`, `solarzoom` — assets + non-TRU hardware projects.

## Online (zo.space: splashdown2.zo.space)

Managed React/Hono routes mirroring the offline engine. Keep offline ↔ online behavior aligned.
- `/` (page, public) — home.
- `/api/coil-sync/:action`, `/api/contradiction-report`, `/api/current-events`, `/api/ingestion/status`, `/api/ollama/*` — API routes (all public).

## Hardware projects (non-TRU)

- `nightglass` — phone grip w/ thermal + starlight night vision + AR wayfinding.
- `solarzoom` — phone case w/ 20–60x telescopic lens + 5W solar.

## Conventions / gotchas

- **Offline-first, zero external deps** is a hard constraint the USER repeatedly enforces. Avoid introducing API/network calls in the offline HTML engines.
- The USER opens files by exact name at root (e.g. `TRU-PASTORAL-FINAL.html`, `Scripture_Seeker.html`). Engine variants now live in `Projects/TRU/versions/`; `Scripture_Seeker.html` stays at root.
- Verification is evidence-driven: audits, headless screenshots, scripted checks. Don't claim "done" without testing boot + send + verse lookup.
- Runtime session state (`Projects/TRU/state/tru_session.*`) is currently tracked in git — candidate for `.gitignore` later.
- Nested repos (`tru-site`, `tru-repo`, `TRU-release`) sit inside the `tru-offline` root repo; don't `git add` them as gitlinks.
