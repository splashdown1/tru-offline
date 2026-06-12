#!/usr/bin/env python3
"""Patch TRU_session_enriched.html with working UI + data"""
from bs4 import BeautifulSoup
import json, gzip, base64, os

out = '/home/workspace/Projects/TRU/TRU_session_enriched.html'
with open(out, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

body = soup.body
h1 = body.find('h1')

injection = soup.new_string(
'<div id="status" style="padding:8px 12px;background:#1a1a2e;color:#c8a84b;font-family:monospace;font-size:13px;margin-bottom:12px;border-radius:4px;letter-spacing:.05em">LOADING TRU...</div>\n'
'<div id="ask-ui" style="margin:0 0 24px 0;border:1px solid #333;padding:16px;background:#111;border-radius:6px">\n'
'  <div style="color:#c8a84b;margin-bottom:10px;font-size:11px;letter-spacing:.1em">□ ASK TRU</div>\n'
'  <textarea id="qinp" rows="2" placeholder="Ask anything..." style="width:100%;padding:10px;background:#0a0a0a;color:#e0d8c8;border:1px solid #333;font-size:15px;border-radius:4px;resize:none;outline:none;font-family:Georgia,serif"></textarea>\n'
'  <div style="margin-top:10px;display:flex;gap:8px;align-items:center">\n'
'    <button id="ask-btn" style="padding:8px 20px;background:#c8a84b;color:#000;border:none;border-radius:16px;cursor:pointer;font-size:13px;font-weight:bold">Ask</button>\n'
'    <button id="dump-btn" style="padding:8px 16px;background:#1a1a2e;color:#888;border:1px solid #333;border-radius:16px;cursor:pointer;font-size:12px">HTML Dump</button>\n'
'  </div>\n'
'  <div id="kp" style="max-height:280px;overflow-y:auto;margin-top:12px;background:#0d0d0d;border:1px solid #222;border-radius:4px;padding:8px;display:none;font-size:13px"></div>\n'
'</div>'
)
h1.insert_next_sibling(injection)

with open('/tmp/trubrain_api.json') as f:
    brain_data = json.load(f)
brain_nodes = brain_data['nodes']
brain_json = json.dumps(brain_nodes, separators=(',', ':')).replace('`', '`')

with gzip.open('/home/workspace/Projects/TRU/data/coil_ot.txt', 'rb') as f:
    ot_raw = f.read().decode('utf-8', errors='replace')
ot_lines = [l.strip() for l in ot_raw.split('\n') if '||' in l and l.strip()]

nt_lines = []
for fname in sorted(os.listdir('/tmp/package/txt')):
    if not fname.endswith('.txt') or 'APP' in fname:
        continue
    with open(f'/tmp/package/txt/{fname}', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '|' not in line:
                continue
            parts = line.split('\t', 1)
            if len(parts) == 2:
                nt_lines.append(parts[0] + '||' + parts[1])

ot_gz = gzip.compress('\n'.join(ot_lines).encode('utf-8'))
ot_b64 = base64.b64encode(ot_gz).decode()

RED = ['Lord','God','Christ','Jesus','grace','faith','love','spirit','truth','life','light','righteous','holiness','mercy','peace','hope','joy','son','father','word','soul','salvation','redeem']

print(f'Data: brain={len(brain_nodes)} OT={len(ot_lines)} NT={len(nt_lines)}')

def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace('\n', '\\n')

js = '''
(function(){
const RED = ''' + json.dumps(RED) + ''';
const BRAIN = ''' + brain_json + ''';
const NT_STR = "''' + esc('\n'.join(nt_lines)) + '''";
const NT = NT_STR.split('\n').filter(l => l.includes('||'));
const OT_B64 = "''' + ot_b64 + '''";
let OT = [];

function loadOT() {
    try {
        const raw = atob(OT_B64);
        const bytes = Uint8Array.from(raw, c => c.charCodeAt(0));
        const dec = pako.ungzip(bytes, {to:'string'});
        OT = dec.split('\n').filter(l => l.includes('||'));
        const s = document.getElementById('status');
        if(s) s.textContent = 'READY: brain=' + BRAIN.length + ' | OT=' + OT.length + ' | NT=' + NT.length;
    } catch(e) {
        const s = document.getElementById('status');
        if(s) { s.textContent = 'ERR: ' + e.message; s.style.background = '#2a1a1a'; }
    }
}

function search(q) {
    const words = q.toLowerCase().split(/\s+/).filter(Boolean);
    if(!words.length || !OT.length) return [];
    const all = [...OT, ...NT];
    const scored = [];
    for(const line of all) {
        const idx = line.indexOf('||');
        if(idx < 0) continue;
        const ref = line.slice(0, idx);
        const text = line.slice(idx+2).toLowerCase();
        let s = 0;
        for(const w of words) { if(text.includes(w)) s++; }
        if(s > 0) scored.push({s, ref, text: line.slice(idx+2)});
    }
    scored.sort((a,b) => b.s - a.s);
    return scored.slice(0, 8);
}

function highlight(text) {
    let out = text;
    for(const w of RED) {
        try { out = out.replace(new RegExp('\\b' + w + '\\b', 'gi'), '<span class="red">$1</span>'); } catch(e){}
    }
    return out;
}

const OT_BOOKS = 'Genesis Exodus Leviticus Numbers Deuteronomy Joshua Judges Ruth 1 Samuel 2 Samuel 1 Kings 2 Kings 1 Chronicles 2 Chronicles Ezra Nehemiah Esther Job Psalms Proverbs Ecclesiastes Song Isaiah Jeremiah Lamentations Ezekiel Daniel Hosea Joel Amos Obadiah Jonah Micah Nahum Habakkuk Zephaniah Haggai Zechariah Malachi'.split(' ');

function render(q, results) {
    const chat = document.getElementById('chat');
    const ud = document.createElement('div');
    ud.className = 'msg user';
    ud.innerHTML = '<p>' + q.replace(/</g,'&lt;') + '</p>';
    chat.appendChild(ud);
    const rd = document.createElement('div');
    rd.className = 'msg tru';
    if(!results.length) {
        rd.innerHTML = '<span class="agent-tag tribunal">□ TRIBUNAL</span><div class="weight-bar" style="width:20%;background:#c8a84b"></div><p><strong>□ TRIBUNAL</strong> — The Spirit of Wisdom weighs all agents.</p><p style="font-style:italic;color:var(--muted)">The Tribunal has no record of that. Try rephrasing.</p>';
    } else {
        let html = '<span class="agent-tag tribunal">□ TRIBUNAL</span><div class="weight-bar" style="width:40%;background:#c8a84b"></div>';
        html += '<p><strong>□ TRIBUNAL</strong> — The Spirit of Wisdom weighs all agents.</p>';
        html += '<div class="doctrine-box"><strong>📖 Scripture:</strong>';
        for(const r of results) {
            const book = OT_BOOKS.some(b => r.ref.includes(b));
            html += '<div class="verse"><div class="ref">' + r.ref + ' ' + (book ? '(OT)' : '(NT)') + '</div><div class="english">' + highlight(r.text) + '</div></div>';
        }
        html += '</div>';
        rd.innerHTML = html;
    }
    chat.appendChild(rd);
    chat.scrollTop = chat.scrollHeight;
}

function handleAsk(q) {
    if(!q.trim()) return;
    if(!OT.length) { alert('Bible loading...'); return; }
    render(q, search(q));
}

function askKnown(k) {
    const n = BRAIN.find(x => x.k === k);
    if(!n) return;
    const el = document.getElementById('qinp');
    if(el) { el.value = n.v; handleAsk(n.v); }
}

function init() {
    loadOT();
    const statusEl = document.getElementById('status');
    if(statusEl) {
        statusEl.textContent = 'READY: ' + BRAIN.length + ' nodes | NT:' + NT.length + ' | OT loading...';
        statusEl.style.background = '#1a2a1a';
    }
    setTimeout(function(){ if(OT.length){ var s=document.getElementById('status'); if(s) s.textContent='READY: brain='+BRAIN.length+' | OT='+OT.length+' | NT='+NT.length; } }, 3000);
    var kpEl = document.getElementById('kp');
    if(kpEl) {
        kpEl.style.display = 'block';
        kpEl.innerHTML = BRAIN.map(function(n){ return '<div class="ki" onclick="askKnown(\''+n.k+'\')" style="padding:4px 8px;border-bottom:1px solid #222;cursor:pointer"><span style="color:#888;font-size:11px">['+n.t+']</span> '+n.v.slice(0,100).replace(/</g,'&lt;')+'</div>'; }).join('');
    }
}

var askBtn = document.getElementById('ask-btn');
var inpEl = document.getElementById('qinp');
var dumpBtn = document.getElementById('dump-btn');
if(askBtn) askBtn.addEventListener('click', function(){ handleAsk(inpEl.value); });
if(inpEl) inpEl.addEventListener('keydown', function(e){ if(e.key==='Enter'&&!e.shiftKey){ e.preventDefault(); handleAsk(inpEl.value); } });
if(dumpBtn) dumpBtn.addEventListener('click', function(){ window.open('data:text/html;charset=utf-8,'+encodeURIComponent(document.documentElement.outerHTML),'_blank'); });

init();
})();
'''

for s in soup.find_all('script'):
    s.extract()
body.append(soup.new_string('<script>' + js + '</script>'))

with open(out, 'w', encoding='utf-8') as f:
    f.write(str(soup))

size = os.path.getsize(out)
print('Saved: ' + str(size) + ' bytes (' + str(size//1024) + 'KB)')
