#!/usr/bin/env python3
"""Build TRU_COMPLETE.html — TRU_SOVEREIGN engine + integrated WordNet dictionary.
Routing: define/definition of/what does X mean → dictionary; verses → scripture;
G/H#### → strong's; why/what is → brain; else → brain/GAP.
"""
import json, re, os

BASE = "/home/workspace"
SRC = f"{BASE}/TRU_SOVEREIGN.html"
DICT = f"{BASE}/Projects/TRU/data/wordnet_compact.json"
OUT = f"{BASE}/TRU_COMPLETE.html"
MANIFEST_OUT = f"{BASE}/Projects/TRU/current/tru_module_manifest.json"


def compact(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


print("loading sovereign + dict data...")
html = open(SRC, "r", encoding="utf-8", errors="replace").read()
dict_data = json.load(open(DICT))
print(f"  sovereign: {len(html):,} bytes, dict words: {len(dict_data):,}")

# ---- 1. inject dict-data block right after brain-data block ----
print("injecting dict-data block...")
m = re.search(r'(<script type="application/json" id="brain-data">.*?</script>)', html, re.DOTALL)
assert m, "brain-data block not found"
insert_after = m.end()
dict_block = '<script type="application/json" id="dict-data">' + compact(dict_data) + '</script>'
html = html[:insert_after] + "\n" + dict_block + html[insert_after:]
print(f"  dict block: {len(dict_block):,} bytes")

# ---- 2. add _DICT var + seedDict + dictQuery + dictBuild ----
print("injecting engine functions...")
old_vars = "let _SEED=null,_BRAIN=null,_KJV=null,_BRAIN_IDX=null;"
assert old_vars in html, "brain vars not found"
new_vars = old_vars + "\nlet _DICT=null;"
html = html.replace(old_vars, new_vars, 1)

# seedDict function (lazy load, same pattern as seedBrain)
seed_fn = """
function seedDict(){ if(_DICT===null){ try{ _DICT=JSON.parse(document.getElementById('dict-data').textContent); }catch(e){ _DICT={}; } } return _DICT; }
function htmlesc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
const DICT_STOP=new Set(["define","definition","what","does","mean","means","the","a","an","of","is","me","tell","do","you","know","how","to","please","def"]);
function dictQuery(q){
  const D=seedDict();
  const low=q.toLowerCase().trim();
  let m;
  if(m=low.match(/\\bdefine\\s+(.+)/)) return dictBuild(m[1].trim(),D);
  if(m=low.match(/definition\\s+of\\s+(.+)/)) return dictBuild(m[1].trim(),D);
  if(m=low.match(/what\\s+does\\s+(.+?)\\s+mean/)) return dictBuild(m[1].trim(),D);
  if(m=low.match(/what\\s+is\\s+the\\s+definition\\s+of\\s+(.+)/)) return dictBuild(m[1].trim(),D);
  return null;
}
function dictBuild(word,D){
  word=word.toLowerCase().replace(/[^a-z0-9'-]/g,'').trim();
  if(!word||word.length<2) return null;
  const cands=[word,word.replace(/s$/,''),word+'s',word.replace(/ing$/,''),word.replace(/ed$/,''),word.replace(/ly$/,'')];
  let senses=null,mw=word;
  for(const c of cands){ if(D[c]){senses=D[c];mw=c;break;} }
  if(!senses) return {reply:"No dictionary entry for \\""+word+"\\". TRU covers "+Object.keys(D).length.toLocaleString()+" words from WordNet.",verdict:"GAP",nodes_used:[],follow_up:false,source:"offline-dict"};
  let lines=["\\u{1F4D6} "+mw];
  senses.forEach((s,i)=>{
    let line="["+s.p+"] "+(i+1)+". "+s.d;
    if(s.s&&s.s.length>1){
      const syn=s.s.filter(w=>w.toLowerCase()!==mw).slice(0,8);
      if(syn.length) line+="  (syn: "+syn.join(", ")+")";
    }
    lines.push(line);
  });
  if(lines.length>12) lines=lines.slice(0,12).concat("... +"+(senses.length-12)+" more senses");
  return {reply:lines.join("\\n"),verdict:"DEFINE",nodes_used:[],follow_up:false,source:"offline-dict"};
}
"""
# inject before route function
route_idx = html.find("function route(q){")
assert route_idx != -1, "route function not found"
html = html[:route_idx] + seed_fn + "\n" + html[route_idx:]

# ---- 3. inject dict check at top of route ----
old_route = 'function route(q){\n  const cmd=command(q);'
new_route = 'function route(q){\n  const dict=dictQuery(q);if(dict){addTurn(q,dict);return dict;}\n  const cmd=command(q);'
assert old_route in html, "route start not found"
html = html.replace(old_route, new_route, 1)

# ---- 4. add DEFINE verdict to VNAME + VERDICT ----
html = html.replace(
    'const VNAME={TRUTH:"TRUTH",SCRIPTURE:"SCRIPTURE",REASON:"REASON",MEMORY:"MEMORY",GAP:"GAP",UNKNOWN:"UNKNOWN",CALC:"CALC"}',
    'const VNAME={TRUTH:"TRUTH",SCRIPTURE:"SCRIPTURE",REASON:"REASON",MEMORY:"MEMORY",GAP:"GAP",UNKNOWN:"UNKNOWN",CALC:"CALC",DEFINE:"DEFINE"}',
    1)
html = html.replace(
    'const VERDICT={TRUTH:"#d8a657",SCRIPTURE:"#b388ff",REASON:"#00e5ff",MEMORY:"#69f0ae",GAP:"#ff5252",UNKNOWN:"#888",CALC:"#aaff00"}',
    'const VERDICT={TRUTH:"#d8a657",SCRIPTURE:"#b388ff",REASON:"#00e5ff",MEMORY:"#69f0ae",GAP:"#ff5252",UNKNOWN:"#888",CALC:"#aaff00",DEFINE:"#e8d44b"}',
    1)

# ---- 5. tighten provenance display in the ui ----
html = html.replace(
    'function addMsg(role,text,verdict,ms){',
    'function addMsg(role,text,verdict,meta){',
    1,
)
html = html.replace(
    'vd.textContent=(VNAME[verdict]||verdict)+(ms?" · "+ms+"ms":"");',
    'vd.textContent=(VNAME[verdict]||verdict)+(meta?" · provenance: "+meta:"");',
    1,
)
html = html.replace(
    '  addMsg("tru",res.reply,res.verdict,res.source?("· "+res.source):"");\n  const src = res.source ? " • "+res.source : " • offline";\n  statusEl.textContent="● "+res.verdict+src;\n',
    '  addMsg("tru",res.reply,res.verdict,res.source||"");\n  const src = res.source ? " • provenance: "+res.source : " • offline";\n  statusEl.textContent="● "+res.verdict+src;\n',
    1,
)

# ---- 6. update boot count text to mention dictionary ----
html = html.replace("31,100 KJV verses", "31,100 KJV verses + 147,982 dictionary words", 1)

# ---- write ----
print("writing...")
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
manifest = {
    "export": os.path.relpath(OUT, BASE),
    "builder": os.path.relpath(__file__, BASE),
    "shell_source": os.path.relpath(SRC, BASE),
    "dictionary": os.path.relpath(DICT, BASE),
    "bridge_crawler": "Projects/TRU/SNAKING_BRIDGE_CRAWLER.md",
    "counts": {
        "dictionary_words": len(dict_data),
        "export_bytes": os.path.getsize(OUT),
    },
}
os.makedirs(os.path.dirname(MANIFEST_OUT), exist_ok=True)
with open(MANIFEST_OUT, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
sz = os.path.getsize(OUT)
print(f"\nDONE: {OUT}")
print(f"size: {sz:,} bytes = {sz/1048576:.2f} MB")
print(f"manifest: {MANIFEST_OUT}")
