s03 · A draft is a Task type
============================

**Tags:** `base` · `workbench`

**Stage:** agreed

**Topic:** JL 261014: "for the theme, we can have different type of tasks, and the tasks can have
different layout, for the Tools/plugins/haipipe-toolkit/servers/workbench, we will have the task type
of draft". A theme's Tasks come in types (the face's `task-type:` line), and each type has its own
layout on the shared frame. `draft` is the first type the base lays out for every theme: a Task that
writes (a paper Section, a report, an email, a discovery or insight page) opens on
`servers/workbench/workbench-task-draft/`, and its theme adds its own Spaces on top. The same day
`servers/haipipe-board` (empty) was deleted and `servers/haipipe-page` was folded into
`workbench-task-draft/reader/`.

**Feeds:** none (the Studio records this, not a Question report)


Files
-----

```text
s03-draft-task-type/
├── s03-draft-task-type.md          this face
├── s03-draft-task-type.excalidraw  the drawing: theme -> Task type -> layout, then the servers folders
├── s03-draft-task-type.png         its preview
└── build_s03_draft_task_type.py    the builder (type counts and the servers tree read from disk)
```


The words the drawing reads
---------------------------

```yaml
key: 'A Task''s face says its type; the type picks its layout. task-type: draft opens the base''s draft
  layout in every theme, and the theme adds its own Spaces on top.'
pick:
- {title: the face, lines: ['task-type: draft']}
- {title: task_type(), lines: [reads that line]}
- {title: task_layouts(), lines: ['draft → workbench-task-draft/task_draft.py']}
- {title: the draft layout, key: true, lines: [Plan · Reading · Draft-Scratch · Evidence]}
- {title: theme on top, lines: [paper adds Comments]}
pick_labels: [read, look up, open, then]
themes:
- {theme: paper, types: 'draft (page-type: section under it)', layout: draft + Comments}
- {theme: labeling, types: 'data · raw · building · scanning · eval', layout: its own table (stays)}
- {theme: work, types: 'raw · data · eval · fit · evidence', layout: vanilla}
- {theme: any theme, types: draft, layout: draft}
servers_before: |
  servers/
  ├── haipipe-board/       only __pycache__
  ├── haipipe-page/        standalone_server.py · assets/ · tests/
  └── workbench/
      └── task-page/       the Page Task's views
steps:
- {title: ✅ haipipe-board deleted, lines: [it held only __pycache__]}
- {title: ✅ haipipe-page folded in, lines: [now workbench-task-draft/reader/, same css load order]}
- {title: ✅ task-page is workbench-task-draft, lines: [89 files rewritten, URLs unchanged]}
- {title: ✅ layout by task-type, lines: [frame.py rule + a test, 19 hosts restarted]}
- {title: ✅ 185 faces say draft, lines: ['task-type: draft above page-type: section', 'the page-type: rule removed']}
- {title: ✅ page is evidence, lines: ['task/10_evidence/haipipe-task-for-evidence']}
open:
- '❓ 58 Sections keep an old web copy in their own delivery/web/; the web Run now writes to the Board''s delivery/'
```


Decided
-------

s03-D01 · A theme's Tasks have types and each type has a layout; the base lays out `task-type: draft`
for every theme (`frame.task_layouts()`, `frame.task_type`; each type's folder `workbench-task-<type>/`), and a theme's own Spaces go on top
(JL 261014: "for the workbench, we will have the task type of draft")

s03-D02 · `servers/workbench/task-page/` is `servers/workbench/workbench-task-draft/`; `PAGE_TASK_SUBS`,
`PAGE_TASK_RUNS` and `page_task_spaces` are `DRAFT_TASK_SUBS`, `DRAFT_TASK_RUNS` and
`draft_task_spaces`; the `/_board/...` addresses stay (JL 261014: "yes, please go ahead and do that")

s03-D03 · `servers/haipipe-board` (only `__pycache__`) is deleted; `servers/haipipe-page` is folded
into `servers/workbench/workbench-task-draft/reader/` (the standalone server, the reader look, its 4 tests),
loaded in the host's old slot so the css order is unchanged (JL 261014: "I think we can delete these
two things")

s03-D04 · Every face that says `page-type: section` (185 in WellDoc, DrFirst, Physician and REACH) says
`task-type: draft` on the line above it; `page-type:` stays as the theme's subtype, and `frame.task_action`
reads only `task-type: draft`. New Sections get the line from `paper_ladder.py` and the section templates
(JL 261014: "Yes, clean them, go ahead and do all")

s03-D05 · `task-type: page` is `task-type: evidence`: `task/10_page/haipipe-task-for-page` is
`task/10_evidence/haipipe-task-for-evidence`; no face used the old name (JL 261014: "go ahead and do all")

s03-D06 · Labeling keeps its own five Task types (`labeling_theme.TYPES`): they mean something only inside a
labeling Block, and `frame.task_layouts()` finds the layouts the base gives every theme (JL 261014: "do all")

s03-D07 · The 39 old flat `runs/delivery-run/run_delivery_*.sh` tickets in FairGlucose's 13 Sections are
deleted; each Section's `runs/run-delivery-<lane>/` ticket is the one that runs (JL 261014: "clean them")


Open
----

1. 58 Sections (WellDoc 21, DrFirst 12, Physician 24, REACH 1) keep an old web copy in their own
   `delivery/web/`, from before the web Run wrote to the Board's `delivery/<version>/<section>/web/`.
   Each one has a fresh copy there (checked 261015), and nothing writes or reads the old one. The list:
   the scratchpad's `orphans_ok.txt`. Removing them was held for a person (all are tracked in git).

(write here, or mark the drawing in red)
