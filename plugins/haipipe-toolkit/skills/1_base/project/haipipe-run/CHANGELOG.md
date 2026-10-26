## 0.36.0 · 2026-10-21 · the Workflow is haipipe-run's

- The haipipe-workflow skill is merged in: `ref/workflow.md` (its body and the unique part of its concepts),
  `ref/plan-schema.md`, `ref/workflow-runtime.md` and `ref/template.workflow.js` moved here with their history; its
  JavaScript API page is dropped, since Claude Code's `workflow-authoring` skill is that reference. A planned graph of
  Runs is a Run question; only 28 of 387 Physician-SPACE Tasks wrote a plan.yaml. Every pointer (the type skills and
  their plan samples, haipipe-task, the paper, insight and labeling workflows, haipipe-work) now names these files.

## [0.36.2] — 2026-10-26

Shorter description (1297 -> 455 characters): what it does, when to use it, its trigger words; aliases and old command names kept (diagnostics/descriptions/261026.yaml). (describe 261026)

## [0.36.1] — 2026-10-25

Links, commands and companions repointed at the helper skills merged into `haipipe-nn`, `haipipe-end`, `haipipe-data`, `haipipe-task-for-fit`, `haipipe-task-for-agent` (now `_parts/<name>/PART.md`). (merge-parts 261025)

## 0.35.0 · 2026-10-21 · Each Run says its role; rebuilt receipts; prune to _old

- `scripts/run_roles.py` (from LLMRec `work/_tools/`, which now loads this copy): proposes each Run card's `role:`
  from its name and writes it after `kind:`, for a Task's Runs only (a Block's drawings take no role); `haipipe-project ladder.py update --today --apply` writes the roles a
  work Block lacks through it. `ref/receipts-and-inventory.md` adds `role:` to the card.
- `ref/receipts-and-inventory.md` § Rebuilt receipts: a Run that keeps only a migration's stand-in gets a receipt read
  from the files it left, marked `receipt: {rebuilt_on, rebuilt_by, read_from}` (LLMRec b01, 25 Runs); the rule says what to read for any Run,
  an analysis Run included, and that the tool is the Project's.
- `scripts/prune_runs.py --to-old`: moves each pruned Run and its configs to
  `work/_old/<bNN>_pruned_<YYMMDD>/<jNN>_<task>_runs/` instead of deleting it, so a Run git does not hold is kept.
  Tests: `test_run_roles.py`, `test_to_old_moves_an_untracked_run_and_its_config_instead_of_deleting`.

## 0.34.2 · 2026-10-20 · Build figure / table opens in 4 · Display

- run-types-by-space: a draft Task's tabs are seven; `run-display-<slug>` opens in 4 · Display, Revise's three in 5 · Revise.

## 0.34.1 · 2026-10-20 · A draft Task's buttons by step tab (b32 s41)

- `ref/run-types-by-space.md`: the Page Task table is now the Draft Task table, each button under the step tab it
  sits in (Studio · 1 · Plan · 2 · Write · 3 · Evidence · 4 · Revise · Delivery), with the Studio's `run-draw-<sNN>`;
  the names come from `task_draft.PAGE_RUN_NAMES`.

## 0.34.0 · 2026-10-19 · Keep only meaningful Runs (JL 261019)

- JL 261019, on a drawing that still showed six replaced parse Runs: "why not delete them!!!! why we have the new
  run????" and "we will just keep the meaningful runs". SKILL.md gains `## Keep only meaningful Runs`: a hard Run
  stays while it is current, open, or read by something in use. A Run another Run supersedes, or one that never ran
  and is not planned, is pruned once nothing in use reads it. Immutable means never edited, not kept forever; git is
  the archive.
- The title "preserved history" becomes "only meaningful Runs". The Result paragraph no longer says to preserve the
  historical Result. The "Choose the next action" table prunes the replaced Run. `ref/identity-and-history.md` and
  `ref/receipts-and-inventory.md` (the Superseded row) say the same, and so does haipipe-task's
  `ref/runtime-yaml-schema.md`.
- `scripts/prune_runs.py`: new. A dry run prints each hard Run's verdict and who reads it; `--apply` deletes the
  Runs it marks, with their configs; `--only` prunes a named candidate once a person judges its reader stale. It
  counts as readers: configs, tickets and run cards of Runs that stay, code that names the Task and the Run, and
  Pages outside the Task. It does not count receipts, its own Task page or Studio faces; it lists those to update,
  with the heavy folders to remove where they live. A Run counts as ran when its config's output path holds
  files. A Run whose output is not on this machine is marked check, never pruned by `--apply`.
  `tests/test_prune_runs.py` checks it.
- First used on Physician-SPACE LLMRec `work/` (442 hard Runs), JL 261019 "go through the whole runs":
  - The first version marked 172 b01/b02 Runs "never ran", nearly all wrongly: their output is in `_WorkSpace/`.
    After the store check, 33 were marked to prune and 59 to check.
  - By hand, some prune verdicts were kept: two that did run (their store folder named by a collection version),
    two pricing snapshots a cost report reads by a shortened name, and b04's planned tickets.
  - 14 b01/b02 deletions were restored from git and handed to those Blocks' owner sessions. b02's status export
    globs its pre-SDK config folders, a reader the first version could not see.
  - b03 (this session's Block) lost 23 Runs; every Run its pipeline ticket calls still exists.
- A fresh-context reviewer of the first version found more problems; all are now fixed and tested
  (`PruneRunsCasesTest`):
  - same-named Runs in sibling Tasks kept each other (the tool now reads the Task number just before the name);
  - frozen configs of replaced Runs counted as readers;
  - deleting a middle Run lost the supersedes chain (`--apply` now marks the older Run `status: superseded`);
  - bare `--only` names matched several Tasks;
  - nothing checked that git held a copy;
  - companion configs such as `driver_tags_r03.yaml` were left behind.
  SKILL.md adds who prunes (the Block's owner session), the snapshot warning, and what the tool cannot see
  (`_old/`, short ranges in prose).
- No content hashes (JL 260928), swept here: the SKILL's reuse row and heavy-output pointer, and
  `ref/identity-and-history.md`, `ref/receipts-and-inventory.md` and `ref/run-catalog.md` now name versions
  and dates, not hashes. haipipe-task 1.15.1 stops its Ticket template from writing sha256 into `heavy.yaml`.
- A paper Board's Pages cite Runs by address range ("b03.j01.t02 r08 to r13"), and the tool missed them
  (LLMRec MISQ story E18, 261020). It now reads addresses, alone or as a range, and counts any Studio face outside
  the Run's own Block as a reader. Before, every Studio `.md` was a mention, so a story citing a Run could not
  keep it.

## 0.33.1 · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## 0.33.0 · 2026-10-07 · A button is named by its Run (JL 261007)

- A theme names its own buttons in `Theme.run_names` (frame.py `named`); the catalogue lists the themes named so far: paper (itself), work, discovery, labeling, cowork; insight and design are open.

- `ref/run-types-by-space.md` rule 6 and the SKILL's Runs-by-Space note: the Runs panel names each button by the soft Run it makes, `run-<type>-<target>`, with what it does in small under it; a target the open folder fixes is filled in (`run-face-b03`), one still to choose stays a placeholder (`run-draw-<sNN>`). Buttons that make the same Run are one: Idea Studio's add, redraw and save-a-session are `run-draw-<sNN>`, its cards one per topic with its passes. The Page Task's buttons show their Page Runs (`run-scratch-<target>`, `run-structure-<slug>`, ...). Code: `servers/workbench/frame.py` `run_type`, `PAGE_RUN_NAMES`; `runs_panel.py` shows the name and the line under it.

# haipipe-run · CHANGELOG

## 0.32.0 · 2026-10-07 · Runs by Space; the soft-Run writer (b03 s21)

- Every workbench button names its owning skill (b03 s21: "every frame button names its
  skill"): `ref/run-types-by-space.md` lists each button of the frame, Block · Job · Task and the
  Page Task, with its skill and its Run; the frame's run types carry the same `skills:` field.
- `scripts/soft_run.py`: new, writes a soft Run's `run.yaml` and ticket (`new`) and its passes
  (`pass`), so no person types the card. A name with a date in it is refused (JL 261006: no
  `<MMDD>` in a soft Run's name; the date is in its passes).
- `tests/test_soft_run.py`: the writer, and that every skill the table names exists.
- `soft_run.py` takes a hyphenated type (`add-venue`, `freeze-predictions`; the target is always
  given, so the name is never split) and `--signs` (paper and design run cards carry them).

- 261007 (version unchanged): Design names every Run `run-<type>-<target>`, hard ones too; `kind:` in run.yaml says
  which, a design hard Run's ticket is its run.yaml, and the description, the Run catalog's Design rows and the
  stale design-commission and Design Delivery lines now say so.

## 0.31.0 · 2026-10-06 · Hard and soft Runs, one folder each, passes (JL 261006)

- The ladder ends in passes: Block → Job → Task → Run → pass (JL 261006: "for the run, it
  can have multiple pass"). A Run is one folder in its scope's `runs/` (JL: "one folders, all
  the run folder in the runs/"); `results/` merges into it as a hard Run's `result/`.
- Two kinds, by where the output lands (JL: "hard-run will only add the results to the
  runs/rNN folder, but soft-run can add to like the scope's studio, reports, draft,
  delivery"). Hard `rNN_<slug>`, ticket `.sh`, evidence, work Tasks only. Soft
  `run-<type>-<target>`, ticket `.md`, any level, no date in the name (JL: "it should be one
  run"; "yes to all"). A Page's evidence Runs are soft; a Page computes no new facts.
- `run.yaml` is the one card per Run, written by tools only. A hard Run may carry several
  type tags under one close rule. A design commission is soft.
- Existing layouts stay readable until haipipe-project 0.11.0 `update` moves them.

## 0.30.1 · 2026-10-05 · Moved under skills/project/ (JL 261005)

- The skill moved from `skills/run/haipipe-run/` to `skills/project/haipipe-run/`, beside
  `haipipe-project`, so the Run level sits with the Project ladder it belongs to (JL 261005:
  "I think they should be run the run into the project as well"; then "please do this now").
  Same depth, so its own relative links are unchanged; 17 files that pointed at
  `run/haipipe-run` now point at `project/haipipe-run`. The name stays `haipipe-run`.

## 0.30.0 · 2026-09-29 · Heavy output in ProjectResult (JL 260929)

- A Result is light: a Task Run's heavy output has its own folder, `_WorkSpace/ProjectResult/<Project>/<block>/<job>/<task>/<run>/` (Ticket `HEAVY_DIR`), with the pointer `heavy.yaml` in the Result; a pipeline asset goes to its stage store.

## 0.29.0 · 2026-09-29

- Result, evidence, and closure: **A Result is light.** Heavy Run output (model, array, cache, row-level table, any file over 10 MB) lives in the owner's heavy store (`_WorkSpace/` for Task Runs) and the Result keeps a pointer (SPACE-relative or `$VAR/...` path, size, hash); never a copy or a symlink in the Result or its Folder (JL 260929).

## 0.28.1 · 2026-09-28

- A Page's delivery builds are one fixed Run per lane (`run_delivery_<lane>`), not numbered RD ids (`SKILL.md`, `ref/identity-and-history.md`, `ref/run-catalog.md`; JL 260928).

## 0.28.0 · 2026-09-22

- `ref/run-catalog.md`: Page RP gains the `revise` kind (`rp-revise-NN_<target>`).

## 0.27.0 · 2026-09-20

Define a Run as a bounded commission with preserved attempts; explain Workflow
Spec and instance lists with dependency/Route graphs. Split the entrypoint into
shared rules plus catalogue, identity/history, and receipt/inventory references.
Index current Task, Discovery, RP/RE/RD, delegated writing, independent display,
Insight, Design, Paper judgment/compile/response, and Labeling profiles. Preserve
native schemas and historical identities; retire active Design Adopt examples.
Clarify waiting/null timestamps, incomplete allocations, owner-qualified counts,
RI binding versus execution-version counts, and closure versus promotion.
Align direct catalogue, Workflow, Task, Page/Paper, and presenter consumers.
New shell Tickets verify declared input bytes, fingerprint the commissioned
contract, archive prior attempt receipts, exclude simultaneous writers and
refuse to overwrite closed Results. Run readers diagnose missing/duplicate
records, resolve declared Task stores and keep recovery rows visible. Existing
copied Tickets and published Results are not migrated by this source update.

## 0.26.1 · 2026-09-15

Replace Phase-owned Run profiles with Workflow Run Spec graphs. Gate and Route
now belong to each Run; distinguish Run Type, Run Spec, and Run Instance; make
human decision Runs conditional on bounded commission, durable receipt, and
independent closure; retain RP feedback as Steps and reopenings as Versions.
Entry gates default open, exit close semantics are mandatory, terminal routes
default to `CLOSE`, and gate/route modes are `human | automatic | agent |
hybrid`; phase/controller labels are adapter metadata, not ontology. Add the
Workflow Runtime boundary: one aggregate `workflow_runtime_id` records frontier
and indexes Run-owned control decisions while child Runs retain owner-native
identities, Tickets, Results, and receipts.
Clarify that Workflow Runtime is optional aggregate infrastructure and that
Skill/interaction/projection behavior belongs to Run Spec × Workspace Cells,
not directly to the Run Spec or Workspace.

## 0.26.0 · 2026-09-14

Clarify that `rp-struct-01` is one multi-person Structure Run containing the
SHAPE and SURVEY cycles, with later structure ids reserved for independent
post-closure goals.

## 0.25.0 · 2026-09-14

Align the Page-facing Run contract with typed `rp-struct-NN`, `rp-sec-NN`,
`rp-para-NN_Pxx[-Pyy]`, and `re-value/display/cite` identities. Clarify that
`DISPLAY` covers tables and figures and that `V_`, `D_`, and `C_` placeholders
are labels bound to a Result/Card, not child Runs.

## 0.24.0 · 2026-09-13

Define the Page projection as Run P, Run E, and Supporting Runs inside Workbench
Outline. Native external Runs keep their identity and are inspected by
reference rather than copied into the Page.

## 0.23.0 · 2026-09-13

Make `riNN` the native Insight Run binding: it points to one normal R ticket,
freezes a new dataset, and owns an independent Result history. A changed
dataset allocates a sibling RI instead of overwriting R or masquerading as a
rerun/version of the old dataset.

## 0.22.0 · 2026-09-13

Define the Task–Page cross-face handoff: Page proposes without reserving a
Task identity, Task returns a native Result, and Page binds it by full identity,
path, and fingerprint without collapsing either closure boundary.

## 0.21.0 · 2026-09-13

Require new runtime receipts to use offset-bearing RFC 3339 date-times; retain
date-only values as readable legacy history without pretending they establish
within-day order or duration.

## 0.20.0 · 2026-09-13

Add the native `rlNN` Labeling Run family while preserving one generic Level-4
Ticket/runtime/Result contract.
