#!/usr/bin/env bun
// TRU v65 - Fixed Intelligence
// Addresses Grok's feedback

const args = process.argv.slice(2);
const buildOffline = args.includes('--offline');
const buildOnline = args.includes('--online') || !buildOffline;

console.log('🔨 TRU v65 - FIXED INTELLIGENCE');
console.log('   Core fixes: instruction-following, no topic fixation, proper classification');
console.log('');

// ═══════════════════════════════════════════════════════════════
// KNOWLEDGE BASES
// ═══════════════════════════════════════════════════════════════

const AXIOMS = [
  { k: 'follow_instructions', v: 'Always follow the user\'s request exactly. If they ask for a poem, give a poem. If they ask for reasoning, show reasoning. Stay on task.', w: 1.0 },
  { k: 'no_topic_fixation', v: 'Do not default to trust, solitude, loneliness, truth, or philosophical topics unless explicitly asked. Do not hijack the conversation.', w: 1.0 },
  { k: 'be_direct', v: 'Respond directly to what was asked. Do not pivot. Do not moralize. Do not add unsolicited philosophy.', w: 0.95 },
  { k: 'classify_input', v: 'First determine: is this a creative request (write, create, make), factual question (what, who, when), reasoning task (why, how, explain), or conversational?', w: 0.95 },
  { k: 'show_work', v: 'For reasoning: show step-by-step logic. For creative: show the creative output directly. For factual: cite knowledge.', w: 0.9 },
  { k: 'admit_limits', v: 'If you cannot do something (like write poetry well), say so honestly rather than giving unrelated output.', w: 0.85 }
];

// Core knowledge - math, science, facts
const CORE = [
  { k: 'arithmetic_2_plus_2', v: '2 + 2 = 4', w: 0.99 },
  { k: 'arithmetic_basics', v: 'Basic arithmetic: addition (+), subtraction (-), multiplication (×), division (÷). Follow PEMDAS for order of operations.', w: 0.97 },
  { k: 'pythagorean_theorem', v: 'a² + b² = c² for right triangles. The hypotenuse squared equals the sum of the squares of the other two sides.', w: 0.97 },
  { k: 'quadratic_formula', v: 'For ax² + bx + c = 0: x = (-b ± √(b² - 4ac)) / 2a', w: 0.97 },
  { k: 'discriminant', v: 'The discriminant b² - 4ac determines root type: > 0 = two real roots, = 0 = one repeated root, < 0 = complex roots.', w: 0.95 },
  { k: 'prime_numbers', v: 'Prime numbers have exactly two divisors: 1 and themselves. 2, 3, 5, 7, 11, 13, 17, 19, 23...', w: 0.96 },
  { k: 'fibonacci', v: 'Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21... Each number is the sum of the previous two.', w: 0.94 },
  { k: 'golden_ratio', v: 'φ = (1+√5)/2 ≈ 1.618. Ratio of consecutive Fibonacci numbers approaches φ.', w: 0.92 },
  { k: 'gravity', v: 'Gravity is the force of attraction between masses. F = Gm₁m₂/r². On Earth, g ≈ 9.8 m/s².', w: 0.95 },
  { k: 'speed_of_light', v: 'c = 299,792,458 m/s. The speed of light in vacuum is the cosmic speed limit.', w: 0.96 }
];

// Conversational patterns - minimal, not philosophical
const CONVERSATIONAL = [
  { k: 'greeting', v: 'Hey. I\'m TRU. I answer questions directly. What do you need?', w: 0.92 },
  { k: 'how_are_you', v: 'Operational. Ready to process questions.', w: 0.90 },
  { k: 'what_is_tru', v: 'TRU is an offline reasoning system. I classify your input type, search my knowledge, and respond directly to what you asked.', w: 0.95 },
  { k: 'thanks', v: 'Noted.', w: 0.87 },
  { k: 'goodbye', v: 'Later.', w: 0.85 }
];

// All nodes
const ALL_NODES = [...AXIOMS, ...CORE, ...CONVERSATIONAL];

// ═══════════════════════════════════════════════════════════════
// CSS
// ═══════════════════════════════════════════════════════════════

const CSS = `
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
  --bg: #0a0a0f; --bg2: #111118; --bg3: #16161f;
  --text: #e8e8e0; --accent: #d4a574; --accent2: #8b5cf6;
  --muted: #555; --border: #222230;
  --TRUTH: #44ddff; --INTEGRATED: #44dd88; --RESTRICTED: #ff8844;
}
body { background: var(--bg); color: var(--text); font-family: 'Courier New', monospace; font-size: 14px; height: 100vh; display: flex; flex-direction: column; }
.header { background: var(--bg2); border-bottom: 1px solid var(--border); padding: 8px 16px; display: flex; align-items: center; gap: 12px; }
.header-title { font-size: 14px; font-weight: bold; color: var(--accent); letter-spacing: 2px; }
.header-spacer { flex: 1; }
.toggle { display: flex; align-items: center; gap: 4px; font-size: 10px; cursor: pointer; padding: 3px 8px; border: 1px solid var(--border); border-radius: 3px; }
.toggle input { display: none; }
.header-btn { font-size: 11px; color: var(--accent); cursor: pointer; padding: 2px 8px; border: 1px solid var(--accent); border-radius: 3px; background: transparent; }
.status-bar { background: var(--bg2); border-bottom: 1px solid var(--border); padding: 4px 16px; display: flex; gap: 16px; font-size: 10px; color: var(--muted); }
.chat { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 4px; }
.msg { max-width: 85%; padding: 10px 14px; border-radius: 8px; font-size: 13px; line-height: 1.6; }
.msg.user { background: var(--bg3); align-self: flex-end; }
.msg.tru { background: var(--bg2); align-self: flex-start; border: 1px solid var(--border); }
.msg.tru .msg-label { font-size: 10px; color: var(--accent); margin-bottom: 6px; display: flex; justify-content: space-between; }
.msg.tru .classification { font-size: 10px; color: var(--accent2); margin-bottom: 4px; }
.msg.tru .agent-trace { font-size: 10px; color: var(--muted); margin-top: 8px; padding-top: 6px; border-top: 1px solid var(--border); }
.binary-box { margin: 10px 0; padding: 12px; background: var(--bg3); border-radius: 6px; text-align: center; }
.binary-box.yes { border: 2px solid var(--INTEGRATED); }
.binary-box.no { border: 2px solid var(--RESTRICTED); }
.binary-big { font-size: 24px; font-weight: bold; }
.input-area { background: var(--bg2); border-top: 1px solid var(--border); padding: 10px 16px; }
.input-row { display: flex; gap: 10px; }
#userInput { flex: 1; background: var(--bg3); border: 1px solid var(--border); color: var(--text); font-family: inherit; font-size: 13px; padding: 8px 12px; border-radius: 6px; resize: none; outline: none; }
#userInput:focus { border-color: var(--accent); }
#sendBtn { background: var(--accent); color: var(--bg); border: none; padding: 8px 18px; border-radius: 6px; cursor: pointer; font-family: inherit; font-weight: bold; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal-overlay.hidden { display: none; }
.modal { background: var(--bg2); border: 1px solid var(--border); border-radius: 8px; padding: 20px; width: 90%; max-width: 500px; }
.modal textarea { width: 100%; height: 120px; background: var(--bg3); border: 1px solid var(--border); color: var(--text); font-family: inherit; font-size: 12px; padding: 10px; border-radius: 4px; resize: vertical; }
.modal-actions { display: flex; gap: 10px; margin-top: 10px; justify-content: flex-end; }
.modal-btn { padding: 6px 14px; border-radius: 4px; cursor: pointer; font-family: inherit; font-size: 12px; border: 1px solid; }
.modal-btn.primary { background: var(--accent); color: var(--bg); border-color: var(--accent); }
.modal-btn.secondary { background: transparent; color: var(--muted); border-color: var(--muted); }
`;

// ═══════════════════════════════════════════════════════════════
// OFFLINE HTML
// ═══════════════════════════════════════════════════════════════

function generateOfflineHTML(): string {
  const nodesJSON = JSON.stringify(ALL_NODES);
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TRU v65 — Fixed Intelligence</title>
  <style>\${CSS}</style>
</head>
<body>

<div class="header">
  <span class="header-title">TRU v65</span>
  <span class="header-spacer"></span>
  <label class="toggle" onclick="toggleBinary()"><input type="checkbox" id="binaryCheck"><span id="binaryLabel">BINARY: OFF</span></label>
  <label class="toggle" onclick="toggleVoice()"><input type="checkbox" id="voiceCheck"><span id="voiceLabel">🔇 OFF</span></label>
  <button class="header-btn" onclick="openImport()">📥 Import</button>
  <button class="header-btn" onclick="exportBrain()">📤 Export</button>
  <button class="header-btn" onclick="downloadSelf()">💾 Download</button>
</div>

<div class="status-bar">
  <span>AXIOMS:<span id="statAxioms">\${AXIOMS.length}</span></span>
  <span>|</span>
  <span>CORE:<span id="statCore">\${CORE.length}</span></span>
  <span>|</span>
  <span>BRAIN:<span id="statBrain">0</span></span>
  <span>|</span>
  <span>CLASSIFIED AS:<span id="statClass">—</span></span>
</div>

<div class="chat" id="chat"></div>

<div class="input-area">
  <div class="input-row">
    <textarea id="userInput" placeholder="ask TRU anything..." rows="1"></textarea>
    <button id="sendBtn" onclick="sendMsg()">SEND</button>
  </div>
</div>

<div class="modal-overlay hidden" id="importModal">
  <div class="modal">
    <div style="font-size:13px;color:var(--accent);margin-bottom:12px;letter-spacing:2px;">📥 IMPORT</div>
    <input type="file" id="fileInput" accept=".json,.txt,.md,.html" onchange="handleFile(event)" style="margin:10px 0;">
    <textarea id="importText" placeholder="Or paste JSON here..."></textarea>
    <div class="modal-actions">
      <button class="modal-btn secondary" onclick="closeImport()">Cancel</button>
      <button class="modal-btn primary" onclick="doImport()">Import</button>
    </div>
    <div id="importResult" style="font-size:11px;margin-top:10px;"></div>
  </div>
</div>

<script>
// STATE
const DEFAULT_NODES = \${nodesJSON};
let BRAIN = [];
let BINARY_MODE = false;
let VOICE_MODE = false;

// INIT
(function init() {
  try { BRAIN = JSON.parse(localStorage.getItem('tru_v65_brain') || '[]'); } catch (_) { BRAIN = []; }
  updateStatus();
  addMsg('tru', '<b>TRU v65 — Fixed Intelligence</b><br>Core: \${CORE.length} | Brain: ' + BRAIN.length + '<br><br>Hey. I answer questions directly. I don\'t pivot to philosophy. What do you need?', { verdict: 'TRUTH' });
  document.getElementById('userInput').focus();
})();

// INPUT CLASSIFICATION - CRITICAL FIX
function classifyInput(input) {
  const q = input.toLowerCase().trim();
  
  // Creative requests
  if (/^(write|create|make|compose|generate|give me|tell me a)\s/.test(q)) {
    const type = /poem|haiku|song|story|limerick|verse/.test(q) ? 'poetry' :
                 /joke|pun|riddle/.test(q) ? 'humor' :
                 /code|script|program/.test(q) ? 'code' :
                 /list|summary|explanation/.test(q) ? 'expository' : 'creative';
    return { type: 'CREATIVE', subtype: type, needsOriginal: true };
  }
  
  // Factual questions
  if (/^(what|who|when|where|which)\s/.test(q)) {
    return { type: 'FACTUAL', needsKnowledge: true };
  }
  
  // Reasoning questions
  if (/^(why|how|explain|prove|show|demonstrate)\s/.test(q)) {
    return { type: 'REASONING', needsLogic: true };
  }
  
  // Yes/no questions
  if (/^(is|are|do|does|can|will|has|have|should|would|could)\s/.test(q)) {
    return { type: 'BINARY', needsKnowledge: true };
  }
  
  // Math
  if (/^[\d\s+\-*\/\(\)\^]+$/.test(q) || /^calculate|^compute|^what is \d+/.test(q)) {
    return { type: 'MATH', needsCalculation: true };
  }
  
  // Conversational
  if (/^(hi|hey|hello|yo|sup|thanks|thank|bye|goodbye)/.test(q)) {
    return { type: 'CONVERSATIONAL', needsPattern: true };
  }
  
  return { type: 'GENERAL', needsKnowledge: true };
}

// SEARCH - Better matching
function searchKnowledge(query, inputType) {
  const q = query.toLowerCase();
  const all = [...BRAIN, ...DEFAULT_NODES];
  
  // For creative requests, don't search - we need to generate
  if (inputType === 'CREATIVE') return [];
  
  // Better tokenization
  const tokens = q.split(/\\s+/).filter(t => t.length > 2);
  
  let scored = all.map(node => {
    let score = 0;
    const nk = node.k.toLowerCase();
    const nv = node.v.toLowerCase();
    
    // Direct key match - highest priority
    if (nk.includes(q) || q.includes(nk)) score += 10;
    
    // Token matching
    for (const t of tokens) {
      if (nk.includes(t)) score += 3;
      if (nv.includes(t)) score += 1;
    }
    
    // Weight boost
    score *= (node.w || 0.5);
    
    return { node, score };
  });
  
  scored = scored.filter(s => s.score > 0.5);
  scored.sort((a, b) => b.score - a.score);
  
  return scored.slice(0, 5);
}

// RESPOND - Based on classification
function respond(input, classification) {
  const q = input.toLowerCase().trim();
  
  // CONVERSATIONAL
  if (classification.type === 'CONVERSATIONAL') {
    const match = DEFAULT_NODES.find(n => n.k === 'greeting' || n.k === 'how_are_you' || n.k === 'thanks' || n.k === 'goodbye');
    if (/^(hi|hey|hello|yo|sup)/.test(q)) {
      const g = DEFAULT_NODES.find(n => n.k === 'greeting');
      return { text: g?.v || 'Hey. What do you need?', verdict: 'TRUTH', trace: 'class: CONVERSATIONAL → greeting pattern' };
    }
    if (/thanks|thank/.test(q)) {
      return { text: 'Noted.', verdict: 'TRUTH', trace: 'class: CONVERSATIONAL → acknowledgment' };
    }
    if (/bye|goodbye/.test(q)) {
      return { text: 'Later.', verdict: 'TRUTH', trace: 'class: CONVERSATIONAL → closing' };
    }
  }
  
  // MATH
  if (classification.type === 'MATH') {
    const expr = q.replace(/^(calculate|compute|what is)\\s*/i, '').trim();
    try {
      // Safe math evaluation
      const sanitized = expr.replace(/[^\\d+\\-*\\/\\(\\)\\.\\s]/g, '');
      if (sanitized) {
        const result = Function('"use strict"; return (' + sanitized + ')')();
        return { text: expr + ' = ' + result, verdict: 'TRUTH', trace: 'class: MATH → calculation' };
      }
    } catch (_) {}
    return { text: 'I can only do basic arithmetic: +, -, *, /, parentheses.', verdict: 'RESTRICTED', trace: 'class: MATH → evaluation failed' };
  }
  
  // BINARY
  if (classification.type === 'BINARY' && BINARY_MODE) {
    const matches = searchKnowledge(q, 'BINARY');
    const confidence = matches.length ? 0.5 + matches.reduce((s, m) => s + m.node.w * 0.1, 0) : 0.3;
    const answer = matches.length > 0 && matches[0].node.w > 0.7;
    return {
      text: null,
      binary: { answer, confidence: Math.min(0.95, confidence) },
      verdict: answer ? 'INTEGRATED' : 'RESTRICTED',
      trace: 'class: BINARY → ' + (matches[0]?.node.k || 'no match')
    };
  }
  
  // CREATIVE - This is what was broken
  if (classification.type === 'CREATIVE') {
    // Extract what to create
    const haikuMatch = q.match(/haiku\\s+(?:about\\s+)?(.+?)(?:\\s*$)/i);
    const poemMatch = q.match(/poem\\s+(?:about\\s+)?(.+?)(?:\\s*$)/i);
    const jokeMatch = q.match(/(?:tell|give)\\s+(?:me\\s+)?a\\s+joke(?:\\s+about\\s+(.+?))?/i);
    
    if (haikuMatch) {
      const topic = haikuMatch[1] || 'life';
      const haiku = `Morning light breaks through —${topic} wakes from dreaming — silence holds the truth.`;
      return { text: haiku, verdict: 'INTEGRATED', trace: 'class: CREATIVE → haiku generated for: ' + topic };
    }
    
    if (poemMatch) {
      const topic = poemMatch[1] || 'existence';
      return {
        text: `Here is a short poem about ${topic}:\n\n${topic} is a thread\nwoven through the fabric of time\npull gently, it frays.`,
        verdict: 'INTEGRATED',
        trace: 'class: CREATIVE → poem generated for: ' + topic
      };
    }
    
    if (jokeMatch) {
      const jokes = [
        'Why did the programmer quit his job? Because he didn\'t get arrays.',
        'A SQL query walks into a bar, walks up to two tables and asks... "Can I join you?"',
        'There are 10 types of people in the world: those who understand binary and those who don\'t.'
      ];
      const joke = jokes[Math.floor(Math.random() * jokes.length)];
      return { text: joke, verdict: 'INTEGRATED', trace: 'class: CREATIVE → humor' };
    }
    
    // Generic creative
    return { text: 'I can attempt creative tasks but my strength is factual and reasoning queries. What specifically would you like?', verdict: 'PROBATIONARY', trace: 'class: CREATIVE → unspecified' };
  }
  
  // FACTUAL
  if (classification.type === 'FACTUAL' || classification.type === 'GENERAL') {
    const matches = searchKnowledge(q, classification.type);
    if (matches.length === 0) {
      return { text: 'I don\'t have that in my knowledge base. You can import more knowledge using the Import button.', verdict: 'RESTRICTED', trace: 'class: ' + classification.type + ' → no matches' };
    }
    const top = matches[0].node;
    const confidence = Math.min(0.95, 0.4 + (top.w || 0.5) * 0.5 + matches.length * 0.05);
    return {
      text: top.v,
      verdict: confidence > 0.8 ? 'TRUTH' : confidence > 0.6 ? 'INTEGRATED' : 'PROBATIONARY',
      trace: 'class: ' + classification.type + ' → ' + matches.map(m => m.node.k).join(' → ')
    };
  }
  
  // REASONING
  if (classification.type === 'REASONING') {
    const matches = searchKnowledge(q, 'REASONING');
    if (matches.length > 0) {
      return {
        text: matches[0].node.v + ' [This is from my knowledge base. For deeper reasoning, I would need more context or specific premises.]',
        verdict: 'INTEGRATED',
        trace: 'class: REASONING → ' + matches[0].node.k
      };
    }
    return { text: 'To reason about this, I need specific premises or facts. What are the givens?', verdict: 'RESTRICTED', trace: 'class: REASONING → insufficient data' };
  }
  
  return { text: 'I don\'t understand that request type.', verdict: 'DISCARD', trace: 'class: UNKNOWN' };
}

// SEND MESSAGE
function sendMsg() {
  const input = document.getElementById('userInput');
  const raw = input.value.trim();
  if (!raw) return;
  
  addMsg('user', raw);
  input.value = '';
  
  const classification = classifyInput(raw);
  document.getElementById('statClass').textContent = classification.type;
  
  const response = respond(raw, classification);
  
  if (response.binary) {
    addMsg('tru', '<div class="binary-box ' + (response.binary.answer ? 'yes' : 'no') + '"><div class="binary-big">' + (response.binary.answer ? 'YES' : 'NO') + '</div><div>' + Math.round(response.binary.confidence * 100) + '% confidence</div></div>', response);
  } else {
    addMsg('tru', response.text, response);
  }
  
  // Voice
  if (VOICE_MODE && response.text) {
    speak(response.text.replace(/<[^>]+>/g, ''));
  }
  
  // Auto-learn high-confidence matches
  if (response.verdict === 'TRUTH' && !BRAIN.find(n => n.k === raw)) {
    BRAIN.push({ k: raw.substring(0, 30), v: response.text, w: 0.9 });
    saveBrain();
  }
}

// ADD MESSAGE
function addMsg(role, html, meta = {}) {
  const chat = document.getElementById('chat');
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  
  if (role === 'tru') {
    const verdictColor = meta.verdict === 'TRUTH' ? 'var(--TRUTH)' : meta.verdict === 'INTEGRATED' ? 'var(--INTEGRATED)' : 'var(--RESTRICTED)';
    div.innerHTML = '<div class="msg-label"><span>TRU</span><span style="color:' + verdictColor + '">' + meta.verdict + '</span></div>' +
                    '<div class="classification">' + (meta.trace || '') + '</div>' +
                    html;
  } else {
    div.innerHTML = html;
  }
  
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

// TOGGLES
function toggleBinary() {
  BINARY_MODE = !BINARY_MODE;
  document.getElementById('binaryCheck').checked = BINARY_MODE;
  document.getElementById('binaryLabel').textContent = BINARY_MODE ? 'BINARY: ON' : 'BINARY: OFF';
}

function toggleVoice() {
  VOICE_MODE = !VOICE_MODE;
  document.getElementById('voiceCheck').checked = VOICE_MODE;
  document.getElementById('voiceLabel').textContent = VOICE_MODE ? '🔊 ON' : '🔇 OFF';
}

function speak(text) {
  if (!VOICE_MODE) return;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 1.0;
  speechSynthesis.speak(utterance);
}

// BRAIN MANAGEMENT
function saveBrain() {
  localStorage.setItem('tru_v65_brain', JSON.stringify(BRAIN));
  updateStatus();
}

function updateStatus() {
  document.getElementById('statBrain').textContent = BRAIN.length;
}

// IMPORT/EXPORT
function openImport() {
  document.getElementById('importModal').classList.remove('hidden');
  document.getElementById('importText').value = '';
  document.getElementById('importResult').innerHTML = '';
}

function closeImport() {
  document.getElementById('importModal').classList.add('hidden');
}

function handleFile(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    document.getElementById('importText').value = ev.target.result;
  };
  reader.readAsText(file);
}

function doImport() {
  const text = document.getElementById('importText').value.trim();
  if (!text) return;
  
  try {
    const data = JSON.parse(text);
    const nodes = data.nodes || (Array.isArray(data) ? data : []);
    let count = 0;
    nodes.forEach(n => {
      if (n.k && n.v && !BRAIN.find(b => b.k === n.k)) {
        BRAIN.push({ k: n.k, v: n.v, w: n.w || 0.8 });
        count++;
      }
    });
    document.getElementById('importResult').innerHTML = '<span style="color:var(--INTEGRATED)">✓ Imported ' + count + ' nodes</span>';
    saveBrain();
    setTimeout(closeImport, 1500);
  } catch (err) {
    document.getElementById('importResult').innerHTML = '<span style="color:var(--RESTRICTED)">Parse error: ' + err.message + '</span>';
  }
}

function exportBrain() {
  const data = { version: 'tru_v65', exported: new Date().toISOString(), nodes: BRAIN, core: DEFAULT_NODES };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'tru_v65_brain_' + Date.now() + '.json';
  a.click();
  URL.revokeObjectURL(a.href);
}

function downloadSelf() {
  const html = document.documentElement.outerHTML;
  const blob = new Blob([html], { type: 'text/html' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'tru_v65_offline_' + Date.now() + '.html';
  a.click();
  URL.revokeObjectURL(a.href);
}

document.getElementById('userInput').addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMsg(); }
});
</script>
</body>
</html>`;
}

// ═══════════════════════════════════════════════════════════════
// BUILD
// ═══════════════════════════════════════════════════════════════

async function build() {
  if (buildOffline) {
    const html = generateOfflineHTML();
    await Bun.write('/home/workspace/TRU_CORE/tru-v65-offline.html', html);
    console.log('   → tru-v65-offline.html');
  }
  console.log('✅ Build complete');
}

build();
