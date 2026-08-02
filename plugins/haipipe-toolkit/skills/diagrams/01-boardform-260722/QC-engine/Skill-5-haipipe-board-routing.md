# haipipe-board-routing · v0.6.1
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
Does `haipipe-board-routing` place one incoming update on the page and section that truly own it?

This verb turns an unstructured message into one anchored Board record rather than another fact left in chat.
The difficult cases are ambiguous ownership, missing pages, human decisions, and work that belongs to another Board.
Its result determines whether the Board stays current without silent page creation, ticks, or unsafe editorial writes.
It is healthy when every input lands, becomes an explicit proposal, or is reported to the outside owner.

## Diagram
<!-- haipipe:skill:tree:start 609036cd9d948960 board/haipipe-board-routing -->

```
haipipe-board-routing/
  CHANGELOG.md          78 ln  haipipe-board-routing · Changelog
  SKILL.md             101 ln  /haipipe-board-routing · one input, one owning page, one anchored write
```

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence if the tree
above is the whole story.
```

## Content
<!-- haipipe:skill:body:start 609036cd9d948960 board/haipipe-board-routing -->

**haipipe-board-routing** · `0.6.1` · last shipped 2026-08-02

- folder   `board/haipipe-board-routing/`
- tools    not declared
- summary  Routes current facts into States, reserves Decision Now and page-level gates for the human, and has the reply list its pending decisions in brief.

### SKILL.md




`haipipe-board`'s sync verb already states the order: claim which question first, then do the work, then write back in the same round.
Routing automates the claim (QC1b §4), which makes two existing failure modes machine-speed, so the rules here exist to keep them impossible rather than unlikely.

**The boundary:**

```
haipipe-board-routing            what it loads          what it never does
─────────────────────            ─────────────────      ─────────────────────
find the owning location         haipipe-board-page     render, serve, check
append the anchored write        haipipe-board-sentence tick a human decision
propose a page when none fits                           change a human page gate
                                                        create a page silently
```

Digest (a session transcript, many inputs) is this verb FANNED OUT: it calls routing per input and never reimplements it.
Digest is not built yet; when it is, it runs in a fresh context for the same reason the cold read does.


- 1 · 🗺 The route, five steps
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

- 2 · ⚖️ The two write laws, inherited not invented
      **The human-decision law (QC1b §5).**
      Routing may append Log lines and factual State rows. When it has inspected the
      evidence, it may move an Aim among the allowed State statuses and records the
      reason in Log. It may not close a `### Decision Now` checkbox or change a
      page-level human gate. Every proposal lands under the owning page's
      `### Decision Now`, inside `## States` (JL 260731: never make the decision in
      chat); the human ticks.
      **The cross-board law (QB1 §4).**
      Mechanical writes carry no judgement and are always allowed.
      Editorial writes are never ours on a board that is neither the skill set nor the board being worked: there, the output is a report addressed to that board's owner, not an edit.

- 3 · 🚪 When nothing fits
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
      **The reply contract (JL 260731).**
      Whatever the end state, the reply closes with the routing footer: one line per write, `page id · ## section`, so the human sees where every record landed without hunting.
      Decisions are LISTED IN BRIEF and never re-argued (JL 260802, amending the count-only rule of 260731): the reply gives one line per Decision Now row, the ask plus the recommended option, so the human can see what is waiting on them without opening the page.
      The full row lives only on the page, with its `Part`, `Why now`, the options and what each commits you to, `Blocks`, and the default; the reply never reproduces those.
      A bare count was too thin to act on, because a number tells the human that something waits and not whether it is worth opening the page now.
      The footer's last line is `Next: <the one action the user should take now>` (JL 260731: "add a new line like Next:xxxx suggest what user to do next"): one concrete, immediately doable step (open this page, tick these rows, hard-refresh and click this button), never a list and never CC's own next task.

- 4 · 📂 Files
      ```
      haipipe-board-routing/
      ├── SKILL.md            this contract
      └── CHANGELOG.md        version history
      ```
      Owns no scripts: the verb is executed by the agent that loads this contract plus the two specs.
      The named next step: the write path itself moves behind `serve.py`'s anchored-append endpoint, so a routed write and a clicked comment share one code path.
<!-- haipipe:skill:body:end -->

## Aims
- [ ] 🧠 Rule this skill's health
      `state:` is a judgment, not a version number: stable, in flux, needs work, or parked.

## States
Page generated 260731 1117. Nothing ruled yet.

## Log
260731 1117 · page generated from `board/haipipe-board-routing/` by `skillpage.py new`

<!-- haipipe:skill:log:start 609036cd9d948960 board/haipipe-board-routing -->

Converted from the skill's own `CHANGELOG.md`: 7 releases.

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
