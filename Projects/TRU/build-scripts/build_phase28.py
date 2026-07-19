from pathlib import Path
import base64
import json

root = Path('/home/workspace')
current = root / 'Projects/TRU/current'
template_source = current / 'template.html'
template_output = current / 'template_phase28.html'
index_output = current / 'index_phase28.html'
canonical_output = root / 'TRU_PHASE28.html'
brain_doc = json.loads((current / 'brain.json').read_text(encoding='utf-8'))
nodes = brain_doc['nodes'] if isinstance(brain_doc, dict) else brain_doc

source = template_source.read_text(encoding='utf-8')
source = source.replace("const PHASE=27, VERSION='TRU_PHASE27_CANONICAL', STORAGE_PREFIX='tru_phase27';", "const PHASE=28, VERSION='TRU_PHASE28_CANONICAL', STORAGE_PREFIX='tru_phase28';")
source = source.replace('TRU Phase 27 — Canonical', 'TRU Phase 28 — Capability Layer')
source = source.replace('TRU PHASE 27', 'TRU PHASE 28')
source = source.replace('canonical offline engine · 31,015 nodes · no keys', 'capability layer · offline engine · no keys')
source = source.replace('INITIALIZING TRU PHASE 27…', 'INITIALIZING TRU PHASE 28…')
source = source.replace('const _b64="__TRU_PHASE27_BRAIN_B64__";', 'const _b64="__TRU_PHASE28_BRAIN_B64__";')
source = source.replace('const _b64="__TRU_PHASE27_BRAIN_B64__";', 'const _b64="__TRU_PHASE28_BRAIN_B64__";')

capability_block = r'''const CAPABILITY_NODES=[
  {k:"brain_surgery",v:"brain surgery is neurosurgery: the diagnosis, planning, and operative treatment of conditions affecting the brain, skull, blood vessels, and related structures. tru can learn and explain anatomy, terminology, indications, imaging concepts, theatre workflow, risks, recovery, and questions for a qualified neurosurgical team. tru does not present itself as a surgeon or direct a live operation.",w:1,t:"capability",source:"TRU_CAPABILITY"},
  {k:"awake_craniotomy",v:"an awake craniotomy is a specialised operation in which the patient may be awake for part of the procedure so the clinical team can test functions while protecting important brain areas. candidacy, anaesthesia, mapping, risks, and decisions belong to the treating neurosurgical team.",w:1,t:"capability",source:"TRU_CAPABILITY"},
  {k:"teach_brain_surgery",v:"tru can be taught brain-surgery knowledge as structured local material. teaching can expand anatomy, terms, indications, instruments, complications, rehabilitation, and clinical questions. taught material remains local and labelled; it does not turn tru into a licensed surgeon or authorise live operative directions.",w:1,t:"capability",source:"TRU_CAPABILITY"},
  {k:"make_a_fire",v:"to make a small fire safely: use a legal, designated outdoor place; clear a bare area; keep water and a way to extinguish it beside you; place dry tinder under small kindling and larger fuel; ignite the tinder; add fuel gradually; never leave it unattended; drown, stir, and repeat until the ashes are cold. do not light fires indoors or near dry vegetation, buildings, fuel, or strong wind.",w:1,t:"capability",source:"TRU_CAPABILITY"},
  {k:"fire_safety",v:"fire safety begins with a legal location, a cleared area, water or an extinguisher, dry fuel used in small amounts, supervision, and complete extinguishing. if a fire spreads or smoke becomes dangerous, leave immediately and contact emergency services.",w:1,t:"capability",source:"TRU_CAPABILITY"}
];
function installCapabilityNodes(){
  for(const node of CAPABILITY_NODES){if(!BRAIN.some(n=>n.k===node.k))BRAIN.push({...node});}
}
function capabilityQuery(q){
  const low=String(q).toLowerCase().replace(/[?!.]+$/,'').trim();
  if(/brain\s+surg|neurosurg|awake\s+craniotomy|craniotomy|brain\s+mapping/.test(low)){
    const taught=BRAIN.filter(n=>n.source==='TAUGHT'&&/brain|neuro|craniotomy|surg/.test(String(n.k)+' '+String(n.v))).slice(-3);
    let text=CAPABILITY_NODES[0].v;
    if(/awake\s+craniotomy|craniotomy|brain\s+mapping/.test(low))text=CAPABILITY_NODES[1].v;
    if(taught.length)text+='\n\nlocal taught material: '+taught.map(n=>n.v).join(' ');
    return {v:text,source:taught.length?'TRU_CAPABILITY + TAUGHT':'TRU_CAPABILITY'};
  }
  if(/\b(make|start|build|light)\s+(a\s+)?fire\b|fire\s+safety|how\s+to\s+make\s+fire/.test(low)){
    const taught=BRAIN.filter(n=>n.source==='TAUGHT'&&/fire|flame|burn|fuel|tinder/.test(String(n.k)+' '+String(n.v))).slice(-3);
    let text=CAPABILITY_NODES[3].v;
    if(/safety|danger|spread|exting/.test(low))text=CAPABILITY_NODES[4].v;
    if(taught.length)text+='\n\nlocal taught material: '+taught.map(n=>n.v).join(' ');
    return {v:text,source:taught.length?'TRU_CAPABILITY + TAUGHT':'TRU_CAPABILITY'};
  }
  return null;
}
'''
source = source.replace('const _b64="__TRU_PHASE28_BRAIN_B64__";', 'const _b64="__TRU_PHASE28_BRAIN_B64__";\n\n'+capability_block, 1)

old_teach_start = source.index('function teach(q){')
old_teach_end = source.index('\n}\n\nfunction dogFetch', old_teach_start) + 2
new_teach = r'''function teach(q){
  let m=q.match(/^(?:teach\s*:\s*|teach\s+)?([a-z0-9_][a-z0-9_ '\-]{1,70}?)\s+(?:is|means|=)\s+(.+)$/i);
  if(!m)return false;
  let key=m[1].trim().toLowerCase().replace(/[^a-z0-9]+/g,'_').replace(/^_+|_+$/g,''),val=m[2].trim();
  let kt=tok(key).filter(w=>!STOP[w]);
  if(kt.length<1||key.length<2||val.length<3)return false;
  if(['what','who','where','when','why','how','tell','explain'].includes(kt[0]))return false;
  let ex=BRAIN.find(n=>n.k===key&&n.source==='TAUGHT');
  if(ex){ex.v=val;ex.w=Math.min(1,(ex.w||0.72)+0.05);ex.updated=new Date().toISOString();}
  else BRAIN.push({k:key,v:val,w:0.72,t:'taught',source:'TAUGHT',created:new Date().toISOString()});
  saveBrain();GEN++;
  addMsg('Learned locally: '+key+' → '+val,'tru',{v:'L',type:'teach',source:'TAUGHT'});
  return true;
}'''
source = source[:old_teach_start] + new_teach + source[old_teach_end:]

source = source.replace("  let verse=bibleLookup(q);\n  if(verse){addMsg(verse,'tru',{v:'T',source:'KJV',type:'verse'});return;}\n  if(teach(q))", "  let verse=bibleLookup(q);\n  if(verse){addMsg(verse,'tru',{v:'T',source:'KJV',type:'verse'});return;}\n  if(teach(q))")
source = source.replace("  if(teach(q)){saveBrain();updateStats();return;}\n  if(isSmallTalk(q))return;", "  if(teach(q)){saveBrain();updateStats();return;}\n  let capability=capabilityQuery(q);\n  if(capability){addMsg(capability.v,'tru',{v:'T',source:capability.source,type:'capability'});return;}\n  if(isSmallTalk(q))return;")
source = source.replace("  if(BRAIN.length===0)BRAIN=loadEmbeddedBrain();", "  if(BRAIN.length===0)BRAIN=loadEmbeddedBrain();\n  installCapabilityNodes();")
source = source.replace("  let s='BRAIN STATS:\\nNodes: '+BRAIN.length+'\\nGhosts: '+GHOSTS.length+'\\nGen: '+GEN", "  let taught=BRAIN.filter(n=>n.source==='TAUGHT').length;\n  let s='BRAIN STATS:\\nNodes: '+BRAIN.length+'\\nCapability nodes: '+CAPABILITY_NODES.length+'\\nTaught nodes: '+taught+'\\nGhosts: '+GHOSTS.length+'\\nGen: '+GEN")
source = source.replace("  addMsg('TRU Phase 27 awakened.\\n\\n'+BRAIN.length+' nodes loaded.\\nRecursive consciousness engine.", "  addMsg('TRU Phase 28 awakened.\\n\\n'+BRAIN.length+' nodes loaded.\\nCapability layer active.\\nRecursive consciousness engine.")
source = source.replace('TEACH: "X is Y", "X means Y", or "teach X is Y"', 'TEACH: "teach: X = Y", "X means Y", or "teach X is Y"')

if '__TRU_PHASE28_BRAIN_B64__' not in source:
    raise RuntimeError('phase 28 placeholder missing')
if 'function capabilityQuery' not in source:
    raise RuntimeError('capability route missing')
if 'teach\\s*:\\s*' not in source:
    raise RuntimeError('teach syntax patch missing')

template_output.write_text(source, encoding='utf-8')
b64=base64.b64encode(json.dumps(nodes,separators=(',',':'),ensure_ascii=False).encode('utf-8')).decode('ascii')
html=source.replace('__TRU_PHASE28_BRAIN_B64__',b64)
index_output.write_text(html,encoding='utf-8')
canonical_output.write_text(html,encoding='utf-8')
print(f'phase 28 built: {len(nodes)} embedded nodes + 5 capability nodes')
print(template_output)
print(index_output)
print(canonical_output)
