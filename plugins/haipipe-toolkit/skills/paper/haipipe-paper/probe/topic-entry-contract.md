# Paper topic and probe-entry contract

This is the Paper-family projection of Board's generic `ref/topic-entry-contract.md`.
It keeps the paper's delivery stake separate from the bank's neutral work request.

```text
0-lifecycle/
├── S03-literature/                  discovery route
│   ├── S-Literature-<n>-<topic>.md  Q-consumer register
│   └── probes/L<nn>-<topic>/        one <n>-<slug>.md probe QA per q-executor
└── S04-value/                       task route
    ├── S-Value-<n>-<topic>.md       Q-consumer register
    └── probes/V<nn>-<topic>/        one <n>-<slug>.md probe QA per q-executor
```

An entry is a probe QA (the entry record): a hidden SOURCE RECORD, not a board page (JL ruling B, 260806): "an entry is a source file the topic page points at, like a PDF; the board renders the topic page, never the entry." One conversation, two QAs: the bank QA is the original, the probe QA is the paper's copy that points at it through `**target**:`. Consumer and executor name SLOTS only (Q-consumer and A-consumer on the register row, q-executor and a-executor inside either QA), never files. The probe QA's digit-first `<n>-<slug>.md` name, `<n>` restarting at 1 per drawer, keeps it out of the board's Q/S/Agent/Meeting page sweep. It carries no page frame: a `# title` line, a `requires:` line, and the four slots below, nothing more.

An originating delivery S page may raise a Q as an Aim. Once it needs evidence, the direct topic page is canonical for that Q's evidence route, paper stake, target prose or claim, current interpretation, and probe QA path. Link back to the originating Aim rather than maintaining an unlinked second question. The probe QA is canonical for the q-executor and its exchange with a bank.

Every entry has exactly one each of:

```markdown
#### q-executor
#### consumer trace
#### bank binding
**state**: planned | commissioned | deferred | read | answered-local
#### a-executor
```

The entry's consumer trace is an audit copy, never a competing register. Queue membership derives from the `**state**:` within bank binding: `planned`, `commissioned`, and `deferred` are queued; `read` and `answered-local` are resolved. New work never creates a top-level `1-probes/`. A migrated paper keeps old paths only beneath `0-lifecycle/_archive/1-probes/` as provenance.
