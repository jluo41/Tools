# Paper Rounds

`1-rounds/` is the paper working-memory layer. It stores dated work rounds:
author/agent discussions, coauthor comments, reviewer comments, decisions,
todo items, and what was applied.

Use `round`, not `feedback`, because the contents are broader than external
feedback.

## Folder Contract

```text
1-rounds/
├── latest.md
└── v260621/
    ├── README.md
    ├── discussion.md
    ├── decisions.md
    ├── todo.md
    └── applied.md
```

The round id is the branch/round name. Do not nest another branch level:

```text
good: 1-rounds/v260621/
bad:  1-rounds/<branch-name>/v260621/
```

## File Semantics

| File | Purpose |
|---|---|
| `latest.md` | Points to the active round id and optional summary |
| `README.md` | Round header: source, date, purpose, maturity, status |
| `discussion.md` | Raw discussion / review text / meeting notes |
| `decisions.md` | Decisions accepted as paper intent |
| `todo.md` | Open needs, edits, probes, displays, citations |
| `applied.md` | Backfill log: what changed where |

## Round Lifecycle

```text
open round
  -> collect discussion
  -> extract decisions
  -> triage todo/open needs
  -> route each item to lifecycle/evidence worker
  -> record applied backfills
  -> close or keep active
```

## Triage Targets

Every `todo.md` item should point to one target:

| Todo type | Target |
|---|---|
| claim unsupported / too strong | `0-lifecycle/2-claims` or probe |
| display missing / stale | `0-lifecycle/4-display` or display task |
| paragraph placement unclear | `0-lifecycle/5-minimap` |
| wording / flow / style | `0-sections/*.tex` or edit skill |
| citation needed / wrong citation | discover or citation component |
| reviewer response | respond/rebuttal skill |

## Dashboard Rule

`/haipipe-paper enter` must surface open round items alongside lifecycle
status. Round todo items are first-class open needs, not afterthoughts.
