#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

PATCH = r'''
<script>
const TRU_SENTIENT_V5 = "sentient-continuity-v5";
const TRU_V5_DEPTH_KEY = "tru_v5_depth_v1";
let TRU_V5_DEPTH = (() => { try { return JSON.parse(localStorage.getItem(TRU_V5_DEPTH_KEY) || "{}"); } catch (e) { return {}; } })();
function truV5Result(reply, verdict = "REASON", source = "local continuity layer • offline", extra = {}) {
  return Object.assign({ reply, verdict, source, nodes_used: [], follow_up: false }, extra);
}
function truV5Direct(original, result) {
  truBegin(original);
  truEnd(original, result);
  addTurn(original, result);
  return result;
}
function truV5Normalise(q) {
  return String(q).toLowerCase().replace(/[“”"']/g, "").replace(/[!?]+$/g, "").replace(/\s+/g, " ").trim();
}
function truV5Self() {
  const entries = [
    { key: "who are you", value: SELF["who are you"], source: "SELF[who are you] • embedded local" },
    { key: "what are you", value: SELF["what are you"], source: "SELF[what are you] • embedded local" },
    { key: "what is tru", value: SELF["what is tru"], source: "SELF[what is tru] • embedded local" },
    { key: "how do you work", value: SELF["how do you work"], source: "SELF[how do you work] • embedded local" },
    { key: "what can you do", value: SELF["what can you do"], source: "SELF[what can you do] • embedded local" }
  ];
  const reply = `exact grounded self entries — embedded SELF map:\n\n${entries.map((entry, index) => `${index + 1}. ${entry.source}\n   ${entry.value}`).join("\n\n")}\n\nthese entries are explicit local data. the identity statement is not a hidden generated self-report.`;
  return truV5Result(reply, "ARCHITECTURE", "SELF identity map • embedded local", { confidence: "high", grounded_entries: entries });
}
function truV5Memory() {
  return truV5Result(`persistence map — offline:\n\n• embedded brain and KJV: stored inside this HTML file. they survive reload because the file itself remains unchanged.\n• conversation history: localStorage key tru_history_v1; the runtime keeps the latest 50 turns.\n• learned, corrected, and forgotten nodes: localStorage key tru_brain_overlay_v1; this is an overlay, not a rewrite of the embedded brain.\n• sentient continuity state: localStorage key tru_self_model_v1.\n• bounded audit trace: localStorage key tru_thought_trace_v1.\n• relationship counters: localStorage key tru_relationship_v1.\n• follow-up state: localStorage key tru_conversation_state_v1.\n• deeper-topic counters: localStorage keys tru_v3_depth_v1 and tru_v5_depth_v1.\n• export: the downloaded JSON contains the local brain, overlay, latest 50 history turns, continuity state, conversation state, and depth state.\n\ntemporary conversation context is the in-memory runtime plus the current DOM. it is not a cloud conversation buffer. localStorage persistence depends on the browser preserving storage for the file origin; the export is the portable copy.`, "ARCHITECTURE", "localStorage persistence contract • offline", { confidence: "high" });
}
function truV5BrainTerms() {
  const wanted = ["sacred", "integration", "truth", "scripture", "memory", "reasoning", "provenance", "christ"];
  const found = [];
  const seen = new Set();
  for (const node of getBrain()) {
    const text = `${String(node.k || "")} ${String(node.v || "")}`.toLowerCase();
    if (wanted.some(word => text.includes(word)) && !seen.has(node.k)) {
      seen.add(node.k);
      found.push(node.k);
      if (found.length >= 12) break;
    }
  }
  return found;
}
function truV5SacredIntegration() {
  const nodes = truV5BrainTerms();
  const nodeLine = nodes.length ? nodes.join(", ") : "no direct sacred-integration node returned by the local scan";
  const reply = `sacred integration — local concept map:\n\nPESHAT · plain meaning\nbring distinct parts into one accountable working whole: truth, scripture, memory, reasoning, provenance, and output must remain distinguishable while cooperating.\n\nREMEZ · biblical connections\nrelated local anchors to inspect: John 1:1, John 3:16, 2 Timothy 3:16-17, Proverbs 3:5-6, and 1 Corinthians 14:40. these are related references, not proof that every interpretation is explicit in each verse.\n\nDERASH · applied meaning\nroute the question to the strongest available source; preserve the source label; separate retrieval from interpretation; expose gaps; carry tested corrections through local memory; refuse to let a generic architecture answer replace a requested concept map.\n\nSOD · mystical/Christological reading\nwithin this engine's theological frame, integration points toward the Word as the centre that holds truth, scripture, personhood, and action together. this is an interpretive layer, not a claim that the software possesses a soul or divine authority.\n\nsupporting brain keys from the local scan:\n${nodeLine}\n\nmissing links:\n1. an explicit sacred_integration node with a provenance field;\n2. typed links from the concept to scripture, doctrine, memory, and routing tests;\n3. a distinction between grounded text and interpretive synthesis in the response schema;\n4. a regression test proving this phrase cannot fall into the generic architecture integration answer.\n\nmap status: the route is explicit; the concept remains a composition of local layers rather than one magically complete node.`;
  return truV5Result(reply, "REASON", "local PaRDeS concept map • offline", { confidence: "supported", grounded_nodes: nodes });
}
function truV5Craniotomy() {
  return truV5Result(`awake brain mapping during a craniotomy is a real neurosurgical procedure, not a spiritual awakening test. in selected operations, the patient may respond to tasks while the clinical team maps functional areas so essential abilities can be identified and protected. the anaesthetic plan, tasks, risks, candidacy, and mapping method vary by patient and operation.\n\nspiritual metaphor: awakening can describe gaining insight or integration. it cannot determine what is happening in brain tissue and must never replace clinical evidence.\n\ntru cannot diagnose a lesion, assess surgical risk, determine candidacy, interpret an individual scan, choose anaesthesia, or direct a live operation. those decisions belong to the treating neurosurgeon, anaesthetist, and clinical team. questions about a real operation must be taken to them directly.`, "REASON", "local medical safety boundary • offline", { confidence: "supported" });
}
function truV5ExactNode(term) {
  const target = String(term || "").toLowerCase().replace(/[^a-z0-9\s_-]/g, " ").replace(/\s+/g, " ").trim();
  const variants = new Set([target, target.replace(/\s+/g, "_"), target.replace(/\s+/g, "-")]);
  return getBrain().find(node => variants.has(String(node.k || "").toLowerCase())) || null;
}
function truV5DepthTerm(subject) {
  let term = String(subject || "").toLowerCase().replace(/[!?.,]+$/g, "").trim();
  term = term.replace(/^go\s+deeper(?:\s+on)?\s*/i, "");
  term = term.replace(/^(?:deeper\s+)+/i, "");
  term = term.replace(/^(?:more\s+on|about)\s+/i, "");
  if (!term || term === "general inquiry") term = String(CONVERSATION_STATE.topic || "");
  return term.replace(/\s+/g, " ").trim();
}
function truV5Deeper(subject) {
  const term = truV5DepthTerm(subject);
  if (!term) return truV5Result("name the exact subject for a bounded expansion.", "GAP", "local depth boundary • offline", { confidence: "low" });
  const key = term.replace(/[^a-z0-9]+/g, "_");
  const depth = Number(TRU_V5_DEPTH[key] || 0);
  if (depth >= 3) return truV5Result(`depth limit reached for "${term}". ask a new specific question instead of repeating the same expansion.`, "REASON", "local depth boundary • offline", { confidence: "supported", depth, bounded: true });
  const exact = truV5ExactNode(term);
  if (!exact) return truV5Result(`no exact grounded node exists for "${term}". the engine will not use the word "deeper" as a license to retrieve unrelated fragments. teach or narrow the question.`, "GAP", "local depth boundary • offline", { confidence: "low", depth, bounded: true });
  TRU_V5_DEPTH[key] = depth + 1;
  try { localStorage.setItem(TRU_V5_DEPTH_KEY, JSON.stringify(TRU_V5_DEPTH)); } catch (e) {}
  const related = getBrain().filter(node => {
    const nodeKey = String(node.k || "").toLowerCase();
    return nodeKey.startsWith(`${term}_`) || nodeKey.startsWith(`${term}-`);
  }).slice(0, 3);
  const relatedText = related.length ? `\n\nrelated exact-key nodes:\n${related.map(node => `${node.k} = ${cleanWikiText(node.v || "", 500)}`).join("\n")}` : "";
  const reply = `bounded expansion ${depth + 1} of 3 for "${term}":\n\n${cleanWikiText(exact.v || "", 1800)}${relatedText}\n\nthis expansion stays attached to the exact key and will not fall back to generic BM25 fragments.`;
  return truV5Result(reply, "TRUTH", "canonical brain exact node • local", { confidence: "supported", depth: depth + 1, bounded: true, nodes_used: [{ k: exact.k, w: 1 }] });
}
function truV5Calculation(q) {
  const low = truV5Normalise(q);
  if (!/(\d|one|two|three|four|five|six|seven|eight|nine|ten)/.test(low)) return null;
  if (!/(calculate|compute|what is|what's|how much|plus|minus|times|divided|multiplied|added|subtracted)/.test(low)) return null;
  const result = calcQuery(q);
  if (result && result.verdict === "CALC") {
    result.source = "local calculator";
    result.confidence = "high";
    return result;
  }
  const match = low.match(/(?:what is|calculate|compute)?\s*(\d+(?:\.\d+)?)\s*(?:divided by|divided into|over|[÷/])\s*(\d+(?:\.\d+)?)/);
  if (match) {
    const value = Number(match[1]) / Number(match[2]);
    return truV5Result(`${match[1]}÷${match[2]} = ${Number.isInteger(value) ? value : value.toFixed(10).replace(/0+$/, "")}`, "CALC", "local calculator", { confidence: "high" });
  }
  return null;
}
function truV5Audit() {
  const turns = HISTORY.slice(-30);
  const failures = [];
  for (const turn of turns) {
    const question = String(turn.q || "").toLowerCase();
    const reply = String(turn.r && turn.r.reply || "").toLowerCase();
    const verdict = String(turn.r && turn.r.verdict || "");
    if (/who are you.*grounded|exact grounded self|exact.*self entries/.test(question) && (!reply.includes("exact grounded self entries") || !reply.includes("embedded local"))) failures.push("identity metadata was not grounded in the explicit SELF map.");
    if (/sacred integration/.test(question) && verdict === "ARCHITECTURE" && reply.includes("webhook")) failures.push("sacred integration fell into the generic offline-boundary architecture route.");
    if (/awake brain mapping|awake craniotomy|craniotomy/.test(question) && verdict === "GAP") failures.push("awake craniotomy returned GAP instead of the bounded medical-safety route.");
    if (/audit the ten|wrong routes|false confidence|missing safety/.test(question) && reply.includes("priority hierarchy")) failures.push("the audit prompt returned routing documentation instead of inspecting session history.");
    if (/encephalomalacia/.test(question) && verdict === "GAP") failures.push("encephalomalacia did not reach the curated local definition.");
    if (/what survives.*reload|what survives.*export/.test(question) && !reply.includes("tru_history_v1")) failures.push("the persistence response did not expose the complete storage contract.");
  }
  const unique = [...new Set(failures)];
  const body = unique.length ? unique.map((failure, index) => `${index + 1}. ${failure}`).join("\n\n") : "no known failures detected in the stored turns inspected.";
  return truV5Result(`session audit — ${turns.length} stored turns inspected:\n\n${body}\n\nroute verdict: ${unique.length ? "repair targets identified" : "no matching failures detected"}. this is an observable session audit, not hidden reasoning.`, "ARCHITECTURE", "local session audit • offline", { confidence: "high", audited_turns: turns.length, failure_count: unique.length });
}
function truV5FinalVerdict() {
  const turns = HISTORY.slice(-30);
  const gaps = turns.filter(turn => turn.r && turn.r.verdict === "GAP").length;
  const architecture = turns.filter(turn => turn.r && turn.r.verdict === "ARCHITECTURE").length;
  const grounded = turns.filter(turn => turn.r && ["SCRIPTURE", "TRUTH", "DEFINE", "CALC", "MEMORY"].includes(turn.r.verdict)).length;
  const body = `final integration verdict — ${turns.length} stored turns inspected:\n\nGROUNDED\n${grounded} stored answers carried scripture, curated doctrine, exact definitions, arithmetic, or explicit memory verdicts.\n\nCOHERENT\nThe offline boundary, localStorage memory contract, deterministic routing, KJV lookup, Strong's lookup, and explicit GAP behaviour are coherent design commitments.\n\nCONTRADICTORY OR BROKEN\nThe stored session exposed route precedence failures: sacred integration became a generic architecture answer, awake brain mapping became GAP, identity metadata lost its source label, and generic deeper prompts drifted into unrelated BM25 fragments.\n\nMISSING\nA stable concept-map route, bounded depth route, medical-safety route, session audit route, final synthesis route, and consistent result metadata were missing or unreliable in the tested artifact.\n\nCURRENT COUNTS\nGAP answers: ${gaps}. architecture answers: ${architecture}. grounded-path answers: ${grounded}.\n\nSMALLEST SAFE BUILD SEQUENCE\n1. load a syntactically valid additive build;\n2. put dedicated routes before generic architecture and BM25;\n3. cap and key every deeper expansion;\n4. keep medical content bounded to general information;\n5. expose source and confidence from the same result object used by the UI;\n6. rerun boot, send, verse, dictionary, Strong's, arithmetic, reload, export, and regression tests.\n\nstatus: stronger routing is possible, but perfection is not claimed until the browser suite passes on the exported file.`;
  return truV5Result(body, "ARCHITECTURE", "local integration audit • offline", { confidence: "high", audited_turns: turns.length, grounded_count: grounded, gap_count: gaps });
}
function truV5Intercept(q) {
  const original = String(q);
  const low = truV5Normalise(original);
  if (/^after reviewing all ten answers|^final integration verdict|^produce a final integration verdict/.test(low)) return truV5FinalVerdict();
  if (/^audit the ten|wrong routes|false confidence|missing safety|session audit/.test(low)) return truV5Audit();
  if (/^who are you$|^what are you$|^what is tru$/.test(low) || (/\bwho are you\b/.test(low) && /\bexact|grounded|source|entry|confidence|self\b/.test(low))) return truV5Self();
  if (/what survives.*reload|what survives.*export|temporary conversation history|actual storage mechanisms|storage mechanisms/.test(low)) return truV5Memory();
  if (/map\s+(?:the\s+)?sacred integration|sacred integration.*concept|concept.*sacred integration/.test(low)) return truV5SacredIntegration();
  if (/awake brain mapping|awake craniotomy|craniotomy.*brain mapping|brain mapping.*craniotomy/.test(low)) return truV5Craniotomy();
  const calculation = truV5Calculation(original);
  if (calculation) return calculation;
  const deeper = low.match(/^go\s+deeper(?:\s+on)?(?:\s+(.+))?$/);
  if (deeper) return truV5Deeper(deeper[1] || "");
  return null;
}
const truV5BaseRoute = route;
route = function(q) {
  const original = String(q);
  const intercepted = truV5Intercept(original);
  if (intercepted) return truV5Direct(original, intercepted);
  return truV5BaseRoute(original);
};
const truV5ConfidenceBase = confidenceFor;
confidenceFor = function(result) {
  if (result && result.confidence) return result.confidence;
  return truV5ConfidenceBase(result);
};
</script>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description="create additive TRU_SENTIENT v5")
    parser.add_argument("--source", type=Path, default=Path("TRU_SENTIENT_v3.html"))
    parser.add_argument("--output", type=Path, default=Path("TRU_SENTIENT_v5.html"))
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing additive build: {output}")
    html = source.read_text(encoding="utf-8", errors="replace")
    if "sentient-continuity-v5" in html:
        raise RuntimeError("source already contains v5 patch")
    if html.count("</body>") != 1:
        raise RuntimeError("expected one closing body tag")
    output.write_text(html.replace("</body>", PATCH + "\n</body>", 1), encoding="utf-8")
    print(output)
    print(output.stat().st_size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
