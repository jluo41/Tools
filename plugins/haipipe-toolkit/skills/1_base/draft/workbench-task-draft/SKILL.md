---
name: workbench-task-draft
description: "Opens and interprets a Draft Task's workbench page: the views 1 · Draft, 2 · Plan, 3 · Evidence and 4 · Display (only when the text calls one), the side pane, Delivery, and what each click writes. Use to read or fix a draft page. Trigger: draft task UI, draft workbench, stale draft page, Draft Lab, /workbench-task-draft."
metadata:
  version: "0.107.0"
  last_updated: "2026-11-27"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /workbench-task-draft · the draft Task's page

Rules come in layers, and the higher one wins:

```text
1  ../../project/hai-block/CONSTITUTION.md      every Block, Job and Task page (A01: no Around the Work band)
2  ../../workbench/hai-ui/CONSTITUTION.md       page words: no state words, no tallies, marks pop out
3  CONSTITUTION.md (this skill)                 the draft page's own articles
4  this file                                    what the page shows now, and what each click writes
5  ref/*.md                                     one part each; ref/classic/ is the old page
```

The page is drawn by `servers/workbench/workbench-task-draft/` for a Task whose face says `task-type: draft`. This
file says what that code shows today; a statement here that the code does not do is a bug in this file.


The page
--------

A bare Task link (`/_board/workbench?path=<task>` or `layout=focus`) opens the Report on **1 · Draft**.

```text
1 · Draft       ✍️ Draft Lab · 📋 Review Report (when a pass exists) · 📚 Examples · 📏 Writing Rubric · ⚖️ Decisions
2 · Plan        🎯 What this Section must do · Structure · 📚 Examples
3 · Evidence    the text with its evidence rows · ✅ Checked at the Board · 📚 Its bib
4 · Display     only when the text calls a Table or Figure: the step's result · Input · its Runs
under each      the view's own 🙋 Interactions fold
side pane •••   Studio · Interactions · Decisions · Things to Know · Checklist · Timeline · Skills · Files · Delivery
```

1. **Four views at most**: `focus_draft_steps.work_views`; Draft first, the others in their step order. A view with
   nothing in it is not shown (Display without a called display).
2. **No state words on the buttons**: a view's button is its number and name only.
3. **No left tabs**: each view is 📋 Review Content followed by its numbered sections (`focus_draft_steps.step_html`).
4. **Draft and Plan show no Process block**: the step's prompt, input and Runs are the Board's and the Job's work;
   Evidence shows what was checked at the Board instead.
5. **Plan shows no Scratch or Requirement**: they are filtered off the view (`focus_draft_steps.py`, the Plan filter).
6. **Under the content only the view's own 🙋 Interactions** (`work_frame.view_asks`); no shared band after it.
7. **Everything else is in the side pane**: one round launcher (`focus_shell.side_launcher`) opens its menu;
   Files is reached only there (`side_pane/files_tree/work_files.render`); there is no right rail.
8. **Delivery**: PDF, Word, Web and Built files (`delivery_export/focus_draft_delivery.section_delivery_views`).
9. **Old view names land on 1 · Draft**: `text`, `runs`, `status`, `mindmap`, `write`, `revise` (`focus_render.py`).

How the cards inside the views behave (Draft Lab's sentences and cards, comments, Plan's map, Evidence rows, a
display under the sentence that calls it) and what each click writes: `ref/draft-lab.md`.


Other routes
------------

The classic page still answers: `/_board/draft`, `?view=draft` (three Spaces with the Runs panel) and
`layout=frame` (Studio, 1 · Plan to 5 · Revise, Delivery). Nothing new is added to it; a link to it is followed,
never handed out. Its layout, routes and tabs: `ref/classic/`.

A short address for a Page is `<DOMAIN>/w/<board-slug>/<page-id>`; `<DOMAIN>` is the origin the reader uses, never
baked into a page. Follow the redirect and read one real value off the response before returning any link.


Who writes what
---------------

The workbench calls no model. A click writes one Markdown file through one POST, refused when the file changed on
disk since it was shown:

```text
POST                       action                                  writes
──────────────────────────────────────────────────────────────────────────────────────────────────────
/_board/draft-card         accept · reject · edit · undo a card     draft/records/<stem>-revise.md
/_board/draft-comment      add · reply · done · reopen · delete     draft/records/<stem>-comments.md
/_board/draft-rule         a ruling on a card                      draft/records/<stem>-revise-rules.md
/_board/draft-plan         edit Plan's map: a point, a paragraph    the newest draft's ## 1 · Structure
/_board/draft              scratch · revise · structure             the current plan, sections 2 and 3, headings
```

Writers of the rest (`_host/serve_post.py` routes the POSTs above):

```text
file                         written by                                         regenerate with
───────────────────────────────────────────────────────────────────────────────────────────────────
plan (draft-v*.md)           run-structure (SHAPE, SURVEY); evidence embed appends
evidence-items.md            SHAPE and SURVEY's item contract                    never (authored)
records/context              CONTEXT (hai-draft-logic, its context page)         hai-draft-logic
records/requirement          cli/requirement.py, or the author verbatim          cli/requirement.py <page>.md
records/discussion · log     any Run or the page chat; log is append-only        never (authored)
records/feedback             cli/feedback.py collect                             cli/feedback.py collect
<page>.md ## Content         page.py adopt, from the Draft                       page.py adopt
delivery/*                   the exporters (exporters/)                          rebuild the lane
```

`edit-preview`, `edit-bullet` and `append-bullet` are refused: sentences are edited in Draft Lab, Bullets and
structure through `run-structure`. A new Shape version (`approved: ⬜`, `supersedes:`) is `run-structure`'s job;
`approved:` is a person's act and a machine only transcribes it.

Two hard rules: never hand-edit a generated file (a view, a `delivery/` artifact): change the code or the Page source
and rebuild; never write, check or compare a content hash: a version is its number and date, staleness is file time.


The folder
----------

`<page>.md` is the product, what the Page asserts; `draft/` is the process, how it came to assert it.

```text
<task>/
├── <stem>.md                          the face; Delivery reads it
├── draft/
│   ├── <stem>-draft-v<G>.<S>[.<E>].md the one current plan: ## 1 · Structure · ## 2 · Scratch · ## 3 · Draft
│   ├── <stem>-evidence-items.md       Evidence Item contracts: Citations · Displays · Values
│   ├── records/                       context · requirement · revise · comments · revise-rules · feedback · log
│   └── previous/                      every superseded plan version
├── runs/<name>.md · results/<name>/   one ticket and one result folder per Run, the same name
├── delivery/                          web · latex · word (generated)
└── studio/                            the person's own drawings and notes
```

1. **Readers never parse the sections themselves**: `hai-draft/src/plan_layout.py::to_canonical` folds them into
   the grammar in `ref/plan-grammar.md`; every writer hands its plan to `from_canonical`.
2. **Versions** are `v<G>.<S>[.<E>]`: `G=0` never touches Content; a Shape change bumps `S` and resets `E`; an
   evidence fold bumps `E` and inherits its Shape's approval (`shape-base:`). At release,
   `hai-draft`'s release decisions decide.
3. **Evidence names**: the stored id keeps its form (`E13-DISPLAY-cohort-overview`); people read the short name
   `Edisplay13`, `Ecite25`, `Evalue01` (`hai-draft/src/item_table.py::short_name`).
4. **A review packet**: when a person asks to review or approve a plan, the structure Run answers with one linked
   packet and writes nothing (`ref/review-packet.md`).


The code
--------

```text
servers/workbench/workbench-task-draft/
├── page_shell/task_draft.py           the draft Task type on the frame
├── page_shell/focus_draft_steps.py    the views and their sections (work_views, step_html)
├── page_shell/focus_draft_report.py   the Review Report      · focus_draft_words.py   view names
├── page_shell/focus_draft_assets.py   page assets            · focus_draft.py         re-exports only
├── page_shell/draft_context.py        a view's scope for the shared frame
├── delivery_export/focus_draft_delivery.py   Delivery's views
├── revise_steps/ · evidence_steps/ · plan_outline/   Draft Lab, Evidence and Plan cards and their writers
├── run_views/                         Run names and cards (ref/runs.md)
└── exporters/                         md2tex.py · md2docx.py and their parts
servers/workbench/page/                the shared frame: block_index_page/focus_render.py (routes),
                                       block_index_page/focus_shell.py (side pane), job_task_views/work_frame.py
```

Validate a change on a real draft Task: every view, editing controls without saving, sign and accept controls
without submitting, the side pane's sections, Files previews and Delivery.


Files
-----

- `CONSTITUTION.md` · `constitution/` · the draft page's articles, each with its check
- `ref/draft-lab.md` · the cards inside the views and what each click writes
- `ref/runs.md` · Run names, opening and closing a Run, adding a Run family
- `ref/plan-grammar.md` · the canonical plan grammar every reader parses
- `ref/item-table.md` · Evidence Item identities, Run graph, derived status
- `ref/record-shape.md` · the records: ids, labels, writers, rules
- `ref/evidence-bundle.md` · the derived per-Bullet evidence join
- `ref/evidence/citations.md` · `values.md` · `displays.md` · `pagex.md` · per-kind authority
- `ref/content-preview.md` · candidate prose storage and the CONTENT handoff
- `ref/review-packet.md` · the review packet
- `ref/skill-record.md` · the ranked Page Skills store
- `ref/specimen-section-plan.md` · an approved Section plan, frozen
- `ref/run-space.md` · the classic All-runs view
- `ref/classic/` · the classic page: `layouts.md`, `space-mapping.md`, `delivery.md`, `folder.md`, `workbench-table.md`
