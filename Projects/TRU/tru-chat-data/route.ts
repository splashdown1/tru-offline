import type { Context } from "hono";
import { parseVerse, retrieveBrain, loadCurrentEvents, type MemoryEntry } from "./parseVerse";
import { loadPrimaries, decideVerdict, lookupSmallTalk, answerFromContext } from "./context";
export default async (c: Context) => {
  if (c.req.method !== "POST") {
    const { loadBrain } = await import("./parseVerse");
    return c.json({ ok: true, model: "local-fact-layer", brain_loaded: !!loadBrain().length, brain_size: loadBrain().length });
  }
  let body: any = {};
  try { body = await c.req.json(); } catch { return c.json({ ok: false, error: "invalid json" }, 400); }
  const query = String(body.query || body.q || "").trim();
  if (!query) return c.json({ ok: false, error: "empty query" }, 400);
  const history: MemoryEntry[] = Array.isArray(body.history) ? body.history.slice(-10) : [];
  const smallTalk = lookupSmallTalk(query);
  const scripture = parseVerse(query);
  const primaries = loadPrimaries(query);
  const events = /(current|latest|news|status|today|breaking|outage)/i.test(query) ? loadCurrentEvents() : null;
  const nodes = retrieveBrain(query);
  const verdict = smallTalk ? "REASON" : decideVerdict(query, !!scripture, primaries, events, nodes);
  const reply = answerFromContext(query, scripture ? `${scripture.ref} — ${scripture.text}` : null, primaries, events, nodes, smallTalk);
  return c.json({
    reply, verdict, model: "local-fact-layer",
    scripture_ref: scripture?.ref || null,
    current_events: events ? { count: events.count || 0, pulled_at: events.pulled_at || null, items: (events.items || []).slice(0, 4) } : null,
    nodes_used: nodes.slice(0, 4).map((n) => ({ k: n.k, w: n.w || 0.7 })),
    primaries_used: primaries.slice(0, 4),
    history_tail: history.slice(-3),
  });
};
