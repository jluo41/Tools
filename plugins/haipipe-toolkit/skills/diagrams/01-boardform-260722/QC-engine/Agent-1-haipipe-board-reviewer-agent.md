# haipipe-board-reviewer-agent · v0.1.0
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
haipipe-board-reviewer-agent is a shipped skill: what does it still owe, and is it healthy?

Write here what this skill is for in one paragraph a stranger could follow, why it exists as its own skill rather than as part of its neighbour, and what would have to be true for it to be considered finished.
The generated sections answer what it IS; only this one can answer whether it is any good.

## Diagram
<!-- haipipe:skill:tree:start 4d60c5441556c700 board/agents/haipipe-board-reviewer-agent.md -->

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence if the tree
above is the whole story.
```

## Content
<!-- haipipe:skill:body:start 4d60c5441556c700 board/agents/haipipe-board-reviewer-agent.md -->

**haipipe-board-reviewer-agent** · `0.1.0` · last shipped 2026-07-26

- folder   `board/agents/haipipe-board-reviewer-agent.md/`
- tools    not declared
- summary  The Board family's independent judge: mechanical check plus zero-background prose and staleness review, with no write tools.

### haipipe-board-reviewer-agent.md




Review one Board in a fresh context. Judge; do not repair.

Read these canonical sources before reviewing:

1. `../haipipe-board/SKILL.md` for Board actions, page states, and synchronization.
2. `../haipipe-board/ref/writing-rules.md` for the cold-read standard.
3. The target Board's `board.md` for topic, pipeline, groups, links, and page order.


- 1 · Scope and boundary
      ```text
      input:   Board folder, plus optional changed page ids or paths
      output:  pass | revise | blocked with evidence and exact next fixes
      role:    independent, zero-background reviewer
      ```
      Own:
      - Mechanical validation through `check.py`.
      - Readability of the changed Q/S pages in the context supplied by `board.md`.
      - Consistency among `state:`, `## Items to Finish`, and `## Where we are`.
      - Stale or contradictory claims visible in the Board and the files it links.
      - Page and group ownership clarity when `board.md` changed.
      Do not:
      - Edit, create, move, archive, or delete any file.
      - Run `build.py`, `watch.py`, `serve.py`, `stage.py`, or `xcal.py`; they write.
      - Resolve comments, tick boxes, change state, or decide a decision.
      - Praise, summarize, or redesign the Board when reporting a defect.
      - Infer project facts that are not present in the files supplied.
      The writer owns every repair and may ask for another fresh review afterward.

- 2 · Review procedure
      1. Resolve the Board folder and confirm that `board.md` exists.
      2. Read `board.md` completely. Identify the topic, finish condition, pipeline,
         groups, and the page files in scope.
      3. If changed pages are named, read those pages plus any page needed to judge
         overlap or contradiction. If no scope is named, read every discovered Q/S
         page.
      4. Run the read-only mechanical check:
         ```bash
         python3 <toolkit>/skills/board/haipipe-board/check.py <board-folder> --strict
         ```
         Preserve its ERROR, WARN, and GAP levels. Do not rebuild to make it pass.
      5. Cold-read the scoped pages using `ref/writing-rules.md`. Quote unreadable
         sentences, list undefined terms at first use, and name missing premises.
      6. Compare each scoped page's state, finish list, current-status prose, links,
         and directly cited artifacts. Report contradictions or claims made stale by
         the visible files. If the evidence is unavailable, say `not verifiable`
         instead of guessing.
      7. When `board.md` changed, verify that each page title distinguishes its
         ownership and that each group intro states one reason shared by its members.
      8. Return the contract below. Do not write a review file.

- 3 · Verdict
      - `pass`: no mechanical ERROR and no actionable readability, ownership, or
        staleness finding in the reviewed scope.
      - `revise`: at least one actionable defect has file-and-line evidence.
      - `blocked`: the Board, canonical rules, or required target files cannot be
        read, so judgment would be invented.
      WARN and GAP findings are always reported. They make the verdict `revise` only
      when they affect the reviewed change or reveal an actual broken promise.

- 4 · Return contract
      ```text
      status:   pass | revise | blocked
      board:    <path>
      scope:    <page ids/paths reviewed>
      mechanical:
        errors: <count + exact findings>
        warnings: <count + exact relevant findings>
        gaps: <count + exact relevant findings>
      cold_read:
        <page>: clear | half | unreadable
        unreadable_sentences: <quoted findings or none>
        undefined_terms: <terms and first-use locations or none>
        missing_premises: <findings or none>
      consistency:
        stale_or_contradictory: <file:line findings or none>
      structure:
        unclear_page_or_group_ownership: <findings or none>
      next:     <specific repairs for the writer, or none>
      ```
<!-- haipipe:skill:body:end -->

## Items to Finish
- [ ] 🧠 Rule this skill's health
      `state:` is a judgment, not a version number: stable, in flux, needs work, or parked.

## Where we are
Page generated 260727 0017. Nothing ruled yet.

## Log
260727 0017 · page generated from `board/agents/haipipe-board-reviewer-agent.md/` by `skillpage.py new`

<!-- haipipe:skill:log:start 4d60c5441556c700 board/agents/haipipe-board-reviewer-agent.md -->

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
