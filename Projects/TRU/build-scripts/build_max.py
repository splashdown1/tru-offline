#!/usr/bin/env python3
"""Build TRU_MAX.html — honest max: 7 merged brains + full KJV + full strongs index + lexicon + xref."""
import json, re, os

BASE = "/home/workspace/Projects/TRU"
SRC_HTML = f"{BASE}/versions/TRU_LOGOS.html"
OUT_HTML = "/home/workspace/TRU_MAX.html"

def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def compact(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

def get_nodes(b):
    """Normalize any brain shape to a list of node dicts."""
    if isinstance(b, dict):
        return b.get("nodes", [])
    if isinstance(b, list):
        return b
    return []

# ---- merge all brains: dedupe by key, richest v wins ----
print("merging brains...")
brain_paths = [
    "repos/tru-omega/brain/core.json",
    "repos/tru-archive/TRU_BRAIN_41.json",
    "repos/tru-archive/TRU_brain.json",
    "Projects/TRU/data/brain_canonical.json",
    "Projects/TRU/data/TRU_MEGA_BRAIN.json",
    "Projects/TRU/current/brain.json",
    "Projects/TRU/phase28/brain.json",
]
merged = {}
total_in = 0
for rp in brain_paths:
    p = f"/home/workspace/{rp}"
    if not os.path.exists(p):
        print(f"  skip (missing): {rp}")
        continue
    try:
        b = load_json(p)
        nodes = get_nodes(b)
        total_in += len(nodes)
        for n in nodes:
            k = n.get("k")
            if not k:
                continue
            v = n.get("v", "")
            if k not in merged or len(v) > len(merged[k].get("v", "")):
                merged[k] = n
    except Exception as e:
        print(f"  skip (error {e}): {rp}")

brain = list(merged.values())
print(f"  total in: {total_in}, unique keys: {len(brain)}")

# ---- load data ----
print("loading data...")
kjv = load_json(f"{BASE}/data/kjv_full.json")
xref = load_json(f"{BASE}/data/xref_compact.json")
sidx = load_json(f"{BASE}/data/strongs_verse_index.json")  # FULL, not compact
greek = load_json(f"{BASE}/data/strongs_greek.json")
hebrew = load_json(f"{BASE}/data/strongs_hebrew.json")
lex = load_json(f"{BASE}/data/strongs_lexicon_kaiserlik.json")
print(f"  kjv={len(kjv)} xref={len(xref)} sidx={len(sidx)} greek={len(greek)} hebrew={len(hebrew)} lex={len(lex)}")

# ---- merge strong's: lexicon primary ----
print("merging strong's...")
strongs = {}
strongs.update(lex)
for src in (greek, hebrew):
    for k, v in src.items():
        if k not in strongs:
            strongs[k] = v
        else:
            for f in ("l", "t", "d", "k"):
                if not strongs[k].get(f) and v.get(f):
                    strongs[k][f] = v[f]
print(f"  merged strongs={len(strongs)}")

# ---- load LOGOS shell ----
print("loading shell...")
with open(SRC_HTML, "r", encoding="utf-8", errors="replace") as f:
    html = f.read()
print(f"  source: {len(html):,} bytes ({len(html)/1048576:.2f} MB)")

# ---- replace blocks ----
def replace_block(html, tag, new_content):
    pattern = r'(<script type="application/json" id="' + re.escape(tag) + r'">)(.*?)(</script>)'
    m = re.search(pattern, html, re.DOTALL)
    if not m:
        print(f"  !! block {tag} not found"); return html, False
    old_len = len(m.group(2))
    html = html[:m.start(1)] + m.group(1) + new_content + m.group(3) + html[m.end(3):]
    print(f"  {tag}: {old_len:,} -> {len(new_content):,} bytes")
    return html, True

print("replacing blocks...")
html, _ = replace_block(html, "kjv-data", compact(kjv))
html, _ = replace_block(html, "strongs-data", compact(strongs))
html, _ = replace_block(html, "xref-data", compact(xref))
html, _ = replace_block(html, "strongs-idx", compact(sidx))
html, _ = replace_block(html, "brain-data", compact([{k: n[k] for k in ("k", "v")} for n in brain]))

# ---- update counts ----
html = re.sub(r'const KJV_COUNT=\d+;', f'const KJV_COUNT={len(kjv)};', html)
html = re.sub(r'const BRAIN_COUNT=\d+;', f'const BRAIN_COUNT={len(brain)};', html)
html = re.sub(r'\d+(?= nodes \+ )', str(len(brain)), html)

# ---- strip WebGPU/WebLLM ----
print("stripping webgpu...")
_b_start = html.find("// ====================================\n// TRU WEBLLM LAYER")
_b_end = html.find("// ── hybrid live LLM layer")
assert _b_start != -1 and _b_end != -1 and _b_start < _b_end, "webllm layer bounds not found"
html = html[:_b_start] + html[_b_end:]

# escalation layer 1 block
_c_start = html.find("// ── escalation layer 1")
_c_end = html.find("// ── escalation layer 2")
assert _c_start != -1 and _c_end != -1 and _c_start < _c_end, "esc layer1 bounds not found"
html = html[:_c_start] + html[_c_end:]

# route dispatch line
_rt = 'if(low==="webllm"||low==="model"||low==="llm") return cmdWebLLM(q);'
if _rt in html:
    html = html.replace(_rt, "", 1)

# neuter cmdWebLLM function to dead-code no-op (can't safely strip whole fn boundary)
html = html.replace("function cmdWebLLM(body){", "function cmdWebLLM_DEAD(body){")

# boot _wg line
old_boot = 'const _wg=webLLMCheck();statusEl.textContent="● ONLINE • LOGOS READY • OFFLINE"+(_wg?" • WebGPU":"");'
assert old_boot in html, "boot _wg line not found"
html = html.replace(old_boot, 'statusEl.textContent="● ONLINE • LOGOS READY • OFFLINE";')

# dangling ref check
for sym in ("TRU_WEBLLM", "webLLMCheck", "_wg", "navigator.gpu"):
    assert sym not in html, f"dangling ref remains: {sym}"
print("  webgpu removed, no dangling refs")

# ---- why-question regex patch (route "why is there X" to brain) ----
old_dl = "if(/^\\s*(what|who|where|when|which|define|explain)\\s+/i.test(q))"
if old_dl in html:
    new_dl = "if(/^\\s*(what|who|where|when|which|define|explain|why)\\s+/i.test(q))"
    html = html.replace(old_dl, new_dl, 1)
    print("  why-regex patched")
else:
    print("  !! why-regex anchor not found")

# ---- write ----
print("writing...")
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)
sz = os.path.getsize(OUT_HTML)
print(f"\nDONE: {OUT_HTML}")
print(f"size: {sz:,} bytes = {sz/1048576:.2f} MB")
