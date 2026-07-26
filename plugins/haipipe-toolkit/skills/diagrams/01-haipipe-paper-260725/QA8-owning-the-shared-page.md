# The ①/③ seam: who owns which region of a shared page
state: 🟡 PARTIAL
owner: JL
method: one seam at a time, each ruled for its own reason

## Question
Two skills write one markdown file. Which regions belong to which, and what happens at every seam between them? Five seams were ruled separately and each for its own reason: who may write which section, which dependency declaration binds, where a paper's state lives, who brings a page into being, and how far the board may go in running paper-specific code.

`QA4` draws the collaboration: `①` owns the substance, `③` owns the shell, the render and the write-back, and they never contend for the same lines. This face is that ownership line in detail, seam by seam, because each seam was ruled separately and each was ruled for a different reason.

Five seams exist: who may write which section, which of two dependency declarations binds, where a paper's own state lives, who brings a page into being, and how far the board may go in running paper-specific code.

## Boundary
- ✅ Covered here
  What each skill may write on a shared page, which declaration is authoritative, where paper state lives, who creates a page, and how far the `dialect: paper` seam reaches.
- ↪ Covered elsewhere
  The collaboration as a whole is `QA4`; how work is DRIVEN from a page is `QA9`; what a board is, and its face grammar, belong to the tool's own board at `../01-boardform-260722/`.

## Diagram
```
 FIVE SEAMS IN ONE MARKDOWN FILE, EACH RULED FOR A DIFFERENT REASON

 ┌ S-Main-7-results.md ─────────────────────────────────────────┐
 │ # title / state: / owner:              ◄ ③ BOARD  furniture  │ ① who writes
 │ <!-- haipipe:contract:start -->                              │   which region
 │   inherited requirements + GATE STATES  ◄ ③ GENERATED,       │
 │ <!-- haipipe:contract:end -->             will be OVERWRITTEN│
 │                                                              │
 │ ## Question · Boundary                 ◄ ① PAPER  substance  │
 │ ## Content     the stage's actual PRODUCT                    │
 │ ## Items to Finish · Where we are      DRAFT and REVISE write│
 │                                        CHECK rules           │
 │ …the human, anywhere, any time. It is plain markdown, and    │
 │  that is the whole reason this shape was chosen.             │
 └──────────────────────────────────────────────────────────────┘

 SEAM 2 · WHICH DEPENDENCY DECLARATION BINDS
    stage.md read_order:   an ORDER · craft · hand-maintained · no power
    the page requires:     a SET · rendered · carries the upstream's
                           GATE STATE  ◄ only one form can say
                           "it exists AND has not passed"

 SEAM 3 · WHERE PAPER STATE LIVES
    ✗ STATUS.md current_layer   hand-written, disagreed with its own
                                gate ledger for MONTHS
    ✅ the frontier is READ      the earliest page whose gate has not
                                passed. Derived, so it cannot disagree
                                with itself. STATUS.md now MIRRORS.

 SEAM 4 · WHO CREATES A PAGE
    Paper Stage is the ONLY public creator ──calls──► stage.py new
    board owns filename · face grammar · Pages insertion · managed block
    paper owns the stage-specific Content jobs

 SEAM 5 · HOW FAR THE BOARD MAY GO IN RUNNING PAPER CODE
    a dialect holds GRAMMAR + RESOLUTION, never rendering, never writing.
    THE LAW IS A TEST: delete src/dialect_paper.py and every board that
    does not declare `dialect: paper` renders BYTE-IDENTICAL.
    verified 260726 on 01-boardform-260722  138c274a ──► 138c274a  ✅
    (this board declares a dialect of its OWN now, so the test
     moved to one that does not)

 WHY ONE FILE AND NOT TWO
    the alternative was an adapter, tried and rejected: a rendering that
    can silently disagree with its source, and a comment layer with
    nothing to write back to. One file removed both, and created these
    five seams in their place.
```

## Content
### One file, two skills: what does each own?
#### Why one file rather than two
The alternative was an adapter: the paper skill writes its own format, the board reads and renders it. It was tried and rejected, because an adapter means a rendering that can silently disagree with its source, and a comment layer that cannot write back to anything a human edits. One file removes both.

#### The ownership line as it actually stands
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

#### The part that is real and unwritten
The Stage Contract block is generated and will be overwritten. Everything else is authored and must never be. That rule exists in the code and in a comment inside the block; it is not in the paper skill's contracts at all, which is exactly where an agent writing a stage would look for it.

#### What belongs in Content
(absorbed from the former `QB9`, 260726: it is this same ownership question asked about one section)

Content is not the Board's description of a stage, its inherited contract, its queue, or its status. It is the thing that stage exists to produce, such as the paper seed, claim ledger, pitch, narrative, visual argument, or reader-facing section.

```
Stage Contract     inherited requirements, venue rules, writing style
Content            this stage's actual product
Items to Finish    work still owed before the gate
Where we are       settled corrections and present state
```

Different stages produce different things. For Section, Content is the section itself. For Display, Content is the visual argument, candidate judgment, caption job, and stable unit meaning. Rendered assets and source files are linked artifacts, not a replacement for Content.

#### Where that seam stood
The one-file decision is implemented and has held. The ownership line is understood by whoever is working and written down nowhere a stage worker reads.

### Two declarations of the same dependency
#### The two forms
```
 stage.md  read_order:        optional craft: which material DRAFT opens first
                              not a dependency graph

 the page  requires:          optional dependency declaration
                              rendered by sync into a Stage Contract that names
                              each source, its GATE STATE, and what it provides
```

#### The evidence
The section-edit contract's old `inputs:` included `z-structure`, a dangling architecture path. That stale entry has now been removed rather than copied into the dependency graph.

Meanwhile `requires:` carries something `inputs:` cannot: the upstream page's gate state at the moment of rendering. A stage can therefore see that its input exists AND has not passed its gate, which is a different and more useful fact than a path.

#### The honest case for keeping inputs
A reading list is an ORDER, and `requires:` is a set. "Open the venue blueprint before the claims ledger" is craft guidance that a dependency graph does not express. If `inputs:` dies, that ordering has to survive somewhere.

#### Where that seam stood
Settled and implemented. The two contracts that carried `inputs:` now use `read_order:`; the known dangling `z-structure` entry is gone. A page may leave `requires:` blank without inventing a dependency.

### Where paper-level state lives
#### What went wrong with the hand-maintained version
`STATUS.md` disagreed with itself. Its restart note and its gate ledger pointed at different frontiers, and an embedded check block recorded that `current_layer` had been left untouched because the contradiction needed a human ruling. A whole board face existed for months to resolve which of two fields in one file was true.

#### The ruling that replaced it
The frontier is READ, not stored: it is the earliest page in the pipeline whose gate has not passed, and every page carries its own `state:`. `STATUS.md` mirrors the board rather than deciding it. A hand-written pointer to the current stage is exactly what started disagreeing with the gate record, so it stopped being written.

#### What is unsettled
That ruling was made on one paper. The skill still describes `STATUS.md` as the machine state each stage updates, so a stage worker following its contract would keep writing a field that no longer decides anything. Either the skill adopts the ruling, or the paper is out of step with its own skill.

#### Where that seam stood
Ruled on one paper, unadopted by the skill. The two are currently in a state where following the contract would undo the ruling.

### Who creates a page?
#### The two creators
```
 DRAFT            copies the stage template and fills it: the disciplinary content,
                  the section's jobs, the placeholder grammar, the Q-consumer block

 stage.py new     writes the face: title, state, owner, requires/style-from/provides,
                  the managed Stage Contract, and a generic Content stub
```

#### Why this is not merely a race
They compose different things. DRAFT knows the stage's craft and the venue's expectations; `stage.py new` knows the board's grammar and the dependency graph. A page needs both, and today whichever runs second either overwrites or sits beside the first.

#### The composition that is designed but unbuilt
The intended answer is on record: a new page's Content should be composed at creation from four layers, the board shell for layout, the stage template for base subsections and gates, the venue template for reader expectations and length, and the previous stages' contracts for accepted inputs and open requirements. Resolution order is stage, then venue, then contracts. That is written down and nothing implements it: `stage.py new` still writes a generic stub.

So the real question is not who creates the page, but who performs that composition, and with which of the two skills' knowledge.

#### The composition order
(absorbed from the former `QB10`, 260726)

```
1. stage template       the disciplinary jobs and gate
2. venue blueprint      section order, reader expectation, length, and style
3. Stage Contracts      accepted upstream requirements and explicit dependencies
4. page authoring       materialize resolved direct headings in ## Content
```

The creator does not keep recomputing the page on every render. The composed headings become authored Content and change only through normal revision, while managed Stage Contract text may refresh independently without overwriting Content.

Template lookup follows the same one-resolver rule as everything else: the stage registry identifies the stage template, the pinned venue page is the first venue source, and the venue playbook is only a fallback or a deeper source behind the pinned contract.

#### Where that seam stood
The creator and composition owner are ruled. A Seed page now passes an end-to-end Board smoke test from one command and is idempotent. The remaining acceptance test is a venue-aligned section page, which needs the later venue-template composition slice.

### The board runs paper code: where is that boundary?
#### Why shape A, stated as a trade rather than a preference
The Diagram lays out the three. B is the one that deserves an argument rather than a dismissal: it buys clean ownership and sells the single property that makes a chip trustworthy, which is that the board can assert what came out of a dialect. Every invariant the board enforces (no chip inside a code span, no evidence that vanishes when scripts are stripped, no marker rewritten in a discussion lane) is enforceable only because the board owns the rewriting step.

With exactly one dialect in existence, a plugin ABI is a cost with no buyer. The trigger for revisiting is named rather than left to taste: a SECOND dialect.

#### The law is a test, and that is the point
`build.py` guards the import behind the declaration and catches `ImportError`, so a missing dialect degrades to plain text rather than crashing. Verified 260726 by moving the module aside and rebuilding both boards.

Stating it as a delete-test rather than a principle is what catches the real failure. Nobody is going to move `dialect_paper.py` into `body.py`; what will happen is one paper-shaped `if` inside a generic function, and that breaks the hash.

#### What a dialect module may not do

- It may not render. It returns `(state, label, tooltip)`; `body.py` decides what a chip is.
- It may not write. It reads a paper tree and holds an index, and nothing else.
- It may not be reached unless a board declared it. The declaration is on the board, never a default.

#### Where that seam stood
Ruled and enforced for the one dialect that exists. The rule is verified but not automated, and it is not written anywhere a future dialect author would look. Both gaps are items above, and neither blocks the remaining `QC` and `QD` slices.

### This board now runs the seam it rules
Since 260726 the design board declares `dialect: paper` against `_fixture`, a small synthetic paper inside its own folder, so the `QC` faces show live chips instead of describing them. The dialect seam became self-demonstrating, and the board became its own regression test: every chip state the design defines is reachable here, including the broken ones.

Turning it on was measured first, not assumed: every marker already written on this board sits inside a fence or backticks, so the collateral was exactly zero chips and only the new examples render.

One consequence, stated rather than discovered later: the delete-test needs a board that declares NO dialect, and this board is no longer one. It runs against `01-boardform-260722`.

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
- [x] 🧠 Rule which declaration is authoritative
      `requires:` on the page, with `inputs:` deleted; or `inputs:` kept and repointed, with a stated reason for the duplication.
- [x] 📐 If deleted: rehome the reading ORDER
      The sequence DRAFT opens things in is real craft. Say where it lives.
- [x] 🧪 Verify no stage reads a path that does not exist
      Whichever survives, this check should pass and today does not.
- [x] 🧭 The frontier is derived, on the consuming paper
      Read off the pipeline from the pages' own `state:` lines; `STATUS.md` mirrors.
- [ ] 🧠 Rule whether this generalizes
      Adopt it in the skill, or state that the MISQ paper is an exception and say what makes it one.
- [ ] 📐 Say what `STATUS.md` is still FOR
      Maturity, round state and the human gate ledger may still belong to it. Frontier does not. Draw that line rather than leaving the file half-authoritative.
- [x] 🧠 Rule the creator
      One entry point. The other becomes a consumer of what it produced.
- [x] 📐 Rule where the four-layer composition runs
      It needs the stage template and the venue template, which are the paper skill's, and the board grammar, which is not. Say which side reaches across.
- [x] 🧱 Choose the four-layer composition
      Stage, venue, upstream contracts, and page ownership have an explicit order.
- [ ] 📐 Define merge conflicts
      State what happens when stage craft, venue form, and upstream requirements disagree.
- [ ] 🧪 Create one page end to end and check it
      A new section page that is board-valid AND carries its stage's real subsection jobs, from a single command.
- [ ] 🧪 Create a venue-aligned section page
      It must be Board-valid and carry the right section jobs without manual restructuring.
- [x] 🧠 Rule where dialect code lives
      Shape A, inside the board, with the boundary stated rather than assumed.
- [x] 🔒 Make the independence claim executable
      Guarded import in `build.py`, plus the byte-identical delete-test.
- [ ] 🧪 Put the delete-test in the build rather than in a session
      It was run by hand. It should run as an assertion or a small check, or it decays into a claim.
- [ ] 📐 Write the rule where a dialect author reads it
      `SKILL.md` says nothing about dialects, so the second one will be written by copying the first and its constraints will travel only by imitation.
- [ ] 🧠 Decide the trigger for revisiting shape B
      Name the condition, most likely a second dialect, so the choice is not re-argued from scratch each time.

## Where we are
Merged 260726 from 5 faces that each ruled one seam of the same joint (JL). Every division, item and Law below is the original's, unchanged; only the framing above is new.

## Files
- `stages/*/stage.md`
  Where the ownership line should be stated.
- `haipipe-board/src/stage_contract.py`
  The only writer of the managed block.
- `stages/5-section-edit/stage.md`
  Four of five inputs archived.
- `0-lifecycle/5-section-edit/6-results/S-Main-7-results.md`
  The same dependencies, generated, with gate states.
- `PHILOSOPHY.md`
  The frontier and maturity axes.
- `0-lifecycle/board.md`
  Carries the ruling in its Topic and Pipeline.
- `stages/*/template.md`
  The disciplinary half of what a new page needs.
- `haipipe-board/stage.py`
  The board half, currently writing a generic stub.
- `haipipe-paper-stage/create-page.py`
  The public composition path; Board shell first, selected stage scaffold second.
- `haipipe-board/src/dialect_paper.py`
  The only paper-aware module in the Board.
- `haipipe-board/build.py`
  The guarded import and the declaration check.
- `haipipe-board/src/body.py`
  The mechanism half: `cite_chips()` and the code-span guard.

## Law
**Two declarations of the same dependency.** Dependencies are optional. When a page declares `requires:`, that field is the authoritative dependency graph. A stage may declare optional `read_order:` to preserve writing craft; it states sequence only and cannot create a dependency.

**Who creates a page.** Paper Stage is the only public creator. It selects the paper stage and its template, then calls the Board's `stage.py new` as a shell primitive. Board owns filename, face grammar, Pages insertion, and the optional managed Stage Contract; Paper owns stage-specific Content jobs. The first slice composes Board shell + stage template. Venue-template and prior-contract composition remain later work for venue-aligned per-unit pages.

**The board runs paper code: where is that boundary.** - Dialect code may hold grammar and resolution. Rendering, invariants and file writing stay with the Board. - A dialect is DELETABLE: the board must build without it, and boards that do not declare it must render byte-identical. - A dialect is opted into by a declaration on the board, never by detection.

## Log
260726 · Merged from five faces that each ruled one seam of the `①`/`③` joint. Every division, item and Law is the original's. Seam labels were renumbered to `SEAM n` after a board-wide glyph sweep collided them with the folder numbers.
