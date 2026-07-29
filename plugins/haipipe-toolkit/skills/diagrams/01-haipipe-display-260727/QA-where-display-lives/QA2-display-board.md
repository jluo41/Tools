# The Display Board and the Paper Board
state: ✅ SETTLED
owner: JL
method: give layer design and one paper unit different Boards because they answer different questions

## Question
Which Board holds Display work?

The Display design Board holds reusable rules for the family.
A paper lifecycle Board holds the live decision for one concrete display unit.

## Boundary
- ✅ This Board owns the reusable Display model, renderer taxonomy, and shared contracts.
- ✅ A paper's `S-Display-N` page owns one concrete visual argument and its human gate.
- 🚫 This Board does not duplicate a paper's claims, caption text, candidate choice, or data values.

## Diagram
```text
DISPLAY DESIGN BOARD                         PAPER LIFECYCLE BOARD
skills/diagrams/01-haipipe-display.../       <paper>/0-lifecycle/
  reusable rules                               S-Display-N-<slug>.md
  renderer choices                              one unit's claim, Intake, wrapper, gate
             │                                               │
             └──────── shared contracts ────────────────────┘
```

## Content
### One Board explains the system
This Board answers questions such as which renderer fits a table and who may promote a candidate.
It is the place to change a reusable rule deliberately.

### One S page runs a unit
The paper page records the display's brief, provenance chain, exact wrapper, open work, and review decision.
It is where a human reviews the specific visual rather than the generic mechanism.

## Items to Finish
- [x] 🧩 Keep the reusable Board outside individual papers
      It lives beside the Display skills under `skills/diagrams/`.
- [x] 📄 Make the paper's `S-Display-N` page the unit-level control surface
      The Paper adapter and stage template name it as the unit's human gate.

## Where we are
The two Boards are complementary rather than nested copies.

## Files
- `paper/1-lifecycle/haipipe-paper-stage/stages/4-display/template.md`
  The concrete paper-unit page shape.
- `paper/1-lifecycle/4-display/ref/paper-adapter.md`
  The bridge between the two layers.

## Law
Law: Reusable rules live on the Display Board; a visual decision lives on its paper's S-Display page.

## Log
260727 · Established the two-Board split while designing the Display control plane.
