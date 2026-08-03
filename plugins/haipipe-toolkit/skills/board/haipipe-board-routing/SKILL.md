---
name: haipipe-board-routing
description: >-
  The WRITE verb of the board family, at BOTH altitudes. Page altitude: take ONE input (a decision made in chat, a finding, a correction, a status change) and land it on the board, by finding the owning page and section and appending an anchored write; it loads the page and sentence specs, reads board.md's ## Pages as the only registry, and proposes rather than creates when nothing fits. Board and group altitude (absorbed from haipipe-board-index on 260802): propose a board's structure with the human before any file exists, materialize it after approval, keep each group's engine-pages-folder lane block current with src/lanes.py, and move pages when a group is renamed or split. It may update an Aim State from inspected evidence, and closes a Decision Now row the human has already answered while never ticking one nobody answered and never changing a page-level human gate. Use when work happened and the board must record it, and when the board's own structure is what changed: route this to the board, write it back, which page owns this, claim the question, board structure, page group, group map, lanes, regroup, propose a board. A DECISION is its most common input: the moment a ruling is made, or a question needs one, call this to find the owning page and write the row or the record, because a decision that stays in the session cannot be seen, carries no Blocks or Default, and leaves no trace of the options weighed. It does NOT render HTML: haipipe-board owns build, serve, page and sentence. Trigger: route, write back, owning page, land this on the board, update the log, we decided, you ruled, JL said, record this decision, add a Decision Now, needs a ruling, which page owns this, put this on the board, board structure, board index, page group, group map, lanes, regroup, /haipipe-board-routing.
metadata:
  version: "0.9.1"
  last_updated: "2026-08-03"
  summary: "Absorbs haipipe-board-index: one WRITE verb now owns both altitudes, so a group-altitude input finally has somewhere to land."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-routing · every write onto a board, at both altitudes

`haipipe-board`'s sync verb already states the order: claim which question first, then do the work, then write back in the same round.
Routing automates the claim (QC1b §4), which makes two existing failure modes machine-speed, so the rules here exist to keep them impossible rather than unlikely.

**The boundary:**

```
haipipe-board-routing            what it loads          what it never does
─────────────────────            ─────────────────      ─────────────────────
propose a board's structure      haipipe-board-page     render, serve, check
materialize it after approval    haipipe-board-sentence tick a human decision
find the owning location                                change a human page gate
append the anchored write                               create a page silently
keep each group's lane block                            materialize an
propose a page when none fits                             unapproved proposal
```

Digest (a session transcript, many inputs) is this verb FANNED OUT: it calls routing per input and never reimplements it.
Digest is not built yet; when it is, it runs in a fresh context for the same reason the cold read does.

## 🗂 Two altitudes, one verb (JL 260802)

Until 260802 the board altitude was a separate skill, `haipipe-board-index`, and this one wrote pages only.
JL merged them: "maybe merge, I will do B".
The merge is not tidying. It closes a gap this verb had carried since it shipped, because a finding about a WHOLE GROUP had no target and stayed in chat, while the block that finding belongs in was owned by the other unit.

```
🗂 BOARD + GROUP altitude          board.md and nothing else
   propose · materialize          the structure, before any page exists
   lanes · regroup                each group's engine · pages · folder block

✍️ PAGE altitude                   one page's .md
   the five-step route            one input → one owning page → one write

   both write MARKDOWN ONLY. haipipe-board renders, serves and checks.
```

The two altitudes keep separate approval rules, and that is the one thing the merge must not blur.
A page-altitude write lands on its own, because it records something that already happened.
A board-altitude write asks a person first, because it decides what pages will exist, and the group letters chosen there are cited by every future page: a rename later is a migration, not an edit.

## 🏗 The board altitude: propose, then materialize

### `propose` · before any file exists

Talk first, write nothing.
From a topic, propose and show:

```
1. spine        one sentence: what is being pinned down
2. close        what must be true for the board to be done
3. groups       3-7 of them, each a responsibility, not a phase
4. pages        the questions each group owns, with ids
5. connections  which group depends on which, and why
6. skills       which skill this board may change (optional)
```

Then **stop and get approval.** Nothing is materialized on a proposal.

### `materialize` · after approval

`board.md` (title, spine, close, `## Topic`, `## Pipeline`, `## Pages`, plus `## Board Structure` when the board must explain its source and webpage shape), one descriptive folder per group, one page file per listed page, then hand off to `haipipe-board` to build the generated `board/` site.

This is the same work `haipipe-board`'s `open` action describes to a person running a board by hand.
The door keeps that description because a person opening their first board should not have to load a second skill; this contract is what an agent loads when it does the work, and the two must be corrected together.

### `lanes` · refresh the per-group blocks

```bash
python3 <this-skill>/src/lanes.py <board-dir>            # dry run: what would change
python3 <this-skill>/src/lanes.py <board-dir> --apply    # write board.md
```

It ROUND-TRIPS.
The page roster is generated from `## Pages` so it can never disagree with the index, but every cell a person typed is kept:

```
· a row whose page still exists   → engine · name · folder all KEPT
· a page with no row yet          → arrives with `?`, which is the to-do list
· a row whose page is gone        → DROPPED
```

Same bargain as `xcal.py` keeping a human's frame position: the generator owns the skeleton, the person owns the meaning, so re-running is never destructive.
A page's `# ` title only SEEDS a new row's name; the column is 29 characters and a real title rarely fits it.

Kept cells are collected GLOBALLY, keyed by page id across the whole file rather than per block, so a page that changes group carries its typed cells with it instead of resetting to `?`.
`dropped` is judged against the whole roster for the same reason: after a regroup a page has merely moved, and only a page in no group is gone.

### `regroup` · move pages into one folder per group

Wraps `haipipe-board/cli/regroup.py`, which is the migration tool for any group rename or split:

```bash
python3 ../haipipe-board/cli/regroup.py <board-dir>            # plan
python3 ../haipipe-board/cli/regroup.py <board-dir> --apply    # git mv
```

Renaming a group letter is a THREE-part change and all three must land together: `git mv` the folder and files, keep the old id as a declared alias so existing citations resolve, then grep the repo for the old id and fix every hit.

### What the board altitude does NOT own

The two canvases the Index carries are content, not structure, so they follow the same approval rule as everything else here.
The board level shows how GROUPS connect and nothing else, because the index already lists every page below it; a board-level roster is the same information twice.
The per-page `⚙️ engine · 📋 page · 📂 folder` mapping lives one altitude down, in each group's own intro, which is what `lanes.py` writes.
A group anchors at `#group-<token>` and is not a page: the anchor scrolls the index, never opens a card, and never enters the settled count.
Rendering the index, checking a page, and checking a sentence all belong to `haipipe-board/cli/`.

## 🗺 The page altitude: the route, five steps

```
1  READ the input        what happened · what kind of record it deserves
                         (a Log line · a State entry · a lane reply ·
                          a Files row · a Decision Now row); a derived view,
                          aggregated from state the pages already hold,
                          deserves NO write, because a copy drifts

2  RESOLVE the board     the session's attached board, or the nearest board.md
                         above the working path; two plausible boards = ask,
                         never guess

3  FIND the owner        read board.md ## Pages, the ONLY registry; an id does
                         not reliably predict a folder (pages move, letters are
                         history), so never resolve by name pattern; aliases in
                         ## Links resolve older ids

4  PICK the section      the page spec says what each section owes; the input's
                         kind decides where it lands (see the table there)

5  WRITE anchored        append under the named ## heading, at the section
                         boundary; the sentence spec says how the line must
                         read (dated, signed, one sentence per line)
```

## ⚖️ The two write laws, inherited not invented

**The human-decision law (QC1b §5).**
Routing may append Log lines and factual State rows. When it has inspected the
evidence, it may move an Aim among the allowed State statuses and records the
reason in Log. It may not close a `### Decision Now` checkbox or change a
page-level human gate. Every proposal lands under the owning page's
`### Decision Now`, inside `## States` (JL 260731: never make the decision in
chat); a row the human has answered is closed with the answer recorded, and a row nobody answered waits for them.

**The cross-board law (QB1 §4).**
Mechanical writes carry no judgement and are always allowed.
Editorial writes are never ours on a board that is neither the skill set nor the board being worked: there, the output is a report addressed to that board's owner, not an edit.

## 🎯 Where a GROUP-altitude input lands (settled by the merge, 260802)

Some findings are about a whole group rather than any one page in it: a status readout across its pages, a gap between what the group promises and what its members cover, a rename that would make the set legible.
Before the merge this verb resolved PAGES only, so such a finding had no target and stayed in chat, which is the failure the board exists to prevent.

It lands in the group's intro prose in `board.md`'s `## Pages`, written at the section boundary, and `lanes.py` refreshes the block underneath it.

```
a finding about ONE page      →  that page's owning section
a finding about A GROUP       →  the group's intro in board.md ## Pages
a finding about THE BOARD     →  ## Topic, ## Pipeline, or ## Board Map
```

Decomposing a group finding onto its member pages was the alternative and it is refused: a finding about the group as a whole splits into pieces that individually say less than the whole did.
The rule was only available once one unit owned both altitudes, which is what the merge bought.

## 🚪 When nothing fits

A piece of work belonging to no question is itself a question that should be opened; that rule already exists in the sync verb.
Routing therefore ends in one of exactly three states:

```
LANDED     the write is on the owning page, and the reply names it
PROPOSED   no page owns this: routing drafts the page id, title, and group
           it would open, and waits; it never creates silently; the draft
           itself is a decision, so it goes to the nearest owning page's
           Decision Now rather than staying in chat
REPORTED   the owner is another family's board: a report, not an edit
```

**The gate before the reply (QA3, JL 260802).**
Five conditions hold before an agent may tell a person a round is done, and `cli/gate.py` runs the two that are mechanical:

```
①  WRITTEN BACK   every change has a record on the page that owns it
②  REBUILT        board.html came from the .md as it stands now
③  CHECKED        0 errors, and no page this round touched gained a warning
④  REACHABLE      the tab the person opens can run what shipped
⑤  STATED         the reply names which of ①-④ ran, with ③'s numbers
```

Run `python3 <board-skill>/cli/gate.py <board> --start` before the work and the same command without `--start` after it. The script lives in `haipipe-board/cli/`, not here: this skill ships one script and it is `src/lanes.py`.
③ compares PER PAGE, never the board's total, because a second session writing the same board moves the total underneath you: it went 304 to 276 during one round on 260802. A warning the round introduced blocks the handback; the board's standing warnings are out of scope.
① and ④ are printed as not tested, because whether a change was substantive and whether the person's own tab has the new assets are judgments the command cannot make. A gate that reports a condition it did not test is worse than no gate.
A round that changed PROSE also owes a cold read by `haipipe-board-reviewer-agent`; a round that changed only mechanics does not, since there is nothing for a reader to judge.
A failed gate is reported, never hidden. "The checker is red and here is why" is worth more than "done" and wrong.

**The reply contract (JL 260731).**
Whatever the end state, the reply closes with the routing footer: one line per write, `page id · ## section`, so the human sees where every record landed without hunting.
Decisions are LISTED IN BRIEF and never re-argued (JL 260802, amending the count-only rule of 260731): the reply gives one line per Decision Now row, the ask plus the recommended option, so the human can see what is waiting on them without opening the page.
The full row lives only on the page, with its `Part`, `Why now`, the options and what each commits you to, `Blocks`, and the default; the reply never reproduces those.
A bare count was too thin to act on, because a number tells the human that something waits and not whether it is worth opening the page now.
The footer's last line is `Next: <the one action the user should take now>` (JL 260731: "add a new line like Next:xxxx suggest what user to do next"): one concrete, immediately doable step (open this page, tick these rows, hard-refresh and click this button), never a list and never CC's own next task.

## 📂 Files

```
haipipe-board-routing/
├── SKILL.md            this contract
├── CHANGELOG.md        version history, including haipipe-board-index's
└── src/lanes.py        the per-group lane block, round-tripped
```

The page altitude owns no script: it is executed by the agent that loads this contract plus the two specs.
The board altitude owns exactly one, `src/lanes.py`, which arrived with `haipipe-board-index` on 260802; `regroup` wraps `haipipe-board/cli/regroup.py` rather than reimplementing it.
Reads and writes `board.md` and page `.md` files only, never the generated `board/` site.
The named next step: the write path itself moves behind `serve.py`'s anchored-append endpoint, so a routed write and a clicked comment share one code path.
