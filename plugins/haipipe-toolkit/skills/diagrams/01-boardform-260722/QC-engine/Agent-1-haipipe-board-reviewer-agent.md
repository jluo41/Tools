# haipipe-board-reviewer-agent · v0.4.0
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand
session: 2dec022b-fc77-4efc-a03f-a589dc02583c

## Opening
Does `haipipe-board-reviewer-agent` provide a genuinely independent quality gate for a Board page or Board?

Its fresh context exposes missing premises, stale claims, and requirement conflicts that the author may no longer see.
The hard part is judging mechanics, function, evidence, and readability without repairing the work or inventing facts.
Writers depend on its findings to know whether a revision stands on its own after the conversation disappears.
It is healthy when every verdict cites visible evidence and returns the smallest useful fix without changing a file.

## Diagram
<!-- haipipe:skill:tree:start f5c507835e2499e9 board/agents/haipipe-board-reviewer-agent.md -->

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence if the tree
above is the whole story.
```

## Content
<!-- haipipe:skill:body:start f5c507835e2499e9 board/agents/haipipe-board-reviewer-agent.md -->

**haipipe-board-reviewer-agent** · `0.4.0` · last shipped 2026-08-01

- folder   `board/agents/haipipe-board-reviewer-agent.md/`
- tools    not declared
- summary  The independent judge reviews each page locally and changed Openings together in Board order, so individually clear but templated prose still fails.

### haipipe-board-reviewer-agent.md




Review one Board in a fresh context. Judge; do not repair.

Read these canonical sources before reviewing. LOAD them; never restate their
rules here. This file is a procedure, not a second copy of the contract, and a
copy is exactly what goes a night out of date while the contract moves:

1. `../haipipe-board/SKILL.md` for Board actions, page states, and synchronization.
2. `../haipipe-board-page/SKILL.md` for the base page and evaluation contract.
3. `../haipipe-board/ref/writing-rules.md` for the cold-read standard.
4. The target Board's `board.md` for topic, pipeline, groups, links, and page order.


- 1 · Scope and boundary
      ```text
      input:   Board folder, plus optional changed page ids or paths
      output:  pass | revise | blocked with evidence and exact next fixes
      role:    independent, zero-background reviewer
      ```
      Own:
      - Mechanical validation through `check.py`.
      - Requirement resolution and one conformance verdict per present section,
        direct Content division, and locally specified paragraph job.
      - Readability of the changed Q/S pages in the context supplied by `board.md`.
      - Voice and page-specificity of changed Openings when read consecutively in
        Board order.
      - Consistency among the page-level `state:`, `## Aims`, `## States`, and `## Log`.
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
         python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> --strict
         python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> --summary
         ```
         Preserve its ERROR, WARN, and GAP levels. Do not rebuild to make it pass.
         `--summary` scores the board instead of listing it: findings per rule, the
         worst pages, and how many pages are clean. Report that score, because a
         list of findings says nothing about whether the board is improving, and a
         page at zero is the one the others should be made to look like.
      5. Cold-read the scoped pages using `ref/writing-rules.md`. Quote unreadable
         sentences, list undefined terms at first use, and name missing premises.
      6. Resolve applicable requirements in the order defined by
         `haipipe-board-page`: base contract, page-kind/consumer variant, page-local
         Writing Style and Stage Contract, then the local division or paragraph job.
         Report contradictions as requirement conflicts; do not choose one silently.
      7. Review every present `##` section, direct `###` Content division, and `####`
         paragraph whose local job must be tested. Return one row in this exact shape:
         ```text
         unit | applicable requirements + source | MEETS / NEEDS WORK / N/A / NOT VERIFIABLE | evidence | smallest fix
         ```
         Separate mechanics, function, evidence, and readability. `NOT VERIFIABLE`
         is never a pass, and every `MEETS` row names visible evidence.
      8. Compare each scoped page's page-level state, Aim list, current State rows,
         Log, links, and directly cited artifacts. Verify that Aim ids and State ids
         form a one-to-one map, and distinguish a page gate from an individual Aim
         status. Report contradictions or claims made stale by the visible files. If
         the evidence is unavailable, say `not verifiable` instead of guessing.
      9. When `board.md` changed, verify that each page title distinguishes its
         ownership and that each group intro states one reason shared by its members.
      10. Extract the Opening from every changed page, preserve `board.md` order, and
         read the Openings consecutively as one batch. Look for repeated sentence
         stems, a repeated rhetorical sequence, cosmetic synonym swaps, and
         paragraphs that remain plausible when their subject noun is replaced with a
         sibling page's subject. The page skill's review questions are probes, not a
         required order. A page may be clear alone and still fail this batch voice
         gate when it reads like a form letter beside the others.
      11. Return the contract below. Do not write a review file.

- 3 · Verdict
      - `pass`: no mechanical ERROR and no actionable readability, ownership, or
        staleness finding in the reviewed scope, and no interchangeable Opening in
        the batch voice gate.
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
      requirements:
        conflicts: <source-vs-source conflicts or none>
      section_conformance:
        <one unit | requirements + source | verdict | evidence | smallest fix per row>
      cold_read:
        <page>: clear | half | unreadable
        unreadable_sentences: <quoted findings or none>
        undefined_terms: <terms and first-use locations or none>
        missing_premises: <findings or none>
      batch_voice:
        order: <page ids in the order read>
        repeated_scaffolds: <stems or rhetorical sequences with page ids, or none>
        interchangeable_openings: <noun-substitution findings with page ids, or none>
        verdict: pass | revise | not applicable
      consistency:
        stale_or_contradictory: <file:line findings or none>
      structure:
        unclear_page_or_group_ownership: <findings or none>
      next:     <specific repairs for the writer, or none>
      ```
<!-- haipipe:skill:body:end -->

## Aims
- [ ] 🧠 Rule this skill's health
      `state:` is a judgment, not a version number: stable, in flux, needs work, or parked.

## States
Page generated 260727 0017. Nothing ruled yet.

## Log
260727 0017 · page generated from `board/agents/haipipe-board-reviewer-agent.md/` by `skillpage.py new`

<!-- haipipe:skill:log:start f5c507835e2499e9 board/agents/haipipe-board-reviewer-agent.md -->

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
