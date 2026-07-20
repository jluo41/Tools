---
name: haipipe-paper-proof-checker
description: Rigorous mathematical proof verification and fixing workflow. Reads a LaTeX proof, identifies gaps via cross-model review (Codex GPT-5.4 xhigh), fixes each gap with full derivations, re-reviews, and generates an audit report. Use when user says "检查证明", "verify proof", "proof check", "审证明", "check this proof", or wants rigorous mathematical verification of a theory paper.
argument-hint: "[path-to-tex-file or proof-description]"
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Agent, mcp__codex__codex, mcp__codex__codex-reply
metadata:
  version: "1.2.0"
  last_updated: "2026-07-19"
  summary: "CHECK-phase PROOF sub-checker (internal, conditionally dispatched): rigorous verification and repair of LaTeX proofs — read, find gaps via cross-model review, fix each with full derivations, re-review, emit an audit report. Dispatched BY haipipe-paper-check when a section carries a proof; it is not the CHECK gate itself and does not run alone as one. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Proof Checker: Rigorous Mathematical Verification & Fixing

Systematically verify a mathematical proof via cross-model adversarial review, fix identified gaps, re-review until convergence, and generate a detailed audit report with proof-obligation accounting.

## Context: $ARGUMENTS

## Constants

- MAX_REVIEW_ROUNDS = 3
- REVIEWER_MODEL = `gpt-5.4` via Codex MCP, reasoning effort always `xhigh`
- **REVIEWER_BACKEND = `codex`** — Default: Codex MCP (xhigh).
  Override with `— reviewer: oracle-pro` for GPT-5.4 Pro via Oracle MCP.
  See `Tools/legacy/dikw-full/research-toolkit/skills/00_meta/shared-references/reviewer-routing.md`.
- AUDIT_DOC: `PROOF_AUDIT.md` at the paper directory root, alongside `main.tex` (cumulative log).
  Primary caller: `haipipe-paper-check` dispatches this skill as its PROOF sub-checker.
- REPORT_TEX: `proof_audit_report.tex` (formal before/after PDF)
- STATE_FILE: `PROOF_CHECK_STATE.json` (for recovery)
- SKELETON_DOC: `PROOF_SKELETON.md` (micro-claim inventory)

### Acceptance Gate (objective, replaces subjective scoring)

The proof passes when ALL of the following hold:
1. Zero open FATAL or CRITICAL issues
2. Every theorem/lemma has: (i) explicit hypotheses, (ii) proof with all interchanges justified, (iii) every application discharges hypotheses in the ledger
3. All big-O/Θ/o statements have declared parameter dependence and uniformity scope
4. Counterexample pass executed on all key lemmas (log candidates even if none found)

## Issue Taxonomy (20 categories, 4 groups)

The 20 categories in 4 groups -- A Logic & Proof Structure, B Analysis & Measure Theory, C Model & Parameter Tracking, D Scope & Claims -- live in `ref/issue-taxonomy.md`.

## Two-Axis Severity System

### Axis A — Proof Status (what is wrong)

| Status | Meaning |
|--------|---------|
| **INVALID** | Statement false as written (counterexample exists or contradiction) |
| **UNJUSTIFIED** | Could be true, but current proof does not establish it |
| **UNDERSTATED** | True only after strengthening assumptions |
| **OVERSTATED** | True only after weakening conclusion / adding qualifiers |
| **UNCLEAR** | Ambiguous notation / definition drift (not wrong per se) |

### Axis B — Impact (how much breaks)

| Impact | Meaning |
|--------|---------|
| **GLOBAL** | Breaks main theorem or core dependency chain |
| **LOCAL** | Affects a side result but not the main theorem |
| **COSMETIC** | Exposition only |

### Severity Labels (derived)

| Label | Definition |
|-------|------------|
| **FATAL** | INVALID + GLOBAL |
| **CRITICAL** | (INVALID + LOCAL) or (UNJUSTIFIED + GLOBAL) |
| **MAJOR** | (UNJUSTIFIED + LOCAL) or (UNDERSTATED/OVERSTATED + GLOBAL) |
| **MINOR** | Clarity / notation / dimension bookkeeping that doesn't change claims |

## Side-Condition Checklists for Common Theorems

The required-conditions cheat-sheet (DCT, MCT, Fubini/Tonelli, Leibniz integral rule, Implicit Function Theorem, Taylor with remainder, Jensen, Cauchy-Schwarz, Weyl/Davis-Kahan, analytic continuation, WLOG reduction) lives in `ref/side-conditions.md` -- when the proof invokes any of them, require explicit verification of ALL its listed conditions.

## Workflow

### Phase 0: Preparation

1. **Locate the proof**: Find the main `.tex` file(s).
2. **Read the entire proof**: Extract list of all theorems/lemmas/propositions/corollaries/definitions/assumptions.
3. **Read reference materials**: Reference papers, prior results.
4. **Build a section map**: Structured list with line numbers and key claims.
5. **Identify the main theorem**: Central result, assumptions, claims.

### Phase 0.5: Proof-Obligation Ledger

Build formal accounting artifacts.
Save to `PROOF_SKELETON.md`:

#### 1. Dependency DAG
Nodes = Definitions / Assumptions / Lemmas / Theorems.
Edges = "uses".
**Detect cycles** (including semantic circularity where Lemma A uses a corollary that quietly depends on A).

#### 2. Assumption Ledger
For each theorem/lemma, list every hypothesis with WHERE each is verified (or mark "UNVERIFIED").
Track **usage-minimal assumption sets** — which assumptions were actually used vs merely stated.

#### 3. Typed Symbol Table
Each symbol must have a **type signature**:
```
κ : scalar ∈ (0,1), depends on (d, α_t, Σ, μ)
u* : vector ∈ ℝ^d, u* = C^{-1}m
B^even : matrix ∈ ℝ^{(L+1)×(L+1)}, symmetric PSD
Ψ_v : function ℝ → ℝ, analytic in (ζ,κ), parity determined by v
```
Flag any symbol whose meaning changes or whose type is inconsistent across uses.

#### 4. Canonical Quantified Statements
For each theorem/lemma, rewrite the statement with **explicit quantifiers, domains, and limit order**:
```
∀K ≥ 3, ∀π ∈ Π_K^{ms,∘} \ E_K, ∃κ_0 > 0 such that ∀κ ∈ (0, κ_0):
  h_act^{(K,π)} = Θ(κ^{α_K^act})  [uniform in π on compact subsets]
```
If you cannot restate a theorem this precisely, mark it **UNCLEAR — needs disambiguation**.

#### 5. Micro-Claim Inventory
Every nontrivial step becomes a numbered micro-claim in **sequent form**:
```
MC-17: Context: [Lemma 3.1, κ < κ_0, Z_κ has bounded moments up to order 2m+2]
       ⊢ Goal: P̂_0 is positive definite
       Rule: monomials linearly independent on support of continuous distribution
       Side-conditions: positive density near origin ✓ (by GMM weak convergence)
```
Each micro-claim has: justification rule name + required conditions + where conditions are proven.

#### 6. Limit-Order Map
Track every asymptotic statement's **limit order and uniformity scope**:
```
h_act = Θ(κ^α)  [as κ→0, uniform in π on compact subsets of Π_K, for fixed K]
τ_act ~ (b/a)n   [as n→∞, for fixed κ,K,π with x_K ≪ 1]
```
Flag any statement where limit order is ambiguous or uniformity is unclear.

### Phase 1: First Review (Codex GPT-5.4 xhigh)

Submit the **complete proof content** with the following **mandatory reviewer checklist** in the prompt:

The mandatory reviewer-checklist prompt -- checks A (definitions) through H (dependency consistency) plus the per-issue output format -- is in `ref/reviewer-prompt.md` (Phase 1 prompt). Dispatch it verbatim as a fresh `mcp__codex__codex` xhigh thread with the **complete proof content** appended.

**Save the threadId.**
Parse into structured issue list.
Write to `PROOF_AUDIT.md`.

### Phase 1.5: Counterexample Red Team

For each CRITICAL or MAJOR issue, and for every key lemma that introduces:
- a new inequality bound
- an identifiability/uniqueness claim
- a curvature/PSD/strong convexity assertion
- a uniform-in-parameter claim
- a convergence mode upgrade (pointwise → uniform, in prob → w.h.p.)

Systematically attempt to construct counterexamples using:

| Strategy | Description |
|----------|-------------|
| **Dimensional collapse** | Set d=1 or 2, K=2, n small |
| **Degeneracy** | Singular covariance, tiny weight, overlapping means, identical components |
| **Extremal distributions** | Two-point ±a, bounded non-subGaussian, heavy tails |
| **Adversarial parameter scaling** | Pick parameters making neglected terms dominate |
| **Numeric falsification** | Translate lemma to a function, brute-force optimize over small domain |

**Rule**: Label "counterexample found" ONLY if algebraically verified.
Otherwise log as "candidate counterexample — needs verification."

Record all attempts (successful or not) in `PROOF_AUDIT.md`.

### Phase 2: Fix Implementation

For each issue, ordered by severity (FATAL → CRITICAL → MAJOR → MINOR):

#### Step 2a: Choose fix strategy
For each issue, explicitly choose one of:
- **ADD_DERIVATION**: Write missing proof steps
- **STRENGTHEN_ASSUMPTION**: Add conditions to theorem statement
- **WEAKEN_CLAIM**: Reduce conclusion scope
- **ADD_REFERENCE**: Cite known result + verify its conditions apply

Log this choice — it is a scope-changing decision when it alters theorem statements.

#### Step 2b: Derive the fix mathematically
- Complete mathematical derivation, not just a claim
- If new proposition/lemma needed, write in full theorem-proof style

#### Step 2c: Implement in LaTeX
- Edit the `.tex` file
- Preserve existing `\label` references where possible

#### Step 2d: Record the fix
```markdown
### Fix N: [SHORT TITLE]
**Issue**: [id] [CATEGORY] — [description]
**Severity**: FATAL / CRITICAL / MAJOR / MINOR
**Status**: INVALID / UNJUSTIFIED / UNDERSTATED / OVERSTATED
**Impact**: GLOBAL / LOCAL / COSMETIC
**Fix strategy**: ADD_DERIVATION / STRENGTHEN_ASSUMPTION / WEAKEN_CLAIM / ADD_REFERENCE
**Location**: Section X, Lines Y-Z

**BEFORE**: [what the proof originally did]
**WHY WRONG**: [mathematical problem, with counterexample if applicable]
**AFTER**: [what the fix does]
**KEY EQUATION**: [central new equation]
**PROOF OBLIGATIONS ADDED**: [new conditions/lemmas introduced]
**DOWNSTREAM EFFECTS**: [which results now need re-checking]
```

#### Step 2e: Compile check
```bash
pdflatex -interaction=nonstopmode <file>.tex 2>&1 | grep -E "Error|Warning|undefined"
```

### Phase 3: Re-Review (Codex GPT-5.4 xhigh)

Use `codex-reply` with saved threadId.
Include fix summaries.
Request the same mandatory checklist.

Check acceptance gate.
If not met, repeat Phases 2-3 (up to MAX_REVIEW_ROUNDS).

### Phase 3.5: Global Closure & Independent Verification

#### Global closure checks
After all fixes, verify the proof as a whole:
- **Statement–conclusion match**: Does the proof end with EXACTLY what the theorem claims (quantifiers, constants, uniformity)?
- **All obligations discharged**: Every node in the obligation DAG is proven or explicitly assumed (and the theorem statement includes it).
- **Case analysis coverage**: Cases partition the domain AND include boundary/degenerate cases.
- **Induction correctness** (if applicable): Base case, inductive step, correct use of IH, induction measure strictly decreases.
- **WLOG reductions**: Each "without loss of generality" spawns a micro-claim proving the reduction is lossless.
- **No silent assumption strengthening**: Any fix that strengthened assumptions has propagated to the main theorem statement.

#### Independent second review for FATAL/CRITICAL fixes
For any fix that resolved a FATAL or CRITICAL issue, submit the **fixed section alone** (without showing the previous critique) to a **fresh Codex thread**:

The blind-review prompt is in `ref/reviewer-prompt.md` (Phase 3.5 prompt) -- dispatch the **fixed section alone** (no prior critique shown) as a fresh `mcp__codex__codex` xhigh thread.

If the blind reviewer finds new issues, re-enter Phase 2.

#### Regression proof-audit
After fixes, re-run:
- DAG acyclicity check (no new cycles introduced)
- Counterexample suite on all DOWNSTREAM lemmas of modified results
- Assumption-delta report: what became stronger/weaker due to fixes?

### Phase 3.9: Unrecoverable Proof Protocol

If acceptance gate is not met after MAX_REVIEW_ROUNDS, output a **Proof Unrecoverable Report**:
1. Minimal set of blocking FATAL/CRITICAL issues that could not be resolved
2. Salvage options ranked: (a) weaken claim, (b) strengthen assumptions, (c) add missing lemmas, (d) restructure argument
3. Which parts of the proof are likely still reusable
4. Recommended next steps for the author

Do NOT silently declare success.
The report must be honest.

### Phase 4: Audit Report Generation

Generate `proof_audit_report.tex` with:

1. **Overview table**: All issues with two-axis severity, category, fix strategy, status
2. **Before/After logic chain**: Red (BEFORE) → Green (AFTER) comparison
3. **For each fix**: original proof → why wrong → counterexample (if any) → complete derivation → remaining subtleties
4. **Proof-obligation diff**: What was unverified before, what is verified now
5. **Summary**: Now proven / still assumed / open problems
6. **Colored boxes**: BEFORE (red), AFTER (green), WHY WRONG (orange), KEY INSIGHT (blue), WARNING (yellow)

Compile: `pdflatex proof_audit_report.tex && pdflatex proof_audit_report.tex`

### Phase 5: State Persistence

Write `PROOF_CHECK_STATE.json`:
```json
{
  "status": "completed",
  "rounds": 2,
  "threadId": "...",
  "fatal_fixed": 0,
  "critical_fixed": 3,
  "major_fixed": 2,
  "minor_fixed": 1,
  "counterexamples_found": 1,
  "counterexample_candidates": 2,
  "acceptance_gate": "PASS",
  "timestamp": "..."
}
```

## Output Files

| File | Content | When |
|------|---------|------|
| `PROOF_SKELETON.md` | Dependency DAG + assumption ledger + micro-claims | Phase 0.5 |
| `PROOF_AUDIT.md` | Cumulative round-by-round audit log | Updated each round |
| `PROOF_AUDIT.json` | Machine-readable submission verdict (see below) | Always emitted |
| `proof_audit_report.tex/.pdf` | Formal before/after report | Phase 4 |
| `PROOF_CHECK_STATE.json` | State for recovery | Phase 5 |

## Submission Artifact Emission

This skill **always** writes `PROOF_AUDIT.json` at the paper directory root (`<your-paper-dir>/PROOF_AUDIT.json`; the legacy `/paper-writing` flow used `paper/`), regardless of caller or whether the paper contains theorems.
A paper with no `\begin{theorem}` / `\begin{lemma}` / `\begin{proof}` emits verdict `NOT_APPLICABLE`; silent skip is forbidden.
The CHECK gate (haipipe-paper-check, the primary caller) and the legacy `Tools/legacy/dikw-full/research-toolkit/tools/verify_paper_audits.sh` both rely on this artifact existing at `<paper-dir>/PROOF_AUDIT.json`.

The artifact conforms to the schema in `Tools/legacy/dikw-full/research-toolkit/skills/00_meta/shared-references/assurance-contract.md`:

```json
{
  "audit_skill":      "haipipe-paper-proof-checker",
  "verdict":          "PASS | WARN | FAIL | NOT_APPLICABLE | BLOCKED | ERROR",
  "reason_code":      "all_proofs_complete | minor_gaps | critical_gap | no_theorems | ...",
  "summary":          "One-line human-readable verdict summary.",
  "audited_input_hashes": {
    "main.tex":                 "sha256:...",
    "sections/4.theory.tex":    "sha256:..."
  },
  "trace_path":       ".aris/traces/haipipe-paper-proof-checker/<date>_run<NN>/",
  "thread_id":        "<codex mcp thread id>",
  "reviewer_model":   "gpt-5.4",
  "reviewer_reasoning": "xhigh",
  "generated_at":     "<UTC ISO-8601>",
  "details": {
    "theorems_audited": <int>,
    "issues": [ { "id": "T1-H3", "severity": "FATAL|CRITICAL|MAJOR|MINOR",
                  "category": "quantifier|domination|...",
                  "location": "sections/4.theory.tex:L182",
                  "note": "..." }, ... ]
  }
}
```

### `audited_input_hashes` scope

Hash the **declared input set** actually reviewed — the theorem-bearing `.tex` files passed into this invocation — not a repo-wide union and not the reviewer's self-reported opened subset.
The external verifier rehashes these entries; any mismatch flags `STALE`.

**Path convention** (must match `Tools/legacy/dikw-full/research-toolkit/tools/verify_paper_audits.sh`): keys are **paths relative to the paper directory** (no `paper/` prefix — the verifier resolves relative to the paper dir; prefixing produces `paper/paper/...` and false-fails as STALE).
Use **absolute paths** for files outside the paper dir.

### Verdict decision table

| Input state                                           | Verdict          | `reason_code` example |
|-------------------------------------------------------|------------------|-----------------------|
| No theorems / lemmas / proofs in paper                | `NOT_APPLICABLE` | `no_theorems`         |
| Theorems present but referenced files unreadable      | `BLOCKED`        | `source_unreadable`   |
| All proof obligations discharged, no gaps             | `PASS`           | `all_proofs_complete` |
| Only MINOR issues (notation / exposition)             | `WARN`           | `minor_gaps`          |
| Any FATAL or CRITICAL issue (logic gap, wrong claim)  | `FAIL`           | `critical_gap`        |
| Reviewer invocation failed (network / malformed)      | `ERROR`          | `reviewer_error`      |

MAJOR issues alone map to `WARN` or `FAIL` at the reviewer's discretion and must carry an explicit justification in `summary` + `details.issues`.

### Thread independence

Every invocation uses a fresh `mcp__codex__codex` thread.
Never `codex-reply` across haipipe-paper-proof-checker runs.
Do not accept prior audit outputs (PAPER_CLAIM_AUDIT, CITATION_AUDIT, EXPERIMENT_LOG) as input — the fresh thread preserves reviewer independence per `Tools/legacy/dikw-full/research-toolkit/skills/00_meta/shared-references/reviewer-independence.md`.

This skill never blocks by itself; the caller decides whether the verdict blocks — today that is haipipe-paper-check (CHECK gate outcome), historically `/paper-writing` Phase 6 plus the legacy verifier via the `assurance` level.

## Example Invocations

```
/haipipe-paper-proof-checker "neurips_2025.tex"
/haipipe-paper-proof-checker "check the GMM generalization proof, focus on dimension dependence"
/haipipe-paper-proof-checker "verify proof in paper.tex — difficulty: nightmare"
```
