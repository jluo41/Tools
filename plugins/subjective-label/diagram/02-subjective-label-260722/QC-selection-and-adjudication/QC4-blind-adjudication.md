# Blind adjudication: turn B_t into human gold without losing the trace
state: ✅ SETTLED
owner: JL
method: Lock a human-first record, reveal pre-labels only afterward, and preserve every clarification, revision, and policy-impact decision.

## Opening
How should the human and strong calibration agent adjudicate B_t so the final Y*_t reflects the human concept rather than committee anchoring?
The human first records class, region, uncertainty, and reason without seeing weak-model predictions.
Only then may the agent reveal disagreement and use it to probe the decision, diagnose guideline execution, or identify a concept change.
This page fixes the blind period, revision trace, unresolved state, and checkpoint handoff.

**Where this page sits**: QC3 freezes B_t, QB2 defines the conversational Session, and QB3 closes the resulting Y*_t and policy draft.

**Why it matters**: A final answer without its initial judgment cannot distinguish genuine correction from model-induced anchoring or concept revision.

## Writing Style
**Language and sentences**: State each adjudication event in chronological order with actor, version, and reason.

**Authority**: The strong agent may challenge and draft; the human alone confirms the final semantic record.

**Fields**: Keep class, region, uncertainty, rationale, and unresolved disposition separate.

## Diagram
**Blind-to-open sequence**: the committee becomes visible only after the human-first record is immutable.

```text
📄 item from B_t
      │
      ▼
🙈 human-first record
🏷 class · 🗺 region · 🌡 uncertainty · 🧾 reason
      │ lock
      ▼
🔓 reveal P_t comparison
      │
      ▼
💬 clarify · contrast · revise · flag impact
      │
      ▼
🏷 Y*_t or 🚨 unresolved
```

## Content

### 1 · Human-first record
**Initial judgment**: the target decision is recorded before committee outputs become available in the Session.

```text
🙈 first pass
├── 🏷 H | L | N
├── 🗺 one of seven regions
├── 🌡 uncertainty
├── 🧾 decisive evidence
└── ⚖️ strongest rejected label
```

#### 1.1 · Blind access
The human sees the item text, relevant source metadata, and the prior closed annotation policy.
The human does not see committee labels, counts, confidence, reasons, region predictions, or selection rank.

#### 1.2 · Immutable first pass
The first-pass record is timestamped and content-addressed before P_t opens.
A later correction appends a new state and never erases what the human initially believed.

### 2 · Post-reveal comparison
**Diagnostic conversation**: weak-model outputs become error evidence after they can no longer anchor the initial judgment.

```text
🙈 human record + 🔓 P_t
        │
        ├──▶ ✅ same label, same rule
        ├──▶ 🟡 same label, different reason
        ├──▶ 🔴 different label
        └──▶ 🌡 uncertainty conflict
```

#### 2.1 · Contrast questions
The strong agent asks which cited evidence is decisive, why the strongest alternative fails, and what smallest text change would flip the label.
It may present prior confirmed counterexamples without treating them as votes.

#### 2.2 · Guideline diagnosis
The comparison is classified as guideline ambiguity, missing boundary rule, misleading example, wrapper failure, executor limitation, or stochastic error.
Only guideline-addressable failures become policy-patch candidates.

### 3 · Revision and concept change
**Change trace**: every altered judgment names whether the human clarified, corrected, or revised the construct.

```text
🔁 changed answer
├── 🧹 momentary correction
├── 💡 clarification of existing intent
└── 🧠 concept revision
          │
          ▼
     🚨 backward-impact queue
```

#### 3.1 · Clarification
Clarification makes an intended boundary explicit without changing its meaning.
The trace links the new rule to affected current and earlier items.

#### 3.2 · Concept revision
A concept revision changes what H, L, or N means for the human authority.
It creates a mandatory backward-impact search and prevents checkpoint closure until affected prior gold is reviewed or explicitly queued.

#### 3.3 · Human confirmation
The human confirms the final class, region, uncertainty, reason, and change type.
The agent cannot close this record from model agreement or its own interpretation.

### 4 · Final disposition
**Round output**: each reviewed item reaches human gold or a visible unresolved state with a next owner.

```text
💬 reviewed item
├── 🏷 Y*_t final human record
└── 🚨 unresolved
      ├── missing context
      ├── policy hole
      └── human revisit required
```

#### 4.1 · Human gold
Y*_t preserves the final class, final region, uncertainty, rationale, first-pass link, pre-label comparison, policy version, and human identity.
Gold means human-confirmed for this project, not universally objective.

#### 4.2 · Unresolved state
An item may remain unresolved when required context is absent, the concept is actively changing, or the human declines a forced decision.
Unresolved is a disposition and never a fourth class or a substitute for NONE.

#### 4.3 · Checkpoint handoff
The Session closes only after all B_t items have a final or unresolved disposition and all policy-impact flags have owners.
QB3 then decides whether the complete round package can freeze.

## Aims

### A1 · 🙈 Human-first record
- A1.1 · Every adjudicated item has an immutable blind initial judgment.
  **Done when:** Class, region, uncertainty, reason, and rejected alternative are saved before P_t opens.

### A2 · 🔓 Post-reveal comparison
- A2.1 · Weak-model errors support diagnosis without redefining the target.
  **Done when:** The comparison and error category are attached to the item trace.

### A3 · 🔁 Revision and concept change
- A3.1 · Every changed decision distinguishes correction, clarification, and concept revision.
  **Done when:** Concept revisions create a backward-impact queue before checkpoint closure.

### A4 · 🏷 Final disposition
- A4.1 · Every B_t item reaches human gold or a visible unresolved state.
  **Done when:** The complete adjudication record passes to QB3 with no silent forced label.

## States

### A1 · 🙈 Human-first record
- ✅ A1.1 · Met; division 1 fixes the blind and immutable first pass.

### A2 · 🔓 Post-reveal comparison
- ✅ A2.1 · Met; division 2 defines the diagnostic reveal and error taxonomy.

### A3 · 🔁 Revision and concept change
- ✅ A3.1 · Met; division 3 fixes human confirmation and backward impact.

### A4 · 🏷 Final disposition
- ✅ A4.1 · Met; division 4 separates gold, unresolved, and checkpoint handoff.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [QC3 §4](QC-selection-and-adjudication/QC3-compose-human-batch.md)
  QC3 supplies the frozen B_t membership and item roles.
- `continues · ALL` · [QB3 page](QB-calibration-round/QB3-checkpoint-and-versions.md)
  QB3 freezes Y*_t, D_t, and G_t only after all dispositions are complete.

### Contracts · what must carry this rule
- `../../ref/ref-architecture.md`
  The architecture must enforce the blind access boundary and human authority.
- `../../ref/ref-schema.md`
  The schema must preserve first pass, final pass, unresolved state, and revision type.

## Law
- 260806 JL · 🙈 The human judgment is blind before weak-model outputs are revealed
      P_t opens only after the first-pass human record is locked, and every later change preserves its cause and backward impact.

## Glossary
- 🙈 **Human-first record**: the immutable class, region, uncertainty, and reason saved before weak-model predictions are visible.
- 🏷 **Human gold Y*_t**: the final human-confirmed item record produced in Calibration Round t.
- 🚨 **Backward-impact queue**: prior gold and policy rules that require review after a concept revision.

## Log
260806 · Created QC4 from the approved blind-adjudication and human-authority rules in QA0.
