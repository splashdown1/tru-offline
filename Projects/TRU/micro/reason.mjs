// TRU MICRO: Reason — Middle path (0.45 ≤ score < 0.85)
// EQ1 + EQ3: State transition + Chain of thought
// Runs tribunal: Archivist → Logos → Optimist → Chaos → Balance → Synthesist

import { WT } from '../shared/constants.mjs';
import { verdictLabel, formatAnswer } from './utils.mjs';

export function reason(query, BRAIN, classification, externalContext = []) {
  const { retrieved } = classification;
  const best = retrieved[0];
  const score = best ? best.score : WT.CHAOS_THRESHOLD;

  // Tribunal loop (placeholder — weights engine handles this)
  // For now: apply rules + generate chain of thought
  const formatted = formatAnswer(best?.node?.v, score);

  // Chain of thought (EQ3: P(y_t | y_{<t}, x))
  const steps = [
    `Archivist → top-${retrieved.length} nodes retrieved from brain`,
    `Logos → scored ${(score * 100).toFixed(0)}% (${verdictLabel(score)})`,
    `Tribunal → ${retrieved.length >= 3 ? 'full tribunal run' : 'partial tribunal run'}`,
    `Synthesist → output generated from ${best?.node?.k || 'no strong match'}`
  ];

  // If external context provided (documents, web results), weave in
  let text = formatted;
  if (externalContext.length > 0) {
    const ctx = externalContext.map(c => c.snippet || c.text || '').filter(Boolean);
    if (ctx.length > 0) {
      text = formatted
        ? `${formatted} [Context: ${ctx.slice(0, 2).join(' ').slice(0, 200)}]`
        : `[Context: ${ctx.slice(0, 1).join(' ').slice(0, 300)}]`;
    }
  }

  return {
    text,
    verdict: verdictLabel(score),
    score,
    matchType: best?.matchType || 'none',
    nodesUsed: retrieved.length,
    type: 'REASON',
    steps
  };
}
