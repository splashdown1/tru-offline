// TRU chat helpers — split into its own file so the route
// stays under the platform's per-route size cap.

import { readFileSync, existsSync } from "node:fs";

export const BRAIN_PATH = "/home/workspace/Projects/TRU/current/brain.json";
export const KJV_PATH = "/home/workspace/Projects/TRU/data/kjv_full.json";
export const SEC_DIR = "/home/workspace/primaries/sec";
export const TEMPLE_FILE = "/home/workspace/primaries/temple/temple_posts.json";
export const ARXIV_DIR = "/home/workspace/primaries/arxiv";
export const EVENTS_PATH = "/home/workspace/primaries/current_events/current_events.json";

const STOP = new Set("the a an and or but if then to of in on for with from by as at is are was were be been being i me my you your we us our they them it this that those these what why how who when where should would could can do does did about into over under again give tell show explain define say said".split(" "));

export const TRUTH_WORDS = ["fact", "facts", "true", "truth", "real", "actual", "verify", "verified", "prove", "evidence", "source", "sources", "primary", "primaries", "corroborate", "corroboration"];

export type BrainNode = { k: string; v: string; w?: number; t?: string; source?: string; ref?: string };
export type MemoryEntry = { role: "user" | "tru"; content: string; ts?: string };

let brainCache: BrainNode[] | null = null;
let brainIndex: Map<string, number[]> | null = null;
let kjvCache: Record<string, string> | null = null;
let currentEventsCache: any = null;
let currentEventsAt = 0;

export function tokenize(text: string): string[] {
  return text.toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/).filter((t) => t.length > 1 && !STOP.has(t));
}

export function isGarbageNode(n: any): boolean {
  if (!n || !n.k) return true;
  const v = String(n.v || "");
  if (v.startsWith("{") && v.endsWith("}")) return true;
  if (v.length > 1200 && /[\{\}\[\]\\]{5,}/.test(v.slice(0, 200))) return true;
  return false;
}

export function loadBrain(): BrainNode[] {
  if (brainCache) return brainCache;
  try {
    const raw = JSON.parse(readFileSync(BRAIN_PATH, "utf8"));
    const arr = Array.isArray(raw) ? raw : Array.isArray(raw?.nodes) ? raw.nodes : [];
    brainCache = arr.filter((n: any) => !isGarbageNode(n));
    brainIndex = new Map();
    for (let i = 0; i < brainCache.length; i++) {
      const node = brainCache[i];
      const seen = new Set<string>();
      for (const tok of tokenize(`${node.k} ${node.v}`)) {
        if (seen.has(tok)) continue;
        seen.add(tok);
        const arr = brainIndex.get(tok) || [];
        arr.push(i);
        brainIndex.set(tok, arr);
      }
    }
  } catch {
    brainCache = [];
    brainIndex = new Map();
  }
  return brainCache;
}

export function loadKJV(): Record<string, string> {
  if (kjvCache) return kjvCache;
  try {
    const raw = JSON.parse(readFileSync(KJV_PATH, "utf8"));
    const out: Record<string, string> = {};
    if (Array.isArray(raw)) {
      for (const v of raw) {
        if (v?.ref && v?.text) {
          const ref = String(v.ref).toLowerCase();
          out[ref] = String(v.text);
          if (v.abbrev) out[String(v.abbrev).toLowerCase()] = String(v.text);
        }
      }
    } else {
      Object.assign(out, raw);
    }
    kjvCache = out;
  } catch {
    kjvCache = {};
  }
  return kjvCache;
}

export function loadCurrentEvents() {
  const now = Date.now();
  if (currentEventsCache && now - currentEventsAt < 30_000) return currentEventsCache;
  try {
    if (!existsSync(EVENTS_PATH)) return null;
    currentEventsCache = JSON.parse(readFileSync(EVENTS_PATH, "utf8"));
    currentEventsAt = now;
    return currentEventsCache;
  } catch {
    return null;
  }
}

// Short -> long book-name map. The kjv stores refs with long book names
// ("John 3:16", "Psalms 23:1"). When we see "jn 3:16" or "psalm 23",
// we resolve to the long name and look it up.
const BOOK_LONG: Record<string, string> = {
  gen: "genesis", gn: "genesis", genesis: "genesis",
  ex: "exodus", exo: "exodus", exodus: "exodus",
  lv: "leviticus", lev: "leviticus", le: "leviticus",
  nu: "numbers", num: "numbers", nb: "numbers",
  dt: "deuteronomy", deut: "deuteronomy", deu: "deuteronomy",
  jdg: "judges", judg: "judges",
  ru: "ruth", rut: "ruth",
  "1sa": "1 samuel", "2sa": "2 samuel",
  "1ki": "1 kings", "2ki": "2 kings",
  "1ch": "1 chronicles", "2ch": "2 chronicles",
  ezr: "ezra", neh: "nehemiah", est: "esther",
  job: "job", jb: "job",
  ps: "psalms", psa: "psalms", psalm: "psalms", psalms: "psalms",
  prov: "proverbs", pro: "proverbs", pr: "proverbs",
  ec: "ecclesiastes", ecc: "ecclesiastes", eccl: "ecclesiastes",
  sng: "song of solomon", song: "song of solomon",
  isa: "isaiah", is: "isaiah",
  jer: "jeremiah", jr: "jeremiah",
  lam: "lamentations",
  ezk: "ezekiel", ezek: "ezekiel", eze: "ezekiel",
  dan: "daniel", dn: "daniel",
  hos: "hosea", joel: "joel", amo: "amos", oba: "obadiah",
  jon: "jonah", mic: "micah", nam: "nahum", hab: "habakkuk",
  zep: "zephaniah", hag: "haggai", zec: "zechariah", mal: "malachi",
  mt: "matthew", matt: "matthew", mat: "matthew",
  mk: "mark", mar: "mark", mr: "mark",
  lk: "luke", lu: "luke",
  jn: "john", jhn: "john", john: "john",
  ac: "acts", acts: "acts", act: "acts",
  rom: "romans", rm: "romans",
  "1co": "1 corinthians", "1cor": "1 corinthians", "1corinthians": "1 corinthians",
  "2co": "2 corinthians", "2cor": "2 corinthians", "2corinthians": "2 corinthians",
  gal: "galatians", ga: "galatians", galatians: "galatians",
  eph: "ephesians", ephesians: "ephesians",
  phil: "philippians", php: "philippians", philippians: "philippians",
  col: "colossians", colossians: "colossians",
  "1th": "1 thessalonians", "1thes": "1 thessalonians", "1thessalonians": "1 thessalonians",
  "2th": "2 thessalonians", "2thes": "2 thessalonians", "2thessalonians": "2 thessalonians",
  "1ti": "1 timothy", "1tim": "1 timothy", "1timothy": "1 timothy",
  "2ti": "2 timothy", "2tim": "2 timothy", "2timothy": "2 timothy",
  tit: "titus", titus: "titus",
  phm: "philemon", philemon: "philemon",
  heb: "hebrews", hebrews: "hebrews",
  jas: "james", jam: "james", james: "james",
  "1pe": "1 peter", "1pet": "1 peter", "1peter": "1 peter",
  "2pe": "2 peter", "2pet": "2 peter", "2peter": "2 peter",
  "1jn": "1 john", "1john": "1 john", "1jhn": "1 john",
  "2jn": "2 john", "2john": "2 john", "2jhn": "2 john",
  "3jn": "3 john", "3john": "3 john", "3jhn": "3 john",
  jud: "jude", jude: "jude",
  rev: "revelation", revelation: "revelation",
};

// Try a few ref variants so we hit whether the kjv is keyed with
// long or short book names.
function lookupKJV(candidates: string[]): string | null {
  const kjv = loadKJV();
  for (const c of candidates) {
    if (kjv[c]) return kjv[c];
  }
  return null;
}

export function parseVerse(q: string): { ref: string; text: string } | null {
  const m = q.toLowerCase().match(/\b((?:[1-3]\s*)?[a-z]+)\s+(\d+):(\d+)\b/);
  if (!m) return null;
  const raw = m[1].replace(/\s+/g, "");
  const long = BOOK_LONG[raw];
  if (!long) return null;
  const chapter = m[2];
  const verse = m[3];
  const candidates = [
    `${long} ${chapter}:${verse}`,
    `${long} ${chapter} :${verse}`,
  ];
  const text = lookupKJV(candidates);
  if (text) return { ref: `${long} ${chapter}:${verse}`, text };
  return null;
}

export function retrieveBrain(q: string): BrainNode[] {
  const brain = loadBrain();
  const idx = brainIndex;
  if (!brain.length || !idx) return [];
  const toks = tokenize(q);
  if (!toks.length) return [];
  const scores = new Map<number, number>();
  for (const tok of toks) {
    for (const i of idx.get(tok) || []) scores.set(i, (scores.get(i) || 0) + 1);
  }
  return [...scores.entries()]
    .map(([i, score]) => ({ node: brain[i], score: score * (brain[i].w || 0.7) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 6)
    .map((r) => r.node);
}
