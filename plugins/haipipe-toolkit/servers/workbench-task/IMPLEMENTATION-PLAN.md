# Task Workbench · question reports and working Views

## Goal

Deliver the agreed Task Workbench on the existing host: one Task Block,
four working Views (Task, Roadmap Studio, Related Paper, Progress), stacked
Question cards with Logic / Work / Report columns, and Block-owned report
Pages in `reports/` beside `studio/`. Make the skills describe the same
storage, ownership and authoring workflow as the running interface.

## Ownership

| Owner | Responsibility |
|---|---|
| `haipipe-task` | Block Questions, their links to native Jobs / Tasks, and the Block report placement contract. Native P-B-E-R and Run identity stay at Task level. |
| `haipipe-page` | Report Page structure, Draft, evidence references, Content adoption, CHECK and release. Reuse this skill; introduce no second report-writing lifecycle. |
| `haipipe-board` | Board membership and source navigation. Report Pages are reading material, never executable `tNN` Tasks or inferred Jobs. |
| `haipipe-workbench-task` | Read and navigate the four Views; explain how Questions, Reports, resources and drawings correspond to disk. |
| Shared Guide / Studio | Reuse family Guide mounting and the existing Excalidraw service and save mechanism. |

## Storage and reading

- `board.md` remains the Block's authored source. An optional `## Questions`
  section holds a fenced YAML question register: stable id, question, logic,
  work references and a relative Report Page path. A `## Related resources`
  section holds source links, contribution and related Question ids.
- `reports/qNN_<topic>/qNN_<topic>.md` is an ordinary same-stem Page. Opening
  supplies the answer summary; the Page's native `state:` is shown as declared.
  Evidence, limits and next actions live in the report's Content. Its Draft,
  process records and Page Runs remain inside that Page Folder.
- `studio/*.excalidraw` holds freeform drawings. Each file has an independent
  collapsible row and embedded editor. Existing `diagram/` remains readable.
- Execution receipts and `workflow/report.yaml` remain with their existing
  Task owners. A Question Report references results without copying them or
  moving native execution into the Block root.
- Task and Progress read the same Question / Report snapshot. Missing reports,
  invalid references and changed evidence are visible; Run completion never
  supplies a Question's answer state.

## Implementation sequence

1. **Contracts and skills.** Add a focused Block Questions / Reports reference
   and examples; update Task hierarchy, scaffold instructions and Workbench
   guidance. Resolve Question report vs P-B-E-R report routing explicitly.
2. **Source support.** Implement bounded readers for the optional Block
   registers and report Pages; preserve existing Job / Task / Run readers.
   Provide a small authoring helper for a new Question report scaffold and
   source-register entries without overwriting existing work.
3. **Working interface.** Replace the old top-level Progress / Runs / Scope
   navigation with Task Space and four Views. Keep native execution detail
   nested under Work and keep unassigned work visible. Mount the shared Guide.
4. **Studio and resources.** Embed existing Block drawings, support a fresh
   drawing through the native Excalidraw path, and show linked resources with
   their Question associations. Persist fold state locally; avoid refreshing
   an active drawing editor.
5. **Delivery.** Update the synthetic demo, design source mapping and server
   documentation. Start an isolated preview through the existing host and
   provide the reachable preview and source links. Conduct the repository's
   fresh-context skill review; do not add or run an automated test suite for
   this request.

## Completion criteria

- Skills and code agree on the Question register and `reports/` Page layout.
- A Block with Questions renders three columns and opens each full report in
  the existing Page reader with a Page Workbench link; a Block without Questions
  keeps its work visible.
- All four working Views read actual sources and have honest empty states.
- Drawing editing uses the native Excalidraw save path and independent rows.
- Shared Guide and existing execution ownership are preserved.
- The implementation and a runnable example are delivered; remaining limitations
  are stated rather than presented as implemented behavior.

## Status

Implemented on the existing host.

- Task 1.10.0 owns the optional registers and the preserving authoring helper.
  The helper creates an ordinary same-stem Page plus `page.toml`; Page owns
  subsequent writing. Workbench Task 0.2.0 documents the four working Views.
- The interface projects registered Questions, nested native Work, report
  Pages and linked evidence. Complete reports use the existing Page reader,
  with a separate Page Workbench link so a report without a Draft is readable.
- Roadmap Studio reuses native Excalidraw files, independent folding rows and
  the native edit lock/save path. Related Paper has a source-register form.
- Shared Guide is mounted and coordinated with the shared-foundation session;
  its Task profile names the four Views and the sibling reports/studio folders.
- A fresh-context skill review applied the handoff to a realistic comparison
  Question. The old View description and a conflicting Page Result-path example
  were corrected. Follow-up review found no blocking handoff conflict.
- The synthetic example was launched on the full host. The actual UI displayed
  all four Views, Guide, and a complete report. A native Excalidraw edit was
  saved into the example Block's drawing file. Screenshots accompany delivery.

No automated tests were added or run for this implementation. The preview uses
synthetic records. Answer state is authored, never inferred from Run completion;
evidence-change warnings cover linked local files, not external resources.
