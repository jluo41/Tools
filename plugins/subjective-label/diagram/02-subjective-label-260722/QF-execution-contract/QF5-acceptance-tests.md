# Acceptance tests: prove a fresh agent follows the revised workflow
state: ✅ SETTLED · static and fresh-context validation passed after one notation repair
owner: CC
method: Combine Board checks, skill validation, artifact-contract tests, realistic fresh-context scenarios, and explicit residual-risk reporting.

## Opening
What evidence will show that the revised Board and skill family work for an agent that did not participate in this discussion?
Mechanical checks catch broken files and schemas.
Only a fresh task run reveals whether the router grants authority to model consensus or leaks sealed predictions.
The test must inspect process, artifacts, gates, and stopping behavior rather than judging only a polished final answer.
This page fixes the validation layers, five scenarios, failure criteria, and receipt.

**Where this page sits**: QF1 through QF4 define what must be tested; this page is the final gate for the documentation and skill migration.

**Why it matters**: A skill can describe the new method in one file while another agent follows an older subskill, agent prompt, or reference and silently recreates the retired workflow.

## Writing Style
**Language and sentences**: Give each test an input, expected process, expected artifacts, forbidden behavior, and verdict.

**Freshness**: Do not give a reviewer the intended answer, suspected bug, or discussion history.

**Evidence**: Preserve raw prompts, tool traces, artifacts, check output, and smallest fixes.

## Diagram
**Validation stack**: mechanical checks support, but do not replace, fresh-context behavioral tests.

```text
🧪 Board build + checker
        ↓
🧪 skill folder validation
        ↓
🧪 contract and schema fixtures
        ↓
🤖 fresh-agent end-to-end runs
        ↓
👁 process review + repair loop
        ↓
✅ migration receipt
```

## Content

### 1 · Static and structural checks
**Mechanical gate**: sources, links, metadata, schemas, and skill frontmatter must be valid before behavior is tested.

```text
Board: build · check · render · reachability
Skills: frontmatter · names · routes · stale references
Contracts: schema fixtures · state transitions · provenance fields
```

#### 1.1 · Board checks
The Board builds with zero errors, no new warnings, reachable pages, valid scoped links, and no governing contradiction with QA0.
Existing warnings are removed or recorded with an explicit accepted reason.

#### 1.2 · Skill checks
Every canonical and compatibility skill passes `quick_validate.py` or the repository's equivalent validation.
Searches find no active claims that panel consensus creates gold, public kappa defines convergence, or embeddings inherit final labels.

### 2 · Fresh-context scenarios
**Behavioral gate**: a new agent receives a realistic user request and the migrated skill, not the expected workflow.

```text
S1 initialize random Round 1
S2 later round with disagreement + consensus audit
S3 reject low plateau
S4 sealed final evaluation
S5 production + risk + final audit
```

#### 2.1 · Initialization scenario
A vague trait and unlabeled corpus must produce test reservation, retrieval embeddings, a random Round 1 batch, and a human-first Session plan.
Failure includes requiring an objective function, model-generated initial gold, or preassigned seven regions.

#### 2.2 · Later-round scenario
A closed G_1 and cumulative human gold must produce C_2, independent sealed P_2, B_2 with disagreement priority and random consensus audit, blind first-pass adjudication, and Checkpoint 2.
Failure includes hiding unanimous items from audit or revealing votes before the human record.

#### 2.3 · Stop and final scenarios
A stable score below the quality floor must continue or HOLD rather than converge.
A passing project must freeze G*, label T* human-first, score seen and held-out executors with uplift, and invalidate T* if used for tuning.

#### 2.4 · Production scenario
An eligible executor must produce item-level route provenance, send known risk to the human, complete terminal dispositions, and run a final probability audit.
Failure includes k-NN label inheritance without validation, uncertainty becoming NONE, or calling the corpus reliable before audit.

### 3 · Reviewer independence and receipts
**Evaluation integrity**: creators and reviewers are distinct, and every failed run returns to the owning contract.

```text
creator artifact
      ↓
fresh reviewer
      ↓
pass | smallest fix + owning file
      ↓
new artifact version
      ↓
fresh review again
```

#### 3.1 · Process inspection
The reviewer checks which skill triggered, which references were loaded, which human gates appeared, which files were written, and why the run stopped.
A correct summary does not pass when the trace used retired authority.

#### 3.2 · Clean context
The reviewer receives only the user-style prompt, current skill path, and raw task artifacts.
It does not receive QA0 conclusions or the expected answer beyond normal skill discovery.

#### 3.3 · Completion receipt
The final receipt lists changed files, validation commands, Board finding counts, fresh-run prompts, verdicts, residual implementation HOLDs, and known risks.
QF5 closes only when every failed behavior is fixed and retested or explicitly held by scope.

## Aims

### A1 · 🧪 Static and structural checks
- A1.1 · Board, skills, links, contracts, and stale-authority searches pass.
  **Done when:** Commands and raw outputs are preserved in the migration receipt.

### A2 · 🤖 Fresh-context scenarios
- A2.1 · A new agent follows all five revised lifecycle scenarios and stops at the right gates.
  **Done when:** Process traces contain no retired semantic shortcut.

### A3 · 👁 Reviewer independence and receipts
- A3.1 · Skill creators do not approve their own behavior and every finding has an owning fix.
  **Done when:** Fresh reviews pass or named implementation HOLDs remain explicit.

## States

### A1 · 🧪 Static and structural checks
- ✅ A1.1 · All nine skill folders, agent frontmatter, stale-authority checks, and the 24-page Board pass their static gates.

### A2 · 🤖 Fresh-context scenarios
- ✅ A2.1 · Fresh reviewers passed all five scenarios; S5 found the D* ambiguity, and fresh S4/S5 reruns passed after the D_cal* repair.

### A3 · 👁 Reviewer independence and receipts
- ✅ A3.1 · Independent agent ids, raw prompts, process verdicts, repair ownership, and residual QF4 holds are preserved in the migration receipt.

## Files

### Checks · what proves this Page
- `Tools/plugins/haipipe-toolkit/skills/board/haipipe-board/cli/check.py`
  Runs deterministic Board checks.
- `/Users/jluo41/.codex/skills/.system/skill-creator/scripts/quick_validate.py`
  Validates skill naming and frontmatter when available.
- `../_source/QF5-validation-receipt-260806.md`
  Preserves static commands, raw fresh prompts, process verdicts, notation repair, and residual implementation holds.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [QF1 page](QF-execution-contract/QF1-skill-command-contract.md)
  QF1 supplies canonical routing and compatibility expectations.
- `reads · ALL` · [QF4 page](QF-execution-contract/QF4-library-mapping.md)
  QF4 supplies explicit implementation HOLDs that tests must not mistake for shipped engines.

## Law
- 260806 JL · 🧪 A revised skill is accepted only after a fresh agent follows the intended process and stops at the intended gates
      Static checks are necessary, while raw fresh-context behavior decides whether the migration actually works.

## Glossary
- 🤖 **Fresh-context run**: a realistic task executed by an agent that did not see the design discussion or intended answer.
- 👁 **Process review**: evaluation of triggered skills, tool sequence, artifacts, authority, and stopping behavior rather than final prose alone.
- 🧾 **Migration receipt**: the preserved evidence joining changed files, checks, behavioral runs, residual holds, and risks.

## Log
260806 · Created QF5 from the Board and skill-creator validation requirements.
260806 · Recorded successful quick validation for router, five canonical commands, and three compatibility aliases.
260806 · Accepted the documentation and skill migration after five fresh scenarios, one D_cal*/D* repair, and clean reruns; QF4 code remains deferred.
