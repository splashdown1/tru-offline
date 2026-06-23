#!/usr/bin/env python3
"""Build TRU_24_5.html — LOGOS engine shell + upgraded data blocks, target ~24.5MB."""
import json, re, sys, os

BASE = "/home/workspace/Projects/TRU"
SRC_HTML = f"{BASE}/versions/TRU_LOGOS.html"
OUT_HTML = "/home/workspace/TRU_24_5.html"

def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def compact(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

# ---- load fresh data ----
print("loading fresh data...")
kjv = load_json(f"{BASE}/data/kjv_full.json")
xref = load_json(f"{BASE}/data/xref_compact.json")
sidx = load_json(f"{BASE}/data/strongs_verse_index_compact.json")
greek = load_json(f"{BASE}/data/strongs_greek.json")
hebrew = load_json(f"{BASE}/data/strongs_hebrew.json")
lex = load_json(f"{BASE}/data/strongs_lexicon_kaiserlik.json")

print(f"  kjv={len(kjv)} xref={len(xref)} sidx={len(sidx)} greek={len(greek)} hebrew={len(hebrew)} lex={len(lex)}")

# ---- merge strong's: lexicon PRIMARY (richest: has p,u + full defs), greek/hebrew fill gaps ----
print("merging strong's (lexicon-primary)...")
strongs = {}
strongs.update(lex)  # primary: {l,t,d,k,p,u}
for src in (greek, hebrew):
    for k, v in src.items():
        if k not in strongs:
            strongs[k] = v
        else:
            for f in ("l", "t", "d", "k"):
                if not strongs[k].get(f) and v.get(f):
                    strongs[k][f] = v[f]
print(f"  merged strongs={len(strongs)}")

# ---- load LOGOS html ----
print("loading LOGOS shell...")
with open(SRC_HTML, "r", encoding="utf-8", errors="replace") as f:
    html = f.read()
print(f"  source: {len(html):,} bytes ({len(html)/1048576:.2f} MB)")

# ---- replace data blocks (keep brain-data intact) ----
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
html, _ = replace_block(html, "kjv-data", compact([{k: v[k] for k in ("ref", "text")} for v in kjv]))
html, _ = replace_block(html, "strongs-data", compact(strongs))
# keep LOGOS original xref-data + strongs-idx (complete proven data; closes size gap to ~24.4MB)
# html, _ = replace_block(html, "xref-data", compact(xref))
# html, _ = replace_block(html, "strongs-idx", compact(sidx))

# ---- brain: load deduped canonical brain.json, compact to [{k,v}], replace block ----
print("loading deduped brain...")
brain_full = load_json(f"{BASE}/current/brain.json")
brain_nodes = brain_full.get("nodes", brain_full) if isinstance(brain_full, dict) else brain_full
brain_compact = compact([{"k": n["k"], "v": n["v"]} for n in brain_nodes])
html, _ = replace_block(html, "brain-data", brain_compact)
print(f"  brain nodes embedded: {len(brain_nodes)}")

# ---- update KJV_COUNT if present ----
html = re.sub(r'const KJV_COUNT=\d+;', f'const KJV_COUNT={len(kjv)};', html)

# ---- update BRAIN_COUNT if present ----
html = re.sub(r'const BRAIN_COUNT=\d+;', f'const BRAIN_COUNT={len(brain_nodes)};', html)

# ---- strip WebGPU/WebLLM (non-functional layer; user request to remove) ----
print("stripping WebGPU/WebLLM layer...")
strips = []

# A. route dispatch line (neutralize cmdWebLLM route)
strips.append(('  if(low==="webllm"||low==="model"||low==="llm") return cmdWebLLM(q);\n', ""))

# B. WebLLM layer header + code block (up to escalation layer 1)
_b_start = html.find("// ====================================\n// TRU WEBLLM LAYER")
_b_end = html.find("// ── hybrid live LLM layer")
assert _b_start != -1 and _b_end != -1 and _b_start < _b_end, "webllm layer bounds not found"
strips.append((html[_b_start:_b_end], ""))

# C. escalation layer 1 block (up to escalation layer 2)
_c_start = html.find("// ── escalation layer 1")
_c_end = html.find("// ── escalation layer 2")
assert _c_start != -1 and _c_end != -1 and _c_start < _c_end, "esc layer1 bounds not found"
strips.append((html[_c_start:_c_end], ""))

# D. boot _wg line (remove webLLMCheck call + WebGPU badge)
strips.append(('const _wg=webLLMCheck();statusEl.textContent="● ONLINE • LOGOS READY • OFFLINE"+(_wg?" • WebGPU":"");',
               'statusEl.textContent="● ONLINE • LOGOS READY • OFFLINE";'))

for old, new in strips:
    assert old in html, f"strip target not found: {old[:70]!r}"
    html = html.replace(old, new, 1)

# verify no dangling code refs (brain content may mention "WebGPU" as a concept — that's fine)
for sym in ("TRU_WEBLLM", "webLLMCheck", "cmdWebLLM", "_wg", "navigator.gpu"):
    assert sym not in html, f"dangling ref remains: {sym}"
print("  webgpu fully removed, no dangling refs")

# ---- patch doctrineLookup: catch "why is there X" / "why is X" → exact-match concept node ----
_old_re = r"|explain\s+)(.+?)[?\s]*$/i"
_new_re = r"|explain\s+|why\s+(?:is\s+there\s+|are\s+there\s+|is\s+|are\s+|does\s+|do\s+))(.+?)[?\s]*$/i"
assert _old_re in html, "doctrineLookup regex not found"
html = html.replace(_old_re, _new_re, 1)
print("  doctrineLookup extended for 'why' questions")

# ---- write ----
print("writing output...")
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)
sz = os.path.getsize(OUT_HTML)
print(f"\nDONE: {OUT_HTML}")
print(f"size: {sz:,} bytes = {sz/1048576:.2f} MB")
print(f"target 24.5 MB, delta: {(sz/1048576)-24.5:+.2f} MB")
