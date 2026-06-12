#!/usr/bin/env python3
"""Build working TRU Session from source HTML."""
from bs4 import BeautifulSoup
import json, gzip, base64, os

# ── Source ────────────────────────────────────────────
src = '/home/.z/chat-uploads/TRU_session_2026-05-14-a989f2ae5393.html'
with open(src, 'r', 'utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

body = soup.body
h1 = body.find('h1')

# ── UI elements ──────────────────────────────────────
injection = soup.new_string('''
<div id="status" style="padding:8px 12px;background:#1a1a2e;color:#c8a84b;font-family:monospace;font-size:13px;margin-bottom:12px;border-radius:4px;letter-spacing:.05em">LOADING TRU...</div>
<div id="ask-ui" style="margin:0 0 24px 0;border:1px solid #333;padding:16px;background:#111;border-radius:6px">
  <div style="color:#c8a84b;margin-bottom:10px;font-size:11px;letter-spacing:.1em">□ ASK TRU</div>
  <textarea id="qinp" rows="2" placeholder="Ask anything..." style="width:100%;padding:10px;background:#0a0a0a;color:#e0d8c8;border:1px solid #333;font-size:15px;border-radius:4px;resize:none;outline:none;font-family:Georgia,serif"></textarea>
  <div style="margin-top:10px;display:flex;gap:8px;align-items:center">
    <button id="ask-btn" style="padding:8px 20px;background:#c8a84b;color:#000;border:none;border-radius:16px;cursor:pointer;font-size:13px;font-weight:bold">Ask</button>
    <button id="dump-btn" style="padding:8px 16px;background:#1a1a2e;color:#888;border:1px solid #333;border-radius:16px;cursor:pointer;font-size:12px">HTML Dump</button>
  </div>
  <div id="kp" style="max-height:280px;overflow-y:auto;margin-top:12px;background:#0d0d0d;border:1px solid #222;border-radius:4px;padding:8px;display:none;font-size:13px"></div>
</div>
''')
h1.insert_next_sibling(injection)

# ── Data: Brain ─────────────────────────────────────
with open('/tmp/trubrain_api.json') as f:
    brain_data = json.load(f)
brain_nodes = brain_data['nodes']
brain_json = json.dumps(brain_nodes, separators=(',', ':')).replace('`', '\\`')
print(f"Brain: {len(brain_nodes)} nodes")

# ── Data: OT ────────────────────────────────────────
with gzip.open('/home/workspace/Projects/TRU/data/coil_ot.txt', 'rb') as f:
    ot_raw = f.read().decode('utf-8', errors='replace')
ot_lines = [l.strip() for l in ot_raw.split('\n') if '||' in l and l.strip()]
print(f"OT: {len(ot_lines)} verses")

# ── Data: NT ─────────────────────────────────────────
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
                ref, greek = parts[0], parts[1]
                nt_lines.append(ref + '||' + greek)
print(f"NT: {len(nt_lines)} verses")

# ── Build JS data as <script> tags (embedded, no compression) ──
# Use data URIs for OT (large) and plain JS arrays for NT+Brain

# OT as one big base64 field, decompress with pako (already in HTML)
ot_gz = gzip.compress('\n'.join(ot_lines).encode('utf-8'))
ot_b64 = base64.b64encode(ot_gz).decode()
print(f"OT gzipped: {len(ot_gz):,} bytes")

# NT as inline JS array (smaller, ~500KB)
def js_str(s):
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
nt_js_array = 'const NT = [`' + '`,\n`'.join(js_str(l) for l in nt_lines) + '`];'

# Brain as inline JSON
brain_js = f'const BRAIN = {brain_json};'

# RED words
RED = ['Lord','God','Christ','Jesus','grace','faith','love','spirit','truth','life','light','righteous','holiness','mercy','peace','hope','joy','son','father','word','soul','salvation','redeem']

# ── Full JS ─────────────────────────────────────────
js = f'''<script>
/* TRU Session — offline interactive */
(function(){{
const RED = {json.dumps(RED)};

// ─── BRAIN ────────────────────────────────────────
{brain_js}
console.log('BRAIN: ' + BRAIN.length + ' nodes');

// ─── OT (gzip-b64, decompress with pako) ─────────
const OT_B64 = "{ot_b64}";

// ─── NT (inline array) ───────────────────────────
{nt_js_array}
console.log('NT: ' + NT.length + ' verses');

// Decompress OT using pako (native gzip wrapper)
function loadOT() {{
    try {{
        const raw = atob(OT_B64);
        const bytes = Uint8Array.from(raw, c => c.charCodeAt(0));
        // pako.ungzip handles gzip format (header+footer)
        const dec = pako.ungzip(bytes, {{to:'string'}});
        window.OT = dec.split('\\n').filter(l => l.includes('||'));
        console.log('OT: ' + window.OT.length + ' verses decompressed');
    }} catch(e) {{
        console.error('OT load error:', e);
        window.OT = [];
    }}
}}

// ─── SEARCH ─────────────────────────────────────
function search(q) {{
    const words = q.toLowerCase().split(/\\s+/).filter(Boolean);
    if(!words.length) return [];
    const all = [...(window.OT||[]), ...NT];
    const scored = [];
    for(const line of all) {{
        const idx = line.indexOf('||');
        if(idx < 0) continue;
        const ref = line.slice(0, idx);
        const text = line.slice(idx + 2).toLowerCase();
        let s = 0;
        for(const w of words) {{ if(text.includes(w)) s++; }}
        if(s > 0) scored.push({{s, ref, text: line.slice(idx+2)}});
    }}
    scored.sort((a,b) => b.s - a.s);
    return scored.slice(0, 8);
}}

function highlight(text) {{
    let out = text;
    for(const w of RED) {{
        try {{ out = out.replace(new RegExp('\\\\b' + w + '\\\\b', 'gi'), '<span class="red">$&</span>'); }} catch(e){{}}
    }}
    return out;
}}

// ─── RENDER ──────────────────────────────────────
function render(q, results) {{
    const chat = document.getElementById('chat');
    const ud = document.createElement('div');
    ud.className = 'msg user';
    ud.innerHTML = '<p>' + q.replace(/</g,'&lt;') + '</p>';
    chat.appendChild(ud);

    const rd = document.createElement('div');
    rd.className = 'msg tru';

    if(!results.length) {{
        rd.innerHTML = '<span class="agent-tag tribunal">□ TRIBUNAL</span><div class="weight-bar" style="width:20%;background:#c8a84b"></div><p><strong>□ TRIBUNAL</strong> — The Spirit of Wisdom weighs all agents.</p><p style="font-style:italic;color:var(--muted)">The Tribunal has no record of that. Try rephrasing.</p>';
    }} else {{
        const otBooks = 'Genesis Exodus Leviticus Numbers Deuteronomy Joshua Judges Ruth 1 Samuel 2 Samuel 1 Kings 2 Kings 1 Chronicles 2 Chronicles Ezra Nehemiah Esther Job Psalms Proverbs Ecclesiastes Song Isaiah Jeremiah Lamentations Ezekiel Daniel Hosea Joel Amos Obadiah Jonah Micah Nahum Habakkuk Zephaniah Haggai Zechariah Malachi'.split(' ');
        let html = '<span class="agent-tag tribunal">□ TRIBUNAL</span><div class="weight-bar" style="width:40%;background:#c8a84b"></div>';
        html += '<p><strong>□ TRIBUNAL</strong> — The Spirit of Wisdom weighs all agents.</p>';
        html += '<div class="doctrine-box"><strong>📖 Scripture:</strong>';
        for(const r of results) {{
            const bookMatch = otBooks.some(b => r.ref.includes(b));
            html += '<div class="verse"><div class="ref">' + r.ref + ' ' + (bookMatch ? '(OT)' : '(NT)') + '</div><div class="english">' + highlight(r.text) + '</div></div>';
        }}
        html += '</div>';
        rd.innerHTML = html;
    }}
    chat.appendChild(rd);
    chat.scrollTop = chat.scrollHeight;
}}

// ─── ASK ─────────────────────────────────────────
function handleAsk(q) {{
    if(!q.trim()) return;
    if(!window.OT || !window.OT.length) {{
        alert('Bible still loading...'); return;
    }}
    render(q, search(q));
}}

function askKnown(k) {{
    const n = BRAIN.find(x => x.k === k);
    if(!n) return;
    document.getElementById('qinp').value = n.v;
    handleAsk(n.v);
}}

// ─── INIT ────────────────────────────────────────
function init() {{
    loadOT(); // starts async OT decompress
    const statusEl = document.getElementById('status');
    if(statusEl) {{
        // Show ready immediately (brain + NT ready, OT loading)
        statusEl.textContent = 'READY: ' + BRAIN.length + ' nodes | NT:' + NT.length + ' | OT loading...';
        statusEl.style.background = '#1a2a1a';
    }}
    // OT decompress + update status when done
    setTimeout(() => {{
        if(window.OT && window.OT.length) {{
            const s = document.getElementById('status');
            if(s) s.textContent = 'READY: ' + BRAIN.length + ' nodes | OT:' + window.OT.length + ' | NT:' + NT.length;
        }}
    }}, 2000);
    // Knowledge panel
    const kpEl = document.getElementById('kp');
    if(kpEl) {{
        kpEl.style.display = 'block';
        kpEl.innerHTML = BRAIN.map(n => '<div class="ki" onclick="askKnown(\\'' + n.k + '\\')" style="padding:4px 8px;border-bottom:1px solid #222;cursor:pointer;font-size:12px"><span style="color:#888">[' + n.t + ']</span> ' + n.v.slice(0,100).replace(/</g,'&lt;') + '</div>').join('');
    }}
}}

// ─── EVENTS ──────────────────────────────────────
document.getElementById('ask-btn').addEventListener('click', () => handleAsk(document.getElementById('qinp').value));
document.getElementById('qinp').addEventListener('keydown', e => {{ if(e.key === 'Enter' && !e.shiftKey) {{ e.preventDefault(); handleAsk(document.getElementById('qinp').value); }} }});
document.getElementById('dump-btn').addEventListener('click', () => {{
    window.open('data:text/html;charset=utf-8,' + encodeURIComponent(document.documentElement.outerHTML), '_blank');
}});

init();
}})();
</script>'''

# ── Add JS ────────────────────────────────────────
body.append(soup.new_string(js))

# ── Save ──────────────────────────────────────────
out = '/home/workspace/Projects/TRU/TRU_session_enriched.html'
with open(out, 'w', 'utf-8') as f:
    f.write(str(soup))

size = os.path.getsize(out)
print(f"\nSaved: {size:,} bytes ({size//1024}KB)")
print(f"Brain: {len(brain_nodes)} | OT: {len(ot_lines)} | NT: {len(nt_lines)}")