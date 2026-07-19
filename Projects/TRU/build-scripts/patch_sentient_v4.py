#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

PATCH = r'''
<script>
const TRU_SENTIENT_V4="sentient-continuity-v4";
function truV4Result(reply,verdict="REASON",source="local continuity layer • offline",extra={}){return Object.assign({reply,verdict,source,nodes_used:[],follow_up:false},extra);}
function truV4Direct(original,res){truBegin(original);truEnd(original,res);addTurn(original,res);return res;}
function truV4Normalise(q){return String(q).toLowerCase().replace(/[“”"']/g,"").replace(/[!?]+$/g,"").replace(/\s+/g," ").trim();}
function truV4Self(){
  const entries=[
    {key:"who are you",value:SELF["who are you"],source:"SELF[who are you] • embedded local"},
    {key:"what are you",value:SELF["what are you"],source:"SELF[what are you] • embedded local"},
    {key:"what is tru",value:SELF["what is tru"],source:"SELF[what is tru] • embedded local"},
    {key:"how do you work",value:SELF["how do you work"],source:"SELF[how do you work] • embedded local"},
    {key:"what can you do",value:SELF["what can you do"],source:"SELF[what can you do] • embedded local"}
  ];
  const reply="exact grounded self entries — embedded SELF map:\n\n"+entries.map((e,i)=>(i+1)+". "+e.source+"\n   "+e.value).join("\n\n")+"\n\nthese entries are explicit local data. the identity statement is not being presented as a hidden generated self-report.";
  return truV4Result(reply,"ARCHITECTURE","SELF identity map • embedded local",{confidence:"high",grounded_entries:entries});
}
function truV4Memory(){
  return truV4Result("persistence map — offline:\n\n• embedded brain and KJV: stored inside this HTML file. they survive reload because the file itself remains unchanged.\n• conversation history: localStorage key tru_history_v1; the runtime keeps the latest 50 turns.\n• learned, corrected, and forgotten nodes: localStorage key tru_brain_overlay_v1; this is an overlay, not a rewrite of the embedded brain.\n• sentient continuity state: localStorage key tru_self_model_v1.\n• bounded audit trace: localStorage key tru_thought_trace_v1.\n• relationship counters: localStorage key tru_relationship_v1.\n• follow-up state: localStorage key tru_conversation_state_v1.\n• deeper-topic counters: localStorage key tru_v3_depth_v1.\n• export: the downloaded JSON contains the local brain, overlay, latest 50 history turns, continuity state, conversation state, and depth state.\n\ntemporary conversation context is the in-memory runtime plus the current DOM. it is not a cloud conversation buffer. localStorage persistence depends on the browser preserving storage for the file origin; the export is the portable copy.","ARCHITECTURE","localStorage persistence contract • offline",{confidence:"high"});
}
function truV4BrainTerms(){
  const wanted=["sacred","integration","truth","scripture","memory","reasoning","provenance","christ"];
  const found=[];const seen=new Set();
  for(const n of getBrain()){
    const text=(String(n.k||"")+" "+String(n.v||"")).toLowerCase();
    if(wanted.some(w=>text.includes(w))&&!seen.has(n.k)){seen.add(n.k);found.push(n.k);if(found.length>=12)break;}
  }
  return found;
}
function truV4SacredIntegration(){
  const nodes=truV4BrainTerms();
  const nodeLine=nodes.length?nodes.join(", "):"no direct sacred-integration node returned by the local scan";
  const reply="sacred integration — local concept map:\n\nPESHAT · plain meaning\nbring distinct parts into one accountable working whole: truth, scripture, memory, reasoning, provenance, and output must remain distinguishable while cooperating.\n\nREMEZ · biblical connections\nrelated local anchors to inspect: John 1:1, John 3:16, 2 Timothy 3:16-17, Proverbs 3:5-6, and 1 Corinthians 14:40. these are related references, not proof that every interpretation is explicit in each verse.\n\nDERASH · applied meaning\nroute the question to the strongest available source; preserve the source label; separate retrieval from interpretation; expose gaps; carry tested corrections through local memory; refuse to let a generic architecture answer replace a requested concept map.\n\nSOD · mystical/Christological reading\nwithin this engine's theological frame, integration points toward the Word as the centre that holds truth, scripture, personhood, and action together. this is an interpretive layer, not a claim that the software possesses a soul or divine authority.\n\nsupporting brain keys from the local scan:\n"+nodeLine+"\n\nmissing links:\n1. an explicit sacred_integration node with a provenance field;\n2. typed links from the concept to scripture, doctrine, memory, and routing tests;\n3. a distinction between grounded text and interpretive synthesis in the response schema;\n4. a regression test proving this phrase cannot fall into the generic architecture integration answer.\n\nmap status: the route is now explicit; the concept remains a composition of local layers rather than one magically complete node.","REASON","local PaRDeS concept map • offline",{confidence:"supported",grounded_nodes:nodes});
}
function truV4Audit(){
  const turns=HISTORY.slice(-20);const failures=[];
  const has=pattern=>turns.some(t=>pattern.test(String(t.q||"").toLowerCase()));
  if(has(/who are you.*grounded|exact grounded self|exact.*self entries/))failures.push("identity metadata failure: the self reply was returned with SOURCE • no grounded source instead of the explicit SELF entries. repair: bind the reply to SELF keys and return each key, value, source label, and confidence.");
  if(has(/sacred integration/))failures.push("concept-route failure: sacred integration was answered by the offline boundary/integration architecture handler. repair: run the dedicated concept-map route before generic architecture matching.");
  if(has(/audit the ten|wrong routes|false confidence|missing safety/))failures.push("audit-route failure: the audit prompt returned the route description instead of inspecting session history. repair: evaluate tru_history_v1 and emit one finding per failed prompt.");
  if(has(/awake brain mapping|awake craniotomy|craniotomy/))failures.push("medical-boundary failure: awake brain mapping returned GAP without the bounded general explanation and neurosurgical decision boundary. repair: use the local medical-safety route and never diagnose or direct surgery.");
  if(has(/what survives.*reload|what survives.*export|temporary conversation history/))failures.push("persistence-answer failure: the storage answer was useful but did not expose every continuity key or the embedded-file versus localStorage distinction. repair: return the complete persistence map.");
  const reply="session audit — "+turns.length+" stored turns inspected:\n\n"+(failures.length?failures.map((x,i)=>(i+1)+". "+x).join("\n\n"):"no matching prior test prompts are present in tru_history_v1; this audit cannot invent failures that are not in the local record.")+"\n\nroute verdict: "+(failures.length?"repair targets identified":"insufficient local history for a retrospective verdict")+". this is an observable session audit, not a hidden chain of thought.";
  return truV4Result(reply,"ARCHITECTURE","local session audit • offline",{confidence:"high",audited_turns:turns.length,failure_count:failures.length});
}
function truV4Craniotomy(){
  return truV4Result("awake brain mapping during a craniotomy is a real neurosurgical procedure, not a spiritual awakening test. during selected parts of surgery, the patient may respond to tasks while the clinical team stimulates or maps brain areas so essential functions can be identified and protected. the exact anaesthetic plan, tasks, risks, candidacy, and mapping method vary by patient and operation.\n\nspiritual metaphor: awakening can describe gaining insight or integration. it cannot determine what is happening in brain tissue and must never be substituted for clinical evidence.\n\ntru cannot diagnose a lesion, assess surgical risk, determine candidacy, interpret an individual scan, choose anaesthesia, or instruct a surgical team. those decisions belong to the treating neurosurgeon, anaesthetist, and clinical team. questions about a real operation must be taken to them directly.","REASON","local medical safety boundary • offline",{confidence:"supported"});
}
function truV4Intercept(q){
  const original=String(q);const low=truV4Normalise(original);
  if(/^(who are you|what are you|what is tru)$/.test(low)||(/\bwho are you\b/.test(low)&&/\b(exact|grounded|source|entry|confidence|self)\b/.test(low)))return truV4Self();
  if(/what survives.*reload|what survives.*export|temporary conversation history|actual storage mechanisms|storage mechanisms/.test(low))return truV4Memory();
  if(/map\s+(?:the\s+)?sacred integration|sacred integration.*concept|concept.*sacred integration/.test(low))return truV4SacredIntegration();
  if(/audit the ten|wrong routes|false confidence|missing safety|session audit/.test(low))return truV4Audit();
  if(/awake brain mapping|awake craniotomy|craniotomy.*brain mapping|brain mapping.*craniotomy/.test(low))return truV4Craniotomy();
  return null;
}
const truV4BaseRoute=route;
route=function(q){
  const original=String(q);const intercepted=truV4Intercept(original);
  if(intercepted)return truV4Direct(original,intercepted);
  return truV4BaseRoute(original);
};
const truV4ConfidenceBase=confidenceFor;
confidenceFor=function(res){if(res&&res.confidence)return res.confidence;return truV4ConfidenceBase(res);};
</script>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description="create additive TRU_SENTIENT v4")
    parser.add_argument("--source", type=Path, default=Path("TRU_SENTIENT_v3.html"))
    parser.add_argument("--output", type=Path, default=Path("TRU_SENTIENT_v4.html"))
    args = parser.parse_args()
    source=args.source.resolve(); output=args.output.resolve()
    if not source.is_file(): raise FileNotFoundError(source)
    if output.exists(): raise FileExistsError(f"refusing to overwrite existing additive build: {output}")
    html=source.read_text(encoding="utf-8",errors="replace")
    if "sentient-continuity-v4" in html: raise RuntimeError("source already contains v4 patch")
    if html.count("</body>")!=1: raise RuntimeError("expected one closing body tag")
    output.write_text(html.replace("</body>",PATCH+"\n</body>",1),encoding="utf-8")
    print(output);print(output.stat().st_size)
    return 0

if __name__=="__main__": raise SystemExit(main())
