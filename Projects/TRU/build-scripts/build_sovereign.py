#!/usr/bin/env python3
"""Build TRU_SOVEREIGN — quality-purified brain. Drops all verse nodes (redundant with kjv-data)."""
import json, re, os, glob

BASE = "/home/workspace"
SRC_HTML = f"{BASE}/Projects/TRU/versions/TRU_LOGOS.html"
OUT_HTML = f"{BASE}/TRU_SOVEREIGN.html"

def load(p):
    with open(p, "r", encoding="utf-8") as f: return json.load(f)

def compact(obj): return json.dumps(obj, ensure_ascii=False, separators=(",",":"))

# verse-pattern key: bookname_chapter:verse or bookname_chapter_verse or bible_*
verse_re = re.compile(r'^[a-z0-9_]+_\d+[:_]\d+', re.I)

def is_verse_node(n):
    k = n.get("k","").strip().lower()
    if k.startswith("bible_"): return True
    if verse_re.match(k): return True
    return False

def is_junk(n):
    v = n.get("v","").strip()
    if not v or len(v) < 40: return True
    return False

print("merging brains (quality filter — drop ALL verse nodes)...")
merged = {}
sources = [
    ("current/brain.json", f"{BASE}/Projects/TRU/current/brain.json"),
    ("mega_brain",         f"{BASE}/Projects/TRU/data/TRU_MEGA_BRAIN.json"),
    ("B41_archive",        f"{BASE}/Projects/TRU/data/TRU_BRAIN_41_ARCHIVE.json"),
]

total_in = 0
dropped_verse = 0
dropped_junk = 0
for label, path in sources:
    if not os.path.exists(path):
        print(f"  {label}: MISSING — skip")
        continue
    d = load(path)
    nodes = d.get("nodes", d if isinstance(d, list) else [])
    cnt = 0
    for n in nodes:
        total_in += 1
        if is_verse_node(n): dropped_verse += 1; continue
        if is_junk(n): dropped_junk += 1; continue
        k = n["k"]
        # keep richest (longest v)
        if k not in merged or len(n.get("v","")) > len(merged[k].get("v","")):
            merged[k] = {"k": k, "v": n["v"], "w": n.get("w",0.8), "t": n.get("t","fact"), "source": n.get("source","TRU")}
            cnt += 1
    print(f"  {label}: {len(nodes)} -> +{cnt} kept")

brain = list(merged.values())
print(f"  TOTAL IN: {total_in} | dropped verse: {dropped_verse} | dropped junk: {dropped_junk}")
print(f"  FINAL BRAIN: {len(brain)} pure knowledge nodes")

# sort by weight desc for consistency
brain.sort(key=lambda n: -float(n.get("w",0.5)))

# ---- load data blocks ----
print("loading data blocks...")
kjv = load(f"{BASE}/Projects/TRU/data/kjv_full.json")
greek = load(f"{BASE}/Projects/TRU/data/strongs_greek.json")
hebrew = load(f"{BASE}/Projects/TRU/data/strongs_hebrew.json")
lex = load(f"{BASE}/Projects/TRU/data/strongs_lexicon_kaiserlik.json")
print(f"  kjv={len(kjv)} greek={len(greek)} hebrew={len(hebrew)} lex={len(lex)}")

# merge strongs: lexicon primary
strongs = {}
strongs.update(lex)
for src in (greek, hebrew):
    for k, v in src.items():
        if k not in strongs: strongs[k] = v
        else:
            for f in ("l","t","d","k"):
                if not strongs[k].get(f) and v.get(f): strongs[k][f] = v[f]
print(f"  merged strongs={len(strongs)}")

# ---- load + patch LOGOS shell ----
print("loading LOGOS shell...")
with open(SRC_HTML, "r", encoding="utf-8", errors="replace") as f:
    html = f.read()

def replace_block(html, tag, new_content):
    pattern = r'(<script type="application/json" id="' + re.escape(tag) + r'">)(.*?)(</script>)'
    m = re.search(pattern, html, re.DOTALL)
    if not m: print(f"  !! {tag} not found"); return html
    html = html[:m.start(1)] + m.group(1) + new_content + m.group(3) + html[m.end(3):]
    return html

print("replacing blocks...")
html = replace_block(html, "brain-data", compact([{k: n[k] for k in ("k","v")} for n in brain]))
html = replace_block(html, "kjv-data", compact([{k: v[k] for k in ("ref","text")} for v in kjv]))
html = replace_block(html, "strongs-data", compact(strongs))

# update counts
html = re.sub(r'const KJV_COUNT=\d+;', f'const KJV_COUNT={len(kjv)};', html)
html = re.sub(r'const BRAIN_COUNT=\d+;', f'const BRAIN_COUNT={len(brain)};', html)
# also patch any hardcoded "30,762" in boot text
html = html.replace("30,762", f"{len(brain):,}")

# ---- strip webgpu ----
print("stripping webgpu...")
s = html.find("// ====================================\n// TRU WEBLLM LAYER")
e = html.find("// ── hybrid live LLM layer")
if s != -1 and e != -1: html = html.replace(html[s:e], "")
s = html.find("// ── escalation layer 1")
e = html.find("// ── escalation layer 2")
if s != -1 and e != -1: html = html.replace(html[s:e], "")
html = html.replace('const _wg=webLLMCheck();statusEl.textContent="● ONLINE • LOGOS READY • OFFLINE"+(_wg?" • WebGPU":"");',
                    'statusEl.textContent="● ONLINE • LOGOS READY • OFFLINE";')
html = html.replace('if(low==="webllm"||low==="model"||low==="llm") return cmdWebLLM(q);', '')
for sym in ("TRU_WEBLLM","webLLMCheck","cmdWebLLM","_wg","navigator.gpu"):
    if sym in html: print(f"  !! dangling: {sym}")

# ---- write ----
print("writing...")
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)
sz = os.path.getsize(OUT_HTML)
print(f"\nDONE: {OUT_HTML}")
print(f"size: {sz:,} bytes = {sz/1048576:.2f} MB")
print(f"brain: {len(brain)} nodes")
