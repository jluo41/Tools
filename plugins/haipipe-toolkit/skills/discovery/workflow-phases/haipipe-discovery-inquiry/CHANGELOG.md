## 0.4.1 · 2026-09-04

- Clarify that `1_search`, `2_review`, and `3_idea` are numbered capability
  families, not D1/D2/D3 workflow phases; executable ownership remains under
  `workflow-phases/`.

## 0.4.0 · 2026-09-04

- Make D1 the direct Discovery workflow-table owner and remove the redundant
  standalone workflow skill.
- Separate D1 SCOPE/PREPARE/ACQUIRE/SYNTHESIZE/CLOSE domain authority from the
  shared Page `00–04` authority and define their Result/receipt handoff.
- Add the canonical Full Workflow Table, Page crosswalk, Runs Overview, Human
  Actions, Skill Coverage, and the explicit `R_discovery = N_admitted` law.
- Reserve the D1 Folder's local Runs for Paper/Source Subjects: direct cite
  lineage skips Page EVIDENCE, and CONTENT records its no-Run rationale.
- Preserve `haipipe-discovery-workflow` only as the stable Folder-contract
  registry identity used by metadata and existing receipts.

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
