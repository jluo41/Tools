# haipipe-board-creator-agent · v0.6.0
state: 🟡 in flux · first real fan-out 260802, 3 of 6 died on a limit
owner: JL
page-type: design
method: unit snapshot in skill/ via skillpage.py plug; every section authored by hand (converted from the mirror kind 260815)

## Opening
`haipipe-board-creator-agent` is the producer for one target Page.
It supports parallel CREATE work and one DRAFT, PROBE, or REVISE authority inside RUN.
Reach for it to produce a Page version; reach for `haipipe-board-reviewer-agent` to judge that version.
It has no Bash tool and never touches `board.md` or rebuilds.
It never performs CHECK, so producer and judge cannot collapse into one hidden pass.

**The words in that paragraph**: A fresh context means the agent starts with no memory of the session that sent it, so everything it knows arrives in one assignment packet: the path, the id, the title, the sources it must read, and, for a new page, the siblings it must not overlap.
The caller is whoever holds `haipipe-board` in the session that dispatches the batch, and it stays a single context precisely because the writes it keeps are the ones two writers would collide on.

**Why the boundary is drawn by collision and not by subject**: Every other unit in this family is bounded by what it is about, the way `haipipe-page` owns one page and `haipipe-sentence` owns everything below a section.
This one is bounded by what it touches, because N copies of it are awake at the same moment.
So its limits are structural rather than advisory: it carries no Bash tool and cannot run `build.py`, `board.md` is out of scope so the one file every writer would collide on stays with the caller, and it may not read a sibling page, whose bytes may be mid-flight.

**Covered elsewhere**: `Agent-1` is the other half of the pair and judges what this one produced; it is read-only and does hold Bash, so it runs the mechanical checker this agent cannot.
`haipipe-board` keeps every shared write: registering the page in `board.md` `## Pages`, the lane block, one rebuild, one check.
The prose standard travels in neither, since each writer loads `haipipe-page` itself and a skill page also loads `haipipe-page-for-skill`, which is what keeps a copied checklist in the packet from drifting away from the skill.

**What the first run does not yet settle**: Those six packets were assembled by hand.
`haipipe-board`'s family section now states the dispatch policy, but its `open` and `add` actions still copy `ref/page-template.md` and write the page in the calling session, and nothing turns an approved page list into N packets.
Whether the fan-out pays at every batch size is also unmeasured; both are Aims below.

**What lifecycle production adds**: RUN supplies the Page, Phase, round, exact current version, intent, sources, constraints, and limits.
The agent performs exactly one DRAFT, PROBE, or REVISE authority and returns artifacts, evidence, findings, reason, and one suggested route.
The controller then rebuilds and versions the result before the independent reviewer sees it.

## Diagram
**What sits in this page's `skill/` plugin**: the unit's contract surface, written by `skillpage.py plug` and renamed so neither the installer glob nor page discovery can mistake it for the live unit.

```
skill/haipipe-board-creator-agent/
  CHANGELOG.md
  haipipe-board-creator-agent.md
```

**What the producer may do**: batch creation fans out by Page, while RUN serializes one Phase receipt before independent CHECK.

```text
   ── two producer modes, neither includes judgment ────────────────

   haipipe-board  (the door, and the only holder of shared state)
        │
        │  the approved proposal table  (QA2 §2)
        │  one row per page = one assignment packet
        ▼
   ┌─────────── FAN OUT · N agents, at the same time ───────────┐
   │                                                            │
   │  Agent-2        Agent-2        Agent-2       Agent-2       │
   │  QA1.md         QA2.md         QA3.md        QB1.md        │
   │    │              │              │             │           │
   │  writes ONE file each · touches nothing shared             │
   │  no Bash → cannot build · board.md → not in scope          │
   │  siblings arrive in the PACKET, never by reading them      │
   └────────────────────────────┬───────────────────────────────┘
                                │  N return contracts
                                ▼
   ┌─────────── SERIALIZE · the caller, exactly once ───────────┐
   │  register every page in board.md ## Pages                  │
   │  lanes.py --apply    build.py    check.py                  │
   └────────────────────────────┬───────────────────────────────┘
                                ▼
                        Agent-1 · reviewer
                    judges the batch, pass | revise

   Page RUN packet ─▶ Agent-2 · one DRAFT / PROBE / REVISE
                           │  phase receipt
                           ▼
                    build + version snapshot
                           │
                           ▼
                    Agent-1 · CHECK and route
```

The two halves are divided by one test: does the write touch a file another writer also touches.
One page's `.md` fails that test and so it fans out; `board.md`, the lane block, `board.html`, and the checker all pass it and so they stay with the caller.

## Content
### 1 · What this unit is, in one screen
**Live and snapshot**: the unit ships from its own folder, and this page judges a plugged copy.
```text
  ⚙️ the live unit, ships        📋 skill/haipipe-board-creator-agent/
     from its own folder    ──▶     the snapshot this page's
                            plug    judgments are about
```
`haipipe-board-creator-agent` produces ONE page in a fresh context: batch creation plus exactly one DRAFT, PROBE, or REVISE phase for RUN, and it never rebuilds or performs CHECK.
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
- [ ] 🚚 Give the caller its half, in `haipipe-board`
      The agent is written and the fan-out procedure is not: `SKILL.md`'s `open` and `add` actions still describe writing pages themselves, and nothing turns an approved proposal table into N assignment packets or performs the serialized tail once.
      Proven necessary on 260802: the six packets that produced the first real fan-out were assembled by hand, one at a time, in the calling session.
- [ ] 🩹 A dispatch that dies mid-batch is recoverable
      Three of the six writers on 260802 hit a session limit. They had written their page first, so nothing was lost, and that was luck rather than design.
      Nothing tells the caller which packets completed, so the caller re-read the files to find out.
- [ ] 📐 Decide the batch size ceiling, if there is one
      Six pages was six contexts reading the same four contracts, and each cost roughly 70,000 tokens.
      Whether that is worth it at every size, or only above some count, is still unmeasured.
- [x] 🧪 Run it on a real multi-page board
      Met 260802: six agents fanned out over six skill and agent pages of `BoardSkillBoard-260722`, one page each, and every one of them respected its scope.
      No two writers touched the same file, no agent edited `board.md`, and each returned a contract naming what it read and what it left alone.
- [x] 📚 It knows to reach past the base contract for a skill page
      0.4.0 added `haipipe-page-for-skill` as source 2, with an instruction to check the target filename before writing a word.
      On 260802 the six writers only used that variant because the caller named it by hand in every packet, which is exactly the copied-checklist dependency this agent's own contract forbids.

## States
It ran for the first time on 260802 and the fan-out worked: six fresh writers, six pages, no scope collision, and the shared writes stayed with the caller as designed.
Its RUN producer half ran for the first time on 260805: the QB8e RUN dispatched this charter for both REVISE phases, as fresh-context `claude -p` subprocesses, and each produced version returned to a fresh judge with zero mechanical findings (receipt `_runs/page/QB8e/260805-0216-QB8e.json`).
Its health is `🟡 in flux` because that first run also exposed two gaps it had no way to show while it had never run.

- 260802 CC · 🧪 The first real fan-out, and what it proved
  Six agents revised six roster Openings at once, each holding one file, none reading a sibling, none holding Bash.
  The concurrency boundary held exactly as `QC1b` §4.2 predicted: one page's `.md` fans out, and `board.md`, the rebuild and the checker stayed with the caller.
  What it did not prove is throughput, because nobody measured the serial alternative.
- 260802 CC · 🩹 Three of six died on a session limit, and only luck made that safe
  Each had already written its page before the limit hit, so the batch completed.
  Had they died a minute earlier the caller would have had three untouched pages and three return contracts it never received, with nothing on disk saying which was which.
- 260802 CC · 📚 The packet carried a rule the agent should have loaded
  Every one of the six packets named `haipipe-page-for-skill` by hand, because the agent's own source list did not mention it.
  This agent's contract forbids exactly that, saying a copied checklist in the packet is not a substitute for loading the skill, so the caller broke the agent's rule to make up for the agent's gap.
  Fixed at 0.4.0. JL found it by asking whether these agents call any skills.

## Log
- 260815 1230 · [REVISE-CC] converted to a for-design page (JL 260815): the three managed spans left the file, `skillpage.py plug` wrote the unit's contract surface to `skill/haipipe-board-creator-agent/`, and Content §2 adopts the selection recorded on the specimen.
- 260806 2116 · [REVISE-CC] swept to the 260806 architecture; authored prose verified clean (skillpage.py sync already current), one unit-side debt recorded: the charter's own source list still says "six Page Types" where haipipe-page 0.21.0 ships ten, and the managed body span mirrors that unit staleness faithfully.
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); the RUN producer half is no longer untried, the QB8e RUN exercised it for both REVISE phases as fresh-context claude -p subprocesses.
260804 · Expanded the authored mirror from batch-only Page creation to the shared producer role: exactly one DRAFT, PROBE, or REVISE authority per RUN receipt, still with no rebuild or CHECK.
260731 · The concurrency boundary was JL's ruling that day: the test is not whether a unit has its own trigger but whether a write touches a file another writer also touches
260802 2100 · Synced to 0.4.0 and the authored half updated after its first real fan-out: six writers, six pages, no scope collision, three killed by a session limit after writing. The agent now loads `haipipe-page-for-skill` itself instead of depending on the caller naming it in the packet, which its own contract forbids
260802 1720 · Health ruled from evidence rather than left as a placeholder Aim: `state:` moved from 🔴 to 🟡 in flux, because the unit is written and registered at 0.3.0 and has never been dispatched. The `🧠 Rule this skill's health` row was removed, since the three Aims below it are the real work
260731 1530 · page generated from `board/agents/haipipe-board-creator-agent.md/` by `skillpage.py new`

