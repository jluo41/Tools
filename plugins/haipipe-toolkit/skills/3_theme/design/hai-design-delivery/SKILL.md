---
name: hai-design-delivery
description: "The release of a design Job on the ladder: freezes each kept design's predicted effect, then writes the kept, passed designs into the Block's delivery/ (designs.json); a person signs. Use to release a Job or check designs.json. Trigger: release designs, designs.json, /hai-design delivery."
disable-model-invocation: true
metadata:
  version: "0.4.1"
  last_updated: "2026-11-27"
---

# /hai-design delivery · the release and designs.json

> Scripts here need Python 3.10+: where a command says `python3`, run it as `uv run --python 3.13 --with pyyaml python ...` (or a SPACE `.venv/bin/python`); see `plugins/haipipe-toolkit/skills/README.md` § Running a skill's scripts.


Delivery storage
---------------------------

Only the Block owns a physical `delivery/` directory. Job, Task and Report
outputs retain their source identity under it: `delivery/jNN_〈job〉/`,
`delivery/jNN_〈job〉/tNN_〈task〉/〈lane〉/`, and
`delivery/reports/qNN_〈report〉/〈lane〉/`. The Block's own output uses
`delivery/〈lane〉/`. Job and Task Delivery views select their source subtree
and link to the whole Block Delivery; they never create local delivery folders.
Runs and Results remain with their source. Every writer and reader uses the
shared `hai-draft/src/common.py` Delivery helpers. Standalone Pages without
a Block keep their own output root; an orphan jNN/tNN must acquire a Block.

In this skill, a Page's or Job's `delivery/〈lane〉/` means its source subtree
inside Block Delivery. Rebuild generated output from source and preserve hand-owned fragments.
A storage operation grants no acceptance, release, send or submission approval.


## Version governance

Keep the version declared in metadata. Change it only with explicit user approval.

## Position

A design Job (`hai-design/ref/design-ladder.md`) ends when a person releases its kept designs. This skill owns
that last step and its file:

```text
t99 run-rank-t99 ─▶ project_predictions.py (hai-design-workflow): prediction.yaml frozen: draft, kept | dropped
                 ─▶ run-freeze-predictions-j〈NN〉    a person signs the predictions
                 ─▶ run-release-j〈NN〉               a person signs the release
                    Design-〈name〉/delivery/jNN_〈goal〉_M0x-〈slug〉-mK_inputs-vM/designs.json · designs.md · screens/〈dNN〉.〈ext〉
                    Design-〈name〉/delivery/designs.json · designs.md · screens/〈jNN〉-〈dNN〉.〈ext〉
                                                   every Job's release, gathered
```

Both Runs are soft: they write `prediction.yaml` and `delivery/`, never a Result. What an Exp later returns comes back
to the Block (`hai-design-method`, `run-add-observed`), not here.

## run-freeze-predictions-j〈NN〉

One review, one sign: the workbench shows this Run and the release as one button, Review and approve.
A person reads each kept design as it reads, its prediction with its `why`, and its review, then signs once.

Each kept design's `prediction.yaml` (`predicted · against · by · why · frozen`) changes from `frozen: draft` to
`frozen: 〈YYMMDD〉`, the day a person signs. A frozen prediction is never edited again; the Exp is scored against it.
A dropped design's prediction stays a draft.

## run-release-j〈NN〉

A design is released when its state is `kept` and its prediction (with a predicted effect) is frozen. A Job whose
t99 ranked must have its ranking projected first (`project_predictions.py`); only a Job with no rank Run (a method
with no ⑤) releases its `passed` designs. Empty words or an unfilled scaffold placeholder are refused: the draft reaches the face only by `project_draft.py draft`. `release.py` checks every
design before it writes anything, so a refusal leaves no prediction half frozen. The release writes:

- `delivery/designs.json`: the schema in [ref/designs-schema.md](ref/designs-schema.md), the words exactly as the
  design Task's `## Design` holds them;
- `delivery/designs.md`: the same designs as a reader sees them, in rank order: each under its Job's folder name
  (never the bare `jNN`), its words, then `Predicted 〈effect〉 against 〈what〉. Why: 〈the basis〉`;
- `delivery/screens/〈dNN〉.〈ext〉`: for a UI design, the rendered screen the last verify judged, copied from its
  Result;
- the Block's `delivery/designs.json` and `designs.md`: this Job's designs added, never twice, each UI screen copied to
  the Block's `delivery/screens/〈jNN〉-〈dNN〉.〈ext〉` and named so there (two Jobs' d04 never collide);
- each released design Task's face: `state: released`.

```bash
python scripts/release.py 〈job folder〉 [--freeze YYMMDD] [--dry]
```

`release.py` refuses a design whose prediction is still a draft, unless `--freeze` gives the date a person signed;
then it freezes the predictions first (this is `run-freeze-predictions` and `run-release` in one session, each still
its own Run folder). It prints what it wrote. Run it again and nothing is added twice.

## The one-page summary

`summary.py` builds a one-page overview with one traced design example from what the Runs wrote, never by hand, into the Block's `delivery/summary.html` and
`summary.pdf` (printed by a local Chrome, headless; without one only the HTML):

- the goal, then the bottom line: the Opening of each Block question whose report is partly or fully answered;
- one row per Job: its method by name, designs released, its rank-1 design and prediction; a held Job's first `## Hold`
  sentence; who approved, when and how, from each `run-release-j〈NN〉` card's `signed:` line;
- one design traced: its words as they read, where it came from (its `why`), its frozen prediction; by default the
  rank-1 design with the narrowest predicted range (the most certain), or `--example jNN:dNN`;
- the next step, and the sources it read.

```bash
python scripts/summary.py 〈block folder〉 [--example jNN:dNN] [--no-pdf]
```

Rebuild it after a release, an answered question or an experiment result. The workbench's Summary links the PDF.

## Boundaries

- A person signs both Runs (the frozen predictions and the release, together) and later the Job's close; an agent
  prepares, never signs.
- The release copies words exactly. Before release, a revision needs a new revise pass and independent verify.
  After release, changed designs require a new Job with its own pins and review; never reopen a released Job.
- A released Job is never edited; a changed method or inputs version is a new Job.
- Placeholders only in this skill; no application, patient or vendor content.

## Files

```text
hai-design-delivery/
├── SKILL.md                    this file
├── ref/designs-schema.md       the designs.json schema
├── scripts/release.py          freeze (with --freeze) and release one Job
├── scripts/summary.py          the Block's one-page summary: delivery/summary.html · .pdf
└── tests/test_release.py · test_summary.py
```
