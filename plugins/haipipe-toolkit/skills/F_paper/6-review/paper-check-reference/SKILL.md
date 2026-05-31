---
name: paper-check-reference
description: "Audit LaTeX paper cross-references and flag broken/positional/orphan items. Scans the root .tex and all transitively \\input{}-ed files, builds maps of \\label / \\ref / \\hyperref / \\cite / \\input, cross-checks them, and produces a markdown audit report. Catches: broken refs (\\ref with no matching \\label), broken inputs (\\input{} file not found), broken citations (\\cite key not in any .bib), positional issues (\\phantomsection\\label{} placed AFTER \\section*{} heading), unlabeled SI sections, orphan labels, and dead bib entries. Companion to citation-verifier (deeper text-content citation audit) and paper-revise-section (logical revision). Use when user says /paper-check-reference, 'check refs', 'audit references', '查 reference', '检查引用', or before submission to catch broken cross-references."
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
  summary: "Audit LaTeX paper cross-references and flag broken/positional/orphan items."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: paper-check-reference
============================

Mechanical audit of LaTeX cross-references in a paper directory. Scans
all .tex files reachable from the root `\documentclass` via `\input{}`,
builds maps of label/ref/cite/input markers, and produces a markdown
report listing 🔴 broken / 🟡 positional / 🟡 orphan / 🟢 informational
items.

This skill is **mechanical** — it checks marker shape and cross-pointer
integrity, not text content or citation accuracy. For text-level
citation audits (does the cited paper actually support the claim?),
use `/citation-verifier` or `/paper-manual-review-citations`.

Usage
=====

```
/paper-check-reference <paper-root-dir-or-root-tex>
```

The argument is either a directory (skill auto-finds the root `.tex`
with `\documentclass`) or a specific root `.tex` path. Output report
defaults to `<paper-dir>/1-feedback/v<latest-tag>/reference-audit.md`,
or stdout if no `1-feedback/` exists.

What it checks
==============

| Severity | Check | What it catches |
|---|---|---|
| 🔴 | Broken refs | `\ref{X}` / `\hyperref[X]{...}` where `X` has no `\label{X}` anywhere in the project |
| 🔴 | Broken inputs | `\input{path}` where `path` (or `path.tex`) does not exist on disk |
| 🔴 | Broken citations | `\cite{X}` where `X` is not defined as a `@type{X, ...}` entry in any `.bib` |
| 🟡 | Phantom-after-section | `\phantomsection\label{...}` placed AFTER its `\section*{}` heading. Recommended fix: move the line to ABOVE the heading so `\hyperref` clicks land on the heading text. |
| 🟡 | Unlabeled SI / appendix sections | `\section*{SI...}` / `\section*{Supplementary...}` / `\section*{Appendix...}` with no `\phantomsection\label{...}` within 2 lines. Recommended fix: add an anchor (even if no current cross-ref needs it, future ones might). |
| 🟡 | Orphan labels | `\label{X}` defined but `X` is never `\ref`-ed or `\hyperref`-ed. Either remove the label or wire up a cross-ref. |
| 🟢 | Dead bib entries | Bib key defined but never cited. Cleanup optional. |

What it does NOT check
======================

- **Citation correctness** (does paper X actually support claim Y?) — use `/citation-verifier`.
- **Number accuracy** (does the prose number match the data source?) — use `/paper-claim-audit` or `/paper-manual-review-values`.
- **Figure / table content** (does the figure render correctly?) — visual inspection / `/paper-compile`.
- **Style / formatting** (em-dashes, AI-flavor prose) — use `/paper-revise-section` Rule 4.

Workflow
========

### Step 1. Locate the root `.tex`

If the argument is a directory, scan top-level `*.tex` and pick the
one containing `\documentclass`. If the argument is a file, use it
directly.

### Step 2. Build the transitively-input-ed file set

Starting from the root, follow every `\input{...}` and `\include{...}`
recursively (resolving `path` → `path.tex` if needed). Comments
(`%...$`, except escaped `\%`) are stripped before regex.

### Step 3. Extract markers

For each .tex file in the closure, regex-extract:
- `\label{name}` → labels map (name → [(file, line)])
- `\ref{name}` / `\autoref{name}` / `\cref{name}` / `\Cref{name}` /
  `\eqref{name}` / `\nameref{name}` / `\hyperref[name]{...}` → refs map
- `\cite{key}` / `\citep{key}` / `\citet{key}` / etc. → cites map
- `\input{path}` / `\include{path}` → input locations

### Step 4. Specialized positional checks

For each `\phantomsection\label{...}` line, check the nearest
non-empty lines above and below. If above is a `\section*{}` (or
`\section{}` / `\subsection*{}`), flag as `phantom_after_section`.

For each `\section*{}` with title containing "SI", "Supplementary",
or "Appendix", check the 2-line window above/below for any
`\phantomsection\label{}`. If absent, flag as `unlabeled_si_section`.

### Step 5. Cross-check + report

- **Broken refs**: refs whose name is not in labels.
- **Orphan labels**: labels whose name is not in refs.
- **Broken citations**: cite keys not in any `.bib`'s `@type{key, ...}`
  set. Skip this category if no `.bib` files exist in the project.
- **Dead bib entries**: bib keys not in cites (informational only).
- **Broken inputs**: input paths that don't resolve to an existing
  file (with or without `.tex` suffix).

### Step 6. Write the report

Markdown report with one section per category, severity-tagged. Each
broken/positional/orphan item lists the file:line where it was found.
Counts go in a summary table at the top.

Output rules
============

- **Format = `.md` ONLY.** This is a deliverable for the author to
  read, possibly with reviewer or co-author.
- **Save path**:
  - If `<paper-dir>/1-feedback/v<tag>/` exists, save to
    `1-feedback/v<latest-tag>/reference-audit.md` (newest version dir).
  - Otherwise save to `<paper-dir>/reference-audit.md`.
  - Override with `-o <path>` flag.
- **Idempotent**: re-running overwrites the same file.

Implementation
==============

The skill's actual logic lives in `check_refs.py` (Python stdlib only,
no external deps). To run from the command line:

```bash
python3 Tools/plugins/research-toolkit/skills/06_write/paper-check-reference/check_refs.py \
    <paper-root-dir> -o <output.md>
```

When invoked via the Skill tool, the assistant should:
1. Locate `check_refs.py` (path above).
2. Run it via Bash on the user's paper directory.
3. Read the resulting `.md` report.
4. Summarize the 🔴 + 🟡 counts in chat; offer to walk through fixes.

Optional `--fix` mode (NOT in v1)
=================================

A future `--fix` flag would auto-apply trivial repairs:
- Move `\phantomsection\label{}` to ABOVE its `\section*{}` heading.
- Add a `\phantomsection\label{sec:auto_<n>}` to unlabeled SI sections.

Auto-fix is NOT applied to:
- Broken refs (which `\label` to add or which `\ref` to fix is a
  judgment call).
- Broken citations (might be a typo, might be a missing .bib entry).
- Orphan labels (might be load-bearing for future refs).

When to invoke this skill vs. neighbours
========================================

| If the author wants ... | Use |
|---|---|
| Find broken refs / orphan labels / phantomsection issues | **paper-check-reference** (this) |
| Verify a citation actually supports a claim | `/citation-verifier` |
| Verify a number in prose matches the data file | `/paper-claim-audit` or `/paper-manual-review-values` |
| Diagnose & propose paragraph-level revisions | `/paper-revise-section` |
| Compile & visually inspect the PDF | `/paper-compile` |
| Build a tracked-changes diff PDF | `/paper-diff-pdf` |

Hard rules
==========

1. **Mechanical only.** Do not infer or guess the "right" label for a
   broken ref. Report it; let the author decide.
2. **No prose edits.** This skill never touches `.tex` content beyond
   the optional --fix mode (which only moves anchor lines, never
   modifies sentences).
3. **No bib edits.** Even if a citation is broken, do not auto-add
   a .bib entry.
4. **Read-only by default.** v1 only produces the `.md` report; the
   `--fix` mode is opt-in and only for trivial positional fixes.
