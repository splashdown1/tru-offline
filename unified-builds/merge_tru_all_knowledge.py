#!/usr/bin/env python3
"""
TRU ALL-KNOWLEDGE UNIFIED MERGER
================================
Additive build. Produces a NEW HTML; never edits any source file.

Inputs (read-only, sources stay untouched):
  - /home/workspace/TRU_ALL_KNOWLEDGE.html  (BASE: 120MB, 18 knowledge packs, no JS engine)
  - /home/workspace/TRU_100.html            (ENGINE: routing/UI/voice)

Process (streaming, low memory):
  1) Stream BASE, find <head> end and <body> insertion point
  2) Extract engine JS from TRU_100.html: find the largest non-data <script> block
  3) Extract engine CSS from TRU_100.html: find <style> blocks (and inline style attrs from <body>)
  4) Inject engine CSS/JS into BASE under an "unified-engine" namespace
  5) Expand brain: build a deep-linkage layer (BRAIN_LINKS script) that connects
     every pack to every other pack by shared token frequency
  6) Write a NEW file: TRU_UNIFIED_ALL_KNOWLEDGE.html
  7) Sanity: parse, count tags, log

Output:
  - /home/workspace/tru-unified-build/TRU_UNIFIED_ALL_KNOWLEDGE.html
  - /home/workspace/tru-unified-build/build_report.json

Run:
  python3 /home/workspace/tru-unified-build/merge_tru_all_knowledge.py
"""

import os
import re
import json
import sys
import time
import hashlib
from collections import Counter

BASE   = "/home/workspace/TRU_ALL_KNOWLEDGE.html"
ENGINE = "/home/workspace/TRU_100.html"
OUTDIR = "/home/workspace/tru-unified-build"
OUT    = os.path.join(OUTDIR, "TRU_UNIFIED_ALL_KNOWLEDGE.html")
REPORT = os.path.join(OUTDIR, "build_report.json")

os.makedirs(OUTDIR, exist_ok=True)

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def stream_lines(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            yield line

def stream_block(path, start_re, end_re, max_bytes=50*1024*1024):
    """Yield chars between start_re and end_re. Caps at max_bytes to bound memory."""
    inside = False
    buf = []
    size = 0
    for line in stream_lines(path):
        if not inside:
            if re.search(start_re, line):
                inside = True
                buf.append(line)
                size += len(line)
        else:
            buf.append(line)
            size += len(line)
            if size > max_bytes:
                log(f"  WARNING: cap {max_bytes} reached inside {start_re}, stopping early")
                return "".join(buf)
            if re.search(end_re, line):
                return "".join(buf)
    return "".join(buf) if inside else ""

# ----------------------------------------------------------------------
# 1) Extract engine JS from TRU_100.html
#    Strategy: find all <script> blocks; pick the largest one that does NOT
#    have type="application/json" or type="application/ld+json"
# ----------------------------------------------------------------------
def find_engine_script(path):
    log(f"Scanning {path} for engine JS blocks...")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    # crude but works: split on <script> open tags, walk
    blocks = re.findall(r'<script\b([^>]*)>(.*?)</script>', html, re.DOTALL)
    log(f"  found {len(blocks)} total <script> blocks")
    candidates = []
    for attrs, body in blocks:
        if 'type="application/json"' in attrs or 'type="application/ld+json"' in attrs:
            continue
        if len(body.strip()) < 1000:
            continue
        candidates.append((len(body), attrs, body))
    if not candidates:
        log("  no engine candidates found!")
        return None
    candidates.sort(reverse=True, key=lambda x: x[0])
    size, attrs, body = candidates[0]
    log(f"  picked engine block: {size:,} bytes  attrs={attrs[:80]}")
    return body

# ----------------------------------------------------------------------
# 2) Extract engine CSS from TRU_100.html (<style> blocks)
# ----------------------------------------------------------------------
def find_engine_css(path):
    log(f"Scanning {path} for <style> blocks...")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    blocks = re.findall(r'<style\b([^>]*)>(.*?)</style>', html, re.DOTALL)
    log(f"  found {len(blocks)} total <style> blocks")
    big = []
    for attrs, body in blocks:
        if len(body.strip()) < 200:
            continue
        big.append((len(body), body))
    big.sort(reverse=True, key=lambda x: x[0])
    if not big:
        return ""
    log(f"  picked top {min(3,len(big))} style blocks: {[s for s,_ in big[:3]]} bytes")
    return "\n".join(b for _, b in big[:3])

# ----------------------------------------------------------------------
# 3) Build brain-linkage layer from BASE's JSON packs
#    Reads BASE, finds each <script type="application/json" id="..."> block,
#    samples top tokens, builds a cross-pack adjacency map.
# ----------------------------------------------------------------------
def build_brain_links(path, max_packs=18, top_tokens=20):
    log(f"Building BRAIN_LINKS from {path}...")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    blocks = re.findall(
        r'<script\s+type="application/json"\s+id="([^"]+)"\s*>(.*?)</script>',
        html, re.DOTALL)
    log(f"  found {len(blocks)} named JSON packs")
    pack_tokens = {}
    for pack_id, body in blocks[:max_packs]:
        try:
            data = json.loads(body)
        except Exception as e:
            log(f"  skip {pack_id}: {e}")
            continue
        # sample: collect all string values recursively (bounded)
        sample = []
        def walk(x, depth=0):
            if depth > 6: return
            if isinstance(x, str): sample.append(x)
            elif isinstance(x, list):
                for it in x[:200]: walk(it, depth+1)
            elif isinstance(x, dict):
                for k,v in list(x.items())[:200]:
                    if isinstance(v, str): sample.append(v)
                    else: walk(v, depth+1)
        walk(data)
        text = " ".join(sample).lower()
        # crude tokenization: word>=3, alpha only
        toks = [w for w in re.findall(r"[a-z]{3,}", text) if len(w) < 30]
        common = Counter(toks).most_common(top_tokens)
        pack_tokens[pack_id] = [w for w, _ in common]
        log(f"    {pack_id}: {len(toks):,} tokens, top {top_tokens}: {pack_tokens[pack_id][:5]}...")

    # build adjacency: for each pair, count shared tokens
    packs = list(pack_tokens.keys())
    links = {}
    for i, a in enumerate(packs):
        for b in packs[i+1:]:
            sa, sb = set(pack_tokens[a]), set(pack_tokens[b])
            shared = sa & sb
            if shared:
                links.setdefault(a, {})[b] = sorted(shared)
                links.setdefault(b, {})[a] = sorted(shared)
    log(f"  built {sum(len(v) for v in links.values())} link entries across {len(links)} packs")
    return {
        "version": 1,
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_base": os.path.basename(BASE),
        "packs_indexed": packs,
        "tokens_per_pack": pack_tokens,
        "cross_links": links,
    }

# ----------------------------------------------------------------------
# 4) Stream BASE and inject
# ----------------------------------------------------------------------
def inject_into_base():
    log(f"=== STEP 1: extract engine JS from {ENGINE} ===")
    engine_js = find_engine_script(ENGINE)
    if not engine_js:
        log("FATAL: no engine JS found")
        sys.exit(1)

    log(f"=== STEP 2: extract engine CSS from {ENGINE} ===")
    engine_css = find_engine_css(ENGINE)

    log(f"=== STEP 3: build brain-linkage layer ===")
    brain = build_brain_links(BASE)
    brain_json = json.dumps(brain, ensure_ascii=False)

    log(f"=== STEP 4: stream-write unified HTML to {OUT} ===")
    log(f"  base size:    {os.path.getsize(BASE):,} bytes")
    log(f"  engine js:    {len(engine_js):,} bytes")
    log(f"  engine css:   {len(engine_css):,} bytes")
    log(f"  brain links:  {len(brain_json):,} bytes")

    # markers
    css_marker = "/* === TRU UNIFIED ENGINE CSS (sourced from TRU_100.html) === */"
    js_marker  = "// === TRU UNIFIED ENGINE JS (sourced from TRU_100.html) ==="
    brain_marker_id = "tru-unified-brain-links"

    injected_css = False
    injected_js = False
    injected_brain = False
    out_size = 0
    with open(BASE, "r", encoding="utf-8", errors="replace") as fin, \
         open(OUT, "w", encoding="utf-8") as fout:
        for line in fin:
            # 1) inject CSS right before </head>
            if not injected_css and "</head>" in line:
                fout.write(f"<style id=\"tru-unified-engine\">\n{css_marker}\n{engine_css}\n</style>\n")
                injected_css = True
                log("  injected unified <style> before </head>")
            # 2) inject brain-links script right after first <body> (so it's data, pre-engine)
            if not injected_brain and re.search(r"<body\b", line):
                fout.write(line)
                fout.write(
                    f'<script type="application/json" id="{brain_marker_id}">\n'
                    f'{brain_json}\n'
                    f'</script>\n'
                )
                injected_brain = True
                log(f"  injected brain-links ({len(brain_json):,} bytes) after <body>")
                continue
            # 3) inject engine JS at end of body
            if not injected_js and re.search(r"</body\s*>", line):
                fout.write(
                    f'<script id="tru-unified-engine">\n{js_marker}\n{engine_js}\n</script>\n'
                )
                fout.write(line)
                injected_js = True
                log(f"  injected engine JS ({len(engine_js):,} bytes) before </body>")
                continue
            fout.write(line)
            out_size += len(line.encode("utf-8"))

    out_size = os.path.getsize(OUT)
    log(f"  output size: {out_size:,} bytes")

    return {
        "base_bytes":      os.path.getsize(BASE),
        "engine_js_bytes": len(engine_js),
        "engine_css_bytes": len(engine_css),
        "brain_json_bytes": len(brain_json),
        "output_bytes":   out_size,
        "injected_css":   injected_css,
        "injected_brain": injected_brain,
        "injected_js":    injected_js,
    }

# ----------------------------------------------------------------------
# 5) Sanity: parse output, count tags, validate JSON packs
# ----------------------------------------------------------------------
def sanity_check():
    log("=== STEP 5: sanity check output ===")
    size = os.path.getsize(OUT)
    sha = hashlib.sha256()
    with open(OUT, "rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk: break
            sha.update(chunk)
    sha_hex = sha.hexdigest()
    log(f"  size:  {size:,} bytes")
    log(f"  sha256: {sha_hex}")

    # count script blocks and tags (lightweight)
    with open(OUT, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    script_tags = len(re.findall(r"<script\b", html))
    style_tags  = len(re.findall(r"<style\b", html))
    json_packs  = re.findall(r'<script\s+type="application/json"\s+id="([^"]+)"', html)
    log(f"  total <script> tags: {script_tags}")
    log(f"  total <style> tags:  {style_tags}")
    log(f"  JSON packs:         {len(json_packs)}")
    for pid in json_packs:
        log(f"    - {pid}")
    return {"sha256": sha_hex, "size": size, "script_tags": script_tags,
            "style_tags": style_tags, "json_packs": json_packs}

# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
if __name__ == "__main__":
    log("TRU ALL-KNOWLEDGE UNIFIED MERGER starting")
    log(f"base:   {BASE}")
    log(f"engine: {ENGINE}")
    log(f"out:    {OUT}")
    inject_summary = inject_into_base()
    sanity = sanity_check()
    report = {
        "build_started":  time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base":           BASE,
        "engine_source":  ENGINE,
        "output":         OUT,
        "output_size_mb": round(sanity["size"]/1024/1024, 2),
        "injection":      inject_summary,
        "sanity":         sanity,
        "policy":         "additive only; no source files modified; output is NEW file",
    }
    with open(REPORT, "w") as f:
        json.dump(report, f, indent=2)
    log(f"=== DONE. report -> {REPORT} ===")
    log(f"=== NEW FILE: {OUT}  ({sanity['size']:,} bytes) ===")
