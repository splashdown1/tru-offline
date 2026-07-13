# COIL SYNC PROTOCOL™ — v2 Specification

**Status:** Active. v1 retained under `v1-legacy/` for reference.

---

## What changed from v1

| Concern | v1 | v2 |
|---|---|---|
| Compression | gzip only | gzip **or** zstd (`x-zstd: true`) |
| Encryption | client-side opt-in | header-negotiated E2E (`x-encrypted: true` + `iv` + `key-id`) |
| Manifest | implicit (chunk index) | explicit `GET /manifest/:fileId` returns `{index: hash, size, ts}` |
| Delta direction | client → server only | bidirectional (`POST /delta` so server can ask client for missing chunks) |
| Resume | checkpoint on client | server-side checkpoint (`POST /checkpoint` writes resumable session token) |
| Auth | none | bearer token (`Authorization: Bearer <COIL_TOKEN>`) on every write |
| Chunk size | fixed client-side | declared in `POST /session` (default 1 MiB, max 16 MiB) |
| Verification | SHA-256 of original chunk | SHA-256 of original **+** Merkle root pinned in `/complete` body |

v1 endpoints and headers still work; v2 is a strict superset.

---

## Endpoints (v2)

### `POST /session`
Open a resumable upload session.

**Headers:** `Authorization: Bearer <COIL_TOKEN>`, `x-original-name`, `x-original-size`, `x-chunk-size?`

**Response:** `200 { fileId, chunkSize, expectedChunks }`

### `POST /upload` *(v1-compatible)*
Same as v1. New optional headers: `x-encrypted`, `x-zstd`, `x-key-id`.

### `POST /checkpoint`
Persist server-side resume state. Body: `{ fileId, lastChunkIndex }`.

**Response:** `200 { ok, resumedAt }`

### `POST /delta` *(new)*
Server-initiated request for missing chunks. Body: `{ fileId, missing: [indices] }`.

**Response:** `200 { ok }` — server then re-issues chunks on the open stream.

### `GET /manifest/:fileId`
**Response:** `{ "0": {hash, size, ts}, "1": {...}, ... }`

### `POST /complete` *(v1-compatible + Merkle root)*
Body now includes `merkleRoot` (hex). Server verifies before finalizing.

**Response:** `200 { ok, fileId, finalHash, merkleVerified, outPath, chunksReconstructed }`

### `GET /status?fileId=<id>` *(v1-compatible, deprecated)*
Returns just the hash map. v2 clients should use `/manifest/:fileId`.

---

## Security

- All write endpoints require `Authorization: Bearer <COIL_TOKEN>`.
- Chunks are hashed (SHA-256) before any optional compression/encryption, and re-verified on the server.
- `merkleRoot` pinned at `/complete` catches bit-rot across the whole file.
- E2E encryption key never touches the server — only `key-id` and `iv` are sent in headers.

---

## Why this is the right home

COIL is the chunked transfer protocol that backs TRU offline payload delivery.
It lives inside `tru-offline` because every TRU engine that needs to ingest
multi-megabyte KB / brain / scripture bundles runs COIL under the hood.
The standalone `coil-system` repo is now archived — this directory is canonical.
