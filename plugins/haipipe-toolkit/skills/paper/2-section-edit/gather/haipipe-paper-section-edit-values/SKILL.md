---
name: haipipe-paper-section-edit-values
description: "values gather worker for section-edit. One skill, one working doc (_VALUES_), full lifecycle: AUDIT (identify every number) → TRACE (link to source) → CANDIDATE (write unverified entries) → [HUMAN GATE] → PLACE (verified → weave into tex) → REVIEW (pre-submission re-derivation walk). Merges former manual-review-values. Hard boundary: agent NEVER fabricates a number, NEVER places an unverified value in tex. The parquet/script decides, not the prose. Trigger: values, numbers, check numbers, numeric consistency, reconcile values, verify stats, manual review values."
argument-hint: "[verb] [section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
metadata:
  version: "1.0.0"
  last_updated: "2026-07-02"
  summary: "Unified values gather worker. AUDIT→TRACE→CANDIDATE→[HUMAN]→PLACE→REVIEW lifecycle. Single working doc = _VALUES_. Absorbs manual-review-values."
  changelog:
    - "1.0.0 (2026-07-02): merged manual-review-values (pre-submission number walk) into one skill with 6 phases. Defined hard boundaries. Defined _VALUES_ format."
    - "0.0.1 (2026-06-29): stub with scope only."
  predecessors:
    - "haipipe-paper-section-edit-values (pre-submission number-by-number walk) — MERGED as Phase 6"
---

Skill: haipipe-paper-section-edit-values
========================================

values gather worker for `haipipe-paper-section-edit`. One skill owns the
full values lifecycle for one section, from number identification through
pre-submission re-derivation. The single working document is
`_VALUES_N-section.md`.

```
/haipipe-paper-section-edit-values                       → status dashboard
/haipipe-paper-section-edit-values audit <section>       → Phase 1: identify every number
/haipipe-paper-section-edit-values trace <section>       → Phase 2-3: link to sources, write candidates
/haipipe-paper-section-edit-values place <section>       → Phase 5: verified values → weave into tex
/haipipe-paper-section-edit-values review <section>      → Phase 6: pre-submission re-derivation walk
```

## Hard Boundaries

1. **NEVER fabricate a number.** Every number in tex must trace to a source
   (task output, regression log, display CSV, or external reference). The
   agent never invents, rounds, or interpolates values.

2. **NEVER place an unverified value in tex.** A value is "verified" when the
   human marks it `✅ verified` in the values map AND the source is confirmed.
   Until both hold, the agent must not weave the number into prose.

3. **The parquet/script decides, not the prose.** When the prose says one number
   and the data source says another, the data source wins. Never pick the
   majority across sections.

4. **NEVER trust cached outputs alone.** Re-run the analysis script or read
   the actual data file. A CSV checked into the repo may predate the canonical
   data.


## Six Phases

```
Phase 1: AUDIT        identify every number in the section
Phase 2: TRACE        link each number to its source (task output, display CSV, script)
Phase 3: CANDIDATE    write unverified entries to _VALUES_
═══════════════════   HUMAN GATE ═══════════════════════════════════════════
Phase 4: (human)      user confirms each number against source, marks ✅ verified
Phase 5: PLACE        verified values → weave into tex prose + sync outline
Phase 6: REVIEW       pre-submission re-derivation walk (from manual-review-values)
```


## Phase 1: AUDIT

Scan the section's tex file and extract every quantitative claim:

- Sample sizes (N = X)
- Rates, percentages, proportions
- Regression coefficients, AMEs, odds ratios
- p-values, confidence intervals, standard errors
- Percentage-point deltas and comparisons
- Date ranges, time periods
- Method claims ("Holm-Bonferroni corrected", "cluster-robust SEs")

For each, record:
```
P#.S# | exact phrase | number(s) | claim type | expected source
```

Skip `%%` comment lines. Do NOT skip table/figure captions.


## Phase 2: TRACE

For each number from Phase 1, identify the canonical source:

| Source type | Where to look |
|---|---|
| Display output | `0-displays/displayNN/results/<run>/*.csv` |
| Task output | `tasks/<task>/results/<run>/` |
| Regression log | Stata `.log` files, Python script output |
| External reference | Cited paper (cross-ref with _CITATION_) |
| Computed inline | Derived from other values (document the arithmetic) |

For method claims, grep the codebase:
```bash
grep -rni "<method keyword>" tasks/ code/
```


## Phase 3: CANDIDATE → _VALUES_

Write entries to `_VALUES_N-section.md`.

### Entry format

```markdown
### P#.S# -- "exact phrase from tex"

- **Value:** the number(s)
- **Type:** sample_size / rate / coefficient / p_value / delta / method_claim
- **Source:** path/to/source/file or "derived: X - Y = Z"
- **Status:** ⬜ unverified | ✅ verified | ⚠️ mismatch | 🔍 source unknown
- **Note:** any context needed for verification
```

### Status legend

```
✅ = verified against source (user confirmed)
⬜ = identified but not yet verified
⚠️ = mismatch between prose and source
🔍 = source file not found, needs investigation
❌ = method claim with no code implementation
```


## Phase 4: HUMAN GATE (agent does not execute this)

The human:
1. Reads each entry in _VALUES_
2. Checks the source file or re-runs the script
3. Marks verified entries as `✅ verified`
4. Flags mismatches with `> JL:` comments


## Phase 5: PLACE

After human verification:

1. For ⚠️ mismatch entries: update the prose number to match the source
2. For ✅ verified entries: confirm the number is correctly woven into tex
3. For ❌ method claims: drop the claim or correct it per user decision
4. Sync outline if any numbers changed
5. Update _VALUES_ statuses


## Phase 6: REVIEW (pre-submission)

The slow, paranoid, human-paced re-derivation pass. For each number:

1. **Re-derive** from raw data (parquet, CSV, script output)
2. **Compare** at displayed precision
3. **Cross-check** against other sections making the same claim
4. **Classify** status and show the user a 4-line summary:
   ```
   P#.S# line NN: "...69.8% CTR, a 6.5% improvement..."
     paper:    69.8%, +6.5 pp
     data:     69.77%, delta = 6.47 pp
     status:   arithmetic_error
     fix:      change "6.5%" → "6.5%"
   ```
5. **Wait** for explicit user approval before any edit

### Method-claim audit

For every method claim, grep the codebase:
- `unsupported_method_claim` -- paper claims X but code doesn't implement X
- `wrong_method_claim` -- paper claims X but code implements Y

### Figure audit

Extract numbers embedded in figures via `pdftotext -layout` or visual read.
Cross-check against body text. For closed-format figure sources (`.pptx`,
`.key`, `.ai`): flag for human action, never edit directly.

### Verification recipes

| Claim type | Recipe |
|---|---|
| Sample size | `len(df[filter])` from parquet |
| Rate | `groupby().agg()` from parquet |
| Delta | Re-derive subtraction from raw rates (never trust claimed delta) |
| Coefficient/AME | Re-run analysis script pipeline |
| p-value | Re-derive from same regression |
| Method claim | `grep -rni` the codebase |

### Status taxonomy

- `exact_match` -- paper and evidence match at displayed precision
- `rounding_ok` / `rounding_drift` -- rounds correctly / wrong direction
- `arithmetic_error` -- individual numbers correct but stated arithmetic wrong
- `number_mismatch` -- paper value disagrees with evidence
- `unit_error` -- value correct but wrong unit (% vs pp)
- `stale_snapshot` -- matches older data, not canonical
- `unsupported_method_claim` / `wrong_method_claim`
- `config_mismatch` -- value from different sample/filter than claimed
- `figure_drift_from_body` -- figure embeds a corrected number
- `unverifiable` -- no script or data source available

**One claim at a time. One approval per fix. No batching.**


## _VALUES_ file organization

```markdown
# §N Section-Name: Values Registry

Total values: K identified, M verified, J unverified, L mismatches

---

## P1. Paragraph headline

### P1.S2 -- "exact phrase"
[entry as defined above]

---

## Open items
- [unverified values, source-unknown entries, method claims to check]
```


## Relation to sibling skills

```
gather/
  haipipe-paper-section-edit-citation     citation  _CITATION_.md
  haipipe-paper-section-edit-values       ← THIS (values, _VALUES_.md)
  haipipe-paper-section-edit-display      display  0-displays/ units
```


## Done criteria

- [ ] All numbers identified in _VALUES_
- [ ] All entries traced to a source
- [ ] No ⚠️ or 🔍 entries remaining
- [ ] All method claims verified against code
- [ ] _LOG updated with values gather summary


## Anti-patterns

- ❌ "All sections agree, so it's correct." (The parquet decides.)
- ❌ Batching fixes
- ❌ Trusting cached outputs without re-running
- ❌ Fabricating a number to fill a gap
- ❌ Skipping figure-embedded numbers
- ❌ "The method claim is standard, no need to grep."
