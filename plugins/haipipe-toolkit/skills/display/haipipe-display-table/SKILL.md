---
name: haipipe-display-table
description: "Render a publication-quality LaTeX table from an aggregated data file (CSV/JSON) for a paper display unit. Use when user says \"做表\", \"生成表格\", \"regression table\", \"coefficient table\", \"descriptive table\", \"comparison table\", or needs a typeset booktabs table from results. The data renderer for tables, parallel to haipipe-display-figure (plots). Reads aggregated outputs only; never recomputes from raw data."
argument-hint: "[table-spec-or-data-path]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, mcp__codex__codex, mcp__codex__codex-reply
metadata:
  version: "0.2.1"
  last_updated: "2026-07-27"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Paper Display Table: Publication-Quality LaTeX Tables from Aggregated Data

Render the LaTeX table(s) for a paper based on: **$ARGUMENTS**

This is the **data-table renderer** of the display family.
Its sibling
`haipipe-display-figure` renders data *plots*; this skill renders data
*tables*.
Both read an aggregated data file and emit a reproducible asset; neither
recomputes from raw evidence (that is a `haipipe-task-for-display` task).

## Output: write into a display unit

The table goes into the caller-supplied unit directory per the shared contract:
`../ref/display-unit-output-contract.md`. For a Page DISPLAY Result, the caller
supplies `<page>/results/<re-run>/payload/<unit>/`; a View or other caller
supplies its own unit path.
THIS renderer's row: asset -> `assets/table-body.tex` (the `tabular`/`threeparttable`
block), with caller-owned `float.tex` the wrapper that `\input`s it (caption + label + placement); rebuild recipe
-> `recipe/gen_*.py`, reading only the approved aggregate in `intake/inputs/`.

One invocation that produces one bounded table unit may be one Run in the parent Workflow.
The numbered steps, generation, compilation, review, and retries are internal Steps; independent
table units with separate receipts are separate Runs.

For a new unit, read `intake/manifest.yaml` before doing anything else.
It must name the task holder, run, canonical artifact, and snapshot that this table may use.
Do not search task folders or select rows from an arbitrary CSV.
Legacy units that contain only `source/` remain legacy and are not silently migrated.

## Scope: What This Skill Can and Cannot Do

| Category | Can render? | Examples |
|----------|-------------|----------|
| **Coefficient / regression tables** | ✅ Yes | OLS/IV/DiD coefficients with SE rows + significance stars, one column per model |
| **Descriptive / summary tables** | ✅ Yes | Means, SD, N by group; balance tables; sample composition |
| **Comparison / feature tables** | ✅ Yes | Method × property matrices, prior-work comparison, capability grids |
| **Ablation tables** | ✅ Yes | Variant × metric grids with best-row bolding |
| **Multi-panel tables** | ✅ Yes | Panel A / Panel B stacked under one float with shared header |
| **Plots (line/bar/scatter/heatmap)** | ❌ No | Use `haipipe-display-figure` |
| **Computing the numbers** | ❌ No | The aggregated CSV/JSON must already exist (from a task/probe) |

**Boundary with the figure renderer:** if the asset is a chart, use
`haipipe-display-figure`.
If it is a typeset table, use this skill.
Tables
were previously a side-feature of the figure renderer; they now live here so the
table-specific concerns (column alignment, decimal places, significance stars, SE
rows, panels, table notes) can be done properly.

## Constants

- **STYLE = `booktabs`** — Table rule style.
  Always three-line (top/mid/bottom rule), never vertical rules.
- **NUMBER_ALIGN = `siunitx`** — Align numeric columns on the decimal point via `S[table-format=...]`; fall back to `r` if siunitx is unavailable.
- **STARS = `* p<0.05, ** p<0.01, *** p<0.001`** — Default significance thresholds.
  State the exact mapping in the table note.
- **SE_STYLE = `paren-below`** — Standard errors in parentheses on the line below each coefficient.
- **DECIMALS = 3** — Default decimal places for coefficients; 0-2 for counts/N.
- **NOTES = `threeparttable`** — Table notes go in a `threeparttable` `tablenotes` block, not in `\caption{}`.
- **FORMAT = `tex`** — Output is `assets/table-body.tex`; the caller-owned `float.tex` wraps it.
- **REVIEWER_MODEL = `gpt-5.5`** — Model used via Codex MCP for table quality review.

## Inputs

1. **Display contract** — the caller-supplied unit's `README.md` (claim, caption intent, section)
2. **Display Intake** — `intake/manifest.yaml` plus an aggregated CSV/JSON snapshot of *already-computed* results.
   Never raw PHI data.
3. **Optional table spec** — column order, which models, star thresholds, decimals, transpose (variables-as-rows vs models-as-columns), rows to bold

If no display contract or verified intake exists, stop and ask the caller to create one.

## Procedure

A caller-directed invocation that produces one bounded display unit is one Run in its parent's
Workflow. The numbered steps, generation scripts, candidate iterations, compilation, and review stay
inside that Run.

### Step 1: Read the Display Contract and Locate Data

Read `<unit-dir>/README.md` for the claim this table must defend,
the target section, and the caption intent.
Read `intake/manifest.yaml`, then its declared snapshot path.
Confirm the snapshot holds *aggregated* results, not row-level PHI, and that its hash matches.

### Step 2: Infer the Table Type

| Data shape | Table type | Layout |
|------------|-----------|--------|
| coef + SE + p, by model | Regression/coefficient table | variables as rows, models as columns |
| stat × group | Descriptive table | stats as rows, groups as columns |
| method × property | Comparison table | methods as rows, properties as columns |
| variant × metric | Ablation table | variants as rows, metrics as columns; bold best |
| two grouped blocks | Multi-panel | Panel A / Panel B stacked, shared column header |

### Step 3: Choose the Template

Decide: `booktabs` always; add `threeparttable` if there are notes; add `siunitx`
`S` columns if numeric alignment matters; `\resizebox` or `tabularx` only if the
table would exceed column/text width.

### Step 4: Write One Generation Script per Table

For each table, write a standalone Python script under `recipe/` that reads the
frozen intake and emits the `.tex` under `assets/`. Resolve paths from the script
location so the working directory cannot change which data is read. Numbers
come from the file, never hardcoded. If an
Observations row is required, N must be declared in the snapshot; missing or
inconsistent N is a HOLD, never zero.

```python
# gen_table2_main_regression.py
from pathlib import Path
import os
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_ID = os.environ.get("DISPLAY_CANDIDATE", "").strip()
if CANDIDATE_ID and not re.fullmatch(r"[A-Za-z0-9_-]+", CANDIDATE_ID):
    raise ValueError("DISPLAY_CANDIDATE must contain only letters, digits, _ or -")
df = pd.read_csv(ROOT / 'intake/inputs/reg_main.csv')  # m1_n, m2_n are approved snapshot fields when requested
INCLUDE_OBSERVATIONS = True  # set from the approved table spec

def stars(p):
    return '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''

def cell(coef, se, p):
    return f"{coef:.3f}{stars(p)}", f"({se:.3f})"

lines = [
    r"\begin{threeparttable}",
    r"\begin{tabular}{l S[table-format=-1.3,table-space-text-post=\textsuperscript{***}] S[table-format=-1.3,table-space-text-post=\textsuperscript{***}]}",
    r"\toprule",
    r" & {(1) Baseline} & {(2) +Controls} \\",
    r"\midrule",
]
for _, r in df.iterrows():
    c1, s1 = cell(r.m1_coef, r.m1_se, r.m1_p)
    c2, s2 = cell(r.m2_coef, r.m2_se, r.m2_p)
    lines.append(f"{r.term} & {c1} & {c2} \\\\")
    lines.append(f" & {{{s1}}} & {{{s2}}} \\\\")
n_columns = {"m1_n", "m2_n"}
if n_columns.intersection(df.columns) and not n_columns.issubset(df.columns):
    raise ValueError("Snapshot must include both m1_n and m2_n")
if INCLUDE_OBSERVATIONS:
    if not n_columns.issubset(df.columns):
        raise ValueError("Observations requested but snapshot must include m1_n and m2_n")
    def verified_n(column):
        parsed = pd.to_numeric(df[column], errors="coerce")
        if parsed.isna().any():
            raise ValueError(f"{column} must contain a verified value in every snapshot row")
        values = parsed.unique()
        if len(values) != 1 or values[0] < 0 or not float(values[0]).is_integer():
            raise ValueError(f"{column} must contain one verified nonnegative integer")
        return int(values[0])
    n1, n2 = verified_n("m1_n"), verified_n("m2_n")
    lines += [
        r"\midrule",
        r"Observations & {%d} & {%d} \\" % (n1, n2),
    ]
lines += [
    r"\bottomrule",
    r"\end{tabular}",
    r"\begin{tablenotes}\footnotesize",
    r"\item Standard errors in parentheses. * p$<$0.05, ** p$<$0.01, *** p$<$0.001.",
    r"\end{tablenotes}",
    r"\end{threeparttable}",
]
if CANDIDATE_ID:
    out = ROOT / 'candidates' / f'{CANDIDATE_ID}-table-body.tex'
else:
    out = ROOT / 'assets/table-body.tex'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(lines) + "\n", encoding='utf-8')
print(f"Wrote {out}")
```

### Step 5: Run the Script, Compile, and Inspect the Unit Preview

These commands are for a single active render. In candidate mode, do not compile
the unit's canonical `preview.pdf`; use the candidate-specific preview procedure below.

```bash
UNIT_DIR=/path/to/caller-supplied-unit
WORK_ROOT=/path/to/caller-asset-reference-base
python "$UNIT_DIR/recipe/gen_table2_main_regression.py"
(cd "$WORK_ROOT" && pdflatex -output-directory "$UNIT_DIR" "$UNIT_DIR/preview.tex")
```

Confirm `assets/table-body.tex` exists and the numbers match the declared Intake
snapshot by spot-check. Open `preview.pdf` and check clipping, alignment, readability,
and the caption/body pairing. Compilation failure or a visible defect is a HOLD. The
caller supplies and approves `float.tex` (caption, label, placement); it `\input`s
the body asset. Do not create `latex_include.tex` or write a self-contained wrapper:
a table renderer never invents or changes paper-facing caption semantics.

For an explicit comparison, copy the active generator to a candidate-suffixed recipe, edit the
copy for that alternative, and render it without touching the active body:

```bash
cp "$UNIT_DIR/recipe/gen_table2_main_regression.py" "$UNIT_DIR/recipe/gen_table2_main_regression-A.py"
DISPLAY_CANDIDATE=A python "$UNIT_DIR/recipe/gen_table2_main_regression-A.py"
```

This writes `candidates/A-table-body.tex`. Build a candidate-named preview under `candidates/`
using that body and the unchanged caller-owned caption, label, placement, and preview preamble.
Do not replace `float.tex` or `preview.pdf`. Inspect and return that candidate preview with its id;
only after the caller chooses it, copy its body to `assets/table-body.tex` and rebuild the canonical
unit preview.

### Step 6: Table Quality Review with REVIEWER_MODEL

Send the matching compiled preview and table body with its approved claim and
caption to GPT-5.5 (via Codex MCP) for advisory review. In candidate mode, use
the candidate-named preview and `candidates/<id>-table-body.tex`, never the
unit's existing `preview.pdf`. A score does not accept or promote a unit; that
decision belongs to the caller.

```
mcp__codex__codex:
  model: gpt-5.5
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    Review this LaTeX table for a [VENUE] submission.
    1. Is the caption self-contained and the header unambiguous?
    2. Are significance stars defined in a note, and consistent with the p-values?
    3. Is numeric alignment correct (decimal-aligned)?
    4. Does the table exceed column/text width?
    5. Any missing rows (Observations, R^2, controls indicator)?
    [paste active or candidate table body + caller-approved caption; attach its matching preview]
```

### Step 7: Quality Checklist

- [ ] Three-line booktabs rules; **no vertical rules**
- [ ] Numbers decimal-aligned; consistent decimal places per column
- [ ] Significance stars present AND defined in a `tablenotes` note
- [ ] Standard errors styled consistently (parentheses, line below)
- [ ] `Observations` / `R^2` / controls-indicator rows use declared snapshot fields; HOLD when a required value is missing
- [ ] **No title inside the table** — caption only
- [ ] Fits column width (`0.48\textwidth`-class) or full text width; `\resizebox` only as last resort
- [ ] Notes in `threeparttable`, not crammed into `\caption{}`
- [ ] Readable in grayscale (bolding/stars, not color, marks the key row)

## Output

The display unit layout (asset -> `assets/table-body.tex` wrapped by `float.tex`,
approved values -> `intake/inputs/`, rebuild recipe -> `recipe/gen_table*.py`) is the shared contract:
`../ref/display-unit-output-contract.md`.

## Relation to the Display Stage and Tasks

```
display-input task (server, PHI)  --aggregate + provenance-->  Intake  -->  this skill  -->  table body
        computes the numbers                                 freezes approved values     (Paper wraps it)
```

The heavy computation (regression, descriptives) is a `haipipe-task-for-display`
task that runs against secure data and exports a movable aggregated CSV.
This
skill turns that CSV into the publication table.
Same split as
`haipipe-display-figure`: the task owns the data, the renderer owns the
typesetting.

## Specialist Return Contract

```
status:    ok | blocked | failed  # ok means rendered/inspected, not selected or accepted
summary:   which table(s) rendered, from which data file, into which display unit
artifacts: [assets/table-body.tex or candidates/<id>-table-body.tex, recipe, inspected preview]
selection: pending | <candidate-id selected by caller>
accepted:  pending  # only the authorized human owner may change this
next:      suggested next command (often /haipipe-paper-display build or insert)
```
