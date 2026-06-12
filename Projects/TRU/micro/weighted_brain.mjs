// TRU MICRO: Weighted Brain — Dog Logic ranking engine
// Heaviest nodes rank first. Weight is confidence × recency × source trust.
// This is the core data structure for TRU Phase 4+

import { WT } from '../shared/constants.mjs';
import { levenshtein, applyDecay } from './utils.mjs';

// ── WNode factory ────────────────────────────────────────────
export function makeNode(k, v, overrides = {}) {
  return {
    k, v,
    t: 'fact',
    w: WT.BASE,
    source: 'CERTIFIED',
    refined_by: [],
    storm_count: 0,
    refine_count: 0,
    accesses: 0,
    last_used: new Date().toISOString(),
    created_by: 'factory',
    ...overrides
  };
}

// ── WeightedBrain ───────────────────────────────────────────
export class WeightedBrain {
  constructor(nodes = []) {
    this.nodes = nodes;
  }

  // Size
  get size() { return this.nodes.length; }

  // Add node
  add(node) {
    const existing = this.nodes.findIndex(n => n.k === node.k);
    if (existing >= 0) {
      // Keep higher weight on collision
      if (node.w > this.nodes[existing].w) {
        this.nodes[existing] = { ...node, last_used: new Date().toISOString() };
      }
    } else {
      this.nodes.push(node);
    }
  }

  // Fetch top-K nodes by computed weight
  fetch(query, k = WT.MAX_NODES || 5) {
    const ql = query.toLowerCase();
    const qtoks = ql.split(/\s+/).filter(t => t.length > 1);

    const results = this.nodes
      .map(n => this._computeScore(query, n, ql, qtoks))
      .filter(r => r.score > 0)
      .sort((a, b) => b.score - a.score || b.node.w - a.node.w)
      .slice(0, k);

    return results;
  }

  // Internal scoring: raw relevance × weight × recency × source trust
  _computeScore(query, node, ql, qtoks) {
    let raw = 0, matchType = 'none';

    // Exact/exact-match on key
    if (node.k.toLowerCase() === ql) { raw = 1.0; matchType = 'exact'; }
    // Partial key match
    else if (node.k.toLowerCase().includes(ql)) { raw = 0.80; matchType = 'key_hit'; }
    else if (ql.includes(node.k.toLowerCase())) { raw = 0.70; matchType = 'query_hit'; }
    // Token overlap
    else {
      const ktoks = node.k.toLowerCase().split(/[_\s]+/);
      let matches = 0;
      for (const qt of qtoks) {
        for (const kt of ktoks) {
          if (kt.startsWith(qt) || qt.startsWith(kt)) matches++;
        }
      }
      raw = (matches / Math.max(qtoks.length, 1)) * 0.5;
      if (raw > 0) matchType = 'token';
    }
    // Value search boost
    if (raw < 0.4) {
      const vl = node.v.toLowerCase();
      for (const qt of qtoks) {
        if (qt.length < 3) continue;
        if (vl.includes(qt)) { raw = Math.max(raw, 0.45); matchType = 'value'; break; }
      }
    }
    if (raw === 0) return { node, score: 0, attnWeight: 0, matchType: 'none' };

    // Apply weight components
    const decayFactor = WT.DECAY_ENABLED ? this._recencyFactor(node) : 1.0;
    const sourceTrust = WT[`SOURCE_${node.source?.toUpperCase()}`] || WT.SOURCE_ARCHIVIST;
    const score = raw * node.w * decayFactor * sourceTrust;
    const attnWeight = score; // attention weight = final score

    return { node, score, attnWeight, matchType };
  }

  _recencyFactor(node) {
    if (!node.last_used) return 1.0;
    const days = (Date.now() - new Date(node.last_used).getTime()) / 86400000;
    return Math.pow(0.5, days / WT.RECENCY_HALFLIFE);
  }

  // Self-refinement: update node weight from tribunal feedback
  refine(nodeKey, delta) {
    const node = this.nodes.find(n => n.k === nodeKey);
    if (!node) return null;
    node.refine_count++;
    node.refined_by.push({ delta, at: new Date().toISOString() });
    // Bayesian update: new_w = old_w + delta * (1 - old_w)
    node.w = Math.min(WT.MAX_WEIGHT, Math.max(WT.MIN_WEIGHT, node.w + delta * (1 - node.w)));
    node.last_used = new Date().toISOString();
    return { ...node };
  }

  // Record access
  touch(nodeKey) {
    const node = this.nodes.find(n => n.k === nodeKey);
    if (node) { node.accesses++; node.last_used = new Date().toISOString(); }
  }

  // Remove fragile nodes (weight below minimum sustained)
  prune(threshold = WT.MIN_WEIGHT * 0.9) {
    const before = this.nodes.length;
    this.nodes = this.nodes.filter(n => n.w >= threshold);
    return before - this.nodes.length;
  }

  // Storm inject (with boost)
  stormInject(nodes) {
    const added = [];
    nodes.forEach(n => {
      if (!this.nodes.find(o => o.k === n.k)) {
        this.nodes.push(n);
        added.push(n);
      }
    });
    return added;
  }

  // JSON serialize
  toJSON() { return [...this.nodes]; }
  static fromJSON(arr) { return new WeightedBrain(arr.map(n => ({ ...n }))); }
}
