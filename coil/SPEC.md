# COIL SYNC PROTOCOL — v2.0.0 Specification
**Status: Finalized 2026-07-13**

---

## What changed from v1

| Area | v1 | v2 |
|---|---|---|
| Chunk suffix | `.bin` | `.part` (zero-padded offset) |
| Manifest | one per server response | one per file (`.MANIFEST.json`) + per-run `ROLLUP.json` |
| Default chunk size | 1 MiB | 1 MiB (configurable) |
| Packer location | inlined in server | standalone `scripts/coil_daily_pack.py` |
| Tie-in | manual | automatic via `scripts/coil_loop_hook.py` |
| Validation | server-side | client-side: per-chunk sha256 + top-level sha256 |
| `ROLLUP.json` | n/a | one per pack run, lists all per-file manifests |

## Layout

```
coil_pack/
├── X.0000000000.part
├── X.0000001048576.part
├── ...
├── X.MANIFEST.json
├── Y.0000000000.part
├── Y.MANIFEST.json
└── ROLLUP.json
```

## Per-file manifest

```json
{
  "fileId": "X",
  "sourcePath": "/abs/path/X",
  "size": 12345,
  "sha256": "top-level sha256 of the full file",
  "chunkSize": 1048576,
  "chunkCount": 12,
  "packedAt": "2026-07-13T18:00:00+00:00",
  "chunks": [
    { "index": 0, "offset": 0, "size": 1048576, "sha256": "...", "name": "X.0000000000.part" },
    ...
  ]
}
```

## Rollup

`ROLLUP.json` is the index for one pack run: a list of per-file
manifests with their sha256, plus run metadata. Verifying the rollup
is the same as verifying each manifest's top-level sha256.

## Validation contract

1. For each chunk in a manifest, `sha256(open(name,'rb').read())` must
   equal `chunks[i].sha256`.
2. Concatenating all chunks in order must reproduce a buffer whose
   `sha256` equals the manifest's top-level `sha256`.

## Pack CLI

```bash
python3 scripts/coil_daily_pack.py /path/to/bundle.html \
    --out /path/to/coil_pack \
    --chunk-size 1048576
```

## Drift-loop hook (logos-engine)

`scripts/coil_loop_hook.py` is the standard tie-in: it finds the newest
`*.html` bundle in a directory, runs the packer against it, and prints
a one-line summary. `logos-engine/TRU/build_daily_bundle.py` calls it
on every drift-corrected run.

## v1 reference

The original v1 implementation is preserved at `v1-legacy/`. Files
there are **frozen** and used only as a reference for clients still on
v1.
