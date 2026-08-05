# Topic page and nested entry contract

Use this optional overlay when a Board has one reader-facing topic page and several neutral requests to run beneath it.
The contract is generic. It names neither a Paper stage nor an evidence bank.

```text
S topic page
  ├── ### Q-consumer register     canonical reader-facing need and stake
  └── probes/<topic>/
       └── one entry page = one q-executor
            ├── consumer trace    audit copy of the Q-consumer
            ├── bank binding      route, target, and state
            └── a-executor        the returned answer
```

An originating delivery page may raise a Q first. The topic page owns its canonical evidence-routing record, while an entry owns the q-executor because it is the neutral question another system can answer. The consumer trace is never a second register.

## Register route line

The register's first line under `### Q-consumer register` is REQUIRED and machine-readable:

```text
route: outward    the questions face published knowledge
route: inward     the questions face results this project must produce
```

The line is the page's type key. A topic page wears a stage-shaped filename, and the register marker alone cannot separate the two routes, so a register with no `route:` line, or with any other value, leaves the page's type unresolvable and the page defective. `route: outward` resolves the page to `page-types/haipipe-board-page-for-literature`; `route: inward` resolves it to `page-types/haipipe-board-page-for-value`.

## Register-row states

A register row ends in exactly one of three states, written on the row itself:

- RESOLVED · the row's stake is met: SUPPORTED by named sources on the outward route, BOUND to an accepted run by path on the inward route
- DEFERRED · with the reason written on the row
- WITHDRAWN · because the claim or need the row served changed

A row in none of these states holds the topic open. The topic's human gate reads the register, not the entries: an answer sitting in an entry's `#### a-executor` that never became a register record does not close its row.

## Entry shape

An entry page lives below `probes/<topic>/`, has `requires: <topic-page-id>`, and has exactly one each of:

```markdown
#### q-executor
#### consumer trace
#### bank binding
**state**: planned | commissioned | deferred | read | answered-local
#### a-executor
```

Queue membership is derived, not maintained in another file. `planned`, `commissioned`, and `deferred` are queued. `read` and `answered-local` are resolved.

`cli/check.py` detects this overlay only when an S page declares `### Q-consumer register`. It then checks direct-topic dependency, entry anatomy, bank state, and whether each trace id occurs in its parent register.
