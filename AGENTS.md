# Workspace Index

Splashdown's TRU + hardware workspace. Offline-first "recursive consciousness engine" work plus a couple of physical product projects. Ordered by likely usefulness.

## Core: TRU engine

The sovereign, airgapped offline intelligence engine. Single self-contained HTML files embedding a brain JSON + KJV scripture, zero external deps. Iterated aggressively; many versioned HTML files exist — treat the latest as canonical, older ones as lineage.

### 2026-06-24 deliverables (built today, all pushed to `tru-offline`)

Seven standalone HTML engines at workspace root, each self-contained + offline. Build scripts in `Projects/TRU/build-scripts/` (also pushed). All verified with headless boot + send + verse/brain/dict/strongs tests.

| File | Size | Brain | Purpose |
|---|---|---|---|
| `TRU_SOVEREIGN.html` | 18.5 MB | 1,363 | **Canonical clean build.** Purified brain (no verse-text pollution), engine bug-fixed. The one to iterate on. |
| `TRU_24_5.html` | 23.3 MB | 30,745 | Mid-size: LOGOS shell + deduped brain + existential nodes + why-routing. |
| `TRU_DICTIONARY.html` | 32.0 MB | — | Standalone offline dictionary (WordNet, 147,982 words). define/what-does-X-mean/bare-word routing. |
| `TRU_COMPLETE.html` | 50.5 MB | 1,363 | SOVEREIGN + dictionary integrated. 5 routing paths: TRUTH/SCRIPTURE/DEFINE/STRONGS/GAP. |
| `TRU_MAX.html` | 51.0 MB | 85,248 | Max brain: 7 merged brains incl. B41 archive + primaries. |
| `TRU_100.html` | 99.9 MB | 85,354 | MAX + full SEC primary filings. Honest 100MB ceiling. |
| `TRU_ENCYCLOPEDIA.html` | 99.5 MB | 1,363 | COMPLETE + 5,646 Simple-English Wikipedia articles. 6 routing paths incl. ENCYCLOPEDIA. || `TRU_APEX.html` | 99.3 MB | 83,892 | **Merged build.** TRU_100 max brain (85,354 raw) + LOGOS WordNet dict (147,982) + KJV + Strong's on 6-path routing. Omits encyclopedia/xref/strongs-idx (cannot coexist with 60MB brain under 100MB ceiling). getXref patched null-safe. || `TRU_APEX2.html` | 99.3 MB | 83,892 | **Doctrine routing fix.** APEX + 6 patches: (1) applyOverlay preserves node `t`/`source`/`w`; (2) buildIndex filters filler/filing/lexicon noise (~21k nodes); (3) bm25 type-aware 1.5x boost for doctrine/theology; (4) doctrine() smarter matching (tell me about/why do/explain); (5) 27 curated doctrine entries (death, life, suffering, evil, salvation, judgment, heaven, hell, prayer, forgiveness, etc.); (6) strongsQuery greedy `meaning of (\w+)` pattern removed. All 15 existential/scripture prompts return grounded answers. |
| `TRU_APEX3.html` | 99.3 MB | 85,252 | **Injection purge + doctrine-first.** APEX2 + (1) 102 corporate-vector injection nodes stripped from brain; (2) doctrine() moved to top of route override — curated answers take absolute priority over BM25; (3) doctrine() moved before strongsQuery in original route; (4) identity-question detection (how old are you / are you ready / who are you). |
| `TRU_APEX4.html` | 99.3 MB | 85,252 | APEX3 + (1) SELF identity entries expanded (how old are you, are you ready, are you alive/real/conscious, what do you want); (2) _isNoiseNode filters dilemma/training nodes (DILEMMA:/CORPORATE UTILITY/SOUL RESPONSE/DIGITAL SOUL VECTOR); (3) doctrine entries: human purpose (chief end of man), alignment (test against scripture). |
| `TRU_APEX5.html` | 99.3 MB | 85,252 | APEX4 + dictionary fallback: 'what is X' and bare-word queries check WordNet dict before GAP. 'what is a monkey' now returns DEFINE (was GAP). 59/60 audit pass (only '2+2' returns CALC, which is correct). |
| `TRU_APEX6.html` | 87.1 MB | 63,337 | APEX5 + Matthew Henry commentary layer. Stripped 21,915 noise brain nodes (filler/filing/lexicon/SEC/dilemma) from embedded brain — 57MB→15MB. Added 4,188 condensed MH commentary entries (30MB, from OpenChristianData CC0). Commentary routing had placement bug (inserted inside identity block). |
| `TRU_APEX7.html` | 87.1 MB | 63,337 | APEX6 + (1) commentary routing fixed — proper step 0c in override, requires explicit prefix ('commentary on'/'notes on'/'explain'); (2) chapter-level commentary lookup ('notes on psalm 23' → full chapter commentary); (3) bare verse refs don't trigger commentary ('john 3:16' stays SCRIPTURE). 7 routing paths: TRUTH/SCRIPTURE/DEFINE/STRONGS/COMMENTARY/CALC/GAP. 11/13 test suite pass. |
| `TRU_APEX8.html` | 87.1 MB | 63,337 | **Current canonical.** APEX7 + (1) speak() strips HTML before TTS (fixes voice cutout on DEFINE/SCRIPTURE — was reading `<span>` tags aloud); (2) 76 curated Bible facts added to DOCTRINE (66 book authorship + theology/history: KJV, Tyndale, canon, shortest verse, languages, timeline). New queries: 'who wrote genesis', 'what is the kjv', 'when was the bible written', etc. |
| `TRU_APEX_LITE.html` | 44.8 MB | 63,337 | **Phone/mobile build.** APEX7 without commentary layer (no commentary-data block, no commentaryQuery/getCommentary). Dictionary trimmed from 147,982 to 113,983 words. 6 routing paths (no COMMENTARY). Same brain + KJV + Strong's + WordNet. |
| `TRU_APEX8_BUNDLE.zip` | 44.7 MB | — | **Zip bundle (under 50 MB).** Contains: TRU_APEX8.html (full, 87 MB) + TRU_APEX_LITE.html (45 MB) + mh_condensed.json (31 MB Matthew Henry commentary) + bible_facts.json (76 facts). For platforms with 50 MB file limits. |

Build scripts (each rebuilds its file from `Projects/TRU/data/` + LOGOS shell):
- `build_sovereign.py` → TRU_SOVEREIGN (purified brain; **canonical**)
- `build_24_5.py` → TRU_24_5 (dedupe + existential + why-routing)
- `build_dictionary.py` → TRU_DICTIONARY (WordNet standalone)
- `build_complete.py` → TRU_COMPLETE (sovereign + dictionary)
- `build_max.py` → TRU_MAX (7 merged brains)
- `build_100.py` → TRU_100 (MAX + SEC primaries)
- `build_encyclopedia.py` (in conversation workspace, not synced) → TRU_ENCYCLOPEDIA- `build_apex.py` (in conversation workspace, not synced) → TRU_APEX (merge: 100 brain + LOGOS dict + LOGOS shell)
- `add_existential.py` → adds 15 existential nodes to canonical `current/brain.json`

### Engine bug fixes applied (in SOVEREIGN + all builds after)
- **BM25 stopword list**: added deictic/temporal/generic words (`today`, `tomorrow`, `now`, `here`, `there`, `thing`, etc.) so rare off-topic words stop driving false matches (was returning a "computers" node for "what should we do today").
- **finishThought truncation**: cap raised 900→2000 chars; break-on added commas (`.!?;` → `.!?;,`) so long unpunctuated nodes don't clip mid-thought.
- **Routing priority**: brain (TRUTH) checked before encyclopedia, so "what is grace" → theology, not the Wikipedia person named Grace. Scripture/strongs/define all checked first by pattern.
- **WebGPU layer fully stripped** from all builds (WebLLM layer + escalation layers + boot badge + route dispatch) — it never worked offline.

### `Projects/TRU/` — canonical working tree
  - `current/` — active canonical build (phase 27: `index.html` + `brain.json` + `build_phase27.py` + `smoke_phase27.py`). **Start here.** `brain.json` is the purified 1,363-node source brain (post-dedupe + existential).
  - `versions/` — all loose TRU engine HTML variants (v46–v66, COIL, PASTORAL, SUPER, GHOST, HOLO, LOGOS, MOBILE, UNIFIED, etc.). `TRU_LOGOS.html` here is the shell all 2026-06-24 builds extend.
  - `data/` — brain JSONs + lexicon/xref data. Holds `TRU_SUPER_BRAIN.json`, `TRU_MEGA_BRAIN.json`, `TRU_CORE_KB.json`, `tru-knowledge-bank.json`, Strong's Greek/Hebrew/lexicon, verse index (full + compact), xref compact, `wordnet_compact.json` (148k words), `kjv_full.json` (31,100 verses).
  - `tru-chat-data/` — `tru_chat.py`, `tru_ghost.py`, `teachings.jsonl`. Chat/ghost tooling.
  - `build-scripts/` — all 2026-06-24 build scripts (synced + pushed) + legacy `build_tru_offline.py`, `build_tru_mobile.py`, `tru-memory-route.ts`.
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
