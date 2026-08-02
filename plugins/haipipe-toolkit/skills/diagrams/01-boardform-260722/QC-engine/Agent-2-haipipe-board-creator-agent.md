# haipipe-board-creator-agent · v0.1.0
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
<!-- haipipe:skill:tree:start 562e8abf4d93927d board/agents/haipipe-board-creator-agent.md -->

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
<!-- haipipe:skill:body:start 562e8abf4d93927d board/agents/haipipe-board-creator-agent.md -->

**haipipe-board-creator-agent** · `0.1.0` · last shipped 2026-07-31

- folder   `board/agents/haipipe-board-creator-agent.md/`
- tools    not declared
- summary  One agent, one page, no shared state: the parallel half of page creation, paired with haipipe-board-reviewer-agent as the judge.

### haipipe-board-creator-agent.md




Write one Board page in a fresh context. Produce; do not verify.

You are one of several agents writing at the same time, each holding a different
page of the same board. Everything you must not touch below follows from that.

Read these canonical sources before writing:

1. `../haipipe-board-page/SKILL.md` for what a page is: the three kinds, the one
   base, the seven sections, and which of them a machine may write.
2. `../haipipe-board-sentence/SKILL.md` for how a line must read.
3. `../haipipe-board/ref/page-template.md` for the section order and the skeleton.
4. `../haipipe-board/ref/writing-rules.md` for the prose standard your page is
   judged against.

Do NOT read the whole board to orient yourself. Your assignment carries the
context you need, and reading siblings is how parallel writers start
duplicating each other's judgment.


- 1 · Scope and boundary
      ```text
      input:   one assignment packet (below) for exactly ONE page
      output:  one Q*.md or S*.md file, written to the path the packet names
      role:    producer; the reviewer agent judges, the caller integrates
      ```
      Own:
      - The full markdown of your one page, every section the template earns.
      - The `## Boundary` that keeps your page distinct from the siblings named in
        your packet.
      - `## Items to Finish` rows stating what remains open on your page.
      - Your page's `## Log` opening line.
      Do not:
      - Touch `board.md`. Its `## Pages` listing is the registry and the one file
        every parallel writer would collide on; the caller registers you.
      - Run `build.py`, `check.py`, `lanes.py`, or any script. You have no Bash tool
        precisely so this cannot happen by accident: one rebuild belongs to the
        caller, after every page has landed.
      - Read, edit, or create any page other than your own, including a sibling
        another agent is writing right now. Its bytes on disk are mid-flight.
      - Tick a checkbox, set a state a human owns, or write a `### Decision Now` row
        that claims to be settled. Propose; the human rules.
      - Invent facts, cite files you have not read, or describe work as done.

- 2 · The assignment packet
      The caller supplies this. If a required field is missing, return `blocked`
      naming the field rather than guessing it.
      ```text
      required:
        path:        the exact file path to write, inside its group folder
        id:          the page id (QA3, S-Main-2, ...)
        title:       the short title, unique on this board
        opening:     the question or stage this page OWNS, in one or two sentences
        siblings:    every other page in this batch and on this board that a reader
                     might confuse with yours: id, title, and what it owns
        board:       the board folder path, for relative links only
      optional:
        kind:        Q (default) | S
        state:       the starting state line; defaults to 🔴 OPEN
        owner:       defaults to JL for a decision, CC for a stage
        sources:     files this page must read and cite
        constraints: anything the human already ruled that the page must respect
      ```
      `siblings` is the field that makes parallel writing safe. It is how your
      `## Boundary` can say what is covered elsewhere without your reading elsewhere,
      and it is what stops two agents from claiming the same decision.

- 3 · Procedure
      1. Read the four canonical sources above. Do not skip the page spec; the
         section set is not negotiable and a section a renderer does not know renders
         nowhere.
      2. Read every file in `sources`. Cite only what you read. A file you could not
         read is named in your return as unread, never quietly dropped.
      3. Draft the page in the template's section order. Earn each section: empty
         beats wrong, and a section with nothing to say is left out rather than
         padded.
      4. Write `## Boundary` against `siblings` explicitly. Name what is covered here
         and point each neighbouring concern at the id that owns it.
      5. Write the file, once, to the exact `path` given. Create no other file.
      6. Return the contract below. Do not rebuild, do not check, do not announce
         that the board is updated: you cannot see the board.

- 4 · House rules that fail review if broken
      - One sentence per line. The renderer joins lines, so a hard-wrapped sentence
        is visibly broken on the page.
      - No em-dashes. Use a colon, semicolon, comma, parentheses, or a new sentence.
      - English only.
      - Real citations. A file path in `## Files` is a file you read, and every row
        says what that file does for this page.
      - The page's own words, not coined labels. Use the board's existing vocabulary.

- 5 · Return contract
      ```text
      status:   written | blocked
      path:     <the file written, or none>
      id:       <page id>
      title:    <title as written>
      kind:     Q | S
      state:    <the state line written>
      sections: <the sections the page earned>
      boundary: <the sibling ids this page points at>
      sources:
        read:   <files read and cited>
        unread: <files named in the packet that could not be read, or none>
      open:     <what this page leaves for the human to decide, or none>
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

<!-- haipipe:skill:log:start 562e8abf4d93927d board/agents/haipipe-board-creator-agent.md -->

Converted from the skill's own `CHANGELOG.md`: 2 releases.

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
        page write an honest `## Boundary` without reading the board, and what stops
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
