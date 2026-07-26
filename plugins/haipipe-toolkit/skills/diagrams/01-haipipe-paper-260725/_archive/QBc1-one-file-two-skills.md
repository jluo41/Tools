# One file, two skills: what does each own?
state: 🟡 PARTIAL
owner: JL
method: keep one shared file; state the ownership line rather than leaving it to habit

## Question
When a lifecycle page is written by one skill and rendered by another, which one owns it?

The answer that was chosen is deliberately blunt: there is ONE file. The stage's artifact and the board's page are the same markdown, not two representations kept in step. That decision removed an entire class of bug before it existed, and it created a smaller, sharper problem in its place, which is that two skills now write to one file and nothing states who may touch which part.

## Boundary
- ✅ Covered here
  The ownership line inside a shared page, and what each skill may write.
- ↪ Covered elsewhere
  What the artifact contains is `QBa1`; the Content boundary is a division of this page, absorbed 260726; what the file is called is `QBa2`; who creates it is `QBc4`.

## Diagram
```
 THE ALTERNATIVE THAT WAS TRIED AND REJECTED

  ✗ TWO FILES + AN ADAPTER          ✅ ONE FILE
   paper writes its format           S-Main-7-results.md
        │  adapter                    ╱          ╲
   board reads and renders     the stage's       the board's
        ▼                      ARTIFACT           PAGE
   a rendering that can          ── the same bytes, no adapter ──
   silently disagree with
   its source, and a comment
   layer with nothing to
   write back to

 ONE FILE REMOVED A BUG CLASS AND CREATED A SHARPER ONE:
 two skills now write to one file, so the line has to be stated.

 WHO MAY WRITE WHAT
 ┌ S-Main-7-results.md ─────────────────────────────────────────┐
 │ # title / state: / owner:            ◄ BOARD  furniture      │
 │ <!-- haipipe:contract:start -->                              │
 │   inherited requirements, gate states  ◄ BOARD  GENERATED,   │
 │ <!-- haipipe:contract:end -->            will be OVERWRITTEN │
 │                                                              │
 │ ## Question · Boundary                ◄ PAPER  substance     │
 │ ## Content        the stage's actual PRODUCT                 │
 │ ## Items to Finish · Where we are     written by DRAFT and   │
 │                                       REVISE, ruled at CHECK │
 │                                                              │
 │ …the human, anywhere, any time. It is plain markdown, and    │
 │  that is the whole reason this shape was chosen.             │
 └──────────────────────────────────────────────────────────────┘

 THE PART THAT IS REAL AND UNWRITTEN  ⚠️
   "the managed block is regenerated" lives in the board's CODE and in
   a comment inside the block. It is not in the paper skill's contracts
   at all, which is exactly where an agent writing a stage would look.
```

## Content
### Why one file rather than two
The alternative was an adapter: the paper skill writes its own format, the board reads and renders it. It was tried and rejected, because an adapter means a rendering that can silently disagree with its source, and a comment layer that cannot write back to anything a human edits. One file removes both.

### The ownership line as it actually stands
```
 /haipipe-paper   the page's SUBSTANCE
                  Question · Boundary · Content · Items to Finish · Where we are
                  written by DRAFT and REVISE, ruled at CHECK

 /haipipe-board   the page's FURNITURE and the machine-managed block
                  the section grammar, the state vocabulary,
                  the Stage Contract between its sentinel comments

 the human        anything, at any time; the file is plain markdown and that
                  is the reason it was chosen
```

### The part that is real and unwritten
The Stage Contract block is generated and will be overwritten. Everything else is authored and must never be. That rule exists in the code and in a comment inside the block; it is not in the paper skill's contracts at all, which is exactly where an agent writing a stage would look for it.

### What belongs in Content
(absorbed from the former `QBa1`, 260726: it is this same ownership question asked about one section)

Content is not the Board's description of a stage, its inherited contract, its queue, or its status. It is the thing that stage exists to produce, such as the paper seed, claim ledger, pitch, narrative, visual argument, or reader-facing section.

```
Stage Contract     inherited requirements, venue rules, writing style
Content            this stage's actual product
Items to Finish    work still owed before the gate
Where we are       settled corrections and present state
```

Different stages produce different things. For Section, Content is the section itself. For Display, Content is the visual argument, candidate judgment, caption job, and stable unit meaning. Rendered assets and source files are linked artifacts, not a replacement for Content.

## Items to Finish
- [x] 📄 One file, not two
      The stage artifact and the board page are the same markdown; no adapter exists.
- [x] 📚 Separate Content from Board furniture
      The S page is one file, but its sections have distinct owners and jobs.
- [ ] 📐 State the Content product in every stage contract
      A fresh worker should know what belongs in Content before it writes.
- [ ] 🔍 Remove inherited and status material from existing Content
      Migration must preserve the substantive artifact while relocating only misplaced material.
- [ ] 🧪 Cold-read one page per stage kind
      The Content heading alone should accurately name what the reader finds below it.
- [ ] 📐 Write the ownership line into the paper skill
      A stage worker reads `stage.md`, not the board's source. If the rule that the managed block is regenerated lives only in the board's code, a worker will eventually hand-edit it.
- [ ] 🧠 Rule what happens when the board's grammar changes
      The section shape rule changed on 2026-07-25 and nine pages were re-levelled by hand. Decide whether a grammar change is a migration the board runs, or a duty the paper skill inherits.

## Where we are
The one-file decision is implemented and has held. The ownership line is understood by whoever is working and written down nowhere a stage worker reads.

## Files
- `stages/*/stage.md`
  Where the ownership line should be stated.
- `haipipe-board/src/stage_contract.py`
  The only writer of the managed block.
