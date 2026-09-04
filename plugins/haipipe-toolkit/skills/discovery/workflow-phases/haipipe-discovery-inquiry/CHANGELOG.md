## 0.3.1 · 2026-09-04

- Clarify that Outline owns the derived Bib and only explicitly declared typed
  CITE items; the aggregate itself is not an Evidence Item.
- Align D1 closure with report-count/path reconciliation and citation
  verification debt.

## 0.3.0 · 2026-09-03

- Align D1 with the current Page contract: `haipipe-plugin-outline` owns the
  Outline Evidence Workspace and CITE/Bib verification.
- Keep Discovery's `runs/` ↔ `results/` as its only local Run inventory; root
  `evidence/` and the standalone Evidence plugin are no longer authorities.

## 0.2.0 · 2026-09-02

- Define D1 Inquiry through five explicit cycles and separate Task progress,
  one-Subject Runs, Page synthesis, Evidence citation authority, and closure.
- Remove the former standalone Bibex dependency in favor of
  `haipipe-plugin-evidence`.

## 0.1.0 · 2026-09-01

- Register `folder-kind: discovery` as D1 with one workflow-owned Page Face,
  Paper/Source Run Task Face, plugins, closure, and handoff.
