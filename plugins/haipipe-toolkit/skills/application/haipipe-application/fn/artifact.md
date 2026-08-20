# `artifact` · project or promote one delivery unit

1. Resolve the owning accepted Design Page and requested unit.
2. If the unit cannot be accepted/rejected/deployed independently, keep it as a Design Page division and generate a versioned projection under `3-artifacts/`.
3. If it passes the independence test, create/resume one `page-type: artifact` Page with `artifact-kind`, `artifact-unit`, and `design-page`.
4. Load the current Design handoff and venue pack. Reject a stale or missing handoff before authoring.
5. Build the venue-required preview and record Design handoff plus render versions.
6. Run CHECK for trace, venue fit, safety, invariants/variants, and visible-version acceptance.
7. Reconcile hand edits to projections back into the owning Page before acceptance.

Return whether the unit stayed a projection or became a Page, its path, versions, acceptance state, and next action.
