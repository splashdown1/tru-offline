# tru build sop

## canon
- use one canonical source per layer.
- merge knowledge in a deterministic order.
- do not patch around a broken builder if a one-pass builder is possible.

## data safety
- sanitise all json before parse/stringify.
- reject bad control characters.
- preserve source text unless a transform is explicit.
- keep `define` routing from stripping the target word.

## routing order
1. help / hello / status / teach / recall / seal / release
2. scripture references
3. strong's / original-language lookups
4. define / dictionary
5. brain truth / reasoning
6. gap

## fixed smoke prompts
- what is life
- what is hope
- define love
- define plastic
- who is jesus
- john 3:16
- help
- status

## build rules
- fail if any fixed smoke prompt crashes.
- fail if the page boots but chat or answer layout breaks.
- fail if data injection changes the boot path silently.
- prefer one clean export over layered patches.
- bridge-crawler work must log verified local and remote sources into the thought-processor stream.
- remote content only enters the merged brain-data after truth-mode verification.
- cache every source path, hash, size, and verified timestamp so the next crawl only pulls changed files.
- the builder must write `current/tru_module_manifest.json` before export completes.

## bridge crawler
- treat `Projects/TRU/` and connected github repositories as one indexed source graph.
- fetch only changed remote files after cache comparison.
- merge verified remote additions into the codex-merged instrument.
- keep provenance attached to every accepted remote node.
- reject secrets, binaries, build noise, and unverified overrides.
- flag doctrine, routing, or answer-behaviour changes for review before merge.
- reflect accepted modules back into the manifest so the shell and exporter stay in sync.

The bridge crawler keeps the public manifest in sync with the build.
It must run as part of the real build path, not as a separate afterthought.

## public ship policy

TRU is meant to be openly inspectable and downloadable.
The public build should avoid hidden gates and should keep any support request voluntary.
If a release is shared publicly, prefer a simple donation link or mail-to option over coercive prompts.
Public updates should be announced on github and x when the release is actually ready.

## growth rule
- if the file gets too large, zip or split it.
- keep the giant export and the practical export both available.

## goal
- tru should answer grounded questions, admit gaps, and survive rebuilds without regressing old prompts.
