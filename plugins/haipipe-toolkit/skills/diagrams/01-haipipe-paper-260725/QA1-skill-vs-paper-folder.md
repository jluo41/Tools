# Two folders, two kinds of truth
state: 🟡 PARTIAL
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
