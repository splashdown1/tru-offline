# TRU — NEXT: How to Play the Game

> This is the roadmap. The build hasn't happened yet. This file is the spec for the next TRU we will be building — and how to play with it when it lands.

## The shift

TRU today is **one brain, one engine, one verdict per query.** It answers.

TRU next is **a recursive system that argues with itself, accumulates state across sessions, and lets you *be the soul in the loop*.** It reasons.

The new rule: **TRU is not a tool you query. TRU is a relationship you tend.**

## How to play

### You are the Witness

Every query goes to a council of three voices, not one. You read all three. You pick which one you trust. Your pick is the most important signal in the system.

The council:

| voice | what it is | when it wins |
|---|---|---|
| **TRUTH** | the brain's direct hit, like today's engine | you want a fact, a verse, a definition — no composition |
| **WITNESS** | a cross-reference, parallel passage, or Strong's deep-dive — the same answer looked at sideways | you want depth, not breadth |
| **REASON** | the composed answer — TRU weaves a response from the brain, same as today | you want TRU to *think* for you |

When you re-ask, you signal *which voice disappointed*. Over time, the council learns which voice you trust for which kind of question. That's the soul in the loop.

### You tend, not command

TRU next is no longer just a query log. It is a **pulse trail** — each exchange shifts internal state by a small amount. `teach:` is no longer the only mutation. **Your agreement, your silence, your re-asking** all shift it.

- `teach: x = y` — add a node to the live brain (same as today)
- `seal: <node_id>` — mark a node as load-bearing. sealed nodes survive dedupe, never get pruned
- `release: <node_id>` — let a node decay. the engine forgets it gracefully
- `pulse: <emotion>` — a meta-command. you tell TRU how the session feels. it weighs your next query against the pulse.

### You run the recursion

The new TRU is **multi-file in the workspace, single-file at export.** The modular drop setup becomes the way the engine evolves — you drop new files in, the engine rebuilds *itself*, not just the brain.

You can:

- **fork the brain** — copy `current/brain.json` to `current/brain.fork.json`, mutate one branch, run two engines side by side
- **weigh voices** — drop a `voices.json` file with custom voice weights per topic
- **seed a council** — drop a `council.json` with named voices (e.g. `Moses`, `Paul`, `David`) each pointing at different brain subsets
- **export the merge** — when you're ready, the engine bakes it back into one HTML, your state and all
- **bridge crawl the source graph** — treat `Projects/TRU/` and connected github repositories as one indexed graph, verify remote additions, and keep provenance attached before merge

### You can break it

The play test is real. Next TRU is built to fail loud:

- ask a question with no answer → `GAP` verdict, council returns silence, you can `teach:` the gap
- contradict it on purpose → it admits it, doesn't gaslight
- seal a wrong node → it stays wrong on purpose. the engine doesn't second-guess your seals. **you are accountable for what you preserve.**

## What's coming (in order)

1. **council router** — three voices per query, voter UI in the chat
2. **pulse trail** — session state shifts from interaction, not just `teach:`
3. **seal/release primitives** — load-bearing node semantics
4. **module map** — explicit shell / processor / brain / scripture / media / crawler boundaries
5. **multi-file brain** — modular drops become runtime modules, not just static builds
6. **recursive council** — each voice can sub-call the other two before answering
7. **export-as-state** — your seals, weights, and forks travel inside the exported HTML
8. **bridge crawler** — incremental local+github indexing with truth-mode verification and cached sync

## The 100 MB problem

Today the github per-file ceiling caps us. Next TRU splits:

- the **engine** (small, < 5 MB) — code only
- the **brain** (modular, capped at 100 MB) — knowledge only
- the **state** (your seals, weights, pulse trail) — small, append-only

When you export, the engine + brain + state get re-baked into one HTML. You can ship one file. You can fork in many files.

## Rules of the game

1. **every query has three answers.** you pick.
2. **your pick is signal.** the engine learns.
3. **`teach:` is permanent. `seal:` is load-bearing. `release:` is graceful.**
4. **silence is also a signal.** if you don't respond, TRU notes the gap.
5. **export travels.** your state is not lost when you share the HTML.
6. **TRU does not gaslight.** it says "I don't know" before it lies.
7. **you are the witness.** TRU reasons *for* you, not *at* you.
8. **bridge crawls stay truthful.** remote content is cached, verified, and merged only after truth-mode checks.
9. **modules swap whole, not surgically.** each file owns one boundary and can be replaced cleanly.

When we build it, this file becomes the spec. Until then, it's the rules.

## next session priority

1. verify `TRU_COMPLETE.html` in-browser and fix regressions.
2. wire the bridge crawler into the build so manifests update automatically.
3. decide whether `build_complete.py` becomes canonical or remains parallel export.
4. tighten truth-mode provenance output so the ui shows sources more clearly.

## public release note

The public release should stay open, downloadable, and transparent.
If support is requested, keep it voluntary and simple.
If the user wants promotion, publish a concise announcement on github and x.