// TRU MICRO: Calibration — Adjust thresholds at runtime
// Calibration panel: FAST, CHAOS, RECENCY_HALFLIFE, BASE weight
// Changes take effect immediately (no restart needed)

import { WT } from '../shared/constants.mjs';

// Current active thresholds (can be overridden by adaptive tuning)
export let activeFAST = WT.FAST_THRESHOLD;
export let activeCHAOS = WT.CHAOS_THRESHOLD;

// ── Calibration presets ─────────────────────────────────────
export const PRESETS = {
  PRECISE:  { fast: 0.90, chaos: 0.50, label: 'Precise — only high-confidence answers' },
  BALANCED: { fast: 0.85, chaos: 0.45, label: 'Balanced — TRU default' },
  CREATIVE: { fast: 0.75, chaos: 0.35, label: 'Creative — tries harder on uncertain queries' },
  CONSERVATIVE: { fast: 0.92, chaos: 0.55, label: 'Conservative — admits more gaps' }
};

// ── Apply preset ─────────────────────────────────────────────
export function applyPreset(name) {
  const p = PRESETS[name];
  if (!p) return { error: `Unknown preset: ${name}` };
  activeFAST = p.fast;
  activeCHAOS = p.chaos;
  return { fast: activeFAST, chaos: activeCHAOS, preset: name };
}

// ── Manual calibration ───────────────────────────────────────
export function calibrate(key, value) {
  switch (key) {
    case 'fast':
      activeFAST = Math.max(0.50, Math.min(0.99, parseFloat(value)));
      break;
    case 'chaos':
      activeCHAOS = Math.max(0.20, Math.min(0.70, parseFloat(value)));
      break;
    case 'recency':
      WT.RECENCY_HALFLIFE = Math.max(1, parseInt(value) || 30);
      break;
    case 'base':
      WT.BASE = Math.max(0.40, Math.min(0.90, parseFloat(value)));
      break;
    case 'decay':
      WT.DECAY_ENABLED = !!(parseInt(value));
      break;
    default:
      return { error: `Unknown key: ${key}` };
  }
  return { [key]: key === 'recency' ? WT.RECENCY_HALFLIFE : (key === 'decay' ? WT.DECAY_ENABLED : (key === 'fast' ? activeFAST : activeCHAOS)) };
}

// ── Get current thresholds ────────────────────────────────────
export function getThresholds() {
  return {
    fast: activeFAST,
    chaos: activeCHAOS,
    truth: WT.TRUTH,
    integrated: WT.INTEGRATED,
    base: WT.BASE,
    decay: WT.DECAY_ENABLED,
    recencyHalflife: WT.RECENCY_HALFLIFE
  };
}

// ── Reset to defaults ────────────────────────────────────────
export function reset() {
  activeFAST = WT.FAST_THRESHOLD;
  activeCHAOS = WT.CHAOS_THRESHOLD;
  WT.BASE = 0.75;
  WT.DECAY_ENABLED = true;
  WT.RECENCY_HALFLIFE = 30;
}

// ── Export current config as JSON (for save/download) ───────
export function exportCalibration() {
  return {
    version: 'phase4',
    fast: activeFAST,
    chaos: activeCHAOS,
    truth: WT.TRUTH,
    integrated: WT.INTEGRATED,
    base: WT.BASE,
    decay: WT.DECAY_ENABLED,
    recencyHalflife: WT.RECENCY_HALFLIFE,
    exported: new Date().toISOString()
  };
}

// ── Import config ─────────────────────────────────────────────
export function importCalibration(config) {
  if (config.fast !== undefined)  activeFAST = config.fast;
  if (config.chaos !== undefined) activeCHAOS = config.chaos;
  if (config.base !== undefined)  WT.BASE = config.base;
  if (config.decay !== undefined) WT.DECAY_ENABLED = config.decay;
  if (config.recencyHalflife !== undefined) WT.RECENCY_HALFLIFE = config.recencyHalflife;
  return getThresholds();
}
