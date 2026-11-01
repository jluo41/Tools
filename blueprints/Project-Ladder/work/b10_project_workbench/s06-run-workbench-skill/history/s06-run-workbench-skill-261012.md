s06 · Run: its workbench and its skill
======================================

Was s05-runs. Renamed on 261011 (JL: "call it run-workbench-skill ... make the run to be a good
definition and explanation, about what they are doing"), then moved to s06 the same day when JL set
the order (JL 261011: "s02 studio, s03 delivery, and s04 related, and s05 report, and s06 run"): s02
to s04 are what the Block alone holds (Studio, Delivery, Related), s05 and s06 the Spaces row's Report
and Runs, which every level keeps its own. Its ids moved with it (s05-D01..D05 became s06-D01..D05).

**Stage:** shaping

**Tags:** `Structure` · `Run and Skill`

**Topic:** the Run seen from both sides: what a Run is and what it does, its workbench (the Runs panel
beside every Space, the Runs Space on every level) and its skill (`/haipipe-run`). It started from
JL 261007 ("how do we manage the runs here ... the soft run, the hard run, how the run looks like in
the folder and workbench"); the earlier decisions are s01-D14 and s01-D15, and the change that put them
in the skill is `../s01-overall-tree-structure/run-skill-draft.md`.

**Feeds:** `reports/q01_bjtr_boundary/` (what a Run is, and where it may sit), `q07_workbench_mapping/`
(the Runs panel, the Runs Space, the pop-out).


What a Run is
-------------

A Run is one piece of work, asked for once. It has four parts:

1. **Target**: what it works on (one topic, one report, one model fit).
2. **Ticket**: the ask, written down: who does what, with which inputs.
3. **Close rule**: how we know it is done, or honestly not done.
4. **Output**: what stays after it: its own `result/`, or the thing it changed.

It is one folder, `runs/<run>/`, in the `runs/` of its level (Block, Job or Task). Each round of work
on the same target is a **pass**, `passes/pNN-<MMDD>/`. A click, a tool call, a retry or a comment is
not a new Run: it is a step inside a Run, or a new pass of it.

What it leaves behind decides its kind. A **hard** Run makes new evidence (a number, a table, a
figure) in its own `result/`, and only a work Task holds one. A **soft** Run changes something its
level keeps (`draft/`, `studio/`, `reports/`, `delivery/`), at any level, and counts as work, not
evidence.


Files
-----

```text
s06-run-workbench-skill/
├── s06-run-workbench-skill.md               this face
├── build_s06_run_workbench_skill.py         the builder; marks are kept on rebuild
├── s06-run-workbench-skill.excalidraw       the story: four frames in one row, joined by arrows; In Tools below
├── s06-run-workbench-skill.png              its preview
├── .s06-run-workbench-skill.seed.json       generated snapshot for preserving marks
└── history/                                 the 261010 builder, drawing, preview and face (five frames)
skill: Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-run/
```

Rebuild: `python build_s06_run_workbench_skill.py` (or `../_build/make.sh`).


In Tools
--------

Where its skill and code sit, under `Tools/plugins/haipipe-toolkit/`. The drawing's "In Tools" frame
reads the same off the disk on every build: the skill's folder as it is, its version, and each
function looked up in its file (JL 261011: "show what are the skills related folders in the Tools").

```text
skills/1_base/project/
├── haipipe-studio/     s02 Studio
├── haipipe-delivery/   s03 Delivery
├── haipipe-related/    s04 Related
├── haipipe-report/     s05 Report
└── haipipe-run/        s06 Run        ◀ this topic
servers/workbench/frame.py         runs_of
servers/workbench/runs_panel.py    run_types · panel_html · panel_markup
```


What the drawing holds
----------------------

```text
① What a Run is          a Run and its four parts (target · ticket · close rule · output), with
                         run-report-q05 of this Block as the example; where it sits; what is and is
                         not a Run; the six tests that earn one
② Hard or soft           what it leaves: a hard Run (r01_rate_tir_hypo, Proj11-CGM-Corpus) beside a
                         soft one (run-draw-s21, this Block), each with its folder; the rule
③ Every round is a pass  run type -> ticket and card -> pass -> pass -> closed (run-draw-s21's
                         passes, read from its run.yaml); a new pass or a new Run; what a pass holds
④ Workbench and skill    this Block's Runs Space as frame.py draws it; the Runs panel; /haipipe-run
Below                    still open (red); hard and soft row by row, and the folders; In Tools
```

Read from disk on every build: this Block's Runs (`runs/*/run.yaml`, each ticket's `close:` line), its
Runs Space through `servers/workbench/frame.py`, and haipipe-run's version.


Finding (read 261011)
---------------------

1. Every Run in this Block names its close rule (read 261012: 12 Runs). Five still said `close: <what settles
   it>`, the line `soft_run.py new` leaves when it is given none (`run-draw-s01`, `s02`, `s04`, `s08`,
   `s21`); they now say what `run-draw-s05` and `s06` say. `new_topic.py session` had made four of
   them; it now writes the close rule itself (s06-D06).
2. The Runs Space shows 4 columns (Run · kind · type · status) and no pop-out; s06-D01 proposed seven
   columns and a pop-out.
3. The hard example still sits in the older layout (`runs/r01_rate_tir_hypo.sh` beside
   `results/r01_rate_tir_hypo/`).


Settled (in haipipe-run 0.33.1)
-------------------------------

1. A Run is hard or soft by where its output lands. Hard `rNN_<slug>`: its own `result/`, evidence,
   a work Task only. Soft `run-<type>-<target>`: writes into its scope's `draft/ studio/ reports/
   delivery/`, not evidence, at a Block, a Job or a Task.
2. One Run is one folder in `runs/`: its ticket, `run.yaml` (the card), and `passes/pNN-<MMDD>/`;
   a hard Run adds `config.yaml` and `result/`. Folder name = ticket stem = `run.yaml` `run:`.
3. A pass is one more execution (hard) or one more round on the same target (soft); new inputs or a
   new target make a new Run.
4. Heavy output goes to `_WorkSpace/ProjectResult/<...>/<run>/`; `result/heavy.yaml` points to it.


Decided
-------

s06-D04 · Renamed s06-run-workbench-skill (was s05-runs): the Run seen from both sides, its workbench
    and its skill, in JL's order: s02 Studio, s03 Delivery, s04 Related (held by the Block alone), s05
    Report, s06 Run (the Spaces row, every level its own) (JL 261011).
s06-D05 · The drawing is one story in four frames joined by arrows, and it defines the Run first, in
    plain words, before hard and soft, passes and the screen (JL 261011: "make the run to be a good
    definition and explanation, about what they are doing"). The 261010 five frames are in history/.
s06-D06 · A topic's soft Run starts with its close rule (261011; settles the old Open 7): `new_topic.py
    session` writes "a person moves the topic's Stage to agreed, or names what is still wrong in red
    on the drawing" into `run-draw-<sNN>`'s ticket (haipipe-studio 0.9.2). `soft_run.py new` still
    takes any rule with `--close`; it does not refuse a ticket without one, since other Run types
    have no default. b10's five placeholders were filled with the same words, naming JL.


Proposed
--------

s06-D01 · Proposed (261007): on screen, a Runs panel sits beside every Space at every level: that
    Space's run types as buttons (they copy a prompt and start nothing), then the recent Runs of that
    Space. Each level tab also has a Runs Space: one plain list of its Runs, read from each `run.yaml`
    (run · kind · type · target · status · passes · last), filtered by the third row (All · hard ·
    soft · <type>). A row opens the Run pop-out: the card, its passes, a result preview (hard:
    metrics and the first figure; soft: before/after and the run table).
s06-D02 · Proposed (261007): a wet Run is a hard Run a person carries out: an `rNN_<slug>.md`
    protocol ticket, a `result/` holding the data collected and an observation log, and a
    `runtime.yaml` the person signs. It cannot repeat exactly, so a replication is a new Run.
    Needs haipipe-run to accept a protocol ticket and a signed receipt (open 1).
s06-D03 · Proposed (261007): an agent session that works on a studio topic is a pass of that topic's
    soft Run, `run-draw-<sNN>` (s02-D27): the ask, the summary, what changed. So a session
    needs no folder of its own, and it lists with every other Run.


Open
----

1. Wet Runs: add the protocol ticket and the person-signed receipt to haipipe-run?
2. Block and Job Runs are soft only: where does a Job's batch launch (`run-launch-<group>`) go?
3. A hard Run's heavy output: show it on screen, or only its `heavy.yaml` pointer?
4. The Runs Space: this level's Runs only, or rolled up from the levels below?
5. A soft pass: when does it close, and who writes its `touched.yaml`?
6. The older layout: when does haipipe-project `update` move each Project's Runs?
7. The Runs Space: build s06-D01's seven columns and the pop-out?

(write here, or mark the drawing in red)
