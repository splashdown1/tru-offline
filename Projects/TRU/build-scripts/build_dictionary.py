#!/usr/bin/env python3
"""Build TRU_DICTIONARY.html — standalone offline dictionary using WordNet.
Detects 'define WORD' / 'what does X mean' / bare word → returns POS, definition, synonyms, example.
"""
import json, re, os, html as htmllib

W = "/home/.z/workspaces/con_ejOuxXpCB2EUV63s/wordnet.json"
OUT = "/home/workspace/TRU_DICTIONARY.html"
DICT_OUT = "/home/workspace/Projects/TRU/data/wordnet_compact.json"

# ---- build word -> senses index ----
print("loading wordnet...")
wn = json.load(open(W))
syn = wn["synset"]
ex_tbl = wn.get("example") or {}  # {templateNumber_str: "sentence with %s"}

def resolve_example(s):
    raw = s.get("example")
    if not raw or not isinstance(raw, list) or not raw:
        return None
    first = raw[0]
    tn = str(first.get("templateNumber", ""))
    tmpl = ex_tbl.get(tn)
    if not tmpl:
        return None
    words = s.get("word") or []
    wn_idx = first.get("wordNumber", 0)
    w = words[wn_idx] if wn_idx < len(words) else (words[0] if words else "")
    return tmpl.replace("%s", w) if "%s" in tmpl else tmpl

POS_MAP = {"n": "noun", "v": "verb", "a": "adj", "s": "adj", "r": "adv"}
idx = {}
for sid, s in syn.items():
    pos = POS_MAP.get(s.get("pos", ""), s.get("pos", ""))
    gloss = (s.get("gloss") or "").strip()
    if not gloss:
        continue
    ex = resolve_example(s)
    words = s.get("word") or []
    entry = {"p": pos, "d": gloss, "e": ex}
    entry["s"] = [w for w in words if w]  # synonyms (incl. self)
    for w in words:
        key = w.lower()
        idx.setdefault(key, []).append(entry)

print(f"  unique words: {len(idx)}")
print(f"  total senses: {sum(len(v) for v in idx.values())}")

# sort senses per word: noun first, then verb, adj, adv; then by gloss length
order = {"noun": 0, "verb": 1, "adj": 2, "adv": 3}
for k in idx:
    idx[k].sort(key=lambda e: (order.get(e["p"], 9), len(e["d"])))

compact = json.dumps(idx, ensure_ascii=False, separators=(",", ":"))
with open(DICT_OUT, "w", encoding="utf-8") as f:
    f.write(compact)
print(f"  dict_compact.json: {len(compact):,} bytes ({len(compact)/1048576:.2f} MB)")

# ---- build standalone HTML ----
# engine: parse query, look up word, render senses
ENGINE = r'''
const D=__DICT__;
function el(t,c,h){const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e;}
function lookup(word){
  word=word.toLowerCase().trim();
  // direct hit
  if(D[word]) return {word, senses:D[word]};
  // try singular/plural + base forms
  const cands=[word, word.replace(/s$/,''), word+'s', word.replace(/ing$/,''), word.replace(/ed$/,''), word.replace(/ly$/,'')];
  for(const c of cands){ if(D[c]) return {word:c, senses:D[c], matched:c}; }
  return null;
}
const STOP=new Set(["define","definition","what","does","mean","means","the","a","an","of","is","me","tell","do","you","know","how","to","please","def"]);
function parse(q){
  q=q.toLowerCase().trim().replace(/[^a-z0-9\s'-]/g,' ').replace(/\s+/g,' ');
  const toks=q.split(' ').filter(t=>t&&!STOP.has(t));
  // patterns: "define X", "definition of X", "what does X mean", "what is X", bare "X"
  let m;
  if(m=q.match(/\bdefine\s+(.+)/)){return m[1].trim();}
  if(m=q.match(/definition\s+of\s+(.+)/)){return m[1].trim();}
  if(m=q.match(/what\s+(?:does|do)\s+(.+?)\s+mean/)){return m[1].trim();}
  if(m=q.match(/what(?:'s| is)\s+(?:an?\s+)?(.+)/)){return m[1].trim();}
  if(m=q.match(/meaning\s+of\s+(.+)/)){return m[1].trim();}
  // fallback: join non-stop tokens
  if(toks.length) return toks.join(' ');
  return q;
}
function render(res){
  if(!res) return '<div style="color:#b33;padding:14px;border-radius:8px;background:rgba(255,80,80,.08)">No entry found. TRU Dictionary covers '+Object.keys(D).length.toLocaleString()+' words from WordNet.</div>';
  let html='<div class="entry">';
  html+='<div class="hw">'+htmlesc(res.word)+(res.matched&&res.matched!==res.word?' <span class="match">(→ '+htmlesc(res.matched)+')</span>':'')+'</div>';
  res.senses.forEach((s,i)=>{
    html+='<div class="sense">';
    html+='<span class="pos">'+htmlesc(s.p)+'</span> ';
    html+='<span class="num">'+(i+1)+'</span> ';
    html+='<span class="def">'+htmlesc(s.d)+'</span>';
    if(s.s&&s.s.length>1) html+=' <span class="syn">⇄ '+s.s.filter(w=>w.toLowerCase()!==res.word).slice(0,8).map(htmlesc).join(', ')+'</span>';
    if(s.e) html+='<div class="ex">"'+htmlesc(s.e)+'"</div>';
    html+='</div>';
  });
  html+='</div>';
  return html;
}
function htmlesc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
const input=document.getElementById('q');
const out=document.getElementById('out');
const log=document.getElementById('log');
const examples=['define hope','what does grace mean','faith','definition of love','define sovereignty'];
examples.forEach(ex=>{
  const b=el('button','ex',ex); b.onclick=()=>{input.value=ex;send();}; document.getElementById('exs').appendChild(b);
});
function send(){
  const q=input.value.trim(); if(!q) return;
  const u=el('div','u','<b>you</b><br>'+htmlesc(q)); log.appendChild(u);
  const w=parse(q);
  const res=lookup(w);
  const a=el('div','a','<b>TRU DICTIONARY</b> <span class="badge">offline • wordnet</span><br>'+render(res));
  log.appendChild(a);
  input.value=''; log.scrollTop=log.scrollHeight;
}
input.addEventListener('keydown',e=>{if(e.key==='Enter')send();});
document.getElementById('btn').onclick=send;
// boot status
document.getElementById('status').textContent='● READY • '+Object.keys(D).length.toLocaleString()+' words • OFFLINE';
'''

CSS = r'''
*{box-sizing:border-box;}
body{margin:0;background:#0e0e10;color:#e8e4dc;font-family:Georgia,'Times New Roman',serif;}
.bar{position:sticky;top:0;background:rgba(14,14,16,.94);backdrop-filter:blur(6px);border-bottom:1px solid #2a2a2e;padding:14px 18px;z-index:5;}
.bar h1{margin:0;font-size:18px;letter-spacing:.08em;color:#7fd1c0;}
.bar .sub{font-size:11px;color:#777;margin-top:2px;}
#status{font-size:11px;color:#7fd1c0;margin-top:4px;font-family:monospace;}
.wrap{max-width:760px;margin:0 auto;padding:18px;}
#log{margin-bottom:18px;}
.u,.a{padding:12px 14px;border-radius:8px;margin-bottom:10px;}
.u{background:rgba(255,255,255,.04);text-align:right;}
.a{background:rgba(127,209,192,.06);border-left:3px solid #7fd1c0;}
.badge{font-size:10px;color:#7fd1c0;border:1px solid #2a4a44;border-radius:3px;padding:1px 5px;margin-left:4px;font-family:monospace;}
.entry{margin-top:6px;}
.hw{font-size:26px;font-weight:bold;color:#f5f1e8;margin-bottom:8px;text-transform:lowercase;}
.match{font-size:13px;color:#888;}
.sense{padding:6px 0;border-bottom:1px dashed #2a2a2e;line-height:1.5;}
.sense:last-child{border-bottom:none;}
.pos{display:inline-block;font-size:10px;font-weight:bold;color:#d8a657;border:1px solid #4a3a1a;border-radius:3px;padding:1px 6px;margin-right:5px;font-family:monospace;text-transform:uppercase;}
.num{color:#666;font-size:12px;margin-right:4px;}
.def{color:#e8e4dc;}
.syn{color:#7fd1c0;font-size:12px;}
.ex{color:#888;font-style:italic;font-size:13px;margin-top:3px;margin-left:24px;}
.inrow{display:flex;gap:8px;align-items:center;}
#q{flex:1;background:#1a1a1e;border:1px solid #2a2a2e;color:#e8e4dc;padding:11px 14px;border-radius:8px;font-size:15px;font-family:inherit;}
#q:focus{outline:none;border-color:#7fd1c0;}
#btn{background:#7fd1c0;color:#0e0e10;border:none;width:42px;height:42px;border-radius:50%;font-size:18px;cursor:pointer;font-weight:bold;}
#btn:hover{background:#9fe0d2;}
#exs{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px;}
.ex{background:#1a1a1e;border:1px solid #2a2a2e;color:#aaa;padding:5px 11px;border-radius:14px;font-size:12px;cursor:pointer;font-family:inherit;}
.ex:hover{border-color:#7fd1c0;color:#7fd1c0;}
'''

doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TRU Dictionary — Offline</title>
<style>{CSS}</style>
</head>
<body>
<div class="bar">
  <h1>TRU DICTIONARY</h1>
  <div class="sub">offline wordnet engine • define any word</div>
  <div id="status">● booting…</div>
</div>
<div class="wrap">
  <div id="log"></div>
  <div class="inrow">
    <input id="q" placeholder="define a word…" autocomplete="off" autofocus>
    <button id="btn">↑</button>
  </div>
  <div id="exs"></div>
</div>
<script type="application/json" id="dict-data">{compact}</script>
<script>
const __DICT__=JSON.parse(document.getElementById('dict-data').textContent);
{ENGINE}
</script>
</body>
</html>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(doc)
sz = os.path.getsize(OUT)
print(f"\nDONE: {OUT}")
print(f"size: {sz:,} bytes = {sz/1048576:.2f} MB")
print(f"words: {len(idx):,}")
