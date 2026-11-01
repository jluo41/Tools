s01 · Work ladder
=================

**Tags:** `Skill`

**Stage:** explore

**For:** a deck, and `plugins/haipipe-toolkit/skills/2_theme/work/haipipe-work/SKILL.md` rewritten to today's work ladder: what a work Block, Job, Task, Run and Studio topic each hold, which of them get a page, and where each kind of request goes, for the people who write the toolkit skills and the agents that route work by them

**Delivery type:** skill

**Covers:** the five rungs of a Project's `work/` world (Block, Job, Task, Run, Studio topic), each with its folder,
its face and what it holds; which rungs get a page and how the others open instead; the route table, each kind of
request to the skill that owns it; the door's boundary.

**Excluded:** the shape every theme shares and its audit (haipipe-project `ref/ladder.md`); each level's own face
contract (haipipe-block, haipipe-job, haipipe-task, haipipe-run, haipipe-studio); the work pages on screen (s02:
workbench-work; s04 and s51 to s59: the pages); which `1_base/task` skills move into `2_theme/work` (set aside on
261031, s02-D02; the routes name where each skill lives today).

**Topic:** haipipe-work's SKILL.md, rewritten to today's work ladder. One rung per level, each with its folder, what
it holds and whether it gets a page: a work Block, Job and Task each get a page (Report checks, Work does, Studio
thinks); a Run gets none and is a row on its Task's Work, opened in the pop-out; a Studio topic gets none and is a
card where it sits, opened by its tags. Under the rungs, where each kind of request goes, each to the skill that owns
it. Today's SKILL.md (0.1.2, 261026) still gives a work Block Questions, `reports/` and `studio/`, and a Run the old
`runs/rNN_<noun>_<qualifier>.sh` beside `results/` (JL 261031: "this studio's content need to be totally rewrite").

**Feeds:** none: a work Block keeps no Questions (JL 261031, s51-D04).


Files
-----

```text
s01-work-ladder/
├── s01-work-ladder.md            this face
├── build_s01_work_ladder.py      the builder: haipipe-studio's five parts; its Design is the ladder, rung by
│                                 rung, and each rung's owner; it reads delivery/render.yaml and j01's Run cards
├── s01-work-ladder.excalidraw    the drawing (five_parts rewrites it: change the builder, never the canvas)
├── s01-work-ladder.png           its card
├── s01-work-ladder.mindmap.md    its mind map, built from this face
├── s01-work-ladder.ideas.md      its open ideas, one a slide: the question, the options, the leaning
├── s01-work-ladder.slides.json   the deck's record, scratch cards with no pictures yet; .slides.html and .pptx
├── delivery/                     deck/ and render.yaml: haipipe-work/SKILL.md, made by j01 t01's Run
└── result/                       this topic's own working output and its history
    ├── first-drawing.excalidraw  the first drawing, the frame "work ladder · Q01" (261007), kept whole
    ├── first-drawing-builder/    its builder, kept whole, retired 261030
    ├── five-part-drawing-261030/ the generic five-part redraw (studio_update.py) it replaced, with its card
    ├── old-face-261031.md        this face before the 261031 rewrite
    ├── old-mindmap-261031/       the mind map written 261026 from the first drawing
    ├── old-slides-261031/        the three idea pictures (261029), their ideas file and deck
    └── theme-alignment-proposal.md   b17 beside b16, b11 and b12 (261031), its form ../runs/r01_collect_theme_alignment/
```

Rebuild: `python build_s01_work_ladder.py` (the drawing and its card); the mind map: haipipe-mindmap
`mindmap.py refresh s01-work-ladder.mindmap.md`; the deck: haipipe-studio `topic_slides.py .`.


Decided
-------

s01-D01 · Its delivery is one skill piece: haipipe-work SKILL.md's "The work ladder" section and the work scaffold, made by j01_work_ladder_contract; the topic sits beside its Job, out of `studio/` (JL 261031, agreed the b17 plan). Replaced by s01-D03 (261031): the delivery is the whole SKILL.md; whether a scaffold stays is Open 1; the place is s01-D07.

s01-D02 · This topic and its drawing are rewritten: what they said no longer holds (JL 261031: "this studio's content
need to be totally rewrite, I think the draw need to be updated as well?").

s01-D03 · Its delivery is haipipe-work, updated: `skills/2_theme/work/haipipe-work/SKILL.md` says today's work ladder
and where each kind of request goes (JL 261031, on s01 and s02: "I have no idea, this should not be the things we
want to focus"; pointing at `skills/2_theme/work`: "you should update this, right?"). It widens s01-D01's one section
to the whole SKILL.md.

s01-D04 · A Run and a Studio topic get no page: a Run is a row on its Task's Work, opened in the pop-out; a topic is a
card where it sits, opened by its tags Slide · Draw · Mind map · Work · Delivery · Interaction (JL 261031, on this
topic's open sticky "does a Run get its own page?": "run will not get its page, and also the studio will not has its
own page as well").

s01-D05 · A work Block, Job and Task each get a page: Report (check), Work (do) and Studio (think), designed one sNN
per level and section at j03's three Tasks, s51 to s59 (JL 261031, s04-D04).

s01-D06 · A work Block keeps no Questions: Findings, Answers and Questions go, so s01 feeds none (JL 261031, s51-D04:
"we will not have the questions").

s01-D07 · Topics sit beside their Jobs and Tasks: never in a `studio/` folder, at most 9 at a Block, 5 at a Job, 3 at
a Task (JL 261030, b35 s01-D12: "we just have sNN, along side with jNN, to make it visible directly"; "we might have
many sNN, but we need to control the numbers").

s01-D08 · s01 is in the Studio group Skill: beside s02 (JL 261031, theme alignment r01 Q1: "I agree").


Open
----

1. Drop the work scaffold from s01's delivery? The base skills already make every rung (`new_board.py`, `new_job.py`, `soft_run.py`, `new_topic.py`, `collect.py`), so j01's `t02_scaffold` waits in `_old/` and the SKILL.md routes to them; s01-D01 named a scaffold, so this is JL's call. Leaning: drop it.
2. Do older Blocks' Questions still go to haipipe-report? Most work Blocks in use keep a `## Questions` register (24 of 43 in the SPACE checked on 261031, and 17 keep `reports/`), and a Block moves only when JL asks; until then the door could keep one route to haipipe-report, or drop it. Leaning: keep one route, marked "older Blocks, until moved".
3. How much of each rung goes in the SKILL.md? One line per rung naming its owner's contract, each rung's whole folder tree, or a `ref/work-ladder.md` with the trees. Leaning: one line per rung, so each rule keeps one copy and nothing drifts.

(write here, or mark the drawing in red)


History
-------

- 261007: first drawn as the frame "work ladder · Q01", one row per level (Block, Job, Task, Run) and one column per Space (Description | Idea Studio · Audience Report | Work Details | Runs · Delivery), today's Task workbench views moved into it and nine open points in red; below it the Board, Job and Task rows from b10's shared definitions. Kept whole: `result/first-drawing.excalidraw` and `result/first-drawing-builder/build_s01_work_ladder.py`.
- Q01 ("How does work climb the ladder?") was proposed 261007 and stayed open; its report `../reports/q01_work_ladder/` goes with the Questions (s01-D06).
- 261026: the mind map written from that drawing, frame by frame: `result/old-mindmap-261031/`.
- 261029: three idea pictures and their deck ("Every rung, the same five doors?", "Four rungs, each holds less", "The answer sits on its Job?"): `result/old-slides-261031/`. Their asks are settled: no page for a Run (s01-D04), a Job keeps `src/` and `sbatch/` for the code its Tasks share (haipipe-project `ref/ladder.md`), no answers to place (s01-D06).
- 261030: redrawn in five parts by `studio_update.py`, the first drawing as its Design: `result/five-part-drawing-261030/`.
- 261031: rewritten (s01-D02); the face before it is `result/old-face-261031.md`. The b17 theme alignment sits in `result/theme-alignment-proposal.md`, since its form `../runs/r01_collect_theme_alignment/` was addressed to s01.
