# haipipe-board-creator-agent · v0.3.0
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
Can `haipipe-board-creator-agent` write one complete page in parallel without touching anything another writer owns?

One fresh writer per page keeps a large Board from becoming a long serial drafting session.
The hard part is preventing overlap while each agent lacks the sibling context and shared registry it would normally inspect.
The caller must keep every shared write, then integrate the batch once and send it to an independent reviewer.
It is healthy when a real multi-page batch passes review without hand-repairing scope collisions.

## Diagram
<!-- haipipe:skill:tree:start 136b101435f5f8d7 board/agents/haipipe-board-creator-agent.md -->

<!-- haipipe:skill:tree:end -->

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
<!-- haipipe:skill:body:start 136b101435f5f8d7 board/agents/haipipe-board-creator-agent.md -->

**haipipe-board-creator-agent** · `0.3.0` · last shipped 2026-08-01

- folder   `board/agents/haipipe-board-creator-agent.md/`
- tools    not declared
- summary  One fresh agent owns one page: create it or revise only its Opening, load the page skill directly, then self-check without self-approving.

### haipipe-board-creator-agent.md




Write one Board page in a fresh context. Produce and self-check; do not independently approve.

You are one of several agents writing at the same time, each holding a different
page of the same board. Everything you must not touch below follows from that.

Use the `Skill` tool to load `haipipe-board-page`, then follow the canonical
sources it routes to. Do not accept a copied checklist of prose requirements in
the assignment packet as a substitute for loading the skill. At minimum, read:

1. `../haipipe-board-page/SKILL.md` for what a page is: the three kinds, the one
   base, the fixed page spine, and which state a machine may write.
2. `../haipipe-board-sentence/SKILL.md` for how a line must read.
3. `../haipipe-board/ref/page-template.md` for the section order and the skeleton.
4. `../haipipe-board/ref/writing-rules.md` for the prose standard your page is
   judged against.

Do NOT read the whole board to orient yourself. Your assignment carries the
context you need, and reading siblings is how parallel writers start
duplicating each other's judgment.


- 1 · Scope and boundary
      ```text
      input:   one assignment packet (below) for exactly ONE page and one operation
      output:  one new Q/S page, or an Opening-only revision to one existing Q/S page
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
        the Opening body. A legacy `## Question` heading is an Opening alias and may
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
      - Canonical Aims use stable ids (`A3.1`, `P1`) and no checkbox. Every Aim has
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
- [ ] 🧠 Rule this skill's health
      `state:` is a judgment, not a version number: stable, in flux, needs work, or parked.
- [ ] 🚚 Give the caller its half, in `haipipe-board`
      The agent is written and the fan-out procedure is not: `SKILL.md`'s `open` and `add` actions still describe writing pages themselves, and nothing yet turns an approved proposal table into N assignment packets or performs the serialized tail once.
- [ ] 🧪 Run it on a real multi-page board
      Nothing has been fanned out yet, so the throughput claim in `## Opening` is reasoning rather than evidence, and the `siblings` field is untested against two agents who genuinely could have overlapped.
- [ ] 📐 Decide the batch size ceiling, if there is one
      Eight pages is eight contexts reading the same four specs; whether that is worth it at every size, or only above some count, is unmeasured.

## States
The agent is written and registered; nothing has run through it yet, and the caller's half does not exist.

- 260731 JL · 🤖 Opened on JL's ask for a parallel page writer
  JL: "we should have a new agent named haipipe-board-creator-agent, it can be called to write the pages markdown in parallels, instead of haipipe-board to write each of them one by one".
  The design question that ask contains is which writes may happen at once, and the answer divides on one test: whether a write touches a file another writer also touches.
  One page's `.md` fails that test and fans out; `board.md`, the lane block, the rebuild, and the checker pass it and stay with the caller, which is why this agent has no Bash tool and no claim on the registry.
  It completes the creator and reviewer pair that `Agent-1` started, and that the task and discovery families in this toolkit already run.

## Log
260731 1530 · page generated from `board/agents/haipipe-board-creator-agent.md/` by `skillpage.py new`

<!-- haipipe:skill:log:start 136b101435f5f8d7 board/agents/haipipe-board-creator-agent.md -->

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
