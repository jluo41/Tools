# Paper skill family

`paper/` composes a manuscript from evidence-bearing Board Pages. The active
architecture is Page-first. The former numbered S-stage runtime was retired
and DELETED 260822 rather than parked; no `_old/` archive exists here.

## Active architecture

Six phases, each named by its authority page, gated by
`haipipe-paper-workflow` (journey 0.6.0, JL 260828); the venue bank is a
library outside the journey:

```text
P0 Ideation (ideate)     Story00 · the repo is minted with this page · sends one
                         idea to its Seed
P1 Story (establish)     Story<NN>-<idea> · THE STORY PAGE · one idea = one
                         paper (0.8.0) · holds the Seed (identity) · Research
                         Question table · E-board with novelty column
P2 Roadmap (route)       Story<NN>-roadmap · child of its Story · plan to COLLECT
                         · block rows serving RQ/E-rows · person-released · then
                         dispatch cards and receipts, lap by lap, on the same page
   ↺ P1↔P2 = the establish loop · exits only through the Seed at G4
P3 Narrative (tell)      Story<NN>-narrative-<desk> · child of its Story · plan
                         to SHOW · one per desk · §1 binds a bank Venue Page
P4 Section (realize)     one per map row · then assemble (a verb) at G6
P5 Round (respond)       in the desk's B group · routes each concern once →
                         Seed / Narrative / Section · gates G0-G7 in the
                         workflow file
```

Each Page runs the shared workflow and owns the evidence it uses:

```text
SHAPE ⇄ SURVEY ⇄ LAND ⇄ EMBED (the OUTLINE part) → WRITE → CHECK (the DRAFT part)

Evidence Item graph
├─ Supporting Runs   Execution/Discovery 0..N · planned at SURVEY
└─ Local Run         Page · Evidence Item exactly 1 · executed at LAND

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

## Paper layout (0.8.0 · JL 260907)

```text
Paper-<Slug>/                        no 0-paperboard/ wrapper · board.md at the root
├── board.md                         paper-root: .
├── A1-Story/
│   ├── Story00-ideation/            the idea pool
│   └── Story01-<idea-slug>/         one Story = one idea · seed + RQ table
│       ├── Story01-roadmap/         plan to collect → tasks/ · discoveries/
│       └── Story01-narrative-<desk>/  plan to show → Ba/Bb
├── Ba-<desk>-Main/  Bb-<desk>-Appendix/  Bc-<desk>-Round/
└── delivery/                        GENERATED from the Section Pages' own
    ├── paper-build.toml             delivery/latex/<page>.tex fragments
    ├── latex/                       master.tex · sections/ · displays/ · .bib · PDF
    └── word/                        .docx converted from latex/
```

## Active files

```text
paper/
├── haipipe-paper/
│   └── SKILL.md              one public Paper door and routing contract
├── haipipe-paper-workflow/
│   └── SKILL.md              the six-phase gate machine; transitions only
├── haipipe-paper-assemble/
│   ├── SKILL.md              complete-paper source-driven DOCX/PDF contract
│   └── ref/                   config example and assembly references
├── workflow-phases/          six journey-phase skills, each owning its
│   ├── haipipe-paper-ideation/     page-type key (JL 260831: replaces page-types/)
│   ├── haipipe-paper-story/       (was haipipe-paper-seed until 0.8.0)
│   ├── haipipe-paper-roadmap/
│   ├── haipipe-paper-narrative/
│   ├── haipipe-paper-section/
│   └── haipipe-paper-round/
│                             (retired literature/value/display/dash Page Types deleted 260822)
├── haipipe-paper-venue/   the one non-phase Page Type: a QBv bank record
├── venue/                    the shared QBv desk bank (bank/), prose playbooks,
│                             and the literature bank
└── TODO.md                   open issues future sessions pick up (task-family format)
```

## Family status

as of 2026-09-07 · regenerate with `/workflow-table paper` · this block is a dated receipt, never a second authority

```text
Part      Phase / Cycle            skill                    ver     L3 content it changes                      L4 Runs               human gate
A1-Story  P0 Ideation              haipipe-paper-ideation   0.6.2   Story00-ideation.md                        Discovery 0..N        G0 PROCEED
A1-Story  P1 Story (seed alias)    haipipe-paper-story      0.8.0   Story<NN>-<idea>.md · §3 RQ table · §6     Page Evidence 0..N    G1 outline tick
A1-Story  P2 Roadmap · collect     haipipe-paper-roadmap    0.6.3   Story<NN>-roadmap.md · parent "collect"    Execution/Discovery   G2 release blocks
A1-Story  P3 Narrative · show      haipipe-paper-narrative  0.8.3   Story<NN>-narrative-<desk>.md · "show"     none                  G4/G5 venue decision
Ba/Bb     P4 Section               haipipe-paper-section    0.8.4   S-<desk>-*.md · delivery/latex/<page>.tex  Page Evidence/Writing  outline v1.0 mint
delivery  assemble (verb)          haipipe-paper-assemble   0.3.0   none · writes build-manifest/qa            Delivery 1 per build  G6 decide to send
Bc        P5 Round send/respond/   haipipe-paper-round      0.5.0   RD<NN>.md · sent/ feedback/ released/      none                  G7 dispositions
          release
gates     all                      haipipe-paper-workflow   0.8.1   none                                       none                  —
door      all                      haipipe-paper            0.8.1   none                                       none                  —
library   consulted at P3          haipipe-paper-venue      0.6.0   QBv bank page                              none                  —
```

First repo on this layout: `examples/Project-Personality-OpioidRx/papers/Paper-AgreeablePrescription`. Static quality and fresh-context field tests have not been run for 0.8.x.

## Complete-paper document build

There are two different Word exports. `haipipe-plugin-delivery/ref/word.md` renders one Page
for coauthor review. `haipipe-paper-assemble` builds the complete manuscript
from the Section Pages' own `delivery/latex/<page>-complete.tex` files,
regenerating the paper's `delivery/latex/` whole (0.3.0). The latter is
deterministic and source-driven: generated Word files and section snapshots
are outputs only, never inputs. New papers should provide a small
`paper-build.toml` and select a venue profile; they should not copy a large
paper-specific `build_word.py`.

## Retired architecture policy

The S01–S10 folders, stage resolver, S-page creator, and S03/S04 probe tooling
are archive material. New work must not reference them. An old paper is migrated
only on explicit request, with the old files preserved and the new build checked.

After changing a Paper skill, run the static validators, repository checks, and
a realistic fresh-context agent test before calling it complete.
