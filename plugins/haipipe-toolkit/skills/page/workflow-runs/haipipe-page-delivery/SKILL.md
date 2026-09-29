---
name: haipipe-page-delivery
description: >-
  The Delivery Run of a Board Page (`rdNN_<target>`): build one declared
  delivery target (web, LaTeX, Word, slides, render) from one released source
  version by running its exporter. The built files are the record: no
  hand-written receipt or manifest. It never rewrites prose or evidence and
  never closes the Page. Trigger: delivery run, build the pdf, build the docx,
  rebuild delivery, stale delivery,
  /haipipe-page-delivery.
metadata:
  version: "0.2.0"
  last_updated: "2026-09-28"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-delivery · one target, one version, one build

> ⛔ **Generated files: never modify them directly; change the code that writes them (or its source), then rerun it** (hard rule, JL 260928; AGENTS.md rule 6). Here that means every file under `delivery/<lane>/`: fix the Page source or the exporter, then run the build again.

**LOAD `../../haipipe-page-workflow/SKILL.md` FIRST.** This file owns the
Delivery Run's delta: when one may be commissioned, what it binds, what it
writes, and what it may not touch. The lanes it writes into are the 📤
Delivery tab's contract in `../../haipipe-workbench-page/ref/delivery.md`;
the identity grammar is `../../haipipe-page/ref/page-run-families.md`.

```text
identity   rdNN_<target>          target ∈ web · latex · word · slide · render
ticket     runs/rdNN_<target>.md
result     results/rdNN_<target>/  runtime.yaml (status, attempt, exporter output)
artifact   delivery/<lane>/…       written by the exporter only; no manifest
actor      agent or automatic; the deck is the one authored exception
```

## 🎯 When it is commissioned

After the content and evidence release barrier is open: the planned Page Runs
are closed and the release decision exists (`haipipe-page-writing`,
`../../haipipe-page/ref/release-decisions.md`). One RD binds one source Page
version, by path and version number, to one target lane. Rebuilding the same target
from the same contract is another attempt in the same RD lineage; a different
target or a materially different source version is a different RD. RD never
reopens or rewrites an RE, and never edits the Page source.

## 🔁 How it runs

1. **Allocate.** The next `rdNN_<target>` and its ticket.
2. **Build.** web through `haipipe-page/cli/page.py build`; LaTeX and Word
   through `/_board/latex` and `/_board/word` (the `exporters/` scripts,
   deterministic, safe to run on click); slides only on the explicit ✨ press
   (`claude -p`, minutes, money); render through the owning Design contract.
3. **Record.** The built files and their file times are the record. Write no
   `delivery/<lane>/build-manifest.json` and no hash by hand (JL 260928, AGENTS.md
   rules 6 and 9); `runtime.yaml` records status, the attempt, and the
   exporter's own warnings.
4. **Show.** The Delivery Workspace compares source and artifacts by file time
   and reports `pass`, `stale`, or `not-built` per lane. A current lane is
   delivery evidence, not a whole-Page acceptance; `haipipe-page-check` is the
   only human whole-Page close gate.

## 🔒 Boundaries

- Never edits `<page>.md`, an Evidence Result, or an accepted Version.
- Never assembles or renames a paper: paper-level assembly is
  `haipipe-paper-assemble`.
- A hand edit inside `delivery/` is overwritten by the next build; the folder
  is derived and safe to gitignore.
- Missing current evidence bindings never fall back to a legacy Bib or display.

## 📂 Files

- `../../haipipe-page-workflow/ref/workflow-table.md` · the `delivery` Run Spec row
- `../../haipipe-page/ref/page-run-families.md` · RD identity and lineage
- `../../haipipe-workbench-page/ref/delivery.md` · the tab, the lanes, the Delivery Workspace
- `../../../../servers/workbench-page/delivery.py` · `export.py` · `exporters/` · the doors and writers
- `../../../paper/haipipe-paper-assemble/SKILL.md` · paper-level assembly, a different Run
