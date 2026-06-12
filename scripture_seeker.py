#!/usr/bin/env python3
"""Scripture Seeker — TRU-powered offline KJV engine"""
from pathlib import Path
import json, re, base64

MEGA = Path('/home/workspace/TRU_MEGA_BRAIN.json')
OUT = Path('/home/workspace/Scripture_Seeker.html')

with open(MEGA) as f:
    nodes = json.load(f)['nodes']

# ── index for fast lookup ──────────────────────────────────────────────
by_key = {n['k']: n for n in nodes}
verse_keys = sorted(by_key.keys())

# ── book manifest ──────────────────────────────────────────────────────
book_pats = {
    'genesis': 'genesis|gen|1 mo|1mo|first gen',
    'exodus': 'exodus|exo|2 mo|2mo|second ex',
    'leviticus': 'leviticus|lev|3 mo|3mo',
    'numbers': 'numbers|num|4 mo|4mo',
    'deuteronomy': 'deuteronomy|deut|deu|5 mo|5mo',
    'joshua': 'joshua|josh|jos',
    'judges': 'judges|judg|jdg',
    'ruth': 'ruth|rth',
    '1_samuel': '1 samuel|1 sam|1sam|i?samuel',
    '2_samuel': '2 samuel|2 sam|2sam|ii?samuel',
    '1_kings': '1 kings|1 kin|1kin|i?kings',
    '2_kings': '2 kings|2 kin|2kin|ii?kings',
    '1_chronicles': '1 chronicles|1 chr|1chr|i?chronicles',
    '2_chronicles': '2 chronicles|2 chr|2chr|ii?chronicles',
    'ezra': 'ezra|ezr',
    'nehemiah': 'nehemiah|neh',
    'esther': 'esther|esth',
    'job': 'job|job',
    'psalms': 'psalms|psalm|ps',
    'proverbs': 'proverbs|prov|prv',
    'ecclesiastes': 'ecclesiastes|eccl|ecc|qoheleth',
    'song_of_solomon': 'song of solomon|song|sos|canticle',
    'isaiah': 'isaiah|isa',
    'jeremiah': 'jeremiah|jer',
    'lamentations': 'lamentations|lam',
    'ezekiel': 'eze|ezekiel|ezekiel',
    'daniel': 'daniel|dan|dn',
    'hosea': 'hosea|hos',
    'joel': 'joel|joe',
    'amos': 'amos|amo',
    'obadiah': 'obadiah|oba',
    'jonah': 'jonah|jon',
    'micah': 'micah|mic',
    'nahum': 'nahum|nah',
    'habakkuk': 'habakkuk|hab',
    'zephaniah': 'zephaniah|zep',
    'haggai': 'haggai|hag',
    'zechariah': 'zechariah|zec',
    'malachi': 'malachi|mal',
    'matthew': 'matthew|matt|mt',
    'mark': 'mark|mrk|mk',
    'luke': 'luke|luk|lk',
    'john': 'john|jn|jhn|joh',
    'acts': 'acts|act|ac',
    'romans': 'romans|rom|rm',
    '1_corinthians': '1 corinthians|1 cor|1cor|i?corinthians',
    '2_corinthians': '2 corinthians|2 cor|2cor|ii?corinthians',
    'galatians': 'galatians|gal|ga',
    'ephesians': 'ephesians|ephes|eph',
    'philippians': 'philippians|phil|pp',
    'colossians': 'colossians|col',
    '1_thessalonians': '1 thessalonians|1 thess|1thess|i?thessalonians',
    '2_thessalonians': '2 thessalonians|2 thess|2thess|ii?thessalonians',
    '1_timothy': '1 timothy|1 tim|1tim|i?timothy',
    '2_timothy': '2 timothy|2 tim|2tim|ii?timothy',
    'titus': 'titus|tit',
    'philemon': 'philemon|phlm',
    'hebrews': 'hebrews|heb',
    'james': 'james|jas',
    '1_peter': '1 peter|1 pet|1pet|i?peter',
    '2_peter': '2 peter|2 pet|2pet|ii?peter',
    '1_john': '1 john|1 jn|1joh|i?john',
    '2_john': '2 john|2 jn|2joh|ii?john',
    '3_john': '3 john|3 jn|3joh|iii?john',
    'jude': 'jude|jud',
    'revelation': 'revelation|rev|revelations|apocalypse',
}

canonical = {
    'genesis': 'Genesis', 'exodus': 'Exodus', 'leviticus': 'Leviticus',
    'numbers': 'Numbers', 'deuteronomy': 'Deuteronomy', 'joshua': 'Joshua',
    'judges': 'Judges', 'ruth': 'Ruth', '1_samuel': '1 Samuel',
    '2_samuel': '2 Samuel', '1_kings': '1 Kings', '2_kings': '2 Kings',
    '1_chronicles': '1 Chronicles', '2_chronicles': '2 Chronicles',
    'ezra': 'Ezra', 'nehemiah': 'Nehemiah', 'esther': 'Esther', 'job': 'Job',
    'psalms': 'Psalms', 'proverbs': 'Proverbs', 'ecclesiastes': 'Ecclesiastes',
    'song_of_solomon': 'Song of Solomon', 'isaiah': 'Isaiah', 'jeremiah': 'Jeremiah',
    'lamentations': 'Lamentations', 'eze': 'Ezekiel', 'daniel': 'Daniel',
    'hosea': 'Hosea', 'joel': 'Joel', 'amos': 'Amos', 'obadiah': 'Obadiah',
    'jonah': 'Jonah', 'micah': 'Micah', 'nahum': 'Nahum', 'habakkuk': 'Habakkuk',
    'zephaniah': 'Zephaniah', 'haggai': 'Haggai', 'zechariah': 'Zechariah',
    'malachi': 'Malachi', 'matthew': 'Matthew', 'mark': 'Mark', 'luke': 'Luke',
    'john': 'John', 'acts': 'Acts', 'romans': 'Romans',
    '1_corinthians': '1 Corinthians', '2_corinthians': '2 Corinthians',
    'galatians': 'Galatians', 'ephesians': 'Ephesians', 'philippians': 'Philippians',
    'colossians': 'Colossians', '1_thessalonians': '1 Thessalonians',
    '2_thessalonians': '2 Thessalonians', '1_timothy': '1 Timothy',
    '2_timothy': '2 Timothy', 'titus': 'Titus', 'philemon': 'Philemon',
    'hebrews': 'Hebrews', 'james': 'James', '1_peter': '1 Peter',
    '2_peter': '2 Peter', '1_john': '1 John', '2_john': '2 John',
    '3_john': '3 John', 'jude': 'Jude', 'revelation': 'Revelation',
}

# normalize ezekiel key
if 'eze' not in canonical:
    canonical['eze'] = 'Ezekiel'

# build book list with chapter counts
book_slugs = []
book_displays = []
book_chapters = {}
for vk in verse_keys:
    m = re.match(r'^([a-z0-9_]+)_(\d+):(\d+)$', vk)
    if m:
        book = m.group(1)
        if book not in book_slugs:
            book_slugs.append(book)
            book_displays.append(canonical.get(book, book.replace('_', ' ').title()))
            book_chapters[book] = set()
        book_chapters[book].add(int(m.group(2)))

# encode brain as base64
b64 = base64.b64encode(json.dumps(nodes, ensure_ascii=False).encode('utf-8')).decode()

stats = f"66 books · {len(verse_keys):,} verses · KJV"

# emit JS book pattern objects
bpat_js = 'const BPATS = ' + json.dumps(book_pats, ensure_ascii=False) + ';\n'
bcanon_js = 'const CANON = ' + json.dumps(book_displays, ensure_ascii=False) + ';\n'
bslug_js = 'const BOOK_SLUGS = ' + json.dumps(book_slugs, ensure_ascii=False) + ';\n'

print(f"Books: {len(book_slugs)}, Verses: {len(verse_keys)}, Brain b64: {len(b64)} chars")

# ──────────────────────────────────────────────────────────────────────
STYLE = """
:root {
  --bg: #0b0d0f; --fg: #f1ece1; --muted: #9a958a; --card: #15181c;
  --accent: #d8a657; --border: #2a2d33; --kid: #a3d977; --blue: #7ab8ff;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font: 15px/1.6 -apple-system, system-ui, "Segoe UI", Roboto, sans-serif;
  min-height: 100vh;
}
header {
  padding: 18px 22px; border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
  flex-wrap: wrap; gap: 12px;
}
header h1 { font-size: 17px; letter-spacing: .06em; }
header .stats { color: var(--muted); font-size: 12px; letter-spacing: .04em; }
main { max-width: 900px; margin: 0 auto; padding: 18px 22px 140px; }

.search-bar { display: flex; gap: 10px; margin: 20px 0 28px; flex-wrap: wrap; }
.search-bar input {
  flex: 1; min-width: 220px; padding: 14px 18px;
  background: var(--card); border: 1px solid var(--border); color: var(--fg);
  border-radius: 10px; font-size: 15px; font-family: inherit;
  outline: none; transition: border-color .2s;
}
.search-bar input:focus { border-color: var(--accent); }
.search-bar input::placeholder { color: var(--muted); }
.search-bar button {
  padding: 12px 24px; background: var(--accent); color: #0b0d0f;
  border: none; border-radius: 10px; font-size: 14px; font-weight: 700;
  cursor: pointer; letter-spacing: .04em;
}
.search-bar button:hover { background: #e8b76a; }

.book-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(145px, 1fr));
  gap: 8px; margin-bottom: 32px;
}
.book-btn {
  background: var(--card); border: 1px solid var(--border); color: var(--fg);
  padding: 10px 12px; border-radius: 8px; font-size: 12px; text-align: left;
  cursor: pointer; transition: all .15s; font-family: inherit;
}
.book-btn:hover { border-color: var(--accent); background: rgba(216,166,87,.08); }
.book-btn .bname { font-weight: 600; display: block; margin-bottom: 2px; }
.book-btn .binfo { color: var(--muted); font-size: 10px; }

.chap-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(60px, 1fr)); gap: 6px; margin: 20px 0 28px; }
.chap-btn {
  background: var(--card); border: 1px solid var(--border); color: var(--fg);
  padding: 8px 4px; border-radius: 6px; font-size: 13px; text-align: center;
  cursor: pointer; transition: all .15s; font-family: inherit;
}
.chap-btn:hover { border-color: var(--accent); background: rgba(216,166,87,.1); }

#chapter-view { display: none; }
#chapter-content { display: none; }

.verse { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; margin: 14px 0; }
.ref { color: var(--accent); font-weight: 600; font-size: 13px; letter-spacing: .04em; text-transform: uppercase; }
.kjv { margin: 6px 0 0; font-style: italic; }
.plain { margin: 8px 0 0; color: #cfd0d2; line-height: 1.7; }
.kid { margin: 10px 0 0; color: var(--kid); border-left: 3px solid var(--kid); padding-left: 10px; font-style: italic; }
.kid::before { content: "In simple words: "; color: var(--muted); font-style: italic; }
.topic-head { color: var(--accent); font-size: 20px; font-weight: 700; margin: 28px 0 8px; letter-spacing: .03em; }
.topic-sub { color: var(--muted); font-size: 13px; margin-bottom: 16px; }
.nores { color: var(--muted); padding: 40px 0; text-align: center; font-size: 15px; }
.nores strong { display: block; font-size: 18px; color: var(--fg); margin-bottom: 8px; }
.exact-card { background: rgba(216,166,87,.06); border: 1px solid rgba(216,166,87,.3); border-radius: 12px; padding: 18px 20px; margin: 16px 0; }
.exact-card .ref { font-size: 15px; }
.exact-card .kjv { font-size: 16px; line-height: 1.7; }
.search-mode { margin: 12px 0; padding: 10px 14px; background: rgba(122,184,255,.06); border: 1px solid rgba(122,184,255,.2); border-radius: 8px; font-size: 13px; color: var(--blue); }

.ch-nav { display: flex; gap: 8px; align-items: center; margin: 20px 0 12px; flex-wrap: wrap; }
.ch-nav .label { color: var(--muted); font-size: 11px; font-weight: 600; letter-spacing: .05em; text-transform: uppercase; }
.ch-nav button { background: transparent; border: 1px solid var(--border); color: var(--fg); padding: 6px 14px; border-radius: 6px; font-size: 12px; cursor: pointer; font-family: inherit; }
.ch-nav button:hover { border-color: var(--accent); }
.navi { display: flex; gap: 8px; margin: 14px 0; }
.navi button { background: transparent; border: 1px solid var(--border); color: var(--muted); padding: 6px 14px; border-radius: 6px; font-size: 12px; cursor: pointer; font-family: inherit; }
.navi button:hover { border-color: var(--accent); color: var(--fg); }
.back-btn { background: transparent; border: 1px solid var(--border); color: var(--muted); padding: 8px 16px; border-radius: 6px; font-size: 12px; cursor: pointer; font-family: inherit; margin-bottom: 16px; }
.back-btn:hover { border-color: var(--accent); color: var(--fg); }
"""

JS = bpat_js + bcanon_js + bslug_js + """
const VKEYS = BRAIN.filter(n => /^[a-z0-9_]+_\\d+:\\d+$/.test(n.k)).map(n => n.k).sort();
const BYK = {};
BRAIN.forEach(n => BYK[n.k] = n);

function matchBook(q) {
  const ql = q.toLowerCase().trim();
  for (const [slug, pat] of Object.entries(BPATS)) {
    try {
      const re = new RegExp('^(' + pat + ')$', 'i');
      if (re.test(ql)) return slug;
    } catch(e) {}
  }
  return null;
}

function parseRef(q) {
  // "john 3:16" "jn 3:16" "john 3 16" "genesis 1" "genesis 1:1"
  const m = q.match(/^([a-zA-Z0-9_ ]+?)\\s+(\\d+)(?:[:\\s]+(\\d+))?$/);
  if (!m) return null;
  const book = matchBook(m[1]);
  if (!book) return null;
  return { book, chap: parseInt(m[2]), verse: m[3] ? parseInt(m[3]) : null };
}

function getVerses(book, chap) {
  const prefix = book + '_' + chap + ':';
  return VKEYS.filter(k => k.startsWith(prefix)).sort((a, b) => {
    const av = parseInt(a.split(':')[1]);
    const bv = parseInt(b.split(':')[1]);
    return av - bv;
  });
}

function verseBlock(ref) {
  const n = BYK[ref];
  if (!n) return '';
  return '<div class="verse"><div class="ref">' + ref.replace(/_/g, ' ') + '</div><div class="kjv">' + n.v + '</div></div>';
}

function showChapter(book, chap) {
  const refs = getVerses(book, chap);
  const disp = CANON[BOOK_SLUGS.indexOf(book)] || book;
  let maxChap = 1;
  try { maxChap = Math.max(...[...new Set(VKEYS.filter(k => k.startsWith(book + '_')).map(k => parseInt(k.split('_')[1].split(':')[0]))]); } catch(e) {}
  const prevDis = chap <= 1 ? 'disabled' : '';
  const html = `
    <div class="ch-nav">
      <button onclick="showBookPicker()">\\u2190 Books</button>
      <span class="label">${disp} ${chap}</span>
      <button onclick="showChapter('${book}', ${chap-1})" ${prevDis}>\\u2190 Prev</button>
      <button onclick="showChapter('${book}', ${chap+1})">Next \\u2192</button>
    </div>
    <h2 class="topic-head">${disp} ${chap}</h2>
    <div class="topic-sub">Chapter \\u00b7 ${refs.length} verses</div>
    ${refs.map(verseBlock).join('')}
  `;
  document.getElementById('chapter-view').style.display = 'none';
  document.getElementById('chapter-content').style.display = 'block';
  document.getElementById('chapter-content').innerHTML = html;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showBookPicker() {
  const html = BOOK_SLUGS.map((slug, i) => {
    let maxChap = 1;
    try { maxChap = Math.max(...[...new Set(VKEYS.filter(k => k.startsWith(slug + '_')).map(k => parseInt(k.split('_')[1].split(':')[0]))]); } catch(e) {}
    return '<button class="book-btn" onclick="showChapPicker(\\'' + slug + '\\')">' +
      '<span class="bname">' + CANON[i] + '</span>' +
      '<span class="binfo">' + maxChap + ' chaps</span></button>';
  }).join('');
  document.getElementById('chapter-view').style.display = 'block';
  document.getElementById('chapter-view').innerHTML = '<div class="book-grid">' + html + '</div>';
  document.getElementById('chapter-content').style.display = 'none';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showChapPicker(book) {
  const refs = VKEYS.filter(k => k.startsWith(book + '_'));
  const chaps = [...new Set(refs.map(k => parseInt(k.split('_')[1].split(':')[0])))].sort((a, b) => a - b);
  const disp = CANON[BOOK_SLUGS.indexOf(book)] || book;
  const html = '<button class="back-btn" onclick="showBookPicker()">\\u2190 All Books</button>' +
    '<div class="chap-grid" style="display:grid">' +
    chaps.map(c => '<button class="chap-btn" onclick="showChapter(\\'' + book + '\\',' + c + ')">' + c + '</button>').join('') +
    '</div>';
  document.getElementById('chapter-view').style.display = 'block';
  document.getElementById('chapter-view').innerHTML = html;
  document.getElementById('chapter-content').style.display = 'none';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function do_lookup() {
  const q = document.getElementById('lookup').value.trim();
  if (!q) return;
  lookup(q);
  document.getElementById('lookup').blur();
}

document.getElementById('lookup').addEventListener('keydown', e => {
  if (e.key === 'Enter') do_lookup();
});

// ── TRU search ───────────────────────────────────────────────────────────
function truSearch(q) {
  const ql = q.toLowerCase();
  const words = ql.split(/\\s+/).filter(w => w.length > 1);

  // Priority 1: exact reference (john 3:16)
  const ref = parseRef(ql);
  if (ref) {
    const full = ref.book + '_' + ref.chap + ':' + (ref.verse || '1');
    if (BYK[full]) {
      const refs = getVerses(ref.book, ref.chap);
      const disp = CANON[BOOK_SLUGS.indexOf(ref.book)] || ref.book;
      let html = '<div class="search-mode">Exact reference: ' + disp + ' ' + ref.chap + (ref.verse ? ':' + ref.verse : '') + '</div>';
      html += '<h2 class="topic-head">' + disp + ' ' + ref.chap + (ref.verse ? ':' + ref.verse : '') + '</h2>';
      if (ref.verse) {
        const exact = BYK[full];
        html += '<div class="exact-card"><div class="ref">' + full.replace(/_/g, ' ') + '</div><div class="kjv">' + exact.v + '</div></div>';
      } else {
        html += '<div class="topic-sub">Chapter \\u00b7 ' + refs.length + ' verses</div>';
        html += refs.map(verseBlock).join('');
      }
      document.getElementById('chapter-view').style.display = 'none';
      document.getElementById('chapter-content').innerHTML = html;
      document.getElementById('chapter-content').style.display = 'block';
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }
  }

  // Priority 2: direct key match
  let bestKey = null, bestScore = 0;
  for (const k of Object.keys(BYK)) {
    let score = 0;
    const kl = k.toLowerCase();
    for (const w of words) {
      if (kl === w) score += 10;
      else if (kl.startsWith(w)) score += 6;
      else if (kl.includes(w)) score += 3;
    }
    if (score > bestScore) { bestScore = score; bestKey = k; }
  }
  if (bestScore >= 3 && bestKey && VKEYS.includes(bestKey)) {
    const disp = CANON[BOOK_SLUGS.indexOf(bestKey.split('_')[0])] || bestKey.split('_')[0];
    document.getElementById('chapter-view').style.display = 'none';
    document.getElementById('chapter-content').innerHTML = '<button class="back-btn" onclick="showBookPicker()">\\u2190 Books</button>' +
      '<h2 class="topic-head">' + bestKey.replace(/_/g, ' ') + '</h2>' +
      '<div class="exact-card"><div class="ref">' + bestKey.replace(/_/g, ' ') + '</div><div class="kjv">' + BYK[bestKey].v + '</div></div>';
    document.getElementById('chapter-content').style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
    return;
  }

  // Priority 3: full-text search
  const matched = [];
  for (const vk of VKEYS) {
    const n = BYK[vk];
    const vl = n.v.toLowerCase();
    let score = 0;
    for (const w of words) {
      const count = (vl.match(new RegExp(w, 'g')) || []).length;
      score += count;
      if (vk.toLowerCase().includes(w)) score += 2;
    }
    if (score > 0) matched.push({ vk, score, v: n.v });
  }
  matched.sort((a, b) => b.score - a.score);
  const top = matched.slice(0, 15);

  if (top.length === 0) {
    document.getElementById('chapter-view').style.display = 'none';
    document.getElementById('chapter-content').innerHTML = '<div class="nores"><strong>Nothing found for "\\u201c' + q + '\\u201d</strong>Try: "john 3:16" \\u00b7 "genesis 1" \\u00b7 "what is grace" \\u00b7 "psalms 23"</div>';
    document.getElementById('chapter-content').style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
    return;
  }

  let html = '<div class="search-mode">Found ' + top.length + ' results for "\\u201c' + q + '\\u201d"</div>';
  html += top.map(n => '<div class="verse"><div class="ref">' + n.vk.replace(/_/g, ' ') + '</div><div class="kjv">' + (n.v.length > 200 ? n.v.slice(0, 200) + '\\u2026' : n.v) + '</div></div>').join('');
  document.getElementById('chapter-view').style.display = 'none';
  document.getElementById('chapter-content').innerHTML = html;
  document.getElementById('chapter-content').style.display = 'block';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function lookup(q) { truSearch(q); }

// start at book picker
showBookPicker();
"""

# Escape single quotes in the JS string for embedding in HTML
JS_ESC = JS.replace("'", "\\'").replace("\\'", "'")

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Scripture Seeker — TRU KJV Engine</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>{STYLE}</style>
</head>
<body>

<header>
  <h1>✦ Scripture Seeker</h1>
  <span class="stats">{stats}</span>
</header>

<main>

<div class="search-bar">
  <input id="lookup" placeholder="e.g. john 3:16 · genesis 1 · what is love · who is God" autocomplete="off" autofocus>
  <button onclick="do_lookup()">Search</button>
</div>

<div id="chapter-view"></div>
<div id="chapter-content"></div>

</main>

<script>
const BRAIN = JSON.parse(atob("{b64}"));
{JS_ESC}
</script>

</body>
</html>'''

with open(OUT, 'w') as f:
    f.write(HTML)

size = OUT.stat().st_size
node_count = len(nodes)
print(f'Scripture Seeker built: {size//1024}kb, {node_count} nodes embedded')
print(f'Output: {OUT}')