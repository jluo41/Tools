# Paper Skill Structure

How `Tools/plugins/haipipe-toolkit/skills/paper` is organized. The reconstruction
to this layout is complete.

The skill tree mirrors the lifecycle spine (`paper-lifecycle.md`,
`lifecycle-map.md`). Skills stay flat inside each group (depth 2,
`paper/<group>/<skill>/SKILL.md`), so `../../ref/` and skill-local refs resolve
uniformly. Stage identity is carried by the skill name, not a nested stage folder.

```text
paper/
├── haipipe-paper/        router + Paper Console front door
├── PHILOSOPHY.md         design philosophy
├── README.md             canonical structure pointer
├── ref/
│   ├── paper-lifecycle.md      stage spine + maturity
│   ├── lifecycle-map.md        stage -> procedure/reads/writes/calls/gate
│   ├── paper-dashboard.md      derive-from-disk frontier
│   ├── paper-rounds.md         1-rounds/ contract
│   ├── delivery-need.md        paper <-> probe/evidence interface
│   └── paper-skill-structure.md
├── 0-enter/             haipipe-paper-enter (Console)
├── 1-lifecycle/         one skill per stage + display renderers
│     haipipe-paper-{seed,pitch,venue,claims,narrative,display,minimap}
│       (venue = recommend + pin the best-fit journal, before claims)
│     + display renderers: -display-{table,figure,diagram,illustration}
│       (illustration default = Codex; -display-illustration-gemini = fallback;
│        framework candidate rounds inside display)
│     + haipipe-paper-lifecycle (orchestrator)
│     (architecture+plan folded into minimap/ref; figure-planner into
│      display/ref; diagram moved to 3-write-edit; incubator retired)
├── 2-rounds/            haipipe-paper-round (enter/new/triage/apply/close)
├── 3-write-edit/        edit family + write* + review cluster + sections/ playbooks
│     review cluster: edit-{claim-audit,reviewer,proof-checker,submission-audit,
│                     manual-review-citations,manual-review-values,check-reference}
├── 4-build-submit/      haipipe-paper-folder + build-{scaffold,restructure,check}
├── 5-respond/           paper-rebuttal + rebuttal-response
├── 6-present/           paper-slides + paper-poster
├── _venue/             venue profiles (knowledge, not stages; consulted)
└── components/          citation, compile, diff (cross-cutting)
```

`_venue/` is a paper-internal area, not a standalone layer. It is the venue
knowledge the lifecycle consults at pitch/claims/narrative/display/write/submit/
respond (`_venue/playbook-<venue>`). Venues hold knowledge, never lifecycle
verbs. The old flat `paper/_venue/` was reshaped into `_venue/`. See
`_venue/README.md` and `_venue/_SCHEMA.md`.

## Stage to Procedure

Lifecycle stages map 1:1 to skills (full table in `lifecycle-map.md`):

```text
enter             -> 0-enter/haipipe-paper-enter
0-seed            -> 1-lifecycle/haipipe-paper-seed
1-pitch           -> 1-lifecycle/haipipe-paper-pitch
venue (choose+pin)-> 1-lifecycle/haipipe-paper-venue (recommend journal, write STATUS venue; before claims)
2-claims          -> 1-lifecycle/haipipe-paper-claims
3-narrative       -> 1-lifecycle/haipipe-paper-narrative
4-display         -> 1-lifecycle/haipipe-paper-display (+ render skills -display-{table,figure,diagram,illustration}[-gemini]; figure-logic ref)
5-minimap         -> 1-lifecycle/haipipe-paper-minimap (folds in architecture-blueprint + plan-outline refs)
write/edit        -> 3-write-edit/*
review            -> 3-write-edit/ (the audit cluster)
round             -> 2-rounds/haipipe-paper-round
respond           -> 5-respond/*
present           -> 6-present/*
```

## Router Rule

`haipipe-paper` should first resolve paper status through `enter`. Then route
actions by the user's intended lifecycle object:

```text
status / enter / preload              -> 0-enter
seed / pitch / claims / narrative
  / figures / minimap                 -> 1-lifecycle
round / todo / decisions              -> 2-rounds
write / edit / review / polish        -> 3-write-edit
  (create/revise prose -> haipipe-paper-edit-{write,weaving})
scaffold / build / check / compile    -> 4-build-submit
rebuttal / response                   -> 5-respond
slides / poster                       -> 6-present
venue / which journal / where submit  -> 1-lifecycle/haipipe-paper-venue  (recommend + pin STATUS venue)
  (the pinned venue's pack             -> _venue/playbook-<venue>, consulted by each stage)
```

## Maturity Rule

Every paper-aware response should report both:

```text
current_layer: 0-seed | 1-pitch | 2-claims | 3-narrative | 4-display | 5-minimap | sections/edit/build
maturity: prospectus | scaffold | claim-ledger | display-map | section-map | draft | submission-candidate | submitted | revision | accepted/published
```

Layer answers "where is the active work?"
Maturity answers "how real is the paper?"
