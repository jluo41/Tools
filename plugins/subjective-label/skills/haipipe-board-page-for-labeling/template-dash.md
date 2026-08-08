<!-- TEMPLATE · THE CONTROL PAGE. ONE PER BOARD, NOT ONE PER RUN.
     Copy this file to `<board>/<group-folder>/S-Label-Dash.md`, fill it, and DELETE each RULE
     comment as you satisfy it.

     WHAT THIS FILE IS. The specimen for the `Label` family's inventory page. The run pages
     have their own specimen, `template.md`. Two kinds, two specimens.

     WHAT A CONTROL PAGE IS. The page that answers what no run page can: which runs exist at
     all. No stage writes it, and it is not a run page that went missing. It is hand-maintained:
     added to when a run opens, edited when a run's blocking gate changes.

     ⚠️ IT NEVER CLOSES. An inventory has nothing to finish, so it carries no ✅ at page level
     and is not counted as a settled page.

     ⚠️ IT STILL NEEDS `## Stage Contract`. The checker requires that section on EVERY S page
     and reports `missing-stage-section` without it, even though a control page has no upstream.
     Say so explicitly rather than leaving it out.
-->

# S Label Dash · which runs exist, and where each one stands

state: 🔴 OPEN
page-type: labeling
owner: <who maintains the roster>

<!-- RULE · `page-type:` is REQUIRED and it is not decoration. The 🔌 Plugin menu's
     🏷 Labeling entry gates on it, so a page that omits the key gets no labeling
     surface however labeling-shaped its filename is. The key beats the filename. -->
method: inventory the runs and their blocking gate; no stage writes this page

provides: the roster a reader checks before opening any single run

<!-- RULE · no `requires:` and no `style-from:`. A control page reads the run pages beside it
     and nothing upstream. Declaring a dependency here would invent one. -->

## Stage Contract

<!-- RULE · you MAY write `### Required Inputs` here, and on a RUN page you may not. The
     difference is `requires:`. `stage.py sync` generates the managed block only for a page
     that declares dependencies, and this page declares none, so nothing will ever be
     generated here to collide with. Do not carry this permission over to `template.md`. -->

### Required Inputs

**None, by design.** A control page inventories a family, and no stage produces an inventory, so this page declares no `requires:` and no `style-from:`. It reads the run pages on this board and nothing else.

### Provides

The roster: one row per run, each naming the single thing that run is blocked on.

## Opening

<the lead question: which runs are open, and what is stopping each one?>
<what a run is, in one clause.>
<why no single run page can answer this.>
<what this page therefore is, and that it holds no method and no judgment.>

**Where this page sits**: it is the control page of the `Label` family, so every run page is one row here.

**More details**: <what a control page is: no stage writes it, and it is not a run that went missing.>

**Why it matters**: <a run nobody remembers is a corpus labeled twice; a blocking gate nobody sees is a person waiting to be asked.>

## Diagram

**The roster**: one row per run, with the gate that is stopping it.

```text
🗂 S-Label-Dash
│
└── <n> · <corpus> × <target>                     <state>
      corpus  <size>
      seal    <which split or sample, read or unread>
      rounds  <n> closed
      blocked <the one thing>
```

## Content

### 1 · The runs

**One row per run**: what it labels, and the one thing stopping it.

```text
run                    target        rounds   blocked on
────────────────────────────────────────────────────────────
<n> · <slug>           <target>      <n>      <the one thing>
```

<!-- RULE · record lines, never a markdown table. Adding a run adds one line. -->

#### 1.1 · What a row may say, and what it may not
(Keeps the inventory from becoming a second copy of each run's state.)
<A row carries id, target, rounds closed, and the single blocking thing.>
<It never carries gate readings, policy version, or rules: those live on the run page and a copy here goes stale the first time a round closes.>
<When a reader needs more than the row, the row's job is done: they open the run.>

#### 1.2 · Why this page is not written by a stage
(A control page inventories a family, and no stage produces an inventory.)
<Every run page is produced by running the loop; this page is produced by there being runs at all.>
<It is hand-maintained, and it never closes.>

## Aims

<!-- RULE · a control page's Aims are about the ROSTER's completeness, never about any run's
     progress. An Aim that tracks a run's gate belongs on that run's page. -->

### A1 · 🗂 The runs
- A1.1 · Every open run has exactly one row here.
  **Done when:** the row count equals the number of run pages on this board.
- A1.2 · Every row names one thing the run is blocked on, or says it is not blocked.
  **Done when:** no row's blocked column is empty while its run is not closed.

## States

### A1 · 🗂 The runs
- ⬜ A1.1 · <what is true now>
- ⬜ A1.2 · <what is true now>

<!-- RULE · state emoji FIRST, then the Aim id: `- ✅ A1.1 · Met. <evidence>`. -->

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · ALL` · [S-Label-<n> page](<group>/S-Label-<n>-<corpus>-<target>.md)
  <one line: what that run supplies to the row above.>

<!-- RULE · one row per run page. These are all on THIS board, so unlike a run page's method
     references, they belong here. -->

## Law

- 🗂 **A row names the blocking gate, never the gate readings.** The readings live on the run page, and a second copy here goes stale the first time a round closes.
- 🚫 **This page never closes.** An inventory has nothing to finish, so it carries no ✅ and is not counted as a settled page.

## Log

<YYMMDD> · <what changed>
