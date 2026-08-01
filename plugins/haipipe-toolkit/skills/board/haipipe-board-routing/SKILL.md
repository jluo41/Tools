---
name: haipipe-board-routing
description: >-
  The routing VERB of the board family: take ONE input (a decision made in chat, a finding, a correction, a status change) and land it on the board, by finding the owning page and section and appending an anchored write. It loads the page and sentence specs, reads board.md's ## Pages as the only registry, proposes rather than creates when nothing fits, and may never tick a box or flip a state. Use when work happened and the board must record it: route this to the board, write it back, which page owns this, claim the question. Trigger: route, write back, owning page, land this on the board, update the log, /haipipe-board-routing.
metadata:
  version: "0.3.0"
  last_updated: "2026-07-31"
  summary: "The footer ends with a Next: line, the one action the user should take now (JL 260731)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-routing · one input, one owning page, one anchored write

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

## 🗺 The route, five steps

```
1  READ the input        what happened · what kind of record it deserves
                         (a Log line · a Where-we-are entry · a lane reply ·
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

**The tick law (QC6 §10).**
Routing reads claims; it cannot verify them.
It may append Log lines and Where-we-are prose and may write `PROPOSED:` before a tick it believes is earned; it may not close a checkbox or change a `state:` line.
Every proposal lands as a row under the owning page's `### Decision Now`, inside `## Where we are` (JL 260731: never make the decision in chat); the human ticks.

**The cross-board law (QB1 §4).**
Mechanical writes carry no judgement and are always allowed.
Editorial writes are never ours on a board that is neither the skill set nor the board being worked: there, the output is a report addressed to that board's owner, not an edit.

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

**The reply contract (JL 260731).**
Whatever the end state, the reply closes with the routing footer: one line per write, `page id · ## section`, so the human sees where every record landed without hunting.
Decisions are pointed at, never re-listed: the footer names the page and its Decision Now row count, and the rows themselves live only on the page.
The footer's last line is `Next: <the one action the user should take now>` (JL 260731: "add a new line like Next:xxxx suggest what user to do next"): one concrete, immediately doable step (open this page, tick these rows, hard-refresh and click this button), never a list and never CC's own next task.

## 📂 Files

```
haipipe-board-routing/
├── SKILL.md            this contract
└── CHANGELOG.md        version history
```

Owns no scripts: the verb is executed by the agent that loads this contract plus the two specs.
The named next step: the write path itself moves behind `serve.py`'s anchored-append endpoint, so a routed write and a clicked comment share one code path.
