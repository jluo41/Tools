# Execute: what must be proved before the Application revision is complete
state: 🟡 PARTIAL · static and fresh-context validation passed · open: runtime specimens
owner: CC

## Opening

What distinguishes a coherent design from a working skill set?

Four kinds of evidence: structural validation of every skill, mechanical Board build/check/gate, fresh-context routing behavior, and runtime Page specimens.
This revision can ship for review with the first three while keeping the specimen debt visible.

### Writing Style

State command, input, observable result, and unresolved debt. A passing validator does not prove a runtime Page exists.

## Diagram

```text
1 skill validators ─┐
2 Board build/check ├─▶ revision reviewable
3 fresh agent run ──┘
4 runtime specimens ──▶ production-complete
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

Validate Application 0.8.0 and all four Page Type folders for frontmatter, required files, and readable references.

#### 2 · Board validation

Rebuild the Board, run the mechanical checker, and close the write gate against the pre-edit baseline.

#### 3 · Fresh-context behavior

A new agent must discover the public skill, identify all four Page Types, put a missing premise into a local Insight Page, keep Probe out of Design, and apply the Artifact promotion test.

#### 4 · Runtime debt

Materialize one Brief, one Insight with Design Handoff, one Design with visible projection, and one stale Artifact negative case. These are product-hardening tasks, not hidden prerequisites for reviewing the architecture version.

## Aims

### A1 · Contract
- A1.1 · Skills and Board pass their mechanical validators.
  **Done when:** receipts are written in the Log.

#### A2 · Fresh context
- A2.1 · A new agent follows the intended route without discussion context.
  **Done when:** QF2 records pass/fail against explicit criteria.

#### A3 · Runtime
- A3.1 · Four positive/negative specimens exercise closing semantics.
  **Done when:** QBt/QI specimen States are green.

## States

### A1 · Contract
- ✅ A1.1 · Seven revised skills passed `quick_validate`; Page Type registry tests passed 2/2; Board gate passed with zero errors and no new warnings.

#### A2 · Fresh context
- ✅ A2.1 · Two fresh-context agents selected the local Insight route, many-Design cardinality, no-Probe Design boundary, and projection-first Artifact rule.

#### A3 · Runtime
- ⬜ A3.1 · Brief, Insight, Design projection, and stale Artifact specimens remain.

## Files

### 🧪 Checks
- `../../../../board/haipipe-board/cli/build.py`
- `../../../../board/haipipe-board/cli/check.py`
- `../../../../board/haipipe-board/cli/gate.py`

### 📋 Contracts
- `../../../../application/haipipe-application/SKILL.md`

## Law

Static pass, fresh-agent pass, and runtime specimen pass are three different claims and must never be merged.

## Log

260820 · Defined the validation stack for Application 0.8.0.
260820 · `quick_validate` passed Application, four Page Types, Page, and Board; registry test passed 2/2.
260820 · Board build/check/gate passed at 39 Pages, zero errors, zero gaps, and no Page warning regression.
260820 · QF2 recorded two fresh-context behavior passes; runtime Page specimens remain explicit hardening debt.
