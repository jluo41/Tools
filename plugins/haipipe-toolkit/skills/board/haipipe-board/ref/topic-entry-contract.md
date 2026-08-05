# Topic page and nested entry contract

Use this optional overlay when a Board has one reader-facing topic page and several neutral requests to run beneath it.
The contract is generic. It names neither a Paper stage nor an evidence bank.

```text
S topic page                        the ONE board page this overlay adds
  ├── ### Q-consumer register     canonical reader-facing need and stake
  └── probes/<topic>/
       └── one probe QA = one q-executor           <n>-<slug>.md · not a page
            ├── consumer trace    audit copy of the Q-consumer
            ├── bank binding      route, bank, target, and state
            └── a-executor        the returned answer
```

An originating delivery page may raise a Q first. The topic page owns its canonical evidence-routing record, while the probe QA owns the q-executor because it is the neutral question another system can answer. The consumer trace is never a second register.

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

A row in none of these states holds the topic open. The topic's human gate reads the register, not the probe QAs: an answer sitting in a probe QA's `#### a-executor` that never became a register record does not close its row.

## The probe QA: a record, not a Page

The nested file is a probe QA (the entry record; "entry" survives only as an informal alias). It is a RECORD, not a board Page (JL ruling B, 260806): "an entry is a source file the topic page points at, like a PDF; the board renders the topic page, never the entry."

The twin naming law (JL, 260806): one conversation, two QAs: the bank QA is the original, the probe QA is the paper's copy that points at it. The bank QA lives in the executor's own tree (its `# Q` is the q-executor, its `## Answer` the a-executor); the probe QA lives below the topic page and binds to the bank QA by the `**target**:` path. The file-level names "QA-executor" and "QA-consumer" are WRONG and retired: consumer and executor name SLOTS only, Q-consumer and A-consumer on the register row, q-executor and a-executor inside either QA, never a file.

The naming law on disk: a probe QA is named `<n>-<slug>.md`, digit first, inside its topic's `probes/<topic>/` folder, and `<n>` restarts at 1 per folder. The digit-first name IS the hiding mechanism, not a style choice: the Board engine's page sweep (`page_files` in `src/common.py`) discovers pages only by the filename prefixes `Q`, `S`, `Agent`, and `Meeting`, so a digit-first file is never swept onto the board, never listed in `## Pages`, and never rendered. Do not "fix" a missing probe QA by giving it a page-shaped name.

A probe QA carries no page frame: no `state:` header, no Opening, no Aims, no States, no Log, and no gate; the topic page carries all of those on its behalf. The record is a `# title` line, a `requires: <topic-page-id>` line naming the one topic page whose register raised it, and exactly one each of the four slots:

```markdown
#### q-executor
#### consumer trace
#### bank binding
**route**: task | discovery
**bank**: reuse | run | code | new
**target**: <path to the answering bank QA file>
**state**: planned | commissioned | deferred | read | answered-local
#### a-executor
```

Queue membership is derived, not maintained in another file. `planned`, `commissioned`, and `deferred` are queued. `read` and `answered-local` are resolved.

`cli/check.py` detects this overlay only when an S page declares `### Q-consumer register`. It then checks each probe QA's direct-topic dependency, slot anatomy, bank state, and whether each trace id occurs in its parent register.
