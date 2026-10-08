# haipipe-insight · version history

## 3.1.0 · 2026-10-08 · A release, from proposals to a signature (b11 s21 phase 3)

- New `ref/release.md`: the life of a release (triage → open → ask · plan · script → review → cuts → sign),
  `release.yaml` (questions, kept · changed · new, retired), the cuts (full, cross, power before contrast, the pooling
  verdict) and signing; one release per triaged batch.
- `ref/partition.md` marked as the register board's older layout; on the ladder the cuts are `release.md`'s.
- `scripts/insight_ladder.py`: release folders may say what they are, `jNN_pN_<slug>` (`version --slug`); the Board's
  Propose Run defaults to `run-propose-coverage`; Run the Job and Sign the release name haipipe-insight, Close names
  haipipe-insight-check, Check consistency is the reviewer's (the run cards, phase 2).

## 3.0.0 · 2026-10-08 · The Prototype and the insight Board, two special boards that work together (b11 s21 phase 1)

- New `ref/insight-ladder.md`, the contract: the Prototype `tasks/Prototype-bNN-<Topic>/` (questions + scripts, a Job
  per release `jNN_pN/`, signed and frozen; `proposals/` its backlog) and the insight Board `insights/Insight-<name>/`
  (one dataset and its versions in board.md; a Job per release × data version `jNN_pN_<D>vM/`, a Task per question,
  a hard Run per cut `runs/rNN_<partition>/`). Twelve rules, the Runs by level with their owners, the six Spaces.
- New `scripts/insight_ladder.py`: prototype · version · question · change · retire · sign · propose · board · data ·
  job · run, with the gates (agreed questions and cuts before signing; a signed release, a frozen data version, a new
  pair and one clock per Job). `job` writes through `ref/open_job.py`; a hard Run's ticket runs `ref/run_job.py`.
- New `tests/test_insight_ladder.py`: the scaffold makes each level, keeps its gates, and the workbench's own reader
  (`servers/workbench-insight/insight_plan_c.py`) reads the result back.
- Decided: one clock per Job; a release is cut per triaged batch of proposals; a kept question reruns on a
  code-moved Job (the compare checks its tables' sha256, a reproducibility check).
- `SKILL.md` rewritten as the door for the two boards; the Insight Block (`ref/block-contract.md`) and the register
  board (`ref/board-contract.md`) are older layouts, read until carried over.

## 2.11.0 · 2026-10-05 · One Insight Block in tasks/ replaces Prototype + Instance (JL 261005)

- New `ref/block-contract.md` (was prototype-contract.md): an Insight topic is one task Block `tasks/b5N_<topic>_dikw/`,
  `workbench: insight`, `datasets:`, `meta/`, one Job per level, one Task per question (`question.md`, `scripts/`, the page).
  A run is `<dataset>_<partition>` with no per-run config; the code exists once (no copy, lock or sync).
- `ref/run_question.py` resolves a task folder and a run; `ref/scaffold_block.py` (was scaffold_instance.py) writes the
  tickets of questions with a compute need; `ref/sync_instance.py` is retired. `carry_over.py`, `question_map.py` and
  `write_answer_page.py` read and write the Block layout.

## 2.10.0 · 2026-10-05 · Every level is a run; the run's report is the report (JL 261005)

- Ask, work, report at every level: Knowledge tests across results and Wisdom tests its counsel, each
  through a script (`ctx.result(<QID>, <file>)` reads the level below; its `reads:` in the receipt
  make the run STALE when one changes). `COLUMNS = "none"` runs a script that reads only results.
- New `ref/figures.py`: the runner draws `results/<partition>/fig_<need>_<table>.png` from the result
  tables by their shape (rates with intervals, message x level, stability, balance, missing, share,
  an estimate beside its interval for Knowledge tests),
  deterministic bytes, never from the rows.
- `reports/<partition>/report.md` is THE report: per need its plain lead lines, its figures, its
  tables rounded, the power table last. The page is the short answer that reads it.
- The receipt carries `tables_sha256` and `content_since`; a rerun that writes the same tables keeps
  `content_since`, so a page read and a CHECK made since stay current.

## 2.9.0 · 2026-10-04 · Plain-reader rules for the answering page (JL 261004)

- `ref/report.md` § Plain-reader rules: lead with the point, a list is a table, round in
  prose, names only when needed, close with what it allows, at most four sentences. Pages
  read in reader mode in the workbench and the web delivery; Word and LaTeX carry the same
  subsections and tables (haipipe-page 0.122.0).

## 2.8.1 · 2026-10-03 · report.md names both layouts

- `ref/report.md` opens by naming the Prototype layout (one page per question, a section per partition, `runs/<partition>.sh`) beside the register board's, which it goes on to describe; before, a writer reading only it would make one page per partition.

## 2.8.0 · 2026-10-03 · The Prototype is the Block, with its studio (JL 261003)

- `ref/prototype-contract.md`: the Prototype carries the Block's `studio/`, no longer optional; an Instance shows its Prototype's.
- New `ref/question_map.py <Prototype>`: writes `studio/question-map.excalidraw` from the question files, one frame per level, one box per live question, one arrow per reuse (`cite` need), a dashed box for a question linked to no other; retired questions counted on the frame. Generated: rerun after a question changes, never edit it.

## 2.7.1 · 2026-10-02 · An Instance may keep studio/ (JL 261002)

- `ref/prototype-contract.md`: the Instance tree names the optional `studio/`, the board's own drawings shown in the workbench's Insight › Studio.

## 2.7.0 · 2026-10-02 · Question file v2 and the carry-over (JL 261002)

- Question file v2 (`ref/prototype-contract.md`): `question` (the short wording), `name`, `ask`, `source` (where it was carried from), `partitions` (asked, not_elsewhere, power), live and retired `needs` in the register's own spec fields (cut, unit, measure, by, uncertainty, rivals, output), `agreed`; Why now and What would answer it as prose. `0-Meta` holds `meta.md`, `partitions.md` (filters, then the reasons) and `thresholds.yaml` with one board-wide `power.smallest_effect_pp`; a question may override it with `effect` and `effect_reason`.
- New `ref/carry_over.py`: a register board becomes a Prototype word for word (Queue wording, name, ask, why now, what would answer it, every need, agreed); ids `Q<L><n>` → `<L><NN>`; a logic refusal (full-only, defer) is not asked there, a data refusal is asked and refused again by its run; `--check` compares every field and rebuilds each division byte for byte; two runs write the same bytes.
- `ref/evidence-needs.md`: coverage adds no need; "one thing" and "needs form a logic" are question-review tests; a cause word in a Data or Information ask is a review note, never a silent rewording.
- `ref/run_question.py`: live needs only; json outputs by dotted key, one json file shared by several needs; the report header names the question. `ref/scaffold_instance.py --prototype --extract` writes a new Instance's board.md. `ref/write_answer_page.py`: an Instance page has one division per partition, in partitions.md order.
- `ref/run_question.py` `shared_paths`: a run rests only on the shared `src/` modules its scripts import (followed through their imports), so adding a module for one question no longer makes every run STALE.
- A signed change retires a need (`retired:`, successor `supersedes:`) or a whole question (`retired:`, `superseded_by:`), records `changes:` and the new question's `source: {from, signed}`; a retired question is asked nowhere and has no live needs (`asked_partitions`, `live_needs`).
- A cross run also gets `ctx.full`, the whole extract with the script's columns, so a cross question can compare each partition with the extract it is cut from.
- `shared_digest`: a run rests only on the thresholds.yaml sections its scripts and imported modules name (and `power` for a powered question), so a key added for one question leaves every other run current.

## 2.6.0 · 2026-10-02 · Prototype and Instance boards (JL 261002)

- New `ref/prototype-contract.md`: a Prototype board (`insights/Prototype-Insight-<Topic>/`) holds the partitions and `0-Meta/` (input, partitions, thresholds) and one folder per question, `<L><NN>-<name>/` in its level folder `1-Data` … `4-Wisdom` (its question file and its one script; a need is `<L><NN>.E<n>`); an Instance board (`insights/Instance-Insight-<Dataset>/`) names the Prototype and one extract and holds one page folder per question × partition the Prototype asks. Each question says whether it generalizes to a partition: `partitions.meaning` (logic) and `partitions.power` (the minimum detectable effect at the partition's n, computed before any contrast). Status is computed, never typed.
- New `ref/run_question.py` (the one runner: resolve, receipt, filter, power, script, output gate, write) and `ref/scaffold_instance.py` (page folders and their `runs/compute.sh`). No B-J-T-R inside a Prototype; the question id is the address.
- New `ref/record_check.py`: records a read-only check agent's verdict as the page's check Run and, on CLOSE, approves the plan (a v0 plan is promoted to v1.0). `ref/write_answer_page.py` writes Instance pages (header `question:` and `partition:`, no `state:`, items read `results/compute/`). Layout: `0-Meta/` plus level folders `1-Data` … `4-Wisdom`; question folders `<L><NN>-<name>`, needs `<L><NN>.E<n>`, Instance pages `<L><NN>-<partition>-<name>`.

## 2.5.0 · 2026-10-02 · The question owns its run (JL 261002)

- `ref/evidence-needs.md` gains five hard rules: one run serves one question; a compute spec's `measure:` and `by:` quote the ask (`· ask: "…"`); `**Ask covered**:` maps every phrase of the ask to a need, `partial:` or `refused:`; the run is proposed from the register and column list before any task is read; reuse only on an identical output. A Data or Information ask states no cause. Binding no longer prefers extending an existing run.

## 2.4.0 · 2026-10-01 · Work specs and the page flow (JL 261001)

- Work specs: every compute need carries cut, unit, measure, grouping or contrast, uncertainty, rivals and output columns, written from the ask before any task is searched; binding is exact-match only; configs list need ids; refusals need a probe run. `ref/report.md` defines no page shape of its own: every answering page at every level is a haipipe-page Page written through its flow (plan with one Evidence Item and division per need, Draft, adopt, health, page CHECK).

## 2.3.0 · 2026-10-01 · Evidence needs join Logic, Work and Report (JL 261001)

- New `ref/evidence-needs.md`: each question lists evidence needs `<QID>.E<n>` (compute · cite · judge) before any run; the answering page's `answers.yaml` binds each need to result files and the fields its `pass:` names; the page cites `[<QID>.E<n>]` and records `results-read:`; `haipipe-insight-check` returns OK · GAP · STALE · UNBOUND · UNPLANNED per cell and fails an overclaimed ✅.
- New verbs `plan` and `bind`; `climb`, `report` and `check` use them. Three new skills: `haipipe-insight-evidence-plan`, `haipipe-insight-bind`, `haipipe-insight-check`.
- The page ticket is no longer called the join; a config's `answers:` is a cross-check derived from the bindings.
- `ref/report.md` § Shape: the answering page is a Page Face (`haipipe-page`): an objective title, an Opening that carries the answer, one Content division per evidence need; `state:` holds the state word only, `answers:` and `strength:` are their own lines; Aims, States, Files and Log move to `draft/records/`. Replaces the rule that the headline states the finding.

## 2.2.0 · 2026-10-01 · Partition names, not letters (JL 261001)

- Partitions carry no letters: folders `<n>-<partition>/` (`1-full/` … `9-cross/`), page ids `<L><NN>-<partition>`, Question Groups `QG-<partition>-<L>`, `🚫 full-only`; reserved-letter rule removed; examples made generic.

## 2.1.0 · 2026-10-01 · The answering page is the report; page tickets (JL 261001)

- No `reports/` folder and no board store `_results/`: the answering page's `.md` is the report,
  and its folder is also a task folder with `runs/run_bNNjNNtNNrNN_<partition>_<task>.sh`
  call-through tickets (`RESULT_DIR` = the page's `results/<ticket>/`) and those results.
- Register cells name the page (`✅ FI02`); the page names the question back (`answers QI2`).
  The page ticket is the join; a config's `answers:` is a cross-check.
- Verbs `climb`, `settle`, `report`, `check` and the resource laws follow `ref/report.md` and
  `ref/board-contract.md`; `ref/partition.md` drops the `RESULT_STORE` dispatch.

## 2.0.0 · 2026-10-01 · One dataset, one board in insights/; Logic · Work · Report (JL 261001)

- A board lives at `<Project>/insights/<Dataset>-InsightBoard/` (the Project's `insights/`
  world comes back; `haipipe-project`). It holds the registers, `reports/` and the light run
  results in `_results/`; heavy files go to `ProjectResult` with a pointer.
- Data and Information are answered by task runs, joined to questions by each config's
  `answers:` line; the code lives in one DIKW task Block (`b5N_<topic>_dikw`, Jobs j1x–j4x by
  level). Knowledge claims in a report; Wisdom keeps its page and signed handoff.
- `ref/board-contract.md` rewritten: three columns, the climb over runs and reports, the three
  pens (register · report · handoff), the concrete board, the DIKW Block, boards made before
  reports. Register cells settle as `✅ report`; questions may carry an Expected line.
- Verbs: `climb` finds or adds the answering config and runs it; `verdict` writes a report;
  `check` traces every number to a named result.

## 1.7.0 · 2026-10-01 · Reports (JL 261001)

- New `report` verb and `ref/report.md`: one Markdown file per question per partition at
  `reports/<partition>/<QID>.md` (headline, answer, strength, limit, the runs it read), not a
  Page Folder. The Insight workbench shows it as the Report column beside Logic and Work.

## 1.6.4 · 2026-09-29 · outline/ to draft/ in current-layout prose (JL 260929)

- Paths that describe the current Page layout say `draft/`: the plan `draft/<stem>-draft-v<G>.<S>[.<E>].md`, records `draft/records/`, `draft/previous/`, `draft/skill/`, the Evidence Markdown `draft/<stem>-evidence-items.md`, `draft/evidence/bibex/` and `draft/evidence/materials/` (JL 260929: "it should be draft"). Mentions of legacy Pages, retired `outline/evidence/` lanes and the migration keep `outline/`, as do the OUTLINE stage, the Outline table and the `outline:` grammar key.

## 1.6.3 — 2026-09-28 · No content hashes (JL 260928)

- `PARENTS` rows, Task RF packets and the Design handoff reference name path and version, never a
  content hash; leftover hash fields in older records are ignored.

## 1.6.2 — 2026-09-20

- Publish the Knowledge strength rubric and the evidence-supported
  `UNDETERMINED` partition verdict; preserve the signed-handoff boundary for
  licensed partial-final non-answers.
- Migration: preserve old verdicts, signatures, and settled cells; route new
  or reopened work through the owner contracts and Workflow reference.

## 1.6.1 — 2026-09-20

- Clarify Run/Runtime/resource vocabulary; route conditional board and partition rules to references. Define successor question ids and current signed handoff eligibility.
- Migration: preserve existing records; see the scoped migration reference and current handoff contract.

1.6.0 · 260920
- Route Application work to bounded native Runs and explicit resource controls.
- Replace stale procedure/parent-family references with real owners, and define
  bounded standing authorization with durable source and scope.
- Migration: `../haipipe-insight-workflow/ref/migration.md`; no live Board rewrite.

1.5.0 · 260916
- `question|ask` and `verdict` now point at real procedures
  (`haipipe-application/fn/question.md`, `fn/verdict.md`): a person asks in
  plain words, the verb decides level, partitions and lineage, then writes the
  row through `python3 -m live.insightboard ask`.
- `check|review` names `haipipe-page-check`; `for-question` is
  `haipipe-insight-question`; the workbench's audit view is the Check Space.
- Fix the bare `ref/partition.md` path: the file lives under haipipe-application.

1.4.0 · 260916
- Add a read-only board grooming projection: mechanical checks, partial
  register frontier, and the signed Wisdom Handoff gate.
- Make the Design boundary explicit: only a person-signed W handoff named by
  a DesignBoard `reads:` line is bindable; D/I/K pages never cross directly.

1.3.1 · 260915
- Bind the unified public door to one Application `workflow_runtime_id`.
- Clarify that I0-I5 are RunTypes, GI0-GI6 are Runtime control keys, and the
  `partition × DIKW target` Question Group is a derived view rather than a
  Folder, Gate, or Run.

1.3.0 · 260915
- Make `/haipipe-insight` the single public Insight door for both Task-side
  topic/data instances and Application InsightBoards.
- Add explicit `task` and `application` routes, preserve the existing
  `/haipipe-task insight` alias, and keep `partition × DIKW target` Question
  Groups scoped to Application InsightBoards.

1.2.1 · 260913
- Consume current task-side Insight evidence by exact `riNN` execution packet,
  including its base-R and dataset binding; retain items-v1 addresses as
  readable history.

1.2.0 · 260913
- Rebase Application Insight Folders on Page v2: Page workflow passes own
  CONTEXT through CHECK/CLOSE, while GI gates alone advance epistemic state.
- Replace active PageX crossing with Supporting Run evidence, exact semantic
  parent-row lineage, and a frozen signed-W Design input.
- Define Question Group as the derived `partition × DIKW target` view
  (`QG-B-I`, `QG-F-W`) without duplicating questions or creating Folders.
- Migration is OWE-ON-NEXT-TOUCH; historical PageX remains readable only.
- Clarify from the fresh-context A00 field test that a missing calculation for
  an existing cell is that Page's Evidence Item; implementation reuse does not
  create a duplicate register question.

1.1.0 · 260908
- Distinguish topic/data research instances and independently runnable items from Application level Folders; require exact item Result evidence at the signed I1/I5 bridge.

Recovered from the SKILL.md frontmatter summary on 260827, when the family retired the `summary:` field: version history lives here and is never loaded at invocation.

- 1.0.5 (260831): replace the last direct Task-Insight-to-Design route with
  the I1-registered, I5-contextualized and signed pre-climbed external-parent
  bridge. RF remains consumer-neutral evidence.

- 1.0.4 (260831): show the unprefixed subject-first board name as canonical;
  `A<NN>_` is visibly an optional project-local ordering prefix.

- 1.0.3 (260831): align the optional ordered prefix with the canonical
  subject-first suffix: `A<NN>_<DataSubject>-InsightBoard`.

- 1.0.2 (260831): new work writes the canonical `evidence/probe/` lane;
  flat `probe/` is compatibility-only.

- 1.0.1 (260831): names the two lane gates as cross-phase authority transfers,
  distinguishes nested Page-local copilot ticks, and makes GI6 settlement
  mandatory after the GI5 export boundary.

- 1.0.0 (260831): I0-I5 each own a Folder contract with Page Face, Task Face,
  workbench profile, gate and handoff. The door retains lane-wide climb,
  register, partition and signing laws.

- 0.6.0 (260828, page-type normalization): the door NAMES its six page types. Nine contracts share `application/page-types/`, so the folder cannot say which door owns which, and neither door named its own roster — this one named three of six, the design door two of three and not its namesake. The roster is names only: versions are read from disk by `/haipipe-skillset-status` and the dated family table lives in `application/README.md` §Family status, so nothing here can go stale. §The Climb Law also becomes the family's single statement of the chain: the four level contracts now CITE it where they carried four byte-identical copies.

- 0.1.0 (JL 260827): the insight door, symmetric to haipipe-design
- 0.1.0 — the one-dataset law, the Climb Law (a six-level lifting chain), the three pens, the lap (six VERBS: how one cell moves), the two ✋ gates. The lane's phases live in the sibling machine haipipe-insight-workflow (I0-I5 named by the six page types, born the same day). NOT the insight KB retired in application
- 6.6.0 (260717): that was an evidence layer competing with the probe bank; this door holds board law and no evidence.

- 0.2.0 (260827, the first fieldtest's law bin): the handoff verb names the signature artifact (`signed:` row, for-wisdom 0.3.0); a zero-card PROBE is a legal quiet pass (F9 — a skipped phase had cards and ignored them, a quiet pass had none); board.md's spine and close are derived headers reconciled by the register pen, citing the registers (F10).

- 0.3.0 (260828, fieldtest round 2): the F1 repair — 🟡 final joined the settle vocabulary in all four places that still said ✅/🚫 only (three pens, verbs, lap entry, lap ⑤); quiet passes DECLARED ("PROBE: zero cards"), F11; ⬜ annotations are register-pen state, F10; and the AUTO CHARTER: a person may pre-authorize classes (vocabulary re-marks, machine-quotable 🟡 finals, header re-derivations) for one bounded run — signatures and new-computation releases never charterable.

- 0.4.0 (260828, fieldtest round 3): lap ③ POINTS at the probe workbench's card grammar instead of assuming it known (Fr1 — a field desk holding only this family could not raise a card); lap ② names the register pen's mint-time allocation write (Fr7); board.md's ## Pages roster and counts ruled disk-derived, completed by the mint act (Fr8); sibling citations unpinned (Fr9).

- 0.5.0 (260828, fieldtest round 4): MATCH joined the lap — before raising AND again at dispatch, because a released card whose numbers the bank already holds dispatches NOTHING (round 4's field desk refused a false dispatch order on exactly this ground: the 260827 run had the grids, and a re-run would muddy the run identity closed pages bind). The designer's commission was wrong and the desk was right; now the law says so.
