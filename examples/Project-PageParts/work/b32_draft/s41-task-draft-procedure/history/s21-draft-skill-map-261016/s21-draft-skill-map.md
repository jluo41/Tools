s21 · The 1_base/draft skills: which stay, which merge
======================================================

**Tags:** `base` · `skills`

**Stage:** explore

**Topic:** JL 261016: "Tools/plugins/haipipe-toolkit/skills/1_base/draft/hai-folder, do we still need this? and
hai-page and hai-sentence? I think we might need a new sNN to discuss about the 1_base/draft structure
problem". `1_base/draft/` has grown to 21 skills and folders: the door (`hai-draft`), a controller, eight Run
skills, a prose worker, three workbench skills, two contracts and an alias. The sketch JL drew the same day (Draft on
top, Evidence and Display below) needs only four: `hai-draft` writes, `hai-draft-review` judges,
`hai-evidence` backs, `hai-display` shows. This topic lists every piece in `1_base/draft/`, says which of the
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
hai-draft/                      the door: Page Folder, Draft Markdown, page.py      (the base)  ✅ stays, takes in the steps
hai-page                        a symlink to hai-draft, the old name (261011)   156 files   🔶 keep until the sweep, then remove
hai-folder/                     the neutral Folder contract: Page Face + Task Face   28 files   🙋 move out of draft/: it is about
                                                                                                   every Folder, so hai-task or
                                                                                                   1_base/project, not draft
hai-sentence/                   the sentence contract: address, comment lanes,       22 files   🔶 fold into hai-draft
                                    evidence cards on a span of words                              (ref/sentence.md); the cards part
                                                                                                   is hai-evidence's anchors now
hai-draft-workflow/             the Page workflow controller (runs the steps)                   🔶 fold into hai-draft
workflow-runs/hai-draft-context      PREPARE: freeze the inputs                                 🔶 → hai-draft ref
workflow-runs/hai-draft-structure    SHAPE + SURVEY: the plan                                   🔶 → hai-draft ref
workflow-runs/hai-draft-scratch      a person's rough notes                                     🔶 → hai-draft ref
workflow-runs/hai-draft-writing      WRITE: the text in one pass                                🔶 → hai-draft ref
workflow-runs/hai-draft-revise       before/after change ledger                                 🔶 → hai-draft ref
workflow-runs/hai-draft-evidence     LAND + EMBED                                               🔶 → hai-evidence (s41-D08 steps)
workflow-runs/hai-draft-check        the Page check gate                                        🔶 → hai-draft-review
workflow-runs/hai-draft-delivery     builds .docx, .tex, .pdf                                   🙋 → hai-draft ref, or hai-delivery
writing/hai-writing             draft, revise, evaluate prose; plain-rules, anti_slop  9 skills 🔶 split: drafting → hai-draft,
                                                                                                   judging → hai-draft-review (new)
writing/1_style, 2_evaluate         vendored writing-dna, humanizer, academic-humanizer             🔶 → under hai-draft-review
workbench/                          /wb and the workbench contract, the folder roster              🙋 not draft-only: every theme
                                                                                                   opens through it; move beside the
                                                                                                   servers or 1_base/project
workbench-page/                     the Page screen: Draft, Evidence, Delivery Spaces              ✅ stays: it is the draft's screen
workbench-studio/                   the Studio tab: drawing above, chat below                      🙋 belongs with hai-studio
pages-example/                      a sample Page Folder (hai-page-guide)                      🔶 → hai-draft/examples/
```


The end shape, proposed
-----------------------

```text
1_base/draft/      hai-draft (writes; the steps as ref/) · hai-draft-review (judges) · workbench-page
1_base/evidence/   hai-evidence (backs)
1_base/display/    hai-display (shows)
elsewhere          hai-folder, workbench, workbench-studio: to their real owners
gone               hai-page alias, hai-sentence, hai-draft-workflow, 8 Run skills, hai-writing
```

The writer and the judge stay two skills on purpose: whoever wrote a text never judges it (the check runs in a fresh
context by another agent), and a separate `hai-draft-review` keeps that line visible.


Decided
-------

s21-D01 · The Excalidraw skills (studio, report, section, read, revise, workflow, job, task, slide, ideation) move from
    `1_base/display/` to `1_base/draw/`; every path in the seven SPACEs is swept and the drawings that recorded
    the old path are rebuilt (JL 261016: "we also need a 1_base/draw to put the excalidraw-xxx skills into here").
s21-D02 · No link inside Tools: the 11 plugin agent links (9 broken since 261014) and the `hai-page` alias are
    removed; `install.sh` installs agents from the skill folders (JL 261016: "do not use the symlink within the Tools").
s21-D03 · `1_base/question/` folds into hai-report: the Questions contract is its `## Questions`, asking and review
    are `ref/asking.md` and `ref/review.md`, `ask-questions` moves to `0_utils/`; Block Questions on disk are unchanged
    (JL 261016: "no need for the question anymore", option "Fold into hai-report").
s21-D04 · `hai-writing` and `hai-draft-check` become `hai-draft-review`, the judge (rules, anti_slop, rubric,
    humanizers, the Page check gate); drafting moves into `hai-draft/ref/writing/`; whoever writes never reviews
    (JL 261016: "should we have the hai-draft-review? ... no more hai-writing"). Done 261016; servers restarted.
s21-D05 · The shared screen manuals leave `draft/`: `workbench` (the /wb door, the folder roster) and `workbench-page`
    move to a `1_base/workbench/` family; `workbench-studio` folds into hai-studio (it owns the Studio); the nine
    `hai-draft-*` agents move from `workbench/agents/` to `hai-draft/agents/`. The screens' code stays in
    `servers/`; theme screen manuals stay with their themes (JL 261016: "do we want so many workbench? I thought the
    workbench is in the server"; "please go ahead and add it").
s21-D06 · `hai-sentence` and the drafting half of `hai-draft` (`ref/writing/`) fold into
    `hai-draft-writing`, which moves up beside `hai-draft-review`: the writer and the judge, never the same
    agent; evidence on a span of words points to hai-evidence's anchors (JL 261016: "hai-sentence ... maybe we
    can have a hai-draft-writing").
s21-D07 · `hai-folder` (293 lines) is retired: its two-faces template (nine required sections no owner had) is
    dropped, and what is used fits one page, `hai-draft/ref/folder.md`: the Task folder (face, draft/, evidence/,
    display/, runs/), one writer each, and the owner header lines `src/folder_contract.py` reads. The checker keeps its
    header checks and loses the section check (JL 261016: "it is too large, it is only for the hai-draft-folder,
    please rethink about it").


Open
----

1. JL: the Run skills (context, structure, scratch, writing, revise, evidence, delivery) and hai-draft-workflow:
   fold into hai-draft as ref/ pages, or keep any apart? hai-sentence: fold in too?
2. Done 261016: hai-folder retired (s21-D07).
3. JL: hai-draft-delivery: a ref of hai-draft, or part of hai-delivery (the Block's delivery/)?
4. JL: workbench and workbench-studio: where do they move, and do they move at all in this pass?
5. Done 261016: hai-draft-review, the excalidraw folder, the Questions fold. Next: the Run skills, then the
   156 hai-page mentions, each checked by opening a real Page in the workbench.

(write here, or mark the drawing in red)
