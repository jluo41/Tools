---
name: haipipe-page-delivery
description: >-
  The Delivery Run of a Board Page (`rdNN_<target>`): build one declared
  delivery target (web, LaTeX, Word, slides, render) from one released source
  version and record the artifact and its build receipt. It never rewrites
  prose or evidence and never closes the Page. Trigger: delivery run, build the
  pdf, build the docx, rebuild delivery, delivery receipt, stale delivery,
  /haipipe-page-delivery.
metadata:
  version: "0.1.0"
  last_updated: "2026-09-22"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-delivery · one target, one version, one receipt

**LOAD `../../haipipe-page-workflow/SKILL.md` FIRST.** This file owns the
Delivery Run's delta: when one may be commissioned, what it binds, what it
writes, and what it may not touch. The lanes it writes into are the 📤
Delivery tab's contract in `../../haipipe-workbench-page/ref/delivery.md`;
the identity grammar is `../../haipipe-page/ref/page-run-families.md`.

```text
identity   rdNN_<target>          target ∈ web · latex · word · slide · render
ticket     runs/rdNN_<target>.md
result     results/rdNN_<target>/  runtime.yaml · build receipt
artifact   delivery/<lane>/…       plus delivery/<lane>/build-manifest.json
actor      agent or automatic; the deck is the one authored exception
```

## 🎯 When it is commissioned

After the content and evidence release barrier is open: the planned Page Runs
are closed and the release decision exists (`haipipe-page-writing`,
`../../haipipe-page/ref/release-decisions.md`). One RD binds one source Page
version, by path and SHA-256, to one target lane. Rebuilding the same target
from the same contract is another attempt in the same RD lineage; a different
target or a materially different source version is a different RD. RD never
reopens or rewrites an RE, and never edits the Page source.

## 🔁 How it runs

1. **Allocate.** The next `rdNN_<target>`, its ticket, and a planned receipt.
2. **Build.** web through `haipipe-page/cli/page.py build`; LaTeX and Word
   through `/_board/latex` and `/_board/word` (the `exporters/` scripts,
   deterministic, safe to run on click); slides only on the explicit ✨ press
   (`claude -p`, minutes, money); render through the owning Design contract.
3. **Receipt.** `delivery/<lane>/build-manifest.json` with the source hash,
   artifact hashes, and diagnostics; `runtime.yaml` records status and the
   exact attempt.
4. **Show.** The Delivery Workspace compares source and artifacts and reports
   `pass`, `stale`, `unverified`, or `not-built` per lane. A build receipt is
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
