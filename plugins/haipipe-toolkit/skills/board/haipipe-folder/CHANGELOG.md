# Changelog

## 0.5.1 · 2026-09-05

- Fix the future Board Tables row grain as one Board Page/Page Folder while
  keeping the current Folder tab, Outline, and Runs surfaces separate.

## 0.5.0 · 2026-09-04

- Define Tables as read projections over the Page Face and Task Face, with
  separate plan and display/runtime lenses.
- Record that Folder currently has separate Folder-tab inventory, Page Outline
  planning/evidence, and Runs runtime projections, but no unified Board Table.
- Reserve Board Tables as a future sibling contract without adding a
  `board-table/` Folder lane or a second Folder authority.

## 0.4.2 · 2026-09-04

- Add the narrow canonical family-owner contract for a stable base Folder kind
  such as Task: it owns both faces directly and must not invent a fake workflow
  phase or duplicate Page-Type skill.

## 0.4.1 · 2026-09-04

- Retire PageX from current Folder plugin selection. Cross-Folder context now
  uses explicit Context Workspace source addresses; cross-Folder evidence uses
  full Supporting Run ids or frozen Local Input addresses. Existing PageX
  material remains read-only migration history.

## 0.4.0 · 2026-09-01

- Require every phase with addressable work to implement its workflow's
  Phase × Run row through a matching Task-Face Run Profile.
- Keep the workflow table as index, phase profile as executable detail, and
  runtime receipts as actual inventory; treat disagreement as structural error.

## 0.3.1 · 2026-09-01

- Delegate the shared Level-4 Run identity, Ticket/Result pairing, receipt,
  lifecycle, and audit invariants to the new neutral `haipipe-run` contract.

## 0.3.0 · 2026-09-01

- Rename the optional presenter from Execution to Runs; Execute remains a
  workflow action and Runs presents plural durable attempts.
- Define Folder-local and Job-backed Task Run/Result mappings as two physical
  dialects of one logical address; never copy Job Results under the Task Page.

## 0.2.0 · 2026-09-01

- Replace the optional Code capability with Execution: exact `runs/` and
  `results/` pairs define the capability, while `scripts/` and config are
  optional implementation material.
- Keep the Task Face universal and Execution optional; the presenter owns no
  lifecycle or closure authority.

## 0.1.3 · 2026-08-31

- Make `workflow/phase.yaml current.folder-kind` the runtime authority for an
  in-place Folder; malformed current state and conflicting Page frontmatter
  block routing instead of falling back.

## 0.1.2 · 2026-08-31

- Give `workflow/phase.yaml` a concrete current/history grammar and classify it
  as control metadata that does not violate phase material-purity gates.
- Add required `page_ruling: none | domain-gate | local` metadata so the owning
  phase, not the generic Page loop, determines whether CHECK owes a person
  RULING and whether it reuses a domain gate.

## 0.1.1 · 2026-08-31

- Define in-place phase evolution: stable Folder address, one current
  `folder-kind`, and append-only `workflow/phase.yaml` history.
- Require cross-Folder audit phases to leave a minimal addressable receipt
  Folder instead of existing only as an unrecorded verb.

## 0.1.0 · 2026-08-31

- Establish Folder as the neutral work object with Page and Task faces.
- Place Folder-kind semantics in domain workflow phases rather than Page-Type skills.
- Define the phase metadata/section contract and legacy `page-type:` bridge.
- Retire the architectural need for a separate Task plugin; PageX binds Folders.
