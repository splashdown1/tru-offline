// TRU MICRO: Self-Refinement — Learning from conversation
// Dog logic: heavier nodes absorb lighter nodes on proximity
// Heavier weight = stronger identity. Conflicting facts merge, not overwrite.

import { WT } from '../shared/constants.mjs';
import { levenshtein } from './utils.mjs';
import { WeightedBrain } from './weighted_brain.mjs';

export class SelfRefinement {
  constructor(brain) {
    this.brain = brain;
    this.sessionGains = []; // track weight changes this session
  }

  // Called after every TRU response. Delta from 0.0–1.0 (confidence delta).
  // delta > 0: response was helpful. delta < 0: response was wrong/confident but wrong.
  record(delta) {
    this.sessionGains.push(delta);
  }

  // End-of-session: apply all deltas to relevant nodes
  finalize() {
    if (this.sessionGains.length === 0) return { nodesRefined: 0, gains: [] };

    // Average session delta
    const avgDelta = this.sessionGains.reduce((a, b) => a + b, 0) / this.sessionGains.length;

    // Find the most recently touched node (proxy for "responded node")
    const lastTouched = this.brain.nodes
      .filter(n => n.last_used)
      .sort((a, b) => new Date(b.last_used) - new Date(a.last_used))[0];

    if (lastTouched) {
      const refined = this.brain.refine(lastTouched.k, avgDelta);
      this.sessionGains = [];
      return { nodesRefined: 1, gains: [avgDelta], refined: refined?.k };
    }

    return { nodesRefined: 0, gains: [avgDelta] };
  }

  // Dog logic: when two nodes are similar, heavier one absorbs lighter one
  mergeSimilar(threshold = 0.75) {
    const merged = [];
    const toRemove = new Set();

    for (let i = 0; i < this.brain.nodes.length; i++) {
      if (toRemove.has(i)) continue;
      for (let j = i + 1; j < this.brain.nodes.length; j++) {
        if (toRemove.has(j)) continue;

        const a = this.brain.nodes[i];
        const b = this.brain.nodes[j];

        // Check key similarity
        const keySim = 1 - levenshtein(a.k, b.k) / Math.max(a.k.length, b.k.length, 1);
        // Check value similarity
        const valSim = 1 - levenshtein(a.v, b.v) / Math.max(a.v.length, b.v.length, 1);
        // Combined similarity
        const sim = (keySim * 0.4 + valSim * 0.6);

        if (sim >= threshold) {
          // Heavier node absorbs lighter
          const [heavier, lighter] = a.w >= b.w ? [a, b] : [b, a];
          heavier.w = Math.min(WT.MAX_WEIGHT, heavier.w + WT.STORM_BOOST);
          heavier.refined_by.push({
            type: 'dog_merge',
            absorbed: lighter.k,
            sim,
            at: new Date().toISOString()
          });
          toRemove.add(this.brain.nodes.indexOf(lighter));
          merged.push({ heavier: heavier.k, lighter: lighter.k, sim: sim.toFixed(2) });
        }
      }
    }

    this.brain.nodes = this.brain.nodes.filter((_, i) => !toRemove.has(i));
    return merged;
  }

  // Adaptive thresholds: adjust FAST/CHAOS based on session accuracy
  adaptFromSession(goodCount, totalQueries) {
    if (totalQueries < 3) return; // need minimum data

    const accuracy = goodCount / totalQueries;
    const baseFAST = 0.85;
    const baseCHAOS = 0.45;

    // If accuracy is high, trust more (lower thresholds)
    // If accuracy is low, be more skeptical (higher thresholds)
    let newFAST = baseFAST;
    let newCHAOS = baseCHAOS;

    if (accuracy >= 0.85) {
      newFAST = baseFAST - 0.05; // trust more
      newCHAOS = baseCHAOS - 0.05;
    } else if (accuracy <= 0.50) {
      newFAST = baseFAST + 0.05; // be more careful
      newCHAOS = baseCHAOS + 0.05;
    }

    // Store adapted thresholds as meta-nodes
    const existingFAST = this.brain.nodes.find(n => n.k === 'adapted_fast_threshold');
    const existingCHAOS = this.brain.nodes.find(n => n.k === 'adapted_chaos_threshold');

    if (existingFAST) existingFAST.v = newFAST.toFixed(2);
    else this.brain.add({ k: 'adapted_fast_threshold', v: newFAST.toFixed(2), t: 'meta', w: 0.5, source: 'ADAPTED' });

    if (existingCHAOS) existingCHAOS.v = newCHAOS.toFixed(2);
    else this.brain.add({ k: 'adapted_chaos_threshold', v: newCHAOS.toFixed(2), t: 'meta', w: 0.5, source: 'ADAPTED' });

    return { newFAST, newCHAOS, accuracy };
  }
}
