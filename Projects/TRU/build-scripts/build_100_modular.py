#!/usr/bin/env python3
"""Build TRU_100.html from the modular drop folder + canonical sources.

Drop files into /home/workspace/Projects/TRU/drop/<category>/ and rebuild.
Auto-dedupe against canonical brain + auto-categorize by content.

Categories (file extension or folder):
  brain/         *.json or *.txt → brain nodes (auto-detect format)
  scripture/     *.json → KJV/verses (replaces kjv-data block if bigger)
  lexicon/       *.json → Strong's/WordNet (merges into strongs block)
  filings/       *.json → SEC filings (added as filing-type brain nodes)
  encyclopedia/  *.json or *.txt → encyclopedia brain nodes (TYPE=encyclopedia)

If a drop folder is empty, the build runs clean off the canonical sources.
"""
import json, re, os, glob

BASE = "/home/workspace"
DROP = f"{BASE}/Projects/TRU/drop"
SRC_HTML = f"{BASE}/Projects/TRU/versions/TRU_LOGOS.html"
OUT_HTML = f"{BASE}/TRU_100.html"

def load(p):
    with open(p, "r", encoding="utf-8") as f: return json.load(f)
def compact(o): return json.dumps(o, ensure_ascii=False, separators=(",",":"))
def norm(s): return s.strip().lower().replace(" ","_") if isinstance(s,str) else str(s)

def node_ok(n):
    return isinstance(n, dict) and "k" in n and "v" in n

def shape_nodes(d):
    """Normalize any brain-shaped json into a list of {k,v,w,t,source}."""
    if isinstance(d, list):
        return [n for n in d if isinstance(n, dict)]
    if isinstance(d, dict):
        if "nodes" in d and isinstance(d["nodes"], list):
            return [n for n in d["nodes"] if isinstance(n, dict)]
        if "data" in d and isinstance(d["data"], list):
            return [n for n in d["data"] if isinstance(n, dict)]
        # fallback: only treat as nodes if values are dicts
        vals = list(d.values())
        if vals and all(isinstance(v, dict) for v in vals):
            return vals
    return []

# ---- merge ALL canonical brains ----
print("=== canonical brains ===")
BRAIN_SOURCES = [
    f"{BASE}/Projects/TRU/current/brain.json",
    f"{BASE}/repos/tru-archive/TRU_BRAIN_41.json",
    f"{BASE}/repos/tru-omega/brain/core.json",
    f"{BASE}/Projects/TRU/phase28/brain.json",
    f"{BASE}/TRU-release/current/brain.json",
    f"{BASE}/repos/tru-archive/TRU_brain.json",
    f"{BASE}/Projects/TRU/data/tru_brain_1290_nodes.json",
    f"{BASE}/Projects/TRU/data/TRU_MEGA_BRAIN.json",
    f"{BASE}/Projects/TRU/data/TRU_SUPER_BRAIN.json",
    f"{BASE}/Projects/TRU/data/TRU_CORE_KB.json",
    f"{BASE}/Projects/TRU/data/tru-knowledge-bank.json",
]
merged = {}
for fp in BRAIN_SOURCES:
    if not os.path.exists(fp): print(f"  skip (missing): {fp}"); continue
    try: d = load(fp)
    except Exception as e: print(f"  skip (bad json {e}): {fp}"); continue
    nodes = shape_nodes(d)
    if not isinstance(nodes, list):
        print(f"  skip (non-list {type(nodes).__name__}): {fp}"); continue
    if not nodes: print(f"  skip (empty): {fp}"); continue
    added = 0
    for n in nodes:
        if not isinstance(n, dict): continue
        if not node_ok(n): continue
        try: k = norm(n["k"])
        except Exception as e: continue
        if k in merged:
            if len(str(n.get("v",""))) > len(str(merged[k].get("v",""))):
                merged[k] = {f: n.get(f) for f in ("k","v","w","t","source","ref") if n.get(f) is not None}
        else:
            merged[k] = {f: n.get(f) for f in ("k","v","w","t","source","ref") if n.get(f) is not None}
            added += 1
    print(f"  {os.path.basename(fp):40s} +{added:5d}  total {len(merged)}")

# ---- SEC primaries ----
print("\n=== SEC primaries ===")
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
        v = excerpt[:319000]
        merged[k] = {"k":k,"v":v,"w":0.5,"t":"filing","source":"SEC_EDGAR","ref":fl.get("source_url","")}
        prim_added += 1
print(f"  +{prim_added} primary filing nodes (total {len(merged)})")

# ---- DROP FOLDER: brain/ ----
print("\n=== drop/brain/ ===")
drop_brain_added = 0
drop_brain_skipped = 0
for fp in sorted(glob.glob(f"{DROP}/brain/*")):
    if not fp.endswith((".json",".txt")): continue
    try:
        if fp.endswith(".json"):
            d = load(fp)
            nodes = shape_nodes(d)
        else:  # .txt: line-based "key::value" or "key|value"
            nodes = []
            with open(fp,"r",encoding="utf-8",errors="replace") as f:
                for ln in f:
                    ln = ln.rstrip("\n")
                    if not ln or ln.startswith("#"): continue
                    if "::" in ln:
                        k,v = ln.split("::",1)
                    elif "|" in ln:
                        k,v = ln.split("|",1)
                    else: continue
                    k,v = k.strip(), v.strip()
                    if k and v: nodes.append({"k":k,"v":v,"w":0.5,"t":"fact","source":"DROP_BRAIN"})
    except Exception as e:
        print(f"  !! skip {os.path.basename(fp)}: {e}")
        drop_brain_skipped += 1
        continue
    for n in nodes:
        if not node_ok(n): continue
        k = norm(n["k"])
        if k in merged:
            if len(str(n.get("v",""))) > len(str(merged[k].get("v",""))):
                merged[k] = {f: n.get(f) for f in ("k","v","w","t","source","ref") if n.get(f) is not None}
        else:
            merged[k] = {f: n.get(f) for f in ("k","v","w","t","source","ref") if n.get(f) is not None}
            drop_brain_added += 1
    print(f"  +{len([n for n in nodes if node_ok(n)])} from {os.path.basename(fp)}")
print(f"  drop/brain: +{drop_brain_added} new nodes")

# ---- DROP FOLDER: filings/ (added as filing-type nodes) ----
print("\n=== drop/filings/ ===")
drop_filing_added = 0
for fp in sorted(glob.glob(f"{DROP}/filings/*.json")):
    try: d = load(fp)
    except Exception as e: print(f"  !! skip {os.path.basename(fp)}: {e}"); continue
    # accept either {filings:[...]} or list of filings
    filings = d.get("filings", d) if isinstance(d, dict) else d
    for fl in filings:
        excerpt = fl.get("text_excerpt", fl.get("text",""))
        if not excerpt or len(excerpt) < 50: continue
        form = fl.get("form","DROP")
        date = fl.get("filing_date", fl.get("date",""))
        cik = fl.get("cik", fl.get("ticker","DROP"))
        k = f"drop_{cik}_{form}_{date}".lower().replace(" ","_")
        v = excerpt[:319000]
        merged[k] = {"k":k,"v":v,"w":0.5,"t":"filing","source":"DROP_FILING","ref":fl.get("source_url","")}
        drop_filing_added += 1
    print(f"  +{len([f for f in filings if isinstance(f,dict)])} from {os.path.basename(fp)}")
print(f"  drop/filings: +{drop_filing_added} nodes")

# ---- DROP FOLDER: encyclopedia/ (TYPE=encyclopedia) ----
print("\n=== drop/encyclopedia/ ===")
drop_enc_added = 0
for fp in sorted(glob.glob(f"{DROP}/encyclopedia/*")):
    if not fp.endswith((".json",".txt")): continue
    try:
        if fp.endswith(".json"):
            d = load(fp)
            nodes = shape_nodes(d)
        else:
            nodes = []
            with open(fp,"r",encoding="utf-8",errors="replace") as f:
                for ln in f:
                    ln = ln.rstrip("\n")
                    if not ln or ln.startswith("#"): continue
                    if "::" in ln: k,v = ln.split("::",1)
                    elif "|" in ln: k,v = ln.split("|",1)
                    else: continue
                    k,v = k.strip(), v.strip()
                    if k and v: nodes.append({"k":k,"v":v,"w":0.5,"t":"encyclopedia","source":"DROP_ENC"})
    except Exception as e:
        print(f"  !! skip {os.path.basename(fp)}: {e}")
        continue
    for n in nodes:
        if not node_ok(n): continue
        k = norm(n["k"])
        # force encyclopedia type on drop
        n["t"] = "encyclopedia"
        n.setdefault("source","DROP_ENC")
        if k not in merged:
            merged[k] = {f: n.get(f) for f in ("k","v","w","t","source","ref") if n.get(f) is not None}
            drop_enc_added += 1
        elif len(str(n.get("v",""))) > len(str(merged[k].get("v",""))):
            n["t"] = "encyclopedia"
            merged[k] = {f: n.get(f) for f in ("k","v","w","t","source","ref") if n.get(f) is not None}
    print(f"  +{len([n for n in nodes if node_ok(n)])} from {os.path.basename(fp)}")
print(f"  drop/encyclopedia: +{drop_enc_added} new nodes")

brain = list(merged.values())
print(f"\n=== FINAL BRAIN: {len(brain):,} nodes ===")

# ---- load data blocks (canonical) ----
print("\n=== data blocks ===")
kjv = load(f"{BASE}/Projects/TRU/data/kjv_full.json")
xref = load(f"{BASE}/Projects/TRU/data/xref_compact.json")
sidx = load(f"{BASE}/Projects/TRU/data/strongs_verse_index.json")
greek = load(f"{BASE}/Projects/TRU/data/strongs_greek.json")
hebrew = load(f"{BASE}/Projects/TRU/data/strongs_hebrew.json")
lex = load(f"{BASE}/Projects/TRU/data/strongs_lexicon_kaiserlik.json")
kjv_lookup = load(f"{BASE}/TRU/kjv_lookup.json")

# ---- DROP FOLDER: scripture/ (replaces kjv-data if drop is bigger) ----
print("\n=== drop/scripture/ ===")
drop_kjv_used = False
drop_kjv_data = None
for fp in sorted(glob.glob(f"{DROP}/scripture/*.json")):
    try:
        d = load(fp)
        if isinstance(d, list): candidates = d
        else: candidates = d.get("verses", d.get("data", []))
        if candidates and len(candidates) > len(kjv):
            drop_kjv_data = candidates
            drop_kjv_used = True
            print(f"  using {os.path.basename(fp)} ({len(candidates)} > {len(kjv)})")
        else:
            print(f"  {os.path.basename(fp)}: {len(candidates) if isinstance(candidates,list) else 0} (smaller than canonical, skipping)")
    except Exception as e: print(f"  !! skip {os.path.basename(fp)}: {e}")
if drop_kjv_used: kjv = drop_kjv_data

# merge strongs (lexicon primary)
strongs = dict(lex)
for src in (greek, hebrew):
    for k, v in src.items():
        if k not in strongs: strongs[k] = v
        else:
            for f in ("l","t","d","k"):
                if not strongs[k].get(f) and v.get(f): strongs[k][f] = v[f]

# ---- DROP FOLDER: lexicon/ (merges into strongs) ----
print("\n=== drop/lexicon/ ===")
for fp in sorted(glob.glob(f"{DROP}/lexicon/*.json")):
    try:
        d = load(fp)
        if not isinstance(d, dict): print(f"  !! {os.path.basename(fp)}: not a dict"); continue
        added = 0
        for k, v in d.items():
            if k not in strongs:
                strongs[k] = v
                added += 1
            else:
                for f in ("l","t","d","k","g","h"):
                    if isinstance(v,dict) and not strongs[k].get(f) and v.get(f):
                        strongs[k][f] = v[f]
        print(f"  +{added} from {os.path.basename(fp)} ({len(d)} total)")
    except Exception as e: print(f"  !! skip {os.path.basename(fp)}: {e}")

print(f"  kjv={len(kjv)} xref={len(xref)} sidx={len(sidx)} strongs={len(strongs)} kjv_lookup={len(kjv_lookup)}")

# ---- load + patch shell ----
print("\n=== shell ===")
with open(SRC_HTML, "r", encoding="utf-8", errors="replace") as f: html = f.read()
print(f"  source: {len(html)/1048576:.2f} MB")

# ---- replace data blocks ----
def replace_block(html, tag, content):
    pat = r'(<script type="application/json" id="' + re.escape(tag) + r'">)(.*?)(</script>)'
    m = re.search(pat, html, re.DOTALL)
    if not m: print(f"  !! {tag} not found"); return html
    old = len(m.group(2))
    html = html[:m.start(1)] + m.group(1) + content + m.group(3) + html[m.end(3):]
    print(f"  {tag}: {old/1048576:6.2f} MB -> {len(content)/1048576:6.2f} MB")
    return html

print("\n=== embedding ===")
html = replace_block(html, "brain-data", compact(brain))
html = replace_block(html, "kjv-data", compact([{k: v[k] for k in ("ref","text")} for v in kjv]))
html = replace_block(html, "strongs-data", compact(strongs))
html = replace_block(html, "xref-data", compact(xref))
html = replace_block(html, "strongs-idx", compact(sidx))

lookup_block = f'<script type="application/json" id="kjv-lookup">{compact(kjv_lookup)}</script>'
if "<script type=\"application/json\" id=\"kjv-lookup\">" not in html:
    html = html.replace("</head>", lookup_block + "\n</head>", 1)
    print(f"  kjv-lookup: +{len(compact(kjv_lookup))/1048576:.2f} MB (new block)")
else:
    html = replace_block(html, "kjv-lookup", compact(kjv_lookup))

html = re.sub(r'const KJV_COUNT=\d+;', f'const KJV_COUNT={len(kjv)};', html)
html = re.sub(r'const BRAIN_COUNT=\d+;', f'const BRAIN_COUNT={len(brain)};', html)

# ---- strip webgpu ----
print("\n=== strip webgpu ===")
strips = []
s = html.find("// ====================================\n// TRU WEBLLM LAYER")
e = html.find("// ── hybrid live LLM layer")
if s != -1 and e != -1: strips.append((html[s:e], ""))
s = html.find("// ── escalation layer 1")
e = html.find("// ── escalation layer 2")
if s != -1 and e != -1: strips.append((html[s:e], ""))
strips.append(('const _wg=webLLMCheck();statusEl.textContent="● ONLINE • LOGOS READY • OFFLINE"+(_wg?" • WebGPU":"");',
               'statusEl.textContent="● ONLINE • LOGOS READY • OFFLINE";'))
strips.append(('if(low==="webllm"||low==="model"||low==="llm") return cmdWebLLM(q);', ''))
for old, new in strips:
    if old in html: html = html.replace(old, new, 1)
for sym in ("TRU_WEBLLM","webLLMCheck","cmdWebLLM","_wg","navigator.gpu"):
    if sym in html: print(f"  !! dangling: {sym}")

# ---- write ----
print("\n=== write ===")
with open(OUT_HTML, "w", encoding="utf-8") as f: f.write(html)
sz = os.path.getsize(OUT_HTML)
print(f"DONE: {OUT_HTML}")
print(f"size: {sz/1048576:.2f} MB  (target 100 MB, delta {(sz/1048576)-100:+.2f} MB)")