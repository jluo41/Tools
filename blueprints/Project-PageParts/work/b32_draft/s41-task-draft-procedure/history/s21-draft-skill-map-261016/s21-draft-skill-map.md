s21 · The 1_base/draft skills: which stay, which merge
======================================================

**Tags:** `base` · `skills`

**Stage:** explore

**Topic:** JL 261016: "Tools/plugins/haipipe-toolkit/skills/1_base/draft/haipipe-folder, do we still need this? and
haipipe-page and haipipe-sentence? I think we might need a new sNN to discuss about the 1_base/draft structure
problem". `1_base/draft/` has grown to 21 skills and folders: the door (`haipipe-draft`), a controller, eight Run
skills, a prose worker, three workbench skills, two contracts and an alias. The sketch JL drew the same day (Draft on
top, Evidence and Display below) needs only four: `haipipe-draft` writes, `haipipe-draft-review` judges,
`haipipe-evidence` backs, `haipipe-display` shows. This topic lists every piece in `1_base/draft/`, says which of the
four it folds into or where else it belongs, and decides the order of the moves. s02 merged the folders
(`1_base/page` + `1_base/writing` into `1_base/draft`, 261014); this topic is about the skills inside.

**Feeds:** s41-task-draft-procedure (D08, the Task's `draft/`, `evidence/`, `display/`); s02-draft-folder-merge.


Files
-----

```text
s21-draft-skill-map/
├── s21-draft-skill-map.md        this face: the inventory and the proposed moves
├── build_s21_draft_skill_map.py  the builder: reads 1_base/draft/ from disk
├── s21-draft-skill-map.excalidraw  the drawing: today, the moves, the end shape
└── s21-draft-skill-map.png       its preview
```


The inventory, today (261016)
-----------------------------

Counts are files outside the skill that name it (plugins and blueprints, drawings left out).

```text
piece in 1_base/draft/              what it is                                         named by   proposed
haipipe-draft/                      the door: Page Folder, Draft Markdown, page.py      (the base)  ✅ stays, takes in the steps
haipipe-page                        a symlink to haipipe-draft, the old name (261011)   156 files   🔶 keep until the sweep, then remove
haipipe-folder/                     the neutral Folder contract: Page Face + Task Face   28 files   🙋 move out of draft/: it is about
                                                                                                   every Folder, so haipipe-task or
                                                                                                   1_base/project, not draft
haipipe-sentence/                   the sentence contract: address, comment lanes,       22 files   🔶 fold into haipipe-draft
                                    evidence cards on a span of words                              (ref/sentence.md); the cards part
                                                                                                   is haipipe-evidence's anchors now
haipipe-draft-workflow/             the Page workflow controller (runs the steps)                   🔶 fold into haipipe-draft
workflow-runs/haipipe-draft-context      PREPARE: freeze the inputs                                 🔶 → haipipe-draft ref
workflow-runs/haipipe-draft-structure    SHAPE + SURVEY: the plan                                   🔶 → haipipe-draft ref
workflow-runs/haipipe-draft-scratch      a person's rough notes                                     🔶 → haipipe-draft ref
workflow-runs/haipipe-draft-writing      WRITE: the text in one pass                                🔶 → haipipe-draft ref
workflow-runs/haipipe-draft-revise       before/after change ledger                                 🔶 → haipipe-draft ref
workflow-runs/haipipe-draft-evidence     LAND + EMBED                                               🔶 → haipipe-evidence (s41-D08 steps)
workflow-runs/haipipe-draft-check        the Page check gate                                        🔶 → haipipe-draft-review
workflow-runs/haipipe-draft-delivery     builds .docx, .tex, .pdf                                   🙋 → haipipe-draft ref, or haipipe-delivery
writing/haipipe-writing             draft, revise, evaluate prose; plain-rules, anti_slop  9 skills 🔶 split: drafting → haipipe-draft,
                                                                                                   judging → haipipe-draft-review (new)
writing/1_style, 2_evaluate         vendored writing-dna, humanizer, academic-humanizer             🔶 → under haipipe-draft-review
workbench/                          /wb and the workbench contract, the folder roster              🙋 not draft-only: every theme
                                                                                                   opens through it; move beside the
                                                                                                   servers or 1_base/project
workbench-page/                     the Page screen: Draft, Evidence, Delivery Spaces              ✅ stays: it is the draft's screen
workbench-studio/                   the Studio tab: drawing above, chat below                      🙋 belongs with haipipe-studio
pages-example/                      a sample Page Folder (haipipe-page-guide)                      🔶 → haipipe-draft/examples/
```


The end shape, proposed
-----------------------

```text
1_base/draft/      haipipe-draft (writes; the steps as ref/) · haipipe-draft-review (judges) · workbench-page
1_base/evidence/   haipipe-evidence (backs)
1_base/display/    haipipe-display (shows)
elsewhere          haipipe-folder, workbench, workbench-studio: to their real owners
gone               haipipe-page alias, haipipe-sentence, haipipe-draft-workflow, 8 Run skills, haipipe-writing
```

The writer and the judge stay two skills on purpose: whoever wrote a text never judges it (the check runs in a fresh
context by another agent), and a separate `haipipe-draft-review` keeps that line visible.


Decided
-------

s21-D01 · The Excalidraw skills (studio, report, section, read, revise, workflow, job, task, slide, ideation) move from
    `1_base/display/` to `1_base/excalidraw/`; every path in the seven SPACEs is swept and the drawings that recorded
    the old path are rebuilt (JL 261016: "we also need a 1_base/excalidraw to put the excalidraw-xxx skills into here").
s21-D02 · No link inside Tools: the 11 plugin agent links (9 broken since 261014) and the `haipipe-page` alias are
    removed; `install.sh` installs agents from the skill folders (JL 261016: "do not use the symlink within the Tools").
s21-D03 · `1_base/question/` folds into haipipe-report: the Questions contract is its `## Questions`, asking and review
    are `ref/asking.md` and `ref/review.md`, `ask-questions` moves to `0_utils/`; Block Questions on disk are unchanged
    (JL 261016: "no need for the question anymore", option "Fold into haipipe-report").
s21-D04 · `haipipe-writing` and `haipipe-draft-check` become `haipipe-draft-review`, the judge (rules, anti_slop, rubric,
    humanizers, the Page check gate); drafting moves into `haipipe-draft/ref/writing/`; whoever writes never reviews
    (JL 261016: "should we have the haipipe-draft-review? ... no more haipipe-writing"). Done 261016; servers restarted.
s21-D05 · The shared screen manuals leave `draft/`: `workbench` (the /wb door, the folder roster) and `workbench-page`
    move to a `1_base/workbench/` family; `workbench-studio` folds into haipipe-studio (it owns the Studio); the nine
    `haipipe-draft-*` agents move from `workbench/agents/` to `haipipe-draft/agents/`. The screens' code stays in
    `servers/`; theme screen manuals stay with their themes (JL 261016: "do we want so many workbench? I thought the
    workbench is in the server"; "please go ahead and add it").
s21-D06 · `haipipe-sentence` and the drafting half of `haipipe-draft` (`ref/writing/`) fold into
    `haipipe-draft-writing`, which moves up beside `haipipe-draft-review`: the writer and the judge, never the same
    agent; evidence on a span of words points to haipipe-evidence's anchors (JL 261016: "haipipe-sentence ... maybe we
    can have a haipipe-draft-writing").
s21-D07 · `haipipe-folder` (293 lines) is retired: its two-faces template (nine required sections no owner had) is
    dropped, and what is used fits one page, `haipipe-draft/ref/folder.md`: the Task folder (face, draft/, evidence/,
    display/, runs/), one writer each, and the owner header lines `src/folder_contract.py` reads. The checker keeps its
    header checks and loses the section check (JL 261016: "it is too large, it is only for the haipipe-draft-folder,
    please rethink about it").


Open
----

1. JL: the Run skills (context, structure, scratch, writing, revise, evidence, delivery) and haipipe-draft-workflow:
   fold into haipipe-draft as ref/ pages, or keep any apart? haipipe-sentence: fold in too?
2. Done 261016: haipipe-folder retired (s21-D07).
3. JL: haipipe-draft-delivery: a ref of haipipe-draft, or part of haipipe-delivery (the Block's delivery/)?
4. JL: workbench and workbench-studio: where do they move, and do they move at all in this pass?
5. Done 261016: haipipe-draft-review, the excalidraw folder, the Questions fold. Next: the Run skills, then the
   156 haipipe-page mentions, each checked by opening a real Page in the workbench.

(write here, or mark the drawing in red)
