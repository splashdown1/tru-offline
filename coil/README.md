# COIL — Chunked Offline Interchange Layer

COIL is the chunked transfer protocol that backs TRU offline payload
delivery. Brain KB bundles, scripture indexes, holographic manifests —
any multi-megabyte asset that needs to land in a TRU engine runs through
COIL.

## Layout

- [`SPEC.md`](./SPEC.md) — **v2 specification** (active)
- [`v1-legacy/`](./v1-legacy/) — v1 reference implementation, frozen

## Versioning

v2 is a strict superset of v1. v1 endpoints and headers still work; new
clients should prefer v2 endpoints (session, checkpoint, manifest,
delta, merkle verification).
