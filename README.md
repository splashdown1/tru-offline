# TRU OFFLINE

monorepo. brain. kjv. ghost builder. all phases. sovereign.
zero network. zero telemetry. zero cloud.

## structure

| path | what |
|---|---|
| `TRU_*.html`, `tru_v*.html`, `Scripture_Seeker.html` | legacy offline builds. self-contained. open in any browser. |
| `Projects/TRU/phase28/`, `current/`, `data/` | canonical build artifacts (brain, kjv, html) |
| `Projects/TRU/tru-chat-data/tru_ghost.py` | ghost builder. CLI or stdin. |
| `Projects/TRU/tru-chat-data/tests/` | smoke tests |
| `Projects/TRU/omega/` | submodule: TRU OMEGA single-file engine |
| `tru-site/` | submodule: zo.site bun+hono version with live ghost export |

## clone

```bash
git clone https://github.com/splashdown1/tru-offline.git
cd tru-offline
git submodule update --init --recursive
```

## build the ghost

the ghost is a self-contained html with brain + kjv baked in. works offline, no api.

```bash
# full bible, all brain nodes (~12mb)
python3 Projects/TRU/tru-chat-data/tru_ghost.py --ts full

# new testament only, 500 brain nodes (~1.4mb)
python3 Projects/TRU/tru-chat-data/tru_ghost.py --nt-only --cap 500 --ts lite
```

output lands in `Projects/TRU/ghost/tru-ghost-<ts>.html`. open it. ask it things.

## flags

| flag | default | what |
|---|---|---|
| `--nt-only` | off | new testament only. drops size from ~12mb to ~1.4mb. |
| `--cap N` | unlimited | max brain nodes. 0 = unlimited. cap reduces size linearly. |
| `--ts NAME` | utc now | filename suffix. |
| `--out-dir DIR` | `Projects/TRU/ghost/` | output dir. |
| `--lookup Q` | — | run one query against the brain+kjv, print result, exit. |

## lookup

```bash
python3 Projects/TRU/tru-chat-data/tru_ghost.py --nt-only --cap 100 --lookup "john 3:16"
# {"ok": true, "result": {"kind": "SCRIPTURE", "text": "john 3:16 — For God so loved...", "score": 100, "source": "kjv"}}
```

## test

```bash
python3 Projects/TRU/tru-chat-data/tests/test_ghost_build.py
```

runs 3 checks: lookup routing, minimal build, full no-cap build. exits 0 on pass.

## stdin api (backward compat)

the ghost also reads a json object on stdin and writes json on stdout. used by the zo.space route at `/api/tru-ghost`.

```json
{"action": "build", "nt_only": true, "brain_cap": 500}
{"action": "lookup", "q": "psalms 23"}
```

the route is at `https://splashdown2.zo.space/api/tru-ghost`. `?download=1` returns the html as an attachment.

## offline guarantee

the ghost html is a single file. brain + kjv inlined as JSON. no fetch, no xhr, no api. works on a plane.

the source files in this repo are also self-contained. no api keys, no external services, no telemetry.

## more

- `Projects/TRU/README.md` — how to talk to TRU (engine interaction guide)
- `Projects/TRU/README_NEXT.md` — the "play the game" spec for the next TRU
- `Projects/TRU/SOUL.md` — TRU's voice + identity spec

## license

private. do whatever. not for distribution without asking.
