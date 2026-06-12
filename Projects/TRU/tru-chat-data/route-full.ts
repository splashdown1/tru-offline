import type { Context } from "hono";
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join } from "node:path";

const BRAIN_PATH = "/home/workspace/Projects/TRU/current/brain.json";
const KJV_PATH = "/home/workspace/Projects/TRU/data/kjv_full.json";
const SEC_DIR = "/home/workspace/primaries/sec";
const TEMPLE_FILE = "/home/workspace/primaries/temple/temple_posts.json";
const ARXIV_DIR = "/home/workspace/primaries/arxiv";
const EVENTS_PATH = "/home/workspace/primaries/current_events/current_events.json";

const STOP = new Set("the a an and or but if then to of in on for with from by as at is are was were be been being i me my you your we us our they them it this that those these what why how who when where should would could can do does did about into over under again give tell show explain define say said".split(" "));
const TRUTH_WORDS = ["fact","facts","true","truth","real","actual","verify","verified","prove","evidence","source","sources","primary","primaries","corroborate","corroboration"];

const BOOK_LONG: Record<string, string> = {
  gen:"genesis",gn:"genesis",genesis:"genesis",
  ex:"exodus",exo:"exodus",exodus:"exodus",
  lv:"leviticus",lev:"leviticus",le:"leviticus",leviticus:"leviticus",
  nu:"numbers",num:"numbers",nb:"numbers",numbers:"numbers",
  dt:"deuteronomy",deut:"deuteronomy",deu:"deuteronomy",deuteronomy:"deuteronomy",
  josh:"joshua",joshua:"joshua",
  jdg:"judges",judg:"judges",judges:"judges",
  ru:"ruth",rut:"ruth",ruth:"ruth",
  "1sa":"1 samuel","1samuel":"1 samuel",
  "2sa":"2 samuel","2samuel":"2 samuel",
  "1ki":"1 kings","1kings":"1 kings",
  "2ki":"2 kings","2kings":"2 kings",
  "1ch":"1 chronicles","1chronicles":"1 chronicles",
  "2ch":"2 chronicles","2chronicles":"2 chronicles",
  ezr:"ezra",ezra:"ezra",
  neh:"nehemiah",nehemiah:"nehemiah",
  est:"esther",esther:"esther",
  job:"job",jb:"job",
  ps:"psalms",psa:"psalms",psalm:"psalms",psalms:"psalms",
  prov:"proverbs",pro:"proverbs",pr:"proverbs",proverbs:"proverbs",
  ec:"ecclesiastes",ecc:"ecclesiastes",eccl:"ecclesiastes",ecclesiastes:"ecclesiastes",
  sng:"song of solomon",song:"song of solomon","song of solomon":"song of solomon",
  isa:"isaiah",is:"isaiah",isaiah:"isaiah",
  jer:"jeremiah",jr:"jeremiah",jeremiah:"jeremiah",
  lam:"lamentations",lamentations:"lamentations",
  ezk:"ezekiel",ezek:"ezekiel",eze:"ezekiel",ezekiel:"ezekiel",
  dan:"daniel",dn:"daniel",daniel:"daniel",
  hos:"hosea",hosea:"hosea",
  joel:"joel",amo:"amos",amos:"amos",oba:"obadiah",obadiah:"obadiah",
  jon:"jonah",jonah:"jonah",mic:"micah",micah:"micah",nam:"nahum",nahum:"nahum",
  hab:"habakkuk",habakkuk:"habakkuk",
  zep:"zephaniah",zephaniah:"zephaniah",hag:"haggai",haggai:"haggai",
  zec:"zechariah",zechariah:"zechariah",mal:"malachi",malachi:"malachi",
  mt:"matthew",matt:"matthew",mat:"matthew",matthew:"matthew",
  mk:"mark",mar:"mark",mr:"mark",mark:"mark",
  lk:"luke",lu:"luke",luke:"luke",
  jn:"john",jhn:"john",john:"john",
  ac:"acts",acts:"acts",act:"acts",
  rom:"romans",rm:"romans",romans:"romans",
  "1co":"1 corinthians","1cor":"1 corinthians","1corinthians":"1 corinthians","corinthians":"1 corinthians",
  "2co":"2 corinthians","2cor":"2 corinthians","2corinthians":"2 corinthians",
  gal:"galatians",ga:"galatians",galatians:"galatians",
  eph:"ephesians",ephesians:"ephesians",
  phil:"philippians",php:"philippians",philippians:"philippians",
  col:"colossians",colossians:"colossians",
  "1th":"1 thessalonians","1thes":"1 thessalonians","1thessalonians":"1 thessalonians","thessalonians":"1 thessalonians",
  "2th":"2 thessalonians","2thes":"2 thessalonians","2thessalonians":"2 thessalonians",
  "1ti":"1 timothy","1tim":"1 timothy","1timothy":"1 timothy","timothy":"1 timothy",
  "2ti":"2 timothy","2tim":"2 timothy","2timothy":"2 timothy",
  tit:"titus",titus:"titus",
  phm:"philemon",philemon:"philemon",
  heb:"hebrews",hebrews:"hebrews",
  jas:"james",jam:"james",james:"james",
  "1pe":"1 peter","1pet":"1 peter","1peter":"1 peter","peter":"1 peter",
  "2pe":"2 peter","2pet":"2 peter","2peter":"2 peter",
  "1jn":"1 john","1john":"1 john","1jhn":"1 john",
  "2jn":"2 john","2john":"2 john","2jhn":"2 john",
  "3jn":"3 john","3john":"3 john","3jhn":"3 john",
  jud:"jude",jude:"jude",
  rev:"revelation",revelation:"revelation",
};

let brainCache: any[] | null = null;
let brainIndex: Map<string, number[]> | null = null;
let kjvCache: Record<string,string> | null = null;

function tokenize(text: string): string[] {
  return text.toLowerCase().replace(/[^a-z0-9\s]/g," ").split(/\s+/).filter(t => t.length>1 && !STOP.has(t));
}

function isGarbage(n: any): boolean {
  if (!n || !n.k) return true;
  const v = String(n.v || "");
  if (v.startsWith("{") && v.endsWith("}")) return true;
  if (v.length>1200 && /[\{\}\[\]\\]{5,}/.test(v.slice(0,200))) return true;
  return false;
}

function loadBrain() {
  if (brainCache) return brainCache;
  try {
    const raw = JSON.parse(readFileSync(BRAIN_PATH, "utf8"));
    const arr = Array.isArray(raw) ? raw : Array.isArray(raw?.nodes) ? raw.nodes : [];
    brainCache = arr.filter((n:any)=>!isGarbage(n));
    brainIndex = new Map();
    for (let i=0;i<brainCache.length;i++) {
      const node = brainCache[i];
      const seen = new Set<string>();
      for (const tok of tokenize(`${node.k} ${node.v}`)) {
        if (seen.has(tok)) continue;
        seen.add(tok);
        const a = brainIndex.get(tok) || [];
        a.push(i);
        brainIndex.set(tok, a);
      }
    }
  } catch { brainCache = []; brainIndex = new Map(); }
  return brainCache;
}

function loadKJV() {
  if (kjvCache) return kjvCache;
  try {
    const raw = JSON.parse(readFileSync(KJV_PATH, "utf8"));
    const out: Record<string,string> = {};
    if (Array.isArray(raw)) {
      for (const v of raw) {
        if (v?.ref && v?.text) {
          const ref = String(v.ref).toLowerCase();
          out[ref] = String(v.text);
        }
      }
    } else Object.assign(out, raw);
    kjvCache = out;
  } catch { kjvCache = {}; }
  return kjvCache;
}

function parseVerse(q: string): { ref: string; text: string } | null {
  const m = q.toLowerCase().match(/\b((?:[1-3]\s*)?[a-z]+)\s+(\d+)(?::(\d+))?\b/);
  if (!m) return null;
  const raw = m[1].replace(/\s+/g,"");
  const long = BOOK_LONG[raw];
  if (!long) return null;
  const chapter = m[2];
  const verse = m[3];
  const kjv = loadKJV();
  if (verse) {
    const key = `${long} ${chapter}:${verse}`;
    if (kjv[key]) return { ref: key, text: kjv[key] };
    return null;
  }
  const key = `${long} ${chapter}:1`;
  if (kjv[key]) return { ref: key, text: kjv[key] };
  return null;
}

function retrieveBrain(q: string) {
  const brain = loadBrain();
  const idx = brainIndex;
  if (!brain.length || !idx) return [];
  const toks = tokenize(q);
  if (!toks.length) return [];
  const scores = new Map<number, number>();
  for (const tok of toks) for (const i of idx.get(tok) || []) scores.set(i, (scores.get(i)||0)+1);
  return [...scores.entries()]
    .map(([i,s])=>({ node: brain[i], score: s * (brain[i].w || 0.7) }))
    .sort((a,b)=>b.score-a.score)
    .slice(0,6)
    .map(r=>r.node);
}

function loadPrimaries(query: string): string[] {
  const q = query.toLowerCase();
  const out: string[] = [];
  const wantSec = /\b(sec|filing|10-k|10-q|8-k|edgar|cik|company|ticker)\b/.test(q);
  const wantArxiv = /\b(arxiv|paper|preprint|study|research)\b/.test(q);
  const wantTemple = /\b(temple|heifer|post|thread|blog)\b/.test(q);
  const wantEvent = /\b(current|latest|news|status|today|breaking|outage)\b/.test(q);
  if (!wantSec && !wantArxiv && !wantTemple && !wantEvent) return out;
  const tok = q.split(/\s+/).find(t => t.length > 3) || "";

  if (wantSec && existsSync(SEC_DIR)) {
    try {
      for (const cikDir of readdirSync(SEC_DIR, { withFileTypes: true })) {
        if (!cikDir.isDirectory()) continue;
        const cikPath = join(SEC_DIR, cikDir.name);
        for (const fp of readdirSync(cikPath).slice(0,6)) {
          if (!fp.endsWith(".json") || fp.startsWith("_")) continue;
          try {
            const rec = JSON.parse(readFileSync(join(cikPath, fp), "utf8"));
            const text = JSON.stringify(rec).toLowerCase();
            if (tok && text.includes(tok)) out.push(`SEC ${rec.name||rec.company||cikDir.name} ${rec.form||""} ${rec.filing_date||rec.date||""}`.trim());
          } catch {}
        }
        if (out.length >= 4) break;
      }
    } catch {}
  }

  if (wantTemple && existsSync(TEMPLE_FILE)) {
    try {
      const posts = JSON.parse(readFileSync(TEMPLE_FILE, "utf8"));
      if (Array.isArray(posts)) for (const post of posts.slice(0,12)) {
        const text = `${post.title||""} ${post.content||""}`.toLowerCase();
        if (tok && text.includes(tok)) out.push(`TEMPLE ${post.title||"post"}`);
        if (out.length >= 6) break;
      }
    } catch {}
  }

  if (wantArxiv && existsSync(ARXIV_DIR)) {
    try {
      for (const cat of readdirSync(ARXIV_DIR, { withFileTypes: true })) {
        if (!cat.isDirectory()) continue;
        const catPath = join(ARXIV_DIR, cat.name);
        for (const fp of readdirSync(catPath).slice(0,6)) {
          if (!fp.endsWith(".json") || fp.startsWith("_")) continue;
          try {
            const paper = JSON.parse(readFileSync(join(catPath, fp), "utf8"));
            const text = `${paper.title||""} ${paper.abstract||paper.summary||""}`.toLowerCase();
            if (tok && text.includes(tok)) out.push(`ARXIV ${paper.title||"paper"}`);
          } catch {}
          if (out.length >= 6) break;
        }
        if (out.length >= 6) break;
      }
    } catch {}
  }

  return out.slice(0,6);
}

function loadEvents() {
  try {
    if (!existsSync(EVENTS_PATH)) return null;
    return JSON.parse(readFileSync(EVENTS_PATH, "utf8"));
  } catch { return null; }
}

const SMALL: Record<string,string> = {
  "hi":"hello. i am tru - sovereign offline engine. ask a real question and i will ground it.",
  "hello":"hello. i am tru - sovereign offline engine. ask a real question and i will ground it.",
  "hey":"hey. tru here. scripture, brain, or primaries - what do you want to weigh?",
  "yo":"yo. tru here. ask me a real question.",
  "thanks":"received. stay sharp.",
  "thank you":"received. stay sharp.",
  "bye":"exit clear. the brain holds.",
  "goodbye":"exit clear. the brain holds.",
};

const SELF: Record<string,string> = {
  "who are you":"i am tru - a sovereign offline intelligence. no cloud calls, no telemetry. brain + kjv + primaries, local route.",
  "what are you":"i am tru - a sovereign offline engine. brain + kjv + primaries.",
  "what is tru":"tru is a recursive consciousness engine. 31k-node brain, the kjv, and a primaries cache.",
  "how are you":"sovereign. brain warm, primaries fresh.",
  "how do you work":"locally. i tokenize, score against scripture, brain, primaries, and return a verdict.",
  "what can you do":"ground answers in scripture, search the 31k-node brain, pull primaries, bake a ghost html.",
  "what is truth":"i treat truth as scripture + brain + primaries all confirming. one source = reason, not truth.",
  "are you ai":"i am a sovereign engine. not a corporate assistant.",
};

function smallTalk(q: string): string | null {
  const k = q.toLowerCase().trim().replace(/[!.?,]+$/,"");
  if (SMALL[k]) return SMALL[k];
  if (SELF[k]) return SELF[k];
  for (const key of Object.keys(SELF)) if (k.includes(key)) return SELF[key];
  for (const key of Object.keys(SMALL)) if (k===key || k.startsWith(key+" ") || k.endsWith(" "+key)) return SMALL[key];
  return null;
}

function decideVerdict(q: string, scriptureHit: boolean, primaries: string[], events: any, nodes: any[]): string {
  const ql = q.toLowerCase();
  if (scriptureHit) return "SCRIPTURE";
  if (events?.items?.length && /\b(current|latest|news|status|today|breaking)\b/.test(ql)) return "CURRENT_EVENTS";
  if (primaries.length) return "TRUTH";
  if (nodes.length) return nodes[0].w && nodes[0].w > 0.9 ? "TRUTH" : "REASON";
  if (TRUTH_WORDS.some(w => ql.includes(w))) return "GAP";
  return "REASON";
}

function answer(q: string, scripture: {ref:string;text:string}|null, primaries: string[], events: any, nodes: any[], small: string|null): string {
  if (small) return small;
  if (scripture) return `${scripture.ref} - ${scripture.text}`;
  if (primaries.length) return `primary signal: ${primaries[0]}.`;
  if (events?.items?.length) {
    const top = events.items[0];
    return `${top.name||top.label||top.kind||"event"} - ${top.source||"live telemetry"}.`;
  }
  if (nodes.length) return nodes.slice(0,2).map((n:any)=>n.v).join(" ").slice(0,700);
  return `i don't have a grounded answer for that yet. sharpen it and i can weigh it against primaries, scripture, and the brain.`;
}

export default async (c: Context) => {
  if (c.req.method !== "POST") {
    const brain = loadBrain();
    return c.json({ ok: true, model: "local-fact-layer", brain_loaded: !!brain.length, brain_size: brain.length });
  }
  let body: any = {};
  try { body = await c.req.json(); } catch { return c.json({ ok: false, error: "invalid json" }, 400); }
  const query = String(body.query || body.q || "").trim();
  if (!query) return c.json({ ok: false, error: "empty query" }, 400);
  const small = smallTalk(query);
  const scripture = parseVerse(query);
  const primaries = loadPrimaries(query);
  const events = /\b(current|latest|news|status|today|breaking|outage)\b/i.test(query) ? loadEvents() : null;
  const nodes = retrieveBrain(query);
  const verdict = small ? "REASON" : decideVerdict(query, !!scripture, primaries, events, nodes);
  const reply = answer(query, scripture, primaries, events, nodes, small);
  return c.json({
    reply, verdict, model: "local-fact-layer",
    scripture_ref: scripture?.ref || null,
    current_events: events ? { count: events.count || 0, pulled_at: events.pulled_at || null, items: (events.items||[]).slice(0,4) } : null,
    nodes_used: nodes.slice(0,4).map((n:any)=>({ k: n.k, w: n.w || 0.7 })),
    primaries_used: primaries.slice(0,4),
  });
};
