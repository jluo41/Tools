haipipe-paper — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.

## [0.7.0] -- 2026-08-06 -- S03/S04 become evidence pages (JL's final design)

JL's evidence-page ruling (260806, "exactly what I want") executed across the
paper projection:

- the topic page is an EVIDENCE PAGE: `route: outward|inward` in its metadata
  head (the type key; the `### Q-consumer register` marker is retired), and
  Content organized BY EXECUTOR: one `### E<n> · <question>` division per
  Q-executor conversation (🔗 QA-probe pointer, `#### consumers` rows with
  per-consumer A-consumer + row state, `#### answer digest`), plus the
  standing `### E0 · incoming` collect queue
- naming final: QA-bank (the executor's original) and QA-probe (the paper's
  stub); the four slot words are capitals everywhere including heading slots
  (`#### Q-executor` / `#### A-executor`; `consumer trace` and `bank binding`
  stay lowercase)
- `probe/topic-entry-contract.md`, `probe/per-stage-dispatch.md`,
  `fn/probes.md`, `stages/CONTRACT.md`, `ref/enter-console.md`, the S01/S02
  stage files, the S03/S04 craft files and READMEs swept to the new shape
- `S03-literature/template.md` + `S04-value/template.md` rewritten to the
  division shape with the head route: line; `entry-template.md` RENAMED
  `qa-probe-template.md` in both folders, in the record shape
- `probe/check_topic_entries.py`: topics detected by the head route: key,
  digit-first `<n>-<slug>.md` record names enforced (the stale S-prefix
  filename rule fixed), capital slot headings canonical
- MISQ 2026 migrated as the proving paper: 8 evidence pages restructured into
  E divisions, 28 QA-probes kept their names and gained capital slots; board
  checker baseline held at 11 ERRORs

## [0.6.1] -- 2026-08-06 -- probe entries are hidden probe QAs (ruling B)

JL ruling B (260806: "an entry is a source file the topic page points at, like a
PDF; the board renders the topic page, never the entry") plus its naming
addendum (one conversation, two QAs: the bank QA is the original, the probe QA
is the paper's copy that points at it):

- `probe/topic-entry-contract.md` and `fn/probes.md` now name the nested file a
  probe QA (the entry record), state the digit-first naming law
  `probes/L<nn>|V<nn>-<topic>/<n>-<slug>.md` with `<n>` restarting at 1 per
  drawer, and say why the name hides it from the board's page sweep.
- `SKILL.md`, `fn/folder.md`, and `ref/comment-protocol.md` wording sweep:
  entry page -> probe QA; the executor's file is the bank QA, the original.
- Stage data updated in place (unversioned folders): `S03-literature/` and
  `S04-value/` `entry-template.md` rewritten to the record shape (# title +
  `requires:` + the four slots, no page frame, no Log), `template.md` example
  pointers and both READMEs moved to the `<n>-<slug>.md` naming.

## [0.6.0] -- 2026-08-06 -- ONE registered skill (thin-paper phase 3)

JL ruling 260806 ("只保留一个 skill, 就是 haipipe-paper"): the paper family now registers
exactly ONE skill, this door; everything else is data. The nine remaining registered
siblings retired to `../_old/phase3-260806/`, their jobs absorbed as internal steps:

- `haipipe-paper-folder` -> `fn/folder.md` (the scaffold procedure; `enter`'s
  get-or-create branch cites it).
- `haipipe-paper-conform` -> `fn/conform.md`; its mechanical checker moved to
  `scripts/check_structure.sh` and the `conform` verb runs it. The delete-test RULE
  text lives in the fn.
- The five S09-build skills became human-triggered door verbs, one fn each:
  `haipipe-paper-compile` -> `fn/compile.md` · `haipipe-paper-diffpdf` ->
  `fn/diffpdf.md` (toolkit at `scripts/diffpdf/`, class presets + known bugs at
  `ref/diffpdf/`) · `haipipe-paper-project` -> `fn/project.md` (runtime at
  `scripts/project/`) · `haipipe-paper-to-overleaf` -> `fn/to-overleaf.md` ·
  `haipipe-paper-to-word` -> `fn/to-word.md` (exporter at `scripts/to-word/`).
- `haipipe-paper-round` + `haipipe-paper-rebuttal` became STAGE DATA: the new `round`
  stage (`../S10-round/round/stage.md` + `template.md`, per-unit, one dated round per
  page, `board_family: Round`) with the reviewer-response craft distilled to
  `../S10-round/rebuttal-craft.md` and loaded via the stage's `craft:` list. New row
  in `stages/index.yml` after section-edit (triggers: round, rebuttal, 返修,
  reviewer response); the checker is the door's own
  `probe/check-probe-cards.sh --stage round`.
- Verbs table updated: folder/conform/build rows now name their fn files; round and
  rebuttal route to the STAGE step, key round. `fn/feedback.md` inboxes repointed
  (fn verbs -> the door's own fallback; round/rebuttal -> `S10-round/round/feedback/`).
- Reference sweep: `../README.md`, `ref/04-lifecycle-map.md`,
  `ref/paper-folder-anatomy.md`, `ref/diffpdf/compile-pipelines.md`, moved scripts'
  self-references, `skills/STRUCTURE.md`, haipipe-project's `project-structure.md`,
  and haipipe-application-round's description all repointed to door verbs / fn paths.
  Boards under `diagrams/` deliberately left for the main session.

## [0.5.0] — 2026-08-05 — the ONE door (thin-paper phase 2)

- Absorbed the three routers into this skill and retired them to `../_old/`:
  `haipipe-paper-stage` (stage resolution via stages/index.yml, create-page.py,
  the one-stage-file rule, the PROBE ceiling with the --depth spend-authority
  warning kept word-for-word, checker-before-CHECK, rebuild-after-write and
  re-read-before-read), `haipipe-paper-enter` (the console procedure, compressed;
  detail in the new `ref/enter-console.md`), and `haipipe-paper-lifecycle`
  (stage ordering, maturity rule, global-pass mode, phase-verb pass-through).
- Phase driving is NOT restated: the door ensures the S page exists and hands it
  to `haipipe-board-page` (WORK ON / RUN); `board/page-phases/` own DPRC.
- `workers/` dissolved: page rules stayed in board/, the LaTeX craft became
  stage data files declared by each stage.md `craft:` list
  (S03 citation-craft.md · S04 values-craft.md · S05 draft-craft.md ·
  S06 revise-place/revise-results/check-evidence-craft.md ·
  S09-build/proof-checker/ as a craft pack), and the probe tooling moved into
  this skill's `probe/` (check-probe-cards.sh, check_topic_entries.py,
  topic-entry-contract.md, per-stage-dispatch.md); the probe worker's unique
  deltas merged into `fn/probes.md`.
- Moved in from the retired stage router: `stages/` (index.yml, CONTRACT.md,
  section-kinds.yml), `create-page.py` (BOARD_STAGE repointed to
  board/haipipe-board/cli/stage.py), `check-contracts.py`, `section-stats.py`,
  and `ref/` (joined by the ex `workers/REF/` files). The comment protocol's
  format detail moved to `ref/comment-protocol.md`; the door keeps the binding
  lifecycle rules.

## [0.4.6] — 2026-07-30 — explicit projection routing

- Added `project` and `projection` to delivery routing so gated S-page content
  reaches `haipipe-paper-project` rather than an implicit submission overwrite.

## [0.4.5] — 2026-07-27 — Display Intake routing

- Separates a missing display-ready aggregate (task-for-display) from a paper-facing render (Paper Display → Intake → renderer).
- Removes the stale direct re-render-to-task route, so an existing verified aggregate is never mistaken for a paper asset.

## [0.4.4] — 2026-07-26 — one evidence dispatch topology

- Synchronized the active Paper probe reference and behavioral preference with
  the runtime chain: Paper PROBE performs ORGANIZE/MATCH, the isolated
  q-executor collector performs DISPATCH/POINT, and task/discovery remain
  behind that collector.
- Removed the last active instruction that told a Paper worker to dispatch
  directly to task/discovery.
- Corrected active probe-entry globs to the topic-folder anatomy
  `1-probes/PP*/*.md`.
- Removed active migration instructions for old probe sidecar paths; the Paper
  contract now exposes only the current topic-folder anatomy.

## [0.4.3] — 2026-07-26 — stage declarations are authoritative

- Replaced the universal four-phase/two-gate story with each stage's
  `phases:` and `gates:` declarations; current stages gate only at CHECK and
  Venue omits REVISE.
- Moved phase/comment history from `_LOG` sidecars into owning S pages.
- Corrected probe ownership: DRAFT raises Q-consumers; PROBE authors entries
  and owns ORGANIZE through INTERPRET.
- Removed the unsupported `argument-hint` frontmatter key so the user-facing
  orchestrator passes the current `skill-creator` validator.

## [0.4.2] — 2026-07-26 — one composed tail, one probe phase

- Declared Paper as Board's canonical enclosing-skill case: Paper emits one
  closing block with the active Board deep link and never appends the direct
  Board `status.py` strip.
- Restored the four-slot DPRC line (`draft | probe | revise | check`) and
  removed the retired `cite` / `val` / `disp` probe sub-tracks.

## [0.4.1] — 2026-07-26 — derived state has one home

- Replaced the stale `current_layer` gate wording with the actual stage-closing approval action.
- Removed remaining `STATUS` references from delivery routing; open needs and resumable state live on Board/S pages, the claim ledger, probe entries, and their target files.


## [0.4.0] — 2026-07-26 — the Closing Block carries the board URL, not a stage strip

Implements the single-door ruling (design board `skills/diagrams/01-haipipe-paper-260725`, faces `QA1` + `QA4`, JL 2026-07-26): **`/haipipe-paper` is the single thing a human types**, and it CALLS `haipipe-board` to build and open the paper's `0-lifecycle/`. `haipipe-board` remains its own door for boards that are not inside a paper. Calling is not owning: `haipipe-board` still owns the format, the build, the filename rule, the html and the write-back.

- **The `stage:` line and `stage-strip.sh` are RETIRED.** The strip was specified in the 260622 feedback as reading `STATUS.md current_layer`, with the stated precondition that a stale value would make it lie. `STATUS.md` is retired and the board renders the spine, so the strip has neither a source nor a job. It was a worse copy of something the human already has open.
- **A deep-linked `board:` line replaces it**, pointing at the page this session is working, so one click lands on it.
- **The `phase:` line survives, and the reason is stated.** It is the only thing in the closing block the board does NOT show: a page's `state:` is its gate status, not the live DPRC progress of a run in flight. The stage line was derivable from the board and therefore redundant; the phase line is not.


## [0.3.2] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 3.2.1; older entries below keep their original numbers).

## 3.2.1 — 2026-07-19 — vocabulary: `probe` (not "the constitution"); entry/`### a-executor` naming

Two vocabulary rulings from JL, both dated 2026-07-19, applied across `paper/`.

**Ruling A — the `probe` nickname.** JL: "宪法 don't use this name, just use `probe`." Every "THE CONSTITUTION" / "the constitution" / "the probe constitution" naming `probe/haipipe-probe/SKILL.md` is replaced by `probe` or by the actual path, whichever reads better at the site. A nickname already in the repo is still a nickname.

**Ruling B — the `a-consumer:` probe-file field.** `- a-consumer:` as a FIELD IN A PROBE FILE was replaced by the entry's `### a-executor`; `check-probe-cards.sh` HARD FAILs it under the `stale-old-format` rule. The a-consumer CONCEPT is untouched and still named a-consumer: it is the per-consumer interpretation written in the STAGE DOC (station ②), anchored `[source: PP<NN>]`. Prose that said "the probe section carries its `a-consumer:`" was wrong twice over — probe files hold ENTRIES, not sections, and what an entry carries is `### a-executor`.

Current model, for reference:
```
QA file (bank)  ->  the ENTRY's `### a-executor`  (probe file: the copy, single source of truth)
                ->  each Q-consumer's a-consumer  (STAGE DOC: what it MEANS for this consumer)
                ->  stage content                 (REVISE weaves it in, discharges the bracket)
```

Written under JL's NO TOMBSTONES rule (2026-07-19): "不需要留退役告示,直接抹除任何痕迹" then "follow this rule to do all the following changes." The docs state only the current contract; this CHANGELOG carries the history.

### Changed — SKILL.md
- The `probe` verb block: "That worker follows the shared probe model (the constitution)" -> "...the shared probe model owned by `probe/haipipe-probe/SKILL.md`".
- Same block: a stage's PROBE phase works "the sections whose `serves:` names that stage" -> "the entries whose `### q-consumer` bullets name that stage". `serves:` is one of the three strings `check-probe-cards.sh` HARD FAILs (`stale-old-format`), so the umbrella was describing a slice the checker rejects. Found during this pass, not on the reported list.

### Changed — fn/probes.md
- Three "constitution" references retitled: the model owner line ("v9.5.0, the constitution" -> "v9.5.0"), the anatomy pointer ("the constitution's \"The probe file\" section" -> "`probe/haipipe-probe/SKILL.md` -> \"The probe file\""), and the loop header ("constitution v9.5.0" -> "probe v9.5.0").

### Unchanged (verified LIVE, ruling B)
Every `a-consumer` in SKILL.md (7 sites) and fn/probes.md (2 sites) already named the stage-doc concept — "each Q-consumer's a-consumer (in the stage doc)", "each stage doc's a-consumer", "a-consumer in its stage doc (station ②)". This file was already on the current model; nothing was rewritten.

## 3.2.0 — 2026-07-19

Changed (JL 2026-07-19, paper/2-phase refactor — the sidecar model is retired: `1-probes/` is the only consumer-side source of truth, `_LOG_<stage>.md` the only sidecar)

- **Retired sidecars swept out of the router.** `Used in: … _CITATION_, _VALUES_` (the two-comment-formats section) → section `.md` files and `1-probes/PP*.md` entries. `fn/probes.md` legacy-migration rule: the "Stage-owned working docs (`_CITATION_`, `_VALUES_`, `_EVIDENCE_`, `_DISPLAY_`) do NOT move" clause named four documents nobody writes; replaced with the live statement of what IS the source of truth.
- **Dissolved lane skills swept out.** `fn/feedback.md` routed `citation, bibtex, references` to `haipipe-paper-probe-citation`; now `haipipe-paper-draft-citation` — citation holes are DRAFT's to open, not PROBE's. `fn/probes.md` step ⑤ said "the harvest lanes pay out"; harvest is INLINE in ⑤ and `### a-executor` is its only sink, so it now names what actually rides along (source anchors, values, display-unit paths).
- **Composing with Evidence Workers diagram** redrawn to the current phase split: DRAFT authored ①ORGANIZE + ②MATCH (most entries close at MATCH, T2 REUSE); PROBE runs ③④⑤ and dispatches through `Agent(haipipe-probe-q-executor-agent)`, which fans out to the task/discovery orchestrators — the router previously showed PROBE calling those orchestrators directly, which is precisely the inline dispatch the collector exists to prevent.
- **Evidence Routing Protocol** re-rooted: `\needprobe{}` comes out when the entry's `**target**` resolves and its `### a-executor` is written (was `target:` + `a-consumer:` — and `a-consumer:` as a probe-file field is a format `check-probe-cards.sh` HARD FAILs). Handoff step (d) attributes MATCH to DRAFT; step (e) states the real backfill chain: PROBE writes `### a-executor` → each Q-consumer writes its a-consumer in the stage doc → 1b-claims.md flips → the flag comes out.
- **Vocabulary**: probe `SECTION` → `## QX<n>` ENTRY across the description, summary, verb line, Delivery Need Routing, and the `probe` verb; `fn/probes.md`'s no-tables rule now says a probe file holds ENTRIES.

## 3.1.1 — 2026-07-19

- WIKI RETIREMENT — three shared docs absorbed here, each now with exactly ONE home (the wiki folder is deleted; every referrer points at the section, nothing is duplicated):
  - **Comment lifecycle** (was `02-comment-lifecycle.md`, 18 referrers) — new section after the Closing Block: actor ids (never hardcode initials), the two formats (blockquote `.md` / `%% {}` tex), the two marks + `========>` reply separator, anchoring, the 6-step lifecycle + 5 rules, `_LOG` format (newest-at-top, non-destructive insert, date + HH:MM headings), the REVISE no-comment-first exception, and the round invariants table. The loaded-context rule is kept: this section is BACKGROUND, so every skill touching working files still INLINES its binding subset.
  - **Delivery Need Routing** (was `11-delivery-need.md`, 11 referrers) — MERGED into the existing section rather than added beside it: how paper talks to probe (command + disk channels), when to record a need, routes, the need-record schema, backfill, and the autonomous-drain loop with its AUTO/PAUSE autonomy policy.
  - **Evidence Routing Protocol** (was `12-evidence-routing.md`, 4 referrers) — new section directly under Delivery Need Routing: the `\needprobe{}` macro, the 5-step handoff protocol, the `probe` verb, background dispatch for heavy probes, and construction-as-a-first-class-beat.
- Structure pointers repointed: skill tree -> `../README.md` (which absorbed `06-paper-skill-structure.md`); rounds -> `../0-enter/haipipe-paper-round/SKILL.md` (which absorbed `07-paper-rounds.md`).

## 3.1.0 — 2026-07-14

- `fn/probe-plans.md` RENAMED to `fn/probes.md` ("plans" is retired vocabulary); the verb table and Dispatch notes re-point at it.
- Dispatch notes: "Verdicts backfill into 1-claims / sections / round logs" -> the answer lands as a section's `reading:`, and the CLAIM's status flips in `0-lifecycle/1b-claims/1b-claims.md` (the only home of a claim's status). "Buffer convention" -> "Probe-file convention".

## [2.11.0] -- 2026-07-14
## 3.0.0 — 2026-07-14

- The `probe` verb is re-pointed at the PROBE-FILE POOL (`1-probes/PPNN_<topic>.md`, one file per TOPIC, one SECTION per question). Before this, every `/haipipe-paper probe` invocation was routed into the dead card/stub model: the routing table sent it to `1-probe-plans/` cards, the `no args SHOW` mode derived statuses from `_ASK/` stubs (which R2 forbids from ever existing, so it would always report zero dispatches even with commissions in flight), and the diagram routed the verdict to the retired gateway.
- `fn/probe-plans.md` REWRITTEN (legacy filename kept, same precedent as check-probe-cards.sh). It was fully pre-v8: cards in `1-probe-plans/`, the status set `planned | dispatched | verdicted` (two of which are DELETED states), and `dispatch Agent(haipipe-probe-orchestrator-agent) -- ALWAYS, no matter how small the need` — the exact opposite of R13. It now carries the 1-probes/ convention, MATCH-before-DISPATCH, and direct dispatch to the two executor orchestrators.
- PREFERENCES.md — the highest-authority text in the bucket, loaded on every paper session — re-stated in v8 terms. It MANDATED the retired 4-step procedure and named the archived gateway agent, so a session would obey it, dispatch a nonexistent agent, fail, and (because the preference explicitly forbids substituting an inline scan) have no legal fallback. The INTENT is preserved verbatim: never fake a probe with a web scan.
- The evidence-routing table's `settled judgment -> the PP card's ## Verdict` route now points at `0-lifecycle/1b-claims/1b-claims.md`, the ONLY home of a claim's status (R7).

JL resource ruling (pairs with haipipe-paper-resource 1.0.0 + haipipe-paper-lifecycle 2.4.0): RESOURCE registered as a venue-FREE stage between seed and claims. New verb `resource | prereq | prerequisite | need` -> `haipipe-paper-lifecycle resource` -> `0-lifecycle/1a-resource/1a-resource.md`: what must EXIST for this paper to be testable, does it exist, and can it CARRY the claim (data, model checkpoints, and producing-code alike). The stage ASKS (Q<n>) and the probe gateway ROUTES (mints the PP, picks the type) -- so no new probe lane and no new namespace. Venue-coupling prose now reads seed + resource + claims as venue-FREE and unchanged on retarget; the closing-block stage-strip example and the Composing diagram both carry `resource`. resource SHARES the number 1 with claims (precedented: 2a-venue/ and 2b-pitch/ already share 2); nothing renumbers.


## [2.10.0] -- 2026-07-12

JL routing ruling (haipipe-probe 7.8.0 companion): `probe plan` (the campaign consolidation pass) gains a ROUTE step — resolve every card's `target:` (the receiving task-folder / discovery folder; `NEW ...` when it must be created; `?` only with a stated reason). The campaign pass is the right moment because it is the only one where the whole evidence campaign is visible at once: two cards routed at the same task-folder are a hint they should merge, and a card with no plausible home is a hint the need is under-specified. DRAFT-buffered skeletons may leave `target: ?` — the paper often does not yet know what the project holds.


## [2.9.0] -- 2026-07-12

JL both-banks layout ruling (pairs with haipipe-probe 7.7.0; supersedes the 2026-06-29 per-stage layout for PROBE CARDS only):
- PPNN cards live FLAT in `1-probe-plans/PPNN_<slug>.md` beside the campaign README -- one cross-stage pool, `serves:` carries stage affinity, the whole campaign is one `ls`. The `probe "<text>"` BUFFER sub-mode files new cards there; `probe plan` reads all cards from the pool.
- Execution-bank stubs live in `_ASK/` containers (`<receiving folder>/_ASK/PPNN_<slug>.md`), filename mirroring the card's.
- `fn/probe-plans.md` rewritten: location + migration direction reversed (legacy per-stage `_PROBE/` cards move INTO the pool on first touch); card anatomy defers to the probe layer's SKILL.md.


## [2.8.0] -- 2026-07-11

Added (JL cross-stage ruling 2026-07-11; pairs with haipipe-probe 7.5.0)
- `probe plan` sub-mode: the CAMPAIGN consolidation pass, run after a cross-stage draft sweep — read all stage drafts + all _PROBE/ cards, merge duplicate needs (one card, many serves:), author the dispatch DAG (gating first, refutation-capable early, dependents wait, query-once) into the Campaign section of 1-probe-plans/README.md; Status board stays generated. Campaign is a HUMAN GATE like DRAFT — present and stop; the user's verb advances to "run".

## [2.7.1] -- 2026-07-11

Changed (two-footed-bridge ruling, JL 2026-07-11; pairs with haipipe-probe 7.4.0)
- `1-probe-plans/README.md` demoted everywhere it is mentioned (description, probe verb row, probe dispatch note) to a GENERATED index: the per-stage `_PROBE/` cards are the single source of truth; the index regenerates from cards + `_ASK` stubs + answering reports and is never hand-maintained; on disagreement, cards win.

## [2.7.0] -- 2026-07-09

Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
- Phase-verb pass-through documented in the routing table: trailing `draft|probe|revise|check` forwards through the lifecycle router to the stage skill; stage skills stop at their human gates and the user's verb advances them.

## [2.6.0] — 2026-07-08

Changed (venue lockfile wiring)
- Venue coupling rule updated: venue stage compiles the pack into `0-lifecycle/2a-venue/2a-venue.md`; the venue-ALIGNED stages consult 2a-venue.md first, with direct `_venue/playbook-<venue>` reads demoted to fallback (2a-venue.md absent) or deep dives via its `[source: ...]` tags.

## [2.5.0] — 2026-07-04

Changed (probe-plan location unified, JL 2026-06-29 per-stage ruling wins over the flat buffer)
- Probe plans live in per-stage `_PROBE/` folders; `1-probe-plans/README.md` is a thin cross-stage index (numbering authority). Verb line, dispatch note, evidence-path map, and fn/probe-plans.md all updated; PP statuses gain `read` (light probe returned, takeaways backfilled into the plan file). `_DISCOVERY_{stage}.md` retired.
- Legacy layout migration rule (fn/probe-plans.md): flat 1-probe-plans/PPNN files move into their source_stage's _PROBE/ on first touch; legacy _DISCOVERY_ folds into the plan file + citation harvest, then deletes; the move is logged in the stage _LOG.

## [2.4.1] — 2026-07-03

Fixed
- Marker rule tightened from "at most one 🔥 and one 🚀 per line" to EXACTLY one of each, never zero (live seed run rendered `draft 🔥` with no 🚀 anywhere). "Reached" defined as entered-not-completed, so a virgin paper's first phase renders `draft 🔥🚀`; a line with 🔥 but no 🚀 is a rendering defect.

## [2.4.0] — 2026-07-03

- create verb RETIRED, absorbed into enter as GET-OR-CREATE (JL: 直接去掉create，enter的时候没有就call create): a missing path CONFIRMS first (repo creation is outward-facing, never off a typo), then runs the same flow (org resolved per invocation, papers-inside recipe, folder scaffold, double-bump) and continues straight into the console. Verbs block, dispatch notes, examples, chooser, argument-hint updated; lifecycle + folder-skill + lifecycle-map cross-references repointed. The create flow itself is unchanged and was validated live (Paper-PhyPatSim run) before the re-homing.

## [2.3.0] — 2026-07-03

- stage-strip.sh moved from the shared-reference folder INTO this skill folder (co-located with the Closing Block spec it renders; JL: 为什么 strip 在 wiki 里有这里也有); all 8 references repointed, no strip content left outside this folder.
- Resolved > JL: / > CC: comment threads archived below verbatim and removed from SKILL.md (comment lifecycle: working doc stays clean, resolved threads move to the log). Companion changes landed in their owners: 08-stage-gate.md Gate Modes (copilot|autopilot) + APPROVAL step + ledger Actor column + Stage Exit Invariant; haipipe-paper-check 1.4.0 (Gate Modes + invariant); haipipe-paper-probe 1.7.0 (From-buffer entry).

### Archived comment threads (verbatim)

**@ Verbs / Dispatch notes**

> CC: write/edit 的老路由目标 haipipe-paper-edit-write / edit-weaving 在重构后已不存在（对应能力并入 2-phase/2-revise workers，由 stage 内部调用）。我把 write/edit/polish 这些词全部路由到 section-edit stage 了，对吗？还是这组动词干脆退休不再出现在 Verbs 块里？
> JL: 是的，旧词不要再出现了，省的误导
> CC: 已退休全部旧词（write/edit/polish/draft/写初稿/整篇润色），section-edit 行只留 section-edit|section|sec|§N。
> JL: 好，done

**@ Closing Block (end every reply)**

> JL: 这个应该有两层吧 一个是stage，一层是phase
> JL: <--- 这里可以弄的再简单一些吗。比如paper root不要了，然后status和current layer放到一起。
> JL: 我们是不是也有其他的file也在讲这个，要不把他调到这里，我们single source of truth
> CC: 三条都已落：两层 strip（stage+phase）、tail 简化为 status·stage + next 两行、01-focus-strip-markers 语义并入本节并删除原文件（enter skill 的引用已改指这里），此节即唯一出处。
> JL: 我想说你这个跟wiki里的strip的关系是什么，会冲突吗？
> CC: 不再冲突：wiki 里剩的只是渲染脚本，现已把 10-stage-strip.sh 也搬进本 skill（./stage-strip.sh，与 spec 同住），8 处引用全部改指，wiki 里已无任何 strip 内容。

**@ Gate-aware (Closing Block)**

> JL: 你要想着我们有两个mode，一个co-pilot 在check phase的时候，人加上comments，一个是auto pilot，在check的时候，call一个subagent，然后让他给comments 你想想这个我们怎么做。但是是的，必须要有一个judgment，就是这个gate-aware，进入下一个stage要非常的明白，要有confirm，要有一个approval的动作（人或者代替人的subagent）
> CC: 方案在 chat 里：CHECK 增加 mode=copilot|autopilot，autopilot 派 reviewer subagent 给 comments + approve/revise verdict，gate ledger 记 approval actor；你点头后我改 08-stage-gate.md + haipipe-paper-check。
> JL: 可以的，你整吧。
> CC: 已整：08-stage-gate.md 加 Gate Modes 节 + APPROVAL 步骤 + ledger 增 Actor 列；haipipe-paper-check 加 Gate Modes 节（autopilot 派 fresh reviewer subagent 落 > REVIEWER: comments + verdict；bibtex 等人类专属项标 DEFERRED 进 human queue，绝不静默放行）。

**@ Composing with Evidence Workers**

> CC: 原文这张图上游还列了 /idea-discovery /run-probe /auto-review-loop /result-to-claim 四个入口，skill 清单里已找不到，我删了。如果它们有新名字（或还想保留占位），告诉我补回。

**@ Composing with Evidence Workers**

> CC: 原文头部还有一处孤立引用（"读 lifecycle 参考时也读 ../1-lifecycle/haipipe-display-figure/SKILL.md"），看不出为什么单点名 figure 渲染器，我也删了。有特殊用途的话说一声。

**@ Composing with Evidence Workers**

> JL: 我们要不要把所有的wiki的内容也都移到这里来。然后随后把wiki的东西删掉。skill最好还是self-contained
> CC: 建议不整体搬：共享 reference folder 本就在 paper 家族内部（家族级 self-contained），02/04/08/10 各有 5-10 个 skill 共用，搬进 umbrella 会让每次调用重新变胖；折中方案已执行 01-focus-strip-markers（并入本文件）+ 单消费者页可逐个并入唯一消费者，详见 chat。

**@ Composing with Evidence Workers**

> JL: 这个的话，我在想，还都是有haipipe-paper-probe 来进行probe calling？不要让haipipe-paper直接call了，他在一个stage的一个phase的阶段来call。
> CC: 已改：umbrella 不再直连 /haipipe-probe，probe run 交给 haipipe-paper-probe（stage 的 PROBE phase worker）消费 1-probe-plans/ 再向下分发；Verbs 行、dispatch note、上图已同步。
> JL: 好，再确认一下。
> CC: 已确认并补齐另一端合同：haipipe-paper-probe 新增 "From-buffer entry" 节（from-buffer <paper_root> [PPNN]：读 planned 项 → reuse-before-create → 分发 /haipipe-probe → 回写 status/probe_ref → 返回 dispatch summary），两端调用签名一致。

## [2.2.0] — 2026-07-03

- JL in-file comment round applied (> JL: / > CC: threads kept in SKILL.md): (1) retired write/edit/polish/draft alias words entirely (省得误导); (2) closing block now TWO-LINE focus strip (stage + phase) with the simplified tail (status·stage merged, paper_root dropped, next only); (3) 01-focus-strip-markers ABSORBED into the Closing Block section as the single source of truth (file deleted; enter skill + 10-stage-strip.sh + the shared-reference index repointed; numbering gap kept); (4) umbrella no longer calls /haipipe-probe directly -- probe run hands 1-probe-plans/ to haipipe-paper-probe (the PROBE phase worker inside a stage's phase), composing diagram + dispatch note + description updated; (5) gate-aware line now names the two approval modes (copilot human / autopilot reviewer subagent), full design pending JL confirm (08-stage-gate.md + check skill).

## [2.1.0] — 2026-07-03

- Dedup rewrite (JL: "会有比较重复的地方吗", same treatment as discovery 2.6.0): say each thing ONCE. Command table + keyword map + positional aliases + Routing Step 2 (the same dispatch stated 4 times) merged into one Verbs block + one 6-rule Routing pass; feedback/digest full spec (written twice + fn/) reduced to one pointer section; create recipe (written twice + owner fn) reduced to one dispatch note; probe/venue-coupling/folder-tree/skill-tree restatements replaced by pointers to their owners (fn/probe-plans.md, 03-paper-lifecycle.md, paper-folder-anatomy.md, 06-paper-skill-structure.md). ~545 -> ~200 lines.
- Stale fixes swept in: 2-claims -> 1-claims backfill refs; 3-narrative.tex -> .md; phantom top-level 2-section-edit/ dir removed from the skill tree (real homes: 1-lifecycle/5-section-edit + 2-phase/); write/edit rerouted to section-edit (old targets haipipe-paper-edit-write/-weaving no longer exist); stage list gained section-edit; "phase skills" wording corrected to stage skills (DPRC phases are internal); retired upstream workflow names dropped from the composing diagram.
- Three open questions embedded as > CC: markers for JL review (write/edit verb fate, retired upstream workflow names, dropped display-figure reference).

## [2.0.2] — 2026-07-03

- create verb added to the front door (JL: should be /haipipe-paper create, not a sub-skill invocation): routes to haipipe-paper-lifecycle folder; repo-backed inside Project-* repos per project/haipipe-project/fn/repo-project.md papers-inside recipe; --org resolved per invocation (paper owner may differ from project owner). Retired prospectus verb/aliases removed (seed replaced it); haipipe-paper-bootstrap specialist entry replaced by haipipe-paper-folder; paper-folder contract tree fixed to current spine (1-claims, 2-pitch, 5-section-edit, .md early stages).

## [2.0.1] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; phase workers probe/ and revise/).

## [2.0.0] — 2026-06-22

- cross-cutting protocol wiring. All stage skills now reference ../1-lifecycle/ref/08-stage-gate.md (confirm-before-advance), ../1-lifecycle/ref/09-stage-illuminate.md (Socratic taste elicitation), 13-tex-quality.md (self-contained compilable tex), 12-evidence-routing.md (\needprobe macro + probe handoff). Stage strip end-of-reply convention enforced. Enter dashboard restructured (pitch summary first). 22 feedback items addressed.

## [1.5.0] — 2026-06-22

- probe buffer (1-probe-plans/). Claim-related evidence needs accumulate as probe plans during lifecycle work, then batch-dispatch to /haipipe-probe. Probe is the universal evidence gateway for claims; it calls task/discover during Gather. Direct task/discover verbs kept for non-claim utility work. See fn/probe-plans.md.

## [1.4.0] — 2026-06-22

- added probe/discover/task verbs as evidence-worker dispatchers. Paper orchestrator can now route directly to /haipipe-probe, /haipipe-discovery, /haipipe-task with project context resolved from the paper path. Paper stays story layer; evidence workers do the work.

## [1.3.0] — 2026-06-21

- renamed paper working-memory layer from feedback to rounds; added lifecycle, rounds, and skill-structure references.

## [1.2.0] — 2026-06-21

- made paper lifecycle the delivery-side owner of story/claims and routed GAP/NEED items through the shared delivery-need interface.

## [1.1.0] — 2026-06-21

- added enter/status paper-session loader routing.

## [1.0.0] — 2026-05-31

- baseline metadata added.
