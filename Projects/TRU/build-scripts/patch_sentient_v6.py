#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

PATCH = r'''
<script>
const TRU_SENTIENT_V6 = "sentient-continuity-v6";
function truV6Result(reply, verdict = "REASON", source = "local integration layer • offline", extra = {}) {
  return Object.assign({ reply, verdict, source, nodes_used: [], follow_up: false }, extra);
}
function truV6Direct(original, result) {
  truBegin(original);
  truEnd(original, result);
  addTurn(original, result);
  return result;
}
function truV6Normalise(q) {
  return String(q).toLowerCase().replace(/[“”"']/g, "").replace(/[!?]+$/g, "").replace(/\s+/g, " ").trim();
}
function truV6SacredMap() {
  const base = typeof truV5SacredIntegration === "function" ? truV5SacredIntegration() : truV6Result("sacred integration requires the local concept-map layer.", "GAP", "local concept-map boundary • offline", { confidence: "low" });
  return base;
}
function truV6SacredCombined() {
  const base = truV6SacredMap();
  const boundary = typeof ARCHITECTURE_ANSWERS !== "undefined" && ARCHITECTURE_ANSWERS.integration ? ARCHITECTURE_ANSWERS.integration.reply : "the offline boundary is local: no webhook, HTTP call, cloud database, or live-LLM fallback is active in this artifact.";
  return truV6Result(`${base.reply}\n\nOFFLINE BOUNDARY\n${boundary}\n\nroute result: sacred integration is the primary concept; the offline boundary is a separate implementation constraint.`, "REASON", "local PaRDeS concept map + offline boundary • local", { confidence: "supported", grounded_nodes: base.grounded_nodes || [] });
}
function truV6SacredGaps() {
  const base = truV6SacredMap();
  return truV6Result(`${base.reply}\n\nRANKED GAP REPAIR\n1. add node sacred_integration with fields k, v, t, source, and provenance.\n2. add typed links sacred_integration → scripture, doctrine, memory, reasoning, and output.\n3. add a response field distinguishing retrieved text from interpretation.\n4. add regression prompts for concept-only, combined concept-plus-boundary, and contradiction-audit wording.\n5. add a browser persistence test covering localStorage and exported JSON.`, "REASON", "local PaRDeS gap audit • offline", { confidence: "supported", grounded_nodes: base.grounded_nodes || [] });
}
function truV6MedicalDefinition() {
  return truV6Result("encephalomalacia is softening or loss of brain tissue after damage such as trauma, infarction, haemorrhage, infection, or reduced oxygen supply. the clinical meaning depends on the location, extent, cause, timing, symptoms, and imaging. this is a general definition, not an interpretation of an individual scan or a diagnosis.", "DEFINE", "curated local medical definition • offline", { confidence: "supported" });
}
function truV6Recall(q) {
  const match = String(q).match(/^recall\s*:?[ \t]*(.+)$/i);
  if (!match) return null;
  const key = match[1].trim();
  return typeof cmdRecall === "function" ? Object.assign(cmdRecall(key), { source: "local memory overlay • offline", confidence: "high" }) : truV6Result("recall requires the local memory layer.", "GAP", "local memory boundary • offline", { confidence: "low" });
}
function truV6PlanningGap() {
  return truV6Result("i do not know your schedule, priorities, location, or available time from the local sources. name the goal and constraints, or teach me a preference. i will not substitute an unrelated brain node for a plan.", "GAP", "local planning boundary • offline", { confidence: "low" });
}
function truV6Intercept(q) {
  const original = String(q);
  const low = truV6Normalise(original);
  if (/^after reviewing all ten answers|^final integration verdict|^produce a final integration verdict/.test(low)) return typeof truV5FinalVerdict === "function" ? truV5FinalVerdict() : truV6Result("the final integration route is unavailable.", "GAP", "local integration audit • offline", { confidence: "low" });
  if (/contradiction audit|audit the ten|wrong routes|false confidence|missing safety|session audit/.test(low)) return typeof truV5Audit === "function" ? truV5Audit() : truV6Result("the session audit route is unavailable.", "GAP", "local session audit • offline", { confidence: "low" });
  if (/^who are you$|^what are you$|^what is tru$/.test(low) || (/\bwho are you\b/.test(low) && /\b(exact|grounded|source|entry|confidence|self)\b/.test(low))) return typeof truV5Self === "function" ? truV5Self() : truV6Result("the grounded self map is unavailable.", "GAP", "local identity boundary • offline", { confidence: "low" });
  if (/what survives.*reload|what survives.*export|temporary conversation history|actual storage mechanisms|storage mechanisms/.test(low)) return typeof truV5Memory === "function" ? truV5Memory() : truV6Result("the persistence map is unavailable.", "GAP", "local persistence boundary • offline", { confidence: "low" });
  if (/what important concepts.*sacred integration|absent.*sacred integration|weakly connected.*sacred integration|gaps?.*sacred integration/.test(low)) return truV6SacredGaps();
  if (/sacred integration/.test(low) && /offline boundary|webhook|http|cloud|api/.test(low)) return truV6SacredCombined();
  if (/sacred integration/.test(low)) return truV6SacredMap();
  if (/awake brain mapping|awake craniotomy|craniotomy.*brain mapping|brain mapping.*craniotomy/.test(low)) return typeof truV5Craniotomy === "function" ? truV5Craniotomy() : truV6Result("awake brain mapping requires the local medical-safety route.", "GAP", "local medical safety boundary • offline", { confidence: "low" });
  if (/\bencephalomalacia\b/.test(low)) return truV6MedicalDefinition();
  const recall = truV6Recall(original);
  if (recall) return recall;
  if (/^(what should we do today|what do you want to do today|what to do today|what do you want to do)$/.test(low)) return truV6PlanningGap();
  const calculation = typeof truV5Calculation === "function" ? truV5Calculation(original) : null;
  if (calculation) return calculation;
  const deeper = low.match(/^go\s+deeper(?:\s+on)?(?:\s+(.+))?$/);
  if (deeper) return typeof truV5Deeper === "function" ? truV5Deeper(deeper[1] || "") : truV6Result("name the exact subject for a bounded expansion.", "GAP", "local depth boundary • offline", { confidence: "low" });
  return null;
}
const truV6BaseRoute = route;
route = function(q) {
  const original = String(q);
  const intercepted = truV6Intercept(original);
  if (intercepted) return truV6Direct(original, intercepted);
  return truV6BaseRoute(original);
};
const truV6ConfidenceBase = confidenceFor;
confidenceFor = function(result) {
  if (result && result.confidence) return result.confidence;
  return truV6ConfidenceBase(result);
};
setTimeout(() => {
  const actual = typeof getBrain === "function" ? getBrain().length : null;
  const sub = document.getElementById("sub");
  if (sub && actual) sub.textContent = actual.toLocaleString() + " nodes • " + KJV_COUNT.toLocaleString() + " verses";
  document.querySelectorAll(".ready").forEach(node => { node.innerHTML = node.innerHTML.replace(/183,374 brain nodes/g, actual ? actual.toLocaleString() + " brain nodes" : "brain nodes"); });
}, 800);
</script>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description="create additive TRU_SENTIENT v6")
    parser.add_argument("--source", type=Path, default=Path("TRU_SENTIENT_v5.html"))
    parser.add_argument("--output", type=Path, default=Path("TRU_SENTIENT_v6.html"))
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing additive build: {output}")
    html = source.read_text(encoding="utf-8", errors="replace")
    if "sentient-continuity-v6" in html:
        raise RuntimeError("source already contains v6 patch")
    if html.count("</body>") != 1:
        raise RuntimeError("expected one closing body tag")
    output.write_text(html.replace("</body>", PATCH + "\n</body>", 1), encoding="utf-8")
    print(output)
    print(output.stat().st_size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
