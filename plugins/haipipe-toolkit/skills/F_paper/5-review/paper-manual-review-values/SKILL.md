---
name: paper-manual-review-values
description: "Section-by-section, number-by-number manual verification of every quantitative claim in the paper, with a human approval gate at every fix. Re-derives each value from raw data files (not from prose-vs-prose internal consistency) and hunts unsupported method claims (e.g., correction procedures the code never applied). Use when user says \"manually review the values\", \"逐个核对论文数字\", \"walk through every number\", \"pre-submission number pass\", or before any high-stakes submission where a single wrong number is unacceptable."
argument-hint: "[paper-directory]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
  summary: "Section-by-section, number-by-number manual verification of every quantitative claim in the paper, with a human approval gate at every fix."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
---

# Paper Manual Review (Values): Walk Every Number, Approve Every Fix

Walk every quantitative claim in the paper at: **$ARGUMENTS**

## Why This Exists

`/paper-claim-audit` runs a one-shot autonomous review and writes a JSON report. That is fast and good enough for routine checks — but it is not what you want before a top-tier submission.

This skill is the slow, paranoid version. Its job is to:

1. Re-derive every number from raw evidence (parquets, pickles, regression scripts), not from "do other sections of the paper say the same thing?"
2. Show the user the evidence chain for every proposed fix
3. Wait for explicit user approval per claim before editing
4. Hunt for method claims that the code never actually applied (the most common silent error in late-stage drafts)
5. Audit every figure as carefully as every body sentence — figures are where stale numbers hide longest, because the source is usually a closed-format file (PowerPoint, Illustrator) that no body-text correction sweep ever touches

The goal is not speed. The goal is that after this skill finishes, the user can defend every digit in the paper — including every digit baked into every figure — to a reviewer who asks "where does this come from?"

## How This Differs From Sibling Skills

| Skill | Mode | Reviewer | Output | When to use |
|-------|------|----------|--------|-------------|
| `/probe-audit` | autonomous | fresh GPT-5.4 | report | code-honesty audit |
| `/result-to-claim` | autonomous | fresh GPT-5.4 | report | "does the data support the inference?" |
| `/paper-claim-audit` | autonomous, one-shot | fresh GPT-5.4 | JSON+MD | routine pre-submission check |
| **`/paper-manual-review-values`** | **interactive, human-paced** | **same agent + human at every gate** | **edits applied + change log** | **high-stakes final submission** |

The autonomous skills answer "did anything obvious slip through?" This skill answers "can the user defend every number under cross-examination?"

## Core Principle

**Three sources of truth, in this order:**

1. **Raw data files** (`*.parquet`, `*.pkl`, `*.csv`) — the canonical source. Every descriptive claim must round-trip from here.
2. **Analysis scripts** (`evaluation/scripts/*.py`, etc.) — for derived numbers (regression coefficients, AMEs, p-values). Re-run the script's exact pipeline; do not trust cached outputs alone.
3. **Other paper sections** — *consistency check only*, never the primary source. If section A says X% and section B says Y% for the same arm, the parquet decides who's right; you do not pick the majority.

**One claim at a time. One human approval per fix. No batching.**

## Inputs

1. **Paper directory** (the argument)
2. **Raw data files** — parquets, pickles, CSVs the analysis scripts use
3. **Analysis scripts** — the code that produced the table/figure values in the paper
4. **No interpretive artifacts** — do NOT read `EXPERIMENT_LOG.md`, `NARRATIVE_REPORT.md`, `*-progress.md`, or any prose summary of the results. These reflect what someone *thought* the results were, not what the data shows.

## Workflow

### Phase 0: Confirm scope and set up

Before touching any claim:

1. Locate the paper master `.tex` file(s) and all `\input`'d sections.
2. Locate the raw data files. For each, confirm with the user:
   - File path
   - What it represents (e.g., "Stage 1 messaged-and-clicked, date X to Y, N rows")
   - Which paper section(s) it backs
3. Locate the analysis scripts that generated each table/figure. If a table cell exists with no traceable script, flag it as `unverifiable` from the start.
4. **Locate every figure file** referenced by `\includegraphics` or `\input` of a figure-rendering snippet. For each, classify the source format up front:
   - Script-generated (matplotlib/etc.) → record the generator script path
   - Closed-format source in repo (`.pptx`/`.key`/`.ai`/`.fig`/`.drawio`) → record the source path
   - PDF/PNG only → record as `pdf-only` and warn the user that figure-side fixes will require manual reconstruction
5. Confirm with the user: which sections and figures are in scope for this pass? (Default: all.)

Output of this phase: an evidence map shown to the user that covers data sources AND figures:

```
EVIDENCE MAP
├── Stage 1 (sections §3.1, §4.1, App B, App F)
│   └── _WorkSpace/.../<stage1>.parquet  N=444,691
├── Stage 2 (sections §4.2, §4.3, §4.4)
│   ├── _WorkSpace/.../<stage2>.parquet  N=248,448 (date-filtered)
│   └── _WorkSpace/.../<stage2>.pkl      (used by regression script)
├── Regression coefficients (App D table)
│   └── evaluation/scripts/3-generate-tab-main-effects.py
└── Figures
    ├── Figure-CTR-by-variant.pdf         → script: figures/plot_ctr.py    (regenerable)
    ├── Figure-DIKW-EvidenceChain.pdf     → source: NOT IN REPO            (pdf-only — flag)
    └── Figure-architecture.pdf           → source: figures/arch.pptx      (closed-format — manual)
```

If the user disagrees with any mapping, fix it before proceeding. Do not start Phase 1 until the figure source map is complete — discovering a `pdf-only` figure mid-walk is much more expensive than discovering it in Phase 0.

### Phase 1: Build the claim list

For each section file in reading order, extract every quantitative claim. For each claim, record:

- Section file + line (or figure file + bounding region)
- The exact phrase
- The number(s)
- Claim type (sample size / rate / pp delta / regression coef / range / p-value / date / method claim / **figure-embedded**)
- The data source it should trace back to

Skip `%%` and `%` comment lines (they don't render). Do NOT skip table `.tex` files — those contain rendered numbers. **Do NOT skip figures** — many papers bake numbers into figure source files (PowerPoint, Illustrator, exported PDFs) where they drift out of sync with the body text.

For figures, also record:

- Source format: `script` (matplotlib/etc.), `closed-format` (`.pptx`/`.key`/`.ai`), or `pdf-only`
- Caption (from the `\caption{...}` in the section file)
- Embedded numeric strings (extract via `pdftotext <file.pdf> -` or via multimodal PDF read if text extraction fails)

The output is a CSV-style log file: `MANUAL_REVIEW_CLAIMS.tsv`. Show the user the count and the breakdown by type before starting verification.

### Phase 2: Section-by-section walkthrough

For each section, in order:

1. Announce the section: "Now reviewing §X.Y — N claims to verify."
2. For each claim in that section:
   - **Re-derive** the value from the raw data using the appropriate recipe (see "Verification recipes" below).
   - **Compare** to the paper's claim at the displayed precision.
   - **Cross-check** against other sections of the paper that make the same claim. If they disagree, the parquet decides — do not silently pick the majority.
   - **Classify** the status (see "Status taxonomy" below).
   - **Show the user** a 4-line summary:
     ```
     §4.2 line 86: "...69.8% CTR, a 6.7% improvement over...63.3%..."
       paper:    69.8%, +6.7 pp
       data:     69.77% (rounds to 69.8%), raw delta = 69.77 - 63.30 = 6.47 pp
       status:   arithmetic_error — claimed delta does not match subtraction
       fix:      change "6.7%" → "6.5%"
     ```
   - **Wait for user response**: approve / reject / discuss. Never edit without explicit approval.
   - **Apply edit** with `Edit` tool only after approval.
   - **Log** the decision in `MANUAL_REVIEW_LOG.md`.
3. At end of section, summarize: N claims, K approved fixes, M deferred, J flagged for further investigation.

Do not proceed to the next section until the user signals to continue. They may want to commit the section's changes first, or pause.

### Phase 3: Figure walkthrough

Figures are where numbers go to die quietly. A body-text fix sweep does not touch them; figures are most often built in PowerPoint, Keynote, or Illustrator and exported to PDF/PNG, with no programmatic link back to the data. A correction in §4.2 of the body never propagates to the figure unless someone manually opens the source and re-exports.

For every figure referenced in the paper:

1. **Identify the source format**:
   - **Script-generated** (matplotlib, seaborn, ggplot, etc.) → look for the generating script in `evaluation/scripts/`, `figures/`, or similar. The fix path is: edit the script, re-run, regenerate the PDF/PNG.
   - **Closed-format source present** (`.pptx`, `.key`, `.ai`, `.xcf`, `.fig`, `.drawio`) → record the source path. The fix path is: open in the native application, edit, re-export. **The agent CAN ONLY FLAG these — it cannot edit closed-format vector sources.**
   - **PDF/PNG only** (no source in repo) → record as `pdf-only`. Fix path is: ask the user to locate the source, OR rebuild from scratch as a script-generated figure. Flag for human action.

2. **Extract embedded text** to find numeric claims baked into the figure:
   ```bash
   pdftotext -layout <figure.pdf> -    # vector PDFs with text layer
   ```
   If text extraction returns garbage (figure is a rasterized PNG embedded in PDF), fall back to multimodal PDF read — the agent has visual inspection capabilities for PDFs.

3. **Verify each embedded number** using the same recipes as Phase 2: re-derive from raw data, compare at displayed precision, classify status.

4. **Cross-check figure caption against figure content**:
   - The caption (in the section `.tex` file) describes what the figure shows. If the caption says "trace for arm X" but the figure quotes a number that belongs to arm Y, that is a **caption-content mismatch** — flag as `figure_caption_mismatch`.
   - The caption is part of the body text and was already walked in Phase 2; the goal here is to catch the case where the figure and the caption point at different things.

5. **Cross-check figure with body text**: if the same arm/value appears in both a figure and the body, they must agree. Disagreements obey the same rule as Phase 4 (cross-section): the parquet decides. If a figure is on the wrong side of an arithmetic correction (e.g., body now says "+6.5%" but the figure still says "+6.7%"), flag as `figure_drift_from_body`.

6. **Apply or flag fixes**:
   - For **script-generated figures**: edit the script (one approval per change), re-run, regenerate the PDF, verify visual diff with the user before committing.
   - For **closed-format sources**: write the required edits into `MANUAL_REVIEW_FIGURES_TODO.md` with explicit instructions ("open `Figure-X.pptx`, change W1 box from `+6.7%` to `+3.2%`, re-export to `Figure-X.pdf`"). Tell the user clearly: this is a human task; the agent cannot complete it.
   - For **pdf-only figures**: same as closed-format — flag and instruct.

7. **Per-figure summary** at the end:
   ```
   Figure-DIKW-EvidenceChainTrace-New.pdf  (closed-format source: not in repo)
     embedded numbers verified: 8
     errors: 2 (W1 "+6.7%" wrong arm; message text paraphrased)
     warnings: 3 (Stage labeling ambiguous; "vs human-designed best" unclear; Δ unit)
     action: TODO list written to MANUAL_REVIEW_FIGURES_TODO.md
   ```

Do not proceed past Phase 3 until the user has either committed the script-figure regenerations or formally accepted the closed-format TODO list.

### Phase 4: Cross-section consistency pass

After every section and figure is walked individually, do one consistency sweep:

For each numeric value that appears in more than one location (body text, table cell, figure embedded text), group occurrences and check they agree at the same precision. Disagreements indicate a stale snapshot somewhere — usually in a section drafted earlier and never re-synced, or a figure exported once and never updated.

**The fix is always to align with the parquet, not to pick the majority.** Even when 3 sections agree and 1 disagrees, the parquet still gets the casting vote. Even when the body has been corrected and only a figure disagrees, the figure must be brought into line.

Show the user the disagreement table; approve unification edits one at a time. Note that figure-side fixes may have been queued in Phase 3 — confirm those are still on the TODO list and not silently dropped.

### Phase 5: Method-claim audit

This is the phase the autonomous skills miss most often.

For every method claim in the paper, **grep the codebase to verify it was actually implemented.** Method claims include:

- Correction procedures: "Holm-Bonferroni corrected", "Benjamini-Hochberg", "FDR-adjusted", "Bonferroni-corrected"
- Weighting/standardization: "inverse propensity weighted", "covariate-adjusted", "propensity-trimmed"
- Robustness procedures: "cluster-robust SEs", "heteroskedasticity-robust", "bootstrap CIs"
- Sample restrictions: "patients with no prior 7-day messages", "first-invitation-only"
- Aggregation rules: "patient-level clustered", "per-visit", "averaged over X seeds"

For each, extract the claim, then:

```bash
grep -rni "<keyword variants>" evaluation/ code/ scripts/
```

If the script that generated the relevant table/figure does not contain the implementation, flag the claim:
- `unsupported_method_claim` — paper claims X but code does not implement X
- `wrong_method_claim` — paper claims X but code implements Y (e.g., paper says "Holm-Bonferroni" but code does FDR-BH)

The fix is one of:
- **Drop the claim** from the prose (most common, least invasive)
- **Implement the method**, regenerate the table, and verify substantive conclusions hold
- **Correct the claim** to match what the code actually does

Show the user the gap and let them choose.

### Phase 6: Write the change log

After all phases complete, write `MANUAL_REVIEW_LOG.md` to the paper directory with:

```markdown
# Paper Manual Review (Values) — Change Log

**Date**: <ISO-8601>
**Paper**: <paper directory>
**Reviewer**: claude (interactive, human-approved)

## Summary
- Total claims walked: N (body: A, tables: B, figures: C)
- Edits applied to .tex / scripts: K
- Figure-side TODOs (manual): F
- Deferred: M
- Flagged for further investigation: J

## Body & table edits applied
| # | Section / Table | Line | Before | After | Reason |
|---|----------------|------|--------|-------|--------|
| 1 | 0-sections/00_abstract.tex | 67 | "+6.7%" | "+6.5%" | arithmetic_error: 69.8 − 63.3 = 6.5, not 6.7 |
| ... |

## Method claims verified
| Claim | Code support | Action |
|-------|-------------|--------|
| "Holm-Bonferroni corrected" | NOT FOUND in evaluation/scripts/3-*.py | dropped from §4.2 line 120 |
| ... |

## Figures audited
| File | Source format | Status | Action |
|------|--------------|--------|--------|
| Figure-CTR-by-variant.pdf | matplotlib (figures/plot_ctr.py) | clean | none |
| Figure-DIKW-EvidenceChain.pdf | pdf-only | 2 errors, 3 warnings | written to FIGURES_TODO.md |
| Figure-architecture.pdf | pptx (closed-format) | caption_mismatch | written to FIGURES_TODO.md |

## Deferred / flagged (body)
- §X.Y line Z: claim about [...] — needs [data source / clarification / regen]

## Figure TODOs (manual edits required, see MANUAL_REVIEW_FIGURES_TODO.md)
- Figure-DIKW-EvidenceChain.pdf, W1 box: change "+6.7%" → "+3.2%" (wrong arm: trace is for completePro, but +6.7% belongs to efficiencyTech)
- Figure-DIKW-EvidenceChain.pdf, top-left quote: change paraphrased message text to production source
- ...

## Evidence map (snapshot)
[parquet paths, N's, and figure source paths]
```

This file is the audit trail. It is what the user shows their advisor or co-authors to demonstrate the paper went through a real review. The accompanying `MANUAL_REVIEW_FIGURES_TODO.md` is the *action* list — what the human still needs to do in PowerPoint/Illustrator before the figures match the corrected body.

## Verification recipes

Per claim type, the agent runs the corresponding recipe and shows the result.

### Sample size (e.g., "N = 444,691")
```python
df = pd.read_parquet(<file>)
print(len(df[df["messaged"]==1]))
# or with date filter:
print(len(df[(df["d"]>=start) & (df["d"]<=end) & (df["messaged"]==1)]))
```

### Descriptive rate (e.g., "salience CTR = 66.1%")
```python
m = df[df["messaged"]==1]
g = m.groupby("experiment_config").agg(n=("messaged","sum"), c=("clicked","sum"))
g["ctr"] = g["c"] / g["n"]
print(g.loc["salience", "ctr"] * 100)
```

### Percentage-point delta (e.g., "+6.5 pp over baseline")
```python
delta_pp = (g.loc[arm, "ctr"] - g.loc["default", "ctr"]) * 100
```
**Always compute this from the raw rates. Never accept a claimed delta without re-deriving the subtraction.**

### Regression coefficient / AME
Re-run the analysis script's exact pipeline (read its source, replicate the model, the date filter, the controls). If `0.0670` is claimed in column 2 of the table:
```python
res = sm.Logit(y, sm.add_constant(X)).fit(disp=0)
mfx = res.get_margeff(at="overall", method="dydx")
```
Match against the table cell at 4 decimal places.

### p-value
Re-derive from the same regression. If claimed `p<0.001`, the script's `pvalue` for that coefficient must indeed be `<0.001`.

### Method claim
Grep. There is no other recipe — either the implementation is in the code or the claim is wrong.

## Status taxonomy

Per claim, classify as:

- `exact_match` — paper value and evidence match at displayed precision
- `rounding_ok` — paper rounds correctly at displayed precision
- `rounding_drift` — paper rounded the wrong direction (e.g., 3.24 → 3.3 instead of 3.2)
- `arithmetic_error` — individual numbers correct but the stated arithmetic between them does not hold (e.g., "69.8% − 63.3% = 6.7 pp")
- `number_mismatch` — paper value disagrees with evidence beyond rounding tolerance
- `unit_error` — value correct but labeled wrong unit (% vs pp, etc.)
- `stale_snapshot` — paper value matches an older parquet/run, not the canonical one
- `unsupported_method_claim` — paper claims a method the code does not implement
- `wrong_method_claim` — paper claims method X, code implements method Y
- `config_mismatch` — value comes from a different sample/filter than claimed
- `aggregation_mismatch` — claimed aggregation does not match what the script did
- `scope_overclaim` — language overstates evidence breadth (e.g., "consistently" when 1 of 3)
- `figure_drift_from_body` — figure embeds a number that was already corrected in the body (or vice versa)
- `figure_caption_mismatch` — caption describes one thing (e.g., "trace for arm X") but the figure shows another (e.g., a number from arm Y)
- `figure_text_paraphrase` — figure quotes prose (e.g., a message string) that doesn't exactly match the production source
- `figure_unverifiable_source` — figure has no programmatic source in the repo (closed-format `.pptx`/`.key`/`.ai` not committed, or `.pdf`-only) — fixes must be flagged for human action, not applied
- `unverifiable` — no script or data source available to verify

## Failure modes to actively hunt (lessons from real misses)

1. **Regression-coefficient-as-arithmetic.** Paper writes "X% CTR vs Y% baseline, +Z pp" where Z is a regression AME, not the subtraction. Reviewer doing the math gets a different number. Always re-derive the subtraction from raw rates and check it equals the claimed delta.

2. **Rounding direction.** Paper says +3.3 pp when the actual delta is +3.24 pp (rounds to +3.2). Easy to miss because the displayed precision swallows the error if you trust the original computation. Always recompute deltas from full-precision raw rates.

3. **Stale snapshot in one section.** §4.1 says 66.1%, §4.3 says 65.9% for the same arm. Internal-consistency reviews miss this if they only check that "five files agree" — the v0503 trap. Always cross-reference every duplicated number across sections, with the parquet as tiebreaker.

4. **Method claim with no implementation.** Paper says "Holm-Bonferroni corrected" but the script reports raw p-values. Reviewers who request the analysis code will find the gap. Grep every method keyword.

5. **% vs pp confusion.** A difference of two rates is `pp`, not `%`. Many papers (including ours) get this wrong throughout. Note this is often a stylistic deferral — flag it but allow the user to keep `%` if it matches the paper's existing convention.

6. **Cohort/filter drift.** Two tables claim the same N, but they come from slightly different filters (e.g., `messaged==1` vs `messaged==1 & date<=X`). Each filter must be made explicit in the verification log.

7. **Cached vs re-run regression outputs.** A table file checked into the repo may be older than the script that generates it. Always re-run; don't trust the `.tex` table cell as ground truth.

8. **Numbers baked into figures.** Body text gets corrected; figures don't follow. The figure was exported once from PowerPoint/Illustrator, the source file lives on someone's laptop, and a +6.7% in the W1 box outlives every body-text correction sweep. Always extract embedded text from every figure and verify against the same data source as the body. When the source format is closed (`.pptx`/`.key`/`.ai`), the agent can only flag — fix is a manual human task.

9. **Figure caption / figure content mismatch.** Caption says "trace for arm X" but the figure quotes a number that belongs to arm Y. This happens when an author updates the trace target (e.g., switches the headline arm from completePro to efficiencyTech) but only updates the caption, not the figure's embedded content — or vice versa. Always cross-check the caption's claimed referent against the numbers actually shown.

## Output contract

Always write four artifacts to the paper directory:

1. **`MANUAL_REVIEW_CLAIMS.tsv`** — one row per claim, with file:line (or figure file + region), type, paper value, evidence value, status, decision (approved/rejected/deferred).
2. **`MANUAL_REVIEW_LOG.md`** — human-readable change log (see Phase 6 template).
3. **`MANUAL_REVIEW_TODO.md`** — deferred body/table items the user explicitly asked to revisit later.
4. **`MANUAL_REVIEW_FIGURES_TODO.md`** — figure-side fixes the agent could not apply (closed-format sources, missing source files). Each entry must include the figure file, the specific embedded element to change, the old value, the new value, and the reason. Format so the user (or a co-author) can act on it without rerunning the audit.

Edits to `.tex` files go directly via `Edit` tool — but only after explicit user approval per edit. Do not bulk-apply. Edits to script-generated figures go via `Edit` (script source) + bash (regenerate) — same approval-per-change rule.

**Closed-format figures (PowerPoint/Keynote/Illustrator/etc.) are never edited by the agent.** They are always flagged to `MANUAL_REVIEW_FIGURES_TODO.md` for human action, even when the required edit is a single-character change.

## Anti-patterns

- ❌ "All five sections say the same thing, so the number is correct." (The v0503 mistake. Internal consistency ≠ correctness; the parquet decides.)
- ❌ "I'll batch the small rounding fixes and apply them together." (No batching. One approval per edit.)
- ❌ "The paper has been through reviewers, the numbers are probably fine." (Reviewers don't have parquet access. You do.)
- ❌ "The script saved its output to a CSV, that's good enough." (Re-run the script. Cached outputs may predate the canonical data.)
- ❌ "The method claim is standard, no need to grep." (Especially likely to be wrong precisely because it's standard. Always grep.)
- ❌ "I'll check arithmetic at the end as a final pass." (Check arithmetic claim-by-claim. By the end, you've forgotten the context.)
- ❌ "The user already trusts these numbers from the previous round." (Trust nothing. The whole point of this skill is the re-derivation.)
- ❌ "The body text is fixed, the figures will follow." (They will not. Figures live in closed-format sources; nobody opens them again until reviewer comments arrive. Audit every figure separately.)
- ❌ "The figure number must be right because it matches the table cell." (The figure may have been built from the same earlier draft as the table. If both are wrong by the same 0.2 pp, agreeing with each other proves nothing.)
- ❌ "I'll just edit the PDF directly to fix that one number." (Editing exported vector PDFs in place is fragile and breaks reproducibility. Always edit the source — script for matplotlib, slide deck for PPTX, etc. — and re-export.)

## When to run

Run this skill:

1. **After `/paper-claim-audit`** — the autonomous audit catches obvious issues fast; this skill catches the subtle ones.
2. **Before submission to a top-tier venue** — when one wrong number is a desk-reject risk.
3. **After major data updates** — when a parquet, pickle, or analysis script changes, walk every dependent claim.
4. **When a co-author flags "I don't trust these numbers"** — this skill produces the audit trail to settle it.

Do not run this skill:

- During early drafting (numbers churn too fast; use `/paper-claim-audit` for periodic checks instead)
- Without raw data access (the skill is useless without parquets/pickles to re-derive against)

## Notes for the agent running this skill

- You will be tempted to skip steps. Don't. The point is paranoid thoroughness.
- You will be tempted to claim "all numbers verified" after walking only a subset. Don't.
- You will be tempted to trust the paper's prose over your own computation. The parquet decides.
- When the user pushes back on a number, **re-derive it from the parquet on the spot** and show them the derivation. Don't argue from memory.
- When you find a method claim with no code support, the conservative default is to drop the claim; never add a fabricated correction procedure to "make it true."
- If the user changes their mind mid-walkthrough about scope or definitions, update the evidence map and start the affected section over. Better than carrying a stale assumption.
- For figures: when in doubt, extract embedded text via `pdftotext -layout` first and verify visually with the multimodal PDF read second. The two passes catch different errors — text extraction catches numeric drift, visual inspection catches caption-content mismatches and message-text paraphrases.
- For closed-format figure sources: never propose to "edit the PDF directly" as a shortcut. Even if technically possible, it breaks the source-of-truth chain. Write the fix to `MANUAL_REVIEW_FIGURES_TODO.md` and stop.
