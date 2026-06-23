#!/usr/bin/env python3
"""Assemble one canonical offline TRU.html.
Reads brain + KJV from disk, injects into a self-contained HTML template.
No external deps, no CDN, no network. Pure JS router mirrors tru_chat.py.
"""
import json, re
from pathlib import Path

WS = Path("/home/workspace")
BRAIN_PATH = WS / "Projects/TRU/current/brain.json"
KJV_PATH   = WS / "Projects/TRU/data/kjv_full.json"
OUT        = WS / "TRU.html"

# ── load + filter brain (mirror tru_chat.py garbage filter) ──
raw = json.loads(BRAIN_PATH.read_text())
arr = raw if isinstance(raw, list) else raw.get("nodes", [])
clean = []
for n in arr:
    v = str(n.get("v", ""))
    if v.startswith("{") and v.endswith("}"):
        continue
    if len(v) > 1200 and re.search(r"[{}\[\]\\]{5,}", v[:200]):
        continue
    # keep only k + v (w is uniformly 0.6; router defaults 0.7)
    clean.append({"k": n.get("k", ""), "v": v})
BRAIN = clean

# ── load KJV (ref + text only) ──
kjv_raw = json.loads(KJV_PATH.read_text())
KJV = [{"ref": v["ref"], "text": v["text"]} for v in kjv_raw if v.get("ref") and v.get("text")]

# ── serialize, escape </script> ──
def js(o):
    return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")

BRAIN_JS = js(BRAIN)
KJV_JS   = js(KJV)

# ── template ──
TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TRU • Holographic Sovereign</title>
<style>
:root{--cyan:#00e5ff;--bg:#000308;--fg:#e6f7ff;}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{height:100%;}
body{
  background:var(--bg);color:var(--fg);
  font-family:ui-monospace,'Courier New',monospace;
  overflow:hidden;position:fixed;inset:0;
}
#stage{position:absolute;left:0;top:0;bottom:0;width:62%;display:flex;align-items:center;justify-content:center;}
/* radial glow */
#stage::before{content:"";position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(ellipse 60% 50% at 50% 50%,rgba(0,229,255,.10) 0%,transparent 60%);}
/* scanlines */
.scan{position:absolute;inset:0;pointer-events:none;opacity:.05;
  background:repeating-linear-gradient(0deg,rgba(0,229,255,.6) 0,rgba(0,229,255,.6) 1px,transparent 1px,transparent 3px);}
#holo{position:relative;width:min(58vh,520px);aspect-ratio:1;}
.layer{position:absolute;left:50%;top:50%;border-radius:50%;
  transform:translate(-50%,-50%);border:1px solid rgba(0,229,255,.5);
  box-shadow:0 0 24px rgba(0,229,255,.25),inset 0 0 24px rgba(0,229,255,.08);
  animation:spin linear infinite;}
.l-rock{width:30%;height:30%;border:none;background:radial-gradient(circle,var(--core,#00e5ff) 0%,rgba(0,229,255,.15) 60%,transparent 100%);
  box-shadow:0 0 60px var(--core,#00e5ff),inset 0 0 30px rgba(255,255,255,.15);animation:breathe 4s ease-in-out infinite;}
.l-immune{width:46%;height:46%;border-style:dashed;animation-duration:24s;}
.l-tribunal{width:56%;height:56%;border-width:2px;animation-duration:18s;animation-direction:reverse;}
.l-wizard{width:66%;height:66%;border-color:rgba(0,229,255,.25);border-style:dotted;animation-duration:32s;}
.l-mirror{width:78%;height:78%;border-color:rgba(0,229,255,.18);animation-duration:42s;animation-direction:reverse;}
.l-standby{width:92%;height:92%;border-color:rgba(0,229,255,.10);animation-duration:60s;}
@keyframes spin{to{transform:translate(-50%,-50%) rotate(360deg);}}
@keyframes breathe{0%,100%{transform:translate(-50%,-50%) scale(1);}50%{transform:translate(-50%,-50%) scale(1.08);}}
.thinking .layer{animation-duration:2s!important;}
.thinking .l-rock{box-shadow:0 0 80px var(--core,#00e5ff),inset 0 0 40px rgba(255,255,255,.3);}

/* header */
.h-title{position:absolute;top:22px;left:42px;font-size:18px;letter-spacing:3px;text-transform:uppercase;
  color:var(--cyan);text-shadow:0 0 18px var(--cyan);pointer-events:none;}
.h-sub{position:absolute;top:48px;left:42px;font-size:10px;color:rgba(0,229,255,.55);letter-spacing:2px;pointer-events:none;}
.legend{position:absolute;left:42px;top:74px;font-size:9px;letter-spacing:2px;color:rgba(0,229,255,.5);line-height:1.9;pointer-events:none;}
.legend div::before{content:"◇ ";}

/* verdict + voice */
.topbar{position:absolute;top:22px;left:44%;display:flex;gap:10px;align-items:center;}
.badge{font-size:11px;letter-spacing:2px;padding:5px 12px;border:1px solid var(--vc,#00e5ff);
  border-radius:999px;text-shadow:0 0 12px var(--vc,#00e5ff);color:var(--vc,#00e5ff);}
.btn{background:transparent;border:1px solid rgba(0,229,255,.3);color:var(--cyan);padding:5px 12px;
  border-radius:999px;font-size:11px;letter-spacing:1px;cursor:pointer;font-family:inherit;}
.btn:hover{background:rgba(0,229,255,.08);}

/* chat */
#chat{position:absolute;right:36px;top:80px;bottom:140px;width:440px;max-width:40vw;
  background:rgba(2,10,18,.78);border:1px solid rgba(0,229,255,.28);border-radius:14px;
  padding:22px;overflow-y:auto;box-shadow:0 0 50px rgba(0,229,255,.18),inset 0 0 30px rgba(0,229,255,.04);
  backdrop-filter:blur(8px);}
#chat::-webkit-scrollbar{width:6px;}#chat::-webkit-scrollbar-thumb{background:rgba(0,229,255,.3);border-radius:3px;}
.msg{margin:12px 0;padding:12px 16px;border-radius:10;font-size:13px;line-height:1.65;white-space:pre-wrap;word-break:break-word;}
.msg.user{background:rgba(0,150,200,.18);border-left:3px solid rgba(100,180,220,.5);}
.msg.tru{background:rgba(0,229,255,.08);border-left:3px solid var(--mc,#00e5ff);}
.msg .vd{font-size:9px;letter-spacing:2px;margin-bottom:6px;color:var(--mc,#00e5ff);opacity:.85;}
.ready{color:#88aabb;font-size:13px;line-height:1.8;}
.ready .h{color:var(--cyan);letter-spacing:2px;margin-bottom:14px;}
.sugg{display:flex;flex-direction:column;gap:6px;margin-top:10px;}
.sugg button{background:rgba(0,229,255,.06);border:1px solid rgba(0,229,255,.22);color:#cfeeff;
  text-align:left;padding:8px 12px;border-radius:8;font-family:inherit;font-size:12px;cursor:pointer;}
.sugg button:hover{background:rgba(0,229,255,.14);}
.thinking-dots{color:var(--cyan);font-size:11px;letter-spacing:2px;padding:8px 4px;}

/* input */
.inputwrap{position:absolute;bottom:36px;left:50%;transform:translateX(-50%);width:min(720px,70%);display:flex;gap:10px;}
#input{flex:1;padding:16px 22px;background:rgba(0,4,10,.78);border:1px solid var(--cyan);color:#fff;
  border-radius:50px;font-size:15px;outline:none;font-family:inherit;letter-spacing:.5px;
  box-shadow:0 0 20px rgba(0,229,255,.30),inset 0 0 20px rgba(0,229,255,.06);}
#send{padding:0 34px;background:var(--cyan);color:#001018;border:none;border-radius:50px;
  font-weight:bold;cursor:pointer;font-family:inherit;letter-spacing:2px;font-size:13;
  box-shadow:0 0 24px rgba(0,229,255,.6);}
#send:disabled{background:#002a36;color:#446;box-shadow:none;cursor:default;}
#status{position:absolute;bottom:22px;left:42px;color:var(--cyan);font-size:12px;letter-spacing:1.5px;text-shadow:0 0 10px var(--cyan);}
.dl{position:absolute;bottom:92px;left:50%;transform:translateX(-50%);}
.note{position:absolute;top:74px;left:44%;color:rgba(0,229,255,.4);font-size:10px;letter-spacing:1px;}
@media(max-width:760px){
  #stage{width:100%;height:42%;bottom:auto;}
  #holo{width:min(38vw,300px);}
  #chat{left:18px;right:18px;width:auto;top:auto;bottom:120px;height:40vh;}
  .legend,.h-sub{display:none;}
}
</style>
</head>
<body>
<div id="stage"><div class="scan"></div><div id="holo">
  <div class="layer l-standby"></div>
  <div class="layer l-mirror"></div>
  <div class="layer l-wizard"></div>
  <div class="layer l-tribunal"></div>
  <div class="layer l-immune"></div>
  <div class="layer l-rock"></div>
</div></div>

<div class="h-title">TRU • Holographic Sovereign</div>
<div class="h-sub" id="sub">offline • sovereign • zero network</div>
<div class="legend"><div>Rock</div><div>Immune</div><div>Tribunal</div><div>Wizard</div><div>Mirror</div><div>Standby</div></div>
<div class="note" id="note"></div>

<div class="topbar">
  <span class="badge" id="badge">REASON</span>
  <button class="btn" id="voiceBtn">🔊 VOICE</button>
</div>

<div id="chat"></div>

<div class="inputwrap">
  <input id="input" placeholder="Speak to me..." autocomplete="off" autofocus>
  <button id="send" disabled>SEND</button>
</div>
<div id="status">● BOOTING • WARMING BRAIN…</div>

<script>
const BRAIN = __BRAIN__;
const KJV = __KJV__;
// ── verdict palette (mirror live /tru) ──
const VERDICT={TRUTH:"#d8a657",SCRIPTURE:"#b388ff",REASON:"#00e5ff",MEMORY:"#69f0ae",GAP:"#ff5252",UNKNOWN:"#888888"};
const VNAME={TRUTH:"TRUTH",SCRIPTURE:"SCRIPTURE",REASON:"REASON",MEMORY:"MEMORY",GAP:"GAP",UNKNOWN:"UNKNOWN"};
const CYAN="#00e5ff";

const STOP=new Set("the a an and or but if then to of in on for with from by as at is are was were be been being i me my you your we us our they them it this that those these what why how who when where should would could can do does did about into over under again give tell show explain define say said".split(" "));
const TRUTH_WORDS=["fact","facts","true","truth","real","actual","verify","verified","prove","evidence","source","sources","primary","primaries","corroborate","corroboration"];

const SMALL={hi:"hello. i'm tru — sovereign offline engine. ask a real question and i'll ground it.",hello:"hello. i'm tru — sovereign offline engine. ask a real question and i'll ground it.",hey:"hey. tru here. scripture or brain — what do you want to weigh?",yo:"yo. tru here. ask me a real question.",thanks:"received. stay sharp.","thank you":"received. stay sharp.",bye:"exit clear. the brain holds.",goodbye:"exit clear. the brain holds."};
const SELF={"who are you":"i'm tru — a sovereign offline intelligence. no cloud calls, no telemetry. brain + kjv, local route.","what are you":"i'm tru — a sovereign offline engine. brain + kjv.","what is tru":"tru is a recursive consciousness engine. a 30k-node brain and the kjv, all local.","how are you":"sovereign. brain warm.","how do you work":"locally. i tokenize, score against scripture and the brain, and return a verdict.","what can you do":"ground answers in scripture and search the brain. fully offline.","what is truth":"i treat truth as scripture + brain confirming. one source = reason, not truth.","are you ai":"i'm a sovereign engine. not a corporate assistant."};
const DOCTRINE={"who is jesus":"jesus is the christ — the son of god, the word made flesh, god come near to save. he was crucified for sin, died, and rose again. he is lord, saviour, and judge. (john 1:1,14; john 3:16; rom 1:4)","who is god":"god is the one creator — spirit, eternal, holy, just, and merciful. he is father, son, and holy spirit. (gen 1:1; deut 6:4; john 4:24)","what is the gospel":"the gospel: christ died for our sins, was buried, and rose again on the third day, that whoever believes in him has eternal life. (1 cor 15:3-4; john 3:16)","what is grace":"grace is god's unmerited favour — salvation given freely, not earned. (eph 2:8-9; titus 2:11)","what is faith":"faith is trusting god — the substance of things hoped for, the evidence of things not seen. (heb 11:1)","what is sin":"sin is falling short of god's standard — lawlessness, rebellion against god. (rom 3:23; 1 john 3:4)","who is the holy spirit":"the holy spirit is god present — the comforter, the spirit of truth, who convicts, regenerates, and empowers. (john 14:26; acts 1:8)","what is the holy spirit":"the holy spirit is god present — the comforter, the spirit of truth, who convicts, regenerates, and empowers. (john 14:26; acts 1:8)","what is salvation":"salvation is deliverance from sin and death through christ — by grace, through faith. (eph 2:8-9; rom 10:9)","what is love":"god is love. love is willing the good of the other — shown at the cross. (1 john 4:8; john 3:16)","what is the soul":"the soul is the living self — the breath of life in man, that belongs to god. (gen 2:7; matt 10:28)","what is mercy":"mercy is god not giving us the judgement we deserve — his compassion toward the guilty. (eph 2:4-5; micah 6:8)","who wrote the bible":"holy men of god spoke as they were moved by the holy ghost. many human authors, one divine author. (2 pet 1:21)","what is repentance":"repentance is turning — a change of mind and direction, turning from sin to god. (acts 3:19; luke 13:3)"};
function doctrine(q){const k=q.toLowerCase().trim().replace(/[!.?,]+$/,"");if(DOCTRINE[k])return DOCTRINE[k];for(const key in DOCTRINE){if(k===key||k.startsWith(key+" ")||k.indexOf(key)>=0)return DOCTRINE[key];}return null;}

// ── KJV map ──
const KJV_MAP=new Map();
for(const v of KJV) KJV_MAP.set(v.ref.toLowerCase(),v.text);

// ── brain inverted index ──
let BRAIN_IDX=null;
function tokenize(text){
  return text.toLowerCase().replace(/[^a-z0-9\s]/g," ").split(/\s+/).filter(t=>t.length>1 && !STOP.has(t));
}
function buildIndex(){
  BRAIN_IDX={};
  for(let i=0;i<BRAIN.length;i++){
    const node=BRAIN[i];
    const seen=new Set();
    for(const tok of tokenize((node.k||"")+" "+(node.v||""))){
      if(seen.has(tok))continue; seen.add(tok);
      (BRAIN_IDX[tok]=BRAIN_IDX[tok]||[]).push(i);
    }
  }
}
function parseVerse(q){
  const m=q.toLowerCase().match(/\b((?:[1-3]\s*)?[a-z]+)\s+(\d+)(?::(\d+))?\b/);
  if(!m)return null;
  const raw=m[1].replace(/\s/g,"");
  const long=BOOK[raw]; if(!long)return null;
  const ch=m[2],vs=m[3];
  if(vs){const key=`${long} ${ch}:${vs}`;if(KJV_MAP.has(key))return{ref:key,text:KJV_MAP.get(key)};return null;}
  const key=`${long} ${ch}:1`;if(KJV_MAP.has(key))return{ref:key,text:KJV_MAP.get(key)};return null;
}
function retrieveBrain(q,limit=6,exclude){
  if(!BRAIN_IDX)buildIndex();
  const toks=tokenize(q); if(!toks.length)return [];
  const scores={};
  for(const tok of toks) for(const i of (BRAIN_IDX[tok]||[])){
    const node=BRAIN[i]; if(exclude&&exclude.has(node.k))continue;
    scores[i]=(scores[i]||0)+1;
  }
  return Object.entries(scores).sort((a,b)=>b[1]-a[1]).slice(0,limit).map(([i,s])=>({node:BRAIN[i],score:s*0.7}));
}
function smallTalk(q){
  const k=q.toLowerCase().trim().replace(/[!.?,]+$/,"");
  if(SMALL[k])return SMALL[k];
  if(SELF[k])return SELF[k];
  for(const key in SELF) if(k.indexOf(key)>=0) return SELF[key];
  for(const key in SMALL) if(k===key||k.startsWith(key+" ")||k.endsWith(" "+key)) return SMALL[key];
  return null;
}
function decide(q,scripture,nodes){
  const ql=q.toLowerCase();
  if(scripture)return"SCRIPTURE";
  if(nodes)return nodes[0].score>0.9?"TRUTH":"REASON";
  if(TRUTH_WORDS.some(w=>ql.indexOf(w)>=0))return"GAP";
  return"REASON";
}
function finishThought(text,max){
  if(text.length<=max)return text;
  const slice=text.slice(0,max);
  const m=slice.match(/.*[.!?;]/);
  if(m&&m[0].length>max*0.4)return m[0];
  const li=slice.lastIndexOf(" ");
  return li>max*0.5?slice.slice(0,li):slice;
}
function answer(q,scripture,nodes,small,fu){
  if(small)return small;
  if(scripture)return `${scripture.ref} — ${scripture.text}`;
  if(nodes){
    let txt=nodes[0].node.v||"";
    if(txt.length<220&&nodes[1])txt+=" "+nodes[1].node.v;
    return finishThought(txt,900);
  }
  if(fu)return "that thread is spent. name a new question and i'll weigh it.";
  return "i do not have a grounded node for that. teach me: remember: <term> = <your definition>.";
}
const HISTORY_KEY="tru_history_v1";
let HISTORY=[];
function loadHistory(){try{HISTORY=JSON.parse(localStorage.getItem(HISTORY_KEY)||"[]")||[];}catch(e){HISTORY=[];}}
function saveHistory(){try{localStorage.setItem(HISTORY_KEY,JSON.stringify(HISTORY.slice(-50)));}catch(e){}}
function addTurn(q,res){HISTORY.push({q,r:{reply:res.reply,verdict:res.verdict,nodes:res.nodes_used.map(n=>n.k)},ts:Date.now()});saveHistory();}
function isFollowUp(q){return /\b(further|more|go on|expand|explain that|elaborate|continue|deeper|what else|again)\b/i.test(q);}
function lastTopic(){for(let i=HISTORY.length-1;i>=0;i--){const h=HISTORY[i];if(h.r.nodes&&h.r.nodes.length)return{q:h.q,used:new Set(h.r.nodes)};}return null;}
function route(q){
  const small=smallTalk(q);
  const doc=doctrine(q);
  const scripture=parseVerse(q);
  const fu=isFollowUp(q)&&!small;
  let exclude=null,ctxQ=q;
  if(fu){const lt=lastTopic();if(lt){exclude=lt.used;ctxQ=lt.q+" "+q;}}
  const nodes=retrieveBrain(ctxQ,6,exclude);
  let verdict,reply;
  if(small){verdict="REASON";reply=small;}
  else if(doc){verdict="TRUTH";reply=doc;}
  else{verdict=decide(q,scripture,nodes);reply=answer(q,scripture,nodes,small,fu);}
  const res={reply,verdict,scripture_ref:scripture?scripture.ref:null,
    nodes_used:nodes.slice(0,4).map(n=>({k:n.node.k,w:0.7})),
    follow_up:fu};
  addTurn(q,res);
  return res;
}

// ── UI ──
const $=id=>document.getElementById(id);
const chat=$("chat"),input=$("input"),sendBtn=$("send"),badge=$("badge"),statusEl=$("status"),note=$("note"),stage=$("stage");
let voice=true, busy=false;
function setVerdict(v){
  const c=VERDICT[v]||CYAN;
  document.documentElement.style.setProperty("--vc",c);
  document.documentElement.style.setProperty("--core",c);
  badge.textContent=VNAME[v]||v; badge.style.color=c; badge.style.borderColor=c; badge.style.textShadow=`0 0 12px ${c}`;
}
function addMsg(role,text,verdict,ms){
  const d=document.createElement("div");
  d.className="msg "+role;
  if(role==="tru"&&verdict){const c=VERDICT[verdict]||CYAN;d.style.setProperty("--mc",c);
    const vd=document.createElement("div");vd.className="vd";vd.textContent=(VNAME[verdict]||verdict)+(ms?` · ${ms}ms`:"");d.appendChild(vd);}
  const t=document.createElement("div");t.textContent=text;d.appendChild(t);
  chat.appendChild(d);chat.scrollTop=chat.scrollHeight;
}
function speak(text){
  if(!voice||!("speechSynthesis"in window))return;
  try{window.speechSynthesis.cancel();}catch(e){}
  const u=new SpeechSynthesisUtterance(text.slice(0,600));
  u.rate=0.96;u.pitch=0.88;
  const vs=window.speechSynthesis.getVoices();
  const pick=vs.find(v=>/samantha|serena|karen|moira|tessa|google uk english female/i.test(v.name))||vs.find(v=>v.lang&&v.lang.startsWith("en")&&/female/i.test(v.name))||vs.find(v=>v.lang&&v.lang.startsWith("en"));
  if(pick)u.voice=pick;
  window.speechSynthesis.speak(u);
}
async function send(qOverride){
  const q=(qOverride!=null?qOverride:input.value).trim();
  if(!q||busy)return;
  input.value="";busy=true;sendBtn.disabled=true;
  addMsg("user",q);
  stage.classList.add("thinking");
  statusEl.textContent="● THINKING • "+q.slice(0,30);
  const t0=performance.now();
  // yield to UI, then route
  await new Promise(r=>setTimeout(r,30));
  let res;
  try{res=route(q);}catch(e){res={reply:"internal fault: "+e.message,verdict:"GAP"};}
  const ms=Math.round(performance.now()-t0);
  stage.classList.remove("thinking");
  setVerdict(res.verdict);
  addMsg("tru",res.reply,res.verdict,ms);
  statusEl.textContent=`● ${res.verdict} • ${ms}ms • offline`;
  speak(res.reply);
  busy=false;sendBtn.disabled=false;input.focus();
}
input.addEventListener("input",()=>{sendBtn.disabled=busy||!input.value.trim();});
input.addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();send();}});
sendBtn.addEventListener("click",()=>send());
$("voiceBtn").addEventListener("click",()=>{voice=!voice;$("voiceBtn").textContent=voice?"🔊 VOICE":"🔇 MUTED";});

// ── boot ──
function ready(){
  loadHistory();
  setVerdict("REASON");
  statusEl.textContent="● ONLINE • SIX-LAYER LATTICE • OFFLINE";
  note.textContent=`${BRAIN.length.toLocaleString()} brain nodes • ${KJV.length.toLocaleString()} verses`;
  let memHtml="";
  if(HISTORY.length){
    const last=Math.min(HISTORY.length,3);
    memHtml=`<div style="color:#d8a657;font-size:11px;letter-spacing:2px;margin:10px 0 6px">REMEMBERED • ${HISTORY.length} TURN${HISTORY.length>1?"S":""}</div>`;
    for(let i=HISTORY.length-last;i<HISTORY.length;i++){
      const h=HISTORY[i];
      memHtml+=`<div style="font-size:11px;color:#6a8;margin:3px 0"><span style="color:#7ad">you:</span> ${esc(h.q).slice(0,60)} → <span style="color:#d8a657">${h.r.verdict}</span></div>`;
    }
    memHtml+=`<div style="color:#556677;font-size:10px;margin:6px 0 10px">say "explain that further" to go deeper on the last thread.</div>`;
  }
  chat.innerHTML=`<div class="ready"><div class="h">READY.</div><div style="margin-bottom:8px">i'm tru. six layers, one signal. fully offline.</div>
    <div style="color:#9ed7ff;margin-bottom:8px">${BRAIN.length.toLocaleString()} brain nodes + ${KJV.length.toLocaleString()} kjv verses loaded locally.</div>
    ${memHtml}
    <div style="color:#557788;font-size:11px;margin-top:8px">try one ↓</div>
    <div class="sugg">
      ${["john 3:16","what is grace","who is jesus","what is the soul","logos","psalm 23"].map(q=>`<button onclick="send(${JSON.stringify(q)})">${q}</button>`).join("")}
    </div></div>`;
  sendBtn.disabled=false;
}
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
// warm index in background, but show ready immediately (index builds lazily on first brain query)
ready();
// pre-build index now so first query is instant
setTimeout(()=>{try{buildIndex();statusEl.textContent="● ONLINE • SIX-LAYER LATTICE • OFFLINE • BRAIN WARM";}catch(e){}},200);
</script>
</body>
</html>
"""

out = TEMPLATE.replace("__BRAIN__", BRAIN_JS).replace("__KJV__", KJV_JS)
OUT.write_text(out, encoding="utf-8")
print(f"wrote {OUT}")
print(f"size: {OUT.stat().st_size:,} bytes")
print(f"brain nodes: {len(BRAIN):,} | kjv verses: {len(KJV):,}")
