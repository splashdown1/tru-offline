// TRU MICRO: Utility functions shared across all micro-scripts

import { WT } from '../shared/constants.mjs';

// ── Levenshtein distance ────────────────────────────────────
export function levenshtein(a, b) {
  if (!a || !b) return a === b ? 0 : 1;
  const m = a.length, n = b.length;
  const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++)
    for (let j = 1; j <= n; j++)
      dp[i][j] = a[i-1] === b[j-1] ? dp[i-1][j-1] : 1 + Math.min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]);
  return dp[m][n];
}

// ── Normalize key ───────────────────────────────────────────
const STOPWORDS = new Set(['the','a','an','is','are','to','of','in','on','at','for','and','or','not','be']);
export function normalizeKey(sentence) {
  const words = sentence
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 1 && !STOPWORDS.has(w))
    .slice(0, 4);
  const slug = words.join('_').slice(0, 50) || ('storm_' + sentence.slice(0, 3).toLowerCase());
  return slug;
}

// ── Score-based verdict label ───────────────────────────────
export function verdictLabel(score) {
  if (score >= WT.TRUTH)    return 'TRUTH';
  if (score >= WT.FAST_THRESHOLD) return 'FAST';
  if (score >= WT.INTEGRATED) return 'INTEGRATED';
  if (score >= WT.REASON)   return 'REASON';
  return 'GAP';
}

// ── Format answer (apply voice + minimal rules) ─────────────
export function formatAnswer(text, score) {
  if (!text) return null;
  // Rule: keep it minimal
  const sentences = text.match(/[^.!?]+[.!?]+/g) || [text];
  const trimmed = sentences.slice(0, 2).join(' ').trim();
  // Rule: apply voice (caller handles speaking)
  return trimmed.length > 400 ? trimmed.slice(0, 397) + '...' : trimmed;
}

// ── Weight decay ───────────────────────────────────────────
export function applyDecay(node) {
  if (!WT.DECAY_ENABLED || !node.last_used) return node;
  const days = (Date.now() - new Date(node.last_used).getTime()) / 86400000;
  const factor = Math.pow(0.5, days / WT.RECENCY_HALFLIFE);
  return { ...node, w: Math.max(WT.MIN_WEIGHT, node.w * factor) };
}

// ── Priority label (heaviest = DOG LOGIC) ──────────────────
export function weightLabel(w) {
  if (w >= 0.90) return 'HEAVY';   // DOG LOGIC: heaviest, fetched first
  if (w >= 0.80) return 'MEDIUM';
  if (w >= 0.60) return 'LIGHT';
  return 'FRAGILE';
}

// ── Self-referential query detection ───────────────────────
const SELF_KEYWORDS = ['you','your','tr u','who are you','what are you','are you','do you'];
export function isSelfReferential(query) {
  const ql = query.toLowerCase();
  return SELF_KEYWORDS.some(k => ql.includes(k));
}

// ── Clone brain (safe mutation) ─────────────────────────────
export function cloneBrain(brain) {
  return brain.map(n => ({ ...n }));
}
