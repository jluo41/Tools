E_insight — Changelog
======================

Layer-scoped changelog for the E_insight (KNOWLEDGE / archive) layer. Newest
first. Rollup lives in the plugin-level `CHANGELOG.md`.


## [2.3.0] — 2026-05-31

### Added
- **Agent skeleton (the layer had none before).** `agents/` now mirrors
  C_task / D_probe, applied THOUGHTFULLY:
  - `creators/` — one thin BUILDER per DIKW layer
    (`card-creator-{data,information,knowledge,wisdom}-agent`). Each calls its
    `haipipe-insight-<layer>` skill headless (full spec → SILENT) to file one
    card, then verifies + returns. `_TEMPLATE.md` to add the next layer.
  - `reviewers/` — **per-type** (a deliberate departure from C/D's
    type-agnostic reviewers, because each DIKW card has a different boundary):
    `card-reviewer-{data,information,knowledge,wisdom}-agent`, each checking
    accuracy (Codex re-reads the cited evidence) + boundary/style — PLUS one
    cross-layer `index-integrity-auditor-agent` (the graph cannot be per-type).
- **`ref/dikw-boundaries.md`** — the canonical boundary of each layer (IS /
  IS NOT / the line to the next layer), the two promotion gates (I→K needs a
  probe; D/I describe vs K/W prescribe), and a complete cross-referenced worked
  example (D01→I01→K01→W01). Creators follow it; per-type reviewers enforce it.
- **`ref/invocation-modes.md`** — the dual-mode contract for the DIKW filer
  skills + the per-layer "spec complete" table + the structured-return schema.
- **DESIGN.md** — agentification + dual-mode + per-type-reviewer design, the
  loop-closure finding, and the asymmetry note (E vs C vs D).
- **Top-level `agents/` registry** — 9 flat symlinks added (registry 13 → 22).

### Changed
- **The 4 DIKW filer skills declare dual-mode** (`haipipe-insight-{data,
  information,knowledge,wisdom}`): interactive (ASK the missing source) OR
  headless (full spec → silent), chosen by input completeness; agent + missing
  source → `status: blocked`, never hang.
- **`haipipe-probe-loop` wired to close L0** (the change lives in D_probe): on
  convergence, Step 3 dispatches `card-creator-data-agent` to file the D card —
  closing the `probe → task → insight` atom the loop previously left open.

### Notes / remaining
- Higher-layer I/K/W auto-synthesis (as D cards accumulate) is NOT per-probe —
  deferred to the report phase / `haipipe-insight-explore`.
- Known model↔skill tension: `haipipe-insight-data` sources a D card from a
  *confirmed probe* (not a task); the loop wiring matches the skill as-built.
  A "D-from-task" reconciliation is a future pass.
