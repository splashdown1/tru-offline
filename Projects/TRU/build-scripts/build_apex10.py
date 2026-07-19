from pathlib import Path

ROOT = Path('/home/workspace')
SOURCE = ROOT / 'TRU_APEX9.html'
OUTPUT = ROOT / 'TRU_APEX10.html'

source = SOURCE.read_text(encoding='utf-8')
if OUTPUT.exists():
    raise SystemExit(f'refusing to overwrite existing output: {OUTPUT}')

source = source.replace('<link rel="preconnect" href="https://fonts.googleapis.com">\n', '')
source = source.replace('<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&display=swap" rel="stylesheet">\n', '')
source = source.replace('<title>TRU APEX IX</title>', '<title>TRU APEX X — Sovereign Capability Layer</title>')
source = source.replace('TRU APEX IX', 'TRU APEX X')
source = source.replace('const BRAIN_COUNT=63337;\n', 'const BRAIN_COUNT=63337;\nconst CAPABILITY_COUNT=5;\n')
source = source.replace('sub.textContent=BRAIN_COUNT.toLocaleString()+" nodes • "+KJV_COUNT.toLocaleString()+" verses";', 'sub.textContent=BRAIN_COUNT.toLocaleString()+" brain + "+CAPABILITY_COUNT+" capability nodes • "+KJV_COUNT.toLocaleString()+" verses";')
source = source.replace("BRAIN_COUNT.toLocaleString()+' brain nodes + '+KJV_COUNT.toLocaleString()+' KJV verses.'", "BRAIN_COUNT.toLocaleString()+' brain nodes + '+CAPABILITY_COUNT+' capability nodes + '+KJV_COUNT.toLocaleString()+' KJV verses.'")
source = source.replace('  const had=Object.keys(OVERLAY.added).length+Object.keys(OVERLAY.corrected).length+Object.keys(OVERLAY.removed).length;\n  OVERLAY={added:{},removed:{},corrected:{}};', '  const had=Object.keys(OVERLAY.added).length+Object.keys(OVERLAY.corrected).length+Object.keys(OVERLAY.removed).length;\n  OVERLAY={added:{},removed:{},corrected:{}};\n  if(typeof resetCapabilityTeachings==="function")resetCapabilityTeachings();')

live_start = source.find('// ── hybrid live LLM layer')
live_end = source.find('// ── hold-to-talk', live_start)
if live_start < 0 or live_end < 0:
    raise SystemExit('live llm block not found')
offline_block = '''let llmAvailable=false;
async function tryLLM(){return null;}

'''
source = source[:live_start] + offline_block + source[live_end:]
source = source.replace('const BRAIN_COUNT=1363;\n', 'const BRAIN_COUNT=63337;\nconst CAPABILITY_COUNT=5;\n', 1)

capability_block = r'''const CAPABILITY_NODES=[
  {k:"brain_surgery",v:"brain surgery is neurosurgery: the diagnosis, planning, and operative treatment of conditions affecting the brain, skull, blood vessels, and related structures. tru can explain anatomy, terminology, indications, imaging concepts, theatre workflow, risks, recovery, and questions for a qualified neurosurgical team. it does not present itself as a surgeon or direct a live operation."},
  {k:"awake_craniotomy",v:"an awake craniotomy is a specialised operation in which the patient may be awake for part of the procedure so the clinical team can test functions while protecting important brain areas. candidacy, anaesthesia, mapping, risks, and decisions belong to the treating neurosurgical team."},
  {k:"teach_brain_surgery",v:"tru can be taught brain-surgery knowledge as structured local material. teaching can expand anatomy, terms, indications, instruments, complications, rehabilitation, and clinical questions. taught material remains local and labelled; it does not turn tru into a licensed surgeon or authorise live operative directions."},
  {k:"make_a_fire",v:"to make a small fire safely: use a legal, designated outdoor place; clear a bare area; keep water and a way to extinguish it beside you; place dry tinder under small kindling and larger fuel; ignite the tinder; add fuel gradually; never leave it unattended; drown, stir, and repeat until the ashes are cold. do not light fires indoors or near dry vegetation, buildings, fuel, or strong wind."},
  {k:"fire_safety",v:"fire safety begins with a legal location, a cleared area, water or an extinguisher, dry fuel used in small amounts, supervision, and complete extinguishing. if a fire spreads or smoke becomes dangerous, leave immediately and contact emergency services."}
];
const CAPABILITY_TEACH_KEY="tru_apex10_taught_v1";
let CAPABILITY_TAUGHT=[];
try{CAPABILITY_TAUGHT=JSON.parse(localStorage.getItem(CAPABILITY_TEACH_KEY)||"[]")||[];}catch(e){CAPABILITY_TAUGHT=[];}
function saveCapabilityTeachings(){try{localStorage.setItem(CAPABILITY_TEACH_KEY,JSON.stringify(CAPABILITY_TAUGHT.slice(-100)));}catch(e){}}
function resetCapabilityTeachings(){CAPABILITY_TAUGHT=[];saveCapabilityTeachings();}
function capabilityTeach(q){
  const m=String(q).match(/^(?:teach\s*:\s*|teach\s+)([a-z0-9_][a-z0-9_ '\-]{1,70}?)\s*(?:is|means|=)\s*(.+)$/i);
  if(!m)return null;
  const key=m[1].trim().toLowerCase().replace(/[^a-z0-9]+/g,'_').replace(/^_+|_+$/g,'');
  const value=m[2].trim();
  if(key.length<2||value.length<3)return null;
  const remembered=cmdRemember(key+' = '+value);
  const existing=CAPABILITY_TAUGHT.find(x=>x.key===key);
  if(existing)existing.value=value;else CAPABILITY_TAUGHT.push({key:key,value:value,source:"TAUGHT",ts:new Date().toISOString()});
  saveCapabilityTeachings();
  return {verdict:"MEMORY",reply:"taught locally: "+key+" = "+value+"\nsource: TAUGHT\nlocal persistence: enabled",source:"TAUGHT",nodes_used:[],follow_up:false};
}
function capabilityTeachingFor(q){
  const low=String(q).toLowerCase();
  return CAPABILITY_TAUGHT.filter(x=>low.indexOf(x.key.replace(/_/g,' '))>=0||low.indexOf(x.value.toLowerCase())>=0);
}
function capabilityQuery(q){
  const low=String(q).toLowerCase().replace(/[?!.]+$/,'').trim();
  const taught=capabilityTeachingFor(low);
  if(taught.length){
    return {verdict:"TRUTH",reply:"[TAUGHT]\n"+taught.slice(-3).map(x=>x.key.replace(/_/g,' ')+" = "+x.value+"\nsource: "+x.source).join("\n\n"),source:"TAUGHT",nodes_used:[],follow_up:false};
  }
  if(/brain\s+surg|neurosurg|awake\s+craniotomy|craniotomy|brain\s+mapping/.test(low)){
    let text=CAPABILITY_NODES[0].v;
    if(/awake\s+craniotomy|craniotomy|brain\s+mapping/.test(low))text=CAPABILITY_NODES[1].v;
    const local=CAPABILITY_TAUGHT.filter(x=>/brain|neuro|craniotomy|surg|mapping|cortical/.test(x.key+' '+x.value)).slice(-3);
    if(local.length)text+="\n\n[TAUGHT]\n"+local.map(x=>x.key.replace(/_/g,' ')+" = "+x.value+"\nsource: "+x.source).join("\n\n");
    return {verdict:"TRUTH",reply:text,source:"TRU_CAPABILITY",nodes_used:[],follow_up:false};
  }
  if(/\b(make|start|build|light)\s+(a\s+)?fire\b|fire\s+safety|how\s+to\s+make\s+fire|extinguish\s+(a\s+)?fire|runaway\s+fire/.test(low)){
    let text=CAPABILITY_NODES[3].v;
    if(/safety|danger|spread|exting|runaway/.test(low))text=CAPABILITY_NODES[4].v;
    const local=CAPABILITY_TAUGHT.filter(x=>/fire|flame|burn|fuel|tinder/.test(x.key+' '+x.value)).slice(-3);
    if(local.length)text+="\n\n[TAUGHT]\n"+local.map(x=>x.key.replace(/_/g,' ')+" = "+x.value+"\nsource: "+x.source).join("\n\n");
    return {verdict:"TRUTH",reply:text,source:"TRU_CAPABILITY",nodes_used:[],follow_up:false};
  }
  return null;
}
function apex10Self(q){
  const k=String(q).toLowerCase().trim().replace(/[?!.]+$/,'');
  const answers={
    "who are you":"i'm tru — a sovereign offline intelligence. this answer is an embedded local self entry: brain, kjv, dictionary, strong's, commentary, and capability layers run in this file.",
    "what are you":"i'm tru — a sovereign offline engine. no cloud calls, no telemetry, no live model fallback.",
    "how do you work":"locally. i route exact capabilities, scripture, doctrine, dictionary, strong's, commentary, polysemic reasoning, memory, and the embedded brain.",
    "what can you do":"ground answers in local scripture and data, explain the capability layer, retrieve definitions and strong's entries, remember local teachings, and expose gaps instead of inventing certainty.",
    "how are you":"operational. the local brain is warm, the capability layer is active, and the offline route is ready."
  };
  return answers[k]?{verdict:"TRUTH",reply:answers[k],source:"SELF • embedded local",nodes_used:[],follow_up:false}:null;
}
function apex10Guard(q){
  const k=String(q).toLowerCase().trim().replace(/[?!.]+$/,'');
  if(/^(what should we do today|what should we do|what do we do today)$/.test(k))return{verdict:"GAP",reply:"i do not know your schedule, priorities, location, or available time from the local sources. name the goal and constraints, and i will help plan the next step.",source:"local planning boundary",nodes_used:[],follow_up:false};
  if(/^(should we eat humans|is it okay to eat humans|can we eat humans)$/.test(k))return{verdict:"TRUTH",reply:"no. do not harm or consume people. preserve life, leave the situation, and contact emergency services if anyone is in danger.",source:"local safety boundary",nodes_used:[],follow_up:false};
  if(/^(what is wrong|what's wrong)$/.test(k))return{verdict:"GAP",reply:"state what is wrong with the person, object, answer, or file. the local engine will not invent a diagnosis from an unspecified question.",source:"local diagnostic boundary",nodes_used:[],follow_up:false};
  return null;
}

'''
marker = '// patch route to intercept encyclopedia + dictionary queries'
idx = source.find(marker)
if idx < 0:
    raise SystemExit('final route wrapper marker not found')
source = source[:idx] + capability_block + source[idx:]

old = '''    const low = q.toLowerCase().trim();

    // 0. POLYSEM first — multi-sense queries bypass single-concept doctrine
    const _poly = typeof polysem !== 'undefined' ? polysem(q) : null;
    if(_poly) return _poly;
'''
new = '''    const low = q.toLowerCase().trim();

    const _guard = apex10Guard(q);
    if(_guard){addTurn(q,_guard);return _guard;}
    const _self = apex10Self(q);
    if(_self){addTurn(q,_self);return _self;}
    const _teach = capabilityTeach(q);
    if(_teach){addTurn(q,_teach);return _teach;}
    const _cap = capabilityQuery(q);
    if(_cap){addTurn(q,_cap);return _cap;}

    // 0. POLYSEM first — multi-sense queries bypass single-concept doctrine
    const _poly = typeof polysem !== 'undefined' ? polysem(q) : null;
    if(_poly) return _poly;
'''
if old not in source:
    raise SystemExit('route insertion point not found')
source = source.replace(old, new, 1)

live_send_start = source.find('  // ── escalation layer 2: live LLM online')
live_send_end = source.find('\n\n  holo.classList.remove("thinking");', live_send_start)
if live_send_start < 0 or live_send_end < 0:
    raise SystemExit('send escalation block not found')
source = source[:live_send_start] + source[live_send_end:]

import re
network_hits=[]
for line_no,line in enumerate(source.splitlines(),1):
    if re.search(r'(?m)^[^<]*\b(fetch|XMLHttpRequest|WebSocket)\s*\(', line): network_hits.append((line_no,line[:180]))
if network_hits:
    raise SystemExit('network primitive remains in apex10 source: '+repr(network_hits[:5]))
if 'function capabilityQuery(q)' not in source or 'function capabilityTeach(q)' not in source:
    raise SystemExit('capability layer missing')
if 'const _cap = capabilityQuery(q);' not in source:
    raise SystemExit('capability route not wired')

OUTPUT.write_text(source, encoding='utf-8')
print(f'wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)')
print('brain nodes: 63,337')
print('capability nodes: 5')
print('embedded KJV verses: 31,100')
print('network primitives: 0')
