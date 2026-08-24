# Paper skill family

`paper/` composes a manuscript from evidence-bearing Board Pages. The active
architecture is Page-first. The former numbered S-stage runtime is retired
under `_old/` and is never loaded by the current Paper door.

## Active architecture

Seven phases, each named by its authority page, gated by
`haipipe-paper-workflow` (journey 0.5.0, JL 260824); the venue bank is a
library outside the journey:

```text
P0 Ideation (ideate)     SD00 · the repo is minted with this page · sends one
                         idea to its Seed
P1 Seed (establish)      SD01 · one per paper · venue-free · E-board with
                         novelty column
P2 Roadmap (route)       SD02 · direction rows serving E-rows · person-released
P3 Collection (collect)  SD03 · dispatch cards · receipts registered lap by lap
   ↺ P1↔P2↔P3 = the establish loop · exits only through the Seed at G4
P4 Narrative (tell)      NA · one per desk · §1 binds a bank Venue Page
P5 Section (realize)     one per map row · then assemble (a verb) at G6
P6 Round (respond)       in the desk's B group · routes each concern once →
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
│   └── SKILL.md              the seven-phase gate machine; transitions only
├── page-types/
│   ├── haipipe-page-for-ideation/
│   ├── haipipe-page-for-seed/
│   ├── haipipe-page-for-roadmap/
│   ├── haipipe-page-for-collection/
│   ├── haipipe-page-for-venue/
│   ├── haipipe-page-for-narrative/
│   ├── haipipe-page-for-section/
│   ├── haipipe-page-for-round/
│                             (retired literature/value/display/dash Page Types deleted 260822)
├── venue/                    reusable playbooks and exemplars
├── TODO.md                   open issues future sessions pick up (task-family format)
└── _old/                     retired stages and implementations; never auto-loaded
```

## Ownership

| Layer | Owns |
|---|---|
| `haipipe-paper` | Paper routing, Page graph, assembly, delivery |
| `haipipe-paper-workflow` | the seven phases, their gates, phase receipts — never content |
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
