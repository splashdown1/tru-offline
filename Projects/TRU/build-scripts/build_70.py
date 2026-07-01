#!/usr/bin/env python3
"""Build TRU_70.html — glossary/index-first modular build.

Doctrine:
- source is canonical data
- sustainment is a single deterministic build pass
- expression is the rendered html layer
- boundary condition: if harm > 0, then U = 0
- formula: if hesiticat > 0, then u = 0

This build keeps the shell stable, injects all data in one pass, and owns css
and layout inside the generator instead of patching the output after the fact.
"""
import json, re, os, glob, sys, base64, gzip
from pathlib import Path

BASE = "/home/workspace"
DROP = f"{BASE}/Projects/TRU/drop"
SRC_HTML = f"{BASE}/Projects/TRU/versions/TRU_LOGOS.html"
OUT_HTML = f"{BASE}/TRU_INFINITE_PLUS.html"


def load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def compact(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def norm(s):
    return s.strip().lower().replace(" ", "_") if isinstance(s, str) else str(s)


def node_ok(n):
    return isinstance(n, dict) and "k" in n and "v" in n


def shape_nodes(d):
    if isinstance(d, list):
        return [n for n in d if isinstance(n, dict)]
    if isinstance(d, dict):
        if "nodes" in d and isinstance(d["nodes"], list):
            return [n for n in d["nodes"] if isinstance(n, dict)]
        if "data" in d and isinstance(d["data"], list):
            return [n for n in d["data"] if isinstance(n, dict)]
        vals = list(d.values())
        if vals and all(isinstance(v, dict) for v in vals):
            return vals
    return []


def add_to_brain(merged, n):
    if not node_ok(n):
        return 0
    k = norm(n["k"])
    nv = str(n.get("v", ""))
    if k in merged:
        if len(nv) > len(str(merged[k].get("v", ""))):
            merged[k] = {f: n.get(f) for f in ("k", "v", "w", "t", "source", "ref") if n.get(f) is not None}
        return 0
    merged[k] = {f: n.get(f) for f in ("k", "v", "w", "t", "source", "ref") if n.get(f) is not None}
    return 1


def sanitize_nodes(nodes):
    ctl = re.compile(r"[\x00-\x1f]")
    out = []
    for n in nodes:
        if isinstance(n, dict) and isinstance(n.get("v"), str):
            n2 = dict(n)
            n2["v"] = ctl.sub(lambda m: " " if m.group(0) == "\t" else "?", n2["v"])
            out.append(n2)
        else:
            out.append(n)
    return out


def gz_b64_bytes(p):
    return base64.b64encode(gzip.compress(Path(p).read_bytes())).decode("ascii")


def build_shell(extra_css, ui_block, brain_json, kjv_shell, strongs_shell, wordnet_shell, glossary_b64, index_b64):
    with open(SRC_HTML, "r", encoding="utf-8") as f:
        src = f.read()

    out = src
    out = out.replace('</style>', extra_css + '\n</style>', 1)
    out = re.sub(
        r'<script type="application/json" id="brain-data">.*?</script>',
        f'<script type="application/json" id="brain-data">{brain_json}</script>',
        out, count=1, flags=re.DOTALL
    )

    if kjv_shell:
        out = re.sub(
            r'<script type="application/json" id="kjv-data">.*?</script>',
            f'<script type="application/json" id="kjv-data">{kjv_shell}</script>',
            out, count=1, flags=re.DOTALL
        )

    if strongs_shell:
        out = re.sub(
            r'<script type="application/json" id="strongs-data">.*?</script>',
            f'<script type="application/json" id="strongs-data">{strongs_shell}</script>',
            out, count=1, flags=re.DOTALL
        )

    if wordnet_shell:
        if '<script type="application/json" id="wordnet-data">' in out:
            out = re.sub(
                r'<script type="application/json" id="wordnet-data">.*?</script>',
                f'<script type="application/json" id="wordnet-data">{wordnet_shell}</script>',
                out, count=1, flags=re.DOTALL
            )
        else:
            out = out.replace('</body>', f'<script type="application/json" id="wordnet-data">{wordnet_shell}</script></body>', 1)

    if glossary_b64 and index_b64:
        out = out.replace(
            '</head>',
            f'<script>window.__GLOSSARY_B64__ = "{glossary_b64}";window.__INDEX_B64__ = "{index_b64}";</script></head>',
            1,
        )

    out = out.replace(
        '<div id="chat"></div>\n<div class="inputbar">\n  <input id="input" placeholder="Speak to me…" autocomplete="off" autocapitalize="sentences">\n  <button id="send" disabled>↑</button>\n</div>',
        ui_block,
        1,
    )
    out = re.sub(r'BRAIN_COUNT=\d+', f'BRAIN_COUNT={len(json.loads(brain_json))}', out)
    out = out.replace("TRU LOGOS", "TRU INFINITE PLUS", 1)
    out = out.replace("offline • sovereign", "offline • sovereign • glossary + index • doctrine • merged", 1)
    return out


print("=== canonical brains (KJV_BIBLE stripped) ===")
BRAIN_SOURCES = [
    f"{BASE}/Projects/TRU/current/brain.json",
    f"{BASE}/repos/tru-archive/TRU_BRAIN_41.json",
    f"{BASE}/repos/tru-omega/brain/core.json",
    f"{BASE}/Projects/TRU/data/tru_brain_1290_nodes.json",
    f"{BASE}/Projects/TRU/data/TRU_MEGA_BRAIN.json",
    f"{BASE}/Projects/TRU/data/TRU_SUPER_BRAIN.json",
    f"{BASE}/Projects/TRU/data/TRU_CORE_KB.json",
    f"{BASE}/Projects/TRU/data/tru-knowledge-bank.json",
    f"{BASE}/Projects/TRU/data/tru_merged_brain.json",
    f"{BASE}/Projects/TRU/data/tru_full_brain.json",
    f"{BASE}/Projects/TRU/data/tru_phase15_brain.json",
]

merged = {}
stripped_kjv = 0
for fp in BRAIN_SOURCES:
    if not os.path.exists(fp):
        print(f"  skip (missing): {fp}")
        continue
    try:
        d = load(fp)
    except Exception as e:
        print(f"  skip (bad json {e}): {fp}")
        continue
    nodes = shape_nodes(d)
    if not nodes:
        print(f"  skip (empty): {fp}")
        continue
    added = 0
    for n in nodes:
        if not node_ok(n):
            continue
        if n.get("source") == "KJV_BIBLE":
            stripped_kjv += 1
            continue
        added += add_to_brain(merged, n)
    print(f"  +{added:6d} (total {len(merged):6d})  {os.path.basename(fp)}")

print(f"stripped {stripped_kjv} redundant KJV_BIBLE nodes from canonical brains")
print(f"brain pool: {len(merged)}")


def ingest_drop_brain():
    added = 0
    files = sorted(glob.glob(f"{DROP}/brain/*.json")) + sorted(glob.glob(f"{DROP}/brain/*.txt"))
    for fp in files:
        try:
            d = load(fp)
        except Exception as e:
            print(f"  skip {os.path.basename(fp)}: {e}")
            continue
        nodes = shape_nodes(d)
        if not nodes:
            print(f"  skip (no nodes): {os.path.basename(fp)}")
            continue
        f_added = 0
        for n in nodes:
            f_added += add_to_brain(merged, n)
        added += f_added
        print(f"  +{f_added} new from {os.path.basename(fp)}")
    return added


def ingest_drop_encyclopedia():
    added = 0
    for fp in sorted(glob.glob(f"{DROP}/encyclopedia/*")):
        bn = os.path.basename(fp).lower()
        if "wordnet" in bn:
            continue
        if not fp.endswith((".json", ".txt")):
            continue
        try:
            d = load(fp)
        except Exception as e:
            print(f"  skip {bn}: {e}")
            continue
        nodes = shape_nodes(d)
        if not nodes:
            if isinstance(d, dict):
                for w, v in d.items():
                    k = f"enc_{norm(w)}"
                    if k not in merged:
                        merged[k] = {"k": k, "v": str(v)[:30000], "w": 0.4, "t": "encyclopedia", "source": "DROP_ENC"}
                        added += 1
            continue
        for n in nodes:
            added += add_to_brain(merged, {**n, "t": "encyclopedia", "source": "DROP_ENC"} if node_ok(n) else {})
    return added


def ingest_drop_filings():
    added = 0
    for fp in sorted(glob.glob(f"{DROP}/filings/*.json")):
        try:
            d = load(fp)
        except Exception as e:
            print(f"  skip {os.path.basename(fp)}: {e}")
            continue
        filings = d.get("filings", d) if isinstance(d, dict) else d
        for fl in filings:
            if not isinstance(fl, dict):
                continue
            excerpt = fl.get("text_excerpt", fl.get("text", ""))
            if not excerpt or len(excerpt) < 50:
                continue
            form = fl.get("form", "DROP")
            date = fl.get("filing_date", fl.get("date", ""))
            cik = fl.get("cik", fl.get("ticker", "DROP"))
            k = f"drop_{cik}_{form}_{date}".lower().replace(" ", "_")
            v = excerpt[:319000]
            if k not in merged:
                merged[k] = {"k": k, "v": v, "w": 0.5, "t": "filing", "source": "DROP_FILING", "ref": fl.get("source_url", "")}
                added += 1
    return added


def ingest_drop_scripture():
    added = 0
    kjv_block = ""
    for fp in sorted(glob.glob(f"{DROP}/scripture/*.json")):
        try:
            d = load(fp)
        except Exception as e:
            print(f"  scripture skip {os.path.basename(fp)}: {e}")
            continue
        cand = compact(d)
        if len(cand) > len(kjv_block):
            kjv_block = cand
            print(f"  kjv-data replaced by {os.path.basename(fp)} ({len(cand)/1024:.0f} KB)")
        items = d if isinstance(d, list) else (d.get("verses", d.get("data", [])) if isinstance(d, dict) else [])
        f_added = 0
        for v in items:
            if not isinstance(v, dict):
                continue
            ref = v.get("ref", v.get("k", ""))
            text = v.get("text", v.get("v", ""))
            if not ref or not text:
                continue
            k = "drop_" + norm(ref).replace(":", "_")
            if k not in merged:
                merged[k] = {"k": k, "v": str(text)[:30000], "w": 0.5, "t": "scripture", "source": "DROP_SCRIPTURE"}
                f_added += 1
        added += f_added
        print(f"  +{f_added} scripture nodes from {os.path.basename(fp)}")
    return added, kjv_block


def ingest_drop_lexicon():
    added = 0
    strongs_block = ""
    for fp in sorted(glob.glob(f"{DROP}/lexicon/*.json")):
        try:
            d = load(fp)
        except Exception as e:
            print(f"  lexicon skip {os.path.basename(fp)}: {e}")
            continue
        cand = compact(d)
        if len(cand) > len(strongs_block):
            strongs_block = cand
            print(f"  strongs-data replaced by {os.path.basename(fp)} ({len(cand)/1024:.0f} KB)")
        f_added = 0
        if isinstance(d, dict):
            for k, v in d.items():
                if not isinstance(v, (dict, str)):
                    continue
                kk = "lex_" + norm(k)
                if kk in merged:
                    continue
                if isinstance(v, dict):
                    text = v.get("def") or v.get("d") or v.get("gloss") or v.get("meaning") or str(v)
                else:
                    text = v
                if not text:
                    continue
                merged[kk] = {"k": kk, "v": str(text)[:30000], "w": 0.5, "t": "lexicon", "source": "DROP_LEXICON"}
                f_added += 1
        added += f_added
        print(f"  +{f_added} lexicon nodes from {os.path.basename(fp)}")
    return added, strongs_block


print("\n=== drop/brain/ ===")
print(f"  +{ingest_drop_brain()} new brain nodes")

print("\n=== drop/encyclopedia/ (non-wordnet) ===")
print(f"  +{ingest_drop_encyclopedia()} encyclopedia nodes")

print("\n=== drop/filings/ ===")
print(f"  +{ingest_drop_filings()} filing nodes")

print("\n=== drop/scripture/ ===")
scripture_added, kjv_block = ingest_drop_scripture()
print(f"  +{scripture_added} scripture nodes")

print("\n=== drop/lexicon/ ===")
lexicon_added, strongs_block = ingest_drop_lexicon()
print(f"  +{lexicon_added} lexicon nodes")

print(f"\nfinal brain pool: {len(merged)} nodes")

print("\n=== wordnet block ===")
wn_data = None
wn_fp = f"{DROP}/encyclopedia/wordnet.json"
if os.path.exists(wn_fp):
    try:
        wn_data = load(wn_fp)
        print(f"  loaded wordnet.json: {len(wn_data)} entries")
    except Exception as e:
        print(f"  wordnet load failed: {e}")

print("\n=== build library blocks ===")
glossary_b64 = ""
index_b64 = ""
glossary_json = f"{BASE}/Projects/TRU/omega/data/glossary.json"
index_json = f"{BASE}/Projects/TRU/omega/data/index.json"
if os.path.exists(glossary_json):
    glossary_b64 = gz_b64_bytes(glossary_json)
    print(f"  glossary.json -> {len(glossary_b64)/1024/1024:.1f} MB b64")
if os.path.exists(index_json):
    index_b64 = gz_b64_bytes(index_json)
    print(f"  index.json -> {len(index_b64)/1024/1024:.1f} MB b64")

extra_css = '''
.tabs {
  display: flex;
  gap: 0;
  border-bottom: 1px solid rgba(0,229,255,.18);
  flex-shrink: 0;
}
.tab {
  background: transparent;
  color: rgba(0,229,255,.45);
  border: 0;
  border-bottom: 2px solid transparent;
  padding: 8px 14px;
  font-size: 11px;
  font-family: monospace;
  letter-spacing: 1px;
  cursor: pointer;
}
.tab:hover { color: #e6f7ff; }
.tab.on {
  color: #00e5ff;
  border-bottom-color: #00e5ff;
}
.doctrine {
  color: rgba(0,229,255,.38);
  font-size: 9px;
  letter-spacing: 1px;
  margin-top: 4px;
  line-height: 1.3;
}
.view {
  display: none;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}
.view.on {
  display: flex;
  flex-direction: column;
}
#view-chat { min-height: 0; }
#view-chat #chat { flex: 1; min-height: 0; }
#view-chat .inputbar { flex-shrink: 0; }
#view-glossary, #view-index {
  padding: 12px 14px 8px;
  gap: 10px;
}
.lib-head {
  flex-shrink: 0;
}
.lib-meta {
  color: rgba(0,229,255,.5);
  font-size: 10px;
  font-family: monospace;
  margin-bottom: 6px;
}
.lib-alpha {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 8px;
}
.lib-alpha button,
.lib-head input,
.idx-bucket,
.idx-back,
.gloss-entry,
.idx-browse {
  font-family: inherit;
}
.lib-head input {
  width: 100%;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid rgba(0,229,255,.25);
  background: rgba(0,20,30,.8);
  color: #fff;
  outline: none;
}
.lib-head input:focus { border-color: #00e5ff; box-shadow: 0 0 12px rgba(0,229,255,.15); }
.lib-results, #idxTop, #idxBrowse { overflow-y: auto; min-height: 0; }
.gloss-entry,
.idx-browse,
.idx-node {
  background: rgba(0,229,255,.05);
  border: 1px solid rgba(0,229,255,.12);
  border-radius: 12px;
  margin-bottom: 8px;
  padding: 10px 12px;
}
.gloss-entry .k,
.idx-browse .k,
.idx-node .k { color: #00e5ff; }
.gloss-entry .v,
.idx-browse .v,
.idx-node .v { color: #d9f8ff; line-height: 1.45; word-break: break-word; }
.gloss-entry .meta,
.gloss-meta,
.idx-meta,
.idx-node .meta { color: rgba(0,229,255,.45); font-size: 10px; font-family: monospace; }
.idx-axis h3 { color: #00e5ff; }
.idx-bucket,
.idx-back,
.gloss-alpha .abtn {
  background: rgba(0,229,255,.06);
  border: 1px solid rgba(0,229,255,.18);
  color: #d9f8ff;
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 10px;
  cursor: pointer;
}
.idx-bucket:hover,
.idx-back:hover,
.gloss-alpha .abtn:hover { border-color: #00e5ff; color: #00e5ff; }
'''

ui_block = '''
<div class="tabs">
  <button class="tab on" data-view="chat">CHAT</button>
  <button class="tab" data-view="glossary">GLOSSARY</button>
  <button class="tab" data-view="index">INDEX</button>
</div>
<div class="view on" id="view-chat">
  <div id="chat"></div>
  <div class="inputbar">
    <input id="input" placeholder="Speak to me…" autocomplete="off" autocapitalize="sentences">
    <button id="send" disabled>↑</button>
  </div>
</div>
<div class="view" id="view-glossary">
  <div class="lib-head">
    <input id="glossQ" placeholder="search glossary...">
    <div class="lib-meta" id="glossMeta">loading...</div>
    <div class="lib-alpha" id="glossAlpha"></div>
  </div>
  <div class="lib-results" id="glossResults"></div>
</div>
<div class="view" id="view-index">
  <div class="lib-head">
    <div class="lib-meta" id="idxMeta">loading...</div>
    <div class="doctrine">if hesiticat > 0, then u = 0</div>
  </div>
  <div id="idxTop"></div>
  <div id="idxBrowse"></div>
</div>
'''


def read_block(html, sid):
    m = re.search(rf'<script type="application/json" id="{sid}">(.*?)</script>', html, re.DOTALL)
    return m.group(1) if m else None

with open(SRC_HTML, "r", encoding="utf-8") as f:
    src = f.read()

kjv_shell = read_block(src, "kjv-data") or ""
strongs_shell = read_block(src, "strongs-data") or ""
wordnet_shell = read_block(src, "wordnet-data") or ""
if kjv_block:
    kjv_shell = kjv_block
if strongs_block:
    strongs_shell = strongs_block
if wn_data:
    wordnet_shell = compact(wn_data)

sanitized = sanitize_nodes(list(merged.values()))
merged = {norm(n["k"]): n for n in sanitized if node_ok(n)}
print(f"post-sanitize brain pool: {len(merged)} nodes")

brain_arr = list(merged.values())
brain_json = compact(brain_arr)
print(f"final brain pool: {len(brain_arr)} nodes")

out = build_shell(extra_css, ui_block, brain_json, kjv_shell, strongs_shell, wordnet_shell, glossary_b64, index_b64)

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(out)

sz = os.path.getsize(OUT_HTML)
print(f"\n=== DONE: {OUT_HTML} ===")
print(f"size: {sz/1048576:.2f} MB")
print(f"brain nodes: {len(brain_arr)}")
print("no mb cap enforced")
