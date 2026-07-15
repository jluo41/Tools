---
name: haipipe-paper-probe-values
description: "values HARVESTER (probe lane worker) for section-edit. One skill, one working doc (_VALUES_). Lifecycle: AUDIT (identify every number) → ROUTE (unsourced numbers → a new question SECTION in 1-probes/) → CANDIDATE (harvest the section's values:/target: QA file, reads ONLY named paths) → PLACE (auto-place source-verified values, flag uncertain for CHECK) → REVIEW (re-derivation walk). Fully automatic. Hard boundary: NEVER fabricates a number -- the parquet/script decides, not the prose. Trigger: values, numbers, check numbers, numeric consistency, reconcile values, verify stats, manual review values."
argument-hint: "[verb] [section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "3.1.0"
  last_updated: "2026-07-14"
  summary: "values HARVESTER (probe lane worker): AUDIT (every number) → ROUTE (unsourced → a question SECTION, after a paper-local sweep of the paper's OWN registries -- adopt the pointer, never the verdict) → CANDIDATE (harvest the named QA file, pointer-following only; never greps tasks/ to DISCOVER a source -- the executor finds, this worker follows) → PLACE → REVIEW. HARVEST reads the target QA file's state line first and REFUSES a `working` or `superseded` (or state-less) target. Read-only: NEVER writes a QA file. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  predecessors:
    - "haipipe-paper-manual-review-values (pre-submission number-by-number walk) — MERGED here as Phase 5"
---

Skill: haipipe-paper-probe-values
========================================

values probe worker for `haipipe-paper-section-edit`. One skill owns the full values lifecycle for one section, from number identification through pre-submission re-derivation. The single working document is `_VALUES_N-section.md`.

```
/haipipe-paper-probe-values                       → status dashboard
/haipipe-paper-probe-values audit <section>       → Phase 1: identify every number
/haipipe-paper-probe-values route <section>       → Phase 2: match to named sources, raise gaps as question SECTIONS
/haipipe-paper-probe-values harvest <stage> <qa_file> → Phase 3: expand the QA file's value anchors → _VALUES_ entries
/haipipe-paper-probe-values place <section>       → Phase 4: auto-place verified, flag uncertain for CHECK
/haipipe-paper-probe-values review <section>      → Phase 5: pre-submission re-derivation walk
```

## Hard Boundaries

1. **NEVER fabricate a number.** Every number in tex must trace to a source (task output, regression log, display CSV, or external reference). The agent never invents, rounds, or interpolates values.

2. **Auto-place only source-verified values.** During PLACE, the agent reads the source file (CSV, log, parquet output) and compares. If the number matches the source at displayed precision, the agent places it (status ✅). If the source is missing, ambiguous, or the number does not match, the agent flags it 🔍 or ⚠️ for CHECK. The human confirms flagged values during CHECK.

3. **The parquet/script decides, not the prose.** When the prose says one number and the data source says another, the data source wins. Never pick the majority across sections.

4. **NEVER trust cached outputs alone.** Re-run the analysis script or read the actual data file. A CSV checked into the repo may predate the canonical data.


## Five Phases (fully automatic)

```
Phase 1: AUDIT        identify every number in the section
Phase 2: ROUTE        match numbers to ALREADY-NAMED sources (a probe section's
                      values:/target:, the _DISPLAY_ registry, _CITATION_); anything
                      unmatched → a question SECTION for the hub (NO bank-grepping)
Phase 3: CANDIDATE    harvest: expand the section's values: lane / target: QA file
                      into _VALUES_ entries (pointer-following — read ONLY named paths)
Phase 4: PLACE        auto-place source-verified values; flag uncertain for CHECK
Phase 5: REVIEW       pre-submission re-derivation walk (from manual-review-values)
```

All five phases run automatically without stopping for human input. The agent traces numbers to source files, verifies what it can, and flags the rest for CHECK. Human review happens ONLY in the CHECK phase (haipipe-paper-check). During CHECK, the human confirms flagged numbers against source, adds `> USER:` comments, and decides. If CHECK restarts PROBE, the agent reads those `> USER:` comments and responds.


## Phase 1: AUDIT

Scan the section's WORKING .md (every `{VAL:? <what>}` slot AND every literal number in the prose); tex only when it exists post-sync. Extract every quantitative claim:

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


## Phase 2: ROUTE (trace-as-grep is RETIRED — JL 2026-07-07 harvester ruling)

Pointer-following only: this worker may READ a path that is already NAMED
somewhere (a probe section's `values:` lane or `target:` QA file, a `_DISPLAY_`
registry row, a `_CITATION_` entry, an explicit path in a tex comment). It may NOT grep
`tasks/`/`code/` to DISCOVER which task holds a number — "which task has this
number" is an evidence question, answered by the EXECUTOR in its own clean
context (index-first discipline lives there, not here).

EXEMPT from that ban (JL 2026-07-10): the paper's OWN registries. Sweeping the
closed whitelist below is pointer-following over indexes the lifecycle itself
curated — the paper deposits verified pointers all through DPRC, and PROBE
checks its own shelves before paying for a dispatch.

For each Phase-1 number:

| Situation | Action |
|---|---|
| A named source covers it (a probe section's values:/target: / a _DISPLAY_ row / _CITATION_ / an inline derivation) | record the pointer; proceed to Phase 3 |
| PAPER-LOCAL SWEEP hits — the number appears in a sibling/prior `_VALUES_*.md`, ANY stage's `answered \| read \| answered-local` probe SECTION's `values:` lane / `target:` QA file (seed, claims, display included), `0-displays/*/source/` (metrics.json, source_data.csv), or `_EVIDENCE_1-claims.md` | ADOPT THE POINTER, NOT THE VERDICT: copy the `Source:` path, add `Note: pointer via <file> (<status> <date>)`; the entry enters ⬜ and PLACE re-verifies against the ORIGINAL source (Hard Boundary 4 untouched) |
| No named source and no paper-local hit | raise a question SECTION in 1-probes/ (q-executor: "where does the number for <phrase> come from?") and hand it to the PROBE hub — MATCH greps the bank's QA corpus, and only an unmatched question is DISPATCHED |

Method claims ("Holm-Bonferroni corrected", "cluster-robust SEs") route the
same way: unverifiable-from-named-sources → a question SECTION, not a codebase grep.


## Phase 3: CANDIDATE → _VALUES_

⚠️ **PRECONDITION — READ THE TARGET QA FILE'S STATE LINE BEFORE HARVESTING (R19/R20).** A QA file
is a TICKET that becomes a RECEIPT, and `harvest <stage> <qa_file>` is a published direct
invocation that must gate itself:

```
state=$(sed -n 's/^- state:[[:space:]]*//p' "$qa_file" | head -1)
```

```
  state: answered        ✅ HARVEST. (and it carries no `superseded-by:`)
  state: working         🚫 REFUSE. The `## Answer` is EMPTY BY CONSTRUCTION — the run is still
                         in flight. Harvesting yields ZERO anchors and reports a silent no-op,
                         which HIDES a live claim. Report "in progress since <started>" and stop.
  … superseded-by: X     🔗 FOLLOW THE CHAIN and harvest the LIVE file instead. A superseded
                         file's numbers are STALE, and PLACE auto-places verified values INTO
                         THE MANUSCRIPT — the day-1/day-40 stale-read bug arriving through the
                         HARVEST lane, where read-target-superseded cannot see it.
  NO state line          🚫 REFUSE. `state:` is MANDATORY (checker: qa-no-state).
```

This is READ-ONLY. This worker still NEVER writes the QA file — ONE WRITER, the executor, always.

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
   - Confirm the number is correctly woven into the section .md (tex follows at sync; never edit tex prose directly)
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
1-probe/
  haipipe-paper-probe-citation     citation  _CITATION_.md
  haipipe-paper-probe-values       ← THIS (values, _VALUES_.md)
  haipipe-paper-probe-display      display  0-displays/ units
```


## Done criteria

- [ ] All numbers identified in _VALUES_
- [ ] All entries traced to a source (or flagged 🔍 for CHECK)
- [ ] Source-verified values auto-placed in tex (✅)
- [ ] Mismatches (⚠️) and unknowns (🔍) flagged for CHECK (not blocking)
- [ ] All method claims checked against code (or flagged ❌ for CHECK)
- [ ] _LOG updated with values probe summary


## Anti-patterns

- ❌ "All sections agree, so it's correct." (The parquet decides.)
- ❌ Batching fixes
- ❌ Trusting cached outputs without re-running
- ❌ Fabricating a number to fill a gap
- ❌ Skipping figure-embedded numbers
- ❌ "The method claim is standard, no need to grep."
