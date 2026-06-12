// TRU Shared Constants — imported by both macro and micro scripts
// Single source of truth for all thresholds, weights, and defaults

export const WT = {
  FAST_THRESHOLD:  0.85,   // ≥0.85 → RECALL (skip tribunal)
  CHAOS_THRESHOLD: 0.45,   // <0.45 → GAP (knowledge gap)
  INTEGRATED:      0.75,   // 0.75–0.84 → INTEGRATED
  REASON:          0.45,   // 0.45–0.74 → REASON (show chain of thought)
  TRUTH:           0.90,   // ≥0.90 → TRUTH (direct, confident)

  // Node weight components
  BASE:            0.75,   // default starting weight
  STORM_BOOST:      0.03,   // Neural Storm certification bonus
  RECENCY_HALFLIFE: 30,     // days until weight decays by half
  MAX_WEIGHT:      0.97,   // never exceed this
  MIN_WEIGHT:      0.55,   // never below this

  // Weight decay
  DECAY_ENABLED:   true,

  // Source multipliers
  SOURCE_CERTIFIED: 1.00,
  SOURCE_STORMED:   0.98,
  SOURCE_USER:      0.95,
  SOURCE_ARCHIVIST: 0.90,

  // Verdict multipliers for storm scoring
  VERDICT_TRUTH:      1.00,
  VERDICT_INTEGRATED: 0.92,
  VERDICT_REASON:     0.85,
  VERDICT_GAP:        0.70,

  // Specificity bonuses for storm scoring
  SPEC_NUMBERS:   0.05,  // has numbers/units
  SPEC_NOUNS:     0.03,  // has proper nouns
  SPEC_DEFINITION:0.02,  // is a definition (contains "is/are")
};

export const MAX_NODES = 5;    // top-K for attention retrieval
export const MAX_INPUT = 500;  // max query length
export const BRAIN_KEY = 'tru_phase6_brain';

export const VERDICT_LABELS = {
  TRUTH:      'TRUTH',
  INTEGRATED: 'TRUST',
  REASON:     'REASON',
  GAP:        'GAP',
  FAST:       'FAST',
  RECALL:     'RECALL'
};
