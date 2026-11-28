# Update a Work Block

`/hai-work update 〈Block〉` aligns the named Block's records and embedded
Job/Task selections with their current contracts. It does not execute pending
work or certify completion. `--check` is strictly read-only: no record writes,
installation, service start or restart.

## Inspect

1. Resolve the SPACE and Block. Read repository guidance and git status. Preserve
   identifiers, untracked material and changes owned by other sessions.
2. Read `board.md`, immediate Job faces, their Task faces, relevant Run cards and
   receipts, Studio bindings, Questions, interactions and delivery records.
   Inventory the scope actually inspected; do not infer full coverage from one page.
3. Resolve the theme and Block role from its records and owning reader. Work and
   Blueprint have different purposes; CoWork, Discovery and specialized themes
   retain their content and writers.
4. Read [workbench](../../../../1_base/workbench/hai-workbench/SKILL.md) and its
   [page rules](../../../../1_base/workbench/hai-workbench/ref/work-pages.md). Resolve
   the owning Block before opening it, then select its Jobs and Tasks in place.
5. Inspect an already-running host. In `--check`, if no host answers, report browser
   verification as pending and finish the independent source checks.

Read the applicable `hai-block`, `hai-job`, `hai-task`, `hai-run`,
`hai-studio`, `hai-report` and `hai-interaction` contracts before editing
their records. Resolve skill locations rather than guessing their schemas.

## Compare records with the rendered view

The shared readers live under `plugins/haipipe-toolkit/servers/workbench/`:

- `page/block_index_page/focus_page.py`: the shared page composition.
- `page/job_task_views/work_frame.py`: Work content.
- `page/job_task_views/focus_jobs.py`: embedded Job and Task selection.
- `page/job_task_views/work_sections.py`: authored content sections.
- `side_pane/files_tree/work_files.py`: real folders and their roles.

| Content | Inspect | Required evidence |
|---|---|---|
| Overview | Goal, requirements, close condition and authored sections | The selected record's face and linked sources |
| Jobs and Tasks | Explicit types, groups, faces, dependencies and Runs | Records agree with the owning type contract and visible selection |
| Findings | Recorded Data, Values, Displays and applicable maps | Actual source bindings and readable outputs |
| Delivery | Artifacts, acceptance and usage | Recorded decisions and working artifact links |
| Blueprint previews | Real example Blocks and current Studio bindings | The live example and the exact part reviewed |
| Supporting content | View/topic associations and Block-level aggregation | Explicit associations supported by the reader |

Do not derive a type, goal, use case or acceptance from a folder name. Empty
sections are omitted; do not create placeholder records to fill them. Read metadata
from the face's supported header fields, not from an example code fence. Add only
headings and fields the relevant owner and reader actually use.

## Apply approved alignment

List the exact paths and changes required, then follow the repository's approval
rules. Keep changes within the named Blocks and approved scope.

- Preserve Questions, decisions, IDs, authored content, Run records and receipts.
  Repair a link only when its intended existing destination is established.
- Keep group, type and use-case fields distinct. Keep unresolved assignments
  unresolved; do not rename records to make a type table appear populated.
- Reconcile a face's work state only from receipts, reviewed outputs and the
  owning lifecycle rules. Nonempty result folders do not prove successful work
  or acceptance. Do not mark a Task complete without its required close evidence.
- Use the one owning writer for changes. Generated content is changed through its
  generator, preserving human-authored material and IDs.
- Stable paragraph IDs enable comments on authored sections. From the toolkit
  root, `python servers/workbench-work/paragraph_ids.py 〈page〉` reports proposed
  IDs; `--apply` writes them when approved. Never renumber existing IDs. A builder
  must preserve IDs in its own output so rebuilding does not erase comment targets.
- Example entries point to real Block-owned selections. Repository demonstrations
  use repository-local paths. Private cross-SPACE example mappings belong in
  `.server_config/workbench-examples.json`, not in public skill text.
- Reuse the shared layout, file tree and pop-out viewer. An approved design still
  awaiting implementation stays in the owning plan until the real behavior passes.
- A service reload is a separate operational action: identify the source checkout,
  coordinate with active sessions, preserve launch settings and verify afterward.
  Never perform it in `--check`.

## Scope supporting records and acceptance

Inside a view, supporting records follow their supported `view:` or topic
association. A face can name `for:`; a Run card can name `target`/`for`; Studio tags
can supply the reader's fallback association. Preserve explicit links and use only
keys accepted by the current reader. Block-level aggregation does not authorize
copying every record into every view.

Checklist asks whether this selected view meets its requirements. Read the level,
view and type skills first. Each check names one observable outcome, its owning
rule and its evidence. Reuse the existing topic's `## Checklist` or supported
scoped face. Use marks and the shared controls for page presentation; record a
required action or failure reason where it is needed.

Distinguish verified, unfinished, blocked, untested and justified inapplicable
requirements in the underlying records. Reopen an affected check with a reason
when a change invalidates its evidence. A recorded walk proves that walk, not the
entire skill contract. The renderer reads authored checks; it does not generate
or certify all requirements. Report a missing checklist association rather than
creating a dummy topic.

Files presents real folders under Block, Maintain, ReadFrom and trace-derived
Touch roles, as implemented by the shared reader. Keep SPACE-relative paths and
actual nesting. Positions can change with sorting; path identity and click targets
must not. Show actual `_WorkSpace` or code folders only when applicable and within
the served root. Omit empty roles and preserve the selected scope.

## Verify

1. Re-read changed records and the diff for lost material or unintended state
   changes. Run the owners' appropriate format checks. A repeat update should
   produce no new change without new source data or requirements.
2. Open the Block and select every affected Job/Task in place. Verify actual view
   content, associations, aggregation, links, file preview, pop-out and close.
   A source check is not a browser check. Use `hai-ui` for UI verification.
3. For Blueprint work, open the configured examples and check the precise behavior
   against the owning type. Distinguish implemented behavior from approved plans.
4. Report changed paths, the checked Block link, checks performed and remaining
   gaps. Record alignment, UI verification and work completion are separate
   conclusions. Never claim every view or SPACE was checked from one example.
