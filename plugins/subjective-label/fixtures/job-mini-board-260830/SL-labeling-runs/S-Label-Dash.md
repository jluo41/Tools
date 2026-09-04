# S Label Dash · the run roster

state: 🔴 OPEN
page-type: labeling
owner: CC
method: inventory the runs and their blocking gate; no stage writes this page

provides: the roster a reader checks before opening any single run

## Stage Contract

### Required Inputs

**None, by design.** A control page inventories a family, and no stage produces an inventory, so this page declares no `requires:` and no `style-from:`. It reads the run pages on this board and nothing else.

### Provides

The roster: one row per run, each naming the single thing that run is blocked on.

## Opening

Which runs are open on this fixture board, and what is stopping each one?
A run is one corpus paired with one label target; here there is exactly one, the 30-item mock corpus paired with `empathy`.
No single run page can say how many runs exist, so this page is the inventory, and it holds no method and no judgment.
It exists on this board so the control-page kind is exercised beside the run kind.

**Where this page sits**: it is the control page of the `Label` family, so every run page is one row here.

**More details**: no stage writes a control page, and it is not a run that went missing. It is hand-maintained: added to when a run opens, edited when a run's blocking gate changes, and it never closes.

**Why it matters**: a run nobody remembers is a corpus labeled twice; a blocking gate nobody sees is a person waiting to be asked. On a one-run fixture the row still proves the roster shape.

## Diagram

**The roster**: one row per run, with the gate that is stopping it.

```text
🗂 S-Label-Dash
│
└── 1 · job-mini × empathy                        🟡 PARTIAL
      corpus  30 mock reviews (24 development, 6 sealed)
      seal    6 reserved ids, unread
      rounds  2 closed
      blocked quality 0.78 < 0.80, and register cell LN still open
```

## Content

### 1 · The runs

**One row per run**: what it labels, and the one thing stopping it.

```text
run                        target     rounds   blocked on
──────────────────────────────────────────────────────────────
1 · job-mini-empathy       empathy    2        quality below floor · LN open
```

#### 1.1 · What a row may say, and what it may not
(Keeps the inventory from becoming a second copy of each run's state.)
A row carries id, target, rounds closed, and the single blocking thing.
It never carries gate readings, policy version, or rules: those live on the run page, and a copy here goes stale the first time a round closes.
When a reader needs more than the row, the row's job is done: they open the run.

#### 1.2 · Why this page is not written by a stage
(A control page inventories a family, and no stage produces an inventory.)
Every run page is produced by running the loop; this page is produced by there being runs at all.
It is hand-maintained, and it never closes.

## Aims

### A1 · 🗂 The runs
- A1.1 · Every open run has exactly one row here.
  **Done when:** the row count equals the number of run pages on this board.
- A1.2 · Every row names one thing the run is blocked on, or says it is not blocked.
  **Done when:** no row's blocked column is empty while its run is not closed.

## States

### A1 · 🗂 The runs
- ✅ A1.1 · Met. One run page exists (`S-Label-1-job-mini-empathy`) and it has one row above.
- ✅ A1.2 · Met. The row names its block: quality 0.78 below the 0.80 floor, register cell LN open.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [S-Label-1 page](SL-labeling-runs/S-Label-1-job-mini-empathy.md)
  The run supplies its state line and its one blocking gate to the row above.

## Law

- 🗂 **A row names the blocking gate, never the gate readings.** The readings live on the run page, and a second copy here goes stale the first time a round closes.
- 🚫 **This page never closes.** An inventory has nothing to finish, so it carries no ✅ and is not counted as a settled page.

## Log

260830 · Page created beside the job-mini fixture; one row, blocked on quality and LN coverage.
