# S04 Value · topic-entry store

This is the Paper-specific home for questions answered with project-task evidence.
It is a runtime storage contract, not a user-facing lifecycle stage.

```text
0-lifecycle/S04-value/
├── S-Value-<n>-<topic>.md            evidence page · E<n> divisions
└── probes/V<nn>-<topic>/
    └── <n>-<slug>.md                 one QA-probe per Q-executor, hidden
```

A QA-probe (the entry record) is not a board page (JL ruling B, 260806): its
digit-first name keeps it out of the board's page sweep, so only the topic
page renders. One conversation, two QAs: the QA-bank is the original, the
QA-probe is the paper's copy that points at it.

The direct topic page owns the paper-facing question, its stake, and its final
interpretation. One nested QA-probe owns a stake-free `#### Q-executor`, an audit
`#### consumer trace`, its `#### bank binding`, and `#### A-executor` answer.

Use this store when the evidence must come from a project task, run, data
inspection, or other task-bank work. See `../haipipe-paper/probe/topic-entry-contract.md`.
