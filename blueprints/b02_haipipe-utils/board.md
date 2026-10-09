# b02 · haipipe-utils

board-kind: task-block
spine: The blueprint of the `plugins/haipipe-utils` package: the normalizers that turn free text in a cohort's own dialect into typed, referenced numbers, and the API that serves them.
close: Every Job's questions have a report Page with an answer status, and every answered question names the skill, server or bank change that settled it.

## Topic

One blueprint Block per package in `plugins/` (261009). haipipe-utils is a contract (haipipe-norm), four members
(describe-food, describe-exercise, describe-medication, describe-insulin), one API host (servers/) and the
reference banks they resolve against. One Job per part.

## Jobs

```text
j01_norm_contract   haipipe-norm: the five rules, the door, the shared packages
j02_food            describe-food: FoodName to USDA nutrition
j03_exercise        describe-exercise: activity to MET and kcal
j04_medication      describe-medication: MedicationID to an FDA drug and a dose with its unit
j05_insulin         describe-insulin: DrugKey to onset, peak, duration
j06_api             servers/: one host, a lane per noun
j07_banks           the reference banks in ExternalStore
```

## Questions

```yaml
questions:
- id: Q01
  title: Does the package say what it is?
  question: plugin.json (0.2.0) names only food and exercise, and the README says
    haipipe-norm ships no code; medication, insulin, the API host and the shared packages
    are missing from the package's own description.
  hypothesis: Bring plugin.json and the README up to the four members, the API and
    the shared packages, and keep them in step with each member's version.
  acceptance: Answered when the manifest and README list every member and the API,
    and a member's release updates them.
  work: []
  report: reports/q01_package_description/q01_package_description.md
- id: Q02
  title: How is a new member added?
  question: 'When a fifth noun joins (a lab value, a symptom), what does it need:
    the contract''s five rules, a client door, a bank and its manifest, an API lane,
    a benchmark?'
  hypothesis: haipipe-norm's 'adding a member' section is the checklist; a scaffold
    makes the folders; a member is done when its suite, lane and benchmark pass.
  acceptance: Answered when the checklist is tested by adding a member (or a dry run
    of one) and every step lands where the contract says.
  work: []
  report: reports/q02_adding_a_member/q02_adding_a_member.md
```
