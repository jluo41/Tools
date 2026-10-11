s05 · Runs
==========

**Tags:** `Workflow`

**Topic:** how Runs are managed: the hard and the soft Run, how one looks in its folder, how it
lives (type, Spec, folder, passes, close), and how it shows in the workbench (JL 261007: "how do we
manage the runs here ... the soft run, the hard run, how the run looks like in the folder and
workbench"). It starts from the contract haipipe-run 0.31.0 states today; the earlier decisions are
s01-D14 and s01-D15, and the change that put them in the skill is `../s01-overall-tree-structure/run-skill-draft.md`.

**Feeds:** `reports/q01_bjtr_boundary/` (what a Run is, and where it may sit), `q07_workbench_mapping/`
(the Runs panel, the Runs Space, the pop-out).


Files
-----

```text
s05-runs/
├── s05-runs.md              this face: what is decided, what is open
├── build_s05_runs.py        the builder; marks are kept on rebuild
├── s05-runs.excalidraw      the drawing: five frames, a plain prototype
└── s05-runs.png             its preview
```

Rebuild: `python build_s05_runs.py` (or `../_build/make.sh`).


What the drawing holds
----------------------

```text
1 · Hard and soft     name · ticket · output · counts as · where · receipt · new pass · new Run, for
                      hard, soft, and a wet hard Run (red: proposed in s01-D28)
2 · In the folder     a work Task's runs/ (one hard, one soft), a Block's or Job's runs/ (soft only),
                      and today's older layout (runs/<run>.sh beside results/<run>/)
3 · Life of a Run     run type -> Run Spec -> runs/<run>/ -> passes/pNN-<MMDD>/ -> closed;
                      when a pass, when a new Run
4 · On screen         the Runs panel beside every Space; the Runs Space on every level (one plain list
                      from run.yaml, filtered by kind or type); a Run pop-out (card, passes, result preview)
Questions             what is still open
```


Settled (in haipipe-run 0.31.0)
-------------------------------

1. A Run is hard or soft by where its output lands. Hard `rNN_<slug>`: its own `result/`, evidence,
   a work Task only. Soft `run-<type>-<target>`: writes into its scope's `draft/ studio/ reports/
   delivery/`, not evidence, at a Block, a Job or a Task.
2. One Run is one folder in `runs/`: its ticket, `run.yaml` (the card), and `passes/pNN-<MMDD>/`;
   a hard Run adds `config.yaml` and `result/`. Folder name = ticket stem = `run.yaml` `run:`.
3. A pass is one more execution (hard) or one more round on the same target (soft); new inputs or a
   new target make a new Run.
4. Heavy output goes to `_WorkSpace/ProjectResult/<...>/<run>/`; `result/heavy.yaml` points to it.


Proposed
--------

s05-D01 · Proposed (261007): on screen, a Runs panel sits beside every Space at every level: that
    Space's run types as buttons (they copy a prompt and start nothing), then the recent Runs of that
    Space. Each level tab also has a Runs Space: one plain list of its Runs, read from each `run.yaml`
    (run · kind · type · target · status · passes · last), filtered by the third row (All · hard ·
    soft · <type>). A row opens the Run pop-out: the card, its passes, a result preview (hard:
    metrics and the first figure; soft: before/after and the ledger).
s05-D02 · Proposed (261007): a wet Run is a hard Run a person carries out: an `rNN_<slug>.md`
    protocol ticket, a `result/` holding the data collected and an observation log, and a
    `runtime.yaml` the person signs. It cannot repeat exactly, so a replication is a new Run.
    Needs haipipe-run to accept a protocol ticket and a signed receipt (open 1).
s05-D03 · Proposed (261007): an agent session that works on a studio topic is a pass of that topic's
    soft Run, `run-draw-<sNN>` (s04-D06): the ask, the summary, what changed. So a session needs no
    folder of its own, and it lists with every other Run.


Open
----

1. Wet Runs: add the protocol ticket and the person-signed receipt to haipipe-run?
2. Block and Job Runs are soft only: where does a Job's batch launch (`run-launch-<group>`) go?
3. A hard Run's heavy output: show it on screen, or only its `heavy.yaml` pointer?
4. The Runs Space: this level's Runs only, or rolled up from the levels below?
5. A soft pass: when does it close, and who writes its `touched.yaml`?
6. The older layout: when does haipipe-project `update` move each Project's Runs?
