# A Board-first paper scaffold
state: 🟡 PARTIAL
owner: JL
method: create the smallest runnable paper, then add manuscript machinery only when the lifecycle reaches it

## Question
What should exist on disk when a new paper is created, and what should appear only during the manuscript upgrade?

The current family map describes a complete manuscript folder, while the folder skill creates empty lifecycle containers and delays LaTeX. A Board-first paper needs a smaller but runnable answer: one control plane, one first page, and no speculative section or Display files.

## Boundary
- ✅ Covered here
  Initial paper creation, absent-until-written lifecycle pages, and the later manuscript upgrade.
- ↪ Covered elsewhere
  Markdown versus TeX authority is `QC1`; page ownership is `QF1`; state authority is `QF3`; page creation is `QF4`.

## Content
### Initial scaffold
```
Paper-X/
├── README.md
├── STATUS.md
├── 0-lifecycle/
│   ├── board.md
│   └── 0-seed/
│       └── S-Seed-0-seed.md
├── 0-displays/
├── 1-probes/
└── 1-rounds/
```

### Absent until allocated
Resource, claims, venue, pitch, narrative, Display, section, appendix, and submission pages appear only when their unit is created.
No request file, Handoff sidecar, generic section stub, or empty stage tree is created in advance.

### Manuscript upgrade
At the Display or section frontier, add the selected venue's manuscript shell, section outputs, bibliography, configuration, and build or export adapters.
The exact generated-versus-authored boundary follows `QC1`.

## Items to Finish
- [x] 🌱 Choose a minimal scaffold
      A new paper does not receive speculative LaTeX, section stubs, or every future S page.
- [x] 🧭 Make the scaffold Board-first
      `0-lifecycle/board.md` and the first Seed page make the new paper runnable immediately.
- [ ] 📍 Rule the remaining role of STATUS.md
      Identity and maturity may remain there, but the active frontier must not compete with S-page state.
- [ ] 🛠 Update the folder skill
      Replace the empty `0-lifecycle/` contract with the Board-first scaffold after the dependent rulings settle.
- [ ] 🧪 Create one paper and enter it
      A fresh agent should open its Board and work Seed without adding or guessing another control file.

## Where we are
The minimal Board-first scaffold is the selected direction.
The existing folder skill still creates an empty lifecycle directory and has not been changed.

## Files
- `3-deliver/1-build/haipipe-paper-folder/SKILL.md`
  The current scaffold contract.
- `README.md`
  The conflicting complete-folder description.
- `0-enter/haipipe-paper-enter/SKILL.md`
  The entry path that should create and open the initial Board.
