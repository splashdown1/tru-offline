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

## growth rule
- if the file gets too large, zip or split it.
- keep the giant export and the practical export both available.

## goal
- tru should answer grounded questions, admit gaps, and survive rebuilds without regressing old prompts.
