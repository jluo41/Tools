# b01 · Example prior work (placeholder)

board-kind: discovery-block
spine: What earlier work found about <a policy> and <an outcome>; three made-up papers read as numbered Runs, their Evidence Bib handed to the Paper-Example.
close: Every Task Page is checked and every placeholder Paper Run has a truthful terminal state.

## Topic

Placeholder only: the discovery theme's example Block in the public Tools repo. Its papers are made up; each is read by
a numbered Paper Run whose Ticket calls `paper_result_build.py --placeholder` (no network call), so every Result, the
Evidence Bib and its hand-over are rebuilt by rerunning a Ticket. Tools' Paper-Example cites the three papers
(`paper/Paper-Example/j03_evidence_cite` reads `j01_policy_effect_inquiry/t01_policy_prior_work`). It leaves out how the
paper prints a citation and how real papers are found.

## Questions

The questions this example Block answers, in two groups. Every paper here is made up.

```yaml
questions:
- id: Q01
  title: The earlier effect
  group: Prior work
  question: What did earlier work find about <the policy> and its effect on <an outcome>?
  report: reports/q01-earlier-effect.md
  work:
  - path: j01_policy_effect_inquiry/t01_policy_prior_work
    stage: Discovery
    role: Reads the earlier studies, one placeholder paper per Run.
- id: Q02
  title: The setting
  group: Prior work
  question: In which settings was the effect measured?
  report: reports/q02-setting.md
  work:
  - path: j01_policy_effect_inquiry/t01_policy_prior_work
    stage: Discovery
    role: Names each paper's setting in its Card.
- id: Q03
  title: The subgroup
  group: Subgroups
  question: Did any earlier work look at the effect by <a characteristic>?
  work:
  - path: j02_subgroup_effect_inquiry/t01_subgroup_prior_work
    stage: Discovery
    role: Will search for papers that split the effect by <a characteristic>.
```

## Pipeline
SCOPE -> PREPARE? -> ACQUIRE -> SYNTHESIZE -> Page CHECK -> CLOSE
## Board Map
```text
Block / Board
└── Job / Group
    └── Task Page
        └── Paper or Source Runs
```
## Pages

<!-- haipipe:discovery-board-jobs:start -->
### j01 · j01_policy_effect_inquiry
The folder name is the Job/Group identity; Task Pages below it are discovered from the direct tree.
### j02 · j02_subgroup_effect_inquiry
The folder name is the Job/Group identity; Task Pages below it are discovered from the direct tree.
<!-- haipipe:discovery-board-jobs:end -->
