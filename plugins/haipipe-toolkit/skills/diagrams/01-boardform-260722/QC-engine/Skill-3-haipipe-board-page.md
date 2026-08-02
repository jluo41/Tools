# haipipe-board-page · v0.5.1
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
Does `haipipe-board-page` give every author and reviewer one dependable contract for what a Board page must do?

This spec owns the shared frame, section responsibilities, closure records, and evaluation rules for every page kind.
The difficult boundary is letting consumer variants define their substance without redefining the frame around it.
Routing, page creation, quick checks, and fresh review all depend on this contract agreeing with itself.
It is healthy when those consumers resolve the same requirements and reach evidence-based verdicts without private copies.

## Diagram
<!-- haipipe:skill:tree:start 342ee35df2f2f394 board/haipipe-board-page -->

```
haipipe-board-page/
  CHANGELOG.md          81 ln  haipipe-board-page · Changelog
  SKILL.md             177 ln  /haipipe-board-page · the page, as a contract you can load
```

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence if the tree
above is the whole story.
```

## Content
<!-- haipipe:skill:body:start 342ee35df2f2f394 board/haipipe-board-page -->

**haipipe-board-page** · `0.5.1` · last shipped 2026-08-01

- folder   `board/haipipe-board-page/`
- tools    not declared
- summary  The page contract is the single evaluation rubric; variants define Content and fill declared frame extension points without redefining the frame.

### SKILL.md




`haipipe-board` is the door you walk through to RUN a board.
This skill is a SPEC: what a page IS, loadable by an agent that has no board open.
QC6 §7 on the design board states the test it passes: a consumer needs these rules with no board open, and the consumers exist: the routing verb deciding "which page, which section", the chat drawer priming a per-page session, and the variant authors in other families.

**The boundary, and it is a hard one:**

```
haipipe-board-page               haipipe-board
─────────────────────            ──────────────────────────────
what a page IS                   rendering it (src/page_question.py)
the section contract             serving and write-back (serve.py)
where a write may land           the checker (check.py)
the base/variant model           the template file itself (ref/page-template.md)
```

This skill NEVER renders, serves, or checks.
The authoritative template stays `haipipe-board/ref/page-template.md`; this contract cites it and must never fork it.


- 1 · 🧬 Three page kinds, one base
      A page's KIND comes from its filename, and the kind decides how the page closes, what its Content holds, and which typed records it fills through the base frame's declared extension points.
      Everything else is the shared base (the model on the design board's QB4, JL 260729).
      ```
      kind          filename                     closes when
      ─────────────────────────────────────────────────────────────────
      Q  decision   Q<group><n>[<face>]-<slug>   every Aim is met or explicitly held
      S  stage      S-<Family>-<unit>-<slug>     its human gate passes
      Skill mirror  Skill-<unit>-<slug>          the unit ships · NEVER counted
      ```
      A page kind used by one consumer family is a VARIANT of the base: it defines Content and may populate fixed extension points in Aims, States, and Stage Contract, but it never redefines, adds, removes, or reorders those frame sections.
      The variant ships under its consumer (`haipipe-paper-stage` is the first), never here.
      This skill owns the BASE those variants extend.

- 2 · 📑 The seven sections, in their fixed on-stage order
      ```
      #   section            owes the reader                      a machine may write
      ──────────────────────────────────────────────────────────────────────────────────
      1   Opening            the lead question + why it matters   nothing
      2   Diagram            the figure; ids in it are links      nothing without the human
      3   Content            the substance, ### divisions         nothing without the human
      4   Aims               durable Content-linked targets       revise only when intent changes
      5   States             one factual current State per Aim    update with evidence; human decisions stay human
      6   Files              engine · inputs · outputs            append a row
      7   folds              Discussion · Law · Lesson · Glossary · Log  append a Log or > lane line
      ```
      Each section answers ONE reader question, and the same five rows define every section's contract (JL 260801, ruled on the design board's QB4 §0): **conveys**, the reader question it answers · **holds**, the elements it must contain · **source**, how the author writes it · **rules**, what binds a write · **omit**, when it may be absent.
      ```
      section            conveys · the reader question                omit
      ──────────────────────────────────────────────────────────────────────
      🧭 Opening          what is this page, why should I care?        never
      🖼 Diagram          can I see the whole subject at once?         when no figure helps: delete
      📚 Content          what does this page actually establish?      Q may · S never
      🎯 Aims             what should become true, and for which Content division? never
      📍 States           what is true now for each Aim, what waits?   never
      📎 Files            which few files continue this work?          allowed, advised against
      🗃 folds            what was ruled, learned, changed, if needed  each optional
      ```
      A sentence answering another section's question is MISPLACED, and the protocol names its home: substance found in Opening moves to Content, Required Inputs and Venue move to Stage Contract, prose rules move to Writing Style, intended outcomes move to Aims, current facts move to States, and temporary next steps become an Aim's optional Plan.
      The full five rows per section live in the design board's `QB4` Content divisions; the authoritative source form stays `haipipe-board/ref/page-template.md`.
      Subsection names inside Aims, States, and Files are CONTEXTUAL (JL 260729): Aims and States mirror the relevant Content divisions, and any names a spec shows are examples, not a taxonomy.
      An Aim is not a task. Write `- A3.1 · target` for a result owned by Content division C3 and `P1` only for a target that genuinely crosses divisions. One division may have zero, one, or many Aims. Each Aim has a testable `Done when` and may carry a temporary `Plan`; changing Plan does not change the Aim.
      The section labels are deliberately both plural: `Aims` contains Aim records and `States` contains their State records. States mirrors every Aim id exactly once: `⬜` not started, `🟡` active, `🟠` waiting on a human or external dependency, `✅` met with evidence, or `⏸️` explicitly held. The section is a snapshot, so the reason for a transition belongs in Log. The strict one-to-one relationship is Aim to current State row, never Content division to Aim.

- 3 · ✅ Evaluation contract
      Evaluation asks whether the authored page satisfies its declared requirements; it does not ask whether the reviewer personally likes the format.
      The requirements stay here, in the page spec and its cited template, rather than being copied into a second evaluation skill.
      The evaluator is a consumer of this contract.
      Resolve applicable requirements in this order:
      1. The base section contract in this skill and `ref/page-template.md`.
      2. The page kind or consumer variant, when one exists.
      3. The page's own `## Writing Style`; on S pages, also its `## Stage Contract`.
      4. The local `###` division purpose and each `####` heading's immediately following `(job line)`, when present.
      A more specific source may refine a broader one but may not silently contradict it.
      When two sources disagree, report a requirement conflict and stop judging that criterion until the owner resolves it.
      Review four distinct axes:
      | Axis | Question | Judge |
      |---|---|---|
      | Mechanics | Is the required structure present, ordered, addressable, and internally consistent? | `check.py` |
      | Function | Does this section answer the reader question the contract assigns to it? | semantic reviewer |
      | Evidence | Can every factual compliance claim point to visible text, a State row, or a linked artifact? | semantic reviewer |
      | Readability | Can a zero-background reader understand the section without supplying a missing premise? | fresh-context reviewer |
      The review units are every present `##` section, every direct `###` Content division, and every `####` paragraph whose local job must be tested.
      Use exactly four verdicts: `MEETS`, `NEEDS WORK`, `N/A`, and `NOT VERIFIABLE`.
      `N/A` means a rule genuinely does not apply; `NOT VERIFIABLE` means the required evidence is unavailable and is never a pass.
      The report is one row per review unit:
      ```text
      unit | applicable requirements + source | verdict | evidence | smallest fix
      ```
      Then report requirement conflicts, mechanical findings, and one page-level verdict.
      The review is read-only: it never edits prose, changes an Aim State, ticks Decision Now, or closes a page.
      Execution uses existing surfaces rather than a new skill:
      - `check.py --strict` supplies the deterministic mechanical findings.
      - The page's `✅ Quality Check` runs the complete row-by-row rubric quickly in the current page chat.
      - `haipipe-board-reviewer-agent` runs the same contract in a fresh context after revision and acts as the independent gate.
      The quick check helps the author iterate; only the fresh reviewer tests whether the page stands on its own without conversation context.
      There is NO `## Boundary` section (JL 260731, said twice). It was added by CC on 260723, never ruled in, and removed from all 47 pages that carried one. What a page covers is the Opening's job; point at a neighbouring page from the prose that needs it.
      One name is RESERVED inside States (JL 260731): `### Decision Now` holds the decisions a machine proposes and the human must make, one `- [ ]` row each carrying the ask, the options, and a recommendation.
      A proposal never lives only in chat: it is written there on the owning page, the human answers by ticking, and an answered row moves into the page's dated record.
      The options take ONE LINE EACH, and each line says what choosing it commits you to (JL 260731: "I want the decision A, B, C, to be in a new line and explain each options, not all the options in one line").
      Three labels crammed onto one line name the options and explain none, so the reader has to reconstruct the consequences before they can choose.
      The recommendation is its own line, naming the letter and why it beats the others.
      ```markdown
      - [ ] 🗣 The ask, stated as one question
            One or two lines of context: what is true today, and what it costs.
            A · the first option, and what choosing it commits you to.
            B · the second option, and what it commits you to.
            → CC recommends B, because <the reason it beats A>.
      ```
      **The write anchor rule (QC6 §9, from a real casualty).**
      A machine write lands at a SECTION BOUNDARY, never at a byte offset: on 260730 a concurrent session spliced a `###` block into the middle of another page's `## Opening` sentence.
      Appending under a named `## ` heading is safe; inserting by offset is how that damage reproduces at scale.
      **The human-decision rule (QC6 §10).**
      A verb reading a transcript can report what the transcript CLAIMS, not verify it.
      So a machine may update an Aim's State only from evidence it can inspect, and may propose a human ruling as a `### Decision Now` row; it may not close that decision checkbox or flip a human-gated page to settled.

- 4 · 🏷 Addressing
      ```
      page        QB4            #QB4
      face        QB4a           a page whose id carries its parent's number
      group       #group-QB      scrolls the index, opens nothing
      sentence    QB5's grammar  haipipe-board-sentence owns everything below the section
      ```
      Every id inside a fenced figure renders as a link (haipipe-board 0.53.0), so a contract that names pages is itself a map.

- 5 · 📂 Files
      ```
      haipipe-board-page/
      ├── SKILL.md            this contract
      └── CHANGELOG.md        version history
      ```
      Reads `haipipe-board/ref/page-template.md` and `ref/board-form.md` §4 (the section mapping and requiredness) and §8 (on-stage order) as the authority; owns no scripts.
      The named next step (QC6 §7): `serve.py`'s hand-rolled `CHAT_RULES` string becomes this contract's consumer instead of restating it, which kills the copy that has already rotted once.
<!-- haipipe:skill:body:end -->

## Items to Finish
- [ ] 🧠 Rule this skill's health
      `state:` is a judgment, not a version number: stable, in flux, needs work, or parked.

## Where we are
Page generated 260731 1115. Nothing ruled yet.

## Log
260731 1115 · page generated from `board/haipipe-board-page/` by `skillpage.py new`

<!-- haipipe:skill:log:start 342ee35df2f2f394 board/haipipe-board-page -->

Converted from the skill's own `CHANGELOG.md`: 7 releases.

260801 · `0.5.1`
      - Clarified the base/variant boundary: a consumer variant defines Content and
        may fill typed records through declared Aims, States, and Stage Contract
        extension points, but it never redefines the shared frame sections.
260801 · `0.5.0`
      - Keeps requirements in the page spec instead of copying them into a separate
        evaluation skill.
      - Resolves base, variant, page-local, Stage Contract, division, and paragraph-job
        requirements before judging.
      - Defines four axes (mechanics, function, evidence, readability), four verdicts,
        and one evidence-bearing report row per section or Content unit.
      - Assigns execution to the existing `check.py`, `✅ Quality Check`, and fresh
        Board reviewer surfaces.
260801 · `0.4.1`
      - Canonicalized the paired section labels as `Aims / States`: both are plural
        collections, while one Aim still maps to one current State record.
      - Kept singular `State` as a legacy input alias alongside `Where we are` and
        `Now`.
260801 · `0.4.0`
      - The page contract now separates durable intent from present fact. `## Aims` holds stable Content-linked targets (`A3.1`, with `P1` for page-level targets), a testable `Done when`, and an optional temporary `Plan`. `## State` mirrors every Aim exactly once with ⬜, 🟡, 🟠, ✅, or ⏸️. State transitions go to Log; Decision Now remains the human-only checkbox edge. A Content division may have zero, one, or many Aims, while every Aim must have one current State row.
      - The fixed sequence is `Opening → Diagram → Content → Aims → State → Files`. The contract no longer teaches the retired generated Structure row or checkbox-based page completion. Historical `Items to Finish`, `Done when`, `Where we are`, and `Now` remain parser aliases, not canonical authoring guidance.
260801 · `0.3.0`
      - The five-row section contract (JL 260801, ruled as option A on the design board's
        QB4 Decision Now): every section answers ONE reader question, and the same five
        rows define each section's contract — conveys · holds · source · rules · omit.
        The seven-sections table gains the reader-question ladder plus the
        misplaced-sentence rule (substance in Opening → Content, contract material in
        Content → Stage Contract, settled flags → Where we are, open work → Items to
        Finish). Long form stays on the board's QB4a-QB4g faces; the compact form now
        lives here and in `ref/q-template.md`'s How-to-use comment, where a writer
        actually meets it.
260731 · `0.2.0`
      - Decision Now: the one RESERVED subsection name inside `## Where we are` (JL, same
        day: "don't make the decision here ... Always go to the corresponding Q's Where we
        are's subsection of Decision Now"). It lists the decisions a machine proposes and
        the human must make, one `- [ ]` row each with the ask, the options, and a
        recommendation; the human answers by ticking; an answered row moves into the
        page's dated record. The 260729 contextual-naming rule stands for every other
        subsection; this is its single exception.
      - The tick rule now names the landing spot: a machine PROPOSES a tick as a Decision
        Now row, never in chat alone.
      - The board pages `QB4e` (the Where-we-are face) and `QC6` on the design board carry
        the first two live subsections.
260731 · `0.1.0`
      - First cut, created on JL's order ("make the haipipe-board thinner, and have other
        skills, like haipipe-board-page ... please creating them now") from the roster the
        design board had already settled: QC6 §8's shape is one door, two SPECS, two VERBS,
        and this is the page SPEC the routing and digest verbs LOAD.
      - Contract-first: no code moved. It owns what a page IS (the three kinds over one
        base, the seven sections in their fixed order, the write anchors), and it cites
        `haipipe-board/ref/q-template.md` as the authority rather than forking it.
      - Carries the two machine-write rules with their provenance: writes land at a
        SECTION BOUNDARY, never a byte offset (QC6 §9, after a concurrent session spliced
        a heading into the middle of another page's Question sentence on 260730), and a
        transcript-reading verb may propose a tick but never tick or flip `state:`
        (QC6 §10, because reporting a claim is not verifying it).
      - Names its own next step from QC6 §7: `serve.py`'s `CHAT_RULES` becomes a consumer
        of this contract instead of a hand-rolled copy, which has already rotted once
        (QB5d caught it describing a page shape that no longer existed).

<!-- haipipe:skill:log:end -->
