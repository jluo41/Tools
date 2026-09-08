# Design v2 migration · 2026-09-07

New work uses a stable `folder-kind: design` Folder and YAML Run Tickets.
Generation Result = DU; verification Result is separate. The unit skill is
a worker, not D2's Folder owner. The historical D2 kind remains resolvable
through the read-only haipipe-design-realization adapter.

## Compatibility boundary

- Existing `design/DU*/` content, card releases, judged lines, phase.yaml,
  accepted rows, and render versions remain unchanged and readable.
- After explicit owner-metadata migration, new commissions in those DS Folders
  use runs/ and results/. Pin old content
  as legacy base/reference files. Never manufacture old execution receipts.
- A legacy record is not automatically eligible for native verify, which
  requires a manifest-backed DU Result. Review it under the legacy reader
  or explicitly commission an input adapter; never silently upgrade authority.
- Current adopted output stays visible until a person adopts a newer result.
- D1/D3/D4/D5 legacy phase descriptions and the old Design plugin are readers,
  not alternate writers. D0 Brief remains a board-scoped input.
- Existing signed W handoffs are pinned as versioned inputs with their
  authority checks intact. Insight itself is unchanged; no new Insight Run
  family or new PageX write is introduced by this migration.
- No live application board is migrated by this skill-source change.

## Existing Folder entry gate

A legacy `workflow/phase.yaml` is still authoritative while it exists; merely
adding Run files must not route the Page through a read-only D4 writer. Before
new work in such a Folder (or one declaring `folder-kind: design-division`),
obtain explicit approval for an owner-metadata migration. Preserve the exact
old control file and Page metadata under a named `workflow/legacy/` snapshot,
remove only that archived legacy file from the active phase.yaml address,
and set the active Page's `folder-kind: design`. Record the migration and its
source hashes. Check that the Page now resolves to `haipipe-design` before
allocating any Ticket. Do not touch historical DU payloads, decisions, previews,
or manufacture past runtime receipts. Without that approval, remain read-only.

New native Folders start with the design kind and no phase.yaml; no migration
is needed. A source-skill update does not grant authority to migrate live Folders.

## Affected callers and checks

Update the Design door/workflow, unit skill, designer agent, Application
design/render/crossing instructions, legacy phase adapters, neutral Run
vocabulary, Folder routing, and Board's Design checker in the same change.
Existing legacy design-family tests remain meaningful; native Run tests add
pairing, hashes, check coverage, independent identity, immutable targets,
rejecting-but-complete verification, and planned/orphan inventory cases.

Historical doctrine is retained in legacy-board.md, the workflow's
legacy-workflow.md, and the old plugin's legacy-thread.md. Load those only
when handling existing records. No current source should send new work into
the old mutable DU phase lifecycle.
