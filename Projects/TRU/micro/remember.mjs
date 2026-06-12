// TRU MICRO: Remember — User teaching via "remember:" command
// Bypasses tribunal. Stores directly to brain.
// Input format: "remember: key = value" or bare "some fact to remember"

import { WT } from '../shared/constants.mjs';
import { normalizeKey } from './utils.mjs';

const STOPWORDS = new Set(['the','a','an','is','are','to','of']);

export function storeNode(content, BRAIN) {
  let k, v;

  const eqIdx = content.indexOf('=');
  if (eqIdx > 0) {
    k = content.slice(0, eqIdx).trim().toLowerCase().replace(/[^a-z0-9_]/g, '_').slice(0, 50);
    v = content.slice(eqIdx + 1).trim();
  } else {
    // No = sign: generate key from first 4 non-stopwords
    k = normalizeKey(content);
    v = content.trim();
  }

  if (!k || !v) return { success: false, reason: 'empty key or value' };

  const exists = BRAIN.find(n => n.k === k);

  const node = {
    k,
    v,
    t: 'fact',
    w: WT.BASE * WT.SOURCE_USER,
    source: 'USER',
    refined_by: [],
    storm_count: 0,
    refine_count: 0,
    accesses: 0,
    last_used: new Date().toISOString(),
    created_by: 'user_remember'
  };

  BRAIN.push(node);

  return {
    success: true,
    key: k,
    node,
    totalNodes: BRAIN.length,
    wasNew: !exists
  };
}
