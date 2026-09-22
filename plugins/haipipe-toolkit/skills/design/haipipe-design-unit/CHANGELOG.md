# haipipe-design-unit · version history

## 0.4.0 current · 2026-09-20 (version unchanged at 0.4.0)

- One Ticket produces one Result; current caller duties end at independent
  Verify and ready Delivery. Historical Adopt receipts remain audit-only.
- Optional Result-local render manifests bind source and image hashes, Item,
  Generate Run and version. Verify may render only into its own Result; images
  do not add content artifacts. The checker validates both local and target
  render evidence, and the presenter reads it without writing a projection.
- The renderer requires an explicit Result directory, rejects closed Results,
  escapes and overwritten versions, and measures the actual Playwright viewport
  using local Chrome. Horizontal/left clipping and vertical overflow cannot
  pass `fits_one_screen`. Fresh-context UI validation exposed the old mismatch.
- Resolve venue guides from the current Design tree and distinguish named hold
  diagnostics, human Commission holds, and blocked runtime receipts.

- `render_screen.py` measures form controls: a control's shown text (its
  value, its chosen option, or its placeholder) joins the weakest-contrast
  sweep, which walked past it before, and every field's edge against what it
  sits on is reported as `weakest_control_border`, with `controls` counting
  them. Found on a login screen whose three `select` date controls were
  invisible to the sweep.
- A UI unit draws anything the patient types into or chooses from as a real
  form control, never a styled `div`, so the render can measure it.

## 0.4.0 · 2026-09-18 (version unchanged at 0.4.0)

- Criterion kinds `starts_with` and `ends_with` join the v2 contract;
  `ends_with` compares the draft with trailing whitespace stripped,
  `starts_with` with leading whitespace stripped.
- The records check reads a closed run's inputs outside the Design Folder
  (Insight pages) as history, so their later edits do not void it; an open
  run must match its pins exactly; a superseded run needs a reason and no
  result. Messages use folder-relative paths and plain words ("Generate
  Result", never "DU").
- Docs: config `goal` is the item's goal sentence; the config carries the
  released rule text and is copied unchanged into Generate and Verify;
  `max_iterations` is the budget inside one Generate run; the brainstorm
  stance limit and the challenge stance/mode pairing are stated; the approval
  record is `results/rdNN_commission_*/decision.yaml`; examples use
  `_item01` slugs and `rNN` criterion ids; a review with unresolved checks is
  failed and routed back to Verify; venue packs are not pinned; the "DU" and
  "v4" labels are gone; one version-governance paragraph instead of two.

## 0.4.0 · 2026-09-13 · user ruling

- Keep the current worker pre-1.0. Later-looking labels below are retracted as
  release assignments and retained only as development provenance.
- Any future `1.0.0+` requires explicit user approval.
- 2026-09-16: the Ticket gained `item: ITEM<NN>`, naming the Design Item the
  Run serves; the checker does not interpret it, the Design workbench groups
  Runs by it.

## 4.0.1 · 2026-09-13

- Forbid treating unsupported Design bytes as readable/read-only migration
  history, fallback evidence, or any compatibility surface.

## 4.0.0 · 2026-09-13

- Move the worker out of `workflow-phases/` and require `rdNN_*` identity.
- Accept only Ticket/Result v2; actively reject v1 and old Design shapes.
- Remove the D2 compatibility reader and old-unit input route.

## 3.0.0 · 2026-09-13

- Add v2 Ticket/Result support with required, mode-aware `design_intent` while
  retaining v1 read compatibility.
- Reject Page Run identities as Design evidence/authority inputs and make
  candidate revisions return through new immutable generation Runs.

## 1.0.4 · 2026-09-01

- Rename the optional executable-unit presenter from Execution to Runs.

## 1.0.3 · 2026-09-01

- Rename optional executable-unit Code to Execution. Run/Result pairing is the
  capability; scripts are optional implementation material.

## 1.0.2 · 2026-08-31

- Make the Page Face posture-aware: pool units expose disclaimer evidence,
  ideation, and inspiration, and forbid `prospect.md` rather than owing it.

## 1.0.1 · 2026-08-31

- Define D2 as the in-place Unit identity of the stable DU Folder, including
  append-only D2 → D3 and failed-verdict D3 → D2 transitions.

## 1.0.0 · 2026-08-31

- Split D2 Unit realization into its own phase-owned Folder contract.
- Preserve posture-specific realization and evidence-grant boundaries.
