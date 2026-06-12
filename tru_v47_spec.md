# TRU v47 — The Sealed Wizard

## concept

TRU v47 is a sealed black box. No visible tribunal, no deliberation panels, no agent pills, no concept graph, no uncertainty meters — nothing that shows the inner machinery. Just: question → TRU answer.

The only control visible: BINARY MODE toggle (yes/no + confidence) and the brain import/export.

Underneath, the WIZARD operates. It is an invisible mathematical core that takes tribunal output and runs it through a thought formula — lambda calculus, golden ratio scaling, Fibonacci timing, Bayes weighting — to shape the final answer before it reaches the user. Merlin never shows his wand.

---

## what the user sees

```
┌─────────────────────────────────────┐
│  TRU v47                      📥📤  │  ← header: title + import/export only
├─────────────────────────────────────┤
│                                     │
│  [user question]                    │
│                                     │
│  TRU answer                         │  ← full screen, everything else hidden
│  ─ or ─                             │
│  YES 96%  NO 100%                   │  ← binary mode result
│  reasoning below                    │
│                                     │
├─────────────────────────────────────┤
│  [__________________] [SEND]        │  ← fixed input
├─────────────────────────────────────┤
│  NODES:12 | BINARY:OFF | COHERENCE: │  ← status strip (no panel clutter)
└─────────────────────────────────────┘
```

---

## the wizard — sealed mathematics

Runs after tribunal, before output. Never visible. Never logged to UI. Processes in the background.

### 1. Sentence Structure as Magic Formula

The wizard treats language as a formal system. A sentence has:

- **SUBJECT** → tribunal's primary entity/agent (who/what)
- **PREDICATE** → tribunal verdict (the relationship claimed)
- **OBJECT** → supporting evidence (the refinement)
- **ADVERBIAL** → confidence/uncertainty (the modifier)

```
SUBJECT [PREDICATE] OBJECT with ADVERBIAL certainty
```

Every TRU answer is a well-formed sentence following this formula. The wizard enforces it.

### 2. Golden Ratio Scaling (φ ≈ 1.618)

Applied to answer structure:

- **Answer length**: `goldenLength = baseLength × φ` — answers are scaled to golden ratio proportions
- **Confidence interval**: confidence ± (1/φ) — the margin around a verdict
- **Knowledge weight**: `weight = φ / (φ + decayFactor)` — recent nodes weigh φ× more than old ones
- **Verdict threshold**: `φ threshold = 0.618` — verdicts above φ are INTEGRATED, below are RESTRICTED

### 3. Lambda Calculus Decomposition

The wizard breaks the reasoning into lambda terms — composable, auditable, reversible:

```
λverdict.   (tribunalAgents × coherence) → finalAnswer
λentity.    λtype.  (who/what/when/where/how) → focusedEntity
λevidence.  λweight. (fact × confidence) → refinedEvidence
λwitness.   λcontradiction. (chaseOut × settleIn) → resolvedTruth
```

Each agent's reasoning is a lambda term. The wizard composes them:

```javascript
const wizardCompose = (agents, verdict, evidence, uncertainty) =>
  (λverdict(verdict))
    .apply(λentity(verdict.entity, verdict.type))
    .apply(λevidence(evidence, computeGoldenWeight(evidence)))
    .apply(λwitness(contradictions, computeBayesPosterior(contradictions)));
```

### 4. Y-Combinator (Recursive Self-Reference)

For iterative refinement of complex answers — the wizard can loop back on itself:

```javascript
const Y = λf. (λx. f(x(x)))(λx. f(x(x)));

// The wizard recursively refines answers until coherence meets threshold:
// refinement = (verdict × goldenRatio) → [refinedVerdict, iterations, settled]
```

### 5. Fibonacci Timing for Sentence Clauses

The wizard structures multi-clause answers using Fibonacci numbers as cadence markers:

- Clause 1: core claim (F₁ = 1)
- Clause 2: supporting evidence (F₂ = 1)
- Clause 3: complication from chaos agent (F₃ = 2)
- Clause 4: resolution (F₅ = 5)
- Clause 5+: use Fibonacci sequence for rhythm

```
[1 clause] = F₁ = 1 — single definitive claim
[2 clauses] = F₂ = 1 — claim + evidence
[3 clauses] = F₃ = 2 — claim + evidence + complication
[5 clauses] = F₅ = 5 — full structured answer
```

### 6. Bayes' Theorem for Evidence Weighting

Updates the tribunal's prior verdict with new evidence:

```javascript
const bayesUpdate = (prior, likelihood, normalization) =>
  (likelihood × prior) / normalization;

// P(truth | evidence) = P(evidence | truth) × P(truth) / P(evidence)
// Evidence from KNOWLEDGE_BASE nodes updates the wizard's posterior confidence
```

### 7. The Full Wizard Pipeline

```
tribunalOutput
    ↓
[1] decomposeIntoLambdas()      → lambda terms per agent
    ↓
[2] goldenRatioScaling()        → φ-weight evidence, set thresholds
    ↓
[3] bayesPosteriorUpdate()     → P(truth|evidence) given tribunal priors
    ↓
[4] fibonacciClauseStructure()→ arrange as Fₙ clauses
    ↓
[5] sentenceFormulaEnforce()  → SUBJECT PREDICATE OBJECT ADVERBIAL
    ↓
[6] yCombinatorRefine()       → loop until coherence > φ threshold
    ↓
[7] goldenConfidenceOutput()   → final confidence = (φ × coherence)
    ↓
→ final answer
```

---

## binary mode (still accessible)

When the user enables BINARY: ON:

- The wizard still runs the full pipeline
- Then applies a binary filter: the claim is reduced to YES or NO
- A big glowing YES/NO box appears at the top of the message
- The full reasoning still appears below

---

## brain upload/download

Still works via the 📥📤 buttons. Brain nodes feed into the wizard's BayesUpdate step. Import merges nodes into KNOWLEDGE_BASE. Export serializes the current brain state. The wizard uses the brain silently — no visual indication of brain activity.

---

## what's visible vs sealed

| visible | sealed (wizard runs this) |
|---|---|
| TRU logo + import/export | everything else |
| chat messages (input + output) | tribunal reasoning |
| BINARY toggle | lambda decomposition |
| status strip (nodes/coherence) | golden ratio scaling |
| | Bayes posterior update |
| | Fibonacci clause structure |
| | Y-combinator refinement |
| | sentence formula enforcement |

---

## version notes

- v47 = sealed v46 — same brain, same tribunal, same axioms, same agents, all hidden behind the wizard
- The math is real and applied — not decorative
- Merlin never shows his wand, but the magic is real
