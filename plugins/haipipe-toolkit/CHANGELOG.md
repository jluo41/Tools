haipipe-toolkit — Changelog
===========================

Plugin-level rollup. Per-layer detail lives in each layer's own
`skills/<LAYER>/CHANGELOG.md`. Newest first.


## [2.3.2] — 2026-05-31

Fix: a probe-cycle now files its claim as a 🟨 K card (was a 🟦 D card).

- **K sources the confirmed probe's `claim`** (not `≥1 I card`). The skill prose
  contradicted the schema — which already said `K sources = confirmed probe` —
  and a single probe-cycle could never reach K through the I-chain (I needs ≥2
  D). Fixed in `haipipe-insight-knowledge`, `card-creator-knowledge-agent`,
  `ref/invocation-modes.md`.
- **probe-loop convergence now dispatches `card-creator-knowledge-agent`**
  (files the K from the claim), not `card-creator-data-agent`. The 🟦 D
  observations come from the probe's task-cycles; 🟩 I / 🟧 W are cross-cycle.
- **Dogfooded** on a stub project (confirmed probe → K01): all
  card-reviewer-knowledge gates + index-integrity passed.
- Docs threaded: `dikw-boundaries.md` (K source = confirmed probe) + `06-probe-cycle.txt` Ⓕ.
- Still pending: the `D-from-task` reconciliation (data skill still reads a probe).


## [2.3.1] — 2026-05-31

Vocabulary + a probe-cycle process doc (docs only).

- **Cycle vocabulary unified** — the three nested units are now
  **narrative-cycle ⊃ probe-cycle ⊃ task-cycle** (renamed from the earlier
  "stage / atom" mix). `L0–L3` stay as loop-level labels.
- **`diagram/v260531/06-probe-cycle.txt`** (new) — the canonical 6-step process
  for running ONE probe cycle (design → bridge → run×N → result → verdict →
  insight), its 4 gates, and the two drive modes. `02` reframed as the
  probe-cycle *anatomy*; `03` as the *nested cycles*; `05` renamed
  `roles-and-stage` → `roles-and-cycle`. Threaded through DESIGN / HANDOFF /
  both CHANGELOGs / probe-loop.


## [2.3.0] — 2026-05-31

The E_insight agent skeleton — E gets the `agents/` + dual-mode parity C_task
and D_probe already had, with a deliberate per-type-reviewer twist.

### Highlights
- **E_insight agentified** — `agents/creators/` (4, one per DIKW layer; each a
  thin headless wrapper over `haipipe-insight-<layer>`) + `agents/reviewers/`
  (**per-type**: `card-reviewer-{data,information,knowledge,wisdom}-agent`, each
  enforcing that card's accuracy + boundary, plus a cross-layer
  `index-integrity-auditor`). A deliberate departure from C/D's type-agnostic
  reviewers — each DIKW card has a genuinely different boundary.
  → see [skills/E_insight/CHANGELOG.md](skills/E_insight/CHANGELOG.md)
- **`ref/dikw-boundaries.md`** — canonical per-layer boundary + the two
  promotion gates + a worked D→I→K→W example; creators follow it, reviewers
  enforce it.
- **Dual-mode DIKW skills** + `ref/invocation-modes.md` — the 4 filer skills run
  interactive OR headless (full spec → silent), chosen by input completeness.
- **Loop closure** — `haipipe-probe-loop` now dispatches `card-creator-data-agent`
  on convergence, filing the D card and closing the probe cycle
  (`probe → task → insight`) the loop previously skipped.
- **Agent registry** 13 → 22 (E adds 9: 4 creators + 5 reviewers).

### Layer changelogs touched this release
- [E_insight](skills/E_insight/CHANGELOG.md) — NEW: agent skeleton, dual-mode, per-type reviewers, dikw-boundaries


## [2.2.0] — 2026-05-31

The E_insight design + research-engine model release. **Design-only** — no
new runtime skills built yet; this records the design + the mental model so
the build has a stable target.

### Highlights
- **E_insight `DESIGN.md`** (`skills/E_insight/DESIGN.md`) — E finally gets
  the skeleton C_task/D_probe already have, applied THOUGHTFULLY (as D_probe
  departed from C_task): dual-mode invocation (= C_task's
  `ref/invocation-modes.md`), `creators/` per DIKW (the headless,
  agent-callable filing path), and `reviewers/` = E's unique `card-fidelity`
  (Codex) + `index-integrity` gates. Templates + agents NOT built yet.
- **Loop-closure finding** — `haipipe-probe-loop` never files insight: the
  probe cycle (`probe → task → INSIGHT`) has an empty last cell. E's headless creators
  are what close it; the loop is WHY filing must be headless.
- **Research-engine model, versioned** — `diagram/v260531/` (6 files): the
  hourglass (decompose ↓1:n / aggregate ↑n:1); the 5 roles (🥢 ask=领导/nudge ·
  📖 narrative=办事的人/brain · 🔧 probe=whip · ✋ task · 🧠 insight); "one
  stage" = one narrative turn; the probe·task·insight distillation chain.
  Vocabulary pinned: **whip** (挥鞭), not "wipe"; narrative is the brain
  (delegates execution, never runs compute).
- **HANDOFF.md** rewritten to resume from this converged model.


## [2.1.0] — 2026-05-31

The C_task "creator + reviewer agents" release: a clean split between thin
per-type builder agents and shared type-agnostic reviewer gates, dual-mode
skills, batch fan-out, and a notebook-bloat policy.

### Highlights
- **C_task agent families** — `creators/` (7 per-type thin builders,
  `code-creator-for-<type>-agent`) + `reviewers/` (2 fixed, type-agnostic
  gates). builder ≠ judge; the creator that writes code never reviews it.
  → see [skills/C_task/CHANGELOG.md](skills/C_task/CHANGELOG.md)
- **Skills renamed** `haipipe-task-<type>` → `haipipe-task-for-<type>` (7
  types; router + logging unchanged), matching the `code-creator-for-<type>`
  naming.
- **Dual-mode skills** — one body, interactive (human steers) OR headless
  (agent passes a full spec → runs silent), chosen by input completeness;
  structured return so an agent caller can locate the scaffolded folder.
- **Knowledge centralized in `ref/`** — `authoring-conventions.md` (shared) +
  `invocation-modes.md` (dual-mode contract). Skills and agents both stay thin;
  knowledge has ONE home.
- **Batch fan-out** — `haipipe-task-batch` skill + Workflow `pipeline`
  (`batch-pipeline.workflow.js`): N typed specs in one session, each flowing
  author → GATE 1 → run → GATE 2 independently; GPU-safe (`autoRun` default off).
- **Notebook policy** — `_meta.notebook: full | thin | off` knob in
  `run-sh-template.sh`; heavy compute (training/data) defaults to `thin`;
  `notebooks/` + `_WorkSpace/` default-gitignored.
  → see [skills/B_project/CHANGELOG.md](skills/B_project/CHANGELOG.md)
- **Per-run quality moved C ← D** — the per-run sanity checklist now lives with
  `run-result-auditor-agent` (C_task GATE 2); `D_probe review run` delegates.
  → see [skills/D_probe/CHANGELOG.md](skills/D_probe/CHANGELOG.md)
- **D_probe agent families (lighter pattern)** — `reviewers/` (structural +
  integrity-Codex + claim-Codex) and `advancers/` (explorer). Deliberately NO
  `creators/`: D_probe's builders stay interactive skills (probe design needs
  steering; no type axis; parallelism is downstream in C_task). The same
  builder≠judge method, applied to a low-volume deliberate layer.
  → see [skills/D_probe/CHANGELOG.md](skills/D_probe/CHANGELOG.md)

### Layer changelogs touched this release
- [C_task](skills/C_task/CHANGELOG.md) — agents, skill renames, dual-mode, batch, notebook knob
- [D_probe](skills/D_probe/CHANGELOG.md) — per-run checklist delegated to C_task; bridge dispatch
- [B_project](skills/B_project/CHANGELOG.md) — notebook retention + gitignore guidance


## [2.0.0] — prior

Baseline at the start of this changelog: Tier-1 umbrellas
(/haipipe-data, /haipipe-nn, /haipipe-end, /haipipe-project, /haipipe-individual)
dispatching to per-stage / per-target Tier-2 specialists across stages 0–6.
