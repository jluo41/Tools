---
name: haipipe-page-evidence
description: >-
  The EVIDENCE phase of a Board Page and the WORKING half of its OUTLINE part:
  two machine-gated cycles, LAND (make every run the item table decided on, in
  the real tasks/ tree, and fill the lanes: citations in evidence/bibex/, cards
  in evidence/probe/ only for questions that leave the page, display units in
  evidence/display/) and EMBED (write the landed numbers into plan v<N+1>,
  never restructure it, and return to SHAPE). Never writes Content. Trigger:
  page evidence, EVIDENCE phase, land the run, make the run, embed the number,
  fold evidence, bind an answer, display intake, /haipipe-page-evidence.
metadata:
  version: "0.14.0"
  last_updated: "2026-09-01"
---

# /haipipe-page-evidence · LAND the runs, then EMBED the numbers

EVIDENCE changes what a Page can safely know. It does not decide the argument
and does not write a sentence of `## Content`.

```text
OUTLINE part
  SHAPE    outline    brief → propose → react → revise      👤 approved:
  SURVEY   outline    the item table: Need · Route · Run     👤 Decide, per row
  LAND     this file  make the runs, fill the lanes          ⚙ every make-row landed
  EMBED    this file  fold the numbers into plan v<N+1>      ⚙ back to SHAPE
```

Load contracts in this order:

```text
haipipe-page
  → matching Page Type
  → haipipe-page-evidence
  → haipipe-plugin-outline/ref/item-table.md   the table this phase executes
  → the lane plugin for each thing it lands (bibex · probe · display · value)
  → haipipe-task, for a row whose outcome is new-run / new-task / new-job / new-block
```

## ⚡ Phase card

```text
READS    target Page · the approved plan · outline/<stem>-items.md, every row
         decided · the runs the rows name · existing cards and units
WRITES   the project's tasks/ tree (a run config, a scaffolded task, executed
         results) · <page>/evidence/bibex/ · <page>/evidence/probe/ (outbound
         rows only) · <page>/evidence/display/ · the ` → <result>` append on a
         row's Run line (LAND) · plan v<N+1>'s Answered: / Drawn: lines (EMBED)
NEVER    target prose · purpose · Aims · the plan's heads, bullets or order ·
         a Decide · a Status word · row-level data or PHI into a page
EXITS    LAND: every ☑ make row is landed · EMBED: every landed row is folded,
         then SHAPE re-agrees the plan
HUMAN    supplies a citation and ticks verified: · accepts a display at CHECK ·
         nothing else; both cycles run unattended
```

## ⚖️ The law this phase executes · a run computes, the page interprets

Every evidence number is answered by a RUN at a real address in the project's
`tasks/` tree (block > job > task > run). The run carries NO interpretation,
which is exactly why any page may bind to it; the reading of a result is
written on the page, at EMBED, under the page's own stake. This generalizes
`haipipe-page-for-task`'s law ("every shown number names the run that produced
it, and a rerun reopens the page") to every page.

The neutrality wall this replaces stripped questions because a language answer
can be bent by the asker. A run cannot: it is deterministic, its config is
diffable, and rerunning it is the audit. So a card with a stripped question
exists only for the rows that still cross to someone else's hands.

## 🟢 LAND · make what the table decided, where it belongs

One pass per decided table; the rows run in parallel where their inputs allow.

```text
outcome       what LAND does                                         landed when
────────────────────────────────────────────────────────────────────────────────────
found         nothing to make: append ` → <result file>` to the row   the file exists
rerun         execute the named run again (/haipipe-task, its runs/)  fresh results/ on disk
new-run       mint one r<NN>_ config in the named task, execute it    results/ on disk
new-task      scaffold t<NN> in the named job (/haipipe-task), then   as new-run
new-job       scaffold j<NN> in the named block, then a task and run  as new-run
new-block     scaffold b<NN>, then down the tree                      as new-run
person        transcribe what the person supplied, verbatim           the entry is in the lane
none          nothing: the row is SHAPE's, LAND skips it              never
```

- **Runs go into the REAL upstream folders**, never a page-side shadow. A
  page-serving computation that belongs to no upstream task is a `new-task`
  under the block that owns the data, named by the stranger test. The
  scaffold, the config grammar and the execution are `/haipipe-task`'s (the
  `runs/` door, `results/` regenerable, simple-code law); this phase names the
  address and presses the door.
- **LAND refuses a `☐` row.** A row with no signed Decide is SURVEY's; a
  machine that makes it anyway has passed a person's gate.
- **The row's Run line gains the arrow, nothing else.** ` → <result file>` is
  the one write LAND makes into the table, repo-relative, the exact file that
  holds the number. Status is never typed; `cli/evidence-status.py` derives
  `landed` from that file's existence.
- **The arrow points where the results ACTUALLY are.** A task's outputs live
  in its own `results/` or in the resolved result store its runner names
  (`result_store:` in the run's config, the `RESULT_STORE` root of
  `haipipe-task/ref/run-sh-template.sh`; the CMS report store under
  `_WorkSpace/0-CMS-Store/` is one). LAND resolves that root and writes the
  real path; it never assumes the file sits inside the task folder.
- **Aggregate only, never rows.** A result that lands here is a table, a log
  line, a summary: nothing row-level, no identifiers, no PHI. The CMS store's
  rule (results/ never PHI) is this phase's rule too.

### 🚪 When a card is still raised · a question leaves the page

A `new-*` row whose computation someone ELSE runs (the secure server, another
person's job, a discovery sweep once that tree joins) becomes a card at
`<page>/evidence/probe/PP<NN>-<slug>/` (`haipipe-plugin-probe`: card.md ·
consumer/ · executor/ · proof/). The wall survives here and only here:

- `consumer/q-consumer.md` holds the stake (page id, claim, why it matters,
  what breaks); `executor/q-executor.md` is the neutral question and is THE
  ONLY THING DISPATCHED; the payload may name card id, route and return
  address, never the stake.
- **One door out, and it is an agent**: hand the batch to
  `haipipe-probe-q-executor-agent`. A phase never calls a task or discovery
  orchestrator itself (JL 260820: 永远只有 haipipe-probe-q-executor-agent 才能够做这件事).
- The card's `serves:` names the row's address; the row's Run line names the
  card in its note. When the answer returns, `proof/` holds the aggregate
  extract, the value gets its `PP<NN>.v<n>` address (`haipipe-plugin-probe`
  §🧮), and the row gains its arrow.
- A `found` or `person` row never mints a card. The table IS its record.

### 📚 The citation lane

Load `haipipe-plugin-bibex`. A machine may subset the sealed bank or
transcribe a real record a person supplied; it never composes one from memory.
`verified` is the person's tick; LAND reports it missing and may not tick it.
If the outline's claim and the source disagree, preserve the source and route
the row back to SHAPE. Do not bend the citation to the claim. Citations are
`person` rows until the discoveries/ tree joins the run grammar.

### 🖼 The display lane

Load `haipipe-plugin-display` and the renderer named by the unit. LAND owns the
material and the drawing, not the prose that discusses it:

```text
① INTAKE   freeze the source material into intake/ (from the row's landed result)
② RENDER   named renderer writes its recipe/candidates
③ PICK     record the selected candidate when the plugin calls for one
④ BUILD    create assets, float source, and preview.pdf
⑤ ACCEPT   human gate at CHECK; never ticked here
```

The unit's recipe IS a run, and its inputs come from runs, so the law holds
twice. A folder without intake is not evidence; frozen intake without a
preview is a HOLD. One `haipipe-display-unit-agent` per 🖼 row, dispatched by
the caller, each owning one folder.

## 📌 EMBED · write the number into the plan, and only the number

One pass per landed table, and it is the OUTLINE part's merge point: every
return converges on the ONE plan file, so EMBED never fans out.

- **Reads each `landed` row's result file and writes the plan's fold lines**:
  a value becomes `Answered: <number> · <PP<NN>.v<n> or the result path>` on
  the bullet that asked; a built unit's README claim becomes `Drawn:`; a
  served Round row `Routed:`. These append under the bullet; they never edit
  its head or Note.
- **The interpretation is written here, page-side**: what the number means
  for THIS bullet, one clause on the `Answered:` line or in the bullet's Note
  as `v<N+1>`. The run never said it; the page says it under its own stake.
- **EMBED fills, never restructures.** It may not add, remove or reorder a
  bullet, a paragraph or a division, and may not change a head. A landed
  answer that breaks a bullet's claim is a ROUTE, not an edit: EMBED stops,
  writes the conflict as a `D<nn>` thread, and routes to SHAPE, where the
  structural pen lives.
- **The result is plan v<N+1>, `approved: ⬜`**, `supersedes: v<N>`; v<N> is
  kept. A tick belongs to the version it ticked.
- **It always returns to SHAPE.** The person re-reads the embedded plan and
  ticks; the tick carries the fork (every row `folded` → the DRAFT part; fresh
  marks → SURVEY). A machine never decides that the part is over.
- **`stale` reopens.** A rerun upstream that changes a result newer than the
  plan flips the row's derived Status to `stale`; the next EMBED re-folds it,
  and a page already drafted routes back here from CHECK.

## 🔀 Exit and routing

```text
LAND   every ☑ make row landed                        → EMBED
LAND   a row's run cannot be made (data absent,        → HOLD, naming the row; or
       server not reachable, PHI would move)              SHAPE if the bullet is wrong
LAND   an outbound card still unanswered               → LAND again (waiting)
EMBED  every landed row folded                         → SHAPE (plan v<N+1>)
EMBED  a landed answer breaks a bullet's claim         → SHAPE with the D<nn> named
```

EVIDENCE never routes to the DRAFT part. The plan absorbs the numbers and a
person re-agrees it before prose begins.

## 📖 Read economy

Read fully only the target Page, the approved plan, the item table and the
result files the rows name. Trust unchanged rows except for one spot check.
Scope checker output to the target Page and keep build logs out of the
reasoning context.

## 🧾 RUN receipt

When called by RUN, follow `../haipipe-page-workflow/ref/page-run-contract.md`
and add:

```text
phase:        EVIDENCE
cycle:        LAND | EMBED
rows:         n decided · n made (by outcome) · n landed · n still owed
runs:         one row per run made or executed: address · results path
cards:        one row per outbound card raised or answered (PP id · serves · state)
values:       PP<NN>.v<n> bindings created or revalidated
renderers:    display unit → renderer → preview path
folded:       n rows written into plan v<N+1> (EMBED)
human_gates:  verified / accepted states, never synthesized
limits:       rows that could not be made, and why
route:        EMBED | SHAPE | LAND | HOLD
reopens:      true when a landed answer changes purpose, Aim, or shape
```

The Page source hash may remain unchanged because EVIDENCE writes plugin
surfaces, the tasks/ tree and the plan, never the page. The receipt must still
name every artifact it landed.

> Since 260831 the lanes live under the page's category folder (`evidence/`,
> haipipe-page §📁); a flat lane name on an unmigrated page, or a flat SYMLINK
> STUB on a migrated one, is the same lane during the migration.
