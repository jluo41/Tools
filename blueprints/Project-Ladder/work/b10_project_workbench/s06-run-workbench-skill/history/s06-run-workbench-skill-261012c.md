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

The drawing's frames, as data (`topic_map.py` draws them; the builder fills the words in ‹ › from the disk):

```yaml
frames:
- title: 🧭 Background, the Run for a newcomer
  intro: the words this topic uses, where a Run sits, and why the topic exists
  cols: 2
  tree:
  - 📖 The words:
    - 🏃 Run, one piece of work asked for once; one folder, runs/<run>/
    - 🎫 ticket, the ask written down (who does what, with which inputs)
    - 🏁 close rule, how we know it is done, or honestly not done
    - 🔁 pass, one more round on the same target (passes/pNN-<MMDD>/)
    - 🪨 hard Run makes new evidence in its own result/; 🪶 soft Run changes what its level keeps
    - 🗂️ Runs Space, the list of a level's Runs; 🔘 Runs panel, the buttons beside every Space
    - 🧰 skill /haipipe-run, owner of the card (run.yaml) and the passes
  - 📍 Where it sits:
    - Block > Job > Task > Run > pass
    - a Run lives in the runs/ of its level
    - a Task holds hard and soft Runs; a Block and a Job, soft only
  - 🎯 Why this topic:
    - "JL 261007: how do we manage the runs, soft and hard, in the folder and on screen"
    - feeds q01 (what a Run is, where it may sit) and q07 (the Runs panel, the pop-out)
    - earlier decisions s01-D14 and s01-D15; the skill change is s01 run-skill-draft.md
- title: 🏃 The Run, its workbench and its skill
  intro: a button starts a Run, a Run keeps passes and a result, the screen lists them, the skill owns the card
  boxes:
  - id: button
    at: [0, 0]
    title: 🔘 A button
    why: a person asks for a piece of work
    most: 1
    tree:
    - ✅ the Runs panel sits beside every Space, at every level
    - "✅ it copies a prompt and starts nothing (first: ‹first_button›)"
    - ✅ each button names the skill that does its work
  - id: run
    at: [1, 0]
    title: 🏃 A Run, runs/<run>/
    why: one piece of work, asked for once
    most: 1
    tree:
    - ‹example_line›
    - "🎫 ticket ‹example_ticket›: the ask"
    - 🏁 close rule ‹example_close›
    - "📇 run.yaml: the card, written by a tool"
    - ✅ ‹close_line›
  - id: passes
    at: [2, 0]
    title: 🔁 Its passes, passes/pNN-<MMDD>/
    why: every round on the same target is one more pass, not a new Run
    most: 1
    tree:
    - ✅ ‹passes_line›
    - 🔁 a retry or a later session on the same target is a pass
    - 🆕 new inputs, a new goal or a new target is a new Run
    - "❓ a wet Run repeated, a replication: proposed in s06-D02"
  - id: result
    at: [3, 0]
    title: 📤 Its result
    why: what stays after the Run
    most: 1
    tree:
    - "🪨 hard: result/ with metrics, a table, a figure; evidence"
    - "🪶 soft: the change in draft/ studio/ reports/ delivery/; work, not evidence"
    - ⬜ heavy output goes to _WorkSpace/ProjectResult/, pointed to by result/heavy.yaml
    - ❓ show a hard Run's heavy output on screen, or only its pointer?
  - id: screen
    at: [0, 1]
    title: 🗂️ The Runs Space, on screen
    why: one plain list of a level's Runs
    most: 1
    tree:
    - ✅ ‹cols_line›
    - "✅ third row: ‹subs›"
    - ❓ ‹cols_n› columns today; s06-D01 proposed seven
    - "❓ a row opens nothing yet: the Run pop-out is proposed in s06-D01"
    - ❓ this level's Runs only, or rolled up from the levels below?
  - id: hard
    at: [1, 1]
    title: 🪨 A hard Run, rNN_<slug>
    why: it makes new evidence, so only a work Task holds one
    most: 1
    tree:
    - ✅ runs/r01_rate_tir_hypo/ (Proj11-CGM-Corpus)
    - 📇 run.yaml, the ticket .sh, config.yaml
    - 📤 result/ holds metrics.json, reward_spec.yaml
    - 🔁 passes/p01-<MMDD>/ hold the log and runtime.yaml
    - ❓ still in the older layout, runs/r01_rate_tir_hypo.sh beside results/ (open 6)
  - id: soft
    at: [2, 1]
    title: 🪶 A soft Run, run-<type>-<target>
    why: it changes what its level keeps, at a Block, a Job or a Task
    most: 1
    tree:
    - "✅ example ‹passes_run›: kind ‹passes_kind›, status ‹passes_status›"
    - 📝 pass.md holds the ask, summary and changed files
    - "❓ a Job holds soft Runs only: where does a batch launch, run-launch-<group>, go?"
    - ❓ when does a soft pass close, and who writes its touched.yaml?
  - id: skill
    at: [3, 1]
    title: 🧰 The skill /haipipe-run ‹version›
    why: it owns what a Run is, so tools write the card and passes
    most: 1
    tree:
    - ✅ soft_run.py new <scope> --type draw --target s05
    - ✅ soft_run.py pass <scope>/runs/run-draw-s05
    - "🖥️ servers/workbench/frame.py: runs_of"
    - "🖥️ servers/workbench/runs_panel.py: run_types, panel_html, panel_markup"
    - "❓ wet Runs: add a protocol ticket and a person-signed receipt? (s06-D02)"
  arrows:
  - {from: button, to: run, label: starts}
  - {from: run, to: passes, label: adds a pass}
  - {from: passes, to: result, label: writes}
  - {from: run, to: hard, label: if it makes evidence}
  - {from: soft, to: result, label: or changes}
  - {from: screen, to: run, label: lists}
  - {from: skill, to: soft, label: keeps the card}
```


Files
-----

```text
s06-run-workbench-skill/
├── s06-run-workbench-skill.md               this face
├── build_s06_run_workbench_skill.py         the builder; marks are kept on rebuild
├── s06-run-workbench-skill.excalidraw       three frames: Background (a tree), the Run (boxes with trees joined by named arrows, emoji on every node), the screen
├── s06-run-workbench-skill.png              its preview
├── .s06-run-workbench-skill.seed.json       generated snapshot for preserving marks
└── history/                                 the 261010, 261012 and 261012b builders, drawings, previews and faces
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
① Background       a tree: the words (Run, ticket, close rule, pass, hard, soft, Runs Space, skill),
                   where a Run sits, why the topic exists
② The Run          boxes joined by named arrows: 🔘 a button -starts-> 🏃 a Run -adds a pass->
                   🔁 its passes -writes-> 📤 its result; 🗂️ the Runs Space lists; 🪨 hard and
                   🪶 soft Runs; 🧰 the skill /haipipe-run; red ❓ leaves are still open
③ The screen       this Block's Runs Space as frame.py draws it, beside /haipipe-run
                   (a ui_frame, in the workbench's colours)
```

Frames ① and ② are the face's `frames:` yaml above, drawn by `topic_map.draw_topic`; the builder fills the words in ‹ › from disk on every build: this Block's Runs (`runs/*/run.yaml`, each ticket's `close:` line), its
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
s06-D07 · Decided (JL 261012, through the b10 watcher: "go ahead and do all"): the drawing is three frames, each a folder tree: ① Background, ② the Tree, ③ the screen (the Runs Space and the skill); the old frames are folded in; the old builder, face and preview are in history/.
s06-D08 · Decided (JL 261012, through the b10 watcher): the drawing is boxes with trees joined by named arrows, an emoji on every node (haipipe-studio 0.13.0); the old builder, face and preview are in history/ (-261012b).


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
