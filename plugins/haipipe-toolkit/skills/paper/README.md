# Paper skill family

`paper/` composes a manuscript from evidence-bearing Board Pages. The active
architecture is Page-first. The former numbered S-stage runtime is retired
under `_old/` and is never loaded by the current Paper door.

## Active architecture

Five phases, gated by `haipipe-paper-workflow`; the venue bank is a library
outside the journey (JL 260823):

```text
P0 Explore    explore page · head of the paper's own board (A0) · the repo
              is minted with this page · graduates one idea
P1 Establish  Seed · one per paper · venue-free · E-board with novelty column
P2 Tell       Narrative · one per desk · §1 binds a bank Venue Page
P3 Realize    Section Pages · one per map row · then assemble (a verb)
P4 Respond    Round · parented to a named Narrative · routes each concern
              once → Seed / Narrative / Section
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
│   └── SKILL.md              the five-phase gate machine; transitions only
├── page-types/
│   ├── haipipe-page-for-explore/
│   ├── haipipe-page-for-seed/
│   ├── haipipe-page-for-venue/
│   ├── haipipe-page-for-narrative/
│   ├── haipipe-page-for-section/
│   ├── haipipe-page-for-round/
│                             (retired literature/value/display/dash Page Types deleted 260822)
├── venue/                    reusable playbooks and exemplars
└── _old/                     retired stages and implementations; never auto-loaded
```

## Ownership

| Layer | Owns |
|---|---|
| `haipipe-paper` | Paper routing, Page graph, assembly, delivery |
| `haipipe-paper-workflow` | the five phases, their gates, phase receipts — never content |
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
