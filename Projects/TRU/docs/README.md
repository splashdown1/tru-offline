# tru blueprint and operations library

**status:** planning only; no engine code changed
**timestamp:** 21 july 2026, 05:25 america/chicago
**scope:** offline-first tru evolution from the apex10 release candidate

this directory contains the design documents that must be approved before implementation begins. they define the target architecture, operating procedures, evidence standards, and release discipline for the next tru generation.

## source of truth

- current release candidate: `TRU_APEX10_RELEASE_CANDIDATE.html`
- prior polysemic baseline: `TRU_APEX9.html`
- canonical modular source tree: `current/`, `data/`, `build-scripts/`, and `ship/`
- existing build rules: `BUILD_SOP.md`
- existing data inventory: `DATA_INVENTORY.md`
- existing modification rules: `MODIFICATION_GUIDE.md`

these documents extend the existing rules. they do not replace them and they do not authorise changes to the release candidate.

## document map

| document | purpose |
|---|---|
| `TRU_EVOLUTION_BLUEPRINT_2026-07-21.md` | product strategy, target architecture, phased gameplan, and exit criteria |
| `TRU_CAPABILITY_BLUEPRINT.md` | solution design for the eight limitations identified in the audit |
| `TRU_DATA_PROVENANCE_SOP.md` | source intake, trust classes, citations, inference boundaries, and teaching controls |
| `TRU_EVALUATION_SOP.md` | benchmark design, regression testing, answer-quality scoring, and failure triage |
| `TRU_PERFORMANCE_SOP.md` | startup, memory, mobile, lazy loading, and profile-release measurements |
| `TRU_MEMORY_STATE_SOP.md` | conversation memory, teachings, export/import, quotas, and recovery |
| `TRU_BUILD_RELEASE_SOP.md` | reproducible builds, manifests, packaging, release channels, and rollback |

## non-negotiable constraints

1. the core remains usable without internet access, api keys, accounts, or external services.
2. no implementation begins until the relevant blueprint and sop have an accepted status.
3. every answer path exposes its source class, confidence state, and whether it is fact, interpretation, or user-taught material.
4. every release is built from canonical source data and a recorded manifest.
5. the practical mobile build and the maximum-content build remain separate products.
6. existing files are preserved. new work is additive until a named replacement is explicitly approved.
7. a failed benchmark blocks release; a visual impression never overrides a failed test.

## approval gates

- **gate 0 — blueprint approved:** product boundaries and terminology are settled.
- **gate 1 — architecture approved:** module boundaries, profiles, and state contracts are settled.
- **gate 2 — evaluation approved:** benchmark corpus and scoring rubric are frozen for the phase.
- **gate 3 — implementation approved:** only then may code or data transforms change.
- **gate 4 — release approved:** all required tests, size checks, provenance checks, and offline checks pass.

## intended outcome

tru does not need to pretend to be a cloud llm. it needs to become a stronger sovereign intelligence instrument: faster to open, harder to misroute, clearer about what it knows, more capable of composing useful answers, more durable across sessions, and easier to build and distribute without losing its offline identity.
