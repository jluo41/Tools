# Minimal example: a board with two questions

For a real board see `../../../diagrams/BoardSkillBoard-260722/` (this plugin's `skills/diagrams` folder), this skill's own board, with 10 questions.
What follows is only the minimal skeleton you can copy.

Folder: `examples/ProjX-Demo/diagram/01-cohort-260801/`

---

## `board.md`

````markdown
# Cohort entry criteria: settle who enters the cohort and who does not
spine: turn "which patients count for this study" into a rule set someone can screen with, every line of it with a stated reason.
close: every Q below has reached ✅ or ⏸️, at which point the entry criteria can be written into the paper's Methods.
source: collaborations/Event-Cohort/meetings/2026-08-01 cohort discussion.md

## Topic
We hold a 2015 to 2020 insurance claims dataset and want to study one class of prescribing behavior.
The first step is deciding who enters the analysis cohort: get this step wrong and every later result is void.
People: JL = project lead, decides. Other colleagues claim work under their own initials.

## Pipeline
The two questions are ordered: first settle what we screen on (QA1), then settle how to validate what came out of the screen (QA2).

## Pages
### QA · Settle the criteria first
QA1-criteria.md
QA2-validate.md
````

---

## `QA1-criteria.md`

````markdown
# The four entry conditions
state: 🟡 PARTIAL
owner: ZW
method: list them one at a time, each with a check that can actually run

## Opening
What must a patient satisfy to enter this study's analysis cohort?

Wrong entry criteria void every later result, and this is the most expensive thing in the project to rework.
While it stays open, QA2 has no stable cohort to validate.

## Outline
```
all claims records  1,240,000 people
      │  ① age ≥ 18
      ▼      980,000
      │  ② ≥ 12 months of continuous enrollment in the observation window
      ▼      410,000
      │  ③ at least one target prescription
      ▼       38,000
      │  ④ drop anyone with a pre-existing contraindication
      ▼       31,500   ← analysis cohort
```

## Aims
### P · Page-level cohort definition
- ✅ P1 · All four conditions exist as executable checks.
  **Done when:** Each translates into one SQL statement or a short code block, not "roughly".
  **Now:** Met; all four checks run.
- ✅ P2 · Every condition has a head count.
  **Done when:** The page reports how many people survive each screen, layer by layer.
  **Now:** Met; the layer-by-layer counts are reported (31,500).
- 🧠 P3 · Every condition has a stated reason.
  **Done when:** A reviewer can see why each screen belongs.
  **Now:** Waiting for the contraindication list (condition ④) to be checked; what we run today is a list copied from elsewhere that nobody has checked.

## Glossary
observation window: the stretch of time in which the data can see this person's records, so anyone whose window is too short has an incomplete prescription history and cannot be counted.

## Discussion
> JL: where does the 12 months in condition ② come from?

## Log
260801 1400 · question opened, four conditions written down first
260801 1415 · layer-by-layer head counts run
````

---

## `QA2-validate.md`

````markdown
# Validating the screened cohort
state: 🔴 OPEN
owner: ZW
method: compare the demographic distribution against a published cohort

## Opening
QA1's four conditions leave 31,500 people, so how do we know the screen was right?

A head count on its own carries no credibility, and a reviewer will press on whether these people really satisfy the entry rules.
Until QA1's condition ④ is settled, any validation result is unstable too.

## Aims
### P · Page-level validation
- 🧠 P1 · Demographics line up with a published cohort.
  **Done when:** Age, sex, and region show no unexplained large gap.
  **Now:** Not started; waiting for QA1 condition ④, before which any validation result is unstable.
- 🧠 P2 · Fifty people pass manual review.
  **Done when:** Raw-record review confirms each sampled person belongs in the cohort.
  **Now:** Not started; waiting for QA1 condition ④.

## Discussion

## Log
260801 1430 · question opened
````
