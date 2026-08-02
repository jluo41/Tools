# haipipe-board-routing · v0.9.0
state: 🟡 in flux · absorbed haipipe-board-index 260802
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-board-routing` is the board family's only verb that writes: one thing that happened becomes one dated record on the page that owns it.
Since 260802 it also proposes a board's groups and pages, then creates those files once a person approves.
`haipipe-board` renders, serves and checks the board; reach here when something that happened must be kept on it.
The merge is one day old, no group finding has landed through the new rule yet, and one unit now holds two approval rules that only the contract keeps apart.

**What one anchored write is**: the input is whatever happened outside the board, such as JL ruling a question in chat, an audit finding, a correction, or a status that changed.
Routing finds the owning page in `board.md`'s `## Pages`, then appends under a named `##` heading rather than at a byte offset, because a blind offset cut `QB4d`'s Opening sentence in half on 260730.
The line it writes is dated and carries who said it, so a later reader can tell when the fact landed and on whose word.

**Why the two altitudes need different approvals**: a page write records something that already happened, so it lands on its own.
A board write decides which pages will exist, and the group letters it picks are cited by every page opened afterwards, so it stops and waits for the person.
Content part 1 states that separation, and `## Aims` carries it as the one open risk the merge introduced.

**Covered elsewhere**: `haipipe-board` owns the machinery, `build.py`, `serve.py` and `check.py`, while this verb writes markdown only.
`haipipe-board-page` says which section a write owes and `haipipe-board-sentence` says how the line must read; routing loads both, and neither of them writes anything itself.
`haipipe-board`'s `open` action still describes propose and materialize too, which Content 2.2 declares on purpose, so those two descriptions have to be corrected together.
`haipipe-board-index` held the board altitude until 260802; its folder is deleted and its page sits in `_archive/`.

**Where it stands**: 10 releases shipped between 260731 and 260802, ending with the merge, which is what `🟡 in flux` on the `state:` line is reporting.
No group-altitude finding has been written through the new landing rule, no fresh agent has been measured choosing this door, and `haipipe-board-digest` is named on the roster and not on disk.
Each of those is an open row in `## Aims`.

## Diagram
<!-- haipipe:skill:tree:start 909a02c37e3ea486 board/haipipe-board-routing -->

**What `haipipe-board-routing` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-board-routing/
  src/
    lanes.py           253 ln  One `⚙️ engine · 📋 pages · 📂 folder` lane block per group, in board.md.
  CHANGELOG.md         129 ln  haipipe-board-routing · Changelog
  SKILL.md             226 ln  /haipipe-board-routing · every write onto a board, at both altitudes
```

<!-- haipipe:skill:tree:end -->

**Both altitudes, and the approval that differs between them**: a board write stops for a person; a page write lands on its own.

```text
WORKFLOW  two altitudes since 260802, two approval rules, one unit

  🗂 BOARD + GROUP ALTITUDE   (arrived with haipipe-board-index)
     a topic, no board yet
        │
        ▼
     propose      spine · close · groups · pages · connections · skills
        │         talk only, write NOTHING
        ▼
     ⛔ STOP and get the person's approval ── this is the rule that
        differs from the page altitude, and the merge must not blur it
        │
        ▼
     materialize  board.md + one folder per group + one file per page
     lanes        src/lanes.py <board> [--apply], round-trips
     regroup      wraps haipipe-board/cli/regroup.py
        │
        ▼  hands off to haipipe-board, which builds the board/ site

  ✍️ PAGE ALTITUDE  ── lands on its own: it records what already happened

  ONE input, no board open
  a ruling · a finding · a correction · a status change
        │
        ▼
  1 READ      what happened, and what record it deserves
              a derived view, aggregated from state the pages already
              hold, deserves NO write, because a copy drifts
        ▼
  2 RESOLVE   the attached board, or the nearest board.md above the path
              two plausible boards = ASK, never guess
        ▼
  3 FIND      board.md ## Pages, the ONLY registry
              an id does not predict a folder, so never resolve by name
              ## Links resolves the older ids
        ▼
  4 PICK      loads 📄 haipipe-board-page  · which section owes this
              loads ✒️ haipipe-board-sentence · how the line must read
        ▼
  5 WRITE     append under the named ## heading, at the SECTION BOUNDARY
              never at a byte offset: a blind offset spliced QB4d's
              Opening sentence in half on 260730

  ── three end states ────────────────────────────────────────────
  ✅ landed     a Log line · a States row · a factual Aim State
  🟡 proposed   a Decision Now row · a page it would open, not opened
  📮 reported   another owner's board: an editorial write becomes a
                report to them, never an edit (QB1 §4)

  ── never ───────────────────────────────────────────────────────
  🚫 tick a checkbox · flip state: · pass a page-level human gate
     it reads a claim and cannot verify it, so it may not close one

  ── where a GROUP-altitude input lands (settled by the merge) ────
  a finding about ONE page   →  that page's owning section
  a finding about A GROUP    →  the group's intro in board.md ## Pages
  a finding about THE BOARD  →  ## Topic, ## Pipeline, or ## Board Map
     this rule was only available once ONE unit owned both altitudes

  🔁 digest = this verb FANNED OUT over one session, one call per
     input. Named on the roster, not on disk.
  ⚙️ one live caller in code today: haipipe-board/cli/meetingpage.py
```

## Content
<!-- haipipe:skill:body:start 909a02c37e3ea486 board/haipipe-board-routing -->

**haipipe-board-routing** · `0.9.0` · last shipped 2026-08-02

- folder   `board/haipipe-board-routing/`
- tools    not declared
- summary  Absorbs haipipe-board-index: one WRITE verb now owns both altitudes, so a group-altitude input finally has somewhere to land.

### SKILL.md




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


- 1 · 🗂 Two altitudes, one verb (JL 260802)
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

- 2 · 🏗 The board altitude: propose, then materialize

- 2.1 · `propose` · before any file exists
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

- 2.2 · `materialize` · after approval
      `board.md` (title, spine, close, `## Topic`, `## Pipeline`, `## Pages`, plus `## Board Structure` when the board must explain its source and webpage shape), one descriptive folder per group, one page file per listed page, then hand off to `haipipe-board` to build the generated `board/` site.
      This is the same work `haipipe-board`'s `open` action describes to a person running a board by hand.
      The door keeps that description because a person opening their first board should not have to load a second skill; this contract is what an agent loads when it does the work, and the two must be corrected together.

- 2.3 · `lanes` · refresh the per-group blocks
      ```bash
      python3 src/lanes.py <board-dir>            # dry run: what would change
      python3 src/lanes.py <board-dir> --apply    # write board.md
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

- 2.4 · `regroup` · move pages into one folder per group
      Wraps `haipipe-board/cli/regroup.py`, which is the migration tool for any group rename or split:
      ```bash
      python3 ../haipipe-board/cli/regroup.py <board-dir>            # plan
      python3 ../haipipe-board/cli/regroup.py <board-dir> --apply    # git mv
      ```
      Renaming a group letter is a THREE-part change and all three must land together: `git mv` the folder and files, keep the old id as a declared alias so existing citations resolve, then grep the repo for the old id and fix every hit.

- 2.5 · What the board altitude does NOT own
      The two canvases the Index carries are content, not structure, so they follow the same approval rule as everything else here.
      The board level shows how GROUPS connect and nothing else, because the index already lists every page below it; a board-level roster is the same information twice.
      The per-page `⚙️ engine · 📋 page · 📂 folder` mapping lives one altitude down, in each group's own intro, which is what `lanes.py` writes.
      A group anchors at `#group-<token>` and is not a page: the anchor scrolls the index, never opens a card, and never enters the settled count.
      Rendering the index, checking a page, and checking a sentence all belong to `haipipe-board/cli/`.

- 3 · 🗺 The page altitude: the route, five steps
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

- 4 · ⚖️ The two write laws, inherited not invented
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

- 5 · 🎯 Where a GROUP-altitude input lands (settled by the merge, 260802)
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

- 6 · 🚪 When nothing fits
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
      Run `python3 cli/gate.py <board> --start` before the work and `cli/gate.py <board>` after it.
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

- 7 · 📂 Files
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
### The other files

1 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
src/lanes.py     253 ln  One `⚙️ engine · 📋 pages · 📂 folder` lane block per group, in board.md.
```

<!-- haipipe:skill:body:end -->

## Aims
- [x] 📐 Whether this verb absorbs the board altitude is ruled
      JL ruled it on 260802 in his own words, "maybe merge, I will do B", and 0.9.0 shipped the merge the same day.
      `haipipe-board-index` is deleted, `src/lanes.py` moved here, and this unit now owns `propose`, `materialize`, `lanes` and `regroup` alongside the five-step route.
- [x] 🧭 A group-altitude input has somewhere to land
      Settled by the merge rather than by its own ruling: a finding about a whole group lands in that group's intro prose in `board.md` `## Pages`, at the section boundary, with `lanes.py` refreshing the block underneath.
      Decomposing such a finding onto its member pages was the alternative and is refused, because the pieces individually say less than the whole did.
      No real group-altitude finding has been landed through the rule yet, which is what the next one will test.
- [ ] ⛔ The two approval rules stay apart inside one unit
      A page write lands on its own and a board write stops for a person, and nothing enforces that separation except the contract saying so.
      This is the specific risk the merge introduced: one unit, two rules, and the weaker one is the easy default under time pressure.
- [ ] 🧪 The door test is run on this unit
      `QC1b` §1.4 measured the test on `haipipe-board-page` and on nothing else: three fresh agents opened that door unaided at tool calls #5, #6 and #5.
      This unit has one caller in code, `haipipe-board/cli/meetingpage.py`, and no evidence yet that an agent handed a bare instruction chooses to open it.
- [ ] 🔁 `haipipe-board-digest` ships or leaves the roster
      Digest is this verb fanned out over a session, one call per input, and it is named on the roster and not on disk.
      Until it exists, this page also carries routing's own design questions by default rather than by decision, which is a fourth row on `QC1b`.
- [x] ⚖️ The write protocol is shipped rather than only argued
      0.8.0 carries the human-decision law, the cross-board law and the anchored-append rule under its own headings, so digest will inherit a written protocol instead of needing a new one.

## States
This is the fastest-moving unit in the family, 10 releases to 0.9.0, and as of 260802 it is the family's only write verb.
Its health is `🟡 in flux` because the merge landed the same day it was ruled and nothing has exercised the new altitude yet.
Both failure modes its page-altitude rules exist to prevent had already happened by hand before it shipped, which is why those fixes were written into the contract rather than learned from it; the board altitude has no equivalent scar tissue yet.

- 260802 JL · 📐 The merge, ruled and shipped the same day
  JL asked what `haipipe-board-index` was for, said it might not be needed, and ruled: "maybe merge, I will do B".
  The recommendation on the row had been to retire the index into the door instead, and JL took the option that also closed the group-altitude row, which retiring would have left open.
  0.9.0 absorbed the altitude, `src/lanes.py` moved in, and the index folder is deleted; the retired `Skill-1` page is in `_archive/` and its id still resolves through `## Links`.
- 260802 CC · 🗂 What the audit found, and the filing mistake that hid it
  Three of the index's five verbs were other units' work written a second time: `propose` and `materialize` are the door's `open`, `regroup` wrapped `cli/regroup.py`, and `check` was a subset of `cli/check.py`.
  It went two days unseen because `QC1b` had filed the index as a CONTRACT beside page and sentence, while its `SKILL.md` was five verbs and no contract, and a unit shelved on the wrong side of that split is never compared against the right list.
- 260802 CC · ⚙️ One caller in code, and it is not a board session
  `haipipe-board/cli/meetingpage.py` names this skill, which makes it the only sub-skill in the family with a consumer written in Python rather than in prose.
  That is real evidence for the door test's premise and it is not the door test, because the script names the skill instead of an agent choosing it.

## Log
260802 1810 · Absorbed `haipipe-board-index` at 0.9.0 on JL's `B` ruling: the board and group altitude, `propose` `materialize` `lanes` `regroup`, and `src/lanes.py`. The Opening, the `WORKFLOW` fence and the Aims were rewritten for two altitudes, and the group-altitude landing rule the merge settled is now on the page. The two Aims that were waiting on `QC1b`'s rows are closed, and one new Aim opened for the risk the merge introduced: one unit now carries two approval rules and only the contract keeps them apart
260802 1720 · Authored half written: the `WORKFLOW` fence replaced the template placeholder with the five-step route, the three end states and the never-list, five real Aims replaced the single health placeholder, and `state:` moved from 🔴 to 🟡 in flux on the release evidence. JL's merge proposal recorded as a State record pointing at `QC1b`'s row rather than restating its options
260731 1117 · page generated from `board/haipipe-board-routing/` by `skillpage.py new`

<!-- haipipe:skill:log:start 909a02c37e3ea486 board/haipipe-board-routing -->

Converted from the skill's own `CHANGELOG.md`: 10 releases.

260802 · `0.9.0`
      - **`haipipe-board-index` is merged into this skill and retired** (JL 260802: "maybe
        merge, I will do B"). This verb now owns BOTH altitudes: `board.md`'s structure and
        a page's sections. The family goes from one door, one altitude, two specs and one
        verb to one door, two specs, one verb.
      - What the audit found, and why the merge and not a rename. Three of the index's five
        verbs were other people's work written a second time: `propose` and `materialize`
        are `haipipe-board`'s `open` action, `regroup` wrapped `haipipe-board/cli/regroup.py`,
        and `check` was a subset of `haipipe-board/cli/check.py`. Only `src/lanes.py` was
        code the family held nowhere else, and it moved here with the merge.
      - **The gap this closes, which is the actual reason to do it.** A finding about a
        whole GROUP had no target and stayed in chat, because this verb resolved pages only
        while the block such a finding belongs in was owned by the other unit. The new
        landing rule: a group-altitude input lands in the group's intro prose in `board.md`
        `## Pages`, written at the section boundary, with `lanes.py` refreshing the block
        underneath. Decomposing a group finding onto its member pages was the alternative
        and is refused, because the pieces individually say less than the whole did.
      - **The two altitudes keep separate approval rules, and the merge must not blur them.**
        A page-altitude write lands on its own, because it records something that already
        happened. A board-altitude write asks a person first, because it decides what pages
        will exist and the group letters it chooses are cited by every future page.
      - `haipipe-board`'s `open` action keeps its own description of propose and materialize
        on purpose: a person opening their first board should not have to load a second
        skill. The duplication is now declared in both files rather than undiscovered, and
        the two must be corrected together.
      - Inherited from `haipipe-board-index`, unchanged in substance: `lanes.py` round-trips
        (roster generated from `## Pages`, every typed cell kept, a new page arrives with `?`,
        a retired page's row dropped); kept cells are collected GLOBALLY by page id, so a
        page that changes group carries its cells with it, proven when 31 of 42 pages moved
        in the `01-boardform-260722` restructure; the board canvas shows how GROUPS connect
        and is never a second copy of the page roster; a group anchors at `#group-<token>`
        and is not a page.
260802 · `0.8.0`
      - Carries QA3's five-condition gate that runs BEFORE the reply, with `cli/gate.py`
        as its one command. ③ compares warnings PER PAGE so a concurrent session cannot
        fail your round; ① and ④ are reported as not tested rather than assumed. A round
        that changed prose also owes a cold read; a mechanics-only round does not.
260802 · `0.7.0`
      - A machine now CLOSES a `### Decision Now` row once the person has answered it,
        recording which option, who ruled, when, and the words they used (JL 260802:
        "I think you should close it automatically, please go ahead and do it").
        It still may not close a row nobody answered, and may not flip a page-level
        human gate; a machine's own recommendation is never an answer. Before this a
        row answered in chat and acted on within the hour still rendered as pending,
        so the page reported work as waiting that had already shipped.
260802 · `0.6.1`
      - Repointed the two inherited write laws and the claim-automation citation after `QC1b`'s
        260802 Content rebuild: `QC6 §9` is now `QC1b §4` and `QC6 §10` is now `QC1b §5`.
260802 · `0.6.0`
      - The reply LISTS its Decision Now rows in brief instead of naming a count
        (JL 260802: "I think you can also briefly list the 5 decisions here as well").
        One line per row, the ask plus the recommended option; the full row, with its
        `Part`, `Why now`, options, `Blocks` and default, still lives only on the page.
        This amends the count-only rule of 260731, which was too thin to act on: a
        number says something waits, not whether it is worth opening the page now.
      - Note for the reader: `0.5.0` is in `SKILL.md` frontmatter with no entry below.
        It was not written by this change and its content is unknown here.
260801 · `0.4.1`
      - Routes current records into the canonical plural `## States` section while
        retaining singular State as an individual record name.
260801 · `0.4.0`
      - Routes current facts into `## State` and may update an Aim status only from
        inspected evidence, recording the transition reason in Log.
      - Keeps `### Decision Now` checkboxes and page-level human gates human-owned.
      - Replaced active `Where we are` instructions with the canonical State name.
260731 · `0.3.0`
      - The footer ends with a `Next:` line. JL, reading a bare routing footer: "what
        should I do? ... you can add a new line like Next:xxxx suggest what user to
        do next." The reply contract now closes with one concrete, immediately
        doable user action (open this page, tick these rows, hard-refresh and click
        this button); one step, never a list, never CC's own next task. The footer
        tells the human where records landed; the Next line tells them what to do
        about it.
260731 · `0.2.0`
      - Proposals land in Decision Now: whatever routing wants the human to decide
        (a PROPOSED tick, a drafted page, an open fork) is written as a row under the
        owning page's `## Where we are` `### Decision Now`, never left in chat
        (JL 260731: "don't make the decision here").
      - The reply contract: every reply closes with the routing footer, one line per
        write, `page id · ## section`, so the human sees where each record landed
        (JL 260731: "show me which page, which section is updated after each response").
        Decisions are pointed at, never re-listed in chat: page id + row count only.
      - Step 1 gains the no-write verdict: a DERIVED view, aggregated from state the
        pages already hold (a status readout, a progress table), deserves no write,
        because a copy of the state mirror drifts. First applied to the QB group
        readout the same day.
260731 · `0.1.0`
      - First cut, created on JL's order, from QC6 §8's settled shape: routing is the unit
        VERB (one input, find its owning page, write it back) and digest, when it arrives,
        is this verb fanned out over a session transcript, calling routing per input.
      - The five-step route reads board.md's `## Pages` as the ONLY registry, because an
        id does not reliably predict a folder (QC6 §9: pages move and letters are
        history), and it ends in exactly three states: LANDED, PROPOSED (never a silent
        page creation), or REPORTED (another family's board gets a report, not an edit).
      - Both write laws are inherited, not invented: the tick law (QC6 §10, propose a
        tick, never tick or flip `state:`) and the cross-board law (QB1 §4, mechanical
        writes always, editorial writes never on someone else's board).
      - Owns no scripts: the verb is the loaded contract plus the page and sentence
        specs. The named next step is sharing serve.py's anchored-append write path with
        the clicked-comment flow, so a routed write cannot invent its own byte-offset
        splice (the QB4d casualty of 260730).

<!-- haipipe:skill:log:end -->
