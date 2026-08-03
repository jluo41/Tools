# haipipe-board-reviewer-agent · v0.6.0
state: 🟡 in question · existence unruled since 260729, never yet dispatched
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand
session: 2dec022b-fc77-4efc-a03f-a589dc02583c

## Opening
This agent is dispatched into a fresh context to judge a board that was just revised, and it is granted no write tool.
Reach for it over the page's own `✅ Quality Check`, which runs the same rubric in the author's session and shares the author's blind spots.
Since 0.4.0 it reads the changed Openings back to back in board order, so a page that is clear alone can still fail beside its siblings.
That pass has never run on a real batch, and this unit's own existence has been unruled since 260729.

**Why it has to be a stranger**: a writer who has just finished a revision knows what they meant, so they cannot see the premise the page never states.
A fresh dispatch has only the files, which is the position every later reader is in.

**What one dispatch returns**: `pass`, `revise`, or `blocked`, with one row per reviewed unit carrying the requirements it was judged against, the verdict, the evidence, and the smallest fix.
It runs `check.py --strict` and `--summary` itself, so the mechanical findings and the prose findings arrive in one report.
`NOT VERIFIABLE` is one of its four verdicts and never counts as a pass.

**Covered elsewhere**: `check.py` is the deterministic half and says nothing about whether prose reads.
`haipipe-board-creator-agent` writes a page and leaves dispatching this reviewer to the caller.
Whether this unit stays at all is a decision row on `QC1b`, and this page's Aims carry what the unit still owes.

## Diagram
<!-- haipipe:skill:tree:start 0cc451fad22069bb board/agents/haipipe-board-reviewer-agent.md -->

<!-- haipipe:skill:tree:end -->

**One dispatch, three passes, no write tool**: what it loads, what it judges, and the verdict it returns.

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
        │     haipipe-board-page/SKILL.md   the base page contract
        │     haipipe-board-page-for-skill/  the SKILL-PAGE variant, when the
        │                                    page under review is Skill-/Agent-
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
  writes   NOTHING: no markdown, no rebuild, no state, no decision
           it has no write tools at all, so the rule is enforced
           rather than promised

  ⚠️ its own existence is the open question: JL said "don't need to
     have the review agent, stop it" on 260729 while one dispatch was
     running, and nobody has confirmed whether that retired the unit
     or only that run. The row is on QC1b's Decision Now.
```

## Content
<!-- haipipe:skill:body:start 0cc451fad22069bb board/agents/haipipe-board-reviewer-agent.md -->

**haipipe-board-reviewer-agent** · `0.6.0` · last shipped 2026-08-01

- folder   `board/agents/haipipe-board-reviewer-agent.md/`
- tools    not declared
- summary  Loads haipipe-board-page-for-skill whenever a page under review is a Skill or Agent skill page, whose Opening rule inverts the base's.

### haipipe-board-reviewer-agent.md




Review one Board in a fresh context. Judge; do not repair.

Read these canonical sources before reviewing. LOAD them; never restate their
rules here. This file is a procedure, not a second copy of the contract, and a
copy is exactly what goes a night out of date while the contract moves:

1. `../haipipe-board/SKILL.md` for Board actions, page states, and synchronization.
2. `../haipipe-board-page/SKILL.md` for the base page and evaluation contract.
3. `../haipipe-board-page-for-skill/SKILL.md` WHENEVER a page under review is a
   `Skill-<n>` or `Agent-<n>` skill page. It is the variant those two kinds are
   judged against, and its Opening rule is the OPPOSITE of the base's: a roster
   page mirrors a unit that ships elsewhere and decides nothing, so it must
   INTRODUCE that unit and may never open with a question. Judging a skill page
   by the base alone marks correct prose as wrong and passes the form letter this
   variant exists to catch.
4. `../haipipe-board/ref/writing-rules.md` for the cold-read standard.
5. The target Board's `board.md` for topic, pipeline, groups, links, and page order.


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
         form a one-to-one map ON A Q OR S PAGE, and distinguish a page gate from an individual Aim
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
- [ ] 🤖 Whether "don't need to have the review agent" retired the unit is ruled
      It was said on 260729 while one dispatch was running, so it may mean that run or the whole agent.
      Three written things go stale together if it meant the unit: `haipipe-board`'s writing rule 3, `QF1`'s acceptance half, and this page's own skill page.
      The row is on `QC1b`'s Decision Now and nothing here restates its options.
- [ ] 🧑‍⚖️ It reads the eight roster Openings consecutively
      That pass is the reason 0.4.0 exists, it has never run on a real batch, and there is now a real batch waiting: eight roster Openings rewritten on 260802, seven of them the same afternoon.
      This is the one check `haipipe-board-page-for-skill` names as decisive and says the author cannot perform.
- [x] 📚 It knows to reach past the base contract for a skill page
      0.5.0 added `haipipe-board-page-for-skill` as source 3, loaded whenever a page under review is a `Skill-<n>` or `Agent-<n>`.
      Without it this agent would have judged skill and agent pages by the base, whose Opening rule is the opposite one, marking correct prose wrong and passing the form letter the variant was written to catch.
- [x] 🛡 The read-only promise is enforced rather than trusted
      Its frontmatter grants `Read`, `Grep`, `Glob`, `Bash` and `Skill` and no write tool at all, so "never edits" is a property of the dispatch rather than an instruction it could disobey.
- [x] 🔗 It loads the contracts instead of carrying a copy of them
      The file says plainly that it is a procedure and not a second copy of the contract, and names five sources to load, "because a copy is exactly what goes a night out of date while the contract moves".
      That is the same defect still open in `live/chat.py`, avoided here by construction.

## States
The agent is written the way this family wants its agents written: it loads five contracts, restates none of them, and holds no write tool.
What is unsettled is not its quality but its existence, and that has been unsettled since 260729.
It reached 0.5.0 on 260802 and has still never been dispatched on this board, so every claim about what its review catches is a claim about a procedure rather than a result.

- 260802 CC · 📚 It did not know about a contract that had shipped hours earlier
  `haipipe-board-page-for-skill` shipped on 260802 and this agent's source list was not updated with it, so it would have judged the eight skill and agent pages by the base contract whose Opening rule is the opposite one.
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
260802 2100 · Synced to 0.5.0 and the authored half updated: the agent now loads `haipipe-board-page-for-skill` for a skill page, which it did not when that variant shipped hours earlier. Two Aims closed, one opened for the consecutive read of the eight roster Openings that is now waiting on it
260802 1720 · Authored half written: the `WORKFLOW` fence replaced the template placeholder with the dispatch, the four loaded contracts, the three-step review and the empty write-tool list, four real Aims replaced the single health placeholder, and `state:` moved from 🔴 to 🟡 in question. Recorded that the 260731 skill-versus-agent ruling argues against the retirement reading of JL's 260729 remark
260727 0017 · page generated from `board/agents/haipipe-board-reviewer-agent.md/` by `skillpage.py new`

<!-- haipipe:skill:log:start 0cc451fad22069bb board/agents/haipipe-board-reviewer-agent.md -->

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
