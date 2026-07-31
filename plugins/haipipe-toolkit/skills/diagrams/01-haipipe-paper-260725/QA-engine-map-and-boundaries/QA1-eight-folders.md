# Eight folders in four pairs, and the two channels out
state: 🟡 PARTIAL
owner: JL
method: every THING has a board; name all six, allow four crossings, and treat the banks as a wall rather than a room

## Question
Where does a new rule, file, or page belong? Eight folders exist in four pairs, because every THING has a board that argues its rules: the paper skill, the two shared skills that are its only channels out, and one manuscript. Put something in the wrong one and it either binds nothing, because no runtime reads it, or it becomes wrong for every other paper.

The word "paper" names several different things at once, and they sit in two different repositories. There is a reusable skill that ships. There is a design board that argues about that skill. There is one manuscript. And there is the control plane that manuscript is worked from. Each holds a different kind of truth and each has a different lifetime, but all four are called "the paper work" in conversation, so nothing stops a file from landing in the wrong one.

The failures are not hypothetical and they are not symmetric. A rule written into a working folder binds nothing, because no runtime reads it. Working state written into the manual makes the manual wrong for every other paper. A design argument that runtime starts depending on means the skill can no longer be shipped without its own history. And a paper that keeps a copy of the universal contract drifts from it silently, since nothing compares the two.

One of these has already happened here. This face used to say "design Board" in the singular, collapsing the skill's board and a paper's board into one word. They use the same tool, the same face grammar and the same four `state:` values, so the collapse looked harmless. It was not: the graduation rule, which says a settled ruling leaves the board for the skill, then appeared to apply to a paper's S pages, whose Content must never leave because it IS the paper.

This is the first face on the board because every later ownership question assumes it is answered. `QB2b` can only say who names a file once it is settled which tree the file is in. `QA8` can only draw an ownership line inside a shared page once it is settled which two owners exist. A reader who cannot place a thing cannot rule on it.

## Boundary
- ✅ Covered here
  The six folders in three thing/board pairs, which kind of truth each holds, the only movements allowed between them, and the outside boundary the paper reaches across for evidence.
- ↪ Covered elsewhere
  What is inside the skill set is `QA2`; what is on the skill board is `QA3`; what a new paper gets is `QA6`; what is on a paper board is `QA7`. How a question actually crosses the evidence wall, and what it may cost, is `QB3b`.

## Diagram
```
   ONE DOOR IN.  /haipipe-paper is the only thing a human TYPES,
   and it CALLS the two channels.  Calling is not owning.

                    👤  the human types ONE command
                              │
                              ▼
                    ①  /haipipe-paper
                       resolves the paper · routes · writes ⑦ and ⑧
                       renders NOTHING · computes NOTHING
                              │
               ┌──────────────┴───────────────┐
               │ calls                        │ calls
               ▼                              ▼
    ③ /haipipe-board                ⑤ /haipipe-probe
      THE HUMAN CHANNEL               THE EVIDENCE CHANNEL
      ├ build.py    ⑧ → board.html    ├ organize  the stake stripped
      ├ serve.py    push the URL      ├ match     the bank, read-only
      └ write-back  a click → ⑧'s md  └ dispatch  through a clean agent
               │                              │
               ▼                              ▼
         👁 eyes · clicks · a yes       tasks/ · discoveries/
               │                              │
               └──── back into ⑧ ──┐  ┌── a QA file, bound BY PATH
                                   ▼  ▼
                         ⑦ the paper · ⑧ its board

      the human NEVER types /haipipe-board or /haipipe-probe for
      paper work. Both stay real doors for what is NOT a paper:
      ③ renders five design boards, this one included.
```

```
   ── WHEN ① calls ③.  three moments, not one ──────────────────────

    1 ENTER    resolve root → get-or-create → build.py → serve.py
               the human is looking at ⑧ BEFORE any work starts

    2 AFTER EVERY WRITE TO ⑧          ← the one a naive reading misses
               a stage run, a phase worker, a CHECK gate: each ends
               with a rebuild, or the human is reading a paper that
               no longer exists

    3 BEFORE ① ACTS                   ← the REVERSE direction
               a comment or a > lane arrived through serve.py, so ⑧'s
               markdown changed under ①. Re-read; never cache.

   ── the dependency was ALREADY there ─────────────────────────────
      create-page.py already calls the Board's stage.py to compose an
      S filename. ① could never ship without ③ at the WRITE layer.
      This ruling extends it to the READ layer and makes an existing
      coupling honest; it does not create a new one.

   ── and it removes an ASYMMETRY rather than adding one ───────────
      ⑤ was already dispatched-to: you type /haipipe-paper probe,
      never /haipipe-probe, and ① still never computes an answer.
      ③ alone was typed. That was an accident of history. (JL 260726)
```

```
   ── the four pairs: every THING has a board ──────────────────────
   ┌───────────────┬─────────────────────────┬──────────────────────────────┐
   │ reusable      │ ① skills/paper/         │ ② diagrams/01-haipipe-       │
   │ THE PAPER     │   35 skills · v0.3.2    │     paper-260725/  33 faces  │
   │  SKILL        │   WHAT SHIPS            │     WHAT IS ARGUED ← here    │
   ├───────────────┼─────────────────────────┼──────────────────────────────┤
   │ reusable      │ ③ board/                │ ④ diagrams/01-boardform-     │
   │ THE HUMAN     │   haipipe-board/        │     260722/  30 faces        │
   │  CHANNEL      │   FIRST-CLASS FAMILY     │     READ-ONLY from here      │
   ├───────────────┼─────────────────────────┼──────────────────────────────┤
   │ reusable      │ ⑤ probe/                │ ⑥ diagram/260714-probe-qa/   │
   │ THE EVIDENCE  │   haipipe-probe/        │     a design FOLDER, not a   │
   │  CHANNEL      │   v0.9.9 · 353 lines    │     board. The one gap.      │
   ├───────────────┼─────────────────────────┼──────────────────────────────┤
   │ ONE PAPER     │ ⑦ Paper-X/              │ ⑧ Paper-X/0-lifecycle/       │
   │               │   sections/ 1-probes/ │     39 S faces · 8 families  │
   │               │   WHAT IS WRITTEN       │     WHAT IS WORKED           │
   └───────────────┴─────────────────────────┴──────────────────────────────┘

   ⑤ and ③ are the same KIND of dependency, and the paper skill says so
   about both. haipipe-paper-probe: "the model is not this file's, this
   file is only the paper-side deltas." create-page.py: the same, onto
   the Board's stage.py. Every phase worker in ① is an adapter.

```

```
   ── the four crossings, and nothing else ─────────────────────────

   ⒜  ② ──graduates──▶ ① AND ③        ④ ──graduates──▶ ③
        a ruling reaches ✅ and its Law is COPIED into the owning skill.
        SEVEN of thirteen groups here land in BOTH.            → QA3

   ⒝  ① ──calls──▶ ③, and the two ──together──▶ ⑦ AND ⑧
        two skills on ONE markdown file, never the same REGION.
        Only ③ writes ⑧ from a click. Only ① writes ⑦.
        ① is the single ENTRY; ③ owns the render. → QA4 QA8 QA9

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
③ board tool     THE HUMAN CHANNEL               skills/board/haipipe-board/
④ its board      the rulings that produced IT    diagrams/01-boardform-260722/
⑤ probe layer    THE EVIDENCE CHANNEL            skills/probe/haipipe-probe/
⑥ its record     a design folder, not a board    diagram/260714-probe-qa/
⑦ paper          one manuscript's real content   examples/…/papers/Paper-X/
⑧ its board      that paper's lifecycle state    Paper-X/0-lifecycle/
```
Eight, in four pairs, and two things are true at once. Every THING has a board, which is the pairing. And `①` writes the paper while owning neither channel out of it, which is the shape (JL 260726).

That second reading is the useful one. A paper has exactly two ways to reach anything outside itself: evidence comes in through `⑤ /haipipe-probe`, and a human reaches the work through `③ /haipipe-board`. `①` owns the substance and neither door. Both doors are shared skills whose models this family depends on and does not own, and the paper skill says so about both of them in its own words: `haipipe-paper-probe` is "only the paper-side deltas", and `create-page.py` is the same thing onto the Board's `stage.py`.

Owning neither door is not the same as being reachable only through them, and conflating the two is what made this face disagree with `QA2` for a week. `①` is the SINGLE thing a human types (JL 260726). It calls `③` to build and open the board, and it calls `⑤` to ask across the wall, and in both cases it renders nothing and computes nothing itself. **Calling is not owning.** The test is what happens on failure: when `serve.py` cannot reach the browser, `①` has no fallback renderer of its own to fall back to, because it never had one. It prints the URL and says the push failed.

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

The single-door half HAS graduated, and on the same day it was ruled. `/haipipe-paper` now calls `③` at all three moments: `haipipe-paper-enter` 0.6.1 builds and opens the board on entry and lost its 152-line duplicate text renderer, `haipipe-paper-stage` 0.8.1 rebuilds after every write and re-reads before every read, and the router's Closing Block carries a deep-linked board URL where a 9-stage strip used to sit.

`README.md` still carries the older complete-folder description.

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
260726 · JL asked for a figure of how `/haipipe-paper` calls `/haipipe-board` and `/haipipe-probe`. The opening diagram showed OWNERSHIP and never showed FLOW, so it was replaced with a call-flow figure: one door in, two channels called, and what comes back. Two blocks added beside it: the three moments `①` calls `③` (the middle one, rebuild after every write, is what a naive reading misses), and why this does not break "owns neither channel": the dependency already existed at the write layer via `create-page.py`, and the ruling removes an asymmetry rather than adding one, because `⑤` was already dispatched-to. Crossing ⒝ now reads `① ──calls──▶ ③`. Ruled and implemented the same day; see `QA4` for the ruling itself.

260726 · Grew from four folders to eight, in four pairs, after JL asked whether the board tool should be numbered. Every THING has a board, so its board is `⑥`. Then JL's synthesis reframed the whole map: `①` writes the paper and owns NEITHER channel out of it. `③` is the human channel, `⑤` the evidence channel. Renumbered so producers come before product, so crossing ⒝ reads `① ＋ ③ ──▶ ⑦ AND ⑧`. 383 glyphs preserved through the swap.
