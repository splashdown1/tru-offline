// TRU MACRO: Orchestrate reasoning session
// High-level flow: Receive → Classify → Route → Respond
// Imports micro-scripts for each step

import { WT, MAX_INPUT } from '../shared/constants.mjs';
import * as micro from '../micro/index.mjs';

// ── Session State ─────────────────────────────────────────
let coilState = 'RESET';
let coilHistory = [];

export function getCoilState() { return coilState; }
export function getCoilHistory() { return coilHistory; }

// ── Main Session Loop ──────────────────────────────────────
// One-shot query processor. Returns { text, verdict, score, steps }
export function runSession(query, BRAIN, externalContext = []) {
  coilState = 'DRAFT';

  // Step 1: Pre-classify — is this recall, reason, or gap?
  const classification = micro.classify(query, BRAIN);

  // Step 2: Route
  let result;
  if (classification.route === 'RECALL') {
    result = micro.recall(query, BRAIN, classification);
  } else if (classification.route === 'REASON') {
    result = micro.reason(query, BRAIN, classification, externalContext);
  } else {
    result = micro.gapResponse(query, BRAIN, classification);
  }

  // Step 3: Record coil state
  coilHistory.push({
    step: coilHistory.length,
    query,
    verdict: result.verdict,
    score: result.score,
    nodesUsed: classification.retrieved.length,
    coilState
  });

  coilState = 'SPEAK';
  return result;
}

// ── Binary Query (yes/no) ──────────────────────────────────
// Fast-path: logosEval only, no full tribunal
export function runBinary(query, BRAIN) {
  const classification = micro.classify(query, BRAIN);
  return micro.binary(query, BRAIN, classification);
}

// ── Remember command (user teaching) ───────────────────────
export function runRemember(content, BRAIN) {
  return micro.storeNode(content, BRAIN);
}

// ── Neural Storm ───────────────────────────────────────────
export function runNeuralStorm(chatMessages, BRAIN) {
  const candidates = micro.extractCandidates(chatMessages);
  const scored = micro.scoreCandidates(candidates);
  const filtered = micro.filterNovel(scored, BRAIN);
  const certified = micro.certify(filtered);
  return micro.injectNodes(certified, BRAIN);
}

// ── Reset session ────────────────────────────────────────────
export function resetSession() {
  coilState = 'RESET';
  coilHistory = [];
}

// ── Load/save brain (macro handles persistence) ─────────────
export function loadBrain() {
  try {
    const raw = localStorage.getItem(WT.BRAIN_KEY || 'tru_phase6_brain');
    return raw ? JSON.parse(raw) : [];
  } catch { return []; }
}

export function saveBrain(BRAIN) {
  try {
    localStorage.setItem(WT.BRAIN_KEY || 'tru_phase6_brain', JSON.stringify(BRAIN));
  } catch {}
}
