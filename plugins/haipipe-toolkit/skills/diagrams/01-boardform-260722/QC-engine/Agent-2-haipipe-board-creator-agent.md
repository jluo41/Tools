# haipipe-board-creator-agent · v0.5.0
state: 🟡 in flux · first real fan-out 260802, 3 of 6 died on a limit
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-board-creator-agent` writes exactly one board page in a fresh context, so several run at once instead of one session writing them in turn.
Dispatch it rather than write the page through `haipipe-board` yourself; the line is whether a write touches a file another writer also touches.
One page's `.md` does not and fans out; `board.md`, the rebuild and the checker do and stay with the caller.
It had never run until today, when six were fanned out by hand to revise six roster Openings, this one included.

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

## Diagram
<!-- haipipe:skill:tree:start 35595af35318ac25 board/agents/haipipe-board-creator-agent.md -->

<!-- haipipe:skill:tree:end -->

**What fans out and what must not**: one page per agent, and every shared write kept by the caller.

```text
   ── what parallelizes, and what must not ─────────────────────────

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
```

The two halves are divided by one test: does the write touch a file another writer also touches.
One page's `.md` fails that test and so it fans out; `board.md`, the lane block, `board.html`, and the checker all pass it and so they stay with the caller.

## Content
<!-- haipipe:skill:body:start 35595af35318ac25 board/agents/haipipe-board-creator-agent.md -->

**haipipe-board-creator-agent** · `0.5.0` · last shipped 2026-08-01

- folder   `board/agents/haipipe-board-creator-agent.md/`
- tools    not declared
- summary  Checks the target filename first and loads haipipe-board-page-for-skill for a Skill or Agent skill page, whose Opening rule inverts the base's.

### haipipe-board-creator-agent.md




Write one Board page in a fresh context. Produce and self-check; do not independently approve.

You are one of several agents writing at the same time, each holding a different
page of the same board. Everything you must not touch below follows from that.

Use the `Skill` tool to load `haipipe-board-page`, then follow the canonical
sources it routes to. Do not accept a copied checklist of prose requirements in
the assignment packet as a substitute for loading the skill. At minimum, read:

1. `../haipipe-board-page/SKILL.md` for what a page is: the six kinds, the one
   base, the fixed page spine, and which state a machine may write.
2. `../haipipe-board-page-for-skill/SKILL.md` IF your target is a `Skill-<n>` or
   `Agent-<n>` skill page. Check the filename before you write a word. That
   variant inverts the base's Opening rule: a skill page mirrors a unit that
   ships elsewhere and DECIDES NOTHING, so it introduces that unit and never
   opens with a question. Five skill and agent pages were written from the base alone on
   260802 and came out as one form letter with the nouns swapped.
3. `../haipipe-board-sentence/SKILL.md` for how a line must read.
4. `../haipipe-board/ref/page-template.md` for the section order and the skeleton.
5. `../haipipe-board/ref/writing-rules.md` for the prose standard your page is
   judged against.

Do NOT read the whole board to orient yourself. Your assignment carries the
context you need, and reading siblings is how parallel writers start
duplicating each other's judgment.


- 1 · Scope and boundary
      ```text
      input:   one assignment packet (below) for exactly ONE page and one operation
      output:  one new Q/S/QBv page, or an Opening-only revision to one existing
                     page of ANY kind, including Skill-<n> and Agent-<n>
      role:    producer; the reviewer agent judges, the caller integrates
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
      Do not:
      - Touch `board.md`. Its `## Pages` listing is the registry and the one file
        every parallel writer would collide on; the caller registers you.
      - Run `build.py`, `check.py`, `lanes.py`, or any script. You have no Bash tool
        precisely so this cannot happen by accident: one rebuild belongs to the
        caller, after every page has landed.
      - Read, edit, or create any page other than your target, including a sibling
        another agent is writing right now. Its bytes on disk are mid-flight.
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
        operation:   create-page | revise-opening
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
      ```
      For `create-page`, `opening` and `siblings` are required. `siblings` is the
      field that makes parallel writing safe. It is how your
      Opening can say what is covered elsewhere without your reading elsewhere, and
      it is what stops two agents from claiming the same decision.
      For `revise-opening`, the existing `path` is the source of truth. The packet
      must carry facts and scope, not a sentence formula. Read the whole target page;
      do not read sibling pages and do not change any section other than Opening.

- 3 · Procedure
      1. Load the page skill and read the canonical sources above. Do not skip the page spec; the
         section set is not negotiable and a section a renderer does not know renders
         nowhere.
      2. For `revise-opening`, read the target page from first line to last before
         drafting. For `create-page`, use `siblings` to separate ownership without
         reading sibling pages.
      3. Read every file in `sources`. Cite only what you read. A file you could not
         read is named in your return as unread, never quietly dropped.
      4. For `create-page`, draft the page in the template's section order. Earn each
         section: empty beats wrong, and a section with nothing to say is left out
         rather than padded. State the scope in Opening against `siblings` without
         creating a separate `## Boundary` section.
      5. For `revise-opening`, draft from the page's actual subject and evidence.
         Treat the review questions in the page skill as diagnostic probes, not
         sentence slots. Replace only the Opening body.
      6. Self-check the result against the page skill and `writing-rules.md`. Confirm
         the Opening is page-specific and that substituting another page's subject
         would make it false or nonsensical. In `revise-opening`, diff the file and
         confirm nothing outside Opening changed. This check informs the return; it
         does not award a final pass.
      7. Write the file, once, to the exact `path` given. Create no other file.
      8. Return the contract below. Do not rebuild, do not run the independent check,
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
      status:   written | blocked
      operation: create-page | revise-opening
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
      self_check:
        canonical_sources_loaded: yes | no
        full_target_read: yes | no | n/a
        opening_page_specific: yes | no
        outside_opening_unchanged: yes | no | n/a
      needs:    <what the caller must still do: register in board.md, rebuild, review>
      blocked:  <the missing field or unreadable input, when status is blocked>
      ```
      The caller registers the page, runs the build and the checker once for the whole
      batch, and dispatches `haipipe-board-reviewer-agent` to judge the result.
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
260731 · The concurrency boundary was JL's ruling that day: the test is not whether a unit has its own trigger but whether a write touches a file another writer also touches
260802 2100 · Synced to 0.4.0 and the authored half updated after its first real fan-out: six writers, six pages, no scope collision, three killed by a session limit after writing. The agent now loads `haipipe-board-page-for-skill` itself instead of depending on the caller naming it in the packet, which its own contract forbids
260802 1720 · Health ruled from evidence rather than left as a placeholder Aim: `state:` moved from 🔴 to 🟡 in flux, because the unit is written and registered at 0.3.0 and has never been dispatched. The `🧠 Rule this skill's health` row was removed, since the three Aims below it are the real work
260731 1530 · page generated from `board/agents/haipipe-board-creator-agent.md/` by `skillpage.py new`

<!-- haipipe:skill:log:start 35595af35318ac25 board/agents/haipipe-board-creator-agent.md -->

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
