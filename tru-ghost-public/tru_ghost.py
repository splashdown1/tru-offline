#!/usr/bin/env python3
"""TRU ghost builder. Reads JSON on stdin, writes JSON on stdout.
CLI: python3 tru_ghost.py [--nt-only] [--cap N] [--ts NAME] [--out-dir DIR] [--lookup Q]"""
import json, sys, html, os, argparse
from pathlib import Path
BRAIN = Path("/home/workspace/Projects/TRU/current/brain.json")
KJV = Path("/home/workspace/Projects/TRU/data/kjv_full.json")
SNAP = Path("/home/workspace/Projects/TRU/state/tru_session.json")
GHOST_DIR = Path("/home/workspace/Projects/TRU/ghost")

STOP = set("the a an and or but if then to of in on for with from by as at is are was were be been being i me my you your we us our they them it this that those these what why how who when where should would could can do does did about into over under again".split())

def esc(s):
    return html.escape(str(s), quote=True)

def toks(s):
    return [t for t in re.sub(r"[^a-z0-9 ]", " ", str(s or "").lower()).split() if len(t) > 2 and t not in STOP]

import re

BOOK_LONG = {
  "gen":"genesis","gn":"genesis","genesis":"genesis",
  "ps":"psalms","psa":"psalms","psalm":"psalms","psalms":"psalms",
  "mt":"matthew","matt":"matthew","matthew":"matthew",
  "mk":"mark","mark":"mark",
  "lk":"luke","luke":"luke",
  "jn":"john","jhn":"john","john":"john",
  "1co":"1 corinthians","1cor":"1 corinthians","1corinthians":"1 corinthians",
  "judges":"judges","jdg":"judges",
  "ruth":"ruth","ru":"ruth",
  "romans":"romans","rom":"romans",
  "rev":"revelation","revelation":"revelation",
}

def parse_verse(q):
    m = re.search(r"\b((?:[1-3]\s*)?[a-z]+)\s+(\d+):(\d+)\b", str(q or "").lower())
    if not m: return None
    long = BOOK_LONG.get(m.group(1).replace(" ",""))
    if not long: return None
    return f"{long} {m.group(2)}:{m.group(3)}"

def load_brain(cap=999999):
    try:
        raw = json.loads(BRAIN.read_text())
        arr = raw if isinstance(raw, list) else raw.get("nodes", [])
        seen = set(); out = []
        for n in arr:
            if not isinstance(n, dict) or not isinstance(n.get("k"), str) or not isinstance(n.get("v"), str): continue
            v = n["v"]
            if v in seen or len(v) < 20: continue
            seen.add(v); out.append(n)
            if len(out) >= cap: break
        return out
    except: return []

def load_kjv(lite=True, nt_only=False):
    try:
        raw = json.loads(KJV.read_text())
        m = {}
        for v in raw:
            if nt_only and v.get("testament") != "nt": continue
            r = str(v.get("ref","")).lower()
            t = v.get("text","")
            if r and t:
                m[r] = t
                if lite:
                    a = v.get("abbrev")
                    if a: m[str(a).lower()] = t
        return m
    except: return {}

def load_session():
    try: return json.loads(SNAP.read_text())
    except: return {"history": []}

def lookup(q, brain, kjv, session):
    ql = str(q or "").strip().lower()
    # 1) scripture
    ref = parse_verse(ql)
    if ref and kjv.get(ref):
        return {"kind":"SCRIPTURE","text":f"{ref} — {kjv[ref]}","score":100,"source":"kjv"}
    # 2) brain
    qw = toks(ql)
    if qw and brain:
        best = None
        for n in brain:
            nw = toks((n.get("k","") or "") + " " + (n.get("v","") or ""))
            hit = sum(1 for t in qw if t in nw)
            if not hit: continue
            score = min(100, int((hit / max(len(qw),1)) * 100 * (n.get("w") or 0.7)))
            if not best or score > best["score"]:
                best = {"kind":(n.get("t") or "TRUTH").upper(),"text":n.get("v",""),"score":score,"source":n.get("source") or "brain"}
        if best: return best
    # 3) session
    hist = session.get("history") or []
    if hist:
        last = hist[-1]
        txt = last.get("a") or last.get("answer") or last.get("text") or ""
        if txt: return {"kind":"MEMORY","text":str(txt),"score":88,"source":"session"}
    return {"kind":"GAP","text":"no match. ask differently.","score":0,"source":None}

def build_html(brain, kjv, session, ts):
    bjson = json.dumps(brain)
    kjson = json.dumps(kjv, separators=(",", ":"))
    sjson = json.dumps(session)
    hitems = "".join(
        '<div class="item"><div class="q">Q: '+esc(h.get("q") or h.get("question") or "")+
        '</div><div class="a">A: '+esc(h.get("a") or h.get("answer") or "")+'</div></div>'
        for h in (session.get("history") or [])[-12:]
    )
    last_q = esc(session.get("last_q") or "")
    return (
'<!doctype html><html lang="en"><head><meta charset="utf-8">'
'<meta name="viewport" content="width=device-width,initial-scale=1">'
f'<title>tru ghost</title>'
'<style>body{margin:0;background:#020208;color:#efe7d6;font-family:ui-monospace,monospace}'
'main{max-width:900px;margin:0 auto;padding:24px}'
'h1{margin:0 0 6px;color:#d8a657;letter-spacing:.14em;text-transform:uppercase;font-size:20px}'
'.sub{color:#6f6a5f;font-size:11px;letter-spacing:.12em;margin-bottom:18px}'
'input,button{font:inherit}input{width:100%;box-sizing:border-box;background:#0b0b14;border:1px solid #1e1e2a;color:#efe7d6;padding:12px 14px;border-radius:10px;outline:none}'
'button{background:transparent;border:1px solid #d8a657;color:#d8a657;padding:10px 14px;border-radius:999px;cursor:pointer;letter-spacing:.12em;text-transform:uppercase;font-size:11px}'
'.row{display:flex;gap:10px;align-items:center;margin:14px 0 18px}'
'.out{border-left:3px solid #d8a657;background:rgba(216,166,87,.05);padding:14px 16px;border-radius:0 10px 10px 0;white-space:pre-wrap;line-height:1.6}'
'.meta{font-size:10px;letter-spacing:.12em;color:#a49b8c;margin-bottom:8px}'
'.history{margin-top:22px;border-top:1px solid #1d1d2b;padding-top:16px}'
'.item{margin:10px 0;padding:12px 14px;background:#0b0b14;border:1px solid #171723;border-radius:10px}'
'.q{color:#9ed7ff}.a{color:#efe7d6;margin-top:6px}'
'.foot{margin-top:20px;font-size:10px;letter-spacing:.16em;color:#6c655b;text-align:center}'
'</style></head><body><main>'
f'<h1>tru ghost</h1><div class="sub">baked {esc(ts)} · offline · airgapped</div>'
'<div class="row"><input id="q" placeholder="ask tru..." autofocus>'
'<button id="ask">ask</button><button id="save">save copy</button></div>'
'<div id="out" class="out">ready.</div><div id="history" class="history"></div>'
'<div class="foot">no network · no telemetry · no cloud</div>'
'</main><script>'
f'const BRAIN={bjson};const KJV={kjson};const SESSION={sjson};'
'const STOP=new Set(["the","a","an","and","or","but","if","then","to","of","in","on","for","with","from","by","as","at","is","are","was","were","be","been","being","i","me","my","you","your","we","us","our","they","them","it","this","that","those","these","what","why","how","who","when","where","should","would","could","can","do","does","did","about","into","over","under","again"]);'
'function tok(s){return String(s||"").toLowerCase().replace(/[^a-z0-9 ]/g," ").split(/\\s+/).filter(t=>t.length>2&&!STOP.has(t));}'
'function esc2(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}'
'function lookup(q){const ql=String(q||"").trim().toLowerCase();const m=ql.match(/\\b((?:[1-3]\\s*)?[a-z]+)\\s+(\\d+):(\\d+)\\b/);if(m){const map={genesis:"genesis",ps:"psalms",psalm:"psalms",psalms:"psalms",matthew:"matthew",mark:"mark",luke:"luke",john:"john",romans:"romans",revelation:"revelation",judges:"judges",ruth:"ruth","1 corinthians":"1 corinthians"};const long=map[m[1].replace(/\\s+/g,"")];if(long){const ref=(long+" "+m[2]+":"+m[3]).toLowerCase();if(KJV[ref])return{kind:"SCRIPTURE",text:ref+" — "+KJV[ref],score:100};}}'
'const qw=tok(q);let best=null;for(const n of BRAIN){const nw=tok(n.k+" "+n.v);let hit=0;for(const t of qw)if(nw.includes(t))hit++;if(!hit)continue;const score=Math.round(Math.min(100,(hit/Math.max(qw.length,1))*100*(n.w||0.7)));if(!best||score>best.score)best={kind:(n.t||"TRUTH").toUpperCase(),text:n.v,score,source:n.source||"brain"};}'
'if(best)return best;const hist=SESSION.history||[];if(hist.length){const last=hist[hist.length-1];return{kind:"MEMORY",text:String(last.a||last.answer||last.text||""),score:88,source:"session"};}return{kind:"GAP",text:"no match. ask differently.",score:0};}'
'function render(){const q=document.getElementById("q").value.trim();const r=lookup(q);document.getElementById("out").innerHTML="<div class=\\"meta\\">"+r.kind+" · "+r.score+"%"+(r.source?" · "+r.source:"")+"</div><div>"+esc2(r.text)+"</div>";}'
'function save(){const blob=new Blob([document.documentElement.outerHTML],{type:"text/html"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="tru-ghost.html";document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}'
f'document.getElementById("history").innerHTML={json.dumps(hitems)};'
f'document.getElementById("q").value={json.dumps(last_q)};'
'document.getElementById("ask").onclick=render;document.getElementById("save").onclick=save;document.getElementById("q").addEventListener("keydown",e=>{if(e.key==="Enter")render()});'
'</script></body></html>'
    )

def parse_args():
    p = argparse.ArgumentParser(description="TRU Ghost offline scripture engine builder")
    p.add_argument("--nt-only", action="store_true", help="New Testament only (~1.4mb vs ~5.7mb full)")
    p.add_argument("--cap", type=int, default=999999, help="Brain node cap (default: unlimited)")
    p.add_argument("--ts", default=None, help="Timestamp string for output filename")
    p.add_argument("--out-dir", default=None, help="Output dir (default: /home/workspace/Projects/TRU/ghost)")
    p.add_argument("--lookup", default=None, help="Run a single lookup, print result, exit")
    return p.parse_args()

def main():
    # CLI mode if any arg was passed
    if len(sys.argv) > 1 and sys.argv[1] != "build":
        args = parse_args()
        brain = load_brain(cap=args.cap)
        kjv = load_kjv(lite=True, nt_only=args.nt_only)
        if args.lookup:
            result = lookup(args.lookup, brain, kjv, load_session())
            print(json.dumps({"ok": True, "result": result}))
            return
        session = load_session()
        from datetime import datetime
        ts = args.ts or datetime.utcnow().isoformat().replace(":", "-").replace(".", "-")
        html = build_html(brain, kjv, session, ts)
        out = Path(args.out_dir) if args.out_dir else GHOST_DIR
        out.mkdir(parents=True, exist_ok=True)
        fp = out / f"tru-ghost-{ts}.html"
        fp.write_text(html, encoding="utf-8")
        print(json.dumps({"ok": True, "path": str(fp), "bytes": len(html)}))
        return
    # legacy JSON-on-stdin mode
    try:
        req = json.loads(sys.stdin.read() or "{}")
    except:
        req = {}
    action = req.get("action", "build")
    if action == "lookup":
        brain = load_brain()
        result = lookup(req.get("q",""), brain, load_kjv(), load_session())
        print(json.dumps({"ok": True, "result": result}))
        return
    nt_only = bool(req.get("nt_only"))
    brain_cap = int(req.get("brain_cap") or 999999)
    brain = load_brain(cap=brain_cap)
    kjv = load_kjv(lite=True, nt_only=nt_only)
    session = load_session()
    ts = req.get("ts") or __import__("datetime").datetime.utcnow().isoformat().replace(":", "-").replace(".", "-")
    html = build_html(brain, kjv, session, ts)
    GHOST_DIR.mkdir(parents=True, exist_ok=True)
    fp = GHOST_DIR / f"tru-ghost-{ts}.html"
    fp.write_text(html, encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(fp), "bytes": len(html)}))

if __name__ == "__main__":
    main()
