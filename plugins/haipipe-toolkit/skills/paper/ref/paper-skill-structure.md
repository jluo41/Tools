# Paper Skill Structure

Target organization for `Tools/plugins/haipipe-toolkit/skills/paper`.

The skill tree should mirror the paper folder's durable lifecycle:

```text
paper/
├── haipipe-paper/               main router
├── ref/
│   ├── paper-lifecycle.md
│   ├── paper-rounds.md
│   └── paper-skill-structure.md
├── 0-enter/
│   └── haipipe-paper-enter/
├── 1-lifecycle/
│   ├── 0-seed/
│   ├── 1-pitch/
│   ├── 2-claims/
│   ├── 3-narrative/
│   ├── 4-figures-tables/
│   └── 5-minimap/
├── 2-rounds/
│   ├── haipipe-paper-round-enter/
│   ├── haipipe-paper-round-new/
│   ├── haipipe-paper-round-triage/
│   ├── haipipe-paper-round-apply/
│   └── haipipe-paper-round-close/
├── 3-write-edit/
├── 4-build-submit/
├── 5-respond/
└── 6-present/
```

## Current-To-Target Mapping

Do not rename all folders in one change. Keep existing skill names stable until
the target wrappers exist.

| Current | Target |
|---|---|
| `1-structure/haipipe-paper-enter` | `0-enter/haipipe-paper-enter` |
| `1-structure/*pitch*` | `1-lifecycle/1-pitch/` |
| `1-structure/*narrative*` | `1-lifecycle/3-narrative/` |
| `1-structure/*display*`, `*figure*`, `*table*` | `1-lifecycle/4-figures-tables/` |
| `3-edit/*` | `3-write-edit/` |
| `2-build/*check*`, compile components | `4-build-submit/` |
| `6-respond/*` | `5-respond/` |
| `7-present/*` | `6-present/` |

## Router Rule

`haipipe-paper` should first resolve paper status through `enter`. Then route
actions by the user's intended lifecycle object:

```text
status / enter / preload        -> 0-enter
seed / pitch / claims / minimap -> 1-lifecycle
round / todo / decisions        -> 2-rounds
write / edit / polish           -> 3-write-edit
compile / check / submit        -> 4-build-submit
rebuttal / response             -> 5-respond
slides / poster                 -> 6-present
```

## Maturity Rule

Every paper-aware response should report both:

```text
current_layer: 0-seed | 1-pitch | 2-claims | 3-narrative | 4-figures-tables | 5-minimap | sections/edit/build
maturity: prospectus | scaffold | claim-ledger | display-map | section-map | draft | submission-candidate | submitted | revision | accepted/published
```

Layer answers "where is the active work?"
Maturity answers "how real is the paper?"
