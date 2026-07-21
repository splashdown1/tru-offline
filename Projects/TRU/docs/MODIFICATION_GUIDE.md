# TRU Data Modification Guide

How to add, swap, or remove a data slot in the LOGOS engine and the
canonical brain pipeline. Companion to `DATA_INVENTORY.md` and
`data/manifest.json`.

The offline engine is one self-contained HTML file. All data is
embedded in `<script type="application/json" id="X"> … </script>` tags
that the build script fills from the manifest. Nothing loads over the
network — there is no API route, no fetch. If the HTML is open, the
data is in it.

## 0. The two pipelines

There are two builders. They are independent and target different
shells.

| Pipeline | Shell | Build script | Manifest |
|---|---|---|---|
| **LOGOS** (18 slots, 99.8 MB embedded) | `Projects/TRU/ship/tru-logos-source/shell/TRU_LOGOS_shell.html` | `Projects/TRU/ship/tru-logos-source/build.py` | `Projects/TRU/ship/tru-logos-source/manifest.json` |
| **Phase 27 / 28** (single base64 brain) | `Projects/TRU/current/template.html`, `Projects/TRU/phase28/template.html` | `current/build_phase27.py`, `phase28/build_phase28.py` | `Projects/TRU/data/manifest.json` (canonical sources reference) |

When you change a data file, **rebuild the pipeline that consumes
that file**. The two pipelines don't share data on disk — they share
*content* (the LOGOS kjv-data and the canonical `Projects/TRU/data/kjv_full.json` are the same dataset in different formats).

## 1. The slot mechanism (LOGOS)

Every data slot is exactly this:

```html
<script type="application/json" id="kjv-data"></script>
```

The build script (`build.py`) reads the shell, finds every empty slot
tag, and replaces `"></script>` with `">CONTENT</script>` where
CONTENT is the JSON file listed for that `id` in `manifest.json`.

The inline consumer script reads the JSON like this:

```js
const _KJV = JSON.parse(
  document.getElementById('kjv-data')?.textContent || '{}'
);
```

Two important properties:
- **id is the contract.** The shell declares the `id`; the manifest
  declares the file; the consumer script reads the `id`. All three
  must agree.
- **Empty slot = boot fault.** If a slot tag is left empty, the
  consumer gets `'{}'` and the engine degrades silently. Rebuild
  before declaring "done."

## 2. To add a new data slot

Five steps. All five.

1. **Add the data file.** Put `data/my-new-data.json` in the LOGOS
   tree. Validate it's parseable JSON:
   `python3 -c "import json; json.load(open('data/my-new-data.json'))"`.

2. **Declare the slot in the shell.** In
   `shell/TRU_LOGOS_shell.html`, add the empty tag alongside the
   others (lines 88–128 in the current shell). Pick a stable `id`:

   ```html
   <script type="application/json" id="my-new-data"></script>
   ```

3. **Register it in the manifest.** Add an entry to
   `ship/tru-logos-source/manifest.json`:

   ```json
   {
     "id": "my-new-data",
     "file": "data/my-new-data.json",
     "bytes": 12345,
     "valid_json": true
   }
   ```

4. **Wire the consumer.** In the engine script (just below the other
   `JSON.parse(document.getElementById('…')…)` lines), add the read
   and any lookup helpers you need. Follow the existing
   `encLookup` / `dictLookup` / `kjvLookup` patterns — normalize
   input, try exact match, fall back to prefix/contains.

5. **Rebuild and verify.**

   ```bash
   cd Projects/TRU/ship/tru-logos-source
   python3 build.py --check
   ```

   Then boot the HTML in a headless browser, send a query that hits
   the new data, and confirm the response is non-empty.

## 3. To swap a data file (e.g. newer KJV text)

1. Replace the file at the manifest path. Keep the filename. Keep the
   schema (top-level shape) identical — the consumer script assumes
   `{ref, text}` for verses, `{word: [senses]}` for dictionary, etc.
2. Update `bytes` in `manifest.json` to the new size.
3. Rebuild: `python3 build.py`.
4. Verify the new file passes the smoke checks for the affected
   queries (`john 3:16`, the largest Strong's number you have a test
   for, etc.).

If the schema changes, also update the consumer script in the shell
and the entry in `data/manifest.json` under `Projects/TRU/data/` —
the modification is then a stage, not a swap. Open an issue or a
phase note.

## 4. To remove a data slot

1. Remove the entry from `manifest.json`.
2. Remove the empty tag from the shell.
3. Remove or guard the `JSON.parse(document.getElementById(...))`
   call. Search the shell for the `id` first — anything else that
   referenced it must be updated or the build will warn about unused
   ids.
4. Rebuild. `build.py` will `SystemExit` if a shell slot has no
   manifest entry, so a half-removed slot surfaces immediately.

## 5. The canonical brain (Phase 27 / 28)

These use a different mechanism: a single base64-encoded JSON dump
substituted into the template at build time.

- Template placeholder: `__TRU_PHASE27_BRAIN_B64__` (or `__TRU_PHASE28_BRAIN_B64__`).
- Build reads `brain.json` from the same folder as the template, JSON
  stringifies the `nodes` array, base64-encodes, and `str.replace`s
  the placeholder.
- Consumer: `JSON.parse(atob(_b64))`.

To swap the brain:
1. Replace `Projects/TRU/current/brain.json` (or
   `phase28/brain.json`). Required shape: `{"nodes": [...]}` where
   each node is `{k, v, w, t, source}`.
2. Run `python3 build_phase27.py` (or `build_phase28.py`).
3. Confirm the printed node count matches what you loaded.

The canonical brain (`Projects/TRU/current/brain.json`, 30,745 nodes
as of 2026-07-13) is also the source for all the larger bundled HTMLs
at the workspace root (`TRU_APEX7.html`, etc.). Updating
`current/brain.json` is a no-op for those — each bundled HTML has
its brain frozen at build time.

## 6. The canonical data set (`Projects/TRU/data/`)

This folder is the "specimen collection" — one canonical file per
data kind, with the rest either converted versions of the same data
or experimental alternates.

- **kjv_full.json** (6.7 MB) is the canonical scripture. The LOGOS
  kjv-data.json is the same content re-cut to `{ref, text}` per
  verse. The `xref_compact.json` is built from it.
- **strongs_hebrew.json + strongs_greek.json + strongs_verse_index_compact.json**
  are the canonical lexicon triple. Anything that says "Strong's"
  should resolve through these.
- **TRU_MEGA_BRAIN.json** (6.8 MB) is the canonical brain dump in
  the un-base64 form. phase28's brain was generated from a snapshot
  of this; current/brain.json is the live version under iteration.
- **TRU_CORE_KB.json, theology_compact.json, rhetoric_compact.json,
  truth_kaiserlik.json** are the four worldview / doctrine
  dictionaries. Anything that does concept lookup by key uses one
  of these.
- **tru_super_brain.js** is a legacy JS dump — a global variable
  assignment that older shells loaded via `<script>`. Do not edit
  it. It's a build artifact of `build_70.py` era. The canonical
  brain is `current/brain.json`; this file is reference only.

The full table (file, size, role, schema, notes) lives in
`DATA_INVENTORY.md`. The `data/manifest.json` in this folder is the
single-machine-readable reference — point your tooling at it instead
of globbing.

## 7. Verification checklist (use after every change)

```bash
# LOGOS: rebuild + byte-check
cd Projects/TRU/ship/tru-logos-source
python3 build.py --check
# Phase 27/28: rebuild
cd ../current && python3 build_phase27.py
cd ../phase28 && python3 build_phase28.py
```

Then open the resulting HTML in a headless browser and exercise:

- `version` → "31,015 nodes online" (or current count)
- `john 3:16` → returns Genesis/John text, not a routing error
- `what is grace` → returns doctrine entry from TRU_CORE_KB
- `define logos` → returns dictionary sense
- `who is julius caesar` → returns encyclopedia entry
- reload the page → conversation history persists, doctrine entries
  persisted, no console errors

A change is "done" only when all six pass. If any of them fail, the
build is partial — fix the manifest, the shell, or the consumer and
rebuild before declaring success.

## 8. Things that are not data

These files look like data but are build wrappers. Don't list them
as data; don't try to swap them via the manifest.

- `Projects/TRU/build-scripts/build_*.py` — historical and current
  builders for the various bundled HTMLs at the workspace root.
- `Projects/TRU/ship/tru-logos-source/build.py` — the LOGOS
  builder (the only one that reads `manifest.json`).
- `Projects/TRU/current/build_phase27.py`,
  `Projects/TRU/phase28/build_phase28.py` — the brain-base64
  builders.
- `Projects/TRU/ship/tru-logos-source/shell/TRU_LOGOS_shell.html`
  — the LOGOS shell (HTML + inline JS). Reads slots by id.
- `Projects/TRU/current/template.html`,
  `Projects/TRU/phase28/template.html` — the brain-base64 shells.

If you find yourself wanting to modify one of these, you're past
the data layer and into the engine layer. Open a phase and write a
proper design doc — these files are not data, they're code.
