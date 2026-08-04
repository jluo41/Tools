# Paper topic and probe-entry contract

This is the Paper-family projection of Board's generic `ref/topic-entry-contract.md`.
It keeps the paper's delivery stake separate from the bank's neutral work request.

```text
0-lifecycle/
├── S03-literature/                  discovery route
│   ├── S-Literature-<n>-<topic>.md  Q-consumer register
│   └── probes/L<n>-<topic>/         one entry page per q-executor
└── S04-value/                       task route
    ├── S-Value-<n>-<topic>.md       Q-consumer register
    └── probes/V<n>-<topic>/         one entry page per q-executor
```

An originating delivery S page may raise a Q as an Aim. Once it needs evidence, the direct topic page is canonical for that Q's evidence route, paper stake, target prose or claim, current interpretation, and entry path. Link back to the originating Aim rather than maintaining an unlinked second question. An entry page is canonical for the q-executor and its exchange with a bank.

Every entry has exactly one each of:

```markdown
#### q-executor
#### consumer trace
#### bank binding
**state**: planned | commissioned | deferred | read | answered-local
#### a-executor
```

The entry's consumer trace is an audit copy, never a competing register. Queue membership derives from the `**state**:` within bank binding: `planned`, `commissioned`, and `deferred` are queued; `read` and `answered-local` are resolved. New work never creates a top-level `1-probes/`. A migrated paper keeps old paths only beneath `0-lifecycle/_archive/1-probes/` as provenance.
