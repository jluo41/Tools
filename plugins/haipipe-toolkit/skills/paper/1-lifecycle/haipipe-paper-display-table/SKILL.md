---
name: haipipe-paper-display-table
description: "Render a publication-quality LaTeX table from an aggregated data file (CSV/JSON) for a paper display unit. Use when user says \"做表\", \"生成表格\", \"regression table\", \"coefficient table\", \"descriptive table\", \"comparison table\", or needs a typeset booktabs table from results. The data renderer for tables, parallel to haipipe-paper-display-figure (plots). Reads aggregated outputs only; never recomputes from raw data."
argument-hint: "[table-spec-or-data-path]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, mcp__codex__codex, mcp__codex__codex-reply
metadata:
  version: "1.0.0"
  last_updated: "2026-06-22"
  summary: "Render publication-quality LaTeX tables from aggregated data files into a paper display unit."
  changelog:
    - "1.0.0 (2026-06-22): created as the dedicated table renderer of the display family; takes over table duty from haipipe-paper-display-figure (which is now plots-only)."
---

# Paper Display Table: Publication-Quality LaTeX Tables from Aggregated Data

Render the LaTeX table(s) for a paper based on: **$ARGUMENTS**

This is the **data-table renderer** of the display family. Its sibling
`haipipe-paper-display-figure` renders data *plots*; this skill renders data
*tables*. Both read an aggregated data file and emit a reproducible asset; neither
recomputes from raw evidence (that is a `haipipe-task-for-display` task).

## Scope: What This Skill Can and Cannot Do

| Category | Can render? | Examples |
|----------|-------------|----------|
| **Coefficient / regression tables** | ✅ Yes | OLS/IV/DiD coefficients with SE rows + significance stars, one column per model |
| **Descriptive / summary tables** | ✅ Yes | Means, SD, N by group; balance tables; sample composition |
| **Comparison / feature tables** | ✅ Yes | Method × property matrices, prior-work comparison, capability grids |
| **Ablation tables** | ✅ Yes | Variant × metric grids with best-row bolding |
| **Multi-panel tables** | ✅ Yes | Panel A / Panel B stacked under one float with shared header |
| **Plots (line/bar/scatter/heatmap)** | ❌ No | Use `haipipe-paper-display-figure` |
| **Computing the numbers** | ❌ No | The aggregated CSV/JSON must already exist (from a task/probe) |

**Boundary with the figure renderer:** if the asset is a chart, use
`haipipe-paper-display-figure`. If it is a typeset table, use this skill. Tables
were previously a side-feature of the figure renderer; they now live here so the
table-specific concerns (column alignment, decimal places, significance stars, SE
rows, panels, table notes) can be done properly.

## Constants

- **STYLE = `booktabs`** — Table rule style. Always three-line (top/mid/bottom rule), never vertical rules.
- **NUMBER_ALIGN = `siunitx`** — Align numeric columns on the decimal point via `S[table-format=...]`; fall back to `r` if siunitx is unavailable.
- **STARS = `* p<0.05, ** p<0.01, *** p<0.001`** — Default significance thresholds. State the exact mapping in the table note.
- **SE_STYLE = `paren-below`** — Standard errors in parentheses on the line below each coefficient.
- **DECIMALS = 3** — Default decimal places for coefficients; 0-2 for counts/N.
- **NOTES = `threeparttable`** — Table notes go in a `threeparttable` `tablenotes` block, not in `\caption{}`.
- **FORMAT = `tex`** — Output is a standalone `float.tex` fragment, input-able by the paper.
- **REVIEWER_MODEL = `gpt-5.5`** — Model used via Codex MCP for table quality review.

## Inputs

1. **Display contract** — the unit's `README.md` (claim, caption intent, section, source) under `0-displays/displayNN-<slug>/`
2. **Aggregated data file** — a CSV/JSON of *already-computed* results (e.g. a regression export from a `Z0N_Display` task). Never raw PHI data.
3. **Optional table spec** — column order, which models, star thresholds, decimals, transpose (variables-as-rows vs models-as-columns), rows to bold

If no display contract exists, scan for aggregated data files and ask which table to render.

## Workflow

### Step 1: Read the Display Contract and Locate Data

Read `0-displays/displayNN-<slug>/README.md` for the claim this table must defend,
the target section, and the caption intent. Locate the aggregated data file it
cites. Confirm the file holds *aggregated* results, not row-level PHI.

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

For each table, write a standalone Python script that reads the data file and
emits the `.tex`. Numbers come from the file, never hardcoded.

```python
# gen_table2_main_regression.py
import pandas as pd

df = pd.read_csv('source/reg_main.csv')   # columns: term, m1_coef, m1_se, m1_p, m2_coef, ...

def stars(p):
    return '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''

def cell(coef, se, p):
    return f"{coef:.3f}{stars(p)}", f"({se:.3f})"

lines = [
    r"\begin{table}[t]", r"\centering",
    r"\caption{Effect of agreeableness on opioid prescribing.}",
    r"\label{tab:main}",
    r"\begin{threeparttable}",
    r"\begin{tabular}{l S[table-format=-1.3] S[table-format=-1.3]}",
    r"\toprule",
    r" & {(1) Baseline} & {(2) +Controls} \\",
    r"\midrule",
]
for _, r in df.iterrows():
    c1, s1 = cell(r.m1_coef, r.m1_se, r.m1_p)
    c2, s2 = cell(r.m2_coef, r.m2_se, r.m2_p)
    lines.append(f"{r.term} & {c1} & {c2} \\\\")
    lines.append(f" & {s1} & {s2} \\\\")
lines += [
    r"\midrule",
    r"Observations & {%d} & {%d} \\" % (df.attrs.get('n1', 0), df.attrs.get('n2', 0)),
    r"\bottomrule",
    r"\end{tabular}",
    r"\begin{tablenotes}\footnotesize",
    r"\item Standard errors in parentheses. * p$<$0.05, ** p$<$0.01, *** p$<$0.001.",
    r"\end{tablenotes}",
    r"\end{threeparttable}",
    r"\end{table}",
]
open('float.tex', 'w').write("\n".join(lines) + "\n")
print("Wrote float.tex")
```

### Step 5: Run the Script, Emit the Include, and Verify

```bash
python gen_table*.py
```

Confirm `float.tex` exists, compiles standalone, and the numbers match the source
file by spot-check. Then write the one-line `latex_include.tex` (`\input{...float.tex}`)
for the master shell.

**float.tex convention:** match the display unit. If the unit's scaffold splits
the float into a caption/label wrapper (`float.tex`) that `\input`s a body asset
(`assets/table-body.tex`), emit the `tabular`/`threeparttable` block into the body
asset and leave the wrapper alone. If the unit has no such split, a self-contained
`float.tex` (the example above) is correct.

### Step 6: Table Quality Review with REVIEWER_MODEL

Send the rendered table + caption to GPT-5.5 (via Codex MCP) for review:

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
    [paste float.tex + caption]
```

### Step 7: Quality Checklist

- [ ] Three-line booktabs rules; **no vertical rules**
- [ ] Numbers decimal-aligned; consistent decimal places per column
- [ ] Significance stars present AND defined in a `tablenotes` note
- [ ] Standard errors styled consistently (parentheses, line below)
- [ ] `Observations` / `R^2` / controls-indicator rows present where relevant
- [ ] **No title inside the table** — caption only
- [ ] Fits column width (`0.48\textwidth`-class) or full text width; `\resizebox` only as last resort
- [ ] Notes in `threeparttable`, not crammed into `\caption{}`
- [ ] Readable in grayscale (bolding/stars, not color, marks the key row)

## Output

```
0-displays/displayNN-<slug>/
├── source/
│   └── reg_main.csv               # aggregated data (from a task; movable, not PHI)
├── gen_table2_main_regression.py  # reproducible CSV -> tex script
├── float.tex                      # the typeset table, \input-able
└── latex_include.tex              # \input snippet for the master
```

## Key Rules

- **Every table must be reproducible** — save the generation script alongside `float.tex`.
- **Do NOT hardcode numbers** — always read from the aggregated CSV/JSON. A hand-typed coefficient is a defect.
- **Aggregated input only** — never read raw row-level / PHI data here; that computation is a `haipipe-task-for-display` task.
- **booktabs, no vertical rules, no chart junk.**
- **Stars and SE rows follow one stated convention**, defined in a `threeparttable` note.
- **One script per table** — re-run a single table when its data changes.
- **No titles inside tables** — captions are in LaTeX only.

## Relation to the Display Stage and Tasks

```
Z0N_Display task (server, PHI)  --aggregated CSV-->  this skill (laptop-safe)  -->  float.tex
        computes the numbers                          typesets the table
```

The heavy computation (regression, descriptives) is a `haipipe-task-for-display`
task that runs against secure data and exports a movable aggregated CSV. This
skill turns that CSV into the publication table. Same split as
`haipipe-paper-display-figure`: the task owns the data, the renderer owns the
typesetting.

## Specialist Return Contract

```
status:    ok | blocked | failed
summary:   which table(s) rendered, from which data file, into which display unit
artifacts: [float.tex, gen script, latex_include.tex paths]
next:      suggested next command (often /haipipe-paper-display build or insert)
```
