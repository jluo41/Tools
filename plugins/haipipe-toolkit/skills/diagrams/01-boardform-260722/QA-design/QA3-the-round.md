# The round: when an agent may reply, and what the reply says
state: 🟡 PARTIAL · the gate is drawn and 5 rows wait on JL
owner: JL
method: name the gate between finishing work and handing it back, make every condition machine-runnable, and rule who owns the reply's body once a board is attached

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

**The round, today and proposed**: where the gate goes, and what each of its conditions asserts.

```text
   ── the round today, and the gate this page proposes ─────────────

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

**The reply as it already ships**: every part that has an owner, and the one question none of them answers.

```text
   part of the reply    what it carries                  status
   ────────────────────────────────────────────────────────────────
   outcome              the round's result, first        ✅ shipped
   routing footer       one line per write ·             ✅ shipped
                        page id · ## section
   decision pointer     the page and its row count,      ✅ shipped
                        never the rows
   Next:                one action for the user          ✅ shipped
   status strip         3 lines from status.py           ✅ shipped
   ────────────────────────────────────────────────────────────────
   none of them says whether the work was right before it was written
```

`haipipe-board-routing` 0.2.0 owns the reply's shape, and this page does not restate it.
Every reply that wrote to a board closes with one line per write, `page id · ## section`, so the human sees where each record landed without hunting for it.
Decisions are pointed at rather than re-listed, which means the footer names the page and its `Decision Now` row count while the rows themselves live only on the page.
That rule came from JL on 260731 and it works; what it does not do is say anything about whether the work was correct before the footer was written.

### 2 · Why habit is not enough, with this session as the evidence

**Three failures, one day**: what shipped, what caught it, and what it cost.

```text
   what shipped                    what caught it        what it cost
   ───────────────────────────────────────────────────────────────────────
   an em-dash in QD4's prose       the warn count,       nothing · caught
                                   24 → 25
   fold comments announced live    JL's own tab          "still hard to add
   in a tab that could not run                           the discussions"
   the new JavaScript
   QC7's ## Files pointing at      nobody                a page wrong within
   four moved functions                                  the hour
   ───────────────────────────────────────────────────────────────────────
   one caught by a rule · one by the human · one by nobody
```

Five releases shipped from this board on 260731, and the build and the checker were run by hand after each one, which is exactly the problem: nothing would have stopped a reply that skipped them.

#### 2.1 · The em-dash that a number caught
An em-dash landed in `QD4`'s prose against a standing house rule, and it was caught only because the warning count was compared against the round's baseline and had risen from 24 to 25.
A round that had not compared the counts would have shipped it silently.

#### 2.2 · The feature that shipped into a tab that could not run it
A reply announced that fold comments were live when the tab JL was using could not run the new JavaScript at all, and JL's answer was "still hard to add the discussions".
The work was genuinely done and the board was genuinely not ready to be checked, which is the exact distinction this gate exists to draw.

#### 2.3 · The page that was wrong the hour it was written
`QC7`'s `## Files` section pointed at `serve.py` for four functions that a concurrent session moved into `live/write.py` within the hour.
Nothing re-read the page after the move, so a page that had just been written was already wrong.

### 3 · The gate, proposed

**The five conditions**: what each one asserts, and the command that answers it.

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

**3.1 · 🔍 What each condition means**

#### 3.1.1 · ① WRITTEN BACK, the work left a trace where the next person will look
You asked, the agent did it, and the only record is the chat.
Tomorrow the chat is gone and the page still says the old thing.
The condition is that every substantive change has a line on its owning page: an Aim's State moved, a `## Log` line was added, a Content part was written.
`SKILL.md`'s `sync` verb already asks for this, and the gate is what turns skipping it from a habit into a failure.

#### 3.1.2 · ② REBUILT, the html a reader opens came from the markdown as it stands now
The `.md` is the only source and `board/` is generated, so an edit is invisible on the page until `cli/build.py` runs.
`watch.py` usually does it, but a dead watcher leaves a correct file and a wrong page, and nothing about the file says which one you have.
The condition is that the build ran during this round and exited clean.

#### 3.1.3 · ③ CHECKED, the checker is not red and this round did not make it redder
`cli/check.py` reads every page and reports errors and warnings: a dead path in `## Files`, a part with no figure, an em-dash in prose, a page whose `state:` contradicts its own Aims.
The condition is 0 errors, plus a warning count no higher than the one at the start of the round.

#### 3.1.4 · ④ REACHABLE, the tab you will actually open can run what shipped
A browser keeps the old CSS and JS until something tells it not to.
On 260731 a round announced that fold comments were live while the tab JL had open could not run the new JavaScript at all, and his answer was "still hard to add the discussions".
The work was genuinely done and the board was genuinely not ready to check, which is the exact distinction this gate draws.
The assets stamp is the mechanism and this is the condition.

#### 3.1.5 · ⑤ STATED, the reply says which of the four actually ran, with numbers
A reply saying "the checker is red and here is why" is worth more than a reply that says done and is wrong.
The condition is that the reply carries `haipipe-board-routing`'s footer, one line per write, plus ③'s before and after counts, and that it never claims a condition the round did not run.

**3.2 · 📊 Why ③ compares a count instead of demanding zero**

#### 3.2.1 · Zero is unpassable, so zero would be ignored
The board carries 276 standing warnings as of 260802, most of them from two conventions the checker gained after the rest of this page was written: 94 parts with no figure and 93 dead `## Files` paths.
Demanding zero would make the gate unpassable and therefore ignored, while demanding that the round did not ADD one is achievable and is exactly the test that caught the em-dash on `QD4`.

#### 3.2.2 · The delta is only trustworthy per page
Comparing whole-board counts has one weakness this session hit directly.
Three other sessions were writing this board at the same time, and the total moved from 304 to 276 and the page count from 53 to 54 during a round that touched one page.
A round can only honestly claim the delta for the pages it edited.

### 4 · What a machine cannot check, and who covers it

**Two instruments, one boundary**: what each one judges, and which of them has no cadence yet.

```text
   instrument        judges                        cadence
   ──────────────────────────────────────────────────────────────
   cli/check.py      structure                     every round
                     dead paths · missing figures  (the gate, ③)
                     em-dashes · state vs Aims
   ──────────────────────────────────────────────────────────────
   Agent-1           prose                         UNRULED
                     is the argument right · is    (the 🤖 row
                     the page still true after     below)
                     the code moved
   ──────────────────────────────────────────────────────────────
   the boundary between them is itself a judgment a machine cannot make
```

A checker tests structure, and it cannot test whether the prose is right, whether the argument holds, or whether the page still says something true after the code moved underneath it.
`QF1` already names the two instruments for this: a mechanical checker for structure, and a zero-background reviewer for readability and visible staleness.
The gate above is the mechanical half made mandatory, and the open question is whether `Agent-1`, the fresh-context reviewer, runs every round or only on request.
Requiring it on every round is honest and slow; requiring it on rounds that changed prose rather than only mechanics is the middle path, and the boundary between those two is itself a judgment a machine cannot make.

### 5 · What the reply says

**The reply, in order**: the four parts a reader gets, and the one that has no owner.

```text
   order   part              owner
   ────────────────────────────────────────────────────────
   1       outcome           this page, §5
   2       the body          ⚠️ NOBODY · see §6
   3       routing footer    haipipe-board-routing
   4       status strip      haipipe-board SKILL.md · QD6
   ────────────────────────────────────────────────────────
   a failed gate is REPORTED at 1, never hidden
```

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
                                    part
   what is true now           ──▶ ## States                the state, not rows
   what only JL can rule      ──▶ ## States ›              the count and where
                                    Decision Now
   what changed this round    ──▶ ## Log                   one line per write
   ────────────────────────────────────────────────────────────────────
   the page is addressable, commentable, and still there tomorrow
   the reply POINTS at it, and closes on status.py's three lines
```

The reply and the page are two places the same round can put the same thing, and only the page keeps it.

**6.1 · 📜 The four contracts that write on one reply**

#### 6.1.1 · Who claims what, and which one is blind to the board
- `CLAUDE.md` at the SPACE root
  The repo default for every session: emoji-headed sections, and any non-trivial design, tradeoff or flow leads with an ASCII diagram rather than prose. It is loaded whether or not a board exists, so it cannot stand down on its own.
- `haipipe-board`'s SKILL.md, section `Session attachment and Closing Block`
  Owns the last three lines that `status.py` renders, and the rule that no prose follows them.
- `haipipe-board-routing` 0.2.0
  Owns the write-back footer: one line per write as `page id · ## section`, decisions pointed at instead of re-listed, and a closing `Next:` line naming one action for the user.
- this page, §5
  Owns the order: outcome first, then the footer, and never a condition the round did not actually run.

#### 6.1.2 · The body between them belongs to nobody
What none of them owns is the BODY between the outcome and the footer, and that is exactly where the two surfaces collide.
The repo default asks for the diagram, the sections and the comparison in the reply; the board asks for those same things on a page, where they carry an address, a state, and a place for a comment to land.
Written in both places they disagree within the hour, and the copy in the terminal is the one nobody can correct, comment on, or find again tomorrow.

**6.2 · 🎛 The proposal, and the half CC decided**

#### 6.2.1 · A precedence rule rather than a fifth contract
Once a board is attached, `haipipe-board` overrides the repo default for as long as the attachment holds, and the reply collapses to outcome, routing footer, status strip.
Anything that would be a section, a drawing, a comparison, or a list of rows becomes a page write first and a pointer second.
A round that produced nothing a page could hold is a discussion round and keeps the repo default, because there is no page to point at and thinking out loud with JL is the one thing a terminal is genuinely better at.

#### 6.2.2 · Why the rule's home is the door and not the verb
CC decided the home rather than asking, since nothing stops until it is answered: the body rule graduates into `haipipe-board`'s SKILL.md beside the closing block it precedes, not into `haipipe-board-routing`.
Routing is a verb and is loaded only when a write is being routed, while a board-attached session that writes nothing still owes the shape; `haipipe-board` is the door and is loaded for the whole session.
Routing keeps the write-lines footer, because those lines exist only when routing ran.

## Aims
### A3 · 🚦 The gate, proposed
- A3.1 · The five conditions run as one command rather than three steps and a remembered number.
  **Done when:** One invocation prints pass or fail plus the warning delta, and no round has to run `cli/build.py` and `cli/check.py` separately and compare by hand.
- A3.2 · The round's starting warning count comes from somewhere durable rather than the agent's own memory.
  **Done when:** Condition ③ reads a recorded baseline, and a session that was not present at the start of the round can still compute the delta.
- A3.3 · The gate is stated in a skill that a runtime actually loads.
  **Done when:** The five conditions are written into `haipipe-board-routing` or `haipipe-board`'s SKILL.md, because no runtime reads a Q page.

### A4 · 🧠 What a machine cannot check, and who covers it
- A4.1 · How often the fresh-context reviewer runs is ruled rather than left to habit.
  **Done when:** `Agent-1`'s cadence is written into the same skill that carries the gate, and a round can tell from the rule alone whether it owes a cold read.

### A6 · 🎛 Who controls the reply's shape once a board is attached
- A6.1 · An attached session knows the reply's shape before it writes its first reply.
  **Done when:** §6's precedence rule sits in `haipipe-board`'s SKILL.md beside the closing block, and a board-attached session given no other instruction produces the pointer form.

### P · 🏁 Page-level validation
- P1 · A fresh agent given only the shipped rule runs the gate without being told to.
  **Done when:** `QF2`'s instrument is run on a small board change and the agent builds, checks, compares the counts, and states the numbers unprompted.

## States
### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🗣 Does a board attachment override the repo's reply format?
      📍 `Part` `### 6 · Who controls the reply's shape once a board is attached`
      🔔 `Why now` JL 260802: "some content we want to put them in the Page, and not the user read the claude code results in TUI". `CLAUDE.md` and `haipipe-board` both claim the reply and neither yields, so the same drawing gets made twice.
      ⭐ `C ·` the live mode decides: `discussion` keeps the repo default, and `implementation`, `review` and `sourcing` collapse to outcome plus footer plus strip. Mode is already a field `status.py` renders every round, so this costs no new machinery.
      `A ·` `haipipe-board` wins for the whole attached session. Simplest to state, and it silences the one thing a terminal is genuinely better at, which is working an idea out before anything is written down.
      `B ·` the two stack, which is today's behaviour and is what produced the question.
      🛑 `Blocks` A6.1; the rule cannot ship until its condition is known.
      🤖 `If nobody answers` C takes effect.

- [ ] 🗣 Do the five conditions become the gate?
      📍 `Part` `### 3 · The gate, proposed`
      🔔 `Why now` JL 260731 asked that agents "work and test themself, and reply when the board is ready for the user to check". Nothing has been written down since, so all five are a habit that happens to have held.
      ⭐ `A ·` ratify all five as drawn. Each is already run by hand today, so this makes an existing practice binding rather than inventing new work.
      `B ·` ratify ① ② ③ only and leave ④ and ⑤ advisory. ④ needs the assets stamp and ⑤ needs ③'s numbers, so this is the half that is buildable today.
      🛑 `Blocks` A3.1 and A3.3; neither the command nor its home can be built around a set that may still change.
      🤖 `If nobody answers` A takes effect.

- [ ] 🗣 What does a rising warning count do to the handback?
      📍 `Part` `### 3 · The gate, proposed`
      🔔 `Why now` The board carries 276 standing warnings, so "zero warnings" is unpassable and would be ignored; the delta is the only usable test, and §3.2.2 shows it is only trustworthy per page.
      ⭐ `A ·` it blocks the handback, for warnings THIS round introduced. The em-dash on `QD4` was caught by exactly this test; the standing warnings stay out of scope.
      `B ·` it is reported in the reply and the round still hands back, which keeps the number visible without stopping work.
      `C ·` it is ignored, which is today's behaviour and is how a warning ships.
      🛑 `Blocks` nothing; ③ runs either way.
      🤖 `If nobody answers` A takes effect, scoped to warnings the round introduced.

- [ ] 🗣 Is the fresh-context reviewer part of every round?
      📍 `Part` `### 4 · What a machine cannot check, and who covers it`
      🔔 `Why now` The gate's mechanical half is about to become binding and the readability half has no cadence at all, so it will default to never.
      ⭐ `B ·` it runs only on rounds that changed prose. A mechanics-only round has nothing for a reader to judge.
      `A ·` `Agent-1` runs every round. Strongest guarantee, and it makes every small fix expensive enough that the gate starts getting skipped.
      `C ·` on request only. Cheapest, and it makes the cold read easy to forget.
      🛑 `Blocks` A4.1.
      🤖 `If nobody answers` B takes effect.

- [ ] 🗣 Which skill does the gate graduate into?
      📍 `Part` `### 3 · The gate, proposed`
      🔔 `Why now` A rule that lives only on this page binds nothing, because no runtime reads a Q page. §6.2.2 already placed the reply's BODY rule in `haipipe-board`; this row is only about the gate, and the two may legitimately differ.
      ⭐ `A ·` `haipipe-board-routing`, which already owns the footer, so the gate and the footer stay two halves of one contract in one skill.
      `B ·` `haipipe-board`'s SKILL.md, which every attached session loads first, so the gate is seen earlier but sits apart from the reply it governs.
      🛑 `Blocks` A3.3.
      🤖 `If nobody answers` A takes effect.

### A3 · 🚦 The gate, proposed
- ⬜ A3.1 · No single command exists. A round still runs `cli/build.py`, then `cli/check.py`, then compares the counts by hand.
- ⬜ A3.2 · Nothing records the baseline. This round captured `304 warn` by hand before editing, and the number was already stale by the end of the round because other sessions were writing the same board.
- 🧠 A3.3 · Waiting on the `🗣 Which skill does the gate graduate into?` row above.

### A4 · 🧠 What a machine cannot check, and who covers it
- 🧠 A4.1 · Waiting on the `🗣 Is the fresh-context reviewer part of every round?` row above.

### A6 · 🎛 Who controls the reply's shape once a board is attached
- 🧠 A6.1 · Waiting on the `🗣 Does a board attachment override the repo's reply format?` row above. §6 is written and CC has settled the home; what is unruled is whether the override is unconditional or decided by the live mode.

### P · 🏁 Page-level validation
- ⬜ P1 · Not run, and it cannot run before A3.3 ships, because there is no shipped rule to hand a fresh agent.

## Files
### ⚙️ Engines · what RUNS this subject
- `../../board/haipipe-board/cli/build.py`
  Condition ②'s instrument; its exit line is what proves `board.html` matches the pages.
- `../../board/haipipe-board/cli/check.py`
  Condition ③'s instrument, and the source of the warning count the gate compares.
- `../../board/haipipe-board/status.py`
  Condition ⑤'s last three lines, and the renderer of the `mode` field the first Decision Now row would switch on.

### 📋 Contracts · what CARRIES a rule to other pages
- `../../board/haipipe-board-routing/SKILL.md`
  Owns the reply's footer and the point-do-not-re-list rule; candidate `A` for the gate's home.
- `../../board/haipipe-board/SKILL.md`
  Owns the closing block and is loaded by every attached session; candidate `B` for the gate, and where §6.2.2 puts the reply-body rule.
- `CLAUDE.md`
  The repo default an attached session has to override; §6.1.1's first contract.

### 🧪 Checks · what CATCHES a page breaking a rule
- `QF-execute/QF1-acceptance.md`
  The two instruments this gate makes mandatory, and the readability half a checker cannot cover.
- `QF-execute/QF2-newcomer.md`
  P1's instrument: hand a fresh agent only the shipped rule and see whether it runs the gate unprompted.

### 📥 Input files · what the work READS
- `QD-working/QD6-session-status-strip.md`
  The settled half of the reply: the three-line strip, its attachment order, and its closed vocabulary.
- `QD-working/_archive/QD4-liveupdate.md`
  Condition ④'s mechanism, and the 260731 incident that showed a finished round can still leave a board a human cannot check.

### 📤 Output files · what a BUILD writes
- `board/QA/QA3-the-round.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit.

## Log
260802 · Reformatted to QB4's grammar on JL's ask: figures and captions on all six parts, `**N.M ·**` groups and `#### N.M.K ·` paragraphs, `## Items to Finish` → `## Aims` with A3/A4/A6/P ids and `Done when`, `## Where we are` → `## States` with one row per Aim, the five Decision Now rows rewritten to QB4 §5.2 (📍 🔔 ⭐ 🛑 🤖), and `## Files` regrouped into the ⚙️ 📋 🧪 📥 📤 action menu
260802 · Opening rewritten on JL's ask ("I need to understand QA3 first"): the visible paragraph was one bare question because the blank line sat after it, so all four explanation sentences rendered inside the drawer; More details is now labelled parts per QB4 §1
260802 · §3 gained one paragraph per condition after JL asked what the five mean; the "24 standing warnings" claim was stale and is now 276 with its two dominant rules named; 4 dead `## Files` paths fixed (`build.py` and `check.py` moved into `cli/`, and two neighbour pages moved into group folders)
260802 · §6 opened on JL's question about who controls a board-attached reply's shape; the body between the outcome and the footer turns out to be unowned, the precedence row is in Decision Now, and CC decided the rule's home itself since nothing stopped on it
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · Opened on JL's ask that agents "work and test themself, and reply when the board is ready for the user to check"; the reply's shape was already settled in haipipe-board-routing 0.2.0, so this page owns only the gate before it
