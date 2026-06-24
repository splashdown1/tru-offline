# TRU LOGOS

this is the merged TRU build.

## what it includes
- local offline brain + kjv
- doctrine lookup
- bm25 local search
- webllm escalation for gap queries
- memory overlay
- hold-to-talk
- mobile-safe layout
- cinzel/title styling

## how it behaves
- scripture and doctrine are answered locally first
- normal questions try webllm if available
- if webllm is unavailable, TRU falls back to local brain search
- memory survives reload in localStorage
- the relic circle on mobile supports hold-to-talk

## files
- `TRU_LOGOS.html`
- `TRU_LOGOS_README.md`

## notes
- this is the merged version from multiple TRU lineages
- it is still self-contained and offline-capable
- it expects a browser with localStorage; webllm is optional
