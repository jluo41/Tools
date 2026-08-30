# Paper skill family

`paper/` composes a manuscript from evidence-bearing Board Pages. The active
architecture is Page-first. The former numbered S-stage runtime was retired
and DELETED 260822 rather than parked; no `_old/` archive exists here.

## Active architecture

Six phases, each named by its authority page, gated by
`haipipe-paper-workflow` (journey 0.6.0, JL 260828); the venue bank is a
library outside the journey:

```text
P0 Ideation (ideate)     SD00 · the repo is minted with this page · sends one
                         idea to its Seed
P1 Seed (establish)      SD01 · one per paper · venue-free · E-board with
                         novelty column
P2 Roadmap (route)       SD02 · block rows serving E-rows · person-released ·
                         then dispatch cards and receipts, lap by lap, on the
                         same page
   ↺ P1↔P2 = the establish loop · exits only through the Seed at G4
P3 Narrative (tell)      NA · one per desk · §1 binds a bank Venue Page
P4 Section (realize)     one per map row · then assemble (a verb) at G6
P5 Round (respond)       in the desk's B group · routes each concern once →
                         Seed / Narrative / Section · gates G0-G7 in the
                         workflow file
```

Each Page runs the shared workflow and owns the evidence it uses:

```text
OUTLINE ⇄ PROBE ⇄ EVIDENCE → DRAFT → REVISE/COMPILE → CHECK

Probe family
├─ PageX      accepted Pages · runs in OUTLINE
└─ QA Probe   Task/Discovery · runs in PROBE/EVIDENCE

<page-dir>/
├── <page>.md
├── outline/
├── pagex/       Probe's accepted-Page lane
├── probe/       Probe's Task/Discovery QA cards, proof, and values
├── bibex/       citation cards and bibliography material
├── display/     zero or more independently accepted displays
├── latex/       generated when requested
└── word/        generated when requested
```

Values have a Page-local surface but no `value/` storage folder: each value
lives inside one probe card's proof and `## Values` block and is cited as
`PP<NN>.v<n>`.

There is no View layer. Literature, Value, and Display are Page-local plugin
lanes, not Page Types.

## Active files

```text
paper/
├── haipipe-paper/
│   └── SKILL.md              one public Paper door and routing contract
├── haipipe-paper-workflow/
│   └── SKILL.md              the six-phase gate machine; transitions only
├── page-types/
│   ├── haipipe-page-for-ideation/
│   ├── haipipe-page-for-seed/
│   ├── haipipe-page-for-roadmap/
│   ├── haipipe-page-for-venue/
│   ├── haipipe-page-for-narrative/
│   ├── haipipe-page-for-section/
│   ├── haipipe-page-for-round/
│                             (retired literature/value/display/dash Page Types deleted 260822)
├── venue/                    the shared QBv desk bank (bank/), prose playbooks,
│                             and the literature bank
└── TODO.md                   open issues future sessions pick up (task-family format)
```

## Family status

as of 2026-08-28 · regenerate with `/skill-set-status paper` · this block is a dated receipt, never a second authority

Five classes, five column sets. A row with an empty field record is `(provisional)` whatever its static score.

```text
DOOR · does every road lead somewhere
| skill         | ver   | routes | resolve | stale | scaffold | desc shape |
|---------------|-------|--------|---------|-------|----------|------------|
| haipipe-paper | 0.1.0 | 12     | 12 OK   | 0     | matches  | use-when ✓ |
                  first NUMBERED version, 260828 · unversioned for 125 commits
```

```text
MACHINE · how much of the machine has ever run
| skill                  | ver   | phases | gates | receipt owner | fired live | gazette |
|------------------------|-------|--------|-------|---------------|------------|---------|
| haipipe-paper-workflow | 0.6.0 | 6      | 8     | 8/8           | 4/8        | ✓       |
                                    fired: G0 G2 G3 G4 · never: G1 G5 G6 G7
```

```text
CONTRACT · the eight properties  (① why ② 词 ③ 址 ④ 量 ⑤ 格 ⑥ 据 ⑦ 查 ⑧ 界)
| contract  | ver   | ①| ②| ③| ④| ⑤| ⑥| ⑦| ⑧| total               | field record        |
|-----------|-------|--|--|--|--|--|--|--|--|---------------------|---------------------|
| roadmap   | 0.5.0 | ✓| ✓| ✓| ✓| ✓| ✓| ✓| ✓| 8/8 · EXERCISED     | 2 boards · 1 FT · 3 gaps patched |
| seed      | 0.5.3 | ✓| ✓| ✓| —| ✓| ✓| ✓| ✓| 7/7 · EXERCISED     | 2 boards · settle + G4 ran |
| ideation  | 0.5.4 | ✓| ✓| ✓| —| ✓| ✓| ✓| ✓| 7/7 · EXERCISED     | 2 boards · CHECK routed HOLD |
| venue     | 0.4.0 | ✓| ✓| ✓| —| ✓| —| ✓| ✓| 6/6 · EXERCISED     | 17 desk pages, consumed |
| section   | 0.4.0 | ✓| ✓| ✓| ◐| ◐| —| ✓| ✓| 6/7 · EXERCISED     | 16 pages, most-used |
| narrative | 0.5.2 | ✓| ✓| ✓| ◐| ✗| ✓| ◐| ✓| 6/8 · USED          | 2 pages · G5 never ran |
| round     | 0.3.1 | ✓| ✓| ✓| ✗| ✓| ✓| ◐| ✓| 6.5/8 (provisional) | 0 instances ever |
```

Population: `instances` counts pages on the REAL paper boards under `examples/`.

It excludes the skill-documentation boards under `skills/diagrams/`, whose pages carry a `page-type:` line because they DESCRIBE a type rather than instantiate one.

`haipipe-board/cli/pagetypes.py` counts the WIDE population and so reports higher numbers (round 1, seed 9, section 17); read its table through this law before scoring a tier.

```text
LIBRARY · assets, and whose clock they keep
| asset            | count | neutral | clock          | consumed at | oldest verify |
|------------------|-------|---------|----------------|-------------|---------------|
| venue/bank       | 17    | ✓       | the desk's own | G5 · §1     | ?             |
| venue/playbook-* | 8     | ✓       | the desk's own | narrative   | ?             |
| venue/literature | 3     | ✓       | ad hoc         | narrative   | ?             |
```

```text
CRAFT · a tool, and what it may touch
| skill                          | ver   | last  | lives in | scope       | reversible |
|--------------------------------|-------|-------|----------|-------------|------------|
| haipipe-paper-revise-humanizer | 0.2.6 | 08-05 | writing/ | section tex | ✓          |
```

Knife points, in the order their repair buys the most:

```text
1  MACHINE fired 4/8 · G5/G6/G7 have never left the page · needed: nothing
   written, only run · next hit: the MS narrative opens G5, the first
   decision letter opens G7 — that opening IS the field test
2  collection: 2 live pages and NO contract ships · the expected residue of
   the 260828 merge, now reported by `pagetypes.py --check` · needed: fold
   the two grandfathered SD03 pages, or state the grandfather in the engine
   · next hit: every run of the drift check until one of the two happens
3  narrative ⑤ · the 17-field section-map row carries no per-field law ·
   needed: one legality sentence per field, roadmap-column style · next
   hit: the C5 inheritance decision when the MS round opens

repaired 260828 · DOOR ver MISSING → 0.1.0 · roadmap 0.3.1 → 0.5.0, its
CHANGELOG reordered newest-first with the duplicate 0.2.0 sections merged,
and the executor-home law reversed: a block's task group lives in the task
layer's own home, examples/<Project>/tasks/{G}{NN}_<name>/, never in the
paper repo — the door's scaffold dropped its tasks/ line to match
```

## Ownership

| Layer | Owns |
|---|---|
| `haipipe-paper` | Paper routing, Page graph, assembly, delivery |
| `haipipe-paper-workflow` | the six phases, their gates, phase receipts — never content |
| `haipipe-page` | Shared Page shape and CREATE/WORK ON verbs |
| Paper Page Type | The persistent shape and closing rule of one paper artifact |
| `haipipe-page-workflow` | OUTLINE through CHECK, receipts, stop rules |
| Page plugins | probes, storage-less value joins, citations, displays, PageX, generated formats |
| `haipipe-board` | rendering, serving, checking, and Board registration |

## Retired architecture policy

The S01–S10 folders, stage resolver, S-page creator, and S03/S04 probe tooling
are archive material. New work must not reference them. An old paper is migrated
only on explicit request, with the old files preserved and the new build checked.

After changing a Paper skill, run the static validators, repository checks, and
a realistic fresh-context agent test before calling it complete.
