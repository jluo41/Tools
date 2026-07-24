---
name: haipipe-paper-conform
description: "Audit a paper folder against the gold-standard layout contract (npjDM2025): masters, 1-compile.sh, NN-MM naming + contiguity, orphan/double \\input, wrapper purity, broken \\input/\\includegraphics/\\bibliography targets, aux hygiene. Report-only; routes each finding to the skill that fixes it. Trigger: check paper structure, structure audit, paper folder check, validate paper layout, conformance, 检查论文结构, /haipipe-paper-conform."
argument-hint: "[paper-dir]"
allowed-tools: Bash, Read, Grep, Glob
metadata:
  version: "0.1.1"
  last_updated: "2026-07-19"
  summary: "Conformance audit for the gold-standard paper folder layout; report-only."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-conform (3-deliver)
=======================================

Answer one question: **does this folder conform to `2-phase/REF/paper-folder-anatomy.md`?**
Report-only; this skill never edits a file.
It is the structural twin of 5-review's content audits, and the verification step `haipipe-paper-scaffold` and `haipipe-paper-restructure` run before they may report `ok`.

Usage
-----

```
/haipipe-paper-conform <paper-dir>
/haipipe-paper-conform          (current dir)
```

Workflow
--------

### Step 1: Run the mechanical checks

```bash
scripts/check_structure.sh <paper-dir>
```

Exit 0 = conforms, 1 = findings, 2 = not a paper folder.
The script covers:

| Block | Checks |
|-------|--------|
| A masters | `0-*.tex` exist (sans `-DIFF`), each has `\documentclass` |
| B build | `1-compile.sh` present + executable |
| C naming | `NN[-MM]_<slug>.tex` / `X_<slug>.tex` grammar; `NN` and `NN-MM` sequences contiguous; `NN-MM` groups have their `NN_` wrapper |
| D wiring | every section file `\input` exactly once (orphans ✗, double-inputs ⚠) |
| E roles | no `\documentclass` in `0-sections/`; wrappers hold only `\input` lines; unstarred `\section{}` in a leaf ⚠ |
| F-H paths | every `\input`, `\includegraphics`, `\bibliography` target exists on disk |
| I hygiene | lingering aux files ⚠ |

### Step 2: Judgment checks (the script cannot see these)

Read briefly and report, do not fix:

- Filename slug still describes the file's content (`02-05_trait-rating-correlation.tex` should be about trait-rating correlation).
- Driver `\input` order matches the venue's section order.
- SI leaves (`A_*`..`Z_*`) are reached only from the SI driver, main sections only from the main driver.
- `0-displays/` assets referenced by no `.tex` at all (candidates for `_old/`, not deletion).

### Step 3: Report + route

Present findings as a table, severity-ranked (✗ before ⚠), each row with its fix route:

| Finding | Fix route |
|---------|-----------|
| Numbering gap, orphan, wrapper prose, stray asset | `/haipipe-paper-restructure --repair` |
| Missing folder/driver/compile script (skeleton incomplete) | `/haipipe-paper-scaffold` (or restructure if content exists) |
| Broken `\includegraphics` (figure was never produced) | `1-lifecycle` figure skills (`haipipe-paper-display-figure`, `haipipe-paper-display-diagram`) |
| Broken `\cite` / bib content problems | `/haipipe-paper-check-evidence` (out of scope here; only the `.bib` file's existence is checked) |
| Prose problems noticed in passing | `1-lifecycle/5-section-edit` (mention, do not expand) |

Clean run = say so in one line and stop; do not invent findings.

Return contract
---------------

```
status:    ok (conforms) | findings | failed
summary:   counts: ✗ / ⚠, one line per finding category
artifacts: [findings table]
next:      the single highest-leverage fix route from Step 3
```
