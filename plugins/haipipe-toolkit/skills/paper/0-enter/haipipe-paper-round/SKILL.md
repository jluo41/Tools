---
name: haipipe-paper-round
description: "Manage the paper's 1-rounds/ working-memory layer: dated work rounds holding discussion, decisions, todo, and applied logs. Subcommands enter|new|triage|apply|close open or resume a round, start a dated vYYMMDD round, turn discussion/review into routed todo items, record applied backfills, and close the round. Use for paper round, work round, round todo, decisions, applied, latest round, open a round, triage review, 2-rounds."
argument-hint: "[enter|new|triage|apply|close] [paper-dir] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.1"
  last_updated: "2026-07-19"
  summary: "Rounds layer: enter/new/triage/apply/close over 1-rounds/vYYMMDD/. Owns the 1-rounds/ contract — folder shape, file semantics, round lifecycle, triage targets, dashboard rule. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-round
==========================

Manage `1-rounds/`, the paper's working-memory layer.
A round is a dated cycle of author/agent discussion, coauthor or reviewer comments, decisions, todo items, and what was applied.
This skill OWNS the `1-rounds/` contract — the Rounds contract section below is its single source of truth.

Use `round`, not `feedback`: the contents are broader than external feedback.

Read first: `../../PHILOSOPHY.md`, `../../1-lifecycle/ref/04-lifecycle-map.md`.

Rounds contract
---------------

`1-rounds/` is the paper working-memory layer. It stores dated work rounds: author/agent
discussions, coauthor comments, reviewer comments, decisions, todo items, and what was
applied.

### Folder contract

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

The round id is the date, `vYYMMDD` (e.g. `v260621`).
The round id is the branch/round name — do not nest another branch level above it:

```text
good: 1-rounds/v260621/
bad:  1-rounds/<branch-name>/v260621/
```

### File semantics

| File | Purpose |
|---|---|
| `latest.md` | Points to the active round id and optional summary |
| `README.md` | Round header: source, date, purpose, maturity, status |
| `discussion.md` | Raw discussion / review text / meeting notes |
| `decisions.md` | Decisions accepted as paper intent |
| `todo.md` | Open needs, edits, probes, displays, citations |
| `applied.md` | Backfill log: what changed where |

### Round lifecycle

```text
open round
  -> collect discussion
  -> extract decisions
  -> triage todo/open needs
  -> route each item to lifecycle/evidence worker
  -> record applied backfills
  -> close or keep active
```

### Triage targets

Every `todo.md` item should point to one target:

| Todo type | Target |
|---|---|
| claim unsupported / too strong | `0-lifecycle/1b-claims` or probe |
| display missing / stale | `0-lifecycle/4-display` or display task |
| paragraph placement unclear | `0-lifecycle/5-section-edit` |
| wording / flow / style | `0-sections/*.tex` or edit skill |
| citation needed / wrong citation | discover or citation component |
| reviewer response | respond/rebuttal skill |

### Dashboard rule

`/haipipe-paper enter` must surface open round items alongside lifecycle status.
Round todo items are first-class open needs, not afterthoughts.

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

Read `1-rounds/latest.md`, then the active round's README/discussion/decisions/todo/applied.
Render the round panel: source, status, and unresolved todo with their targets.
Read-only.
Defer the broader paper dashboard to the Paper Console (`haipipe-paper-enter`).

### new

Create `1-rounds/vYYMMDD/` with the five contract files (README header plus discussion/decisions/todo/applied stubs).
Point `1-rounds/latest.md` at it.
Ask for the round source/purpose if not given.
Do not pre-create rebuttal/submission subtrees; `haipipe-paper-rebuttal` adds those for external-review rounds.

### triage

Read `discussion.md` (raw review/meeting text).
Extract decisions into `decisions.md` and open needs into `todo.md`.
Every todo item points to one target, per the Triage targets table in the Rounds contract above.

### apply

For each todo item, route to its target stage or evidence worker (Skill/Task), or apply it directly when low-risk.
Record each change in `applied.md` as a backfill log (what changed, where, which todo it closes).
Gate costly or claim-committing actions per the copilot policy.

### close

Mark the round `status: closed` in its README, summarize what was applied and what carried over, and update `latest.md` (point to a new active round or `none`).
Carry unresolved todo items into the next round.

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
