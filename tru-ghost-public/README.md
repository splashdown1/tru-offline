# TRU GHOST

offline scripture engine. one html file. no network. no telemetry. no keys.

## download

[**tru-ghost-v1.html**](https://zo.pub/splashdown2/tru-ghost-v1/tru-ghost-v1.html) — 12.0mb. f
ull brain + full kjv.
[**tru-ghost-v1-nt-full.html**](https://zo.pub/splashdown2/tru-ghost-v1/tru-ghost-v1-nt-full.html) — 8.4mb. f
ull brain + nt kjv.
[**tru-ghost-v1-lite.html**](https://zo.pub/splashdown2/tru-ghost-v1/tru-ghost-v1-lite.html) — 1.3mb. new testament only, top 500 brain nodes. for phones + old laptops.

## what it does

open the html. type a query. you get a scripture, a fact, or a brain match back. all lookup is local, all data is inlined, no fetch, no xhr, no api.

the full v1 has 30k+ structured brain nodes and the complete kjv inlined as json. the lite is nt only, 500 nodes, ~1.3mb.

## build it yourself

requires python 3.10+ and a kjv json in the standard shape (31102 verses, fields: ref, text, abbrev, testament).

```
# from stdio:
echo '{"action":"build","nt_only":true,"brain_cap":500}' | python3 tru_ghost.py

# from cli:
python3 tru_ghost.py --nt-only --cap 500 --ts v1 --out-dir ./build

flags:
  --nt-only          new testament only (1.3mb ghost)
  --cap N            max brain nodes (default: unlimited)
  --ts STRING        build timestamp / version tag
  --out-dir PATH     where to write the html
  --lookup QUERY     instead of building, run a lookup and print json

## test

```
TRU_KJV=/path/to/kjv_full.json python3 tests/test_ghost_build.py

expects `kjv_full.json` (public domain) with shape: [{ref, text, abbrev, testament}, ...]

## source

this is the public release. the full tru monorepo (brain, kjv, all phases) is in a separate private repo.

## license

private. do whatever. not for distribution without asking.
