// TRU MICRO: Binary — Yes/No fast path
// Matches if query starts with: is, are, do, does, can, will, has, have, should, would, could

import { WT } from '../shared/constants.mjs';
import { verdictLabel } from './utils.mjs';

const BINARY_PATTERNS = /^(is|are|do|does|can|will|has|have|should|would|could)\s/i;

export function binary(query, BRAIN, classification) {
  if (!BINARY_PATTERNS.test(query)) return null; // not binary

  const { retrieved } = classification;
  const score = retrieved[0]?.score || 0;
  const answer = score >= WT.CHAOS_THRESHOLD;
  const word = answer ? 'YES' : 'NO';

  const sentences = {
    YES: [
      'The Archivist found relevant nodes.',
      'Likely yes, based on available knowledge.',
      'The tribunal finds evidence supports yes.'
    ],
    NO: [
      'The Archivist found no strong match.',
      'Likely no, based on available knowledge.',
      'The tribunal finds insufficient evidence.'
    ]
  };

  const opts = answer ? sentences.YES : sentences.NO;
  const extra = retrieved[0]?.node?.v
    ? opts[0]
    : opts[1];

  return {
    text: `**${word}.** ${extra}`,
    verdict: verdictLabel(score),
    score,
    type: 'BINARY',
    steps: [
      `Archivist → ${retrieved.length} nodes retrieved`,
      `Logos → scored ${(score * 100).toFixed(0)}%`,
      `Binary decision → ${word} (threshold: ${(WT.CHAOS_THRESHOLD * 100).toFixed(0)}%)`
    ]
  };
}
