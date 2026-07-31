# The Display as a split unit
state: 🟡 PARTIAL
owner: JL
method: keep one display identity while separating authoritative rebuild work from the journal-facing projection

## Question
What is one Display unit made of, and which half belongs to paper work versus the submission package?

The earlier “move the whole folder” ruling was incomplete because one unit contains both machinery and deliverable bytes. The implemented answer is a projection boundary: the S page and rebuild workspace live under `0-lifecycle/3-display/`; only `float.tex` and the selected `assets/` project to unnumbered `displays/<unit>/`.

## Boundary
- ✅ Covered here
  What the unit contains, what each part is for, and the authoritative-workspace versus submission-projection split.
- ↪ Covered elsewhere
  WHY a unit has both a page and a folder is `QA3@display`, ruled and not re-argued: "A page decides; a folder renders. Neither replaces the other." What the Intake inside `source/` must carry is `QB2@display`; how `candidates/` is promoted into `assets/` is `QB4@display`; who ASKED for the render that fills them is `QD2`; the caption and label inside `float.tex` are `QD3`; where the float lands is `QD4`.

## Content
### One identity, two projections
Measured practice gives every Display unit one stable S id. That id binds the authoritative page/workspace to its small journal-facing projection.

```
0-lifecycle/3-display/
├── S-Display-1b-research-design.md       AUTHORITY + GATE
└── workspace/S-Display-1b-research-design/
    ├── README.md · source/               rebuild contract
    ├── candidates/ · versions/           selection history
    └── preview.tex · preview.pdf          isolated review

displays/S-Display-1b-research-design/     SUBMISSION PROJECTION
├── float.tex                              caption + label + include
└── assets/                                selected live render only
```

### The delete test, applied honestly
The numbered tree is excluded from the journal cut; the unnumbered tree must compile by itself. Applied member by member:

- `float.tex` · deliverable. It is what `\input` reaches.
- `assets/` · deliverable, restricted to the selected file(s) the float reaches.
- `README.md`, `source/`, `candidates/`, `versions/`, `preview.*` · numbered working state.

The split preserves both rulings: work lives with the Board; the submission projection remains unnumbered and self-contained.

### What this does NOT change
The unit id, label, and manuscript `\ref{}` stay stable. A renderer may rebuild candidates inside the workspace, but only an explicit Display promotion may replace the selected submission bytes.

## Items to Finish
- [x] 📐 Fix the anatomy from the units that exist
      Eight members: page, README, source, candidates, versions, preview, float, and selected assets.
- [x] ⚖️ Rule and apply the split
      Page/workspace under `0-lifecycle/3-display/`; `float.tex` plus selected `assets/` under unnumbered `displays/<unit>/`.
- [x] 📎 Align QA6 with the split
      QA6 now names `displays/` as the submission projection rather than the home of working state.
- [ ] 🧹 Finish legacy cleanup
      Retired flat buckets stay archived; do not let `_old/` or `_old2/` become active owners again.
- [ ] 🧪 Repair and compile the incomplete projection
      `displays/S-Display-4a-main-regression/float.tex` is absent, so Paper projection G4 correctly blocks.

## Where we are
The split is implemented on the MISQ paper and QA6 now agrees with it. The remaining live defect is one incomplete submission projection, which is why G4 blocks.

## Files
- `displays/`
  Journal-facing unit projections; each active unit contains only `float.tex` and selected `assets/`.
- `0-lifecycle/3-display/`
  `S-Display-*` authority pages plus `workspace/` rebuild state.
- `0-lifecycle/3-display/build-displays.py`
  Projects selected display bytes into the unnumbered submission tree.

## Law
One Display unit has one identity and two filesystem roles. Board authority and rebuild state stay numbered; only the selected `float.tex` and assets enter the unnumbered journal projection.

## Log
260730 · Reconciled the 260727 whole-folder move with QA6's submission cut: split authority/workspace from the journal-facing projection and recorded the one incomplete projected unit.
