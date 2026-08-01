# The round: when an agent may reply, and what the reply says
state: 🔴 OPEN
owner: JL
method: name the gate between finishing work and handing it back, make every condition machine-runnable, and cite the reply's shape where it already lives

## Opening
When may an agent stop working and reply, and what must the reply say?
Half of this is settled: `haipipe-board-routing` 0.2.0 already rules that every board-writing reply closes with a `page id · ## section` footer and that decisions are pointed at rather than re-listed.
The other half is not written anywhere.
Nothing says an agent must have written its work back, rebuilt the board, and run the checker before it claims to be done, so a reply can arrive while `board.html` is stale or the checker is red, and the human opens a board that does not match what the reply promised.

JL 260731 stated the missing half directly: an agent should "work and test themself, and reply when the board is ready for the user to check".
This face owns that gate.


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
Each condition is stated so a script can answer it, because a condition a human has to judge is a condition that gets skipped when the round is long.

```text
   ①  WRITTEN BACK   every substantive change has a record on its owning page
                     SKILL.md's sync verb already says this; the gate enforces it
   ②  REBUILT        build.py ran and exited clean, so board.html matches the .md
   ③  CHECKED        check.py reports 0 errors, and the warning count is not
                     higher than it was when the round started
   ④  REACHABLE      what the human will open can run what shipped
                     QD4's assets stamp is the mechanism; this is the condition
   ⑤  STATED         the reply carries routing's footer, plus ③'s numbers
```

Condition ③ is the one worth arguing about, and the warning count rather than its absence is deliberate.
This board carries 24 standing warnings that predate the round, most of them whole-line bold that renders as a group title, so demanding zero would make the gate unpassable and therefore ignored.
Demanding that the round did not ADD one is both achievable and exactly the test that caught the em-dash.

### 4 · What a machine cannot check, and who covers it
A checker tests structure, and it cannot test whether the prose is right, whether the argument holds, or whether the page still says something true after the code moved underneath it.
`QF1` already names the two instruments for this: a mechanical checker for structure, and a zero-background reviewer for readability and visible staleness.
The gate above is the mechanical half made mandatory, and the open question is whether `Agent-1`, the fresh-context reviewer, runs every round or only on request.
Requiring it on every round is honest and slow; requiring it on rounds that changed prose rather than only mechanics is the middle path, and the boundary between those two is itself a judgment a machine cannot make.

### 5 · What the reply says
The reply states the outcome first, then the footer, and it never claims a condition it did not run.
A gate that failed is reported rather than hidden, because a reply saying "the checker is red and here is why" is worth more than a reply that says done and is wrong.
The numbers belong in the reply because they are the evidence the human would otherwise have to reproduce.

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

## Where we are
The reply's shape is settled and shipped; the gate before it is not written anywhere and is currently a habit that happens to have held.
Every condition proposed above is something this session already did by hand on 260731, which is the argument that they are achievable, and the three failures in §2 are the argument that doing them by hand is not enough.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

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
- `../../board/haipipe-board/check.py`
  Condition ③'s instrument, and the source of the warning count the gate compares.
- `../../board/haipipe-board/build.py`
  Condition ②'s instrument; its exit line is what proves `board.html` matches the pages.

### Neighbor faces this gate leans on
- `QF1-acceptance.md`
  The two instruments this gate makes mandatory, and the readability half a checker cannot cover.
- `QD4-liveupdate.md`
  Condition ④'s mechanism, and the 260731 incident that showed a finished round can still leave a board a human cannot check.

## Log
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · Opened on JL's ask that agents "work and test themself, and reply when the board is ready for the user to check"; the reply's shape was already settled in haipipe-board-routing 0.2.0, so this face owns only the gate before it
