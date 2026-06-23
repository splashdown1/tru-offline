#!/usr/bin/env python3
"""Build TRU_100.html — target ~100MB, all real content."""
import json, re, os, glob

BASE = "/home/workspace"
SRC_HTML = f"{BASE}/Projects/TRU/versions/TRU_LOGOS.html"
OUT_HTML = f"{BASE}/TRU_100.html"

def load(p):
    with open(p, "r", encoding="utf-8") as f: return json.load(f)
def compact(o): return json.dumps(o, ensure_ascii=False, separators=(",",":"))
def norm(s): return s.strip().lower().replace(" ","_") if isinstance(s,str) else str(s)

# ---- merge ALL brains ----
print("merging all brains...")
BRAIN_SOURCES = [
    f"{BASE}/Projects/TRU/current/brain.json",
    f"{BASE}/repos/tru-archive/TRU_BRAIN_41.json",
    f"{BASE}/repos/tru-omega/brain/core.json",
    f"{BASE}/Projects/TRU/phase28/brain.json",
    f"{BASE}/TRU-release/current/brain.json",
    f"{BASE}/repos/tru-archive/TRU_brain.json",
    f"{BASE}/Projects/TRU/data/tru_brain_1290_nodes.json",
]
merged = {}
for fp in BRAIN_SOURCES:
    if not os.path.exists(fp): print(f"  skip (missing): {fp}"); continue
    d = load(fp)
    nodes = d.get("nodes", d) if isinstance(d, dict) else d
    if not isinstance(nodes, list): print(f"  skip (bad shape): {fp}"); continue
    added = 0
    for n in nodes:
        if not isinstance(n, dict) or "k" not in n or "v" not in n: continue
        k = norm(n["k"])
        if k in merged:
            # keep richer (longer v)
            if len(str(n.get("v",""))) > len(str(merged[k].get("v",""))):
                merged[k] = {f: n.get(f) for f in ("k","v","w","t","source","ref") if n.get(f) is not None}
        else:
            merged[k] = {f: n.get(f) for f in ("k","v","w","t","source","ref") if n.get(f) is not None}
            added += 1
    print(f"  {os.path.basename(fp)}: +{added} (total {len(merged)})")

# ---- add SEC primaries as brain nodes ----
print("adding SEC primaries...")
prim_files = sorted(glob.glob(f"{BASE}/primaries/sec/*/_index.json"))
prim_added = 0
for fp in prim_files:
    d = load(fp)
    name = d.get("name","").strip()
    cik = d.get("cik","")
    for fl in d.get("filings", []):
        excerpt = fl.get("text_excerpt","")
        if not excerpt or len(excerpt) < 50: continue
        form = fl.get("form","")
        date = fl.get("filing_date","")
        k = f"sec_{cik}_{form}_{date}".lower().replace(" ","_")
        # cap excerpt to keep ~100MB target
        v = excerpt[:319000]
        merged[k] = {"k": k, "v": v, "w": 0.5, "t": "filing", "source": "SEC_EDGAR", "ref": fl.get("source_url","")}
        prim_added += 1
print(f"  +{prim_added} primary filing nodes (total {len(merged)})")

brain = list(merged.values())
print(f"  FINAL BRAIN: {len(brain)} nodes")

# ---- load data blocks ----
print("loading data blocks...")
kjv = load(f"{BASE}/Projects/TRU/data/kjv_full.json")
xref = load(f"{BASE}/Projects/TRU/data/xref_compact.json")
sidx = load(f"{BASE}/Projects/TRU/data/strongs_verse_index.json")  # FULL (19.7MB)
greek = load(f"{BASE}/Projects/TRU/data/strongs_greek.json")
hebrew = load(f"{BASE}/Projects/TRU/data/strongs_hebrew.json")
lex = load(f"{BASE}/Projects/TRU/data/strongs_lexicon_kaiserlik.json")
kjv_lookup = load(f"{BASE}/TRU/kjv_lookup.json")  # 62,200 verses

# merge strongs (lexicon primary)
strongs = dict(lex)
for src in (greek, hebrew):
    for k, v in src.items():
        if k not in strongs: strongs[k] = v
        else:
            for f in ("l","t","d","k"):
                if not strongs[k].get(f) and v.get(f): strongs[k][f] = v[f]

print(f"  kjv={len(kjv)} xref={len(xref)} sidx={len(sidx)} strongs={len(strongs)} kjv_lookup={len(kjv_lookup)}")

# ---- load + patch shell ----
print("loading shell...")
with open(SRC_HTML, "r", encoding="utf-8", errors="replace") as f: html = f.read()
print(f"  source: {len(html)/1048576:.2f} MB")

# ---- replace data blocks ----
def replace_block(html, tag, content):
    pat = r'(<script type="application/json" id="' + re.escape(tag) + r'">)(.*?)(</script>)'
    m = re.search(pat, html, re.DOTALL)
    if not m: print(f"  !! {tag} not found"); return html
    old = len(m.group(2))
    html = html[:m.start(1)] + m.group(1) + content + m.group(3) + html[m.end(3):]
    print(f"  {tag}: {old:,} -> {len(content):,}")
    return html

print("embedding blocks...")
html = replace_block(html, "brain-data", compact(brain))
html = replace_block(html, "kjv-data", compact([{k: v[k] for k in ("ref","text")} for v in kjv]))
html = replace_block(html, "strongs-data", compact(strongs))
html = replace_block(html, "xref-data", compact(xref))
html = replace_block(html, "strongs-idx", compact(sidx))

# add kjv-lookup as a NEW block (insert before </head> or after strongs-idx)
lookup_block = f'<script type="application/json" id="kjv-lookup">{compact(kjv_lookup)}</script>'
html = html.replace("</head>", lookup_block + "\n</head>", 1)
print(f"  kjv-lookup: +{len(compact(kjv_lookup)):,} (new block)")

# update counts
html = re.sub(r'const KJV_COUNT=\d+;', f'const KJV_COUNT={len(kjv)};', html)
html = re.sub(r'const BRAIN_COUNT=\d+;', f'const BRAIN_COUNT={len(brain)};', html)

# ---- strip webgpu ----
print("stripping webgpu...")
strips = []
s = html.find("// ====================================\n// TRU WEBLLM LAYER")
e = html.find("// ── hybrid live LLM layer")
if s != -1 and e != -1: strips.append((html[s:e], ""))
s = html.find("// ── escalation layer 1")
e = html.find("// ── escalation layer 2")
if s != -1 and e != -1: strips.append((html[s:e], ""))
# escalation call
strips.append(('const _wg=webLLMCheck();statusEl.textContent="● ONLINE • LOGOS READY • OFFLINE"+(_wg?" • WebGPU":"");',
               'statusEl.textContent="● ONLINE • LOGOS READY • OFFLINE";'))
# route dispatch: remove webllm/llm case entirely
strips.append(('if(low==="webllm"||low==="model"||low==="llm") return cmdWebLLM(q);', ''))
for old, new in strips:
    if old in html: html = html.replace(old, new, 1)

for sym in ("TRU_WEBLLM","webLLMCheck","cmdWebLLM","_wg","navigator.gpu"):
    if sym in html: print(f"  !! dangling: {sym}")

# ---- write ----
print("writing...")
with open(OUT_HTML, "w", encoding="utf-8") as f: f.write(html)
sz = os.path.getsize(OUT_HTML)
print(f"\nDONE: {OUT_HTML}")
print(f"size: {sz:,} bytes = {sz/1048576:.2f} MB")
print(f"target 100 MB, delta: {(sz/1048576)-100:+.2f} MB")
