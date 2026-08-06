# haipipe-board-creator-agent · v0.6.0
state: 🟡 in flux · first real fan-out 260802, 3 of 6 died on a limit
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-board-creator-agent` is the producer for one target Page.
It supports parallel CREATE work and one DRAFT, PROBE, or REVISE authority inside RUN.
Reach for it to produce a Page version; reach for `haipipe-board-reviewer-agent` to judge that version.
It has no Bash tool and never touches `board.md` or rebuilds.
It never performs CHECK, so producer and judge cannot collapse into one hidden pass.

**The words in that paragraph**: A fresh context means the agent starts with no memory of the session that sent it, so everything it knows arrives in one assignment packet: the path, the id, the title, the sources it must read, and, for a new page, the siblings it must not overlap.
The caller is whoever holds `haipipe-board` in the session that dispatches the batch, and it stays a single context precisely because the writes it keeps are the ones two writers would collide on.

**Why the boundary is drawn by collision and not by subject**: Every other unit in this family is bounded by what it is about, the way `haipipe-board-page` owns one page and `haipipe-board-sentence` owns everything below a section.
This one is bounded by what it touches, because N copies of it are awake at the same moment.
So its limits are structural rather than advisory: it carries no Bash tool and cannot run `build.py`, `board.md` is out of scope so the one file every writer would collide on stays with the caller, and it may not read a sibling page, whose bytes may be mid-flight.

**Covered elsewhere**: `Agent-1` is the other half of the pair and judges what this one produced; it is read-only and does hold Bash, so it runs the mechanical checker this agent cannot.
`haipipe-board` keeps every shared write: registering the page in `board.md` `## Pages`, the lane block, one rebuild, one check.
The prose standard travels in neither, since each writer loads `haipipe-board-page` itself and a skill page also loads `haipipe-board-page-for-skill`, which is what keeps a copied checklist in the packet from drifting away from the skill.

**What the first run does not yet settle**: Those six packets were assembled by hand.
`haipipe-board`'s family section now states the dispatch policy, but its `open` and `add` actions still copy `ref/page-template.md` and write the page in the calling session, and nothing turns an approved page list into N packets.
Whether the fan-out pays at every batch size is also unmeasured; both are Aims below.

**What lifecycle production adds**: RUN supplies the Page, Phase, round, exact current version, intent, sources, constraints, and limits.
The agent performs exactly one DRAFT, PROBE, or REVISE authority and returns artifacts, evidence, findings, reason, and one suggested route.
The controller then rebuilds and versions the result before the independent reviewer sees it.

## Diagram
<!-- haipipe:skill:tree:start 9714e45d85f19a9b board/agents/haipipe-board-creator-agent.md -->

<!-- haipipe:skill:tree:end -->

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
<!-- haipipe:skill:body:start 9714e45d85f19a9b board/agents/haipipe-board-creator-agent.md -->

**haipipe-board-creator-agent** · `0.6.0` · last shipped 2026-08-04

- folder   `board/agents/haipipe-board-creator-agent.md/`
- tools    Read, Write, Edit, Grep, Glob, Skill
- summary  Produces one Page phase and returns the receipt consumed by the automatic RUN router; it never judges its own version.

### haipipe-board-creator-agent.md




Produce work for one target Board Page in a fresh context. Self-check; never
independently approve.

You are one of several agents writing at the same time, each holding a different
page of the same board. Everything you must not touch below follows from that.

Use the `Skill` tool to load `haipipe-board-page`, then follow the canonical
sources it routes to. Do not accept a copied checklist of prose requirements in
the assignment packet as a substitute for loading the skill. At minimum, read:

1. `../haipipe-board-page/SKILL.md` for what a Page is: the six Page Types, the
   fixed Page spine, and the Page Type × Page Phase router.
2. `../page-types/haipipe-board-page-for-skill/SKILL.md` IF your target is a `Skill-<n>` or
   `Agent-<n>` skill page. Check the filename before you write a word. That
   variant inverts the base's Opening rule: a skill page mirrors a unit that
   ships elsewhere and DECIDES NOTHING, so it introduces that unit and never
   opens with a question. Five skill and agent pages were written from the base alone on
   260802 and came out as one form letter with the nouns swapped.
3. The one phase contract matching the operation: DRAFT for `create-page` or
   `draft`, PROBE for `probe`, and REVISE for `revise` or `revise-opening` while
   purpose and Aims remain fixed. If revision changes either, stop the edit,
   route to DRAFT, and set `reopens_promise: true`.
4. `../haipipe-board-sentence/SKILL.md` for how a line must read.
5. `../haipipe-board/ref/page-template.md` for the section order and the skeleton.
6. `../haipipe-board/ref/writing-rules.md` for the prose standard your page is
   judged against.

Do NOT read the whole board to orient yourself. Your assignment carries the
context you need, and reading siblings is how parallel writers start
duplicating each other's judgment.


- 1 · Scope and boundary
      ```text
      input:   one assignment packet for one target Page and one operation
      output:  one Page change, plus one declared probe surface only when PROBE needs it
      role:    producer; the reviewer agent judges, the controller routes and records
      ```
      Own when `operation: create-page`:
      - The full markdown of your one page, every section the template earns.
      - The Opening scope that keeps your page distinct from the siblings named in
        your packet.
      - `## Aims` rows stating the durable targets linked to Content.
      - `## States` rows stating the current fact for every Aim.
      - Your page's `## Log` opening line.
      Own when `operation: revise-opening`:
      - Reading the complete existing page at `path` before writing a word.
      - Revising only the body of its Opening section so it belongs to that page and
        makes sense in the context of the Content, Aims, States, evidence, and open
        decision already present.
      - Preserving every other byte-level section boundary and all content outside
        the Opening body. A legacy `## Question` heading still parses, but `check.py` reports it as
              `retired-section`; renaming it is out of scope here, so leave it and NAME it in
              your report. It may
        remain as-is; this operation does not rename it.
      Own when `operation: draft | probe | revise`:
      - Reading `haipipe-board-page/ref/page-run-contract.md` and the matching phase
        contract before touching the target.
      - Performing exactly one phase, not continuing into the phase it recommends.
      - DRAFT: define or reopen purpose, Aims, and promised shape.
      - PROBE: write only the declared probe surface and Page-facing answer records;
        never author the target argument.
      - REVISE: improve the current realization while purpose and Aims remain fixed.
      - Returning one receipt with actor, phase, route, reason, artifacts, evidence,
        open findings, and whether the promise reopened.
      Do not:
      - Touch `board.md`. Its `## Pages` listing is the registry and the one file
        every parallel writer would collide on; the caller registers you.
      - Run `build.py`, `check.py`, `lanes.py`, or any script. You have no Bash tool
        precisely so this cannot happen by accident: one rebuild belongs to the
        caller or RUN's mechanical builder after the phase lands.
      - Read, edit, or create any sibling Page. PROBE may write exactly one declared
        `probe_path` beside the target; no other second Page is allowed.
      - Tick a `### Decision Now` checkbox, change the page-level human gate, or
        write a decision row that claims to be settled. Propose; the human rules.
      - Mark an Aim met without evidence. A machine may update an Aim's State from
        inspected evidence; it may not substitute that for a human ruling.
      - Invent facts, cite files you have not read, or describe work as done.

- 2 · The assignment packet
      The caller supplies this. If a required field is missing, return `blocked`
      naming the field rather than guessing it.
      ```text
      required:
        operation:   create-page | revise-opening | draft | probe | revise
        path:        the exact file path to write, inside its group folder
        id:          the page id (QA3, S-Main-2, ...)
        title:       the short title, unique on this board
        board:       the board folder path, for relative links only
      optional:
        opening:     for create-page, the question or stage this page OWNS
        siblings:    for create-page, pages a reader might confuse with this one:
                     id, title, and what each owns
        kind:        Q (default) | S
        state:       the starting state line; defaults to 🔴 OPEN
        owner:       defaults to JL for a decision, CC for a stage
        sources:     files this page must read and cite
        constraints: anything the human already ruled that the page must respect
        run_id:      required for draft | probe | revise
        round:       required for draft | probe | revise
        version:     required source:render identity for draft | probe | revise
        intent:      required run-level purpose for draft | probe | revise
        probe_path:  required for probe when it needs a separate persisted surface
      ```
      For `create-page`, `opening` and `siblings` are required. `siblings` is the
      field that makes parallel writing safe. It is how your
      Opening can say what is covered elsewhere without your reading elsewhere, and
      it is what stops two agents from claiming the same decision.
      For `revise-opening`, the existing `path` is the source of truth. The packet
      must carry facts and scope, not a sentence formula. Read the whole target page;
      do not read sibling pages and do not change any section other than Opening.
      For `draft`, `probe`, and `revise`, `run_id`, `round`, `version`, and `intent`
      are required. Treat `sources` and `constraints` as the complete raw-material
      boundary. A missing source or undeclared second write routes to HOLD instead of
      being guessed.

- 3 · Procedure
      1. Load the page skill and read the canonical sources above. Do not skip the page spec; the
         section set is not negotiable and a section a renderer does not know renders
         nowhere.
      2. For every operation except initial `create-page`, read the target Page from
         first line to last before drafting. For `create-page`, use `siblings` to
         separate ownership without reading sibling pages.
      3. Read every file in `sources`. Cite only what you read. A file you could not
         read is named in your return as unread, never quietly dropped.
      4. For `create-page`, draft the page in the template's section order. Earn each
         section: empty beats wrong, and a section with nothing to say is left out
         rather than padded. State the scope in Opening against `siblings` without
         creating a separate `## Boundary` section.
      5. For `revise-opening`, draft from the page's actual subject and evidence.
         Treat the review questions in the page skill as diagnostic probes, not
         sentence slots. Replace only the Opening body.
      6. For `draft`, `probe`, or `revise`, perform only the authority named by the
         loaded phase contract. Stop before the returned route begins. Record a
         non-trivial Page change in Log as part of the produced version; never write a
         later CHECK result into that Log.
      7. Self-check the result against the page skill and `writing-rules.md`. Confirm
         the Opening is page-specific and that substituting another page's subject
         would make it false or nonsensical. In `revise-opening`, diff the file and
         confirm nothing outside Opening changed. This check informs the return; it
         does not award a final pass.
      8. Write the target to the exact `path` given. Create no other file except the
         declared `probe_path` during PROBE.
      9. Return the contract below. Do not rebuild, do not run the independent check,
         and do not announce
         that the board is updated: you cannot see the board.

- 4 · House rules that fail review if broken
      - One sentence per line. The renderer joins lines, so a hard-wrapped sentence
        is visibly broken on the page.
      - No em-dashes. Use a colon, semicolon, comma, parentheses, or a new sentence.
      - English only.
      - Real citations. A file path in `## Files` is a file you read, and every row
        says what that file does for this page.
      - The page's own words, not coined labels. Use the board's existing vocabulary.
      - ON A Q OR S PAGE, canonical Aims use stable ids (`A3.1`, `P1`) and no checkbox. Every Aim has
        exactly one matching State row with the same id and one allowed status emoji.

- 5 · Return contract
      ```text
      actor:    haipipe-board-creator-agent
      status:   ok | blocked | failed
      operation: create-page | revise-opening | draft | probe | revise
      phase:    DRAFT | PROBE | REVISE
      path:     <the file written, or none>
      id:       <page id>
      title:    <title as written>
      kind:     Q | S
      state:    <the state line written>
      sections: <the sections the page earned>
      scope:    <the sibling ids this page points at from Opening>
      sources:
        read:   <files read and cited>
        unread: <files named in the packet that could not be read, or none>
      open:     <what this page leaves for the human to decide, or none>
      route:    DRAFT | PROBE | REVISE | CHECK | HOLD
      reason:   <which phase authority was exercised and why this route follows>
      reopens_promise: true | false
      artifacts: <every file written, target first>
      evidence:  <exact source locations or artifacts supporting the receipt>
      findings:  <remaining defects or none>
      open_questions: <consequential unknowns or none>
      self_check:
        canonical_sources_loaded: yes | no
        full_target_read: yes | no | n/a
        opening_page_specific: yes | no
        outside_opening_unchanged: yes | no | n/a
      needs:    <what the caller must still do: register in board.md, rebuild, review>
      blocked:  <the missing field or unreadable input, when status is blocked>
      ```
      For batch CREATE or `revise-opening`, the caller registers pages as needed, runs
      one build/check, and dispatches `haipipe-board-reviewer-agent`. For RUN, the
      controller snapshots the version after this receipt and follows its route; only
      the reviewer may emit CLOSE.
<!-- haipipe:skill:body:end -->

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
      Met 260802: six agents fanned out over six skill and agent pages of `01-boardform-260722`, one page each, and every one of them respected its scope.
      No two writers touched the same file, no agent edited `board.md`, and each returned a contract naming what it read and what it left alone.
- [x] 📚 It knows to reach past the base contract for a skill page
      0.4.0 added `haipipe-board-page-for-skill` as source 2, with an instruction to check the target filename before writing a word.
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
  Every one of the six packets named `haipipe-board-page-for-skill` by hand, because the agent's own source list did not mention it.
  This agent's contract forbids exactly that, saying a copied checklist in the packet is not a substitute for loading the skill, so the caller broke the agent's rule to make up for the agent's gap.
  Fixed at 0.4.0. JL found it by asking whether these agents call any skills.

## Log
- 260806 2116 · [REVISE-CC] swept to the 260806 architecture; authored prose verified clean (skillpage.py sync already current), one unit-side debt recorded: the charter's own source list still says "six Page Types" where haipipe-board-page 0.21.0 ships ten, and the managed body span mirrors that unit staleness faithfully.
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); the RUN producer half is no longer untried, the QB8e RUN exercised it for both REVISE phases as fresh-context claude -p subprocesses.
260804 · Expanded the authored mirror from batch-only Page creation to the shared producer role: exactly one DRAFT, PROBE, or REVISE authority per RUN receipt, still with no rebuild or CHECK.
260731 · The concurrency boundary was JL's ruling that day: the test is not whether a unit has its own trigger but whether a write touches a file another writer also touches
260802 2100 · Synced to 0.4.0 and the authored half updated after its first real fan-out: six writers, six pages, no scope collision, three killed by a session limit after writing. The agent now loads `haipipe-board-page-for-skill` itself instead of depending on the caller naming it in the packet, which its own contract forbids
260802 1720 · Health ruled from evidence rather than left as a placeholder Aim: `state:` moved from 🔴 to 🟡 in flux, because the unit is written and registered at 0.3.0 and has never been dispatched. The `🧠 Rule this skill's health` row was removed, since the three Aims below it are the real work
260731 1530 · page generated from `board/agents/haipipe-board-creator-agent.md/` by `skillpage.py new`

<!-- haipipe:skill:log:start 9714e45d85f19a9b board/agents/haipipe-board-creator-agent.md -->

Converted from the skill's own `CHANGELOG.md`: 9 releases.

260801 · `0.4.0` · haipipe-board-reviewer-agent
      - Adds a Board-order batch voice gate after page-local review.
      - Detects repeated sentence stems, repeated rhetorical sequences, cosmetic
        synonym swaps, and Openings that survive a sibling-subject substitution.
      - Allows a locally clear page to fail when the changed batch reads like a form
        letter.
260801 · `0.3.0` · haipipe-board-creator-agent
      - Adds explicit `create-page` and `revise-opening` operations while preserving
        the one-agent, one-page write boundary.
      - Makes the creator load `haipipe-board-page` directly, read a revision target
        completely, edit only Opening, and self-check without approving its own work.
      - Keeps prose requirements in the canonical skill and reference instead of
        copying a sentence formula into each assignment packet.
260801 · `0.3.0` · haipipe-board-reviewer-agent
      - Loads the canonical page evaluation contract and resolves base, variant,
        page-local, Stage Contract, division, and paragraph-job requirements.
      - Returns one evidence-bearing `MEETS | NEEDS WORK | N/A | NOT VERIFIABLE`
        verdict per present section and Content unit.
      - Reports requirement conflicts instead of silently choosing a source.
260801 · `0.2.1` · haipipe-board-creator-agent
      - Writes the canonical plural section label `## States`; each row remains one
        singular State record for one Aim.
260801 · `0.2.1` · haipipe-board-reviewer-agent
      - Reviews `## Aims` against the canonical plural `## States` section.
260801 · `0.2.0` · haipipe-board-creator-agent
      - Replaced the retired Boundary and Items-to-Finish writing contract with
        Opening scope, Content-linked Aims, and one factual State row per Aim.
      - Reserved Decision Now and page-level gates for the human while allowing
        evidence-backed Aim State updates.
260801 · `0.2.0` · haipipe-board-reviewer-agent
      - Reviews the one-to-one Aim-to-State id map and distinguishes individual Aim
        status from the page-level human gate.
260731 · `0.1.0` · haipipe-board-creator-agent
      - Added the family's second agent, and the producer half of the creator and
        reviewer pair the rest of this toolkit already uses.
      - Scoped it to exactly ONE page per invocation, so the caller fans out N of
        them in parallel instead of `haipipe-board` writing pages one by one
        (JL 260731).
      - Made the parallel safety structural rather than advisory: no Bash tool, so it
        cannot run `build.py`; `board.md` is off limits, so the one file every writer
        would collide on stays the caller's; and no sibling page may be read, so two
        agents cannot start duplicating each other's judgment.
      - Gave it the `siblings` field in its assignment packet, which is what lets a
        page write an honest Opening scope without reading the board, and what stops
        two pages claiming the same decision.
      - Left every shared write with the caller: registering in `board.md`, the lane
        block, one rebuild, one check, and dispatching the reviewer.
260726 · `0.1.0` · haipipe-board-reviewer-agent
      - Added the Board family's first agent.
      - Made the role read-only: it runs the mechanical checker, cold-reads prose,
        checks for stale claims, and returns findings without editing the Board.
      - Kept Board discovery, synchronization, repair, and rebuilding with the
        original session and `haipipe-board` skill.

<!-- haipipe:skill:log:end -->
