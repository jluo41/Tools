# Skill commands: expose the revised lifecycle without breaking old calls
state: ✅ SETTLED · canonical skills and compatibility aliases migrated
owner: CC
method: Keep one router, introduce canonical lifecycle commands, and preserve old command names as explicit compatibility aliases.

## Opening
Which commands should a new user invoke, and how should old calls reach the revised lifecycle?
Mutating commands must cover initialization, one complete Calibration Round, sealed final evaluation, and corpus completion.
A separate status command remains read-only.
Old iterate, validate, and scale names may remain as aliases, but their panel-centered semantics cannot remain active.
This page fixes the canonical commands, resumable round boundary, compatibility behavior, and implementation-honesty rule.

**Where this page sits**: QA through QE define the method; QF2 and QF3 define the artifacts and agents each command may use.

**Why it matters**: A renamed menu with old internal assumptions would route users into unanimous auto-gold, public-kappa stopping, and unvalidated label inheritance.

## Writing Style
**Language and sentences**: State trigger, precondition, durable output, human gate, and stop condition for every command.

**Compatibility**: An alias must name the canonical command and report semantic migrations rather than silently emulating the old workflow.

**Honesty**: A skill must HOLD at an unimplemented engine boundary instead of claiming an artifact exists.

## Diagram
**Command lifecycle**: five canonical doors cover the complete project while three old names remain aliases.

```text
/label-init
   ↓
/label-round × N
   ↓
/label-evaluate
   ↓
/label-complete

/label-status reads every state

aliases: iterate → round · validate → evaluate · scale → complete
```

## Content

### 1 · Canonical command surface
**Five doors**: each command owns one lifecycle responsibility and one durable handoff.

```text
init      corpus + seal + embeddings + Round 1 readiness
round     C_t/P_t/B_t + Session + Checkpoint
evaluate  G* + blind T* gold + executor scorecards
complete  production + risk queue + final audit
status    read-only project and gate state
```

#### 1.1 · Initialization
`/label-init` validates the corpus, reserves sealed-test identifiers, creates embeddings for retrieval, initializes artifacts, and prepares the random Round 1 batch.
It does not require an objective function or a pre-existing label geometry.

#### 1.2 · Calibration Round
`/label-round` is resumable across candidate, prelabel, session, and checkpoint phases.
Round 1 takes its random batch directly, while later rounds create C_t, P_t, and B_t before human review.

#### 1.3 · Final evaluation and completion
`/label-evaluate` requires a QD4 stop and frozen G*, then creates late human gold and scorecards without optimization.
`/label-complete` requires an eligible production policy, labels the remainder, routes risk, and closes only after final audit.

### 2 · Compatibility aliases
**Migration path**: old names remain discoverable but cannot preserve retired semantics.

```text
iterate   alias to round
validate  alias to evaluate
scale     alias to complete
```

#### 2.1 · Alias response
An alias reports the canonical command before dispatch and notes any missing new prerequisite.
It never invokes the old panel-authority, public-license, or static-cascade path.

#### 2.2 · Project migration
Older projects require a schema and state migration before a canonical command writes new artifacts.
The router may inspect and propose migration, but it must not reinterpret prior model consensus as human gold.

### 3 · Gates and resumability
**Safe dispatch**: every mutating command reads state, resumes the exact open phase, and writes through the authorized keeper.

```text
🧾 state read
  ↓
✅ precondition check
  ↓
🔁 resume or start one phase
  ↓
📌 authorized write
  ↓
🧾 next state
```

#### 3.1 · Human gates
Semantic acceptance, blind adjudication, stopping signoff, and risk review cannot be auto-closed by the router.
The skill records the pending decision and stops at a durable boundary.

#### 3.2 · Implementation holds
When a required schema, script, or agent operation is not implemented, the command emits an explicit HOLD with the missing capability and safe next action.
It never fabricates a checkpoint, test score, or completed corpus.

## Aims

### A1 · 🚪 Canonical command surface
- A1.1 · Five commands cover initialization, rounds, evaluation, completion, and status.
  **Done when:** Router and canonical subskills expose the settled preconditions, outputs, and gates.

### A2 · 🔁 Compatibility aliases
- A2.1 · Old commands reach new semantics without treating retired artifacts as valid gold.
  **Done when:** Iterate, validate, and scale are thin, explicit aliases.

### A3 · 🛑 Gates and resumability
- A3.1 · Commands resume safely and stop honestly at human or implementation boundaries.
  **Done when:** Every subskill names its state transitions, write authority, and HOLD behavior.

## States

### A1 · 🚪 Canonical command surface
- ✅ A1.1 · Router plus init, round, evaluate, complete, and status skills expose the settled lifecycle and gates.

### A2 · 🔁 Compatibility aliases
- ✅ A2.1 · Legacy sl-* names resolve through the router, which rejects retired semantics; the alias skills themselves retired 260815.

### A3 · 🛑 Gates and resumability
- ✅ A3.1 · Every canonical mutating skill names resumable phases, human gates, write authority, and explicit HOLD behavior.

## Files

### Contracts · what this Page changes
- `../../skills/subjective-label/SKILL.md`
  The router must expose the canonical lifecycle and compatibility aliases.
- `../../skills/label-init/SKILL.md`
  Initialization must reserve the seal and prepare a random Round 1.
- `../../skills/label-round/SKILL.md`
  The canonical Calibration Round from C_t through closed D_t and G_t.
- `../../skills/label-evaluate/SKILL.md`
  The sealed final-test and executor-scorecard command.
- `../../skills/label-complete/SKILL.md`
  The validated production, reconciliation, and final-audit command.
- `../../skills/label-status/SKILL.md`
  The read-only state and gate dashboard.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QA0 page](1-QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  QA0 supplies the governing lifecycle and authority.

## Law
- 260806 JL · 🚪 The canonical skill lifecycle is init, round, evaluate, complete, and status
      Iterate, validate, and scale may remain compatibility aliases but cannot preserve retired panel-centered semantics.

## Glossary
- 🚪 **Canonical command**: the current supported lifecycle entry whose contract matches the governing Board.
- 🔁 **Compatibility alias**: an older command name that reports and dispatches to the canonical contract without keeping old behavior.
- 🛑 **Implementation HOLD**: a truthful stop at a required capability that has not yet shipped.

## Log

- 260816 · Commands renamed sl-* to label-* and the five skills moved to `skills/page-workflows/`; the three alias skills retired; this page and the board Links repointed.
260806 · Created QF1 to govern the subjective-label router and subskill migration.
260806 · Migrated five canonical skills and three compatibility aliases; all skill folders passed quick validation.
