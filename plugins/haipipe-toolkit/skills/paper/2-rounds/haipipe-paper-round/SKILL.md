---
name: haipipe-paper-round
description: "Manage the paper's 1-rounds/ working-memory layer: dated work rounds holding discussion, decisions, todo, and applied logs. Subcommands enter|new|triage|apply|close open or resume a round, start a dated vYYMMDD round, turn discussion/review into routed todo items, record applied backfills, and close the round. Use for paper round, work round, round todo, decisions, applied, latest round, open a round, triage review, 2-rounds."
argument-hint: "[enter|new|triage|apply|close] [paper-dir] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-06-22"
  summary: "Rounds layer: enter/new/triage/apply/close over 1-rounds/vYYMMDD/."
---

Skill: haipipe-paper-round
==========================

Manage `1-rounds/`, the paper's working-memory layer. A round is a dated cycle
of author/agent discussion, coauthor or reviewer comments, decisions, todo
items, and what was applied. The contract is in `../../ref/paper-rounds.md`.

Use `round`, not `feedback`: the contents are broader than external feedback.

Read first: `../../PHILOSOPHY.md`, `../../ref/paper-rounds.md`,
`../../ref/lifecycle-map.md`.

Folder contract
---------------

```text
1-rounds/
├── latest.md            active-round pointer
└── vYYMMDD/
    ├── README.md        round header: source, date, purpose, maturity, status
    ├── discussion.md    raw discussion / review text / meeting notes
    ├── decisions.md     decisions accepted as paper intent
    ├── todo.md          open needs, edits, probes, displays, citations
    └── applied.md       backfill log: what changed where
```

The round id is the date, `vYYMMDD` (e.g. `v260621`). Do not nest a branch level
above it.

Subcommands
-----------

```text
/haipipe-paper round enter [paper-dir]    open/resume the active round; show open todo
/haipipe-paper round new [paper-dir]      start a dated vYYMMDD round; point latest.md at it
/haipipe-paper round triage [paper-dir]   discussion -> decisions + routed todo
/haipipe-paper round apply [paper-dir]    route/execute todo; record applied backfills
/haipipe-paper round close [paper-dir]    mark the round closed; update latest.md
```

### enter

Read `1-rounds/latest.md`, then the active round's README/discussion/decisions/
todo/applied. Render the round panel: source, status, and unresolved todo with
their targets. Read-only. Defer the broader paper dashboard to the Paper Console
(`haipipe-paper-enter`).

### new

Create `1-rounds/vYYMMDD/` with the five contract files (README header plus
discussion/decisions/todo/applied stubs). Point `1-rounds/latest.md` at it. Ask
for the round source/purpose if not given. Do not pre-create rebuttal/submission
subtrees; `haipipe-paper-rebuttal` adds those for external-review rounds.

### triage

Read `discussion.md` (raw review/meeting text). Extract decisions into
`decisions.md` and open needs into `todo.md`. Every todo item points to one
target, per `../../ref/paper-rounds.md`:

```text
claim unsupported / too strong   -> 0-lifecycle/2-claims or probe
display missing / stale          -> 0-lifecycle/4-figures-tables or display task
paragraph placement unclear      -> 0-lifecycle/5-minimap
wording / flow / style           -> 0-sections/*.tex or edit skill
citation needed / wrong          -> discover or citation component
reviewer response                -> respond/rebuttal skill
```

### apply

For each todo item, route to its target stage or evidence worker (Skill/Task),
or apply it directly when low-risk. Record each change in `applied.md` as a
backfill log (what changed, where, which todo it closes). Gate costly or
claim-committing actions per the copilot policy.

### close

Mark the round `status: closed` in its README, summarize what was applied and
what carried over, and update `latest.md` (point to a new active round or
`none`). Carry unresolved todo items into the next round.

Routing
-------

```text
1. First token in {enter,new,triage,apply,close} -> that subcommand.
2. Else if an active round exists                  -> enter.
3. Else                                            -> new.
```

Return Contract
---------------

```text
status:    ok | blocked | failed
summary:   1-3 sentences
artifacts: [round files read/written]
next:      suggested next command (often a lifecycle stage or evidence worker)
```
