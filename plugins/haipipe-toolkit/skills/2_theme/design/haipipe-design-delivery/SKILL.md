---
name: haipipe-design-delivery
description: >-
  The release of a design Job on the ladder, and the one file another system reads.
  Owns run-freeze-predictions-j<NN> (each kept design's predicted effect frozen,
  a person signs) and run-release-j<NN> (the kept, passed designs written word for
  word into the Job's delivery/designs.json and designs.md, screens/ for a UI, and
  gathered into the Block's delivery/; a person signs), and the designs.json
  schema. Use to freeze predictions, release a Job, read or check designs.json, or
  hand released designs to the system that sends them. Ends at the release:
  sending and measuring belong downstream. Trigger: release designs, release a
  design Job, freeze design predictions, designs.json, design delivery, hand off
  designs, /haipipe-design-delivery.
metadata:
  version: "0.4.0"
  last_updated: "2026-10-07"
---

# /haipipe-design-delivery · the release and designs.json

## Version governance

Only explicit user approval may authorize a version change. This skill starts at `0.4.0` and keeps it (created
261007, b12 s12: "one owner for the one file another system reads").

## Position

A design Job (`haipipe-design/ref/design-ladder.md`) ends when a person releases its kept designs. This skill owns
that last step and its file:

```text
t99 run-rank-t99 ─▶ project_predictions.py (haipipe-design-workflow): prediction.yaml frozen: draft, kept | dropped
                 ─▶ run-freeze-predictions-j<NN>    a person signs the predictions
                 ─▶ run-release-j<NN>               a person signs the release
                    jNN_<goal>_<method>/delivery/designs.json · designs.md · screens/<dNN>.<ext>
                    Design-<name>/delivery/designs.json · designs.md · screens/<jNN>-<dNN>.<ext>
                                                   every Job's release, gathered
```

Both Runs are soft: they write `prediction.yaml` and `delivery/`, never a Result. What an Exp later returns comes back
to the Block (`haipipe-design-method`, `run-add-observed`), not here.

## run-freeze-predictions-j<NN>

Each kept design's `prediction.yaml` (`predicted · against · by · frozen`) changes from `frozen: draft` to
`frozen: <YYMMDD>`, the day a person signs. A frozen prediction is never edited again; the Exp is scored against it.
A dropped design's prediction stays a draft.

## run-release-j<NN>

A design is released when its state is `kept` and its prediction (with a predicted effect) is frozen. A Job whose
t99 ranked must have its ranking projected first (`project_predictions.py`); only a Job with no rank Run (a method
with no ⑤) releases its `passed` designs. Words that are still the scaffold's placeholder (`<the design, word for
word>`), or empty, are refused: the draft reaches the face only by `project_draft.py draft`. `release.py` checks every
design before it writes anything, so a refusal leaves no prediction half frozen. The release writes:

- `delivery/designs.json`: the schema in [ref/designs-schema.md](ref/designs-schema.md), the words exactly as the
  design Task's `## Design` holds them;
- `delivery/designs.md`: the same designs as a reader sees them, in rank order;
- `delivery/screens/<dNN>.<ext>`: for a UI design, the rendered screen the last verify judged, copied from its
  Result;
- the Block's `delivery/designs.json` and `designs.md`: this Job's designs added, never twice, each UI screen copied to
  the Block's `delivery/screens/<jNN>-<dNN>.<ext>` and named so there (two Jobs' d04 never collide);
- each released design Task's face: `state: released`.

```bash
python scripts/release.py <job folder> [--freeze YYMMDD] [--dry]
```

`release.py` refuses a design whose prediction is still a draft, unless `--freeze` gives the date a person signed;
then it freezes the predictions first (this is `run-freeze-predictions` and `run-release` in one session, each still
its own Run folder). It prints what it wrote. Run it again and nothing is added twice.

## Boundaries

- A person signs both Runs (the frozen predictions and the release, together) and later the Job's close; an agent
  prepares, never signs.
- The words are copied, never rewritten: a change to a design is a new pass of `run-revise` and a new verify, then a
  new release.
- A released Job is never edited; a changed method or inputs version is a new Job.
- Placeholders only in this skill; no application, patient or vendor content.

## Files

```text
haipipe-design-delivery/
├── SKILL.md                    this file
├── ref/designs-schema.md       the designs.json schema
├── scripts/release.py          freeze (with --freeze) and release one Job
└── tests/test_release.py
```
