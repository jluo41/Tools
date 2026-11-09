# Update a Work Block to the current focus UI

`/haipipe-work update <Block>` is an agent procedure. It aligns the specified
Block and its existing Job/Task pages with the current shared renderer. It does
not copy a demonstration Block, execute pending work, or certify completion.
`--check` runs the inspection and verification without edits or server restarts.

## 1. Inspect the actual work

1. Resolve the SPACE root and exact Block. Read its repository guidance and git
   status. Preserve unrelated changes, existing identifiers and untracked content.
2. Read `board.md`, the immediate Job faces, their Task faces, Questions and work
   bindings, Studio topics, relevant Run cards/receipts, and delivery records.
   Inventory child pages before claiming the whole Block was checked. Read large
   result files only as necessary; do not enumerate private datasets into UI text.
3. Resolve the theme through the existing workbench reader. A folder under `work/`
   may be a specialized Prototype or claimed by another theme. Route specialized
   Paper, Design, Insight or Labeling pages to their own skills. CoWork and Discovery
   share the frame but retain their own records and content; do not reclassify them.
4. Identify **Work Block** or **Blueprint Block** from its purpose and existing
   `ui-*` page references. Being in a `blueprints/` directory is insufficient. An
   ordinary data/model/paper-results Block gets no theme-development views.
5. Open the current focus page through `/wb` on the existing SPACE host. Distinguish
   missing source records from an outdated renderer. A Block already on the current
   renderer may need no file edits. In `--check`, inspect the running host without
   starting or restarting it; if unavailable, report browser verification as pending.

For editing faces, read `haipipe-block/ref/board-contract.md`, `haipipe-job` and
`haipipe-task` as applicable. For topic changes read `haipipe-studio`; for Questions
and work links read `haipipe-report`; for Interactions read `haipipe-interaction`.
Resolve these installed skills or their package locations; never guess their schemas.

## 2. Compare with the current contract

Use `../workbench-work/SKILL.md` relative to the **haipipe-work skill directory**
and the current `servers/workbench/{focus_page,work_frame,work_files}.py` readers.
From the Tools root, the b17 `ui/block-views.md`, `job-views.md`, `task-views.md`,
`run-views.md` and `view-guide.json` document the views. Do not copy their illustrative content.
The shared UI determines the layout; the Block's records determine what it says.

| View | Inspect and align | Do not invent |
|---|---|---|
| Overview | Goal from the level's face; Requirements and close conditions; MindMap from existing topics, Questions and work | Goals or requirements inferred only from folder names |
| Status | Existing Jobs/Tasks/Runs and recorded states; topic tabs with related B–J–T–R on the right; authored Dependencies | New Job types, synthetic Runs, or a generic Next Steps list replacing View BJTR |
| Findings | Actual outputs, values, answers, maps, and theme-specific records with their sources | Findings copied from a template or completion inferred from a file's existence |
| Delivery | Actual artifacts, recorded acceptance and usage | Acceptance, release, or delivery merely because a build exists |
| Blueprint UI views | Configured real example pages, type/view matrix, walkthroughs, review evidence | Block UI / Job UI / Task UI / Run UI on an ordinary Work Block, or an unsupported level's example |
| Title line | The type and use case under each title come from the records: a face's `use-case:`, a work Task's `task-type:`, a Run's `type:` | A `use-case:` guessed from a folder name, or one copied from the Block to its Jobs |

Current source formats include header `spine:`/`goal:`, `close:`, `use-case:`
and `view:`, and authored `## Requirements`, `## Dependencies`, `## Acceptance`,
`## Usage`, `## Checklist`, `## Decisions` or `## Things to Know` where the relevant
reader uses them. Header metadata belongs before the first `##`; an example in
a code fence or body paragraph is not metadata. Keep the owner's current schema.
Do not add every heading to every file simply to fill a screen.

## 3. Apply only supported changes

- `update` authorizes routine, reversible content and link alignment within the
  named Blocks. Briefly state the concrete differences, then make those changes;
  no extra confirmation is needed for the already-requested update.
- Preserve IDs, Questions, answers, decisions, Run history, receipts and work state.
  Repair a broken link when its intended existing target is unambiguous. Do not
  rename folders, relocate artifacts, prune Runs, execute jobs, or release outputs
  as part of presentation alignment.
- Keep explicit use cases on the owning face. A Job's use case is not inherited
  from the Block or guessed from its name. Reuse the actual supported Job type.
  A Block or Job whose purpose clearly matches one use case of its type table may
  get a `use-case:` line; when two fit, leave it unwritten and record the gap.
- Bring stale Task states up to their Runs: a face whose `state:` is empty, NOT
  STARTED or OPEN while its Runs hold non-empty `result/` folders becomes
  `🟡 RESULTS IN, UNREAD · <n> of <m> Runs returned`. Never write DONE: a person
  closes a Task. Skip faces another session has not committed.
- A Job face without `emoji:` may get one that names what the Job does (the Status
  row shows it); keep any emoji already chosen.
- Blueprint example entries must point to existing pages of the correct level.
  Public Tools blueprints use repository-local demonstration pages. Cross-SPACE
  use-case examples belong in the ignored deployment mapping
  `.server_config/workbench-examples.json`, never private paths/origins in public
  skill files. Verify both the source face and the resulting link.
- Reuse the shared frame, folded sections, left tabs/right content, file tree and
  large pop-out. Do not generate a separate static page or duplicate renderer for
  each Block. A current focus URL uses `layout=focus&section=report` with the chosen
  `group`; setting `workbench-layout: workflow` is not a prerequisite.
- If a needed value or association is unclear, retain the original and record the
  specific gap. Finish independent corrections. Ask only for the unresolved
  substantive choice; missing data is not permission to fabricate it.
- If a server is stale, identify its source checkout and existing host first.
  Reload that host when needed and authorized; preserve its origin, binding,
  authentication and terminal settings. Do not reinstall, pull, or update every
  SPACE as an incidental step. Report a missing server capability as a code gap.

## 4. Scope Around the Work and its Checklist

The eight sections are **Studio · Interactions · Decisions · Things to Know ·
Checklist · Timeline · Skills · Files**, in that order, without number prefixes.
Inside a view they use one consistent selection of linked topics, pages and Runs.
On the right rail they include the current page and its descendants across views.
Do not attach all Block records to every view to avoid an empty section.

The current reader resolves explicit `view:` first, then a valid topic association
(`for:` on page faces, `target`/`for` on Run cards). Studio topic tags can match a
view when no explicit view is authored. Canonical keys are `overview`, `standing`
(Status), `findings`, `delivery`, `ui-block`, `ui-job`, `ui-task`, `ui-run`. Status also lists
every Interaction still waiting on the person unless the form names another view (261109). Use these only
when the record's content supports the association. Preserve an explicit existing
association; genuinely cross-view records remain available on the rail rather
than being assigned arbitrarily to one view.

Checklist answers: **Has this Block/Job/Task view met its requirements?**
Read the relevant level, view and Task-type skills before defining checks. Each
item names one observable outcome and links its evidence and owning skill rule.
Separate `Done`, `Open`, `Blocked`, `Not checked` and justified `Not applicable`.
A changed file is not a passed browser check; a recorded walk is only one check.

Use the existing owning topic's `## Checklist`, with its supported view association,
or another existing scoped face that the renderer reads. Reuse its format; a table
is appropriate when evidence needs columns. For example (illustrative, not a record
to paste as completed):

| Check | State | Evidence | Skill rule |
|---|---|---|---|
| Selecting a Status topic shows only its linked Tasks and Runs | Not checked | Link to the actual topic and subsequent browser check | workbench-work: view scope |
| Every displayed delivery opens its recorded artifact | Not checked | Link to the actual delivery record and checked artifact | haipipe-delivery: source ownership |

Mark Done only after checking the criterion. Preserve unrelated completed items;
reopen an affected item with a reason if new changes invalidate its evidence.
If no suitable owning topic exists, report the missing checklist association;
create a topic only when justified under `haipipe-studio`, not a dummy topic to
make a section nonempty. Current UI renders authored checklists and derives
walkthrough presence; it does **not** automatically generate or certify all skill
requirements. Keep unresolved checks visible in the update report.

Files groups reference real sources: Blocks (including Runs), Tools · Skills and
Tools · UI; Workspace means the SPACE's actual `_WorkSpace`, Code its actual `code`
folder, only when present and within the served root. Do not create placeholder
directories. The view's Files uses its selected sources; the rail is broader.

## 5. Verify and report

1. Validate changed faces and their linked files using the owning readers. Re-read
   the diff for lost content or state changes. A repeat update should find no new
   edits unless the underlying requirements or source records changed.
2. Open each applicable view on the Block and every changed Job/Task page. Check
   the current view buttons, numbered Review Content, unnumbered Around the Work,
   scope versus rail roll-up, and actual example/delivery/file links. Exercise
   topic selection, file preview, large pop-out and close. Check narrow layout
   when layout code changed. Use `haipipe-ui` for UI verification.
3. Blueprint only: verify each configured level's example matches its type; the
   relevant walkthroughs and review records must be reachable. Missing evidence
   remains Open or Not checked, never silently marked passed.
4. Report changed paths, the actual checked page link, passed checks and remaining
   gaps. Distinguish `content aligned`, `UI verified` and `work complete`; an update
   grants only the first two when supported. Use the Block map for work progress.
   Never claim every SPACE or every view was checked from one example.

The legacy `/wb update` migration has a separate scope (folder moves, proposals,
Run metadata and classic workflow setup). It is not an alias for this procedure.
Use it only for a separately requested structural migration and follow its own
dry-run and approval rules.
