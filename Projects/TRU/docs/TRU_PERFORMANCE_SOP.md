# tru performance and device profile sop

**timestamp:** 21 july 2026, 05:25 america/chicago
**status:** planning sop; no runtime changes authorised

## purpose

this sop prevents the maximum-content archive from becoming the default burden on every device.

## 1. performance principles

- measure first, optimise second.
- first interaction matters more than total archive readiness.
- load only the modules required by the selected profile.
- retain the maximum build as an intentional archive profile.
- never trade grounding or state safety for a faster first paint.
- a failed optional module must be visible and recoverable.

## 2. profile budgets

exact numbers must be set after baseline measurement. the first planning pass uses relative priorities:

| profile | startup priority | memory priority | content priority |
|---|---|---|---|
| core | highest | highest | essential brain, kjv, status, help, gap |
| study | high | high | scripture, dictionary, strong's, commentary, xrefs |
| complete | balanced | balanced | broad everyday reference |
| max | lowest | lowest | full approved archive |

phase 0 must record numeric budgets for:

- file size.
- cold start.
- first answer.
- peak memory.
- post-answer memory.
- full profile readiness.

## 3. load sequence

1. render the shell and status.
2. validate the embedded manifest.
3. load the kernel and essential index.
4. make the first supported query interactive.
5. load profile-required modules.
6. load optional modules only when selected or requested.
7. update status with actual module readiness.

no loading screen may claim that all knowledge is online when only the core is ready.

## 4. mobile rules

- mobile profile excludes archive-only material by default.
- commentary and encyclopedia remain separate packs.
- large indexes use compact representations approved by the data inventory.
- long answers are paginated or collapsed without losing the underlying evidence.
- text-to-speech receives clean text, not markup.
- state writes are scheduled and recoverable rather than triggered on every keystroke.
- low-memory behaviour is tested with a long session, not just a fresh boot.

## 5. measurement procedure

for each profile and device target:

1. start from a fresh browser process.
2. open the exact artifact.
3. record time to shell render.
4. record time to interactive state.
5. send a fixed short prompt.
6. record first answer latency.
7. send a scripture prompt and a broad brain prompt.
8. record peak and steady-state memory.
9. reload and repeat the state check.
10. record console errors and module failures.
11. repeat after the profile has been idle.
12. save the report with timestamp and artifact hash.

## 6. performance failure handling

- if core is slow, inspect kernel, essential index, and startup parsing first.
- if first answer is fast but later lookup fails, inspect lazy module readiness and fallback state.
- if memory grows across a session, inspect retained answer objects, state journal, and duplicate indexes.
- if mobile degrades while desktop passes, do not simply raise the mobile limit; reduce the profile or split the module.
- if a profile needs a module outside its budget, move that capability to a named optional pack.

## 7. performance release gate

an artifact fails the performance gate if:

- it exceeds its approved profile budget.
- it blocks first interaction while loading nonessential modules.
- it reports ready before its required module is usable.
- it silently drops a requested capability.
- it causes state loss while reducing memory.
- it passes on desktop but has no declared mobile behaviour.
