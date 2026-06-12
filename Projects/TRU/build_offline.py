import base64, gzip, json, re, os

with open('/home/workspace/Projects/TRU/data/brain_b64.txt') as f:
    BRAIN_B64 = f.read().strip()
with open('/home/workspace/Projects/TRU/data/ot_b64.txt') as f:
    OT_B64 = f.read().strip()
with open('/home/workspace/Projects/TRU/data/nt_b64.txt') as f:
    NT_B64 = f.read().strip()

with open('/tmp/trubrain_api.json') as f:
    nodes = json.load(f)['brain']

agents = [
    {"id":"archivist","label":"ARCHIVIST","role":"Scripture / source authority","weight":1.0},
    {"id":"exegete","label":"EXEGETE","role":"Greek / Hebrew word study","weight":1.0},
    {"id":"critic","label":"CRITIC","role":"Context / historical critique","weight":1.0},
    {"id":"architect","label":"ARCHITECT","role":"Systematic theology / structure","weight":1.0},
    {"id":"balance","label":"BALANCE","role":"Spirit of Wisdom — blind scales","weight":1.5},
]

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TRU Phase 25 — Offline Living Bible</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0a0a0f;color:#e8e8e8;font-family:'Courier New',monospace;min-height:100vh;display:flex;flex-direction:column}}
.d{{display:flex;gap:8px;flex-wrap:wrap;align-items:center}}
.hdr{{padding:14px 18px;border-bottom:1px solid #1e2530;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10}}
.logo{{display:flex;align-items:center;gap:12px}}
.orb{{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#00ffcc,#0088ff);box-shadow:0 0 20px #00ffcc55;animation:p 3s infinite}}
@keyframes p{{0%,100%{{box-shadow:0 0 20px #00ffcc44}}50%{{box-shadow:0 0 40px #00ffccaa}}}}
.ttl{{font-size:20px;font-weight:700;background:linear-gradient(90deg,#00ffcc,#0088ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.sub{{font-size:9px;color:#444;letter-spacing:2}}
.btns{{display:flex;gap:8px;flex-wrap:wrap}}
button{{cursor:pointer;font-family:inherit}}
.btn-dump{{background:#111;color:#00ffcc;border:1px solid #00ffcc33;padding:6px 12px;border-radius:6px;font-size:11}}
.btn-persona{{padding:6px 12px;border-radius:6px;font-size:11;font-weight:bold;border:1px solid}}
.modes{{padding:9px 14px;background:#12161f;border-bottom:1px solid #1e2530;display:flex;gap:6px;flex-wrap:wrap;align-items:center}}
.mode-btn{{background:#1a1f2e;color:#777;border:none;padding:7px 13px;border-radius:4px;font-weight:bold;font-size:12}}
.mode-btn.active{{background:#50fa7b;color:#000}}
.tribunal{{padding:7px 14px;background:#0f1318;border-bottom:1px solid #1e2530;display:flex;gap:5px;flex-wrap:wrap;align-items:center}}
.trib-label{{font-size:9px;color:#00ffcc;margin-right:3px;letter-spacing:1}}
.agent-tag{{font-size:9px;padding:3px 7px;border-radius:3px;background:#1a1f2e;color:#8be9fd;border:1px solid #333}}
.agent-tag.star{{color:#ffd700;border-color:#ffd70044;font-weight:bold}}
.phase-label{{margin-left:auto;font-size:9px;color:#333}}
.chat{{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10}}
.empty{{text-align:center;color:#2a2a2a;margin-top:60px;font-size:13}}
.msg-user{{align-self:flex-end;background:#1a2a1a;color:#a8e6a8;padding:9px 14px;border-radius:10px 10px 0 10px;max-width:80%;font-size:13}}
.msg-tru{{background:#0f1a1f;border:1px solid #00ffcc22;border-radius:0 10px 10px 10px;padding:12px 14px;max-width:100%}}
.verdict-bar{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}}
.vb{{font-size:10px;padding:2px 8px;border-radius:10px;font-weight:bold}}
.v-truth{{background:#50fa7b22;color:#50fa7b;border:1px solid #50fa7b55}}
.v-integ{{background:#8be9fd22;color:#8be9fd;border:1px solid #8be9fd55}}
.v-prob{{background:#ffb86c22;color:#ffb86c;border:1px solid #ffb86c55}}
.v-restr{{background:#ff555522;color:#ff5555;border:1px solid #ff555555}}
.ref-label{{font-size:9px;color:#00ffcc;margin-bottom:7px;letter-spacing:1}}
.truth-card{{margin-bottom:9px;padding-bottom:8px;border-bottom:1px solid #1a2530}}
.truth-card:last-of-type{{border-bottom:none}}
.ref{{color:#ffd700;font-size:10px}}
.vr-tag{{font-size:10px;color:#6272a4;float:right}}
.greek{{color:#a8e6ff;font-size:11px;margin-bottom:3px}}
.english{{color:#d1d7e0;font-size:12px;line-height:1.5}}
.answer{{font-size:11px;color:#444;margin-top:6px;padding-top:6px;border-top:1px solid #1a2530;line-height:1.6}}
.cite{{font-size:10px;color:#333;margin-top:3px}}
.input-bar{{padding:12px 14px;border-top:1px solid #1e2530;display:flex;gap:8px}}
input{{flex:1;background:#111;color:#00ffcc;border:1px solid #1e2530;border-radius:8px;padding:9px 13px;font-size:13;font-family:inherit;outline:none}}
input:focus{{border-color:#00ffcc44}}
.ask-btn{{background:linear-gradient(135deg,#00ffcc,#0088ff);color:#000;border:none;padding:9px 18px;border-radius:8px;font-weight:bold;font-size:13}}
.status{{margin-left:auto;font-size:10px;padding-right:6px}}
.s-ok{{color:#50fa7b}}
.s-loading{{color:#555}}
.loading{{color:#333;font-size:12px;padding:6px 0}}
</style>
</head>
<body>

<div class="hdr">
  <div class="logo">
    <div class="orb"></div>
    <div>
      <div class="ttl">TRU Phase 25</div>
      <div class="sub">OFFLINE LIVING BIBLE · <span id="nodeCount">{len(nodes)} NODES</span></div>
    </div>
  </div>
  <div class="btns">
    <button class="btn-dump" id="dumpBtn">📥 dump html</button>
    <button class="btn-persona" id="personaBtn">🧠 🟢 ON</button>
  </div>
</div>

<div class="modes">
  <button class="mode-btn active" id="btnBible" onclick="setMode('bible')">📖 Bible</button>
  <button class="mode-btn" id="btnGeneral" onclick="setMode('general')">🌐 General</button>
  <button class="mode-btn" id="btnRaw" onclick="setMode('raw')">⚡ TRU Core</button>
  <span class="status" id="status">⏳ Loading...</span>
</div>

<div class="tribunal">
  <span class="trib-label">TRIBUNAL:</span>
  <span class="agent-tag" id="tag-archivist">ARCHIVIST</span>
  <span class="agent-tag" id="tag-exegete">EXEGETE</span>
  <span class="agent-tag" id="tag-critic">CRITIC</span>
  <span class="agent-tag" id="tag-architect">ARCHITECT</span>
  <span class="agent-tag star" id="tag-balance">BALANCE ★</span>
  <span class="phase-label">DRY TRUTH · STEADY NUDGE</span>
</div>

<div class="chat" id="chat">
  <div class="empty">Ask TRU anything. Scripture. Theology. Truth.</div>
</div>

<div class="input-bar">
  <input id="input" placeholder="Ask TRU anything..." onkeydown="if(event.key==='Enter')ask()">
  <button class="ask-btn" onclick="ask()">ASK</button>
</div>

<script>
const BRAIN_B64 = `{BRAIN_B64}`;
const OT_B64 = `{OT_B64}`;
const NT_B64 = `{NT_B64}`;
const AGENTS = {json.dumps(agents, ensure_ascii=False)};

let brain = [];
let bibleOT = [];
let bibleNT = [];
let msgs = [];
let mode = 'bible';
let personaOn = true;
let hydrated = false;
let loading = false;

const STOP = new Set(['the','a','an','and','or','but','in','on','at','to','for','of','by','with','as','is','are','was','were','be','been','being','have','has','had','do','does','did','will','would','should','could','may','might','must','this','that','these','those','i','you','he','she','it','we','they','what','which','who','when','where','how','all','each','every','both','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','just','if','then','because','while','although','though','since','until','unless','about','into','through','during','before','after','above','below','between','under','again','further','once','here','there','from','up','down','out','off','over','your','my','his','her','their','our','any','said','made']);

const AGENT_KEYWORDS = {{
  archivist: ['bible','scripture','verse','psalm','genesis','john','romans','law','promise','god','lord','christ','jesus','paul','moses','israel','prophet','covenant','kingdom','book','psalms','proverbs'],
  exegete: ['word','greek','hebrew','aramaic','meaning','translate','definition','strong','lexicon'],
  critic: ['why','history','context','ancient','practice','original','custom','tradition','pagan','jewish','roman','who wrote','when written'],
  architect: ['system','doctrine','truth','logic','principle','rule','law','theology','trinity','atonement','salvation','grace','faith','definition','what is','explain'],
}};

function tokens(text) {{
  return text.toLowerCase().replace(/[^\\w\\s]/g,' ').split(/\\s+/).filter(w=>w.length>2&&!STOP.has(w));
}}

function searchBible(query) {{
  const toks = tokens(query);
  if (!toks.length) return [];
  const otR = bibleOT.map(line => {{
    const parts = line.split('||');
    const ref = parts[0]||'', en = parts[1]||'', gr = parts[2]||'';
    let s = 0;
    for (const t of toks) {{ if (en.toLowerCase().includes(t)) s++; if (gr.toLowerCase().includes(t)) s += 0.5; }}
    const redBooks = ['ps','pr','job','ss','is','jr','lm','ez','dn','ho','jl','am','ob','jn','mc','na','hb','zp','hg','zec','mal','mt','mk','lk','jn','ac','ro','ga','eph','phil','col','1th','2th','heb','jas','1pe','1jn','re'];
    for (const rb of redBooks) {{ if (ref.startsWith(rb+' ')) {{ s *= 1.3; break; }} }}
    return {{ ref, english: en, greek: gr, score: s, testament: 'ot', type: 'verse' }};
  }}).filter(r=>r.score>0).sort((a,b)=>b.score-a.score).slice(0,20);

  const ntR = bibleNT.map(line => {{
    const parts = line.split('||');
    const ref = parts[0]||'', gr = parts[1]||'';
    let s = 0;
    for (const t of toks) {{ if (gr.toLowerCase().includes(t)) s++; }}
    if (gr && toks.some(t=>gr.toLowerCase().includes(t))) s *= 1.2;
    return {{ ref, english: gr, greek: gr, score: s, testament: 'nt', type: 'verse' }};
  }}).filter(r=>r.score>0).sort((a,b)=>b.score-a.score).slice(0,20);

  return [...otR, ...ntR];
}}

function scoreNode(toks, node) {{
  let s = 0;
  for (const t of toks) if ((node.v||'').toLowerCase().includes(t)) s++;
  return s === 0 ? 0 : s * (node.w || 0.8);
}}

function searchBrain(query) {{
  const toks = tokens(query);
  return brain.map(n => ({{...n, score: scoreNode(toks, n)}}))
    .filter(n => n.score > 0)
    .sort((a,b) => b.score - a.score)
    .slice(0, 12);
}}

function getVerdict(score) {{
  if (score > 9) return 'TRUTH';
  if (score > 5) return 'INTEGRATED';
  if (score > 2.5) return 'PROBATIONARY';
  return 'RESTRICTED';
}}

function vcolor(v) {{
  return v==='TRUTH'?'#50fa7b':v==='INTEGRATED'?'#8be9fd':v==='PROBATIONARY'?'#ffb86c':'#ff5555';
}}

function agentCards(result, query) {{
  return AGENTS.map(a => {{
    let base = (result.score || 1) * a.weight;
    const kw = AGENT_KEYWORDS[a.id] || [];
    for (const k of kw) {{ if (query.toLowerCase().includes(k)) {{ base *= 1.4; break; }} }}
    if (a.id === 'exegete' && result.greek) base *= 1.3;
    if (a.id === 'balance') base *= 1.5;
    const total = AGENTS.reduce((s,ag) => {{
      let b = (result.score || 1) * ag.weight;
      for (const k of (AGENT_KEYWORDS[ag.id]||[])) {{ if (query.toLowerCase().includes(k)) {{ b *= 1.4; break; }} }}
      if (ag.id === 'exegete' && result.greek) b *= 1.3;
      if (ag.id === 'balance') b *= 1.5;
      return s + b;
    }}, 0);
    const pct = total > 0 ? Math.round((base / total) * 100) : 0;
    let statement = '';
    if (a.id === 'archivist') statement = result.ref ? `📖 Source: "${{result.ref}}" — ${{a.weight}}x` : `📖 No scripture — ${{a.weight}}x`;
    if (a.id === 'exegete') statement = result.greek ? `✦ "${{result.greek.slice(0,40)}}" — Greek confirmed` : `✦ No Greek match — neutral`;
    if (a.id === 'critic') statement = result.english ? `⚔️ Context: "${{result.english.slice(0,40)}}"` : `⚔️ Context insufficient`;
    if (a.id === 'architect') statement = result.type ? `🔺 Structure: ${{result.type}}` : `🔺 No doctrine match`;
    if (a.id === 'balance') statement = `⚖️ Spirit of Wisdom: ${{a.weight}}x weight — scales tip toward truth`;
    return {{ ...a, statement, score: base, pct }};
  }});
}}

async function ask() {{
  const input = document.getElementById('input');
  const q = input.value.trim();
  if (!q || loading) return;
  input.value = '';
  msgs.push({{ role: 'user', text: q }});
  render();
  loading = true;
  render();

  let bibleResults = [];
  let brainResults = [];

  if (mode === 'bible') {{
    bibleResults = searchBible(q);
  }} else {{
    brainResults = searchBrain(q);
  }}

  let answer = '', citation = '', verdict = 'RESTRICTED', totalScore = 0, truthCards = [];

  if (bibleResults.length > 0) {{
    const top = bibleResults[0];
    const cards = agentCards(top, q);
    totalScore = cards.reduce((a,b)=>a+b.score,0);
    verdict = getVerdict(totalScore);
    answer = top.greek ? `✦ ${{top.greek}}\\n→ ${{top.english}}` : top.english;
    citation = `${{top.ref}} · ${{verdict}} (${{totalScore.toFixed(2)}})`;
    truthCards = cards;
  }} else if (brainResults.length > 0) {{
    const top = brainResults[0];
    const cards = agentCards(top, q);
    totalScore = cards.reduce((a,b)=>a+b.score,0);
    verdict = getVerdict(totalScore);
    answer = top.v || top.text || '';
    citation = `${{top.k}} · ${{verdict}} (${{totalScore.toFixed(2)}})`;
    truthCards = cards;
  }} else {{
    answer = personaOn
      ? 'The Spirit of Wisdom moves, but the vessels are not yet aligned. Ask again with different words.'
      : `No match in ${{brain.length}} nodes. Try: grace, truth, jesus, salvation, job, trinity, faith`;
    citation = 'no match';
    verdict = 'RESTRICTED';
  }}

  msgs.push({{ role: 'tru', text: answer, citation, verdict, totalScore, truthCards, bibleResults, brainResults, mode, q }});
  loading = false;
  render();
}}

function render() {{
  const chat = document.getElementById('chat');
  if (msgs.length === 0) {{
    chat.innerHTML = '<div class="empty">Ask TRU anything. Scripture. Theology. Truth.</div>';
    return;
  }}
  chat.innerHTML = msgs.map(msg => {{
    if (msg.role === 'user') return `<div class="msg-user">${{esc(msg.text)}}</div>`;
    let html = `<div class="msg-tru">`;
    const vc = vcolor(msg.verdict);
    html += `<div class="verdict-bar">
      <span class="vb v-${{msg.verdict.toLowerCase()}}">${{msg.verdict}}</span>
      <span style="font-size:10px;color:#6272a4">score:${{(msg.totalScore||0).toFixed(2)}}</span>
    </div>`;
    if (msg.truthCards && msg.truthCards.length > 0 && msg.mode === 'bible') {{
      html += `<div style="margin-bottom:10px"><div class="ref-label">— RED LETTER TRIBUNAL —</div>`;
      msg.truthCards.forEach(c => {{
        html += `<div class="truth-card">
          <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:4px">
            <span style="color:#ffd700">${{c.label}} ★</span>
            <span style="color:${{c.weight>1?'#ffd700':'#6272a4'}}">${{c.weight}}x · ${{c.pct}}%</span>
          </div>
          <div style="font-size:11px;color:#8be9fd">${{esc(c.statement)}}</div>
        </div>`;
      }});
      if (msg.bibleResults && msg.bibleResults.length > 0) {{
        html += `<div style="margin-top:8px;font-size:9px;color:#333">${{msg.bibleResults.length}} matches in ${{bibleOT.length+bibleNT.length}} verses</div>`;
      }}
      html += `</div>`;
    }}
    if (msg.brainResults && msg.brainResults.length > 0 && msg.mode !== 'bible') {{
      html += `<div style="margin-bottom:10px"><div class="ref-label">— KNOWLEDGE MATCHES —</div>`;
      msg.brainResults.slice(0,6).forEach(r => {{
        html += `<div class="truth-card">
          <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:2px">
            <span style="color:#bd93f9">${{esc(r.k||'')}}</span>
            <span style="color:#6272a4">w:${{r.w?.toFixed(2)}}</span>
          </div>
          <div style="color:#c0c8d8;font-size:12px">${{esc((r.v||'').slice(0,100))}}</div>
        </div>`;
      }});
      html += `</div>`;
    }}
    html += `<div class="answer">${{esc(msg.text)}}</div>`;
    if (msg.citation) html += `<div class="cite">src: ${{esc(msg.citation)}}</div>`;
    html += `</div>`;
    return html;
  }}).join('');
  chat.scrollTop = chat.scrollHeight;
}}

function esc(s) {{
  if (!s) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}

function setMode(m) {{
  mode = m;
  document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('btn' + m.charAt(0).toUpperCase() + m.slice(1)).classList.add('active');
}}

document.getElementById('personaBtn').onclick = () => {{
  personaOn = !personaOn;
  const btn = document.getElementById('personaBtn');
  btn.textContent = personaOn ? '🧠 🟢 ON' : '🧠 ⚫ OFF';
  btn.style.background = personaOn ? '#00ffcc' : '#222';
  btn.style.color = personaOn ? '#000' : '#555';
  btn.style.borderColor = personaOn ? '#00ffcc' : '#444';
}};

document.getElementById('dumpBtn').onclick = () => {{
  const dump = {{
    version: 'TRU_Phase_25',
    exported: new Date().toISOString(),
    mode, personaOn,
    nodeCount: brain.length,
    messages: msgs,
    fullBrain: brain,
    bibleSample: {{ ot: bibleOT.slice(0,5), nt: bibleNT.slice(0,5) }},
    agents: AGENTS,
  }};
  const blob = new Blob([JSON.stringify(dump, null, 2)], {{type:'application/json'}});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'TRU_Phase25_' + Date.now() + '.json';
  a.click();
  URL.revokeObjectURL(url);
}};

async function init() {{
  // Load pako for decompression
  try {{
    const {{ default: pako }} = await import('https://cdn.jsdelivr.net/npm/pako@2.1.0/+esm');
    window.pako = pako;
  }} catch(e) {{ console.warn('pako load failed:', e); }}

  try {{
    if (typeof pako !== 'undefined') {{
      brain = JSON.parse(pako.ungzip(atob(BRAIN_B64), {{ to: 'string' }}));
    }} else {{
      brain = JSON.parse(atob(BRAIN_B64));
    }}
    document.getElementById('nodeCount').textContent = brain.length + ' NODES';
  }} catch(e) {{ console.error('Brain load failed:', e); }}

  try {{
    if (typeof pako !== 'undefined') {{
      bibleOT = pako.ungzip(atob(OT_B64), {{ to: 'string' }}).split('\\n').filter(l=>l.trim()&&l.includes('||'));
    }} else {{
      bibleOT = atob(OT_B64).split('\\n').filter(l=>l.trim()&&l.includes('||'));
    }}
  }} catch(e) {{ console.error('OT load failed:', e); }}

  try {{
    if (typeof pako !== 'undefined') {{
      bibleNT = pako.ungzip(atob(NT_B64), {{ to: 'string' }}).split('\\n').filter(l=>l.trim()&&l.includes('||'));
    }} else {{
      bibleNT = atob(NT_B64).split('\\n').filter(l=>l.trim()&&l.includes('||'));
    }}
  }} catch(e) {{ console.error('NT load failed:', e); }}

  if (bibleOT.length > 0) {{
    hydrated = true;
    document.getElementById('status').textContent = '✅ Bible loaded';
    document.getElementById('status').className = 'status s-ok';
  }}
  render();
}}

window.DUMP = () => {{
  return {{ brain, bibleOT, bibleNT, msgs, mode, personaOn, hydrated, nodeCount: brain.length }};
}};

init();
</script>
</body>
</html>'''

out_path = '/home/workspace/Projects/TRU/TRU_Phase25_Offline.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

size = os.path.getsize(out_path)
print(f'Done: {size} bytes ({size//1024}KB)')
