# Who creates a page?
state: ✅ SETTLED
owner: JL
method: one creator; the other consumes what it made

## Question
When a stage runs for the first time and its page does not exist yet, which skill brings it into being?

Both currently claim it. The paper skill's DRAFT phase writes the artifact from a stage template. The board's tooling has a `new` verb that creates a page with its metadata and its managed contract block. Neither one knows about the other, so whichever runs first wins and the second finds a file it did not expect.

## Boundary
- ✅ Covered here
  Creation of a lifecycle page: who runs it, and what the new page contains.
- ↪ Covered elsewhere
  What goes in the page afterwards is `QBa1`; Content composition is a division of this page, absorbed 260726; the naming is `QBa2`; the ownership of the parts is `QBc1`.

## Diagram
```
 BOTH SKILLS CLAIMED CREATION, AND NEITHER KNEW ABOUT THE OTHER

  DRAFT (paper)                    stage.py new (board)
  the stage's CRAFT                the board's GRAMMAR
  · disciplinary content           · title / state / owner
  · the section's jobs             · requires / style-from / provides
  · placeholder grammar            · the managed Stage Contract
  · the Q-consumer block           · Pages insertion
        ╲                                ╱
         ╲    whichever ran SECOND       ╱
          ╲   overwrote or sat beside   ╱   ⚠️
           ╲         the first         ╱

 THE RULING: ONE PUBLIC CREATOR, ONE PRIMITIVE
   Paper Stage  ──calls──►  stage.py new   as a shell primitive
   Board owns   filename · face grammar · Pages insertion · managed block
   Paper owns   the stage-specific Content jobs

 THE COMPOSITION THAT IS DESIGNED AND UNBUILT   ⚠️
   a new page's Content should resolve from four layers, in order:
     1  stage template     the disciplinary jobs and the gate
     2  venue blueprint    section order, reader expectation, length
     3  Stage Contracts    accepted upstream requirements
     4  page authoring     materialize the resolved headings
   composed ONCE at creation, then authored. Not recomputed per render,
   so the managed block may refresh without touching Content.

   today  stage.py new writes a GENERIC STUB.
   so the real question was never who creates the page.
   It is who performs that composition, and with whose knowledge.
```

## Content
### The two creators
```
 DRAFT            copies the stage template and fills it: the disciplinary content,
                  the section's jobs, the placeholder grammar, the Q-consumer block

 stage.py new     writes the face: title, state, owner, requires/style-from/provides,
                  the managed Stage Contract, and a generic Content stub
```

### Why this is not merely a race
They compose different things. DRAFT knows the stage's craft and the venue's expectations; `stage.py new` knows the board's grammar and the dependency graph. A page needs both, and today whichever runs second either overwrites or sits beside the first.

### The composition that is designed but unbuilt
The intended answer is on record: a new page's Content should be composed at creation from four layers, the board shell for layout, the stage template for base subsections and gates, the venue template for reader expectations and length, and the previous stages' contracts for accepted inputs and open requirements. Resolution order is stage, then venue, then contracts. That is written down and nothing implements it: `stage.py new` still writes a generic stub.

So the real question is not who creates the page, but who performs that composition, and with which of the two skills' knowledge.

### The composition order
(absorbed from the former `QBa2`, 260726)

```
1. stage template       the disciplinary jobs and gate
2. venue blueprint      section order, reader expectation, length, and style
3. Stage Contracts      accepted upstream requirements and explicit dependencies
4. page authoring       materialize resolved direct headings in ## Content
```

The creator does not keep recomputing the page on every render. The composed headings become authored Content and change only through normal revision, while managed Stage Contract text may refresh independently without overwriting Content.

Template lookup follows the same one-resolver rule as everything else: the stage registry identifies the stage template, the pinned venue page is the first venue source, and the venue playbook is only a fallback or a deeper source behind the pinned contract.

## Law
Paper Stage is the only public creator. It selects the paper stage and its template, then calls the Board's `stage.py new` as a shell primitive. Board owns filename, face grammar, Pages insertion, and the optional managed Stage Contract; Paper owns stage-specific Content jobs.

The first slice composes Board shell + stage template. Venue-template and prior-contract composition remain later work for venue-aligned per-unit pages.

## Items to Finish
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

## Where we are
The creator and composition owner are ruled. A Seed page now passes an end-to-end Board smoke test from one command and is idempotent. The remaining acceptance test is a venue-aligned section page, which needs the later venue-template composition slice.

## Files
- `stages/*/template.md`
  The disciplinary half of what a new page needs.
- `haipipe-board/stage.py`
  The board half, currently writing a generic stub.
- `haipipe-paper-stage/create-page.py`
  The public composition path; Board shell first, selected stage scaffold second.
