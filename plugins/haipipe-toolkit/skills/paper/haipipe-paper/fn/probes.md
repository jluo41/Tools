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

The shared crossing model (stake stripping, the wall, the QA state-line
contract, the two LAWS, derived states) is owned by `probe/haipipe-probe/SKILL.md`;
the page-phase contract is `board/page-phases/haipipe-board-page-probe`. This
file holds only how a PAPER runs the loop, plus the paper-side deltas.

## Runtime layout

```text
0-lifecycle/
├── S03-literature/
│   ├── S-Literature-<n>-<topic>.md
│   └── probes/L<nn>-<topic>/<n>-<slug>.md
└── S04-value/
    ├── S-Value-<n>-<topic>.md
    └── probes/V<nn>-<topic>/<n>-<slug>.md
```

An entry is a probe QA (the entry record): a hidden source record, not a board
page (JL ruling B, 260806). Its digit-first `<n>-<slug>.md` name, `<n>`
restarting at 1 per drawer, keeps it out of the board's page sweep, so the
board renders the topic page only. One conversation, two QAs: the bank QA is
the original, the probe QA is the paper's copy that points at it.

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

All commands go through the door's PROBE step; the stages never touch the bank
themselves.

## The five-step loop

```text
① ORGANIZE   open one entry per Q-executor under the owning S03/S04 topic
② MATCH      read the bank's QA corpus and set route, bank, target, state
③ DISPATCH   send only the frozen q-executor block for unmatched work
④ POINT      bind target to the answering QA file
⑤ INTERPRET  copy into a-executor and update the parent topic register
```

The default rule is MATCH before DISPATCH. The paper never writes the bank and
never executes task or discovery work inline.

### ② MATCH mechanics (the paper-side deltas)

- Resolve `project_root` by walking UP from the paper root to the first
  ancestor containing `discoveries/`. Do NOT use `git rev-parse`: a repo-backed
  paper is its own git repo.
- MATCH runs over the bank's READABLE QA corpus (`{tasks,discoveries}/**/QA/*.md`)
  and matches ON THE ANSWER, never on the topic. A hit is `bank: reuse` with the
  entry's `target` pointed at that QA file; nothing runs. Most entries SHOULD
  land on `reuse`.
- Route on the TARGET, not on the verdict: `bank` says what the bank would have
  to DO, `target` says whether the readable answer EXISTS yet.

```text
target: <an existing QA path>   → ④/⑤ : verify the state line, then harvest
target: NEW <path>              → ③   : dispatch only for bank: run | code | new
```

- T1 LOCAL is MATCH's own shortcut: root the question against the paper's OWN
  registries and close it `answered-local`. The closed whitelist: entries
  already `read` or `answered-local` beneath `S03-literature/probes/` or
  `S04-value/probes/` · `displays/` units · the `.bib` · the stage's S page
  `## Log`. Adopt the POINTER, never the verdict (a reused value re-verifies
  against its ORIGINAL source at PLACE).
- DISPLAY-shaped needs are REROUTED, not collected: they become a DR row in
  `0-lifecycle/S05-display/_DISPLAY_REQUEST.md` and the entry closes
  `answered-local` with "rerouted to display stage: DRNN".

### The depth ceiling (before any ③)

Read `probe_depth:` from the stage's `stage.md`, or the value the invocation
passed as `probe --depth N`, whichever is HIGHER. Map each entry's `bank`
verdict onto the bank's own ladder, then compare:

```text
bank: reuse  = depth 0   results already answer it       free, nothing runs
bank: run    = depth 1   old script, new config          costs
bank: code   = depth 2   must write new code first       costs
bank: new    = depth 3   open a new task-folder          costs most

    depth(bank) <= probe_depth   →  ③ DISPATCH it
    depth(bank) >  probe_depth   →  DEFER it, and STOP for that entry
```

Deferring is a correct outcome, not a failure; declare it on the entry as
`**state**: deferred` plus a `**deferred**: depth-<n> · <reason>` line, never
as silence. The `--depth` spend-authority rule itself lives in the door
(`../SKILL.md`, "The PROBE ceiling"): never raise the ceiling on your own
initiative.

### ③ DISPATCH goes through the collector

Hand the still-collecting SET to `Agent(haipipe-probe-q-executor-agent)` with
`project_root`, the probe QAs, and each one's PROBE-authored `route`
(task|discovery, AUTHORITATIVE). The agent's clean context IS the wall: it
sends each `q-executor` VERBATIM to the task or discovery orchestrator agent
and returns `{ entry → target: QA-path | in-flight | failed }`. A stage or the
door calling an orchestrator agent inline bypasses this contract; results
would land nowhere reviewable.

### ④ POINT is verified on disk

Do not trust the return blind: `ls` the target and `grep '^- state:' <target>`.
`answered` → harvest; `working` → stays `commissioned` (report in progress);
no path → `failed`. A `commissioned` target that has since gone `answered` is
harvested now, not at its eta.

### ⑤ INTERPRET and harvest (inline)

- Copy the QA answer into `#### a-executor`, then update the parent topic's
  Q-consumer register with its paper-facing interpretation and the entry path.
- The AUTHOR writes a claim's status (supported | refuted | inconclusive +
  confidence + claim_type) into the owning S02 claims page, never in the probe
  file. A resource-serving entry writes its reading back as the Q's `A:` on the
  resource page (existence AND fitness AND what it KILLS).
- Harvested values carry a FABRICATION GUARD: the literal value string must
  grep in its named source file (`grep -F '<value>' <source>`); a value with no
  source hit is REJECTED.
- Source anchors are transcribed in the QA file's own words; NEVER generate
  bibtex, NEVER touch `.bib`. Display links only for units that EXIST or whose
  DR row is `done`.
- Placing anything INTO manuscript prose is REVISE's job
  (`../../S06-main/section-edit/revise-place-craft.md`), not PROBE's.

### VERIFY

```sh
sh paper/haipipe-paper/probe/check-probe-cards.sh <paper_root> [--stage <key>]
```

The FAIL codes are probe's. Never report a green PROBE over a FAIL.

## Reference

```text
probe/haipipe-probe/SKILL.md         the shared model. Read it first.
probe/topic-entry-contract.md        the paper-specific S03/S04 entry shape (this door's probe/ folder)
probe/per-stage-dispatch.md          per-stage routing · seed/claims/resource specifics
probe/check-probe-cards.sh           the VERIFY / stage-gate checker (family-local)
```
