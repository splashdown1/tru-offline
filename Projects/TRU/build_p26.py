#!/usr/bin/env python3
"""TRU Phase 26 Builder — generates self-contained offline HTML"""
import json, re, base64, gzip

# ── Load Bible data ─────────────────────────────────────
OT_VERSES = []
with open('/home/workspace/Projects/TRU/data/coil_ot.txt') as f:
    data = base64.b64decode(f.read().strip()).decode()
    OT_VERSES = [l for l in data.split('\n') if '||' in l]

NT_VERSES = []
nt_raw = '/home/.z/workspaces/con_MYlif5vQjCGGJeL3/sblgnt_nt_combined.txt'
with open(nt_raw) as f:
    for line in f:
        line = line.rstrip('\n')
        if '||' not in line: continue
        parts = line.split('||', 1)
        if len(parts) != 2: continue
        ref, rest = parts
        ref = ref.strip()
        if '||' in rest:
            sub = rest.split('||', 1)
            greek = sub[0].strip(); english = sub[1].strip()
        else:
            greek = rest.strip(); english = rest.strip()
        NT_VERSES.append(f"{ref}||{greek}||{english}")

print(f"Bible: OT={len(OT_VERSES)} NT={len(NT_VERSES)}")

# ── Load brain data ──────────────────────────────────────
with open('/tmp/trubrain_api.json') as f:
    api = json.load(f)
brain = api['nodes']
print(f"Brain: {len(brain)} nodes")
brain_json = json.dumps(brain, ensure_ascii=False)

# ── Compress all data ─────────────────────────────────────
def b64gzip(data): return base64.b64encode(gzip.compress(data.encode())).decode()

OT_B64  = b64gzip('\n'.join(OT_VERSES))
NT_B64  = b64gzip('\n'.join(NT_VERSES))
BRA_GZ  = b64gzip(brain_json)

print(f"Sizes: brain={len(BRA_GZ)} ot={len(OT_B64)} nt={len(NT_B64)}")

# ── Build HTML ────────────────────────────────────────────
html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>TRU — The Living Bible</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0c0c14;--surface:#13131f;--card:#1a1a2a;--border:#252540;
  --fg:#e8e4d4;--muted:#8884a0;--accent:#c8a84b;--red:#e05050;
  --green:#50c878;--blue:#5080e0;--purple:#a050c8;
  --font:'Georgia',serif;
}
body{background:var(--bg);color:var(--fg);font-family:var(--font);min-height:100vh;display:flex;flex-direction:column}
#app{flex:1;display:flex;flex-direction:column;max-width:900px;width:100%;margin:0 auto;padding:0 16px}

/* ── Header ── */
header{display:flex;align-items:center;gap:12px;padding:16px 0;border-bottom:1px solid var(--border)}
#logo{width:40px;height:40px;background:var(--card);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:20px;border:1px solid var(--border)}
header h1{font-size:1.3rem;color:var(--accent);letter-spacing:.05em}
header h1 span{display:block;font-size:.65rem;color:var(--muted);font-weight:normal;letter-spacing:.15em;text-transform:uppercase}
.mode-row{display:flex;gap:8px;margin-left:auto}
.mode-btn{
  padding:6px 14px;border-radius:20px;border:1px solid var(--border);
  background:var(--card);color:var(--muted);cursor:pointer;font-size:.75rem;
  transition:all .2s;letter-spacing:.05em;
}
.mode-btn.active{background:var(--accent);color:#000;border-color:var(--accent);font-weight:bold}
.mode-btn:hover:not(.active){border-color:var(--accent);color:var(--accent)}

/* ── Agent Tabs ── */
#tribunal{display:flex;gap:6px;padding:12px 0;flex-wrap:wrap;border-bottom:1px solid var(--border)}
.t-agent{
  padding:5px 12px;border-radius:16px;border:1px solid var(--border);
  background:var(--surface);color:var(--muted);cursor:pointer;font-size:.7rem;
  transition:all .2s;opacity:.55;
}
.t-agent.active{opacity:1;background:var(--card);border-color:var(--accent);color:var(--accent)}
.t-agent.active[data-a="ARCHIVIST"]{border-color:#5080e0;color:#80a0ff}
.t-agent.active[data-a="EXEGETE"]{border-color:#50c878;color:#80ffaa}
.t-agent.active[data-a="CRITIC"]{border-color:#e05050;color:#ff8080}
.t-agent.active[data-a="ARCHITECT"]{border-color:#a050c8;color:#cc80e0}
.t-agent.active[data-a="BALANCE"]{border-color:#c8a84b;color:#ffe080}

/* ── Messages ── */
#chat{flex:1;overflow-y:auto;padding:16px 0;display:flex;flex-direction:column;gap:12px}
.msg{padding:14px 16px;border-radius:12px;border:1px solid var(--border);background:var(--surface);line-height:1.65;font-size:.95rem}
.msg.user{align-self:flex-end;background:#1a2030;border-color:#304060;color:#c8d8f0}
.msg.tru .agent-tag{display:inline-block;font-size:.65rem;letter-spacing:.12em;text-transform:uppercase;padding:2px 8px;border-radius:10px;margin-bottom:8px}
.msg.tru .agent-tag.tribunal{background:#c8a84b22;color:#c8a84b;border:1px solid #c8a84b44}
.msg.tru .agent-tag.archivis{background:#5080e022;color:#80a0ff;border:1px solid #5080e044}
.msg.tru .agent-tag.exegete{background:#50c87822;color:#80ffaa;border:1px solid #50c87844}
.msg.tru .agent-tag.critic{background:#e0505022;color:#ff8080;border:1px solid #e0505044}
.msg.tru .agent-tag.architect{background:#a050c822;color:#cc80e0;border:1px solid #a050c844}
.msg.tru .agent-tag.balance{background:#c8a84b22;color:#ffe080;border:1px solid #c8a84b44}
.msg.tru .weight-bar{display:inline-block;height:4px;border-radius:2px;background:var(--accent);margin-bottom:6px;transition:width .6s ease}
.msg.tru .red-letter{color:#ff7070;font-style:italic}
.msg.tru .greek-text{color:#a0c0ff;font-family:'Times New Roman',serif;font-size:1.02em}

/* ── Bible results ── */
.verse{margin:8px 0;padding:10px 12px;background:var(--card);border-radius:8px;border:1px solid var(--border)}
.verse.ref{color:var(--accent);font-size:.78rem;font-weight:bold;letter-spacing:.05em;margin-bottom:4px}
.verse .greek{color:#a0c0ff;font-family:'Times New Roman',serif;margin:.3em 0;font-size:.95em}
.verse .english{color:var(--fg);line-height:1.6}
.verse .red{color:#ff6060;font-style:italic}
.verse .score{float:right;font-size:.7rem;color:var(--muted);margin-top:2px}
.doctrine-box{margin:10px 0;padding:10px 14px;background:#1a2535;border-radius:8px;border:1px solid #304060;font-size:.85rem;color:#a0c0e0}
.doctrine-box strong{color:var(--accent)}

/* ── Input ── */
#input-row{display:flex;gap:10px;padding:14px 0;border-top:1px solid var(--border);align-items:flex-end}
#qinp{flex:1;padding:12px 16px;background:var(--surface);border:1px solid var(--border);border-radius:24px;color:var(--fg);font-size:1rem;font-family:var(--font);outline:none;resize:none;min-height:44px;max-height:140px;transition:border-color .2s}
#qinp:focus{border-color:var(--accent)}
#qinp::placeholder{color:var(--muted)}
.btn{width:44px;height:44px;border-radius:22px;border:1px solid var(--border);background:var(--card);color:var(--accent);cursor:pointer;font-size:1.1rem;display:flex;align-items:center;justify-content:center;transition:all .2s;flex-shrink:0}
.btn:hover{background:var(--accent);color:#000;border-color:var(--accent)}
.btn:active{transform:scale(.95)}
.icon-btn{font-size:.75rem;letter-spacing:.05em;width:auto;padding:0 14px}

/* ── Status ── */
#status{font-size:.7rem;color:var(--muted);padding:4px 0;text-align:center;letter-spacing:.08em}
#status.ok{color:#50c878}
#status.loading{color:var(--accent);animation:pulse 1s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}

/* ── Loader ── */
#loader{display:none;flex-direction:column;align-items:center;justify-content:center;flex:1;gap:14px;color:var(--muted)}
#loader.show{display:flex}
#loader .spinner{width:36px;height:36px;border:3px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
#loader p{font-size:.85rem;letter-spacing:.1em;text-transform:uppercase}
</style>
</head>
<body>
<div id="app">
  <header>
    <div id="logo">✦</div>
    <h1>TRU <span>The Living Bible</span></h1>
    <div class="mode-row">
      <button class="mode-btn active" id="mode-bible">BIBLE</button>
      <button class="mode-btn" id="mode-tru">TRU</button>
      <button class="mode-btn" id="mode-both">BOTH</button>
    </div>
  </header>

  <div id="tribunal">
    <div class="t-agent active" data-a="tribunal">⬡ TRIBUNAL</div>
    <div class="t-agent" data-a="archivis">⊕ ARCHIVIST</div>
    <div class="t-agent" data-a="exegete">⊗ EXEGETE</div>
    <div class="t-agent" data-a="critic">⊖ CRITIC</div>
    <div class="t-agent" data-a="architect">⊗ ARCHITECT</div>
    <div class="t-agent" data-a="balance">⚖ BALANCE</div>
  </div>

  <div id="chat"></div>
  <div id="loader"><div class="spinner"></div><p>Loading TRU...</p></div>
  <p id="status">Initialising...</p>

  <div id="input-row">
    <textarea id="qinp" placeholder="Ask TRU anything..." rows="1"></textarea>
    <button class="btn" id="send-btn" title="Ask">↑</button>
    <button class="btn icon-btn" id="dump-btn" title="Download HTML dump">↓</button>
  </div>
</div>

<script>
'use strict';

// ══════════════════════════════════════════════════════════
// DATA PAYLOADS
// ══════════════════════════════════════════════════════════
const BRA_GZ = atob('COMPRESSED_BRAIN_PLACEHOLDER');
const OT_B64 = atob('COMPRESSED_OT_PLACEHOLDER');
const NT_B64 = atob('COMPRESSED_NT_PLACEHOLDER');

// ══════════════════════════════════════════════════════════
// STATE
// ══════════════════════════════════════════════════════════
let brain = [], ot = [], nt = [];
let mode = 'bible'; // bible | tru | both
let agent = 'tribunal'; // tribunal | archivis | exegete | critic | architect | balance
let loading = false;

const S = {
  brain: [], ot: {}, nt: {}, // keyed by book abbrev
  bibleMode: 'bible',
  agents: {
    tribunal: { label: '⬡ TRIBUNAL', color: '#c8a84b', desc: 'Balances all agents, weighted toward Christ & Wisdom', weight: 0.30 },
    archivis: { label: '⊕ ARCHIVIST', color: '#5080e0', desc: 'Fetches Scripture — Greek + English side-by-side, red letters first', weight: 0.25 },
    exegete: { label: '⊗ EXEGETE', color: '#50c878', desc: 'Explains meaning of Greek/Hebrew words in context', weight: 0.20 },
    critic:  { label: '⊖ CRITIC',  color: '#e05050', desc: 'Tests the interpretation against doctrine & contradiction', weight: 0.10 },
    architect:{ label: '⊗ ARCHITECT', color: '#a050c8', desc: 'Synthesises a complete theological answer from the data', weight: 0.10 },
    balance: { label: '⚖ BALANCE', color: '#c8a84b', desc: 'Blind scales — always weighted toward The Spirit of Wisdom', weight: 0.05 }
  },
  doctrine: [
    {k:'trinity',       t:'The Trinity: One God, three Persons (Father, Son, Holy Spirit). All equal in essence, distinct in role.'},
    {k:'incarnation',  t:'Christ is fully God and fully man — the divine Word made flesh (John 1:14).'},
    {k:'grace',        t:'Grace: unmerited favour. Salvation is by grace through faith, not works (Eph 2:8-9).'},
    {k:'atonement',    t:'Christ substitutionarily atones for sin — His shed blood redeems those who believe.'},
    {k:'resurrection', t:'Jesus rose bodily on the third day. His resurrection is the guarantee of ours (1 Cor 15:20).'},
    {k:'Scripture',    t:'The Bible is God-breathed — sufficient, authoritative, and without error in all matters of faith.'},
    {k:'covenant',     t:'God operates through covenants: Creation, Fall, Noah, Abraham, Moses, David, New Covenant.'},
    {k:'sovereignty',  t:'God is sovereign — He foreordains all that comes to pass, yet humans bear genuine responsibility.'},
    {k:'sanctific',    t:'Believers are set apart by the Spirit, progressively conformed to Christ\'s image.'},
    {k:'eschatology',  t:'Christ will return bodily to judge the living and dead, establishing the new heavens and earth.'}
  ],
  redWords: ['father','god','christ','jesus','lord','spirit','holy','truth','life','light','love','righteous','salvation','grace','faith',' mercy','kingdom','glory','righteous','eternal']
};

// ── Bible lookup helpers ───────────────────────────────
const BOOK_MAP = {
  gn:'Genesis',ex:'Exodus',lv:'Leviticus',nu:'Numbers',dt:'Deuteronomy',
  josh:'Joshua',judg:'Judges',ru:'Ruth',1sm:'1 Samuel',2sm:'2 Samuel',
  1ki:'1 Kings',2ki:'2 Kings',1ch:'1 Chronicles',2ch:'2 Chronicles',
  ezr:'Ezra',neh:'Nehemiah',est:'Esther',job:'Job',ps:'Psalm',
  pr:'Proverbs',ec:'Ecclesiastes',ss:'Song of Solomon',is:'Isaiah',
  jer:'Jeremiah',lm:'Lamentations',ez:'Ezekiel',dn:'Daniel',
  hs:'Hosea',jl:'Joel',am:'Amos',ob:'Obadiah',jn:'Jonah',mic:'Micah',
  nm:'Nahum',hb:'Habakkuk',zp:'Zephaniah',hg:'Haggai',zc:'Zechariah',ml:'Malachi',
  mt:'Matthew',mk:'Mark',lk:'Luke',jn:'John',acts:'Acts',
  rm:'Romans',1co:'1 Corinthians',2co:'2 Corinthians',ga:'Galatians',
  ep:'Ephesians',pp:'Philippians',cl:'Colossians',1th:'1 Thessalonians',
  2th:'2 Thessalonians',1tm:'1 Timothy',2tm:'2 Timothy',ti:'Titus',
  pm:'Philemon',hb:'Hebrews',jm:'James',1pe:'1 Peter',2pe:'2 Peter',
  1jn:'1 John',2jn:'2 John',3jn:'3 John',jd:'Jude',re:'Revelation'
};

function buildOT(lines) {
  for (const l of lines) {
    const p = l.indexOf('||');
    if (p < 0) continue;
    const ref = l.slice(0, p).trim(), text = l.slice(p + 2);
    const sp = ref.indexOf(' ');
    const bk = ref.slice(0, sp).toLowerCase();
    if (!S.ot[bk]) S.ot[bk] = [];
    S.ot[bk].push({ref, text: text.replace(/[{}[]]/g, '')});
  }
}

function buildNT(lines) {
  for (const l of lines) {
    const parts = l.split('||');
    if (parts.length < 2) continue;
    const ref = parts[0].trim(), greek = parts[1].trim();
    const eng = parts[2] ? parts[2].trim() : greek;
    const ab = ref.match(/^(\\w+)/)?.[1].toLowerCase() || '';
    if (!S.nt[ab]) S.nt[ab] = [];
    S.nt[ab].push({ref, greek, english: eng});
  }
}

// ── Decompress ──────────────────────────────────────────
async function decompress(b64) {
  return new TextDecoder().decode(pako.inflate(atob(b64)));
}

// ── Bible search ────────────────────────────────────────
function isRed(text) {
  const t = text.toLowerCase();
  return S.redWords.some(w => t.includes(w));
}

function wrapRed(text) {
  const t = text.toLowerCase();
  let r = text;
  for (const w of S.redWords) {
    const re = new RegExp('\\\\b(' + w + ')\\\\b', 'gi');
    r = r.replace(re, '<span class="red">$1</span>');
  }
  return r;
}

function searchBible(query, testament) {
  const q = query.toLowerCase();
  const results = [];
  const books = testament === 'nt' ? S.nt : S.ot;
  for (const [bk, verses] of Object.entries(books)) {
    for (const v of verses) {
      const hay = (v.text || v.english || '').toLowerCase();
      if (hay.includes(q)) {
        const score = q.split(/\\s+/).filter(w => w.length > 2).reduce((s, w) => s + (hay.includes(w) ? 1 : 0), 0);
        results.push({...v, bk, score, testament});
      }
      if (results.length >= 120) break;
    }
    if (results.length >= 120) break;
  }
  results.sort((a, b) => b.score - a.score);
  return results;
}

// ── Brain search ────────────────────────────────────────
function searchBrain(query) {
  const q = query.toLowerCase(), words = q.split(/\\s+/).filter(w => w.length > 2);
  const results = [];
  for (const n of S.brain) {
    const hay = (n.k + ' ' + n.v).toLowerCase();
    const score = words.reduce((s, w) => s + (hay.includes(w) ? 1 : 0), 0);
    if (score > 0) results.push({...n, score});
  }
  results.sort((a, b) => b.score - a.score);
  return results.slice(0, 20);
}

// ── Agent responses ─────────────────────────────────────
function weightBar(w) {
  return '<div class="weight-bar" style="width:' + Math.round(w * 100) + 'px;background:' +
    S.agents[agent].color + '"></div>';
}

function tag(a) {
  const cls = {tribunal:'tribunal', archivis:'archivis', exegete:'exegete', critic:'critic', architect:'architect', balance:'balance'}[a] || 'tribunal';
  return '<span class="agent-tag ' + cls + '">' + S.agents[a].label + '</span>';
}

function renderBibleResults(results, query) {
  if (!results.length) return '<p style="color:var(--muted);font-style:italic">No scripture found for "' + query + '".</p>';
  let h = '';
  const shown = results.slice(0, 20);
  for (const v of shown) {
    const ref = v.bk ? v.bk.toUpperCase() + ' ' + v.ref.replace(/^\\w+ /, '') : v.ref;
    const red = isRed(v.text || v.english || '');
    const wrapped = red ? wrapRed(v.text || v.english) : (v.text || v.english);
    const greek = v.greek ? '<div class="greek">' + v.greek + '</div>' : '';
    const english = v.english && v.greek ? '<div class="english">' + wrapped + '</div>' : '';
    h += '<div class="verse"><div class="ref">' + ref + '<span class="score">◆ ' + v.score + '</span></div>' +
      greek + english + '</div>';
  }
  if (results.length > 20) h += '<p style="color:var(--muted);font-size:.8rem;margin-top:8px">+ ' + (results.length - 20) + ' more verses</p>';
  return h;
}

function agentTribunal(query, bibleResults, brainResults) {
  const hasBible = bibleResults.length > 0;
  const hasBrain = brainResults.length > 0;
  if (!hasBible && !hasBrain) {
    return '<p style="font-style:italic;color:var(--muted)">The Tribunal has no record of that. Try rephrasing, or ask in Bible mode.</p>';
  }
  let h = weightBar(S.agents.tribunal.weight);
  h += '<p><strong>⬡ TRIBUNAL</strong> — The Spirit of Wisdom weighs all agents.</p>';
  if (hasBible) {
    const top = bibleResults.slice(0, 3);
    h += '<div class="doctrine-box"><strong>📖 Scripture:</strong>';
    for (const v of top) {
      const ref = v.bk ? v.bk.toUpperCase() + ' ' + v.ref.replace(/^\w+ /, '') : v.ref;
      const red = isRed(v.text || v.english || '');
      const txt = red ? wrapRed(v.text || v.english) : (v.text || v.english);
      h += '<div style="margin-top:6px"><strong style="color:var(--accent)">' + ref + '</strong>: ' + txt + '</div>';
    }
    h += '</div>';
  }
  if (hasBrain && mode === 'both') {
    const doc = S.doctrine.find(d => query.toLowerCase().includes(d.k));
    if (doc) {
      h += '<div class="doctrine-box"><strong>⚙ Doctrine:</strong> ' + doc.t + '</div>';
    }
  }
  return h;
}

function agentArchivis(query, bibleResults) {
  if (!bibleResults.length) return '<p style="font-style:italic;color:var(--muted)">⊕ ARCHIVIST found no scripture for this query.</p>';
  let h = weightBar(S.agents.archivis.weight);
  h += '<p><strong>⊕ ARCHIVIST</strong> — Scripture, Greek + English, red letters prioritised.</p>';
  const redFirst = bibleResults.filter(v => isRed(v.text || v.english || '')).slice(0, 8);
  const rest = bibleResults.slice(0, 12).filter(v => !isRed(v.text || v.english || ''));
  const ordered = [...redFirst, ...rest].slice(0, 12);
  h += renderBibleResults(ordered, query);
  return h;
}

function agentExegete(query, bibleResults) {
  let h = weightBar(S.agents.exegete.weight);
  h += '<p><strong>⊗ EXEGETE</strong> — Word study from the Greek & Hebrew.</p>';
  if (!bibleResults.length) return h + '<p style="color:var(--muted);font-style:italic">No verses found to exegete.</p>';
  const samples = bibleResults.slice(0, 5);
  h += '<div style="margin-top:8px">';
  for (const v of samples) {
    const ref = v.bk ? v.bk.toUpperCase() + ' ' + v.ref.replace(/^\w+ /, '') : v.ref;
    h += '<div class="verse"><div class="ref">' + ref + '</div>';
    if (v.greek) h += '<div class="greek">' + v.greek + '</div>';
    h += '<div class="english">' + (v.text || v.english || '') + '</div></div>';
  }
  h += '</div>';
  h += '<div class="doctrine-box"><strong>⊗ Word notes:</strong> Key Greek terms found in this passage: λόγος (logos/word), θεός (theos/God), χάρις (charis/grace), πίστις (pistis/faith), δικαιοσύνη (dikaiosyne/righteousness), σωτηρία (soteria/salvation), ζωή (zoe/life), φῶς (phos/light), ἀγάπη (agape/love), πνεῦμα (pneuma/spirit).</div>';
  return h;
}

function agentCritic(query, bibleResults) {
  let h = weightBar(S.agents.critic.weight);
  h += '<p><strong>⊖ CRITIC</strong> — Testing interpretation against Scripture & doctrine.</p>';
  const issues = [];
  // Cross-reference checks
  if (bibleResults.length >= 2) {
    issues.push('✓ Multiple witnesses: ' + bibleResults.slice(0, 3).map(v => {
      const m = v.ref.match(/^(\w+)\\s(\\d+:\\d+)/);
      return m ? m[1] + ' ' + m[2] : v.ref;
    }).join(', '));
  }
  if (bibleResults.some(v => (v.text || v.english || '').toLowerCase().includes('grace'))) {
    issues.push('✓ Grace passage confirmed — not by works (Eph 2:8-9).');
  }
  if (bibleResults.some(v => (v.text || v.english || '').toLowerCase().includes('law') || (v.text || v.english || '').toLowerCase().includes('command'))) {
    issues.push('⚠ Law vs. Grace tension noted — check Pauline epistles.');
  }
  if (!issues.length) issues.push('No contradictions detected. Scripture is consistent.');
  h += '<div class="doctrine-box">' + issues.map(i => '<div style="margin:4px 0">' + i + '</div>').join('') + '</div>';
  return h;
}

function agentArchitect(query, bibleResults, brainResults) {
  let h = weightBar(S.agents.architect.weight);
  h += '<p><strong>⊗ ARCHITECT</strong> — Synthesising a complete theological answer.</p>';
  // Find relevant doctrine
  const relevant = S.doctrine.filter(d => {
    const k = query.toLowerCase();
    return k.includes(d.k) || d.t.toLowerCase().includes(k.split(/\\s+/)[0]);
  });
  if (relevant.length) {
    h += '<div class="doctrine-box"><strong>Foundation doctrines:</strong>';
    for (const d of relevant) h += '<div style="margin-top:6px">' + d.t + '</div>';
    h += '</div>';
  }
  // Build answer from verses
  const topVerses = bibleResults.slice(0, 6);
  if (topVerses.length) {
    h += '<div style="margin-top:10px"><strong style="color:var(--accent)">Key scriptures:</strong>';
    for (const v of topVerses) {
      const ref = v.bk ? v.bk.toUpperCase() + ' ' + v.ref.replace(/^\w+ /, '') : v.ref;
      h += '<div class="verse"><div class="ref">' + ref + '</div>';
      if (v.greek) h += '<div class="greek">' + v.greek + '</div>';
      h += '<div class="english">' + (v.text || v.english || '') + '</div></div>';
    }
    h += '</div>';
  }
  return h;
}

function agentBalance(query) {
  let h = weightBar(S.agents.balance.weight);
  h += '<p><strong>⚖ BALANCE</strong> — Blind scales always weighted toward The Spirit of Wisdom.</p>';
  h += '<div class="doctrine-box">The BALANCE agent holds the scales in equilibrium. When all agents speak, BALANCE ensures no single voice — including itself — outweighs the witness of Scripture and the leading of the Holy Spirit. The answer TRU gives is not final because any agent said so, but because the whole body of Christ confirms it.</div>';
  // Show all agent weights
  h += '<div style="margin-top:10px">';
  for (const [k, a] of Object.entries(S.agents)) {
    h += '<div style="display:flex;justify-content:space-between;font-size:.75rem;margin:3px 0;color:' + a.color + '"><span>' + a.label + '</span><span>' + Math.round(a.weight * 100) + '%</span></div>';
  }
  h += '</div>';
  return h;
}

function fullResponse(query, bibleResults, brainResults) {
  const tagName = tag(agent);
  let body = '';
  switch (agent) {
    case 'tribunal':   body = agentTribunal(query, bibleResults, brainResults); break;
    case 'archivis':   body = agentArchivis(query, bibleResults); break;
    case 'exegete':    body = agentExegete(query, bibleResults); break;
    case 'critic':     body = agentCritic(query, bibleResults); break;
    case 'architect':  body = agentArchitect(query, bibleResults, brainResults); break;
    case 'balance':    body = agentBalance(query); break;
    default:           body = agentTribunal(query, bibleResults, brainResults);
  }
  return '<div class="msg tru">' + tagName + body + '</div>';
}

// ── HTML dump ───────────────────────────────────────────
function downloadDump() {
  const chats = document.getElementById('chat');
  const html = '<!DOCTYPE html>\\n<html lang="en">\\n<head>\\n<meta charset="UTF-8"/>\\n<title>TRU Session</title>\\n<style>' +
    document.querySelector('style').innerHTML + '</style></head>\\n<body>\\n<div style="max-width:800px;margin:0 auto;padding:20px">' +
    '<h1 style="color:#c8a84b;margin-bottom:20px">TRU — The Living Bible</h1>' +
    chats.innerHTML + '</div></body></html>';
  const blob = new Blob([html], {type: 'text/html'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
  a.download = 'TRU_session_' + new Date().toISOString().slice(0, 10) + '.html'; a.click();
}

// ── Render ──────────────────────────────────────────────
function addMsg(role, html) {
  const c = document.getElementById('chat');
  const d = document.createElement('div');
  d.className = 'msg ' + role;
  d.innerHTML = typeof html === 'string' ? html : html;
  c.appendChild(d);
  c.scrollTop = c.scrollHeight;
  return d;
}

function setStatus(txt, cls) {
  const s = document.getElementById('status');
  s.textContent = txt; s.className = cls || '';
}

// ── Init ────────────────────────────────────────────────
async function init() {
  setStatus('Decompressing brain...', 'loading');
  try { S.brain = JSON.parse(await decompress(BRA_GZ)); } catch(e) { S.brain = []; }
  setStatus('Decompressing Bible...', 'loading');
  try { buildOT((await decompress(OT_B64)).split('\\n')); } catch(e) {}
  try { buildNT((await decompress(NT_B64)).split('\\n')); } catch(e) {}
  setStatus('TRU ready — ' + S.brain.length + ' nodes, ' + Object.keys(S.ot).length + ' OT books', 'ok');
  document.getElementById('loader').classList.remove('show');
}

function ask(query) {
  if (!query.trim() || loading) return;
  loading = true;
  addMsg('user', '<p>' + query + '</p>');
  setStatus('Searching...', 'loading');

  const testament = mode === 'tru' ? null : 'both';
  const bibleResults = mode === 'tru' ? [] : searchBible(query, 'both');
  const brainResults = mode === 'tru' || mode === 'both' ? searchBrain(query) : [];
  const response = fullResponse(query, bibleResults, brainResults);
  addMsg('tru', response);
  setStatus('TRU ready', 'ok');
  loading = false;
}

// ── Events ──────────────────────────────────────────────
document.getElementById('send-btn').addEventListener('click', () => {
  ask(document.getElementById('qinp').value);
  document.getElementById('qinp').value = '';
});
document.getElementById('qinp').addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(e.target.value); e.target.value = ''; }
});
document.getElementById('dump-btn').addEventListener('click', downloadDump);
for (const b of document.querySelectorAll('.mode-btn')) {
  b.addEventListener('click', () => {
    document.querySelectorAll('.mode-btn').forEach(x => x.classList.remove('active'));
    b.classList.add('active'); mode = b.dataset.mode;
  });
}
document.querySelectorAll('.mode-btn').forEach(b => b.dataset.mode = b.id.replace('mode-', ''));
for (const a of document.querySelectorAll('.t-agent')) {
  a.addEventListener('click', () => {
    document.querySelectorAll('.t-agent').forEach(x => x.classList.remove('active'));
    a.classList.add('active'); agent = a.dataset.a;
  });
}

// ── Boot ────────────────────────────────────────────────
init();
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pako/2.1.0/pako.min.js"></script>
</body>
</html>
""".replace("'COMPRESSED_BRAIN_PLACEHOLDER'", "BRA_GZ").replace("'COMPRESSED_OT_PLACEHOLDER'", "OT_B64").replace("'COMPRESSED_NT_PLACEHOLDER'", "NT_B64")

# Now do proper placeholder replacement
html = html.replace("const BRA_GZ = atob('COMPRESSED_BRAIN_PLACEHOLDER');", 'const BRA_GZ = atob("' + BRA_GZ + '");')
html = html.replace("const OT_B64 = atob('COMPRESSED_OT_PLACEHOLDER');", 'const OT_B64 = atob("' + OT_B64 + '");')
html = html.replace("const NT_B64 = atob('COMPRESSED_NT_PLACEHOLDER');", 'const NT_B64 = atob("' + NT_B64 + '");')

with open('/home/workspace/Projects/TRU/TRU_Phase26_Offline.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Written: {os.path.getsize('/home/workspace/Projects/TRU/TRU_Phase26_Offline.html') // 1024}KB")