# TRU Data Inventory

> Generated 2026-07-13 (America/Chicago)
> Scope: every `*.json`/encoded text artefact in `Projects/TRU/data/`, `Projects/TRU/current/`, `Projects/TRU/TRU/`, `Projects/TRU/ship/tru-logos-source/data/`, `Projects/TRU/omega/{data,brain}/`, `TRU-release/data/`, and a few orphan mirrors. No file rewritten — read-only scan.

## 0. Source-tree index

| Tree | Role | Total size | Status |
|---|---|---|---|
| `Projects/TRU/data/` | **Canonical working data** (per `AGENTS.md`) | ~120 MB across 38 files | Canonical |
| `Projects/TRU/current/brain.json` | **Canonical brain** (30,745 nodes, phase 27 build) | 6.6 MB | Canonical |
| `Projects/TRU/ship/tru-logos-source/data/` | LOGOS-shipped data (separate schema) | ~100 MB across 29 files | Active build target |
| `Projects/TRU/omega/{data,brain}/` | OMEGA experiment tree — glossary + brain + 1,956 edges | ~19 MB | Experimental, do not depend on |
| `Projects/TRU/TRU/` | Standalone 30,762-node brain + lookup (no provenance) | 16 MB | Legacy / mirror |
| `TRU-release/data/` | Older snapshot of strongs/strongs-verse-index/xref (Jun 19) | ~20 MB | Legacy, do not edit |
| `tru-unified-build/tru-offline-clone/Projects/TRU/data/` | Exact byte-clone of working data | ~120 MB | Mirror, do not edit |
| `repos/logos-engine/TRU/kjv_lookup.json` | Logos-engine mirror | 9.7 MB | Mirror |
| `/home/workspace/kjv_complete.json` | Orphan — chapter/verse tree, different schema | 5.0 MB | Orphan — leave alone |

---

## 1. `Projects/TRU/data/` — canonical working data

38 files. Encoded wrappers (`*.b64`, `*.txt`, `*.js`) cover the same content as the corresponding JSONs.

### 1.1 Brain variants (history)

| File | Size | Schema | Nodes | Notes |
|---|---:|---|---:|---|
| `TRU_SUPER_BRAIN.json` | 300 K | `{version, nodes, brain}` | n/a | Wraps brain under `brain` key |
| `tru_brain_1290_nodes.json` | 660 K | `{version, exported, nodes, brain}` | n/a | Phase N snapshot |
| `tru_full_brain.json` | 269 K | `list[{k,v,w,t,s}]` | 803 | 5-field shape |
| `tru_merged_brain.json` | 628 K | `list[{k,v,t,w,source,…}]` | 1,294 | 11-field shape with provenance |
| `tru_phase15_brain.json` | 245 K | `list[{k,v,w,t,s}]` | 661 | Phase 15 snapshot |
| `tru_super_brain.js` | 484 K | JS literal | n/a | Mirror of `TRU_SUPER_BRAIN` |
| `tru_brain_min.js` | 393 K | JS literal | n/a | Minified brain |
| `brain_b64.txt` / `brain_offline.b64` | 141 K | base64 JSON | n/a | Encoded form |
| `TRU_MEGA_BRAIN.json` | 6.7 M | `{version, nodes, exported}` | 30,745 | **Identical to `brain_canonical.json`** — duplicate |
| `brain_canonical.json` | 6.7 M | `{version, nodes, exported}` | 30,745 | Same bytes as `TRU_MEGA_BRAIN.json` |

`TRU_MEGA_BRAIN.json` and `brain_canonical.json` are byte-identical. **Canonical brain for the current pipeline is `Projects/TRU/current/brain.json` (same shape, 30,745 nodes, last updated 2026-06-23 22:36).** The two old `brain_canonical.json`/`TRU_MEGA_BRAIN.json` files in `data/` are older snapshots from `2026-05-19/20`.

### 1.2 Knowledge banks

| File | Size | Schema | Top-level | Count |
|---|---:|---|---|---:|
| `TRU_CORE_KB.json` | 43 K | dict | thematic keys (truth, sovereignty, consciousness…) | 120 |
| `tru-knowledge-bank.json` | 25 K | dict | `{knowledge_bank_version, description, categories, entries}` | n entries |

### 1.3 KJV (scripture text)

| File | Size | Schema | Count | Notes |
|---|---:|---|---:|---|
| `kjv_full.json` | 6.4 M | `list[{ref, text, abbrev, testament}]` | 31,100 | **Canonical** for verse lookup |
| `kjv_ot_english.json` | 4.9 M | same | 23,147 | OT subset |
| `kjv_nt_greek_english.json` | 1.5 M | same | 7,953 | NT subset |
| `kjv_bible.js` | 6.7 M | JS literal | 31,100 | Mirror of `kjv_full.json` |
| `bible_*.b64`, `bible_job_book.txt`, `coil_*.txt/brotli.txt`, `nt_b64.txt`, `ot_b64.txt` | various | base64/brotli | 31,100 | Encoded wrappers around the same KJV — same content, different transport |

### 1.4 Lexicons

| File | Size | Schema | Count | Notes |
|---|---:|---|---:|---|
| `strongs_greek.json` | 697 K | dict keyed `G####` | 5,523 | **Canonical Greek** |
| `strongs_hebrew.json` | 1006 K | dict keyed `H####` | 8,674 | **Canonical Hebrew** |
| `strongs_lexicon_kaiserlik.json` | 4.6 M | dict keyed `G####`/`H####` | 12,040 | Combined + extended entries |
| `strongs_verse_index.json` | 20 M | dict keyed `H####` | 13,654 | Full per-verse index |
| `strongs_verse_index_compact.json` | 2.9 M | dict keyed `H####` | 13,654 | **Use this** — 7× smaller, same keys |

### 1.5 Cross-references

| File | Size | Schema | Count | Notes |
|---|---:|---|---:|---|
| `xref_compact.json` | 4.5 M | dict keyed `"<book> <ch>:<v>"` | 30,412 | **Canonical** — already compact |

### 1.6 WordNet

| File | Size | Schema | Count | Notes |
|---|---:|---|---:|---|
| `wordnet_compact.json` | 32 M | dict keyed by lemma | 147,982 | **Canonical** — same data as LOGOS `dict-data.json` |

---

## 2. `Projects/TRU/current/` — canonical brain + template

| File | Size | Notes |
|---|---:|---|
| `brain.json` | 6.6 M | 30,745 nodes; node 0 = `{k, v, w, t, source}`. Source breakdown: KJV_BIBLE 29,439 / TRAINING_SET 321 / TRU_EMBEDDED_BRAIN 258 / TRU_HTML_LOGIC 253 / JSON_FILE 155 / TRU_BRAIN 123 / SUPPLEMENTAL 49 / CERTIFIED 44. Type breakdown: fact 30,129 / rule 592 / doctrine 15 / ghost 9. **This is the canonical brain.** |
| `template.html` | 16 K | Phase-27 shell — does **not** contain `{{DATA_SLOTS}}` sentinel. Needs stage-2 sentinel injection. |
| `index.html` | 8.5 M | Phase-27 bundle |
| `README.md`, `build_phase27.py`, `smoke_phase27.py`, `tru_module_manifest.json` | small | Build scripts and module manifest |
| `tru_module_manifest.json` | 336 B | Current module manifest — only `encyclopedia-data` + `dict-data` slots listed (per handoff). Does **not** enumerate the scripture/strongs/xref slots. |

**`current/template.html` is missing the `{{DATA_SLOTS}}` sentinel** that the handoff described for stage 2 — this work was either not committed yet, or lives in a different tree. See `§4` for the LOGOS shell, which does have the slot system.

---

## 3. `Projects/TRU/TRU/` — standalone brain + lookup

| File | Size | Schema | Count | Notes |
|---|---:|---|---:|---|
| `TRU_BRAIN_41.json` | 6.3 M | `list[{k,v,w,t,source}]` | 30,762 | 17 nodes newer than `current/brain.json`; **no provenance fields** beyond `source`. Likely a downstream export. |
| `kjv_lookup.json` | 9.2 M | dict keyed `"<book><ch>:<v>"` and `"<book> <ch>:<v>"` | 31,100 | Both space-separated and no-space variants per verse |
| `ghost/` | empty | — | — | — |

This `TRU_BRAIN_41.json` is essentially the same content as `current/brain.json` but without `version`/`exported` envelope and without the doctrine provenance flags. Treat as a **legacy mirror**; do not modify.

---

## 4. `Projects/TRU/ship/tru-logos-source/` — LOGOS build tree

LOGOS uses a different schema than the working data tree — brain nodes are `[{"k","v"}]` (no `w`/`t`/`source`), and KJV/Strong's are dict-of-arrays.

### 4.1 `data/` (29 files, ~100 MB)

#### Big slots (referenced by `manifest.json`)

| ID | File | Size | Schema | Count |
|---|---|---:|---|---:|
| `encyclopedia-data` | `encyclopedia-data.json` | 50 M | dict | 5,646 (Simple-English Wikipedia) |
| `dict-data` | `dict-data.json` | 32 M | dict | 147,982 (WordNet) |
| `kjv-data` | `kjv-data.json` | 5.2 M | `list[{ref, text}]` | 31,100 |
| `xref-data` | `xref-data.json` | 4.9 M | dict | 30,412 |
| `strongs-data` | `strongs-data.json` | 4.9 M | dict | 12,040 |
| `strongs-idx` | `strongs-idx.json` | 3.1 M | dict | 13,654 |
| `brain-data` | `brain-data.json` | 227 K | `list[{k, v}]` | 954 |

#### Ancient-wisdom modules (12 files)

| File | Size | Schema | Count |
|---|---:|---|---:|
| `ancient-literature-epic.json` | 62 K | `list[{k,v}]` | 271 |
| `ancient-hermetic-neoplatonism.json` | 58 K | `list[{k,v}]` | 120 |
| `ancient-roman.json` | 50 K | `list[{k,v}]` | 250 |
| `ancient-science-medicine.json` | 49 K | `list[{k,v}]` | 211 |
| `ancient-greek-philosophy.json` | 36 K | `list[{k,v}]` | 128 |
| `ancient-law-codes.json` | 35 K | `list[{k,v}]` | 100 |
| `ancient-proverbs-maxims.json` | 15 K | `list[{k,v}]` | 56 |
| `ancient-philosophy-glossary.json` | 11 K | `list[{k,v}]` | 47 |
| `ancient-eastern-wisdom.json` | 10 K | `list[{k,v}]` | 45 |
| `ancient-history.json` | 10 K | `list[{k,v}]` | 33 |
| `life-data.json` | 49 K | `list[{k,v}]` | n/a |
| `coding-knowledge.json` | 18 K | `list[{k,v}]` | 51 |
| `cook-knowledge.json` | 8.6 K | `list[{k,v}]` | 25 |

#### Dictionary companion files (5)

`eastern-wisdom-dictionary.json` (45 entries), `greek-philosophy-dictionary.json`, `hermetic-dictionary.json` (sized 73K), `history-dictionary.json`, `law-dictionary.json`, `literature-dictionary.json` (100K), `medical-dictionary.json` (80K), `philosophy-dictionary.json`, `proverbs-dictionary.json` (23K), `roman-dictionary.json` (84K). All dict-shaped, ~10–100K each, ~0.5 MB total.

`.pre-v13.bak` files exist for `brain-data.json` and the shell — keep as rollback.

### 4.2 `shell/`

| File | Size | Notes |
|---|---:|---|
| `TRU_LOGOS_shell.html` | 64 K | The actual LOGOS shell — this is the stage-2 "shell/template.html" equivalent |
| `TRU_LOGOS_shell.html.pre-v13.bak` | 62 K | Pre-v13 backup |

### 4.3 `manifest.json`

18 entries, 99.8 MB total, matches `data/` file list. Same `manifest.json` shape as the `encyclopedia-data`/`dict-data` slot entries.

### 4.4 `builds/`, `build.py`, `README.md`

Standard LOGOS build artefacts. README is the public handoff (DARPA pitch, build bible gist refs).

---

## 5. `Projects/TRU/omega/` — experimental graph engine

| File | Size | Schema | Count | Notes |
|---|---:|---|---:|---|
| `brain/core.json` | 9.5 M | `{version, nodes}` | n/a | OMEGA's own brain — different shape, do not merge with `current/brain.json` |
| `brain/edges.json` | 107 K | `list[{s, r, t, w}]` | 1,956 | Subject→object triples with weight |
| `brain/manifesto.json` | 783 B | dict | n/a | OMEGA identity/archetype/sovereign block |
| `brain/stats.json` | 725 B | dict | 9 keys | Per-type/per-source counts |
| `data/glossary.json` | 5.1 M | dict with `entries` array | n/a | Glossary for OMEGA |
| `data/index.json` | 3.4 M | dict with `node_lookup` | n/a | Node index |
| `TRU_OMEGA_v1.html`, `dist/omega-v0.2.html` | — | — | — | OMEGA build outputs |

OMEGA is a separate engine. **Do not import OMEGA data into the LOGOS/current pipelines** — schemas are incompatible.

---

## 6. `TRU-release/data/` — legacy snapshot (Jun 19)

Same files as canonical `Projects/TRU/data/` minus the `b64`/`brotli`/`js` wrappers:

`kjv_full.json` / `strongs_greek.json` / `strongs_hebrew.json` / `strongs_lexicon_kaiserlik.json` / `xref_compact.json` / `strongs_verse_index_compact.json`. Last touched 2026-06-19. **Do not edit — frozen.**

---

## 7. Mirrors / orphans

- `tru-unified-build/tru-offline-clone/Projects/TRU/data/` — full byte-clone of canonical data, untouched
- `repos/logos-engine/TRU/kjv_lookup.json` — separate fork mirror
- `/home/workspace/kjv_complete.json` — **different schema** (`{books: [{book, chapters: [{chapter, verses: [{verse, text}]}]}]}`), 5 MB. Not used by any current pipeline; leave alone.

---

## 8. Canonical sources — final decision

| Domain | Canonical | Why |
|---|---|---|
| Brain (active build) | `Projects/TRU/current/brain.json` | Most recent, has version/exported envelope, ties to `current/build_phase27.py` + `current/template.html` |
| Brain (LOGOS build) | `Projects/TRU/ship/tru-logos-source/data/brain-data.json` | LOGOS schema; 954 nodes is intentional small core |
| KJV text | `Projects/TRU/data/kjv_full.json` | All 31,100 verses, four-field shape matches what TRU templates expect |
| Strong's Greek | `Projects/TRU/data/strongs_greek.json` | Standard 5,523-entry G#### keying |
| Strong's Hebrew | `Projects/TRU/data/strongs_hebrew.json` | Standard 8,674-entry H#### keying |
| Strong's combined | `Projects/TRU/data/strongs_lexicon_kaiserlik.json` | 12,040 entries (combined + extended) |
| Strong's verse index | `Projects/TRU/data/strongs_verse_index_compact.json` | 7× smaller than `_index.json`, same keys |
| Cross-references | `Projects/TRU/data/xref_compact.json` | Already compact, 30,412 entries |
| WordNet | `Projects/TRU/data/wordnet_compact.json` | Same content as LOGOS `dict-data.json` |
| Knowledge bank | `Projects/TRU/data/tru-knowledge-bank.json` | Newer (Jun 27) |
| OMEGA brain + glossary | `Projects/TRU/omega/{brain,data}/` | Do **not** import into LOGOS/current |
| LOGOS encyclopedia | `Projects/TRU/ship/tru-logos-source/data/encyclopedia-data.json` | 5,646 articles, already used by `encyclopedia-data` head slot |
| LOGOS dictionaries (companion) | `Projects/TRU/ship/tru-logos-source/data/{eastern,greek,hermetic,history,law,literature,medical,philosophy,proverbs,roman}-dictionary.json` | LOGOS-specific |

## 9. Duplicates worth knowing about

1. `Projects/TRU/data/TRU_MEGA_BRAIN.json` ≡ `Projects/TRU/data/brain_canonical.json` — byte-identical 6,981,840 bytes. One of them can go; recommend keeping `brain_canonical.json` (more descriptive name).
2. `Projects/TRU/data/kjv_full.json` is mirrored in `kjv_bible.js`, `bible_*.b64`, `coil_*.txt`, `bible_job_book.txt`, `nt_b64.txt`, `ot_b64.txt` — same content, different transports. Keep the JSON as canonical, the wrappers stay as build artefacts.
3. `Projects/TRU/data/wordnet_compact.json` ≈ `Projects/TRU/ship/tru-logos-source/data/dict-data.json` — same 147,982 lemmas. Do not delete one to "consolidate" — they have different keying in some entries and are consumed by different builds.
4. `Projects/TRU/data/strongs_verse_index.json` and `..._compact.json` have the same 13,654 keys; the compact form is the one to use at runtime.
5. `TRU/TRU_BRAIN_41.json` (30,762 nodes) overlaps `current/brain.json` (30,745) by ~99.9% — small downstream drift. Read-only mirror; do not promote to canonical.

## 10. What's missing for stage 2

- `Projects/TRU/current/template.html` does not contain `{{DATA_SLOTS}}` sentinel — stage 2 sentinel injection has not landed here yet, or lives elsewhere. The LOGOS shell at `Projects/TRU/ship/tru-logos-source/shell/TRU_LOGOS_shell.html` is the working shell.
- `current/tru_module_manifest.json` only enumerates `encyclopedia-data` + `dict-data` head slots. Needs to grow to include kjv, strongs, xref, wordnet slots.
- `current/tru_module_manifest.json` is 336 B; the LOGOS `ship/tru-logos-source/manifest.json` is 18 entries / 99.8 MB. These are different things in different trees — the former is the **head-slot manifest** the template uses to inject body data, the latter is a **build-pipeline manifest** tracking all data files. The current/truth inventory should grow `current/tru_module_manifest.json` into the head-slot form, mirroring the LOGOS slot IDs.
