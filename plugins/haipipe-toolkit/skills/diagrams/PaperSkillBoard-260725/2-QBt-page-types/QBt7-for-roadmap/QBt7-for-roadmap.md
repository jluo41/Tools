# QBt7 · Plan the campaign and register what comes back, one page

state: ✅ SETTLED · 0.3.1 · plan and intake on one page · absorbed the Collection page
page-type: roadmap
owner: JL
method: one ledger row per block, released by a person, settled lap by lap onto the Seed

## Opening
Where does a paper plan its evidence campaign, and where do the receipts land when the work comes home?
Roadmap is both, on one page (`SD02-roadmap`): BLOCK rows serving Seed E-rows on the way out, lap divisions registering QA receipts on the way back.
A block is a task group, its jobs are task folders, its runs are configurations, addressed `B<n>T<n>r<n>`.
The page plans and registers, and never executes; QA files stay the substance: register, never restate.

**Where this page sits**: journey phase P2, the other half of the establish loop; gates G2 (release) and G3 (lap settle) both read this page, and the loop exits only through the Seed at G4.

**Why it matters**: without one campaign page, dispatch intent and landed receipts keep separate books and the Seed's E-rows flip on memory.

## Writing Style
One ledger row per block: the E-row it serves, executor, done-when, budget, and the person's release mark.
Register receipts by QA path; never copy an answer's body onto this page.

## Diagram
**The establish loop**: the Seed states gaps, the Roadmap runs the campaign.

```text
🌱 Seed §6 gaps (⬜/🔨 E-rows)
   │ G2: every open E-row has a ▶️ released block row or a waiver ·
   │     a person releases, block by block — a machine only proposes
   ▼
🗺 SD02-roadmap
├── Mission · Block Board (one row per block B<n>)
├── B1 · B2 · … block divisions (jobs T<n>, runs r<n>)
├── L1 · L2 · … lap divisions ── landed QA receipts
│      G3: done-when holds · every card binds a landed QA path ·
│           settle PROPOSALS → the Seed alone flips E-rows ✅
└── Open (last)
   gaps remain → next lap · gaps closed or waived → face G4 on the Seed
```

## Content
### 1 · Roadmap contract
**Fixed grammar**: division 1 is Mission, division 2 the Block Board, then one division per block in id order, one per lap in id order, Open last.

```text
mission · block board · B<n> blocks · L<n> laps · open
```

Each block row names the Seed E-row it serves, its executor, done-when, budget, and the person's release; each block's home is a task group under the paper's `tasks/`.
The lap face registers what came home: dispatch cards bind landed QA paths, and the lap's settle proposals cite them.
Two pens, never crossed: the Roadmap proposes settles; the Seed alone writes E-row flips, each flip citing the QA file its block row landed.
There is no separate Collection page: the lap divisions are the campaign's intake, and boards still holding an `SD03-collection` page from the earlier journey are grandfathered.

## Aims
### A1 · 🗺 Roadmap contract
- A1.1 · Every open Seed gap has a released route or a visible waiver.
  **Done when:** G2 reads clean: each 🔨/⬜ E-row names a ▶️ block row or a waiver on the Seed's Log.
- A1.2 · Every landed receipt is registered where the plan promised it.
  **Done when:** G3 reads clean: done-when holds, every dispatched card binds a landed QA path, and the settle is written on the Seed.

## States
### A1 · 🗺 Roadmap contract
- ✅ A1.1 · The 0.3.x contract makes G2 a readable assertion over the Block Board.
- ✅ A1.2 · G2 and G3 have fired live (2 boards, 1 field test, 3 gaps patched), per the family status of 260828.

## Files
- `../../paper/page-types/haipipe-page-for-roadmap/SKILL.md` · source contract
- `../../paper/haipipe-paper-workflow/SKILL.md` · gates G2/G3 and the establish loop

## Log
260828 · Specimen minted during the field repair. Roadmap entered the family with the journey (260824) as the route phase's authority page; this morning it absorbed the Collection page (0.3.0) and pinned each block's task-group home (0.3.1). Known knife point: the contract file says 0.3.1 while its CHANGELOG labels the same law 0.4.0; the family's own status lists the reconcile as open.
