---
name: haipipe-probe-review
description: "QA specialist of haipipe-probe. Three complementary checks. (1) STRUCTURAL: audits run quality (per-run sanity) and probe quality (statistical claim integrity) via checklists, produces ✅/⚠️/❌ + actionable issues. (2) INTEGRITY: Codex MCP fraud-pattern audit (ground-truth provenance, metric-definition consistency, phantom results, scope-language mismatch, individual/split leakage), writes INTEGRITY_AUDIT.md. (3) SEMANTIC: Codex MCP judges whether evidence supports the intended claim (yes/partial/no + confidence), writes CLAIMS_FROM_RESULTS.md. The honest-science gate before a claim becomes a paper-able statement. Trigger: review, audit, qa, integrity, fraud check, fake ground truth, phantom results, scope check, claim verdict, supports?, /haipipe-probe-review."
argument-hint: "[run|probe|claim|project] [target]"
allowed-tools: Bash, Read, Write, Grep, Glob, Skill, mcp__codex__codex, mcp__codex__codex-reply
metadata:
  version: "1.2.0"
  last_updated: "2026-06-01"
  summary: "QA specialist of haipipe-probe."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-06-01): update probe artifact paths for lightweight `MM-NN_slug` layout."
    - "1.2.0 (2026-06-01): switch probe folder + ref examples to date-based `MMDD` / `P.MMDD`."
---

Skill: haipipe-probe-review
=================================

The **scientific-honesty gate**. Before a claim leaves a probe
yaml and enters a paper / dashboard / decision, this skill audits:

  - Per-probe quality (is the comparison apples-to-apples?)
  - Honesty (is the setup free of fraud patterns?)
  - Claim support (do the results mean what we say?)

(Per-RUN quality moved to C_task `run-result-auditor-agent` — `review run`
delegates to it; see Commands below.)

**Agent embodiment (builder ≠ judge).** The three checks below ARE three
independent D_probe reviewer agents — dispatch them as `subagent_type` (e.g.
from `haipipe-probe-loop` or a `G_application` session) for an out-of-family
verdict, or run their logic inline here:

```
review probe     → probe-structural-reviewer-agent   (review.md)
review integrity → probe-integrity-auditor-agent      (INTEGRITY_AUDIT.md, Codex)
review claim     → claim-verifier-agent               (CLAIMS_FROM_RESULTS.md, Codex)
```

This skill remains the canonical home for the checklists + Codex prompts; the
agents are thin pointers to it (`skills/D_probe/agents/`).


Commands
--------

```
/haipipe-probe review run <run-path>
  STRUCTURAL: per-run trustworthiness. DELEGATES to the C_task agent
  run-result-auditor-agent — read skills/C_task/agents/reviewers/run-result-auditor-agent.md
  and dispatch its body to a Task subagent over <run-path>. Per-run
  quality is a C_task judgment; D_probe only consumes the verdict.

/haipipe-probe review probe <probe>
  STRUCTURAL: audit ONE probe against the per-probe checklist.

/haipipe-probe review integrity <probe>
  INTEGRITY: Codex MCP reads eval scripts / configs / results / claims
  and judges 5 fraud patterns (A. GT provenance / B. metric consistency /
  C. phantom results / D. scope mismatch / E. individual leakage).
  Writes INTEGRITY_AUDIT.md sidecar.

/haipipe-probe review claim <probe>
  SEMANTIC: Codex judges whether evidence supports the claim.
  Auto-runs integrity first if no recent audit. Writes CLAIMS_FROM_RESULTS.md
  for downstream consumption (e.g. /haipipe-paper-structure-narrative).

/haipipe-probe review project [project-path]
  STRUCTURAL: audit ALL probes + all referenced runs in a project.
  Output ranked by severity.
```


Per-run checklist — MOVED to C_task
------------------------------------

The per-run sanity checklist (runtime.status, exit_code, git_sha,
metrics.json parseable, heavy-artifact placement, ...) now lives with the
agent that owns it: **`skills/C_task/agents/reviewers/run-result-auditor-agent.md`**
(GATE 2). "Did THIS run produce a trustworthy artifact?" is a C_task
question, not a D_probe one.

`review run` above delegates to that agent. The per-probe checklist below
consumes its verdict (see "all linked runs pass run-result-auditor-agent").
D_probe does NOT re-implement the per-run list — single source of truth.


Per-probe checklist
-------------------------

```
□ all arms have ≥ 1 linked run
□ paired arms have equal N runs (warn if unequal)
□ N ≥ 3 for statistical claim (else mark claim as "exploratory")
□ all linked runs pass run-result-auditor-agent (GATE 2, C_task)
□ all linked runs share same git_sha (within arm AND across arms)
□ all linked runs share same AIData version (read from configs)
□ same training schedule across arms (only the intended difference varies)
□ outlier seed handling: if 1 seed dominates t-test, both raw +
  outlier-excluded numbers reported
□ caveats: list covers all detectable confounds (run checklist below)
□ baseline arm exists (no claim without control)
□ if result.status == confirmed: p < 0.05 AND |Δ| > noise floor
```


Caveats auto-detection (run before approving probe)
---------------------------------------------------------

```
⚠️ Single seed?                            → flag noise floor uncertainty
⚠️ Compared against different framework?    → flag apples-to-oranges
⚠️ Different hyperparameter tuning?         → flag confound
⚠️ Different params count by >2x?           → flag scale confound
⚠️ Data parser bug history?                 → flag the fix
⚠️ Outlier seed?                            → note + show outlier-excluded analysis
⚠️ Loss differs from comparison group?      → flag objective confound
⚠️ Filter / split definition changed?       → flag dataset confound
```

Each YES → must appear in the probe's `caveats:` list, OR the
review fails with a "missing caveat" issue.


Integrity audit — fraud-pattern check via Codex MCP
----------------------------------------------------

`review integrity <probe>` is a SEPARATE Codex check from claim verdict:

```
integrity      "is the experimental setup honest?"
claim verdict  "do the honest results support the intended claim?"
```

Integrity is the earlier gate — fraud invalidates any downstream verdict.
Adapted from research-toolkit's `probe-audit`, specialized for our
CGM / ML-research domain.

### Role separation (CRITICAL)

```
Executor (Claude, this skill)  →  collects file paths ONLY
                                   does NOT read or summarize content
Reviewer (Codex via MCP)       →  reads files directly
                                   judges each category independently
```

Prevents the executor — who built the probe — from rationalizing
its own work. Reviewer sees raw files; executor sees only paths.


### Fraud categories (5)

| Cat | Pattern                            | Domain example                                                                       |
|-----|------------------------------------|--------------------------------------------------------------------------------------|
| A   | Ground-truth provenance            | CGM 2h forecast: GT must be future bins from raw CGM, NOT model output               |
| B   | Metric-definition consistency      | "MAE" silently shifts horizon (288:312 vs 552:575) across arms — the B92/A41 gap     |
| C   | Phantom results                    | claim references metrics.json key/number that doesn't exist or doesn't match         |
| D   | Scope-language mismatch            | "comprehensive across conditions" with N=1 seed → FAIL                               |
| E   | Individual/split leakage              | same patient_id appears in train AND test split (cross-individual claim broken)         |

A / C / D adapted from `probe-audit`; B / E added for CGM-domain
realities (per [[project_b92_eval_position_mismatch]] and per-individual
splitting requirements).


### Codex prompt (review integrity)

```
mcp__codex__codex:
  config: {"model_reasoning_effort": "xhigh"}
  sandbox: read-only
  cwd: <project root>
  prompt: |
    PROBE INTEGRITY AUDIT

    Read the files below and check 5 fraud patterns.

    Files (paths only — you read content yourself):
      eval scripts:   [tasks/.../*eval*.py and metric defs]
      configs:        [configs/<NAME>.yaml for every linked run]
      results:        [results/<NAME>/metrics.json for every linked run]
      runtime:        [results/<NAME>/runtime.yaml for every linked run]
      probe:     [probes/<MMDD>_<slug>/probe.yaml]
      claim refs:     [CLAIMS_FROM_RESULTS.md, paper/*.tex if present]

    Categories:
      A. Ground-truth provenance       — is GT from dataset or model output?
      B. Metric-definition consistency — same metric key, horizon, exclusion across arms?
      C. Phantom results               — referenced file / key / number actually exists?
      D. Scope-language mismatch       — claim wording vs N seeds, N datasets
      E. Individual/split leakage         — patient_id leak across splits?

    For each category report:
      status:    PASS | WARN | FAIL
      evidence:  exact file:line references
      details:   one paragraph

    Overall verdict: PASS | WARN | FAIL.
    Be thorough. Read every eval script and config.
```


### Output: INTEGRITY_AUDIT.md

Sidecar file in the probe folder:

```
probes/<MMDD>_<slug>/INTEGRITY_AUDIT.md
```

Schema:

```markdown
# INTEGRITY AUDIT — P.0601

- overall_verdict:  pass | warn | fail
- audited_at:       <ISO timestamp>
- auditor:          codex-xhigh

## A. Ground-truth provenance: PASS|WARN|FAIL
[evidence file:line + details]

## B. Metric-definition consistency: ...
## C. Phantom results: ...
## D. Scope-language mismatch: ...
## E. Individual/split leakage: ...

## Action items
- [specific fix per non-PASS category]
```

`overall_verdict` is also mirrored into `CLAIMS_FROM_RESULTS.md`
`integrity_status:` field whenever claim verdict is run.


### Gating: integrity → claim verdict

```
integrity = fail  →  claim verdict REFUSES to run; user must fix first
integrity = warn  →  claim verdict runs but confidence auto-capped at
                     ≤ medium; findings copied into "Known caveats:" of
                     the claim prompt
integrity = pass  →  claim verdict runs normally
```

If `/review claim <probe>` is invoked without a recent INTEGRITY_AUDIT.md
(< 24h old, same git_sha), this skill auto-runs integrity first in the
same session before claim verdict.


### Integrity vs caveats — distinct concepts

```
caveats     experimenter-declared confounds (param-count diff, etc.)
            → live in probe.yaml caveats: list
            → ACCEPTABLE if declared and qualifying the claim

integrity   reviewer-detected fraud patterns (fake GT, leakage, etc.)
            → live in INTEGRITY_AUDIT.md
            → NOT acceptable; invalidate the setup until fixed
```


Claim verdict — semantic judgment via Codex MCP
------------------------------------------------

The `review claim <probe>` mode delegates the value-judgment to an external
LLM. Structural checklists catch "is the comparison apples-to-apples?";
this catches "does the data actually mean what we say it means?". They
are complementary — run both before any submission claim.

### Why Codex, not Claude

This skill collects evidence and routes; Codex evaluates. Claude
implemented the probes and naturally rationalizes its own work;
an out-of-family reviewer doesn't. This is the same reviewer-independence
principle the auto-review-loop uses.

### Codex prompt (Step 2 of result-to-claim)

```
mcp__codex__codex:
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    RESULT-TO-CLAIM EVALUATION

    Judge whether experimental results support the intended claim.

    Intended claim: [the claim these probes test]
    Probes run: [list with method, dataset, metrics]
    Results: [paste key numbers, comparison deltas, significance]
    Baselines: [baseline numbers and sources — reproduced or from paper]
    Known caveats: [confounding factors, limited datasets, missing comparisons]

    Evaluate:
    1. claim_supported: yes | partial | no
    2. what_results_support: what the data actually shows
    3. what_results_dont_support: where the data falls short of the claim
    4. missing_evidence: specific evidence gaps
    5. suggested_claim_revision: strengthen / weaken / reframe
    6. next_probes_needed: specific probes to fill gaps
    7. confidence: high | medium | low

    Be honest. Do not inflate claims beyond what the data supports.
    A single positive result on one dataset does not support a general claim.
```

### Verdict integration with structural review

If `review probe <probe>` (structural) was run first, its issues feed
the Codex prompt as `Known caveats:`. If the structural review found
`error`-severity issues, the semantic verdict's confidence is
auto-downgraded to `low` regardless of Codex's own confidence.

### Routing by verdict

```
yes      → claim supported. If ablations incomplete → suggest
           /haipipe-probe explore propose <probe>. Else ready for paper.
partial  → update claim to reflect what IS supported. Suggest supplementary
           probes (via /haipipe-probe explore propose). Multiple
           rounds of partial on the same claim → consider narrowing scope.
no       → record postmortem in findings.md. Decide whether to pivot
           (next IDEA_REPORT entry) or try an alternative approach.
```

### Output: CLAIMS_FROM_RESULTS.md

Written at project root (or wherever the probe lives). Schema:

```markdown
# CLAIMS_FROM_RESULTS

## Claim: <one-sentence claim>

- claim_supported: yes | partial | no
- confidence:      high | medium | low
- integrity_status: pass | warn | fail | unavailable
- what_results_support: ...
- what_results_dont_support: ...
- missing_evidence: ...
- suggested_claim_revision: ...
- next_probes_needed: ...
- raw_evidence_files: [paths to results/*.json or metrics.json]
- reviewed_by: codex-<reasoning-effort>, <timestamp>
```

Downstream `/haipipe-paper-structure-narrative` reads this as the spine of its
claim ↔ evidence matrix.


Output format
--------------

```
═══ Probe P.0601 review ═══
Status: ⚠️ 2 warnings, 0 errors

✅ Arms paired (N=3 each)
✅ Same AIData v3, same training schedule
✅ git_sha consistent (e2d67d63 across all 6 runs)
⚠️ LHM-A has 1.2× params vs baseline — scale confound NOT in caveats
⚠️ One seed (lhm_seed7) shows MAE 22.1 vs others 24.0; outlier-excluded
   analysis missing

Recommended actions:
  1. Add caveat: "LHM-A has 1.2× params — partial scale confound"
  2. Add outlier-excluded result: aggregate without lhm_seed7
  3. Mark result.status as "confirmed-pending-caveats" until fixed

═══ Linked runs (6) ═══
  ✅ run_seed42_baseline    pass
  ✅ run_seed7_baseline     pass
  ✅ run_seed13_baseline    pass
  ✅ run_seed42_lhm         pass
  ⚠️ run_seed7_lhm          outlier; needs documentation
  ✅ run_seed13_lhm         pass
```


Severity levels
----------------

```
❌ error    blocks any claim — must fix
⚠️ warning  weakens claim — should fix, must document if not
🔵 info     observation — no action required
```


Risk profile
-------------

- `review run|probe|project` (structural): READ-ONLY. Produces a
  report (stdout or `--out <path>`).
- `review integrity` (Codex fraud audit): WRITES `INTEGRITY_AUDIT.md`
  in the probe folder. Calls `mcp__codex__codex` (external LLM,
  read-only sandbox). Does not modify probe yaml or run artifacts.
- `review claim` (semantic): WRITES `CLAIMS_FROM_RESULTS.md` at the
  project root. Calls `mcp__codex__codex` (external LLM). May auto-invoke
  `review integrity` as a preceding step. Does not modify probe
  yaml or run artifacts.


Disambiguation
---------------

  - No verb (just <probe>) → default to `probe` (structural) review.
  - "integrity" / "audit" / "fraud" / "honesty" + ID → integrity audit via Codex.
  - "claim" / "verdict" / "supports?" + ID → semantic verdict via Codex
    (auto-runs integrity first if no recent audit).
  - "claim" or "integrity" alone (no ID) → ASK which probe.
  - No target at all → default to `project` review on cwd.
  - run-path that isn't a run → bail with helpful message.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "P.0601 review: 0 errors, 2 warnings, recommended actions: 3"
          OR "P.0601 integrity audit: WARN (B metric-definition inconsistent)"
          OR "P.0601 claim verdict: partial (confidence: medium)"
artifacts: [report stdout / --out path / INTEGRITY_AUDIT.md / CLAIMS_FROM_RESULTS.md]
next:      apply suggested actions then /result aggregate <probe> again
          OR if integrity WARN/FAIL: fix flagged categories then /review integrity <probe>
          OR if claim verdict was partial/no: /haipipe-probe explore propose <probe>
```
