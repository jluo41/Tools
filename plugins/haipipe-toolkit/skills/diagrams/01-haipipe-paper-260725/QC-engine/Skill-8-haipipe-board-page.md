# haipipe-board-page · v0.2.0
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-board-page` defines the reusable working record: Q, S, and Skill page kinds; the fixed on-stage sections; and the safe, anchored places a machine may write. It is why a Paper stage can live in the same Markdown object a reader opens and comments on.

It stops at page mechanics. This Paper Board adds the semantic overlay: `QC3` says which Paper contracts own regions of a stage page, and `QC5` says what Paper sections, paragraphs, sentences, and evidence must accomplish. The shared page shape must not be mistaken for a manuscript template.

## Diagram
<!-- haipipe:skill:tree:start 9759e3ddfab0bac7 board/haipipe-board-page -->

```
haipipe-board-page/
  CHANGELOG.md          40 ln  haipipe-board-page · Changelog
  SKILL.md             110 ln  /haipipe-board-page · the page, as a contract you can load
```

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence if the tree
above is the whole story.
```

## Content
<!-- haipipe:skill:body:start 9759e3ddfab0bac7 board/haipipe-board-page -->

**haipipe-board-page** · `0.2.0` · last shipped 2026-07-31

- folder   `board/haipipe-board-page/`
- tools    not declared
- summary  Decision Now is the one reserved subsection name inside Where we are: machine-proposed decisions land there as tickable rows, never only in chat (JL 260731).

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
      A page's KIND comes from its filename, and the kind decides only how the page closes and what its Content holds.
      Everything else is the shared base (the model on the design board's QB4, JL 260729).
      ```
      kind          filename                     closes when
      ─────────────────────────────────────────────────────────────────
      Q  decision   Q<group><n>[<face>]-<slug>   its Items boxes all close
      S  stage      S-<Family>-<unit>-<slug>     its human gate passes
      Skill mirror  Skill-<unit>-<slug>          the unit ships · NEVER counted
      ```
      A page kind used by one consumer family is a VARIANT of the base: it redefines Content only, and it ships under its consumer (`haipipe-paper-stage` is the first), never here.
      This skill owns the BASE those variants extend.

- 2 · 📑 The seven sections, in their fixed on-stage order
      ```
      #   section            owes the reader                      a machine may write
      ──────────────────────────────────────────────────────────────────────────────────
      1   Opening            the lead question + the drawer       nothing
                             (Structure · Why this matters)       (render-derived)
      2   Diagram            the figure; ids in it are links      nothing without the human
      3   Content            the substance, ### divisions         nothing without the human
      4   Items to Finish    the testable gap, - [ ] boxes        PROPOSE a tick, never tick
      5   Where we are       the state mirror, dated entries      append a dated entry
      6   Files              engine · inputs · outputs            append a row
      7   folds              Discussion · Law · Lesson · Log      append a Log or > lane line
      ```
      Subsection names inside Items, Where we are, and Files are CONTEXTUAL (JL 260729): they come from the page's subject, and any names a spec shows are examples, not a taxonomy.
      There is NO `## Boundary` section (JL 260731, said twice). It was added by CC on 260723, never ruled in, and removed from all 47 pages that carried one. What a page covers is the Opening's job; point at a neighbouring page from the prose that needs it.
      One name is RESERVED inside Where we are (JL 260731): `### Decision Now` holds the decisions a machine proposes and the human must make, one `- [ ]` row each carrying the ask, the options, and a recommendation.
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
      **The tick rule (QC6 §10).**
      A verb reading a transcript can report what the transcript CLAIMS, not verify it.
      So a machine may write Log lines and Where-we-are prose and may PROPOSE a tick as a `### Decision Now` row; it may not close a checkbox or flip `state:`.

- 3 · 🏷 Addressing
      ```
      page        QB4            #QB4
      face        QB12b           a page whose id carries its parent's number
      group       #group-QB      scrolls the index, opens nothing
      sentence    QB5's grammar  haipipe-board-sentence owns everything below the section
      ```
      Every id inside a fenced figure renders as a link (haipipe-board 0.53.0), so a contract that names pages is itself a map.

- 4 · 📂 Files
      ```
      haipipe-board-page/
      ├── SKILL.md            this contract
      └── CHANGELOG.md        version history
      ```
      Reads `haipipe-board/ref/page-template.md` and `ref/board-form.md` §4 (the section mapping and requiredness) and §8 (on-stage order) as the authority; owns no scripts.
      The named next step (QC6 §7): `serve.py`'s hand-rolled `CHAT_RULES` string becomes this contract's consumer instead of restating it, which kills the copy that has already rotted once.
<!-- haipipe:skill:body:end -->

## Aims
- [ ] 🧠 Rule this skill's health
      `state:` is a judgment, not a version number: stable, in flux, needs work, or parked.

## States
Mirrored into the Engine roster as the generic page contract used by every route. `QC3` is the bridge to Paper-specific page meaning; the Board card itself remains a reusable specification rather than a second Paper authoring contract.

## Log
260801 0000 · page generated from `board/haipipe-board-page/` by `skillpage.py new`

<!-- haipipe:skill:log:start 9759e3ddfab0bac7 board/haipipe-board-page -->

Converted from the skill's own `CHANGELOG.md`: 2 releases.

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
        (QB13b caught it describing a page shape that no longer existed).

<!-- haipipe:skill:log:end -->
