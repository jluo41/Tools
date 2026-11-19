# Bricks: what a paper is built from

JL 261117 (session Paper-Element): "Element 组成最终的 delivery。所以做好一个 delivery 就是要把 element 做好"; "定义
element，就是定义了雕塑"; then "BLOCK IS A LARGE AREA, AND brick is unit". This file names that unit, sorts its types,
places it on the page and on disk, and gives its life. It is a design reference: what is built today is marked, the
rest is owed (§ 8).

## 1. The picture: a building site and a blue-tape walk

A paper is one building site, a **Block**. It is built from **Bricks**. Each Brick has a number, a grade and a site
log. Near the end of a build the owner walks the rooms and puts a strip of blue tape on every fault; the crew fixes
each one and pulls its tape; the keys are handed over when no tape is left.

With AI the crew walks first. A fault it is sure of (a crooked brick, an unfilled joint) it fixes and untapes by
itself; the owner never sees it. A fault it is not sure of (move this wall? which material here?) gets a strip of
tape and one line on why. The owner walks in and sees only the tape that is left.

| Site | Here |
| --- | --- |
| a site (a large area) | Block: one paper |
| one phase of the build | writing Job: one version, one send (`j11_writing_v<MMDD>_<desk>`) |
| a room | Task: one Section |
| a brick | **Brick**: a sentence, a value, a research question |
| a brick's grade | brick type (§ 3) |
| the number on a brick | its address (`C2.P1.s2`, `RQ.H2`, `V_auc`) |
| where it sits on the drawings | 📍, its home file and anchor (§ 5) |
| the construction drawings | Story and Plan, signed before building (W1) |
| the foundation | the paper's question, `RQ.Q` |
| a load-bearing wall | a research question or claim: change it and everything above is checked again (❗) |
| the steel inside a wall | evidence (values, citations): unseen, carries the load, needs its certificate |
| the acceptance standard | the rubric, ★ |
| the site log | 🕘, the Brick's history (§ 7) |
| **blue tape** | 🙋 and 💬: what is left for the person |
| the owner's signature | ✓ |
| handing over the keys | the delivery: PDF, Word, the send |

The same column shows on the floor plan, the elevation and the structural drawing, under one part number. So does a
Brick: `V_auc` shows on the Board's Evidence, the version's Evidence and the Section's Evidence, and lives in `j02`.

Why Brick: Block is a large area and Brick its unit; the scale is the point. "Item" already means Evidence Item,
Review Item, Design Item and more; "Element" reads as an HTML element in code. A Brick's address never starts with
`b`, so it never reads as a Block id.

## 2. One Brick, three places

A Brick is one identity held in three places, joined by its address:

```text
                       a Brick: C2.P1.s2 (lineage sent-7f3)
             ┌───────────────────────┼───────────────────────┐
        content (file)          records (cards)            shown (page)
  draft/<stem>-draft-v4.md      draft/records/             Draft › Draft Lab
  §3 · "AUC rose to 0.91 …"     <stem>-comments.md         <li data-addr="C2.P1.s2">
                                <stem>-revise.md           📍 💬 1  ★ 7  🕘 2
                                <stem>-checked.md
```

- **Content** is the Brick itself; 📍 points at it.
- **Records** are the tape and the log on it: the card files of `servers/workbench/ref/cards.md` § 6.
- **Shown** is the Brick on a page, `view › section › brick`; one Brick may show on several pages, it has one home.

## 3. Brick types: the class tree (is-a)

The first split is who can close a Brick, because it decides how much tape reaches the person.

```text
Brick                                  base: address, home, history, marks, cards
│
├─ Choice      no right answer, only a trade-off. AI never closes it: it cuts the options to two or three,
│   │          ranks them, says why, and tapes 🙋
│   ├─ question        the paper's question                         RQ.Q
│   ├─ idea            a research direction                         j01.I04
│   ├─ rq              rq.question RQ.RQ1 · rq.hypothesis RQ.H2 · rq.claim (also checked)
│   ├─ beat            what one Section must make clear             story.C2
│   ├─ bullet          a Section plan bullet                        B9
│   └─ display_plan    a planned figure or table
│
├─ Prose       a standard, no single answer; better with each pass. AI closes it when it passes, tapes it when stuck
│   ├─ paragraph                                                    C1.P2
│   ├─ sentence                                                     C1.P2.s8
│   │   └─ sentence.abstract · .intro · .methods · .results · .discussion · .letter   (rubric overrides)
│   └─ title                                                        C1.title
│
├─ Fact        a right answer exists (the data, the source, the venue's rule). AI closes it; a mismatch is tape
│   ├─ value                                                        V_xxx
│   ├─ citation                                                     C_xxx
│   ├─ display         the checked half: venue limits, the Run that draws it   D_xxx
│   ├─ term                                                         term.SNF
│   └─ venue_rule
│
└─ Input       someone else raised it. AI splits, routes and drafts a reply; the person takes the stance
    └─ review_item                                                  R2.3
```

What each level fixes, a child inheriting its parent:

| Level | Fixes |
| --- | --- |
| Brick | the address rules, 📍, 🕘, the marks, the card format |
| loop (Choice, Prose, Fact, Input) | who may close it, when the loop stops, which marks may show (a Fact has no 📝, a Choice always ends in 🙋) |
| type (`sentence`) | its rubric, its address shape, its home, the skill that writes it |
| subtype (`sentence.methods`) | rubric lines it adds or overrides |

On the site: Prose is laying (the crew redoes it), Fact is material testing (against a standard), Choice is a design
change (the owner signs), Input is a correction notice (the crew answers each line).

## 4. Brick instances: part-of and refers-to

Instances hang in one tree, the chain of why:

```text
RQ.Q                                  question
└─ RQ.H1                              rq.hypothesis
    └─ story.C2                       beat: Results must make H1 clear
        └─ j11 · t03_results · B4     bullet
            └─ C2.P1                  paragraph
                ├─ C2.P1.s1           sentence.results
                ├─ C2.P1.s2           sentence.results ──refers-to──▶ V_auc, D_fig2
                └─ C2.P1.s3           sentence.results ──refers-to──▶ C_smith2024
```

- Every sentence can be asked why, up to the question. A sentence that reaches no beat is surplus.
- Fact Bricks are not in the tree; they are nodes of the refers-to graph (`$V_xxx$`, `\cite{C_xxx}`), shared by many
  sentences.
- part-of is held where the content already sits (a sentence under its bullet; a bullet naming its beat). Nothing is
  copied to hold it.

## 5. 📍 Where a Brick lives

Every Brick shows a quiet 📍 first in its mark strip. Its hover names the files; a click opens the pop-out reader at
the Brick.

| Case | Mark | Hover | Click |
| --- | --- | --- | --- |
| home here: this page owns the Brick | 📍 | content file and anchor; card file | the reader, scrolled to the Brick |
| shown here, home elsewhere (`V_auc` in a Section) | 📍↗ | the home's path; change it there | the home page |
| generated (LaTeX, a drawn figure) | 📍⚙️ | the source and the Run that makes it | the source; an 📝 here is an instruction to the next Run (`cards.md` § 8) |

A Brick whose home cannot be resolved draws no 📍, and the page checker lists it (`cards.md` § 3 rule 5).

## 6. On the page: view › section › brick

Every page is `Report › view › section`, then the Brick. Each numbered section under 📋 Review Content is one of three
kinds; a page must be able to say which:

| Kind | Holds | Marks |
| --- | --- | --- |
| bricks | Bricks of one or more types, each with `data-addr` | each Brick's own strip |
| rollup | rows that link to another page (a version, a Job, a Section) | that page's 🙋 N, 📝 N only |
| reference | examples, drawings, files | none |

The paper pages as served for `blueprints/Project-Ladder/paper/Paper-Example` (read live, 2026-11-17):

| Page | View | Section | Kind | Brick type | Home |
| --- | --- | --- | --- | --- | --- |
| Board | Idea | Directions | bricks | idea | `s01-ideation/` |
| Board | Idea | Theory | bricks | theory (to define) | `s01-ideation/` |
| Board | Idea | Open points | bricks | open point (to define) | `s01-ideation/` |
| Board | Story | Direction | bricks | question | story topic |
| Board | Story | Pitch | bricks | pitch (to define) | story topic |
| Board | Story | Research Questions | bricks | rq | story topic; ✅ has `data-addr` |
| Board | Story | Reading | bricks | related | `s10`-`s19` |
| Board | Story | Venues | bricks | venue_rule | `venues/<venue>/call.md` |
| Board | Story | Story by Section | bricks | beat | story topic |
| Board | Data + Paper Plan | Data flow · Paper flow | bricks | flow step, section row (to define) | `s03`, `s04` |
| Board | Support blocks | Work · Discovery | rollup | | |
| Board | Evidence | Values · Citations | bricks, shown | value, citation | `j02`, `j03` |
| Board | Displays | Plan · Displays | bricks | display_plan, display | `s06`, `j01` |
| Board | Displays | Examples | reference | | |
| Board | Displays | Story by Section | bricks, shown | beat | story topic |
| Board | Writing | each version · Sections to finish | rollup | | |
| version | Structure | Structure | bricks | layout row (to define) | the version face's `## Narrative` |
| version | Evidence · Display | Values · Citations · Displays | bricks, shown | value, citation, display | `j01`-`j03` |
| Section | 1 · Draft | Draft Lab | bricks | paragraph, sentence, title | `draft/`; sentences still keyed by `data-s` |
| Section | 1 · Draft | Examples | reference | | |
| Section | 1 · Draft | Writing Rubric | bricks | rule | `draft/records/<stem>-requirement.md`, `-revise-rules.md` |
| Section | 1 · Draft | Decisions | bricks | decision | `draft/records/` |
| Section | 2 · Plan | Structure | bricks | bullet | `draft/` |
| Section | 3 · Evidence | each value group · What does not resolve | bricks, shown | value, citation | `j02`, `j03` |
| `j02_evidence_value` | Values | Values | bricks | value | here |
| `j01_evidence_display` | Displays | Displays | bricks | display | here |
| `j31_review_*` | MindMap · Plan + Results · Findings | (none yet) | bricks | review_item | here |

## 7. The life of a Brick

```text
 ⬜ planned ──▶ 🧱 laid ──▶ ★ rated ──┬──▶ 🔁 redone by AI ──┐
                                     │         ▲            │  (fixed and accepted by itself)
                                     │         └────────────┘
                                     ├──▶ 🙋 taped ──▶ the person acts ──▶ rated again
                                     └──▶ ✓ checked ──▶ 📦 delivered ──▶ 🔀 carried into the next version
                                              │
                    upstream changed, or its words changed
                                              ▼
                                           ❗ stale ──▶ rated again

                     at any time: ✂️ split · 🔗 merged · 🗑️ cut
```

| Stage | On site | Mark | Recorded in | By | Today |
| --- | --- | --- | --- | --- | --- |
| planned | on the drawings, not laid | ⬜ | the plan bullet | the person signs (W1) | ✅ |
| laid | first laid, numbered | | Draft §3; the address is minted | AI (W2) | ✅ address; no lineage id |
| rated | the inspector's score | ★ | `-revise.md` Pass | fresh raters (W3) | ✅ |
| redone | taken down and relaid | 🕘 | a new Draft version; an accepted edit card | AI, judged by a blind A/B reader (W4) | ✅; 🤖 mark owed |
| taped | left for the owner | 🙋 💬 📝 | `-comments.md`; a proposed edit card | AI tapes, the person acts | ✅ |
| checked | the owner signs | ✓ | `-checked.md`, with the words it saw | the person only | ✅ |
| stale | a load-bearing wall moved | ❗ | nowhere yet | derived | ⬜ (changed words lapse a ✓; an upstream change marks nothing) |
| delivered | phase handed over, sealed | 🔒 | `delivery/`, the build manifest | the person writes `sent` | ✅ sealed; no mark on the Brick |
| carried | the next phase keeps this wall | 🕘 | the lineage | `paper_ladder.py next` | ⬜ |
| split, merged | one wall made two, two made one | 🕘 | the lineage ("split into s3, s4") | AI or the person | ⬜ (only the "moved" list) |
| cut | the wall is removed | struck | an edit card with `Expected: (cut)` | AI proposes, the person accepts | ✅ |

**The history is the site log**: when, who, what, why, one line per change.

```text
sent-7f3
├─ 11-20  laid      AI      "The AUC was 0.91."                         from B4
├─ 11-20  ★ 6       AI      not specific
├─ 11-20  redone    AI      "AUC rose to 0.91 in the held-out cohort."  A/B: easier, same meaning
├─ 11-20  ★ 8       AI      passes
├─ 11-21  💬        person  "define held-out"
├─ 11-21  redone    AI      definition added
├─ 11-22  ✓         person
├─ 11-30  📦        person  sent with j11
├─ 01-10  ❗        derived review item R2.3 points at it
└─ 01-12  carried   AI      into j12 · C2.P1.s2
```

The lines already exist, spread over the Draft versions, `-revise.md`, `-comments.md`, `-checked.md` and `delivery/`.
🕘 reads them by address and lineage into one log; no second log file is written.

## 8. What is owed

1. **A lineage id** per Brick, kept across versions, splits and merges: the thread 🕘 follows.
2. **❗ stale**: when an upstream Brick (rq, beat, value) changes, the Bricks below and the sentences that refer to it
   are marked.
3. **🔒 on a delivered Brick**, and no click may change it (`cards.md` § 8 already forbids the write).
4. **📍** in `item_marks.marks()`, with `item_address.resolve()` returning file, anchor and case; first on the Story's
   Research Questions (they carry `data-addr`), then Draft Lab.
5. **Draft Lab sentences on `data-addr`** instead of `.sx-row` / `data-s`.
6. **Each section declares its kind** (bricks, rollup, reference) and its Brick types, so the checker finds a bricks
   section with no addresses and the 🙋 tray knows where to gather.
7. **The types marked "to define"** in § 6 get a rubric, a home and a writer, or are folded into an existing type.
8. **The review Job's pages** show `review_item` Bricks.
9. **The other paper workflows** (`/haipipe-paper-ideation`, `/haipipe-paper-story`) define their loops over Choice
   Bricks, as `haipipe-paper-draft/ref/workflow.md` (W0-W5) does for Prose Bricks.
