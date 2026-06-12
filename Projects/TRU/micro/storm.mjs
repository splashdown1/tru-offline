// TRU MICRO: Neural Storm — Self-learning from chat history
// Phase 3 complete: 4-step pipeline (extract → score → filter → certify)
// Dog logic: only the heaviest, most novel facts get stored

import { WT } from '../shared/constants.mjs';
import { normalizeKey, levenshtein } from './utils.mjs';

// ── Step 1: Extract candidate facts from TRU messages ──────
export function extractCandidates(chatMessages) {
  const EXCLUDE_PATTERNS = /^(Archivist|Logos|Tribunal ◉|◉|eq:|h_|RECALL|GEASON|GAP|TRUTH|TRUST)/;
  const STOP_SENTENCES = /^(Archivist →|Logos →|Tribunal →|Synthesist →|EQ[123]:|COIL:)/;

  return chatMessages
    .filter(m => m.role === 'tru')
    .flatMap(m => {
      const raw = m.text || m.content || '';
      return (raw.match(/[^.!?\n]+[.!?]+/g) || [])
        .map(s => s.trim())
        .filter(s => s.length > 15 && s.length < 250)
        .filter(s => !EXCLUDE_PATTERNS.test(s) && !STOP_SENTENCES.test(s))
        .map(s => ({ text: s, verdict: m.verdict || 'REASON', score: m.score || 0.75 }));
    });
}

// ── Step 2: Score each candidate ─────────────────────────────
export function scoreCandidates(candidates) {
  return candidates.map(c => {
    let w = WT.BASE;

    // Verdict multiplier
    if (c.verdict === 'TRUTH')      w *= WT.VERDICT_TRUTH;
    else if (c.verdict === 'INTEGRATED') w *= WT.VERDICT_INTEGRATED;
    else if (c.verdict === 'REASON') w *= WT.VERDICT_REASON;
    else if (c.verdict === 'GAP')    w *= WT.VERDICT_GAP;

    // Specificity bonuses
    if (/\d+/.test(c.text))              w += WT.SPEC_NUMBERS;    // has numbers
    if (/[A-Z][a-z]{2,}/.test(c.text))  w += WT.SPEC_NOUNS;      // proper nouns
    if (/\b(is|are|are not|was)\b/i.test(c.text)) w += WT.SPEC_DEFINITION; // definition

    return {
      text: c.text,
      rawScore: c.score,
      stormWeight: Math.min(WT.MAX_WEIGHT, Math.max(WT.MIN_WEIGHT, w)),
      verdict: c.verdict
    };
  });
}

// ── Step 3: Filter novel (deduplicate against brain) ─────────
export function filterNovel(scored, BRAIN) {
  return scored.filter(c => {
    const key = normalizeKey(c.text);
    const existing = BRAIN.find(n => n.k === key);
    if (existing) {
      // Upgrade if storm weight is higher
      if (c.stormWeight > existing.w) {
        existing.w = c.stormWeight;
        existing.last_used = new Date().toISOString();
        existing.storm_count = (existing.storm_count || 0) + 1;
      }
      return false; // not novel
    }
    // Check Levenshtein similarity
    for (const n of BRAIN) {
      if (levenshtein(key, n.k) < 3) return false;
      if (levenshtein(c.text, n.v) < 20) return false;
    }
    return true;
  });
}

// ── Step 4: Certify and inject ────────────────────────────────
export function certify(nodes) {
  // Apply storm boost to certified novel nodes
  return nodes.map(n => ({
    ...n,
    stormWeight: Math.min(WT.MAX_WEIGHT, n.stormWeight + WT.STORM_BOOST)
  }));
}

export function injectNodes(certified, BRAIN) {
  const added = [];
  certified.forEach(c => {
    const key = normalizeKey(c.text);
    const node = {
      k: key,
      v: c.text,
      t: 'fact',
      w: c.stormWeight,
      source: 'STORMED',
      refined_by: [],
      storm_count: 1,
      refine_count: 0,
      accesses: 0,
      last_used: new Date().toISOString(),
      created_by: 'neural_storm'
    };
    BRAIN.push(node);
    added.push({ k: key, v: c.text, w: c.stormWeight });
  });
  return added;
}

// ── Full storm pipeline ──────────────────────────────────────
export function runStorm(chatMessages, BRAIN) {
  const extracted = extractCandidates(chatMessages);
  const scored = scoreCandidates(extracted);
  const filtered = filterNovel(scored, BRAIN);
  const certified = certify(filtered);
  return injectNodes(certified, BRAIN);
}
