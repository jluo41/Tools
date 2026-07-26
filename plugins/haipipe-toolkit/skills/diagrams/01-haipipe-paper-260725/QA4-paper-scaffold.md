# ⑦ The paper: what exists on disk
state: 🟡 PARTIAL
owner: JL
method: create the smallest runnable paper, then add manuscript machinery only when the lifecycle reaches it

## Question
What should exist on disk when a new paper is created, and what should appear only later? A new paper gets a control plane and exactly one runnable page. Everything else stays absent until its unit is allocated, so nothing speculative accumulates that nobody wrote and nobody dares delete.

The current family map describes a complete manuscript folder, while the folder skill creates empty lifecycle containers and delays LaTeX. A Board-first paper needs a smaller but runnable answer: one control plane, one first page, and no speculative section or Display files.


The approach is to create the smallest thing that is already runnable, and let every later page arrive only when its unit is allocated. What we want is a new paper that works from minute one and never accumulates speculative files nobody wrote and nobody can safely delete.
## Boundary
- ✅ Covered here
  Initial paper creation, absent-until-written lifecycle pages, and the later manuscript upgrade.
- ↪ Covered elsewhere
  Which folder this folder is at all is `QA1`; its own board is `QA5`; Markdown versus TeX authority is `QBa1`; page ownership is `QBc1`; state authority is `QBc3`; page creation is `QBc4`.
## Diagram
```
   DAY 0 · everything a new paper gets, and nothing more

   Paper-X/
   ├── README.md          ├── 0-displays/     empty, real
   ├── STATUS.md          └── 1-probes/       empty, real
   └── 0-lifecycle/
       ├── board.md            ← the control plane exists from minute one
       └── 0-seed/
           └── S-Seed-0-seed.md   ← exactly one page, and it is runnable

   ────────────────────────── the lifecycle runs ──────────────────────────▶

   every other S page is ABSENT UNTIL ITS UNIT IS CREATED
     resource · claims · venue · pitch · narrative
     Display-1..N · Main-1..N · Appendix-A..F · Submission-0..3
     Round-1..N, each in 0-lifecycle/7-round/ with its own letters beside it

   ✗ never created in advance: a request file, a Handoff sidecar,
     a generic section stub, an empty stage tree

                                          ▲
                          MANUSCRIPT UPGRADE, at the Display
                          or section frontier and not before:
                          venue shell · 0-sections/ · .bib
                          · build and export adapters
```

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
└── 1-probes/
```

### Absent until allocated
Resource, claims, venue, pitch, narrative, Display, section, appendix, and submission pages appear only when their unit is created.
No request file, Handoff sidecar, generic section stub, or empty stage tree is created in advance.

### Manuscript upgrade
At the Display or section frontier, add the selected venue's manuscript shell, section outputs, bibliography, configuration, and build or export adapters.
The exact generated-versus-authored boundary follows `QBa1`.

### What crosses this folder's edge
```
 ① ──▶ ⑦  the skill set     IN. A stage run writes here, and only a stage run
                            does. The paper CONSUMES the settled contract and
                            never stores a copy of it: no SKILL.md, no stage
                            contract, and no venue pack is ever copied in.

 ⑧ ──▶ ⑦  the paper board   IN, and this is the edge that surprises people.
                            0-lifecycle/ is INSIDE this folder, and it is where
                            the paper's real Content lives. 0-sections/*.tex is
                            GENERATED from those pages, never hand-authored, so
                            the manuscript files here are build products.

 ⑦ ──▶ the wall             OUT. 1-probes/ holds one entry per question this
                            paper cannot answer, each bound BY PATH to a
                            QA/<n>-<slug>.md in tasks/ or discoveries/. The
                            paper may not compute and may not read the
                            literature; it asks, and it records where it asked.

 ⑦ ──▶ ②                    NOTHING. A paper never writes to a design board.
```
So almost nothing here is authored in place. The prose arrives from `⑧`, the numbers and citations arrive across the wall, and the build products are generated. What this folder genuinely owns is the shape: which containers exist, and which of them are allowed to be empty.

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


The scaffold shape is ruled. One thing on this page is not: `STATUS.md`'s remaining role. Identity and maturity may stay there, but the active frontier must not compete with S-page state, and that line has never been drawn. Until it is, this page describes a folder with two possible answers to "where is this paper", which is exactly what `QA5` forbids.

Reopened to 🟡 on 260726 (JL): a face carrying an unruled sub-question is not settled, whatever emoji its item wears.
## Files
- `3-deliver/1-build/haipipe-paper-folder/SKILL.md`
  The current scaffold contract.
- `README.md`
  The conflicting complete-folder description.
- `0-enter/haipipe-paper-enter/SKILL.md`
  The entry path that should create and open the initial Board.

## Law
A new paper is created Board-first and minimal: README, STATUS, the four containers, `0-lifecycle/board.md`, and one Seed page. That is enough to be runnable, and nothing more is created.

Every other lifecycle page is absent until its unit is allocated. No request file, Handoff sidecar, generic section stub, or empty stage tree is created in advance. Manuscript machinery is an upgrade performed at the Display or section frontier, never at creation.

## Log
260726 · Rounds moved inside the lifecycle (JL). `1-rounds/` is retired as a top-level container: the round page and its received artifacts both live in `0-lifecycle/7-round/`. One page per round, not four. `haipipe-paper-folder` now scaffolds three containers, not four; `haipipe-paper-round` still owns a superseded five-file contract and needs a rewrite.
