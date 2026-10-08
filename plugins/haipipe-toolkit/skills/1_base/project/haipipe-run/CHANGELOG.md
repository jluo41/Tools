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
