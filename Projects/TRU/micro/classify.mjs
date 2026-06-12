// TRU MICRO: Classify — Determine routing decision
// EQ2: Attention → decides whether to RECALL, REASON, or GAP

import { WT, MAX_NODES } from '../shared/constants.mjs';
import { levenshtein, isSelfReferential } from './utils.mjs';

// Self-referential node (fallback for "who are you" etc.)
const SELF_NODE = { k: 'who_are_you', v: "I'm TRU. I think, I weigh, I remember. I learn from you. Truth compounds without limit.", t: 'fact', w: 0.98, source: 'CERTIFIED' };

export function classify(query, BRAIN) {
  const ql = query.toLowerCase().trim();

  // Self-referential: bypass normal retrieval, use dedicated node
  if (isSelfReferential(ql)) {
    return {
      route: 'RECALL',
      retrieved: [{ node: SELF_NODE, score: 0.98, attnWeight: 1.0, matchType: 'self' }],
      isSelfRef: true
    };
  }

  // Tokenize query
  const qtoks = ql.split(/\s+/).filter(t => t.length > 1);

  // Attention: score all nodes against query
  const scored = BRAIN.map(node => {
    if (!node.k || !node.v) return null;
    const kl = node.k.toLowerCase();
    const vl = node.v.toLowerCase();
    let s = 0, matchType = 'none';

    // Exact key match
    if (kl === ql) { s = 1.0; matchType = 'exact_key'; }
    // Key contains query
    else if (kl.includes(ql)) { s = 0.80; matchType = 'key_contains'; }
    // Query contains key
    else if (ql.includes(kl)) { s = 0.70; matchType = 'query_contains_key'; }
    // Partial token match on key
    else {
      const ktoks = kl.split(/[_\s]+/);
      let matches = 0;
      for (const qt of qtoks) {
        for (const kt of ktoks) {
          if (kt.startsWith(qt) || qt.startsWith(kt)) matches++;
        }
      }
      s = (matches / Math.max(qtoks.length, 1)) * 0.5;
      matchType = matches > 0 ? 'token' : 'none';
    }
    // Value search (deeper relevance)
    if (s < 0.4) {
      for (const qt of qtoks) {
        if (qt.length < 3) continue;
        if (vl.includes(qt)) { s = Math.max(s, 0.45 * node.w); matchType = 'value_hit'; break; }
      }
    }
    // Weight × base score
    s *= node.w;

    return { node, score: s, matchType, attnWeight: s };
  }).filter(r => r && r.score > 0);

  scored.sort((a, b) => b.score - a.score);
  const top = scored.slice(0, MAX_NODES);
  const best = top[0] || null;

  // Route decision
  if (!best || best.score < WT.CHAOS_THRESHOLD) {
    return { route: 'GAP', retrieved: top, isSelfRef: false };
  }
  if (best.score >= WT.FAST_THRESHOLD) {
    return { route: 'RECALL', retrieved: top, isSelfRef: false };
  }
  return { route: 'REASON', retrieved: top, isSelfRef: false };
}
