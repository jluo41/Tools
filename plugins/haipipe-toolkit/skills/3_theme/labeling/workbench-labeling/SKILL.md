---
name: workbench-labeling
description: "Open and inspect Labeling inside the shared Block workbench; owns its Blueprint Studio and content mapping. Trigger: labeling workbench, /workbench-labeling."
metadata:
  version: "0.37.0"
  last_updated: "2026-11-27"
---

# Labeling workbench

Read `workbench`, `hai-labeling` and [CONSTITUTION.md](CONSTITUTION.md) first. Shared code owns navigation,
Bands, folds, left tabs, previews and pop-outs; Labeling owns its content and guarded semantic actions.

## Open the Block

Resolve the SPACE and an existing host. Find the owning Block through actual ancestry before opening a Job,
Task, Run or Studio topic. Pass the Block path to the shared `workbench/cli/wb.py`; select internal records through
the Block. Verify the resulting title, URL and selection. Preserve its configured origin, authentication and service;
a requested page change does not authorize a restart. A missing selector is an implementation gap, not a reason
to invent another page or return a child URL.

## Work content

| Block type | Job binding | Task ownership |
|---|---|---|
| Itemization | source snapshot and accepted recipe | `items`: describe, build, revise, check and embedding |
| Guideline Generation | Items, construct and human authority | `labeling-meaning` and `labeling-expression` |
| Labeling at Scale | Items, signed release and executor configuration | `labeling-scanning`; authorized external `eval` when needed |

These are approved design boundaries. Inspect the real record faces and supported writers before allocating work;
independent Job Type values and production adapters are still required. The `labeling-building` and `labeling`
records are supported execution shapes whose artifacts determine their operations; do not manufacture a fourth
Block type from them. Human meaning approval, blind judgments, release signatures and immutable handoffs belong
to their canonical writers. Studio discussion does not duplicate those forms or signatures.

Use shared Report / Studio / Jobs navigation. Job Main summarizes its bound inputs, results and required action;
a selected Task shows its actual operation results, Runs, reviews and guarded actions. Hide the Task row on Main.
Job topic and Task topic describe real groupings only; types are separate. A missing Task layer is omitted.
Labels carry names; marks and layout carry state. Keep history, provenance tags and check tallies off page labels.

## Blueprint Studio

The Blueprint is `examples/Project-Ladder/blueprint/b15_theme_labeling`.
Bands are outer group headings; Studio Type definitions specify content. Use the shared `studio_types` and
`studio_tabs` readers for Band names and order. Do not copy a Band registry into Labeling. Each Studio fold opens
independently; empty Bands and absent type-definition groups are omitted. The shared registry is
`examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/studio-bands.json`, separate from type
definitions. Work owns runtime reload and acceptance of the s75/s77/s79 type-definition retirement; verify the
running host before claiming that integration complete.

- s01–s03 reference Work's Block Structure definition for Itemization, Guideline Generation and Labeling at Scale.
- s41/s42 retain Items and Building procedure instances, owned by the corresponding Task skills. They do not
  require a shared Task Procedure type definition; keep their delivery content, directories and sources.

This inventory requires no additional Labeling Studio Type definition. Ordinary Work Blocks show Studio instances;
do not add mandatory type-definition topics or empty groups. Theme guidance belongs to Theme Guide.

Block Structure keeps Structure / Draw / Skills and derives applicable Job types / Task types views from each
instance’s `types.md` using shared `hai-studio/scripts/block_types_pages.py`. Folder, Job-Task and Studio
each embed their relevant examples. A missing catalog or empty Task inventory is not a passing check.
Each catalog declares all four type levels, for/holds, real source fields and owning skills; absent levels remain
explicit. Independent Job identifiers and actual Work Studio Band names/numbering remain unresolved.
Blueprint Bands do not supply the ordinary Block’s Band design. The shared type definition’s Examples/Draw
requirements need reconciliation. For Labeling, examples stay embedded under their corresponding Folder,
Job-Task or Studio content. Structure renders all three subjects and their embedded examples as collapsible
folder trees using Work’s shared `tree_html` and CSS. Draw’s Job-Task and Studio items use dedicated fragments
and the shared mindmap drawing; its Folder item retains the shared folder tree. Both presentations read the
same verified names and parentage; neither changes real folders.
Variable or undecided names use `〈 〉`; fixed Task types retain contract names. Concrete examples name actual
records or identify design-only proposals. The optional `eval` adapter maps final labels/external gold while
`hai-task-for-eval` requires ModelInstance/AIData; resolve this input boundary before scaffolding that Task. Skills reads real owning files. A one-item view is full width; multiple
items use shared left tabs. Preview links use `ui_parts.open_dot`.

Block Job UI Preview keeps outputs in its appropriate preview/Files and implementation comparison in Checklist;
Delivery/Instances are not separate top buttons for that type. This rule does not remove other Studio types' views.

The generated structure pages come from `b15_theme_labeling/delivery/structure/build.py` and `model.json`.
Change those sources and regenerate their HTML; do not hand-edit generated pages. Keep directories, human canvases
and history intact. Record exact file plans and checks with `hai-trace` before approved changes.

## Sources and implementation boundaries

- `servers/workbench-labeling/labeling_theme.py`: recognized Task types and theme content adapters.
- `servers/workbench-labeling/labeling_focus.py`: current Labeling focus content.
- `servers/workbench-labeling/labeling_block_preview.py`: synthetic design preview renderer.
- `../workbench-task-labeling/SKILL.md` and `servers/workbench-labeling/workbench-task-labeling/`: Task content
  and guarded action ownership. Its independently addressed Page instructions require alignment; take content
  and writer contracts from it, and follow the shared Block-only navigation rule for every entry.
- `servers/workbench-labeling/guide/guide.yaml`: family guidance; `related/papers.md`: verified papers.
- `ref/workbench-table.md`: generated operation/view mapping. Its source is
  `../hai-labeling-building/ref/ref-space-mapping.md`; regenerate with `ref/make_workbench_table.py`.
- [Current topic contracts](ref/topics.md): current rules, guards and unresolved implementation work.

The b02 walkthrough has actual Job, Task and Studio records. b03–b05 contain synthetic design models; they do not
establish actual production Jobs, Tasks or receipts. Their custom shell and the CLI's child-route behavior require
shared-frame integration. A structure preview passing does not establish that integration.

## Check

Run b15's `delivery/structure/build.py --check` with the host's supported Python, then
`hai-studio/scripts/topic_titles_check.py` scoped to b15. Check shared `block_types_pages.py --check` for each instance and run the shared Studio tests when bindings change.
The shared type checker’s empty-level failures remain reported until it can distinguish absent layers from missing
contracts; no-catalog success cannot establish coverage. Type member links must retain the owning Block route.
Open the verified Tailscale Block entry; expand Bands, topics, folder-tree branches, examples and skill sources; check Draw separately. Confirm
readable text and the Block's title/route. Validate skill edits from a fresh context as README requires.
