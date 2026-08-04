# S03 Literature · topic-entry store

This is the Paper-specific home for questions answered with external discovery.
It is a runtime storage contract, not a user-facing lifecycle stage.

```text
0-lifecycle/S03-literature/
├── S-Literature-<n>-<topic>.md       canonical Q-consumer register
└── probes/L<n>-<topic>/
    └── S-Literature-<n>-<slug>.md    one Q-executor entry
```

The direct topic page owns the paper-facing question, its stake, and its final
interpretation. One nested entry owns a stake-free `#### q-executor`, an audit
`#### consumer trace`, its `#### bank binding`, and `#### a-executor` answer.

Use this store when the evidence must come from literature, search, review, or
other external discovery. See `phase/1-probe/haipipe-paper-probe/ref/topic-entry-contract.md`.
