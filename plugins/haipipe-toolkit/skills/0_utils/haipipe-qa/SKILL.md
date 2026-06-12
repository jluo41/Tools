---
name: haipipe-qa
description: "Structured QA walkthrough for data pipelines and code. Discovers issues, presents them one at a time, waits for user decision, then fixes. Use when the user says 'check this', 'QA', 'go through questions', 'double check', 'any issues?', or wants a systematic review of pipeline code or data."
metadata:
  version: "1.0.0"
  last_updated: "2026-06-12"
  summary: "One-issue-at-a-time QA walkthrough: discover, present, decide, fix, next."
  changelog:
    - "1.0.0 (2026-06-12): initial design from CC variable QA session."
---

# /haipipe-qa -- Structured QA Walkthrough

**Purpose**: systematically discover and resolve issues in pipeline code or data,
presenting ONE issue at a time so the user stays in control of each decision.

The anti-pattern this skill prevents: dumping 7 issues at once, the user gets lost,
fixes get tangled, and some issues are silently skipped. Instead: discover all,
present one, get a decision, apply, move to next.


## When to use

- User says: "check this", "QA", "double check", "any issues?", "go through it"
- After a build or refactor, before shipping to server
- When reviewing generated code or data quality
- When the user says "one by one"


## Two phases

```
Phase 1: DISCOVER       (read-only, no changes)
  Scan the target scope, collect ALL issues into a numbered list.
  Write the list to a QA_ISSUES.md file in the target folder.
  Show the user a summary: N issues found, severity breakdown.

Phase 2: WALKTHROUGH    (one issue at a time)
  For each issue in order:
    1. PRESENT  -- show the issue: what, where, why it matters
    2. WAIT     -- ask the user what to do (fix / skip / discuss)
    3. ACT      -- apply the decision
    4. CONFIRM  -- show the result, mark issue resolved
    5. NEXT     -- move to the next issue
```


## Issue format

Each issue in QA_ISSUES.md follows this structure:

```markdown
### Q{N}: {short title}

- **Severity**: BLOCKER | WARN | INFO
- **Where**: {file}:{line} (or {file} if file-level)
- **What**: {one sentence describing the problem}
- **Why it matters**: {one sentence on impact if not fixed}
- **Evidence**: {the specific code/data that shows the problem}
- **Suggested fix**: {concrete action}
- **Status**: OPEN | FIXED | SKIPPED | DISCUSSED
```


## Discovery checklist (fn/discover.md)

The discover phase runs checks organized by category. Not all categories
apply to every target -- skip categories that don't match the scope.

```
Category              Checks                                   Applies to
--------------------  ---------------------------------------- ----------
A. Naming parity      variable names match across stages        data/reg
B. Config consistency  globals match between configs             all
C. Data types          flag vs date vs continuous                data
D. Binarization        CC codes 0-3 vs 0/1 vs dates             data
E. Variable coverage   expected vars exist in output             data/reg
F. Encoding            ASCII-only, no BOM, no PS7 syntax         all
G. Path portability    ws_root anchored, no hardcoded paths      all
H. SSC/dependency      no blocked SSC, rangejoin guarded         all
I. STATATMP            set before preserve/tempfile              all
J. Source parity       synth vs full configs aligned              data
K. Row plausibility    N > 0 after each filter step              data
L. Merge completeness  no all-missing columns after merge        data
M. Outcome variance    DV has non-zero variance                  reg
N. Control consistency BENE_CONDITION same across all scripts    reg
```


## Walkthrough protocol (fn/walkthrough.md)

### Presenting an issue

```
## Q{N} of {TOTAL}: {title}  [{severity}]

**Where:** `{file}:{line}`

**Problem:** {clear explanation}

**Evidence:**
{code snippet or data showing the problem}

**Impact:** {what goes wrong if not fixed}

**Suggested fix:** {concrete action}

What do you want to do?
- Fix it now
- Skip (accept the risk)
- Discuss (need more context)
```

### Rules

1. Present exactly ONE issue per turn
2. WAIT for user response before moving to next
3. If user says "fix" -- apply the fix, show what changed, then present next
4. If user says "skip" -- mark SKIPPED in QA_ISSUES.md, present next
5. If user says "discuss" -- explain deeper, re-ask
6. After the last issue: show the final summary (N fixed, N skipped, N discussed)
7. If user says "fix all" or "just fix everything" -- batch-apply all remaining fixes


## Invocation

```
/haipipe-qa <target-path>                    full QA (discover + walkthrough)
/haipipe-qa discover <target-path>           discover only (write QA_ISSUES.md)
/haipipe-qa walkthrough <target-path>        resume walkthrough on existing QA_ISSUES.md
/haipipe-qa check <specific-check> <path>    run one check category (e.g. "naming", "encoding")
```

Target path can be:
- A task folder (e.g. `C01_data_pipeline_opioid`)
- A task group (e.g. `R01_Reg_TraitOpioid`) -- scans all D-series inside
- A specific file (e.g. `scripts/full-variables.do`) -- focused checks only


## Return contract

```yaml
status: ok | issues_found | blocked
qa_file: QA_ISSUES.md
total_issues: N
fixed: N
skipped: N
open: N
next: "<what to do next>"
```


## Design rationale

This skill was born from a real session where we discovered 7 interleaved issues
(CC naming, `_ever` dates, config duplication, stale comments, binarization bugs,
runner naming, synth-vs-real divergence) and the user got lost tracking them all.

Key insight: **the user should never have to hold more than one issue in their head.**
The skill's job is to be the queue -- discover everything upfront, then drip-feed
one decision at a time.
