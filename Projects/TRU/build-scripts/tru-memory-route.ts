import type { Context } from "hono";
import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from "node:fs";
import { join } from "node:path";

const MEM_DIR = "/home/workspace/Projects/TRU/memory";
const TEACH_FILE = join(MEM_DIR, "teachings.jsonl");
const TURN_FILE = join(MEM_DIR, "turns.jsonl");
const RECALL_FILE = join(MEM_DIR, "recall_cache.json");

mkdirSync(MEM_DIR, { recursive: true });
for (const f of [TEACH_FILE, TURN_FILE]) if (!existsSync(f)) writeFileSync(f, "");

// simple jsonl append
function append(path: string, obj: any) {
  writeFileSync(path, JSON.stringify(obj) + "\n", { flag: "a" });
}

// load all jsonl
function loadAll(path: string): any[] {
  try {
    return readFileSync(path, "utf-8").split("\n").filter(Boolean).map((l) => JSON.parse(l));
  } catch {
    return [];
  }
}

// naive keyword score for recall
function score(text: string, q: string): number {
  const t = text.toLowerCase();
  let s = 0;
  for (const w of q.toLowerCase().split(/\W+/).filter((x) => x.length > 2)) {
    if (t.includes(w)) s += 1;
  }
  return s;
}

export default async (c: Context) => {
  const method = c.req.method;

  if (method === "GET") {
    const q = c.req.query("q") || "";
    const limit = Math.min(parseInt(c.req.query("limit") || "12"), 50);
    const teachings = loadAll(TEACH_FILE);
    const turns = loadAll(TURN_FILE);
    let recall: any[] = [];
    try {
      recall = existsSync(RECALL_FILE) ? JSON.parse(readFileSync(RECALL_FILE, "utf-8")) : [];
    } catch {
      recall = [];
    }
    // score every source against the query
    const pool = [
      ...teachings.map((x) => ({ kind: "teaching", text: `${x.term || ""} = ${x.definition || ""}`, meta: x })),
      ...turns.slice(-200).map((x) => ({ kind: "turn", text: `${x.q || ""} → ${x.reply || ""}`, meta: x })),
      ...recall.map((x) => ({ kind: "cloud", text: `${x.subject || ""} ${x.body || ""}`, meta: x })),
    ];
    const ranked = (q ? pool.map((x) => ({ ...x, _s: score(x.text, q) })).filter((x) => x._s > 0).sort((a, b) => b._s - a._s) : pool.slice(-limit)).slice(0, limit);
    return c.json({
      ok: true,
      query: q,
      count: ranked.length,
      recall: ranked.map(({ kind, text, meta, _s }: any) => ({ kind, text: text.slice(0, 600), score: _s, ts: meta?.ts })),
      stats: { teachings: teachings.length, turns: turns.length, cloud: recall.length },
    });
  }

  if (method === "POST") {
    let body: any;
    try {
      body = await c.req.json();
    } catch {
      return c.json({ ok: false, error: "invalid json" }, 400);
    }
    const kind = body.kind || "turn";
    const ts = Date.now();
    if (kind === "teaching") {
      const rec = { ts, term: String(body.term || "").trim(), definition: String(body.definition || "").trim(), verdict: body.verdict, source: body.source || "taught" };
      if (!rec.term || !rec.definition) return c.json({ ok: false, error: "term + definition required" }, 400);
      append(TEACH_FILE, rec);
      return c.json({ ok: true, saved: "teaching", term: rec.term, to_cloud: "queued for daily sync" });
    }
    // default: turn
    const rec = { ts, q: String(body.q || "").slice(0, 500), reply: String(body.reply || "").slice(0, 1200), verdict: body.verdict || "REASON", nodes: Array.isArray(body.nodes) ? body.nodes.slice(0, 4) : [] };
    append(TURN_FILE, rec);
    return c.json({ ok: true, saved: "turn", to_cloud: "queued for daily sync" });
  }

  return c.json({ ok: false, error: "use GET or POST" }, 405);
};
