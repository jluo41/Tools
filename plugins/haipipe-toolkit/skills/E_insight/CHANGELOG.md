E_insight — Changelog
======================

Layer-scoped changelog for the E_insight (KNOWLEDGE / archive) layer. Newest
first. Rollup lives in the plugin-level `CHANGELOG.md`.


## [2.3.4] — 2026-05-31

### Added
- **W is now wired into the probe-cycle** (the K's twin). A converged
  `haipipe-probe-loop` Step 3 now files the 🟨 K, then OPTIONALLY (◇) chains
  `card-creator-wisdom-agent --scope <new-K>` to file the per-probe 🟧 W (the
  probe's concrete next-step), scoped to the just-filed K. Skips when the probe
  implies no concrete next-step (no fabrication). The W machinery
  (`haipipe-insight-wisdom` + `card-creator-wisdom-agent` + `invocation-modes`
  W row) was already correct — only the probe-loop wiring was missing.
- The probe-cycle deliverable is now **🟨 K + 🟧 W** end-to-end; the
  narrative-cycle gets both the claim and the recommended next whip-crack.

### Changed
- Distinction made explicit: **per-probe W** (single-K next-step, filed in the
  loop) vs **strategic W** (across many K, stays cross-cycle via the report
  phase / `haipipe-insight-explore`).
- Docs threaded: `06-probe-cycle.txt` step ⑥ + gates table, `00-index.txt`,
  `07-end-to-end-claim-gap.txt`, `ARCHITECTURE.md`, `DESIGN.md` Q2 (which still
  described the pre-K-fix `card-creator-data-agent` dispatch — corrected to
  knowledge→wisdom).

### Verified
- **Dogfood-verified** on the stub (`/tmp/haipipe-dogfood/`): confirmed probe →
  K01 → **W01** ("param-matched FiLM re-test"). 13/13 `card-reviewer-wisdom`
  gates + 5/5 `index-integrity` gates green on an independent re-run (reciprocal
  K01↔W01 back-link, INDEX consistency, schema sections/enums, type/cost enums,
  actionable `/haipipe-probe` command, boundary = action-not-restated-belief).


## [2.3.2] — 2026-05-31

### Fixed
- **K now sources the confirmed probe's `claim`**, not `≥1 I card`. The
  `haipipe-insight-knowledge` skill + `card-creator-knowledge-agent` +
  `ref/invocation-modes.md` (K row) now take a `probe_ref` (status==confirmed);
  the probe's `claim` becomes the K, `caveats` → counter-evidence, supporting
  I cards cited in the body. This matches `ref/insight-md-schema.md` (which
  already said K sources = confirmed probe) and unblocks a single probe-cycle
  from reaching K (the I-chain needs ≥2 D, which one cycle can't produce).
- `probe-loop` convergence dispatches `card-creator-knowledge-agent` (the K),
  closing the probe-cycle with its actual deliverable.
- `dikw-boundaries.md`: K boundary + worked example now source the probe.
- **Dogfood-verified** on a stub (confirmed probe → K01; all gates passed).


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
  closing the probe cycle (`probe → task → insight`, L0) the loop previously left open.

### Notes / remaining
- Higher-layer I/K/W auto-synthesis (as D cards accumulate) is NOT per-probe —
  deferred to the report phase / `haipipe-insight-explore`.
- Known model↔skill tension: `haipipe-insight-data` sources a D card from a
  *confirmed probe* (not a task); the loop wiring matches the skill as-built.
  A "D-from-task" reconciliation is a future pass.
