# A UI preview topic · a page looked at before and while the code draws it

A Studio topic type. Its face says `**Delivery type:** ui`; it previews a workbench page. The worked
example is b17_theme_work's `s11-work-job-preview/`. The rule behind it is hai-ui A08.

## The folder

```text
sNN-<slug>/
├── sNN-<slug>.md        the face: For, Covers, Topic, Decided, Open, Files; **Delivery type:** ui
├── sNN-<slug>.html      the topic's page: the list of its views, one <button data-src> each
└── delivery/ui/         the quick views, one html each
```

Studio reads the page's buttons (`servers/workbench/studio/tabs/studio_tabs.py` `page_items`) and shows
each view as a left tab; the page's own button row is not shown.

## Kinds

A UI preview names its kind on its face, under the Delivery type: `**UI preview:** Job · work`. Each kind
previews one kind of page over its own example Block; they are different topics, never one merged preview.

**Job UI Previews, the s1N band**: one topic per theme, each a Job inside its Block (its Main, its Tasks) over
that theme's example Block. They differ by theme, so each is its own topic; a new theme takes the next s1N.

| sNN | Job UI Preview | Example Block |
|---|---|---|
| s11 | work | `work/b01_example_work` (`s11-work-job-preview`) |
| s12 | blueprint | `blueprint/b17_theme_work` (`s12-blueprint-job-preview`) |
| s13 | cowork | `cowork/b01_example_cowork` (`s13-cowork-job-preview`) |
| s14 | discovery | `discovery/b01_example_discovery` (`s14-discovery-job-preview`) |
| s15 | knowledge | `knowledge/b18_a2ui_learning` (`s15-knowledge-job-preview`) |

Insight has three kinds of Block, so its Job UI Previews sit in its own theme Block, b11_theme_insight:

| sNN | Job UI Preview | Example Block |
|---|---|---|
| s11 | insight | `insight/Insight-Example` (`s11-insight-job-preview`) |
| s12 | insight-questionbook | `insight/InsightQuestionBook-Example` (`s12-questionbook-job-preview`) |
| s13 | insight-dataprep | `insight/InsightDataPrep-Example` (`s13-dataprep-job-preview`) |

Design has two kinds of Block, so its Job UI Previews sit in its own theme Block, b12_theme_design:

| sNN | Job UI Preview | Example Block |
|---|---|---|
| s11 | design | `design/Design-Example` (`s11-design-job-preview`) |
| s12 | design-methodbook | `design/DesignMethodBook-Example` (`s12-methodbook-job-preview`) |

**Other kinds**: a Block's own Guide is `s99` (`**UI preview:** Guide`, b17's `s99-guide-view`). A new kind
is a new row here and a new topic. The Block whose pages it designs names its example Blocks on its face's
`examples:` line, so the Files pane shows them.

## Page and Effect

Studio's top buttons for the topic are Page · Effect · Draw · Delivery. Page and Effect each list their views as left tabs, even when there is one, so another view is one more tab.

1. **Page, the live views**: `data-src="/_board/workbench?path=<url-encoded example Block path>&amp;layout=focus[&amp;section=…]"`,
   the page the server renders over the theme's example Block, so it changes with the code.
   Origin-relative, never a host.
   A live view names the part of the page it is about with `&amp;mark=<part>[,<part>]`, a part a class name
   (`jobs-rows`) or a data attribute (`jsub=main` for `[data-jsub="main"]`): the page outlines the visible
   ones in red and scrolls to them (`focus-assets/focus.js`). Views of one page share one address and differ
   only in their mark: s11's Page tabs, in the order the page reads, all open the example Block's Jobs with j11
   picked: job-rows (`jobs-rows,job-ttopics,job-subs`), job-overview (`view=overview`), job-tasks
   (`view=standing`), job-findings (`view=findings`). A tab is named `<level>-<part>`; a Task's are `task-…`.
2. **Effect, the quick views**: an html in `delivery/ui/`, for what the code cannot draw yet (an effect,
   a proposal). Light and dark by `prefers-color-scheme`.
3. **At least one live view**: a design is looked at on the example Block's real page, not on a drawing
   of it. A topic whose design is not in the code yet holds only quick views, and owes its live view.

## When a quick view fades, and when it goes

Once a quick view's design is in the code, its button gets `class="old"`: Effect shows it faded, after
the others, and a live view under Page shows the design instead. Once the design is settled and nobody
compares against it any more, the faded view is deleted: its file and its button go, and the face's
decisions name it "(removed <yymmdd>)". Effect keeps only what is still being looked at (s11 keeps Task
states). A quick view's name says what it shows (Task states), never "Effects" or a version label.

## The example Block it renders

Each theme keeps one example Block, made only by `new_board.py`, `new_job.py` and `soft_run.py`, holding
every Job and Task state and no real work (`hai-block` ref/board-contract.md § Example Blocks). Work:
`examples/Project-Ladder/work/b01_example_work`; paper: `examples/Project-Ladder/paper/Paper-Example`.

## s99, the Block Guide

`s99` is a Block's own Guide (how to use this Block's page), one per Block, always last, made by hand with
`new_topic.py --nn 99`; it is a UI preview topic. It differs from s81-s89, which design the theme's Guide
shared by every Block. Example: b17_theme_work's `s99-guide-view/`, one quick view over b01_example_work
until the Guide section is in the code.

## The check

```bash
python3 plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/ui_preview_check.py [examples/<sub>]
```

From the Tools-SPACE root. It finds every UI preview topic under `examples/` and reports one with no
page, one with no live view, a view that names a host, and a quick view whose file is not there; exit 1 on
any. Whether a quick view's design is in the code cannot be read from files, so `class="old"` is not checked.
