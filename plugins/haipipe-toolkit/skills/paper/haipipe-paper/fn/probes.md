# Paper probe routing

The Paper layer owns why a question matters. The task and discovery layers own
the evidence. PROBE is the durable path between them:

```text
DRAFT: direct topic page owns the Q-consumer and paper stake
  ↓
PROBE: one nested entry owns the Q-executor and bank binding
  ↓
EXECUTOR: task or discovery produces a QA file
  ↓
PROBE: entry copies the answer; topic page records paper interpretation
```

## Runtime layout

```text
0-lifecycle/
├── S03-literature/
│   ├── S-Literature-<n>-<topic>.md
│   └── probes/L<n>-<topic>/S-Literature-<n>-<slug>.md
└── S04-value/
    ├── S-Value-<n>-<topic>.md
    └── probes/V<n>-<topic>/S-Value-<n>-<slug>.md
```

S03 is for outside-project discovery. S04 is for project-task evidence. The
direct topic page is canonical for its `### Q-consumer register`: it states the
paper-facing question, stake, and final interpretation. Every nested entry has
one direct topic `requires:` and exactly this anatomy:

```markdown
#### q-executor
<neutral, stake-free question sent verbatim to the executor>

#### consumer trace
Q-<Stage>-<n> <audit copy only; it must exist in the parent topic register>

#### bank binding
**route**: task | discovery
**bank**: reuse | run | code | new
**target**: <QA file or NEW>
**state**: planned | commissioned | deferred | read | answered-local

#### a-executor
<answer copied from the resolved QA file>
```

`planned`, `commissioned`, and `deferred` form the queue. `read` and
`answered-local` are resolved. A `consumer trace` is audit history, never a
second Q-consumer source of truth.

There is no live top-level `1-probes/`. A migrated paper may preserve it only
under `0-lifecycle/_archive/1-probes/`.

## Commands

```text
/haipipe-paper probe "<question>"       raise a Q-consumer and route it to S03 or S04
/haipipe-paper probe                    inspect the nested entry queue
/haipipe-paper probe run                run the five-step loop over queued entries
/haipipe-paper probe run <topic-id>     run one topic, for example literature-1
```

All commands go through `haipipe-paper-probe`.

## The five-step loop

```text
① ORGANIZE   open one entry per Q-executor under the owning S03/S04 topic
② MATCH      read the bank's QA corpus and set route, bank, target, state
③ DISPATCH   send only the frozen q-executor block for unmatched work
④ POINT      bind target to the answering QA file
⑤ INTERPRET  copy into a-executor and update the parent topic register
```

The default rule is MATCH before DISPATCH. The paper never writes the bank and
never executes task or discovery work inline. See
`phase/1-probe/haipipe-paper-probe/ref/topic-entry-contract.md` for the exact
contract and `check-probe-cards.sh` for its deterministic verification.
