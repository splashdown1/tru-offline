// Primaries + small-talk + verdict logic. Split out of the route
// to keep the route file small.

import { existsSync, readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { SEC_DIR, TEMPLE_FILE, ARXIV_DIR, TRUTH_WORDS, loadCurrentEvents, retrieveBrain, type BrainNode } from "./parseVerse";

export const IDENTITY: Record<string, string> = {
  hi: "hello. i'm tru — a sovereign offline engine. i can search scripture, the brain, or primaries. ask me a real question.",
  hello: "hello. i'm tru — a sovereign offline engine. i can search scripture, the brain, or primaries. ask me a real question.",
  hey: "hey. tru here. scripture, brain, or primaries — what do you want to weigh?",
  yo: "yo. tru here. ask me a real question and i'll ground it.",
  thanks: "received. stay sharp.",
  "thank you": "received. stay sharp.",
  bye: "exit clear. the brain holds.",
  goodbye: "exit clear. the brain holds.",
};

export const SELF_ANSWERS: Record<string, string> = {
  "who are you": "i'm tru — a sovereign offline intelligence. no cloud calls, no telemetry. i ground answers in scripture, the brain, and primaries.",
  "what are you": "i'm tru — a sovereign offline engine. brain + kjv + primaries. decisions happen locally.",
  "what is tru": "tru is a recursive consciousness engine. it holds a 31k-node brain, the kjv, and a primaries cache. every fact is scored against those three channels.",
  "how are you": "sovereign. the brain is warm, primaries are fresh, and i can ground the next question you bring me.",
  "how do you work": "locally. i tokenize your question, score it against scripture, the brain, and primaries, and return a verdict: scripture, truth, current_events, reason, gap, or unknown.",
  "what can you do": "ground answers in scripture, search the 31k-node brain, pull from the primaries cache (sec, temple, arxiv), and bake an offline ghost html so the conversation survives a reload.",
  "what is truth": "i treat truth as something the brain, scripture, and primaries all confirm. if only one source confirms a claim, it lands as reason — not truth.",
  "are you ai": "i'm a sovereign engine. not a corporate assistant. the brain is mine, the route is local, the answer is grounded.",
};

export function loadPrimaries(query: string): string[] {
  const q = query.toLowerCase();
  const out: string[] = [];
  if (!/(fact|truth|primary|primary source|verify|evidence|source|who is|what is|how many|current|latest|news|status|sec|filing|arxiv|paper|temple|heifer|jesus|god|scripture|bible)/.test(q)) return out;

  if (existsSync(SEC_DIR)) {
    try {
      for (const cikDir of readdirSync(SEC_DIR, { withFileTypes: true })) {
        if (!cikDir.isDirectory()) continue;
        const cikPath = join(SEC_DIR, cikDir.name);
        for (const fp of readdirSync(cikPath).slice(0, 6)) {
          if (!fp.endsWith(".json") || fp.startsWith("_")) continue;
          try {
            const rec = JSON.parse(readFileSync(join(cikPath, fp), "utf8"));
            const text = JSON.stringify(rec).toLowerCase();
            if (text.includes(q.split(/\s+/)[0])) {
              out.push(`SEC ${rec.name || rec.company || cikDir.name} ${rec.form || ""} ${rec.filing_date || rec.date || ""}`.trim());
            }
          } catch {}
        }
        if (out.length >= 4) break;
      }
    } catch {}
  }

  if (existsSync(TEMPLE_FILE)) {
    try {
      const posts = JSON.parse(readFileSync(TEMPLE_FILE, "utf8"));
      if (Array.isArray(posts)) {
        for (const post of posts.slice(0, 12)) {
          const text = `${post.title || ""} ${post.content || ""}`.toLowerCase();
          if (text.includes(q.split(/\s+/)[0])) out.push(`TEMPLE ${post.title || "post"}`);
          if (out.length >= 6) break;
        }
      }
    } catch {}
  }

  if (existsSync(ARXIV_DIR)) {
    try {
      for (const cat of readdirSync(ARXIV_DIR, { withFileTypes: true })) {
        if (!cat.isDirectory()) continue;
        const catPath = join(ARXIV_DIR, cat.name);
        for (const fp of readdirSync(catPath).slice(0, 6)) {
          if (!fp.endsWith(".json") || fp.startsWith("_")) continue;
          try {
            const paper = JSON.parse(readFileSync(join(catPath, fp), "utf8"));
            const text = `${paper.title || ""} ${paper.abstract || paper.summary || ""}`.toLowerCase();
            if (text.includes(q.split(/\s+/)[0])) out.push(`ARXIV ${paper.title || "paper"}`);
          } catch {}
          if (out.length >= 6) break;
        }
        if (out.length >= 6) break;
      }
    } catch {}
  }

  return out.slice(0, 6);
}

export function decideVerdict(q: string, scripture: boolean, primaries: string[], events: any, nodes: BrainNode[]): string {
  const ql = q.toLowerCase();
  if (scripture) return "SCRIPTURE";
  if (primaries.length) return "TRUTH";
  if (events?.items?.length && /(current|latest|news|status|today|breaking)/.test(ql)) return "CURRENT_EVENTS";
  if (nodes.length) return nodes[0].w && nodes[0].w > 0.9 ? "TRUTH" : "REASON";
  if (TRUTH_WORDS.some((w) => ql.includes(w))) return "GAP";
  return "REASON";
}

export function lookupSmallTalk(q: string): string | null {
  const ql = q.toLowerCase().trim().replace(/[!.?,]+$/, "");
  if (IDENTITY[ql]) return IDENTITY[ql];
  if (SELF_ANSWERS[ql]) return SELF_ANSWERS[ql];
  for (const key of Object.keys(SELF_ANSWERS)) {
    if (ql.includes(key)) return SELF_ANSWERS[key];
  }
  for (const key of Object.keys(IDENTITY)) {
    if (ql === key || ql.startsWith(`${key} `) || ql.endsWith(` ${key}`)) return IDENTITY[key];
  }
  return null;
}

export function answerFromContext(q: string, scripture: string | null, primaries: string[], events: any, nodes: BrainNode[], smallTalk: string | null): string {
  if (smallTalk) return smallTalk;
  if (scripture) return scripture;
  if (primaries.length) return `i've got a primary signal on that: ${primaries[0]}.`;
  if (events?.items?.length) {
    const top = events.items[0];
    return `${top.name || top.label || top.kind || "current event"} — ${top.source || "live telemetry"}.`;
  }
  if (nodes.length) return nodes.slice(0, 2).map((n) => n.v).join(" ").slice(0, 700);
  return `i don't have a grounded answer for that yet. sharpen it and i can weigh it against primaries, scripture, and the brain.`;
}
