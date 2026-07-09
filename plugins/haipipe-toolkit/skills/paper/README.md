# Paper Skill

Canonical reference. This file + `wiki/` win over anything elsewhere.

A paper is a delivery contract, not a writing folder. It owns one manuscript's story, claims, displays, minimap, and prose. Evidence lives in tasks/discoveries/insights at the project level; each stage's _PROBE/PPNN card carries contract + receipt + verdict. Claim gaps buffer in `1-probe-plans/` and batch-dispatch to probe (the universal evidence gateway; probe calls task/discover during Gather). Direct task/discover for non-claim utility work only.

## The mission-controller metaphor

Each lifecycle stage is a **mission controller for one aim** — its artifact and that artifact's done-criteria — releasing probes as satellites until the result is solid (JL 2026-07-09).

- Same control room everywhere: every stage drives DRAFT → PROBE → REVISE → CHECK; only the mission target changes (seed doc, claims ledger, pitch, narrative, display map, section prose).
- Satellites, not sorties: during PROBE the stage launches probe plans through the evidence gateway into project space — task probes fly internal space (runs, data, models), discovery probes fly external space (literature). Mission control never leaves home: it plans, dispatches, collects returns, backfills.
- Rounds until green: DPRC cycles repeat until the CHECK gate passes, then the controller hands off to the next stage.
- Fleet sizes differ: `1-claims` runs the biggest constellation — mission control targeting solid claims, exit gate "every claim solid or scheduled"; `4-display` is the other heavy-launch stage (units materialized via tasks); pitch/narrative fly light audit probes over territory the claims fleet already mapped.

## Paper-folder layout

```text
<paper-root>/
├── STATUS.md                current layer, maturity, active round
├── 0-<paper>.tex/.bib       main manuscript shell
├── 0-lifecycle/              maturation spine (md + _LOG; display = tex + pdf)
│   ├── 0-seed/  1-claims/  2-pitch/  3-narrative/  4-display/  5-editing/
├── 0-sections/               manuscript prose .tex
├── 0-displays/displayNN-*/   figure/table units
├── 1-probe-plans/PPNN_*.md   evidence-need buffer -> batch-dispatch to probe
├── 1-rounds/vYYMMDD/         work rounds (discussion, decisions, todo, applied)
├── 1-config.yaml
└── 1-compile.sh
```

`0-` = source of truth (content). `1-` = process (build + revise).

## Skill-tree layout

```text
paper/
├── haipipe-paper/    router + Paper Console
├── 0-enter/          Paper Console (haipipe-paper-enter)
├── 1-lifecycle/      stage procedures (seed, claims, pitch, narrative, display)
│                     + display renderers (-table, -figure, -diagram, -illustration)
├── 2-phase/          shared phase workers: DRAFT-PROBE-REVISE-CHECK (DPRC)
│                     haipipe-paper-{draft,probe,revise,check} + sub-workers
├── 3-build-submit/   scaffold, restructure, check
├── 4-respond/        rebuttal, response
├── 5-present/        slides, poster
├── _venue/           venue profiles (knowledge, not verbs) — see _venue/README.md
├── components/       citation, compile, diff
└── wiki/             lifecycle, rounds, skill-structure, lifecycle-map
```

## References

| File | Read it for |
|---|---|
| `wiki/03-paper-lifecycle.md` | stage spine, maturity ladder, loopback rule, evidence-worker handoff |
| `wiki/07-paper-rounds.md` | `1-rounds/` contract, file semantics, triage targets |
| `wiki/06-paper-skill-structure.md` | skill-tree target, router rule, maturity rule |
| `wiki/04-lifecycle-map.md` | stage-to-procedure map with reads/writes/calls |

## Retired names

| Retired | Use instead |
|---|---|
| `1-feedback/` | `1-rounds/` |
| `architecture-minimap`, `paper-plan`, `display-contract` | `2-claims`, `3-narrative`, `4-display`, `5-minimap` |
| `0-displays/Figures/` `Tables/` buckets | `0-displays/displayNN-<slug>/` |
| project-level narrative coordination | paper owns its story; gaps route to probe |
| `haipipe-paper-{conference,journal,is}` | `_venue/playbook-<venue>` + lifecycle verbs |
| `haipipe-paper-{create,revise}` | `3-write-edit/haipipe-paper-edit-{write,weaving}` |
