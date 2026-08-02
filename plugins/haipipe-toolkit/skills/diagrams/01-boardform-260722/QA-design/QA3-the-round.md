# The round: when an agent may reply, and what the reply says
state: 🔴 OPEN
owner: JL
method: name the gate between finishing work and handing it back, make every condition machine-runnable, and cite the reply's shape where it already lives

## Opening
What must be true before an agent can tell you a round of Board work is done?
A round is one turn: you ask, the agent works, and it hands the Board back to you.
Today it hands back when the WORK is finished, which is not the same as the BOARD being ready for you to open.
Those two came apart three times on 260731, and a person caught it each time.
This page decides whether five conditions become a gate the agent must pass before it may say done.

**What "hand back" means**: The agent stops working and gives you the turn, usually with a sentence like "done, take a look".
Nothing reads the Board afterwards to check that the sentence is true.

**Why the work being right is not enough**: The work and the artifact you open are two different things.
An agent can write every word correctly and still leave you a stale `board.html`, a `## Files` list pointing at a file that moved an hour ago, or a checker that is red.
All three are real and all three happened on the same day; part 2 names them one by one.

**The five conditions, in one word each**: Written back, rebuilt, checked, reachable, stated.
Part 3 gives each one the command that answers it and the failure it prevents.
Each is written so a script can answer it, because a condition a person has to judge is the condition that gets skipped at the end of a long round.

**What this page owns, and what it does not**: The reply's footer and its closing strip are already settled and shipped, so this page does not restate them.
`haipipe-board-routing` owns the write-back footer and `QD6` owns the three-line status strip.
This page owns the gate that runs BEFORE the reply, and part 6 adds the newer half of the same problem, which is who controls the body of the reply in between.


## Diagram

```text
   ── the round today, and the gate this face proposes ─────────────

   TODAY                          PROPOSED
   ─────────────────────────      ─────────────────────────────────
   work                           work
     │                              │
   write it back                  write it back        ① every change has a
     │                              │                     record on its page
     │                            rebuild               ② board.html matches
     │                              │                     the .md it came from
     │                            check                 ③ 0 errors, and warns
     │                              │                     did not rise
     │                            confirm reachable    ④ the tab the human
     │                              │                     opens can run it
     ▼                              ▼
   reply "done"                   reply, stating ①-④ and the footer
     │                              │
     ▼                              ▼
   JL finds it is not             JL opens a board that is
   (260731: "still hard           already in the state the
   to add the discussions")       reply describes

   verification is HABIT today, and habit is what a gate replaces
```

## Content
### 1 · The half that is already settled
`haipipe-board-routing` 0.2.0 owns the reply's shape, and this face does not restate it.
Every reply that wrote to a board closes with one line per write, `page id · ## section`, so the human sees where each record landed without hunting for it.
Decisions are pointed at rather than re-listed, which means the footer names the page and its `Decision Now` row count while the rows themselves live only on the page.
That rule came from JL on 260731 and it works; what it does not do is say anything about whether the work was correct before the footer was written.

### 2 · Why habit is not enough, with this session as the evidence
Five releases shipped from this board on 260731, and the build and the checker were run by hand after each one, which is exactly the problem: nothing would have stopped a reply that skipped them.
Three concrete failures from the same day show what the gap costs.

An em-dash landed in `QD4`'s prose against a standing house rule, and it was caught only because the warning count was compared against the round's baseline and had risen from 24 to 25.
A round that had not compared the counts would have shipped it silently.

A reply announced that fold comments were live when the tab JL was using could not run the new JavaScript at all, and JL's answer was "still hard to add the discussions".
The work was genuinely done and the board was genuinely not ready to be checked, which is the exact distinction this gate exists to draw.

`QC7`'s `## Files` section pointed at `serve.py` for four functions that a concurrent session moved into `live/write.py` within the hour.
Nothing re-read the page after the move, so a face that had just been written was already wrong.

### 3 · The gate, proposed

**The five conditions**: what each one asks, and the command that answers it.

```text
   condition          what it asserts                    what answers it
   ────────────────────────────────────────────────────────────────────────
   ①  WRITTEN BACK    every change has a record on       a person, today
                      the page that owns it
   ②  REBUILT         board.html came from the .md       cli/build.py
                      as it stands now
   ③  CHECKED         0 errors, warnings no higher       cli/check.py
                      than at the round's start
   ④  REACHABLE       the tab you open can run           the assets stamp
                      what shipped
   ⑤  STATED          the reply names which of ①-④       the routing footer
                      ran, with ③'s numbers              + status.py
```

They run in that order, and each one catches a different way a round can look finished without being finished.

- ① WRITTEN BACK · the work left a trace where the next person will look
  You asked, the agent did it, and the only record is the chat. Tomorrow the chat is gone and the page still says the old thing. The condition is that every substantive change has a line on its owning page: an Aim's State moved, a `## Log` line was added, a Content division was written. `SKILL.md`'s `sync` verb already asks for this, and the gate is what turns skipping it from a habit into a failure.
- ② REBUILT · the html a reader opens came from the markdown as it stands now
  The `.md` is the only source and `board/` is generated, so an edit is invisible on the page until `cli/build.py` runs. `watch.py` usually does it, but a dead watcher leaves a correct file and a wrong page, and nothing about the file says which one you have. The condition is that the build ran during this round and exited clean.
- ③ CHECKED · the structural checker is not red, and this round did not make it redder
  `cli/check.py` reads every page and reports errors and warnings: a dead path in `## Files`, a division with no figure, an em-dash in prose, a page whose `state:` contradicts its own Aims. The condition is 0 errors, plus a warning count no higher than the one at the start of the round.
- ④ REACHABLE · the tab you will actually open can run what shipped
  A browser keeps the old CSS and JS until something tells it not to. On 260731 a round announced that fold comments were live while the tab JL had open could not run the new JavaScript at all, and his answer was "still hard to add the discussions". The work was genuinely done and the board was genuinely not ready to check, which is the exact distinction this gate draws. The assets stamp is the mechanism and this is the condition.
- ⑤ STATED · the reply says which of the four actually ran, with numbers
  A reply saying "the checker is red and here is why" is worth more than a reply that says done and is wrong. The condition is that the reply carries `haipipe-board-routing`'s footer, one line per write, plus ③'s before and after counts, and that it never claims a condition the round did not run.

Condition ③ is the one worth arguing about, and comparing the warning count rather than demanding its absence is deliberate.
The board carries 281 standing warnings today, most of them from two conventions the checker gained after the rest of this face was written: 97 dead `## Files` paths and 94 divisions with no figure.
Demanding zero would make the gate unpassable and therefore ignored, while demanding that the round did not ADD one is achievable and is exactly the test that caught the em-dash on `QD4`.
Comparing whole-board counts has one weakness this session hit directly: a concurrent session editing the same board moves the number underneath you, so the delta is only trustworthy per page.

### 4 · What a machine cannot check, and who covers it
A checker tests structure, and it cannot test whether the prose is right, whether the argument holds, or whether the page still says something true after the code moved underneath it.
`QF1` already names the two instruments for this: a mechanical checker for structure, and a zero-background reviewer for readability and visible staleness.
The gate above is the mechanical half made mandatory, and the open question is whether `Agent-1`, the fresh-context reviewer, runs every round or only on request.
Requiring it on every round is honest and slow; requiring it on rounds that changed prose rather than only mechanics is the middle path, and the boundary between those two is itself a judgment a machine cannot make.

### 5 · What the reply says
The reply states the outcome first, then the footer, and it never claims a condition it did not run.
A gate that failed is reported rather than hidden, because a reply saying "the checker is red and here is why" is worth more than a reply that says done and is wrong.
The numbers belong in the reply because they are the evidence the human would otherwise have to reproduce.

### 6 · Who controls the reply's shape once a board is attached

**Two surfaces**: what each thing a round produces is worth on the page, and what is left for the reply.

```text
  ── one round, two surfaces, and what each one is for ───────────────

   what the round produced        📋 THE PAGE              💬 THE REPLY
   ──────────────────────────     ────────────────────     ─────────────────
   a drawing of the design    ──▶ ## Diagram               a link to it
   the argument, the options,
     the tradeoff             ──▶ ## Content · one         one outcome line
                                    division
   what is true now           ──▶ ## States                the state, not rows
   what only JL can rule      ──▶ ## States ›              the count and where
                                    Decision Now
   what changed this round    ──▶ ## Log                   one line per write
   ────────────────────────────────────────────────────────────────────
   the page is addressable, commentable, and still there tomorrow
   the reply POINTS at it, and closes on status.py's three lines
```

The reply and the page are two places the same round can put the same thing, and only the page keeps it.

Four contracts write on the same reply today, and only one of them can tell that a board is open.

- `CLAUDE.md` at the SPACE root
  The repo default for every session: emoji-headed sections, and any non-trivial design, tradeoff or flow leads with an ASCII diagram rather than prose. It is loaded whether or not a board exists, so it cannot stand down on its own.
- `haipipe-board`'s SKILL.md, section `Session attachment and Closing Block`
  Owns the last three lines that `status.py` renders, and the rule that no prose follows them.
- `haipipe-board-routing` 0.2.0
  Owns the write-back footer: one line per write as `page id · ## section`, decisions pointed at instead of re-listed, and a closing `Next:` line naming one action for the user.
- this face, §5
  Owns the order: outcome first, then the footer, and never a condition the round did not actually run.

What none of them owns is the BODY between the outcome and the footer, and that is exactly where the two surfaces collide.
The repo default asks for the diagram, the sections and the comparison in the reply; the board asks for those same things on a page, where they carry an address, a state, and a place for a comment to land.
Written in both places they disagree within the hour, and the copy in the terminal is the one nobody can correct, comment on, or find again tomorrow.

The proposal is a precedence rule rather than a fifth contract.
Once a board is attached, `haipipe-board` overrides the repo default for as long as the attachment holds, and the reply collapses to outcome, routing footer, status strip.
Anything that would be a section, a drawing, a comparison, or a list of rows becomes a page write first and a pointer second.
A round that produced nothing a page could hold is a discussion round and keeps the repo default, because there is no page to point at and thinking out loud with JL is the one thing a terminal is genuinely better at.

CC decided the home rather than asking, since nothing stops until it is answered: the body rule graduates into `haipipe-board`'s SKILL.md beside the closing block it precedes, not into `haipipe-board-routing`.
Routing is a verb and is loaded only when a write is being routed, while a board-attached session that writes nothing still owes the shape; `haipipe-board` is the door and is loaded for the whole session.
Routing keeps the write-lines footer, because those lines exist only when routing ran.

## Items to Finish
### The gate as one command
- [ ] 🧰 Make the gate one command
      Today it is `build.py` then `check.py` then a manual comparison of warning counts against a number the agent remembered; it should be one invocation that prints pass or fail and the delta.
- [ ] 📌 Decide where the round's starting baseline comes from
      Condition ③ compares against the count at the start of the round, and nothing records that number today, so it lives only in the agent's memory of its own session.

### Shipping and proving the rule
- [ ] 📜 State the gate in the skill that owns it
      A rule that lives only on this page binds nothing, since no runtime reads a Q page; it graduates into `haipipe-board-routing`, which already owns the reply, or into `haipipe-board`'s `SKILL.md`.
- [ ] 🧪 Test the gate with a fresh agent
      `QF2`'s instrument applies directly: give an agent only the shipped rule, have it do a small board change, and see whether it runs the gate without being told.
- [ ] 🎛 Ship the attached-session reply rule where every session sees it
      §6's precedence rule binds nothing while it lives on this page; it graduates into `haipipe-board`'s SKILL.md, beside the closing block it precedes, so an attached session reads it before its first reply.

## Where we are
The reply's shape is settled and shipped; the gate before it is not written anywhere and is currently a habit that happens to have held.
Every condition proposed above is something this session already did by hand on 260731, which is the argument that they are achievable, and the three failures in §2 are the argument that doing them by hand is not enough.
260802 corrected what "settled and shipped" covers: only the footer and the strip are shipped, and §6 shows the body between them is claimed by the repo default and by nobody who knows a board is attached.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🎛 Rule whether a board attachment overrides the repo's reply format
      A · `haipipe-board` wins for the whole attached session, so every reply is outcome plus footer plus strip, and every drawing, comparison or section goes on a page.
      B · the two stack, so the reply keeps `CLAUDE.md`'s emoji sections and the board only adds its footer, which is today's behaviour and is what produced this question.
      C · the live mode decides: `discussion` keeps the repo default, and `implementation`, `review` and `sourcing` collapse to the pointer form.
      → CC's proposal: C. A silences the one thing a terminal is genuinely better at, which is working an idea out with JL before anything is written down; B is the status quo that puts the same drawing in a transcript and on no page. Mode is already a field `status.py` renders every round, so the switch needs no new machinery.
- [ ] 🚦 Ratify the five conditions as the gate
      Written back, rebuilt, checked, reachable, stated, all of them before an agent may reply that a round is done.
      → CC's proposal: yes as drawn; each one is already run by hand today, so this makes an existing practice binding rather than inventing new work.
- [ ] 📊 Rule what a rising warning count does
      A · it blocks the handback, so a round that raised the count cannot be called done until it is back down.
      B · it is reported in the reply and the round still hands back, which keeps the count visible without stopping work.
      C · it is ignored, which is today's behaviour and is how a warning ships.
      → CC's proposal: A for warnings the round introduced, because the em-dash on `QD4` was caught by exactly this test and would otherwise have shipped; the 24 standing warnings stay out of scope.
- [ ] 🤖 Rule whether the fresh-context reviewer is part of every round
      A · `Agent-1` runs every round, which is the strongest guarantee and makes every small fix expensive.
      B · it runs only on rounds that changed prose, since a mechanics-only round has nothing for a reader to judge.
      C · it runs on request only, which is cheapest and makes the cold read easy to forget.
      → CC's proposal: B; a mechanics-only round has nothing for a reader to judge, and A makes every small fix expensive enough that the gate gets skipped.
- [ ] 🏠 Rule where the gate graduates to
      A · `haipipe-board-routing` already owns the reply, so the gate and the footer stay two halves of one contract in one skill.
      B · `haipipe-board`'s `SKILL.md` is loaded first by every agent, so the gate is seen earlier but lives apart from the reply it governs.
      → CC's proposal: A, because the gate and the footer are two halves of one contract and splitting them across two skills is how they drift apart.

## Files
### Engines
- `../../board/haipipe-board-routing/SKILL.md`
  Owns the reply's footer and the point-do-not-re-list rule; the likely home for this gate once it is settled.
- `../../board/haipipe-board/cli/check.py`
  Condition ③'s instrument, and the source of the warning count the gate compares.
- `../../board/haipipe-board/cli/build.py`
  Condition ②'s instrument; its exit line is what proves `board.html` matches the pages.

### Neighbor faces this gate leans on
- `QF-execute/QF1-acceptance.md`
  The two instruments this gate makes mandatory, and the readability half a checker cannot cover.
- `QD-working/_archive/QD4-liveupdate.md`
  Condition ④'s mechanism, and the 260731 incident that showed a finished round can still leave a board a human cannot check.

## Log
260802 · Opening rewritten on JL's ask ("I need to understand QA3 first"): the visible paragraph was one bare question because the blank line sat after it, so all four explanation sentences rendered inside the drawer; More details is now labelled parts per QB4 §1
260802 · §3 gained one record line per condition after JL asked what the five mean; the "24 standing warnings" claim was stale and is now 281 with its two dominant rules named; 4 dead `## Files` paths fixed (`build.py` and `check.py` moved into `cli/`, and two neighbour pages moved into group folders)
260802 · §6 opened on JL's question about who controls a board-attached reply's shape; the body between the outcome and the footer turns out to be unowned, the precedence row is in Decision Now, and CC decided the rule's home itself since nothing stopped on it
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · Opened on JL's ask that agents "work and test themself, and reply when the board is ready for the user to check"; the reply's shape was already settled in haipipe-board-routing 0.2.0, so this face owns only the gate before it
