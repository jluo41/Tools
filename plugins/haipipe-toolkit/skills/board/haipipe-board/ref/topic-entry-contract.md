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
