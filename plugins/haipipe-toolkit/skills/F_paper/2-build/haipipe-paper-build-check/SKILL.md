---
name: haipipe-paper-build-check
description: "Audit a paper folder against the gold-standard layout contract (npjDM2025): masters, 1-compile.sh, NN-MM naming + contiguity, orphan/double \\input, wrapper purity, broken \\input/\\includegraphics/\\bibliography targets, aux hygiene. Report-only; routes each finding to the skill that fixes it. Trigger: check paper structure, structure audit, paper folder check, validate paper layout, conformance, 检查论文结构, /haipipe-paper-build-check."
argument-hint: "[paper-dir]"
allowed-tools: Bash, Read, Grep, Glob
metadata:
  version: "1.1.0"
  last_updated: "2026-06-04"
  summary: "Conformance audit for the gold-standard paper folder layout; report-only."
  changelog:
    - "1.1.0 (2026-06-05): renamed from paper-structure-check to haipipe-paper-build-check (haipipe-paper-* name unification)."
    - "1.0.0 (2026-06-04): initial version; script verified green on Paper-MapPhyTrait-npjDM2025."
---

Skill: haipipe-paper-build-check (2-build)
=======================================

Answer one question: **does this folder conform to `2-build/_shared/paper-folder-anatomy.md`?** Report-only; this skill never edits a file. It is the structural twin of 5-review's content audits, and the verification step `haipipe-paper-build-scaffold` and `haipipe-paper-build-restructure` run before they may report `ok`.

Usage
-----

```
/haipipe-paper-build-check <paper-dir>
/haipipe-paper-build-check          (current dir)
```

Workflow
--------

### Step 1: Run the mechanical checks

```bash
scripts/check_structure.sh <paper-dir>
```

Exit 0 = conforms, 1 = findings, 2 = not a paper folder. The script covers:

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
- `0-display/` assets referenced by no `.tex` at all (candidates for `_old/`, not deletion).

### Step 3: Report + route

Present findings as a table, severity-ranked (✗ before ⚠), each row with its fix route:

| Finding | Fix route |
|---------|-----------|
| Numbering gap, orphan, wrapper prose, stray asset | `/haipipe-paper-build-restructure --repair` |
| Missing folder/driver/compile script (skeleton incomplete) | `/haipipe-paper-build-scaffold` (or restructure if content exists) |
| Broken `\includegraphics` (figure was never produced) | `1-structure` figure skills (`haipipe-paper-structure-figure`, `haipipe-paper-structure-figure-spec`) |
| Broken `\cite` / bib content problems | `components/citation/` (out of scope here; only the `.bib` file's existence is checked) |
| Prose problems noticed in passing | `3-edit` (mention, do not expand) |

Clean run = say so in one line and stop; do not invent findings.

Return contract
---------------

```
status:    ok (conforms) | findings | failed
summary:   counts: ✗ / ⚠, one line per finding category
artifacts: [findings table]
next:      the single highest-leverage fix route from Step 3
```
