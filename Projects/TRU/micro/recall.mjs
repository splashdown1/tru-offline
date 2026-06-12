// TRU MICRO: Recall — Fast path (score ≥ 0.85)
// EQ1: h_t = f(h_{t-1}, x_t) → direct output
// No tribunal loop. Logos outputs immediately.

import { WT } from '../shared/constants.mjs';
import { verdictLabel, formatAnswer } from './utils.mjs';

export function recall(query, BRAIN, classification) {
  const { retrieved, isSelfRef } = classification;
  const best = retrieved[0];

  const score = best ? best.score : 0;
  const text = best ? best.node.v : null;
  const verdict = isSelfRef ? 'TRUTH' : (score >= WT.TRUTH ? 'TRUTH' : 'FAST');

  // Apply rules (Synthesist follows, never quotes rules)
  const formatted = formatAnswer(text, score);

  return {
    text: formatted,
    verdict,
    score,
    matchType: best?.matchType || 'none',
    nodesUsed: retrieved.length,
    type: 'RECALL',
    steps: []
  };
}
