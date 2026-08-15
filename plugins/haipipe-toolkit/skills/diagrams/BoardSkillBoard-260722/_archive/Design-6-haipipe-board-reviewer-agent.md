# haipipe-board-reviewer-agent · v0.7.0
state: 🟡 in question · existence unruled since 260729, first exercised 260805 in the QB8e RUN
owner: JL
page-type: design
method: unit snapshot in skill/ via skillpage.py plug; every section authored by hand (converted from the mirror kind 260815)
session: 2dec022b-fc77-4efc-a03f-a589dc02583c

## Opening
`haipipe-board-reviewer-agent` is the fresh, read-only judge for a changed Board scope or one exact Page version inside RUN.
Reach for it over the Page's own `✅ Quality Check`, which shares the author's context and blind spots.
It verifies the source and render identity and judges the declared requirements.
CHECK then routes to CLOSE, REVISE, PROBE, DRAFT, or HOLD without curing its own finding.

**Why it has to be a stranger**: a writer who has just finished a revision knows what they meant, so they cannot see the premise the page never states.
A fresh dispatch has only the files, which is the position every later reader is in.

**What one dispatch returns**: `pass`, `revise`, or `blocked`, one row per reviewed unit, the exact checked version, and the authority route that follows.
It runs `check.py --strict` and `--summary` itself, so the mechanical findings and the prose findings arrive in one report.
`NOT VERIFIABLE` is one of its four verdicts and never counts as a pass.

**Covered elsewhere**: `check.py` is the deterministic half and says nothing about whether prose reads.
`haipipe-board-creator-agent` writes a page and leaves dispatching this reviewer to the caller.
Whether this unit stays at all is a decision row on `QC1b`, and this page's Aims carry what the unit still owes.

## Diagram
**What sits in this page's `skill/` plugin**: the unit's contract surface, written by `skillpage.py plug` and renamed so neither the installer glob nor page discovery can mistake it for the live unit.

```
skill/haipipe-board-reviewer-agent/
  CHANGELOG.md
  haipipe-board-reviewer-agent.md
```

**One dispatch, three passes, no write tool**: what it loads, what it judges, and how a verdict becomes a route.

```text
WORKFLOW  one file, no write tools, and the reason it must be a stranger

  the author finishes a revision
        │  the author CANNOT review it: they know far too much
        │  that was never written down
        ▼
  🤖 DISPATCH a fresh context  (a skill is LOADED, an agent is DISPATCHED)
        │
        ├─▶ LOADS, never restates:
        │     haipipe-board/SKILL.md        actions, states, sync
        │     haipipe-page/SKILL.md   the base page contract
        │     haipipe-page-for-skill/  the SKILL-PAGE variant, when the
        │                                    page under review is Skill-/Agent-
        │     page-phases/haipipe-page-check/  the CHECK judgment and
        │                                    routing boundary inside RUN
        │     ref/writing-rules.md          the cold-read standard
        │     the target board.md           topic, groups, links, order
        │
        ├─① check.py            the mechanical half, read-only
        ├─② cold-read each changed page in board.md context
        └─③ read the changed OPENINGS CONSECUTIVELY, in board order
              a page that is locally clear still FAILS here if its
              Opening is a form letter whose subject could be swapped
        ▼
  returns  ✅ pass   ✏️ revise   🛑 blocked
  routes   CLOSE · REVISE · PROBE · DRAFT · HOLD
  writes   NOTHING: no markdown, no rebuild, no state, no decision
           it has no write tools at all, so the rule is enforced
           rather than promised

  ⚠️ its own existence is the open question: JL said "don't need to
     have the review agent, stop it" on 260729 while one dispatch was
     running, and nobody has confirmed whether that retired the unit
     or only that run. The row is on QC1b's Decision Now.
```

## Content
### 1 · What this unit is, in one screen
**Live and snapshot**: the unit ships from its own folder, and this page judges a plugged copy.
```text
  ⚙️ the live unit, ships        📋 skill/haipipe-board-reviewer-agent/
     from its own folder    ──▶     the snapshot this page's
                            plug    judgments are about
```
`haipipe-board-reviewer-agent` is the read-only, fresh-context CHECK: it judges one source and render version, returns CLOSE, REVISE, PROBE, DRAFT, or HOLD, and never repairs the board it judges.
The live unit is one .md dispatched from `board/agents/`.

### 2 · Selection record · adopted from the specimen
**Where the record lives**: one argument, one home, adopted by reference.
```text
  🅰🅱 the candidates + full record ──▶ Design-3-haipipe-page · Content §2
  📄 this page keeps only what is its own: health · aims · snapshot
```
This page converted to a for-design page under the 260815 ruling that retired the mirror kind.
The candidates and the full record are written once, on the specimen: `Design-3-haipipe-page` Content §2.
This page adopts that selection rather than restating it, because seven copies of one argument would recreate the form-letter failure the ruling killed.
What is page-specific stays here: the Opening, the Aims, the States judgment on the unit's health, and the plugged snapshot above.

## Aims
- [ ] 🤖 Whether "don't need to have the review agent" retired the unit is ruled
      It was said on 260729 while one dispatch was running, so it may mean that run or the whole agent.
      Three written things go stale together if it meant the unit: `haipipe-board`'s writing rule 3, `QF1`'s acceptance half, and this page's own skill page.
      The row is on `QC1b`'s Decision Now and nothing here restates its options.
- [ ] 🧑‍⚖️ It reads the eight roster Openings consecutively
      That pass is the reason 0.4.0 exists, it has never run on a real batch, and there is now a real batch waiting: eight roster Openings rewritten on 260802, seven of them the same afternoon.
      This is the one check `haipipe-page-for-skill` names as decisive and says the author cannot perform.
- [x] 📚 It knows to reach past the base contract for a skill page
      0.5.0 added `haipipe-page-for-skill` as source 3, loaded whenever a page under review is a `Skill-<n>` or `Agent-<n>`.
      Without it this agent would have judged skill and agent pages by the base, whose Opening rule is the opposite one, marking correct prose wrong and passing the form letter the variant was written to catch.
- [x] 🛡 The read-only promise is enforced rather than trusted
      Its frontmatter grants `Read`, `Grep`, `Glob`, `Bash` and `Skill` and no write tool at all, so "never edits" is a property of the dispatch rather than an instruction it could disobey.
- [x] 🔗 It loads the contracts instead of carrying a copy of them
      The file says plainly that it is a procedure and not a second copy of the contract, and names six sources to load, "because a copy is exactly what goes a night out of date while the contract moves".
      That is the same defect still open in `live/chat.py`, avoided here by construction.

## States
The agent is written the way this family wants its agents written: it loads six sources, restates none of them, and holds no write tool.
What is unsettled is not its quality but its existence, and that has been unsettled since 260729.
It reached 0.7.0 on 260804 and was first exercised on this board on 260805, when the QB8e RUN dispatched its charter three times as the judge, as fresh-context `claude -p` subprocesses rather than the Agent tool.
Its review now has first results rather than only a procedure: two revise verdicts with file-and-line findings and one final pass that routed the run to CLOSE (receipt `_runs/page/QB8e/260805-0216-QB8e.json`).

- 260802 CC · 📚 It did not know about a contract that had shipped hours earlier
  `haipipe-page-for-skill` shipped on 260802 and this agent's source list was not updated with it, so it would have judged the eight skill and agent pages by the base contract whose Opening rule is the opposite one.
  JL found it by asking whether these agents call any skills, which is the kind of question a source list never answers on its own.
  Fixed at 0.5.0. The general lesson is on the agents' changelog: shipping a variant is finished when every agent that loads the base knows when to reach past it, not when the variant exists.
- 260802 CC · 🤖 The 260731 ruling argues against the retirement reading
  JL ruled that a skill is LOADED and an agent is DISPATCHED, and gave agents their own page kind below the skills.
  That distinction only matters if the agent exists, so the roster change made after the "stop it" remark reads as keeping the unit rather than dropping it.
  Nothing has been changed on the retirement reading, which means the status quo is already the answer the default points at.
- 260802 CC · 👁 The batch it was built for is now waiting
  Eight roster Openings were rewritten on 260802, seven of them in one afternoon and six by parallel writers working from one packet shape.
  That is precisely the input 0.4.0's consecutive-Openings pass was added to judge, and the session limit is the only reason it has not run.

## Log
- 260815 1230 · [REVISE-CC] converted to a for-design page (JL 260815): the three managed spans left the file, `skillpage.py plug` wrote the unit's contract surface to `skill/haipipe-board-reviewer-agent/`, and Content §2 adopts the selection recorded on the specimen.
- 260806 2116 · [REVISE-CC] swept to the 260806 architecture; the Diagram load list gains `page-phases/haipipe-page-check` (source 4 of six on disk since the RUN work) and the two "five sources/contracts" counts become six
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); "never yet dispatched" is over, the QB8e RUN exercised this judge three times as fresh-context claude -p subprocesses and its final CHECK pass closed the run.
260804 · Updated the authored mirror for exact-version CHECK and the CLOSE, REVISE, PROBE, DRAFT, or HOLD route returned to Page RUN.
260802 2100 · Synced to 0.5.0 and the authored half updated: the agent now loads `haipipe-page-for-skill` for a skill page, which it did not when that variant shipped hours earlier. Two Aims closed, one opened for the consecutive read of the eight roster Openings that is now waiting on it
260802 1720 · Authored half written: the `WORKFLOW` fence replaced the template placeholder with the dispatch, the four loaded contracts, the three-step review and the empty write-tool list, four real Aims replaced the single health placeholder, and `state:` moved from 🔴 to 🟡 in question. Recorded that the 260731 skill-versus-agent ruling argues against the retirement reading of JL's 260729 remark
260727 0017 · page generated from `board/agents/haipipe-board-reviewer-agent.md/` by `skillpage.py new`

