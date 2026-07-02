---
name: haipipe-paper-section-edit-values
description: "values gather worker for section-edit. One skill, one working doc (_VALUES_), full lifecycle: AUDIT (identify every number) → TRACE (link to source) → CANDIDATE (write entries) → PLACE (auto-place source-verified values, flag uncertain for CHECK) → REVIEW (pre-submission re-derivation walk). Fully automatic -- no human gate. Human review happens in CHECK phase only. Hard boundary: agent NEVER fabricates a number. The parquet/script decides, not the prose. Trigger: values, numbers, check numbers, numeric consistency, reconcile values, verify stats, manual review values."
argument-hint: "[verb] [section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
metadata:
  version: "1.0.0"
  last_updated: "2026-07-02"
  summary: "Unified values gather worker. AUDIT→TRACE→CANDIDATE→PLACE→REVIEW lifecycle (fully automatic, no human gate). Human review happens in CHECK only. Single working doc = _VALUES_. Absorbs manual-review-values."
  changelog:
    - "1.0.0 (2026-07-02): merged manual-review-values (pre-submission number walk) into one skill with 6 phases. Defined hard boundaries. Defined _VALUES_ format."
    - "0.0.1 (2026-06-29): stub with scope only."
  predecessors:
    - "haipipe-paper-section-edit-values (pre-submission number-by-number walk) — MERGED as Phase 5"
---

Skill: haipipe-paper-section-edit-values
========================================

values gather worker for `haipipe-paper-section-edit`. One skill owns the full values lifecycle for one section, from number identification through pre-submission re-derivation. The single working document is `_VALUES_N-section.md`.

```
/haipipe-paper-section-edit-values                       → status dashboard
/haipipe-paper-section-edit-values audit <section>       → Phase 1: identify every number
/haipipe-paper-section-edit-values trace <section>       → Phase 2-3: link to sources, write entries
/haipipe-paper-section-edit-values place <section>       → Phase 4: auto-place verified, flag uncertain for CHECK
/haipipe-paper-section-edit-values review <section>      → Phase 5: pre-submission re-derivation walk
```

## Hard Boundaries

1. **NEVER fabricate a number.** Every number in tex must trace to a source (task output, regression log, display CSV, or external reference). The agent never invents, rounds, or interpolates values.

2. **Auto-place only source-verified values.** During PLACE, the agent reads the source file (CSV, log, parquet output) and compares. If the number matches the source at displayed precision, the agent places it (status ✅). If the source is missing, ambiguous, or the number does not match, the agent flags it 🔍 or ⚠️ for CHECK. The human confirms flagged values during CHECK.

3. **The parquet/script decides, not the prose.** When the prose says one number and the data source says another, the data source wins. Never pick the majority across sections.

4. **NEVER trust cached outputs alone.** Re-run the analysis script or read the actual data file. A CSV checked into the repo may predate the canonical data.


## Five Phases (fully automatic)

```
Phase 1: AUDIT        identify every number in the section
Phase 2: TRACE        link each number to its source (task output, display CSV, script)
Phase 3: CANDIDATE    write entries to _VALUES_ with source + status
Phase 4: PLACE        auto-place source-verified values; flag uncertain for CHECK
Phase 5: REVIEW       pre-submission re-derivation walk (from manual-review-values)
```

All five phases run automatically without stopping for human input. The agent traces numbers to source files, verifies what it can, and flags the rest for CHECK. Human review happens ONLY in the CHECK phase (haipipe-paper-section-edit-checker). During CHECK, the human confirms flagged numbers against source, adds `> JL:` comments, and decides. If CHECK restarts GATHER, the agent reads those `> JL:` comments and responds.


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


## Phase 4: PLACE (automatic)

The agent auto-places values it can verify against source files and flags the rest for CHECK.

1. **For each entry in _VALUES_,** read the source file and compare the number at displayed precision.

2. **If the source confirms the value** (exact match or rounding-correct):
   - Update status: ⬜ → ✅
   - Confirm the number is correctly woven into tex prose
   - Sync outline if needed

3. **If the source contradicts the value** (⚠️ mismatch):
   - Update status: ⬜ → ⚠️
   - Record the discrepancy in _VALUES_ (prose says X, source says Y)
   - Flag for CHECK (the human decides which is correct)

4. **If the source is missing or ambiguous** (🔍):
   - Update status: ⬜ → 🔍
   - Record what was searched and not found
   - Flag for CHECK (the human locates the source)

5. **For ❌ method claims** with no code implementation:
   - Flag for CHECK (the human confirms or drops the claim)

6. Update _VALUES_ statuses and continue. No blocking.


## Phase 5: REVIEW (pre-submission)

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

Extract numbers embedded in figures via `pdftotext -layout` or visual read. Cross-check against body text. For closed-format figure sources (`.pptx`, `.key`, `.ai`): flag for human action, never edit directly.

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
- [ ] All entries traced to a source (or flagged 🔍 for CHECK)
- [ ] Source-verified values auto-placed in tex (✅)
- [ ] Mismatches (⚠️) and unknowns (🔍) flagged for CHECK (not blocking)
- [ ] All method claims checked against code (or flagged ❌ for CHECK)
- [ ] _LOG updated with values gather summary


## Anti-patterns

- ❌ "All sections agree, so it's correct." (The parquet decides.)
- ❌ Batching fixes
- ❌ Trusting cached outputs without re-running
- ❌ Fabricating a number to fill a gap
- ❌ Skipping figure-embedded numbers
- ❌ "The method claim is standard, no need to grep."
