## 0.13.0 · 2026-11-13 · the start door knows the two loops

- `scripts/start.py` reads 🧭 meaning and 🛠 expression Tasks and opens the new focus page (`layout=focus`), which
  opens on the step that needs you; it no longer links the old Work Details tabs. After the items Task it asks
  `engine/two_loops.py` for the one next thing: a waiting form, an unsigned guideline, a round that sent cards back
  to meaning, the next round, the release sign, then the Job's Delivery once the release is signed.
- `engine/two_loops.py` is the one rule for where a meaning or expression Task opens; the workbench page
  (`labeling_steps.default_view`) uses it too, so the door and the page agree.
- `engine/items_task.next_step` links the items Task's focus page and names its steps Data, Items, Embedding.
- The meaning and expression skills reply with Report › <step> links (Work is retired).

## 0.12.0 · 2026-11-01

- The two loops (b15 s58, stage 2; JL 261101: "Please make them work"): a Job's building as two Tasks, 🧭 meaning (`labeling-meaning`) and 🛠 expression (`labeling-expression`); routing to the new kinds `interaction` (Frame, Report, Preferences, Update) and `expression` (a round, Release).

## 0.11.1 · 2026-10-14 · keys is now ground truth

- The Task type once called keys is ground truth (📏): papers say ground truth or gold labels, not keys; its
  `task-type: raw` line is unchanged.

## [0.11.2] — 2026-10-26

Door for hidden helpers (15 stage skills): they leave the skill listing (`disable-model-invocation: true`) and this door reads their SKILL.md by path. (door 261026)

## 0.11.0 · 2026-10-14 · Start from a Job

- `/haipipe-labeling <Job folder>` is the person's one start message: `scripts/start.py` reads the Job (its Tasks
  by `task-type:`), opens the workbench on the tab of the step the Job is at (through /wb), and prints the ladder,
  the step now and who does it; the door then guides that one step and stops. The items Task's steps go to
  `haipipe-labeling-preparation` (b15 s41); after the items, the no-argument behaviour runs on the building Task.

# haipipe-labeling · CHANGELOG

## 0.10.0 · 2026-10-07

Renamed from `subjective-label` to `haipipe-labeling`, the door name every theme
uses (`haipipe-<theme>`, JL 261007); the folder is `skills/2_theme/labeling/haipipe-labeling/`.
The view skills (`subjective-label-<view>`), schema ids (`subjective-label/v2`, ...)
and the receipt `domain` keep their names. `workbench-labeling` moved up to
`skills/2_theme/labeling/workbench-labeling/` in the same change.

## 0.9.1 · 2026-09-29

Clarify that a View context Skill is one of several Skills declared by a Run
Type. The Run Type table names shared workflow, domain, and procedure Skills
as well; a historical Run's actual Skill usage is not inferred from that table.

## 0.9.0 · 2026-09-29

Add the VIEW layer: eleven view skills, one per workbench view, never shared
(JL 260929). A Run card names only its view skill; route a Run request there.

## 0.7.0 · 2026-09-01

Replace four phase-sized Runs with 25 independently closable P0-P5 operation
kinds. Keep episodes and human gate events outside the Run count, and separate
planned counts from receipt-backed actual inventory.

## 0.6.0 · 2026-09-01

Separate the Level-3 Labeling job from its Level-4 Runs and route allocation,
resume, presentation, and audit through the new Labeling Run dialect.

## 0.5.0 · 2026-08-30

First versioned edition of the three-layer family (goal session, Stages A+B). LAW doors (`label-building`, `label-scanning`), ORDER machines (`label-building-workflow`, `label-scanning-workflow`), and the CROSSING (`subjective-label-workflow`: P0-P5, G0-G6, handoff, invalidation). Round unit + register + rendered views in `ref-assets.md` §1/§3/§6a; exercised by `fixtures/job-mini/` and its board `fixtures/job-mini-board-260830/`. Cold-run defects fixed same day: G2/G3 split (stop vs freeze signature), P3 single authority artifact, registry single definition with the Final Evaluator as writer, use-vs-define rule for phase numbers.
