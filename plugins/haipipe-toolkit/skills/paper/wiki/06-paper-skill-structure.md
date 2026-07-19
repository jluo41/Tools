# Paper Skill Structure

How `Tools/plugins/haipipe-toolkit/skills/paper` is organized. The reconstruction
to this layout is complete.

The skill tree mirrors the lifecycle spine (`../1-lifecycle/ref/03-paper-lifecycle.md`,
`../1-lifecycle/ref/04-lifecycle-map.md`) on two axes: `1-lifecycle/` holds the STAGE orchestrators
(user-facing; define WHAT each stage delivers) and `2-phase/` holds the PHASE
workers (internal; define HOW: DRAFT -> PROBE -> REVISE -> CHECK). Inside those
two groups each numbered stage/phase folder holds its skills
(`paper/1-lifecycle/<N-stage>/<skill>/SKILL.md`); support groups stay flat
(`paper/<group>/<skill>/SKILL.md`).

```text
paper/
├── haipipe-paper/        router + Paper Console front door
├── PHILOSOPHY.md         design philosophy
├── README.md             canonical structure pointer
├── wiki/               shared references (dashboard, rounds, delivery-need, structure)
│   ├── 05-paper-dashboard.md      derive-from-disk frontier
│   ├── 07-paper-rounds.md         1-rounds/ contract
│   ├── 11-delivery-need.md        paper <-> probe/evidence interface
│   └── 06-paper-skill-structure.md
├── 0-enter/             haipipe-paper-enter (Console) + haipipe-paper-round
├── 1-lifecycle/         STAGE orchestrators, one numbered folder per stage
│     ref/               lifecycle references (03-paper-lifecycle, 04-lifecycle-map, 08-stage-gate, 09-stage-illuminate)
│     0-seed/haipipe-paper-seed
│     1a-resource/haipipe-paper-resource     (venue-FREE; stage 1a)
│     1b-claims/haipipe-paper-claims         (venue-FREE; stage 1b)
│     2a-venue/haipipe-paper-venue           (venue pin; venue-ALIGNED boundary; stage 2a)
│     2b-pitch/haipipe-paper-pitch            (venue-ALIGNED cover letter; stage 2b)
│     3-narrative/haipipe-paper-narrative
│     4-display/haipipe-paper-display + renderers
│       -display-{table,figure,diagram,illustration}
│       (illustration = Codex bridge;
│        framework candidate rounds inside display)
│     5-section-edit/haipipe-paper-section-edit + section-type/ norms
│     + haipipe-paper-lifecycle (orchestrator)
├── 2-phase/             PHASE workers (internal; driven by stage skills)
│     0-draft/haipipe-paper-draft  (retired write-* style skills live in 2-phase/_archive/)
│     1-probe/haipipe-paper-probe (+ -probe-{citation,display,values})
│     2-revise/haipipe-paper-revise (+ -revise-{content,humanizer,results,weaving})
│     3-check/haipipe-paper-check (+ haipipe-paper-proof-checker)
├── 3-deliver/      downstream of the argument, grouped by verb-intent:
│     1-build/   haipipe-paper-{scaffold,restructure,check,folder}   (structure the folder)
│     2-audit/   haipipe-paper-{claim-audit,submission-audit,reviewer,optimizer}   (read-only findings)
│     3-polish/  haipipe-paper-{consistency,format,typeset,improve-loop}   (mutate the draft)
│     4-ship/    haipipe-paper-{compile,diffpdf,to-overleaf}   (produce & move the artifact)
├── 4-respond/           haipipe-paper-rebuttal + paper-rebuttal + rebuttal-response
├── 5-present/           paper-slides + paper-poster
└── venue/             venue playbook packs (knowledge, not stages; consulted)
```

`venue/` is a paper-internal area, not a standalone layer. It is the venue
knowledge the lifecycle consults at pitch/narrative/display/section-edit/
submit/respond (`venue/playbook-<venue>`). Venues hold knowledge, never lifecycle
verbs. The old flat `paper/venue/` was reshaped into `venue/`. See
`venue/README.md` and `venue/_SCHEMA.md`.

## Stage to Procedure

Lifecycle stages map 1:1 to skills (full table in `../1-lifecycle/ref/04-lifecycle-map.md`):

```text
enter             -> 0-enter/haipipe-paper-enter
0-seed            -> 1-lifecycle/0-seed/haipipe-paper-seed
1-resource        -> 1-lifecycle/1a-resource/haipipe-paper-resource (venue-FREE; what must EXIST for the paper to be testable; is stage 1a, just before claims (1b))
1-claims          -> 1-lifecycle/1b-claims/haipipe-paper-claims
venue (choose+pin)-> 1-lifecycle/2a-venue/haipipe-paper-venue (recommend journal, write STATUS venue; after claims, before pitch; claims is venue-free)
2-pitch           -> 1-lifecycle/2b-pitch/haipipe-paper-pitch
3-narrative       -> 1-lifecycle/3-narrative/haipipe-paper-narrative
4-display         -> 1-lifecycle/4-display/haipipe-paper-display (+ render skills -display-{table,figure,diagram,illustration}[-gemini])
5-section-edit    -> 1-lifecycle/5-section-edit/haipipe-paper-section-edit (per-section DRAFT/PROBE/REVISE/CHECK)
review            -> 3-deliver/2-audit/ (claim-audit, submission-audit, reviewer, optimizer)
round             -> 0-enter/haipipe-paper-round
respond           -> 4-respond/*
present           -> 5-present/*
```

Every stage drives its phases through the `2-phase/` workers (never
user-invoked directly):

```text
DRAFT  -> 2-phase/0-draft/haipipe-paper-draft
PROBE  -> 2-phase/1-probe/haipipe-paper-probe    (runs the five-step loop ORGANIZE->MATCH->DISPATCH->POINT->INTERPRET;
                                                  DISPATCH goes DIRECT to Agent(haipipe-task-orchestrator-agent) /
                                                  Agent(haipipe-discovery-orchestrator-agent) — no gateway, and
                                                  /haipipe-probe is the CONSTITUTION, never a dispatch tier)
REVISE -> 2-phase/2-revise/haipipe-paper-revise
CHECK  -> 2-phase/3-check/haipipe-paper-check   (final human gate; DRAFT review is the other)
```

## Router Rule

`haipipe-paper` should first resolve paper status through `enter`. Then route
actions by the user's intended lifecycle object:

```text
status / enter / preload              -> 0-enter
seed / resource / claims / venue / pitch
  / narrative / figures / section-edit -> 1-lifecycle
round / todo / decisions              -> 0-enter/haipipe-paper-round
write / edit / revise (prose)         -> 1-lifecycle/5-section-edit (drives 2-phase/ workers)
review / audits                       -> 3-deliver/2-audit
scaffold / build / check              -> 3-deliver/1-build
polish / format / typeset             -> 3-deliver/3-polish
compile / diff / overleaf / ship      -> 3-deliver/4-ship
rebuttal / response                   -> 4-respond
slides / poster                       -> 5-present
venue / which journal / where submit  -> 1-lifecycle/2a-venue/haipipe-paper-venue  (recommend + pin STATUS venue)
  (the pinned venue's pack             -> venue/playbook-<venue>, consulted by each stage)
```

## Maturity Rule

Every paper-aware response should report both:

```text
current_layer: 0-seed | 1-resource | 1-claims | venue | 2-pitch | 3-narrative | 4-display | 5-section-edit | review/round
maturity: seed | resource | resource-blocked | scaffold | claim-ledger | display-map | section-edit | draft | submission-candidate | submitted | revision | accepted/published
```

Layer answers "where is the active work?"
Maturity answers "how real is the paper?"
