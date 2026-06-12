// TRU MICRO: Gap Response — No matching nodes (score < 0.45)
// Admit ignorance. Do not guess. Never hallucinate.

import { WT } from '../shared/constants.mjs';

export function gapResponse(query, BRAIN, classification) {
  return {
    text: "I don't have that. Upload a brain file or say `remember: key = value` to teach me.",
    verdict: 'GAP',
    score: classification.retrieved[0]?.score || 0,
    matchType: 'none',
    nodesUsed: classification.retrieved.length,
    type: 'GAP',
    steps: [
      `Archivist → ${classification.retrieved.length} nodes retrieved (all below threshold)`,
      `Logos → scored ${((classification.retrieved[0]?.score || 0) * 100).toFixed(0)}% < ${(WT.CHAOS_THRESHOLD * 100).toFixed(0)}% (GAP)`,
      `Chaos → falsification complete. No strong match. Admitting knowledge gap.`,
      `Synthesist → honest GAP response generated.`
    ]
  };
}
