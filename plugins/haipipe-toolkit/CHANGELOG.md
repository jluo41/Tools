haipipe-toolkit — Changelog
===========================

Plugin-level rollup. Per-layer detail lives in each layer's own `skills/<LAYER>/CHANGELOG.md`. Newest first.

## [Unreleased] — 2026-07-26 — Board becomes a first-class family

- Promoted `haipipe-board` from `skills/0_utils/` to
  `skills/board/haipipe-board/`, parallel to paper, probe, and task.
- Added `skills/board/agents/haipipe-board-reviewer-agent.md`, a read-only
  fresh-context judge for mechanical, readability, and visible-staleness checks,
  and registered it through the plugin's top-level `agents/`.
- Kept all working design Boards in `skills/diagrams/`; no diagram folder moved.
- Repointed the Paper lifecycle integration, HAIChat Board API, live Board
  links, top-level structure documentation, and installed Claude/Codex skill
  symlinks to the new path.
- Made Paper Enter the single composed door: it rebuilds/opens the first-class
  Board, stores only paper identity, derives the frontier from artifacts,
  S-page state, and actor/date gate receipts, and leaves phase/gate history in
  each owning S page's `## Log`.
- Unified evidence execution on one path: DRAFT raises Q-consumers, PROBE owns
  the five-step loop, and only the isolated q-executor collector calls the
  task/discovery orchestrators. Deferred work now needs a real deferred entry,
  so a prose-only Venue deferral cannot pass vacuously.
- Unified Resource on its stage-owned `Resource Description` + `Q-consumer`
  schema across DRAFT, Lifecycle, Enter, and CHECK.
- Made CHECK resolve the authoritative `stages/<order>-<key>/stage.md`, added
  Venue's no-REVISE gate path, and made Venue resolve both labelled `style:`
  and `template:` paths for every section kind.
- Clarified the probe wall: the original stake may survive only in the
  review-only q-consumer copy; q-executor, a-executor, collector payloads,
  bindings, and bank files remain clean. Canonicalized the paper-only terminal
  `concern` state while preserving the universal four-subsection anatomy.
- Completed the Board-first adapter: a stage template's logical Q-consumer is
  now generated and operated as checklist records in `## Items to Finish`,
  never as a duplicate block under `## Content`; all 95 venue section
  templates use the same record and current DRAFT→PROBE→REVISE→CHECK sequence.
- Made the stage page generator merge Setext overview divisions with ATX
  paragraph divisions, so venue-specific section templates retain both the
  structural overview and prose scaffold while keeping Q records Board-only.
- Tightened executable probe validation: a terminal `concern` now requires
  exactly `route: none`, rejects bank/target/returned-answer fields and
  non-consumer stake leakage, while valid normal and declared-deferred entries
  continue to pass. Deferred declarations are resolved from the paper root.
- Made the stage-contract checker reject retired `0-sections/` and
  `0-displays/` field values instead of accepting them as resolvable paths.
- Aligned delivery with the new control plane: Folder creation routes through
  confirm-gated Enter, Display owns its gallery exception in `3-display/`, and
  Compile resolves explicit, Display, or full-paper targets while keeping
  compiler success separate from Board approval.

## [Unreleased] — 2026-07-14

**PROBE LAYER v3 — the probe becomes a paper-level Q/A map; the bank becomes probe-unaware.**
Spec of record: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` (APPROVED by JL 2026-07-14, rulings R1-R18). The operative
form is `skills/probe/haipipe-probe/SKILL.md` v8.0.0 — the constitution; where any doc disagrees
with it, it wins.

The model in one paragraph. A PROBE is a PAPER-LEVEL DOCUMENT and nothing else:
`papers/<P>/1-probes/PPNN_<topic>.md` (and `applications/<A>/1-probes/`, same shape). One file
per TOPIC; each question the DRAFT stage raised is ONE SECTION (`serves:` / `target:` / `state:`
/ `commission:` / `reading:`), plus ONE `## Why` per file holding the stake, which never leaves
the file. **Binding is by PATH, never by id** (R1): PP numbers are paper-local footnote numbers,
so two papers may both carry a PP04 and nothing collides — no PP id ever crosses to the bank.

The bank (`tasks/` + `discoveries/`) is **PROBE-UNAWARE** (R2): no `_ASK/`, no `_ANS/`, no
`answers:` field, no PP id anywhere. It answers plain questions through its own new `qa` verb
(R11) — `/haipipe-task qa "<question>" [<leaf>]` and `/haipipe-discovery qa` — which gates
① QA SCAN → ② DIGEST → ③ P-B-E-R (or 🚫 REFUSE) and returns `<leaf>/QA/<n>-<slug>.md`: the
executor's READABLE digest, numbered so `ls QA/` IS the index (R9, both banks). The `qa` verb has
THREE callers: a human exploring, the orchestrator itself (self-directed answerability work), and
a paper's probe DISPATCH (R18). **The probe CAUSES a QA file; the EXECUTOR AUTHORS it** (CC-8).

TWO SESSION MODES (R17): the LEFT executor session runs P-B-E-R for its own sake — the bank grows
autonomously — and only the RIGHT consumer session asks. So most probes should land on T2 REUSE
and a commission is the EXCEPTION, not the norm.

TWO LAWS. LAW 1: a consumer session NEVER executes task/discovery work inline — dispatch means
handing the `commission` block, VERBATIM, and nothing else (never `## Why`, never the probe file,
never the paper). LAW 2: backstop lint on two surfaces — probe commissions carry no `C\d`/`H\d`/
stake words; bank `QA/*.md` carry no consumer vocabulary.

RETIRED / DELETED:
- `haipipe-probe-orchestrator-agent` (the evidence GATEWAY) — archived + de-registered. Its SWEEP
  became the paper-side MATCH; its dispatch is now a DIRECT `Agent()` call on
  `haipipe-task-orchestrator-agent` / `haipipe-discovery-orchestrator-agent`, whose clean context
  IS the wall. SURVIVING: the `haipipe-probe-review` skill + `haipipe-probe-reviewer-agent`
  (paper-side claim judging).
- `_ASK/` + `_ANS/` mailboxes · the `answers:` return field · `probes.ledger` · project-unique PP
  ids · the probe-aware `asks` verb (reborn probe-unaware as `qa`) · "Verdict" / `verdicted` as a
  probe term (claim status now lives in `1-claims.md`, per-claim, per-paper, private).
  ⚠️ A DISCOVERY's own `verdict.md` (the Review-type terminal file) is a DIFFERENT thing and it
  SURVIVES.
- Vocabulary: `card` → **probe** (allowlist rename only — ~90 of 941 uses in this repo mean other
  things: poster card styles, venue-ui-card, KPI cards, `_CITATION_` cards, "model card").
  `1-probe-plans/` → `1-probes/`. "row" / "table" → BANNED; say **Q-paper** / **SECTION**.
  "Takeaways" → `reading`. `check-probe-cards.sh` KEEPS its filename (65 refs / 33 files); only
  its internals were rewritten.

Root docs rewritten to v3: `ARCHITECTURE.md` (the probe section, the writer table, the two session
modes, the five-step loop, the cost ladder, the two LAWS, status derivation, the project layout —
`QA/` in, `_ASK/` out), `skills/STRUCTURE.md`, `README.md` (the research-axis verbs + glossary),
`USAGE.md` (the whole probe.yaml-era recipe book replaced: the 4 worlds, the qa verb, the probe
loop; the dangling `MENTAL_MODEL.md` / `probe-yaml-schema.md` / `fn/bridge.md` refs removed).

Cross-cutting sweep (surfaces outside the layer buckets):
- `skills/0_utils/haipipe-run-timeline/SKILL.md` 1.0.0 → **1.1.0**. Its worked example dispatched
  the retired gateway agent and wrote a `probe.yaml`. Re-cut to the live doors (direct
  `haipipe-task-orchestrator-agent` / `haipipe-discovery-orchestrator-agent`, ending in a
  `<leaf>/QA/<n>-<slug>.md` write), plus a new LAW-1 audit rule: **a Write into `tasks/` or
  `discoveries/` from the consumer lane (L0) is the leak this timeline exists to catch.**
  (The `0_utils` bucket keeps no CHANGELOG.md of its own; the bump is recorded here and in the
  skill's `metadata.summary`.)
- `skills/insight/README.md` + `CHANGELOG.md` — the tombstone stays retired; only its forward
  pointers were corrected. They named the PPNN card's `## Verdict`, the `_ASK/` stub chain, and
  the gateway SWEEP — all three now dead. K now splits (general FACT → the executor's QA file;
  paper-specific JUDGMENT → `1-claims.md`); W is a probe SECTION reaching the `qa` verb;
  cross-consumer reuse is a plain grep of the bank's QA corpus.
- **`agents/` (plugin root) — 12 of 14 registrations were DANGLING symlinks; removed.** All 12
  pointed at RETIRED agents whose sources no longer exist at the linked path: the 8 insight
  `card-creator-*` / `card-reviewer-*` agents + `index-integrity-auditor-agent` (moved to
  `skills/insight/_archive/` on 2026-07-12 and de-registered from `~/.claude/agents/`, but never
  from HERE), and `claim-verifier-agent` / `probe-integrity-auditor-agent` /
  `probe-structural-reviewer-agent` (the three Judge agents merged into
  `haipipe-probe-reviewer-agent` on 2026-06-23; their `skills/probe/haipipe-probe/agents/` source
  folder is long gone). A broken symlink in a registration directory is not history — history
  lives in `_archive/` and in CHANGELOGs. This enforces the standing rule stated in
  `skills/probe/agents/README.md`: **anything under `_archive/` is NEVER registered.** Two live
  registrations remain: `haipipe-task-creator-agent`, `haipipe-task-reviewer-agent`. (Predates the
  probe v3 work — found by its cross-cutting sweep.)

Per-layer detail: `skills/probe/haipipe-probe/CHANGELOG.md`, `skills/probe/agents/CHANGELOG.md`,
`skills/task/haipipe-task/CHANGELOG.md`, `skills/discovery/haipipe-discovery/CHANGELOG.md`,
`skills/paper/…`, `skills/application/…`, `skills/project/CHANGELOG.md` (3.2.0).


## [Unreleased] — 2026-07-03

Discovery layer v2.5.0: type specialist skills haipipe-discovery-search /
-review / -idea created, one heading each bucket (mirrors haipipe-data-source
etc.); orchestrator Execute dispatches them; Review Output Contract moved into
haipipe-discovery-review. Also the never-tables-for-papers rule applied across
all worker output formats, layer docs made self-contained (no upper-layer
mentions), concrete example slugs. Detail: `skills/discovery/haipipe-discovery/CHANGELOG.md`.

Discovery layer v2.4.0 (JL simplification pass, same day as v2.3.0 below):
novelty_check re-typed Review -> Idea (buckets = types exactly 1:1);
parent:/consumed_by: removed — discovery is probe-UNAWARE, references point one
way downward (the probe organizes and records links on its side); folder
contract slimmed to discovery.yaml + evidence files (status.yaml/site.md
dropped; report: block appended at Report). Schema doc rewritten lean.
Detail: `skills/discovery/haipipe-discovery/CHANGELOG.md`.

Discovery layer v2.3.0: buckets 4 -> 3, one folder per type, English-only.

- Merged `skills/discovery/2_read/` into `1_search/`; renumbered `3_review/` ->
  `2_review/` and `4_idea/` -> `3_idea/`. Each type (Search/Review/Idea) now maps
  1:1 to its Execute bucket; `novelty-check` stays in `3_idea/` (serves
  Review-judge, the one documented exception).
- Purged residual 搜/析/创 from DESIGN.md, agents/, and live docs (the v2.1.0
  English rename had missed them); backfilled 2.1.0/2.2.0 changelog entries.
- Removed dangling references (0_venue/, D_patent/, /idea-discovery,
  /research-pipeline, /patent-pipeline, agents' fn/plan-build-execute-report
  reads) and a stray self-symlink; synced the codex-plugins mirror (moot hours
  later: a parallel session deleted the whole codex-plugins/ tree from the
  working copy the same day).
- Detail: `skills/discovery/haipipe-discovery/CHANGELOG.md`.


## [Unreleased] — 2026-06-21

Structure: moved numbered task-domain families under `skills/task/` while
keeping all skill names and slash commands unchanged.

- Moved `skills/{1_data,2_nn,3_end,4_individual}/` to
  `skills/task/{1_data,2_nn,3_end,4_individual}/`.
- Kept `/haipipe-data`, `/haipipe-nn`, `/haipipe-end`, and
  `/haipipe-individual` stable; skill identity still comes from each
  `SKILL.md` frontmatter `name:`.
- Updated plugin docs, task design notes, diagrams, and stale individual-skill
  path references.

Structure: discovery layer renamed and the narrative layer retired in discovery docs.

- Renamed `skills/discover/` to `skills/discovery/` so the layer concept reads
  as a noun, matching the `discoveries/` artifact dir and the task/probe/insight
  siblings. The skill was then also renamed `haipipe-discover` -> `haipipe-discovery`
  (haipipe-<noun> convention); the command is now `/haipipe-discovery`.
- Retired the narrative parent in the discovery docs: a discovery now has two
  parents only, a delivery lifecycle (`paper`/`application`) for L* landscape /
  novelty work and a `probe` for claim-level evidence. Story-side dispatch moved
  from Narrative-open to Delivery-open.
- Recast the discovery model: a discovery is one research topic = its own FOLDER
  (`discovery.yaml` + `sources.md`/`notes.md`/`verdict.md` + `status.yaml`/
  `site.md`), mirroring a task-folder; reverted v1.5's single-file default, which
  the dry-run fixture and blueprint never followed.
- Added `skills/discovery/haipipe-discover/ref/lifecycle-map.md`, the canonical
  lifecycle table (`open -> search -> read -> review/idea -> post`, each stage
  filling one IO file), isomorphic to the probe lifecycle map; SKILL.md and
  DESIGN.md point to it instead of restating it. Added
  `skills/discovery/haipipe-discovery/CHANGELOG.md` for layer parity. → see [skills/discovery/haipipe-discovery/CHANGELOG.md](skills/discovery/haipipe-discovery/CHANGELOG.md)
- Follow-up still open: `skills/STRUCTURE.md` and
  `blueprints/end-to-end-sandwich-run.md` still reference the old `discover`
  path and the narrative layer.


## [Unreleased] — 2026-06-20

Structure: removed letter prefixes from research-layer skill folders while
keeping all skill names and slash commands unchanged.

- Renamed `skills/{A_discover,B_project,C_task,D_probe,E_insight,F_paper,G_application,N_narrative}/`
  to `skills/{discover,project,task,probe,insight,paper,application,narrative}/`.
- Kept numbered task-domain folders unchanged: `0_*`, `1_data`, `2_nn`,
  `3_end`, and `4_individual`.
- Updated plugin docs and cross-references to use the new folder names.


## [0.2.5] — 2026-07-24 · paper is paper, display is display

Split poster and slides along the seam that was already there. Each used to read a paper *and* typeset the result; the two halves now live where they belong, joined by a written contract (`display/ref/content-plan-spec.md` — a markdown content plan plus a figures folder).

- **`display/haipipe-display-poster`** and **`display/haipipe-display-slides`** (renamed from `paper-poster`/`paper-slides`) are now RENDERERS: content plan + figures → tcbposter / beamer → PDF · PPTX · SVG. They never open `main.tex` or `sections/*.tex`, and refuse rather than hunt for a source when the plan is incomplete. Any source can feed them — a paper, an application, a talk outline typed by hand.
- **`paper/5-present/paper-poster`** and **`paper-slides`** are now EXTRACTORS: read the paper, decide what a poster/talk shows of it, write the plan, dispatch to the renderer. Selection is a paper judgement and stays with paper; layout is not.
- The seam was already in the code — old Phase 1 produced `POSTER_CONTENT_PLAN.md` / `SLIDE_OUTLINE.md` and Phases 2-8 only ever read that. The split formalised the intermediate instead of inventing one.

## [0.2.4] — 2026-07-24 · display/ bucket

New shared **`display/`** bucket for cross-cutting render tools. Pulled the four display RENDERERS out of `paper/1-lifecycle/4-display/` and dropped the paper prefix (`haipipe-paper-display-{figure,illustration,diagram,table}` → `haipipe-display-*`); moved `paper-poster` / `paper-slides` out of `paper/5-present/` (names kept, they still consume a compiled paper). html-ppt / html-to-svg already lived here. The paper 4-display **stage** (the display-plan doc + `ref/display-unit-output-contract.md`) STAYS in paper — only the renderers moved. All 75 references updated across 25 files; git mv preserved history.

## [0.2.3] — 2026-07-24 · 0.x policy

Reset every skill **and** this package to `0.x` — the whole toolkit is declared pre-1.0 until JL blesses individual pieces. Mechanical renumber `X.Y.Z → 0.X.Y` across 135 skills (2 already-0.x skills left alone; `diagram-drawio` given `0.1.0`); `plugin.json 2.3.4 → 0.2.3`, marketplace `2.0.0 → 0.2.0`. Each skill's own CHANGELOG got a matching top entry; older entries keep their original numbers.

## [2.4.0] — 2026-06-16

Feature: endpoint lifecycle overhaul — MIMIC-IV mortality deployed to Databricks end-to-end.

### Endpoint skills (3_end/)
- **LESSON.md**: 14 lessons from MIMIC endpoint build (L1–L14), journey summary, deployment platform comparison (SageMaker vs Databricks).
- **haipipe-end/ref/0-overview.md**: three-layer builder architecture (template → project → production), deployment platform verb table (validate → upload → register → deploy → smoke test → stress test → promote), roundtrip invariant.
- **haipipe-end-meta**: inputSchema follows Databricks `dataframe_records` format, 3 builder examples in `ref/examples/` (CGM, Weight, MIMIC).
- **haipipe-end-src2input + input2src**: real-data roundtrip test REQUIRED for design/review.
- **haipipe-end-endpointset**: step 5b reproducibility check, D-prefix exclusion (160MB→14MB), three-level roundtrip enforcement.
- **haipipe-end-deploy-databricks**: platform repo link, verb-to-script mapping, MIMIC config example, gotchas (D-prefix, DATABRICKS_USER).

### Task skills (task/)
- **haipipe-task-for-endpoint**: renamed from haipipe-task-for-inference, C-series endpoint building scope.
- **haipipe-task-for-fit**: ExampleFn, SKIP_TRAINING parameter, step 8 reproducibility, prediction_results.json must-be-non-empty.
- **haipipe-task-for-data**: 00_develop pattern (develop→execute pairs per stage), D-prefix dictionary table exclusion.
- **haipipe-task/ref/task-lifecycle.workflow.js**: template-based task detection (data/fit/endpoint → don't modify .py).

### Data skills (1_data/)
- **haipipe-data-source**: D-prefix tables are SourceFn-only, never enter examples or payloads.

### Infrastructure
- **haipipe-qa**: new QA walkthrough skill for systematic pipeline review.


## [2.3.4] — 2026-05-31

Feature: a probe-cycle now returns 🟧 W (the next-step) as well as 🟨 K.

- **W wired into the probe-cycle.** On convergence, `haipipe-probe-loop` Step 3 files the 🟨 K, then OPTIONALLY (◇) chains `card-creator-wisdom-agent --scope <new-K>` → one per-probe 🟧 W (the probe's concrete next-step), scoped to that K. Skips cleanly when the probe implies no next-step (no fabrication).
- The W machinery (`haipipe-insight-wisdom` + `card-creator-wisdom-agent` + `invocation-modes` W row) was already correct — only the wiring was missing. The probe-cycle deliverable is now **K + W** end-to-end, so the narrative gets the claim AND the recommended next whip-crack to decide `ignite`.
- **Per-probe W** (single-K next-step, in the loop) is now distinguished from **strategic W** (across many K, stays cross-cycle).
- **Dogfooded**: confirmed probe → K01 → W01 ("param-matched FiLM re-test"); 13/13 card-reviewer-wisdom + 5/5 index-integrity gates green (independent re-run).
- Docs threaded: `06`/`00`/`07` diagrams, `ARCHITECTURE.md`, `DESIGN.md` (Q2 corrected from the stale `card-creator-data-agent` dispatch). The v2.3.3 "W is the next wiring target" caveats are now flipped to "K + W both wired". → see [skills/insight/CHANGELOG.md](skills/insight/CHANGELOG.md)


## [2.3.3] — 2026-05-31

Docs: named the end-to-end hinge between narrative-cycle and probe-cycle.

- **Claim Gap Contract** is now the explicit connector: a narrative C-slot marked `GAP`/`weak` in `claims.md` becomes the evidence contract for one probe-cycle. The contract expects K/W (K is wired now; W remains the next wiring target); the narrative re-reads K/W and records `ignite`.
- Added `diagram/v260531/07-end-to-end-claim-gap.txt` for the full ask→claim-gap→probe→K/W→cash-out workflow.
- Threaded the concept through `ARCHITECTURE.md`, `HANDOFF.md`, the diagram index, `skills/narrative/DESIGN.md`, and the narrative schema.


## [2.3.2] — 2026-05-31

Fix: a probe-cycle now files its claim as a 🟨 K card (was a 🟦 D card).

- **K sources the confirmed probe's `claim`** (not `≥1 I card`). The skill prose contradicted the schema — which already said `K sources = confirmed probe` — and a single probe-cycle could never reach K through the I-chain (I needs ≥2 D). Fixed in `haipipe-insight-knowledge`, `card-creator-knowledge-agent`, `ref/invocation-modes.md`.
- **probe-loop convergence now dispatches `card-creator-knowledge-agent`** (files the K from the claim), not `card-creator-data-agent`. The 🟦 D observations come from the probe's task-cycles; 🟩 I / 🟧 W are cross-cycle.
- **Dogfooded** on a stub project (confirmed probe → K01): all card-reviewer-knowledge gates + index-integrity passed.
- Docs threaded: `dikw-boundaries.md` (K source = confirmed probe) + `06-probe-cycle.txt` Ⓕ.
- Still pending: the `D-from-task` reconciliation (data skill still reads a probe).


## [2.3.1] — 2026-05-31

Vocabulary + a probe-cycle process doc (docs only).

- **Cycle vocabulary unified** — the three nested units are now **narrative-cycle ⊃ probe-cycle ⊃ task-cycle** (renamed from the earlier "stage / atom" mix). `L0–L3` stay as loop-level labels.
- **`diagram/v260531/06-probe-cycle.txt`** (new) — the canonical 6-step process for running ONE probe cycle (design → bridge → run×N → result → verdict → insight), its 4 gates, and the two drive modes. `02` reframed as the probe-cycle *anatomy*; `03` as the *nested cycles*; `05` renamed `roles-and-stage` → `roles-and-cycle`. Threaded through DESIGN / HANDOFF / both CHANGELOGs / probe-loop.


## [2.3.0] — 2026-05-31

The insight agent skeleton — E gets the `agents/` + dual-mode parity task and probe already had, with a deliberate per-type-reviewer twist.

### Highlights
- **insight agentified** — `agents/creators/` (4, one per DIKW layer; each a thin headless wrapper over `haipipe-insight-<layer>`) + `agents/reviewers/` (**per-type**: `card-reviewer-{data,information,knowledge,wisdom}-agent`, each enforcing that card's accuracy + boundary, plus a cross-layer `index-integrity-auditor`). A deliberate departure from C/D's type-agnostic reviewers — each DIKW card has a genuinely different boundary. → see [skills/insight/CHANGELOG.md](skills/insight/CHANGELOG.md)
- **`ref/dikw-boundaries.md`** — canonical per-layer boundary + the two promotion gates + a worked D→I→K→W example; creators follow it, reviewers enforce it.
- **Dual-mode DIKW skills** + `ref/invocation-modes.md` — the 4 filer skills run interactive OR headless (full spec → silent), chosen by input completeness.
- **Loop closure** — `haipipe-probe-loop` now dispatches `card-creator-data-agent` on convergence, filing the D card and closing the probe cycle (`probe → task → insight`) the loop previously skipped.
- **Agent registry** 13 → 22 (E adds 9: 4 creators + 5 reviewers).

### Layer changelogs touched this release
- [insight](skills/insight/CHANGELOG.md) — NEW: agent skeleton, dual-mode, per-type reviewers, dikw-boundaries


## [2.2.0] — 2026-05-31

The insight design + research-engine model release. **Design-only** — no new runtime skills built yet; this records the design + the mental model so the build has a stable target.

### Highlights
- **insight `DESIGN.md`** (`skills/insight/DESIGN.md`) — E finally gets the skeleton task/probe already have, applied THOUGHTFULLY (as probe departed from task): dual-mode invocation (= task's `ref/invocation-modes.md`), `creators/` per DIKW (the headless, agent-callable filing path), and `reviewers/` = E's unique `card-fidelity` (Codex) + `index-integrity` gates. Templates + agents NOT built yet.
- **Loop-closure finding** — `haipipe-probe-loop` never files insight: the probe cycle (`probe → task → INSIGHT`) has an empty last cell. E's headless creators are what close it; the loop is WHY filing must be headless.
- **Research-engine model, versioned** — `diagram/v260531/` (6 files): the hourglass (decompose ↓1:n / aggregate ↑n:1); the 5 roles (🥢 ask=领导/nudge · 📖 narrative=办事的人/brain · 🔧 probe=whip · ✋ task · 🧠 insight); "one stage" = one narrative turn; the probe·task·insight distillation chain. Vocabulary pinned: **whip** (挥鞭), not "wipe"; narrative is the brain (delegates execution, never runs compute).
- **HANDOFF.md** rewritten to resume from this converged model.


## [2.1.0] — 2026-05-31

The task "creator + reviewer agents" release: a clean split between thin per-type builder agents and shared type-agnostic reviewer gates, dual-mode skills, batch fan-out, and a notebook-bloat policy.

### Highlights
- **task agent families** — `creators/` (7 per-type thin builders, `code-creator-for-<type>-agent`) + `reviewers/` (2 fixed, type-agnostic gates). builder ≠ judge; the creator that writes code never reviews it. → see [skills/task/CHANGELOG.md](skills/task/CHANGELOG.md)
- **Skills renamed** `haipipe-task-<type>` → `haipipe-task-for-<type>` (7 types; router + logging unchanged), matching the `code-creator-for-<type>` naming.
- **Dual-mode skills** — one body, interactive (human steers) OR headless (agent passes a full spec → runs silent), chosen by input completeness; structured return so an agent caller can locate the scaffolded folder.
- **Knowledge centralized in `ref/`** — `authoring-conventions.md` (shared) + `invocation-modes.md` (dual-mode contract). Skills and agents both stay thin; knowledge has ONE home.
- **Batch fan-out** — `haipipe-task-batch` skill + Workflow `pipeline` (`batch-pipeline.workflow.js`): N typed specs in one session, each flowing author → GATE 1 → run → GATE 2 independently; GPU-safe (`autoRun` default off).
- **Notebook policy** — `_meta.notebook: full | thin | off` knob in `run-sh-template.sh`; heavy compute (training/data) defaults to `thin`; `notebooks/` + `_WorkSpace/` default-gitignored. → see [skills/project/CHANGELOG.md](skills/project/CHANGELOG.md)
- **Per-run quality moved C ← D** — the per-run sanity checklist now lives with `run-result-auditor-agent` (task GATE 2); `probe review run` delegates. → see [skills/probe/CHANGELOG.md](skills/probe/CHANGELOG.md)
- **probe agent families (lighter pattern)** — `reviewers/` (structural + integrity-Codex + claim-Codex) and `advancers/` (explorer). Deliberately NO `creators/`: probe's builders stay interactive skills (probe design needs steering; no type axis; parallelism is downstream in task). The same builder≠judge method, applied to a low-volume deliberate layer. → see [skills/probe/CHANGELOG.md](skills/probe/CHANGELOG.md)

### Layer changelogs touched this release
- [task](skills/task/CHANGELOG.md) — agents, skill renames, dual-mode, batch, notebook knob
- [probe](skills/probe/CHANGELOG.md) — per-run checklist delegated to task; bridge dispatch
- [project](skills/project/CHANGELOG.md) — notebook retention + gitignore guidance


## [2.0.0] — prior

Baseline at the start of this changelog: Tier-1 umbrellas (/haipipe-data, /haipipe-nn, /haipipe-end, /haipipe-project, /haipipe-individual) dispatching to per-stage / per-target Tier-2 specialists across stages 0–6.
