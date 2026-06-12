#!/usr/bin/env python3
"""TRU chat engine. Reads JSON {q, history} on stdin, writes JSON on stdout.
Invoked by /api/tru-chat as a subprocess so the route file stays small.
"""
import json, sys, re
from pathlib import Path

KJV_PATH = "/home/workspace/Projects/TRU/data/kjv_full.json"
BRAIN_PATH = "/home/workspace/Projects/TRU/current/brain.json"
SEC_DIR = "/home/workspace/primaries/sec"
EVENTS_PATH = "/home/workspace/primaries/current_events/current_events.json"

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
  if scripture: return f"{scripture['ref']} — {scripture['text']}"
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
