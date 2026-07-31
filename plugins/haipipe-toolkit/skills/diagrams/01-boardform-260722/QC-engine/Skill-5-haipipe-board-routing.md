# haipipe-board-routing · v0.1.0
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
haipipe-board-routing is a shipped skill: what does it still owe, and is it healthy?

Write here what this skill is for in one paragraph a stranger could follow, why it exists as its own skill rather than as part of its neighbour, and what would have to be true for it to be considered finished.
The generated sections answer what it IS; only this one can answer whether it is any good.

## Diagram
<!-- haipipe:skill:tree:start afe80030f1303737 board/haipipe-board-routing -->

```
haipipe-board-routing/
  CHANGELOG.md          25 ln  haipipe-board-routing · Changelog
  SKILL.md              86 ln  /haipipe-board-routing · one input, one owning page, one anchored write
```

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence if the tree
above is the whole story.
```

## Content
<!-- haipipe:skill:body:start afe80030f1303737 board/haipipe-board-routing -->

**haipipe-board-routing** · `0.1.0` · last shipped 2026-07-31

- folder   `board/haipipe-board-routing/`
- tools    not declared
- summary  First cut (QC6 §8: the unit VERB; digest is this verb fanned out): the five-step route, the two write laws, and the propose-not-create rule.

### SKILL.md




`haipipe-board`'s sync verb already states the order: claim which question first, then do the work, then write back in the same round.
Routing automates the claim (QC6 §9), which makes two existing failure modes machine-speed, so the rules here exist to keep them impossible rather than unlikely.

**The boundary:**

```
haipipe-board-routing            what it loads          what it never does
─────────────────────            ─────────────────      ─────────────────────
find the owning location         haipipe-board-page     render, serve, check
append the anchored write        haipipe-board-sentence tick a box, flip state:
propose a page when none fits                           create a page silently
```

Digest (a session transcript, many inputs) is this verb FANNED OUT: it calls routing per input and never reimplements it.
Digest is not built yet; when it is, it runs in a fresh context for the same reason the cold read does.


- 1 · 🗺 The route, five steps
      ```
      1  READ the input        what happened · what kind of record it deserves
                               (a Log line · a Where-we-are entry · a lane reply ·
                                a Files row · a PROPOSED tick)

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
      **The tick law (QC6 §10).**
      Routing reads claims; it cannot verify them.
      It may append Log lines and Where-we-are prose and may write `PROPOSED:` before a tick it believes is earned; it may not close a checkbox or change a `state:` line.
      The human ticks.
      **The cross-board law (QB1 §4).**
      Mechanical writes carry no judgement and are always allowed.
      Editorial writes are never ours on a board that is neither the skill set nor the board being worked: there, the output is a report addressed to that board's owner, not an edit.

- 3 · 🚪 When nothing fits
      A piece of work belonging to no question is itself a question that should be opened; that rule already exists in the sync verb.
      Routing therefore ends in one of exactly three states:
      ```
      LANDED     the write is on the owning page, and the reply names it
      PROPOSED   no page owns this: routing drafts the page id, title, and group
                 it would open, and waits; it never creates silently
      REPORTED   the owner is another family's board: a report, not an edit
      ```

- 4 · 📂 Files
      ```
      haipipe-board-routing/
      ├── SKILL.md            this contract
      └── CHANGELOG.md        version history
      ```
      Owns no scripts at 0.1.0: the verb is executed by the agent that loads this contract plus the two specs.
      The named next step: the write path itself moves behind `serve.py`'s anchored-append endpoint, so a routed write and a clicked comment share one code path.
<!-- haipipe:skill:body:end -->

## Items to Finish
- [ ] 🧠 Rule this skill's health
      `state:` is a judgment, not a version number: stable, in flux, needs work, or parked.

## Where we are
Page generated 260731 1117. Nothing ruled yet.

## Log
260731 1117 · page generated from `board/haipipe-board-routing/` by `skillpage.py new`

<!-- haipipe:skill:log:start afe80030f1303737 board/haipipe-board-routing -->

Converted from the skill's own `CHANGELOG.md`: 1 releases.

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
