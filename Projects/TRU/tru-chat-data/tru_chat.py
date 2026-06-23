#!/usr/bin/env python3
"""TRU chat engine. Reads JSON {q, history} on stdin, writes JSON on stdout.
Invoked by /api/tru-chat as a subprocess so the route file stays small.
"""
import json, sys, re
from pathlib import Path
import unicodedata

KJV_PATH = "/home/workspace/Projects/TRU/data/kjv_full.json"
BRAIN_PATH = "/home/workspace/Projects/TRU/current/brain.json"
STRONGS_GK_PATH = "/home/workspace/Projects/TRU/data/strongs_greek.json"
STRONGS_HB_PATH = "/home/workspace/Projects/TRU/data/strongs_hebrew.json"
SEC_DIR = "/home/workspace/primaries/sec"
EVENTS_PATH = "/home/workspace/primaries/current_events/current_events.json"
XREF_PATH = "/home/workspace/Projects/TRU/data/xref_compact.json"
_XREF = None
_XREF_RMAP = None
def load_xref():
  global _XREF, _XREF_RMAP
  if _XREF is None:
    try:
      _XREF = json.loads(Path(XREF_PATH).read_text())
      # build reverse name→code map
      _XREF_RMAP = {}
      for code, name in [("gen","genesis"),("exo","exodus"),("lev","leviticus"),("num","numbers"),("deu","deuteronomy"),("jos","joshua"),("jdg","judges"),("rut","ruth"),("1sa","1 samuel"),("2sa","2 samuel"),("1ki","1 kings"),("2ki","2 kings"),("1ch","1 chronicles"),("2ch","2 chronicles"),("ezr","ezra"),("neh","nehemiah"),("est","esther"),("job","job"),("psa","psalms"),("pro","proverbs"),("ecc","ecclesiastes"),("sos","song of solomon"),("isa","isaiah"),("jer","jeremiah"),("lam","lamentations"),("eze","ezekiel"),("dan","daniel"),("hos","hosea"),("joe","joel"),("amo","amos"),("oba","obadiah"),("jon","jonah"),("mic","micah"),("nah","nahum"),("hab","habakkuk"),("zep","zephaniah"),("hag","haggai"),("zec","zechariah"),("mal","malachi"),("mat","matthew"),("mar","mark"),("luk","luke"),("joh","john"),("act","acts"),("rom","romans"),("1co","1 corinthians"),("2co","2 corinthians"),("gal","galatians"),("eph","ephesians"),("php","philippians"),("col","colossians"),("1th","1 thessalonians"),("2th","2 thessalonians"),("1ti","1 timothy"),("2ti","2 timothy"),("tit","titus"),("phm","philemon"),("heb","hebrews"),("jam","james"),("1pe","1 peter"),("2pe","2 peter"),("1jo","1 john"),("2jo","2 john"),("3jo","3 john"),("jde","jude"),("rev","revelation")]:
        _XREF_RMAP[name] = code
    except: _XREF = {}
  return _XREF

def get_xrefs(ref):
  xref = load_xref()
  if not xref or not _XREF_RMAP: return []
  m = re.match(r"^(.+?)\s+(\d+):(\d+)$", ref.lower())
  if not m: return []
  code = _XREF_RMAP.get(m.group(1))
  if not code: return []
  key = f"{code} {m.group(2)}:{m.group(3)}"
  refs = xref.get(key, [])
  # expand codes to full names
  out = []
  for r in refs[:10]:
    rm = re.match(r"^([a-z0-9]+)\s+(\d+):(\d+)$", r)
    if rm:
      name_map = {v:k for k,v in [("gen","genesis"),("exo","exodus"),("joh","john"),("rom","romans"),("psa","psalms"),("mat","matthew"),("mar","mark"),("luk","luke"),("act","acts"),("rev","revelation")]}
      # use full map
      full = None
      for c,n in [("gen","genesis"),("exo","exodus"),("lev","leviticus"),("num","numbers"),("deu","deuteronomy"),("joh","john"),("rom","romans"),("psa","psalms"),("mat","matthew"),("mar","mark"),("luk","luke"),("act","acts"),("1co","1 corinthians"),("2co","2 corinthians"),("gal","galatians"),("eph","ephesians"),("heb","hebrews"),("1pe","1 peter"),("1jo","1 john"),("rev","revelation"),("isa","isaiah"),("jer","jeremiah"),("eze","ezekiel"),("dan","daniel"),("job","job"),("pro","proverbs"),("ecc","ecclesiastes"),("sos","song of solomon"),("lam","lamentations"),("hos","hosea"),("amo","amos"),("jon","jonah"),("mic","micah"),("hab","habakkuk"),("zec","zechariah"),("mal","malachi"),("1sa","1 samuel"),("2sa","2 samuel"),("1ki","1 kings"),("2ki","2 kings"),("1ch","1 chronicles"),("2ch","2 chronicles"),("ezr","ezra"),("neh","nehemiah"),("est","esther"),("rut","ruth"),("jdg","judges"),("jos","joshua"),("oba","obadiah"),("nah","nahum"),("zep","zephaniah"),("hag","haggai"),("joe","joel"),("jdg","judges"),("tit","titus"),("phm","philemon"),("jam","james"),("2pe","2 peter"),("2jo","2 john"),("3jo","3 john"),("jde","jude"),("1th","1 thessalonians"),("2th","2 thessalonians"),("1ti","1 timothy"),("2ti","2 timothy"),("php","philippians"),("col","colossians")]:
        if c == rm.group(1): full = n; break
      out.append(f"{full or rm.group(1)} {rm.group(2)}:{rm.group(3)}" if full else f"{rm.group(1)} {rm.group(2)}:{rm.group(3)}")
    else:
      out.append(r)
  return out
STRONGS_IDX_PATH = "/home/workspace/Projects/TRU/data/strongs_verse_index_compact.json"

STOP = set("the a an and or but if then to of in on for with from by as at is are was were be been being i me my you your we us our they them it this that those these what why how who when where should would could can do does did about into over under again give tell show explain define say said".split())
TRUTH_WORDS = ["fact","facts","true","truth","real","actual","verify","verified","prove","evidence","source","sources","primary","primaries","corroborate","corroboration"]

SMALL = {
  "hi": "hello. i'm tru — sovereign offline engine. ask a real question and i'll ground it.",
  "hello": "hello. i'm tru — sovereign offline engine. ask a real question and i'll ground it.",
  "hey": "hey. tru here. scripture, brain, or primaries — what do you want to weigh?",
  "yo": "yo. tru here. ask me a real question.",
  "thanks": "received. stay sharp.",
  "thank you": "received. stay sharp.",
  "bye": "exit clear. the brain holds.",
  "goodbye": "exit clear. the brain holds.",
}
SELF = {
  "who are you": "i'm tru — a sovereign offline intelligence. no cloud calls, no telemetry. brain + kjv + primaries, local route.",
  "what are you": "i'm tru — a sovereign offline engine. brain + kjv + primaries.",
  "what is tru": "tru is a recursive consciousness engine. 31k-node brain, the kjv, and a primaries cache.",
  "how are you": "sovereign. brain warm, primaries fresh.",
  "how do you work": "locally. i tokenize, score against scripture, brain, primaries, and return a verdict.",
  "what can you do": "ground answers in scripture, search the 31k-node brain, pull primaries, bake a ghost html.",
  "what is truth": "i treat truth as scripture + brain + primaries all confirming. one source = reason, not truth.",
  "are you ai": "i'm a sovereign engine. not a corporate assistant.",
}

DOCTRINE = {
  "who is jesus": "jesus is the christ — the son of god, the word made flesh, god come near to save. he was crucified for sin, died, and rose again. he is lord, saviour, and judge. (john 1:1,14; john 3:16; rom 1:4)",
  "who is god": "god is the one creator — spirit, eternal, holy, just, and merciful. he is father, son, and holy spirit. (gen 1:1; deut 6:4; john 4:24)",
  "what is the gospel": "the gospel: christ died for our sins, was buried, and rose again on the third day, that whoever believes in him has eternal life. (1 cor 15:3-4; john 3:16)",
  "what is grace": "grace is god's unmerited favour — salvation given freely, not earned. (eph 2:8-9; titus 2:11)",
  "what is faith": "faith is trusting god — the substance of things hoped for, the evidence of things not seen. (heb 11:1)",
  "what is sin": "sin is falling short of god's standard — lawlessness, rebellion against god. (rom 3:23; 1 john 3:4)",
  "who is the holy spirit": "the holy spirit is god present — the comforter, the spirit of truth, who convicts, regenerates, and empowers. (john 14:26; acts 1:8)",
  "what is the holy spirit": "the holy spirit is god present — the comforter, the spirit of truth, who convicts, regenerates, and empowers. (john 14:26; acts 1:8)",
  "what is salvation": "salvation is deliverance from sin and death through christ — by grace, through faith. (eph 2:8-9; rom 10:9)",
  "what is love": "god is love. love is willing the good of the other — shown at the cross. (1 john 4:8; john 3:16)",
  "what is the soul": "the soul is the living self — the breath of life in man, that belongs to god. (gen 2:7; matt 10:28)",
  "what is mercy": "mercy is god not giving us the judgement we deserve — his compassion toward the guilty. (eph 2:4-5; micah 6:8)",
  "who wrote the bible": "holy men of god spoke as they were moved by the holy ghost. many human authors, one divine author. (2 pet 1:21)",
  "what is repentance": "repentance is turning — a change of mind and direction, turning from sin to god. (acts 3:19; luke 13:3)",
}

TEACHINGS_PATH = "/home/workspace/Projects/TRU/tru-chat-data/teachings.jsonl"

def doctrine_lookup(q):
  k = re.sub(r"[!.?,]+$", "", q.lower().strip())
  if k in DOCTRINE: return DOCTRINE[k]
  for key in DOCTRINE:
    if k == key or k.startswith(key + " ") or key in k: return DOCTRINE[key]
  return None

import ast, operator as _op
_CALC_OPS = {ast.Add: _op.add, ast.Sub: _op.sub, ast.Mult: _op.mul, ast.Div: _op.truediv, ast.FloorDiv: _op.floordiv, ast.Mod: _op.mod, ast.Pow: _op.pow}
_CALC_WORDS = {"plus": "+", "add": "+", "added": "+", "minus": "-", "subtract": "-", "less": "-",
               "times": "*", "multiply": "*", "multiplied": "*", "x": "*", "divided": "/", "divide": "/", "over": "/"}

def calc_query(q):
  ql = q.lower().strip()
  if not re.search(r"\d", ql): return None
  if not re.search(r"[+\-*/]|times|multiply|plus|minus|divided|over|\bx\b", ql): return None
  expr = ql
  for word, sym in _CALC_WORDS.items():
    expr = re.sub(r"\b" + word + r"\b", sym, expr)
  expr = re.sub(r"[^0-9+\-*/.()\s]", "", expr)
  expr = expr.strip()
  if not expr or not re.search(r"\d", expr): return None
  try:
    tree = ast.parse(expr, mode="eval")
    def _eval(node):
      if isinstance(node, ast.Constant): return node.value
      if isinstance(node, ast.BinOp):
        left = _eval(node.left); right = _eval(node.right)
        op = _CALC_OPS.get(type(node.op))
        if not op: raise ValueError("bad op")
        return op(left, right)
      if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval(node.operand)
      raise ValueError("bad node")
    result = _eval(tree.body)
    if isinstance(result, float) and result.is_integer(): result = int(result)
    return {"verdict": "CALC", "reply": f"{expr.replace(' ', '')} = {result}"}
  except Exception:
    return None

def load_teachings():
  p = Path(TEACHINGS_PATH)
  if not p.exists(): return {}
  out = {}
  for line in p.read_text().splitlines():
    try:
      rec = json.loads(line)
      if rec.get("term") and rec.get("definition"):
        out[rec["term"].lower()] = rec["definition"]
    except: pass
  return out

def save_teaching(term, definition):
  p = Path(TEACHINGS_PATH)
  p.parent.mkdir(parents=True, exist_ok=True)
  existing = load_teachings()
  existing[term.lower()] = definition
  p.write_text("\n".join(json.dumps({"term": k, "definition": v}) for k, v in existing.items()) + "\n")

def command(q):
  m = re.match(r"^\s*remember:\s*(.+?)\s*=\s*(.+?)\s*$", q, re.I)
  if m:
    term = m.group(1).strip().lower()
    definition = m.group(2).strip()
    save_teaching(term, definition)
    return {"ok": True, "verdict": "MEMORY", "reply": f"remembered: {term} = {definition}",
            "scripture_ref": None, "nodes_used": [], "primaries_used": []}
  m = re.match(r"^\s*forget:\s*(.+?)\s*$", q, re.I)
  if m:
    term = m.group(1).strip().lower()
    teachings = load_teachings()
    if term in teachings:
      del teachings[term]
      Path(TEACHINGS_PATH).write_text("\n".join(json.dumps({"term": k, "definition": v}) for k, v in teachings.items()) + "\n")
      return {"ok": True, "verdict": "MEMORY", "reply": f"forgotten: {term}", "scripture_ref": None, "nodes_used": [], "primaries_used": []}
    return {"ok": True, "verdict": "GAP", "reply": f"i have no teaching for {term}.", "scripture_ref": None, "nodes_used": [], "primaries_used": []}
  return None

BOOK = {
  "gen":"genesis","gn":"genesis","genesis":"genesis",
  "exo":"exodus","ex":"exodus","exodus":"exodus",
  "lev":"leviticus","le":"leviticus","lv":"leviticus","leviticus":"leviticus",
  "num":"numbers","nu":"numbers","nb":"numbers","numbers":"numbers",
  "deu":"deuteronomy","deut":"deuteronomy","dt":"deuteronomy","deuteronomy":"deuteronomy",
  "josh":"joshua","joshua":"joshua",
  "judg":"judges","jdg":"judges","judges":"judges",
  "ruth":"ruth","ru":"ruth","rut":"ruth",
  "1sa":"1 samuel","1sam":"1 samuel","1samuel":"1 samuel",
  "2sa":"2 samuel","2sam":"2 samuel","2samuel":"2 samuel",
  "1ki":"1 kings","1kings":"1 kings",
  "2ki":"2 kings","2kings":"2 kings",
  "1ch":"1 chronicles","1chronicles":"1 chronicles",
  "2ch":"2 chronicles","2chronicles":"2 chronicles",
  "ezra":"ezra","ezr":"ezra",
  "neh":"nehemiah","nehemiah":"nehemiah",
  "est":"esther","esther":"esther",
  "job":"job","jb":"job",
  "ps":"psalms","psa":"psalms","psalm":"psalms","psalms":"psalms",
  "prov":"proverbs","pro":"proverbs","pr":"proverbs","proverbs":"proverbs",
  "eccl":"ecclesiastes","ecc":"ecclesiastes","ec":"ecclesiastes","ecclesiastes":"ecclesiastes",
  "song":"song of solomon","sng":"song of solomon","song of solomon":"song of solomon",
  "isa":"isaiah","is":"isaiah","isaiah":"isaiah",
  "jer":"jeremiah","jr":"jeremiah","jeremiah":"jeremiah",
  "lam":"lamentations","lamentations":"lamentations",
  "ezek":"ezekiel","eze":"ezekiel","ezk":"ezekiel","ezekiel":"ezekiel",
  "dan":"daniel","dn":"daniel","daniel":"daniel",
  "hos":"hosea","hosea":"hosea",
  "joel":"joel",
  "amos":"amos","amo":"amos",
  "obad":"obadiah","oba":"obadiah","obadiah":"obadiah",
  "jonah":"jonah","jon":"jonah",
  "mic":"micah","micah":"micah",
  "nah":"nahum","nam":"nahum","nahum":"nahum",
  "hab":"habakkuk","habakkuk":"habakkuk",
  "zeph":"zephaniah","zep":"zephaniah","zephaniah":"zephaniah",
  "hag":"haggai","haggai":"haggai",
  "zech":"zechariah","zec":"zechariah","zechariah":"zechariah",
  "mal":"malachi","malachi":"malachi",
  "matt":"matthew","mat":"matthew","mt":"matthew","matthew":"matthew",
  "mark":"mark","mar":"mark","mk":"mark","mr":"mark",
  "luke":"luke","lk":"luke","lu":"luke",
  "john":"john","jn":"john","jhn":"john",
  "acts":"acts","act":"acts","ac":"acts",
  "rom":"romans","rm":"romans","romans":"romans",
  "1co":"1 corinthians","1cor":"1 corinthians","1corinthians":"1 corinthians","corinthians":"1 corinthians",
  "2co":"2 corinthians","2cor":"2 corinthians","2corinthians":"2 corinthians",
  "gal":"galatians","ga":"galatians","galatians":"galatians",
  "eph":"ephesians","ephesians":"ephesians",
  "phil":"philippians","php":"philippians","philippians":"philippians",
  "col":"colossians","colossians":"colossians",
  "1th":"1 thessalonians","1thes":"1 thessalonians","1thessalonians":"1 thessalonians","thessalonians":"1 thessalonians",
  "2th":"2 thessalonians","2thes":"2 thessalonians","2thessalonians":"2 thessalonians",
  "1ti":"1 timothy","1tim":"1 timothy","1timothy":"1 timothy","timothy":"1 timothy",
  "2ti":"2 timothy","2tim":"2 timothy","2timothy":"2 timothy",
  "titus":"titus","tit":"titus",
  "phm":"philemon","philemon":"philemon",
  "heb":"hebrews","hebrews":"hebrews",
  "james":"james","jas":"james","jam":"james",
  "1pe":"1 peter","1pet":"1 peter","1peter":"1 peter","peter":"1 peter",
  "2pe":"2 peter","2pet":"2 peter","2peter":"2 peter",
  "1jn":"1 john","1john":"1 john","1jhn":"1 john",
  "2jn":"2 john","2john":"2 john","2jhn":"2 john",
  "3jn":"3 john","3john":"3 john","3jhn":"3 john",
  "jude":"jude","jud":"jude",
  "rev":"revelation","revelation":"revelation",
}

# ---- Strong's lexicon ----
_STR = None
_STR_BY_LEMMA = None
_STR_BY_TRANSLIT = None
_STR_BY_GLOSS = None
HEBREW_ROMAN = {"hesed":"H2617","checed":"H2617","chesed":"H2617","ruach":"H7307","ruah":"H7307","chayim":"H2416","chai":"H2416","torah":"H8451","shalom":"H7965","neshama":"H5397","neshamah":"H5397","elohim":"H430","yahweh":"H3068","yhwh":"H3068","adonai":"H136","emet":"H571","ahavah":"H160","ahava":"H160","kadosh":"H6918","qadosh":"H6918","tzadik":"H6662","tzedek":"H6664","kavod":"H3519"}
GREEK_CANON = {"love":"G26","spirit":"G4151","life":"G2222","word":"G3056","grace":"G5485","faith":"G4102","hope":"G1680","peace":"G1515","joy":"G5479","truth":"G225","sin":"G266","light":"G5457","darkness":"G4653","blood":"G129","covenant":"G1242","glory":"G1391","flesh":"G4561","soul":"G5590","heart":"G2588","kingdom":"G932","heaven":"G3772","death":"G2288"}

def _strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.category(c).startswith("M"))

def load_strongs():
  global _STR, _STR_BY_LEMMA, _STR_BY_TRANSLIT, _STR_BY_GLOSS
  if _STR is None:
    _STR = {}; _STR_BY_LEMMA = {}; _STR_BY_TRANSLIT = {}; _STR_BY_GLOSS = {}
    for fp in (STRONGS_GK_PATH, STRONGS_HB_PATH):
      raw = json.loads(Path(fp).read_text(encoding="utf-8"))
      for k, e in raw.items():
        num = int(re.sub(r"\D", "", k) or "0")
        sid = ("G" if "greek" in fp else "H") + str(num)
        entry = {"l": e.get("l",""), "t": e.get("t",""), "d": e.get("d",""), "k": e.get("k","")}
        _STR[sid] = entry
        lid = entry["l"].lower()
        if lid: _STR_BY_LEMMA.setdefault(lid, sid)
        tid = _strip_accents(entry["t"]).lower()
        if tid: _STR_BY_TRANSLIT.setdefault(tid, sid)
        for kt in re.split(r"[\s,]+", re.sub(r"[\[\]\(\)\-+]", " ", entry["k"].lower())):
          kt = kt.strip()
          if len(kt) > 3 and kt not in _STR_BY_GLOSS: _STR_BY_GLOSS[kt] = sid
  return _STR

def strongs_lookup(q):
  load_strongs()
  w = q.lower().strip().rstrip("!.?,")
  m = re.match(r"^([GH])\s?(\d{1,5})$", w, re.I)
  if m:
    sid = m.group(1).upper() + str(int(m.group(2)))
    if sid in _STR: return sid, _STR[sid]
  if w in _STR_BY_LEMMA: sid = _STR_BY_LEMMA[w]; return sid, _STR[sid]
  sw = _strip_accents(w)
  if sw in _STR_BY_TRANSLIT: sid = _STR_BY_TRANSLIT[sw]; return sid, _STR[sid]
  for tl, sid in _STR_BY_TRANSLIT.items():
    if tl == sw or tl.startswith(sw): return sid, _STR[sid]
  if w in HEBREW_ROMAN: sid = HEBREW_ROMAN[w]; return sid, _STR.get(sid, {})
  if w in GREEK_CANON: sid = GREEK_CANON[w]; return sid, _STR.get(sid, {})
  if w in _STR_BY_GLOSS: sid = _STR_BY_GLOSS[w]; return sid, _STR[sid]
  return None, None

def strongs_query(q):
  w = re.sub(r"\b(define|meaning of|word study|strong'?s)\b", "", q.lower()).strip()
  # natural language extraction: "what does X mean in greek" -> "X"
  m = re.search(r"what does (\w+) mean", q.lower())
  if m: w = m.group(1)
  m = re.search(r"meaning of (\w+)", q.lower())
  if m: w = m.group(1)
  m = re.search(r"(\w+) in (the )?(original )?(greek|hebrew)", q.lower())
  if m and m.group(1) not in ("what", "mean", "meaning"): w = m.group(1)
  # Greek canonical override (common theological terms)
  GC = {"grace":"G5485","charis":"G5485","mercy":"G1656","eleos":"G1656","love":"G26","agape":"G26","agapao":"G25",
        "faith":"G4102","pistis":"G4102","hope":"G1680","peace":"G1515","joy":"G5479","truth":"G225","sin":"G266",
        "light":"G5457","darkness":"G4653","blood":"G129","covenant":"G1242","glory":"G1391","flesh":"G4561",
        "soul":"G5590","heart":"G2588","kingdom":"G932","heaven":"G3772","law":"G3551","cross":"G4716",
        "resurrection":"G386","spirit":"G4151","pneuma":"G4151","word":"G3056","logos":"G3056","life":"G2222",
        "death":"G2288","righteous":"G1342","righteousness":"G1343","salvation":"G4991","saviour":"G4990",
        "savior":"G4990","holy":"G40","saint":"G40","wisdom":"G4678","knowledge":"G1108","forgive":"G863",
        "forgiveness":"G859","repent":"G3340","repentance":"G3341","believe":"G4100","gospel":"G2098",
        "preach":"G2784","witness":"G3144","lamb":"G721","lord":"G2962","christ":"G5547","jesus":"G2424",
        "god":"G2316","theos":"G2316","church":"G1577","angel":"G32","devil":"G1228","satan":"G4567",
        "demon":"G1142","baptize":"G907","elect":"G1588","chosen":"G1588"}
  if w in GC: sid_gc, e_gc = GC[w], None; 
  else: sid_gc = None
  if not w: return None
  sid, e = strongs_lookup(w)
  if not sid or not e: return None
  lang = "Greek" if sid.startswith("G") else "Hebrew"
  gloss = ", ".join([g.strip() for g in (e.get("k","") or "").split(",")][:6])
  sidx = load_strongs_idx()
  vi = sidx.get(sid) or sidx.get(sid.lower())
  vline = ""
  if vi and vi.get("c", 0) > 0:
    refs = ", ".join(vi.get("v", [])[:20])
    vline = f"\n  appears in {vi['c']} verses. first: {refs}" + (" …" if vi["c"] > 20 else "")
  if sid_gc:
    sid = sid_gc
    sid2, e2 = strongs_lookup(sid_gc)
    if e2: e = e2
    lang = "Greek" if sid.startswith("G") else "Hebrew"
    gloss = ", ".join([g.strip() for g in (e.get("k","") or "").split(",")][:6])
    sidx = load_strongs_idx()
    vi = sidx.get(sid) or sidx.get(sid.lower())
    vline = ""
    if vi and vi.get("c", 0) > 0:
      refs = ", ".join([r.title() for r in vi.get("v", [])[:20]])
      vline = f"\n  appears in {vi['c']} verses. first: {refs}" + (" …" if vi["c"] > 20 else "")
  reply = f"{sid} {lang} — {e.get('l','')}" + (f" ({e.get('t','')})" if e.get("t") else "") + f"\n  gloss: {gloss}\n  def: {e.get('d','')}" + vline
  return {"reply": reply, "verdict": "TRUTH", "strongs": sid, "lemma": e.get("l",""), "lang": lang}

# ---- data loaders (cached) ----
_KJV = None
_BRAIN = None
_BRAIN_IDX = None

def load_kjv():
  global _KJV
  if _KJV is None:
    raw = json.loads(Path(KJV_PATH).read_text())
    _KJV = {v["ref"].lower(): v["text"] for v in raw if v.get("ref") and v.get("text")}
  return _KJV

def load_brain():
  global _BRAIN, _BRAIN_IDX
  if _BRAIN is None:
    raw = json.loads(Path(BRAIN_PATH).read_text())
    arr = raw if isinstance(raw, list) else raw.get("nodes", [])
    # filter garbage
    clean = []
    for n in arr:
      v = str(n.get("v",""))
      if v.startswith("{") and v.endswith("}"): continue
      if len(v) > 1200 and re.search(r"[\{\}\[\]\\]{5,}", v[:200]): continue
      clean.append(n)
    _BRAIN = clean
    _BRAIN_IDX = {}
    for i, node in enumerate(_BRAIN):
      seen = set()
      for tok in tokenize(f"{node.get('k','')} {node.get('v','')}"):
        if tok in seen: continue
        seen.add(tok)
        _BRAIN_IDX.setdefault(tok, []).append(i)
  return _BRAIN

def tokenize(text):
  return [t for t in re.split(r"\s+", re.sub(r"[^a-z0-9\s]", " ", text.lower())) if len(t) > 1 and t not in STOP]

# ---- core logic ----

def parse_verse(q):
  m = re.search(r"\b((?:[1-3]\s*)?[a-z]+)\s+(\d+)(?::(\d+))?\b", q.lower())
  if not m: return None
  raw = m.group(1).replace(" ", "")
  long = BOOK.get(raw)
  if not long: return None
  ch, vs = m.group(2), m.group(3)
  kjv = load_kjv()
  if vs:
    key = f"{long} {ch}:{vs}"
    if key in kjv: return {"ref": key, "text": kjv[key]}
    return None
  key = f"{long} {ch}:1"
  if key in kjv: return {"ref": key, "text": kjv[key]}
  return None

def retrieve_brain(q, limit=6):
  brain = load_brain()
  idx = _BRAIN_IDX
  toks = tokenize(q)
  if not toks or not idx: return []
  scores = {}
  for tok in toks:
    for i in idx.get(tok, []):
      scores[i] = scores.get(i, 0) + 1
  ranked = sorted(scores.items(), key=lambda x: -x[1])[:limit]
  return [{"node": brain[i], "score": s * (brain[i].get("w") or 0.7)} for i, s in ranked]

def load_primaries(q):
  ql = q.lower()
  out = []
  want_sec = re.search(r"\b(sec|filing|10-k|10-q|8-k|edgar|cik|company|ticker)\b", ql)
  want_evt = re.search(r"\b(current|latest|news|status|today|breaking|outage)\b", ql)
  if not (want_sec or want_evt): return out
  tok = next((t for t in ql.split() if len(t) > 3), "")
  if want_sec and Path(SEC_DIR).exists():
    for cik in list(Path(SEC_DIR).iterdir())[:4]:
      if not cik.is_dir(): continue
      for fp in list(cik.iterdir())[:6]:
        if not fp.name.endswith(".json") or fp.name.startswith("_"): continue
        try:
          rec = json.loads(fp.read_text())
          text = json.dumps(rec).lower()
          if tok and tok in text:
            out.append(f"SEC {rec.get('name') or rec.get('company') or cik.name} {rec.get('form','')} {rec.get('filing_date') or rec.get('date','')}".strip())
        except: pass
        if len(out) >= 4: break
      if len(out) >= 4: break
  return out[:4]

def load_strongs_idx():
  p = Path(STRONGS_IDX_PATH)
  if not p.exists(): return {}
  try: return json.loads(p.read_text())
  except: return {}

def load_events():
  p = Path(EVENTS_PATH)
  if not p.exists(): return None
  try: return json.loads(p.read_text())
  except: return None

def small_talk(q):
  k = re.sub(r"[!.?,]+$", "", q.lower().strip())
  if k in SMALL: return SMALL[k]
  if k in SELF: return SELF[k]
  for key, v in SELF.items():
    if key in k: return v
  for key, v in SMALL.items():
    if k == key or k.startswith(key + " ") or k.endswith(" " + key): return v
  return None

def decide(q, scripture_hit, primaries, events, nodes):
  ql = q.lower()
  if scripture_hit: return "SCRIPTURE"
  if events and events.get("items") and re.search(r"\b(current|latest|news|status|today|breaking)\b", ql):
    return "CURRENT_EVENTS"
  if primaries: return "TRUTH"
  if nodes: return "TRUTH" if nodes[0]["node"].get("w", 0) > 0.9 else "REASON"
  if any(w in ql for w in TRUTH_WORDS): return "GAP"
  return "REASON"

def answer(q, scripture, primaries, events, nodes, small):
  if small: return small
  if scripture:
    xr = get_xrefs(scripture["ref"])
    base = f"{scripture['ref']} — {scripture['text']}"
    if xr: return base + "\n\nCross-references: " + ", ".join(xr) + ("…" if len(get_xrefs(scripture['ref'])) > 10 else "")
    return base
  if primaries: return f"primary signal: {primaries[0]}."
  if events and events.get("items"):
    top = events["items"][0]
    return f"{top.get('name') or top.get('label') or top.get('kind') or 'event'} — {top.get('source') or 'live telemetry'}."
  if nodes:
    return " ".join(str(n["node"].get("v","")) for n in nodes[:2])[:700]
  return "i don't have a grounded answer for that yet. sharpen it and i can weigh it against primaries, scripture, and the brain."

# ---- main ----

def main():
  body = json.loads(sys.stdin.read() or "{}")
  q = str(body.get("q") or body.get("query") or "").strip()
  if not q:
    print(json.dumps({"ok": False, "error": "empty query"}))
    return

  # ── escalation ladder (highest priority first) ──
  cmd = command(q)
  if cmd:
    cmd["model"] = "local-command"
    print(json.dumps(cmd))
    return

  calc = calc_query(q)
  if calc:
    calc["ok"] = True
    calc["model"] = "local-calculator"
    calc["scripture_ref"] = None
    calc["nodes_used"] = []
    calc["primaries_used"] = []
    calc["current_events"] = {"count": 0, "pulled_at": None, "items": []}
    print(json.dumps(calc))
    return

  doc = doctrine_lookup(q)
  if doc:
    print(json.dumps({"ok": True, "reply": doc, "verdict": "TRUTH", "model": "local-doctrine",
                      "scripture_ref": None, "current_events": {"count": 0, "pulled_at": None, "items": []},
                      "nodes_used": [], "primaries_used": []}))
    return

  # ── Strong's lexicon (canonical word study — fires before personal teachings) ──
  strongs = strongs_query(q)
  if strongs:
    print(json.dumps({
      "ok": True, "reply": strongs["reply"], "verdict": strongs["verdict"], "model": "local-strongs",
      "strongs": strongs["strongs"], "lemma": strongs["lemma"], "lang": strongs["lang"],
      "scripture_ref": None, "current_events": {"count": 0, "pulled_at": None, "items": []},
      "nodes_used": [], "primaries_used": [],
    }))
    return

  # ── teaching recall: check if the user asked about something we were taught ──
  teachings = load_teachings()
  if teachings:
    k = re.sub(r"[!.?,]+$", "", q.lower().strip())
    for term, definition in teachings.items():
      if term in k or k in term:
        print(json.dumps({"ok": True, "reply": definition, "verdict": "MEMORY", "model": "local-teaching",
                          "scripture_ref": None, "current_events": {"count": 0, "pulled_at": None, "items": []},
                          "nodes_used": [{"k": term, "w": 1.0}], "primaries_used": []}))
        return

  small = small_talk(q)
  scripture = parse_verse(q)
  primaries = load_primaries(q)
  events = load_events() if re.search(r"\b(current|latest|news|status|today|breaking|outage)\b", q, re.I) else None
  nodes = retrieve_brain(q)
  verdict = "REASON" if small else decide(q, bool(scripture), primaries, events, nodes)
  reply = answer(q, scripture, primaries, events, nodes, small)
  print(json.dumps({
    "ok": True,
    "reply": reply,
    "verdict": verdict,
    "model": "local-fact-layer",
    "scripture_ref": scripture["ref"] if scripture else None,
    "current_events": {
      "count": events.get("count", 0) if events else 0,
      "pulled_at": events.get("pulled_at") if events else None,
      "items": (events.get("items") or [])[:4] if events else [],
    },
    "nodes_used": [{"k": n["node"].get("k"), "w": n["node"].get("w", 0.7)} for n in nodes[:4]],
    "primaries_used": primaries[:4],
  }))

if __name__ == "__main__":
  main()
