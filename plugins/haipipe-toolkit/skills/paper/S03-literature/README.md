# S03 Literature · topic-entry store

This is the Paper-specific home for questions answered with external discovery.
It is a runtime storage contract, not a user-facing lifecycle stage.

```text
0-lifecycle/S03-literature/
├── S-Literature-<n>-<topic>.md       canonical Q-consumer register
└── probes/L<nn>-<topic>/
    └── <n>-<slug>.md                 one probe QA per q-executor, hidden
```

A probe QA (the entry record) is not a board page (JL ruling B, 260806): its
digit-first name keeps it out of the board's page sweep, so only the topic
page renders. One conversation, two QAs: the bank QA is the original, the
probe QA is the paper's copy that points at it.

The direct topic page owns the paper-facing question, its stake, and its final
interpretation. One nested probe QA owns a stake-free `#### q-executor`, an audit
`#### consumer trace`, its `#### bank binding`, and `#### a-executor` answer.

Use this store when the evidence must come from literature, search, review, or
other external discovery. See `../haipipe-paper/probe/topic-entry-contract.md`.
