# Six folders in three pairs, and what may cross between them
state: ✅ SETTLED
owner: JL
method: every THING has a board; name all six, allow four crossings, and treat the banks as a wall rather than a room

## Question
Where does a new rule, file, or page belong? Six folders exist in three pairs, each holding a different kind of truth: a reusable skill and its design board, the board tool and its own board, one manuscript and its lifecycle board. Put something in the wrong one and it either binds nothing, because no runtime reads it, or it becomes wrong for every other paper.

The word "paper" names four different things at once, and they sit in two different repositories. There is a reusable skill that ships. There is a design board that argues about that skill. There is one manuscript. And there is the control plane that manuscript is worked from. Each holds a different kind of truth and each has a different lifetime, but all four are called "the paper work" in conversation, so nothing stops a file from landing in the wrong one.

The failures are not hypothetical and they are not symmetric. A rule written into a working folder binds nothing, because no runtime reads it. Working state written into the manual makes the manual wrong for every other paper. A design argument that runtime starts depending on means the skill can no longer be shipped without its own history. And a paper that keeps a copy of the universal contract drifts from it silently, since nothing compares the two.

One of these has already happened here. This face used to say "design Board" in the singular, collapsing the skill's board and a paper's board into one word. They use the same tool, the same face grammar and the same four `state:` values, so the collapse looked harmless. It was not: the graduation rule, which says a settled ruling leaves the board for the skill, then appeared to apply to a paper's S pages, whose Content must never leave because it IS the paper.

This is the first face on the board because every later ownership question assumes it is answered. `QBa2` can only say who names a file once it is settled which tree the file is in. `QBc1` can only draw an ownership line inside a shared page once it is settled which two owners exist. A reader who cannot place a thing cannot rule on it.

## Boundary
- ✅ Covered here
  The six folders in three thing/board pairs, which kind of truth each holds, the only movements allowed between them, and the outside boundary the paper reaches across for evidence.
- ↪ Covered elsewhere
  What is inside the skill set is `QA2`; what is on the skill board is `QA3`; what a new paper gets is `QA4`; what is on a paper board is `QA5`. How a question actually crosses the evidence wall and comes back is `QBb1`, and what it may cost is `QBb2`.

## Diagram
```
                        THE THING                    ITS BOARD
   ┌──────────────┬────────────────────────┬──────────────────────────────┐
   │  reusable    │ ① skills/paper/        │ ② diagrams/                  │
   │  THE PAPER   │   35 skills · v0.3.2   │     01-haipipe-paper-260725/ │
   │   SKILL      │   WHAT SHIPS           │     32 Q faces · WHAT IS     │
   │              │                        │     ARGUED  <- you are here  │
   ├──────────────┼────────────────────────┼──────────────────────────────┤
   │  reusable    │ ③ 0_utils/             │ ④ diagrams/                  │
   │  THE BOARD   │   haipipe-board/       │     01-boardform-260722/     │
   │   TOOL       │   v0.24.0 · builds ②,  │     27 Q faces               │
   │              │   ⑧ and ④ itself      │     READ-ONLY from here      │
   ├──────────────┼────────────────────────┼──────────────────────────────┤
   │  ONE PAPER   │ ⑦ Paper-X/             │ ⑧ Paper-X/0-lifecycle/       │
   │              │   0-sections/ …        │     39 S faces · 8 families  │
   │              │   WHAT IS WRITTEN      │     WHAT IS WORKED           │
   └──────────────┴────────────────────────┴──────────────────────────────┘

   every row is a THING and the BOARD that governs it. That is the whole
   shape. ③ builds the entire right-hand column, including its own board.

   ── the four crossings, and nothing else ─────────────────────────

   ⒜  ② ──graduates──▶ ①  AND ③          ④ ──graduates──▶ ③
        a ruling reaches ✅ and its Law is COPIED into the owning
        skill. SEVEN of thirteen groups here land in BOTH ① and ③.
        Applied to one side only, it is a defect.             → QA3

   ⒝  ① ＋ ③ ──together──▶ ⑦ AND ⑧
        two skills alternate on ONE markdown file and never write the
        same REGION. ③ composes the filename, the shell, the managed
        block, and everything a human types; ① writes the substance
        and generates ⑦ from it.
        Only ③ writes ⑧ from a click. Only ① writes ⑦. → QA6 QA7 QA8

   ⒞  ⑦ ──asks across──▶  THE EVIDENCE WALL
        examples/Project-*/tasks/ · discoveries/
        not a room: outside, owned by another skill family. A paper
        may not compute and may not read the literature.      → QBb1

   ⒟  ✗ FORBIDDEN
        ① ──▶ ②   a runtime skill needing an open Q page
        ③ ──▶ ②   the tool depending on the board that designs it
        ③ ──▶ ④   likewise, and for the same reason
        ② ──▶ ⑦   reading a paper's state off a design board
        ② ──▶ ④   this board RULING the board tool's own board.
                   We consult ④; we never write it.
        delete any board and every skill still runs. If that is ever
        untrue, something has been placed wrong.
```

## Content
### Six folders, three pairs, one wall
```
① paper skill    settled, reusable procedure     skills/paper/
② its board      the rulings that produced it    diagrams/01-haipipe-paper-260725/
③ board tool     the thing that renders boards   skills/0_utils/haipipe-board/
④ its board      the rulings that produced IT    diagrams/01-boardform-260722/
⑦ paper          one manuscript's real content   examples/…/papers/Paper-X/
⑧ its board      that paper's lifecycle state    Paper-X/0-lifecycle/
```
Six, in three pairs, and the pairing IS the pattern: every THING has a board, and the board holds the arguments that produced the thing. Two pairs are reusable; one is a single manuscript.

Calling it "four folders and a tool" was wrong, and the phrasing gave it away (JL 260726): a thing numbered `③` in the same sequence as the others is in the same set. But five was wrong too, because it left `③` as the only thing on the map without a board, while its board, `01-boardform-260722`, was already cited by four faces here as the authority for what a board is. Numbering it `④` makes that citation structural instead of an appeal to something off the map.

`④` differs from the other five in one respect worth stating: **we rule nothing there.** This board consults it and never writes it, exactly as `QA3`'s Law says a design board behaves toward anyone who is not its owner. It is on the map because it is the board of a thing already on the map, not because we claim it.

The crossing that carries the most weight is `⒝`, because it is the one that produces anything. `①` and `③` are two separate skills that write the same markdown file and never contend, because their regions are disjoint: `③` owns the filename, the face shell, the managed contract block and every keystroke a human contributes through the live layer, while `①` owns Question, Boundary, Content, Items to Finish and Where we are, and is the only one of the two that generates `⑦`. `QA7` states that ownership line seam by seam; `QA8` states how work leaves a page and returns to it.

The evidence banks are deliberately not numbered among them. `tasks/` and `discoveries/` sit beside `papers/` inside a project, they are owned by `/haipipe-task` and `/haipipe-discovery`, and no page of this skill rules anything about their contents. Calling them a fifth folder gives them false parity with the four and breaks the grid. They are the OUTSIDE, and what matters here is the wall and how a question crosses it.

### Two of them are boards, and they are opposites
`②` and `⑧` use the same tool and the same grammar, which makes them look like one thing. They are not.

A design board is a RECORD. Its rulings are supposed to leave: `✅` means the Law is copied into `①`, and from then on the skill binds, not the board. Delete `②` and the skill still runs.

A paper board is a CONTROL PLANE. Nothing leaves it. A gated S page keeps its Content, because that Content is the paper. Delete `⑧` and `⑦` loses its frontier, its queue and its state.

Same glyph, opposite meaning: `✅` on `②` is a ruling made, `✅` on `⑧` is a human gate passed. That difference is argued on its own two pages, `QA3` and `QA5`, written as deliberate opposites.

### Placing something new
```
 a rule that is still argued          →  a Q face on ②
 a rule that is decided               →  ② as a ## Law, then graduate into ①
 a procedure an agent must follow     →  ①, in the owning SKILL.md or contract
 one paper's prose, display, number   →  ⑦
 one paper's status, queue, gate      →  ⑧
 a number or citation from a run      →  across the wall, bound from ⑦'s 1-probes/
```

## Items to Finish
- [x] 🧭 Separate the six folders, in three pairs
      Every THING has a board. `③`'s board is `④`, read-only from here (JL 260726).
- [x] 🧭 Separate the folders by the kind of truth each holds
      Each holds a different kind of truth, and the two boards are named separately rather than collapsed into one word.
- [x] 🧱 Treat the banks as a wall, not a room
      They belong to another skill family and this board rules nothing about their contents, so numbering them among the four was false parity (JL 260726).
- [x] 🔀 State the four legal crossings
      Graduation into BOTH skills, the ①＋③ collaboration that produces ⑦ and ⑧, asking across the wall, and the three forbidden directions (260726).
- [ ] 📐 State the boundary in the paper family map
      `README.md` still describes the tree without this distinction. A fresh agent must be able to place a new file without reading this board.
- [ ] 🧪 Check for reverse dependencies
      No runtime skill should require an open Q page or infer paper state from `②`. This has never been checked.

## Where we are
The six folders and the four crossings are ruled.

Two corrections landed on 260726, both from real confusion rather than review. The two kinds of board had been one word, which made the graduation rule appear to apply to a paper's S pages. And the evidence banks had been counted as a fifth folder, which put a folder owned by another skill family on the same footing as the four this skill owns.

None of it has graduated. `README.md` still carries the older complete-folder description.

## Files
- `README.md`
  The paper family map that should carry this boundary.
- `0-lifecycle/`
  The live `⑧` inside one paper instance.
- `haipipe-probe/`
  The layer that owns the crossing to the banks.

## Law
Six folders in three pairs, and exactly four crossings between them. Every thing has a board, and that board holds the arguments that produced it.

A settled ruling graduates from the skill board into the OWNING SKILL, which for seven of thirteen groups means both `①` and `③`, and only then binds. A ruling landed on one half of a pair is a defect.

`①` and `③` produce `⑦` and `⑧` together, on one file, in disjoint regions: the tool owns the shell and every human keystroke, the paper skill owns the substance and every generated manuscript file. A paper consumes the settled contract and never stores the universal manual. A paper binds a question it cannot answer to a bank answer, by path, across a wall it may not reach through in any other way.

The evidence banks are not a folder of this skill. They are owned elsewhere, and nothing on this board rules their contents.

No runtime skill may require an open Q page, and no paper's state may be inferred from a design board. A design record is never a runtime dependency: delete any board and every skill still runs.

A board is ruled by its owner alone and consulted by everyone else. This board rules `①` and, for the contract half, `③`. It never rules `④`.
