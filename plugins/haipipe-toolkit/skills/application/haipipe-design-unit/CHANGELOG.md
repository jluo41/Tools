# haipipe-design-unit · version history

## 0.4.0 current · 2026-09-13 · user ruling

- Keep the current worker pre-1.0. Later-looking labels below are retracted as
  release assignments and retained only as development provenance.
- Any future `1.0.0+` requires explicit user approval.

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
