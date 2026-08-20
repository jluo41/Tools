# Paper evidence-page and QA-probe contract

This is the Paper-family projection of Board's generic `ref/topic-entry-contract.md`.
It keeps the paper's delivery stake separate from the bank's neutral work request.

```text
0-lifecycle/
├── S03-literature/                  discovery route · head `route: outward`
│   ├── S-Literature-<n>-<topic>.md  evidence page: E<n> divisions + E0 incoming
│   └── probes/L<nn>-<topic>/        one <n>-<slug>.md QA-probe per Q-executor
└── S04-value/                       task route · head `route: inward`
    ├── S-Value-<n>-<topic>.md       evidence page: E<n> divisions + E0 incoming
    └── probes/V<nn>-<topic>/        one <n>-<slug>.md QA-probe per Q-executor
```

A QA-probe ("entry" survives only as an informal alias) is a hidden SOURCE RECORD, not a board page (JL ruling B, 260806): "an entry is a source file the topic page points at, like a PDF; the board renders the topic page, never the entry." One conversation, two QAs: the QA-bank is the original, the QA-probe is the paper's stub that points at it through `**target**:`. Word order matters: QA-bank and QA-probe, never bank-QA or probe-QA. Consumer and executor name SLOTS only, and the four slot words are CAPITALS everywhere, including heading slots: Q-consumer and A-consumer on the evidence page's consumer rows, Q-executor and A-executor inside either QA. Never a file name. The QA-probe's digit-first `<n>-<slug>.md` name, `<n>` restarting at 1 per drawer, keeps it out of the board's Q/S/Agent/Meeting page sweep. It carries no page frame: a `# title` line, a `requires:` line, and the four slots below, nothing more.

The evidence page organizes its Content BY EXECUTOR (JL 260806): one `### E<n> · <the executor question>` division per Q-executor conversation, each carrying its `🔗 QA-probe:` pointer with the record's state, a `#### consumers` block (one row per collected Q-consumer: source page id, the stake in one line, the A-consumer interpretation, and the row state ⬜ · SUPPORTED|BOUND · DEFERRED · WITHDRAWN), and a `#### answer digest` block of 2-3 lines from the A-executor. `### E0 · incoming` is the standing queue: a Q-consumer born on any page is COLLECTED there until EVIDENCE translates it into a new E<n> and opens its QA-probe. One E<n> division ↔ one QA-probe; many QA-probes may point at one QA-bank, and that sharing lives at the bank.

An originating delivery S page may raise a Q as an Aim. Once it needs evidence, the direct evidence page is canonical for that Q's evidence route, paper stake, target prose or claim, current interpretation, and QA-probe path. Link back to the originating Aim rather than maintaining an unlinked second question. The QA-probe is canonical for the Q-executor and its exchange with a bank.

Every QA-probe has exactly one each of:

```markdown
#### Q-executor
#### consumer trace
#### bank binding
**state**: planned | commissioned | deferred | read | answered-local
#### A-executor
```

The QA-probe's consumer trace is an audit copy, never a competing consumer surface; `consumer trace` and `bank binding` are not among the four slot words and stay lowercase. Queue membership derives from the `**state**:` within bank binding: `planned`, `commissioned`, and `deferred` are queued; `read` and `answered-local` are resolved. New work never creates a top-level `1-probes/`. A migrated paper keeps old paths only beneath `0-lifecycle/_archive/1-probes/` as provenance.
