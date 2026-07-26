# Eight folders in four pairs, and the two channels out
state: ✅ SETTLED
owner: JL
method: every THING has a board; name all six, allow four crossings, and treat the banks as a wall rather than a room

## Question
Where does a new rule, file, or page belong? Eight folders exist in four pairs, because every THING has a board that argues its rules: the paper skill, the two shared skills that are its only channels out, and one manuscript. Put something in the wrong one and it either binds nothing, because no runtime reads it, or it becomes wrong for every other paper.

The word "paper" names several different things at once, and they sit in two different repositories. There is a reusable skill that ships. There is a design board that argues about that skill. There is one manuscript. And there is the control plane that manuscript is worked from. Each holds a different kind of truth and each has a different lifetime, but all four are called "the paper work" in conversation, so nothing stops a file from landing in the wrong one.

The failures are not hypothetical and they are not symmetric. A rule written into a working folder binds nothing, because no runtime reads it. Working state written into the manual makes the manual wrong for every other paper. A design argument that runtime starts depending on means the skill can no longer be shipped without its own history. And a paper that keeps a copy of the universal contract drifts from it silently, since nothing compares the two.

One of these has already happened here. This face used to say "design Board" in the singular, collapsing the skill's board and a paper's board into one word. They use the same tool, the same face grammar and the same four `state:` values, so the collapse looked harmless. It was not: the graduation rule, which says a settled ruling leaves the board for the skill, then appeared to apply to a paper's S pages, whose Content must never leave because it IS the paper.

This is the first face on the board because every later ownership question assumes it is answered. `QB4` can only say who names a file once it is settled which tree the file is in. `QA8` can only draw an ownership line inside a shared page once it is settled which two owners exist. A reader who cannot place a thing cannot rule on it.

## Boundary
- ✅ Covered here
  The six folders in three thing/board pairs, which kind of truth each holds, the only movements allowed between them, and the outside boundary the paper reaches across for evidence.
- ↪ Covered elsewhere
  What is inside the skill set is `QA2`; what is on the skill board is `QA3`; what a new paper gets is `QA6`; what is on a paper board is `QA7`. How a question actually crosses the evidence wall, and what it may cost, is `QB9`.

## Diagram
```
   ① writes the paper and owns NEITHER channel out of it.
   Two shared skills own the two channels, and that is the whole shape:

        THE EVIDENCE                                    THE HUMAN
       tasks/ discoveries/                          eyes, clicks, a yes
              ▲                                             ▲
              │                                             │
        ⑤ /haipipe-probe          ①            ③ /haipipe-board
        the ONLY door       /haipipe-paper       the ONLY way a human
        evidence enters by  the SUBSTANCE        touches a page
              │              writes ⑦ and ⑧             │
              └─────────────────┬───────────────────────┘
                                ▼
                      ⑦ the paper · ⑧ its board

   ── the four pairs: every THING has a board ──────────────────────
   ┌───────────────┬─────────────────────────┬──────────────────────────────┐
   │ reusable      │ ① skills/paper/         │ ② diagrams/01-haipipe-       │
   │ THE PAPER     │   35 skills · v0.3.2    │     paper-260725/  33 faces  │
   │  SKILL        │   WHAT SHIPS            │     WHAT IS ARGUED ← here    │
   ├───────────────┼─────────────────────────┼──────────────────────────────┤
   │ reusable      │ ③ 0_utils/              │ ④ diagrams/01-boardform-     │
   │ THE HUMAN     │   haipipe-board/        │     260722/  27 faces        │
   │  CHANNEL      │   v0.24.0               │     READ-ONLY from here      │
   ├───────────────┼─────────────────────────┼──────────────────────────────┤
   │ reusable      │ ⑤ probe/                │ ⑥ diagram/260714-probe-qa/   │
   │ THE EVIDENCE  │   haipipe-probe/        │     a design FOLDER, not a   │
   │  CHANNEL      │   v0.9.9 · 353 lines    │     board. The one gap.      │
   ├───────────────┼─────────────────────────┼──────────────────────────────┤
   │ ONE PAPER     │ ⑦ Paper-X/              │ ⑧ Paper-X/0-lifecycle/       │
   │               │   0-sections/ 1-probes/ │     39 S faces · 8 families  │
   │               │   WHAT IS WRITTEN       │     WHAT IS WORKED           │
   └───────────────┴─────────────────────────┴──────────────────────────────┘

   ⑤ and ③ are the same KIND of dependency, and the paper skill says so
   about both. haipipe-paper-probe: "the model is not this file's, this
   file is only the paper-side deltas." create-page.py: the same, onto
   the Board's stage.py. Every phase worker in ① is an adapter.

   ── the four crossings, and nothing else ─────────────────────────

   ⒜  ② ──graduates──▶ ① AND ③        ④ ──graduates──▶ ③
        a ruling reaches ✅ and its Law is COPIED into the owning skill.
        SEVEN of thirteen groups here land in BOTH.            → QA3

   ⒝  ① ＋ ③ ──together──▶ ⑦ AND ⑧
        two skills on ONE markdown file, never the same REGION.
        Only ③ writes ⑧ from a click. Only ① writes ⑦. → QA4 QA8 QA9

   ⒞  ⑦ ──asks across──▶ THE EVIDENCE WALL, through ⑤
        as a STRING with the stake stripped; the answer returns as a
        FILE, bound BY PATH. The bank never learns the claim. → QA5

   ⒟  ✗ FORBIDDEN
        ① ──▶ ②     a runtime skill needing an open Q page
        ③ ──▶ ②     the tool depending on the board that designs it
        ② ──▶ ④ ⑥   ruling a record this family does not own
        ② ──▶ ⑦     reading a paper's state off a design board
        delete any board and every skill still runs.
```

## Content
### Eight folders, four pairs, and two channels
```
① paper skill    settled, reusable procedure     skills/paper/
② its board      the rulings that produced it    diagrams/01-haipipe-paper-260725/
③ board tool     THE HUMAN CHANNEL               skills/0_utils/haipipe-board/
④ its board      the rulings that produced IT    diagrams/01-boardform-260722/
⑤ probe layer    THE EVIDENCE CHANNEL            skills/probe/haipipe-probe/
⑥ its record     a design folder, not a board    diagram/260714-probe-qa/
⑦ paper          one manuscript's real content   examples/…/papers/Paper-X/
⑧ its board      that paper's lifecycle state    Paper-X/0-lifecycle/
```
Eight, in four pairs, and two things are true at once. Every THING has a board, which is the pairing. And `①` writes the paper while owning neither channel out of it, which is the shape (JL 260726).

That second reading is the useful one. A paper has exactly two ways to reach anything outside itself: evidence comes in through `⑤ /haipipe-probe`, and a human reaches the work through `③ /haipipe-board`. `①` owns the substance and neither door. Both doors are shared skills whose models this family depends on and does not own, and the paper skill says so about both of them in its own words: `haipipe-paper-probe` is "only the paper-side deltas", and `create-page.py` is the same thing onto the Board's `stage.py`.

`⑥` is the one asymmetry worth stating: it is a design folder rather than a board, so the evidence channel's rationale cannot be read, commented on or closed the way the other two can.

Calling it "four folders and a tool" was wrong, and the phrasing gave it away (JL 260726): a thing numbered `③` in the same sequence as the others is in the same set. But five was wrong too, because it left `③` as the only thing on the map without a board, while its board, `01-boardform-260722`, was already cited by four faces here as the authority for what a board is. Numbering it `④` makes that citation structural instead of an appeal to something off the map.

`④` differs from the other five in one respect worth stating: **we rule nothing there.** This board consults it and never writes it, exactly as `QA3`'s Law says a design board behaves toward anyone who is not its owner. It is on the map because it is the board of a thing already on the map, not because we claim it.

The crossing that carries the most weight is `⒝`, because it is the one that produces anything. `①` and `③` are two separate skills that write the same markdown file and never contend, because their regions are disjoint: `③` owns the filename, the face shell, the managed contract block and every keystroke a human contributes through the live layer, while `①` owns Question, Boundary, Content, Items to Finish and Where we are, and is the only one of the two that generates `⑦`. `QA8` states that ownership line seam by seam; `QA9` states how work leaves a page and returns to it.

The evidence banks are deliberately not numbered among them. `tasks/` and `discoveries/` sit beside `papers/` inside a project, they are owned by `/haipipe-task` and `/haipipe-discovery`, and no page of this skill rules anything about their contents. Calling them a fifth folder gives them false parity with the folders we own and breaks the grid. They are the OUTSIDE, and what matters here is the wall and how a question crosses it.

### Two of them are boards, and they are opposites
`②` and `⑧` use the same tool and the same grammar, which makes them look like one thing. They are not.

A design board is a RECORD. Its rulings are supposed to leave: `✅` means the Law is copied into `①`, and from then on the skill binds, not the board. Delete `②` and the skill still runs.

A paper board is a CONTROL PLANE. Nothing leaves it. A gated S page keeps its Content, because that Content is the paper. Delete `⑧` and `⑦` loses its frontier, its queue and its state.

Same glyph, opposite meaning: `✅` on `②` is a ruling made, `✅` on `⑧` is a human gate passed. That difference is argued on its own two pages, `QA3` and `QA7`, written as deliberate opposites.

### Why two of the eight have no face
`④` and `⑥` are the design records of skills this family does not own, and `QA3`'s Law says a board is ruled by its owner alone and consulted by everyone else. So they are named on the map, cited constantly, and never given a page here. That is the rule working, not a gap to fill: writing a face about `④` would be this board ruling a board it has no standing over.

### The two channels are not covered equally, and that is honest
```
 ③ the human channel     3 faces   QA4 the tool · QA8 the region seam
                                   · QA9 the driving seam
 ⑤ the evidence channel  1 face    QA5
```
The asymmetry is real and it reflects where the rulings are. `③`'s contract with `①` is heavily ruled here: who names a file, who creates a page, which dependency declaration binds, where state lives, the dialect seam, the queue, the runner. `⑤` owns nearly all of its own contract, and this family rules only which questions a paper raises and how a landed answer is interpreted.

The thing to watch is that the imbalance stays a reflection and does not become a habit. If the evidence channel ever grows a second ruled seam, it earns a second face by the same test as anything else.

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
- [x] 🧭 Separate the eight folders, in four pairs
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
The eight folders and the four crossings are ruled.

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
Eight folders in four pairs, and exactly four crossings between them. Every thing has a board, and that board holds the arguments that produced it.

A settled ruling graduates from the skill board into the OWNING SKILL, which for seven of thirteen groups means both `①` and `③`, and only then binds. A ruling landed on one half of a pair is a defect.

`①` and `③` produce `⑦` and `⑧` together, on one file, in disjoint regions: the tool owns the shell and every human keystroke, the paper skill owns the substance and every generated manuscript file. A paper consumes the settled contract and never stores the universal manual. A paper binds a question it cannot answer to a bank answer, by path, across a wall it may not reach through in any other way.

The evidence banks are not a folder of this skill. They are owned elsewhere, and nothing on this board rules their contents.

No runtime skill may require an open Q page, and no paper's state may be inferred from a design board. A design record is never a runtime dependency: delete any board and every skill still runs.

A board is ruled by its owner alone and consulted by everyone else. This board rules `①` and, for the contract half, `③`. It never rules `④`.

## Log
260726 · Grew from four folders to eight, in four pairs, after JL asked whether the board tool should be numbered. Every THING has a board, so its board is `⑥`. Then JL's synthesis reframed the whole map: `①` writes the paper and owns NEITHER channel out of it. `③` is the human channel, `⑤` the evidence channel. Renumbered so producers come before product, so crossing ⒝ reads `① ＋ ③ ──▶ ⑦ AND ⑧`. 383 glyphs preserved through the swap.
