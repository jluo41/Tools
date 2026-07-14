probe - Changelog
===================

Layer-scoped changelog for the probe (PROBE / claim) layer. Newest first.
Rollup lives in the plugin-level `CHANGELOG.md`.


## [6.0.0] — 2026-07-14 — THE PROBE BECOMES A PAPER-LEVEL Q/A MAP; the gateway is retired

Ruling: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` v3 — APPROVED by JL 2026-07-14, R1–R18. That document is the
SPEC OF RECORD for this layer; the per-skill changelogs carry the detail.

The layer's shape, in one diagram:

```text
   📄 CONSUMER (paper / application)                  ⚙️ BANK (probe-UNAWARE)
   papers/<P>/1-probes/PPNN_<topic>.md                tasks/<leaf>/ · discoveries/<leaf>/
   one file per TOPIC · one SECTION per question      own plan.yaml|discovery.yaml
   (serves/target/state/commission/reading)           own results/|sources.md
   + one '## Why' — the stake, never leaves           + OPTIONAL QA/<n>-<slug>.md
        │                                                       ▲
        │  ③ DISPATCH the commission VERBATIM, DIRECT ──────────┘
        │     Agent(haipipe-task-orchestrator-agent)
        │     Agent(haipipe-discovery-orchestrator-agent)
        └─ binds by PATH (target:) — no PP id ever crosses
```

What changed
- **A probe is a PAPER-LEVEL DOCUMENT**, not a folder and not a card: `1-probes/PPNN_<topic>.md`,
  one file per topic, one SECTION per question. Binding is by PATH (R1) — PP numbers are
  consumer-local footnote numbers, so there is no ledger and nothing to renumber.
- **The bank is PROBE-UNAWARE** (R2). It answers plain questions through its own `qa` verb
  (`/haipipe-task qa`, `/haipipe-discovery qa`) and returns `<leaf>/QA/<n>-<slug>.md`.
  The probe CAUSES a QA file; the EXECUTOR authors it (CC-8).
- **The two LAWS**: a consumer session NEVER executes bank work inline (dispatch only); lint both
  surfaces (commission blocks; bank QA files) for consumer vocabulary.
- `haipipe-probe` → **8.0.0** (the constitution: probe file anatomy, path binding, the QA/
  contract, the qa verb, the five-step loop ORGANIZE→MATCH→DISPATCH→POINT→INTERPRET, the cost
  ladder, status derivation, the writer table).

RETIRED (see `PART 9` of haipipe-probe/SKILL.md — the full do-not-resurrect list)
- **`haipipe-probe-orchestrator-agent` — the evidence GATEWAY.** Archived + de-registered. Its
  SWEEP became the consumer-side MATCH; its dispatch is now a direct `Agent()` call on the two
  executor orchestrators. It was a third clean context in front of two that already had one.
- `1-probe-plans/` → `1-probes/` · PPNN "cards" → probe FILES · `_ASK/`+`_ANS/` stubs · the
  `answers:` field · the `asks` verb (reborn probe-unaware as `qa`) · `## Verdict` + the
  `verdicted` state · `status:` → `state:`.

SURVIVING, and repaired in the same pass — the claim-judging path, which still runs
- `haipipe-probe-review` → **2.1.0** and `haipipe-probe-reviewer-agent` → **4.1.0**. The JUDGMENT
  is unchanged (G1 structural · G2 integrity with the deterministic `g2_integrity_check.py` and
  its >95 / 80–95 / <80 thresholds · G3 claim · the confidence scale · the `associational |
  causal` guard). Two things moved, and both files still described the dead world until now:
  their **CALLER** (the gateway was their only declared dispatcher — they had none; it is now the
  consumer's PROBE-phase worker at ⑤ INTERPRET, `mode: full`) and their **LANDING SITE** (the
  judgment lands in the consumer's `0-lifecycle/1-claims/1-claims.md`, per-claim, per-consumer,
  private — never in a probe file).
- 产审分离 is preserved and now better grounded: the EXECUTOR assembles the evidence in its own
  probe-unaware session, and a SEPARATE fresh-context reviewer grades it.
- ⚠️ A DISCOVERY's own `verdict.md` terminal file is executor-native and SURVIVES. It is not the
  retired `## Verdict` block; do not delete or rename it.

## [5.2.0] — 2026-07-06 — Judgment process becomes a SKILL: haipipe-probe-review

JL ruling: "haipipe-probe-review可以被新的agent call，但是我们还是需要一个skill来规范流程；haipipe-probe就只保留 reviewer之外的内容."

- NEW skill `haipipe-probe-review/` 1.0.0 — the governed G1/G2/G3 rulebook (gate substance, g2 thresholds, verdict vocabulary, return contract), extracted from the reviewer agent 2.1.0 body. Normal path: invoked headless by the reviewer agent; direct call only with a complete claim + refs spec. Writes nothing.
- haipipe-probe-reviewer-agent → 3.0.0 thin shell: claim + refs in → Skill(haipipe-probe-review) → judgment returned as text. Skill added to tools. Two-tier review model unchanged (per-layer artifact reviewers vs this claim-level judge).
- Instruments moved `agents/` → `haipipe-probe-review/`: g2_integrity_check.py + probe-caveats-checklist.txt (the skill owns its own docs).
- haipipe-probe → 6.2.0: keeps everything EXCEPT the judgment process (layer contract, PPNN card anatomy incl. where the verdict LANDS, DIRECT ASK); judge references now point at the sibling skill. Gateway → 2.0.3 (Step 3 names the rulebook).
- `.claude/skills/haipipe-probe-review` symlink registered.

## [5.1.1] — 2026-07-06 — Reviewer agent body folderless-native (closes the [5.1.0] follow-up)

- haipipe-probe-reviewer-agent 2.1.0: rewrote the body off the folder era. Removed the pre-Judge creator-loop gates (Plan review of probe.yaml, Gather/Read review of evidence.md — none of those artifacts exist folderless) and every "write verdict.md / set probe.yaml.verdict" instruction. G1/G2/G3 now RETURN their results as text; the gateway carries the return and the caller lands it in the PPNN card `## Verdict`. Reconciled the G3 verdict vocabulary to the PPNN card's `supported | refuted | inconclusive` (was `yes | partial | no | blocked`). Gate check-substance is unchanged: G1 structural checklist, G2 five fraud-patterns + g2_integrity_check.py thresholds (>95 pass / 80-95 warn / <80 fail), G3 scope / caveats / confidence.


## [5.1.0] — 2026-07-06 — Archive pass (folder-era content off the live surface)

Moved to `_archive/` (folder-era history; live contract = haipipe-probe/SKILL.md + the two agents):
- DESIGN.md, PHILOSOPHY.md, MENTAL_MODEL.md, SKILLSET_REVIEW.md — four folder-era prose docs (~1,100 lines) that still sat at the bucket surface under HISTORICAL banners; DESIGN's Authority block had pointed at the deleted ref/ + fn/.
- agents/CODE_REVIEW.md — one-time 2026-06-23 review of the old agents.
- haipipe-probe/diagram/03-probe-aware-entrypoint.txt — folder-era sketch (minimap / arms / Return vocab); empty diagram/ removed.
- agents/_old/ → _archive/_old/ — creator + the 3 pre-merge Judge reviewers.
- agents/feedback/ → _archive/agents-feedback/ and haipipe-probe/feedback/ → _archive/skill-feedback/ — folder/Codex-era lesson inboxes, already digested into the refactor.
- _archive/README.md added: provenance table + "not current" banner.

Changed
- agents/README.md rewritten off the folder-era roster (creator-as-live, the 5-stage folder lifecycle, dead ../fn/ ../ref/ pointers) to the two live agents + the folderless dispatch flow.
- haipipe-probe/SKILL.md: the lone live pointer repointed `../DESIGN.md` → `../_archive/DESIGN.md`.

Live surface now = CHANGELOG.md + SOP-folderless-refactor.md (transient) + agents/ (2 agents, g2 script, checklist, README) + haipipe-probe/ (SKILL, CHANGELOG, PREFERENCES).
Follow-up flagged (not touched): haipipe-probe-reviewer-agent.md body (lines 49-186) is still folder-era procedure under a "treat-as-legacy" disclaimer — a folderless rewrite of its gate sections is the next cleanup.


## [5.0.0] — 2026-07-05 — FOLDERLESS REFACTOR

Removed (JL: probes/ duplicated the paper-side _PROBE card — 不是 single source of truth)
- probes/ folders (probe.yaml, evidence.md, status.md, verdict.md): the consumer's per-stage _PROBE/PPNN card is now the single home for contract + receipt + verdict (## Verdict section, full mode). Legacy folders stay on disk read-only; SWEEP may read, nothing writes.
- Probe Console (interactive; .probe-console.yaml): panel duties folded into /haipipe-paper enter.
- haipipe-probe-creator-agent → agents/_old/ (its three outputs no longer exist; linking absorbed by the gateway, presentation by the return contract).

Changed
- haipipe-probe-orchestrator-agent 2.0.0 = evidence gateway: SWEEP over discoveries/tasks/insights, shape reuse|enrich|fresh, zero writes anywhere (Write/Edit removed — executes the long-recorded 4.3.0(7) decision, resolving the open C1 thread as A). All run-earned discipline retained (project-local sweep, trust-the-ledger, shape honesty, fresh-must-land, no inline searching, bg dispatch, batch, lean boot).
- haipipe-probe-reviewer-agent 2.0.0: judges claim + evidence refs; G1/G2/G3 + verdict RETURNED as text, landed by the caller's TRANSLATE.
- haipipe-probe SKILL.md 6.0.0: thin layer-contract doc (PPNN card anatomy, dispatch map); fn/ + ref/ marked LEGACY (G-gate definitions still referenced by the reviewer).

## [4.0.0] - 2026-06-22

### Changed
- Reframed around the **Probe Console** + concise lifecycle
  **Plan → Gather → Read → Judge → Return**; flat probe folders; group folders removed.
- `probe-aware no-arg dashboard` (`ref/probe-dashboard.md`) and the scattered-work
  **filing judge** (`ref/probe-attach.md`, `/haipipe-probe file`) added.

### Removed (v3 supporting layer that no longer fit)
- `ref/`: probe-lifecycle.workflow.js, probe-status-template.txt,
  probe-run-dashboard-template.txt, probe-cycle-audit-template.txt,
  probe-headline-template.txt, probe-entry-template.txt, workflow-plan-sample.yaml,
  _legacy-scope-expmt.md, log-format.md (all orphaned; superseded by lifecycle-map + dashboard).
- `fn/`: design.md, bridge.md, harvest.md (were full v3 bodies mislabeled "aliases";
  routing now maps legacy verbs to the v4 procedures).
- specialists `haipipe-probe-inspect/` and `haipipe-probe-explore/` (dropped from v4 commands;
  status→Console/dashboard, unused→dashboard UNLINKED EVIDENCE).
- agents: probe-idea-creator, probe-idea-reviewer (no auto Plan mode), probe-explorer
  (no explore command). Kept the 3 Judge reviewers and wired them into fn/judge.md.
- diagrams 01-probe-lifecycle, 02-three-layer-pyramid.

### Fixed
- Plugin top-level `agents/` symlinks for the 3 probe reviewers were dead
  (`../skills/D_probe/...` after the D_probe→probe rename); repointed to `../skills/probe/...`.


## [2.0.0] - 2026-06-11

### Added
- **IPO workflow adoption.** probe now follows the haipipe-workflow (project)
  IPO pattern - the same universal unit that task adopted for task folders.
  - `ref/workflow-plan-sample.yaml` - the probe lifecycle as an IPO plan template.
    6 domain phases (Design → Bridge → Run → Aggregate → Review → Claim), each
    with steps declaring `files_in` / `files_out`. Follows `plan-schema.md`.
  - `haipipe-probe/ref/probe-lifecycle.workflow.js` - the 4-stage lifecycle
    (Plan → Build → Execute → Report) wrapping the 6 domain phases. Plan creates
    the probe plan; Build executes Design + Bridge; Execute runs Run + Aggregate +
    Review + Claim; Report mirrors the plan with results.
  - Lifecycle section added to `haipipe-probe/SKILL.md` showing the mapping:
    Plan → Build (Design + Bridge) → Execute (Run + Aggregate + Review + Claim)
    → Report.

### Notes
- The 4-stage lifecycle is the same universal wrapper from task/haipipe-workflow.
  The 6 domain phases are probe-specific - not copied from task. task's eval
  task has Load/Score/Compare/Emit; probe has Design/Bridge/Run/Aggregate/Review/Claim.
- Builder asymmetry preserved: Design, Bridge, Result remain interactive skills in the
  workflow.js (not creator-reviewer agent loops). Reviewer agents run in the Review
  domain phase (P5), gated sequentially (structural → integrity → semantic).
- No per-probe `workflow/` folder - probe.yaml is already the plan (hypothesis + arms +
  aggregation), and CYCLE.md (from inspect cycle) is the report. The workflow-plan-sample
  serves as the reference template; probe-lifecycle.workflow.js is shared across probes.


## [Unreleased] - 2026-05-31

### Added
- **Agent families (lighter than task, by design).** New `agents/`:
  - `reviewers/` (3): `probe-structural-reviewer-agent`,
    `probe-integrity-auditor-agent` (Codex), `claim-verifier-agent` (Codex) -
    the three honesty checks as independent, dispatchable subagents
    (builder ≠ judge). Thin pointers to `haipipe-probe-review/SKILL.md` +
    `ref/` (no duplicated checklists/prompts).
  - `advancers/` (1): `probe-explorer-agent` - probe's unique third family
    (proposes research direction; task has no analog).
  - Registered as flat symlinks under the plugin top-level `agents/` for
    `subagent_type` dispatch (by `haipipe-probe-loop`, `application`).
- **Intentional asymmetry vs task: NO `creators/`.** probe's builders
  (`design`, `result`, `bridge`) STAY interactive skills - designing a probe
  needs human steering and there is no task-type axis to fan out; probe
  parallelism lives downstream in task (via the bridge). Documented in
  `agents/README.md`.
- Wiring notes added to `haipipe-probe-review` (three checks ↔ three reviewer
  agents) and `haipipe-probe-explore` (↔ probe-explorer-agent).

### Changed
- **Per-run quality is no longer owned here.** The per-run sanity checklist
  (runtime.status / exit_code / git_sha / metrics.json parseable / heavy-artifact
  placement) moved to the task unified reviewer `haipipe-task-reviewer-agent`
  (GATE 2). `haipipe-probe-review` `review run` now DELEGATES to that agent
  instead of re-implementing the checklist - single source of truth. "Did THIS
  run produce a trustworthy artifact?" is a task question; probe only
  consumes the verdict. The per-probe checklist's line now reads "all linked
  runs pass haipipe-task-reviewer-agent GATE 2 (task)".
- **Bridge dispatch updated.** `haipipe-probe-bridge` Step 3 invokes the task
  reviewer by reading `skills/task/agents/haipipe-task-reviewer-agent.md` and
  handing its body to a Task subagent (the agent is a role-doc invoked by path,
  registered at the plugin top-level `agents/` for `subagent_type` addressing).

### Notes
- Integrity audit (5 fraud patterns) and claim verdict remain Codex-backed
  judgments inside `haipipe-probe-review` - unchanged this round.
