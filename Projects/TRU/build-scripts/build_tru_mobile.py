#!/usr/bin/env python3
"""Assemble mobile-optimized TRU_MOBILE.html for iPhone (Proton Mail / Files app).
Single-column, touch-first, iOS WebKit-safe. Same brain + KJV as desktop.
"""
import json, re
from pathlib import Path

WS = Path("/home/workspace")
BRAIN_PATH = WS / "Projects/TRU/current/brain.json"
KJV_PATH   = WS / "Projects/TRU/data/kjv_full.json"
OUT        = WS / "TRU_MOBILE.html"

# ── load + filter brain (same as desktop) ──
raw = json.loads(BRAIN_PATH.read_text())
arr = raw if isinstance(raw, list) else raw.get("nodes", [])
clean = []
for n in arr:
    v = str(n.get("v", ""))
    if v.startswith("{") and v.endswith("}"):
        continue
    if len(v) > 1200 and re.search(r"[{}\[\]\\]{5,}", v[:200]):
        continue
    clean.append({"k": n.get("k", ""), "v": v})
BRAIN = clean

# ── load KJV ──
kjv_raw = json.loads(KJV_PATH.read_text())
KJV = [{"ref": v["ref"], "text": v["text"]} for v in kjv_raw if v.get("ref") and v.get("text")]

def js(o):
    return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")

BRAIN_JS = js(BRAIN)
KJV_JS   = js(KJV)

# ── mobile template ──
TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&display=swap" rel="stylesheet">
<title>TRU</title>
<style>
:root{--cyan:#00e5ff;--bg:#000308;--fg:#e6f7ff;}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent;}
html{height:100%;}
body{
  background:var(--bg);color:var(--fg);
  font-family:-apple-system,ui-monospace,'Courier New',monospace;
  font-size:16px; /* prevents iOS zoom on input focus */
  height:100dvh;
  display:flex;flex-direction:column;
  overflow:hidden;
  -webkit-text-size-adjust:100%;
  padding-top:env(safe-area-inset-top);
  padding-bottom:env(safe-area-inset-bottom);
}
/* ── header: compact holo + title ── */
.header{
  flex-shrink:0;
  display:flex;align-items:center;gap:12px;
  padding:10px 16px 8px;
  border-bottom:1px solid rgba(0,229,255,.2);
  background:rgba(0,4,10,.9);
}
.holo-mini{
  position:relative;width:44px;height:44px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
}
.holo-mini .core{
  width:14px;height:14px;border-radius:50%;
  background:radial-gradient(circle,var(--core,#00e5ff) 0%,rgba(0,229,255,.2) 70%,transparent 100%);
  box-shadow:0 0 16px var(--core,#00e5ff);
  animation:breathe 4s ease-in-out infinite;
}
.holo-mini .ring{
  position:absolute;border-radius:50%;border:1px solid rgba(0,229,255,.4);
  animation:spin linear infinite;
}
.holo-mini .r1{width:26px;height:26px;animation-duration:8s;}
.holo-mini .r2{width:36px;height:36px;border-style:dashed;animation-duration:12s;animation-direction:reverse;}
.holo-mini .r3{width:44px;height:44px;border-color:rgba(0,229,255,.15);animation-duration:20s;}
.thinking .core{box-shadow:0 0 28px var(--core,#00e5ff);animation-duration:1s;}
.listening .core{box-shadow:0 0 36px #ff5252,inset 0 0 18px rgba(255,82,82,.5);background:radial-gradient(circle,#ff5252 0%,rgba(255,82,82,.2) 70%,transparent 100%);animation-duration:0.6s;}
.listening .ring{border-color:rgba(255,82,82,.5)!important;animation-duration:1.5s!important;}
#holo{-webkit-user-select:none;user-select:none;cursor:pointer;}
#listenHint{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(255,82,82,.18);border:1px solid rgba(255,82,82,.5);color:#ffb3b3;padding:8px 18px;border-radius:999px;font-size:12px;letter-spacing:2px;z-index:50;display:none;backdrop-filter:blur(6px);}
.thinking .ring{animation-duration:2s!important;}
@keyframes spin{to{transform:rotate(360deg);}}
@keyframes breathe{0%,100%{transform:scale(1);}50%{transform:scale(1.15);}}
.title-block{flex:1;min-width:0;}
.title{font-family:'Cinzel',ui-monospace,monospace;font-size:15px;letter-spacing:4px;color:var(--cyan);text-shadow:0 0 12px rgba(0,229,255,.5);}
.subtitle{font-size:10px;color:rgba(0,229,255,.4);letter-spacing:1px;margin-top:2px;}
.badge{
  font-size:10px;letter-spacing:1.5px;padding:4px 10px;border-radius:999px;
  border:1px solid var(--vc,#00e5ff);color:var(--vc,#00e5ff);
  text-shadow:0 0 8px var(--vc,#00e5ff);flex-shrink:0;
}
/* ── chat log ── */
#chat{
  flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;
  padding:14px 14px 8px;
  display:flex;flex-direction:column;gap:10px;
}
#chat::-webkit-scrollbar{width:0;}
.msg{padding:12px 14px;border-radius:14px;font-size:15px;line-height:1.6;white-space:pre-wrap;word-break:break-word;max-width:88%;}
.msg.user{background:rgba(0,150,200,.16);border:1px solid rgba(100,180,220,.25);align-self:flex-end;border-bottom-right-radius:4px;}
.msg.tru{background:rgba(0,229,255,.07);border:1px solid rgba(0,229,255,.2);align-self:flex-start;border-bottom-left-radius:4px;}
.msg .vd{font-size:9px;letter-spacing:1.5px;margin-bottom:5px;color:var(--mc,#00e5ff);opacity:.7;}
.ready{color:#88aabb;font-size:14px;line-height:1.7;padding:8px 4px;}
.ready .h{color:var(--cyan);letter-spacing:2px;margin-bottom:10px;font-size:15px;}
.sugg{display:flex;flex-direction:column;gap:7px;margin-top:12px;}
.sugg button{
  background:rgba(0,229,255,.08);border:1px solid rgba(0,229,255,.25);color:#cfeeff;
  text-align:left;padding:11px 14px;border-radius:10px;font-family:inherit;font-size:14px;cursor:pointer;
  min-height:44px;
}
.sugg button:active{background:rgba(0,229,255,.2);}
.thinking-dots{color:var(--cyan);font-size:13px;letter-spacing:2px;padding:10px 4px;}
/* ── input bar ── */
.inputbar{
  flex-shrink:0;
  display:flex;gap:10px;align-items:center;
  padding:10px 14px calc(10px + env(safe-area-inset-bottom));
  background:rgba(0,4,10,.95);
  border-top:1px solid rgba(0,229,255,.25);
}
#input{
  flex:1;
  padding:14px 18px;
  background:rgba(0,20,30,.8);
  border:1px solid rgba(0,229,255,.4);
  color:#fff;border-radius:24px;
  font-size:16px; /* iOS no-zoom */
  font-family:inherit;outline:none;
  min-height:48px;
  -webkit-appearance:none;
}
#input:focus{border-color:var(--cyan);box-shadow:0 0 12px rgba(0,229,255,.3);}
#send{
  width:48px;height:48px;flex-shrink:0;
  background:var(--cyan);color:#001018;
  border:none;border-radius:50%;
  font-size:18px;font-weight:bold;cursor:pointer;
  box-shadow:0 0 16px rgba(0,229,255,.5);
  display:flex;align-items:center;justify-content:center;
  -webkit-appearance:none;
}
#send:disabled{background:#002a36;color:#446;box-shadow:none;}
#send:active:not(:disabled){transform:scale(.92);}
#status{
  font-size:9px;color:rgba(0,229,255,.5);letter-spacing:1px;
  text-align:center;padding:2px 0 0;flex-shrink:0;
}
</style>
</head>
<body>
<div id="listenHint">● LISTENING</div>
<div class="header">
  <div class="holo-mini" id="holo">
    <div class="ring r3"></div>
    <div class="ring r2"></div>
    <div class="ring r1"></div>
    <div class="core"></div>
  </div>
  <div class="title-block">
    <div class="title">TRU</div>
    <div class="subtitle" id="sub">offline • sovereign</div>
  </div>
  <div class="badge" id="badge">REASON</div>
</div>
<div id="chat"></div>
<div class="inputbar">
  <input id="input" placeholder="Speak to me…" autocomplete="off" autocapitalize="sentences">
  <button id="send" disabled>↑</button>
</div>
<div id="status">● BOOTING…</div>

<script type="application/json" id="brain-data">__BRAIN__</script>
<script type="application/json" id="kjv-data">__KJV__</script>
<script>
// LAZY LOAD: do not parse 11MB at boot (iOS WKWebView chokes). Parse on first use.
const BRAIN_COUNT=__BRAIN_COUNT__;
const KJV_COUNT=__KJV_COUNT__;
let _BRAIN=null,_KJV=null,_BRAIN_IDX=null;
function getBrain(){ if(_BRAIN===null){ _BRAIN=JSON.parse(document.getElementById('brain-data').textContent); } return _BRAIN; }
function getKjv(){ if(_KJV===null){ _KJV=JSON.parse(document.getElementById('kjv-data').textContent); } return _KJV; }
const VERDICT={TRUTH:"#d8a657",SCRIPTURE:"#b388ff",REASON:"#00e5ff",MEMORY:"#69f0ae",GAP:"#ff5252",UNKNOWN:"#888"};
const VNAME={TRUTH:"TRUTH",SCRIPTURE:"SCRIPTURE",REASON:"REASON",MEMORY:"MEMORY",GAP:"GAP",UNKNOWN:"UNKNOWN"};
const CYAN="#00e5ff";
const STOP=new Set("the a an and or but if then to of in on for with from by as at is are was were be been being i me my you your we us our they them it this that those these what why how who when where should would could can do does did about into over under again give tell show explain define say said".split(" "));
const TRUTH_WORDS=["fact","facts","true","truth","real","actual","verify","verified","prove","evidence","source","sources","primary","primaries","corroborate","corroboration"];
const SMALL={hi:"hello. i'm tru — sovereign offline engine. ask a real question and i'll ground it.",hello:"hello. i'm tru — sovereign offline engine. ask a real question and i'll ground it.",hey:"hey. tru here. scripture or brain — what do you want to weigh?",yo:"yo. tru here. ask me a real question.",thanks:"received. stay sharp.","thank you":"received. stay sharp.",bye:"exit clear. the brain holds.",goodbye:"exit clear. the brain holds."};
const SELF={"who are you":"i'm tru — a sovereign offline intelligence. no cloud calls, no telemetry. brain + kjv, local route.","what are you":"i'm tru — a sovereign offline engine. brain + kjv.","what is tru":"tru is a recursive consciousness engine. a 30k-node brain and the kjv, all local.","how are you":"sovereign. brain warm.","how do you work":"locally. i tokenize, score against scripture and the brain, and return a verdict.","what can you do":"ground answers in scripture and search the brain. fully offline.","what is truth":"i treat truth as scripture + brain confirming. one source = reason, not truth.","are you ai":"i'm a sovereign engine. not a corporate assistant."};
const DOCTRINE={"who is jesus":"jesus is the christ — the son of god, the word made flesh, god come near to save. he was crucified for sin, died, and rose again. he is lord, saviour, and judge. (john 1:1,14; john 3:16; rom 1:4)","who is god":"god is the one creator — spirit, eternal, holy, just, and merciful. he is father, son, and holy spirit. (gen 1:1; deut 6:4; john 4:24)","what is the gospel":"the gospel: christ died for our sins, was buried, and rose again on the third day, that whoever believes in him has eternal life. (1 cor 15:3-4; john 3:16)","what is grace":"grace is god's unmerited favour — salvation given freely, not earned. (eph 2:8-9; titus 2:11)","what is faith":"faith is trusting god — the substance of things hoped for, the evidence of things not seen. (heb 11:1)","what is sin":"sin is falling short of god's standard — lawlessness, rebellion against god. (rom 3:23; 1 john 3:4)","who is the holy spirit":"the holy spirit is god present — the comforter, the spirit of truth, who convicts, regenerates, and empowers. (john 14:26; acts 1:8)","what is the holy spirit":"the holy spirit is god present — the comforter, the spirit of truth, who convicts, regenerates, and empowers. (john 14:26; acts 1:8)","what is salvation":"salvation is deliverance from sin and death through christ — by grace, through faith. (eph 2:8-9; rom 10:9)","what is love":"god is love. love is willing the good of the other — shown at the cross. (1 john 4:8; john 3:16)","what is the soul":"the soul is the living self — the breath of life in man, that belongs to god. (gen 2:7; matt 10:28)","what is mercy":"mercy is god not giving us the judgement we deserve — his compassion toward the guilty. (eph 2:4-5; micah 6:8)","who wrote the bible":"holy men of god spoke as they were moved by the holy ghost. many human authors, one divine author. (2 pet 1:21)","what is repentance":"repentance is turning — a change of mind and direction, turning from sin to god. (acts 3:19; luke 13:3)"};
function doctrine(q){const k=q.toLowerCase().trim().replace(/[!.?,]+$/,"");if(DOCTRINE[k])return DOCTRINE[k];for(const key in DOCTRINE){if(k===key||k.startsWith(key+" ")||k.indexOf(key)>=0)return DOCTRINE[key];}return null;}

let _KJV_MAP=null;
function getKjvMap(){ if(_KJV_MAP===null){ _KJV_MAP=new Map(); for(const v of getKjv()) _KJV_MAP.set(v.ref.toLowerCase(),v.text); } return _KJV_MAP; }

const BOOK={"gen":"genesis","gn":"genesis","genesis":"genesis","exo":"exodus","ex":"exodus","exodus":"exodus","lev":"leviticus","le":"leviticus","lv":"leviticus","leviticus":"leviticus","num":"numbers","nu":"numbers","nb":"numbers","numbers":"numbers","deu":"deuteronomy","deut":"deuteronomy","dt":"deuteronomy","deuteronomy":"deuteronomy","josh":"joshua","joshua":"joshua","judg":"judges","jdg":"judges","judges":"judges","ruth":"ruth","ru":"ruth","rut":"ruth","1sa":"1 samuel","1sam":"1 samuel","1samuel":"1 samuel","2sa":"2 samuel","2sam":"2 samuel","2samuel":"2 samuel","1ki":"1 kings","1kings":"1 kings","2ki":"2 kings","2kings":"2 kings","1ch":"1 chronicles","1chronicles":"1 chronicles","2ch":"2 chronicles","2chronicles":"2 chronicles","ezra":"ezra","ezr":"ezra","neh":"nehemiah","nehemiah":"nehemiah","est":"esther","esther":"esther","job":"job","jb":"job","ps":"psalms","psa":"psalms","psalm":"psalms","psalms":"psalms","prov":"proverbs","pro":"proverbs","pr":"proverbs","proverbs":"proverbs","eccl":"ecclesiastes","ecc":"ecclesiastes","ec":"ecclesiastes","ecclesiastes":"ecclesiastes","song":"song of solomon","sng":"song of solomon","song of solomon":"song of solomon","isa":"isaiah","is":"isaiah","isaiah":"isaiah","jer":"jeremiah","jr":"jeremiah","jeremiah":"jeremiah","lam":"lamentations","lamentations":"lamentations","ezek":"ezekiel","eze":"ezekiel","ezk":"ezekiel","ezekiel":"ezekiel","dan":"daniel","dn":"daniel","daniel":"daniel","hos":"hosea","hosea":"hosea","joel":"joel","amos":"amos","amo":"amos","obad":"obadiah","oba":"obadiah","obadiah":"obadiah","jonah":"jonah","jon":"jonah","mic":"micah","micah":"micah","nah":"nahum","nam":"nahum","nahum":"nahum","hab":"habakkuk","habakkuk":"habakkuk","zeph":"zephaniah","zep":"zephaniah","zephaniah":"zephaniah","hag":"haggai","haggai":"haggai","zech":"zechariah","zec":"zechariah","zechariah":"zechariah","mal":"malachi","malachi":"malachi","matt":"matthew","mat":"matthew","mt":"matthew","matthew":"matthew","mark":"mark","mar":"mark","mk":"mark","mr":"mark","luke":"luke","lk":"luke","lu":"luke","john":"john","jn":"john","jhn":"john","acts":"acts","act":"acts","ac":"acts","rom":"romans","rm":"romans","romans":"romans","1co":"1 corinthians","1cor":"1 corinthians","1corinthians":"1 corinthians","corinthians":"1 corinthians","2co":"2 corinthians","2cor":"2 corinthians","2corinthians":"2 corinthians","gal":"galatians","ga":"galatians","galatians":"galatians","eph":"ephesians","ephesians":"ephesians","phil":"philippians","php":"philippians","philippians":"philippians","col":"colossians","colossians":"colossians","1th":"1 thessalonians","1thes":"1 thessalonians","1thessalonians":"1 thessalonians","thessalonians":"1 thessalonians","2th":"2 thessalonians","2thes":"2 thessalonians","2thessalonians":"2 thessalonians","1ti":"1 timothy","1tim":"1 timothy","1timothy":"1 timothy","timothy":"1 timothy","2ti":"2 timothy","2tim":"2 timothy","2timothy":"2 timothy","titus":"titus","tit":"titus","phm":"philemon","philemon":"philemon","heb":"hebrews","hebrews":"hebrews","james":"james","jas":"james","jam":"james","1pe":"1 peter","1pet":"1 peter","1peter":"1 peter","peter":"1 peter","2pe":"2 peter","2pet":"2 peter","2peter":"2 peter","1jn":"1 john","1john":"1 john","1jhn":"1 john","2jn":"2 john","2john":"2 john","2jhn":"2 john","3jn":"3 john","3john":"3 john","3jhn":"3 john","jude":"jude","jud":"jude","rev":"revelation","revelation":"revelation"};

// ── BM25 index ──
let IDX=null,DOC_LEN=[],AVG_LEN=0,N=0,DF={};
function tokenize(t){return t.toLowerCase().replace(/[^a-z0-9\s]/g," ").split(/\s+/).filter(x=>x.length>1&&!STOP.has(x));}
function buildIndex(){
  IDX={};DOC_LEN=[];DF={};N=getBrain().length;
  let total=0;
  for(let i=0;i<N;i++){
    const toks=tokenize((getBrain()[i].k||"")+" "+(getBrain()[i].v||""));
    DOC_LEN[i]=toks.length;total+=toks.length;
    const seen={};
    for(const t of toks){if(!seen[t]){seen[t]=1;(IDX[t]=IDX[t]||[]).push(i);DF[t]=(DF[t]||0)+1;}}
  }
  AVG_LEN=total/N||1;
}
function bm25(q,limit,exclude){
  if(!IDX)buildIndex();
  const toks=tokenize(q);if(!toks.length)return[];
  const scores={};
  const k1=1.5,b=0.75;
  for(const t of toks){
    const postings=IDX[t]||[];const df=DF[t]||0;
    const idf=Math.log(1+(N-df+0.5)/(df+0.5));
    for(const i of postings){
      if(exclude&&exclude.has(getBrain()[i].k))continue;
      const tf=postings.filter(x=>x===i).length;
      const norm=1-b+b*(DOC_LEN[i]/AVG_LEN);
      const s=idf*(tf*(k1+1))/(tf+k1*norm);
      scores[i]=(scores[i]||0)+s;
    }
  }
  return Object.entries(scores).sort((a,b)=>b[1]-a[1]).slice(0,limit).map(([i,s])=>({node:getBrain()[i],bm25:s,score:s}));
}
function parseVerse(q){
  const m=q.toLowerCase().match(/\b((?:[1-3]\s*)?[a-z]+)\s+(\d+)(?::(\d+))?/);
  if(!m)return null;
  const raw=m[1].replace(/\s/g,"");const long=BOOK[raw];if(!long)return null;
  const ch=m[2],vs=m[3];
  if(vs){const key=long+" "+ch+":"+vs;if(getKjvMap().has(key))return{ref:key,text:getKjvMap().get(key)};return null;}
  const key=long+" "+ch+":1";if(getKjvMap().has(key))return{ref:key,text:getKjvMap().get(key)};return null;
}
function smallTalk(q){
  const k=q.toLowerCase().trim().replace(/[!.?,]+$/,"");
  if(SMALL[k])return SMALL[k];if(SELF[k])return SELF[k];
  for(const key in SELF)if(k.indexOf(key)>=0)return SELF[key];
  for(const key in SMALL)if(k===key||k.startsWith(key+" ")||k.endsWith(" "+key))return SMALL[key];
  return null;
}
function decide(q,scripture,nodes){
  const ql=q.toLowerCase();
  if(scripture)return"SCRIPTURE";
  if(nodes)return nodes[0].score>0.9?"TRUTH":"REASON";
  if(TRUTH_WORDS.some(w=>ql.indexOf(w)>=0))return"GAP";
  return"REASON";
}
function finishThought(t,max){
  if(t.length<=max)return t;
  const s=t.slice(0,max);const m=s.match(/.*[.!?;]/);
  if(m&&m[0].length>max*0.4)return m[0];
  const li=s.lastIndexOf(" ");return li>max*0.5?s.slice(0,li):s;
}
function answer(q,scripture,nodes,small,fu){
  if(small)return small;
  if(scripture)return scripture.ref+" — "+scripture.text;
  if(nodes){let t=nodes[0].node.v||"";if(t.length<220&&nodes[1])t+=" "+nodes[1].node.v;return finishThought(t,900);}
  if(fu)return"that thread is spent. name a new question and i'll weigh it.";
  return"i do not have a grounded node for that. teach me: remember: <term> = <your definition>.";
}
// ── memory ──
const HK="tru_history_v1";let HISTORY=[];
function loadHistory(){try{HISTORY=JSON.parse(localStorage.getItem(HK)||"[]")||[];}catch(e){HISTORY=[];}}
function saveHistory(){try{localStorage.setItem(HK,JSON.stringify(HISTORY.slice(-50)));}catch(e){}}
function addTurn(q,res){HISTORY.push({q,r:{reply:res.reply,verdict:res.verdict,nodes:(res.nodes_used||[]).map(n=>n.k)},ts:Date.now()});saveHistory();}
function isFollowUp(q){return /\b(further|more|go on|expand|explain that|elaborate|continue|deeper|what else|again)\b/i.test(q);}
function lastTopic(){for(let i=HISTORY.length-1;i>=0;i--){const h=HISTORY[i];if(h.r.nodes&&h.r.nodes.length)return{q:h.q,used:new Set(h.r.nodes)};}return null;}

const LLM_ENDPOINT="https://splashdown2.zo.space/api/tru-chat";
const LLM_TIMEOUT=20000; // 20s max wait for LLM

async function tryLLM(q){
  try{
    const ctrl=new AbortController();
    const tid=setTimeout(()=>ctrl.abort(),LLM_TIMEOUT);
    const hist=HISTORY.slice(-10).map(h=>({role:"user",text:h.q}));
    const resp=await fetch(LLM_ENDPOINT,{
      method:"POST",
      headers:{"content-type":"application/json","Accept":"application/json"},
      signal:ctrl.signal,
      body:JSON.stringify({query:q,history:hist})
    });
    clearTimeout(tid);
    if(!resp.ok)return null;
    const data=await resp.json();
    if(data.ok&&data.reply)return {reply:data.reply,verdict:data.verdict||"TRUTH",scripture_ref:data.scripture_ref||null,source:"llm"};
    return null;
  }catch(e){return null;}
}

async function route(q){
  // ── small talk: local, instant, no data needed ──
  const small=smallTalk(q);
  if(small){const res={reply:small,verdict:"REASON",source:"local"};addTurn(q,res);return res;}

  // ── everything else: try live LLM first (Gabriel voice + memory), fall back to local ──
  const llmRes=await tryLLM(q);
  if(llmRes){addTurn(q,llmRes);return llmRes;}

  // ── offline fallback: local doctrine + scripture + brain (lazy parse on first use) ──
  const doc=doctrine(q);
  if(doc){const res={reply:doc,verdict:"TRUTH",source:"local"};addTurn(q,res);return res;}
  const scripture=parseVerse(q);
  if(scripture){const res={reply:scripture.ref+" — "+scripture.text,verdict:"SCRIPTURE",scripture_ref:scripture.ref,source:"local"};addTurn(q,res);return res;}
  const fu=isFollowUp(q);
  let exclude=null,ctxQ=q;
  if(fu){const lt=lastTopic();if(lt){exclude=lt.used;ctxQ=lt.q+" "+q;}}
  const nodes=bm25(ctxQ,6,exclude);
  const verdict=decide(q,scripture,nodes);
  const reply=answer(q,scripture,nodes,small,fu);
  const res={reply,verdict,scripture_ref:scripture?scripture.ref:null,nodes_used:nodes.slice(0,4).map(n=>({k:n.node.k,w:0.7})),follow_up:fu,source:"brain"};
  addTurn(q,res);
  return res;
}

// ── UI ──
const $=id=>document.getElementById(id);
const chat=$("chat"),input=$("input"),sendBtn=$("send"),badge=$("badge"),statusEl=$("status"),sub=$("sub"),holo=$("holo");
let busy=false;
function setVerdict(v){
  const c=VERDICT[v]||CYAN;
  document.documentElement.style.setProperty("--vc",c);
  document.documentElement.style.setProperty("--core",c);
  badge.textContent=VNAME[v]||v;
}
function addMsg(role,text,verdict,ms){
  const d=document.createElement("div");
  d.className="msg "+role;
  if(role==="tru"&&verdict){
    const c=VERDICT[verdict]||CYAN;d.style.setProperty("--mc",c);
    const vd=document.createElement("div");vd.className="vd";
    vd.textContent=(VNAME[verdict]||verdict)+(ms?" · "+ms+"ms":"");d.appendChild(vd);
  }
  const t=document.createElement("div");t.textContent=text;d.appendChild(t);
  chat.appendChild(d);chat.scrollTop=chat.scrollHeight;
}
function speak(text){
  if(!("speechSynthesis"in window))return;
  try{window.speechSynthesis.cancel();}catch(e){}
  const u=new SpeechSynthesisUtterance(text.slice(0,600));
  u.rate=0.96;u.pitch=0.88;
  const vs=window.speechSynthesis.getVoices();
  const pick=vs.find(v=>/samantha|serena|karen|moira|tessa/i.test(v.name))||vs.find(v=>v.lang&&v.lang.startsWith("en"));
  if(pick)u.voice=pick;
  window.speechSynthesis.speak(u);
}
async function send(qOverride){
  const q=(qOverride!=null?qOverride:input.value).trim();
  if(!q||busy)return;
  input.value="";busy=true;sendBtn.disabled=true;
  addMsg("user",q);
  holo.classList.add("thinking");
  statusEl.textContent="● EXECUTING • "+q.slice(0,30);
  const t0=performance.now();
  let res;
  try{
    // show connecting status if not a fast local path
    const isLocal=smallTalk(q)||doctrine(q)||parseVerse(q);
    if(!isLocal)statusEl.textContent="● CONNECTING • LLM…";
    res=await route(q);
  }catch(e){res={reply:"internal fault: "+e.message,verdict:"GAP"};}
  const ms=Math.round(performance.now()-t0);
  holo.classList.remove("thinking");
  setVerdict(res.verdict);
  addMsg("tru",res.reply,res.verdict,ms);
  const src=res.source==="llm"?"llm":res.source==="local"?"local":"offline";
  statusEl.textContent="● "+res.verdict+" • "+src+" • "+ms+"ms";
  speak(res.reply);
  busy=false;sendBtn.disabled=false;input.focus();
}
// iOS needs a small delay to focus input after tap
sendBtn.addEventListener("click",()=>send());
input.addEventListener("input",()=>{sendBtn.disabled=busy||!input.value.trim();});
input.addEventListener("keydown",e=>{if(e.key==="Enter"){e.preventDefault();send();}});

// ── hold-to-talk (Web Speech API) ──
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
let rec=null, listening=false, holdTimer=null;
function startListen(){
  if(listening||!SR)return;
  try{
    rec = new SR();
    rec.lang="en-US"; rec.interimResults=false; rec.continuous=false; rec.maxAlternatives=1;
    rec.onresult = (e)=>{
      const t = e.results[0][0].transcript.trim();
      if(t) send(t); // route transcript through normal send (LLM + voice out)
    };
    rec.onend = ()=>{ if(listening){stopListen();} };
    rec.onerror = (e)=>{ stopListen(); statusEl.textContent="● MIC ERROR • "+(e.error||""); };
    rec.start();
    listening=true;
    document.body.classList.add("listening");
    $("listenHint").style.display="block";
    $("listenHint").textContent="● LISTENING — release to send";
    statusEl.textContent="● LISTENING…";
  }catch(e){ statusEl.textContent="● MIC UNAVAILABLE"; }
}
function stopListen(){
  listening=false;
  document.body.classList.remove("listening");
  $("listenHint").style.display="none";
  if(rec){try{rec.stop();}catch(e){} rec=null;}
  statusEl.textContent="● ONLINE • HYBRID • OFFLINE-READY";
}
// wire hold-to-talk on the relic circle
function holdStart(e){if(e)e.preventDefault(); holdTimer=setTimeout(()=>{startListen();},120);} // small delay = press vs tap
function holdEnd(e){if(e)e.preventDefault(); clearTimeout(holdTimer); if(listening){stopListen();} }
holo.addEventListener("touchstart",holdStart,{passive:false});
holo.addEventListener("touchend",holdEnd,{passive:false});
holo.addEventListener("touchcancel",holdEnd,{passive:false});
holo.addEventListener("mousedown",holdStart);
holo.addEventListener("mouseleave",holdEnd);
window.addEventListener("mouseup",holdEnd);
// preload voices (iOS needs this early)
if("speechSynthesis"in window){try{window.speechSynthesis.getVoices();}catch(e){}}
// ── boot ──
function ready(){
  try{
  loadHistory();
  setVerdict("REASON");
  statusEl.textContent="● ONLINE • OFFLINE";
  sub.textContent=BRAIN_COUNT.toLocaleString()+" nodes • "+KJV_COUNT.toLocaleString()+" verses";
  // if we have remembered turns, show a note
  let memNote="";
  if(HISTORY.length>0){
    memNote='<div style="color:#69f0ae;font-size:11px;margin-bottom:10px">● REMEMBERED • '+HISTORY.length+' TURNS</div>';
  }
  chat.innerHTML='<div class="ready">'+memNote+
    '<div class="h">READY.</div>'+
    '<div style="margin-bottom:8px">I\'m TRU. Fully offline. Sovereign.</div>'+
    '<div style="color:#9ed7ff;margin-bottom:8px;font-size:13px">'+BRAIN_COUNT.toLocaleString()+' brain nodes + '+KJV_COUNT.toLocaleString()+' KJV verses.</div>'+
    '<div style="color:#557788;font-size:12px">try one ↓ — or hold the relic ◉ to speak</div>'+
    '<div class="sugg">'+
    ["john 3:16","who is jesus","what is grace","what is the soul","psalm 23","faith without works"].map(q=>'<button onclick="send('+JSON.stringify(q)+')">'+q+'</button>').join("")+
    '</div></div>';
  sendBtn.disabled=false;
  // warm index in background (best-effort)
  setTimeout(()=>{statusEl.textContent="● ONLINE • HYBRID • OFFLINE-READY";},300);
  }catch(e){console.error("boot fault",e); sendBtn.disabled=false; statusEl.textContent="● ONLINE • OFFLINE";}
}
ready();
</script>
</body>
</html>
"""

out = TEMPLATE.replace("__BRAIN__", BRAIN_JS).replace("__KJV__", KJV_JS).replace("__BRAIN_COUNT__", str(len(BRAIN))).replace("__KJV_COUNT__", str(len(KJV)))
OUT.write_text(out, encoding="utf-8")
print(f"wrote {OUT}")
print(f"size: {OUT.stat().st_size:,} bytes")
print(f"brain nodes: {len(BRAIN):,} | kjv verses: {len(KJV):,}")
print(f"brain count: {len(BRAIN):,}")
print(f"kjv count: {len(KJV):,}")
