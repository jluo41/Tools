# Two folders, two kinds of truth
state: ✅ SETTLED
owner: JL
method: separate reusable behavior from one paper's live state before assigning any file

## Question
What belongs in the reusable paper skill package, and what belongs in one live paper folder?

The word "paper folder" currently names two different things, so rules, working state, generated artifacts, and design history can drift into the same tree. Every later ownership question depends on drawing this boundary first.

## Boundary
- ✅ Covered here
  The boundary among the design Board, the reusable skill package, a paper instance, and the evidence banks.
- ↪ Covered elsewhere
  The layers inside the skill package are `QA2`; the anatomy of one callable skill is `QA3`; the initial paper instance scaffold is `QA4`.

## Diagram
```
        ┌──────────────────────────────────────────────────────────┐
        │  design Board      diagram/01-haipipe-paper-260725/       │
        │  open reasoning · rulings · why                           │
        └───────────────────────┬──────────────────────────────────┘
                                │  a ruling that reaches ✅ GRADUATES
                                ▼        (and only then)
        ┌──────────────────────────────────────────────────────────┐
        │  skill package     Tools/…/skills/paper/                  │
        │  settled procedures · contracts · scripts · assets        │
        └───────────────────────┬──────────────────────────────────┘
                                │  a paper CONSUMES the contract
                                ▼        it never stores the manual
        ┌──────────────────────────────────────────────────────────┐
        │  paper instance    examples/…/papers/Paper-X/             │
        │  Content · queues · state · comments · deliverables       │
        └───────────────────────┬──────────────────────────────────┘
                                │  binds a question BY PATH
                                ▼
        ┌──────────────────────────────────────────────────────────┐
        │  evidence banks    tasks/ · discoveries/  →  QA/<n>.md    │
        └──────────────────────────────────────────────────────────┘

        ✗ FORBIDDEN, and the thing this face exists to prevent:
          runtime ──▶ design Board       a skill needing an open Q page
          runtime ──▶ Board for state    reading paper state off the design record
```

## Content
### Four spaces
```
design Board    records open reasoning and rulings about how the system should work
skill package   stores settled reusable procedures, contracts, scripts, and assets
paper instance  stores one paper's Content, queues, state, comments, and deliverables
evidence banks  store task and discovery answers that a paper binds by path
```

### Graduation direction
An open Board ruling does not bind runtime behavior.
A settled ruling graduates into the owning skill or reference.
A paper instance consumes the settled contract but never stores the universal manual.

## Items to Finish
- [x] 🧭 Separate the four spaces
      The design Board, skill package, paper instance, and evidence banks have different kinds of truth.
- [ ] 📐 State the boundary in the paper family map
      A fresh agent must be able to place a new rule or artifact without reading this design discussion.
- [ ] 🧪 Check for reverse dependencies
      No runtime skill should require an open Q page or infer paper state from the design Board.

## Where we are
The four-space distinction is accepted as the organizing principle.
It has not yet graduated into the runtime paper skills.

## Files
- `README.md`
  The paper family map that should carry the settled boundary.
- `diagram/01-haipipe-paper-260725/`
  The design record, not a runtime dependency.
- `0-lifecycle/`
  The live Board root inside one paper instance.

## Law
Four spaces, four kinds of truth, and the direction between them is one-way.

An open Board ruling does not bind runtime behavior. A settled ruling graduates into the owning skill or reference, and only then does it bind.

A paper instance consumes the settled contract and never stores the universal manual. No runtime skill may require an open Q page, and no runtime skill may infer paper state from the design Board.
