# Application Skill Structure

How `Tools/plugins/haipipe-toolkit/skills/application` is organized. Mirrors `../../paper/wiki/06-paper-skill-structure.md`; the paper-alignment refactor to this layout landed 2026-07-06 (SOP archived in `../haipipe-application/CHANGELOG.md` §5.0.0).

The skill tree mirrors the lifecycle spine on two axes: `1-lifecycle/` holds the STAGE orchestrators (user-facing; define WHAT each stage delivers) and `2-phase/` holds the PHASE workers (internal; define HOW: DRAFT -> PROBE -> REVISE -> CHECK). Inside those two groups each numbered stage/phase folder holds its skills; support groups stay flat.

```text
application/
├── haipipe-application/   router + Intervention Console front door + stage-strip.sh + fn/ + PREFERENCES.md
├── README.md              canonical structure pointer
├── PHILOSOPHY.md          design philosophy
├── wiki/
│   ├── 03-intervention-lifecycle.md   stage spine + venue gating + maturity
│   ├── 05-intervention-dashboard.md   derive-from-disk frontier
│   ├── 06-application-skill-structure.md
│   ├── 08-stage-gate.md               Gate Ledger + venue-scaled depth
│   └── 11-delivery-need.md            application <-> probe interface
├── 0-enter/               haipipe-application-enter (Console) + haipipe-application-round
├── 1-lifecycle/           STAGE orchestrators, one numbered folder per stage
│     0-seed/haipipe-application-seed                (venue-FREE)
│     1-claims/haipipe-application-claims            (venue-FREE)
│     2-pitch/haipipe-application-pitch              (venue-ALIGNED)
│     3-narrative/haipipe-application-narrative      (venue-GATED)
│     4-display/haipipe-application-display          (venue-GATED; owns per-unit jobs)
│     5-section-edit/haipipe-application-section-edit (sectioned venues)
│     + haipipe-application-venue (pin modality + stages_skipped + claims_settlement; writes 2-venue/2-venue.md Artifact Principles; after claims, before pitch)
│     + haipipe-application-lifecycle (orchestrator)
├── 2-phase/               PHASE workers (internal; driven by stage skills)
│     README.md + USAGE.md + WIRING.md    (bucket-root docs: architecture, recipes, wiring)
│     0-draft/haipipe-application-draft
│     1-probe/haipipe-application-probe   (the ONLY evidence door; + check-probe-cards.sh, ref/)
│     2-revise/haipipe-application-revise
│     3-check/haipipe-application-check   (+ checks.sh, gate-persona.md, attendance-modes.md)
├── 3-build-deploy/        haipipe-application-artifact (the `draft` verb) + review + claim-audit + deploy
├── 4-iterate/             haipipe-application-iterate (post-deploy A/B refinement)
├── _venue/                venue packs (knowledge, not stages; README + style-profile [+ exemplars])
├── _audience/             audience packs (knowledge) + audience-requirements.md
└── _archive/              retired: haipipe-application-ask (+ its refs), haipipe-application-minimap
```

## Stage to Procedure

```text
enter             -> 0-enter/haipipe-application-enter
0-seed            -> 1-lifecycle/0-seed/haipipe-application-seed
1-claims          -> 1-lifecycle/1-claims/haipipe-application-claims
venue (pin)       -> 1-lifecycle/haipipe-application-venue (after claims, before pitch; claims is venue-free; writes 0-lifecycle/2-venue/2-venue.md)
2-pitch           -> 1-lifecycle/2-pitch/haipipe-application-pitch
3-narrative       -> 1-lifecycle/3-narrative/haipipe-application-narrative      (venue-gated)
4-display         -> 1-lifecycle/4-display/haipipe-application-display          (venue-gated)
5-section-edit    -> 1-lifecycle/5-section-edit/haipipe-application-section-edit (sectioned venues)
draft (artifact)  -> 3-build-deploy/haipipe-application-artifact
review / audit    -> 3-build-deploy/haipipe-application-{review,claim-audit}
deploy            -> 3-build-deploy/haipipe-application-deploy
round             -> 0-enter/haipipe-application-round
iterate           -> 4-iterate/haipipe-application-iterate
```

Every stage drives its phases through the `2-phase/` workers (never user-invoked directly):

```text
DRAFT  -> 2-phase/0-draft/haipipe-application-draft
PROBE  -> 2-phase/1-probe/haipipe-application-probe   (runs the five-step loop ORGANIZE->MATCH->DISPATCH->POINT->INTERPRET;
                                                       DISPATCH goes DIRECT to Agent(haipipe-task-orchestrator-agent) /
                                                       Agent(haipipe-discovery-orchestrator-agent) — the probe gateway
                                                       agent is RETIRED, and /haipipe-probe is the CONSTITUTION, not a
                                                       dispatch tier)
REVISE -> 2-phase/2-revise/haipipe-application-revise
CHECK  -> 2-phase/3-check/haipipe-application-check   (the only human-involved phase; writes the Gate Ledger)
```

## Router Rule

`haipipe-application` should first resolve intervention status through `enter`. Then route actions by the user's intended lifecycle object:

```text
status / enter / preload                    -> 0-enter
seed / claims / venue / pitch
  / narrative / display / section-edit      -> 1-lifecycle
round / todo / decisions                    -> 0-enter/haipipe-application-round
draft / write / make the <venue>            -> 3-build-deploy/haipipe-application-artifact
review / claim-audit / deploy               -> 3-build-deploy
iterate / A/B                               -> 4-iterate
probe / evidence gap                        -> a question SECTION in 1-probes/; `run` -> 2-phase/1-probe worker
venue / which channel                       -> 1-lifecycle/haipipe-application-venue
  (the pinned venue's pack                  -> _venue/venue-<name>, consulted by each aligned stage)
```

## Maturity Rule

Every application-aware response should report both:

```text
current_layer: 0-seed | 1-claims | venue | 2-pitch | 3-narrative | 4-display | 5-section-edit | draft | review | deploy
maturity: prospect | claim-ledger | venue-pinned | pitched | narrated | display-mapped | section-edit | drafted | reviewed | deployed | iterating | retired
```

Layer answers "where is the active work?" Maturity answers "how real is the intervention?"
