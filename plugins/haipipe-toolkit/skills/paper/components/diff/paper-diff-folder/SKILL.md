---
name: paper-diff-folder
description: "Produce a multi-file diff between the current paper folder and a prior version (git commit / branch / tag / sibling folder). Writes 1-diff/vs-<ref>/ inside the paper folder, containing: per-section .tex line diffs, figure delta list, table value delta list, citation delta list, summary.md. Use when preparing a rebuttal package, comparing submissions, or showing reviewers what changed since v0. Companion to haipipe-paper-edit-diffpdf (which produces a single colored PDF). Trigger: diff folder, paper diff, what changed, since last submission, vs commit, /paper-diff-folder."
argument-hint: <paper-folder> <ref> [--scope=sections|display|cite|all]
allowed-tools: Bash, Read, Write, Grep, Glob
---

paper-diff-folder — STUB
=========================

Multi-file diff writer. Sister to `haipipe-paper-edit-diffpdf` (which produces ONE
colored-diff PDF of the manuscript). This skill produces a STRUCTURED
folder of diffs against a reference, written into the paper folder
itself as `1-diff/vs-<ref>/`.

Goal layout produced
--------------------

```
<paper>/1-diff/vs-<ref-shortname>/
├── summary.md                       human-readable overview of changes
├── sections/
│   ├── 00_abstract.diff             unified diff per .tex file
│   ├── 01_introduction.diff
│   ├── 02-00_overview.diff
│   ├── ...
│   └── E_supplementary-revision.diff
├── display/
│   ├── figures-changed.md           added / removed / replaced figures
│   └── tables-changed.md            added / removed / value-shifted tables
├── citations/
│   └── citations-changed.md         added / removed / metadata-changed bib entries
└── metadata.yaml                    ref kind (commit/branch/folder), date, scope
```

Reference forms supported
--------------------------

```
git-commit          paper-diff-folder . abc1234
git-branch          paper-diff-folder . overleaf-2026-05-21-1954
git-tag             paper-diff-folder . submitted-v1
sibling-folder      paper-diff-folder . ../Paper-XXX-prev-snapshot/
backup-folder       paper-diff-folder . 0-sections.backup-2026-05-08
```

Behavior contract
------------------

1. **Resolve ref** — if it's a git ref, materialize a snapshot in
   tempdir; if it's a folder path, use directly.
2. **Diff 0-sections/** — for each pair of matching `.tex` files,
   produce a unified diff. Track adds (only-in-new) and removes
   (only-in-old).
3. **Diff 0-displays/** — list figures/tables added, removed, or with
   changed contents (use pHash for images, file hash for PDF).
4. **Diff .bib** — added / removed / metadata-changed entries.
5. **Write summary.md** — top-of-file changes table:
   `N sections changed, M figures swapped, K citations added/removed`.
6. **Write metadata.yaml** — what ref, what date, what scope.

Invocation example
-------------------

```bash
# Inside a paper folder on branch review_v0325:
/paper-diff-folder . overleaf
# Produces: ./1-diff/vs-overleaf/summary.md + tree
```

Status
------

**STUB**. Implementation TODO. Acceptance criteria:
- Runs on FairGlucose paper (vs `0-fairglucose-icml2026` committed at submission)
- Produces a non-empty summary.md
- All section .tex files have a corresponding `.diff` file (empty if unchanged)
- Figure list matches manually inspected list

Related skills
---------------

- `haipipe-paper-edit-diffpdf` (`components/diff/`) — single-PDF colored diff
- `1-narrative/narrative-report` — what the paper claims; this skill
  shows whether those claims changed
- `6-respond/paper-rebuttal` — consumes summary.md to draft "what we
  changed" block in the rebuttal
